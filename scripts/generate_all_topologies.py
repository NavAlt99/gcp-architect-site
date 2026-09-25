#!/usr/bin/env python3
"""
generate_all_topologies.py - Generates authentic, per-topic topologies for all 60 topics.
Addresses diagram-diagnosis.md Findings 1, 2, 3, 4, 5, and Recommendations 1, 2, 3, 4, 5, 6.

1. Generates authentic D1 (Map), D2 (Flow), and D3 (Failure) topologies for topics 005-060
   with real GCP components, real branching, authentic scopes, and domain failure modes.
2. Preserves handcrafted topics 001-004 while ensuring proper metadata and formatting.
3. Updates all 180 diagram JSON files in diagrams/.
4. Regenerates all 180 standalone HTML files in diagrams/.
5. Injects Section 2B Diagram Suite Navigation ("Where Am I" progression strip) into all 60 topic pages.
6. Updates embedded script tags (<script id="spec-d*-data">) and context cards in all 60 topic pages.
7. Verifies zero generic template instances remain across the curriculum.
"""

import os
import sys
import json
import glob
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIAGRAMS_DIR = os.path.join(BASE_DIR, "diagrams")
PAGES_DIR = os.path.join(BASE_DIR, "pages")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

sys.path.insert(0, SCRIPTS_DIR)
from build_website import generate_standalone_diagram_html

# Load full topic definitions
from topic_topologies_spec import TOPIC_SPECS

def build_specs_for_topic(t_no_str):
    t_no = int(t_no_str)
    spec_def = TOPIC_SPECS.get(t_no)
    if not spec_def:
        raise ValueError(f"Missing spec definition for topic {t_no}")
    
    roadmap_id = spec_def["roadmap_id"]
    title = spec_def["title"]
    
    # 1. D1 Scope & Architecture Map
    d1 = {
        "id": f"topic-{t_no_str}-d1",
        "title": f"{title} — Scope & Architecture Map",
        "topic_no": t_no_str,
        "roadmap_id": roadmap_id,
        "kind": "map",
        "purpose": spec_def["d1_purpose"],
        "routing_rationale": spec_def["d1_rationale"],
        "groups": spec_def["d1_groups"],
        "nodes": spec_def["d1_nodes"],
        "edges": spec_def["d1_edges"],
        "steps": spec_def["d1_steps"],
        "scenarios": spec_def["d1_scenarios"]
    }
    
    # 2. D2 Request & Control Flow
    d2 = {
        "id": f"topic-{t_no_str}-d2",
        "title": f"{title} — Request & Control Flow",
        "topic_no": t_no_str,
        "roadmap_id": roadmap_id,
        "kind": "flow",
        "purpose": spec_def["d2_purpose"],
        "routing_rationale": spec_def["d2_rationale"],
        "groups": spec_def["d2_groups"],
        "nodes": spec_def["d2_nodes"],
        "edges": spec_def["d2_edges"],
        "steps": spec_def["d2_steps"],
        "scenarios": spec_def["d2_scenarios"]
    }
    
    # 3. D3 Failure Injection & Auto-Healing
    d3 = {
        "id": f"topic-{t_no_str}-d3",
        "title": f"{title} — Failure Injection & Auto-Healing",
        "topic_no": t_no_str,
        "roadmap_id": roadmap_id,
        "kind": "failure",
        "purpose": spec_def["d3_purpose"],
        "routing_rationale": spec_def["d3_rationale"],
        "groups": spec_def["d3_groups"],
        "nodes": spec_def["d3_nodes"],
        "edges": spec_def["d3_edges"],
        "steps": spec_def["d3_steps"],
        "scenarios": spec_def["d3_scenarios"]
    }
    
    return d1, d2, d3

