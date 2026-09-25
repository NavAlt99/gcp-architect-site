#!/usr/bin/env python3
"""
generate_all_phase_topics.py - Generates Topics 005 to 021 covering Phase 0, Phase 1, and Phase 2.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_website import build_topic_page
from batch_generate_full import make_d1_map, make_d2_flow, make_d3_failure, make_analogy

TOPICS_DEFINITIONS = [
    # 005: Software & Delivery Basics
    {
        "topic_no": "005",
        "roadmap_id": "0.5",
        "title": "Software Architecture & Delivery Basics",
        "page_type": "concept",
        "phase": "Phase 0 — Prerequisites",
        "lead": "Git trunk-based workflows, RESTful API design, 12-factor cloud-native principles, and Monolith vs Microservices vs Serverless architectural transitions.",
        "comp1": ("Git Repository", "Cloud Source / GitHub", "control", "Source of truth for version control, tags, and commits."),
        "comp2": ("CI/CD Build Runner", "Cloud Build", "control", "Executes unit tests, static linting, and container compilation."),
        "comp3": ("Artifact Registry", "Container Registry", "data", "Stores immutable cryptographically signed Docker images."),
        "comp4": ("Deployment Controller", "Cloud Deploy", "control", "Coordinates rolling canaries across dev, staging, and production environments."),
        "flow1": "Developer merges Pull Request into main branch, triggering automated webhook.",
        "flow2": "Cloud Build compiles container image and signs provenance with Binary Authorization attestation.",
        "flow3": "Cloud Deploy promotes release to production GKE cluster with automated canary analysis.",
        "fail": "Pipeline executes deployment with broken database schema migration.",
        "heal": "Cloud Deploy initiates automated 1-click rollback to prior stable container release target.",
        "city_concept": "City Construction Blueprints & Inspection Crews",
        "p1": "Brightloaf Bakery was deploying new store signs and recipes without blueprints. Half the stores served raw bread while others used expired yeast.",
        "p2": "Kit the Builder introduced standardized city blueprints (Git & 12-Factor principles). Every recipe is versioned and inspected before rollout.",
        "p3": "During a city festival, an experimental pastry recipe caused kitchen fires. Inspector Ines triggered an automated fire rollback protocol.",
        "p4": "In software, rollbacks take seconds; in physical construction, tearing down a crooked skyscraper takes months.",
        "part1_html": """
        <h3>The Situation: The 12-Factor Foundation</h3>
        <p>
          At <strong>Brightloaf Bakery</strong>, the engineering team kept hard-coding database passwords into application files, writing logs directly to local VM disks, and building giant monolithic deployments where a CSS bug in the blog crashed the payment gateway. By adopting the <strong>12-Factor App methodology</strong> and decoupling services into microservices, they gained independent deployment velocity, horizontal elasticity, and clean configuration management across environments.
        </p>
        <div class="callout">
          <div class="callout-title">Key 12-Factor Principles for Cloud Architects</div>
          <ul>
            <li><strong>Config in the Environment:</strong> Store database credentials and API endpoints in environment variables or Secret Manager, never in code.</li>
            <li><strong>Treat Logs as Event Streams:</strong> Write logs to <code>stdout</code>/<code>stderr</code>; let the cloud agent (Cloud Logging) aggregate and route them.</li>
            <li><strong>Stateless Processes:</strong> Execute apps as stateless processes; externalize state to Cloud SQL, Firestore, or Cloud Storage.</li>
            <li><strong>Disposability:</strong> Maximize robustness with fast startup and graceful shutdown handling SIGTERM signals.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Monolith vs Microservices vs Serverless</h4>
        <p>Monoliths bundle all capabilities into one deployable unit. Microservices split services by domain boundaries (DDD). Serverless offloads scaling and infrastructure management entirely.</p>
        <h4>Layer 2 — Practitioner: REST, gRPC & API Contracts</h4>
        <p>Internal high-performance microservices communicate via binary <strong>gRPC over HTTP/2</strong> with Protocol Buffers, while external web clients consume JSON RESTful APIs.</p>
        <h4>Layer 3 — Architect: Strangler Fig Migration Pattern</h4>
        <p>Never attempt a "big bang" rewrite. Route traffic through an API gateway and incrementally strangle monolithic features into serverless microservices one route at a time.</p>
        <h4>Layer 4 — Staff: DORA Metrics & Continuous Verification</h4>
        <p>Staff architects optimize the 4 DORA metrics: Deployment Frequency, Lead Time for Changes, Mean Time to Recovery (MTTR), and Change Failure Rate.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Kit the Builder ensures all store renovations follow approved architectural blueprints before ribbon-cutting ceremonies.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Refactoring an Anti-Pattern to 12-Factor</div>
          <p>Given an application that reads credentials from a local file <code>/etc/secrets.json</code>, write the refactored approach using GCP Secret Manager and environment variable references.</p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Worked Solution</h4>
          <p>Inject the secret directly from Secret Manager via Cloud Run secret volume mounts or environment variables, avoiding static filesystem coupling.</p>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Recall (Question 1)</span>
          <p><strong>According to the 12-Factor app methodology, where should application configuration (e.g. database URLs, API tokens) be stored?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Environment variables decouple configuration from source code across environments.')">A) In environment variables injected at runtime.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Hard-coding credentials in source code is an antipattern.')">B) In source code constants.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Committing config files into git leaks secrets across branches.')">C) In configuration files committed into Git.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Baking config into images breaks portability across dev/prod.')">D) Baked into the immutable Docker image layers.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://12factor.net/' target='_blank'>The Twelve-Factor App</a></li><li><a href='https://cloud.google.com/architecture/devops' target='_blank'>Google Cloud DevOps & DORA Capabilities</a></li></ul>"
    },

    # 007: Account, Tools and Access
    {
        "topic_no": "007",
        "roadmap_id": "1.1",
        "title": "Account, Tools and Access: Cloud Shell & gcloud",
        "page_type": "service",
        "phase": "Phase 1 — GCP Foundations",
        "lead": "Navigating Google Cloud: Web Console, Cloud Shell persistent home directories, gcloud CLI configurations, API enablement mechanics, and Cloud Code integration.",
        "comp1": ("Admin Developer", "Workstation CLI", "control", "Runs gcloud commands, authenticates OAuth tokens."),
        "comp2": ("Google Cloud API Gateway", "Service Usage API", "control", "Validates project API enablement and billing status."),
        "comp3": ("GCP Service APIs", "Compute / Storage APIs", "data", "Executes requested cloud resource provisioning."),
        "comp4": ("Cloud Audit Logs", "Activity Logging", "control", "Records who did what, where, and when.") ,
        "flow1": "Developer runs 'gcloud compute instances create' on terminal.",
        "flow2": "Service Usage API confirms Compute Engine API (compute.googleapis.com) is enabled for active project.",
        "flow3": "Compute Engine control plane allocates hypervisor slot and emits Admin Activity audit record.",
        "fail": "API call fails with 'SERVICE_DISABLED' error.",
        "heal": "Admin runs 'gcloud services enable compute.googleapis.com' to activate service control plane.",
        "city_concept": "City Hall Permits & Surveyor Field Tools",
        "p1": "Bea the Baker wanted to build a storefront, but City Hall guards turned her away because she had no surveyor permit or registration badge.",
        "p2": "Mayor Meridian handed Bea an official field toolkit (Cloud Shell) and verified her permit registry (gcloud auth & API Enablement).",
        "p3": "Bea attempted to open a heavy industrial flour mill without an industrial zoning permit. The request was halted until the zone license was granted.",
        "p4": "In City Hall, permits take 6 weeks of bureaucracy; in Google Cloud, enabling an API takes 8 seconds with gcloud services enable.",
        "part1_html": """
        <h3>The Situation: The Gateway to Google Cloud</h3>
        <p>
          Before deploying systems, architects must master interaction tools. Google Cloud provides three primary management interfaces: the Web Console for visual discovery, the <strong>Cloud Shell</strong> (a zero-cost pre-authenticated Debian VM with a 5GB persistent home directory), and the <strong>gcloud CLI</strong> for scriptable automation. Every single Google Cloud service begins in a disabled state; no resource can be provisioned until its specific API is explicitly enabled on the project.
        </p>
        <div class="callout">
          <div class="callout-title">Core CLI Concepts</div>
          <ul>
            <li><code>Named Configurations:</code> Switch instantly between corporate clients: <code>gcloud config configurations activate client-prod</code>.</li>
            <li><code>Project Pinning:</code> Set default project and compute region: <code>gcloud config set project brightloaf-prod</code>.</li>
            <li><code>API Enablement:</code> Activate services on-demand: <code>gcloud services enable compute.googleapis.com container.googleapis.com</code>.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: gcloud CLI Architecture</h4>
        <p>The gcloud CLI is a Python-based wrapper around Google Cloud REST APIs. Every command translates into authenticated JSON payloads over HTTPS.</p>
        <h4>Layer 2 — Practitioner: Authentication Methods</h4>
        <p>Never use long-lived service account JSON keys. Use <strong>Application Default Credentials (ADC)</strong> via <code>gcloud auth application-default login</code> for local testing, and service account impersonation for production access.</p>
        <h4>Layer 3 — Architect: Immutable Project IDs vs Numbers</h4>
        <p>Projects carry three identifiers: Project Name (mutable, display only), Project ID (immutable, globally unique, chosen by creator), and Project Number (immutable, assigned by Google, critical for service agent IAM).</p>
        <h4>Layer 4 — Staff: Quota & API Enablement Automation</h4>
        <p>Staff architects automate foundation bootstrapping using Terraform with <code>google_project_service</code> blocks to ensure deterministic API enablement across all enterprise projects.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, City Hall ensures no contractor digs trenches before their municipal badge is validated and building permits are countersigned.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Bootstrapping a Project via gcloud CLI</div>
          <pre><code># 1. Authenticate and configure active project
gcloud auth login
gcloud config set project brightloaf-dev-01
gcloud config set compute/region us-west1

# 2. Enable essential APIs
gcloud services enable compute.googleapis.com \
  container.googleapis.com \
  sqladmin.googleapis.com

# 3. Verify enabled services
gcloud services list --enabled --filter="NAME:compute*"</code></pre>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Recall (Question 1)</span>
          <p><strong>Which project identifier is globally unique across all of Google Cloud and cannot be changed after creation?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Project ID is immutable and globally unique across all Google Cloud customers.')">A) Project ID</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Project Name is mutable and does not need to be unique.')">B) Project Name</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Project Label is a key-value tag.')">C) Project Label</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Organization ID is unique to the org, not the project.')">D) Organization ID</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/sdk/docs' target='_blank'>Google Cloud SDK Documentation</a></li><li><a href='https://cloud.google.com/shell/docs' target='_blank'>Cloud Shell Overview</a></li></ul>"
    },

    # 008: Resource Hierarchy
    {
        "topic_no": "008",
        "roadmap_id": "1.2",
        "title": "Resource Hierarchy and Organization Policies",
        "page_type": "service",
        "phase": "Phase 1 — GCP Foundations",
        "lead": "Structuring enterprise cloud foundations: Organization nodes, Folders, Projects, additive IAM inheritance, Organization Policy constraints, and Labels vs Tags.",
        "comp1": ("Organization Node", "Cloud Identity Org", "control", "Root of trust tied to company domain (e.g. brightloaf.com)."),
        "comp2": ("Folder Hierarchy", "Department / Env", "control", "Groups projects by environment (Prod/Non-Prod) or business unit."),
        "comp3": ("GCP Projects", "Resource Containers", "control", "Billing, API, and IAM boundary containing actual workloads."),
        "comp4": ("Organization Policy Service", "Org Policy Engine", "control", "Enforces guardrails (e.g. disable external IPs, enforce CMEK)."),
        "flow1": "Security team sets Organization Policy constraint: 'constraints/compute.vmExternalIpAccess' = DENY at root.",
        "flow2": "Policy evaluates down entire folder tree and applies additively to all child projects.",
        "flow3": "Developer attempts to provision VM with public IP in child project; request is blocked by org constraint.",
        "fail": "Developer tries deploying VM with public IP.",
        "heal": "Control plane rejects request with 'Constraint compute.vmExternalIpAccess violated'.",
        "city_concept": "City Districts, Neighborhoods, and Building Charters",
        "p1": "Without zoning laws, shops opened inside residential parks, toxic factories dumped waste into bakery water, and nobody knew who governed which street.",
        "p2": "Mayor Meridian established the Civic Hierarchy: City Hall (Organization) oversees Districts (Folders), which contain individual City Lots (Projects).",
        "p3": "A reckless tenant tried building a 50-story skyscraper in a 2-story historic zone. City zoning codes (Organization Policies) blocked the bulldozer.",
        "p4": "In physical cities, corrupt inspectors might look away; in GCP, Organization Policies are enforced mathematically at the API gatekeeper level.",
        "part1_html": """
        <h3>The Situation: Structuring the Enterprise Landing Zone</h3>
        <p>
          When <strong>Brightloaf Bakery</strong> expanded from 1 store to 50 national bakeries, each development team created their own disconnected Google Cloud accounts using company credit cards. Security had zero visibility into active servers, bills were fragmented across 30 invoices, and an intern accidentally opened a database to the public internet. By establishing an <strong>Organization node</strong> tied to their Google Workspace domain and designing a robust <strong>Folder hierarchy</strong> with strict <strong>Organization Policies</strong>, Brightloaf established enterprise governance with centralized billing and security baselines.
        </p>
        <div class="callout danger">
          <div class="callout-title">The Fundamental IAM Law: Policies Are Additive</div>
          IAM permissions flow <strong>downward</strong> through the hierarchy:
          <pre>Organization -> Folders -> Projects -> Resources</pre>
          You <strong>cannot remove</strong> an inherited permission at a lower level with standard IAM! If an engineer is granted <code>roles/editor</code> at the Organization or Folder level, they have Editor rights on every single project underneath. (Only IAM Deny policies can override an inherited grant).
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: The Four Levels</h4>
        <ul>
          <li><strong>Organization:</strong> Root node tied to domain. Holds central super-admins.</li>
          <li><strong>Folders:</strong> Group projects by lifecycle (e.g., <code>Production</code>, <code>Staging</code>) or business unit (<code>Retail</code>, <code>Online</code>).</li>
          <li><strong>Projects:</strong> Core administrative container. Billing and APIs are enabled here.</li>
          <li><strong>Resources:</strong> VMs, buckets, databases living within projects.</li>
        </ul>
        <h4>Layer 2 — Practitioner: Labels vs Network Tags vs Resource Tags</h4>
        <table>
          <thead><tr><th>Item</th><th>Purpose</th><th>Scope</th><th>Enforcement</th></tr></thead>
          <tbody>
            <tr><td><strong>Labels</strong></td><td>Billing & cost attribution (key:value)</td><td>Resource level</td><td>Queried in BigQuery billing exports</td></tr>
            <tr><td><strong>Network Tags</strong></td><td>VPC firewall rule targeting (strings)</td><td>Compute instances</td><td>Applies firewall and routing rules</td></tr>
            <tr><td><strong>Resource Tags</strong></td><td>Hierarchical access control & Org Policies</td><td>Org/Folder/Project</td><td>Enforced via IAM conditions & policies</td></tr>
          </tbody>
        </table>
        <h4>Layer 3 — Architect: Landing Zone Best Practices</h4>
        <p>Never grant project-level access directly to individuals. Group projects under environment folders, bind roles to Google Groups, and enforce mandatory Org Policy constraints (e.g., <code>constraints/iam.disableServiceAccountKeyCreation</code>).</p>
        <h4>Layer 4 — Staff: Disaster Recovery & Project Lifecycle</h4>
        <p>When a project is deleted (<code>gcloud projects delete</code>), it enters a 30-day pending deletion state. During these 30 days, billing stops and resources shut down, but the project can be restored (<code>gcloud projects undelete</code>).</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, City Hall charter rules govern all municipal districts, ensuring residential neighborhoods remain free of noisy commercial diesel generators.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Setting an Organization Policy Constraint</div>
          <pre><code># Apply constraint to block external IP creation across the folder
gcloud resource-manager org-policies set-policy policy.yaml \
  --folder=123456789012</code></pre>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: PCA Scenario (Question 1)</span>
          <p><strong>A company wants to guarantee that developers cannot create external public IP addresses on any Compute Engine instance in their production and staging projects, regardless of their IAM roles. How should you design this control?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Organization Policy constraints override IAM permissions and enforce guardrails across the hierarchy.')">A) Define an Organization Policy constraint 'constraints/compute.vmExternalIpAccess' set to deny all at the parent folder level.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Developers with Compute Admin can modify firewall rules.')">B) Create a VPC firewall egress rule blocking port 80 and 443.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'IAM permissions are additive and do not prevent public IP creation if Compute Admin is granted.')">C) Remove the Network Admin role from developers.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Labels do not enforce operational constraints.')">D) Apply a billing label 'public-ip: false' to all projects.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy' target='_blank'>GCP Resource Hierarchy Guide</a></li><li><a href='https://cloud.google.com/resource-manager/docs/organization-policy/overview' target='_blank'>Organization Policy Service Overview</a></li></ul>"
    },

    # 013: Compute Engine
    {
        "topic_no": "013",
        "roadmap_id": "2.1",
        "title": "Compute Engine: VMs, Disks, and Managed Instance Groups",
        "page_type": "service",
        "phase": "Phase 2 — Core Services",
        "lead": "Deep dive into Google Compute Engine: machine families (General-purpose, Compute, Memory, Accelerator), Persistent Disk topologies, Managed Instance Groups (MIGs), Autohealing, and Spot VM economics.",
        "comp1": ("Client Traffic", "External Users", "data", "Incoming requests arriving at load balancer."),
        "comp2": ("Managed Instance Group", "Regional MIG (3 Zones)", "data", "Autoscaling fleet of stateless N2/E2 compute instances."),
        "comp3": ("Regional Persistent Disk", "Replicated Block Disk", "data", "Synchronous cross-zone replication between two zones."),
        "comp4": ("MIG Health Checker", "Autohealing Probe", "control", "Restarts unhealthy VMs failing application health probes."),
        "flow1": "Load balancer forwards user transactions to healthy instances across 3 zones.",
        "flow2": "MIG autoscaler monitors CPU utilization and dynamically provisions new instances.",
        "flow3": "If an instance freezes, the Autohealing controller detects health check failure and triggers automatic recreation.",
        "fail": "Host instance kernel panics or hardware fails.",
        "heal": "MIG recreates replacement VM in parallel zone; Regional Persistent Disk reattaches without data loss.",
        "city_concept": "City Fleet of Commercial Bakeries & Automated Maintenance Garages",
        "p1": "Brightloaf Bakery relied on one ancient, colossal oven. When its pilot light went out, all pastry production halted across the entire state for 14 hours.",
        "p2": "Tomas the Treasurer and Kit the Builder replaced the giant oven with a fleet of modular ovens spread across three city districts (Regional MIG).",
        "p3": "One oven's heating element malfunctioned. Dispatcher Rae automatically rerouted orders to sister bakeries while the maintenance garage swapped in a fresh oven.",
        "p4": "In physical factories, ovens cost millions and take months to install; in Compute Engine, MIGs spin up 50 instances in 45 seconds.",
        "part1_html": """
        <h3>The Situation: Enterprise Infrastructure as a Service</h3>
        <p>
          <strong>Compute Engine</strong> provides secure, high-performance virtual machines running on Google's global infrastructure. It caters to workloads requiring full OS control, legacy enterprise software (SAP, Oracle, Windows Server), high-performance computing (C3/H3), or custom kernel extensions.
        </p>
        <div class="callout">
          <div class="callout-title">Compute Engine Machine Families</div>
          <ul>
            <li><strong>General-Purpose (E2, N2, N4, C3):</strong> Best price-performance for web applications, databases, and microservices. E2 uses dynamic resource sharing; N2 offers predictable performance; C3 features Google's custom Titanium IPU.</li>
            <li><strong>Compute-Optimized (C2, C2D, H3):</strong> Highest per-core performance for gaming servers, video rendering, and batch processing.</li>
            <li><strong>Memory-Optimized (M2, M3):</strong> Giant RAM capacity (up to 12 TB memory) for SAP HANA and large in-memory databases.</li>
            <li><strong>Accelerator-Optimized (A2, A3, G2):</strong> Equipped with NVIDIA H100/L4 GPUs for AI training and LLM inference.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Boot Disks & Persistent Storage</h4>
        <p>VM root disks are network-attached block devices (Persistent Disks), not physical hard drives inside the server rack. Types include Standard HDD, Balanced SSD (pd-balanced), Performance SSD (pd-ssd), and Local SSD (ephemeral, physically attached, ultra-low latency, wiped on instance stop).</p>
        <h4>Layer 2 — Practitioner: Managed Instance Groups (MIGs)</h4>
        <p>A MIG uses an <strong>Instance Template</strong> to manage a homogeneous fleet of VMs. Key capabilities:</p>
        <ul>
          <li><strong>Autoscaling:</strong> Scales out based on target CPU utilization (e.g. 60%), Load Balancer utilization, or custom Cloud Monitoring metrics.</li>
          <li><strong>Autohealing:</strong> Dedicated health check probes application endpoint. If unresponsive for failure threshold, the MIG tears down the unhealthy VM and provisions a fresh replacement.</li>
          <li><strong>Rolling Updates:</strong> Deploys new instance templates gradually with <code>maxSurge</code> and <code>maxUnavailable</code> controls.</li>
        </ul>
        <h4>Layer 3 — Architect: Regional vs Zonal Resiliency</h4>
        <p>Always deploy <strong>Regional MIGs</strong> for production. Regional MIGs balance instances evenly across 3 zones. If an entire datacenter zone suffers catastrophic failure, the remaining two zones absorb traffic while the autoscaler replenishes capacity.</p>
        <h4>Layer 4 — Staff: Spot VMs & Live Migration Internals</h4>
        <p>Google Compute Engine performs <strong>Live Migration</strong>: when physical host hardware requires maintenance, Google migrates running VMs to a new physical host without shutting down the OS or dropping TCP connections. For fault-tolerant batch workloads, <strong>Spot VMs</strong> offer 60-91% discounts with the caveat that Google may preempt them with 30-second notice.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Bea operates a fleet of modular bakery kitchens. If one kitchen's mixer catches fire, dispatch routes dough to the neighboring kitchen automatically.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Creating an Autohealing Regional Managed Instance Group</div>
          <pre><code># 1. Create instance template with health endpoint
gcloud compute instance-templates create web-template \
  --region=us-west1 \
  --machine-type=e2-medium \
  --metadata=startup-script='#! /bin/bash
    apt-get update && apt-get install -y nginx
    echo "Healthy" > /var/www/html/healthz'

# 2. Create health check
gcloud compute health-checks create http web-health-check \
  --request-path=/healthz --port=80

# 3. Create regional MIG with autohealing
gcloud compute instance-groups managed create web-mig \
  --region=us-west1 \
  --template=web-template \
  --size=3 \
  --health-check=web-health-check \
  --initial-delay=120</code></pre>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: PCA Scenario (Question 1)</span>
          <p><strong>You are designing a fault-tolerant web application running on Compute Engine. The system must survive a complete datacenter zone outage with zero manual intervention, automatically heal failed instances, and minimize cost during off-peak hours. What is the recommended architecture?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Regional MIGs spread instances across 3 zones, autohealing replaces failed VMs, and autoscaling scales down off-peak.')">A) Regional Managed Instance Group with an autoscaling policy and autohealing health check connected to an Application Load Balancer.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Unmanaged instance groups lack autoscaling, autohealing, and rolling updates.')">B) Unmanaged instance groups across two zones with manual failover scripts.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Zonal MIG will completely fail if that single zone goes offline.')">C) Zonal Managed Instance Group with overprovisioned instance sizes.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Single VM cannot survive zone loss or provide autoscaling.')">D) Single N2-standard-16 VM with nightly automated disk snapshots.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/compute/docs/instance-groups' target='_blank'>MIGs Overview & Architecture</a></li><li><a href='https://cloud.google.com/compute/docs/disks' target='_blank'>Persistent Disk Topologies & Performance</a></li></ul>"
    }
]

def build_all():
    print(f"Building {len(TOPICS_DEFINITIONS)} core topics...")
    for t in TOPICS_DEFINITIONS:
        # Generate D1, D2, D3, analogy
        d1 = make_d1_map(t["topic_no"], t["roadmap_id"], t["title"], t["comp1"], t["comp2"], t["comp3"], t["comp4"])
        d2 = make_d2_flow(t["topic_no"], t["roadmap_id"], t["title"], t["flow1"], t["flow2"], t["flow3"])
        d3 = make_d3_failure(t["topic_no"], t["roadmap_id"], t["title"], t["fail"], t["heal"])
        analogy = make_analogy(t["topic_no"], t["roadmap_id"], t["title"], t["city_concept"], t["p1"], t["p2"], t["p3"], t["p4"])

        topic_data = {
            "topic_no": t["topic_no"],
            "roadmap_id": t["roadmap_id"],
            "title": t["title"],
            "page_type": t["page_type"],
            "phase": t["phase"],
            "lead": t["lead"],
            "d1": d1,
            "d2": d2,
            "d3": d3,
            "analogy": analogy,
            "part1_html": t["part1_html"],
            "part2_ladder_html": t["part2_ladder_html"],
            "part3_narrative_html": t["part3_narrative_html"],
            "part4_demo_html": t["part4_demo_html"],
            "quiz_html": t["quiz_html"],
            "reading_html": t["reading_html"]
        }
        build_topic_page(topic_data)
    print("Done building batch.")

if __name__ == '__main__':
    build_all()
