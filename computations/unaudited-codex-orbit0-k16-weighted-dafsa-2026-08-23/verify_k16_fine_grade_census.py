#!/usr/bin/env python3
"""Small result/interface guard for the exhaustive K16 fine-grade census."""

import argparse
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results_k16_fine_grade_census.json"
TABLE = HERE / "k16_fine_grade_census.tsv"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = json.loads(RESULT.read_text())
    grades = result["target_bearing_fine_grade_H_orbits"]
    if args.mutate:
        grades += 1
    require(grades == 1, "hostile grade-count mutation fired")
    require(result["target_row_H_orbits"] == 1_848_174
            and result["source_column_H_orbits"] == 98_609_090
            and result["ordinary_column_trie_nodes_visited"] == 843_704_501
            and result["grade_supports_equal"] is True
            and result["sample_output_grade_checks"] == 315,
            "fine-grade exhaustive census changed")
    expected = ("grade_hex\ttarget_row_H_orbits\tsource_column_H_orbits\n"
                + "02" * 24 + "\t1848174\t98609090\n")
    require(TABLE.read_text() == expected, "balanced-grade table changed")
    logical = dict(result)
    logical.pop("elapsed_seconds")
    print("PASS", sha256(json.dumps(logical, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest())


if __name__ == "__main__":
    main()
