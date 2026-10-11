# NASA PS EDA coursework delivery

Goal: upgrade the existing NASA project into a Chinese coursework report with an offline D3 interface and a Node.js service.

Scope: retain the supplied fixed CSV and existing six analytical views; add the population audit, field dictionary, descriptive statistics, log-scale radius distribution, discovery-method counts, physical-parameter rank correlation and chart-level interpretations. Never describe the fixed snapshot as live data.

Implementation: extend the existing Python analysis through `build_report.py`, generate the HTML and machine-readable report from computed statistics, and preserve the base EDA code. Keep the D3 dependency local. Add a dependency-free Node static service with an explicit public file allowlist.

Validation: reproduce counts from raw CSV, check exclusions and bin conservation, check bootstrap and sensitivity results, run Node HTTP integration tests, and inspect desktop/mobile browser rendering and filter/brush/export interactions.

Design: an observatory research notebook. Ink #101b2b, paper #16263b, foreground #e5eeff, cyan #83baff, amber #ffa98c, divider #31445f. Serif bilingual title; sans-serif Chinese body; monospace numbers and numbered sections. The signature is a sample-selection strip that visually separates literature rows, default solutions and unique confirmed planets.

Execution: proceed in this chat within the requested scope. No deployment or public publication is requested.
