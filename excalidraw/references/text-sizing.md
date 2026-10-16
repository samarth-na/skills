# Text sizing

Use short labels, explicit line breaks, and generous containers for the first draft. Inspect the rendered text once.
Do not build a font-measurement tool for an ordinary board.

## Stored text dimensions

Excalidraw 0.18.1 computes text height as:

```
height = lineCount × fontSize × lineHeight
```

For size `20` and line height `1.25`, one line is `25` pixels high. Extra padding belongs around the text, not in this formula.
Use the element's `lineHeight`. The copy-ready templates use `1.25`; other fonts can use different values.

Width depends on the actual font and glyphs. For an initial estimate with Virgil or Excalifont:

```
width ≈ longestLineChars × fontSize × 0.62
```

Use roughly `0.72` for an uppercase-heavy line (more than 60% of its letters uppercase). Apply the factor line by line and take the maximum width: a single caps-heavy line such as a code token sets the width for its own line only, not the whole element. Count CJK characters as two for this estimate.

For column-aligned equations, use Cascadia (`fontFamily` 3, monospace). Proportional fonts (Virgil, Excalifont, Helvetica) never align space-padded text; split label and value into separate elements at fixed x positions instead.
These are layout heuristics, not measured bounds. Repeated wide glyphs, emoji, and fallback fonts can exceed them.
Leave spare space in the layout. Shorten or split a label that does not fit in the rendered view.

## Containers and labels

- Free text uses `containerId: null` and usually `autoResize: true`. Write its dimensions even when auto-resize is enabled.
- Bound text uses `containerId` and a matching entry in the container's `boundElements`.
- Set `text` to the displayed lines and `originalText` to the unwrapped content.
- Position hand-written labels explicitly. Do not assume every loading path will repair their size or position.
- Arrow labels are centered on the path. Ordinary lines are not text containers.

For 0.18.1, the available label width and height depend on the container shape:

| Shape | Available width | Available height |
| --- | --- | --- |
| Rectangle | `width - 10` | `height - 10` |
| Diamond | `round(width / 2) - 10` | `round(height / 2) - 10` |
| Ellipse | `round(width / √2) - 10` | `round(height / √2) - 10` |

These are the library's interior limits, not preferred design margins. Leave additional space for readability.

## When a precise check is needed

Use the existing editor with its fonts loaded. Browser canvas `measureText` provides width for the selected font.
The skeleton API also measures text in that runtime. Headless font shims cannot provide exact metrics.
It can flag valid text and miss malformed scenes. Do not treat its exit code as proof of clipping or scene validity.
Use JSON/reference checks for structure and the rendered view for layout.
