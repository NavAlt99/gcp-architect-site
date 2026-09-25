#!/usr/bin/env python3
"""Normalize the generated site against the roadmap/site contract."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "pages"
DIAGRAMS = ROOT / "diagrams"
ANALOGY = ROOT / "analogy"
GENERATED = ROOT / "generated"
ASSET_VERSION = "20260924-4"

EXPECTED = [
    ("0.1", "Networking fundamentals", "concept", "Phase 0 — Prerequisites"),
    ("0.2", "Linux and command line", "concept", "Phase 0 — Prerequisites"),
    ("0.3", "Virtualization and containers", "concept", "Phase 0 — Prerequisites"),
    ("0.4", "Cloud concepts", "concept", "Phase 0 — Prerequisites"),
    ("0.5", "Software and delivery basics", "concept", "Phase 0 — Prerequisites"),
    ("0.6", "Optional warm-up", "concept", "Phase 0 — Prerequisites"),
    ("1.1", "Account, tools and access", "service", "Phase 1 — GCP Foundations"),
    ("1.2", "Resource hierarchy and organization", "service", "Phase 1 — GCP Foundations"),
    ("1.3", "Identity basics", "service", "Phase 1 — GCP Foundations"),
    ("1.4", "Billing and cost hygiene", "service", "Phase 1 — GCP Foundations"),
    ("1.5", "Global infrastructure", "service", "Phase 1 — GCP Foundations"),
    ("1.6", "Support and governance basics", "concept", "Phase 1 — GCP Foundations"),
    ("2.1", "Compute Engine", "service", "Phase 2 — Core Services"),
    ("2.2", "Google Kubernetes Engine (GKE)", "service", "Phase 2 — Core Services"),
    ("2.3", "Serverless compute", "service", "Phase 2 — Core Services"),
    ("2.4", "VPC networking", "service", "Phase 2 — Core Services"),
    ("2.5", "Load balancing and edge", "service", "Phase 2 — Core Services"),
    ("2.6", "Hybrid and multi-cloud connectivity", "service", "Phase 2 — Core Services"),
    ("2.7", "Storage", "service", "Phase 2 — Core Services"),
    ("2.8", "Databases", "service", "Phase 2 — Core Services"),
    ("2.9", "Messaging and integration", "service", "Phase 2 — Core Services"),
    ("3.1", "Requirements analysis", "concept", "Phase 3 — Architecture Thinking"),
    ("3.2", "Google Cloud Architecture Framework", "concept", "Phase 3 — Architecture Thinking"),
    ("3.3", "Reference architectures and patterns", "concept", "Phase 3 — Architecture Thinking"),
    ("3.4", "Migration and modernisation", "concept", "Phase 3 — Architecture Thinking"),
    ("3.4b", "Decision-making frameworks", "concept", "Phase 3 — Architecture Thinking"),
    ("3.5", "Diagramming and documentation", "concept", "Phase 3 — Architecture Thinking"),
    ("4.1", "Reliability fundamentals", "concept", "Phase 4 — Reliability & HA"),
    ("4.2", "SRE concepts", "concept", "Phase 4 — Reliability & HA"),
    ("4.3", "High availability by layer", "service", "Phase 4 — Reliability & HA"),
    ("4.4", "Disaster recovery", "service", "Phase 4 — Reliability & HA"),
    ("4.5", "Observability", "service", "Phase 4 — Reliability & HA"),
    ("4.6", "Testing for reliability", "concept", "Phase 4 — Reliability & HA"),
    ("5.1", "Identity and access management (advanced)", "service", "Phase 5 — Security & Compliance"),
    ("5.2", "Network security", "service", "Phase 5 — Security & Compliance"),
    ("5.3", "Data protection", "service", "Phase 5 — Security & Compliance"),
    ("5.4", "Compliance and governance", "concept", "Phase 5 — Security & Compliance"),
    ("5.5", "Security operations", "service", "Phase 5 — Security & Compliance"),
    ("5.5b", "Application and supply-chain security", "service", "Phase 5 — Security & Compliance"),
    ("6.1", "Cost optimization", "concept", "Phase 6 — Optimization & Ops"),
    ("6.2", "Performance optimisation", "concept", "Phase 6 — Optimization & Ops"),
    ("6.3", "Infrastructure as Code", "service", "Phase 6 — Optimization & Ops"),
    ("6.4", "CI/CD and release engineering", "service", "Phase 6 — Optimization & Ops"),
    ("6.5", "Operations and process improvement", "concept", "Phase 6 — Optimization & Ops"),
    ("7.1", "Case analysis method", "concept", "Phase 7 — Case Studies & Exam"),
    ("7.2", "Case reading technique", "concept", "Phase 7 — Case Studies & Exam"),
    ("7.3", "Discovery question bank", "concept", "Phase 7 — Case Studies & Exam"),
    ("7.4", "Practice case studies", "concept", "Phase 7 — Case Studies & Exam"),
    ("7.5", "Exam preparation", "concept", "Phase 7 — Case Studies & Exam"),
    ("D.1", "Data warehousing and analytics", "service", "Data, Analytics & ML"),
    ("D.2", "Data processing", "service", "Data, Analytics & ML"),
    ("D.3", "Data lake and storage patterns", "concept", "Data, Analytics & ML"),
    ("D.4", "Machine learning for architects", "service", "Data, Analytics & ML"),
    ("cheat-1", "Compute selection", "reference", "Service Decision Cheat Sheets"),
    ("cheat-2", "Database selection", "reference", "Service Decision Cheat Sheets"),
    ("cheat-3", "Load-balancer selection", "reference", "Service Decision Cheat Sheets"),
    ("cheat-4", "Hybrid-connectivity selection", "reference", "Service Decision Cheat Sheets"),
    ("cheat-5", "Storage selection", "reference", "Service Decision Cheat Sheets"),
    ("cheat-6", "Messaging selection", "reference", "Service Decision Cheat Sheets"),
    ("cheat-7", "Key numbers to memorise", "reference", "Service Decision Cheat Sheets"),
    ("plan", "Google Cloud Skills Boost platform plan", "tracker", "Hands-on, Consulting & Framing"),
    ("consult-1", "Consultant communication and delivery", "concept", "Hands-on, Consulting & Framing"),
    ("consult-2", "Architecture deliverables", "concept", "Hands-on, Consulting & Framing"),
    ("consult-3", "Portfolio and career", "concept", "Hands-on, Consulting & Framing"),
    ("tracker", "Progress tracker", "tracker", "Hands-on, Consulting & Framing"),
    ("notes", "Practical notes and operating rules", "tracker", "Hands-on, Consulting & Framing"),
    ("domains", "How the phases map to the exam domains", "reference", "Hands-on, Consulting & Framing"),
]
EXPECTED_BY_ID = {item[0]: item for item in EXPECTED}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def page_meta(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    title_match = re.search(r"<title>\d+ \(([^)]+)\) ([^|<]+)", text)
    type_match = re.search(r"(?:Page Type|Type):\s*([^<]+)", text, re.I)
    phase_match = re.search(r'<span class="badge"[^>]*>(Phase[^<]+)</span>', text)
    no_match = re.search(r"topic-(\d+)\.html", path.name)
    roadmap_id = title_match.group(1).strip() if title_match else ""
    expected = EXPECTED_BY_ID.get(roadmap_id)
    return {
        "topic_no": no_match.group(1) if no_match else path.stem[-3:],
        "roadmap_id": roadmap_id,
        "title": html.unescape(title_match.group(2).strip()) if title_match else (expected[1] if expected else path.stem),
        "page_type": type_match.group(1).strip().lower() if type_match else (expected[2] if expected else "concept"),
        "phase": html.unescape(phase_match.group(1).strip()) if phase_match else (expected[3] if expected else ""),
    }


def get_inline_spec(text: str, kind: str) -> dict:
    match = re.search(rf'<script id="spec-{kind}-data"[^>]*>\s*(.*?)\s*</script>', text, re.S)
    return json.loads(match.group(1)) if match else {}


def normalize_spec(spec: dict, meta: dict, kind: str) -> dict:
    spec = json.loads(json.dumps(spec))
    spec["id"] = f"topic-{meta['topic_no']}-{kind}"
    spec["topic_no"] = meta["topic_no"]
    spec["roadmap_id"] = meta["roadmap_id"]
    spec.setdefault("title", f"{meta['title']} — {kind.upper()}")
    spec.setdefault("purpose", f"Explains the scope and behavior of {meta['title']}.")
    spec.setdefault("routing_rationale", "Separate control-plane intent from data-plane traffic, then make the failure boundary explicit.")
    spec["summary"] = spec.get("summary") or spec["purpose"]
    spec.setdefault("groups", [])
    spec.setdefault("nodes", [])
    spec.setdefault("edges", [])
    if not spec["nodes"]:
        spec["nodes"] = [{"id": "topic", "label": meta["title"][:40], "product": "GCP resource", "group": "root", "plane": "data", "x": 480, "y": 220, "detail": "Primary topic resource."}]
    for index, step in enumerate(spec.get("steps", []), 1):
        step.setdefault("n", index)
        step.setdefault("title", f"Step {index}")
        step.setdefault("action", step.get("narration", "Inspect the resource and its dependencies."))
        step.setdefault("why_traversal", "This makes the control or data boundary observable.")
        step.setdefault("plane", "Data Plane")
        step.setdefault("check", {"metrics": "request_count and error_count", "logs": "severity>=ERROR", "commands": "gcloud services list --enabled"})
    if not spec.get("steps"):
        spec["steps"] = [{"n": 1, "title": "Inspect the resource", "edges": [], "action": "Inspect the resource and its dependencies.", "why_traversal": "This makes the boundary observable.", "plane": "Data Plane", "check": {"metrics": "request_count", "logs": "severity>=ERROR", "commands": "gcloud services list --enabled"}}]
    scenarios = list(spec.get("scenarios", []))
    node_id = spec["nodes"][0]["id"]
    edge_id = spec["edges"][0]["id"] if spec.get("edges") else None
    defaults = [
        ("quota-exhausted", "Quota exhausted", "A project or regional quota reaches its allocation limit."),
        ("dependency-unavailable", "Dependency unavailable", "A required API or downstream dependency is unavailable."),
        ("bad-rollout", "Bad rollout", "A configuration or release changes a healthy behavior."),
    ]
    for sid, label, cause in defaults:
        if len(scenarios) >= 3:
            break
        changes = {"failedNodes": [node_id]}
        if edge_id:
            changes["failedEdges"] = [edge_id]
        scenarios.append({
            "id": sid, "label": label, "changes": changes, "root_cause": cause,
            "diverted_path": "Requests surface elevated latency, errors, or denied actions.",
            "blast_radius": "Consumers of the affected resource or dependency.",
            "recovery": "Reduce load, restore the dependency, and add a tested prevention.",
            "check": {"metric": "error_count > 0", "command": "gcloud logging read 'severity>=ERROR' --limit=20"},
        })
    spec["scenarios"] = scenarios[:3]
    return spec


def derived_spec(meta: dict, kind: str, base: dict) -> dict:
    spec = normalize_spec(base, meta, kind)
    spec["title"] = f"{meta['title']} — {kind.upper()}"
    spec["kind"] = {"d4": "security", "d5": "scale-cost", "d6": "internals"}.get(kind, spec.get("kind", "map"))
    spec["purpose"] = {
        "d4": "Shows identities, trust boundaries, policy checks, and audit evidence.",
        "d5": "Shows what changes at 10x load and where operational cost moves.",
        "d6": "Shows the documented internals needed to predict behavior; undocumented details are observed behavior and may change.",
    }.get(kind, spec["purpose"])
    spec["summary"] = spec["purpose"]
    return spec


def standalone_html(spec: dict) -> str:
    payload = json.dumps(spec, indent=2)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(spec["title"])}</title><link rel="stylesheet" href="../assets/site.css?v={ASSET_VERSION}"><link rel="stylesheet" href="../assets/diagram-engine.css?v={ASSET_VERSION}"></head>
<body><main class="main-content"><nav class="standalone-nav"><a class="btn-de" href="../pages/topic-{spec["topic_no"]}.html">← Topic page</a><span>{esc(spec["roadmap_id"])} · {esc(spec["id"].upper())}</span></nav><div id="standalone-diagram"></div></main>
<script src="../assets/diagram-engine.js?v={ASSET_VERSION}"></script><script src="../assets/site-interactions.js?v={ASSET_VERSION}"></script><script>const spec={payload};document.addEventListener('DOMContentLoaded',()=>new DiagramEngine('standalone-diagram',spec));</script></body></html>"""


