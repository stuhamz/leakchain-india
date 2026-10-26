"""Quality cycle v0.9: numerical eligibility, old-record preservation, lineage caution and frontend export."""
import csv, json, unittest
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rd(name, folder='data'):
 with (ROOT/folder/f'{name}.csv').open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
class Version09Quality(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.sources=rd('sources');cls.incidents=rd('incidents');cls.events=rd('events');cls.claims=rd('claims')
  cls.source_count=Counter(s['incident_id'] for s in cls.sources if s['source_role']=='case')
 def test_numbers_and_all_50_have_three_docs(self):
  self.assertEqual(tuple(map(len,(self.incidents,self.sources,self.events,self.claims))),(50,161,203,220))
  self.assertEqual(len(rd('source_independence_v0_9')),161)
  self.assertEqual(len(rd('claim_evidence_audit_v0_9')),220)
  for inc in self.incidents:self.assertGreaterEqual(self.source_count[inc['incident_id']],3)
 def test_every_v08_source_and_claim_preserved(self):
  for n in ['sources','claims','content_profiles','screening_log']:
   old=rd(n,'data/frozen_v0_8');new=rd(n)
   self.assertEqual(new[:len(old)],old,n)
 def test_v08_incidents_and_events_only_add_links(self):
  for n,column in [('incidents','source_ids'),('events','claim_ids')]:
   old=rd(n,'data/frozen_v0_8'); now=rd(n)
   self.assertEqual(len(now),len(old))
   for a,b in zip(old,now):
    self.assertEqual(set(a),set(b))
    for k in a:
     if k==column:
      self.assertEqual(b[k].split(';')[:len(a[k].split(';'))],a[k].split(';'))
     else:self.assertEqual(a[k],b[k],(n,k,a.get('incident_id')))
 def test_provenance_not_overcertified(self):
  meta=rd('source_independence_v0_9'); audited=rd('claim_evidence_audit_v0_9')
  self.assertEqual(len(set(x['source_id'] for x in meta)),len(self.sources))
  self.assertTrue(all(x['independent_incident_fact_certified']=='False' for x in meta))
  self.assertTrue(all(x['independent_fact_confirmation']=='False' for x in audited))
  self.assertTrue(all(x['original_exhibit_reviewed']=='False' for x in audited))
  self.assertTrue(all(x['independent_lineages_verified']=='False' for x in rd('publication_gate')))
  self.assertFalse(any(x['publication_gate']=='PUBLISH' for x in rd('publication_gate')))
  self.assertIn('SAME_PUBLISHING_GROUP_AND_COMPLAINT',[x['independence_status'] for x in meta])
  self.assertIn('PRIMARY_ADJUDICATED_RECORD',[x['independence_status'] for x in meta])
  self.assertEqual({x['claim_id'] for x in audited if x['adjudication_scope']=='offence_and_conviction_at_trial'},{'CL-084','CL-085'})
 def test_four_backfills_match_cases(self):
  expectation={'SB-158':'LCI-0005','SB-159':'LCI-0008','SB-160':'LCI-0016','SB-161':'LCI-0019'}
  ss={s['source_id']:s for s in self.sources}
  for sid,iid in expectation.items():self.assertEqual(ss[sid]['incident_id'],iid)
  ca={c['claim_id']:c for c in self.claims}
  for i,s in enumerate(expectation,start=217):self.assertEqual(ca[f'CL-{i}']['source_id'],s)
 def test_official_filing_only_proves_procedure(self):
  c=next(x for x in self.claims if x['claim_id']=='CL-219')
  self.assertEqual(c['claim_status'],'judicial_finding');self.assertIn('filing',c['claim_summary'].lower())
  self.assertIn('only',c['analytical_limit'].lower())
 def test_new_ui_exports_are_entirely_linked(self):
  base=json.loads((ROOT/'ui_data/browser_bundle_v0_9.json').read_text())
  self.assertEqual(len(base['cases']),50)
  self.assertFalse(base['counts']['publication_ready'])
  self.assertEqual(base['counts']['total_sources'],len(self.sources))
  total=0
  for inc in base['cases']:
   self.assertTrue(inc['source_count']>=3)
   self.assertFalse(inc['lineages_independently_certified'])
   sourceids={x['id'] for x in inc['sources']}
   for ev in inc['events']:
    self.assertIn(ev['sequence_basis'],('analytical_stage','reported_event_date','report_publication_date'))
    if ev['date'] is None:self.assertFalse(ev['date_is_reported_day'])
    for c in ev['claims']:
     self.assertIn(c['source_id'],sourceids)
     self.assertFalse(c['independent_fact_confirmation'])
   self.assertEqual(len(inc['graph']['edges']),len(inc['events'])-1)
   self.assertTrue(all(edge['relation']=='display_order_only' for edge in inc['graph']['edges']))
   total+=len(inc['events'])
  self.assertEqual(total,len(self.events))
 def test_not_pushed(self):
  checkpoint=json.loads((ROOT/'docs/checkpoint_v0_9.json').read_text())
  self.assertFalse(checkpoint['github_pushed']);self.assertFalse(checkpoint['publication_ready'])
if __name__=='__main__':unittest.main()
