#!/usr/bin/env python3
"""Create non-identifying, source-linked event summaries and DOT graphs."""
from pathlib import Path
from collections import defaultdict
import csv
import json
from validate import ROOT, load_tables, validate, parse_id_list

OUT = ROOT/'outputs'

def escape_dot(value: str) -> str:
    return value.replace('\\','\\\\').replace('"','\\"').replace('\n',' ')

def create_outputs(data):
    errors = validate(data)
    if errors:
        raise ValueError('Data validation must pass before reconstruction: '+ '; '.join(errors))
    OUT.mkdir(exist_ok=True)
    claims={r['claim_id']:r for r in data['claims']}
    sources={r['source_id']:r for r in data['sources']}
    allgraphs=[]
    report=['# LeakChain India | Generated source-linked timelines', '', 'Generated from the current release CSVs. Arrows in graph files are presentation order only, not causal links.', '']
    for incident in data['incidents']:
        iid = incident['incident_id']
        evs=sorted((x for x in data['events'] if x['incident_id']==iid), key=lambda x:int(x['display_order']))
        nodes=[]
        dot=['digraph "'+iid+'" {', '  rankdir=TB;', '  node [shape=box, style=rounded, fontname="Arial"];', '  edge [label="display order only", fontsize=9];']
        report += ['## '+iid+' | '+incident['label'], '', '**Acquisition:** '+incident['acquisition_code']+' / '+incident['acquisition_status']+'.  **Limit:** '+incident['limitation'], '']
        for index, ev in enumerate(evs):
            records=[]
            for cid in parse_id_list(ev['claim_ids']):
                c=claims[cid]
                records.append({'claim_id':cid,'source_id':c['source_id'],'source_url':sources[c['source_id']]['url'], 'status':c['claim_status'], 'claim':c['claim_summary'],'locator':c['source_locator'],'limit':c['analytical_limit']})
            nodes.append({'event_id':ev['event_id'],'display_order':int(ev['display_order']),'event_type':ev['event_type'],'date':ev['event_date'] or None,'sequence_basis':ev['sequence_basis'],'summary':ev['summary'],'evidence':records})
            label=f"{ev['event_id']} | {ev['event_type']}\n{ev['event_date'] or 'date unknown'}\n{ev['summary']}"
            dot.append('  "'+ev['event_id']+'" [label="'+escape_dot(label)+'"];')
            if index>0:
                dot.append('  "'+evs[index-1]['event_id']+'" -> "'+ev['event_id']+'";')
            report.append(f"{ev['display_order']}. **{ev['event_type']}** ({ev['event_date'] or 'underlying date unknown'}): {ev['summary']} Claims: {ev['claim_ids']}. Sequence basis: `{ev['sequence_basis']}`.")
        report.append('')
        dot.append('}')
        (OUT/(iid+'.dot')).write_text('\n'.join(dot)+'\n', encoding='utf-8')
        allgraphs.append({'incident_id':iid,'label':incident['label'],'primary_category':incident['primary_category'],'acquisition_code':incident['acquisition_code'],'acquisition_status':incident['acquisition_status'],'nodes':nodes, 'edge_semantics':'display order only; no causal or transfer inference'})
    (OUT/'incident_graphs.json').write_text(json.dumps(allgraphs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'timelines.md').write_text('\n'.join(report),encoding='utf-8')
    print('Wrote',len(allgraphs),'source-linked reconstructions to outputs/')

if __name__=='__main__':
    create_outputs(load_tables())
