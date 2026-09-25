#!/usr/bin/env python3
"""Normalize the generated site against the roadmap/site contract."""

from __future__ import annotations

import html
import json
import re
import argparse
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
ROADMAP_ITEMS: dict[str, list[str]] = {}


def load_roadmap_items(source: Path | None) -> dict[str, list[str]]:
    """Read checklist items from the roadmap so page prose has real topic anchors."""
    if not source or not source.is_file():
        return {}
    sections: dict[str, list[str]] = {}
    current_id = ""
    current_title = ""
    for raw in source.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        heading = re.match(r"^###\s+([^\s]+)\s+(.+)$", line)
        if heading:
            current_id = heading.group(1)
            current_title = heading.group(2).strip()
            sections[current_id] = []
            sections[current_title.casefold()] = sections[current_id]
            continue
        item = re.match(r"^-\s+\[[ xX]\]\s+(.+)$", line)
        if item and current_id:
            sections[current_id].append(item.group(1).strip())

    aliases = {
        "cheat-1": "Compute: which one?",
        "cheat-2": "Database: which one?",
        "cheat-3": "Load balancer: which one?",
        "cheat-4": "Hybrid connectivity: which one?",
        "cheat-5": "Storage: which one?",
        "cheat-6": "Messaging: which one?",
        "cheat-7": "Key numbers to memorise",
    }
    result: dict[str, list[str]] = {}
    for roadmap_id, title, _page_type, _phase in EXPECTED:
        items = sections.get(roadmap_id, [])
        if not items and roadmap_id in aliases:
            items = sections.get(aliases[roadmap_id].casefold(), [])
        if items:
            result[roadmap_id] = items
    return result


def tail_node(node_id: str, label: str, product: str, plane: str, x: int, y: int, detail: str) -> dict:
    return {
        "id": node_id, "label": label, "product": product, "group": "root",
        "plane": plane, "x": x, "y": y, "detail": detail,
    }


def tail_edge(edge_id: str, source: str, target: str, label: str, plane: str) -> dict:
    return {"id": edge_id, "from": source, "to": target, "label": label, "plane": plane}


