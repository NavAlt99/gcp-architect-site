import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_json(rel_path):
    with open(os.path.join(BASE_DIR, rel_path), 'r') as f:
        return json.load(f)

def generate_standalone_diagram(topic_id, d_num):
    spec_path = f"diagrams/{topic_id}-d{d_num}.json"
    spec = load_json(spec_path)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{spec['title']} ({spec['id'].upper()})</title>
  <link rel="stylesheet" href="../assets/site.css">
  <link rel="stylesheet" href="../assets/diagram-engine.css">
  <style>
    body {{
      padding: 1.5rem;
      background: var(--bg-body);
    }}
    .standalone-nav {{
      margin-bottom: 1rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
  </style>
</head>
<body>
  <div class="standalone-nav">
    <a href="../pages/{topic_id}.html" class="btn-de">← Back to Topic Page</a>
    <span style="font-weight:600; color:var(--text-muted);">{spec['roadmap_id']} • {spec['title']}</span>
    <button class="btn-de" onclick="location.reload()">↺ Reload</button>
  </div>
  
  <div id="standalone-diagram"></div>

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
    out_path = os.path.join(BASE_DIR, f"diagrams/{topic_id}-d{d_num}.html")
    with open(out_path, 'w') as f:
        f.write(html_content)
    print(f"Generated standalone diagram: {out_path}")

def update_topic_page(topic_id):
    d1 = load_json(f"diagrams/{topic_id}-d1.json")
    d2 = load_json(f"diagrams/{topic_id}-d2.json")
    d3 = load_json(f"diagrams/{topic_id}-d3.json")
    analogy = load_json(f"analogy/{topic_id}.json")
    
    page_path = os.path.join(BASE_DIR, f"pages/{topic_id}.html")
    with open(page_path, 'r') as f:
        content = f.read()

    # Create inline script with zero fetch calls
    new_script_section = f"""  <!-- Embedded Data & Scripts (Zero Fetch / 100% Offline & File:// Compatible) -->
  <script id="spec-d1-data" type="application/json">
{json.dumps(d1, indent=2)}
  </script>
  <script id="spec-d2-data" type="application/json">
{json.dumps(d2, indent=2)}
  </script>
  <script id="spec-d3-data" type="application/json">
{json.dumps(d3, indent=2)}
  </script>
  <script id="analogy-data" type="application/json">
{json.dumps(analogy, indent=2)}
  </script>

  <script src="../assets/diagram-engine.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      // Parse embedded JSON synchronously (bypasses browser file:// CORS restrictions)
      const specD1 = JSON.parse(document.getElementById('spec-d1-data').textContent);
      const specD2 = JSON.parse(document.getElementById('spec-d2-data').textContent);
      const specD3 = JSON.parse(document.getElementById('spec-d3-data').textContent);
      window.analogyData = JSON.parse(document.getElementById('analogy-data').textContent);

      // Initialize all diagrams immediately
      new DiagramEngine('diagram-d1', specD1);
      new DiagramEngine('diagram-d2', specD2);
      new DiagramEngine('diagram-d3', specD3);

      // Initialize analogy beat
      showAnalogyBeat(1);
    }});

    function showAnalogyBeat(stepNum) {{
      if (!window.analogyData) return;
      const beat = window.analogyData.beats.find(b => b.step === stepNum);
      if (!beat) return;

      const container = document.getElementById('analogy-display');
      container.innerHTML = `
        <h4 style="margin-top:0;">Beat ${{beat.step}}: ${{beat.name}}</h4>
        <p style="font-size:0.95rem; line-height:1.6;">${{beat.story}}</p>
        <div style="font-size:0.85rem; color:var(--text-muted);">
          <strong>Analogy Visual Elements:</strong> ${{beat.analogy_elements.join(' • ')}}
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
        btn.textContent = '🙈 Hide Worked Solution & Rubric';
      }} else {{
        block.style.display = 'none';
        btn.textContent = '👁 Show Worked Solution & Rubric';
      }}
    }}

    function checkQuiz(element, isCorrect, explanation) {{
      const card = element.closest('.quiz-card');
      const options = card.querySelectorAll('.quiz-option');
      options.forEach(opt => {{
        opt.style.borderColor = 'var(--border-color)';
        opt.style.background = 'var(--bg-card)';
      }});

      element.style.borderColor = isCorrect ? 'var(--color-success)' : 'var(--color-danger)';
      element.style.background = isCorrect ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)';

      const explEl = card.querySelector('.quiz-explanation');
      explEl.style.display = 'block';
      explEl.innerHTML = `<strong>${{isCorrect ? '✅ Correct' : '❌ Incorrect'}}:</strong> ${{explanation}}`;
    }}
  </script>
"""
    # Replace from <!-- Scripts --> to </body>
    idx = content.find("<!-- Scripts -->")
    if idx != -1:
        end_idx = content.find("</body>")
        updated_content = content[:idx] + new_script_section + content[end_idx:]
        with open(page_path, 'w') as f:
            f.write(updated_content)
        print(f"Updated {page_path} with embedded synchronous data.")

if __name__ == '__main__':
    generate_standalone_diagram('topic-001', 1)
    generate_standalone_diagram('topic-001', 2)
    generate_standalone_diagram('topic-001', 3)
    update_topic_page('topic-001')
