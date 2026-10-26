#!/usr/bin/env python3
"""Generate static, non-identifying browser/search/visualization data from audited CSVs.
No assumptions about event causality, exact chronology, offender guilt, or fact independence.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from pathlib import Path
import csv,json,re
from validate import ROOT,load_tables,validate,parse_id_list
OUT=ROOT/'ui_data'

def rows(name):
 with (ROOT/'data'/f'{name}.csv').open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))

def build():
 data=load_tables();issues=validate(data)
 if issues: raise ValueError('Invalid core dataset: '+str(issues[:5]))
 inc=data['incidents']; evs=data['events']; cls=data['claims']; src=data['sources'];
 src_i={x['source_id']:x for x in src};cla_i={x['claim_id']:x for x in cls}
 lineage={x['source_id']:x for x in rows('source_independence_v0_9')}
 claim_a={x['claim_id']:x for x in rows('claim_evidence_audit_v0_9')}
 profiles={x['incident_id']:x for x in rows('content_profiles')}
 excs=defaultdict(list)
 for x in rows('coding_exceptions'):excs[x['incident_id']].append(x)
 all_details=[];search=[]
 for x in inc:
  iid=x['incident_id'];profile=profiles[iid];sids=parse_id_list(x['source_ids'])
  source_cards=[{'id':s,'publisher':src_i[s]['publisher'],'title':src_i[s]['title'],'url':src_i[s]['url'],'published_on':src_i[s]['published_on'],'source_kind':src_i[s]['source_kind'],'origin_group':lineage[s]['origin_group'],'independence_status':lineage[s]['independence_status'],'review_method':lineage[s]['review_method'],'support_scope':lineage[s]['support_scope'],'limitation':src_i[s]['limitation']} for s in sids]
  events=[]
  for e in sorted((a for a in evs if a['incident_id']==iid),key=lambda r:int(r['display_order'])):
   evclaims=[]
   for cid in parse_id_list(e['claim_ids']):
    c=cla_i[cid];a=claim_a[cid]
    evclaims.append({'claim_id':cid,'source_id':c['source_id'],'status':c['claim_status'],'summary':c['claim_summary'],'source_locator':c['source_locator'],'analytical_limit':c['analytical_limit'],'evidence_level':a['evidence_level'],'adjudication_scope':a['adjudication_scope'],'independent_fact_confirmation':False})
   events.append({'event_id':e['event_id'],'step':int(e['display_order']),'type':e['event_type'],'date':e['event_date'] or None,'date_precision':e['date_precision'],'sequence_basis':e['sequence_basis'],'date_is_reported_day':bool(e['event_date'] and e['sequence_basis']=='reported_event_date'),'summary':e['summary'],'platform_or_system_role':e['platform_or_system_role'],'claims':evclaims})
  detail={'incident_id':iid,'label':x['label'],'state':x['state'],'primary_category':x['primary_category'],'acquisition_code':x['acquisition_code'],'acquisition_status':x['acquisition_status'],'circulation_status':x['circulation_status'],'commercial_distribution_status':x['commercial_distribution_status'],'investigation_status':x['investigation_status'],'case_boundary':x['case_boundary'],'limitation':x['limitation'],'content_modality':profile['content_modality'],'circulation_scope':profile['circulation_scope'],'exploitation_mode':profile['exploitation_mode'],'source_count':len(source_cards),'lineages_independently_certified':False,'publication_gate':'REVIEW_PENDING','events':events,'sources':source_cards,'unresolved_issues':excs[iid], 'graph':{'nodes':[{'id':e['event_id'],'type':e['type'],'order':e['step']} for e in events],'edges':[{'source':events[j]['event_id'],'target':events[j+1]['event_id'],'relation':'display_order_only'} for j in range(len(events)-1)],'causality_not_inferred':True}}
  all_details.append(detail)
  tokens=' '.join([x['label'],x['state'],x['primary_category'],x['acquisition_code'],x['circulation_status'],profile['exploitation_mode'],profile['content_modality'],profile['circulation_scope'],' '.join(e['summary'] for e in events)])
  tokens=re.sub(r'\s+',' ',tokens).lower().strip()
  search.append({'incident_id':iid,'label':x['label'],'state':x['state'],'category':x['primary_category'],'modality':profile['content_modality'],'scope':profile['circulation_scope'],'acquisition_code':x['acquisition_code'],'sources':len(sids),'event_types':sorted({e['type'] for e in events}),'issues_count':len(excs[iid]),'text':tokens})
 counts=lambda key:dict(sorted(Counter(a[key] for a in all_details).items()))
 stats={'total_incidents':len(all_details),'total_events':len(evs),'total_claims':len(cls),'total_sources':len(src),'incident_categories':counts('primary_category'),'states':counts('state'),'acquisition_codes':counts('acquisition_code'),'circulation_scopes':counts('circulation_scope'),'modalities':counts('content_modality'),'event_types':dict(sorted(Counter(x['type'] for i in all_details for x in i['events']).items())),'sources_by_kind':dict(sorted(Counter(s['source_kind'] for s in src).items())),'timeline_dates_known':sum(bool(x['date']) for i in all_details for x in i['events']),'timeline_dates_unknown':sum(not x['date'] for i in all_details for x in i['events']),'cases_with_unresolved_issues':sum(bool(i['unresolved_issues']) for i in all_details),'independent_incident_fact_certifications':0,'publication_ready':False}
 OUT.mkdir(exist_ok=True)
 bundle={'schema_version':'0.9','research_notice':'Source-attributed investigative research. Allegations are not adjudicated facts. Narrative graph edges do not establish causation or transfer. Exact dates only where recorded.','counts':stats,'cases':all_details}
 for name,obj in [('browser_bundle_v0_9.json',bundle),('search_index_v0_9.json',search),('chart_facets_v0_9.json',stats)]:
  (OUT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 print(f'UI-data exports: {len(all_details)} incident cards, {sum(len(i["events"]) for i in all_details)} timeline events, {len(src)} source register entries.')
 return bundle
if __name__=='__main__':build()
