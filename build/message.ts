// The message: reading code blocks into tokens or bits, and the output files.
import { BuildError } from "./dom.ts";
import type { Registry } from "./registry.ts";
import { groupRuns, type Article, type Topic } from "./lessons.ts";

export const CHUNK_BITS = 8;

export interface Token {
  text: string; // as written: a number, a bracket or a symbol name
  start: number; // position in its line
  type: number;
  value: number;
}

export interface Line {
  text: string; // a code line as written, or the text of a comment
  comment?: Element; // the <span data-comment>, for comment lines
  tokens: Token[];
}

export interface Block {
  lines: Line[];
  tokens: Token[];
  bits?: string; // for a bits block (<pre data-bits>, e.g. the beacon): its 0s and 1s, sent as they are
}

// The code elements of an article's message blocks (illustrations are not sent).
export function messageCode(article: Element): Element[] {
  return Array.from(article.querySelectorAll("pre:not([data-illustration]) > code"));
}

export function readBlock(code: Element, registry: Registry, where: string): Block {
  // Comments are on their own lines: swap each for a marker line, then split into lines.
  const copy = code.cloneNode(true) as Element;
  const comments = Array.from(code.querySelectorAll("[data-comment]"));
  for (const span of copy.querySelectorAll("[data-comment]")) span.replaceWith(copy.ownerDocument.createTextNode("\u0000"));
  let comment = 0;
  const lines: Line[] = [];
  const tokens: Token[] = [];
  let depth = 0;
  const raw = code.parentElement!.hasAttribute("data-bits");
  let bits = "";
  copy.textContent!.split("\n").forEach((text, index) => {
    const at = `${where}, line ${index + 1}`;
    if (text.includes("\u0000")) {
      const span = comments[comment++];
      lines.push({ text: span.textContent!, comment: span, tokens: [] });
      return;
    }
    const line: Line = { text, tokens: [] };
    if (raw) {
      if (/[^01\s]/.test(text)) throw new BuildError(`${at}: a bits block may only contain 0, 1 and spaces`);
      bits += text.replace(/\s/g, "");
      lines.push(line);
      return;
    }
    for (const match of text.matchAll(/[()]|[^\s()]+/g)) {
      const token = classify(match[0], match.index!, registry, at);
      if (token.type === 1) depth += token.value === 0 ? 1 : -1;
      if (depth < 0) throw new BuildError(`${at}: ")" without a matching "("`);
      line.tokens.push(token);
      tokens.push(token);
    }
    lines.push(line);
  });
  if (depth > 0) throw new BuildError(`${where}: ${depth} unclosed "(" at the end of the block`);
  return raw ? { lines, tokens, bits } : { lines, tokens };
}

function classify(text: string, start: number, registry: Registry, at: string): Token {
  if (text === "(" || text === ")") return { text, start, type: 1, value: text === "(" ? 0 : 1 };
  if (/^\d+$/.test(text)) {
    const value = Number(text);
    if (value >= 2 ** CHUNK_BITS) throw new BuildError(`${at}: ${text} does not fit in a chunk; write it with big`);
    return { text, start, type: 0, value };
  }
  const symbol = registry.get(text);
  if (!symbol) throw new BuildError(`${at}: unknown symbol "${text}"`);
  return { text, start, type: symbol.type, value: symbol.id };
}

export function chunkBits(value: number): string {
  return value.toString(2).padStart(CHUNK_BITS, "0");
}

export function tokenBits(token: Token): string {
  return chunkBits(token.type) + " " + chunkBits(token.value);
}

export interface Message {
  articles: { article: Article; blocks: Block[] }[];
  topics: Topic[];
}

// The message in reading order: a heading for each run of a topic and each lesson that has message blocks, then the blocks.
type Entry = { heading: string } | { block: Block };

function outline(message: Message): Entry[] {
  const blocks = new Map(message.articles.map(({ article, blocks }) => [article, blocks]));
  const entries: Entry[] = [];
  const groups = groupRuns(message.articles.map(({ article }) => article), message.topics);
  for (const group of groups) {
    const lessons = group.articles.filter((article) => blocks.get(article)!.length > 0);
    if (lessons.length === 0) continue;
    entries.push({ heading: `; ==== ${group.topic.title} ====` });
    for (const article of lessons) {
      entries.push({ heading: `; ---- Lesson ${article.number}: ${article.title} ----` });
      for (const block of blocks.get(article)!) entries.push({ block });
    }
  }
  return entries;
}

// Writes the outline: a blank line before each heading and between blocks.
function write(message: Message, header: string[], block: (block: Block) => string[]): string {
  const out = [...header];
  let previous: Entry | undefined;
  for (const entry of outline(message)) {
    if ("heading" in entry) out.push("", entry.heading);
    else {
      if (previous && "block" in previous) out.push("");
      out.push(...block(entry.block));
    }
    previous = entry;
  }
  out.push("");
  return out.join("\n");
}

export function messageText(message: Message): string {
  const header = [
    "; The cosmic-language message as text. Generated by `npm run build`; do not edit.",
    "; Numbers, brackets and symbol names are tokens; lines of 0s and 1s (the beacon and the terminator) are bits, sent as they are.",
    "; Everything from ; to the end of a line is a comment and is not sent.",
  ];
  return write(message, header, (block) => block.lines.map((line) => (line.comment ? `; ${line.text}` : line.text)));
}

export function messageBits(message: Message): string {
  const header = [
    "; The cosmic-language message as bits: each token is a type chunk and a value chunk. Generated by `npm run build`.",
    "; Only the 0s and 1s outside comments are sent; spaces, line breaks and comments (from ; to the end of a line) are for reading.",
  ];
  return write(message, header, (block) =>
    block.lines.flatMap((line) => {
      if (line.comment) return [`; ${line.text}`];
      if (block.bits !== undefined) return line.text.trim() ? [line.text.trim()] : [];
      return line.tokens.map((token) => `${tokenBits(token)}   ; ${token.text}`);
    }),
  );
}

// The stream exactly as sent: every message block in order, bits blocks as they are, tokens as two chunks each.
export function messageStream(message: Message): string {
  const blocks = message.articles.flatMap(({ blocks }) => blocks);
  return blocks
    .map((block) => block.bits ?? block.tokens.map((token) => chunkBits(token.type) + chunkBits(token.value)).join(""))
    .join("");
}

// The bit stream packed into bytes, most significant bit first; the last byte is padded with 0s.
export function messageBinary(stream: string): { bytes: Uint8Array; length: number } {
  const bytes = new Uint8Array(Math.ceil(stream.length / 8));
  for (let i = 0; i < stream.length; i++) if (stream[i] === "1") bytes[i >> 3] |= 0x80 >> (i & 7);
  return { bytes, length: stream.length };
}

// message.bin as text, like `xxd -b`: the byte offset, then 8 bytes per line in binary.
export function binaryDump({ bytes, length }: { bytes: Uint8Array; length: number }): string {
  const padding = bytes.length * 8 - length;
  const out = [
    "; message.bin as binary numbers, 8 bytes per line after the byte offset. Generated by `npm run build`.",
    `; ${length} bits in ${bytes.length} bytes` + (padding ? `; the last ${padding} bits are padding, not part of the message.` : "."),
  ];
  const width = String(bytes.length).length;
  for (let offset = 0; offset < bytes.length; offset += 8) {
    const line = Array.from(bytes.subarray(offset, offset + 8), (byte) => chunkBits(byte)).join(" ");
    out.push(`${String(offset).padStart(width, "0")}: ${line}`);
  }
  return out.join("\n") + "\n";
}
