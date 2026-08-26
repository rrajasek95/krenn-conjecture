#!/usr/bin/env python3
"""Assemble the corrected complete K18 charge from frozen exact ledgers."""
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
OLD=ROOT/'computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/results_k18_charge.json';NEW=HERE/'results_missing_k18_22_charge.json';DAG=ROOT/'computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json';OUT=HERE/'results_complete_k18_charge.json'
def digest(p):return sha256(p.read_bytes()).hexdigest()
def obj(x):return {'numerator':x.numerator,'denominator':x.denominator,'text':str(x)}
def main():
 old=json.loads(OLD.read_text());new=json.loads(NEW.read_text());dag=json.loads(DAG.read_text());U=new['scale']
 mapping={'direct_K18':['D18:244|R:direct','D18:334|R:direct','D18:343|R:direct','D18:424|R:direct','D18:433|R:direct','D18:442|R:direct'],'K14_K4':['D14:222|R:4'],'K15_K3':['D15:223|R:3','D15:232|R:3','D15:322|R:3'],'K16_K2':['D16:224|R:2','D16:233|R:2','D16:242|R:2','D16:323|R:2','D16:332|R:2','D16:422|R:2'],'hidden_K14_K2_K2_repair':['D14:222|R:2-2']}
 required=dag['required_reachable_lineage_ids_by_degree']['18'];covered=[x for xs in mapping.values()for x in xs];assert dag['counts']['nodes_reachable']==321 and len(required)==len(covered)==17 and set(required)==set(covered) and len(set(covered))==17
 of=Fraction(old['total']['full_charge']['numerator'],old['total']['full_charge']['denominator']);oi=Fraction(old['total']['K18_irreducible_charge']['numerator'],old['total']['K18_irreducible_charge']['denominator']);mf=Fraction(int(new['full_charge_scaled']),U);mi=Fraction(int(new['irreducible_charge_scaled']),U);tf=of+mf;ti=oi+mi
 result={'status':'PASS_COMPLETE_K18_PATH_CHARGE_ASSEMBLY','scope':'exact immediate 77-cycle full/irreducible charge; no K18 row collection or later tails','linearity_theorem':new['linearity_theorem'],'dag_coverage':{'reachable_nodes':321,'required_K18_paths':17,'covered_K18_paths':17,'missing':[],'extra':[],'component_to_lineages':mapping,'superseded_scope':'old K16_K2 saw no hidden K14 [2,2] contribution because discarded K16 parents were absent; the recovered component is added once'},'K18':{'prior_enumerated_16_path_subtotal':{'full':obj(of),'irreducible':obj(oi)},'missing_path_22_repair':{'lineage':'D14:222|R:2-2','full':obj(mf),'irreducible':obj(mi)},'corrected_complete_17_path_total':{'full':obj(tf),'irreducible':obj(ti)},'nonzero_irreducible':ti!=0},'guards':{'literal_prefix':new['literal_prefix_guard'],'merged_profiles':new['merged_profiles'],'profile_tail_terms':{'full':new['full_profile_tail_terms'],'irreducible':new['irreducible_profile_tail_terms']}},'pinned':{str(p.relative_to(ROOT)):digest(p) for p in(OLD,NEW,DAG)}}
 logical=sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest();result['logical_sha256']=logical;tmp=OUT.with_suffix('.json.tmp');tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');tmp.replace(OUT);print(json.dumps({'status':result['status'],'complete':result['K18']['corrected_complete_17_path_total'],'logical_sha256':logical},indent=2))
if __name__=='__main__':main()
