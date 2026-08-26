#!/usr/bin/env python3
"""Check the bounded global-column-interner prototype against inline rows."""

from pathlib import Path
import argparse
import hashlib
import json


HERE = Path(__file__).resolve().parent
INLINE = HERE / "results_lazy_all_interner_forward_r1_rss.json"
INTERNED = HERE / "results_lazy_all_interner_r1_rss.json"
RESULTS = HERE / "results_joint_cegar_column_interner.json"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def logical_digest(value):
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def audit():
    inline = json.loads(INLINE.read_text())
    interned = json.loads(INTERNED.read_text())
    require(inline["column_storage"] == "inline_key", "inline label changed")
    require(interned["column_storage"] == "global_u32_interner",
            "interner label changed")
    equal_fields = (
        "prime", "source_words", "initial_source_word_count",
        "available_generator_pool_words", "initial_target_touching_rows",
        "initial_independent_rows", "rounds", "terminal", "final_rank",
        "final_basis_nnz", "final_remainder_terms", "target_reduced_to_zero",
        "terminal_modular_dual_support", "terminal_integer_crossing_translations",
        "terminal_integer_crossing_words", "terminal_integer_target_pairing",
        "final_remainder_sha256",
    )
    mismatches = {
        field: [inline.get(field), interned.get(field)]
        for field in equal_fields if inline.get(field) != interned.get(field)
    }
    require(not mismatches, f"interner changed exact algebra: {mismatches}")
    first = interned["rounds"][0]
    require((first["crossing_candidates"], first["crossing_rows_selected"],
             first["independent_rows_added"], first["rank_after"]) ==
            (12708, 261, 256, 124624), "round-one guard changed")
    require(interned["final_interned_columns"] == 4585601,
            "interner distinct-column count changed")
    require(interned["final_column_hash_collisions"] == 0,
            "unexpected exact-fingerprint collision")
    require(interned["final_basis_nnz"] == 12939819,
            "interner row-nnz count changed")
    elapsed_ratio = interned["elapsed_ms"] / inline["elapsed_ms"]
    require(elapsed_ratio > 2, "prototype no longer crosses the stop threshold")
    result = {
        "status": "PASS exact prototype; RETIRE because slowdown exceeds 2x",
        "rounds": 1,
        "rank": interned["final_rank"],
        "basis_nnz": interned["final_basis_nnz"],
        "distinct_interned_columns": interned["final_interned_columns"],
        "fingerprint_collisions": interned["final_column_hash_collisions"],
        "distinct_column_fraction": round(
            interned["final_interned_columns"] / interned["final_basis_nnz"], 9
        ),
        "inline_elapsed_ms": inline["elapsed_ms"],
        "interned_elapsed_ms": interned["elapsed_ms"],
        "elapsed_ratio": round(elapsed_ratio, 9),
        "rss_verdict": (
            "unavailable: sandboxed /usr/bin/time -l could not read kern.clockrate"
        ),
        "scope": (
            "Exact round-one comparison with forward lex order. The >2x stop "
            "criterion fires, so no r8/r16 or long decision run was performed."
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
        raise RuntimeError("stored column-interner audit changed")
    print(text, end="")


if __name__ == "__main__":
    main()
