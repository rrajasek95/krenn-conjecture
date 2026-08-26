#!/usr/bin/env python3
"""Independent design-only referee of the conditional rep4 all-162 ledger."""
from __future__ import annotations
import copy,hashlib,itertools,json,os
from pathlib import Path
H=Path(__file__).resolve().parent; ROOT=H.parents[1]
DES=ROOT/'computations/unaudited-codex-n8-x5-rep4-all162-terminal-promotion-conditional-design-2026-08-26'
CON=ROOT/'computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-design-2026-08-25'
CREF=ROOT/'computations/unaudited-codex-n8-x5-rep4-guard-minor-contraction-referee-2026-08-25'
CEN=ROOT/'computations/unaudited-codex-n8-x5-rep4-first25-exact-q-held-2026-08-26'
RANK0=ROOT/'computations/unaudited-codex-n8-x5-seven-block-reps1-4-5-low-rank-carrier-2026-08-25'
Q1=ROOT/'computations/unaudited-codex-n8-x5-rep4-all-equal-y-exact-q-terminal-referee-2026-08-25'
Q2=ROOT/'computations/unaudited-codex-n8-x5-rep4-all-equal-y-exact-q-terminal-second-referee-2026-08-25'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def replay(m):
 n=0
 for line in m.read_text().splitlines():
  if not line.strip(): continue
  digest,name=line.split(None,1); name=name.strip(); local=(m.parent/name).resolve(); rooted=(ROOT/name).resolve(); p=local if local.is_file() else rooted
  assert p.is_file() and sha(p)==digest,(p,digest); n+=1
 return n
PINS={
 DES/'MANIFEST.sha256':'933016a415b1bf3b1d1ec851514461184097b25ed578f1a5e83488ffc075b237',
 DES/'results_terminal_promotion_design.json':'ced7906cb327337ec86b0a87738c955d7542fb58652ea0885409754a9915ca39',
 DES/'future_dependencies.json':'0ec1fb5dd783b8fc3e729e862390300366ec534c734fd3de0ae00a056f40e2f0',
 DES/'results_hostile_tests.json':'778f021aa3af9a57993143fa8c1169dbcfa606c145e2184d2c33f93b11d76758',
 DES/'terminal_promotion_acceptance.schema.json':'acd1006444d45c286369be9555fb77dc203e74f0e6b12319ca2ce8bebae82fce',
 CON/'MANIFEST.sha256':'7f47c0567580aba565925b95860bace46ebaf5703aace4ec8aa100f48ec33e02',
 CON/'results_rep4_contraction_design.json':'7e96874cca1afaaa377aa3001d8e00b73ed4fe9322381ec269c4a46b9144bf0c',
 CREF/'FINAL_MANIFEST.sha256':'185b51b8107d5dcf12e7194a7d806157e0df6a2b6d047cf4adc6c8ac400fa4ae',
 CREF/'results_referee.json':'279565e76618b8fa8c4eb08f513f8109a018d23ed1e9fe11acb0489dd82bb863',
 CEN/'MANIFEST.sha256':'d6c098fb885ad9faac566b6f01a9e94f01aa6a8b4a61562ec4fa14f66b44a029',
 CEN/'canonical_census.json':'12773aacfd9fa702ce4202a5da64c356d0451be8b904ebcf9848bcbf99913261',
 RANK0/'MANIFEST.sha256':'9a3cec1a39422d2c3d7a6b40f6acdec0b04b19b893c0a1fb657c69d3b50bb8fe',
 RANK0/'results_remaining_reps_low_rank_carrier.json':'359aa45545d85378dd9e945eb82be3adb98922648025fe853f930feac2b5f458',
 Q1/'FINAL_MANIFEST.sha256':'a8280c98344eb62f6df89ffec125e6cdba33a7dae63f47061c71114f7aabe805',
 Q1/'results_referee.json':'ccc22fe2ec3d5db1d3ed3d175e5196819efa3e412cf632ef8c862ae70f3b72d3',
 Q2/'FINAL_MANIFEST.sha256':'b2a543e59df1edf32df414f44938b418e35ea4ed258354642aff3d2b45e522b4',
 Q2/'results_second_referee.json':'4e38098b41a4b4fb16eb443e56f4b6ca6de6edbd390eec9df464b0147e1c21f1',
}
for p,d in PINS.items(): assert sha(p)==d,(p,sha(p),d)
counts={'design':replay(DES/'MANIFEST.sha256'),'contraction':replay(CON/'MANIFEST.sha256'),'contraction_referee':replay(CREF/'FINAL_MANIFEST.sha256'),'census_held':replay(CEN/'MANIFEST.sha256'),'rank0':replay(RANK0/'MANIFEST.sha256'),'group0_referee1':replay(Q1/'FINAL_MANIFEST.sha256'),'group0_referee2':replay(Q2/'FINAL_MANIFEST.sha256')}
design=json.loads((DES/'results_terminal_promotion_design.json').read_text()); future=json.loads((DES/'future_dependencies.json').read_text())
con=json.loads((CON/'results_rep4_contraction_design.json').read_text()); cref=json.loads((CREF/'results_referee.json').read_text())
assert con['status']=='PASS_STRICT_SMALLER_EXACT_DESIGN_NO_IDEAL_RUN' and cref['status']=='PASS_STRICT_SMALLER_EXACT_DESIGN_NO_RUN_NO_CLOSURE'
assert con['chart_census']==cref['chart_census']=={'raw':972,'S3_orbits':162,'orbit_size':6,'y_orbits':81,'z_orbits':81}
# Independently regenerate the simultaneous-S3 orbit partition.
def canonical(record):
 coordinate,p,q,r,kind,s,a,b=record; images=[]
 for perm in itertools.permutations(range(3)):
  aa,bb=sorted((perm[a],perm[b])); images.append((perm[coordinate],perm[p],perm[q],perm[r],kind,perm[s],aa,bb))
 return min(images)