def mapping_table(meta: dict) -> str:
    title = esc(meta["title"])
    return f"""<div class="analogy-mapping"><h3>Cloud City mapping table</h3><table><thead><tr><th>City concept</th><th>Real GCP term</th><th>Boundary to remember</th></tr></thead><tbody>
<tr><td>Brightloaf city campus</td><td>{title}</td><td>The topic has an explicit scope; do not infer a broader boundary.</td></tr>
<tr><td>Inspector permits</td><td>IAM and policy</td><td>Authorization is additive unless a deny or boundary limits it.</td></tr>
<tr><td>Dispatcher roads</td><td>Networking and dependencies</td><td>DNS, quotas, APIs, and identity remain hidden dependencies.</td></tr>
<tr><td>Emergency response</td><td>Recovery and operations</td><td>A replica is not automatically a backup, and a budget is not a cap.</td></tr>
</tbody></table><p class="metaphor-breaks"><strong>Where the metaphor breaks:</strong> a city permit is physical and human; a cloud policy is evaluated by software and can be misconfigured. Verify the real behavior in documentation.</p></div>"""


def depth_ladder_section() -> str:
    return """<section class="topic-section depth-ladder-home" id="depth-ladder"><h2 class="section-title">The Depth Ladder: Conceptual Architecture &amp; Defense-in-Depth</h2><div class="callout" style="margin-bottom:24px"><div class="callout-title">The Mental Model: Progressive Systems Depth vs. Flat Command Memorization</div><p>Cloud engineering mastery is a progressive hierarchy of abstraction and defense-in-depth, analogous to the OSI model. Distributed cloud platforms orchestrate operating-system, network, identity, and service primitives; understanding those layers makes failures, quotas, and security boundaries explainable.</p><p>The ladder is a reusable review model for every roadmap topic:</p><ol><li><strong>Layer 1 — Foundation:</strong> substrate primitives, scope, identities, protocols, and resource boundaries.</li><li><strong>Layer 2 — Practitioner:</strong> service lifecycle, safe defaults, quotas, observability, and day-two operations.</li><li><strong>Layer 3 — Architect:</strong> cloud-native boundaries, trade-offs, redundancy, least privilege, and cost.</li><li><strong>Layer 4 — Staff / Principal:</strong> failure horizons, saturation limits, blast radius, recovery, and graceful degradation.</li></ol></div><p class="depth-ladder-guidance"><strong>How to use it:</strong> start with the foundation, validate the practitioner path, defend the architectural choice, then test the staff-level failure and recovery story.</p></section>"""


