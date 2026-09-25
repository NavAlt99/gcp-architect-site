#!/usr/bin/env python3
"""
update_homepage.py - Updates index.html with all 60 generated topic cards, filters, and search.
"""

import os
import glob
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

TOPIC_INFO = [
    # Phase 0
    ("001", "0.1", "Networking Fundamentals", "concept", "Phase 0 — Prerequisites", "OSI & TCP/IP layers, RFC 1918 subnets, CIDR calculation, DNS, TCP/TLS handshakes, and stateful firewalls."),
    ("002", "0.2", "Linux & Command Line for Architects", "concept", "Phase 0 — Prerequisites", "systemd service supervision, journalctl inspection, IAP SSH bastion tunneling, and jq CLI parsing."),
    ("003", "0.3", "Virtualization and Containers", "concept", "Phase 0 — Prerequisites", "Hardware vs OS virtualization, cgroups & namespaces, multi-stage Distroless builds, and Pod lifecycle."),
    ("004", "0.4", "Cloud Concepts & Operating Models", "concept", "Phase 0 — Prerequisites", "IaaS/PaaS/FaaS service boundaries, Shared Responsibility security matrix, and stateless vs stateful patterns."),
    ("005", "0.5", "Software Architecture & Delivery Basics", "concept", "Phase 0 — Prerequisites", "12-factor cloud-native app design, REST vs gRPC, and Strangler Fig microservice modernization."),
    ("006", "0.6", "Cloud Digital Leader & Business Foundations", "concept", "Phase 0 — Prerequisites", "CapEx vs OpEx cloud economics, Total Cost of Ownership (TCO) modeling, and Google Cloud Adoption Framework."),
    
    # Phase 1
    ("007", "1.1", "Account, Tools and Access", "service", "Phase 1 — GCP Foundations", "Cloud Console, Cloud Shell persistent home directories, gcloud named configurations, and API enablement."),
    ("008", "1.2", "Resource Hierarchy & Org Policies", "service", "Phase 1 — GCP Foundations", "Organization node, folders, project lifecycle, additive IAM inheritance, and Organization Policy constraints."),
    ("009", "1.3", "Identity Basics: IAM & Service Accounts", "service", "Phase 1 — GCP Foundations", "Google Groups, least-privilege predefined roles, service account impersonation, and Workload Identity."),
    ("010", "1.4", "Billing, Cost Hygiene, and FinOps", "service", "Phase 1 — GCP Foundations", "Billing accounts, automated Pub/Sub budget notifications, BigQuery cost export, and rate vs allocation quotas."),
    ("011", "1.5", "Global Infrastructure & Network Tiers", "service", "Phase 1 — GCP Foundations", "Regions, availability zones, Jupiter fiber fabric, and Premium vs Standard Network Service Tiers."),
    ("012", "1.6", "Support, Governance & Asset Inventory", "concept", "Phase 1 — GCP Foundations", "Customer Care support plans, Cloud Asset Inventory real-time analysis, Service Health, and Preview vs GA SLAs."),
    
    # Phase 2
    ("013", "2.1", "Compute Engine: VMs & Managed Instance Groups", "service", "Phase 2 — Core Services", "General-purpose E2/N2/C3 machine families, Persistent Disks, Regional MIGs, Autohealing, and Spot VMs."),
    ("014", "2.2", "Google Kubernetes Engine (GKE)", "service", "Phase 2 — Core Services", "GKE Autopilot vs Standard, VPC-native clusters, Standalone NEGs, Dataplane V2, and Workload Identity."),
    ("015", "2.3", "Serverless Compute: Cloud Run & Functions", "service", "Phase 2 — Core Services", "Cloud Run services vs jobs, concurrency tuning, Direct VPC Egress, Eventarc triggers, and scale-to-zero."),
    ("016", "2.4", "Virtual Private Cloud (VPC) Networking", "service", "Phase 2 — Core Services", "Global VPC architecture, custom subnets, routes, hierarchical firewall policies, and Shared VPC."),
    ("017", "2.5", "Cloud Load Balancing, CDN & Cloud Armor", "service", "Phase 2 — Core Services", "Global External ALB Anycast proxy, L4 Passthrough, Cloud CDN edge caching, and Cloud Armor WAF rules."),
    ("018", "2.6", "Hybrid & Multi-Cloud Connectivity", "service", "Phase 2 — Core Services", "Cloud HA VPN 99.99% dual tunnels, Dedicated vs Partner Interconnect, and Cloud Router BGP dynamic routing."),
    ("019", "2.7", "Cloud Storage & Enterprise Filesystems", "service", "Phase 2 — Core Services", "Standard, Nearline, Coldline, Archive storage classes, Autoclass, Uniform Bucket Access, and Bucket Lock."),
    ("020", "2.8", "Databases: Cloud SQL, Spanner & Bigtable", "service", "Phase 2 — Core Services", "Cloud SQL Regional HA, Cloud Spanner 99.999% global external consistency, Firestore, and Bigtable NoSQL."),
    ("021", "2.9", "Messaging & Integration: Pub/Sub & Tasks", "service", "Phase 2 — Core Services", "Cloud Pub/Sub at-least-once streaming, dead-letter topics, message ordering, and Cloud Tasks rate limiting."),

    # Phase 3
    ("022", "3.1", "Requirements Analysis: Business & Technical Discovery", "concept", "Phase 3 — Architecture Thinking", "Converting stakeholder goals into quantifiable SLAs, latency budgets, MoSCoW prioritization, and stakeholder maps."),
    ("023", "3.2", "Google Cloud Architecture Framework", "concept", "Phase 3 — Architecture Thinking", "The six pillars: Operational Excellence, Security, Reliability, Cost, Performance, and System Design."),
    ("024", "3.3", "Reference Architectures & Enterprise Patterns", "concept", "Phase 3 — Architecture Thinking", "Three-tier web apps, reactive microservices, multi-region active-active vs active-passive, and enterprise landing zones."),
    ("025", "3.4", "Migration & Modernization: The 6 Rs", "concept", "Phase 3 — Architecture Thinking", "The 6 Rs (Rehost, Replatform, Refactor, Repurchase, Retire, Retain), Migration Center, and Strangler Fig cutover."),
    ("026", "3.4b", "Decision-Making Frameworks: ADRs & Matrices", "concept", "Phase 3 — Architecture Thinking", "Build vs Buy vs Managed, weighted decision scorecards, Architecture Decision Records (ADRs), and TCO modeling."),
    ("027", "3.5", "Diagramming & Documentation: C4 Model", "concept", "Phase 3 — Architecture Thinking", "Visual communication: The C4 Model (Context, Container, Component, Code), network flows, and Diagrams as Code."),

    # Phase 4
    ("028", "4.1", "Reliability Fundamentals & Availability Math", "concept", "Phase 4 — Reliability & HA", "Downtime calculations (99.9% vs 99.99%), series vs parallel composite SLAs, failure domains, and circuit breakers."),
    ("029", "4.2", "SRE Concepts: SLIs, SLOs & Error Budgets", "concept", "Phase 4 — Reliability & HA", "Quantifying reliability: SLIs, SLOs, error budget burn rates, the Four Golden Signals, and blameless post-mortems."),
    ("030", "4.3", "High Availability by Layer", "service", "Phase 4 — Reliability & HA", "Multi-layer redundancy: Regional MIGs, GKE multi-zone node pools, HA VPN dual tunnels, and Spanner multi-region Paxos."),
    ("031", "4.4", "Disaster Recovery Patterns (RTO & RPO)", "concept", "Phase 4 — Reliability & HA", "RTO vs RPO trade-offs: Backup & Restore, Pilot Light, Warm Standby, and Hot Standby (Active-Active)."),
    ("032", "4.5", "Observability: Monitoring, Logging & Trace", "service", "Phase 4 — Reliability & HA", "Cloud Monitoring dashboards, centralized log sinks, BigQuery Log Analytics, distributed Cloud Trace, and Ops Agent."),
    ("033", "4.6", "Testing for Reliability: Load & Chaos", "concept", "Phase 4 — Reliability & HA", "Distributed load testing with k6/Locust, chaos engineering fault injection, canary analysis, and Game Day simulations."),

    # Phase 5
    ("034", "5.1", "Advanced IAM, Federation & Zero Trust", "service", "Phase 5 — Security & Compliance", "IAM Conditions, Deny policies, Workload Identity Federation (keyless GitHub/AWS), PAM, and BeyondCorp IAP."),
    ("035", "5.2", "Network Security: VPC-SC & Cloud Armor", "service", "Phase 5 — Security & Compliance", "VPC Service Controls perimeters, Cloud Armor WAF (OWASP Top 10) & DDoS defense, and Private Service Connect."),
    ("036", "5.3", "Data Protection: Cloud KMS & Cloud DLP", "service", "Phase 5 — Security & Compliance", "Customer-Managed Encryption Keys (CMEK), Cloud HSM, Sensitive Data Protection (DLP), and Confidential Computing."),
    ("037", "5.4", "Compliance, Governance & Assured Workloads", "concept", "Phase 5 — Security & Compliance", "Shared Responsibility Model, SOC/PCI/HIPAA/GDPR compliance, Assured Workloads, and Policy as Code guardrails."),
    ("038", "5.5", "Security Operations & Threat Detection", "service", "Phase 5 — Security & Compliance", "Security Command Center (SCC) Premium/Enterprise, Event Threat Detection, Container Threat Detection, and SecOps SOAR."),
    ("039", "5.5b", "Application & Supply-Chain Security (SLSA)", "concept", "Phase 5 — Security & Compliance", "Artifact Analysis vulnerability scanning, Binary Authorization attestations, SLSA levels, and Distroless containers."),

    # Phase 6
    ("040", "6.1", "Cost Optimization & FinOps", "concept", "Phase 6 — Optimization & Ops", "Inform/Optimize/Operate, BigQuery billing export, Committed Use Discounts (CUDs), Spot VMs, and egress optimization."),
    ("041", "6.2", "Performance Optimization & Bottlenecks", "concept", "Phase 6 — Optimization & Ops", "CPU/RAM/IOPS/Network bottlenecks, multi-tier caching (CDN, Memorystore), query plans, and connection pooling."),
    ("042", "6.3", "Infrastructure as Code: Terraform & GitOps", "service", "Phase 6 — Optimization & Ops", "Terraform modules, remote state in GCS with locking, Cloud Foundation Toolkit, and Config Connector."),
    ("043", "6.4", "CI/CD & Release Engineering: Cloud Deploy", "service", "Phase 6 — Optimization & Ops", "Cloud Build serverless triggers, Artifact Registry provenance, Cloud Deploy automated canaries, and DORA 4 metrics."),
    ("044", "6.5", "Operations & Platform Engineering", "concept", "Phase 6 — Optimization & Ops", "Platform engineering operating model, golden paths, runbook automation, and periodic Well-Architected reviews."),

    # Phase 7
    ("045", "7.1", "Case Analysis Method & Discovery Framework", "concept", "Phase 7 — Case Studies & Exam", "The 6-step consulting playbook: Goals, Constraints, Technical Reqs, Watchpoints, Architecture, and Rejected Options."),
    ("046", "7.4a", "Case Study: EHR Healthcare", "case-study", "Phase 7 — Case Studies & Exam", "Modernizing legacy on-premises healthcare records with strict HIPAA compliance, Apigee gateway, and Cloud SQL HA."),
    ("047", "7.4b", "Case Study: Mountkirk Games", "case-study", "Phase 7 — Case Studies & Exam", "Global mobile multiplayer gaming backend: Cloud Spanner 99.999% consistency, GKE Autopilot, and real-time BigQuery."),
    ("048", "7.4c", "Case Study: TerramEarth", "case-study", "Phase 7 — Case Studies & Exam", "IoT telemetry from 20M agricultural vehicles: Cellular vs Wi-Fi dual ingest, Cloud Bigtable time-series, and Vertex AI."),
    ("049", "7.4d", "Case Study: Helicopter Racing League", "case-study", "Phase 7 — Case Studies & Exam", "Global low-latency live video streaming: Transcoder API, Cloud CDN edge caching, and real-time Vertex AI predictions."),
    ("050", "7.5", "PCA Exam Strategy & Keyword Elimination", "concept", "Phase 7 — Case Studies & Exam", "The elimination method, trigger keyword decoders ('minimum ops', 'zero data loss'), and exam day time management."),

    # Cross-Cutting Data & ML
    ("051", "D.1", "Data Warehousing: BigQuery & Looker", "service", "Data, Analytics & ML", "Separation of compute (Dremel) and storage (Capacitor), table partitioning and clustering, BI Engine, and Looker Studio."),
    ("052", "D.2", "Data Processing: Dataflow & Dataproc", "service", "Data, Analytics & ML", "Unified streaming/batch on Apache Beam, managed Spark/Hadoop on Dataproc, and Cloud Composer Airflow orchestration."),
    ("053", "D.3", "Data Lake, Lakehouse & BigLake", "service", "Data, Analytics & ML", "Tiered storage zones (raw, curated, consumption), open formats (Parquet, Iceberg), BigLake, and Dataplex governance."),
    ("054", "D.4", "Machine Learning: Vertex AI Architecture", "service", "Data, Analytics & ML", "AI hierarchy (APIs, AutoML, Custom), Vertex AI Pipelines, Feature Store, Model Registry, and GPU vs TPU hardware."),

    # Service Decision Cheat Sheets
    ("055", "CS.1", "Compute Decision Cheat Sheet", "cheat-sheet", "Service Decision Cheat Sheets", "Compute Engine vs GKE Autopilot vs Cloud Run vs Cloud Functions vs Cloud Batch decision matrix."),
    ("056", "CS.2", "Database Decision Cheat Sheet", "cheat-sheet", "Service Decision Cheat Sheets", "Cloud SQL vs AlloyDB vs Cloud Spanner vs Firestore vs Cloud Bigtable vs Memorystore decision matrix."),
    ("057", "CS.3", "Load Balancer Decision Cheat Sheet", "cheat-sheet", "Service Decision Cheat Sheets", "Global External ALB vs Regional External ALB vs Internal ALB vs Proxy vs Passthrough Network LB."),
    ("058", "CS.4", "Hybrid Connectivity Decision Cheat Sheet", "cheat-sheet", "Service Decision Cheat Sheets", "Cloud HA VPN (99.99%) vs Dedicated Interconnect vs Partner Interconnect vs Cross-Cloud Interconnect."),
    ("059", "CS.5", "Storage & Messaging Decision Cheat Sheet", "cheat-sheet", "Service Decision Cheat Sheets", "Cloud Storage classes (Standard, Nearline, Coldline, Archive); Pub/Sub vs Cloud Tasks vs Eventarc queues."),
    ("060", "CS.6", "Key Numbers, Limits & SLAs to Memorise", "cheat-sheet", "Service Decision Cheat Sheets", "Availability math table (99.9% vs 99.99%), storage retention minimums, network throughput limits, and official SLAs.")
]

