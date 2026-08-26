#!/usr/bin/env python3
"""Exact finite-contraction test for all iterated extensions of direct D10."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
RECURRENCE = REPO / "computations/unaudited-codex-n8-x5-four-dual-degree-recurrence-audit-2026-08-25/audit_recurrence.py"
CERTIFICATE = REPO / "computations/unaudited-codex-n8-x5-four-d10-seeded-support-repair-2026-08-25/exact_lift_direct/integer_dual.tsv"
PINS = {
    "recurrence_source": "b0210a9c8a4a6361f4519aa91930563424fdca5f3d09ebb20e5425e6b2bdb2f9",
    "certificate": "c639faa986903b66d003dc4513bb9ad029f5b0027dd15714d8c5449a494c8246",
    "provider": "53850c4224fcc901bb5bd0d4c5be58d92ae4f4fb04bfdc887bc4492f4dd41d6c",
}


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    assert sha(RECURRENCE) == PINS["recurrence_source"]
    assert sha(CERTIFICATE) == PINS["certificate"]
    spec = importlib.util.spec_from_file_location("recurrence", RECURRENCE)
    recurrence = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recurrence)
    generators = recurrence.load_provider("direct")
    assert recurrence.PROVIDER_SHA["direct"] == PINS["provider"]
    lines = CERTIFICATE.read_text().splitlines()
    assert lines[0].split("\t") == ["KRENN_X5_BLOCKER_D10_PRIMITIVE_INTEGER_DUAL_V1", "243", "1"]
    dual = {}
    for line in lines[1:]:
        kind, raw, raw_value = line.split("\t")
        row, value = tuple(map(int, raw.split(","))), int(raw_value)
        assert kind == "ROW" and len(row) == 10 and row not in dual
        dual[row] = value
    assert dual[(361,) * 10] == 1 and set(dual.values()) <= {-1, 1}
    by_contraction, failures = recurrence.induction_layer_audit(generators, dual)
    assert by_contraction == {
        2: {"candidates": 491, "failures": 491},
        4: {"candidates": 615, "failures": 615},
    }
    assert len(failures) == 1_106
    first = recurrence.simplify_failure(failures[0])
    assert first == {
        "generator": 0,
        "generator_degree": 4,
        "contraction_k": 2,
        "t_free_multiplier": "0,0,117,117,216,216,225,225",
        "pairing": -1,
        "realized": [{
            "row": "0,0,117,117,216,216,225,225,361,361",
            "generator_coefficient": -1,
            "dual_weight": 1,
            "contribution": -1,
        }],
    }
    result = {
        "schema": "KRENN_X5_DIRECT_D10_FINITE_CONTRACTION_AUDIT_V1",
        "status": "PASS_EXACT_NEGATIVE_ALL_DEGREE_TEST",
        "certificate_sha256": PINS["certificate"],
        "certificate_support": len(dual),
        "target_coefficient": dual[(361,) * 10],
        "direct_d10_to_d11_c1_transport_failures": 0,
        "by_contraction": {str(key): value for key, value in by_contraction.items()},
        "total_contraction_failures": len(failures),
        "first_failure": first,
        "all_iterated_t_extensions_proved": False,
        "interpretation": "D10-to-D11 works only because C1 is disjoint; C2 and C4 disprove induction beyond one step",
        "degree_twelve_read": False,
    }
    temporary = HERE / "results_d10_direct_contraction_audit.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_d10_direct_contraction_audit.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
