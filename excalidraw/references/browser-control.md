# Driving Excalidraw in a browser

Do not drive Excalidraw with browser automation for ordinary board work. Write the scene file, build the preview with `scripts/make-preview.py`, and present it with `tools.browser.preview`. That path is deterministic and does not depend on pixels.

## The canvas problem

Excalidraw draws the scene on one `<canvas>`. Shapes, text, and arrows are **not** DOM nodes. Accessibility snapshots and CSS selectors cannot see them. Consequences:

- You cannot locate "the red rectangle" with a role or text selector.
- Clicks on shapes are raw coordinates.
- Zoom, scroll, and layout changes move every target.

Excalidraw draws the scene on one `<canvas>`. Shapes, text, and arrows are **not** DOM nodes, so automation clicks are raw coordinates that shift with zoom and scroll. That is why board work stays in the scene file plus the generated preview.

## Forbidden: excalidraw.com and storage tampering

A past session opened `https://excalidraw.com` in the user's visible browser, imported an agent scene into it, and overwrote the user's saved canvas. The backup-restore attempt failed. This must never recur:

- Never navigate any browser to `excalidraw.com` for agent work. No exceptions.
- Never use `browser-control` (or any automation) on an Excalidraw page: no goto, drop, click, snapshot-driven editing, or share-link flow.
- Never read or write `localStorage` keys such as `excalidraw` / `excalidraw-state`, and never touch IndexedDB databases such as `files-db`, on any origin.
- Never mix the two browser systems for one board: the desktop Review pane (`tools.browser.*`) is the only renderer. Do not shuttle scenes through the user's Chromium session.
- If a step would replace, reload, or clear a page holding user content, stop. Backups are not a license for destructive writes.

## The only rendering path

1. Write or edit `~/.opencode/excalidraw/<slug>.excalidraw`.
2. Rebuild with `scripts/make-preview.py`.
3. Present the `.html` preview with `tools.browser.preview`.
4. Change the JSON for the next iteration, never the live page.

There is no supported browser-control flow for Excalidraw boards. Do not enable it for this skill.

Do not attempt headless screenshots of the preview as a QA fallback either: the viewer paints its canvas after page load, so headless captures come back empty. Visual QA happens through the desktop preview, not a headless browser.