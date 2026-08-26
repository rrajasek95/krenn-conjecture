#!/usr/bin/env python3
"""Fail-closed audit of the rep1 orientation/census and first modular gate."""

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
CHARTS = ((0, 0), (0, 1), (1, 0), (1, 1), (1, 2))


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def normalize(i, p, q):
    candidates = []
    for permutation in itertools.permutations(range(3)):
        if permutation[i] == 0:
            candidates.append((permutation[p], permutation[q]))
    return min(candidates)


def validate(result):
    assert result["schema"] == "KRENN_X5_REP1_DIAGONAL_INCIDENCE_AUDIT_V1"
    assert result["status"] == "FAIL_CLOSED_P00_WALL_ZERO_COVERAGE"
    assert result["input_generation"] == "PASS"
    assert result["orientation_census"] == "PASS"
    assert result["coverage"] == {"modular_units": 0, "exact_Q_units": 0, "representative_1_closed": False}
    assert result["scope"] == {"representative_1_only": True, "transport": False, "rep5": False}


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
    assert metadata["schema"] == "KRENN_X5_REP1_DIAGONAL_INCIDENCE_GATE_V1"
    assert metadata["status"] == "PASS_INPUT_GENERATION_AND_ORIENTATION_CENSUS"
    assert metadata["representative_id"] == 1
    assert metadata["support"] == {
        "added": ["06", "13", "17", "25", "26", "46", "47"],
        "fixed": ["03", "16", "27", "45"],
        "star_terms": [
            [1, 6, "switched", [0, 6], [1, 3]],
            [5, 6, "switched", [0, 6], [3, 5]],
        ],
        "supported_matchings": 12,
        "variable": ["04", "12", "35", "67"],
    }
    assert metadata["source_orientation"] == {
        "P": "Col(A06)",
        "Q": "ColSpan(A13^T,A35)",
        "carrier": "A06^T*K*[A13^T|A35]",
        "elimination": "A46=-A47*A26^T",
        "guard": ["A06*A47^T=0", "(I-A17*A26)*A47^T=0"],
        "incidence": ["A06*x=e0", "A13^T*y+A35*z=e0"],
    }
    assert metadata["counts"] == {"equations": 6586, "full_x5": 6561, "guard_after_elimination": 18, "incidence": 6, "saturation": 1, "variables": 100}
    assert metadata["parent_full_x5_digest"] == "61640fb492640847a58cf9f5e2f1dbc3f381736d7909325f35b2dfffb211d5eb"
    cases = {(i, p, q): normalize(i, p, q) for i, p, q in itertools.product(range(3), repeat=3)}
    assert len(cases) == 27 and set(cases.values()) == set(CHARTS)
    assert metadata["s3_normalization"]["all_27_cases_covered"] is True
    assert tuple(tuple(item) for item in metadata["s3_normalization"]["outside_entry_orbits"]) == CHARTS
    for chart in ("p00", "p01", "p10", "p11", "p12"):
        for ring in ("p32003", "Q"):
            record = metadata["inputs"][chart][ring]
            assert sha256(HERE / record["path"]) == record["sha256"]

    run = json.loads((HERE / "results_modular_p00.json").read_text())
    assert run["schema"] == "KRENN_X5_REP1_DIAGONAL_INCIDENCE_MODULAR_P00_V1"
    assert run["status"] == "FAIL_CLOSED_RESOURCE_GATE"
    assert run["termination"] == "WALL_CAP_60"
    assert run["mathematical_coverage"] is False and run["Q_launched"] is False
    assert run["rss_cap_bytes"] == 8 * 1024**3 and run["observed_peak_rss_bytes"] < run["rss_cap_bytes"]
    assert run["input_sha256"] == metadata["inputs"]["p00"]["p32003"]["sha256"]
    assert "INPUT_GENERATORS=6586" in run["stdout"]
    assert "STATUS=UNIT_IDEAL" not in run["stdout"] and "STATUS=NONUNIT_OR_UNRESOLVED" not in run["stdout"]

    result = {
        "schema": "KRENN_X5_REP1_DIAGONAL_INCIDENCE_AUDIT_V1",
        "status": "FAIL_CLOSED_P00_WALL_ZERO_COVERAGE",
        "input_generation": "PASS",
        "orientation_census": "PASS",
        "run": {
            "result": "results_modular_p00.json",
            "result_sha256": sha256(HERE / "results_modular_p00.json"),
            "wall_seconds": run["wall_seconds"],
            "peak_rss_bytes": run["observed_peak_rss_bytes"],
            "termination": run["termination"],
        },
        "coverage": {"modular_units": 0, "exact_Q_units": 0, "representative_1_closed": False},
        "next_obligation": "smaller exact quotient or separately authorized wider p00 modular gate; Q remains barred",
        "scope": {"representative_1_only": True, "transport": False, "rep5": False},
    }
    validate(result)
    tests = {
        "overclaim_modular_unit": hostile(result, lambda item: item["coverage"].__setitem__("modular_units", 1)),
        "overclaim_closed": hostile(result, lambda item: item["coverage"].__setitem__("representative_1_closed", True)),
        "transport_overclaim": hostile(result, lambda item: item["scope"].__setitem__("transport", True)),
        "rep5_overclaim": hostile(result, lambda item: item["scope"].__setitem__("rep5", True)),
        "orientation_drop": hostile(result, lambda item: item.__setitem__("orientation_census", "FAIL")),
    }
    assert all(tests.values())
    result["hostile_tests"] = tests
    temporary = HERE / "results_rep1_incidence_audit.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_rep1_incidence_audit.json")
    print(json.dumps({"status": result["status"], "hostiles": len(tests), "Q_units": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
