// <cl-lessons>: lists the articles of lessons/ as links, or includes them as articles.
// The element is replaced by what it renders.
//
//   as      links | articles          (default links)
//   href    file | anchor             (links; default file)
//   select  all | parts | lessons     (links; default all)
//   src     directory of the pages    (links with href="file"; default lessons/)
//   views   generated views to add    (articles; default "symbols chunks bits", "" for none)
import type { Window } from "happy-dom";
import { escape } from "../dom.ts";
import { anchor as id, findArticle, groupByPart, type Article } from "../lessons.ts";
import type { Registry } from "../registry.ts";
import { addViews, VIEWS, type View } from "../views.ts";

export interface Context {
  articles: Article[];
  registry: Registry;
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

    links(): string {
      const select = this.getAttribute("select") ?? "all";
      const anchor = this.getAttribute("href") === "anchor";
      const src = this.getAttribute("src") ?? "lessons/";
      const link = (article: Article) =>
        `<a href="${anchor ? `#${id(article)}` : `${src}${escape(article.slug)}.html`}">${escape(article.title)}</a>`;
      const list = (articles: Article[], start?: number) =>
        `<ol${start && start > 1 ? ` start="${start}"` : ""}>\n${articles.map((a) => `<li>${link(a)}</li>`).join("\n")}\n</ol>`;
      if (select === "parts") return list(context.articles.filter((a) => a.kind === "part"));
      if (select === "lessons") return list(context.articles.filter((a) => a.kind === "lesson"));
      const items = groupByPart(context.articles).map(({ part, lessons }) => {
        const nested = lessons.length ? "\n" + list(lessons, lessons[0].number) : "";
        return part ? `<li>${link(part)}${nested}</li>` : `<li>${nested}</li>`;
      });
      return `<ol>\n${items.join("\n")}\n</ol>`;
    }

    articles(): string {
      const views = (this.getAttribute("views") ?? "symbols chunks bits")
        .split(/\s+/)
        .filter((view): view is View => (VIEWS as readonly string[]).includes(view));
      return groupByPart(context.articles)
        .map(({ part, lessons }) => {
          const articles = [...(part ? [part] : []), ...lessons].map((article) => this.article(article, views));
          return `<section>\n${articles.join("\n\n")}\n</section>`;
        })
        .join("\n\n");
    }

    // The article as written, with its id and the generated views added.
    article(article: Article, views: View[]): string {
      const source = new window.DOMParser().parseFromString(article.source, "text/html") as unknown as Document;
      const element = findArticle(source, article.slug);
      element.id = id(article);
      addViews(element, context.registry, views, article.slug);
      return element.outerHTML;
    }
  }

  window.customElements.define("cl-lessons", ClLessons as never);
}
