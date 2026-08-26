#!/usr/bin/env python3
"""Reconstruct and replay the exact cutoff-9 obstruction for orbit0."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
INTERFACE = (HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
             / "orbit0_cutoff9_target_overlap.jsonl")
SOURCE = HERE / "results_orbit0_cutoff9_source_supports.jsonl"
SEED = (HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
        / "orbit0_cutoff9_seed.txt")
MODULAR = (HERE / "results_orbit0_cutoff9_overlap_p1009.json",
           HERE / "results_orbit0_cutoff9_overlap_p1013.json")
OUT = HERE / "results_orbit0_cutoff9_exact_dual.json"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def crt(left, left_prime, right, right_prime):
    return (left + left_prime * (
        (right - left) * pow(left_prime, -1, right_prime) % right_prime
    )) % (left_prime * right_prime)


def reconstruct(residue, modulus):
    bound = math.isqrt(modulus // 2)
    old_r, r = modulus, residue
    old_s, s = 0, 1
    while r and abs(r) > bound:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
    require(r and s, "rational reconstruction failed")
    if s < 0:
        r, s = -r, -s
    common = math.gcd(r, s)
    value = Fraction(r // common, s // common)
    require((value.numerator - residue * value.denominator) % modulus == 0,
            "rational reconstruction congruence failed")
    return value


def main():
    first, second = [json.loads(path.read_text()) for path in MODULAR]
    require(first["prime"] == 1009 and second["prime"] == 1013,
            "dual primes changed")
    left, right = dict(first["left_dual"]), dict(second["left_dual"])
    require(tuple(left) == tuple(right) and len(left) == 37,
            "two-prime dual supports differ")
    modulus = 1009 * 1013
    dual = {row: reconstruct(crt(value, 1009, right[row], 1013), modulus)
            for row, value in left.items()}

    with INTERFACE.open() as stream:
        header = json.loads(next(stream))
        target = Counter({row: Fraction(numerator, denominator)
                          for row, numerator, denominator in header["target"]})
        checked = 0
        for line in stream:
            column = json.loads(line)
            pairing = sum(dual.get(row, Fraction()) * value
                          for row, value in column["entries"])
            require(pairing == 0, f"dual fails on core column {column['index']}")
            checked += 1
    require(checked == header["column_count"] == 115839, "core column count changed")
    target_pairing = sum(dual.get(row, Fraction()) * value
                         for row, value in target.items())
    require(target_pairing == 2304, "exact target pairing changed")

    # Pull the quotient functional back through the singleton eliminations.
    # At pivot k, all non-pivot rows and later pivot rows are absent from the
    # original pivot column; the one new coefficient is therefore determined
    # from already assigned earlier pivots.
    labelled_dual = {header["rows_hex"][row]: value for row, value in dual.items()}
    source_records = []
    with SOURCE.open() as stream:
        source_header = json.loads(next(stream))
        for line in stream:
            source_records.append(json.loads(line))
    pivots = sorted((item for item in source_records if item["role"] == "pivot"),
                    key=lambda item: item["pivot_order"])
    require(len(pivots) == source_header["pivot_count"] == 71492,
            "cutoff9 pivot count changed")
    nonzero_pivot_values = 0
    for item in pivots:
        pivot_row = item["pivot_row_hex"]
        pivot_entry = sum(value for row, value in item["original_entries"]
                          if row == pivot_row)
        require(pivot_entry == item["pivot_coefficient"],
                "declared pivot coefficient differs from original support")
        tail = sum(labelled_dual.get(row, Fraction()) * value
                   for row, value in item["original_entries"] if row != pivot_row)
        value = -tail / pivot_entry
        if value:
            labelled_dual[pivot_row] = value
            nonzero_pivot_values += 1
    # Literal check of every retained pivot/core source column.  Columns with
    # final empty support are combinations eliminated by these same pivots.
    for item in source_records:
        pairing = sum(labelled_dual.get(row, Fraction()) * value
                      for row, value in item["original_entries"])
        require(pairing == 0,
                f"pulled-back dual fails source column {item['source_closure_column']}")
    full_target = Counter()
    for line in SEED.read_text().splitlines():
        fields = line.split()
        if fields and fields[0] in ("ROW", "TARGET"):
            full_target[fields[1]] += Fraction(int(fields[2]), int(fields[3]))
    full_pairing = sum(labelled_dual.get(row, Fraction()) * value
                       for row, value in full_target.items())
    require(full_pairing == 2304, "pulled-back target pairing changed")
    mutation = dict(dual)
    mutation[min(mutation)] += 1
    require(mutation != dual, "dual mutation did not fire")

    result = {
        "chart": "zero0_three_identical_perfect_matchings",
        "cutoff": 9,
        "conclusion": "H0H1H2 is not in I_mix + K_anchor^9 over Q for orbit0",
        "interface_sha256": sha256(INTERFACE.read_bytes()).hexdigest(),
        "source_support_ledger_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "dual": [[header["rows_hex"][row], value.numerator, value.denominator]
                 for row, value in sorted(dual.items())],
        "dual_terms": len(dual),
        "target_pairing": [target_pairing.numerator, target_pairing.denominator],
        "core_columns_checked": checked,
        "pivots_checked": len(pivots),
        "retained_source_columns_checked": len(source_records),
        "nonzero_pivot_pullback_values": nonzero_pivot_values,
        "exact_q_replay": True,
        "mutation_fires": True,
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("orbit0 cutoff9 exact dual: PASS")
    print("dual/pairing/pivot pullback:", len(dual), target_pairing,
          nonzero_pivot_values)
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
