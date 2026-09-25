#!/usr/bin/env python3
"""
batch_generate_full.py - Upgraded factory functions for GCP Architect Interactive Diagrams.
Generates comprehensive 4-to-5 step traversals, architectural context, routing rationales,
and detailed failure mode breakdowns.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_website import build_topic_page

def make_d1_map(topic_no, roadmap_id, title, comp1, comp2, comp3, comp4):
    """
    D1: Scope & Architecture Map
    5-hop detailed lifecycle with security perimeters, data vs control planes,
    and 2 enterprise failure scenarios.
    """
    return {
        "id": f"topic-{topic_no}-d1",
        "title": f"{title} — Scope & Architecture Map",
        "topic_no": topic_no,
        "roadmap_id": roadmap_id,
        "kind": "map",
        "purpose": f"Visualizes {title} boundaries, establishing zero-trust perimeter isolation between public internet clients, managed edge proxies, and private VPC backend tiers.",
        "routing_rationale": "External client traffic cannot directly access internal compute instances or state stores. It must terminate at Google Edge Anycast proxies, undergo IAM identity authentication, and traverse Andromeda SDN before reaching private RFC 1918 subnets.",
        "groups": [
            {"id": "g-ext", "label": "External Client & Edge Ingress", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-core", "label": "GCP Project & Private VPC Perimeter", "type": "project", "scope": "project", "x": 300, "y": 30, "width": 620, "height": 360}
        ],
        "nodes": [
            {"id": "n1", "label": comp1[0], "product": comp1[1], "group": "g-ext", "plane": comp1[2], "x": 150, "y": 140, "detail": comp1[3]},
            {"id": "n2", "label": comp2[0], "product": comp2[1], "group": "g-core", "plane": comp2[2], "x": 450, "y": 140, "detail": comp2[3]},
            {"id": "n3", "label": comp3[0], "product": comp3[1], "group": "g-core", "plane": comp3[2], "x": 750, "y": 140, "detail": comp3[3]},
            {"id": "n4", "label": comp4[0], "product": comp4[1], "group": "g-core", "plane": comp4[2], "x": 750, "y": 280, "detail": comp4[3]},
            {"id": "n5", "label": "Cloud Operations / Audit", "product": "Cloud Logging & Trace", "group": "g-core", "plane": "control", "x": 450, "y": 280, "detail": "Centralized immutable audit trail, latency tracking, and operational metric collection."}
        ],
        "edges": [
            {"id": "e1", "from": "n1", "to": "n2", "label": "1. Ingress Request / Auth", "plane": "data"},
            {"id": "e2", "from": "n2", "to": "n3", "label": "2. Dispatched Workload", "plane": "data"},
            {"id": "e3", "from": "n3", "to": "n4", "label": "3. State Query / Mutation", "plane": "data"},
            {"id": "e4", "from": "n3", "to": "n5", "label": "4. Structured Audit Log", "plane": "control"},
            {"id": "e5", "from": "n2", "to": "n5", "label": "5. Edge Metrics & Traces", "plane": "control"}
        ],
        "steps": [
            {
                "n": 1,
                "title": "Ingress Initiation & Perimeter Traversal",
                "edges": ["e1"],
                "action": f"Client initiates request from {comp1[0]} to {comp2[0]} over TLS 1.3.",
                "why_traversal": f"Traffic enters through Google Anycast Edge; TLS cryptographic handshake is terminated close to user, mitigating Layer 3/4 volumetric DDoS attacks before internal routing.",
                "protocol": "TCP / TLS 1.3 (Port 443)",
                "plane": "Data Plane",
                "narration": f"Step 1: Ingress traffic arrives from {comp1[0]} to {comp2[0]} across Google Edge network.",
                "check": {"commands": f"gcloud {comp2[1].lower().replace(' ', '')} list", "metrics": "loadbalancing.googleapis.com/https/request_count"}
            },
            {
                "n": 2,
                "title": "IAM Validation & Workload Dispatch",
                "edges": ["e2"],
                "action": f"{comp2[0]} evaluates IAM permissions and routes request over Andromeda SDN to {comp3[0]}.",
                "why_traversal": "Zero-Trust policy requires verifying cryptographic caller identity and VPC Service Control perimeters before releasing traffic into private compute subnets.",
                "protocol": "Internal HTTP/2 or gRPC",
                "plane": "Data Plane",
                "narration": f"Step 2: {comp2[0]} validates request credentials and dispatches payload to {comp3[0]}.",
                "check": {"commands": "gcloud logging read 'protoPayload.authenticationInfo.principalEmail:*'", "metrics": "custom.googleapis.com/rpc/latency"}
            },
            {
                "n": 3,
                "title": "State Persistence & Data Sync",
                "edges": ["e3"],
                "action": f"{comp3[0]} executes business logic, processing payload and updating state on {comp4[0]}.",
                "why_traversal": "Separates stateless application compute from stateful persistence; backends communicate over private RFC 1918 peered connections without traversing the public internet.",
                "protocol": "TCP (RFC 1918 Private Peering)",
                "plane": "Data Plane",
                "narration": f"Step 3: {comp3[0]} processes transaction and synchronizes persistent state with {comp4[0]}.",
                "check": {"commands": "gcloud compute instances list", "metrics": "compute.googleapis.com/instance/disk/write_bytes_count"}
            },
            {
                "n": 4,
                "title": "Telemetry & Observability Ingestion",
                "edges": ["e4", "e5"],
                "action": f"Both {comp2[0]} and {comp3[0]} emit structured logs, OpenTelemetry traces, and latency telemetry to Cloud Operations.",
                "why_traversal": "Asynchronous logging ensures observability without introducing latency into the client request path.",
                "protocol": "HTTPS POST / OpenTelemetry gRPC",
                "plane": "Control Plane",
                "narration": f"Step 4: Operational components stream telemetry and immutable audit events to Cloud Logging and Cloud Monitoring.",
                "check": {"commands": "gcloud logging read 'severity>=INFO' --limit=10", "metrics": "logging.googleapis.com/log_entry_count"}
            }
        ],
        "scenarios": [
            {
                "id": "quota-exceeded",
                "label": "Regional Quota Saturation",
                "changes": {"failedNodes": ["n2"], "failedEdges": ["e2"]},
                "root_cause": f"Production traffic spike exceeded regional API rate quota or CPU allocation ceiling on {comp2[0]}.",
                "diverted_path": f"Normal path ({comp1[0]} → {comp2[0]} → {comp3[0]}) is blocked. {comp2[0]} rejects new connections with HTTP 429 Too Many Requests; client must activate exponential backoff.",
                "blast_radius": f"All incoming client requests to {comp2[0]} are throttled, preventing new transaction processing across the entire region.",
                "recovery": "Configure Cloud Monitoring quota alerts at 80% threshold; request automated quota increases via Service Quotas API and distribute traffic across secondary GCP regions.",
                "narration": f"Regional quota saturated on {comp2[0]}. New requests are throttled with HTTP 429.",
                "check": {"command": "gcloud compute project-info describe --format='yaml(quotas)'", "metric": "serviceruntime.googleapis.com/quota/exceeded"}
            },
            {
                "id": "iam-revoked",
                "label": "Service Account Permission Revoked",
                "changes": {"failedNodes": ["n3"], "failedEdges": ["e3"]},
                "root_cause": f"Principal service account lost required IAM binding or custom role was modified, denying access between {comp3[0]} and {comp4[0]}.",
                "diverted_path": f"Requests traverse through {comp2[0]} into {comp3[0]}, but fail at hop 3 with HTTP 403 Forbidden when calling {comp4[0]}; operations are aborted and error logged.",
                "blast_radius": f"Transactions requiring state mutation on {comp4[0]} fail consistently while read-only requests may succeed.",
                "recovery": "Audit IAM policy bindings using Cloud Asset Inventory; re-apply least-privilege Terraform service account roles with automated CI/CD policy linting.",
                "narration": f"IAM permission denied on {comp3[0]} when accessing {comp4[0]}. Requests fail with HTTP 403.",
                "check": {"command": "gcloud projects get-iam-policy $PROJECT_ID", "metric": "iam.googleapis.com/policy/denial_count"}
            }
        ]
    }

def make_d2_flow(topic_no, roadmap_id, title, step1_desc, step2_desc, step3_desc):
    """
    D2: Request & Control Flow
    5-step end-to-end request lifecycle with granular protocol and security checkpoints.
    """
    return {
        "id": f"topic-{topic_no}-d2",
        "title": f"{title} — Request & Control Flow",
        "topic_no": topic_no,
        "roadmap_id": roadmap_id,
        "kind": "flow",
        "purpose": f"Traces end-to-end transaction execution across client ingress, gateway authorization, worker task processing, state synchronization, and audit emission.",
        "routing_rationale": "Client interaction is decoupled from backend execution. The edge proxy terminates external connections and balances load across autoscaled workers, while Cloud Logging captures non-repudiable audit records in parallel.",
        "groups": [
            {"id": "g-edge", "label": "Client & Edge Ingress", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 260, "height": 360},
            {"id": "g-mesh", "label": "Service Mesh & Backends", "type": "vpc", "scope": "regional", "x": 320, "y": 30, "width": 600, "height": 360}
        ],
        "nodes": [
            {"id": "f1", "label": "Client User / CLI", "product": "User Agent", "group": "g-edge", "plane": "data", "x": 150, "y": 140, "detail": "Origin of client interaction or API request."},
            {"id": "f2", "label": "Gateway / Control Plane", "product": "GCP Service", "group": "g-mesh", "plane": "control", "x": 460, "y": 140, "detail": "Validates request authentication, policy constraints, and routing table."},
            {"id": "f3", "label": "Worker Backend Fleet", "product": "Managed Compute", "group": "g-mesh", "plane": "data", "x": 750, "y": 140, "detail": "Executes core application logic and data transformation."},
            {"id": "f4", "label": "Telemetry & Audit Logs", "product": "Cloud Logging", "group": "g-mesh", "plane": "control", "x": 460, "y": 280, "detail": "Captures immutable audit trail and operational metrics."},
            {"id": "f5", "label": "Data Persistence Tier", "product": "Storage & DB", "group": "g-mesh", "plane": "data", "x": 750, "y": 280, "detail": "High-durability storage confirming transactional commits."}
        ],
        "edges": [
            {"id": "ef1", "from": "f1", "to": "f2", "label": "1. Ingress Request", "plane": "data"},
            {"id": "ef2", "from": "f2", "to": "f3", "label": "2. Forward Execution", "plane": "data"},
            {"id": "ef3", "from": "f3", "to": "f5", "label": "3. Commit State", "plane": "data"},
            {"id": "ef4", "from": "f2", "to": "f4", "label": "4. Audit Emission", "plane": "control"}
        ],
        "steps": [
            {
                "n": 1,
                "title": "Client Connection & Endpoint Ingress",
                "edges": ["ef1"],
                "action": f"Client user or automated workflow initiates API request: {step1_desc}.",
                "why_traversal": "Client establishes encrypted session with managed gateway; terminates TLS session and validates client token before accessing internal services.",
                "protocol": "HTTPS / TLS 1.3",
                "plane": "Data Plane",
                "narration": f"Step 1: {step1_desc}",
                "check": {"commands": "curl -Iv https://service.brightloaf.internal", "logs": "Ingress request received"}
            },
            {
                "n": 2,
                "title": "Policy Verification & Task Dispatch",
                "edges": ["ef2"],
                "action": f"Gateway authenticates caller identity, verifies routing rules, and forwards workload: {step2_desc}.",
                "why_traversal": "Internal service mesh routes traffic based on URL path or gRPC method, balancing connections evenly across available healthy worker replicas.",
                "protocol": "gRPC / HTTP/2 over VPC",
                "plane": "Data Plane",
                "narration": f"Step 2: Gateway validates credentials and routes payload to Worker Backend Fleet: {step2_desc}.",
                "check": {"commands": "gcloud logging read 'logName:cloudaudit'", "metrics": "service/latency"}
            },
            {
                "n": 3,
                "title": "State Persistence & Consistency",
                "edges": ["ef3"],
                "action": f"Worker backend fleet processes computation and persists changes to data storage: {step3_desc}.",
                "why_traversal": "Guarantees ACID transactions or persistent event ordering before returning success status to caller.",
                "protocol": "Database Wire Protocol / RFC 1918",
                "plane": "Data Plane",
                "narration": f"Step 3: Worker fleet commits state to persistence tier: {step3_desc}.",
                "check": {"commands": "gcloud compute instances list", "metrics": "storage/write_ops_count"}
            },
            {
                "n": 4,
                "title": "Audit Logging & Observability",
                "edges": ["ef4"],
                "action": "Gateway emits non-repudiable Cloud Audit Log recording principal identity, method, and response code.",
                "why_traversal": "Compliance frameworks (SOC 2, ISO 27001) mandate that all administrative and data-access requests maintain an immutable audit trail.",
                "protocol": "Internal Logging Agent / OpenTelemetry",
                "plane": "Control Plane",
                "narration": "Step 4: Gateway generates structured audit log and forwards to Cloud Logging.",
                "check": {"commands": "gcloud logging read 'logName:cloudaudit.googleapis.com/activity'", "metrics": "logging.googleapis.com/log_entry_count"}
            }
        ],
        "scenarios": [
            {
                "id": "auth-fail",
                "label": "IAM Authentication Revoked",
                "changes": {"failedNodes": ["f2"], "failedEdges": ["ef2"]},
                "root_cause": "Principal service account disabled, expired client certificate, or deleted OAuth token.",
                "diverted_path": "Normal forwarding path (Gateway → Worker Backend) is terminated immediately. Gateway responds to client with HTTP 401 Unauthorized / HTTP 403 Forbidden without reaching backend.",
                "blast_radius": "All API calls authenticated with the affected service account are rejected immediately.",
                "recovery": "Rotate credentials, generate new short-lived OAuth tokens via Cloud IAM Credentials API, and inspect access logs in Cloud Logging.",
                "narration": "Principal service account disabled or key expired. Ingress proxy returns HTTP 403 Forbidden.",
                "check": {"command": "gcloud iam service-accounts describe SA_NAME", "metric": "permission_denied_count > 0"}
            },
            {
                "id": "backend-timeout",
                "label": "Worker Backend Saturation / Timeout",
                "changes": {"failedNodes": ["f3"], "failedEdges": ["ef3"]},
                "root_cause": "Worker fleet memory exhaustion (OOM) or unhandled runtime deadlock preventing request completion within gateway timeout window (30s).",
                "diverted_path": "Gateway attempts connection to Worker Backend; after timeout threshold elapses with no response, gateway returns HTTP 504 Gateway Timeout and trips circuit breaker.",
                "blast_radius": "Requests routed to saturated instances fail; autoscaling group must spin up additional instances to restore throughput.",
                "recovery": "Configure Compute Engine / Cloud Run autoscaler on CPU and concurrency metrics; enable Cloud Trace to pinpoint backend latency bottlenecks.",
                "narration": "Worker fleet saturated. Gateway encounters timeout and returns HTTP 504.",
                "check": {"command": "gcloud logging read 'httpRequest.status>=500'", "metric": "loadbalancing.googleapis.com/https/backend_latencies"}
            }
        ]
    }

def make_d3_failure(topic_no, roadmap_id, title, fail_desc, heal_desc):
    """
    D3: Failure Injection & Auto-Healing
    4-step resilience walkthrough showing active probing, failure detection,
    automated failover routing, and capacity auto-healing.
    """
    return {
        "id": f"topic-{topic_no}-d3",
        "title": f"{title} — Failure Injection & Auto-Healing",
        "topic_no": topic_no,
        "roadmap_id": roadmap_id,
        "kind": "failure",
        "purpose": f"Demonstrates high-availability fault isolation: how automated health check probes detect zonal failure and redirect production traffic to standby replicas without manual intervention.",
        "routing_rationale": "High-availability architectures prevent single-point-of-failure outages by distributing workloads across independent failure domains (zones/regions). Health checks poll backends constantly and update the load balancer routing mesh instantaneously.",
        "groups": [
            {"id": "g-prim", "label": "Primary Active Zone (Zone A)", "type": "vpc", "scope": "zonal", "x": 30, "y": 30, "width": 410, "height": 360},
            {"id": "g-failover", "label": "Standby Recovery Zone (Zone B)", "type": "vpc", "scope": "zonal", "x": 480, "y": 30, "width": 430, "height": 360}
        ],
        "nodes": [
            {"id": "act-node", "label": "Active Service Node", "product": "Primary Unit", "group": "g-prim", "plane": "data", "x": 220, "y": 140, "detail": "Primary serving instance handling active production requests."},
            {"id": "act-hc", "label": "Health Check Probe", "product": "Cloud Monitoring", "group": "g-prim", "plane": "control", "x": 220, "y": 280, "detail": "Polls TCP/HTTP port every 5 seconds; 3 consecutive timeouts declare failure."},
            {"id": "stby-node", "label": "Standby Node (Zone B)", "product": "Failover Unit", "group": "g-failover", "plane": "data", "x": 680, "y": 140, "detail": "Warm standby replica running in separate availability zone."},
            {"id": "alert-mgr", "label": "Cloud Router / Failover", "product": "Load Balancing Mesh", "group": "g-failover", "plane": "control", "x": 680, "y": 280, "detail": "Updates forwarding rule weights to reroute traffic to healthy endpoints."}
        ],
        "edges": [
            {"id": "efl1", "from": "act-hc", "to": "act-node", "label": "1. Health Status Probe", "plane": "control"},
            {"id": "efl2", "from": "act-hc", "to": "alert-mgr", "label": "2. Signal Unhealthy Status", "plane": "control"},
            {"id": "efl3", "from": "alert-mgr", "to": "stby-node", "label": "3. Activate Standby Route", "plane": "control"},
            {"id": "efl4", "from": "act-node", "to": "stby-node", "label": "4. Replicate State & Heal", "plane": "data"}
        ],
        "steps": [
            {
                "n": 1,
                "title": "Steady-State Health Monitoring",
                "edges": ["efl1"],
                "action": "Cloud Health Check probe sends HTTP GET /healthz every 5 seconds to Active Service Node.",
                "why_traversal": "Continuous active probing verifies that the instance is not merely powered on, but capable of processing application requests and database queries.",
                "protocol": "HTTP / TCP Port 8080",
                "plane": "Control Plane",
                "narration": "Step 1: Health check probe continuously validates Active Service Node response codes.",
                "check": {"commands": "gcloud compute health-checks describe hc-app-probe", "metrics": "compute.googleapis.com/health_check/probe_count"}
            },
            {
                "n": 2,
                "title": "Outage Trigger & Anomaly Detection",
                "edges": ["efl2"],
                "action": f"Failure Trigger: {fail_desc}. Health check encounters 3 consecutive timeouts and marks node UNHEALTHY.",
                "why_traversal": "Multi-probe threshold prevents transient network blips from triggering premature, expensive failovers.",
                "protocol": "Internal Control Signal",
                "plane": "Control Plane",
                "narration": f"Step 2: Failure occurs ({fail_desc}). Probe signals unhealthy threshold breach to Load Balancer.",
                "check": {"commands": "gcloud compute health-checks list", "metrics": "health/is_healthy = 0"}
            },
            {
                "n": 3,
                "title": "Automated Failover & Traffic Eviction",
                "edges": ["efl3"],
                "action": "Control plane withdraws unhealthy node from forwarding table and redirects incoming traffic to Standby Node in Zone B.",
                "why_traversal": "Traffic reroutes in under 5 seconds across Google Andromeda SDN without DNS TTL delay or client reconfiguration.",
                "protocol": "SDN Flow Table Update",
                "plane": "Control Plane",
                "narration": "Step 3: Load balancer evicts unhealthy instance and reroutes active traffic to Standby Node in Zone B.",
                "check": {"commands": "gcloud compute backend-services get-health bs-app", "logs": "Instance marked UNHEALTHY; traffic diverted"}
            },
            {
                "n": 4,
                "title": "Capacity Recovery & Auto-Healing",
                "edges": ["efl4"],
                "action": f"Auto-Healing: {heal_desc}. Managed Instance Group recreates failed instance and synchronizes state.",
                "why_traversal": "MIG auto-healing restores full multi-zone redundancy, returning the cluster to balanced multi-active serving capacity.",
                "protocol": "Instance Lifecycle Re-creation",
                "plane": "Data Plane",
                "narration": f"Step 4: Auto-healing restores capacity ({heal_desc}). Standby Node serves traffic while new unit initializes.",
                "check": {"commands": "gcloud compute instances list", "logs": "Auto-healing repair completed"}
            }
        ],
        "scenarios": [
            {
                "id": "split-brain",
                "label": "Cross-Zone Partition / Split-Brain",
                "changes": {"failedNodes": ["act-node", "stby-node"], "failedEdges": ["efl4"]},
                "root_cause": "Network partition severs inter-zone consensus heartbeat between Zone A and Zone B.",
                "diverted_path": "Normal cross-zone state sync is blocked. Distributed consensus quorum (Raft/Paxos) pauses writes to avoid data corruption, returning read-only views until partition heals.",
                "blast_radius": "Write operations blocked across both zones; read traffic served with stale-read warning flag.",
                "recovery": "Rely on Google Cloud Spanner / etcd multi-zone quorum; automated tie-breaker witness in third zone confirms majority before promoting leader.",
                "narration": "Network partition prevents consensus between zones. Quorum halts writes to prevent split-brain.",
                "check": {"command": "gcloud compute networks describe NETWORK_NAME", "metric": "consensus_quorum_lost"}
            },
            {
                "id": "cascade-exhaustion",
                "label": "Cascading Failover Overload",
                "changes": {"failedNodes": ["stby-node"]},
                "root_cause": "Standby Zone B lacks sufficient provisioned capacity to absorb 100% of Zone A's diverted traffic, causing CPU exhaustion.",
                "diverted_path": "Traffic diverts from Zone A to Zone B, but Zone B saturates instantly. Dropped connection rates spike to 100%.",
                "blast_radius": "Entire multi-zone deployment suffers outage despite successful failover mechanics.",
                "recovery": "Enforce minimum N+1 or N+2 capacity provisioning rules; configure regional autoscaling to pre-scale standby zones.",
                "narration": "Standby zone saturates under sudden 100% traffic surge. Requests drop across both zones.",
                "check": {"command": "gcloud compute instance-groups managed describe mig-zone-b", "metric": "compute.googleapis.com/instance_group/size"}
            }
        ]
    }

def make_analogy(topic_no, roadmap_id, title, city_concept, p1, p2, p3, p4):
    return {
        "topic_no": topic_no,
        "roadmap_id": roadmap_id,
        "title": f"Cloud City: {title}",
        "city_concept": city_concept,
        "beats": [
            {"step": 1, "name": "The City Problem", "story": p1, "analogy_elements": ["Unregulated Chaos", "Disorganized Dispatch"]},
            {"step": 2, "name": "The City Solution", "story": p2, "analogy_elements": ["Municipal Charter", "Civic Dispatcher"]},
            {"step": 3, "name": "City Under Stress", "story": p3, "analogy_elements": ["Traffic Gridlock", "Automated Relief Gates"]},
            {"step": 4, "name": "Where Metaphor Breaks", "story": p4, "analogy_elements": ["Physical City vs Software SDN"]}
        ]
    }

print("Upgraded batch generator templates ready.")