# Topics 061–071 are the reference/consulting tail of the roadmap. Their
# original generated diagrams were one-node fallbacks. These profiles give
# each topic a real decision path that can be reused across its six lenses.
TAIL_PROFILES = {
    "061": {
        "title": "Case reading technique",
        "summary": "Extract measurable requirements and watchpoints from a cloud architecture case before choosing services.",
        "focus": "numbers, hidden adjectives, stated versus implied needs, and out-of-scope boundaries",
        "nodes": [
            tail_node("brief", "Exam Case Brief", "Case study source", "control", 120, 220, "The narrative containing business goals, constraints, and signals."),
            tail_node("numbers", "Measured Facts", "Users, RPS, TB, latency, RTO/RPO, budget", "control", 330, 120, "Numbers that turn a vague case into testable requirements."),
            tail_node("requirements", "Requirement Ledger", "Functional and non-functional needs", "control", 520, 220, "A separated list of stated needs and inferred needs."),
            tail_node("watchpoints", "Watchpoint Register", "Conflicts, compliance, skills", "control", 710, 120, "Risks hidden behind words such as global, regulated, spiky, or legacy."),
            tail_node("capabilities", "GCP Capability Map", "Services and architecture patterns", "data", 710, 320, "A traceable mapping from each requirement to a cloud capability."),
            tail_node("scope", "Explicit Out-of-Scope", "Excluded requirements", "control", 520, 360, "Constraints that must not accidentally enter the design."),
        ],
        "edges": [
            tail_edge("e1", "brief", "numbers", "extract facts", "control"),
            tail_edge("e2", "numbers", "requirements", "quantify", "control"),
            tail_edge("e3", "requirements", "watchpoints", "challenge assumptions", "control"),
            tail_edge("e4", "requirements", "capabilities", "map to GCP", "control"),
            tail_edge("e5", "brief", "scope", "mark exclusions", "control"),
        ],
        "failures": [
            ("missed-number", "A number is missed", "numbers", "A scale, latency, budget, or recovery figure is not captured.", "Re-read the case and add the value to the requirement ledger."),
            ("hidden-constraint", "A hidden constraint is ignored", "watchpoints", "An adjective conceals regulatory, geographic, or operational risk.", "Turn the adjective into an explicit question and review it."),
            ("untraceable-choice", "A service choice has no requirement", "capabilities", "The proposed capability cannot be traced back to a case requirement.", "Reject the orphan choice or document the missing requirement."),
        ],
    },
    "062": {
        "title": "Discovery question bank",
        "summary": "Move from a client business driver to measurable availability, load, data, risk, and success criteria.",
        "focus": "business driver, availability and recovery targets, load shape, data location, constraints, and success measures",
        "nodes": [
            tail_node("sponsor", "Client Sponsor", "Business owner", "control", 100, 220, "The stakeholder who explains why the project exists."),
            tail_node("driver", "Business Driver", "Revenue, time-to-market, risk", "control", 270, 120, "The outcome that should anchor all technical questions."),
            tail_node("slo", "Availability / RTO / RPO", "SLO and recovery targets", "control", 470, 220, "The measurable service and recovery objectives."),
            tail_node("load", "Peak and Average Load", "Throughput and latency profile", "data", 650, 120, "The traffic shape, not just a single peak number."),
            tail_node("residency", "Data and Regulation", "Geography and compliance", "control", 650, 320, "Where users and data may legally or operationally reside."),
            tail_node("estate", "Existing Systems and Skills", "Integrations and team capability", "control", 470, 380, "Constraints that shape migration, operations, and supportability."),
            tail_node("success", "Success Measures", "Business and technical KPIs", "control", 850, 220, "How the customer will decide the architecture worked."),
        ],
        "edges": [
            tail_edge("e1", "sponsor", "driver", "why now?", "control"),
            tail_edge("e2", "driver", "slo", "what must hold?", "control"),
            tail_edge("e3", "slo", "load", "size the service", "control"),
            tail_edge("e4", "slo", "residency", "bound the design", "control"),
            tail_edge("e5", "residency", "estate", "check constraints", "control"),
            tail_edge("e6", "load", "success", "measure outcome", "control"),
        ],
        "failures": [
            ("wrong-driver", "The solution answers the wrong driver", "driver", "Technical activity is mistaken for the business outcome.", "Restate the driver and obtain sponsor confirmation."),
            ("unmeasured-target", "Targets remain qualitative", "slo", "No availability, recovery, latency, or cost threshold can be tested.", "Write measurable targets and the evidence source for each."),
            ("missing-constraint", "A residency or skill constraint arrives late", "residency", "The chosen architecture cannot satisfy geography, regulation, or team capability.", "Add the constraint to the decision record before service selection."),
        ],
    },
    "063": {
        "title": "Practice case studies",
        "summary": "Turn a timed case prompt into a one-page design, diagram, ADR set, cost estimate, and peer critique.",
        "focus": "official cases, one-page designs, diagrams, ADRs, cost estimates, time-boxing, and architecture-framework critique",
        "nodes": [
            tail_node("prompt", "Case Prompt", "Official or invented scenario", "control", 100, 220, "The bounded case to solve under a time limit."),
            tail_node("design", "One-Page Design", "Goals, constraints, requirements", "control", 290, 120, "A concise design with a reason for each major choice."),
            tail_node("diagram", "Architecture Diagram", "Flows, boundaries, failure domains", "data", 500, 220, "A visual explanation of components and traffic paths."),
            tail_node("adr", "ADR Set", "Decisions and rejected alternatives", "control", 710, 120, "Decision records that preserve context and consequences."),
            tail_node("cost", "Rough Cost Estimate", "Assumptions and unit economics", "control", 710, 320, "A directional cost model that exposes its assumptions."),
            tail_node("critique", "Peer Critique", "Five architecture framework pillars", "control", 500, 380, "A review that tests trade-offs, risks, and missing evidence."),
            tail_node("timer", "30-Minute Timer", "Exam-style pacing", "control", 290, 320, "The constraint that forces prioritisation and a defensible answer."),
        ],
        "edges": [
            tail_edge("e1", "prompt", "design", "extract requirements", "control"),
            tail_edge("e2", "design", "diagram", "explain topology", "data"),
            tail_edge("e3", "diagram", "adr", "justify choices", "control"),
            tail_edge("e4", "diagram", "cost", "price assumptions", "control"),
            tail_edge("e5", "timer", "design", "time-box", "control"),
            tail_edge("e6", "adr", "critique", "review trade-offs", "control"),
        ],
        "failures": [
            ("scope-creep", "The case exceeds the time box", "timer", "Research expands while the required design remains unfinished.", "Write assumptions, time-box discovery, and move open questions to risks."),
            ("diagram-gap", "The design cannot be explained visually", "diagram", "The diagram omits a dependency, boundary, or failure domain.", "Trace every requirement through a node and an edge."),
            ("unsupported-adr", "An ADR has no evidence", "adr", "The recommendation is asserted without a rejected alternative or cost impact.", "Add assumptions, evidence, consequences, and a verification date."),
        ],
    },
    "064": {
        "title": "Messaging selection",
        "summary": "Select Pub/Sub, Cloud Tasks, Eventarc, or Workflows from delivery, ordering, rate-control, and orchestration requirements.",
        "focus": "fan-out, rate control, event triggers, orchestration, ordering, replay, and dead-letter handling",
        "nodes": [
            tail_node("producer", "Order / Event Producer", "Application or Google service", "data", 90, 220, "The system that emits work or an event."),
            tail_node("decision", "Messaging Decision", "Delivery and control requirements", "control", 280, 220, "The choice point for delivery, fan-out, rate, and orchestration."),
            tail_node("pubsub", "Pub/Sub Topic", "Fan-out and durable messaging", "data", 500, 90, "Decoupled asynchronous delivery with subscriptions, replay, and dead lettering."),
            tail_node("tasks", "Cloud Tasks Queue", "Rate-controlled task delivery", "data", 500, 220, "Targeted delivery with retries and per-queue rate control."),
            tail_node("eventarc", "Eventarc Trigger", "Event-driven routing", "control", 500, 350, "Routes supported provider or custom events to a target."),
            tail_node("workflow", "Workflows", "Multi-step orchestration", "control", 700, 220, "Coordinates steps, retries, and service calls."),
            tail_node("consumer", "Consumer Service", "Cloud Run / GKE / function", "data", 880, 220, "Processes the message or event and reports outcome."),
            tail_node("recovery", "DLQ / Replay / Retry", "Failure handling", "control", 700, 380, "Prevents poison messages from silently disappearing."),
        ],
        "edges": [
            tail_edge("e1", "producer", "decision", "publish work", "data"),
            tail_edge("e2", "decision", "pubsub", "fan-out / replay", "control"),
            tail_edge("e3", "decision", "tasks", "rate-control", "control"),
            tail_edge("e4", "decision", "eventarc", "react to event", "control"),
            tail_edge("e5", "decision", "workflow", "orchestrate steps", "control"),
            tail_edge("e6", "pubsub", "consumer", "deliver message", "data"),
            tail_edge("e7", "tasks", "consumer", "deliver task", "data"),
            tail_edge("e8", "consumer", "recovery", "retry / dead letter", "control"),
        ],
        "failures": [
            ("wrong-delivery-model", "The selected service cannot meet delivery semantics", "decision", "Fan-out, rate control, event routing, or orchestration needs are mismatched.", "Re-evaluate the requirement matrix before implementation."),
            ("poison-message", "A consumer repeatedly fails", "consumer", "Retries amplify load or a message blocks useful work.", "Use bounded retries, dead lettering, and an operator replay path."),
            ("unbounded-workflow", "Orchestration grows without a boundary", "workflow", "A multi-step process has no timeout, idempotency, or compensation plan.", "Set explicit timeouts and record compensating actions."),
        ],
    },
    "065": {
        "title": "Google Cloud Skills Boost platform plan",
        "summary": "Sequence Cloud Skills Boost learning paths and specialist quests into an evidence-backed architect practice plan.",
        "focus": "learning-path sequencing, hands-on labs, budget alerts, project safety, checkpoints, and evidence capture",
        "nodes": [
            tail_node("learner", "Learner Goal", "PCA and architecture judgment", "control", 90, 220, "The outcome that determines which learning path is next."),
            tail_node("digital", "Cloud Digital Leader", "Optional warm-up", "control", 270, 100, "Business framing and low-pressure cloud vocabulary."),
            tail_node("engineer", "Cloud Engineer Path", "Core infrastructure labs", "control", 470, 220, "Hands-on networking, compute, storage, and operations foundation."),
            tail_node("pca", "PCA Learning Path", "Professional Cloud Architect", "control", 680, 100, "Architecture trade-offs, case analysis, and exam preparation."),
            tail_node("quests", "Specialist Quests", "Networking, security, Kubernetes, data", "control", 680, 340, "Optional depth after the core path."),
            tail_node("lab", "Disposable Lab Project", "Trial or free-tier project", "data", 470, 380, "A guarded project with region, IAM, budget, and cleanup controls."),
            tail_node("evidence", "Evidence Log", "Screenshots, ADRs, notes, checkpoints", "control", 880, 220, "Proof of what was learned and what remains to verify."),
        ],
        "edges": [
            tail_edge("e1", "learner", "digital", "optional warm-up", "control"),
            tail_edge("e2", "learner", "engineer", "build foundation", "control"),
            tail_edge("e3", "engineer", "pca", "advance to architecture", "control"),
            tail_edge("e4", "pca", "quests", "add specialist depth", "control"),
            tail_edge("e5", "engineer", "lab", "practice safely", "data"),
            tail_edge("e6", "lab", "evidence", "capture result", "control"),
            tail_edge("e7", "pca", "evidence", "pass checkpoint", "control"),
        ],
        "failures": [
            ("path-skipping", "A learner skips the foundation", "engineer", "Advanced labs are attempted without the networking or IAM model needed to explain them.", "Return to the prerequisite path and record the missing concept."),
            ("unsafe-lab", "A lab project has no guardrails", "lab", "Credentials, budget, region, or cleanup controls are missing.", "Set the project guard, budget alert, least privilege, and destroy step first."),
            ("no-evidence", "Completion cannot be demonstrated", "evidence", "A lab was run but its decision, result, or checkpoint was not recorded.", "Capture the architecture, observation, cost, and next verification."),
        ],
    },
    "066": {
        "title": "Consultant communication and delivery",
        "summary": "Turn discovery into executive outcomes, engineering constraints, options, a recommendation, and an agreed delivery record.",
        "focus": "workshops, executive outcomes, engineering detail, options, proposals, assumptions, risks, and review feedback",
        "nodes": [
            tail_node("workshop", "Discovery Workshop", "Questions and stakeholder map", "control", 100, 220, "The facilitated session that exposes outcomes, constraints, and risks."),
            tail_node("executive", "Executive Outcome", "Risk, cost, time-to-value", "control", 300, 100, "The concise story for decision-makers."),
            tail_node("engineering", "Engineering Constraints", "Latency, integration, operations", "control", 300, 340, "The detail engineers need to validate feasibility."),
            tail_node("options", "Options Matrix", "Alternatives and weighted criteria", "control", 520, 220, "At least two viable options with explicit trade-offs."),
            tail_node("proposal", "Proposal / SOW", "Scope, assumptions, deliverables", "control", 720, 100, "The delivery contract and boundaries."),
            tail_node("risks", "Assumptions and Risk Log", "Open questions and mitigations", "control", 720, 340, "Uncertainty that needs an owner and a next action."),
            tail_node("decision", "Recommendation and Review", "Decision and feedback", "control", 920, 220, "The selected path and the feedback loop that keeps it honest."),
        ],
        "edges": [
            tail_edge("e1", "workshop", "executive", "frame outcome", "control"),
            tail_edge("e2", "workshop", "engineering", "capture constraints", "control"),
            tail_edge("e3", "executive", "options", "compare value", "control"),
            tail_edge("e4", "engineering", "options", "compare feasibility", "control"),
            tail_edge("e5", "options", "proposal", "scope the work", "control"),
            tail_edge("e6", "options", "risks", "record uncertainty", "control"),
            tail_edge("e7", "proposal", "decision", "recommend and review", "control"),
        ],
        "failures": [
            ("single-option", "The recommendation has no alternative", "options", "The client cannot see what was rejected or what the trade-off buys.", "Present multiple options with weighted criteria and consequences."),
            ("scope-drift", "The delivery boundary is ambiguous", "proposal", "Assumptions become commitments and change requests arrive late.", "Make scope, exclusions, deliverables, and verification dates explicit."),
            ("unowned-risk", "A risk is recorded without an owner", "risks", "An open question persists through approval and delivery.", "Assign an owner, mitigation, evidence, and escalation path."),
        ],
    },
    "067": {
        "title": "Architecture deliverables",
        "summary": "Assemble the architecture artifacts needed to move from requirements through decisions, cost, security, recovery, and operations handover.",
        "focus": "requirements, diagrams, ADRs, cost estimates, security mapping, migration plans, DR plans, and runbooks",
        "nodes": [
            tail_node("requirements", "Requirements Baseline", "Business and technical needs", "control", 90, 220, "The measurable requirements that every artifact must answer."),
            tail_node("diagram", "Architecture Diagram", "Context, flows, boundaries", "data", 280, 100, "The visual topology and failure domains."),
            tail_node("adr", "Decision Records", "ADRs and alternatives", "control", 280, 340, "Why each major design choice was made."),
            tail_node("cost", "Cost Estimate", "Assumptions and unit economics", "control", 500, 220, "A quantified cost view with assumptions."),
            tail_node("security", "Security Mapping", "Controls and compliance", "control", 700, 100, "Identity, data, network, and audit controls mapped to requirements."),
            tail_node("dr", "DR Plan", "RTO, RPO, tests", "control", 700, 340, "Recovery design, runbook, and test result."),
            tail_node("handover", "Operations Handover", "Runbooks and ownership", "control", 900, 220, "The team, signals, escalation, and day-two operating model."),
        ],
        "edges": [
            tail_edge("e1", "requirements", "diagram", "visualise", "control"),
            tail_edge("e2", "requirements", "adr", "decide", "control"),
            tail_edge("e3", "diagram", "cost", "size and price", "control"),
            tail_edge("e4", "adr", "cost", "quantify trade-off", "control"),
            tail_edge("e5", "diagram", "security", "map controls", "control"),
            tail_edge("e6", "diagram", "dr", "model failure", "control"),
            tail_edge("e7", "security", "handover", "operate safely", "control"),
            tail_edge("e8", "dr", "handover", "hand over recovery", "control"),
        ],
        "failures": [
            ("orphan-artifact", "An artifact does not trace to a requirement", "diagram", "The document looks complete but cannot justify a component or control.", "Add a requirement reference to the diagram, ADR, and review checklist."),
            ("unpriced-design", "Cost assumptions are missing", "cost", "A recommendation is approved without a cost range or unit driver.", "Record assumptions, sensitivity, and an owner for current pricing verification."),
            ("handover-gap", "Operations cannot recover the service", "handover", "Runbooks, ownership, signals, or DR tests are absent.", "Run the handover review and rehearse the recovery path."),
        ],
    },
    "068": {
        "title": "Portfolio and career",
        "summary": "Build a credible architect portfolio from documented projects, decisions, cost models, Terraform, writing, and deliberate learning.",
        "focus": "documented projects, decision logs, cost estimates, Terraform repositories, certifications, community, and release notes",
        "nodes": [
            tail_node("project", "Documented Project", "Architecture case", "data", 90, 220, "A real or fictional architecture with a clear business outcome."),
            tail_node("repo", "Architecture Repository", "Diagram and Terraform", "control", 290, 100, "Versioned implementation and design evidence."),
            tail_node("decisions", "Decision Log", "ADRs and trade-offs", "control", 290, 340, "The reasoning that makes the portfolio credible."),
            tail_node("cost", "Cost Model", "Estimate and assumptions", "control", 500, 220, "A design that acknowledges unit economics."),
            tail_node("writeup", "Published Case Study", "Blog, zine, or walkthrough", "control", 700, 100, "A clear explanation for technical and executive readers."),
            tail_node("certs", "Certification Sequence", "CDL, ACE, PCA, specialty", "control", 700, 340, "A learning plan that reinforces the portfolio."),
            tail_node("community", "Community and Release Notes", "Feedback and current knowledge", "control", 900, 220, "External feedback and awareness of changing services."),
        ],
        "edges": [
            tail_edge("e1", "project", "repo", "implement and version", "control"),
            tail_edge("e2", "project", "decisions", "record choices", "control"),
            tail_edge("e3", "repo", "cost", "measure assumptions", "control"),
            tail_edge("e4", "decisions", "cost", "explain trade-off", "control"),
            tail_edge("e5", "repo", "writeup", "explain architecture", "control"),
            tail_edge("e6", "writeup", "community", "get feedback", "control"),
            tail_edge("e7", "project", "certs", "reinforce gaps", "control"),
        ],
        "failures": [
            ("demo-only", "The portfolio shows commands but no decisions", "decisions", "A reviewer cannot see assumptions, rejected alternatives, or consequences.", "Add ADRs and a design-review narrative to every project."),
            ("unverifiable-cost", "The cost model cannot be checked", "cost", "Pricing, workload size, or unit assumptions are absent.", "Publish assumptions and a verification date, not a false precision."),
            ("stale-advice", "The portfolio ignores platform change", "community", "Service behavior, limits, or exam guidance has changed since publication.", "Track release notes and mark time-sensitive claims for re-verification."),
        ],
    },
    "069": {
        "title": "Progress tracker",
        "summary": "Turn the roadmap into a measurable loop of topic completion, labs, checkpoints, evidence, and next actions.",
        "focus": "phases, topic and lab completion, checkpoints, evidence, and the next highest-value action",
        "nodes": [
            tail_node("phase", "Phase Board", "Phases 0–7 and cross-cutting tracks", "control", 90, 220, "The high-level sequence and current phase."),
            tail_node("topics", "Topic Checklist", "Concepts and services", "control", 290, 100, "What has been studied and what remains."),
            tail_node("labs", "Lab Checklist", "Hands-on exercises", "data", 290, 340, "What has been practiced safely."),
            tail_node("checkpoint", "Checkpoint", "Design review or case output", "control", 500, 220, "A proof point that the phase is understood."),
            tail_node("evidence", "Evidence Log", "Notes, ADRs, diagrams, results", "control", 700, 100, "The artifact supporting completion."),
            tail_node("next", "Next Action", "Smallest useful follow-up", "control", 700, 340, "The next action chosen from evidence, not vague intention."),
            tail_node("snapshot", "Progress Snapshot", "Local browser state", "control", 900, 220, "A local view of progress; it does not create cloud resources."),
        ],
        "edges": [
            tail_edge("e1", "phase", "topics", "select topics", "control"),
            tail_edge("e2", "phase", "labs", "select labs", "control"),
            tail_edge("e3", "topics", "checkpoint", "test understanding", "control"),
            tail_edge("e4", "labs", "checkpoint", "test practice", "data"),
            tail_edge("e5", "checkpoint", "evidence", "record proof", "control"),
            tail_edge("e6", "evidence", "next", "choose gap", "control"),
            tail_edge("e7", "next", "snapshot", "update locally", "control"),
        ],
        "failures": [
            ("checkbox-without-proof", "A topic is marked complete without evidence", "topics", "Completion records activity but not understanding or a design artifact.", "Attach a note, quiz result, diagram, or review output."),
            ("lab-without-checkpoint", "Hands-on work never becomes judgment", "labs", "A lab is run but its trade-off and failure result are not reviewed.", "Convert the lab into a checkpoint with an explicit lesson."),
            ("stale-next-action", "The next action no longer reflects the gap", "next", "Progress continues while the highest-risk learning gap remains open.", "Recalculate the next action from the latest evidence."),
        ],
    },
    "070": {
        "title": "Practical notes and operating rules",
        "summary": "Keep architecture work safe and current with authoritative sources, explicit assumptions, project guardrails, and cleanup rules.",
        "focus": "authoritative documentation, assumptions, project safety, budgets, least privilege, cleanup, and verification dates",
        "nodes": [
            tail_node("question", "Architecture Question", "Decision or operational rule", "control", 90, 220, "The claim or action that needs a defensible answer."),
            tail_node("docs", "Authoritative Documentation", "Product docs and release notes", "control", 290, 100, "The source used to verify time-sensitive behavior."),
            tail_node("assumptions", "Assumptions and Limits", "Scope, quota, cost, behavior", "control", 290, 340, "What is believed, what is unknown, and what may change."),
            tail_node("guardrails", "Project Guardrails", "IAM, APIs, region, budget", "control", 500, 220, "The safe boundary before any cloud action."),
            tail_node("runbook", "Runbook and Cleanup", "Observe, recover, destroy", "data", 700, 100, "The reversible operational path and deletion verification."),
            tail_node("verify", "Verification Date", "Review trigger", "control", 700, 340, "When the claim must be checked again."),
            tail_node("decision", "Approved Decision", "Evidence-backed architecture", "control", 900, 220, "The result that can be handed to a reviewer or operator."),
        ],
        "edges": [
            tail_edge("e1", "question", "docs", "find source", "control"),
            tail_edge("e2", "question", "assumptions", "bound uncertainty", "control"),
            tail_edge("e3", "docs", "guardrails", "apply safely", "control"),
            tail_edge("e4", "assumptions", "guardrails", "test constraints", "control"),
            tail_edge("e5", "guardrails", "runbook", "operate and clean up", "data"),
            tail_edge("e6", "docs", "verify", "schedule review", "control"),
            tail_edge("e7", "runbook", "decision", "approve with recovery", "control"),
            tail_edge("e8", "verify", "decision", "keep current", "control"),
        ],
        "failures": [
            ("stale-fact", "A time-sensitive claim is outdated", "docs", "The design relies on a product limit, price, or behavior without a current source.", "Add an authoritative link and verification date."),
            ("unsafe-action", "A cloud action bypasses guardrails", "guardrails", "The wrong project, identity, region, or budget is used.", "Require explicit project confirmation, least privilege, and plan review."),
            ("orphaned-resource", "Cleanup is assumed rather than verified", "runbook", "Resources or billing remain after the exercise or migration.", "Destroy named resources and verify deletion asynchronously."),
        ],
    },
    "071": {
        "title": "How the phases map to the exam domains",
        "summary": "Trace roadmap phases to the five exam-domain capabilities: design, infrastructure management, security, process optimisation, and reliability.",
        "focus": "Design and Plan, Manage Infrastructure, Security and Compliance, Process Optimization, and Reliability",
        "nodes": [
            tail_node("phase-design", "Phases 3, 6, 7", "Architecture, optimisation, case analysis", "control", 90, 100, "Where design and planning judgment is built."),
            tail_node("phase-infra", "Phases 1, 2, 4", "Foundations, core services, HA", "control", 90, 340, "Where infrastructure management is practiced."),
            tail_node("phase-security", "Phase 5", "Security and compliance", "control", 300, 460, "Where identity, network, data, and governance controls are built."),
            tail_node("domain-design", "Design and Plan", "Exam domain capability", "control", 400, 100, "Plan a cloud architecture from requirements and constraints."),
            tail_node("domain-infra", "Manage Infrastructure", "Exam domain capability", "control", 400, 340, "Operate and evolve cloud infrastructure."),
            tail_node("domain-security", "Security and Compliance", "Exam domain capability", "control", 650, 460, "Protect systems, data, identities, and compliance boundaries."),
            tail_node("domain-process", "Process Optimization", "Exam domain capability", "control", 650, 100, "Improve delivery and operations with measurable feedback."),
            tail_node("domain-reliability", "Reliability", "Exam domain capability", "control", 650, 280, "Design for failure, recovery, and service objectives."),
            tail_node("evidence", "Case / Design Evidence", "Diagrams, ADRs, labs, checkpoints", "data", 900, 220, "Artifacts that demonstrate the capability rather than just naming it."),
        ],
        "edges": [
            tail_edge("e1", "phase-design", "domain-design", "build judgment", "control"),
            tail_edge("e2", "phase-design", "domain-process", "optimise choices", "control"),
            tail_edge("e3", "phase-design", "domain-reliability", "test trade-offs", "control"),
            tail_edge("e4", "phase-infra", "domain-infra", "operate services", "control"),
            tail_edge("e5", "phase-infra", "domain-reliability", "practice HA", "control"),
            tail_edge("e6", "phase-security", "domain-security", "apply controls", "control"),
            tail_edge("e7", "domain-design", "evidence", "produce artifacts", "data"),
            tail_edge("e8", "domain-security", "evidence", "show controls", "data"),
            tail_edge("e9", "domain-reliability", "evidence", "show recovery", "data"),
        ],
        "failures": [
            ("domain-blind-spot", "A domain has no learning evidence", "evidence", "The learner can recite a domain but has no diagram, ADR, lab, or case output.", "Attach a concrete artifact to each domain capability."),
            ("phase-mismatch", "A phase is mapped to the wrong capability", "domain-design", "Study time is spent without closing the intended exam or consulting gap.", "Review the phase-to-domain mapping before selecting the next topic."),
            ("reliability-omission", "Reliability is treated as a single phase", "domain-reliability", "Recovery, failure domains, and operations are omitted from otherwise complete designs.", "Thread reliability checks through infrastructure, security, cost, and case work."),
        ],
    },
}


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


