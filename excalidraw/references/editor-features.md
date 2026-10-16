# Excalidraw editor features

A map of what the Excalidraw editor can do. Use it to answer "can Excalidraw do X?" and to know which names the UI and the data model use. Pinned to `@excalidraw/excalidraw` 0.18.x unless a note says otherwise. Verify current UI labels against <https://docs.excalidraw.com> and the in-app help (`?`).

## Canvas and navigation

| Feature | Notes |
| --- | --- |
| Pan | Hold `Space` and drag, middle-mouse drag, or the hand tool (`H`). |
| Zoom | `CtrlOrCmd++` / `CtrlOrCmd+-`, `CtrlOrCmd+0` to reset. Wheel and trackpad gestures also work. Zoom range is 10% to 3000% (`MIN_ZOOM`, `MAX_ZOOM`). |
| Zoom to fit | `Shift+1` (all), `Shift+2` (fit selection in viewport), `Shift+3` (fit selection). |
| Zen mode | `Alt+Z`. Hides the UI chrome. `appState.zenModeEnabled`. |
| View mode | `Alt+R`. Read-only canvas for presenting. `appState.viewModeEnabled`. |
| Grid | `CtrlOrCmd+'`. `appState.gridModeEnabled`, `gridSize`, `gridStep`. |
| Snap to objects | `Alt+S`. `appState.objectsSnapModeEnabled`. |
| Theme | Light or dark. `Shift+Alt+D`. `appState.theme` is `"light"` or `"dark"`. |
| Canvas background | Set through the canvas background picker. `appState.viewBackgroundColor`. |
| Stats for nerds | `Alt+/`. Element counts and properties. `appState.stats`. |

## Tools

The tool set is `TOOL_TYPE`: `selection`, `rectangle`, `diamond`, `ellipse`, `arrow`, `line`, `freedraw`, `text`, `image`, `eraser`, `hand`, `frame`, `magicframe`, `embeddable`, `laser`.

| Tool | Key | Notes |
| --- | --- | --- |
| Selection | `V` / `1` | Move, resize, rotate, and edit elements. |
| Rectangle | `R` / `2` | |
| Diamond | `D` / `3` | |
| Ellipse | `O` / `4` | |
| Arrow | `A` / `5` | Binds to shapes. See Arrows below. |
| Line | `L` / `6` | Multi-point line. |
| Draw (freehand) | `P` / `7` | Pressure-sensitive freehand. `freedraw` elements. |
| Text | `T` / `8` | Free text and labels. |
| Image | `9` | Insert an image file. |
| Eraser | `E` / `0` | Delete elements by touch. |
| Frame | `F` | Group elements into a named frame. |
| Hand | `H` | Pan without drawing. |
| Laser pointer | `K` | Transient pointer trail for presentations. |
| Eyedropper ("pick color") | `I` | Pick a color from the canvas. |
| Web embed | tool button | Add a generic embeddable or iframe. |

Tool lock: press `Q` to keep the active tool after drawing. `appState.activeTool.locked`.

## Shape properties

| Property | Options | Element field |
| --- | --- | --- |
| Stroke color | Palette plus custom. | `strokeColor` |
| Background color | Palette plus custom, or transparent. | `backgroundColor` |
| Fill | Hachure, cross-hatch, solid, zigzag. | `fillStyle` |
| Stroke width | Thin (1), bold (2), extra bold (4). | `strokeWidth` |
| Stroke style | Solid, dashed, dotted. | `strokeStyle` |
| Sloppiness | Architect (0), artist (1), cartoonist (2). | `roughness` |
| Edges | Round or sharp. | `roundness` |
| Opacity | 0–100. | `opacity` |
| Arrowheads | arrow, bar, dot, circle, circle_outline, triangle, triangle_outline, diamond, diamond_outline, crowfoot variants, or none. | `startArrowhead`, `endArrowhead` |

Per-element properties persist in the file. See [scene-format.md](./scene-format.md).

## Text

- Fonts shipped: Virgil (1), Helvetica (2), Cascadia (3), Excalifont (5), Nunito (6), Lilita One (7), Comic Shanns (8), Liberation Sans (9). `FONT_FAMILY`. Value 4 is unused.
- Font size, text align (`left`, `center`, `right`), and vertical align (`top`, `middle`, `bottom`).
- Double-click a shape to add or edit a label. A label is a bound text element inside a container.
- Text wraps inside a container; free text auto-resizes.
- Line height and autowrap are element fields, not direct UI toggles.

## Arrows and lines

- **Binding**: an arrow endpoint snaps to a shape and stays attached when the shape moves. Both sides store the reference (`startBinding`/`endBinding` and `boundElements`).
- **Arrowheads**: independent start and end arrowheads, including crowfoot notation for ER diagrams.
- **Elbow arrows**: right-angle routing. `arrow.elbowed`, with `fixedSegments`.
- **Labeled arrows**: double-click an arrow to add a text label.
- **Multi-point lines**: click to add points, `CtrlOrCmd+Enter` to finish editing.

## Editing operations