raw=[]
for coordinate,p,q,r,s in itertools.product(range(3),repeat=5):
 for kind in ('y','z'):
  for other in range(3):
   if other!=q:
    a,b=sorted((q,other)); raw.append((coordinate,p,q,r,kind,s,a,b))
groups={}
for rec in raw: groups.setdefault(canonical(rec),[]).append(rec)
assert len(raw)==len(set(raw))==972 and len(groups)==162 and set(map(len,groups.values()))=={6}
keys=sorted(groups); census=json.loads((CEN/'canonical_census.json').read_text()); records=census['groups']
assert census['counts']=={'raw':972,'canonical_groups':162,'members_each':6,'y_groups':81,'z_groups':81}
assert [x['group_id'] for x in records]==list(range(162))
for gid,key in enumerate(keys):
 rec=records[gid]; assert tuple(rec['canonical_chart'])==key and {tuple(x) for x in rec['raw_members']}==set(groups[key]) and rec['raw_member_count']==6
assert sum(k[4]=='y' for k in keys)==sum(k[4]=='z' for k in keys)==81 and sum(x[4]=='y' for x in raw)==sum(x[4]=='z' for x in raw)==486
# Rank-zero clause is exact and intentionally does not promote nonzero pairing-only ranks.
low=json.loads((RANK0/'results_remaining_reps_low_rank_carrier.json').read_text()); rep4=next(x for x in low['representatives'] if x['representative_id']==4)
assert rep4['proof']['closed_rank_scope']==[0] and rep4['proof']['pairing_only_rank_scope']==[1,2,3]
assert rep4['proof']['zero_outside_factor']==design['rank_zero_structural_branch']['zero_outside_implication'] and 'A47=0' in rep4['proof']['zero_outside_factor'] and 'L67=0' in rep4['proof']['zero_outside_factor']
assert design['rank_zero_structural_branch']['scope']==[0] and 'nonzero pairing-only claims are not used' in design['rank_zero_structural_branch']['source_pin_scope']
# Group zero has two independent exact-Q unit seals, matching census group zero.
q1=json.loads((Q1/'results_referee.json').read_text()); q2=json.loads((Q2/'results_second_referee.json').read_text())
assert q1['status']=='PASS_EXACT_Q_UNIT_IDEAL_REP4_ALL_EQUAL_Y_SAME_CHART' and q2['status']=='PASS_EXACT_Q_STRONG_UNIT_IDEAL_ONE_REP4_CHART_ONLY'
assert q1['source_sha256']==q2['source_sha256']==records[0]['exact_Q_source_sha256']==design['sealed_group0']['exact_Q_source_sha256']
assert design['sealed_group0']['group_id']==0 and design['sealed_group0']['chart']==records[0]['canonical_chart']==[0,0,0,0,'y',0,0,1] and design['sealed_group0']['unit_remainder']==0
# Four held source families cover the future IDs, but all terminal hashes/files remain absent.
held=[
 ('computations/unaudited-codex-n8-x5-rep4-first25-exact-q-held-2026-08-26/source_ledger.json',list(range(1,26))),
 ('computations/unaudited-codex-n8-x5-rep4-groups26-75-exact-q-conditional-held-2026-08-26/source_ledger.json',list(range(26,76))),
 ('computations/unaudited-codex-n8-x5-rep4-groups76-125-exact-q-conditional-held-2026-08-26/source_ledger.json',list(range(76,126))),
 ('computations/unaudited-codex-n8-x5-rep4-groups126-161-exact-q-conditional-held-2026-08-26/source_ledger.json',list(range(126,162))),
]
for rel,ids in held:
 ledger=json.loads((ROOT/rel).read_text()); scope=ledger['scope']
 assert ledger['selection']['selected_group_ids']==ids and scope['solver_launches']==0 and scope['results_materialized']==0 and scope['mathematical_coverage_added'] is False and scope['rep4_closed'] is False
