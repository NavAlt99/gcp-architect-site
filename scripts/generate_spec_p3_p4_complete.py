#!/usr/bin/env python3
"""
generate_spec_p3_p4_complete.py - Populates spec_p3_p4.py with all 12 topics:
022: Requirements Analysis: Discovery
023: Google Cloud Architecture Framework
024: Reference Architectures & Patterns
025: Migration & Modernization: The 6 Rs
026: Decision Frameworks: ADRs & Matrices
027: Diagramming & Docs: C4 Model
028: Reliability Fundamentals & Availability
029: SRE Concepts: SLIs, SLOs & Error Budgets
030: High Availability by Layer
031: Disaster Recovery Patterns (RTO & RPO)
032: Observability: Monitoring, Logs & Trace
033: Testing for Reliability: Load & Chaos
"""

import os
import json
import spec_p3_p4

existing_specs = spec_p3_p4.get_specs()

# We will define the new topics to complete Phase 3 and Phase 4
new_specs = {}

def make_spec(t_no, r_id, title,
              d1_p, d1_r, d1_g, d1_n, d1_e, d1_s, d1_sc,
              d2_p, d2_r, d2_g, d2_n, d2_e, d2_s, d2_sc,
              d3_p, d3_r, d3_g, d3_n, d3_e, d3_s, d3_sc):
    return {
        "topic_no": f"{t_no:03d}",
        "roadmap_id": r_id,
        "title": title,
        "d1_purpose": d1_p, "d1_rationale": d1_r, "d1_groups": d1_g, "d1_nodes": d1_n, "d1_edges": d1_e, "d1_steps": d1_s, "d1_scenarios": d1_sc,
        "d2_purpose": d2_p, "d2_rationale": d2_r, "d2_groups": d2_g, "d2_nodes": d2_n, "d2_edges": d2_e, "d2_steps": d2_s, "d2_scenarios": d2_sc,
        "d3_purpose": d3_p, "d3_rationale": d3_r, "d3_groups": d3_g, "d3_nodes": d3_n, "d3_edges": d3_e, "d3_steps": d3_s, "d3_scenarios": d3_sc,
    }