TAIL_LENSES = {
    "d1": ("Architecture map", "Trace the primary decision path"),
    "d2": ("Working sequence", "Follow the handoff sequence"),
    "d3": ("Failure analysis", "Inspect the evidence at the failure boundary"),
    "d4": ("Security and ownership", "Check the trust, ownership, and evidence boundary"),
    "d5": ("Scale and cost", "Stress the capacity, time, and cost boundary"),
    "d6": ("Implementation seams", "Inspect the documented implementation seam"),
}


def tail_edge_ids(profile: dict, kind: str) -> list[str]:
    edges = profile["edges"]
    count = len(edges)
    if count >= 6:
        indexes = {
            "d1": [0, 1, 2], "d2": [1, 2, 3], "d3": [2, 3, 4],
            "d4": [0, 3, 4], "d5": [1, 4, 5], "d6": [count - 3, count - 2, count - 1],
        }[kind]
    else:
        indexes = {
            "d1": [0, 1, 2], "d2": [1, 2, 3], "d3": [2, 3, 4],
            "d4": [0, 2, 4], "d5": [1, 3, 4], "d6": [2, 3, 4],
        }[kind]
    return [edges[min(index, count - 1)]["id"] for index in indexes]


def tail_spec(meta: dict, kind: str) -> dict:
    profile = TAIL_PROFILES[meta["topic_no"]]
    node_by_id = {node["id"]: node for node in profile["nodes"]}
    edge_by_id = {edge["id"]: edge for edge in profile["edges"]}
    lens_title, lens_action = TAIL_LENSES[kind]
    steps = []
    for number, edge_id in enumerate(tail_edge_ids(profile, kind), 1):
        edge = edge_by_id[edge_id]
        source = node_by_id[edge["from"]]["label"]
        target = node_by_id[edge["to"]]["label"]
        steps.append({
            "n": number,
            "title": f"{lens_title}: {source} → {target}",
            "edges": [edge_id],
            "action": f"{source} {edge['label']} to {target}; record evidence for {profile['focus']}.",
            "why_traversal": f"{lens_action} for {profile['title']} by making {target} an explicit review boundary.",
            "protocol": "Review / evidence handoff",
            "plane": edge["plane"].title() + " Plane",
            "check": {
                "metrics": f"{meta['roadmap_id']}:{kind}:step_{number}:evidence_present",
                "logs": f"topic={meta['roadmap_id']} lens={kind} edge={edge_id}",
                "commands": f"record and verify {edge_id} for {meta['title']}",
            },
        })
    scenarios = []
    for scenario_id, label, node_id, cause, recovery in profile["failures"]:
        incident_edges = [edge["id"] for edge in profile["edges"] if node_id in {edge["from"], edge["to"]}]
        scenarios.append({
            "id": scenario_id,
            "label": label,
            "changes": {"failedNodes": [node_id], "failedEdges": incident_edges[:1]},
            "root_cause": cause,
            "diverted_path": f"The {profile['title']} path stops at the affected boundary and the evidence trail becomes incomplete.",
            "blast_radius": f"Consumers of {node_by_id[node_id]['label']} and any downstream decision depending on it.",
            "recovery": recovery,
            "check": {
                "metric": f"{meta['roadmap_id']}:{kind}:{scenario_id}:resolved",
                "command": f"review {kind} evidence for {node_by_id[node_id]['label']}",
            },
        })
    return normalize_spec({
        "id": f"topic-{meta['topic_no']}-{kind}",
        "title": f"{meta['title']} — {kind.upper()}",
        "topic_no": meta["topic_no"],
        "roadmap_id": meta["roadmap_id"],
        "kind": {"d1": "map", "d2": "flow", "d3": "failure", "d4": "security", "d5": "scale-cost", "d6": "internals"}[kind],
        "purpose": f"{TAIL_LENSES[kind][0]} for {meta['title']}: {profile['focus']}.",
        "routing_rationale": f"Use the {kind.upper()} lens to keep {profile['focus']} connected to an explicit owner, evidence path, and recovery action.",
        "summary": profile["summary"],
        "groups": [],
        "nodes": json.loads(json.dumps(profile["nodes"])),
        "edges": json.loads(json.dumps(profile["edges"])),
        "steps": steps,
        "scenarios": scenarios,
    }, meta, kind)


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


