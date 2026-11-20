// Builds docs/ from site/, which has the same layout: copies site/assets/, renders site/lessons/ and the pages in site/, writes the message.
// docs/ holds only generated files: the build deletes it and makes it again.
import { cpSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { defineClLessons } from "./components/cl-lessons.ts";
import { defineClVocabulary } from "./components/cl-vocabulary.ts";
import { BuildError, createWindow, parse, serialize } from "./dom.ts";
import { findArticle, loadArticles, loadTopics } from "./lessons.ts";
import { binaryDump, messageBinary, messageBits, messageStream, messageCode, messageText, readBlock, type Message } from "./message.ts";
import { loadRegistry } from "./registry.ts";
import { VIEWS } from "./views.ts";
import { enrichArticle } from "./enrich.ts";
import { computeUsage } from "./usage.ts";
import { runCheckers } from "./check/checkers.ts";

const root = resolve(import.meta.dirname, "..");
const dir = (name: string) => join(root, name);
const docs = dir("docs");
const site = dir("site"); // the sources of the pages, laid out like docs/, so relative links work in both

async function build(): Promise<void> {
  const window = createWindow();
  const registry = loadRegistry();
  const topics = loadTopics(window, readFileSync(join(site, "topics.html"), "utf8"));
  const all = loadArticles(window, join(site, "lessons"), topics);
  // Lessons that replace another (data-replaces) are only in the decoy version.
  const articles = all.filter((article) => !article.replaces);
  const replacements = new Map(all.filter((article) => article.replaces).map((article) => [article.replaces!, article]));

  rmSync(docs, { recursive: true, force: true });
  mkdirSync(docs);
  cpSync(join(site, "assets"), join(docs, "assets"), { recursive: true });

  // The message, from the message blocks in file order.
  const read = (article: (typeof all)[number]) => {
    const element = findArticle(parse(window, article.source), article.slug);
    const blocks = messageCode(element).map((code, i) => readBlock(code, registry, `${article.slug}, block ${i + 1}`));
    return { article, blocks };
  };
  const message: Message = { articles: articles.map(read), topics };
  // Decoy: the full message with each replaced lesson swapped for its replacement, in the same place: for fun, to see
  // whether a blind reader places the sender at another star. Its measured ranges are not checked.
  const decoy: Message = { articles: articles.map((article) => read(replacements.get(article.slug) ?? article)), topics };

  // Three versions of the message. Full: every lesson (docs/message.*). Cautious: everything except the optional
  // lessons, which reveal where and who we are (docs/cautious/). Minimal: only the game and what it needs, the lessons
  // with the topic "minimal" (docs/minimal/).
  const MINIMAL = "minimal";
  const inMinimal = new Set(articles.filter((article) => article.topics.includes(MINIMAL)).map((article) => article.slug));
  const optional = new Set(articles.filter((article) => article.optional).map((article) => article.slug));
  const minimal: Message = { articles: message.articles.filter(({ article }) => inMinimal.has(article.slug)), topics };
  const minimalBinary = messageBinary(messageStream(minimal));
  const cautious: Message = { articles: message.articles.filter(({ article }) => !optional.has(article.slug)), topics };
  const cautiousBinary = messageBinary(messageStream(cautious));
  // The checks (build/check/checkers.ts): hard errors. CHECKS=… or SKIP_CHECKS=… chooses among them.
  const checks = runCheckers({
    versions: { full: message, cautious, minimal, decoy },
    text: { full: messageText(message), cautious: messageText(cautious), minimal: messageText(minimal), decoy: messageText(decoy) },
    registry,
    isMinimal: (slug) => inMinimal.has(slug),
    isOptional: (slug) => optional.has(slug),
  });
  const decoyBinary = messageBinary(messageStream(decoy));
  const bits = messageBits(message);
  const binary = messageBinary(messageStream(message));
  // A byte order mark, so browsers read these plain-text files as UTF-8 (≠, ∀, π …) instead of guessing.
  const BOM = "\ufeff";
  writeFileSync(join(docs, "message.txt"), BOM + messageText(message));
  writeFileSync(join(docs, "message.bits"), BOM + bits);
  writeFileSync(join(docs, "message.bin"), binary.bytes);
  writeFileSync(join(docs, "message.bin.txt"), binaryDump(binary));
  mkdirSync(join(docs, MINIMAL));
  writeFileSync(join(docs, MINIMAL, "message.txt"), BOM + messageText(minimal));
  writeFileSync(join(docs, MINIMAL, "message.bits"), BOM + messageBits(minimal));
  writeFileSync(join(docs, MINIMAL, "message.bin"), minimalBinary.bytes);
  writeFileSync(join(docs, MINIMAL, "message.bin.txt"), binaryDump(minimalBinary));
  mkdirSync(join(docs, "cautious"));
  writeFileSync(join(docs, "cautious", "message.txt"), BOM + messageText(cautious));
  writeFileSync(join(docs, "cautious", "message.bits"), BOM + messageBits(cautious));
  writeFileSync(join(docs, "cautious", "message.bin"), cautiousBinary.bytes);
  writeFileSync(join(docs, "cautious", "message.bin.txt"), binaryDump(cautiousBinary));
  mkdirSync(join(docs, "decoy"));
  writeFileSync(join(docs, "decoy", "message.txt"), BOM + messageText(decoy));
  writeFileSync(join(docs, "decoy", "message.bits"), BOM + messageBits(decoy));
  writeFileSync(join(docs, "decoy", "message.bin"), decoyBinary.bytes);
  writeFileSync(join(docs, "decoy", "message.bin.txt"), binaryDump(decoyBinary));

  // Where each symbol is introduced and used, for the vocabulary page and the lessons.
  const usage = computeUsage(message, replacements);

  // Each lesson page as written, with the generated views added.
  mkdirSync(join(docs, "lessons"));
  for (const article of all) {
    const document = parse(window, article.source);
    enrichArticle(findArticle(document, article.slug), article, [...VIEWS], { registry, usage, base: "../" });
    writeFileSync(join(docs, "lessons", `${article.slug}.html`), serialize(document));
  }

  // Templates, with their custom elements rendered.
  for (const file of readdirSync(site).filter((f) => f.endsWith(".html"))) {
    const page = createWindow();
    page.document.write(readFileSync(join(site, file), "utf8"));
    defineClLessons(page, { articles, topics, registry, usage });
    defineClVocabulary(page, usage);
    await page.happyDOM.waitUntilComplete();
    writeFileSync(join(docs, file), serialize(page.document as unknown as Document));
    await page.happyDOM.close();
  }
  await window.happyDOM.close();

  const tokens = message.articles.reduce((n, a) => n + a.blocks.reduce((m, b) => m + b.tokens.length, 0), 0);
  console.log(`${articles.length} articles, ${tokens} tokens, ${binary.length} bits (${binary.bytes.length} bytes)`);
  const minimalTokens = minimal.articles.reduce((n, a) => n + a.blocks.reduce((m, b) => m + b.tokens.length, 0), 0);
  console.log(`decoy: ${decoy.articles.length} articles, ${decoyBinary.length} bits (${decoyBinary.bytes.length} bytes), ${replacements.size} ${replacements.size === 1 ? "lesson" : "lessons"} replaced`);
  console.log(`cautious: ${cautious.articles.length} articles, ${cautiousBinary.length} bits (${cautiousBinary.bytes.length} bytes)`);
  console.log(`minimal: ${minimal.articles.length} articles, ${minimalTokens} tokens, ${minimalBinary.length} bits (${minimalBinary.bytes.length} bytes)`);
  for (const line of checks) console.log(`check ${line}`);
}

try {
  await build();
} catch (error) {
  if (!(error instanceof BuildError)) throw error;
  console.error(`build failed: ${error.message}`);
  process.exit(1);
}
