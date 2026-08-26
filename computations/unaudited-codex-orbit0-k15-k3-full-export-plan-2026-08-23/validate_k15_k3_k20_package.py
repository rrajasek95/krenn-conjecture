#!/usr/bin/env python3
"""Independent exact audit of the grouped K15/K3 -> K20 charge."""
from fractions import Fraction
from pathlib import Path
import hashlib, json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
CHARGE=HERE/"results_k15_k3_group_charge.json"
MERGE=HERE/"results_k15_k3_profile_merge.json"
REFEREE=HERE/"results_k15_merge_full_stream_referee.json"
SAMPLES=HERE/"k15_k3_group_charge_samples.tsv"
REPORT=HERE/"CHARGE_REPORT.md"
DAG=ROOT/"computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
PRIOR=ROOT/"computations/unaudited-codex-orbit0-k20-222-consumer-design-2026-08-23/results_partial_k20_27path_9_gap.json"
OUT=HERE/"results_k15_k3_k20_independent_validation.json"
IDS=["D15:223|R:3-2","D15:232|R:3-2","D15:322|R:3-2"]
U=400591699200

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def logical(x):
 y=dict(x);y.pop("logical_sha256",None)
 return hashlib.sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def main():
 c,m,r,dag,prior=[json.loads(p.read_text()) for p in (CHARGE,MERGE,REFEREE,DAG,PRIOR)]
 pins={CHARGE:"6de9c573ba136304e91db2a9fc83ad1ab2804cee5103102cd77ef568fb60fdb7",MERGE:"7033bbff3bd353ef306de165e94bf11911f65d9570da6079eee7b382a4181c9b",REFEREE:"8ccd570fc6d36a17989c6877d4229b8a5f4d76922709461280ad696b03c46cb7",SAMPLES:"3a1fc64ac6ae7035030706e2a9d7e58f2898f05e28fc9adf45fcf29c540aa18e",REPORT:"baea4aa98eb2e5d5599482d4768e42a19b6f6eee02b7d23b4cecb2ad2a138cbf"}
 assert all(sha(p)==h for p,h in pins.items())
 required=dag["required_reachable_lineage_ids_by_degree"]["20"]
 assert all(x in required and x in prior["missing_paths"] and x not in prior["covered_ids"] for x in IDS)
 assert len(IDS)==len(set(IDS))==3
 assert c["status"]=="PASS_K15_K3_GROUPED_OCCURRENCEWISE_K2_CHARGE"
 assert m["status"]=="PASS_FULL_K15_K3_SIGNED_PROFILE_MERGE"
 assert c["scale_U"]==str(U) and m["scale_U"]==str(U)
 assert c["profile_records"]==m["output_records"]==25564391
 assert c["input_profile_uses"]==m["output_uses"]==2311887188
 assert c["input_weight_scaled"]==m["output_weight_scaled"]
 assert c["profile_tail_evaluations"]==12*c["profile_records"]
 assert c["individual_id_charges"] is None
 full=Fraction(int(c["full_77_charge_scaled"]),U)
 irr=Fraction(int(c["irreducible_77_charge_scaled"]),U)
 assert full==Fraction(1697405675284864,451605)
 assert irr==Fraction(1647487669247872,451605)
 out={"status":"PASS_INDEPENDENT_K15_K3_GROUPED_THREE_ID_K20_CHARGE","scope":"One source-faithful aggregate scalar over exactly three D15:*|R:3-2 DAG IDs; no individual scalar split or K16 inference.","dag_lineage_ids":IDS,"charge":{"full_scaled_U":c["full_77_charge_scaled"],"full":str(full),"irreducible_scaled_U":c["irreducible_77_charge_scaled"],"irreducible":str(irr)},"census":{"profile_records":c["profile_records"],"profile_tail_evaluations":c["profile_tail_evaluations"],"irreducible_profile_tail_evaluations":c["irreducible_profile_tail_evaluations"],"input_profile_uses":c["input_profile_uses"],"literal_key_guards":c["literal_key_guards"]},"pinned":{str(p.relative_to(ROOT)):h for p,h in pins.items()},"dag_sha256":sha(DAG),"prior_27_partial_sha256":sha(PRIOR)}
 out["logical_sha256"]=logical(out)
 tmp=Path(str(OUT)+".tmp");tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");tmp.replace(OUT)
 print(json.dumps({"status":out["status"],"logical_sha256":out["logical_sha256"],"ids":IDS,**out["charge"]},indent=2))

if __name__=="__main__":main()
