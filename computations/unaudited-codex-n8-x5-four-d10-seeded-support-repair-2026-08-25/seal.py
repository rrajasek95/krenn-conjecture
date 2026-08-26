#!/usr/bin/env python3
"""Fail-closed cross-artifact seal for the four-branch D10 gate."""
import hashlib
import json
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PRIMES = (1073741827, 1000000007)
BRANCHES = ("direct", "triangle_endpoint_colour", "third_colour", "cap_endpoint_colour")
EXPECTED = {
    "source": "162fb54dfc1c28f93d1a6f0a7dbbb0827f18c57645a28ab0fb602cf1bd3e85b6",
    "binary": "48cce22f3f5c9cb897b98b65a7f3d1fb971f115fc696c404170cb2148f7c211a",
    "independent_replay": "399b86e7e2625806db294f1b8a1203cffef078639f11c7892fd47359061998c0",
}

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

def load(name):
    return json.loads((HERE / name).read_text())

def parse_dual(path):
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    out = {}
    for line in lines[1:]:
        kind, raw, value = line.split("\t")
        row = tuple(map(int, raw.split(",")))
        assert kind == "ROW" and len(row) == 10 and row == tuple(sorted(row)) and row not in out
        out[row] = int(value)
    assert out[(361,) * 10] == 1
    return header, out

def atomic(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)

def main():
    assert sha(HERE / "src/main.rs") == EXPECTED["source"]
    assert sha(HERE / "x5_four_d10_seeded_repair") == EXPECTED["binary"]
    assert sha(HERE / "results_independent_integer_replay.json") == EXPECTED["independent_replay"]
    seed = load("results_seed_build.json")
    first, second = load("results_first_prime.json"), load("results_second_prime.json")
    lift, independent, hostiles = load("results_characteristic_zero_lift.json"), load("results_independent_integer_replay.json"), load("results_hostile_tests.json")
    assert seed["status"] == "PASS_FOUR_EXACT_D10_TRANSPORT_SEEDS"
    assert first["status"] == second["status"] == "PASS_FOUR_GLOBAL_MODULAR_DUALS"
    assert lift["status"] == "PASS_FOUR_CHARACTERISTIC_ZERO_D10_DUAL_OBSTRUCTIONS"
    assert independent["status"] == "PASS_FOUR_CHARACTERISTIC_ZERO_D10_OBSTRUCTIONS"
    assert hostiles["status"] == "PASS_ALL_HOSTILES_REJECTED" and hostiles["test_count"] == 8
    assert [r["branch"] for r in first["records"]] == list(BRANCHES)
    assert [r["branch"] for r in second["records"]] == list(BRANCHES)
    exact_records = {r["branch"]: r for r in independent["records"]}
    records = []
    for branch, r0, r1 in zip(BRANCHES, first["records"], second["records"]):
        assert r0["branch"] == r1["branch"] == branch
        assert r0["selected_columns"] == r1["selected_columns"] and r0["dual_support"] == r1["dual_support"]
        assert r0["selected_sha256"] == r1["selected_sha256"]
        assert r0["selected_columns"] <= 200000 and r1["selected_columns"] <= 200000
        assert max(r0["elapsed_seconds"], r1["elapsed_seconds"]) < 180
        assert max(r0["peak_rss_kib"], r1["peak_rss_kib"]) < 8 * 1024 * 1024
        signed_maps = []
        for prime in PRIMES:
            header, modular = parse_dual(HERE / f"p{prime}_{branch}/dual.tsv")
            assert header == ["KRENN_X5_BLOCKER_D10_MODULAR_DUAL_V1", str(prime), str(len(modular)), "1"]
            signed_maps.append({row: value if value <= prime // 2 else value - prime for row, value in modular.items()})
        assert signed_maps[0] == signed_maps[1]
        header, integer = parse_dual(HERE / f"exact_lift_{branch}/integer_dual.tsv")
        assert header == ["KRENN_X5_BLOCKER_D10_PRIMITIVE_INTEGER_DUAL_V1", str(len(integer)), "1"]
        assert integer == signed_maps[0]
        exact = exact_records[branch]
        assert exact["support"] == len(integer) == r0["dual_support"]
        assert exact["target_coefficient"] == 1 and exact["pairing_failures"] == 0
        records.append({
            "branch": branch, "transported_violations": r0["transported_violation_count"],
            "selected_columns": r0["selected_columns"], "integer_support": len(integer),
            "integer_weight_set": sorted(set(integer.values())),
            "literal_incident_columns_replayed": exact["literal_incident_columns_replayed"],
            "p107_elapsed_seconds": r0["elapsed_seconds"], "p100_elapsed_seconds": r1["elapsed_seconds"],
            "peak_rss_kib": max(r0["peak_rss_kib"], r1["peak_rss_kib"]),
            "integer_dual_sha256": sha(HERE / f"exact_lift_{branch}/integer_dual.tsv"),
        })
    assert not any(path.name.startswith("d11") for path in HERE.iterdir())
    result = {
        "schema": "KRENN_X5_FOUR_D10_SEEDED_GATE_FINAL_AUDIT_V1",
        "status": "PASS_FOUR_EXACT_CHARACTERISTIC_ZERO_D10_OBSTRUCTIONS",
        "source_sha256": EXPECTED["source"], "binary_sha256": EXPECTED["binary"],
        "records": records, "two_safe_primes": list(PRIMES), "target": "t^10",
        "all_exact_target_coefficients": 1, "total_pairing_failures": 0,
        "column_cap": 200000, "per_branch_wall_seconds": 180, "per_branch_rss_gib": 8,
        "hostile_tests_passed": 8, "degree_eleven_launched": False,
    }
    atomic(HERE / "results_final_audit.json", result)
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
