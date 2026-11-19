// Views of message blocks: added as a <details data-views> table after each block's <pre>.
// The <pre> itself is left untouched.
import { escape } from "./dom.ts";
import { messageCode, readBlock, tokenBits, type Line, type Token } from "./message.ts";
import type { Registry } from "./registry.ts";
import { parseBlock } from "./check/structure.ts";
import { mathHtml } from "./lisp/display.ts";

export const VIEWS = ["words", "symbols", "math", "chunks", "bits"] as const;
export type View = (typeof VIEWS)[number];

// `views` lists the generated views; "words" is always included as the first column. `href`, if given, links the
// symbols in the symbols view to their entries on the vocabulary page.
export type Href = (name: string) => string | undefined;

export function addViews(article: Element, registry: Registry, views: View[], where: string, href?: Href): void {
  const columns: View[] = ["words", ...views.filter((view) => view !== "words")];
  if (columns.length === 1) return;
  messageCode(article).forEach((code, index) => {
    const block = readBlock(code, registry, `${where}, block ${index + 1}`);
    if (block.bits !== undefined) return; // a bits block already is its own bits view
    // the math view shows each sentence whole, on the line where it starts
    const starts = new Map<number, string[]>();
    for (const node of parseBlock(block.lines, "line")) {
      const line = Number(/line (\d+)$/.exec(node.where)![1]) - 1;
      starts.set(line, [...(starts.get(line) ?? []), mathHtml(node, registry)]);
    }
    const rows = block.lines
      .map((line, index) => ({ line, math: starts.get(index)?.join("  ") ?? "" }))
      .filter(({ line }) => line.comment !== undefined || line.tokens.length > 0)
      .map(({ line, math }) => {
        if (line.tokens.length === 0) {
          const comment = line.commentHtml ?? escape(line.comment!);
          return `<tr data-comment-row><td colspan="${columns.length}"><span data-comment>${comment}</span></td></tr>`;
        }
        return `<tr>${columns.map((view) => `<td data-view="${view}">${view === "math" ? math : cell(view, line, registry, href)}</td>`).join("")}</tr>`;
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

function cell(view: View, line: Line, registry: Registry, href?: Href): string {
  switch (view) {
    case "words":
    case "symbols": {
      // Keep the spacing of the line as written.
      let html = "";
      let end = 0;
      for (const token of line.tokens) {
        const shown = written(view, token, registry);
        const target = view === "symbols" && token.type !== 1 ? href?.(token.text) : undefined;
        html += escape(line.code.slice(end, token.start)) + (target ? `<a href="${escape(target)}">${shown}</a>` : shown);
        end = token.start + token.text.length;
      }
      return `<code>${html}</code>`;
    }
    case "math":
      return ""; // filled in per sentence, above
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
