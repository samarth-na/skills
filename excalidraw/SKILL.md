---
name: excalidraw
description: Use Excalidraw as a visual output medium. Write or edit .excalidraw scenes, generate an editable HTML preview, and show it in the desktop browser. Use for Excalidraw files, boards, diagrams, visual explanations, and editor feature questions. Save board artifacts under ~/.opencode/excalidraw. Load this before generating or changing .excalidraw content.
metadata:
  opencode/autoinvoke: "true"
---

# Excalidraw

Use the board as another way to explain, compare, teach, and present information.
Speed is the priority: write `.excalidraw` → generate editable `.html` → render.
The `.excalidraw` JSON file is the source of truth. Ordinary boards need no npm packages or custom runner.

The examples are a starting point, not a ceiling. Use the feature references when the task needs more.

## Default workflow (fast path)

1. Read the source material or the existing scene.
2. Write the scene to `~/.opencode/excalidraw/<slug>.excalidraw`. Create the directory with `mkdir -p ~/.opencode/excalidraw` if needed. Keep one canonical file per board. Match its size to the explanation.
3. Generate the editable preview with one stdlib-only command:
   `python3 <skill-dir>/scripts/make-preview.py ~/.opencode/excalidraw/<slug>.excalidraw` This writes `<slug>.html` beside the scene using [assets/viewer.html](./assets/viewer.html). Building needs no network; viewing needs network access for the CDN-hosted editor.
4. Show the local `.html` with `tools.browser.preview` through the `execute` tool. Use the absolute file path. The user can edit the board in that preview.

Do not run a separate `--check` before the build. The build already checks structure and reports layout warnings.
Show the first useful board immediately. Fix obvious problems when visible, not through a mandatory screenshot or zero-warning loop.

Read only the reference needed for the current feature. Use a short stdlib script for repeated elements when helpful.
Do not install packages, probe imports, or build a rendering pipeline for ordinary boards.
If previewing fails, provide the scene and generated HTML paths, if available. State the limitation without rebuilding tools.

## Copy-ready scene

This is complete scene JSON, not a skeleton that needs conversion. Copy element fields and assign unique IDs for new elements.

```json
{
  "type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
  "appState": { "viewBackgroundColor": "#ffffff" }, "files": {},
  "elements": [
    {
      "id": "box", "type": "rectangle", "x": 0, "y": 0, "width": 200, "height": 100,
      "angle": 0, "strokeColor": "#1e1e1e", "backgroundColor": "#a5d8ff", "fillStyle": "solid",
      "strokeWidth": 2, "strokeStyle": "solid", "roughness": 1, "opacity": 100,
      "seed": 1, "version": 1, "versionNonce": 1, "index": null, "isDeleted": false,
      "groupIds": [], "frameId": null, "boundElements": [{ "id": "label", "type": "text" }],
      "updated": 1, "link": null, "locked": false, "roundness": { "type": 3 }
    },
    {
      "id": "label", "type": "text", "x": 65, "y": 37.5, "width": 70, "height": 25,
      "angle": 0, "strokeColor": "#1e1e1e", "backgroundColor": "transparent", "fillStyle": "solid",
      "strokeWidth": 1, "strokeStyle": "solid", "roughness": 1, "opacity": 100,
      "seed": 2, "version": 1, "versionNonce": 2, "index": null, "isDeleted": false,
      "groupIds": [], "frameId": null, "boundElements": null,
      "updated": 1, "link": null, "locked": false, "roundness": null,
      "text": "Start", "originalText": "Start", "fontSize": 20, "fontFamily": 5,
      "textAlign": "center", "verticalAlign": "middle", "containerId": "box",
      "autoResize": false, "lineHeight": 1.25
    }
  ]
}
```

- For free text, set `containerId: null`, `autoResize: true`, and position it directly.
- Keep labels short. Use explicit line breaks and generous containers. Text height is `lineCount × fontSize × lineHeight`.
- Character-count width estimates are approximate. Use the rendered view to decide whether text fits.
- Use consistent spacing, one reading direction, and a small color palette. Keep connectors clear of labels.
- Change `rectangle` to `ellipse` or `diamond` for those shapes. Their labels need more interior space.
- Arrows store local `points`, such as `[[0, 0], [100, 0]]`. A horizontal arrow legitimately has height `0`.
- Bound labels and arrows need references in both directions. Frame children store the frame's ID in `frameId`.
- Images need an element `fileId` and a matching data URL entry in `files`.
- For arrow, image, and frame examples, read only the relevant section of [element-templates.md](./references/element-templates.md).

