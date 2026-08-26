#!/usr/bin/env python3
"""Independent zero-run referee for held rep4 groups126..161."""
from __future__ import annotations
import ast,copy,hashlib,importlib.util,json,os
from pathlib import Path
H=Path(__file__).resolve().parent; ROOT=H.parents[1]
PKG=ROOT/'computations/unaudited-codex-n8-x5-rep4-groups126-161-exact-q-conditional-held-2026-08-26'
BASE=ROOT/'computations/unaudited-codex-n8-x5-rep4-first25-exact-q-held-2026-08-26'
DESIGN=ROOT/'computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25'
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  while chunk:=f.read(1<<20): h.update(chunk)
 return h.hexdigest()
def replay(manifest):
 n=0
 for line in manifest.read_text().splitlines():
  if not line.strip(): continue
  digest,name=line.split(None,1); p=(manifest.parent/name.strip()).resolve(); assert p.is_file() and sha(p)==digest,(p,sha(p),digest); n+=1
 return n
PINS={
 PKG/'MANIFEST.sha256':'62884ffc80b9507cfe105ead45579f7116d1db74e5393da4930656546eba0dc2',
 PKG/'source_ledger.json':'fa301fd4d1e61626781cedd3ecb362189671b042c9cba8cfbe68977bb79ceb38',
 PKG/'future_dependencies.json':'18b7cae58e965187bcbb97ef7a319aacd92fccb6be4010d9630caad83ef77e75',
 PKG/'dependency_verifier.py':'fc44d47caef2915dc8cf7dc384d544e8c858e4be8de372b08d01a30abb3b90eb',
 PKG/'results_hostile_tests.json':'b15cdacc3ff88d14b43760f430bd9ba327fe332d1d34a99d1b5ffb989dcfcc90',
 PKG/'run_groups126_161.py':'959ab7cfa85ddf23f328ae03edeaefabc0a775ede98b4768953b46c91fe0022a',
 BASE/'MANIFEST.sha256':'d6c098fb885ad9faac566b6f01a9e94f01aa6a8b4a61562ec4fa14f66b44a029',
 BASE/'canonical_census.json':'12773aacfd9fa702ce4202a5da64c356d0451be8b904ebcf9848bcbf99913261',
 DESIGN/'MANIFEST.sha256':'7f47c0567580aba565925b95860bace46ebaf5703aace4ec8aa100f48ec33e02',
 DESIGN/'generate_design.py':'b83218b25635efe8c46ff2faf9e2028921408d884be7fb2e4d8541ccdf9c847a',
}
for p,d in PINS.items(): assert sha(p)==d,(p,sha(p),d)
counts={'package':replay(PKG/'MANIFEST.sha256'),'base':replay(BASE/'MANIFEST.sha256'),'design':replay(DESIGN/'MANIFEST.sha256')}
spec=importlib.util.spec_from_file_location('rep4_final36_design',DESIGN/'generate_design.py'); assert spec and spec.loader
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
census=json.loads((BASE/'canonical_census.json').read_text()); assert census['status']=='PASS_REGENERATED_AUTHORITATIVE_972_TO_162_CENSUS'
assert census['counts']=={'raw':972,'canonical_groups':162,'members_each':6,'y_groups':81,'z_groups':81} and [x['group_id'] for x in census['groups']]==list(range(162))
ep='''ideal G=slimgb(I);\nprint("GROEBNER_SIZE="+string(size(G)));\npoly remainder=reduce(1,G);\nprint("UNIT_REMAINDER="+string(remainder));\nif (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\nquit;\n'''
ledger=json.loads((PKG/'source_ledger.json').read_text()); lanes=ledger['lanes']; selected=list(range(126,162))
assert ledger['selection']['required_closed_union']==list(range(126)) and ledger['selection']['selected_group_ids']==selected
assert [x['group_id'] for x in lanes]==selected and [x['ordinal'] for x in lanes]==list(range(1,37))
total=0
for lane in lanes:
 rec=census['groups'][lane['group_id']]; q=m.build_program(tuple(rec['canonical_chart'])); assert q.endswith('quit;\n') and q.count('quit;')==1
 data=(q[:-len('quit;\n')]+ep).encode(); digest=hashlib.sha256(data).hexdigest(); source=PKG/lane['source_path']
 assert lane['canonical_chart']==rec['canonical_chart'] and lane['family']==rec['family']
 assert digest==rec['exact_Q_source_sha256']==lane['source_sha256']==sha(source) and source.read_bytes()==data
 assert len(data)==rec['exact_Q_source_bytes']==lane['source_bytes']==source.stat().st_size
 assert lane['variables']==91 and lane['generators']==6577; total+=len(data)
