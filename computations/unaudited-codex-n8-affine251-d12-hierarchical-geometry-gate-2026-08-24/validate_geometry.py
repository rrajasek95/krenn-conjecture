#!/usr/bin/env python3
import argparse
import json


def validate(value):
    assert value["status"] == "PASS_EXACT_NONPROMOTION"
    assert value["verdict"] == "NO_PROMOTION_TIMING_NOT_STABLE"
    assert value["promotion"] is False
    assert value["continued_beyond_round660"] is False
    assert value["run_count"] == 15
    assert value["all_checkpoints_byte_identical"] is True
    assert value["all_equations_verified"] is True
    assert value["fixture"]["equations"] == 246321
    assert value["fixture"]["candidate_support"] == 352
    assert value["best_observed"]["workers"] == 16
    assert value["best_observed"]["merge_arity"] == 8
    assert value["best_observed"]["checkpoint_sha256"] == value["fixture"]["checkpoint_sha256"]
    assert value["best_observed"]["speedup"] > 2.61
    assert value["repeated_16x8_median"]["fair_solve_seconds"] > value["sealed_reference"]["fair_solve_seconds"]
    assert value["normalized_16x8"]["speedup"] < value["sealed_reference"]["speedup"]
    assert value["normalized_16x8"]["speedup"] < 2.61
    for record in value["records"]:
        assert record["checkpoint_sha256"] == value["fixture"]["checkpoint_sha256"]
        assert record["total_seconds"] < 120
        assert record["peak_rss_bytes"] < 36 * 1024**3
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    value = json.load(open(args.input))
    validate(value)
    print(json.dumps({"status": "PASS", "promotion": False, "verdict": value["verdict"]}, sort_keys=True))


if __name__ == "__main__":
    main()