## Show and update the board

Save all board artifacts under `~/.opencode/excalidraw/`, including revisions and any requested supplemental exports.
`<slug>.excalidraw` is canonical; `<slug>.html` is the editable preview. Do not place board previews in `~/.opencode/html/`.
That directory is for standalone HTML documents, not Excalidraw boards.

Build the preview with `scripts/make-preview.py` (it escapes `<` as `\u003c` and sets the title). Treat the `.html` as disposable output. Keep IDs stable and preserve the user's layout. Do not regenerate the whole board for a small change.

Present the `.html` file in the desktop Review pane. Do not start a server for it.

The local viewer also exposes `window.excalidrawViewer.load(scene, label)` after the editor is ready.
This loads the scene into memory. It does not save to disk or attach a file handle.
Use **Save as** once to choose the canonical `.excalidraw` file.
If the browser downloads instead of writing in place, replace the canonical file with the download before agent edits resume.
After a user edit, save and re-read the canonical file before patching it.
The viewer does not watch the file. Rebuild the preview after agent edits and re-preview it.

## Protect existing work

- Banned outright: opening, driving, importing into, or saving from `https://excalidraw.com` with any agent tool. That site holds the user's personal work in its own storage. Agent work lives only in `~/.opencode/excalidraw/` plus its generated preview. No exceptions, no workarounds via share links or automation.
- Do not automate the user's canvas with coordinate clicks or import an agent scene into their existing browser tab.
- Never read or write another board's `localStorage` or IndexedDB. Do not back up or restore another origin's storage.
- Agent edits go into scene JSON. Use an editor API only for a task that specifically needs it in an isolated local runtime.
- Deliver the scene and editable HTML by default. Static exports are optional when requested, not a replacement for the board.

For teaching, draw the first useful explanation immediately. Add one concept or worked example per turn on the same board.
Keep IDs stable and preserve the user's layout. Do not regenerate the whole board for a small change.
When the user chooses the board as the session canvas, put explanations there and use chat for brief coordination and direct answers.

## Optional checks

Normal builds stop on structural errors but still generate HTML when layout warnings exist.
Warnings are approximate. Use the visible board to decide whether spacing or text needs adjustment.

Use `make-preview.py --check` only for diagnosis or when a check is requested.
It writes nothing. Exit 0 means no reported problems; exit 1 means structural errors or layout warnings.
Neither mode proves that text fits. If rendering is unavailable, leave extra space and state that layout is visually unverified.

## Features beyond the starter scene

Use shapes, free text, bound labels, arrows, groups, frames, images, links, and styling to suit the explanation.
The editor also supports libraries, embeds, diagram conversion, and export options. Read the relevant reference before using an unfamiliar field or API.
Feature availability depends on the editor version and runtime. Do not treat the simple example as the full feature set.

| Need | Read only this reference |
| --- | --- |
| Unfamiliar element fields or bindings | [scene-format.md](./references/scene-format.md) |
| Text sizing problem | [text-sizing.md](./references/text-sizing.md) |
| Existing app already uses the package; React integration; Mermaid conversion | [skeleton-api.md](./references/skeleton-api.md) |
| Safe local rendering and browser boundaries | [browser-control.md](./references/browser-control.md) |
| Editor feature or shortcut question | [editor-features.md](./references/editor-features.md), [keyboard-shortcuts.md](./references/keyboard-shortcuts.md) |
| Persistence, export options, or embedding the editor | [appstate-and-export.md](./references/appstate-and-export.md) |
| Long-lived session notes | [communication-canvas.md](./references/communication-canvas.md) |

The package is browser-first. Use its API inside an existing browser/app runtime, not a plain Node import.
Use direct JSON for ordinary elements. Let the editor route elbow arrows unless the task needs a version-matched advanced API.
