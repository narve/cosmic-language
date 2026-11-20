// What the build adds to a lesson on a generated page (its own page, or an article on a version page):
// - an id on each message block, so the vocabulary can link to the block that introduces a symbol;
// - the markup of the blocks (markup.ts);
// - a list of the token types and symbols the lesson introduces, after its heading, linked to the vocabulary page;
// - links from <code> in the prose to the vocabulary, for a symbol's name (the first in each paragraph);
// - the generated views (views.ts), whose symbols view links every symbol.
// `base` is the way from the page to docs/: "../" for a lesson page, "" for a page in docs/ itself.
import { escape } from "./dom.ts";
import type { Article } from "./lessons.ts";
import { symbolFragment } from "./meaning.ts";
import { markupBlocks } from "./markup.ts";
import { messageCode } from "./message.ts";
import type { Registry } from "./registry.ts";
import { blockId, type Usage } from "./usage.ts";
import { addViews, type View } from "./views.ts";
import { TYPES } from "../vocabulary/index.ts";

export interface Enrich {
  registry: Registry;
  usage: Usage;
  base: string;
}

// The link to a name's entry on the vocabulary page, or undefined if the name is not a symbol or a type name.
export function vocabularyHref(name: string, { registry, base }: { registry: Registry; base: string }): string | undefined {
  const entry = registry.get(name);
  if (entry?.symbol) return `${base}vocabulary.html${symbolFragment(entry.symbol)}`;
  if (entry?.alias) return `${base}vocabulary.html#type-${entry.alias.name}`;
  return undefined;
}

export function enrichArticle(element: Element, article: Article, views: View[], context: Enrich): void {
  messageCode(element).forEach((code, index) => {
    code.parentElement!.id = blockId(article, index + 1);
  });
  markupBlocks(element, context.registry, article.slug);
  linkProse(element, context);
  listNewSymbols(element, article, context);
  addViews(element, context.registry, views, article.slug, (name) => vocabularyHref(name, context));
}

function listNewSymbols(element: Element, article: Article, context: Enrich): void {
  const types = (context.usage.newTypes.get(article.slug) ?? []).map((id) => TYPES.find((type) => type.id === id)!);
  const names = context.usage.newIn.get(article.slug) ?? [];
  if (types.length === 0 && names.length === 0) return;
  const typeHref = (name: string) => `${context.base}vocabulary.html#type-${name}`;
  const typeItems = types.map((type) => `<li><a href="${escape(typeHref(type.name))}">${escape(type.name)}</a></li>`);
  const symbolItems = names.map((name) => {
    const entry = context.registry.get(name);
    const typeName = entry?.symbol ? entry.symbol.type.name : "brackets"; // ( and ) are the values of type 1
    const href = vocabularyHref(name, context) ?? typeHref(typeName);
    return `<li><a href="${escape(href)}"><code>${escape(name)}</code></a> <small>${escape(typeName)}</small></li>`;
  });
  const row = (label: string, items: string[]) => (items.length ? `<dt>${label}</dt><dd><ul>${items.join("")}</ul></dd>` : "");
  const aside = element.ownerDocument.createElement("aside");
  aside.setAttribute("data-new-symbols", "");
  aside.innerHTML = `<p>New in this lesson</p><dl>${row(typeItems.length === 1 ? "Type" : "Types", typeItems)}${row(symbolItems.length === 1 ? "Symbol" : "Symbols", symbolItems)}</dl>`;
  const heading = element.querySelector("h1, h2, h3, h4, h5, h6");
  if (heading) heading.after(aside);
  else element.prepend(aside);
}

function linkProse(element: Element, context: Enrich): void {
  for (const block of element.querySelectorAll("p, li, dd, td")) {
    if (block.closest("pre, aside, details")) continue;
    const seen = new Set<string>();
    for (const code of block.querySelectorAll("code")) {
      if (code.closest("a") || code.children.length > 0) continue;
      const name = code.textContent ?? "";
      const href = vocabularyHref(name, context);
      if (!href || seen.has(name)) continue;
      seen.add(name);
      const link = element.ownerDocument.createElement("a");
      link.setAttribute("href", href);
      code.replaceWith(link);
      link.append(code);
    }
  }
}
