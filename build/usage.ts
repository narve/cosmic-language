// Where each symbol is introduced and used: computed from the message, for the vocabulary page, the lists of new
// symbols on the lessons, and links to blocks.
import { anchor, type Article } from "./lessons.ts";
import type { Message } from "./message.ts";

export interface Place {
  article: Article;
  block: number; // 1, 2, 3 … among the lesson's message blocks
}

export interface Usage {
  first: Map<string, Place>; // symbol name → where it first appears
  uses: Map<string, Place[]>; // symbol name → the first block of every lesson that uses it, in message order
  newIn: Map<string, string[]>; // lesson slug → the symbols it introduces, in order (the brackets ( and ) count)
  newTypes: Map<string, number[]>; // lesson slug → the token types that first appear in it, in order
}

const BRACKETS = 1; // symbols are the brackets ( and ) and types 2 and above; numbers and type names are not

export function blockId(article: Article, block: number): string {
  return `${anchor(article)}-block-${block}`;
}

export function computeUsage(message: Message, decoy?: Message): Usage {
  const usage = usageOf(message);
  if (!decoy) return usage;
  // A lesson that replaces another (the decoy) introduces what it introduces in the decoy version, and the decoy's own
  // symbols are introduced and used there.
  const inDecoy = usageOf(decoy);
  for (const { article } of decoy.articles) {
    if (!article.replaces) continue;
    usage.newIn.set(article.slug, inDecoy.newIn.get(article.slug) ?? []);
    usage.newTypes.set(article.slug, inDecoy.newTypes.get(article.slug) ?? []);
  }
  for (const [name, place] of inDecoy.first) {
    if (usage.first.has(name)) continue;
    usage.first.set(name, place);
    usage.uses.set(name, inDecoy.uses.get(name) ?? []);
  }
  return usage;
}

function usageOf(message: Message): Usage {
  const usage: Usage = { first: new Map(), uses: new Map(), newIn: new Map(), newTypes: new Map() };
  const types = new Set<number>();
  for (const { article, blocks } of message.articles) {
    blocks.forEach((block, index) => {
      const place = { article, block: index + 1 };
      for (const token of block.tokens) {
        if (!types.has(token.type)) {
          types.add(token.type);
          usage.newTypes.set(article.slug, [...(usage.newTypes.get(article.slug) ?? []), token.type]);
        }
        if (token.type < BRACKETS) continue;
        const name = token.text;
        if (!usage.first.has(name)) {
          usage.first.set(name, place);
          usage.newIn.set(article.slug, [...(usage.newIn.get(article.slug) ?? []), name]);
        }
        const uses = usage.uses.get(name) ?? [];
        if (!uses.some((use) => use.article === article)) uses.push(place);
        usage.uses.set(name, uses);
      }
    });
  }
  return usage;
}