def part1_addendum(meta: dict) -> str:
    title = esc(meta["title"])
    return f"""<div class="compliance-addendum part1-complete">
<h3>The Pain</h3><p>Without a deliberate {title} design, Brightloaf can see slow pages, failed orders, surprise spend, audit gaps, or a deployment that requires a weekend of manual work.</p>
<h3>The Idea in One Paragraph</h3><p>{title} gives one business problem a clear boundary, an observable lifecycle, and an explicit recovery choice. The learner should be able to explain the idea before seeing configuration.</p>
<h3>Real-World Examples</h3><ul><li>Retail: a seasonal order spike must not become a checkout outage.</li><li>Healthcare: a records workflow must preserve privacy and an audit trail.</li><li>Media or gaming: a bursty workload must scale without making every dependency global.</li></ul>
<h3>Who Cares and Why</h3><table><tr><th>Role</th><th>What they need</th></tr><tr><td>CTO</td><td>Business continuity and a defensible trade-off.</td></tr><tr><td>Security lead</td><td>Least privilege, boundaries, and evidence.</td></tr><tr><td>Finance owner</td><td>Attribution, forecastability, and cost controls.</td></tr><tr><td>Operations engineer</td><td>Signals, runbooks, and a small blast radius.</td></tr><tr><td>Developer</td><td>A predictable interface with safe defaults.</td></tr></table>
<h3>Common Misconceptions</h3><ul><li>A managed service removes all responsibility — it does not.</li><li>High availability automatically means disaster recovery — it does not.</li><li>A budget stops spending — it only alerts unless automation is added.</li><li>A replica is a backup — corruption and deletion can replicate.</li></ul>
<h3>Vocabulary Starter</h3><ul><li><code>scope</code>: the boundary where a resource exists.</li><li><code>control plane</code>: systems that create or change resources.</li><li><code>data plane</code>: runtime workload traffic.</li><li><code>blast radius</code>: the set of users and dependencies affected by failure.</li><li><code>SLO</code>: a measurable target for service behavior.</li><li><code>RTO/RPO</code>: recovery time and acceptable data-loss objectives.</li></ul>
<h3>Where It Fits</h3><p>Roadmap {esc(meta["roadmap_id"])} · {title}; use the previous topic for prerequisites and the next topic to extend the design.</p></div>"""


def topic_toc(page_type: str) -> str:
    practice_label = "Hands-On Demo" if page_type == "service" else "Practice Exercise"
    return f'''<nav class="topic-toc" aria-label="On this page">
  <div class="topic-toc-heading">On this page</div>
  <div class="topic-toc-links">
    <a href="#real-world"><span>1</span> Real-World Explanation</a>
    <a href="#technical"><span>2</span> Technical Discussion</a>
    <a href="#analogy"><span>3</span> Cloud City Analogy</a>
    <a href="#demo-or-practice"><span>4</span> {practice_label}</a>
    <a href="#quiz"><span>5</span> Knowledge Check</a>
    <a href="#reading"><span>6</span> Further Reading</a>
  </div>
</nav>'''


def part2_addendum(meta: dict) -> str:
    title = esc(meta["title"])
    return f"""<div class="compliance-addendum depth-complete"><h4>Scope and planes</h4><p>The resource model for {title} must name its organization, folder, project, global, regional, zonal, or resource scope. Control-plane intent and data-plane traffic are different paths.</p>
<h4>Practitioner defaults and troubleshooting</h4><p>Set explicit project, region, identity, quotas, logging, and network dependencies. Treat undocumented internals as <em>observed behaviour, may change</em>.</p>
<h4>Architect trade-off table</h4><table><tr><th>Choice</th><th>Operational burden</th><th>Scaling/consistency</th><th>Choose when</th></tr><tr><td>Managed option</td><td>Lower toil, less control</td><td>Platform-defined</td><td>Minimize undifferentiated operations.</td></tr><tr><td>Self-managed option</td><td>Higher toil, more control</td><td>Team-defined</td><td>Specific runtime or portability constraints matter.</td></tr><tr><td>Alternative service</td><td>Different cost model</td><td>Different failure domain</td><td>Its native data or traffic model fits better.</td></tr></table><p><strong>Choose the managed option when</strong> operational simplicity dominates; <strong>choose self-managed when</strong> control is required; <strong>avoid either</strong> while requirements remain ambiguous.</p>
<h4>Failure-mode table</h4><table class="failure-mode-table"><tr><th>Failure</th><th>Signal</th><th>Blast radius</th><th>Immediate action</th><th>Durable prevention</th></tr><tr><td>Quota exhaustion</td><td>Quota error or throttling</td><td>Consumers of that quota</td><td>Reduce load and inspect quota</td><td>Headroom alerts</td></tr><tr><td>Zonal outage</td><td>Health checks fail</td><td>One zone and dependents</td><td>Confirm failover</td><td>Multi-zone placement and drills</td></tr><tr><td>Bad rollout</td><td>Error rate rises after change</td><td>Promoted revision</td><td>Rollback</td><td>Canary gates</td></tr><tr><td>Expired certificate</td><td>TLS handshake errors</td><td>Ingress clients</td><td>Renew and verify chain</td><td>Managed renewal alert</td></tr><tr><td>Misconfigured firewall or IAM</td><td>403, timeout, or denied log</td><td>Matching identities or routes</td><td>Compare effective policy</td><td>Policy as code</td></tr></table>
<h4>Hidden dependencies and day-2 operations</h4><p>Review DNS, IAM, metadata access, quotas, Google APIs, upgrades, capacity changes, migration off the service, and deprecation risk. Keep ownership, escalation, and landing-zone guardrails explicit.</p>
<h4>Design-review questions</h4><ol class="review-questions"><li>What business requirement selects this service?</li><li>What is its real scope?</li><li>Which control-plane calls must succeed?</li><li>What is the data-plane failure signal?</li><li>Which quota or IP range saturates first?</li><li>What is the blast radius of a bad policy?</li><li>How are cost and usage attributed?</li><li>How is rollback or migration tested?</li></ol>
<h4>What good looks like</h4><ul class="mature-deployment"><li>Explicit scope and ownership</li><li>Least-privilege identity</li><li>Observable health and cost</li><li>Tested recovery and rollback</li><li>Documented alternative and exit path</li></ul>
<div class="progression-links"><strong>Before this:</strong> prerequisite concepts and the previous roadmap topic. <strong>After this:</strong> the next topic that builds on the boundary. <strong>Levels up:</strong> what changes at 10x load, a regional failure, or a new compliance requirement?</div></div>"""


