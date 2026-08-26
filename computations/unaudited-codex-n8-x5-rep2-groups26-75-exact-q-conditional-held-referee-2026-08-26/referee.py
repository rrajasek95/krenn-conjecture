#!/usr/bin/env python3
from __future__ import annotations
import ast,copy,hashlib,importlib.util,json
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
PKG=ROOT/'computations/unaudited-codex-n8-x5-rep2-groups26-75-exact-q-conditional-held-2026-08-26'
BASE=ROOT/'computations/unaudited-codex-n8-x5-rep2-first25-exact-q-held-2026-08-25'
DESIGN=ROOT/'computations/unaudited-codex-n8-x5-rep2-corrected-guard-minor-contraction-design-2026-08-25'

def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  while chunk:=f.read(1<<20):h.update(chunk)
 return h.hexdigest()
def replay(manifest):
 count=0
 for line in manifest.read_text().splitlines():
  if not line.strip():continue
  digest,name=line.split(None,1);p=Path(name.strip());p=p if p.is_absolute() else (manifest.parent/p).resolve()
  assert p.is_file() and sha(p)==digest,(p,sha(p),digest);count+=1
 return count

pins={
 PKG/'MANIFEST.sha256':'07c356ff169a8586add38bb8cb808977570a1ad83f001fb4918c5da163ef0f38',
 PKG/'source_ledger.json':'0a9ad8dfb140d8e601c88429c13945d1182ac6dffe2c7dcc022a1b353a1005e7',
 PKG/'normalize_dependency.py':'c4625a17f0368e94a1debed8c76126284f9a66e4dc0de929025046f2ca15e150',
 PKG/'future_dependency.json':'df9ec9aba49241c0d17853c9081917e48b134e16b51f382fee85f4f5f550651c',
 PKG/'results_hostile_tests.json':'30b7c525af0f086a3153dd49400d38fb2adfdf823649126ec6cbfa9774855b18',
 PKG/'run_groups26_75.py':'2cdcfa471e0432a734b9089a14f4f8443ea609b3517a6cd7f4bd853133b568b9',
 BASE/'MANIFEST.sha256':'d694841e71b7982f50449b033ae21fb5798bd0ae765f75a9d655909a8c61022c',
 BASE/'canonical_census.json':'5ee661f3fdfd0e35e75d92d6efe7700b83011049e1d74a712ba8918681f86c8a',
 DESIGN/'MANIFEST.sha256':'ab18ee8446de2a163f1e6c14dfc60d2cd4c6465f5464206e10ecb35c2d2facf2',
 DESIGN/'generate_design.py':'ca23dbcb4179753393b7b0b3cd81d5c73d2c1bd26da559b00ca5136524aa83dc',
}
for path,want in pins.items():assert sha(path)==want,(path,sha(path),want)
manifest_counts={'package':replay(PKG/'MANIFEST.sha256'),'base':replay(BASE/'MANIFEST.sha256'),'design':replay(DESIGN/'MANIFEST.sha256')}

spec=importlib.util.spec_from_file_location('rep2_conditional_referee_design',DESIGN/'generate_design.py');assert spec and spec.loader
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);engine=module.load_engine();module.configure_engine(engine)
census=json.loads((BASE/'canonical_census.json').read_text());assert census['counts']=={'raw':972,'canonical_groups':162,'members_each':6,'y_groups':81,'z_groups':81}
assert [x['group_id'] for x in census['groups']]==list(range(162))
ep='''ideal G=slimgb(I);\nprint("GROEBNER_SIZE="+string(size(G)));\npoly remainder=reduce(1,G);\nprint("UNIT_REMAINDER="+string(remainder));\nif (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\nquit;\n'''
ledger=json.loads((PKG/'source_ledger.json').read_text());lanes=ledger['lanes'];selected=list(range(26,76))
assert ledger['selection']=={'required_closed_union':list(range(26)),'rule':'exact canonical group IDs 26..75 in strict ascending order','selected_group_ids':selected}
assert [x['group_id'] for x in lanes]==selected and [x['ordinal'] for x in lanes]==list(range(1,51))
total=0
for lane in lanes:
 rec=census['groups'][lane['group_id']];base=module.build_program(engine,tuple(rec['canonical_chart']));assert base.endswith('quit;\n')
 q=base[:-len('quit;\n')]+ep;data=q.encode();digest=hashlib.sha256(data).hexdigest();source=PKG/lane['source_path']
 assert lane['canonical_chart']==rec['canonical_chart'] and lane['family']==rec['family']
 assert digest==rec['exact_Q_source_sha256']==lane['source_sha256']==sha(source)
 assert len(data)==rec['exact_Q_source_bytes']==lane['source_bytes']==source.stat().st_size
 assert source.read_bytes()==data and lane['variables']==91 and lane['generators']==6577;total+=len(data)

dep=json.loads((PKG/'future_dependency.json').read_text());assert dep['status']=='UNSATISFIED_NULL_HASH_PAIR' and dep['satisfied'] is False
assert dep['manifest_sha256'] is dep['result_sha256'] is None
future_manifest=ROOT/dep['required']['manifest_path'];future_result=ROOT/dep['required']['result_path']
assert not future_manifest.exists() and not future_result.exists()
assert dep['required']['groups_closed']==list(range(1,26)) and dep['required']['closed_union']==list(range(26))
speca=importlib.util.spec_from_file_location('rep2_dependency_adapter',PKG/'normalize_dependency.py');assert speca and speca.loader
adapter=importlib.util.module_from_spec(speca);speca.loader.exec_module(adapter)
good={'schema':dep['required']['result_schema'],'status':dep['required']['result_status'],'groups_closed':list(range(1,26))}
def rejected(contract,result,mh='a'*64,rh='b'*64):
 try:adapter.validate_payload(contract,result,mh,rh)
 except (AssertionError,KeyError,TypeError):return True
 return False
