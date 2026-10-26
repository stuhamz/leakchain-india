# Source lineage and publication eligibility | v0.4

Publication target: at least 50 distinct cases, with a minimum of three relevant source records *per case*.

A source record is not equivalent to an independent witness or independently verified fact.
- `source_id`: every separately identified document
- `publisher`: outlet or primary institution
- `origin_note`: whether reporting draws on a police briefing, court judgment, wire story, original investigation or scholarly analysis
- `independence`: evaluate in `source_lineage_audit.csv` before release

Three publications repeating the same police briefing satisfy the *documentation count* but do not establish three independent evidentiary lineages. A report about an arrest does not prove the crime; a bail ruling does not prove guilt; a recovered camera does not prove footage exists; and threats are not dissemination.

The no-push rule remains in effect. Data files exclude images, victim identifiers, exploitative media, platform handles and active distribution channels. Research sources are public articles and a court judgment that itself redacts victim identity.

When two sources conflict, do not vote by majority; preserve disagreement in an exception register and do not infer which is correct without better evidence.
