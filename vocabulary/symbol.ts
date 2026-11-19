// The shape of a symbol in the vocabulary.
import type { TypeDef } from "./types.ts";

export interface SymbolDef {
  type: TypeDef; // the type const itself, not its number
  id: number; // the value chunk; fixed: 1, 2, 3 … per type (an element's id is its atomic number)
  name: string; // as written in the lessons: "=", "∀", "exp", "planck-length"
  sign?: string; // how the symbols view shows it, if not by its name: "¬", "·", "H"
  arity?: string; // operators only: "2" exactly two arguments, "2+" two or more, "0+" any number
  meaning?: Meaning;
}

// A meaning is plain text in which `code` is shown as code and {u} as a variable. Written with the tag m, it may
// refer to other symbols: m`never below ${plus} …`. A reference is a TypeScript value, so a misspelt or removed
// symbol is a compile error, not a dead link; on the pages it becomes a link to that symbol.
export type Meaning = string | { parts: readonly (string | SymbolDef)[] };

export const m = (strings: TemplateStringsArray, ...refs: SymbolDef[]): Meaning => ({
  parts: strings.flatMap((text, i) => (i < refs.length ? [text, refs[i]] : [text])),
});
