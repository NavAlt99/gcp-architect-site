"""
spec_p2.py - Topics 013 to 021 (Phase 2: Core Services)
Compute, GKE, Serverless, VPC, LB/CDN/Armor, Hybrid, Storage, Databases, Messaging
"""

def get_specs():
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

    # 013: Compute Engine
    specs[13] = make_spec(
        13, "2.1", "Compute Engine: VMs, Disks, and Managed Instance Groups",
        "Maps Compute Engine architecture: details Regional Managed Instance Groups (MIGs), Regional Persistent Disks, and automated health check boundaries.",
        "Compute Engine isolates virtual machines across availability zones. Regional MIGs balance VM counts across zones, while Regional Persistent Disks synchronously replicate data.",
        [
            {"id": "g-ext-lb", "label": "Edge Anycast Ingress (Cloud Load Balancing)", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-mig-core", "label": "Regional MIG Boundary (us-central1)", "type": "region", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-storage-tier", "label": "High-Durability Regional Disk Fabric", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "alb", "label": "Global External ALB", "product": "Cloud Load Balancing", "group": "g-ext-lb", "plane": "data", "x": 140, "y": 140, "detail": "Distributes HTTP traffic across healthy backend VM instances in all zones."},
            {"id": "hc-probe", "label": "Regional Health Check", "product": "Compute Health Check", "group": "g-ext-lb", "plane": "control", "x": 140, "y": 280, "detail": "Probes port 8080 /healthz; informs MIG manager of dead instances."},
            {"id": "mig-mgr", "label": "Regional Instance Group Mgr", "product": "Compute MIG Controller", "group": "g-mig-core", "plane": "control", "x": 440, "y": 140, "detail": "Maintains target capacity; automatically recreates failed instances from template."},
            {"id": "vm-zone-a", "label": "VM Instance (Zone A)", "product": "n2-standard-4 (us-central1-a)", "group": "g-mig-core", "plane": "data", "x": 440, "y": 280, "detail": "Primary serving instance processing application workloads."},
            {"id": "reg-pd", "label": "Regional Persistent Disk", "product": "pd-ssd (Synchronous 2-Zone)", "group": "g-storage-tier", "plane": "data", "x": 780, "y": 200, "detail": "Synchronously replicates block storage writes across Zone A and Zone B."}
        ],
        [
            {"id": "e1", "from": "alb", "to": "vm-zone-a", "label": "1. Forward HTTP Traffic", "plane": "data"},
            {"id": "e2", "from": "hc-probe", "to": "vm-zone-a", "label": "2. Health Probe (5s)", "plane": "control"},
            {"id": "e3", "from": "vm-zone-a", "to": "reg-pd", "label": "3. Synchronous Block Write", "plane": "data"},
            {"id": "e4", "from": "hc-probe", "to": "mig-mgr", "label": "4. Health Status Signal", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Load Balancer Dispatch", "edges": ["e1"], "action": "Load balancer forwards user transaction to healthy VM instance in Zone A.", "why_traversal": "Anycast distributes traffic to optimal zonal endpoints.", "protocol": "HTTP/1.1 TCP 8080", "plane": "Data Plane"},
            {"n": 2, "title": "Synchronous Disk Write", "edges": ["e3"], "action": "VM commits data block; Regional PD replicates to Zone B before acknowledging write.", "why_traversal": "Regional PD achieves RPO=0 across zonal datacenter outages.", "protocol": "SCSI / NVMe over Fabric", "plane": "Data Plane"},
            {"n": 3, "title": "Continuous Health Probing", "edges": ["e2", "e4"], "action": "Health prober validates response; reports healthy status to MIG controller.", "why_traversal": "Enables proactive eviction if backend becomes unresponsive.", "protocol": "HTTP GET /healthz", "plane": "Control Plane"}
        ],
        [
            {"id": "zone-a-failure", "label": "Zonal Datacenter Hardware Failure", "changes": {"failedNodes": ["vm-zone-a"], "failedEdges": ["e1", "e3"]}, "root_cause": "Hypervisor host hardware crash terminates VM in Zone A.", "diverted_path": "Health check flags timeout; MIG auto-heals by provisioning replacement VM in Zone B.", "blast_radius": "In-flight request retried by ALB; Regional PD reattaches with zero data loss.", "recovery": "Instance template boots in Zone B and mounts existing Regional PD."}
        ],
        # D2
        "Traces Compute Engine autoscaling and traffic dispatch: shows how Cloud Load Balancing distributes requests to healthy MIG instances based on CPU utilization.",
        "Autoscalers monitor aggregate CPU and load balancer utilization, adding VM instances across zones to keep average utilization below target thresholds.",
        [
            {"id": "g-ingress", "label": "Client Ingress & Load Balancing", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-autoscaler", "label": "Autoscaling Control Loop", "type": "project", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-backends", "label": "Managed Instance Group Fleet", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "client-stream", "label": "Surging Client Traffic", "product": "External Traffic Flow", "group": "g-ingress", "plane": "data", "x": 140, "y": 140, "detail": "Traffic surges from 1,000 to 10,000 QPS during flash sale."},
            {"id": "gfe-proxy", "label": "Cloud Load Balancer", "product": "External HTTPS LB", "group": "g-ingress", "plane": "data", "x": 140, "y": 280, "detail": "Terminates TLS and routes to backend service with round-robin balancing."},
            {"id": "mig-autoscaler", "label": "Compute Autoscaler", "product": "Target CPU: 70%", "group": "g-autoscaler", "plane": "control", "x": 440, "y": 200, "detail": "Monitors average CPU across fleet; calculates required VM count."},
            {"id": "vm-inst-1", "label": "VM Instance #1 (Saturated)", "product": "Zone A (95% CPU)", "group": "g-backends", "plane": "data", "x": 780, "y": 140, "detail": "Current running instance approaching saturation limit."},
            {"id": "vm-inst-2", "label": "VM Instance #2 (Scaled Out)", "product": "Zone B (Fresh Boot)", "group": "g-backends", "plane": "data", "x": 780, "y": 280, "detail": "Newly booted VM launched from instance template absorbing redirected load."}
        ],
        [
            {"id": "e1", "from": "client-stream", "to": "gfe-proxy", "label": "1. Influx Surge (10k QPS)", "plane": "data"},
            {"id": "e2", "from": "gfe-proxy", "to": "vm-inst-1", "label": "2. Dispatch Requests", "plane": "data"},
            {"id": "e3", "from": "vm-inst-1", "to": "mig-autoscaler", "label": "3. Telemetry: 95% CPU", "plane": "control"},
            {"id": "e4", "from": "mig-autoscaler", "to": "vm-inst-2", "label": "4. Spin Up Replica", "plane": "control"},
            {"id": "e5", "from": "gfe-proxy", "to": "vm-inst-2", "label": "5. Distribute Balanced Load", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Traffic Surge Ingress", "edges": ["e1", "e2"], "action": "Flash sale traffic drives VM #1 CPU to 95%, breaching 70% target threshold.", "why_traversal": "Load balancer forwards traffic to available healthy instances.", "protocol": "HTTPS 443", "plane": "Data Plane"},
            {"n": 2, "title": "Autoscaling Decision", "edges": ["e3", "e4"], "action": "Autoscaler detects CPU violation; orders MIG manager to provision VM #2 in Zone B.", "why_traversal": "Spreads capacity evenly across availability zones for redundancy.", "protocol": "Compute Engine API", "plane": "Control Plane"},
            {"n": 3, "title": "Traffic Equalization", "edges": ["e5"], "action": "VM #2 passes initialization check; load balancer dispatches 50% traffic to new VM.", "why_traversal": "Average CPU drops to 52%, restoring sub-100ms response latencies.", "protocol": "HTTP/2 Multiplexing", "plane": "Data Plane"}
        ],
        [
            {"id": "autoscaler-max-cap", "label": "MIG Maximum Capacity Reached", "changes": {"failedNodes": ["vm-inst-1"], "failedEdges": ["e2"]}, "root_cause": "Traffic exceeded maxReplicas = 10 setting in autoscaling policy.", "diverted_path": "No additional VMs provisioned; existing backends queue requests, increasing p99 latency.", "blast_radius": "Users experience latency degradation and 504 Gateway Timeouts.", "recovery": "Increase maxReplicas limit or configure secondary failover region."}
        ],
        # D3
        "Simulates VM hardware crash: demonstrates MIG auto-healing detecting consecutive health check probe timeouts, recreating the failed VM, and re-attaching persistent storage.",
        "The MIG auto-healing controller recreates instances in-place using the instance template, restoring zonal serving capacity within 120 seconds.",
        [
            {"id": "g-failed-zone", "label": "Degraded Zone A (Failed Host)", "type": "vpc", "scope": "zonal", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-healed-zone", "label": "Auto-Healing & Recovery Controller", "type": "project", "scope": "regional", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "crashed-vm", "label": "Crashed VM Instance", "product": "Kernel Panic / OOM", "group": "g-failed-zone", "plane": "data", "x": 220, "y": 140, "detail": "Operating system kernel hung; stops responding to TCP port 8080."},
            {"id": "health-prober", "label": "Auto-Healing Prober", "product": "HTTP Health Check", "group": "g-failed-zone", "plane": "control", "x": 220, "y": 280, "detail": "Consecutive timeouts (3x5s); declares instance UNHEALTHY."},
            {"id": "mig-healer", "label": "MIG Auto-Healer", "product": "Instance Group Manager", "group": "g-healed-zone", "plane": "control", "x": 700, "y": 140, "detail": "Issues compute.instances.delete and recreates fresh instance from golden template."},
            {"id": "recreated-vm", "label": "Recreated VM Instance", "product": "Fresh Clean Boot", "group": "g-healed-zone", "plane": "data", "x": 700, "y": 280, "detail": "Successfully boots, mounts persistent disk, and resumes serving customer traffic."}
        ],
        [
            {"id": "e1", "from": "health-prober", "to": "crashed-vm", "label": "1. Probe Timeout (Connection Refused)", "plane": "control"},
            {"id": "e2", "from": "health-prober", "to": "mig-healer", "label": "2. Signal Unhealthy Instance", "plane": "control"},
            {"id": "e3", "from": "mig-healer", "to": "recreated-vm", "label": "3. Recreate from Instance Template", "plane": "control"},
            {"id": "e4", "from": "recreated-vm", "to": "health-prober", "label": "4. Verify Healthy HTTP 200", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Failure Detection", "edges": ["e1"], "action": "Health prober sends HTTP request; receives TCP reset due to kernel hang.", "why_traversal": "Application-level health checks detect deadlocks that hypervisor pings miss.", "protocol": "TCP Connection Probe", "plane": "Control Plane"},
            {"n": 2, "title": "Auto-Healing Signal", "edges": ["e2"], "action": "Prober signals MIG manager after 3 consecutive failures (15s total).", "why_traversal": "Prevents premature restarts while avoiding extended customer outages.", "protocol": "MIG Controller Event", "plane": "Control Plane"},
            {"n": 3, "title": "Instance Re-creation", "edges": ["e3"], "action": "MIG auto-healer tears down corrupt VM and launches clean instance from image template.", "why_traversal": "Restores immutable, verified software state in under 90 seconds.", "protocol": "Compute Engine API", "plane": "Control Plane"},
            {"n": 4, "title": "Service Restoration", "edges": ["e4"], "action": "Recreated VM initializes and responds HTTP 200 OK; traffic resumes.", "why_traversal": "Self-healing architecture restores SLA without manual operator intervention.", "protocol": "HTTP 200 OK", "plane": "Control Plane"}
        ],
        [
            {"id": "persistent-crashloop", "label": "Corrupt Disk Boot CrashLoop", "changes": {"failedNodes": ["recreated-vm"], "failedEdges": ["e4"]}, "root_cause": "Root filesystem corruption on persistent disk causes new VM to panic during boot.", "diverted_path": "Recreated instance fails health check repeatedly; auto-healer throttles reboots.", "blast_radius": "Capacity remains degraded by 1 instance until image is patched.", "recovery": "Deploy stateless instances with OS on ephemeral disk and data on managed databases."}
        ]
    )

    # 014: GKE
    specs[14] = make_spec(
        14, "2.2", "Google Kubernetes Engine (GKE): Autopilot & Enterprise Clusters",
        "Maps Google Kubernetes Engine (GKE) architecture: establishes boundaries between Google-managed Control Plane, multi-zone Node Pools, Standalone NEGs, and Workload Identity.",
        "GKE separates control plane orchestration from data-plane execution. In Autopilot clusters, Google manages worker node provisioning, OS security, and auto-upgrades.",
        [
            {"id": "g-cp", "label": "Google-Managed Control Plane (API Server & etcd)", "type": "project", "scope": "global", "x": 30, "y": 30, "width": 260, "height": 360},
            {"id": "g-nodes", "label": "Multi-Zone Node Pool Subnet (RFC 1918)", "type": "vpc", "scope": "regional", "x": 310, "y": 30, "width": 310, "height": 360},
            {"id": "g-ingress-neg", "label": "Container-Native Ingress (Cloud Load Balancing)", "type": "external", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "k8s-api", "label": "K8s API Server", "product": "kube-apiserver", "group": "g-cp", "plane": "control", "x": 150, "y": 140, "detail": "Managed master endpoint validating declarative manifests and RBAC."},
            {"id": "etcd", "label": "etcd Consensus Store", "product": "Distributed Key-Value", "group": "g-cp", "plane": "control", "x": 150, "y": 280, "detail": "Replicated state store recording cluster specs, leases, and pod bindings."},
            {"id": "kubelet-node", "label": "GKE Worker Node", "product": "Container-Optimized OS", "group": "g-nodes", "plane": "data", "x": 450, "y": 140, "detail": "Host VM running containerd runtime and kubelet daemon."},
            {"id": "pod-workload", "label": "Application Pod", "product": "10.4.2.15 (VPC Native)", "group": "g-nodes", "plane": "data", "x": 450, "y": 280, "detail": "Container with direct IP routable across VPC via Alias IP / Andromeda."},
            {"id": "standalone-neg", "label": "Standalone NEG", "product": "Network Endpoint Group", "group": "g-ingress-neg", "plane": "data", "x": 780, "y": 200, "detail": "Directly registers Pod IPs with Cloud Load Balancer, bypassing kube-proxy iptables."}
        ],
        [
            {"id": "e1", "from": "k8s-api", "to": "etcd", "label": "1. Commit Pod Manifest", "plane": "control"},
            {"id": "e2", "from": "k8s-api", "to": "kubelet-node", "label": "2. Schedule to Worker Node", "plane": "control"},
            {"id": "e3", "from": "kubelet-node", "to": "pod-workload", "label": "3. Spawn Container Pod", "plane": "data"},
            {"id": "e4", "from": "pod-workload", "to": "standalone-neg", "label": "4. Register Pod IP Directly", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Manifest Commit", "edges": ["e1"], "action": "Deployment controller submits pod spec; API server writes state to etcd.", "why_traversal": "Raft consensus guarantees cluster state durability across control plane replicas.", "protocol": "etcd Raft RPC", "plane": "Control Plane"},
            {"n": 2, "title": "Kubelet Scheduling", "edges": ["e2", "e3"], "action": "kube-scheduler binds pod to node; kubelet invokes containerd to launch container.", "why_traversal": "VPC-native cluster assigns real RFC 1918 VPC IP directly to pod network namespace.", "protocol": "Container Runtime Interface (CRI)", "plane": "Data Plane"},
            {"n": 3, "title": "NEG Registration", "edges": ["e4"], "action": "NEG controller attaches pod IP directly to Cloud Load Balancer backend service.", "why_traversal": "Eliminates kube-proxy iptables overhead and double-hop routing latencies.", "protocol": "Compute Engine NEG API", "plane": "Control Plane"}
        ],
        [
            {"id": "pod-ip-exhaustion", "label": "Secondary Subnet CIDR Exhaustion", "changes": {"failedNodes": ["pod-workload"], "failedEdges": ["e3"]}, "root_cause": "Node pool scaled beyond /20 pod CIDR range; no IP addresses left for new pods.", "diverted_path": "Pods remain stuck in Pending state with FailedCreatePodSandBox error.", "blast_radius": "New pod replicas cannot schedule; autoscaling blocked.", "recovery": "Use GKE multi-pod CIDR feature to attach secondary subnet to node pool."}
        ],
        # D2
        "Traces container-native load balancing: shows client traffic routing from Google Cloud Load Balancer directly to Pod IPs via Standalone Network Endpoint Groups (NEGs).",
        "Container-native load balancing bypasses kube-proxy and iptables node hops, routing traffic directly from the load balancer to the pod IP for minimal latency.",
        [
            {"id": "g-client-edge", "label": "Client Ingress & Edge Proxy", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-neg-mesh", "label": "Cloud Load Balancing (NEG Routing)", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-gke-pods", "label": "VPC-Native Pod Fleet (Zone A & B)", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "user-client", "label": "Internet Client", "product": "User Browser", "group": "g-client-edge", "plane": "data", "x": 140, "y": 140, "detail": "Submits shopping cart transaction over HTTPS."},
            {"id": "gfe-edge", "label": "Anycast Edge GFE", "product": "Google Front End", "group": "g-client-edge", "plane": "data", "x": 140, "y": 280, "detail": "Terminates TLS 1.3 at closest PoP and evaluates Cloud Armor policies."},
            {"id": "backend-neg", "label": "Backend Service (NEG)", "product": "Cloud Load Balancing", "group": "g-neg-mesh", "plane": "control", "x": 440, "y": 200, "detail": "Maintains live table of healthy Pod IPs and port numbers across all cluster nodes."},
            {"id": "pod-1", "label": "Pod 1 (10.4.1.8)", "product": "Cart Service (Zone A)", "group": "g-gke-pods", "plane": "data", "x": 780, "y": 140, "detail": "Container receiving request directly; zero NodePort or kube-proxy hops."},
            {"id": "pod-2", "label": "Pod 2 (10.4.2.14)", "product": "Cart Service (Zone B)", "group": "g-gke-pods", "plane": "data", "x": 780, "y": 280, "detail": "Container replica in second zone receiving balanced traffic flow."}
        ],
        [
            {"id": "e1", "from": "user-client", "to": "gfe-edge", "label": "1. HTTPS POST /checkout", "plane": "data"},
            {"id": "e2", "from": "gfe-edge", "to": "backend-neg", "label": "2. Route to Backend NEG", "plane": "data"},
            {"id": "e3", "from": "backend-neg", "to": "pod-1", "label": "3a. Direct Pod IP Delivery", "plane": "data"},
            {"id": "e4", "from": "backend-neg", "to": "pod-2", "label": "3b. Direct Pod IP Delivery", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Client Ingress", "edges": ["e1"], "action": "User submits transaction; Google Front End terminates connection at edge.", "why_traversal": "Pulls packet into Google fiber within milliseconds.", "protocol": "HTTPS TLS 1.3", "plane": "Data Plane"},
            {"n": 2, "title": "NEG Health Filtering", "edges": ["e2"], "action": "Load balancer consults NEG endpoint table; balances traffic across healthy pods.", "why_traversal": "Container-native health checks verify pod readiness directly, not just node health.", "protocol": "Internal Andromeda Routing", "plane": "Control Plane"},
            {"n": 3, "title": "Direct Pod Delivery", "edges": ["e3", "e4"], "action": "Andromeda delivers packet directly to container vETH interface (10.4.1.8).", "why_traversal": "Bypasses kube-proxy iptables DNAT; preserves real client IP address without X-Forwarded-For loss.", "protocol": "HTTP/1.1 TCP", "plane": "Data Plane"}
        ],
        [
            {"id": "readiness-gate-fail", "label": "Pod Readiness Gate Failure", "changes": {"failedNodes": ["pod-1"], "failedEdges": ["e3"]}, "root_cause": "Container started but warm-up cache initialization took 30 seconds; readiness probe returned 503.", "diverted_path": "NEG controller delays adding pod to load balancer until readiness gate passes.", "blast_radius": "Zero customer traffic routed to cold container; existing pods serve traffic.", "recovery": "Configure readinessGates in pod spec to prevent premature traffic dispatch."}
        ],
        # D3
        "Simulates GKE worker node kernel panic: demonstrates node failure detection, Pod eviction, and automatic rescheduling onto healthy standby nodes.",
        "Kubernetes control plane detects NodeNotReady status, marks pods for eviction, and schedules replacements onto healthy nodes with available resource allocations.",
        [
            {"id": "g-failed-node", "label": "Failed Worker Node (Kernel Panic)", "type": "vpc", "scope": "zonal", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-control-heal", "label": "Control Plane Eviction & Standby Node", "type": "project", "scope": "regional", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "crashed-node", "label": "Crashed Worker Node", "product": "Kernel Panic / NodeNotReady", "group": "g-failed-node", "plane": "data", "x": 220, "y": 140, "detail": "Underlying Linux VM encounters kernel deadlock; kubelet heartbeat ceases."},
            {"id": "evicted-pod", "label": "Terminated Pod", "product": "Status: Terminating", "group": "g-failed-node", "plane": "data", "x": 220, "y": 280, "detail": "Pod running on crashed node loses network connectivity."},
            {"id": "node-controller", "label": "Node Lifecycle Controller", "product": "kube-controller-manager", "group": "g-control-heal", "plane": "control", "x": 700, "y": 140, "detail": "Detects 40s heartbeat timeout; evicts pods and triggers node auto-repair."},
            {"id": "standby-node", "label": "Healthy Standby Node", "product": "Zone B Node Pool", "group": "g-control-heal", "plane": "data", "x": 700, "y": 280, "detail": "Kube-scheduler immediately schedules replacement pod; container pulls and runs in <15s."}
        ],
        [
            {"id": "e1", "from": "crashed-node", "to": "node-controller", "label": "1. Heartbeat Timeout (NodeNotReady)", "plane": "control"},
            {"id": "e2", "from": "node-controller", "to": "evicted-pod", "label": "2. Evict Unresponsive Pods", "plane": "control"},
            {"id": "e3", "from": "node-controller", "to": "standby-node", "label": "3. Re-schedule Replacement Pod", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Node Failure Detection", "edges": ["e1"], "action": "Node controller detects missing kubelet lease update after 40 seconds.", "why_traversal": "Automated node monitoring identifies frozen hardware without human alerts.", "protocol": "Kubernetes Lease API", "plane": "Control Plane"},
            {"n": 2, "title": "Automated Pod Eviction", "edges": ["e2"], "action": "Controller sets node taint node.kubernetes.io/unreachable and evicts pods.", "why_traversal": "Ensures deployment replica count is restored on surviving cluster capacity.", "protocol": "Kubernetes Taint Controller", "plane": "Control Plane"},
            {"n": 3, "title": "Rapid Standby Reschedule", "edges": ["e3"], "action": "kube-scheduler places replacement pod onto healthy worker node in Zone B.", "why_traversal": "GKE Autopilot node auto-provisioning ensures capacity is always available.", "protocol": "kube-scheduler RPC", "plane": "Data Plane"}
        ],
        [
            {"id": "pvc-attachment-lock", "label": "ReadWriteOnce PersistentVolume Lock", "changes": {"failedNodes": ["standby-node"], "failedEdges": ["e3"]}, "root_cause": "Failed node did not release persistent disk lock (Multi-Attach error).", "diverted_path": "Replacement pod stuck in ContainerCreating waiting for volume detachment.", "blast_radius": "Stateful workloads experience delayed recovery (6-8 minutes).", "recovery": "Use Regional PD with volumeAttachment timeouts or transition to Cloud Spanner/Firestore."}
        ]
    )

    # 015: Serverless Compute: Cloud Run, Functions, and Workflows
    specs[15] = make_spec(
        15, "2.3", "Serverless Compute: Cloud Run, Functions, and Workflows",
        "Visualizes Serverless Compute architecture: details Cloud Run, Cloud Functions, Eventarc event brokers, and Serverless VPC Access Connectors.",
        "Cloud Run provides serverless container execution with automatic scale-to-zero. Serverless VPC Access enables private connectivity to internal VPC databases.",
        [
            {"id": "g-ingress-serv", "label": "Serverless Ingress & Event Trigger", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-run-core", "label": "Cloud Run Managed Container Fleet", "type": "project", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-private-vpc", "label": "Private VPC & Managed Database Tier", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "client-req", "label": "HTTPS Client / Eventarc", "product": "Client Invocation", "group": "g-ingress-serv", "plane": "data", "x": 140, "y": 140, "detail": "Public web request or Cloud Storage object creation event."},
            {"id": "run-proxy", "label": "Cloud Run Ingress Proxy", "product": "Envoy Edge Mesh", "group": "g-ingress-serv", "plane": "control", "x": 140, "y": 280, "detail": "Terminates TLS; manages container auto-scaling and concurrency multiplexing."},
            {"id": "run-instance", "label": "Container Instance", "product": "gVisor MicroVM (1 vCPU, 512MB)", "group": "g-run-core", "plane": "data", "x": 440, "y": 140, "detail": "Isolated sandboxed container handling up to 80 concurrent requests."},
            {"id": "vpc-connector", "label": "Serverless VPC Connector", "product": "vpcaccess.googleapis.com", "group": "g-run-core", "plane": "control", "x": 440, "y": 280, "detail": "Throughput-scalable bridge routing private RFC 1918 traffic from Cloud Run into VPC."},
            {"id": "cloud-sql", "label": "Cloud SQL (Private IP)", "product": "PostgreSQL (10.0.2.8)", "group": "g-private-vpc", "plane": "data", "x": 780, "y": 200, "detail": "Enterprise database rejecting public internet access; accepts internal VPC traffic only."}
        ],
        [
            {"id": "e1", "from": "client-req", "to": "run-proxy", "label": "1. Ingress Request", "plane": "data"},
            {"id": "e2", "from": "run-proxy", "to": "run-instance", "label": "2. Concurrency Dispatch", "plane": "data"},
            {"id": "e3", "from": "run-instance", "to": "vpc-connector", "label": "3. Internal RFC 1918 Route", "plane": "data"},
            {"id": "e4", "from": "vpc-connector", "to": "cloud-sql", "label": "4. Query Database", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Serverless Ingress", "edges": ["e1"], "action": "Request arrives at Cloud Run; proxy evaluates container concurrency.", "why_traversal": "If idle, launches microVM container in hundreds of milliseconds.", "protocol": "HTTPS TLS 1.3", "plane": "Data Plane"},
            {"n": 2, "title": "MicroVM Execution", "edges": ["e2"], "action": "Container processes request in gVisor sandbox; connects to private database.", "why_traversal": "gVisor provides hardware-grade multi-tenant security boundary.", "protocol": "Local gVisor Syscall", "plane": "Data Plane"},
            {"n": 3, "title": "Serverless VPC Egress", "edges": ["e3", "e4"], "action": "Packet traverses Serverless VPC Connector into private VPC to query Cloud SQL.", "why_traversal": "Allows serverless containers to communicate with private enterprise databases without public IPs.", "protocol": "TCP Port 5432 (PostgreSQL)", "plane": "Data Plane"}
        ],
        [
            {"id": "connector-throughput-saturation", "label": "VPC Connector Throughput Saturation", "changes": {"failedNodes": ["vpc-connector"], "failedEdges": ["e3"]}, "root_cause": "Concurrent database queries exceeded e2-micro VPC connector bandwidth limit (200 Mbps).", "diverted_path": "Packets dropped at VPC boundary; Cloud Run returns HTTP 500.", "blast_radius": "Database queries fail under high traffic surge.", "recovery": "Resize Serverless VPC Access connector to min 3 instances with e2-standard-4 machine types."}
        ],
        # D2
        "Traces cold-start and request invocation: from HTTPS client ingress through Cloud Run internal proxy to container startup and database query.",
        "When traffic arrives at an idle service, Cloud Run launches container instances in hundreds of milliseconds, dynamically adjusting concurrency per container.",
        [
            {"id": "g-req", "label": "Idle Ingress State", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-scaling", "label": "Scale-from-Zero Dynamic Controller", "type": "project", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-exec", "label": "Warmed Serving Container", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "user-wake", "label": "First User Request", "product": "HTTPS Invocation", "group": "g-req", "plane": "data", "x": 140, "y": 140, "detail": "Arrives at service that has scaled down to 0 instances to save costs."},
            {"id": "proxy-buffer", "label": "Cloud Run Request Buffer", "product": "Envoy Queue", "group": "g-req", "plane": "control", "x": 140, "y": 280, "detail": "Holds incoming HTTP connection open while container cold-starts."},
            {"id": "run-scaler", "label": "Instance Autoscaler", "product": "Scale-to-Zero Controller", "group": "g-scaling", "plane": "control", "x": 440, "y": 200, "detail": "Detects 0 available instances; pulls image and provisions microVM in 350ms."},
            {"id": "warm-container", "label": "Active Container Instance", "product": "Node.js Server", "group": "g-exec", "plane": "data", "x": 780, "y": 140, "detail": "Executes application bootstrap; binds to port $PORT (8080)."},
            {"id": "served-resp", "label": "HTTP 200 OK Response", "product": "Client Delivery", "group": "g-exec", "plane": "data", "x": 780, "y": 280, "detail": "Releases buffered request and streams payload back to client."}
        ],
        [
            {"id": "e1", "from": "user-wake", "to": "proxy-buffer", "label": "1. Ingress on Idle Service", "plane": "data"},
            {"id": "e2", "from": "proxy-buffer", "to": "run-scaler", "label": "2. Signal Cold Start Needed", "plane": "control"},
            {"id": "e3", "from": "run-scaler", "to": "warm-container", "label": "3. Provision & Bootstrap MicroVM", "plane": "control"},
            {"id": "e4", "from": "proxy-buffer", "to": "warm-container", "label": "4. Release Buffered HTTP Request", "plane": "data"},
            {"id": "e5", "from": "warm-container", "to": "served-resp", "label": "5. Stream Payload (HTTP 200)", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Idle Connection Buffering", "edges": ["e1", "e2"], "action": "Request arrives at 0-replica service; proxy buffers connection while notifying scaler.", "why_traversal": "Scale-to-zero saves 100% compute costs during periods of inactivity.", "protocol": "HTTPS 443", "plane": "Control Plane"},
            {"n": 2, "title": "Sub-Second MicroVM Boot", "edges": ["e3"], "action": "Cloud Run pulls container image from Artifact Registry cache and boots gVisor sandbox.", "why_traversal": "Container starts in ~350ms, minimizing cold start latency penalty.", "protocol": "Internal Infrastructure RPC", "plane": "Control Plane"},
            {"n": 3, "title": "Execution and Response", "edges": ["e4", "e5"], "action": "Proxy flushes buffered request to active container; application returns HTTP 200.", "why_traversal": "Subsequent requests reuse warm container with sub-10ms response times.", "protocol": "HTTP/1.1 TCP 8080", "plane": "Data Plane"}
        ],
        [
            {"id": "cold-start-timeout", "label": "Heavy Application Startup Timeout", "changes": {"failedNodes": ["warm-container"], "failedEdges": ["e3"]}, "root_cause": "Heavy Java/Spring container took 45s to initialize, exceeding container startup timeout.", "diverted_path": "Cloud Run terminates container; proxy returns HTTP 504 Gateway Timeout.", "blast_radius": "First users encounter failure after extended wait.", "recovery": "Configure min-instances = 1 to keep container warm; optimize JVM startup with GraalVM."}
        ],
        # D3
        "Simulates container cold-start latency spike and concurrency saturation: demonstrates min-instances configuration eliminating cold starts under surge.",
        "Setting min-instances maintains warm container replicas, ensuring zero-latency request handling during unpredictable traffic spikes.",
        [
            {"id": "g-cold-spike", "label": "Unpredictable Influx Spike", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-min-pool", "label": "Warm Min-Instances Pool & Concurrency Governor", "type": "project", "scope": "regional", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "burst-traffic", "label": "Sudden 5,000 QPS Burst", "product": "Flash Traffic Influx", "group": "g-cold-spike", "plane": "data", "x": 220, "y": 140, "detail": "Marketing campaign launches; sudden 100x traffic spike hits serverless service."},
            {"id": "concurrency-meter", "label": "Concurrency Monitor", "product": "Cloud Run Governor", "group": "g-cold-spike", "plane": "control", "x": 220, "y": 280, "detail": "Monitors active concurrent requests per container instance (limit: 80)."},
            {"id": "warm-pool", "label": "Warm Min-Instances Fleet", "product": "min-instances = 10", "group": "g-min-pool", "plane": "data", "x": 700, "y": 140, "detail": "Pre-warmed running containers ready to absorb immediate 800 concurrent connections."},
            {"id": "rapid-scale", "label": "Rapid Autoscaling Engine", "product": "Auto-scale up to 100", "group": "g-min-pool", "plane": "control", "x": 700, "y": 280, "detail": "Spins up 90 additional container instances dynamically within 5 seconds."}
        ],
        [
            {"id": "e1", "from": "burst-traffic", "to": "concurrency-meter", "label": "1. Influx Wave", "plane": "data"},
            {"id": "e2", "from": "concurrency-meter", "to": "warm-pool", "label": "2. Absorb Immediate Wave", "plane": "data"},
            {"id": "e3", "from": "concurrency-meter", "to": "rapid-scale", "label": "3. Trigger Dynamic Scale-Out", "plane": "control"},
            {"id": "e4", "from": "rapid-scale", "to": "warm-pool", "label": "4. Expand Active Fleet", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Zero-Latency Absorption", "edges": ["e1", "e2"], "action": "5,000 QPS influx arrives; pre-warmed min-instances absorb first wave instantly.", "why_traversal": "Min-instances eliminates cold-start penalty for critical user journeys.", "protocol": "HTTPS 443", "plane": "Data Plane"},
            {"n": 2, "title": "Scale-Out Trigger", "edges": ["e3"], "action": "Concurrency governor detects 80% saturation on warm instances; calls rapid scaler.", "why_traversal": "Predictive scaling prevents container memory exhaustion.", "protocol": "Internal Scale RPC", "plane": "Control Plane"},
            {"n": 3, "title": "Fleet Expansion", "edges": ["e4"], "action": "Autoscaler launches 90 additional container instances across multiple zones.", "why_traversal": "Accommodates full 5,000 QPS load while maintaining sub-80ms p95 latency.", "protocol": "gVisor Provisioning", "plane": "Control Plane"}
        ],
        [
            {"id": "db-connection-exhaustion", "label": "Downstream Database Connection Pool Exhaustion", "changes": {"failedNodes": ["warm-pool"], "failedEdges": ["e2"]}, "root_cause": "100 Cloud Run instances each opened 20 direct connections to PostgreSQL (2,000 total).", "diverted_path": "Cloud SQL rejects new TCP connections with 'FATAL: sorry, too many clients already'.", "blast_radius": "All API endpoints requiring database queries fail.", "recovery": "Deploy Cloud SQL Auth Proxy with built-in connection pooling or use PgBouncer."}
        ]
    )

    # 016: VPC Networking & Security
    specs[16] = make_spec(
        16, "2.4", "Virtual Private Cloud (VPC) Networking & Security",
        "Maps Virtual Private Cloud (VPC) Networking: establishes global VPC boundaries, multi-region subnets, Cloud NAT gateways, and Cloud Router dynamic BGP.",
        "Google Cloud VPCs are global resources spanning all regions. Subnets are regional, allowing compute instances across the globe to communicate privately without public IPs.",
        [
            {"id": "g-ext-net", "label": "External SaaS & Edge Internet", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-vpc-us", "label": "Global VPC: production-vpc (Subnet us-central1 / 10.1.0.0/24)", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-vpc-eu", "label": "Global VPC: production-vpc (Subnet europe-west1 / 10.2.0.0/24)", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "saas-api", "label": "External SaaS API", "product": "Public Payment Gateway", "group": "g-ext-net", "plane": "data", "x": 140, "y": 140, "detail": "External vendor endpoint requiring outbound HTTPS connectivity over public internet."},
            {"id": "cloud-nat", "label": "Cloud NAT Gateway", "product": "Regional Outbound NAT", "group": "g-vpc-us", "plane": "data", "x": 440, "y": 140, "detail": "Performs source network address translation for private RFC 1918 instances."},
            {"id": "vm-us", "label": "Private Compute VM (US)", "product": "10.1.0.5 (No Public IP)", "group": "g-vpc-us", "plane": "data", "x": 440, "y": 280, "detail": "Compute Engine instance processing local order transactions."},
            {"id": "cloud-router", "label": "Cloud Router (BGP)", "product": "ASN 64513 Dynamic BGP", "group": "g-vpc-eu", "plane": "control", "x": 780, "y": 140, "detail": "Exchanges dynamic routes and manages Cloud NAT port allocations."},
            {"id": "vm-eu", "label": "Private Database VM (EU)", "product": "10.2.0.8 (Europe Subnet)", "group": "g-vpc-eu", "plane": "data", "x": 780, "y": 280, "detail": "Private VM communicating directly with US VM over Google private fiber without public IPs."}
        ],
        [
            {"id": "e1", "from": "vm-us", "to": "cloud-nat", "label": "1. Outbound Egress to NAT", "plane": "data"},
            {"id": "e2", "from": "cloud-nat", "to": "saas-api", "label": "2. SNAT to SaaS API", "plane": "data"},
            {"id": "e3", "from": "vm-us", "to": "vm-eu", "label": "3. Global VPC Private Routing", "plane": "data"},
            {"id": "e4", "from": "cloud-router", "to": "cloud-nat", "label": "4. Dynamic Port Allocation", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Outbound NAT Egress", "edges": ["e1", "e2"], "action": "Private VM calls SaaS API; Cloud NAT translates 10.1.0.5:54321 to public IP 35.190.20.10:1024.", "why_traversal": "Private VMs communicate with internet APIs without exposing inbound listening ports.", "protocol": "TCP SYN / HTTPS 443", "plane": "Data Plane"},
            {"n": 2, "title": "Global Private Routing", "edges": ["e3"], "action": "US VM communicates directly with EU VM across Google's private Andromeda SDN backbone.", "why_traversal": "Global VPC routing eliminates VPN tunnels or public internet transit between regions.", "protocol": "Private RFC 1918 TCP", "plane": "Data Plane"},
            {"n": 3, "title": "Dynamic Port Scaling", "edges": ["e4"], "action": "Cloud Router automatically allocates additional port blocks to VM as connection count rises.", "why_traversal": "Dynamic Port Allocation prevents packet drops during outbound connection spikes.", "protocol": "Internal Control RPC", "plane": "Control Plane"}
        ],
        [
            {"id": "nat-exhaustion", "label": "Cloud NAT Port Pool Exhaustion", "changes": {"failedNodes": ["cloud-nat"], "failedEdges": ["e2"]}, "root_cause": "VM initiated 10,000 concurrent outbound connections; static port allocation ran out of ports.", "diverted_path": "New outbound TCP handshakes dropped; external SaaS calls time out.", "blast_radius": "Only outbound SaaS calls from this VM fail; intra-VPC traffic to EU VM continues normally.", "recovery": "Enable Dynamic Port Allocation on Cloud NAT and assign secondary NAT IP addresses."}
        ],
        # D2
        "Traces private VM outbound internet egress: from private RFC 1918 compute instance through Cloud NAT gateway to external SaaS APIs.",
        "Cloud NAT provides managed outbound source IP translation, allowing private VMs to download software updates without exposing inbound attack surfaces.",
        [
            {"id": "g-client-vm", "label": "Private Subnet (us-central1-a)", "type": "subnet", "scope": "zonal", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-andromeda-core", "label": "VPC Andromeda Routing Mesh", "type": "vpc", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-ext-gateway", "label": "Internet Gateway & External SaaS", "type": "external", "scope": "external", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "private-vm", "label": "Private VM (10.1.0.5)", "product": "Compute Instance", "group": "g-client-vm", "plane": "data", "x": 140, "y": 140, "detail": "Application instance without external public IP address."},
            {"id": "firewall-engine", "label": "VPC Firewall Egress Rule", "product": "Hierarchical Firewall", "group": "g-client-vm", "plane": "control", "x": 140, "y": 280, "detail": "Evaluates allow-egress-to-saas rule (TCP 443 priority 1000)."},
            {"id": "andromeda-sw", "label": "Andromeda vSwitch", "product": "VPC Virtual Switch", "group": "g-andromeda-core", "plane": "data", "x": 440, "y": 140, "detail": "Encapsulates packet; consults VPC route table for 0.0.0.0/0 default route."},
            {"id": "nat-engine", "label": "Cloud NAT Gateway", "product": "NAT IP 34.120.80.5", "group": "g-andromeda-core", "plane": "data", "x": 440, "y": 280, "detail": "Replaces private source IP and port with public NAT IP and allocated port."},
            {"id": "saas-endpoint", "label": "External SaaS Service", "product": "api.stripe.com", "group": "g-ext-gateway", "plane": "data", "x": 780, "y": 200, "detail": "Receives authorized API call originating from verified Cloud NAT static IP."}
        ],
        [
            {"id": "e1", "from": "private-vm", "to": "firewall-engine", "label": "1. Check Egress Firewall", "plane": "control"},
            {"id": "e2", "from": "private-vm", "to": "andromeda-sw", "label": "2. Forward Packet to vSwitch", "plane": "data"},
            {"id": "e3", "from": "andromeda-sw", "to": "nat-engine", "label": "3. Match Default Internet Route", "plane": "data"},
            {"id": "e4", "from": "nat-engine", "to": "saas-endpoint", "label": "4. SNAT Egress to Public Internet", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Firewall Rule Validation", "edges": ["e1"], "action": "VPC firewall verifies outbound TCP port 443 is permitted.", "why_traversal": "Egress firewall rules enforce defense-in-depth against data exfiltration.", "protocol": "Stateful Firewall Inspection", "plane": "Control Plane"},
            {"n": 2, "title": "Route Table Lookup", "edges": ["e2", "e3"], "action": "Andromeda vSwitch matches 0.0.0.0/0 next-hop default internet gateway.", "why_traversal": "Directs outbound packet to Cloud NAT for source address translation.", "protocol": "Internal VPC Route", "plane": "Data Plane"},
            {"n": 3, "title": "SNAT Translation & Egress", "edges": ["e4"], "action": "Cloud NAT allocates port 12048 and transmits packet to api.stripe.com.", "why_traversal": "Vendor sees static Google Cloud IP; replies return along stateful reverse mapping.", "protocol": "HTTPS TLS 1.3", "plane": "Data Plane"}
        ],
        [
            {"id": "egress-firewall-deny", "label": "Egress Firewall Deny Rule Triggered", "changes": {"failedNodes": ["firewall-engine"], "failedEdges": ["e2"]}, "root_cause": "Default egress deny rule blocked unauthorized outbound port 22 / 8080.", "diverted_path": "Packet dropped silently at vNIC boundary; VPC Flow Log captures denial.", "blast_radius": "Only unauthorized ports blocked; approved port 443 traffic continues.", "recovery": "Create explicit egress firewall rule allowing target destination CIDR and port."}
        ],
        # D3
        "Simulates Cloud NAT port exhaustion outage: demonstrates high-concurrency connections dropping SYN packets and automated dynamic port allocation recovery.",
        "Enabling Dynamic Port Allocation allows Cloud NAT to automatically assign additional IP ports to saturated VMs, preventing connection dropouts.",
        [
            {"id": "g-sat-vm", "label": "Port-Saturated Private VM", "type": "subnet", "scope": "zonal", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-dynamic-nat", "label": "Cloud NAT Dynamic Port Allocation Recovery", "type": "vpc", "scope": "regional", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "saturated-vm", "label": "Private VM (Port Saturated)", "product": "10.1.0.5 (64/64 Ports Used)", "group": "g-sat-vm", "plane": "data", "x": 220, "y": 140, "detail": "Batch scraper attempts 500 simultaneous outbound API connections."},
            {"id": "drop-counter", "label": "Andromeda Drop Counter", "product": "VPC Flow Logs", "group": "g-sat-vm", "plane": "control", "x": 220, "y": 280, "detail": "Detects dropped SYN packets: router.googleapis.com/nat/dropped_sent_packets_count."},
            {"id": "dynamic-allocator", "label": "Cloud NAT Dynamic Allocator", "product": "Dynamic Port Allocation", "group": "g-dynamic-nat", "plane": "control", "x": 700, "y": 140, "detail": "Expands allocated port block from 64 to 512 ports dynamically per VM."},
            {"id": "secondary-nat-ip", "label": "Secondary NAT IP Address", "product": "34.120.90.12 (Pool Expansion)", "group": "g-dynamic-nat", "plane": "data", "x": 700, "y": 280, "detail": "Adds 64,512 additional outbound ephemeral ports to the regional pool."}
        ],
        [
            {"id": "e1", "from": "saturated-vm", "to": "drop-counter", "label": "1. SYN Drop (Port Starvation)", "plane": "control"},
            {"id": "e2", "from": "drop-counter", "to": "dynamic-allocator", "label": "2. Trigger Port Expansion", "plane": "control"},
            {"id": "e3", "from": "dynamic-allocator", "to": "secondary-nat-ip", "label": "3. Provision Additional NAT IP", "plane": "control"},
            {"id": "e4", "from": "saturated-vm", "to": "secondary-nat-ip", "label": "4. Outbound Connections Restored", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Port Starvation Detection", "edges": ["e1"], "action": "VM exhausts minimum 64 allocated ports; subsequent SYN attempts drop.", "why_traversal": "Static allocation restricts each VM to a fixed slice of the 64k port range.", "protocol": "TCP SYN", "plane": "Control Plane"},
            {"n": 2, "title": "Dynamic Port Allocation", "edges": ["e2", "e3"], "action": "Dynamic Port Allocation automatically scales VM allocation up to max 1,024 ports.", "why_traversal": "Adapts port assignments to real-time workload demand without VM restart.", "protocol": "Internal NAT Control", "plane": "Control Plane"},
            {"n": 3, "title": "Connection Flow Recovery", "edges": ["e4"], "action": "VM uses new port block to complete TCP handshakes with zero packet drop.", "why_traversal": "Secondary NAT IP doubles total pool capacity, eliminating drops under surge.", "protocol": "TCP Established", "plane": "Data Plane"}
        ],
        [
            {"id": "max-ports-breached", "label": "Cloud NAT Max Ports Per VM Limit Hit", "changes": {"failedNodes": ["saturated-vm"], "failedEdges": ["e1"]}, "root_cause": "Workload exceeded max_ports_per_vm = 1024 setting due to connection pooling bug.", "diverted_path": "Additional connections dropped until idle sockets time out.", "blast_radius": "Confined to rogue VM initiating unbounded connection loops.", "recovery": "Implement HTTP connection keep-alive in application code; raise max_ports_per_vm."}
        ]
    )

    # 017: Load Balancing, CDN & Cloud Armor
    specs[17] = make_spec(
        17, "2.5", "Cloud Load Balancing, Cloud CDN, and Cloud Armor",
        "Maps Google Cloud Load Balancing, Cloud CDN, and Cloud Armor: establishes edge defense layers between internet clients and internal VPC backend services.",
        "Traffic terminates at Google's global Anycast edge. Cloud Armor inspects layer 7 traffic for OWASP threats, Cloud CDN serves cached assets, and ALB routes to healthy backends.",
        [
            {"id": "g-edge-perimeter", "label": "Google Global Anycast Edge (GFE Fleet)", "type": "region", "scope": "global", "x": 30, "y": 30, "width": 260, "height": 360},
            {"id": "g-defense-tier", "label": "Cloud Armor & Edge Caching (Cloud CDN)", "type": "project", "scope": "global", "x": 310, "y": 30, "width": 310, "height": 360},
            {"id": "g-backends-vpc", "label": "Regional Backend Service (VPC Subnets)", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "client-anycast", "label": "Global Internet Clients", "product": "Global Traffic Ingress", "group": "g-edge-perimeter", "plane": "data", "x": 150, "y": 140, "detail": "Worldwide users connecting to single Anycast VIP 34.120.50.80."},
            {"id": "gfe-proxy", "label": "Google Front End (GFE)", "product": "Global External ALB", "group": "g-edge-perimeter", "plane": "data", "x": 150, "y": 280, "detail": "Terminates TLS; offloads HTTP/2 and HTTP/3 QUIC handshakes."},
            {"id": "cloud-armor", "label": "Cloud Armor WAF", "product": "OWASP & DDoS Protection", "group": "g-defense-tier", "plane": "control", "x": 450, "y": 140, "detail": "Inspects SQLi, XSS, and applies rate-limiting rules at line rate."},
            {"id": "cloud-cdn", "label": "Cloud CDN Edge Cache", "product": "Edge Cache Memory", "group": "g-defense-tier", "plane": "data", "x": 450, "y": 280, "detail": "Caches static images, CSS, and video segments; serves cache hits in <10ms."},
            {"id": "backend-mig", "label": "Regional Backend MIG", "product": "Compute Engine (10.1.0.0/24)", "group": "g-backends-vpc", "plane": "data", "x": 780, "y": 200, "detail": "Private autoscaling application backends receiving decrypted HTTP requests."}
        ],
        [
            {"id": "e1", "from": "client-anycast", "to": "gfe-proxy", "label": "1. Single Global Anycast VIP", "plane": "data"},
            {"id": "e2", "from": "gfe-proxy", "to": "cloud-armor", "label": "2. Security Inspection", "plane": "control"},
            {"id": "e3", "from": "gfe-proxy", "to": "cloud-cdn", "label": "3. Edge Cache Evaluation", "plane": "data"},
            {"id": "e4", "from": "cloud-cdn", "to": "backend-mig", "label": "4. Forward Cache Miss to Origin", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Global Edge Termination", "edges": ["e1"], "action": "Clients worldwide connect to single Anycast IP; TLS terminates at closest edge PoP.", "why_traversal": "Minimizes round-trip latency for TLS negotiation before internal routing.", "protocol": "HTTP/3 QUIC / TLS 1.3", "plane": "Data Plane"},
            {"n": 2, "title": "Inline WAF Filtering", "edges": ["e2"], "action": "Cloud Armor evaluates incoming request headers against OWASP Top 10 rules.", "why_traversal": "Blocks malicious attacks at Google's edge before consuming backend compute.", "protocol": "Cloud Armor Policy Engine", "plane": "Control Plane"},
            {"n": 3, "title": "Edge Cache Check", "edges": ["e3"], "action": "Cloud CDN checks edge storage; serves cached asset immediately if found.", "why_traversal": "Reduces origin server load and eliminates bandwidth egress fees.", "protocol": "Cache Lookup", "plane": "Data Plane"},
            {"n": 4, "title": "Origin Forwarding", "edges": ["e4"], "action": "On cache miss, request traverses private fiber to regional backend MIG instances.", "why_traversal": "Internal Andromeda transport guarantees encrypted, predictable delivery.", "protocol": "Encapsulated HTTP/1.1", "plane": "Data Plane"}
        ],
        [
            {"id": "ddos-layer7", "label": "Volumetric HTTP Flood Attack", "changes": {"failedNodes": ["cloud-armor"], "failedEdges": ["e4"]}, "root_cause": "Botnet launches 500,000 req/sec Layer 7 HTTP GET flood against login endpoint.", "diverted_path": "Cloud Armor adaptive rate limit rule triggers; drops attacking IPs with HTTP 429 at edge.", "blast_radius": "Attack absorbed entirely at Google edge PoPs; backend instances stay at 15% CPU.", "recovery": "Security team tightens Cloud Armor rate-limit threshold to 100 req/min per IP."}
        ],
        # D2
        "Traces an external HTTPS request: from edge Anycast IP through Cloud Armor security evaluation and Cloud CDN cache check to backend Compute Engine VM.",
        "Global External ALB terminates TLS handshakes at the edge nearest the client, routing decrypted payloads across Google's high-speed fiber backbone.",
        [
            {"id": "g-ingress-edge", "label": "Edge Anycast Ingress", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-inspection-mesh", "label": "Cloud Armor Security Inspection", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-backend-origin", "label": "VPC Origin Backend Instances", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "client-browser", "label": "Web Client (San Francisco)", "product": "User Browser", "group": "g-ingress-edge", "plane": "data", "x": 140, "y": 140, "detail": "Submits HTTPS GET /static/logo.png request."},
            {"id": "edge-gfe", "label": "Anycast Edge GFE (Bay Area)", "product": "Google Front End", "group": "g-ingress-edge", "plane": "data", "x": 140, "y": 280, "detail": "Terminates TCP/TLS; extracts URI path and client IP 198.51.100.24."},
            {"id": "armor-eval", "label": "Cloud Armor Evaluator", "product": "Security Policy Rule", "group": "g-inspection-mesh", "plane": "control", "x": 440, "y": 140, "detail": "Confirms client IP is not on deny-list and request contains no SQLi signatures."},
            {"id": "cdn-cache", "label": "Cloud CDN Cache Hit", "product": "Edge Cache HIT", "group": "g-inspection-mesh", "plane": "data", "x": 440, "y": 280, "detail": "Finds valid cached copy of logo.png; prepares immediate HTTP 200 payload."},
            {"id": "origin-vm", "label": "Origin Backend VM", "product": "App Server (Idle)", "group": "g-backend-origin", "plane": "data", "x": 780, "y": 200, "detail": "Origin server remains untouched; zero CPU cycles spent on static asset requests."}
        ],
        [
            {"id": "e1", "from": "client-browser", "to": "edge-gfe", "label": "1. HTTPS GET /static/logo.png", "plane": "data"},
            {"id": "e2", "from": "edge-gfe", "to": "armor-eval", "label": "2. Evaluate Security Policy", "plane": "control"},
            {"id": "e3", "from": "armor-eval", "to": "cdn-cache", "label": "3. Lookup Asset Cache Key", "plane": "data"},
            {"id": "e4", "from": "cdn-cache", "to": "client-browser", "label": "4. Immediate Cache Hit Delivery", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Edge Ingress", "edges": ["e1"], "action": "Client request lands on San Francisco Anycast PoP; TLS handshakes in 8ms.", "why_traversal": "Edge termination eliminates long cross-country TLS negotiation latency.", "protocol": "TLS 1.3 TCP 443", "plane": "Data Plane"},
            {"n": 2, "title": "Armor Validation", "edges": ["e2"], "action": "Cloud Armor inspects request headers and parameters at hardware speed.", "why_traversal": "Ensures malicious payloads are dropped before touching cache or backends.", "protocol": "Inline Policy Filter", "plane": "Control Plane"},
            {"n": 3, "title": "Cache Hit Return", "edges": ["e3", "e4"], "action": "Cloud CDN retrieves cached asset from RAM and streams HTTP 200 to client.", "why_traversal": "Total response time is 12ms; origin backend VM is never contacted.", "protocol": "HTTP/2 200 OK", "plane": "Data Plane"}
        ],
        [
            {"id": "cache-miss-stampede", "label": "Cache Stampede / Origin Overload", "changes": {"failedNodes": ["cdn-cache"], "failedEdges": ["e4"]}, "root_cause": "Cache expired during viral traffic surge; 50,000 concurrent requests bypassed CDN to origin.", "diverted_path": "Origin VM CPU saturates to 100%; request latency spikes to 4,000ms.", "blast_radius": "Dynamic API calls queued behind static image processing.", "recovery": "Enable Cloud CDN request collapsing and serve-stale-while-revalidating settings."}
        ],
        # D3
        "Simulates volumetric Layer 7 DDoS attack: demonstrates Cloud Armor rate-limiting rules detecting malicious IP floods and dropping packets at the edge.",
        "Cloud Armor filters millions of malicious requests per second at Google's edge, preventing upstream application servers from suffering CPU or memory exhaustion.",
        [
            {"id": "g-ddos-source", "label": "Botnet DDoS Ingress (10,000 IPs)", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-edge-drop", "label": "Google Edge Cloud Armor Shield", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "botnet-flood", "label": "Botnet HTTP Flood", "product": "100k QPS Layer 7 Attack", "group": "g-ddos-source", "plane": "data", "x": 220, "y": 140, "detail": "Distributed malicious nodes hammering /api/login endpoint with randomized headers."},
            {"id": "rate-limit-rule", "label": "Cloud Armor Rate Limiter", "product": "Rule: 100 req/min per IP", "group": "g-ddos-source", "plane": "control", "x": 220, "y": 280, "detail": "Monitors per-client request frequency; flags clients breaching 100 req/min threshold."},
            {"id": "edge-blocker", "label": "Edge Drop Engine (GFE)", "product": "HTTP 429 Dropper", "group": "g-edge-drop", "plane": "control", "x": 700, "y": 140, "detail": "Drops malicious TCP sockets directly at edge PoPs; returns HTTP 429 Too Many Requests."},
            {"id": "protected-origin", "label": "Healthy Application Origin", "product": "Backend VM Cluster", "group": "g-edge-drop", "plane": "data", "x": 700, "y": 280, "detail": "Origin backend servers remain at 12% CPU, serving legitimate users seamlessly."}
        ],
        [
            {"id": "e1", "from": "botnet-flood", "to": "rate-limit-rule", "label": "1. Flood Request Stream", "plane": "data"},
            {"id": "e2", "from": "rate-limit-rule", "to": "edge-blocker", "label": "2. Activate Rate-Limit Drop", "plane": "control"},
            {"id": "e3", "from": "edge-blocker", "to": "protected-origin", "label": "3. Forward Filtered Valid Traffic", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Attack Influx", "edges": ["e1"], "action": "Botnet opens 100,000 HTTP requests per second across worldwide Anycast PoPs.", "why_traversal": "Anycast distributes the attack across hundreds of Google edge facilities.", "protocol": "HTTP/1.1 Flood", "plane": "Data Plane"},
            {"n": 2, "title": "Edge Rate-Limiting", "edges": ["e2"], "action": "Cloud Armor rate limiting triggers immediately, rejecting attacking IPs with HTTP 429.", "why_traversal": "Filtering happens in Google edge silicon; zero malicious packets reach backends.", "protocol": "Cloud Armor Edge Rule", "plane": "Control Plane"},
            {"n": 3, "title": "Protected Operations", "edges": ["e3"], "action": "Clean customer transactions pass through unharmed; origin backends operate normally.", "why_traversal": "Maintains 99.99% availability during severe volumetric cyber attacks.", "protocol": "Clean HTTPS Traffic", "plane": "Data Plane"}
        ],
        [
            {"id": "false-positive-lockout", "label": "NAT Gateway False Positive Block", "changes": {"failedNodes": ["rate-limit-rule"], "failedEdges": ["e2"]}, "root_cause": "Rate limit rule grouped all enterprise corporate office users behind a single egress IP.", "diverted_path": "Legitimate corporate employees blocked by Cloud Armor threshold.", "blast_radius": "All employees on corporate WiFi receive HTTP 429.", "recovery": "Configure Cloud Armor rate limiting based on Session Cookie or User-Agent instead of raw IP."}
        ]
    )

    # 018: Hybrid and Multi-Cloud Connectivity
    specs[18] = make_spec(
        18, "2.6", "Hybrid and Multi-Cloud Connectivity: VPN & Interconnect",
        "Maps Hybrid and Multi-Cloud Connectivity: details Cloud HA VPN 99.99% dual tunnels, Dedicated Interconnect, and Cloud Router dynamic BGP routing.",
        "Enterprise hybrid networks combine high-bandwidth Dedicated Interconnect with encrypted Cloud HA VPN backup tunnels, synchronized via dynamic BGP.",
        [
            {"id": "g-onprem-dc", "label": "Enterprise On-Premises Datacenter", "type": "onprem", "scope": "onprem", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-hybrid-mesh", "label": "Hybrid Edge (Interconnect & HA VPN)", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-gcp-vpc", "label": "Google Cloud VPC (production-vpc)", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "corp-router", "label": "On-Prem Core Router", "product": "Cisco / Juniper (ASN 65001)", "group": "g-onprem-dc", "plane": "data", "x": 140, "y": 140, "detail": "Enterprise border router with dual redundant physical cross-connects."},
            {"id": "corp-lan", "label": "Corporate Subnet", "product": "192.168.10.0/24", "group": "g-onprem-dc", "plane": "data", "x": 140, "y": 280, "detail": "Internal corporate workstations and legacy databases."},
            {"id": "dedicated-ic", "label": "Dedicated Interconnect", "product": "100 Gbps Physical Link", "group": "g-hybrid-mesh", "plane": "data", "x": 440, "y": 140, "detail": "Direct fiber cross-connect into Google colocation facility (99.99% SLA)."},
            {"id": "ha-vpn", "label": "Cloud HA VPN (Dual Tunnels)", "product": "IPsec Encrypted (99.99%)", "group": "g-hybrid-mesh", "plane": "data", "x": 440, "y": 280, "detail": "Encrypted backup tunnel running across public internet with dual active interfaces."},
            {"id": "cloud-router-bgp", "label": "Cloud Router (BGP)", "product": "ASN 64513 Dynamic BGP", "group": "g-gcp-vpc", "plane": "control", "x": 780, "y": 140, "detail": "Exchanges BGP routes with on-prem; sets MED=100 for Interconnect, MED=200 for VPN."},
            {"id": "gcp-db", "label": "Private Cloud Workload", "product": "Compute / Spanner (10.0.1.0/24)", "group": "g-gcp-vpc", "plane": "data", "x": 780, "y": 280, "detail": "Google Cloud resources receiving low-latency hybrid packets."}
        ],
        [
            {"id": "e1", "from": "corp-lan", "to": "corp-router", "label": "1. Corporate Outbound Traffic", "plane": "data"},
            {"id": "e2", "from": "corp-router", "to": "dedicated-ic", "label": "2. Primary 100G Path (MED 100)", "plane": "data"},
            {"id": "e3", "from": "corp-router", "to": "ha-vpn", "label": "2b. Standby IPsec Path (MED 200)", "plane": "data"},
            {"id": "e4", "from": "dedicated-ic", "to": "cloud-router-bgp", "label": "3. BGP Route Propagation", "plane": "control"},
            {"id": "e5", "from": "dedicated-ic", "to": "gcp-db", "label": "4. Private Low-Latency Delivery", "plane": "data"}
        ],
        [
            {"n": 1, "title": "BGP Route Exchange", "edges": ["e4"], "action": "Cloud Router and corporate router exchange routes dynamically via eBGP.", "why_traversal": "Dynamic BGP eliminates manual static route updates and supports instant failover.", "protocol": "BGP TCP 179", "plane": "Control Plane"},
            {"n": 2, "title": "Primary Interconnect Ingress", "edges": ["e1", "e2", "e5"], "action": "Packet traverses Dedicated Interconnect with 100Gbps line rate and <3ms latency.", "why_traversal": "BGP MED (Multi-Exit Discriminator) prioritizes lowest-cost Interconnect link over VPN.", "protocol": "802.1Q VLAN / IP", "plane": "Data Plane"},
            {"n": 3, "title": "Standby Readiness", "edges": ["e3"], "action": "Cloud HA VPN keeps BGP session active in standby mode, ready for instant switchover.", "why_traversal": "Guarantees 99.99% enterprise network SLA across physical disaster scenarios.", "protocol": "IPsec IKEv2", "plane": "Control Plane"}
        ],
        [
            {"id": "fiber-cut-primary", "label": "Primary Interconnect Physical Fiber Cut", "changes": {"failedNodes": ["dedicated-ic"], "failedEdges": ["e2", "e5"]}, "root_cause": "Metropolitan construction severs physical fiber cross-connect into Google colocation facility.", "diverted_path": "BGP keepalive timeout (3s) withdraws Interconnect route; traffic instantly diverts to Cloud HA VPN.", "blast_radius": "Sub-second session failover; bandwidth drops from 100Gbps to 3Gbps IPsec ceiling.", "recovery": "Enterprise traffic continues uninterrupted; fiber technicians repair cross-connect."}
        ],
        # D2
        "Traces on-premises to Google Cloud private packet flow: from corporate datacenter router across Dedicated Interconnect to private VPC workloads.",
        "Cloud Router exchanges BGP routes dynamically, ensuring on-premises clients reach Google Cloud subnets across the lowest-latency interconnect path.",
        [
            {"id": "g-onprem-src", "label": "On-Premises ERP Server", "type": "onprem", "scope": "onprem", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-interconnect-pipe", "label": "Dedicated Interconnect Fiber & VLAN", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-target-vpc", "label": "GCP Target Subnet (us-east4)", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "erp-client", "label": "SAP ERP Host (192.168.1.50)", "product": "On-Prem Linux Server", "group": "g-onprem-src", "plane": "data", "x": 140, "y": 140, "detail": "Submits batch financial ledger sync to cloud database."},
            {"id": "dc-switch", "label": "Datacenter Core Switch", "product": "802.1Q VLAN Tagging", "group": "g-onprem-src", "plane": "data", "x": 140, "y": 280, "detail": "Tags frames with VLAN ID 450; forwards to Google Interconnect cross-connect."},
            {"id": "interconnect-pipe", "label": "Interconnect LAG (2x10G)", "product": "Direct Fiber Cross-Connect", "group": "g-interconnect-pipe", "plane": "data", "x": 440, "y": 140, "detail": "Private physical circuit terminating in Google Ashburn colocation facility."},
            {"id": "vlan-attachment", "label": "Cloud Interconnect Attachment", "product": "Partner / Dedicated VLAN", "group": "g-interconnect-pipe", "plane": "control", "x": 440, "y": 280, "detail": "Binds physical VLAN into private VPC network routing table."},
            {"id": "cloud-db-target", "label": "Cloud SQL Replica (10.0.4.12)", "product": "PostgreSQL Target", "group": "g-target-vpc", "plane": "data", "x": 780, "y": 200, "detail": "Receives streaming replication packets at sub-3ms latency without public internet hops."}
        ],
        [
            {"id": "e1", "from": "erp-client", "to": "dc-switch", "label": "1. Dispatch Private Payload", "plane": "data"},
            {"id": "e2", "from": "dc-switch", "to": "interconnect-pipe", "label": "2. VLAN Encapsulation (802.1Q)", "plane": "data"},
            {"id": "e3", "from": "interconnect-pipe", "to": "vlan-attachment", "label": "3. Terminate on Cloud Attachment", "plane": "control"},
            {"id": "e4", "from": "vlan-attachment", "to": "cloud-db-target", "label": "4. Direct Private Subnet Delivery", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Datacenter Frame Tagging", "edges": ["e1", "e2"], "action": "Core switch attaches VLAN tag 450 and transmits packet over 10G optical transceiver.", "why_traversal": "VLAN attachments segment different enterprise tenants across physical circuits.", "protocol": "Ethernet 802.1Q", "plane": "Data Plane"},
            {"n": 2, "title": "Optical Transit", "edges": ["e3"], "action": "Packet traverses Google fiber cross-connect; attachment verifies BGP route entry.", "why_traversal": "Guaranteed bandwidth with zero packet loss or encryption CPU overhead.", "protocol": "Optical Fiber Line Rate", "plane": "Data Plane"},
            {"n": 3, "title": "Database Ingestion", "edges": ["e4"], "action": "Andromeda delivers packet to Cloud SQL internal IP 10.0.4.12.", "why_traversal": "High-throughput database synchronization completes within SLA.", "protocol": "TCP Port 5432", "plane": "Data Plane"}
        ],
        [
            {"id": "bgp-asn-mismatch", "label": "BGP Peer ASN Configuration Error", "changes": {"failedNodes": ["vlan-attachment"], "failedEdges": ["e3"]}, "root_cause": "Network engineer misconfigured remote ASN as 65002 instead of 65001 on Cloud Router.", "diverted_path": "BGP session remains in Connect/Active state; routes not installed into VPC table.", "blast_radius": "All traffic across VLAN attachment blocked.", "recovery": "Correct peer ASN configuration on Cloud Router to match on-premises router."}
        ],
        # D3
        "Simulates primary Interconnect fiber cut: demonstrates Cloud Router BGP keepalive timeout and automated sub-second failover to Cloud HA VPN.",
        "BGP detects physical link failure within 3 seconds, withdrawing the primary route and shifting traffic to the standby HA VPN tunnel without dropped sessions.",
        [
            {"id": "g-failed-fiber", "label": "Primary Interconnect Cut", "type": "onprem", "scope": "onprem", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-failover-vpn", "label": "Automated BGP Failover to Cloud HA VPN", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "fiber-cut-event", "label": "Fiber Cut (Optical Loss)", "product": "Physical Link Failure", "group": "g-failed-fiber", "plane": "data", "x": 220, "y": 140, "detail": "Backhoe cuts fiber conduit outside colocation facility; link state goes down."},
            {"id": "bgp-monitor", "label": "BGP Keepalive Sentinel", "product": "Hold Timer = 9s", "group": "g-failed-fiber", "plane": "control", "x": 220, "y": 280, "detail": "3 missed keepalives (3s intervals); tears down primary BGP peering session."},
            {"id": "cloud-router-fail", "label": "Cloud Router Route Manager", "product": "BGP Dynamic Routing", "group": "g-failover-vpn", "plane": "control", "x": 700, "y": 140, "detail": "Withdraws 100G route; recalculates next-hop to secondary Cloud HA VPN tunnel (MED 200)."},
            {"id": "ha-vpn-active", "label": "Cloud HA VPN Tunnel #1", "product": "IPsec Active Route", "group": "g-failover-vpn", "plane": "data", "x": 700, "y": 280, "detail": "Absorbs enterprise traffic flow across encrypted internet path within 2.8 seconds."}
        ],
        [
            {"id": "e1", "from": "fiber-cut-event", "to": "bgp-monitor", "label": "1. Loss of Carrier (LoC)", "plane": "control"},
            {"id": "e2", "from": "bgp-monitor", "to": "cloud-router-fail", "label": "2. BGP Session Down Event", "plane": "control"},
            {"id": "e3", "from": "cloud-router-fail", "to": "ha-vpn-active", "label": "3. Promote Standby VPN Route", "plane": "control"},
            {"id": "e4", "from": "fiber-cut-event", "to": "ha-vpn-active", "label": "4. Divert Traffic to IPsec Tunnel", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Link Disruption", "edges": ["e1"], "action": "Physical fiber break interrupts light signal; optical transceivers detect loss of carrier.", "why_traversal": "Hardware sensors trigger immediate BGP protocol withdrawal.", "protocol": "Optical Loss Alert", "plane": "Control Plane"},
            {"n": 2, "title": "BGP Route Withdrawal", "edges": ["e2"], "action": "BGP monitor declares peer dead; Cloud Router withdraws primary route from VPC table.", "why_traversal": "Fast BGP timers prevent routing blackholes during unexpected network breaks.", "protocol": "BGP UPDATE (Withdraw)", "plane": "Control Plane"},
            {"n": 3, "title": "Automated VPN Failover", "edges": ["e3", "e4"], "action": "Traffic automatically diverts to established Cloud HA VPN tunnels without dropped TCP sessions.", "why_traversal": "Continuous active BGP peering over VPN ensures sub-3-second failover convergence.", "protocol": "IPsec Encapsulated TCP", "plane": "Data Plane"}
        ],
        [
            {"id": "vpn-bandwidth-ceiling", "label": "HA VPN Bandwidth Throttling", "changes": {"failedNodes": ["ha-vpn-active"], "failedEdges": ["e4"]}, "root_cause": "10Gbps enterprise workload exceeded single Cloud HA VPN tunnel limit (3Gbps per tunnel).", "diverted_path": "Excess packets dropped; application throughput throttled.", "blast_radius": "High-bandwidth data sync slows down; interactive apps unaffected.", "recovery": "Deploy multiple Cloud HA VPN tunnels with ECMP (Equal-Cost Multi-Path) routing."}
        ]
    )

    # 019: Cloud Storage & Enterprise Filesystems
    specs[19] = make_spec(
        19, "2.7", "Cloud Storage, Object Lifecycle, and Enterprise File Systems",
        "Maps Cloud Storage and Enterprise Filesystems: details storage classes (Standard, Nearline, Coldline, Archive), Autoclass, and Filestore NFS shares.",
        "Cloud Storage provides 99.999999999% (11 9s) annual durability across multi-region geographic redundancy, supporting object lifecycle management and uniform access.",
        [
            {"id": "g-client-ingest", "label": "Client Object Ingestion", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-storage-tiers", "label": "Cloud Storage Classes & Autoclass", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-nfs-mesh", "label": "Filestore NFS & Immutable Governance", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "uploader", "label": "Client Ingestion SDK", "product": "gsutil / GCS API", "group": "g-client-ingest", "plane": "data", "x": 140, "y": 140, "detail": "Uploads multipart media files and transactional ledger documents."},
            {"id": "autoclass-mgr", "label": "Autoclass Engine", "product": "Object Lifecycle Manager", "group": "g-storage-tiers", "plane": "control", "x": 440, "y": 140, "detail": "Monitors access patterns; transitions inactive data to cheaper tiers automatically."},
            {"id": "std-tier", "label": "Standard Storage Tier", "product": "Hot Storage (11 9s Durability)", "group": "g-storage-tiers", "plane": "data", "x": 440, "y": 280, "detail": "Frequent access storage with high IOPS and zero retrieval fees."},
            {"id": "bucket-lock", "label": "Bucket Lock (WORM)", "product": "Retention Policy", "group": "g-nfs-mesh", "plane": "control", "x": 780, "y": 140, "detail": "Immutable compliance lock: prevents deletion or overwrite for 7 years (SEC 17a-4)."},
            {"id": "filestore-nfs", "label": "Filestore Enterprise", "product": "NFSv3 Shared Storage", "group": "g-nfs-mesh", "plane": "data", "x": 780, "y": 280, "detail": "POSIX shared filesystem mounted simultaneously across 50 GKE worker pods."}
        ],
        [
            {"id": "e1", "from": "uploader", "to": "std-tier", "label": "1. Resumable Multipart Upload", "plane": "data"},
            {"id": "e2", "from": "autoclass-mgr", "to": "std-tier", "label": "2. Monitor Read Frequency", "plane": "control"},
            {"id": "e3", "from": "std-tier", "to": "bucket-lock", "label": "3. Apply Retention Lock", "plane": "control"},
            {"id": "e4", "from": "std-tier", "to": "filestore-nfs", "label": "4. Mount NFS File Share", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Multipart Ingestion", "edges": ["e1"], "action": "Client initiates resumable upload; object chunks replicated across multi-region facilities.", "why_traversal": "Multi-region dual-region replication guarantees 11 9s data durability.", "protocol": "HTTPS JSON API", "plane": "Data Plane"},
            {"n": 2, "title": "Automated Tiering", "edges": ["e2"], "action": "Autoclass transitions data untouched for 90 days from Standard to Coldline.", "why_traversal": "Reduces monthly storage cost by 70% without changing application bucket paths.", "protocol": "Autoclass Lifecycle", "plane": "Control Plane"},
            {"n": 3, "title": "WORM Retention Enforcement", "edges": ["e3"], "action": "Bucket Lock policy locks retention period; prevents deletion even by project owners.", "why_traversal": "Guarantees SEC 17a-4 and financial regulatory compliance.", "protocol": "Storage Compliance API", "plane": "Control Plane"}
        ],
        [
            {"id": "retention-block", "label": "Unauthorized Deletion Intercept", "changes": {"failedNodes": ["bucket-lock"], "failedEdges": ["e3"]}, "root_cause": "Rogue administrator script executed gsutil rm -r on compliance bucket.", "diverted_path": "Cloud Storage rejects command with HTTP 403 Retention Policy Locked.", "blast_radius": "Zero data loss; compliance documents preserved.", "recovery": "Bucket Lock cannot be bypassed until retention timestamp expires."}
        ],
        # D2
        "Traces object ingestion and lifecycle tiering: from client upload through Cloud Storage APIs to automated Autoclass transition into Archive cold storage.",
        "Autoclass dynamically monitors object access frequency, moving inactive data to cheaper Coldline/Archive storage without modifying application code.",
        [
            {"id": "g-upload", "label": "Client Ingestion Channel", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-bucket-space", "label": "Cloud Storage Bucket Lifecycle", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-archive-tier", "label": "Archive Cold Storage Substrate", "type": "project", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "client-uploader", "label": "Client Application", "product": "GCS Client SDK", "group": "g-upload", "plane": "data", "x": 140, "y": 140, "detail": "Uploads 100MB PDF document invoices into customer bucket."},
            {"id": "gcs-frontend", "label": "GCS Regional API", "product": "storage.googleapis.com", "group": "g-upload", "plane": "control", "x": 140, "y": 280, "detail": "Validates IAM roles/storage.objectCreator and generates unique object generation ID."},
            {"id": "std-storage", "label": "Day 0-30: Standard Tier", "product": "Frequent Access", "group": "g-bucket-space", "plane": "data", "x": 440, "y": 140, "detail": "Active customer invoice queried frequently during first month ($0.020/GB)."},
            {"id": "coldline-storage", "label": "Day 90: Coldline Tier", "product": "Infrequent Access", "group": "g-bucket-space", "plane": "data", "x": 440, "y": 280, "detail": "Autoclass transitions object to Coldline ($0.007/GB) after 90 days idle."},
            {"id": "archive-storage", "label": "Day 365: Archive Tier", "product": "Cold Archive Storage", "group": "g-archive-tier", "plane": "data", "x": 780, "y": 200, "detail": "Long-term regulatory archival ($0.0012/GB); sub-second read latency retained."}
        ],
        [
            {"id": "e1", "from": "client-uploader", "to": "gcs-frontend", "label": "1. PutObject Request", "plane": "data"},
            {"id": "e2", "from": "gcs-frontend", "to": "std-storage", "label": "2. Store in Standard Class", "plane": "data"},
            {"id": "e3", "from": "std-storage", "to": "coldline-storage", "label": "3. 90-Day Idle Transition", "plane": "control"},
            {"id": "e4", "from": "coldline-storage", "to": "archive-storage", "label": "4. 365-Day Archive Transition", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Initial Hot Storage", "edges": ["e1", "e2"], "action": "Invoice is uploaded to Standard tier; immediately readable by billing web apps.", "why_traversal": "Standard class optimizes frequent read throughput without retrieval fees.", "protocol": "HTTPS REST", "plane": "Data Plane"},
            {"n": 2, "title": "Coldline Tiering", "edges": ["e3"], "action": "Autoclass observes 90 days without access; moves object storage class to Coldline.", "why_traversal": "Saves 65% on storage costs while keeping same bucket and object name.", "protocol": "Autoclass Background Job", "plane": "Control Plane"},
            {"n": 3, "title": "Archive Compliance", "edges": ["e4"], "action": "After 1 year, object transitions to Archive class for 7-year regulatory retention.", "why_traversal": "Achieves lowest possible storage cost ($1.20/TB/month) with sub-second retrieval.", "protocol": "GCS Lifecycle Engine", "plane": "Control Plane"}
        ],
        [
            {"id": "early-deletion-fee", "label": "Coldline Early Deletion Penalty", "changes": {"failedNodes": ["coldline-storage"], "failedEdges": ["e4"]}, "root_cause": "Application deleted Coldline object 15 days after transition (min duration is 90 days).", "diverted_path": "Deletion succeeds, but Google Cloud bills remaining 75 days as early deletion fee.", "blast_radius": "Unplanned operational billing charges.", "recovery": "Use Autoclass instead of manual lifecycle rules to automatically manage deletion windows."}
        ],
        # D3
        "Simulates accidental bucket deletion and ransomware attempt: demonstrates Bucket Lock and Object Versioning preventing unauthorized data destruction.",
        "Object Retention Lock enforces immutable WORM (Write Once, Read Many) compliance, ensuring objects cannot be deleted or overwritten even by project owners.",
        [
            {"id": "g-attack-vector", "label": "Malicious / Accidental Deletion Attempt", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-immutability", "label": "Object Versioning & Retention Lock Shield", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "compromised-admin", "label": "Compromised Admin Key", "product": "Ransomware / Rogue Script", "group": "g-attack-vector", "plane": "control", "x": 220, "y": 140, "detail": "Executes gsutil rm -r -f gs://brightloaf-ledger to destroy corporate books."},
            {"id": "audit-alert-sec", "label": "Cloud Audit Security Alert", "product": "Audit Activity Event", "group": "g-attack-vector", "plane": "control", "x": 220, "y": 280, "detail": "Logs attempted deletion with principal identity and source IP address."},
            {"id": "retention-lock-shield", "label": "Bucket Lock (WORM Shield)", "product": "Locked Retention Policy", "group": "g-immutability", "plane": "control", "x": 700, "y": 140, "detail": "Strictly rejects object deletion attempts until expiration timestamp."},
            {"id": "versioned-history", "label": "Object Versioning Vault", "product": "Non-current Generations", "group": "g-immutability", "plane": "data", "x": 700, "y": 280, "detail": "Preserves immutable historical generations even if live object is overwritten."}
        ],
        [
            {"id": "e1", "from": "compromised-admin", "to": "retention-lock-shield", "label": "1. Attempt Delete Locked Bucket", "plane": "control"},
            {"id": "e2", "from": "retention-lock-shield", "to": "audit-alert-sec", "label": "2. Emit Security Alert & Block", "plane": "control"},
            {"id": "e3", "from": "retention-lock-shield", "to": "versioned-history", "label": "3. Retain Prior Generations", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Destruction Attempt", "edges": ["e1"], "action": "Compromised admin attempts to delete accounting records.", "why_traversal": "Security controls must withstand compromised credentials.", "protocol": "GCS Delete API", "plane": "Control Plane"},
            {"n": 2, "title": "WORM Enforcement", "edges": ["e2"], "action": "Bucket Lock intercepts command; responds HTTP 403 Retention policy prevents deletion.", "why_traversal": "Cryptographic WORM policy cannot be bypassed by project owners or Google support.", "protocol": "HTTP 403 Forbidden", "plane": "Control Plane"},
            {"n": 3, "title": "Version Preservation", "edges": ["e3"], "action": "Object versioning keeps non-current generation intact; data recovery takes seconds.", "why_traversal": "Zero data loss achieved even under full root account takeover.", "protocol": "GCS Versioning Restore", "plane": "Data Plane"}
        ],
        [
            {"id": "lifecycle-delete-conflict", "label": "Lifecycle Rule Overriding Versioning", "changes": {"failedNodes": ["versioned-history"], "failedEdges": ["e3"]}, "root_cause": "Misconfigured lifecycle rule set DeleteNoncurrentVersion after 1 day.", "diverted_path": "Non-current generations purged automatically by lifecycle manager.", "blast_radius": "Historical versions lost before human recovery could occur.", "recovery": "Increase noncurrentDaysRetention to minimum 30 days on compliance buckets."}
        ]
    )

    # 020: Databases: Cloud SQL, Spanner, Firestore, and Bigtable
    specs[20] = make_spec(
        20, "2.8", "Databases: Cloud SQL, Spanner, Firestore, and Bigtable",
        "Maps Google Cloud Database architecture: contrasts Cloud SQL (Regional HA), Cloud Spanner (Global 99.999% Paxos), and Cloud Bigtable (Low-Latency NoSQL).",
        "Relational workloads requiring strict global consistency use Cloud Spanner. Regional enterprise applications use Cloud SQL with synchronous replication.",
        [
            {"id": "g-app-tier", "label": "Application Client Tier", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-relational-db", "label": "Relational Persistence (Cloud SQL & Spanner)", "type": "project", "scope": "regional", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-nosql-db", "label": "High-Throughput NoSQL (Bigtable & Firestore)", "type": "project", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "app-client", "label": "Application Workload", "product": "GKE Microservices", "group": "g-app-tier", "plane": "data", "x": 140, "y": 140, "detail": "Handles customer checkout, inventory updates, and analytical telemetry."},
            {"id": "cloud-sql-ha", "label": "Cloud SQL (Regional HA)", "product": "PostgreSQL / MySQL", "group": "g-relational-db", "plane": "data", "x": 440, "y": 140, "detail": "Primary instance with synchronous persistent disk replication to standby zone."},
            {"id": "cloud-spanner", "label": "Cloud Spanner (Global)", "product": "99.999% Paxos & TrueTime", "group": "g-relational-db", "plane": "data", "x": 440, "y": 280, "detail": "Horizontally scalable relational database with external consistency worldwide."},
            {"id": "cloud-bigtable", "label": "Cloud Bigtable", "product": "Low-Latency NoSQL", "group": "g-nosql-db", "plane": "data", "x": 780, "y": 140, "detail": "Sub-10ms write throughput for millions of IoT sensor events per second."},
            {"id": "firestore", "label": "Cloud Firestore", "product": "Serverless Document NoSQL", "group": "g-nosql-db", "plane": "data", "x": 780, "y": 280, "detail": "Real-time client synchronization and mobile offline data caching."}
        ],
        [
            {"id": "e1", "from": "app-client", "to": "cloud-sql-ha", "label": "1. Regional ACID Transactions", "plane": "data"},
            {"id": "e2", "from": "app-client", "to": "cloud-spanner", "label": "2. Global Multi-Region Writes", "plane": "data"},
            {"id": "e3", "from": "app-client", "to": "cloud-bigtable", "label": "3. Streaming High-Volume Events", "plane": "data"},
            {"id": "e4", "from": "app-client", "to": "firestore", "label": "4. Mobile Profile Document Sync", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Regional ACID Ingestion", "edges": ["e1"], "action": "Orders service executes SQL transaction on Cloud SQL with automatic failover.", "why_traversal": "Cloud SQL delivers standard relational compatibility with minimal operational toil.", "protocol": "PostgreSQL Protocol TCP 5432", "plane": "Data Plane"},
            {"n": 2, "title": "Global Consistency Commit", "edges": ["e2"], "action": "Global inventory reservation commits across continents via Spanner Paxos quorum.", "why_traversal": "TrueTime atomic clocks guarantee external consistency without distributed locking bottlenecks.", "protocol": "Spanner gRPC", "plane": "Data Plane"},
            {"n": 3, "title": "Massive NoSQL Writes", "edges": ["e3"], "action": "Real-time sensor logs stream into Bigtable tablets on Colossus shared storage.", "why_traversal": "Bigtable handles millions of writes per second with sub-10ms response times.", "protocol": "HBase / Bigtable gRPC", "plane": "Data Plane"}
        ],
        [
            {"id": "spanner-hotspot", "label": "Monotonically Increasing Key Hotspotting", "changes": {"failedNodes": ["cloud-spanner"], "failedEdges": ["e2"]}, "root_cause": "Application used sequential timestamp primary key (2026-09-24-001) causing write hotspot.", "diverted_path": "Single Spanner split node saturates to 100% CPU; write latency spikes.", "blast_radius": "All insert operations on that table delayed.", "recovery": "Prepend hash prefix or use UUIDv4 to distribute writes across all cluster nodes."}
        ],
        # D2
        "Traces transactional commit lifecycle in Cloud Spanner: from client write across distributed Paxos consensus leader and TrueTime atomic timestamping.",
        "TrueTime uses atomic clocks and GPS receivers to assign globally consistent timestamps, enabling lock-free distributed read transactions across continents.",
        [
            {"id": "g-client-writer", "label": "Application Client", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-paxos-mesh", "label": "Cloud Spanner Distributed Paxos Quorum", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-truetime-sync", "label": "Google TrueTime Atomic Time Fabric", "type": "project", "scope": "global", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "writer-app", "label": "Spanner Client App", "product": "Spanner SDK", "group": "g-client-writer", "plane": "data", "x": 140, "y": 140, "detail": "Initiates read-write transaction to transfer account balances."},
            {"id": "spanner-frontend", "label": "Spanner API Gateway", "product": "spanner.googleapis.com", "group": "g-client-writer", "plane": "control", "x": 140, "y": 280, "detail": "Routes transaction to the designated Paxos split leader for this keyspace."},
            {"id": "paxos-leader", "label": "Paxos Leader Replica", "product": "Split Leader (Zone A)", "group": "g-paxos-mesh", "plane": "data", "x": 440, "y": 140, "detail": "Acquires lock; coordinates two-phase commit and requests TrueTime commit timestamp."},
            {"id": "paxos-follower", "label": "Paxos Follower Replica", "product": "Split Follower (Zone B)", "group": "g-paxos-mesh", "plane": "data", "x": 440, "y": 280, "detail": "Appends transaction log to Colossus storage; votes to accept commit."},
            {"id": "truetime-engine", "label": "TrueTime Atomic Clock", "product": "GPS & Rubidium Masters", "group": "g-truetime-sync", "plane": "control", "x": 780, "y": 200, "detail": "Guarantees time uncertainty bound (epsilon < 7ms); enforces commit wait."}
        ],
        [
            {"id": "e1", "from": "writer-app", "to": "spanner-frontend", "label": "1. Begin Transaction", "plane": "data"},
            {"id": "e2", "from": "spanner-frontend", "to": "paxos-leader", "label": "2. Route to Split Leader", "plane": "data"},
            {"id": "e3", "from": "paxos-leader", "to": "truetime-engine", "label": "3. Request Commit Timestamp", "plane": "control"},
            {"id": "e4", "from": "paxos-leader", "to": "paxos-follower", "label": "4. Paxos Write Quorum (2 of 3)", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Transaction Routing", "edges": ["e1", "e2"], "action": "Client initiates read-write transaction; SDK routes payload directly to Paxos leader.", "why_traversal": "Direct leader routing minimizes consensus coordination latency.", "protocol": "Spanner gRPC", "plane": "Data Plane"},
            {"n": 2, "title": "TrueTime Timestamp Assignment", "edges": ["e3"], "action": "Paxos leader requests TrueTime timestamp [t.earliest, t.latest] and enforces commit wait.", "why_traversal": "Commit wait guarantees past transactions have strictly lower timestamps than future ones.", "protocol": "TrueTime API", "plane": "Control Plane"},
            {"n": 3, "title": "Paxos Quorum Consensus", "edges": ["e4"], "action": "Leader writes mutation log to majority quorum of replicas before committing.", "why_traversal": "Paxos consensus guarantees data survival even if an entire availability zone disappears.", "protocol": "Paxos Protocol RPC", "plane": "Data Plane"}
        ],
        [
            {"id": "paxos-leader-partition", "label": "Paxos Leader Zone Isolation", "changes": {"failedNodes": ["paxos-leader"], "failedEdges": ["e4"]}, "root_cause": "Network partition isolates Zone A leader from remaining 2 zones.", "diverted_path": "Follower replicas in Zone B and C elect new leader in <3 seconds without data loss.", "blast_radius": "In-flight uncommitted transaction retried by SDK on new leader.", "recovery": "TrueTime and Paxos ensure strict serializability is maintained across failovers."}
        ],
        # D3
        "Simulates Cloud SQL primary zone failure: demonstrates automated health detection, standby promotion, and DNS/IP failover in under 60 seconds.",
        "Cloud SQL Regional HA synchronizes persistent disk writes to a standby zone. When the primary crashes, the standby assumes the primary role automatically.",
        [
            {"id": "g-primary-zone", "label": "Cloud SQL Primary (Zone A)", "type": "vpc", "scope": "zonal", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-standby-zone", "label": "Cloud SQL Standby (Zone B)", "type": "vpc", "scope": "zonal", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "primary-db", "label": "Primary Cloud SQL DB", "product": "Active Master (Zone A)", "group": "g-primary-zone", "plane": "data", "x": 220, "y": 140, "detail": "Serving all read/write queries via private IP 10.0.1.10."},
            {"id": "cloudsql-sentinel", "label": "High-Availability Sentinel", "product": "Control Plane Health Monitor", "group": "g-primary-zone", "plane": "control", "x": 220, "y": 280, "detail": "Heartbeats primary instance every 2s; triggers failover after 30s unresponsive."},
            {"id": "standby-db", "label": "Standby Cloud SQL DB", "product": "Warm Standby (Zone B)", "group": "g-standby-zone", "plane": "data", "x": 700, "y": 140, "detail": "Synchronously replicating block-level disk changes; promoted to Primary in <60s."},
            {"id": "dns-switcher", "label": "Internal Private DNS FQDN", "product": "Private Service Connect / IP", "group": "g-failover", "plane": "control", "x": 700, "y": 280, "detail": "Flips internal IP address pointer to point customer apps directly to Zone B."}
        ],
        [
            {"id": "e1", "from": "cloudsql-sentinel", "to": "primary-db", "label": "1. Heartbeat Probe Timeout", "plane": "control"},
            {"id": "e2", "from": "cloudsql-sentinel", "to": "standby-db", "label": "2. Promote Standby to Primary", "plane": "control"},
            {"id": "e3", "from": "standby-db", "to": "dns-switcher", "label": "3. Switchover Private IP", "plane": "control"},
            {"id": "e4", "from": "primary-db", "to": "standby-db", "label": "4. Synchronous Storage Replication", "plane": "data"}
        ],
        [
            {"n": 1, "title": "Heartbeat Failure", "edges": ["e1"], "action": "Primary database instance in Zone A experiences hardware failure; heartbeats cease.", "why_traversal": "Sentinel detects host failure without requiring operator intervention.", "protocol": "Internal Sentinel Probe", "plane": "Control Plane"},
            {"n": 2, "title": "Standby Promotion", "edges": ["e2"], "action": "Control plane promotes standby instance in Zone B; mounts replicated storage.", "why_traversal": "Synchronous replication guarantees zero data loss (RPO = 0).", "protocol": "Cloud SQL Control API", "plane": "Control Plane"},
            {"n": 3, "title": "DNS & Traffic Convergence", "edges": ["e3"], "action": "Private IP address flips to promoted instance; applications reconnect in <60s.", "why_traversal": "Applications reconnect automatically using standard retry logic (RTO < 60s).", "protocol": "Internal Private DNS", "plane": "Control Plane"}
        ],
        [
            {"id": "split-brain-prevention", "label": "Fencing Stale Primary Instance", "changes": {"failedNodes": ["primary-db"], "failedEdges": ["e1", "e4"]}, "root_cause": "Network partition caused primary to appear dead while still executing queries.", "diverted_path": "Sentinel uses STONITH fencing; forcibly powers off Zone A instance before promoting Zone B.", "blast_radius": "Prevents split-brain data corruption across dual active primaries.", "recovery": "Automatic fencing guarantees absolute data consistency across failovers."}
        ]
    )

    # 021: Messaging and Integration: Pub/Sub, Cloud Tasks, and Eventarc
    specs[21] = make_spec(
        21, "2.9", "Messaging and Integration: Pub/Sub, Cloud Tasks, and Eventarc",
        "Maps Messaging and Integration architecture: details Cloud Pub/Sub at-least-once streaming, Dead-Letter Topics, and Cloud Tasks rate-limiting queues.",
        "Asynchronous messaging decouples producers from consumers. Pub/Sub provides massively scalable broadcast messaging, while Cloud Tasks guarantees rate-controlled dispatch.",
        [
            {"id": "g-producers", "label": "Event Producers & Ingestion", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-pubsub-bus", "label": "Cloud Pub/Sub Asynchronous Message Fabric", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-consumers", "label": "Subscribers & Dead-Letter Isolation", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "order-service", "label": "Order Service Producer", "product": "App Engine / Cloud Run", "group": "g-producers", "plane": "data", "x": 140, "y": 140, "detail": "Publishes order.created event with JSON payload to orders-topic."},
            {"id": "cloud-tasks", "label": "Cloud Tasks Rate Queue", "product": "cloudtasks.googleapis.com", "group": "g-producers", "plane": "control", "x": 140, "y": 280, "detail": "Rate-limits transactional calls to 50 req/sec to protect downstream legacy ERP."},
            {"id": "orders-topic", "label": "Pub/Sub Topic (Multi-Zone)", "product": "Global Pub/Sub Topic", "group": "g-pubsub-bus", "plane": "data", "x": 440, "y": 140, "detail": "Replicates message synchronously across 3 zones before returning publish ACK."},
            {"id": "dlq-topic", "label": "Dead-Letter Topic (DLQ)", "product": "orders-dead-letter", "group": "g-pubsub-bus", "plane": "control", "x": 440, "y": 280, "detail": "Captures poisoned messages after 5 consecutive subscriber processing failures."},
            {"id": "billing-sub", "label": "Billing Worker Subscriber", "product": "Push/Pull Subscription", "group": "g-consumers", "plane": "data", "x": 780, "y": 140, "detail": "Worker fleet pulling messages, processing credit cards, and sending ACK."},
            {"id": "fraud-sub", "label": "Fraud Detection Subscriber", "product": "Broadcast Fanout Sub", "group": "g-consumers", "plane": "data", "x": 780, "y": 280, "detail": "Independent subscriber receiving duplicate stream in parallel without contention."}
        ],
        [
            {"id": "e1", "from": "order-service", "to": "orders-topic", "label": "1. Publish Message (Sync Replicated)", "plane": "data"},
            {"id": "e2", "from": "orders-topic", "to": "billing-sub", "label": "2a. Fanout Subscription A", "plane": "data"},
            {"id": "e3", "from": "orders-topic", "to": "fraud-sub", "label": "2b. Fanout Subscription B", "plane": "data"},
            {"id": "e4", "from": "billing-sub", "to": "dlq-topic", "label": "3. Forward Poison Messages to DLQ", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Synchronous Topic Publication", "edges": ["e1"], "action": "Producer publishes event; Pub/Sub replicates across zones and returns messageID.", "why_traversal": "Multi-zone durability guarantees zero lost messages even if datacenter loses power.", "protocol": "Pub/Sub gRPC", "plane": "Data Plane"},
            {"n": 2, "title": "1-to-Many Fanout", "edges": ["e2", "e3"], "action": "Pub/Sub delivers identical message copies to Billing and Fraud subscriptions.", "why_traversal": "Decoupled fanout allows adding new consumers without modifying producer code.", "protocol": "StreamingPull / HTTP Push", "plane": "Data Plane"},
            {"n": 3, "title": "Dead-Letter Quarantining", "edges": ["e4"], "action": "Unprocessable poisoned message fails 5 times; subscription routes it to DLQ topic.", "why_traversal": "Prevents malformed messages from blocking valid transactions in subscriber queue.", "protocol": "DLQ Auto-Forward", "plane": "Control Plane"}
        ],
        [
            {"id": "subscriber-crash", "label": "Subscriber Backlog Accumulation", "changes": {"failedNodes": ["billing-sub"], "failedEdges": ["e2"]}, "root_cause": "Downstream payment gateway outage causes Billing Worker pods to crash repeatedly.", "diverted_path": "Messages accumulate in Pub/Sub subscription storage (up to 7-day retention).", "blast_radius": "Order confirmation emails delayed; zero message loss.", "recovery": "Deploy additional subscriber worker pods; messages process rapidly once gateway recovers."}
        ],
        # D2
        "Traces event message publishing and consumption: from producer API call across Pub/Sub topic to push/pull subscriber acknowledgment and dead-letter handling.",
        "Pub/Sub replicates messages across multiple zones before acknowledging publish requests, guaranteeing durable delivery even during infrastructure failures.",
        [
            {"id": "g-producer-lane", "label": "Event Ingress Lane", "type": "external", "scope": "external", "x": 30, "y": 30, "width": 240, "height": 360},
            {"id": "g-buffer-lane", "label": "Pub/Sub Ingestion & Storage Buffer", "type": "project", "scope": "global", "x": 300, "y": 30, "width": 310, "height": 360},
            {"id": "g-worker-lane", "label": "StreamingPull Consumer Workers", "type": "vpc", "scope": "regional", "x": 640, "y": 30, "width": 290, "height": 360}
        ],
        [
            {"id": "checkout-api", "label": "Checkout API Service", "product": "Event Publisher", "group": "g-producer-lane", "plane": "data", "x": 140, "y": 140, "detail": "Generates order payload: {order_id: 9942, amount: 45.00}."},
            {"id": "pubsub-frontend", "label": "Pub/Sub Frontend Proxy", "product": "pubsub.googleapis.com", "group": "g-producer-lane", "plane": "control", "x": 140, "y": 280, "detail": "Validates schema definition and authenticates service account token."},
            {"id": "storage-buffer", "label": "Multi-Zone Storage Buffer", "product": "Replicated Log", "group": "g-buffer-lane", "plane": "data", "x": 440, "y": 140, "detail": "Writes message log to SSD across 3 zones; assigns ordering key and ack deadline."},
            {"id": "sub-lease-mgr", "label": "Ack Deadline Manager", "product": "Subscription Lease (60s)", "group": "g-buffer-lane", "plane": "control", "x": 440, "y": 280, "detail": "Monitors unacknowledged messages; redelivers if worker fails to ack within 60s."},
            {"id": "worker-pull", "label": "GKE Worker (Pull Client)", "product": "Subscriber Daemon", "group": "g-worker-lane", "plane": "data", "x": 780, "y": 200, "detail": "Receives message via persistent StreamingPull connection; executes database commit."}
        ],
        [
            {"id": "e1", "from": "checkout-api", "to": "pubsub-frontend", "label": "1. Publish Request", "plane": "data"},
            {"id": "e2", "from": "pubsub-frontend", "to": "storage-buffer", "label": "2. Write 3-Zone Storage", "plane": "data"},
            {"id": "e3", "from": "storage-buffer", "to": "worker-pull", "label": "3. Dispatch via StreamingPull", "plane": "data"},
            {"id": "e4", "from": "worker-pull", "to": "sub-lease-mgr", "label": "4. Return Acknowledge (ACK)", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Publish and Durability", "edges": ["e1", "e2"], "action": "Publisher sends message; Pub/Sub commits to multi-zone storage before sending 200 OK.", "why_traversal": "Synchronous replication ensures no message loss even under catastrophic host failure.", "protocol": "Pub/Sub gRPC", "plane": "Data Plane"},
            {"n": 2, "title": "StreamingPull Dispatch", "edges": ["e3"], "action": "Pub/Sub pushes message over open bidirectional gRPC stream to GKE worker.", "why_traversal": "StreamingPull minimizes delivery latency compared to polling.", "protocol": "HTTP/2 Bidirectional gRPC", "plane": "Data Plane"},
            {"n": 3, "title": "Acknowledgment Commitment", "edges": ["e4"], "action": "Worker completes database write and sends ACK; Pub/Sub removes message from queue.", "why_traversal": "At-least-once delivery guarantees every event is processed to completion.", "protocol": "Acknowledge RPC", "plane": "Control Plane"}
        ],
        [
            {"id": "duplicate-delivery", "label": "At-Least-Once Duplicate Message Delivery", "changes": {"failedNodes": ["sub-lease-mgr"], "failedEdges": ["e4"]}, "root_cause": "Worker took 65 seconds to process; ack deadline expired at 60 seconds.", "diverted_path": "Pub/Sub redelivers message to secondary worker; worker must enforce idempotency.", "blast_radius": "Duplicate processing risk if database insert is not idempotent.", "recovery": "Use unique transaction ID as database primary key; use modifyAckDeadline to extend lease."}
        ],
        # D3
        "Simulates downstream consumer crash: demonstrates unacknowledged message backpressure, exponential retry backoff, and dead-letter topic routing.",
        "When worker consumers fail repeatedly, Pub/Sub forwards unprocessable messages to a Dead-Letter Topic after 5 failed attempts, preserving queue flow.",
        [
            {"id": "g-failing-consumer", "label": "Crashing Consumer Worker", "type": "vpc", "scope": "regional", "x": 30, "y": 30, "width": 420, "height": 360},
            {"id": "g-dlq-recovery", "label": "Dead-Letter Queue Isolation & Alerting", "type": "project", "scope": "global", "x": 480, "y": 30, "width": 440, "height": 360}
        ],
        [
            {"id": "poison-msg", "label": "Poison Pill Message", "product": "Malformed JSON Payload", "group": "g-failing-consumer", "plane": "data", "x": 220, "y": 140, "detail": "Contains corrupted schema causing worker JSON parser to throw fatal panic."},
            {"id": "crashing-worker", "label": "Crashing Worker Pod", "product": "CrashLoopBackOff", "group": "g-failing-consumer", "plane": "data", "x": 220, "y": 280, "detail": "Crashes on receipt; fails to acknowledge message across 5 retry attempts."},
            {"id": "dlq-router", "label": "Pub/Sub DLQ Router", "product": "maxDeliveryAttempts = 5", "group": "g-dlq-recovery", "plane": "control", "x": 700, "y": 140, "detail": "Detects 5th delivery failure; automatically forwards poison pill to Dead-Letter Topic."},
            {"id": "quarantine-bucket", "label": "DLQ Storage & SecOps Alert", "product": "Cloud Monitoring / GCS", "group": "g-dlq-recovery", "plane": "control", "x": 700, "y": 280, "detail": "Alerts on-call engineers; saves malformed payload for post-mortem analysis."}
        ],
        [
            {"id": "e1", "from": "poison-msg", "to": "crashing-worker", "label": "1. Dispatch Corrupt Message", "plane": "data"},
            {"id": "e2", "from": "crashing-worker", "to": "dlq-router", "label": "2. Consecutive NACK / Timeout (5x)", "plane": "control"},
            {"id": "e3", "from": "dlq-router", "to": "quarantine-bucket", "label": "3. Forward to Dead-Letter Topic", "plane": "control"}
        ],
        [
            {"n": 1, "title": "Poison Pill Ingestion", "edges": ["e1"], "action": "Worker receives corrupted message; throws unhandled null pointer exception and crashes.", "why_traversal": "Malformed client payloads must not cause systemic queue blockage.", "protocol": "StreamingPull", "plane": "Data Plane"},
            {"n": 2, "title": "Exponential Retry Backoff", "edges": ["e2"], "action": "Pub/Sub applies exponential retry backoff (10s, 20s, 40s); records 5 failed deliveries.", "why_traversal": "Backoff gives transient downstream dependencies time to self-heal.", "protocol": "Pub/Sub Retry Policy", "plane": "Control Plane"},
            {"n": 3, "title": "Quarantine and Unblock", "edges": ["e3"], "action": "Pub/Sub moves poison message to DLQ topic and ACKs main subscription.", "why_traversal": "Unblocks remaining valid queue messages, restoring production processing flow.", "protocol": "DLQ Routing Event", "plane": "Control Plane"}
        ],
        [
            {"id": "dlq-subscription-missing", "label": "Dead-Letter Topic Lacks Attached Subscription", "changes": {"failedNodes": ["quarantine-bucket"], "failedEdges": ["e3"]}, "root_cause": "Dead-letter topic was created without any subscription attached to retain messages.", "diverted_path": "Poison messages routed to DLQ topic are permanently lost without retention.", "blast_radius": "Inability to analyze and replay failed messages.", "recovery": "Attach pull subscription to DLQ topic; stream events into BigQuery error audit table."}
        ]
    )

    return specs
