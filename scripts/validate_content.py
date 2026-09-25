#!/usr/bin/env python3
"""Static contract checks for the generated GCP Architect learning site."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

SITE = Path(__file__).resolve().parents[1]
PAGES = SITE / "pages"
DIAGRAMS = SITE / "diagrams"
GENERATED = SITE / "generated"
sys.path.insert(0, str(Path(__file__).parent))
from repair_site import EXPECTED, page_meta  # noqa: E402


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def local_target(base: Path, value: str) -> Path | None:
    if not value or value.startswith(("#", "data:", "mailto:", "javascript:")):
        return None
    parsed = urlparse(value)
    if parsed.scheme or parsed.netloc:
        return None
    return (base / parsed.path).resolve()


def validate() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []
    pages = sorted(PAGES.glob("topic-*.html"))
    home_text = (SITE / "index.html").read_text(encoding="utf-8", errors="ignore")
    if "The Depth Ladder: Conceptual Architecture" not in home_text or 'id="depth-ladder"' not in home_text:
        fail(errors, "index.html: missing shared Depth Ladder section")
    catalog = [page_meta(path) for path in pages]
    by_id = {item["roadmap_id"]: item for item in catalog if item["roadmap_id"]}
    expected_ids = [item[0] for item in EXPECTED]
    missing = [item for item in expected_ids if item not in by_id]
    if missing:
        fail(errors, "Missing canonical roadmap IDs: " + ", ".join(missing))
    canonical_count = len(set(by_id) & set(expected_ids))
    if canonical_count != len(expected_ids):
        notes.append(f"Canonical topics: {canonical_count}/{len(expected_ids)}")
    else:
        notes.append(f"Canonical topics: {canonical_count}/{len(expected_ids)}; extras retained: {len(catalog) - canonical_count}")

    required_page_tokens = [
        "id=\"real-world\"", "id=\"technical\"", "id=\"analogy\"", "id=\"demo-or-practice\"", "id=\"quiz\"",
        "part1-complete", "depth-complete", "analogy-mapping", "brightloaf-data", "analogy-scene",
        "Band: Recall", "Band: PCA Scenario", "Band: Staff Review", "Band: Practical Task",
        "Common Misconceptions", "Failure-mode table", "progression-links",
    ]
    for path in pages:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "The Depth Ladder: Conceptual Architecture" in text:
            fail(errors, f"{path.name}: shared Depth Ladder was not removed")
        for token in required_page_tokens:
            if token not in text:
                fail(errors, f"{path.name}: missing {token}")
        if 'class="demo-complete"' in text and 'class="demo-safety-banner"' not in text:
            fail(errors, f"{path.name}: live demo is missing safety banner")
        for attr in re.findall(r"(?:href|src)=\"([^\"]+)\"", text):
            target = local_target(path.parent, attr)
            if target and not target.exists():
                fail(errors, f"{path.name}: broken local link {attr}")
        for kind in ("d1", "d2", "d3", "d4", "d5", "d6"):
            match = re.search(rf'<script id="spec-{kind}-data"[^>]*>\s*(.*?)\s*</script>', text, re.S)
            if not match:
                fail(errors, f"{path.name}: missing inline {kind} spec")
                continue
            try:
                json.loads(match.group(1))
            except json.JSONDecodeError as exc:
                fail(errors, f"{path.name}: invalid inline {kind} JSON ({exc})")

    specs = sorted(DIAGRAMS.glob("*.json"))
    for spec_path in specs:
        if not spec_path.with_suffix(".html").exists():
            continue
        try:
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(errors, f"{spec_path.name}: invalid JSON ({exc})")
            continue
        if not spec.get("summary"):
            fail(errors, f"{spec_path.name}: missing accessible summary")
        scenarios = spec.get("scenarios", [])
        if len(scenarios) < 3:
            fail(errors, f"{spec_path.name}: fewer than 3 scenarios")
        for step in spec.get("steps", []):
            if not step.get("check"):
                fail(errors, f"{spec_path.name}: step {step.get('n')} missing check")
            if not step.get("action") and not step.get("narration"):
                fail(errors, f"{spec_path.name}: step {step.get('n')} missing narration/action")

    html_diagrams = sorted(DIAGRAMS.glob("*.html"))
    if len(html_diagrams) != len(specs) - 1:  # brightloaf or other non-diagram JSONs may be nearby in future.
        notes.append(f"Diagram artifacts: {len(html_diagrams)} HTML / {len(specs)} JSON")
    for path in html_diagrams:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "diagram-engine.js" not in text or "new DiagramEngine" not in text:
            fail(errors, f"{path.name}: standalone diagram is not wired to the shared engine")

    for forbidden in ("brightloaf-dev-01", "Cloud Router automatically allocates additional port blocks", "@import url('https://fonts.googleapis.com"):
        for path in [SITE / "index.html", SITE / "assets/site.css", SITE / "assets/diagram-engine.css", *pages]:
            if forbidden in path.read_text(encoding="utf-8", errors="ignore"):
                fail(errors, f"{path.relative_to(SITE)}: forbidden text {forbidden}")
    raster = [path for path in SITE.rglob("*") if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}]
    if raster:
        fail(errors, "Raster assets found: " + ", ".join(str(path.relative_to(SITE)) for path in raster))
    for required in ("README.md", "README.html", "roadmap-content.html", "brightloaf.json", "assets/city-glyphs.svg", "assets/gcp-glyphs.svg", "scripts/test_diagrams.py", "scripts/build_site.py"):
        if not (SITE / required).exists():
            fail(errors, f"Missing required artifact: {required}")
    interactions = (SITE / "assets" / "site-interactions.js").read_text(encoding="utf-8", errors="ignore")
    if "data-theme-toggle" not in interactions or "gcp-architect-theme" not in interactions:
        fail(errors, "site-interactions.js: missing persistent theme toggle")
    for stylesheet in (SITE / "assets" / "site.css", SITE / "assets" / "diagram-engine.css"):
        if 'html[data-theme="light"]' not in stylesheet.read_text(encoding="utf-8", errors="ignore"):
            fail(errors, f"{stylesheet.name}: missing light-theme overrides")

    rows = ["# Generated content manifest", "", f"Canonical roadmap topics: {len(expected_ids)}", f"Generated topic pages: {len(catalog)}", "", "| Topic | Roadmap ID | Title | Type | Phase |", "|---:|---|---|---|---|"]
    for item in sorted(catalog, key=lambda value: int(value["topic_no"]) if value["topic_no"].isdigit() else 9999):
        rows.append(f'| {item["topic_no"]} | {item["roadmap_id"]} | {item["title"]} | {item["page_type"]} | {item["phase"]} |')
    GENERATED.mkdir(exist_ok=True)
    (GENERATED / "manifest.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    return errors, notes


if __name__ == "__main__":
    errors, notes = validate()
    for note in notes:
        print("NOTE:", note)
    if errors:
        print(f"FAIL: {len(errors)} validation errors")
        for error in errors[:80]:
            print(" -", error)
        if len(errors) > 80:
            print(f" - ... {len(errors) - 80} more")
        raise SystemExit(1)
    print("PASS: content contract, local links, diagram specs, safety checks, and manifest")
