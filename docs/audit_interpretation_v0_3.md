# LeakChain India v0.3 | Quality and interpretation review

Cutoff: 26 October 2026. This study is a purposive pilot, not a random or representative national sample.

- Incident episodes: **22**
- New this version: **14** (LCI-0009 to LCI-0022)
- Source records: **35** (2 context records)
- Coded events and source-linked claims: **81 each**
- GitHub: **not pushed**

## Distribution evidence is not uniform

- **4** not_established: No reliable evidence of onward distribution.
- **3** reported_limited_sharing: Reported sharing to one or limited recipients.
- **2** reported_public_or_commercial: Reported commercial/public circulation.
- **7** reported_public_posting: Reported online posting.
- **1** reported_wider_circulation_unspecified: Reported wider sharing without reliable audience boundaries.
- **5** threat_only: Threatened release, no public dissemination established.

These labels describe what published sources say. In particular, `reported_public_posting` is a police/publication report, not independent platform verification. Recovered devices or apparent camera placement alone do not prove a publicly available leak.

## Why several well-known candidates were not admitted

- Gudlavalleru 2024: later forensic/police reporting found no hidden camera or illicit footage; excluded.
- CMR College January 2025: initial police search reportedly found no relevant clips; later reporting conflicted. Deferred pending an authoritative forensic resolution.
- Ameenpur March 2025: admitted as documented concealed-camera discovery; the presence of footage is unresolved, so the event type is `camera_placement`.
- Hosur November 2025: camera placement reported; captured video not established.
- Gorakhpur September 2026: allegations of circulation are not treated as proven distribution.

## Limits before public release

1. No trial judgments or source video files have been evaluated for these 14 additions.
2. Many claims trace to the same police briefing even where multiple newspapers cover them; this is not independent corroboration.
3. The dataset includes exposure and threat cases as well as circulation cases; filtering on `circulation_scope` is mandatory for studies of distribution.
4. Case reconstruction uses publication-level locators and broad article sections; finer paragraph-level indexing should be introduced during the next audit.
5. Second-reader independent coding and protocol preregistration have not been completed.
6. The source URLs point to ordinary publisher sites; they do not include active exploitation services or media.

## Technical audit gates

- Original v0.2 rows compared against the copied starting tables at every build checkpoint.
- Source domains restricted to an explicitly reviewed allowlist.
- Referential integrity of source, incident, event and claim IDs checked.
- Exact one-row-per-incident profiles required.
- Unknown acquisition distinguished from technical compromise.
- Threat-only cases forbidden from carrying a distribution event in the new 0.3 tests.
- New `camera_placement` stage differentiates device discovery from evidence of recording.
- Full Python unit test suite run after release edits.
