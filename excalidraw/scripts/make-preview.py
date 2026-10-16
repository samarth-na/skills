#!/usr/bin/env python3
"""Generate an editable HTML preview for an Excalidraw scene.

Reads a .excalidraw scene and the skill's viewer.html, injects the scene as
window.__EXCALIDRAW_SCENE__, and writes a preview HTML file next to the scene.
The scene is embedded; viewing needs network access for the CDN-hosted editor.

Zero dependencies (stdlib only). Usage:
    python3 make-preview.py ~/.opencode/excalidraw/board.excalidraw [--out board.html]
    python3 make-preview.py ~/.opencode/excalidraw/board.excalidraw --check

--check validates the scene without writing anything: structural errors
(envelope keys, unique IDs, finite dimensions, matching bindings/image refs)
plus layout warnings (overlapping boxes, labels overflowing their containers).
Exit code: 0 means clean, 1 means errors (or warnings in --check mode),
2 means usage or file error. Normal builds still write HTML when only
layout warnings exist.
"""
import json
import math
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
VIEWER = SKILL_DIR / "assets" / "viewer.html"
MARKER = "<script>\n  window.__EXCALIDRAW_SCENE__ = window.__EXCALIDRAW_SCENE__ || null;\n</script>"


def load_scene(path):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, json.JSONDecodeError) as err:
        print(f"cannot read {path}: {err}", file=sys.stderr)
        sys.exit(2)


def check(scene):
    errors = []
    warnings = []
    if not isinstance(scene, dict):
        return ["scene must be a JSON object"], []
    if scene.get("type") != "excalidraw":
        errors.append('scene.type must be "excalidraw"')
    if scene.get("version") != 2:
        errors.append("scene.version must be 2")
    elements = scene.get("elements")
    if not isinstance(elements, list):
        return errors + ["scene.elements must be an array"], []
    by_id = {}
    for el in elements:
        if not isinstance(el, dict):
            errors.append("every element must be an object")
            continue
        eid = el.get("id")
        if not eid:
            errors.append("element without id")
            continue
        if eid in by_id:
            errors.append(f'duplicate id "{eid}"')
        by_id[eid] = el
        for key in ("x", "y", "width", "height"):
            val = el.get(key)
            if not isinstance(val, (int, float)) or not math.isfinite(val):
                errors.append(f'{eid}: {key} must be a finite number')
        if el.get("type") in ("rectangle", "diamond", "ellipse", "text", "image", "frame", "magicframe"):
            w, h = el.get("width"), el.get("height")
            if isinstance(w, (int, float)) and isinstance(h, (int, float)):
                if w <= 0 or h <= 0:
                    errors.append(f"{eid}: needs positive width/height")
    for el in elements:
        if not isinstance(el, dict):
            continue
        eid = el.get("id")
        container = el.get("containerId")
        if container and container not in by_id:
            errors.append(f'{eid}: containerId "{container}" not found')
        for binding in (el.get("startBinding"), el.get("endBinding")):
            if isinstance(binding, dict):
                target = by_id.get(binding.get("elementId"))
                if target is None:
                    errors.append(f'{eid}: binding to missing "{binding.get("elementId")}"')
                elif not any(b.get("id") == eid for b in target.get("boundElements") or []):
                    errors.append(f"{eid}: one-sided binding to \"{binding.get('elementId')}\"")
        bound = el.get("boundElements") or []
        for ref in bound:
            if isinstance(ref, dict) and ref.get("id") not in by_id:
                errors.append(f'{eid}: boundElements references missing "{ref.get("id")}"')
        if el.get("type") == "image":
            fid = el.get("fileId")
            if fid not in (scene.get("files") or {}):
                errors.append(f'{eid}: fileId "{fid}" missing from files map')
    warnings.extend(check_layout(elements, by_id))
    warnings.extend(check_arrow_crossings(elements, by_id))
    return errors, warnings


