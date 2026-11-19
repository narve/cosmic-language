// The symbol registry, made from the vocabulary (vocabulary/index.ts), the one master of every type and symbol.
// The vocabulary's shape is checked here: a mistake in it is a build error.
import { BuildError } from "./dom.ts";
import { TYPES, VOCABULARY, type SymbolDef, type TypeDef } from "../vocabulary/index.ts";

export interface Entry {
  name: string;
  type: number;
  id: number;
  sign: string;
  arity?: string; // operators only: "2", "2+", "0+" …
  symbol?: SymbolDef; // the vocabulary entry
}

export type Registry = Map<string, Entry>;

const ELEMENT = TYPES.find((type) => type.name === "element")!;

export function loadRegistry(): Registry {
  checkVocabulary();
  const registry: Registry = new Map();
  for (const symbol of VOCABULARY) {
    const entry: Entry = { name: symbol.name, type: symbol.type.id, id: symbol.id, sign: symbol.sign ?? "", symbol };
    if (symbol.arity !== undefined) entry.arity = symbol.arity;
    registry.set(symbol.name, entry);
  }
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
  for (const symbol of VOCABULARY) {
    const at = `${symbol.type.name} ${symbol.id} (${symbol.name})`;
    if (!TYPES.includes(symbol.type)) fail(`${at} has a type that is not in TYPES`);
    if (!symbol.name || /[\s()]/.test(symbol.name)) fail(`${at}: a name must be non-empty, without spaces or brackets`);
    if (/^\d+$/.test(symbol.name)) fail(`${at}: a name cannot be a number`);
    claim(symbol.name, at);
    if (symbol.sign && symbol.sign !== symbol.name) claim(symbol.sign, `the sign of ${at}`);
    const isOperator = symbol.type.name === "operator";
    if (isOperator && !/^\d+\+?$/.test(symbol.arity ?? "")) fail(`${at}: an operator needs an arity such as "2" or "2+"`);
    if (!isOperator && symbol.arity !== undefined) fail(`${at}: only operators have an arity`);
    if (!byType.has(symbol.type)) byType.set(symbol.type, []);
    byType.get(symbol.type)!.push(symbol);
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
