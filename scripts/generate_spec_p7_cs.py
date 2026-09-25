#!/usr/bin/env python3
"""
generate_spec_p7_cs.py - Generates spec_p7_cs.py with authentic specifications for:
Phase 7: Case Studies (045 to 050)
Data & ML Specialty Deep-Dives (051 to 054)
Exam Cheat Sheets (055 to 060)
"""

import os
import json

def build_p7_cs_specs():
    specs = {}

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

    # 045: Case Analysis Method & Discovery Framework
    specs[45] = make_spec(
        45, "7.1", "Case Analysis Method & Discovery",
        "Visualizes the Systematic Case Study Discovery Framework: extracting business drivers, non-functional requirements, technical constraints, and mapping them directly to Google Cloud target architectures.",
        "PCA case study analysis requires decoupling subjective narrative from objective architectural constraints: identify compliance, latency, cost, and availability requirements first before selecting GCP services.",
        [
            {"id": "g-case-narrative", "label": "Enterprise Narrative & Business Goals", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-matrix-analysis", "label": "Architectural Synthesis & Sizing Matrix", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-target-blueprint", "label": "Google Cloud Target Reference Blueprint", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "biz-driver", "label": "Business Driver: Global Expansion", "product": "Sub-100ms Worldwide Latency", "group": "g-case-narrative", "plane": "control", "x": 140, "y": 140, "detail": "Company expanding from US to Europe and Asia; demands 99.99% availability."},
            {"id": "compliance-req", "label": "Regulatory Constraint: HIPAA/GDPR", "product": "Strict Data Residency & CMEK", "group": "g-case-narrative", "plane": "control", "x": 140, "y": 280, "detail": "Patient and customer data must remain encrypted at rest and in transit with audit logs."},
            {"id": "sizing-synthesizer", "label": "Constraint Matrix Evaluator", "product": "Maps SLAs to Cloud Services", "group": "g-matrix-analysis", "plane": "control", "x": 440, "y": 200, "detail": "Evaluates candidate architectures; rejects single-region solutions due to global latency."},
            {"id": "cloud-target-arch", "label": "Target Cloud Architecture", "product": "GKE + Multi-Region Spanner", "group": "g-target-blueprint", "plane": "data", "x": 780, "y": 140, "detail": "Global Anycast External ALB + Regional GKE + Cloud Spanner Multi-Region."},
            {"id": "finops-validation", "label": "FinOps Cost Model Sign-off", "product": "TCO Analysis & CUD Alignment", "group": "g-target-blueprint", "plane": "control", "x": 780, "y": 280, "detail": "Confirms solution meets budget ceiling using 3-year Flexible Spend CUDs."}
        ],
        [
            {"id": "e1", "from": "biz-driver", "to": "sizing-synthesizer", "label": "1. Extract Latency & SLA Goals", "plane": "control"},
            {"id": "e2", "from": "compliance-req", "to": "sizing-synthesizer", "label": "2. Extract Security & Sovereignty Rules", "plane": "control"},
            {"id": "e3", "from": "sizing-synthesizer", "to": "cloud-target-arch", "label": "3. Synthesize Target Architecture", "plane": "control"},
            {"id": "e4", "from": "cloud-target-arch", "to": "finops-validation", "label": "4. Verify Financial Viability", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Constraint Extraction", "edges": ["e1", "e2"], "action": "Architect deconstructs case study text into numeric SLAs, latency targets, and compliance rules.", "why_traversal": "Prevents subjective architectural bias by anchoring on quantitative requirements.", "protocol": "Architecture Discovery Matrix", "plane": "Control Plane"},
            {"n": 2, "title": "Architecture Blueprint Synthesis", "edges": ["e3", "e4"], "action": "Matches requirements to GCP multi-region topology and confirms financial sustainability.", "why_traversal": "Produces exam-winning designs that satisfy both technical and commercial criteria.", "protocol": "Solution Blueprinting", "plane": "Data Plane"}
        ],
        [
            {"id": "over-engineering-penalty", "label": "Over-Engineering Distractor Trap", "changes": {"failedNodes": ["cloud-target-arch"], "failedEdges": ["e3"]}, "root_cause": "Architect proposed complex real-time Apache Beam pipeline when requirements only asked for daily batch reports.", "diverted_path": "Operational overhead and cost exceed project scope by 400%.", "blast_radius": "Architecture fails exam review scoring.", "recovery": "Adhere strictly to minimal operational complexity: use BigQuery scheduled queries for batch reporting."}
        ],
        # D2
        "Traces Case Study Technical Translation: converting business requirements into explicit GCP component choices via decision rubric.",
        "Systematic decision rubrics eliminate guesswork when matching high-level business goals to specific Google Cloud services.",
        [
            {"id": "g-bus-req", "label": "Business Goal Statement", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-rubric-logic", "label": "Architectural Translation Rubric", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-gcp-service", "label": "Selected Google Cloud Service", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "req-statement", "label": "'Zero downtime global SQL database'", "product": "Customer Requirement", "group": "g-bus-req", "plane": "control", "x": 140, "y": 200, "detail": "Must maintain strong ACID consistency across North America and Europe."},
            {"id": "rule-acid", "label": "Constraint: ACID + Global SQL", "product": "Relational + Horizontal Scaling", "group": "g-rubric-logic", "plane": "control", "x": 440, "y": 140, "detail": "Filters out NoSQL (Firestore/Bigtable) and single-region relational (Cloud SQL)."},
            {"id": "rule-sla", "label": "Constraint: 99.999% SLA", "product": "Max 5 min downtime/year", "group": "g-rubric-logic", "plane": "control", "x": 440, "y": 280, "detail": "Requires synchronous multi-region Paxos consensus."},
            {"id": "selected-spanner", "label": "Cloud Spanner Multi-Region", "product": "Optimal GCP Service Match", "group": "g-gcp-service", "plane": "data", "x": 780, "y": 200, "detail": "Globally distributed relational database delivering 99.999% SLA with external consistency."}
        ],
        [
            {"id": "e1", "from": "req-statement", "to": "rule-acid", "label": "1. Evaluate SQL / ACID Need", "plane": "control"},
            {"id": "e2", "from": "req-statement", "to": "rule-sla", "label": "2. Evaluate SLA & Global Reach", "plane": "control"},
            {"id": "e3", "from": "rule-acid", "to": "selected-spanner", "label": "3. Eliminate Incompatible Options", "plane": "control"},
            {"id": "e4", "from": "rule-sla", "to": "selected-spanner", "label": "4. Select Cloud Spanner", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Constraint Filtering", "edges": ["e1", "e2"], "action": "Applies technical constraints: relational SQL + multi-region consistency.", "why_traversal": "Eliminates Cloud SQL (single-region limit) and Bigtable (NoSQL).", "protocol": "Decision Filter", "plane": "Control Plane"},
            {"n": 2, "title": "Product Confirmation", "edges": ["e3", "e4"], "action": "Cloud Spanner identified as the only GCP service meeting all criteria.", "why_traversal": "Guarantees mathematically sound service selection.", "protocol": "Service Selection Rubric", "plane": "Data Plane"}
        ],
        [
            {"id": "wrong-service-selection", "label": "Selected Cloud SQL for Multi-Region Active-Active", "changes": {"failedNodes": ["selected-spanner"], "failedEdges": ["e4"]}, "root_cause": "Architect selected Cloud SQL with cross-region read replica, failing write availability in secondary region.", "diverted_path": "Secondary region cannot accept writes during regional failover.", "blast_radius": "Architectural failure during disaster.", "recovery": "Select Cloud Spanner Multi-Region when write availability is required across multiple regions."}
        ],
        # D3
        "Simulates Compliance & Cost Trade-off Conflict: demonstrates resolving tension between extreme availability targets and strict budgetary caps.",
        "Real-world architecture requires negotiating trade-offs: when business availability goals exceed budget reality, architects present quantitative tiered options.",
        [
            {"id": "g-conflict-src", "label": "Requirements Incompatibility Conflict", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-tradeoff-solver", "label": "Architectural Trade-Off Resolution Engine", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "req-5nines", "label": "Demanded 99.999% SLA", "product": "Five-Nines Multi-Region", "group": "g-conflict-src", "plane": "control", "x": 220, "y": 140, "detail": "Stakeholder demands zero downtime under all circumstances across 3 continents."},
            {"id": "budget-cap-strict", "label": "Strict $1,500/Month Budget", "product": "Budget Ceiling", "group": "g-conflict-src", "plane": "control", "x": 220, "y": 280, "detail": "Budget ceiling is mathematically insufficient for multi-region Spanner + Interconnects."},
            {"id": "tradeoff-matrix", "label": "Tiered Trade-Off Matrix", "product": "Option A vs Option B Analysis", "group": "g-tradeoff-solver", "plane": "control", "x": 700, "y": 140, "detail": "Presents Tier 1 (99.9% Regional Cloud SQL @ $800/mo) vs Tier 2 (99.999% Spanner @ $4,500/mo)."},
            {"id": "agreed-compromise", "label": "Approved Realistic Design", "product": "Tier 1: 99.9% Regional HA Approved", "group": "g-tradeoff-solver", "plane": "control", "x": 700, "y": 280, "detail": "Stakeholders align on Tier 1 Regional HA, saving $3,700/mo while meeting business goals."}
        ],
        [
            {"id": "e1", "from": "req-5nines", "to": "tradeoff-matrix", "label": "1. Highlight Cost Implication", "plane": "control"},
            {"id": "e2", "from": "budget-cap-strict", "to": "tradeoff-matrix", "label": "2. Highlight Budget Boundary", "plane": "control"},
            {"id": "e3", "from": "tradeoff-matrix", "to": "agreed-compromise", "label": "3. Reach Executive Consensus", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Conflict Formalization", "edges": ["e1", "e2"], "action": "Architect constructs trade-off matrix demonstrating mathematical incompatibility of five-nines at low budget.", "why_traversal": "Reframes subjective emotional debate into objective financial reality.", "protocol": "Trade-off Matrix Evaluation", "plane": "Control Plane"},
            {"n": 2, "title": "Consensus Alignment", "edges": ["e3"], "action": "Leadership signs off on Regional HA architecture with clear documented RTO/RPO expectations.", "why_traversal": "Protects engineering team from unrealistic SLA commitments.", "protocol": "ADR Stakeholder Sign-Off", "plane": "Control Plane"}
        ],
        [
            {"id": "unspoken-sla-failure", "label": "Unspoken Assumption Causes Production Crisis", "changes": {"failedNodes": ["tradeoff-matrix"], "failedEdges": ["e3"]}, "root_cause": "Architect silently built single-zone database to stay within budget without informing leadership.", "diverted_path": "Zonal maintenance caused 20-minute outage; CEO furious at lack of 5-nines.", "blast_radius": "Executive loss of trust in engineering.", "recovery": "Always document SLA limitations explicitly in Architecture Decision Records signed by executive sponsors."}
        ]
    )

    # 046: Case Study: EHR Healthcare
    specs[46] = make_spec(
        46, "7.4a", "Case Study: EHR Healthcare",
        "Visualizes HIPAA-Compliant Enterprise Healthcare Architecture: On-Premises Hospital EMR systems, Cloud Healthcare API (FHIR/HL7v2), Cloud DLP PII de-identification, and Cloud Spanner multi-region clinical storage.",
        "EHR Healthcare mandates strict HIPAA compliance, continuous patient record synchronization from legacy on-premises hospitals, and sub-second querying of clinical histories with zero downtime.",
        [
            {"id": "g-onprem-hospital", "label": "On-Premises Hospital Clinics & EMRs", "type": "onprem", "scope": "onprem", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-gcp-healthcare", "label": "Google Cloud Healthcare API & DLP Tier", "type": "project", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-clinical-data", "label": "HIPAA-Compliant Multi-Region Persistence", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "hospital-emr", "label": "Epic / Cerner Hospital EMR", "product": "HL7v2 / C-CDA Feeds", "group": "g-onprem-hospital", "plane": "data", "x": 140, "y": 140, "detail": "Generates real-time patient admission, discharge, and transfer (ADT) messages."},
            {"id": "vpn-interconnect", "label": "Cloud Interconnect (Encrypted)", "product": "MACsec Dedicated 10Gbps", "group": "g-onprem-hospital", "plane": "data", "x": 140, "y": 280, "detail": "Dedicated private hybrid connection with MACsec L2 wire-speed encryption."},
            {"id": "healthcare-api", "label": "Cloud Healthcare API", "product": "FHIR Store (R4) & HL7 Ingestion", "group": "g-gcp-healthcare", "plane": "data", "x": 440, "y": 140, "detail": "Translates legacy HL7 messages into modern FHIR resources with BAA signed."},
            {"id": "dlp-healthcare", "label": "Cloud DLP De-Identification", "product": "Crypto-Hash Medical Record Numbers", "group": "g-gcp-healthcare", "plane": "control", "x": 440, "y": 280, "detail": "Pseudonymizes patient identifiers for clinical research pipelines."},
            {"id": "spanner-ehr", "label": "Cloud Spanner EHR Multi-Region", "product": "99.999% Clinical Relational DB", "group": "g-clinical-data", "plane": "data", "x": 780, "y": 140, "detail": "Stores core patient charts with continuous multi-region replication and CMEK."},
            {"id": "bq-clinical-lake", "label": "BigQuery Analytics Lake", "product": "De-Identified Research Data", "group": "g-clinical-data", "plane": "data", "x": 780, "y": 280, "detail": "Analyzes clinical efficacy and treatment outcomes without exposing patient PHI."}
        ],
        [
            {"id": "e1", "from": "hospital-emr", "to": "vpn-interconnect", "label": "1. Transmit HL7 Messages", "plane": "data"},
            {"id": "e2", "from": "vpn-interconnect", "to": "healthcare-api", "label": "2. Ingest into Cloud Healthcare API", "plane": "data"},
            {"id": "e3", "from": "healthcare-api", "to": "spanner-ehr", "label": "3. Commit FHIR Patient Chart", "plane": "data"},
            {"id": "e4", "from": "healthcare-api", "to": "dlp-healthcare", "label": "4. Stream for De-Identification", "plane": "control"},
            {"id": "e5", "from": "dlp-healthcare", "to": "bq-clinical-lake", "label": "5. Load Sanitized Data to BigQuery", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Secure Ingestion & Standardization", "edges": ["e1", "e2"], "action": "Hospital EMR streams HL7 messages over MACsec Interconnect into Cloud Healthcare API.", "why_traversal": "Normalizes disparate legacy healthcare protocols into standardized FHIR format.", "protocol": "HL7v2 over MLLP / TLS", "plane": "Data Plane"},
            {"n": 2, "title": "Dual-Path Clinical Storage & Research", "edges": ["e3", "e4", "e5"], "action": "Writes raw patient chart to Spanner while de-identifying data for research in BigQuery.", "why_traversal": "Satisfies strict HIPAA patient privacy while enabling population health analytics.", "protocol": "FHIR REST API / DLP Streaming", "plane": "Data Plane"}
        ],
        [
            {"id": "phi-exfiltration-blocked", "label": "Unauthorized Direct Clinical Query Blocked", "changes": {"failedNodes": ["spanner-ehr"], "failedEdges": ["e3"]}, "root_cause": "External analytics dashboard attempted to query raw patient charts directly from Cloud Spanner.", "diverted_path": "VPC Service Controls denies request: analytics must query de-identified BigQuery lake.", "blast_radius": "Zero patient PHI exposed.", "recovery": "Re-point analytics tools to BigQuery de-identified dataset."}
        ],
        # D2
        "Traces End-to-End Patient Record Ingestion: from hospital clinic HL7 message to FHIR parsing, DLP tokenization, and Spanner transactional commit.",
        "Streaming patient telemetry through the Cloud Healthcare API ensures real-time clinical record availability across distributed hospital emergency rooms.",
        [
            {"id": "g-clinic-admission", "label": "Emergency Room Admission Terminal", "type": "onprem", "scope": "onprem", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-ingest-transform", "label": "Cloud Healthcare FHIR Pipeline", "type": "project", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-spanner-commit", "label": "Multi-Region Patient EHR Persistence", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "er-terminal", "label": "ER Check-In Terminal", "product": "HL7 ADT_A01 Message", "group": "g-clinic-admission", "plane": "data", "x": 140, "y": 200, "detail": "Nurse admits patient in hospital; generates HL7 admission transaction."},
            {"id": "hl7-adapter", "label": "Healthcare API Ingress", "product": "HL7v2 to FHIR R4 Converter", "group": "g-ingest-transform", "plane": "data", "x": 440, "y": 140, "detail": "Validates message structure and converts to Patient and Encounter FHIR resources."},
            {"id": "audit-hipaa", "label": "HIPAA Audit Logger", "product": "Cloud Audit Logs (Data Access)", "group": "g-ingest-transform", "plane": "control", "x": 440, "y": 280, "detail": "Logs exact clinician ID, timestamp, and patient identifier access for HIPAA audits."},
            {"id": "spanner-ehr-master", "label": "Cloud Spanner Leader", "product": "External Consistency Commit", "group": "g-spanner-commit", "plane": "data", "x": 780, "y": 200, "detail": "Commits patient encounter in 4ms; immediately visible to doctors in all regions."}
        ],
        [
            {"id": "e1", "from": "er-terminal", "to": "hl7-adapter", "label": "1. Ingest ADT_A01 Admission", "plane": "data"},
            {"id": "e2", "from": "hl7-adapter", "to": "audit-hipaa", "label": "2. Record HIPAA Audit Event", "plane": "control"},
            {"id": "e3", "from": "hl7-adapter", "to": "spanner-ehr-master", "label": "3. Commit FHIR Encounter Record", "plane": "data"}
        ],
        [
            {"n": 1, "title": "HL7 to FHIR Transformation", "edges": ["e1", "e2"], "action": "Cloud Healthcare API ingests message and logs immutable data access audit trail.", "why_traversal": "Guarantees regulatory compliance and converts proprietary formats to open standards.", "protocol": "MLLP / HTTPS", "plane": "Data Plane"},
            {"n": 2, "title": "Multi-Region Clinical Commit", "edges": ["e3"], "action": "Cloud Spanner commits transaction with TrueTime external consistency.", "why_traversal": "Ensures doctors in any connected hospital clinic see identical, up-to-the-millisecond records.", "protocol": "Spanner gRPC Commit", "plane": "Data Plane"}
        ],
        [
            {"id": "truetime-drift-spike", "label": "Clock Drift Halts Cross-Region Transaction", "changes": {"failedNodes": ["spanner-ehr-master"], "failedEdges": ["e3"]}, "root_cause": "Severe NTP clock skew detected on local client machine.", "diverted_path": "Spanner TrueTime API prevents commit until uncertainty window resolves, ensuring zero data anomalies.", "blast_radius": "Transaction delayed by 12ms.", "recovery": "TrueTime self-stabilizes via Google atomic clock synchronization."}
        ],
        # D3
        "Simulates Healthcare Ransomware Outage & Immutable Backup Recovery: hospital on-premises EMR is encrypted by ransomware; Google Cloud Spanner and GCS immutable backups restore operations.",
        "Immutable Object Retention policies (Bucket Lock) prevent ransomware from overwriting or deleting historical cloud backups even if administrative credentials are stolen.",
        [
            {"id": "g-hospital-ransom", "label": "Compromised On-Premises Hospital", "type": "onprem", "scope": "onprem", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-immutable-cloud", "label": "Google Cloud Immutable Recovery Vault", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "ransom-locked-emr", "label": "Ransomware-Encrypted EMR", "product": "Status: DOWN (Cipher Locked)", "group": "g-hospital-ransom", "plane": "data", "x": 220, "y": 140, "detail": "On-premise SAN storage encrypted by malware; hospital clinical staff locked out."},
            {"id": "cut-interconnect", "label": "Sever Interconnect Connection", "product": "Emergency Air-Gap Isolation", "group": "g-hospital-ransom", "plane": "control", "x": 220, "y": 280, "detail": "Network team disables BGP session to prevent ransomware from propagating to cloud."},
            {"id": "locked-gcs-backup", "label": "Locked GCS Backup Vault", "product": "Bucket Lock (WORM Compliant)", "group": "g-immutable-cloud", "plane": "data", "x": 700, "y": 140, "detail": "Holds hourly EHR snapshots; immutable retention policy guarantees files cannot be deleted."},
            {"id": "cloud-ehr-portal", "label": "Cloud Run Emergency Portal", "product": "Disaster Standby EHR Portal", "group": "g-immutable-cloud", "plane": "data", "x": 700, "y": 280, "detail": "Clinicians log into secure Google Cloud portal over BeyondCorp, resuming patient care in 12 minutes."}
        ],
        [
            {"id": "e1", "from": "ransom-locked-emr", "to": "cut-interconnect", "label": "1. Isolate Hospital Network", "plane": "control"},
            {"id": "e2", "from": "cut-interconnect", "to": "locked-gcs-backup", "label": "2. Verify Cloud Backup Integrity", "plane": "control"},
            {"id": "e3", "from": "locked-gcs-backup", "to": "cloud-ehr-portal", "label": "3. Hydrate Emergency EHR Portal", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Air-Gap Network Isolation", "edges": ["e1", "e2"], "action": "Interconnect severed to protect cloud environment; Cloud Storage Bucket Lock verified intact.", "why_traversal": "WORM (Write Once, Read Many) compliance prevents ransomware from tampering with cloud backups.", "protocol": "BGP Shutdown", "plane": "Control Plane"},
            {"n": 2, "title": "Emergency Cloud Activation", "edges": ["e3"], "action": "Emergency clinical portal activated; doctors access patient medical records securely.", "why_traversal": "Restores life-saving clinical operations without paying ransom.", "protocol": "BeyondCorp Zero Trust Ingress", "plane": "Data Plane"}
        ],
        [
            {"id": "stolen-admin-delete-fail", "label": "Attacker Tries to Delete Immutable Backups", "changes": {"failedNodes": ["locked-gcs-backup"], "failedEdges": ["e3"]}, "root_cause": "Attacker obtained GCP Project Owner credentials and ran 'gsutil rm -r gs://ehr-backups'.", "diverted_path": "Cloud Storage Bucket Lock strictly rejects deletion: retention policy active.", "blast_radius": "Zero backup data lost.", "recovery": "Revoke compromised admin credentials and notify enterprise incident response team."}
        ]
    )

    # 047: Case Study: Mountkirk Games
    specs[47] = make_spec(
        47, "7.4b", "Case Study: Mountkirk Games",
        "Visualizes Mountkirk Games Global Real-Time Gaming Architecture: Global Anycast External ALB, GKE Autopilot Game Server fleets managed by Agones, Cloud Spanner for player profiles, and Pub/Sub + Dataflow telemetry pipelines.",
        "Mountkirk Games requires global low-latency multiplayer matchmaking, dynamic scaling to absorb millions of concurrent players during new game releases, and global consistency for game economies and leaderboards.",
        [
            {"id": "g-gamers-edge", "label": "Global Gamers & Anycast Edge", "type": "external", "scope": "global", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-agones-fleet", "label": "GKE Agones Game Server Fleets", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-game-persistence", "label": "Cloud Spanner & Analytics Pipeline", "type": "project", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "mobile-gamer", "label": "Global Mobile Gamers", "product": "UDP / WebSockets (Low Latency)", "group": "g-gamers-edge", "plane": "data", "x": 140, "y": 140, "detail": "Millions of concurrent players connecting from North America, Europe, and Asia."},
            {"id": "anycast-game-lb", "label": "External Passthrough LB", "product": "Global Anycast VIP (UDP)", "group": "g-gamers-edge", "plane": "data", "x": 140, "y": 280, "detail": "Terminates player UDP traffic at edge and routes to nearest regional cluster."},
            {"id": "agones-controller", "label": "Agones Game Controller", "product": "Kubernetes Custom Resource (CRD)", "group": "g-agones-fleet", "plane": "control", "x": 440, "y": 140, "detail": "Allocates game session pods; marks pods as 'Allocated' so autoscaler will not terminate them."},
            {"id": "game-pod", "label": "Dedicated Game Server Pod", "product": "C++ / Go Game Engine (UDP)", "group": "g-agones-fleet", "plane": "data", "x": 440, "y": 280, "detail": "Runs 60 FPS real-time match simulation for 100 players with sub-30ms tick rate."},
            {"id": "spanner-economy", "label": "Cloud Spanner Leaderboards", "product": "Global Consistency / Inventory", "group": "g-game-persistence", "plane": "data", "x": 780, "y": 140, "detail": "Guarantees zero item duplication or currency race conditions across global players."},
            {"id": "pubsub-telemetry", "label": "Pub/Sub Game Analytics", "product": "500,000 Events/sec Ingestion", "group": "g-game-persistence", "plane": "data", "x": 780, "y": 280, "detail": "Streams game event telemetry to Dataflow and BigQuery for anti-cheat detection."}
        ],
        [
            {"id": "e1", "from": "mobile-gamer", "to": "anycast-game-lb", "label": "1. Connect over Anycast UDP", "plane": "data"},
            {"id": "e2", "from": "anycast-game-lb", "to": "agones-controller", "label": "2. Request Matchmaking Allocation", "plane": "control"},
            {"id": "e3", "from": "agones-controller", "to": "game-pod", "label": "3. Allocate Dedicated Game Pod", "plane": "control"},
            {"id": "e4", "from": "game-pod", "to": "spanner-economy", "label": "4. Persist Match Rewards & Items", "plane": "data"},
            {"id": "e5", "from": "game-pod", "to": "pubsub-telemetry", "label": "5. Stream In-Game Telemetry", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Low-Latency Ingress & Session Allocation", "edges": ["e1", "e2", "e3"], "action": "Anycast routes players to local region; Agones allocates dedicated match server pod.", "why_traversal": "Keeps network latency under 30ms while preventing pod eviction mid-game.", "protocol": "UDP / Agones API", "plane": "Data Plane"},
            {"n": 2, "title": "Economy Persistence & Analytics Streaming", "edges": ["e4", "e5"], "action": "Game server records loot to Cloud Spanner and streams match metrics to Pub/Sub.", "why_traversal": "Prevents virtual currency duplication and feeds real-time anti-cheat analytics.", "protocol": "Spanner gRPC / Pub/Sub API", "plane": "Data Plane"}
        ],
        [
            {"id": "pod-termination-mid-match", "label": "Autoscaler Prematurely Terminates Active Game", "changes": {"failedNodes": ["agones-controller"], "failedEdges": ["e3"]}, "root_cause": "Generic Kubernetes Horizontal Pod Autoscaler was used instead of Agones custom controller.", "diverted_path": "HPA terminated 50 active match pods during traffic dip, disconnecting 5,000 players.", "blast_radius": "Player frustration and app store ratings drop.", "recovery": "Always use Agones Fleet Autoscaler which respects 'Allocated' state and never kills active sessions."}
        ],
        # D2
        "Traces Matchmaking & Session Lifecycle Flow: player match request -> matchmaker allocation -> game server provisioning -> live gameplay -> match completion rewards.",
        "Decoupling the stateless matchmaking engine from stateful game servers allows independent scaling during sudden viral game launch surges.",
        [
            {"id": "g-player-match", "label": "Matchmaking Client Ingress", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-agones-lifecycle", "label": "Agones Pod Lifecycle Orchestration", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-rewards-commit", "label": "Player Inventory & Leaderboard Commit", "type": "project", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "matchmaker-svc", "label": "Open Match Service", "product": "Cloud Run Matchmaker", "group": "g-player-match", "plane": "control", "x": 140, "y": 200, "detail": "Groups 100 players with similar skill rating (MMR) into match ticket."},
            {"id": "agones-allocator", "label": "Agones Allocator Service", "product": "gRPC Fleet Allocator", "group": "g-agones-lifecycle", "plane": "control", "x": 440, "y": 140, "detail": "Finds Ready game pod; marks state as 'Allocated' in 15ms."},
            {"id": "active-match-pod", "label": "Active Game Session Pod", "product": "Playing State (15 min)", "group": "g-agones-lifecycle", "plane": "data", "x": 440, "y": 280, "detail": "Hosts multiplayer match; streams game physics updates over UDP."},
            {"id": "spanner-loot-commit", "label": "Cloud Spanner Transaction", "product": "Atomic In-App Purchase & XP", "group": "g-rewards-commit", "plane": "data", "x": 780, "y": 200, "detail": "Transacts player rewards and updates global leaderboard ranking atomically."}
        ],
        [
            {"id": "e1", "from": "matchmaker-svc", "to": "agones-allocator", "label": "1. Request Match Server Assignment", "plane": "control"},
            {"id": "e2", "from": "agones-allocator", "to": "active-match-pod", "label": "2. Transition Pod to 'Allocated'", "plane": "control"},
            {"id": "e3", "from": "active-match-pod", "to": "spanner-loot-commit", "label": "3. Commit Final Match Rewards", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Game Pod Allocation", "edges": ["e1", "e2"], "action": "Open Match requests server; Agones transitions warm pod from Ready to Allocated.", "why_traversal": "Provides instantaneous sub-second match connection for waiting players.", "protocol": "gRPC Stream", "plane": "Control Plane"},
            {"n": 2, "title": "Atomic Economy Finalization", "edges": ["e3"], "action": "Upon victory, match rewards write to Cloud Spanner with serializable isolation.", "why_traversal": "Eliminates cheating and virtual inventory desynchronization.", "protocol": "Spanner 2PC Commit", "plane": "Data Plane"}
        ],
        [
            {"id": "allocation-timeout-burst", "label": "Fleet Pool Depleted (All Pods Allocated)", "changes": {"failedNodes": ["agones-allocator"], "failedEdges": ["e2"]}, "root_cause": "Traffic spike exhausted pre-warmed Ready buffer; allocator returned 404.", "diverted_path": "Matchmaking queue times increase from 2s to 45s.", "blast_radius": "Delayed matchmaking for new players.", "recovery": "Increase Agones Fleet bufferSize to maintain 25% pre-warmed Ready pods during peak hours."}
        ],
        # D3
        "Simulates Game Launch Day Flash Mob Surge: 10x traffic spike tests GKE Autopilot cluster node autoscaling and Spanner automatic splitting.",
        "Game launch spikes represent massive unpredictable demand; serverless elasticity cushions surges by provisioning thousands of nodes in parallel.",
        [
            {"id": "g-viral-influx", "label": "Viral Game Launch Influx (5M Players)", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-scaling-shield", "label": "Autopilot & Spanner Elastic Headroom", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "gamer-tsunami", "label": "5,000,000 Concurrent Players", "product": "Peak Launch Surge (10x Normal)", "group": "g-viral-influx", "plane": "data", "x": 220, "y": 140, "detail": "Worldwide release triggers unprecedented simultaneous login surge."},
            {"id": "traffic-buffer", "label": "Cloud Armor DDoS & Rate Limiter", "product": "Traffic Smoothing Shield", "group": "g-viral-influx", "plane": "control", "x": 220, "y": 280, "detail": "Smooths packet bursts and blocks malicious bot registration scripts."},
            {"id": "gke-node-surge", "label": "GKE Cluster Autoscaler", "product": "Scales 200 -> 2,500 Nodes", "group": "g-scaling-shield", "plane": "data", "x": 700, "y": 140, "detail": "Provisions Compute Engine compute instances across 3 regional zones dynamically."},
            {"id": "spanner-auto-split", "label": "Spanner Automatic Split Engine", "product": "Splits Load Across 48 Nodes", "group": "g-scaling-shield", "plane": "data", "x": 700, "y": 280, "detail": "Automatically splits hot database split ranges across new compute nodes in seconds."}
        ],
        [
            {"id": "e1", "from": "gamer-tsunami", "to": "traffic-buffer", "label": "1. Ingress 10x Launch Traffic", "plane": "data"},
            {"id": "e2", "from": "traffic-buffer", "to": "gke-node-surge", "label": "2. Trigger GKE Rapid Node Expansion", "plane": "control"},
            {"id": "e3", "from": "traffic-buffer", "to": "spanner-auto-split", "label": "3. Distribute Database Read/Write Spikes", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Traffic Absorption & Cluster Expansion", "edges": ["e1", "e2"], "action": "Cloud Armor smooths traffic; GKE Autoscaler provisions 2,300 additional nodes in 4 minutes.", "why_traversal": "Absorbs viral launch demand without crashing existing game matches.", "protocol": "Compute Engine API", "plane": "Data Plane"},
            {"n": 2, "title": "Linear Database Scaling", "edges": ["e3"], "action": "Cloud Spanner splits player data ranges across expanded node fleet seamlessly.", "why_traversal": "Maintains sub-10ms transactional latency despite 1000% load increase.", "protocol": "Paxos Split Rebalancing", "plane": "Data Plane"}
        ],
        [
            {"id": "gcp-quota-limit-crash", "label": "Regional vCPU Quota Ceiling Blocks Scaling", "changes": {"failedNodes": ["gke-node-surge"], "failedEdges": ["e2"]}, "root_cause": "Project hit hard default regional vCPU quota (limit: 5,000 vCPUs).", "diverted_path": "GKE Autoscaler events show 'QUOTA_EXCEEDED'; players queued in matchmaking for hours.", "blast_radius": "Launch day failure and lost player revenue.", "recovery": "Submit proactive quota increase requests 3 weeks prior to major game launch events."}
        ]
    )

    # 048: Case Study: TerramEarth
    specs[48] = make_spec(
        48, "7.4c", "Case Study: TerramEarth",
        "Visualizes TerramEarth Global IoT Connected Fleet Architecture: 20 Million Agricultural Vehicles, cellular & dealer Wi-Fi ingestion, Cloud Pub/Sub, Cloud Dataflow windowing, Cloud Bigtable time-series storage, and BigQuery ML predictive maintenance.",
        "TerramEarth requires dual-mode telemetry ingestion: intermittent real-time cellular data (200k vehicles) and bulk historical Wi-Fi uploads (20M vehicles), unified into predictive maintenance models to reduce tractor field downtime.",
        [
            {"id": "g-tractor-fleet", "label": "Global Tractor Fleet & Dealerships", "type": "external", "scope": "global", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-dual-ingest", "label": "Dual-Path Telemetry Ingestion Engine", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-lakehouse-analytics", "label": "Bigtable Time-Series & BigQuery ML", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "connected-tractor", "label": "Real-Time Connected Tractors", "product": "Cellular Uplink (200k Units)", "group": "g-tractor-fleet", "plane": "data", "x": 140, "y": 140, "detail": "Streams critical engine temperature and oil pressure metrics in real-time."},
            {"id": "dealer-wifi-upload", "label": "Dealership Maintenance Wi-Fi", "product": "Batch 500MB GCS Dumps (20M Units)", "group": "g-tractor-fleet", "plane": "data", "x": 140, "y": 280, "detail": "Uploads accumulated 500MB sensor log files when tractor visits dealer for service."},
            {"id": "pubsub-cellular", "label": "Cloud Pub/Sub Streaming", "product": "Real-time Telemetry Topic", "group": "g-dual-ingest", "plane": "data", "x": 440, "y": 140, "detail": "Ingests real-time cellular sensor events with millisecond latency."},
            {"id": "dataflow-pipeline", "label": "Cloud Dataflow (Beam)", "product": "Streaming & Batch Unification", "group": "g-dual-ingest", "plane": "control", "x": 440, "y": 280, "detail": "Applies 10-minute sliding windows and normalizes disparate sensor schemas."},
            {"id": "bigtable-timeseries", "label": "Cloud Bigtable (Telemetry)", "product": "Sub-10ms Time-Series Store", "group": "g-lakehouse-analytics", "plane": "data", "x": 780, "y": 140, "detail": "Stores billions of operational data points keyed by tractor_id#timestamp."},
            {"id": "bq-predictive-ml", "label": "BigQuery Predictive Maintenance", "product": "BQML Failure Forecasting", "group": "g-lakehouse-analytics", "plane": "control", "x": 780, "y": 280, "detail": "Predicts component failure 4 weeks before breakdown, dispatching dealer parts automatically."}
        ],
        [
            {"id": "e1", "from": "connected-tractor", "to": "pubsub-cellular", "label": "1. Stream Real-time Metrics", "plane": "data"},
            {"id": "e2", "from": "dealer-wifi-upload", "to": "dataflow-pipeline", "label": "2. Ingest Batch Sensor Dumps", "plane": "data"},
            {"id": "e3", "from": "pubsub-cellular", "to": "dataflow-pipeline", "label": "3. Stream Telemetry to Beam", "plane": "data"},
            {"id": "e4", "from": "dataflow-pipeline", "to": "bigtable-timeseries", "label": "4. Write Time-Series Records", "plane": "data"},
            {"id": "e5", "from": "bigtable-timeseries", "to": "bq-predictive-ml", "label": "5. Train Predictive ML Models", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Dual-Path Telemetry Ingestion", "edges": ["e1", "e2", "e3"], "action": "Pub/Sub handles streaming cellular data; Cloud Storage handles dealer batch uploads.", "why_traversal": "Accommodates both modern connected tractors and legacy offline agricultural equipment.", "protocol": "MQTT / HTTPS Batch Upload", "plane": "Data Plane"},
            {"n": 2, "title": "Time-Series Persistence & Predictive AI", "edges": ["e4", "e5"], "action": "Dataflow writes to Bigtable for low-latency operational dashboarding; BigQuery trains failure models.", "why_traversal": "Reduces catastrophic in-field tractor breakdowns by 85%.", "protocol": "Bigtable gRPC / BigQuery Storage API", "plane": "Data Plane"}
        ],
        [
            {"id": "batch-gcs-parser-crash", "label": "Corrupted CSV Format Crashes Batch Pipeline", "changes": {"failedNodes": ["dataflow-pipeline"], "failedEdges": ["e2"]}, "root_cause": "Dealer uploaded corrupted binary file with .csv extension.", "diverted_path": "Dataflow worker threw uncaught parse exception; batch job failed.", "blast_radius": "Delayed dealer maintenance reports.", "recovery": "Add dead-letter queue (DLQ) pattern in Apache Beam pipeline to discard malformed records."}
        ],
        # D2
        "Traces Predictive Maintenance Pipeline Flow: raw sensor anomaly detection in Bigtable -> BigQuery ML model inference -> automated parts dispatch to local dealership.",
        "Predictive maintenance bridges real-time telemetry with supply chain logistics, ensuring replacement parts arrive at the dealership before the tractor breaks down.",
        [
            {"id": "g-anomaly-detect", "label": "Real-Time Sensor Anomaly Trigger", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-ml-prediction", "label": "BigQuery Machine Learning Inference", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-dispatch-supply", "label": "Automated Dealership Logistics", "type": "organization", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "sensor-spike", "label": "Turbine RPM Vibration Spike", "product": "Vibration > 4.2 Gs (Anomaly)", "group": "g-anomaly-detect", "plane": "data", "x": 140, "y": 200, "detail": "Harvester sensor detects abnormal high-frequency vibration in main cutting drum."},
            {"id": "bqml-model", "label": "BigQuery ML Classification", "product": "ML.PREDICT (Failure Prob: 94%)", "group": "g-ml-prediction", "plane": "control", "x": 440, "y": 200, "detail": "Evaluates vibration pattern against 10 years of historical failure telemetry."},
            {"id": "dealer-parts-order", "label": "Automated SAP Parts Order", "product": "Part #CR-8891 Bearing Assembly", "group": "g-dispatch-supply", "plane": "control", "x": 780, "y": 140, "detail": "Automatically triggers replacement part shipment from regional warehouse."},
            {"id": "farmer-mobile-app", "label": "Farmer Notification Push", "product": "Schedule Service Warning", "group": "g-dispatch-supply", "plane": "data", "x": 780, "y": 280, "detail": "Alerts farmer via mobile app to bring harvester to dealer before harvest season begins."}
        ],
        [
            {"id": "e1", "from": "sensor-spike", "to": "bqml-model", "label": "1. Feed Anomaly to ML Model", "plane": "control"},
            {"id": "e2", "from": "bqml-model", "to": "dealer-parts-order", "label": "2. Failure Probability > 90% -> Order Part", "plane": "control"},
            {"id": "e3", "from": "dealer-parts-order", "to": "farmer-mobile-app", "label": "3. Notify Farmer with Available Appointment", "plane": "control"}
        ],
        [
            {"n": 1, "title": "ML Failure Prediction", "edges": ["e1", "e2"], "action": "BQML evaluates live sensor stream against failure patterns; flags 94% failure risk.", "why_traversal": "Identifies impending failure weeks before human operators can detect symptoms.", "protocol": "BigQuery SQL ML.PREDICT", "plane": "Control Plane"},
            {"n": 2, "title": "Autonomous Supply Chain Dispatch", "edges": ["e3"], "action": "ERP system automatically orders parts and sends appointment slot to farmer's mobile phone.", "why_traversal": "Eliminates downtime during critical 14-day annual crop harvest window.", "protocol": "REST API / Cloud Tasks", "plane": "Control Plane"}
        ],
        [
            {"id": "false-positive-parts-flood", "label": "Model Overfitting Orders Unneeded Parts", "changes": {"failedNodes": ["bqml-model"], "failedEdges": ["e2"]}, "root_cause": "Model was trained on unnormalized data from rocky field terrain; flagged normal bumps as failures.", "diverted_path": "500 unnecessary parts shipped to rural dealerships.", "blast_radius": "Logistical waste.", "recovery": "Retrain model with accelerometer normalization and feature engineering on soil terrain type."}
        ],
        # D3
        "Simulates Cellular Blackout & Massive Post-Outage Ingestion Surge: 50,000 tractors reconnect simultaneously after a regional cellular outage.",
        "Buffer-based streaming architecture (Pub/Sub + Dataflow) absorbs massive reconnection surges without dropping telemetry or crashing analytics backends.",
        [
            {"id": "g-blackout-reconnect", "label": "Post-Cellular Outage Influx (50,000 Tractors)", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-pubsub-buffer", "label": "Pub/Sub & Dataflow Elastic Cushion", "type": "project", "scope": "regional", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "backlog-surge", "label": "Accumulated Telemetry Surge", "product": "50k Units Uploading 6 Hours of Logs", "group": "g-blackout-reconnect", "plane": "data", "x": 220, "y": 140, "detail": "Tractors re-establish cellular link and dump buffered local memory simultaneously."},
            {"id": "pubsub-backlog-absorber", "label": "Pub/Sub Elastic Partition Buffer", "product": "Absorbs 250k msgs/sec Spike", "group": "g-blackout-reconnect", "plane": "control", "x": 220, "y": 280, "detail": "Pub/Sub scales dynamically without provisioned partition limits, buffering messages safely."},
            {"id": "dataflow-autoscale-fleet", "label": "Dataflow Autoscaling Workers", "product": "Scales 8 -> 64 n2-standard-4 Nodes", "group": "g-pubsub-buffer", "plane": "data", "x": 700, "y": 140, "detail": "Autoscaler monitors Pub/Sub backlog age and spins up 64 workers within 3 minutes."},
            {"id": "bigtable-smooth-ingest", "label": "Bigtable Writes Sustained", "product": "Sub-8ms Write Latency Maintained", "group": "g-pubsub-buffer", "plane": "data", "x": 700, "y": 280, "detail": "Bigtable absorbs 250,000 writes/sec with zero dropped packets and no hotspotting."}
        ],
        [
            {"id": "e1", "from": "backlog-surge", "to": "pubsub-backlog-absorber", "label": "1. Influx Reconnection Telemetry", "plane": "data"},
            {"id": "e2", "from": "pubsub-backlog-absorber", "to": "dataflow-autoscale-fleet", "label": "2. Signal Backlog Growth to Autoscaler", "plane": "control"},
            {"id": "e3", "from": "dataflow-autoscale-fleet", "to": "bigtable-smooth-ingest", "label": "3. Parallel Drain to Bigtable", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Surge Decoupling & Buffering", "edges": ["e1", "e2"], "action": "Pub/Sub absorbs 20x traffic surge without backpressure; Dataflow scales up worker nodes.", "why_traversal": "Decouples unpredictable vehicle reconnection bursts from processing capacity.", "protocol": "Cloud Pub/Sub Streaming", "plane": "Control Plane"},
            {"n": 2, "title": "Parallel Backlog Processing", "edges": ["e3"], "action": "64 Dataflow workers drain backlog in 18 minutes, writing orderly time-series into Bigtable.", "why_traversal": "Guarantees zero data loss while maintaining real-time processing SLAs.", "protocol": "Apache Beam Pipeline", "plane": "Data Plane"}
        ],
        [
            {"id": "direct-db-write-crash", "label": "Direct Database Write Anti-Pattern Meltdown", "changes": {"failedNodes": ["pubsub-backlog-absorber"], "failedEdges": ["e2"]}, "root_cause": "System attempted to write tractor telemetry directly to database without Pub/Sub buffer.", "diverted_path": "50,000 simultaneous connections exhausted DB connection pool; 80% of packets lost.", "blast_radius": "Permanent loss of critical field sensor data.", "recovery": "Never connect external IoT devices directly to databases; always place Cloud Pub/Sub at ingress."}
        ]
    )

    # 049: Case Study: Helicopter Racing League
    specs[49] = make_spec(
        49, "7.4d", "Case Study: Helicopter Racing League",
        "Visualizes Helicopter Racing League (HRL) Low-Latency Global Telemetry & Video Streaming Architecture: Helicopter telemetry sensors & HD cameras, Cloud Pub/Sub, Cloud Dataflow, Cloud Spanner, and Cloud CDN video acceleration.",
        "HRL requires sub-second streaming of in-flight race telemetry (G-force, RPM, position) to augment global live video broadcasts with real-time predictive overtake AI graphics.",
        [
            {"id": "g-racing-copters", "label": "Race Helicopters & In-Flight Sensors", "type": "external", "scope": "global", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-realtime-processing", "label": "Real-Time Telemetry & AI Prediction", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-viewer-broadcast", "label": "Global Fan Experience & Live Video Tier", "type": "vpc", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "helicopter-telemetry", "label": "Helicopter Sensor Array", "product": "100Hz Telemetry & 4K Camera", "group": "g-racing-copters", "plane": "data", "x": 140, "y": 140, "detail": "Streams rotor RPM, airspeed, GPS coordinates, and G-force over private cellular."},
            {"id": "mobile-edge-cell", "label": "5G Trackside Mobile Edge", "product": "Google Cloud Distributed Edge", "group": "g-racing-copters", "plane": "data", "x": 140, "y": 280, "detail": "Ultra-low-latency 5G edge compute gateway at racing circuit PoP."},
            {"id": "dataflow-telemetry", "label": "Dataflow Streaming Engine", "product": "Sliding Window Race Positions", "group": "g-realtime-processing", "plane": "data", "x": 440, "y": 140, "detail": "Computes instantaneous race leaderboards and lap split times in under 50ms."},
            {"id": "vertex-predictive-ai", "label": "Vertex AI Overtake Predictor", "product": "Real-time Probability Engine", "group": "g-realtime-processing", "plane": "control", "x": 440, "y": 280, "detail": "Predicts pass probability based on rotor aerodynamics and entry velocity."},
            {"id": "cloud-cdn-video", "label": "Cloud CDN Live Video Cache", "product": "Low-Latency HLS / CMAF Stream", "group": "g-viewer-broadcast", "plane": "data", "x": 780, "y": 140, "detail": "Distributes 4K race video feeds worldwide with sub-second glass-to-glass latency."},
            {"id": "spanner-race-state", "label": "Cloud Spanner Live Leaderboard", "product": "Global Race Standings", "group": "g-viewer-broadcast", "plane": "data", "x": 780, "y": 280, "detail": "Delivers globally synchronized race standings to mobile fan apps worldwide."}
        ],
        [
            {"id": "e1", "from": "helicopter-telemetry", "to": "mobile-edge-cell", "label": "1. 5G Low-Latency Sensor Stream", "plane": "data"},
            {"id": "e2", "from": "mobile-edge-cell", "to": "dataflow-telemetry", "label": "2. Ingest to Dataflow Pipeline", "plane": "data"},
            {"id": "e3", "from": "dataflow-telemetry", "to": "vertex-predictive-ai", "label": "3. Feed Real-time Aerodynamic State", "plane": "control"},
            {"id": "e4", "from": "vertex-predictive-ai", "to": "cloud-cdn-video", "label": "4. Inject Dynamic AR Graphic Overlay", "plane": "data"},
            {"id": "e5", "from": "dataflow-telemetry", "to": "spanner-race-state", "label": "5. Update Global Fan Leaderboards", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Ultra-Low Latency Telemetry Ingestion", "edges": ["e1", "e2"], "action": "In-flight sensors stream over 5G edge into Dataflow in under 20 milliseconds.", "why_traversal": "Provides the sub-second baseline needed for augmented reality sports broadcasting.", "protocol": "QUIC / UDP Stream", "plane": "Data Plane"},
            {"n": 2, "title": "Predictive AI Augmentation & Global Broadcast", "edges": ["e3", "e4", "e5"], "action": "Vertex AI predicts overtakes; overlays probability onto video stream cached via Cloud CDN.", "why_traversal": "Engages 10 million global fans with cutting-edge real-time predictive graphics.", "protocol": "CMAF HLS / Spanner gRPC", "plane": "Data Plane"}
        ],
        [
            {"id": "canyon-5g-drop", "label": "Intermittent Track Shadow Signal Loss", "changes": {"failedNodes": ["mobile-edge-cell"], "failedEdges": ["e2"]}, "root_cause": "Helicopter dipped into mountain canyon, dropping 5G signal for 4 seconds.", "diverted_path": "Helicopter onboard flash memory buffered telemetry; transmitted burst upon re-emergence.", "blast_radius": "Dataflow event-time watermarking sorted packets correctly with zero distortion.", "recovery": "Dataflow watermark handling absorbed out-of-order data automatically."}
        ],
        # D2
        "Traces Real-Time Predictive AI Graphics Injection Flow: telemetry ingestion -> aerodynamic ML inference -> graphic overlay composition -> Cloud CDN broadcast distribution.",
        "Synchronizing sensor event timestamps with video presentation timestamps (PTS) ensures augmented reality telemetry overlays align perfectly with live helicopter footage.",
        [
            {"id": "g-raw-sensor", "label": "In-Flight Sensor Telemetry", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-ar-composer", "label": "AI Prediction & Video Compositor", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-fan-endpoints", "label": "Global Fan Mobile & TV Broadcast", "type": "project", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "rotor-data", "label": "Rotor Pitch & Bank Angle", "product": "Event Timestamp: 14:02:11.450", "group": "g-raw-sensor", "plane": "data", "x": 140, "y": 200, "detail": "Helicopter #7 banks hard into turn 4 at 160 knots."},
            {"id": "ai-pass-model", "label": "Vertex AI Prediction Endpoint", "product": "Inference Latency: 12ms", "group": "g-ar-composer", "plane": "control", "x": 440, "y": 140, "detail": "Predicts 87% probability of overtaking Helicopter #2 in turn 4."},
            {"id": "transcoder-api", "label": "Live Stream Video Transcoder", "product": "Transcoder API (CMAF)", "group": "g-ar-composer", "plane": "data", "x": 440, "y": 280, "detail": "Composites dynamic '87% OVERTAKE' graphic onto 4K video frame."},
            {"id": "fan-screen", "label": "Fan Living Room TV (4K 60FPS)", "product": "Cloud CDN Glass-to-Glass: 850ms", "group": "g-fan-endpoints", "plane": "data", "x": 780, "y": 200, "detail": "Displays synchronized graphic overlay matching live helicopter banking on screen."}
        ],
        [
            {"id": "e1", "from": "rotor-data", "to": "ai-pass-model", "label": "1. Send Flight Dynamics to Model", "plane": "control"},
            {"id": "e2", "from": "ai-pass-model", "to": "transcoder-api", "label": "2. Inject Prediction Metadata", "plane": "control"},
            {"id": "e3", "from": "transcoder-api", "to": "fan-screen", "label": "3. Broadcast Enhanced Stream", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Sub-Second AI Inference", "edges": ["e1", "e2"], "action": "Vertex AI computes overtake odds in 12ms; passes metadata to Live Stream Transcoder.", "why_traversal": "Enables predictive graphics before the physical maneuver even concludes.", "protocol": "gRPC Inference", "plane": "Control Plane"},
            {"n": 2, "title": "Ultra-Low-Latency CDN Delivery", "edges": ["e3"], "action": "Transcoder emits CMAF chunks cached at Google edge PoPs; viewers watch with sub-second delay.", "why_traversal": "Creates an immersive real-time viewing experience on par with on-track spectators.", "protocol": "HTTP/3 CMAF over Cloud CDN", "plane": "Data Plane"}
        ],
        [
            {"id": "pts-desync-lag", "label": "Video-Telemetry Clock Desynchronization", "changes": {"failedNodes": ["transcoder-api"], "failedEdges": ["e2"]}, "root_cause": "Telemetry NTP clock differed from video camera Genlock clock by 400ms.", "diverted_path": "Graphic overlay appeared 400ms after the overtake was already completed on screen.", "blast_radius": "Awkward viewer experience.", "recovery": "Lock telemetry sensor timestamps directly to camera video timecode (SMPTE) at edge."}
        ],
        # D3
        "Simulates Cloud CDN Video Ingress Failure & Multi-Region Fallback: primary video transcoder facility loses power; traffic fails over to backup regional transcoder with zero stream interruption.",
        "Live sports broadcasting demands zero buffering; dual-region active-active transcoding clusters paired with Cloud CDN origin failover eliminate viewer blackouts.",
        [
            {"id": "g-pri-transcode", "label": "Primary Transcoder: us-central1 (Outage)", "type": "region", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-sec-transcode", "label": "Secondary Transcoder: us-east4 (Failover)", "type": "region", "scope": "regional", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "pri-encoder-dead", "label": "Primary Transcoder (Failed)", "product": "Status: POWER_FAILURE", "group": "g-pri-transcode", "plane": "data", "x": 220, "y": 140, "detail": "Datacenter power glitch abruptly knocks out primary encoding cluster."},
            {"id": "cdn-origin-shield", "label": "Cloud CDN Origin Failover", "product": "Automatic Backend Switching", "group": "g-pri-transcode", "plane": "control", "x": 220, "y": 280, "detail": "Detects HTTP 502 from primary origin; automatically shifts requests to secondary origin."},
            {"id": "sec-encoder-live", "label": "Secondary Transcoder (Active)", "product": "Encoding 4K Stream in us-east4", "group": "g-sec-transcode", "plane": "data", "x": 700, "y": 140, "detail": "Warm standby transcoder picks up stream chunk encoding in < 2 seconds."},
            {"id": "uninterrupted-fans", "label": "Global Viewers (Zero Buffering)", "product": "Continuous Video Playback", "group": "g-sec-transcode", "plane": "data", "x": 700, "y": 280, "detail": "Edge cache buffers absorb 2-second switchover; zero dropped frames for 10M viewers."}
        ],
        [
            {"id": "e1", "from": "pri-encoder-dead", "to": "cdn-origin-shield", "label": "1. Detect Origin Failure", "plane": "control"},
            {"id": "e2", "from": "cdn-origin-shield", "to": "sec-encoder-live", "label": "2. Reroute Origin Traffic", "plane": "control"},
            {"id": "e3", "from": "sec-encoder-live", "to": "uninterrupted-fans", "label": "3. Stream Secondary Video Chunks", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Automated Origin Health Check Detection", "edges": ["e1", "e2"], "action": "Cloud CDN detects primary origin failure and switches to secondary origin automatically.", "why_traversal": "Eliminates single point of failure in video distribution pipeline.", "protocol": "CDN Origin Failover Policy", "plane": "Control Plane"},
            {"n": 2, "title": "Zero-Buffer Viewer Experience", "edges": ["e3"], "action": "Secondary origin continues segment stream; player video buffer plays through transition.", "why_traversal": "Protects broadcast integrity and sponsor advertising revenue.", "protocol": "HTTPS CMAF Video Chunks", "plane": "Data Plane"}
        ],
        [
            {"id": "origin-failover-timeout-stall", "label": "Long Health Check Timeout Causes Player Buffering", "changes": {"failedNodes": ["cdn-origin-shield"], "failedEdges": ["e2"]}, "root_cause": "Origin timeout set to 15 seconds; player 3-second buffer emptied before switch occurred.", "diverted_path": "Viewers saw spinning loading wheel for 12 seconds.", "blast_radius": "Viewer complaints during final race lap.", "recovery": "Tune Cloud CDN origin timeout to 2 seconds with 2 consecutive retry limits."}
        ]
    )

    # 050: PCA Exam Strategy & Keyword Elimination
    specs[50] = make_spec(
        50, "7.5", "PCA Exam Strategy & Keyword Elimination",
        "Visualizes Google Cloud Certified Professional Cloud Architect (PCA) Exam Deconstruction Strategy: stem keyword extraction, distractor elimination rubric, Google-recommended practices alignment, and winning architecture selection.",
        "The PCA exam tests decision-making under constraints: identify the question's explicit business trade-offs ('minimal operational overhead' = serverless; 'lift-and-shift' = M4VM; 'global SQL' = Spanner) to eliminate distractors with certainty.",
        [
            {"id": "g-exam-stem", "label": "Question Stem & Keyword Extraction", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-distractor-filter", "label": "Distractor Elimination & Antipattern Filter", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-winning-choice", "label": "Validated Exam-Winning GCP Architecture", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "exam-question", "label": "PCA Exam Scenario Stem", "product": "Constraint: 'Minimal Ops + Container'", "group": "g-exam-stem", "plane": "control", "x": 140, "y": 140, "detail": "Question specifies deploying stateless web container with automated scaling and zero server management."},
            {"id": "keyword-extractor", "label": "Keyword Matcher", "product": "Flags: 'Minimal Ops' -> Serverless", "group": "g-exam-stem", "plane": "control", "x": 140, "y": 280, "detail": "Keywords strictly demand fully managed serverless over self-managed VMs."},
            {"id": "eliminate-gce", "label": "Discard: Compute Engine VMs", "product": "Eliminated: High Operational Burden", "group": "g-distractor-filter", "plane": "control", "x": 440, "y": 100, "detail": "Requires OS patching, custom scaling scripts, and manual VM maintenance."},
            {"id": "eliminate-gke-std", "label": "Discard: GKE Standard", "product": "Eliminated: Node Pool Management", "group": "g-distractor-filter", "plane": "control", "x": 440, "y": 200, "detail": "Requires configuring node pools, upgrading kubelet versions, and rightsizing nodes."},
            {"id": "winning-cloudrun", "label": "Correct Option: Cloud Run", "product": "Serverless Container Execution", "group": "g-winning-choice", "plane": "data", "x": 780, "y": 200, "detail": "Zero server management, native OCI container support, scale-to-zero, per-second billing."}
        ],
        [
            {"id": "e1", "from": "exam-question", "to": "keyword-extractor", "label": "1. Extract Core Constraint Keywords", "plane": "control"},
            {"id": "e2", "from": "keyword-extractor", "to": "eliminate-gce", "label": "2. Rule Out Self-Managed VMs", "plane": "control"},
            {"id": "e3", "from": "keyword-extractor", "to": "eliminate-gke-std", "label": "3. Rule Out Complex Node Mgmt", "plane": "control"},
            {"id": "e4", "from": "keyword-extractor", "to": "winning-cloudrun", "label": "4. Match Google-Recommended Best Practice", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Keyword Isolation & Elimination", "edges": ["e1", "e2", "e3"], "action": "Extracts 'minimal ops'; eliminates Compute Engine and GKE Standard as high maintenance.", "why_traversal": "Eliminates 2 of 4 multiple-choice options within 15 seconds.", "protocol": "Keyword Elimination Logic", "plane": "Control Plane"},
            {"n": 2, "title": "Best-Practice Selection", "edges": ["e4"], "action": "Selects Cloud Run as the optimal fit meeting 100% of functional and operational criteria.", "why_traversal": "Aligns with Google Cloud Architecture Framework principles.", "protocol": "Decision Tree Match", "plane": "Data Plane"}
        ],
        [
            {"id": "overlooked-caveat-trap", "label": "Overlooked 'Non-HTTP' Constraint Fails Selection", "changes": {"failedNodes": ["winning-cloudrun"], "failedEdges": ["e4"]}, "root_cause": "Candidate missed that the container required custom raw TCP/UDP protocol not supported by Cloud Run.", "diverted_path": "Cloud Run selection fails; GKE Autopilot was the correct choice.", "blast_radius": "Incorrect answer selected on exam.", "recovery": "Always verify protocol constraints (HTTP/gRPC vs raw TCP/UDP) before finalizing compute choice."}
        ],
        # D2
        "Traces Step-by-Step Question Deconstruction Traversal: read stem -> identify constraint modifiers -> eliminate distractors -> select Google recommended answer.",
        "Systematic elimination consistently narrows questions down from 4 possibilities to 1 unambiguous winning answer in under 60 seconds.",
        [
            {"id": "g-stem-reading", "label": "Step 1: Read Stem & Highlight Modifiers", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-antipattern-scan", "label": "Step 2: Antipattern Elimination", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-validated-pick", "label": "Step 3: Validated Exam Selection", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "scenario-input", "label": "Question: 'Migrate on-prem VM rapidly'", "product": "Constraint: 'Minimal refactoring'", "group": "g-stem-reading", "plane": "control", "x": 140, "y": 200, "detail": "Must migrate 200 Windows VMs to Google Cloud within 30 days."},
            {"id": "discard-rewrite", "label": "Discard: 'Rewrite to Cloud Functions'", "product": "Fails: 30-day timeline impossible", "group": "g-antipattern-scan", "plane": "control", "x": 440, "y": 140, "detail": "Rewriting 200 applications in 30 days is unrealistic; violates 'minimal refactoring'."},
            {"id": "discard-manual", "label": "Discard: 'Export OVA & upload to GCS'", "product": "Fails: High manual toil", "group": "g-antipattern-scan", "plane": "control", "x": 440, "y": 280, "detail": "Manual export/import causes days of downtime per server."},
            {"id": "select-m4vm", "label": "Select: Migrate to Virtual Machines", "product": "Correct: Automated Replication Engine", "group": "g-validated-pick", "plane": "data", "x": 780, "y": 200, "detail": "Replicates live VM disks in background; automated cutover with minimal downtime."}
        ],
        [
            {"id": "e1", "from": "scenario-input", "to": "discard-rewrite", "label": "1. Reject Time-Intensive Refactoring", "plane": "control"},
            {"id": "e2", "from": "scenario-input", "to": "discard-manual", "label": "2. Reject Manual High-Downtime Toil", "plane": "control"},
            {"id": "e3", "from": "discard-rewrite", "to": "select-m4vm", "label": "3. Converge on Google Migration Tooling", "plane": "control"},
            {"id": "e4", "from": "discard-manual", "to": "select-m4vm", "label": "4. Confirm Migrate to Virtual Machines", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Modifier Elimination", "edges": ["e1", "e2"], "action": "Filters options that violate timeline or require excessive engineering refactoring.", "why_traversal": "Eliminates options that sound technically impressive but violate practical business constraints.", "protocol": "Rubric Elimination", "plane": "Control Plane"},
            {"n": 2, "title": "Tooling Confirmation", "edges": ["e3", "e4"], "action": "Selects Google's purpose-built migration service (M4VM) as the intended solution.", "why_traversal": "Guarantees full alignment with exam grading key.", "protocol": "PCA Scoring Algorithm", "plane": "Data Plane"}
        ],
        [
            {"id": "deprecated-tool-selection", "label": "Selected Deprecated Velostrata / M4CE Name", "changes": {"failedNodes": ["select-m4vm"], "failedEdges": ["e4"]}, "root_cause": "Candidate memorized outdated product name (Velostrata) instead of current Migrate to Virtual Machines.", "diverted_path": "Confused on exam terminology.", "blast_radius": "Hesitation and potential lost score.", "recovery": "Study modern Google Cloud product branding: Migrate to Virtual Machines (v5.x)."}
        ],
        # D3
        "Simulates Exam Distractor Trap Detection: identifies subtle trick phrases ('least cost', 'RTO = 0', 'global external consistency') that disqualify seemingly correct answers.",
        "Recognizing exam trap phrasing prevents candidates from selecting technically functional but exam-incorrect distractor answers.",
        [
            {"id": "g-trap-phrase", "label": "Subtle Exam Trap Phrasing", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-trap-disarm", "label": "Architectural Trap Disarmament", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "trap-least-cost", "label": "Modifier: 'Most cost-effective'", "product": "Budget is Primary Constraint", "group": "g-trap-phrase", "plane": "control", "x": 220, "y": 140, "detail": "Question asks for the most cost-effective backup storage for 7-year legal compliance."},
            {"id": "distractor-standard", "label": "Distractor: Standard Cloud Storage", "product": "Cost: $0.020/GB/month", "group": "g-trap-phrase", "plane": "control", "x": 220, "y": 280, "detail": "Technically stores backups, but costs 16x more than Archive class."},
            {"id": "winning-archive", "label": "Correct: Archive Cloud Storage", "product": "Cost: $0.0012/GB/month", "group": "g-trap-disarm", "plane": "data", "x": 700, "y": 140, "detail": "Lowest-cost storage class designed specifically for data accessed less than once a year."},
            {"id": "bucket-lock-rule", "label": "Add: Retention Policy (Bucket Lock)", "product": "WORM Compliance Guaranteed", "group": "g-trap-disarm", "plane": "control", "x": 700, "y": 280, "detail": "Satisfies the 7-year regulatory retention requirement without operational overhead."}
        ],
        [
            {"id": "e1", "from": "trap-least-cost", "to": "distractor-standard", "label": "1. Disqualify High-Cost Standard Tier", "plane": "control"},
            {"id": "e2", "from": "trap-least-cost", "to": "winning-archive", "label": "2. Select Archive Tier (Lowest Cost)", "plane": "data"},
            {"id": "e3", "from": "winning-archive", "to": "bucket-lock-rule", "label": "3. Fulfill 7-Year Legal Hold Mandate", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Cost Modifier Analysis", "edges": ["e1", "e2"], "action": "Recognizes 'most cost-effective' requires evaluating storage pricing per gigabyte.", "why_traversal": "Archive class ($0.0012) beats Standard ($0.020) and Nearline ($0.010).", "protocol": "Cost Optimization Analysis", "plane": "Control Plane"},
            {"n": 2, "title": "Regulatory Requirement Alignment", "edges": ["e3"], "action": "Bucket Lock satisfies legal hold requirement cleanly.", "why_traversal": "Delivers comprehensive answer satisfying all question clauses.", "protocol": "Compliance Synthesis", "plane": "Data Plane"}
        ],
        [
            {"id": "overlooked-retrieval-fee", "label": "Selected Archive Storage for Daily Active Backups", "changes": {"failedNodes": ["winning-archive"], "failedEdges": ["e2"]}, "root_cause": "Workload required daily backup restoration tests; Archive retrieval fees made it more expensive than Standard.", "diverted_path": "Retrieval fees exceeded storage savings by 500%.", "blast_radius": "Incorrect answer selected.", "recovery": "Only select Archive storage when data access frequency is strictly once a year or less."}
        ]
    )

    # 051: BigQuery Architecture & Lakehouse Analytics
    specs[51] = make_spec(
        51, "D.1", "Data Warehousing: BigQuery & Looker",
        "Visualizes BigQuery Serverless Lakehouse Architecture: Colossus distributed storage (Capacitor columnar format) decoupled from Dremel query engine (Borg slot scheduler), Jupiter petabit network, BI Engine cache, and Looker semantic modeling.",
        "BigQuery's foundational superpower is the total decoupling of compute from storage: scale storage infinitely at commodity prices while scaling query compute dynamically from 0 to tens of thousands of slots on demand.",
        [
            {"id": "g-storage-colossus", "label": "Colossus Distributed Storage (Capacitor)", "type": "project", "scope": "global", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-compute-dremel", "label": "Dremel Query Execution Engine (Borg)", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-bi-looker", "label": "BI Engine & Looker Semantic Layer", "type": "organization", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "capacitor-files", "label": "Capacitor Columnar Storage", "product": "Partitioned & Clustered Tables", "group": "g-storage-colossus", "plane": "data", "x": 140, "y": 140, "detail": "Stores data organized by column; prune partitions to scan only relevant date blocks."},
            {"id": "jupiter-network", "label": "Jupiter Petabit Network", "product": "1 Petabit/sec Bisection Bandwidth", "group": "g-storage-colossus", "plane": "data", "x": 140, "y": 280, "detail": "Connects thousands of compute slots to storage disks with zero network bottleneck."},
            {"id": "dremel-slots", "label": "Dremel Slot Worker Fleet", "product": "Dynamic Slot Autoscaling (Borg)", "group": "g-compute-dremel", "plane": "data", "x": 440, "y": 140, "detail": "Executes parallel tree aggregation; scales from 100 to 2,000 slots in seconds."},
            {"id": "bi-engine-cache", "label": "BigQuery BI Engine", "product": "In-Memory Vectorized Execution", "group": "g-bi-looker", "plane": "data", "x": 780, "y": 140, "detail": "Sub-second SQL acceleration caching frequently queried analytical aggregations."},
            {"id": "looker-dashboard", "label": "Looker Enterprise BI", "product": "LookML Semantic Modeling", "group": "g-bi-looker", "plane": "control", "x": 780, "y": 280, "detail": "Governed business intelligence dashboards used by 5,000 corporate business analysts."}
        ],
        [
            {"id": "e1", "from": "looker-dashboard", "to": "bi-engine-cache", "label": "1. Execute Analytical Query", "plane": "control"},
            {"id": "e2", "from": "bi-engine-cache", "to": "dremel-slots", "label": "2. Fallback on Cache Miss", "plane": "control"},
            {"id": "e3", "from": "dremel-slots", "to": "jupiter-network", "label": "3. Stream Columns via Jupiter", "plane": "data"},
            {"id": "e4", "from": "jupiter-network", "to": "capacitor-files", "label": "4. Read Partitioned Data", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Decoupled Storage & Compute Querying", "edges": ["e1", "e2"], "action": "Looker submits SQL query; BI Engine serves from memory or falls back to Dremel slots.", "why_traversal": "Delivers sub-second dashboard performance for 90% of business queries.", "protocol": "LookML / BigQuery REST API", "plane": "Control Plane"},
            {"n": 2, "title": "Petabit Shuffling & Aggregation", "edges": ["e3", "e4"], "action": "Jupiter streams columnar data from Colossus disks into Dremel slots in parallel.", "why_traversal": "Scans petabytes of data in seconds without disk I/O bottlenecks.", "protocol": "Jupiter Bisection Network", "plane": "Data Plane"}
        ],
        [
            {"id": "full-table-scan-shock", "label": "Unpartitioned Table Triggers $1,200 Query", "changes": {"failedNodes": ["capacitor-files"], "failedEdges": ["e4"]}, "root_cause": "Analyst ran 'SELECT *' on an unpartitioned 200TB table, scanning all columns and rows.", "diverted_path": "Query scanned 200TB, incurring $1,250 on-demand cost for a single run.", "blast_radius": "Runaway analytical cost spike.", "recovery": "Enforce table partitioning on date and clustering on user_id, and configure maximum bytes billed limits."}
        ],
        # D2
        "Traces Query Optimization Traversal: full table scan vs partitioned & clustered table scan comparing bytes processed, slot usage, and query execution time.",
        "Partitioning and clustering dramatically reduce the number of bytes read, cutting query costs by over 95% while speeding up execution tenfold.",
        [
            {"id": "g-raw-query", "label": "SQL Query Formulation", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-slot-execution", "label": "BigQuery Optimizer & Partition Pruner", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-result-delivery", "label": "Query Results & Financial Impact", "type": "project", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "user-sql", "label": "WHERE order_date = '2026-09-24'", "product": "Targeted Date Filter", "group": "g-raw-query", "plane": "control", "x": 140, "y": 200, "detail": "Queries orders for a single business day out of a 5-year historical dataset."},
            {"id": "partition-pruner", "label": "Partition Pruning Engine", "product": "Prunes 1,824 out of 1,825 Days", "group": "g-slot-execution", "plane": "control", "x": 440, "y": 140, "detail": "Skips 99.9% of storage files; only scans the single matching daily partition block."},
            {"id": "cluster-sorter", "label": "Cluster Key Sorter", "product": "Filter: customer_id = 'C9921'", "group": "g-slot-execution", "plane": "control", "x": 440, "y": 280, "detail": "Within the partition, cluster metadata identifies the exact 128MB block containing customer."},
            {"id": "cost-optimized-result", "label": "Bytes Scanned: 42MB (vs 12TB)", "product": "Cost: $0.0002 / Duration: 1.1s", "group": "g-result-delivery", "plane": "data", "x": 780, "y": 200, "detail": "Returns query result in 1.1 seconds with virtually zero compute cost."}
        ],
        [
            {"id": "e1", "from": "user-sql", "to": "partition-pruner", "label": "1. Evaluate Partition Filter", "plane": "control"},
            {"id": "e2", "from": "partition-pruner", "to": "cluster-sorter", "label": "2. Isolate Clustered Data Blocks", "plane": "control"},
            {"id": "e3", "from": "cluster-sorter", "to": "cost-optimized-result", "label": "3. Stream Compact Results", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Partition & Cluster Pruning", "edges": ["e1", "e2"], "action": "BigQuery query planner reads table metadata and discards 99.9% of storage blocks.", "why_traversal": "Eliminates scanning unreferenced historical data.", "protocol": "Metadata Optimization Engine", "plane": "Control Plane"},
            {"n": 2, "title": "Instant Economical Execution", "edges": ["e3"], "action": "Reads 42MB instead of 12TB, returning answers in 1.1 seconds.", "why_traversal": "Delivers massive cost savings and high concurrency without slot contention.", "protocol": "Capacitor Vector Read", "plane": "Data Plane"}
        ],
        [
            {"id": "unclustered-performance-degradation", "label": "High-Cardinality Unclustered Scan", "changes": {"failedNodes": ["cluster-sorter"], "failedEdges": ["e3"]}, "root_cause": "Table was clustered on high-cardinality unique UUID instead of date/country.", "diverted_path": "Cluster blocks could not be pruned effectively; bytes scanned increased by 50x.", "blast_radius": "Slow query performance and higher costs.", "recovery": "Cluster tables on low-to-medium cardinality columns frequently used in WHERE or GROUP BY clauses."}
        ],
        # D3
        "Simulates Slot Saturation & Dynamic Reservation Autoscaling: unexpected concurrent ETL burst saturates 2,000 baseline slots; BigQuery Edition autoscaling allocates burst capacity.",
        "BigQuery Editions (Standard, Enterprise, Enterprise Plus) support dynamic slot autoscaling, seamlessly absorbing analytical query spikes without queueing delays.",
        [
            {"id": "g-etl-storm", "label": "Concurrent Analytical Burst (50 Queries)", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-slot-autoscale", "label": "BigQuery Enterprise Edition Slot Pool", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "concurrent-queries", "label": "50 Heavy Concurrent SQL Queries", "product": "Demanding 4,000 Slots Simultaneously", "group": "g-etl-storm", "plane": "data", "x": 220, "y": 140, "detail": "End-of-month financial reconciliation queries run concurrently with marketing ETL."},
            {"id": "slot-monitor-alert", "label": "Slot Utilization Sentinel", "product": "Baseline 2,000 Slots @ 100% Saturation", "group": "g-etl-storm", "plane": "control", "x": 220, "y": 280, "detail": "Queries begin queuing; execution wait times climb from 2s to 45s."},
            {"id": "slot-autoscaler", "label": "Enterprise Slot Autoscaler", "product": "Scales +1,500 Dynamic Slots", "group": "g-slot-autoscale", "plane": "control", "x": 700, "y": 140, "detail": "Automatically expands reservation pool from 2,000 to 3,500 slots in 10 seconds."},
            {"id": "unblocked-pipeline", "label": "Queued Queries Complete", "product": "Queue Cleared / P95 Latency Restored", "group": "g-slot-autoscale", "plane": "data", "x": 700, "y": 280, "detail": "All 50 queries execute in parallel; slots scale back down to 2,000 when workload clears."}
        ],
        [
            {"id": "e1", "from": "concurrent-queries", "to": "slot-monitor-alert", "label": "1. Saturate Baseline Slot Pool", "plane": "data"},
            {"id": "e2", "from": "slot-monitor-alert", "to": "slot-autoscaler", "label": "2. Trigger Slot Autoscaling Expansion", "plane": "control"},
            {"id": "e3", "from": "slot-autoscaler", "to": "unblocked-pipeline", "label": "3. Allocate Burst Slots & Clear Queue", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Saturation Detection", "edges": ["e1", "e2"], "action": "BigQuery detects query queue depth increasing and requests additional slots.", "why_traversal": "Prevents business-critical reporting deadlines from being missed.", "protocol": "Borg Slot Allocator", "plane": "Control Plane"},
            {"n": 2, "title": "Elastic Slot Scaling", "edges": ["e3"], "action": "Pool expands to 3,500 slots; queries finish in parallel; costs scale down automatically.", "why_traversal": "Balances high performance during peaks with cost predictability during idle periods.", "protocol": "BigQuery Reservation API", "plane": "Data Plane"}
        ],
        [
            {"id": "slot-cap-starvation", "label": "Hard Max Slots Cap Causes Indefinite Queueing", "changes": {"failedNodes": ["slot-autoscaler"], "failedEdges": ["e3"]}, "root_cause": "Administrator set max_slots cap to 2,000, preventing autoscaler from expanding.", "diverted_path": "Executive dashboard queries queued for 45 minutes during board meeting.", "blast_radius": "Delayed business decision-making.", "recovery": "Increase max_slots limit on Enterprise reservation or create dedicated high-priority reservation pool for Looker."}
        ]
    )

    # 052: Data Processing: Dataflow & Dataproc
    specs[52] = make_spec(
        52, "D.2", "Data Processing: Dataflow & Dataproc",
        "Visualizes Unified Data Processing Architecture: Cloud Dataflow (Apache Beam, Streaming Engine, auto-scaling) vs Cloud Dataproc (Managed Spark/Hadoop, Ephemeral clusters, Cloud Storage connector).",
        "Data processing architecture divides into serverless unified stream/batch (Cloud Dataflow with Apache Beam) vs open-source ecosystem compatibility (Cloud Dataproc running native Apache Spark, Hive, and Presto on ephemeral compute).",
        [
            {"id": "g-input-streams", "label": "Enterprise Streaming & Batch Ingestion", "type": "project", "scope": "global", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-dataflow-tier", "label": "Cloud Dataflow (Serverless Apache Beam)", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-dataproc-tier", "label": "Cloud Dataproc (Managed Apache Spark)", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "pubsub-stream", "label": "Real-Time Event Stream", "product": "Cloud Pub/Sub (100k msg/s)", "group": "g-input-streams", "plane": "data", "x": 140, "y": 140, "detail": "Continuous clickstream and IoT telemetry requiring sub-second windowed processing."},
            {"id": "gcs-raw-files", "label": "Historical Parquet Files", "product": "Cloud Storage Data Lake (50TB)", "group": "g-input-streams", "plane": "data", "x": 140, "y": 280, "detail": "Nightly batch logs stored in GCS buckets ready for ETL aggregation."},
            {"id": "dataflow-engine", "label": "Dataflow Streaming Engine", "product": "Exactly-Once Stateful Processing", "group": "g-dataflow-tier", "plane": "data", "x": 440, "y": 140, "detail": "Offloads state to dedicated backend; auto-scales worker fleet based on watermark lag."},
            {"id": "dataproc-cluster", "label": "Dataproc Ephemeral Cluster", "product": "Managed Spark / Hadoop (Spot VMs)", "group": "g-dataproc-tier", "plane": "data", "x": 780, "y": 140, "detail": "Spins up 100 Spot VM workers; runs 45-minute Spark job; auto-terminates upon completion."},
            {"id": "bigquery-sink", "label": "BigQuery Storage Write API", "product": "Unified Analytical Target", "group": "g-dataproc-tier", "plane": "data", "x": 780, "y": 280, "detail": "Direct streaming ingestion into partitioned tables with exactly-once delivery."}
        ],
        [
            {"id": "e1", "from": "pubsub-stream", "to": "dataflow-engine", "label": "1. Ingest Unbounded Stream", "plane": "data"},
            {"id": "e2", "from": "gcs-raw-files", "to": "dataproc-cluster", "label": "2. Ingest Nightly Parquet Batches", "plane": "data"},
            {"id": "e3", "from": "dataflow-engine", "to": "bigquery-sink", "label": "3. Stream Exactly-Once Windowed Results", "plane": "data"},
            {"id": "e4", "from": "dataproc-cluster", "to": "bigquery-sink", "label": "4. Write Transformed Analytics Tables", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Serverless Streaming & Ephemeral Batch Ingestion", "edges": ["e1", "e2"], "action": "Pub/Sub streams into Dataflow; Dataproc reads historical Parquet from GCS.", "why_traversal": "Applies the optimal compute runtime to each workload type.", "protocol": "Pub/Sub / GCS Connector", "plane": "Data Plane"},
            {"n": 2, "title": "Unified Analytics Delivery", "edges": ["e3", "e4"], "action": "Both pipelines persist transformed records into BigQuery tables with zero data duplication.", "why_traversal": "Creates unified analytical layer supporting real-time operational BI and historical reporting.", "protocol": "BigQuery Storage Write API", "plane": "Data Plane"}
        ],
        [
            {"id": "spot-vm-eviction-cascade", "label": "Dataproc Spot VM Eviction Outage", "changes": {"failedNodes": ["dataproc-cluster"], "failedEdges": ["e2", "e4"]}, "root_cause": "Dataproc cluster configured with 100% Spot VMs including master node; Google reclaimed master.", "diverted_path": "Cluster crashed mid-job; entire 4-hour batch job failed.", "blast_radius": "Delayed nightly financial reporting.", "recovery": "Configure standard persistent VMs for master and primary workers; use Spot VMs strictly for secondary task workers."}
        ],
        # D2
        "Traces Dataflow Streaming Engine Watermark Traversal: event-time windowing, handling late-arriving data, and emitting aggregated metrics to BigQuery.",
        "Event-time watermarking ensures calculations remain accurate even when mobile or IoT devices experience intermittent connectivity and submit delayed timestamps.",
        [
            {"id": "g-event-time-src", "label": "Unbounded Event Stream (Out of Order)", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-beam-windowing", "label": "Apache Beam Windowing & Watermark Engine", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-window-output", "label": "Aggregated Analytical Metrics", "type": "project", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "delayed-event", "label": "Event: 10:02 (Arrived at 10:08)", "product": "Delayed Mobile Telemetry", "group": "g-event-time-src", "plane": "data", "x": 140, "y": 200, "detail": "User clicked purchase in subway; event delayed by 6 minutes until cell signal returned."},
            {"id": "fixed-window", "label": "5-Minute Fixed Windows", "product": "Window [10:00 - 10:05)", "group": "g-beam-windowing", "plane": "control", "x": 440, "y": 140, "detail": "Groups events based on actual event timestamp rather than ingestion arrival time."},
            {"id": "watermark-eval", "label": "Watermark & Allowed Lateness", "product": "Allowed Lateness: 10 Minutes", "group": "g-beam-windowing", "plane": "control", "x": 440, "y": 280, "detail": "Tracks clock progress; accepts delayed 10:02 event and triggers window accumulation."},
            {"id": "bigquery-metric-row", "label": "BigQuery Sales Summary Row", "product": "Window [10:00 - 10:05] Revenue = $42,100", "group": "g-window-output", "plane": "data", "x": 780, "y": 200, "detail": "Updates window total with late event with exactly-once guarantee."}
        ],
        [
            {"id": "e1", "from": "delayed-event", "to": "fixed-window", "label": "1. Ingest Delayed Event", "plane": "data"},
            {"id": "e2", "from": "fixed-window", "to": "watermark-eval", "label": "2. Check Watermark & Lateness", "plane": "control"},
            {"id": "e3", "from": "watermark-eval", "to": "bigquery-metric-row", "label": "3. Emit Corrected Window Metric", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Event-Time Processing", "edges": ["e1", "e2"], "action": "Dataflow assigns event to [10:00-10:05) window based on click time, not arrival time.", "why_traversal": "Preserves analytical integrity regardless of network transmission latency.", "protocol": "Apache Beam Model", "plane": "Control Plane"},
            {"n": 2, "title": "Late Data Accumulation", "edges": ["e3"], "action": "Watermark acknowledges event falls within allowed lateness; updates BigQuery aggregate.", "why_traversal": "Eliminates inaccurate business metrics caused by delayed client submissions.", "protocol": "BigQuery Storage Write API", "plane": "Data Plane"}
        ],
        [
            {"id": "excessive-lateness-drop", "label": "Data Arrives Beyond Allowed Lateness", "changes": {"failedNodes": ["watermark-eval"], "failedEdges": ["e3"]}, "root_cause": "Event arrived 2 hours late; allowed lateness was configured for 10 minutes.", "diverted_path": "Event discarded; dropped counter incremented.", "blast_radius": "Slight metric undercounting.", "recovery": "Tune allowed lateness to balance memory state retention cost against data completeness."}
        ],
        # D3
        "Simulates Dataproc Cloud Storage Connector Throughput Bottleneck: demonstrates eliminating HDFS cluster storage by reading directly from GCS with ephemeral nodes.",
        "Decoupling storage from Dataproc clusters using the Google Cloud Storage connector eliminates 24/7 idle cluster costs and allows clusters to be ephemeral.",
        [
            {"id": "g-legacy-hdfs", "label": "Legacy Persistent HDFS Architecture", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-modern-ephemeral", "label": "Modern Ephemeral Dataproc + GCS", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "hdfs-datanode-waste", "label": "24/7 Running HDFS DataNodes", "product": "Billing $12,000/mo Idle Compute", "group": "g-legacy-hdfs", "plane": "data", "x": 220, "y": 140, "detail": "30 VMs kept running continuously merely to prevent HDFS data loss between jobs."},
            {"id": "hdfs-disk-full", "label": "HDFS Disk Space Full Alert", "product": "Storage Tied Directly to Compute", "group": "g-legacy-hdfs", "plane": "control", "x": 220, "y": 280, "detail": "Must provision expensive compute nodes whenever storage capacity runs low."},
            {"id": "gcs-connector-mount", "label": "Cloud Storage Connector (gcs://)", "product": "gs://analytics-lakehouse/data", "group": "g-modern-ephemeral", "plane": "data", "x": 700, "y": 140, "detail": "Spark reads directly from GCS buckets with petabit bandwidth at $0.020/GB/mo."},
            {"id": "ephemeral-auto-kill", "label": "Scheduled Ephemeral Cluster", "product": "Auto-Delete After 10 Min Idle", "group": "g-modern-ephemeral", "plane": "control", "x": 700, "y": 280, "detail": "Cluster boots, processes Spark job in 40 minutes, and terminates; compute cost drops by 80%."}
        ],
        [
            {"id": "e1", "from": "hdfs-datanode-waste", "to": "hdfs-disk-full", "label": "1. Storage Exhaustion Forces Scaling", "plane": "control"},
            {"id": "e2", "from": "hdfs-disk-full", "to": "gcs-connector-mount", "label": "2. Migrate HDFS Data to GCS", "plane": "control"},
            {"id": "e3", "from": "gcs-connector-mount", "to": "ephemeral-auto-kill", "label": "3. Run Ephemeral Spark Job & Terminate", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Storage Decoupling Migration", "edges": ["e1", "e2"], "action": "Migrates data from on-cluster HDFS disks to durable Cloud Storage buckets.", "why_traversal": "Decouples storage pricing from compute instance lifecycles.", "protocol": "DistCp over Interconnect", "plane": "Control Plane"},
            {"n": 2, "title": "Ephemeral Compute Execution", "edges": ["e3"], "action": "Dataproc spins up Spot workers, reads from GCS, writes output, and auto-destroys.", "why_traversal": "Eliminates $12,000/month in idle compute waste while providing infinite storage scaling.", "protocol": "Google Cloud Storage Connector", "plane": "Data Plane"}
        ],
        [
            {"id": "gcs-rename-performance-trap", "label": "Spark HDFS Directory Rename Bottleneck on GCS", "changes": {"failedNodes": ["gcs-connector-mount"], "failedEdges": ["e3"]}, "root_cause": "Spark job executed thousands of directory renames; GCS emulates renames via slow copy-and-delete operations.", "diverted_path": "Job completion stalled for 45 minutes during output commit phase.", "blast_radius": "Delayed batch pipeline completion.", "recovery": "Enable the Cloud Storage Direct Commit or FileOutputCommitter v2 in Dataproc Spark configuration."}
        ]
    )

    # 053: Enterprise Data Lake with BigLake & Dataplex Governance
    specs[53] = make_spec(
        53, "D.3", "Data Lake, Lakehouse & BigLake",
        "Visualizes Governed Enterprise Lakehouse Architecture: Cloud Storage, AWS S3, and Azure Blob multi-cloud data lakes unified via BigLake, open table formats (Iceberg, Delta, Hudi), and Dataplex centralized data mesh governance.",
        "BigLake unifies data warehouses and data lakes into a single governed lakehouse: query open table formats directly in Cloud Storage or multi-cloud buckets with BigQuery performance while enforcing fine-grained row- and column-level security through Dataplex.",
        [
            {"id": "g-multicloud-storage", "label": "Multi-Cloud Storage Tier (GCS / S3)", "type": "project", "scope": "global", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-biglake-engine", "label": "BigLake Storage Engine & Open Formats", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-dataplex-mesh", "label": "Dataplex Centralized Data Governance", "type": "organization", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "gcs-iceberg", "label": "GCS Apache Iceberg Tables", "product": "Open Table Format (Parquet)", "group": "g-multicloud-storage", "plane": "data", "x": 140, "y": 140, "detail": "ACID transactions and partition evolution on top of Cloud Storage object files."},
            {"id": "aws-s3-lake", "label": "AWS S3 / Azure Blob Storage", "product": "External Cloud Lake Data", "group": "g-multicloud-storage", "plane": "data", "x": 140, "y": 280, "detail": "Petabytes of operational logs in AWS S3 queried in-place via BigQuery Omni."},
            {"id": "biglake-connector", "label": "BigLake Metastore & Connector", "product": "BigQuery Omni & Storage API", "group": "g-biglake-engine", "plane": "data", "x": 440, "y": 200, "detail": "Executes SQL directly on open files without data duplication or cross-cloud egress fees."},
            {"id": "dataplex-catalog", "label": "Dataplex Data Mesh Catalog", "product": "Automated Metadata Discovery", "group": "g-dataplex-mesh", "plane": "control", "x": 780, "y": 140, "detail": "Discovers schemas, manages data lineage, and classifies sensitive data across lakes."},
            {"id": "fine-grained-sec", "label": "Row / Column Security Policy", "product": "Policy Tags & Dynamic Masking", "group": "g-dataplex-mesh", "plane": "control", "x": 780, "y": 280, "detail": "Masks credit card columns and filters rows based on caller IAM department."}
        ],
        [
            {"id": "e1", "from": "gcs-iceberg", "to": "biglake-connector", "label": "1. Read Iceberg Parquet Tables", "plane": "data"},
            {"id": "e2", "from": "aws-s3-lake", "to": "biglake-connector", "label": "2. Query S3 via BigQuery Omni", "plane": "data"},
            {"id": "e3", "from": "biglake-connector", "to": "dataplex-catalog", "label": "3. Register Discovered Assets", "plane": "control"},
            {"id": "e4", "from": "dataplex-catalog", "to": "fine-grained-sec", "label": "4. Enforce Access Policy Tags", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Federated Multi-Cloud In-Place Querying", "edges": ["e1", "e2"], "action": "BigLake executes SQL queries over GCS Iceberg tables and AWS S3 in-place.", "why_traversal": "Eliminates multi-million dollar data egress costs and avoids vendor lock-in.", "protocol": "BigQuery Omni / Parquet Read", "plane": "Data Plane"},
            {"n": 2, "title": "Centralized Governance & Masking", "edges": ["e3", "e4"], "action": "Dataplex catalogs data assets and applies dynamic data masking to sensitive columns.", "why_traversal": "Ensures uniform compliance and security across diverse multi-cloud analytical assets.", "protocol": "Dataplex Policy Engine", "plane": "Control Plane"}
        ],
        [
            {"id": "unmasked-column-leak", "label": "Missing Policy Tag Exposes SSN Column", "changes": {"failedNodes": ["fine-grained-sec"], "failedEdges": ["e4"]}, "root_cause": "New table schema added 'social_security_num' column without applying Dataplex policy tag.", "diverted_path": "Marketing analyst queried raw table and viewed customer SSNs.", "blast_radius": "Privacy compliance breach.", "recovery": "Automate policy tag inheritance in Dataplex so new sensitive columns are masked by default."}
        ],
        # D2
        "Traces Multi-Cloud BigLake Federated Query Flow: analyst submits single SQL join -> BigQuery Omni runs local compute in AWS S3 -> joins with GCP Iceberg -> streams unified result.",
        "BigQuery Omni executes compute natively within AWS and Azure facilities, sending only the final aggregated result rows across cloud boundaries.",
        [
            {"id": "g-analyst-console", "label": "BigQuery Studio / BI Analyst", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-omni-aws-exec", "label": "BigQuery Omni Cluster (Inside AWS)", "type": "external", "scope": "external", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-gcp-join-tier", "label": "BigQuery Lakehouse (Inside GCP)", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "federated-sql", "label": "Federated Multi-Cloud SQL", "product": "SELECT * FROM aws_s3 JOIN gcs_table", "group": "g-analyst-console", "plane": "control", "x": 140, "y": 200, "detail": "Analyst writes standard SQL joining AWS order logs with GCP customer records."},
            {"id": "omni-aws-worker", "label": "BigQuery Omni (AWS us-east-1)", "product": "Local Compute Slots in AWS", "group": "g-omni-aws-exec", "plane": "data", "x": 440, "y": 200, "detail": "Reads 10TB of S3 Parquet data locally; filters down to 50KB summary result."},
            {"id": "cross-cloud-summary", "label": "Compact 50KB Cross-Cloud Egress", "product": "Zero Egress Bill Shock", "group": "g-gcp-join-tier", "plane": "data", "x": 780, "y": 140, "detail": "Transfers only the 50KB aggregated summary from AWS to GCP over TLS."},
            {"id": "final-joined-result", "label": "Unified Analytical View", "product": "Returned to Analyst in 2.8s", "group": "g-gcp-join-tier", "plane": "data", "x": 780, "y": 280, "detail": "Final joined dataset delivered to dashboard with zero multi-terabyte egress charges."}
        ],
        [
            {"id": "e1", "from": "federated-sql", "to": "omni-aws-worker", "label": "1. Dispatch Local Compute to AWS", "plane": "control"},
            {"id": "e2", "from": "omni-aws-worker", "to": "cross-cloud-summary", "label": "2. Egress Only Compact Summary", "plane": "data"},
            {"id": "e3", "from": "cross-cloud-summary", "to": "final-joined-result", "label": "3. Join with Local GCP Lakehouse", "plane": "data"}
        ],
        [
            {"n": 1, "title": "In-Region Compute Execution", "edges": ["e1", "e2"], "action": "BigQuery Omni runs compute inside AWS, reducing 10TB of raw files to 50KB.", "why_traversal": "Eliminates AWS internet data egress charges ($900 saved on single query).", "protocol": "BigQuery Omni Worker Protocol", "plane": "Control Plane"},
            {"n": 2, "title": "Seamless Cross-Cloud Join", "edges": ["e3"], "action": "BigQuery joins compact AWS summary with GCP customer data in memory.", "why_traversal": "Enables multi-cloud analytics without complex ETL pipelines.", "protocol": "BigQuery Dremel Join", "plane": "Data Plane"}
        ],
        [
            {"id": "cross-cloud-iam-role-expiry", "label": "AWS IAM Role Expiration Drops Query", "changes": {"failedNodes": ["omni-aws-worker"], "failedEdges": ["e2"]}, "root_cause": "The AWS IAM role assumed by Google Cloud STS expired after 12 hours.", "diverted_path": "Query fails with AWS AccessDenied.", "blast_radius": "Scheduled hourly multi-cloud dashboard fails.", "recovery": "Configure automated AWS IAM role trust policy renewal with Google Cloud identity federation."}
        ],
        # D3
        "Simulates Dataplex Data Quality & Quarantine Pipeline: automated data profiling catches 15% missing null values and diverts dirty data into quarantine bucket.",
        "Dataplex automated data quality tasks inspect analytical datasets before downstream consumption, quarantining bad data to prevent corrupting executive dashboards.",
        [
            {"id": "g-raw-land-zone", "label": "Incoming Data Batch Landing Zone", "type": "project", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-dataplex-guard", "label": "Dataplex Quality & Quarantine Engine", "type": "organization", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "corrupted-csv-batch", "label": "Corrupted Vendor CSV Upload", "product": "Null Customer_ID in 15% of Rows", "group": "g-raw-land-zone", "plane": "data", "x": 220, "y": 140, "detail": "Third-party vendor uploaded daily sales batch missing primary key values."},
            {"id": "dataplex-profiler", "label": "Dataplex Auto Data Profiling", "product": "Quality Rule: Customer_ID NOT NULL", "group": "g-raw-land-zone", "plane": "control", "x": 220, "y": 280, "detail": "Profiles batch; detects 15% null values violating quality rule DQ_089."},
            {"id": "quarantine-bucket", "label": "Quarantine Bucket (GCS)", "product": "gs://analytics-lake/quarantine/", "group": "g-dataplex-guard", "plane": "data", "x": 700, "y": 140, "detail": "Isolates rejected records and alerts vendor data engineering team in Slack."},
            {"id": "clean-lakehouse-table", "label": "Clean Production Lakehouse", "product": "100% Validated Clean Data", "group": "g-dataplex-guard", "plane": "data", "x": 700, "y": 280, "detail": "Downstream executive dashboards only ingest 100% verified clean data."}
        ],
        [
            {"id": "e1", "from": "corrupted-csv-batch", "to": "dataplex-profiler", "label": "1. Scan Upload for Quality Rules", "plane": "control"},
            {"id": "e2", "from": "dataplex-profiler", "to": "quarantine-bucket", "label": "2. Divert Corrupted Records to Quarantine", "plane": "data"},
            {"id": "e3", "from": "dataplex-profiler", "to": "clean-lakehouse-table", "label": "3. Promote Clean Verified Records", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Automated Quality Profiling", "edges": ["e1", "e2"], "action": "Dataplex inspects rows against declarative rules and catches 15% null violations.", "why_traversal": "Prevents dirty data from contaminating downstream analytics.", "protocol": "Dataplex Data Quality Task", "plane": "Control Plane"},
            {"n": 2, "title": "Quarantine & Clean Ingestion", "edges": ["e3"], "action": "Diverts corrupt rows to quarantine while allowing valid records to proceed to BigQuery.", "why_traversal": "Maintains pipeline flow without halting entire enterprise data ingestion.", "protocol": "Cloud Storage Object Routing", "plane": "Data Plane"}
        ],
        [
            {"id": "unquarantined-bad-data", "label": "Dirty Data Corrupts Executive Revenue Dashboard", "changes": {"failedNodes": ["clean-lakehouse-table"], "failedEdges": ["e3"]}, "root_cause": "Quality check was configured in 'alert only' mode without active quarantine routing.", "diverted_path": "Corrupt null records loaded into production; revenue reports showed 15% false dip.", "blast_radius": "C-suite alarmed by false financial drop.", "recovery": "Enable automated quarantine routing in Dataplex quality task definitions."}
        ]
    )

    # 054: Production ML Platform with Vertex AI & Feature Store
    specs[54] = make_spec(
        54, "D.4", "Machine Learning: Vertex AI Architecture",
        "Visualizes Production MLOps Architecture: BigQuery source data, Vertex AI Feature Store (low-latency online serving + batch training), Vertex AI Pipelines (Kubeflow), Model Registry, and Autoscaling Prediction Endpoints with GPU/TPU accelerators.",
        "Production MLOps requires treating machine learning like software engineering: feature stores eliminate training-serving skew, automated pipelines retrain models on concept drift, and model registries enforce governance before deployment.",
        [
            {"id": "g-feature-lake", "label": "Data & Feature Engineering Tier", "type": "project", "scope": "global", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-mlops-pipeline", "label": "Vertex AI Continuous Training (Pipelines)", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-serving-endpoints", "label": "Vertex AI Model Serving & Monitoring", "type": "project", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "feature-store", "label": "Vertex AI Feature Store", "product": "Sub-10ms Online Feature Serving", "group": "g-feature-lake", "plane": "data", "x": 140, "y": 140, "detail": "Serves real-time customer behavioral features (e.g. 7-day spend, last login time)."},
            {"id": "bq-training-data", "label": "BigQuery Training Set", "product": "Point-in-Time Accurate Features", "group": "g-feature-lake", "plane": "data", "x": 140, "y": 280, "detail": "Generates training datasets with point-in-time joins to eliminate data leakage."},
            {"id": "kfp-pipeline", "label": "Vertex AI Pipelines (Kubeflow)", "product": "Automated Model Training DAG", "group": "g-mlops-pipeline", "plane": "control", "x": 440, "y": 140, "detail": "Orchestrates data prep, model training on A100 GPUs, and evaluation metrics."},
            {"id": "model-registry", "label": "Vertex AI Model Registry", "product": "Versioned Model Governance", "group": "g-mlops-pipeline", "plane": "control", "x": 440, "y": 280, "detail": "Tracks model versions (v1.0, v1.1), metrics, and approval status before rollout."},
            {"id": "prediction-endpoint", "label": "Vertex Prediction Endpoint", "product": "Autoscaling GPU/TPU Service", "group": "g-serving-endpoints", "plane": "data", "x": 780, "y": 140, "detail": "Serves real-time online inference with sub-15ms p99 response times."},
            {"id": "drift-monitor", "label": "Vertex Model Monitoring", "product": "Feature Skew & Drift Detection", "group": "g-serving-endpoints", "plane": "control", "x": 780, "y": 280, "detail": "Calculates distance between serving features and training baseline; triggers retrain."}
        ],
        [
            {"id": "e1", "from": "bq-training-data", "to": "kfp-pipeline", "label": "1. Ingest Point-in-Time Features", "plane": "data"},
            {"id": "e2", "from": "kfp-pipeline", "to": "model-registry", "label": "2. Register Validated Model", "plane": "control"},
            {"id": "e3", "from": "model-registry", "to": "prediction-endpoint", "label": "3. Deploy to GPU Endpoint", "plane": "control"},
            {"id": "e4", "from": "feature-store", "to": "prediction-endpoint", "label": "4. Enrich Inference with Online Features", "plane": "data"},
            {"id": "e5", "from": "prediction-endpoint", "to": "drift-monitor", "label": "5. Monitor Prediction Requests for Drift", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Continuous Training & Registration", "edges": ["e1", "e2", "e3"], "action": "Pipeline trains model on GPU cluster, validates accuracy, and deploys to endpoint.", "why_traversal": "Automates machine learning deployment with strict governance controls.", "protocol": "Kubeflow Pipeline / REST API", "plane": "Control Plane"},
            {"n": 2, "title": "Real-Time Inference & Drift Supervision", "edges": ["e4", "e5"], "action": "Endpoint fetches live features from Feature Store in 4ms; Model Monitoring watches for drift.", "why_traversal": "Eliminates training-serving skew and guarantees long-term model accuracy.", "protocol": "gRPC Online Prediction", "plane": "Data Plane"}
        ],
        [
            {"id": "concept-drift-accuracy-collapse", "label": "Undetected Concept Drift Degrades Fraud Detection", "changes": {"failedNodes": ["prediction-endpoint"], "failedEdges": ["e5"]}, "root_cause": "Attacker changed fraud patterns; model accuracy dropped from 94% to 52% over 3 weeks.", "diverted_path": "Model continued approving fraudulent transactions due to disabled Model Monitoring.", "blast_radius": "$450,000 in fraudulent transaction losses.", "recovery": "Enable Vertex AI Model Monitoring with automated email alerting and automated retraining triggers."}
        ],
        # D2
        "Traces Real-Time Online Inference Flow: client mobile app request -> API Gateway -> Vertex AI Prediction Endpoint -> Feature Store online lookup -> inference return.",
        "Online feature lookup decouples the mobile client from feature computation: client sends user ID, and Vertex AI enriches the payload with 50 engineered features in 3 milliseconds.",
        [
            {"id": "g-client-inference", "label": "Customer Mobile Client", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-serving-cluster", "label": "Vertex AI Serving Infrastructure", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-online-feature-vault", "label": "Low-Latency Online Feature Store", "type": "project", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "mobile-checkout", "label": "Checkout: $340 Cart", "product": "User: u8921 / Merchant: m440", "group": "g-client-inference", "plane": "data", "x": 140, "y": 200, "detail": "User attempts transaction; app requests real-time fraud risk score."},
            {"id": "vertex-serving-pod", "label": "Vertex Prediction Worker", "product": "XGBoost Fraud Model (v2.1)", "group": "g-serving-cluster", "plane": "data", "x": 440, "y": 200, "detail": "Runs scoring algorithm in 2.2ms on dedicated container runtime."},
            {"id": "online-feature-table", "label": "Feature Store Online Entity", "product": "Bigtable-Backed Online Store", "group": "g-online-feature-vault", "plane": "data", "x": 780, "y": 140, "detail": "Stores entity u8921: 24h_fail_count: 0, 7d_avg_spend: $310, account_age: 412d."},
            {"id": "fraud-score-result", "label": "Fraud Score: 0.02 (Approved)", "product": "Inference Total Latency: 14ms", "group": "g-serving-cluster", "plane": "data", "x": 440, "y": 290, "detail": "Returns transaction approval token to mobile app in 14ms."}
        ],
        [
            {"id": "e1", "from": "mobile-checkout", "to": "vertex-serving-pod", "label": "1. POST /predict (user_id: u8921)", "plane": "data"},
            {"id": "e2", "from": "vertex-serving-pod", "to": "online-feature-table", "label": "2. Read Online Entity Features (3ms)", "plane": "data"},
            {"id": "e3", "from": "online-feature-table", "to": "vertex-serving-pod", "label": "3. Return 50 Feature Values", "plane": "data"},
            {"id": "e4", "from": "vertex-serving-pod", "to": "fraud-score-result", "label": "4. Output Approved Decision", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Online Feature Enrichment", "edges": ["e1", "e2", "e3"], "action": "Prediction worker retrieves customer features from Feature Store in 3ms.", "why_traversal": "Eliminates need for mobile client to compute or pass complex feature histories.", "protocol": "gRPC Entity Lookup", "plane": "Data Plane"},
            {"n": 2, "title": "Low-Latency Fraud Scoring", "edges": ["e4"], "action": "Model evaluates 50 features and outputs fraud probability of 0.02 in 2.2ms.", "why_traversal": "Secures financial transaction without adding perceptible friction to checkout.", "protocol": "Vertex AI Prediction Protocol", "plane": "Data Plane"}
        ],
        [
            {"id": "feature-staleness-drift", "label": "Batch Feature Sync Lag Causes False Rejections", "changes": {"failedNodes": ["online-feature-table"], "failedEdges": ["e3"]}, "root_cause": "Hourly streaming ingestion to Feature Store failed, causing customer spend features to be stale.", "diverted_path": "Model rejected valid customer purchases.", "blast_radius": "Customer checkout abandonment.", "recovery": "Transition to real-time streaming feature ingestion using Vertex AI Feature Store streaming write API."}
        ],
        # D3
        "Simulates Automated Model Retraining Triggered by Drift Alert: Vertex Model Monitoring detects feature drift exceeding Kolmogorov-Smirnov statistical threshold and triggers Kubeflow pipeline retraining.",
        "Continuous machine learning requires closed-loop automation: monitoring drift automatically launches retraining pipelines, producing freshly calibrated models with zero human intervention.",
        [
            {"id": "g-drift-alert-src", "label": "Model Monitoring & Drift Detection", "type": "project", "scope": "global", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-retrain-pipeline", "label": "Automated Retraining & Champion-Challenger Rollout", "type": "vpc", "scope": "regional", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "drift-detected-alert", "label": "Feature Drift Alert (p < 0.01)", "product": "Distance: 0.18 > Threshold: 0.10", "group": "g-drift-alert-src", "plane": "control", "x": 220, "y": 140, "detail": "Statistical test confirms production input feature distribution has shifted from training data."},
            {"id": "eventarc-retrain-trigger", "label": "Eventarc Pipeline Trigger", "product": "Triggers Cloud Function", "group": "g-drift-alert-src", "plane": "control", "x": 220, "y": 280, "detail": "Receives drift alert and launches Vertex AI Pipeline job with latest 30-day BigQuery dataset."},
            {"id": "kfp-retrain-run", "label": "Kubeflow Pipeline Execution", "product": "Trains Challenger Model v2.2", "group": "g-retrain-pipeline", "plane": "control", "x": 700, "y": 140, "detail": "Retrains on modern feature distribution; confirms accuracy 95.2% exceeds v2.1 baseline."},
            {"id": "champion-traffic-split", "label": "Canary Traffic Promotion", "product": "Traffic Split: 90% v2.1 / 10% v2.2", "group": "g-retrain-pipeline", "plane": "data", "x": 700, "y": 280, "detail": "Promotes newly retrained model as challenger canary; shifts 100% traffic once verified."}
        ],
        [
            {"id": "e1", "from": "drift-detected-alert", "to": "eventarc-retrain-trigger", "label": "1. Fire Drift Breach Notification", "plane": "control"},
            {"id": "e2", "from": "eventarc-retrain-trigger", "to": "kfp-retrain-run", "label": "2. Launch Vertex Retraining Pipeline", "plane": "control"},
            {"id": "e3", "from": "kfp-retrain-run", "to": "champion-traffic-split", "label": "3. Deploy Challenger Model to Endpoint", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Automated Drift Triggering", "edges": ["e1", "e2"], "action": "Model Monitoring identifies distribution shift and launches training DAG automatically.", "why_traversal": "Eliminates model performance degradation without requiring manual data science audits.", "protocol": "Eventarc / Cloud Functions", "plane": "Control Plane"},
            {"n": 2, "title": "Champion-Challenger Canary Deployment", "edges": ["e3"], "action": "New model deployed as canary; endpoint splits traffic to safely validate accuracy on live users.", "why_traversal": "Guarantees retrained models perform safely in production before full cutover.", "protocol": "Vertex AI Traffic Splitting", "plane": "Data Plane"}
        ],
        [
            {"id": "pipeline-gpu-quota-fail", "label": "Retraining Fails Due to GPU Quota Exhaustion", "changes": {"failedNodes": ["kfp-retrain-run"], "failedEdges": ["e3"]}, "root_cause": "Pipeline requested 8x NVIDIA A100 GPUs, but regional quota was capped at 4.", "diverted_path": "Retraining job queued indefinitely; stale model continued degrading.", "blast_radius": "Model accuracy decayed for another 2 weeks.", "recovery": "Pre-allocate dedicated Vertex AI Custom Job GPU reservation or fallback to CPU training."}
        ]
    )

    # 055: Compute Decision Cheat Sheet
    specs[55] = make_spec(
        55, "CS.1", "Compute Decision Cheat Sheet",
        "Visualizes PCA Compute Decision Framework: Compute Engine (Bare VMs, custom kernels, GPUs, stateful) vs GKE (Microservices, complex container orchestration, Agones) vs Cloud Run (Stateless HTTP/gRPC, scale-to-zero, fast dev) vs Cloud Functions (Event handlers, light glue code).",
        "Mastering Google Cloud compute selection requires evaluating three core dimensions: abstraction level (IaaS vs CaaS vs FaaS), scaling characteristics (scale-to-zero vs pre-warmed), and protocol support (HTTP vs raw TCP/UDP).",
        [
            {"id": "g-workload-profile", "label": "Workload Architecture Constraints", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-serverless-tier", "label": "Serverless Compute (Zero Ops)", "type": "project", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-infra-tier", "label": "Container & Infrastructure Compute", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "req-stateless-http", "label": "Stateless HTTP / gRPC Container?", "product": "Containerized Request-Response", "group": "g-workload-profile", "plane": "control", "x": 140, "y": 140, "detail": "Standard microservices responding to web and mobile API requests."},
            {"id": "req-heavy-infra", "label": "Custom OS / Raw TCP / Bare Metal?", "product": "Non-HTTP / Complex Cluster", "group": "g-workload-profile", "plane": "control", "x": 140, "y": 280, "detail": "Legacy Windows, kernel modules, high-performance computing, or game servers."},
            {"id": "cloud-run-pick", "label": "Cloud Run (First Choice)", "product": "Fully Managed Serverless Container", "group": "g-serverless-tier", "plane": "data", "x": 440, "y": 140, "detail": "Fastest time-to-market; scales from 0 to 1,000 instances; zero cluster maintenance."},
            {"id": "cloud-fn-pick", "label": "Cloud Functions (2nd Gen)", "product": "Eventarc Single-Purpose Glue Code", "group": "g-serverless-tier", "plane": "data", "x": 440, "y": 280, "detail": "Lightweight event handlers triggered by Cloud Storage uploads or Pub/Sub events."},
            {"id": "gke-autopilot-pick", "label": "GKE Autopilot", "product": "Managed Kubernetes Orchestration", "group": "g-infra-tier", "plane": "data", "x": 780, "y": 140, "detail": "Complex multi-container pods, stateful workloads, service mesh, and custom networking."},
            {"id": "gce-mig-pick", "label": "Compute Engine MIGs", "product": "IaaS Virtual Machine Fleets", "group": "g-infra-tier", "plane": "data", "x": 780, "y": 280, "detail": "Full root access, custom kernel extensions, Windows Server, and local NVMe SSDs."}
        ],
        [
            {"id": "e1", "from": "req-stateless-http", "to": "cloud-run-pick", "label": "1. Yes -> Route to Cloud Run", "plane": "control"},
            {"id": "e2", "from": "req-stateless-http", "to": "cloud-fn-pick", "label": "2. Single Event Handler -> Cloud Functions", "plane": "control"},
            {"id": "e3", "from": "req-heavy-infra", "to": "gke-autopilot-pick", "label": "3. Complex Container Ecosystem -> GKE", "plane": "control"},
            {"id": "e4", "from": "req-heavy-infra", "to": "gce-mig-pick", "label": "4. Monolith / Custom OS -> Compute Engine", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Serverless-First Evaluation", "edges": ["e1", "e2"], "action": "Google recommends Cloud Run as default compute for all containerized HTTP services.", "why_traversal": "Delivers highest developer velocity and lowest total cost of ownership.", "protocol": "Decision Rubric", "plane": "Control Plane"},
            {"n": 2, "title": "Orchestration & Infrastructure Path", "edges": ["e3", "e4"], "action": "Non-HTTP, multi-container, or stateful systems route to GKE Autopilot or Compute Engine.", "why_traversal": "Provides granular infrastructure control when serverless constraints are breached.", "protocol": "Infrastructure Sizing", "plane": "Control Plane"}
        ],
        [
            {"id": "wrong-compute-cost-penalty", "label": "Selected Compute Engine for Idle Microservice", "changes": {"failedNodes": ["gce-mig-pick"], "failedEdges": ["e4"]}, "root_cause": "Deployed low-traffic internal webhook on 3 always-on Compute Engine VMs.", "diverted_path": "Cost $220/month for 15 requests/day; Cloud Run would have cost $0.00/month.", "blast_radius": "Unnecessary ongoing cloud expenditure.", "recovery": "Migrate stateless idle microservices to Cloud Run scale-to-zero."}
        ],
        # D2
        "Traces Step-by-Step Compute Selection Flow: question prompt analysis -> container status -> protocol check -> execution duration -> optimal compute product.",
        "Following the structured compute decision tree eliminates hesitation on exam scenarios.",
        [
            {"id": "g-input-check", "label": "Step 1: Container & Protocol Check", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-scaling-check", "label": "Step 2: Operational Overhead & Scaling", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-final-verdict", "label": "Step 3: Optimal Compute SKU Selection", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "q-check-container", "label": "Is Application Containerized?", "product": "OCI Container Image Available", "group": "g-input-check", "plane": "control", "x": 140, "y": 140, "detail": "Yes: Application packaged as Docker container."},
            {"id": "q-check-protocol", "label": "Protocol: HTTP/gRPC or Custom TCP?", "product": "HTTPS REST API Endpoint", "group": "g-input-check", "plane": "control", "x": 140, "y": 280, "detail": "Responds to HTTPS webhooks within 60 minutes."},
            {"id": "q-check-ops", "label": "Operational Requirement: Minimal Ops", "product": "No Cluster or OS Management", "group": "g-scaling-check", "plane": "control", "x": 440, "y": 200, "detail": "Eliminates GKE Standard and Compute Engine due to node maintenance."},
            {"id": "verdict-cloud-run", "label": "Result: Cloud Run Fully Managed", "product": "Winner: 100% Constraint Match", "group": "g-final-verdict", "plane": "data", "x": 780, "y": 200, "detail": "Optimal GCP compute choice meeting all requirements with zero idle cost."}
        ],
        [
            {"id": "e1", "from": "q-check-container", "to": "q-check-protocol", "label": "1. Confirmed Containerized", "plane": "control"},
            {"id": "e2", "from": "q-check-protocol", "to": "q-check-ops", "label": "2. Confirmed HTTPS Protocol", "plane": "control"},
            {"id": "e3", "from": "q-check-ops", "to": "verdict-cloud-run", "label": "3. Confirmed Minimal Ops Requirement", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Constraint Verification", "edges": ["e1", "e2"], "action": "Verifies containerization and protocol compatibility.", "why_traversal": "Quickly filters out incompatible runtimes.", "protocol": "Decision Filter", "plane": "Control Plane"},
            {"n": 2, "title": "Final Selection", "edges": ["e3"], "action": "Applies operational filter: selects Cloud Run as winning product.", "why_traversal": "Aligns with PCA exam scoring rubric.", "protocol": "PCA Answer Key", "plane": "Data Plane"}
        ],
        [
            {"id": "batch-duration-timeout", "label": "Workload Exceeds 60-Minute Cloud Run Timeout", "changes": {"failedNodes": ["verdict-cloud-run"], "failedEdges": ["e3"]}, "root_cause": "Job was an 8-hour batch video render; Cloud Run killed execution at 60-minute limit.", "diverted_path": "Batch jobs aborted mid-stream.", "blast_radius": "Application failure.", "recovery": "Route long-running batch jobs to Cloud Batch or Cloud Run Jobs with extended execution timeouts."}
        ],
        # D3
        "Simulates Compute Migration: migrating legacy monolithic Compute Engine VM into Cloud Run container, eliminating OS patching overhead and reducing idle cloud spend.",
        "Refactoring stateless legacy VMs to Cloud Run eliminates administrative operating system patching while enabling automated scale-to-zero.",
        [
            {"id": "g-legacy-vm-tier", "label": "Legacy Monolithic Compute Engine VM", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-modern-run-tier", "label": "Modernized Serverless Cloud Run", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "unpatched-gce-vm", "label": "Legacy e2-standard-4 VM", "product": "Status: 18 Kernel CVEs Pending", "group": "g-legacy-vm-tier", "plane": "data", "x": 220, "y": 140, "detail": "Requires manual weekly OS patching, firewall rule maintenance, and disk resizing."},
            {"id": "idle-vm-burn", "label": "24/7 Compute Billing Burn", "product": "Cost: $118/Month (Even at 0 QPS)", "group": "g-legacy-vm-tier", "plane": "control", "x": 220, "y": 280, "detail": "Runs 24/7 despite receiving zero traffic between 6 PM and 8 AM."},
            {"id": "containerized-run", "label": "Cloud Run Microservice", "product": "Zero OS Management / Zero CVEs", "group": "g-modern-run-tier", "plane": "data", "x": 700, "y": 140, "detail": "Runs application container on Google-managed hardened gVisor sandbox."},
            {"id": "scale-to-zero-savings", "label": "Scale-to-Zero Cost Model", "product": "Cost: $4.20/Month (96% Savings)", "group": "g-modern-run-tier", "plane": "control", "x": 700, "y": 280, "detail": "Scales to zero instances during idle night hours; wakes up in 150ms on incoming request."}
        ],
        [
            {"id": "e1", "from": "unpatched-gce-vm", "to": "containerized-run", "label": "1. Containerize App via Buildpacks", "plane": "control"},
            {"id": "e2", "from": "idle-vm-burn", "to": "scale-to-zero-savings", "label": "2. Flip Traffic to Scale-to-Zero", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Modernization & Containerization", "edges": ["e1"], "action": "Cloud Buildpacks packages application into container without requiring Dockerfile.", "why_traversal": "Eliminates operating system patching responsibility permanently.", "protocol": "Cloud Buildpacks", "plane": "Control Plane"},
            {"n": 2, "title": "Financial Optimization", "edges": ["e2"], "action": "Cloud Run scales to zero during off-hours, slashing monthly infrastructure bill by 96%.", "why_traversal": "Frees up engineering time from server maintenance to feature development.", "protocol": "Cloud Run Admin API", "plane": "Control Plane"}
        ],
        [
            {"id": "cold-start-latency-spike", "label": "Cold Start Latency Impacts Morning Users", "changes": {"failedNodes": ["scale-to-zero-savings"], "failedEdges": ["e2"]}, "root_cause": "Heavy Java Spring Boot container took 12 seconds to initialize from 0 instances at 8 AM.", "diverted_path": "First morning customer requests timed out.", "blast_radius": "Morning user frustration.", "recovery": "Set min-instances=1 on Cloud Run to maintain a pre-warmed instance during business hours."}
        ]
    )

    # 056: Database Decision Cheat Sheet
    specs[56] = make_spec(
        56, "CS.2", "Database Decision Cheat Sheet",
        "Visualizes PCA Database Selection Matrix: Relational (Cloud SQL, AlloyDB, Cloud Spanner) vs NoSQL Key-Value/Document (Firestore, Bigtable, Memorystore) evaluated across SQL support, ACID transaction scope, scaling limits, and global availability.",
        "Choosing a Google Cloud database requires systematic constraint mapping: Relational vs NoSQL? Single-region vs Multi-region? Read-heavy caching vs Petabyte write-heavy streaming? Knowing the exact boundaries prevents costly architectural re-platforming.",
        [
            {"id": "g-db-model-choice", "label": "Data Model & Query Semantics", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-relational-tier", "label": "Relational SQL Tier (ACID)", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-nosql-tier", "label": "NoSQL High-Throughput Tier", "type": "project", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "need-sql", "label": "Relational SQL Required?", "product": "Joins, Foreign Keys, Complex SQL", "group": "g-db-model-choice", "plane": "control", "x": 140, "y": 140, "detail": "Existing schema requires strict relational integrity and complex multi-table joins."},
            {"id": "need-nosql", "label": "NoSQL / High Volume Required?", "product": "Millions of QPS / Flexible Schema", "group": "g-db-model-choice", "plane": "control", "x": 140, "y": 280, "detail": "Massive horizontal scale, document hierarchy, or sub-10ms key-value lookups."},
            {"id": "spanner-db-choice", "label": "Cloud Spanner Multi-Region", "product": "Global SQL (99.999% SLA)", "group": "g-relational-tier", "plane": "data", "x": 440, "y": 140, "detail": "Horizontal scaling, multi-region external consistency, limitless storage capacity."},
            {"id": "cloudsql-choice", "label": "Cloud SQL / AlloyDB", "product": "Regional Managed SQL (Max 64TB)", "group": "g-relational-tier", "plane": "data", "x": 440, "y": 280, "detail": "Drop-in PostgreSQL, MySQL, SQL Server compatibility; automatic HA failover."},
            {"id": "firestore-choice", "label": "Cloud Firestore", "product": "Document NoSQL (Mobile / Web)", "group": "g-nosql-tier", "plane": "data", "x": 780, "y": 140, "detail": "Real-time client synchronization, offline mobile cache, flexible JSON documents."},
            {"id": "bigtable-choice", "label": "Cloud Bigtable", "product": "Wide-Column Time-Series (Sub-10ms)", "group": "g-nosql-tier", "plane": "data", "x": 780, "y": 280, "detail": "Sustains millions of writes/sec; ideal for IoT, financial tickers, and telemetry data."}
        ],
        [
            {"id": "e1", "from": "need-sql", "to": "spanner-db-choice", "label": "1. Global Scale + 99.999% SLA -> Spanner", "plane": "control"},
            {"id": "e2", "from": "need-sql", "to": "cloudsql-choice", "label": "2. Regional Standard SQL -> Cloud SQL", "plane": "control"},
            {"id": "e3", "from": "need-nosql", "to": "firestore-choice", "label": "3. Mobile / Document Sync -> Firestore", "plane": "control"},
            {"id": "e4", "from": "need-nosql", "to": "bigtable-choice", "label": "4. Heavy Stream / IoT (>1TB) -> Bigtable", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Relational Routing", "edges": ["e1", "e2"], "action": "Evaluates relational scaling: Cloud Spanner for global horizontal scale; Cloud SQL for regional workloads.", "why_traversal": "Prevents over-provisioning Spanner when Cloud SQL satisfies requirements.", "protocol": "Decision Rubric", "plane": "Control Plane"},
            {"n": 2, "title": "NoSQL Routing", "edges": ["e3", "e4"], "action": "Evaluates NoSQL: Firestore for client-facing mobile documents; Bigtable for raw telemetry scale.", "why_traversal": "Ensures database performance matches data access patterns.", "protocol": "NoSQL Sizing Matrix", "plane": "Control Plane"}
        ],
        [
            {"id": "firestore-for-iot-trap", "label": "Selected Firestore for High-Throughput IoT Stream", "changes": {"failedNodes": ["firestore-choice"], "failedEdges": ["e3"]}, "root_cause": "Ingested 100,000 writes/sec into single Firestore document; hit hard 1 write/sec per document limit.", "diverted_path": "Writes blocked with RESOURCE_EXHAUSTED errors; massive billing overrun.", "blast_radius": "IoT ingestion failure.", "recovery": "Select Cloud Bigtable for high-throughput streaming writes exceeding 10,000 QPS."}
        ],
        # D2
        "Traces Step-by-Step Database Decision Traversal: relational vs NoSQL -> transaction scope -> capacity ceiling -> target database selection.",
        "A rigorous decision traversal guides architects to the exact right database product within 3 questions.",
        [
            {"id": "g-schema-q", "label": "Step 1: Schema & Joins Needed?", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-scale-q", "label": "Step 2: Scale & Geo Distribution?", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-db-winner", "label": "Step 3: Validated Database Selection", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "q-sql-needed", "label": "Requires Full SQL Joins & Schema", "product": "Yes: Complex Enterprise Relational", "group": "g-schema-q", "plane": "control", "x": 140, "y": 200, "detail": "Must support foreign keys and standard SQL transactions."},
            {"id": "q-geo-scale", "label": "Requires Multi-Region Active Writes", "product": "Yes: Global Synchronous ACID", "group": "g-scale-q", "plane": "control", "x": 440, "y": 200, "detail": "Users in US, Europe, and Asia all write to database simultaneously with 0 RPO."},
            {"id": "winner-spanner", "label": "Selected: Cloud Spanner Multi-Region", "product": "Delivers 99.999% SLA with TrueTime", "group": "g-db-winner", "plane": "data", "x": 780, "y": 200, "detail": "The only database in Google Cloud delivering global synchronous ACID SQL transactions."}
        ],
        [
            {"id": "e1", "from": "q-sql-needed", "to": "q-geo-scale", "label": "1. Confirmed Relational Need", "plane": "control"},
            {"id": "e2", "from": "q-geo-scale", "to": "winner-spanner", "label": "2. Confirmed Multi-Region Active Writes", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Constraint Narrowing", "edges": ["e1"], "action": "Relational requirement filters out Bigtable and Firestore.", "why_traversal": "Focuses evaluation strictly on relational engines.", "protocol": "Relational Filter", "plane": "Control Plane"},
            {"n": 2, "title": "Global Scaling Confirmation", "edges": ["e2"], "action": "Multi-region active write requirement eliminates Cloud SQL (which only supports read replicas across regions).", "why_traversal": "Spanner is the unambiguous, definitive answer.", "protocol": "Spanner Selection Rule", "plane": "Data Plane"}
        ],
        [
            {"id": "cloudsql-scale-ceiling", "label": "Cloud SQL Hits 64TB Storage Hard Ceiling", "changes": {"failedNodes": ["winner-spanner"], "failedEdges": ["e2"]}, "root_cause": "System outgrew Cloud SQL 64TB storage limit; database locked into read-only mode.", "diverted_path": "Emergency sharding required under production duress.", "blast_radius": "System outage.", "recovery": "Plan migration to Cloud Spanner before databases approach the 64TB limit."}
        ],
        # D3
        "Simulates Database Failover & Replication Resiliency: Cloud SQL High Availability zonal failover vs Cloud Spanner Multi-Region Paxos consensus during datacenter failure.",
        "Comparing failover mechanisms highlights the difference between Cloud SQL's 60-second active-standby restart versus Cloud Spanner's continuous sub-second Paxos quorum.",
        [
            {"id": "g-datacenter-outage", "label": "Datacenter Outage Zone us-central1-a", "type": "zone", "scope": "zonal", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-surviving-failover", "label": "Surviving Zone us-central1-b (Failover Target)", "type": "zone", "scope": "zonal", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "dead-primary-sql", "label": "Cloud SQL Primary (Dead)", "product": "Status: HARDWARE_FAILURE", "group": "g-datacenter-outage", "plane": "data", "x": 220, "y": 140, "detail": "Hardware failure in zone us-central1-a terminates primary database instance."},
            {"id": "heartbeat-watchdog", "label": "Cloud SQL HA Watchdog", "product": "Heartbeat Timeout (60 Seconds)", "group": "g-datacenter-outage", "plane": "control", "x": 220, "y": 280, "detail": "Detects 30 seconds of missed heartbeats; initiates automated regional disk failover."},
            {"id": "standby-promoted-sql", "label": "Promoted Standby Cloud SQL", "product": "Promoted to Primary in Zone B", "group": "g-surviving-failover", "plane": "data", "x": 700, "y": 140, "detail": "Attaches regional persistent disk and recovers crash logs in 52 seconds."},
            {"id": "app-reconnect-pool", "label": "GKE App Pods Reconnected", "product": "Cloud SQL Proxy Auto-Reconnect", "group": "g-surviving-failover", "plane": "data", "x": 700, "y": 280, "detail": "Cloud SQL Proxy seamlessly updates connection IP; application resumes transactions."}
        ],
        [
            {"id": "e1", "from": "dead-primary-sql", "to": "heartbeat-watchdog", "label": "1. Loss of Primary Heartbeat", "plane": "control"},
            {"id": "e2", "from": "heartbeat-watchdog", "to": "standby-promoted-sql", "label": "2. Promote Standby Instance", "plane": "control"},
            {"id": "e3", "from": "standby-promoted-sql", "to": "app-reconnect-pool", "label": "3. Re-establish Application Connections", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Automated Zonal Failover", "edges": ["e1", "e2"], "action": "Watchdog detects failure and promotes standby instance on regional persistent disk.", "why_traversal": "Provides automated disaster recovery without data loss within the region.", "protocol": "Cloud SQL HA Orchestrator", "plane": "Control Plane"},
            {"n": 2, "title": "Application Recovery", "edges": ["e3"], "action": "Cloud SQL Proxy transparently redirects client queries to the new primary in Zone B in under 60s.", "why_traversal": "Restores production database availability with zero manual intervention.", "protocol": "Cloud SQL Proxy gRPC", "plane": "Data Plane"}
        ],
        [
            {"id": "app-crash-on-reconnect", "label": "Application Crashes Due to Stale Connection Pool", "changes": {"failedNodes": ["app-reconnect-pool"], "failedEdges": ["e3"]}, "root_cause": "Application connection pool was configured without validation query or max-lifetime.", "diverted_path": "Pods held dead TCP connections to dead Zone A; threw continuous 500 errors.", "blast_radius": "Outage persisted for 30 minutes until pods were manually restarted.", "recovery": "Configure HikariCP / DB pool with testOnBorrow=true and maxLifetime=1800000ms."}
        ]
    )

    # 057: Load Balancer Decision Cheat Sheet
    specs[57] = make_spec(
        57, "CS.3", "Load Balancer Decision Cheat Sheet",
        "Visualizes PCA Load Balancer Selection Matrix: External Application Load Balancer (Global/Regional L7 HTTP/S) vs External Proxy Network Load Balancer (Global L4 TCP/SSL) vs External Passthrough Network Load Balancer (Regional L4 UDP/TCP non-proxy) vs Internal Load Balancers.",
        "Selecting the correct Google Cloud Load Balancer requires evaluating three precise criteria: Layer 7 HTTP/S vs Layer 4 TCP/UDP, Global Anycast edge termination vs Regional routing, and whether client IP preservation is mandatory.",
        [
            {"id": "g-protocol-scope", "label": "Traffic Protocol & Geographic Scope", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-global-proxies", "label": "Global Anycast Proxy Load Balancers", "type": "vpc", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-regional-passthrough", "label": "Regional Passthrough Load Balancers", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "traffic-l7-http", "label": "Traffic: HTTP / HTTPS / gRPC?", "product": "L7 Application Traffic", "group": "g-protocol-scope", "plane": "control", "x": 140, "y": 140, "detail": "Requires URL path routing, TLS termination, Cloud CDN caching, and Cloud Armor WAF."},
            {"id": "traffic-l4-tcp-udp", "label": "Traffic: Raw TCP / UDP / VoIP?", "product": "L4 Transport Traffic", "group": "g-protocol-scope", "plane": "control", "x": 140, "y": 280, "detail": "Non-HTTP protocols, gaming UDP streams, or requires direct client source IP preservation."},
            {"id": "global-alb-pick", "label": "External Application LB (Global)", "product": "Global Anycast L7 Proxy", "group": "g-global-proxies", "plane": "data", "x": 440, "y": 140, "detail": "Single Anycast IP; terminates TLS at edge; routes to backends across multiple regions."},
            {"id": "global-tcp-proxy-pick", "label": "External Proxy Network LB", "product": "Global Anycast L4 Proxy", "group": "g-global-proxies", "plane": "data", "x": 440, "y": 280, "detail": "Terminates non-HTTP TCP/SSL traffic at Google edge; routes over private fiber."},
            {"id": "passthrough-nlb-pick", "label": "External Passthrough Network LB", "product": "Regional Maglev L4 (Direct IP)", "group": "g-regional-passthrough", "plane": "data", "x": 780, "y": 140, "detail": "Preserves client IP directly; supports UDP; routes traffic directly without proxy hops."},
            {"id": "internal-alb-pick", "label": "Internal Application LB", "product": "Regional RFC 1918 Private LB", "group": "g-regional-passthrough", "plane": "data", "x": 780, "y": 280, "detail": "Internal microservice-to-microservice traffic routing within Shared VPC subnets."}
        ],
        [
            {"id": "e1", "from": "traffic-l7-http", "to": "global-alb-pick", "label": "1. L7 + Global Anycast -> External ALB", "plane": "control"},
            {"id": "e2", "from": "traffic-l7-http", "to": "internal-alb-pick", "label": "2. L7 + Private Internal -> Internal ALB", "plane": "control"},
            {"id": "e3", "from": "traffic-l4-tcp-udp", "to": "global-tcp-proxy-pick", "label": "3. L4 TCP + Global Anycast -> Proxy NLB", "plane": "control"},
            {"id": "e4", "from": "traffic-l4-tcp-udp", "to": "passthrough-nlb-pick", "label": "4. L4 UDP / Preserve IP -> Passthrough NLB", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Layer 7 Ingress Selection", "edges": ["e1", "e2"], "action": "HTTP/HTTPS traffic routes to External ALB for edge caching or Internal ALB for microservices.", "why_traversal": "Provides URL-based routing and edge security policies.", "protocol": "HTTP/2 & HTTP/3", "plane": "Control Plane"},
            {"n": 2, "title": "Layer 4 Ingress Selection", "edges": ["e3", "e4"], "action": "TCP/UDP traffic routes to Proxy NLB for Anycast or Passthrough NLB for direct IP preservation.", "why_traversal": "Supports gaming, streaming, and custom non-HTTP enterprise protocols.", "protocol": "TCP / UDP Transport", "plane": "Data Plane"}
        ],
        [
            {"id": "udp-dropped-by-alb-trap", "label": "Configured Application LB for UDP Gaming Traffic", "changes": {"failedNodes": ["global-alb-pick"], "failedEdges": ["e1"]}, "root_cause": "External Application Load Balancer only supports HTTP, HTTPS, and gRPC; dropped all UDP packets.", "diverted_path": "Game client connection timeouts.", "blast_radius": "Total multiplayer outage.", "recovery": "Use External Passthrough Network Load Balancer for UDP gaming and streaming protocols."}
        ],
        # D2
        "Traces Load Balancer Selection Decision Traversal: External vs Internal -> Layer 7 vs Layer 4 -> Global vs Regional -> Client IP preservation requirement.",
        "Decision paths cleanly resolve complex networking scenarios to the exact Google Cloud load balancer SKU.",
        [
            {"id": "g-boundary-q", "label": "Step 1: Public Internet or Private VPC?", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-layer-q", "label": "Step 2: Layer 7 (HTTP) or Layer 4 (TCP/UDP)?", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-winner-lb", "label": "Step 3: Optimal Load Balancer Match", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "q-public-facing", "label": "Public External Clients", "product": "Users on Internet Worldwide", "group": "g-boundary-q", "plane": "control", "x": 140, "y": 200, "detail": "Millions of global users connecting from web browsers and mobile apps."},
            {"id": "q-l7-features", "label": "Requires WAF & Edge Caching", "product": "Cloud Armor & Cloud CDN Needed", "group": "g-layer-q", "plane": "control", "x": 440, "y": 200, "detail": "Must protect against DDoS and cache static media assets at edge."},
            {"id": "select-global-alb", "label": "External Application LB (Global)", "product": "Selected: Global Anycast L7 LB", "group": "g-winner-lb", "plane": "data", "x": 780, "y": 200, "detail": "Single Anycast VIP delivering Cloud Armor WAF, Cloud CDN, and multi-region routing."}
        ],
        [
            {"id": "e1", "from": "q-public-facing", "to": "q-l7-features", "label": "1. External Ingress Confirmed", "plane": "control"},
            {"id": "e2", "from": "q-l7-features", "to": "select-global-alb", "label": "2. L7 Features Required -> External ALB", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Boundary & Feature Filtering", "edges": ["e1", "e2"], "action": "Confirms external internet exposure and Layer 7 feature requirements.", "why_traversal": "Pinpoints External Application Load Balancer with 100% confidence.", "protocol": "Load Balancer Rubric", "plane": "Control Plane"}
        ],
        [
            {"id": "wrong-regional-lb-pick", "label": "Selected Regional ALB for Multi-Region Workload", "changes": {"failedNodes": ["select-global-alb"], "failedEdges": ["e2"]}, "root_cause": "Selected Regional External ALB, preventing cross-region failover between US and Europe.", "diverted_path": "Regional outage took down service globally.", "blast_radius": "Unnecessary downtime.", "recovery": "Select Global External ALB when backends span multiple Google Cloud regions."}
        ],
        # D3
        "Simulates Global Multi-Region Traffic Spillover: us-central1 backend reaches 100% capacity; Global Application Load Balancer seamlessly spills excess traffic to europe-west1.",
        "Global Anycast load balancing protects saturated regional backends by dynamically redistributing excess request capacity across global datacenter fleets.",
        [
            {"id": "g-saturated-region", "label": "Saturated Region: us-central1 (Capacity 100%)", "type": "region", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-overflow-region", "label": "Surviving Region: europe-west1 (Capacity 35%)", "type": "region", "scope": "regional", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "us-backend-saturated", "label": "us-central1 Backend MIG", "product": "Serving 10,000 QPS (Max Capacity)", "group": "g-saturated-region", "plane": "data", "x": 220, "y": 140, "detail": "CPU utilization reaches 85%; max rate per instance threshold breached."},
            {"id": "alb-spillover-logic", "label": "Global Anycast Spillover Engine", "product": "Dynamic Capacity Balancing", "group": "g-saturated-region", "plane": "control", "x": 220, "y": 280, "detail": "Directs newly arriving US client requests across private fiber to Europe."},
            {"id": "europe-backend-healthy", "label": "europe-west1 Backend MIG", "product": "Absorbs 3,000 QPS Spillover", "group": "g-overflow-region", "plane": "data", "x": 700, "y": 140, "detail": "Healthy European cluster has 65% idle headroom; processes US requests cleanly."},
            {"id": "zero-dropped-requests", "label": "Zero Dropped HTTP Requests", "product": "100% Customer Success Rate", "group": "g-overflow-region", "plane": "data", "x": 700, "y": 280, "detail": "Customers experience 80ms transatlantic latency rather than HTTP 503 errors."}
        ],
        [
            {"id": "e1", "from": "us-backend-saturated", "to": "alb-spillover-logic", "label": "1. Signal Saturated Capacity", "plane": "control"},
            {"id": "e2", "from": "alb-spillover-logic", "to": "europe-backend-healthy", "label": "2. Spill Excess Traffic to Europe", "plane": "data"},
            {"id": "e3", "from": "europe-backend-healthy", "to": "zero-dropped-requests", "label": "3. Deliver 100% Successful Responses", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Capacity Overflow Detection", "edges": ["e1", "e2"], "action": "Load balancer detects us-central1 at max capacity; reroutes excess packets to Europe.", "why_traversal": "Prevents local backend crash under viral surge.", "protocol": "Anycast BGP Spillover", "plane": "Control Plane"},
            {"n": 2, "title": "Graceful Global Degradation", "edges": ["e3"], "action": "Europe absorbs load; users experience slightly higher latency instead of hard errors.", "why_traversal": "Prioritizes availability over localized latency during major surges.", "protocol": "Google Private Backbone", "plane": "Data Plane"}
        ],
        [
            {"id": "max-rate-unconfigured-crash", "label": "Missing Max Rate Configuration Drops Traffic", "changes": {"failedNodes": ["alb-spillover-logic"], "failedEdges": ["e2"]}, "root_cause": "Backend service lacked 'max rate per instance' setting; ALB sent 100% traffic to local region.", "diverted_path": "us-central1 crashed under 25,000 QPS; 100% of US users dropped.", "blast_radius": "System outage in primary market.", "recovery": "Configure 'max rate per instance' or 'max utilization' on all Global ALB backend services."}
        ]
    )

    # 058: Hybrid Connectivity Decision Cheat Sheet
    specs[58] = make_spec(
        58, "CS.4", "Hybrid Connectivity Decision Cheat Sheet",
        "Visualizes PCA Hybrid Connectivity Decision Matrix: Cloud VPN (HA VPN with dynamic BGP, max 3Gbps/tunnel) vs Dedicated Interconnect (10G/100G physical cross-connect) vs Partner Interconnect (50M-10G via service provider) vs Cross-Cloud Interconnect vs Carrier Peering.",
        "Choosing hybrid cloud networking requires evaluating bandwidth, encryption, physical colocation presence, and SLA targets: 99.99% high availability mandates dual colocation facilities and four cross-connects.",
        [
            {"id": "g-hybrid-req-eval", "label": "Bandwidth & SLA Requirements", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-interconnect-tier", "label": "Enterprise Dedicated & Partner Interconnect", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-vpn-peering-tier", "label": "IPsec VPN & Direct Peering", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "req-bandwidth-large", "label": "Bandwidth > 10Gbps Required?", "product": "High-Throughput Data Migration", "group": "g-hybrid-req-eval", "plane": "control", "x": 140, "y": 140, "detail": "Demands 10Gbps to 100Gbps dedicated pipe without public internet transit."},
            {"id": "req-quick-budget", "label": "Bandwidth < 3Gbps / Low Budget?", "product": "Encrypted Public Internet Path", "group": "g-hybrid-req-eval", "plane": "control", "x": 140, "y": 280, "detail": "Fast setup (hours), encrypted IPsec, dynamic BGP routing, lower cost."},
            {"id": "dedicated-interconnect", "label": "Dedicated Interconnect (10/100G)", "product": "Physical Cross-Connect to Google", "group": "g-interconnect-tier", "plane": "data", "x": 440, "y": 140, "detail": "Direct fiber connection at Google colocation facility; 99.99% SLA architecture."},
            {"id": "partner-interconnect", "label": "Partner Interconnect (50M-10G)", "product": "Service Provider Co-location", "group": "g-interconnect-tier", "plane": "data", "x": 440, "y": 280, "detail": "For enterprises whose data center is not colocated with a Google facility."},
            {"id": "ha-vpn-pick", "label": "Cloud HA VPN (99.99% SLA)", "product": "Dual Tunnels over Dynamic BGP", "group": "g-vpn-peering-tier", "plane": "data", "x": 780, "y": 140, "detail": "IPsec encrypted tunnels (max 3Gbps per tunnel); supports active-active BGP routing."},
            {"id": "cross-cloud-pick", "label": "Cross-Cloud Interconnect", "product": "Direct Link to AWS / Azure", "group": "g-vpn-peering-tier", "plane": "data", "x": 780, "y": 280, "detail": "Pre-provisioned physical connection between Google Cloud and AWS/Azure datacenters."}
        ],
        [
            {"id": "e1", "from": "req-bandwidth-large", "to": "dedicated-interconnect", "label": "1. >10Gbps + Colocated -> Dedicated Interconnect", "plane": "control"},
            {"id": "e2", "from": "req-bandwidth-large", "to": "partner-interconnect", "label": "2. Sub-10Gbps or Not Colocated -> Partner Interconnect", "plane": "control"},
            {"id": "e3", "from": "req-quick-budget", "to": "ha-vpn-pick", "label": "3. <3Gbps + IPsec Encryption -> HA VPN", "plane": "control"},
            {"id": "e4", "from": "req-bandwidth-large", "to": "cross-cloud-pick", "label": "4. Direct AWS/Azure Link -> Cross-Cloud", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Bandwidth & Physical Presence Evaluation", "edges": ["e1", "e2"], "action": "Assesses physical datacenter location and throughput volume.", "why_traversal": "Dedicated Interconnect requires customer presence in Google colocation facility.", "protocol": "Physical 802.1q VLAN", "plane": "Control Plane"},
            {"n": 2, "title": "Encryption & Multi-Cloud Evaluation", "edges": ["e3", "e4"], "action": "Selects HA VPN for IPsec encryption or Cross-Cloud Interconnect for AWS/Azure.", "why_traversal": "Provides secure, high-availability hybrid connectivity matched to budget.", "protocol": "IPsec / BGP Routing", "plane": "Data Plane"}
        ],
        [
            {"id": "unencrypted-interconnect-audit", "label": "Interconnect Lacks IPsec for Regulated Data", "changes": {"failedNodes": ["dedicated-interconnect"], "failedEdges": ["e1"]}, "root_cause": "Compliance auditor rejected standard Interconnect because traffic was unencrypted on wire.", "diverted_path": "Audit finding issued.", "blast_radius": "Delayed migration sign-off.", "recovery": "Deploy Cloud HA VPN over Cloud Interconnect or enable MACsec encryption on Dedicated Interconnect."}
        ],
        # D2
        "Traces 99.99% High Availability Interconnect Topology Flow: 2 metropolitan colocation facilities, 4 physical cross-connects, dual Cloud Routers, and dynamic BGP route propagation.",
        "Achieving Google's 99.99% Interconnect SLA requires total physical diversity: two distinct colocation sites with redundant connections to two Cloud Routers.",
        [
            {"id": "g-onprem-dc1", "label": "Customer On-Prem DC / Colocation A", "type": "onprem", "scope": "onprem", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-google-colo", "label": "Google Edge: Dual Metro Colocations", "type": "external", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-vpc-cloud-routers", "label": "GCP Production VPC (Dual Cloud Routers)", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "onprem-router1", "label": "On-Premises Edge Router 1", "product": "BGP ASN: 65001 (Metro 1)", "group": "g-onprem-dc1", "plane": "data", "x": 140, "y": 140, "detail": "Connects to Google Colocation Facility 1 (e.g. Equinix Ashburn)."},
            {"id": "onprem-router2", "label": "On-Premises Edge Router 2", "product": "BGP ASN: 65001 (Metro 2)", "group": "g-onprem-dc1", "plane": "data", "x": 140, "y": 280, "detail": "Connects to Google Colocation Facility 2 (e.g. CoreSite Reston)."},
            {"id": "google-colo1", "label": "Google Metro Facility 1", "product": "Dual 10G Dedicated Circuits", "group": "g-google-colo", "plane": "data", "x": 440, "y": 140, "detail": "Carries Primary VLAN attachments to Cloud Router A."},
            {"id": "google-colo2", "label": "Google Metro Facility 2", "product": "Dual 10G Dedicated Circuits", "group": "g-google-colo", "plane": "data", "x": 440, "y": 280, "detail": "Carries Secondary VLAN attachments to Cloud Router B."},
            {"id": "cloud-router-ha", "label": "Dual Regional Cloud Routers", "product": "Dynamic BGP (99.99% SLA)", "group": "g-vpc-cloud-routers", "plane": "control", "x": 780, "y": 200, "detail": "Propagates VPC subnets to on-premise network and dynamically fails over in < 3 seconds."}
        ],
        [
            {"id": "e1", "from": "onprem-router1", "to": "google-colo1", "label": "1. 10G Cross-Connect Metro 1", "plane": "data"},
            {"id": "e2", "from": "onprem-router2", "to": "google-colo2", "label": "2. 10G Cross-Connect Metro 2", "plane": "data"},
            {"id": "e3", "from": "google-colo1", "to": "cloud-router-ha", "label": "3. Primary BGP Peering Session", "plane": "control"},
            {"id": "e4", "from": "google-colo2", "to": "cloud-router-ha", "label": "4. Secondary BGP Peering Session", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Dual-Metro Physical Cross-Connects", "edges": ["e1", "e2"], "action": "Provisions redundant physical circuits across two distinct metropolitan areas.", "why_traversal": "Protects against localized fiber cuts or datacenter power outages.", "protocol": "10GBASE-LR Optical Fiber", "plane": "Data Plane"},
            {"n": 2, "title": "Dynamic BGP Route Exchange", "edges": ["e3", "e4"], "action": "Cloud Routers exchange routes via eBGP; if Metro 1 fails, Metro 2 takes 100% traffic.", "why_traversal": "Satisfies Google's 99.99% SLA contractual requirements.", "protocol": "eBGP Dynamic Routing", "plane": "Control Plane"}
        ],
        [
            {"id": "single-colo-9999-trap", "label": "Single Colocation Facility Violates 99.99% SLA", "changes": {"failedNodes": ["google-colo2"], "failedEdges": ["e2", "e4"]}, "root_cause": "Customer deployed 4 cross-connects inside a single colocation facility to save cost.", "diverted_path": "Google denies 99.99% SLA claim when facility power glitch caused outage.", "blast_radius": "Only 99.9% SLA applies.", "recovery": "Mandate dual distinct metropolitan colocation facilities for all 99.99% SLA architectures."}
        ],
        # D3
        "Simulates Major Metro Facility Blackout: Metro 1 physical colocation experiences catastrophic power failure; BGP withdraws routes and shifts traffic to Metro 2 in 2.4 seconds.",
        "Dynamic BGP route withdrawal ensures seamless hybrid failover during major telecommunications infrastructure disruptions.",
        [
            {"id": "g-blackout-metro", "label": "Metro 1 Colocation (Total Power Loss)", "type": "external", "scope": "global", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-surviving-metro", "label": "Metro 2 Colocation & Cloud Router Failover", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "dead-colo-1", "label": "Metro 1 Circuits (Dead)", "product": "Substation Transformer Fire", "group": "g-blackout-metro", "plane": "data", "x": 220, "y": 140, "detail": "Entire Ashburn colocation facility loses municipal and generator power."},
            {"id": "bgp-keepalive-fail", "label": "BGP Keepalive Timeout", "product": "BGP Peer Down (Hold Time = 3s)", "group": "g-blackout-metro", "plane": "control", "x": 220, "y": 280, "detail": "Cloud Router A detects missed BGP keepalives and withdraws Metro 1 routes."},
            {"id": "metro-2-circuits", "label": "Metro 2 Circuits (Active)", "product": "Reston Secondary 10G Link", "group": "g-surviving-metro", "plane": "data", "x": 700, "y": 140, "detail": "Absorbs 100% of hybrid traffic with zero packet loss."},
            {"id": "uninterrupted-hybrid", "label": "Continuous Hybrid Workloads", "product": "0 Dropped Database Transactions", "group": "g-surviving-metro", "plane": "data", "x": 700, "y": 280, "detail": "Core enterprise database sync continues uninterrupted across Google backbone."}
        ],
        [
            {"id": "e1", "from": "dead-colo-1", "to": "bgp-keepalive-fail", "label": "1. Loss of Physical Carrier Signal", "plane": "control"},
            {"id": "e2", "from": "bgp-keepalive-fail", "to": "metro-2-circuits", "label": "2. BGP Reroutes Traffic to Metro 2", "plane": "control"},
            {"id": "e3", "from": "metro-2-circuits", "to": "uninterrupted-hybrid", "label": "3. Transmit 100% of Traffic via Reston", "plane": "data"}
        ],
        [
            {"n": 1, "title": "BGP Route Withdrawal", "edges": ["e1", "e2"], "action": "BGP session times out in 3 seconds; Cloud Router diverts packets to Metro 2.", "why_traversal": "Demonstrates why dynamic BGP routing is required for enterprise resilience.", "protocol": "BGP Route Withdrawal", "plane": "Control Plane"},
            {"n": 2, "title": "Zero-Loss Failover", "edges": ["e3"], "action": "Metro 2 carries full production load; enterprise applications experience zero disruption.", "why_traversal": "Proves the resilience of the 99.99% SLA dual-metro architecture.", "protocol": "802.1q VLAN Failover", "plane": "Data Plane"}
        ],
        [
            {"id": "static-routing-blackhole", "label": "Static Route Configuration Blackholes Traffic", "changes": {"failedNodes": ["bgp-keepalive-fail"], "failedEdges": ["e2"]}, "root_cause": "Team configured static routes instead of dynamic BGP.", "diverted_path": "Packets continued sending to dead link; all hybrid traffic dropped.", "blast_radius": "Total on-premise to cloud hybrid outage.", "recovery": "Never use static routes for high-availability hybrid cloud networks; enforce dynamic BGP."}
        ]
    )

    # 059: Storage & Messaging Decision Cheat Sheet
    specs[59] = make_spec(
        59, "CS.5", "Storage & Messaging Decision Cheat Sheet",
        "Visualizes Storage Classes & Messaging Selection Architecture: Cloud Storage classes (Standard, Nearline, Coldline, Archive) + Filestore Enterprise NFS paired with Messaging systems (Cloud Pub/Sub global streaming vs Cloud Tasks rate-limited execution vs Pub/Sub Lite).",
        "Cost optimization in storage and messaging demands matching access patterns: transition stale objects to Coldline/Archive storage while using Cloud Tasks for targeted rate-limiting and Cloud Pub/Sub for high-throughput broadcast streaming.",
        [
            {"id": "g-storage-classes", "label": "Cloud Storage Classes & Lifecycle", "type": "project", "scope": "global", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-filestore-nfs", "label": "Enterprise Managed File Shares", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-messaging-tier", "label": "Asynchronous Messaging & Queuing", "type": "project", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "gcs-standard", "label": "Standard Cloud Storage", "product": "Daily Access (Web Media / Data)", "group": "g-storage-classes", "plane": "data", "x": 140, "y": 100, "detail": "Hot storage with zero retrieval fees; best for active website assets and live analytics."},
            {"id": "gcs-nearline", "label": "Nearline Storage (30-Day)", "product": "Access <= Once / Month", "group": "g-storage-classes", "plane": "data", "x": 140, "y": 180, "detail": "Monthly backups; 30-day minimum storage commitment; lower storage price."},
            {"id": "gcs-coldline", "label": "Coldline Storage (90-Day)", "product": "Access <= Once / Quarter", "group": "g-storage-classes", "plane": "data", "x": 140, "y": 260, "detail": "Disaster recovery images; 90-day minimum storage commitment."},
            {"id": "gcs-archive", "label": "Archive Storage (365-Day)", "product": "Access < Once / Year", "group": "g-storage-classes", "plane": "data", "x": 140, "y": 340, "detail": "Regulatory compliance cold storage; $0.0012/GB/mo; 365-day commitment."},
            {"id": "filestore-share", "label": "Filestore Enterprise NFS", "product": "POSIX Shared File System", "group": "g-filestore-nfs", "plane": "data", "x": 440, "y": 200, "detail": "Multi-reader multi-writer NFSv3 share for GKE and legacy CMS applications."},
            {"id": "pubsub-engine", "label": "Cloud Pub/Sub", "product": "Global Ingestion (Fan-Out)", "group": "g-messaging-tier", "plane": "data", "x": 780, "y": 140, "detail": "Decoupled many-to-many event streaming with infinite scale and no provisioning."},
            {"id": "cloud-tasks-engine", "label": "Cloud Tasks", "product": "Targeted Rate-Limited Task Queue", "group": "g-messaging-tier", "plane": "control", "x": 780, "y": 280, "detail": "Point-to-point execution with explicit dispatch rate limits and scheduled delivery times."}
        ],
        [
            {"id": "e1", "from": "gcs-standard", "to": "gcs-nearline", "label": "1. Age > 30d -> Transition to Nearline", "plane": "control"},
            {"id": "e2", "from": "gcs-nearline", "to": "gcs-coldline", "label": "2. Age > 90d -> Transition to Coldline", "plane": "control"},
            {"id": "e3", "from": "gcs-coldline", "to": "gcs-archive", "label": "3. Age > 365d -> Transition to Archive", "plane": "control"},
            {"id": "e4", "from": "filestore-share", "to": "pubsub-engine", "label": "4. Publish File Change Event", "plane": "control"},
            {"id": "e5", "from": "pubsub-engine", "to": "cloud-tasks-engine", "label": "5. Route to Rate-Limited Task Queue", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Lifecycle Cost Optimization", "edges": ["e1", "e2", "e3"], "action": "Automated object lifecycle policies transition data to cheaper storage tiers as it ages.", "why_traversal": "Slashes storage expenditure by up to 90% automatically.", "protocol": "GCS Lifecycle Management", "plane": "Control Plane"},
            {"n": 2, "title": "Messaging Ingestion & Task Control", "edges": ["e4", "e5"], "action": "Pub/Sub absorbs high-throughput event spikes; Cloud Tasks controls execution rate to protect backends.", "why_traversal": "Combines massive fan-out ingestion with controlled downstream dispatch.", "protocol": "Pub/Sub / Tasks API", "plane": "Data Plane"}
        ],
        [
            {"id": "archive-early-deletion-shock", "label": "Early Deletion Penalty Fee Shock", "changes": {"failedNodes": ["gcs-archive"], "failedEdges": ["e3"]}, "root_cause": "Application deleted 100TB of Archive data after 10 days; billed for remaining 355 days of storage.", "diverted_path": "Early deletion fee wiped out anticipated storage savings.", "blast_radius": "Surprise $4,500 bill.", "recovery": "Never store temporary or frequently deleted files in Coldline or Archive storage classes."}
        ],
        # D2
        "Traces Messaging Selection Flow: Pub/Sub vs Cloud Tasks vs Pub/Sub Lite evaluated on fan-out, rate-limiting, dedup, and message ordering requirements.",
        "Choosing between Pub/Sub and Cloud Tasks is simple: Pub/Sub for many-to-many broadcast streaming; Cloud Tasks for point-to-point rate-limited task execution.",
        [
            {"id": "g-msg-input", "label": "Step 1: Messaging Pattern Requirement", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-delivery-ctl", "label": "Step 2: Delivery & Rate-Limiting Controls", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-msg-winner", "label": "Step 3: Optimal Messaging Technology", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "q-fanout-pattern", "label": "Pattern: 1 Publisher, 5 Independent Services", "product": "Many-to-Many Fan-Out", "group": "g-msg-input", "plane": "control", "x": 140, "y": 140, "detail": "Order created event must be consumed independently by Billing, Inventory, and Shipping."},
            {"id": "q-rate-limit-pattern", "label": "Pattern: Protect Legacy Backend (Max 20 req/s)", "product": "Explicit Rate-Limiting", "group": "g-msg-input", "plane": "control", "x": 140, "y": 280, "detail": "Must throttle requests so legacy database is not overwhelmed."},
            {"id": "match-pubsub", "label": "Selected: Cloud Pub/Sub", "product": "Topics + Multiple Subscriptions", "group": "g-delivery-ctl", "plane": "data", "x": 440, "y": 140, "detail": "Each downstream microservice has independent subscription and ACK state."},
            {"id": "match-tasks", "label": "Selected: Cloud Tasks", "product": "Queue Dispatch Rate: 20/sec", "group": "g-delivery-ctl", "plane": "data", "x": 440, "y": 280, "detail": "Guarantees dispatch rate never exceeds 20 requests/sec with exponential retry backoff."},
            {"id": "winner-messaging", "label": "Architectural Synergy", "product": "Pub/Sub Ingress + Tasks Dispatch", "group": "g-msg-winner", "plane": "data", "x": 780, "y": 200, "detail": "Combines broadcast fan-out with protective downstream rate-limiting."}
        ],
        [
            {"id": "e1", "from": "q-fanout-pattern", "to": "match-pubsub", "label": "1. Fan-Out -> Route to Pub/Sub", "plane": "control"},
            {"id": "e2", "from": "q-rate-limit-pattern", "to": "match-tasks", "label": "2. Rate Limiting -> Route to Cloud Tasks", "plane": "control"},
            {"id": "e3", "from": "match-pubsub", "to": "winner-messaging", "label": "3. Broadcast Notification", "plane": "data"},
            {"id": "e4", "from": "match-tasks", "to": "winner-messaging", "label": "4. Throttled Downstream Invocation", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Pattern Evaluation", "edges": ["e1", "e2"], "action": "Directs broadcast requirements to Pub/Sub and rate-throttling to Cloud Tasks.", "why_traversal": "Applies the exact messaging service designed for each architectural pattern.", "protocol": "Decision Filter", "plane": "Control Plane"},
            {"n": 2, "title": "Integrated Delivery", "edges": ["e3", "e4"], "action": "Combines both systems for end-to-end reliability and downstream database protection.", "why_traversal": "Prevents downstream microservices from crashing under upstream surges.", "protocol": "Pub/Sub + Tasks Orchestration", "plane": "Data Plane"}
        ],
        [
            {"id": "pubsub-flood-crashes-db", "label": "Pub/Sub Subscriber Floods Legacy Database", "changes": {"failedNodes": ["match-pubsub"], "failedEdges": ["e3"]}, "root_cause": "Used Pub/Sub without rate limiting to call legacy database; 50,000 concurrent push deliveries crashed DB.", "diverted_path": "Database offline for 2 hours.", "blast_radius": "Full system crash.", "recovery": "Introduce Cloud Tasks or Pull subscriber with concurrency throttling in front of fragile databases."}
        ],
        # D3
        "Simulates Pub/Sub Dead-Letter Queue (DLQ) & Poison Pill Isolation: malformed payload fails consumer processing 5 times and is automatically diverted to DLQ topic.",
        "Dead-letter topics isolate poison pill messages that repeatedly crash subscriber code, allowing healthy message processing to continue uninterrupted.",
        [
            {"id": "g-message-flow", "label": "Active Production Pub/Sub Subscription", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-dlq-quarantine", "label": "Dead-Letter Queue (DLQ) & Remediation", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "poison-message", "label": "Poison Pill JSON Message", "product": "Malformed Payload (Corrupted UTF-8)", "group": "g-message-flow", "plane": "data", "x": 220, "y": 140, "detail": "Message triggers unhandled panic in subscriber parsing code."},
            {"id": "failing-subscriber", "label": "Order Processing Subscriber", "product": "Crashes on Parse (5 NACKs)", "group": "g-message-flow", "plane": "data", "x": 220, "y": 280, "detail": "Rejects message 5 consecutive times; exceeds maxDeliveryAttempts=5 threshold."},
            {"id": "dlq-topic", "label": "Dead-Letter Topic (DLQ)", "product": "orders-dead-letter-topic", "group": "g-dlq-quarantine", "plane": "data", "x": 700, "y": 140, "detail": "Pub/Sub automatically routes poison message away from main subscription queue."},
            {"id": "unblocked-orders", "label": "Healthy Orders Flowing", "product": "100% Throughput Restored", "group": "g-dlq-quarantine", "plane": "data", "x": 700, "y": 280, "detail": "Main subscription continues processing remaining 10,000 valid orders smoothly."}
        ],
        [
            {"id": "e1", "from": "poison-message", "to": "failing-subscriber", "label": "1. Attempt Message Delivery", "plane": "data"},
            {"id": "e2", "from": "failing-subscriber", "to": "dlq-topic", "label": "2. 5 Delivery Failures -> Divert to DLQ", "plane": "control"},
            {"id": "e3", "from": "dlq-topic", "to": "unblocked-orders", "label": "3. Unblock Main Subscription Processing", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Poison Pill Isolation", "edges": ["e1", "e2"], "action": "Pub/Sub tracks retry count; diverts failing message to dead-letter topic after 5 NACKs.", "why_traversal": "Prevents bad payloads from permanently blocking the head of the subscription queue.", "protocol": "Pub/Sub DLQ Engine", "plane": "Control Plane"},
            {"n": 2, "title": "Queue Unblocking & Remediation", "edges": ["e3"], "action": "Valid orders resume processing; alert notifies engineers to inspect poison message in DLQ.", "why_traversal": "Delivers continuous uptime even when upstream clients emit malformed data.", "protocol": "Cloud Pub/Sub ACK", "plane": "Data Plane"}
        ],
        [
            {"id": "missing-dlq-infinite-loop", "label": "Missing DLQ Causes Infinite CrashLoopBackOff", "changes": {"failedNodes": ["failing-subscriber"], "failedEdges": ["e2"]}, "root_cause": "Subscription lacked DLQ configuration; subscriber crashed and restarted in infinite loop.", "diverted_path": "Subscriber pods crashed repeatedly; queue backlogged with 50,000 unprocessed orders.", "blast_radius": "Delayed customer order fulfillment.", "recovery": "Always attach dead-letter topics with maxDeliveryAttempts on all production subscriptions."}
        ]
    )

    # 060: Key Numbers, Limits & SLAs to Memorise
    specs[60] = make_spec(
        60, "CS.6", "Key Numbers, Limits & SLAs to Memorise",
        "Visualizes PCA Essential Metrics, SLAs & Limit Math: Compound Availability formulas (Serial vs Parallel), Service SLAs (Spanner 99.999% vs Cloud SQL 99.95% vs Compute Engine 99.99%), Storage limits, and Network throughput ceilings.",
        "Passing the PCA exam requires instant recall of critical service boundaries: Spanner multi-region yields 5 minutes downtime/year (99.999%), Cloud SQL allows 4.38 hours downtime/year (99.95%), and compound serial availability degrades with each chained dependency.",
        [
            {"id": "g-sla-math", "label": "Compound Availability & Downtime Math", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-service-limits", "label": "Critical GCP Limits & Ceilings", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-network-limits", "label": "Network & Throughput Formulas", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "sla-serial-math", "label": "Serial Availability Formula", "product": "A_total = A1 * A2 * A3", "group": "g-sla-math", "plane": "control", "x": 140, "y": 140, "detail": "Three 99.9% services in series = 99.7% availability (26 hours downtime/year)."},
            {"id": "sla-parallel-math", "label": "Parallel Availability Formula", "product": "A_total = 1 - (1 - A1)*(1 - A2)", "group": "g-sla-math", "plane": "control", "x": 140, "y": 280, "detail": "Two 99.9% services in parallel = 99.9999% availability (31 seconds downtime/year)."},
            {"id": "spanner-5nines", "label": "Cloud Spanner Multi-Region", "product": "99.999% SLA (5.26 min/yr down)", "group": "g-service-limits", "plane": "data", "x": 440, "y": 140, "detail": "Highest database SLA in Google Cloud; requires 3+ regions with TrueTime Paxos."},
            {"id": "cloudsql-ha-sla", "label": "Cloud SQL HA Regional", "product": "99.95% SLA (4.38 hr/yr down)", "group": "g-service-limits", "plane": "data", "x": 440, "y": 280, "detail": "60-second automatic failover; maximum 64TB storage volume size per instance."},
            {"id": "vm-egress-cap", "label": "Compute Egress Cap: 2 Gbps/vCPU", "product": "Tier 1: Max 100 Gbps / Instance", "group": "g-network-limits", "plane": "data", "x": 780, "y": 140, "detail": "Standard networking allows 2Gbps per vCPU up to 32Gbps; Tier 1 networking enables 100Gbps."},
            {"id": "gcs-object-limits", "label": "Cloud Storage Limits", "product": "Max 5TB Object / 11 9s Durability", "group": "g-network-limits", "plane": "data", "x": 780, "y": 280, "detail": "Single object maximum size: 5TB; 11 9s annual durability (99.999999999%)."}
        ],
        [
            {"id": "e1", "from": "sla-serial-math", "to": "spanner-5nines", "label": "1. Counteract Serial Degradation", "plane": "control"},
            {"id": "e2", "from": "sla-parallel-math", "to": "cloudsql-ha-sla", "label": "2. Model Regional HA Redundancy", "plane": "control"},
            {"id": "e3", "from": "spanner-5nines", "to": "vm-egress-cap", "label": "3. Size Compute Bandwidth for DB", "plane": "control"},
            {"id": "e4", "from": "cloudsql-ha-sla", "to": "gcs-object-limits", "label": "4. Verify Storage Limits & SLAs", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Availability Mathematics Synthesis", "edges": ["e1", "e2"], "action": "Applies serial and parallel mathematical formulas to calculate compound system availability.", "why_traversal": "Reveals why chaining services degrades overall SLA and how parallel redundancy cures it.", "protocol": "Reliability Formulas", "plane": "Control Plane"},
            {"n": 2, "title": "Service Limit Validation", "edges": ["e3", "e4"], "action": "Validates network bandwidth quotas (2Gbps/core) and object size limits (5TB max).", "why_traversal": "Ensures architecture proposals never breach hard platform physical ceilings.", "protocol": "Platform Limits Matrix", "plane": "Control Plane"}
        ],
        [
            {"id": "serial-sla-breach-trap", "label": "Serial Dependency Chain Violates Customer Contract", "changes": {"failedNodes": ["sla-serial-math"], "failedEdges": ["e1"]}, "root_cause": "System chained 5 separate services with 99.9% SLAs; actual availability was only 99.5%.", "diverted_path": "Breached 99.9% contractual customer SLA; triggered 25% financial refund penalties.", "blast_radius": "Severe financial loss.", "recovery": "Redesign architecture using asynchronous decoupling (Pub/Sub) and parallel redundant deployments."}
        ],
        # D2
        "Traces Compound Availability Calculation Traversal: Front End (99.99%) * Compute (99.95%) * Database (99.95%) = 99.89% serial availability -> Refactored to 99.999% via multi-region parallel design.",
        "Step-by-step compound availability calculations expose hidden reliability flaws in serial cloud architectures.",
        [
            {"id": "g-serial-chain-calc", "label": "Serial Component Availability Math", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-refactored-parallel", "label": "Refactored Parallel Multi-Region Math", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-sla-contract-met", "label": "Final Contractual Compliance", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "serial-calc", "label": "Serial: 0.9999 * 0.9995 * 0.9995", "product": "Compound Availability: 99.89%", "group": "g-serial-chain-calc", "plane": "control", "x": 140, "y": 200, "detail": "99.89% availability permits 48.6 minutes of downtime every month (Fails 99.99% goal)."},
            {"id": "parallel-calc", "label": "Parallel: 1 - (1 - 0.9995)^2", "product": "Redundant Regions: 99.99997%", "group": "g-refactored-parallel", "plane": "control", "x": 440, "y": 200, "detail": "Two active-active regional clusters reduce un-availability to virtually zero."},
            {"id": "contract-approved", "label": "Satisfies 99.99% Enterprise SLA", "product": "Max Downtime: 4.3 Min / Month", "group": "g-sla-contract-met", "plane": "data", "x": 780, "y": 200, "detail": "Architecture mathematically guaranteed to satisfy contract with high safety margin."}
        ],
        [
            {"id": "e1", "from": "serial-calc", "to": "parallel-calc", "label": "1. Serial Fails SLA -> Introduce Redundancy", "plane": "control"},
            {"id": "e2", "from": "parallel-calc", "to": "contract-approved", "label": "2. Confirm Parallel Math Exceeds Target", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Serial Failure Recognition", "edges": ["e1"], "action": "Calculates compound math: 99.89% fails customer's 99.99% requirement.", "why_traversal": "Demonstrates why single-region multi-tier systems cannot meet four-nines SLAs.", "protocol": "Availability Math", "plane": "Control Plane"},
            {"n": 2, "title": "Parallel Math Verification", "edges": ["e2"], "action": "Dual-region active-active deployment achieves 99.9999%, passing SLA with ease.", "why_traversal": "Proves architectural viability mathematically before writing code.", "protocol": "SLA Certification", "plane": "Data Plane"}
        ],
        [
            {"id": "shared-failure-domain-trap", "label": "Common Mode Failure Invalidates Parallel Math", "changes": {"failedNodes": ["parallel-calc"], "failedEdges": ["e2"]}, "root_cause": "Both parallel regions shared a single global IAM service account that had its permissions revoked.", "diverted_path": "Both regions crashed simultaneously; parallel math became irrelevant.", "blast_radius": "Global outage.", "recovery": "Eliminate shared dependencies across redundant failure domains."}
        ],
        # D3
        "Simulates Network Bandwidth Quota Exhaustion: single Compute Engine VM attempts to egress 15Gbps on 4 vCPUs; packets throttled at 8Gbps (2Gbps/core ceiling).",
        "Understanding compute bandwidth caps (2Gbps per vCPU) prevents network starvation on data-intensive workloads; scaling vCPUs or enabling Tier 1 unlocks higher throughput.",
        [
            {"id": "g-egress-source", "label": "Under-Sized Compute Engine VM", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-network-throttle", "label": "Google Andromeda SDN Bandwidth Enforcer", "type": "project", "scope": "regional", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "stream-attempt", "label": "15Gbps Video Stream Influx", "product": "4 vCPUs (e2-standard-4)", "group": "g-egress-source", "plane": "data", "x": 220, "y": 140, "detail": "Application attempts to stream 15Gbps of data to external clients."},
            {"id": "andromeda-policer", "label": "Andromeda Rate Policer", "product": "Hard Limit: 8 Gbps (4 vCPU * 2Gbps)", "group": "g-egress-source", "plane": "control", "x": 220, "y": 280, "detail": "Andromeda virtual switch drops packets exceeding the 8Gbps hardware ceiling."},
            {"id": "packet-drop-penalty", "label": "46% Packet Drop Rate", "product": "TCP Retransmission Storm", "group": "g-network-throttle", "plane": "data", "x": 700, "y": 140, "detail": "Video streams stutter; clients experience severe buffering and disconnects."},
            {"id": "upsized-tier1-vm", "label": "Resize to 16 vCPU (Tier 1)", "product": "Unlocks 32 Gbps - 100 Gbps", "group": "g-network-throttle", "plane": "data", "x": 700, "y": 280, "detail": "Upsizing VM or enabling Tier 1 networking restores smooth packet delivery with zero drops."}
        ],
        [
            {"id": "e1", "from": "stream-attempt", "to": "andromeda-policer", "label": "1. Exceed 2Gbps/core Bandwidth Ceiling", "plane": "data"},
            {"id": "e2", "from": "andromeda-policer", "to": "packet-drop-penalty", "label": "2. Drop Packets Exceeding 8Gbps", "plane": "control"},
            {"id": "e3", "from": "packet-drop-penalty", "to": "upsized-tier1-vm", "label": "3. Upgrade VM Size to Remove Bottleneck", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Bandwidth Policing", "edges": ["e1", "e2"], "action": "Andromeda SDN enforces hard 2Gbps/vCPU limit, dropping 46% of packets.", "why_traversal": "Demonstrates the physical compute engine network egress limit.", "protocol": "SDN Rate Limiter", "plane": "Data Plane"},
            {"n": 2, "title": "Capacity Expansion Resolution", "edges": ["e3"], "action": "Resizing to 16 vCPUs elevates bandwidth limit to 32Gbps, eliminating packet drops.", "why_traversal": "Sizes network throughput mathematically based on core count.", "protocol": "Compute Engine Machine Sizing", "plane": "Data Plane"}
        ],
        [
            {"id": "unmonitored-egress-drop", "label": "Network Drop Overlooked as CPU Health Looked Normal", "changes": {"failedNodes": ["packet-drop-penalty"], "failedEdges": ["e2"]}, "root_cause": "VM CPU utilization was only 35%; engineers did not realize network bandwidth quota was being throttled.", "diverted_path": "Engineers spent 3 days debugging application code instead of network quota.", "blast_radius": "Delayed resolution of customer buffering.", "recovery": "Monitor 'instance/network/dropped_packets' metric in Cloud Monitoring to alert on bandwidth policing."}
        ]
    )

    return specs

if __name__ == "__main__":
    specs = build_p7_cs_specs()
    print(f"Generated {len(specs)} specs for Phase 7 & CS: {sorted(list(specs.keys()))}")

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spec_p7_cs.py")
    with open(out_path, "w") as f:
        f.write('"""\n')
        f.write('spec_p7_cs.py - Topics 045 to 060\n')
        f.write('Phase 7: Case Studies (045 to 050)\n')
        f.write('Data & ML Specialty Deep-Dives (051 to 054)\n')
        f.write('Cheat Sheets (055 to 060)\n')
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

        for t_no in sorted(specs.keys()):
            s = specs[t_no]
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

    print("Successfully wrote spec_p7_cs.py!")
