// molecules: the symbols of type 9. Ids are fixed: never renumber, add new symbols with the next free id.
import { molecule } from "./types.ts";
import type { SymbolDef } from "./symbol.ts";

export const dihydrogen = { type: molecule, id: 1, name: "dihydrogen", sign: "H₂" } satisfies SymbolDef;
export const water = { type: molecule, id: 2, name: "water", sign: "H₂O" } satisfies SymbolDef;
export const methane = { type: molecule, id: 3, name: "methane", sign: "CH₄" } satisfies SymbolDef;
export const ammonia = { type: molecule, id: 4, name: "ammonia", sign: "NH₃" } satisfies SymbolDef;
export const carbonDioxide = { type: molecule, id: 5, name: "carbon-dioxide", sign: "CO₂" } satisfies SymbolDef;
export const adenine = { type: molecule, id: 6, name: "adenine", sign: "C₅H₅N₅" } satisfies SymbolDef;
export const thymine = { type: molecule, id: 7, name: "thymine", sign: "C₅H₆N₂O₂" } satisfies SymbolDef;
export const guanine = { type: molecule, id: 8, name: "guanine", sign: "C₅H₅N₅O" } satisfies SymbolDef;
export const cytosine = { type: molecule, id: 9, name: "cytosine", sign: "C₄H₅N₃O" } satisfies SymbolDef;

export const MOLECULES: readonly SymbolDef[] = [dihydrogen, water, methane, ammonia, carbonDioxide, adenine, thymine, guanine, cytosine];
