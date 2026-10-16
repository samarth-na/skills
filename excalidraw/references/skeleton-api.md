# Skeleton API: build elements from code

Use this API when the task already has an Excalidraw browser/app runtime or specifically needs package integration. For ordinary board creation, use the direct JSON example in [../SKILL.md](../SKILL.md).

`convertToExcalidrawElements` turns a small description ("skeleton") into full elements. It fills bookkeeping fields and connects labels and arrows. Run it in the existing browser runtime. Do not create a Node bundler or shim runner just to generate a board.

This API is **beta**. Pin the library version.

## Signature

```ts
convertToExcalidrawElements(
  elements: ExcalidrawElementSkeleton[] | null,
  opts?: { regenerateIds: boolean }   // default: true
): OrderedExcalidrawElement[]
```

- `regenerateIds: true` (default) replaces IDs and remaps skeleton references. Use `false` to keep stable IDs for later edits.

```js
import { convertToExcalidrawElements, serializeAsJSON } from "@excalidraw/excalidraw";

const elements = convertToExcalidrawElements([
  { type: "rectangle", x: 0, y: 0 },
], { regenerateIds: false });
```

## Common pattern

```js
const elements = convertToExcalidrawElements([
  { type: "rectangle", id: "a", x: 0, y: 0, width: 200, height: 100, label: { text: "Start" } },
  { type: "diamond", id: "b", x: 300, y: 0, width: 200, height: 100, label: { text: "OK?" } },
  { type: "arrow", x: 200, y: 50, start: { id: "a" }, end: { id: "b" }, label: { text: "yes" } },
]);
```

## Supported shapes

### Rectangle, ellipse, diamond

`type`, `x`, `y` are required. Everything else is optional.

```js
convertToExcalidrawElements([
  { type: "rectangle", x: 50, y: 250, width: 200, height: 100, backgroundColor: "#c0eb75", strokeWidth: 2 },
  { type: "ellipse", x: 300, y: 250, width: 200, height: 100, backgroundColor: "#ffc9c9", strokeStyle: "dotted", fillStyle: "solid" },
  { type: "diamond", x: 550, y: 250, width: 200, height: 100, strokeColor: "#1971c2", strokeStyle: "dashed", fillStyle: "cross-hatch" },
]);
```

### Text

`type`, `x`, `y`, `text` are required.

```js
convertToExcalidrawElements([
  { type: "text", x: 100, y: 100, text: "HELLO WORLD!" },
  { type: "text", x: 100, y: 150, text: "STYLED", fontSize: 20, strokeColor: "#5f3dc4" },
]);
```

### Lines and arrows

`type`, `x`, `y` are required. `points` is optional; the API fills a default.

```js
convertToExcalidrawElements([
  { type: "arrow", x: 450, y: 20, startArrowhead: "circle", endArrowhead: "triangle", strokeColor: "#1971c2" },
  { type: "line", x: 450, y: 60, strokeColor: "#2f9e44", strokeStyle: "dotted" },
]);
```

### Text containers (labels)

Add a `label` property to a container. `label.text` is required. If you omit the container size, the API sizes it from the label.

```js
convertToExcalidrawElements([
  { type: "rectangle", x: 300, y: 290, label: { text: "RECTANGLE LABEL" } },
  { type: "ellipse", x: 500, y: 100, label: { text: "ELLIPSE\nLABEL" } },
  { type: "diamond", x: 100, y: 100, label: { text: "DIAMOND\nLABEL", textAlign: "center", verticalAlign: "middle" } },
]);
```

`label` accepts `fontSize`, `fontFamily`, `textAlign`, `verticalAlign`, `strokeColor`, and other element fields, so a label can carry its own styling.

### Labelled arrows

An arrow also accepts `label`.

```js
convertToExcalidrawElements([
  { type: "arrow", x: 100, y: 100, label: { text: "LABELED ARROW" } },
]);
```

### Arrow bindings

Add `start` and `end` to an arrow. Each side takes either a `type` (a new shape is created and bound) or an `id` (bind to an existing element). Other fields on `start`/`end` are optional.

Bind to a new shape by type:

```js
convertToExcalidrawElements([
  { type: "arrow", x: 255, y: 239, label: { text: "HELLO" }, start: { type: "rectangle" }, end: { type: "ellipse" } },
]);
```

Bind by id to reuse one shape across arrows:

```js
convertToExcalidrawElements([
  { type: "ellipse", id: "ellipse-1", x: 390, y: 356, width: 150, height: 150, backgroundColor: "#d8f5a2" },
  { type: "diamond", id: "diamond-1", x: -30, y: 380, width: 100 },
  { type: "arrow", x: 100, y: 440, start: { id: "diamond-1" }, end: { id: "ellipse-1" } },
]);
```

Use `{ regenerateIds: false }` so your `id` values survive.

`start` and `end` also accept `{ type: "text", text: "..." }` to bind an arrow to text.

### Frames

A frame takes `type`, `children` (element ids), and an optional `name`.

```js
convertToExcalidrawElements([
  { type: "rectangle", x: 10, y: 10, id: "1" },
  { type: "diamond", x: 120, y: 20, id: "2", label: { text: "IN FRAME" } },
  { type: "frame", children: ["1", "2"], name: "My frame" },
]);
```

## What the skeleton API does not cover

- `freedraw`, `iframe`, and `embeddable` are accepted as complete elements. They pass through without the shape-construction defaults.
- Hand-drawn `points` shaping for lines and arrows is limited. For precise multi-point paths, pass `points` on the linear element, or edit the element after creation.
- It does not render. Convert, then export or display. See [appstate-and-export.md](./appstate-and-export.md).

## After conversion

Serialize to a scene file:

```js
const json = serializeAsJSON(elements, { viewBackgroundColor: "#ffffff" }, {}, "local");
```

Pass `elements` to a React `<Excalidraw initialData={{ elements }} />`, or to `excalidrawAPI.updateScene({ elements })` in a running editor.

## Notes for agents

- Use a skeleton for initial construction. After hand edits, the saved `.excalidraw` file is the source of truth.
- Set `regenerateIds: false` when ids are referenced by bindings.
- The skeleton is not itself a `.excalidraw` file. Convert first, then serialize.
- If you only need to change a few elements of an existing scene, load the scene JSON, find the elements by id, mutate or replace them, then re-serialize. Re-running the whole skeleton is simpler when you own the file.
