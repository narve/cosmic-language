// The symbol registry, read from the specification's tables (<table data-type="N">).
import type { Window } from "happy-dom";
import { BuildError, parse } from "./dom.ts";

export interface Entry {
  name: string;
  type: number;
  id: number;
  sign: string;
}

export type Registry = Map<string, Entry>;

export function loadRegistry(window: Window, specHtml: string): Registry {
  const document = parse(window, specHtml);
  const registry: Registry = new Map();
  const signs = new Map<string, string>();
  for (const table of document.querySelectorAll("table[data-type]")) {
    const type = Number(table.getAttribute("data-type"));
    const headings = Array.from(table.querySelectorAll("thead th")).map((th) => th.textContent!.trim());
    const [idColumn, nameColumn, signColumn] = ["Id", "Name", "Sign"].map((h) => headings.indexOf(h));
    if (idColumn < 0 || nameColumn < 0) throw new BuildError(`registry table of type ${type} needs Id and Name columns`);
    for (const row of table.querySelectorAll("tbody tr")) {
      const cells = row.children;
      const symbol: Entry = {
        type,
        id: Number(cells[idColumn].textContent!.trim()),
        name: cells[nameColumn].textContent!.trim(),
        sign: signColumn < 0 ? "" : cells[signColumn].textContent!.trim(),
      };
      const other = registry.get(symbol.name);
      if (other) throw new BuildError(`symbol name "${symbol.name}" is listed in type ${other.type} and type ${type}`);
      registry.set(symbol.name, symbol);
      if (symbol.sign) {
        if (signs.has(symbol.sign)) throw new BuildError(`sign "${symbol.sign}" is used by "${signs.get(symbol.sign)}" and "${symbol.name}"`);
        signs.set(symbol.sign, symbol.name);
      }
    }
  }
  for (const [sign, name] of signs) {
    if (registry.has(sign) && sign !== name) throw new BuildError(`sign "${sign}" of "${name}" is also a symbol name`);
  }
  return registry;
}
