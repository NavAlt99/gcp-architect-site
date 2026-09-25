#!/usr/bin/env python3
"""
generate_core_services.py - Generates Topics 009-012, 014-021 to complete Phase 1 and Phase 2.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_website import build_topic_page
from batch_generate_full import make_d1_map, make_d2_flow, make_d3_failure, make_analogy

CORE_SERVICES_LIST = [
    # 009: Identity basics
    {
        "topic_no": "009",
        "roadmap_id": "1.3",
        "title": "Identity Basics: IAM, Principals, and Service Accounts",
        "page_type": "service",
        "phase": "Phase 1 — GCP Foundations",
        "lead": "The zero-trust identity perimeter: Cloud Identity, principals, Google Groups, basic vs predefined vs custom roles, policy bindings, and service account key-less security.",
        "comp1": ("Cloud Identity", "IdP Directory", "control", "Synchronizes corporate employees and security groups from Google Workspace or Okta/Azure AD."),
        "comp2": ("IAM Policy Engine", "Cloud IAM", "control", "Evaluates subject, role, resource, and conditional context on every API call."),
        "comp3": ("Workload Service Account", "Robot Identity", "data", "Non-human principal attached to Compute Engine / Cloud Run / GKE pods."),
        "comp4": ("Cloud Audit Logs", "Activity Trail", "control", "Logs authorization grants and service account impersonation tokens."),
        "flow1": "Workload initiates API call using attached metadata server service account credentials.",
        "flow2": "Cloud IAM verifies policy bindings: confirms roles/storage.objectViewer granted on target bucket.",
        "flow3": "Access granted without any static private keys embedded in application code.",
        "fail": "Rogue developer downloads a static Service Account private JSON key onto their personal laptop.",
        "heal": "Organization Policy 'iam.disableServiceAccountKeyCreation' blocks key export; forces token impersonation.",
        "city_concept": "City Identity Badges & Security Checkpoints",
        "p1": "Anyone could walk into Brightloaf's recipe vault by claiming they worked there. Contractors made physical duplicate master keys that were lost in coffee shops.",
        "p2": "Ines the Inspector deployed biometric municipal badges (Cloud Identity & IAM). Keys are retired in favor of time-expiring wristbands (Impersonation).",
        "p3": "A disgruntled employee tried using an expired delivery pass to enter the treasury. The electronic gate instantly revoked the badge.",
        "p4": "In physical gates, guards might get tired; in Cloud IAM, every single packet and API call evaluates cryptographic proofs in sub-milliseconds.",
        "part1_html": """
        <h3>The Situation: The New Security Perimeter</h3>
        <p>
          In traditional datacenters, security focused on network firewalls and perimeter fences. In Google Cloud, <strong>Identity is the new perimeter</strong>. Every API call (whether from a human developer, an automated deployment pipeline, or a VM querying a database) must be authenticated and authorized by <strong>Cloud IAM (Identity and Access Management)</strong>.
        </p>
        <div class="callout danger">
          <div class="callout-title">The Three Golden Rules of Cloud IAM</div>
          <ul>
            <li><strong>Assign Roles to Groups, Never Individuals:</strong> When an employee joins or leaves a team, adding them to a Google Group automatically provisions or revokes their permissions across all projects.</li>
            <li><strong>Ban Primitive Roles in Production:</strong> Never grant <code>Owner</code>, <code>Editor</code>, or <code>Viewer</code> in production. Always use narrow <strong>Predefined Roles</strong> (e.g. <code>roles/storage.objectViewer</code>) or Custom Roles.</li>
            <li><strong>Never Export Service Account Keys:</strong> Storing <code>key.json</code> files on developer machines is the #1 cause of cloud breaches. Use <strong>Workload Identity</strong> and <strong>Service Account Impersonation</strong> instead.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Principals & Roles</h4>
        <p>An IAM policy binding represents: <em>Who (Principal) can do What (Role) on Which Resource (Project/Bucket/Instance)?</em></p>
        <h4>Layer 2 — Practitioner: Service Account Types</h4>
        <ul>
          <li><strong>User-Managed Service Accounts:</strong> Created by developers for specific workloads (e.g. <code>app-prod@brightloaf.iam.gserviceaccount.com</code>).</li>
          <li><strong>Default Service Accounts:</strong> Auto-created by GCP with overly permissive Editor roles. <em>Antipattern:</em> Always disable default service accounts in production.</li>
          <li><strong>Google-Managed Service Agents:</strong> Internal Google robots running background tasks (e.g. <code>service-PROJECT_NUM@compute-system.iam.gserviceaccount.com</code>).</li>
        </ul>
        <h4>Layer 3 — Architect: IAM Conditions & Deny Policies</h4>
        <p>Use <strong>IAM Conditions</strong> to restrict access based on time of day, originating IP address, or resource name prefixes. Use <strong>IAM Deny Policies</strong> to enforce hard organizational restrictions that cannot be overridden by project-level admins.</p>
        <h4>Layer 4 — Staff: Workload Identity Federation</h4>
        <p>Connect multi-cloud workloads (GitHub Actions, AWS Lambda, on-premises Kubernetes) to GCP without service account keys using OpenID Connect (OIDC) tokens via <strong>Workload Identity Federation</strong>.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Ines the Inspector ensures every visitor holds a valid electronic keycard with minimum necessary clearances.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Service Account Impersonation (Key-Less Access)</div>
          <pre><code># 1. Create a dedicated least-privilege service account
