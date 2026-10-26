import csv, unittest
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def rd(n, folder='data'):
 with (R/folder/f'{n}.csv').open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
class Version6(unittest.TestCase):
 def test_frozen_v05_rows_preserved(self):
  for n in ('sources','claims','events'):
   old=rd(n,'data/frozen_v0_5');now=rd(n); ids=old[0].keys();key=list(ids)[0]
   for row in old:
    new=next(x for x in now if x[key]==row[key])
    for k in ids:
     if n=='events' and k=='claim_ids': self.assertTrue(new[k] == row[k] or new[k].startswith(row[k] + ';'))
     else:self.assertEqual(row[k],new[k])
 def test_all_new_cases_three_sources(self):
  cnt=Counter(s['incident_id'] for s in rd('sources') if s['source_role']=='case')
  for n in range(29,33):self.assertGreaterEqual(cnt[f'LCI-{n:04d}'],3)
 def test_source_claim_use(self):
  cs={r['source_id'] for r in rd('claims')}
  self.assertTrue(set('SB-%03d'%i for i in range(83,98)).issubset(cs))
 def test_synthetic_distinction(self):
  e=rd('events');p={r['incident_id']:r for r in rd('content_profiles')}
  for i in range(29,32):
   iid=f'LCI-{i:04d}';self.assertTrue(any(r['incident_id']==iid and r['event_type']=='synthetic_generation' for r in e))
  self.assertEqual(p['LCI-0029']['circulation_scope'],'threat_only')
  self.assertEqual(p['LCI-0031']['circulation_scope'],'reported_limited_sharing')
 def test_unpublished_gate(self):
  self.assertFalse(any(r['independent_lineages_verified']=='True' for r in rd('publication_gate')))
