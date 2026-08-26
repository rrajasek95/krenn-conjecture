#!/usr/bin/env python3
from __future__ import annotations
import ast,copy,hashlib,importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
PKG=ROOT/'computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-conditional-held-2026-08-26';BASE=ROOT/'computations/unaudited-codex-n8-x5-rep4-first25-exact-q-held-2026-08-26';DESIGN=ROOT/'computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25'
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  while chunk:=f.read(1<<20):h.update(chunk)
 return h.hexdigest()
def replay(manifest):
 count=0
 for line in manifest.read_text().splitlines():
  if not line.strip():continue
  digest,name=line.split(None,1);path=Path(name.strip());path=path if path.is_absolute() else (manifest.parent/path).resolve();assert path.is_file() and sha(path)==digest,(path,sha(path),digest);count+=1
 return count
pins={PKG/'MANIFEST.sha256':'c79cf415a4dc6327dcaefa7f9f002a1f1f2b5af5afef2a80bab16d8cfc9ccbb6',PKG/'source_ledger.json':'48e9fb104efd69a1267f5ff1015a2142af33d481a430bebab2f794442afa8341',PKG/'normalize_dependency.py':'3fca6f290c810bbf9e15d524de79510ab7c7bad11069890e85d12ab8843895a9',PKG/'future_dependency.json':'14914c42a19896d680a8cab0c154795ea15b7e8fae0d52b0a0b58e26c8f40a5d',PKG/'results_hostile_tests.json':'c38a0f2ef014e7c54f24ccbd1e4f7e61fe3b4006df981054782e01b76d34f134',PKG/'run_groups26_75.py':'b29a78c495517ddb9c43147c5c9ec1091c921a63e4a8285cf7549d0926d721aa',BASE/'MANIFEST.sha256':'d6c098fb885ad9faac566b6f01a9e94f01aa6a8b4a61562ec4fa14f66b44a029',BASE/'canonical_census.json':'12773aacfd9fa702ce4202a5da64c356d0451be8b904ebcf9848bcbf99913261',DESIGN/'MANIFEST.sha256':'7f47c0567580aba565925b95860bace46ebaf5703aace4ec8aa100f48ec33e02',DESIGN/'generate_design.py':'b83218b25635efe8c46ff2faf9e2028921408d884be7fb2e4d8541ccdf9c847a'}
for path,want in pins.items():assert sha(path)==want,(path,sha(path),want)
manifest_counts={'package':replay(PKG/'MANIFEST.sha256'),'base':replay(BASE/'MANIFEST.sha256'),'design':replay(DESIGN/'MANIFEST.sha256')}
spec=importlib.util.spec_from_file_location('rep4_conditional_referee_design',DESIGN/'generate_design.py');assert spec and spec.loader;module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
census=json.loads((BASE/'canonical_census.json').read_text());assert census['counts']=={'raw':972,'canonical_groups':162,'members_each':6,'y_groups':81,'z_groups':81} and [x['group_id'] for x in census['groups']]==list(range(162))
ep='''ideal G=slimgb(I);\nprint("GROEBNER_SIZE="+string(size(G)));\npoly remainder=reduce(1,G);\nprint("UNIT_REMAINDER="+string(remainder));\nif (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\nquit;\n'''
ledger=json.loads((PKG/'source_ledger.json').read_text());lanes=ledger['lanes'];selected=list(range(26,76));assert ledger['selection']=={'required_closed_union':list(range(26)),'rule':'exact canonical group IDs 26..75 in strict ascending order','selected_group_ids':selected} and [x['group_id'] for x in lanes]==selected and [x['ordinal'] for x in lanes]==list(range(1,51))
total=0
for lane in lanes:
 rec=census['groups'][lane['group_id']];base=module.build_program(tuple(rec['canonical_chart']));assert base.endswith('quit;\n');q=base[:-len('quit;\n')]+ep;data=q.encode();digest=hashlib.sha256(data).hexdigest();source=PKG/lane['source_path']
 assert lane['canonical_chart']==rec['canonical_chart'] and lane['family']==rec['family'] and digest==rec['exact_Q_source_sha256']==lane['source_sha256']==sha(source) and source.read_bytes()==data
 assert len(data)==rec['exact_Q_source_bytes']==lane['source_bytes']==source.stat().st_size and lane['variables']==91 and lane['generators']==6577;total+=len(data)
dep=json.loads((PKG/'future_dependency.json').read_text());assert dep['status']=='UNSATISFIED_NULL_HASH_PAIR' and dep['satisfied'] is False and dep['manifest_sha256'] is dep['result_sha256'] is None and dep['required']['groups_closed']==list(range(1,26)) and dep['required']['closed_union']==list(range(26))
future_manifest=ROOT/dep['required']['manifest_path'];future_result=ROOT/dep['required']['result_path'];assert not future_manifest.exists() and not future_result.exists()
speca=importlib.util.spec_from_file_location('rep4_dependency_adapter',PKG/'normalize_dependency.py');assert speca and speca.loader;adapter=importlib.util.module_from_spec(speca);speca.loader.exec_module(adapter)
good={'schema':dep['required']['result_schema'],'status':dep['required']['result_status'],'groups_closed':list(range(1,26))};hostiles={}
def reject(name,cm=None,rm=None,mh='a'*64,rh='b'*64):
 c,r=copy.deepcopy(dep),copy.deepcopy(good)
 if cm:cm(c)
 if rm:rm(r)
 try:adapter.validate_payload(c,r,mh,rh)
 except (AssertionError,KeyError,TypeError):hostiles[name]=True
 else:hostiles[name]=False
