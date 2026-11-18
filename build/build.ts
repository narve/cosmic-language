// Builds docs/ from the sources: copies assets/, renders lessons/ and templates/, writes the message.
// docs/ holds only generated files (apart from .gitkeep).
import { cpSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { defineClLessons } from "./components/cl-lessons.ts";
import { BuildError, createWindow, parse, serialize } from "./dom.ts";
import { findArticle, loadArticles, loadTopics } from "./lessons.ts";
import { binaryDump, messageBinary, messageBits, messageStream, messageCode, messageText, readBlock, type Message } from "./message.ts";
import { loadRegistry } from "./registry.ts";
import { addViews, VIEWS } from "./views.ts";
import { checkMinimal, checkOptional, checkSelfReference, checkStructure } from "./check/structure.ts";
import { checkMeasurements, MARGIN } from "./check/measurements.ts";

const root = resolve(import.meta.dirname, "..");
const dir = (name: string) => join(root, name);
const docs = dir("docs");

async function build(): Promise<void> {
  const window = createWindow();
  const registry = loadRegistry(window, readFileSync(join(dir("templates"), "specification.html"), "utf8"));
  const topics = loadTopics(window, readFileSync(join(dir("templates"), "topics.html"), "utf8"));
  const articles = loadArticles(window, dir("lessons"), topics);

  for (const entry of readdirSync(docs)) if (entry !== ".gitkeep") rmSync(join(docs, entry), { recursive: true });
  cpSync(dir("assets"), join(docs, "assets"), { recursive: true });

  // The message, from the message blocks in file order.
  const message: Message = {
    articles: articles.map((article) => {
      const element = findArticle(parse(window, article.source), article.slug);
      const blocks = messageCode(element).map((code, i) => readBlock(code, registry, `${article.slug}, block ${i + 1}`));
      return { article, blocks };
    }),
    topics,
  };
  // The structure rules of the specification (§10.1): hard errors.
  checkStructure(message, registry);

  // Three versions of the message. Full: every lesson (docs/message.*). Cautious: everything except the optional
  // lessons, which reveal where and who we are (docs/cautious/). Minimal: only the game and what it needs, the lessons
  // with the topic "minimal" (docs/minimal/).
  const MINIMAL = "minimal";
  const inMinimal = new Set(articles.filter((article) => article.topics.includes(MINIMAL)).map((article) => article.slug));
  checkMinimal(message, (slug) => inMinimal.has(slug));
  const optional = new Set(articles.filter((article) => article.optional).map((article) => article.slug));
  checkOptional(message, (slug) => optional.has(slug));
  const minimal: Message = { articles: message.articles.filter(({ article }) => inMinimal.has(article.slug)), topics };
  const minimalBinary = messageBinary(messageStream(minimal));
  const cautious: Message = { articles: message.articles.filter(({ article }) => !optional.has(article.slug)), topics };
  const cautiousBinary = messageBinary(messageStream(cautious));
  // What each version says about itself must hold for that version.
  const selfReferences = [checkSelfReference(message, "full"), checkSelfReference(cautious, "cautious"), checkSelfReference(minimal, "minimal")];
  const bits = messageBits(message);
  const binary = messageBinary(messageStream(message));
  // A byte order mark, so browsers read these plain-text files as UTF-8 (≠, ∀, π …) instead of guessing.
  const BOM = "\ufeff";
  writeFileSync(join(docs, "message.txt"), BOM + messageText(message));
  // Every measured range must hold for the reference data, with room to spare (§10.1).
  const measurements = checkMeasurements(messageText(message));
  if (measurements.failures > 0) {
    const failing = measurements.report.filter((line) => !line.startsWith("ok"));
    throw new BuildError(`${measurements.failures} measured ranges fail (each bound must be at least ${MARGIN} standard uncertainties from the reference value):\n${failing.join("\n")}`);
  }
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

  // Each lesson page as written, with the generated views added.
  mkdirSync(join(docs, "lessons"));
  for (const article of articles) {
    const document = parse(window, article.source);
    addViews(findArticle(document, article.slug), registry, [...VIEWS], article.slug);
    writeFileSync(join(docs, "lessons", `${article.slug}.html`), serialize(document));
  }

  // Templates, with their custom elements rendered.
  for (const file of readdirSync(dir("templates")).filter((f) => f.endsWith(".html"))) {
    const page = createWindow();
    page.document.write(readFileSync(join(dir("templates"), file), "utf8"));
    defineClLessons(page, { articles, topics, registry });
    await page.happyDOM.waitUntilComplete();
    writeFileSync(join(docs, file), serialize(page.document as unknown as Document));
    await page.happyDOM.close();
  }
  await window.happyDOM.close();

  const tokens = message.articles.reduce((n, a) => n + a.blocks.reduce((m, b) => m + b.tokens.length, 0), 0);
  console.log(`${articles.length} articles, ${tokens} tokens, ${binary.length} bits (${binary.bytes.length} bytes)`);
  const minimalTokens = minimal.articles.reduce((n, a) => n + a.blocks.reduce((m, b) => m + b.tokens.length, 0), 0);
  console.log(`measurements: ${measurements.checked} ranges, all at least ${MARGIN} standard uncertainties inside their bounds`);
  console.log(`about itself: ${selfReferences.join(", ")} sentences checked (full, cautious, minimal)`);
  console.log(`cautious: ${cautious.articles.length} articles, ${cautiousBinary.length} bits (${cautiousBinary.bytes.length} bytes)`);
  console.log(`minimal: ${minimal.articles.length} articles, ${minimalTokens} tokens, ${minimalBinary.length} bits (${minimalBinary.bytes.length} bytes)`);
}

try {
  await build();
} catch (error) {
  if (!(error instanceof BuildError)) throw error;
  console.error(`build failed: ${error.message}`);
  process.exit(1);
}
