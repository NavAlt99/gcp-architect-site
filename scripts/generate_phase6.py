#!/usr/bin/env python3
"""
generate_phase6.py - Generates Topics 040 to 044 covering Phase 6: Optimization and Operations.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_website import build_topic_page
from batch_generate_full import make_d1_map, make_d2_flow, make_d3_failure, make_analogy

PHASE6_TOPICS = [
    # 040: Cost Optimization & FinOps
    {
        "topic_no": "040",
        "roadmap_id": "6.1",
        "title": "Cost Optimization & FinOps: CUDs, Spot VMs & Billing Analytics",
        "page_type": "concept",
        "phase": "Phase 6 — Optimization and Operations",
        "lead": "Maximizing cloud business value: FinOps lifecycle (Inform, Optimize, Operate), BigQuery billing export, Committed Use Discounts (CUDs), Spot VMs, storage tiering, and egress cost containment.",
        "comp1": ("Cloud Resource Fleet", "Compute & Databases", "data", "Generates usage events, network egress bytes, and storage allocations."),
        "comp2": ("Cloud Billing Export", "BigQuery Billing Feed", "control", "Streams granular SKU-level usage, project labels, and cost data to BigQuery daily."),
        "comp3": ("FinOps Intelligence", "Looker Studio / Recommender", "control", "Identifies idle resources, rightsizing candidates, and optimal CUD spend commitments."),
        "comp4": ("Automated Cost Policy", "Pub/Sub & Cloud Functions", "control", "Triggers automated shutdowns of non-production environments after business hours."),
        "flow1": "Workloads run across projects, tagged with standardized billing labels (env, cost-center, owner).",
        "flow2": "Billing export delivers daily cost data to BigQuery; Looker Studio dashboard displays unit cost per customer.",
        "flow3": "Recommender API identifies 40 idle persistent disks and recommends 1-year flexible CUDs.",
        "fail": "A batch test job spins up 200 high-memory instances on on-demand pricing and runs continuously over the weekend.",
        "heal": "Budget alert threshold triggers Cloud Function via Pub/Sub, automatically terminating runaway non-prod instances.",
        "city_concept": "City Budget Office & Municipal Utility Meters",
        "p1": "Municipal departments were leaving streetlights blazing at noon and running unused water pumps because nobody received a broken-down electricity bill.",
        "p2": "Treasurer Tomas installed smart digital meters (Billing Export) and gave each department a monthly utility dashboard (FinOps).",
        "p3": "Tomas signed a 3-year municipal coal contract at a 50% discount (Committed Use Discount) for the steady-state baseline power grid.",
        "p4": "City power contracts take months to negotiate; cloud Committed Use Discounts can be purchased instantly via Console or API.",
        "part1_html": """
        <h3>The Situation: The Shock of the Unmanaged Cloud Bill</h3>
        <p>
          Moving to the cloud shifts costs from predictable capital investments to variable operating expenses. Without proactive governance, organizations experience "cloud bill shock"—where unattached persistent disks, oversized VMs, and accidental cross-region egress result in massive unexpected costs.
        </p>
        <p>
          <strong>FinOps</strong> (Cloud Financial Operations) is the operational cultural framework that brings financial accountability to variable cloud spend. It follows a continuous three-phase lifecycle:
        </p>
        <div class="callout">
          <div class="callout-title">The FinOps Lifecycle</div>
          <ul>
            <li><strong>Inform:</strong> Establishing visibility. Exporting detailed billing data to BigQuery, enforcing mandatory resource labeling (<code>environment</code>, <code>cost-center</code>, <code>application</code>), and building Looker Studio dashboards.</li>
            <li><strong>Optimize:</strong> Taking action to reduce waste. Right-sizing oversized VMs, using Spot VMs for fault-tolerant batch workloads, deleting unattached disks, moving cold data to Archive storage, and purchasing Committed Use Discounts (CUDs).</li>
            <li><strong>Operate:</strong> Embedding continuous financial discipline into daily engineering workflows, tracking unit economics (cost per user or transaction), and setting automated budget alerts.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Granular Resource Labeling & BigQuery Export</h4>
        <p>Never rely on high-level monthly PDF invoices. Export detailed billing data directly to <strong>BigQuery</strong>. Enforce Organization Policies requiring labels on all resources to enable showback and chargeback.</p>
        <h4>Layer 2 — Practitioner: Spot VMs vs Committed Use Discounts (CUDs)</h4>
        <p>Use <strong>Spot VMs</strong> (60-91% discount) for stateless, interruptible batch processing. For predictable steady-state baselines, purchase <strong>Committed Use Discounts (CUDs)</strong>: Spend-based (flexible across regions and machine types) or Resource-based (highest discount for fixed vCPUs/RAM in a specific region).</p>
        <h4>Layer 3 — Architect: Network Egress & Storage Tiering Optimization</h4>
        <p>Network egress is frequently the most overlooked cloud expense: keep traffic within the same region whenever possible (inter-region and internet egress incur charges). Use <strong>Cloud Storage Autoclass</strong> to automatically transition unaccessed objects to Nearline, Coldline, and Archive tiers.</p>
        <h4>Layer 4 — Staff: Unit Economics & FinOps Automation</h4>
        <p>Staff architects tie cloud spend directly to business value: <em>"Our cost to process one checkout transaction dropped from $0.04 to $0.012."</em> Automate non-production environment shutdowns (e.g., stop staging VMs every evening at 19:00).</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Treasurer Tomas tracks water and power meters daily, turning off park fountains automatically when gates close at dusk.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: BigQuery Billing Query for Cost Anomalies</div>
          <p>Run a SQL query against exported billing data to find the top 5 cost-generating services over the past 30 days.</p>
        </div>
        <pre><code class="language-sql">SELECT
  service.description AS service_name,
  sku.description AS sku_name,
  ROUND(SUM(cost), 2) AS total_cost_usd,
  ROUND(SUM(usage.amount_in_pricing_units), 2) AS usage_quantity,
  usage.pricing_unit AS pricing_unit
