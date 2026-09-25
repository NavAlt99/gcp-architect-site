#!/usr/bin/env python3
"""
build_website.py - Comprehensive generator for GCP Architect Roadmap Learning Site
Adheres to gcp-architect-zine-site-prompt-NoImage.md and Kubernetes Apartment Style Lock.
"""

import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_DIR = os.path.join(BASE_DIR, "pages")
DIAGRAMS_DIR = os.path.join(BASE_DIR, "diagrams")
ANALOGY_DIR = os.path.join(BASE_DIR, "analogy")
GENERATED_DIR = os.path.join(BASE_DIR, "generated")

os.makedirs(PAGES_DIR, exist_ok=True)
os.makedirs(DIAGRAMS_DIR, exist_ok=True)
os.makedirs(ANALOGY_DIR, exist_ok=True)
os.makedirs(GENERATED_DIR, exist_ok=True)

# Shared HTML Header template matching Kubernetes Apartment / JetBrains Mono Theme
HTML_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{topic_no} ({roadmap_id}) {title} | GCP Architect Explorer</title>
  <link rel="stylesheet" href="../assets/site.css">
  <link rel="stylesheet" href="../assets/diagram-engine.css">
</head>
<body>

  <!-- Navigation -->
  <header class="site-nav">
    <div class="nav-container">
      <a href="../index.html" class="brand-link">
        <span style="font-size:16px;">☁</span>
        <span class="brand-text">GCP ARCHITECT ROADMAP</span>
      </a>
      <nav class="nav-links">
        <a href="../index.html" class="nav-link">Architecture Explorer</a>
        <a href="#diagrams" class="nav-link">Interactive Diagrams</a>
        <a href="#demo-or-practice" class="nav-link">{demo_or_practice_label}</a>
        <a href="#quiz" class="nav-link">Knowledge Check</a>
      </nav>
    </div>
  </header>

  <main class="main-content">
    
    <!-- Topic Header -->
    <header class="page-header">
      <div class="page-meta">
        <span class="badge">Topic {topic_no}</span>
        <span class="badge badge-type">Roadmap ID: {roadmap_id}</span>
        <span class="badge" style="background:#1c1006; color:#fb923c; border-color:#f97316;">{phase}</span>
        <span class="badge badge-type">Type: {page_type}</span>
        <span style="font-size:11px; color:var(--text-dim); margin-left:auto;">Verified: 2026-09-24</span>
      </div>
      <h1 class="page-title">{title}</h1>
      <p class="page-lead">{lead}</p>
    </header>
"""

HTML_FOOTER = """
  </main>

  <footer style="text-align: center; padding: 24px; color: var(--text-dim); font-size: 11px; border-top: 1px solid var(--panel-border);">
    Google Cloud Architect Roadmap • Minimalist Systems Design • 100% Static & Offline Compatible
  </footer>

  <!-- Embedded Data & Scripts (Zero Fetch / 100% Offline & File:// Compatible) -->
  <script id="spec-d1-data" type="application/json">
{spec_d1_json}
  </script>
  <script id="spec-d2-data" type="application/json">
{spec_d2_json}
  </script>
  <script id="spec-d3-data" type="application/json">
{spec_d3_json}
  </script>
  <script id="analogy-data" type="application/json">
{analogy_json}
  </script>

  <script src="../assets/diagram-engine.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      const specD1 = JSON.parse(document.getElementById('spec-d1-data').textContent);
      const specD2 = JSON.parse(document.getElementById('spec-d2-data').textContent);
      const specD3 = JSON.parse(document.getElementById('spec-d3-data').textContent);
      window.analogyData = JSON.parse(document.getElementById('analogy-data').textContent);

      new DiagramEngine('diagram-d1', specD1);
      new DiagramEngine('diagram-d2', specD2);
      new DiagramEngine('diagram-d3', specD3);

      showAnalogyBeat(1);
    }});

    function showAnalogyBeat(stepNum) {{
      if (!window.analogyData) return;
      const beat = window.analogyData.beats.find(b => b.step === stepNum);
      if (!beat) return;

      const container = document.getElementById('analogy-display');
      container.innerHTML = `
        <h4 style="margin-top:0; color:var(--accent);">Beat ${{beat.step}}: ${{beat.name}}</h4>
        <p style="font-size:12.5px; line-height:1.6; color:var(--text-main);">${{beat.story}}</p>
        <div style="font-size:11.5px; color:var(--text-dim);">
          <strong style="color:#fb923c;">Analogy Tokens:</strong> ${{beat.analogy_elements.join(' • ')}}
        </div>
      `;

      document.querySelectorAll('.stepper-btn').forEach((btn, idx) => {{
        btn.classList.toggle('active', (idx + 1) === stepNum);
      }});
    }}

    function toggleSolution() {{
      const block = document.getElementById('solution-block');
      const btn = document.getElementById('toggle-solution-btn');
      if (block.style.display === 'none') {{
        block.style.display = 'block';
        btn.textContent = '🙈 Hide Solution & Rubric';
      }} else {{
        block.style.display = 'none';
        btn.textContent = '👁 Show Solution & Rubric';
      }}
    }}

    function checkQuiz(element, isCorrect, explanation) {{
      const card = element.closest('.quiz-card');
      const options = card.querySelectorAll('.quiz-option');
      options.forEach(opt => {{
        opt.style.borderColor = 'var(--panel-border)';
        opt.style.background = 'var(--panel)';
      }});

      element.style.borderColor = isCorrect ? 'var(--accent-green)' : 'var(--accent-red)';
      element.style.background = isCorrect ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)';

      const explEl = card.querySelector('.quiz-explanation');
      explEl.style.display = 'block';
      explEl.innerHTML = `<strong style="color:${{isCorrect ? '#34d399' : '#f87171'}};">${{isCorrect ? '✅ Correct' : '❌ Incorrect'}}:</strong> ${{explanation}}`;
    }}
  </script>
