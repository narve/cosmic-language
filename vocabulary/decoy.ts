// The decoy's own symbols: names for what the decoy version says instead of the full message (decoy.html). A decoy
// symbol is only used by the lessons that replace another (data-replaces), and it sends the type and id that its
// place in the decoy calls for: ids first appear as 1, 2, 3 … in every version, so a decoy symbol takes the id of the
// full message's symbol at the same place. It is not tied to that symbol otherwise; the build checks the ids per
// version, and that no version sends one id under two names.
import { constant, molecule } from "./types.ts";
import type { SymbolDef } from "./symbol.ts";

// The hereditary molecules of the decoy's senders, and their parts (the chemistry of life, decoy)
export const xna = { type: constant, id: 57, name: "xna", meaning: "domain: the hereditary molecules of the decoy's senders, each two strands of bases on a backbone of threose and phosphate, wound round each other in a left-handed helix", decoy: true } satisfies SymbolDef;
export const diaminopurine = { type: molecule, id: 22, name: "diaminopurine", sign: "C₅H₆N₆", meaning: "2,6-diaminopurine, a base of the decoy's hereditary molecules", decoy: true } satisfies SymbolDef;
export const hydroxymethyluracil = { type: molecule, id: 23, name: "hydroxymethyluracil", sign: "C₅H₆N₂O₃", meaning: "5-hydroxymethyluracil, the partner of 2,6-diaminopurine", decoy: true } satisfies SymbolDef;
export const xanthine = { type: molecule, id: 24, name: "xanthine", sign: "C₅H₄N₄O₂", meaning: "xanthine, a base of the decoy's hereditary molecules", decoy: true } satisfies SymbolDef;
export const diaminopyrimidine = { type: molecule, id: 25, name: "diaminopyrimidine", sign: "C₄H₆N₄", meaning: "2,4-diaminopyrimidine, the partner of xanthine", decoy: true } satisfies SymbolDef;
export const threose = { type: molecule, id: 30, name: "threose", sign: "C₄H₈O₄", meaning: "threose, the sugar of the decoy's hereditary molecules", decoy: true } satisfies SymbolDef;
export const diaminopurineTriphosphate = { type: molecule, id: 31, name: "diaminopurine-triphosphate", sign: "C₁₀H₁₇N₆O₁₃P₃", meaning: "the triphosphate of 2,6-diaminopurine and ribose, which carries energy in the decoy's senders", decoy: true } satisfies SymbolDef;

export const DECOY_SYMBOLS: readonly SymbolDef[] = [xna, diaminopurine, hydroxymethyluracil, xanthine, diaminopyrimidine, threose, diaminopurineTriphosphate];
