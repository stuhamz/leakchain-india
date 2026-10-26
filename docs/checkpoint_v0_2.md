# LeakChain India | Checkpoint 2, systematic expansion v0.2

**Frozen on 26 October 2026. Not peer reviewed.**

## Scope and release decisions

- v0.1 preserved: LCI-0001 and LCI-0002 and their original source, event and claim records unchanged.
- Six distinct cases admitted, with IDs LCI-0003 through LCI-0008. No new record created for republished copies of the same story.
- New cases cover LC-02 relationship-based disclosures and LC-03 covert recording. LC-04 personal account compromise remains unfilled rather than forced.
- Only credible published source articles are indexed. Underlying images, private identifiers, distribution links, and forensic evidence have not been collected.
- **A4 is a categorisation of reported original possession/disclosure, not proof that the original capture was consensual.**

## New interpretive distinction

Added `content_profiles.csv` with one row per episode to separate videos from photos and distinguish public posting, commercial distribution, wider but unlocated circulation, and **threats without substantiated public posting**. Existing case counts are unchanged, original four CSV columns are unchanged, and the profiles for LCI-0001 and LCI-0002 are marked backfilled.

## Source caveats

The incident-level documentary basis for this batch is principally police accounts published by reporters, with limited direct documentary access and mostly undated underlying acts. The new graph event order is analytical display order, **not necessarily a verified chronology or proven transmission route**. Police announcements are not findings of guilt. The original evidence is not inspected.

## Candidate decisions

See `data/screening_log.csv` for included, deferred, out-of-scope and duplicate candidates. Defer does not mean false; it means the current dataset should not make stronger claims.

## Research integrity gate

1. A unique episode identifier and a separate source identifier for every distinct publication.
2. One or more event claims per event, each traceable to the registered source.
3. Date precision unknown unless underlying event date established.
4. No platform intrusion conclusion where source only describes image disclosure.
5. No conclusion of sales when sources only report threats, or monetisation intent.
6. Separate source lineage from independent corroboration.
7. Validator and unit tests before any release.

## Next checkpoint

Locate LC-04 account compromise cases with a verifiable primary technical or official basis; pursue judgments or primary official materials for at least two admitted cases. Independently recode a random subset before claims of intercoder agreement. Only then consider publishing comparative quantitative summaries.