def topic_items(meta: dict) -> list[str]:
    items = list(ROADMAP_ITEMS.get(meta["roadmap_id"], []))
    if items:
        return items
    title = meta["title"]
    return [
        f"Define the business outcome and boundary for {title}.",
        f"Name the GCP capabilities and dependencies used by {title}.",
        f"Record the trade-off, evidence, owner, and rollback for {title}.",
        f"Test the failure and recovery story for {title}.",
    ]


def item_text(items: list[str], index: int, limit: int = 180) -> str:
    value = items[index % len(items)]
    if len(value) > limit:
        value = value[: limit - 1].rstrip() + "…"
    return esc(value)


def part1_addendum(meta: dict) -> str:
    title = esc(meta["title"])
    roadmap_id = esc(meta["roadmap_id"])
    items = topic_items(meta)
    examples = "".join(
        f"<li>Brightloaf scenario: make <strong>{item_text(items, i)}</strong> observable and reviewable before launch.</li>"
        for i in range(min(3, len(items)))
    )
    roles = "".join(
        f"<tr><td>{role}</td><td>{need} <strong>{item_text(items, i)}</strong>.</td></tr>"
        for i, (role, need) in enumerate([
            ("Business owner", "Protect the outcome represented by"),
            ("Platform owner", "Set the scope and operating boundary for"),
            ("Security lead", "Require evidence around"),
            ("Finance owner", "Attribute the cost of"),
            ("Operations engineer", "Detect and recover when"),
        ])
    )
    misconceptions = "".join(
        f"<li><strong>{item_text(items, i)}</strong> is a requirement to verify, not proof that the design is safe by itself.</li>"
        for i in range(min(4, len(items)))
    )
    vocabulary = "".join(
        f"<li><code>{term}</code>: the topic-specific anchor is <strong>{item_text(items, i)}</strong>.</li>"
        for i, term in enumerate(("scope anchor", "operating signal", "trade-off evidence", "failure horizon", "exit condition"))
    )
    return f"""<div class="compliance-addendum part1-complete">
<p class="inline-references"><strong>Foundation references:</strong> {inline_reference_markup(meta)}</p>
<h3>The Pain</h3><p>{title} becomes risky when teams treat <strong>{item_text(items, 0)}</strong> as a checkbox instead of a boundary with an owner, evidence, and recovery path.</p>
<h3>The Idea in One Paragraph</h3><p>{title} is a design decision anchored by <strong>{item_text(items, 0)}</strong>. Connect it to <strong>{item_text(items, 1)}</strong>, make the dependency visible, and state what changes when the requirement or failure domain changes.</p>
<h3>Real-World Examples</h3><ul>{examples}</ul>
<h3>Who Cares and Why</h3><table><tr><th>Role</th><th>Specific concern</th></tr>{roles}</table>
<h3>Common Misconceptions</h3><ul>{misconceptions}</ul>
<h3>Vocabulary Starter</h3><ul>{vocabulary}</ul>
<h3>Where It Fits</h3><p>Roadmap {roadmap_id} · {title}. Start with <strong>{item_text(items, 0)}</strong>, then connect it to <strong>{item_text(items, len(items) - 1)}</strong> and the next topic's decision boundary.</p></div>"""


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
    <a href="#references"><span>7</span> References</a>
  </div>
