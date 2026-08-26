#!/usr/bin/env python3
"""Exact-Q core reconstruction and full singleton lift for orbit0 cutoff 8."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRIMES = (1009, 1013, 1019)
MATRIX = HERE / "results_orbit0_cutoff8_direct.jsonl"
SOURCE = HERE / "results_orbit0_cutoff8_source_supports.jsonl"
SEED = (HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
        / "orbit0_cutoff8_seed.txt")
CORE_OUT = HERE / "results_orbit0_cutoff8_exact_core_certificate.json"
FULL_OUT = HERE / "results_orbit0_cutoff8_full_quotient_certificate.json"


def crt(left, left_prime, right, right_prime):
    return (left + left_prime * (
        (right - left) * pow(left_prime, -1, right_prime) % right_prime
    )) % (left_prime * right_prime)


def rational_reconstruct(residue, modulus):
    bound = math.isqrt(modulus // 2)
    old_r, r = modulus, residue
    old_s, s = 0, 1
    while r and abs(r) > bound:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
    require(r and s, "rational reconstruction failed")
    numerator, denominator = r, s
    if denominator < 0:
        numerator, denominator = -numerator, -denominator
    common = math.gcd(numerator, denominator)
    value = Fraction(numerator // common, denominator // common)
    require((value.numerator - residue * value.denominator) % modulus == 0,
            "rational reconstruction congruence failed")
    return value


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add_column(vector, entries, coefficient):
    for row, multiplicity in entries:
        vector[row] += coefficient * multiplicity
        if vector[row] == 0:
            del vector[row]


def reconstruct():
    modular = [json.loads((HERE / f"results_orbit0_cutoff8_p{prime}.json").read_text())
               for prime in PRIMES]
    solutions = [dict(item["solution"]) for item in modular]
    support = set().union(*solutions)
    require(all(set(solution) == support for solution in solutions),
            "modular solution supports differ")
    modulus = PRIMES[0]
    residues = dict(solutions[0])
    for prime, solution in zip(PRIMES[1:], solutions[1:]):
        residues = {index: crt(residues[index], modulus, solution[index], prime)
                    for index in support}
        modulus *= prime
    coefficients = {index: rational_reconstruct(residue, modulus)
                    for index, residue in residues.items()}
    require(all(value is not None for value in coefficients.values()),
            "rational reconstruction is incomplete")
    return {index: value for index, value in coefficients.items() if value}


def core_replay(coefficients):
    replay = Counter()
    selected_entries = {}
    with MATRIX.open() as stream:
        header = json.loads(next(stream))
        target = Counter({row: Fraction(numerator, denominator)
                          for row, numerator, denominator in header["target"]})
        for line in stream:
            item = json.loads(line)
            coefficient = coefficients.get(item["index"])
            if coefficient:
                entries = tuple(map(tuple, item["entries"]))
                selected_entries[item["index"]] = entries
                add_column(replay, entries, coefficient)
    require(replay == target, "exact cutoff8 core replay failed")
    mutation = replay.copy()
    add_column(mutation, selected_entries[min(coefficients)], Fraction(1))
    require(mutation != target, "cutoff8 core mutation did not fire")
    return header


def full_replay(coefficients):
    target = Counter()
    for line in SEED.read_text().splitlines():
        fields = line.split()
        if fields and fields[0] in ("ROW", "TARGET"):
            target[fields[1]] += Fraction(int(fields[2]), int(fields[3]))
    combination = Counter()
    pivots = []
    chosen = []
    with SOURCE.open() as stream:
        header = json.loads(next(stream))
        for line in stream:
            item = json.loads(line)
            entries = tuple(map(tuple, item["original_entries"]))
            if item["role"] == "core":
                coefficient = coefficients.get(item["core_index"], Fraction())
                if coefficient:
                    add_column(combination, entries, coefficient)
                    chosen.append((item, coefficient))
            else:
                pivots.append((item, entries))
    pivots.sort(key=lambda pair: pair[0]["pivot_order"])
    require(len(pivots) == header["pivot_count"] == 13695, "cutoff8 pivot count changed")
    for item, entries in reversed(pivots):
        residual = target.get(item["pivot_row_hex"], Fraction()) \
            - combination.get(item["pivot_row_hex"], Fraction())
        coefficient = residual / item["pivot_coefficient"]
        if coefficient:
            add_column(combination, entries, coefficient)
            chosen.append((item, coefficient))
    require(combination == target, "cutoff8 reverse singleton lift failed")
    mutation = combination.copy()
    add_column(mutation, chosen[0][0]["original_entries"], Fraction(1))
    require(mutation != target, "cutoff8 full mutation did not fire")
    return chosen


def main():
    coefficients = reconstruct()
    header = core_replay(coefficients)
    core = {
        "chart": "zero0_three_identical_perfect_matchings",
        "cutoff": 8,
        "crt_primes": list(PRIMES),
        "matrix_sha256": sha256(MATRIX.read_bytes()).hexdigest(),
        "row_count": header["row_count"],
        "column_count": header["column_count"],
        "solution": [[index, value.numerator, value.denominator]
                     for index, value in sorted(coefficients.items())],
        "solution_terms": len(coefficients),
        "exact_core_replay": True,
        "mutation_fires": True,
    }
    logical = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    CORE_OUT.write_text(json.dumps(core, indent=2, sort_keys=True) + "\n")
    chosen = full_replay(coefficients)
    terms = [{
        "coefficient": [coefficient.numerator, coefficient.denominator],
        "core_index": item.get("core_index"),
        "multiplier_cell_ids": item["multiplier_cell_ids"],
        "pivot_order": item.get("pivot_order"),
        "role": item["role"],
        "source_closure_column": item["source_closure_column"],
        "word": item["word"],
    } for item, coefficient in chosen]
    terms.sort(key=lambda item: item["source_closure_column"])
    full = {
        "chart": core["chart"], "cutoff": 8,
        "scope": "exact invariant quotient identity; literal orbit-average expansion requires independent replay",
        "seed_sha256": sha256(SEED.read_bytes()).hexdigest(),
        "source_support_ledger_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "pivot_count": 13695,
        "nonzero_source_terms": len(terms),
        "max_denominator": max(item["coefficient"][1] for item in terms),
        "exact_reverse_pivot_replay": True, "mutation_fires": True,
        "terms": terms,
    }
    logical = json.dumps(full, sort_keys=True, separators=(",", ":"))
    full["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    FULL_OUT.write_text(json.dumps(full, indent=2, sort_keys=True) + "\n")
    print("orbit0 cutoff8 exact core + full pivot replay: PASS")
    print("core/full terms:", len(coefficients), len(terms),
          "max denominator:", full["max_denominator"])
    print("logical sha256:", core["logical_sha256"], full["logical_sha256"])


if __name__ == "__main__":
    main()
