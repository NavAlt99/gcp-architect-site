#!/usr/bin/env python3
"""Fast, dependency-free diagram integration checks."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
DIAGRAMS = SITE / "diagrams"


def main() -> int:
    errors: list[str] = []
    html_files = sorted(DIAGRAMS.glob("*.html"))
    for path in html_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "../assets/diagram-engine.js" not in text:
            errors.append(f"{path.name}: missing shared engine")
        if "new DiagramEngine('standalone-diagram'" not in text and 'new DiagramEngine("standalone-diagram"' not in text:
            errors.append(f"{path.name}: missing engine initialization")
        spec_path = path.with_suffix(".json")
        if not spec_path.exists():
            errors.append(f"{path.name}: missing JSON source")
            continue
        try:
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{spec_path.name}: {exc}")
            continue
        if not spec.get("id") or not spec.get("summary"):
            errors.append(f"{spec_path.name}: missing id or summary")
    engine = SITE / "assets" / "diagram-engine.js"
    result = subprocess.run(["node", "--check", str(engine)], capture_output=True, text=True)
    if result.returncode:
        errors.append("diagram-engine.js: node --check failed: " + result.stderr.strip())
    if errors:
        print(f"FAIL: {len(errors)} diagram test errors")
        print("\n".join(" - " + error for error in errors[:80]))
        return 1
    print(f"PASS: {len(html_files)} standalone diagrams and shared engine")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
