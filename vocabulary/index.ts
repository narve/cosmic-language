// The vocabulary: every token type and every symbol of the message, with its fixed id. This is the one master:
// the build's registry, the specification's tables (§6, §9) and the views are made from it.
import type { SymbolDef } from "./symbol.ts";
import type { TypeDef } from "./types.ts";
import { OPERATORS } from "./operators.ts";
import { CONSTANTS } from "./constants.ts";
import { VARIABLES } from "./variables.ts";
import { PARTICLES } from "./particles.ts";
import { ELEMENTS } from "./elements.ts";
import { DIMENSIONS } from "./dimensions.ts";
import { PHYSICAL_CONSTANTS } from "./physical-constants.ts";
import { MOLECULES } from "./molecules.ts";
import { DECOY_SYMBOLS } from "./decoy.ts";

// Every type and every symbol by its const name, for code that refers to a particular one (e.g. not, forAll).
export * from "./types.ts";
export * from "./operators.ts";
export * from "./constants.ts";
export * from "./variables.ts";
export * from "./particles.ts";
export * from "./elements.ts";
export * from "./dimensions.ts";
export * from "./physical-constants.ts";
export * from "./molecules.ts";
export * from "./decoy.ts";
export type { SymbolDef, Meaning } from "./symbol.ts";
export type { TypeDef } from "./types.ts";

// The symbols of each type that has symbols, in the order of the specification's tables.
export const SYMBOLS: readonly (readonly SymbolDef[])[] = [OPERATORS, CONSTANTS, VARIABLES, PARTICLES, ELEMENTS, DIMENSIONS, PHYSICAL_CONSTANTS, MOLECULES];

// The full message's symbols; the decoy's own symbols (decoy.ts) are kept apart, in DECOY.
export const VOCABULARY: readonly SymbolDef[] = SYMBOLS.flat();
export const DECOY: readonly SymbolDef[] = DECOY_SYMBOLS;

export function symbolsOf(type: TypeDef): readonly SymbolDef[] {
  return VOCABULARY.filter((symbol) => symbol.type === type);
}