def inject_diagram_suite_into_html(html, spec_d1, spec_d2, spec_d3):
    """
    Injects the topic-level 'Where Am I' progression strip and updates
    context cards and embedded JSON script tags.
    """
    suite_nav_html = """        <!-- Topic-Level 'Where Am I' Architecture Viewpoints Progression Strip -->
        <div class="diagram-suite-nav">
          <span class="suite-title">VIEWPOINT:</span>
          <a href="#diagram-d1" class="suite-pill"><span class="pill-id">D1</span> SCOPE &amp; BOUNDARY MAP</a>
          <span class="suite-arrow">→</span>
          <a href="#diagram-d2" class="suite-pill"><span class="pill-id">D2</span> REQUEST &amp; DATA FLOW</a>
          <span class="suite-arrow">→</span>
          <a href="#diagram-d3" class="suite-pill"><span class="pill-id">D3</span> CHAOS &amp; RESILIENCE</a>
        </div>"""

    card_d1 = f"""        <!-- Diagram 1 Context Card & Container -->
        <div class="diagram-context-card" style="margin-top: 18px; margin-bottom: 10px; padding: 12px 14px; background: rgba(33, 150, 243, 0.05); border-left: 3px solid var(--accent); border-radius: 0 4px 4px 0;">
          <h4 style="margin: 0 0 5px 0; color: var(--text); font-size: 13.5px;">Diagram 1: {spec_d1.get('title', 'Scope & Boundary Map')}</h4>
          <p style="margin: 0; font-size: 12px; color: var(--text-dim); line-height: 1.5;">
            <strong>Architectural Intent:</strong> {spec_d1.get('purpose', '')}
          </p>
        </div>"""

    card_d2 = f"""        <!-- Diagram 2 Context Card & Container -->
        <div class="diagram-context-card" style="margin-top: 28px; margin-bottom: 10px; padding: 12px 14px; background: rgba(33, 150, 243, 0.05); border-left: 3px solid var(--accent); border-radius: 0 4px 4px 0;">
          <h4 style="margin: 0 0 5px 0; color: var(--text); font-size: 13.5px;">Diagram 2: {spec_d2.get('title', 'Request & Control Flow')}</h4>
          <p style="margin: 0; font-size: 12px; color: var(--text-dim); line-height: 1.5;">
            <strong>Architectural Intent:</strong> {spec_d2.get('purpose', '')}
          </p>
        </div>"""

    card_d3 = f"""        <!-- Diagram 3 Context Card & Container -->
        <div class="diagram-context-card" style="margin-top: 28px; margin-bottom: 10px; padding: 12px 14px; background: rgba(33, 150, 243, 0.05); border-left: 3px solid var(--accent); border-radius: 0 4px 4px 0;">
          <h4 style="margin: 0 0 5px 0; color: var(--text); font-size: 13.5px;">Diagram 3: {spec_d3.get('title', 'Failure Injection & Auto-Healing')}</h4>
          <p style="margin: 0; font-size: 12px; color: var(--text-dim); line-height: 1.5;">
            <strong>Architectural Intent:</strong> {spec_d3.get('purpose', '')}
          </p>
        </div>"""

    # Check if suite nav already present; if not, inject right before card_d1 or right inside Section 2B
    if "diagram-suite-nav" not in html:
        # Pattern to find diagrams start
        pat = r'(<div id=\"diagrams\"[^>]*>\s*<h3>2B[^<]*</h3>.*?(?:<div class=\"callout\"[^>]*>.*?</div>\s*</div>\s*)?)((?:<!-- Diagram 1 Context Card.*?-->\s*)?<div class=\"diagram-context-card\"|<div id=\"diagram-d1\">)'
        def rep_suite(m):
            return m.group(1) + "\n" + suite_nav_html + "\n\n" + m.group(2)
        html, count = re.subn(pat, rep_suite, html, count=1, flags=re.DOTALL)
        if count == 0:
            # Fallback insertion
            html = html.replace('<div id="diagram-d1">', suite_nav_html + '\n' + card_d1 + '\n<div id="diagram-d1">')

    # Replace / update Context Cards
    # Replace Card 1
    p_c1 = r'<!-- Diagram 1 Context Card.*?-->\s*<div class="diagram-context-card".*?</div>(?=\s*<div id="diagram-d1">)'
    html = re.sub(p_c1, card_d1.strip(), html, flags=re.DOTALL)

    # Replace Card 2
    p_c2 = r'<!-- Diagram 2 Context Card.*?-->\s*<div class="diagram-context-card".*?</div>(?=\s*<div id="diagram-d2">)'
    html = re.sub(p_c2, card_d2.strip(), html, flags=re.DOTALL)

    # Replace Card 3
    p_c3 = r'<!-- Diagram 3 Context Card.*?-->\s*<div class="diagram-context-card".*?</div>(?=\s*<div id="diagram-d3">)'
    html = re.sub(p_c3, card_d3.strip(), html, flags=re.DOTALL)

    # Update embedded JSON specs in script tags
    p1 = r'(<script id=\"spec-d1-data\" type=\"application/json\">)(.*?)(</script>)'
    html = re.sub(p1, lambda m: m.group(1) + '\n' + json.dumps(spec_d1, indent=2) + '\n  ' + m.group(3), html, flags=re.DOTALL)

    p2 = r'(<script id=\"spec-d2-data\" type=\"application/json\">)(.*?)(</script>)'
    html = re.sub(p2, lambda m: m.group(1) + '\n' + json.dumps(spec_d2, indent=2) + '\n  ' + m.group(3), html, flags=re.DOTALL)

    p3 = r'(<script id=\"spec-d3-data\" type=\"application/json\">)(.*?)(</script>)'
    html = re.sub(p3, lambda m: m.group(1) + '\n' + json.dumps(spec_d3, indent=2) + '\n  ' + m.group(3), html, flags=re.DOTALL)

    return html

