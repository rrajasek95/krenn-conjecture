#!/usr/bin/env python3
"""Independent current-state audit of the conditional rep1 all-162 design."""
from __future__ import annotations
import copy,hashlib,itertools,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
DES=ROOT/'computations/unaudited-codex-n8-x5-rep1-all162-terminal-promotion-conditional-design-2026-08-25';QUO=ROOT/'computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-2026-08-25';QREF=ROOT/'computations/unaudited-codex-n8-x5-seven-block-rep1-guard-minor-quotient-referee-2026-08-25';CEN=ROOT/'computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-2026-08-25';CREF=ROOT/'computations/unaudited-codex-n8-x5-rep1-remaining161-canonical-census-referee-2026-08-25';RANK0=ROOT/'computations/unaudited-codex-n8-x5-seven-block-reps1-4-5-low-rank-carrier-2026-08-25';CLOSED37=ROOT/'computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-held-v2-2026-08-25';CLOSED37_REF=ROOT/'computations/unaudited-codex-n8-x5-rep1-next50-exact-q-normalized-held-v2-referee-2026-08-25';CLOSED87=ROOT/'computations/unaudited-codex-n8-x5-rep1-groups38-87-exact-q-terminal-referee-2026-08-25';HELD88=ROOT/'computations/unaudited-codex-n8-x5-rep1-groups88-137-satisfied-dependency-binding-v2-2026-08-26';HELD138=ROOT/'computations/unaudited-codex-n8-x5-rep1-groups138-161-exact-q-conditional-held-referee-2026-08-25'
PINS={DES/'MANIFEST.sha256':'df566e74f8048648605ab54b2ced3a513c6ff107310fca599384c2702df159d4',DES/'results_terminal_promotion_design.json':'5ea7e89aab44a62e8a89d4ebc41bdaeb9826098be420dc1f3ed14ab4b2cba2a2',DES/'future_dependencies.json':'cfaac79b9a04d37e32abd13b1a976af5e6c9b6f559ac3366893626652152769a',DES/'results_hostile_tests.json':'7ab2082d9b89379e052a4071a4c61dfac5457a88e736fbd8fed5da999db4ef25',DES/'terminal_promotion_acceptance.schema.json':'0fd92f7481e5e7f402e1c3e502ce5e1e9fab075cbc47b80d6fa6d2cf1cd0ec20',QUO/'MANIFEST.sha256':'4f367478c0a91257022234f5115979423bc8e889dd81a74cc3c200e25e3f82c1',QUO/'results_design_audit.json':'abe37d5ae4555fc2df64a3778b6d8a84e316613afbed72d61fb820d8f64bdabb',QREF/'FINAL_MANIFEST.sha256':'16226d5f15d9f0d2d419095ec3842a7122ad77b40c1abe83bc9afe1b45b7800c',QREF/'results_referee.json':'904c8143c647a8e36a3d94389923e979bf4d965ff6fc455dc72dbf3ef609d37e',CEN/'MANIFEST.sha256':'6ed49a2e534955569149eaf2fe80b05aa3513507b41fe44575679eef0271fcb1',CEN/'results_canonical_census.json':'5ef1acc6ee2b97e993ae930b4ba420ce5c1c8c9eac16995d3a31b5c7a3eb5161',CREF/'FINAL_MANIFEST.sha256':'f4779fdf166f008ac6ddf98b64a76cae1d1f81cccca1b51ef4b9a9a824b8cd5a',CREF/'results_referee.json':'36ce4421dcf73f816514664000d1889ce85c32cbf11cf38684f8cdb71a934b29',RANK0/'MANIFEST.sha256':'9a3cec1a39422d2c3d7a6b40f6acdec0b04b19b893c0a1fb657c69d3b50bb8fe',RANK0/'results_remaining_reps_low_rank_carrier.json':'359aa45545d85378dd9e945eb82be3adb98922648025fe853f930feac2b5f458',CLOSED37/'normalized_next25_dependency.json':'29467d0587851aa7bba1e3fd97addc56c67a33e3683c019cf7fc8c74ff396b76',CLOSED37_REF/'FINAL_MANIFEST.sha256':'950e504da1e64a4056cce58b0440165f5f8e5be4c159e2431f5010c5e06fbdc2',CLOSED37_REF/'results_referee.json':'1b303cb18146e5cadb4da5bf765fc9c2dd03f6593742652f34f5808691194a87',CLOSED87/'FINAL_MANIFEST.sha256':'e6987baa4abf37de21e0466932f554ab9272da8a775ae89e5e25cfadd7ba17fc',CLOSED87/'results_referee.json':'42e13d3e2103283e80f4f91af4d8433e21dc482435b945b3c252fa13452e7763',HELD88/'FINAL_MANIFEST.sha256':'4294a7fcc432dc7221b28b207332011f4d6ceb668946c50da9f0ae3584129366',HELD88/'results_referee.json':'940b1f491393e94137041e6c3991f7dc4f98275f17e053f131ef65a21df172ea',HELD138/'FINAL_MANIFEST.sha256':'27ef2e78a85a7f9a9fd89576da782c300d3734158212e27e990e42bc7435b414',HELD138/'results_referee.json':'0a95f1d61729180393c58f457abf91239c9665f0c127a4721a896a1211c8291b'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def replay(m):
 n=0
 for line in m.read_text().splitlines():
  if not line.strip():continue
  e,x=line.split(None,1);p=Path(x.strip())
  if not p.is_absolute():
   local=(m.parent/p).resolve();rooted=(ROOT/p).resolve();p=local if local.is_file() else rooted
  assert p.is_file() and sha(p)==e,p;n+=1
 return n
for p,h in PINS.items():assert sha(p)==h,(p,sha(p),h)
counts={'design':replay(DES/'MANIFEST.sha256'),'quotient':replay(QUO/'MANIFEST.sha256'),'quotient_referee':replay(QREF/'FINAL_MANIFEST.sha256'),'census':replay(CEN/'MANIFEST.sha256'),'census_referee':replay(CREF/'FINAL_MANIFEST.sha256'),'closed0_37_referee':replay(CLOSED37_REF/'FINAL_MANIFEST.sha256'),'closed38_87':replay(CLOSED87/'FINAL_MANIFEST.sha256'),'held88_137':replay(HELD88/'FINAL_MANIFEST.sha256'),'held138_161':replay(HELD138/'FINAL_MANIFEST.sha256')}
design=json.loads((DES/'results_terminal_promotion_design.json').read_text());future=json.loads((DES/'future_dependencies.json').read_text());census=json.loads((CEN/'results_canonical_census.json').read_text());cref=json.loads((CREF/'results_referee.json').read_text());qdesign=json.loads((QUO/'results_design_audit.json').read_text());qref=json.loads((QREF/'results_referee.json').read_text())
assert design['status']=='HELD_PROMOTION_THREE_FUTURE_PASS_SEALS_ABSENT' and qdesign['chart_union']=={'all_equal_y_orbits':1,'complete':True,'orbits':162,'raw':972,'y_orbits':81,'z_orbits':81} and qref['status']=='PASS_EXACT_DESIGN_ONLY_NO_CLOSURE'
# Independent S3 orbit regeneration.
def representative(record):
 coordinate,p,q,r,kind,s,a,b=record;out=[]
 for perm in itertools.permutations(range(3)):
  aa,bb=sorted((perm[a],perm[b]));out.append((perm[coordinate],perm[p],perm[q],perm[r],kind,perm[s],aa,bb))
 return min(out)
raw=[]
for coordinate,p,q,r,s in itertools.product(range(3),repeat=5):
 for kind in ('y','z'):
  for other in range(3):
   if other!=q:
    a,b=sorted((q,other));raw.append((coordinate,p,q,r,kind,s,a,b))
groups={}
for record in raw:groups.setdefault(representative(record),[]).append(record)
assert len(raw)==len(set(raw))==972 and len(groups)==162 and set(map(len,groups.values()))=={6}
keys=sorted(groups);records=census['enumeration']['records'];assert [r['group_id'] for r in records]==list(range(162))
for gid,key in enumerate(keys):
 rec=records[gid];assert tuple(rec['canonical_chart'])==key and {tuple(x) for x in rec['raw_members']}==set(groups[key]) and rec['raw_member_count']==6
assert sum(key[4]=='y' for key in keys)==sum(key[4]=='z' for key in keys)==81 and sum(x[4]=='y' for x in raw)==sum(x[4]=='z' for x in raw)==486
assert cref['status']=='PASS_EXACT_972_TO_162_CENSUS_NO_IDEALS' and cref['members_per_group']==6
# Rank-zero branch only: the third exact guard gives A46=0 when A47=0;
# the pinned carrier record then supplies the L67/cap67 implication.
rank=json.loads((RANK0/'results_remaining_reps_low_rank_carrier.json').read_text());rep1=next(x for x in rank['representatives'] if x['representative_id']==1)
assert rep1['exact_guard']==['A06*A47^T=0','A47^T+A17*A46^T=0','A26*A47^T+A46^T=0'] and rep1['proof']['closed_rank_scope']==[0]
assert rep1['proof']['zero_outside_factor']==design['rank_zero_structural_branch']['outside_zero_implication'] and 'L67=0' in rep1['proof']['zero_outside_factor']
assert 'retracted/nonzero pairing-only claims are not used' in design['rank_zero_structural_branch']['source_pin_scope']
# Current exact closure is now 0..87; later two shards remain held only.
c37=json.loads((CLOSED37/'normalized_next25_dependency.json').read_text());c87=json.loads((CLOSED87/'results_referee.json').read_text());h88=json.loads((HELD88/'results_referee.json').read_text());h138=json.loads((HELD138/'results_referee.json').read_text())
assert c37['closed_union']==list(range(38)) and c87['baseline_closed_union']==list(range(38)) and c87['groups_closed']==list(range(38,88)) and c87['closed_union']==list(range(88))
assert h88['scope']['solver_runs']==0 and not h88['scope']['launch_clearance_materialized'] and h138['scope']['solver_runs']==0 and h138['scope']['groups_newly_closed']==0
remaining=future['dependencies'][1:];assert [x['group_ids'] for x in remaining]==[list(range(88,138)),list(range(138,162))] and all(x['manifest_sha256'] is x['result_sha256'] is None for x in remaining)
for entry in remaining:assert not (ROOT/entry['manifest_path']).exists() and not (ROOT/entry['result_path']).exists()
shards=[list(range(88)),list(range(88,138)),list(range(138,162))];flat=[x for s in shards for x in s];assert len(flat)==len(set(flat))==162 and sorted(flat)==list(range(162))
assert design['prospective_union_proof']=={'group_count':162,'union':list(range(162)),'duplicates':[],'missing':[],'extra':[],'all_future_required':True}
# Independent ledger/union/scope hostiles.
def validate_state(state):
 ss=state['shards'];f=[x for s in ss for x in s];assert len(f)==len(set(f))==162 and sorted(f)==list(range(162));assert state['raw']==972 and state['groups']==162 and state['members']==6 and state['yz']==[81,81];assert state['rank0']==[0];assert state['remaining_null']==2;assert state['rep']=='rep1 only' and not state['cross'] and not state['full']
good={'shards':copy.deepcopy(shards),'raw':972,'groups':162,'members':6,'yz':[81,81],'rank0':[0],'remaining_null':2,'rep':'rep1 only','cross':False,'full':False};validate_state(good);hostiles={}
mutations={'missing_group':lambda x:x['shards'][1].pop(),'duplicate_group':lambda x:x['shards'][1].append(137),'extra_group':lambda x:x['shards'][2].append(162),'raw_count':lambda x:x.__setitem__('raw',971),'orbit_count':lambda x:x.__setitem__('groups',161),'member_count':lambda x:x.__setitem__('members',5),'y_count':lambda x:x.__setitem__('yz',[80,82]),'rank0_scope':lambda x:x.__setitem__('rank0',[]),'future_slot_missing':lambda x:x.__setitem__('remaining_null',1),'cross_rep':lambda x:x.__setitem__('cross',True),'full_conjecture':lambda x:x.__setitem__('full',True),'other_rep':lambda x:x.__setitem__('rep','all reps')}
for name,mutation in mutations.items():
 candidate=copy.deepcopy(good);mutation(candidate)
 try:validate_state(candidate)
 except AssertionError:hostiles[name]=True
 else:hostiles[name]=False
assert len(hostiles)==12 and all(hostiles.values())
prodtests=json.loads((DES/'results_hostile_tests.json').read_text());assert prodtests['status']=='PASS_EXACT_LEDGER_AND_12_HOSTILES' and all(prodtests['hostile_tests'].values())
schema=json.loads((DES/'terminal_promotion_acceptance.schema.json').read_text());props=schema['properties'];assert schema['additionalProperties'] is False and set(schema['required'])==set(props)
for key in ('groups88_137_manifest_sha256','groups88_137_result_sha256','groups138_161_manifest_sha256','groups138_161_result_sha256'):assert props[key].get('pattern')=='^[0-9a-f]{64}$'
assert props['closed_group_ids']['const']==list(range(162)) and props['cross_representative_transport']['const'] is False and props['full_conjecture']['const'] is False
assert design['scope']=={'representative':'rep1 only','full_family':'all 972 localized raw charts of rep1 across both y/z partner-pivot families','transport':'only common simultaneous S3 color renaming within each source-labelled rep1 chart','cross_representative_transport':False,'other_representatives_closed':[],'full_conjecture':False,'promotion_currently_authorized':False,'solver_runs':0}
for absent in ('terminal_promotion_acceptance.json','results_terminal_promotion.json','future_terminal_seals.json'):assert not (DES/absent).exists()
assert not list(HERE.glob('*.tmp'))
out={'schema':'KRENN_X5_REP1_ALL162_TERMINAL_PROMOTION_CONDITIONAL_DESIGN_REFEREE_V1','status':'PASS_DESIGN_ONLY_CURRENT_0_87_SEALED_FUTURE_88_161_REQUIRED','producer_manifest_sha256':PINS[DES/'MANIFEST.sha256'],'producer_result_sha256':PINS[DES/'results_terminal_promotion_design.json'],'authoritative_contraction':{'raw_charts':972,'canonical_groups':162,'members_per_group':6,'y_groups':81,'z_groups':81,'y_raw':486,'z_raw':486,'two_minor_cover':True,'forward_reverse_localization':True},'rank_zero_clause':{'scope':[0],'third_guard_implication':'A47=0 implies A46=0','carrier_implication':rep1['proof']['zero_outside_factor'],'nonzero_rank_claims_used':False},'current_exact_seals':{'closed_group_ids':list(range(88)),'baseline_0_37_manifest_sha256':PINS[CLOSED37_REF/'FINAL_MANIFEST.sha256'],'groups38_87_manifest_sha256':PINS[CLOSED87/'FINAL_MANIFEST.sha256'],'groups38_87_result_sha256':PINS[CLOSED87/'results_referee.json']},'future_slots':{'groups88_137':{'manifest_sha256':None,'result_sha256':None,'held_design_manifest_sha256':PINS[HELD88/'FINAL_MANIFEST.sha256']},'groups138_161':{'manifest_sha256':None,'result_sha256':None,'held_design_manifest_sha256':PINS[HELD138/'FINAL_MANIFEST.sha256']}},'prospective_union':{'current':list(range(88)),'future_88_137':list(range(88,138)),'future_138_161':list(range(138,162)),'exact_union':list(range(162)),'duplicates':[],'missing':[],'extra':[]},'hostile_tests':hostiles,'manifest_counts':counts,'scope':{'design_only':True,'promotion_authorized':False,'rep1_only':True,'cross_representative_promotion':False,'other_representatives_closed':[],'full_conjecture':False,'solver_runs':0}}
(HERE/'results_referee.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'current_closed':88,'future':74,'raw':972,'groups':162,'hostiles':12,'runs':0},sort_keys=True))