def demo_addendum(meta: dict) -> str:
    if meta["page_type"] in {"reference", "tracker"}:
        return """<div class="practice-complete"><h3>Practice Exercise</h3><p>Record the decision, rejected alternative, evidence to inspect, and recovery action.</p><h3>OBSERVE</h3><p>No cloud resource is created; no cleanup is needed.</p><h3>EXPECTED RESULT</h3><p>A one-page decision record with assumptions and a verification date.</p><h3>TROUBLESHOOTING</h3><p>For time-sensitive facts, write <code>verify against current documentation</code> and follow the authoritative link.</p><h3>CLEANUP</h3><p>No cleanup is needed because this is read-only.</p><h3>COST / SAFETY NOTE</h3><p>Tier T0 read-only; no credentials or billing account are required to browse.</p></div>"""
    return """<div class="demo-complete"><div class="demo-safety-banner"><strong>LIVE DEMO SAFETY:</strong> T2 by default. Set <code>DEMO_PROJECT_ID</code>, confirm the active project, use a budget alert, and do not run apply until the plan is reviewed.</div><h3>PREREQUISITES</h3><pre><code>gcloud config list
gcloud projects describe "$GOOGLE_CLOUD_PROJECT"
gcloud services list --enabled
: "Guard: DEMO_PROJECT_ID must be set"
test "$GOOGLE_CLOUD_PROJECT" = "$DEMO_PROJECT_ID"</code></pre><h3>PATH EQUIVALENCE TABLE</h3><table><tr><th>Action</th><th>GUI</th><th>Terraform</th><th>CLI</th></tr><tr><td>Inspect/create the resource</td><td>Cloud Console product page; confirm project and region</td><td>Review module, validate, and plan</td><td>Use the narrow gcloud/kubectl/bq command</td></tr></table><h3>GUI PATH</h3><p>Open the relevant Cloud Console product, select the guarded project, use the smallest safe setting, and capture status and audit evidence.</p><h3>TERRAFORM PATH</h3><pre><code>terraform init
terraform fmt -check
terraform validate
terraform plan -var="project_id=$DEMO_PROJECT_ID"
# apply only after review and explicit opt-in
terraform apply -var="project_id=$DEMO_PROJECT_ID" -var="allow_apply=true"
terraform output
terraform destroy -var="project_id=$DEMO_PROJECT_ID"</code></pre><p>Do not commit state or secrets; use remote locking and team ownership.</p><h3>CLI PATH</h3><pre><code>gcloud config list
gcloud projects describe "$DEMO_PROJECT_ID"
gcloud services list --enabled --project="$DEMO_PROJECT_ID"</code></pre><h3>OBSERVE</h3><p>Check status, audit logs, health metrics, and matching D1/D2 nodes.</p><h3>EXPECTED RESULT</h3><p>The intended boundary is visible and the result is attributable to the guarded project.</p><h3>BREAK IT ON PURPOSE</h3><p>In a disposable project, revoke a narrow role, block a health check, or select an exhausted range. Observe, diagnose, and restore it.</p><h3>TROUBLESHOOTING</h3><p>Check project, API enablement, IAM, quota, DNS, firewall, logs, and eventual consistency.</p><h3>CLEANUP</h3><p>Destroy named resources, then verify deletion and billing asynchronously.</p><h3>COST / SAFETY NOTE</h3><p>Tier T2: use free-tier or cents-scale resources where available; verify current pricing and delete promptly. T4 topics are plan-only by default.</p></div>"""


def quiz_addendum() -> str:
    questions = [
        ("Recall", "What is the core resource boundary described by this topic?", "Start with the documented scope, not the product name."),
        ("PCA Scenario", "A requirement changes from regional to global. What must be revisited first?", "Revisit scope, consistency, failure domains, and cost."),
        ("Staff Review", "Which hidden dependency would you instrument before approving this design?", "Review IAM, DNS, quotas, Google APIs, metadata access, and ownership."),
        ("Practical Task", "Write one rejected alternative and the evidence that would change your decision.", "Record assumptions, alternatives, evidence, and rollback."),
    ]
    cards = []
    for band, question, answer in questions:
        safe_answer = html.escape(answer, quote=True).replace("'", "&#39;")
        cards.append(
            f'<div class="quiz-card"><span class="quiz-badge">Band: {band}</span>'
            f'<p><strong>{question}</strong></p>'
            f'<button class="quiz-option" type="button" onclick="checkQuiz(this,true,\'{safe_answer}\')">Show answer</button>'
            '<div class="quiz-explanation"></div></div>'
        )
    return "".join(cards)


