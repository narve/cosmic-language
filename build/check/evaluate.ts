// The evaluate checker: every sentence the interpreter (build/lisp/evaluate.ts) can compute must be true, and none
// may divide by zero. Sentences it cannot compute are counted, with the most common reasons, but not checked.
import { BuildError } from "../dom.ts";
import { Interpreter, Undefined, Unknown } from "../lisp/evaluate.ts";
import type { Message } from "../message.ts";
import type { Registry } from "../registry.ts";
import { parseBlock, show } from "./structure.ts";

export interface Evaluation {
  true: number;
  unknown: number;
  reasons: Map<string, number>; // why sentences could not be computed
  failures: string[];
}

export function evaluateMessage(message: Message, registry: Registry): Evaluation {
  const interpreter = new Interpreter(registry);
  const result: Evaluation = { true: 0, unknown: 0, reasons: new Map(), failures: [] };
  for (const { article, blocks } of message.articles) {
    blocks.forEach((block, index) => {
      if (block.bits !== undefined) return;
      for (const node of parseBlock(block.lines, `${article.slug}, block ${index + 1}`)) {
        if (!node.items) continue; // a bare number (the calibration)
        try {
          if (interpreter.truth(node)) result.true++;
          else result.failures.push(`${node.where}: false: ${show(node)}`);
        } catch (error) {
          if (error instanceof Undefined) result.failures.push(`${node.where}: ${error.message}, in ${show(node)}`);
          else if (error instanceof Unknown) {
            result.unknown++;
            const reason = error.message.replace(/ of .*$/, "");
            result.reasons.set(reason, (result.reasons.get(reason) ?? 0) + 1);
          } else throw error;
        }
      }
    });
  }
  return result;
}

export function checkEvaluation(message: Message, registry: Registry): string {
  const result = evaluateMessage(message, registry);
  if (result.failures.length > 0) {
    throw new BuildError(`${result.failures.length} sentences are false or undefined to the interpreter:\n${result.failures.join("\n")}`);
  }
  const top = [...result.reasons].sort((a, b) => b[1] - a[1]).slice(0, 3).map(([reason, n]) => `${reason} ${n}`);
  return `${result.true} sentences computed, all true; ${result.unknown} not computable (most often: ${top.join("; ")})`;
}
