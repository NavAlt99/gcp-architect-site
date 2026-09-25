#!/usr/bin/env python3
"""
generate_phase1_phase2_remaining.py - Generates Topics 006, 010, 011, 012, 017, 018, 019, 021.
Completes Phase 0, Phase 1, and Phase 2.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_website import build_topic_page
from batch_generate_full import make_d1_map, make_d2_flow, make_d3_failure, make_analogy

REMAINING_TOPICS = [
    # 006: Optional warm-up
    {
        "topic_no": "006",
        "roadmap_id": "0.6",
        "title": "Cloud Digital Leader & Business Foundations",
        "page_type": "concept",
        "phase": "Phase 0 — Prerequisites",
        "lead": "Business framing of cloud transformation: Total Cost of Ownership (TCO), CapEx vs OpEx, Google Cloud value pillars, and executive communication.",
        "comp1": ("Executive Sponsor", "Business Leader", "control", "Evaluates cloud ROI, agility, and risk management."),
        "comp2": ("Cloud Adoption Framework", "CAF Assessment", "control", "Evaluates People, Process, Technology, and Governance maturity."),
        "comp3": ("FinOps Cost Center", "Budget Model", "control", "Transitions upfront capital expenditure to variable operating expenditure."),
        "comp4": ("Value Metrics Tracker", "KPI Dashboard", "control", "Tracks time-to-market and customer satisfaction improvements."),
        "flow1": "Leadership initiates cloud readiness assessment across business units.",
        "flow2": "CAF framework identifies skills gaps, security baselines, and quick-win workloads.",
        "flow3": "Finance establishes pay-as-you-go operating expenditure model.",
        "fail": "Business treats cloud migration as a pure lift-and-shift without modernizing processes.",
        "heal": "Leadership adopts Cloud Center of Excellence (CCoE) and FinOps training.",
        "city_concept": "City Modernization Vision & Council Appropriations",
        "p1": "The City Council was spending millions maintaining decaying brick municipal warehouses that took two years to approve.",
        "p2": "Mayor Meridian drafted the Modern City Charter (Cloud Digital Leader), moving funds from rigid real estate purchases to flexible municipal services.",
        "p3": "Department directors overspent their monthly budgets because electricity was now metered on-demand. Tomas the Treasurer set hard spending alerts.",
        "p4": "In government, budgets are locked in annual cycles; in cloud FinOps, unit economics adjust dynamically every hour.",
        "part1_html": """
        <h3>The Situation: Aligning Technology with Business Value</h3>
        <p>
          Cloud architecture is not merely about VMs and networks; it is an economic transformation. Organizations migrate to Google Cloud to move from <strong>Capital Expenditure (CapEx)</strong>—purchasing expensive hardware up front that depreciates over 5 years—to <strong>Operating Expenditure (OpEx)</strong>, paying only for resources consumed in real time.
        </p>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Google Cloud Adoption Framework (CAF)</h4>
        <p>The CAF evaluates 4 core pillars: Learn, Lead, Scale, and Secure across tactical, strategic, and transformational maturity stages.</p>
        <h4>Layer 2 — Practitioner: CapEx vs OpEx Accounting</h4>
        <p>CapEx requires multi-year forecasting and hardware over-provisioning. OpEx aligns cloud spend directly with business revenue (unit economics).</p>
        <h4>Layer 3 — Architect: TCO & ROI Modeling</h4>
        <p>Total Cost of Ownership (TCO) includes datacenter power, cooling, real estate, physical security guards, hardware replacement, and engineering maintenance.</p>
        <h4>Layer 4 — Staff: Executive Alignment & Business Case Defense</h4>
        <p>Staff architects justify cloud investments to CFOs and CTOs using business risk mitigation, compliance agility, and faster time-to-market.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Mayor Meridian ensures that every municipal tax dollar spent returns visible improvements to public transit and safety.</p>",
        "part4_demo_html": "<div class='callout'><div class='callout-title'>Practice Drill: Business Case Pitch</div><p>Draft a 3-bullet pitch to a CFO explaining why moving from on-premise hardware to Google Cloud saves money and increases agility.</p></div>",
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Recall (Question 1)</span>
          <p><strong>What is the primary financial advantage of shifting from CapEx to OpEx in cloud computing?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! OpEx replaces large upfront equipment purchases with flexible, pay-as-you-go operating costs.')">A) Paying only for resources consumed without large upfront capital outlays.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Hardware depreciation is an on-premises CapEx reality.')">B) Depreciating physical hardware over five years.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Upfront commitments are optional CUDs, not the primary cloud shift.')">C) Locking in 10-year datacenter real-estate leases.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Security remains a shared responsibility.')">D) Eliminating all security responsibilities.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/adoption-framework' target='_blank'>Google Cloud Adoption Framework</a></li></ul>"
    },

    # 010: Billing and Cost Hygiene
    {
        "topic_no": "010",
        "roadmap_id": "1.4",
        "title": "Billing, Cost Hygiene, and FinOps Architecture",
        "page_type": "service",
        "phase": "Phase 1 — GCP Foundations",
        "lead": "Financial engineering on Google Cloud: Billing Accounts vs Projects, automated Budgets & Alerts via Pub/Sub, BigQuery billing export analysis, and quota management.",
        "comp1": ("Billing Account", "Cloud Billing", "control", "Master corporate paying entity linked to credit card or invoice agreement."),
        "comp2": ("Budget Alert Service", "Cloud Monitoring", "control", "Evaluates current spend against forecast thresholds (50%, 90%, 100%)."),
        "comp3": ("Pub/Sub Alert Topic", "Cloud Pub/Sub", "control", "Triggers automated Cloud Functions to disable billing if runaway spend occurs."),
        "comp4": ("BigQuery Billing Export", "BigQuery Analytics", "data", "Stores detailed raw cost attribution data with resource labels.") ,
        "flow1": "Projects accumulate metered resource usage charges in real time.",
        "flow2": "Budget service evaluates spend; triggers Pub/Sub notification when 90% threshold is breached.",
        "flow3": "Raw billing records stream into BigQuery dataset for automated Looker Studio executive reporting.",
        "fail": "A developer script loops infinitely, spawning 500 GPU instances and incurring $10,000 in overnight charges.",
        "heal": "Programmatic budget notification on Pub/Sub invokes Cloud Function that revokes project billing.",
        "city_concept": "City Treasury, Utility Meters, and Emergency Spending Caps",
        "p1": "Brightloaf Bakery left the kitchen water taps running full blast for three weeks. When the utility bill arrived, the bakery was nearly bankrupted.",
        "p2": "Tomas the Treasurer installed digital meters (Cloud Billing Export) and set automated alarm bells when water consumption exceeded 50% of budget.",
        "p3": "A pipe burst in the basement. The automatic shutoff valve (Pub/Sub + Cloud Function) cut the water main before the building flooded.",
        "p4": "In physical billing, utility companies bill you 30 days late; in Google Cloud, billing data streams to BigQuery in continuous increments.",
        "part1_html": """
        <h3>The Situation: Why FinOps Comes on Day One</h3>
        <p>
          The most dangerous mistake a cloud engineer can make is deploying infrastructure before configuring <strong>Budgets and Alerts</strong>. In cloud environments, mistakes scale with the same speed as success. A single recursive script can provision hundreds of high-end compute instances overnight, resulting in catastrophic surprise bills.
        </p>
        <div class="callout warning">
          <div class="callout-title">Budgets Alert, They Do NOT Cap Spend!</div>
          Google Cloud Budget alerts <strong>do not shut down resources automatically</strong>. By default, they send email alerts to Billing Admins. To automatically cap spend or shut down projects during runaways, architects must configure <strong>Programmatic Budget Notifications via Pub/Sub</strong> to trigger an automated Cloud Function that unlinks the billing account.
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Billing Accounts & Roles</h4>
        <p>Billing Accounts are separate from projects. One Billing Account can fund hundreds of projects. Key roles: <em>Billing Account Administrator</em> (manages payments/links), <em>Billing Account User</em> (can attach projects), and <em>Billing Account Viewer</em> (reads cost data).</p>
        <h4>Layer 2 — Practitioner: Labels for Cost Allocation</h4>
        <p>Apply mandatory labels to every resource (e.g. <code>environment: prod</code>, <code>cost-center: retail</code>, <code>owner: team-alpha</code>). These labels flow into the BigQuery billing export for granular chargeback reporting.</p>
        <h4>Layer 3 — Architect: Quota Architecture (Rate vs Allocation)</h4>
        <ul>
          <li><strong>Rate Quotas:</strong> Limits API requests per minute (e.g. 1000 read requests/min to Compute API). Resets automatically.</li>
          <li><strong>Allocation Quotas:</strong> Limits total active resources (e.g. max 24 regional vCPUs in us-central1). Requires formal quota increase request via Console.</li>
        </ul>
        <h4>Layer 4 — Staff: Committed Use Discounts (CUDs)</h4>
        <p>Staff architects commit to 1-year or 3-year usage to receive up to 57% discounts: <strong>Resource-Based CUDs</strong> (for steady-state predictable VM shapes) vs <strong>Flexible Spend-Based CUDs</strong> (for diverse compute across GCE, GKE, and Cloud Run).</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Tomas the Treasurer monitors municipal water and electricity consumption with automated digital meters.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Creating a Billing Budget with gcloud</div>
          <pre><code># Create a $1000 monthly budget with alerts at 50%, 90%, and 100%
gcloud billing budgets create \
  --billing-account=012345-6789AB-CDEF01 \
  --display-name="Production Budget" \
  --budget-amount=1000USD \
  --threshold-rule=percent=0.5 \
  --threshold-rule=percent=0.9 \
  --threshold-rule=percent=1.0</code></pre>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Application (Question 1)</span>
          <p><strong>You set a $5,000 monthly budget alert on a production Google Cloud project. On day 15, spend reaches $5,001. What happens to the running Compute Engine instances?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Budgets only generate email alerts or Pub/Sub events; they do not terminate or interrupt active resources.')">A) Nothing; instances continue running normally while alert emails are dispatched.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'GCP never terminates active instances without programmatic automation.')">B) All VMs are immediately stopped by Google Cloud.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Budgets do not throttle CPU.')">C) VMs are throttled to 10% CPU capacity.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'The project is not deleted.')">D) The project enters a 30-day shutdown state.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/billing/docs/how-to/budgets' target='_blank'>Cloud Billing Budgets & Alerts</a></li><li><a href='https://cloud.google.com/billing/docs/how-to/export-data-bigquery' target='_blank'>Exporting Billing Data to BigQuery</a></li></ul>"
    },

    # 011: Global Infrastructure
    {
        "topic_no": "011",
        "roadmap_id": "1.5",
        "title": "Google Global Infrastructure & Network Tiers",
        "page_type": "service",
        "phase": "Phase 1 — GCP Foundations",
        "lead": "The physical foundation of Google Cloud: Regions, availability zones, sub-sea fiber networks (B4/Jupiter), edge points of presence, and Premium vs Standard Network Service Tiers.",
        "comp1": ("Global Edge PoP", "Edge Network", "data", "Over 180 Google Points of Presence where traffic enters the Google private fiber network."),
        "comp2": ("Google B4 Backbone", "Private Terabit Fiber", "data", "Google-owned inter-datacenter fiber optic cables spanning oceans and continents."),
        "comp3": ("Region Datacenter", "Campus us-central1", "data", "Physical facilities with redundant power, cooling, and Titan security chips."),
        "comp4": ("Network Service Tiers", "Premium vs Standard", "control", "Governs whether traffic transits Google private fiber or public internet ISPs.") ,
        "flow1": "User in London sends request to app hosted in Iowa (us-central1).",
        "flow2": "In Premium Tier, traffic enters London Edge PoP immediately and travels across Google private fiber.",
        "flow3": "In Standard Tier, traffic bounces across third-party public internet ISPs until reaching Iowa.",
        "fail": "Public transit provider cuts undersea cable, causing massive packet loss on standard internet.",
        "heal": "Premium Tier routes traffic automatically over Google's redundant undersea cables with zero loss.",
        "city_concept": "City International Airports, Transit Hubs, and High-Speed Rail",
        "p1": "Bea wanted to ship bread to Paris. She handed parcels to random hitchhikers on public dirt roads. Packages got lost, spoiled, or delayed by traffic.",
        "p2": "Mayor Meridian connected Cloud City to a private high-speed dedicated maglev railway (Google Global Fiber Network) with secured customs terminals.",
        "p3": "A landslide blocked one international railway tunnel. The central dispatch automatically diverted trains through an alternative mountain tunnel in milliseconds.",
        "p4": "In public roads, potholes and tollbooths delay traffic; on Google's private B4 network, packets travel at two-thirds the speed of light in vacuum.",
        "part1_html": """
        <h3>The Situation: Google's Secret Architectural Weapon</h3>
        <p>
          Google Cloud is built upon the same private planetary network that powers Google Search, YouTube, and Maps. Google operates hundreds of thousands of kilometers of privately owned subsea and terrestrial fiber optic cables. When you send traffic to a Google Cloud Anycast IP, your packets enter Google's private network at the nearest edge Point of Presence (PoP) and travel across Google's high-speed private backbone, completely bypassing the congested public internet.
        </p>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Regions and Zones</h4>
        <p>A <strong>Region</strong> is an independent geographic area (e.g. <code>us-west1</code> in The Dalles, Oregon). Each region contains at least three distinct <strong>Zones</strong> (e.g. <code>us-west1-a</code>, <code>b</code>, <code>c</code>) isolated against physical power, flood, and fire events.</p>
        <h4>Layer 2 — Practitioner: Network Service Tiers (Premium vs Standard)</h4>
        <table>
          <thead><tr><th>Dimension</th><th>Premium Tier (Default)</th><th>Standard Tier</th></tr></thead>
          <tbody>
            <tr><td><strong>Routing Path</strong></td><td>Enters Google private fiber at nearest edge PoP close to user (Cold Potato).</td><td>Transits public internet ISPs until reaching destination datacenter region (Hot Potato).</td></tr>
            <tr><td><strong>Global Anycast IP</strong></td><td>Supported (Single IP routes to nearest region worldwide).</td><td>Not supported (Regional IPs only).</td></tr>
            <tr><td><strong>SLA & Performance</strong></td><td>Guaranteed high throughput, low jitter, and 99.99% network SLA.</td><td>Variable performance subject to third-party ISP congestion.</td></tr>
          </tbody>
        </table>
        <h4>Layer 3 — Architect: Choosing a Primary Region</h4>
        <p>Select regions based on: 1) Proximity to users (latency), 2) Regulatory data residency compliance, 3) Service availability (not all GPUs or services exist in every region), 4) Cost (pricing varies by 20-30% between regions), and 5) Carbon footprint.</p>
        <h4>Layer 4 — Staff: Subsea Cable Redundancy & Jupiter Datacenter Fabric</h4>
        <p>Google datacenters employ the <strong>Jupiter</strong> Clos network fabric, delivering petabits-per-second bisection bandwidth across compute racks. Subsea cables (Curie, Dunant, Equiano, Grace Hopper) provide multi-terabit redundant cross-ocean transport.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, express bullet trains link the city center to global commercial ports without stopping at traffic lights.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Reserving a Static IP with Network Tier Selection</div>
          <pre><code># Reserve a global Premium Tier Anycast IP
