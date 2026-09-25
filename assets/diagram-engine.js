/**
 * diagram-engine.js - Kubernetes Apartment / ByteMonk Style Lock Diagram Engine
 * v4.0 — High-Fidelity Architecture Traversal Engine:
 *         - Dark Monospace ByteMonk Aesthetic (zero emoji, pure terminal style)
 *         - Single-Screen Side-by-Side Traversal (controls, viewport, narration & telemetry)
 *         - Auto-Sized Dynamic Nodes (eliminates text overflow & label clipping)
 *         - Dynamic Edge Endpoint Routing based on true node bounding boxes
 *         - Deep Scope Rendering (Organization, Folder, Project, Region, Zone, VPC, Subnet)
 *         - Sub-second Reactive Step Navigation & Scenario Analysis
 */
class DiagramEngine {
  constructor(containerId, spec) {
    this.container = document.getElementById(containerId);
    if (!this.container) return;
    this.spec = spec;
    this.currentStep = -1;
    this.isPlaying = false;
    this.playTimer = null;
    this.speeds = [2200, 3500, 1400];
    this.speedLabels = ['[SPEED: 2.2s]', '[SPEED: 3.5s]', '[SPEED: 1.4s]'];
    this.speedIndex = 0;
    this.playSpeed = this.speeds[this.speedIndex];
    this.activeScenario = null;
    this.selectedNode = null;
    this.zoom = 1;
    this.tableVisible = false;
    this.compareMode = false;
    this.layersVisible = true;
    this._packetAnim = null;
    this._edgePathCache = {};
    this.init();
  }

  init() {
    this.container.classList.add('diagram-container');
    this.computeNodeDimensions();
    this.renderSkeleton();
    this.renderSVG();
    this.updateStep(0);
    this.bindEvents();
  }

  /* ── Compute dynamic node dimensions to fit labels comfortably ─ */
  computeNodeDimensions() {
    if (!this.spec.nodes) return;
    this.spec.nodes.forEach(n => {
      const label = n.label || n.id || '';
      const sub = n.product || n.plane || '';
      const maxLen = Math.max(label.length, sub.length);
      // Monospace font at 11.5px averages ~7.2px per character.
      // Add generous horizontal padding (36px total) and enforce minimum 145px width.
      n._w = Math.max(145, Math.ceil(maxLen * 7.6 + 36));
      n._h = 54;
    });
  }