contract=json.loads((PKG/'future_dependencies.json').read_text())
assert contract['status']=='UNSATISFIED_THREE_NULL_HASH_PAIRS' and contract['satisfied'] is False and contract['required_closed_union']==list(range(126))
assert [d['name'] for d in contract['dependencies']]==['groups1_25','groups26_75','groups76_125']
assert all(not d['satisfied'] and d['manifest_sha256'] is d['result_sha256'] is None for d in contract['dependencies'])
for d in contract['dependencies']: assert not (ROOT/d['manifest_path']).exists() and not (ROOT/d['result_path']).exists()
sv=importlib.util.spec_from_file_location('rep4_final36_verifier',PKG/'dependency_verifier.py'); assert sv and sv.loader
v=importlib.util.module_from_spec(sv); sv.loader.exec_module(v)
good=[{'schema':d['result_schema'],'status':d['result_status'],'groups_closed':list(d['groups_closed'])} for d in contract['dependencies']]
hostiles={}
def reject(name,cm=None,rm=None,mhs=None,rhs=None):
 c,r=copy.deepcopy(contract),copy.deepcopy(good)
 if cm: cm(c)
 if rm: rm(r)
 try: v.validate_payload(c,r,mhs or ['a'*64,'b'*64,'c'*64],rhs or ['d'*64,'e'*64,'f'*64])
 except (AssertionError,KeyError,TypeError): hostiles[name]=True
 else: hostiles[name]=False