def _seg_samples(p, q, n=20):
    for i in range(n + 1):
        t = i / n
        yield (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def check_arrow_crossings(elements, by_id):
    """Arrow shafts crossing text they do not label. Warnings only."""
    out = []
    texts = [
        e for e in elements
        if isinstance(e, dict) and e.get("type") == "text" and not e.get("isDeleted")
        and all(isinstance(e.get(k), (int, float)) for k in ("x", "y", "width", "height"))
    ]
    for el in elements:
        if not isinstance(el, dict) or el.get("type") not in ("line", "arrow"):
            continue
        if el.get("isDeleted"):
            continue
        pts = el.get("points") or []
        if len(pts) < 2:
            continue
        ox, oy = el.get("x") or 0, el.get("y") or 0
        abs_pts = [(ox + p[0], oy + p[1]) for p in pts]
        bound = {el.get("id")}
        for binding in (el.get("startBinding"), el.get("endBinding")):
            if isinstance(binding, dict) and binding.get("elementId"):
                bound.add(binding.get("elementId"))
        for i in range(len(abs_pts) - 1):
            for sx, sy in _seg_samples(abs_pts[i], abs_pts[i + 1]):
                for t in texts:
                    # The arrow's own label rides the shaft by design, and
                    # labels of connected shapes sit near the endpoints.
                    if t.get("containerId") == el.get("id"):
                        continue
                    if t.get("containerId") in bound:
                        continue
                    if any(r.get("id") == t.get("id") for r in el.get("boundElements") or []):
                        continue
                    pad = 1
                    if (t["x"] - pad < sx < t["x"] + t["width"] + pad
                            and t["y"] - pad < sy < t["y"] + t["height"] + pad):
                        out.append(
                            f'crossing: arrow "{el["id"]}" passes through text "{t["id"]}"'
                        )
                        break
                else:
                    continue
                break
    # Deduplicate repeat hits from adjacent samples on the same pair.
    seen, uniq = set(), []
    for w in out:
        if w not in seen:
            seen.add(w)
            uniq.append(w)
    return uniq


def _line_factor(line):
    letters = "".join(c for c in line if c.isalpha())
    if not letters:
        return 0.62
    upper = sum(1 for c in letters if c.isupper())
    return 0.72 if upper / len(letters) > 0.6 else 0.62


def _est_text_size(el):
    lines = str(el.get("text") or "").split("\n")
    size = el.get("fontSize") or 20
    lh = el.get("lineHeight") or 1.25
    width = max(
        (len(l) * size * _line_factor(l) for l in lines), default=0
    )
    return width, len(lines) * size * lh


def check_layout(elements, by_id):
    """Machine-checkable layout failures. Warnings only, never errors."""
    out = []
    solids = [
        e for e in elements
        if isinstance(e, dict) and not e.get("isDeleted")
        and e.get("type") in ("rectangle", "diamond", "ellipse", "text", "image", "frame", "magicframe")
        and all(isinstance(e.get(k), (int, float)) for k in ("x", "y", "width", "height"))
    ]

    def linked(a, b):
        if a.get("containerId") == b.get("id") or b.get("containerId") == a.get("id"):
            return True
        for owner, other in ((a, b), (b, a)):
            if any(r.get("id") == other.get("id") for r in owner.get("boundElements") or []):
                return True
        # Same group: intentionally composed (e.g. text layered on a shape).
        if set(a.get("groupIds") or []) & set(b.get("groupIds") or []):
            return True
        return False

    def contains(outer, inner, margin=8):
        return (
            outer["x"] - margin <= inner["x"]
            and outer["y"] - margin <= inner["y"]
            and outer["x"] + outer["width"] + margin >= inner["x"] + inner["width"]
            and outer["y"] + outer["height"] + margin >= inner["y"] + inner["height"]
        )

    for i, a in enumerate(solids):
        for b in solids[i + 1 :]:
            if linked(a, b):
                continue
            # A card containing its content is intentional, not a collision.
            if contains(a, b) or contains(b, a):
                continue
            ax1, ay1 = a["x"] + 2, a["y"] + 2
            ax2, ay2 = a["x"] + a["width"] - 2, a["y"] + a["height"] - 2
            bx1, by1 = b["x"] + 2, b["y"] + 2
            bx2, by2 = b["x"] + b["width"] - 2, b["y"] + b["height"] - 2
            ox, oy = min(ax2, bx2) - max(ax1, bx1), min(ay2, by2) - max(ay1, by1)
            if ox <= 0 or oy <= 0:
                continue
            # Corner grazes (e.g. diamond/ellipse bounding boxes) are noise;
            # only flag collisions covering a real fraction of a box.
            smaller = min(a["width"] * a["height"], b["width"] * b["height"])
            if smaller > 0 and (ox * oy) / smaller > 0.05:
                out.append(f'overlap: "{a["id"]}" and "{b["id"]}" boxes intersect')
    for el in elements:
        if not isinstance(el, dict) or el.get("type") != "text" or el.get("isDeleted"):
            continue
        cont = by_id.get(el.get("containerId") or "")
        if cont and cont.get("type") in ("rectangle", "diamond", "ellipse"):
            est_w, est_h = _est_text_size(el)
            cw, ch = cont["width"], cont["height"]
            if cont["type"] == "rectangle":
                avail_w, avail_h = cw - 10, ch - 10
            elif cont["type"] == "diamond":
                avail_w, avail_h = round(cw / 2) - 10, round(ch / 2) - 10
            else:
                avail_w, avail_h = round(cw / 1.4142) - 10, round(ch / 1.4142) - 10
            if est_w > avail_w or est_h > avail_h:
                out.append(
                    f'overflow: label "{el["id"]}" needs ~{est_w:.0f}x{est_h:.0f} '
                    f'but "{cont["id"]}" fits ~{avail_w}x{avail_h}'
                )
        elif not el.get("containerId"):
            # Free text: the editor renders stored dims as-is, so a
            # guessed-narrow box clips even with autoResize enabled.
            # (Headless scenes measured with font shims are the usual cause.)
            est_w, est_h = _est_text_size(el)
            w, h = el.get("width") or 0, el.get("height") or 0
            if w < est_w or h < est_h:
                out.append(
                    f'clipped: free text "{el["id"]}" {str(el.get("text"))[:40]!r} '
                    f"stored {w}x{h} < ~{est_w:.0f}x{est_h:.0f}"
                )
    return out


def main(argv):
    if not argv or "--help" in argv or "-h" in argv:
        print(__doc__.strip())
        return 0 if argv else 2
    src = Path(argv[0])
    check_only = "--check" in argv
    scene = load_scene(src)
    errors, warnings = check(scene)
    if errors:
        for p in errors:
            print(f"error: {p}")
        return 1
    for w in warnings:
        print(f"warning: {w}")
    if check_only:
        if warnings:
            print(f"warnings: {len(warnings)} (no file written)")
            return 1
        print(f"ok: {src} ({len(scene['elements'])} elements)")
        return 0
    out = None
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])
    else:
        out = src.with_suffix(".html")
    try:
        viewer = VIEWER.read_text()
    except OSError as err:
        print(f"cannot read viewer: {err}", file=sys.stderr)
        return 2
    if MARKER not in viewer:
        print("viewer marker not found; viewer.html changed?", file=sys.stderr)
        return 2
    payload = json.dumps(scene).replace("<", "\\u003c")
    page = viewer.replace(
        MARKER, f"<script>window.__EXCALIDRAW_SCENE__ = {payload};</script>", 1
    )
    title = src.stem
    page = page.replace(
        "<title>Excalidraw local editor</title>", f"<title>{title}</title>", 1
    )
    out.write_text(page)
    print(f"wrote {out} ({len(page)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
