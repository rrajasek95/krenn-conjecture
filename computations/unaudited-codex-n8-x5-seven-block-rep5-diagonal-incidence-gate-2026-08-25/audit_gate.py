#!/usr/bin/env python3
"""Fail-closed audit of the stopped rep5 incidence gate."""

from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def validate(result):
    assert result["schema"] == "KRENN_X5_REP5_DIAGONAL_INCIDENCE_AUDIT_V1"
    assert result["status"] == "INCOMPLETE_MODULAR_WALL_GATE"
    assert result["mathematical_coverage"] is False
    assert result["representative_5_closed"] is False
    assert result["attempted_charts"] == ["p00_modular"]
    assert result["Q_runs"] == 0 and result["unattempted_charts"] == ["p01", "p10", "p11", "p12"]
    assert result["scope"] == {"representative_5_only": True, "transport": False, "other_representatives": False, "non_full_family": False}


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
    run = json.loads((HERE / "results_p32003_p00.json").read_text())
    assert metadata["status"] == "PASS_INPUT_GENERATION_AND_REP3_BYTE_REPRODUCTION"
    assert metadata["representative_id"] == 5
    assert metadata["support"]["supported_matchings"] == 12
    assert metadata["source_orientation"]["carrier"] == "A06^T*K*[A35|A37]"
    assert metadata["s3_normalization"]["complete"] is True
    assert run["status"] == "FAIL_CLOSED_RESOURCE_GATE"
    assert run["termination"] == "WALL_CAP_60"
    assert run["mathematical_coverage"] is False
    assert run["input_sha256"] == metadata["inputs"]["p00"]["p32003"]["sha256"]
    for chart in ("p01", "p10", "p11", "p12"):
        assert not (HERE / f"results_p32003_{chart}.json").exists()
        assert not (HERE / f"results_Q_{chart}.json").exists()
    assert not (HERE / "results_Q_p00.json").exists()
    result = {
        "schema": "KRENN_X5_REP5_DIAGONAL_INCIDENCE_AUDIT_V1",
        "status": "INCOMPLETE_MODULAR_WALL_GATE",
        "mathematical_coverage": False,
        "representative_5_closed": False,
        "attempted_charts": ["p00_modular"],
        "Q_runs": 0,
        "unattempted_charts": ["p01", "p10", "p11", "p12"],
        "resource_evidence": {"wall_cap_seconds": 60, "observed_wall_seconds": run["wall_seconds"], "peak_rss_bytes": run["observed_peak_rss_bytes"], "termination": run["termination"]},
        "preserved_exact_design": {"variables": 100, "equations": 6586, "charts": 5, "parent_digest": metadata["parent_full_x5_digest"], "source_orientation": metadata["source_orientation"], "rep3_byte_reproduction": True},
        "next_obligation": "A separately authorized wider modular p00 gate or an algebraically smaller rep5 incidence quotient; exact Q remains forbidden until modular unit.",
        "scope": {"representative_5_only": True, "transport": False, "other_representatives": False, "non_full_family": False},
        "pins": {"metadata_sha256": sha256(HERE / "gate_metadata.json"), "modular_p00_result_sha256": sha256(HERE / "results_p32003_p00.json")},
    }
    validate(result)
    tests = {
        "coverage_overclaim": hostile(result, lambda x: x.__setitem__("mathematical_coverage", True)),
        "closure_overclaim": hostile(result, lambda x: x.__setitem__("representative_5_closed", True)),
        "Q_overclaim": hostile(result, lambda x: x.__setitem__("Q_runs", 1)),
        "chart_overclaim": hostile(result, lambda x: x["attempted_charts"].append("p01_modular")),
        "transport_overclaim": hostile(result, lambda x: x["scope"].__setitem__("transport", True)),
    }
    assert all(tests.values())
    result["hostile_tests"] = tests
    temporary = HERE / "results_rep5_incidence_audit.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_rep5_incidence_audit.json")
    print(json.dumps({"status": result["status"], "coverage": False, "Q_runs": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
