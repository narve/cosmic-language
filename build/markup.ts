// The markup of message blocks on the generated pages. The lesson sources write their code blocks as plain text
// (comments as "; …", variables and logic words as they are); the build adds the markup:
//   comments            <span data-comment>; …</span>
//   variables           <var>u</var>
//   logic words         <data value="not">not</data> (the symbols view shows their signs)
//   type names          <data value="4" data-type-name>variable</data> (sent as the number of the type)
// Comments get no markup inside: a variable in a comment is plain text.
import { escape } from "./dom.ts";
import { messageCode, readBlock, type Line, type Token } from "./message.ts";
import type { Registry } from "./registry.ts";
import { and, falseValue, implies, not, or, trueValue } from "../vocabulary/index.ts";

const LOGIC_WORDS = new Set<string>([trueValue, falseValue, not, and, or, implies].map((symbol) => symbol.name));
const VARIABLE = 4;

export function markupBlocks(article: Element, registry: Registry, where: string): void {
  messageCode(article).forEach((code, index) => {
    const block = readBlock(code, registry, `${where}, block ${index + 1}`);
    code.innerHTML = block.lines.map((line) => markLine(line, registry)).join("\n");
  });
}

function markLine(line: Line, registry: Registry): string {
  let html = "";
  let end = 0;
  for (const token of line.tokens) {
    html += escape(line.code.slice(end, token.start)) + markToken(token, registry);
    end = token.start + token.text.length;
  }
  html += escape(line.code.slice(end));
  if (line.comment !== undefined) html += `<span data-comment>${escape(line.comment)}</span>`;
  return html;
}

function markToken(token: Token, registry: Registry): string {
  const text = escape(token.text);
  if (token.type === VARIABLE) return `<var>${text}</var>`;
  const entry = registry.get(token.text);
  if (entry?.alias) return `<data value="${entry.alias.id}" data-type-name>${text}</data>`;
  if (LOGIC_WORDS.has(token.text)) return `<data value="${text}">${text}</data>`;
  return text;
}
