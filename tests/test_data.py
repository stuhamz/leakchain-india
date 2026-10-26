import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from validate import load_tables, validate

class TestPilot(unittest.TestCase):
    def setUp(self):
        self.data=load_tables()
    def test_clean_release(self):
        self.assertEqual(validate(self.data), [])
    def test_bad_source_link_detected(self):
        altered=copy.deepcopy(self.data)
        altered['claims'][0]['source_id']='SB-999'
        self.assertTrue(any('source link' in e for e in validate(altered)))
    def test_allegation_not_finding(self):
        self.assertEqual(self.data['incidents'][0]['acquisition_status'],'official_allegation_reported')
    def test_kerala_unknown_acquisition(self):
        self.assertEqual(self.data['incidents'][1]['acquisition_code'],'A0')
        self.assertEqual(self.data['incidents'][1]['acquisition_status'],'unknown')
    def test_context_is_not_case_evidence(self):
        self.assertTrue(all(s['incident_id']=='' for s in self.data['sources'] if s['source_role']=='context'))
    def test_no_future_claims(self):
        altered=copy.deepcopy(self.data)
        altered['events'][0]['event_date']='2027-01-01'
        altered['events'][0]['date_precision']='day'
        altered['events'][0]['sequence_basis']='reported_event_date'
        self.assertTrue(any('future event' in e for e in validate(altered)))
    def test_sensitive_link_detection(self):
        altered=copy.deepcopy(self.data)
        altered['claims'][0]['claim_summary']='see https://example.com/suspect.mp4'
        self.assertTrue(any('sensitive URL' in e for e in validate(altered)))

    def test_content_profiles_exact_coverage(self):
        import csv
        with (Path(__file__).resolve().parents[1]/'data'/'content_profiles.csv').open(newline='',encoding='utf8') as fh:
            prof=list(csv.DictReader(fh))
        self.assertEqual(sorted(p['incident_id'] for p in prof),sorted(i['incident_id'] for i in self.data['incidents']))
    def test_threat_only_not_public_posting(self):
        import csv
        with (Path(__file__).resolve().parents[1]/'data'/'content_profiles.csv').open(newline='',encoding='utf8') as fh:
            prof={p['incident_id']:p for p in csv.DictReader(fh)}
        self.assertEqual(prof['LCI-0004']['circulation_scope'],'threat_only')
    def test_no_duplicate_source_urls(self):
        urls=[s['url'].rstrip('/') for s in self.data['sources']]
        self.assertEqual(len(urls),len(set(urls)))
    def test_category_distribution(self):
        labels={i['incident_id']:i['primary_category'] for i in self.data['incidents']}
        self.assertEqual(labels['LCI-0001'],'LC-01')
        self.assertEqual(labels['LCI-0005'],'LC-02')
        self.assertEqual(labels['LCI-0003'],'LC-03')

if __name__=='__main__': unittest.main()
