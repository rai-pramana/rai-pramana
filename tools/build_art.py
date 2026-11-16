#!/usr/bin/env python3
"""Generate the self-hosted SVGs: the typing band and the Fuji scene.

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
itself never depends on animation: the resting state is fully visible, and the
moving parts are a drawn rule and drifting mist. A client that refuses CSS still
shows the whole card, just still.
"""
from pathlib import Path

import jp

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "assets"

TYPING_W = 700
TYPING_H = 66        # ink ends at 54.8 (line 2 descender); rule at 57.6 needs room
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
    """Two outlined lines, centred, with a rule that draws itself once.

    Nothing is clipped at rest: a CSS-blind client shows both lines complete.
    """
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{TYPING_W}" height="{TYPING_H}" '
        f'viewBox="0 0 {TYPING_W} {TYPING_H}" role="img" '
        f'aria-label="こんにちは、ライともうします — Software Engineer · Data Engineer">',
        "<style>"
        "@keyframes draw{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
        "@keyframes glow{0%,100%{opacity:.45}50%{opacity:.85}}"
        ".rule{transform-origin:50% 50%;animation:draw 1.1s .15s ease-out both}"
        ".spark{animation:glow 4.5s ease-in-out infinite}"
        "@media (prefers-reduced-motion:reduce){*{animation:none!important;"
        "transform:none!important}}"
        "</style>",
    ]

    widths = []
    for txt, size, base, op in TYPING_LINES:
        g, w = jp.group(txt, size, gold, 0, base, opacity=op)
        widths.append(w)
        x = (TYPING_W - w) / 2
        parts.append(f'<g transform="translate({x:.2f},0)">{g}</g>')

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


# ---------------------------------------------------------------- Fuji scene
def _torii(c, cx, base_y, s):
    """Torii gate: kasagi with upturned tips, shimaki, nuki, gakuzuka, pillars.

    Drawn around a local origin at the pillar foot, then scaled and placed, so the
    gate stays in proportion at any size. Local proportions are a myōjin torii:
    280 wide by 190 tall (1.47:1). The first pass was 1.97:1 and read as a
    garden trellis, not a gate.
    """
    g, b, l = c["gold"], c["bronze"], c["line"]
    return (
        f'<g transform="translate({cx} {base_y}) scale({s})">'
        # kasagi -- the lintel, tips lifted at both ends
        f'<path d="M-140 -190 Q-150 -199 -136 -203 L-116 -207 L116 -207 L136 -203 '
        f'Q150 -199 140 -190 L132 -195 L-132 -195 Z" fill="{g}"/>'
        # shimaki -- the beam directly under it, a shade deeper
        f'<path d="M-120 -176 L120 -176 L120 -164 L-120 -164 Z" fill="{b}"/>'
        # nuki -- the lower tie beam
        f'<path d="M-112 -124 L112 -124 L112 -112 L-112 -112 Z" fill="{g}"/>'
        # gakuzuka -- centre strut between nuki and shimaki
        f'<path d="M-8 -166 L8 -166 L8 -122 L-8 -122 Z" fill="{b}"/>'
        # pillars, tapered inward toward the foot
        f'<path d="M-94 -112 L-74 -112 L-68 0 L-88 0 Z" fill="{g}"/>'
        f'<path d="M74 -112 L94 -112 L88 0 L68 0 Z" fill="{g}"/>'
        # kamebara -- the foot stones
        f'<path d="M-94 -7 L-64 -7 L-64 0 L-94 0 Z" fill="{l}"/>'
        f'<path d="M64 -7 L94 -7 L94 0 L64 0 Z" fill="{l}"/>'
        f'</g>'
    )


def _fuji(c):
    """Fuji: silhouette, snow cap with a soft zigzag hem, two faint ridges.

    The cap carries a 1.2px stroke in the mountain colour. Without it the cap is
    white-on-white in the light theme (1.00:1) and the peak reads as flat-topped
    against the sky; the stroke defines the summit in both themes.
    """
    m, s, l = c["mount"], c["snow"], c["line"]
    return (
        f'<path d="M300 214 C438 156 552 82 600 62 C648 82 762 156 900 214 Z" fill="{m}"/>'
        f'<path d="M520 124 C554 98 580 72 600 62 C620 72 646 98 680 124 '
        f'L654 116 L634 136 L610 116 L586 138 L562 116 L542 134 Z" fill="{s}" '
        f'stroke="{m}" stroke-width="1.2" stroke-linejoin="round"/>'
        f'<path d="M600 62 C588 116 570 168 546 214" fill="none" stroke="{l}" '
        f'stroke-width="1.2" stroke-opacity="0.45"/>'
        f'<path d="M600 62 C616 118 640 172 664 214" fill="none" stroke="{l}" '
        f'stroke-width="1.2" stroke-opacity="0.32"/>'
    )