</nav>'''


REFERENCE_PROFILES = (
    ("network", [
        ("VPC network overview", "https://cloud.google.com/vpc/docs/overview", "Resource scope, subnets, routes, and network boundaries."),
        ("Google Cloud network connectivity overview", "https://cloud.google.com/network-connectivity/docs/overview", "Connectivity choices and their operating boundaries."),
    ]),
    ("linux", [
        ("Compute Engine guest environments", "https://cloud.google.com/compute/docs/images", "How operating-system images and guest environments fit the platform."),
        ("Compute Engine troubleshooting", "https://cloud.google.com/compute/docs/troubleshooting", "A practical starting point for diagnosing VM behavior."),
    ]),
    ("container", [
        ("Google Cloud container overview", "https://cloud.google.com/learn/what-is-a-container", "Container primitives before orchestration details."),
        ("GKE overview", "https://cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview", "The managed Kubernetes control-plane and node model."),
    ]),
    ("cloud concept", [
        ("Google Cloud overview", "https://cloud.google.com/docs/overview", "Core resource, product, and platform vocabulary."),
        ("Google Cloud Architecture Framework", "https://cloud.google.com/architecture/framework", "A common lens for reliability, security, cost, and operations."),
    ]),
    ("architecture", [
        ("Google Cloud Architecture Center", "https://cloud.google.com/architecture", "Reference architectures and design patterns."),
        ("Google Cloud Architecture Framework", "https://cloud.google.com/architecture/framework", "Principles for evaluating architecture decisions."),
    ]),
    ("cloud digital", [
        ("Cloud Digital Leader certification guide", "https://cloud.google.com/learn/certification/cloud-digital-leader", "Business and technology foundations for cloud decisions."),
        ("Google Cloud overview", "https://cloud.google.com/docs/overview", "The platform vocabulary used by the topic."),
    ]),
    ("account", [
        ("Google Cloud resource hierarchy", "https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy", "Organizations, folders, projects, and resource scope."),
        ("Google Cloud SDK documentation", "https://cloud.google.com/sdk/docs", "The gcloud toolchain and command-line model."),
    ]),
    ("resource hierarchy", [
        ("Google Cloud resource hierarchy", "https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy", "Inheritance and administrative boundaries."),
        ("Organization Policy overview", "https://cloud.google.com/resource-manager/docs/organization-policy/overview", "Central guardrails and policy constraints."),
    ]),
    ("identity", [
        ("IAM overview", "https://cloud.google.com/iam/docs/overview", "Principals, permissions, roles, and policy evaluation."),
        ("IAM policy concepts", "https://cloud.google.com/iam/docs/overview#policy", "How access decisions are represented and inherited."),
    ]),
    ("billing", [
        ("Cloud Billing documentation", "https://cloud.google.com/billing/docs", "Accounts, budgets, exports, and cost controls."),
        ("Cost optimization pillar", "https://cloud.google.com/architecture/framework/cost-optimization", "Cost as an architectural constraint."),
    ]),
    ("compute", [
        ("Compute Engine documentation", "https://cloud.google.com/compute/docs", "VMs, disks, images, and instance lifecycle."),
        ("Managed instance groups overview", "https://cloud.google.com/compute/docs/instance-groups", "Scaling, autohealing, and regional placement."),
    ]),
    ("kubernetes", [
        ("GKE documentation", "https://cloud.google.com/kubernetes-engine/docs", "Clusters, workloads, networking, and operations."),
        ("GKE architecture", "https://cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview", "Control plane, nodes, and managed boundaries."),
    ]),
    ("serverless", [
        ("Cloud Run documentation", "https://cloud.google.com/run/docs", "Request-driven containers and operational boundaries."),
        ("Google Cloud serverless overview", "https://cloud.google.com/serverless", "How managed serverless products differ."),
    ]),
    ("load balancing", [
        ("Choosing a load balancer", "https://cloud.google.com/load-balancing/docs/choosing-load-balancer", "The product-selection decision tree."),
        ("Cloud Load Balancing overview", "https://cloud.google.com/load-balancing/docs", "Frontend, backend, health-check, and policy concepts."),
    ]),
    ("storage", [
        ("Cloud Storage documentation", "https://cloud.google.com/storage/docs", "Objects, buckets, locations, and lifecycle."),
        ("Cloud Storage storage classes", "https://cloud.google.com/storage/docs/storage-classes", "Access patterns, retention, and cost trade-offs."),
    ]),
    ("database", [
        ("Google Cloud databases overview", "https://cloud.google.com/products/databases", "How the main managed database families differ."),
        ("Database migration and modernization", "https://cloud.google.com/architecture/database-migration", "Selection and migration context for data systems."),
    ]),
    ("messaging", [
        ("Pub/Sub documentation", "https://cloud.google.com/pubsub/docs", "Topics, subscriptions, delivery, and replay."),
        ("Cloud Tasks documentation", "https://cloud.google.com/tasks/docs", "Rate-controlled task delivery and retries."),
    ]),
    ("requirements", [
        ("Operational excellence pillar", "https://cloud.google.com/architecture/framework/operational-excellence", "Turning business outcomes into operating requirements."),
        ("Reliability pillar", "https://cloud.google.com/architecture/framework/reliability", "Availability, recovery, and failure-domain thinking."),
    ]),
    ("migration", [
        ("Migration Center", "https://cloud.google.com/migration-center", "Discovery, assessment, and migration planning."),
        ("Migration and modernization overview", "https://cloud.google.com/architecture/migration-to-google-cloud", "Migration patterns and decision boundaries."),
    ]),
    ("decision", [
        ("Google Cloud Architecture Center", "https://cloud.google.com/architecture", "Reference patterns for comparing alternatives."),
        ("Architecture Framework decision principles", "https://cloud.google.com/architecture/framework", "A review lens for durable decisions."),
    ]),
    ("diagram", [
        ("C4 model", "https://c4model.com/", "A practical hierarchy for communicating software architecture."),
        ("Google Cloud Architecture Center", "https://cloud.google.com/architecture", "Cloud reference diagrams and patterns."),
    ]),
    ("reliability", [
        ("Reliability pillar", "https://cloud.google.com/architecture/framework/reliability", "Reliability principles and failure-domain design."),
        ("Google SRE resources", "https://sre.google/resources/", "SLOs, error budgets, and operational practice."),
    ]),
    ("sre", [
        ("Google SRE book", "https://sre.google/sre-book/table-of-contents/", "The foundational SRE operating model."),
        ("Google SRE workbook", "https://sre.google/workbook/table-of-contents/", "Applying SLOs and error budgets in practice."),
    ]),
    ("disaster recovery", [
        ("Disaster recovery planning guide", "https://cloud.google.com/architecture/dr-scenarios", "Recovery patterns, RTO, RPO, and trade-offs."),
        ("Backup and DR documentation", "https://cloud.google.com/backup-disaster-recovery", "Managed backup and recovery capabilities."),
    ]),
    ("observability", [
        ("Cloud Monitoring documentation", "https://cloud.google.com/monitoring/docs", "Metrics, dashboards, alerting, and SLOs."),
        ("Cloud Logging documentation", "https://cloud.google.com/logging/docs", "Logs, routing, retention, and analysis."),
    ]),
    ("testing", [
        ("Reliability pillar", "https://cloud.google.com/architecture/framework/reliability", "Testing and designing for failure."),
        ("Google SRE workbook", "https://sre.google/workbook/table-of-contents/", "Operational validation and production readiness."),
    ]),
    ("security", [
        ("Google Cloud security overview", "https://cloud.google.com/security", "Security responsibilities and platform controls."),
        ("Security pillar", "https://cloud.google.com/architecture/framework/security", "Identity, data, network, and operational security."),
    ]),
    ("compliance", [
        ("Compliance resource center", "https://cloud.google.com/security/compliance", "Compliance programs and shared responsibility."),
        ("Assured Workloads documentation", "https://cloud.google.com/assured-workloads/docs", "Regulated workload controls and boundaries."),
    ]),
    ("security operations", [
        ("Security Command Center overview", "https://cloud.google.com/security-command-center/docs/concepts-security-command-center-overview", "Finding, prioritizing, and responding to security risk."),
        ("Cloud Logging documentation", "https://cloud.google.com/logging/docs", "Evidence and audit trails for operations."),
    ]),
    ("supply-chain", [
        ("Software supply chain security", "https://cloud.google.com/software-supply-chain-security", "Build, attest, and deploy trusted artifacts."),
        ("Binary Authorization documentation", "https://cloud.google.com/binary-authorization/docs", "Deployment-time admission and attestation."),
    ]),
    ("cost", [
        ("Cost optimization pillar", "https://cloud.google.com/architecture/framework/cost-optimization", "FinOps and cost-aware architecture."),
        ("Google Cloud cost management", "https://cloud.google.com/cost-management", "Budgets, reporting, and optimization tools."),
    ]),
    ("performance", [
        ("Performance optimization pillar", "https://cloud.google.com/architecture/framework/performance-optimization", "Latency, throughput, and capacity reasoning."),
        ("Google Cloud Architecture Center", "https://cloud.google.com/architecture", "Performance-oriented reference patterns."),
    ]),
    ("terraform", [
        ("Terraform on Google Cloud", "https://cloud.google.com/docs/terraform", "Infrastructure as code workflow and provider guidance."),
        ("Google provider documentation", "https://registry.terraform.io/providers/hashicorp/google/latest/docs", "Resource arguments and provider behavior."),
    ]),
    ("ci/cd", [
        ("Cloud Build documentation", "https://cloud.google.com/build/docs", "Build automation and delivery foundations."),
        ("Cloud Deploy documentation", "https://cloud.google.com/deploy/docs", "Progressive delivery and promotion."),
    ]),
    ("operations", [
        ("Operational excellence pillar", "https://cloud.google.com/architecture/framework/operational-excellence", "Operating, improving, and governing platforms."),
        ("Cloud Operations suite", "https://cloud.google.com/products/operations", "Monitoring, logging, tracing, and profiling."),
    ]),
    ("case", [
        ("Professional Cloud Architect certification guide", "https://cloud.google.com/certification/guides/cloud-architect", "Official exam scope and case-study expectations."),
        ("Google Cloud Architecture Center", "https://cloud.google.com/architecture", "Reference architectures for comparison."),
    ]),
    ("bigquery", [
        ("BigQuery documentation", "https://cloud.google.com/bigquery/docs", "Warehouse concepts, SQL, storage, and execution."),
        ("BigQuery partitioned tables", "https://cloud.google.com/bigquery/docs/partitioned-tables", "Scan reduction and cost-aware table design."),
    ]),
    ("dataflow", [
        ("Dataflow documentation", "https://cloud.google.com/dataflow/docs", "Managed Beam execution and pipeline operations."),
        ("Dataproc documentation", "https://cloud.google.com/dataproc/docs", "Managed Spark and Hadoop processing."),
    ]),
    ("data lake", [
        ("BigLake documentation", "https://cloud.google.com/biglake/docs", "Open-format data access and governance."),
        ("Dataplex Universal Catalog", "https://cloud.google.com/dataplex/docs", "Data discovery, quality, and governance."),
    ]),
    ("machine learning", [
        ("Vertex AI documentation", "https://cloud.google.com/vertex-ai/docs", "Managed ML development and serving."),
        ("Vertex AI architecture", "https://cloud.google.com/architecture/ai-ml", "Reference patterns for ML systems."),
    ]),
    ("cheat sheet", [
        ("Google Cloud product documentation", "https://cloud.google.com/docs", "A product-neutral starting point before choosing a service."),
        ("Google Cloud Architecture Framework", "https://cloud.google.com/architecture/framework", "Trade-offs across reliability, security, cost, and operations."),
    ]),
    ("skills boost", [
        ("Cloud Skills Boost learning paths", "https://www.cloudskillsboost.google/paths", "Structured hands-on learning paths and labs."),
        ("Google Cloud training and certification", "https://cloud.google.com/learn/training", "Official training and credential pathways."),
    ]),
    ("consultant", [
        ("Google Cloud Architecture Framework", "https://cloud.google.com/architecture/framework", "A common language for client-facing architecture reviews."),
        ("Google Cloud Architecture Center", "https://cloud.google.com/architecture", "Reference material for options and proposals."),
    ]),
    ("portfolio", [
        ("Professional Cloud Architect certification guide", "https://cloud.google.com/certification/guides/cloud-architect", "A capability model for communicating architecture experience."),
        ("Google Cloud Architecture Center", "https://cloud.google.com/architecture", "Examples to anchor portfolio artifacts."),
    ]),
    ("progress", [
        ("Google Cloud certification overview", "https://cloud.google.com/learn/certification", "Credential scope and preparation resources."),
        ("Cloud Skills Boost learning paths", "https://www.cloudskillsboost.google/paths", "Hands-on evidence and progression checkpoints."),
    ]),
    ("notes", [
        ("Google Cloud documentation", "https://cloud.google.com/docs", "Authoritative product and platform reference."),
        ("Google Cloud Architecture Framework", "https://cloud.google.com/architecture/framework", "Operating rules that generalize across services."),
    ]),
    ("domain", [
        ("Professional Cloud Architect certification guide", "https://cloud.google.com/certification/guides/cloud-architect", "Official exam domains and case-study context."),
        ("Google Cloud Architecture Framework", "https://cloud.google.com/architecture/framework", "Architecture principles behind the domains."),
    ]),
)


def topic_references(meta: dict) -> list[tuple[str, str, str]]:
    title = meta["title"].casefold()
    for keyword, links in REFERENCE_PROFILES:
        if keyword in title:
            return list(links)
    return [
        ("Google Cloud documentation", "https://cloud.google.com/docs", "Start with the official vocabulary and product boundary."),
        ("Google Cloud Architecture Framework", "https://cloud.google.com/architecture/framework", "Use the framework to test reliability, security, cost, and operations."),
    ]


def references_section(meta: dict) -> str:
    links = "".join(
        f'<li><a href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a><span> — {esc(reason)}</span></li>'
        for label, url, reason in topic_references(meta)
    )
    return f'''<section class="topic-section references-section" id="references"><h2 class="section-title"><span class="section-number">7</span> References</h2><p>Use these sources to establish the foundation for <strong>{esc(meta["title"])}</strong>, verify product behavior, and then return to the architecture discussion.</p><ul class="reference-list">{links}</ul></section>'''


def inline_reference_markup(meta: dict, count: int = 2) -> str:
    """Render concise links beside the concept prose that uses them."""
    return " · ".join(
        f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>'
        for label, url, _reason in topic_references(meta)[:count]
    )


CLAIM_REFERENCE_RULES = (
    ("subnet", "Subnet IP allocation rules", "https://cloud.google.com/vpc/docs/subnets"),
    ("cidr", "Subnet IP allocation rules", "https://cloud.google.com/vpc/docs/subnets"),
    ("firewall", "VPC firewall rules", "https://cloud.google.com/firewall/docs/firewalls"),
    ("dns", "Cloud DNS overview", "https://cloud.google.com/dns/docs/overview"),
    ("ttl", "Cloud DNS overview", "https://cloud.google.com/dns/docs/overview"),
    ("nat", "Cloud NAT overview", "https://cloud.google.com/nat/docs/overview"),
    ("load balanc", "Choosing a load balancer", "https://cloud.google.com/load-balancing/docs/choosing-load-balancer"),
    ("iam", "IAM overview", "https://cloud.google.com/iam/docs/overview"),
    ("service account", "IAM service accounts", "https://cloud.google.com/iam/docs/service-accounts"),
    ("kubernetes", "GKE overview", "https://cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview"),
    ("pub/sub", "Pub/Sub documentation", "https://cloud.google.com/pubsub/docs"),
    ("cloud tasks", "Cloud Tasks documentation", "https://cloud.google.com/tasks/docs"),
    ("terraform", "Terraform on Google Cloud", "https://cloud.google.com/docs/terraform"),
    ("bigquery", "BigQuery documentation", "https://cloud.google.com/bigquery/docs"),
    ("dataflow", "Dataflow documentation", "https://cloud.google.com/dataflow/docs"),
    ("vertex ai", "Vertex AI documentation", "https://cloud.google.com/vertex-ai/docs"),
    ("cloud kms", "Cloud KMS documentation", "https://cloud.google.com/kms/docs"),
    ("vpc service controls", "VPC Service Controls overview", "https://cloud.google.com/vpc-service-controls/docs/overview"),
)


def claim_sources(meta: dict, claim_text: str) -> list[tuple[str, str]]:
    lowered = re.sub(r"<[^>]+>", " ", claim_text).casefold()
    selected: list[tuple[str, str]] = []
    for keyword, label, url in CLAIM_REFERENCE_RULES:
        if keyword in lowered and (label, url) not in selected:
            selected.append((label, url))
    for label, url, _reason in topic_references(meta):
        if (label, url) not in selected:
            selected.append((label, url))
        if len(selected) >= 2:
            break
    return selected[:2]


def claim_citation(meta: dict, claim_text: str = "") -> str:
    """Render compact numbered proof links for a nearby claim."""
    sources = claim_sources(meta, claim_text)
    return " ".join(
        f'<a href="{esc(url)}" target="_blank" rel="noopener" aria-label="Source: {esc(label)}">[{index}]</a>'
        for index, (label, url) in enumerate(sources, 1)
    )


def annotate_claims(text: str, meta: dict) -> str:
    """Attach source markers to explanatory paragraphs and misconception items."""
    for section_id in ("real-world", "technical"):
        pattern = re.compile(rf'(<section[^>]*\bid="{section_id}"[^>]*>)(.*?)(</section>)', re.S | re.I)

        def annotate_section(match: re.Match[str]) -> str:
            body = match.group(2)

            def annotate_paragraph(paragraph: re.Match[str]) -> str:
                attrs, content = paragraph.group(1), paragraph.group(2)
                if "inline-references" in attrs or "table-citation" in attrs or "claim-citation" in content:
                    return paragraph.group(0)
                return f'<p{attrs}>{content} <sup class="claim-citation">{claim_citation(meta, content)}</sup></p>'

            body = re.sub(r'<p\b([^>]*)>(.*?)</p>', annotate_paragraph, body, flags=re.S | re.I)

            def annotate_item(item: re.Match[str]) -> str:
                content = item.group(1)
                if "claim-citation" in content:
                    return item.group(0)
                return f'<li>{content} <sup class="claim-citation">{claim_citation(meta, content)}</sup></li>'

            body = re.sub(r'<li\b[^>]*>(.*?)</li>', annotate_item, body, flags=re.S | re.I)
            body = re.sub(
                r'(<table\b[^>]*>.*?</table>)(?!\s*<p class="table-citation")',
                lambda table: table.group(1) + f'<p class="table-citation claim-citation"><strong>Sources:</strong> {claim_citation(meta, table.group(1))}</p>',
                body,
                flags=re.S | re.I,
            )
            body = re.sub(
                r'(<pre\b[^>]*>.*?</pre>)(?!\s*<p class="table-citation")',
                lambda code: code.group(1) + (f'<p class="table-citation claim-citation"><strong>Sources:</strong> {claim_citation(meta, code.group(1))}</p>' if re.search(r'formula|example|usable|reserved|cidr|rto|rpo', code.group(1), re.I) else ""),
                body,
                flags=re.S | re.I,
            )
            return match.group(1) + body + match.group(3)

        text = pattern.sub(annotate_section, text, count=1)
    return text


def part2_addendum(meta: dict) -> str:
    title = esc(meta["title"])
    items = topic_items(meta)
    tradeoffs = "".join(
        f"<tr><td>{choice}</td><td>{burden}</td><td>{item_text(items, i)}</td><td>{when}</td></tr>"
        for i, (choice, burden, when) in enumerate([
            ("Managed path", "Less undifferentiated toil", "when the team can accept the platform boundary"),
            ("Explicit path", "More configuration and ownership", "when control over the requirement is material"),
            ("Alternative or defer", "Lower commitment while evidence is missing", "when the requirement needs validation"),
        ])
    )
    failures = "".join(
        f"<tr><td>Gap in {item_text(items, i, 120)}</td><td>The requirement is absent from the design evidence.</td><td>Consumers of {title} that depend on this decision.</td><td>Inspect the relevant path and record the observed result.</td><td>Turn the item into a review gate and a repeatable test.</td></tr>"
        for i in range(5)
    )
    questions = "".join(
        f"<li>What business requirement makes <strong>{item_text(items, i)}</strong> necessary?</li>"
        for i in range(8)
    )
    good = "".join(
        f"<li>The design names evidence for <strong>{item_text(items, i)}</strong> and an owner for the next action.</li>"
        for i in range(5)
    )
    return f"""<div class="compliance-addendum depth-complete">
<p class="inline-references"><strong>Technical references:</strong> {inline_reference_markup(meta)}</p>
<h4>Scope and planes</h4><p>The scope of {title} is set by <strong>{item_text(items, 0)}</strong>. Separate the control-plane decision from the runtime path, and state which organization, project, region, zone, or resource owns the boundary.</p>
<h4>Practitioner defaults and troubleshooting</h4><p>Start by verifying <strong>{item_text(items, 1)}</strong>, then inspect the identity, quota, network, logging, and dependency evidence that can invalidate that assumption.</p>
<h4>Architect trade-off table</h4><table><tr><th>Choice</th><th>Operational burden</th><th>Topic-specific consequence</th><th>Choose when</th></tr>{tradeoffs}</table><p>Make the choice reversible where possible: record why <strong>{item_text(items, 0)}</strong> wins, what evidence would change the decision, and how the team will detect drift.</p>
<h4>Failure-mode table</h4><table class="failure-mode-table"><tr><th>Failure</th><th>Signal</th><th>Blast radius</th><th>Immediate action</th><th>Durable prevention</th></tr>{failures}</table>
<h4>Hidden dependencies and day-2 operations</h4><p>For {title}, review the dependencies implied by <strong>{item_text(items, 2)}</strong> and <strong>{item_text(items, len(items) - 1)}</strong>; assign ownership, an escalation path, a cost signal, and a migration or deprecation plan.</p>
<h4>Design-review questions</h4><ol class="review-questions">{questions}</ol>
<h4>What good looks like</h4><ul class="mature-deployment">{good}</ul>
<div class="progression-links"><strong>Before this:</strong> establish the prerequisite for <strong>{item_text(items, 0)}</strong>. <strong>After this:</strong> connect the decision to <strong>{item_text(items, len(items) - 1)}</strong>. <strong>Levels up:</strong> test the same design under a regional failure, 10× load, a cost constraint, or a new compliance requirement.</div></div>"""


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


def replace_addendum(text: str, class_name: str, replacement: str) -> str:
    """Replace all copies of an addendum while retaining exactly one copy."""
    pattern = re.compile(rf'<div class="compliance-addendum {re.escape(class_name)}">.*?</div>', re.S)
    first = True

    def replace(match: re.Match[str]) -> str:
        nonlocal first
        if first:
            first = False
            return replacement
        return ""

    return pattern.sub(replace, text)


def replace_inline_specs(text: str, specs: dict[str, dict]) -> str:
    for kind, spec in specs.items():
        payload = json.dumps(spec, indent=2)
        pattern = re.compile(rf'<script id="spec-{kind}-data"[^>]*>\s*.*?\s*</script>', re.S)
        replacement = f'<script id="spec-{kind}-data" type="application/json">\n{payload}\n</script>'
        text = pattern.sub(lambda _match: replacement, text, count=1)
    return text


def div_block_bounds(text: str, start: int) -> tuple[int, int] | None:
    """Return the bounds of the div beginning at *start*, including its close tag."""
    token = re.compile(r"<div\b[^>]*>|</div\s*>", re.I)
    depth = 0
    for match in token.finditer(text, start):
        if match.group(0).lower().startswith("</"):
            depth -= 1
            if depth == 0:
                return start, match.end()
        else:
            depth += 1
    return None


def analogy_div_start(text: str, *, element_id: str | None = None, class_name: str | None = None) -> re.Match[str] | None:
    """Find an analogy div opening tag regardless of attribute order."""
    if element_id:
        return re.search(rf'<div\b[^>]*\bid=["\']{re.escape(element_id)}["\'][^>]*>', text, re.I)
    if class_name:
        return re.search(rf'<div\b(?=[^>]*\bclass=["\'][^"\']*\b{re.escape(class_name)}\b)[^>]*>', text, re.I)
    return None


def normalize_analogy_layout(text: str) -> str:
    """Keep the beat panel, SVG host, and mapping table as separate siblings.

    Older pages accidentally placed the scene and mapping inside the beat panel.
    The beat renderer replaces the panel contents, which removes those elements.
    This small balanced-div pass repairs that legacy shape without needing a DOM
    parser in the static-site generator.
    """
    display_match = analogy_div_start(text, element_id="analogy-display")
    if not display_match:
        return text
    display_bounds = div_block_bounds(text, display_match.start())
    if not display_bounds:
        return text
    _, display_end = display_bounds
    closing_start = text.rfind("</div", display_match.end(), display_end)
    if closing_start < display_match.end():
        return text
    inner = text[display_match.end():closing_start]
    nested_blocks: list[tuple[int, int]] = []
    for match in (
        analogy_div_start(inner, element_id="analogy-scene"),
        analogy_div_start(inner, class_name="analogy-mapping"),
    ):
        if not match:
            continue
        bounds = div_block_bounds(inner, match.start())
        if bounds:
            nested_blocks.append(bounds)
    if not nested_blocks:
        return text
    for block_start, block_end in sorted(nested_blocks, reverse=True):
        inner = inner[:block_start] + inner[block_end:]
    extracted = "".join(text[display_match.end() + start:display_match.end() + end] for start, end in sorted(nested_blocks))
    replacement = text[display_match.start():display_match.end()] + inner + text[closing_start:display_end] + extracted
    return text[:display_match.start()] + replacement + text[display_end:]


def insert_after_analogy_div(text: str, addition: str, *, element_id: str | None = None, class_name: str | None = None) -> str:
    match = analogy_div_start(text, element_id=element_id, class_name=class_name)
    if not match:
        return text
    bounds = div_block_bounds(text, match.start())
    if not bounds:
        return text
    return text[:bounds[1]] + addition + text[bounds[1]:]


def topic_catalog() -> list[dict]:
    return sorted(
        (page_meta(path) for path in PAGES.glob("topic-*.html")),
        key=lambda item: int(item["topic_no"]),
    )


def navigation_markup(meta: dict, catalog: list[dict]) -> tuple[str, str, str, str]:
    """Build every topic-navigation surface from the current page catalog."""
    index = next(i for i, item in enumerate(catalog) if item["topic_no"] == meta["topic_no"])
    total = len(catalog)
    previous = catalog[index - 1] if index else None
    following = catalog[index + 1] if index + 1 < total else None
    last_no = catalog[-1]["topic_no"]

    phases: list[str] = []
    for item in catalog:
        if item["phase"] not in phases:
            phases.append(item["phase"])
    options: list[str] = []
    for phase in phases:
        options.append(f'<optgroup label="{esc(phase)}">')
        for item in catalog:
            if item["phase"] != phase:
                continue
            selected = " selected" if item["topic_no"] == meta["topic_no"] else ""
            short_title = item["title"] if len(item["title"]) <= 38 else item["title"][:35] + "…"
            options.append(
                f'<option value="topic-{esc(item["topic_no"])}.html"{selected}>'
                f'{esc(item["topic_no"])} [{esc(item["roadmap_id"])}] {esc(short_title)}</option>'
            )
        options.append("</optgroup>")

    if previous:
        prev_url = f'topic-{previous["topic_no"]}.html'
        prev_arrow = f'<a href="{prev_url}" class="nav-topic-arrow prev" title="Previous Topic: {esc(previous["title"])} [Key: P]">‹</a>'
        prev_subnav = f'<a href="{prev_url}" class="subnav-nav-btn prev" title="{esc(previous["title"])}">← Prev ({esc(previous["topic_no"])})</a>'
        prev_dock = f'<a href="{prev_url}" class="dock-btn prev" title="Previous Topic: {esc(previous["title"])} [Key: P]">← {esc(previous["topic_no"])}</a>'
        prev_card = f'<a href="{prev_url}" class="pagination-card prev"><div class="pagination-direction">← PREVIOUS TOPIC</div><div class="pagination-topic-meta">{esc(previous["phase"])} · [{esc(previous["roadmap_id"])}]</div><div class="pagination-title">{esc(previous["topic_no"])}: {esc(previous["title"])}</div><div class="pagination-shortcut">Shortcut: <kbd>P</kbd> or <kbd>←</kbd></div></a>'
    else:
        prev_url = ""
        prev_arrow = '<a href="../index.html" class="nav-topic-arrow prev disabled" title="Start of Roadmap">‹</a>'
        prev_subnav = '<span class="subnav-nav-btn prev disabled">← Prev</span>'
        prev_dock = '<span class="dock-btn prev disabled">← Start</span>'
        prev_card = '<a href="../index.html" class="pagination-card prev"><div class="pagination-direction">← ROADMAP START</div><div class="pagination-topic-meta">Curriculum Overview</div><div class="pagination-title">Start at Topic 001</div><div class="pagination-shortcut">Shortcut: <kbd>P</kbd> or <kbd>I</kbd></div></a>'

    if following:
        next_url = f'topic-{following["topic_no"]}.html'
        next_arrow = f'<a href="{next_url}" class="nav-topic-arrow next" title="Next Topic: {esc(following["title"])} [Key: N]">›</a>'
        next_subnav = f'<a href="{next_url}" class="subnav-nav-btn next" title="{esc(following["title"])}">Next ({esc(following["topic_no"])}) →</a>'
        next_dock = f'<a href="{next_url}" class="dock-btn next" title="Next Topic: {esc(following["title"])} [Key: N]">{esc(following["topic_no"])} →</a>'
        next_card = f'<a href="{next_url}" class="pagination-card next"><div class="pagination-direction">NEXT TOPIC →</div><div class="pagination-topic-meta">{esc(following["phase"])} · [{esc(following["roadmap_id"])}]</div><div class="pagination-title">{esc(following["topic_no"])}: {esc(following["title"])}</div><div class="pagination-shortcut">Shortcut: <kbd>N</kbd> or <kbd>→</kbd></div></a>'
    else:
        next_url = ""
        next_arrow = '<a href="../index.html" class="nav-topic-arrow next disabled" title="End of Roadmap">›</a>'
        next_subnav = '<span class="subnav-nav-btn next disabled">Next →</span>'
        next_dock = '<span class="dock-btn next disabled">End →</span>'
        next_card = f'<a href="../index.html" class="pagination-card next"><div class="pagination-direction">ROADMAP COMPLETED ✓</div><div class="pagination-topic-meta">All {total} Topics Mastered</div><div class="pagination-title">Return to Architecture Explorer</div><div class="pagination-shortcut">Shortcut: <kbd>N</kbd> or <kbd>I</kbd></div></a>'

    header = f'''<!-- Navigation -->
