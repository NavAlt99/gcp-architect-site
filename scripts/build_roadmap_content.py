#!/usr/bin/env python3
"""Turn the Markdown roadmap's checklists and review guidance into a browsable artifact."""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path
from urllib.parse import quote_plus

SITE = Path(__file__).resolve().parents[1]
ASSET_VERSION = "20260924-4"
sys.path.insert(0, str(SITE / "scripts"))
from repair_site import claim_sources, page_meta  # noqa: E402


def esc(value: str) -> str:
    return html.escape(value, quote=True)


CHECKLIST_REFERENCE_RULES = (
    ("TCP/IP", "VPC network overview", "https://cloud.google.com/vpc/docs/overview"),
    ("OSI", "Google Cloud Architecture Framework", "https://cloud.google.com/architecture/framework"),
    ("IPv4", "VPC subnet documentation", "https://cloud.google.com/vpc/docs/subnets"),
    ("RFC 1918", "RFC 1918 private address space", "https://www.rfc-editor.org/rfc/rfc1918"),
    ("CIDR", "VPC subnet documentation", "https://cloud.google.com/vpc/docs/subnets"),
    ("IPv6", "VPC IPv6 documentation", "https://cloud.google.com/vpc/docs/using-ipv6"),
    ("DNS", "Cloud DNS overview", "https://cloud.google.com/dns/docs/overview"),
    ("TTL", "Cloud DNS overview", "https://cloud.google.com/dns/docs/overview"),
    ("HTTP/HTTPS", "HTTPS load balancing", "https://cloud.google.com/load-balancing/docs/https"),
    ("TLS handshake", "SSL certificates for load balancing", "https://cloud.google.com/load-balancing/docs/ssl-certificates"),
    ("certificates", "SSL certificates for load balancing", "https://cloud.google.com/load-balancing/docs/ssl-certificates"),
    ("NAT", "Cloud NAT overview", "https://cloud.google.com/nat/docs/overview"),
    ("Routing", "VPC routes", "https://cloud.google.com/vpc/docs/routes"),
    ("BGP", "Cloud Router BGP overview", "https://cloud.google.com/network-connectivity/docs/router/concepts/overview"),
    ("VPN", "Cloud VPN concepts", "https://cloud.google.com/network-connectivity/docs/vpn/concepts/overview"),
    ("IPsec", "Cloud VPN concepts", "https://cloud.google.com/network-connectivity/docs/vpn/concepts/overview"),
    ("load balancing", "Choosing a load balancer", "https://cloud.google.com/load-balancing/docs/choosing-load-balancer"),
    ("health checks", "Load-balancer health checks", "https://cloud.google.com/load-balancing/docs/health-check-concepts"),
    ("firewall", "VPC firewall rules", "https://cloud.google.com/firewall/docs/firewalls"),
    ("IAM", "IAM overview", "https://cloud.google.com/iam/docs/overview"),
    ("service account", "IAM service accounts", "https://cloud.google.com/iam/docs/service-accounts"),
    ("Kubernetes", "GKE overview", "https://cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview"),
    ("Pub/Sub", "Pub/Sub documentation", "https://cloud.google.com/pubsub/docs"),
    ("Terraform", "Terraform on Google Cloud", "https://cloud.google.com/docs/terraform"),
    ("BigQuery", "BigQuery documentation", "https://cloud.google.com/bigquery/docs"),
    ("Dataflow", "Dataflow documentation", "https://cloud.google.com/dataflow/docs"),
    ("Vertex AI", "Vertex AI documentation", "https://cloud.google.com/vertex-ai/docs"),
)


def source_marker(sources: list[tuple[str, str]], kind: str = "t") -> str:
    markers = []
    for index, (label, url) in enumerate(sources, 1):
        marker = kind if len(sources) == 1 else f"{kind}{index}"
        markers.append(
            f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer" aria-label="Source: {esc(label)}">{marker}</a>'
        )
    return f'<sup class="checklist-citation">[{",".join(markers)}]</sup>'


def topic_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    text = re.sub(r"<script\b.*?</script>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", text))).casefold()


def site_topic_index() -> list[dict]:
    topics = []
    for path in sorted((SITE / "pages").glob("topic-*.html")):
        meta = page_meta(path)
        topics.append({"topic_no": meta["topic_no"], "title": meta["title"], "text": topic_text(path)})
    return topics


