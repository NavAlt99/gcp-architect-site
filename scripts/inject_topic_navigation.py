#!/usr/bin/env python3
"""
inject_topic_navigation.py - Adds complete multi-point navigation across the generated topic catalog:
1. Header Topic Switcher with quick Prev/Next and a phase-grouped dropdown
2. Breadcrumb / Progress sub-nav bar
3. Bottom Topic Pagination Cards (Prev, Roadmap Index, Next)
4. Persistent Floating Quick Navigation Dock (bottom-right)
5. Keyboard Shortcuts (P = Prev, N = Next, I = Index, Alt+Left/Right)
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_DIR = os.path.join(BASE_DIR, "pages")

# Legacy fallback catalog. At runtime this is replaced with the generated page catalog.
TOPICS = [
    ("001", "0.1", "Networking Fundamentals", "concept", "Phase 0 — Prerequisites"),
    ("002", "0.2", "Linux & Command Line for Architects", "concept", "Phase 0 — Prerequisites"),
    ("003", "0.3", "Virtualization and Containers", "concept", "Phase 0 — Prerequisites"),
    ("004", "0.4", "Cloud Concepts & Operating Models", "concept", "Phase 0 — Prerequisites"),
    ("005", "0.5", "Software Architecture & Delivery Basics", "concept", "Phase 0 — Prerequisites"),
    ("006", "0.6", "Cloud Digital Leader & Business Foundations", "concept", "Phase 0 — Prerequisites"),
    
    ("007", "1.1", "Account, Tools and Access", "service", "Phase 1 — GCP Foundations"),
    ("008", "1.2", "Resource Hierarchy & Org Policies", "service", "Phase 1 — GCP Foundations"),
    ("009", "1.3", "Identity Basics: IAM & Service Accounts", "service", "Phase 1 — GCP Foundations"),
    ("010", "1.4", "Billing, Cost Hygiene, and FinOps", "service", "Phase 1 — GCP Foundations"),
    ("011", "1.5", "Global Infrastructure & Network Tiers", "service", "Phase 1 — GCP Foundations"),
    ("012", "1.6", "Support, Governance & Asset Inventory", "concept", "Phase 1 — GCP Foundations"),
    
    ("013", "2.1", "Compute Engine: VMs & Managed Instance Groups", "service", "Phase 2 — Core Services"),
    ("014", "2.2", "Google Kubernetes Engine (GKE)", "service", "Phase 2 — Core Services"),
    ("015", "2.3", "Serverless Compute: Cloud Run & Functions", "service", "Phase 2 — Core Services"),
    ("016", "2.4", "Virtual Private Cloud (VPC) Networking", "service", "Phase 2 — Core Services"),
    ("017", "2.5", "Cloud Load Balancing, CDN & Cloud Armor", "service", "Phase 2 — Core Services"),
    ("018", "2.6", "Hybrid & Multi-Cloud Connectivity", "service", "Phase 2 — Core Services"),
    ("019", "2.7", "Cloud Storage & Enterprise Filesystems", "service", "Phase 2 — Core Services"),
    ("020", "2.8", "Databases: Cloud SQL, Spanner & Bigtable", "service", "Phase 2 — Core Services"),
    ("021", "2.9", "Messaging & Integration: Pub/Sub & Tasks", "service", "Phase 2 — Core Services"),

    ("022", "3.1", "Requirements Analysis: Discovery", "concept", "Phase 3 — Architecture Thinking"),
    ("023", "3.2", "Google Cloud Architecture Framework", "concept", "Phase 3 — Architecture Thinking"),
    ("024", "3.3", "Reference Architectures & Patterns", "concept", "Phase 3 — Architecture Thinking"),
    ("025", "3.4", "Migration & Modernization: The 6 Rs", "concept", "Phase 3 — Architecture Thinking"),
    ("026", "3.4b", "Decision Frameworks: ADRs & Matrices", "concept", "Phase 3 — Architecture Thinking"),
    ("027", "3.5", "Diagramming & Docs: C4 Model", "concept", "Phase 3 — Architecture Thinking"),

    ("028", "4.1", "Reliability Fundamentals & Availability", "concept", "Phase 4 — Reliability & HA"),
    ("029", "4.2", "SRE Concepts: SLIs, SLOs & Error Budgets", "concept", "Phase 4 — Reliability & HA"),
    ("030", "4.3", "High Availability by Layer", "service", "Phase 4 — Reliability & HA"),
    ("031", "4.4", "Disaster Recovery Patterns (RTO & RPO)", "concept", "Phase 4 — Reliability & HA"),
    ("032", "4.5", "Observability: Monitoring, Logs & Trace", "service", "Phase 4 — Reliability & HA"),
    ("033", "4.6", "Testing for Reliability: Load & Chaos", "concept", "Phase 4 — Reliability & HA"),

    ("034", "5.1", "Advanced IAM, Federation & Zero Trust", "service", "Phase 5 — Security & Compliance"),
    ("035", "5.2", "Network Security: VPC-SC & Cloud Armor", "service", "Phase 5 — Security & Compliance"),
    ("036", "5.3", "Data Protection: Cloud KMS & DLP", "service", "Phase 5 — Security & Compliance"),
    ("037", "5.4", "Compliance, Governance & Assured Workloads", "concept", "Phase 5 — Security & Compliance"),
    ("038", "5.5", "Security Operations & Threat Detection", "service", "Phase 5 — Security & Compliance"),
    ("039", "5.5b", "Application & Supply-Chain Security (SLSA)", "concept", "Phase 5 — Security & Compliance"),

    ("040", "6.1", "Cost Optimization & FinOps", "concept", "Phase 6 — Optimization & Ops"),
    ("041", "6.2", "Performance Optimization & Bottlenecks", "concept", "Phase 6 — Optimization & Ops"),
    ("042", "6.3", "Infrastructure as Code: Terraform & GitOps", "service", "Phase 6 — Optimization & Ops"),
    ("043", "6.4", "CI/CD & Release Engineering: Cloud Deploy", "service", "Phase 6 — Optimization & Ops"),
    ("044", "6.5", "Operations & Platform Engineering", "concept", "Phase 6 — Optimization & Ops"),

    ("045", "7.1", "Case Analysis Method & Discovery Framework", "concept", "Phase 7 — Case Studies & Exam"),
    ("046", "7.4a", "Case Study: EHR Healthcare", "case-study", "Phase 7 — Case Studies & Exam"),
    ("047", "7.4b", "Case Study: Mountkirk Games", "case-study", "Phase 7 — Case Studies & Exam"),
    ("048", "7.4c", "Case Study: TerramEarth", "case-study", "Phase 7 — Case Studies & Exam"),
    ("049", "7.4d", "Case Study: Helicopter Racing League", "case-study", "Phase 7 — Case Studies & Exam"),
    ("050", "7.5", "PCA Exam Strategy & Keyword Elimination", "concept", "Phase 7 — Case Studies & Exam"),

    ("051", "D.1", "Data Warehousing: BigQuery & Looker", "service", "Data, Analytics & ML"),
    ("052", "D.2", "Data Processing: Dataflow & Dataproc", "service", "Data, Analytics & ML"),
    ("053", "D.3", "Data Lake, Lakehouse & BigLake", "service", "Data, Analytics & ML"),
    ("054", "D.4", "Machine Learning: Vertex AI Architecture", "service", "Data, Analytics & ML"),

    ("055", "CS.1", "Compute Decision Cheat Sheet", "cheat-sheet", "Service Decision Cheat Sheets"),
    ("056", "CS.2", "Database Decision Cheat Sheet", "cheat-sheet", "Service Decision Cheat Sheets"),
    ("057", "CS.3", "Load Balancer Decision Cheat Sheet", "cheat-sheet", "Service Decision Cheat Sheets"),
    ("058", "CS.4", "Hybrid Connectivity Decision Cheat Sheet", "cheat-sheet", "Service Decision Cheat Sheets"),
    ("059", "CS.5", "Storage & Messaging Decision Cheat Sheet", "cheat-sheet", "Service Decision Cheat Sheets"),
    ("060", "CS.6", "Key Numbers, Limits & SLAs to Memorise", "cheat-sheet", "Service Decision Cheat Sheets")
]


def load_generated_topics():
    """Read navigation metadata from every generated page, including the tail topics."""
    from pathlib import Path
    from repair_site import page_meta

    rows = []
    for path in Path(PAGES_DIR).glob("topic-*.html"):
        meta = page_meta(path)
        if meta["roadmap_id"]:
            rows.append((meta["topic_no"], meta["roadmap_id"], meta["title"], meta["page_type"], meta["phase"]))
    return sorted(rows, key=lambda item: int(item[0]))


generated_topics = load_generated_topics()
if generated_topics:
    TOPICS = generated_topics

# Build dropdown options once
def build_dropdown_options(current_topic_no):
    phases = []
    seen = set()
    for item in TOPICS:
        p = item[4]
        if p not in seen:
            seen.add(p)
            phases.append(p)
    
    html_parts = []
    for p in phases:
        items = [t for t in TOPICS if t[4] == p]
        html_parts.append(f'            <optgroup label="{p}">')
        for it in items:
            sel = ' selected' if it[0] == current_topic_no else ''
            title_clean = it[2] if len(it[2]) <= 32 else it[2][:30] + '…'
            html_parts.append(f'              <option value="topic-{it[0]}.html"{sel}>{it[0]} [{it[1]}] {title_clean}</option>')
        html_parts.append('            </optgroup>')
    return "\n".join(html_parts)

def enrich_topic_page(idx):
    item = TOPICS[idx]
    topic_no, roadmap_id, title, page_type, phase = item
    prev_item = TOPICS[idx - 1] if idx > 0 else None
    next_item = TOPICS[idx + 1] if idx + 1 < len(TOPICS) else None
    
    file_path = os.path.join(PAGES_DIR, f"topic-{topic_no}.html")
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} does not exist!")
        return False
        
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Header Navigation Switcher
    if prev_item:
        prev_url = f"topic-{prev_item[0]}.html"
        header_prev_arrow = f'<a href="{prev_url}" class="nav-topic-arrow prev" title="Previous Topic: {prev_item[2]} [Key: P]">‹</a>'
        subnav_prev_btn = f'<a href="{prev_url}" class="subnav-nav-btn prev" title="{prev_item[2]}">← Prev ({prev_item[0]})</a>'
        dock_prev_btn = f'<a href="{prev_url}" class="dock-btn prev" title="Previous Topic: {prev_item[2]} [Key: P]">← {prev_item[0]}</a>'
        pagination_prev = f"""      <!-- Previous Topic -->
      <a href="{prev_url}" class="pagination-card prev">
        <div class="pagination-direction">← PREVIOUS TOPIC</div>
        <div class="pagination-topic-meta">{prev_item[4]} • [{prev_item[1]}]</div>
        <div class="pagination-title">{prev_item[0]}: {prev_item[2]}</div>
        <div class="pagination-shortcut">Shortcut: <kbd>P</kbd> or <kbd>←</kbd></div>
      </a>"""
    else:
        prev_url = "../index.html"
        header_prev_arrow = '<a href="../index.html" class="nav-topic-arrow prev disabled" title="Start of Roadmap (Topic 001)">‹</a>'
        subnav_prev_btn = '<span class="subnav-nav-btn prev disabled">← Prev</span>'
        dock_prev_btn = '<span class="dock-btn prev disabled">← 001</span>'
        pagination_prev = """      <!-- Previous Topic (Start of Curriculum) -->
      <a href="../index.html" class="pagination-card prev">
        <div class="pagination-direction">← ROADMAP START</div>
        <div class="pagination-topic-meta">Curriculum Overview</div>
        <div class="pagination-title">Topic 001: Networking Fundamentals</div>
        <div class="pagination-shortcut">Shortcut: <kbd>P</kbd> or <kbd>I</kbd></div>
      </a>"""

    if next_item:
        next_url = f"topic-{next_item[0]}.html"
        header_next_arrow = f'<a href="{next_url}" class="nav-topic-arrow next" title="Next Topic: {next_item[2]} [Key: N]">›</a>'
        subnav_next_btn = f'<a href="{next_url}" class="subnav-nav-btn next" title="{next_item[2]}">Next ({next_item[0]}) →</a>'
        dock_next_btn = f'<a href="{next_url}" class="dock-btn next" title="Next Topic: {next_item[2]} [Key: N]">{next_item[0]} →</a>'
        pagination_next = f"""      <!-- Next Topic -->
      <a href="{next_url}" class="pagination-card next">
        <div class="pagination-direction">NEXT TOPIC →</div>
        <div class="pagination-topic-meta">{next_item[4]} • [{next_item[1]}]</div>
        <div class="pagination-title">{next_item[0]}: {next_item[2]}</div>
        <div class="pagination-shortcut">Shortcut: <kbd>N</kbd> or <kbd>→</kbd></div>
      </a>"""
    else:
        next_url = "../index.html"
        header_next_arrow = f'<a href="../index.html" class="nav-topic-arrow next disabled" title="End of Roadmap (Topic {TOPICS[-1][0]})">›</a>'
        subnav_next_btn = '<span class="subnav-nav-btn next disabled">Next →</span>'
        dock_next_btn = f'<span class="dock-btn next disabled">{TOPICS[-1][0]} →</span>'
        pagination_next = f"""      <!-- Next Topic (End of Curriculum) -->
      <a href="../index.html" class="pagination-card next">
        <div class="pagination-direction">ROADMAP COMPLETED ✓</div>
        <div class="pagination-topic-meta">All {len(TOPICS)} Topics Mastered</div>
        <div class="pagination-title">Return to Architecture Explorer</div>
        <div class="pagination-shortcut">Shortcut: <kbd>N</kbd> or <kbd>I</kbd></div>
      </a>"""

    dropdown_options = build_dropdown_options(topic_no)
    
    # 1. Update Header Navigation
    # Replace existing <header class="site-nav">...</header>
    new_header = f"""  <!-- Navigation -->
  <header class="site-nav">
    <div class="nav-container">
      <a href="../index.html" class="brand-link">
        <span style="font-size:16px;">☁</span>
        <span class="brand-text">GCP ARCHITECT ROADMAP</span>
      </a>

      <!-- Quick Topic Navigator -->
      <div class="nav-topic-switcher">
        {header_prev_arrow}
        <div class="nav-select-wrapper">
          <select class="nav-topic-select" onchange="if(this.value) window.location.href=this.value;" title="Quick Jump to Any Topic">
{dropdown_options}
          </select>
        </div>
        {header_next_arrow}
      </div>

      <nav class="nav-links">
        <a href="../index.html" class="nav-link">Overview</a>
        <a href="#diagrams" class="nav-link">Diagrams</a>
        <a href="#demo-or-practice" class="nav-link">Labs</a>
        <a href="#quiz" class="nav-link">Knowledge Check</a>
      </nav>
    </div>
  </header>"""

    html = re.sub(r'<!-- Navigation -->\s*<header class="site-nav">[\s\S]*?</header>', new_header, html)

    # 2. Add Breadcrumb / Sub-Navigation Strip (Right after <main class="main-content">)
    subnav_strip = f"""
    <!-- Topic Sub-Navigation Strip -->
    <nav class="topic-subnav-strip" aria-label="Topic Sub-Navigation">
      <div class="subnav-breadcrumbs">
        <a href="../index.html" class="crumb-home">🗺 Roadmap Index</a>
        <span class="crumb-sep">/</span>
        <span class="crumb-phase">{phase}</span>
        <span class="crumb-sep">/</span>
        <span class="crumb-current">Topic {topic_no}</span>
      <span class="crumb-progress">({idx + 1} of {len(TOPICS)})</span>
      </div>
      <div class="subnav-actions">
        {subnav_prev_btn}
        <a href="../index.html" class="subnav-nav-btn" title="View all topics">☰ Index</a>
        {subnav_next_btn}
      </div>
    </nav>
