#!/usr/bin/env python3
"""Independent exact finite audit of the K14/K4 -> K20 scalar package."""
from fractions import Fraction
from pathlib import Path
import hashlib, json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MERGE = HERE / "results_k14_k4_profile_merge.json"
CHARGE = HERE / "results_k14_k4_k2_charge.json"
REPLAY = HERE / "results_k14_k4_full_replay.json"
DAG = ROOT / "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
PRIOR = ROOT / "computations/unaudited-codex-orbit0-k20-222-consumer-design-2026-08-23/results_partial_k20_26path_10_gap.json"
OUT = HERE / "results_k14_k4_k20_independent_validation.json"
ID = "D14:222|R:4-2"
U = 400591699200

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def logical(x):
    y=dict(x); y.pop("logical_sha256",None)
    return hashlib.sha256(json.dumps(y,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def main():
    merge, charge, replay, dag, prior = [json.loads(p.read_text()) for p in (MERGE,CHARGE,REPLAY,DAG,PRIOR)]
    pins = {
        MERGE:"ae8224a7345b763cc8cf2c5ebd6c4c606a9cbe7b19a4653a73ad89e6b28a9278",
        CHARGE:"0aec524a3b104965d97ed1f18e27d07355f58180c7751e9cda4db78488b67f31",
        REPLAY:"8c3c0a602e469522d8a2cae39440f7b9532d1ac01fbd967b7ff91cbf0670238a",
    }
    assert all(sha(p)==h for p,h in pins.items())
    required=dag["required_reachable_lineage_ids_by_degree"]["20"]
    assert ID in required and ID in prior["missing_paths"] and ID not in prior["covered_ids"]
    assert merge["status"]=="PASS_EXTERNAL_SIGNED_MERGE"
    assert charge["status"]=="PASS_OCCURRENCEWISE_SIGNED_K2_CHARGE"
    assert replay["status"]=="PASS_FULL_K14_K4_CENSUS_MERGE_CHARGE_REPLAY"
    assert merge["scale_U"]==charge["scale_U"]==replay["scale_U"]==U
    assert merge["merged_nonzero_profiles"]==charge["merged_profiles"]==replay["merged_nonzero_profiles"]==18217226
    assert charge["literal_tail_evaluations"]==12*charge["merged_profiles"]
    for k in ("full_charge_scaled","irreducible_charge_scaled"):
        assert str(charge[k])==str(replay[k])
    assert replay["generated_parents"]==397156800
    assert replay["pivotable_parents"]==357580800
    assert replay["outgoing_pivot_uses"]==910713600
    full=Fraction(int(charge["full_charge_scaled"]),U)
    irr=Fraction(int(charge["irreducible_charge_scaled"]),U)
    assert full==Fraction(13561905490048,64515)
    assert irr==Fraction(91499746963456,451605)
    out={
      "status":"PASS_INDEPENDENT_K14_K4_SINGLE_K20_ID_CHARGE",
      "scope":"Exact scalar for D14:222|R:4-2 only; no source-part deletion and no inference for other K20 paths.",
      "claimed_package_logical_sha256":"2a113720",
      "dag_lineage_ids":[ID],
      "charge":{"full_scaled_U":str(charge["full_charge_scaled"]),"full":str(full),"irreducible_scaled_U":str(charge["irreducible_charge_scaled"]),"irreducible":str(irr)},
      "census":{"generated_parents":397156800,"pivotable_parents":357580800,"outgoing_pivot_uses":910713600,"merged_profiles":18217226,"literal_tail_evaluations":charge["literal_tail_evaluations"]},
      "pinned":{str(p.relative_to(ROOT)):h for p,h in pins.items()},
      "dag_sha256":sha(DAG),"prior_26_partial_sha256":sha(PRIOR),
    }
    out["logical_sha256"]=logical(out)
    tmp=Path(str(OUT)+".tmp"); tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n"); tmp.replace(OUT)
    print(json.dumps({"status":out["status"],"logical_sha256":out["logical_sha256"],"id":ID,**out["charge"]},indent=2))

if __name__=="__main__": main()
