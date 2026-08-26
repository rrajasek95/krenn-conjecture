#!/usr/bin/env python3
import argparse
import json


def validate(value):
    assert value["status"] == "PASS_EXACT_REPRODUCIBLE_PROMOTION"
    assert value["verdict"] == "PROMOTE_16_SHARD_RANK_MATERIALIZATION"
    assert value["promotion"] is True
    assert value["continued_beyond_round660"] is False
    assert value["run_count"] == 9
    assert value["all_checkpoints_byte_identical"] is True
    assert value["all_equations_verified"] is True
    assert all(value["ordering_contract"].values())
    assert value["memory_contract"]["maximum_observed_peak_rss_bytes"] < value["memory_contract"]["hard_rss_bytes"]
    assert value["recommended_configuration"] == {
        "workers": 16, "merge_arity": 2, "rank_mode": "sharded", "rank_shards": 16
    }
    assert value["improvement"]["rank_phase_factor"] > 3.5
    assert value["improvement"]["fair_solve_factor"] > 3.0
    assert value["improvement"]["sequential_speedup"] > 8.0
    assert value["promoted_median"]["peak_rss_bytes"] < 36 * 1024**3
    assert value["promoted_median"]["fair_solve_seconds"] < value["baseline_median"]["fair_solve_seconds"]
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
    print(json.dumps({"status": "PASS", "promotion": True, "verdict": value["verdict"]}, sort_keys=True))


if __name__ == "__main__":
    main()
