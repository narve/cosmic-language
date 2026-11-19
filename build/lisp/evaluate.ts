// A small interpreter for the message's expressions: the checker's own reading of each symbol, written apart from
// the lessons' wording, so the two must agree.
//
// Values: exact rational numbers (BigInt fractions), truth values, lists, and symbols as data (inside quote).
// What it cannot compute (real numbers, infinite domains, physics, the game, the message itself …) raises Unknown
// with a reason; such a sentence is neither true nor false to the interpreter. A division by zero raises
// Undefined: the specification forbids it, except in the branch of an if that is not picked (§8.2).
import type { Node } from "../check/structure.ts";
import type { Token } from "../message.ts";
import type { Registry } from "../registry.ts";

export class Unknown extends Error {}
export class Undefined extends Error {}

export interface Rational { n: bigint; d: bigint } // d > 0, in lowest terms
export interface Sym { sym: string } // a symbol as data, e.g. inside quote
export interface Fn { fn: string } // an operator used as a value, e.g. the + of (apply + …)
export type Value = Rational | boolean | Value[] | Sym | Fn;

const VARIABLE = 4;

// The prisoner's dilemma, read independently of the lesson: the moves, the cost of a round to the first player,
// and each strategy's rule for its next move, given its own history (rounds of [own move, other's move]).
const C: Sym = { sym: "cooperate" }, D: Sym = { sym: "defect" };
const STRATEGIES = ["always-cooperate", "always-defect", "tit-for-tat", "suspicious-tit-for-tat", "grim", "pavlov", "generous-tit-for-tat", "random"];
const LOSS: Record<string, number> = { "cooperate cooperate": 3, "defect defect": 5, "cooperate defect": 7, "defect cooperate": 2 };
function strategyMove(strategy: string, history: Sym[][]): Sym[] {
  const last = history[history.length - 1];
  const theirs = history.map((round) => round[1].sym);
  switch (strategy) {
    case "always-cooperate": return [C];
    case "always-defect": return [D];
    case "tit-for-tat": return last ? [last[1]] : [C];
    case "suspicious-tit-for-tat": return last ? [last[1]] : [D];
    case "grim": return theirs.includes("defect") ? [D] : [C];
    case "pavlov": return !last || last[0].sym === last[1].sym ? [C] : [D];
    case "generous-tit-for-tat": return !last || last[1].sym === "cooperate" ? [C] : [C, D, D];
    case "random": return [C, D];
  }
  throw new Unknown(`the strategy ${strategy}`);
}

const gcd = (a: bigint, b: bigint): bigint => (b === 0n ? (a < 0n ? -a : a) : gcd(b, a % b));
export function rational(n: bigint, d: bigint = 1n): Rational {
  if (d === 0n) throw new Undefined("division by zero");
  if (d < 0n) [n, d] = [-n, -d];
  const g = gcd(n, d) || 1n;
  return { n: n / g, d: d / g };
}
const isRational = (v: Value): v is Rational => typeof v === "object" && v !== null && "n" in v;
const isSym = (v: Value): v is Sym => typeof v === "object" && v !== null && "sym" in v;
const isFn = (v: Value): v is Fn => typeof v === "object" && v !== null && "fn" in v;

export function equal(a: Value, b: Value): boolean {
  if (Array.isArray(a) || Array.isArray(b)) return Array.isArray(a) && Array.isArray(b) && a.length === b.length && a.every((x, i) => equal(x, b[i]));
  if (isRational(a) || isRational(b)) return isRational(a) && isRational(b) && a.n === b.n && a.d === b.d;
  if (isSym(a) || isSym(b)) return isSym(a) && isSym(b) && a.sym === b.sym;
  if (isFn(a) || isFn(b)) return isFn(a) && isFn(b) && a.fn === b.fn;
  return a === b;
}

export function show(v: Value): string {
  if (Array.isArray(v)) return `(${v.map(show).join(" ")})`;
  if (isRational(v)) return v.d === 1n ? String(v.n) : `${v.n}/${v.d}`;
  if (isSym(v)) return v.sym;
  if (isFn(v)) return v.fn;
  return String(v);
}

type Env = Map<string, Value>;

export class Interpreter {
  constructor(private registry: Registry) {}

  // A sentence: true, false, or Unknown / Undefined thrown.
  truth(node: Node): boolean {
    const value = this.evaluate(node, new Map());
    if (typeof value !== "boolean") throw new Unknown(`a sentence with the value ${show(value)}, not true or false`);
    return value;
  }

  evaluate(node: Node, env: Env): Value {
    if (node.token) return this.atom(node.token, env);
    const [head, ...args] = node.items!;
    const name = head.token?.text;
    if (!name) throw new Unknown("a group without an operator");
    const special = this.special(name, args, env);
    if (special !== undefined) return special;
    return this.call(name, args.map((arg) => this.evaluate(arg, env)));
  }