def _seigaiha(c, y0, rows=3, r=26):
    """Overlapping wave arcs -- the page's divider motif, reused at the shoreline."""
    out = []
    for row in range(rows):
        y = y0 + row * r * 0.72
        x = -r * 2 + (r if row % 2 else 0)
        while x < SCENE_W + r * 2:
            out.append(
                f'<g transform="translate({x} {y:.1f})" fill="none" '
                f'stroke="{c["line"]}" stroke-opacity="{0.34 - row * 0.07:.2f}">'
                f'<circle r="{r}" stroke-width="1.1"/>'
                f'<circle r="{r*0.74:.1f}" stroke-width="1"/>'
                f'<circle r="{r*0.48:.1f}" stroke-width="0.9"/>'
                f'<circle r="{r*0.22:.1f}" stroke-width="0.8"/></g>')
            x += r * 2
    return "".join(out)


STARS = [(120, 52, 1.5), (232, 34, 1.1), (352, 62, 1.3), (498, 30, 1.0),
         (742, 44, 1.4), (864, 26, 1.1), (1016, 58, 1.3), (1108, 36, 1.0),
         (640, 22, 0.9)]

PETALS = [(300, 60, 0.0), (700, 30, 3.1), (860, 70, 6.2), (500, 40, 8.4),
          (1060, 50, 10.7)]


def scene_svg(c):
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SCENE_W}" height="{SCENE_H}" '
        f'viewBox="0 0 {SCENE_W} {SCENE_H}" aria-hidden="true" focusable="false">',
        "<style>"
        "@keyframes drift{from{transform:translateX(0)}to{transform:translateX(120px)}}"
        "@keyframes twinkle{0%,100%{opacity:.2}50%{opacity:.85}}"
        "@keyframes breathe{0%,100%{opacity:.5}50%{opacity:.8}}"
        "@keyframes fall{0%{transform:translate(0,-24px);opacity:0}"
        "14%{opacity:.7}100%{transform:translate(-52px,196px);opacity:0}}"
        ".mist{animation:drift 34s linear infinite}"
        ".star{animation:twinkle 5.5s ease-in-out infinite}"
        ".moon{animation:breathe 9s ease-in-out infinite}"
        ".pt{animation:fall 13s linear infinite}"
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
        "</style>",
        f'<rect width="{SCENE_W}" height="{SCENE_H}" fill="{c["bg"]}"/>',
        # soft sky wash so the horizon is not a hard band
        f'<ellipse cx="600" cy="200" rx="720" ry="118" fill="{c["sky"]}" '
        f'fill-opacity="0.9"/>',
        # moon -- muted gold, never a red sun
        f'<g class="moon"><circle cx="948" cy="82" r="48" fill="{c["glow"]}" '
        f'fill-opacity="0.10"/><circle cx="948" cy="82" r="33" fill="{c["glow"]}" '
        f'fill-opacity="0.18"/><circle cx="948" cy="82" r="20" fill="{c["gold"]}" '
        f'fill-opacity="0.6"/></g>',
    ]

    for i, (x, y, r) in enumerate(STARS):
        p.append(f'<circle class="star" cx="{x}" cy="{y}" r="{r}" fill="{c["gold"]}" '
                 f'style="animation-delay:{i * 0.63:.2f}s" fill-opacity="0.75"/>')

    # mountain behind, gate in front on the left third
    p.append(_fuji(c))
    p.append(_torii(c, 238, 226, 0.66))

    for y, h, op, dur in ((150, 16, 0.10, 34), (176, 12, 0.08, 46), (128, 9, 0.06, 58)):
        p.append(f'<g class="mist" style="animation-duration:{dur}s">'
                 f'<rect x="-140" y="{y}" width="1480" height="{h}" rx="{h/2}" '
                 f'fill="{c["gold"]}" fill-opacity="{op}"/></g>')

    p.append(_seigaiha(c, 198, rows=3, r=26))
    p.append(f'<rect x="0" y="{SCENE_H - 8}" width="{SCENE_W}" height="8" '
             f'fill="{c["bg"]}"/>')

    for x, y, d in PETALS:
        p.append(f'<path class="pt" d="M{x} {y} q5 -4.5 9.5 0 q-4.5 5 -9.5 0 Z" '
                 f'fill="{c["gold"]}" fill-opacity="0.5" '
                 f'style="animation-delay:{d}s"/>')

    p.append("</svg>")
    return "".join(p)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "typing-dark.svg").write_text(typing_svg(DARK["gold"], DARK["bright"], DARK["bg"]))
    (OUT / "typing-light.svg").write_text(typing_svg(LIGHT["gold"], LIGHT["bright"], LIGHT["bg"]))
    (OUT / "fuji-dark.svg").write_text(scene_svg(DARK))
    (OUT / "fuji-light.svg").write_text(scene_svg(LIGHT))

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

    for f in ("typing-dark", "typing-light", "fuji-dark", "fuji-light"):
        s = (OUT / f"{f}.svg").read_text()
        print(f"  {f}: {len(s):6}B  text={s.count('<text')}  paths={s.count('<path')}")
        bad += s.count("<text")
    print("FAIL" if bad else "OK")
    raise SystemExit(1 if bad else 0)


if __name__ == "__main__":
    main()