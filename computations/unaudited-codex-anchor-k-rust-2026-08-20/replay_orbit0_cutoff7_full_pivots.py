#!/usr/bin/env python3
"""Lift the orbit0 cutoff-7 core identity through every singleton pivot."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SEED = (HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
        / "orbit0_cutoff7_seed.txt")
CORE = HERE / "results_orbit0_cutoff7_exact_core_certificate.json"
SOURCE = HERE / "results_orbit0_cutoff7_source_supports.jsonl"
OUT = HERE / "results_orbit0_cutoff7_full_quotient_certificate.json"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add_column(vector, entries, coefficient):
    for row, multiplicity in entries:
        vector[row] += coefficient * multiplicity
        if vector[row] == 0:
            del vector[row]


def main():
    target = Counter()
    for line in SEED.read_text().splitlines():
        fields = line.split()
        if fields and fields[0] in ("ROW", "TARGET"):
            target[fields[1]] += Fraction(int(fields[2]), int(fields[3]))
    core = json.loads(CORE.read_text())
    core_coefficients = {index: Fraction(coefficient)
                         for index, coefficient in core["solution"]}
    pivots = []
    chosen = []
    combination = Counter()
    with SOURCE.open() as stream:
        header = json.loads(next(stream))
        for line in stream:
            item = json.loads(line)
            entries = tuple((row, value) for row, value in item["original_entries"])
            if item["role"] == "core":
                coefficient = core_coefficients.get(item["core_index"], Fraction())
                if coefficient:
                    add_column(combination, entries, coefficient)
                    chosen.append((item, coefficient))
            else:
                pivots.append((item, entries))
    require(len(pivots) == header["pivot_count"] == 2075, "pivot count changed")
    require(len(core_coefficients) == core["solution_terms"] == 94, "core support changed")
    pivots.sort(key=lambda pair: pair[0]["pivot_order"])
    require([item["pivot_order"] for item, _ in pivots] == list(range(len(pivots))),
            "pivot order is not deterministic")
    for item, entries in reversed(pivots):
        row = item["pivot_row_hex"]
        residual = target.get(row, Fraction()) - combination.get(row, Fraction())
        coefficient = residual / item["pivot_coefficient"]
        if coefficient:
            add_column(combination, entries, coefficient)
            chosen.append((item, coefficient))
    require(combination == target, "reverse singleton lift failed over Q")
    mutation = combination.copy()
    add_column(mutation, chosen[0][0]["original_entries"], Fraction(1))
    require(mutation != target, "full-source mutation did not fire")
    terms = []
    for item, coefficient in chosen:
        terms.append({
            "coefficient": [coefficient.numerator, coefficient.denominator],
            "core_index": item.get("core_index"),
            "multiplier_cell_ids": item["multiplier_cell_ids"],
            "pivot_order": item.get("pivot_order"),
            "role": item["role"],
            "source_closure_column": item["source_closure_column"],
            "word": item["word"],
        })
    terms.sort(key=lambda item: (item["source_closure_column"], item["role"]))
    result = {
        "chart": "zero0_three_identical_perfect_matchings",
        "cutoff": 7,
        "scope": "exact invariant quotient identity; literal orbit-average expansion requires independent replay",
        "seed_sha256": sha256(SEED.read_bytes()).hexdigest(),
        "source_support_ledger_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "pivot_count": len(pivots),
        "nonzero_source_terms": len(terms),
        "max_denominator": max(item["coefficient"][1] for item in terms),
        "exact_reverse_pivot_replay": True,
        "mutation_fires": True,
        "terms": terms,
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("orbit0 cutoff7 full pivot replay: PASS")
    print("nonzero quotient source terms/max denominator:",
          result["nonzero_source_terms"], result["max_denominator"])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
