---
name: html
description: Generate self-contained single-file HTML documents and pages — reports, summaries, dashboards, style guides, slide decks, notes, explainers with diagrams, landing pages, resumes, printables, any single HTML file. Use when asked to create, write, summarize, explain, or present anything as an HTML file; when the user mentions @html, "html file", "single file page", "one file that opens anywhere", or "shareable document"; or when output must work offline with no build step and no external requests. Do not use for Markdown output, PDFs, or component frameworks like React or Vue.
metadata:
  opencode/autoinvoke: "true"
---

# HTML documents and pages

## What you produce

One self-contained `.html` file. Save every delivered file to
`~/.opencode/html/<slug>.html`, including revisions. Create the directory with
`mkdir -p ~/.opencode/html` if needed. Do not scatter output across the repo,
Desktop, or temporary directories.

The file opens from disk and works offline. Embed CSS, JavaScript, images, and
diagrams. Use no external assets, network requests, build step, or package installs.

This skill supplies a standard stylesheet and simple output rules. The component
catalog is a starting point, not a limit on what the agent can represent.

## Fast path: write → show → iterate

1. Read the source and `components/shell.html`.
2. Read only the components needed for the content.
3. Write the file with a stylesheet placeholder.
4. Replace the placeholder with `styles/base.css` verbatim. Add a skin if useful.
5. Show the file with `tools.browser.preview` through the `execute` tool.

Write the useful document first. Do not turn a simple page into a validation project.
Fix visible problems when they appear. Revise the same file unless a separate version is requested.

## Compose and extend

- Reuse component markup when it fits. Preserve existing `c-` classes so the stylesheet still applies.
- Compose layouts with `.c-wrap`, `.c-section`, `.c-stack`, `.c-grid`, `.c-split`, `.c-rail`, and `.c-card`.
- Add markup, CSS, inline SVG, or vanilla JavaScript when the catalog does not cover the task.
- Prefer the `--c-*` tokens for custom styling. Keep overrides after the standard stylesheet.
- Use custom properties for routine tuning, such as `style="--v: 62%"` on a bar fill.

There is no custom-code line limit. Keep extensions as simple as the task permits.
Do not edit the skill or add a shared component just to finish one document.

## Stylesheets: swappable design languages

| File | Role |
| --- | --- |
| `styles/base.css` | Complete default design language. Marker: `/* html-skill: standalone */`. |
| `styles/editorial.css` | Skin: warm paper, serif reading. Marker: `/* html-skill: skin */`. |

Rules:

- Paste the chosen stylesheet verbatim between `<style>` tags in `<head>`.
  Put document-specific overrides after it instead of editing the pasted copy.
- A **standalone** stylesheet is used alone. A **skin** is pasted after
  `base.css` — skins override tokens and selective rules only; markup stays
  identical.
- Switching a skin should not require markup changes. Extensions can add their own markup and classes.
- To add a design language: copy `styles/editorial.css`, override tokens first
  (`--c-bg`, `--c-ink`, `--c-accent`, `--c-font-*`, `--c-radius-*`, `--c-measure`),
  then fix whatever surfaces still look wrong. Give it the `skin` marker unless
  it truly replaces every rule, then `standalone`.

## Document anatomy

Start from `components/shell.html`. Follow these output rules:

- exactly one `<h1>`, and it matches the `<title>`;
- `<title>` and `<meta name="description">` state what the document is;
- `<meta name="color-scheme" content="light dark">` and the pre-paint theme
  script in `<head>` — before first paint, or the page flickers;
- skip link to `<main id="main">`;
- sections are `<section class="c-section" id="…">`; ids are stable and human;
- a TOC (`components/navigation.html`) when it helps navigation, with every link target present;
- theme toggle button and footer, unless the format is a print-only handout.

## Content rules

- Heading levels carry structure. Never pick a level for its size.
- For long documents, give each `h2`/`h3` an anchor link (`.c-hlink`).
- Prose follows the user's writing preferences. Plain, direct, one idea per
  paragraph. Remove filler and promotional adjectives.
- Escape `<`, `>`, `&` inside every `<pre>`.
- Tables need `<thead>`, and numbers right-align with `.c-num`.
- Every `<img>` has `alt`. Evidence images get a `.c-figure` caption.
- Filename: short, descriptive, hyphenated — `production-finalization.html`,
  `commits-2026-09-22.html`, `api-settings-explainer.html`.

## JavaScript

Reuse the component blocks for theme, print, copy, navigation, dialogs, filters,
tabs, and motion. Include only the features the document uses.

Custom vanilla JavaScript is allowed. Keep it inline and offline. Do not add
frameworks or fetch data. Essential content must remain readable without JavaScript.

## Motion and accessibility

- `prefers-reduced-motion` is honored by `base.css`; JS that animates must
  check it too (the counter block shows the pattern).
- Landmarks (`header`, `nav`, `main`, `footer`) and `aria-label` on every `nav`.
- Focus states come from the stylesheet; never remove outlines.
- Design mobile-first. At 360px width the page has no horizontal scrollbar.
  Only `.c-table-wrap`, code blocks, diffs, terminals, and `.c-tabs-nav` may
  scroll internally (`overflow-x: auto` comes from the stylesheet).
- Popups (`.c-drop-body`, mini-rail TOC, tooltips) stay within
  `calc(100vw - 2rem)`. Touch targets are at least 24px in each dimension.
- Wrap every `<table>` in `.c-table-wrap`. Prefer plain `.c-grid` (auto-fit)
  unless fixed columns are required.

## Diagrams

Embed SVG inline in a `.c-shot` frame (`components/media.html`) or as a
`data:image/svg+xml;base64,` URI. Use `data:image/png;base64,` for PNG images.
Do not link separate image files.

## Lightweight review

Show the file once. Correct obvious layout or content problems. Do not run a
checker, screenshot matrix, or repeated audit by default. Use targeted checks
when the user asks or a specific problem needs diagnosis.

`python3 <skill-dir>/scripts/check.py FILE.html` is an optional diagnostic for
markup, classes, headings, anchors, code escaping, and some asset references.
It is not a delivery gate or proof of offline behavior or accessibility.

Keep secrets and private information out unless the user explicitly requests their inclusion.
If the preview cannot open, provide the file path and state that rendering was not verified.

## Files

| Path | Contents |
| --- | --- |
| `styles/base.css` | Canonical stylesheet: tokens, theme, reset, all components. |
| `styles/editorial.css` | Skin: serif, warm paper. |
| `components/shell.html` | Skeleton, header, footer, theme, print. |
| `components/layout.html` | Containers, grids, regions, cards. |
| `components/reading.html` | Headings, prose, quotes, callouts, verdicts, footnotes. |
| `components/evidence.html` | Code blocks, diffs, terminals, chips, copy JS. |
| `components/data.html` | Tables, stats, bars, meters, timelines, comparisons. |
| `components/navigation.html` | TOC, rail, crumbs, pager, scroll-spy JS. |
| `components/interaction.html` | Accordion, dialog, tooltip, dropdown, filter, tabs. |
| `components/forms.html` | Fields, choices, buttons, validation states. |
| `components/media.html` | Figures, screenshots, diagrams, embeds. |
| `components/motion.html` | Reveals, counters, marquee, slide decks. |
| `specimen.html` | Every component rendered — the visual reference. |
| `scripts/check.py` | Optional markup diagnostic. |
