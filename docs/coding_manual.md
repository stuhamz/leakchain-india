# LeakChain India | Coding Manual v0.1

## 1. Research unit and inclusion

**Incident episode**: a materially connected, publicly documented occurrence of unauthorised recording, exposure, circulation, or commercial exploitation of private or intimate imagery in India. A single operation may involve multiple platforms, intermediaries, videos, arrests and articles yet remain one incident episode; separately documented underlying incidents may be split after an explicit decision.

Include if all apply:

1. India is materially involved.
2. Alleged or documented exposure, promotion, or distribution of private or intimate imagery is central.
3. A safe, identifiable credible publication provides substantive incident evidence.
4. At least two stages (such as recording environment, circulation, discovery, enforcement) can be reconstructed with source-specific claims.
5. Coding does not require hosting or accessing nonconsensual imagery or identifying victims.

Exclude from the incident corpus if primarily a generic privacy story without a concrete episode, purely consensual media dissemination, uncorroborated social-media allegations without a stable source, fictional incidents, or general regulation without case details. Maintain excluded leads in a private screening log rather than artificially inflating counts.

## 2. Incident categories (what type of incident)

| Code | Meaning |
|---|---|
| LC-01 | Institutional surveillance recording exposure, e.g. healthcare, cinema, hotel or workplace CCTV |
| LC-02 | Disclosure involving relationship-based access or possession of private recordings |
| LC-03 | Covert or otherwise unauthorised recording/capture |
| LC-04 | Personal device, account or cloud compromise linked to imagery exposure |
| LC-05 | Synthetic or manipulated intimate imagery circulated without consent; separate subcorpus |
| LC-06 | Institutional evidence of commercial child-abuse-material promotion and platform enforcement; **governance-only subcorpus** |

These are **content and situation categories**, not proof of technical method. In v0.1, both pilot cases are LC-01. Multiple labels may be warranted later, but there must be one primary category.

## 3. Acquisition mechanisms (how obtained)

| Code | Meaning |
|---|---|
| A0 | Unknown or unestablished |
| A1 | Unauthorised access to institutional recording infrastructure |
| A2 | Misuse of legitimate institutional access |
| A3 | Covert or otherwise unauthorised original recording |
| A4 | Nonconsensual disclosure by original recipient or possessor |
| A5 | Compromise of personal device/account/cloud storage |
| A6 | Synthetic creation or alteration, no original recording required |
| A7 | Other clearly documented mechanism |

**A0 is required** where the public record describes competing possibilities without establishing a mechanism. If investigators allege A1 but no court has assessed it, use A1 **with** `acquisition_status=official_allegation_reported`, not as a verified breach.

## 4. Source classification

- `investigative_journalism`: original reporting, potentially direct observations and interviews.
- `news_reporting`: reports of police or institutional statements, without original documents reproduced.
- `wire_reporting`: third-party reporting (e.g. a wire service) of an institutional action.
- `government_publication`: official policy or release.
- `platform_statement`: an organisation's own published claim.

Source role is `case` or `context`. Neither source tier nor publisher reputation makes every claim a fact; **claim status** controls interpretation.

## 5. Claim status

| Value | Interpretation |
|---|---|
| `official_allegation_reported` | Original news source attributes assertion to police, chargesheet, prosecution or institutional complaint. Not proved in court. |
| `journalist_original_observation` | Reporter describes directly documented observation; verify access and editorial scope. |
| `media_report_of_official_action` | Press reports an FIR, arrest, filing or Commission directive. The procedural action, not guilt, is the claim. |
| `media_report_of_institutional_response` | Management describes a response or mitigation; effectiveness unproven. |
| `publication_metadata` | Article publication time, not date of the crime. |
| `judicial_finding` | A competent court expressly establishes a proposition in a judgment available and reviewed directly. Not used in v0.1. |
| `unverified_report` | Reported but minimally substantiated; distinguish from established facts. |

A **claim** is an attributed assertion tied to exactly one source and one event. An event may have multiple claims; repetition of the same initial press account does not count as independent corroboration.

## 6. Events and chronology

Permitted event types: `recording`, `acquisition`, `distribution`, `detection`, `evidence_collection`, `publication`, `mitigation`, `enforcement`, `prosecution`, `oversight`.

`event_date` is blank when the underlying event date is not reliably established. `date_precision` is `unknown` for blanks and `day` for YYYY-MM-DD. `sequence_basis` is:

