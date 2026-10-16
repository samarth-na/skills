#!/usr/bin/env python3
"""Optional diagnostic for @html output.

Usage: python3 check.py FILE.html [FILE2.html ...]

Flags common markup issues in one run:

  - tag balance (unclosed or mismatched tags);
  - every class used in markup or JS selectors is defined in the file's own
    <style> blocks or in this skill's styles/*.css;
  - exactly one <h1>, and it matches the <title>;
  - every href="#..." anchor resolves to an id that exists;
  - <pre> content is escaped (no raw <, >, or bare &);
  - no external loadable assets (src, <link>, @import, url()); http(s) in
    anchor hrefs is fine, citations load nothing.

Exits 0 on pass, 1 on any finding. Optional only, not a delivery gate.
"""
import re
import sys
from pathlib import Path
from html.parser import HTMLParser

SKILL = Path(__file__).resolve().parent.parent
VOID = {"meta", "link", "img", "br", "hr", "input", "source", "wbr", "col",
        "area", "base", "embed", "track", "param"}
NON_CLASS = {"c-theme"}  # localStorage key, not a class


class Balance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"stray </{tag}> at {self.getpos()}")
            return
        open_tag, pos = self.stack.pop()
        if open_tag != tag:
            self.errors.append(
                f"<{open_tag}> at {pos} closed by </{tag}> at {self.getpos()}")


def skill_classes():
    defined = set()
    for css in sorted((SKILL / "styles").glob("*.css")):
        defined |= set(re.findall(r"\.([a-z][a-z0-9_-]*)", css.read_text()))
    return defined


def main(paths):
    defined_base = skill_classes()
    fail = False
    for raw in paths:
        f = Path(raw)
        text = f.read_text()
        issues = []

        defined = set(defined_base)
        for block in re.findall(r"<style[^>]*>(.*?)</style>", text, re.S):
            defined |= set(re.findall(r"\.([a-z][a-z0-9_-]*)", block))

        p = Balance()
        p.feed(text)
        p.close()
        for tag, pos in p.stack:
            issues.append(f"[TAG] unclosed <{tag}> at {pos}")
        issues.extend(f"[TAG] {e}" for e in p.errors)

        used = set()
        for attr in re.findall(r'class="([^"]+)"', text):
            used |= set(attr.split())
        for sel in re.findall(r"['\"]\.((?:c-)[a-z0-9- ]+)['\"]", text):
            used |= set(sel.split())
        used = {c for c in used if c.startswith("c-") and c not in NON_CLASS}
        for m in sorted(c for c in used if c not in defined):
            issues.append(f"[CLASS] uses .{m} but nothing defines it")

        h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", text, re.S)
        title = re.findall(r"<title[^>]*>(.*?)</title>", text, re.S)
        if len(h1) != 1:
            issues.append(f"[HEAD] expected 1 <h1>, found {len(h1)}")
        elif title:
            h1t = re.sub(r"<[^>]+>", "", h1[0])
            if " ".join(h1t.split()) != " ".join(title[0].split()):
                issues.append("[HEAD] <h1> does not match <title>")

        ids = set(re.findall(r'id="([^"]+)"', text))
        for a in sorted(set(re.findall(r'href="#([^"]+)"', text))):
            if a not in ids:
                issues.append(f"[ANCHOR] href=\"#{a}\" has no matching id")

        tables = len(re.findall(r"<table[\s>]", text))
        wraps = len(re.findall(r"c-table-wrap", text))
        if tables > wraps:
            issues.append(
                f"[RESP] {tables} <table> but only {wraps} .c-table-wrap: "
                "wrap every table so wide tables scroll internally")
        if 'name="viewport"' not in text:
            issues.append('[RESP] no <meta name="viewport">: page will not '
                          "scale on narrow screens")
        if re.search(r"width:\s*min\(100vw", text):
            issues.append("[RESP] width from 100vw includes the scrollbar: "
                         "use 100% against the padded body instead")

        for pre in re.findall(r"<pre[^>]*>(.*?)</pre>", text, re.S):
            code = re.sub(r"<[^>]+>", "", pre)
            if "<" in code or ">" in code:
                issues.append(f"[PRE] raw < or > inside <pre>: {code[:60]!r}")
            for amp in re.finditer(r"&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)", code):
                issues.append(f"[PRE] bare & inside <pre>: …{code[max(0, amp.start()-20):amp.start()+20]!r}")
                break

        ext = []
        ext += re.findall(r'(?:src|data-src)="((?:https?:)?//[^"]*)"', text)
        ext += re.findall(r'<link[^>]+href="((?:https?:)?//[^"]*)"', text)
        for style in re.findall(r"<style[^>]*>(.*?)</style>", text, re.S):
            ext += re.findall(r'@import\s+(?:url\()?[\'"]?((?:https?:)?//[^)]*)', style)
            ext += re.findall(r'url\(\s*[\'"]?((?:https?:)?//[^)]*)', style)
        for u in sorted(set(ext)):
            issues.append(f"[ASSET] external loadable reference: {u}")

        if issues:
            fail = True
            for i in issues:
                print(i)
        print(f"{f.name}: {'FAIL' if issues else 'ok'}")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: check.py FILE.html [FILE2.html ...]")
        sys.exit(2)
    main(sys.argv[1:])
