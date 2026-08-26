#!/usr/bin/env python3
"""Export the exact 6,800-coordinate K17 colour-content target vector."""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "results_reduced_k17_census.json"
OUT = HERE / "k17_colour_content_target.tsv"
RESULT = HERE / "results_k17_colour_content_target_export.json"
CYCLE_DUAL = (HERE.parents[1]
              / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23"
              / "k16_cycle_partition_dual.tsv")


def main():
    data = json.loads(SOURCE.read_text())
    rows = []
    total = Fraction()
    cycle_vector = {}
    for key, stats in sorted(data["by_colour_content_type"].items()):
        numerator, denominator = stats["signed_mass"]
        value = Fraction(numerator, denominator)
        rows.append((key, value))
        total += value
        partition = tuple(sorted(sum(map(int, component.split(":")))
                                 for component in key.split(";")))
        cycle_vector[partition] = cycle_vector.get(partition, Fraction()) + value
    assert len(rows) == 6800
    assert total == Fraction(-12_732_235_776, 7)
    with OUT.open("w") as stream:
        stream.write("colour_content_type\tnumerator\tdenominator\n")
        for key, value in rows:
            stream.write(f"{key}\t{value.numerator}\t{value.denominator}\n")
    dual = {}
    lines = CYCLE_DUAL.read_text().splitlines()
    assert lines[0] == "cycle_partition\tinteger_coefficient"
    for line in lines[1:]:
        key, coefficient = line.split("\t")
        dual[tuple(map(int, key.split(",")))] = int(coefficient)
    charge = sum(value * dual.get(key, 0)
                 for key, value in cycle_vector.items())
    assert charge == Fraction(-9_747_200_926_208, 6_545)
    result = {
        "status": "PASS exact 6800-coordinate K17 colour-content export",
        "coordinates": len(rows),
        "nonzero_target_coordinates": sum(value != 0 for _key, value in rows),
        "total_mass": [total.numerator, total.denominator],
        "forgotten_cycle_partitions": sum(value != 0
                                          for value in cycle_vector.values()),
        "cycle_dual_pairing": [charge.numerator, charge.denominator],
        "target_sha256": sha256(OUT.read_bytes()).hexdigest(),
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
