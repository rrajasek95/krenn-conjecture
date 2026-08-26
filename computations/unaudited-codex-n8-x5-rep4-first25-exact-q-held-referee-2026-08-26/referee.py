#!/usr/bin/env python3
from __future__ import annotations
import hashlib,importlib.util,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
RUN=ROOT/'computations/unaudited-codex-n8-x5-rep4-first25-exact-q-held-2026-08-26'
DESIGN=ROOT/'computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25'
CLOSED=ROOT/'computations/unaudited-codex-n8-x5-rep4-all-equal-y-exact-q-held-plan-2026-08-25'
FIRST=ROOT/'computations/unaudited-codex-n8-x5-rep4-all-equal-y-exact-q-terminal-referee-2026-08-25'
SECOND=ROOT/'computations/unaudited-codex-n8-x5-rep4-all-equal-y-exact-q-terminal-second-referee-2026-08-25'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def replay(path):
    for line in path.read_text().splitlines():
        digest,name=line.split(None,1);p=Path(name.strip());p=p if p.is_absolute() else (path.parent/p).resolve();assert sha(p)==digest,(p,sha(p),digest)

pins={
 RUN/'MANIFEST.sha256':'d6c098fb885ad9faac566b6f01a9e94f01aa6a8b4a61562ec4fa14f66b44a029',
 RUN/'source_ledger.json':'59cbe8e6464be1774bbf9310cacae4ef4c9cf076f6185926716881b376718587',
 RUN/'canonical_census.json':'12773aacfd9fa702ce4202a5da64c356d0451be8b904ebcf9848bcbf99913261',
 RUN/'run_first25.py':'0f85a651c70da8582451987fd56801fb44bdb6c2c611361f4a399d1d1034809e',
 RUN/'held_schedule.json':'0cf3e98e50687b21c69717d9792388defcc28c569cc935613b431d3fac3f416d',
 RUN/'results_hostile_tests.json':'558eb3eb88f11dc78b702b992edae824575aefe786907a7ddeab5d4fb73116a9',
 DESIGN/'MANIFEST.sha256':'7f47c0567580aba565925b95860bace46ebaf5703aace4ec8aa100f48ec33e02',
 DESIGN/'generate_design.py':'b83218b25635efe8c46ff2faf9e2028921408d884be7fb2e4d8541ccdf9c847a',
 CLOSED/'rep4_all_equal_y_exact_Q.sing':'c90c69b11ca931677bc1de138bdfc8c1eb7618d5aee20744764e4a4b1b511019',
 CLOSED/'TERMINAL_MANIFEST.sha256':'ff3178d7b546d4afadeeb8659001685d7d5bd3bb78c73b06b33ed539184e6d5d',
 FIRST/'FINAL_MANIFEST.sha256':'a8280c98344eb62f6df89ffec125e6cdba33a7dae63f47061c71114f7aabe805',
 SECOND/'FINAL_MANIFEST.sha256':'b2a543e59df1edf32df414f44938b418e35ea4ed258354642aff3d2b45e522b4',
}
for path,want in pins.items():assert sha(path)==want,(path,sha(path),want)
replay(RUN/'MANIFEST.sha256');replay(DESIGN/'MANIFEST.sha256');replay(CLOSED/'TERMINAL_MANIFEST.sha256');replay(FIRST/'FINAL_MANIFEST.sha256');replay(SECOND/'FINAL_MANIFEST.sha256')

spec=importlib.util.spec_from_file_location('rep4_independent_design',DESIGN/'generate_design.py');assert spec and spec.loader
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
raw,groups=module.orbit_ledger();ordered=sorted(groups.items())
assert len(raw)==972 and len(ordered)==162 and all(len(members)==6 for _,members in ordered)
assert sum(rep[4]=='y' for rep,_ in ordered)==81 and sum(rep[4]=='z' for rep,_ in ordered)==81
census=json.loads((RUN/'canonical_census.json').read_text())
assert census['counts']=={'raw':972,'canonical_groups':162,'members_each':6,'y_groups':81,'z_groups':81}
epilogue='''ideal G=slimgb(I);\nprint("GROEBNER_SIZE="+string(size(G)));\npoly remainder=reduce(1,G);\nprint("UNIT_REMAINDER="+string(remainder));\nif (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\nquit;\n'''
regenerated=[]
for gid,(representative,members) in enumerate(ordered):
    base=module.build_program(representative);assert base.endswith('quit;\n') and base.count('quit;')==1
    q=base[:-len('quit;\n')]+epilogue;data=q.encode()
    regenerated.append({'group_id':gid,'canonical_chart':list(representative),'family':representative[4],'raw_members':[list(x) for x in sorted(members)],'raw_member_count':len(members),'exact_Q_source_sha256':hashlib.sha256(data).hexdigest(),'exact_Q_source_bytes':len(data)})
