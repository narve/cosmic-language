// The lessons in lessons/ (ordered by file name, numbered by position) and their topics.
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import type { Window } from "happy-dom";
import { BuildError, parse } from "./dom.ts";

export interface Article {
  slug: string; // file name without .html
  title: string; // text of the first heading
  topics: string[]; // from data-topic; the first one groups the lesson in runs
  optional: boolean; // data-optional: may be left out of a message, so no other lesson may use what it introduces
  replaces?: string; // data-replaces: the slug of the lesson this one stands in for, in the decoy version only
  number: number; // position in the message
  source: string; // the whole file
}

// A topic, defined once as <section id="math"> in templates/topics.html: its title (h2) and introduction.
export interface Topic {
  name: string;
  title: string;
  intro: string; // html of the section, without its h2 and <cl-lessons>
}

export interface Group {
  topic: Topic;
  id: string; // the group's anchor: the topic name, then name-2, name-3 … for later runs
  first: boolean; // the first group of its topic (only this one shows the introduction)
  articles: Article[];
}

export function loadArticles(window: Window, dir: string, topics: Topic[]): Article[] {
  const names = new Set(topics.map((topic) => topic.name));
  const files = readdirSync(dir)
    .filter((file) => file.endsWith(".html"))
    .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
  const loaded = files.map((file) => {
    const source = readFileSync(join(dir, file), "utf8");
    const article = findArticle(parse(window, source), file);
    const heading = article.querySelector("h1, h2, h3, h4, h5, h6");
    const topics = (article.getAttribute("data-topic") ?? "").split(/\s+/).filter(Boolean);
    if (topics.length === 0) throw new BuildError(`${file}: the article needs a data-topic`);
    for (const name of topics) {
      if (!names.has(name)) throw new BuildError(`${file}: unknown topic "${name}" (see templates/topics.html)`);
    }
    return {
      slug: file.slice(0, -".html".length),
      title: heading ? heading.textContent!.trim() : file,
      topics,
      optional: article.hasAttribute("data-optional"),
      replaces: article.getAttribute("data-replaces") ?? undefined,
      number: 0,
      source,
    };
  });
  // Lessons are numbered by their place in the message; a lesson that replaces another takes that one's number.
  let number = 0;
  for (const article of loaded) if (!article.replaces) article.number = ++number;
  for (const article of loaded) {
    if (!article.replaces) continue;
    const original = loaded.find((other) => other.slug === article.replaces && !other.replaces);
    if (!original) throw new BuildError(`${article.slug}: data-replaces names "${article.replaces}", which is not a lesson`);
    article.number = original.number;
  }
  return loaded;
}

export function loadTopics(window: Window, html: string): Topic[] {
  const document = parse(window, html);
  return Array.from(document.querySelectorAll("main > section[id]"), (section) => {
    const copy = section.cloneNode(true) as Element;
    const title = copy.querySelector("h2")?.textContent?.trim() ?? section.id;
    copy.querySelectorAll("h2, cl-lessons").forEach((element) => element.remove());
    return { name: section.id, title, intro: copy.innerHTML.trim() };
  });
}

// The article's id on pages that include it: a valid CSS identifier, e.g. lesson-090-equal-and-not-equal.
export function anchor(article: Article): string {
  return `lesson-${article.slug}`;
}

// The single article.lesson of a page.
export function findArticle(document: Document, file: string): Element {
  const articles = document.querySelectorAll("article");
  if (articles.length !== 1 || !articles[0].matches(".lesson")) {
    throw new BuildError(`${file}: needs exactly one <article class="lesson">`);
  }
  return articles[0];
}

// Runs of consecutive lessons with the same first topic, in message order.
export function groupRuns(articles: Article[], topics: Topic[]): Group[] {
  const groups: Group[] = [];
  const seen = new Map<string, number>();
  for (const article of articles) {
    const name = article.topics[0];
    const last = groups[groups.length - 1];
    if (last && last.topic.name === name) last.articles.push(article);
    else {
      const count = (seen.get(name) ?? 0) + 1;
      seen.set(name, count);
      const topic = topics.find((c) => c.name === name)!;
      groups.push({ topic, id: count === 1 ? name : `${name}-${count}`, first: count === 1, articles: [article] });
    }
  }
  return groups;
}

// One group per topic, in the order of templates/topics.html; a lesson appears in each of its topics.
export function groupByTopic(articles: Article[], topics: Topic[]): Group[] {
  return topics
    .map((topic) => ({
      topic,
      id: topic.name,
      first: true,
      articles: articles.filter((article) => article.topics.includes(topic.name)),
    }))
    .filter((group) => group.articles.length > 0);
}
