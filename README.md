# Cosmic Language

*"We come in peace"* – in the Cosmic Language.

A message that explains itself: it starts from bare bits and builds up, one lesson at a time, through mathematics
and physics, so that a receiver who shares nothing with us but math, logic and physics can read it.

**Read it at <https://narve.github.io/cosmic-language/>.**

## Intro

I've always been fascinated by aliens, and how to communicate with them. This is my attempt to build a
self-describing message, starting from scratch, with no shared assumptions.

There are several versions of the message:

- A [minimal](https://narve.github.io/cosmic-language/minimal/) version, trying only to say "We come in peace".
- A [full](https://narve.github.io/cosmic-language/full/) version, explaining more advanced math, physics and
  chemistry, and using that to describe and place the Sun, the Earth and the humans.
- A ["cautious"](https://narve.github.io/cosmic-language/cautious/) version, explaining more advanced math, physics
  and chemistry, but leaving out anything that can link this message to us. (Dark forest!)
- A [decoy](https://narve.github.io/cosmic-language/decoy/) version, similar to the full version but swapping the
  actual truth with a hopefully plausible alternative civilization, living on another star (Kepler-1647, a pair of
  stars 1.2 kpc away).

The decoy version is also used to test whether the most alien intelligences we have access to, modern LLMs, can
understand the message without any instructions. See the
[blind test](https://narve.github.io/cosmic-language/blind-tests.html). (Spoiler: they can!)

The message is presented as a set of annotated, reader-friendly HTML pages, with options to show the message both as
the "source" (the way *we* write it) and as the bits that are actually sent.

If you just want to read the message, start with the
[minimal version](https://narve.github.io/cosmic-language/minimal/). It is a bit heavy on math and logic. After that,
go to the [full version](https://narve.github.io/cosmic-language/full/) for the advanced math, physics, chemistry,
astronomy, and finally the Sun, the Earth and the humans.

## A very high level description

The message starts with a list of prime numbers (including 1!), to make it clear that this is an artificial message,
not noise. This is in unary notation, just runs of 1s: `01011011101111101111111` …

Then the prime numbers are repeated, this time in the standard binary notation used throughout the message.

The notation uses [S-expressions](https://en.wikipedia.org/wiki/S-expression), like Lisp, and initially uses math to
define various terms. On top of these operators it introduces actors, strategies, morals and the prisoner's dilemma,
so that it can finally say: *We come in peace.*

## Documents

- [Specification](https://narve.github.io/cosmic-language/specification.html): the exact rules of the format.
- [Vocabulary](https://narve.github.io/cosmic-language/vocabulary.html): every type and symbol, with its meaning, the
  lesson that introduces it and the lessons that use it.
- [Versions](https://narve.github.io/cosmic-language/versions.html): the four versions and their message files.
- [Topics](https://narve.github.io/cosmic-language/topics.html): the lessons grouped by topic.
- [Previous work](https://narve.github.io/cosmic-language/previous-work.html): earlier messages to the stars and what
  we learn from them.
- [Twenty aliens](https://narve.github.io/cosmic-language/aliens.html): readers imagined by fiction, and what the
  message would mean to each.
- [Blind test](https://narve.github.io/cosmic-language/blind-tests.html): what a reader made of the message when it
  got nothing but the bits.

## Building

Requires Node.js 22.18 or later.

```sh
npm ci
npm run build
```

The build reads the sources in `site/` and `vocabulary/`, deletes `docs/` and makes it again: the pages, one page per
version, and the message files (`message.txt`, `message.bits`, `message.bin`, and the same per version in
`docs/cautious/`, `docs/minimal/` and `docs/decoy/`). Open `docs/index.html` in a browser to read the result.

`docs/` holds only generated files and is not committed. On every push and pull request,
`.github/workflows/docs.yml` runs the build; on `main` it publishes `docs/` to GitHub Pages.

### Layout

| Path | What it holds |
|------|---------------|
| `site/*.html` | The pages (`index`, `topics`, `specification`, `previous-work`, `blind-tests`, `versions`, `decoy`, `aliens`, `vocabulary`). Plain HTML plus custom elements such as `<cl-lessons>`, `<cl-files>` and `<cl-vocabulary>`, rendered by the build. |
| `site/lessons/` | One HTML file per lesson, ordered by file name (`090-equal-and-not-equal.html`, numbers in steps of 10). The file order is the order of the message. |
| `site/assets/` | `style.css`, `views.js` and `favicon.svg`. |
| `vocabulary/` | The master list of every token type and symbol (TypeScript): `types.ts`, one file per type of symbol, `decoy.ts` (the decoy's own symbols, which send the ids of the full message's symbols they stand in for) and `index.ts`. The build's registry and the specification's tables (§6, §9) are made from it. |
| `build/` | The build (TypeScript, run with `tsx`, DOM via happy-dom). `build/build.ts` is the entry point; `build/components/` renders the custom elements. |
| `build/check/` | The checks run by the build, and the reference data they use. |
| `build/lisp/` | A small interpreter (`evaluate.ts`) and a renderer to mathematical notation (`display.ts`). |

`site/` is laid out exactly like `docs/`, so relative links work both when a source file is opened in a browser and
on the generated site (links to generated files, such as `message.txt`, work only in `docs/`).

There is no source file per version: the build makes `docs/full/`, `docs/cautious/`, `docs/minimal/` and
`docs/decoy/` from the lessons and the sections of `site/versions.html`. The versions are made by leaving out whole
lessons:

- **full**: every lesson (`docs/message.*`);
- **cautious**: everything except the lessons marked `data-optional` (the Sun, the Galaxy, pulsars, the
  chemistry of life, humans);
- **minimal**: the lessons with the topic `minimal` (the signal, the mathematics and the prisoner's dilemma);
- **decoy**: the full message with each lesson marked `data-replaces="slug"` swapped in for the lesson it replaces,
  and the lessons marked `data-not-in-decoy` (none today) left out. Replacing lessons may use the decoy's own symbols
  (`vocabulary/decoy.ts`), listed on the decoy page.

On the generated pages, the build adds ids, syntax markup, a "New in this lesson" list, links to the vocabulary, and
after each message block the symbols, chunks and bits views. It never changes what a lesson says.

### Checks

The build stops when the message cannot be encoded (an unknown symbol, a number above 255, unbalanced brackets, a
name or sign used twice) or breaks a rule of the specification. The checks are separate checkers in
`build/check/checkers.ts`:

- **structure**: a group starts with an operator and has the arity the registry gives; every variable is bound;
  every symbol of the version is used; decoy symbols appear only in replacing lessons, and no version sends one type
  and id under two names; a new symbol appears in at least 3 sentences of the lesson that introduces it (spec §10.1);
- **id-order**: in every version, the ids of each type first appear as 1, 2, 3 … with none missing;
- **minimal**: a minimal lesson uses only symbols that minimal lessons introduce;
- **optional**: no lesson uses a symbol that an optional lesson introduces;
- **self-reference**: what each version says about itself (such as the size of the message) holds for that version;
- **new-symbols**: a "New …" clause in a lesson's prose names only symbols that the lesson introduces;
- **measurements**: every `observed` range is checked against reference data; each bound must be at least 5 standard
  uncertainties from the value (also for the decoy, against its own values);
- **evaluate**: every sentence the interpreter can compute (exact fractions, finite lists) must be true and none may
  divide by zero, in the full and the decoy version; the rest is counted as not computable.

Run only some checks, or leave some out:

```sh
CHECKS=structure,evaluate npm run build
SKIP_CHECKS=measurements npm run build
```

### Other scripts

| Command | What it does |
|---------|--------------|
| `npm run watch` | Reruns the build when any file in `site/` changes. It polls every 500 ms, because file events do not reliably cross a virtiofs mount. A failed build is reported and the watcher goes on. |
| `npm run check:measurements` | Prints the margin of every measured range. |
| `npm run reference` | Makes `build/check/reference/generated/reference.json` from the downloaded sources and `transcribed.json`. |
| `npm run --silent blind [task]` | A blind-decoding run: a headless `claude` that gets only the bits, in a container without network. See `build/check/blind/run.sh` for the options. Run `npm run build` first. |

### Reference data

`build/check/reference/` holds no code:

- `sources/`: the downloaded reference sources (CODATA 2022, NUBASE2020, AME2020, BIPM, NASA, ATNF, PDG and others),
  never edited;
- `transcribed.json`: values read by hand from PDFs;
- `generated/`: `reference.json` (from `npm run reference`) and `cmb-quadrupole.json` (from
  `build/check/cmb-quadrupole.py`, made from three full-sky maps too large to keep).

Every source is listed in full in §8.4 of the specification.

## Contributing

Comments, bugs, corrections, ideas: please create issues, forks and pull requests on
[GitHub](https://github.com/narve/cosmic-language). Run `npm run build` before sending a change; it must pass.

## Disclaimers

- There are several build-time checks and verifications, but there can definitely be errors, especially in the
  physics part.
- The idea and much of the "source code" of the message is mine. But AI has been used extensively, and much of the
  prose shows that – deal with it :)
- I am not the first to have this idea! Ideas and inspiration came from many places – see
  [previous work](https://narve.github.io/cosmic-language/previous-work.html) for background.