<header class="site-nav"><div class="nav-container"><a href="../index.html" class="brand-link"><span style="font-size:16px;">☁</span><span class="brand-text">GCP ARCHITECT ROADMAP</span></a><div class="nav-topic-switcher">{prev_arrow}<div class="nav-select-wrapper"><select class="nav-topic-select" onchange="if(this.value) window.location.href=this.value;" title="Quick Jump to Any Topic">{"".join(options)}</select></div>{next_arrow}</div><nav class="nav-links"><a href="../index.html" class="nav-link">Overview</a><a href="#diagrams" class="nav-link">Diagrams</a><a href="#demo-or-practice" class="nav-link">Labs</a><a href="#quiz" class="nav-link">Knowledge Check</a></nav></div></header>'''
    subnav = f'''<!-- Topic Sub-Navigation Strip -->
<nav class="topic-subnav-strip" aria-label="Topic Sub-Navigation"><div class="subnav-breadcrumbs"><a href="../index.html" class="crumb-home">🗺 Roadmap Index</a><span class="crumb-sep">/</span><span class="crumb-phase">{esc(meta["phase"])}</span><span class="crumb-sep">/</span><span class="crumb-current">Topic {esc(meta["topic_no"])}</span><span class="crumb-progress">({index + 1} of {total})</span></div><div class="subnav-actions">{prev_subnav}<a href="../index.html" class="subnav-nav-btn" title="View all topics">☰ Index</a>{next_subnav}</div></nav>'''
    pagination = f'''<!-- Topic Pagination Footer -->
