#!/usr/bin/env python3
"""Assemble the corrected complete K19 charge from frozen exact ledgers."""
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
OLD=ROOT/'computations/unaudited-codex-orbit0-k19-charge-2026-08-23/results_k19_charge.json'
NEW=ROOT/'computations/unaudited-codex-orbit0-hidden-k16-full-charge-2026-08-23/results_full_hidden_k3_k4_charge.json'
DAG=ROOT/'computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json'
OUT=HERE/'results_complete_k19_charge.json'
def digest(p):return sha256(p.read_bytes()).hexdigest()
def fobj(x):return {'numerator':x.numerator,'denominator':x.denominator,'text':str(x)}
def main():
 old=json.loads(OLD.read_text());new=json.loads(NEW.read_text());dag=json.loads(DAG.read_text());U=new['scale']
 mapping={
  'direct_k19':['D19:344|R:direct','D19:434|R:direct','D19:443|R:direct'],
  'k15_k4':['D15:223|R:4','D15:232|R:4','D15:322|R:4'],
  'k16_direct_k3':['D16:224|R:3','D16:233|R:3','D16:242|R:3','D16:323|R:3','D16:332|R:3','D16:422|R:3'],
  'k17_direct_k2':['D17:234|R:2','D17:243|R:2','D17:324|R:2','D17:333|R:2','D17:342|R:2','D17:423|R:2','D17:432|R:2'],
  'k17_k14_k2':['D14:222|R:3-2'],
  'k17_k15_k2':['D15:223|R:2-2','D15:232|R:2-2','D15:322|R:2-2'],
  'hidden_k14_k2_k3_repair':['D14:222|R:2-3'],
 }
 required=dag['required_reachable_lineage_ids_by_degree']['19'];covered=[x for xs in mapping.values() for x in xs]
 assert dag['counts']['nodes_reachable']==321 and len(required)==24 and len(covered)==24 and set(covered)==set(required) and len(set(covered))==24
 old_full=Fraction(old['combined']['full_charge']['numerator'],old['combined']['full_charge']['denominator']);old_irr=Fraction(old['combined']['K19_irreducible_charge']['numerator'],old['combined']['K19_irreducible_charge']['denominator'])
 miss_full=Fraction(int(new['K19_path_23']['full_charge_scaled']),U);miss_irr=Fraction(int(new['K19_path_23']['irreducible_charge_scaled']),U)
 total_full=old_full+miss_full;total_irr=old_irr+miss_irr
 k20_full=Fraction(int(new['K20_path_24']['full_charge_scaled']),U);k20_irr=Fraction(int(new['K20_path_24']['irreducible_charge_scaled']),U);k20_required=dag['required_reachable_lineage_ids_by_degree']['20'];assert len(k20_required)==36 and 'D14:222|R:2-4' in k20_required
 result={'status':'PASS_COMPLETE_K19_PATH_CHARGE_ASSEMBLY','scope':'exact 77-cycle immediate full/irreducible charge; no row collection or downstream reduction','dag_coverage':{'reachable_nodes':321,'required_K19_paths':len(required),'covered_K19_paths':len(covered),'missing_K19_paths':sorted(set(required)-set(covered)),'extra_K19_paths':sorted(set(covered)-set(required)),'component_to_lineages':mapping,'superseded_prior_placeholder':'old k16_k14_k3=0 covered only retained nonpivotable K16 rows and is replaced by hidden_k14_k2_k3_repair'},'K19':{'prior_enumerated_23_path_subtotal':{'full':fobj(old_full),'irreducible':fobj(old_irr)},'missing_path_23_repair':{'lineage':'D14:222|R:2-3','full':fobj(miss_full),'irreducible':fobj(miss_irr)},'corrected_complete_24_path_total':{'full':fobj(total_full),'irreducible':fobj(total_irr)},'nonzero_irreducible':total_irr!=0},'K20_partial_only':{'dag_required_paths':len(k20_required),'this_component_coverage':1,'lineage':'D14:222|R:2-4','full':fobj(k20_full),'irreducible':fobj(k20_irr),'complete_total_claim':False},'pinned':{str(p.relative_to(ROOT)):digest(p) for p in (OLD,NEW,DAG)}}
 logical=sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest();result['logical_sha256']=logical;HERE.mkdir(parents=True,exist_ok=True);tmp=OUT.with_suffix('.json.tmp');tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');tmp.replace(OUT);print(json.dumps({'status':result['status'],'K19_complete':result['K19']['corrected_complete_24_path_total'],'K20_partial':result['K20_partial_only'],'logical_sha256':logical},indent=2))
if __name__=='__main__':main()
