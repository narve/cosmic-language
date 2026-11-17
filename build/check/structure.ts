// The structure rules of the specification (§10), checked on the parsed message. All but the last are hard errors:
// - an unquoted group starts with an operator and has the number of arguments its arity allows;
// - ∀, ∃ and sequence bind a variable, and every variable is bound (sentences are closed);
// - every symbol in the registry is used, and ids follow the order of first appearance in each type;
// - (reported, not an error) a symbol is in at least EXAMPLES sentences of the lesson that introduces it.
import { BuildError } from "../dom.ts";
import type { Message, Token } from "../message.ts";
import type { Registry } from "../registry.ts";

export const EXAMPLES = 3; // k in the specification

const OPERATOR = 2;
const VARIABLE = 4;
const ELEMENT = 6; // an element's id is its atomic number, not its order of appearance
const BINDERS = new Set(["∀", "∃", "sequence"]); // (binder variable values body): the variable is bound in the body

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

function checkNode(node: Node, registry: Registry, bound: Set<string>): void {
  if (node.token) {
    if (node.token.type === VARIABLE && !bound.has(node.token.text)) {
      throw new BuildError(`${node.where}: the variable ${node.token.text} is not bound by ∀, ∃ or sequence`);
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
  for (const arg of args) checkNode(arg, registry, bound);
}

function symbols(node: Node, into: Set<string> = new Set()): Set<string> {
  if (node.token) {
    if (node.token.type >= OPERATOR) into.add(node.token.text);
  } else for (const item of node.items!) symbols(item, into);
  return into;
}

export interface Short {
  name: string;
  lesson: string;
  sentences: number;
}

// Throws on a broken rule. Returns the symbols with fewer than EXAMPLES sentences in their first lesson.
export function checkStructure(message: Message, registry: Registry): Short[] {
  const first = new Map<string, Short>(); // in order of first appearance
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
  for (const name of registry.keys()) {
    if (!first.has(name)) throw new BuildError(`the symbol "${name}" is in the registry but not in the message`);
  }
  const next = new Map<number, number>();
  for (const { name, lesson } of first.values()) {
    const { type, id } = registry.get(name)!;
    if (type === ELEMENT) continue;
    const expected = next.get(type) ?? 1;
    if (id !== expected) {
      throw new BuildError(`${lesson}: "${name}" is the next new symbol of type ${type}, so its id must be ${expected}, not ${id} (ids follow the order of first appearance)`);
    }
    next.set(type, expected + 1);
  }
  return [...first.values()].filter((symbol) => symbol.sentences < EXAMPLES);
}
