import csv, json, unittest
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
def rd(n, base='data'):
 with (R/base/f'{n}.csv').open(encoding='utf-8',newline='') as f: return list(csv.DictReader(f))
class Version5(unittest.TestCase):
 def test_summary_is_actual_csv_count(self):
  a=json.loads((R/'docs'/'checkpoint_v0_5.json').read_text())
  for k,n in [('incidents','incidents'),('registered_sources_total','sources'),('events','events'),('claims','claims')]:self.assertEqual(a[k],len(rd(n,'data/frozen_v0_5')))
 def test_coverage_is_recomputed(self):
  cnt=Counter(s['incident_id'] for s in rd('sources') if s['source_role']=='case')
  for g in rd('publication_gate'):
   self.assertEqual(int(g['registered_source_count']),cnt[g['incident_id']]); self.assertEqual(g['passes_minimum_3']=='True',cnt[g['incident_id']]>=3)
 def test_no_passing_incident_has_fewer_than_three_sources(self):
  for row in rd('publication_gate'):
   if row['publication_gate']=='REVIEW_PENDING':self.assertGreaterEqual(int(row['registered_source_count']),3)
 def test_prior_25_incidents_preserved(self):
  rows=rd('incidents'); self.assertEqual([x['incident_id'] for x in rows[:25]],[f'LCI-{i:04d}' for i in range(1,26)])
 def test_3_new_cases_have_at_least_3_sources(self):
  for i in range(26,29):
   r=next(x for x in rd('publication_gate') if x['incident_id']==f'LCI-{i:04d}');self.assertGreaterEqual(int(r['registered_source_count']),3)
 def test_no_sources_from_active_media_distribution(self):
  for r in rd('sources'):
   self.assertNotIn('t.me/',r['url']);self.assertNotIn('instagram.com/',r['url'])
 def test_source_ids_contiguous_and_unique(self):
  ids=[int(x['source_id'].split('-')[1]) for x in rd('sources')];self.assertEqual(ids,list(range(1,max(ids)+1)))
 def test_old_missing_six_persisted(self):
  ids={x['source_id'] for x in rd('sources')};self.assertTrue(set(f'SB-{i:03d}' for i in range(58,64)).issubset(ids))
 def test_aligarh_procedure_not_conviction(self):
  i=next(x for x in rd('incidents') if x['incident_id']=='LCI-0020');self.assertIn('remand_refused',i['investigation_status']);self.assertNotIn('convicted',i['investigation_status'])
