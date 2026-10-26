# Audit report | LeakChain v0.2

Date: 26 October 2026. This is an internal, first-pass audit, not independent academic validation.

## Inventory

- **total_incidents:** 8
- **new_incidents:** 6
- **total_events:** 36
- **total_claims:** 36
- **total_sources:** 16
- **case_source_records:** 14
- **context_source_records:** 2

## Controlled case decisions

Six new incident episodes admitted. One syndicated duplicate collapsed; three candidates deferred and two excluded. Screening ledger stores a reason for every decision.

## Checks conducted

- original rows unchanged
- unique IDs/URLs
- foreign-key integrity
- one profile per episode
- no future source dates
- reported claims linked to same-episode published source
- threat differentiated from distribution
- no unsupported A5 account compromise
- safe source URLs only

## Deliberately unresolved

- No independent second researcher has coded the cases
- Primary police and judicial exhibits not reviewed for newly admitted incidents
- Event sequence for new cases is analytical, not independently verified chronology
- Research sample is purposive and not representative
- Syndicated copies are not independent sources

## Method note

One source-specific claim is used for every new event. This is **traceability** but not independently validated truth; a second-reader reliability study has not occurred. Original v0.1 rows were compared directly against the archived v0.1 ZIP and found semantically identical across all four original tables.

## Carry-forward issue from v0.1

The original case source `SB-006` is registered and linked at incident level but is not referenced directly by an event claim. It remains as contextual support for the Kerala acquisition-mechanism uncertainty. This was inherited from v0.1; the new seven case source records all have claim-level use. A later review should decide whether SB-006 merits its own precise claim or should be reclassified as contextual to avoid ambiguous source coverage.
