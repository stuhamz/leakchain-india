#!/usr/bin/env python3
"""Offline integrity checker for LeakChain India pilot data. No network access."""
from __future__ import annotations
import csv
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
TODAY = date(2026, 10, 26)  # release cutoff, not the date of execution
FILES = ['sources', 'incidents', 'events', 'claims']
REQUIRED = {
    'sources': ['source_id', 'incident_id', 'source_role', 'source_kind', 'published_on', 'publisher', 'title', 'url', 'accessed_on', 'origin_note', 'limitation'],
    'incidents': ['incident_id', 'label', 'state', 'primary_category', 'acquisition_code', 'acquisition_status', 'circulation_status', 'commercial_distribution_status', 'investigation_status', 'source_ids', 'case_boundary', 'limitation'],
    'events': ['event_id', 'incident_id', 'display_order', 'event_type', 'event_date', 'date_precision', 'sequence_basis', 'summary', 'platform_or_system_role', 'claim_ids'],
    'claims': ['claim_id', 'incident_id', 'event_id', 'source_id', 'claim_status', 'claim_summary', 'source_locator', 'analytical_limit'],
}
IDS = {'sources':'source_id','incidents':'incident_id','events':'event_id','claims':'claim_id'}
ALLOWED_DOMAINS = {
 'orissahighcourt.nic.in', 'www.loksatta.com', 'allaboutbelgaum.com', 'indiankanoon.org', 'www.abplive.com', 'www.ahmedabadmirror.com', 'www.daijiworld.com', 'www.deccanherald.com',
 'ndtv.in', 'epaper.navhindtimes.in', 'odishabytes.com', 'ommcomnews.com', 'tv9kannada.com', 'www.vijayavani.net', 'www.thestatesman.com',
 'www.indianeconomicobserver.com', 'www.devdiscourse.com', 'thesouthfirst.com', 'newsable.asianetnews.com', 'www.jagran.com', 'economictimes.indiatimes.com', 'www.ibc24.in', 'www.siasat.com', 'indtoday.com',
 'bangaloremirror.indiatimes.com', 'www.mid-day.com', 'www.thedailyjagran.com', 'www.amarujala.com', 'www.bbc.com', 'oecd.ai', 'news.abplive.com',
 'cyrilla.org', 'globalfreedomofexpression.columbia.edu', 'internetdemocracy.in', 'www.freepressjournal.in', 'www.tribuneindia.com', 'deshgujarat.com', 'hyderabadmail.com', 'malayalam.news18.com', 'www.asianetnews.com',
 'indianexpress.com', 'www.thenewsminute.com', 'keralakaumudi.com',
 'www.deccanchronicle.com', 'www.pib.gov.in', 'about.fb.com',
 'www.hindustantimes.com', 'www.ndtv.com', 'www.indiatoday.in', 'www.newindianexpress.com', 'timesofindia.indiatimes.com', 'www.onmanorama.com', 'www.thegoan.net', 'theprint.in', 'www.theweek.in', 'telanganatoday.com', 'www.indiatoday.in', 'www.newindianexpress.com', 'timesofindia.indiatimes.com', 'www.onmanorama.com', 'www.thegoan.net', 'theprint.in', 'www.theweek.in', 'telanganatoday.com',
}

def parse_id_list(s: str) -> list[str]:
    return [x.strip() for x in s.split(';') if x.strip()]

def load_tables(root: Path = ROOT) -> dict[str, list[dict[str, str]]]:
    result = {}
    for name in FILES:
        with (root / 'data' / f'{name}.csv').open(encoding='utf-8-sig', newline='') as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames != REQUIRED[name]:
                raise ValueError(f'{name}.csv columns do not match locked v0.1 schema')
            result[name] = list(reader)
    return result

