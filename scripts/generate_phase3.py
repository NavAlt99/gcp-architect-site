#!/usr/bin/env python3
"""
generate_phase3.py - Generates Topics 022 to 027 covering Phase 3: Architecture Thinking.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_website import build_topic_page
from batch_generate_full import make_d1_map, make_d2_flow, make_d3_failure, make_analogy

PHASE3_TOPICS = [
    # 022: Requirements Analysis
    {
        "topic_no": "022",
        "roadmap_id": "3.1",
        "title": "Requirements Analysis: Business & Technical Discovery",
        "page_type": "concept",
        "phase": "Phase 3 — Architecture Thinking",
        "lead": "Transforming ambiguous stakeholder goals into measurable engineering specifications: functional vs non-functional '-ilities', SLAs, latency budgets, MoSCoW prioritization, and stakeholder mapping.",
        "comp1": ("Business Stakeholder", "Executive / Product", "control", "Defines business revenue goals, time-to-market constraints, and regulatory requirements."),
        "comp2": ("Lead Cloud Architect", "Solution Design", "control", "Translates business drivers into measurable non-functional technical requirements."),
        "comp3": ("Target GCP Architecture", "System Blueprint", "data", "Combines managed compute, database, and network services to fulfill SLA/SLO."),
        "comp4": ("Requirements Traceability Matrix", "Doc Repository", "control", "Maps every business constraint to verified architecture components."),
        "flow1": "Architect conducts discovery interviews across CTO, Finance, Operations, and Security teams.",
        "flow2": "Qualitative expectations ('system must be fast') are formalized into measurable SLIs ('p99 latency < 250ms at 50,000 RPS').",
        "flow3": "Architecture design decisions are documented in a Requirements Traceability Matrix and approved by stakeholders.",
        "fail": "Stakeholder changes compliance requirements late in project; architecture lacks encryption at rest auditability.",
        "heal": "Architect refactors storage layer to use Cloud KMS Customer-Managed Encryption Keys (CMEK) and updates requirement matrix.",
        "city_concept": "City Zoning Board & Municipal Charters",
        "p1": "Residents demanded 'faster streets' and 'better power', but builders poured concrete without knowing if trucks or bicycles would use the roads.",
        "p2": "The Zoning Board (Requirements Analysis) established precise civic metrics: roads must support 10-ton vehicles at 40 km/h with 99.9% bridge uptime.",
        "p3": "During a sudden heatwave, the power grid sagged because air conditioning demand was never captured in the non-functional requirements.",
        "p4": "City road re-zoning takes decades; in software architecture, cloud elastic capacity can be dynamically provisioned in minutes.",
        "part1_html": """
        <h3>The Situation: Bridging the Business-Technical Chasm</h3>
        <p>
          At <strong>Brightloaf Bakery</strong>, the executive team announced plans to scale online ordering to 25 countries. The CEO told engineering: <em>"Make it fast, reliable, and cheap."</em> Without systematic requirements analysis, one engineer provisioned a multi-region active-active Spanner database costing $20,000/month, while another deployed a single micro-VM that crashed on day one.
        </p>
        <p>
          The Lead Cloud Architect intervened by instituting formal <strong>Requirements Discovery</strong>. The team segregated Functional Requirements (what the system does: cart checkout, recipe search) from Non-Functional Requirements (how the system behaves: 99.95% monthly availability, p99 latency &lt; 200ms, RTO &lt; 15 min).
        </p>
        <div class="callout">
          <div class="callout-title">The Non-Functional '-ilities' Matrix</div>
          <ul>
            <li><strong>Availability:</strong> e.g., 99.95% uptime allows at most 21.9 minutes of unplanned downtime per month.</li>
            <li><strong>Scalability:</strong> Handling peak load spikes (e.g., 10x traffic increase during Black Friday morning) without manual intervention.</li>
            <li><strong>Durability:</strong> Cloud Storage 99.999999999% (11 9s) ensures data survives physical media failures.</li>
            <li><strong>Observability:</strong> Exporting SLI metrics, centralized audit logs, and distributed traces with sub-second ingestion.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Functional vs Non-Functional Requirements</h4>
        <p>Functional requirements define business workflows (user authentication, payment processing). Non-functional requirements (NFRs) dictate performance, security, compliance, and disaster recovery constraints.</p>
        <h4>Layer 2 — Practitioner: Quantifying Ambiguity & MoSCoW Prioritization</h4>
        <p>Never accept vague terms like "high availability". Convert them into: <em>"System must sustain 5,000 requests/sec with p99 latency &lt; 300ms across 2 GCP regions with zero data loss (RPO = 0)"</em>. Use MoSCoW (Must have, Should have, Could have, Won't have) to protect release dates.</p>
        <h4>Layer 3 — Architect: Stakeholder Mapping & Conflict Resolution</h4>
        <p>Balancing conflicting stakeholder priorities: Finance wants lowest cost (OpEx reduction), Security demands zero external IPs and CMEK encryption, Product wants rapid feature delivery, and SRE demands strict error budgets.</p>
        <h4>Layer 4 — Staff: Strategic Enterprise Alignment & TCO</h4>
        <p>Staff architects validate long-term contracts, existing software licenses (Bring Your Own License for Windows/SQL Server), vendor lock-in trade-offs, and multi-year Total Cost of Ownership models.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Chief Planner Nora interviews emergency services, merchants, and residential leaders before approving structural foundations.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Discovery Interview to Technical Specification</div>
          <p>
            A retail client states: <em>"Our checkout system must never lose orders, even if a whole datacenter burns down. We expect 1,000 orders/sec during holiday sales. Customers complain if pages take more than 1 second to load."</em>
          </p>
          <p>Translate these business statements into: (1) Availability target, (2) RTO/RPO targets, (3) Latency SLI, and (4) GCP service selection candidates.</p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Architectural Specification Solution</h4>
          <ol>
            <li><strong>Availability Target:</strong> 99.99% monthly availability with multi-region failover.</li>
            <li><strong>RTO / RPO:</strong> RTO &lt; 5 minutes (automated failover); RPO = 0 (synchronous replication across regions).</li>
            <li><strong>Latency SLI:</strong> p99 end-to-end checkout response time &lt; 800ms at 1,000 RPS.</li>
            <li><strong>GCP Candidates:</strong> Cloud Spanner multi-region instance for ACID order persistence (RPO=0), Cloud Run or GKE across multiple regions fronted by a Global External Application Load Balancer.</li>
          </ol>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Scenario Analysis (Question 1)</span>
          <p><strong>A financial enterprise requires that financial transaction records are guaranteed never to be lost in the event of an entire GCP region outage, with immediate zero-downtime consistency for balance inquiries. Which technical constraint and database selection satisfies this requirement?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! RPO=0 across regions requires synchronous replication with external consistency, which Cloud Spanner multi-region provides natively.')">A) RPO = 0; Cloud Spanner multi-region instance with synchronous Paxos replication.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud SQL cross-region read replicas use asynchronous replication; failover incurs data loss (RPO > 0).')">B) RPO = 0; Cloud SQL with an asynchronous cross-region read replica.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Firestore in single-region mode cannot survive a full regional outage.')">C) RPO = 15 minutes; Firestore single-region database with hourly snapshots.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Bigtable provides eventual consistency across clusters, not strict ACID transactional balance consistency.')">D) RPO = 0; Cloud Bigtable multi-cluster replication.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/architecture/framework' target='_blank'>Google Cloud Architecture Framework: Overview</a></li><li><a href='https://cloud.google.com/architecture/framework/system-design' target='_blank'>Architecture Framework: System Design Pillar</a></li></ul>"
    },

    # 023: Google Cloud Architecture Framework
    {
        "topic_no": "023",
        "roadmap_id": "3.2",
        "title": "Google Cloud Architecture Framework: The Six Pillars",
        "page_type": "concept",
        "phase": "Phase 3 — Architecture Thinking",
        "lead": "Guiding architectural excellence through Google's six pillars: System Design, Operational Excellence, Security, Reliability, Cost Optimization, and Performance Optimization.",
        "comp1": ("Architecture Review Board", "Governance Team", "control", "Evaluates system designs against Google Cloud Architecture Framework pillars."),
        "comp2": ("Reliability & Security Pillars", "Core Principles", "control", "Enforces zero-trust identity, fault isolation, and automated incident recovery."),
        "comp3": ("Cost & Performance Pillars", "Efficiency Engine", "data", "Optimizes resource allocation, committed use discounts, and autoscaling latency."),
        "comp4": ("Operational Excellence Pillar", "CI/CD & Observability", "control", "Automates release pipelines, progressive rollouts, and blameless post-mortems."),
        "flow1": "Engineering team submits proposed workload blueprint to Architecture Review Board.",
        "flow2": "Design is audited against each pillar: identifying single points of failure, security risks, and cost anomalies.",
        "flow3": "Trade-offs are explicitly quantified and recorded in an Architecture Decision Record (ADR).",
        "fail": "Security team mandates double-hop inspection proxies that introduce 300ms latency, violating performance SLA.",
        "heal": "Architect refactors network flow to use Cloud Armor and Private Service Connect, eliminating the proxy bottleneck.",
        "city_concept": "The Six Municipal Building Standards",
        "p1": "Cloud City grew haphazardly: bridges were strong but too narrow, water pipes leaked, and building permits took six months.",
        "p2": "Mayor Meridian established the Six Standards of Civic Design: Structural Safety, Fire Defense, Clean Water, Budget Balance, Fast Transit, and Public Parks.",
        "p3": "When a gold-plated fountain drained the city treasury, the Finance Bureau invoked the Budget Pillar to substitute sustainable local stone.",
        "p4": "Civic construction requires decades of physical re-engineering; in GCP, architectural pillars are maintained through automated policy guardrails.",
        "part1_html": """
        <h3>The Situation: Moving Beyond Guesswork</h3>
        <p>
          Without an architectural standard, every engineering team in an enterprise invents their own practices. Team A deploys everything in a single zone to save money (ignoring Reliability). Team B adds six redundant load balancers and third-party firewalls that balloon costs (ignoring Cost Optimization).
        </p>
        <p>
          The <strong>Google Cloud Architecture Framework</strong> provides an authoritative blueprint across six core pillars:
        </p>
        <div class="callout">
          <div class="callout-title">The 6 Pillars of the Architecture Framework</div>
          <ol>
            <li><strong>System Design:</strong> Foundation of your cloud architecture—geography, zones, naming conventions, and sustainability.</li>
            <li><strong>Operational Excellence:</strong> Deploying, running, and monitoring workloads efficiently using automation and CI/CD.</li>
            <li><strong>Security, Privacy, and Compliance:</strong> Protecting data, identities, networks, and workloads with zero trust.</li>
            <li><strong>Reliability:</strong> Designing resilient systems that withstand failures and automatically heal.</li>
            <li><strong>Cost Optimization:</strong> Maximizing business value while minimizing unnecessary cloud spend.</li>
            <li><strong>Performance Optimization:</strong> Tuning compute, network, and storage to meet throughput and latency goals.</li>
          </ol>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Understanding the Pillars</h4>
        <p>Each pillar provides actionable checklists, anti-patterns to avoid, and Google-recommended architectural patterns.</p>
        <h4>Layer 2 — Practitioner: Managing Conflicts Between Pillars</h4>
        <p>Pillars naturally conflict: high reliability (multi-region active-active) increases cost; deep security packet inspection increases latency. Architects must document these trade-offs explicitly.</p>
        <h4>Layer 3 — Architect: Architecture Review Automation</h4>
        <p>Using Google Cloud Architecture Center tools, Cloud Health Assessments, and Security Command Center to validate pillar compliance continuously.</p>
        <h4>Layer 4 — Staff: Enterprise Standardization & Governance</h4>
        <p>Staff architects codify pillar rules into Terraform modules, Organization Policies, and automated CI/CD policy-as-code linters.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, inspectors audit every new skyscraper against municipal safety, energy efficiency, and emergency evacuation guidelines.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Pillar Trade-Off Analysis</div>
          <p>
            A startup is designing an image-processing service. They propose running 100 preemptible/Spot VMs across 3 zones behind an internal queue with autohealing.
          </p>
          <p>Analyze this proposal across the <strong>Reliability</strong>, <strong>Cost Optimization</strong>, and <strong>Operational Excellence</strong> pillars. What are the key risks and mitigations?</p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Trade-Off Analysis Solution</h4>
          <ul>
            <li><strong>Cost Optimization:</strong> Spot VMs save 60-91% compared to on-demand instances; ideal for stateless queue processing.</li>
            <li><strong>Reliability:</strong> Spot VMs can be reclaimed with 30 seconds notice. Mitigation: Use idempotent message acknowledgments (Pub/Sub) and spread across 3 zones to prevent mass eviction.</li>
            <li><strong>Operational Excellence:</strong> Implement automated graceful shutdown hooks on <code>SIGTERM</code> to requeue in-flight tasks cleanly.</li>
          </ul>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Framework Trade-offs (Question 1)</span>
          <p><strong>An architect is designing an analytics ingestion pipeline. The team needs to balance Cost Optimization against Reliability. The data is non-critical telemetry that can be replayed from the source edge devices if an outage occurs. Which design best adheres to the framework?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! For fault-tolerant batch workloads with replayable upstream sources, Spot VMs and single-region managed services optimize cost without violating business needs.')">A) Use Cloud Run or Spot VM workers in a single region with autoscaling, accepting transient interruption.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Multi-region active-active Spanner is excessively costly for replayable non-critical telemetry.')">B) Deploy multi-region Cloud Spanner instances across 3 continents with active-active routing.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Sole-tenant nodes are significantly more expensive and intended for compliance/licensing isolation.')">C) Provision dedicated sole-tenant nodes with 3-year committed use discounts.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Manual provisioning violates the Operational Excellence pillar and increases operational overhead.')">D) Manually provision unmanaged Compute Engine instances with static IP addresses.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/architecture/framework/operational-excellence' target='_blank'>Architecture Framework: Operational Excellence</a></li><li><a href='https://cloud.google.com/architecture/framework/cost-optimization' target='_blank'>Architecture Framework: Cost Optimization</a></li></ul>"
    },

    # 024: Reference Architectures and Patterns
    {
        "topic_no": "024",
        "roadmap_id": "3.3",
        "title": "Reference Architectures & Enterprise Design Patterns",
        "page_type": "concept",
        "phase": "Phase 3 — Architecture Thinking",
        "lead": "Canonical cloud blueprints: Three-tier web applications, event-driven reactive microservices, multi-region active-active vs active-passive, and enterprise landing zone hubs.",
        "comp1": ("Global Anycast Ingress", "Cloud CDN / Armor", "data", "Terminates client TLS at Google's edge, mitigates DDoS attacks, and caches static assets."),
        "comp2": ("Application Microservices", "GKE / Cloud Run", "data", "Stateless container services running auto-scaled business logic across multiple zones."),
        "comp3": ("Transactional Persistence", "Cloud Spanner / SQL", "data", "Relational database tier maintaining ACID guarantees and read replica offload."),
        "comp4": ("Event Fabric & Telemetry", "Pub/Sub & Logging", "control", "Decouples asynchronous service events and aggregates real-time metrics."),
        "flow1": "Global external HTTPS traffic hits edge Anycast IP and is routed to closest healthy regional backend.",
        "flow2": "Stateless container pods authenticate internal service-to-service calls using Workload Identity and mTLS.",
        "flow3": "Transactional records are committed to the database while domain events are published asynchronously to Pub/Sub.",
        "fail": "Primary database zone suffers physical power interruption.",
        "heal": "Managed HA database initiates automated failover to standby replica in secondary zone within 60 seconds.",
        "city_concept": "City Hub, Spoke & Ring Highway Architecture",
        "p1": "Every shop in Brightloaf tried to route delivery trucks directly through the narrow town square, causing complete gridlock.",
        "p2": "City Planner Nora designed an outer beltway (Global Load Balancer) and neighborhood logistics hubs (Microservice pods with local delivery vans).",
        "p3": "When a main bridge collapsed, automated traffic lights diverted trucks to the eastern bypass without a single package being dropped.",
        "p4": "Physical city highway expansion takes a decade; software traffic routing topologies can be reconfigured in seconds via software-defined DNS and BGP.",
        "part1_html": """
        <h3>The Situation: The Value of Proven Blueprints</h3>
        <p>
          Architectural patterns are reusable solutions to commonly occurring problems. Rather than designing every cloud system from a blank sheet of paper, architects rely on battle-tested reference architectures developed by Google Cloud engineering.
        </p>
        <p>
          Whether building an e-commerce platform, a real-time IoT ingestion engine, or an enterprise SaaS product, understanding core structural patterns ensures high availability, security isolation, and horizontal scalability by default.
        </p>
        <div class="callout">
          <div class="callout-title">Core Enterprise Architectural Patterns</div>
          <ul>
            <li><strong>Three-Tier Web Architecture:</strong> Presentation (Cloud CDN / LB), Logic (Cloud Run / GKE), and Persistence (Cloud SQL / Spanner).</li>
            <li><strong>Event-Driven Microservices:</strong> Ingestion via Pub/Sub, processing via Cloud Tasks & Eventarc, asynchronous decoupling.</li>
            <li><strong>Multi-Region Active-Active:</strong> Stateless compute running concurrently in 2+ regions fronted by Global External Application LB.</li>
            <li><strong>Shared VPC Enterprise Landing Zone:</strong> Central networking hub project hosting Shared VPC subnets, connecting spoke projects with strict IAM separation.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Decoupling & Statelessness</h4>
        <p>Compute nodes must remain strictly stateless. Session state, user carts, and transient uploads must be stored in Redis (Memorystore) or object storage (Cloud Storage).</p>
        <h4>Layer 2 — Practitioner: Multi-Region Active-Active vs Active-Passive</h4>
        <p>Active-active routes live traffic to both regions simultaneously, offering near-zero RTO. Active-passive keeps a warm or cold standby region, requiring DNS or LB cutover during regional disaster.</p>
        <h4>Layer 3 — Architect: Multi-Tenant SaaS Isolation Patterns</h4>
        <p>Isolating tenants by GCP project (highest isolation, compliance-friendly), by Kubernetes namespace (moderate isolation, high resource density), or by row-level database security tags.</p>
        <h4>Layer 4 — Staff: Anti-Pattern Detection & Eradication</h4>
        <p>Identifying anti-patterns: chatty synchronous cross-region database queries, monolithic shared databases across autonomous services, and missing circuit breakers.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Nora maps ring roads, subway lines, and distribution warehouses to keep commerce flowing smoothly.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Anti-Pattern Identification</div>
          <p>
            Review the following architecture: <em>"A mobile app connects directly to a single Compute Engine VM public IP running MySQL, Redis, and Python Django in us-central1-a. Nightly backups are written to the root disk."</em>
          </p>
          <p>List 4 critical architectural flaws and provide the modern GCP reference architecture replacement for each.</p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Remediation Solution</h4>
          <ol>
            <li><strong>Single Point of Failure (SPOF):</strong> Replace single VM with a Regional Managed Instance Group (MIG) or Cloud Run behind an External Application Load Balancer.</li>
            <li><strong>Co-located State & Monolith:</strong> Externalize MySQL to Cloud SQL Regional HA and Redis to Memorystore.</li>
            <li><strong>Public IP Direct Ingress:</strong> Place compute in private subnets with no public IPs; use Cloud NAT for egress and Load Balancer with Cloud Armor for ingress.</li>
            <li><strong>Local Root Disk Backups:</strong> Store automated backups and point-in-time recovery archives in Cloud Storage with cross-region dual-region replication.</li>
          </ol>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Reference Architectures (Question 1)</span>
          <p><strong>An e-commerce business needs to modernize its monolithic web application to support rapid global expansion. The solution must support independent microservice team deployments, eliminate single points of failure, and offer lowest operational maintenance. Which architecture should you recommend?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Global External Application LB with Cloud Run services provides serverless container execution, zero ops overhead, independent rollouts, and automatic multi-zone high availability.')">A) Global External Application Load Balancer routing to independent Cloud Run container services backed by Cloud SQL Regional HA.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Single unmanaged VMs in one zone represent a severe single point of failure with high maintenance.')">B) Single Compute Engine VM in us-central1 running Docker Compose and local PostgreSQL.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Self-managed Kubernetes on bare compute instances incurs massive operational patching overhead.')">C) Self-managed Kubernetes on unmanaged Compute Engine instances with persistent disks.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'App Engine standard does not offer the same multi-service container portability and modern Cloud Deploy integration.')">D) App Engine standard environment with local sqlite databases.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/architecture' target='_blank'>Google Cloud Architecture Center</a></li><li><a href='https://cloud.google.com/architecture/landing-zones' target='_blank'>Landing Zone Design on Google Cloud</a></li></ul>"
    },

    # 025: Migration and Modernisation
    {
        "topic_no": "025",
        "roadmap_id": "3.4",
        "title": "Migration & Modernization: The 6 Rs & Wave Planning",
        "page_type": "concept",
        "phase": "Phase 3 — Architecture Thinking",
        "lead": "Strategic workload transitions: The 6 Rs (Rehost, Replatform, Refactor, Repurchase, Retire, Retain), Migration Center discovery, Database Migration Service, and Strangler Fig cutover.",
        "comp1": ("On-Premises Datacenter", "Legacy VMware / DB", "data", "Physical servers, SAN storage, and monolithic SQL databases hosting corporate systems."),
        "comp2": ("Migration Center & Discovery", "Inventory Tool", "control", "Discovers asset inventory, dependency graphs, performance utilization, and TCO estimates."),
        "comp3": ("Migration Pipelines", "M2VM / DMS / STS", "control", "Automates continuous replication of VM blocks, database change logs, and object storage."),
        "comp4": ("Google Cloud Target VPC", "Target Foundation", "data", "Target environment with Landing Zone guardrails, Shared VPC, and managed databases."),
        "flow1": "Discovery agents scan on-premises inventory, mapping interconnect dependencies and server utilization.",
        "flow2": "Workloads are categorized into migration waves based on complexity and dependency graphs.",
        "flow3": "Continuous replication keeps target cloud databases and disks in sync until scheduled cutover window.",
        "fail": "Cutover fails during maintenance window due to unexpected hard-coded IP dependency in legacy application.",
        "heal": "Migration team triggers immediate DNS rollback and updates application config via Cloud DNS policy before next attempt.",
        "city_concept": "City Relocation & Historic District Restoration",
        "p1": "The old industrial waterfront was sinking. Factories had rusty boilers, proprietary plumbing, and no electrical schematics.",
        "p2": "Urban Planners categorized every factory: some to move brick-by-brick (Rehost), some to upgrade with modern boilers (Replatform), and some to demolish completely (Retain/Retire).",
        "p3": "During the hospital relocation, power was kept active in both the old clinic and new hospital simultaneously until the final patient was moved.",
        "p4": "Moving brick factories takes years; cloud migrations can replicate petabytes of data over high-speed Interconnect in days.",
        "part1_html": """
        <h3>The Situation: The 6 Rs of Cloud Migration</h3>
        <p>
          Organizations rarely move to Google Cloud by rewriting everything from scratch overnight. Attempting a "Big Bang" migration is the single highest-risk endeavor in IT. Successful cloud architects use the <strong>6 Rs framework</strong> to determine the optimal strategy for each application:
        </p>
        <div class="callout">
          <div class="callout-title">The 6 Rs Migration Strategies</div>
          <ul>
            <li><strong>Rehost (Lift and Shift):</strong> Move VMs as-is to Compute Engine without code changes using Migrate to Virtual Machines (M2VM). Quickest path to exit a datacenter.</li>
            <li><strong>Replatform (Lift, Tinker, and Shift):</strong> Modernize the runtime without changing core code (e.g., move self-hosted MySQL to Cloud SQL, or package an app into a container for Cloud Run).</li>
            <li><strong>Refactor / Re-architect:</strong> Rewrite applications using cloud-native services (microservices on GKE, Pub/Sub, Spanner, Serverless). Highest business agility.</li>
            <li><strong>Repurchase (Drop and Shop):</strong> Replace bespoke software with commercial SaaS (e.g., moving self-hosted email to Google Workspace, or custom CRM to Salesforce).</li>
            <li><strong>Retire:</strong> Identify and decommission obsolete servers and applications that are no longer used (often 10-20% of an enterprise inventory).</li>
            <li><strong>Retain (Revisit):</strong> Keep workloads on-premise temporarily due to legacy dependencies, active hardware amortization, or regulatory sovereignty constraints.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Discovery & Assessment (Migration Center)</h4>
        <p>Use Google Cloud Migration Center to inventory servers, track actual CPU/RAM utilization, identify oversized machines, and model Total Cost of Ownership (TCO).</p>
        <h4>Layer 2 — Practitioner: Data & Database Migration Mechanics</h4>
        <p>Use <strong>Database Migration Service (DMS)</strong> for minimal downtime replication of MySQL/PostgreSQL/Oracle to Cloud SQL/AlloyDB. Use <strong>Storage Transfer Service (STS)</strong> for large-scale object migration.</p>
        <h4>Layer 3 — Architect: Cutover Strategies & The Strangler Fig Pattern</h4>
        <p>Avoid big-bang cutovers. Use the Strangler Fig pattern: place an API Gateway in front of legacy systems and peel off individual routes to cloud microservices incrementally.</p>
        <h4>Layer 4 — Staff: Wave Planning & Rollback Engineering</h4>
        <p>Grouping workloads into migration waves (Wave 0: Landing Zone & Pilot; Wave 1: Non-critical internal apps; Wave 2: Core business services; Wave 3: Complex databases). Every wave requires a documented, tested rollback plan.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Nora schedules infrastructure upgrades neighborhood by neighborhood, ensuring water and power remain on 24/7.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Database Migration Service Readiness Assessment</div>
          <p>Simulate verifying on-premises MySQL binary logging configuration for Database Migration Service continuous replication.</p>
        </div>
        <pre><code class="language-bash"># 1. Verify binlog format on source database
SHOW VARIABLES LIKE 'binlog_format';
# Must return: ROW

# 2. Check retention hours for binlog replication
SHOW VARIABLES LIKE 'expire_logs_days';

# 3. Create replication service account with REPLICATION SLAVE privileges
CREATE USER 'dms_replicator'@'%' IDENTIFIED BY 'SecurePassw0rd!';
GRANT REPLICATION SLAVE, SELECT, RELOAD, REPLICATION CLIENT ON *.* TO 'dms_replicator'@'%';
FLUSH PRIVILEGES;

# 4. In GCP: verify connection profile via gcloud
gcloud database-migration connection-profiles create mysql source-db-profile \\
    --provider=ON_PREMISES \\
    --display-name="On-Premises Production MySQL" \\
    --host="203.0.113.10" \\
    --port=3306 \\
    --username="dms_replicator" \\
    --region="us-central1"</code></pre>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Migration Strategy (Question 1)</span>
          <p><strong>A company needs to vacate a leased colocation datacenter within 60 days. They run 400 VMware virtual machines and multiple legacy databases with customized OS kernels. They want to minimize risk and meet the deadline. Which migration strategy should the architect recommend?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Rehosting (lift-and-shift) using Migrate to Virtual Machines or Google Cloud VMware Engine (GCVE) provides the fastest, lowest-risk datacenter evacuation path without requiring immediate application rewrites.')">A) Rehost using Migrate to Virtual Machines (M2VM) or Google Cloud VMware Engine (GCVE) to meet the tight deadline, modernizing later.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Refactoring 400 apps into microservices takes months or years, causing them to miss the 60-day lease deadline.')">B) Completely refactor all 400 workloads into serverless microservices on Cloud Run before cutover.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Repurchasing requires vendor RFPs and contract negotiations that exceed 60 days.')">C) Repurchase commercial SaaS replacements for all applications immediately.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Retaining workloads in the datacenter directly violates the mandate to vacate within 60 days.')">D) Retain all systems on-premise and purchase replacement hardware.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/migration-center/docs' target='_blank'>Google Cloud Migration Center Documentation</a></li><li><a href='https://cloud.google.com/database-migration' target='_blank'>Database Migration Service (DMS)</a></li></ul>"
    },

    # 026: Decision-Making Frameworks & ADRs
    {
        "topic_no": "026",
        "roadmap_id": "3.4b",
        "title": "Decision-Making Frameworks: ADRs & Trade-Off Matrices",
        "page_type": "concept",
        "phase": "Phase 3 — Architecture Thinking",
        "lead": "Rigorous architectural evaluation: Build vs Buy vs Managed, weighted decision scorecards, Architecture Decision Records (ADRs), and Total Cost of Ownership (TCO) comparisons.",
        "comp1": ("Architectural Context", "Business Problem", "control", "Documents the business scenario, regulatory constraints, and functional requirements driving a decision."),
        "comp2": ("Alternative Options Evaluated", "Trade-Off Matrix", "control", "Evaluates Option A, Option B, and Option C against weighted architectural criteria."),
        "comp3": ("Architecture Decision Record (ADR)", "Versioned Git Doc", "control", "Formal immutable record of Context, Decision, Consequences, and Alternatives Considered."),
        "comp4": ("Implementation Verification", "Deployed Systems", "data", "Validates that the chosen architecture satisfies the predicted performance and cost metrics."),
        "flow1": "Architect identifies critical technical fork (e.g., self-hosted Kafka on GKE vs fully managed Cloud Pub/Sub).",
        "flow2": "Team drafts weighted trade-off matrix scoring operational overhead, throughput, latency, and TCO.",
        "flow3": "Formal ADR is committed to Git repository with explicit positive and negative consequences signed off by leads.",
        "fail": "A new team lead attempts to revert an architectural decision without understanding historical constraints.",
        "heal": "Team references the versioned ADR in Git, clarifying why the current choice was made and what conditions permit revisiting it.",
        "city_concept": "City Council Charters & Municipal Archives",
        "p1": "New city council members kept overturning decisions made two years earlier, wasting millions tearing down newly built tram lines.",
        "p2": "City Archivist Arthur established the Municipal Charter Log (ADRs). Every major bridge or rail decision was recorded with reasons, cost projections, and alternatives.",
        "p3": "When a contractor asked why the city chose stone over steel for the seawall, Arthur pulled ADR #14 showing steel rusted in the saltwater bay.",
        "p4": "Municipal paper records can be lost in fires; digital Git-versioned ADRs provide permanent, searchable institutional memory.",
        "part1_html": """
        <h3>The Situation: Why Architecture Decision Records Matter</h3>
        <p>
          In high-velocity engineering organizations, the question <em>"Why did we build it this way?"</em> is asked constantly. Without formal documentation, the context behind critical decisions is lost when senior engineers change teams or companies.
        </p>
        <p>
          An <strong>Architecture Decision Record (ADR)</strong> is a lightweight text document that captures an important architectural decision made along with its context and consequences. Committing ADRs to source control alongside code creates an immutable audit trail of technical leadership.
        </p>
        <div class="callout">
          <div class="callout-title">Standard ADR Anatomy (Michael Nygard Template)</div>
          <ol>
            <li><strong>Title:</strong> Short noun phrase with sequential ID (e.g., <code>ADR-004: Use Cloud Pub/Sub for Asynchronous Order Ingestion</code>).</li>
            <li><strong>Status:</strong> Proposed, Accepted, Rejected, Deprecated, or Superseded.</li>
            <li><strong>Context:</strong> The business context, forces at play, and constraints that motivated the decision.</li>
            <li><strong>Decision:</strong> The change that we are committing to make.</li>
            <li><strong>Consequences:</strong> The outcome of the decision—both positive benefits and negative trade-offs.</li>
            <li><strong>Alternatives Considered:</strong> Other options explored and specific reasons why they were rejected.</li>
          </ol>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Build vs Buy vs Managed Service</h4>
        <p>Engineers love to build. Architects evaluate total lifecycle costs: building custom infrastructure requires 24/7 on-call rotations, security patching, and upgrades that detract from core business differentiation.</p>
        <h4>Layer 2 — Practitioner: Weighted Decision Matrices</h4>
        <p>Score options mathematically: assign weights to criteria (Operational Simplicity: 30%, Cost: 25%, Latency: 25%, Portability: 20%). Multiply scores (1-5) by weights to eliminate emotional bias.</p>
        <h4>Layer 3 — Architect: TCO & Reversibility (One-Way vs Two-Way Doors)</h4>
        <p>Jeff Bezos popularized "Type 1" (irreversible, one-way doors like database engine selection) vs "Type 2" (reversible, two-way doors like VM instance sizing). Spend deep analytical time on Type 1 decisions.</p>
        <h4>Layer 4 — Staff: Managing Technical Debt & Superseding ADRs</h4>
        <p>As business scale changes, architectures must evolve. When revisiting a decision, never edit the original ADR—create a new ADR that explicitly <em>Supersedes ADR-004</em>.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Archivist Arthur preserves every council resolution in the public archives so future builders understand why foundations were laid.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Write an ADR</div>
          <p>
            Write a complete ADR for Brightloaf Bakery deciding between <strong>Cloud SQL for PostgreSQL</strong> vs <strong>Cloud Spanner</strong> for their new regional loyalty rewards program (projected 200 writes/second, 1 TB total storage, budget constraint of $300/month).
          </p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Sample ADR: Loyalty Rewards Persistence</h4>
          <p><strong>Title:</strong> ADR-012: Select Cloud SQL for PostgreSQL for Loyalty Service</p>
          <p><strong>Status:</strong> Accepted</p>
          <p><strong>Context:</strong> Loyalty service requires relational ACID transactions at 200 writes/sec with 1 TB storage. Monthly infrastructure budget is strictly capped at $300.</p>
          <p><strong>Decision:</strong> We will deploy Cloud SQL for PostgreSQL with Regional HA (db-custom-4-16) and automated cross-zone failover.</p>
          <p><strong>Consequences:</strong> Positive: Fits well within budget (~$180/mo); fully managed backups; standard Postgres SQL support. Negative: Limited to vertical scaling if traffic exceeds 10,000 writes/sec.</p>
          <p><strong>Alternatives Rejected:</strong> Cloud Spanner rejected because minimum cost (~$600+/month) exceeds the budget constraint, and extreme multi-region horizontal scaling is unnecessary for this workload.</p>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Architectural Decision Making (Question 1)</span>
          <p><strong>When evaluating whether to build a self-managed messaging cluster on Compute Engine versus adopting Google Cloud Pub/Sub, what is the primary consideration from an enterprise Total Cost of Ownership (TCO) perspective?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! TCO includes ongoing operational toil: OS patching, cluster rebalancing, broker sizing, disk management, and on-call engineering hours.')">A) Cloud Pub/Sub eliminates ongoing engineering operational overhead for patching, cluster maintenance, and broker capacity management.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Raw Compute Engine VM hardware costs are often lower per raw byte, but engineering maintenance dwarfs the hardware savings.')">B) Compute Engine VMs are always more expensive per GB transferred than managed serverless messaging.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud Pub/Sub has an SLA of 99.95%, but high availability is not the only TCO dimension.')">C) Cloud Pub/Sub provides an absolute 100% SLA guarantee.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Self-managed clusters can be deployed across zones manually.')">D) Compute Engine cannot be deployed in multiple availability zones.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/architecture/framework/system-design' target='_blank'>Architecture Framework: System Design Pillar</a></li><li><a href='https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions' target='_blank'>Documenting Architecture Decisions (Michael Nygard)</a></li></ul>"
    },

    # 027: Diagramming and Documentation
    {
        "topic_no": "027",
        "roadmap_id": "3.5",
        "title": "Diagramming & Documentation: C4 Model & Visual Standards",
        "page_type": "concept",
        "phase": "Phase 3 — Architecture Thinking",
        "lead": "Visual communication for cloud architects: The C4 Model (Context, Container, Component, Code), network topology flows, data lineage diagrams, and Mermaid/draw.io standards.",
        "comp1": ("System Context (Level 1)", "High-Level Boundary", "control", "Shows how users, external partner APIs, and enterprise systems interact with the cloud solution."),
        "comp2": ("Container Diagram (Level 2)", "Subsystems & Storage", "control", "Maps applications, databases, microservices, and network boundaries across GCP regions."),
        "comp3": ("Component Diagram (Level 3)", "Internal Structure", "data", "Details internal components inside a single container (controllers, repositories, services)."),
        "comp4": ("Living Architecture Repo", "Documentation as Code", "control", "Stores diagrams as code (Mermaid/PlantUML) in Git alongside Terraform infrastructure."),
        "flow1": "Architect draws Level 1 Context diagram to align executive stakeholders on project scope.",
        "flow2": "Architect expands into Level 2 Container diagram depicting GCP VPCs, subnets, GKE clusters, and Cloud SQL.",
        "flow3": "Developers and SREs use Level 3 Component diagrams to implement secure API endpoints and CI/CD pipelines.",
        "fail": "Diagram is drawn with ambiguous lines, missing protocols, unlabelled arrows, and no trust boundary markers.",
        "heal": "Architect applies C4 visual standards: labeling every edge with protocol (HTTPS/gRPC) and demarcating private vs public subnets.",
        "city_concept": "City Blueprints & Geological Survey Maps",
        "p1": "A construction crew built an electrical substation on top of the main freshwater aqueduct because they were working from a tourist cartoon map.",
        "p2": "The Chief Surveyor instituted layered blueprints: Level 1 City Overview, Level 2 District Utilities, Level 3 Building Schematics.",
        "p3": "During a gas leak emergency, repair crews pulled the Level 2 utility schematic and located the shutoff valve in 90 seconds.",
        "p4": "Paper blueprints fade and tear; modern diagrams-as-code are version-controlled, automated, and permanently accurate.",
        "part1_html": """
        <h3>The Situation: The Danger of Ambiguous Architecture Diagrams</h3>
        <p>
          Almost every failed cloud deployment can be traced back to an ambiguous diagram. A white box labeled "API" connected by an unlabelled arrow to another white box labeled "Database" hides dozens of critical questions:
        </p>
        <ul>
          <li>What protocol is used? (HTTPS, gRPC, raw TCP?)</li>
          <li>Is the connection authenticated, encrypted in transit (TLS 1.3), or traversing the public internet?</li>
          <li>What happens when the database is unreachable? (Retry? Circuit break? Failover?)</li>
          <li>Which GCP project, VPC, region, and security perimeter does each service belong to?</li>
        </ul>
        <p>
          Professional cloud architects use structured methodologies like the <strong>C4 Model</strong> and diagrammatic standards to communicate unambiguous technical designs.
        </p>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: The C4 Model (Zoom Levels)</h4>
        <p>Created by Simon Brown, C4 provides 4 zoom levels: <strong>Context</strong> (people and systems), <strong>Containers</strong> (deployable units like Cloud Run, GKE pods, Cloud SQL), <strong>Components</strong> (internal software modules), and <strong>Code</strong> (class diagrams).</p>
        <h4>Layer 2 — Practitioner: Network & Data Flow Standards</h4>
        <p>Every arrow must have a clear direction, explicit label, and protocol (e.g., <code>HTTPS / OAuth 2.0 (Port 443)</code>). Group components into clear visual perimeters: External, VPC, Regional Subnet, and Database Tier.</p>
        <h4>Layer 3 — Architect: Sequence Diagrams for Failure Scenarios</h4>
        <p>Static diagrams only show the happy path. Architects produce UML sequence diagrams illustrating failure scenarios: timeouts, primary zone crashes, circuit breakers tripping, and health check rerouting.</p>
        <h4>Layer 4 — Staff: Diagrams as Code (Mermaid & PlantUML)</h4>
        <p>Storing diagrams as text in Git alongside code. Pull requests update both the Terraform code and the Mermaid diagram simultaneously, preventing documentation drift.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Nora's multi-layered blueprints allow city engineers to zoom from the entire metropolitan area down to individual water valves.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Diagrams as Code with Mermaid</div>
          <p>Examine the following Mermaid code block. It represents a secure 3-tier GCP web architecture. Review the diagram syntax.</p>
        </div>
        <pre><code class="language-mermaid">graph TD
    Client[Internet Clients] -->|HTTPS 443| LB[Global External ALB]
    LB -->|mTLS / Port 8080| GKE[GKE Autopilot Workload Pods]
    GKE -->|Private Service Connect| SQL[(Cloud SQL PostgreSQL HA)]
    GKE -->|Async Event| PS[Cloud Pub/Sub Topic]
    PS -->|Push Subscription| CR[Cloud Run Worker]
    
    subgraph VPC [Custom Global VPC]
        subgraph SubnetApp [Regional Subnet: 10.0.1.0/24]
            GKE
        end
        subgraph SubnetDB [Managed Service Subnet]
            SQL
        end
    end</code></pre>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Diagramming Standards (Question 1)</span>
          <p><strong>When presenting a cloud architecture design to both security auditors and executive stakeholders, which diagramming approach best ensures clarity and compliance?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! The C4 model provides distinct levels of abstraction: Level 1 Context for executives, and Level 2 Container/VPC topologies with explicit protocols and security perimeters for auditors.')">A) Use the C4 model to provide a Level 1 System Context diagram for executives, and Level 2 Container diagrams with explicit network protocols and VPC perimeters for auditors.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'A single massive diagram containing every low-level detail overwhelms executives and obscures business context.')">B) Put every single VM, IP address, and software library into a single diagram for all audiences.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Omitting protocol labels creates ambiguity and fails security audits.')">C) Omit protocol names and port numbers to keep diagrams uncluttered for auditors.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Unstructured whiteboard photos are not auditable or reproducible engineering artifacts.')">D) Rely exclusively on informal hand-drawn whiteboard photos stored in chat channels.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://c4model.com/' target='_blank'>The C4 Model for Visualising Software Architecture</a></li><li><a href='https://cloud.google.com/architecture/diagrams' target='_blank'>Google Cloud Architecture Diagramming Tools & Icons</a></li></ul>"
    }
]

def main():
    print(f"Building Phase 3 (Topics 022 to 027) - {len(PHASE3_TOPICS)} topics...")
    for item in PHASE3_TOPICS:
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
