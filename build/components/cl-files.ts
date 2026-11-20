// <cl-files version="minimal">: the list of a version's message files, with what each holds and its size, read
// from the files the build has written. The element is replaced by the list.
import { statSync } from "node:fs";
import { join } from "node:path";
import type { Window } from "happy-dom";
import { BuildError, escape } from "../dom.ts";

export interface VersionFiles {
  dir: string; // the version's folder in docs/, "" for the full version (its files are at the top)
  bits: number; // the length of the message in bits
}

export interface FilesContext {
  docs: string; // the docs/ folder on disk
  base: string; // the way from the page to docs/
  versions: Record<string, VersionFiles>;
}

const FILES: [name: string, about: string][] = [
  ["message.txt", "the message as text, as in the lessons: numbers, brackets and symbol names, with the comments"],
  ["message.bits", "the bits as text, one token per line, each with its symbol as a comment"],
  ["message.bin", "the bits, packed eight to a byte"],
  ["message.bin.txt", "message.bin as binary numbers, for viewing"],
];

export function defineClFiles(window: Window, context: FilesContext): void {
  const document = window.document;
  const number = (n: number) => n.toLocaleString("en-GB");

  class ClFiles extends window.HTMLElement {
    connectedCallback() {
      const name = this.getAttribute("version") ?? "";
      const version = context.versions[name];
      if (!version) throw new BuildError(`<cl-files version="${name}">: unknown version`);
      const items = FILES.map(([file, about]) => {
        const path = version.dir ? `${version.dir}/${file}` : file;
        const bytes = statSync(join(context.docs, path)).size;
        const size = file === "message.bin" ? `${number(version.bits)} bits in ${number(bytes)} bytes` : `${number(bytes)} bytes`;
        return `<li><a href="${escape(context.base + path)}"><code>${file}</code></a>: ${escape(about)} (${size}).</li>`;
      });
      const template = document.createElement("template");
      template.innerHTML = `<ul data-files>\n${items.join("\n")}\n</ul>`;
      this.replaceWith(template.content);
    }
  }

  window.customElements.define("cl-files", ClFiles as never);
}
