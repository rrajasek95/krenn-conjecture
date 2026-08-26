#!/usr/bin/env python3
"""Strict source-extracted ledger for authoritative D4--D12 artifacts."""

import argparse
import json
from pathlib import Path

from audit_affine251_orbit import sha256, validate_result


FILES = {
    4: ("results_d4_last_p1073741827.json", "results_d4_p1073741789.json", "results_d4_exact_dual_audit.json"),
    5: ("results_d5_p1073741827.json", "results_d5_p1073741789.json", "results_d5_exact_dual_audit.json"),
    6: ("results_d6_p1073741827.json", "results_d6_p1073741789.json", "results_d6_exact_dual_audit.json"),
    7: ("results_d7_p1073741827.json", "results_d7_p1073741789.json", "results_d7_exact_dual_audit.json"),
    8: ("results_d8_last_control.json", "results_d8_last_p1073741789_control.json", "results_d8_independent_audit.json"),
    9: ("results_d9_last_p1073741827.json", "results_d9_last_p1073741789.json", "results_d9_exact_dual_audit.json"),
    10: ("results_d10_last_p1073741827.json", "results_d10_last_p1073741789.json", "results_d10_exact_dual_audit.json"),
    11: ("results_d11_p1073741827.json", "results_d11_p1073741789.json", "results_d11_exact_dual_audit.json"),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    degrees = []
    for degree, names in FILES.items():
        paths = [args.root / name for name in names]
        assert all(path.exists() for path in paths)
        first, second = (json.loads(path.read_text()) for path in paths[:2])
        validate_result(first, degree)
        validate_result(second, degree)
        assert first["prime"] == 1073741827 and second["prime"] == 1073741789
        for key in ("status", "row_orbits", "column_orbits", "rank", "matrix_nnz", "member_mod_prime"):
            assert first[key] == second[key]
        audit = json.loads(paths[2].read_text())
        assert audit["status"] == "PASS" and audit["degree"] == degree
        assert audit["deep_referee"]["exact_char0_nonmembership"] is True
        degrees.append({
            "degree": degree,
            "status": "EXACT_CHAR0_NONMEMBER",
            "row_orbits": first["row_orbits"],
            "column_orbits": first["column_orbits"],
            "rank": first["rank"],
            "matrix_nnz": first["matrix_nnz"],
            "prime_results": [sha256(paths[0]), sha256(paths[1])],
            "exact_audit_sha256": sha256(paths[2]),
            "exact_dual_support": audit["deep_referee"]["exact_rational_dual_support"],
            "exact_dual_max_denominator": audit["deep_referee"]["exact_rational_dual_max_denominator"],
        })
    d12_result_path = args.root / "results_d12_p1073741827.json"
    d12_audit_path = args.root / "results_d12_incomplete_audit.json"
    d12_result = json.loads(d12_result_path.read_text())
    d12_audit = json.loads(d12_audit_path.read_text())
    assert d12_result["status"] == "INCOMPLETE_RESOURCE_GATE"
    assert d12_result["member_mod_prime"] is None and d12_result["rank"] == -1
    assert d12_audit["status"] == "PASS_INCOMPLETE_RESOURCE_GATE"
    result = {
        "schema": "KRENN_AFFINE251_EXACT_DEGREE_LEDGER_V1",
        "status": "EXACT_CHAR0_NONMEMBERSHIP_D4_D11_D12_RESOURCE_GATED",
        "degrees": degrees,
        "d12": {
            "status": "INCOMPLETE_RESOURCE_GATE",
            "mathematical_verdict": None,
            "row_orbits_discovered": d12_audit["row_orbits_discovered"],
            "column_orbits_discovered": d12_audit["column_orbits_discovered"],
            "row_frontier": d12_audit["row_frontier"],
            "column_frontier": d12_audit["column_frontier"],
            "result_sha256": sha256(d12_result_path),
            "audit_sha256": sha256(d12_audit_path),
        },
        "scope": "finite-degree homogeneous ideal membership for the single x67_01=1 affine cover",
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
