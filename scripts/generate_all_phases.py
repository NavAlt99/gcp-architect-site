#!/usr/bin/env python3
"""
generate_all_phases.py - Programmatic generation for Roadmap Phases
Generates complete topics with D1-D3 diagrams, analogy scenes, quizzes, and demos.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_website import build_topic_page

def create_phase_topics():
    topics = []

    # -------------------------------------------------------------
    # Topic 004: Cloud Concepts
    # -------------------------------------------------------------
    topics.append({
        "topic_no": "004",
        "roadmap_id": "0.4",
        "title": "Cloud Concepts & Operating Models",
        "page_type": "concept",
        "phase": "Phase 0 — Prerequisites",
        "lead": "IaaS vs PaaS vs FaaS service boundaries, Google Cloud shared responsibility matrix, horizontal vs vertical scalability, and stateless vs stateful design principles.",
        "d1": {
            "id": "topic-004-d1",
            "title": "Cloud Service Models & Shared Responsibility",
            "topic_no": "004",
            "roadmap_id": "0.4",
            "kind": "map",
            "groups": [
                {"id": "g-cust", "label": "Customer Responsibility", "type": "project", "scope": "project", "x": 30, "y": 40, "width": 410, "height": 340},
                {"id": "g-goog", "label": "Google Cloud Responsibility", "type": "vpc", "scope": "global", "x": 480, "y": 40, "width": 410, "height": 340}
            ],
            "nodes": [
                {"id": "iam-data", "label": "IAM, Data & Content", "product": "Customer Domain", "group": "g-cust", "plane": "control", "x": 150, "y": 140, "detail": "Access management, dataset classification, customer encryption keys, network security rules."},
                {"id": "app-code", "label": "Application Code", "product": "Customer Domain", "group": "g-cust", "plane": "data", "x": 310, "y": 140, "detail": "Container binaries, code vulnerabilities, library dependencies, application logic."},
                {"id": "os-patch", "label": "OS & Runtime (IaaS/PaaS)", "product": "Shared Boundary", "group": "g-cust", "plane": "data", "x": 230, "y": 280, "detail": "Guest OS patches (Customer on GCE; Google on Cloud Run / Cloud Functions / GKE Autopilot)."},
                {"id": "infra", "label": "Physical Datacenter & Fiber", "product": "Google Domain", "group": "g-goog", "plane": "data", "x": 590, "y": 140, "detail": "B4 backbone fiber, Titan security chips, physical campus biometric security, hardware disposal."},
                {"id": "hyper-sdn", "label": "Hypervisor & Andromeda SDN", "product": "Google Domain", "group": "g-goog", "plane": "data", "x": 750, "y": 200, "detail": "Software-defined networking, hypervisor patching, physical disk encryption by default."}
            ],
            "edges": [
                {"id": "e-resp1", "from": "iam-data", "to": "app-code", "label": "Authorize Execution", "plane": "control"},
                {"id": "e-resp2", "from": "app-code", "to": "os-patch", "label": "Runtime Dependency", "plane": "data"},
                {"id": "e-resp3", "from": "os-patch", "to": "infra", "label": "Execute on Google Infra", "plane": "data"}
            ],
            "steps": [
                {
                    "n": 1,
                    "edges": ["e-resp1", "e-resp2"],
                    "narration": "Customer defines access control policies and uploads application code into the project.",
                    "check": {"commands": "gcloud projects get-iam-policy $PROJECT_ID", "logs": "Audit logs for IAM policy changes"}
                },
                {
                    "n": 2,
                    "edges": ["e-resp3"],
                    "narration": "Google Cloud infrastructure executes workload over validated physical fiber and custom security hardware.",
                    "check": {"commands": "gcloud compute instances describe vm-1 --zone=us-central1-a", "metrics": "instance/uptime"}
                }
            ],
            "scenarios": [
                {
                    "id": "breach-misconfig",
                    "label": "Public Cloud Storage Data Leak (Customer Error)",
                    "changes": {"failedNodes": ["iam-data"]},
                    "narration": "Customer grants 'allUsers' the 'roles/storage.objectViewer' role. Data is leaked; Google's physical security remains 100% intact, but customer boundary failed.",
                    "check": {"command": "gcloud storage buckets get-iam-policy gs://customer-bucket", "metric": "Public bucket policy alert in Security Command Center"}
                }
            ]
        },
        "d2": {
            "id": "topic-004-d2",
            "title": "Elastic Auto-Scaling: Horizontal vs Vertical",
            "topic_no": "004",
            "roadmap_id": "0.4",
            "kind": "flow",
            "groups": [
                {"id": "g-lb", "label": "Global Ingress Traffic", "type": "external", "scope": "global", "x": 30, "y": 40, "width": 260, "height": 340},
                {"id": "g-scale", "label": "Compute Fleet (Managed Instance Group)", "type": "vpc", "scope": "regional", "x": 320, "y": 40, "width": 570, "height": 340}
            ],
            "nodes": [
                {"id": "traffic-spk", "label": "Traffic Surge (10x QPS)", "product": "External Users", "group": "g-lb", "plane": "data", "x": 160, "y": 140, "detail": "Black Friday customer spike pouring into External HTTPS Load Balancer."},
                {"id": "lb-node", "label": "Cloud Load Balancing", "product": "L7 Anycast LB", "group": "g-lb", "plane": "data", "x": 160, "y": 280, "detail": "Monitors backend instance utilization and triggers autoscaling signal."},
                {"id": "vm1", "label": "Instance A (Zone A)", "product": "Compute Engine", "group": "g-scale", "plane": "data", "x": 480, "y": 140, "detail": "CPU utilization reaches 85% (threshold is 60%)."},
                {"id": "vm2", "label": "Instance B (Zone B)", "product": "Compute Engine", "group": "g-scale", "plane": "data", "x": 680, "y": 140, "detail": "MIG autoscaler provisions new instance horizontally in under 60 seconds."},
                {"id": "vm3", "label": "Instance C (Zone C)", "product": "Compute Engine", "group": "g-scale", "plane": "data", "x": 680, "y": 280, "detail": "Evenly distributes capacity across all three availability zones."}
            ],
            "edges": [
                {"id": "e-trf", "from": "traffic-spk", "to": "lb-node", "label": "1. HTTPS Requests", "plane": "data"},
                {"id": "e-sat", "from": "lb-node", "to": "vm1", "label": "2. High CPU Saturation", "plane": "data"},
                {"id": "e-scale-out", "from": "vm1", "to": "vm2", "label": "3. Autoscaler Triggers +1 VM", "plane": "control"},
                {"id": "e-balance", "from": "lb-node", "to": "vm3", "label": "4. Distribute Traffic Evenly", "plane": "data"}
            ],
            "steps": [
                {
                    "n": 1,
                    "edges": ["e-trf", "e-sat"],
                    "narration": "Step 1: Traffic surges. Existing VM CPU exceeds autoscaler target threshold (60%).",
                    "check": {"commands": "gcloud compute instance-groups managed list", "metrics": "compute.googleapis.com/instance_group/size"}
                },
                {
                    "n": 2,
                    "edges": ["e-scale-out", "e-balance"],
                    "narration": "Step 2: Regional MIG provisions instances in Zone B and C, spreading load without downtime.",
                    "check": {"commands": "gcloud compute instance-groups managed list-instances mig-web", "logs": "Autoscaler: scaled up by 2 instances"}
                }
            ],
            "scenarios": [
                {
                    "id": "quota-lock",
                    "label": "Regional vCPU Quota Exhaustion",
                    "changes": {"failedNodes": ["vm3"]},
                    "narration": "Project vCPU quota limit reached. MIG cannot spin up Instance C; existing VMs saturate at 100% CPU, increasing HTTP 503 errors.",
                    "check": {"command": "gcloud compute project-info describe --project=$PROJECT", "metric": "compute.googleapis.com/quota/allocation_exceeded"}
                }
            ]
        },
        "d3": {
            "id": "topic-004-d3",
            "title": "Stateless vs Stateful Application Failure Modes",
            "topic_no": "004",
            "roadmap_id": "0.4",
            "kind": "failure",
            "groups": [
                {"id": "g-stateless", "label": "Stateless Tier (Cloud Run / MIG)", "type": "project", "scope": "regional", "x": 30, "y": 40, "width": 410, "height": 340},
                {"id": "g-stateful", "label": "Stateful Tier (Database / Storage)", "type": "vpc", "scope": "regional", "x": 480, "y": 40, "width": 410, "height": 340}
            ],
            "nodes": [
                {"id": "app1", "label": "Web Instance (Stateless)", "product": "Compute Engine", "group": "g-stateless", "plane": "data", "x": 160, "y": 140, "detail": "Stores no local sessions or uploads. Can be terminated at any second."},
                {"id": "app2", "label": "Replacement Instance", "product": "Compute Engine", "group": "g-stateless", "plane": "data", "x": 160, "y": 280, "detail": "Autohealed instantly; takes over traffic seamlessly."},
                {"id": "bad-db", "label": "Monolithic Local DB", "product": "PostgreSQL on Root Disk", "group": "g-stateful", "plane": "data", "x": 680, "y": 140, "detail": "Stores database state on non-replicated local filesystem."},
                {"id": "cloud-sql", "label": "Cloud SQL HA Standby", "product": "Cloud SQL", "group": "g-stateful", "plane": "data", "x": 680, "y": 280, "detail": "Synchronous regional replication with automated sub-minute failover."}
            ],
            "edges": [
                {"id": "e-crash-heal", "from": "app1", "to": "app2", "label": "Instance Dies -> Autoheal", "plane": "control"},
                {"id": "e-fail-state", "from": "app1", "to": "bad-db", "label": "Write to Local Storage", "plane": "data"},
                {"id": "e-safe-state", "from": "app2", "to": "cloud-sql", "label": "Externalized State", "plane": "data"}
            ],
            "steps": [
                {
                    "n": 1,
                    "edges": ["e-fail-state"],
                    "narration": "Antipattern: Web application writes customer session tokens and uploaded images directly to local VM disk.",
                    "check": {"commands": "ls -l /var/www/uploads", "logs": "Session stored locally in /tmp"}
                },
                {
                    "n": 2,
                    "edges": ["e-crash-heal", "e-safe-state"],
                    "narration": "Cloud-Native Architecture: VM state is externalized to Cloud SQL and Cloud Storage. Any VM can crash without data loss.",
                    "check": {"commands": "gcloud sql instances describe prod-db", "metrics": "cloudsql.googleapis.com/database/state"}
                }
            ],
            "scenarios": [
                {
                    "id": "zonal-blackout",
                    "label": "Zone us-central1-a Complete Outage",
                    "changes": {"failedNodes": ["app1", "bad-db"]},
                    "narration": "Datacenter zone loses power. Stateless nodes seamlessly regenerate in Zone B; local database suffers total downtime until zone recovers.",
                    "check": {"command": "gcloud compute instances list", "metric": "Zone outage status alert"}
                }
            ]
        },
        "analogy": {
            "topic_no": "004",
            "roadmap_id": "0.4",
            "title": "Cloud City Utilities & Civic Responsibility Agreements",
            "city_concept": "Municipal Water Grid vs Tenant Fixtures",
            "beats": [
                {
                    "step": 1,
                    "name": "The City Problem",
                    "story": "Brightloaf Bakery was confused about who fixes what. When a faucet broke inside Bea's bakery kitchen, she blamed Mayor Meridian. When the city reservoir pipeline burst, Bea tried digging up the street with a kitchen spoon.",
                    "analogy_elements": ["Broken Kitchen Faucet", "Burst City Water Main"]
                },
                {
                    "step": 2,
                    "name": "The City Solution",
                    "story": "Mayor Meridian published the Civic Charter (Shared Responsibility Matrix). The City guarantees pristine pressurized water to the building meter (Google Cloud Infrastructure). Bea is responsible for the kitchen pipes, interior faucets, and turning off taps before leaving (Customer Domain).",
                    "analogy_elements": ["Civic Water Meter (Service Boundary)", "City Aqueduct (Google Backbone)"]
                },
                {
                    "step": 3,
                    "name": "The City Under Stress",
                    "story": "During a city festival, Bea needed 10x more baking ovens. Instead of buying a mammoth single oven that took 6 months to forge (Vertical Scale), Bea rented 10 modular bakery booths that opened within minutes (Horizontal Elasticity).",
                    "analogy_elements": ["Mammoth Oven (Scale Up)", "Fleet of Modular Kiosks (Scale Out)"]
                },
                {
                    "step": 4,
                    "name": "Where the Metaphor Breaks",
                    "story": "In a physical city, if a tenant leaves their storefront door wide open, physical locks and neighbors might deter burglary. In Cloud Storage, leaving an object permission set to 'allUsers' immediately indexes private files to every automated crawler on earth within seconds.",
                    "analogy_elements": ["Public Bucket Misconfiguration"]
                }
            ]
        },
        "part1_html": """
        <h3>The Situation: The Foundation of Cloud Architecture</h3>
        <p>
          When <strong>Brightloaf Bakery</strong> moved to Google Cloud, management initially treated cloud infrastructure like a leased corporate datacenter. They bought giant oversized virtual machines (scaling vertically), manually scheduled weekly backups, and expected Google support to patch their WordPress PHP vulnerabilities. When their database instance ran out of disk space, the site crashed. They realized they were paying cloud prices while inheriting legacy datacenter fragility.
        </p>

        <div class="callout">
          <div class="callout-title">The Three Foundational Cloud Truths</div>
          <ul>
            <li><strong>Everything Fails All the Time:</strong> Design systems assuming VMs will be preempted, zones will fail, and network packets will drop. Build autohealing into every tier.</li>
            <li><strong>Scale Out, Not Up:</strong> Horizontal elasticity (adding small identical compute units) provides higher availability and lower cost than buying massive multi-core single instances.</li>
            <li><strong>Externalize State:</strong> Stateless application layers can scale to zero or surge to thousands of instances instantaneously. Keep state in durable, managed data stores (Cloud SQL, Spanner, Cloud Storage).</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Service Models (IaaS, PaaS, FaaS, SaaS)</h4>
        <table>
          <thead>
            <tr>
              <th>Model</th>
              <th>GCP Services</th>
              <th>What Customer Manages</th>
              <th>What Google Manages</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>IaaS (Infrastructure as a Service)</strong></td>
              <td>Compute Engine, VPC, Persistent Disk</td>
              <td>OS patching, security updates, firewall rules, middleware, application code.</td>
              <td>Physical hardware, hypervisor, datacenter cooling, power, physical networking.</td>
            </tr>
            <tr>
              <td><strong>PaaS (Platform as a Service)</strong></td>
              <td>App Engine, Cloud SQL, GKE Autopilot</td>
              <td>Application code, database schema, data access policies.</td>
              <td>OS provisioning, kernel updates, database engine patching, high availability failover.</td>
            </tr>
            <tr>
              <td><strong>FaaS / Serverless</strong></td>
              <td>Cloud Run, Cloud Run functions</td>
              <td>Container image or function code, trigger bindings.</td>
              <td>Zero-to-N autoscaling, routing, concurrency multiplexing, container sandbox.</td>
            </tr>
          </tbody>
        </table>

        <h4>Layer 2 — Practitioner: The Shared Responsibility Security Matrix</h4>
        <p>
          Google secures the cloud; the customer secures what they put <em>in</em> the cloud. Customer is always 100% responsible for:
        </p>
        <ul>
          <li>IAM roles, service account keys, and credential rotation.</li>
          <li>Data classification, bucket access controls (avoiding <code>allUsers</code>).</li>
          <li>VPC network topologies, private subnets, and firewall allow/deny rules.</li>
          <li>Application code dependencies and software supply chain vulnerabilities.</li>
        </ul>

        <h4>Layer 3 — Architect: Availability Zones & Regions Selection</h4>
        <p>
          A Google Cloud <strong>Region</strong> is an independent geographic area with at least three <strong>Zones</strong> separated by kilometers to prevent correlated physical disaster while maintaining sub-millisecond inter-zone latency.
        </p>
        <ul>
          <li><strong>Zonal Resource:</strong> Compute Engine instance, zonal Persistent Disk (fails if zone fails).</li>
          <li><strong>Regional Resource:</strong> Regional MIG, Cloud SQL HA, Cloud Storage regional bucket (survives single zone loss).</li>
          <li><strong>Multi-Regional / Global Resource:</strong> Global External ALB, Cloud Spanner, Cloud Storage multi-region, Cloud DNS (survives entire region loss).</li>
        </ul>

        <h4>Layer 4 — Staff: Disaster Recovery RTO & RPO Engineering</h4>
        <div class="callout warning">
          <div class="callout-title">SLA & Failure Impact Table</div>
          <table>
            <thead>
              <tr>
                <th>Scope Failure</th>
                <th>Blast Radius</th>
                <th>Architectural Mitigation</th>
                <th>SLA Objective</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Instance Crash</strong></td>
                <td>Single VM running application</td>
                <td>Managed Instance Group (MIG) with Autohealing health checks.</td>
                <td>99.9% single VM with SSD.</td>
              </tr>
              <tr>
                <td><strong>Zonal Datacenter Loss</strong></td>
                <td>All instances & disks in zone us-central1-a</td>
                <td>Regional MIG spread across 3 zones + Regional Persistent Disks.</td>
                <td>99.99% across zones in region.</td>
              </tr>
              <tr>
                <td><strong>Regional Fiber Sever / Natural Disaster</strong></td>
                <td>Entire region us-east1 offline</td>
                <td>Multi-region Cloud Spanner + Global ALB with cross-region failover.</td>
                <td>99.999% global multi-region.</td>
              </tr>
            </tbody>
          </table>
        </div>
        """,
        "part3_narrative_html": """
        <p>
          Cloud City's municipal code separates the city's power grid from Bea's bakery ovens, ensuring that Bea can swap a broken mixer without interrupting city water supplies.
        </p>
        """,
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Calculating Composite Availability SLA</div>
          <p>
            Brightloaf Bakery designs an e-commerce checkout architecture with three sequential dependencies:
          </p>
          <ol>
            <li>Global External HTTPS Load Balancer: <strong>99.99% SLA</strong></li>
            <li>Compute Engine Regional MIG in us-west1: <strong>99.95% SLA</strong></li>
            <li>Cloud SQL PostgreSQL Single-Instance (Non-HA): <strong>99.90% SLA</strong></li>
          </ol>
          <p><strong>Tasks:</strong></p>
          <ul>
            <li>Calculate the composite end-to-end SLA for the system (Formula: SLA_total = SLA_1 * SLA_2 * SLA_3).</li>
            <li>Convert the resulting SLA into maximum allowed downtime per month (30 days = 43,200 minutes).</li>
            <li>State the single architectural change required to raise the database availability to 99.95%.</li>
          </ul>
        </div>

        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">
          👁 Show Solution & Rubric
        </button>

        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Worked Solution</h4>
          <p><strong>1. Composite SLA Calculation:</strong></p>
          <pre><code>SLA_total = 0.9999 * 0.9995 * 0.9990 = 0.9984004995 -> 99.84%</code></pre>
          <p><strong>2. Maximum Allowed Downtime:</strong></p>
          <pre><code>Allowed Downtime = (1 - 0.9984) * 43,200 minutes = 0.0016 * 43,200 = 69.12 minutes/month</code></pre>
          <p><strong>3. Required Architecture Upgrade:</strong> Upgrade Cloud SQL from Single-Instance to <strong>Regional High Availability (HA)</strong> with synchronous standby in a second zone. This raises the database SLA from 99.90% to 99.95%.</p>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: PCA Scenario (Question 1)</span>
          <p><strong>You are architecting a mission-critical billing API for a retail enterprise. The business requires 99.99% monthly availability, zero data loss in the event of an entire datacenter zone outage, and an RTO under 1 minute. How should you design the compute and database layers?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Regional MIGs distribute stateless compute across 3 zones with autohealing, and Cloud SQL Regional HA maintains synchronous replication to a standby in a second zone with automated sub-minute failover.')">A) Regional Managed Instance Group across 3 zones behind an Application Load Balancer with Cloud SQL in Regional HA configuration.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Incorrect: Zonal MIG will fail completely if that single zone suffers an outage.')">B) Zonal Managed Instance Group with nightly automated database backups.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Incorrect: Single VM cannot meet 99.99% SLA or survive zonal loss.')">C) Single large E2-standard-32 VM with local SSD for maximum read/write performance.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Incorrect: Asynchronous read replicas do not provide automatic failover and risk data loss under sudden zonal crash.')">D) Two Compute Engine instances in Zone A connecting to Cloud SQL with an asynchronous read replica in Zone B.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": """
        <ul>
          <li><strong>Architecture Framework:</strong> <a href="https://cloud.google.com/architecture/framework/reliability" target="_blank">Google Cloud Reliability Pillar</a>.</li>
          <li><strong>Shared Responsibility:</strong> <a href="https://cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate" target="_blank">Shared Responsibility & Shared Fate on GCP</a>.</li>
          <li><strong>SLA Summary:</strong> <a href="https://cloud.google.com/terms/sla" target="_blank">Google Cloud Service Level Agreements Directory</a>.</li>
        </ul>
        """
    })

    return topics

if __name__ == '__main__':
    all_t = create_phase_topics()
    for t in all_t:
        build_topic_page(t)
    print(f"Generated {len(all_t)} additional topics.")
