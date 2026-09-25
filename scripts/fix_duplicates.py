#!/usr/bin/env python3
"""
Fix Finding 1 from site-content-audit-v2.md:
- Remove 13x duplicated `div.compliance-addendum.part1-complete` blocks from Part 1.
- Remove 13x duplicated `div.compliance-addendum.depth-complete` blocks from Part 2A.

Topics 001–060 each have 14 copies of each block; we keep the first and drop the rest.
Topics 061–071 are already correct (1 copy each) and are skipped.
"""

from __future__ import annotations

import sys
from pathlib import Path

from bs4 import BeautifulSoup, Tag

SITE = Path(__file__).resolve().parents[1]
PAGES = SITE / "pages"


def remove_extra_duplicates(soup: BeautifulSoup, selector_classes: list[str]) -> int:
    """Find all elements that have ALL the given classes, keep first, remove the rest.
    Returns the number of elements removed."""
    # find_all with a list of classes finds elements that have ALL of those classes
    all_matches = soup.find_all(lambda tag: tag.name == "div" and all(
        cls in (tag.get("class") or []) for cls in selector_classes
    ))
    removed = 0
    for dup in all_matches[1:]:  # keep index 0, remove rest
        dup.decompose()
        removed += 1
    return removed


def fix_page(path: Path) -> tuple[int, int]:
    """Fix one page. Returns (part1_removed, depth_removed)."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(text, "html.parser")

    part1_removed = remove_extra_duplicates(soup, ["compliance-addendum", "part1-complete"])
    depth_removed = remove_extra_duplicates(soup, ["compliance-addendum", "depth-complete"])

    if part1_removed > 0 or depth_removed > 0:
        path.write_text(str(soup), encoding="utf-8")

    return part1_removed, depth_removed


def main() -> None:
    pages = sorted(PAGES.glob("topic-*.html"))
    total_part1 = 0
    total_depth = 0
    changed = 0

    for page_path in pages:
        p1, d1 = fix_page(page_path)
        if p1 > 0 or d1 > 0:
            print(f"  {page_path.name}: removed {p1} part1 dups, {d1} depth dups")
            total_part1 += p1
            total_depth += d1
            changed += 1
        else:
            print(f"  {page_path.name}: already clean")

    print()
    print(f"Done. {changed} pages updated.")
    print(f"  Part 1 blocks removed : {total_part1}")
    print(f"  Depth blocks removed  : {total_depth}")


if __name__ == "__main__":
    main()
