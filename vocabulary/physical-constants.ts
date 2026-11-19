// physical-constants: the symbols of type 8. Ids are fixed: never renumber, add new symbols with the next free id.
import { physicalConstant } from "./types.ts";
import type { SymbolDef } from "./symbol.ts";

export const c = { type: physicalConstant, id: 1, name: "c", meaning: "the speed of every photon; wavelength × frequency" } satisfies SymbolDef;
export const hbar = { type: physicalConstant, id: 2, name: "ħ", meaning: "a photon's energy = ħ × 2π × frequency" } satisfies SymbolDef;
export const G = { type: physicalConstant, id: 3, name: "G", meaning: "Newton's law of gravitation" } satisfies SymbolDef;
export const ke = { type: physicalConstant, id: 4, name: "ke", meaning: "Coulomb's law of the electric force" } satisfies SymbolDef;
export const km = { type: physicalConstant, id: 5, name: "km", meaning: "the law of the magnetic force between two wires; ke ÷ km = c²" } satisfies SymbolDef;
export const planckLength = { type: physicalConstant, id: 6, name: "planck-length", sign: "ℓP", meaning: "planck-length² = ħG / c³" } satisfies SymbolDef;
export const planckTime = { type: physicalConstant, id: 7, name: "planck-time", sign: "tP", meaning: "planck-time² = ħG / c⁵" } satisfies SymbolDef;
export const planckMass = { type: physicalConstant, id: 8, name: "planck-mass", sign: "mP", meaning: "planck-mass² = ħc / G" } satisfies SymbolDef;
export const hydrogenLine = { type: physicalConstant, id: 9, name: "hydrogen-line", meaning: "the photon of hydrogen's 21 cm line, identified by its energy and period" } satisfies SymbolDef;
export const kB = { type: physicalConstant, id: 10, name: "kB", meaning: "a gas's particles have average energy of motion 3/2 kB × temperature" } satisfies SymbolDef;
export const planckTemperature = { type: physicalConstant, id: 11, name: "planck-temperature", sign: "TP", meaning: "planck-temperature² = ħc⁵ / (G kB²)" } satisfies SymbolDef;

export const PHYSICAL_CONSTANTS: readonly SymbolDef[] = [c, hbar, G, ke, km, planckLength, planckTime, planckMass, hydrogenLine, kB, planckTemperature];
