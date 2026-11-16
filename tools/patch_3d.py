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
PIE = '<g transform="translate(40, 520)">'   # the pie + its legend group


def strip_pie(s):
    """Delete the depth-1 <g> subtree that starts at PIE."""
    i = s.find(PIE)
    if i == -1:
        return s, False
    d, j = 0, i
    while True:
        no, nc = s.find("<g", j), s.find("</g>", j)
        if nc == -1:
            raise ValueError("unbalanced <g> while stripping the pie")
        if no != -1 and no < nc:
            d += 1
            j = no + 2
        else:
            d -= 1
            j = nc + 4
            if d == 0:
                return s[:i] + s[j:], True


def legend(colors, cx=240, cy=676):
    """'Less [swatches] More' centred in the freed lower-left corner.

    The swatches must keep the graph's own shades -- that is the whole point of a
    key -- so the darkest one (#1f2430) sits at 1.10:1 against the ink card and
    would be an invisible box. The 1px border is what carries it: #6E7781 clears
    3:1 against both cards (3.76 dark / 4.55 light), so one stroke works for the
    pair instead of a per-theme variant.
    """
    sw, gap = 26, 30
    x0 = cx + 52
    parts = [f'<text x="{cx}" y="{cy + 5}" class="fill-fg" font-size="13">Less</text>']
    for i, c in enumerate(colors):
        parts.append(
            f'<rect x="{x0 + i * gap}" y="{cy - 13}" width="{sw}" height="{sw}" rx="3" '
            f'fill="{c}" stroke="#6E7781" stroke-width="1"/>'
        )
    parts.append(
        f'<text x="{x0 + len(colors) * gap + 2}" y="{cy + 5}" class="fill-fg" '
        f'font-size="13">More</text>'
    )
    return '<g class="contrib-legend">' + "".join(parts) + '</g>'


def strip_legend(s):
    """Remove an already-inserted legend so the step can run twice safely."""
    out, n = [], 0
    i = 0
    while True:
        j = s.find('<g class="contrib-legend">', i)
        if j == -1:
            out.append(s[i:])
            break
        out.append(s[i:j])
        d, k = 0, j
        while True:
            no, nc = s.find("<g", k), s.find("</g>", k)
            if nc == -1:
                raise ValueError("unbalanced <g> while stripping the legend")
            if no != -1 and no < nc:
                d += 1
                k = no + 2
            else:
                d -= 1
                k = nc + 4
                if d == 0:
                    break
        i = k
        n += 1
    return "".join(out), n


def main():
    settings = json.loads((ROOT / "profile-3d-settings.json").read_text())
    bad = 0
    for entry in settings:
        name = entry["fileName"]
        p = ROOT / "profile-3d-contrib" / name
        if not p.exists():
            print(f"  {name}: absent, skipped")
            continue
        s = p.read_text()
        s, had_legend = strip_legend(s)
        s, hit = strip_pie(s)
        if not hit:
            # run twice and the pie is already gone -- normal, not an error
            print(f"  {name}: no pie group (already stripped)" if had_legend
                  else f"  {name}: WARNING no pie group found (upstream changed?)")
            if not had_legend:
                bad += 1
        arcs = len(re.findall(r'stroke-width="2px"', s))
        if arcs:
            print(f"  {name}: WARNING {arcs} pie arc(s) survived the strip")
            bad += 1
        s = s.replace("</svg>", legend(entry["contribColors"]) + "</svg>")
        p.write_text(s)
        print(f"  {name}: pie removed, legend added "
              f"(replaced {had_legend} existing, {len(s)}B)")

    # the legend must not become the new tofu: ASCII labels only
    for entry in settings:
        p = ROOT / "profile-3d-contrib" / entry["fileName"]
        if p.exists():
            s = p.read_text()
            if not s.isascii():
                print(f"  {entry['fileName']}: WARNING non-ASCII crept in")
                bad += 1
            if s.count('class="contrib-legend"') != 1:
                print(f"  {entry['fileName']}: WARNING "
                      f"{s.count('class=' + chr(34) + 'contrib-legend' + chr(34))} legends")
                bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())