gcloud compute addresses create global-lb-ip \
  --global \
  --network-tier=PREMIUM

# Reserve a cheaper regional Standard Tier IP for non-critical batch ingress
gcloud compute addresses create batch-ip \
  --region=us-west1 \
  --network-tier=STANDARD</code></pre>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Recall (Question 1)</span>
          <p><strong>What is the primary difference between Google Cloud Premium Tier and Standard Tier networking?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Premium Tier enters Google private fiber as close to the user as possible (cold potato), while Standard Tier travels across the public internet.')">A) Premium Tier routes traffic over Google private global backbone; Standard Tier routes over the public internet.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Standard Tier supports IPv4 and IPv6.')">B) Standard Tier does not support IPv4.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Both tiers support encryption.')">C) Premium Tier encrypts packets, but Standard Tier does not.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Standard Tier is available in multiple regions.')">D) Standard Tier is only available in North America.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/network-tiers/docs/overview' target='_blank'>Network Service Tiers Overview</a></li><li><a href='https://cloud.google.com/about/locations' target='_blank'>Google Cloud Regions & Datacenter Locations</a></li></ul>"
    },

    # 017: Load Balancing and Edge
    {
        "topic_no": "017",
        "roadmap_id": "2.5",
        "title": "Cloud Load Balancing, Cloud CDN, and Cloud Armor",
        "page_type": "service",
        "phase": "Phase 2 — Core Services",
        "lead": "High-capacity global edge architecture: Global External Application Load Balancers (HTTP/S), Regional L7, L4 Passthrough Network LBs, Cloud CDN caching, and Cloud Armor WAF defense.",
        "comp1": ("Global Client", "Web / Mobile App", "data", "User initiating HTTPS request from anywhere in the world."),
        "comp2": ("Google Frontend (GFE)", "Cloud Load Balancing", "data", "Global Anycast edge proxy terminating TLS and routing via URL maps."),
        "comp3": ("Cloud Armor WAF", "Security Policy", "control", "Evaluates OWASP Top 10, IP rate limits, and adaptive DDoS protection."),
        "comp4": ("Cloud CDN Cache", "Edge Cache Node", "data", "Serves cached static images, videos, and scripts directly from Google edge PoP.") ,
        "flow1": "Client sends HTTPS request to single global Anycast IP address.",
        "flow2": "Nearest Google Frontend terminates TLS, applies Cloud Armor security inspection, and checks Cloud CDN cache.",
        "flow3": "If cache miss, request routes across Andromeda SDN to nearest healthy backend MIG in us-west1 or europe-west1.",
        "fail": "A distributed denial of service (DDoS) attack hits the application with 500,000 requests per second.",
        "heal": "Cloud Armor rate limiting blocks malicious IP ranges at edge; Google Anycast absorbs the volumetric flood.",
        "city_concept": "City Grand Arrival Gates, Customs Quarantine, and Express Parcel Depot",
        "p1": "Customers swarmed Brightloaf's tiny storefront entrance. Bad actors pushed in fake coupons, while shoppers in London had to send letters across the Atlantic for a menu.",
        "p2": "Rae the Dispatcher constructed Global Edge Gates (Load Balancers & Anycast). Customs officers (Cloud Armor) filter bad actors, while regional kiosks (CDN) hand out menus instantly.",
        "p3": "A botnet flooded the gates with bogus catalog requests. Cloud Armor slammed the iron portcullis on the botnet while legitimate pastry shoppers walked in freely.",
        "p4": "In physical gates, crowds cause street riots; Google Cloud Load Balancers handle millions of QPS without warm-up time.",
        "part1_html": """
        <h3>The Situation: True Global Load Balancing Without Pre-Warming</h3>
        <p>
          Unlike traditional load balancers (like AWS ALB) that scale up DNS records and require "pre-warming" before massive traffic spikes, <strong>Google Cloud Load Balancing is a software-defined, distributed proxy running on Google Frontends (GFEs)</strong>. A single Global External Application Load Balancer presents one Anycast IP address to the entire world. It can scale instantly from 0 to 1,000,000+ QPS without any pre-warming or DNS changes.
        </p>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Load Balancer Taxonomy</h4>
        <ul>
          <li><strong>Global External Application Load Balancer (L7):</strong> HTTP/HTTPS/HTTP2/gRPC. Terminate TLS at edge; URL host and path routing; integrates with Cloud CDN and Cloud Armor.</li>
          <li><strong>Regional External Application Load Balancer (L7):</strong> HTTP/S within a single region for strict data sovereignty compliance.</li>
          <li><strong>External Passthrough Network Load Balancer (L4):</strong> Raw TCP/UDP. Non-proxy, preserves client IP, ultra-high performance Maglev packet forwarding.</li>
          <li><strong>Internal Application / Network Load Balancer:</strong> Private RFC 1918 load balancing between microservice tiers inside the VPC.</li>
        </ul>
        <h4>Layer 2 — Practitioner: SSL Policies & Google-Managed Certificates</h4>
        <p>Google Cloud provisions, validates, and auto-renews free SSL certificates via <strong>Certificate Manager</strong>. Use <strong>SSL Policies</strong> to restrict cipher suites (e.g. mandate TLS 1.3 and ban insecure CBC ciphers).</p>
        <h4>Layer 3 — Architect: Cloud Armor WAF & Edge Caching</h4>
        <p>Protect origins from Layer 7 attacks using <strong>Cloud Armor</strong>: preconfigured rules defend against SQLi, XSS, and LFI. Enable <strong>Cloud CDN</strong> on backend buckets or services to serve static web assets directly from edge caches with sub-10ms response times.</p>
        <h4>Layer 4 — Staff: Cross-Region Overflow & Failover Mechanics</h4>
        <p>Global ALBs monitor backend capacity (target utilization or rate). When the us-west1 cluster reaches 100% capacity during a local flash sale, the load balancer automatically overflows excess traffic to us-central1 without returning HTTP 503 errors.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Rae the Dispatcher directs millions of travelers through automated biometric arrival gates with zero waiting in line.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Creating a Cloud Armor Security Policy</div>
          <pre><code># 1. Create Cloud Armor policy
gcloud compute security-policies create block-bad-actors \
  --description="Block SQLi and rate limit bots"

# 2. Add preconfigured OWASP SQL injection rule
gcloud compute security-policies rules create 1000 \
  --security-policy=block-bad-actors \
  --expression="evaluatePreconfiguredExpr('sqli-v33-stable')" \
  --action=deny-403

# 3. Attach policy to backend service
gcloud compute backend-services update web-backend-service \
  --global \
  --security-policy=block-bad-actors</code></pre>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: PCA Scenario (Question 1)</span>
          <p><strong>An e-commerce website experiences sudden Layer 7 SQL injection attacks against their search API. You must block these attacks at Google's network edge before traffic reaches your GKE pods, with zero modifications to application source code. What should you configure?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Cloud Armor integrates with External Application Load Balancers to evaluate WAF rules (including OWASP SQLi) at edge PoPs.')">A) Attach a Cloud Armor security policy with preconfigured SQLi rules to the External Application Load Balancer backend service.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'VPC firewall rules operate at Layer 3/4 and cannot parse HTTP payloads or SQL syntax.')">B) Create a VPC firewall rule blocking port 80 and 443.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud CDN caches content but does not inspect SQL injection payloads.')">C) Enable Cloud CDN on the backend service.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'L4 Network Load Balancer does not inspect HTTP application payloads.')">D) Migrate to an External Passthrough Network Load Balancer.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/load-balancing/docs/application-load-balancer' target='_blank'>External Application Load Balancer Overview</a></li><li><a href='https://cloud.google.com/armor/docs' target='_blank'>Google Cloud Armor Documentation</a></li></ul>"
    },

    # 018: Hybrid Connectivity
    {
        "topic_no": "018",
        "roadmap_id": "2.6",
        "title": "Hybrid and Multi-Cloud Connectivity: VPN & Interconnect",
        "page_type": "service",
        "phase": "Phase 2 — Core Services",
        "lead": "Bridging corporate datacenters to Google Cloud: Cloud HA VPN (99.99% SLA), Dedicated vs Partner Interconnect, Cross-Cloud Interconnect, Cloud Router, and BGP dynamic routing.",
        "comp1": ("On-Premises Datacenter", "Customer Router", "data", "Customer border router running BGP over IPsec or direct cross-connect."),
        "comp2": ("Cloud HA VPN Gateway", "Managed VPN Gateway", "data", "Provides two interfaces with active-active IPsec tunnels offering 99.99% SLA."),
        "comp3": ("Cloud Router", "BGP Route Controller", "control", "Dynamically exchanges routing prefixes with on-premises BGP peers."),
        "comp4": ("Dedicated Interconnect", "Physical Fiber 100G", "data", "Direct physical circuit between customer network and Google colocation facility.") ,
        "flow1": "On-premises database initiates data replication call to private Google Cloud IP (10.0.1.5).",
        "flow2": "Packet traverses active IPsec tunnel or 100 Gbps physical Interconnect circuit.",
        "flow3": "Cloud Router advertises VPC subnet routes back to on-premises network via BGP.",
        "fail": "A backhoe cuts primary physical fiber circuit outside the datacenter.",
        "heal": "BGP detects keepalive failure; instantly reroutes traffic through secondary redundant circuit with zero packet loss.",
        "city_concept": "City Inter-State Freight Tunnels & Secured Border Rail",
        "p1": "Brightloaf Bakery's corporate headquarters was located in Chicago, while cloud kitchens were in Oregon. Delivery trucks got stuck in snowstorms on public interstates.",
        "p2": "Rae the Dispatcher excavated a twin-bore underground high-speed freight tunnel (HA VPN / Interconnect) directly between the city depot and the bakery headquarters.",
        "p3": "A flood collapsed Tunnel A. Automated rail signals (BGP) instantly switched all freight trains into Tunnel B without delaying a single shipment.",
        "p4": "In physical construction, digging tunnels takes years; in Google Cloud, provisioning an HA VPN takes 5 minutes.",
        "part1_html": """
        <h3>The Situation: The Hybrid Enterprise Reality</h3>
        <p>
          Most enterprises do not migrate to the cloud in a single weekend. For years, cloud environments must securely interoperate with on-premises corporate datacenters, legacy mainframe systems, and partner clouds (AWS/Azure). Google Cloud provides two primary hybrid connectivity vehicles: <strong>Cloud VPN</strong> over the public internet, and <strong>Cloud Interconnect</strong> over private physical circuits.
        </p>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Cloud HA VPN (High Availability)</h4>
        <p>Cloud HA VPN provides a <strong>99.99% availability SLA</strong>. It consists of two interfaces, each with its own public IP address. To achieve 99.99% SLA, you must configure <strong>two tunnels</strong> connected to two separate on-premises customer gateway interfaces with dynamic BGP routing.</p>
        <h4>Layer 2 — Practitioner: Cloud Interconnect (Dedicated vs Partner)</h4>
        <ul>
          <li><strong>Dedicated Interconnect:</strong> Direct physical 10 Gbps or 100 Gbps cross-connect between your datacenter router and Google's colocation facility. Best for massive data transfer (>10 Gbps) and low latency.</li>
          <li><strong>Partner Interconnect:</strong> Connects through a supported service provider (Equinix, Megaport). Best when physical presence in a Google colocation facility is unavailable or bandwidth requirements are under 10 Gbps.</li>
        </ul>
        <h4>Layer 3 — Architect: Cloud Router & BGP Dynamic Routing</h4>
        <p>Never use static routes for hybrid architectures. <strong>Cloud Router</strong> uses Border Gateway Protocol (BGP) to dynamically exchange routes between on-premises and Google Cloud VPCs. Use <strong>Multi-Exit Discriminator (MED)</strong> values to establish active/passive priority configurations.</p>
        <h4>Layer 4 — Staff: 99.99% Interconnect Topology</h4>
        <p>To qualify for Google's 99.99% Interconnect SLA, architects must provision <strong>four VLAN attachments across two separate metropolitan areas (metros) and two separate edge routers (EERs)</strong>.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, dual underground freight rail tunnels connect the municipal warehouse directly to regional agricultural supply farms.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Creating a Cloud HA VPN Gateway</div>
          <pre><code># 1. Create HA VPN gateway with two external interfaces
gcloud compute vpn-gateways create ha-vpn-gw \
  --network=production-vpc \
  --region=us-west1

# 2. Create Cloud Router for BGP route exchange
gcloud compute routers create vpn-router \
  --network=production-vpc \
  --region=us-west1 \
  --asn=65001</code></pre>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: PCA Scenario (Question 1)</span>
          <p><strong>An enterprise requires a hybrid connection between their on-premises datacenter and Google Cloud. The workload requires 50 Gbps sustained throughput, predictable sub-5ms latency, and a 99.99% availability SLA. What connectivity solution must you design?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Dedicated Interconnect provides 100 Gbps circuits and achieves 99.99% SLA with redundant connections across two metros.')">A) Dedicated Interconnect configured across two distinct metropolitan areas with four VLAN attachments.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'HA VPN maxes out at 3 Gbps per tunnel and transits the public internet.')">B) Cloud HA VPN with 10 parallel tunnels.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Single metro only qualifies for 99.9% SLA, not 99.99%.')">C) Dedicated Interconnect in a single metro location with two VLAN attachments.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Carrier peering does not support private RFC 1918 traffic or an SLA.')">D) Carrier Peering connection.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/network-connectivity/docs/vpn/concepts/overview' target='_blank'>Cloud HA VPN Overview</a></li><li><a href='https://cloud.google.com/network-connectivity/docs/interconnect/concepts/overview' target='_blank'>Cloud Interconnect Topologies</a></li></ul>"
    },

    # 019: Storage
    {
        "topic_no": "019",
        "roadmap_id": "2.7",
        "title": "Cloud Storage, Object Lifecycle, and Enterprise File Systems",
        "page_type": "service",
        "phase": "Phase 2 — Core Services",
        "lead": "Planetary-scale unstructured storage: Cloud Storage classes (Standard, Nearline, Coldline, Archive), Autoclass, retention policies, Bucket Lock, and managed Filestore NFS.",
        "comp1": ("Application Uploader", "Web App Client", "data", "Uploads invoices, media, and database dumps via signed URLs."),
        "comp2": ("Cloud Storage Bucket", "Unified Object Store", "data", "Stores immutable objects with 99.999999999% (11 9s) annual durability."),
        "comp3": ("Object Lifecycle Engine", "Lifecycle Policy", "control", "Automatically transitions cold objects to Nearline, Coldline, and Archive classes."),
        "comp4": ("Bucket Lock Compliance", "WORM Retention Policy", "control", "Guarantees regulatory immutability (Write Once, Read Many).") ,
        "flow1": "Application generates signed URL allowing user to upload customer invoice directly to bucket.",
        "flow2": "Object is stored in Standard class with 11 9s durability.",
        "flow3": "Lifecycle policy inspects object age: transitions to Coldline after 90 days and deletes after 7 years.",
        "fail": "A compromised admin account attempts to delete compliance audit files.",
        "heal": "Bucket Lock retention policy blocks object deletion; even Google root administrators cannot delete locked objects.",
        "city_concept": "City Central Silos, Archival Vaults, and Sealed Time Capsules",
        "p1": "Brightloaf Bakery dumped receipts, flour sacks, and tax audits in cardboard boxes in the backyard. Rain destroyed paper records and mice ate the tax forms.",
        "p2": "Mayor Meridian constructed concrete municipal vaults (Cloud Storage). Daily flour goes in the open warehouse, while 10-year financial audits go into sealed blast-proof vaults.",
        "p3": "A crooked politician tried shredding campaign donation receipts. The titanium time-lock (Bucket Lock) prevented the vault door from opening for 5 years.",
        "p4": "In physical archives, paper degrades over time; in Cloud Storage, Google uses Reed-Solomon erasure coding across multiple facilities to guarantee 11 9s durability.",
        "part1_html": """
        <h3>The Situation: The Universal Object Store</h3>
        <p>
          <strong>Cloud Storage (GCS)</strong> is Google Cloud's foundational service for unstructured object data (media files, analytics data lakes, database backups, website assets). Every object is stored with <strong>99.999999999% (11 9s) annual durability</strong> through automated erasure coding across independent physical failure domains.
        </p>
        <div class="callout">
          <div class="callout-title">Storage Classes: Balancing Access Frequency and Cost</div>
          <ul>
            <li><strong>Standard:</strong> Active, frequently accessed data (websites, mobile apps, streaming media). No retrieval fees, no minimum storage duration.</li>
            <li><strong>Nearline:</strong> Accessed less than once a month (monthly backups, recent reports). Low storage cost, small retrieval fee, 30-day minimum duration.</li>
            <li><strong>Coldline:</strong> Accessed less than once a quarter (disaster recovery data). Ultra-low storage cost, 90-day minimum duration.</li>
            <li><strong>Archive:</strong> Accessed less than once a year (regulatory compliance, tax archives). Lowest storage cost, 365-day minimum duration.</li>
            <li><strong>Autoclass:</strong> Automatically transitions objects between classes based on access patterns without manual lifecycle rules.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Location Types & Replication</h4>
        <ul>
          <li><strong>Regional:</strong> Stored within one region across 3 zones. Lowest cost; highest in-region compute performance.</li>
          <li><strong>Dual-Region:</strong> Stored across two specific regions (e.g. <code>nam4</code>: Iowa and South Carolina) with Turbo Replication for 15-minute RPO failover.</li>
          <li><strong>Multi-Region:</strong> Geo-redundant storage spread across a continent (e.g. <code>US</code> or <code>EU</code>). Survives full regional catastrophe.</li>
        </ul>
        <h4>Layer 2 — Practitioner: Uniform Bucket-Level Access (UBLA)</h4>
        <p>Always enable <strong>Uniform Bucket-Level Access</strong>. UBLA disables legacy per-object Access Control Lists (ACLs) and unifies all security under Cloud IAM. This prevents accidental data leaks caused by legacy object permissions.</p>
        <h4>Layer 3 — Architect: Signed URLs & Direct Client Uploads</h4>
        <p>Never proxy large file uploads through backend API servers. Have the server generate a cryptographic <strong>Signed URL</strong> with a 15-minute expiration, allowing the user's browser to stream gigabytes directly into Cloud Storage.</p>
        <h4>Layer 4 — Staff: Bucket Lock (WORM Compliance)</h4>
        <p>For regulatory compliance (SEC Rule 17a-4, FINRA, HIPAA), architects configure <strong>Retention Policies with Bucket Lock</strong>. Once locked, objects cannot be deleted or overwritten by any user (including Google support) until the retention duration expires.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, municipal granaries store fresh wheat for daily baking while titanium vaults hold century-old historical town charters.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Creating a Compliance Bucket with Lifecycle Rules</div>
          <pre><code># Create bucket with Uniform Bucket-Level Access
gcloud storage buckets create gs://brightloaf-compliance-vault \
  --location=us-west1 \
  --uniform-bucket-level-access

# Apply retention policy of 365 days
gcloud storage buckets update gs://brightloaf-compliance-vault \
  --retention-period=365d</code></pre>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Application (Question 1)</span>
          <p><strong>A financial institution must store transaction audit logs for 7 years to satisfy regulatory compliance. The records must be strictly immutable and protected against accidental or malicious deletion by any administrator. How should you design the storage solution?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! A Cloud Storage bucket with a 7-year retention policy and Bucket Lock permanently enforces WORM compliance.')">A) Cloud Storage bucket with an Archive storage class, a 7-year retention policy, and Bucket Lock enabled.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Admins with Owner permissions can delete versioned objects.')">B) Cloud Storage bucket with object versioning enabled and delete permissions removed from developers.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Persistent Disks do not provide WORM compliance or 11 9s durability.')">C) Persistent Disk snapshot stored in Coldline storage.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Filestore does not offer immutable WORM compliance locks.')">D) Enterprise Filestore instance with read-only permissions.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/storage/docs/storage-classes' target='_blank'>Cloud Storage Classes Guide</a></li><li><a href='https://cloud.google.com/storage/docs/bucket-lock' target='_blank'>Bucket Lock & Retention Policies</a></li></ul>"
    },

    # 021: Messaging and Integration
    {
        "topic_no": "021",
        "roadmap_id": "2.9",
        "title": "Messaging and Integration: Pub/Sub, Cloud Tasks, and Eventarc",
        "page_type": "service",
        "phase": "Phase 2 — Core Services",
        "lead": "Asynchronous microservice decoupling: Cloud Pub/Sub publish-subscribe mechanics, push vs pull subscriptions, message ordering, dead-letter topics, Cloud Tasks rate-limiting, and Workflows orchestration.",
        "comp1": ("Order Producer", "Frontend Microservice", "data", "Publishes order event JSON messages to Pub/Sub topic."),
        "comp2": ("Cloud Pub/Sub", "Global Message Broker", "data", "Durable distributed message queue with at-least-once delivery guarantee."),
        "comp3": ("Dead-Letter Topic", "Error Quarantine", "control", "Captures poison-pill messages that fail processing after max delivery attempts."),
        "comp4": ("Cloud Tasks", "Task Scheduler", "data", "Provides precise execution scheduling, rate-limiting, and deduping.") ,
        "flow1": "Web order service publishes 'OrderPlaced' event message to Pub/Sub topic.",
        "flow2": "Pub/Sub replicates message across 3 zones and fans out to inventory, payment, and email subscriptions.",
        "flow3": "Subscribers process payload and acknowledge (ACK); unacknowledged messages are retried automatically.",
        "fail": "A malformed JSON payload crashes consumer workers repeatedly.",
        "heal": "Dead-letter policy routes poison message to dead-letter queue after 5 failed attempts, restoring queue throughput.",
        "city_concept": "City Postal Sorting Facility & Pneumatic Tube Dispatch",
        "p1": "When a customer ordered bread, the baker had to sprint across town to the flour mill, wait for grinding, sprint to the packaging plant, and sprint back. The store was paralyzed.",
        "p2": "Mayor Meridian installed a Central Pneumatic Tube Mail Dispatch (Cloud Pub/Sub). When an order is placed, a dispatch capsule drops into the system.",
        "p3": "One delivery address had an invalid street name. After 5 failed delivery attempts, the letter was filed in the Lost Letter Registry (Dead-Letter Topic).",
        "p4": "In physical mail, letters get lost or waterlogged; Cloud Pub/Sub guarantees at-least-once delivery with global durability.",
        "part1_html": """
        <h3>The Situation: Decoupling Distributed Microservices</h3>
        <p>
          In monolithic systems, services invoke each other synchronously via HTTP or database locks. If the email notification service slows down, the entire checkout process times out. By introducing <strong>Cloud Pub/Sub</strong> as an asynchronous message bus, producers publish events without waiting for consumers, achieving true architectural decoupling and smoothing traffic spikes.
        </p>
        <div class="callout">
          <div class="callout-title">Pub/Sub vs Cloud Tasks: When to Use Which?</div>
          <ul>
            <li><strong>Cloud Pub/Sub (Publish-Subscribe):</strong> 1-to-many message distribution. Publisher does not know or care who is listening. Best for event streaming, analytics pipelines, and decoupled microservices.</li>
            <li><strong>Cloud Tasks (Task Queues):</strong> 1-to-1 asynchronous invocation. Explicit target endpoint, strict rate-limiting (e.g. max 50 requests/sec to legacy API), scheduled execution in the future, and task deduplication.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Push vs Pull Subscriptions</h4>
        <ul>
          <li><strong>Pull Subscriptions:</strong> Consumers poll Pub/Sub for messages and send explicit ACKs. Best for high-volume batch processing (Dataflow, GKE worker pools).</li>
          <li><strong>Push Subscriptions:</strong> Pub/Sub sends HTTPS POST requests directly to consumer endpoints (Cloud Run, webhooks). Best for serverless scale-to-zero architectures.</li>
        </ul>
        <h4>Layer 2 — Practitioner: Delivery Guarantees & Dead-Letter Topics</h4>
        <p>Pub/Sub guarantees <strong>at-least-once delivery</strong>. Consumers must be designed to be <strong>idempotent</strong> (handling duplicate messages safely). Configure a <strong>Dead-Letter Topic</strong> with a maximum delivery attempts threshold (e.g. 5) to quarantine corrupt poison-pill messages.</p>
        <h4>Layer 3 — Architect: Message Ordering & Retention</h4>
        <p>By default, Pub/Sub does not guarantee strict FIFO ordering. To preserve sequence (e.g. bank account deposits and withdrawals), enable <strong>Message Ordering Keys</strong>. Pub/Sub retains unacknowledged messages for up to 7 days (or replay acknowledged messages via seek).</p>
        <h4>Layer 4 — Staff: Exactly-Once Processing with Dataflow</h4>
        <p>For financial transactions where duplicates cannot be tolerated, combine Pub/Sub with <strong>Cloud Dataflow (Apache Beam)</strong> to achieve cryptographically verified <strong>exactly-once processing</strong> semantics.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, the central pneumatic postal sorting office routes letters to baking, packaging, and billing departments simultaneously.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Creating a Pub/Sub Topic with Dead-Letter Handling</div>
          <pre><code># 1. Create dead letter topic and main topic
gcloud pubsub topics create order-dead-letter
gcloud pubsub topics create order-events

# 2. Create subscription with dead-letter policy
gcloud pubsub subscriptions create order-worker-sub \
  --topic=order-events \
  --ack-deadline=30 \
  --dead-letter-topic=order-dead-letter \
  --max-delivery-attempts=5</code></pre>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: PCA Scenario (Question 1)</span>
          <p><strong>Your e-commerce application needs to send order confirmation webhooks to third-party merchant partners. The partner endpoints can only handle a maximum rate of 25 requests per second and often experience temporary outages requiring scheduled retry backoffs. Which service should you choose?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Cloud Tasks is specifically designed for 1-to-1 task execution with explicit rate limiting and scheduled retries.')">A) Cloud Tasks with a queue configured with a rate limit of 25 dispatches/sec.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Pub/Sub pushes as fast as possible and does not support strict rate-limit throttling.')">B) Cloud Pub/Sub with a push subscription.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud Scheduler is for cron schedules, not per-order queues.')">C) Cloud Scheduler jobs.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud Memorystore is an in-memory cache, not a managed task queue.')">D) Cloud Memorystore for Redis queue.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/pubsub/docs/overview' target='_blank'>Cloud Pub/Sub Architecture</a></li><li><a href='https://cloud.google.com/tasks/docs/dual-overview' target='_blank'>Cloud Tasks vs Pub/Sub</a></li></ul>"
    },

    # 012: Support and Governance Basics
    {
        "topic_no": "012",
        "roadmap_id": "1.6",
        "title": "Support, Governance Basics, and Asset Inventory",
        "page_type": "concept",
        "phase": "Phase 1 — GCP Foundations",
        "lead": "Operational governance: Google Cloud Support tiers (Basic, Standard, Enhanced, Premium), Cloud Asset Inventory real-time analysis, Service Health, and Preview vs GA launch stages.",
        "comp1": ("Cloud Asset Inventory", "Metadata Engine", "control", "Maintains real-time 10-year snapshot of all Google Cloud resources across the organization."),
        "comp2": ("Personalized Service Health", "Health Dashboard", "control", "Provides tailored alerts on outages specifically impacting active projects."),
        "comp3": ("Enterprise Support", "Technical Account Manager", "control", "Guarantees 15-minute response times for critical P1 outages."),
        "comp4": ("Audit Logging Sink", "Central Log Sink", "control", "Exports asset changes and admin mutations to BigQuery for compliance auditing.") ,
        "flow1": "Engineer provisions cloud storage bucket.",
        "flow2": "Cloud Asset Inventory records asset birth event and streams metadata change to central Pub/Sub topic.",
        "flow3": "Governance engine checks compliance against company encryption standards.",
        "fail": "A major Google Cloud regional network incident occurs.",
        "heal": "Personalized Service Health dispatches automated alert notifying SRE team before user tickets file.",
        "city_concept": "City Emergency Operations Center & Municipal Property Deeds",
        "p1": "The City Council had no central property ledger. Nobody knew how many water pumps the city owned, who built them, or what condition they were in.",
        "p2": "Ola the Operator set up the Central Registry (Cloud Asset Inventory) and established Emergency Response hotlines (Premium Support).",
        "p3": "A power substation failed. The Municipal Emergency Dashboard notified the mayor within 2 minutes with affected street maps.",
        "p4": "In physical cities, property deeds take weeks to search; in Cloud Asset Inventory, querying 100,000 resources across 500 projects takes 2 seconds.",
        "part1_html": """
        <h3>The Situation: Governance at Scale</h3>
        <p>
          Managing 5 projects is simple; managing 500 projects across 3,000 developers requires automated governance. <strong>Cloud Asset Inventory</strong> gives architects a real-time, searchable database of every virtual machine, bucket, IAM binding, and network rule across the entire Google Cloud organization.
        </p>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Google Cloud Support Tiers</h4>
        <ul>
          <li><strong>Basic:</strong> Billing support and documentation only (Free).</li>
          <li><strong>Standard:</strong> 4-hour response time for P2 business issues ($29/mo + 3% spend).</li>
          <li><strong>Enhanced:</strong> 1-hour response time for P1 critical issues ($500/mo + 3% spend).</li>
          <li><strong>Premium:</strong> 15-minute response for P1 outages, designated Technical Account Manager (TAM), and Event Management ($12,500/mo + spend).</li>
        </ul>
        <h4>Layer 2 — Practitioner: Launch Stages (Preview vs GA)</h4>
        <p>Never run production workloads on <strong>Preview</strong> or <strong>Early Access</strong> features. Only <strong>Generally Available (GA)</strong> products carry Google Cloud SLAs and full enterprise support backing.</p>
        <h4>Layer 3 — Architect: Cloud Asset Inventory Queries</h4>
        <p>Use <code>gcloud asset search-all-resources</code> and <code>search-all-iam-policies</code> to audit compliance across thousands of projects in seconds.</p>
        <h4>Layer 4 — Staff: Personalized Service Health API</h4>
        <p>Do not rely on the public status dashboard. Integrate the <strong>Personalized Service Health API</strong> into PagerDuty to receive automated alerts for incidents specifically impacting your project IDs.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Ola the Operator coordinates municipal emergency services from the central control tower.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Auditing Org-Wide Public Buckets with Cloud Asset Inventory</div>
          <pre><code># Search entire organization for any bucket allowing public read access
gcloud asset search-all-iam-policies \
  --scope=organizations/123456789012 \
  --query="policy:allUsers"</code></pre>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Recall (Question 1)</span>
          <p><strong>Which Google Cloud support tier is required to receive a 15-minute initial response time for mission-critical P1 outages and an assigned Technical Account Manager (TAM)?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Premium Support guarantees 15-minute response times for critical P1 issues and provides a TAM.')">A) Premium Support</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Enhanced Support provides 1-hour response for P1 and has no dedicated TAM.')">B) Enhanced Support</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Standard Support has 4-hour response times.')">C) Standard Support</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Basic Support provides no technical case handling.')">D) Basic Support</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/asset-inventory/docs/overview' target='_blank'>Cloud Asset Inventory Documentation</a></li><li><a href='https://cloud.google.com/support' target='_blank'>Google Cloud Customer Care Support Plans</a></li></ul>"
    }
]

def build_all_remaining():
    print(f"Building {len(REMAINING_TOPICS)} remaining topics across Phase 0, 1, 2...")
    for t in REMAINING_TOPICS:
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
    print("Done building remaining topics.")

if __name__ == '__main__':
    build_all_remaining()
