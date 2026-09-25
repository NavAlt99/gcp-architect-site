"""
spec_phase0_phase1.py - Topics 001 to 012 (Phase 0: Prerequisites & Phase 1: GCP Foundations)
"""

def get_specs():
    specs = {}

    # Topic 001: Networking Fundamentals (Preserve/Enhance)
    specs[1] = {
        "topic_no": "001",
        "roadmap_id": "0.1",
        "title": "Networking Fundamentals",
        "d1_purpose": "Visualizes foundational Google Cloud network segmentation: how external client requests traverse Anycast edge infrastructure and Andromeda SDN to reach zero-trust RFC 1918 private subnets without exposing backend VMs.",
        "d1_rationale": "Direct internet ingress to private instances is forbidden. Traffic must first resolve via Anycast DNS, terminate at an External HTTP(S) Load Balancer (Google Front End), and be encapsulated over Andromeda SDN before reaching private VMs. Outbound egress is mediated via Cloud NAT.",
        "d1_groups": [
            {"id": "g-internet", "label": "Public Internet & Client Edge", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-gcp-project", "label": "GCP Project: brightloaf-prod", "type": "project", "scope": "project", "x": 300, "y": 30, "width": 620, "height": 360},
            {"id": "g-vpc-subnet", "label": "VPC: production-vpc (Subnet: us-west1 / 10.0.1.0/24)", "type": "vpc", "scope": "regional", "x": 320, "y": 90, "width": 580, "height": 280}
        ],
        "d1_nodes": [
            {"id": "client", "label": "Client Browser", "product": "External Client", "group": "g-internet", "plane": "data", "x": 140, "y": 120, "detail": "User machine initiating DNS queries and TLS connections over IPv4/IPv6."},
            {"id": "dns", "label": "DNS Resolver", "product": "Cloud DNS", "group": "g-internet", "plane": "control", "x": 140, "y": 270, "detail": "Resolves domain brightloaf.com to public load balancer Anycast virtual IP."},
            {"id": "lb", "label": "External HTTP(S) LB", "product": "Cloud Load Balancing", "group": "g-gcp-project", "plane": "data", "x": 420, "y": 150, "detail": "L7 Global proxy with Anycast IP terminating TLS handshakes and routing to backends."},
            {"id": "vm", "label": "App Backend VM", "product": "Compute Engine", "group": "g-vpc-subnet", "plane": "data", "x": 640, "y": 180, "detail": "Private Compute Engine VM in 10.0.1.0/24 subnet (Private IP: 10.0.1.4, no public IP)."},
            {"id": "nat", "label": "Cloud NAT Gateway", "product": "Cloud NAT", "group": "g-vpc-subnet", "plane": "data", "x": 800, "y": 270, "detail": "Regional NAT gateway translating egress packets from RFC 1918 to public IPs."}
        ],
        "d1_edges": [
            {"id": "e1", "from": "client", "to": "dns", "label": "1. DNS Query (A Record)", "plane": "control"},
            {"id": "e2", "from": "client", "to": "lb", "label": "2. HTTPS Ingress (Anycast)", "plane": "data"},
            {"id": "e3", "from": "lb", "to": "vm", "label": "3. Andromeda SDN Encapsulation", "plane": "data"},
            {"id": "e4", "from": "vm", "to": "nat", "label": "4. Private Egress via Route", "plane": "data"}
        ],
        "d1_steps": [
            {"n": 1, "title": "DNS Name Resolution", "edges": ["e1"], "action": "Client machine queries 8.8.8.8 for brightloaf.com A record.", "why_traversal": "Anycast DNS returns the nearest Google Edge Point of Presence virtual IP.", "protocol": "UDP/53 DNS", "plane": "Control Plane"},
            {"n": 2, "title": "Anycast Edge Ingress", "edges": ["e2"], "action": "Browser performs TLS 1.3 handshake with Google Front End proxy.", "why_traversal": "Connection terminates at edge nearest user; payload traverses Google private fiber.", "protocol": "TCP 443 / TLS 1.3", "plane": "Data Plane"},
            {"n": 3, "title": "SDN Internal Routing", "edges": ["e3"], "action": "Andromeda encapsulates request over Geneve tunnel to private VM.", "why_traversal": "Zero-trust network: backends have no public IP and sit in private subnets.", "protocol": "Internal Geneve / Andromeda", "plane": "Data Plane"},
            {"n": 4, "title": "Outbound NAT Egress", "edges": ["e4"], "action": "Backend VM calls external SaaS API through Cloud NAT gateway.", "why_traversal": "Cloud NAT dynamically assigns source ports without exposing inbound attack surface.", "protocol": "TCP / SNAT", "plane": "Data Plane"}
        ],
        "d1_scenarios": [
            {"id": "nat-exhaustion", "label": "SNAT Port Exhaustion", "changes": {"failedNodes": ["nat"], "failedEdges": ["e4"]}, "root_cause": "Private VM opened more than 64 concurrent egress sockets without dynamic port allocation.", "diverted_path": "Outbound SYN packets are dropped by Cloud NAT gateway; external API calls hang.", "blast_radius": "All private VMs sharing the NAT gateway experience outbound connection timeouts.", "recovery": "Enable Dynamic Port Allocation on Cloud NAT; assign secondary external IP addresses."}
        ],
        "d2_purpose": "Traces the packet lifecycle from browser keystroke to HTTP 200 payload delivery across Google Edge Anycast and Andromeda SDN.",
        "d2_rationale": "Rather than routing traffic across standard public internet transit hops with variable latency, Google Anycast pulls the packet into Google's private fiber network at the nearest edge PoP, routing under Andromeda SDN direct to backend containers.",
        "d2_groups": [
            {"id": "g-client", "label": "Client Environment", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 220, "height": 360},
            {"id": "g-edge", "label": "Google Edge Network (Anycast PoP)", "type": "region", "scope": "global", "x": 280, "y": 30, "width": 280, "height": 360},
            {"id": "g-vpc", "label": "Regional VPC Subnet & Andromeda Mesh", "type": "vpc", "scope": "regional", "x": 590, "y": 30, "width": 340, "height": 360}
        ],
        "d2_nodes": [
            {"id": "browser", "label": "Browser (URL bar)", "product": "User Agent", "group": "g-client", "plane": "data", "x": 130, "y": 140, "detail": "User enters https://brightloaf.com/menu; initiates socket connection."},
            {"id": "os-cache", "label": "OS Resolver / Cache", "product": "Host DNS", "group": "g-client", "plane": "control", "x": 130, "y": 280, "detail": "Checks local hosts file and OS resolver cache before sending recursive query."},
            {"id": "edge-pop", "label": "Anycast Edge PoP", "product": "Edge Infrastructure", "group": "g-edge", "plane": "data", "x": 420, "y": 140, "detail": "BGP Anycast routes request to nearest Google Point of Presence worldwide."},
            {"id": "gfe", "label": "Google Front End (GFE)", "product": "Edge Proxy", "group": "g-edge", "plane": "control", "x": 420, "y": 280, "detail": "Terminates TCP/TLS connection; applies DDoS filtering and HTTP/2 multiplexing."},
            {"id": "andromeda", "label": "Andromeda vSwitch", "product": "Software-Defined Network", "group": "g-vpc", "plane": "data", "x": 750, "y": 140, "detail": "Software-defined flow programming directs packet to destination virtual NIC."},
            {"id": "backend-pod", "label": "Backend Container / VM", "product": "Target Workload", "group": "g-vpc", "plane": "data", "x": 750, "y": 280, "detail": "Application daemon receives HTTP request and computes JSON response."}
        ],
        "d2_edges": [
            {"id": "e1", "from": "browser", "to": "os-cache", "label": "1. Resolve Hostname", "plane": "control"},
            {"id": "e2", "from": "browser", "to": "edge-pop", "label": "2. BGP Anycast Routing", "plane": "data"},
            {"id": "e3", "from": "edge-pop", "to": "gfe", "label": "3. TLS Termination", "plane": "control"},
            {"id": "e4", "from": "gfe", "to": "andromeda", "label": "4. Private Fiber Ingress", "plane": "data"},
            {"id": "e5", "from": "andromeda", "to": "backend-pod", "label": "5. vNIC Dispatch", "plane": "data"}
        ],
        "d2_steps": [
            {"n": 1, "title": "Hostname Resolution", "edges": ["e1"], "action": "OS resolver resolves brightloaf.com to Anycast VIP 34.120.45.67.", "why_traversal": "DNS lookup precedes TCP handshake; Anycast VIP directs packet to closest Google PoP.", "protocol": "DNS UDP/53", "plane": "Control Plane"},
            {"n": 2, "title": "BGP Anycast Ingress", "edges": ["e2"], "action": "Browser opens TCP SYN connection to nearest Google Point of Presence.", "why_traversal": "BGP routing pulls packet into Google private fiber in under 15ms.", "protocol": "TCP SYN / TLS 1.3", "plane": "Data Plane"},
            {"n": 3, "title": "Edge TLS Termination", "edges": ["e3"], "action": "Google Front End terminates TLS handshake and performs HTTP/2 multiplexing.", "why_traversal": "Decouples encryption from backend compute; prevents edge SSL exhaustion.", "protocol": "TLS 1.3 / HTTP/2", "plane": "Control Plane"},
            {"n": 4, "title": "Internal Fiber Transit", "edges": ["e4"], "action": "GFE forwards HTTP payload across private Andromeda SDN to destination VPC.", "why_traversal": "Andromeda encapsulates packets with high-throughput hardware NIC offload.", "protocol": "Encapsulated Geneve", "plane": "Data Plane"},
            {"n": 5, "title": "Backend Processing", "edges": ["e5"], "action": "Andromeda delivers packet to backend container vNIC for execution.", "why_traversal": "Application parses payload and generates HTTP 200 response back along reverse path.", "protocol": "HTTP/1.1 or gRPC", "plane": "Data Plane"}
        ],
        "d2_scenarios": [
            {"id": "gfe-overload", "label": "Edge Proxy Throttling", "changes": {"failedNodes": ["gfe"], "failedEdges": ["e4"]}, "root_cause": "Volumetric traffic burst saturates edge proxy HTTP request buffer.", "diverted_path": "GFE returns HTTP 429 Too Many Requests; packet does not traverse to Andromeda.", "blast_radius": "Incoming clients encounter retry delays.", "recovery": "Configure Cloud Armor rate limiting and autoscaling backend capacity."}
        ],
        "d3_purpose": "Demonstrates automated packet failure recovery across SNAT port exhaustion and MTU blackholing, proving how Cloud NAT dynamic port allocation and PMTUD prevent silent connection drops.",
        "d3_rationale": "When a single zone encounters link saturation, Andromeda SDN and Cloud Load Balancing withdraw the degraded route in under 5 seconds, rerouting established TCP flows to healthy standby paths.",
        "d3_groups": [
            {"id": "g-prim", "label": "Primary Traffic Path (Zone A)", "type": "vpc", "scope": "zonal", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-failover", "label": "Resilience & Failover Path (Zone B)", "type": "vpc", "scope": "zonal", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        "d3_nodes": [
            {"id": "vm-a", "label": "Active Backend VM (Zone A)", "product": "Compute Engine", "group": "g-prim", "plane": "data", "x": 220, "y": 140, "detail": "Serving active production traffic in availability zone us-central1-a."},
            {"id": "probe-a", "label": "Health Check Probe", "product": "Cloud Monitoring", "group": "g-prim", "plane": "control", "x": 220, "y": 280, "detail": "Polls HTTP /healthz every 5s; 3 timeouts mark backend unhealthy."},
            {"id": "vm-b", "label": "Standby Backend VM (Zone B)", "product": "Compute Engine", "group": "g-failover", "plane": "data", "x": 700, "y": 140, "detail": "Healthy warm standby instance in independent failure domain us-central1-b."},
            {"id": "andromeda-lb", "label": "Andromeda Flow Router", "product": "Cloud Load Balancing", "group": "g-failover", "plane": "control", "x": 700, "y": 280, "detail": "Dynamically updates routing table to bypass unhealthy instance."}
        ],
        "d3_edges": [
            {"id": "e1", "from": "probe-a", "to": "vm-a", "label": "1. Health Probe HTTP", "plane": "control"},
            {"id": "e2", "from": "probe-a", "to": "andromeda-lb", "label": "2. Signal Unhealthy Status", "plane": "control"},
            {"id": "e3", "from": "andromeda-lb", "to": "vm-b", "label": "3. Reroute Traffic Flow", "plane": "control"},
            {"id": "e4", "from": "vm-a", "to": "vm-b", "label": "4. Drain & Sync State", "plane": "data"}
        ],
        "d3_steps": [
            {"n": 1, "title": "Steady-State Health Probing", "edges": ["e1"], "action": "Cloud Health Check probes VM in Zone A with HTTP GET /healthz.", "why_traversal": "Validates process responsiveness before routing incoming customer traffic.", "protocol": "HTTP/1.1 TCP 8080", "plane": "Control Plane"},
            {"n": 2, "title": "Probe Failure Detection", "edges": ["e2"], "action": "After 3 missed probes, prober notifies Andromeda flow router of VM failure.", "why_traversal": "Automated eviction prevents blackholing customer transactions on crashed instance.", "protocol": "Internal Control RPC", "plane": "Control Plane"},
            {"n": 3, "title": "Dynamic Traffic Failover", "edges": ["e3"], "action": "Andromeda rewires forwarding table to direct new TCP flows to Zone B.", "why_traversal": "Sub-second route convergence preserves client SLAs during zonal outages.", "protocol": "Andromeda Flow Update", "plane": "Control Plane"},
            {"n": 4, "title": "Healthy State Recovery", "edges": ["e4"], "action": "Standby VM in Zone B assumes active traffic load with zero dropped sessions.", "why_traversal": "Workloads distributed across independent failure domains maintain 99.99% availability.", "protocol": "TCP Connection Migration", "plane": "Data Plane"}
        ],
        "d3_scenarios": [
            {"id": "zonal-blackhole", "label": "Zone A Fiber Blackhole", "changes": {"failedNodes": ["vm-a"], "failedEdges": ["e1"]}, "root_cause": "Physical optical fiber failure in Zone A datacenter cuts backend connectivity.", "diverted_path": "Traffic is immediately shifted to Zone B standby nodes; Zone A is quarantined.", "blast_radius": "Only uncommitted in-flight packets in Zone A require client retry.", "recovery": "Automated regional MIG pre-scales Zone B capacity to absorb 100% diverted traffic."}
        ]
    }

    # Topic 005: Software Architecture & Delivery Basics
    specs[5] = {
        "topic_no": "005",
        "roadmap_id": "0.5",
        "title": "Software Architecture & Delivery Basics",
        "d1_purpose": "Establishes modern software delivery architecture: maps the progression from Git trunk-based development through Cloud Build CI to Artifact Registry and Cloud Deploy CD.",
        "d1_rationale": "Direct manual deployments to production are forbidden. Code changes must pass automated testing in Cloud Build, generate cryptographically signed image digests in Artifact Registry, and promote via Cloud Deploy canary gates.",
        "d1_groups": [
            {"id": "g-src", "label": "Source Control & Developer Edge", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-ci", "label": "Google Cloud CI/CD Perimeter (Cloud Build & Deploy)", "type": "project", "scope": "project", "x": 300, "y": 30, "width": 320, "height": 360},
            {"id": "g-runtime", "label": "Target Production Runtime (GKE & Cloud Run)", "type": "vpc", "scope": "regional", "x": 650, "y": 30, "width": 280, "height": 360}
        ],
        "d1_nodes": [
            {"id": "dev-git", "label": "Developer Git Repo", "product": "GitHub / Git", "group": "g-src", "plane": "control", "x": 140, "y": 140, "detail": "Trunk-based branch with signed commits triggering automated webhooks."},
            {"id": "cb-trigger", "label": "Cloud Build Trigger", "product": "Cloud Build", "group": "g-ci", "plane": "control", "x": 450, "y": 120, "detail": "Listens for push events; launches isolated build workers in Google VPC."},
            {"id": "art-reg", "label": "Artifact Registry", "product": "Artifact Registry", "group": "g-ci", "plane": "data", "x": 450, "y": 270, "detail": "Stores immutable, SHA256-verified OCI container images with vulnerability scan."},
            {"id": "cloud-deploy", "label": "Cloud Deploy Pipeline", "product": "Cloud Deploy", "group": "g-ci", "plane": "control", "x": 780, "y": 120, "detail": "Manages declarative release promotion across dev, staging, and production."},
            {"id": "gke-prod", "label": "GKE Production Cluster", "product": "Google Kubernetes Engine", "group": "g-runtime", "plane": "data", "x": 780, "y": 270, "detail": "Runs containerized microservices behind autoscaling pods and load balancers."}
        ],
        "d1_edges": [
            {"id": "e1", "from": "dev-git", "to": "cb-trigger", "label": "1. Git Push Webhook", "plane": "control"},
            {"id": "e2", "from": "cb-trigger", "to": "art-reg", "label": "2. Push OCI Image Digest", "plane": "data"},
            {"id": "e3", "from": "art-reg", "to": "cloud-deploy", "label": "3. Register Release", "plane": "control"},
            {"id": "e4", "from": "cloud-deploy", "to": "gke-prod", "label": "4. Progressive Canary Rollout", "plane": "data"}
        ],
        "d1_steps": [
            {"n": 1, "title": "Commit Trigger", "edges": ["e1"], "action": "Developer merges pull request; webhook notifies Cloud Build.", "why_traversal": "Automates pipeline execution without manual developer credentials.", "protocol": "HTTPS Webhook", "plane": "Control Plane"},
            {"n": 2, "title": "Hermetic Container Build", "edges": ["e2"], "action": "Cloud Build executes hermetic compilation and pushes image to Artifact Registry.", "why_traversal": "Produces immutable digest (sha256:...) ensuring provenance integrity.", "protocol": "Docker Registry v2", "plane": "Data Plane"},
            {"n": 3, "title": "Release Declaration", "edges": ["e3"], "action": "Artifact Registry triggers Cloud Deploy to create release target manifest.", "why_traversal": "Enforces separation of concerns between build phase and release rollout.", "protocol": "Google Cloud API", "plane": "Control Plane"},
            {"n": 4, "title": "Canary Rollout", "edges": ["e4"], "action": "Cloud Deploy orchestrates 10% canary traffic shift onto GKE cluster.", "why_traversal": "Verifies real user latency and error budgets before 100% promotion.", "protocol": "Kubernetes API / Skaffold", "plane": "Data Plane"}
        ],
        "d1_scenarios": [
            {"id": "cve-detected", "label": "Critical Vulnerability Intercept", "changes": {"failedNodes": ["art-reg"], "failedEdges": ["e3"]}, "root_cause": "Automatic vulnerability scanning detects critical CVE-2026-1029 in base image.", "diverted_path": "Artifact Registry blocks release promotion; Binary Authorization signature is withheld.", "blast_radius": "Build is stopped in CI; production workloads remain untouched.", "recovery": "Base image is patched in Git repo; automated pipeline re-runs to clear scan."}
        ],
        "d2_purpose": "Traces an automated release promotion: from git commit webhook trigger through container compilation, Binary Authorization signing, and multi-target canary verification.",
        "d2_rationale": "Immutable artifact digests guarantee that the exact binary tested in staging is deployed to production, preventing configuration drift across deployment environments.",
        "d2_groups": [
            {"id": "g-src", "label": "Source Control (GitHub Enterprise)", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-ci", "label": "Cloud CI Pipeline (Cloud Build)", "type": "project", "scope": "project", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-cd", "label": "Automated CD (Cloud Deploy & GKE)", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        "d2_nodes": [
            {"id": "git-commit", "label": "Signed Git Commit", "product": "Git Trunk", "group": "g-src", "plane": "control", "x": 140, "y": 140, "detail": "Developer commits verified cryptographic signature to main branch."},
            {"id": "cb-worker", "label": "Cloud Build Worker", "product": "Cloud Build", "group": "g-ci", "plane": "data", "x": 440, "y": 140, "detail": "Compiles Go/Node binary inside ephemeral container worker."},
            {"id": "binauth", "label": "Binary Authorization Signer", "product": "Cloud KMS & Attestor", "group": "g-ci", "plane": "control", "x": 440, "y": 280, "detail": "Cryptographically signs image digest with KMS private key after tests pass."},
            {"id": "canary-gate", "label": "Cloud Deploy Canary Gate", "product": "Cloud Deploy", "group": "g-cd", "plane": "control", "x": 780, "y": 140, "detail": "Routes 10% traffic to canary pod and measures error budget for 10 minutes."},
            {"id": "prod-pods", "label": "Production Pod Fleet", "product": "GKE Autopilot", "group": "g-cd", "plane": "data", "x": 780, "y": 280, "detail": "Full 100% production pods receiving stable customer traffic."}
        ],
        "d2_edges": [
            {"id": "e1", "from": "git-commit", "to": "cb-worker", "label": "1. Trigger Webhook", "plane": "control"},
            {"id": "e2", "from": "cb-worker", "to": "binauth", "label": "2. Verify Test Results", "plane": "control"},
            {"id": "e3", "from": "binauth", "to": "canary-gate", "label": "3. Attestation Signature", "plane": "control"},
            {"id": "e4", "from": "canary-gate", "to": "prod-pods", "label": "4. Promote 100% Release", "plane": "data"}
        ],
        "d2_steps": [
            {"n": 1, "title": "Build Invocation", "edges": ["e1"], "action": "Signed commit fires webhook to provision isolated Cloud Build worker.", "why_traversal": "Hermetic worker guarantees reproducible compilation without host pollution.", "protocol": "HTTPS POST", "plane": "Control Plane"},
            {"n": 2, "title": "Security Attestation", "edges": ["e2"], "action": "After automated unit and SAST security tests pass, KMS signs attestation.", "why_traversal": "Binary Authorization requires cryptographic proof of testing before deployment.", "protocol": "Cloud KMS Sign RPC", "plane": "Control Plane"},
            {"n": 3, "title": "Canary Verification", "edges": ["e3"], "action": "Cloud Deploy admits signed image and spins up 10% canary pods.", "why_traversal": "Validates real production traffic without risking full cluster outage.", "protocol": "Kubernetes Admission Webhook", "plane": "Control Plane"},
            {"n": 4, "title": "Full Fleet Promotion", "edges": ["e4"], "action": "Canary health metrics confirm zero errors; Cloud Deploy updates 100% of pods.", "why_traversal": "Rolling update ensures zero downtime and seamless customer session persistence.", "protocol": "Kubernetes RollingUpdate", "plane": "Data Plane"}
        ],
        "d2_scenarios": [
            {"id": "signature-missing", "label": "Missing Security Attestation", "changes": {"failedNodes": ["binauth"], "failedEdges": ["e3"]}, "root_cause": "Unit test failure prevented KMS attestor from signing container image.", "diverted_path": "GKE Admission Controller blocks pod scheduling with HTTP 403 Forbidden.", "blast_radius": "Only current release is halted; active production remains stable.", "recovery": "Fix failing tests, re-run CI pipeline to obtain valid KMS signature."}
        ],
        "d3_purpose": "Simulates a broken production rollout: demonstrates automated canary analysis detecting HTTP 5xx spikes and triggering instant 1-click rollback to the prior stable release.",
        "d3_rationale": "Cloud Deploy monitors real-time deployment health metrics. If canary targets breach error budget thresholds, traffic is instantly reverted without waiting for manual SRE intervention.",
        "d3_groups": [
            {"id": "g-canary", "label": "Canary Verification Target (10% Traffic)", "type": "vpc", "scope": "zonal", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-stable", "label": "Prior Stable Release (90% Traffic)", "type": "vpc", "scope": "zonal", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        "d3_nodes": [
            {"id": "canary-pod", "label": "Canary Pod (v2.1 Buggy)", "product": "GKE Pod", "group": "g-canary", "plane": "data", "x": 220, "y": 140, "detail": "Throws uncaught null pointer exception on 15% of inbound requests."},
            {"id": "slo-monitor", "label": "Cloud Monitoring SLO Alert", "product": "Cloud Monitoring", "group": "g-canary", "plane": "control", "x": 220, "y": 280, "detail": "Detects HTTP 500 error budget burn rate exceeding 14x threshold."},
            {"id": "deploy-controller", "label": "Cloud Deploy Controller", "product": "Cloud Deploy", "group": "g-failover", "plane": "control", "x": 700, "y": 280, "detail": "Executes automated rollback hook; patches Kubernetes target back to v2.0."},
            {"id": "stable-pod", "label": "Stable Pod Fleet (v2.0)", "product": "GKE Pod Fleet", "group": "g-failover", "plane": "data", "x": 700, "y": 140, "detail": "Healthy prior release absorbs 100% of production traffic safely."}
        ],
        "d3_edges": [
            {"id": "e1", "from": "canary-pod", "to": "slo-monitor", "label": "1. Emit HTTP 500 Metrics", "plane": "control"},
            {"id": "e2", "from": "slo-monitor", "to": "deploy-controller", "label": "2. Trigger Rollback Hook", "plane": "control"},
            {"id": "e3", "from": "deploy-controller", "to": "stable-pod", "label": "3. Revert Traffic to v2.0", "plane": "control"},
            {"id": "e4", "from": "canary-pod", "to": "stable-pod", "label": "4. Terminate Buggy Pods", "plane": "data"}
        ],
        "d3_steps": [
            {"n": 1, "title": "Error Budget Burn Detection", "edges": ["e1"], "action": "Canary pod emits 5xx errors; Cloud Monitoring detects severe error budget burn.", "why_traversal": "Automated telemetry flags software defects before full production exposure.", "protocol": "OpenTelemetry gRPC", "plane": "Control Plane"},
            {"n": 2, "title": "Automated Rollback Signal", "edges": ["e2"], "action": "Monitoring fires webhook to Cloud Deploy API requesting rollback.", "why_traversal": "Eliminates human delay during high-severity production degradations.", "protocol": "Pub/Sub / Webhook", "plane": "Control Plane"},
            {"n": 3, "title": "Traffic Reversion", "edges": ["e3"], "action": "Cloud Deploy resets load balancer weights, routing 100% traffic back to v2.0.", "why_traversal": "Instantly restores user experience while defect is investigated.", "protocol": "Cloud Load Balancing API", "plane": "Control Plane"},
            {"n": 4, "title": "Faulty Pod Eviction", "edges": ["e4"], "action": "GKE sends SIGTERM to canary pods, terminating failed release cleanly.", "why_traversal": "Reclaims cluster resources and locks pipeline until patch is committed.", "protocol": "Kubernetes SIGTERM", "plane": "Data Plane"}
        ],
        "d3_scenarios": [
            {"id": "bad-migration", "label": "Database Schema Incompatibility", "changes": {"failedNodes": ["canary-pod"], "failedEdges": ["e1"]}, "root_cause": "v2.1 application code expected columns not yet present in production database.", "diverted_path": "All canary requests fail with SQL syntax exceptions; automated rollback triggers.", "blast_radius": "Confined to 10% canary traffic for under 45 seconds.", "recovery": "Deploy forward-compatible database migrations before releasing new application binaries."}
        ]
    }

    # Topic 006: Cloud Digital Leader & Business Foundations
    specs[6] = {
        "topic_no": "006",
        "roadmap_id": "0.6",
        "title": "Cloud Digital Leader & Business Foundations",
        "d1_purpose": "Maps Google Cloud Adoption Framework (CAF) governance: connects Executive Sponsors, Center of Excellence (CoE), FinOps Cost Centers, and cloud migration workstreams.",
        "d1_rationale": "Cloud transformation requires foundational alignment between People, Process, and Technology. Value streams and budget governance precede multi-workload migration.",
        "d1_groups": [
            {"id": "g-exec", "label": "Executive Leadership & Business Governance", "type": "organization", "scope": "organization", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-coe", "label": "Cloud Center of Excellence (CCoE) & Landing Zone", "type": "project", "scope": "project", "x": 300, "y": 30, "width": 320, "height": 360},
            {"id": "g-streams", "label": "Business Unit Workstreams & Cost Centers", "type": "vpc", "scope": "regional", "x": 650, "y": 30, "width": 280, "height": 360}
        ],
        "d1_nodes": [
            {"id": "exec-board", "label": "Executive Sponsor", "product": "Business Governance", "group": "g-exec", "plane": "control", "x": 140, "y": 140, "detail": "Establishes cloud vision, business value metrics, and CapEx to OpEx funding model."},
            {"id": "finops-mgr", "label": "FinOps Cost Governance", "product": "Cloud Billing & BigQuery", "group": "g-exec", "plane": "control", "x": 140, "y": 280, "detail": "Tracks unit economics, budget allocation, and committed use discounts."},
            {"id": "ccoe-core", "label": "Cloud Center of Excellence", "product": "Architecture Standards", "group": "g-coe", "plane": "control", "x": 450, "y": 140, "detail": "Defines guardrails, Terraform landing zones, and shared VPC blueprints."},
            {"id": "landing-zone", "label": "Enterprise Landing Zone", "product": "Org Hierarchy & VPC", "group": "g-coe", "plane": "data", "x": 450, "y": 280, "detail": "Provisioned baseline infrastructure: Org policies, central logging, and peering."},
            {"id": "bu-workload", "label": "Business Unit Fleet", "product": "Target Applications", "group": "g-streams", "plane": "data", "x": 780, "y": 200, "detail": "Modernized application workloads operating within enterprise compliance perimeters."}
        ],
        "d1_edges": [
            {"id": "e1", "from": "exec-board", "to": "ccoe-core", "label": "1. Mandate & Budget", "plane": "control"},
            {"id": "e2", "from": "finops-mgr", "to": "landing-zone", "label": "2. Attach Billing Account", "plane": "control"},
            {"id": "e3", "from": "ccoe-core", "to": "landing-zone", "label": "3. Deploy Golden Blueprints", "plane": "control"},
            {"id": "e4", "from": "landing-zone", "to": "bu-workload", "label": "4. Onboard Application Squads", "plane": "data"}
        ],
        "d1_steps": [
            {"n": 1, "title": "Strategic Charter", "edges": ["e1"], "action": "Executive sponsors establish CCoE charter and digital transformation roadmap.", "why_traversal": "Executive alignment prevents shadow IT and establishes unified governance.", "protocol": "Enterprise Governance", "plane": "Control Plane"},
            {"n": 2, "title": "FinOps Foundation", "edges": ["e2"], "action": "FinOps team associates centralized billing accounts and budget alerts to projects.", "why_traversal": "Ensures cost visibility and prevents unallocated infrastructure expenditure.", "protocol": "Cloud Billing API", "plane": "Control Plane"},
            {"n": 3, "title": "Landing Zone Provisioning", "edges": ["e3"], "action": "CCoE deploys automated Terraform landing zone with organization security constraints.", "why_traversal": "Provides secure, compliant foundation before migrating production workloads.", "protocol": "Infrastructure as Code", "plane": "Control Plane"},
            {"n": 4, "title": "Squad Onboarding", "edges": ["e4"], "action": "Business unit engineering squads receive pre-configured project environments.", "why_traversal": "Accelerates time-to-market while guaranteeing security compliance.", "protocol": "Resource Manager API", "plane": "Data Plane"}
        ],
        "d1_scenarios": [
            {"id": "shadow-it", "label": "Unsanctioned Cloud Adoption", "changes": {"failedNodes": ["ccoe-core"], "failedEdges": ["e3"]}, "root_cause": "Product team bypassed CCoE landing zone and created unmanaged projects.", "diverted_path": "Unmanaged projects lack central logging and organization policy constraints.", "blast_radius": "Security perimeter vulnerabilities and unmonitored cloud spending.", "recovery": "Enforce organization creation restrictions; migrate unmanaged projects into CCoE hierarchy."}
        ],
        "d2_purpose": "Traces the cloud migration evaluation lifecycle: from initial Total Cost of Ownership (TCO) discovery through Landing Zone setup to iterative application cutover.",
        "d2_rationale": "Workloads are categorized by migration complexity. Low-risk applications migrate first to establish operational confidence and train engineering squads.",
        "d2_groups": [
            {"id": "g-onprem", "label": "On-Premises Datacenter (CapEx)", "type": "onprem", "scope": "onprem", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-eval", "label": "Discovery & TCO Engine (StrataZone)", "type": "project", "scope": "project", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-cloud", "label": "Target Cloud Landing Zone (OpEx)", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        "d2_nodes": [
            {"id": "legacy-vm", "label": "Legacy On-Prem Fleet", "product": "VMware Cluster", "group": "g-onprem", "plane": "data", "x": 140, "y": 140, "detail": "Aging physical server hardware with depreciating capital expenditure."},
            {"id": "strata-tool", "label": "StrataZone Discovery Agent", "product": "Migration Assessment", "group": "g-eval", "plane": "control", "x": 440, "y": 140, "detail": "Scans CPU, RAM, and IOPS utilization to compute right-sized cloud TCO."},
            {"id": "finops-review", "label": "Business Value Approval", "product": "TCO Business Case", "group": "g-eval", "plane": "control", "x": 440, "y": 280, "detail": "Validates 3-year ROI and commits to Google Cloud spend agreement."},
            {"id": "landing-vpc", "label": "Cloud Landing Zone", "product": "Shared VPC & IAM", "group": "g-cloud", "plane": "control", "x": 780, "y": 140, "detail": "Enterprise security perimeter configured with least-privilege IAM."},
            {"id": "migrated-app", "label": "Modernized Cloud Service", "product": "Cloud Run & Cloud SQL", "group": "g-cloud", "plane": "data", "x": 780, "y": 280, "detail": "Elastic autoscaled cloud workload billed per second of actual usage."}
        ],
        "d2_edges": [
            {"id": "e1", "from": "legacy-vm", "to": "strata-tool", "label": "1. Inventory & Metrics", "plane": "control"},
            {"id": "e2", "from": "strata-tool", "to": "finops-review", "label": "2. Generate TCO Report", "plane": "control"},
            {"id": "e3", "from": "finops-review", "to": "landing-vpc", "label": "3. Approve Foundation", "plane": "control"},
            {"id": "e4", "from": "landing-vpc", "to": "migrated-app", "label": "4. Cutover Production Traffic", "plane": "data"}
        ],
        "d2_steps": [
            {"n": 1, "title": "Infrastructure Discovery", "edges": ["e1"], "action": "StrataZone agent inventories datacenter VMs, memory, and network throughput.", "why_traversal": "Accurate telemetry prevents over-provisioning and establishes sizing baseline.", "protocol": "WMI / SSH Probe", "plane": "Control Plane"},
            {"n": 2, "title": "TCO Analysis", "edges": ["e2"], "action": "Financial model maps CapEx hardware refresh cycles to OpEx cloud consumption.", "why_traversal": "Defends architectural decisions with measurable business ROI.", "protocol": "Financial Analysis", "plane": "Control Plane"},
            {"n": 3, "title": "Landing Zone Readiness", "edges": ["e3"], "action": "Enterprise approves cloud business case and provisions enterprise landing zone.", "why_traversal": "Guarantees governance and compliance guardrails are active prior to cutover.", "protocol": "Terraform Automation", "plane": "Control Plane"},
            {"n": 4, "title": "Workload Cutover", "edges": ["e4"], "action": "Workload cuts over to Google Cloud managed services, unlocking elastic auto-scaling.", "why_traversal": "Replaces fixed maintenance overhead with on-demand scaling.", "protocol": "DNS Cutover / BGP", "plane": "Data Plane"}
        ],
        "d2_scenarios": [
            {"id": "over-provision", "label": "Lift-and-Shift Cost Shock", "changes": {"failedNodes": ["strata-tool"], "failedEdges": ["e2"]}, "root_cause": "Migrating on-premises VMs 1:1 without rightsizing over-allocated CPU/RAM.", "diverted_path": "Cloud monthly invoice spikes due to idle compute reservations.", "blast_radius": "FinOps budget ceiling breached within 30 days.", "recovery": "Activate Google Cloud Recommender API; downsize instances based on p95 usage."}
        ],
        "d3_purpose": "Simulates cloud migration budget overrun and timeline slippage: demonstrates automated FinOps anomaly detection and stakeholder governance escalation.",
        "d3_rationale": "Automated cost anomaly detection flags unplanned egress or oversized VMs within 24 hours, triggering architecture reviews before monthly invoices finalize.",
        "d3_groups": [
            {"id": "g-fin", "label": "FinOps Anomaly Detection", "type": "project", "scope": "project", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-action", "label": "Automated Remediations & Rightsizing", "type": "project", "scope": "project", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        "d3_nodes": [
            {"id": "cost-anomaly", "label": "Cost Anomaly Detector", "product": "Cloud Billing API", "group": "g-fin", "plane": "control", "x": 220, "y": 140, "detail": "Monitors hourly spend slope; alerts when egress exceeds $500/day forecast."},
            {"id": "pubsub-alert", "label": "FinOps Pub/Sub Topic", "product": "Cloud Pub/Sub", "group": "g-fin", "plane": "control", "x": 220, "y": 280, "detail": "Dispatches high-priority spend alert to FinOps team and Slack."},
            {"id": "recommender", "label": "Active Assist Recommender", "product": "Google Cloud Recommender", "group": "g-action", "plane": "control", "x": 700, "y": 140, "detail": "Identifies oversized VMs and unattached persistent disks."},
            {"id": "auto-remediate", "label": "Automated Policy Enforcer", "product": "Cloud Functions", "group": "g-action", "plane": "control", "x": 700, "y": 280, "detail": "Automatically scales down idle dev environments outside business hours."}
        ],
        "d3_edges": [
            {"id": "e1", "from": "cost-anomaly", "to": "pubsub-alert", "label": "1. Publish Budget Breach", "plane": "control"},
            {"id": "e2", "from": "pubsub-alert", "to": "recommender", "label": "2. Trigger Rightsizing Analysis", "plane": "control"},
            {"id": "e3", "from": "recommender", "to": "auto-remediate", "label": "3. Execute Rightsizing Script", "plane": "control"},
            {"id": "e4", "from": "cost-anomaly", "to": "auto-remediate", "label": "4. Verify Spend Stabilization", "plane": "control"}
        ],
        "d3_steps": [
            {"n": 1, "title": "Anomaly Identification", "edges": ["e1"], "action": "Cloud Billing detects unexpected cross-region egress spend spike.", "why_traversal": "Early detection prevents multi-thousand-dollar end-of-month surprises.", "protocol": "Billing Alert Hook", "plane": "Control Plane"},
            {"n": 2, "title": "Governance Notification", "edges": ["e2"], "action": "Alert dispatches to FinOps engineers; Recommender API evaluates root cause.", "why_traversal": "Pinpoints exact VM or bucket causing anomalous cloud expenditures.", "protocol": "Cloud Pub/Sub", "plane": "Control Plane"},
            {"n": 3, "title": "Automated Rightsizing", "edges": ["e3"], "action": "Policy automation powers off non-production VMs and removes unattached disks.", "why_traversal": "Immediate programmatic remediation stops financial bleeding.", "protocol": "Cloud Functions / gcloud", "plane": "Control Plane"},
            {"n": 4, "title": "Budget Recovery", "edges": ["e4"], "action": "Daily run-rate returns below threshold; architecture review scheduled.", "why_traversal": "Ensures sustainable cloud operating model aligned with executive financial targets.", "protocol": "BigQuery Billing Analysis", "plane": "Control Plane"}
        ],
        "d3_scenarios": [
            {"id": "egress-leak", "label": "Cross-Region Egress Leak", "changes": {"failedNodes": ["cost-anomaly"], "failedEdges": ["e1"]}, "root_cause": "VM in us-central1 was querying Cloud Storage multi-region bucket in europe-west.", "diverted_path": "Transatlantic egress charges accumulated rapidly.", "blast_radius": "Monthly network budget exceeded in 72 hours.", "recovery": "Reconfigure storage bucket to regional us-central1; enable VPC peering."}
        ]
    }

    return specs