assert regenerated==census['groups']
matches=[x for x in regenerated if x['exact_Q_source_sha256']==pins[CLOSED/'rep4_all_equal_y_exact_Q.sing']]
assert len(matches)==1 and matches[0]['group_id']==0 and matches[0]['canonical_chart']==[0,0,0,0,'y',0,0,1]
assert census['closed_group_identification']=={'group_id':0,'method':'unique exact-Q source SHA match to independently sealed all-equal-y chart','chart':[0,0,0,0,'y',0,0,1],'source_sha256':pins[CLOSED/'rep4_all_equal_y_exact_Q.sing'],'terminal_manifest_sha256':pins[CLOSED/'TERMINAL_MANIFEST.sha256'],'first_referee_manifest_sha256':pins[FIRST/'FINAL_MANIFEST.sha256'],'second_referee_manifest_sha256':pins[SECOND/'FINAL_MANIFEST.sha256']}

ledger=json.loads((RUN/'source_ledger.json').read_text());lanes=ledger['lanes']
assert ledger['selection']=={'excluded_proven_group_ids':[0],'rule':'25 lowest canonical group IDs after excluding exactly the sealed all-equal-y group','selected_group_ids':list(range(1,26))}
assert [x['group_id'] for x in lanes]==list(range(1,26)) and [x['ordinal'] for x in lanes]==list(range(1,26))
for lane in lanes:
    source=RUN/lane['source_path'];entry=regenerated[lane['group_id']]
    assert lane['canonical_chart']==entry['canonical_chart'] and lane['family']==entry['family']
    assert lane['variables']==91 and lane['generators']==6577
    assert sha(source)==lane['source_sha256']==entry['exact_Q_source_sha256']
    assert source.stat().st_size==lane['source_bytes']==entry['exact_Q_source_bytes']
    text=source.read_text();assert text.count('ring r=0,')==text.count('ideal G=slimgb(I);')==text.count('poly remainder=reduce(1,G);')==text.count('quit;')==1

runner=(RUN/'run_first25.py').read_text()
for token in ('SELECTED=tuple(range(1,26))','NATIVE_WALL=240','WRAPPER_WALL=250','RSS_CAP=8*1024**3','LIB.proc_listpgrppids','LIB.proc_pid_rusage','if not unit:stop=',"'parallel':False","'relaunch':False",'atomic(path,record)',"exclusive(HERE/'BATCH_ATTEMPT.json'"):
    assert token in runner,token
assert runner.count('subprocess.Popen(')==1 and 'start_new_session=True' in runner
hostile=json.loads((RUN/'results_hostile_tests.json').read_text());assert hostile['status']=='PASS_10_HOSTILES_ZERO_RUN' and hostile['solver_runs']==0 and len(hostile['tests'])==10 and all(hostile['tests'].values())
for absent in ('independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):
    assert not (RUN/absent).exists(),absent
assert not list(RUN.rglob('*.tmp'))
schedule=json.loads((RUN/'held_schedule.json').read_text());assert schedule['scope']['solver_launches']==schedule['scope']['result_files']==schedule['scope']['groups_newly_closed']==0
out={'schema':'KRENN_X5_REP4_FIRST25_EXACT_Q_HELD_REFEREE_V1','status':'PASS_APPROVE_HELD_STRICT_REP4_FIRST25_ZERO_RUN','producer_manifest_sha256':pins[RUN/'MANIFEST.sha256'],'canonical_census_sha256':pins[RUN/'canonical_census.json'],'source_ledger_sha256':pins[RUN/'source_ledger.json'],'runner_sha256':pins[RUN/'run_first25.py'],'raw_charts':972,'canonical_groups':162,'members_each':6,'y_groups':81,'z_groups':81,'closed_group_id':0,'closed_source_sha256':pins[CLOSED/'rep4_all_equal_y_exact_Q.sing'],'closed_first_referee_manifest_sha256':pins[FIRST/'FINAL_MANIFEST.sha256'],'closed_second_referee_manifest_sha256':pins[SECOND/'FINAL_MANIFEST.sha256'],'selected_group_ids':list(range(1,26)),'sources_byte_identical':25,'variables_each':91,'generators_each':6577,'native_wall_seconds_each':240,'wrapper_wall_seconds_each':250,'rss_cap_bytes_each':8589934592,'strict_sequential':True,'stop_first':True,'parallel':False,'skip':False,'reorder':False,'relaunch':False,'hostiles_rejected':10,'solver_runs':0,'mathematical_coverage_added':False,'rep4_closed':False,'conjecture_closed':False,'approval':'HELD_ONLY_NO_LAUNCH'}
(HERE/'results_referee.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':out['status'],'groups':[1,25],'sources':25,'runs':0,'result_sha256':sha(HERE/'results_referee.json')},sort_keys=True))
