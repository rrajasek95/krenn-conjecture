#!/usr/bin/env python3
"""Assemble the two certified K20 paths and audit the 34-path remainder."""
from fractions import Fraction
from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DAGP = ROOT / "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
P24P = ROOT / "computations/unaudited-codex-orbit0-hidden-k16-full-charge-2026-08-23/results_full_hidden_k3_k4_charge.json"
P222P = HERE / "results_k20_222_charge.json"
OUT = HERE / "results_partial_k20_charge_and_34_path_gap.json"
U = 400_591_699_200

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def frac(x):
    q = Fraction(int(x), U)
    return {"scaled_numerator": str(x), "numerator": q.numerator,
            "denominator": q.denominator, "text": str(q)}

dag = json.loads(DAGP.read_text())
p24 = json.loads(P24P.read_text())
p222 = json.loads(P222P.read_text())
required = dag["required_reachable_lineage_ids_by_degree"]["20"]
assert len(required) == len(set(required)) == 36
covered = ["D14:222|R:2-2-2", "D14:222|R:2-4"]
remaining = [x for x in required if x not in covered]
assert len(remaining) == 34

def classify(x):
    if x.startswith("D15:"):
        return "raw_checkpoint_direct_K15_seeds_but_downstream_pivotable_parent_collection_missing"
    if x.startswith("D16:"):
        return "raw_checkpoint_direct_K16_seeds_but_downstream_pivotable_parent_collection_missing"
    if x.startswith("D17:"):
        return "K17_checkpoints_are_irreducible_only_regenerate_direct_K17_from_structure"
    if x.startswith("D18:"):
        return "no_pivotable_K18_checkpoint_for_this_lineage_regenerate_direct_K18_from_structure"
    if x == "D20:444|R:direct":
        return "direct_K20_source_packet_available_no_parent_checkpoint_needed"
    if x == "D14:222|R:3-3":
        return "K14_source_available_but_pivotable_K17_intermediate_not_serialized"
    if x == "D14:222|R:4-2":
        return "K14_source_available_but_pivotable_K18_intermediate_not_serialized"
    raise AssertionError(x)

groups = {}
for x in remaining: groups.setdefault(classify(x), []).append(x)
assert {k: len(v) for k,v in groups.items()} == {
    "K14_source_available_but_pivotable_K17_intermediate_not_serialized": 1,
    "K14_source_available_but_pivotable_K18_intermediate_not_serialized": 1,
    "raw_checkpoint_direct_K15_seeds_but_downstream_pivotable_parent_collection_missing": 6,
    "raw_checkpoint_direct_K16_seeds_but_downstream_pivotable_parent_collection_missing": 12,
    "K17_checkpoints_are_irreducible_only_regenerate_direct_K17_from_structure": 7,
    "no_pivotable_K18_checkpoint_for_this_lineage_regenerate_direct_K18_from_structure": 6,
    "direct_K20_source_packet_available_no_parent_checkpoint_needed": 1,
}

v24f = int(p24["K20_path_24"]["full_charge_scaled"])
v24i = int(p24["K20_path_24"]["irreducible_charge_scaled"])
v222f = int(p222["full_charge_scaled"])
v222i = int(p222["irreducible_charge_scaled"])
result = {
    "status": "PASS_EXACT_TWO_PATH_K20_PARTIAL_AND_34_PATH_GAP",
    "complete_K20_claim": False,
    "scale": U,
    "dag": {"required_paths": 36, "covered_paths": covered,
            "remaining_paths": remaining, "remaining_groups": groups},
    "certified_paths": {
        "D14:222|R:2-4": {"full": frac(v24f), "irreducible": frac(v24i),
                            "source": str(P24P.relative_to(ROOT))},
        "D14:222|R:2-2-2": {"full": frac(v222f), "irreducible": frac(v222i),
                              "source": str(P222P.relative_to(ROOT))},
    },
    "certified_two_path_partial": {
        "full": frac(v24f + v222f),
        "irreducible": frac(v24i + v222i),
    },
    "checkpoint_scope": {
        "checkpoint_direct_K15.bin": "raw direct K15 source rows; can seed its six paths, but no completed K17/K18 pivotable descendants",
        "checkpoint_direct_K16.bin": "raw direct K16 source rows; can seed its twelve paths, but no completed K18 pivotable descendants",
        "checkpoint_k17_*.bin": "irreducible normals only; cannot feed K20 because the required pivotable K17 rows were discarded",
        "results_k18_charge.json": "scalar immediate charge only; no pivotable K18 parent provenance",
        "checkpoint_k18_22_pivotable.bin": "supplies only the now-completed hidden D14:222|R:2-2-2 path",
        "filtered_k16_structure.bin": "source/factor/pivot tables can regenerate direct K17, K18, K20 and missing K14 descendants, but this is new computation",
    },
    "guard": "There is no authoritative 34-path subtotal. The two-path sum is not a complete K20 charge.",
    "pinned": {str(p.relative_to(ROOT)): sha(p) for p in (DAGP, P24P, P222P)},
}
logical = dict(result)
logical.pop("pinned")
result["logical_sha256"] = hashlib.sha256(json.dumps(logical, sort_keys=True, separators=(",",":")).encode()).hexdigest()
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": result["status"], "partial": result["certified_two_path_partial"],
                  "remaining": len(remaining), "logical_sha256": result["logical_sha256"]}, indent=2))
