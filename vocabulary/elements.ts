// elements: the symbols of type 6. Ids are fixed: never renumber, add new symbols with the next free id.
import { element } from "./types.ts";
import type { SymbolDef } from "./symbol.ts";

export const hydrogen = { type: element, id: 1, name: "hydrogen", sign: "H" } satisfies SymbolDef;
export const helium = { type: element, id: 2, name: "helium", sign: "He" } satisfies SymbolDef;
export const carbon = { type: element, id: 6, name: "carbon", sign: "C" } satisfies SymbolDef;
export const nitrogen = { type: element, id: 7, name: "nitrogen", sign: "N" } satisfies SymbolDef;
export const oxygen = { type: element, id: 8, name: "oxygen", sign: "O" } satisfies SymbolDef;
export const neon = { type: element, id: 10, name: "neon", sign: "Ne" } satisfies SymbolDef;
export const argon = { type: element, id: 18, name: "argon", sign: "Ar" } satisfies SymbolDef;
export const krypton = { type: element, id: 36, name: "krypton", sign: "Kr" } satisfies SymbolDef;
export const xenon = { type: element, id: 54, name: "xenon", sign: "Xe" } satisfies SymbolDef;
export const radon = { type: element, id: 86, name: "radon", sign: "Rn" } satisfies SymbolDef;

export const ELEMENTS: readonly SymbolDef[] = [hydrogen, helium, carbon, nitrogen, oxygen, neon, argon, krypton, xenon, radon];
