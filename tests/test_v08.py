"""Version 0.8 research gate and v0.7 immutability tests."""
import csv, json, unittest
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def rows(n,folder='data/frozen_v0_8'):
 with (R/folder/f'{n}.csv').open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
class Version8(unittest.TestCase):
 def setUp(self):
  self.inc=rows('incidents');self.src=rows('sources');self.eve=rows('events');self.claim=rows('claims')
  self.p={x['incident_id']:x for x in rows('content_profiles')}
  self.count=Counter(x['incident_id'] for x in self.src if x['source_role']=='case')
 def test_contiguous_and_counts(self):
  for table,prefix,width,key in [(self.inc,'LCI',4,'incident_id'),(self.src,'SB',3,'source_id'),(self.eve,'EV',3,'event_id'),(self.claim,'CL',3,'claim_id')]:
   self.assertEqual([x[key] for x in table],[f'{prefix}-{i:0{width}d}' for i in range(1,len(table)+1)])
  self.assertEqual((len(self.inc),len(self.src),len(self.eve),len(self.claim)),(50,157,203,216))
 def test_frozen_v07_identical_exceptions_only_additive(self):
  oldnames=['incidents','sources','events','claims','content_profiles','source_lineage_audit','coding_exceptions','screening_log']
  for n in oldnames:
   old=rows(n,'data/frozen_v0_7');new=rows(n)
   if n in ['coding_exceptions','screening_log']:
    self.assertEqual(new[:len(old)],old,n)
    continue
   key=list(old[0])[0];now={r[key]:r for r in new}
   for r in old:
    self.assertIn(r[key],now,(n,r[key]))
    for k,v in r.items():
     c=now[r[key]][k]
     if (n=='incidents' and k=='source_ids' and r[key] in ['LCI-0016','LCI-0019']) or (n=='events' and k=='claim_ids' and r['incident_id'] in ['LCI-0016','LCI-0019']):
      self.assertTrue(c==v or c.startswith(v+';'),(n,r[key],k,c,v))
     else:self.assertEqual(c,v,(n,r[key],k))
 def test_every_new_case_has_three_distinct_registered_sources(self):
  source_byid={x['source_id']:x for x in self.src}
  for i in range(39,51):
   iid=f'LCI-{i:04d}';inc=next(x for x in self.inc if x['incident_id']==iid)
   sids=inc['source_ids'].split(';');self.assertGreaterEqual(len(sids),3)
   self.assertEqual(len(sids),len(set(sids)))
   self.assertEqual(len({source_byid[s]['publisher'] for s in sids}),len(sids))
   self.assertEqual(self.count[iid],len(sids))
 def test_publication_gate_and_gaps(self):
  gate=rows('publication_gate');self.assertEqual(len(gate),50)
  gaps=[x['incident_id'] for x in self.inc if self.count[x['incident_id']]<3]
  self.assertEqual(gaps,['LCI-0005','LCI-0008','LCI-0016','LCI-0019'])
  self.assertEqual(sum(max(0,3-self.count[x['incident_id']]) for x in self.inc),4)
  self.assertEqual(sum(self.count[x['incident_id']]>=3 for x in self.inc),46)
  for g in gate:
   self.assertEqual(int(g['registered_source_count']),self.count[g['incident_id']])
   self.assertEqual(g['publication_gate'],'HOLD' if self.count[g['incident_id']]<3 else 'REVIEW_PENDING')
   self.assertEqual(g['independent_lineages_verified'],'False')
 def test_procedural_judicial_claim_not_guilt(self):
  c=next(x for x in self.claim if x['incident_id']=='LCI-0016' and x['claim_status']=='judicial_finding')
  s=next(x for x in self.src if x['source_id']==c['source_id'])
  self.assertEqual(s['source_kind'],'judicial_primary')
  self.assertIn('interim bail',c['claim_summary'].lower())
  self.assertIn('neither proves',c['analytical_limit'])
 def test_disclosure_scope_critical_distinctions(self):
  self.assertEqual(self.p['LCI-0041']['circulation_scope'],'reported_public_or_commercial')
  self.assertEqual(self.p['LCI-0042']['circulation_scope'],'not_established')
  self.assertEqual(self.p['LCI-0048']['circulation_scope'],'reported_limited_sharing')
  self.assertEqual(self.p['LCI-0050']['circulation_scope'],'threat_only')
  types={x['event_type'] for x in self.eve if x['incident_id']=='LCI-0050'}
  self.assertIn('synthetic_generation',types)
  self.assertNotIn('recording',types)
 def test_case_conflicts_are_documented(self):
  exceptions=rows('coding_exceptions')
  for iid in ['LCI-0016','LCI-0019','LCI-0041','LCI-0047','LCI-0048','LCI-0050']:
   self.assertTrue(any(x['incident_id']==iid for x in exceptions),iid)
 def test_no_published_media_or_private_accounts(self):
  files=list((R/'outputs').glob('*'))
  self.assertTrue(all(p.suffix in ('.dot','.json','.md') for p in files))
  self.assertFalse(any('instagram.com/' in s['url'] or 't.me/' in s['url'] for s in self.src))
 def test_next_ids_and_archive_gate(self):
  ck=json.loads((R/'docs/checkpoint_v0_8.json').read_text(encoding='utf8'))
  self.assertEqual(ck['next_incident_id'],'LCI-0051')
  self.assertFalse(ck['public_release_ready'] or ck['github_pushed'])
  self.assertEqual(ck['source_lineages_independently_certified'],0)
if __name__=='__main__':unittest.main()
