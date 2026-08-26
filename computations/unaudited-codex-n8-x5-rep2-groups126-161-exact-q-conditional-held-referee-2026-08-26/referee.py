#!/usr/bin/env python3
from __future__ import annotations
import ast,copy,hashlib,importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];PKG=ROOT/'computations/unaudited-codex-n8-x5-rep2-groups126-161-exact-q-conditional-held-2026-08-26';BASE=ROOT/'computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-2026-08-25';DESIGN=ROOT/'computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25'
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as stream:
  while chunk:=stream.read(1<<20):h.update(chunk)
 return h.hexdigest()
def replay(manifest):
 count=0
 for line in manifest.read_text().splitlines():
  if not line.strip():continue
  digest,name=line.split(None,1);path=Path(name.strip());path=path if path.is_absolute() else (manifest.parent/path).resolve();assert path.is_file() and sha(path)==digest,(path,sha(path),digest);count+=1
 return count
pins={PKG/'MANIFEST.sha256':'83c87103e2414b48d37724ce803c747ee0d2c9a9f757353c172bb17226477147',PKG/'source_ledger.json':'c34b3616bef36d49c63904e676c540208a24dd2057eb176153ad03034db0b8a6',PKG/'future_dependencies.json':'ab8198b3c9745368e51f1f5c481d81b62823f7255d046a80e3d94a7c2cad0e9c',PKG/'dependency_verifier.py':'b784729f817f2986fac597009b65698e62fc8a0ba944447c21b95cd5dde29ff5',PKG/'results_hostile_tests.json':'6feb616a9ad037934eed7dc8b21b44745a3cd1ceeb734424edb85d434466f497',PKG/'run_groups126_161.py':'07281312d1b227c0a629b917485b39c04a976df9bb4fbbf17c2bd92459743407',BASE/'MANIFEST.sha256':'d694841e71b7982f50449b033ae21fb5798bd0ae765f75a9d655909a8c61022c',BASE/'canonical_census.json':'5ee661f3fdfd0e35e75d92d6efe7700b83011049e1d74a712ba8918681f86c8a',DESIGN/'MANIFEST.sha256':'ab18ee8446de2a163f1e6c14dfc60d2cd4c6465f5464206e10ecb35c2d2facf2',DESIGN/'generate_design.py':'ca23dbcb4179753393b7b0b3cd81d5c73d2c1bd26da559b00ca5136524aa83dc'}
for path,want in pins.items():assert sha(path)==want,(path,sha(path),want)
manifest_counts={'package':replay(PKG/'MANIFEST.sha256'),'base':replay(BASE/'MANIFEST.sha256'),'design':replay(DESIGN/'MANIFEST.sha256')}
spec=importlib.util.spec_from_file_location('rep2_final36_referee_design',DESIGN/'generate_design.py');assert spec and spec.loader;module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);engine=module.load_engine();module.configure_engine(engine)
census=json.loads((BASE/'canonical_census.json').read_text());assert census['counts']=={'raw':972,'canonical_groups':162,'members_each':6,'y_groups':81,'z_groups':81} and [x['group_id'] for x in census['groups']]==list(range(162))
ep='''ideal G=slimgb(I);\nprint("GROEBNER_SIZE="+string(size(G)));\npoly remainder=reduce(1,G);\nprint("UNIT_REMAINDER="+string(remainder));\nif (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\nquit;\n'''
ledger=json.loads((PKG/'source_ledger.json').read_text());lanes=ledger['lanes'];selected=list(range(126,162));assert ledger['selection']['required_closed_union']==list(range(126)) and ledger['selection']['selected_group_ids']==selected and [x['group_id'] for x in lanes]==selected and [x['ordinal'] for x in lanes]==list(range(1,37))
total=0
for lane in lanes:
 rec=census['groups'][lane['group_id']];base=module.build_program(engine,tuple(rec['canonical_chart']));assert base.endswith('quit;\n');q=base[:-len('quit;\n')]+ep;data=q.encode();digest=hashlib.sha256(data).hexdigest();source=PKG/lane['source_path']
 assert lane['canonical_chart']==rec['canonical_chart'] and lane['family']==rec['family'] and digest==rec['exact_Q_source_sha256']==lane['source_sha256']==sha(source) and source.read_bytes()==data
 assert len(data)==rec['exact_Q_source_bytes']==lane['source_bytes']==source.stat().st_size and lane['variables']==91 and lane['generators']==6577;total+=len(data)
