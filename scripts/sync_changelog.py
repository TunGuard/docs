#!/usr/bin/env python3
"""Generate content/<lang>/changelog.md from the binary repo's CHANGELOG.md.

The documentation lives in a separate repository from the code, so the
changelog is pulled in at build time instead of being duplicated by hand. Run
without arguments to use the changelog from the default branch, or pass
``--ref`` to pin a release tag:

    python scripts/sync_changelog.py --ref v2.4.18
"""
from __future__ import annotations

import argparse
import pathlib
import urllib.error
import urllib.request

REPOSITORY = "TunGuard/tanguard-binary"
LANGUAGES = ("en", "fr", "es")
ROOT = pathlib.Path(__file__).resolve().parent.parent


def download(ref: str) -> str:
    url = f"https://raw.githubusercontent.com/{REPOSITORY}/{ref}/CHANGELOG.md"
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read().decode("utf-8")


def render(changelog: str) -> str:
    lines = changelog.splitlines()
    # Drop the leading "# Changelog" heading: the page title comes from the
    # front matter below, so keeping it would render a duplicate heading.
    if lines and lines[0].strip().lower() == "# changelog":
        lines = lines[1:]
    body = "\n".join(lines).strip("\n")
    return f"---\ntitle: Changelog\n---\n\n{body}\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ref",
        default="main",
        help=f"git ref of {REPOSITORY} to read CHANGELOG.md from (default: main)",
    )
    args = parser.parse_args()

    try:
        changelog = download(args.ref)
    except (urllib.error.HTTPError, urllib.error.URLError) as error:
        raise SystemExit(f"failed to fetch CHANGELOG.md for {args.ref}: {error}")

    page = render(changelog)
    for language in LANGUAGES:
        target = ROOT / "content" / language / "changelog.md"
        target.write_text(page, encoding="utf-8")
        print(f"wrote {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