def site_topic_marker(phrase: str, topics: list[dict]) -> str:
    pattern = re.compile(rf"(?<![A-Za-z0-9]){re.escape(phrase)}(?![A-Za-z0-9])", re.I)
    matches = [topic for topic in topics if pattern.search(topic["text"])]
    if not matches:
        return ""
    links = ",".join(
        f'<a href="pages/topic-{esc(topic["topic_no"])}.html" target="_self" aria-label="Site topic {esc(topic["topic_no"])}: {esc(topic["title"])}">{esc(topic["topic_no"])}</a>'
        for topic in matches
    )
    return f'<sup class="checklist-topic-reference">site:[{links}]</sup>'


def inline_checklist_item(value: str, title: str, topics: list[dict]) -> str:
    """Attach proof links immediately after the concept they support."""
    matches = []
    for phrase, label, url in CHECKLIST_REFERENCE_RULES:
        match = re.search(re.escape(phrase), value, re.I)
        if match and not any(match.start() < end and match.end() > start for start, end, *_rest in matches):
            matches.append((match.start(), match.end(), phrase, label, url))
    matches.sort()
    if not matches:
        sources = claim_sources({"title": title}, value)
        return esc(value) + " " + source_marker(sources)
    parts = []
    cursor = 0
    for start, end, phrase, label, url in matches:
        parts.append(esc(value[cursor:end]))
        parts.append(source_marker([(label, url)]))
        parts.append(site_topic_marker(phrase, topics))
        cursor = end
    parts.append(esc(value[cursor:]))
    return "".join(parts)


def topic_source_row(title: str) -> str:
    query = quote_plus(f"Google Cloud {title}")
    community_query = quote_plus(title)
    text_sources = [
        ("Stack Overflow community", "https://stackoverflow.com/questions/tagged/google-cloud-platform"),
        ("Reddit community", f"https://www.reddit.com/r/googlecloud/search/?q={community_query}&restrict_sr=1"),
    ]
    video_sources = [
        ("YouTube topic search", f"https://www.youtube.com/results?search_query={query}"),
        ("Google Cloud Tech channel", "https://www.youtube.com/@googlecloudtech"),
    ]
    return (
        '<p class="topic-source-row"><strong>More:</strong> Community '
        f'{source_marker(text_sources, "t")} · YouTube {source_marker(video_sources, "v")}</p>'
    )


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
    topics = site_topic_index()
    sections_html = []
    for section in sections:
        items = "".join(f'<li><label><input type="checkbox" data-roadmap-check="{esc(section["id"])}-{i}"> {inline_checklist_item(value, section["title"], topics)}</label></li>' for i, value in enumerate(section["items"], 1))
        citations = topic_source_row(section["title"])
        sections_html.append(f'<details class="roadmap-source-section"><summary><strong>{esc(section["id"])}</strong> {esc(section["title"])} <span class="roadmap-count">{len(section["items"])} items</span></summary><ul>{items}</ul>{citations}</details>')
    lab_html = "".join(f'<li><label><input type="checkbox" data-roadmap-check="lab-{i}"> {esc(value)}</label></li>' for i, value in enumerate(labs, 1))
    checkpoint_html = "".join(f'<article class="topic-section"><h3>Checkpoint {i}</h3><p>{esc(value)}</p></article>' for i, value in enumerate(checkpoints, 1))
    trap_html = "".join(f'<article class="topic-section"><h3>Common trap {i}</h3><p>{esc(value)}</p></article>' for i, value in enumerate(traps, 1))
    body = f'''<section class="topic-section"><p><strong>Source:</strong> {esc(source.name)} · <strong>{total} roadmap checkbox items</strong> ({topic_total} topic items + {len(labs)} lab items) · {len(checkpoints)} checkpoints · {len(traps)} common-trap sections.</p><p>Use the checkboxes for local progress only; they are stored in this browser and do not create cloud resources.</p></section><section class="topic-section"><h2>Topic checklist</h2>{''.join(sections_html)}</section><section class="topic-section"><h2>Hands-on labs</h2><ul>{lab_html}</ul></section><section class="topic-section"><h2>Checkpoints</h2>{checkpoint_html}</section><section class="topic-section"><h2>Common traps</h2>{trap_html}</section>'''
    result = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Roadmap content checklist</title><link rel="stylesheet" href="assets/site.css?v={ASSET_VERSION}"></head><body><main class="main-content"><p><a href="index.html">← Roadmap index</a></p><header class="page-header"><h1 class="page-title">Roadmap content checklist</h1><p class="page-lead">Source-derived checklist, topic citations, labs, checkpoints, and common traps.</p></header>{body}</main><script src="assets/site-interactions.js?v={ASSET_VERSION}"></script></body></html>'''
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
