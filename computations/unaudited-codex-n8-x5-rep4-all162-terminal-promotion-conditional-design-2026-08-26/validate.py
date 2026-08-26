#!/usr/bin/env python3
"""Fail-closed validation of held rep4 all-162 terminal-promotion design."""
import copy,hashlib,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
design=json.loads((HERE/'results_terminal_promotion_design.json').read_text());future=json.loads((HERE/'future_dependencies.json').read_text());hostiles=json.loads((HERE/'results_hostile_tests.json').read_text());schema=json.loads((HERE/'terminal_promotion_acceptance.schema.json').read_text());assert design['status']=='HELD_PROMOTION_FOUR_FUTURE_PASS_SEALS_ABSENT'
c=design['authoritative_contraction'];assert c['raw_charts']==972 and c['canonical_s3_charts']==162 and c['members_per_chart']==6 and c['y_groups']==c['z_groups']==81 and c['y_raw']==c['z_raw']==486 and c['independent_referee_pass'] is True
rank0=design['rank_zero_structural_branch'];assert rank0['representative_id']==4 and rank0['scope']==[0] and rank0['outside_pair']=='47' and 'A47=0' in rank0['zero_outside_implication'] and 'L67=0' in rank0['zero_outside_implication'] and 'nonzero pairing-only claims are not used' in rank0['source_pin_scope']
g0=design['sealed_group0'];assert g0['group_id']==0 and g0['chart']==[0,0,0,0,'y',0,0,1] and g0['exact_Q_source_sha256']=='c90c69b11ca931677bc1de138bdfc8c1eb7618d5aee20744764e4a4b1b511019' and g0['unit_remainder']==0
expected=[[0],list(range(1,26)),list(range(26,76)),list(range(76,126)),list(range(126,162))];assert [s['group_ids'] for s in design['closure_shards']]==expected and sum(expected,[])==list(range(162)) and design['prospective_union_proof']=={'group_count':162,'union':list(range(162)),'duplicates':[],'missing':[],'extra':[],'all_four_future_required':True}
t=design['raw_s3_transport'];assert [x['group_id'] for x in t]==list(range(162)) and all(x['raw_member_count']==len(x['raw_s3_members'])==6 for x in t);raw=[tuple(m) for x in t for m in x['raw_s3_members']];assert len(raw)==len(set(raw))==972 and sum(x['family']=='y' for x in t)==sum(x['family']=='z' for x in t)==81
assert design['scope']=={'representative':'rep4 only','full_family':'all 972 localized raw charts of rep4 across both y/z partner-pivot families','transport':'only common simultaneous S3 color renaming within each source-labelled rep4 chart','cross_representative_transport':False,'other_representatives_closed':[],'full_conjecture':False,'promotion_currently_authorized':False,'solver_runs':0}
assert future['status']=='UNSATISFIED_FOUR_NULL_HASH_PAIRS' and future['sealed_group0'] is True and future['satisfied'] is False and [d['group_ids'] for d in future['dependencies']]==expected[1:] and all(d['manifest_sha256'] is d['result_sha256'] is None and d['satisfied'] is False for d in future['dependencies'])
for d in future['dependencies']:assert not (ROOT/d['manifest_path']).exists() and not (ROOT/d['result_path']).exists()
assert hostiles['status']=='PASS_EXACT_LEDGER_AND_16_HOSTILES' and hostiles['hostile_count']==len(hostiles['hostile_tests'])==16 and all(hostiles['hostile_tests'].values()) and hostiles['solver_runs']==0 and hostiles['design_sha256']==sha(HERE/'results_terminal_promotion_design.json') and hostiles['future_dependencies_sha256']==sha(HERE/'future_dependencies.json')
assert schema['additionalProperties'] is False and set(schema['required'])==set(schema['properties']);props=schema['properties'];assert props['closed_group_ids']['const']==list(range(162)) and props['representative']['const']=='rep4' and props['promotion_design_sha256']['const']==sha(HERE/'results_terminal_promotion_design.json') and props['future_dependencies_sha256']['const']==sha(HERE/'future_dependencies.json')
def accepts(instance):
 if set(instance)!=set(schema['required']):return False
 for key,rule in props.items():
  value=instance[key]
  if 'const' in rule and value!=rule['const']:return False
  if rule.get('type')=='string' and not isinstance(value,str):return False
  if 'pattern' in rule and (not isinstance(value,str) or re.fullmatch(rule['pattern'],value) is None):return False
 return True
good={key:(rule['const'] if 'const' in rule else 'a'*64) for key,rule in props.items()};assert accepts(good);schema_hostiles={}
for name,mutate in {'null_future_hash':lambda x:x.__setitem__('groups1_25_manifest_sha256',None),'malformed_future_hash':lambda x:x.__setitem__('groups126_161_result_sha256','a'*63),'missing_group':lambda x:x['closed_group_ids'].pop(),'cross_rep_true':lambda x:x.__setitem__('cross_representative_transport',True),'full_conjecture_true':lambda x:x.__setitem__('full_conjecture',True),'wrong_representative':lambda x:x.__setitem__('representative','rep1'),'extra_property':lambda x:x.__setitem__('other_rep',2),'wrong_group0_referee':lambda x:x.__setitem__('group0_first_referee_manifest_sha256','0'*64)}.items():candidate=copy.deepcopy(good);mutate(candidate);schema_hostiles[name]=not accepts(candidate)
assert len(schema_hostiles)==8 and all(schema_hostiles.values())
for forbidden in ('terminal_promotion_acceptance.json','results_terminal_promotion.json','future_terminal_seals.json'):assert not (HERE/forbidden).exists()
assert not list(HERE.glob('*.tmp')) and not list(HERE.glob('*.singular'))
for rel,want in design['pins'].items():path=ROOT/rel;assert path.is_file() and sha(path)==want,rel
m=HERE/'MANIFEST.sha256';checked=0
if m.exists():
 for line in m.read_text().splitlines():digest,name=line.split('  ',1);path=(HERE/name).resolve();assert path.is_file() and sha(path)==digest,name;checked+=1
print(json.dumps({'status':'PASS_HELD_ZERO_RUN_FOUR_FUTURE_SEALS_REQUIRED','canonical_groups':162,'raw_s3_members':972,'y_z_groups':[81,81],'sealed_group0':[0],'future_exact_q_required':[1,161],'ledger_hostiles':16,'schema_hostiles':8,'manifest_lines_checked':checked,'solver_runs':0},sort_keys=True))