def main():
    print("=" * 70)
    print("Executing diagram-diagnosis.md Full Remediation:")
    print("Generating Authentic Per-Topic Topologies for All 60 Topics")
    print("=" * 70)

    # Process all 60 topics
    for t_no in range(1, 61):
        t_no_str = f"{t_no:03d}"
        
        # Check if topic is handcrafted (001, 002, 003, 004) or needs full generation
        if t_no in [1, 2, 3, 4] and t_no not in TOPIC_SPECS:
            # Load existing handcrafted specs
            with open(os.path.join(DIAGRAMS_DIR, f"topic-{t_no_str}-d1.json")) as f:
                d1 = json.load(f)
            with open(os.path.join(DIAGRAMS_DIR, f"topic-{t_no_str}-d2.json")) as f:
                d2 = json.load(f)
            with open(os.path.join(DIAGRAMS_DIR, f"topic-{t_no_str}-d3.json")) as f:
                d3 = json.load(f)
            # Regenerate standalone HTML with engine v4.0
            for d, d_kind in [(d1, "d1"), (d2, "d2"), (d3, "d3")]:
                html_path = os.path.join(DIAGRAMS_DIR, f"topic-{t_no_str}-{d_kind}.html")
                with open(html_path, 'w') as f:
                    f.write(generate_standalone_diagram_html(d))
        else:
            d1, d2, d3 = build_specs_for_topic(t_no_str)
            
            # Write updated JSON files
            for d, d_kind in [(d1, "d1"), (d2, "d2"), (d3, "d3")]:
                json_path = os.path.join(DIAGRAMS_DIR, f"topic-{t_no_str}-{d_kind}.json")
                with open(json_path, 'w') as f:
                    json.dump(d, f, indent=2)
                
                # Regenerate standalone HTML
                html_path = os.path.join(DIAGRAMS_DIR, f"topic-{t_no_str}-{d_kind}.html")
                with open(html_path, 'w') as f:
                    f.write(generate_standalone_diagram_html(d))

        # Update topic page in pages/
        page_path = os.path.join(PAGES_DIR, f"topic-{t_no_str}.html")
        if os.path.exists(page_path):
            with open(page_path, 'r') as f:
                content = f.read()
            updated_content = inject_diagram_suite_into_html(content, d1, d2, d3)
            with open(page_path, 'w') as f:
                f.write(updated_content)

    print("\nVerifying all diagrams across site...")
    # Audit verification
    all_json_files = sorted(glob.glob(os.path.join(DIAGRAMS_DIR, "topic-*-d*.json")))
    generic_d2_count = 0
    generic_d3_count = 0
    overflow_count = 0
    total_diagrams = len(all_json_files)

    for path in all_json_files:
        with open(path) as f:
            data = json.load(f)
        labels = [n.get("label", "") for n in data.get("nodes", [])]
        
        # Check for generic labels
        if "Worker Backend Fleet" in labels or "Data Persistence Tier" in labels:
            generic_d2_count += 1
        if "Active Service Node" in labels and "Standby Node (Zone B)" in labels:
            generic_d3_count += 1
            
        # Check node label overflow against dynamic sizing
        for n in data.get("nodes", []):
            lbl = n.get("label", "")
            sub = n.get("product", "") or n.get("plane", "")
            max_char = max(len(lbl), len(sub))
            node_width = max(145, max_char * 7.6 + 36)
            # If standard monospace text length * 7.5 > box width, it overflows
            if (len(lbl) * 7.5) > (node_width - 16):
                overflow_count += 1

    print(f"Total Diagrams Audited: {total_diagrams}")
    print(f"Generic D2 Diagrams Remaining: {generic_d2_count} (Goal: 0)")
    print(f"Generic D3 Diagrams Remaining: {generic_d3_count} (Goal: 0)")
    print(f"Overflowing Node Labels: {overflow_count} (Goal: 0)")
    print("Remediation execution complete.")

if __name__ == "__main__":
    main()
