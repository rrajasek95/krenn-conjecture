#!/usr/bin/env python3
"""Independent zero-run referee for the rep2 group16 closed-t modular lane."""
from __future__ import annotations
import ast,hashlib,json,re
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[1]
P=ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-closed-t-modular-held-2026-08-26'
Q=ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-67-timeout-reduction-design-2026-08-26/rep2_group016_67_Vt0_Vt1_Vt2_Q.sing'
DEPS={
 'timeout':(ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-combined-smallest-modular-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256','ef85c2ee938da004226540d76e609feb9fae4261808f6ac755e9bfd8b268c73c'),
 'design':(ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-67-timeout-reduction-design-2026-08-26/MANIFEST.sha256','3d4d6fbc89f5adcc45032c37b1b038780761f479313575c59e4e8bd760da75fd'),
 'referee':(ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-67-timeout-reduction-referee-2026-08-26/MANIFEST.sha256','e41de381875869a6ac206454b57e091b7ed1093f76aad4a9b71ed30929d3b3cd'),
 'torus':(ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-decomposition-design-2026-08-26/MANIFEST.sha256','1492e69373819fda0c50afc4f1366e2d6da90e857c26f73c03c0212ffd879282'),
 'guard':(ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-isomorphism-guard-pivot-design-2026-08-26/MANIFEST.sha256','6a781149041e8808d58a53af77059253fe0a0d4295052bfe34756a0f994a0aee'),
 'comparison':(ROOT/'computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-referee-comparison-2026-08-26/MANIFEST.sha256','1a2dcba289d5f31e39be48c4f98ff44a6b0c6891841fd345df52f06abfd5525a')}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def split_top(s):
 out=[];d=0;start=0
 for i,c in enumerate(s):
  if c=='(':d+=1
  elif c==')':d-=1
  elif c==',' and d==0:out.append(s[start:i]);start=i+1
 out.append(s[start:]);assert d==0;return out
def check_runner(s):
 ast.parse(s)
 required=('NATIVE=240','WRAPPER=255','RSS_CAP=8*1024**3','proc_listallpids','proc_pidpath','proc_listpgrppids','proc_pid_rusage','start_new_session=True','grss(process.pid)','os.killpg','os.O_EXCL','os.replace(t,path)',"exclusive(H/'ATTEMPT.json'",'prior_timeout_reused\':False','other_chart_launched\':False','automatic_relaunch\':False')
 assert all(x in s for x in required)
 assert 'shell=True' not in s and "subprocess.run(['ps'" not in s
def main():
 assert sha(P/'MANIFEST.sha256')=='eefb9e1045f63f945fa62cc83119f171128575eb29d5a1d41b1aabf2e6a374c2'
 assert sha(Q)=='43beb317cb0bc59b24f1d4c5613ef6baccd7ec064651e004c1f8eb4657d538fc'
 for _,(path,digest) in DEPS.items():assert sha(path)==digest
 statuses={
  'timeout':json.loads((DEPS['timeout'][0].parent/'results_referee.json').read_text())['status'],
  'referee':json.loads((DEPS['referee'][0].parent/'results_referee.json').read_text())['status'],
  'torus':json.loads((DEPS['torus'][0].parent/'results_design.json').read_text())['status'],
  'guard':json.loads((DEPS['guard'][0].parent/'results_group16_design.json').read_text())['status'],
  'comparison':json.loads((DEPS['comparison'][0].parent/'results_referee_comparison.json').read_text())['status']}
 assert statuses=={'timeout':'PASS_FAIL_CLOSED_NATIVE_WALL_ZERO_COVERAGE','referee':'PASS_EXACT_FOUR_STRATUM_REDUCTION_REFEREE_ZERO_SOLVES','torus':'PASS_EXACT_19_STRATUM_DESIGN_ZERO_SOLVES','guard':'PASS_NO_PREFIX_TRANSPORT_STRICT_88_6574_THREE_CHART_QUOTIENT_ZERO_SOLVES','comparison':'PASS_TORUS_19_EXACT_AND_SOUND_57_INTERSECTION_ZERO_SOLVES'}
 modular=P/'rep2_group016_62_Vt0_Vt1_Vt2_p32003.sing';assert sha(modular)=='d7e57a3d43fb1280381660be2fea9c966eb086bd2aced3189b0f599030f5822b'
 q=Q.read_bytes();p=modular.read_bytes();strong=b'''ideal G=slimgb(I);
print("GROEBNER_SIZE="+string(size(G)));
poly remainder=reduce(1,G);
print("UNIT_REMAINDER="+string(remainder));
if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }
quit;
''';expected=q.replace(b'ring r=0,(',b'ring r=32003,(',1)[:-len(b'quit;\n')]+strong;assert p==expected
 text=q.decode();variables=text.split('ring r=0,(',1)[1].split('),dp;',1)[0].split(',');gens=split_top(text.split('ideal I=',1)[1].split(';\n',1)[0]);assert len(variables)==62 and len(gens)==6568 and len(set(gens))==6568
 assert all(x not in variables for x in ('t0','t1','t2','a57_11','a57_21'))
 runner=P/'run_one_lane.py';assert sha(runner)=='a617b032eae5ecdb3cf41660f43fb900891e86240a97ffe4f25417d56a2de624';r=runner.read_text();check_runner(r)
 hostiles=[]
 for name,m in [('wall',r.replace('NATIVE=240','NATIVE=241',1)),('rss',r.replace('RSS_CAP=8*1024**3','RSS_CAP=9*1024**3',1)),('observer',r.replace('grss(process.pid)','(0,0)',1)),('atomic',r.replace('os.replace(t,path)','path.write_text(t.read_text())',1))]:
  rejected=False
  try:check_runner(m)
  except AssertionError:rejected=True
  assert rejected;hostiles.append({'name':name,'rejected':True})
 held=json.loads((P/'held_pilot.json').read_text());assert held['status']=='HELD_ZERO_RUN_PENDING_INDEPENDENT_AUDIT_AND_FRESH_CLEARANCE' and held['scope']['attempts']==held['scope']['solver_runs']==held['scope']['results']==0 and held['scope']['prior_timeout_reused'] is False
 absent=('independent_referee_acceptance.json','launch_clearance.json','ATTEMPT.json','result.json','result.json.tmp','stdout.log','stderr.log','watchdog.json','RUN_EXCLUSIVE.lock');assert all(not (P/x).exists() for x in absent) and not list(P.glob('*.tmp')) and not list(P.rglob('__pycache__'))
 for n in ('independent_referee_acceptance.schema.json','launch_clearance.schema.json'):
  s=json.loads((P/n).read_text());assert s['additionalProperties'] is False and set(s['required'])==set(s['properties'])
 result={'schema':'KRENN_X5_REP2_GROUP16_CLOSED_T_MODULAR_HELD_REFEREE_V1','status':'PASS_APPROVED_HELD_ZERO_RUN','held_manifest_sha256':sha(P/'MANIFEST.sha256'),'exact_Q_sha256':sha(Q),'modular_source_sha256':sha(modular),'variables':62,'generators':6568,'chart':'V(A67,A12,t0,t1,t2) intersect D(b0)','runner_sha256':sha(runner),'native_wall_seconds':240,'wrapper_wall_seconds':255,'rss_cap_bytes':8589934592,'direct_libproc_group_rss':True,'atomic_result':True,'dependency_manifests':{k:v[1] for k,v in DEPS.items()},'dependency_statuses':statuses,'hostiles':hostiles,'attempts':0,'solver_runs':0,'mathematical_coverage':False,'group16_closed':False,'rep2_closed':False,'exact_Q_authorized':False,'other_chart_authorized':False,'automatic_relaunch_authorized':False,'approval_scope':'held one-lane F_32003 diagnostic only; fresh acceptance and manager/resource clearance still required'}
 (H/'results_referee.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'])
if __name__=='__main__':main()
