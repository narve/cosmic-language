// molecules: the symbols of type 9. Ids are fixed: never renumber, add new symbols with the next free id.
import { molecule } from "./types.ts";
import type { SymbolDef } from "./symbol.ts";

export const dihydrogen = { type: molecule, id: 1, name: "dihydrogen", sign: "H₂" } satisfies SymbolDef;
export const water = { type: molecule, id: 2, name: "water", sign: "H₂O" } satisfies SymbolDef;
export const methane = { type: molecule, id: 3, name: "methane", sign: "CH₄" } satisfies SymbolDef;
export const ammonia = { type: molecule, id: 4, name: "ammonia", sign: "NH₃" } satisfies SymbolDef;
export const carbonDioxide = { type: molecule, id: 5, name: "carbon-dioxide", sign: "CO₂" } satisfies SymbolDef;
export const carbonMonoxide = { type: molecule, id: 6, name: "carbon-monoxide", sign: "CO" } satisfies SymbolDef;
export const hydrogenCyanide = { type: molecule, id: 7, name: "hydrogen-cyanide", sign: "HCN" } satisfies SymbolDef;
export const formaldehyde = { type: molecule, id: 8, name: "formaldehyde", sign: "H₂CO" } satisfies SymbolDef;
export const methanol = { type: molecule, id: 9, name: "methanol", sign: "CH₃OH" } satisfies SymbolDef;
export const acetylene = { type: molecule, id: 10, name: "acetylene", sign: "C₂H₂" } satisfies SymbolDef;
export const cyanoacetylene = { type: molecule, id: 11, name: "cyanoacetylene", sign: "HC₃N" } satisfies SymbolDef;
export const dinitrogen = { type: molecule, id: 12, name: "dinitrogen", sign: "N₂" } satisfies SymbolDef;
export const dioxygen = { type: molecule, id: 13, name: "dioxygen", sign: "O₂" } satisfies SymbolDef;
export const glucose = { type: molecule, id: 14, name: "glucose", sign: "C₆H₁₂O₆" } satisfies SymbolDef;
export const glycine = { type: molecule, id: 15, name: "glycine", sign: "C₂H₅NO₂" } satisfies SymbolDef;
export const adenine = { type: molecule, id: 16, name: "adenine", sign: "C₅H₅N₅" } satisfies SymbolDef;
export const thymine = { type: molecule, id: 17, name: "thymine", sign: "C₅H₆N₂O₂" } satisfies SymbolDef;
export const guanine = { type: molecule, id: 18, name: "guanine", sign: "C₅H₅N₅O" } satisfies SymbolDef;
export const cytosine = { type: molecule, id: 19, name: "cytosine", sign: "C₄H₅N₃O" } satisfies SymbolDef;
export const uracil = { type: molecule, id: 20, name: "uracil", sign: "C₄H₄N₂O₂" } satisfies SymbolDef;
export const urea = { type: molecule, id: 21, name: "urea", sign: "CH₄N₂O" } satisfies SymbolDef;
export const dopamine = { type: molecule, id: 22, name: "dopamine", sign: "C₈H₁₁NO₂" } satisfies SymbolDef;
export const serotonin = { type: molecule, id: 23, name: "serotonin", sign: "C₁₀H₁₂N₂O" } satisfies SymbolDef;
export const adrenaline = { type: molecule, id: 24, name: "adrenaline", sign: "C₉H₁₃NO₃" } satisfies SymbolDef;

export const MOLECULES: readonly SymbolDef[] = [dihydrogen, water, methane, ammonia, carbonDioxide, carbonMonoxide, hydrogenCyanide, formaldehyde, methanol, acetylene, cyanoacetylene, dinitrogen, dioxygen, glucose, glycine, adenine, thymine, guanine, cytosine, uracil, urea, dopamine, serotonin, adrenaline];
