#!/usr/bin/env python3
"""Turn the Markdown roadmap's checklists and review guidance into a browsable artifact."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
ASSET_VERSION = "20260924-4"


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def build(source: Path) -> None:
    current = None
    sections: list[dict] = []
    labs: list[str] = []
    checkpoints: list[str] = []
    traps: list[str] = []
    in_labs = False
    for raw in source.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        heading = re.match(r"^###\s+([^\s]+)\s+(.+)$", line)
        if heading:
            current = {"id": heading.group(1), "title": heading.group(2), "items": []}
            sections.append(current)
            in_labs = False
            continue
        if line.startswith("**Hands-on labs**"):
            in_labs = True
            continue
        item = re.match(r"^- \[[ xX]\]\s+(.+)$", line)
        if item:
            value = item.group(1)
            if in_labs:
                labs.append(value)
            elif current:
                current["items"].append(value)
            continue
        checkpoint = re.match(r"^\*\*Checkpoint:\*\*\s*(.+)$", line)
        trap = re.match(r"^\*\*Common traps:\*\*\s*(.+)$", line)
        if checkpoint:
            checkpoints.append(checkpoint.group(1))
        if trap:
            traps.append(trap.group(1))

    topic_total = sum(len(section["items"]) for section in sections)
    total = topic_total + len(labs)
    sections_html = []
    for section in sections:
        items = "".join(f'<li><label><input type="checkbox" data-roadmap-check="{esc(section["id"])}-{i}"> {esc(value)}</label></li>' for i, value in enumerate(section["items"], 1))
        sections_html.append(f'<details class="roadmap-source-section"><summary><strong>{esc(section["id"])}</strong> {esc(section["title"])} <span class="roadmap-count">{len(section["items"])} items</span></summary><ul>{items}</ul></details>')
    lab_html = "".join(f'<li><label><input type="checkbox" data-roadmap-check="lab-{i}"> {esc(value)}</label></li>' for i, value in enumerate(labs, 1))
    checkpoint_html = "".join(f'<article class="topic-section"><h3>Checkpoint {i}</h3><p>{esc(value)}</p></article>' for i, value in enumerate(checkpoints, 1))
    trap_html = "".join(f'<article class="topic-section"><h3>Common trap {i}</h3><p>{esc(value)}</p></article>' for i, value in enumerate(traps, 1))
    body = f'''<section class="topic-section"><p><strong>Source:</strong> {esc(source.name)} · <strong>{total} roadmap checkbox items</strong> ({topic_total} topic items + {len(labs)} lab items) · {len(checkpoints)} checkpoints · {len(traps)} common-trap sections.</p><p>Use the checkboxes for local progress only; they are stored in this browser and do not create cloud resources.</p></section><section class="topic-section"><h2>Topic checklist</h2>{''.join(sections_html)}</section><section class="topic-section"><h2>Hands-on labs</h2><ul>{lab_html}</ul></section><section class="topic-section"><h2>Checkpoints</h2>{checkpoint_html}</section><section class="topic-section"><h2>Common traps</h2>{trap_html}</section>'''
    result = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Roadmap content checklist</title><link rel="stylesheet" href="assets/site.css?v={ASSET_VERSION}"></head><body><main class="main-content"><p><a href="index.html">← Roadmap index</a></p><header class="page-header"><h1 class="page-title">Roadmap content checklist</h1><p class="page-lead">Source-derived checklist, labs, checkpoints, and common traps.</p></header>{body}</main><script src="assets/site-interactions.js?v={ASSET_VERSION}"></script></body></html>'''
    (SITE / "roadmap-content.html").write_text(result, encoding="utf-8")
    print(f"Wrote roadmap-content.html: {total} checklist items ({topic_total} topics + {len(labs)} labs), {len(checkpoints)} checkpoints, {len(traps)} trap sections")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--roadmap", required=True)
    args = parser.parse_args()
    source = Path(args.roadmap).expanduser().resolve()
    if not source.is_file():
        parser.error(f"roadmap source does not exist: {source}")
    build(source)
