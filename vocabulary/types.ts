// The token types: the type chunk of a token. Ids are fixed. Names are lowercase; how they are shown (small caps,
// upper case …) is a matter of formatting.
//
// In the lessons a type name may be written where a type is meant, as in (= (type (quote u)) variable): it is an
// alias, sent as the number of its type (here 4). Nothing about types is sent as words.

export interface TypeDef {
  id: number; // the type chunk
  name: string; // lowercase, unique among type names and symbol names
  meaning: string; // the value chunk of a token of this type; `code` and {var} as in symbol meanings
}

export const number = { id: 0, name: "number", meaning: "One chunk: a natural number 0–255" } as const satisfies TypeDef;
export const brackets = { id: 1, name: "brackets", meaning: "One chunk: `0` = OPEN, `1` = CLOSE. Values `2–255` are reserved for later structural tokens." } as const satisfies TypeDef;
export const operator = { id: 2, name: "operator", meaning: "One chunk: an operator or relation id (§9.1)" } as const satisfies TypeDef;
export const constant = { id: 3, name: "constant", meaning: "One chunk: a constant id (§9.2)" } as const satisfies TypeDef;
export const variable = { id: 4, name: "variable", meaning: "One chunk: a variable id (§9.3)" } as const satisfies TypeDef;
export const particle = { id: 5, name: "particle", meaning: "One chunk: a particle id (§9.4)" } as const satisfies TypeDef;
export const element = { id: 6, name: "element", meaning: "One chunk: the atomic number (the number of protons)" } as const satisfies TypeDef;
export const dimension = { id: 7, name: "dimension", meaning: "One chunk: a dimension id (§9.6)" } as const satisfies TypeDef;
export const physicalConstant = { id: 8, name: "physical-constant", meaning: "One chunk: a physical constant id (§9.7)" } as const satisfies TypeDef;
export const molecule = { id: 9, name: "molecule", meaning: "One chunk: a molecule id (§9.8)" } as const satisfies TypeDef;

export const TYPES: readonly TypeDef[] = [number, brackets, operator, constant, variable, particle, element, dimension, physicalConstant, molecule];