- `reported_event_date`: event date stated in a source;
- `report_publication_date`: source dated the reported response, but exact underlying event date is not assured;
- `analytical_stage`: interpretative position in a reconstruction, not a verified sequence.

Never silently substitute publication date for incident date. Graph arrows express display order only; they do not imply proven transfer, culpability, or causality.

## 7. Minimum claim audit

For each claim:

1. Link one event and one published source.
2. Record a stable section/paragraph locator or concise source-location description.
3. Use narrow paraphrase and assign a claim status.
4. State what the source **does not establish**.
5. Check that names, usernames, channel names, payment credentials and harmful media URLs never enter the public dataset.
6. For contested claims, record rival hypotheses explicitly with source support; otherwise mark `unknown`.

## 8. Reproducibility and sampling

The first two episodes are purposively selected to stress-test the codebook. The sample cannot support prevalence, network-size, rates, total sales, platform failure rates or causal claims about India. For expansion, freeze eligibility and definitions, track all exclusions and duplicate decisions, and invite an independent second reviewer to recode a subset. Do not claim intercoder reliability before it is measured.

## 9. Release governance

Only publish non-identifying evidence descriptions and safe links to reporting, academic work, and official releases. Do not include imagery or active routes for locating it. Corrections should be made through documented commits with the date and source of changes. Record allegations neutrally and do not treat criminal charges as convictions.


## 10. v0.2 scoped amendment, 26 October 2026

- `threat` event type distinguishes a reported threatened disclosure from documented distribution. A threatened release must never be counted as footage publicly posted.
- `data/content_profiles.csv` distinguishes content modality, reach of circulation and form of exploitation. The first two pilots were backfilled without changing their original event/claim rows.
- Photo-only incidents are included as **intimate imagery disclosure** when the publicly reported private-image context meets the documented incident rule. Video counts should be computed from `content_modality`, not assumed from the name LeakChain.
- Each report of a suspected arrest or forensic examination remains a report of official action, not validation of every police narrative claim.
- As of this batch there are no source-verified new A5 (personal account compromise) cases. A genuine breach classification needs direct records or reliable reporting of technical findings.

## v0.3 clarification (26 October 2026)

The primary category describes the episode, not proof of system hacking. Capture, threat, one-recipient transfer, limited sharing, online posting and commercial circulation must be distinguished. A camera reportedly found in a private space does not prove that footage was retained or distributed. Police/press accounts are linked at the claim level; no claim is promoted to a court finding without an actual court source. Negative forensic findings (for example, initial searches not finding recordings) are reasons to defer or expressly qualify candidate episodes.

A v0.3 event type `camera_placement` was introduced for cases where the documented allegation/observation supports placement or discovery of a camera, but not confirmed video capture. Do not recode `camera_placement` to `recording` based solely on a device being present.

## v0.6 amendment, 26 October 2026

`synthetic_generation` is a permitted event stage for creation/manipulation of content. Do not use `recording` when no genuine intimate recording is evidenced. For synthetic content keep source-image acquisition distinct from fabrication, recipient-only forwarding, public posting, and threatened wider posting. Use police-reported allegations when no original images or expert examination can be assessed.

## v0.7 amendment, 26 October 2026

An additional category `LC-07` was introduced for impersonation-induced intimate content solicitation where an existing interpersonal relationship is not established (for example, fake female personas eliciting images). This prevents forcing fraudulent grooming into `LC-02` relationship-based disclosure. `LC-04 / A5` includes alleged copying of private device files during authorised repair, which is a misuse-of-access allegation, not proof of a remote hack. For extortion amounts, keep image-related extortion separate from other financial fraud and avoid treating image-senders as confirmed paying victims.

New case sources remain reference counts, not independently authenticated fact lineages. An unresolved inconsistency in reported complaint date or accused count is documented, not silently reconciled.

## v0.8 evidence handling

- A primary court order documents procedural disposition only. Interim bail never confirms the truth of a reported underlying intimate-imagery allegation.
- Article counts describing recovered recordings refer to artifacts, not necessarily individuals or separate incidents. Conflicting counts are logged as exceptions, not reconciled by averaging.
- Reported sale or alleged distribution of hotel recordings is source-reported and remains separate from verified transactions or observed channels.
- Sharing privately with a spouse is limited disclosure. Threats to publish are coded as `threat_only` unless publication is separately reported.
- Impersonation without a proven pre-existing romantic relationship remains LC-07. Conflicting authentic and synthetic imagery must not be collapsed into a real nude-video claim.
- New articles from a third newspaper do not automatically constitute independent evidentiary lineages.
