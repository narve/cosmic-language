// Views of message blocks: added as a <details data-views> table after each block's <pre>.
// The <pre> itself is left untouched.
import { escape } from "./dom.ts";
import { messageCode, readBlock, tokenBits, type Line, type Token } from "./message.ts";
import type { Registry } from "./registry.ts";

export const VIEWS = ["words", "symbols", "chunks", "bits"] as const;
export type View = (typeof VIEWS)[number];

// `views` lists the generated views; "words" is always included as the first column.
export function addViews(article: Element, registry: Registry, views: View[], where: string): void {
  const columns: View[] = ["words", ...views.filter((view) => view !== "words")];
  if (columns.length === 1) return;
  messageCode(article).forEach((code, index) => {
    const block = readBlock(code, registry, `${where}, block ${index + 1}`);
    if (block.bits !== undefined) return; // a bits block already is its own bits view
    const rows = block.lines
      .filter((line) => line.comment !== undefined || line.tokens.length > 0)
      .map((line) => {
        if (line.tokens.length === 0) {
          const comment = line.commentHtml ?? escape(line.comment!);
          return `<tr data-comment-row><td colspan="${columns.length}"><span data-comment>${comment}</span></td></tr>`;
        }
        return `<tr>${columns.map((view) => `<td data-view="${view}">${cell(view, line, registry)}</td>`).join("")}</tr>`;
      });
    const details = code.ownerDocument.createElement("details");
    details.setAttribute("data-views", "");
    details.innerHTML =
      `\n<summary>${columns.slice(1).join(", ").replace(/, ([^,]*)$/, " and $1")}</summary>\n<table>\n` +
      `<thead><tr>${columns.map((view) => `<th data-view="${view}">${view}</th>`).join("")}</tr></thead>\n` +
      `<tbody>\n${rows.join("\n")}\n</tbody>\n</table>\n`;
    const pre = code.parentElement!;
    pre.after(details);
    pre.after(code.ownerDocument.createTextNode("\n"));
  });
}

function cell(view: View, line: Line, registry: Registry): string {
  switch (view) {
    case "words":
    case "symbols": {
      // Keep the spacing of the line as written.
      let html = "";
      let end = 0;
      for (const token of line.tokens) {
        html += escape(line.code.slice(end, token.start)) + written(view, token, registry);
        end = token.start + token.text.length;
      }
      return `<code>${html}</code>`;
    }
    case "chunks":
      return `<samp>${line.tokens.map((token) => `${token.type}:${token.value}`).join(" ")}</samp>`;
    case "bits":
      // A non-breaking space inside a token and two spaces between tokens, so lines wrap only between tokens.
      return `<samp>${line.tokens.map((token) => tokenBits(token).replace(" ", "\u00a0")).join("  ")}</samp>`;
  }
}

function written(view: View, token: Token, registry: Registry): string {
  if (token.type <= 1) {
    const alias = registry.get(token.text)?.alias;
    if (alias) return `<data value="${alias.id}" data-type-name>${escape(token.text)}</data>`; // a type name, sent as its number
    return escape(token.text);
  }
  if (token.type === 4) return `<var>${escape(token.text)}</var>`;
  const sign = registry.get(token.text)!.sign;
  if (view === "symbols" && sign) return `<data value="${escape(token.text)}">${escape(sign)}</data>`;
  return escape(token.text);
}