hostiles={}
def reject(name,cm=None,rm=None,mh='a'*64,rh='b'*64):
 c,r=copy.deepcopy(dep),copy.deepcopy(good)
 if cm:cm(c)
 if rm:rm(r)
 hostiles[name]=rejected(c,r,mh,rh)
reject('null_treated_satisfied',lambda c:c.__setitem__('satisfied',True));reject('future_hash_injected',lambda c:c.__setitem__('manifest_sha256','0'*64));reject('wrong_schema',rm=lambda r:r.__setitem__('schema','wrong'));reject('wrong_status',rm=lambda r:r.__setitem__('status','wrong'));reject('missing_group',rm=lambda r:r['groups_closed'].pop());reject('duplicate_group',rm=lambda r:r['groups_closed'].__setitem__(24,24));reject('extra_group',rm=lambda r:r['groups_closed'].append(26));reject('reordered_groups',rm=lambda r:r['groups_closed'].reverse());reject('baseline_zero_removed',lambda c:c['required']['closed_union'].pop(0));reject('closed_union_extra',lambda c:c['required']['closed_union'].append(26));reject('bad_manifest_hash',mh='a'*63);reject('bad_result_hash',rh='z'*64)
packaged=json.loads((PKG/'results_hostile_tests.json').read_text());assert len(hostiles)==12 and all(hostiles.values()) and packaged['tests']==hostiles and packaged['status']=='PASS_12_HOSTILES_FUTURE_ABSENT' and packaged['solver_runs']==0

runner=(PKG/'run_groups26_75.py').read_text();ast.parse(runner)
for token in ('SELECTED=tuple(range(26,76))','NATIVE_WALL=240','WRAPPER_WALL=250','RSS_CAP=8*1024**3','proc_listpgrppids','proc_pid_rusage',"assert NORMALIZED.is_file(),'HELD: future PASS_ALL_25 dependency has not been normalized'","dep['closed_union']==list(range(26))",'for lane in lanes:','if not unit:stop=',"'parallel':False","'relaunch':False","exclusive(HERE/'BATCH_ATTEMPT.json'",'atomic(path,record)'):
 assert token in runner,token
assert runner.count('subprocess.Popen(')==1 and 'start_new_session=True' in runner
assert runner.index("assert NORMALIZED.is_file()")<runner.index("exclusive(HERE/'BATCH_ATTEMPT.json'")<runner.index('subprocess.Popen(')
for absent in ('normalized_dependency.json','independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):
 assert not (PKG/absent).exists(),absent
assert not list(PKG.rglob('*.tmp'))

out={'schema':'KRENN_X5_REP2_GROUPS26_75_CONDITIONAL_HELD_REFEREE_V1','status':'PASS_CONDITIONAL_HELD_GROUPS26_75_BLOCKED_ZERO_RUNS','producer_manifest_sha256':pins[PKG/'MANIFEST.sha256'],'source_ledger_sha256':pins[PKG/'source_ledger.json'],'authoritative_census_sha256':pins[BASE/'canonical_census.json'],'adapter_sha256':pins[PKG/'normalize_dependency.py'],'future_dependency_sha256':pins[PKG/'future_dependency.json'],'runner_sha256':pins[PKG/'run_groups26_75.py'],'baseline_closed_group':[0],'required_future_groups':list(range(1,26)),'derived_union_if_satisfied':list(range(26)),'dependency_satisfied':False,'future_hashes':[None,None],'future_files_present':False,'hostiles_passed':12,'selected_group_ids':selected,'canonical_sources_verified':50,'total_source_bytes':total,'variables_each':91,'generators_each':6577,'limits_each':{'native_wall_seconds':240,'wrapper_wall_seconds':250,'rss_cap_bytes':8*1024**3},'strict_sequential_stop_first':True,'manifest_counts':manifest_counts,'scope':{'held_approval_only':True,'launch_authorized':False,'solver_runs':0,'mathematical_coverage':False,'rep2_closed':False}}
approval={'schema':'KRENN_X5_REP2_GROUPS26_75_CONDITIONAL_HELD_APPROVAL_NOT_EXECUTOR_ACCEPTANCE_V1','status':'PASS_HELD_ONLY_BLOCKED_ON_EXACT_GROUPS1_25_TERMINAL_BINDING','producer_manifest_sha256':pins[PKG/'MANIFEST.sha256'],'dependency_spec_sha256':pins[PKG/'future_dependency.json'],'future_terminal_manifest_sha256':None,'future_terminal_result_sha256':None,'selected_group_ids':selected,'launch_authorized':False,'solver_runs':0}
(HERE/'results_referee.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');(HERE/'HELD_APPROVAL.json').write_text(json.dumps(approval,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':out['status'],'sources':50,'groups':[26,75],'runs':0,'result_sha256':sha(HERE/'results_referee.json')},sort_keys=True))