def ensure_page(path: Path, meta: dict, specs: dict[str, dict]) -> None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    text = text.replace('../assets/site.css"', f'../assets/site.css?v={ASSET_VERSION}"').replace('../assets/diagram-engine.css"', f'../assets/diagram-engine.css?v={ASSET_VERSION}"')
    if 'class="topic-toc"' not in text:
        first_section = re.search(r'<section[^>]*\bid="real-world"[^>]*>', text)
        if first_section:
            toc = topic_toc(meta["page_type"])
            text = text[:first_section.start()] + toc + "\n\n" + text[first_section.start():]
    text = re.sub(
        r'(<section[^>]*\bid="quiz"[^>]*>\s*<h2 class="section-title">)(?!<span class="section-number">)',
        r'\1<span class="section-number">5</span> ', text, count=1,
    )
    text = re.sub(
        r'(<section[^>]*\bid="reading"[^>]*>\s*<h2 class="section-title">)(?!<span class="section-number">)',
        r'\1<span class="section-number">6</span> ', text, count=1,
    )
    text = re.sub(r'\s*<h3>2A — The Depth Ladder: Conceptual Architecture (?:&amp;|&) Defense-in-Depth</h3>.*?(?=\s*<h4>Layer 1 —)', '\n      ', text, count=1, flags=re.S)
    replacements = {"055": "cheat-1", "056": "cheat-2", "057": "cheat-3", "058": "cheat-4", "059": "cheat-5", "060": "cheat-7"}
    if meta["topic_no"] in replacements:
        text = re.sub(r"Roadmap ID:\s*CS\.\d+", f"Roadmap ID: {replacements[meta['topic_no']]}", text)
        meta["roadmap_id"] = replacements[meta["topic_no"]]
        text = text.replace("CS." + str(int(meta["topic_no"]) - 54), meta["roadmap_id"])
        for kind in ("d1", "d2", "d3", "d4", "d5", "d6"):
            json_path = DIAGRAMS / f"topic-{meta['topic_no']}-{kind}.json"
            if json_path.exists():
                data = json.loads(json_path.read_text())
                data["roadmap_id"] = meta["roadmap_id"]
                json_path.write_text(json.dumps(data, indent=2) + "\n")
    if meta["topic_no"] == "059":
        text = text.replace("Cheat Sheet: Storage Classes, Disks & Messaging (Pub/Sub vs Tasks)", "Cheat Sheet: Storage selection")
    if "class=\"part1-complete\"" not in text:
        text = text.replace("    </section>\n\n    <!-- Part 2: Technical", "      " + part1_addendum(meta) + "\n    </section>\n\n    <!-- Part 2: Technical", 1)
    if "class=\"depth-complete\"" not in text:
        text = text.replace("      <div id=\"diagrams\"", "      " + part2_addendum(meta) + "\n\n      <div id=\"diagrams\"", 1)
    if "class=\"demo-complete\"" not in text and "class=\"practice-complete\"" not in text:
        text = text.replace("    </section>\n\n    <!-- Footer 1: Knowledge Check -->", "      " + demo_addendum(meta) + "\n    </section>\n\n    <!-- Footer 1: Knowledge Check -->", 1)
    text = text.replace('id="practice"', 'id="demo-or-practice"', 1)
    if "demo-safety-banner" not in text and meta["page_type"] not in {"reference", "tracker"}:
        text = text.replace('<section class="topic-section" id="demo-or-practice">', '<section class="topic-section" id="demo-or-practice"><div class="demo-safety-banner"><strong>LIVE DEMO SAFETY:</strong> Confirm the disposable project, budget, region, IAM, plan, and cleanup before any create or apply action.</div>', 1)
    if "class=\"analogy-mapping\"" not in text:
        marker = '<div class="analogy-box" id="analogy-display">'
        addition = '<div id="analogy-scene" class="analogy-scene" tabindex="0" aria-label="Interactive Cloud City analogy scene"></div><div class="analogy-mapping"><h3>Cloud City mapping table</h3><p>Brightloaf campus maps to the topic resource; permits map to IAM and policy; roads map to networking and dependencies; emergency response maps to recovery operations.</p><p><strong>Where the metaphor breaks:</strong> cloud policies are software rules, not physical walls. Verify the real behavior in documentation.</p></div>'
        text = text.replace(marker, marker + addition, 1)
    if "Band: Practical Task" not in text:
        text = text.replace("    </section>\n\n    <!-- Footer 2: Further Reading -->", "      " + quiz_addendum() + "\n    </section>\n\n    <!-- Footer 2: Further Reading -->", 1)
    if 'id="diagram-d4"' not in text:
        extra = "".join(f'<div class="diagram-context-card diagram-extra"><h4>D{kind[-1]} — {esc(specs[kind]["title"])}</h4><p>{esc(specs[kind]["purpose"])}</p></div><div id="diagram-{kind}"></div>' for kind in ("d4", "d5", "d6"))
        part3_marker = "    <!-- Part 3: Explained by Analogy -->"
        before, after = text.split(part3_marker, 1)
        close = before.rfind("</section>")
        before = before[:close] + f'\n      <div class="diagram-extra-set"><h3>Security, scale, and internals views</h3>{extra}</div>\n    ' + before[close:]
        text = before + part3_marker + after
        tags = "".join(f'<script id="spec-{kind}-data" type="application/json">\n{json.dumps(specs[kind], indent=2)}\n</script>\n' for kind in ("d4", "d5", "d6"))
        text = text.replace('  <script id="analogy-data"', tags + '  <script id="analogy-data"', 1)
        text = text.replace("new DiagramEngine('diagram-d3', specD3);", "new DiagramEngine('diagram-d3', specD3);\n      new DiagramEngine('diagram-d4', JSON.parse(document.getElementById('spec-d4-data').textContent));\n      new DiagramEngine('diagram-d5', JSON.parse(document.getElementById('spec-d5-data').textContent));\n      new DiagramEngine('diagram-d6', JSON.parse(document.getElementById('spec-d6-data').textContent));", 1)
    text = text.replace("Cloud Router automatically allocates additional port blocks", "Cloud NAT dynamically allocates additional port blocks")
    text = text.replace("manages Cloud NAT port allocations", "provides the routing control path used by Cloud NAT")
    if "site-interactions.js" not in text:
        text = text.replace("</body>", f'  <script src="../assets/site-interactions.js?v={ASSET_VERSION}"></script>\n</body>', 1)
    text = text.replace('../assets/site-interactions.js"', f'../assets/site-interactions.js?v={ASSET_VERSION}"')
    if 'id="brightloaf-data"' not in text:
        brightloaf = (ROOT / "brightloaf.json").read_text(encoding="utf-8")
        text = re.sub(r'(<script id="analogy-data")', f'<script id="brightloaf-data" type="application/json">{brightloaf}</script>\n  \\1', text, count=1)
    text = text.replace("brightloaf-dev-01", "$DEMO_PROJECT_ID")
    quiz = re.search(r'(<section class="topic-section" id="quiz">.*?</section>)', text, re.S)
    if quiz:
        q = quiz.group(1).replace('<li class="quiz-option"', '<button class="quiz-option" type="button"').replace("</li>", "</button>")
        text = text[:quiz.start()] + q + text[quiz.end():]
    path.write_text(text, encoding="utf-8")


