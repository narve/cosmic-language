// variables: the symbols of type 4. Ids increase in order of first appearance in the message; renumber when that order changes.
import { variable } from "./types.ts";
import type { SymbolDef } from "./symbol.ts";

export const u = { type: variable, id: 1, name: "u" } satisfies SymbolDef;
export const v = { type: variable, id: 2, name: "v" } satisfies SymbolDef;
export const w = { type: variable, id: 3, name: "w" } satisfies SymbolDef;
export const z = { type: variable, id: 4, name: "z" } satisfies SymbolDef;

export const VARIABLES: readonly SymbolDef[] = [u, v, w, z];