</body>
</html>
"""

def generate_standalone_diagram_html(spec):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{spec['title']} ({spec['id'].upper()})</title>
  <link rel="stylesheet" href="../assets/site.css">
  <link rel="stylesheet" href="../assets/diagram-engine.css">
  <style>
    body {{
      padding: 24px 16px;
      background: var(--bg);
      font-family: var(--font-mono);
    }}
    .standalone-nav {{
      max-width: 960px;
      margin: 0 auto 16px auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
  </style>
</head>
<body>
  <div class="standalone-nav">
    <a href="../pages/topic-{spec['topic_no']}.html" class="btn-de">← Back to Topic Page</a>
    <span style="font-size:12px; font-weight:600; color:var(--accent);">{spec['roadmap_id']} • {spec['title']}</span>
    <button class="btn-de" onclick="location.reload()">↺ Reload</button>
  </div>
  
  <div style="max-width:960px; margin:0 auto;">
    <div id="standalone-diagram"></div>
  </div>

  <script src="../assets/diagram-engine.js"></script>
  <script>
    const spec = {json.dumps(spec, indent=2)};
    document.addEventListener('DOMContentLoaded', () => {{
      new DiagramEngine('standalone-diagram', spec);
    }});
  </script>
</body>
</html>
"""

def build_topic_page(topic_data):
    topic_no = topic_data['topic_no']
    roadmap_id = topic_data['roadmap_id']
    title = topic_data['title']
    page_type = topic_data['page_type']
    phase = topic_data['phase']
    lead = topic_data['lead']
    
    # Save JSON files
    d1 = topic_data['d1']
    d2 = topic_data['d2']
    d3 = topic_data['d3']
    analogy = topic_data['analogy']

    with open(os.path.join(DIAGRAMS_DIR, f"topic-{topic_no}-d1.json"), 'w') as f:
        json.dump(d1, f, indent=2)
    with open(os.path.join(DIAGRAMS_DIR, f"topic-{topic_no}-d2.json"), 'w') as f:
        json.dump(d2, f, indent=2)
    with open(os.path.join(DIAGRAMS_DIR, f"topic-{topic_no}-d3.json"), 'w') as f:
        json.dump(d3, f, indent=2)
    with open(os.path.join(ANALOGY_DIR, f"topic-{topic_no}.json"), 'w') as f:
        json.dump(analogy, f, indent=2)

    # Generate standalone diagram HTML files
    with open(os.path.join(DIAGRAMS_DIR, f"topic-{topic_no}-d1.html"), 'w') as f:
        f.write(generate_standalone_diagram_html(d1))
    with open(os.path.join(DIAGRAMS_DIR, f"topic-{topic_no}-d2.html"), 'w') as f:
        f.write(generate_standalone_diagram_html(d2))
    with open(os.path.join(DIAGRAMS_DIR, f"topic-{topic_no}-d3.html"), 'w') as f:
        f.write(generate_standalone_diagram_html(d3))

    # Body parts
    part1_html = topic_data['part1_html']
    part2_ladder_html = topic_data['part2_ladder_html']
    part3_narrative_html = topic_data['part3_narrative_html']
    part4_demo_html = topic_data['part4_demo_html']
    quiz_html = topic_data['quiz_html']
    reading_html = topic_data['reading_html']

    demo_or_practice_label = "Hands-On Demo" if page_type == "service" else "Practice Exercise"

    body_html = f"""
    <!-- Part 1: Real-World Explanation -->
    <section class="topic-section" id="real-world">
      <h2 class="section-title"><span class="section-number">1</span> Real-World Explanation</h2>
      {part1_html}
    </section>

    <!-- Part 2: Technical Discussion & Diagrams -->
    <section class="topic-section" id="technical">
      <h2 class="section-title"><span class="section-number">2</span> Technical Discussion & Architecture Diagrams</h2>
      
      <h3>2A — The Depth Ladder: Conceptual Architecture & Defense-in-Depth</h3>
      
      <div class="callout" style="margin-bottom: 24px;">
        <div class="callout-title">The Mental Model: Progressive Systems Depth vs. Flat Command Memorization</div>
        <p>
          In cloud engineering, technical mastery is not an arbitrary bag of CLI flags—it is a <strong>progressive hierarchy of abstraction and defense-in-depth</strong>, directly analogous to the <strong>OSI 7-Layer model in computer networking</strong>.
        </p>
        <p>
          In networking, an architect cannot reason about Layer 7 HTTP/2 reverse proxies or BGP multi-cloud routing without first mastering Layer 2 frame switching, Layer 3 IP addressing, and Layer 4 TCP stateful handshakes. Similarly, cloud platforms are not magical black boxes; they are <strong>distributed orchestrations of operating system, network, and IAM primitives</strong>. If an engineer only knows how to click buttons in the Google Cloud Console, they are helpless when a service encounters cascading failures, quota starvation, or security boundary breaches.
        </p>
        <p>
          The Depth Ladder structures systems understanding into four deliberate, interlocking tiers of engineering capability:
        </p>
        <ol style="margin-bottom: 0;">
          <li><strong>Layer 1 — Foundation (The Substrate Primitive):</strong> The kernel physics, file descriptors, network sockets, and IAM identities that govern all compute.</li>
          <li><strong>Layer 2 — Practitioner (Operational Supervision & Observability):</strong> Declarative service lifecycles, resource quotas, daemon supervision, and structured telemetry.</li>
          <li><strong>Layer 3 — Architect (Cloud-Native Boundaries & Zero-Trust Access):</strong> Enterprise network perimeters, managed service mesh, cross-zone redundancy, and least-privilege security fabrics.</li>
          <li><strong>Layer 4 — Staff / Principal (Failure Horizons, Saturation Limits & Blast Radius):</strong> Chaos dynamics, saturation math, failover cascade prevention, and graceful self-healing.</li>
        </ol>
      </div>

      {part2_ladder_html}

      <div id="diagrams" style="margin-top: 40px;">
        <h3>2B — Interactive Architecture Diagrams</h3>
        
        <div class="callout" style="margin-bottom: 24px;">
          <div class="callout-title">Diagram Architectural Scope & Taxonomy: Why These Three Diagrams Exist</div>
          <p>
            Architecture diagrams in this curriculum are not decorative illustrations; they are <strong>precision engineering models</strong> designed to answer three distinct, non-overlapping architectural questions for every topic:
          </p>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; margin-top: 12px;">
            <div style="background: var(--bg); border: 1px solid var(--border); border-radius: 4px; padding: 12px;">
              <strong style="color: var(--accent); font-size: 13px;">D1 — Scope & Boundary Map (Structural Lens)</strong>
              <p style="font-size: 12px; margin: 6px 0 0 0; color: var(--text-dim);">
                <strong>Question Answered:</strong> <em>Where do execution and security boundaries lie?</em><br>
                Maps components into their isolation perimeters (Client Edge vs Project VPC vs Managed Services). Establishes trust boundaries, network ingress choke-points, and data-plane vs control-plane separation.
              </p>
            </div>
            <div style="background: var(--bg); border: 1px solid var(--border); border-radius: 4px; padding: 12px;">
              <strong style="color: var(--accent); font-size: 13px;">D2 — Request & Control Flow (Runtime Ingress Lens)</strong>
              <p style="font-size: 12px; margin: 6px 0 0 0; color: var(--text-dim);">
                <strong>Question Answered:</strong> <em>How does production traffic traverse the architecture securely?</em><br>
                Traces an end-to-end operational journey—from ingress initiation and IAM perimeter validation across Andromeda SDN to backend state persistence and audit logging.
              </p>
            </div>
            <div style="background: var(--bg); border: 1px solid var(--border); border-radius: 4px; padding: 12px;">
              <strong style="color: var(--accent); font-size: 13px;">D3 — Failure Injection & Resilience (Chaos Lens)</strong>
              <p style="font-size: 12px; margin: 6px 0 0 0; color: var(--text-dim);">
                <strong>Question Answered:</strong> <em>How does the system degrade, alert, and auto-heal under catastrophic failure?</em><br>
                Models the exact mechanics of component saturation, network timeouts, and health check evictions under stress, revealing observability signals and automated failover pathways.
              </p>
            </div>
          </div>
        </div>

        <!-- Diagram 1 Context Card & Container -->
        <div class="diagram-context-card" style="margin-top: 24px; margin-bottom: 12px; padding: 14px; background: rgba(33, 150, 243, 0.05); border-left: 3px solid var(--accent); border-radius: 0 4px 4px 0;">
          <h4 style="margin: 0 0 6px 0; color: var(--text); font-size: 14px;">Diagram 1: {d1.get('title', 'Scope & Boundary Map')}</h4>
          <p style="margin: 0; font-size: 12.5px; color: var(--text-dim); line-height: 1.5;">
            <strong>Architectural Intent:</strong> {d1.get('purpose', 'Visualizes isolation perimeters, trust boundaries, and execution planes.')}
          </p>
        </div>
        <div id="diagram-d1"></div>

        <!-- Diagram 2 Context Card & Container -->
        <div class="diagram-context-card" style="margin-top: 36px; margin-bottom: 12px; padding: 14px; background: rgba(33, 150, 243, 0.05); border-left: 3px solid var(--accent); border-radius: 0 4px 4px 0;">
          <h4 style="margin: 0 0 6px 0; color: var(--text); font-size: 14px;">Diagram 2: {d2.get('title', 'Request & Control Flow')}</h4>
          <p style="margin: 0; font-size: 12.5px; color: var(--text-dim); line-height: 1.5;">
            <strong>Architectural Intent:</strong> {d2.get('purpose', 'Traces end-to-end request lifecycle and control-plane dispatch.')}
          </p>
        </div>
        <div id="diagram-d2"></div>

        <!-- Diagram 3 Context Card & Container -->
        <div class="diagram-context-card" style="margin-top: 36px; margin-bottom: 12px; padding: 14px; background: rgba(33, 150, 243, 0.05); border-left: 3px solid var(--accent); border-radius: 0 4px 4px 0;">
          <h4 style="margin: 0 0 6px 0; color: var(--text); font-size: 14px;">Diagram 3: {d3.get('title', 'Failure Injection & Resilience')}</h4>
          <p style="margin: 0; font-size: 12.5px; color: var(--text-dim); line-height: 1.5;">
            <strong>Architectural Intent:</strong> {d3.get('purpose', 'Demonstrates fault injection, saturation limits, and automated healing.')}
          </p>
        </div>
        <div id="diagram-d3"></div>
      </div>
    </section>

    <!-- Part 3: Explained by Analogy -->
    <section class="topic-section" id="analogy">
      <h2 class="section-title"><span class="section-number">3</span> Explained by Analogy: Cloud City</h2>
      {part3_narrative_html}

      <div class="analogy-stepper" style="margin-top: 20px;">
        <button class="stepper-btn active" onclick="showAnalogyBeat(1)">1. The City Problem</button>
        <button class="stepper-btn" onclick="showAnalogyBeat(2)">2. The City Solution</button>
        <button class="stepper-btn" onclick="showAnalogyBeat(3)">3. City Under Stress</button>
        <button class="stepper-btn" onclick="showAnalogyBeat(4)">4. Where Metaphor Breaks</button>
      </div>

      <div class="analogy-box" id="analogy-display"></div>
    </section>

    <!-- Part 4: Demo or Practice Exercise -->
    <section class="topic-section" id="demo-or-practice">
      <h2 class="section-title"><span class="section-number">4</span> {demo_or_practice_label}</h2>
      {part4_demo_html}
    </section>

    <!-- Footer 1: Knowledge Check -->
    <section class="topic-section" id="quiz">
      <h2 class="section-title">Check Your Understanding</h2>
      {quiz_html}
    </section>

    <!-- Footer 2: Further Reading -->
    <section class="topic-section" id="reading">
      <h2 class="section-title">Further Reading & Authoritative Google Cloud Docs</h2>
      {reading_html}
    </section>
"""

    full_page = (
        HTML_HEAD.format(
            topic_no=topic_no,
            roadmap_id=roadmap_id,
            title=title,
            phase=phase,
            page_type=page_type,
            lead=lead,
            demo_or_practice_label=demo_or_practice_label
        )
        + body_html
        + HTML_FOOTER.format(
            spec_d1_json=json.dumps(d1, indent=2),
            spec_d2_json=json.dumps(d2, indent=2),
            spec_d3_json=json.dumps(d3, indent=2),
            analogy_json=json.dumps(analogy, indent=2)
        )
    )

    page_path = os.path.join(PAGES_DIR, f"topic-{topic_no}.html")
    with open(page_path, 'w') as f:
        f.write(full_page)
    print(f"Built topic page: {page_path}")
    
    try:
        from inject_topic_navigation import enrich_topic_page
        enrich_topic_page(int(topic_no) - 1)
    except Exception as e:
        pass

print("build_website core template ready.")
