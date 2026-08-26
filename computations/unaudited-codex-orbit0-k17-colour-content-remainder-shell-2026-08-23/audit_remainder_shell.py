#!/usr/bin/env python3
"""Small exact audit of the remainder-rooted provider screen and capped shell."""
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    result = json.loads((HERE / "results_remainder_shell.json").read_text())
    if "--mutate" in sys.argv:
        result["low_incidence_screen"]["unique_provider_coordinates"] = 1
    screen = (HERE / "remainder_provider_screen.tsv").read_text().splitlines()
    require(screen[0] == "colour_content_type\ttarget_rows\tdistinct_literal_provider_lower_bound", screen[0])
    rows = [line.split("\t") for line in screen[1:]]
    require(len(rows) == 4612, len(rows))
    exterior = [row for row in rows if int(row[1]) == 0]
    represented = [row for row in rows if int(row[1]) > 0]
    require(len(exterior) == 40 and all(int(row[2]) == 0 for row in exterior), exterior[:2])
    require(len(represented) == 4572 and all(int(row[2]) == 2 for row in represented), represented[:2])
    require(sum(int(row[1]) for row in represented) == 34_835_632, "incidence sum")
    require(result["low_incidence_screen"] == {
        "scope": "all 55191349 checkpoint rows", "zero_provider_coordinates": 40,
        "unique_provider_coordinates": 0, "at_least_two_provider_coordinates": 4572,
        "target_row_incidence_sum": 34_835_632}, result["low_incidence_screen"])
    require((result["status"], result["terminal"]) == ("BOUNDED_CAP", "100000_distinct_vectors"), result)
    census = result["census"]
    require((census["checkpoint_rows_processed"], census["literal_mixed_source_columns_visited"],
             census["distinct_projected_vectors"], census["coordinates"], census["new_coordinates"],
             census["vector_nnz"]) == (2_890_587, 2_736_556, 100_000, 35_521, 19_109, 839_871), census)
    zero = json.loads((HERE / "results_zero_mixed_provider_coordinates.json").read_text())
    require((zero["coordinates"], zero["target_row_count_sum"], zero["target_row_count_max"])
            == (40, 0, 0), zero)
    pins = {
        "remainder_provider_screen.tsv": "eb836c6c844a1ccce5c7f36a888a5623aff86f9e60541f3164fc48ed5a687a2b",
        "remainder_shell_coordinates.tsv": "f916c9ca1a8b7a5d49025a53efac37facf6f41cc051324b9c18afc88aa9351b4",
        "remainder_shell_vectors.tsv": "3d8f1351857da814ead9273c179bef8c0c8c449b8c87626bbec59401fc72ca10",
        "zero_mixed_provider_coordinates.tsv": "db0ebd25e4bd15c0d9e23ca8afbd7c21fc3f176233d4c137250c7d901f076887",
    }
    for name, digest in pins.items():
        require(sha256((HERE / name).read_bytes()).hexdigest() == digest, name)
    logical = {key: value for key, value in result.items() if key != "elapsed_seconds"}
    print(json.dumps({"status": "PASS", "logical_sha256": sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
