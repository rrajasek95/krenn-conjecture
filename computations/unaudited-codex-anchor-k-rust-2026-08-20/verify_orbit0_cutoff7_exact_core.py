#!/usr/bin/env python3
"""Exact-Z replay of the orbit0 cutoff-7 peeled-core certificate."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
MATRIX = HERE / "results_orbit0_cutoff7_direct.jsonl"
MODULAR = (HERE / "results_orbit0_cutoff7_p1009.json",
           HERE / "results_orbit0_cutoff7_p1013.json")
OUT = HERE / "results_orbit0_cutoff7_exact_core_certificate.json"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def centered(value, prime):
    value %= prime
    return value if value <= prime // 2 else value - prime


def main():
    modular = [json.loads(path.read_text()) for path in MODULAR]
    solutions = [dict(item["solution"]) for item in modular]
    indices = tuple(solutions[0])
    require(indices == tuple(solutions[1]), "two-prime solution supports differ")
    coefficients = {index: centered(value, modular[0]["prime"])
                    for index, value in solutions[0].items()}
    for item, solution in zip(modular, solutions):
        prime = item["prime"]
        require(all(coefficient % prime == solution[index]
                    for index, coefficient in coefficients.items()),
                f"integer lift fails modulo {prime}")

    with MATRIX.open() as stream:
        header = json.loads(next(stream))
        target = Counter({row: numerator // denominator
                          for row, numerator, denominator in header["target"]})
        require(all(numerator % denominator == 0
                    for _, numerator, denominator in header["target"]),
                "orbit0 target ceased to be integral")
        replay = Counter()
        mutation = Counter()
        selected = set(coefficients)
        for line in stream:
            column = json.loads(line)
            index = column["index"]
            if index not in selected:
                continue
            coefficient = coefficients[index]
            for row, value in column["entries"]:
                replay[row] += coefficient * value
                mutation[row] += coefficient * value
            if index == indices[0]:
                for row, value in column["entries"]:
                    mutation[row] += value
    replay += Counter()
    mutation += Counter()
    require(replay == target, "exact-Z core replay failed")
    require(mutation != target, "coefficient mutation did not fire")
    core = {
        "chart": "zero0_three_identical_perfect_matchings",
        "cutoff": 7,
        "matrix_sha256": sha256(MATRIX.read_bytes()).hexdigest(),
        "row_count": header["row_count"],
        "column_count": header["column_count"],
        "solution": [[index, coefficients[index]] for index in indices],
        "solution_terms": len(indices),
        "max_abs_coefficient": max(map(abs, coefficients.values())),
        "exact_integer_replay": True,
        "mutation_fires": True,
    }
    logical = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(core, indent=2, sort_keys=True) + "\n")
    print("orbit0 cutoff7 exact-Z core replay: PASS")
    print("solution terms/max abs:", len(indices), core["max_abs_coefficient"])
    print("logical sha256:", core["logical_sha256"])


if __name__ == "__main__":
    main()