contract=json.loads((PKG/'future_dependencies.json').read_text());assert contract['status']=='UNSATISFIED_THREE_NULL_HASH_PAIRS' and contract['satisfied'] is False and contract['required_closed_union']==list(range(126)) and [d['name'] for d in contract['dependencies']]==['groups1_25','groups26_75','groups76_125_v2'] and all(not d['satisfied'] and d['manifest_sha256'] is d['result_sha256'] is None for d in contract['dependencies'])
future_paths=[]
for dep in contract['dependencies']:
 manifest=ROOT/dep['manifest_path'];result=ROOT/dep['result_path'];assert not manifest.exists() and not result.exists();future_paths.extend((str(manifest),str(result)))
specv=importlib.util.spec_from_file_location('rep2_final36_dependency_verifier',PKG/'dependency_verifier.py');assert specv and specv.loader;verifier=importlib.util.module_from_spec(specv);specv.loader.exec_module(verifier)
good=[{'schema':d['result_schema'],'status':d['result_status'],'groups_closed':list(d['groups_closed'])} for d in contract['dependencies']];hostiles={}
def reject(name,cm=None,rm=None,mhs=None,rhs=None):
 c,r=copy.deepcopy(contract),copy.deepcopy(good)
 if cm:cm(c)
 if rm:rm(r)
 try:verifier.validate_payload(c,r,mhs or ['a'*64,'b'*64,'c'*64],rhs or ['d'*64,'e'*64,'f'*64])
 except (AssertionError,KeyError,TypeError):hostiles[name]=True
 else:hostiles[name]=False
