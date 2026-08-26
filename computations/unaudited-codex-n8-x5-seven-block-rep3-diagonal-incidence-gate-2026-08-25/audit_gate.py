#!/usr/bin/env python3
"""Fail-closed audit of all five exact-Q rep3 incidence charts."""

from __future__ import annotations

import copy
import hashlib
import itertools
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
CHARTS = ("p00", "p01", "p10", "p11", "p12")
REPRESENTATIVES = ((0, 0), (0, 1), (1, 0), (1, 1), (1, 2))


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def orbit_representative(i, p, q):
    candidates = []
    for permutation in itertools.permutations(range(3)):
        if permutation[i] != 0:
            continue
        candidates.append((permutation[p], permutation[q]))
    answer = min(candidates)
    assert answer in REPRESENTATIVES
    return answer


def validate(result):
    assert result["schema"] == "KRENN_X5_REP3_DIAGONAL_INCIDENCE_AUDIT_V1"
    assert result["status"] == "PASS_REP3_ALL_RANKS_EXACT_Q"
    assert result["census"] == {"normalized_charts": 5, "modular_units": 5, "exact_Q_units": 5, "full_x5_equations_per_chart": 6561, "mathematically_closed_representatives": [3]}
    assert result["s3_normalization"]["all_27_coordinate_entry_cases_covered"] is True
    assert result["theorem"]["rank_zero_closed"] is True
    assert result["theorem"]["nonzero_ranks_closed"] is True
    assert result["scope"] == {"representative_3_only": True, "transport_to_other_representatives": False, "non_full_family": False, "broad_cegar": False}


def hostile(result, mutation):
    candidate = copy.deepcopy(result)
    mutation(candidate)
    try:
        validate(candidate)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


def main():
    metadata = json.loads((HERE / "gate_metadata.json").read_text())
    assert metadata["status"] == "PASS_INPUT_GENERATION"
    assert metadata["counts"] == {"variables": 100, "equations": 6586, "full_x5": 6561, "guard_after_elimination": 18, "incidence": 6, "saturation": 1}
    assert tuple(tuple(x) for x in metadata["s3_normalization"]["outside_entry_orbits"]) == REPRESENTATIVES
    runs = []
    for chart in CHARTS:
        if chart == "p00":
            modular_path = HERE / "results_modular_p00.json"
            q_path = HERE / "results_q_p00.json"
        else:
            modular_path = HERE / f"results_p32003_{chart}.json"
            q_path = HERE / f"results_Q_{chart}.json"
        modular = json.loads(modular_path.read_text())
        exact_q = json.loads(q_path.read_text())
        assert modular["status"] == "UNIT_IDEAL_MODULAR" and modular["mathematical_coverage"] is True
        assert exact_q["status"] == "UNIT_IDEAL_EXACT_Q" and exact_q["mathematical_coverage"] is True
        assert modular["input_sha256"] == metadata["inputs"][chart]["p32003"]["sha256"]
        assert exact_q["input_sha256"] == metadata["inputs"][chart]["Q"]["sha256"]
        runs.append({
            "chart": chart,
            "modular_result": modular_path.name,
            "modular_sha256": sha256(modular_path),
            "modular_wall_seconds": modular["wall_seconds"],
            "exact_Q_result": q_path.name,
            "exact_Q_sha256": sha256(q_path),
            "exact_Q_wall_seconds": exact_q["wall_seconds"],
        })

    cases = {(i, p, q): orbit_representative(i, p, q) for i, p, q in itertools.product(range(3), repeat=3)}
    assert len(cases) == 27 and set(cases.values()) == set(REPRESENTATIVES)
    result = {
        "schema": "KRENN_X5_REP3_DIAGONAL_INCIDENCE_AUDIT_V1",
        "status": "PASS_REP3_ALL_RANKS_EXACT_Q",
        "census": {"normalized_charts": 5, "modular_units": 5, "exact_Q_units": 5, "full_x5_equations_per_chart": 6561, "mathematically_closed_representatives": [3]},
        "runs": runs,
        "s3_normalization": {
            "action": "simultaneous permutation of the three colors on i and both A37 entry indices",
            "coordinate_normalization": "i maps to 0",
            "residual_stabilizer": "swap 1 and 2",
            "entry_orbit_representatives": [list(x) for x in REPRESENTATIVES],
            "all_27_coordinate_entry_cases_covered": True,
        },
        "theorem": {
            "rank_zero_closed": True,
            "rank_zero_reason": "A37=0 forces A36=0, so L67=0; nonzero full-family A67 makes cap67 active.",
            "nonzero_ranks_closed": True,
            "nonzero_reason": "A06*A37^T=0 makes P=Col(A06) proper and the A03=I pairing live. For each i and each possible nonzero A37 entry, the exact-Q incidence ideal is unit, proving not(e_i in P and e_i in ColSpan(A35,A37)); hence all three Kii are live.",
            "full_x5_and_guard_used": True,
        },
        "supersedes_pairing_only_manifest": "423b3186b76388d3a84ca79c18dcaa7fde0fcfcee7f25abbf70de699cc6605f3",
        "scope": {"representative_3_only": True, "transport_to_other_representatives": False, "non_full_family": False, "broad_cegar": False},
    }
    validate(result)
    tests = {
        "drop_Q_unit": hostile(result, lambda x: x["census"].__setitem__("exact_Q_units", 4)),
        "drop_normalized_case": hostile(result, lambda x: x["s3_normalization"].__setitem__("all_27_coordinate_entry_cases_covered", False)),
        "rank_overclaim_mutation": hostile(result, lambda x: x["theorem"].__setitem__("nonzero_ranks_closed", False)),
        "transport_overclaim": hostile(result, lambda x: x["scope"].__setitem__("transport_to_other_representatives", True)),
        "non_family_overclaim": hostile(result, lambda x: x["scope"].__setitem__("non_full_family", True)),
    }
    assert all(tests.values())
    result["hostile_tests"] = tests
    temporary = HERE / "results_rep3_incidence_audit.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_rep3_incidence_audit.json")
    print(json.dumps({"status": result["status"], "charts": 5, "Q_units": 5}, sort_keys=True))


if __name__ == "__main__":
    main()
