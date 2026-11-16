#!/usr/bin/env python3
"""勢い · Momentum -- 12-month contribution activity, drawn from real data.

Replaces the decorative Fuji scene with a widget that answers a question:
"how has this account actually been used?" The bars are real contribution
counts pulled from the GitHub GraphQL API, bucketed by calendar month.

Rules, same as the rest of the drawn assets:
  · dual theme, emitted as two files selected by <picture>
  · one warm hue family (gold -> bronze -> cream), no saturated accents
  · Japanese is NOT drawn here -- the section heading is HTML, so no viewer
    font can turn it into tofu. This file contains no <text> at all except
    the ASCII month initials, which every font on earth has.
  · decorative furniture is aria-hidden; the numbers it encodes are stated
    in the alt text, which is the accessible path for a chart image.

Data source: tools/data/contrib.json, refreshed by tools/fetch_contrib.py.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
DATA = ROOT / "tools" / "data" / "contrib.json"

W, H = 1200, 260
PAD_L, PAD_R, PAD_T, PAD_B = 92, 40, 34, 46
N_MONTHS = 13

DARK = {
    "bg": "#1A1B27",
    "grid": "#2A2E3C",
    "axis": "#4A5162",
    "label": "#8B949E",
    "value": "#C9D1D9",
    "bars": ["#8A6F45", "#A97E3E", "#CEAF6A", "#E3D8B8"],  # bronze -> cream, all >=3.6:1
    "peak": "#F2E9D8",
}
LIGHT = {
    "bg": "#FFFFFF",
    "grid": "#E6E1D6",
    "axis": "#B9AE97",
    "label": "#6E7781",
    "value": "#24292F",
    "bars": ["#3A2A14", "#5E4720", "#926536", "#A97E3E"],  # dark -> mid, all >=3.66:1
    "peak": "#1B1611",
}

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _lum(h: str) -> float:
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a: str, b: str) -> float:
    l1, l2 = sorted((_lum(a), _lum(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def load_series() -> list[tuple[str, int]]:
    """[(YYYY-MM, contributions), ...] ascending, from the cached API dump."""
    raw = json.loads(DATA.read_text())
    cal = raw["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    buckets: dict[str, int] = {}
    for week in cal["weeks"]:
        for day in week["contributionDays"]:
            key = day["date"][:7]
            buckets[key] = buckets.get(key, 0) + day["contributionCount"]
    series = sorted(buckets.items())
    return series[-N_MONTHS:]


def _bar_tone(i: int, n: int, peak: bool, c: dict) -> str:
    if peak:
        return c["peak"]
    # older months sit further down the ramp, so the eye lands on recent work
    slot = int(i / max(1, n - 1) * (len(c["bars"]) - 1))
    return c["bars"][slot]


def momentum_svg(c: dict, series: list[tuple[str, int]]) -> str:
    n = len(series)
    counts = [v for _, v in series]
    top = max(counts) if counts else 1
    peak_i = counts.index(top) if top else 0

    plot_w = W - PAD_L - PAD_R
    plot_h = H - PAD_T - PAD_B
    base_y = PAD_T + plot_h
    slot = plot_w / n
    bw = min(58.0, slot * 0.58)

    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="Monthly contribution activity, last {n} months">',
        f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>',
    ]

    # horizontal rules at 0 / 50 / 100 % of the peak, dashed and quiet
    for frac in (0.0, 0.5, 1.0):
        y = base_y - plot_h * frac
        dash = ' stroke-dasharray="3 5"' if frac else ""
        p.append(f'<line x1="{PAD_L}" y1="{y:.1f}" x2="{W - PAD_R}" y2="{y:.1f}" '
                 f'stroke="{c["grid"] if frac else c["axis"]}" stroke-width="1"{dash}/>')
        if frac:
            p.append(
                f'<text x="{PAD_L - 14}" y="{y + 4:.1f}" fill="{c["label"]}" '
                f'font-size="11" font-family="ui-monospace,SFMono-Regular,'
                f'Menlo,Consolas,monospace" text-anchor="end">'
                f'{int(top * frac)}</text>')

    for i, ((month, count),) in enumerate(zip(series)):
        h = plot_h * (count / top) if top else 0
        x = PAD_L + slot * i + (slot - bw) / 2
        y = base_y - h
        peak = i == peak_i
        p.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{max(h, 1.5):.1f}" '
            f'rx="2" fill="{_bar_tone(i, n, peak, c)}">'
            f'<title>{month}: {count}</title></rect>')

        # month initial -- ASCII on purpose, see module docstring
        p.append(
            f'<text x="{x + bw / 2:.1f}" y="{base_y + 18}" fill="{c["label"]}" '
            f'font-size="11" font-family="ui-monospace,SFMono-Regular,Menlo,'
            f'Consolas,monospace" text-anchor="middle">{MONTHS[int(month[5:7]) - 1]}</text>')

        if peak:
            p.append(
                f'<text x="{x + bw / 2:.1f}" y="{y - 9:.1f}" fill="{c["value"]}" '
                f'font-size="12" font-weight="600" font-family="ui-monospace,'
                f'SFMono-Regular,Menlo,Consolas,monospace" text-anchor="middle">'
                f'{count}</text>')

    p.append("</svg>")
    return "".join(p)


def alt_text(series: list[tuple[str, int]]) -> str:
    counts = [v for _, v in series]
    total = sum(counts)
    peak_i = counts.index(max(counts))
    m, v = series[peak_i]
    return (f"Monthly contribution activity for the last {len(series)} months, "
            f"{total} contributions total. Busiest month {MONTHS[int(m[5:7]) - 1]} "
            f"{m[:4]} with {v}.")


def main() -> int:
    series = load_series()
    if not series:
        print("FAIL: no contribution data")
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    for name, c in (("dark", DARK), ("light", LIGHT)):
        (OUT / f"momentum-{name}.svg").write_text(momentum_svg(c, series))

    bad = 0
    # every bar tone must clear 3:1 against its card background (WCAG 1.4.11)
    for name, c in (("dark", DARK), ("light", LIGHT)):
        worst = min(contrast(t, c["bg"]) for t in c["bars"] + [c["peak"]])
        ok = worst >= 3.0
        bad += not ok
        print(f"  {name:5} worst bar vs bg {worst:5.2f}:1  {'OK' if ok else 'FAIL'}")
        # axis text must clear AA for small text
        for role in ("label", "value"):
            r = contrast(c[role], c["bg"])
            ok = r >= 4.5
            bad += not ok
            print(f"  {name:5} {role:5} text vs bg {r:5.2f}:1  "
                  f"{'AA' if ok else 'FAIL'}")

    for f in ("momentum-dark", "momentum-light"):
        s = (OUT / f"{f}.svg").read_text()
        # 13 month labels + 2 axis ticks + 1 peak label; anything else is a bug
        want = len(series) + 3
        got = s.count("<text")
        ok = got == want
        bad += not ok
        print(f"  {f}: {len(s):6}B  text={got} (want {want})  "
              f"rect={s.count('<rect')}  {'OK' if ok else 'FAIL'}")

        # no CJK anywhere in this file: the section heading carries the Japanese
        nonascii = [c for c in s if ord(c) > 127]
        ok = not nonascii
        bad += not ok
        print(f"  {f}: non-ASCII chars={len(nonascii)}  "
              f"{'ASCII-only OK' if ok else 'FAIL'}")

        # every <text> must be monospaced -- the only family we rely on here
        ok = s.count("ui-monospace") >= got
        bad += not ok
        print(f"  {f}: monospace declarations={s.count('ui-monospace')}  "
              f"{'OK' if ok else 'FAIL'}")

    print("FAIL" if bad else "OK")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())