#!/usr/bin/env python3
"""Replay the finite guards for the lazy all-X5 CEGAR benchmarks."""

from pathlib import Path
import argparse
import hashlib
import json


HERE = Path(__file__).resolve().parent
CAP256 = HERE / "results_lazy_all_mixed_x5_cap256_joint_cegar_rust_p32003.json"
CAP2048 = HERE / "results_lazy_all_mixed_x5_cap2048_timeout.json"
CAP8192 = HERE / "results_lazy_all_mixed_x5_cap8192_memory_stop.json"
REVERSE = HERE / "results_lazy_all_mixed_x5_cap8192_reverse_pivot_stop.json"
FORWARD_FILL = HERE / "results_lazy_all_mixed_x5_cap8192_forward_r3_fill.json"
RESULTS = HERE / "results_lazy_all_x5_cegar_checks.json"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(value):
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def audit():
    small = load(CAP256)
    medium = load(CAP2048)
    large = load(CAP8192)
    reverse = load(REVERSE)
    forward = load(FORWARD_FILL)

    require(small["prime"] == 32003, "cap256 prime changed")
    require(small["lazy_pool_kind"] == "all_6558_mixed_X5",
            "cap256 is not the full mixed-word pool")
    require((small["initial_source_word_count"],
             small["available_generator_pool_words"],
             small["initial_independent_rows"]) == (22, 6558, 124368),
            "cap256 initial interface changed")
    require(small["indexed_scanner_round1_crosscheck"],
            "indexed/direct round-one guard missing")
    require(len(small["rounds"]) == 256, "cap256 round count changed")
    require(small["rounds"][0]["crossing_candidates"] == 12708,
            "round-one crossing census changed")
    require(small["rounds"][0]["crossing_rows_selected"] == 261,
            "round-one independent-cap scan count changed")
    require(all(row["independent_rows_added"] == 256
                for row in small["rounds"]),
            "a cap256 round did not add 256 independent rows")
    require(small["final_rank"] == 124368 + 256 * 256 == 189904,
            "cap256 final rank changed")
    require((small["terminal"], small["final_remainder_terms"]) ==
            ("round cap", 13636), "cap256 must remain explicitly partial")
    scan = small["all_word_scan"]
    require((scan["mixed_words"], scan["modular_crossing_words"],
             scan["modular_crossing_translations"],
             scan["modular_cheapest_word"],
             scan["modular_cheapest_word_crossings"]) ==
            (6558, 5904, 3609752, "10222210", 1),
            "cap256 terminal crossing census changed")

    require(medium["status"].startswith("STOPPED"),
            "cap2048 stopped guard missing")
    require(medium["all_completed_rounds_added_full_cap"],
            "cap2048 full-batch guard failed")
    require(medium["final_partial_rank"] ==
            medium["initial_rank"] + medium["completed_rounds"] * 2048 ==
            454096, "cap2048 rank ledger changed")
    require(medium["last_completed_round"]["closure_elapsed_seconds"] >= 1200,
            "cap2048 did not reach its hard wall gate")
    require(medium["inference"].startswith("none"),
            "cap2048 partial run lost its no-inference guard")

    require(large["status"].startswith("STOPPED"),
            "cap8192 stopped guard missing")
    require(large["final_partial_rank"] ==
            large["initial_rank"] + large["completed_rounds"] * 8192 ==
            320976, "cap8192 rank ledger changed")
    require(large["memory_gate"]["rss_kib"] > 16 * 1024 * 1024,
            "cap8192 did not cross the recorded 16 GiB gate")
    require(large["inference"].startswith("none"),
            "cap8192 partial run lost its no-inference guard")

    require(reverse["pivot_order"] == "reverse_lex",
            "reverse benchmark pivot label changed")
    require(reverse["completed_rounds"] == 3,
            "reverse benchmark completed-round guard changed")
    require(reverse["interrupted_round"]["active_seconds_lower_bound"] > 120,
            "reverse benchmark did not cross the round gate")
    require(forward["pivot_order"] == "forward_lex",
            "forward fill benchmark pivot label changed")
    require((forward["rounds"][-1]["rank_after"],
             forward["rounds"][-1]["basis_nnz_after"]) ==
            (148944, 20951696), "forward r3 fill profile changed")
    require((reverse["last_completed_rank"],
             reverse["last_completed_basis_nnz"]) ==
            (141018, 128306549), "reverse r3 fill profile changed")
    fill_ratio = (
        reverse["last_completed_basis_nnz"] /
        forward["rounds"][-1]["basis_nnz_after"]
    )
    time_ratio = reverse["rounds"][-1]["elapsed_seconds"] / 7.06
    require(fill_ratio > 6 and time_ratio > 15,
            "reverse-pivot retirement margins disappeared")

    evidence = {
        "status": "PASS lazy all-X5 CEGAR finite guards",
        "indexed_direct_round1_candidates": 12708,
        "cap256": {
            "rounds": 256,
            "rank": 189904,
            "live_crossing_words": 5904,
            "live_crossing_translations": 3609752,
        },
        "cap2048": {
            "rounds": 161,
            "rank": 454096,
            "stop": "20-minute gate",
        },
        "cap8192": {
            "rounds": 24,
            "rank": 320976,
            "stop": "RSS over 16 GiB",
        },
        "reverse_pivot": {
            "rounds": 3,
            "fill_ratio_vs_forward_r3": round(fill_ratio, 6),
            "time_ratio_vs_forward_r3": round(time_ratio, 6),
            "verdict": "retired",
        },
        "scope": (
            "Exact finite-field guards for the frozen degree-13 joint "
            "edge/colour semigroup. All decision runs are nonterminal."
        ),
    }
    evidence["logical_sha256"] = digest(evidence)
    return evidence


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
        raise RuntimeError("stored lazy-all CEGAR checks changed")
    print(text, end="")


if __name__ == "__main__":
    main()