  /* ── Skeleton (Side-by-side single-screen workspace) ────────── */
  renderSkeleton() {
    const purposeText = this.spec.purpose ||
      `Visualizes ${this.spec.title.toLowerCase()} across security boundaries, isolated network tiers, and Google Andromeda SDN.`;
    const rationaleText = this.spec.routing_rationale ||
      `Traffic navigates from public edge termination through identity verification into private Andromeda VPC backends.`;
    const totalSteps = (this.spec.steps && this.spec.steps.length) ? this.spec.steps.length : 1;

    this.container.innerHTML = `
      <div class="diagram-header">
        <div class="diagram-title-wrap">
          <h4>${this.spec.title} <span class="diagram-badge">${this.spec.id.toUpperCase()}</span></h4>
        </div>
      </div>
      <div class="diagram-context-banner">
        <div class="context-pill">
          <span class="context-tag">ARCHITECTURAL PURPOSE</span>
          <span class="context-text">${purposeText}</span>
        </div>
        <div class="context-pill rationale-pill">
          <span class="context-tag">TRAVERSAL RATIONALE</span>
          <span class="context-text">${rationaleText}</span>
        </div>
      </div>
      <div class="diagram-workspace">
        <!-- Scenarios stay above the diagram for fast failure-mode switching. -->
        <div class="scenario-bar diagram-scenarios" id="${this.spec.id}-scenario-bar">
          <span class="scenario-title">SCENARIOS:</span>
          <button class="scenario-btn active" data-scenario="normal">[NORMAL]</button>
          ${(this.spec.scenarios || []).map(sc => `
            <button class="scenario-btn" data-scenario="${sc.id}">[! ${sc.label}]</button>
          `).join('')}
        </div>

        <!-- Full-width SVG drawing viewport -->
        <div class="diagram-viewport">
          <svg class="diagram-svg" id="${this.spec.id}-svg"
               viewBox="0 0 960 440"
               role="img" aria-label="${this.spec.title || 'Architecture Diagram'}"
               xmlns="http://www.w3.org/2000/svg">
            <defs>
              <filter id="${this.spec.id}-glow-packet" x="-50%" y="-50%" width="200%" height="200%">
                <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#ff5722"/>
                <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#ec4899"/>
              </filter>
              <filter id="${this.spec.id}-glow-label" x="-4" y="-4" width="108%" height="130%">
                <feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#f43f5e" flood-opacity="0.7"/>
              </filter>
              <marker id="${this.spec.id}-arrow-data" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#4a213a" />
              </marker>
              <marker id="${this.spec.id}-arrow-active" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#f43f5e" />
              </marker>
              <marker id="${this.spec.id}-arrow-failed" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#ef4444" />
              </marker>
            </defs>
            <g id="${this.spec.id}-groups"></g>
            <g id="${this.spec.id}-edges"></g>
            <g id="${this.spec.id}-nodes"></g>
            <g id="${this.spec.id}-labels"></g>
            <circle id="${this.spec.id}-packet" class="packet" cx="0" cy="0" r="7"/>
          </svg>
        </div>

        <!-- Scenarios, navigation, and dynamic display stay directly below the diagram. -->
        <div class="diagram-sidebar">
          <div class="diagram-toolbar diagram-navigation" aria-label="Diagram navigation controls">
            <button class="btn-de" id="${this.spec.id}-btn-speed" title="Adjust pacing">${this.speedLabels[this.speedIndex]}</button>
            <button class="btn-de" id="${this.spec.id}-btn-prev" title="Step back (left arrow)">[PREV]</button>
            <button class="btn-de" id="${this.spec.id}-btn-play" title="Play or pause (space)">[PLAY]</button>
            <button class="btn-de" id="${this.spec.id}-btn-next" title="Step forward (right arrow)">[NEXT]</button>
            <button class="btn-de" id="${this.spec.id}-btn-reset" title="Reset view">[RESET]</button>
            <button class="btn-de" id="${this.spec.id}-btn-zoom-in" title="Zoom in">[ZOOM+]</button>
            <button class="btn-de" id="${this.spec.id}-btn-zoom-out" title="Zoom out">[ZOOM-]</button>
            <button class="btn-de" id="${this.spec.id}-btn-focus" title="Focus selected node">[FOCUS]</button>
            <button class="btn-de" id="${this.spec.id}-btn-compare" title="Compare normal and degraded state">[COMPARE]</button>
            <button class="btn-de" id="${this.spec.id}-btn-layers" title="Toggle scope layers">[LAYERS]</button>
            <button class="btn-de" id="${this.spec.id}-btn-table" title="Show accessible table view">[TABLE]</button>
            <button class="btn-de" id="${this.spec.id}-btn-export" title="Export as SVG">[EXPORT SVG]</button>
          </div>
          <div class="diagram-display-grid">
          <div class="panel-card narration-panel">
            <h5><span>HOP <span id="${this.spec.id}-step-num">1</span> OF ${totalSteps}</span> <span>LIVE TRAVERSAL</span></h5>
            <div class="narration-box" id="${this.spec.id}-narration">Select [PLAY] or [NEXT] to trace the request packet.</div>
          </div>
          <div class="panel-card telemetry-panel">
            <h5><span>TELEMETRY &amp; CLI</span> <span>SIGNALS</span></h5>
            <div id="${this.spec.id}-checks">
              <div class="check-item"><span>Select a step to inspect monitoring telemetry.</span></div>
            </div>
          </div>
          </div>
        </div>
      </div>
      <div class="diagram-table-view" id="${this.spec.id}-table-view" hidden></div>
    `;
  }

