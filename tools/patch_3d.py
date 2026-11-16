#!/usr/bin/env python3
"""Turn the 3D card's language pie into a legend for the 3D graph itself.

The upstream action (yoshi389111/github-profile-3d-contrib) always emits a
language pie + legend in the lower-left. We already have a language card
(tools/build_langs.py), so the pie is a duplicate -- and it counts
"Jupyter Notebook", which the language card deliberately skips because
notebooks commit rendered base64 PNG output.

What the card is actually missing is a key for the five contribution shades:
the 3D bars use contribColors[0..4] with nothing explaining them. So the pie's
corner becomes exactly that: "Less [swatch x5] More", the convention readers
already know from GitHub's own contribution graph.

Run as a post-process step after the action. Colours come from
profile-3d-settings.json, so dark and light stay in sync with the graph.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIE = '<g transform="translate(40, 520)"'   # the pie + its legend group
KEY = '<g class="contrib-legend">'          # the legend we insert


def _drop(s, needle):
    """Delete every balanced <g> subtree whose opening tag contains `needle`.

    Returns (text, count). String scan, not XML: the SVG carries no namespaces
    and re-serialising it would reorder attributes, breaking byte-comparison
    against the action's own output.
    """
    out, n, i = [], 0, 0
    while (j := s.find(needle, i)) != -1:
        out.append(s[i:j])
        d, k = 0, j
        while True:
            no, nc = s.find("<g", k), s.find("</g>", k)
            if nc == -1:
                raise ValueError(f"unbalanced <g> while dropping {needle!r}")
            if no != -1 and no < nc:
                d += 1
                k = no + 2
            else:
                d -= 1
                k = nc + 4
                if d == 0:
                    break
        i, n = k, n + 1
    return "".join(out) + s[i:], n


def legend(colors, cx=240, cy=676):
    """'Less [swatches] More' centred in the freed lower-left corner.

    The swatches must keep the graph's own shades -- that is the whole point of a
    key -- so the darkest one (#1f2430) sits at 1.10:1 against the ink card and
    would be an invisible box. The 1px border is what carries it: #6E7781 clears
    3:1 against both cards (3.76 dark / 4.55 light), so one stroke works for the
    pair instead of a per-theme variant.
    """
    sw, gap, x0 = 26, 30, cx + 52
    swatches = "".join(
        f'<rect x="{x0 + i * gap}" y="{cy - 13}" width="{sw}" height="{sw}" rx="3" '
        f'fill="{c}" stroke="#6E7781" stroke-width="1"/>'
        for i, c in enumerate(colors)
    )
    more = x0 + len(colors) * gap + 2
    return (f'{KEY}<text x="{cx}" y="{cy + 5}" class="fill-fg" font-size="13">Less</text>'
            f'{swatches}<text x="{more}" y="{cy + 5}" class="fill-fg" font-size="13">More</text></g>')


def main():
    settings = json.loads((ROOT / "profile-3d-settings.json").read_text())
    bad = 0
    for e in settings:
        p = ROOT / "profile-3d-contrib" / e["fileName"]
        if not p.exists():
            print(f"  {e['fileName']}: absent, skipped")
            continue
        s, had_key = _drop(p.read_text(), KEY)
        s, hit = _drop(s, PIE)
        if not hit:
            # second run: the pie is already gone. Only an error if we never
            # inserted a key either, i.e. upstream renamed the group.
            print(f"  {e['fileName']}: no pie group (already stripped)" if had_key
                  else f"  {e['fileName']}: WARNING no pie group found (upstream changed?)")
            bad += not had_key
        arcs = len(re.findall(r'stroke-width="2px"', s))
        if arcs:
            print(f"  {e['fileName']}: WARNING {arcs} pie arc(s) survived the strip")
            bad += 1
        s = s.replace("</svg>", legend(e["contribColors"]) + "</svg>")
        p.write_text(s)
        print(f"  {e['fileName']}: pie removed, legend added "
              f"(replaced {had_key} existing, {len(s)}B)")

    # the key must not become the new tofu: ASCII labels, exactly one legend
    for e in settings:
        p = ROOT / "profile-3d-contrib" / e["fileName"]
        if not p.exists():
            continue
        s = p.read_text()
        if not s.isascii():
            print(f"  {e['fileName']}: WARNING non-ASCII crept in")
            bad += 1
        n = s.count(KEY)
        if n != 1:
            print(f"  {e['fileName']}: WARNING {n} legends (expected 1)")
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())