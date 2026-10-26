# LeakChain India v0.9.1 | Research interface release

Date: 26 October 2026

## Version scope

A production-style static site was added over the audited v0.9 dataset. **No source CSV research facts were changed.** All 50 cases, 203 events, 220 claims and 161 registered sources remain as recorded at the v0.9 quality checkpoint. `assets/data.js` reproduces the same case JSON from `src/export_ui_data.py` in a browser-usable, fully offline form.

## Implemented interface

- Overview and featured case cards, corpus statistics, case categories and circulation distribution.
- Full-text case directory, with category, state, circulation scope, event-type and exception filters, sort, pagination, and filtered CSV or full JSON exports.
- Addressable incident pages `#/case/LCI-0001`, interactive SVG event reconstructions, horizontal navigation and zoom, synchronized event-list selection, evidence source and claim cards, documentary reference links, and case-specific coding exceptions.
- Exploratory analytics for categories, states, event-stage totals, circulation statuses, source kinds and date completeness.
- Side-by-side comparison of up to four incidents.
- Research methodology page with primary evidence caveats and direct links to coding and audit files.
- Responsive desktop and mobile layout, keyboard-accessible event nodes, dark/light appearance preference, reduced-motion support and no remote runtime dependencies.

## Visual semantics

- A graph edge always means `display_order_only`, matching the audit export. It is not a causal or transmission edge.
- Event date unknown is displayed as `Underlying date unknown`, rather than guessed.
- A primary court record is described only to the extent its specific linked claim and adjudication scope support it.
- Publisher count is separate from origin-level independent corroboration; no certified incident-level independence is claimed.
- Threatened sharing, limited sharing, public posting and alleged commercial circulation remain distinct corpus classifications.
- No photos or private video content are embedded or fetched.

## Operational deployment

This release uses `index.html` in the repository root, plain CSS and JavaScript, and a generated static data assignment loaded before the interface script. The interface runs offline from `file://` and on GitHub Pages project paths. GitHub Pages source can be `main` branch, `/(root)` folder. No Node.js build required.

## Validation

Repository tests include core CSV and frozen-baseline audits plus new website integrity tests, source-to-claim linkage checks and embedded-bundle equivalence. An interactive Chromium smoke test exercised the overview, 50-case search, an incident graph and timeline, comparison, analytics, methodology, appearance and responsive mobile navigation. All known JavaScript runtime errors encountered during testing were corrected.

## Research status

The user may deploy the website when ready. Dataset independent-origin certification, second-coder agreement and some primary-document checks remain open, and these limitations are visible in the interface. Deployment should not be misrepresented as peer review or external certification.