FROM
  `my-billing-project.billing_export.gcp_billing_export_v1_012345_6789AB_CDEF01`
WHERE
  _PARTITIONDATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY
  service_name, sku_name, pricing_unit
ORDER BY
  total_cost_usd DESC
LIMIT 5;</code></pre>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: FinOps & Cost Strategy (Question 1)</span>
          <p><strong>A company runs a production GKE cluster hosting microservices that require steady, predictable CPU capacity 24/7/365, alongside an overnight batch processing workload that takes 4 hours and can tolerate unexpected node preemptions. What is the most cost-effective compute purchasing strategy?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! 3-year Committed Use Discounts provide maximum cost reduction (up to 70%) for predictable steady-state baselines, while Spot VMs provide up to 91% discount for interruptible overnight batch jobs.')">A) Purchase 3-year Committed Use Discounts (CUDs) for the steady-state microservice nodes, and use a separate Spot VM node pool for the overnight batch processing.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Running on-demand instances without commitments or Spot discounts results in paying full list price unnecessarily.')">B) Run all workloads on standard on-demand VMs without commitments.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Spot VMs are interruptible with 30s notice and should never host mission-critical production microservices without fallback.')">C) Run all production microservices and batch jobs exclusively on Spot VMs.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Sole-tenant nodes add premium dedicated hardware costs that increase overall expenditure.')">D) Provision sole-tenant nodes for all workloads.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/architecture/framework/cost-optimization' target='_blank'>Architecture Framework: Cost Optimization</a></li><li><a href='https://www.finops.org/framework/' target='_blank'>FinOps Foundation Framework</a></li></ul>"
    },

    # 041: Performance Optimization & Bottleneck Analysis
    {
        "topic_no": "041",
        "roadmap_id": "6.2",
        "title": "Performance Optimization: Bottlenecks, Caching & Scaling",
        "page_type": "concept",
        "phase": "Phase 6 — Optimization and Operations",
        "lead": "Systematic latency and throughput tuning: CPU, memory, IOPS, and network bottleneck isolation; multi-tier caching (Cloud CDN, Memorystore, BigQuery BI Engine); autoscaling cooldown tuning; and database connection pooling.",
        "comp1": ("Global Client Edge", "Cloud CDN & Anycast", "data", "Caches static assets at 100+ points of presence, offloading 85% of traffic from origins."),
        "comp2": ("Application Cache Tier", "Memorystore Redis", "data", "Sub-millisecond in-memory cache for frequently accessed session tokens and product catalogs."),
        "comp3": ("Stateless Compute Pool", "Cloud Run / MIG", "data", "Autoscaling compute fleet tuned with predictive scaling and optimized cooldown timers."),
        "comp4": ("High-Performance Database", "Spanner / AlloyDB", "data", "Columnar caching and connection poolers mitigating database connection storms."),
        "flow1": "Client requests web resource; Cloud CDN serves static content directly from edge cache in 12ms.",
        "flow2": "Dynamic API calls pass to Cloud Run, which queries Memorystore Redis cache for user session data.",
        "flow3": "Cache misses execute optimized, indexed queries against Cloud SQL via connection pooler.",
        "fail": "A sudden morning traffic surge causes severe thread starvation and database connection pool exhaustion.",
        "heal": "Cloud SQL Auth Proxy and PgBouncer connection pooler queue requests, preventing backend database crash.",
        "city_concept": "City Traffic Bottlenecks & Express Highway Lanes",
        "p1": "Every morning at 08:00, all cars and delivery trucks funnelled into a single one-lane cobblestone street, causing miles of gridlocked traffic.",
        "p2": "Traffic Engineer Tilda built express bypass lanes (Cloud CDN) and neighborhood parking hubs (Memorystore) so local commuters never entered the center.",
        "p3": "When a stadium concert let out, automated traffic signals synchronized green lights (Predictive Autoscaling) to flush traffic in 10 minutes.",
        "p4": "Paving physical bypass roads takes two years; configuring Cloud CDN edge caching takes 60 seconds via Cloud Console.",
        "part1_html": """
        <h3>The Situation: The Multi-Layer Latency Chain</h3>
        <p>
          When users complain that an application is "slow", engineers frequently make the mistake of immediately upgrading the VM instance size. If the bottleneck is actually an unindexed database query or disk IOPS throttling, doubling the VM's vCPU will increase the bill without improving performance.
        </p>
        <p>
          True performance optimization requires <strong>systematic bottleneck isolation</strong> across the entire request lifecycle:
        </p>
        <div class="callout">
          <div class="callout-title">The Four Classical Cloud Bottlenecks</div>
          <ul>
            <li><strong>CPU Bottleneck:</strong> Thread starvation, serialization locks, or compute-heavy encryption. Diagnosed via Cloud Profiler.</li>
            <li><strong>Memory Bottleneck:</strong> Excessive JVM garbage collection pauses, swapping, or OOM (Out Of Memory) container restarts.</li>
            <li><strong>Disk IOPS / Throughput:</strong> Persistent Disk performance scales with disk size and vCPU count! A 10 GB standard disk provides only 7.5 IOPS; a 1 TB SSD disk provides 30,000 IOPS.</li>
            <li><strong>Network Latency:</strong> Inter-region round trips, uncompressed payloads, missing HTTP/2 connection reuse, or Standard Tier network routing.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Multi-Tier Caching Architecture</h4>
        <p>Apply caching at every layer: (1) <strong>Cloud CDN</strong> at Google's edge for static images and CSS; (2) <strong>Memorystore (Redis/Memcached)</strong> for microservice session state; (3) <strong>BigQuery BI Engine</strong> for sub-second dashboard queries in memory.</p>
        <h4>Layer 2 — Practitioner: Autoscaling Cooldown & Predictive Scaling</h4>
        <p>Tune autoscaling parameters: configure <strong>cooldown periods</strong> (e.g. 60 seconds) to prevent aggressive thrashing. Enable <strong>predictive autoscaling</strong> on MIGs to spin up instances ahead of predicted daily traffic spikes.</p>
        <h4>Layer 3 — Architect: Database Connection Pooling & Query Plans</h4>
        <p>Every open PostgreSQL connection consumes ~10 MB of RAM. High-concurrency serverless microservices will easily exhaust database connection limits. Deploy <strong>PgBouncer</strong> or Cloud SQL connector poolers to multiplex thousands of client requests over a pool of 50 persistent connections.</p>
        <h4>Layer 4 — Staff: Network Performance & HTTP/3 Optimization</h4>
        <p>Mandate <strong>Premium Network Tier</strong> to enter Google's private global fiber backbone at the nearest point of presence. Enable HTTP/3 (QUIC) on Load Balancers to eliminate TCP head-of-line blocking over unreliable mobile connections.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Tilda synchronizes traffic signals and opens express highway lanes before morning rush hour begins.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Identifying the Root Bottleneck</div>
          <p>
            An architect inspects an application dashboard: VM CPU utilization is at 18%, Memory is at 35%, but API latency has increased from 80ms to 4,200ms. Disk write queue length is 120, and read latency is 85ms on a 50 GB standard persistent disk (pd-standard).
          </p>
          <p>Identify the bottleneck and provide the immediate architectural fix.</p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Bottleneck Remediation</h4>
          <ol>
            <li><strong>Root Cause:</strong> Disk IOPS and throughput starvation. A 50 GB standard persistent disk (<code>pd-standard</code>) provides only ~37.5 read/write IOPS and ~6 MB/s throughput, causing disk write queues to back up and threads to block on I/O.</li>
            <li><strong>Remediation:</strong> Upgrade the disk type to <code>pd-ssd</code> or <code>hyperdisk-balanced</code>, and increase the disk size to at least 250 GB. In GCP, disk performance scales directly with allocated disk capacity. Persistent disks can be resized online without stopping the virtual machine.</li>
          </ol>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Performance Tuning (Question 1)</span>
          <p><strong>A serverless web application deployed on Cloud Run communicates with Cloud SQL for PostgreSQL. Under peak traffic surges of 20,000 requests per minute, the application frequently fails with "FATAL: remaining connection slots are reserved for non-replication superuser connections". What is the recommended architectural solution?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Highly elastic serverless runtimes like Cloud Run create hundreds of container instances that easily exhaust PostgreSQL connection limits. Deploying a connection pooler (like PgBouncer) or using Cloud SQL connection pooling multiplexes connections efficiently.')">A) Deploy a database connection pooler such as PgBouncer between Cloud Run and Cloud SQL, or configure the built-in Cloud SQL connector connection pool limits.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Increasing max instances on Cloud Run will spin up even more containers, worsening database connection exhaustion.')">B) Increase Cloud Run max scale instances from 100 to 1,000.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud Storage is an object store; it cannot substitute for an active transactional SQL connection.')">C) Route database writes through a Cloud Storage bucket.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Disabling health checks masks availability failures and causes outages.')">D) Disable Cloud Run health checks to prevent superfluous connections.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/architecture/framework/performance-optimization' target='_blank'>Architecture Framework: Performance Optimization</a></li><li><a href='https://cloud.google.com/compute/docs/disks/performance' target='_blank'>Optimizing Persistent Disk and Hyperdisk Performance</a></li></ul>"
    },

    # 042: Infrastructure as Code: Terraform & Config Connector
    {
        "topic_no": "042",
        "roadmap_id": "6.3",
        "title": "Infrastructure as Code: Terraform, GitOps & Config Connector",
        "page_type": "service",
        "phase": "Phase 6 — Optimization and Operations",
        "lead": "Declarative cloud engineering: Terraform modular architecture, remote state management in Cloud Storage with object locking, Cloud Foundation Toolkit blueprints, and Kubernetes-native Config Connector.",
        "comp1": ("Git Source Repository", "Version-Controlled HCL", "control", "Stores modular Terraform manifests, variable definitions, and CI/CD triggers."),
        "comp2": ("CI/CD Terraform Runner", "Cloud Build / Atlantis", "control", "Executes terraform plan and terraform apply within automated security guardrails."),
        "comp3": ("Remote State Backend", "Cloud Storage Lock", "control", "Maintains encrypted, versioned Terraform state file with distributed mutex locking."),
        "comp4": ("Google Cloud API Fleet", "Target Infrastructure", "data", "Declaratively provisions VPCs, GKE clusters, and Cloud SQL databases without console drift."),
        "flow1": "Engineer submits Pull Request adding a new regional subnet and firewall rule in Terraform.",
        "flow2": "Cloud Build runs <code>terraform plan</code>, posting the planned resource diff directly to the PR comments.",
        "flow3": "Lead architect approves PR; pipeline acquires state lock in GCS and applies infrastructure changes cleanly.",
        "fail": "A junior engineer manually edits a firewall rule in the Google Cloud Console, causing configuration drift.",
        "heal": "Nightly automated Terraform CI/CD pipeline detects drift, revokes manual change, and restores declared Git state.",
        "city_concept": "City Master Schematics & Municipal Building Stamps",
        "p1": "Carpenters were adding balconies and knocking down load-bearing walls without recording changes on the city master architectural plans.",
        "p2": "City Architect Arthur declared that no brick could be laid without an approved Master Blueprint Stamp (Infrastructure as Code).",
        "p3": "When a rogue builder tried to add an unapproved staircase, inspectors compared the house to the master blueprint and dismantled the stairs.",
        "p4": "Updating paper blueprints requires drafting tables and erasers; Terraform HCL code is version-controlled, testable, and repeatable.",
        "part1_html": """
        <h3>The Situation: The Chaos of "ClickOps"</h3>
        <p>
          Provisioning cloud resources manually through the Google Cloud Console ("ClickOps") is an anti-pattern for enterprise workloads. It creates environments that cannot be reproduced, audited, or reliably recovered during a disaster. 
        </p>
        <p>
          <strong>Infrastructure as Code (IaC)</strong> treats cloud infrastructure with the exact same rigor as application code: written in declarative text files, version-controlled in Git, tested in CI/CD pipelines, and deployed automatically.
        </p>
        <div class="callout">
          <div class="callout-title">Core Terraform Concepts on Google Cloud</div>
          <ul>
            <li><strong>Declarative Syntax (HCL):</strong> You declare <em>what</em> the infrastructure should look like; Terraform calculates the dependency graph and steps needed to reach that state.</li>
            <li><strong>Remote State in Cloud Storage:</strong> Storing <code>terraform.tfstate</code> in an encrypted, versioned GCS bucket with automated locking prevents concurrent execution corruption.</li>
            <li><strong>Cloud Foundation Toolkit (CFT):</strong> Google's enterprise-grade, opinionated, production-ready Terraform modules that adhere to CIS security benchmarks.</li>
            <li><strong>Config Connector:</strong> A Kubernetes operator that allows you to manage Google Cloud resources (VPCs, Cloud SQL, Buckets) natively via Kubernetes Custom Resource Definitions (CRDs).</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Remote State Locking in GCS</h4>
        <p>Always configure a remote backend in Cloud Storage with Object Versioning enabled. Terraform uses GCS strongly-consistent metadata locking to prevent two engineers from applying changes simultaneously.</p>
        <h4>Layer 2 — Practitioner: Terraform Modules & Workspaces</h4>
        <p>Never write monolithic 5,000-line <code>main.tf</code> files. Break infrastructure into reusable modules (<code>modules/vpc</code>, <code>modules/gke</code>, <code>modules/cloudsql</code>). Use workspaces or folder-based environments (<code>environments/dev</code>, <code>environments/prod</code>).</p>
        <h4>Layer 3 — Architect: Drift Detection & Automated Reconciliation</h4>
        <p>Manual console changes create "configuration drift". Schedule a daily automated <code>terraform plan -detailed-exitcode</code> pipeline. If drift is detected, automatically notify SREs or trigger an auto-apply to overwrite unapproved changes.</p>
        <h4>Layer 4 — Staff: GitOps with Config Connector & Policy Controller</h4>
        <p>Staff architects implement GitOps: developers commit Kubernetes YAML manifests to Git. <strong>Config Sync</strong> syncs manifests to GKE, and <strong>Config Connector</strong> provisions the underlying GCP cloud infrastructure automatically.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Arthur's master schematics ensure that every district uses identical fire hydrants and pipe fittings.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Configuring a Secure Terraform GCS Backend</div>
          <p>Declare a remote Google Cloud Storage state backend with locking in your Terraform code.</p>
        </div>
        <pre><code class="language-hcl"># backend.tf
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  backend "gcs" {
    bucket  = "tf-state-brightloaf-prod-0123"
    prefix  = "terraform/state/production"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# main.tf
resource "google_compute_network" "vpc_network" {
  name                    = "custom-vpc-prod"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet_app" {
  name          = "subnet-app-us-central1"
  ip_cidr_range = "10.10.1.0/24"
  region        = "us-central1"
  network       = google_compute_network.vpc_network.id
  private_ip_google_access = true
}</code></pre>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: IaC Best Practices (Question 1)</span>
          <p><strong>A multi-team engineering department is adopting Terraform to manage cloud infrastructure across 30 GCP projects. What is the Google-recommended approach for managing the Terraform state file securely and reliably?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Storing Terraform state in a dedicated Cloud Storage bucket with object versioning, restricted IAM permissions, and automated state locking is the Google-recommended best practice.')">A) Use a dedicated Cloud Storage bucket with Object Versioning enabled and IAM least privilege to store the state file with automated distributed locking.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Committing state files into Git repositories leaks sensitive plaintext credentials and secrets.')">B) Commit the terraform.tfstate file directly into the shared Git source code repository.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Local state files prevent collaboration, lack locking, and are lost if the engineer laptop crashes.')">C) Keep state files on each developer local laptop filesystem.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Compute Engine root disks do not provide distributed concurrency locking across multiple team members.')">D) Store the state file on a Compute Engine persistent disk mounted on a jump host.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/docs/terraform' target='_blank'>Terraform on Google Cloud Guide</a></li><li><a href='https://cloud.google.com/config-connector/docs/overview' target='_blank'>Config Connector Overview</a></li></ul>"
    },

    # 043: CI/CD and Release Engineering
    {
        "topic_no": "043",
        "roadmap_id": "6.4",
        "title": "CI/CD & Release Engineering: Cloud Build, Deploy & DORA",
        "page_type": "service",
        "phase": "Phase 6 — Optimization and Operations",
        "lead": "Continuous delivery pipelines: Cloud Build serverless triggers, Artifact Registry provenance, Cloud Deploy automated canary targets, blue/green switching, and tracking the four DORA metrics.",
        "comp1": ("Developer Pull Request", "Cloud Source / GitHub", "control", "Code branch triggering automated webhook build pipelines upon peer approval."),
        "comp2": ("Continuous Integration", "Cloud Build Serverless", "control", "Compiles code, runs unit tests, scans CVEs, and publishes immutable image digest."),
        "comp3": ("Artifact Registry", "Signed Container Repository", "data", "Stores cryptographically signed artifacts with automated vulnerability scanning."),
        "comp4": ("Continuous Delivery", "Cloud Deploy Pipeline", "control", "Manages automated promotion across Dev, Staging, and Production with canary gates."),
        "flow1": "Developer merges commit to main branch; Cloud Build executes multi-step container build.",
        "flow2": "Image digest is pushed to Artifact Registry and signed with Binary Authorization attestation.",
        "flow3": "Cloud Deploy deploys release to Staging GKE cluster; automated integration tests pass.",
        "fail": "A critical regression in the production canary causes HTTP 500 error rates to spike to 6%.",
        "heal": "Cloud Deploy initiates automated 1-click rollback, restoring previous healthy container target in 15 seconds.",
        "city_concept": "City Municipal Printing Press & Delivery Fleets",
        "p1": "Newspaper delivery boys were printing unverified rumors and distributing them directly to town doorsteps, causing riots.",
        "p2": "Master Printer Paul established the Editorial Press Line (CI/CD): writers submit stories to editors, fact-checkers verify sources, and only approved papers are loaded onto wagons.",
        "p3": "When an error slipped into the morning edition, Paul sent a boy on a bicycle to replace the front page before wagons reached Main Street (Canary Rollback).",
        "p4": "Physical paper printing cannot be retracted once read; digital cloud deployments can be rolled back in seconds with zero downtime.",
        "part1_html": """
        <h3>The Situation: High-Velocity, Low-Risk Delivery</h3>
        <p>
          High-performing organizations do not choose between speed and stability. Research from <strong>DORA (DevOps Research and Assessment)</strong> proves that elite engineering teams deploy code multiple times per day while maintaining drastically lower failure rates.
        </p>
        <p>
          Google Cloud provides an integrated serverless continuous integration and continuous delivery (CI/CD) ecosystem:
        </p>
        <div class="callout">
          <div class="callout-title">The Four Core DORA Metrics</div>
          <ul>
            <li><strong>Deployment Frequency:</strong> How often code is successfully deployed to production (Elite: multiple deploys per day).</li>
            <li><strong>Lead Time for Changes:</strong> Time from code commit to running in production (Elite: less than one hour).</li>
            <li><strong>Mean Time to Recovery (MTTR):</strong> How long it takes to restore service after an incident (Elite: less than one hour).</li>
            <li><strong>Change Failure Rate:</strong> Percentage of deployments that cause a production failure or rollback (Elite: 0-15%).</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Cloud Build Serverless Pipelines</h4>
        <p>Cloud Build executes builds on fully managed, serverless infrastructure scaling to hundreds of concurrent workers. Define builds in <code>cloudbuild.yaml</code> with parallel build steps, caching, and substitutions.</p>
        <h4>Layer 2 — Practitioner: Modern Artifact Registry Practices</h4>
        <p>Never overwrite the <code>latest</code> tag. Tag images with immutable Git commit SHA hashes (e.g., <code>us-central1-docker.pkg.dev/proj/repo/app:sha-a8f23c</code>). Enable automated vulnerability scanning and cleanup policies.</p>
        <h4>Layer 3 — Architect: Cloud Deploy & Progressive Canary Promotion</h4>
        <p><strong>Cloud Deploy</strong> separates CI from CD. It manages delivery pipelines across target stages (Dev &gt; Staging &gt; Prod). Supports automated <strong>Canary deployments</strong>: deploy 10% to production, pause for approval or verification, then promote to 100%.</p>
        <h4>Layer 4 — Staff: Secure Supply Chain Pipelines (SLSA 3)</h4>
        <p>Staff architects enforce private worker pools with zero public IPs, service account token impersonation, and automated Binary Authorization signing at the build stage.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Paul fact-checks and prints municipal decrees in orderly batches before dispatching delivery riders.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Creating a Cloud Deploy Delivery Pipeline</div>
          <p>Define a declarative continuous delivery pipeline promoting releases from staging to production.</p>
        </div>
        <pre><code class="language-yaml"># clouddeploy.yaml
apiVersion: deploy.cloud.google.com/v1
kind: DeliveryPipeline
metadata:
  name: order-service-pipeline
description: Production delivery pipeline for Order Microservice
serialPipeline:
  stages:
  - targetId: staging-cluster
    profiles: [staging]
  - targetId: prod-cluster
    profiles: [prod]
    strategy:
      canary:
        runtimeConfig:
          kubernetes:
            serviceNetworking:
              service: "order-service"
              deployment: "order-service"
        canaryDeployment:
          percentages: [25, 50]
          verify: true</code></pre>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Release Engineering (Question 1)</span>
          <p><strong>Your engineering organization wants to eliminate deployment downtime and reduce blast radius during major application upgrades on GKE. If an error occurs during release, traffic must immediately revert to the stable version with zero user disruption. Which deployment strategy fulfills this?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Blue/Green deployment provisions an identical new environment (Green) alongside the stable active environment (Blue). Switching traffic at the load balancer or service level allows instant, zero-downtime cutover and immediate rollback.')">A) Blue/Green or Canary deployment managed via Cloud Deploy, allowing immediate traffic rollback if health metrics degrade.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Big Bang deployments replace all instances simultaneously and incur high downtime risk during failures.')">B) Big Bang cutover during off-peak weekend hours.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Deleting old pods before verifying new ones creates severe downtime and risks extended outages if new pods fail to start.')">C) Deleting all existing GKE pods before creating the new deployment.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Rolling updates without canary verification or automated health gating still expose 100% of users to undetected runtime bugs.')">D) Unconditional rolling update without readiness probes or health checks.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/deploy/docs' target='_blank'>Google Cloud Deploy Documentation</a></li><li><a href='https://dora.dev/' target='_blank'>DORA: DevOps Research and Assessment</a></li></ul>"
    },

    # 044: Operations and Process Improvement
    {
        "topic_no": "044",
        "roadmap_id": "6.5",
        "title": "Operations & Process Improvement: Platform Engineering & Reviews",
        "page_type": "concept",
        "phase": "Phase 6 — Optimization and Operations",
        "lead": "Scaling operational excellence: Modern platform operating models (Platform Team vs Stream-Aligned Teams), automated runbooks, incident retrospectives, and Well-Architected periodic reviews.",
        "comp1": ("Stream-Aligned Product Teams", "Autonomous Developers", "control", "Builds customer-facing business features using self-service platform primitives."),
        "comp2": ("Internal Developer Platform", "Platform Team / Portal", "control", "Provides golden paths, pre-approved Terraform modules, and automated landing zones."),
        "comp3": ("Automated Operations Engine", "Cloud Workflows / Runbooks", "control", "Automates routine maintenance: snapshot cleanup, log archiving, and certificate renewal."),
        "comp4": ("Well-Architected Review Board", "Periodic Governance", "control", "Conducts quarterly architectural audits evaluating cost, security, and reliability maturity."),
        "flow1": "Product team uses internal self-service portal to request a pre-hardened Cloud Run microservice sandbox.",
        "flow2": "Platform automation executes Terraform module, creating VPC subnet, IAM service account, and CI/CD triggers.",
        "flow3": "System runs in production; quarterly Well-Architected review evaluates SLO performance and identifies optimization targets.",
        "fail": "A critical production certificate expires because renewal was a manual spreadsheet task.",
        "heal": "Platform team replaces manual tasks with automated Cloud Workflow using Google-managed Certificate Manager.",
        "city_concept": "City Public Works Department & Civic Operations",
        "p1": "Every shop owner had to dig their own sewer ditch and pave their own sidewalk, creating a patchwork of broken gravel and overflowing gutters.",
        "p2": "Mayor Meridian established the Public Works Department (Platform Engineering): providing standardized paved roads, clean water mains, and street sweepers.",
        "p3": "Public Works conducted quarterly city audits, repairing cobblestones before wagons broke their axles.",
        "p4": "Physical city infrastructure maintenance requires heavy earthmovers; cloud platform automation updates thousands of resources via declarative APIs.",
        "part1_html": """
        <h3>The Situation: The Evolution of Cloud Operating Models</h3>
        <p>
          As organizations scale beyond a handful of cloud projects, the traditional centralized IT ticketing model (where developers file Jira tickets asking operations engineers to open a firewall port or provision a database) becomes the primary bottleneck to business agility.
        </p>
        <p>
          Leading cloud organizations adopt <strong>Platform Engineering</strong>. The Platform Team treats developer infrastructure as a product, providing <strong>"Golden Paths"</strong>—self-service, secure, automated templates that empower stream-aligned product teams to deploy autonomously.
        </p>
        <div class="callout">
          <div class="callout-title">The Three Operating Models</div>
          <ul>
            <li><strong>Centralized Operations (Legacy):</strong> Ops team owns and manages all infrastructure; developers throw code over the wall. High ticket queues, slow velocity.</li>
            <li><strong>You Build It, You Run It (Decentralized):</strong> Every product team manages their own VPCs, IAM, and servers. Fast, but leads to security drift, wasted spend, and duplicated effort.</li>
            <li><strong>Platform Engineering (Modern):</strong> A dedicated platform team builds automated self-service internal developer platforms (IDPs). Guardrails are built-in by default.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Eliminating Manual Toil with Runbook Automation</h4>
        <p>Toil is manual, repetitive, tactical work devoid of enduring value (e.g. manually restarting deadlocked pods, rotating passwords). Automate runbooks using <strong>Cloud Workflows</strong>, <strong>Cloud Scheduler</strong>, and Cloud Functions.</p>
        <h4>Layer 2 — Practitioner: Establishing the Cloud Center of Excellence (CCoE)</h4>
        <p>A cross-functional CCoE unites enterprise architects, security leads, finance (FinOps), and developers to establish architectural standards, review patterns, and govern landing zones.</p>
        <h4>Layer 3 — Architect: Conducting Well-Architected Reviews</h4>
        <p>Schedule formal quarterly architectural reviews for all tier-1 workloads. Evaluate designs against the Google Cloud Architecture Framework pillars, identifying single points of failure, cost leaks, and security risks.</p>
        <h4>Layer 4 — Staff: Enterprise Systems Thinking & Culture</h4>
        <p>Staff architects transform culture: moving from blame to psychological safety, fostering continuous learning, establishing transparent technical RFC processes, and aligning engineering roadmaps with business revenue outcomes.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Nora's Public Works crew maintains the civic foundation so merchants can focus entirely on serving customers.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Designing a Well-Architected Review Checklist</div>
          <p>
            Create a 5-question audit checklist for a team preparing to launch an e-commerce checkout service to production, covering Reliability, Security, Cost, and Operations.
          </p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Well-Architected Review Checklist</h4>
          <ol>
            <li><strong>Reliability:</strong> Does the architecture eliminate single points of failure? Are compute workloads distributed across at least 3 zones behind a regional load balancer with autohealing?</li>
            <li><strong>Security:</strong> Are backend instances deployed with zero public IPs? Are service account keys prohibited in favor of Workload Identity?</li>
            <li><strong>Cost:</strong> Are resources labeled with <code>cost-center</code> and <code>environment</code>? Have idle disks been removed and CUD commitments evaluated?</li>
            <li><strong>Operational Excellence:</strong> Is the entire infrastructure codified in Terraform? Are CI/CD pipelines configured with automated rollback?</li>
            <li><strong>Observability:</strong> Are SLIs and SLOs defined for checkout availability and latency with multi-window burn rate alerts configured?</li>
          </ol>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Cloud Operating Models (Question 1)</span>
          <p><strong>An enterprise enterprise engineering department suffers from slow release cycles because developers must submit manual tickets to a central infrastructure team for every new database, VPC subnet, and IAM role. Which operating model should the Chief Architect recommend to increase developer velocity while maintaining organizational governance?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Platform engineering establishes automated self-service golden paths with built-in security guardrails, allowing developers to provision pre-approved infrastructure autonomously.')">A) Transition to a Platform Engineering model: build an internal self-service developer platform using automated Terraform modules and policy guardrails.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Hiring more ticket processors scales costs linearly without addressing the fundamental operational bottleneck.')">B) Double the size of the centralized operations team to process Jira tickets faster.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Granting all developers full Project Owner permissions creates severe security risks, compliance violations, and uncontrolled cost ballooning.')">C) Grant all software developers Project Owner roles on production GCP projects.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Freezing all cloud deployments halts business innovation and solves nothing.')">D) Eliminate cloud infrastructure and move back to on-premises datacenters.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/architecture/framework/operational-excellence' target='_blank'>Architecture Framework: Operational Excellence</a></li><li><a href='https://teamtopologies.com/' target='_blank'>Team Topologies: Organizing Business & Technology Teams</a></li></ul>"
    }
]

