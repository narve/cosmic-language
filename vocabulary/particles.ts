// particles: the symbols of type 5. Ids increase in order of first appearance in the message; renumber when that order changes.
import { particle } from "./types.ts";
import type { SymbolDef } from "./symbol.ts";

export const electron = { type: particle, id: 1, name: "electron", sign: "e⁻" } satisfies SymbolDef;
export const proton = { type: particle, id: 2, name: "proton", sign: "p" } satisfies SymbolDef;
export const neutron = { type: particle, id: 3, name: "neutron", sign: "n" } satisfies SymbolDef;
export const photon = { type: particle, id: 4, name: "photon", sign: "γ" } satisfies SymbolDef;
export const antineutrino = { type: particle, id: 5, name: "antineutrino", sign: "ν̄ₑ" } satisfies SymbolDef;
export const positron = { type: particle, id: 6, name: "positron", sign: "e⁺" } satisfies SymbolDef;
export const kaon = { type: particle, id: 7, name: "kaon", sign: "K⁰L" } satisfies SymbolDef;

export const PARTICLES: readonly SymbolDef[] = [electron, proton, neutron, photon, antineutrino, positron, kaon];
