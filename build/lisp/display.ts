// Another display of the same sentences: ordinary mathematical notation, as HTML. It reads the parsed tree, never
// the source text, so it shows exactly what is sent: (= (+ 2 3) 5) becomes 2 + 3 = 5, (∀ u (list 1 2 3) (< u 4))
// becomes ∀u ∈ ⟨1, 2, 3⟩: u < 4. Only brackets the notation needs are shown.
import { escape } from "../dom.ts";
import type { Node } from "../check/structure.ts";
import type { Registry } from "../registry.ts";

const VARIABLE = 4;
// Binding strength: a higher number binds tighter. A part is put in brackets when it binds less tightly than its place.
const LOGIC = 1, RELATION = 2, SUM = 3, PRODUCT = 4, NEGATION = 5, POWER = 6, ATOM = 7;
const RELATIONS = new Set(["=", "≠", "<", ">", "≤", "≥"]);
const INFIX: Record<string, [string, number]> = {
  "+": [" + ", SUM], "−": [" − ", SUM], "×": [" × ", PRODUCT], "÷": [" / ", PRODUCT], dot: [" · ", PRODUCT], cross: [" × ", PRODUCT],
  and: [" ∧ ", LOGIC], or: [" ∨ ", LOGIC], implies: [" ⇒ ", LOGIC],
};

interface Shown { html: string; strength: number }

export function mathHtml(node: Node, registry: Registry): string {
  return new Display(registry).show(node).html;
}

class Display {
  constructor(private registry: Registry) {}

  show(node: Node): Shown {
    if (node.token) return { html: this.atom(node), strength: ATOM };
    const [head, ...args] = node.items!;
    const name = head.token?.text ?? "";
    const part = (n: Node, strength: number) => {
      const shown = this.show(n);
      return shown.strength < strength ? `(${shown.html})` : shown.html;
    };
    const variable = (n: Node) => this.atom(n);
    if (RELATIONS.has(name)) return { html: args.map((a) => part(a, RELATION + 1)).join(` ${escape(name)} `), strength: RELATION };
    if (name in INFIX) {
      const [sign, strength] = INFIX[name];
      // left-associative: the first part may bind as tightly as the whole, the others must bind more tightly
      return { html: args.map((a, i) => part(a, i === 0 ? strength : strength + 1)).join(escape(sign)), strength };
    }
    switch (name) {
      case "neg": return { html: `−${part(args[0], NEGATION)}`, strength: NEGATION };
      case "not": return { html: `¬${part(args[0], NEGATION)}`, strength: NEGATION };
      case "^": return { html: `${part(args[0], POWER + 1)}<sup>${this.show(args[1]).html}</sup>`, strength: POWER };
      case "abs": return { html: `|${this.show(args[0]).html}|`, strength: ATOM };
      case "big": {
        const digits = args.map((a) => a.token?.type === 0 ? a.token.value : NaN);
        if (digits.every((d) => !Number.isNaN(d))) return { html: String(digits.reduce((s, d) => s * 256 + d, 0)), strength: ATOM };
        break;
      }
      case "list": return { html: `⟨${args.map((a) => this.show(a).html).join(", ")}⟩`, strength: ATOM };
      case "quote": return { html: `⌜${this.show(args[0]).html}⌝`, strength: ATOM };
      case "∀":
      case "∃":
        return { html: `${escape(name)}${variable(args[0])} ∈ ${part(args[1], ATOM)}: ${this.show(args[2]).html}`, strength: LOGIC - 1 };
      case "sequence":
        return { html: `[${this.show(args[2]).html} | ${variable(args[0])} ∈ ${part(args[1], ATOM)}]`, strength: ATOM };
      case "average":
        return { html: `avg<sub>${variable(args[0])} ∈ ${this.show(args[1]).html}</sub> ${part(args[2], POWER)}`, strength: PRODUCT };
      case "let":
        return { html: `let ${variable(args[0])} = ${this.show(args[1]).html} in ${this.show(args[2]).html}`, strength: LOGIC - 1 };
      case "if":
        return { html: `if ${this.show(args[0]).html} then ${this.show(args[1]).html} else ${this.show(args[2]).html}`, strength: LOGIC - 1 };
    }
    // any other operator: as a function, f(a, b)
    return { html: `${this.symbol(name)}(${args.map((a) => this.show(a).html).join(", ")})`, strength: ATOM };
  }

  private atom(node: Node): string {
    const token = node.token!;
    if (token.type === VARIABLE) return `<var>${escape(token.text)}</var>`;
    const alias = this.registry.get(token.text)?.alias;
    if (alias) return `<data value="${alias.id}" data-type-name>${escape(token.text)}</data>`;
    if (token.type === 0) return escape(token.text);
    return this.symbol(token.text);
  }

  private symbol(name: string): string {
    const sign = this.registry.get(name)?.sign;
    return escape(sign || name);
  }
}
