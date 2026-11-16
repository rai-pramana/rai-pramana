#!/usr/bin/env python3
"""Donut chart for the language card (self-hosted, dual theme).

Why not GitHub's top-langs card: it offers no colour control, and a single-hue
bar ramp made five of eight rows look identical. So the card is ours.

Palette rule (the part that is actually checkable):
  · every slice is >= 3:1 against the card background -- WCAG 1.4.11 non-text
    contrast, the bar a *meaningful* slice has to clear
  · slices are separated by a 1.5px stroke in the card background colour, which
    is what makes two similar-value golds readable next to each other
  · warm gold/bronze carries the page; steel and violet appear once each so the
    eight categories stay distinguishable without turning into a rainbow

Adjacent-slice contrast is deliberately NOT maximised: eight tones inside one
hue cannot all be 3:1 against each other, and forcing it produces a saturated
palette that fights the neo-Tokyo ink. The stroke is the separator; the numbers
in the legend are the real read-out.
"""
from pathlib import Path
import json, math, html

HERE = Path(__file__).resolve().parent
LANGS = json.loads((HERE / "data" / "langs.json").read_text())
# Jupyter Notebook is ~50% of raw bytes because notebooks commit rendered
# output (base64 PNG) with the code. Counting it reports the profile as half
# notebook when the authored source is mostly Python/JS/HTML.
SKIP = {"Jupyter Notebook"}

rows = [(k, v) for k, v in sorted(LANGS.items(), key=lambda kv: -kv[1]) if k not in SKIP][:8]
total = sum(v for _, v in rows)

# name, dark-theme slice, light-theme slice
PALETTE = [
    ("Python",           "#E9D6B4", "#6E5730"),
    ("JavaScript",       "#B4813C", "#9A6B2F"),
    ("HTML",             "#6F7F8C", "#33404E"),
    ("C",                "#8A6F45", "#7A5C2E"),
    ("Kotlin",           "#D8BD8A", "#4C391C"),
    ("Shell",            "#7E6A9B", "#5F5178"),
    ("TeX",              "#A9803F", "#8A6F45"),
    ("TypeScript",       "#5C6B7D", "#55636F"),
]
assert len(PALETTE) >= len(rows)
COL = {n: (d, l) for n, d, l in PALETTE}

W, H = 480, 264
CX, CY, R_OUT, R_IN = 128, 146, 84, 52
LEG_X = 246


def _lum(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    l1, l2 = sorted((_lum(a), _lum(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


# angles: start at 12 o'clock, clockwise
segments, a = [], -90.0
for name, val in rows:
    sweep = 360 * val / total
    segments.append((name, a, a + sweep, val))
    a += sweep


def pt(cx, cy, r, deg):
    t = math.radians(deg)
    return cx + r * math.cos(t), cy + r * math.sin(t)


def ring_path(a0, a1):
    """Donut slice between two angles (degrees, 0 = 3 o'clock)."""
    large = 1 if (a1 - a0) > 180 else 0
    x0, y0 = pt(CX, CY, R_OUT, a0)
    x1, y1 = pt(CX, CY, R_OUT, a1)
    x2, y2 = pt(CX, CY, R_IN, a1)
    x3, y3 = pt(CX, CY, R_IN, a0)
    return (f"M {x0:.2f} {y0:.2f} A {R_OUT} {R_OUT} 0 {large} 1 {x1:.2f} {y1:.2f} "
            f"L {x2:.2f} {y2:.2f} A {R_IN} {R_IN} 0 {large} 0 {x3:.2f} {y3:.2f} Z")


FONT = "Segoe UI,Helvetica,Arial,sans-serif"


def card(bg, border, title, text, muted):
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" aria-label="Top languages">',
         f'<rect width="{W}" height="{H}" rx="6" fill="{bg}" stroke="{border}"/>',
         f'<text x="16" y="30" font-family="{FONT}" font-size="14" font-weight="600" '
         f'fill="{title}">Top Languages</text>']

    idx = 0 if bg != "#FFFFFF" else 1
    for name, a0, a1, val in segments:
        p.append(f'<path d="{ring_path(a0, a1)}" fill="{COL[name][idx]}" '
                 f'stroke="{bg}" stroke-width="1.5"/>')

    p.append(f'<text x="{CX}" y="{CY - 2}" text-anchor="middle" font-family="{FONT}" '
             f'font-size="20" font-weight="600" fill="{title}">{len(rows)}</text>')
    p.append(f'<text x="{CX}" y="{CY + 15}" text-anchor="middle" font-family="{FONT}" '
             f'font-size="10" letter-spacing="0.6" fill="{muted}">LANGS</text>')

    y = 62
    for name, a0, a1, val in segments:
        pct = 100 * val / total
        p.append(f'<rect x="{LEG_X}" y="{y - 8}" width="9" height="9" rx="2" '
                 f'fill="{COL[name][idx]}" stroke="{border}" stroke-width="0.6"/>')
        p.append(f'<text x="{LEG_X + 17}" y="{y}" font-family="{FONT}" font-size="11.5" '
                 f'fill="{text}">{html.escape(name)}</text>')
        p.append(f'<text x="{W - 16}" y="{y}" text-anchor="end" font-family="{FONT}" '
                 f'font-size="10.5" fill="{muted}">{pct:.1f}%</text>')
        y += 24
    p.append("</svg>")
    return "".join(p)


out = HERE.parent / "assets"
(out / "langs-dark.svg").write_text(
    card("#1A1B27", "#353A47", "#D8BD8A", "#C9D1D9", "#8B949E"))
(out / "langs-light.svg").write_text(
    card("#FFFFFF", "#DCDCDC", "#87683A", "#24292F", "#6E7781"))

print(f"rows={len(rows)} total={total:,}")
bad = 0
for n, v in rows:
    d, l = COL[n]
    cd, cl = contrast(d, "#1A1B27"), contrast(l, "#FFFFFF")
    flag = "" if min(cd, cl) >= 3.0 else "  <-- FAIL 3:1"
    bad += flag != ""
    print(f"  {n:<11} {100 * v / total:5.1f}%  dark {d} {cd:5.2f}:1   "
          f"light {l} {cl:5.2f}:1{flag}")
for f in ("langs-dark", "langs-light"):
    s = (out / f"{f}.svg").read_text()
    print(f"  {f}: {len(s)}B slices={s.count('<path')} text={s.count('<text')}")
raise SystemExit(1 if bad else 0)