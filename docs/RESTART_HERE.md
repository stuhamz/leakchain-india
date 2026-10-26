# Restart LeakChain India at v0.9.2, timeline-first interface

1. **Repository status:** Complete static research website implemented over v0.9 audited data, dated 26 October 2026. GitHub not pushed by the assistant. User can deploy from repository root with GitHub Pages.
2. **Corpus:** 50 episodes LCI-0001 through LCI-0050; 161 registered sources SB-001 through SB-161; 203 events EV-001 through EV-203; 220 linked claims CL-001 through CL-220.
3. **Primary data:** v0.9 CSV tables unchanged. Historical v0.8 baseline is frozen at `data/frozen_v0_8/`. New v0.9 records SB-158..SB-161 and CL-217..CL-220 remain attributed and limited in scope.
4. **Site:** Open root `index.html` directly, or serve locally. Overview, searchable case explorer, 50 case pages, interactive incident timelines and source evidence, analytics, comparison, and methodology are available. See `docs/interface_release_v0_9_2.md`.
5. **Source qualifications:** 50/50 cases have >=3 registered documents; independent source-lineage certification remains pending. `data/source_independence_v0_9.csv` and `data/claim_evidence_audit_v0_9.csv` retain origin and adjudication-scope assessments.
6. **Judicial nuance:** LCI-0023 has a trial-court conviction in the corpus record; LCI-0016 has court filing and interim-bail history only, not proof of the underlying allegation. Preserve proposition-level limits.
7. **Unresolved disputes:** Examples include LCI-0008 moving-to-Mumbai chronology, LCI-0019 original-versus-altered images/source parentage, LCI-0041 reported recording counts, and LCI-0048 complaint details. Do not silently reconcile.
8. **Key commands:** `python src/validate.py`, `python src/reconstruct.py`, `python src/build_site_data.py`, `python -m unittest discover -s tests -v`, `python src/verify_manifest.py`. Following a deliberate content change, regenerate the manifest last with `python src/build_manifest.py`.
9. **Next identifiers:** incident LCI-0051, source SB-162, event EV-204, claim CL-221. Never recycle identifiers.
10. **Publication scope:** The website is functionally ready for GitHub Pages. It makes no claim to peer review, independent corroboration, verified prevalence, or causal reconstruction. Private incident media and victim identifiers are not included.
