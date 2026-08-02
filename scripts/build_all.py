"""Regenerate every profile asset in dependency order.

    python scripts/build_all.py            # refresh art from the committed data
    python scripts/build_all.py --fetch    # also re-scrape the contribution graph
    python scripts/build_all.py --photo    # also re-cut the portrait matte

The portrait steps are opt-in because they need Pillow/rembg and only matter
when the source photo changes; CI just needs --fetch.
"""

from __future__ import annotations

import argparse
import runpy
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent


def run(name: str) -> None:
    print(f"\n==> {name}")
    runpy.run_path(str(SCRIPTS / name), run_name="__main__")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true", help="re-scrape GitHub contributions")
    parser.add_argument("--photo", action="store_true", help="re-cut the portrait and ASCII art")
    parser.add_argument("--all", action="store_true", help="shorthand for --fetch --photo")
    args = parser.parse_args()

    sys.path.insert(0, str(SCRIPTS))

    if args.fetch or args.all:
        run("fetch_contributions.py")
    if args.photo or args.all:
        run("prep_photo.py")
        run("make_ascii.py")

    run("make_profile_card.py")
    run("render_heatmap_svg.py")
    print("\nAll assets are up to date.")


if __name__ == "__main__":
    main()
