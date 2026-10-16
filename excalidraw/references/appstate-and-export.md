# App state and scene persistence

Boards persist as `.excalidraw` scene JSON plus the generated interactive `.html` preview. Static image exports (SVG, PNG) are banned outputs for this skill: never produce, preview, attach, or screenshot them. If a static image is requested, deliver the interactive board instead and say static exports are out of scope.

## App state

`AppState` is large. Most of it is local UI state (selection, dialogs, scroll). On export, `cleanAppStateForExport` keeps only these keys:

| Key | Meaning |
| --- | --- |
| `viewBackgroundColor` | Canvas background color, e.g. `"#ffffff"`. |
| `gridModeEnabled` | Whether the grid shows. |
| `gridSize` | Grid cell size in px, or `null`. |
| `gridStep` | Grid step. |

So a `.excalidraw` file never persists selection, zoom, or scroll. Do not rely on them.

### App-state keys used by export

Pass these inside `appState` to the export functions:

| Key | Default | Effect |
| --- | --- | --- |
| `exportBackground` | `true` | Include the background color. |
| `viewBackgroundColor` | `"#fff"` | Background color used when `exportBackground` is true. |
| `exportWithDarkMode` | `false` | Render with the dark theme. |
| `exportEmbedScene` | `false` | Embed the scene JSON inside the SVG or PNG (larger file, round-trippable). |
| `exportScale` | `1` | Raster scale for PNG. `EXPORT_SCALES` lists the UI choices. |

For the public export functions, pass `exportPadding` as a top-level option, not inside `appState`. Its default is `10` pixels.
When importing a scene for editing, use `appState` for the background and grid settings.

## Serialize and restore

```js
import { serializeAsJSON, restore, restoreElements } from "@excalidraw/excalidraw";

const json = serializeAsJSON(elements, { viewBackgroundColor: "#ffffff" }, {}, "local");
const elements2 = restoreElements(JSON.parse(json).elements, null);
```

- `serializeAsJSON(elements, appState, files, "local")` returns the `.excalidraw` JSON string. Use `"local"` for a file, `"database"` for server persistence.
- `restore` / `restoreElements` normalize scenes in a package runtime: fill defaults, upgrade old schema, and drop some invalid elements. They are not validators.
- `loadFromBlob`, `loadSceneOrLibraryFromBlob`, and `isValidExcalidrawData` handle files and validation in the browser.

## Rendering: the only supported path

Write the scene file, build the preview with `../scripts/make-preview.py`, and present the `.html` preview with `tools.browser.preview`. There is no supported image-export path in this skill.

## Embedding the editor in an app

```jsx
import { Excalidraw, convertToExcalidrawElements } from "@excalidraw/excalidraw";
import "@excalidraw/excalidraw/index.css"; // or the package CSS path in your bundler

function App() {
  const [api, setApi] = useState(null);
  const elements = convertToExcalidrawElements([{ type: "rectangle", x: 0, y: 0 }]);
  return (
    <div style={{ height: 640 }}>
      <Excalidraw initialData={{ elements }} excalidrawAPI={setApi} />
    </div>
  );
}
```

The component needs a parent with a fixed height. Use the imperative API for automation:

| Method | Use |
| --- | --- |
| `getSceneElements()` | Read visible elements. |
| `updateScene({ elements, appState })` | Replace scene contents. |
| `getAppState()` / `getFiles()` | Read state and binary files. |
| `scrollToContent(target?, opts?)` | Fit or center content. |
| `history.clear()` | Clear undo history. |
| `setActiveTool({ type })` | Switch tools programmatically. |
| `addFiles([...])` | Add binary files (images). |

`Ref` support was removed in v0.17.0. Use `excalidrawAPI`.

`index.css` (or `index.scss`) must be loaded for the editor to look correct.