<nav class="topic-pagination" aria-label="Topic Pagination">{prev_card}<a href="../index.html" class="pagination-card index" title="Return to All Topics Index"><div class="pagination-direction">ROADMAP OVERVIEW</div><div class="pagination-topic-meta">All {total} Topics · {len(phases)} Phases</div><div class="pagination-title">Architecture Explorer</div><div class="pagination-shortcut">Key: <kbd>I</kbd></div></a>{next_card}</nav>'''
    floating = f'''<!-- Floating Quick Navigation Dock -->
<div class="floating-topic-dock" id="floating-topic-dock">{prev_dock}<span class="dock-indicator" title="Topic {esc(meta["topic_no"])} of {total}">{esc(meta["topic_no"])} / {esc(last_no)}</span>{next_dock}<a href="../index.html" class="dock-btn index" title="Roadmap Overview [Key: I]">☰</a></div>
<script>(function(){{const prevUrl={json.dumps(prev_url)};const nextUrl={json.dumps(next_url)};document.addEventListener('keydown',(e)=>{{if(['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName)||e.target.isContentEditable)return;if(e.key==='p'||e.key==='P'||e.key==='['||(e.key==='ArrowLeft'&&e.altKey)){{if(prevUrl)window.location.href=prevUrl;}}else if(e.key==='n'||e.key==='N'||e.key===']'||(e.key==='ArrowRight'&&e.altKey)){{if(nextUrl)window.location.href=nextUrl;}}else if(e.key==='i'||e.key==='I')window.location.href='../index.html';}});}})();</script>
<!-- End Floating Quick Navigation Dock -->'''
    return header, subnav, pagination, floating


def normalize_navigation(text: str, meta: dict, catalog: list[dict]) -> str:
    header, subnav, pagination, floating = navigation_markup(meta, catalog)
    text = re.sub(r'\s*<!-- Navigation -->\s*<header class="site-nav">.*?</header>', "\n" + header, text, count=1, flags=re.S)
    text = re.sub(r'\s*<header class="site-nav">.*?</header>', "\n" + header, text, count=1, flags=re.S)
    text = re.sub(r'\s*<!-- Topic Sub-Navigation Strip -->.*?</nav>\s*', "\n", text, count=1, flags=re.S)
    text = re.sub(r'\s*<nav class="topic-subnav-strip"[^>]*>.*?</nav>\s*', "\n", text, count=1, flags=re.S)
    text = text.replace('<main class="main-content">', '<main class="main-content">\n' + subnav, 1)
    text = re.sub(r'\s*<!-- Topic Pagination Footer -->.*?</nav>\s*', "\n", text, count=1, flags=re.S)
    text = re.sub(r'\s*<nav class="topic-pagination"[^>]*>.*?</nav>\s*', "\n", text, count=1, flags=re.S)
    text = text.replace('</main>', pagination + '\n</main>', 1)
    text = re.sub(r'\s*<!-- Floating Quick Navigation Dock -->.*?<!-- End Floating Quick Navigation Dock -->\s*', "\n", text, count=1, flags=re.S)
    text = text.replace('</body>', floating + '\n</body>', 1)
    return text


def normalize_quiz_markup(text: str) -> str:
    """Use valid button groups instead of buttons directly inside list elements."""
    match = re.search(r'(<section[^>]*\bid="quiz"[^>]*>.*?</section>)', text, re.S | re.I)
    if not match:
        return text
    quiz = match.group(1)
    quiz = re.sub(r'<ul\b[^>]*\bclass=["\'][^"\']*\bquiz-options\b[^"\']*["\'][^>]*>', '<div class="quiz-options" role="group" aria-label="Answer options">', quiz, flags=re.I)
    quiz = re.sub(r'</ul\s*>', '</div>', quiz, flags=re.I)

    def option_opening(option: re.Match[str]) -> str:
        attrs = option.group(1)
        if not re.search(r'\btype\s*=', attrs, re.I):
            attrs += ' type="button"'
        return f'<button{attrs}>'

    quiz = re.sub(r'<li\b([^>]*\bclass=["\'][^"\']*\bquiz-option\b[^"\']*["\'][^>]*)>', option_opening, quiz, flags=re.I)
    quiz = re.sub(r'</li\s*>', '</button>', quiz, flags=re.I)
    return text[:match.start()] + quiz + text[match.end():]


def personalize_shared_prose(text: str, meta: dict) -> str:
    """Break accidental copy-paste prose while keeping reusable quiz prompts intact."""
    title = esc(meta["title"])
    replacements = {
        "Shows identities, trust boundaries, policy checks, and audit evidence.": f"Shows identities, trust boundaries, policy checks, and audit evidence for <strong>{title}</strong>.",
        "Shows what changes at 10x load and where operational cost moves.": f"Shows what changes at 10x load for <strong>{title}</strong> and where operational cost moves.",
        "Shows the documented internals needed to predict behavior; undocumented details are observed behavior and may change.": f"Shows the documented internals needed to predict <strong>{title}</strong>; undocumented details are observed behavior and may change.",
        "Define resource scope, vocabulary, control plane, data plane, and the common wrong picture.": f"Define resource scope, vocabulary, control plane, data plane, and the common wrong picture for <strong>{title}</strong>.",
        "Set safe defaults and inspect IAM, APIs, quotas, networking, billing, and logs.": f"Set safe defaults for <strong>{title}</strong> and inspect IAM, APIs, quotas, networking, billing, and logs.",
        "Compare operational burden, scaling, consistency, cost, portability, and compliance.": f"Compare operational burden, scaling, consistency, cost, portability, and compliance for <strong>{title}</strong>.",
        "Predict behavior from internals, failure modes, blast radius, ownership, and day-two operations.": f"Predict <strong>{title}</strong> behavior from internals, failure modes, blast radius, ownership, and day-two operations.",
        "The city story follows Brightloaf through a problem, solution, stress event, and explicit limit.": f"The city story for <strong>{title}</strong> follows Brightloaf through a problem, solution, stress event, and explicit limit.",
        "Where the metaphor breaks: a city permit is physical and human; a cloud policy is evaluated by software and can be misconfigured. Verify the real behavior in documentation.": f"Where the metaphor breaks for <strong>{title}</strong>: a city permit is physical and human; a cloud policy is evaluated by software and can be misconfigured. Verify the real behavior in documentation.",
        "Architecture diagrams in this curriculum are not decorative illustrations; they are precision engineering models designed to answer three distinct, non-overlapping architectural questions for every topic:": f"Architecture diagrams for <strong>{title}</strong> are not decorative illustrations; they are precision engineering models designed to answer three distinct, non-overlapping architectural questions:",
        "Record the decision, rejected alternative, evidence to inspect, and recovery action.": f"Record the <strong>{title}</strong> decision, rejected alternative, evidence to inspect, and recovery action.",
        "A one-page decision record with assumptions and a verification date.": f"A one-page <strong>{title}</strong> decision record with assumptions and a verification date.",
        "Tier T0 read-only; no credentials or billing account are required to browse.": f"Tier T0 read-only for <strong>{title}</strong>; no credentials or billing account are required to browse.",
        "Open the relevant Cloud Console product, select the guarded project, use the smallest safe setting, and capture status and audit evidence.": f"Open the relevant Cloud Console product for <strong>{title}</strong>, select the guarded project, use the smallest safe setting, and capture status and audit evidence.",
        "Do not commit state or secrets; use remote locking and team ownership.": f"Do not commit <strong>{title}</strong> state or secrets; use remote locking and team ownership.",
        "Check status, audit logs, health metrics, and matching D1/D2 nodes.": f"Check <strong>{title}</strong> status, audit logs, health metrics, and matching D1/D2 nodes.",
    }
    for source, replacement in replacements.items():
        text = text.replace(source, replacement)
    text = text.replace(
        "Check project, API enablement, IAM, quota, DNS, firewall, logs, and eventual consistency.",
        f"Check project, API enablement, IAM, quota, DNS, firewall, logs, and eventual consistency for <strong>{title}</strong>.",
    )
    text = text.replace(
        "Destroy named resources, then verify deletion and billing asynchronously.",
        f"Destroy named <strong>{title}</strong> resources, then verify deletion and billing asynchronously.",
    )
    text = text.replace(
        "In a disposable project, revoke a narrow role, block a health check, or select an exhausted range. Observe, diagnose, and restore it.",
        f"In a disposable project for <strong>{title}</strong>, revoke a narrow role, block a health check, or select an exhausted range. Observe, diagnose, and restore it.",
    )
    text = text.replace(
        "The intended boundary is visible and the result is attributable to the guarded project.",
        f"The intended <strong>{title}</strong> boundary is visible and the result is attributable to the guarded project.",
    )
    text = text.replace(
        "Tier T2: use free-tier or cents-scale resources where available; verify current pricing and delete promptly. T4 topics are plan-only by default.",
        f"Tier T2 for <strong>{title}</strong>: use free-tier or cents-scale resources where available; verify current pricing and delete promptly. T4 topics are plan-only by default.",
    )
    return text


def ensure_page(path: Path, meta: dict, specs: dict[str, dict], catalog: list[dict]) -> None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    text = normalize_analogy_layout(text)
    text = personalize_shared_prose(text, meta)
    text = normalize_quiz_markup(text)
    text = normalize_navigation(text, meta, catalog)
    if 'id="references"' not in text:
        reading = re.search(r'(<section[^>]*\bid="reading"[^>]*>.*?</section>)', text, re.S | re.I)
        if reading:
            text = text[:reading.end()] + references_section(meta) + text[reading.end():]
        else:
            text = text.replace('</main>', references_section(meta) + '</main>', 1)
    if meta["topic_no"] in TAIL_PROFILES:
        text = replace_inline_specs(text, specs)
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
    text = replace_addendum(text, "part1-complete", part1_addendum(meta))
    text = replace_addendum(text, "depth-complete", part2_addendum(meta))
    if "class=\"part1-complete\"" not in text:
        text = text.replace("    </section>\n\n    <!-- Part 2: Technical", "      " + part1_addendum(meta) + "\n    </section>\n\n    <!-- Part 2: Technical", 1)
    if "class=\"depth-complete\"" not in text:
        text = text.replace("      <div id=\"diagrams\"", "      " + part2_addendum(meta) + "\n\n      <div id=\"diagrams\"", 1)
    if "class=\"demo-complete\"" not in text and "class=\"practice-complete\"" not in text:
        text = text.replace("    </section>\n\n    <!-- Footer 1: Knowledge Check -->", "      " + demo_addendum(meta) + "\n    </section>\n\n    <!-- Footer 1: Knowledge Check -->", 1)
    text = text.replace('id="practice"', 'id="demo-or-practice"', 1)
    if "demo-safety-banner" not in text and meta["page_type"] not in {"reference", "tracker"}:
        text = text.replace('<section class="topic-section" id="demo-or-practice">', '<section class="topic-section" id="demo-or-practice"><div class="demo-safety-banner"><strong>LIVE DEMO SAFETY:</strong> Confirm the disposable project, budget, region, IAM, plan, and cleanup before any create or apply action.</div>', 1)
    if 'id="analogy-scene"' not in text:
        text = insert_after_analogy_div(
            text,
            '<div id="analogy-scene" class="analogy-scene" tabindex="0" aria-label="Interactive Cloud City analogy scene"></div>',
            element_id="analogy-display",
        )
    if "class=\"analogy-mapping\"" not in text:
        text = insert_after_analogy_div(
            text,
            '<div class="analogy-mapping"><h3>Cloud City mapping table</h3><p>Brightloaf campus maps to the topic resource; permits map to IAM and policy; roads map to networking and dependencies; emergency response maps to recovery operations.</p><p><strong>Where the metaphor breaks:</strong> cloud policies are software rules, not physical walls. Verify the real behavior in documentation.</p></div>',
            element_id="analogy-scene",
        )
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
    text = re.sub(r'\s*<sup class="claim-citation">.*?</sup>', '', text, flags=re.S)
    text = annotate_claims(text, meta)
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
    if meta["topic_no"] in TAIL_PROFILES:
        specs = {kind: tail_spec(meta, kind) for kind in ("d1", "d2", "d3", "d4", "d5", "d6")}
    else:
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
        references_section(meta),
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
    catalog = topic_catalog()
    for path in sorted(PAGES.glob("topic-*.html")):
        meta = page_meta(path)
        if not meta["roadmap_id"]:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if meta["topic_no"] in TAIL_PROFILES:
            specs = {kind: tail_spec(meta, kind) for kind in ("d1", "d2", "d3", "d4", "d5", "d6")}
        else:
            specs = {kind: normalize_spec(get_inline_spec(text, kind), meta, kind) for kind in ("d1", "d2", "d3")}
            specs.update({kind: derived_spec(meta, kind, specs["d1"]) for kind in ("d4", "d5", "d6")})
        for kind, spec in specs.items():
            (DIAGRAMS / f"topic-{meta['topic_no']}-{kind}.json").write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
            (DIAGRAMS / f"topic-{meta['topic_no']}-{kind}.html").write_text(standalone_html(spec), encoding="utf-8")
        ensure_page(path, meta, specs, catalog)
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


def main(roadmap: Path | None = None) -> None:
    global ROADMAP_ITEMS
    PAGES.mkdir(exist_ok=True)
    DIAGRAMS.mkdir(exist_ok=True)
    ANALOGY.mkdir(exist_ok=True)
    GENERATED.mkdir(exist_ok=True)
    default_roadmap = ROOT.parent / "gcp-architect-roadmap.md"
    ROADMAP_ITEMS = load_roadmap_items(roadmap or default_roadmap)
    create_missing_pages()
    normalize_all_pages()
    write_index()
    write_artifacts()
    print(f"Repaired {len(list(PAGES.glob('topic-*.html')))} topic pages.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roadmap", type=Path, help="Roadmap Markdown source used for topic-specific guidance")
    args = parser.parse_args()
    main(args.roadmap)