reject('null_treated_satisfied',lambda c:c.__setitem__('satisfied',True)); reject('future_hash_injected',lambda c:c['dependencies'][0].__setitem__('manifest_sha256','0'*64)); reject('dependency_order_swapped',lambda c:c['dependencies'].reverse())
reject('first_wrong_schema',rm=lambda r:r[0].__setitem__('schema','wrong')); reject('first_missing',rm=lambda r:r[0]['groups_closed'].pop()); reject('first_duplicate',rm=lambda r:r[0]['groups_closed'].__setitem__(24,24))
reject('middle_wrong_status',rm=lambda r:r[1].__setitem__('status','wrong')); reject('middle_missing',rm=lambda r:r[1]['groups_closed'].pop()); reject('middle_duplicate',rm=lambda r:r[1]['groups_closed'].__setitem__(49,74)); reject('middle_reordered',rm=lambda r:r[1]['groups_closed'].reverse())
reject('third_wrong_schema',rm=lambda r:r[2].__setitem__('schema','wrong')); reject('third_wrong_status',rm=lambda r:r[2].__setitem__('status','wrong')); reject('third_missing',rm=lambda r:r[2]['groups_closed'].pop()); reject('third_duplicate',rm=lambda r:r[2]['groups_closed'].__setitem__(49,124)); reject('third_reordered',rm=lambda r:r[2]['groups_closed'].reverse())
reject('cross_first_middle_overlap',rm=lambda r:r[1]['groups_closed'].__setitem__(0,25)); reject('cross_middle_third_overlap',rm=lambda r:r[2]['groups_closed'].__setitem__(0,75)); reject('union_extra',lambda c:c['required_closed_union'].append(126)); reject('bad_manifest_hash',mhs=['a'*63,'b'*64,'c'*64]); reject('bad_result_hash',rhs=['d'*64,'e'*64,'z'*64])
fabricated=v.validate_payload(contract,good,['a'*64,'b'*64,'c'*64],['d'*64,'e'*64,'f'*64])
try: v.verify_payload(contract,fabricated,ROOT)
except (AssertionError,FileNotFoundError): hostiles['fabricated_or_stale_normalized_all_six_artifacts_absent']=True
else: hostiles['fabricated_or_stale_normalized_all_six_artifacts_absent']=False
pack=json.loads((PKG/'results_hostile_tests.json').read_text()); assert len(hostiles)==21 and all(hostiles.values()) and pack['tests']==hostiles and pack['status']=='PASS_21_HOSTILES_ALL_THREE_FUTURES_ABSENT' and pack['solver_runs']==0
runner=(PKG/'run_groups126_161.py').read_text(); ast.parse(runner)
for token in ('SELECTED=tuple(range(126,162))','NATIVE_WALL=240','WRAPPER_WALL=250','RSS_CAP=8*1024**3','proc_listpgrppids','proc_pid_rusage',"assert NORMALIZED.is_file(),'HELD: all three future dependencies have not been normalized'",'for lane in lanes:',"'parallel':False","'relaunch':False",'atomic(path,record)'): assert token in runner,token
assert runner.count('subprocess.Popen(')==1 and 'start_new_session=True' in runner
for absent in ('normalized_dependencies.json','independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'): assert not (PKG/absent).exists(),absent
assert not list(PKG.rglob('*.tmp'))
out={'schema':'KRENN_X5_REP4_GROUPS126_161_CONDITIONAL_HELD_REFEREE_V1','status':'PASS_CONDITIONAL_HELD_GROUPS126_161_BLOCKED_ZERO_RUNS','producer_manifest_sha256':PINS[PKG/'MANIFEST.sha256'],'source_ledger_sha256':PINS[PKG/'source_ledger.json'],'authoritative_census_sha256':PINS[BASE/'canonical_census.json'],'dependency_verifier_sha256':PINS[PKG/'dependency_verifier.py'],'future_dependencies_sha256':PINS[PKG/'future_dependencies.json'],'runner_sha256':PINS[PKG/'run_groups126_161.py'],'required_future_groups':[list(range(1,26)),list(range(26,76)),list(range(76,126))],'derived_union_if_satisfied':list(range(126)),'dependency_satisfied':False,'future_hashes':[None]*6,'future_files_present':False,'runner_replays_all_six_terminal_artifacts_before_attempt':True,'hostiles_passed':21,'fabricated_or_stale_normalized_rejected':True,'selected_group_ids':selected,'canonical_sources_verified':36,'total_source_bytes':total,'variables_each':91,'generators_each':6577,'limits_each':{'native_wall_seconds':240,'wrapper_wall_seconds':250,'rss_cap_bytes':8*1024**3},'strict_sequential_stop_first':True,'manifest_counts':counts,'scope':{'held_approval_only':True,'launch_authorized':False,'solver_runs':0,'mathematical_coverage':False,'rep4_closed':False}}
approval={'schema':'KRENN_X5_REP4_GROUPS126_161_CONDITIONAL_HELD_APPROVAL_NOT_EXECUTOR_ACCEPTANCE_V1','status':'PASS_HELD_ONLY_BLOCKED_ON_ALL_THREE_EXACT_TERMINAL_BINDINGS','producer_manifest_sha256':PINS[PKG/'MANIFEST.sha256'],'dependency_spec_sha256':PINS[PKG/'future_dependencies.json'],'future_terminal_hashes':[None]*6,'selected_group_ids':selected,'launch_authorized':False,'solver_runs':0}
for name,obj in [('results_referee.json',out),('HELD_APPROVAL.json',approval)]:
 t=H/(name+'.tmp'); t.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); os.replace(t,H/name)
print(json.dumps({'status':out['status'],'sources':36,'bytes':total,'hostiles':21,'runs':0,'result_sha256':sha(H/'results_referee.json')},sort_keys=True))
