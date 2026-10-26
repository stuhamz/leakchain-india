# LeakChain India | Checkpoint v0.5 (unpublished)

Date: 26 October 2026. All changes are local research work, not a GitHub push.

## Critical corrected accounting issue
The previous v0.4 report said 63 registered sources but the actual v0.4 ZIP contained **57 source rows**. Six intended reports (`SB-058` to `SB-063`) were only counted in the written report and were never persisted into the CSV. This checkpoint repairs those six records after independent article checks and derives every count directly from the data. The pre-repair 57-source archive is preserved.

## Current verified row counts
- **28 incidents**, 3 newly screened (LCI-0026 through LCI-0028)
- **82 registered sources**, of which 80 incident-linked and 2 contextual
- **107 events** and **107 claims**
- **19/28** incidents with at least three registered sources. 9 below the gate and **12** minimum further sources needed for currently accepted cases.
- **0** incident source-lineage groups fully verified as independently corroborating every key allegation. The three-source minimum is not the same as three independent lines of fact.

## Source quality
- Existing article backfill: 13 checked articles, including 6 previously omitted from the real CSV.
- New cases use diverse publishers, but share underlying police evidence in many assertions.
- Duplicative and syndicated accounts are flagged in `data/source_lineage_audit.csv`.
- Diu, Rajkot and other pre-existing incidents are not recounted by article, alleged video, or platform account.
- Source reports that identify people do not cause victim identifiers to be stored in incident/event/claim tables.

## Material correction
- LCI-0020, Aligarh: reporter describes a magistrate rejecting remand and ruling an arrest unlawful in one complaint. This is explicitly added as a reported court-process event and does not establish acquittal or disprove allegations. Original signed order still needed.
- LCI-0026 Assam: AI impersonation and alleged subscription monetisation are not authenticated recording leaks; police financial estimates remain attributed.
- LCI-0027 Delhi: synthetic harassment posts do not establish a hacked platform or leaked genuine intimate recording.
- LCI-0028 Bengaluru: blackmail threat is coded as **threat only**, with no established online posting.

## Remaining gaps
Under three sources: LCI-0005, LCI-0006, LCI-0008, LCI-0011, LCI-0016, LCI-0017, LCI-0019, LCI-0020, LCI-0022. Publication status stays HOLD for these. Stronger LC-04 personal/cloud compromise evidence remains a priority. No existing case is counted as independently verified solely because it has three URLs.