reject('null_treated_satisfied',lambda c:c.__setitem__('satisfied',True));reject('future_hash_injected',lambda c:c['dependencies'][0].__setitem__('manifest_sha256','0'*64));reject('dependency_order_swapped',lambda c:c['dependencies'].reverse());reject('first_wrong_schema',rm=lambda r:r[0].__setitem__('schema','wrong'));reject('first_missing',rm=lambda r:r[0]['groups_closed'].pop());reject('first_duplicate',rm=lambda r:r[0]['groups_closed'].__setitem__(24,24));reject('middle_wrong_status',rm=lambda r:r[1].__setitem__('status','wrong'));reject('middle_missing',rm=lambda r:r[1]['groups_closed'].pop());reject('middle_duplicate',rm=lambda r:r[1]['groups_closed'].__setitem__(49,74));reject('middle_reordered',rm=lambda r:r[1]['groups_closed'].reverse());reject('third_wrong_schema',rm=lambda r:r[2].__setitem__('schema','wrong'));reject('third_wrong_status',rm=lambda r:r[2].__setitem__('status','wrong'));reject('third_missing',rm=lambda r:r[2]['groups_closed'].pop());reject('third_duplicate',rm=lambda r:r[2]['groups_closed'].__setitem__(49,124));reject('third_reordered',rm=lambda r:r[2]['groups_closed'].reverse());reject('cross_first_middle_overlap',rm=lambda r:r[1]['groups_closed'].__setitem__(0,25));reject('cross_middle_third_overlap',rm=lambda r:r[2]['groups_closed'].__setitem__(0,75));reject('union_extra',lambda c:c['required_closed_union'].append(126));reject('bad_manifest_hash',mhs=['a'*63,'b'*64,'c'*64]);reject('bad_result_hash',rhs=['d'*64,'e'*64,'z'*64])
fabricated=verifier.validate_payload(contract,good,['a'*64,'b'*64,'c'*64],['d'*64,'e'*64,'f'*64])
try:verifier.verify_payload(contract,fabricated,ROOT)
except (AssertionError,FileNotFoundError):hostiles['fabricated_or_stale_normalized_all_six_artifacts_absent']=True
else:hostiles['fabricated_or_stale_normalized_all_six_artifacts_absent']=False
packaged=json.loads((PKG/'results_hostile_tests.json').read_text());assert len(hostiles)==21 and all(hostiles.values()) and packaged['tests']==hostiles and packaged['status']=='PASS_21_HOSTILES_ALL_THREE_FUTURES_ABSENT' and packaged['solver_runs']==0
runner=(PKG/'run_groups126_161.py').read_text();ast.parse(runner)
for token in ('SELECTED=tuple(range(126,162))','NATIVE_WALL=240','WRAPPER_WALL=250','RSS_CAP=8*1024**3','proc_listpgrppids','proc_pid_rusage',"assert NORMALIZED.is_file(),'HELD: all three future dependencies have not been normalized'","replay=verify_payload(json.loads(FUTURE.read_text()),dependency,ROOT)","replay['status']=='PASS_REPLAYED_ALL_SIX_DEPENDENCY_ARTIFACTS_EXACT_UNION_0_125'",'for lane in lanes:','if not unit:stop=',"'parallel':False","'relaunch':False","exclusive(HERE/'BATCH_ATTEMPT.json'",'atomic(path,record)'):assert token in runner,token
assert runner.count('subprocess.Popen(')==1 and 'start_new_session=True' in runner and runner.index('replay=verify_payload(')<runner.index("exclusive(HERE/'BATCH_ATTEMPT.json'")<runner.index('subprocess.Popen(')
for absent in ('normalized_dependencies.json','independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):assert not (PKG/absent).exists(),absent
assert not list(PKG.rglob('*.tmp'))
out={'schema':'KRENN_X5_REP2_GROUPS126_161_CONDITIONAL_HELD_REFEREE_V1','status':'PASS_CONDITIONAL_HELD_GROUPS126_161_BLOCKED_ZERO_RUNS','producer_manifest_sha256':pins[PKG/'MANIFEST.sha256'],'source_ledger_sha256':pins[PKG/'source_ledger.json'],'authoritative_census_sha256':pins[BASE/'canonical_census.json'],'dependency_verifier_sha256':pins[PKG/'dependency_verifier.py'],'future_dependencies_sha256':pins[PKG/'future_dependencies.json'],'runner_sha256':pins[PKG/'run_groups126_161.py'],'required_future_groups':[list(range(1,26)),list(range(26,76)),list(range(76,126))],'derived_union_if_satisfied':list(range(126)),'dependency_satisfied':False,'future_hashes':[None]*6,'future_files_present':False,'runner_replays_all_six_terminal_artifacts_before_attempt':True,'hostiles_passed':21,'fabricated_or_stale_normalized_rejected':True,'selected_group_ids':selected,'canonical_sources_verified':36,'total_source_bytes':total,'variables_each':91,'generators_each':6577,'limits_each':{'native_wall_seconds':240,'wrapper_wall_seconds':250,'rss_cap_bytes':8*1024**3},'strict_sequential_stop_first':True,'manifest_counts':manifest_counts,'scope':{'held_approval_only':True,'launch_authorized':False,'solver_runs':0,'mathematical_coverage':False,'rep2_closed':False}}
approval={'schema':'KRENN_X5_REP2_GROUPS126_161_CONDITIONAL_HELD_APPROVAL_NOT_EXECUTOR_ACCEPTANCE_V1','status':'PASS_HELD_ONLY_BLOCKED_ON_ALL_THREE_EXACT_TERMINAL_BINDINGS','producer_manifest_sha256':pins[PKG/'MANIFEST.sha256'],'dependency_spec_sha256':pins[PKG/'future_dependencies.json'],'future_terminal_hashes':[None]*6,'selected_group_ids':selected,'launch_authorized':False,'solver_runs':0}
(HERE/'results_referee.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');(HERE/'HELD_APPROVAL.json').write_text(json.dumps(approval,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'sources':36,'groups':[126,161],'runs':0,'result_sha256':sha(HERE/'results_referee.json')},sort_keys=True))
