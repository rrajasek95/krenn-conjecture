#!/usr/bin/env python3
"""Independent exact-Q and DAG-coverage audit of the grouped 17-path package."""
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import hashlib, json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULT = HERE / "results_k20_17_path_profile_charge.json"
LEDGER = ROOT / "computations/unaudited-codex-orbit0-k20-36-path-availability-ledger-2026-08-23/results_k20_36_path_ledger.json"
DAG = ROOT / "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
OUT = HERE / "results_k20_17_path_independent_validation.json"
U = 400591699200

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def q(obj): return Fraction(int(obj["numerator"]), int(obj["denominator"]))
def logical(obj):
    x = dict(obj); x.pop("logical_sha256", None)
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def main():
    r, ledger, dag = map(lambda p: json.loads(p.read_text()), (RESULT, LEDGER, DAG))
    assert sha(RESULT) == "48fdf06e272357bea970d00e9ec00631be1cbc024b9dfc6ee2ec61ba5f13835c"
    assert r["logical_sha256"] == "7e8b3d71621560cc866b9bc50b3fc99608371af02d43d3f371f98e6d3a595504"
    assert logical(r) == r["logical_sha256"]
    assert sha(LEDGER) == r["pinned"][str(LEDGER.relative_to(ROOT))]
    assert sha(DAG) == ledger["dag"]["sha256"]
    required = dag["required_reachable_lineage_ids_by_degree"]["20"]
    assert len(required) == len(set(required)) == 36

    expected = defaultdict(list)
    existing = set()
    for x in ledger["lineages"]:
        if x["availability"] == "TERMINAL_PARENT_PROFILE_CHECKPOINT_AVAILABLE":
            expected[x["group"]].append(x["lineage_id"])
        elif x["availability"] == "EXACT_K20_CHARGE_COMPUTED":
            existing.add(x["lineage_id"])
    # Direct D20 landed after the availability ledger was frozen.
    existing.add("D20:444|R:direct")
    got = {name: g["dag_lineage_ids"] for name,g in r["groups"].items()}
    assert set(got) == set(expected)
    for name in got:
        assert got[name] == expected[name], (name, got[name], expected[name])
    flat = [x for ids in got.values() for x in ids]
    assert len(flat) == len(set(flat)) == 17
    assert flat == r["coverage"]["dag_ids"]
    assert not (set(flat) & existing)
    assert set(flat) <= set(required)

    sums = {"full": Fraction(), "irreducible": Fraction()}
    scaled = {"full": 0, "irreducible": 0}
    totals = {"keys": 0, "full_evaluations": 0, "irreducible_evaluations": 0}
    for g in r["groups"].values():
        for kind in ("full", "irreducible"):
            charge = q(g[f"{kind}_charge"])
            sc = int(g[f"{kind}_charge_scaled_U"])
            assert charge * U == sc
            assert g[f"{kind}_charge"]["text"] == str(charge)
            sums[kind] += charge; scaled[kind] += sc
        for key in totals: totals[key] += int(g[key])
    s = r["subtotal"]
    for kind in ("full", "irreducible"):
        assert sums[kind] == q(s[f"{kind}_charge"])
        assert scaled[kind] == int(s[f"{kind}_charge_scaled_U"])
        assert sums[kind] * U == scaled[kind]
    assert all(totals[k] == s[k] for k in totals)
    assert r["arithmetic"]["old_profile_scale"] // U == r["arithmetic"]["exact_scale_ratio"] == 198237
    assert r["arithmetic"]["old_profile_scale"] % U == 0

    out = {
        "status": "PASS_INDEPENDENT_K20_17_PATH_GROUPED_EXACT_Q",
        "scope": "Validates four disjoint aggregate scalars covering 17 DAG IDs; does not split aggregate scalars by individual ID or infer remaining paths.",
        "coverage": {"groups": got, "count": len(flat), "disjoint_from_existing_three": True},
        "subtotal": {
            "full_scaled_U": str(scaled["full"]), "full": str(sums["full"]),
            "irreducible_scaled_U": str(scaled["irreducible"]), "irreducible": str(sums["irreducible"]),
            **totals,
        },
        "pinned": {str(p.relative_to(ROOT)): sha(p) for p in (RESULT, LEDGER, DAG)},
    }
    out["logical_sha256"] = logical(out)
    tmp = Path(str(OUT)+".tmp"); tmp.write_text(json.dumps(out, indent=2, sort_keys=True)+"\n"); tmp.replace(OUT)
    print(json.dumps({"status":out["status"], "logical_sha256":out["logical_sha256"], **out["subtotal"]}, indent=2))

if __name__ == "__main__": main()
