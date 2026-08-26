#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
l=json.loads((HERE/'source_ledger.json').read_text());c=json.loads((HERE/'canonical_census.json').read_text());p=json.loads((HERE/'held_schedule.json').read_text());h=json.loads((HERE/'results_hostile_tests.json').read_text());assert sha(HERE/'source_ledger.json')=='59cbe8e6464be1774bbf9310cacae4ef4c9cf076f6185926716881b376718587' and sha(HERE/'canonical_census.json')=='12773aacfd9fa702ce4202a5da64c356d0451be8b904ebcf9848bcbf99913261' and sha(HERE/'run_first25.py')=='0f85a651c70da8582451987fd56801fb44bdb6c2c611361f4a399d1d1034809e';assert c['closed_group_identification']['group_id']==0 and c['closed_group_identification']['source_sha256']=='c90c69b11ca931677bc1de138bdfc8c1eb7618d5aee20744764e4a4b1b511019';assert [x['group_id'] for x in c['groups']]==list(range(162));raw=[tuple(m) for x in c['groups'] for m in x['raw_members']];assert len(raw)==len(set(raw))==972 and sum(x['family']=='y' for x in c['groups'])==sum(x['family']=='z' for x in c['groups'])==81;assert l['selection']['selected_group_ids']==list(range(1,26)) and [x['group_id'] for x in l['lanes']]==list(range(1,26))
for x in l['lanes']:s=HERE/x['source_path'];assert sha(s)==x['source_sha256'] and s.stat().st_size==x['source_bytes'];text=s.read_text();assert text.count('ring r=0,')==text.count('ideal G=slimgb(I);')==text.count('poly remainder=reduce(1,G);')==text.count('quit;')==1
runner=(HERE/'run_first25.py').read_text();compile(runner,str(HERE/'run_first25.py'),'exec')
for token in ('proc_listpgrppids','proc_pid_rusage','group_rss','NATIVE_WALL=240','WRAPPER_WALL=250','RSS_CAP=8*1024**3','BATCH_ATTEMPT.json','if not unit:stop=','atomic(path,record)'):assert token in runner,token
assert p['scope']=={'representative':'rep4 only','source_regeneration_only':True,'solver_launches':0,'result_files':0,'attempt_markers':0,'clearances':0,'groups_newly_closed':0,'rep4_closed':False,'mathematical_coverage_added':False,'cross_representative_transport':False};assert h['status']=='PASS_10_HOSTILES_ZERO_RUN' and all(h['tests'].values())
for name in ('independent_referee_acceptance.schema.json','launch_clearance.schema.json'):s=json.loads((HERE/name).read_text());assert s['additionalProperties'] is False and set(s['required'])==set(s['properties'])
for absent in ('independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):assert not (HERE/absent).exists(),absent
assert not list(HERE.glob('*.tmp'))
for rel,expected in l['pins'].items():path=ROOT/rel;assert path.is_file() and sha(path)==expected
m=HERE/'MANIFEST.sha256';n=0
if m.exists():
 for line in m.read_text().splitlines():digest,name=line.split('  ',1);path=(HERE/name).resolve();assert path.is_file() and sha(path)==digest,name;n+=1
print(json.dumps({'status':'PASS_HELD_REP4_FIRST25_ZERO_RUN','closed_group':0,'selected':list(range(1,26)),'sources':25,'manifest_lines_checked':n,'solver_runs':0},sort_keys=True))
