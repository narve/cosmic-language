// Builds docs/ from site/, which has the same layout: copies site/assets/, renders site/lessons/ and the pages in site/, writes the message.
// docs/ holds only generated files: the build deletes it and makes it again.
import { cpSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { defineClLessons } from "./components/cl-lessons.ts";
import { defineClVocabulary } from "./components/cl-vocabulary.ts";
import { defineClFiles } from "./components/cl-files.ts";
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

// The pages of site/: every .html file outside lessons/ and assets/, as paths relative to site/.
function pages(folder: string): string[] {
  return readdirSync(folder, { recursive: true, encoding: "utf8" })
    .filter((file) => file.endsWith(".html") && !/^(lessons|assets)\//.test(file))
    .map((file) => relative(folder, join(folder, file)).split("\\").join("/"));
}

// The sections of site/versions.html with an id: one per version, its title (h2) and its text, without the h2,
// subheadings and lesson lists. Its links are written from docs/, so they get "../" to work from docs/<version>/.
function loadVersions(window: ReturnType<typeof createWindow>, html: string): { name: string; title: string; intro: string }[] {
  const document = parse(window, html);
  return Array.from(document.querySelectorAll("main > section[id]"), (section) => {
    const copy = section.cloneNode(true) as Element;
    const title = copy.querySelector("h2")?.textContent?.trim() ?? section.id;
    copy.querySelectorAll("h2, h3, cl-lessons").forEach((element) => element.remove());
    for (const link of copy.querySelectorAll("a[href]")) {
      const href = link.getAttribute("href")!;
      if (!/^([a-z]+:|#|\/)/.test(href)) link.setAttribute("href", `../${href}`);
    }
    return { name: section.id, title, intro: copy.innerHTML.trim() };
  });
}

// The page of one version, written from docs/<version>/.
function versionPage(name: string, title: string, intro: string): string {
  const heading = `The ${title.toLowerCase()} message`;
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${heading} · Cosmic Language</title>
  <link rel="stylesheet" href="../assets/style.css">
  <link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
  <script src="../assets/views.js" defer></script>
</head>
<body>

<header>
  <small>Draft · the ${name} version</small>
  <h1>${heading}</h1>
  ${intro}
  <p>All its lessons on one page, in the order of the message, each with what it sends. The exact rules are in the <a href="../specification.html">specification</a>; all versions are compared on <a href="../versions.html">versions</a>.</p>
</header>

<nav aria-label="Contents">
  <cl-lessons version="${name}" as="links" href="anchor" group="runs"></cl-lessons>
</nav>

<main>
  <cl-lessons version="${name}" as="articles" group="runs"></cl-lessons>
</main>

<footer>cosmic-language · ${name} version · draft</footer>
</body>
</html>
`;
}

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
  // Decoy: the full message with each replaced lesson swapped for its replacement, in the same place, and the lessons
  // marked data-not-in-decoy left out: for fun, to see whether a blind reader places the sender at another star.
  const decoyArticles = articles.filter((article) => !article.notInDecoy).map((article) => replacements.get(article.slug) ?? article);
  const decoy: Message = { articles: decoyArticles.map(read), topics };

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

  // The lessons of each version, in message order, for the version pages (docs/full/, docs/minimal/ …).
  const versions = {
    full: articles,
    cautious: articles.filter((article) => !optional.has(article.slug)),
    minimal: articles.filter((article) => inMinimal.has(article.slug)),
    decoy: decoyArticles,
  };

  // Where each version's message files are, and its length in bits, for <cl-files>.
  const files = {
    full: { dir: "", bits: binary.length },
    cautious: { dir: "cautious", bits: cautiousBinary.length },
    minimal: { dir: MINIMAL, bits: minimalBinary.length },
    decoy: { dir: "decoy", bits: decoyBinary.length },
  };

  // A page with its custom elements rendered, written to docs/<file>.
  const render = async (html: string, file: string) => {
    const page = createWindow();
    page.document.write(html);
    const base = "../".repeat(file.split("/").length - 1);
    defineClLessons(page, { articles, versions, topics, registry, usage, base });
    defineClVocabulary(page, usage);
    defineClFiles(page, { docs, base, versions: files });
    await page.happyDOM.waitUntilComplete();
    mkdirSync(join(docs, dirname(file)), { recursive: true });
    writeFileSync(join(docs, file), serialize(page.document as unknown as Document));
    await page.happyDOM.close();
  };

  // The pages of site/ (outside lessons/ and assets/), at the same place in docs/.
  for (const file of pages(site)) await render(readFileSync(join(site, file), "utf8"), file);

  // One page per version, docs/<version>/index.html: all its lessons, made from its section in site/versions.html.
  for (const { name, title, intro } of loadVersions(window, readFileSync(join(site, "versions.html"), "utf8"))) {
    if (!(name in versions)) throw new BuildError(`site/versions.html: <section id="${name}"> is not a version`);
    await render(versionPage(name, title, intro), `${name}/index.html`);
  }
  await window.happyDOM.close();

  const tokens = message.articles.reduce((n, a) => n + a.blocks.reduce((m, b) => m + b.tokens.length, 0), 0);
  console.log(`${articles.length} articles, ${tokens} tokens, ${binary.length} bits (${binary.bytes.length} bytes)`);
  const minimalTokens = minimal.articles.reduce((n, a) => n + a.blocks.reduce((m, b) => m + b.tokens.length, 0), 0);
  console.log(`decoy: ${decoy.articles.length} articles, ${decoyBinary.length} bits (${decoyBinary.bytes.length} bytes), ${replacements.size} ${replacements.size === 1 ? "lesson" : "lessons"} replaced, ${articles.length - decoyArticles.length} left out`);
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