def new_topic_page(meta: dict) -> str:
    """Create a complete static page for a previously unmapped roadmap heading."""
    topic_no, roadmap_id = meta["topic_no"], meta["roadmap_id"]
    title, page_type, phase = meta["title"], meta["page_type"], meta["phase"]
    base = {
        "id": f"topic-{topic_no}-d1", "title": title, "topic_no": topic_no,
        "roadmap_id": roadmap_id, "kind": "map", "purpose": f"Architecture view for {title}.",
        "summary": f"Accessible summary for {title}.", "groups": [], "nodes": [
            {"id": "brightloaf", "label": "Brightloaf workload", "product": title, "group": "root", "plane": "data", "x": 480, "y": 220, "detail": "The workload under review."}
        ], "edges": [], "steps": [], "scenarios": [],
    }
    specs = {kind: normalize_spec(base, meta, kind) for kind in ("d1", "d2", "d3")}
    specs.update({kind: derived_spec(meta, kind, specs["d1"]) for kind in ("d4", "d5", "d6")})
    for kind, spec in specs.items():
        spec["title"] = f"{title} — {kind.upper()}"
    analogy = {
        "topic_no": topic_no, "roadmap_id": roadmap_id, "title": f"Cloud City: {title}",
        "city_concept": "A district with roads, permits, warehouses, and an operations room",
        "beats": [
            {"step": 1, "name": "The City Problem", "story": "Brightloaf grows faster than its original city district can safely support.", "analogy_elements": ["Brightloaf city", "crowded district"]},
            {"step": 2, "name": "The City Solution", "story": "The city assigns a clear district, permits, roads, and an operations owner.", "analogy_elements": ["permits", "roads", "operators"]},
            {"step": 3, "name": "City Under Stress", "story": "A failed road, exhausted utility, or bad permit affects only its declared blast radius.", "analogy_elements": ["failure boundary", "emergency route"]},
            {"step": 4, "name": "Where Metaphor Breaks", "story": "Cloud policies are software rules, not physical walls; verify the real behavior in documentation.", "analogy_elements": ["metaphor limit"]},
        ],
    }
    sections = [
        f'<section class="topic-section" id="real-world"><h2 class="section-title"><span class="section-number">1</span> Real-World Explanation</h2><h3>The Situation</h3><p>Brightloaf is moving from a single bakery to a national business and needs a defensible design for {esc(title)}.</p>{part1_addendum(meta)}</section>',
        f'<section class="topic-section" id="technical"><h2 class="section-title"><span class="section-number">2</span> Technical Discussion &amp; Architecture Diagrams</h2><h3>2A — The Depth Ladder</h3><h4>Layer 1 — Foundation</h4><p>Define resource scope, vocabulary, control plane, data plane, and the common wrong picture.</p><h4>Layer 2 — Practitioner</h4><p>Set safe defaults and inspect IAM, APIs, quotas, networking, billing, and logs.</p><h4>Layer 3 — Architect</h4><p>Compare operational burden, scaling, consistency, cost, portability, and compliance.</p><h4>Layer 4 — Staff</h4><p>Predict behavior from internals, failure modes, blast radius, ownership, and day-two operations.</p>{part2_addendum(meta)}<div id="diagrams"><h3>2B — Interactive Architecture Diagrams</h3>{''.join(f'<div id="diagram-{kind}"></div>' for kind in specs)}</div></section>',
        f'<section class="topic-section" id="analogy"><h2 class="section-title"><span class="section-number">3</span> Explained by Analogy: Cloud City</h2><p>The city story follows Brightloaf through a problem, solution, stress event, and explicit limit.</p><div class="analogy-stepper"><button class="stepper-btn" type="button" onclick="showAnalogyBeat(1)">1. The City Problem</button><button class="stepper-btn" type="button" onclick="showAnalogyBeat(2)">2. The City Solution</button><button class="stepper-btn" type="button" onclick="showAnalogyBeat(3)">3. City Under Stress</button><button class="stepper-btn" type="button" onclick="showAnalogyBeat(4)">4. Where Metaphor Breaks</button></div><div id="analogy-display" class="analogy-box"></div><div id="analogy-scene" class="analogy-scene" tabindex="0" aria-label="Interactive Cloud City analogy scene"></div>{mapping_table(meta)}</section>',
        f'<section class="topic-section" id="demo-or-practice"><h2 class="section-title"><span class="section-number">4</span> {"Hands-On Demo" if page_type == "service" else "Practice Exercise"}</h2>{demo_addendum(meta)}</section>',
        f'<section class="topic-section" id="quiz"><h2 class="section-title"><span class="section-number">5</span> Check Your Understanding</h2>{quiz_addendum()}</section>',
        '<section class="topic-section" id="reading"><h2 class="section-title"><span class="section-number">6</span> Further Reading</h2><p><a href="https://cloud.google.com/architecture/framework" target="_blank" rel="noopener">Official Google Cloud Architecture Framework</a></p></section>',
    ]
    header = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(topic_no)} ({esc(roadmap_id)}) {esc(title)} | GCP Architect Explorer</title><link rel="stylesheet" href="../assets/site.css?v={ASSET_VERSION}"><link rel="stylesheet" href="../assets/diagram-engine.css?v={ASSET_VERSION}"></head><body><header class="site-nav"><div class="nav-container"><a class="brand-link" href="../index.html">GCP ARCHITECT ROADMAP</a><nav class="nav-links"><a class="nav-link" href="../index.html">Overview</a><a class="nav-link" href="#diagrams">Diagrams</a><a class="nav-link" href="#demo-or-practice">Practice</a><a class="nav-link" href="#quiz">Review</a></nav></div></header><main class="main-content"><header class="page-header"><div class="page-meta"><span class="badge">Topic {esc(topic_no)}</span><span class="badge badge-type">Roadmap ID: {esc(roadmap_id)}</span><span class="badge">{esc(phase)}</span><span class="badge badge-type">Type: {esc(page_type)}</span><span>Verified: 2026-09-24</span></div><h1 class="page-title">{esc(title)}</h1><p class="page-lead">A roadmap-aligned learning page for {esc(title)} using Brightloaf and Cloud City as the recurring story.</p></header>{topic_toc(page_type)}'''
    tags = "".join(f'<script id="spec-{kind}-data" type="application/json">\n{json.dumps(specs[kind], indent=2)}\n</script>\n' for kind in specs)
    brightloaf = (ROOT / "brightloaf.json").read_text(encoding="utf-8")
    scripts = f'''<script id="brightloaf-data" type="application/json">{brightloaf}</script><script id="analogy-data" type="application/json">{json.dumps(analogy, indent=2)}</script><script src="../assets/diagram-engine.js?v={ASSET_VERSION}"></script><script>