"""
    # Remove existing subnav strip if re-running
    html = re.sub(r'<!-- Topic Sub-Navigation Strip -->[\s\S]*?</nav>\s*', '', html)
    # Insert right after <main class="main-content">
    html = re.sub(r'(<main class="main-content">)', r'\1' + subnav_strip, html)

    # 3. Add Bottom Topic Pagination Cards (Right before </main>)
    # Remove existing pagination if re-running
    html = re.sub(r'<!-- Topic Pagination Footer -->[\s\S]*?</nav>\s*', '', html)
    
    pagination_section = f"""
    <!-- Topic Pagination Footer -->
    <nav class="topic-pagination" aria-label="Topic Pagination">
{pagination_prev}

      <!-- Roadmap Overview -->
      <a href="../index.html" class="pagination-card index" title="Return to All Topics Index">
        <div class="pagination-direction">ROADMAP OVERVIEW</div>
        <div class="pagination-topic-meta">All {len(TOPICS)} Topics • 7+ Phases</div>
        <div class="pagination-title">Architecture Explorer</div>
        <div class="pagination-shortcut">Key: <kbd>I</kbd></div>
      </a>

{pagination_next}
    </nav>
"""
    html = re.sub(r'(\s*</main>)', pagination_section + r'\1', html)

    # 4. Add Floating Quick Navigation Dock & Keyboard Navigation Script
    # Remove existing floating dock & keyboard script if re-running
    html = re.sub(r'<!-- Floating Quick Navigation Dock -->[\s\S]*?<!-- End Floating Quick Navigation Dock -->\s*', '', html)

    prev_target = prev_url if prev_item else ''
    next_target = next_url if next_item else ''

    floating_and_script = f"""  <!-- Floating Quick Navigation Dock -->
  <div class="floating-topic-dock" id="floating-topic-dock">
    {dock_prev_btn}
    <span class="dock-indicator" title="Topic {topic_no} of {len(TOPICS)}">{topic_no} / {TOPICS[-1][0]}</span>
    {dock_next_btn}
    <a href="../index.html" class="dock-btn index" title="Roadmap Overview [Key: I]">☰</a>
  </div>

  <script>
    // Global Keyboard Navigation between topics
    (function() {{
      const prevUrl = "{prev_target}";
      const nextUrl = "{next_target}";
      document.addEventListener('keydown', (e) => {{
        if (['INPUT', 'TEXTAREA', 'SELECT'].includes(e.target.tagName) || e.target.isContentEditable) return;
        if (e.key === 'p' || e.key === 'P' || e.key === '[' || (e.key === 'ArrowLeft' && e.altKey)) {{
          if (prevUrl) window.location.href = prevUrl;
        }} else if (e.key === 'n' || e.key === 'N' || e.key === ']' || (e.key === 'ArrowRight' && e.altKey)) {{
          if (nextUrl) window.location.href = nextUrl;
        }} else if (e.key === 'i' || e.key === 'I') {{
          window.location.href = '../index.html';
        }}
      }});
    }})();
  </script>
  <!-- End Floating Quick Navigation Dock -->
"""
    html = re.sub(r'(\s*</body>)', '\n' + floating_and_script + r'\1', html)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
        
    return True

def main():
    print(f"Injecting full navigation system into all {len(TOPICS)} generated topic pages...")
    success_count = 0
    for i in range(len(TOPICS)):
        if enrich_topic_page(i):
            success_count += 1
    print(f"Successfully injected navigation into {success_count}/{len(TOPICS)} pages.")

if __name__ == "__main__":
    main()
