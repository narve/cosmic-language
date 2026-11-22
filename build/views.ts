// Views of message blocks: a row of checkboxes under the lesson's heading, and after each block's <pre> a
// <figure data-views> with a table of one row per line and one cell per view. The <pre> itself is left untouched.
// style.css shows the checked views, without JavaScript.
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
  const blocks = messageCode(article)
    .map((code, index) => ({ code, block: readBlock(code, registry, `${where}, block ${index + 1}`) }))
    .filter(({ block }) => block.bits === undefined); // a bits block already is its own bits view
  if (blocks.length === 0) return;
  addChoice(article, columns, where);
  blocks.forEach(({ code, block }) => {
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
    const figure = code.ownerDocument.createElement("figure");
    figure.setAttribute("data-views", "");
    figure.innerHTML =
      `\n<table>\n<thead><tr>${columns.map((view) => `<th scope="col" data-view="${view}">${view}</th>`).join("")}</tr></thead>\n` +
      `<tbody>\n${rows.join("\n")}\n</tbody>\n</table>\n`;
    const pre = code.parentElement!;
    pre.after(figure);
    pre.after(code.ownerDocument.createTextNode("\n"));
  });
}

// The row of checkboxes under the lesson's heading. style.css shows the checked views, without JavaScript.
function addChoice(article: Element, columns: View[], where: string): void {
  const fieldset = article.ownerDocument.createElement("fieldset");
  fieldset.setAttribute("data-view-choice", "");
  fieldset.innerHTML =
    "<legend>Show</legend>" +
    columns
      .map((view) => {
        // the input is a sibling of its label, so that CSS can tell when two boxes are checked (input:checked ~ input:checked)
        const id = `view-${where}-${view}`;
        return `<input type="checkbox" id="${id}" value="${view}"${view === "words" ? " checked" : ""}><label for="${id}">${view}</label>`;
      })
      .join("");
  article.querySelector("h1, h2, h3, h4, h5, h6")!.after(fieldset);
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