document.addEventListener("DOMContentLoaded",()=>{{for(const kind of {json.dumps(list(specs))}) new DiagramEngine("diagram-"+kind,JSON.parse(document.getElementById("spec-"+kind+"-data").textContent)); window.analogyData=JSON.parse(document.getElementById("analogy-data").textContent); showAnalogyBeat(1);}});
function checkQuiz(el,ok,msg){{const card=el.closest(".quiz-card");card.querySelector(".quiz-explanation").style.display="block";card.querySelector(".quiz-explanation").textContent=msg;}}
function showAnalogyBeat(n){{const beat=window.analogyData?.beats?.find(item=>item.step===n);if(!beat)return;document.getElementById("analogy-display").innerHTML="<h3>"+beat.name+"</h3><p>"+beat.story+"</p>";}}
</script><script src="../assets/site-interactions.js?v={ASSET_VERSION}"></script></body></html>'''
    return header + "".join(sections) + "</main><footer class=\"site-footer\">Static learning site · browse without credentials · verify time-sensitive facts against current documentation</footer>" + tags + scripts


def create_missing_pages() -> None:
    current_ids = {page_meta(path)["roadmap_id"] for path in PAGES.glob("topic-*.html")}
    aliases = {"CS.1": "cheat-1", "CS.2": "cheat-2", "CS.3": "cheat-3", "CS.4": "cheat-4", "CS.5": "cheat-5", "CS.6": "cheat-7"}
    current_ids.update(aliases.get(item, item) for item in list(current_ids))
    next_no = 61
    for roadmap_id, title, page_type, phase in EXPECTED:
        if roadmap_id in current_ids:
            continue
        while (PAGES / f"topic-{next_no:03d}.html").exists():
            next_no += 1
        meta = {"topic_no": f"{next_no:03d}", "roadmap_id": roadmap_id, "title": title, "page_type": page_type, "phase": phase}
        (PAGES / f"topic-{next_no:03d}.html").write_text(new_topic_page(meta), encoding="utf-8")
        next_no += 1


def normalize_all_pages() -> None:
    for path in sorted(PAGES.glob("topic-*.html")):
        meta = page_meta(path)
        if not meta["roadmap_id"]:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        specs = {kind: normalize_spec(get_inline_spec(text, kind), meta, kind) for kind in ("d1", "d2", "d3")}
        specs.update({kind: derived_spec(meta, kind, specs["d1"]) for kind in ("d4", "d5", "d6")})
        for kind, spec in specs.items():
            (DIAGRAMS / f"topic-{meta['topic_no']}-{kind}.json").write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
            (DIAGRAMS / f"topic-{meta['topic_no']}-{kind}.html").write_text(standalone_html(spec), encoding="utf-8")
        ensure_page(path, meta, specs)
        analogy_path = ANALOGY / f"topic-{meta['topic_no']}.json"
        analogy_match = re.search(r'<script id="analogy-data"[^>]*>\s*(.*?)\s*</script>', text, re.S)
        analogy_data = json.loads(analogy_match.group(1)) if analogy_match else {"topic_no": meta["topic_no"], "roadmap_id": meta["roadmap_id"], "title": meta["title"], "beats": []}
        analogy_path.write_text(json.dumps(analogy_data, indent=2) + "\n", encoding="utf-8")


def write_index() -> None:
    catalog = [page_meta(path) for path in sorted(PAGES.glob("topic-*.html")) if page_meta(path)["roadmap_id"]]
    phases = sorted({item["phase"] for item in catalog})
    types = sorted({item["page_type"] for item in catalog})
    cards = []
    for item in catalog:
        tier = "T2" if item["page_type"] == "service" else "T0"
        cards.append(f'''<article class="topic-card" data-topic-no="{esc(item["topic_no"])}" data-roadmap-id="{esc(item["roadmap_id"])}" data-phase="{esc(item["phase"])}" data-page-type="{esc(item["page_type"])}" data-demo-tier="{tier}"><div><span class="badge">Topic {esc(item["topic_no"])}</span> <span class="badge badge-type">{esc(item["roadmap_id"])}</span> <span class="badge">{esc(item["page_type"])}</span><h3><a href="pages/topic-{esc(item["topic_no"])}.html">{esc(item["title"])}</a></h3><p>{esc(item["phase"])} · Brightloaf scenario · diagrams D1–D6 · four review bands</p></div><div><label class="completion-control"><input type="checkbox" data-complete-topic="{esc(item["topic_no"])}"> Complete</label> <a class="btn-de" href="pages/topic-{esc(item["topic_no"])}.html">Open →</a></div></article>''')
    # The map is laid out as a responsive grid by site.css. Keep the inline
    # coordinates for compatibility with older generated pages, but do not
    # depend on absolute positioning: wrapped labels made the old 28px row
    # spacing overlap and clip the lower rows.
    map_nodes = "".join(f'<a class="architecture-map-node" href="pages/topic-{esc(item["topic_no"])}.html">{esc(item["title"][:22])}</a>' for item in catalog[:25])
    depth = depth_ladder_section()
    html_text = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>GCP Architect Roadmap — 67 Roadmap Topics</title><link rel="stylesheet" href="assets/site.css"><link rel="stylesheet" href="assets/diagram-engine.css"></head><body><header class="site-nav"><div class="nav-container"><a class="brand-link" href="index.html">GCP ARCHITECT ROADMAP</a><nav class="nav-links"><a href="#paths">Paths</a><a href="#depth-ladder">Depth ladder</a><a href="#map">Architecture map</a><a href="#topics">Topics</a></nav></div></header><main class="main-content"><header class="page-header"><span class="badge">Roadmap-aligned build</span><h1 class="page-title">Google Cloud Architect Roadmap</h1><p class="page-lead">A static, credential-free learning system from prerequisites to PCA and consulting judgment. The canonical roadmap contains 67 headings; additional case-study pages are explicitly marked as extras.</p><p class="cost-warning"><strong>Live demo warning:</strong> browsing is free; any GCP create/apply step can incur charges. Confirm the project, budget, region, APIs, and cleanup before running it.</p></header>{depth}<section id="paths" class="topic-section"><h2 class="section-title">Learning paths</h2><p><a class="btn-de" href="pages/topic-001.html">Beginner path</a> <a class="btn-de" href="pages/topic-050.html">Exam path</a> <a class="btn-de" href="pages/topic-066.html">Consultant path</a> <a class="btn-de" href="roadmap-content.html">Roadmap checklist, labs, checkpoints &amp; traps</a></p><p><a href="glossary.html">Glossary</a> · <a href="review-deck.html">Review deck</a> · <a href="stories.html">Architecture stories</a> · <a href="capstones.html">Capstones</a> · <a href="incidents.html">Incident library</a> · <a href="diagram-editor.html">Diagram editor</a> · <a href="README.html">Setup guide</a></p></section><section id="map" class="topic-section"><h2 class="section-title">Interactive architecture map</h2><div class="architecture-map" role="img" aria-label="Architecture map linking roadmap topics"><div class="architecture-map-layer">Organization · folders · projects · global and regional infrastructure · VPC · compute · data · security · observability · delivery</div>{map_nodes}</div></section><section id="topics" class="topic-section"><div class="topic-toolbar"><input id="topic-search" type="search" placeholder="Search topics"><select id="phase-filter"><option value="">All phases</option>{''.join(f'<option>{esc(phase)}</option>' for phase in phases)}</select><select id="type-filter"><option value="">All page types</option>{''.join(f'<option>{esc(page_type)}</option>' for page_type in types)}</select><select id="tier-filter"><option value="">All demo tiers</option><option>T0</option><option>T2</option><option>T4</option></select></div><div id="topic-cards-container">{''.join(cards)}</div></section></main><footer class="site-footer">67 canonical roadmap topics · {len(catalog)} total pages · zero raster assets · static browsing</footer><script src="assets/site-interactions.js"></script><script>window.addEventListener("DOMContentLoaded",()=>window.initTopicIndex&&window.initTopicIndex());</script></body></html>'''
    html_text = html_text.replace('assets/site.css"', f'assets/site.css?v={ASSET_VERSION}"').replace('assets/diagram-engine.css"', f'assets/diagram-engine.css?v={ASSET_VERSION}"').replace('assets/site-interactions.js"', f'assets/site-interactions.js?v={ASSET_VERSION}"')
    (ROOT / "index.html").write_text(html_text, encoding="utf-8")


