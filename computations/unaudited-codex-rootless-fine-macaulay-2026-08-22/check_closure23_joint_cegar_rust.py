#!/usr/bin/env python3
"""Cross-check the dependency-free Rust closure23 exchange audit."""

from pathlib import Path
import argparse
import hashlib
import json


HERE = Path(__file__).resolve().parent
PYTHON = HERE / "results_closure22_plus_00000200_joint_cegar.json"
RUST = HERE / "results_closure22_plus_00000200_joint_cegar_rust.json"
RUST64 = HERE / "results_closure22_plus_00000200_joint_cegar_rust_64.json"
RESULTS = HERE / "results_closure23_rust_crosscheck.json"


FIELDS = (
    "prime",
    "source_words",
    "added_complete_profile71_orbit",
    "extra_words",
    "initial_target_touching_rows",
    "initial_independent_rows",
    "rounds",
    "terminal",
    "final_rank",
    "final_remainder_terms",
    "target_reduced_to_zero",
    "terminal_modular_dual_support",
    "terminal_integer_dual_balanced_max_abs",
    "terminal_integer_crossing_translations",
    "terminal_integer_crossing_words",
    "terminal_integer_max_abs_translation_pairing",
    "terminal_integer_target_pairing",
    "terminal_integer_is_full_semigroup_separator",
    "terminal_integer_dual",
    "final_remainder_sha256",
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def logical_digest(value):
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def audit():
    python = json.loads(PYTHON.read_text())
    rust = json.loads(RUST.read_text())
    rust64 = json.loads(RUST64.read_text())

    mismatches = {
        field: {"python": python.get(field), "rust": rust.get(field)}
        for field in FIELDS
        if python.get(field) != rust.get(field)
    }
    require(not mismatches, f"Rust/Python terminal mismatch: {mismatches}")
    require(len(python["rounds"]) >= 64, "Python reference has fewer than 64 rounds")
    require(rust64["rounds"] == python["rounds"][:64],
            "Rust max64 ledger differs from Python prefix")
    require(rust64["final_rank"] == python["rounds"][63]["rank_after"],
            "Rust max64 rank differs")
    require(rust64["terminal_modular_dual_support"] ==
            python["rounds"][64]["dual_support"],
            "Rust max64 terminal dual is not Python round65 dual")
    require(rust64["final_remainder_sha256"] == python["final_remainder_sha256"],
            "Rust max64 remainder differs")
    require((len(rust["rounds"]), rust["final_rank"],
             rust["terminal_modular_dual_support"],
             rust["terminal_integer_dual_balanced_max_abs"],
             rust["terminal_integer_target_pairing"],
             rust["terminal_integer_crossing_translations"]) ==
            (100, 133968, 156, 4, 1, 0), "terminal must-fire stats changed")

    result = {
        "status": "PASS Rust closure23 matches Python through 64 rounds and terminal",
        "python_result_sha256": hashlib.sha256(PYTHON.read_bytes()).hexdigest(),
        "rust_result_sha256": hashlib.sha256(RUST.read_bytes()).hexdigest(),
        "rust64_result_sha256": hashlib.sha256(RUST64.read_bytes()).hexdigest(),
        "rounds_cross_checked": 64,
        "terminal_rounds": len(rust["rounds"]),
        "terminal_rank": rust["final_rank"],
        "terminal_remainder_terms": rust["final_remainder_terms"],
        "terminal_dual_support": rust["terminal_modular_dual_support"],
        "terminal_integer_dual_max_abs": rust[
            "terminal_integer_dual_balanced_max_abs"
        ],
        "terminal_integer_target_pairing": rust[
            "terminal_integer_target_pairing"
        ],
        "terminal_integer_crossings": rust[
            "terminal_integer_crossing_translations"
        ],
        "rust_elapsed_ms": rust["elapsed_ms"],
        "scope": (
            "Exact comparison of the fixed closure22+00000200 word set. "
            "The first 64 round ledgers and the complete 100-round terminal "
            "state agree field-for-field."
        ),
    }
    result["logical_sha256"] = logical_digest(result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = audit()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        RESULTS.write_text(text)
    if args.check_results and RESULTS.read_text() != text:
        raise RuntimeError("stored Rust/Python cross-check changed")
    print(text, end="")


if __name__ == "__main__":
    main()

