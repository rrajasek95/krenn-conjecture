#!/usr/bin/env python3
from __future__ import annotations
import ast,copy,hashlib,importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];PKG=ROOT/'computations/unaudited-codex-n8-x5-rep4-groups76-125-exact-q-conditional-held-2026-08-26';BASE=ROOT/'computations/unaudited-codex-n8-x5-rep4-first25-exact-q-held-2026-08-26';DESIGN=ROOT/'computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25'
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
pins={PKG/'MANIFEST.sha256':'0d2d7cfce0ed9e862b573e4fdc5791b3384c7bd21fbd6e9ff9e663c79f387115',PKG/'source_ledger.json':'b311e566fab04932f0c49a285ac3190ae4ac7a02f102799a9a2c6b34a949e4bb',PKG/'future_dependencies.json':'02e042533a68fb7a9a08d230caa7de915c3176e4d7e54b8f68a9704da7e6916e',PKG/'normalize_dependencies.py':'5afc90779b09c31950e30cb7f11cb198d9c37f5d655e6926fcfad2980561733c',PKG/'results_hostile_tests.json':'c2b63c220e87435c2c501827674cdc1dec736809f49a5b664721fa4c15664de7',PKG/'run_groups76_125.py':'3e5a744b6017dc0ba4a4d9789039bb4697d20fd1b42332195dc015cfd1e91abd',BASE/'MANIFEST.sha256':'d6c098fb885ad9faac566b6f01a9e94f01aa6a8b4a61562ec4fa14f66b44a029',BASE/'canonical_census.json':'12773aacfd9fa702ce4202a5da64c356d0451be8b904ebcf9848bcbf99913261',DESIGN/'MANIFEST.sha256':'7f47c0567580aba565925b95860bace46ebaf5703aace4ec8aa100f48ec33e02',DESIGN/'generate_design.py':'b83218b25635efe8c46ff2faf9e2028921408d884be7fb2e4d8541ccdf9c847a'}
for path,want in pins.items():assert sha(path)==want,(path,sha(path),want)
manifest_counts={'package':replay(PKG/'MANIFEST.sha256'),'base':replay(BASE/'MANIFEST.sha256'),'design':replay(DESIGN/'MANIFEST.sha256')}
spec=importlib.util.spec_from_file_location('rep4_76_125_referee_design',DESIGN/'generate_design.py');assert spec and spec.loader;module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
census=json.loads((BASE/'canonical_census.json').read_text());assert census['counts']=={'raw':972,'canonical_groups':162,'members_each':6,'y_groups':81,'z_groups':81} and [x['group_id'] for x in census['groups']]==list(range(162))
ep='''ideal G=slimgb(I);\nprint("GROEBNER_SIZE="+string(size(G)));\npoly remainder=reduce(1,G);\nprint("UNIT_REMAINDER="+string(remainder));\nif (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }\nquit;\n'''
ledger=json.loads((PKG/'source_ledger.json').read_text());lanes=ledger['lanes'];selected=list(range(76,126));assert ledger['selection']['required_closed_union']==list(range(76)) and ledger['selection']['selected_group_ids']==selected and [x['group_id'] for x in lanes]==selected and [x['ordinal'] for x in lanes]==list(range(1,51))
total=0
for lane in lanes:
 rec=census['groups'][lane['group_id']];base=module.build_program(tuple(rec['canonical_chart']));assert base.endswith('quit;\n');q=base[:-len('quit;\n')]+ep;data=q.encode();digest=hashlib.sha256(data).hexdigest();source=PKG/lane['source_path']
 assert lane['canonical_chart']==rec['canonical_chart'] and lane['family']==rec['family'] and digest==rec['exact_Q_source_sha256']==lane['source_sha256']==sha(source) and source.read_bytes()==data
 assert len(data)==rec['exact_Q_source_bytes']==lane['source_bytes']==source.stat().st_size and lane['variables']==91 and lane['generators']==6577;total+=len(data)
contract=json.loads((PKG/'future_dependencies.json').read_text());assert contract['status']=='UNSATISFIED_BOTH_NULL_HASH_PAIRS' and contract['satisfied'] is False and contract['required_closed_union']==list(range(76)) and len(contract['dependencies'])==2 and all(not d['satisfied'] and d['manifest_sha256'] is d['result_sha256'] is None for d in contract['dependencies'])
future_paths=[]
for dep in contract['dependencies']:
 manifest=ROOT/dep['manifest_path'];result=ROOT/dep['result_path'];assert not manifest.exists() and not result.exists();future_paths.extend((str(manifest),str(result)))
speca=importlib.util.spec_from_file_location('rep4_76_125_adapter',PKG/'normalize_dependencies.py');assert speca and speca.loader;adapter=importlib.util.module_from_spec(speca);speca.loader.exec_module(adapter)
first={'schema':contract['dependencies'][0]['result_schema'],'status':contract['dependencies'][0]['result_status'],'groups_closed':list(range(1,26))};middle={'schema':contract['dependencies'][1]['result_schema'],'status':contract['dependencies'][1]['result_status'],'groups_closed':list(range(26,76))};hostiles={}
def reject(name,cm=None,fm=None,mm=None,mhs=None,rhs=None):
 c,f,m=copy.deepcopy(contract),copy.deepcopy(first),copy.deepcopy(middle)
 if cm:cm(c)
 if fm:fm(f)
 if mm:mm(m)
 try:adapter.validate_payload(c,f,m,mhs or ['a'*64,'b'*64],rhs or ['c'*64,'d'*64])
 except (AssertionError,KeyError,TypeError):hostiles[name]=True
 else:hostiles[name]=False