def main():
    print(f"Building Phase 6 (Topics 040 to 044) - {len(PHASE6_TOPICS)} topics...")
    for item in PHASE6_TOPICS:
        t_no = item["topic_no"]
        r_id = item["roadmap_id"]
        title = item["title"]
        
        d1 = make_d1_map(t_no, r_id, title, item["comp1"], item["comp2"], item["comp3"], item["comp4"])
        d2 = make_d2_flow(t_no, r_id, title, item["flow1"], item["flow2"], item["flow3"])
        d3 = make_d3_failure(t_no, r_id, title, item["fail"], item["heal"])
        analogy = make_analogy(t_no, r_id, title, item["city_concept"], item["p1"], item["p2"], item["p3"], item["p4"])
        
        topic_data = {
            "topic_no": t_no,
            "roadmap_id": r_id,
            "title": title,
            "page_type": item["page_type"],
            "phase": item["phase"],
            "lead": item["lead"],
            "d1": d1,
            "d2": d2,
            "d3": d3,
            "analogy": analogy,
            "part1_html": item["part1_html"],
            "part2_ladder_html": item["part2_ladder_html"],
            "part3_narrative_html": item["part3_narrative_html"],
            "part4_demo_html": item["part4_demo_html"],
            "quiz_html": item["quiz_html"],
            "reading_html": item["reading_html"]
        }
        build_topic_page(topic_data)
        print(f"  ✓ Generated Topic {t_no}: {title}")

if __name__ == "__main__":
    main()