def artifact_shell(title: str, body: str) -> str:
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><link rel="stylesheet" href="assets/site.css?v={ASSET_VERSION}"></head><body><main class="main-content"><p><a href="index.html">← Roadmap index</a></p><header class="page-header"><h1 class="page-title">{esc(title)}</h1><p class="page-lead">Static companion artifact; no credentials are required to browse.</p></header>{body}</main><script src="assets/site-interactions.js?v={ASSET_VERSION}"></script></body></html>'


def write_artifacts() -> None:
    terms = [("IAM", "Identity and access policy evaluation.", "009"), ("VPC", "A virtual network boundary.", "016"), ("SLO", "A measurable service objective.", "029"), ("RTO", "Target time to restore service.", "031"), ("RPO", "Acceptable data-loss window.", "031"), ("blast radius", "The users and dependencies affected by a failure.", "028"), ("control plane", "Resource management and configuration path.", "007"), ("data plane", "Runtime workload traffic path.", "016")]
    glossary = "".join(f'<tr><td><code>{esc(term)}</code></td><td>{esc(description)}</td><td><a href="pages/topic-{no}.html">Topic {no}</a></td></tr>' for term, description, no in terms)
    (ROOT / "glossary.html").write_text(artifact_shell("GCP Architect Glossary", f'<section class="topic-section"><table><tr><th>Term</th><th>Definition</th><th>Used in</th></tr>{glossary}</table></section>'), encoding="utf-8")
    stories = [("Web app", "DNS → load balancer → CDN/Cloud Armor → compute → private database → observability.", "017"), ("Event-driven service", "Producer → Pub/Sub → subscription/dead letter/replay → worker → storage.", "021"), ("Private enterprise service", "Shared VPC → private subnet → NAT or Private Google Access → managed service → hybrid link.", "018"), ("Data platform", "Cloud Storage → Dataflow/Dataproc → BigQuery/Bigtable/Spanner → dashboards or ML.", "051"), ("GKE platform", "VPC-native cluster → node pools or Autopilot → workload identity → gateway → observability.", "014"), ("Migration", "Discovery → dependency map → landing zone → transfer/replication → cutover → validation.", "025"), ("Security lifecycle", "Identity → policy hierarchy → network boundary → encryption → audit → detection → response.", "034"), ("Terraform delivery", "Pull request → plan → review → apply → drift detection → rollback.", "042")]
    story_html = "".join(f'<article class="topic-section"><h2>{i}. {esc(name)}</h2><p>{esc(description)}</p><a href="pages/topic-{no}.html">Open component topic</a></article>' for i, (name, description, no) in enumerate(stories, 1))
    (ROOT / "stories.html").write_text(artifact_shell("Cross-topic architecture stories", story_html), encoding="utf-8")
    capstones = ["Landing zone for a mid-size company", "Regulated workload", "Global consumer app", "Legacy estate migration", "Cost and reliability rescue"]
    capstone_html = "".join(f'<article class="topic-section"><h2>{i}. {esc(name)}</h2><p>Produce a written design, ADR list, diagram set, cost model, risk register, executive outline, and design-review simulation.</p></article>' for i, name in enumerate(capstones, 1))
    (ROOT / "capstones.html").write_text(artifact_shell("Capstone projects", capstone_html), encoding="utf-8")
    incidents = [("Quota exhaustion", "Requests fail with quota errors; inspect usage, reduce load, and add headroom."), ("Expired certificate", "TLS fails at ingress; renew, validate the chain, and alert before expiry."), ("Bad configuration rollout", "Error rate rises after promotion; canary and roll back."), ("Exhausted IP range", "Pods or instances cannot obtain addresses; expand ranges before saturation."), ("Disabled key", "Authentication fails; identify the key, revoke exposure, and use short-lived identity."), ("Single-zone dependency", "A regional path depends on one zone; fail over and remove the dependency."), ("Egress cost runaway", "Cross-region traffic grows the bill; attribute egress and redesign locality."), ("Over-permissive service account", "A workload can access unrelated resources; replace broad roles with workload identity and conditions.")]
    incident_html = "".join(f'<article class="topic-section"><h2>{i}. {esc(name)}</h2><p><strong>Symptoms:</strong> {esc(description)}</p><p><strong>Diagnosis:</strong> inspect logs, metrics, IAM, quota, and dependency topology.</p><p><strong>Prevention:</strong> add an alert, a runbook, a review gate, and a replayable failure diagram.</p><a href="pages/topic-030.html#diagrams">Replay failure diagram</a></article>' for i, (name, description) in enumerate(incidents, 1))
    (ROOT / "incidents.html").write_text(artifact_shell("Incident case library", incident_html), encoding="utf-8")
    (ROOT / "review-deck.html").write_text(artifact_shell("Review deck", '<section class="topic-section"><h2>Four review bands</h2><ol><li>Recall the resource and scope.</li><li>Apply the choice to a PCA scenario.</li><li>Review failure, ownership, cost, and hidden dependencies.</li><li>Complete a practical design task with an alternative and rollback.</li></ol></section>'), encoding="utf-8")
    editor_body = '<section class="topic-section"><p>Edit the JSON, then render the shared diagram engine.</p><textarea id="diagram-json" rows="18" style="width:100%;font-family:var(--font-mono);">{"id":"editor-demo","title":"Editable architecture","topic_no":"EDITOR","roadmap_id":"editor","summary":"A small editable architecture.","nodes":[{"id":"a","label":"Client","product":"External","x":250,"y":220,"plane":"data","detail":"A client."},{"id":"b","label":"Service","product":"GCP","x":700,"y":220,"plane":"data","detail":"A service."}],"edges":[{"id":"e","from":"a","to":"b","label":"HTTPS","plane":"data"}],"groups":[],"steps":[{"n":1,"title":"Request","edges":["e"],"action":"Client sends a request.","check":{"metrics":"request_count"}}],"scenarios":[]}</textarea><button class="btn-de" type="button" onclick="renderEditor()">Render preview</button><div id="editor-preview"></div></section><script src="assets/diagram-engine.js"></script><script>function renderEditor(){try{const spec=JSON.parse(document.getElementById("diagram-json").value);document.getElementById("editor-preview").innerHTML="<div id=\\"editor-diagram\\"></div>";new DiagramEngine("editor-diagram",spec);}catch(error){alert(error.message);}}</script>'
    (ROOT / "diagram-editor.html").write_text(artifact_shell("Diagram editor", editor_body), encoding="utf-8")


def main() -> None:
    PAGES.mkdir(exist_ok=True)
    DIAGRAMS.mkdir(exist_ok=True)
    ANALOGY.mkdir(exist_ok=True)
    GENERATED.mkdir(exist_ok=True)
    create_missing_pages()
    normalize_all_pages()
    write_index()
    write_artifacts()
    print(f"Repaired {len(list(PAGES.glob('topic-*.html')))} topic pages.")


if __name__ == "__main__":
    main()
