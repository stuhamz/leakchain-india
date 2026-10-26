# LeakChain India | Checkpoint v0.6 (unpublished)

Dated 26 October 2026. Input baseline v0.5 is frozen in `data/frozen_v0_5`. All counts below are computed from CSV records.

## Accounting

- 32 incident episodes (4 additions, LCI-0029 through LCI-0032)
- 97 registered sources (15 additions, SB-083 through SB-097)
- 125 events and 127 evidence claims
- 25/32 incidents with 3+ registered sources; 7 still under the minimum, requiring 10 new sources for full coverage
- 0 incidents certified to have independent primary-source lineages; publishing is HOLD.

## New cases and epistemic boundaries

- LCI-0029: Delhi job impersonation and AI edited-image extortion. Threat, payment and arrest alleged; no established public image dissemination.
- LCI-0030: Bhubaneswar relationship-linked image morphing and alleged posting; distinct from LCI-0016 April 6 case. Two local sources differ on surname spelling.
- LCI-0031: Karnataka fabricated video reportedly sent to mother and threatened online posting. This is limited forwarding and a threat, not confirmed public release.
- LCI-0032: Kendrapada June nurse case with alleged two-person circulation. Third paper omits alleged associate; no verified 2-person criminal operation.
- SB-083: Goa LCI-0017 Navhind Times local original e-paper page provides an additional publisher report, but police is the underlying source.
- SB-084: Aligarh LCI-0020 NDTV reporter corroborates investigation background, not guilt; reported larger target count should not be merged with number of recovered videos. Court-process correction from v0.5 stays intact.

## Design improvement

A dedicated `synthetic_generation` event type was added to codebook version 0.6. This ensures constructed media is not falsely described as genuine recorded intimate footage. In each case all acquisition, circulation, monetary and enforcement claims remain attributed. The existing 28 incidents were preserved, apart from explicit addition of source references to LCI-0017 and LCI-0020.

## Outstanding

The active list of under-three-source incidents: LCI-0005, LCI-0006, LCI-0008, LCI-0011, LCI-0016, LCI-0019, LCI-0022. Remote personal cloud compromise remains one admitted case. SC-045 suspected Gmail compromise stays deferred on its sole detailed FIR-based report; alleged account access is not a forensic conclusion. Aligarh original court order remains outstanding. No incident is classified as confirmed solely because three articles repeat the same police source. No GitHub push made.
