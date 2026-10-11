# Verification · 2026-10-01

- Original source: user-supplied NASA PS export, 40,188 rows × 92 columns, SHA-256 recorded in report.
- Rebuilt through build_report.py with deterministic host-cluster bootstrap (seed 20261001, 1000 repetitions).
- npm test passed: HTTP responses, local D3, downloads, HEAD, unsupported methods, invalid URLs and private-file rejection; independent statistics and artifact-link checks.
- Independent checks cover uniqueness of 6,298 confirmed default planets, per-field missingness/exclusion reconciliation, medians, full scatter populations, Mass-only mass-radius sample, histogram count conservation, method/year totals and symmetric correlations.
- Browser: all 9 views loaded, 12 SVGs including linked panels; no console warnings/errors.
- Interactions checked: Radial Velocity filter reduces period-radius sample to 28; brush selects a subset and updates summaries; clear restores 4,633; Microlensing radius filter reports no data.
- Responsive layout checked at 1440 × 1000 and 390 × 844, with no page-level horizontal overflow.
- SVG download is implemented with self-contained computed colors and a background. The in-app browser did not expose a downloadable file during the event check; downloaded-file verification remains unconfirmed. Use a standard browser for file export.

Statistical limits: observational selection, method-related missingness, host dependence, model-derived parameters, unpropagated measurement error, and an incomplete 2026 year are explicitly discussed. No claim of guaranteed grades is made.
