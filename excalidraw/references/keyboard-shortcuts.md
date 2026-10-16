# Keyboard shortcuts

Sources: the app's shortcut map in `packages/excalidraw/actions/shortcuts.ts` and the in-app help dialog (`?`). The tool-key list matches the editor's tool actions. Verify in-app with `?` when a shortcut matters.

Notation: **Cmd** is macOS, **Ctrl** is Windows and Linux. **Alt** is Option on macOS. "CtrlOrCmd" below means Cmd on macOS and Ctrl elsewhere.

The in-app help dialog opens with `?`. It lists every shortcut with a search box.

## Tools

| Action | Shortcut |
| --- | --- |
| Selection | `V` or `1` |
| Rectangle | `R` or `2` |
| Diamond | `D` or `3` |
| Ellipse | `O` or `4` |
| Arrow | `A` or `5` |
| Line | `L` or `6` |
| Draw (freehand) | `P` or `7` |
| Text | `T` or `8` |
| Insert image | `9` |
| Eraser | `E` or `0` |
| Frame | `F` |
| Hand (pan) | `H` |
| Laser pointer | `K` |
| Pick color from canvas (eyedropper) | `I` |
| Show stroke color picker | `S` |
| Show background color picker | `G` |
| Keep the selected tool active after drawing (tool lock) | `Q` |
| Edit text / add label | `Enter` |
| Finish editing (text editor) | `Esc` |
| Edit or finish line/arrow points | `CtrlOrCmd+Enter` |
| New line in the text editor | `Enter` or `Shift+Enter` |
| Prevent arrow binding | hold `CtrlOrCmd` while dragging |
| Add or update a link on a shape | `CtrlOrCmd+K` |

## View

| Action | Shortcut |
| --- | --- |
| Zoom in | `CtrlOrCmd++` |
| Zoom out | `CtrlOrCmd+-` |
| Reset zoom | `CtrlOrCmd+0` |
| Zoom to fit all elements | `Shift+1` |
| Zoom to selection (fit in viewport) | `Shift+2` |
| Zoom to fit selection | `Shift+3` |
| Page up / down | `PageUp` / `PageDown` |
| Page left / right | `Shift+PageUp` / `Shift+PageDown` |
| Zen mode | `Alt+Z` |
| View mode | `Alt+R` |
| Toggle theme | `Shift+Alt+D` |
| Show grid | `CtrlOrCmd+'` |
| Snap to objects | `Alt+S` |
| Stats for nerds | `Alt+/` |
| Move canvas | hold `Space` and drag, or middle-mouse drag |

## Editor and scene

| Action | Shortcut |
| --- | --- |
| Save scene | `CtrlOrCmd+S` |
| Open scene | `CtrlOrCmd+O` |
| Export image | `CtrlOrCmd+Shift+E` |
| Command palette | `CtrlOrCmd+/` or `CtrlOrCmd+Shift+P` |
| Search in scene | `CtrlOrCmd+F` |
| Copy | `CtrlOrCmd+C` |
| Cut | `CtrlOrCmd+X` |
| Paste | `CtrlOrCmd+V` |
| Select all | `CtrlOrCmd+A` |
| Delete selection | `Delete` |
| Clear canvas | `CtrlOrCmd+Delete` |
| Undo | `CtrlOrCmd+Z` |
| Redo | `CtrlOrCmd+Y` (also `CtrlOrCmd+Shift+Z`) |
| Duplicate selection | `CtrlOrCmd+D`, or `Alt`+drag |
| Copy as PNG | `Shift+Alt+C` |
| Copy styles | `CtrlOrCmd+Alt+C` |
| Paste styles | `CtrlOrCmd+Alt+V` |
| Group selection | `CtrlOrCmd+G` |
| Ungroup selection | `CtrlOrCmd+Shift+G` |
| Lock / unlock selection | `CtrlOrCmd+Shift+L` |
| Flip horizontal | `Shift+H` |
| Flip vertical | `Shift+V` |
| Bring forward | `CtrlOrCmd+]` |
| Send backward | `CtrlOrCmd+[` |
| Bring to front | `CtrlOrCmd+Shift+]` (macOS: `CtrlOrCmd+Alt+]`) |
| Send to back | `CtrlOrCmd+Shift+[` (macOS: `CtrlOrCmd+Alt+[`) |
| Align top / bottom / left / right | `CtrlOrCmd+Shift+Arrow` |
| Decrease / increase font size | `CtrlOrCmd+Shift+<` / `CtrlOrCmd+Shift+>` |
| Toggle shortcuts help | `?` |

## Flowchart quick-create

These are drawing gestures, not single keys:

1. Press `R` to pick the rectangle tool.
2. Press `Enter` to add a text label, then `Esc` when done.
3. `CtrlOrCmd+Arrow` creates a new connected node in the arrow direction. Repeat to chain nodes.
4. Press `Tab` while drawing to switch the next node between rectangle, diamond, and ellipse.
5. `Alt+Arrow` moves the selection.

Source: <https://plus.excalidraw.com/how-to-start>.

## Notes

- Tool keys `V R D O A L P T E` and their digit equivalents are the stable set. `H`, `K`, `F`, `I` cover hand, laser, frame, and eyedropper.
- `Q` is tool lock in current versions. Some older third-party lists still show `Shift+Enter`; the source of truth is the in-app `?` dialog.
- A focused text editor consumes most keys. Press `Esc` first to return to the canvas.
- `CtrlOrCmd+S` saves to the active file when the app has file access; otherwise it saves to the browser.
