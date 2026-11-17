// Shared happy-dom helpers: a window that never loads or runs page resources.
import { Window } from "happy-dom";

export class BuildError extends Error {}

export function createWindow(): Window {
  return new Window({
    settings: {
      disableJavaScriptFileLoading: true,
      disableJavaScriptEvaluation: true,
      disableCSSFileLoading: true,
      disableIframePageLoading: true,
    },
  });
}

// Parses a page into a stand-alone document (no custom elements are upgraded in it).
export function parse(window: Window, html: string): Document {
  return new window.DOMParser().parseFromString(html, "text/html") as unknown as Document;
}

export function serialize(document: Document): string {
  return "<!DOCTYPE html>\n" + document.documentElement.outerHTML + "\n";
}

export function escape(text: string): string {
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
