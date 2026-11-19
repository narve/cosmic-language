// dimensions: the symbols of type 7. Ids are fixed: never renumber, add new symbols with the next free id.
import { dimension } from "./types.ts";
import type { SymbolDef } from "./symbol.ts";

export const massDim = { type: dimension, id: 1, name: "M", meaning: "mass" } satisfies SymbolDef;
export const lengthDim = { type: dimension, id: 2, name: "L", meaning: "length" } satisfies SymbolDef;
export const timeDim = { type: dimension, id: 3, name: "T", meaning: "time" } satisfies SymbolDef;
export const chargeDim = { type: dimension, id: 4, name: "Q", meaning: "charge" } satisfies SymbolDef;
export const temperatureDim = { type: dimension, id: 5, name: "Θ", meaning: "temperature" } satisfies SymbolDef;

export const DIMENSIONS: readonly SymbolDef[] = [massDim, lengthDim, timeDim, chargeDim, temperatureDim];
