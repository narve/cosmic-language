// The article files in lessons/: ordered by file name, numbered by position.
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import type { Window } from "happy-dom";
import { BuildError, parse } from "./dom.ts";

export interface Article {
  slug: string; // file name without .html
  kind: "part" | "lesson";
  title: string; // text of the first heading
  number: number; // position among the parts, or among the lessons
  source: string; // the whole file
}

export function loadArticles(window: Window, dir: string): Article[] {
  const files = readdirSync(dir)
    .filter((file) => file.endsWith(".html"))
    .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
  const count = { part: 0, lesson: 0 };
  return files.map((file) => {
    const source = readFileSync(join(dir, file), "utf8");
    const article = findArticle(parse(window, source), file);
    const kind = article.classList.contains("part") ? "part" : "lesson";
    const heading = article.querySelector("h1, h2, h3, h4, h5, h6");
    return {
      slug: file.slice(0, -".html".length),
      kind,
      title: heading ? heading.textContent!.trim() : file,
      number: ++count[kind],
      source,
    };
  });
}

// The article's id on pages that include it: a valid CSS identifier, e.g. lesson-080-counting.
export function anchor(article: Article): string {
  return `${article.kind}-${article.slug}`;
}

// The single article.lesson or article.part of a page.
export function findArticle(document: Document, file: string): Element {
  const articles = document.querySelectorAll("article");
  if (articles.length !== 1 || !articles[0].matches(".lesson, .part")) {
    throw new BuildError(`${file}: needs exactly one <article class="lesson"> or <article class="part">`);
  }
  return articles[0];
}

// Parts with the lessons that follow them. Lessons before the first part form a group without a part.
export function groupByPart(articles: Article[]): { part?: Article; lessons: Article[] }[] {
  const groups: { part?: Article; lessons: Article[] }[] = [];
  for (const article of articles) {
    if (article.kind === "part") groups.push({ part: article, lessons: [] });
    else {
      if (groups.length === 0) groups.push({ lessons: [] });
      groups[groups.length - 1].lessons.push(article);
    }
  }
  return groups;
}
