// The structure rules of the specification (§10.1), checked on the parsed message. All are hard errors:
// - the hole ? of a question appears only inside quote;
// - an unquoted group starts with an operator and has the number of arguments its arity allows;
// - ∀, ∃ and sequence bind a variable, and every variable is bound (sentences are closed);
// - every symbol in the registry is used (checkStructure, on the full version);
// - in every version, the ids of each type first appear in the order 1, 2, 3 … with none missing (checkIdOrder);
// - a symbol is in at least EXAMPLES sentences of the lesson that introduces it;
// - a type name (an alias for the number of a type) stands only where a type is meant: as an argument of a
//   comparison that also has a (type …) argument, as in (= (type (quote u)) variable).
import { BuildError } from "../dom.ts";
import type { Message, Token } from "../message.ts";
import type { Registry } from "../registry.ts";

export const EXAMPLES = 3; // k in the specification

const OPERATOR = 2;
const VARIABLE = 4;
const ELEMENT = 6; // an element's id is its atomic number, not its order of appearance
const BINDERS = new Set(["∀", "∃", "sequence", "average", "let"]); // (binder variable values body): the variable is bound in the body
const COMPARISONS = new Set(["=", "≠", "<", ">", "≤", "≥"]);

// A token, or a bracket group with the tokens and groups inside it.
export interface Node {
  token?: Token;
  items?: Node[];
  where: string; // lesson, block and line
}

// The top-level items of a block: sentences (groups) and bare tokens. The build has already checked the brackets.
export function parseBlock(lines: { tokens: Token[] }[], where: string): Node[] {
  const top: Node[] = [];
  const open: Node[] = [];
  lines.forEach((line, index) => {
    const at = `${where}, line ${index + 1}`;
    for (const token of line.tokens) {
      const parent = open.length > 0 ? open[open.length - 1].items! : top;
      if (token.text === "(") {
        const group: Node = { items: [], where: at };
        parent.push(group);
        open.push(group);
      } else if (token.text === ")") open.pop();
      else parent.push({ token, where: at });
    }
  });
  return top;
}

export function show(node: Node): string {
  return node.token ? node.token.text : `(${node.items!.map(show).join(" ")})`;
}

function allowed(arity: string, count: number): boolean {
  const least = parseInt(arity, 10);
  return arity.endsWith("+") ? count >= least : count === least;
}

function checkNode(node: Node, registry: Registry, bound: Set<string>, typeSlot = false): void {
  if (node.token) {
    if (registry.get(node.token.text)?.alias && !typeSlot) {
      throw new BuildError(`${node.where}: the type name ${node.token.text} may only be compared with a (type …), as in (= (type (quote u)) variable)`);
    }
    // a quoted expression is not checked (below), so a hole reached here is outside every quote
    if (node.token.text === "?") throw new BuildError(`${node.where}: a question (a sentence with ?) can only be mentioned, inside quote`);
    if (node.token.type === VARIABLE && !bound.has(node.token.text)) {
      throw new BuildError(`${node.where}: the variable ${node.token.text} is not bound by ∀, ∃, sequence, average or let`);
    }
    return;
  }
  const [head, ...args] = node.items!;
  const operator = head?.token?.type === OPERATOR ? registry.get(head.token.text) : undefined;
  if (!operator) throw new BuildError(`${node.where}: ${show(node)} does not start with an operator`);
  if (operator.arity && !allowed(operator.arity, args.length)) {
    throw new BuildError(`${node.where}: ${operator.name} takes ${operator.arity} arguments, not ${args.length}, in ${show(node)}`);
  }
  if (operator.name === "quote") return; // a quoted expression is mentioned, not used: anything goes inside
  if (BINDERS.has(operator.name)) {
    const [variable, values, body] = args;
    if (variable.token?.type !== VARIABLE) {
      throw new BuildError(`${node.where}: ${operator.name} needs a variable as its first argument, in ${show(node)}`);
    }
    checkNode(values, registry, bound);
    checkNode(body, registry, new Set(bound).add(variable.token.text));
    return;
  }
  const typed = COMPARISONS.has(operator.name) && args.some((arg) => arg.items?.[0]?.token?.text === "type");
  for (const arg of args) checkNode(arg, registry, bound, typed);
}

function symbols(node: Node, into: Set<string> = new Set()): Set<string> {
  if (node.token) {
    if (node.token.type >= OPERATOR) into.add(node.token.text);
  } else for (const item of node.items!) symbols(item, into);
  return into;
}

interface First {
  name: string;
  lesson: string; // the lesson that introduces the symbol
  sentences: number; // sentences of that lesson that use it
}

