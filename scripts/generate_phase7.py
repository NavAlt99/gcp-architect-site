#!/usr/bin/env python3
"""
generate_phase7.py - Generates Topics 045 to 050 covering Phase 7: Case Study Analysis and Exam Prep.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_website import build_topic_page
from batch_generate_full import make_d1_map, make_d2_flow, make_d3_failure, make_analogy

PHASE7_TOPICS = [
    # 045: Case Analysis Method & Discovery Framework
    {
        "topic_no": "045",
        "roadmap_id": "7.1",
        "title": "Case Analysis Method: The 6-Step Architect Discovery Framework",
        "page_type": "concept",
        "phase": "Phase 7 — Case Studies & Exam Prep",
        "lead": "The professional consulting playbook: Extracting hidden requirements, separating stated needs from implied needs, mapping constraints to GCP capabilities, and rejecting inferior alternatives.",
        "comp1": ("Customer Problem Brief", "Case Narrative", "control", "Raw business requirements, regulatory mandates, and legacy system constraints."),
        "comp2": ("Architect Discovery Engine", "6-Step Methodology", "control", "Analyzes business goals, technical requirements, watchpoints, and trade-offs."),
        "comp3": ("Proposed Target Blueprint", "GCP Solution Design", "data", "Formulates defended architectural choices with documented rationale."),
        "comp4": ("Rejected Alternatives Log", "ADR & Justification", "control", "Documents explicit technical reasons why alternative options were discarded."),
        "flow1": "Architect highlights every number (RPS, TB, users, latency, budget) and adjective ('global', 'spiky', 'legacy').",
        "flow2": "Discovery framework categorizes constraints: regulatory compliance (HIPAA/PCI), data sovereignty, and team skills.",
        "flow3": "Architect produces defended architecture blueprint with explicit alternative elimination rationale.",
        "fail": "Architect proposes technology based on hype without mapping directly to customer's stated requirements.",
        "heal": "Framework forces review against the 6-Step checklist, eliminating unjustified complexity.",
        "city_concept": "City Court of Inquest & Grand Architectural Jurors",
        "p1": "Builders were proposing ornate marble bridges across dry riverbeds while crowded slums lacked clean drinking water.",
        "p2": "The Grand Inquest established the Six Civic Questions: Purpose, Budget, Flood Lines, Risks, Blueprint, and Rejected Ideas.",
        "p3": "When a builder proposed a gilded clocktower, the jury rejected it because the city water aqueduct was sinking.",
        "p4": "Civic jury hearings take months; architectural discovery frameworks produce clear decision scorecards in hours.",
        "part1_html": """
        <h3>The Situation: How Enterprise Architects Read Case Studies</h3>
        <p>
          Whether presenting to a Fortune 500 board or taking the Google Professional Cloud Architect (PCA) exam, success depends on one skill: <strong>deconstructing business ambiguity into defensible technical decisions</strong>.
        </p>
        <p>
          Every successful architecture evaluation follows the <strong>6-Step Case Analysis Method</strong>:
        </p>
        <div class="callout">
          <div class="callout-title">The 6-Step Analysis Sequence</div>
          <ol>
            <li><strong>Business Goals:</strong> What does business success look like? (e.g. Expand to 5 new international markets, reduce operational cost by 40%, meet IPO timeline).</li>
            <li><strong>Constraints:</strong> What boundaries cannot be changed? (e.g. Fixed budget, HIPAA compliance, 9-month migration deadline, team only knows Python/SQL).</li>
            <li><strong>Technical Requirements:</strong> Quantitative specifications (e.g. 100,000 peak RPS, sub-100ms global latency, 99.99% availability, zero data loss RPO=0).</li>
            <li><strong>Risks and Watchpoints:</strong> Conflicting requirements or hidden traps (e.g. Compliance demands data residency in Europe, but business wants global replication).</li>
            <li><strong>Proposed Architecture:</strong> Selected GCP services with an explicit justification for each component.</li>
            <li><strong>Alternatives Rejected:</strong> Explicit reasons why plausible alternative technologies were deliberately eliminated.</li>
          </ol>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Underlining Numbers and Adjectives</h4>
        <p>In every case prompt, underline every number (e.g., <em>"50,000 vehicles", "every 2 seconds", "10 TB/day"</em>) and every adjective (e.g., <em>"real-time", "bursty", "legacy", "regulated"</em>). Adjectives conceal hidden non-functional requirements.</p>
        <h4>Layer 2 — Practitioner: Spotting "Watchpoints" and Traps</h4>
        <p>Watch for conflicting needs: <em>"Minimize operational overhead"</em> points to managed serverless (Cloud Run, Spanner), while <em>"Lowest compute hardware cost"</em> points to Spot VMs and Compute Engine.</p>
        <h4>Layer 3 — Architect: Defending the "Why" (The Justification Principle)</h4>
        <p>Never recommend a service without attaching a business reason: e.g., <em>"We selected Cloud Spanner not just because it is relational, but because the business requires multi-region 99.999% availability with synchronous consistency."</em></p>
        <h4>Layer 4 — Staff: Executive Storytelling & Stakeholder Delivery</h4>
        <p>Staff architects deliver recommendations tailored to the audience: presenting financial ROI to the CFO, compliance guardrails to the CISO, and developer velocity to the VP of Engineering.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Nora cross-examines contractors using the 6 Civic Questions before approving municipal bond funding.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Case Study Deconstruction Drill</div>
          <p>Read the excerpt: <em>"A media streaming startup with 10M global users streams live concerts. Peak traffic spikes 20x during shows. Viewers experience buffering in Asia. The engineering team consists of 3 developers who want zero infrastructure maintenance."</em></p>
          <p>Extract: (1) Core business goal, (2) Top 2 technical requirements, (3) Key constraint, (4) Recommended GCP compute & CDN design.</p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Deconstruction Rubric</h4>
          <ol>
            <li><strong>Business Goal:</strong> Deliver smooth global live streaming without user churn.</li>
            <li><strong>Technical Requirements:</strong> Elastic auto-scaling to absorb 20x spikes; low-latency edge delivery to Asia.</li>
            <li><strong>Constraint:</strong> Tiny 3-person team requiring zero infrastructure ops overhead.</li>
            <li><strong>Recommended Design:</strong> Cloud Run (serverless container autoscaling) fronted by Cloud CDN with Media CDN caching at Google's global edge network. Reject self-hosted Kubernetes to avoid operational maintenance.</li>
          </ol>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Case Reading (Question 1)</span>
          <p><strong>When evaluating a case study that states "The development team has deep expertise in PostgreSQL and Docker, but has never managed Kubernetes and must deploy a new product in 6 weeks with minimal ops overhead", which compute and database combination is optimal?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Cloud Run runs existing Docker containers with zero server management, and Cloud SQL provides fully managed PostgreSQL matching existing team skills.')">A) Cloud Run for container deployment and Cloud SQL for PostgreSQL for database persistence.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'GKE Standard introduces a steep Kubernetes learning curve and operational overhead that violates the 6-week timeline.')">B) GKE Standard with a self-managed PostgreSQL cluster on Compute Engine.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Rewriting applications for Spanner schema and query conventions requires extensive retraining that exceeds 6 weeks.')">C) Compute Engine unmanaged VMs with Cloud Spanner.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Bigtable is a NoSQL key-value store, not a relational PostgreSQL replacement.')">D) Cloud Functions with Cloud Bigtable.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/certification/guides/cloud-architect' target='_blank'>Official Google Professional Cloud Architect Exam Guide</a></li><li><a href='https://cloud.google.com/architecture' target='_blank'>Google Cloud Architecture Center Case Studies</a></li></ul>"
    },

    # 046: Case Study: EHR Healthcare
    {
        "topic_no": "046",
        "roadmap_id": "7.4a",
        "title": "Case Study: EHR Healthcare — HIPAA, Legacy DB & Cloud Migration",
        "page_type": "case-study",
        "phase": "Phase 7 — Case Studies & Exam Prep",
        "lead": "Official Case Study Analysis: EHR Healthcare — Modernizing a legacy on-premises healthcare records provider with strict HIPAA compliance, insurance API gateway, Cloud SQL HA, and BigQuery analytics.",
        "comp1": ("Hospital & Clinic Clients", "Partner Ingress", "data", "Sends patient electronic health records and queries insurance benefits over HTTPS APIs."),
        "comp2": ("Apigee API Management", "Enterprise API Gateway", "control", "Enforces OAuth 2.0 authentication, rate limiting, and HIPAA compliance audit logging."),
        "comp3": ("EHR Microservices Fleet", "GKE Regional Cluster", "data", "Runs containerized medical services inside private VPC with zero public IP addresses."),
        "comp4": ("Compliant Health Persistence", "Cloud SQL HA & BigQuery", "data", "CMEK-encrypted relational patient store and de-identified BigQuery research lake."),
        "flow1": "Hospital system authenticates to Apigee gateway; request is validated and rate-limited.",
        "flow2": "Apigee routes call over internal Private Service Connect to private GKE medical service.",
        "flow3": "Transactions commit to Cloud SQL HA with CMEK; de-identified records stream to BigQuery for analytics.",
        "fail": "A legacy insurance partner API in the on-premises datacenter experiences an unannounced outage.",
        "heal": "Cloud Pub/Sub queues transaction requests; Cloud Tasks manages retries with exponential backoff.",
        "city_concept": "City Hospital Network & Secure Medical Archives",
        "p1": "Regional clinics were couriering paper patient charts in unlocked wagons, losing charts and violating patient privacy laws.",
        "p2": "Chief Physician Paul built a pneumatic tube network (Apigee & Private VPC) connecting clinics to the Central Medical Vault.",
        "p3": "When a clinic sent an unsealed request, the pneumatic valve rejected the capsule and alerted the Medical Board.",
        "p4": "Pneumatic tubes are limited by physical air pressure; cloud APIs securely transmit millions of encrypted health records globally.",
        "part1_html": """
        <h3>Case Profile: EHR Healthcare</h3>
        <p>
          <strong>Company Background:</strong> EHR Healthcare is a leading provider of Electronic Health Record software to hospitals, private clinics, and insurance payers. They currently host their monolithic application stack across multiple colocation datacenters with aging hardware.
        </p>
        <div class="callout">
          <div class="callout-title">EHR Healthcare Requirements Breakdown</div>
          <ul>
            <li><strong>Business Goals:</strong> Accelerate integration with third-party healthcare providers, scale during public health surges, reduce datacenter CapEx, and monetize anonymized clinical research data.</li>
            <li><strong>Regulatory Constraints:</strong> Strict <strong>HIPAA</strong> compliance, customer data isolation, encryption in transit and at rest with customer-managed keys (CMEK), 7-year immutable audit log retention.</li>
            <li><strong>Technical Requirements:</strong> 99.99% availability, sub-second API latency, private connectivity to legacy on-premises insurance systems, automated disaster recovery.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Hybrid Connectivity (Cloud HA VPN & Interconnect)</h4>
        <p>Establish dual-tunnel <strong>Cloud HA VPN</strong> or <strong>Dedicated Interconnect</strong> connecting existing datacenters to GCP Shared VPC, enabling private, encrypted database replication without public IP exposure.</p>
        <h4>Layer 2 — Practitioner: Apigee API Management for Payer Integration</h4>
        <p>Deploy <strong>Apigee</strong> as the enterprise API gateway. Apigee manages developer onboarding for external hospitals, validates OAuth 2.0 tokens, enforces rate limiting, and masks sensitive patient identifiers.</p>
        <h4>Layer 3 — Architect: Private GKE & Cloud SQL Regional HA with CMEK</h4>
        <p>Deploy workloads to <strong>Private GKE clusters</strong> with Workload Identity. Relational patient records reside in <strong>Cloud SQL for PostgreSQL Regional HA</strong> with Cloud KMS CMEK encryption and automated cross-zone failover.</p>
        <h4>Layer 4 — Staff: De-Identification & BigQuery Research Data Lake</h4>
        <p>Use <strong>Sensitive Data Protection (Cloud DLP)</strong> to tokenize and de-identify patient names and social security numbers before loading clinical outcomes into BigQuery for researcher queries.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Paul ensures patient records are encrypted inside brass cylinders before dispatch through the pneumatic network.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: EHR Healthcare Exam Defense</div>
          <p>
            An exam question asks: <em>"EHR Healthcare must allow external insurance providers to query patient benefit coverage via REST APIs while enforcing rate limiting, OAuth 2.0 security, and providing analytics on API usage. Which service should you choose?"</em>
          </p>
          <p>Explain why <strong>Apigee</strong> is superior to Cloud Endpoints or API Gateway in this scenario.</p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Defended Answer</h4>
          <p><strong>Apigee</strong> is Google Cloud's enterprise-grade API management platform. It offers advanced developer portals, comprehensive monetization, sophisticated rate-limiting policies, OAuth 2.0 token brokering, and enterprise analytics out of the box. Cloud Endpoints and API Gateway lack enterprise developer portals and advanced rate-limiting/monetization needed for external B2B healthcare partner ecosystems.</p>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Case Study: EHR Healthcare (Question 1)</span>
          <p><strong>EHR Healthcare needs to retain patient access audit logs for 7 years to meet HIPAA compliance. Medical auditors require the ability to run SQL queries against this log archive to investigate historical data breaches. Which architecture meets compliance with minimum cost?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Exporting logs via Log Sink to a BigQuery dataset with long-term partitioned storage and Cloud Storage bucket lock satisfies 7-year retention and allows rapid SQL auditing.')">A) Create an aggregated Cloud Logging sink routing audit logs to BigQuery for SQL analytics, with long-term archive to Cloud Storage with Bucket Lock (WORM).</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Default Cloud Logging storage retains logs for at most 400 days and does not satisfy the 7-year requirement.')">B) Retain logs in default Cloud Logging buckets with no export.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Pub/Sub retention cannot exceed 7 days.')">C) Stream logs into Cloud Pub/Sub with 7-year message retention enabled.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Compute Engine VMs require manual patching and have single points of failure.')">D) Write logs to a local disk on a Compute Engine VM.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/solutions/healthcare-life-sciences' target='_blank'>Google Cloud Healthcare & Life Sciences Solutions</a></li><li><a href='https://cloud.google.com/apigee/docs' target='_blank'>Apigee API Management Documentation</a></li></ul>"
    },

    # 047: Case Study: Mountkirk Games
    {
        "topic_no": "047",
        "roadmap_id": "7.4b",
        "title": "Case Study: Mountkirk Games — Global Multiplayer & Spanner",
        "page_type": "case-study",
        "phase": "Phase 7 — Case Studies & Exam Prep",
        "lead": "Official Case Study Analysis: Mountkirk Games — Architecting a globally distributed mobile multiplayer game backend with Cloud Spanner 99.999% consistency, GKE Autopilot, Pub/Sub, and BigQuery analytics.",
        "comp1": ("Mobile Game Clients", "Millions of Global Players", "data", "Establishes low-latency WebSocket / UDP sessions and submits game score telemetry."),
        "comp2": ("Global Game Gateways", "Global External ALB", "data", "Routes players to closest regional GKE cluster with Anycast single IP."),
        "comp3": ("Game Server Pods", "GKE Autopilot Fleet", "data", "Executes real-time multiplayer logic, matchmaking, and player state synchronization."),
        "comp4": ("Global Consistent Persistence", "Cloud Spanner Multi-Region", "data", "Provides 99.999% SLA relational ACID storage with zero-downtime global schema updates."),
        "flow1": "Global players launch game; Anycast ALB terminates TLS and routes to lowest-latency regional GKE pod.",
        "flow2": "Game servers execute matchmaking and record player inventory and purchases in Cloud Spanner.",
        "flow3": "Telemetry events stream via Pub/Sub and Dataflow into BigQuery for real-time player behavior modeling.",
        "fail": "A sudden viral celebrity tweet drives a 15x spike in player logins across North America and Europe.",
        "heal": "GKE Autopilot automatically scales node capacity; Cloud Spanner scales compute processing units horizontally.",
        "city_concept": "City Grand Colosseum & Worldwide Broadcasts",
        "p1": "The City Colosseum was hosting games, but spectators from across the globe had to send carrier pigeons to place bets, resulting in delayed wagers and lost tickets.",
        "p2": "Arena Master Marcus built telegraph scoreboards (Global Load Balancer) and connected regional betting kiosks directly to the Central Vault (Cloud Spanner).",
        "p3": "When 100,000 extra spectators arrived, Marcus opened additional arena turnstiles (GKE Autopilot) within minutes.",
        "p4": "Physical colosseums have fixed stone seating; cloud gaming backends auto-scale elastically to absorb millions of concurrent players.",
        "part1_html": """
        <h3>Case Profile: Mountkirk Games</h3>
        <p>
          <strong>Company Background:</strong> Mountkirk Games is an established mobile game studio expanding into real-time, global multiplayer gaming. Their previous game experienced unexpected viral popularity, which overwhelmed their legacy single-region MySQL database and caused hours of game downtime.
        </p>
        <div class="callout">
          <div class="callout-title">Mountkirk Games Requirements Breakdown</div>
          <ul>
            <li><strong>Business Goals:</strong> Deliver a seamless, lag-free global player experience; scale instantly during marketing campaigns; minimize operational management; monetize game data with machine learning.</li>
            <li><strong>Technical Requirements:</strong> Global low-latency data access; relational consistency for in-game purchases and currency balances; 99.999% database availability; ingestion of 500,000 score events/sec.</li>
            <li><strong>Watchpoints:</strong> Single-region databases cannot support global writes without cross-region replication lag; manual server provisioning cannot keep pace with viral spikes.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Global Anycast Routing (Global External ALB)</h4>
        <p>Use a single Anycast IP address to terminate client connections at the nearest Google edge PoP, routing traffic across Google's private fiber backbone to regional GKE clusters.</p>
        <h4>Layer 2 — Practitioner: GKE Autopilot for Game Server Fleets</h4>
        <p>Run game server containers on <strong>GKE Autopilot</strong>. Autopilot automates node provisioning, OS patching, and cluster hardening, eliminating operational toil so game developers can focus on gameplay mechanics.</p>
        <h4>Layer 3 — Architect: Cloud Spanner Multi-Region for In-Game Purchases</h4>
        <p>Deploy <strong>Cloud Spanner</strong> in a multi-region configuration. Spanner provides relational ACID guarantees, 99.999% SLA availability, and synchronous Paxos replication, ensuring in-game coin balances are never corrupted or double-spent.</p>
        <h4>Layer 4 — Staff: Streaming Telemetry Pipeline (Pub/Sub &gt; Dataflow &gt; BigQuery)</h4>
        <p>Stream real-time game telemetry through <strong>Cloud Pub/Sub</strong> into <strong>Dataflow</strong> (running Apache Beam windowing) and sink directly into <strong>BigQuery</strong> for real-time fraud detection and churn modeling.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Marcus ensures every arena wager is recorded instantaneously in the central ledger with zero discrepancies.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Mountkirk Database Selection Justification</div>
          <p>
            An exam scenario asks: <em>"Mountkirk Games needs a transactional database to store user currency balances. The game is played simultaneously across North America, Europe, and Asia. Players must never experience stale currency balances or double-spending, and the database must guarantee 99.999% availability. Which database must be chosen?"</em>
          </p>
          <p>Justify why <strong>Cloud Spanner</strong> is the only correct answer.</p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Defended Justification</h4>
          <p><strong>Cloud Spanner Multi-Region</strong> is the only database in Google Cloud that provides: (1) Globally distributed synchronous relational ACID transactions, (2) Strong external consistency using TrueTime atomic clocks, and (3) A <strong>99.999% SLA</strong> (less than 5.26 minutes of downtime per year). Cloud SQL only reaches 99.95% within a single region, Bigtable lacks multi-row ACID transactions, and Firestore does not provide 99.999% multi-region relational SQL.</p>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Case Study: Mountkirk Games (Question 1)</span>
          <p><strong>Mountkirk Games wants to analyze gameplay telemetry from 20 million active mobile devices to detect cheating and adjust game difficulty in near real-time. The ingestion pipeline must scale automatically to handle millions of events per second with minimal operational overhead. Which architecture should you choose?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Cloud Pub/Sub handles massive streaming ingestion elastically, Dataflow provides auto-scaling stream processing with windowing, and BigQuery stores petabytes for SQL analytics.')">A) Ingest events via Cloud Pub/Sub, process with Cloud Dataflow, and sink into BigQuery for real-time analysis and machine learning.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Compute Engine VMs require manual scaling and broker management, creating high operational overhead.')">B) Deploy an unmanaged Apache Kafka cluster on Compute Engine instances with persistent disks.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud SQL row-by-row transactional writes will lock and exhaust connection pools under millions of events per second.')">C) Write telemetry events directly from mobile devices into Cloud SQL for PostgreSQL.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud Storage batch uploads introduce high latency and do not provide near real-time stream processing.')">D) Upload hourly CSV files from mobile devices into Cloud Storage buckets.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/spanner/docs' target='_blank'>Cloud Spanner Architecture & Documentation</a></li><li><a href='https://cloud.google.com/solutions/gaming' target='_blank'>Google Cloud Gaming Solutions</a></li></ul>"
    },

    # 048: Case Study: TerramEarth
    {
        "topic_no": "048",
        "roadmap_id": "7.4c",
        "title": "Case Study: TerramEarth — IoT Fleet, Bigtable & Predictive Maintenance",
        "page_type": "case-study",
        "phase": "Phase 7 — Case Studies & Exam Prep",
        "lead": "Official Case Study Analysis: TerramEarth — Ingesting real-time telemetry from 20 million heavy agricultural vehicles: cellular vs Wi-Fi connectivity, Cloud Bigtable time-series storage, Dataflow, and Vertex AI predictive maintenance.",
        "comp1": ("Connected Vehicle Fleet", "20M Heavy Tractors", "data", "Transmits critical telemetry: engine temperature, hydraulic pressure, and GPS coordinates."),
        "comp2": ("Dual Ingestion Paths", "Cellular & Wi-Fi GCS", "data", "Real-time critical alerts over cellular; large batch diagnostic dumps over local Wi-Fi to Cloud Storage."),
        "comp3": ("High-Throughput NoSQL", "Cloud Bigtable", "data", "Sub-10ms time-series storage absorbing millions of writes per second with linear scalability."),
        "comp4": ("Predictive AI Engine", "Vertex AI & BigQuery", "control", "Trains ML models on historical sensor patterns to predict tractor component failure 48 hours in advance."),
        "flow1": "Vehicles upload real-time cellular telemetry alerts directly to Google Cloud Pub/Sub.",
        "flow2": "When vehicles return to maintenance depots, 50 GB diagnostic logs upload over Wi-Fi to Cloud Storage.",
        "flow3": "Dataflow transforms data and writes to Cloud Bigtable for real-time dashboards and BigQuery for ML training.",
        "fail": "A sudden cellular tower outage in the agricultural valley interrupts vehicle uploads.",
        "heal": "Vehicles buffer telemetry locally on embedded SSD storage and resume upload via exponential backoff upon reconnection.",
        "city_concept": "City Municipal Cart Fleet & Workshop Sensors",
        "p1": "Twenty thousand city freight wagons were breaking wooden axles on cobblestones without warning, blocking streets for days.",
        "p2": "Master Mechanic Martha installed vibration meters on every wagon axle (IoT Sensors) and built two reporting channels: emergency bells (Cellular) and depot inspections (Wi-Fi).",
        "p3": "Martha recorded all vibration logs in the Grand Ledger (Bigtable), noticing axles groaned at a specific pitch 2 days before snapping.",
        "p4": "Manual mechanical checks take hours per wagon; cloud IoT ingest processes sensor telemetry from 20M vehicles in sub-seconds.",
        "part1_html": """
        <h3>Case Profile: TerramEarth</h3>
        <p>
          <strong>Company Background:</strong> TerramEarth designs and manufactures heavy agricultural and mining equipment. They have over <strong>20 million vehicles</strong> deployed globally. 200,000 vehicles have continuous cellular connectivity, while the remaining 19.8 million vehicles upload sensor data only when they return to maintenance depots with Wi-Fi.
        </p>
        <div class="callout">
          <div class="callout-title">TerramEarth Requirements Breakdown</div>
          <ul>
            <li><strong>Business Goals:</strong> Predict equipment failures before they happen (predictive maintenance) to prevent costly farm downtime; sell autonomous operational insights to equipment operators.</li>
            <li><strong>Technical Requirements:</strong> Ingest streaming real-time alerts from 200,000 cellular vehicles (200 sensors at 1 Hz = millions of events/sec); ingest 50 GB daily Wi-Fi batch files from 19.8M vehicles; sub-10ms query latency for operational telemetry dashboards.</li>
            <li><strong>Core Watchpoint:</strong> <strong>Dual Ingestion Strategy</strong>. Real-time streaming (Pub/Sub) vs massive asynchronous batch file uploads (Cloud Storage + Storage Transfer Service).</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: The Dual-Speed Ingestion Architecture</h4>
        <p>Segregate workloads: (1) <strong>Speed Layer (Cellular):</strong> Vehicles publish real-time alerts directly to Cloud Pub/Sub; (2) <strong>Batch Layer (Wi-Fi):</strong> Vehicles dump compressed binary sensor files to regional <strong>Cloud Storage</strong> buckets when connected to depot Wi-Fi.</p>
        <h4>Layer 2 — Practitioner: Cloud Bigtable for High-Throughput Time-Series</h4>
        <p>Sensor telemetry is time-series data with extreme write volume. <strong>Cloud Bigtable</strong> provides linear horizontal scalability with sub-10ms read/write latency. Design row keys properly: <code>vehicle_id#timestamp_reversed</code> to prevent hotspotting on a single node.</p>
        <h4>Layer 3 — Architect: Dataflow ETL & BigLake Analytics</h4>
        <p>Use <strong>Cloud Dataflow</strong> to execute unified batch and streaming pipelines. Dataflow deduplicates telemetry events, parses binary formats, and writes operational metrics to Bigtable while sinking curated tables to BigQuery via BigLake.</p>
        <h4>Layer 4 — Staff: Vertex AI Predictive Maintenance Pipelines</h4>
        <p>Train anomaly detection and regression models on <strong>Vertex AI</strong> using historical sensor degradation curves. When real-time Bigtable telemetry matches a pre-failure signature, trigger an automated maintenance alert dispatching replacement parts to the farm.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Martha checks vibration logs on her ledger, dispatching mechanics to replace wagon axles before they crack.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: TerramEarth Row Key Design Drill</div>
          <p>
            In Cloud Bigtable, sequential row keys (e.g. <code>timestamp#sensor_id</code>) cause a critical anti-pattern known as <strong>hotspotting</strong>, where 100% of writes hit a single Bigtable tablet server while other nodes remain idle.
          </p>
          <p>Design an optimal row key schema for TerramEarth's 20 million vehicles to ensure uniform distribution across all Bigtable cluster nodes.</p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Optimal Row Key Schema</h4>
          <p><strong>Recommended Schema:</strong> <code>&lt;vehicle_id&gt;#&lt;sensor_type&gt;#&lt;reversed_timestamp&gt;</code></p>
          <ul>
            <li><strong>vehicle_id prefix:</strong> Distributes writes across different lexicographical keyspaces and nodes evenly, preventing sequential write hotspotting.</li>
            <li><strong>sensor_type:</strong> Allows targeted scanning of specific telemetry metrics (e.g. engine temperature).</li>
            <li><strong>reversed_timestamp (Long.MAX_VALUE - timestamp):</strong> Ensures the most recent telemetry readings appear first during range scans, accelerating real-time dashboard queries.</li>
          </ul>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Case Study: TerramEarth (Question 1)</span>
          <p><strong>TerramEarth wants to ingest 50 GB daily diagnostic files uploaded from 19.8 million vehicles when they connect to dealer Wi-Fi networks worldwide. The solution must provide cost-effective global upload endpoints with lowest latency and minimal operational management. Which architecture should you choose?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Multi-Region Cloud Storage buckets with signed URLs allow vehicles to upload directly to Google edge network endpoints securely without managing server fleets.')">A) Generate short-lived signed URLs for vehicles to upload compressed diagnostic files directly to multi-region Cloud Storage buckets.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'An SFTP server on a single VM is a bottleneck that cannot absorb parallel uploads from millions of vehicles.')">B) Deploy an SFTP server on a single Compute Engine VM with an attached persistent disk.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud SQL has storage and connection limitations that cannot store petabytes of raw binary files cost-effectively.')">C) Upload files directly into Cloud SQL for MySQL as BLOB columns.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud Pub/Sub has a maximum message size of 10 MB and cannot accept 50 GB files.')">D) Stream the 50 GB files through Cloud Pub/Sub messages.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/bigtable/docs' target='_blank'>Cloud Bigtable Schema Design & Documentation</a></li><li><a href='https://cloud.google.com/solutions/iot' target='_blank'>Google Cloud IoT & Telemetry Architectures</a></li></ul>"
    },

    # 049: Case Study: Helicopter Racing League (HRL)
    {
        "topic_no": "049",
        "roadmap_id": "7.4d",
        "title": "Case Study: Helicopter Racing League — Video Streaming & Real-Time ML",
        "page_type": "case-study",
        "phase": "Phase 7 — Case Studies & Exam Prep",
        "lead": "Official Case Study Analysis: Helicopter Racing League (HRL) — Global low-latency real-time video streaming, in-flight race telemetry, Transcoder API, Cloud CDN, and Vertex AI real-time prediction models.",
        "comp1": ("Racing Helicopters", "High-Speed Onboard Telemetry", "data", "Streams 4K video feeds and 100 Hz cockpit telemetry while maneuvering at 200 mph."),
        "comp2": ("Video Transcoding Pipeline", "Live Stream / Transcoder API", "control", "Transcodes high-bitrate video streams into multi-bitrate HLS/DASH formats for global mobile delivery."),
        "comp3": ("Global Video CDN Edge", "Cloud CDN / Media CDN", "data", "Caches live video segments at Google's global edge network, delivering sub-second live latency."),
        "comp4": ("Race Predictions Engine", "Vertex AI & Cloud Run", "control", "Predicts overtaking maneuvers and race winner probabilities in real time for broadcast graphics."),
        "flow1": "Helicopters transmit live video and telemetry over high-speed radio links to ground stations.",
        "flow2": "Ground stations ingest streams into Google Cloud via Transcoder API and Cloud Pub/Sub.",
        "flow3": "Cloud CDN delivers live video chunks to global viewers; Vertex AI serves real-time prediction overlays.",
        "fail": "A sudden burst of 5 million viewers tunes into the championship race final lap.",
        "heal": "Cloud CDN caches 98% of video fragment requests at the edge, protecting origin encoding servers from overload.",
        "city_concept": "City Sky Regatta & Signal Mirrors",
        "p1": "Airships were racing across the mountain valley, but spectators in the town square could only see distant specks and had no idea who was winning.",
        "p2": "Broadcaster Brian mounted signal mirrors on airships (Video Feeds) and set up relay towers (Cloud CDN) beaming live flags to every street corner.",
        "p3": "Brian hired an actuary (Vertex AI) who calculated wind drift to announce the winner 30 seconds before the final turn.",
        "p4": "Signal mirrors are obscured by fog; digital video streaming over cloud CDN reaches millions of devices simultaneously in 4K.",
        "part1_html": """
        <h3>Case Profile: Helicopter Racing League (HRL)</h3>
        <p>
          <strong>Company Background:</strong> The Helicopter Racing League (HRL) is a global sports organization that organizes high-speed helicopter races in diverse locations worldwide. They want to modernize their broadcast platform to deliver ultra-low latency video streaming, real-time telemetry overlays, and predictive race analytics.
        </p>
        <div class="callout">
          <div class="callout-title">HRL Requirements Breakdown</div>
          <ul>
            <li><strong>Business Goals:</strong> Increase fan engagement with immersive digital broadcasts; expand viewer base globally; provide real-time predictive telemetry overlays (e.g. probability of pilot overtaking in turn 3).</li>
            <li><strong>Technical Requirements:</strong> Transcode high-definition live video feeds into multi-bitrate streams with sub-3 second latency; ingest high-frequency telemetry from racing helicopters; support millions of concurrent global viewers.</li>
            <li><strong>Key Challenge:</strong> Balancing compute-intensive video encoding with low-latency edge caching and real-time machine learning predictions.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Video Ingestion & Transcoder API</h4>
        <p>Use the <strong>Live Stream API</strong> and <strong>Transcoder API</strong> to convert raw RTMP/SRT video feeds into multi-bitrate HTTP Live Streaming (HLS) and Dynamic Adaptive Streaming over HTTP (DASH) segments.</p>
        <h4>Layer 2 — Practitioner: Media CDN & Cloud CDN Edge Delivery</h4>
        <p>Deliver video segments via <strong>Media CDN</strong> (built on Google's YouTube infrastructure). Media CDN provides edge caching at hundreds of metropolitan locations, offloading origin servers and eliminating stream buffering.</p>
        <h4>Layer 3 — Architect: Real-Time Telemetry Pipeline (Pub/Sub & Dataflow)</h4>
        <p>In-flight telemetry (speed, G-force, altitude, engine RPM) streams through <strong>Cloud Pub/Sub</strong> into <strong>Dataflow</strong>. Telemetry is joined with live video timestamp metadata to synchronize graphic overlays.</p>
        <h4>Layer 4 — Staff: Vertex AI Real-Time Prediction Overlays</h4>
        <p>Deploy trained TensorFlow models to <strong>Vertex AI Endpoints</strong>. The model evaluates current flight trajectories and outputs probability scores for live broadcast overlays with sub-100ms inference latency.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Brian broadcasts airship regattas to thousands of pub lanterns across the valley with zero signal delay.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Live Video Streaming Architecture Defense</div>
          <p>
            An exam scenario asks: <em>"HRL needs to deliver live race video streams to millions of concurrent viewers globally with minimum latency and highest cache hit ratio, while preventing origin server exhaustion. Which edge service should be deployed?"</em>
          </p>
          <p>Contrast <strong>Cloud CDN / Media CDN</strong> with self-hosting NGINX reverse proxies on Compute Engine.</p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Defended Answer</h4>
          <p><strong>Cloud CDN / Media CDN</strong> leverages Google's global edge network of thousands of Points of Presence (PoPs) connected via private fiber. It automatically caches video chunks (HLS/DASH) at the edge closest to the user, providing over 95% origin cache offload with sub-second latency. Self-hosting NGINX proxies on Compute Engine requires manual autoscaling, cannot match Google's global Anycast edge presence, and introduces severe single-region origin bottlenecks under viral viewer spikes.</p>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Case Study: HRL (Question 1)</span>
          <p><strong>Helicopter Racing League wants to train a machine learning model to predict race outcomes using historical telemetry from past seasons. The data science team prefers using Python Jupyter notebooks and wants an automated managed pipeline for model training, hyperparameter tuning, and endpoint deployment. Which service should you recommend?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Vertex AI provides managed Jupyter notebooks (Workbench), automated pipelines, hyperparameter tuning, model registry, and managed deployment endpoints.')">A) Vertex AI with Vertex AI Workbench notebooks and Vertex AI Pipelines.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Compute Engine requires manual GPU driver installation, OS patching, and does not provide managed MLOps pipelines.')">B) Compute Engine VMs with manual NVIDIA GPU driver installations.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud Functions has execution time limits (max 60 min) and lacks GPU support for heavy ML training.')">C) Cloud Functions with local scikit-learn libraries.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'BigQuery ML is suited for SQL models on tabular data, but does not provide Jupyter notebooks or general custom deep learning pipelines.')">D) BigQuery ML only.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/media-cdn/docs' target='_blank'>Google Cloud Media CDN Documentation</a></li><li><a href='https://cloud.google.com/vertex-ai/docs' target='_blank'>Vertex AI Machine Learning Platform</a></li></ul>"
    },

    # 050: Exam Strategy & PCA Keyword Elimination
    {
        "topic_no": "050",
        "roadmap_id": "7.5",
        "title": "PCA Exam Strategy: Keyword Elimination & Domain Mastery",
        "page_type": "concept",
        "phase": "Phase 7 — Case Studies & Exam Prep",
        "lead": "Mastering the Google Cloud Professional Cloud Architect exam: Domain weightings, question taxonomy, the method of elimination, trigger keyword mapping, and pacing tactics.",
        "comp1": ("Exam Question Prompt", "Complex Scenario", "control", "Contains stated requirements, unstated constraints, distracting noise, and target goals."),
        "comp2": ("Keyword Decoder Engine", "Architectural Mental Model", "control", "Maps trigger words to Google Cloud architectural principles and managed service tiers."),
        "comp3": ("Option Elimination Matrix", "Process of Elimination", "control", "Eliminates options that violate constraints (cost, compliance, downtime, operational overhead)."),
        "comp4": ("Defended Correct Choice", "Optimal Solution", "data", "Selects the most cost-effective, least-operational-overhead, fully compliant architecture."),
        "flow1": "Candidate reads question stem, identifying business constraint and non-functional requirements.",
        "flow2": "Candidate spots trigger words ('minimum operational overhead', 'lowest cost', 'zero data loss').",
        "flow3": "Candidate eliminates options containing anti-patterns, leaving the single defended architecture.",
        "fail": "Candidate chooses an option that functions technically but introduces unnecessary manual operational overhead.",
        "heal": "Candidate remembers Google's preference for fully managed, serverless solutions and selects the managed tier.",
        "city_concept": "City Master Builder Licensing Examination",
        "p1": "Apprentices were memorizing the weights of bricks without understanding how arches distribute load, failing when asked to build bridges.",
        "p2": "Grand Master Marcus reformed the Master Builder Exam: presenting real-world city crises and testing judgment under strict time limits.",
        "p3": "Candidates learned to spot trick questions: when asked for the fastest bridge, the answer was a pontoon bridge, not a five-year stone arch.",
        "p4": "Apprentice exams test rote memory; Cloud Architect exams test strategic trade-off judgment under enterprise constraints.",
        "part1_html": """
        <h3>The Situation: The Nature of the PCA Exam</h3>
        <p>
          The <strong>Google Cloud Professional Cloud Architect (PCA)</strong> exam is widely recognized as one of the most challenging certifications in IT. Unlike junior associate exams that test service trivia or CLI flags, the PCA exam evaluates <strong>architectural judgment</strong>.
        </p>
        <p>
          Almost every multiple-choice question contains <strong>two technically plausible answers</strong>. The wrong answer will technically work, but it violates a key constraint (it costs too much, requires manual ops maintenance, or fails a compliance rule).
        </p>
        <div class="callout">
          <div class="callout-title">The Master Trigger Keyword Decoder</div>
          <ul>
            <li><strong>"Minimum operational overhead" / "Least management effort":</strong> Lean immediately toward fully managed serverless services (Cloud Run, GKE Autopilot, Cloud Spanner, BigQuery, Pub/Sub). Reject self-hosted Compute Engine VMs.</li>
            <li><strong>"Lowest cost for fault-tolerant batch":</strong> Spot VMs (Preemptible), Cloud Storage Archive tier, BigQuery flat-rate/editions with reservations.</li>
            <li><strong>"Global external consistency" / "99.999% SLA":</strong> Cloud Spanner multi-region.</li>
            <li><strong>"Zero public IPs" / "Prevent data exfiltration":</strong> VPC Service Controls, Private Google Access, Private Service Connect, Identity-Aware Proxy (IAP).</li>
            <li><strong>"Without modifying application code":</strong> Rehost (M2VM), Containerize as-is, Cloud SQL instead of Spanner, Cloud Load Balancing URL maps.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: The 5-Step Elimination Technique</h4>
        <ol>
          <li>Read the <strong>last sentence</strong> first to know what is being asked (e.g. <em>"What should you do to minimize cost?"</em>).</li>
          <li>Scan for hard constraints: Budget, Compliance (HIPAA/PCI), Timeline, Skill gaps.</li>
          <li>Eliminate options that are technically impossible or violate GCP product limits.</li>
          <li>Eliminate options that violate the stated constraint (e.g. choosing Compute Engine when asked for minimal ops).</li>
          <li>Select the defended answer among remaining candidates.</li>
        </ol>
        <h4>Layer 2 — Practitioner: Time Management & Pacing</h4>
        <p>The exam consists of ~50-60 questions over 120 minutes. That allows roughly <strong>2 minutes per question</strong>. Case study questions require reading long narratives; bookmark difficult questions and return to them on your second pass.</p>
        <h4>Layer 3 — Architect: Case Study Question Mechanics</h4>
        <p>Case study questions (EHR Healthcare, Mountkirk Games, TerramEarth, HRL) account for ~20-30% of the exam. Because case studies are public before the exam, master the business goals, constraints, and architecture of each case study before exam day!</p>
        <h4>Layer 4 — Staff: The Architect Mindset</h4>
        <p>Think like a Google Chief Architect: prefer cloud-native patterns, decouple systems asynchronously with queues, minimize human toil, and enforce zero-trust identity guardrails.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Marcus awards the Master Builder medallion to architects who prove they can build safe, cost-efficient structures.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Elimination Drill</div>
          <p>
            Question: <em>"An organization needs to host an internal employee portal. The application runs in a Docker container, requires HTTPS authentication using corporate Google accounts, and must scale to zero when no employees are active at night to minimize cost with zero server maintenance. Which architecture should you choose?"</em>
          </p>
          <p>Apply the 5-step elimination technique to evaluate options A, B, C, and D.</p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>Elimination Walkthrough</h4>
          <ul>
            <li><strong>Option A (Compute Engine VM with NGINX):</strong> <em>Eliminated.</em> Does not scale to zero automatically; requires OS patching and server maintenance.</li>
            <li><strong>Option B (GKE Standard cluster):</strong> <em>Eliminated.</em> GKE cluster management fee and running worker nodes incur continuous cost even with zero traffic; high operational overhead.</li>
            <li><strong>Option C (Cloud Run behind Identity-Aware Proxy):</strong> <strong>CORRECT.</strong> Cloud Run natively runs Docker containers, scales to zero (0 instances = $0 cost), requires zero server maintenance, and IAP integrates directly with corporate Google accounts for HTTPS authentication.</li>
            <li><strong>Option D (Cloud Storage static website):</strong> <em>Eliminated.</em> Cannot execute containerized dynamic application logic.</li>
          </ul>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Exam Strategy (Question 1)</span>
          <p><strong>When an exam question specifically asks to design a solution that requires "minimal ongoing operational management and maintenance", which architectural choice should the candidate prioritize?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Fully managed serverless services (Cloud Run, GKE Autopilot, Spanner, BigQuery) offload OS patching, cluster management, and capacity sizing to Google, representing minimal operational overhead.')">A) Fully managed, serverless Google Cloud services (such as Cloud Run, GKE Autopilot, and BigQuery) that eliminate infrastructure patching and capacity management.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Unmanaged Compute Engine VMs require continuous OS patching, monitoring, and capacity management, representing the highest operational overhead.')">B) Unmanaged Compute Engine instances with custom shell scripts.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Self-managing open-source clusters incurs heavy operational maintenance for upgrades, broker balancing, and disk management.')">C) Self-managed open-source Kubernetes and Kafka clusters on bare VMs.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Sole-tenant nodes add hardware configuration management.')">D) Dedicated sole-tenant hardware nodes.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/certification/cloud-architect' target='_blank'>Google Professional Cloud Architect Certification Page</a></li><li><a href='https://cloud.google.com/architecture/framework' target='_blank'>Google Cloud Architecture Framework</a></li></ul>"
    }
]

def main():
    print(f"Building Phase 7 (Topics 045 to 050) - {len(PHASE7_TOPICS)} topics...")
    for item in PHASE7_TOPICS:
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
