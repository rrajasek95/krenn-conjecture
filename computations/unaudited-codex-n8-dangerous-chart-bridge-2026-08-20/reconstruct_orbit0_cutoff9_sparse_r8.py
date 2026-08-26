#!/usr/bin/env python3
"""Reconstruct a sparse exact K-degree-eight representative from cutoff 9.

The target-overlap modular echelon leaves the same 120-row support at two
primes.  This script reconstructs its rational solution and remainder, replays
the complete exact core, then reverses all singleton pivots against the literal
source-support ledger.  The terminal residual is therefore a source-faithful
representative of T modulo I_mix + K^9, not merely a modular/core remainder.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
RUST = HERE.parent / "unaudited-codex-anchor-k-rust-2026-08-20"
INTERFACE = HERE / "orbit0_cutoff9_target_overlap.jsonl"
MODULAR = (RUST / "results_orbit0_cutoff9_overlap_p1009.json",
           RUST / "results_orbit0_cutoff9_overlap_p1013.json")
SOURCE = RUST / "results_orbit0_cutoff9_source_supports.jsonl"
SEED = HERE / "orbit0_cutoff9_seed.txt"
T2_PATH = HERE / "audit_orbit0_t2_pivot_setup.py"
T2_SPEC = importlib.util.spec_from_file_location("orbit0_t2_setup", T2_PATH)
T2 = importlib.util.module_from_spec(T2_SPEC)
T2_SPEC.loader.exec_module(T2)
OUT = HERE / "results_orbit0_cutoff9_sparse_r8.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def crt(left, left_prime, right, right_prime):
    return (left + left_prime * (
        (right - left) * pow(left_prime, -1, right_prime) % right_prime
    )) % (left_prime * right_prime)


def reconstruct_common(field):
    first, second = [json.loads(path.read_text()) for path in MODULAR]
    require(first["prime"] == 1009 and second["prime"] == 1013,
            "modular primes changed")
    left, right = dict(first[field]), dict(second[field])
    require(tuple(left) == tuple(right), f"{field} supports differ")
    modulus = 1009 * 1013
    answer = {}
    for index, value in left.items():
        lifted = crt(value, 1009, right[index], 1013)
        if lifted > modulus // 2:
            lifted -= modulus
        answer[index] = Fraction(lifted)
    return answer


def add_entries(polynomial, entries, coefficient):
    for row, value in entries:
        updated = polynomial.get(row, 0) + coefficient * value
        if updated:
            polynomial[row] = updated
        else:
            polynomial.pop(row, None)


def main():
    reordered_coefficients = reconstruct_common("solution")
    modular_remainder = reconstruct_common("remainder")
    core_combination = Counter()
    core_columns = {}
    with INTERFACE.open() as handle:
        header = json.loads(next(handle))
        rows_hex = header["rows_hex"]
        core_target = Counter({row: Fraction(numerator, denominator)
                               for row, numerator, denominator
                               in header["target"]})
        for line in handle:
            record = json.loads(line)
            coefficient = reordered_coefficients.get(record["index"])
            if coefficient:
                add_entries(core_combination, record["entries"], coefficient)
                core_columns[record["original_index"]] = (
                    coefficient, record["word"], record["multiplier_cell_ids"]
                )
    core_residual = core_target.copy()
    add_entries(core_residual, core_combination.items(), Fraction(-1))
    expected_core_residual = Counter({index: value
                                      for index, value in modular_remainder.items()
                                      if value})
    require(core_residual == expected_core_residual
            and len(core_residual) == 120,
            "exact core remainder differs from two-prime reconstruction")

    full_target = Counter()
    for line in SEED.read_text().splitlines():
        fields = line.split()
        if fields and fields[0] in ("ROW", "TARGET"):
            full_target[fields[1]] += Fraction(int(fields[2]), int(fields[3]))

    full_combination = Counter()
    pivots = []
    chosen = []
    with SOURCE.open() as handle:
        source_header = json.loads(next(handle))
        for line in handle:
            record = json.loads(line)
            if record["role"] == "core":
                chosen_core = core_columns.get(record["core_index"])
                if chosen_core is not None:
                    coefficient, word, multiplier = chosen_core
                    require(record["word"] == word
                            and record["multiplier_cell_ids"] == multiplier,
                            "reordered/core source provenance mismatch")
                    add_entries(full_combination, record["original_entries"],
                                coefficient)
                    chosen.append((record, coefficient))
            else:
                pivots.append(record)
    require(len(pivots) == source_header["pivot_count"] == 71492,
            "pivot count changed")
    pivots.sort(key=lambda record: record["pivot_order"], reverse=True)
    for record in pivots:
        row = record["pivot_row_hex"]
        coefficient = ((full_target.get(row, 0)
                        - full_combination.get(row, 0))
                       / record["pivot_coefficient"])
        if coefficient:
            add_entries(full_combination, record["original_entries"], coefficient)
            chosen.append((record, coefficient))

    full_residual = full_target.copy()
    add_entries(full_residual, full_combination.items(), Fraction(-1))
    expected_full = Counter({rows_hex[index]: value
                             for index, value in core_residual.items()})
    require(full_residual == expected_full,
            "reverse singleton replay changed the sparse core residual")
    residual = Counter({bytes.fromhex(row): value
                        for row, value in full_residual.items()})
    require(len(residual) == 120
            and all(len(row) == 12 and T2.row_k_degree(row) == 8
                    for row in residual),
            "sparse representative is not wholly total-degree12/K-degree8")

    orbit_sizes = {row: len(T2.row_orbit(row)) for row in residual}
    require(all(value % 1 == 0 for value in residual.values()),
            "quotient residual unexpectedly nonintegral")
    labelled_coefficients = Counter()
    for row, mass in residual.items():
        labelled_coefficients[mass / orbit_sizes[row]] += orbit_sizes[row]

    terms = [{
        "coefficient": [coefficient.numerator, coefficient.denominator],
        "core_index": record.get("core_index"),
        "multiplier_cell_ids": record["multiplier_cell_ids"],
        "pivot_order": record.get("pivot_order"),
        "role": record["role"],
        "source_closure_column": record["source_closure_column"],
        "word": record["word"],
    } for record, coefficient in chosen]
    terms.sort(key=lambda item: item["source_closure_column"])
    total_mass = sum(residual.values())
    sizes = tuple(orbit_sizes.values())
    result = {
        "status": "UNAUDITED exact-Q sparse K8 representative with full pivot replay",
        "chart": 0,
        "cutoff": 9,
        "modular_primes": [1009, 1013],
        "interface_sha256": sha256(INTERFACE.read_bytes()).hexdigest(),
        "source_ledger_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "seed_sha256": sha256(SEED.read_bytes()).hexdigest(),
        "core_solution_terms": len(reordered_coefficients),
        "core_remainder_rows": len(core_residual),
        "full_source_terms": len(terms),
        "maximum_source_denominator": max(item["coefficient"][1]
                                           for item in terms),
        "exact_core_replay": True,
        "exact_reverse_pivot_replay": True,
        "residual_total_degree": 12,
        "residual_K_degree": 8,
        "residual_quotient_orbits": len(residual),
        "residual_labelled_support": sum(sizes),
        "residual_total_orbit_mass": [total_mass.numerator, total_mass.denominator],
        "residual_orbit_size_histogram": {
            str(size): count for size, count in sorted(Counter(sizes).items())
        },
        "residual_quotient_mass_histogram": {
            str(value): count for value, count in sorted(Counter(residual.values()).items())
        },
        "residual_labelled_coefficient_histogram": {
            str(value): count for value, count in sorted(labelled_coefficients.items())
        },
        "residual": [[row.hex(), value.numerator, value.denominator]
                     for row, value in sorted(residual.items())],
        "terms": terms,
        "conclusion": (
            "T is congruent modulo I_mix+K^9 to this exact 120-orbit "
            "K-degree-eight polynomial; its square is a valid replacement "
            "for the 301-orbit R8 square in gr_K^16(R/I_mix)."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("orbit0 cutoff9 sparse R8 reconstruction: PASS")
    print("core solution/remainder:", len(reordered_coefficients), len(core_residual))
    print("full source terms:", len(terms))
    print("residual quotient/labelled:", len(residual), sum(sizes))
    print("residual total mass:", total_mass)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
