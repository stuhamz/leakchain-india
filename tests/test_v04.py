import csv,unittest
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
def read(name,base='data'):
 with (ROOT/base/(name+'.csv')).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
class QualityExpansion(unittest.TestCase):
 def test_old_records_not_overwritten(self):
  for name in ('events','claims','sources','content_profiles'):
   old=read(name,'data/frozen_v0_3'); now=read(name)
   for earlier,current in zip(old,now):
    for col,value in earlier.items():
     if name=='events' and col=='claim_ids': self.assertEqual(current[col].split(';')[:len(value.split(';'))],value.split(';'))
     else: self.assertEqual(current[col],value)
 def test_22_old_incidents_are_same_except_new_source_ids(self):
  old=read('incidents','data/frozen_v0_3'); now=read('incidents')
  for a,b in zip(old,now):
   for col in a:
    if col=='source_ids':self.assertEqual(b[col].split(';')[:len(a[col].split(';'))],a[col].split(';'))
    elif a['incident_id']=='LCI-0020' and col in ('investigation_status','limitation'):self.assertNotEqual(b[col],a[col])
    else:self.assertEqual(b[col],a[col])
 def test_25_distinct_incidents(self):
  ids=[r['incident_id'] for r in read('incidents')[:25]]
  self.assertEqual(ids,[f'LCI-{x:04d}' for x in range(1,26)])
 def test_new_cases_have_three_sources(self):
  n=Counter(s['incident_id'] for s in read('sources') if s['source_role']=='case')
  for i in read('incidents')[22:]:self.assertGreaterEqual(n[i['incident_id']],3)
 def test_not_yet_publication_ready(self):
  p=read('publication_gate'); self.assertGreaterEqual(len(p),25)
  self.assertTrue(all(x['independent_lineages_verified']=='False' for x in p))
  self.assertFalse(any(x['publication_gate']=='PUBLISH' for x in p))
 def test_new_categories_are_real(self):
  cats={x['incident_id']:x['primary_category'] for x in read('incidents')}
  self.assertEqual(cats['LCI-0023'],'LC-04');self.assertEqual(cats['LCI-0024'],'LC-05')
 def test_no_fake_distribution_for_threats(self):
  prof={r['incident_id']:r for r in read('content_profiles')}
  for iid in ['LCI-0024']:
   self.assertEqual(prof[iid]['circulation_scope'],'threat_only')
   self.assertFalse(any(e['incident_id']==iid and e['event_type']=='distribution' for e in read('events')))
 def test_new_case_claims_are_grounded(self):
  es={e['event_id']:e for e in read('events')};ss={s['source_id']:s for s in read('sources')}
  for c in read('claims')[81:]:
   self.assertEqual(es[c['event_id']]['incident_id'],c['incident_id'])
   self.assertEqual(ss[c['source_id']]['incident_id'],c['incident_id'])
   self.assertTrue(c['source_locator'] and c['analytical_limit'])
 if __name__=='__main__':unittest.main()
