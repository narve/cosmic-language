// variables: the symbols of type 4. Ids are fixed: never renumber, add new symbols with the next free id.
import { variable } from "./types.ts";
import type { SymbolDef } from "./symbol.ts";

export const u = { type: variable, id: 1, name: "u" } satisfies SymbolDef;
export const v = { type: variable, id: 2, name: "v" } satisfies SymbolDef;
export const w = { type: variable, id: 3, name: "w" } satisfies SymbolDef;
export const z = { type: variable, id: 4, name: "z" } satisfies SymbolDef;

export const VARIABLES: readonly SymbolDef[] = [u, v, w, z];
