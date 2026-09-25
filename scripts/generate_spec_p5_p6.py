#!/usr/bin/env python3
"""
generate_spec_p5_p6.py - Generates spec_p5_p6.py with authentic specifications for:
Phase 5: Security & Compliance (Topics 034 to 039)
Phase 6: DevOps, FinOps & Operations (Topics 040 to 044)
"""

import os
import json

def build_p5_p6_specs():
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

    # 034: Advanced IAM, Federation & Zero Trust
    specs[34] = make_spec(
        34, "5.1", "Advanced IAM, Federation & Zero Trust",
        "Visualizes Enterprise Zero Trust & IAM Architecture: Workforce Identity Federation, BeyondCorp Enterprise Context-Aware Access, Service Account impersonation, and condition-based access controls.",
        "Zero Trust dictates that no network or user is implicitly trusted; authentication and authorization require continuous identity assertion, device posture evaluation, and ephemeral short-lived credentials.",
        [
            {"id": "g-idp", "label": "Enterprise Identity Provider (IdP)", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-beyondcorp", "label": "BeyondCorp Context-Aware Gateway", "type": "organization", "scope": "organization", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-gcp-iam", "label": "Google Cloud IAM & Short-Lived STS", "type": "project", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "okta-idp", "label": "Okta / Azure AD IdP", "product": "SAML 2.0 / OIDC Provider", "group": "g-idp", "plane": "control", "x": 140, "y": 140, "detail": "Corporate directory authenticating enterprise users with hardware MFA keys."},
            {"id": "user-device", "label": "Managed Corporate Laptop", "product": "Chrome Enterprise Client", "group": "g-idp", "plane": "data", "x": 140, "y": 280, "detail": "Corporate device reporting encryption status, OS version, and certificate health."},
            {"id": "caa-engine", "label": "Context-Aware Access", "product": "Access Context Manager", "group": "g-beyondcorp", "plane": "control", "x": 440, "y": 140, "detail": "Evaluates user group, device posture, geographic origin, and IP subnets before granting access."},
            {"id": "sts-broker", "label": "Security Token Service", "product": "Federation STS Token Broker", "group": "g-gcp-iam", "plane": "control", "x": 780, "y": 140, "detail": "Exchanges external OIDC assertion for short-lived (1-hour) Google OAuth2 token."},
            {"id": "sa-impersonation", "label": "Service Account Impersonation", "product": "iam.serviceAccounts.getAccessToken", "group": "g-gcp-iam", "plane": "control", "x": 780, "y": 280, "detail": "Grants temporary access without requiring permanent, downloadable JSON private keys."}
        ],
        [
            {"id": "e1", "from": "okta-idp", "to": "caa-engine", "label": "1. SAML/OIDC Identity Claim", "plane": "control"},
            {"id": "e2", "from": "user-device", "to": "caa-engine", "label": "2. Transmit Device Posture State", "plane": "control"},
            {"id": "e3", "from": "caa-engine", "to": "sts-broker", "label": "3. Authorize Federated Token Minting", "plane": "control"},
            {"id": "e4", "from": "sts-broker", "to": "sa-impersonation", "label": "4. Impersonate Target Workload SA", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Federated Claim & Context Evaluation", "edges": ["e1", "e2"], "action": "Okta authenticates user; Access Context Manager evaluates device encryption and corporate network location.", "why_traversal": "Validates both user identity and device security posture simultaneously.", "protocol": "OIDC + BeyondCorp Posture", "plane": "Control Plane"},
            {"n": 2, "title": "Ephemeral Token Exchange", "edges": ["e3", "e4"], "action": "Google STS validates OIDC claims and exchanges them for a short-lived token impersonating the deployment SA.", "why_traversal": "Completely eliminates downloadable JSON service account keys, extinguishing key leak vectors.", "protocol": "STS Token Exchange API", "plane": "Control Plane"}
        ],
        [
            {"id": "compromised-device-block", "label": "Unencrypted Device Access Denied", "changes": {"failedNodes": ["caa-engine"], "failedEdges": ["e3"]}, "root_cause": "Contractor accessed GCP Console from personal laptop with disk encryption disabled.", "diverted_path": "Context-Aware Access rejects request with HTTP 403 Access Level Violation.", "blast_radius": "Zero compromise of enterprise resources.", "recovery": "Contractor must enable FileVault/BitLocker and enroll device in corporate MDM."}
        ],
        # D2
        "Traces the Workforce Identity Federation Token Exchange Flow: from enterprise OIDC token generation to Google Cloud STS exchange and resource invocation.",
        "Direct token exchange allows enterprise engineers to authenticate to Google Cloud using their existing corporate credentials without creating duplicate Google identities.",
        [
            {"id": "g-client-auth", "label": "Enterprise Developer Workstation", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-sts-auth", "label": "Google Cloud STS Federation Pool", "type": "organization", "scope": "organization", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-res-target", "label": "Target Cloud APIs (BigQuery)", "type": "project", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "dev-cli", "label": "gcloud CLI / Terraform", "product": "Developer Terminal", "group": "g-client-auth", "plane": "control", "x": 140, "y": 140, "detail": "Developer executes gcloud auth login or runs terraform plan."},
            {"id": "okta-auth", "label": "Okta OIDC Endpoint", "product": "Signs OIDC JWT with RSA Key", "group": "g-client-auth", "plane": "control", "x": 140, "y": 280, "detail": "Issues cryptographically signed JWT containing user email and department claims."},
            {"id": "workforce-pool", "label": "Workforce Identity Pool", "product": "Audience Validation & Attribute Mapping", "group": "g-sts-auth", "plane": "control", "x": 440, "y": 200, "detail": "Maps Okta 'groups' claim directly to Google IAM conditional principal roles."},
            {"id": "ephemeral-token", "label": "Short-Lived Access Token", "product": "OAuth2 Token (1 Hour TTL)", "group": "g-res-target", "plane": "control", "x": 780, "y": 140, "detail": "Valid for exactly 3600 seconds; automatically refreshed by gcloud."},
            {"id": "bigquery-api", "label": "BigQuery Data Access", "product": "Evaluates IAM Dataset Roles", "group": "g-res-target", "plane": "data", "x": 780, "y": 280, "detail": "Executes SQL query within authorized dataset boundaries."}
        ],
        [
            {"id": "e1", "from": "dev-cli", "to": "okta-auth", "label": "1. Request OIDC Token (PKCE)", "plane": "control"},
            {"id": "e2", "from": "okta-auth", "to": "workforce-pool", "label": "2. Submit JWT to Google STS", "plane": "control"},
            {"id": "e3", "from": "workforce-pool", "to": "ephemeral-token", "label": "3. Mint 60-Minute Google Token", "plane": "control"},
            {"id": "e4", "from": "ephemeral-token", "to": "bigquery-api", "label": "4. Query Production Analytics", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Corporate Authentication", "edges": ["e1", "e2"], "action": "Developer authenticates with Okta; CLI sends signed JWT to Google Workforce Pool.", "why_traversal": "Maintains single centralized enterprise authentication source.", "protocol": "OIDC OAuth 2.0 PKCE", "plane": "Control Plane"},
            {"n": 2, "title": "Federated Token Issuance", "edges": ["e3", "e4"], "action": "Google STS maps claims and issues short-lived token to execute authorized BigQuery queries.", "why_traversal": "Ensures zero static secrets exist on developer workstations.", "protocol": "REST / Google APIs", "plane": "Data Plane"}
        ],
        [
            {"id": "claim-mapping-mismatch", "label": "Attribute Mapping Claim Mismatch", "changes": {"failedNodes": ["workforce-pool"], "failedEdges": ["e3"]}, "root_cause": "Okta sent 'department' claim but Google Pool expected 'dept_name'.", "diverted_path": "STS token issued without BigQuery roles; queries rejected with HTTP 403.", "blast_radius": "Data engineers unable to run scheduled analytics.", "recovery": "Correct attribute mapping expression in Workforce Identity Pool configuration."}
        ],
        # D3
        "Simulates Service Account Key Compromise & Automated Quarantine: detects key leak on GitHub and revokes credentials within 5 seconds.",
        "Cloud Asset Inventory and Eventarc integrate with secret scanning partners to detect leaked service account keys and automatically disable them before exploitation.",
        [
            {"id": "g-leak-source", "label": "Public GitHub Repository Leak", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-auto-defense", "label": "Automated Key Revocation Engine", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "leaked-key", "label": "Exposed JSON SA Key", "product": "Accidental Public Git Commit", "group": "g-leak-source", "plane": "data", "x": 220, "y": 140, "detail": "Developer accidentally committed service-account-key.json to public GitHub repo."},
            {"id": "github-scanner", "label": "GitHub Secret Scanning", "product": "Real-time Partner Webhook", "group": "g-leak-source", "plane": "control", "x": 220, "y": 280, "detail": "Identifies Google Cloud private key pattern within 2 seconds of git push."},
            {"id": "eventarc-ingest", "label": "Eventarc Security Receiver", "product": "Cloud Event Router", "group": "g-auto-defense", "plane": "control", "x": 700, "y": 140, "detail": "Receives key compromise event; routes to automated revocation function."},
            {"id": "iam-disabler", "label": "Cloud Functions Key Revoker", "product": "iam.serviceAccountKeys.disable", "group": "g-auto-defense", "plane": "control", "x": 700, "y": 280, "detail": "Calls IAM Admin API to disable leaked key ID in 3.4 seconds."}
        ],
        [
            {"id": "e1", "from": "leaked-key", "to": "github-scanner", "label": "1. Git Push Exposes Secret", "plane": "control"},
            {"id": "e2", "from": "github-scanner", "to": "eventarc-ingest", "label": "2. Send Partner Compromise Alert", "plane": "control"},
            {"id": "e3", "from": "eventarc-ingest", "to": "iam-disabler", "label": "3. Trigger Automated Revocation", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Secret Detection & Ingestion", "edges": ["e1", "e2"], "action": "GitHub scans commit, identifies GCP private key, and notifies Google Security webhook.", "why_traversal": "Catches exposure within seconds before malicious actors can exploit it.", "protocol": "HTTPS Webhook Notification", "plane": "Control Plane"},
            {"n": 2, "title": "Automated Key Deactivation", "edges": ["e3"], "action": "Function disables key immediately and notifies security operations in Slack.", "why_traversal": "Reduces exposure window from days to under 4 seconds.", "protocol": "IAM Admin REST API", "plane": "Control Plane"}
        ],
        [
            {"id": "disabled-key-prod-outage", "label": "Revoked Key Halts Production Batch Job", "changes": {"failedNodes": ["iam-disabler"], "failedEdges": ["e3"]}, "root_cause": "The leaked key was actively shared with a critical production billing batch process.", "diverted_path": "Batch job fails with HTTP 401 Unauthorized.", "blast_radius": "Temporary batch processing pause.", "recovery": "Migrate production batch jobs to Workload Identity Federation, eliminating JSON keys forever."}
        ]
    )

    # 035: Network Security: VPC-SC & Cloud Armor
    specs[35] = make_spec(
        35, "5.2", "Network Security: VPC-SC & Cloud Armor",
        "Visualizes Multi-Layer Network Security: Cloud Armor WAF and DDoS mitigation at the edge, coupled with VPC Service Controls (VPC-SC) perimeters protecting confidential BigQuery and Cloud Storage assets.",
        "Defense-in-depth requires filtering malicious inbound traffic at the Google edge (Cloud Armor) while simultaneously preventing authorized compute instances from exfiltrating sensitive data to unauthorized external endpoints (VPC-SC).",
        [
            {"id": "g-armor-edge", "label": "Google Edge: Cloud Armor WAF", "type": "external", "scope": "global", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-vpc-dmz", "label": "DMZ VPC: Frontend Microservices", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-vpcsc-perimeter", "label": "VPC-SC Perimeter: Core Data Vault", "type": "project", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "armor-waf", "label": "Cloud Armor Enterprise", "product": "OWASP Top 10 + DDoS Defense", "group": "g-armor-edge", "plane": "data", "x": 140, "y": 140, "detail": "Blocks SQLi, XSS, and L7 HTTP floods; evaluates client IP reputation scores."},
            {"id": "rate-limiter", "label": "Adaptive Rate Limiting", "product": "Max 500 req/min per IP", "group": "g-armor-edge", "plane": "data", "x": 140, "y": 280, "detail": "Throttles brute-force login attempts and automated credential stuffing bots."},
            {"id": "frontend-gke", "label": "GKE Microservice Fleet", "product": "Internal Workloads (Private Subnet)", "group": "g-vpc-dmz", "plane": "data", "x": 440, "y": 200, "detail": "Processes client requests; calls backend storage via Private Service Connect."},
            {"id": "vpcsc-guard", "label": "VPC Service Perimeter", "product": "Access Context Manager Rules", "group": "g-vpcsc-perimeter", "plane": "control", "x": 780, "y": 140, "detail": "Strict boundary enclosing BigQuery and GCS; blocks data transfers outside perimeter."},
            {"id": "secure-bq", "label": "Confidential BigQuery Data", "product": "Protected Analytic Dataset", "group": "g-vpcsc-perimeter", "plane": "data", "x": 780, "y": 280, "detail": "Customer PII data accessible only from authorized IPs and VPC perimeters."}
        ],
        [
            {"id": "e1", "from": "armor-waf", "to": "frontend-gke", "label": "1. Forward Sanitized Traffic", "plane": "data"},
            {"id": "e2", "from": "rate-limiter", "to": "frontend-gke", "label": "2. Allow Valid Rate Ingress", "plane": "data"},
            {"id": "e3", "from": "frontend-gke", "to": "vpcsc-guard", "label": "3. Cross-Perimeter PSC Query", "plane": "data"},
            {"id": "e4", "from": "vpcsc-guard", "to": "secure-bq", "label": "4. Verify Ingress Policy & Query", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Edge Threat Filtering", "edges": ["e1", "e2"], "action": "Cloud Armor inspects HTTP request, blocks SQL injection attempt, and permits clean traffic.", "why_traversal": "Eliminates attack payloads before they reach application containers.", "protocol": "WAF Rule Engine", "plane": "Data Plane"},
            {"n": 2, "title": "Perimeter Verification & Data Access", "edges": ["e3", "e4"], "action": "VPC-SC validates that request originates from authorized GKE VPC and permits BigQuery read.", "why_traversal": "Strictly isolates sensitive data from unauthorized exfiltration routes.", "protocol": "VPC Service Controls Enforcement", "plane": "Control Plane"}
        ],
        [
            {"id": "data-exfil-attempt", "label": "Insider Data Exfiltration Thwarted", "changes": {"failedNodes": ["vpcsc-guard"], "failedEdges": ["e4"]}, "root_cause": "Compromised GKE pod attempted to copy BigQuery data to an external personal GCS bucket.", "diverted_path": "VPC-SC blocks outbound transfer: VPC_SERVICE_CONTROLS_VIOLATION.", "blast_radius": "Zero data leaked; security alert dispatched to SCC in real time.", "recovery": "Investigate compromised pod, rotate pod service account, and quarantine node."}
        ],
        # D2
        "Traces Multi-Perimeter Ingress/Egress Communication: how GKE in Project A securely accesses BigQuery in Project B using explicit VPC Service Controls Ingress & Egress rules.",
        "VPC Service Controls allows granular perimeter bridging using cryptographically validated identity and network constraints without merging entire projects into a single flat network.",
        [
            {"id": "g-perim-a", "label": "Perimeter Alpha: App Services (Project A)", "type": "project", "scope": "regional", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-egress-rule", "label": "Access Context Manager Ingress/Egress Rules", "type": "organization", "scope": "organization", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-perim-b", "label": "Perimeter Beta: Data Lakehouse (Project B)", "type": "project", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "app-sa-caller", "label": "App Service Account", "product": "app-runner@proj-a.iam.gserviceaccount.com", "group": "g-perim-a", "plane": "data", "x": 140, "y": 200, "detail": "GKE pod executing transactional analytics query across project boundaries."},
            {"id": "egress-policy", "label": "Perimeter A Egress Rule", "product": "Allows egress to Proj B for BigQuery", "group": "g-egress-rule", "plane": "control", "x": 440, "y": 140, "detail": "Specifies from identity: app-runner, to service: bigquery.googleapis.com."},
            {"id": "ingress-policy", "label": "Perimeter B Ingress Rule", "product": "Allows ingress from Perimeter A", "group": "g-egress-rule", "plane": "control", "x": 440, "y": 280, "detail": "Validates caller identity and source project before admitting request."},
            {"id": "bq-lakehouse", "label": "Project B BigQuery Dataset", "product": "orders_fact Table", "group": "g-perim-b", "plane": "data", "x": 780, "y": 200, "detail": "Executes query and streams partitioned results back to Project A."}
        ],
        [
            {"id": "e1", "from": "app-sa-caller", "to": "egress-policy", "label": "1. Initiate Cross-Project Call", "plane": "data"},
            {"id": "e2", "from": "egress-policy", "to": "ingress-policy", "label": "2. Match Egress Rule & Bridge", "plane": "control"},
            {"id": "e3", "from": "ingress-policy", "to": "bq-lakehouse", "label": "3. Match Ingress Rule & Execute", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Egress Policy Validation", "edges": ["e1", "e2"], "action": "Perimeter A checks egress policy: caller is authorized to contact BigQuery in Project B.", "why_traversal": "Prevents unauthorized outbound calls while allowing approved workflows.", "protocol": "VPC-SC Egress Rule", "plane": "Control Plane"},
            {"n": 2, "title": "Ingress Admittance", "edges": ["e3"], "action": "Perimeter B confirms caller identity matches ingress whitelist and executes query.", "why_traversal": "Secures data perimeter from arbitrary external callers.", "protocol": "VPC-SC Ingress Rule", "plane": "Data Plane"}
        ],
        [
            {"id": "unauthorized-method-block", "label": "Unauthorized Storage API Method Blocked", "changes": {"failedNodes": ["ingress-policy"], "failedEdges": ["e3"]}, "root_cause": "Caller attempted to call storage.buckets.delete instead of permitted bigquery.tables.getData.", "diverted_path": "VPC-SC evaluates method constraint and rejects deletion attempt.", "blast_radius": "Zero data loss.", "recovery": "Restrict caller permissions strictly to read-only analytical operations."}
        ],
        # D3
        "Simulates Cloud Armor Adaptive Protection: automated machine learning detects a Layer 7 HTTP flood attack, generates a custom WAF signature, and blocks attack traffic.",
        "Adaptive Protection analyzes traffic baselines using machine learning, automatically producing targeted rules to neutralize novel zero-day application attacks.",
        [
            {"id": "g-ddos-flood", "label": "Distributed Botnet (100,000 IPs)", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-armor-defense", "label": "Cloud Armor Adaptive Protection Engine", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "botnet-flood", "label": "L7 HTTP Flood (1M QPS)", "product": "Automated Headless Browsers", "group": "g-ddos-flood", "plane": "data", "x": 220, "y": 140, "detail": "Botnet sends 1,000,000 requests/sec with rotating User-Agent strings."},
            {"id": "ml-detector", "label": "Adaptive Threat Analyzer", "product": "Real-time Traffic Anomaly ML", "group": "g-ddos-flood", "plane": "control", "x": 220, "y": 280, "detail": "Identifies common attack fingerprint in HTTP headers within 45 seconds."},
            {"id": "auto-waf-rule", "label": "Dynamic WAF Rule Generated", "product": "Rule: deny if header matches signature", "group": "g-armor-defense", "plane": "control", "x": 700, "y": 140, "detail": "Generates rule with confidence score 0.98; deploys to edge proxy in 2 seconds."},
            {"id": "edge-drop", "label": "Edge Traffic Drop (HTTP 429)", "product": "Google Anycast PoP Edge", "group": "g-armor-defense", "plane": "data", "x": 700, "y": 280, "detail": "Drops 99.8% of botnet traffic at edge PoPs worldwide; backend origin CPU drops to 20%."}
        ],
        [
            {"id": "e1", "from": "botnet-flood", "to": "ml-detector", "label": "1. Analyze Influx Fingerprint", "plane": "control"},
            {"id": "e2", "from": "ml-detector", "to": "auto-waf-rule", "label": "2. Synthesize Signature & Rule", "plane": "control"},
            {"id": "e3", "from": "auto-waf-rule", "to": "edge-drop", "label": "3. Enforce Rule at Global Edge", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Anomaly Identification", "edges": ["e1", "e2"], "action": "Adaptive Protection ML correlates requests across 100k IPs and extracts distinguishing header.", "why_traversal": "Identifies complex distributed attacks that evade simple rate limiters.", "protocol": "Machine Learning Anomaly Engine", "plane": "Control Plane"},
            {"n": 2, "title": "Automated Edge Mitigation", "edges": ["e3"], "action": "Cloud Armor deploys targeted rule to all edge points of presence, dropping flood packets.", "why_traversal": "Protects backend web servers from exhaustion and eliminates origin egress charges.", "protocol": "Cloud Armor Rule Deployment", "plane": "Data Plane"}
        ],
        [
            {"id": "rule-false-positive-risk", "label": "Overly Broad Signature Drops Legitimate Users", "changes": {"failedNodes": ["auto-waf-rule"], "failedEdges": ["e3"]}, "root_cause": "Signature used common header shared by legitimate mobile application users.", "diverted_path": "Legitimate customers receive HTTP 429 errors.", "blast_radius": "Customer checkout disruption.", "recovery": "Deploy Adaptive Protection rules in preview mode first and refine signature with multi-attribute matching."}
        ]
    )

    # 036: Data Protection: Cloud KMS & DLP
    specs[36] = make_spec(
        36, "5.3", "Data Protection: Cloud KMS & DLP",
        "Visualizes Cryptographic Hierarchy & Sensitive Data Protection: Cloud KMS (CMEK, Cloud EKM, HSM, Key Rings) combined with Cloud DLP automated inspection, de-identification, and crypto-tokenization.",
        "Comprehensive data protection requires securing data at rest with customer-managed cryptographic keys (CMEK) while automatically identifying and pseudonymizing sensitive PII before analytical persistence.",
        [
            {"id": "g-kms-tier", "label": "Cryptographic Hierarchy: Cloud KMS", "type": "project", "scope": "global", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-dlp-pipeline", "label": "Automated Sensitive Data Protection (DLP)", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-secure-storage", "label": "Protected Storage & Analytics", "type": "project", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "cloud-hsm-key", "label": "Cloud HSM Key Ring", "product": "FIPS 140-2 Level 3 Hardware Key", "group": "g-kms-tier", "plane": "control", "x": 140, "y": 140, "detail": "Hardware security module storing root encryption keys with automatic annual rotation."},
            {"id": "dek-generator", "label": "Data Encryption Key (DEK)", "product": "Envelope Encryption Engine", "group": "g-kms-tier", "plane": "control", "x": 140, "y": 280, "detail": "Generates local AES-256 keys to encrypt raw records; wrapped by Key Encryption Key (KEK)."},
            {"id": "dlp-inspect", "label": "Cloud DLP Inspect Engine", "product": "InfoType Detection (SSN, Cards)", "group": "g-dlp-pipeline", "plane": "data", "x": 440, "y": 140, "detail": "Scans raw files using built-in infoTypes to identify social security and credit card numbers."},
            {"id": "dlp-tokenize", "label": "Crypto-Tokenization Engine", "product": "Deterministic Pseudonymization", "group": "g-dlp-pipeline", "plane": "data", "x": 440, "y": 280, "detail": "Replaces sensitive SSN with encrypted token: TOKEN_#8921_x9f preserving format."},
            {"id": "sanitized-bq", "label": "Sanitized BigQuery Data", "product": "CMEK-Encrypted Dataset", "group": "g-secure-storage", "plane": "data", "x": 780, "y": 200, "detail": "Stores tokenized analytical records encrypted at rest using Cloud KMS HSM key."}
        ],
        [
            {"id": "e1", "from": "cloud-hsm-key", "to": "dek-generator", "label": "1. Wrap Local DEK with HSM KEK", "plane": "control"},
            {"id": "e2", "from": "dlp-inspect", "to": "dlp-tokenize", "label": "2. Flag PII & Invoke Tokenizer", "plane": "data"},
            {"id": "e3", "from": "dek-generator", "to": "sanitized-bq", "label": "3. Encrypt Dataset with CMEK", "plane": "control"},
            {"id": "e4", "from": "dlp-tokenize", "to": "sanitized-bq", "label": "4. Persist De-Identified Records", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Envelope Encryption & Key Wrapping", "edges": ["e1", "e3"], "action": "Cloud KMS generates wrapped DEK for BigQuery storage encryption.", "why_traversal": "Delivers cryptographic key ownership with zero performance degradation on large tables.", "protocol": "KMS Envelope Encryption", "plane": "Control Plane"},
            {"n": 2, "title": "PII Inspection & Tokenization", "edges": ["e2", "e4"], "action": "Cloud DLP scans payload, identifies sensitive infoTypes, tokenizes them, and writes to BigQuery.", "why_traversal": "Allows analysts to query sanitized data without exposing raw PII.", "protocol": "Cloud DLP REST API", "plane": "Data Plane"}
        ],
        [
            {"id": "key-disable-kill-switch", "label": "Emergency CMEK Revocation Shuts Down Access", "changes": {"failedNodes": ["cloud-hsm-key"], "failedEdges": ["e1", "e3"]}, "root_cause": "Security incident response officer disabled the KEK in Cloud KMS.", "diverted_path": "All reads and writes to BigQuery instantly blocked across all users.", "blast_radius": "Immediate dataset freeze.", "recovery": "Re-enable KEK version in Cloud KMS once security threat is resolved."}
        ],
        # D2
        "Traces Automated Data De-Identification Flow: raw CSV upload to Cloud Storage -> Eventarc notification -> Cloud Run DLP execution -> CMEK-encrypted BigQuery ingestion.",
        "Automating data de-identification at the ingestion boundary ensures raw sensitive information never enters enterprise analytical data lakes.",
        [
            {"id": "g-raw-drop", "label": "Secure Staging Ingestion", "type": "project", "scope": "regional", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-sanitize-svc", "label": "Serverless Sanitization Pipeline", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-clean-lake", "label": "Governed Analytic Storage", "type": "project", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "raw-gcs-bucket", "label": "Raw Ingestion GCS Bucket", "product": "Retention Policy = 24 Hours", "group": "g-raw-drop", "plane": "data", "x": 140, "y": 140, "detail": "Staging bucket with CMEK encryption receiving customer CSV batch dumps."},
            {"id": "eventarc-trigger", "label": "Eventarc Object Finalize", "product": "CloudEvents Router", "group": "g-raw-drop", "plane": "control", "x": 140, "y": 280, "detail": "Emits google.cloud.storage.object.v1.finalized event on upload."},
            {"id": "run-dlp-worker", "label": "Cloud Run DLP Processor", "product": "Inspect & De-Identify Service", "group": "g-sanitize-svc", "plane": "data", "x": 440, "y": 200, "detail": "Streams records through DLP API; masks emails and tokenizes government IDs."},
            {"id": "cmek-bq-table", "label": "BigQuery Target Table", "product": "CMEK-Protected Lakehouse", "group": "g-clean-lake", "plane": "data", "x": 780, "y": 140, "detail": "Analytical table containing only pseudonymized records ready for business BI."},
            {"id": "gcs-purge", "label": "Auto-Delete Raw Object", "product": "Lifecycle Expiration (Immediate)", "group": "g-clean-lake", "plane": "control", "x": 780, "y": 280, "detail": "Permanently deletes raw staging file from GCS once sanitization succeeds."}
        ],
        [
            {"id": "e1", "from": "raw-gcs-bucket", "to": "eventarc-trigger", "label": "1. Object Created Event", "plane": "control"},
            {"id": "e2", "from": "eventarc-trigger", "to": "run-dlp-worker", "label": "2. Trigger Processing Worker", "plane": "control"},
            {"id": "e3", "from": "run-dlp-worker", "to": "cmek-bq-table", "label": "3. Stream Sanitized Rows", "plane": "data"},
            {"id": "e4", "from": "cmek-bq-table", "to": "gcs-purge", "label": "4. Purge Unredacted Staging File", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Ingestion Eventing", "edges": ["e1", "e2"], "action": "Upload to GCS fires Eventarc event; Cloud Run container starts instantly.", "why_traversal": "Serverless event-driven architecture scales to zero when no uploads occur.", "protocol": "CloudEvents / HTTP", "plane": "Control Plane"},
            {"n": 2, "title": "Sanitization & Storage", "edges": ["e3", "e4"], "action": "DLP transforms sensitive fields; clean data lands in BigQuery; staging file is destroyed.", "why_traversal": "Minimizes time unredacted data resides in cloud storage to under 30 seconds.", "protocol": "BigQuery Storage Write API", "plane": "Data Plane"}
        ],
        [
            {"id": "dlp-quota-backlog", "label": "DLP API Quota Exhaustion", "changes": {"failedNodes": ["run-dlp-worker"], "failedEdges": ["e3"]}, "root_cause": "Sudden upload of 5,000 files exceeded regional DLP inspection byte quota.", "diverted_path": "Cloud Run worker receives HTTP 429 Too Many Requests; files queue.", "blast_radius": "Delayed data ingestion for business reports.", "recovery": "Request quota increase and implement Cloud Tasks queue with controlled concurrency rate."}
        ],
        # D3
        "Simulates External Key Manager (Cloud EKM) Network Failure: demonstrates automated fail-safe behavior when external enterprise key server is unreachable.",
        "Cloud EKM ensures data can only be decrypted when an external enterprise key management system approves the request; if the EKM connection fails, data remains cryptographically locked.",
        [
            {"id": "g-onprem-ekm", "label": "On-Premises Thales / Fortanix EKM", "type": "onprem", "scope": "onprem", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-cloud-ekm-target", "label": "Google Cloud EKM Integration", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "onprem-hsm-server", "label": "On-Prem HSM Key Manager", "product": "Enterprise EKM Appliance", "group": "g-onprem-ekm", "plane": "control", "x": 220, "y": 140, "detail": "Maintains physical custody of master encryption keys outside Google Cloud."},
            {"id": "ekm-vpn-interconnect", "label": "Cloud Interconnect / EKM VPN", "product": "Private EKM Network Path", "group": "g-onprem-ekm", "plane": "data", "x": 220, "y": 280, "detail": "Carries TLS wrapped key unwrap requests from Google Cloud to enterprise HSM."},
            {"id": "cloud-ekm-bridge", "label": "Cloud EKM Gateway", "product": "Google Cloud KMS EKM Endpoint", "group": "g-cloud-ekm-target", "plane": "control", "x": 700, "y": 140, "detail": "Relays cryptographic requests to enterprise EKM server."},
            {"id": "locked-storage", "label": "Locked BigQuery / GCS Data", "product": "Un-decryptable Ciphertext", "group": "g-cloud-ekm-target", "plane": "data", "x": 700, "y": 280, "detail": "Data cannot be decrypted by Google or anyone else while EKM is offline."}
        ],
        [
            {"id": "e1", "from": "onprem-hsm-server", "to": "ekm-vpn-interconnect", "label": "1. Provide Key Access Justification", "plane": "control"},
            {"id": "e2", "from": "ekm-vpn-interconnect", "to": "cloud-ekm-bridge", "label": "2. Forward Decryption Authorization", "plane": "control"},
            {"id": "e3", "from": "cloud-ekm-bridge", "to": "locked-storage", "label": "3. Decrypt Ciphertext Blocks", "plane": "data"}
        ],
        [
            {"n": 1, "title": "External Key Negotiation", "edges": ["e1", "e2"], "action": "Cloud KMS connects to on-prem EKM, providing audit justification reason for key access.", "why_traversal": "Customer maintains absolute cryptographic sovereignty over data decryption.", "protocol": "Cloud EKM Protocol / TLS", "plane": "Control Plane"},
            {"n": 2, "title": "Data Decryption", "edges": ["e3"], "action": "Upon receiving unwrapped key from on-prem HSM, BigQuery decrypts storage blocks.", "why_traversal": "Proves that Google cannot decrypt data without external customer consent.", "protocol": "AES-256 GCM Decryption", "plane": "Data Plane"}
        ],
        [
            {"id": "ekm-network-severed", "label": "Enterprise EKM Network Outage", "changes": {"failedNodes": ["ekm-vpn-interconnect"], "failedEdges": ["e2"]}, "root_cause": "On-premise enterprise firewall reboot severed TLS connection to Cloud EKM.", "diverted_path": "Cloud EKM fails closed; all BigQuery queries fail with 'EKM_UNREACHABLE'.", "blast_radius": "Data operations halted until enterprise network recovers.", "recovery": "Restore on-premise firewall and configure redundant Cloud Interconnect paths for EKM traffic."}
        ]
    )

    # 037: Compliance, Governance & Assured Workloads
    specs[37] = make_spec(
        37, "5.4", "Compliance, Governance & Assured Workloads",
        "Visualizes Regulated Compliance Architecture: Assured Workloads (FedRAMP High, HIPAA, CJIS, EU Sovereignty), Key Access Justifications (KAJ), and Personnel Access Controls (PAC).",
        "Assured Workloads enforces regulatory boundaries at the folder level through immutable organization policies, guaranteeing data residency and restricting Google personnel access.",
        [
            {"id": "g-gov-control", "label": "Enterprise Compliance & Governance", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-assured-folder", "label": "Assured Workloads Regulated Folder", "type": "project", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-google-support", "label": "Google Cloud Support & KAJ Boundary", "type": "external", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "compliance-officer", "label": "Enterprise CISO / Auditor", "product": "Regulatory Oversight", "group": "g-gov-control", "plane": "control", "x": 140, "y": 140, "detail": "Monitors compliance posture and reviews access justification logs in real time."},
            {"id": "org-guardrail", "label": "Org Policy Guardrails", "product": "Resource Location Restriction", "group": "g-gov-control", "plane": "control", "x": 140, "y": 280, "detail": "Restricts resource provisioning strictly to compliant regions (e.g., us-gov-west1 or europe-west3)."},
            {"id": "assured-env", "label": "FedRAMP High Environment", "product": "Assured Workloads Project", "group": "g-assured-folder", "plane": "data", "x": 440, "y": 200, "detail": "Hosts government workloads with FIPS 140-2 encryption and CJIS background-checked support."},
            {"id": "kaj-enforcer", "label": "Key Access Justifications (KAJ)", "product": "Policy Approval Gate", "group": "g-google-support", "plane": "control", "x": 780, "y": 140, "detail": "Evaluates rationale before Google Cloud support personnel can access encryption keys."},
            {"id": "pac-restricted", "label": "Personnel Access Controls (PAC)", "product": "US Persons Only (FedRAMP)", "group": "g-google-support", "plane": "control", "x": 780, "y": 280, "detail": "Guarantees that only vetted US citizens located in the US handle technical support."}
        ],
        [
            {"id": "e1", "from": "compliance-officer", "to": "org-guardrail", "label": "1. Deploy Compliance Baseline", "plane": "control"},
            {"id": "e2", "from": "org-guardrail", "to": "assured-env", "label": "2. Enforce Folder Constraints", "plane": "control"},
            {"id": "e3", "from": "assured-env", "to": "kaj-enforcer", "label": "3. Log Support Access Request", "plane": "control"},
            {"id": "e4", "from": "kaj-enforcer", "to": "pac-restricted", "label": "4. Verify Justification & Citizenship", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Regulatory Guardrail Enforcement", "edges": ["e1", "e2"], "action": "Assured Workloads folder applies automated constraints blocking non-compliant regions.", "why_traversal": "Eliminates risk of human error violating sovereign residency laws.", "protocol": "Org Policy as Code", "plane": "Control Plane"},
            {"n": 2, "title": "Support Access Justification Audit", "edges": ["e3", "e4"], "action": "When support ticket is opened, KAJ demands automated justification and verifies PAC vetting.", "why_traversal": "Ensures cloud provider personnel cannot access customer data without explicit logged consent.", "protocol": "KAJ Webhook Verification", "plane": "Control Plane"}
        ],
        [
            {"id": "location-constraint-violation", "label": "Deployment Blocked in Non-Compliant Region", "changes": {"failedNodes": ["org-guardrail"], "failedEdges": ["e2"]}, "root_cause": "Terraform script attempted to spin up GCS bucket in asia-east1 within FedRAMP folder.", "diverted_path": "Resource Manager blocks API call: 'Violates constraints/gcp.resourceLocations'.", "blast_radius": "Zero regulatory violation.", "recovery": "Update Terraform configuration to target authorized region us-gov-west1."}
        ],
        # D2
        "Traces Support Case Elevation with Key Access Justifications: how a Google support engineer requests access, triggering automated KAJ approval and audit logging.",
        "Key Access Justifications provides visibility and automated veto power over every single Google administrative access attempt to your encrypted data.",
        [
            {"id": "g-support-req", "label": "Google Cloud Support Tier", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-kaj-policy", "label": "Customer Key Access Justification Engine", "type": "organization", "scope": "organization", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-audit-trail", "label": "Enterprise Security Information & Event Management", "type": "project", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "support-ticket", "label": "Support Ticket #49102", "product": "Customer Support Investigation", "group": "g-support-req", "plane": "control", "x": 140, "y": 140, "detail": "Support engineer investigates kernel memory fault reported by customer."},
            {"id": "access-approval", "label": "Access Approval Request", "product": "Access Transparency Elevation", "group": "g-support-req", "plane": "control", "x": 140, "y": 280, "detail": "Requests temporary read access to VM diagnostic crash dump."},
            {"id": "kaj-rule-eval", "label": "KAJ Automated Policy", "product": "Reason: CUSTOMER_INITIATED_SUPPORT", "group": "g-kaj-policy", "plane": "control", "x": 440, "y": 200, "detail": "Validates reason against open ticket number; approves single-use decryption token."},
            {"id": "chronicle-siem", "label": "Chronicle SIEM Log Sink", "product": "Access Transparency Audit Log", "group": "g-audit-trail", "plane": "control", "x": 780, "y": 140, "detail": "Logs exact engineer ID, timestamp, justification string, and affected resource."},
            {"id": "ciso-alert", "label": "SecOps Notification", "product": "Slack #compliance-alerts", "group": "g-audit-trail", "plane": "control", "x": 780, "y": 280, "detail": "Notifies enterprise compliance team of approved administrative access."}
        ],
        [
            {"id": "e1", "from": "support-ticket", "to": "access-approval", "label": "1. Escalate Ticket for Access", "plane": "control"},
            {"id": "e2", "from": "access-approval", "to": "kaj-rule-eval", "label": "2. Submit Justification Code", "plane": "control"},
            {"id": "e3", "from": "kaj-rule-eval", "to": "chronicle-siem", "label": "3. Publish Access Transparency Event", "plane": "control"},
            {"id": "e4", "from": "chronicle-siem", "to": "ciso-alert", "label": "4. Broadcast to SecOps Team", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Support Request Justification", "edges": ["e1", "e2"], "action": "Support engineer requests access with reason CUSTOMER_INITIATED_SUPPORT.", "why_traversal": "Requires clear operational necessity before any administrative access.", "protocol": "Access Approval API", "plane": "Control Plane"},
            {"n": 2, "title": "Transparent Audit Logging", "edges": ["e3", "e4"], "action": "Access Transparency records immutable audit entry; SecOps receives instant notification.", "why_traversal": "Delivers indisputable proof of cloud provider interactions for regulatory auditors.", "protocol": "Cloud Audit Logging", "plane": "Control Plane"}
        ],
        [
            {"id": "unjustified-access-denied", "label": "Arbitrary Access Request Denied by KAJ", "changes": {"failedNodes": ["kaj-rule-eval"], "failedEdges": ["e3"]}, "root_cause": "Support request had invalid ticket reference code.", "diverted_path": "KAJ automatically rejects key unwrap; engineer blocked from viewing data.", "blast_radius": "Zero data exposure.", "recovery": "Support engineer must associate valid customer ticket and obtain explicit customer sign-off."}
        ],
        # D3
        "Simulates Sovereign Boundary Breach Prevention: demonstrates Organization Policy blocking unauthorized cross-border replication of EU medical records.",
        "Org policy constraints enforce absolute territorial sovereignty, terminating data replication jobs that attempt to egress data outside legal jurisdictions.",
        [
            {"id": "g-eu-perimeter", "label": "Sovereign European Data Boundary (europe-west3)", "type": "region", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-illegal-egress", "label": "Non-Compliant Destination (us-central1)", "type": "region", "scope": "regional", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "gdpr-patient-db", "label": "EU GDPR Patient Database", "product": "europe-west3 Cloud Spanner", "group": "g-eu-perimeter", "plane": "data", "x": 220, "y": 140, "detail": "Contains 10 million European electronic health records governed by GDPR Article 44."},
            {"id": "sovereign-guardrail", "label": "Sovereignty Org Policy", "product": "constraints/gcp.restrictNonEUDataTransfer", "group": "g-eu-perimeter", "plane": "control", "x": 220, "y": 280, "detail": "Strictly forbids data replication outside European Union data centers."},
            {"id": "cross-border-backup", "label": "Unauthorized US Replication Job", "product": "Storage Transfer Service Job", "group": "g-illegal-egress", "plane": "control", "x": 700, "y": 140, "detail": "Misconfigured disaster recovery job attempted to mirror database to us-central1."},
            {"id": "rejection-enforce", "label": "Data Transfer Blocked (403)", "product": "Sovereign Perimeter Shield", "group": "g-illegal-egress", "plane": "control", "x": 700, "y": 280, "detail": "Terminates replication pipeline; dispatches high-urgency compliance incident."}
        ],
        [
            {"id": "e1", "from": "cross-border-backup", "to": "gdpr-patient-db", "label": "1. Attempt Cross-Border Read", "plane": "control"},
            {"id": "e2", "from": "gdpr-patient-db", "to": "sovereign-guardrail", "label": "2. Evaluate Transfer Boundary", "plane": "control"},
            {"id": "e3", "from": "sovereign-guardrail", "to": "rejection-enforce", "label": "3. Block Transfer & Alert CISO", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Boundary Enforcement", "edges": ["e1", "e2"], "action": "Replication job queries patient database; Org Policy intercepts destination parameter.", "why_traversal": "Validates legal jurisdiction boundaries before transferring any byte.", "protocol": "Cloud Resource Policy Engine", "plane": "Control Plane"},
            {"n": 2, "title": "Hard Block & Compliance Containment", "edges": ["e3"], "action": "Transfer aborted; Security Command Center files high-severity sovereignty incident.", "why_traversal": "Prevents catastrophic GDPR regulatory fines ($20M+ or 4% of global turnover).", "protocol": "Security Policy Enforcement", "plane": "Control Plane"}
        ],
        [
            {"id": "manual-export-leak", "label": "Manual Cloud Shell GCS Download Attempt", "changes": {"failedNodes": ["rejection-enforce"], "failedEdges": ["e3"]}, "root_cause": "Developer attempted to download patient CSV using Cloud Shell outside EU.", "diverted_path": "VPC Service Controls and Org Policy deny Cloud Shell egress.", "blast_radius": "Zero data leaked.", "recovery": "Mandate access to sensitive data exclusively via sovereign virtual desktops in Europe."}
        ]
    )

    # 038: Security Operations & Threat Detection
    specs[38] = make_spec(
        38, "5.5", "Security Operations & Threat Detection",
        "Visualizes Cloud Security Operations (SecOps): Security Command Center (SCC) Premium, Event Threat Detection, Chronicle SIEM, and automated SOAR incident response playbooks.",
        "Modern cloud security operations must replace manual triage with real-time streaming threat detection and automated SOAR orchestration to neutralize adversaries within seconds.",
        [
            {"id": "g-telemetry-sink", "label": "Cloud Telemetry & Audit Logs", "type": "project", "scope": "global", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-scc-chronicle", "label": "SCC & Chronicle SIEM Detection Engine", "type": "organization", "scope": "organization", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-soar-auto", "label": "Chronicle SOAR & Automated Containment", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "audit-stream", "label": "Cloud Audit Logs Stream", "product": "Admin Activity & Data Access Logs", "group": "g-telemetry-sink", "plane": "control", "x": 140, "y": 140, "detail": "Captures all API calls across Google Cloud projects in real time."},
            {"id": "vpc-flow", "label": "VPC Flow Logs & DNS Logs", "product": "Network Packet Metadata", "group": "g-telemetry-sink", "plane": "data", "x": 140, "y": 280, "detail": "Streams netflow records to detect anomalous outbound connections."},
            {"id": "scc-etd", "label": "SCC Event Threat Detection", "product": "Cryptomining & Brute-Force Detection", "group": "g-scc-chronicle", "plane": "control", "x": 440, "y": 140, "detail": "Uses Google threat intelligence to detect malware, coin miners, and privilege escalations."},
            {"id": "chronicle-rules", "label": "Chronicle YARA-L Rules", "product": "Petabyte-Scale SIEM Analytics", "group": "g-scc-chronicle", "plane": "control", "x": 440, "y": 280, "detail": "Correlates multi-stage attack patterns across cloud and on-premise infrastructure."},
            {"id": "soar-playbook", "label": "SOAR Quarantine Playbook", "product": "Automated Network Isolation", "group": "g-soar-auto", "plane": "control", "x": 780, "y": 200, "detail": "Applies quarantine network tag to compromised VM, severing internet access in 4 seconds."}
        ],
        [
            {"id": "e1", "from": "audit-stream", "to": "scc-etd", "label": "1. Stream Cloud Audit Telemetry", "plane": "control"},
            {"id": "e2", "from": "vpc-flow", "to": "chronicle-rules", "label": "2. Stream VPC Netflow Logs", "plane": "data"},
            {"id": "e3", "from": "scc-etd", "to": "soar-playbook", "label": "3. Alert: High Severity Finding", "plane": "control"},
            {"id": "e4", "from": "chronicle-rules", "to": "soar-playbook", "label": "4. Trigger Threat Containment", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Continuous Telemetry Analysis", "edges": ["e1", "e2"], "action": "SCC and Chronicle ingest audit and flow logs, matching indicators of compromise (IoCs).", "why_traversal": "Provides unified visibility across identity and network attack vectors.", "protocol": "Streaming Log Ingestion", "plane": "Control Plane"},
            {"n": 2, "title": "Automated Incident Containment", "edges": ["e3", "e4"], "action": "SOAR playbook executes instantly, isolating the infected instance and preserving memory dumps.", "why_traversal": "Neutralizes active breaches before attackers can move laterally.", "protocol": "SOAR Automation Playbook", "plane": "Control Plane"}
        ],
        [
            {"id": "quarantine-bypass-failure", "label": "Quarantine Tag Missing Firewall Rule", "changes": {"failedNodes": ["soar-playbook"], "failedEdges": ["e3"]}, "root_cause": "VPC lacked firewall deny rule targeted to the 'quarantine' network tag.", "diverted_path": "VM was tagged, but traffic continued egressing to command-and-control server.", "blast_radius": "Data exfiltration continued for 30 minutes.", "recovery": "Pre-provision high-priority (priority 1) deny-all ingress/egress firewall rules for quarantine tags."}
        ],
        # D2
        "Traces Automated Cryptomining Malware Containment: from suspicious outbound Stratum protocol connection detection to VM snapshot and forensic network isolation.",
        "Automated forensic response preserves volatile memory and disk state for security analysts before severing network connectivity, ensuring evidence is preserved for prosecution.",
        [
            {"id": "g-infected-vm", "label": "Compromised Compute Instance", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-detection-pipeline", "label": "Threat Detection & Alert Pipeline", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-contain-forensics", "label": "Forensic Containment Actions", "type": "project", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "miner-process", "label": "Cryptomining Process", "product": "XMRig Miner (CPU 100%)", "group": "g-infected-vm", "plane": "data", "x": 140, "y": 140, "detail": "Malware spawned via unpatched web vulnerability; connects to mining pool."},
            {"id": "mining-pool-ip", "label": "Mining Pool Outbound Connection", "product": "Stratum Protocol (Port 3333)", "group": "g-infected-vm", "plane": "data", "x": 140, "y": 280, "detail": "Sends proof-of-work hashes to malicious mining pool IP."},
            {"id": "scc-detector", "label": "SCC Finding: CRYPTOMINING", "product": "Finding Severity: HIGH", "group": "g-detection-pipeline", "plane": "control", "x": 440, "y": 200, "detail": "Identifies known mining pool IP address from Google Threat Intelligence database."},
            {"id": "forensic-disk-snap", "label": "Forensic Disk Snapshot", "product": "gcloud compute disks snapshot", "group": "g-contain-forensics", "plane": "control", "x": 780, "y": 140, "detail": "Creates point-in-time forensic image of infected disk for evidence analysis."},
            {"id": "quarantine-firewall", "label": "Apply Quarantine Tag", "product": "Network Isolation (Priority 0)", "group": "g-contain-forensics", "plane": "control", "x": 780, "y": 280, "detail": "Applies network tag 'quarantine'; drops 100% of ingress and egress traffic."}
        ],
        [
            {"id": "e1", "from": "miner-process", "to": "mining-pool-ip", "label": "1. Outbound Hash Submission", "plane": "data"},
            {"id": "e2", "from": "mining-pool-ip", "to": "scc-detector", "label": "2. Flow Log Flagged by SCC", "plane": "control"},
            {"id": "e3", "from": "scc-detector", "to": "forensic-disk-snap", "label": "3. Capture Forensic Snapshot", "plane": "control"},
            {"id": "e4", "from": "scc-detector", "to": "quarantine-firewall", "label": "4. Sever Outbound Connectivity", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Threat Identification", "edges": ["e1", "e2"], "action": "VPC flow log records connection to mining pool; SCC Event Threat Detection triggers finding.", "why_traversal": "Detects cryptomining within seconds without needing agent software inside the VM.", "protocol": "Netflow Anomaly Matching", "plane": "Control Plane"},
            {"n": 2, "title": "Forensic Capture & Isolation", "edges": ["e3", "e4"], "action": "Automated pipeline snapshots disk for digital forensics and drops all traffic.", "why_traversal": "Preserves forensic evidence while eliminating compute cost and risk of lateral spread.", "protocol": "Compute Engine Admin API", "plane": "Control Plane"}
        ],
        [
            {"id": "snapshot-timeout", "label": "Disk Snapshot Timeout During High I/O", "changes": {"failedNodes": ["forensic-disk-snap"], "failedEdges": ["e3"]}, "root_cause": "Disk saturated by mining malware I/O; snapshot request queued for 120 seconds.", "diverted_path": "Isolation delayed while waiting for snapshot.", "blast_radius": "Additional 2 minutes of unauthorized network egress.", "recovery": "Execute network quarantine tag application concurrently before initiating disk snapshot."}
        ],
        # D3
        "Simulates Credential Theft & Lateral Movement Detection: illustrates anomalous IAM Service Account token generation from unauthorized IP and automated credential revocation.",
        "Anomalous API call correlation flags stolen credentials being used outside corporate IP boundaries, instantly revoking active sessions.",
        [
            {"id": "g-attacker-origin", "label": "Adversary External Infrastructure", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-iam-defense", "label": "Cloud IAM Threat Defense & Revocation", "type": "organization", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "stolen-token-call", "label": "Stolen OAuth2 Access Token", "product": "IP: 198.51.100.44 (Tor Exit)", "group": "g-attacker-origin", "plane": "control", "x": 220, "y": 140, "detail": "Attacker uses exfiltrated access token from unauthorized geographic location."},
            {"id": "unusual-api-burst", "label": "compute.instances.list Burst", "product": "Reconnaissance API Scan", "group": "g-attacker-origin", "plane": "control", "x": 220, "y": 280, "detail": "Attacker scripts massive inventory scan across 50 production projects."},
            {"id": "anomaly-engine", "label": "Cloud Audit Anomaly Detector", "product": "Finding: ANOMALOUS_IAM_GRANT", "group": "g-iam-defense", "plane": "control", "x": 700, "y": 140, "detail": "Detects impossible travel velocity and Tor exit node source IP."},
            {"id": "session-revoker", "label": "Revoke All Active IAM Sessions", "product": "gcloud iam service-accounts disable", "group": "g-iam-defense", "plane": "control", "x": 700, "y": 280, "detail": "Disables service account and revokes all active OAuth2 bearer tokens in 2.1 seconds."}
        ],
        [
            {"id": "e1", "from": "stolen-token-call", "to": "unusual-api-burst", "label": "1. Replay Stolen Token for Recon", "plane": "control"},
            {"id": "e2", "from": "unusual-api-burst", "to": "anomaly-engine", "label": "2. Flag Tor IP & Anomalous Volume", "plane": "control"},
            {"id": "e3", "from": "anomaly-engine", "to": "session-revoker", "label": "3. Revoke Identity & Kill Sessions", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Impossible Travel Detection", "edges": ["e1", "e2"], "action": "Anomaly detector correlates API call origin; token issued in New York used from Tor node 2 minutes later.", "why_traversal": "Detects token theft even when the token itself is technically valid.", "protocol": "Cloud Audit Log Analysis", "plane": "Control Plane"},
            {"n": 2, "title": "Immediate Credential Revocation", "edges": ["e3"], "action": "Automated workflow disables compromised service account and forces session termination.", "why_traversal": "Stops reconnaissance in its tracks before data exfiltration can commence.", "protocol": "IAM Admin API", "plane": "Control Plane"}
        ],
        [
            {"id": "broad-revocation-blast", "label": "Service Account Disabling Shuts Down Core Services", "changes": {"failedNodes": ["session-revoker"], "failedEdges": ["e3"]}, "root_cause": "The compromised credential was a shared core production service account.", "diverted_path": "Revoking account crashed 40 healthy production backend instances.", "blast_radius": "Production service downtime.", "recovery": "Enforce per-workload service accounts so revocation of one credential never impacts unrelated systems."}
        ]
    )

    # 039: Application & Supply-Chain Security (SLSA)
    specs[39] = make_spec(
        39, "5.5b", "Application & Supply-Chain Security (SLSA)",
        "Visualizes SLSA Level 3 Secure Software Supply Chain: hermetic Cloud Build pipelines, Artifact Analysis vulnerability scanning, cryptographic in-toto provenance attestations, and GKE Binary Authorization admission gates.",
        "Software supply chain security mandates cryptographic verification at every step: no container image may execute in production unless it was built by an approved CI pipeline and certified free of critical CVEs.",
        [
            {"id": "g-build-tier", "label": "Hermetic Build & Provenance (SLSA L3)", "type": "project", "scope": "global", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-artifact-vault", "label": "Artifact Registry & Attestation Vault", "type": "project", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-gke-gate", "label": "Production GKE Admission Gate", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "cloud-build-hermetic", "label": "Cloud Build (Isolated Worker)", "product": "SLSA Level 3 Hermetic Build", "group": "g-build-tier", "plane": "control", "x": 140, "y": 140, "detail": "Builds container in isolated environment without unvetted internet dependencies."},
            {"id": "kms-provenance-signer", "label": "KMS Attestation Signer", "product": "Cloud KMS Asymmetric Key", "group": "g-build-tier", "plane": "control", "x": 140, "y": 280, "detail": "Digitally signs in-toto build provenance attestation with enterprise private key."},
            {"id": "artifact-vuln-scan", "label": "Artifact Analysis Vulnerability Scan", "product": "Continuous CVE Scanner", "group": "g-artifact-vault", "plane": "control", "x": 440, "y": 140, "detail": "Scans image layers for OS and language package vulnerabilities against CVE databases."},
            {"id": "attestation-authority", "label": "Binary Authorization Attestor", "product": "Quality & Security Sign-Off", "group": "g-artifact-vault", "plane": "control", "x": 440, "y": 280, "detail": "Verifies zero Critical/High CVEs exist before writing verified security attestation."},
            {"id": "binauth-webhook", "label": "Binary Authorization Gatekeeper", "product": "GKE Admission Controller", "group": "g-gke-gate", "plane": "control", "x": 780, "y": 200, "detail": "Intercepts pod creation requests; verifies cryptographically signed attestations before pod starts."}
        ],
        [
            {"id": "e1", "from": "cloud-build-hermetic", "to": "kms-provenance-signer", "label": "1. Generate Provenance Metadata", "plane": "control"},
            {"id": "e2", "from": "cloud-build-hermetic", "to": "artifact-vuln-scan", "label": "2. Push Container to Registry", "plane": "data"},
            {"id": "e3", "from": "artifact-vuln-scan", "to": "attestation-authority", "label": "3. Scan Results Clean (0 CVEs)", "plane": "control"},
            {"id": "e4", "from": "kms-provenance-signer", "to": "binauth-webhook", "label": "4. Verify Provenance Signature", "plane": "control"},
            {"id": "e5", "from": "attestation-authority", "to": "binauth-webhook", "label": "5. Verify Security Attestation", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Hermetic Build & Signing", "edges": ["e1", "e2"], "action": "Cloud Build compiles container in private worker pool and signs provenance with KMS.", "why_traversal": "Guarantees container artifact originates from exact immutable Git commit.", "protocol": "in-toto Provenance Spec", "plane": "Control Plane"},
            {"n": 2, "title": "Vulnerability Audit & Attestation", "edges": ["e3"], "action": "Artifact Analysis scans all packages; attestor attaches signed security certificate.", "why_traversal": "Validates software quality before image is authorized for deployment.", "protocol": "Grafeas / Kritis Protocol", "plane": "Control Plane"},
            {"n": 3, "title": "GKE Admission Enforcement", "edges": ["e4", "e5"], "action": "Binary Authorization admission webhook verifies both attestations and admits pod.", "why_traversal": "Guarantees unauthorized or modified images cannot execute in production.", "protocol": "Kubernetes Admission Webhook", "plane": "Control Plane"}
        ],
        [
            {"id": "rogue-image-rejection", "label": "Untrusted Public DockerHub Image Blocked", "changes": {"failedNodes": ["binauth-webhook"], "failedEdges": ["e4", "e5"]}, "root_cause": "Attacker compromised GKE credentials and attempted to deploy unapproved cryptocurrency miner.", "diverted_path": "Binary Authorization blocks deployment: 'Image denied: missing required attestations'.", "blast_radius": "Zero compromise of production cluster.", "recovery": "Rotate compromised Kubernetes service account and audit cluster RBAC bindings."}
        ],
        # D2
        "Traces the End-to-End SLSA L3 Cryptographic Attestation Pipeline: Git commit push -> hermetic build -> automated vulnerability gate -> KMS signing -> GKE pod deployment.",
        "Chaining multiple independent attestations (Build Provenance + Security Vulnerability Sign-off) prevents compromised developers or build steps from unilaterally pushing unverified code.",
        [
            {"id": "g-dev-src", "label": "Source Code Repository (Git)", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-ci-engine", "label": "Automated Security CI Pipeline", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-prod-deploy", "label": "Production Kubernetes Cluster", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "git-pr-merged", "label": "Signed Git Commit", "product": "GPG Signed Commit (SHA: e4b91f)", "group": "g-dev-src", "plane": "control", "x": 140, "y": 140, "detail": "Peer-reviewed commit merged into main branch with mandatory 2-person approval."},
            {"id": "builder-bot", "label": "Cloud Build Worker Pool", "product": "Private Worker Pool (No Internet)", "group": "g-ci-engine", "plane": "control", "x": 440, "y": 100, "detail": "Builds OCI image from pinned dependencies; generates container digest SHA256."},
            {"id": "cve-checker", "label": "CVE Security Validator", "product": "Artifact Analysis Gate", "group": "g-ci-engine", "plane": "control", "x": 440, "y": 200, "detail": "Evaluates container against NIST NVD; confirms 0 Critical or High severity CVEs."},
            {"id": "attestor-service", "label": "KMS Provenance Attestor", "product": "Asymmetric Signer", "group": "g-ci-engine", "plane": "control", "x": 440, "y": 300, "detail": "Signs in-toto payload: 'Built by Cloud Build from commit e4b91f; verified clean'."},
            {"id": "prod-k8s-pod", "label": "Deployed Production Pod", "product": "Running Verified Container", "group": "g-prod-deploy", "plane": "data", "x": 780, "y": 200, "detail": "Pod runs with read-only root filesystem and dropped Linux capabilities."}
        ],
        [
            {"id": "e1", "from": "git-pr-merged", "to": "builder-bot", "label": "1. Webhook Triggers Hermetic Build", "plane": "control"},
            {"id": "e2", "from": "builder-bot", "to": "cve-checker", "label": "2. Scan Built Image Digest", "plane": "control"},
            {"id": "e3", "from": "cve-checker", "to": "attestor-service", "label": "3. Security Gate Passed -> Sign", "plane": "control"},
            {"id": "e4", "from": "attestor-service", "to": "prod-k8s-pod", "label": "4. Verify Attestation & Launch Pod", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Build & Vulnerability Verification", "edges": ["e1", "e2"], "action": "Cloud Build compiles container in private worker pool and runs vulnerability scan.", "why_traversal": "Establishes cryptographic link between source commit and built binary.", "protocol": "GitOps Trigger", "plane": "Control Plane"},
            {"n": 2, "title": "Attestation Signing & Cluster Launch", "edges": ["e3", "e4"], "action": "Attestor signs image with KMS; GKE admission controller verifies signature and launches pod.", "why_traversal": "Prevents any unauthorized artifact modification between build and runtime.", "protocol": "Binary Authorization REST API", "plane": "Data Plane"}
        ],
        [
            {"id": "critical-cve-block", "label": "Critical OpenSSL CVE Halts Pipeline", "changes": {"failedNodes": ["cve-checker"], "failedEdges": ["e3"]}, "root_cause": "Base container image contained unpatched Critical remote code execution vulnerability.", "diverted_path": "CVE checker rejects image; no attestation signed; deployment blocked.", "blast_radius": "Prevents vulnerable container from entering production.", "recovery": "Update Dockerfile to latest base image containing security patch."}
        ],
        # D3
        "Simulates Breakglass Emergency Deployment: illustrates emergency override procedures when immediate production fixes must bypass Binary Authorization gates.",
        "Breakglass procedures allow authorized on-call engineers to deploy emergency hotfixes during major outages, while generating immutable audit logs for post-incident review.",
        [
            {"id": "g-emergency-outage", "label": "High-Severity Production Outage (P1)", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-breakglass-gate", "label": "Binary Authorization Breakglass Engine", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "hotfix-image", "label": "Emergency Hotfix Container", "product": "Built Locally (No CI Attestation)", "group": "g-emergency-outage", "plane": "data", "x": 220, "y": 140, "detail": "Lead engineer crafts urgent 2-line database deadlock fix during $50k/min outage."},
            {"id": "breakglass-annotation", "label": "Breakglass Override Annotation", "product": "image-policy.k8s.io/break-glass: true", "group": "g-emergency-outage", "plane": "control", "x": 220, "y": 280, "detail": "Pod manifest explicitly asserts emergency breakglass permission."},
            {"id": "binauth-evaluator", "label": "BinAuth Admission Controller", "product": "Evaluates Breakglass Permission", "group": "g-breakglass-gate", "plane": "control", "x": 700, "y": 140, "detail": "Permits unsigned container pod creation due to breakglass annotation."},
            {"id": "audit-incident-log", "label": "Security Incident Audit Log", "product": "High-Severity Audit Finding", "group": "g-breakglass-gate", "plane": "control", "x": 700, "y": 280, "detail": "Logs exact engineer identity, timestamp, and container SHA to Cloud Audit Logs."}
        ],
        [
            {"id": "e1", "from": "hotfix-image", "to": "breakglass-annotation", "label": "1. Attach Breakglass Pod Annotation", "plane": "control"},
            {"id": "e2", "from": "breakglass-annotation", "to": "binauth-evaluator", "label": "2. Bypass Attestation Gate", "plane": "control"},
            {"id": "e3", "from": "binauth-evaluator", "to": "audit-incident-log", "label": "3. Emit Irrevocable Audit Finding", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Emergency Breakglass Assertion", "edges": ["e1", "e2"], "action": "Engineer deploys hotfix with breakglass annotation; admission controller admits pod.", "why_traversal": "Provides operational escape hatch to resolve critical business outages.", "protocol": "Kubernetes Pod Specification", "plane": "Control Plane"},
            {"n": 2, "title": "Audit Accountability", "edges": ["e3"], "action": "Cloud Audit Logs records breakglass event; security alerts are triggered for mandatory retrospective.", "why_traversal": "Guarantees emergency overrides cannot be used secretly or maliciously without audit trail.", "protocol": "Cloud Audit Logging", "plane": "Control Plane"}
        ],
        [
            {"id": "unauthorized-breakglass-attempt", "label": "Unauthorized Engineer Denied Breakglass Access", "changes": {"failedNodes": ["binauth-evaluator"], "failedEdges": ["e3"]}, "root_cause": "Developer lacked container.deployments.breakglass IAM permission.", "diverted_path": "Admission controller rejects deployment; pod fails to start.", "blast_radius": "Only vetted emergency response personnel can activate breakglass.", "recovery": "Designated on-call lead engineer with required breakglass role must execute the deployment."}
        ]
    )

    # 040: Cost Optimization & FinOps
    specs[40] = make_spec(
        40, "6.1", "Cost Optimization & FinOps",
        "Visualizes Enterprise FinOps Cloud Financial Management: Billing BigQuery Export, Looker Cost Dashboards, Committed Use Discounts (CUDs), Active Recommender engine, and automated programmatic budget kill-switches.",
        "FinOps aligns cloud spending with business value; organizations must combine rate optimization (CUDs, Spot VMs) with usage optimization (Recommender rightsizing, auto-sleep dev environments).",
        [
            {"id": "g-billing-export", "label": "Billing Account & BigQuery Data Sink", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-finops-analysis", "label": "FinOps Analytics & CUD Allocation", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-cost-controls", "label": "Automated Cost Controls & Guardrails", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "detailed-billing", "label": "Detailed Cost BigQuery Export", "product": "Hourly Resource Billing Data", "group": "g-billing-export", "plane": "control", "x": 140, "y": 140, "detail": "Exports granular resource-level cost, SKU, project ID, and label telemetry."},
            {"id": "budget-alert-pubsub", "label": "Cloud Billing Budget Alerts", "product": "Thresholds: 50%, 80%, 100%", "group": "g-billing-export", "plane": "control", "x": 140, "y": 280, "detail": "Sends automated JSON notifications when actual or forecasted spend breaches caps."},
            {"id": "cuds-manager", "label": "Committed Use Discounts (CUDs)", "product": "3-Year Flexible Spend Commits", "group": "g-finops-analysis", "plane": "control", "x": 440, "y": 140, "detail": "Applies 57% compute discount across baseline VMs across all regions."},
            {"id": "recommender-api", "label": "Active Assist Recommender", "product": "Idle VM & Sizing Suggestions", "group": "g-finops-analysis", "plane": "control", "x": 440, "y": 280, "detail": "Identifies overprovisioned instances and unattended disks; estimates $4,200/mo savings."},
            {"id": "budget-kill-fn", "label": "Programmatic Budget Enforcer", "product": "Cloud Functions Auto-Cap", "group": "g-cost-controls", "plane": "control", "x": 780, "y": 200, "detail": "Disables billing or stops non-production dev instances when budget exceeds 100%."}
        ],
        [
            {"id": "e1", "from": "detailed-billing", "to": "cuds-manager", "label": "1. Analyze Baseline Compute Spend", "plane": "control"},
            {"id": "e2", "from": "detailed-billing", "to": "recommender-api", "label": "2. Scan for Idle/Over-Sized VMs", "plane": "control"},
            {"id": "e3", "from": "budget-alert-pubsub", "to": "budget-kill-fn", "label": "3. Ingest Budget Breach Notification", "plane": "control"},
            {"id": "e4", "from": "budget-kill-fn", "to": "cuds-manager", "label": "4. Verify Savings vs Commits", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Billing Ingestion & Optimization Analysis", "edges": ["e1", "e2"], "action": "BigQuery analyzes billing data; Recommender identifies over-provisioned VMs.", "why_traversal": "Provides granular cost attribution by team, environment, and service.", "protocol": "BigQuery SQL Export", "plane": "Control Plane"},
            {"n": 2, "title": "Automated Budget Action", "edges": ["e3", "e4"], "action": "Billing alert fires Pub/Sub message; Cloud Function shuts down idle dev environments.", "why_traversal": "Enforces strict financial guardrails to prevent surprise cloud bills.", "protocol": "Eventarc / Cloud Functions", "plane": "Control Plane"}
        ],
        [
            {"id": "over-commit-cud-trap", "label": "Over-Committed Resource CUD Trap", "changes": {"failedNodes": ["cuds-manager"], "failedEdges": ["e1"]}, "root_cause": "Purchased 3-year N1 resource-based CUDs right before migrating architecture to N2D/C3.", "diverted_path": "Company pays for unused N1 capacity for 2.5 remaining years.", "blast_radius": "$80,000 in un-offset cloud spend.", "recovery": "Prioritize Flexible Spend-Based CUDs which apply automatically across all VM families and regions."}
        ],
        # D2
        "Traces Automated Programmatic Budget Enforcement Flow: monthly spend threshold breached -> Pub/Sub notification -> Cloud Run execution -> sandbox project billing decoupling.",
        "Programmatic budget enforcement provides an automated safety net for sandbox and development environments, ensuring runaway experiments cannot drain corporate budgets.",
        [
            {"id": "g-spend-source", "label": "Sandbox Development Project", "type": "project", "scope": "regional", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-billing-mon", "label": "Cloud Billing Budget Watchdog", "type": "organization", "scope": "organization", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-enforce-tier", "label": "Automated Enforcement Handler", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "rogue-gpu-job", "label": "Runaway GPU Training Job", "product": "8x A100 GPUs ($24/hour)", "group": "g-spend-source", "plane": "data", "x": 140, "y": 140, "detail": "Intern launched unconstrained ML model training loop over the weekend."},
            {"id": "project-spend", "label": "Current Monthly Spend", "product": "$1,040 / $1,000 Budget Cap", "group": "g-spend-source", "plane": "control", "x": 140, "y": 280, "detail": "Exceeds 100% of allocated monthly sandbox development budget."},
            {"id": "billing-budget-alert", "label": "Budget Alert Triggered", "product": "Pub/Sub Topic: billing-alerts", "group": "g-billing-mon", "plane": "control", "x": 440, "y": 200, "detail": "Emits JSON notification: costAmount: 1040.50, budgetAmount: 1000.00."},
            {"id": "stop-vm-worker", "label": "Cloud Function Cap Worker", "product": "gcloud compute instances stop", "group": "g-enforce-tier", "plane": "control", "x": 780, "y": 140, "detail": "Iterates through sandbox project and cleanly shuts down all running VM instances."},
            {"id": "slack-finops-notify", "label": "Slack FinOps Alert", "product": "Webhook: #finops-alerts", "group": "g-enforce-tier", "plane": "control", "x": 780, "y": 280, "detail": "Notifies developer and engineering manager of budget cap enforcement."}
        ],
        [
            {"id": "e1", "from": "rogue-gpu-job", "to": "project-spend", "label": "1. Accelerate Project Spend", "plane": "data"},
            {"id": "e2", "from": "project-spend", "to": "billing-budget-alert", "label": "2. Exceed 100% Threshold", "plane": "control"},
            {"id": "e3", "from": "billing-budget-alert", "to": "stop-vm-worker", "label": "3. Invoke Remediation Worker", "plane": "control"},
            {"id": "e4", "from": "stop-vm-worker", "to": "slack-finops-notify", "label": "4. Post Confirmation Alert", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Budget Breach Notification", "edges": ["e1", "e2", "e3"], "action": "Cloud Billing publishes event to Pub/Sub within 15 minutes of budget breach.", "why_traversal": "Enables proactive serverless intervention before runaway spend escalates.", "protocol": "Cloud Pub/Sub Event", "plane": "Control Plane"},
            {"n": 2, "title": "Safe Compute Halting", "edges": ["e4"], "action": "Function stops running instances without deleting persistent disks, preserving code and data.", "why_traversal": "Cuts variable compute burn to zero immediately while preventing developer data loss.", "protocol": "Compute Engine REST API", "plane": "Control Plane"}
        ],
        [
            {"id": "billing-unlink-prod-trap", "label": "Unlinking Billing Destroys Project Resources", "changes": {"failedNodes": ["stop-vm-worker"], "failedEdges": ["e4"]}, "root_cause": "Automation unlinked billing from project instead of stopping VMs; triggered Google 30-day resource deletion countdown.", "diverted_path": "Production database threatened with deletion.", "blast_radius": "Critical risk to persistent infrastructure.", "recovery": "Never unlink billing in production; use targeted compute instance stopping for sandbox cost control."}
        ],
        # D3
        "Simulates Orphaned Resource Leak & Automated Reclamation: detects unattached Persistent Disks and unassigned External IPs and reclaims them.",
        "Unattached storage volumes and idle static IP addresses quietly consume thousands of dollars monthly; Active Assist Recommender automatically reclaims wasted spend.",
        [
            {"id": "g-waste-source", "label": "Orphaned Infrastructure Waste", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-reclaim-engine", "label": "Active Assist Automated Reclaimer", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "unattached-ssd", "label": "Unattached 2TB SSD Disk", "product": "Status: READY (0 Attachments)", "group": "g-waste-source", "plane": "data", "x": 220, "y": 140, "detail": "Left behind after test VM was deleted 45 days ago; billing $340/month."},
            {"id": "idle-static-ip", "label": "Unassigned External Static IP", "product": "Billing $0.010/hr Unused Fee", "group": "g-waste-source", "plane": "control", "x": 220, "y": 280, "detail": "Static external IP reserved but not bound to any forwarding rule or VM."},
            {"id": "recommender-scan", "label": "Recommender Idle Resource Scan", "product": "google.compute.disk.IdleResourceRecommender", "group": "g-reclaim-engine", "plane": "control", "x": 700, "y": 140, "detail": "Identifies zero disk read/write IOPS for past 30 days."},
            {"id": "reclaim-handler", "label": "Snapshot & Purge Function", "product": "Create Backup Snapshot & Delete Disk", "group": "g-reclaim-engine", "plane": "control", "x": 700, "y": 280, "detail": "Creates final backup snapshot in Standard GCS and releases unattached SSD and IP."}
        ],
        [
            {"id": "e1", "from": "unattached-ssd", "to": "recommender-scan", "label": "1. Ingest Zero IOPS Metric", "plane": "control"},
            {"id": "e2", "from": "idle-static-ip", "to": "recommender-scan", "label": "2. Flag Unassigned Static IP", "plane": "control"},
            {"id": "e3", "from": "recommender-scan", "to": "reclaim-handler", "label": "3. Execute Automated Reclamation", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Idle Detection", "edges": ["e1", "e2"], "action": "Recommender identifies persistent disks with zero I/O and unattached IPs.", "why_traversal": "Automates detection of invisible cloud financial waste.", "protocol": "Recommender REST API", "plane": "Control Plane"},
            {"n": 2, "title": "Safe Snapshot & Deletion", "edges": ["e3"], "action": "Function creates safety backup snapshot before deleting disk and releases IP.", "why_traversal": "Saves $340/mo per disk while retaining ability to restore data if needed.", "protocol": "Compute Engine Admin API", "plane": "Control Plane"}
        ],
        [
            {"id": "accidental-db-disk-purge", "label": "Reclamation Purges Offline Database Standby", "changes": {"failedNodes": ["reclaim-handler"], "failedEdges": ["e3"]}, "root_cause": "Cold standby database disk was intentionally detached; automation lacked exclusion tag.", "diverted_path": "Standby disk deleted; required restoring from snapshot.", "blast_radius": "Delayed DR test.", "recovery": "Add exclusion tag finops:skip-reclaim on intentional cold standby disks."}
        ]
    )

    # 041: Performance Optimization & Scalability Engineering
    specs[41] = make_spec(
        41, "6.2", "Performance Optimization & Scalability",
        "Visualizes High-Performance Low-Latency Architecture: Google Premium Tier Network routing, HTTP/3 QUIC load balancing, Tau T2D / C3 Compute instances, Memorystore Redis caching, and Cloud Bigtable wide-column storage.",
        "Maximizing performance requires optimizing every millisecond along the request lifecycle: Anycast edge ingestion (Premium Tier), TLS 1.3 0-RTT handshakes, compute caching, and non-blocking sub-millisecond database lookups.",
        [
            {"id": "g-edge-perf", "label": "Global Edge: Premium Tier & QUIC", "type": "external", "scope": "global", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-compute-tier", "label": "Compute Acceleration Tier", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-lowlatency-storage", "label": "Sub-Millisecond Storage Tier", "type": "project", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "premium-net", "label": "Premium Network Tier", "product": "Google Global Fiber Backbone", "group": "g-edge-perf", "plane": "data", "x": 140, "y": 140, "detail": "Routes user packets into closest local Google PoP; traverses private fiber backbone."},
            {"id": "http3-quic", "label": "HTTP/3 & QUIC Transport", "product": "UDP-Based 0-RTT Handshakes", "group": "g-edge-perf", "plane": "data", "x": 140, "y": 280, "detail": "Eliminates head-of-line blocking and establishes encrypted connections in 0 round-trips."},
            {"id": "tau-compute", "label": "Tau T2D / C3 Compute Nodes", "product": "AMD Milan / Intel Sapphire Rapids", "group": "g-compute-tier", "plane": "data", "x": 440, "y": 140, "detail": "High-performance vCPUs delivering 40% higher price-performance for containerized workloads."},
            {"id": "memorystore-cluster", "label": "Memorystore Cluster for Redis", "product": "In-Memory Microsecond Cache", "group": "g-compute-tier", "plane": "data", "x": 440, "y": 280, "detail": "Delivers sub-millisecond read latencies for 1,000,000+ QPS hot key queries."},
            {"id": "bigtable-storage", "label": "Cloud Bigtable SSD Storage", "product": "Sub-10ms Wide-Column NoSQL", "group": "g-lowlatency-storage", "plane": "data", "x": 780, "y": 200, "detail": "Scales linearly with node count, sustaining millions of writes with single-digit millisecond latency."}
        ],
        [
            {"id": "e1", "from": "premium-net", "to": "http3-quic", "label": "1. Ingest via Closest PoP", "plane": "data"},
            {"id": "e2", "from": "http3-quic", "to": "tau-compute", "label": "2. Route Over Private Fiber", "plane": "data"},
            {"id": "e3", "from": "tau-compute", "to": "memorystore-cluster", "label": "3. Query Sub-Millisecond Cache", "plane": "data"},
            {"id": "e4", "from": "tau-compute", "to": "bigtable-storage", "label": "4. Read/Write Linear Bigtable", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Network Ingress Acceleration", "edges": ["e1", "e2"], "action": "Packets enter Google fiber at user's local metro PoP; QUIC terminates handshakes in 0-RTT.", "why_traversal": "Eliminates public internet congestion and reduces latency by up to 50%.", "protocol": "HTTP/3 over UDP", "plane": "Data Plane"},
            {"n": 2, "title": "Tiered Caching & Storage Retrieval", "edges": ["e3", "e4"], "action": "Compute checks Redis cache; cache misses retrieve data from Bigtable in under 8ms.", "why_traversal": "Achieves consistent sub-10ms p99 response times under massive global load.", "protocol": "gRPC / RESP", "plane": "Data Plane"}
        ],
        [
            {"id": "standard-tier-degradation", "label": "Standard Tier Cold-Potato Routing Latency", "changes": {"failedNodes": ["premium-net"], "failedEdges": ["e2"]}, "root_cause": "Traffic switched to Standard Network Tier, routing over congested public ISP hops.", "diverted_path": "Transatlantic latency jumps from 68ms to 240ms with 3% packet loss.", "blast_radius": "User experience degrades worldwide.", "recovery": "Enforce Premium Network Tier on all production External Load Balancers."}
        ],
        # D2
        "Traces Request Acceleration: comparing Premium Tier (cold-potato routing on Google private fiber) against Standard Tier (hot-potato routing over public internet).",
        "Google Premium Tier ingests traffic at the edge PoP closest to the user, traveling over private illuminated fiber with dedicated SLA guarantees.",
        [
            {"id": "g-london-user", "label": "Client Location: London, UK", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-google-backbone", "label": "Google Private Global Backbone (Cold-Potato)", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-dest-us", "label": "Destination: us-central1 (Iowa)", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "london-client", "label": "User Browser (London)", "product": "Requests Dynamic API Endpoint", "group": "g-london-user", "plane": "data", "x": 140, "y": 200, "detail": "User initiates HTTPS request to api.global.service."},
            {"id": "london-pop", "label": "London Google PoP Edge", "product": "Ingress Latency: 1.8ms", "group": "g-google-backbone", "plane": "data", "x": 440, "y": 140, "detail": "Anycast BGP routes packet immediately into Google private network at London PoP."},
            {"id": "transatlantic-fiber", "label": "Transatlantic Subsea Cable", "product": "Dunant / Equiano Private Fiber", "group": "g-google-backbone", "plane": "data", "x": 440, "y": 280, "detail": "Crosses Atlantic Ocean on Google-owned subsea fiber with zero public transit hops."},
            {"id": "backend-iowa", "label": "Compute Backend (Iowa)", "product": "Total RTT: 74ms (Consistent)", "group": "g-dest-us", "plane": "data", "x": 780, "y": 200, "detail": "Processes API request and returns dynamic JSON payload back along private fiber."}
        ],
        [
            {"id": "e1", "from": "london-client", "to": "london-pop", "label": "1. Ingress at London PoP (1.8ms)", "plane": "data"},
            {"id": "e2", "from": "london-pop", "to": "transatlantic-fiber", "label": "2. Route via Google Fiber", "plane": "data"},
            {"id": "e3", "from": "transatlantic-fiber", "to": "backend-iowa", "label": "3. Terminate at us-central1", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Immediate Ingress", "edges": ["e1"], "action": "Packet enters Google network in London within 2 milliseconds of leaving client device.", "why_traversal": "Minimizes exposure to unreliable public ISP transit.", "protocol": "Anycast BGP", "plane": "Data Plane"},
            {"n": 2, "title": "Private Subsea Routing", "edges": ["e2", "e3"], "action": "Traffic travels across private transatlantic cables directly to Iowa datacenter.", "why_traversal": "Guarantees lowest possible latency and near-zero jitter.", "protocol": "Google Private SDN (B4)", "plane": "Data Plane"}
        ],
        [
            {"id": "public-isp-peering-storm", "label": "Public Internet Congestion Spike (Standard Tier)", "changes": {"failedNodes": ["transatlantic-fiber"], "failedEdges": ["e2"]}, "root_cause": "Standard tier routed traffic over public transit during transcontinental fiber cut.", "diverted_path": "Packets routed through 14 intermediate ISP hops with 18% loss.", "blast_radius": "High latency and timeouts for international users.", "recovery": "Migrate workload back to Premium Network Tier."}
        ],
        # D3
        "Simulates Cloud Bigtable Key Hotspotting & Automated Tablet Rebalancing: illustrates detection of monotonically increasing row keys and key visualizer remediation.",
        "Monotonically increasing row keys (like sequential timestamps) cause all write traffic to pile onto a single tablet server; salting or reversing keys distributes load evenly across all nodes.",
        [
            {"id": "g-hotspot-client", "label": "IoT Ingestion Stream (Sequential Keys)", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-bigtable-cluster", "label": "Cloud Bigtable Distributed Tablet Cluster", "type": "project", "scope": "regional", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "iot-stream", "label": "100k IoT Devices", "product": "Row Key: timestamp#device_id", "group": "g-hotspot-client", "plane": "data", "x": 220, "y": 140, "detail": "All 100,000 devices send metrics with current timestamp prefix: 2026-09-24T12:00:01#dev1."},
            {"id": "key-visualizer", "label": "Bigtable Key Visualizer", "product": "Diagnostic Diagnostic Heatmap", "group": "g-hotspot-client", "plane": "control", "x": 220, "y": 280, "detail": "Reveals intense bright red horizontal stripe indicating write hotspotting on single tablet."},
            {"id": "hot-tablet-node", "label": "Tablet Node 1 (CPU 100%)", "product": "Overloaded Single Tablet Server", "group": "g-bigtable-cluster", "plane": "data", "x": 700, "y": 140, "detail": "Receives 100% of write traffic; write latency spikes from 3ms to 4,500ms."},
            {"id": "salted-rebalance", "label": "Salted Hash Key Distribution", "product": "Row Key: hash(device_id)#timestamp", "group": "g-bigtable-cluster", "plane": "data", "x": 700, "y": 280, "detail": "Distributes writes evenly across all 16 tablet nodes; cluster CPU drops to 22%."}
        ],
        [
            {"id": "e1", "from": "iot-stream", "to": "hot-tablet-node", "label": "1. Monotonic Timestamp Writes", "plane": "data"},
            {"id": "e2", "from": "hot-tablet-node", "to": "key-visualizer", "label": "2. Flag Write Saturation Heatmap", "plane": "control"},
            {"id": "e3", "from": "key-visualizer", "to": "salted-rebalance", "label": "3. Apply Hashed Row Key Pattern", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Hotspotting Saturation", "edges": ["e1", "e2"], "action": "Sequential timestamp keys funnel all writes to one tablet; Key Visualizer reveals severe hotspot.", "why_traversal": "Visualizes the most common Bigtable anti-pattern.", "protocol": "Bigtable gRPC Stream", "plane": "Control Plane"},
            {"n": 2, "title": "Key Salting & Even Distribution", "edges": ["e3"], "action": "Application switches row key prefix to hash(device_id); writes scatter across all tablets.", "why_traversal": "Restores single-digit millisecond write performance across millions of QPS.", "protocol": "Row Key Hash Salting", "plane": "Data Plane"}
        ],
        [
            {"id": "unmitigated-hotspot-crash", "label": "Tablet Server Thrashing", "changes": {"failedNodes": ["hot-tablet-node"], "failedEdges": ["e1"]}, "root_cause": "Application persisted sequential keys without salting during sudden IoT telemetry surge.", "diverted_path": "Writes fail with DEADLINE_EXCEEDED; IoT gateway buffers overflow.", "blast_radius": "IoT telemetry data loss.", "recovery": "Pre-split Bigtable tables and salt row keys with murmur3 hash prefixes."}
        ]
    )

    # 042: Infrastructure as Code: Terraform on GCP
    specs[42] = make_spec(
        42, "6.3", "Infrastructure as Code: Terraform & GitOps",
        "Visualizes Enterprise Terraform & GitOps Architecture: GitHub repository, Cloud Build CI/CD, Terraform Cloud / Cloud Foundation Fabric, remote state locking in GCS, and Policy as Code (tfsec/checkov).",
        "Infrastructure as Code must be managed with software engineering rigor: version control, automated static analysis, speculative planning on pull requests, and automated deployment with state locking.",
        [
            {"id": "g-git-repo", "label": "GitOps Version Control (GitHub)", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-ci-runner", "label": "Cloud Build Terraform Runner", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-cloud-state", "label": "Encrypted Remote State & Lock Vault", "type": "project", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "git-pr-code", "label": "Terraform PR (main.tf)", "product": "Feature Branch Infrastructure", "group": "g-git-repo", "plane": "control", "x": 140, "y": 140, "detail": "Proposes new VPC peering and GKE Autopilot cluster configurations."},
            {"id": "tf-sec-scan", "label": "Policy as Code (checkov)", "product": "Static Security Analysis", "group": "g-git-repo", "plane": "control", "x": 140, "y": 280, "detail": "Validates Terraform against CIS GCP Benchmark; fails PR if public IPs are enabled."},
            {"id": "tf-plan-exec", "label": "terraform plan Runner", "product": "Speculative Execution", "group": "g-ci-runner", "plane": "control", "x": 440, "y": 140, "detail": "Computes exact delta: +3 to add, ~1 to change, 0 to destroy; comments on PR."},
            {"id": "tf-apply-exec", "label": "terraform apply (Merged)", "product": "Least-Privilege Deployer SA", "group": "g-ci-runner", "plane": "control", "x": 440, "y": 280, "detail": "Applies validated infrastructure upon PR merge to main branch."},
            {"id": "gcs-state-lock", "label": "GCS Remote State Bucket", "product": "Object Versioning + CMEK", "group": "g-cloud-state", "plane": "control", "x": 780, "y": 200, "detail": "Stores default.tfstate with object versioning and strong consistent locking."}
        ],
        [
            {"id": "e1", "from": "git-pr-code", "to": "tf-sec-scan", "label": "1. Run Security Linter on PR", "plane": "control"},
            {"id": "e2", "from": "tf-sec-scan", "to": "tf-plan-exec", "label": "2. Generate Speculative Plan", "plane": "control"},
            {"id": "e3", "from": "tf-plan-exec", "to": "gcs-state-lock", "label": "3. Read Remote State File", "plane": "control"},
            {"id": "e4", "from": "tf-apply-exec", "to": "gcs-state-lock", "label": "4. Acquire Lock & Write New State", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Speculative Verification", "edges": ["e1", "e2", "e3"], "action": "Pull request triggers static security check and generates speculative plan using GCS state.", "why_traversal": "Provides visual diff to reviewers before any cloud changes are committed.", "protocol": "GitOps CI Automation", "plane": "Control Plane"},
            {"n": 2, "title": "Atomic Apply & State Locking", "edges": ["e4"], "action": "Upon merge, Cloud Build acquires state lock, applies changes, and releases lock.", "why_traversal": "Prevents concurrent execution conflicts and eliminates state corruption.", "protocol": "Terraform GCS Backend", "plane": "Control Plane"}
        ],
        [
            {"id": "stuck-state-lock", "label": "State Lock Contention Halts Pipeline", "changes": {"failedNodes": ["gcs-state-lock"], "failedEdges": ["e4"]}, "root_cause": "A previous runner crashed mid-execution, leaving lock.tflock orphaned in GCS.", "diverted_path": "All subsequent CI runs fail with 'Error acquiring the state lock'.", "blast_radius": "Infrastructure deployments blocked.", "recovery": "Verify runner is terminated and execute 'terraform force-unlock <LOCK_ID>'."}
        ],
        # D2
        "Traces Multi-Environment Terraform Promotion Flow: dev -> staging -> production directory isolation using Cloud Foundation Fabric modules and least-privilege service accounts.",
        "Directory-level environment separation prevents accidental blast-radius leakage between development experiments and mission-critical production systems.",
        [
            {"id": "g-env-dev", "label": "Environments: Development (Isolated)", "type": "project", "scope": "regional", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-env-stage", "label": "Environments: Staging (Pre-Prod)", "type": "project", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-env-prod", "label": "Environments: Production (Governed)", "type": "project", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "dev-tf", "label": "envs/dev/main.tf", "product": "Fast Iteration / Ephemeral", "group": "g-env-dev", "plane": "control", "x": 140, "y": 200, "detail": "Deploys small e2-medium instances; auto-destroys nightly at 8 PM."},
            {"id": "stage-tf", "label": "envs/stage/main.tf", "product": "Production-Parity Staging", "group": "g-env-stage", "plane": "control", "x": 440, "y": 200, "detail": "Deploys full multi-zone cluster mirroring production architecture."},
            {"id": "prod-approval", "label": "Mandatory Peer Approval", "product": "2-Person Rule Sign-off", "group": "g-env-prod", "plane": "control", "x": 780, "y": 140, "detail": "Requires approvals from Lead SRE and Security Officer before applying."},
            {"id": "prod-tf", "label": "envs/prod/main.tf", "product": "Highly-Available Production", "group": "g-env-prod", "plane": "control", "x": 780, "y": 280, "detail": "Provisions regional GKE cluster, Spanner multi-region, and Cloud Armor rules."}
        ],
        [
            {"id": "e1", "from": "dev-tf", "to": "stage-tf", "label": "1. Validate Module in Dev -> Promote", "plane": "control"},
            {"id": "e2", "from": "stage-tf", "to": "prod-approval", "label": "2. Verify Load Tests -> Request Approval", "plane": "control"},
            {"id": "e3", "from": "prod-approval", "to": "prod-tf", "label": "3. Authorized -> Apply Production", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Progressive Environment Promotion", "edges": ["e1", "e2"], "action": "Changes tested in dev, promoted to staging for automated integration testing.", "why_traversal": "Validates infrastructure code under realistic traffic before reaching production.", "protocol": "Git Tag Promotion", "plane": "Control Plane"},
            {"n": 2, "title": "Governed Production Apply", "edges": ["e3"], "action": "Production deployment requires explicit cryptographic sign-off from designated leads.", "why_traversal": "Prevents unauthorized or unreviewed changes from impacting live users.", "protocol": "GitHub Branch Protection", "plane": "Control Plane"}
        ],
        [
            {"id": "untested-prod-merge", "label": "Emergency Direct Production Edit Disallowed", "changes": {"failedNodes": ["prod-approval"], "failedEdges": ["e3"]}, "root_cause": "Engineer tried to bypass staging to apply hotfix directly to production Terraform.", "diverted_path": "Branch protection rule rejects direct push.", "blast_radius": "Production protected from unvalidated drift.", "recovery": "Follow standard hotfix pipeline through staging with expedited review."}
        ],
        # D3
        "Simulates Terraform Drift Detection & Auto-Remediation: detects out-of-band manual console edits and automatically reverts production state.",
        "Configuration drift occurs when engineers make manual emergency changes in the Google Cloud Console; automated drift detection restores git-defined desired state.",
        [
            {"id": "g-manual-tamper", "label": "Out-of-Band Console Modification", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-drift-corrector", "label": "Automated Drift Detection & Healing", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "manual-edit", "label": "Manual Console Modification", "product": "Changed Machine Type: e2-micro -> n2-32", "group": "g-manual-tamper", "plane": "data", "x": 220, "y": 140, "detail": "Developer manually enlarged VM in Cloud Console, introducing $1,800/mo cost increase."},
            {"id": "cai-asset-event", "label": "Cloud Asset Inventory Event", "product": "Resource Update Event", "group": "g-manual-tamper", "plane": "control", "x": 220, "y": 280, "detail": "Captures instant resource mutation event and emits CloudEvent."},
            {"id": "drift-cron-job", "label": "Scheduled Drift Runner", "product": "Cloud Scheduler (Hourly)", "group": "g-drift-corrector", "plane": "control", "x": 700, "y": 140, "detail": "Executes 'terraform plan -detailed-exitcode' to detect discrepancy."},
            {"id": "auto-revert-apply", "label": "terraform apply -auto-approve", "product": "Reverts to Git Desired State", "group": "g-drift-corrector", "plane": "control", "x": 700, "y": 280, "detail": "Reverts VM back to git-defined e2-micro, eliminating configuration drift."}
        ],
        [
            {"id": "e1", "from": "manual-edit", "to": "cai-asset-event", "label": "1. Mutate Live Cloud Resource", "plane": "control"},
            {"id": "e2", "from": "cai-asset-event", "to": "drift-cron-job", "label": "2. Trigger Drift Evaluation", "plane": "control"},
            {"id": "e3", "from": "drift-cron-job", "to": "auto-revert-apply", "label": "3. Revert Live State to Git Spec", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Drift Discovery", "edges": ["e1", "e2"], "action": "Automated runner detects live VM differs from Terraform code in repository.", "why_traversal": "Identifies shadow IT and unauthorized production modifications.", "protocol": "Terraform Plan Diff", "plane": "Control Plane"},
            {"n": 2, "title": "Automated Reconciliation", "edges": ["e3"], "action": "Cloud Build applies Git code, overriding manual change and restoring compliance.", "why_traversal": "Enforces Git as the single source of truth across all cloud infrastructure.", "protocol": "Terraform Revert Apply", "plane": "Control Plane"}
        ],
        [
            {"id": "revert-production-incident", "label": "Auto-Revert Destroys Emergency Hotfix", "changes": {"failedNodes": ["auto-revert-apply"], "failedEdges": ["e3"]}, "root_cause": "The manual edit was a legitimate emergency fix during an active P1 outage.", "diverted_path": "Automated runner reverted the fix, re-breaking the production service.", "blast_radius": "Recurrence of customer outage.", "recovery": "Engineers executing emergency fixes must add an emergency override freeze lock to the CI pipeline."}
        ]
    )

    # 043: CI/CD & Release Engineering: Cloud Deploy
    specs[43] = make_spec(
        43, "6.4", "CI/CD & Release Engineering: Cloud Deploy",
        "Visualizes Enterprise Progressive Delivery: Cloud Build CI, Artifact Registry, Google Cloud Deploy delivery pipelines, Canary releases (10% -> 50% -> 100%), and automated rollback triggers.",
        "Progressive delivery minimizes blast radius; releases must be gradually exposed to real users while automated telemetry monitoring instantly rolls back defective releases before customers notice.",
        [
            {"id": "g-ci-build", "label": "Continuous Integration: Cloud Build", "type": "project", "scope": "global", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-deploy-pipe", "label": "Google Cloud Deploy Delivery Pipeline", "type": "project", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-canary-fleet", "label": "Progressive Canary Rollout (GKE)", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "cloud-build-ci", "label": "Cloud Build Pipeline", "product": "Container Build & Test", "group": "g-ci-build", "plane": "control", "x": 140, "y": 140, "detail": "Compiles Go binaries, executes unit tests, and packages container images."},
            {"id": "artifact-reg", "label": "Artifact Registry", "product": "Container Registry Digest", "group": "g-ci-build", "plane": "data", "x": 140, "y": 280, "detail": "Stores immutable container image tagged with commit SHA and release semver."},
            {"id": "cloud-deploy-ctl", "label": "Cloud Deploy Pipeline", "product": "Delivery Pipeline: web-app", "group": "g-deploy-pipe", "plane": "control", "x": 440, "y": 200, "detail": "Orchestrates multi-target progression (Dev -> Staging -> Prod) with canary phases."},
            {"id": "baseline-v1-pods", "label": "Stable Baseline Pods (v1.0)", "product": "Handling 90% Production Traffic", "group": "g-canary-fleet", "plane": "data", "x": 780, "y": 140, "detail": "Existing proven release running without error."},
            {"id": "canary-v2-pods", "label": "Canary Pods (v1.1)", "product": "Handling 10% Production Traffic", "group": "g-canary-fleet", "plane": "data", "x": 780, "y": 280, "detail": "New release receiving fractional user traffic under real-time telemetry observation."}
        ],
        [
            {"id": "e1", "from": "cloud-build-ci", "to": "artifact-reg", "label": "1. Push Tested OCI Image", "plane": "data"},
            {"id": "e2", "from": "artifact-reg", "to": "cloud-deploy-ctl", "label": "2. Create Cloud Deploy Release", "plane": "control"},
            {"id": "e3", "from": "cloud-deploy-ctl", "to": "baseline-v1-pods", "label": "3. Maintain Baseline Traffic (90%)", "plane": "data"},
            {"id": "e4", "from": "cloud-deploy-ctl", "to": "canary-v2-pods", "label": "4. Route 10% Traffic to Canary", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Build & Delivery Hand-off", "edges": ["e1", "e2"], "action": "Cloud Build creates immutable container; Cloud Deploy initializes canary release.", "why_traversal": "Decouples continuous integration (build/test) from continuous delivery (deployment/release).", "protocol": "Cloud Deploy API", "plane": "Control Plane"},
            {"n": 2, "title": "Canary Traffic Splitting", "edges": ["e3", "e4"], "action": "GKE Gateway API splits ingress traffic: 90% to stable baseline, 10% to canary pods.", "why_traversal": "Limits potential blast radius of defects to only 10% of users.", "protocol": "Gateway API HTTPRoute", "plane": "Data Plane"}
        ],
        [
            {"id": "canary-regression-detect", "label": "Canary Latency Regression Triggers Instant Rollback", "changes": {"failedNodes": ["canary-v2-pods"], "failedEdges": ["e4"]}, "root_cause": "v1.1 contained an unindexed database query causing p99 latency to spike to 2,800ms.", "diverted_path": "Cloud Deploy automated canary health check fails; shifts 100% traffic back to v1.0.", "blast_radius": "Only 10% of users impacted for 45 seconds.", "recovery": "Rollback completes automatically in 12 seconds with zero human intervention."}
        ],
        # D2
        "Traces Canary Progressive Promotion Flow: Phase 1 (10% traffic for 15 min) -> Phase 2 (50% traffic for 30 min) -> Phase 3 (100% full promotion).",
        "Progressive phase advancements require automated metric verification across each stage, guaranteeing system stability before traffic ramps up.",
        [
            {"id": "g-phase-init", "label": "Phase 1: Canary Initiation (10%)", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-phase-ramp", "label": "Phase 2: Traffic Ramp (50%)", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-phase-full", "label": "Phase 3: Complete Rollout (100%)", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "canary-p1", "label": "Canary Stage 1 (10%)", "product": "Duration: 15 Minutes", "group": "g-phase-init", "plane": "data", "x": 140, "y": 200, "detail": "Monitors error rate and p99 latency against baseline."},
            {"id": "slo-verify-p1", "label": "Automated Metric Gate", "product": "Error Rate < 0.05%", "group": "g-phase-ramp", "plane": "control", "x": 440, "y": 140, "detail": "Cloud Monitoring MQL confirms zero SLO regression during Phase 1."},
            {"id": "canary-p2", "label": "Canary Stage 2 (50%)", "product": "Duration: 30 Minutes", "group": "g-phase-ramp", "plane": "data", "x": 440, "y": 280, "detail": "Increases traffic to 50% to test database connection pool under higher concurrency."},
            {"id": "full-rollout-p3", "label": "Full Promotion (100%)", "product": "v1.1 Promoted to Primary", "group": "g-phase-full", "plane": "data", "x": 780, "y": 200, "detail": "Retires v1.0 baseline pods; v1.1 handles 100% of production traffic."}
        ],
        [
            {"id": "e1", "from": "canary-p1", "to": "slo-verify-p1", "label": "1. Evaluate 15-Minute Metrics", "plane": "control"},
            {"id": "e2", "from": "slo-verify-p1", "to": "canary-p2", "label": "2. Metrics Clean -> Ramp to 50%", "plane": "data"},
            {"id": "e3", "from": "canary-p2", "to": "full-rollout-p3", "label": "3. Concurrency Stable -> 100%", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Stage 1 Metric Verification", "edges": ["e1", "e2"], "action": "Cloud Deploy checks Cloud Monitoring metrics; automatically promotes to 50% traffic.", "why_traversal": "Automates release verification without requiring engineers to stare at dashboards.", "protocol": "Cloud Monitoring MQL Gate", "plane": "Control Plane"},
            {"n": 2, "title": "Full Production Cutover", "edges": ["e3"], "action": "After 30 minutes at 50% load, full rollout executes; old pods drained cleanly.", "why_traversal": "Completes zero-downtime progressive deployment with complete confidence.", "protocol": "Kubernetes Rolling Update", "plane": "Data Plane"}
        ],
        [
            {"id": "connection-pool-exhaustion", "label": "Phase 2 Concurrency Exhausts DB Connections", "changes": {"failedNodes": ["canary-p2"], "failedEdges": ["e3"]}, "root_cause": "At 50% traffic, database connection pool hit hard limit of 200 connections.", "diverted_path": "Latency spiked; Cloud Deploy halted Phase 2 and initiated automatic rollback.", "blast_radius": "Full production outage prevented.", "recovery": "Deploy PgBouncer / Cloud SQL Proxy connection pooling before re-attempting rollout."}
        ],
        # D3
        "Simulates Automated Canary Rollback: Cloud Monitoring detects HTTP 500 error spike in canary pods and triggers instant 100% traffic diversion back to baseline.",
        "Automated rollback removes human panic during bad deployments, returning the system to a known good state in seconds.",
        [
            {"id": "g-failing-canary", "label": "Failing Canary Pods (v1.1)", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-stable-fallback", "label": "Stable Baseline Fallback (v1.0)", "type": "project", "scope": "regional", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "canary-500-surge", "label": "Canary HTTP 500 Errors", "product": "Error Rate: 8.2% Spike", "group": "g-failing-canary", "plane": "data", "x": 220, "y": 140, "detail": "Canary microservice throws NullPointerException on real customer shopping carts."},
            {"id": "slo-watchdog-alert", "label": "Cloud Monitoring MQL Alert", "product": "Alert: CANARY_SLO_BREACH", "group": "g-failing-canary", "plane": "control", "x": 220, "y": 280, "detail": "Detects canary error rate > 1% threshold within 15 seconds."},
            {"id": "deploy-rollback-cmd", "label": "Cloud Deploy Auto-Rollback", "product": "gcloud deploy rollouts rollback", "group": "g-stable-fallback", "plane": "control", "x": 700, "y": 140, "detail": "Reverts Gateway API route weights: 100% to v1.0, 0% to canary."},
            {"id": "recovered-stable-pods", "label": "Stable Pods Absorb 100% Traffic", "product": "100% Healthy Traffic Flow", "group": "g-stable-fallback", "plane": "data", "x": 700, "y": 280, "detail": "Error rate drops back to 0.01% immediately; customer impact resolved."}
        ],
        [
            {"id": "e1", "from": "canary-500-surge", "to": "slo-watchdog-alert", "label": "1. Ingest Canary Error Telemetry", "plane": "control"},
            {"id": "e2", "from": "slo-watchdog-alert", "to": "deploy-rollback-cmd", "label": "2. Trigger Automated Rollback", "plane": "control"},
            {"id": "e3", "from": "deploy-rollback-cmd", "to": "recovered-stable-pods", "label": "3. Restore 100% Baseline Routing", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Defect Detection", "edges": ["e1", "e2"], "action": "Watchdog detects 8.2% error rate in canary and signals Cloud Deploy rollback.", "why_traversal": "Catches application regressions before they reach the general user population.", "protocol": "Cloud Monitoring Alert Policy", "plane": "Control Plane"},
            {"n": 2, "title": "Instantaneous Rollback Execution", "edges": ["e3"], "action": "Gateway route weight shifts 100% traffic back to v1.0; defective pods terminated.", "why_traversal": "Restores production reliability in under 15 seconds.", "protocol": "Gateway API Weight Update", "plane": "Data Plane"}
        ],
        [
            {"id": "db-migration-rollback-failure", "label": "Destructive DB Schema Change Prevents Rollback", "changes": {"failedNodes": ["recovered-stable-pods"], "failedEdges": ["e3"]}, "root_cause": "v1.1 executed destructive SQL migration dropping a column required by v1.0.", "diverted_path": "Rollback failed; v1.0 pods crashed because required column was missing.", "blast_radius": "Full production outage requiring manual database restoration.", "recovery": "Enforce expand-and-contract database migration pattern: never drop columns in the same release as code changes."}
        ]
    )

    # 044: Platform Engineering & Golden Paths
    specs[44] = make_spec(
        44, "6.5", "Platform Engineering & Golden Paths",
        "Visualizes Internal Developer Platform (IDP) Architecture: Backstage Developer Portal, Golden Path software templates, Service Catalog, Cloud Workflows orchestration, and self-service Terraform module vending.",
        "Platform engineering treats developer experience as a product; Golden Paths provide self-service templates that embed enterprise security, networking, and observability by default.",
        [
            {"id": "g-dev-portal", "label": "Developer Self-Service Portal (Backstage)", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-platform-orch", "label": "Platform Orchestration & Cloud Workflows", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-vended-env", "label": "Vended Cloud Landing Zone (VPC & GKE)", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "backstage-ui", "label": "Backstage Service Catalog", "product": "Golden Path Template Selector", "group": "g-dev-portal", "plane": "control", "x": 140, "y": 140, "detail": "Developer chooses 'Secure Event-Driven Go Microservice' from catalog."},
            {"id": "params-form", "label": "Service Sizing Form", "product": "Input Parameters & Cost Center", "group": "g-dev-portal", "plane": "control", "x": 140, "y": 280, "detail": "Captures business unit, cost center, QPS expectations, and environment tier."},
            {"id": "workflows-engine", "label": "Cloud Workflows Orchestrator", "product": "Platform Vending Pipeline", "group": "g-platform-orch", "plane": "control", "x": 440, "y": 200, "detail": "Coordinates GCP Project creation, IAM role bindings, and GitHub repository creation."},
            {"id": "vended-project", "label": "New GCP Project (Shared VPC)", "product": "Automated Landing Zone", "group": "g-vended-env", "plane": "control", "x": 780, "y": 140, "detail": "Pre-configured with org policies, Shared VPC attachment, and CMEK encryption keys."},
            {"id": "gke-namespace", "label": "Isolated GKE Namespace", "product": "NetworkPolicy + ResourceQuota", "group": "g-vended-env", "plane": "data", "x": 780, "y": 280, "detail": "Provisioned with pre-wired CI/CD deployment service account and Prometheus monitoring."}
        ],
        [
            {"id": "e1", "from": "backstage-ui", "to": "params-form", "label": "1. Select Golden Path Template", "plane": "control"},
            {"id": "e2", "from": "params-form", "to": "workflows-engine", "label": "2. Submit Sizing & Metadata", "plane": "control"},
            {"id": "e3", "from": "workflows-engine", "to": "vended-project", "label": "3. Provision Governed GCP Project", "plane": "control"},
            {"id": "e4", "from": "workflows-engine", "to": "gke-namespace", "label": "4. Configure GKE Namespace & CI/CD", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Self-Service Intake", "edges": ["e1", "e2"], "action": "Developer submits template form; platform validates metadata and cost center.", "why_traversal": "Eliminates ticket-based delays while maintaining financial accountability.", "protocol": "Backstage REST API", "plane": "Control Plane"},
            {"n": 2, "title": "Automated Platform Vending", "edges": ["e3", "e4"], "action": "Cloud Workflows provisions project, binds IAM roles, and attaches Shared VPC in under 3 minutes.", "why_traversal": "Delivers secure-by-default infrastructure without developer cognitive burden.", "protocol": "Cloud Resource Manager API", "plane": "Control Plane"}
        ],
        [
            {"id": "quota-exhaustion-block", "label": "Project Quota Exhaustion Halts Vending", "changes": {"failedNodes": ["workflows-engine"], "failedEdges": ["e3"]}, "root_cause": "Organization reached folder quota ceiling of 100 projects.", "diverted_path": "Cloud Workflows catches error; dispatches automated quota increase request.", "blast_radius": "Delayed onboarding for new service.", "recovery": "Implement automated quota buffer monitoring alert at 80% project quota utilization."}
        ],
        # D2
        "Traces Golden Path Microservice Vending Flow: template selection -> GitHub repo creation -> CI/CD pipeline instantiation -> GCP infrastructure binding -> first deployment.",
        "Golden Paths provide developers with a fully functional hello-world service with working CI/CD, telemetry, and security policies ready in minutes.",
        [
            {"id": "g-stage-scaffold", "label": "Step 1: Code Repository Scaffolding", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-stage-infra", "label": "Step 2: Cloud Infrastructure Vending", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-stage-deploy", "label": "Step 3: Initial Deployment Verification", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "github-scaffold", "label": "GitHub Repo Scaffolding", "product": "Go Gin Template + Dockerfile", "group": "g-stage-scaffold", "plane": "control", "x": 140, "y": 200, "detail": "Generates repo with pre-configured GitHub Actions, Dependabot, and C4 docs."},
            {"id": "terraform-vendor", "label": "Terraform Cloud Runner", "product": "Provisions Cloud SQL & Pub/Sub", "group": "g-stage-infra", "plane": "control", "x": 440, "y": 200, "detail": "Applies enterprise golden module with automated daily backups and CMEK keys."},
            {"id": "first-deploy-run", "label": "Automated First Deploy", "product": "Cloud Deploy Release v0.1.0", "group": "g-stage-deploy", "plane": "data", "x": 780, "y": 140, "detail": "Deploys working sample endpoint to dev GKE cluster."},
            {"id": "telemetry-verify", "label": "Observability Pre-Wired", "product": "Dashboard & SLO Live", "group": "g-stage-deploy", "plane": "control", "x": 780, "y": 280, "detail": "Cloud Monitoring dashboard and PagerDuty alerts created automatically."}
        ],
        [
            {"id": "e1", "from": "github-scaffold", "to": "terraform-vendor", "label": "1. Initialize Repo & Trigger Infra Build", "plane": "control"},
            {"id": "e2", "from": "terraform-vendor", "to": "first-deploy-run", "label": "2. Infra Ready -> Trigger Initial Deploy", "plane": "control"},
            {"id": "e3", "from": "first-deploy-run", "to": "telemetry-verify", "label": "3. Verify Health & Wire Telemetry", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Automated Repository & Infrastructure Provisioning", "edges": ["e1", "e2"], "action": "Platform scaffolds Git repo and provisions matching Terraform infrastructure.", "why_traversal": "Reduces developer onboarding time from 3 weeks to 3 minutes.", "protocol": "GitHub & Terraform APIs", "plane": "Control Plane"},
            {"n": 2, "title": "Zero-Day Observability", "edges": ["e3"], "action": "Sample service deploys; monitoring dashboard and SLO burn rate alerts go live instantly.", "why_traversal": "Ensures no service enters production without baseline observability.", "protocol": "Cloud Monitoring API", "plane": "Control Plane"}
        ],
        [
            {"id": "broken-template-failure", "label": "Outdated Dockerfile Base Image Fails Build", "changes": {"failedNodes": ["github-scaffold"], "failedEdges": ["e1"]}, "root_cause": "Golden Path template referenced deprecated Go 1.18 base image with CVEs.", "diverted_path": "CI security linter rejects build; developer vending fails.", "blast_radius": "Developer onboarding blocked.", "recovery": "Platform team maintains automated weekly CI test running all Golden Path templates."}
        ],
        # D3
        "Simulates Platform Multi-Tenancy Noisy Neighbor Containment: GKE ResourceQuotas and NetworkPolicies prevent rogue tenant from starving cluster resources.",
        "Platform engineering multi-tenancy requires strict isolation boundaries: ResourceQuotas prevent CPU/memory starvation, and NetworkPolicies enforce zero-trust pod isolation.",
        [
            {"id": "g-rogue-tenant", "label": "Noisy Neighbor Tenant (Namespace A)", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-governed-cluster", "label": "Governed Multi-Tenant Platform Cluster", "type": "project", "scope": "regional", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "memory-leak-pod", "label": "Rogue Memory Leak Pod", "product": "Consuming 64GB RAM (Runaway)", "group": "g-rogue-tenant", "plane": "data", "x": 220, "y": 140, "detail": "Unchecked memory leak attempts to consume entire node cluster RAM."},
            {"id": "port-scan-attempt", "label": "Cross-Tenant Port Scan", "product": "Probing Namespace B (Illegal)", "group": "g-rogue-tenant", "plane": "control", "x": 220, "y": 280, "detail": "Rogue tenant pod attempts to probe internal ports of payment service in Namespace B."},
            {"id": "quota-enforcer", "label": "GKE ResourceQuota Enforcer", "product": "Hard Limit: 16GB RAM / Namespace", "group": "g-governed-cluster", "plane": "control", "x": 700, "y": 140, "detail": "OOM-kills runaway pod; preserves 100% of RAM for other tenants."},
            {"id": "netpol-shield", "label": "Calico / Cilium NetworkPolicy", "product": "Default Deny All Cross-Namespace", "group": "g-governed-cluster", "plane": "control", "x": 700, "y": 280, "detail": "Drops cross-tenant packets; logs security violation to Security Command Center."}
        ],
        [
            {"id": "e1", "from": "memory-leak-pod", "to": "quota-enforcer", "label": "1. Exceed Namespace Memory Quota", "plane": "control"},
            {"id": "e2", "from": "port-scan-attempt", "to": "netpol-shield", "label": "2. Block Cross-Namespace Traffic", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Resource Quota Enforcement", "edges": ["e1"], "action": "Kubernetes kubelet evicts leaking pod when namespace quota ceiling is reached.", "why_traversal": "Protects neighbor tenants from noisy-neighbor starvation.", "protocol": "ResourceQuota OOMKill", "plane": "Control Plane"},
            {"n": 2, "title": "Zero-Trust Network Isolation", "edges": ["e2"], "action": "NetworkPolicy drops unauthorized cross-namespace packets at the Linux eBPF layer.", "why_traversal": "Enforces strict network isolation between enterprise business units on shared clusters.", "protocol": "eBPF Packet Drop", "plane": "Control Plane"}
        ],
        [
            {"id": "missing-netpol-leak", "label": "Default Allow Cross-Namespace Data Leak", "changes": {"failedNodes": ["netpol-shield"], "failedEdges": ["e2"]}, "root_cause": "Platform team omitted default-deny NetworkPolicy in newly vended namespace.", "diverted_path": "Rogue pod successfully read internal metrics from payment namespace.", "blast_radius": "Internal security breach.", "recovery": "Enforce baseline NetworkPolicy injection via Policy Controller admission mutating webhook."}
        ]
    )

    return specs

if __name__ == "__main__":
    specs = build_p5_p6_specs()
    print(f"Generated {len(specs)} specs for Phase 5 & 6: {sorted(list(specs.keys()))}")

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spec_p5_p6.py")
    with open(out_path, "w") as f:
        f.write('"""\n')
        f.write('spec_p5_p6.py - Topics 034 to 044\n')
        f.write('Phase 5: Security & Compliance\n')
        f.write('Phase 6: DevOps, FinOps & Operations\n')
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

    print("Successfully wrote spec_p5_p6.py!")
