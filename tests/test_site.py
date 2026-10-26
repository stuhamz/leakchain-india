"""Offline static site, export and evidentiary semantic integrity checks."""
import unittest,json,csv,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BUNDLE=json.loads((ROOT/'ui_data/browser_bundle_v0_9.json').read_text(encoding='utf8'))
JS=(ROOT/'assets/data.js').read_text(encoding='utf8')
EMBEDDED=json.loads(JS.split('window.LEAKCHAIN_DATA = ',1)[1].strip().removesuffix(';'))
CASES=BUNDLE['cases']

class TestSite(unittest.TestCase):
 def test_offline_bundle_matches_audited_json(self):
  self.assertEqual(EMBEDDED,BUNDLE)
 def test_50_incidents_and_counts(self):
  self.assertEqual(len(CASES),50)
  self.assertEqual(BUNDLE['counts']['total_events'],203)
  self.assertEqual(BUNDLE['counts']['total_claims'],220)
  self.assertEqual(BUNDLE['counts']['total_sources'],161)
 def test_every_case_has_unique_id(self):
  ids=[c['incident_id'] for c in CASES]
  self.assertEqual(len(ids),len(set(ids)))
  self.assertEqual(ids[0],'LCI-0001')
  self.assertEqual(ids[-1],'LCI-0050')
 def test_case_has_linked_claims_and_sources(self):
  total=0
  for c in CASES:
   src={s['id'] for s in c['sources']}
   self.assertGreaterEqual(len(src),3,c['incident_id'])
   self.assertEqual(len(src),c['source_count'])
   for e in c['events']:
    self.assertGreaterEqual(len(e['claims']),1,e['event_id'])
    for claim in e['claims']:
     total+=1
     self.assertIn(claim['source_id'],src,claim)
     self.assertTrue(claim['source_locator'] or claim['analytical_limit'],claim)
  self.assertEqual(total,220)
 def test_visual_graph_edges_only_display_order(self):
  for c in CASES:
   evs={e['event_id'] for e in c['events']}
   self.assertTrue(c['graph']['causality_not_inferred'])
   self.assertEqual(len(c['graph']['edges']),len(evs)-1)
   for edge in c['graph']['edges']:
    self.assertEqual(edge['relation'],'display_order_only')
    self.assertIn(edge['source'],evs)
    self.assertIn(edge['target'],evs)
 def test_dates_not_fabricated(self):
  actuals=[e for c in CASES for e in c['events']]
  self.assertEqual(sum(bool(e['date']) for e in actuals),23)
  self.assertEqual(sum(not e['date'] for e in actuals),180)
  for e in actuals:
   if e['date'] is None:self.assertEqual(e['date_precision'],'unknown')
 def test_independence_not_falsely_certified(self):
  self.assertFalse(BUNDLE['counts']['publication_ready'])
  self.assertEqual(BUNDLE['counts']['independent_incident_fact_certifications'],0)
  for c in CASES:
   self.assertFalse(c['lineages_independently_certified'])
   self.assertEqual(c['publication_gate'],'REVIEW_PENDING')
   for e in c['events']:
    for claim in e['claims']:self.assertFalse(claim['independent_fact_confirmation'])
 def test_protocol_assets_exist(self):
  for path in ['index.html','assets/app.js','assets/styles.css','assets/data.js','assets/favicon.svg','docs/coding_manual.md','docs/quality_cycle_v0_9.md','src/build_site_data.py']:
   self.assertTrue((ROOT/path).is_file(),path)
 def test_site_is_local_and_deployable(self):
  page=(ROOT/'index.html').read_text(encoding='utf8')
  self.assertIn('assets/data.js',page)
  self.assertIn('assets/app.js',page)
  self.assertIn('assets/styles.css',page)
  self.assertNotIn('https://cdn',page)
  self.assertIn('href="#/explore"',page)
 def test_public_source_schemes_only(self):
  for c in CASES:
   for s in c['sources']:
    self.assertRegex(s['url'],r'^https?://',s['id'])
 def test_core_tables_intact(self):
  for table,count in [('incidents',50),('events',203),('claims',220),('sources',161)]:
   with (ROOT/'data'/f'{table}.csv').open(encoding='utf8',newline='') as f:
    self.assertEqual(sum(1 for _ in csv.DictReader(f)),count)