  private atom(token: Token, env: Env): Value {
    if (token.type === 0) return rational(BigInt(token.value)); // a number, or a type name sent as its number
    if (token.type === VARIABLE) {
      const value = env.get(token.text);
      if (value === undefined) throw new Unknown(`the unbound variable ${token.text}`);
      return value;
    }
    if (token.text === "true") return true;
    if (token.text === "false") return false;
    if (token.type === 2) return { fn: token.text };
    if (token.text === "cooperate" || token.text === "defect" || STRATEGIES.includes(token.text)) return { sym: token.text };
    if (token.text === "moves") return [C, D];
    if (token.text === "tournament") return STRATEGIES.slice(0, 6).map((sym) => ({ sym }));
    throw new Unknown(`the constant ${token.text}`);
  }

  // The forms that do not evaluate all their arguments first. Returns undefined for an ordinary operator.
  private special(name: string, args: Node[], env: Env): Value | undefined {
    const bind = (variable: Node, value: Value) => new Map(env).set(variable.token!.text, value);
    switch (name) {
      case "quote":
        return this.data(args[0]);
      case "if": {
        const condition = this.evaluate(args[0], env);
        if (typeof condition !== "boolean") throw new Unknown("if with a condition that is not true or false");
        return this.evaluate(condition ? args[1] : args[2], env);
      }
      case "let":
        return this.evaluate(args[2], bind(args[0], this.evaluate(args[1], env)));
      case "∀":
      case "∃":
      case "sequence": {
        const domain = this.evaluate(args[1], env);
        if (!Array.isArray(domain)) throw new Unknown(`${name} over ${show(domain)}`);
        const values = domain.map((item) => this.evaluate(args[2], bind(args[0], item)));
        if (name === "sequence") return values;
        const truths = values.map((value) => {
          if (typeof value !== "boolean") throw new Unknown(`${name} of a value that is not true or false`);
          return value;
        });
        return name === "∀" ? truths.every(Boolean) : truths.some(Boolean);
      }
    }
    return undefined;
  }

  // An expression as data: numbers stay numbers, symbols become symbols, groups become lists.
  data(node: Node): Value {
    if (node.items) return node.items.map((item) => this.data(item));
    const token = node.token!;
    if (token.type === 0) return rational(BigInt(token.value));
    return { sym: token.text };
  }

  // Data back to an expression, for eval.
  private node(value: Value): Node {
    if (Array.isArray(value)) return { items: value.map((item) => this.node(item)), where: "eval" };
    if (isRational(value)) {
      if (value.d !== 1n || value.n < 0n || value.n > 255n) throw new Unknown(`eval of the number ${show(value)}`);
      return { token: { text: String(value.n), start: 0, type: 0, value: Number(value.n) }, where: "eval" };
    }
    if (isSym(value) || isFn(value)) {
      const text = isSym(value) ? value.sym : value.fn;
      const entry = this.registry.get(text);
      if (!entry) throw new Unknown(`eval of the unknown symbol ${text}`);
      return { token: { text, start: 0, type: entry.type, value: entry.id }, where: "eval" };
    }
    throw new Unknown(`eval of ${show(value)}`);
  }

