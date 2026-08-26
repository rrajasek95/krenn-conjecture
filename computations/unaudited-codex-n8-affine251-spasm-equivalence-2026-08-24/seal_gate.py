#!/usr/bin/env python3
"""Seal the bounded SpaSM experiment without upgrading an incomplete D11 run.

This script deliberately performs only a streaming audit of the retained SMS
files.  It never invokes SpaSM or the matrix exporter.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path

import audit_spasm_gate as gate


HERE = Path(__file__).resolve().parent
PRIME0 = 1_073_741_827
PRIME1 = 1_073_741_789
BUILD_SNAPSHOT = (
    HERE
    / "target/release/build/affine251-spasm-export-907d4950f29001f9/out/retained_main.rs"
)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            h.update(block)
    return h.hexdigest()


def pin_build_inputs() -> dict[str, dict[str, object]]:
    """Pin immutable inputs while detecting the post-build live-source drift."""
    out: dict[str, dict[str, object]] = {}
    for name, (path, expected) in gate.PINS.items():
        if name == "retained_source":
            continue
        actual = sha(path)
        assert actual == expected, f"stale pin {name}: {actual} != {expected}"
        out[name] = {"path": str(path.relative_to(gate.ROOT)), "sha256": actual}

    # build.rs changed only seven crate-level `//!` markers to `//` before
    # include!(). Reversing exactly those markers recovers the source bytes
    # that were compiled, including their authoritative SHA-256.
    assert sha(BUILD_SNAPSHOT) == "bd1977b8e82326cc1ca1e3c832f1fd59eb8d3e4e8facae9151dc4a43ba2e93cc"
    lines = BUILD_SNAPSHOT.read_text().splitlines()
    assert len(lines) > 7 and all(lines[i].startswith("//") for i in range(7))
    for i in range(7):
        lines[i] = "//!" + lines[i][2:]
    reconstructed = ("\n".join(lines) + "\n").encode()
    build_time_sha = hashlib.sha256(reconstructed).hexdigest()
    assert build_time_sha == gate.PINS["retained_source"][1]
    live_path = gate.PINS["retained_source"][0]
    out["retained_source_build_time"] = {
        "original_path": str(live_path.relative_to(gate.ROOT)),
        "original_sha256_at_build_and_d10_gate": build_time_sha,
        "sanitized_build_snapshot_path": str(BUILD_SNAPSHOT.relative_to(gate.ROOT)),
        "sanitized_build_snapshot_sha256": sha(BUILD_SNAPSHOT),
        "post_build_live_source_drift_observed_during_gate": True,
        "note": "live path is mutable and deliberately not treated as build provenance",
    }
    return out


def require_d10_pass(report: dict) -> None:
    assert report["schema"] == "KRENN_AFFINE251_SPASM_EQUIVALENCE_V1"
    assert report["status"] == "PASS" and report["degree"] == 10
    assert report["primes"] == [PRIME0, PRIME1]
    assert report["export"]["row_orbits"] == 36_475
    assert report["export"]["column_orbits"] == 2_120
    assert report["export"]["matrix_nnz"] == 101_283
    assert report["matrix_sha256"] == sha(HERE / "matrix_d10_integer_AT.sms")
    assert report["rhs_sha256"] == sha(HERE / "rhs_d10_target.sms")
    for prime in (PRIME0, PRIME1):
        run = report["spasm_runs"][str(prime)]
        assert run["rank"] == 2_014 and run["rhs_consistent"] is False
        assert run["elapsed_seconds"] < 300
        assert 0 < run["peak_rss_bytes"] < 8 * 1024**3
        assert run["solution_sha256"] == sha(HERE / f"solution_d10_p{prime}.sms")
    assert report["hostile_mutations_rejected"] == 6


def require_d11_fail_closed(report: dict) -> None:
    assert report["schema"] == "KRENN_AFFINE251_SPASM_GATE_FAILURE_V1"
    assert report["status"] == "GATE_FAILED_END_TO_END_WALL"
    assert report["degree"] == 11
    assert report["equivalence_accepted"] is False
    assert report["spasm_complete_primes"] == []
    assert report["spasm_incomplete_primes"] == [PRIME0]
    assert report["spasm_not_started_primes"] == [PRIME1]
    assert report["solution_artifacts"] == []
    export = report["export"]
    assert export["status"] == "PASS" and export["elapsed_seconds"] < 300
    assert export["row_orbits"] == 3_722_556
    assert export["column_orbits"] == 195_924
    assert export["matrix_nnz"] == 18_713_801
    assert report["matrix_sha256"] == sha(HERE / "matrix_d11_integer_AT.sms")
    assert report["rhs_sha256"] == sha(HERE / "rhs_d11_target.sms")
    assert report["incomplete_diagnostic"]["last_processed_row"] < export["column_orbits"]
    assert report["incomplete_diagnostic"]["rank_available"] is False
    assert report["incomplete_diagnostic"]["rhs_result_available"] is False
    contract = report["resource_contract"]
    assert contract["end_to_end_wall_seconds"] == 300
    assert contract["export_elapsed_seconds"] < 300
    assert 0 < contract["solver_budget_remaining_after_export_seconds"] < 32
    assert contract["acceptance_possible_when_solver_diagnostic_started"] is False
    assert report["retained_dual_audit"][str(PRIME0)]["all_columns_annihilated"] is True
    assert report["retained_dual_audit"][str(PRIME1)]["all_columns_annihilated"] is True


def hostile_selftests(d10: dict, d11: dict) -> int:
    mutations = []
    forged = copy.deepcopy(d10)
    forged["spasm_runs"][str(PRIME0)]["rank"] += 1
    mutations.append((require_d10_pass, forged))
    forged = copy.deepcopy(d10)
    forged["spasm_runs"][str(PRIME1)]["rhs_consistent"] = True
    mutations.append((require_d10_pass, forged))
    forged = copy.deepcopy(d10)
    forged["matrix_sha256"] = "0" * 64
    mutations.append((require_d10_pass, forged))
    forged = copy.deepcopy(d11)
    forged["status"] = "PASS"
    mutations.append((require_d11_fail_closed, forged))
    forged = copy.deepcopy(d11)
    forged["equivalence_accepted"] = True
    mutations.append((require_d11_fail_closed, forged))
    forged = copy.deepcopy(d11)
    forged["spasm_complete_primes"] = [PRIME0]
    mutations.append((require_d11_fail_closed, forged))
    forged = copy.deepcopy(d11)
    forged["solution_artifacts"] = ["forged.sms"]
    mutations.append((require_d11_fail_closed, forged))
    forged = copy.deepcopy(d11)
    forged["export"]["matrix_nnz"] -= 1
    mutations.append((require_d11_fail_closed, forged))
    forged = copy.deepcopy(d11)
    forged["retained_dual_audit"][str(PRIME1)]["all_columns_annihilated"] = False
    mutations.append((require_d11_fail_closed, forged))

    rejected = 0
    for validator, mutation in mutations:
        try:
            validator(mutation)
        except AssertionError:
            rejected += 1
    assert rejected == len(mutations)
    return rejected


def main() -> None:
    pins = pin_build_inputs()
    d10 = json.loads((HERE / "results_spasm_equivalence_d10.json").read_text())
    require_d10_pass(d10)

    metadata = json.loads((HERE / "export_d11.json").read_text())
    assert metadata["degree"] == 11 and metadata["status"] == "PASS"
    expected = {
        prime: json.loads((gate.AFF / f"results_d11_p{prime}.json").read_text())
        for prime in (PRIME0, PRIME1)
    }
    for prime, result in expected.items():
        assert result["degree"] == 11 and result["prime"] == prime
        assert result["rank"] == 194_006
        assert result["member_mod_prime"] is False
        assert result["row_orbits"] == metadata["row_orbits"]
        assert result["column_orbits"] == metadata["column_orbits"]
        assert result["matrix_nnz"] == metadata["matrix_nnz"]

    # Independent streaming check of every retained D11 matrix entry against
    # both retained separating duals.  This is not a SpaSM rank computation.
    dual_audit = gate.verify_matrix_and_duals(
        HERE / "matrix_d11_integer_AT.sms", metadata, 11, expected
    )

    stderr_path = HERE / f"spasm_d11_p{PRIME0}.stderr.log"
    stderr = stderr_path.read_text(errors="replace").replace("\r", "\n")
    progress = [(int(a), int(b), int(c)) for a, b, c in re.findall(
        r"\[pivots\]\s+(\d+) / (\d+) --- found (\d+) new", stderr
    )]
    assert progress and all(total == metadata["column_orbits"] for _, total, _ in progress)
    last_processed, total_rows, last_found = progress[-1]
    assert last_processed < total_rows
    assert not re.search(r"rank = \d+", stderr)
    assert "WARNING: no solution" not in stderr
    assert not list(HERE.glob("solution_d11*.sms"))
    assert not list(HERE.glob("solution_d11*.tmp"))
    assert not (HERE / f"spasm_d11_p{PRIME1}.stderr.log").exists()

    # File timestamps are preserved as diagnostic provenance only.  They are
    # not substituted for a mathematical result or a formal peak-RSS trace.
    diagnostic_seconds = stderr_path.stat().st_mtime - stderr_path.stat().st_birthtime
    processed_fraction = last_processed / total_rows
    linear_projection = diagnostic_seconds / processed_fraction
    failure = {
        "schema": "KRENN_AFFINE251_SPASM_GATE_FAILURE_V1",
        "status": "GATE_FAILED_END_TO_END_WALL",
        "degree": 11,
        "primes_required": [PRIME0, PRIME1],
        "equivalence_accepted": False,
        "spasm_complete_primes": [],
        "spasm_incomplete_primes": [PRIME0],
        "spasm_not_started_primes": [PRIME1],
        "solution_artifacts": [],
        "pins": pins,
        "exporter_sha256": sha(gate.EXPORTER),
        "matrix_sha256": sha(HERE / "matrix_d11_integer_AT.sms"),
        "rhs_sha256": sha(HERE / "rhs_d11_target.sms"),
        "export": metadata,
        "retained_validator_expectation": {
            str(prime): {"rank": expected[prime]["rank"], "member_mod_prime": False}
            for prime in (PRIME0, PRIME1)
        },
        "retained_dual_audit": dual_audit,
        "resource_contract": {
            "end_to_end_wall_seconds": 300,
            "rss_limit_gib": 8,
            "export_elapsed_seconds": metadata["elapsed_seconds"],
            "solver_budget_remaining_after_export_seconds": 300 - metadata["elapsed_seconds"],
            "acceptance_possible_when_solver_diagnostic_started": False,
            "solver_diagnostic_is_outside_acceptance_budget": True,
        },
        "incomplete_diagnostic": {
            "prime": PRIME0,
            "command_algorithm": "SpaSM solve default greedy alternating-cycle pivot search",
            "termination": "operator SIGTERM after decisive projection; diagnostic was outside the exhausted end-to-end acceptance budget",
            "elapsed_seconds_from_file_timestamps": diagnostic_seconds,
            "last_processed_row": last_processed,
            "total_rows": total_rows,
            "last_reported_new_pivots": last_found,
            "processed_fraction": processed_fraction,
            "linear_projected_seconds": linear_projection,
            "rank_available": False,
            "rhs_result_available": False,
            "stderr_sha256": sha(stderr_path),
            "stdout_sha256": sha(HERE / f"spasm_d11_p{PRIME0}.stdout.log"),
            "peak_rss": "not formally captured; external ps observations were below 0.4 GiB",
        },
        "stop_reason": (
            "The exact export consumed 268.459 of the 300 end-to-end seconds, leaving "
            "only 31.541 seconds; therefore D11 acceptance was already impossible when "
            "the solver diagnostic began. At the last diagnostic progress record only "
            "40454/195924 rows had been processed. No rank, "
            "residual, solution, or SpaSM equivalence is claimed for D11."
        ),
        "d12_launched": False,
    }
    require_d11_fail_closed(failure)
    failure_path = HERE / "results_spasm_equivalence_d11_gate_failure.json"
    failure_path.write_text(json.dumps(failure, indent=2, sort_keys=True) + "\n")

    audit = {
        "schema": "KRENN_AFFINE251_SPASM_GATE_FINAL_AUDIT_V1",
        "status": "PASS_FAIL_CLOSED",
        "d10_status": "PASS_EXACT_EQUIVALENCE_TWO_PRIMES",
        "d11_status": "GATE_FAILED_NO_EQUIVALENCE_CLAIM",
        "d10_result_sha256": sha(HERE / "results_spasm_equivalence_d10.json"),
        "d11_failure_sha256": sha(failure_path),
        "hostile_mutations_rejected": hostile_selftests(d10, failure),
        "scope": {"d10": "accepted", "d11": "not accepted", "d12": "not launched"},
    }
    (HERE / "results_final_audit.json").write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