# 023: Google Cloud Architecture Framework
new_specs[23] = make_spec(
    23, "3.2", "Google Cloud Architecture Framework",
    "Visualizes the 5 pillars of the Google Cloud Architecture Framework: System Design, Operational Excellence, Security/Privacy, Reliability, and Cost Optimization mapped onto enterprise governance layers.",
    "A well-architected cloud footprint balances all five pillars simultaneously; over-optimizing one pillar (e.g. cost) without honoring security guardrails or reliability targets creates severe technical debt.",
    [
        {"id": "g-gov", "label": "Enterprise Governance & Security Pillar", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
        {"id": "g-ops", "label": "System Design & Operational Excellence", "type": "project", "scope": "project", "x": 300, "y": 30, "width": 310, "height": 360},
        {"id": "g-rel-cost", "label": "Reliability & Cost Optimization Tier", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
    ],
    [
        {"id": "pillar-sec", "label": "Security & Zero Trust Guardrail", "product": "Org Policy & IAM", "group": "g-gov", "plane": "control", "x": 140, "y": 140, "detail": "Restricts public IPs, enforces CMEK encryption keys, and enforces VPC Service Controls."},
        {"id": "pillar-ops", "label": "Operational Excellence Pipeline", "product": "Cloud Build & Deploy", "group": "g-ops", "plane": "control", "x": 440, "y": 140, "detail": "Automated GitOps CI/CD with progressive delivery, canary validation, and health checks."},
        {"id": "pillar-sys", "label": "System Design Architecture", "product": "Stateless Microservices", "group": "g-ops", "plane": "data", "x": 440, "y": 280, "detail": "Loosely-coupled event-driven microservices communicating over asynchronous Pub/Sub."},
        {"id": "pillar-rel", "label": "Reliability & Multi-Zone HA", "product": "Regional MIG & Cloud SQL HA", "group": "g-rel-cost", "plane": "data", "x": 780, "y": 140, "detail": "Redundant active-standby instances with automatic cross-zone failover < 60 seconds."},
        {"id": "pillar-cost", "label": "FinOps Cost Guardrails", "product": "Budgets, CUDs & Recommender", "group": "g-rel-cost", "plane": "control", "x": 780, "y": 280, "detail": "Continuous rightsizing recommendations, 3-year committed use discounts, and autoscaling caps."}
    ],
    [
        {"id": "e1", "from": "pillar-sec", "to": "pillar-ops", "label": "1. Enforce Security Policies in CI/CD", "plane": "control"},
        {"id": "e2", "from": "pillar-ops", "to": "pillar-sys", "label": "2. Deploy Validated Microservices", "plane": "data"},
        {"id": "e3", "from": "pillar-sys", "to": "pillar-rel", "label": "3. Provision Multi-Zone Redundancy", "plane": "data"},
        {"id": "e4", "from": "pillar-rel", "to": "pillar-cost", "label": "4. Apply Cost Optimization & CUDs", "plane": "control"}
    ],
    [
        {"n": 1, "title": "Security Guardrail Verification", "edges": ["e1"], "action": "Architecture Framework validates IAM least-privilege and VPC-SC perimeters.", "why_traversal": "Security posture must be validated before operational deployment.", "protocol": "Policy as Code", "plane": "Control Plane"},
        {"n": 2, "title": "Operational Delivery", "edges": ["e2"], "action": "Cloud Build applies container security scanning and deploys stateless containers.", "why_traversal": "Ensures reproducible, immutable artifacts across dev, stage, and prod.", "protocol": "GitOps Delivery", "plane": "Control Plane"},
        {"n": 3, "title": "Reliability & Cost Synthesis", "edges": ["e3", "e4"], "action": "Regional MIG instances paired with 1-year CUDs satisfy uptime target within budget.", "why_traversal": "Balances high availability with financial predictability.", "protocol": "FinOps Analysis", "plane": "Data Plane"}
    ],
    [
        {"id": "pillar-conflict", "label": "Cost Cutting Compromises Disaster Recovery", "changes": {"failedNodes": ["pillar-rel"], "failedEdges": ["e3"]}, "root_cause": "Team disabled cross-zone standby database to save 40% compute costs.", "diverted_path": "Zone failure causes 6-hour catastrophic outage with data loss.", "blast_radius": "Production database down during zonal incident.", "recovery": "Re-enable multi-zone HA and leverage Committed Use Discounts (CUDs) to achieve cost goals safely."}
    ],
    # D2
    "Traces the Architecture Review Lifecycle: from business requirements submission through 5-pillar scorecard evaluation to final deployment approval.",
    "Structured architecture reviews evaluate risks against formal checklists across each pillar, producing actionable Architecture Decision Records (ADRs).",
    [
        {"id": "g-submission", "label": "Project Intake & Architecture Proposal", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
        {"id": "g-review-board", "label": "Architecture Review Board (ARB) Evaluation", "type": "project", "scope": "project", "x": 300, "y": 30, "width": 310, "height": 360},
        {"id": "g-prod-landing", "label": "Approved Infrastructure Deployment", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
    ],
    [
        {"id": "arch-proposal", "label": "RFC Architecture Proposal", "product": "Design Document v1", "group": "g-submission", "plane": "control", "x": 140, "y": 140, "detail": "Engineers submit RFC detailing new event processing service on Google Cloud."},
        {"id": "scorecard-sec", "label": "Security Scorecard Check", "product": "VPC-SC / KMS Review", "group": "g-review-board", "plane": "control", "x": 440, "y": 100, "detail": "Reviews customer data classification, encryption key rotation, and perimeter ingress."},
        {"id": "scorecard-rel", "label": "Reliability & SLO Audit", "product": "Target: 99.95% SLO", "group": "g-review-board", "plane": "control", "x": 440, "y": 200, "detail": "Validates regional redundancy, circuit breakers, and RTO/RPO disaster recovery procedures."},
        {"id": "scorecard-cost", "label": "FinOps Sizing Model", "product": "Monthly TCO Forecast", "group": "g-review-board", "plane": "control", "x": 440, "y": 300, "detail": "Reviews projected spend against cost center allocation and commits."},
        {"id": "arb-approval", "label": "Signed Architecture Record", "product": "ADR-042 Approved", "group": "g-prod-landing", "plane": "control", "x": 780, "y": 200, "detail": "Architecture Decision Record recorded in Git; triggers Terraform release pipeline."}
    ],
    [
        {"id": "e1", "from": "arch-proposal", "to": "scorecard-sec", "label": "1. Submit for Security Review", "plane": "control"},
        {"id": "e2", "from": "arch-proposal", "to": "scorecard-rel", "label": "2. Verify Resilience Architecture", "plane": "control"},
        {"id": "e3", "from": "arch-proposal", "to": "scorecard-cost", "label": "3. Analyze FinOps Sizing", "plane": "control"},
        {"id": "e4", "from": "scorecard-sec", "to": "arb-approval", "label": "4. Security Sign-off", "plane": "control"},
        {"id": "e5", "from": "scorecard-rel", "to": "arb-approval", "label": "5. SRE Sign-off", "plane": "control"},
        {"id": "e6", "from": "scorecard-cost", "to": "arb-approval", "label": "6. FinOps Sign-off", "plane": "control"}
    ],
    [
        {"n": 1, "title": "Multi-Pillar Scorecard Review", "edges": ["e1", "e2", "e3"], "action": "Proposal evaluated in parallel across Security, Reliability, and Cost pillars.", "why_traversal": "Parallel reviews identify trade-offs before code and infrastructure are committed.", "protocol": "Review Checklist", "plane": "Control Plane"},
        {"n": 2, "title": "Consensus & Formal Approval", "edges": ["e4", "e5", "e6"], "action": "All three leads endorse design; ADR is signed and checked into Git repository.", "why_traversal": "Maintains immutable architectural governance trail for auditability.", "protocol": "ADR Signing", "plane": "Control Plane"}
    ],
    [
        {"id": "sec-rejection", "label": "Security Gate Blocks Unencrypted Public Storage", "changes": {"failedNodes": ["scorecard-sec"], "failedEdges": ["e4"]}, "root_cause": "Proposal attempted to use public GCS bucket for staging client uploads.", "diverted_path": "Automated security linter flags violation; ARB rejects design.", "blast_radius": "Deployment blocked until design updated.", "recovery": "Revise proposal to use Private Service Connect with signed upload URLs."}
    ],
    # D3
    "Simulates architectural drift: unauthorized infrastructure change detected by Security Command Center and auto-remediated via Cloud Functions.",
    "Real-time posture management detects misconfigurations that diverge from approved architectural baselines and triggers instant policy enforcement.",
    [
        {"id": "g-drift-source", "label": "Unauthorized Configuration Drift", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
        {"id": "g-auto-remediation", "label": "Automated Security Remediation Pipeline", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
    ],
    [
        {"id": "rogue-firewall", "label": "Rogue Firewall Rule", "product": "Allow 0.0.0.0/0 on Port 22", "group": "g-drift-source", "plane": "data", "x": 220, "y": 140, "detail": "Developer manually opened public SSH port to debug a production issue."},
        {"id": "scc-detector", "label": "Security Command Center", "product": "Finding: OPEN_SSH_PORT", "group": "g-drift-source", "plane": "control", "x": 220, "y": 280, "detail": "SCC Real-time posture engine flags high-severity vulnerability within 15 seconds."},
        {"id": "pubsub-alert", "label": "Security Finding Event", "product": "Pub/Sub Notification Topic", "group": "g-auto-remediation", "plane": "control", "x": 700, "y": 140, "detail": "SCC streams JSON finding event to pubsub topic 'security-auto-heal'."},
        {"id": "remediate-fn", "label": "Auto-Remediation Function", "product": "Cloud Run Event Receiver", "group": "g-auto-remediation", "plane": "control", "x": 700, "y": 280, "detail": "Invokes Compute Engine API to immediately delete rogue firewall rule."}
    ],
    [
        {"id": "e1", "from": "rogue-firewall", "to": "scc-detector", "label": "1. Detect Security Policy Drift", "plane": "control"},
        {"id": "e2", "from": "scc-detector", "to": "pubsub-alert", "label": "2. Publish Violation Finding", "plane": "control"},
        {"id": "e3", "from": "pubsub-alert", "to": "remediate-fn", "label": "3. Trigger Remediation Function", "plane": "control"}
    ],
    [
        {"n": 1, "title": "Continuous Posture Detection", "edges": ["e1"], "action": "SCC scans resource changes and identifies open SSH port violating org policy.", "why_traversal": "Eliminates reliance on periodic manual audits; catches exposures immediately.", "protocol": "Cloud Asset Inventory Notification", "plane": "Control Plane"},
        {"n": 2, "title": "Event-Driven Orchestration", "edges": ["e2", "e3"], "action": "Alert streams through Pub/Sub to trigger serverless remediation handler.", "why_traversal": "Decouples detection from automated action, enabling auditable remediation.", "protocol": "Cloud Pub/Sub", "plane": "Control Plane"},
        {"n": 3, "title": "Automated Policy Restoration", "edges": [], "action": "Cloud Run function deletes rogue rule and alerts SecOps in Slack.", "why_traversal": "Reduces mean time to remediate (MTTR) from hours to 8 seconds.", "protocol": "Compute Engine REST API", "plane": "Control Plane"}
    ],
    [
        {"id": "remediation-loop", "label": "IAM Permission Deprivation on Remediation SA", "changes": {"failedNodes": ["remediate-fn"], "failedEdges": ["e3"]}, "root_cause": "Remediation Service Account lacked compute.securityPolicies.delete permission.", "diverted_path": "Remediation function throws HTTP 403 Forbidden; rogue rule remains open.", "blast_radius": "Compute instance exposed to internet scanning for 4 hours.", "recovery": "Grant custom role with exact required permissions and set up failure alert on remediation function errors."}
    ]
)

# 024: Reference Architectures & Patterns
new_specs[24] = make_spec(
    24, "3.3", "Reference Architectures & Patterns",
    "Visualizes production enterprise 3-tier cloud reference architecture: Global Cloud Armor + Cloud CDN edge, autoscaled container microservices in private subnets, and Cloud Spanner / Memorystore data persistence.",
    "Separating edge security, application business logic, and transactional storage into distinct tiers enforces defense-in-depth and independent scaling boundaries.",
    [
        {"id": "g-edge", "label": "Global Edge & Acceleration Tier", "type": "external", "scope": "global", "x": 30, "y": 30, "width": 240, "height": 360},
        {"id": "g-app", "label": "Application Microservices Tier (Private)", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
        {"id": "g-data", "label": "Persistence & Cache Data Tier", "type": "project", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
    ],
    [
        {"id": "edge-lb", "label": "External Application Load Balancer", "product": "Global Anycast + Cloud Armor", "group": "g-edge", "plane": "data", "x": 140, "y": 140, "detail": "Terminates TLS handshakes at edge, inspects OWASP Top 10 rules, and caches static assets."},
        {"id": "cloud-cdn", "label": "Cloud CDN Edge Cache", "product": "Edge Cache Point of Presence", "group": "g-edge", "plane": "data", "x": 140, "y": 280, "detail": "Serves 85% of static asset requests directly from Google edge PoP caches."},
        {"id": "gke-app", "label": "GKE App Microservices", "product": "Autopilot Regional Cluster", "group": "g-app", "plane": "data", "x": 440, "y": 140, "detail": "Private cluster across 3 zones running business logic pods behind Internal ALB."},
        {"id": "redis-cache", "label": "Memorystore for Redis", "product": "HA In-Memory Cache", "group": "g-data", "plane": "data", "x": 780, "y": 140, "detail": "Sub-millisecond latency cache for hot product catalog and session data."},
        {"id": "spanner-db", "label": "Cloud Spanner Multi-Region", "product": "Globally Consistent Relational DB", "group": "g-data", "plane": "data", "x": 780, "y": 280, "detail": "Multi-region database delivering 99.999% availability with external consistency."}
    ],
    [
        {"id": "e1", "from": "edge-lb", "to": "cloud-cdn", "label": "1. Check Edge Cache", "plane": "data"},
        {"id": "e2", "from": "edge-lb", "to": "gke-app", "label": "2. Forward Dynamic Requests", "plane": "data"},
        {"id": "e3", "from": "gke-app", "to": "redis-cache", "label": "3. Query Hot Cache", "plane": "data"},
        {"id": "e4", "from": "gke-app", "to": "spanner-db", "label": "4. Read/Write Persistent DB", "plane": "data"}
    ],
    [
        {"n": 1, "title": "Edge Inspection & Caching", "edges": ["e1", "e2"], "action": "Cloud Armor inspects request; Cloud CDN serves cached content or forwards to GKE.", "why_traversal": "Absorbs traffic at Google edge, reducing load on backend microservices.", "protocol": "HTTPS / QUIC", "plane": "Data Plane"},
        {"n": 2, "title": "Microservice Processing", "edges": ["e3", "e4"], "action": "GKE pods check Redis for product data; fallback to Cloud Spanner on cache miss.", "why_traversal": "Cache-aside pattern optimizes read latency to under 2ms for 90% of requests.", "protocol": "gRPC / Spanner API", "plane": "Data Plane"}
    ],
    [
        {"id": "cache-stampede", "label": "Cache Eviction Thundering Herd", "changes": {"failedNodes": ["redis-cache"], "failedEdges": ["e3"]}, "root_cause": "Memorystore Redis node restarted during scheduled maintenance without cluster replication.", "diverted_path": "50,000 requests/sec simultaneously bypass cache and hammer Cloud Spanner.", "blast_radius": "Database latency spikes from 8ms to 850ms.", "recovery": "Enable Memorystore HA with automatic failover and deploy client-side probabilistic early expiration."}
    ],
    # D2
    "Traces the End-to-End Cache-Aside Request Flow: demonstrates request dispatch, cache lookup, Spanner query on miss, and asynchronous cache repopulation.",
    "A clean cache-aside implementation guarantees fresh data while protecting backend relational databases from read query exhaustion.",
    [
        {"id": "g-client-req", "label": "Client Ingress & Load Balancing", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
        {"id": "g-service-logic", "label": "Service Layer & Cache Validation", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
        {"id": "g-storage-tier", "label": "Transactional Storage Layer", "type": "project", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
    ],
    [
        {"id": "user-client", "label": "Mobile / Web Client", "product": "HTTPS Request", "group": "g-client-req", "plane": "data", "x": 140, "y": 140, "detail": "User navigates to catalog item /products/sku-99214."},
        {"id": "app-service", "label": "Catalog Microservice", "product": "Cloud Run Container", "group": "g-service-logic", "plane": "data", "x": 440, "y": 140, "detail": "Receives request; executes cache-aside lookup logic."},
        {"id": "cache-store", "label": "Memorystore Redis", "product": "Cache Miss / Hit Lookup", "group": "g-service-logic", "plane": "data", "x": 440, "y": 280, "detail": "Stores JSON serialized catalog items with 1-hour TTL."},
        {"id": "spanner-data", "label": "Cloud Spanner Leader", "product": "Primary Paxos Replica", "group": "g-storage-tier", "plane": "data", "x": 780, "y": 140, "detail": "Executes SELECT * FROM Products WHERE Sku = 'sku-99214'."},
        {"id": "pubsub-invalidate", "label": "Cloud Pub/Sub Invalidation", "product": "Cache Eviction Topic", "group": "g-storage-tier", "plane": "control", "x": 780, "y": 280, "detail": "Publishes cache invalidation event when catalog updates occur."}
    ],
    [
        {"id": "e1", "from": "user-client", "to": "app-service", "label": "1. GET /products/sku-99214", "plane": "data"},
        {"id": "e2", "from": "app-service", "to": "cache-store", "label": "2. Redis GET sku-99214", "plane": "data"},
        {"id": "e3", "from": "app-service", "to": "spanner-data", "label": "3. Spanner Query (Cache Miss)", "plane": "data"},
        {"id": "e4", "from": "spanner-data", "to": "cache-store", "label": "4. Redis SETEX (Backfill)", "plane": "data"},
        {"id": "e5", "from": "spanner-data", "to": "pubsub-invalidate", "label": "5. Publish Invalidation on Mutation", "plane": "control"}
    ],
    [
        {"n": 1, "title": "Cache Evaluation", "edges": ["e1", "e2"], "action": "App service queries Redis for SKU. If key exists, returns payload immediately in 1.2ms.", "why_traversal": "Eliminates roundtrips to relational database for repeated read queries.", "protocol": "RESP (Redis)", "plane": "Data Plane"},
        {"n": 2, "title": "Persistence Query & Cache Repopulation", "edges": ["e3", "e4"], "action": "On cache miss, queries Spanner, returns response to user, and asynchronously populates Redis.", "why_traversal": "Ensures subsequent requests for this SKU hit memory cache.", "protocol": "gRPC / Redis Protocol", "plane": "Data Plane"},
        {"n": 3, "title": "Cache Coherence Invalidation", "edges": ["e5"], "action": "When inventory or price changes, Spanner commit triggers Pub/Sub to invalidate Redis key.", "why_traversal": "Prevents stale inventory or incorrect pricing data from persisting in cache.", "protocol": "Pub/Sub Fan-out", "plane": "Control Plane"}
    ],
    [
        {"id": "stale-cache-leak", "label": "Deadlock Invalidation Worker", "changes": {"failedNodes": ["pubsub-invalidate"], "failedEdges": ["e5"]}, "root_cause": "Invalidation subscriber crashed due to unhandled JSON schema change.", "diverted_path": "Redis cache serves out-of-date product pricing for 60 minutes.", "blast_radius": "Customers buy items at incorrect prices.", "recovery": "Deploy schema validation on Pub/Sub messages and add dead-letter topic alerting."}
    ],
    # D3
    "Simulates regional database network partition: illustrates Cloud Spanner automatic Paxos quorum failover with zero data loss.",
    "Cloud Spanner maintains external consistency and zero RPO by requiring a majority quorum of voting replicas across 3 regions before committing any transaction.",
    [
        {"id": "g-primary-region", "label": "Region 1: us-central1 (Voting Leader)", "type": "region", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
        {"id": "g-secondary-region", "label": "Region 2: us-east1 (Quorum Voting Replicas)", "type": "region", "scope": "regional", "x": 480, "y": 30, "width": 440, "height": 360}
    ],
    [
        {"id": "spanner-r1-leader", "label": "Spanner Leader (us-central1)", "product": "Primary Paxos Leader", "group": "g-primary-region", "plane": "data", "x": 220, "y": 140, "detail": "Coordinates transaction 2-phase commits and local read locks."},
        {"id": "app-r1", "label": "GKE App Pods (us-central1)", "product": "Local Service Clients", "group": "g-primary-region", "plane": "data", "x": 220, "y": 280, "detail": "Routes database reads and writes to local Spanner leader node."},
        {"id": "spanner-r2-replica", "label": "Spanner Paxos Replica (us-east1)", "product": "Voting Quorum Member", "group": "g-secondary-region", "plane": "data", "x": 700, "y": 140, "detail": "Replicates write logs and votes on transaction commit consensus."},
        {"id": "witness-r3", "label": "Witness Region (us-west1)", "product": "Tie-Breaker Witness", "group": "g-secondary-region", "plane": "control", "x": 700, "y": 280, "detail": "Participates in voting without storing full persistent database data."}
    ],
    [
        {"id": "e1", "from": "app-r1", "to": "spanner-r1-leader", "label": "1. Transaction Commit Request", "plane": "data"},
        {"id": "e2", "from": "spanner-r1-leader", "to": "spanner-r2-replica", "label": "2. Paxos Replicate Log", "plane": "data"},
        {"id": "e3", "from": "spanner-r1-leader", "to": "witness-r3", "label": "3. Request Quorum Vote", "plane": "control"}
    ],
    [
        {"n": 1, "title": "Transaction Propose", "edges": ["e1"], "action": "GKE sends write transaction to local Spanner leader node in us-central1.", "why_traversal": "Clients communicate directly with the Paxos leader for low-latency writes.", "protocol": "Spanner gRPC", "plane": "Data Plane"},
        {"n": 2, "title": "Paxos Consensus Round", "edges": ["e2", "e3"], "action": "Leader replicates write log to us-east1 and witness in us-west1 to obtain 2/3 majority.", "why_traversal": "Majority agreement guarantees durability before acknowledgment.", "protocol": "Paxos Consensus", "plane": "Data Plane"}
    ],
    [
        {"id": "leader-region-down", "label": "Total us-central1 Regional Blackout", "changes": {"failedNodes": ["spanner-r1-leader", "app-r1"], "failedEdges": ["e1", "e2"]}, "root_cause": "Catastrophic fiber cut isolates entire us-central1 Google data center facility.", "diverted_path": "us-east1 replica and us-west1 witness elect us-east1 as new Paxos leader in < 5 seconds.", "blast_radius": "Zero data loss (RPO = 0); application traffic redirects to us-east1 in < 15 seconds.", "recovery": "Global Application Load Balancer shifts all user traffic to healthy us-east1 GKE cluster."}
    ]
)

# 025: Migration Strategies & The 6 Rs
new_specs[25] = make_spec(
    25, "3.4", "Migration Strategies & The 6 Rs",
    "Visualizes the 6 Rs Enterprise Migration Framework (Rehost, Replatform, Refactor, Repurchase, Retain, Retire) and Google Cloud migration tooling (Migrate to Virtual Machines, DMS, Storage Transfer Service).",
    "Selecting the proper migration path balances migration velocity, operational refactoring cost, and long-term cloud native agility.",
    [
        {"id": "g-onprem", "label": "Legacy On-Premise Data Center", "type": "onprem", "scope": "onprem", "x": 30, "y": 30, "width": 240, "height": 360},
        {"id": "g-migration-tools", "label": "Google Cloud Migration Engine", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
        {"id": "g-gcp-landing", "label": "Target Cloud Landing Zone", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
    ],
    [
        {"id": "legacy-vm", "label": "VMware ESXi Workloads", "product": "On-Prem Virtual Machines", "group": "g-onprem", "plane": "data", "x": 140, "y": 140, "detail": "Monolithic enterprise applications running on legacy VMware vSphere infrastructure."},
        {"id": "legacy-oracle", "label": "On-Prem Oracle / MySQL DB", "product": "Enterprise Relational DB", "group": "g-onprem", "plane": "data", "x": 140, "y": 280, "detail": "Core transaction database holding critical customer transaction history."},
        {"id": "m4vm-engine", "label": "Migrate to Virtual Machines", "product": "Agentless Replication Engine", "group": "g-migration-tools", "plane": "control", "x": 440, "y": 140, "detail": "Streams OS disk blocks directly into Google Cloud Persistent Disk with zero downtime."},
        {"id": "dms-engine", "label": "Database Migration Service", "product": "Continuous CDC Replication", "group": "g-migration-tools", "plane": "control", "x": 440, "y": 280, "detail": "Serverless streaming replication with schema translation to Cloud SQL / AlloyDB."},
        {"id": "gce-migrated", "label": "Compute Engine / GKE", "product": "Modernized Cloud Workload", "group": "g-gcp-landing", "plane": "data", "x": 780, "y": 140, "detail": "Rehosted VMs running on Compute Engine or refactored into GKE containers."},
        {"id": "cloudsql-target", "label": "Cloud SQL / AlloyDB", "product": "Fully Managed Database", "group": "g-gcp-landing", "plane": "data", "x": 780, "y": 280, "detail": "Target managed database running with automatic maintenance, HA, and automated backups."}
    ],
    [
        {"id": "e1", "from": "legacy-vm", "to": "m4vm-engine", "label": "1. Replicate VM Disk Blocks", "plane": "data"},
        {"id": "e2", "from": "legacy-oracle", "to": "dms-engine", "label": "2. Stream Binlog / CDC Data", "plane": "data"},
        {"id": "e3", "from": "m4vm-engine", "to": "gce-migrated", "label": "3. Launch Compute Engine Instance", "plane": "data"},
        {"id": "e4", "from": "dms-engine", "to": "cloudsql-target", "label": "4. Synchronize Target Database", "plane": "data"}
    ],
    [
        {"n": 1, "title": "Continuous Background Replication", "edges": ["e1", "e2"], "action": "M4VM and DMS stream data over Dedicated Interconnect while on-prem services remain live.", "why_traversal": "Eliminates multi-day maintenance outages during enterprise data synchronization.", "protocol": "TLS Block Streaming / CDC", "plane": "Data Plane"},
        {"n": 2, "title": "Final Cutover & Launch", "edges": ["e3", "e4"], "action": "Final delta sync completes in < 3 minutes; traffic switches over to GCP with minimal downtime.", "why_traversal": "Provides clean, controlled cutover with verified data consistency.", "protocol": "Cutover Orchestration", "plane": "Control Plane"}
    ],
    [
        {"id": "cutover-network-stall", "label": "Interconnect Bandwidth Saturation", "changes": {"failedNodes": ["m4vm-engine"], "failedEdges": ["e1"]}, "root_cause": "Under-sized Cloud Interconnect saturated by unthrottled block replication.", "diverted_path": "Production on-prem traffic experiences high packet loss.", "blast_radius": "On-prem user response times degrade.", "recovery": "Enable bandwidth rate limiting on M4VM replication schedules during business hours."}
    ],
    # D2
    "Traces the Step-by-Step Low-Downtime Migration Cutover: baseline sync, continuous CDC delta replication, application quiesce, and DNS flip.",
    "Orchestrating database quiescence before final DNS record updates prevents split-brain writes and ensures zero data loss during cloud cutovers.",
    [
        {"id": "g-source-env", "label": "Source On-Premise Environment", "type": "onprem", "scope": "onprem", "x": 30, "y": 30, "width": 240, "height": 360},
        {"id": "g-cutover-ctl", "label": "Cutover Automation Controller", "type": "project", "scope": "project", "x": 300, "y": 30, "width": 310, "height": 360},
        {"id": "g-dest-env", "label": "Target Google Cloud Production", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
    ],
    [
        {"id": "onprem-app", "label": "On-Prem Application Server", "product": "Source Web & App Tier", "group": "g-source-env", "plane": "data", "x": 140, "y": 140, "detail": "Active source application serving live customer traffic."},
        {"id": "onprem-db", "label": "Source MySQL 8.0 Primary", "product": "Source Transaction DB", "group": "g-source-env", "plane": "data", "x": 140, "y": 280, "detail": "Replicating write binlogs continuously to Database Migration Service."},
        {"id": "dms-streamer", "label": "DMS Continuous CDC", "product": "Lag < 2 seconds", "group": "g-cutover-ctl", "plane": "control", "x": 440, "y": 200, "detail": "Maintains sub-second replication synchronization between source and target."},
        {"id": "dns-switcher", "label": "Cloud DNS Record Manager", "product": "TTL = 60 seconds", "group": "g-dest-env", "plane": "control", "x": 780, "y": 140, "detail": "Updates api.company.com A record from on-prem IP to GCP Anycast VIP."},
        {"id": "target-alloydb", "label": "Target AlloyDB / Cloud SQL", "product": "Promoted to Primary DB", "group": "g-dest-env", "plane": "data", "x": 780, "y": 280, "detail": "Promoted from replica to standalone primary; opens read/write connections."}
    ],
    [
        {"id": "e1", "from": "onprem-db", "to": "dms-streamer", "label": "1. Stream Delta Transactions", "plane": "data"},
        {"id": "e2", "from": "dms-streamer", "to": "target-alloydb", "label": "2. Apply to Target Instance", "plane": "data"},
        {"id": "e3", "from": "onprem-app", "to": "onprem-db", "label": "3. Quiesce Writes (Maintenance)", "plane": "control"},
        {"id": "e4", "from": "dms-streamer", "to": "target-alloydb", "label": "4. Promote Target to Primary", "plane": "control"},
        {"id": "e5", "from": "dns-switcher", "to": "target-alloydb", "label": "5. Update DNS to GCP VIP", "plane": "control"}
    ],
    [
        {"n": 1, "title": "Continuous Delta Synchronization", "edges": ["e1", "e2"], "action": "DMS maintains real-time replication lag below 2 seconds.", "why_traversal": "Prepares target database for instantaneous cutover.", "protocol": "MySQL Binlog Replication", "plane": "Data Plane"},
        {"n": 2, "title": "Graceful Quiesce & Promote", "edges": ["e3", "e4"], "action": "Source app placed in read-only mode; DMS applies final delta and promotes target.", "why_traversal": "Eliminates risk of in-flight write loss.", "protocol": "DMS Promotion API", "plane": "Control Plane"},
        {"n": 3, "title": "Global Traffic Redirection", "edges": ["e5"], "action": "Cloud DNS flips A record to Google Cloud External Load Balancer VIP.", "why_traversal": "Clients transition seamlessly to cloud environment within 60 seconds.", "protocol": "Anycast DNS", "plane": "Control Plane"}
    ],
    [
        {"id": "split-brain-write", "label": "Split-Brain Write Conflict", "changes": {"failedNodes": ["onprem-app"], "failedEdges": ["e3"]}, "root_cause": "Old on-prem app remained in read-write mode after DNS flip due to stale client DNS caches.", "diverted_path": "5% of customers continued writing to on-prem database while 95% wrote to GCP.", "blast_radius": "Data reconciliation conflict across two database primaries.", "recovery": "Immediately sever network connectivity from on-prem app to source database."}
    ],
    # D3
    "Simulates migration rollback scenario: undetected application defect forces emergency reversal of cutover without data loss.",
    "Reverse replication pipelines established during cutover guarantee a safe fallback path if critical production bugs appear in the cloud environment.",
    [
        {"id": "g-cloud-rollback", "label": "Google Cloud Target (Post-Cutover)", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
        {"id": "g-onprem-fallback", "label": "On-Prem Fallback Environment", "type": "onprem", "scope": "onprem", "x": 480, "y": 30, "width": 440, "height": 360}
    ],
    [
        {"id": "cloud-failing-app", "label": "Cloud Run App (Defective v2)", "product": "HTTP 500 Spike (Memory Leak)", "group": "g-cloud-rollback", "plane": "data", "x": 220, "y": 140, "detail": "New cloud microservice triggers memory leak under production concurrency."},
        {"id": "cloud-primary-db", "label": "Cloud SQL Primary", "product": "Writing Live Customer Data", "group": "g-cloud-rollback", "plane": "data", "x": 220, "y": 280, "detail": "Holds 45 minutes of new orders generated post-cutover."},
        {"id": "reverse-cdc", "label": "Reverse CDC Replication Pipeline", "product": "Streaming Changes Backwards", "group": "g-onprem-fallback", "plane": "control", "x": 700, "y": 140, "detail": "Streams new orders from Cloud SQL back to on-premise MySQL database."},
        {"id": "onprem-restored-db", "label": "On-Prem MySQL Primary", "product": "Restored Source Primary", "group": "g-onprem-fallback", "plane": "data", "x": 700, "y": 280, "detail": "Ready to resume live traffic without losing the 45 minutes of new orders."}
    ],
    [
        {"id": "e1", "from": "cloud-failing-app", "to": "cloud-primary-db", "label": "1. Write Cloud Orders", "plane": "data"},
        {"id": "e2", "from": "cloud-primary-db", "to": "reverse-cdc", "label": "2. Stream Reverse CDC Log", "plane": "control"},
        {"id": "e3", "from": "reverse-cdc", "to": "onprem-restored-db", "label": "3. Synchronize On-Premise DB", "plane": "data"}
    ],
    [
        {"n": 1, "title": "Reverse Synchronization Active", "edges": ["e1", "e2", "e3"], "action": "Reverse replication channel continuously syncs new cloud transactions back to on-prem.", "why_traversal": "Establishes a zero-data-loss safety net during the vulnerable post-cutover window.", "protocol": "Reverse CDC Stream", "plane": "Data Plane"},
        {"n": 2, "title": "Controlled Emergency Rollback", "edges": [], "action": "Cloud traffic halted; DNS reverted to on-prem; on-prem app resumes with complete data.", "why_traversal": "Restores production reliability in minutes without data corruption or loss.", "protocol": "DNS Failback", "plane": "Control Plane"}
    ],
    [
        {"id": "no-reverse-replication", "label": "Missing Reverse Replication Trap", "changes": {"failedNodes": ["reverse-cdc"], "failedEdges": ["e2"]}, "root_cause": "Team omitted reverse CDC pipeline to save setup time.", "diverted_path": "Rollback requires discarding 45 minutes of customer transactions or manual SQL patching.", "blast_radius": "Severe business disruption and manual reconciliation.", "recovery": "Mandate reverse replication pipelines as an architectural prerequisite for cutover approval."}
    ]
)

# 026: Decision Frameworks: ADRs & Matrices
new_specs[26] = make_spec(
    26, "3.4b", "Decision Frameworks: ADRs & Trade-offs",
    "Visualizes Architecture Decision Frameworks: systematic weighted scoring matrices, trade-off analysis (Cost vs Latency vs Operational Overhead), and formal Architecture Decision Records (ADRs).",
    "Architectural choices must never rely on intuition; multi-criteria decision analysis (MCDA) transparently weights trade-offs and binds engineering teams to documented rationales.",
    [
        {"id": "g-input-matrix", "label": "Decision Criteria & Weightings", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
        {"id": "g-candidate-tech", "label": "Candidate Architecture Evaluation", "type": "project", "scope": "project", "x": 300, "y": 30, "width": 310, "height": 360},
        {"id": "g-adr-output", "label": "Architecture Decision Record (ADR)", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
    ],
    [
        {"id": "criteria-weights", "label": "Weighted Evaluation Model", "product": "Cost 30% / SLA 40% / Ops 30%", "group": "g-input-matrix", "plane": "control", "x": 140, "y": 200, "detail": "Defines quantitative scoring rubric across total cost of ownership, SLA, and developer velocity."},
        {"id": "opt-gce", "label": "Option A: Compute Engine MIGs", "product": "High Ops / Low Unit Cost", "group": "g-candidate-tech", "plane": "control", "x": 440, "y": 100, "detail": "Score: 7.2/10. Requires manual OS patching, golden images, and custom auto-healing scripts."},
        {"id": "opt-gke", "label": "Option B: GKE Autopilot", "product": "Balanced Ops / High Scaling", "group": "g-candidate-tech", "plane": "control", "x": 440, "y": 200, "detail": "Score: 8.9/10. Managed Kubernetes control plane, per-pod billing, native horizontal pod autoscaling."},
        {"id": "opt-run", "label": "Option C: Cloud Run", "product": "Zero Ops / Scale-to-Zero", "group": "g-candidate-tech", "plane": "control", "x": 440, "y": 300, "detail": "Score: 9.4/10. Best fit for stateless HTTP APIs; fastest development velocity, zero idle server cost."},
        {"id": "adr-record", "label": "ADR-019: Cloud Run Selection", "product": "Signed Markdown in Git", "group": "g-adr-output", "plane": "control", "x": 780, "y": 200, "detail": "Documents Context, Decision, Consequences, and rejected alternatives for enterprise audit."}
    ],
    [
        {"id": "e1", "from": "criteria-weights", "to": "opt-gce", "label": "1. Score Compute Engine", "plane": "control"},
        {"id": "e2", "from": "criteria-weights", "to": "opt-gke", "label": "2. Score GKE Autopilot", "plane": "control"},
        {"id": "e3", "from": "criteria-weights", "to": "opt-run", "label": "3. Score Cloud Run", "plane": "control"},
        {"id": "e4", "from": "opt-run", "to": "adr-record", "label": "4. Crown Winner & Publish ADR", "plane": "control"}
    ],
    [
        {"n": 1, "title": "Scoring Matrix Evaluation", "edges": ["e1", "e2", "e3"], "action": "Candidates scored against standardized criteria (pricing, SLA, operational burden).", "why_traversal": "Grounds technology selection in objective data rather than vendor hype or developer bias.", "protocol": "Decision Matrix Algorithm", "plane": "Control Plane"},
        {"n": 2, "title": "ADR Publication", "edges": ["e4"], "action": "Winner recorded in Git repository under docs/adr/0019-compute-selection.md.", "why_traversal": "Creates permanent context for future engineers, preventing re-debating settled choices.", "protocol": "Git Version Control", "plane": "Control Plane"}
    ],
    [
        {"id": "criteria-bias", "label": "Hidden Operational Complexity Trap", "changes": {"failedNodes": ["opt-gce"], "failedEdges": ["e1"]}, "root_cause": "Team selected Compute Engine purely on low raw VM pricing, ignoring $15k/mo engineer maintenance overhead.", "diverted_path": "Operations team overwhelmed by kernel CVE patching and manual failovers.", "blast_radius": "Engineering roadmaps delayed by 3 months.", "recovery": "Incorporate total operational burden and fully burdened engineering hours into scoring rubric."}
    ],
    # D2
    "Traces the Compute Decision Tree Flow: evaluating workload constraints (statefulness, GPU, long-running processes, traffic burstiness) to arrive at the optimal GCP compute target.",
    "Decision trees guide engineers through branching criteria to systematically narrow down compute options from 6 candidates to 1 clear winner.",
    [
        {"id": "g-workload-attr", "label": "Workload Requirements Assessment", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
        {"id": "g-decision-branch", "label": "Branching Architecture Logic", "type": "project", "scope": "project", "x": 300, "y": 30, "width": 310, "height": 360},
        {"id": "g-selected-runtime", "label": "Optimal Google Cloud Runtime", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
    ],
    [
        {"id": "app-type-check", "label": "Containerized HTTP API?", "product": "Stateless & Request-Driven", "group": "g-workload-attr", "plane": "control", "x": 140, "y": 140, "detail": "Workload packaged in OCI container; responds to HTTPS requests within 60 minutes."},
        {"id": "run-check", "label": "Scale-to-Zero Required?", "product": "Zero Nighttime Traffic", "group": "g-workload-attr", "plane": "control", "x": 140, "y": 280, "detail": "Internal developer tool receives zero requests between 7 PM and 7 AM."},
        {"id": "eval-branch", "label": "Cloud Run Suitability Check", "product": "Meets 100% Constraints", "group": "g-decision-branch", "plane": "control", "x": 440, "y": 200, "detail": "No GPU needed, execution < 60 min, containerized -> Direct route to Cloud Run."},
        {"id": "target-runtime", "label": "Cloud Run Fully Managed", "product": "Pay-per-Request Runtime", "group": "g-selected-runtime", "plane": "data", "x": 780, "y": 200, "detail": "Deployed with concurrency=80, min-instances=0, max-instances=100."}
    ],
    [
        {"id": "e1", "from": "app-type-check", "to": "eval-branch", "label": "1. Yes: OCI Container", "plane": "control"},
        {"id": "e2", "from": "run-check", "to": "eval-branch", "label": "2. Yes: Burst / Idle Pattern", "plane": "control"},
        {"id": "e3", "from": "eval-branch", "to": "target-runtime", "label": "3. Provision Cloud Run Service", "plane": "data"}
    ],
    [
        {"n": 1, "title": "Constraint Verification", "edges": ["e1", "e2"], "action": "Decision tree evaluates container packaging and traffic distribution.", "why_traversal": "Rapidly filters out unsuitable runtimes like App Engine Standard or bare VMs.", "protocol": "Decision Tree Evaluation", "plane": "Control Plane"},
        {"n": 2, "title": "Automated Deployment", "edges": ["e3"], "action": "gcloud run deploy executes instantly based on decision tree recommendation.", "why_traversal": "Fast-tracks development while adhering to enterprise standards.", "protocol": "Cloud Run Admin API", "plane": "Data Plane"}
    ],
    [
        {"id": "timeout-breach", "label": "60-Minute Execution Timeout Exceeded", "changes": {"failedNodes": ["target-runtime"], "failedEdges": ["e3"]}, "root_cause": "Workload required 4-hour batch video encoding, exceeding Cloud Run's 60-minute limit.", "diverted_path": "Jobs killed mid-execution with HTTP 504.", "blast_radius": "Batch jobs fail silently.", "recovery": "Re-evaluate decision tree: route long-running batch jobs to Cloud Run Jobs or Cloud Batch."}
    ],
    # D3
    "Simulates Architecture Drift & Enforcement: detects rogue resource creation violating approved ADR-019 and enforces organizational policy guardrails.",
    "Policy Controller and Organization Policies act as runtime enforcers for architectural decisions, rejecting configurations that diverge from signed ADRs.",
    [
        {"id": "g-unauthorized-action", "label": "Unauthorized Deployment Attempt", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
        {"id": "g-guardrail-enforce", "label": "Org Policy & Policy Controller Guardrail", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
    ],
    [
        {"id": "rogue-vm-launch", "label": "Rogue GCE VM Creation", "product": "Unapproved e2-standard-16", "group": "g-unauthorized-action", "plane": "data", "x": 220, "y": 140, "detail": "Developer tries to deploy unmanaged VM contrary to ADR-019 serverless mandate."},
        {"id": "policy-validator", "label": "Policy Controller / Gatekeeper", "product": "Admission Webhook", "group": "g-guardrail-enforce", "plane": "control", "x": 700, "y": 140, "detail": "Intercepts API request; evaluates constraint template enforcing approved compute types."},
        {"id": "rejection-event", "label": "Admission Rejected (403)", "product": "Violates Constraint ADR-019", "group": "g-guardrail-enforce", "plane": "control", "x": 700, "y": 280, "detail": "Rejects resource creation with actionable feedback pointing developer to Cloud Run docs."}
    ],
    [
        {"id": "e1", "from": "rogue-vm-launch", "to": "policy-validator", "label": "1. Intercept Compute API Request", "plane": "control"},
        {"id": "e2", "from": "policy-validator", "to": "rejection-event", "label": "2. Block & Enforce Architectural Policy", "plane": "control"}
    ],
    [
        {"n": 1, "title": "API Interception", "edges": ["e1"], "action": "Cloud Resource Manager and Policy Controller intercept resource creation attempt.", "why_traversal": "Prevents unauthorized infrastructure from ever spinning up in production.", "protocol": "Admission Control Webhook", "plane": "Control Plane"},
        {"n": 2, "title": "Enforcement & Education", "edges": ["e2"], "action": "Request blocked with error: 'Compute Engine not permitted for HTTP microservices. Use Cloud Run per ADR-019'.", "why_traversal": "Educates developers and enforces architectural consistency across teams.", "protocol": "HTTP 403 Forbidden Response", "plane": "Control Plane"}
    ],
    [
        {"id": "bypass-guardrail", "label": "Policy Bypass via Personal Test Project", "changes": {"failedNodes": ["policy-validator"], "failedEdges": ["e2"]}, "root_cause": "Developer deployed rogue VM in sandbox folder missing organizational policy inheritance.", "diverted_path": "Unmonitored VM runs for 2 months accumulating $1,200/month unapproved charges.", "blast_radius": "Shadow IT cost leak.", "recovery": "Attach Org Policy constraints at root organization level so child folders cannot evade guardrails."}
    ]
)

# 027: Diagramming & Docs: C4 Model
new_specs[27] = make_spec(
    27, "3.5", "Diagramming & Docs: C4 Model",
    "Visualizes the C4 Architecture Diagramming Model applied to Google Cloud: Level 1 (System Context), Level 2 (Container), Level 3 (Component), and Level 4 (Code) with live cloud infrastructure mapping.",
    "The C4 model provides hierarchical zoom levels, ensuring business executives, systems architects, and software engineers understand the system at their required depth without visual clutter.",
    [
        {"id": "g-c1-context", "label": "C4 Level 1: System Context", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
        {"id": "g-c2-container", "label": "C4 Level 2: Cloud Container Architecture", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
        {"id": "g-c3-component", "label": "C4 Level 3: Microservice Components", "type": "project", "scope": "project", "x": 640, "y": 30, "width": 290, "height": 360}
    ],
    [
        {"id": "c1-actor", "label": "Online Retail Customer", "product": "Web & Mobile Endpoints", "group": "g-c1-context", "plane": "data", "x": 140, "y": 140, "detail": "Interacts with checkout and search systems over HTTPS."},
        {"id": "c1-banking-saas", "label": "Stripe Payment Gateway", "product": "External Banking SaaS", "group": "g-c1-context", "plane": "control", "x": 140, "y": 280, "detail": "Authorizes credit card transactions via external REST API."},
        {"id": "c2-gke-cluster", "label": "GKE Order Service Container", "product": "Order Microservice Pods", "group": "g-c2-container", "plane": "data", "x": 440, "y": 140, "detail": "Encapsulates order management and payment orchestration business logic."},
        {"id": "c2-spanner", "label": "Cloud Spanner Database", "product": "Orders Relational Storage", "group": "g-c2-container", "plane": "data", "x": 440, "y": 280, "detail": "Persists transactional order items and customer billing records."},
        {"id": "c3-auth-filter", "label": "JWT Authentication Filter", "product": "Go Middleware Component", "group": "g-c3-component", "plane": "control", "x": 780, "y": 140, "detail": "Validates OAuth2 bearer tokens against Google Cloud Identity / Firebase."},
        {"id": "c3-order-repo", "label": "Spanner Repository Layer", "product": "Go Data Access Object", "group": "g-c3-component", "plane": "data", "x": 780, "y": 280, "detail": "Encapsulates SQL queries and connection pooling to Cloud Spanner."}
    ],
    [
        {"id": "e1", "from": "c1-actor", "to": "c2-gke-cluster", "label": "1. Place Order (HTTPS)", "plane": "data"},
        {"id": "e2", "from": "c2-gke-cluster", "to": "c1-banking-saas", "label": "2. Charge Payment Card", "plane": "control"},
        {"id": "e3", "from": "c2-gke-cluster", "to": "c3-auth-filter", "label": "3. Validate Token Inside Pod", "plane": "control"},
        {"id": "e4", "from": "c3-auth-filter", "to": "c3-order-repo", "label": "4. Invoke Repository", "plane": "data"},
        {"id": "e5", "from": "c3-order-repo", "to": "c2-spanner", "label": "5. Commit SQL Transaction", "plane": "data"}
    ],
    [
        {"n": 1, "title": "Context to Container Traversal", "edges": ["e1", "e2"], "action": "Customer triggers order; GKE container invokes external SaaS payment gateway.", "why_traversal": "Shows high-level external boundaries (C1 Context).", "protocol": "HTTPS REST", "plane": "Data Plane"},
        {"n": 2, "title": "Container to Component Traversal", "edges": ["e3", "e4", "e5"], "action": "Inside the GKE pod, request traverses Auth Filter to Order Repository and writes to Spanner.", "why_traversal": "Reveals internal structural design without losing the bigger picture (C2 to C3).", "protocol": "In-Memory Go Function Calls", "plane": "Control Plane"}
    ],
    [
        {"id": "c4-drift-failure", "label": "Architecture Diagram Out of Sync", "changes": {"failedNodes": ["c3-order-repo"], "failedEdges": ["e4"]}, "root_cause": "Engineers added direct Redis cache bypass without updating C3 component diagram.", "diverted_path": "New developers debug stale flow assumption, wasting 2 days.", "blast_radius": "Engineering onboarding confusion.", "recovery": "Adopt Diagram-as-Code (Mermaid / Structurizr) embedded in Git repo with automated CI verification."}
    ],
    # D2
    "Traces the Diagram-as-Code CI/CD Pipeline: from markdown/Mermaid commit in Git through automated rendering to the Developer Portal.",
    "Treating diagrams as code versioned alongside Terraform configurations prevents architectural documentation from drifting out of sync with production.",
    [
        {"id": "g-dev-git", "label": "Git Version Control Repository", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
        {"id": "g-builder-ci", "label": "Cloud Build Documentation CI", "type": "project", "scope": "project", "x": 300, "y": 30, "width": 310, "height": 360},
        {"id": "g-portal-hosting", "label": "Internal Developer Portal (Backstage)", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
    ],
    [
        {"id": "git-commit", "label": "architecture.c4 Git Commit", "product": "Structurizr DSL / Mermaid", "group": "g-dev-git", "plane": "control", "x": 140, "y": 140, "detail": "Developer pushes updated C4 container topology alongside feature branch."},
        {"id": "ci-linter", "label": "C4 Model Syntax Linter", "product": "Automated Diagram Linter", "group": "g-builder-ci", "plane": "control", "x": 440, "y": 140, "detail": "Validates boundary tags, relationships, and ensures no orphan nodes exist."},
        {"id": "ci-renderer", "label": "Mermaid SVG Generator", "product": "Headless CLI Renderer", "group": "g-builder-ci", "plane": "control", "x": 440, "y": 280, "detail": "Compiles text DSL into responsive vector SVG diagrams and embeds into HTML docs."},
        {"id": "portal-bucket", "label": "Docs GCS Bucket", "product": "Cloud Storage Static Site", "group": "g-portal-hosting", "plane": "data", "x": 780, "y": 140, "detail": "Stores static documentation artifacts behind Cloud CDN."},
        {"id": "backstage-ui", "label": "Backstage Catalog Portal", "product": "Enterprise Service Catalog", "group": "g-portal-hosting", "plane": "data", "x": 780, "y": 280, "detail": "Displays interactive C4 diagrams with zoomable components for 500+ engineers."}
    ],
    [
        {"id": "e1", "from": "git-commit", "to": "ci-linter", "label": "1. Trigger Webhook on PR", "plane": "control"},
        {"id": "e2", "from": "ci-linter", "to": "ci-renderer", "label": "2. Pass Lint -> Generate SVGs", "plane": "control"},
        {"id": "e3", "from": "ci-renderer", "to": "portal-bucket", "label": "3. Upload Vector Assets to GCS", "plane": "data"},
        {"id": "e4", "from": "portal-bucket", "to": "backstage-ui", "label": "4. Render in Developer Portal", "plane": "data"}
    ],
    [
        {"n": 1, "title": "Validation & Compilation", "edges": ["e1", "e2"], "action": "Cloud Build runs linter on C4 DSL and renders vector SVGs.", "why_traversal": "Treats documentation with the same testing rigor as application code.", "protocol": "Cloud Build Pipeline", "plane": "Control Plane"},
        {"n": 2, "title": "Publication & Discovery", "edges": ["e3", "e4"], "action": "Artifacts published to GCS bucket; Backstage Developer Portal displays latest architecture.", "why_traversal": "Provides single source of architectural truth accessible to the entire organization.", "protocol": "Static Asset Ingestion", "plane": "Data Plane"}
    ],
    [
        {"id": "syntax-lint-failure", "label": "Invalid Diagram Syntax Blocks PR Merge", "changes": {"failedNodes": ["ci-linter"], "failedEdges": ["e2"]}, "root_cause": "Pull request contained broken Mermaid syntax with unclosed relationship arrow.", "diverted_path": "CI check fails; PR blocked from merging into main branch.", "blast_radius": "Prevents broken documentation from contaminating production portal.", "recovery": "Fix syntax error locally, test with mermaid-cli, and push revised commit."}
    ],
    # D3
    "Simulates Documentation vs Production Reality Drift: automated Drift Detector flags newly provisioned BigQuery dataset missing from C4 Level 2 Container diagram.",
    "Cloud Asset Inventory diffing automatically flags unmapped production infrastructure, triggering an automated GitHub Issue to keep diagrams accurate.",
    [
        {"id": "g-prod-state", "label": "Live Production Cloud Infrastructure", "type": "project", "scope": "global", "x": 30, "y": 30, "width": 420, "height": 360},
        {"id": "g-doc-validator", "label": "Architecture Doc Drift Detector", "type": "vpc", "scope": "regional", "x": 480, "y": 30, "width": 440, "height": 360}
    ],
    [
        {"id": "unmapped-bq", "label": "Unmapped BigQuery Dataset", "product": "Live GCP Dataset: 'analytics_raw'", "group": "g-prod-state", "plane": "data", "x": 220, "y": 140, "detail": "Data science team spun up production BigQuery dataset without updating architecture docs."},
        {"id": "cai-scanner", "label": "Cloud Asset Inventory Feed", "product": "Real-Time Resource Export", "group": "g-prod-state", "plane": "control", "x": 220, "y": 280, "detail": "Exports snapshot of all active GCP resources in the project."},
        {"id": "drift-comparator", "label": "C4 vs Live State Comparator", "product": "Cloud Function Analyzer", "group": "g-doc-validator", "plane": "control", "x": 700, "y": 140, "detail": "Compares active resources in Cloud Asset Inventory against nodes in architecture.c4."},
        {"id": "github-issue", "label": "Automated GitHub Drift Issue", "product": "Issue: 'Undocumented BigQuery Node'", "group": "g-doc-validator", "plane": "control", "x": 700, "y": 280, "detail": "Opens issue with git diff snippet showing proposed addition to C4 container diagram."}
    ],
    [
        {"id": "e1", "from": "unmapped-bq", "to": "cai-scanner", "label": "1. Ingest Resource Creation Event", "plane": "control"},
        {"id": "e2", "from": "cai-scanner", "to": "drift-comparator", "label": "2. Feed Live Asset State", "plane": "control"},
        {"id": "e3", "from": "drift-comparator", "to": "github-issue", "label": "3. File Documentation Drift Issue", "plane": "control"}
    ],
    [
        {"n": 1, "title": "Live Asset Discovery", "edges": ["e1", "e2"], "action": "Cloud Asset Inventory detects new BigQuery resource and passes state to analyzer.", "why_traversal": "Maintains continuous visibility over actual cloud inventory.", "protocol": "Cloud Asset API", "plane": "Control Plane"},
        {"n": 2, "title": "Drift Alerting", "edges": ["e3"], "action": "Analyzer detects discrepancy and files GitHub Issue with automated fix snippet.", "why_traversal": "Eliminates documentation obsolescence with zero manual tracking burden.", "protocol": "GitHub REST API", "plane": "Control Plane"}
    ],
    [
        {"id": "false-positive-storm", "label": "Transient Ephemeral Node Noise", "changes": {"failedNodes": ["drift-comparator"], "failedEdges": ["e3"]}, "root_cause": "Analyzer treated short-lived GKE batch pods as missing C4 architectural containers.", "diverted_path": "500 spam GitHub issues filed in 2 hours.", "blast_radius": "Engineering team mutes documentation alerts.", "recovery": "Add resource exclusion filter ignoring ephemeral pods and temporary staging buckets."}
    ]
)

# 029: SRE Concepts: SLIs, SLOs & Error Budgets
new_specs[29] = make_spec(
    29, "4.2", "SRE Concepts: SLIs, SLOs & Error Budgets",
    "Visualizes SRE Reliability Engineering: Service Level Indicators (SLIs), Service Level Objectives (SLOs), error budget consumption math, and automated release velocity gates.",
    "Error budgets turn reliability from an adversarial debate between Product and SRE into an objective, data-driven mathematical policy: feature velocity continues only while error budget remains.",
    [
        {"id": "g-sli-probes", "label": "Telemetry Probes & SLI Measurement", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 240, "height": 360},
        {"id": "g-slo-engine", "label": "SLO Engine & 30-Day Error Budget", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
        {"id": "g-release-gate", "label": "Release Velocity & Governance Gate", "type": "organization", "scope": "organization", "x": 640, "y": 30, "width": 290, "height": 360}
    ],
    [
        {"id": "probe-availability", "label": "Availability SLI Probe", "product": "HTTP 200 vs 5xx Ratio", "group": "g-sli-probes", "plane": "data", "x": 140, "y": 140, "detail": "Good requests (non-5xx) / Total requests measured at Load Balancer: 99.94% over 30d."},
        {"id": "probe-latency", "label": "Latency SLI Probe", "product": "p99 < 350ms Probe", "group": "g-sli-probes", "plane": "data", "x": 140, "y": 280, "detail": "Percentage of requests completing under 350ms: 98.7% over 30d rolling window."},
        {"id": "budget-meter", "label": "Error Budget Tracker", "product": "Remaining: 18.4% (30-day)", "group": "g-slo-engine", "plane": "control", "x": 440, "y": 200, "detail": "For 99.9% SLO, allows 43 minutes of downtime per month. 35 minutes already consumed."},
        {"id": "deploy-gatekeeper", "label": "Cloud Deploy Policy Gate", "product": "Automated Freeze Enforcer", "group": "g-release-gate", "plane": "control", "x": 780, "y": 140, "detail": "Queries error budget before production release; halts non-urgent deployments if budget < 0."},
        {"id": "sre-reliability-sprint", "label": "Reliability Sprint Mode", "product": "SRE Task Redirection", "group": "g-release-gate", "plane": "control", "x": 780, "y": 280, "detail": "Mandates that 100% of engineering bandwidth switches to bug fixes and resilience hardening."}
    ],
    [
        {"id": "e1", "from": "probe-availability", "to": "budget-meter", "label": "1. Ingest Availability SLI", "plane": "control"},
        {"id": "e2", "from": "probe-latency", "to": "budget-meter", "label": "2. Ingest Latency SLI", "plane": "control"},
        {"id": "e3", "from": "budget-meter", "to": "deploy-gatekeeper", "label": "3. Evaluate Release Permission", "plane": "control"},
        {"id": "e4", "from": "deploy-gatekeeper", "to": "sre-reliability-sprint", "label": "4. Trigger Freeze if Budget Exhausted", "plane": "control"}
    ],
    [
        {"n": 1, "title": "SLI Telemetry Aggregation", "edges": ["e1", "e2"], "action": "Cloud Monitoring MQL evaluates availability and latency ratios over 30-day rolling window.", "why_traversal": "Provides objective mathematical quantification of user happiness.", "protocol": "MQL Query Engine", "plane": "Control Plane"},
        {"n": 2, "title": "Budget Evaluation & Release Gating", "edges": ["e3", "e4"], "action": "If error budget drops to 0%, deployment pipeline automatically locks out feature releases.", "why_traversal": "Aligns developer incentives directly with system reliability.", "protocol": "Cloud Deploy Admission Webhook", "plane": "Control Plane"}
    ],
    [
        {"id": "budget-override-failure", "label": "Executive Override Deploys Fragile Feature", "changes": {"failedNodes": ["deploy-gatekeeper"], "failedEdges": ["e4"]}, "root_cause": "Executive manually overrode deployment freeze while error budget was exhausted at 0%.", "diverted_path": "Unstable feature release causes 5-hour global outage.", "blast_radius": "System availability drops to 98.2%; SLA financial penalty triggered.", "recovery": "Establish strict C-level governance requiring joint VP Engineering and SRE sign-off to override freeze."}
    ],
    # D2
    "Traces Multi-Window Multi-Burn-Rate Alerting: how SRE alerting detects both rapid catastrophic burn (14x burn rate) and slow chronic leakage (2x burn rate) without false alarms.",
    "Using dual time windows (1-hour short window + 6-hour long window) prevents alert fatigue from transient spikes while alerting on genuine budget exhaustion.",
    [
        {"id": "g-metric-stream", "label": "Real-Time Telemetry Feed", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 240, "height": 360},
        {"id": "g-burn-eval", "label": "Cloud Monitoring Burn Rate Evaluator", "type": "project", "scope": "project", "x": 300, "y": 30, "width": 310, "height": 360},
        {"id": "g-action-tier", "label": "SRE Incident Response Routing", "type": "organization", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
    ],
    [
        {"id": "traffic-stream", "label": "Live Production Traffic", "product": "15,000 QPS Telemetry", "group": "g-metric-stream", "plane": "data", "x": 140, "y": 140, "detail": "Emits HTTP status codes and response latencies to Cloud Monitoring."},
        {"id": "error-burst", "label": "500 Error Spike", "product": "5% Failure Rate Surge", "group": "g-metric-stream", "plane": "data", "x": 140, "y": 280, "detail": "Sudden surge in HTTP 500 errors burns error budget rapidly."},
        {"id": "short-window", "label": "Short Window (1h) 14x Burn", "product": "Consumes 2% Budget / Hour", "group": "g-burn-eval", "plane": "control", "x": 440, "y": 140, "detail": "Quickly detects urgent outages that would consume entire monthly budget in 50 hours."},
        {"id": "long-window", "label": "Long Window (6h) 14x Burn", "product": "Confirms Sustained Breach", "group": "g-burn-eval", "plane": "control", "x": 440, "y": 280, "detail": "Verifies degradation is persistent rather than a 30-second transient blip."},
        {"id": "pagerduty-critical", "label": "PagerDuty P1 Escalation", "product": "Immediate Page (SRE Primary)", "group": "g-action-tier", "plane": "control", "x": 780, "y": 200, "detail": "Fires high-urgency page to primary on-call SRE only when BOTH windows breach."}
    ],
    [
        {"id": "e1", "from": "traffic-stream", "to": "error-burst", "label": "1. Sudden Outage Influx", "plane": "data"},
        {"id": "e2", "from": "error-burst", "to": "short-window", "label": "2. Compute 1-Hour Burn Rate", "plane": "control"},
        {"id": "e3", "from": "error-burst", "to": "long-window", "label": "3. Compute 6-Hour Burn Rate", "plane": "control"},
        {"id": "e4", "from": "short-window", "to": "pagerduty-critical", "label": "4. Condition A: 1h Burn > 14x", "plane": "control"},
        {"id": "e5", "from": "long-window", "to": "pagerduty-critical", "label": "5. Condition B: 6h Burn > 14x -> Alert!", "plane": "control"}
    ],
    [
        {"n": 1, "title": "Dual Window Analysis", "edges": ["e1", "e2", "e3"], "action": "Cloud Monitoring MQL evaluates both short-window and long-window error rates simultaneously.", "why_traversal": "Requires sustained failure across both windows before waking engineers up at night.", "protocol": "MQL Alert Policy", "plane": "Control Plane"},
        {"n": 2, "title": "Targeted Incident Dispatch", "edges": ["e4", "e5"], "action": "Both conditions met; PagerDuty wakes on-call SRE with direct links to dashboard.", "why_traversal": "Eliminates alert fatigue and gives 99% confidence that incident is authentic.", "protocol": "PagerDuty Integration API", "plane": "Control Plane"}
    ],
    [
        {"id": "transient-spike-dampening", "label": "Transient Blip Suppressed", "changes": {"failedNodes": ["long-window"], "failedEdges": ["e5"]}, "root_cause": "A 45-second network glitch caused short-window alert to fire, but long-window remained below threshold.", "diverted_path": "No page sent; on-call engineer sleep protected.", "blast_radius": "Zero false pages.", "recovery": "Dual-window logic successfully absorbed transient blip as designed."}
    ],
    # D3
    "Simulates Error Budget Depletion leading to Automated Production Deployment Freeze: illustrates system protection during release instability.",
    "Automating the enforcement of deployment freezes removes political friction between engineering leads and ensures system stability takes precedence.",
    [
        {"id": "g-burn-source", "label": "Production Microservice Degradation", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
        {"id": "g-freeze-enforce", "label": "Automated Deployment Freeze Enforcer", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
    ],
    [
        {"id": "buggy-v3-release", "label": "Unstable v3 Payment Release", "product": "NullPointer Bug Under Load", "group": "g-burn-source", "plane": "data", "x": 220, "y": 140, "detail": "New microservice release burns 85% of monthly error budget in 12 hours."},
        {"id": "budget-monitor", "label": "Error Budget Sentinel", "product": "Budget Remaining: 0.0%", "group": "g-burn-source", "plane": "control", "x": 220, "y": 280, "detail": "Detects budget exhaustion; marks project as 'STABILITY_FREEZE_ACTIVE'."},
        {"id": "cloud-deploy-pipe", "label": "Cloud Deploy Release Pipeline", "product": "Release Target: Production", "group": "g-freeze-enforce", "plane": "control", "x": 700, "y": 140, "detail": "Attempts to promote v3.1 marketing feature to production."},
        {"id": "freeze-lockout", "label": "Automated Freeze Webhook", "product": "HTTP 423 Locked (Freeze Active)", "group": "g-freeze-enforce", "plane": "control", "x": 700, "y": 280, "detail": "Rejects deployment automatically; permits only emergency rollback or reliability patches."}
    ],
    [
        {"id": "e1", "from": "buggy-v3-release", "to": "budget-monitor", "label": "1. Rapid Budget Consumption", "plane": "control"},
        {"id": "e2", "from": "budget-monitor", "to": "freeze-lockout", "label": "2. Signal Budget Depleted", "plane": "control"},
        {"id": "e3", "from": "cloud-deploy-pipe", "to": "freeze-lockout", "label": "3. Attempt Feature Promotion", "plane": "control"}
    ],
    [
        {"n": 1, "title": "Budget Depletion Detection", "edges": ["e1", "e2"], "action": "Sentinel detects error budget has dropped to 0% and arms the deployment freeze webhook.", "why_traversal": "Enforces SRE agreement without requiring manual leadership intervention.", "protocol": "Eventarc Notification", "plane": "Control Plane"},
        {"n": 2, "title": "Automated Deployment Block", "edges": ["e3"], "action": "Cloud Deploy pipeline queries webhook, receives HTTP 423 Locked, and halts release.", "why_traversal": "Protects production users from further instability until reliability is restored.", "protocol": "Admission Control Webhook", "plane": "Control Plane"}
    ],
    [
        {"id": "freeze-bypass-attempt", "label": "Unauthorized Bypass Attempt", "changes": {"failedNodes": ["freeze-lockout"], "failedEdges": ["e3"]}, "root_cause": "Developer attempted to push code using personal service account with owner role.", "diverted_path": "Cloud Audit Logs flags IAM privilege misuse; SecOps notified.", "blast_radius": "Bypass blocked by immutable pipeline guardrail.", "recovery": "Remove broad IAM roles and enforce all production deployments through Cloud Deploy service account."}
    ]
)

# 030: High Availability by Layer
new_specs[30] = make_spec(
    30, "4.3", "High Availability by Layer",
    "Visualizes Defense-in-Depth High Availability across all 5 infrastructure layers: DNS Anycast, Multi-Region Interconnect, Regional Compute MIGs, Dual-Region Cloud Storage, and Multi-Region Cloud Spanner Paxos.",
    "System availability is only as strong as its weakest link; true high availability requires redundancy, automated failover, and isolation at every single layer of the stack.",
    [
        {"id": "g-dns-net", "label": "Layer 1 & 2: DNS & Network Layer", "type": "external", "scope": "global", "x": 30, "y": 30, "width": 240, "height": 360},
        {"id": "g-compute-migs", "label": "Layer 3: Regional Compute Fleet", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
        {"id": "g-storage-db", "label": "Layer 4 & 5: Storage & Database HA", "type": "project", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
    ],
    [
        {"id": "anycast-dns", "label": "Cloud DNS Anycast Routing", "product": "Global 100% SLA DNS", "group": "g-dns-net", "plane": "control", "x": 140, "y": 140, "detail": "Anycast BGP routes client to closest healthy edge PoP worldwide with 100% SLA."},
        {"id": "dual-interconnect", "label": "Dual Cloud Interconnects", "product": "99.99% Enterprise Interconnect", "group": "g-dns-net", "plane": "data", "x": 140, "y": 280, "detail": "Dual redundant 10Gbps links across two distinct metropolitan colocation facilities."},
        {"id": "regional-mig", "label": "Regional MIG (3 Zones)", "product": "Compute Engine MIG (a, b, c)", "group": "g-compute-migs", "plane": "data", "x": 440, "y": 200, "detail": "Spreads instances evenly across zones a, b, and c with auto-healing health checks."},
        {"id": "dual-gcs", "label": "Dual-Region Cloud Storage", "product": "Dual-Region (nam4) Bucket", "group": "g-storage-db", "plane": "data", "x": 780, "y": 140, "detail": "Replicates objects across us-central1 and us-east4 with turbo replication."},
        {"id": "multi-spanner", "label": "Cloud Spanner Multi-Region", "product": "99.999% SLA Relational DB", "group": "g-storage-db", "plane": "data", "x": 780, "y": 280, "detail": "Replicated across 3 regions with Paxos consensus, surviving full regional loss."}
    ],
    [
        {"id": "e1", "from": "anycast-dns", "to": "regional-mig", "label": "1. Anycast Route to Closest Region", "plane": "data"},
        {"id": "e2", "from": "dual-interconnect", "to": "regional-mig", "label": "2. Redundant Hybrid Ingress", "plane": "data"},
        {"id": "e3", "from": "regional-mig", "to": "dual-gcs", "label": "3. Access Replicated Storage", "plane": "data"},
        {"id": "e4", "from": "regional-mig", "to": "multi-spanner", "label": "4. Multi-Region Synchronous Writes", "plane": "data"}
    ],
    [
        {"n": 1, "title": "Ingress Redundancy", "edges": ["e1", "e2"], "action": "Anycast DNS and dual interconnects guarantee zero-downtime client packet ingress.", "why_traversal": "Eliminates single point of failure before traffic reaches cloud compute.", "protocol": "BGP Anycast / 802.1q", "plane": "Data Plane"},
        {"n": 2, "title": "Compute & Data Resiliency", "edges": ["e3", "e4"], "action": "Regional MIG distributes traffic across 3 zones; data persists across dual-region storage and Spanner.", "why_traversal": "Ensures entire physical datacenter loss results in zero data loss and zero downtime.", "protocol": "HTTPS / Spanner Paxos", "plane": "Data Plane"}
    ],
    [
        {"id": "single-zone-db-trap", "label": "Single-Zone Cloud SQL Bottleneck", "changes": {"failedNodes": ["regional-mig"], "failedEdges": ["e4"]}, "root_cause": "System used multi-zone compute but pointed to a single-zone non-HA database.", "diverted_path": "Zone outage takes down database; all compute pods crash due to database timeouts.", "blast_radius": "100% application outage despite multi-zone compute.", "recovery": "Upgrade database to Cloud SQL High Availability with automatic failover replica."}
    ],
    # D2
    "Traces Automatic Zonal Failover within a Regional Managed Instance Group: health check failure detection, instance draining, and traffic shifting to healthy zones.",
    "Regional Managed Instance Groups continuously monitor instance health via application HTTP endpoints, automatically evicting failing nodes without dropping connections.",
    [
        {"id": "g-ingress-lb", "label": "Regional Application Load Balancer", "type": "external", "scope": "regional", "x": 30, "y": 30, "width": 240, "height": 360},
        {"id": "g-zone-a", "label": "Zone A: Degraded Compute Zone", "type": "zone", "scope": "zonal", "x": 300, "y": 30, "width": 310, "height": 170},
        {"id": "g-zone-b", "label": "Zone B: Healthy Compute Zone", "type": "zone", "scope": "zonal", "x": 300, "y": 220, "width": 310, "height": 170},
        {"id": "g-auto-heal", "label": "MIG Auto-Healing Controller", "type": "project", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
    ],
    [
        {"id": "regional-alb", "label": "Regional Backend Service", "product": "Traffic Health Router", "group": "g-ingress-lb", "plane": "data", "x": 140, "y": 200, "detail": "Monitors backend health check status across all zones."},
        {"id": "vm-zone-a", "label": "VM Instance A1 (Failing)", "product": "Kernel Panic / Health 503", "group": "g-zone-a", "plane": "data", "x": 440, "y": 100, "detail": "Fails 3 consecutive /healthz checks; ALB stops dispatching new traffic."},
        {"id": "vm-zone-b", "label": "VM Instance B1 (Healthy)", "product": "Handling 100% of Requests", "group": "g-zone-b", "plane": "data", "x": 440, "y": 290, "detail": "Autoscaling triggers; adds VM B2 to handle additional load from Zone A."},
        {"id": "mig-controller", "label": "Compute Engine MIG Manager", "product": "Auto-Healing Orchestrator", "group": "g-auto-heal", "plane": "control", "x": 780, "y": 200, "detail": "Recreates unhealthy VM A1 in Zone A or Zone C automatically."}
    ],
    [
        {"id": "e1", "from": "regional-alb", "to": "vm-zone-a", "label": "1. Health Probe Fails (HTTP 503)", "plane": "control"},
        {"id": "e2", "from": "regional-alb", "to": "vm-zone-b", "label": "2. Shift 100% Traffic to Zone B", "plane": "data"},
        {"id": "e3", "from": "vm-zone-a", "to": "mig-controller", "label": "3. Signal Unhealthy Instance", "plane": "control"},
        {"id": "e4", "from": "mig-controller", "to": "vm-zone-b", "label": "4. Scale Up Capacity to Absorb Load", "plane": "control"}
    ],
    [
        {"n": 1, "title": "Health Check Failure Detection", "edges": ["e1"], "action": "Regional ALB detects 3 consecutive failed health checks on VM A1.", "why_traversal": "Prevents sending user traffic to dead or corrupted backend instances.", "protocol": "HTTP Health Check Probe", "plane": "Control Plane"},
        {"n": 2, "title": "Traffic Redirection & Healing", "edges": ["e2", "e3", "e4"], "action": "ALB shifts all traffic to Zone B; MIG controller destroys VM A1 and provisions fresh replacement.", "why_traversal": "Delivers zero-downtime auto-recovery without human intervention.", "protocol": "Compute Engine Control API", "plane": "Data Plane"}
    ],
    [
        {"id": "flapping-health-cascade", "label": "Flapping Health Check Cascade", "changes": {"failedNodes": ["vm-zone-b"], "failedEdges": ["e2"]}, "root_cause": "Health check timeout set too low (1s); shifting load to Zone B caused Zone B health checks to timeout.", "diverted_path": "ALB marks ALL zones unhealthy; returns HTTP 502 Bad Gateway to all users.", "blast_radius": "Complete cluster failure due to overly aggressive health check thresholds.", "recovery": "Tune health check thresholds: increase timeout to 5s and check interval to 10s with 3 failure thresholds."}
    ],
    # D3
    "Simulates Multi-Zone Power Outage: demonstrates cross-zone failover resilience and automated capacity rebalancing.",
    "Testing complete zone loss proves that regional topologies can sustain 33% physical capacity loss without degrading customer experience.",
    [
        {"id": "g-outage-zone", "label": "Zone us-central1-a (Total Power Loss)", "type": "zone", "scope": "zonal", "x": 30, "y": 30, "width": 420, "height": 360},
        {"id": "g-surviving-zones", "label": "Surviving Zones: us-central1-b & us-central1-c", "type": "region", "scope": "regional", "x": 480, "y": 30, "width": 440, "height": 360}
    ],
    [
        {"id": "zone-a-cluster", "label": "Zone A Instances (Dead)", "product": "Unresponsive Hardware", "group": "g-outage-zone", "plane": "data", "x": 220, "y": 200, "detail": "Physical substation transformer failure drops all servers in us-central1-a."},
        {"id": "zone-b-cluster", "label": "Zone B Instances (Healthy)", "product": "Operating at 75% Capacity", "group": "g-surviving-zones", "plane": "data", "x": 700, "y": 140, "detail": "Absorbs 50% of redirected traffic; autoscaler provisions additional nodes."},
        {"id": "zone-c-cluster", "label": "Zone C Instances (Healthy)", "product": "Operating at 75% Capacity", "group": "g-surviving-zones", "plane": "data", "x": 700, "y": 280, "detail": "Absorbs remaining 50% of redirected traffic with zero dropped transactions."}
    ],
    [
        {"id": "e1", "from": "zone-a-cluster", "to": "zone-b-cluster", "label": "1. Redirect 50% Ingress Traffic", "plane": "data"},
        {"id": "e2", "from": "zone-a-cluster", "to": "zone-c-cluster", "label": "2. Redirect 50% Ingress Traffic", "plane": "data"}
    ],
    [
        {"n": 1, "title": "Zonal Evacuation", "edges": ["e1", "e2"], "action": "Regional load balancer immediately routes all traffic away from dead Zone A into Zones B and C.", "why_traversal": "Regional architecture absorbs zonal catastrophes seamlessly.", "protocol": "Maglev Dynamic Flow Table", "plane": "Data Plane"}
    ],
    [
        {"id": "insufficient-headroom", "label": "Capacity Starvation in Surviving Zones", "changes": {"failedNodes": ["zone-b-cluster", "zone-c-cluster"], "failedEdges": ["e1", "e2"]}, "root_cause": "Cluster was running at 90% utilization before outage; surviving zones hit CPU saturation.", "diverted_path": "Latency spikes from 25ms to 4,200ms; requests queue and timeout.", "blast_radius": "Severe degradation across all users.", "recovery": "Maintain N+1 capacity headroom: never exceed 66% baseline CPU utilization in a 3-zone regional cluster."}
    ]
)

# 031: Disaster Recovery Patterns (RTO & RPO)
new_specs[31] = make_spec(
    31, "4.4", "Disaster Recovery Patterns (RTO & RPO)",
    "Visualizes the 4 Disaster Recovery Strategies (Backup & Restore, Pilot Light, Warm Standby, Hot Multi-Region Active-Active) mapped across Recovery Time Objective (RTO) and Recovery Point Objective (RPO) trade-offs.",
    "Selecting a Disaster Recovery strategy requires balancing the financial cost of idle standby infrastructure against the business revenue loss per hour of operational downtime.",
    [
        {"id": "g-primary-region", "label": "Primary Production Region (us-central1)", "type": "region", "scope": "regional", "x": 30, "y": 30, "width": 240, "height": 360},
        {"id": "g-replication-ch", "label": "Continuous Data Replication Channel", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
        {"id": "g-dr-standby-region", "label": "Disaster Recovery Region (us-east4)", "type": "region", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
    ],
    [
        {"id": "pri-app", "label": "Primary GKE Workloads", "product": "100% Active User Traffic", "group": "g-primary-region", "plane": "data", "x": 140, "y": 140, "detail": "Active regional cluster processing 10,000 orders/sec."},
        {"id": "pri-db", "label": "Cloud SQL Primary DB", "product": "Synchronous SSD Storage", "group": "g-primary-region", "plane": "data", "x": 140, "y": 280, "detail": "Primary transactional database writing WAL logs."},
        {"id": "dr-rep-channel", "label": "Cross-Region Read Replica", "product": "Async Cross-Region CDC", "group": "g-replication-ch", "plane": "control", "x": 440, "y": 280, "detail": "Replicates WAL changes across Google global backbone with RPO < 5 seconds."},
        {"id": "dr-standby-app", "label": "Warm Standby GKE Cluster", "product": "Minimal Baseline (2 Pods)", "group": "g-dr-standby-region", "plane": "data", "x": 780, "y": 140, "detail": "Keeps core pods pre-warmed; ready to autoscale to 100 pods within 3 minutes."},
        {"id": "dr-promoted-db", "label": "Promotable Secondary DB", "product": "RTO < 5m / RPO < 5s", "group": "g-dr-standby-region", "plane": "data", "x": 780, "y": 280, "detail": "Promoted to read-write primary upon regional failover activation."}
    ],
    [
        {"id": "e1", "from": "pri-app", "to": "pri-db", "label": "1. Write Transaction Data", "plane": "data"},
        {"id": "e2", "from": "pri-db", "to": "dr-rep-channel", "label": "2. Stream Cross-Region Replication", "plane": "control"},
        {"id": "e3", "from": "dr-rep-channel", "to": "dr-promoted-db", "label": "3. Replicate to Backup Region", "plane": "data"},
        {"id": "e4", "from": "dr-standby-app", "to": "dr-promoted-db", "label": "4. Re-bind Connection on Failover", "plane": "data"}
    ],
    [
        {"n": 1, "title": "Asynchronous Cross-Region Sync", "edges": ["e1", "e2", "e3"], "action": "Primary writes replicate across Google dedicated fiber backbone to us-east4.", "why_traversal": "Guarantees RPO < 5 seconds without penalizing primary write latency.", "protocol": "PostgreSQL Streaming Replication", "plane": "Data Plane"},
        {"n": 2, "title": "Warm Standby Ready State", "edges": ["e4"], "action": "Standby GKE cluster runs minimal baseline instances, ready for instant scale-up.", "why_traversal": "Reduces RTO to < 5 minutes while saving 70% compute costs compared to hot standby.", "protocol": "GKE Cluster Autoscaling", "plane": "Control Plane"}
    ],
    [
        {"id": "cold-backup-rto-trap", "label": "Cold Backup RTO Disaster", "changes": {"failedNodes": ["dr-standby-app"], "failedEdges": ["e4"]}, "root_cause": "Organization used Cold Backup strategy for 20TB database to save money.", "diverted_path": "Restoring 20TB database from GCS bucket took 28 hours during regional outage.", "blast_radius": "Business offline for over a full day; massive financial loss.", "recovery": "Upgrade mission-critical workloads from Cold Backup to Warm Standby or Spanner Multi-Region."}
    ],
    # D2
    "Traces the Automated Warm Standby Failover Workflow: regional health degradation detection, replica promotion, DNS traffic flip, and autoscaling.",
    "Automating the disaster recovery runbook via Cloud Functions and Cloud DNS routing policies eliminates human latency during high-stress regional outages.",
    [
        {"id": "g-failover-mon", "label": "Health Probing & Outage Sentinel", "type": "organization", "scope": "global", "x": 30, "y": 30, "width": 240, "height": 360},
        {"id": "g-failover-orch", "label": "Automated DR Orchestrator", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
        {"id": "g-backup-dest", "label": "Promoted DR Destination (us-east4)", "type": "region", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
    ],
    [
        {"id": "sentinel-probe", "label": "Global Uptime Check Probe", "product": "Multi-Region Prober", "group": "g-failover-mon", "plane": "control", "x": 140, "y": 200, "detail": "Probes primary region endpoint from 6 worldwide locations every 10 seconds."},
        {"id": "dr-orchestrator", "label": "Cloud Workflows DR Engine", "product": "Automated Failover Runbook", "group": "g-failover-orch", "plane": "control", "x": 440, "y": 200, "detail": "Coordinates database promotion, DNS TTL flip, and pod scaling sequentially."},
        {"id": "dns-failover-policy", "label": "Cloud DNS Failover Policy", "product": "Automated Health-Routed DNS", "group": "g-backup-dest", "plane": "control", "x": 780, "y": 140, "detail": "Automatically directs queries to us-east4 load balancer VIP upon health check failure."},
        {"id": "scaled-gke-pods", "label": "Autoscaled GKE Pods", "product": "Scaled 2 -> 60 Pods", "group": "g-backup-dest", "plane": "data", "x": 780, "y": 280, "detail": "Horizontal Pod Autoscaler brings up 60 pods within 90 seconds to handle production load."}
    ],
    [
        {"id": "e1", "from": "sentinel-probe", "to": "dr-orchestrator", "label": "1. Confirm Primary Outage (3 Failures)", "plane": "control"},
        {"id": "e2", "from": "dr-orchestrator", "to": "dns-failover-policy", "label": "2. Flip DNS to Backup Region", "plane": "control"},
        {"id": "e3", "from": "dr-orchestrator", "to": "scaled-gke-pods", "label": "3. Trigger Emergency Pod Scaling", "plane": "control"}
    ],
    [
        {"n": 1, "title": "Outage Confirmation", "edges": ["e1"], "action": "Uptime check confirms 100% loss of primary region across all probes.", "why_traversal": "Multi-region consensus prevents false failover from local network blips.", "protocol": "Cloud Monitoring Uptime Check", "plane": "Control Plane"},
        {"n": 2, "title": "Automated Runbook Execution", "edges": ["e2", "e3"], "action": "Workflows promotes secondary DB, instructs Cloud DNS to flip, and scales GKE pods.", "why_traversal": "Completes full regional failover in under 4 minutes with zero human intervention.", "protocol": "Cloud Workflows / REST APIs", "plane": "Control Plane"}
    ],
    [
        {"id": "dns-cache-poisoning", "label": "High TTL Stalls Failover Redirection", "changes": {"failedNodes": ["dns-failover-policy"], "failedEdges": ["e2"]}, "root_cause": "DNS TTL was configured to 86,400 seconds (24 hours) instead of 60 seconds.", "diverted_path": "Client ISP resolvers cached dead IP; failover took 24 hours to reach users.", "blast_radius": "Customers unable to connect despite backup region being fully operational.", "recovery": "Enforce maximum 60-second DNS TTLs on all disaster recovery failover routing policies."}
    ],
    # D3
    "Simulates Split-Brain DR Disaster Mode: illustrates Spanner Paxos consensus preventing two isolated regions from both accepting writes.",
    "Split-brain scenarios corrupt databases when partitioned regions both accept contradictory updates; Paxos quorum algorithms mathematically eliminate this hazard.",
    [
        {"id": "g-part-a", "label": "Partitioned Region A (us-central1)", "type": "region", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
        {"id": "g-part-b", "label": "Partitioned Region B (us-east4 + Witness)", "type": "region", "scope": "regional", "x": 480, "y": 30, "width": 440, "height": 360}
    ],
    [
        {"id": "spanner-a-iso", "label": "Spanner Node A (Minority: 1/3)", "product": "Isolated Replica", "group": "g-part-a", "plane": "data", "x": 220, "y": 200, "detail": "Cannot reach other nodes; cannot achieve 2/3 majority vote."},
        {"id": "spanner-b-maj", "label": "Spanner Node B (Majority: 2/3)", "product": "Active Paxos Quorum", "group": "g-part-b", "plane": "data", "x": 700, "y": 140, "detail": "Forms quorum with Witness region; continues safely committing customer transactions."},
        {"id": "witness-c", "label": "Witness Node (us-west1)", "product": "Quorum Voting Partner", "group": "g-part-b", "plane": "control", "x": 700, "y": 280, "detail": "Casts second vote required for majority quorum."}
    ],
    [
        {"id": "e1", "from": "spanner-a-iso", "to": "spanner-b-maj", "label": "1. WAN Partition Severed (Fiber Cut)", "plane": "control"},
        {"id": "e2", "from": "spanner-b-maj", "to": "witness-c", "label": "2. Form 2/3 Majority Quorum", "plane": "data"}
    ],
    [
        {"n": 1, "title": "Partition Isolation", "edges": ["e1"], "action": "Network cut separates Region A. Node A recognizes it is in a minority partition.", "why_traversal": "Node A voluntarily blocks writes, preventing split-brain corruption.", "protocol": "Paxos Heartbeat Loss", "plane": "Control Plane"},
        {"n": 2, "title": "Majority Quorum Continuation", "edges": ["e2"], "action": "Region B pairs with Witness to maintain 2/3 majority and safely accepts writes.", "why_traversal": "Provides zero RPO and continuous availability despite catastrophic network partitioning.", "protocol": "Paxos Quorum Consensus", "plane": "Data Plane"}
    ],
    [
        {"id": "two-node-quorum-trap", "label": "Two-Node Even Split Deadlock", "changes": {"failedNodes": ["witness-c"], "failedEdges": ["e2"]}, "root_cause": "System was deployed with only 2 nodes across 2 regions without an odd tie-breaker witness.", "diverted_path": "50/50 partition causes both nodes to freeze; entire global database halts.", "blast_radius": "Global system outage.", "recovery": "Always deploy an odd number of voting replicas (minimum 3 or 5) across distinct fault domains."}
    ]
)

# 033: Testing for Reliability: Load & Chaos
new_specs[33] = make_spec(
    33, "4.6", "Testing for Reliability: Load & Chaos",
    "Visualizes Chaos Engineering and Automated Reliability Testing: distributed load generators, Chaos Mesh pod/network fault injectors, automated blast-radius containment, and SLO watchdog abort triggers.",
    "Reliability cannot be proven theoretically; it must be continuously validated in production under controlled synthetic failures with automated blast-radius circuit breakers.",
    [
        {"id": "g-load-chaos-src", "label": "Synthetic Load & Chaos Injector Fleet", "type": "project", "scope": "regional", "x": 30, "y": 30, "width": 240, "height": 360},
        {"id": "g-target-gke", "label": "Target Production GKE Cluster", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
        {"id": "g-blast-watchdog", "label": "Blast Radius Watchdog & Kill Switch", "type": "organization", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
    ],
    [
        {"id": "locust-load", "label": "Distributed Locust Fleet", "product": "Synthetic 25,000 QPS Load", "group": "g-load-chaos-src", "plane": "data", "x": 140, "y": 140, "detail": "Generates realistic customer shopping cart transaction patterns at peak volume."},
        {"id": "chaos-controller", "label": "Chaos Mesh Controller", "product": "Kubernetes CRD Injector", "group": "g-load-chaos-src", "plane": "control", "x": 140, "y": 280, "detail": "Injects synthetic 400ms network latency and terminates random payment pods."},
        {"id": "gke-app-pods", "label": "Payment Microservice Pods", "product": "Target GKE Autopilot Pods", "group": "g-target-gke", "plane": "data", "x": 440, "y": 140, "detail": "Tested pods: verifies circuit breaker and retry with exponential backoff handling."},
        {"id": "downstream-db", "label": "Cloud SQL Database", "product": "Production Transaction DB", "group": "g-target-gke", "plane": "data", "x": 440, "y": 280, "detail": "Monitored to ensure connection pools are not saturated by chaotic retries."},
        {"id": "slo-watchdog", "label": "SLO Error Budget Watchdog", "product": "Burn Rate Circuit Breaker", "group": "g-blast-watchdog", "plane": "control", "x": 780, "y": 200, "detail": "Continuously evaluates error budget; triggers emergency chaos abort if > 0.5% budget burned."}
    ],
    [
        {"id": "e1", "from": "locust-load", "to": "gke-app-pods", "label": "1. Inject 25,000 QPS Synthetic Traffic", "plane": "data"},
        {"id": "e2", "from": "chaos-controller", "to": "gke-app-pods", "label": "2. Inject 400ms Latency & Kill Pods", "plane": "control"},
        {"id": "e3", "from": "gke-app-pods", "to": "downstream-db", "label": "3. Handle Retries with Exponential Backoff", "plane": "data"},
        {"id": "e4", "from": "gke-app-pods", "to": "slo-watchdog", "label": "4. Stream Telemetry to Budget Watchdog", "plane": "control"}
    ],
    [
        {"n": 1, "title": "Synthetic Stress & Fault Injection", "edges": ["e1", "e2"], "action": "Locust hammers API with peak traffic while Chaos Mesh terminates random pods.", "why_traversal": "Validates system resilience under combined peak load and hardware failure.", "protocol": "Locust HTTP + Chaos CRD", "plane": "Data Plane"},
        {"n": 2, "title": "Circuit Breaker & Watchdog Guardrail", "edges": ["e3", "e4"], "action": "Pods absorb latency via retries; watchdog monitors error budget to prevent customer impact.", "why_traversal": "Proves auto-healing capability while guaranteeing blast radius is strictly contained.", "protocol": "MQL Real-Time Metric Stream", "plane": "Control Plane"}
    ],
    [
        {"id": "retry-storm-meltdown", "label": "Retry Storm Cascading Outage", "changes": {"failedNodes": ["downstream-db"], "failedEdges": ["e3"]}, "root_cause": "Developers configured retries with immediate retry (no exponential backoff or jitter).", "diverted_path": "50,000 retries hit database in 1 second, crashing Cloud SQL connection pool.", "blast_radius": "Production database failure impacting all customers.", "recovery": "Enforce circuit breaker pattern (Resilience4j / Envoy) and exponential backoff with full jitter."}
    ],
    # D2
    "Traces the Step-by-Step Chaos Experiment Lifecycle: hypothesis verification, baseline measurement, fault injection, resilience observation, and automated cleanup.",
    "A structured chaos experiment must always establish a steady-state hypothesis before introducing chaos to mathematically verify that the system self-heals.",
    [
        {"id": "g-exp-phase1", "label": "Phase 1: Steady-State Baseline", "type": "project", "scope": "regional", "x": 30, "y": 30, "width": 240, "height": 360},
        {"id": "g-exp-phase2", "label": "Phase 2: Chaos Injection & Blast Guard", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
        {"id": "g-exp-phase3", "label": "Phase 3: Automated Verification & Cleanup", "type": "organization", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
    ],
    [
        {"id": "baseline-check", "label": "Verify Steady State", "product": "p99 < 200ms / Error Rate 0.01%", "group": "g-exp-phase1", "plane": "control", "x": 140, "y": 200, "detail": "Validates that production SLO is healthy before beginning chaos experiment."},
        {"id": "inject-network-delay", "label": "Inject 300ms Delay", "product": "Chaos Mesh NetworkChaos", "group": "g-exp-phase2", "plane": "control", "x": 440, "y": 140, "detail": "Emulates cross-region WAN degradation between app service and inventory service."},
        {"id": "circuit-breaker-trip", "label": "Envoy Circuit Breaker", "product": "Trips after 5 Consecutive Delays", "group": "g-exp-phase2", "plane": "data", "x": 440, "y": 280, "detail": "Shunts traffic to fallback cached inventory response in 2ms."},
        {"id": "automated-cleanup", "label": "Experiment Complete & Cleaned", "product": "Delete Chaos CRD", "group": "g-exp-phase3", "plane": "control", "x": 780, "y": 200, "detail": "Removes chaos injection; verifies system recovers to steady-state within 30 seconds."}
    ],
    [
        {"id": "e1", "from": "baseline-check", "to": "inject-network-delay", "label": "1. Confirm Steady State -> Inject Chaos", "plane": "control"},
        {"id": "e2", "from": "inject-network-delay", "to": "circuit-breaker-trip", "label": "2. Induce Latency -> Trip Circuit Breaker", "plane": "data"},
        {"id": "e3", "from": "circuit-breaker-trip", "to": "automated-cleanup", "label": "3. Verify Fallback -> Clean Up Injection", "plane": "control"}
    ],
    [
        {"n": 1, "title": "Hypothesis Confirmation", "edges": ["e1"], "action": "Validates steady-state; injects 300ms network delay into inventory service.", "why_traversal": "Ensures experiment tests a specific resilience hypothesis.", "protocol": "Kubernetes CRD Application", "plane": "Control Plane"},
        {"n": 2, "title": "Circuit Breaker Shunting", "edges": ["e2"], "action": "Envoy proxy trips circuit breaker and returns cached catalog data.", "why_traversal": "Confirms user experience is shielded from downstream latency.", "protocol": "Envoy Filter Protocol", "plane": "Data Plane"},
        {"n": 3, "title": "Cleanup & Verification", "edges": ["e3"], "action": "Chaos controller deletes fault CRD; telemetry confirms p99 returns to < 200ms.", "why_traversal": "Leaves zero lingering synthetic defects in production.", "protocol": "Kubernetes API Cleanup", "plane": "Control Plane"}
    ],
    [
        {"id": "linger-chaos-failure", "label": "Zombie Chaos CRD Lingers in Production", "changes": {"failedNodes": ["automated-cleanup"], "failedEdges": ["e3"]}, "root_cause": "CI runner crashed mid-experiment, leaving NetworkChaos CRD running indefinitely.", "diverted_path": "Production service permanently degraded by 300ms.", "blast_radius": "Customers experience sluggish checkout for 8 hours.", "recovery": "Add automated TTL expiration directly in Chaos Mesh CRD spec so faults self-terminate."}
    ],
    # D3
    "Simulates Chaos Blast-Radius Breach & Automated Emergency Kill-Switch: error budget burn threshold triggers immediate chaos termination.",
    "Chaos experiments must incorporate hard automated kill switches to guarantee that synthetic testing never causes an uncontrolled real production outage.",
    [
        {"id": "g-chaos-active", "label": "Active Chaos Fault Injection", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
        {"id": "g-kill-switch-ctrl", "label": "Automated Chaos Kill-Switch Controller", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
    ],
    [
        {"id": "active-pod-killer", "label": "Aggressive Pod Killer CRD", "product": "Killing 50% of Pods Simultaneously", "group": "g-chaos-active", "plane": "control", "x": 220, "y": 140, "detail": "Experiment erroneously configured to terminate 50% of production checkout pods."},
        {"id": "live-user-impact", "label": "HTTP 503 Outage Spike", "product": "Error Rate Surges to 8.5%", "group": "g-chaos-active", "plane": "data", "x": 220, "y": 280, "detail": "Checkout transactions failing for real paying customers."},
        {"id": "budget-kill-trigger", "label": "Error Budget Sentinel", "product": "Burn Rate > 20x (Emergency)", "group": "g-kill-switch-ctrl", "plane": "control", "x": 700, "y": 140, "detail": "Detects 0.5% monthly error budget burned in 2 minutes; triggers kill switch."},
        {"id": "emergency-terminator", "label": "Emergency Chaos Kill-Switch", "product": "kubectl delete chaos --all", "group": "g-kill-switch-ctrl", "plane": "control", "x": 700, "y": 280, "detail": "Immediately aborts all chaos experiments and restores normal pod routing within 4 seconds."}
    ],
    [
        {"id": "e1", "from": "active-pod-killer", "to": "live-user-impact", "label": "1. Unintended Production Blast", "plane": "data"},
        {"id": "e2", "from": "live-user-impact", "to": "budget-kill-trigger", "label": "2. Detect Error Budget Threshold Breach", "plane": "control"},
        {"id": "e3", "from": "budget-kill-trigger", "to": "emergency-terminator", "label": "3. Fire Emergency Abort Command", "plane": "control"}
    ],
    [
        {"n": 1, "title": "Blast Radius Breach Detection", "edges": ["e1", "e2"], "action": "Watchdog detects error rate exceeding 1% threshold during chaos execution.", "why_traversal": "Guarantees chaos testing never compromises business SLAs.", "protocol": "Real-time Telemetry Breach", "plane": "Control Plane"},
        {"n": 2, "title": "Immediate Emergency Abort", "edges": ["e3"], "action": "Kill-switch executes cluster API call deleting all active Chaos CRDs in < 4 seconds.", "why_traversal": "Restores production stability before customers notice significant disruption.", "protocol": "Kubernetes Admission Webhook Abort", "plane": "Control Plane"}
    ],
    [
        {"id": "stuck-kill-switch", "label": "RBAC Denies Kill-Switch Execution", "changes": {"failedNodes": ["emergency-terminator"], "failedEdges": ["e3"]}, "root_cause": "Kill-switch service account lacked cluster-admin permission to delete Chaos CRDs.", "diverted_path": "Chaos continues running; checkout remains down for 35 minutes.", "blast_radius": "Major high-severity production incident.", "recovery": "Pre-verify kill-switch permissions with automated pre-flight testing before every experiment."}
    ]
)

print(f"Generated new specs for topics: {sorted(list(new_specs.keys()))}")
# Merge existing and new
all_p3_p4 = {}
all_p3_p4.update(existing_specs)
all_p3_p4.update(new_specs)
print(f"Total topics in Phase 3 & 4: {sorted(list(all_p3_p4.keys()))}")

# Write to spec_p3_p4.py
spec_p3_p4_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spec_p3_p4.py")

with open(spec_p3_p4_path, "w") as f:
    f.write('"""\n')
    f.write('spec_p3_p4.py - Topics 022 to 033\n')
    f.write('Phase 3: Design Process & Architecture Framework\n')
    f.write('Phase 4: Reliability & SRE\n')
    f.write('"""\n\n')
    f.write('def get_specs():\n')
    f.write('    specs = {}\n\n')
    f.write('    def make_spec(t_no, r_id, title,\n')
    f.write('                  d1_p, d1_r, d1_g, d1_n, d1_e, d1_s, d1_sc,\n')
    f.write('                  d2_p, d2_r, d2_g, d2_n, d2_e, d2_s, d2_sc,\n')
    f.write('                  d3_p, d3_r, d3_g, d3_n, d3_e, d3_s, d3_sc):\n')
    f.write('        return {\n')
    f.write('            "topic_no": f"{t_no:03d}",\n')
    f.write('            "roadmap_id": r_id,\n')
    f.write('            "title": title,\n')
    f.write('            "d1_purpose": d1_p, "d1_rationale": d1_r, "d1_groups": d1_g, "d1_nodes": d1_n, "d1_edges": d1_e, "d1_steps": d1_s, "d1_scenarios": d1_sc,\n')
    f.write('            "d2_purpose": d2_p, "d2_rationale": d2_r, "d2_groups": d2_g, "d2_nodes": d2_n, "d2_edges": d2_e, "d2_steps": d2_s, "d2_scenarios": d2_sc,\n')
    f.write('            "d3_purpose": d3_p, "d3_rationale": d3_r, "d3_groups": d3_g, "d3_nodes": d3_n, "d3_edges": d3_e, "d3_steps": d3_s, "d3_scenarios": d3_sc,\n')
    f.write('        }\n\n')

    for t_no in sorted(all_p3_p4.keys()):
        s = all_p3_p4[t_no]
        f.write(f'    specs[{t_no}] = make_spec(\n')
        f.write(f'        {t_no}, {json.dumps(s["roadmap_id"])}, {json.dumps(s["title"])},\n')
        f.write(f'        {json.dumps(s["d1_purpose"])},\n')
        f.write(f'        {json.dumps(s["d1_rationale"])},\n')
        f.write(f'        {json.dumps(s["d1_groups"])},\n')
        f.write(f'        {json.dumps(s["d1_nodes"])},\n')
        f.write(f'        {json.dumps(s["d1_edges"])},\n')
        f.write(f'        {json.dumps(s["d1_steps"])},\n')
        f.write(f'        {json.dumps(s["d1_scenarios"])},\n')
        f.write(f'        {json.dumps(s["d2_purpose"])},\n')
        f.write(f'        {json.dumps(s["d2_rationale"])},\n')
        f.write(f'        {json.dumps(s["d2_groups"])},\n')
        f.write(f'        {json.dumps(s["d2_nodes"])},\n')
        f.write(f'        {json.dumps(s["d2_edges"])},\n')
        f.write(f'        {json.dumps(s["d2_steps"])},\n')
        f.write(f'        {json.dumps(s["d2_scenarios"])},\n')
        f.write(f'        {json.dumps(s["d3_purpose"])},\n')
        f.write(f'        {json.dumps(s["d3_rationale"])},\n')
        f.write(f'        {json.dumps(s["d3_groups"])},\n')
        f.write(f'        {json.dumps(s["d3_nodes"])},\n')
        f.write(f'        {json.dumps(s["d3_edges"])},\n')
        f.write(f'        {json.dumps(s["d3_steps"])},\n')
        f.write(f'        {json.dumps(s["d3_scenarios"])}\n')
        f.write('    )\n\n')

    f.write('    return specs\n')

print("Successfully written to spec_p3_p4.py!")
