// <cl-lessons>: lists the lessons of site/lessons/ as links, or includes them as articles.
// The element is replaced by what it renders.
//
//   as        links | articles            (default links)
//   href      file | anchor               (links; default file)
//   topic  one or more topic names  (only lessons in one of them; default all)
//   group     none | runs | topic      (default none)
//             runs: consecutive lessons of the same first topic, in message order
//             topic: one group per topic, in the order of site/topics.html
//   src       directory of the pages      (links with href="file"; default lessons/)
//   views     generated views to add      (articles; default "symbols math chunks bits", "" for none)
import type { Window } from "happy-dom";
import { escape } from "../dom.ts";
import { anchor as id, findArticle, groupByTopic, groupRuns, type Article, type Topic, type Group } from "../lessons.ts";
import type { Registry } from "../registry.ts";
import { VIEWS, type View } from "../views.ts";
import { enrichArticle } from "../enrich.ts";
import type { Usage } from "../usage.ts";

export interface Context {
  articles: Article[];
  topics: Topic[];
  registry: Registry;
  usage: Usage;
}

export function defineClLessons(window: Window, context: Context): void {
  const document = window.document;

  class ClLessons extends window.HTMLElement {
    connectedCallback() {
      const html = this.getAttribute("as") === "articles" ? this.articles() : this.links();
      const template = document.createElement("template");
      template.innerHTML = html;
      this.replaceWith(template.content);
    }

    selected(): Article[] {
      const wanted = (this.getAttribute("topic") ?? "").split(/\s+/).filter(Boolean);
      if (wanted.length === 0) return context.articles;
      return context.articles.filter((article) => article.topics.some((name) => wanted.includes(name)));
    }

    groups(): Group[] | undefined {
      const group = this.getAttribute("group") ?? "none";
      if (group === "runs") return groupRuns(this.selected(), context.topics);
      if (group === "topic") return groupByTopic(this.selected(), context.topics);
      return undefined;
    }

    links(): string {
      const anchor = this.getAttribute("href") === "anchor";
      const src = this.getAttribute("src") ?? "lessons/";
      const href = (article: Article) => (anchor ? `#${id(article)}` : `${src}${escape(article.slug)}.html`);
      // <li value> keeps each lesson's number in the message, also in a selection.
      const list = (articles: Article[]) =>
        `<ol>\n${articles.map((a) => `<li value="${a.number}"><a href="${href(a)}">${escape(a.title)}</a></li>`).join("\n")}\n</ol>`;
      const groups = this.groups();
      if (!groups) return list(this.selected());
      const items = groups.map((group) => {
        const target = anchor ? `#${group.id}` : `topics.html#${group.topic.name}`;
        return `<li><a href="${target}">${escape(group.topic.title)}</a>\n${list(group.articles)}</li>`;
      });
      return `<ul>\n${items.join("\n")}\n</ul>`;
    }

    articles(): string {
      const views = (this.getAttribute("views") ?? "symbols math chunks bits")
        .split(/\s+/)
        .filter((view): view is View => (VIEWS as readonly string[]).includes(view));
      const groups = this.groups();
      if (!groups) return this.selected().map((article) => this.article(article, views)).join("\n\n");
      return groups
        .map((group) => {
          const intro = group.first && group.topic.intro ? `\n${group.topic.intro}` : "";
          const articles = group.articles.map((article) => this.article(article, views)).join("\n\n");
          return `<section id="${group.id}" data-topic="${group.topic.name}">\n<h2>${escape(group.topic.title)}</h2>${intro}\n\n${articles}\n</section>`;
        })
        .join("\n\n");
    }

    // The article as written, with its id and the generated views added.
    article(article: Article, views: View[]): string {
      const source = new window.DOMParser().parseFromString(article.source, "text/html") as unknown as Document;
      const element = findArticle(source, article.slug);
      element.id = id(article);
      enrichArticle(element, article, views, { registry: context.registry, usage: context.usage, base: "" });
      return element.outerHTML;
    }
  }

  window.customElements.define("cl-lessons", ClLessons as never);
}
