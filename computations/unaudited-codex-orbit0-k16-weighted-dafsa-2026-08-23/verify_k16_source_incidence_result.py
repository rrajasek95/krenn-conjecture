#!/usr/bin/env python3
"""Small independent guard for the frozen K16 source-incidence census."""

import argparse
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results_k16_source_incidence.json"
DAFSA_RESULT = HERE / "results_k16_weighted_dafsa.json"
BINARY = HERE / "weighted_k16_literal_orbits.dafsa"


def digest(path):
    h = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = json.loads(RESULT.read_text())
    dafsa = json.loads(DAFSA_RESULT.read_text())
    count = result["target_touching_source_column_H_orbits"]
    if args.mutate:
        count -= 1
    require(count == 98_609_090, "hostile column-count mutation fired")
    require(result["input_terminal_H_orbits"] == 1_848_174
            and result["first_terminal_index_reaching_2000001_column_orbits"] == 37_910
            and result["complete_terminal_pass"] is True
            and result["rank_solve_launched"] is False
            and result["lower_frontier_expansion_launched"] is False,
            "incidence scope/count guard changed")
    automaton = result["column_language_automaton"]
    require(result["raw_inverse_incidence_occurrences"] == 137_311_379
            and automaton["global_hash_set_materialized"] is False
            and automaton["external_sort_runs"] == 69
            and automaton["sum_of_run_local_unique_keys"] == 112_332_174
            and (automaton["states"], automaton["arcs"], automaton["root_state"])
            == (39_763_164, 71_283_240, 39_763_163)
            and automaton["root_language_count"] == 98_609_090,
            "column-language automaton changed")
    require(result["prefix_control"] == {
        "terminal_H_orbits": 10_000,
        "raw_literal_incidence_occurrences": 731_859,
        "distinct_target_touching_source_column_H_orbits": 647_409,
    }, "independent Python prefix changed")
    require(result["lex_q_control"]["literal_incident_columns"]
            == result["lex_q_control"]["optimized_incident_columns"] == 106
            and result["lex_q_control"]["sets_equal"] is True,
            "lex-q provider crosscheck changed")
    require(dafsa["logical_sha256"] == result["weighted_dafsa_logical_sha256"]
            and digest(BINARY) == result["weighted_dafsa_binary_sha256"],
            "weighted DAFSA dependency changed")
    logical = dict(result)
    logical.pop("elapsed_seconds")
    print("PASS", sha256(json.dumps(logical, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest())


if __name__ == "__main__":
    main()
