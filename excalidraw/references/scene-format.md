# Excalidraw scene format

Reference for the `.excalidraw` JSON file. This is the portable, editable, git-diffable source of truth for any Excalidraw scene. Pinned to `@excalidraw/excalidraw` 0.18.1 unless noted.

## File envelope

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    { "type": "rectangle", "id": "r1", "x": 0, "y": 0, "width": 200, "height": 100, "...": "..." }
  ],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridModeEnabled": false,
    "gridSize": null,
    "gridStep": 5
  },
  "files": {}
}
```

| Key | Required | Value |
| --- | --- | --- |
| `type` | yes | `"excalidraw"`. A library file uses `"excalidrawlib"`. |
| `version` | yes | `2` for scenes and libraries (`VERSIONS.excalidraw`). |
| `source` | yes | URL of the app that wrote the file. Use `https://excalidraw.com` for hand-made scenes. |
| `elements` | yes | Array of elements, in z-order (last is on top). |
| `appState` | yes | Cleaned on export to `viewBackgroundColor`, `gridModeEnabled`, `gridSize`, `gridStep` only. See [appstate-and-export.md](./appstate-and-export.md). |
| `files` | no | Map of `fileId` to binary file data. Empty object when the scene has no images. |

File MIME types: `application/vnd.excalidraw+json` for scenes, `application/vnd.excalidrawlib+json` for libraries.

## Element common properties

Every element has these fields.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Unique. Bindings reference it. |
| `type` | string | See the type table below. |
| `x`, `y` | number | Top-left position in scene coordinates. |
| `width`, `height` | number | Bounding box size. |
| `angle` | number | Rotation in radians, not degrees. |
| `strokeColor` | string | Hex color or `"transparent"`. |
| `backgroundColor` | string | Hex color or `"transparent"` (the default). |
| `fillStyle` | string | `hachure`, `cross-hatch`, `solid`, `zigzag`. |
| `strokeWidth` | number | `1` thin, `2` bold, `4` extra bold. |
| `strokeStyle` | string | `solid`, `dashed`, `dotted`. |
| `roundness` | object \| null | `null` for sharp corners, or `{ "type": 2 }` proportional / `{ "type": 3, "value": 32 }` adaptive / `{ "type": 1 }` legacy. |
| `roughness` | number | `0` architect (clean), `1` artist (default), `2` cartoonist. |
| `opacity` | number | `0` to `100`. |
| `seed` | number | Random integer. Keeps the hand-drawn shape stable across renders. |
| `version` | number | Increments on each change. |
| `versionNonce` | number | Random integer, regenerated on each change. |
| `index` | string \| null | Fractional index for ordering. Keep in sync with array order. `convertToExcalidrawElements` assigns it. |
| `isDeleted` | boolean | Soft-delete flag. |
| `groupIds` | string[] | Group memberships, deepest first. |
| `frameId` | string \| null | Owning frame id. |
| `boundElements` | object[] \| null | Elements bound to this one: `{ "id": "...", "type": "arrow" \| "text" }`. |
| `updated` | number | Epoch milliseconds of the last update. |
| `link` | string \| null | URL opened when the element is clicked. |
| `locked` | boolean | Locked elements cannot be edited on the canvas. |
| `customData` | object | Optional app-owned data. |

## Element types

| `type` | Extra required fields | Additional fields |
| --- | --- | --- |
| `rectangle`, `diamond`, `ellipse` | none | none |
| `text` | `text` | `fontSize`, `fontFamily`, `textAlign`, `verticalAlign`, `containerId`, `originalText`, `autoResize`, `lineHeight` |
| `line`, `arrow` | `points` | `points`, `lastCommittedPoint`, `startBinding`, `endBinding`, `startArrowhead`, `endArrowhead`; `arrow` adds `elbowed` |
| `freedraw` | none | `points`, `pressures`, `simulatePressure`, `lastCommittedPoint` |
| `image` | `fileId` | `fileId`, `status`, `scale`, `crop` |
| `frame`, `magicframe` | none | `name` |
| `embeddable`, `iframe` | none | none (`customData` used for generation state) |
| `selection` | internal | Not written to scenes. |

`points` are **local** coordinates relative to the element's `x`,`y`. The first point is usually `[0, 0]`.

### Value reference

