#!/usr/bin/env python3
"""Refresh tools/data/contrib.json from the GitHub GraphQL API.

Usage:
    gh auth status          # must be authenticated
    python3 tools/fetch_contrib.py

Writes the raw contribution calendar so build_momentum.py never has to hit
the network at render time. Keeps the dump small -- it stores only the
fields the widget needs.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tools" / "data" / "contrib.json"

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def main() -> int:
    login = subprocess.run(
        ["gh", "api", "user", "--jq", ".login"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()

    proc = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={QUERY}", "-F", f"login={login}"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        print(proc.stderr.strip(), file=sys.stderr)
        return 1

    payload = json.loads(proc.stdout)
    cal = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload))
    print(f"{login}: {cal['totalContributions']} contributions, "
          f"{len(cal['weeks'])} weeks -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())