gcloud iam service-accounts create order-reader \
  --description="Reads orders from Cloud Storage" \
  --display-name="order-reader"

# 2. Grant read access to a specific bucket
gcloud storage buckets add-iam-policy-binding gs://brightloaf-orders \
  --member="serviceAccount:order-reader@brightloaf-prod.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"

# 3. Allow developers in group to impersonate the service account without keys
gcloud iam service-accounts add-iam-policy-binding \
  order-reader@brightloaf-prod.iam.gserviceaccount.com \
  --member="group:devops@brightloaf.com" \
  --role="roles/iam.serviceAccountTokenCreator"</code></pre>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: PCA Scenario (Question 1)</span>
          <p><strong>Your security team mandates that continuous integration build agents running on GitHub Actions must deploy containers to Google Artifact Registry without storing long-lived service account keys in GitHub secrets. What should you implement?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Workload Identity Federation exchanges GitHub Actions OIDC tokens for short-lived Google Cloud access tokens with zero static keys.')">A) Configure Workload Identity Federation using GitHub Actions OIDC token provider.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Storing encrypted keys in GitHub still creates static long-lived credentials.')">B) Store a service account private JSON key in encrypted GitHub repository secrets.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Allowing allUsers creates a critical security breach.')">C) Grant Artifact Registry Writer role to allUsers.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Basic Auth with passwords does not eliminate key management risks.')">D) Use Basic Authentication credentials in the Docker build step.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/iam/docs/overview' target='_blank'>Cloud IAM Overview</a></li><li><a href='https://cloud.google.com/iam/docs/best-practices-service-accounts' target='_blank'>Service Account Best Practices</a></li><li><a href='https://cloud.google.com/iam/docs/workload-identity-federation' target='_blank'>Workload Identity Federation</a></li></ul>"
    },

    # 014: GKE (Google Kubernetes Engine)
    {
        "topic_no": "014",
        "roadmap_id": "2.2",
        "title": "Google Kubernetes Engine (GKE): Autopilot & Enterprise Clusters",
        "page_type": "service",
        "phase": "Phase 2 — Core Services",
        "lead": "Enterprise container orchestration: Autopilot vs Standard mode, Regional HA control planes, Container-Native Load Balancing via NEGs, Workload Identity Federation for GKE, and Dataplane V2.",
        "comp1": ("GKE Control Plane", "Managed API & etcd", "control", "Google-managed high-availability regional control plane across 3 zones."),
        "comp2": ("GKE Node Pool", "Compute Worker Nodes", "data", "VPC-native nodes running containerd runtime and kubelet."),
        "comp3": ("Standalone NEG", "Network Endpoint Group", "data", "Routes ingress traffic directly from Cloud Load Balancer to Pod IPs."),
        "comp4": ("Workload Identity", "IAM Identity Engine", "control", "Maps Kubernetes ServiceAccounts directly to Google ServiceAccounts.") ,
        "flow1": "Kubelet schedules Pod onto worker node; Dataplane V2 allocates Pod IP from VPC secondary subnet range.",
        "flow2": "Standalone NEG controller registers Pod IP and container port directly into External Application Load Balancer backend.",
        "flow3": "Client traffic bypasses NodePort and kube-proxy, terminating directly on the Pod container.",
        "fail": "A worker node experiences hardware failure and becomes NodeNotReady.",
        "heal": "Control plane evicts pods and reschedules them on healthy nodes; Node Auto-repair replaces the physical VM.",
        "city_concept": "City Container Terminal & Harbor Fleet Coordination",
        "p1": "Brightloaf Bakery was shipping bread using thousands of individual delivery mopeds. Drivers collided in traffic, half got lost, and keeping maintenance logs was impossible.",
        "p2": "Mayor Meridian constructed a state-of-the-art container terminal (GKE). Standardized shipping crates (Containers) are loaded onto automated regional rail lines.",
        "p3": "During a flash storm, a rail dock was flooded. The harbor master (GKE Scheduler) rerouted all incoming shipping crates to dry docks across town without dropping a single package.",
        "p4": "In physical shipping, cranes take minutes to reposition; in GKE Autopilot, pods scale out in seconds with zero node management required.",
        "part1_html": """
        <h3>The Situation: The World's Premier Kubernetes Platform</h3>
        <p>
          Google invented Kubernetes based on two decades of running internal container orchestration (Borg). <strong>Google Kubernetes Engine (GKE)</strong> is the industry's most mature, scalable managed Kubernetes service. For architects, the first major decision is choosing between <strong>GKE Autopilot</strong> and <strong>GKE Standard</strong>.
        </p>
        <div class="callout">
          <div class="callout-title">GKE Autopilot vs Standard Mode</div>
          <ul>
            <li><strong>GKE Autopilot (Recommended by Google):</strong> Hands-free operations. Google manages, provisions, scales, and patches the worker nodes and control plane. Customers pay only for the Pod CPU, memory, and storage requested. Hardened security defaults (Shielded nodes, Workload Identity, Dataplane V2) are preconfigured.</li>
            <li><strong>GKE Standard:</strong> Full node configuration flexibility. Customers manage node pools, pick exact Compute Engine machine types, configure kernel parameters, and pay for the underlying VMs regardless of pod utilization.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: VPC-Native Clusters & Alias IPs</h4>
        <p>Always create <strong>VPC-native clusters</strong>. VPC-native clusters allocate Pod IP addresses from secondary VPC subnet ranges. This allows Pods to be directly routable within the VPC without double-NAT overhead.</p>
        <h4>Layer 2 — Practitioner: Container-Native Load Balancing (NEGs)</h4>
        <p>In traditional Kubernetes, an Ingress routes traffic to a NodePort, which kube-proxy hops across internal nodes (adding latency). GKE uses <strong>Network Endpoint Groups (NEGs)</strong>: the Google Cloud Load Balancer routes traffic <em>directly to the Pod IP</em>, bypassing kube-proxy entirely and preserving true client IP addresses.</p>
        <h4>Layer 3 — Architect: Workload Identity Federation for GKE</h4>
        <p>Never store Google Cloud service account keys inside Kubernetes Secrets. With <strong>Workload Identity</strong>, you bind a Kubernetes ServiceAccount (KSA) to a Google ServiceAccount (GSA). Any pod running under that KSA automatically acquires Google Cloud IAM permissions via metadata server emulation.</p>
        <h4>Layer 4 — Staff: Multi-Cluster Fleet & GitOps with Config Sync</h4>
        <p>Staff architects manage multi-region GKE clusters as a unified <strong>Fleet</strong>. Declarative cluster configurations and security policies are synchronized continuously from Git repositories using <strong>Config Sync</strong>.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, the central container terminal coordinates cargo transfers across district docks with computerized precision.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Deploying a GKE Autopilot Cluster</div>
          <pre><code># Provision production regional GKE Autopilot cluster
gcloud container clusters create-auto brightloaf-prod-cluster \
  --region=us-west1 \
  --network=production-vpc \
  --subnetwork=gke-subnet \
  --cluster-secondary-range-name=pod-ranges \
  --services-secondary-range-name=service-ranges</code></pre>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: PCA Scenario (Question 1)</span>
          <p><strong>You are architecting a containerized microservice on GKE that must read objects from a private Cloud Storage bucket. Company security policy strictly forbids storing long-lived service account credentials inside Kubernetes Secrets or container images. What should you configure?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Workload Identity links the Kubernetes ServiceAccount to a Google ServiceAccount with Cloud Storage permissions.')">A) Enable GKE Workload Identity, create a Kubernetes ServiceAccount, and bind it to a Google ServiceAccount with Storage Object Viewer role.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Granting storage permissions to the Compute Engine default node service account gives all pods on that node full access.')">B) Grant the Storage Object Viewer role to the default Compute Engine service account.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Mounting JSON keys violates the security mandate.')">C) Mount a service account private key as a Kubernetes Secret volume.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Public buckets create a severe security vulnerability.')">D) Make the Cloud Storage bucket public with a signed URL.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview' target='_blank'>GKE Autopilot Architecture</a></li><li><a href='https://cloud.google.com/kubernetes-engine/docs/how-to/container-native-load-balancing' target='_blank'>Container-Native Load Balancing with NEGs</a></li><li><a href='https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity' target='_blank'>Workload Identity for GKE</a></li></ul>"
    },

    # 015: Serverless Compute
    {
        "topic_no": "015",
        "roadmap_id": "2.3",
        "title": "Serverless Compute: Cloud Run, Functions, and Workflows",
        "page_type": "service",
        "phase": "Phase 2 — Core Services",
        "lead": "Modern serverless system design: Cloud Run services vs jobs, concurrency tuning, cold start mitigation, event-driven triggers with Eventarc, and stateful orchestration via Workflows.",
        "comp1": ("Eventarc / HTTP", "Event Source", "control", "Emits events from Cloud Storage, Pub/Sub, or webhooks."),
        "comp2": ("Cloud Run Proxy", "Serverless Ingress", "data", "Autoscales container instances from 0 to 1000 in seconds."),
        "comp3": ("Cloud Run Container", "Stateless Microservice", "data", "Executes container handling up to 1000 concurrent requests per instance."),
        "comp4": ("Serverless VPC Connector", "VPC Direct Egress", "data", "Allows serverless containers to reach private Cloud SQL and internal VPC IPs.") ,
        "flow1": "HTTP request or Pub/Sub event arrives at Cloud Run routing proxy.",
        "flow2": "Proxy checks instance pool; if instances are at capacity, scales up fresh container within milliseconds.",
        "flow3": "Container routes database queries into private VPC through Direct VPC Egress.",
        "fail": "Sudden burst traffic causes cold-start latency spike on Java runtime.",
        "heal": "Architect configures 'min-instances=2' to maintain warm capacity pool.",
        "city_concept": "On-Demand City Kiosks & Event-Driven Delivery Crews",
        "p1": "Brightloaf Bakery was paying 24/7 for 10 servers to handle order cancellations, even though cancellations only occurred twice an hour.",
        "p2": "Tomas the Treasurer deployed on-demand popup kiosks (Cloud Run). When an order cancellation arrives, the kiosk springs open, handles the order, and vanishes.",
        "p3": "During a sudden flash mob, 500 customers rushed the kiosk. Cloud Run automatically duplicated into 20 kiosks instantaneously without dropping an order.",
        "p4": "In physical construction, popups require permits and setup crews; in Cloud Run, container instances scale to zero when idle with zero idle billing.",
        "part1_html": """
        <h3>The Situation: The Default Choice for Modern APIs</h3>
        <p>
          For modern web applications, microservices, and event processing, <strong>Cloud Run is Google Cloud's default compute recommendation</strong>. Unlike traditional serverless that forced proprietary runtimes, Cloud Run executes any standard OCI container image listening on an HTTP port. It provides genuine <strong>scale-to-zero</strong> economics (pay nothing when idle) and rapid horizontal scaling to thousands of instances.
        </p>
        <div class="callout">
          <div class="callout-title">Cloud Run Services vs Cloud Run Jobs</div>
          <ul>
            <li><strong>Cloud Run Services:</strong> Long-running HTTP endpoints listening for web requests, gRPC calls, or Pub/Sub push messages. Autoscales based on incoming request concurrency.</li>
            <li><strong>Cloud Run Jobs:</strong> Runs tasks to completion (e.g. nightly database backups, batch data processing, machine learning inference jobs). Does not listen on an HTTP port; terminates when task finishes.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Concurrency vs One-Request-Per-Instance</h4>
        <p>Unlike AWS Lambda (which executes strictly 1 request per container instance), <strong>Cloud Run handles up to 1000 concurrent requests per instance</strong> (default 80). Tuning concurrency significantly reduces costs and cold-start frequency.</p>
        <h4>Layer 2 — Practitioner: Connecting to Private VPC Resources</h4>
        <p>By default, Cloud Run has no access to private RFC 1918 VPC networks. Use <strong>Direct VPC Egress</strong> (or Serverless VPC Access connectors) to allow Cloud Run to query private Cloud SQL databases, Redis Memorystore, and internal microservices securely.</p>
        <h4>Layer 3 — Architect: Event-Driven Architectures with Eventarc</h4>
        <p>Build decoupled event pipelines using <strong>Eventarc</strong>: capture Cloud Storage bucket uploads, Cloud Audit Log events, or custom Pub/Sub messages and route them directly to Cloud Run microservices in CloudEvents format.</p>
        <h4>Layer 4 — Staff: Traffic Splitting & Blue/Green Deployments</h4>
        <p>Every deployment to Cloud Run creates an immutable <strong>Revision</strong>. Staff engineers use revision tags and gradual traffic splitting (e.g. 5% to canary, 95% to current) to execute zero-downtime rollouts with instant rollback capabilities.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, automated popup kiosks appear on street corners exactly when demand arises and vanish when the crowd disperses.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Deploying a Scalable Cloud Run Service</div>
          <pre><code># Deploy container with min-instances and private VPC egress
gcloud run deploy order-api \
  --image=us-docker.pkg.dev/brightloaf-prod/apps/order-api:v1 \
  --region=us-west1 \
  --platform=managed \
  --concurrency=80 \
  --min-instances=1 \
  --max-instances=100 \
  --allow-unauthenticated \
  --network=production-vpc \
  --subnet=serverless-subnet</code></pre>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Application (Question 1)</span>
          <p><strong>A retail company has a seasonal batch job that processes 50,000 product images once per week. The job takes 45 minutes to run and does not serve incoming HTTP traffic. Which compute service is the most cost-effective and operationally simple?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Cloud Run Jobs run containerized batch tasks to completion without HTTP listening requirements and scale to zero.')">A) Cloud Run Jobs</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud Run Services expect an HTTP server and have a default 60-minute request timeout.')">B) Cloud Run Services</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud Functions have a 9-minute execution limit in gen1 and 60 minutes in gen2, but Jobs are purpose-built for batch runs.')">C) Cloud Functions (gen1)</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Dedicated Compute Engine VM left running 24/7 incurs massive idle costs.')">D) Dedicated Compute Engine N2-standard VM left running continuously.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/run/docs/overview/what-is-cloud-run' target='_blank'>Cloud Run Documentation</a></li><li><a href='https://cloud.google.com/eventarc/docs' target='_blank'>Eventarc Event-Driven Architecture</a></li></ul>"
    },

    # 016: VPC Networking
    {
        "topic_no": "016",
        "roadmap_id": "2.4",
        "title": "Virtual Private Cloud (VPC) Networking & Security",
        "page_type": "service",
        "phase": "Phase 2 — Core Services",
        "lead": "Global software-defined enterprise networking: Custom VPCs, regional subnets, routes, hierarchical firewall policies, Shared VPC host/service projects, and Private Google Access.",
        "comp1": ("Client Browser", "External Internet", "data", "External consumer connecting via HTTPS."),
        "comp2": ("Cloud NAT", "Outbound Gateway", "data", "Enables private VMs to fetch external packages without public IPs."),
        "comp3": ("Private Compute Subnet", "VPC Subnet 10.0.1.0/24", "data", "Isolated internal subnet hosting application VMs with no external IPs."),
        "comp4": ("Cloud Router", "BGP Dynamic Router", "control", "Manages route tables and coordinates BGP routing with on-premises networks.") ,
        "flow1": "External client connects to load balancer Anycast virtual IP.",
        "flow2": "Andromeda SDN routes packet across Google private network to private backend VM.",
        "flow3": "Backend VM queries external payment API through Cloud NAT outbound translation.",
        "fail": "Engineer attempts to peer two VPCs that share identical 10.0.0.0/16 CIDRs.",
        "heal": "Control plane rejects peering; architect implements Private NAT or centralized IPAM.",
        "city_concept": "City Roadway Network, Expressways, and Gated Districts",
        "p1": "Every bakery kitchen was built directly on the public sidewalk with no fence. Thieves walked in, and delivery trucks collided at unpainted intersections.",
        "p2": "Rae the Dispatcher designed private gated industrial parks (VPC Networks) with designated avenue addresses (Subnets) and security checkpoints (Firewalls).",
        "p3": "Two districts accidentally named their streets 'Main Street 100'. Delivery trucks refused to cross the bridge due to address collisions.",
        "p4": "In physical cities, bridges can cross over each other; in VPC Network Peering, overlapping subnets fail with mathematical finality.",
        "part1_html": """
        <h3>The Situation: The Global Software-Defined Network</h3>
        <p>
          Google Cloud's <strong>Virtual Private Cloud (VPC)</strong> is fundamentally different from other cloud providers. In AWS or Azure, a VPC is bound to a single region. In Google Cloud, <strong>a VPC is a global resource</strong>. Subnets are regional, meaning a single VPC can span multiple regions worldwide, allowing instances in Frankfurt, Iowa, and Tokyo to communicate across Google's private global fiber network without traversing the public internet.
        </p>
        <div class="callout">
          <div class="callout-title">The Auto Mode vs Custom Mode Rule</div>
          Never use <strong>Auto Mode VPCs</strong> in production. Auto mode creates a pre-assigned <code>/20</code> subnet in every single Google Cloud region, using up RFC 1918 space and creating massive subnet overlap risks when connecting to on-premises networks or establishing VPC Peering. Always choose <strong>Custom Mode VPCs</strong> with explicit, deliberate CIDR allocations.
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Subnets & Secondary Ranges</h4>
        <p>Subnets are regional. In GCP, exactly <strong>4 IP addresses are reserved</strong> per subnet: <code>.0</code> (network), <code>.1</code> (default gateway), <code>.2</code> (reserved by Google), and <code>.3</code> (reserved by Google). Secondary ranges are used to allocate IP blocks for GKE Pods and Services.</p>
        <h4>Layer 2 — Practitioner: Shared VPC (The Enterprise Standard)</h4>
        <p>The standard enterprise architecture pattern is <strong>Shared VPC</strong>. A central network team manages the network in a <strong>Host Project</strong> (subnets, routes, firewall rules, VPN/Interconnect), while application teams deploy workloads in separate <strong>Service Projects</strong> attached to the host project's subnets.</p>
        <h4>Layer 3 — Architect: Private Google Access & Private Service Connect (PSC)</h4>
        <p>Private VMs without external IPs can access Google APIs (Cloud Storage, BigQuery) securely via <strong>Private Google Access</strong>. To consume internal SaaS services or multi-tenant databases without VPC peering, use <strong>Private Service Connect (PSC)</strong> endpoints.</p>
        <h4>Layer 4 — Staff: Hierarchical Firewall Policies & Andromeda SDN</h4>
        <p>Staff architects use <strong>Hierarchical Firewall Policies</strong> attached at the Organization or Folder level to enforce non-negotiable security rules (e.g. deny all inbound port 22 except from IAP) across all projects in the company.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Rae the Dispatcher ensures the citywide road network allows delivery trucks to travel smoothly without private traffic jams.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Building a Custom VPC with Private Subnets</div>
          <pre><code># 1. Create custom VPC network
gcloud compute networks create production-vpc --subnet-mode=custom

# 2. Add regional subnets
gcloud compute networks subnets create us-west-web \
  --network=production-vpc \
  --region=us-west1 \
  --range=10.10.1.0/24 \
  --enable-private-ip-google-access

# 3. Create firewall rule allowing internal traffic
gcloud compute firewall-rules create allow-internal-vpc \
  --network=production-vpc \
  --allow=tcp,udp,icmp \
  --source-ranges=10.10.0.0/16</code></pre>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: PCA Scenario (Question 1)</span>
          <p><strong>An enterprise requires central management of all network topology, subnets, and firewall rules by a dedicated infrastructure team, while allowing multiple business units to deploy VMs in isolated projects with separate billing. What architecture must you implement?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Shared VPC allows a central host project to share subnets with attached service projects.')">A) Shared VPC with a central Host Project and attached Service Projects.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'VPC Peering decentralizes firewall management and requires complex peering meshes.')">B) VPC Network Peering between independent projects.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud VPN between projects adds latency, bandwidth bottlenecks, and operational overhead.')">C) Cloud VPN tunnels between all individual projects.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Single project violates isolation and separate billing mandates.')">D) Single monolithic project containing all business unit resources.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/vpc/docs/overview' target='_blank'>Google Cloud VPC Overview</a></li><li><a href='https://cloud.google.com/vpc/docs/shared-vpc' target='_blank'>Shared VPC Architecture & Administration</a></li></ul>"
    },

    # 020: Databases
    {
        "topic_no": "020",
        "roadmap_id": "2.8",
        "title": "Databases: Cloud SQL, Spanner, Firestore, and Bigtable",
        "page_type": "service",
        "phase": "Phase 2 — Core Services",
        "lead": "The database decision matrix: Relational vs NoSQL, Cloud SQL HA topologies, Cloud Spanner 99.999% global consistency, Firestore document stores, and Bigtable IoT petabyte scaling.",
        "comp1": ("Application Backend", "Microservice Fleet", "data", "Queries transactional datastore via Private IP."),
        "comp2": ("Cloud SQL Primary", "PostgreSQL Primary", "data", "Handles active ACID transactions and writes in primary zone."),
        "comp3": ("Synchronous Standby", "Cloud SQL Standby", "data", "Maintains synchronous block replication in parallel zone for sub-minute failover."),
        "comp4": ("Cloud Spanner", "Horizontally Scalable RDBMS", "data", "Multi-region external consistency with 99.999% SLA.") ,
        "flow1": "Application executes transaction on primary database instance.",
        "flow2": "Storage layer synchronously commits write to regional persistent disk in both zones.",
        "flow3": "Read requests distribute across read replicas; analytical queries offload via Datastream to BigQuery.",
        "fail": "Primary database datacenter zone suffers hardware outage.",
        "heal": "Cloud SQL triggers automated failover to standby instance in Zone B; DNS flips in under 60 seconds.",
        "city_concept": "City Record Archives & Municipal Ledgers",
        "p1": "Brightloaf Bakery kept recipe secrets and financial ledgers in a single notebook in the kitchen drawer. A spilled cup of coffee obliterated two years of financial history.",
        "p2": "Mayor Meridian built the Central Municipal Records Hall (Cloud SQL & Spanner). All transactions are recorded in synchronized vaults across multiple city gates.",
        "p3": "During a city earthquake, the North Vault was destroyed. The South Vault instantly assumed primary ledger authority without losing a single cent.",
        "p4": "In physical archives, duplicating books takes hours; in Cloud Spanner, atomic transactions commit across continents using atomic GPS clocks.",
        "part1_html": """
        <h3>The Situation: Selecting the Right Persistence Engine</h3>
        <p>
          Data architecture determines the scalability and reliability ceiling of every cloud system. Google Cloud offers purpose-built databases engineered for distinct operational requirements. For architects, knowing <strong>which database to choose and why</strong> is heavily tested on the Professional Cloud Architect (PCA) exam.
        </p>
        <div class="callout">
          <div class="callout-title">The Master Database Selection Guide</div>
          <ul>
            <li><strong>Cloud SQL:</strong> Traditional relational (MySQL, PostgreSQL, SQL Server). Best for workloads up to a few terabytes requiring full SQL compatibility and existing ORM support.</li>
            <li><strong>Cloud Spanner:</strong> Enterprise relational with unlimited horizontal scale and <strong>99.999% SLA</strong>. ACID compliance with global external consistency. Best for mission-critical banking, global inventory, and massive transactional scale.</li>
            <li><strong>Firestore:</strong> Fully managed serverless NoSQL document database. Real-time synchronization, mobile SDKs, offline support, scale-to-zero. Best for web/mobile apps and user profiles.</li>
            <li><strong>Cloud Bigtable:</strong> Petabyte-scale, ultra-low latency NoSQL wide-column database. Millisecond response times for massive streaming writes (IoT, time-series, financial ticker data).</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Cloud SQL High Availability (HA)</h4>
        <p>Cloud SQL HA uses <strong>Regional Persistent Disks</strong> to synchronously replicate data across two zones in the same region. If the primary zone fails, the failover to the standby instance occurs automatically in under 60 seconds without data loss.</p>
        <h4>Layer 2 — Practitioner: Read Replicas vs Backups</h4>
        <p>Read replicas offload read queries, but <strong>replicas do not protect against data corruption</strong> (an accidental <code>DROP TABLE</code> replicates instantly). Always enable <strong>Point-In-Time Recovery (PITR)</strong> via automated binary logging.</p>
        <h4>Layer 3 — Architect: Cloud Spanner TrueTime & Key Design</h4>
        <p>Spanner achieves global transactions without locking bottlenecks using <strong>TrueTime</strong> (synchronized atomic clocks and GPS receivers in Google datacenters). <em>Critical Spanner Rule:</em> Never use sequential auto-incrementing primary keys; sequential keys create <strong>hotspots</strong> on single splits. Always use UUIDv4 or bit-reversed keys.</p>
        <h4>Layer 4 — Staff: Database Migration & CDC with Datastream</h4>
        <p>Staff architects execute zero-downtime database migrations from on-premises Oracle/PostgreSQL to Google Cloud using <strong>Database Migration Service (DMS)</strong> and <strong>Datastream</strong> Change Data Capture (CDC).</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, civic ledgers are replicated across secure municipal vaults to guarantee that ownership records survive any disaster.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Creating a Cloud SQL HA PostgreSQL Instance</div>
          <pre><code># Provision regional HA PostgreSQL instance with private IP
gcloud sql instances create brightloaf-prod-db \
  --database-version=POSTGRES_15 \
  --tier=db-custom-4-16384 \
  --region=us-west1 \
  --availability-type=REGIONAL \
  --storage-type=SSD \
  --storage-size=100GB \
  --storage-auto-increase \
  --backup \
  --enable-bin-log \
  --network=projects/brightloaf-prod/global/networks/production-vpc \
  --no-assign-ip</code></pre>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: PCA Scenario (Question 1)</span>
          <p><strong>A multinational payment processing corporation requires a globally distributed relational database. The system must support ACID transactions across three continents, scale horizontally to tens of thousands of write queries per second, provide strong external consistency, and guarantee 99.999% availability. Which database must you select?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Cloud Spanner is the only database in the industry offering multi-region horizontal relational scale with 99.999% SLA and external consistency.')">A) Cloud Spanner multi-region instance</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud SQL is a single-region system and cannot scale horizontally across continents.')">B) Cloud SQL for PostgreSQL with cross-region read replicas</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Bigtable is NoSQL and does not support multi-table ACID transactions or complex SQL joins.')">C) Cloud Bigtable with multi-cluster replication</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'AlloyDB is regional, not globally distributed across three continents.')">D) AlloyDB for PostgreSQL in us-central1</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/spanner/docs/true-time-external-consistency' target='_blank'>Cloud Spanner TrueTime Architecture</a></li><li><a href='https://cloud.google.com/sql/docs/postgres/high-availability' target='_blank'>Cloud SQL High Availability Overview</a></li></ul>"
    }
]

def build_core_services():
    print(f"Building {len(CORE_SERVICES_LIST)} core services topics...")
    for t in CORE_SERVICES_LIST:
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
    print("Done building core services.")

if __name__ == '__main__':
    build_core_services()
