#!/usr/bin/env python3
import argparse
import json


def validate(value):
    assert value["status"] == "PASS_EXACT_ONE_ROUND_PORTFOLIO_AUDIT"
    assert value["input_state"] == {"prime": 1073741827, "round": 849, "columns": 460676, "support": 312}
    assert value["output_state"] == {"prime": 1073741827, "round": 850, "columns": 461464, "support": 327}
    assert value["round849_input_all_column_replay"] == {
        "columns": 460676, "terms": 46796079, "verification_failures": 0
    }
    assert value["portfolio_compared"] == {
        "strategies": ["repair", "cold"], "pivots": ["first", "last", "rare"],
        "task_count": 6, "parallel": True
    }
    assert value["selected_strategy"] == "cold" and value["selected_pivot"] == "rare"
    assert value["cold_rare_remains_selected"] is True
    assert value["portfolio_selected_control_checkpoint_identical"] is True
    assert value["portfolio_selected_control_vector_cache_identical"] is True
    assert value["semantic_round_record_identical_excluding_timings"] is True
    assert value["mathematical_artifacts_differ_only_by_audit_configuration_and_timing_metadata"] is True
    assert value["production_mutated"] is False and value["continued_beyond_round850"] is False
    assert value["global_annihilation"] is None and value["target_pairing"] is None
    assert value["portfolio"]["peak_rss_kib"] < 36 * 1024 * 1024
    assert value["selected_control"]["peak_rss_kib"] < 36 * 1024 * 1024
    assert value["portfolio"]["hashes"]["checkpoint.bin"] == value["selected_control"]["hashes"]["checkpoint.bin"]
    assert value["portfolio"]["hashes"]["vectors.bin"] == value["selected_control"]["hashes"]["vectors.bin"]
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    value = json.load(open(args.input))
    validate(value)
    print(json.dumps({"status": "PASS", "selected": "cold/rare", "round": 850}, sort_keys=True))


if __name__ == "__main__":
    main()