  private call(name: string, a: Value[]): Value {
    const q = (v: Value): Rational => {
      if (!isRational(v)) throw new Unknown(`${name} of ${show(v)}, not a rational number`);
      return v;
    };
    const b = (v: Value): boolean => {
      if (typeof v !== "boolean") throw new Unknown(`${name} of ${show(v)}, not true or false`);
      return v;
    };
    const l = (v: Value): Value[] => {
      if (!Array.isArray(v)) throw new Unknown(`${name} of ${show(v)}, not a list`);
      return v;
    };
    const cmp = (x: Rational, y: Rational) => x.n * y.d - y.n * x.d;
    const chain = (ok: (c: bigint) => boolean) => a.map(q).every((x, i, all) => i === 0 || ok(cmp(all[i - 1], x)));
    const add = (x: Rational, y: Rational) => rational(x.n * y.d + y.n * x.d, x.d * y.d);
    const mul = (x: Rational, y: Rational) => rational(x.n * y.n, x.d * y.d);
    switch (name) {
      case "=": return a.every((x) => equal(x, a[0]));
      case "≠": return !equal(a[0], a[1]);
      case "<": return chain((c) => c < 0n);
      case ">": return chain((c) => c > 0n);
      case "≤": return chain((c) => c <= 0n);
      case "≥": return chain((c) => c >= 0n);
      case "+": return a.map(q).reduce(add);
      case "×": return a.map(q).reduce(mul);
      case "−": return add(q(a[0]), rational(-q(a[1]).n, q(a[1]).d));
      case "neg": return rational(-q(a[0]).n, q(a[0]).d);
      case "÷": {
        const [x, y] = [q(a[0]), q(a[1])];
        if (y.n === 0n) throw new Undefined(`division of ${show(x)} by zero`);
        return rational(x.n * y.d, x.d * y.n);
      }
      case "big": return rational(a.map(q).reduce((s, digit) => s * 256n + digit.n, 0n));
      case "^": {
        const [x, e] = [q(a[0]), q(a[1])];
        if (e.d !== 1n || e.n < 0n) throw new Unknown(`^ with the exponent ${show(e)}`);
        if (x.n === 0n && e.n === 0n) return rational(1n);
        return rational(x.n ** e.n, x.d ** e.n);
      }
      case "abs": return rational(q(a[0]).n < 0n ? -q(a[0]).n : q(a[0]).n, q(a[0]).d);
      case "not": return !b(a[0]);
      case "and": return a.map(b).every(Boolean);
      case "or": return a.map(b).some(Boolean);
      case "implies": return !b(a[0]) || b(a[1]);
      case "list": return a;
      case "length": return rational(BigInt(l(a[0]).length));
      case "item": {
        const list = l(a[0]);
        const k = q(a[1]);
        if (k.d !== 1n || k.n < 1n || k.n > BigInt(list.length)) throw new Undefined(`item ${show(k)} of a list of ${list.length}`);
        return list[Number(k.n) - 1];
      }
      case "count": {
        if (!Array.isArray(a[1])) throw new Unknown(`count in ${show(a[1])}`);
        return rational(BigInt(a[1].filter((x) => equal(x, a[0])).length));
      }
      case "rest": {
        const list = l(a[0]);
        if (list.length === 0) throw new Undefined("rest of an empty list");
        return list.slice(1);
      }
      case "apply": {
        if (!isFn(a[0])) throw new Unknown(`apply of ${show(a[0])}`);
        return this.call(a[0].fn, l(a[1]));
      }
      case "mean": {
        const list = l(a[0]).map(q);
        if (list.length === 0) throw new Undefined("mean of an empty list");
        return mul(list.reduce(add), rational(1n, BigInt(list.length)));
      }
      case "chance": {
        const list = l(a[1]);
        if (list.length === 0) throw new Undefined("chance in an empty list");
        return rational(BigInt(list.filter((x) => equal(x, a[0])).length), BigInt(list.length));
      }
      case "pairs": return l(a[0]).flatMap((x) => l(a[1]).map((y) => [x, y]));
      case "dot": return l(a[0]).map(q).map((x, i) => mul(x, q(l(a[1])[i]))).reduce(add);
      case "cross": {
        const [u, v] = [l(a[0]).map(q), l(a[1]).map(q)];
        const det = (i: number, j: number) => add(mul(u[i], v[j]), rational(-mul(u[j], v[i]).n, mul(u[j], v[i]).d));
        return [det(1, 2), det(2, 0), det(0, 1)];
      }
      case "type": {
        const v = a[0];
        if (isRational(v)) return rational(0n);
        if (Array.isArray(v)) return rational(1n);
        if (isSym(v) || isFn(v)) {
          const entry = this.registry.get(isSym(v) ? v.sym : v.fn);
          if (entry) return rational(BigInt(entry.type));
        }
        throw new Unknown(`type of ${show(v)}`);
      }
      case "eval": return this.evaluate(this.node(a[0]), new Map());
      case "fill": {
        const fill = (v: Value): Value => (Array.isArray(v) ? v.map(fill) : isSym(v) && v.sym === "?" ? a[1] : v);
        return fill(a[0]);
      }
      case "loss": {
        const key = `${show(a[0])} ${show(a[1])}`;
        if (!(key in LOSS)) throw new Unknown(`loss of ${key}`);
        return rational(BigInt(LOSS[key]));
      }
      case "move": {
        if (!isSym(a[0])) throw new Unknown(`move of ${show(a[0])}`);
        return strategyMove(a[0].sym, this.history(a[1]));
      }
      case "rounds": return this.rounds(a[0], a[1], q(a[2]));
      case "cost": return this.rounds(a[0], a[1], q(a[2])).map((round) => this.call("loss", round)).reduce((s: Rational, x) => add(s, q(x)), rational(0n));
    }
    throw new Unknown(`the operator ${name}`);
  }

  private history(value: Value): Sym[][] {
    if (!Array.isArray(value) || !value.every((round) => Array.isArray(round) && round.length === 2 && round.every(isSym))) {
      throw new Unknown(`a history ${show(value)}`);
    }
    return value as Sym[][];
  }

  // The history of n rounds of two strategies, from the first one's side; only for strategies that never pick by
  // chance (one move to pick from).
  private rounds(first: Value, second: Value, n: Rational): Sym[][] {
    if (!isSym(first) || !isSym(second) || n.d !== 1n || n.n < 0n) throw new Unknown(`rounds of ${show(first)} and ${show(second)}`);
    const key = `${first.sym} ${second.sym} ${n.n}`;
    const cached = this.played.get(key);
    if (cached) return cached;
    const mine: Sym[][] = [], theirs: Sym[][] = [];
    for (let i = 0n; i < n.n; i++) {
      const a = strategyMove(first.sym, mine), b = strategyMove(second.sym, theirs);
      if (a.length !== 1 || b.length !== 1) throw new Unknown(`rounds of a strategy that picks by chance`);
      mine.push([a[0], b[0]]);
      theirs.push([b[0], a[0]]);
    }
    this.played.set(key, mine);
    return mine;
  }

  private played = new Map<string, Sym[][]>();
}
