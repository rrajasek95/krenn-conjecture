#!/usr/bin/env python3
"""Exact bounded kernel/relative-Gram assembly from a factorized B20 control."""
import argparse
import json
import os
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def nullspace(matrix):
    rows = [[Fraction(value) for value in row] for row in matrix]
    m = len(rows)
    n = len(rows[0]) if rows else 0
    pivot_columns = []
    pivot_row = 0
    for column in range(n):
        found = next((row for row in range(pivot_row, m) if rows[row][column]), None)
        if found is None:
            continue
        rows[pivot_row], rows[found] = rows[found], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for row in range(m):
            if row != pivot_row and rows[row][column]:
                factor = rows[row][column]
                rows[row] = [left - factor * right for left, right in zip(rows[row], rows[pivot_row])]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == m:
            break
    free = [column for column in range(n) if column not in pivot_columns]
    basis = []
    for column in free:
        vector = [Fraction(0) for _ in range(n)]
        vector[column] = 1
        for row, pivot in reversed(list(enumerate(pivot_columns))):
            vector[pivot] = -sum(rows[row][j] * vector[j] for j in free)
        basis.append(vector)
    return basis, len(pivot_columns)


def fraction_text(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--B20-result", type=Path, required=True)
    parser.add_argument("--target-coefficient", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = args.B20_result if args.B20_result.is_absolute() else ROOT / args.B20_result
    output = args.output if args.output.is_absolute() else ROOT / args.output
    result = json.loads(source.read_text())
    need(result["status"] == "PASS_BOUNDED_FACTORIZED_K24_B20_EQUIVALENCE", "B20 control status")
    grams = {int(key): int(value) for key, value in result["factorized_block_gram"].items()}
    need(set(grams) == {20, 22, 23, 24}, "B20 blocks")
    G_lower = [[grams[20] + grams[22] + grams[23]]]
    G_top = [[grams[24]]]
    kernel, lower_rank = nullspace(G_lower)
    need(lower_rank == 1 and kernel == [], "one-column lower kernel control")
    r = Fraction(args.target_coefficient)
    target_pairing_raw = Fraction(G_top[0][0]) * r
    target_norm = r * r * G_top[0][0]
    full_gram = G_lower[0][0] + G_top[0][0]
    normal_solution = target_pairing_raw / full_gram
    projected_norm = target_pairing_raw * normal_solution
    need(projected_norm != target_norm, "full filtered Gram must reject bounded target")
    payload = {
        "status": "PASS_INCONCLUSIVE_BOUNDED_FACTORIZED_RELATIVE_GRAM_CONTROL",
        "component_status": "COLUMN_CAP_1_NOT_COMPLETE",
        "columns": 1,
        "target_coefficient": [r.numerator, r.denominator],
        "G20": str(grams[20]),
        "G22": str(grams[22]),
        "G23": str(grams[23]),
        "G24": str(grams[24]),
        "G_lower": str(G_lower[0][0]),
        "lower_rank": lower_rank,
        "lower_nullity": len(kernel),
        "relative_columns": len(kernel),
        "relative_gram_dimension": 0,
        "target_top_norm": fraction_text(target_norm),
        "full_filtered_gram": str(full_gram),
        "full_filtered_normal_solution": fraction_text(normal_solution),
        "full_filtered_projected_norm": fraction_text(projected_norm),
        "full_filtered_exact_norm_identity": False,
        "kernel_route_and_full_gram_route_agree": True,
        "bounded_component_membership": False,
        "global_membership_verdict": "INCONCLUSIVE_INCOMPLETE_CLOSURE",
        "theorem": "ker(G_lower)=ker(L20); relative Gram is K^T*G24*K. Equivalently test (0,R24) against the full filtered Gram G_lower+G24.",
        "scope_guard": "one-column bounded algebra control only; no global nonmembership, K24 charge, or conjecture claim",
    }
    temporary = Path(str(output) + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
