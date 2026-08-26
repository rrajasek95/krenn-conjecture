#!/usr/bin/env python3
"""Independent finite audit of the direct-six grouped K20 charge package."""
from fractions import Fraction
from pathlib import Path
import hashlib, json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CENSUS = HERE / "results_direct_k18_profile_census.json"
CHARGE = HERE / "results_direct_k18_k2_charge.json"
REPLAY = HERE / "results_direct_k18_profile_census_replay.json"
REPORT = HERE / "REPORT.md"
DAG = ROOT / "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
OUT = HERE / "results_direct6_k20_independent_validation.json"
U = 400591699200
EXPECTED = [
    "D18:244|R:2", "D18:334|R:2", "D18:343|R:2",
    "D18:424|R:2", "D18:433|R:2", "D18:442|R:2",
]

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def logical(obj):
    x = dict(obj); x.pop("logical_sha256", None)
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def main():
    census, charge, replay, dag = [json.loads(p.read_text()) for p in (CENSUS, CHARGE, REPLAY, DAG)]
    pins = {
        CENSUS: "325c873857d27230797ea86a2b0c5f5a8b986b66dbaad1def315eec42374c967",
        CHARGE: "82a5c213cb916523386f524242c8a5aba0e32dd91291d0f5c017de268b1541ad",
        REPLAY: "3d3a0c0c6dd534ba22b1fffd1b41ff3a28929011be22b15d6f223d590aa7eeae",
        REPORT: "12148f43f4f63ae0270b8110b342d468c700efa5f490b52d0a9675aaffb32eb3",
    }
    assert all(sha(p) == h for p,h in pins.items())
    required = dag["required_reachable_lineage_ids_by_degree"]["20"]
    ids = sorted(census["lineages"])
    assert ids == EXPECTED
    assert len(ids) == len(set(ids)) == 6 and set(ids) <= set(required)
    assert all(x.startswith("D18:") and x.endswith("|R:2") for x in ids)

    assert census["status"] == "PASS_FULL_DIRECT6_K18_ENRICHED_PROFILE_CENSUS"
    assert replay["status"] == "PASS_INDEPENDENT_STRUCTURE_AND_DIGEST_REPLAY"
    assert charge["status"] == "PASS_TRIVIAL_K2_CHARGE_EVALUATION"
    assert census["scale"] == charge["scale"] == U
    assert replay["charge_result_sha256"] == sha(CHARGE)
    assert sum(x["full_parents"] for x in census["lineages"].values()) == 152251200
    assert sum(x["pivotable_parents"] for x in census["lineages"].values()) == 137817600
    assert sum(x["outgoing_pivot_uses"] for x in census["lineages"].values()) == census["total_outgoing_pivot_uses"] == 260736000
    assert census["merged_nonzero_keys"] == charge["profile_keys"] == 979091
    assert charge["literal_tail_evaluations"] == 12 * charge["profile_keys"]

    full_scaled = int(charge["full_charge_scaled"])
    irr_scaled = int(charge["irreducible_charge_scaled"])
    full, irr = Fraction(full_scaled, U), Fraction(irr_scaled, U)
    assert full == 391435264 and irr == 401282048
    out = {
        "status": "PASS_INDEPENDENT_DIRECT6_GROUPED_K20_CHARGE",
        "scope": "One exact aggregate scalar over six disjoint direct D18-to-K20 DAG IDs; no per-lineage scalar split and no inference for other paths.",
        "claimed_package_logical_sha256": "27b3442d",
        "dag_lineage_ids": ids,
        "coverage_count": len(ids),
        "charge": {
            "full_scaled_U": str(full_scaled), "full": str(full),
            "irreducible_scaled_U": str(irr_scaled), "irreducible": str(irr),
        },
        "census": {
            "profile_keys": charge["profile_keys"],
            "literal_tail_evaluations": charge["literal_tail_evaluations"],
            "irreducible_tail_evaluations": charge["irreducible_tail_evaluations"],
            "full_parents": 152251200,
            "pivotable_parents": 137817600,
            "outgoing_pivot_uses": 260736000,
        },
        "pinned": {str(p.relative_to(ROOT)): h for p,h in pins.items()},
        "dag_sha256": sha(DAG),
    }
    out["logical_sha256"] = logical(out)
    tmp = Path(str(OUT)+".tmp"); tmp.write_text(json.dumps(out, indent=2, sort_keys=True)+"\n"); tmp.replace(OUT)
    print(json.dumps({"status":out["status"], "logical_sha256":out["logical_sha256"], "ids":ids, **out["charge"]}, indent=2))

if __name__ == "__main__": main()
