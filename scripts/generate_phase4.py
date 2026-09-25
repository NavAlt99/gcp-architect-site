#!/usr/bin/env python3
"""
generate_phase4.py - Generates Topics 028 to 033 covering Phase 4: Reliability and High Availability.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_website import build_topic_page
from batch_generate_full import make_d1_map, make_d2_flow, make_d3_failure, make_analogy

PHASE4_TOPICS = [
    # 028: Reliability Fundamentals
    {
        "topic_no": "028",
        "roadmap_id": "4.1",
        "title": "Reliability Fundamentals: Availability Math & Failure Domains",
        "page_type": "concept",
        "phase": "Phase 4 — Reliability and High Availability",
        "lead": "Mathematical foundations of resilient systems: 99.9% vs 99.99% downtime calculations, series vs parallel composite SLAs, failure domains, exponential backoff with jitter, and circuit breakers.",
        "comp1": ("Edge Client Device", "User Traffic", "data", "Sends API requests with built-in retry logic and client-side circuit breakers."),
        "comp2": ("Load Balancer Ingress", "Global Anycast ALB", "data", "Distributes traffic across independent regional failure domains and health checks."),
        "comp3": ("Independent Regional Backends", "Multi-Zone Services", "data", "Stateless microservice instances isolated across separate fault domains."),
        "comp4": ("Resilience Telemetry", "Cloud Monitoring", "control", "Tracks error budgets, circuit breaker trips, and retry amplification."),
        "flow1": "Client sends API request to primary service endpoint.",
        "flow2": "Downstream dependency experiences transient network timeout (HTTP 503).",
        "flow3": "Client applies truncated exponential backoff with randomized jitter to prevent thundering herd overload.",
        "fail": "Downstream database becomes completely unresponsive, threatening cascading thread exhaustion.",
        "heal": "Circuit breaker trips to OPEN state, failing fast and serving cached fallback responses without waiting for timeouts.",
        "city_concept": "City Flood Gates & Dual Redundant Aqueducts",
        "p1": "When a single water pipe burst in the north district, the entire city ran dry because every neighborhood was connected in a single serial pipeline.",
        "p2": "Hydraulic Engineer Hugh installed dual parallel aqueducts with automated bulkhead valves isolating neighborhoods.",
        "p3": "During a flash flood, northern flood gates slammed shut, preventing contamination from reaching the southern drinking reservoir.",
        "p4": "Physical water pipes take days to reroute; digital network traffic reroutes across zones in milliseconds.",
        "part1_html": """
        <h3>The Situation: The Unforgiving Math of Downtime</h3>
        <p>
          At <strong>Brightloaf Bakery</strong>, the mobile ordering platform experienced three outages in one month. The VP of Engineering asked: <em>"We use Google Cloud, so why aren't we automatically 99.99% available?"</em>
        </p>
        <p>
          The answer lies in the mathematics of <strong>Composite SLAs</strong>. When services are chained in <strong>series</strong> (Service A depends on Service B, which depends on Service C), overall availability is the <em>product</em> of their individual SLAs:
        </p>
        <p style="text-align:center; font-family:var(--font-mono); color:var(--accent); font-size:15px; margin: 12px 0;">
          Composite SLA (Series) = SLA<sub>A</sub> × SLA<sub>B</sub> × SLA<sub>C</sub>
        </p>
        <p>
          If each service has an individual SLA of 99.9% (0.999), the composite availability is:
          <br><code>0.999 × 0.999 × 0.999 = 0.9970 (99.70%)</code>.
          <br>That represents over <strong>2 hours and 11 minutes</strong> of allowed downtime per month!
        </p>
        <div class="callout">
          <div class="callout-title">The Availability Math Table</div>
          <ul>
            <li><strong>99% (Two 9s):</strong> ~7.31 hours downtime per month (~3.65 days/year).</li>
            <li><strong>99.9% (Three 9s):</strong> ~43.8 minutes downtime per month (~8.77 hours/year).</li>
            <li><strong>99.95% (Three and a half 9s):</strong> ~21.9 minutes downtime per month (~4.38 hours/year).</li>
            <li><strong>99.99% (Four 9s):</strong> ~4.38 minutes downtime per month (~52.6 minutes/year).</li>
            <li><strong>99.999% (Five 9s - Spanner):</strong> ~26.3 seconds downtime per month (~5.26 minutes/year).</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Series vs Parallel Availability Math</h4>
        <p>To improve availability beyond any single component, place components in <strong>parallel</strong> (redundancy):<br><code>SLA = 1 - ((1 - SLA_A) × (1 - SLA_B))</code>. Two 99.9% components in parallel achieve <code>1 - (0.001 × 0.001) = 99.9999%</code>.</p>
        <h4>Layer 2 — Practitioner: Failure Domains & Blast Radius</h4>
        <p>Isolate failure domains: VM failure &lt; Zonal failure &lt; Regional failure &lt; Global control plane failure. Architect workloads so a single zone outage never drops more than 33% of capacity.</p>
        <h4>Layer 3 — Architect: Exponential Backoff, Jitter & Circuit Breakers</h4>
        <p>Simple retries create a "thundering herd" or "retry storm" that crushes recovering backends. Always add <strong>randomized jitter</strong>: <code>sleep = min(cap, base × 2^attempt) + rand(0, base)</code>. Use <strong>Circuit Breakers</strong> (Open, Half-Open, Closed) to fail fast when error rates cross 50%.</p>
        <h4>Layer 4 — Staff: Bulkheads, Graceful Degradation & Load Shedding</h4>
        <p>When saturated, drop low-priority requests (search recommendations, analytics logging) with HTTP 429 to protect high-priority transactions (order checkout, payment processing).</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Hugh designs parallel water lines and automated isolation gates so a break on Main Street never cuts off City Hospital.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Calculating Composite SLA</div>
          <p>
            An application relies on three components in series: (1) Cloud Run (SLA: 99.95%), (2) Cloud SQL Regional HA (SLA: 99.95%), and (3) Memorystore Redis Standard (SLA: 99.9%).
          </p>
          <p>Calculate: (a) The composite SLA for the entire path, and (b) The maximum allowed monthly downtime.</p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>SLA Calculation Solution</h4>
          <ol>
            <li><strong>Composite SLA:</strong> 0.9995 × 0.9995 × 0.999 = <code>0.99800025 (99.80%)</code>.</li>
            <li><strong>Allowed Monthly Downtime:</strong> 30 days × 24 hrs × 60 min = 43,200 total minutes.<br>
            <code>43,200 × (1 - 0.9980) = 86.4 minutes</code> (~1 hour 26 minutes per month).</li>
            <li><strong>Architectural Takeaway:</strong> Even with high-grade managed services, chaining three services drops your end-to-end SLA below 99.9%! To fix this, decouple the cache or make it an optional non-blocking lookup.</li>
          </ol>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: SLA Math (Question 1)</span>
          <p><strong>A business contract requires an SLA of 99.95% monthly availability for a public web application. The proposed design consists of an External HTTPS Load Balancer (99.99%) routing to Compute Engine Regional MIG (99.99%) which queries a single unmanaged MySQL VM in one zone (99.5%). Will this system meet the contract SLA?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Series composite SLA is limited by its weakest link: 0.9999 × 0.9999 × 0.995 = 99.48%, which fails the 99.95% requirement by a wide margin.')">A) No, because the serial dependency on the unmanaged single-zone MySQL VM caps overall availability at roughly 99.48%.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'The load balancer does not compensate for a failed backend database.')">B) Yes, because the 99.99% load balancer masks the database downtime.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'SLAs multiply across serial dependencies; you cannot average them.')">C) Yes, because the mathematical average of the components is (99.99 + 99.99 + 99.5) / 3 = 99.82%.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Regional MIG does not mitigate database failure.')">D) Yes, because the Regional MIG automatically heals database crashes.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/architecture/framework/reliability' target='_blank'>Architecture Framework: Reliability Pillar</a></li><li><a href='https://sre.google/sre-book/embracing-risk/' target='_blank'>Google SRE Book: Embracing Risk & Availability Math</a></li></ul>"
    },

    # 029: SRE Concepts, SLIs, SLOs & Error Budgets
    {
        "topic_no": "029",
        "roadmap_id": "4.2",
        "title": "SRE Concepts: SLIs, SLOs, Error Budgets & The Four Golden Signals",
        "page_type": "concept",
        "phase": "Phase 4 — Reliability and High Availability",
        "lead": "Site Reliability Engineering principles: Service Level Indicators (SLIs), Service Level Objectives (SLOs), error budget release gating, the Four Golden Signals (Latency, Traffic, Errors, Saturation), and blameless post-mortems.",
        "comp1": ("Customer Journey", "Checkout Traffic", "data", "Represents real user interactions passing through production endpoints."),
        "comp2": ("SLI Metric Collector", "Cloud Monitoring", "control", "Measures good events vs total valid events (e.g. HTTP responses < 300ms without 5xx)."),
        "comp3": ("SLO & Error Budget Engine", "Service Level Objective", "control", "Calculates remaining monthly error budget and evaluates burn rate alerts."),
        "comp4": ("CI/CD Release Gating", "Cloud Deploy", "control", "Automatically halts deployment pipeline when error budget burn rate exceeds 14.4x."),
        "flow1": "Users submit checkout transactions through cloud load balancer.",
        "flow2": "Cloud Monitoring computes SLI: <code>Count(HTTP 200 & latency < 200ms) / Count(Total Requests)</code>.",
        "flow3": "When SLO is 99.9% and errors consume 20% of error budget in 1 hour, burn-rate alerting triggers SRE pager.",
        "fail": "A buggy software release deploys to production, driving error rates to 8% and rapidly depleting the error budget.",
        "heal": "Release gating policy automatically freezes feature deployments until reliability engineering restores budget.",
        "city_concept": "City Public Transit Reliability Pledges",
        "p1": "Commuters complained subway trains were always late, but city transit managers insisted operations were 'fine'.",
        "p2": "Transit Director Tilda defined the Transit Pledge (SLO): 99% of subway trains must arrive within 3 minutes of scheduled time.",
        "p3": "When track construction caused train delays that consumed 80% of the monthly delay budget, all non-essential upgrades were halted to prioritize repairs.",
        "p4": "Subway schedules are adjusted on paper quarterly; cloud SLO burn rates can automatically throttle deployment pipelines in real time.",
        "part1_html": """
        <h3>The Situation: Resolving the Conflict Between Dev and Ops</h3>
        <p>
          In traditional software teams, developers are rewarded for shipping features quickly, while operations engineers are rewarded for keeping systems stable. This creates an adversarial relationship: Dev wants change, Ops fears change.
        </p>
        <p>
          Google Site Reliability Engineering (SRE) resolves this structural conflict using <strong>Service Level Objectives (SLOs)</strong> and <strong>Error Budgets</strong>:
        </p>
        <div class="callout">
          <div class="callout-title">The SRE Vocabulary: SLI, SLO, SLA</div>
          <ul>
            <li><strong>SLI (Service Level Indicator):</strong> A quantifiable metric of service performance:
              <br><code>SLI = (Good Events / Total Valid Events) × 100%</code>.
            </li>
            <li><strong>SLO (Service Level Objective):</strong> An internal reliability target agreed upon by Product and Engineering (e.g., 99.9% of requests over 30 rolling days).</li>
            <li><strong>SLA (Service Level Agreement):</strong> A commercial contract with external customers specifying financial consequences or credits if violated. (Rule: <code>SLO &gt; SLA</code>).</li>
            <li><strong>Error Budget:</strong> The room for unreliability: <code>Error Budget = 100% - SLO</code>. For a 99.9% SLO, the error budget is <strong>0.1%</strong>.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: The Four Golden Signals</h4>
        <p>Focus monitoring on the 4 Golden Signals: <strong>Latency</strong> (time taken to serve a request), <strong>Traffic</strong> (demand / RPS / concurrent sessions), <strong>Errors</strong> (explicit failures like HTTP 5xx, or misformed responses), and <strong>Saturation</strong> (fraction of constrained resources used, e.g. memory or thread pool saturation).</p>
        <h4>Layer 2 — Practitioner: Multi-Window Multi-Burn-Rate Alerts</h4>
        <p>Do not alert on static thresholds (e.g. CPU &gt; 80%). Alert on <strong>Error Budget Burn Rate</strong>: a 14.4x burn rate consumes 2% of your monthly budget in 1 hour; this requires immediate paging. A 2x burn rate consumes 10% in 36 hours; send a ticket.</p>
        <h4>Layer 3 — Architect: Error Budget Policies & Release Freezes</h4>
        <p>Establish a binding social contract: when the error budget is exhausted, developers stop shipping new product features and focus 100% of their sprints on reliability, bug fixes, and test automation.</p>
        <h4>Layer 4 — Staff: Blameless Post-Mortems & Eliminating Toil</h4>
        <p>When incidents occur, conduct blameless post-mortems focused on systemic flaws, not human mistakes. SRE teams cap operational toil (manual repetitive tasks) at 50%, dedicating the remaining time to engineering automation.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Tilda tracks subway delays against public benchmarks, pausing track painting whenever on-time performance dips.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Creating an SLO in Cloud Monitoring</div>
          <p>Define an availability SLO using the Google Cloud CLI or Monitoring API.</p>
        </div>
        <pre><code class="language-bash"># 1. List available monitored services
gcloud monitoring services list

# 2. Create a service for an App/Cloud Run service
gcloud monitoring services create \\
    --service-id="checkout-service" \\
    --display-name="Checkout Microservice"

# 3. Define an Availability SLO (99.9% over a 28-day rolling window)
# slo.json:
# {
#   "displayName": "99.9% - High Availability Checkout",
#   "goal": 0.999,
#   "rollingPeriod": "2419200s",
#   "serviceLevelIndicator": {
#     "basicSli": {
#       "availability": {}
#     }
#   }
# }
gcloud monitoring services slos create \\
    --service="checkout-service" \\
    --config-from-file="slo.json"</code></pre>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: SRE Principles (Question 1)</span>
          <p><strong>Your team maintains a critical payment API with an SLO of 99.95% availability over a 30-day window. After a major deployment, the service experiences a 2-hour outage, burning 100% of the monthly error budget. According to SRE principles, what action should the engineering team take?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! When an error budget is depleted, the error budget policy dictates freezing non-critical feature releases and redirecting engineering capacity to stability, testing, and hardening.')">A) Halt new feature deployments and dedicate engineering sprints to reliability improvements, automated rollbacks, and bug fixes until the error budget recovers.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Arbitrarily lowering the SLO hides problems and violates customer expectations.')">B) Immediately lower the SLO to 99.0% so feature deployments can continue without violation.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Blameless culture strictly prohibits punitive actions against individuals.')">C) Identify the engineer who merged the PR and remove their deployment privileges.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Ignoring error budgets undermines the entire purpose of SRE governance.')">D) Continue deploying new features as scheduled while silencing monitoring alerts for the remainder of the month.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://sre.google/workbook/implementing-slos/' target='_blank'>Google SRE Workbook: Implementing SLOs</a></li><li><a href='https://cloud.google.com/monitoring/service-monitoring' target='_blank'>Cloud Monitoring Service-Level Objectives (SLOs)</a></li></ul>"
    },

    # 030: High Availability by Layer
    {
        "topic_no": "030",
        "roadmap_id": "4.3",
        "title": "High Availability by Layer: Compute, Network, Storage & Database",
        "page_type": "service",
        "phase": "Phase 4 — Reliability and High Availability",
        "lead": "Architecting multi-layer redundancy: Regional MIGs with autohealing, GKE multi-zone node pools, HA VPN dual tunnels, Spanner multi-region Paxos, and Cloud DNS failover routing.",
        "comp1": ("Edge Network Layer", "Cloud DNS & Global ALB", "data", "Anycast frontend with 100% SLA Cloud DNS and health-checked backend routing."),
        "comp2": ("Compute Tier", "Regional MIG / GKE", "data", "Instances spread across 3 availability zones with Pod Disruption Budgets."),
        "comp3": ("Database Tier", "Cloud SQL HA / Spanner", "data", "Synchronous multi-zone replication with automated heartbeats and sub-minute failover."),
        "comp4": ("Storage & Messaging", "Dual-Region GCS / Pub/Sub", "data", "Geo-redundant object storage and global durable message queues."),
        "flow1": "Global ALB receives traffic and routes across healthy instances in Zone A, B, and C.",
        "flow2": "App instances execute transactions and persist state to synchronous multi-zone database.",
        "flow3": "Cloud Storage and Pub/Sub replicate objects and messages across regions automatically.",
        "fail": "A physical datacenter fiber cut takes out all of Zone us-central1-b.",
        "heal": "Load Balancer stops routing to Zone B; Regional MIG autoheals by provisioning replacement VMs in Zone A and C.",
        "city_concept": "City Civil Defense & Multi-Grid Redundancy",
        "p1": "A transformer explosion at the central power plant plunged the entire metropolitan transit, hospital, and water systems into darkness.",
        "p2": "City Planner Nora divided the city into three independent power districts connected by automated cross-tie switches.",
        "p3": "When Substation B flooded, Substation A and C automatically doubled their output, keeping hospitals and traffic lights running seamlessly.",
        "p4": "High-voltage city grid switching takes mechanical relays and minutes; software-defined cloud routing balances load in seconds.",
        "part1_html": """
        <h3>The Situation: Eliminating Single Points of Failure (SPOFs)</h3>
        <p>
          High availability (HA) cannot be achieved by focusing on a single layer. An application with a perfectly resilient Kubernetes cluster will still experience total downtime if it connects to a single-zone database, or if its DNS provider has an outage.
        </p>
        <p>
          A true enterprise architect applies <strong>defense-in-depth redundancy</strong> across every layer of the technology stack:
        </p>
        <div class="callout">
          <div class="callout-title">The Four Layers of High Availability</div>
          <ul>
            <li><strong>Network Layer:</strong> Cloud DNS (100% SLA guarantee), Global External Application Load Balancers, Cloud HA VPN (two active tunnels in separate gateway interfaces for 99.99% SLA), redundant Cloud Routers with BGP.</li>
            <li><strong>Compute Layer:</strong> Regional Managed Instance Groups (MIGs) distributing VMs evenly across 3 zones with autohealing; GKE Regional Clusters with multi-zone node pools and Pod Disruption Budgets (PDBs).</li>
            <li><strong>Database Layer:</strong> Cloud SQL Regional HA (primary and standby in separate zones with synchronous block-level replication); Cloud Spanner (multi-region synchronous Paxos replication across 3+ regions with 99.999% SLA).</li>
            <li><strong>Storage & Messaging Layer:</strong> Dual-Region or Multi-Region Cloud Storage buckets with turbo replication; Cloud Pub/Sub with automatic global message replication across multiple zones.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Zonal vs Regional vs Multi-Regional Deployments</h4>
        <p>Zonal resources (single VM, single persistent disk) fail when the zone fails. Regional resources (Regional MIG, Cloud SQL HA) survive single zone outages. Multi-region resources (Spanner, Multi-Region GCS) survive entire regional disasters.</p>
        <h4>Layer 2 — Practitioner: Health Checks (Shallow vs Deep) & Autohealing</h4>
        <p>Configure separate <strong>Readiness Probes</strong> (is the app ready to take traffic?) and <strong>Liveness Probes</strong> (is the app deadlocked and in need of a reboot?). Never let a health check query an external database (deep probe); a database slowdown will cause the LB to kill all app instances simultaneously!</p>
        <h4>Layer 3 — Architect: GKE High Availability Primitives</h4>
        <p>Enforce <code>topologySpreadConstraints</code> to balance pods across failure zones; configure <code>PodDisruptionBudgets</code> (PDB) to ensure at least 80% of replicas remain available during node pool upgrades.</p>
        <h4>Layer 4 — Staff: Multi-Region Active-Active Data Synchronization</h4>
        <p>Staff architects navigate CAP theorem trade-offs: choosing between external consistency (Cloud Spanner Paxos) or eventual consistency (Bigtable multi-cluster replication with write conflicts resolved by last-write-wins).</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Nora ensures hospitals have solar panels, backup diesel generators, and two separate municipal grid connections.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Creating a Regional Managed Instance Group with Autohealing</div>
          <p>Deploy a resilient regional compute cluster across 3 zones with automated health monitoring.</p>
        </div>
        <pre><code class="language-bash"># 1. Create a health check for autohealing
gcloud compute health-checks create http hc-web-autohealing \\
    --port=80 \\
    --request-path="/healthz" \\
    --check-interval=5s \\
    --timeout=5s \\
    --unhealthy-threshold=3 \\
    --healthy-threshold=2

# 2. Create an instance template
gcloud compute instance-templates create template-web-v1 \\
    --machine-type=e2-medium \\
    --image-family=debian-12 \\
    --image-project=debian-cloud \\
    --tags=http-server \\
    --metadata=startup-script='#!/bin/bash
      apt-get update && apt-get install -y nginx
      echo "Healthy" > /var/www/html/healthz'

# 3. Create a Regional MIG distributing instances across 3 zones
gcloud compute instance-groups managed create mig-web-regional \\
    --template=template-web-v1 \\
    --size=6 \\
    --region=us-central1 \\
    --health-check=hc-web-autohealing \\
    --initial-delay=60s</code></pre>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: HA Architecture (Question 1)</span>
          <p><strong>You are designing a mission-critical web application on Compute Engine that must survive the complete loss of an availability zone with zero human intervention and no downtime. Which configuration is required?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Regional Managed Instance Groups automatically distribute VMs across multiple zones and provision replacements if a zone suffers an outage.')">A) A Regional Managed Instance Group (MIG) configured across 3 zones behind an External Application Load Balancer with autohealing enabled.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'A zonal instance group resides in one zone and will fail completely if that zone has an outage.')">B) A Zonal Managed Instance Group with 10 instances in us-central1-a.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Unmanaged instance groups lack autohealing and automated multi-zone capacity rebalancing.')">C) An unmanaged instance group with VMs in two separate zones.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Standalone VMs require manual script intervention and cannot participate in automated regional load balancing health checks.')">D) Two standalone VMs in different zones managed by cron shell scripts.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/compute/docs/instance-groups/distributing-instances-with-regional-migs' target='_blank'>Distributing Instances with Regional MIGs</a></li><li><a href='https://cloud.google.com/kubernetes-engine/docs/concepts/regional-clusters' target='_blank'>GKE Regional Clusters Architecture</a></li></ul>"
    },

    # 031: Disaster Recovery Patterns (RTO/RPO)
    {
        "topic_no": "031",
        "roadmap_id": "4.4",
        "title": "Disaster Recovery Patterns: RTO, RPO & Multi-Region Strategies",
        "page_type": "concept",
        "phase": "Phase 4 — Reliability and High Availability",
        "lead": "Preparing for catastrophic failures: Recovery Time Objective (RTO) vs Recovery Point Objective (RPO), Backup & Restore, Pilot Light, Warm Standby, and Hot Standby (Active-Active).",
        "comp1": ("Primary Active Region", "Production DC / Region", "data", "Handles 100% of live production traffic and transactional writes."),
        "comp2": ("Replication Pipeline", "Storage / DB Replication", "control", "Replicates data asynchronously or synchronously to secondary disaster recovery target."),
        "comp3": ("Disaster Recovery Region", "Secondary Standby", "data", "Maintains pilot light or warm compute capacity ready to absorb traffic during disaster."),
        "comp4": ("DR Orchestration Engine", "Cloud DNS / Runbook", "control", "Monitors primary health and executes automated or 1-click failover routing."),
        "flow1": "Production region processes live user transactions and replicates database snapshots to secondary region.",
        "flow2": "Continuous health monitoring probes detect total loss of primary production region.",
        "flow3": "Failover runbook executes: Cloud DNS updates routing policies and standby compute scales up to full production capacity.",
        "fail": "Catastrophic submarine cable severance isolates the primary cloud region.",
        "heal": "Global Load Balancer detects regional backend failure and shifts 100% of incoming traffic to standby region.",
        "city_concept": "City Evacuation Drills & Emergency Operations Centers",
        "p1": "When a catastrophic river flood inundated the downtown municipal hall, all emergency communications ceased because all backup radios were stored in the basement.",
        "p2": "Mayor Meridian established an Emergency Operations Bunker on the southern hill (Standby DR Site) with independent power and synchronized radio logs.",
        "p3": "During the annual spring drill (Game Day), the city cut main hall power to prove the southern bunker could assume emergency control in under 15 minutes.",
        "p4": "Moving civil emergency personnel requires physical trucks and sirens; cloud DR cutover shifts global network traffic with a DNS route change.",
        "part1_html": """
        <h3>The Situation: Designing for the Worst-Case Scenario</h3>
        <p>
          High Availability (HA) protects against component or zonal failures within a region. <strong>Disaster Recovery (DR)</strong> protects against catastrophic events that take down an entire geographic region (earthquakes, submarine fiber cuts, massive geopolitical events, or widespread power grid collapses).
        </p>
        <p>
          DR strategy is defined strictly by two business metrics:
        </p>
        <div class="callout">
          <div class="callout-title">RTO and RPO Definitions</div>
          <ul>
            <li><strong>RTO (Recovery Time Objective):</strong> How long can the business tolerate being offline before services are restored? (e.g., <em>"System must be back online within 15 minutes."</em>)</li>
            <li><strong>RPO (Recovery Point Objective):</strong> How much data loss can the business tolerate, measured in time? (e.g., <em>"We cannot lose more than 5 minutes of transaction data."</em>)</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: The 4 Core DR Patterns</h4>
        <ol>
          <li><strong>Backup and Restore (Cold):</strong> Highest RTO (hours/days), highest RPO (hours). Data backed up to Cloud Storage; infrastructure provisioned from scratch via Terraform upon disaster. Lowest cost.</li>
          <li><strong>Pilot Light:</strong> Moderate RTO (15-30 min), low RPO (minutes). Database runs continuously in DR region with live replication; minimal core servers running; app tier spun up via MIGs on failover.</li>
          <li><strong>Warm Standby:</strong> Low RTO (minutes), very low RPO (seconds). Scaled-down version of full environment running in DR region ready to take immediate traffic.</li>
          <li><strong>Hot Standby / Active-Active:</strong> Near-zero RTO, zero RPO. Traffic actively served from both regions concurrently fronted by Global External Application Load Balancer. Highest cost.</li>
        </ol>
        <h4>Layer 2 — Practitioner: Data Replication Trade-offs</h4>
        <p>Synchronous replication guarantees zero data loss (RPO = 0) but adds latency (speed of light over fiber). Asynchronous replication has zero write latency impact on primary transactions, but incurs data loss (RPO &gt; 0) during an abrupt regional outage.</p>
        <h4>Layer 3 — Architect: Failover & Failback Mechanics</h4>
        <p>Plan the <strong>failback</strong> before you plan the failover! Once the disaster is resolved, how do you sync newly created records from the DR region back to the primary region without dual-writing or data corruption?</p>
        <h4>Layer 4 — Staff: Disaster Recovery Testing (Game Days & Drills)</h4>
        <p>An untested DR plan is merely a hypothesis. Staff architects conduct mandatory tabletop exercises and live Game Days, injecting chaos and verifying runbooks against real systems under controlled conditions.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Nora runs quarterly blackout drills, switching municipal emergency dispatches to the secondary bunker to prove the system works.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Selecting the Optimal DR Pattern</div>
          <p>Match the business requirement to the most cost-effective DR pattern:</p>
          <ol>
            <li><strong>Scenario A:</strong> E-commerce checkout: RTO &lt; 1 minute, RPO = 0. Budget: High.</li>
            <li><strong>Scenario B:</strong> Employee internal wiki: RTO &lt; 24 hours, RPO &lt; 24 hours. Budget: Minimal.</li>
            <li><strong>Scenario C:</strong> Financial reporting portal: RTO &lt; 20 minutes, RPO &lt; 5 minutes. Budget: Moderate.</li>
          </ol>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Pattern Selection Rubric</h4>
          <ul>
            <li><strong>Scenario A:</strong> <em>Hot Standby / Multi-Region Active-Active</em> using Cloud Spanner multi-region and Cloud Run across two regions with Global ALB.</li>
            <li><strong>Scenario B:</strong> <em>Backup and Restore (Cold)</em> using nightly Cloud Storage bucket replication and Terraform scripts stored in Git.</li>
            <li><strong>Scenario C:</strong> <em>Pilot Light</em> with Cloud SQL cross-region read replica and a pre-configured instance template in the secondary region.</li>
          </ul>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: DR Strategy (Question 1)</span>
          <p><strong>A financial trading application requires an RPO of less than 1 second and an RTO of less than 30 seconds across geographic regions. Which database and compute architecture fulfills these strict requirements?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Cloud Spanner multi-region synchronous replication guarantees RPO=0 across regions, and active-active compute behind a Global External Application LB provides sub-minute RTO.')">A) Multi-region Cloud Spanner instance with active-active compute services running in two regions fronted by a Global External Application Load Balancer.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud SQL cross-region read replicas use asynchronous replication; promotion takes several minutes and incurs data loss (RPO > 1 second).')">B) Cloud SQL with an asynchronous cross-region read replica and manual promotion scripts.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Restoring databases from nightly snapshots incurs hours of data loss (RPO = hours).')">C) Compute Engine instances with automated nightly snapshots transferred to a secondary region.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Firestore single-region databases cannot serve traffic if the primary region goes offline.')">D) Firestore in Native Mode in a single region with Cloud DNS failover routing.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/architecture/disaster-recovery' target='_blank'>Disaster Recovery Planning Guide on Google Cloud</a></li><li><a href='https://cloud.google.com/architecture/dr-scenarios-for-data' target='_blank'>Disaster Recovery Scenarios for Data</a></li></ul>"
    },

    # 032: Observability: Monitoring, Logging & Trace
    {
        "topic_no": "032",
        "roadmap_id": "4.5",
        "title": "Observability: Cloud Monitoring, Logging, Trace & Profiler",
        "page_type": "service",
        "phase": "Phase 4 — Reliability and High Availability",
        "lead": "Full-stack visibility across Google Cloud: Cloud Monitoring dashboards, centralized log sinks and Log Analytics, distributed tracing with Cloud Trace, Cloud Profiler, and Ops Agent.",
        "comp1": ("Compute Workloads", "GKE / VMs / Run", "data", "Generates structured JSON logs, OpenTelemetry traces, and system metrics."),
        "comp2": ("Google Cloud Ops Agent", "Telemetry Daemon", "control", "Streams host metrics and application logs to Google Cloud Observability backend."),
        "comp3": ("Cloud Log Router & Sinks", "Log Routing Pipeline", "control", "Filters and exports security audit logs to BigQuery and Cloud Storage archives."),
        "comp4": ("Cloud Monitoring & Alerting", "Incident Engine", "control", "Evaluates alerting policies, uptime checks, and dispatches PagerDuty notifications."),
        "flow1": "Application emits structured JSON log entries to stdout and exports traces via OpenTelemetry.",
        "flow2": "Log Router processes entries, matching filter rules and streaming security events to centralized security project.",
        "flow3": "Monitoring dashboard visualizes p99 latency; alert policy triggers notification when error threshold is breached.",
        "fail": "A sudden latency spike occurs on an internal microservice, causing 504 Gateway Timeouts.",
        "heal": "Engineer inspects Cloud Trace flame graph, identifying an unindexed database query taking 4.2 seconds.",
        "city_concept": "City Monitoring Towers & Dispatch Telemetry",
        "p1": "Firefighters only discovered fires when citizens ran into the station screaming; the city had no centralized alarm system.",
        "p2": "Chief Inspector Ines built high observation towers with smoke detectors, barometers, and direct telegraph wires to dispatch.",
        "p3": "When a minor smoke plume appeared in the grain warehouse, dispatchers dispatched a fire brigade in 45 seconds before flames spread.",
        "p4": "Telegraph wires can break in severe storms; cloud observability pipelines use distributed global endpoints with buffered retries.",
        "part1_html": """
        <h3>The Situation: You Cannot Manage What You Cannot Measure</h3>
        <p>
          In modern distributed cloud systems with dozens of microservices, troubleshooting by SSH-ing into individual virtual machines and grepping log files is obsolete. 
        </p>
        <p>
          Google Cloud Observability (formerly Stackdriver) provides an integrated suite covering the three pillars of observability: <strong>Metrics</strong>, <strong>Logs</strong>, and <strong>Traces</strong>:
        </p>
        <div class="callout">
          <div class="callout-title">The Observability Suite Components</div>
          <ul>
            <li><strong>Cloud Monitoring:</strong> Real-time performance dashboards, custom metrics, uptime checks, and automated alerting policies with multi-channel dispatch (Slack, PagerDuty, Webhooks).</li>
            <li><strong>Cloud Logging:</strong> Centralized log aggregation with sub-second search, Log Router sinks, and Log Analytics (powered by BigQuery SQL syntax).</li>
            <li><strong>Cloud Trace:</strong> Distributed tracing that visualizes latency bottlenecks across microservices using latency flame graphs.</li>
            <li><strong>Cloud Profiler:</strong> Continuous low-overhead CPU and memory profiling of production applications to identify code hotspots.</li>
            <li><strong>Error Reporting:</strong> Automatically groups application stack traces and exceptions into deduplicated issues with status tracking.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Structured Logging & The Ops Agent</h4>
        <p>Always output logs as single-line JSON to <code>stdout</code>/<code>stderr</code> containing <code>severity</code>, <code>message</code>, and <code>trace</code> IDs. On Compute Engine VMs, install the unified <strong>Ops Agent</strong> (combines Fluent Bit and OpenTelemetry).</p>
        <h4>Layer 2 — Practitioner: Centralized Log Sinks & Log Exclusions</h4>
        <p>Use Organization-level Log Sinks to route all audit logs across all enterprise projects into a central locked BigQuery dataset or Cloud Storage bucket. Use <strong>Log Exclusions</strong> to drop high-volume debug logs and save cost.</p>
        <h4>Layer 3 — Architect: OpenTelemetry Instrumentation & Trace Propagation</h4>
        <p>Adopt vendor-neutral OpenTelemetry standards. Propagate the <code>traceparent</code> W3C HTTP header across microservice hops so a single end-to-end user request can be visualized in Cloud Trace.</p>
        <h4>Layer 4 — Staff: Log Analytics & Security Information Integration (SIEM)</h4>
        <p>Enable Log Analytics to query petabytes of logs using standard SQL queries. Stream high-severity security logs to Chronicle / SecOps for automated threat hunting.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Inspector Ines monitors dials and gauges in the central dispatch room, spotting water leaks before streets flood.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Creating a Centralized Log Sink via CLI</div>
          <p>Export all high-severity error logs across your project to a central BigQuery dataset for compliance auditing.</p>
        </div>
        <pre><code class="language-bash"># 1. Create target BigQuery dataset for audit logs
bq mk --location=US audit_logs_dataset

# 2. Create the Cloud Logging sink
gcloud logging sinks create central-audit-sink \\
    bigquery.googleapis.com/projects/my-audit-project/datasets/audit_logs_dataset \\
    --log-filter='severity>=ERROR AND protoPayload.@type="type.googleapis.com/google.cloud.audit.AuditLog"'

# 3. Grant the sink's unique service account write permissions on BigQuery
# The command output provides the writerIdentity (e.g. serviceAccount:p12345-sinks@gcp-sa-logging.iam.gserviceaccount.com)
gcloud projects add-iam-policy-binding my-audit-project \\
    --member="serviceAccount:service-PROJECT_NUMBER@gcp-sa-logging.iam.gserviceaccount.com" \\
    --role="roles/bigquery.dataEditor"</code></pre>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Observability Architecture (Question 1)</span>
          <p><strong>A compliance auditor requires your company to retain all Admin Activity and Data Access audit logs across 50 production GCP projects for 7 years in an immutable format, with the ability to run SQL queries for forensic investigations. Which architecture fulfills these requirements at the lowest cost?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Organization-level aggregated log sinks route logs from all child projects into a centralized BigQuery dataset or Cloud Storage bucket with Bucket Lock (WORM) retention for 7 years.')">A) Create an aggregated log sink at the GCP Organization level routing to a central project with BigQuery Log Analytics and Cloud Storage with Object Retention Lock (WORM).</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Default log bucket retention is 30 or 400 days and does not meet the 7-year regulatory requirement.')">B) Keep logs in the default _Default log bucket in each individual project.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Streaming millions of logs to an unmanaged Compute Engine VM running Elasticsearch is expensive, unreliable, and creates high operational overhead.')">C) Run an unmanaged Elasticsearch cluster on a single Compute Engine instance and forward logs via syslog.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Pub/Sub retains messages for at most 7 days and is not a durable 7-year storage medium.')">D) Stream all logs into a Pub/Sub topic with 7-year message retention enabled.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/logging/docs/routing/overview' target='_blank'>Cloud Logging: Routing & Storage Overview</a></li><li><a href='https://cloud.google.com/trace/docs' target='_blank'>Cloud Trace Distributed Tracing</a></li></ul>"
    },

    # 033: Testing for Reliability & Chaos Engineering
    {
        "topic_no": "033",
        "roadmap_id": "4.6",
        "title": "Testing for Reliability: Load, Chaos & Game Days",
        "page_type": "concept",
        "phase": "Phase 4 — Reliability and High Availability",
        "lead": "Proactive resilience validation: Distributed load testing with k6/Locust, chaos engineering fault injection, canary analysis, and structured Game Day simulations.",
        "comp1": ("Distributed Load Generator", "Locust / k6 on GKE", "data", "Simulates realistic synthetic user traffic profiles and traffic spikes."),
        "comp2": ("Chaos Injection Engine", "Chaos Mesh / Litmus", "control", "Injects artificial CPU stress, packet loss, DNS corruption, and killed instances."),
        "comp3": ("Production System Under Test", "Resilient Architecture", "data", "Multi-zone application stack designed to absorb stress and heal automatically."),
        "comp4": ("Automated Canary Analyzer", "Cloud Deploy / Spinnaker", "control", "Evaluates SLI deviations on 5% canary traffic before approving full rollout."),
        "flow1": "Load generator ramps synthetic traffic from 1,000 RPS to 50,000 RPS over 15 minutes.",
        "flow2": "Chaos engine terminates 50% of application pods in Zone A simultaneously.",
        "flow3": "System auto-scales in Zone B and C; Canary analyzer confirms p99 latency remains within SLO bounds.",
        "fail": "Chaos injection reveals that application pods hang for 60 seconds on terminated database connections.",
        "heal": "Engineers configure aggressive TCP keep-alive and connection pool timeout limits, resolving the failover hang.",
        "city_concept": "City Fire Drills & Controlled Seismic Testing",
        "p1": "The city built a massive new suspension bridge, but nobody knew if it could withstand gale-force winds until a winter storm nearly collapsed it.",
        "p2": "Chief Inspector Ines established mandatory wind-tunnel testing and controlled seismic vibration drills before certifying public structures.",
        "p3": "During a simulated gas explosion drill, emergency dispatchers noticed a hospital route was blocked by construction and established a permanent bypass.",
        "p4": "Physical city destructive testing damages concrete; cloud chaos experiments inject non-destructive, scoped digital faults.",
        "part1_html": """
        <h3>The Situation: The Illusion of Reliability</h3>
        <p>
          You cannot prove a system is reliable by letting it run undisturbed during quiet business hours. The true resilience of an architecture is only revealed when things break—under severe load spikes, unexpected hardware crashes, or network partitions.
        </p>
        <p>
          <strong>Chaos Engineering</strong> is the discipline of experimenting on a system in order to build confidence in the system's capability to withstand turbulent conditions in production.
        </p>
        <div class="callout">
          <div class="callout-title">The Reliability Testing Hierarchy</div>
          <ul>
            <li><strong>Unit & Integration Testing:</strong> Validates functional business logic in isolated code modules.</li>
            <li><strong>Load & Stress Testing:</strong> Identifies system breaking points, saturation bottlenecks, and autoscaling latency (using tools like Locust, k6, or JMeter).</li>
            <li><strong>Chaos Engineering:</strong> Injects failure modes (killing nodes, adding latency, blocking egress ports) to verify graceful degradation and circuit breakers.</li>
            <li><strong>Canary Deployments:</strong> Routes a small fraction of real production traffic (e.g., 2-5%) to a new release to catch regressions before full rollout.</li>
            <li><strong>Game Days:</strong> Cross-functional team exercises where engineers simulate real-world disaster scenarios to test incident response and runbooks.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Load Testing vs Stress Testing</h4>
        <p>Load testing validates that the system fulfills expected peak production traffic (e.g., 10,000 RPS). Stress testing pushes the system far beyond capacity (e.g., 50,000 RPS) to observe how it fails—whether it sheds load gracefully or crashes completely.</p>
        <h4>Layer 2 — Practitioner: Progressive Rollouts & Canary Analysis</h4>
        <p>Using <strong>Cloud Deploy</strong> with automated canary targets: deploy version 2 to 10% of users, evaluate error rate and latency SLIs for 30 minutes, and automatically promote to 100% or execute a 1-click rollback.</p>
        <h4>Layer 3 — Architect: Blast-Radius Minimization in Chaos Experiments</h4>
        <p>Never run unconstrained chaos tests in production. Constrain experiments using blast-radius limiters: start in staging, inject faults into a single canary pod, and have an immediate "Emergency Stop" button that aborts the test instantly.</p>
        <h4>Layer 4 — Staff: Running Enterprise Game Days</h4>
        <p>Staff architects organize quarterly Game Days. One team ("Red Team") acts as the chaos instigator, while the on-call SRE team ("Blue Team") must diagnose, mitigate, and resolve the incident using only their dashboards, alerts, and runbooks.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Ines schedules controlled emergency tests with smoke machines to ensure hospital dispatchers react instantly.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Designing a Chaos Experiment Plan</div>
          <p>
            Write a 4-step Chaos Engineering experiment plan for Brightloaf Bakery to verify that their <strong>Regional GKE cluster</strong> survives the sudden loss of an entire availability zone.
          </p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Chaos Experiment Plan</h4>
          <ol>
            <li><strong>Hypothesis:</strong> If all nodes in Zone <code>us-central1-a</code> are abruptly drained, the Regional GKE cluster will redistribute pods to Zones <code>b</code> and <code>c</code>, maintaining p99 latency &lt; 300ms with zero HTTP 5xx errors.</li>
            <li><strong>Steady State Metric:</strong> Monitor checkout SLI (successful transactions &gt; 99.95%, p99 latency &lt; 250ms).</li>
            <li><strong>Fault Injection:</strong> Execute <code>kubectl drain &lt;node-in-zone-a&gt; --delete-emptydir-data --force --ignore-daemonsets</code> or cordoning all nodes in the target zone.</li>
            <li><strong>Rollback / Stop Criterion:</strong> If overall HTTP error rate exceeds 1% for more than 30 seconds, immediately uncordon nodes and abort the experiment.</li>
          </ol>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Reliability Verification (Question 1)</span>
          <p><strong>Before deploying a major architectural change to a mission-critical billing pipeline, your team wants to verify that the system can handle a 5x surge in transactions while automatically isolating failures. What is the most effective engineering methodology to achieve this?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Running distributed stress tests combined with automated canary deployments and structured chaos experiments validates both peak load handling and fault isolation.')">A) Conduct distributed load and stress testing using synthetic generators combined with progressive canary deployments and monitored chaos experiments.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Manual code reviews cannot predict distributed runtime saturation or network partition behaviors.')">B) Rely exclusively on manual peer code reviews without performing load or chaos testing.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Deploying untested architectural changes directly to 100% of production traffic violates basic SRE release safety.')">C) Deploy the new version immediately to 100% of production traffic during peak business hours to see if it holds up.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Testing on a single developer workstation does not simulate multi-node network latency or database concurrency.')">D) Run unit tests on a developer laptop and extrapolate performance from CPU utilization.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/architecture/framework/reliability' target='_blank'>Architecture Framework: Testing for Reliability</a></li><li><a href='https://principlesofchaos.org/' target='_blank'>Principles of Chaos Engineering</a></li></ul>"
    }
]

def main():
    print(f"Building Phase 4 (Topics 028 to 033) - {len(PHASE4_TOPICS)} topics...")
    for item in PHASE4_TOPICS:
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
