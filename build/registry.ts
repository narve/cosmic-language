// The symbol registry, made from the vocabulary (vocabulary/index.ts), the one master of every type and symbol.
// The vocabulary's shape is checked here: a mistake in it is a build error.
import { BuildError } from "./dom.ts";
import { DECOY, TYPES, VOCABULARY, type SymbolDef, type TypeDef } from "../vocabulary/index.ts";

export interface Entry {
  name: string;
  type: number;
  id: number;
  sign: string;
  arity?: string; // operators only: "2", "2+", "0+" …
  symbol?: SymbolDef; // the vocabulary entry
  alias?: TypeDef; // a type name, written where a type is meant and sent as the number of the type (type 0)
  decoy?: boolean; // a symbol of the decoy version only (vocabulary/decoy.ts)
}

export type Registry = Map<string, Entry>;

const ELEMENT = TYPES.find((type) => type.name === "element")!;

export function loadRegistry(): Registry {
  checkVocabulary();
  const registry: Registry = new Map();
  for (const symbol of [...VOCABULARY, ...DECOY]) {
    const entry: Entry = { name: symbol.name, type: symbol.type.id, id: symbol.id, sign: symbol.sign ?? "", symbol };
    if (symbol.arity !== undefined) entry.arity = symbol.arity;
    if (symbol.decoy) entry.decoy = true;
    registry.set(symbol.name, entry);
  }
  // Type names are aliases: (= (type (quote u)) variable) is sent as (= (type (quote u)) 4).
  for (const type of TYPES) registry.set(type.name, { name: type.name, type: 0, id: type.id, sign: "", alias: type });
  return registry;
}

function checkVocabulary(): void {
  const fail = (message: string) => {
    throw new BuildError(`vocabulary: ${message}`);
  };
  TYPES.forEach((type, index) => {
    if (type.id !== index) fail(`the types must be listed in order of their ids: ${type.name} has id ${type.id} at position ${index}`);
  });
  const names = new Map<string, string>(); // name or sign → what it belongs to
  const claim = (key: string, owner: string) => {
    if (names.has(key)) fail(`"${key}" is used by ${names.get(key)} and by ${owner}`);
    names.set(key, owner);
  };
  for (const type of TYPES) claim(type.name, `the type ${type.name}`);
  const byType = new Map<TypeDef, SymbolDef[]>();
  const check = (symbol: SymbolDef) => {
    const at = `${symbol.type.name} ${symbol.id} (${symbol.name})`;
    if (!TYPES.includes(symbol.type)) fail(`${at} has a type that is not in TYPES`);
    if (!symbol.name || /[\s()]/.test(symbol.name)) fail(`${at}: a name must be non-empty, without spaces or brackets`);
    if (/^\d+$/.test(symbol.name)) fail(`${at}: a name cannot be a number`);
    claim(symbol.name, at);
    if (symbol.sign && symbol.sign !== symbol.name) claim(symbol.sign, `the sign of ${at}`);
    const isOperator = symbol.type.name === "operator";
    if (isOperator && !/^\d+\+?$/.test(symbol.arity ?? "")) fail(`${at}: an operator needs an arity such as "2" or "2+"`);
    if (!isOperator && symbol.arity !== undefined) fail(`${at}: only operators have an arity`);
  };
  for (const symbol of VOCABULARY) {
    check(symbol);
    if (symbol.decoy) fail(`${symbol.type.name} ${symbol.id} (${symbol.name}) is marked decoy: decoy symbols belong in vocabulary/decoy.ts`);
    if (!byType.has(symbol.type)) byType.set(symbol.type, []);
    byType.get(symbol.type)!.push(symbol);
  }
  // A decoy symbol may share its type and id with a symbol of the full message, never with another decoy symbol;
  // whether its id fits its place is checked per version (id-order).
  const decoyIds = new Set<string>();
  for (const symbol of DECOY) {
    check(symbol);
    const at = `${symbol.type.name} ${symbol.id} (${symbol.name})`;
    if (!symbol.decoy) fail(`${at} is in vocabulary/decoy.ts but not marked decoy`);
    if (symbol.type === ELEMENT) fail(`${at}: an element's id is its atomic number, so it has no decoy name`);
    if (decoyIds.has(`${symbol.type.id} ${symbol.id}`)) fail(`two decoy ${symbol.type.name} symbols share the id ${symbol.id}`);
    decoyIds.add(`${symbol.type.id} ${symbol.id}`);
  }
  for (const [type, symbols] of byType) {
    const ids = symbols.map((symbol) => symbol.id);
    if (new Set(ids).size !== ids.length) fail(`two ${type.name} symbols share an id`);
    if (type === ELEMENT) continue; // an element's id is its atomic number
    const sorted = [...ids].sort((a, b) => a - b);
    sorted.forEach((id, index) => {
      if (id !== index + 1) fail(`the ${type.name} ids must run 1, 2, 3 … without gaps; ${index + 1} is missing`);
    });
  }
}

// The names of the symbols that belong to a version: the full message's, and in the decoy the decoy's own symbols
// in place of the full message's symbols with the same type and id.
export function versionSymbols(registry: Registry, decoy: boolean): Set<string> {
  const entries = [...registry.values()].filter((entry) => !entry.alias);
  const taken = new Set(entries.filter((entry) => entry.decoy).map((entry) => `${entry.type} ${entry.id}`));
  return new Set(entries
    .filter((entry) => (decoy ? entry.decoy || !taken.has(`${entry.type} ${entry.id}`) : !entry.decoy))
    .map((entry) => entry.name));
}
