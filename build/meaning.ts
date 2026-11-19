// A vocabulary meaning as HTML: `code` becomes <code>, {u} a variable, and a referenced symbol a link to it.
import { escape } from "./dom.ts";
import type { Meaning, SymbolDef } from "../vocabulary/index.ts";

// The anchor of a symbol in the tables (specification, vocabulary page): its type name and its name, e.g.
// "operator-exp", "constant-π". In a link it is percent-encoded (symbolFragment).
export function symbolAnchor(symbol: SymbolDef): string {
  return `${symbol.type.name}-${symbol.name}`;
}

export function symbolFragment(symbol: SymbolDef): string {
  return `#${encodeURIComponent(symbolAnchor(symbol))}`;
}

export function meaningHtml(meaning: Meaning | undefined, href: (symbol: SymbolDef) => string): string {
  if (meaning === undefined) return "";
  const parts = typeof meaning === "string" ? [meaning] : meaning.parts;
  return parts
    .map((part) => (typeof part === "string" ? text(part) : `<a href="${escape(href(part))}"><code>${escape(part.name)}</code></a>`))
    .join("");
}

function text(plain: string): string {
  return escape(plain)
    .replace(/`([^`]*)`/g, "<code>$1</code>")
    .replace(/\{([^{}\s]+)\}/g, "<var>$1</var>");
}