def validate(data: dict[str, list[dict[str,str]]]) -> list[str]:
    errors = []
    codebook = json.loads((ROOT/'schemas'/'data_dictionary.json').read_text(encoding='utf-8'))
    keys = {}
    for name in FILES:
        rows = data[name]
        keys[name] = {r[IDS[name]] for r in rows}
        for value, count in Counter(r[IDS[name]] for r in rows).items():
            if not value or count != 1:
                errors.append(f'{name}: empty or duplicate ID {value!r}')
        for r in rows:
            if any(v is None for v in r.values()):
                errors.append(f'{name}: malformed CSV row {r}')
    lookup = {name:{r[IDS[name]]:r for r in data[name]} for name in FILES}
    for source in data['sources']:
        sid = source['source_id']
        if source['source_role'] not in codebook['source_role']:
            errors.append(f'{sid}: invalid source_role')
        if source['source_kind'] not in codebook['source_kind']:
            errors.append(f'{sid}: invalid source_kind')
        if source['source_role'] == 'case' and source['incident_id'] not in keys['incidents']:
            errors.append(f'{sid}: case source has missing incident')
        if source['source_role'] == 'context' and source['incident_id']:
            errors.append(f'{sid}: context source linked to incident')
        try:
            parsed = urlparse(source['url'])
            if parsed.scheme != 'https' or parsed.hostname not in ALLOWED_DOMAINS:
                errors.append(f'{sid}: source URL is not on reviewed publication whitelist')
        except ValueError:
            errors.append(f'{sid}: invalid URL')
        for field in ('published_on','accessed_on'):
            try:
                d = date.fromisoformat(source[field])
                if d > TODAY:
                    errors.append(f'{sid}: {field} after pilot cutoff')
            except ValueError:
                errors.append(f'{sid}: invalid {field}')
    for inc in data['incidents']:
        iid = inc['incident_id']
        if inc['primary_category'] not in codebook['categories']:
            errors.append(f'{iid}: invalid category')
        if inc['acquisition_code'] not in codebook['acquisition_codes']:
            errors.append(f'{iid}: invalid acquisition code')
        if inc['acquisition_status'] not in codebook['incident_acquisition_status_values']:
            errors.append(f'{iid}: invalid acquisition status')
        if inc['acquisition_code'] == 'A0' and inc['acquisition_status'] != 'unknown':
            errors.append(f'{iid}: A0 must be unknown')
        if inc['acquisition_code'] != 'A0' and inc['acquisition_status'] == 'unknown':
            errors.append(f'{iid}: non-A0 mechanism cannot have unknown status')
        for sid in parse_id_list(inc['source_ids']):
            s = lookup['sources'].get(sid)
            if not s or s['incident_id'] != iid or s['source_role'] != 'case':
                errors.append(f'{iid}: invalid source reference {sid}')
    for ev in data['events']:
        eid, iid = ev['event_id'], ev['incident_id']
        if iid not in keys['incidents']:
            errors.append(f'{eid}: invalid incident')
        if ev['event_type'] not in codebook['event_types']:
            errors.append(f'{eid}: invalid event type')
        if ev['sequence_basis'] not in codebook['sequence_basis']:
            errors.append(f'{eid}: invalid sequence basis')
        if ev['date_precision'] not in codebook['date_precision']:
            errors.append(f'{eid}: invalid date precision')
        if (bool(ev['event_date']) != (ev['date_precision'] == 'day')):
            errors.append(f'{eid}: date_precision/date mismatch')
        if ev['event_date']:
            try:
                if date.fromisoformat(ev['event_date']) > TODAY:
                    errors.append(f'{eid}: future event for release cutoff')
            except ValueError:
                errors.append(f'{eid}: invalid event date')
        if ev['sequence_basis'] == 'analytical_stage' and ev['event_date']:
            errors.append(f'{eid}: analytical undated stage incorrectly has exact date')
        if not ev['claim_ids']:
            errors.append(f'{eid}: unsubstantiated event')
        for cid in parse_id_list(ev['claim_ids']):
            claim = lookup['claims'].get(cid)
            if not claim or claim['incident_id'] != iid or claim['event_id'] != eid:
                errors.append(f'{eid}: dangling or mismatched claim {cid}')
        try:
            if int(ev['display_order']) < 1: raise ValueError()
        except ValueError:
            errors.append(f'{eid}: invalid display_order')
    for iid in keys['incidents']:
        indices = [int(e['display_order']) for e in data['events'] if e['incident_id']==iid and e['display_order'].isdigit()]
        if sorted(indices) != list(range(1,len(indices)+1)):
            errors.append(f'{iid}: non-contiguous event display_order')
    for claim in data['claims']:
        cid = claim['claim_id']
        ev = lookup['events'].get(claim['event_id'])
        source = lookup['sources'].get(claim['source_id'])
        if claim['claim_status'] not in codebook['claim_status_values']:
            errors.append(f'{cid}: invalid claim_status')
        if not ev or ev['incident_id'] != claim['incident_id']:
            errors.append(f'{cid}: invalid event link')
        if not source or source['incident_id'] != claim['incident_id'] or source['source_role']!='case':
            errors.append(f'{cid}: invalid case source link')
        if ev and cid not in parse_id_list(ev['claim_ids']):
            errors.append(f'{cid}: not referenced by parent event')
        if not claim['source_locator'] or not claim['analytical_limit']:
            errors.append(f'{cid}: no locator or limitation')
    # v0.2 profiles are mandatory and explicitly separate disclosure threats from actual posting.
    import csv as _csv
    with (ROOT/'data'/'content_profiles.csv').open(encoding='utf-8',newline='') as fh:
        profiles=list(_csv.DictReader(fh))
    valid_scopes={'reported_public_or_commercial','reported_wider_circulation_unspecified','reported_public_posting','reported_limited_sharing','threat_only','not_established'}
    pids=[r.get('incident_id','') for r in profiles]
    if Counter(pids) != Counter(keys['incidents']):
        errors.append('content_profiles: exact one-to-one incident coverage required')
    for p in profiles:
        if p.get('circulation_scope') not in valid_scopes:
            errors.append(f"{p.get('incident_id')}: invalid circulation scope")
        if not p.get('content_modality') or not p.get('exploitation_mode'):
            errors.append(f"{p.get('incident_id')}: missing content profile")
    for inc in data['incidents']:
        profile=next((p for p in profiles if p['incident_id']==inc['incident_id']),None)
        if not profile: continue
        if profile['circulation_scope']=='threat_only' and 'threat' not in inc['circulation_status']:
            errors.append(f"{inc['incident_id']}: threatened disclosure wrongly labelled")
    # Do not allow duplicate safe source URLs or forward-looking publication records.
    urls=[x['url'].rstrip('/') for x in data['sources']]
    if len(urls) != len(set(urls)):
        errors.append('sources: duplicated canonical URL')
    # Explicitly avoid public rows containing media URLs, account handles, or media file paths.
    for name in ('incidents','events','claims'):
        for row in data[name]:
            text = ' '.join(row.values())
            if re.search(r'https?://|\bt\.me/|\b@[\w]{3,}|\.(mp4|mov|mkv|avi)\b', text, re.I):
                errors.append(f'{name}: possible sensitive URL/handle/media filename in public data')
    return errors

def main():
    try:
        data=load_tables()
        errors=validate(data)
    except Exception as e:
        print('VALIDATION FAILED:',e)
        return 1
    if errors:
        print('VALIDATION FAILED')
        for error in errors: print(' -',error)
        return 1
    print('Validation passed: %d episodes, %d events, %d claims, %d sources (%d case, %d context)' % (
        len(data['incidents']),len(data['events']),len(data['claims']),len(data['sources']),
        sum(s['source_role']=='case' for s in data['sources']),
        sum(s['source_role']=='context' for s in data['sources'])))
    return 0

if __name__=='__main__':
    sys.exit(main())
