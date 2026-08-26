#!/usr/bin/env python3
"""Fail-closed design hostiles; no solver."""
import copy,hashlib,json,os
from pathlib import Path
H=Path(__file__).resolve().parent; r=json.loads((H/'results_design.json').read_text())
def validate(x):
 assert x['status']=='PASS_EXACT_19_STRATUM_DESIGN_ZERO_SOLVES' and x['consumed_attempt']['relaunch_authorized'] is False
 assert x['source_rebuild']=={'variables':91,'generators':6577,'bytes':1834840,'sha256':'79a2cf5c70cf939e434cf445c98d7a5e132f68ddd2253f7757d06d4450da01c8','byte_identical':True}
 t=x['torus']; assert t['matching_products_weight_zero'] and t['guard_character_relations'] and t['unit_gauge_coordinates']==['beta','abar','a57_00'] and t['unit_gauge_determinant']==1 and t['base_gauge_variables']==88
 d=x['decomposition']; assert d['stratum_count']==19 and d['variable_histogram']=={'70':1,'78':9,'87':9} and len(d['sources'])==19
 assert sum(s['kind']=='A67_entry_open' for s in d['sources'])==9 and sum(s['kind']=='A67_zero_A12_entry_open' for s in d['sources'])==9 and sum(s['kind']=='A67_zero_A12_zero' for s in d['sources'])==1
 assert all(s['generators']==s['unique_generators']==6577 and s['trivial_generators']==0 for s in d['sources'])
 assert x['symmetry_obstruction']['source_labelled_vertex_automorphism_count']==1 and x['symmetry_obstruction']['transport_to_closed_group_found'] is False
 assert x['scope']=={'design_only':True,'singular_runs':0,'ideal_runs':0,'group16_closed':False,'rep2_closed':False,'performance_claim':False,'relaunch_or_reuse_authorized':False,'next_valid_step':'independent design audit, then fresh held pilots per stratum only if separately cleared'}
validate(r); hostiles={}
mutations={'drop_stratum':lambda x:x['decomposition']['sources'].pop(),'wrong_gauge_det':lambda x:x['torus'].__setitem__('unit_gauge_determinant',0),'omit_unit':lambda x:x['torus']['unit_gauge_coordinates'].pop(),'matching_weight':lambda x:x['torus'].__setitem__('matching_products_weight_zero',False),'guard_weight':lambda x:x['torus'].__setitem__('guard_character_relations',False),'variable_overclaim':lambda x:x['decomposition'].__setitem__('variable_histogram',{'70':1,'78':9,'86':9}),'duplicate_generator':lambda x:x['decomposition']['sources'][0].__setitem__('unique_generators',6576),'trivial_generator':lambda x:x['decomposition']['sources'][0].__setitem__('trivial_generators',1),'symmetry_overclaim':lambda x:x['symmetry_obstruction'].__setitem__('transport_to_closed_group_found',True),'automorphism_overclaim':lambda x:x['symmetry_obstruction'].__setitem__('source_labelled_vertex_automorphism_count',2),'relaunch':lambda x:x['consumed_attempt'].__setitem__('relaunch_authorized',True),'closure':lambda x:x['scope'].__setitem__('group16_closed',True),'run':lambda x:x['scope'].__setitem__('singular_runs',1),'performance':lambda x:x['scope'].__setitem__('performance_claim',True)}
for name,fn in mutations.items():
 x=copy.deepcopy(r); fn(x)
 try:validate(x)
 except (AssertionError,KeyError,TypeError):hostiles[name]=True
 else:hostiles[name]=False
assert len(hostiles)==14 and all(hostiles.values())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest(); out={'schema':'KRENN_X5_REP2_GROUP16_TORUS_GAUGE_DESIGN_HOSTILES_V1','status':'PASS_14_HOSTILES_ZERO_RUN','design_sha256':sha(H/'results_design.json'),'hostile_count':14,'hostile_tests':hostiles,'solver_runs':0}
t=H/'results_hostiles.json.tmp'; t.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); os.replace(t,H/'results_hostiles.json'); print(json.dumps({'status':out['status'],'hostiles':14},sort_keys=True))