cards_html = ""
for item in TOPIC_INFO:
    topic_no, roadmap_id, title, page_type, phase, desc = item
    type_badge = "Service" if page_type == "service" else ("Case Study" if page_type == "case-study" else ("Cheat Sheet" if page_type == "cheat-sheet" else "Concept"))
    type_class = "badge-type" if page_type in ["service", "case-study"] else "badge"
    
    # Phase color mapping
    if "Phase 0" in phase:
        phase_color = "#f97316"; phase_bg = "rgba(249, 115, 22, 0.12)"
    elif "Phase 1" in phase:
        phase_color = "#38bdf8"; phase_bg = "rgba(56, 189, 248, 0.12)"
    elif "Phase 2" in phase:
        phase_color = "#ec4899"; phase_bg = "rgba(236, 72, 153, 0.12)"
    elif "Phase 3" in phase:
        phase_color = "#a855f7"; phase_bg = "rgba(168, 85, 247, 0.12)"
    elif "Phase 4" in phase:
        phase_color = "#10b981"; phase_bg = "rgba(16, 185, 129, 0.12)"
    elif "Phase 5" in phase:
        phase_color = "#ef4444"; phase_bg = "rgba(239, 68, 68, 0.12)"
    elif "Phase 6" in phase:
        phase_color = "#eab308"; phase_bg = "rgba(234, 179, 8, 0.12)"
    elif "Phase 7" in phase:
        phase_color = "#06b6d4"; phase_bg = "rgba(6, 182, 212, 0.12)"
    elif "Data" in phase:
        phase_color = "#8b5cf6"; phase_bg = "rgba(139, 92, 246, 0.12)"
    else: # Cheat sheets
        phase_color = "#f43f5e"; phase_bg = "rgba(244, 63, 94, 0.12)"
    
    cards_html += f"""
      <div class="topic-card" style="border: 1px solid var(--panel-border); border-radius: 10px; background: #0b0f1d; padding: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; margin-bottom: 14px;">
        <div style="flex: 1; min-width: 280px;">
          <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 8px; flex-wrap: wrap;">
            <span class="badge" style="background:var(--accent); color:#090d16; font-weight:700;">Topic {topic_no}</span>
            <span class="badge badge-type">{roadmap_id}</span>
            <span class="badge" style="background:{phase_bg}; color:{phase_color}; border-color:{phase_color};">{phase}</span>
            <span class="{type_class}">{type_badge}</span>
          </div>
          <h3 style="margin: 4px 0 8px 0; font-size: 15px;">
            <a href="pages/topic-{topic_no}.html" style="color:#fff; text-decoration:none;">{title}</a>
          </h3>
          <p style="margin: 0; color: var(--text-dim); font-size: 12px; max-width: 720px; line-height: 1.5;">
            {desc}
          </p>
          <div style="margin-top: 10px; display: flex; gap: 12px; font-size: 11px; color: var(--text-dim);">
            <span>Diagrams: <strong style="color:#38bdf8;">D1, D2, D3</strong></span> • 
            <span>Analogy: <strong style="color:#ec4899;">Cloud City Scene</strong></span> • 
            <span>Evaluation: <strong style="color:#f97316;">PCA Knowledge Check</strong></span>
          </div>
        </div>
        <div>
          <a href="pages/topic-{topic_no}.html" class="btn-de active" style="text-decoration:none; padding: 8px 16px; white-space:nowrap;">
            Open Topic Page →
          </a>
        </div>
      </div>
"""

