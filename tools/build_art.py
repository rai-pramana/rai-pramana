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
embedding -- seigaiha-dark.svg has been drifting that way for months. The two
lines take turns typing themselves forever: each line types in, holds, fades,
and the other line follows. The text never depends on animation: every glyph is
a path whose only animated property is opacity, and its default is 1, so a
client that refuses CSS shows the whole card, just still. There is deliberately
no caret: it would sit in the wrong place once the last glyph lands.

The charts live in siblings: build_langs.py (language donut) and
build_momentum.py (monthly activity). This file is only the band.
"""
from pathlib import Path

import jp

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "assets"

TYPING_W = 700
TYPING_H = 66        # ink ends at 54.8 (line 2 descender); rule at 57.6 needs room
SCENE_W, SCENE_H = 1200, 260

# The band is one row that changes text, not two rows that alternate: it reads
# as a headline cycling, which is what readme-typing-svg's `lines=` does.
#
# (text, px size, bold)
TYPING_FRAMES = [
    ("Rai Pramana's GitHub Stats", 28, True),
    ("ライ・プラマニのGitHub統計", 28, True),
]

# How long each frame reads before the next one takes over. The typing itself is
# derived from glyph count, so a longer line simply types for longer.
HOLD_MS = 1000        # pause after a line finishes -- the reference's `pause=1000`
CHAR_MS = 45          # per-glyph reveal
CLEAR_MS = 260        # fade the old line out before the new one types
BASELINE = 40         # one row, vertically centred in the 66px band
RULE_Y = 57.6          # sits below the descender box (40 + 4.8 = 44.8... see main)

DARK = dict(bg="#1A1B27", sky="#141520", gold="#D8BD8A", bright="#F0E3C4",
            bronze="#B08D57", line="#6F5C3C", soft="#8B949E", mount="#424958",
            snow="#E9E4D8", glow="#D8BD8A")
LIGHT = dict(bg="#FFFFFF", sky="#FAF6EC", gold="#87683A", bright="#5E4423",
             bronze="#A98F5B", line="#C9B48C", soft="#6E7781", mount="#C9BA98",
             snow="#FFFFFF", glow="#D8BD8A")

RULE_Y = 57.6          # sits below the row's descender box (40 + 21.3 = 61.3 -- see main)


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
    """One outlined row that types itself, holds, then types the next line.

    This is the readme-typing-svg `lines=` behaviour -- a single headline that
    cycles through two strings -- rebuilt without <text>. The reference does it
    with `<text font-family="Noto Sans Japanese">`, which is one missing font
    away from tofu: the browser resolves that family to whatever monospace it
    has, and a box without a CJK face draws ライ as boxes. Outlining each glyph
    removes the dependency entirely.

    Each glyph is a <path> with its own reveal keyframe; each line is a <g>
    whose opacity window is the line's turn. The reveal animates OPACITY ONLY
    and defaults to 1, so a client that strips <style> shows the first line
    complete instead of a blank band.

    There is deliberately no caret: it would sit in the wrong place once the
    last glyph lands, and hiding it afterwards is one more thing that can break
    in a renderer that never runs the animation.
    """
    # Time is laid out per line: type, hold, then a short clear so the handover
    # does not snap. One cycle is the sum, and every animation is that same
    # cycle length, so the whole band loops without JS or a shared clock.
    spans, clock = [], 0.0
    for txt, size, bold in TYPING_FRAMES:
        n = len(jp.runs(txt, size, bold)[0])
        type_ms = n * CHAR_MS
        spans.append(dict(start=clock, n=n, type_ms=type_ms, type_end=clock + type_ms,
                          hold_end=clock + type_ms + HOLD_MS,
                          end=clock + type_ms + HOLD_MS + CLEAR_MS))
        clock = spans[-1]["end"]
    cycle = clock

    pct = lambda ms: f"{ms / cycle * 100:.3f}%"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{TYPING_W}" height="{TYPING_H}" '
        f'viewBox="0 0 {TYPING_W} {TYPING_H}" role="img" '
        f'aria-label="{TYPING_FRAMES[0][0]} — {TYPING_FRAMES[1][0]}">',
        "<style>"
        "@keyframes draw{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
        "@keyframes glow{0%,100%{opacity:.45}50%{opacity:.85}}",
    ]

    # The window: hidden outside the line's turn, visible inside it, then a
    # short fade so the handover does not snap. The "hidden" stop gets its own
    # offset -- merging it with 0% (`0%,52%{opacity:0}` then `52%{opacity:1}`)
    # leaves Chrome one stop valued 1 at 52%, so it ramps the line up across
    # its whole off-turn and the text shows faintly before its turn.
    for i, s in enumerate(spans):
        hidden = f"{pct(s['start'])}{{opacity:0}}" if s["start"] > 0 else ""
        parts.append(
            f"@keyframes w{i}{{"
            f"0%{{opacity:0}}"
            + hidden
            + f"{pct(s['start'] + 1)}{{opacity:1}}"
            f"{pct(s['hold_end'])}{{opacity:1}}"
            f"{pct(s['end'])}{{opacity:0}}"
            f"100%{{opacity:0}}}}")

    # The reveal: one @keyframes per glyph, each flipping to 1 at its own
    # millisecond. A per-glyph keyframe rather than a negative animation-delay
    # -- a negative delay makes every glyph read as already-typed on frame 0,
    # which is exactly the stagger the loop needs to keep.
    reveal = "".join(
        f"@keyframes g{i}_{k}{{0%,{pct(s['start'] + k * CHAR_MS)}{{opacity:0}}"
        f"{pct(s['start'] + k * CHAR_MS + 1)}{{opacity:1}}100%{{opacity:1}}}}"
        for i, s in enumerate(spans)
        for k in range(s["n"])
    )
    parts.append(
        reveal
        + ".rule{transform-origin:50% 50%;animation:draw 1.1s .15s ease-out both}"
        ".spark{animation:glow 4.5s ease-in-out infinite}"
        # No opacity:1 here on purpose. The lines share one row, so forcing
        # everything visible would stack line 1 on top of line 0 -- a client
        # that honours reduced motion would get an unreadable double exposure.
        # With animation off, each line falls back to its presentation
        # attribute: line 0 (no attribute) shows, line 1 (opacity="0") does not.
        "@media (prefers-reduced-motion:reduce){*{animation:none!important;"
        "transform:none!important}}"
        "</style>",
    )

    for i, (txt, size, bold) in enumerate(TYPING_FRAMES):
        glyphs, w = jp.runs(txt, size, bold)
        x = (TYPING_W - w) / 2          # each line centred on its own width
        body = "".join(
            f'<path class="ch" style="animation:g{i}_{k} {cycle:.0f}ms '
            f'linear infinite" d="{d}"/>'
            for k, (d, _) in enumerate(glyphs)
        )
        # The presentation attribute is the static fallback, and it must not be
        # 1 for every line: they occupy the same row. CSS animation overrides
        # the attribute, so the cycling still works; with CSS gone, only line 0
        # is left standing.
        op = "" if i == 0 else ' opacity="0"'
        parts.append(
            f'<g transform="translate({x:.2f},{BASELINE})" fill="{gold}"{op} '
            f'style="animation:w{i} {cycle:.0f}ms linear infinite">{body}</g>')

    # hairline under the row, exactly as wide as the wider line
    half = max(jp.layout(t, s, b)[1] for t, s, b in TYPING_FRAMES) / 2
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