// The checks of the build, as separate checkers that can be chosen one by one.
//
// Each checker has a name, says what it checks, and throws a BuildError on a broken rule; it returns a one-line
// summary. `npm run build` runs them all. To run only some, or to leave some out:
//   CHECKS=structure,id-order npm run build
//   SKIP_CHECKS=measurements,evaluate npm run build
// The shape of the vocabulary is checked when the registry is made, before any checker: nothing works without it.
import { BuildError } from "../dom.ts";
import type { Message } from "../message.ts";
import type { Registry } from "../registry.ts";
import { checkMeasurements, MARGIN } from "./measurements.ts";
import { checkIdOrder, checkMinimal, checkOptional, checkSelfReference, checkStructure } from "./structure.ts";
import { checkEvaluation } from "./evaluate.ts";

export const VERSIONS = ["full", "cautious", "minimal", "decoy"] as const;
export type Version = (typeof VERSIONS)[number];

export interface CheckContext {
  versions: Record<Version, Message>;
  text: Record<Version, string>; // each version as message.txt
  registry: Registry;
  isMinimal: (slug: string) => boolean;
  isOptional: (slug: string) => boolean;
}

export interface Checker {
  name: string;
  about: string;
  run: (context: CheckContext) => string; // a summary; throws a BuildError on a broken rule
}

export const CHECKERS: Checker[] = [
  {
    name: "structure",
    about: "groups start with an operator of the right arity, variables are bound, ? only in quote, type names only where a type is meant, every symbol is used, a new symbol is in at least 3 sentences of its lesson (spec §10.1)",
    run: ({ versions, registry }) => {
      checkStructure(versions.full, registry);
      checkStructure(versions.decoy, registry);
      return "full and decoy";
    },
  },
  {
    name: "id-order",
    about: "in every version, the ids of each type first appear as 1, 2, 3 … with none missing",
    run: ({ versions, registry }) => {
      for (const version of VERSIONS) checkIdOrder(versions[version], registry, version);
      return VERSIONS.join(", ");
    },
  },
  {
    name: "minimal",
    about: "a minimal lesson only uses symbols that minimal lessons introduce",
    run: ({ versions, isMinimal }) => {
      checkMinimal(versions.full, isMinimal);
      return "ok";
    },
  },
  {
    name: "optional",
    about: "no lesson depends on a symbol that an optional lesson introduces",
    run: ({ versions, isOptional }) => {
      checkOptional(versions.full, isOptional);
      return "ok";
    },
  },
  {
    name: "self-reference",
    about: "what each version says about itself (item and count of message) holds for that version",
    run: ({ versions }) => `${VERSIONS.map((version) => checkSelfReference(versions[version], version)).join(", ")} sentences (${VERSIONS.join(", ")})`,
  },
  {
    name: "measurements",
    about: `every measured range is at least ${MARGIN} standard uncertainties from the reference value (full version only)`,
    run: ({ text }) => {
      const result = checkMeasurements(text.full);
      if (result.failures > 0) {
        const failing = result.report.filter((line) => !line.startsWith("ok"));
        throw new BuildError(`${result.failures} measured ranges fail (each bound must be at least ${MARGIN} standard uncertainties from the reference value):\n${failing.join("\n")}`);
      }
      return `${result.checked} ranges, all at least ${MARGIN} standard uncertainties inside their bounds`;
    },
  },
  {
    name: "evaluate",
    about: "every sentence the interpreter can compute is true, and none divides by zero (full and decoy)",
    run: ({ versions, registry }) => checkEvaluation(versions.full, registry),
  },
];

// Runs the chosen checkers, in the order above, and returns their summaries.
export function runCheckers(context: CheckContext, env: Record<string, string | undefined> = process.env): string[] {
  const names = new Set(CHECKERS.map((checker) => checker.name));
  const list = (value: string | undefined) => (value ?? "").split(",").map((name) => name.trim()).filter(Boolean);
  const only = list(env.CHECKS);
  const skip = list(env.SKIP_CHECKS);
  for (const name of [...only, ...skip]) {
    if (!names.has(name)) throw new BuildError(`no checker "${name}"; the checkers are ${[...names].join(", ")}`);
  }
  return CHECKERS.filter((checker) => (only.length === 0 || only.includes(checker.name)) && !skip.includes(checker.name)).map(
    (checker) => `${checker.name}: ${checker.run(context)}`,
  );
}
