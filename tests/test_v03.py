import csv
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def rows(name):
    with (ROOT/'data'/f'{name}.csv').open(encoding='utf8',newline='') as f:
        return list(csv.DictReader(f))

class Version03Checks(unittest.TestCase):
    def setUp(self):
        self.inc=rows('incidents');self.evs=rows('events');self.claims=rows('claims');self.src=rows('sources');self.profiles=rows('content_profiles');self.screen=rows('screening_log')
        self.byid={x['incident_id']:x for x in self.inc}
        self.pby={x['incident_id']:x for x in self.profiles}
    def test_22_distinct_incidents(self):
        self.assertGreaterEqual(len(self.inc),22)
        self.assertEqual(len(set(self.byid)),len(self.inc))
        self.assertEqual([x['incident_id'] for x in self.inc],[f'LCI-{n:04d}' for n in range(1,len(self.inc)+1)])
    def test_new_case_source_links(self):
        sid={s['source_id'] for s in self.src}
        for i in self.inc[8:]:
            self.assertTrue(set(i['source_ids'].split(';'))<=sid)
    def test_no_acquisition_hacking_without_source(self):
        self.assertFalse(any(i['acquisition_code']=='A5' for i in self.inc[8:22]))
    def test_unconfirmed_recordings_are_camera_placements(self):
        for iid in ['LCI-0014','LCI-0015']:
            first=[e for e in self.evs if e['incident_id']==iid and e['display_order']=='1']
            self.assertEqual([e['event_type'] for e in first],['camera_placement'])
            self.assertEqual(self.pby[iid]['circulation_scope'],'not_established')
    def test_threat_only_distinct_from_distribution(self):
        for i in self.inc:
            if self.pby[i['incident_id']]['circulation_scope']=='threat_only':
                self.assertIn('threat',i['circulation_status'])
                self.assertFalse(any(e['event_type']=='distribution' for e in self.evs if e['incident_id']==i['incident_id']))
    def test_claims_have_event_and_citation(self):
        ev={e['event_id']:e for e in self.evs};source={s['source_id']:s for s in self.src}
        for c in self.claims:
            self.assertEqual(ev[c['event_id']]['incident_id'],c['incident_id'])
            self.assertEqual(source[c['source_id']]['incident_id'],c['incident_id'])
            self.assertNotEqual(c['source_locator'].strip(),'')
    def test_screening_counterevidence(self):
        self.assertTrue(any('CMR engineering' in r['candidate_description'] and r['decision']=='deferred' for r in self.screen))
        self.assertTrue(any('Gudlavalleru' in r['candidate_description'] and r['decision']=='excluded' for r in self.screen))
    def test_source_count_and_no_content_host(self):
        self.assertGreaterEqual(len(self.src),35)
        for s in self.src:
            self.assertTrue(s['url'].startswith('https://'))
            self.assertNotIn('t.me/',s['url'])
    def test_no_judicial_finding_imputation_new(self):
        self.assertTrue(all(x['claim_status']!='judicial_finding' for x in self.claims if 9<=int(x['incident_id'].split('-')[1])<=22 and int(x['claim_id'].split('-')[1])<=165))
        # v0.8 court order records interim bail alone, not the alleged offence.
        procedural=[x for x in self.claims if x['claim_status']=='judicial_finding' and x['incident_id']=='LCI-0016']
        self.assertEqual(len(procedural),2)
        self.assertTrue(any('interim bail' in x['claim_summary'].lower() for x in procedural))
        self.assertTrue(any('filing register' in x['claim_summary'].lower() for x in procedural))
        self.assertTrue(all(x['analytical_limit'] and not any(w in x['claim_summary'].lower() for w in ['guilty','convicted']) for x in procedural))
    def test_new_incident_types(self):
        self.assertEqual(Counter(i['primary_category'] for i in self.inc[:22]),Counter({'LC-03':12,'LC-02':8,'LC-01':2}))

if __name__=='__main__':unittest.main()
