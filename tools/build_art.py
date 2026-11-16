#!/usr/bin/env python3
"""Generate the self-hosted SVGs: the typing band.

Two rules from the README apply here:

  · No <text> anywhere. Every glyph is an outlined <path> (see tools/jp.py), so
    Japanese cannot render as tofu on any viewer. The old readme-typing-svg badge
    asked for `font=Zen Maru Gothic` but embedded nothing -- @font-face count 0,
    base64 count 0 -- so it fell through to `monospace`, which has no CJK, and
    boxed up everywhere. Outlining removes the whole class of failure.

  · Every colour clears 3:1 against its own card background (WCAG 1.4.11) and
    body text clears 4.5:1 (1.4.3). The table at the bottom of main() enforces it.

Animation is CSS inside the SVG, which survives GitHub's camo proxy and <img>
embedding -- seigaiha-dark.svg has been drifting that way for months. The text
itself never depends on animation: each glyph is a path whose only animated
property is opacity, and its default is 1, so a client that refuses CSS shows
the whole card, just still. There is deliberately no caret: it would sit in the
wrong place once the last glyph lands.

The charts live in siblings: build_langs.py (language donut) and
build_momentum.py (monthly activity). This file is only the band.
"""
from pathlib import Path

import jp

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "assets"

TYPING_W = 700
TYPING_H = 66        # ink ends at 54.8 (line 2 descender); rule at 57.6 needs room
CHAR_MS = 62         # per-glyph delay; ~16 chars/line reads as typing, not a wipe
LINE_MS = 260        # pause between the two lines
SCENE_W, SCENE_H = 1200, 260

DARK = dict(bg="#1A1B27", sky="#141520", gold="#D8BD8A", bright="#F0E3C4",
            bronze="#B08D57", line="#6F5C3C", soft="#8B949E", mount="#424958",
            snow="#E9E4D8", glow="#D8BD8A")
LIGHT = dict(bg="#FFFFFF", sky="#FAF6EC", gold="#87683A", bright="#5E4423",
             bronze="#A98F5B", line="#C9B48C", soft="#6E7781", mount="#C9BA98",
             snow="#FFFFFF", glow="#D8BD8A")

# (text, px size, baseline y, opacity)
TYPING_LINES = [
    ("こんにちは、ライともうします", 24, 26, 1.0),
    ("Software Engineer · Data Engineer", 20, 50, 0.86),
]
RULE_Y = 57.6          # sits below line 2's descender box (50 + 4.8 = 54.8)


def _lum(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    l1, l2 = sorted((_lum(a), _lum(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


# ---------------------------------------------------------------- typing band
def typing_svg(gold, bright, bg):
    """Two outlined lines that type themselves, centred, with a rule that draws.

    Each glyph is a <path> with its own animation-delay, so the band types on
    instead of appearing whole. The reveal animates OPACITY ONLY, and the
    default (no-CSS) value is opacity 1 -- a client that strips <style> shows
    both lines complete instead of blank, which is the failure mode a
    `visibility:hidden` + `forwards` approach would have. No caret: it would sit
    in the wrong place once the last glyph lands, and a cursor that has to be
    hidden after typing is one more thing that can break in a static renderer.
    """
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{TYPING_W}" height="{TYPING_H}" '
        f'viewBox="0 0 {TYPING_W} {TYPING_H}" role="img" '
        f'aria-label="{TYPING_LINES[0][0]} — {TYPING_LINES[1][0]}">',
        "<style>"
        "@keyframes type{from{opacity:0}to{opacity:1}}"
        "@keyframes draw{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
        "@keyframes glow{0%,100%{opacity:.45}50%{opacity:.85}}"
        "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}"
        ".ch{animation:type .01s linear both}"
        ".rule{transform-origin:50% 50%;animation:draw 1.1s .15s ease-out both}"
        ".spark{animation:glow 4.5s ease-in-out infinite}"
        "@media (prefers-reduced-motion:reduce){*{animation:none!important;"
        "transform:none!important}}"
        "</style>",
    ]

    widths, clock = [], 0.0
    for txt, size, base, op in TYPING_LINES:
        glyphs, w = jp.runs(txt, size)
        widths.append(w)
        x = (TYPING_W - w) / 2
        body = "".join(
            f'<path class="ch" style="animation-delay:{clock + i * CHAR_MS:.0f}ms" '
            f'd="{d}"/>'
            for i, (d, _) in enumerate(glyphs)
        )
        parts.append(
            f'<g transform="translate({x:.2f},{base})" fill="{gold}" '
            f'fill-opacity="{op}">{body}</g>')
        clock += len(glyphs) * CHAR_MS + LINE_MS

    # hairline under the block, exactly as wide as the wider line
    half = max(widths) / 2
    parts.append(
        f'<g class="rule"><rect x="{TYPING_W/2 - half:.2f}" y="{RULE_Y:.2f}" '
        f'width="{half*2:.2f}" height="1.1" rx="0.55" fill="{bright}" '
        f'fill-opacity="0.45"/></g>')
    # one gold ember riding the rule, breathing rather than blinking
    parts.append(f'<circle class="spark" cx="{TYPING_W/2:.1f}" cy="{RULE_Y + 0.55:.2f}" r="1.6" '
                 f'fill="{bright}" fill-opacity="0.9"/>')
    parts.append("</svg>")
    return "".join(parts)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "typing-dark.svg").write_text(typing_svg(DARK["gold"], DARK["bright"], DARK["bg"]))
    (OUT / "typing-light.svg").write_text(typing_svg(LIGHT["gold"], LIGHT["bright"], LIGHT["bg"]))

    bad = 0
    for name, fg, bg in (("gold on ink", DARK["gold"], DARK["bg"]),
                         ("bronze on ink", DARK["bronze"], DARK["bg"]),
                         ("soft on ink", DARK["soft"], DARK["bg"]),
                         ("gold on white", LIGHT["gold"], LIGHT["bg"]),
                         ("soft on white", LIGHT["soft"], LIGHT["bg"])):
        c = contrast(fg, bg)
        ok = c >= 4.5
        bad += not ok
        print(f"  {name:16} {fg} on {bg}  {c:5.2f}:1  {'AA' if ok else 'FAIL'}")

    for f in ("typing-dark", "typing-light"):
        s = (OUT / f"{f}.svg").read_text()
        print(f"  {f}: {len(s):6}B  text={s.count('<text')}  paths={s.count('<path')}")
        bad += s.count("<text")
    print("FAIL" if bad else "OK")
    raise SystemExit(1 if bad else 0)


if __name__ == "__main__":
    main()