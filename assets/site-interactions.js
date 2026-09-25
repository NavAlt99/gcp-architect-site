(function () {
  "use strict";

  var themeStorageKey = "gcp-architect-theme";
  function readTheme() {
    try { return localStorage.getItem(themeStorageKey) || "dark"; } catch (_) { return "dark"; }
  }
  function setTheme(theme) {
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem(themeStorageKey, theme); } catch (_) { /* file:// or privacy mode */ }
    var button = document.querySelector("[data-theme-toggle]");
    if (button) {
      var light = theme === "light";
      button.textContent = light ? "☾ Dark mode" : "☀ Light mode";
      button.setAttribute("aria-label", light ? "Switch to dark mode" : "Switch to light mode");
      button.setAttribute("aria-pressed", String(light));
    }
  }
  document.documentElement.dataset.theme = readTheme();

  function initThemeToggle() {
    if (document.querySelector("[data-theme-toggle]")) return;
    var button = document.createElement("button");
    button.type = "button";
    button.className = "theme-toggle";
    button.setAttribute("data-theme-toggle", "true");
    button.addEventListener("click", function () {
      setTheme(document.documentElement.dataset.theme === "light" ? "dark" : "light");
    });
    var nav = document.querySelector(".nav-container");
    if (nav) {
      nav.appendChild(button);
    } else {
      var host = document.createElement("div");
      host.className = "theme-fallback-host";
      host.appendChild(button);
      document.body.insertBefore(host, document.body.firstChild);
    }
    setTheme(document.documentElement.dataset.theme || "dark");
  }

  function escapeText(value) {
    return String(value).replace(/[&<>"']/g, function (ch) {
      return {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[ch];
    });
  }

  function renderAnalogyScene(beat) {
    var host = document.getElementById("analogy-scene");
    if (!host) return;
    var title = window.analogyData && window.analogyData.title ? window.analogyData.title : "Topic";
    host.innerHTML =
      '<svg class="city-scene-svg" viewBox="0 0 760 260" role="img" aria-labelledby="city-scene-title city-scene-desc">' +
      '<title id="city-scene-title">Cloud City analogy for ' + escapeText(title) + '</title>' +
      '<desc id="city-scene-desc">A code-drawn city scene with a campus, road, gate, inspector, and control room mapped to GCP boundaries.</desc>' +
      '<rect class="city-ground" x="8" y="8" width="744" height="244" rx="16"></rect>' +
      '<path class="city-road" d="M48 192 H712"></path>' +
      '<g class="city-element" tabindex="0" role="button" aria-label="Brightloaf campus maps to the topic resource">' +
      '<rect x="70" y="74" width="150" height="86" rx="10"></rect><text x="145" y="108" text-anchor="middle">Brightloaf campus</text><text x="145" y="132" text-anchor="middle">topic resource</text></g>' +
      '<g class="city-element" tabindex="0" role="button" aria-label="Inspector maps to IAM and policy">' +
      '<rect x="292" y="54" width="150" height="86" rx="10"></rect><text x="367" y="88" text-anchor="middle">Inspector permits</text><text x="367" y="112" text-anchor="middle">IAM / policy</text></g>' +
      '<g class="city-element" tabindex="0" role="button" aria-label="Dispatcher maps to networking and dependencies">' +
      '<rect x="514" y="74" width="150" height="86" rx="10"></rect><text x="589" y="108" text-anchor="middle">Dispatcher roads</text><text x="589" y="132" text-anchor="middle">network / APIs</text></g>' +
      '<circle class="city-beacon" cx="380" cy="192" r="10"></circle><text class="city-step" x="380" y="230" text-anchor="middle">Beat ' + escapeText(beat && beat.step ? beat.step : 1) + ': ' + escapeText(beat && beat.name ? beat.name : "The city story") + '</text></svg>';
    host.querySelectorAll(".city-element").forEach(function (element) {
      element.addEventListener("click", function () { host.classList.toggle("mapping-selected"); });
      element.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          host.classList.toggle("mapping-selected");
        }
      });
    });
  }

  window.showAnalogyBeat = function (step) {
    var data = window.analogyData;
    if (!data || !data.beats) return;
    var beat = data.beats.find(function (item) { return item.step === step; });
    if (!beat) return;
    var display = document.getElementById("analogy-display");
    if (display) {
      display.innerHTML = "<h4>Beat " + escapeText(beat.step) + ": " + escapeText(beat.name) + "</h4><p>" + escapeText(beat.story) + "</p><p><strong>City elements:</strong> " + escapeText((beat.analogy_elements || []).join(" · ")) + "</p>";
    }
    renderAnalogyScene(beat);
    document.querySelectorAll(".stepper-btn").forEach(function (button, index) {
      button.classList.toggle("active", index + 1 === step);
    });
  };

  window.initTopicIndex = function () {
    var cards = Array.prototype.slice.call(document.querySelectorAll(".topic-card"));
    var search = document.getElementById("topic-search");
    var phase = document.getElementById("phase-filter");
    var type = document.getElementById("type-filter");
    var tier = document.getElementById("tier-filter");
    function apply() {
      var query = search ? search.value.toLowerCase() : "";
      cards.forEach(function (card) {
        var visible = card.textContent.toLowerCase().indexOf(query) >= 0 &&
          (!phase || !phase.value || card.dataset.phase === phase.value) &&
          (!type || !type.value || card.dataset.pageType === type.value) &&
          (!tier || !tier.value || card.dataset.demoTier === tier.value);
        card.hidden = !visible;
      });
    }
    [search, phase, type, tier].filter(Boolean).forEach(function (control) { control.addEventListener("input", apply); control.addEventListener("change", apply); });
    document.querySelectorAll("[data-complete-topic]").forEach(function (box) {
      var key = "gcp-architect-complete-" + box.dataset.completeTopic;
      box.checked = localStorage.getItem(key) === "true";
      box.addEventListener("change", function () { localStorage.setItem(key, String(box.checked)); });
    });
    document.querySelectorAll("[data-roadmap-check]").forEach(function (box) {
      var key = "gcp-roadmap-check-" + box.dataset.roadmapCheck;
      box.checked = localStorage.getItem(key) === "true";
      box.addEventListener("change", function () { localStorage.setItem(key, String(box.checked)); });
    });
    apply();
  };

  document.addEventListener("DOMContentLoaded", function () {
    initThemeToggle();
    if (document.getElementById("topic-cards-container")) window.initTopicIndex();
    if (window.analogyData && document.getElementById("analogy-display")) window.showAnalogyBeat(1);
    document.querySelectorAll(".page-meta").forEach(function (meta) {
      var page = document.querySelector("[data-topic-no]");
      if (meta.querySelector("[data-page-complete]")) return;
      var match = document.body.innerHTML.match(/Topic (\d{3})/);
      if (!match) return;
      var no = match[1], key = "gcp-architect-complete-" + no;
      var label = document.createElement("label");
      label.className = "completion-control page-completion";
      label.innerHTML = '<input type="checkbox" data-page-complete> Mark complete';
      var checkbox = label.querySelector("input");
      checkbox.checked = localStorage.getItem(key) === "true";
      checkbox.addEventListener("change", function () { localStorage.setItem(key, String(checkbox.checked)); });
      meta.appendChild(label);
    });
  });
}());