// What the message says about itself must hold for the version it is in: every (= (count (quote S) message) n) and
// (= (item message k) x) is checked against the message's own items (its numbers and sentences, in order).
export function checkSelfReference(message: Message, version: string): number {
  const items: Node[] = [];
  for (const { article, blocks } of message.articles) {
    blocks.forEach((block, index) => {
      if (block.bits === undefined) items.push(...parseBlock(block.lines, `${article.slug}, block ${index + 1}`));
    });
  }
  const shown = items.map(show);
  const word = (n: Node | undefined) => n?.token?.text;
  let checked = 0;
  for (const node of items) {
    const [eq, left, right] = node.items ?? [];
    if (word(eq) !== "=" || !left?.items || !right) continue;
    const [op, a, b] = left.items;
    if (word(op) === "count" && word(b) === "message" && a?.items && word(a.items[0]) === "quote") {
      const expected = Number(word(right));
      const actual = shown.filter((s) => s === show(a.items[1])).length;
      if (actual !== expected) throw new BuildError(`${node.where}: in the ${version} version, ${show(a.items[1])} is in the message ${actual} times, not ${expected}`);
      checked++;
    } else if (word(op) === "item" && word(a) === "message") {
      const k = Number(word(b));
      if (shown[k - 1] !== show(right)) throw new BuildError(`${node.where}: in the ${version} version, item ${k} of the message is ${shown[k - 1]}, not ${show(right)}`);
      checked++;
    }
  }
  return checked;
}

// An optional lesson may be left out of a message: no lesson that is not optional may use a symbol that it introduces.
// Optional lessons may build on each other: they are all in the full version and all left out of the others.
export function checkOptional(message: Message, isOptional: (slug: string) => boolean): void {
  const introducedIn = new Map<string, string>();
  for (const { article, blocks } of message.articles) {
    for (const block of blocks) for (const token of block.tokens) {
      if (token.type < OPERATOR) continue;
      if (!introducedIn.has(token.text)) introducedIn.set(token.text, article.slug);
      const home = introducedIn.get(token.text)!;
      if (home !== article.slug && isOptional(home) && !isOptional(article.slug)) {
        throw new BuildError(`${article.slug} uses "${token.text}", which the optional lesson ${home} introduces; an optional lesson must be possible to leave out`);
      }
    }
  }
}

// The minimal version is a message of its own: a minimal lesson may only use symbols that a minimal lesson introduces.
export function checkMinimal(message: Message, isMinimal: (slug: string) => boolean): void {
  const introducedIn = new Map<string, string>();
  for (const { article, blocks } of message.articles) {
    for (const block of blocks) for (const token of block.tokens) {
      if (token.type < OPERATOR) continue;
      if (!introducedIn.has(token.text)) introducedIn.set(token.text, article.slug);
      const home = introducedIn.get(token.text)!;
      if (isMinimal(article.slug) && !isMinimal(home)) {
        throw new BuildError(`${article.slug} is in the minimal version but uses "${token.text}", which ${home} introduces and which is not`);
      }
    }
  }
}

// In a version of the message, the ids of each type (but elements, whose id is the atomic number) must first appear
// in the order 1, 2, 3 …, with none missing: the lessons that make up the smaller versions come first. Ids are
// fixed in the vocabulary, so a new symbol out of order is an error, not a reason to renumber silently.
export function checkIdOrder(message: Message, registry: Registry, version: string): void {
  const next = new Map<number, number>();
  const seen = new Set<string>();
  for (const { article, blocks } of message.articles) {
    for (const block of blocks) for (const token of block.tokens) {
      if (token.type < OPERATOR || token.type === ELEMENT || seen.has(token.text)) continue;
      seen.add(token.text);
      const expected = next.get(token.type) ?? 1;
      if (token.value !== expected) {
        const { symbol } = registry.get(token.text)!;
        throw new BuildError(`${article.slug}: in the ${version} version, "${token.text}" is the next new ${symbol?.type.name ?? `type ${token.type}`} symbol, so its id should be ${expected}, not ${token.value}: ids appear in the order 1, 2, 3 … in every version (move lessons, or change the vocabulary deliberately)`);
      }
      next.set(token.type, expected + 1);
    }
  }
}

// Throws on a broken rule.
export function checkStructure(message: Message, registry: Registry): void {
  const first = new Map<string, First>(); // in order of first appearance
  for (const { article, blocks } of message.articles) {
    blocks.forEach((block, index) => {
      if (block.bits !== undefined) return;
      for (const node of parseBlock(block.lines, `${article.slug}, block ${index + 1}`)) {
        checkNode(node, registry, new Set());
        for (const name of symbols(node)) {
          const seen = first.get(name);
          if (!seen) first.set(name, { name, lesson: article.slug, sentences: 1 });
          else if (seen.lesson === article.slug) seen.sentences++;
        }
      }
    });
  }
  for (const [name, entry] of registry) {
    if (entry.alias) continue; // a type name is a number, not a symbol
    if (!first.has(name)) throw new BuildError(`the symbol "${name}" is in the registry but not in the message`);
  }
  const short = [...first.values()].filter((symbol) => symbol.sentences < EXAMPLES);
  if (short.length > 0) {
    const list = short.map(({ name, lesson, sentences }) => `\n  ${name}: ${sentences} in ${lesson}`).join("");
    throw new BuildError(`a new symbol must be in at least ${EXAMPLES} sentences of the lesson that introduces it:${list}`);
  }
}
