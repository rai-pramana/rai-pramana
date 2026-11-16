#!/usr/bin/env python3
"""Outline text into SVG paths so it can never render as tofu.

GitHub renders <img src="*.svg"> on the *viewer's* machine. Any <text> left in a
widget is therefore one missing font away from a row of boxes: a box with no CJK
font installed sees 日本語 as tofu, because the Latin fallback chain (DejaVu /
Noto Sans / Liberation) simply has no glyph for it and fontconfig does not
substitute a CJK face on most Linux installs.

Fix: convert every glyph to a <path>. The SVG carries its own outlines, so it
renders identically everywhere. Same rule the hero already follows.

Fonts (SIL OFL 1.1):
  JP    Zen Maru Gothic - rounded, warm, reads as Japanese without shouting
  Latin Noto Sans      - what GitHub itself uses for body copy, so a mixed line
                         ("3D 貢献") does not change voice mid-string
"""
from functools import lru_cache
from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

CANDIDATES = {
    ("jp", "regular"): [Path.home() / ".fonts/ZenMaruGothic.ttf",
                        Path("/usr/share/fonts/ZenMaruGothic-Regular.ttf")],
    ("jp", "bold"): [Path.home() / ".fonts/ZenMaruGothic-Bold.ttf",
                     Path("/usr/share/fonts/ZenMaruGothic-Bold.ttf")],
    ("latin", "regular"): [Path("/usr/share/fonts/noto/NotoSans-Regular.ttf"),
                           Path("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"),
                           Path("/usr/share/fonts/noto/NotoSansCJK-Regular.ttc")],
    ("latin", "bold"): [Path("/usr/share/fonts/noto/NotoSans-Bold.ttf"),
                        Path("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf")],
}


def _first_existing(paths, what):
    for p in paths:
        if p.exists():
            return p
    raise SystemExit(f"missing font for {what}; looked in: " + ", ".join(map(str, paths)))


@lru_cache(maxsize=8)
def _font(kind, bold):
    path = _first_existing(CANDIDATES[(kind, "bold" if bold else "regular")],
                           f"{kind}/{'bold' if bold else 'regular'}")
    f = TTFont(str(path))
    return f, f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm


def _pick(ch):
    """Non-ASCII goes to Zen Maru (kana, kanji, CJK punctuation); ASCII stays on
    Noto so Latin copy keeps GitHub's body voice."""
    return "latin" if ord(ch) < 128 else "jp"


@lru_cache(maxsize=1024)
def layout(text, size, bold=False):
    """Lay `text` out at `size` px.

    Returns (paths, width, bbox); baseline sits at y=0 and x starts at 0, bbox is
    the ink box (xmin, ymin, xmax, ymax) with y negative above the baseline.
    """
    paths = []
    x = 0.0
    box = [float("inf"), float("inf"), float("-inf"), float("-inf")]
    for ch in text:
        first = _pick(ch)
        for kind in (first, "jp" if first == "latin" else "latin"):  # preferred, then fallback
            _, gs, cmap, upem = _font(kind, bold)
            name = cmap.get(ord(ch))
            if name:
                break
        if not name:                          # nothing has it: keep the advance
            x += size * 0.5
            continue

        s = size / upem
        pen = SVGPathPen(gs)
        gs[name].draw(TransformPen(pen, Transform(s, 0, 0, -s, x, 0)))
        if d := pen.getCommands():
            paths.append(d)

        bp = BoundsPen(gs)
        gs[name].draw(TransformPen(bp, Transform(s, 0, 0, -s, x, 0)))
        if bp.bounds:
            x0, y0, x1, y1 = bp.bounds
            box[0] = min(box[0], x0)
            box[1] = min(box[1], y0)
            box[2] = max(box[2], x1)
            box[3] = max(box[3], y1)

        x += gs[name].width * s

    if box[0] is float("inf"):
        box = [0.0, -size, x, 0.0]
    return paths, x, tuple(box)


def runs(text, size, bold=False):
    """Per-character outlines as (path_d, x_start).

    Same shaping as layout(), but one entry per glyph so a caller can stagger
    them. `d` already carries its own x offset (TransformPen bakes it in), so a
    caller only needs to translate the whole line to centre it. Whitespace
    advances the pen and yields no entry -- a space types instantly, which is
    what a real typist's rhythm looks like anyway.
    """
    out, x = [], 0.0
    for ch in text:
        first = _pick(ch)
        name = None
        for kind in (first, "jp" if first == "latin" else "latin"):
            _, gs, cmap, upem = _font(kind, bold)
            name = cmap.get(ord(ch))
            if name:
                break
        if not name:                          # nothing has it: keep the advance
            x += size * 0.5
            continue
        s = size / upem
        pen = SVGPathPen(gs)
        gs[name].draw(TransformPen(pen, Transform(s, 0, 0, -s, x, 0)))
        if d := pen.getCommands():
            out.append((d, x))
        x += gs[name].width * s
    return out, x


def svg(text, size, fill, bold=False, pad=0.04, cls=""):
    """Standalone SVG document for `text`, cropped to its ink box."""
    paths, width, (x0, y0, x1, y1) = layout(text, size, bold)
    pad = size * pad
    vx, vy = x0 - pad, y0 - pad
    vw, vh = (x1 - x0) + 2 * pad, (y1 - y0) + 2 * pad
    body = "".join(f'<path d="{d}"/>' for d in paths)
    klass = f' class="{cls}"' if cls else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{vw:.2f}" height="{vh:.2f}" '
            f'viewBox="{vx:.2f} {vy:.2f} {vw:.2f} {vh:.2f}"{klass} '
            f'role="img" aria-label="{text}">'
            f'<g fill="{fill}">{body}</g></svg>')


def group(text, size, fill, x, y, bold=False, opacity=None):
    """Inline <g> for composing several runs inside one larger SVG."""
    paths, width, _ = layout(text, size, bold)
    body = "".join(f'<path d="{d}"/>' for d in paths)
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<g transform="translate({x:.2f},{y:.2f})" fill="{fill}"{op}>{body}</g>',
            width)


if __name__ == "__main__":
    import sys
    for t in sys.argv[1:] or ["技術", "一期一会 · よろしくお願いします"]:
        s = svg(t, 24, "#D8BD8A")
        print(f"{t!r}: {len(s)}B")
        print("  " + s[:180])