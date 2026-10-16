# Element templates

Copy-ready JSON for the default, zero-dependency workflow. Read only the section for the element you need.

Write the file to `~/.opencode/excalidraw/<slug>.excalidraw`, then build its preview with `scripts/make-preview.py`. Copy the common fields as shown. Library restoration fills some defaults, but it does not validate every field or reference.

Field meanings and value tables: [scene-format.md](./scene-format.md).

## Minimal scene file

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": { "viewBackgroundColor": "#ffffff" },
  "files": {}
}
```

## Shared rules

- Use short labels and generous containers. Check text in the rendered view. See [text-sizing.md](./text-sizing.md) only if sizing needs attention.
- Give every element a unique `id`.
- Set `seed` and `versionNonce` to any integers. Set `version` to `1` and `updated` to `1`. These are bookkeeping values; the numbers need not be real timestamps.
- `index` may be `null`. Array order controls z-order (last is on top).
- Keep bindings symmetric. A bound arrow appears in the shape's `boundElements`, and the arrow names the shape in `startBinding`/`endBinding`. A label appears in the container's `boundElements`, and the text names the container in `containerId`.
- `angle` is radians.
- Give boxes, images, and text positive dimensions. Horizontal or vertical lines and arrows can have one zero dimension.

## Rectangle, ellipse, diamond

Change only `type`. All three share this shape.

```json
{
  "id": "box",
  "type": "rectangle",
  "x": 0,
  "y": 0,
  "width": 200,
  "height": 100,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "seed": 1,
  "version": 1,
  "versionNonce": 1,
  "index": null,
  "isDeleted": false,
  "groupIds": [],
  "frameId": null,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false,
  "roundness": { "type": 3 }
}
```

`"roundness": null` gives sharp corners. Use `{ "type": 3 }` for the adaptive radius.

## Free text

```json
{
  "id": "t1",
  "type": "text",
  "x": 40,
  "y": 40,
  "width": 200,
  "height": 25,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "hachure",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "seed": 2,
  "version": 1,
  "versionNonce": 2,
  "index": null,
  "isDeleted": false,
  "groupIds": [],
  "frameId": null,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false,
  "roundness": null,
  "text": "Hello",
  "fontSize": 20,
  "fontFamily": 5,
  "textAlign": "left",
  "verticalAlign": "top",
  "containerId": null,
  "originalText": "Hello",
  "autoResize": true,
  "lineHeight": 1.25
}
```

For multi-line text, put `\n` in both `text` and `originalText`. For free text, set `originalText` equal to the displayed lines.

## Shape with a bound label

Two elements. The container lists the text; the text names the container. Use `autoResize: false` for wrapped labels. Write the label's dimensions and centered position explicitly. Do not assume the loading path will reposition it.

Container:

```json
{
  "id": "box",
  "type": "rectangle",
  "x": 0,
  "y": 0,
  "width": 200,
  "height": 100,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#b2f2bb",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "seed": 3,
  "version": 1,
  "versionNonce": 3,
  "index": null,
  "isDeleted": false,
  "groupIds": [],
  "frameId": null,
  "boundElements": [{ "id": "box-label", "type": "text" }],
  "updated": 1,
  "link": null,
  "locked": false,
  "roundness": { "type": 3 }
}
```

Label:

```json
{
  "id": "box-label",
  "type": "text",
  "x": 70,
  "y": 37,
  "width": 60,
  "height": 25,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "hachure",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "seed": 4,
  "version": 1,
  "versionNonce": 4,
  "index": null,
  "isDeleted": false,
  "groupIds": [],
  "frameId": null,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false,
  "roundness": null,
  "text": "Label",
  "fontSize": 20,
  "fontFamily": 5,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": "box",
  "originalText": "Label",
  "autoResize": false,
  "lineHeight": 1.25
}
```

## Arrow

`points` are relative to `x`,`y`. The first point is usually `[0, 0]`.

```json
{
  "id": "a1",
  "type": "arrow",
  "x": 200,
  "y": 50,
  "width": 100,
  "height": 0,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "hachure",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "seed": 5,
  "version": 1,
  "versionNonce": 5,
  "index": null,
  "isDeleted": false,
  "groupIds": [],
  "frameId": null,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false,
  "roundness": { "type": 2 },
  "points": [[0, 0], [100, 0]],
  "lastCommittedPoint": null,
  "startBinding": null,
  "endBinding": null,
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "elbowed": false
}
```

A multi-segment arrow adds points, for example `[[0, 0], [0, 80], [-120, 80]]`.

Write arrows normalized: `x`,`y` at the bounding-box top-left with non-negative `points` (e.g. a leftward 100px arrow is `x` at the left end, `points` `[[100, 0], [0, 0]]`, `width` 100). Negative-point forms render ambiguously across readers.

## Arrow bound to two shapes

Add the binding on both sides. The arrow:

```json
{
  "id": "a1",
  "type": "arrow",
  "x": 200,
  "y": 50,
  "width": 100,
  "height": 0,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "hachure",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "seed": 6,
  "version": 1,
  "versionNonce": 6,
  "index": null,
  "isDeleted": false,
  "groupIds": [],
  "frameId": null,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false,
  "roundness": { "type": 2 },
  "points": [[0, 0], [100, 0]],
  "lastCommittedPoint": null,
  "startBinding": { "elementId": "box", "focus": 0, "gap": 4 },
  "endBinding": { "elementId": "box2", "focus": 0, "gap": 4 },
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "elbowed": false
}
```

Each bound shape adds the arrow to its `boundElements`:

```json
"boundElements": [{ "id": "a1", "type": "arrow" }]
```

## Line

Same as the arrow, but `"type": "line"` and no arrowheads:

```json
"startArrowhead": null,
"endArrowhead": null
```

## Freedraw

```json
{
  "id": "f1",
  "type": "freedraw",
  "x": 0,
  "y": 0,
  "width": 80,
  "height": 40,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "hachure",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "seed": 7,
  "version": 1,
  "versionNonce": 7,
  "index": null,
  "isDeleted": false,
  "groupIds": [],
  "frameId": null,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false,
  "roundness": null,
  "points": [[0, 0], [30, 20], [80, 40]],
  "pressures": [],
  "simulatePressure": true,
  "lastCommittedPoint": null
}
```

## Frame

Set each child's `frameId` to the frame's ID. Stored frame elements have no `children` list. That field belongs to the skeleton API.

```json
{
  "id": "frame1",
  "type": "frame",
  "x": 0,
  "y": 0,
  "width": 400,
  "height": 300,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "seed": 8,
  "version": 1,
  "versionNonce": 8,
  "index": null,
  "isDeleted": false,
  "groupIds": [],
  "frameId": null,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false,
  "roundness": null,
  "name": "My frame"
}
```

## Image

Add an image element and a matching entry in the top-level `files` map.

```json
{
  "id": "img1",
  "type": "image",
  "x": 0,
  "y": 0,
  "width": 300,
  "height": 200,
  "angle": 0,
  "strokeColor": "transparent",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "seed": 9,
  "version": 1,
  "versionNonce": 9,
  "index": null,
  "isDeleted": false,
  "groupIds": [],
  "frameId": null,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false,
  "roundness": null,
  "fileId": "f-image-1",
  "status": "saved",
  "scale": [1, 1],
  "crop": null
}
```

Files map:

```json
{
  "f-image-1": {
    "id": "f-image-1",
    "mimeType": "image/png",
    "dataURL": "data:image/png;base64,...",
    "created": 1,
    "status": "saved"
  }
}
```

## Elements best added in the editor

`embeddable` and `iframe` store their target URL in the base `link` field. `magicframe` and `stickynote` are newer types. Add these in the editor rather than by hand, then read the saved file for the exact shape.

## Full example

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "appState": { "viewBackgroundColor": "#ffffff" },
  "files": {},
  "elements": [
    {
      "id": "box", "type": "rectangle", "x": 0, "y": 0, "width": 200, "height": 100,
      "angle": 0, "strokeColor": "#1e1e1e", "backgroundColor": "#a5d8ff", "fillStyle": "solid",
      "strokeWidth": 2, "strokeStyle": "solid", "roughness": 1, "opacity": 100,
      "seed": 1, "version": 1, "versionNonce": 1, "index": null, "isDeleted": false,
      "groupIds": [], "frameId": null,
      "boundElements": [{ "id": "box-label", "type": "text" }],
      "updated": 1, "link": null, "locked": false, "roundness": { "type": 3 }
    },
    {
      "id": "box-label", "type": "text", "x": 70, "y": 37, "width": 60, "height": 25,
      "angle": 0, "strokeColor": "#1e1e1e", "backgroundColor": "transparent", "fillStyle": "hachure",
      "strokeWidth": 1, "strokeStyle": "solid", "roughness": 1, "opacity": 100,
      "seed": 2, "version": 1, "versionNonce": 2, "index": null, "isDeleted": false,
      "groupIds": [], "frameId": null, "boundElements": null, "updated": 1, "link": null,
      "locked": false, "roundness": null, "text": "Start", "fontSize": 20, "fontFamily": 5,
      "textAlign": "center", "verticalAlign": "middle", "containerId": "box",
      "originalText": "Start", "autoResize": false, "lineHeight": 1.25
    }
  ]
}
```

## Check once

Parse the JSON. Check unique IDs, finite dimensions, matching bindings, and image file references with `scripts/make-preview.py --check`.
Then inspect the scene in the interactive preview at a readable zoom. Fix observed defects.
