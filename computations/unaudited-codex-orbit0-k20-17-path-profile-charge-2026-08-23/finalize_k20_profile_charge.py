#!/usr/bin/env python3
"""Finalize and source-audit the four exact K20 profile charge groups."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RAW = HERE / "results_k20_17_path_profile_charge.raw.json"
OUT = HERE / "results_k20_17_path_profile_charge.json"
LEDGER_REL = "computations/unaudited-codex-orbit0-k20-36-path-availability-ledger-2026-08-23/results_k20_36_path_ledger.json"
K19_REL = "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/results_k19_charge.json"
K19_LITERAL_REL = "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/results_profile_charge_selftest.json"

GROUP_IDS = {
    "K14_R33": ["D14:222|R:3-3"],
    "K15_R23": [f"D15:{p}|R:2-3" for p in ("223", "232", "322")],
    "K16_R4": [f"D16:{p}|R:4" for p in ("224", "233", "242", "323", "332", "422")],
    "K17_R3": [f"D17:{p}|R:3" for p in ("234", "243", "324", "333", "342", "423", "432")],
}

EXPECTED = {
    "K14_R33": (13_844_092, 443_010_944, 401_361_864, 668_097_555_872_690_110_464, 646_669_930_011_363_016_704),
    "K15_R23": (16_109_793, 515_513_376, 468_973_320, 2_451_374_855_329_335_902_208, 2_406_624_067_438_972_305_408),
    "K16_R4": (1_033_323, 61_999_380, 50_670_420, 55_658_097_647_153_971_200, 59_538_481_378_612_346_880),
    "K17_R3": (2_661_633, 85_172_256, 77_326_608, 628_299_883_300_894_801_920, 627_773_999_337_119_416_320),
}


def load(rel: str):
    return json.loads((ROOT / rel).read_text())


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def q(value: int, scale: int):
    x = Fraction(value, scale)
    return {"numerator": x.numerator, "denominator": x.denominator, "text": str(x)}


def logical(value) -> str:
    clean = dict(value)
    clean.pop("logical_sha256", None)
    return hashlib.sha256(json.dumps(clean, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main() -> None:
    raw = json.loads(RAW.read_text())
    ledger = load(LEDGER_REL)
    k19 = load(K19_REL)
    prior_literal = load(K19_LITERAL_REL)
    assert raw["status"] == "PASS_K20_17_PATH_PROFILE_CHARGE"
    assert raw["scale_U"] == 400_591_699_200
    assert raw["old_scale"] == 79_412_096_674_310_400
    assert raw["scale_ratio"] == 198_237
    assert raw["old_scale"] == raw["scale_U"] * raw["scale_ratio"]
    assert raw["literal_profile_cycle_checks"] == 83_968
    assert prior_literal == {"status": "PASS_LITERAL_PROFILE_CHARGE_SELFTEST", "comparisons": 83_968}

    expected_ids = {
        x["lineage_id"]
        for x in ledger["lineages"]
        if x["availability"] == "TERMINAL_PARENT_PROFILE_CHECKPOINT_AVAILABLE"
    }
    actual_ids = {x for ids in GROUP_IDS.values() for x in ids}
    assert expected_ids == actual_ids and len(actual_ids) == 17

    groups = {}
    totals = {"keys": 0, "full_evaluations": 0, "irreducible_evaluations": 0, "full": 0, "irreducible": 0}
    path_index = []
    for name, ids in GROUP_IDS.items():
        g = raw["groups"][name]
        vals = (
            g["keys"], g["full_evaluations"], g["irreducible_evaluations"],
            int(g["full_charge_scaled_U"]), int(g["irreducible_charge_scaled_U"]),
        )
        assert vals == EXPECTED[name]
        tail_count = 60 if g["target_degree"] == 4 else 32
        assert g["full_evaluations"] == g["keys"] * tail_count
        assert 0 <= g["irreducible_evaluations"] <= g["full_evaluations"]
        assert k19["pinned"][g["source_profile"]]
        groups[name] = dict(g)
        groups[name]["dag_lineage_ids"] = ids
        groups[name]["charge_granularity"] = "exact aggregate over this disjoint DAG-ID set"
        groups[name]["full_charge"] = q(vals[3], raw["scale_U"])
        groups[name]["irreducible_charge"] = q(vals[4], raw["scale_U"])
        for lineage in ids:
            path_index.append({
                "lineage_id": lineage,
                "charge_group": name,
                "individual_scalar_available": len(ids) == 1,
                "group_full_charge": groups[name]["full_charge"],
                "group_irreducible_charge": groups[name]["irreducible_charge"],
            })
        for field in ("keys", "full_evaluations", "irreducible_evaluations"):
            totals[field] += g[field]
        totals["full"] += vals[3]
        totals["irreducible"] += vals[4]

    rsub = raw["subtotal"]
    assert (totals["keys"], totals["full_evaluations"], totals["irreducible_evaluations"], totals["full"], totals["irreducible"]) == (
        rsub["keys"], rsub["full_evaluations"], rsub["irreducible_evaluations"], int(rsub["full_charge_scaled_U"]), int(rsub["irreducible_charge_scaled_U"])
    )

    result = {
        "status": "PASS_EXACT_K20_17_PATH_PROFILE_CHARGE_SUBTOTAL",
        "scale_U": raw["scale_U"],
        "arithmetic": {
            "old_profile_scale": raw["old_scale"],
            "exact_scale_ratio": raw["scale_ratio"],
            "every_profile_weight_divisible_by_scale_ratio": True,
            "sign_rule": "Frozen profile weights already contain every prior pivot sign and denominator; changing the terminal tail degree introduces no additional sign or division.",
        },
        "literal_guard": {
            "comparisons": raw["literal_profile_cycle_checks"],
            "statement": "For raw source rows, profile-derived cycle partitions equal literal child-row cycle partitions for K2/K3/K4 tails.",
        },
        "groups": groups,
        "path_index": sorted(path_index, key=lambda x: x["lineage_id"]),
        "coverage": {
            "dag_ids": sorted(actual_ids),
            "count": 17,
            "matches_certified_availability_ledger": True,
            "aggregation_guard": "Three interfaces discarded packet labels before terminal evaluation. Their exact charges belong to the named disjoint DAG-ID sets; they are not duplicated as individual lineage scalars.",
        },
        "subtotal": {
            "keys": totals["keys"],
            "full_evaluations": totals["full_evaluations"],
            "irreducible_evaluations": totals["irreducible_evaluations"],
            "full_charge_scaled_U": str(totals["full"]),
            "irreducible_charge_scaled_U": str(totals["irreducible"]),
            "full_charge": q(totals["full"], raw["scale_U"]),
            "irreducible_charge": q(totals["irreducible"], raw["scale_U"]),
        },
        "elapsed_seconds": raw["elapsed_seconds"],
        "scope": "Exact immediate 77-cycle charge for four source-compressed profile groups covering 17 K20 DAG paths; no parent-row collection, K21 tails, or complete-K20 claim.",
        "pinned": {
            LEDGER_REL: sha(ROOT / LEDGER_REL),
            K19_REL: sha(ROOT / K19_REL),
            K19_LITERAL_REL: sha(ROOT / K19_LITERAL_REL),
            str(RAW.relative_to(ROOT)): sha(RAW),
        },
    }
    result["logical_sha256"] = logical(result)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "subtotal": result["subtotal"], "logical_sha256": result["logical_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
