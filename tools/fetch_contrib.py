#!/usr/bin/env python3
"""Refresh tools/data/contrib.json from the GitHub GraphQL API.

Usage:
    GITHUB_TOKEN=... python3 tools/fetch_contrib.py     # Actions
    python3 tools/fetch_contrib.py                      # local, needs gh auth

Writes the raw contribution calendar so build_momentum.py never has to hit
the network at render time. Keeps the dump small -- it stores only the
fields the widget needs.

Talks to the API over plain HTTPS rather than shelling out to `gh`: the CLI
is present on GitHub runners but not guaranteed, and it also wants its own
auth dance. The token is all we ever needed.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tools" / "data" / "contrib.json"
API = "https://api.github.com"

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


def token() -> str:
    """GITHUB_TOKEN (Actions) or GH_TOKEN, falling back to `gh auth token`."""
    for var in ("GITHUB_TOKEN", "GH_TOKEN"):
        if os.environ.get(var):
            return os.environ[var]
    try:
        return subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, check=True
        ).stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        sys.exit(
            "no GitHub token: set GITHUB_TOKEN, or run `gh auth login` first\n"
            f"  ({exc})"
        )


def api(path: str, tok: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        f"{API}/{path}",
        data=data,
        headers={
            "Authorization": f"Bearer {tok}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "momentum-chart-builder",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        sys.exit(f"GitHub API {path} failed: HTTP {exc.code}\n{exc.read().decode()[:400]}")


def main() -> int:
    tok = token()

    login = api("user", tok)["login"]

    payload = api("graphql", tok, {"query": QUERY, "variables": {"login": login}})
    if "errors" in payload:
        sys.exit(f"graphql errors: {payload['errors']}")

    cal = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload))
    print(f"{login}: {cal['totalContributions']} contributions, "
          f"{len(cal['weeks'])} weeks -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())