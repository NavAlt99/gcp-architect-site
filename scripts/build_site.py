#!/usr/bin/env python3
"""Rebuild and validate the static site from an explicit roadmap source."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roadmap", default=os.environ.get("ROADMAP_PATH"), help="Path to the roadmap Markdown source")
    args = parser.parse_args()
    if not args.roadmap:
        parser.error("provide --roadmap or set ROADMAP_PATH")
    roadmap = Path(args.roadmap).expanduser().resolve()
    if not roadmap.is_file():
        parser.error(f"roadmap source does not exist: {roadmap}")
    print(f"Using roadmap source: {roadmap}")
    commands = [
        [sys.executable, str(SITE / "scripts" / "repair_site.py")],
        [sys.executable, str(SITE / "scripts" / "build_roadmap_content.py"), "--roadmap", str(roadmap)],
        [sys.executable, str(SITE / "scripts" / "validate_content.py")],
        [sys.executable, str(SITE / "scripts" / "test_diagrams.py")],
    ]
    for command in commands:
        result = subprocess.run(command, cwd=SITE.parent)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