reject('null_treated_satisfied',lambda c:c.__setitem__('satisfied',True));reject('future_hash_injected',lambda c:c['dependencies'][0].__setitem__('manifest_sha256','0'*64));reject('dependency_order_swapped',lambda c:c['dependencies'].reverse());reject('first_wrong_schema',fm=lambda x:x.__setitem__('schema','wrong'));reject('first_missing',fm=lambda x:x['groups_closed'].pop());reject('first_duplicate',fm=lambda x:x['groups_closed'].__setitem__(24,24));reject('middle_wrong_status',mm=lambda x:x.__setitem__('status','wrong'));reject('middle_missing',mm=lambda x:x['groups_closed'].pop());reject('middle_duplicate',mm=lambda x:x['groups_closed'].__setitem__(49,74));reject('cross_overlap',mm=lambda x:x['groups_closed'].__setitem__(0,25));reject('union_extra',lambda c:c['required_closed_union'].append(76));reject('bad_hash_pair',mhs=['a'*63,'b'*64],rhs=['c'*64,'z'*64])
packaged=json.loads((PKG/'results_hostile_tests.json').read_text());assert len(hostiles)==12 and all(hostiles.values()) and packaged['tests']==hostiles and packaged['status']=='PASS_12_HOSTILES_BOTH_FUTURES_ABSENT' and packaged['solver_runs']==0
runner=(PKG/'run_groups76_125.py').read_text();ast.parse(runner)
for token in ('SELECTED=tuple(range(76,126))','NATIVE_WALL=240','WRAPPER_WALL=250','RSS_CAP=8*1024**3','proc_listpgrppids','proc_pid_rusage',"assert NORMALIZED.is_file(),'HELD: future PASS groups1..25 and26..75 dependencies have not been normalized'","for rel,want in zip(dep['dependency_manifest_paths'],dep['dependency_manifest_sha256']):assert sha(ROOT/rel)==want","for rel,want in zip(dep['dependency_result_paths'],dep['dependency_result_sha256']):assert sha(ROOT/rel)==want",'for lane in lanes:','if not unit:stop=',"'parallel':False","'relaunch':False","exclusive(HERE/'BATCH_ATTEMPT.json'",'atomic(path,record)'):assert token in runner,token
assert runner.count('subprocess.Popen(')==1 and 'start_new_session=True' in runner and runner.index("for rel,want in zip(dep['dependency_result_paths']")<runner.index("exclusive(HERE/'BATCH_ATTEMPT.json'")<runner.index('subprocess.Popen(')
for absent in ('normalized_dependencies.json','independent_referee_acceptance.json','launch_clearance.json','BATCH_ATTEMPT.json','batch_result.json','results'):assert not (PKG/absent).exists(),absent
assert not list(PKG.rglob('*.tmp'))
out={'schema':'KRENN_X5_REP4_GROUPS76_125_CONDITIONAL_HELD_REFEREE_V1','status':'PASS_CONDITIONAL_HELD_GROUPS76_125_BLOCKED_ZERO_RUNS','producer_manifest_sha256':pins[PKG/'MANIFEST.sha256'],'source_ledger_sha256':pins[PKG/'source_ledger.json'],'authoritative_census_sha256':pins[BASE/'canonical_census.json'],'adapter_sha256':pins[PKG/'normalize_dependencies.py'],'future_dependencies_sha256':pins[PKG/'future_dependencies.json'],'runner_sha256':pins[PKG/'run_groups76_125.py'],'required_future_groups':[list(range(1,26)),list(range(26,76))],'derived_union_if_satisfied':list(range(76)),'dependency_satisfied':False,'future_hashes':[None,None,None,None],'future_files_present':False,'runner_reopens_and_rehashes_all_dependency_paths':True,'hostiles_passed':12,'selected_group_ids':selected,'canonical_sources_verified':50,'total_source_bytes':total,'variables_each':91,'generators_each':6577,'limits_each':{'native_wall_seconds':240,'wrapper_wall_seconds':250,'rss_cap_bytes':8*1024**3},'strict_sequential_stop_first':True,'manifest_counts':manifest_counts,'scope':{'held_approval_only':True,'launch_authorized':False,'solver_runs':0,'mathematical_coverage':False,'rep4_closed':False}}
approval={'schema':'KRENN_X5_REP4_GROUPS76_125_CONDITIONAL_HELD_APPROVAL_NOT_EXECUTOR_ACCEPTANCE_V1','status':'PASS_HELD_ONLY_BLOCKED_ON_BOTH_EXACT_TERMINAL_BINDINGS','producer_manifest_sha256':pins[PKG/'MANIFEST.sha256'],'dependency_spec_sha256':pins[PKG/'future_dependencies.json'],'future_terminal_hashes':[None,None,None,None],'selected_group_ids':selected,'launch_authorized':False,'solver_runs':0}
(HERE/'results_referee.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');(HERE/'HELD_APPROVAL.json').write_text(json.dumps(approval,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'sources':50,'groups':[76,125],'runs':0,'result_sha256':sha(HERE/'results_referee.json')},sort_keys=True))