  /* ── SVG rendering ────────────────────────────────────────── */
  renderSVG() {
    const groupsG  = document.getElementById(`${this.spec.id}-groups`);
    const nodesG   = document.getElementById(`${this.spec.id}-nodes`);
    const edgesG   = document.getElementById(`${this.spec.id}-edges`);
    const labelsG  = document.getElementById(`${this.spec.id}-labels`);

    /* ── Groups (hierarchical scope containers) ── */
    if (this.spec.groups) {
      this.spec.groups.forEach(g => {
        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        const gType = (g.type || 'project').toLowerCase();
        const gScope = (g.scope || 'regional').toLowerCase();
        rect.setAttribute('class', `svg-group-box group-${gType} group-scope-${gScope}`);
        rect.setAttribute('x', g.x || 20);
        rect.setAttribute('y', g.y || 20);
        rect.setAttribute('width', g.width || 200);
        rect.setAttribute('height', g.height || 200);
        rect.setAttribute('rx', '12');
        groupsG.appendChild(rect);

        // Group title
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('class', 'svg-group-label');
        text.setAttribute('x', (g.x || 20) + 14);
        text.setAttribute('y', (g.y || 20) + 20);
        text.textContent = g.label;
        groupsG.appendChild(text);

        // Group scope pill badge
        const scopeBadge = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        scopeBadge.setAttribute('class', 'svg-group-scope-pill');
        scopeBadge.setAttribute('x', (g.x || 20) + 14);
        scopeBadge.setAttribute('y', (g.y || 20) + 33);
        scopeBadge.textContent = `[SCOPE: ${(g.scope || g.type || 'REGIONAL').toUpperCase()}]`;
        groupsG.appendChild(scopeBadge);
      });
    }

    /* ── Edges (paths + animated dashes) ── */
    if (this.spec.edges) {
      this.spec.edges.forEach(e => {
        const fromNode = this.spec.nodes.find(n => n.id === e.from);
        const toNode   = this.spec.nodes.find(n => n.id === e.to);
        if (!fromNode || !toNode) return;

        const pathD = this.calculateEdgePath(fromNode, toNode);

        // Base connector line
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', pathD);
        path.setAttribute('id', `${this.spec.id}-edge-${e.id}`);
        path.setAttribute('class', e.plane === 'control' ? 'svg-edge-control' : 'svg-edge-data');
        path.setAttribute('marker-end', `url(#${this.spec.id}-arrow-data)`);
        edgesG.appendChild(path);

        // Animated flow dash line overlay
        const dashPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        dashPath.setAttribute('d', pathD);
        dashPath.setAttribute('id', `${this.spec.id}-dash-${e.id}`);
        dashPath.setAttribute('class', 'connector-dash');
        edgesG.appendChild(dashPath);

        // Cache path element for packet animation
        this._edgePathCache[e.id] = path;

        /* ── Edge label (rendered in top-layer labelsG) ── */
        if (e.label) {
          const mid = this._getPathMidpoint(path, fromNode, toNode);
          const labelG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
          labelG.setAttribute('id', `${this.spec.id}-elabel-${e.id}`);
          labelG.setAttribute('class', 'svg-edge-label-group');

          const charLen = e.label.length;
          const estW = Math.max(50, charLen * 6.5 + 14);
          const estH = 17;

          // Background pill
          const bg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
          bg.setAttribute('class', 'svg-edge-label-bg');
          bg.setAttribute('x', mid.x - estW / 2);
          bg.setAttribute('y', mid.y - 12);
          bg.setAttribute('width', estW);
          bg.setAttribute('height', estH);
          bg.setAttribute('rx', '5');
          bg.setAttribute('ry', '5');

          // Text
          const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
          text.setAttribute('class', 'svg-edge-label');
          text.setAttribute('x', mid.x);
          text.setAttribute('y', mid.y);
          text.textContent = e.label;

          labelG.appendChild(bg);
          labelG.appendChild(text);
          labelsG.appendChild(labelG);

          requestAnimationFrame(() => {
            try {
              const bbox = text.getBBox();
              if (bbox && bbox.width > 0) {
                const padX = 6;
                const padY = 3;
                bg.setAttribute('x', bbox.x - padX);
                bg.setAttribute('y', bbox.y - padY);
                bg.setAttribute('width', bbox.width + padX * 2);
                bg.setAttribute('height', bbox.height + padY * 2);
              }
            } catch (_) { /* fallback */ }
          });
        }
      });
    }

    /* ── Nodes (dynamically sized and centered) ── */
    if (this.spec.nodes) {
      this.spec.nodes.forEach(n => {
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('class', 'svg-node');
        g.setAttribute('id', `${this.spec.id}-node-${n.id}`);
        g.setAttribute('tabindex', '0');
        g.setAttribute('role', 'button');
        g.setAttribute('aria-label', `${n.label || n.id} (${n.product || n.plane || 'resource'})`);
        const w = n._w || 145;
        const h = n._h || 54;
        g.setAttribute('transform', `translate(${n.x - w / 2}, ${n.y - h / 2})`);

        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('class', 'svg-node-rect');
        rect.setAttribute('width', w);
        rect.setAttribute('height', h);
        rect.setAttribute('rx', '10');
        g.appendChild(rect);

        const title = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        title.setAttribute('class', 'svg-node-title');
        title.setAttribute('x', w / 2);
        title.setAttribute('y', 23);
        title.textContent = n.label;
        g.appendChild(title);

        const sub = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        sub.setAttribute('class', 'svg-node-sub');
        sub.setAttribute('x', w / 2);
        sub.setAttribute('y', 40);
        sub.textContent = n.product || n.plane || '';
        g.appendChild(sub);

        g.addEventListener('click', () => this.inspectNode(n));
        g.addEventListener('keydown', (event) => {
          if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            this.inspectNode(n);
          }
        });
        nodesG.appendChild(g);
      });
    }
  }

  /* ── Bézier curve midpoint calculation ── */
  _getPathMidpoint(pathEl, fromNode, toNode) {
    try {
      const len = pathEl.getTotalLength();
      if (len > 0) {
        const pt = pathEl.getPointAtLength(len / 2);
        return { x: pt.x, y: pt.y - 10 };
      }
    } catch (_) { /* fallback below */ }

    if (fromNode && toNode) {
      const mx = (fromNode.x + toNode.x) / 2;
      const my = (fromNode.y + toNode.y) / 2 - 12;
      return { x: mx, y: my };
    }
    return { x: 480, y: 200 };
  }

  /* ── Edge path calculation with dynamic bounding box clipping ── */
  calculateEdgePath(from, to) {
    const dx0 = to.x - from.x;
    const dy0 = to.y - from.y;
    const absDx = Math.abs(dx0);
    const absDy = Math.abs(dy0);

    const fromW2 = (from._w || 145) / 2;
    const fromH2 = (from._h || 54) / 2;
    const toW2   = (to._w || 145) / 2;
    const toH2   = (to._h || 54) / 2;

    // Predominantly vertical — exit from bottom/top
    if (absDy > absDx * 1.2) {
      const startX = from.x;
      const startY = from.y + (dy0 > 0 ? fromH2 : -fromH2);
      const endX   = to.x;
      const endY   = to.y + (dy0 > 0 ? -toH2 : toH2);
      const cdy = (endY - startY) * 0.45;
      return `M ${startX} ${startY} C ${startX} ${startY + cdy}, ${endX} ${endY - cdy}, ${endX} ${endY}`;
    }

    // Predominantly horizontal — exit from right/left
    const startX = from.x + (dx0 > 0 ? fromW2 : -fromW2);
    const startY = from.y;
    const endX   = to.x + (dx0 > 0 ? -toW2 : toW2);
    const endY   = to.y;

    // Slight upward arch when on horizontal line for label clearance
    if (absDy < 25) {
      const cdx = (endX - startX) * 0.35;
      const arch = -22;
      return `M ${startX} ${startY} C ${startX + cdx} ${startY + arch}, ${endX - cdx} ${endY + arch}, ${endX} ${endY}`;
    }

    const cdx = (endX - startX) * 0.4;
    return `M ${startX} ${startY} C ${startX + cdx} ${startY}, ${endX - cdx} ${endY}, ${endX} ${endY}`;
  }

  /* ── Step management ─────────────────────────────────────── */
  updateStep(index) {
    if (!this.spec.steps || !this.spec.steps.length) return;
    this.currentStep = Math.max(0, Math.min(index, this.spec.steps.length - 1));
    const step = this.spec.steps[this.currentStep];
    const stepNum = this.currentStep + 1;
    const totalSteps = this.spec.steps.length;

    const stepNumEl = document.getElementById(`${this.spec.id}-step-num`);
    if (stepNumEl) stepNumEl.textContent = stepNum;

    // Render Structured Step Narration (Monospace, ByteMonk Style Lock)
    const narrationEl = document.getElementById(`${this.spec.id}-narration`);
    const actionText = step.action || step.narration;
    const whyPathText = step.why_traversal || step.why ||
      'Enforces architectural security boundaries: external traffic terminates at public proxies and authenticates before traversing internal VPC software-defined networks.';
    const stepTitle = step.title || `Hop ${stepNum}: Component Transaction`;

    narrationEl.innerHTML = `
      <div class="step-narration-card">
        <div class="step-narration-header">
          <span class="step-badge-mini">HOP ${stepNum} OF ${totalSteps}</span>
          <span class="step-title-text">${stepTitle}</span>
        </div>
        <div class="step-section">
          <strong style="color:var(--accent);">ACTION:</strong> ${actionText}
        </div>
        <div class="step-section">
          <strong style="color:var(--accent-cyan);">TRAVERSAL RATIONALE:</strong> ${whyPathText}
        </div>
        ${step.protocol || step.plane ? `
          <div class="step-meta">
            ${step.protocol ? `<span class="meta-pill">PROTOCOL: ${step.protocol}</span>` : ''}
            <span class="meta-pill">PLANE: ${step.plane || 'Data Plane'}</span>
            ${step.edges ? `<span class="meta-pill">EDGES: ${step.edges.join(', ')}</span>` : ''}
          </div>
        ` : ''}
      </div>
    `;

    /* Reset all edges, dashes, labels, nodes */
    if (this.spec.edges) {
      this.spec.edges.forEach(e => {
        const el   = document.getElementById(`${this.spec.id}-edge-${e.id}`);
        const dash = document.getElementById(`${this.spec.id}-dash-${e.id}`);
        const lbl  = document.getElementById(`${this.spec.id}-elabel-${e.id}`);
        if (el) {
          el.classList.remove('svg-edge-active', 'svg-edge-failed');
          el.setAttribute('marker-end', `url(#${this.spec.id}-arrow-data)`);
        }
        if (dash) dash.classList.remove('on');
        if (lbl)  lbl.classList.remove('active');
      });
    }

    if (this.spec.nodes) {
      this.spec.nodes.forEach(n => {
        const el = document.getElementById(`${this.spec.id}-node-${n.id}`);
        if (el) el.classList.remove('active');
      });
    }

    /* Cancel in-flight packet animation */
    if (this._packetAnim) { cancelAnimationFrame(this._packetAnim); this._packetAnim = null; }

    const packet = document.getElementById(`${this.spec.id}-packet`);

    if (step.edges && step.edges.length > 0) {
      step.edges.forEach(edgeId => {
        const el   = document.getElementById(`${this.spec.id}-edge-${edgeId}`);
        const dash = document.getElementById(`${this.spec.id}-dash-${edgeId}`);
        const lbl  = document.getElementById(`${this.spec.id}-elabel-${edgeId}`);
        if (el) {
          el.classList.add('svg-edge-active');
          el.setAttribute('marker-end', `url(#${this.spec.id}-arrow-active)`);
        }
        if (dash) dash.classList.add('on');
        if (lbl)  lbl.classList.add('active');

        const ed = (this.spec.edges || []).find(e => e.id === edgeId);
        if (ed) {
          const fn = document.getElementById(`${this.spec.id}-node-${ed.from}`);
          const tn = document.getElementById(`${this.spec.id}-node-${ed.to}`);
          if (fn) fn.classList.add('active');
          if (tn) tn.classList.add('active');
        }
      });

      if (packet) {
        packet.classList.add('on');
        this._animatePacketSequence(packet, step.edges);
      }
    } else if (packet && this.spec.nodes && this.spec.nodes.length > 0) {
      packet.classList.add('on');
      packet.setAttribute('cx', this.spec.nodes[0].x);
      packet.setAttribute('cy', this.spec.nodes[0].y);
    }

    /* Telemetry Checks */
    const checksEl = document.getElementById(`${this.spec.id}-checks`);
    if (checksEl) {
      if (step.check) {
        checksEl.innerHTML = '';
        if (step.check.metrics) {
          checksEl.innerHTML += `<div class="check-item"><span>METRIC: <code>${step.check.metrics}</code></span><button class="copy-mini-btn" onclick="navigator.clipboard.writeText('${step.check.metrics}')">[COPY]</button></div>`;
        }
        if (step.check.logs) {
          checksEl.innerHTML += `<div class="check-item"><span>LOG FILTER: <code>${step.check.logs}</code></span><button class="copy-mini-btn" onclick="navigator.clipboard.writeText('${step.check.logs.replace(/'/g, "\\'")}')">[COPY]</button></div>`;
        }
        if (step.check.commands) {
          checksEl.innerHTML += `<div class="check-item"><span>COMMAND: <code>${step.check.commands}</code></span><button class="copy-mini-btn" onclick="navigator.clipboard.writeText('${step.check.commands.replace(/'/g, "\\'")}')">[COPY]</button></div>`;
        }
      } else {
        checksEl.innerHTML = `<div class="check-item"><span>Standard state. No error or threshold breach detected.</span></div>`;
      }
    }
  }

  /* ── Sequential packet animation across edges in a step ──── */
  _animatePacketSequence(packet, edgeIds) {
    if (!edgeIds || edgeIds.length === 0) return;

    let edgeIndex = 0;
    const runNextEdge = () => {
      if (edgeIndex >= edgeIds.length) return;
      const edgeId = edgeIds[edgeIndex++];
      this._animatePacketAlongSingleEdge(packet, edgeId, () => {
        runNextEdge();
      });
    };

    runNextEdge();
  }

  /* ── Single edge packet animation via requestAnimationFrame ─ */
  _animatePacketAlongSingleEdge(packet, edgeId, onComplete) {
    const pathEl = this._edgePathCache[edgeId];
    if (!pathEl) {
      if (onComplete) onComplete();
      return;
    }

    let totalLen = 0;
    try { totalLen = pathEl.getTotalLength(); } catch (_) {
      if (onComplete) onComplete();
      return;
    }

    if (totalLen <= 0) {
      if (onComplete) onComplete();
      return;
    }

    const duration = Math.min(800, Math.max(400, totalLen * 2.2));
    const start = performance.now();

    const tick = (now) => {
      const elapsed = now - start;
      const t = Math.min(elapsed / duration, 1);
      const eased = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;

      try {
        const pt = pathEl.getPointAtLength(eased * totalLen);
        packet.setAttribute('cx', pt.x);
        packet.setAttribute('cy', pt.y);
      } catch (_) { /* fallback */ }

      if (t < 1) {
        this._packetAnim = requestAnimationFrame(tick);
      } else {
        if (onComplete) onComplete();
      }
    };

    this._packetAnim = requestAnimationFrame(tick);
  }

  /* ── Node inspector ── */
  inspectNode(node) {
    this.selectedNode = node;
    const narrationEl = document.getElementById(`${this.spec.id}-narration`);
    narrationEl.innerHTML = `
      <div class="step-narration-card">
        <div class="step-narration-header">
          <span class="step-badge-mini" style="background:rgba(56,189,248,0.2); color:#38bdf8; border-color:#38bdf8;">COMPONENT INSPECTOR</span>
          <span class="step-title-text">${node.label} (${node.product || 'GCP Resource'})</span>
        </div>
        <div class="step-section">
          <strong style="color:var(--accent);">ROLE &amp; FUNCTION:</strong> ${node.detail || 'Standard GCP component in architecture topology.'}
        </div>
        <div class="step-meta">
          <span class="meta-pill">GROUP: ${node.group || 'Regional'}</span>
          <span class="meta-pill">SCOPE: ${node.scope || this.scopeForNode(node)}</span>
          <span class="meta-pill">PLANE: ${node.plane || 'Data'}</span>
          <span class="meta-pill">NODE ID: ${node.id}</span>
        </div>
      </div>
    `;
  }

  scopeForNode(node) {
    const group = (this.spec.groups || []).find(item => item.id === node.group || item.label === node.group);
    return node.scope || (group && (group.scope || group.type)) || 'resource';
  }

  setZoom(delta) {
    this.zoom = Math.max(0.65, Math.min(1.8, this.zoom + delta));
    const svg = document.getElementById(`${this.spec.id}-svg`);
    if (svg) {
      svg.style.transform = `scale(${this.zoom})`;
      svg.style.transformOrigin = 'center center';
    }
  }

  focusSelected() {
    const nodes = this.container.querySelectorAll('.svg-node');
    nodes.forEach(node => node.classList.toggle('focus-dim', Boolean(this.selectedNode) && node.id !== `${this.spec.id}-node-${this.selectedNode.id}`));
    if (this.selectedNode) this.container.classList.add('focus-mode');
  }

  toggleLayers() {
    this.layersVisible = !this.layersVisible;
    this.container.classList.toggle('layers-hidden', !this.layersVisible);
    const button = document.getElementById(`${this.spec.id}-btn-layers`);
    if (button) button.classList.toggle('active', !this.layersVisible);
  }

  toggleCompare() {
    this.compareMode = !this.compareMode;
    this.container.classList.toggle('compare-mode', this.compareMode);
    const button = document.getElementById(`${this.spec.id}-btn-compare`);
    if (button) button.classList.toggle('active', this.compareMode);
    const narration = document.getElementById(`${this.spec.id}-narration`);
    if (this.compareMode && narration) {
      narration.insertAdjacentHTML('afterbegin', '<div class="compare-banner">COMPARE: normal topology is shown with the selected degraded scenario.</div>');
    }
  }

  toggleTable() {
    this.tableVisible = !this.tableVisible;
    const table = document.getElementById(`${this.spec.id}-table-view`);
    if (!table) return;
    table.hidden = !this.tableVisible;
    const rows = (this.spec.nodes || []).map(node => `<tr><td>${node.label || node.id}</td><td>${node.product || ''}</td><td>${node.scope || this.scopeForNode(node)}</td><td>${node.plane || ''}</td><td>${node.detail || ''}</td></tr>`).join('');
    const edges = (this.spec.edges || []).map(edge => `<li><code>${edge.from}</code> → <code>${edge.to}</code> · ${edge.label || 'dependency'} · ${edge.plane || 'data'}</li>`).join('');
    table.innerHTML = `<h5>Accessible architecture table</h5><p>${this.spec.summary || this.spec.purpose || ''}</p><table><thead><tr><th>Node</th><th>Product</th><th>Scope</th><th>Plane</th><th>Detail</th></tr></thead><tbody>${rows}</tbody></table><h5>Edges</h5><ul>${edges || '<li>No edges declared.</li>'}</ul>`;
  }

  /* ── Scenario injection with rich architectural breakdown ── */
  setScenario(scenarioId) {
    this.activeScenario = scenarioId;
    const scenarioBtns = this.container.querySelectorAll('.scenario-btn');
    scenarioBtns.forEach(btn => {
      btn.classList.toggle('active', btn.dataset.scenario === scenarioId);
    });

    if (this.spec.nodes) {
      this.spec.nodes.forEach(n => {
        const el = document.getElementById(`${this.spec.id}-node-${n.id}`);
        if (el) el.classList.remove('failed');
      });
    }

    if (this.spec.edges) {
      this.spec.edges.forEach(e => {
        const el = document.getElementById(`${this.spec.id}-edge-${e.id}`);
        if (el) {
          el.classList.remove('svg-edge-failed');
          el.setAttribute('marker-end', `url(#${this.spec.id}-arrow-data)`);
        }
      });
    }

    if (scenarioId === 'normal') {
      this.updateStep(this.currentStep);
      return;
    }

    const sc = (this.spec.scenarios || []).find(s => s.id === scenarioId);
    if (!sc) return;

    if (sc.changes && sc.changes.failedNodes) {
      sc.changes.failedNodes.forEach(nid => {
        const el = document.getElementById(`${this.spec.id}-node-${nid}`);
        if (el) el.classList.add('failed');
      });
    }

    if (sc.changes && sc.changes.failedEdges) {
      sc.changes.failedEdges.forEach(eid => {
        const el = document.getElementById(`${this.spec.id}-edge-${eid}`);
        if (el) {
          el.classList.add('svg-edge-failed');
          el.setAttribute('marker-end', `url(#${this.spec.id}-arrow-failed)`);
        }
      });
    }

    const rootCause = sc.root_cause || sc.narration;
    const divertedPath = sc.diverted_path ||
      'Normal request path is interrupted at the failed node. Downstream components receive timeout errors or drop packets without acknowledgment, forcing client retries or failover redirection.';
    const blastRadius = sc.blast_radius ||
      'All user sessions dependent on this tier experience elevated latency, HTTP 5xx errors, or severed connections.';
    const recovery = sc.recovery ||
      'Deploy multi-region Anycast failover, cross-zone active-standby redundancy, automated health check eviction, and exponential backoff circuit breakers.';

    document.getElementById(`${this.spec.id}-narration`).innerHTML = `
      <div class="scenario-analysis-card">
        <div class="scenario-alert-header">
          <span class="scenario-alert-badge">[FAILURE MODE: ${sc.label.toUpperCase()}]</span>
        </div>
        <div class="scenario-section">
          <strong style="color:#ef4444;">ROOT CAUSE:</strong> ${rootCause}
        </div>
        <div class="scenario-section">
          <strong style="color:#f97316;">DIVERGENT PATH:</strong> ${divertedPath}
        </div>
        <div class="scenario-section">
          <strong style="color:#fbbf24;">BLAST RADIUS:</strong> ${blastRadius}
        </div>
        <div class="scenario-section">
          <strong style="color:#10b981;">DURABLE MITIGATION:</strong> ${recovery}
        </div>
      </div>
    `;

    if (sc.check) {
      const checksEl = document.getElementById(`${this.spec.id}-checks`);
      if (checksEl) {
        checksEl.innerHTML = `
          <div class="check-item" style="border-left-color: #ef4444;">
            <span>ERROR METRIC: <code>${sc.check.metric || 'error_count > 0'}</code></span>
          </div>
          <div class="check-item" style="border-left-color: #ef4444;">
            <span>DIAGNOSIS CLI: <code>${sc.check.command || 'gcloud logging read ...'}</code></span>
          </div>
        `;
      }
    }
  }

  /* ── Speed adjustment ── */
  cycleSpeed() {
    this.speedIndex = (this.speedIndex + 1) % this.speeds.length;
    this.playSpeed = this.speeds[this.speedIndex];
    const speedBtn = document.getElementById(`${this.spec.id}-btn-speed`);
    if (speedBtn) speedBtn.textContent = this.speedLabels[this.speedIndex];

    if (this.isPlaying) {
      clearInterval(this.playTimer);
      this.playTimer = setInterval(() => {
        if (this.currentStep >= (this.spec.steps.length - 1)) {
          this.isPlaying = false;
          const playBtn = document.getElementById(`${this.spec.id}-btn-play`);
          if (playBtn) {
            playBtn.textContent = '[REPLAY]';
            playBtn.classList.remove('active');
          }
          clearInterval(this.playTimer);
        } else {
          this.updateStep(this.currentStep + 1);
        }
      }, this.playSpeed);
    }
  }

  /* ── Play / Pause ── */
  togglePlay() {
    this.isPlaying = !this.isPlaying;
    const playBtn = document.getElementById(`${this.spec.id}-btn-play`);
    if (this.isPlaying) {
      playBtn.textContent = '[PAUSE]';
      playBtn.classList.add('active');

      if (this.currentStep >= (this.spec.steps.length - 1)) {
        this.updateStep(0);
      }

      this.playTimer = setInterval(() => {
        if (this.currentStep >= (this.spec.steps.length - 1)) {
          this.isPlaying = false;
          playBtn.textContent = '[REPLAY]';
          playBtn.classList.remove('active');
          clearInterval(this.playTimer);
        } else {
          this.updateStep(this.currentStep + 1);
        }
      }, this.playSpeed);
    } else {
      playBtn.textContent = '[PLAY]';
      playBtn.classList.remove('active');
      clearInterval(this.playTimer);
    }
  }

  /* ── Event binding ── */
  bindEvents() {
    const speedBtn  = document.getElementById(`${this.spec.id}-btn-speed`);
    const playBtn   = document.getElementById(`${this.spec.id}-btn-play`);
    const nextBtn   = document.getElementById(`${this.spec.id}-btn-next`);
    const prevBtn   = document.getElementById(`${this.spec.id}-btn-prev`);
    const resetBtn  = document.getElementById(`${this.spec.id}-btn-reset`);
    const zoomInBtn = document.getElementById(`${this.spec.id}-btn-zoom-in`);
    const zoomOutBtn = document.getElementById(`${this.spec.id}-btn-zoom-out`);
    const focusBtn = document.getElementById(`${this.spec.id}-btn-focus`);
    const compareBtn = document.getElementById(`${this.spec.id}-btn-compare`);
    const layersBtn = document.getElementById(`${this.spec.id}-btn-layers`);
    const tableBtn = document.getElementById(`${this.spec.id}-btn-table`);
    const exportBtn = document.getElementById(`${this.spec.id}-btn-export`);

    if (speedBtn) speedBtn.addEventListener('click', () => this.cycleSpeed());
    if (playBtn)  playBtn.addEventListener('click', () => this.togglePlay());
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        if (this.isPlaying) this.togglePlay();
        this.updateStep(this.currentStep + 1);
      });
    }
    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        if (this.isPlaying) this.togglePlay();
        this.updateStep(this.currentStep - 1);
      });
    }
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        if (this.isPlaying) this.togglePlay();
        this.setScenario('normal');
        this.updateStep(0);
        if (playBtn) {
          playBtn.textContent = '[PLAY]';
          playBtn.classList.remove('active');
        }
      });
    }
    if (zoomInBtn) zoomInBtn.addEventListener('click', () => this.setZoom(0.1));
    if (zoomOutBtn) zoomOutBtn.addEventListener('click', () => this.setZoom(-0.1));
    if (focusBtn) focusBtn.addEventListener('click', () => this.focusSelected());
    if (compareBtn) compareBtn.addEventListener('click', () => this.toggleCompare());
    if (layersBtn) layersBtn.addEventListener('click', () => this.toggleLayers());
    if (tableBtn) tableBtn.addEventListener('click', () => this.toggleTable());

    const viewport = this.container.querySelector('.diagram-viewport');
    if (viewport) viewport.addEventListener('wheel', (event) => {
      if (event.ctrlKey || event.metaKey) {
        event.preventDefault();
        this.setZoom(event.deltaY < 0 ? 0.05 : -0.05);
      }
    }, { passive: false });

    if (exportBtn) {
      exportBtn.addEventListener('click', () => {
        const svg = document.getElementById(`${this.spec.id}-svg`);
        const serializer = new XMLSerializer();
        const source = serializer.serializeToString(svg);
        const url = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(source);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${this.spec.id}.svg`;
        link.click();
      });
    }

    const scenarioBar = document.getElementById(`${this.spec.id}-scenario-bar`);
    if (scenarioBar) {
      scenarioBar.addEventListener('click', (e) => {
        if (e.target.classList.contains('scenario-btn')) {
          this.setScenario(e.target.dataset.scenario);
        }
      });
    }

    // Scoped keyboard navigation for this diagram container
    this.container.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      if (e.key === 'ArrowRight') { e.preventDefault(); this.updateStep(this.currentStep + 1); }
      else if (e.key === 'ArrowLeft')  { e.preventDefault(); this.updateStep(this.currentStep - 1); }
      else if (e.key === ' ') { e.preventDefault(); this.togglePlay(); }
    });
    this.container.setAttribute('tabindex', '0');

    // Global keyboard navigation if only 1 diagram is on page
    if (document.querySelectorAll('.diagram-container').length <= 1) {
      window.addEventListener('keydown', (e) => {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
        if (e.key === 'ArrowRight') { this.updateStep(this.currentStep + 1); }
        else if (e.key === 'ArrowLeft')  { this.updateStep(this.currentStep - 1); }
        else if (e.key === ' ') { e.preventDefault(); this.togglePlay(); }
      });
    }
  }
}
window.DiagramEngine = DiagramEngine;