expected=[[0]]+[ids for _,ids in held]
assert [x['group_ids'] for x in design['closure_shards']]==expected
flat=sum(expected,[]); assert len(flat)==len(set(flat))==162 and sorted(flat)==list(range(162))
assert design['prospective_union_proof']=={'group_count':162,'union':list(range(162)),'duplicates':[],'missing':[],'extra':[],'all_four_future_required':True}
assert future['status']=='UNSATISFIED_FOUR_NULL_HASH_PAIRS' and future['satisfied'] is False and future['sealed_group0'] is True
assert [x['group_ids'] for x in future['dependencies']]==expected[1:] and all(not x['satisfied'] and x['manifest_sha256'] is x['result_sha256'] is None for x in future['dependencies'])
for dep in future['dependencies']: assert not (ROOT/dep['manifest_path']).exists() and not (ROOT/dep['result_path']).exists()
# Independent 16-way fail-closed state mutations, including all overclaim surfaces.
def validate_state(x):
 f=sum(x['shards'],[]); assert len(f)==len(set(f))==162 and sorted(f)==list(range(162)); assert x['raw']==972 and x['groups']==162 and x['members']==6 and x['yz']==[81,81]; assert x['rank0']==[0] and x['group0']; assert x['null']==8 and x['rep']=='rep4 only' and not x['cross'] and not x['full'] and x['other']==[]
good={'shards':copy.deepcopy(expected),'raw':972,'groups':162,'members':6,'yz':[81,81],'rank0':[0],'group0':True,'null':8,'rep':'rep4 only','cross':False,'full':False,'other':[]}; validate_state(good)
mutations={
 'missing_group':lambda x:x['shards'][2].pop(),'duplicate_group':lambda x:x['shards'][3].append(125),'extra_group':lambda x:x['shards'][4].append(162),
 'raw_count':lambda x:x.__setitem__('raw',971),'orbit_count':lambda x:x.__setitem__('groups',161),'member_count':lambda x:x.__setitem__('members',5),'yz_count':lambda x:x.__setitem__('yz',[80,82]),
 'rank0_removed':lambda x:x.__setitem__('rank0',[]),'rank0_expanded':lambda x:x.__setitem__('rank0',[0,1]),'group0_unsealed':lambda x:x.__setitem__('group0',False),
 'future_hash_present':lambda x:x.__setitem__('null',7),'future_all_satisfied':lambda x:x.__setitem__('null',0),'wrong_rep':lambda x:x.__setitem__('rep','rep2 only'),
 'cross_rep':lambda x:x.__setitem__('cross',True),'full_conjecture':lambda x:x.__setitem__('full',True),'other_rep':lambda x:x.__setitem__('other',[1]),}
