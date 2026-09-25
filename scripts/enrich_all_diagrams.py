#!/usr/bin/env python3
"""
enrich_all_diagrams.py - Enriches all 180+ interactive diagram JSON specs,
standalone HTML diagram pages, and topic pages across the entire GCP roadmap.

Adds:
- Clear 'purpose' (Architectural Context)
- 'routing_rationale' (Why normal operation traverses this route)
- 4 to 5 elaborate steps (Action, Why This Path, Protocol, Plane, Checks)
- 2 comprehensive failure mode scenarios (Root Cause, Path Divergence, Blast Radius, Durable Prevention)
- Updates standalone diagram HTML files and embedded topic page script tags.
"""

import os
import glob
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIAGRAMS_DIR = os.path.join(BASE_DIR, "diagrams")
PAGES_DIR = os.path.join(BASE_DIR, "pages")

def enrich_spec(spec):
    diag_id = spec.get("id", "")
    title = spec.get("title", "Architecture Interaction")
    kind = spec.get("kind", "map")
    nodes = {n["id"]: n for n in spec.get("nodes", [])}
    edges = spec.get("edges", [])

    # 1. Purpose & Routing Rationale
    if "purpose" not in spec or not spec["purpose"]:
        if kind == "map" or diag_id.endswith("-d1"):
            spec["purpose"] = f"Visualizes {title} boundaries, establishing zero-trust perimeter isolation between public internet clients, managed edge proxies, and private VPC backend tiers."
            spec["routing_rationale"] = "External client traffic cannot directly access internal compute instances or state stores. It must terminate at Google Edge Anycast proxies, undergo IAM identity authentication, and traverse Andromeda SDN before reaching private RFC 1918 subnets."
        elif kind == "flow" or diag_id.endswith("-d2"):
            spec["purpose"] = f"Traces end-to-end transaction execution across client ingress, gateway authorization, worker task processing, state synchronization, and audit emission for {title}."
            spec["routing_rationale"] = "Client interaction is decoupled from backend execution. The edge proxy terminates external connections and balances load across autoscaled workers, while Cloud Logging captures non-repudiable audit records in parallel."
        else: # failure / d3
            spec["purpose"] = f"Demonstrates high-availability fault isolation for {title}: how automated health check probes detect failure and redirect production traffic to standby replicas without manual intervention."
            spec["routing_rationale"] = "High-availability architectures prevent single-point-of-failure outages by distributing workloads across independent failure domains (zones/regions). Health checks poll backends constantly and update the load balancer routing mesh instantaneously."

    # 2. Expand Steps to 4 or 5 elaborate steps if it currently has only 2 steps
    steps = spec.get("steps", [])
    if len(steps) <= 2 and len(edges) >= 2:
        comp_labels = [n.get("label", n["id"]) for n in spec.get("nodes", [])]
        c1 = comp_labels[0] if len(comp_labels) > 0 else "Client Caller"
        c2 = comp_labels[1] if len(comp_labels) > 1 else "Managed Gateway"
        c3 = comp_labels[2] if len(comp_labels) > 2 else "Core Processing Engine"
        c4 = comp_labels[3] if len(comp_labels) > 3 else "State Persistence Tier"
        c5 = comp_labels[4] if len(comp_labels) > 4 else "Cloud Operations / Audit"

        if kind == "map" or diag_id.endswith("-d1"):
            # Construct 4 or 5 hops
            new_steps = [
                {
                    "n": 1,
                    "title": "Ingress Initiation & Perimeter Traversal",
                    "edges": [edges[0]["id"]],
                    "action": f"Client initiates request from {c1} to {c2} over TLS 1.3.",
                    "why_traversal": f"Traffic enters through Google Anycast Edge; TLS cryptographic handshake is terminated close to user, mitigating Layer 3/4 volumetric DDoS attacks before internal routing.",
                    "protocol": "TCP / TLS 1.3 (Port 443)",
                    "plane": "Data Plane",
                    "narration": f"Hop 1: Ingress traffic arrives from {c1} to {c2} across Google Edge network.",
                    "check": {"commands": f"gcloud {c2.lower().replace(' ', '')[:15]} list", "metrics": "loadbalancing.googleapis.com/https/request_count"}
                },
                {
                    "n": 2,
                    "title": "IAM Validation & Workload Dispatch",
                    "edges": [edges[1]["id"]] if len(edges) > 1 else [edges[0]["id"]],
                    "action": f"{c2} evaluates IAM permissions and routes request over Andromeda SDN to {c3}.",
                    "why_traversal": "Zero-Trust policy requires verifying cryptographic caller identity and VPC Service Control perimeters before releasing traffic into private compute subnets.",
                    "protocol": "Internal HTTP/2 or gRPC",
                    "plane": "Data Plane",
                    "narration": f"Hop 2: {c2} validates request credentials and dispatches payload to {c3}.",
                    "check": {"commands": "gcloud logging read 'protoPayload.authenticationInfo.principalEmail:*'", "metrics": "custom.googleapis.com/rpc/latency"}
                }
            ]
            if len(edges) > 2:
                new_steps.append({
                    "n": 3,
                    "title": "State Persistence & Data Sync",
                    "edges": [edges[2]["id"]],
                    "action": f"{c3} executes business logic, processing payload and updating state on {c4}.",
                    "why_traversal": "Separates stateless application compute from stateful persistence; backends communicate over private RFC 1918 peered connections without traversing the public internet.",
                    "protocol": "TCP (RFC 1918 Private Peering)",
                    "plane": "Data Plane",
                    "narration": f"Hop 3: {c3} processes transaction and synchronizes persistent state with {c4}.",
                    "check": {"commands": "gcloud compute instances list", "metrics": "compute.googleapis.com/instance/disk/write_bytes_count"}
                })
            if len(edges) > 3:
                new_steps.append({
                    "n": len(new_steps) + 1,
                    "title": "Telemetry & Observability Ingestion",
                    "edges": [edges[3]["id"]],
                    "action": f"Operational components stream telemetry and immutable audit events to {c5}.",
                    "why_traversal": "Asynchronous logging ensures observability without introducing latency into the client request path.",
                    "protocol": "HTTPS POST / OpenTelemetry gRPC",
                    "plane": "Control Plane",
                    "narration": f"Hop {len(new_steps) + 1}: Operational components stream telemetry and immutable audit events to {c5}.",
                    "check": {"commands": "gcloud logging read 'severity>=INFO' --limit=10", "metrics": "logging.googleapis.com/log_entry_count"}
                })
            else:
                new_steps.append({
                    "n": len(new_steps) + 1,
                    "title": "Response Delivery & Acknowledgment",
                    "edges": [edges[0]["id"]],
                    "action": f"Final response payload is returned from {c2} to {c1} with HTTP 200 OK.",
                    "why_traversal": "Client receives cryptographic confirmation of completed transaction across established low-latency HTTP/2 connection.",
                    "protocol": "HTTP/2 Response (Port 443)",
                    "plane": "Data Plane",
                    "narration": f"Hop {len(new_steps) + 1}: Final response payload returned to {c1} with HTTP 200 OK.",
                    "check": {"commands": "curl -Iv https://service.brightloaf.internal", "metrics": "loadbalancing.googleapis.com/https/response_count"}
                })
            spec["steps"] = new_steps

        elif kind == "flow" or diag_id.endswith("-d2"):
            new_steps = [
                {
                    "n": 1,
                    "title": "Client Connection & Endpoint Ingress",
                    "edges": [edges[0]["id"]],
                    "action": f"Client user or automated workflow initiates API request to {c2}.",
                    "why_traversal": "Client establishes encrypted session with managed gateway; terminates TLS session and validates client token before accessing internal services.",
                    "protocol": "HTTPS / TLS 1.3",
                    "plane": "Data Plane",
                    "narration": f"Hop 1: Ingress request received from {c1} at {c2}.",
                    "check": {"commands": "curl -Iv https://service.brightloaf.internal", "logs": "Ingress request received"}
                },
                {
                    "n": 2,
                    "title": "Policy Verification & Task Dispatch",
                    "edges": [edges[1]["id"]] if len(edges) > 1 else [edges[0]["id"]],
                    "action": f"{c2} validates caller identity, evaluates routing rules, and dispatches workload to {c3}.",
                    "why_traversal": "Internal service mesh routes traffic based on URL path or gRPC method, balancing connections evenly across available healthy worker replicas.",
                    "protocol": "gRPC / HTTP/2 over VPC",
                    "plane": "Data Plane",
                    "narration": f"Hop 2: {c2} validates credentials and routes payload to {c3}.",
                    "check": {"commands": "gcloud logging read 'logName:cloudaudit'", "metrics": "service/latency"}
                }
            ]
            if len(edges) > 2:
                new_steps.append({
                    "n": 3,
                    "title": "State Persistence & Consistency",
                    "edges": [edges[2]["id"]],
                    "action": f"{c3} processes computation and persists changes to {c4}.",
                    "why_traversal": "Guarantees ACID transactions or persistent event ordering before returning success status to caller.",
                    "protocol": "Database Wire Protocol / RFC 1918",
                    "plane": "Data Plane",
                    "narration": f"Hop 3: {c3} commits state to {c4}.",
                    "check": {"commands": "gcloud compute instances list", "metrics": "storage/write_ops_count"}
                })
            new_steps.append({
                "n": len(new_steps) + 1,
                "title": "Audit Logging & Response Delivery",
                "edges": [edges[-1]["id"]],
                "action": f"Gateway emits non-repudiable Cloud Audit Log recording principal identity, method, and response code to {c5 if len(comp_labels)>4 else 'Audit Logger'}.",
                "why_traversal": "Compliance frameworks mandate that all administrative and data-access requests maintain an immutable audit trail.",
                "protocol": "Internal Logging Agent / OpenTelemetry",
                "plane": "Control Plane",
                "narration": f"Hop {len(new_steps) + 1}: Gateway generates structured audit log and returns HTTP 200 OK.",
                "check": {"commands": "gcloud logging read 'logName:cloudaudit.googleapis.com/activity'", "metrics": "logging.googleapis.com/log_entry_count"}
            })
            spec["steps"] = new_steps

        else: # failure / d3
            new_steps = [
                {
                    "n": 1,
                    "title": "Steady-State Health Monitoring",
                    "edges": [edges[0]["id"]],
                    "action": f"Health check probe sends heartbeat polling requests every 5 seconds to {c1}.",
                    "why_traversal": "Continuous active probing verifies that the instance is not merely powered on, but capable of processing application requests and database queries.",
                    "protocol": "HTTP / TCP Port 8080",
                    "plane": "Control Plane",
                    "narration": f"Hop 1: Health check probe continuously validates {c1} response codes.",
                    "check": {"commands": "gcloud compute health-checks describe hc-app-probe", "metrics": "compute.googleapis.com/health_check/probe_count"}
                },
                {
                    "n": 2,
                    "title": "Outage Trigger & Anomaly Detection",
                    "edges": [edges[0]["id"]],
                    "action": f"Failure Trigger: {c1} encounters threshold saturation or crash. Health check records 3 consecutive timeouts.",
                    "why_traversal": "Multi-probe threshold prevents transient network blips from triggering premature, expensive failovers.",
                    "protocol": "Internal Control Signal",
                    "plane": "Control Plane",
                    "narration": f"Hop 2: Failure occurs on {c1}. Probe signals unhealthy threshold breach to Load Balancer.",
                    "check": {"commands": "gcloud compute health-checks list", "metrics": "health/is_healthy = 0"}
                },
                {
                    "n": 3,
                    "title": "Automated Failover & Traffic Eviction",
                    "edges": [edges[1]["id"]] if len(edges) > 1 else [edges[0]["id"]],
                    "action": f"Control plane withdraws {c1} from forwarding table and redirects incoming traffic to standby unit {c3}.",
                    "why_traversal": "Traffic reroutes in under 5 seconds across Google Andromeda SDN without DNS TTL delay or client reconfiguration.",
                    "protocol": "SDN Flow Table Update",
                    "plane": "Control Plane",
                    "narration": f"Hop 3: Load balancer evicts {c1} and reroutes active traffic to {c3}.",
                    "check": {"commands": "gcloud compute backend-services get-health bs-app", "logs": "Instance marked UNHEALTHY; traffic diverted"}
                },
                {
                    "n": 4,
                    "title": "Capacity Recovery & Auto-Healing",
                    "edges": [edges[-1]["id"]],
                    "action": f"Auto-Healing: Managed Instance Group recreates failed instance and synchronizes state with {c3}.",
                    "why_traversal": "MIG auto-healing restores full multi-zone redundancy, returning the cluster to balanced multi-active serving capacity.",
                    "protocol": "Instance Lifecycle Re-creation",
                    "plane": "Data Plane",
                    "narration": f"Hop 4: Auto-healing restores capacity; {c3} serves traffic while new unit initializes.",
                    "check": {"commands": "gcloud compute instances list", "logs": "Auto-healing repair completed"}
                }
            ]
            spec["steps"] = new_steps

    # 3. Enhance Scenarios with root_cause, diverted_path, blast_radius, recovery
    scenarios = spec.get("scenarios", [])
    enhanced_scenarios = []
    for sc in scenarios:
        sc_id = sc.get("id", "scenario")
        label = sc.get("label", "Failure Scenario")
        failed_nodes = sc.get("changes", {}).get("failedNodes", [])
        failed_node_labels = [nodes[nid]["label"] for nid in failed_nodes if nid in nodes]
        target_name = ", ".join(failed_node_labels) if failed_node_labels else "Active Component"

        root_cause = sc.get("root_cause") or sc.get("narration") or f"Hardware fault, regional quota exhaustion, or unhandled exception in {target_name}."
        diverted_path = sc.get("diverted_path") or f"Normal request path is interrupted at {target_name}. Downstream components receive timeout errors or drop packets without acknowledgment, forcing client retries or failover redirection."
        blast_radius = sc.get("blast_radius") or f"All user sessions dependent on {target_name} experience elevated latency, HTTP 5xx errors, or severed connections."
        recovery = sc.get("recovery") or "Deploy multi-region Anycast failover, cross-zone active-standby redundancy, automated health check eviction, and exponential backoff circuit breakers."

        sc["root_cause"] = root_cause
        sc["diverted_path"] = diverted_path
        sc["blast_radius"] = blast_radius
        sc["recovery"] = recovery
        enhanced_scenarios.append(sc)

    # Ensure at least 2 scenarios
    if len(enhanced_scenarios) < 2:
        node_ids = list(nodes.keys())
        victim = node_ids[min(1, len(node_ids)-1)] if node_ids else "n1"
        victim_label = nodes.get(victim, {}).get("label", "Primary Unit")
        enhanced_scenarios.append({
            "id": "transient-network-drop",
            "label": f"{victim_label} Network Degradation",
            "changes": {"failedNodes": [victim]},
            "root_cause": f"Underlying Andromeda vSwitch queue saturation or hypervisor host maintenance causing 40% packet loss on {victim_label}.",
            "diverted_path": f"Incoming TCP streams to {victim_label} experience high retransmission rates and latency spikes up to 4500ms; gateway circuit breaker opens to shed load.",
            "blast_radius": f"Transactions processed by {victim_label} slow down significantly; client applications encounter timeout errors.",
            "recovery": "Configure client-side exponential backoff with full jitter; deploy Regional Managed Instance Groups with auto-healing and minimum 3-zone distribution.",
            "narration": f"Packet loss and connection timeouts detected on {victim_label}. Circuit breaker trips to protect cluster.",
            "check": {"command": f"gcloud compute instances describe {victim} --format='yaml(status)'", "metric": "compute.googleapis.com/instance/network/dropped_packets_count"}
        })

    spec["scenarios"] = enhanced_scenarios
    return spec