full_index = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>GCP Architect Roadmap — Architecture Explorer (60 Topics)</title>
  <link rel="stylesheet" href="assets/site.css">
</head>
<body>

  <!-- App Header -->
  <header class="site-nav">
    <div class="nav-container">
      <a href="index.html" class="brand-link">
        <span style="font-size:16px;">☁</span>
        <span class="brand-text">GCP ARCHITECT ROADMAP</span>
      </a>
      <nav class="nav-links">
        <a href="#paths" class="nav-link">Learning Paths</a>
        <a href="#topics" class="nav-link">All 60 Topics</a>
        <a href="pages/topic-001.html" class="btn-de active" style="text-decoration:none;">Start Topic 001 →</a>
      </nav>
    </div>
  </header>

  <main class="main-content">
    
    <!-- Hero Heading -->
    <header class="page-header" style="text-align: center; padding: 40px 10px 30px;">
      <span class="badge" style="margin-bottom: 14px;">Version 3.0 • Complete 60-Topic System Architecture</span>
      <h1 class="page-title">Google Cloud Architect Roadmap</h1>
      <p class="page-lead" style="max-width: 780px; margin: 0 auto;">
        From foundational systems mechanics to Professional Cloud Architect (PCA) certification and staff-level consulting judgement. Minimalist ByteMonk dark aesthetic, animated packet flows, failure injection, and zero raster dependencies.
      </p>
      <div style="margin-top: 18px; display: flex; justify-content: center; gap: 16px; flex-wrap: wrap; font-size: 12px; color: var(--text-dim);">
        <span>📦 <strong>60</strong> Comprehensive Topics</span> • 
        <span>📊 <strong>180</strong> Interactive SVG Diagrams</span> • 
        <span>🏙 <strong>60</strong> Cloud City Metaphors</span> • 
        <span>🛡 <strong>100%</strong> Offline & Static</span>
      </div>
    </header>

    <!-- Learning Path Selection -->
    <section class="topic-section" id="paths">
      <h2 class="section-title">Curated Learning Paths</h2>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px;">
        <div class="panel-card" style="border-top: 3px solid #f97316;">
          <h4 style="margin-top:0; color:#f97316;">🌱 Phase 0: Prerequisites</h4>
          <p style="font-size: 12px; color: var(--text-dim); margin-bottom:14px;">
            Networking, Linux POSIX primitives, containers, cloud operating models, and 12-factor architecture.
          </p>
          <a href="pages/topic-001.html" class="btn-de" style="text-decoration:none;">Topics 001 – 006 →</a>
        </div>
        <div class="panel-card" style="border-top: 3px solid #38bdf8;">
          <h4 style="margin-top:0; color:#38bdf8;">🏛 Phase 1: GCP Foundations</h4>
          <p style="font-size: 12px; color: var(--text-dim); margin-bottom:14px;">
            Resource hierarchy, Cloud Identity, least-privilege IAM, service accounts, and FinOps budgeting.
          </p>
          <a href="pages/topic-007.html" class="btn-de" style="text-decoration:none;">Topics 007 – 012 →</a>
        </div>
        <div class="panel-card" style="border-top: 3px solid #ec4899;">
          <h4 style="margin-top:0; color:#ec4899;">⚡ Phase 2: Core Services</h4>
          <p style="font-size: 12px; color: var(--text-dim); margin-bottom:14px;">
            Compute Engine, GKE Autopilot, Serverless Cloud Run, VPC networking, Load Balancing, and Databases.
          </p>
          <a href="pages/topic-013.html" class="btn-de" style="text-decoration:none;">Topics 013 – 021 →</a>
        </div>
        <div class="panel-card" style="border-top: 3px solid #a855f7;">
          <h4 style="margin-top:0; color:#a855f7;">🧠 Phase 3: Architecture Thinking</h4>
          <p style="font-size: 12px; color: var(--text-dim); margin-bottom:14px;">
            Requirements discovery, Architecture Framework 6 pillars, 6 Rs migration, ADRs, and C4 diagramming.
          </p>
          <a href="pages/topic-022.html" class="btn-de" style="text-decoration:none;">Topics 022 – 027 →</a>
        </div>
        <div class="panel-card" style="border-top: 3px solid #10b981;">
          <h4 style="margin-top:0; color:#10b981;">🛡 Phase 4: Reliability & HA</h4>
          <p style="font-size: 12px; color: var(--text-dim); margin-bottom:14px;">
            Availability math (series vs parallel), SRE error budgets, multi-layer HA, Disaster Recovery, and Observability.
          </p>
          <a href="pages/topic-028.html" class="btn-de" style="text-decoration:none;">Topics 028 – 033 →</a>
        </div>
        <div class="panel-card" style="border-top: 3px solid #ef4444;">
          <h4 style="margin-top:0; color:#ef4444;">🔒 Phase 5: Security & Compliance</h4>
          <p style="font-size: 12px; color: var(--text-dim); margin-bottom:14px;">
            Workload Identity, VPC Service Controls, Cloud Armor, Cloud KMS CMEK, SCC threat detection, and SLSA.
          </p>
          <a href="pages/topic-034.html" class="btn-de" style="text-decoration:none;">Topics 034 – 039 →</a>
        </div>
        <div class="panel-card" style="border-top: 3px solid #eab308;">
          <h4 style="margin-top:0; color:#eab308;">⚙️ Phase 6: Optimization & Ops</h4>
          <p style="font-size: 12px; color: var(--text-dim); margin-bottom:14px;">
            FinOps CUD commitments, bottleneck analysis, Terraform IaC, Cloud Deploy canaries, and Platform Engineering.
          </p>
          <a href="pages/topic-040.html" class="btn-de" style="text-decoration:none;">Topics 040 – 044 →</a>
        </div>
        <div class="panel-card" style="border-top: 3px solid #06b6d4;">
          <h4 style="margin-top:0; color:#06b6d4;">🎓 Phase 7: Case Studies & Exam</h4>
          <p style="font-size: 12px; color: var(--text-dim); margin-bottom:14px;">
            6-step case method, EHR Healthcare, Mountkirk Games, TerramEarth, HRL, and PCA trigger keyword elimination.
          </p>
          <a href="pages/topic-045.html" class="btn-de" style="text-decoration:none;">Topics 045 – 050 →</a>
        </div>
        <div class="panel-card" style="border-top: 3px solid #8b5cf6;">
          <h4 style="margin-top:0; color:#8b5cf6;">📊 Cross-Cutting: Data & AI</h4>
          <p style="font-size: 12px; color: var(--text-dim); margin-bottom:14px;">
            BigQuery Dremel/Capacitor, Dataflow Beam streaming, Dataproc, BigLake Lakehouses, and Vertex AI MLOps.
          </p>
          <a href="pages/topic-051.html" class="btn-de" style="text-decoration:none;">Topics 051 – 054 →</a>
        </div>
        <div class="panel-card" style="border-top: 3px solid #f43f5e;">
          <h4 style="margin-top:0; color:#f43f5e;">📑 Service Decision Cheat Sheets</h4>
          <p style="font-size: 12px; color: var(--text-dim); margin-bottom:14px;">
            Instant revision matrices: Compute, Database, Load Balancer, Hybrid, Storage, and Key PCA Numbers.
          </p>
          <a href="pages/topic-055.html" class="btn-de" style="text-decoration:none;">Topics 055 – 060 →</a>
        </div>
      </div>
    </section>

    <!-- Topics Grid -->
    <section class="topic-section" id="topics">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 12px;">
        <div>
          <h2 class="section-title" style="margin: 0; border: none; padding: 0;">Roadmap Topic Inventory ({len(TOPIC_INFO)} Topics Built)</h2>
          <p style="margin: 4px 0 0 0; font-size: 12px; color: var(--text-dim);">Search across all concepts, services, case studies, and decision matrices.</p>
        </div>
        <input type="text" id="topic-search" oninput="filterTopics()" placeholder="Search topics, services, or keywords..." style="padding: 8px 14px; border: 1px solid var(--panel-border); border-radius: 6px; font-size: 12px; font-family:var(--font-mono); background:#080d1a; color:#fff; width: 320px;">
      </div>

      <div id="topic-cards-container">
        {cards_html}
      </div>
    </section>

  </main>

  <footer style="text-align: center; padding: 28px; color: var(--text-dim); font-size: 11px; border-top: 1px solid var(--panel-border);">
    Google Cloud Architect Roadmap • Minimalist Systems Design • 100% Static & Offline Compatible
  </footer>

  <script>
    function filterTopics() {{
      const query = document.getElementById('topic-search').value.toLowerCase();
      document.querySelectorAll('.topic-card').forEach(card => {{
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(query) ? 'flex' : 'none';
      }});
    }}
  </script>

</body>
</html>
"""

with open(INDEX_PATH, 'w') as f:
    f.write(full_index)

print(f"Successfully updated index.html with all {len(TOPIC_INFO)} topics.")
