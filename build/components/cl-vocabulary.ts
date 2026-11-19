// <cl-vocabulary type="operator">: the table of one type's symbols, from the vocabulary. With the attribute uses, two
// more columns: the lesson block that introduces each symbol, and the lessons that use it (needs the usage).
// <cl-types>: the table of the token types.
// Each element is replaced by what it renders. Every symbol row has an id (operator-exp, constant-π …) to link to.
import type { Window } from "happy-dom";
import { BuildError, escape } from "../dom.ts";
import { meaningHtml, symbolAnchor, symbolFragment } from "../meaning.ts";
import { TYPES, symbolsOf, type SymbolDef } from "../../vocabulary/index.ts";
import { blockId, type Usage } from "../usage.ts";

export function defineClVocabulary(window: Window, usage?: Usage): void {
  const document = window.document;
  const replace = (element: Element, html: string) => {
    const template = document.createElement("template");
    template.innerHTML = html;
    element.replaceWith(template.content);
  };
  const link = (symbol: SymbolDef) => symbolFragment(symbol);

  class ClVocabulary extends window.HTMLElement {
    connectedCallback() {
      const name = this.getAttribute("type");
      const type = TYPES.find((t) => t.name === name);
      if (!type) throw new BuildError(`<cl-vocabulary type="${name}">: no such type`);
      const symbols = [...symbolsOf(type)].sort((a, b) => a.id - b.id);
      const arity = type.name === "operator";
      const meaning = symbols.some((symbol) => symbol.meaning !== undefined);
      const uses = this.hasAttribute("uses");
      if (uses && !usage) throw new BuildError("<cl-vocabulary uses> needs the usage of the symbols");
      const head = ["Id", "Name", "Sign", ...(arity ? ["Arity"] : []), ...(meaning ? ["Meaning"] : []), ...(uses ? ["Introduced in", "Used in"] : [])];
      const lesson = (place: { article: { slug: string; number: number; title: string }; block: number }, text: string) =>
        `<a href="lessons/${place.article.slug}.html#${blockId(place.article as never, place.block)}" title="${escape(place.article.title)}">${text}</a>`;
      const rows = symbols.map((symbol) => {
        const cells = [String(symbol.id), `<code>${escape(symbol.name)}</code>`, escape(symbol.sign ?? "")];
        if (arity) cells.push(escape(symbol.arity ?? ""));
        if (meaning) cells.push(meaningHtml(symbol.meaning, link));
        if (uses) {
          const first = usage!.first.get(symbol.name);
          const all = usage!.uses.get(symbol.name) ?? [];
          cells.push(first ? lesson(first, `${first.article.number}. ${escape(first.article.title)}`) : "");
          cells.push(all.map((place) => lesson(place, String(place.article.number))).join(", "));
        }
        return `      <tr id="${escape(symbolAnchor(symbol))}">${cells.map((cell) => `<td>${cell}</td>`).join("")}</tr>`;
      });
      replace(this, `<table data-type="${type.id}">
    <thead><tr>${head.map((h) => `<th>${h}</th>`).join("")}</tr></thead>
    <tbody>
${rows.join("\n")}
    </tbody>
  </table>`);
    }
  }

  class ClTypes extends window.HTMLElement {
    connectedCallback() {
      const rows = TYPES.map((type) => `      <tr id="type-${type.name}"><td><code>${type.id}</code></td><td><code>${escape(type.name)}</code></td><td>${meaningHtml(type.meaning, link)}</td></tr>`);
      replace(this, `<table>
    <thead><tr><th>Type</th><th>Name</th><th>Value</th></tr></thead>
    <tbody>
${rows.join("\n")}
    </tbody>
  </table>`);
    }
  }

  window.customElements.define("cl-vocabulary", ClVocabulary);
  window.customElements.define("cl-types", ClTypes);
}