hostiles={}
for name,fn in mutations.items():
 candidate=copy.deepcopy(good); fn(candidate)
 try: validate_state(candidate)
 except AssertionError: hostiles[name]=True
 else: hostiles[name]=False
assert len(hostiles)==16 and all(hostiles.values())
prod=json.loads((DES/'results_hostile_tests.json').read_text()); assert prod['status']=='PASS_EXACT_LEDGER_AND_16_HOSTILES' and prod['hostile_count']==16 and all(prod['hostile_tests'].values())
schema=json.loads((DES/'terminal_promotion_acceptance.schema.json').read_text()); assert schema['additionalProperties'] is False and set(schema['required'])==set(schema['properties'])
assert schema['properties']['closed_group_ids']['const']==list(range(162)) and schema['properties']['representative']['const']=='rep4' and schema['properties']['cross_representative_transport']['const'] is False and schema['properties']['full_conjecture']['const'] is False
assert design['scope']=={'representative':'rep4 only','full_family':'all 972 localized raw charts of rep4 across both y/z partner-pivot families','transport':'only common simultaneous S3 color renaming within each source-labelled rep4 chart','cross_representative_transport':False,'other_representatives_closed':[],'full_conjecture':False,'promotion_currently_authorized':False,'solver_runs':0}
for absent in ('terminal_promotion_acceptance.json','results_terminal_promotion.json','future_terminal_seals.json'): assert not (DES/absent).exists()
assert not list(DES.glob('*.tmp')) and not list(H.glob('*.tmp'))
out={'schema':'KRENN_X5_REP4_ALL162_TERMINAL_PROMOTION_CONDITIONAL_DESIGN_REFEREE_V1','status':'PASS_DESIGN_ONLY_GROUP0_SEALED_FUTURE_1_161_REQUIRED','producer_manifest_sha256':PINS[DES/'MANIFEST.sha256'],'producer_result_sha256':PINS[DES/'results_terminal_promotion_design.json'],'authoritative_contraction':{'raw_charts':972,'canonical_groups':162,'members_per_group':6,'y_groups':81,'z_groups':81,'y_raw':486,'z_raw':486,'variables_each':91,'generators_each':6577,'forward_reverse_localization':True},'rank_zero_clause':{'scope':[0],'outside_pair':'47','carrier_implication':rep4['proof']['zero_outside_factor'],'nonzero_rank_claims_used':False},'sealed_group0':{'group_id':0,'source_sha256':records[0]['exact_Q_source_sha256'],'independent_q_seals':2,'unit_remainder':0},'future_slots':{dep['name']:{'group_ids':dep['group_ids'],'manifest_sha256':None,'result_sha256':None} for dep in future['dependencies']},'prospective_union':{'sealed':[0],'future':list(range(1,162)),'exact_union':list(range(162)),'duplicates':[],'missing':[],'extra':[]},'future_hashes_absent':8,'future_artifacts_absent':8,'hostile_tests':hostiles,'producer_hostiles_passed':16,'manifest_counts':counts,'scope':{'design_only':True,'promotion_authorized':False,'rep4_only':True,'cross_representative_promotion':False,'other_representatives_closed':[],'full_conjecture':False,'solver_runs':0}}
t=H/'results_referee.json.tmp'; t.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); os.replace(t,H/'results_referee.json')
print(json.dumps({'status':out['status'],'sealed_groups':1,'future_groups':161,'raw':972,'hostiles':16,'runs':0},sort_keys=True))