reject('null_treated_satisfied',lambda c:c.__setitem__('satisfied',True));reject('future_hash_injected',lambda c:c.__setitem__('manifest_sha256','0'*64));reject('wrong_schema',rm=lambda r:r.__setitem__('schema','wrong'));reject('wrong_status',rm=lambda r:r.__setitem__('status','wrong'));reject('missing_group',rm=lambda r:r['groups_closed'].pop());reject('duplicate_group',rm=lambda r:r['groups_closed'].__setitem__(24,24));reject('extra_group',rm=lambda r:r['groups_closed'].append(26));reject('reordered_groups',rm=lambda r:r['groups_closed'].reverse());reject('baseline_removed',lambda c:c['required']['closed_union'].pop(0));reject('union_extra',lambda c:c['required']['closed_union'].append(26));reject('bad_manifest_hash',mh='a'*63);reject('bad_result_hash',rh='z'*64)
packaged=json.loads((PKG/'results_hostile_tests.json').read_text());assert len(hostiles)==12 and all(hostiles.values()) and packaged['tests']==hostiles and packaged['status']=='PASS_12_HOSTILES_FUTURE_ABSENT' and packaged['solver_runs']==0
runner=(PKG/'run_groups26_75.py').read_text();ast.parse(runner)
for token in ('SELECTED=tuple(range(26,76))','NATIVE_WALL=240','WRAPPER_WALL=250','RSS_CAP=8*1024**3','proc_listpgrppids','proc_pid_rusage',"assert NORMALIZED.is_file(),'HELD: future PASS_ALL_25 dependency has not been normalized'","dep['closed_union']==list(range(26))",'for lane in lanes:','if not unit:stop=',"'parallel':False","'relaunch':False","exclusive(HERE/'BATCH_ATTEMPT.json'",'atomic(path,record)'):assert token in runner,token
assert runner.count('subprocess.Popen(')==1 and 'start_new_session=True' in runner and runner.index("assert NORMALIZED.is_file()")<runner.index("exclusive(HERE/'BATCH_ATTEMPT.json'")<runner.index('subprocess.Popen(')
for absent in ('normalized_dependency.json','independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):assert not (PKG/absent).exists(),absent
assert not list(PKG.rglob('*.tmp'))
out={'schema':'KRENN_X5_REP4_GROUPS26_75_CONDITIONAL_HELD_REFEREE_V1','status':'PASS_CONDITIONAL_HELD_GROUPS26_75_BLOCKED_ZERO_RUNS','producer_manifest_sha256':pins[PKG/'MANIFEST.sha256'],'source_ledger_sha256':pins[PKG/'source_ledger.json'],'authoritative_census_sha256':pins[BASE/'canonical_census.json'],'adapter_sha256':pins[PKG/'normalize_dependency.py'],'future_dependency_sha256':pins[PKG/'future_dependency.json'],'runner_sha256':pins[PKG/'run_groups26_75.py'],'baseline_closed_group':[0],'required_future_groups':list(range(1,26)),'derived_union_if_satisfied':list(range(26)),'dependency_satisfied':False,'future_hashes':[None,None],'future_files_present':False,'hostiles_passed':12,'selected_group_ids':selected,'canonical_sources_verified':50,'total_source_bytes':total,'variables_each':91,'generators_each':6577,'limits_each':{'native_wall_seconds':240,'wrapper_wall_seconds':250,'rss_cap_bytes':8*1024**3},'strict_sequential_stop_first':True,'manifest_counts':manifest_counts,'scope':{'held_approval_only':True,'launch_authorized':False,'solver_runs':0,'mathematical_coverage':False,'rep4_closed':False}}
approval={'schema':'KRENN_X5_REP4_GROUPS26_75_CONDITIONAL_HELD_APPROVAL_NOT_EXECUTOR_ACCEPTANCE_V1','status':'PASS_HELD_ONLY_BLOCKED_ON_EXACT_GROUPS1_25_TERMINAL_BINDING','producer_manifest_sha256':pins[PKG/'MANIFEST.sha256'],'dependency_spec_sha256':pins[PKG/'future_dependency.json'],'future_terminal_manifest_sha256':None,'future_terminal_result_sha256':None,'selected_group_ids':selected,'launch_authorized':False,'solver_runs':0}
(HERE/'results_referee.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');(HERE/'HELD_APPROVAL.json').write_text(json.dumps(approval,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'sources':50,'groups':[26,75],'runs':0,'result_sha256':sha(HERE/'results_referee.json')},sort_keys=True))
