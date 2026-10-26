# LeakChain India v0.9.2 | Timeline-first interface update

Date: 26 October 2026

## Change

The case-detail **Interactive event sequence** diagram and its zoom/scroll controls were removed following interface review. The adjacent **Event timeline** already provided each stage, its sequence, its source-linked claims and its uncertainty annotations. Showing both introduced unnecessary duplication.

## Preserved functionality

- The single interactive timeline now appears immediately below the case overview.
- Clicking a timeline stage updates the selected event, claim citations and documentary evidence panel.
- Timeline selection retains keyboard focus and does not rebuild the entire event list.
- Search, category and evidence filters, research analytics, cross-case comparison, exported data, theme selection and responsive mobile pages are unchanged.
- All 50 cases, 203 events, 220 claims and 161 registered sources remain unchanged. Underlying research graph records and historical audit exports are preserved as data, but no longer displayed as duplicate charts on case pages.
- The overview illustration remains a decorative research identity element, not an interactive incident graph.

## Interpretation

Timeline order is a researcher-coded narrative order, **not necessarily dated chronology or proof of causality**. Underlying event dates that were unknown remain explicitly unknown.

## Deployment

Identical to v0.9.1: place the repository files at GitHub repository root and publish `main` branch from `/(root)` using GitHub Pages.
