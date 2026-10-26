import csv, unittest, json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
def read(n,folder='data'):
 if folder=='data':folder='data/frozen_v0_7'
 with (R/folder/f'{n}.csv').open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
class Version7(unittest.TestCase):
 def setUp(self):
  self.inc=read('incidents');self.src=read('sources');self.eve=read('events');self.clm=read('claims')
 def test_frozen_v06_untouched_except_additive_backfill(self):
  for n in ('incidents','sources','events','claims','content_profiles','source_lineage_audit','coding_exceptions'):
   a=read(n,'data/frozen_v0_6');b=read(n)
   if n=='coding_exceptions':
    before=Counter(tuple(sorted(x.items())) for x in a);after=Counter(tuple(sorted(x.items())) for x in b)
    self.assertFalse(before-after)
    continue
   key=list(a[0].keys())[0];lookup={r[key]:r for r in b}
   for old in a:
    self.assertIn(old[key],lookup)
    new=lookup[old[key]]
    for col,value in old.items():
     if (n=='incidents' and col=='source_ids' and old[key] in ['LCI-0006','LCI-0011','LCI-0022'] or n=='events' and col=='claim_ids' and old['incident_id'] in ['LCI-0006','LCI-0011','LCI-0022']):
      self.assertTrue(new[col].startswith(value+';') or new[col]==value,(n,old[key],col))
     else:self.assertEqual(new[col],value,(n,old[key],col))
 def test_primary_ids_and_cardinality(self):
  self.assertEqual([r['incident_id'] for r in self.inc],[f'LCI-{i:04d}' for i in range(1,39)])
  self.assertEqual([r['source_id'] for r in self.src],[f'SB-{i:03d}' for i in range(1,120)])
  self.assertEqual([r['event_id'] for r in self.eve],[f'EV-{i:03d}' for i in range(1,155)])
  self.assertEqual([r['claim_id'] for r in self.clm],[f'CL-{i:03d}' for i in range(1,166)])
 def test_each_new_source_used_in_claim(self):
  referenced={c['source_id'] for c in self.clm}
  self.assertTrue(set(f'SB-{n:03d}' for n in range(98,120)).issubset(referenced))
 def test_new_cases_three_sources(self):
  counts=Counter(s['incident_id'] for s in self.src if s['source_role']=='case')
  for n in range(33,39):self.assertEqual(counts[f'LCI-{n:04d}'],3)
  self.assertEqual([id for id in (r['incident_id'] for r in self.inc) if counts[id]<3],['LCI-0005','LCI-0008','LCI-0016','LCI-0019'])
  self.assertEqual(sum(max(0,3-counts[id]) for id in [r['incident_id'] for r in self.inc]),6)
 def test_lc07_fraudulent_solicitation(self):
  cats={r['incident_id']:r['primary_category'] for r in self.inc}
  self.assertEqual(cats['LCI-0033'],'LC-07')
  self.assertEqual(cats['LCI-0034'],'LC-04')
  self.assertEqual(cats['LCI-0036'],'LC-05')
  self.assertIn('LC-07',json.loads((R/'schemas/data_dictionary.json').read_text())['categories'])
 def test_synthetic_type_but_not_real_recording(self):
  for iid in ['LCI-0036','LCI-0038']:
   et={ev['event_type'] for ev in self.eve if ev['incident_id']==iid}
   self.assertIn('synthetic_generation',et)
   self.assertNotIn('recording',et)
 def test_threat_scope_and_misuse(self):
  cp={p['incident_id']:p for p in read('content_profiles')}
  self.assertEqual(cp['LCI-0033']['circulation_scope'],'threat_only')
  self.assertEqual(cp['LCI-0037']['circulation_scope'],'reported_limited_sharing')
  self.assertEqual(cp['LCI-0038']['circulation_scope'],'reported_limited_sharing')
 def test_narrative_count_units_and_unresolved_dates(self):
  inc={i['incident_id']:i for i in self.inc}
  self.assertIn('investment',inc['LCI-0033']['limitation'])
  self.assertIn('2024',inc['LCI-0034']['limitation'])
  self.assertIn('OTP',inc['LCI-0037']['limitation'])
  self.assertTrue(any(r['incident_id']=='LCI-0034' and r['status']=='unresolved_chronology_and_dedup' for r in read('coding_exceptions')))
 def test_screening_dedup(self):
  logs=read('screening_log')
  for n in range(33,39):self.assertEqual(len([r for r in logs if r['decision']=='admitted' and r['linked_incident_id']==f'LCI-{n:04d}']),1)
  self.assertTrue(any('Coimbatore' in r['candidate_description'] and r['decision']=='deferred' for r in logs))
 def test_publication_hold(self):
  gates=read('publication_gate')
  self.assertEqual(len(gates),38)
  self.assertFalse(any(r['independent_lineages_verified']=='True' for r in gates))
  self.assertFalse(any(r['publication_gate']=='PUBLISH' for r in gates))