| Property | Values |
| --- | --- |
| `fillStyle` | `hachure`, `cross-hatch`, `solid`, `zigzag` |
| `strokeStyle` | `solid`, `dashed`, `dotted` |
| `strokeWidth` | `1`, `2`, `4` |
| `roughness` | `0` architect, `1` artist, `2` cartoonist |
| `opacity` | `0`–`100` |
| `fontFamily` | `1` Virgil, `2` Helvetica, `3` Cascadia, `5` Excalifont, `6` Nunito, `7` Lilita One, `8` Comic Shanns, `9` Liberation Sans |
| `textAlign` | `left`, `center`, `right` |
| `verticalAlign` | `top`, `middle`, `bottom` |
| `arrowhead` | `arrow`, `bar`, `dot`, `circle`, `circle_outline`, `triangle`, `triangle_outline`, `diamond`, `diamond_outline`, `crowfoot_one`, `crowfoot_many`, `crowfoot_one_or_many`, or `null` |
| `image.status` | `pending`, `saved`, `error` |

`fontFamily` values are integers. The installed library exports `FONT_FAMILY` (`Virgil` 1, `Helvetica` 2, `Cascadia` 3, `Excalifont` 5, `Nunito` 6, `Lilita One` 7, `Comic Shanns` 8, `Liberation Sans` 9). Value `4` is unused.

## Text elements and containers

Two kinds of text exist.

1. **Free text**: `containerId` is `null`. The element carries its own `x`,`y`,`width`,`height`.
2. **Bound text / label**: the text lives inside a container (rectangle, diamond, ellipse, or arrow). The text has a `containerId`. The container lists the text in its `boundElements`. The container decides the text position; the text is centered or aligned inside it.

Rules for bound text:

- `originalText` holds the unwrapped text. `text` holds the wrapped result. Set both to the same string for a new label.
- `autoResize` is `false` for wrapped text in a container.
- The container's `boundElements` must contain `{ "id": "<textId>", "type": "text" }`.
- Color note: a text label colors itself from the container's `strokeColor` when the label does not set its own.

Build labels with the skeleton API instead of by hand. It sets these fields correctly. See [skeleton-api.md](./skeleton-api.md).

## Arrows, lines, and bindings

Arrows use `startBinding` and `endBinding` to attach to shapes. Ordinary lines leave these fields null. Each arrow binding is:

```json
{ "elementId": "r1", "focus": 0, "gap": 8 }
```

- `elementId` is the bound shape id.
- `focus` positions the attachment along the shape edge (-1 to 1).
- `gap` is the distance from the shape edge.

The bound shape lists the arrow in its `boundElements`:

```json
{ "id": "a1", "type": "arrow" }
```

Keep both sides in sync. Inconsistent bindings can break or be repaired during loading, depending on the restoration options.

Elbow arrows set `"elbowed": true` and may add `fixedSegments`, `startIsSpecial`, `endIsSpecial`. Prefer the skeleton API or the editor over hand-writing these.

## Images and the `files` map

An image element has a `fileId`. The matching entry lives in the top-level `files` map:

```json
{
  "files": {
    "abc123": {
      "id": "abc123",
      "mimeType": "image/png",
      "dataURL": "data:image/png;base64,...",
      "created": 1700000000000,
      "status": "saved"
    }
  }
}
```

`mimeType` accepts the image types in `IMAGE_MIME_TYPES` plus `application/octet-stream`. `dataURL` is a full data URL.

## Invariants and pitfalls

- **Use positive dimensions for boxes, text, and images.** A horizontal or vertical line or arrow can have one zero dimension. Linear elements need at least two points.
- **Set `version`: 1, `versionNonce`, `seed`, and `updated` on each new element.** The skeleton API does this. If you hand-write elements, Excalidraw's `restore` fills missing values, but explicit values avoid surprises.
- **Prefer `isDeleted: true` over removing an element** when the scene may still reference it. If no element references it, you can remove it.
- **Keep `index` in array order**, or leave it `null` and let the library assign indices.
- **`angle` is radians.** Convert degrees with `angle * Math.PI / 180`.
- **Bound text and arrows require both directions** of the reference, or the binding breaks.
- **`appState` on disk is minimal.** Most app state is local UI state and is not exported. Do not expect `zoom` or `scrollX` to persist in the file.
- **The `files` map keys are file ids, not element ids**, even though the type is written loosely as `Record<id, ...>`.

## Verify a scene you wrote

For a normal board, parse the JSON and check IDs, coordinates, references, and image files with `scripts/make-preview.py --check`. Then inspect the rendered preview.

When working inside an existing package runtime, `restore` can normalize the file. It takes the whole scene object, not the elements array:

```js
import { restore } from "@excalidraw/excalidraw";
const { elements } = restore(JSON.parse(sceneJson), null, null);
```

Normalization is not validation. It can discard unsupported elements, replace duplicate IDs, and fill defaults without reporting an error.
Compare active element IDs and counts before and after normalization. Check references separately. Deleted elements can legitimately remain in an editor scene.
Use `scripts/make-preview.py --check` for the routine structural check. It needs no dependencies.
