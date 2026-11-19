// The new-symbols checker: a "New …" clause in a lesson's prose (from "New" to the first "." or ";") may only name
// symbols that the lesson introduces. Each lesson page also shows a generated list of what it introduces, so the
// prose need not name them all; but what it names as new must be new. Mentions of older symbols belong after the
// clause, e.g. "New: cos, which gives an angle; cos is built from exp."
import { BuildError, createWindow, parse } from "../dom.ts";
import { findArticle } from "../lessons.ts";
import type { Message } from "../message.ts";
import type { Registry } from "../registry.ts";
import { computeUsage } from "../usage.ts";

export function checkNewSymbols(full: Message, decoy: Message, registry: Registry): string {
  const usage = computeUsage(full);
  // a lesson that replaces another (the decoy) introduces what the lesson it replaces introduces
  const newIn = (slug: string, replaces?: string) => new Set(usage.newIn.get(replaces ?? slug) ?? []);
  const articles = [...full.articles, ...decoy.articles.filter(({ article }) => article.replaces)].map(({ article }) => article);
  const window = createWindow();
  const errors: string[] = [];
  let clauses = 0;
  for (const article of articles) {
    const element = findArticle(parse(window, article.source), article.slug);
    const introduced = newIn(article.slug, article.replaces);
    for (const paragraph of element.querySelectorAll("p")) {
      for (const clause of paragraph.innerHTML.matchAll(/\bNew\b[^.;]*/g)) {
        clauses++;
        for (const code of clause[0].matchAll(/<code>([^<]*)<\/code>/g)) {
          const name = code[1].replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&");
          if (registry.get(name)?.symbol && !introduced.has(name)) {
            errors.push(`${article.slug}: "New …" names ${name}, which this lesson does not introduce`);
          }
        }
      }
    }
  }
  void window.happyDOM.close();
  if (errors.length > 0) throw new BuildError(errors.join("\n"));
  return `${clauses} "New …" clauses, every symbol they name is introduced there`;
}
