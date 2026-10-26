# LeakChain India v0.9 | Evidence-quality cycle, 26 October 2026

**Status:** research-quality checkpoint complete for structural integrity and the three-registered-document requirement. **Unpublished.** The absence of independent second-coder and broad primary-document verification must not be interpreted as a completed academic peer review or independent source certification. A web interface has not yet been implemented.

## Verified package quantities

- **50** distinct, already accepted source-attributed incident episodes.
- **161** registered documents, including **159 case-linked** and 2 context-only.
- **203** narrative reconstruction events and **220** linked source-attributed claims.
- **50/50** incidents meet the protocol's minimum of three **registered documents**, not necessarily three independent evidentiary origins.
- **24** coding-exception or resolution records; the register contains both open disagreements and previously documented clarifications. The existence of a row alone does not mean a conflict is unresolved.
- **23** events contain a day-level date, and **180** have no confirmed day-level date in the coded dataset. Date absence remains explicit and never synthesized from article publication times.
- All source-independence assessments remain conservative. No case has been certified as independently corroborated across all material claims.

## Four backfilled documents

| Case | Source | Document / scope | Evidentiary caveat |
|---|---|---|---|
| LCI-0005 | SB-158 | The New Indian Express, Bengaluru, 4 September 2023 | Police-origin account: supports reported arrest and device seizure, not forensic confirmation or video dissemination |
| LCI-0008 | SB-159 | Times of India reproducing PTI wire, 16 June 2022 | Same Vanrai investigation; differing timeline of when individuals moved to Mumbai is explicitly logged |
| LCI-0016 | SB-160 | Orissa High Court official filing register, 3 May 2025, PDF page 3, entry 25 | Primary record establishes case filing, not alleged private-media disclosure; distinct from the existing interim-bail order |
| LCI-0019 | SB-161 | Marathi-language Loksatta, 20 April 2025 | Part of the Indian Express publishing group; separate document but overlapping police complaint; does not resolve image-authenticity dispute |

The four new source IDs are **SB-158 through SB-161**. The source-linked additions are **CL-217 through CL-220**; existing event and incident records were preserved except for append-only `claim_ids` and `source_ids` foreign-key lists. The complete earlier data tables are frozen under `data/frozen_v0_8/` for field-by-field comparison.

## Judicial nuance: do not flatten court records

LCI-0023 has a **trial court adjudication**. The published original judgment, *State of West Bengal v Animesh Boxi*, GR 1587/17, dated 7 March 2018, includes a conviction order and sentencing dispositions. It is correct to show a trial-court finding for the propositions expressed in the judgment. The case's appellate outcome has not been established in this corpus. Claims CL-084 and CL-085 are labelled `trial_court_adjudicated_finding`; CL-083 is a statement about the judgment's narrative recital and should not be equated automatically with all elements of a proved offence.

LCI-0016, by contrast, includes a High Court interim-bail decision and the filing register. The latter sources support **procedural facts only**. Claims CL-215 and CL-219 are `primary_procedural_only`. The substantive allegation retains its media/police evidentiary status.

This distinction is present in the machine-readable `claim_evidence_audit_v0_9.csv` and UI-ready detail export. Neither primary judgment nor bail record means *every* other source assertion is automatically independently corroborated.

## Source-independence review

The 161-item `source_independence_v0_9.csv` separately lists source publisher, probable source-origin grouping, evidence scope, review level and certification status. Classifications derived only from metadata are **provisional**, not representations of a completed 161-document full-text review. About 10 linked historical/new source records were directly checked during this cycle, including the new additions and original trial judgment; the remainder have conservative metadata-driven flags.

Avoid these errors:

- Three URLs are documentation, **not three independent observations**. For example, PTI reprints and direct police quotations often have one origin.
- Two different languages within a newspaper group do not automatically produce independent underlying evidence. Loksatta and Indian Express coverage of LCI-0019 share publisher ownership and concern the same complaint.
- An alleged money demand is not proven payment; a threat is not online publication; an installed camera is not proven retained footage; a filed case is not a conviction.
- Contradictory reports about counts, dates, original versus manipulated imagery, or the scope of sharing remain in `coding_exceptions.csv` until better records permit a documented resolution.

## Quality gates executed

1. CSV column schema, enum values, identifier uniqueness, all claim/event/source foreign keys, event order contiguity, domain whitelist, and publication cutoff validation.
2. **Field-by-field preservation of v0.8** sources, claims, content profiles and screening decisions, and append-only modification of existing incident/source and event/claim reference lists.
3. Source-count and evidentiary-independence safeguards, including no false public-ready flag.
4. Reconstruction regenerated for all 50 cases, with claim references and presentation-order-only graph arrows.
5. UI-ready JSON export validated against all 50 cases, source/claim links, reported date precision and narrative-only edge semantics.
6. Unit tests and package SHA-256 checksum verification (see checkpoint and `manifest.json`).

## Generated interface data, not an interface

- `ui_data/browser_bundle_v0_9.json`: case records, source cards, event cards, per-event claims, epistemic labels, unresolved coding issues and non-causal display graph links.
- `ui_data/search_index_v0_9.json`: compact records for text search, filters and faceting.
- `ui_data/chart_facets_v0_9.json`: counts for visualization, **not population prevalence**.
- `docs/ui_blueprint_v0_9.md`: future React interface acceptance and design plan.

Regenerate the JSON exports with `python src/export_ui_data.py` after any data update. The frontend must not infer transmission paths from DOT or JSON graph edges. Exact event dates must not be invented.

## Remaining research limitations and next action

The 50-case count and numerical documentation gate are achieved, but full independent source certification, second-coder reliability and broad primary-document review **remain open**. A dissertation or peer-reviewed paper must present these plainly and undertake appropriate independent validation before making stronger empirical claims.

Next work item is the read-only visual interface and its usability tests. **Do not push to GitHub or describe this as a final independently verified empirical corpus until expressly decided by the research owner.**
