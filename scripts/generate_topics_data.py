#!/usr/bin/env python3
"""
generate_topics_data.py - Generates Topic 002 to Topic 021 (Phase 0, Phase 1, Phase 2)
Adheres strictly to the 4-part template, Depth Ladder, and Kubernetes Apartment Style Lock.
"""

import sys
import os

import json

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_website import build_topic_page, DIAGRAMS_DIR

def get_phase0_topics():
    topics = []
    
    # Topic 002: Linux and Command Line
    with open(os.path.join(DIAGRAMS_DIR, "topic-002-d1.json")) as f:
        t002_d1 = json.load(f)
    with open(os.path.join(DIAGRAMS_DIR, "topic-002-d2.json")) as f:
        t002_d2 = json.load(f)
    with open(os.path.join(DIAGRAMS_DIR, "topic-002-d3.json")) as f:
        t002_d3 = json.load(f)

    topics.append({
        "topic_no": "002",
        "roadmap_id": "0.2",
        "title": "Linux and Command Line for Cloud Architects",
        "page_type": "concept",
        "phase": "Phase 0 — Prerequisites",
        "lead": "Mastering the POSIX foundation: file permissions, systemd service supervision, journalctl log inspection, SSH bastion tunnels, and jq JSON parsing for gcloud CLI operations.",
        "d1": t002_d1,
        "d2": t002_d2,
        "d3": t002_d3,
        "analogy": {
            "topic_no": "002",
            "roadmap_id": "0.2",
            "title": "Cloud City Operating Regulations & Inspection Crews",
            "city_concept": "Building Codes, Service Permits, and Registry Ledgers",
            "beats": [
                {
                    "step": 1,
                    "name": "The City Problem",
                    "story": "Brightloaf Bakery's kitchen equipment was running unmonitored. Ovens overheated without warning, unmanaged delivery carts cluttered the fire exits, and nobody kept an official record of building keys.",
                    "analogy_elements": ["Unsupervised Ovens (Unmanaged Processes)", "Lost Building Keys (SSH Sprawl)"]
                },
                {
                    "step": 2,
                    "name": "The City Solution",
                    "story": "Ola the Operator introduced building superintendent guidelines (systemd). All engines are catalogued, fire permits are verified via digital visitor badges (OS Login), and fuel consumption is strictly metered (cgroups).",
                    "analogy_elements": ["Superintendent Office (systemd)", "Building Ledgers (journalctl)", "Electronic Badge Reader (IAP / OS Login)"]
                },
                {
                    "step": 3,
                    "name": "The City Under Stress",
                    "story": "During a flash pastry sale, delivery orders swamped the mailroom. The room hit its maximum parcel capacity (ulimit open file descriptors) and new letters were dropped at the doorstep until Superintendent Ola expanded the intake ceiling.",
                    "analogy_elements": ["Overfilled Mailroom (Too many open files)", "Expanded Mail Slots (ulimit -n 65535)"]
                },
                {
                    "step": 4,
                    "name": "Where the Metaphor Breaks",
                    "story": "In a physical city, if a basement fills up with flour bags, you can stack them into the hallway. In Linux filesystems, if the Inode Table is full, creating a single zero-byte text file is strictly rejected by physics, regardless of empty disk gigabytes.",
                    "analogy_elements": ["Rigid Inode Capacity Ceiling"]
                }
            ]
        },
        "part1_html": """
        <h3>The Situation: Command Line Mastery Under Fire</h3>
        <p>
          At <strong>Brightloaf Bakery</strong>, the flagship e-commerce ordering engine suddenly stopped accepting order transactions at 2:00 AM on a Saturday. The web UI dashboard was unresponsive. The on-call engineer attempted to SSH into the host machine, only to be rejected with permission denied errors. When they finally accessed the console, typing commands hung because log output had completely frozen the shell. Without foundational Linux and shell debugging skills, diagnosing whether the failure stemmed from network dropouts, memory exhaustion, or disk quota failure was impossible.
        </p>

        <div class="callout danger">
          <div class="callout-title">The Pain: Why Senior Architects Must Master Linux Primitives</div>
          Cloud infrastructure is ultimately managed POSIX software:
          <ul>
            <li><strong>The Bastion Antipattern:</strong> Exposing port 22 directly to public IP addresses results in automated brute-force attacks and compliance violations. Modern cloud design uses Identity-Aware Proxy (IAP) TCP forwarding.</li>
            <li><strong>Process Supervision Gaps:</strong> Running production apps with background <code>nohup</code> commands rather than managed <code>systemd</code> units means crashes remain unhealed and logs are lost.</li>
            <li><strong>Unparsed CLI Output:</strong> Manually reading 500-line JSON outputs from <code>gcloud</code> instead of querying fields with <code>jq</code> or <code>--format</code> leads to human error during critical production rollouts.</li>
          </ul>
        </div>

        <h3>Core Vocabulary</h3>
        <ul>
          <li><code>systemd / systemctl</code>: Linux init system and service manager responsible for bootstrapping user space and supervising daemons.</li>
          <li><code>journalctl</code>: Centralized log query tool parsing binary systemd logs with exact time, unit, and priority filtering.</li>
          <li><code>ulimit</code>: Shell built-in controlling per-process resource allocations (maximum open file descriptors, max processes, virtual memory).</li>
          <li><code>jq</code>: Lightweight, high-performance command-line JSON processor essential for scripting gcloud API payloads.</li>
        </ul>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Processes, Filesystems & Permissions (The Execution Substrate)</h4>
        <p>
          <strong>Architectural Role & Significance:</strong> Layer 1 establishes the baseline security boundary and resource primitives of the host. In Linux, the unifying abstraction is that <em>"everything is a file descriptor"</em>—including regular disk files, network sockets, anonymous pipes, hardware block devices, and UNIX domain sockets.
        </p>
        <p>
          Permissions are governed by the POSIX 9-bit permission mask (<code>rwxrwxrwx</code>) distributed across three scopes: User (Owner), Group, and Other (World). In enterprise cloud environments:
        </p>
        <ul>
          <li><strong>Least-Privilege Process Execution:</strong> Production daemons must never execute as <code>root</code> (UID 0). A container or service breakout running as root has complete write access to the host kernel memory space and raw block devices. Layer 1 mandates dedicated service accounts (e.g. <code>appuser:appuser</code>, UID/GID 1001).</li>
          <li><strong>Immutable Substrate Filesystems:</strong> Cloud instances mount virtual persistent disks formatted as <code>ext4</code> or <code>XFS</code>. Modern cloud architectures configure root filesystems with <code>nodev</code>, <code>nosuid</code>, and mount sensitive application directories with strict <code>0750</code> or <code>0640</code> permissions, ensuring private keys and configuration secrets cannot be read across tenant boundaries.</li>
          <li><strong>Socket & Descriptor Inheritance:</strong> When an application opens thousands of incoming client connections, each is a file descriptor in the kernel's file table. Understanding Layer 1 invariants prevents socket leaks and permission escalation vulnerabilities before higher-level services are layered on top.</li>
        </ul>

        <h4>Layer 2 — Practitioner: Service Supervision, Declarative Lifecycles & Log Telemetry</h4>
        <p>
          <strong>Architectural Role & Significance:</strong> Moving from ad-hoc operational commands (e.g. running <code>nohup python server.py &</code>) to production-grade, declarative process supervision. Layer 2 is the operational contract between the application and the host operating system.
        </p>
        <p>
          In modern Linux distributions across Google Cloud (Debian, Ubuntu, Rocky Linux, COS), process supervision is governed by <strong>systemd (PID 1)</strong>. A declared unit file (e.g., <code>/etc/systemd/system/brightloaf.service</code>) defines the complete operational contract:
        </p>
        <pre><code>[Unit]
Description=Brightloaf Order Processing Service
Documentation=https://docs.brightloaf.internal/orders
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=appuser
Group=appuser
WorkingDirectory=/opt/brightloaf
ExecStart=/usr/bin/node /opt/brightloaf/server.js
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5s
KillMode=mixed
TimeoutStopSec=30s

# Resource Quotas & File Descriptor Ceilings
LimitNOFILE=65535
MemoryMax=2G
CPUQuota=150%

# Security Sandboxing
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target</code></pre>
        <p>
          <strong>Why this matters for Defense-in-Depth:</strong>
        </p>
        <ul>
          <li><strong>Deterministic Crash Recovery:</strong> <code>Restart=always</code> with <code>RestartSec=5s</code> prevents transient memory spikes or uncaught exceptions from causing permanent cluster outages.</li>
          <li><strong>Hard Resource Bounding:</strong> <code>MemoryMax=2G</code> and <code>CPUQuota=150%</code> enforce Linux kernel <code>cgroups v2</code> constraints, ensuring a memory leak in one service cannot starve critical system daemons (like <code>sshd</code> or <code>google-guest-agent</code>).</li>
          <li><strong>Structured Binary Telemetry:</strong> All <code>stdout</code> and <code>stderr</code> streams are captured by <code>systemd-journald</code> with microsecond timestamps and process metadata. Practitioners inspect logs deterministically via <code>journalctl -u brightloaf.service --since "15 min ago" -p err --no-pager</code> without maintaining custom log scrapers.</li>
        </ul>

        <h4>Layer 3 — Architect: Modern Secure Access Without Public IPs (Zero-Trust Cloud Fabric)</h4>
        <p>
          <strong>Architectural Role & Significance:</strong> Elevating from single-node Linux administration to enterprise distributed cloud boundaries. The architect designs network perimeters that completely eliminate exposure to the public internet while preserving frictionless operational access.
        </p>
        <p>
          The legacy enterprise pattern relied on <strong>SSH Bastion Jump Hosts</strong> with public IP addresses sitting in a DMZ. This pattern is fundamentally broken in modern cloud architecture:
        </p>
        <ul>
          <li>Bastions introduce a concentrated, internet-facing attack surface vulnerable to zero-day OpenSSH exploits and automated credential brute-forcing.</li>
          <li>Static SSH private keys on engineer laptops are frequently leaked, forgotten, or never rotated.</li>
          <li>Maintaining bastion host patch cycles, HA failovers, and ingress firewall whitelists incurs heavy operational toil.</li>
        </ul>
        <p>
          <strong>The Google Cloud Zero-Trust Architectural Standard: IAP TCP Forwarding + OS Login</strong>
        </p>
        <p>
          Google Cloud eliminates bastion jump hosts entirely by unifying identity, software-defined networking, and OS authentication:
        </p>
        <ol>
          <li><strong>Zero Public IPs (Complete Perimeter Isolation):</strong> Compute Engine instances live exclusively within private VPC subnets with RFC 1918 internal IP addresses (e.g. <code>10.128.0.0/20</code>). They possess no external IP addresses and cannot be scanned from the internet.</li>
          <li><strong>Edge-Terminated TLS Authentication:</strong> Administrative traffic never connects directly to port 22 over the internet. When an engineer executes <code>gcloud compute ssh &lt;instance&gt; --tunnel-through-iap</code>, the CLI opens an encrypted TLS 1.3 WebSocket tunnel to Google Cloud's globally distributed Edge Proxies on port 443. Google evaluates Identity and Access Management (IAM) permissions (<code>roles/iap.tunnelResourceAccessor</code>) and Context-Aware Access policies (device health, IP geolocation) at the perimeter.</li>
          <li><strong>Andromeda SDN Microsegmentation:</strong> Only if edge IAM authorization succeeds does Google Cloud's Andromeda SDN forward the encapsulated TCP packets into the private VPC on port 22. VPC firewall rules enforce this by allowing ingress port 22 <em>strictly from Google's IAP netblock: <code>35.235.240.0/20</code></em>.</li>
          <li><strong>OS Login Dynamic PAM Federation:</strong> Inside the Linux VM, the <code>/lib/security/pam_oslogin.so</code> module intercepts the SSH handshake. Instead of consulting a static local <code>~/.ssh/authorized_keys</code> file, PAM queries the Google Cloud Instance Metadata Server (<code>http://metadata.google.internal/computeMetadata/v1/oslogin/users</code>), dynamically resolving the caller's Cloud Identity, POSIX UID/GID, and short-lived public keys. When an employee leaves the company, revoking their IAM role instantly cuts off SSH access to every VM across the enterprise within seconds.</li>
        </ol>

        <h4>Layer 4 — Staff / Principal: System Limits, Chaos Horizons & Blast Radius Containment</h4>
        <p>
          <strong>Architectural Role & Significance:</strong> Understanding the catastrophic failure horizons where operating system abstractions shatter under extreme load. A Staff Architect designs systems with the mathematical awareness of kernel ceilings, filesystem structures, and cascading blast radii.
        </p>
        <div class="callout warning">
          <div class="callout-title">Enterprise Failure-Mode Table: Linux Kernel & Subsystem Limits</div>
          <table>
            <thead>
              <tr>
                <th>Failure Phenomenon</th>
                <th>Root Cause & Syscall Mechanism</th>
                <th>Blast Radius</th>
                <th>Immediate Triage Action</th>
                <th>Durable Architectural Prevention</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>EMFILE (File Descriptor Saturation)</strong></td>
                <td>Process opens more sockets/files than permitted by <code>ulimit -n</code>. Kernel syscall <code>accept4()</code> or <code>socket()</code> fails with <code>errno 24 (Too many open files)</code>. Incoming connections stall.</td>
                <td>Single application daemon or reverse proxy. Upstream load balancers register 502 Bad Gateway and failover.</td>
                <td>Elevate limits dynamically without restarting process: <br><code>prlimit --pid=&lt;pid&gt; --nofile=65536:65536</code></td>
                <td>Declare <code>LimitNOFILE=65535</code> in the systemd unit file; verify system-wide ceilings via <code>sysctl fs.file-max</code>.</td>
              </tr>
              <tr>
                <td><strong>100% Inode Exhaustion (Silent Disk Lock)</strong></td>
                <td>Millions of zero-byte or micro error logs consume all pointers in the filesystem inode table. <code>df -h</code> shows gigabytes of free disk space, but <code>open(..., O_CREAT)</code> returns <code>ENOSPC</code>. Filesystem locks read-only.</td>
                <td>Entire Compute Engine instance. Database transactions halt, Docker daemon cannot spawn containers, and monitoring agents crash.</td>
                <td>Find directory hoarding inodes: <br><code>find / -xdev -printf '%h\\n' | sort | uniq -c | sort -k 1 -n | tail -n 20</code>; purge stale caches.</td>
                <td>Deploy automated <code>logrotate</code> with strict size-based rotation (<code>maxsize 50M</code>); mount separate dedicated persistent disks for <code>/var/log</code> and data paths.</td>
              </tr>
              <tr>
                <td><strong>Kernel OOM Killer (Exit 137 SIGKILL)</strong></td>
                <td>Total physical RAM + swap is exhausted. Linux kernel <code>mm/oom_kill.c</code> calculates <code>oom_badness()</code> score and sends uncatchable <code>SIGKILL</code> to the process consuming the most memory.</td>
                <td>Primary application process terminated instantly. In-flight transactions dropped; state unpersisted.</td>
                <td>Inspect kernel ring buffer: <br><code>dmesg -T | grep -i 'killed process'</code>; restart unit and configure emergency temporary swapfile.</td>
                <td>Set explicit runtime heap boundaries (e.g. JVM <code>-Xmx</code>, Node.js <code>--max-old-space-size</code>); configure systemd <code>MemoryMax</code> with 20% headroom below VM machine type RAM.</td>
              </tr>
            </tbody>
          </table>
        </div>
        """,
        "part3_narrative_html": """
        <p>
          In <strong>Cloud City</strong>, building superintending is governed by strict municipal charters. Ola the Operator ensures no rogue boilers run without a licensed engineer, and gate passes are validated electronically at the perimeter checkpoint.
        </p>
        """,
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Practice Exercise: Troubleshooting a Failing Daemon via CLI</div>
          <p>
            You are tasked with diagnosing a private Compute Engine VM hosting an API service that has fallen out of load balancer health checks.
          </p>
          <ol>
            <li>Construct the exact <code>gcloud compute ssh</code> command using IAP tunneling without a public IP.</li>
            <li>Write the single-line <code>journalctl</code> command to view logs from unit <code>api.service</code> emitted in the last 15 minutes filtered for error priority.</li>
            <li>Write a <code>jq</code> query that parses the output of <code>gcloud compute instances list --format=json</code> to return only the instance names and internal IP addresses where status is <code>RUNNING</code>.</li>
          </ol>
        </div>

        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">
          👁 Show Solution & Rubric
        </button>

        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Worked Solution</h4>
          <p><strong>1. IAP SSH Command:</strong></p>
          <pre><code>gcloud compute ssh api-backend-vm --zone=us-west1-b --tunnel-through-iap</code></pre>
          <p><strong>2. Filtered journalctl command:</strong></p>
          <pre><code>journalctl -u api.service --since "15 minutes ago" -p err..emerg --no-pager</code></pre>
          <p><strong>3. jq filter query:</strong></p>
          <pre><code>gcloud compute instances list --format=json | jq -r '.[] | select(.status=="RUNNING") | {name: .name, internal_ip: .networkInterfaces[0].networkIP}'</code></pre>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Recall (Question 1)</span>
          <p><strong>Which command correctly displays filesystem disk space usage alongside inode utilization?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! df -h shows human-readable space, and df -i shows inode count and usage percentage.')">A) df -h && df -i</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'du displays disk usage by directory, not total filesystem inode allocations.')">B) du -sh *</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'lsblk lists block devices, not filesystem inode metadata.')">C) lsblk -f</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'fdisk manages partition tables.')">D) fdisk -l</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>

        <div class="quiz-card">
          <span class="quiz-badge">Band: Application (Question 2)</span>
          <p><strong>To allow DevOps engineers to SSH into private Compute Engine VMs using Identity-Aware Proxy (IAP) without external IP addresses, what ingress firewall rule must be configured?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! 35.235.240.0/20 is the dedicated Google IP range reserved for IAP TCP forwarding.')">A) Ingress allow TCP:22 from source range 35.235.240.0/20</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, '0.0.0.0/0 exposes the port to the public internet, violating the private security model.')">B) Ingress allow TCP:22 from 0.0.0.0/0</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, '10.0.0.0/8 only allows internal RFC 1918 traffic from within the VPC, not from Google IAP edge proxy.')">C) Ingress allow TCP:22 from 10.0.0.0/8</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, '169.254.169.254 is the instance metadata server.')">D) Ingress allow TCP:22 from 169.254.169.254/32</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": """
        <ul>
          <li><strong>IAP Documentation:</strong> <a href="https://cloud.google.com/iap/docs/using-tcp-forwarding" target="_blank">TCP Forwarding with Cloud IAP</a> (Verifies 35.235.240.0/20 firewall requirement).</li>
          <li><strong>OS Login:</strong> <a href="https://cloud.google.com/compute/docs/oslogin" target="_blank">Managing Instance Access with OS Login</a> (Verifies IAM-linked SSH key synchronization).</li>
          <li><strong>gcloud CLI Syntax:</strong> <a href="https://cloud.google.com/sdk/gcloud/reference/topic/filters" target="_blank">gcloud Filtering and Formatting Guide</a>.</li>
        </ul>
        """
    })
    
    # Topic 003: Virtualization and Containers
    topics.append({
        "topic_no": "003",
        "roadmap_id": "0.3",
        "title": "Virtualization and Containers: From Hypervisors to Kubernetes",
        "page_type": "concept",
        "phase": "Phase 0 — Prerequisites",
        "lead": "Understanding the isolation boundary: Type-1/Type-2 hypervisors, Linux cgroups & namespaces, container image layers, and foundational Kubernetes runtime objects.",
        "d1": {
            "id": "topic-003-d1",
            "title": "Virtual Machines vs Container Isolation Architecture",
            "topic_no": "003",
            "roadmap_id": "0.3",
            "kind": "map",
            "groups": [
                {"id": "g-vm", "label": "Hardware Virtualization (VM)", "type": "project", "scope": "project", "x": 30, "y": 40, "width": 410, "height": 340},
                {"id": "g-ctr", "label": "OS-Level Virtualization (Container)", "type": "vpc", "scope": "regional", "x": 480, "y": 40, "width": 410, "height": 340}
            ],
            "nodes": [
                {"id": "hyper", "label": "Host Hypervisor (KVM)", "product": "Virtualization", "group": "g-vm", "plane": "data", "x": 140, "y": 280, "detail": "Emulates physical hardware; runs full separate guest operating system kernels."},
                {"id": "guest-os", "label": "Guest OS & Kernel", "product": "Virtual OS", "group": "g-vm", "plane": "data", "x": 140, "y": 140, "detail": "Heavyweight memory footprint, minutes to boot, separate security boundary."},
                {"id": "shared-kern", "label": "Shared Host Linux Kernel", "product": "Linux Kernel", "group": "g-ctr", "plane": "data", "x": 580, "y": 280, "detail": "Single shared kernel managing cgroups, namespaces, and security seccomp profiles."},
                {"id": "app-sandbox", "label": "Container Sandbox (CRI)", "product": "containerd / runc", "group": "g-ctr", "plane": "data", "x": 760, "y": 140, "detail": "Lightweight process isolated by PID, mount, and network namespaces. Boots in milliseconds."}
            ],
            "edges": [
                {"id": "e-vm-boot", "from": "hyper", "to": "guest-os", "label": "Hardware Emulation", "plane": "data"},
                {"id": "e-ctr-cgroup", "from": "shared-kern", "to": "app-sandbox", "label": "Namespace Isolation", "plane": "data"}
            ],
            "steps": [
                {
                    "n": 1,
                    "edges": ["e-vm-boot"],
                    "narration": "VM Architecture: Hypervisor allocates dedicated virtual CPUs and RAM blocks, executing a discrete guest OS kernel.",
                    "check": {"commands": "virsh list || dmesg | grep -i kvm", "metrics": "compute.googleapis.com/instance/cpu/utilization"}
                },
                {
                    "n": 2,
                    "edges": ["e-ctr-cgroup"],
                    "narration": "Container Architecture: Container engine leverages host Linux kernel cgroups and namespaces to isolate processes without guest OS overhead.",
                    "check": {"commands": "crictl ps || docker ps", "logs": "containerd: starting container process"}
                }
            ],
            "scenarios": [
                {
                    "id": "kernel-panic",
                    "label": "Host Kernel Panic Impact",
                    "changes": {"failedNodes": ["shared-kern", "app-sandbox"]},
                    "narration": "A kernel crash on the host takes down all colocated containers instantly. In VMs, a guest kernel panic is isolated strictly to that individual VM.",
                    "check": {"command": "uptime", "metric": "NodeNotReady condition in Kubernetes"}
                }
            ]
        },
        "d2": {
            "id": "topic-003-d2",
            "title": "OCI Container Image Layer Union Filesystem",
            "topic_no": "003",
            "roadmap_id": "0.3",
            "kind": "flow",
            "groups": [
                {"id": "g-ro", "label": "Immutable Read-Only Image Layers", "type": "project", "scope": "global", "x": 30, "y": 40, "width": 460, "height": 340},
                {"id": "g-rw", "label": "Ephemeral Runtime Layer", "type": "vpc", "scope": "zonal", "x": 520, "y": 40, "width": 370, "height": 340}
            ],
            "nodes": [
                {"id": "base-layer", "label": "Base OS Layer (Debian)", "product": "Layer sha256:1a", "group": "g-ro", "plane": "data", "x": 160, "y": 140, "detail": "Underlying root filesystem libraries and package binaries."},
                {"id": "runtime-layer", "label": "Node.js / Python Runtime", "product": "Layer sha256:2b", "group": "g-ro", "plane": "data", "x": 360, "y": 140, "detail": "Language interpreter and global dependencies."},
                {"id": "app-code", "label": "App Source Code Layer", "product": "Layer sha256:3c", "group": "g-ro", "plane": "data", "x": 360, "y": 280, "detail": "Compiled application code and configuration files."},
                {"id": "rw-overlay", "label": "Container Read-Write Overlay", "product": "OverlayFS Diff", "group": "g-rw", "plane": "data", "x": 700, "y": 200, "detail": "Copy-on-write transient filesystem layer. Destroyed when container stops."}
            ],
            "edges": [
                {"id": "e-b1", "from": "base-layer", "to": "runtime-layer", "label": "1. Layer Build", "plane": "data"},
                {"id": "e-b2", "from": "runtime-layer", "to": "app-code", "label": "2. Layer Build", "plane": "data"},
                {"id": "e-union", "from": "app-code", "to": "rw-overlay", "label": "3. Union Mount (OverlayFS)", "plane": "data"}
            ],
            "steps": [
                {
                    "n": 1,
                    "edges": ["e-b1", "e-b2"],
                    "narration": "Image build step: Dockerfile instructions create content-addressable SHA256 layers cached across multiple microservices.",
                    "check": {"commands": "docker history &lt;image-id&gt;", "logs": "Artifact Registry: image pushed"}
                },
                {
                    "n": 2,
                    "edges": ["e-union"],
                    "narration": "Runtime execution: OverlayFS unions read-only image layers under a thin mutable read-write layer.",
                    "check": {"commands": "mount | grep overlay", "metrics": "container/disk/write_bytes_count"}
                }
            ],
            "scenarios": [
                {
                    "id": "ephemeral-loss",
                    "label": "State Written to Container RW Layer Lost",
                    "changes": {"failedNodes": ["rw-overlay"]},
                    "narration": "Application wrote user uploads directly to container filesystem instead of a PersistentVolume or Cloud Storage bucket. Container restarts; data vanishes.",
                    "check": {"command": "ls /data", "metric": "Customer uploads 404 count spikes"}
                }
            ]
        },
        "d3": {
            "id": "topic-003-d3",
            "title": "Kubernetes Pod Lifecycle & Failure States",
            "topic_no": "003",
            "roadmap_id": "0.3",
            "kind": "failure",
            "groups": [
                {"id": "g-cp", "label": "K8s Control Plane", "type": "project", "scope": "project", "x": 30, "y": 40, "width": 380, "height": 340},
                {"id": "g-node", "label": "Worker Node (Kubelet)", "type": "vpc", "scope": "regional", "x": 450, "y": 40, "width": 440, "height": 340}
            ],
            "nodes": [
                {"id": "apiserver", "label": "kube-apiserver", "product": "Control Plane", "group": "g-cp", "plane": "control", "x": 140, "y": 140, "detail": "Validates and persists Pod manifest state in etcd."},
                {"id": "sched", "label": "kube-scheduler", "product": "Control Plane", "group": "g-cp", "plane": "control", "x": 310, "y": 140, "detail": "Assigns unscheduled Pod to a healthy worker node."},
                {"id": "kubelet", "label": "kubelet Daemon", "product": "Worker Agent", "group": "g-node", "plane": "control", "x": 580, "y": 140, "detail": "Communicates with CRI to pull image and run containers."},
                {"id": "pod-status", "label": "Pod: CrashLoopBackOff", "product": "Pod Workload", "group": "g-node", "plane": "data", "x": 760, "y": 280, "detail": "Container repeatedly crashes immediately after startup. Backoff delay increases exponentially."}
            ],
            "edges": [
                {"id": "e-sch", "from": "apiserver", "to": "sched", "label": "Watch Unbound Pods", "plane": "control"},
                {"id": "e-bind", "from": "sched", "to": "kubelet", "label": "Assign Node Binding", "plane": "control"},
                {"id": "e-crash", "from": "kubelet", "to": "pod-status", "label": "Container Exit != 0", "plane": "data"}
            ],
            "steps": [
                {
                    "n": 1,
                    "edges": ["e-sch", "e-bind"],
                    "narration": "Normal schedule: API server accepts Pod spec, scheduler selects Node, kubelet triggers container start.",
                    "check": {"commands": "kubectl get pods -o wide", "logs": "Scheduled pod to node-pool-1"}
                },
                {
                    "n": 2,
                    "edges": ["e-crash"],
                    "narration": "Failure Trigger: Application throws unhandled runtime exception or missing environment variable; container exits immediately.",
                    "check": {"commands": "kubectl logs &lt;pod-name&gt; --previous", "logs": "Fatal error: missing DATABASE_URL"}
                }
            ],
            "scenarios": [
                {
                    "id": "image-pull-backoff",
                    "label": "ImagePullBackOff (Registry Auth Failure)",
                    "changes": {"failedNodes": ["kubelet", "pod-status"]},
                    "narration": "Node service account lacks 'roles/artifactregistry.reader' or image tag does not exist. Kubelet fails image pull.",
                    "check": {"command": "kubectl describe pod &lt;pod&gt;", "metric": "Failed to pull image: 403 Forbidden"}
                }
            ]
        },
        "analogy": {
            "topic_no": "003",
            "roadmap_id": "0.3",
            "title": "Cloud City Construction: Freestanding Estates vs Shared High-Rise Apartments",
            "city_concept": "Estates with Private Utilities vs High-Rise Units with Shared Plumbing",
            "beats": [
                {
                    "step": 1,
                    "name": "The City Problem",
                    "story": "Brightloaf Bakery was buying an entire detached estate with its own dedicated power generator, water well, and security guard for every single baker (Virtual Machines). Costs soared, and building a new estate took 20 minutes.",
                    "analogy_elements": ["Detached Mansions (VMs)", "Private Power Plant (Guest Kernel)"]
                },
                {
                    "step": 2,
                    "name": "The City Solution",
                    "story": "Mayor Meridian constructed a modular high-rise apartment complex (Containers / Kubernetes). Bakers rent individual private apartments (Namespaces) sharing central city water and power mains (Shared Linux Kernel). New rooms furnish in seconds.",
                    "analogy_elements": ["Apartment Complex (Container Host)", "Modular Apartments (Pods)", "Shared Plumbing (Host Kernel)"]
                },
                {
                    "step": 3,
                    "name": "The City Under Stress",
                    "story": "One reckless baker left their commercial dough mixer running at full throttle, threatening to brown out the entire building. Superintendent Ola clamped a municipal circuit breaker (cgroup CPU/memory limit) on that specific apartment.",
                    "analogy_elements": ["Power Surge (CPU Spike)", "Circuit Breaker (cgroups)"]
                },
                {
                    "step": 4,
                    "name": "Where the Metaphor Breaks",
                    "story": "In an apartment building, a catastrophic foundation crack can compromise all tenants simultaneously. Because containers share one host kernel, an unpatched kernel privilege escalation allows an attacker to break out of a container onto the host machine.",
                    "analogy_elements": ["Shared Kernel Security Boundary"]
                }
            ]
        },
        "part1_html": """
        <h3>The Situation: Scaling From Monolithic VMs to Container Fleets</h3>
        <p>
          As <strong>Brightloaf Bakery</strong> introduced online seasonal ordering, spinning up full Compute Engine virtual machines took 3 to 5 minutes per instance. During sudden traffic spikes, demand overwhelmed the existing servers before new instances could complete boot sequences. Furthermore, engineers suffered from <em>"it worked on my laptop"</em> syndrome, as differing local Python versions broke production deployments. By containerizing workloads using Docker OCI standards and preparing for Google Kubernetes Engine (GKE), Brightloaf reduced deployment spin-up times to sub-second windows with bit-for-bit environment parity.
        </p>

        <div class="callout">
          <div class="callout-title">The Mental Model: VM vs Container Isolation</div>
          <ul>
            <li><strong>Virtual Machines:</strong> Virtualize the underlying hardware. Each VM runs a full guest operating system, kernel, and system services. Strongest security boundary, but heavy footprint.</li>
            <li><strong>Containers:</strong> Virtualize the operating system. Each container is a group of host processes isolated by Linux kernel primitives (cgroups and namespaces). Extremely fast and lightweight, but sharing the host kernel.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Linux Namespaces and Control Groups</h4>
        <p>
          Containers are not hardware emulations; they are standard Linux processes running with restricted views:
        </p>
        <ul>
          <li><strong>PID Namespace:</strong> Isolates process IDs; the container process believes it is PID 1.</li>
          <li><strong>Net Namespace:</strong> Provides an independent virtual network interface, routing table, and port bindings.</li>
          <li><strong>Mount Namespace:</strong> Presents a private filesystem mount tree based on union container layers.</li>
          <li><strong>cgroups (Control Groups):</strong> Enforces strict CPU, memory, IO, and network bandwidth quotas.</li>
        </ul>

        <h4>Layer 2 — Practitioner: Multi-Stage Container Image Hygiene</h4>
        <p>
          Never package build compilers, package managers, or SDKs into production container images. Use multi-stage Docker builds with Google Distroless base images:
        </p>
        <pre><code># Build Stage
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

# Production Distroless Stage
FROM gcr.io/distroless/nodejs20-debian12
WORKDIR /app
COPY --from=build /app /app
USER nonroot:nonroot
EXPOSE 8080
CMD ["server.js"]</code></pre>

        <h4>Layer 3 — Architect: Container Sandboxing & Security Boundaries</h4>
        <p>
          Because containers share the host Linux kernel, multi-tenant untrusted code requires hardened isolation:
        </p>
        <ul>
          <li><strong>GKE Sandbox (gVisor):</strong> Implements a user-space kernel that intercepts and filters application system calls, preventing host kernel exploits.</li>
          <li><strong>Compute Engine Confidential VMs:</strong> Employs AMD SEV memory encryption to protect data in memory from hypervisor inspection.</li>
        </ul>

        <h4>Layer 4 — Staff: Pod Crash Triage & Recovery</h4>
        <div class="callout warning">
          <div class="callout-title">Container Failure-Mode Table</div>
          <table>
            <thead>
              <tr>
                <th>Failure State</th>
                <th>Signal</th>
                <th>Root Cause</th>
                <th>Staff Remediation</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>CrashLoopBackOff</strong></td>
                <td>Restart count increments; exit code 1 or 137.</td>
                <td>Application crash, missing secret/config, or OOM kill.</td>
                <td>Inspect <code>kubectl logs -p &lt;pod&gt;</code> and <code>kubectl describe pod</code> events.</td>
              </tr>
              <tr>
                <td><strong>ImagePullBackOff</strong></td>
                <td>Pod stuck in Waiting state.</td>
                <td>403 Forbidden or typo in image tag/registry URI.</td>
                <td>Verify node service account IAM role <code>roles/artifactregistry.reader</code>.</td>
              </tr>
              <tr>
                <td><strong>CreateContainerConfigError</strong></td>
                <td>Pod cannot transition to Running.</td>
                <td>Referenced ConfigMap or Secret does not exist.</td>
                <td>Verify Secret Manager synchronization and namespace scoping.</td>
              </tr>
            </tbody>
          </table>
        </div>
        """,
        "part3_narrative_html": """
        <p>
          The Cloud City high-rise apartments provide shared, efficient municipal services while granting Bea the Baker private suites for each recipe engine.
        </p>
        """,
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Designing a Kubernetes Pod Manifest with Liveness Probes</div>
          <p>
            Write a production Kubernetes Pod specification for the <code>brightloaf-order-service</code> satisfying these constraints:
          </p>
          <ul>
            <li>Image: <code>us-docker.pkg.dev/brightloaf-prod/apps/orders:v1.2.0</code></li>
            <li>Runs as non-root user (UID 10001) with a read-only root filesystem.</li>
            <li>Enforces resource requests (250m CPU, 256Mi memory) and limits (500m CPU, 512Mi memory).</li>
            <li>Configures an HTTP liveness probe on path <code>/healthz</code>, port 8080, with a 5-second timeout.</li>
          </ul>
        </div>

        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">
          👁 Show Solution & Rubric
        </button>

        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Worked Solution</h4>
          <pre><code>apiVersion: v1
kind: Pod
metadata:
  name: brightloaf-order-service
  labels:
    app.kubernetes.io/name: orders
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 10001
  containers:
  - name: order-api
    image: us-docker.pkg.dev/brightloaf-prod/apps/orders:v1.2.0
    securityContext:
      readOnlyRootFilesystem: true
      allowPrivilegeEscalation: false
    resources:
      requests:
        cpu: "250m"
        memory: "256Mi"
      limits:
        cpu: "500m"
        memory: "512Mi"
    livenessProbe:
      httpGet:
        path: /healthz
        port: 8080
      initialDelaySeconds: 10
      periodSeconds: 10
      timeoutSeconds: 5
      failureThreshold: 3</code></pre>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Application (Question 1)</span>
          <p><strong>A container in a Kubernetes Pod crashes with Exit Code 137. What was the cause of termination?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Exit 137 indicates 128 + 9 (SIGKILL), typically triggered by the Linux kernel OOM killer or Kubernetes container memory limit exhaustion.')">A) Out Of Memory (OOM) killed by the Linux kernel cgroup limit.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Graceful SIGTERM is exit code 143 (128 + 15).')">B) Graceful SIGTERM shutdown initiated by rolling update.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Exit code 1 indicates general application runtime exception.')">C) Unhandled application syntax error.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Failed health check triggers kubelet SIGTERM followed by SIGKILL, but OOM specifically yields exit 137 directly.')">D) Readiness probe timeout.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": """
        <ul>
          <li><strong>GKE Hardening Guide:</strong> <a href="https://cloud.google.com/kubernetes-engine/docs/how-to/hardening-your-cluster" target="_blank">Google Cloud GKE Cluster Hardening</a>.</li>
          <li><strong>GKE Sandbox (gVisor):</strong> <a href="https://cloud.google.com/kubernetes-engine/docs/concepts/sandbox-pods" target="_blank">Sandbox Pods with gVisor</a>.</li>
          <li><strong>OCI Specifications:</strong> <a href="https://opencontainers.org/" target="_blank">Open Container Initiative Image Spec</a>.</li>
        </ul>
        """
    })

    return topics

if __name__ == '__main__':
    p0 = get_phase0_topics()
    for t in p0:
        build_topic_page(t)
    print(f"Generated {len(p0)} topics successfully.")