def generate_standalone_diagram_html(spec):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{spec['title']} ({spec['id'].upper()})</title>
  <link rel="stylesheet" href="../assets/site.css">
  <link rel="stylesheet" href="../assets/diagram-engine.css">
  <style>
    body {{
      padding: 24px 16px;
      background: var(--bg);
      font-family: var(--font-mono);
    }}
    .standalone-nav {{
      max-width: 960px;
      margin: 0 auto 16px auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
  </style>
</head>
<body>
  <div class="standalone-nav">
    <a href="../pages/topic-{spec['topic_no']}.html" class="btn-de">← Back to Topic Page</a>
    <span style="font-size:12px; font-weight:600; color:var(--accent);">{spec.get('roadmap_id', '')} • {spec['title']}</span>
    <button class="btn-de" onclick="location.reload()">↺ Reload</button>
  </div>
  
  <div style="max-width:960px; margin:0 auto;">
    <div id="standalone-diagram"></div>
  </div>

  <script src="../assets/diagram-engine.js"></script>
  <script>
    const spec = {json.dumps(spec, indent=2)};
    document.addEventListener('DOMContentLoaded', () => {{
      new DiagramEngine('standalone-diagram', spec);
    }});
  </script>
</body>
</html>
"""

def main():
    specs = sorted(glob.glob(os.path.join(DIAGRAMS_DIR, "topic-*-d*.json")))
    print(f"Found {len(specs)} diagram specs to enrich...")

    updated_specs = {}

    for path in specs:
        with open(path, 'r') as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"Error loading {path}: {e}")
                continue

        enriched = enrich_spec(data)
        updated_specs[enriched["id"]] = enriched

        with open(path, 'w') as f:
            json.dump(enriched, f, indent=2)

        # Regenerate standalone HTML
        html_path = path.replace(".json", ".html")
        with open(html_path, 'w') as f:
            f.write(generate_standalone_diagram_html(enriched))

    print(f"Updated {len(updated_specs)} diagram JSON files and standalone HTML files.")

    # Now update all topic pages in pages/
    pages = sorted(glob.glob(os.path.join(PAGES_DIR, "*.html")))
    print(f"Updating embedded JSON specs in {len(pages)} topic pages...")

    for page_path in pages:
        fname = os.path.basename(page_path)
        m = re.match(r"topic-(\d+)\.html", fname)
        if not m:
            continue
        topic_no = m.group(1)

        d1_id = f"topic-{topic_no}-d1"
        d2_id = f"topic-{topic_no}-d2"
        d3_id = f"topic-{topic_no}-d3"

        d1 = updated_specs.get(d1_id)
        d2 = updated_specs.get(d2_id)
        d3 = updated_specs.get(d3_id)

        if not (d1 and d2 and d3):
            continue

        with open(page_path, 'r') as f:
            content = f.read()

        # Update spec-d1-data
        p1 = r'(<script id=\"spec-d1-data\" type=\"application/json\">)(.*?)(</script>)'
        content = re.sub(p1, lambda m: m.group(1) + '\n' + json.dumps(d1, indent=2) + '\n  ' + m.group(3), content, flags=re.DOTALL)

        # Update spec-d2-data
        p2 = r'(<script id=\"spec-d2-data\" type=\"application/json\">)(.*?)(</script>)'
        content = re.sub(p2, lambda m: m.group(1) + '\n' + json.dumps(d2, indent=2) + '\n  ' + m.group(3), content, flags=re.DOTALL)

        # Update spec-d3-data
        p3 = r'(<script id=\"spec-d3-data\" type=\"application/json\">)(.*?)(</script>)'
        content = re.sub(p3, lambda m: m.group(1) + '\n' + json.dumps(d3, indent=2) + '\n  ' + m.group(3), content, flags=re.DOTALL)

        with open(page_path, 'w') as f:
            f.write(content)

    print("Successfully updated all topic pages with enriched diagram specs!")

if __name__ == "__main__":
    main()