| Operation | Shortcut | Notes |
| --- | --- | --- |
| Multi-select | `Shift`+click, or drag a marquee | |
| Select all | `CtrlOrCmd+A` | |
| Deep select | `CtrlOrCmd`+click | Select inside a group. |
| Group / ungroup | `CtrlOrCmd+G` / `CtrlOrCmd+Shift+G` | `groupIds` on elements. |
| Align | `CtrlOrCmd+Shift+Arrow` | Aligns selected elements. |
| Distribute | context menu | Even spacing for three or more elements. |
| Order | `CtrlOrCmd+[` / `]` (and `Shift`/macOS `Alt` variants) | Z-order. Array order in the file. |
| Lock / unlock | `CtrlOrCmd+Shift+L` | `locked`. |
| Duplicate | `CtrlOrCmd+D` or `Alt`+drag | |
| Flip | `Shift+H` / `Shift+V` | Horizontal / vertical. |
| Delete | `Delete` | Soft-delete via `isDeleted`. |
| Undo / redo | `CtrlOrCmd+Z` / `CtrlOrCmd+Y` | |
| Copy / cut / paste | `CtrlOrCmd+C` / `X` / `V` | Paste as plaintext with `CtrlOrCmd+Shift+V`. |
| Copy styles / paste styles | `CtrlOrCmd+Alt+C` / `CtrlOrCmd+Alt+V` | |
| Copy as PNG | `Shift+Alt+C` | |

## Frames

- A frame is a named container. Move the frame to move its contents.
- `frame` elements have a `name`. Elements inside set `frameId`.
- Frame rendering options: `appState.frameRendering` (`enabled`, `name`, `outline`, `clip`).
- **Magic frame** (`magicframe`) is a newer, related element type. Check the installed version before relying on it.

## Libraries

- Personal library: save reusable elements from the canvas. Shortcut to add has no default binding.
- Install a library from a URL, or import/export `.excalidrawlib` files (`VERSIONS.excalidrawLibrary` = 2).
- Library sidebar: the default sidebar opens the library tab. `updateLibrary` adds items programmatically.
- Public library gallery: <https://libraries.excalidraw.com/>.

## Images

- Insert PNG, JPEG, GIF, WebP, BMP, ICO, AVIF, and SVG.
- Crop an image: select it and use the crop action. `image.crop` and `image.scale`.
- Embedded files live in the scene's `files` map. Very large scenes grow with the images.

## Embeds

- Embed YouTube and Vimeo by pasting a URL onto the canvas.
- Generic web embed / iframe for other URLs. `validateEmbeddable` in the component restricts which URLs are allowed.
- A `renderEmbeddable` prop can replace the default embed rendering.

## Diagrams from text

- **Mermaid to Excalidraw**: paste Mermaid text in the text-to-diagram dialog. Uses `@excalidraw/mermaid-to-excalidraw`.
- **Text to diagram**: generate a diagram from a prompt. This is an AI feature and may need a key or a Plus account. The dialog is `openDialog: { name: "ttd", tab: "text-to-diagram" | "mermaid" }`.

## Search, links, and panels

- **Search in scene**: `CtrlOrCmd+F`. Matches text in elements. `appState.searchMatches`.
- **Command palette**: `CtrlOrCmd+/` or `CtrlOrCmd+Shift+P`. Runs any action by name.
- **Element link**: `CtrlOrCmd+K` links a shape to another element or an external URL. Stored in `element.link`.
- **Stats panel**: `Alt+/`.
- **Laser pointer**: `K`, for live presentations. Color is configurable (`DEFAULT_LASER_COLOR`).

## Export and save

Skill rule: agents never produce static exports. The deliverable is always the `.excalidraw` scene plus its interactive preview. The table below describes what the editor app offers, not what agents may deliver.

| Format | Notes |
| --- | --- |
| PNG | Editor feature only. Banned as an agent deliverable. |
| SVG | Editor feature only. Banned as an agent deliverable. |
| JSON (`.excalidraw`) | The full editable scene. `serializeAsJSON`. |
| Clipboard | Editor feature for the user at the keyboard. |
| `.excalidrawlib` | Library items only. |

Export options: `exportBackground`, `viewBackgroundColor`, `exportWithDarkMode`, `exportEmbedScene` (embed the scene inside the image), `exportScale`, `exportPadding`. See [appstate-and-export.md](./appstate-and-export.md).

Save targets:
- The browser stores the scene in LocalStorage by default (`EditorLocalStorage`).
- **Save to disk** writes a `.excalidraw` file.
- Excalidraw+ saves to a cloud workspace.

## Sharing and collaboration

- **Shareable link**: encrypted end-to-end. The link uses a `#json=<id>,<key>` fragment; the server never sees the drawing.
- **Live collaboration**: real-time multi-user editing in a shared room. `isCollaborating`, `collaborators`.
- **Follow mode**: follow another collaborator's viewport.
- Excalidraw+ adds cloud workspaces, scene management, and search across scenes (`CtrlOrCmd+P` in Plus).

## Interface and appearance

- **Zen mode** and **view mode** for distraction-free or read-only use.
- **Default sidebar** with a library tab; can be docked or floating (`defaultSidebarDockedPreference`).
- **Context menu**: right-click a selection or the canvas for contextual actions, each shown with its shortcut.
- **Welcome screen** and **help dialog**.
- **Mobile / touch**: pinch-zoom, touch drawing, pen support (`penMode`).

## Version notes

- The skeleton docs on `docs.excalidraw.com` currently mention a `stickynote` type. Confirm it exists in installed 0.18.1 before use; it may be newer.
- `magicframe` and the `ttd` text-to-diagram dialog exist in the codebase of 0.18.x. Availability in the hosted free app can differ and may be gated.

## Related references

- Element and file format: [scene-format.md](./scene-format.md)
- Building elements from code: [skeleton-api.md](./skeleton-api.md)
- Export and embedding: [appstate-and-export.md](./appstate-and-export.md)
- Keyboard shortcuts: [keyboard-shortcuts.md](./keyboard-shortcuts.md)
- Browser automation: [browser-control.md](./browser-control.md)