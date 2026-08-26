#!/usr/bin/env python3
"""Exact relative/full-Gram equivalence on the induced 257-column control."""
import argparse
import json
import os
from fractions import Fraction
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def fraction_text(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--columns", type=Path, required=True)
    parser.add_argument("--edges", type=Path, required=True)
    parser.add_argument("--gate-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    need(not args.output.exists(), "refuse overwrite")
    gate = json.loads(args.gate_result.read_text())
    need(gate["status"] == "PASS_BOUNDED_K24_SPARSE_CLOSURE_GATES_NO_LAUNCH", "gate status")
    need(gate["sample257"]["natural_unique_columns"] == 257, "257 columns")
    need(gate["one_source_unit"]["closure_status"] == "COLUMN_CAP_BEFORE_INCIDENCE", "source cap")
    column_lines = args.columns.read_text().splitlines()
    need(column_lines[0] == "index\tnatural_column_key\torbit_size\ttarget_coefficient_numerator\ttarget_coefficient_denominator", "column header")
    coefficients = []
    keys = []
    for expected, line in enumerate(column_lines[1:]):
        fields = line.split("\t")
        need(len(fields) == 5 and int(fields[0]) == expected, "column sequence")
        keys.append(fields[1])
        need(int(fields[2]) > 0 and 384 % int(fields[2]) == 0, "orbit divisor")
        coefficients.append(Fraction(int(fields[3]), int(fields[4])))
    need(len(keys) == len(set(keys)) == len(coefficients) == 257, "column census")
    edge_lines = args.edges.read_text().splitlines()
    need(edge_lines[0] == "left_index\tright_index\tG20\tG22\tG23\tG24", "edge header")
    diagonal = {}
    off_diagonal = 0
    for line in edge_lines[1:]:
        fields = list(map(int, line.split("\t")))
        need(len(fields) == 6 and 0 <= fields[0] <= fields[1] < 257, "edge shape")
        need(any(fields[2:]), "zero edge retained")
        if fields[0] != fields[1]:
            off_diagonal += 1
        else:
            need(fields[0] not in diagonal and all(value > 0 for value in fields[2:]), "diagonal edge")
            diagonal[fields[0]] = tuple(fields[2:])
    need(off_diagonal == 0 and len(diagonal) == 257, "distributed induced Gram must be diagonal")
    target_norm = Fraction(0)
    projected_norm = Fraction(0)
    norm_gap = Fraction(0)
    lower_diagonal = []
    top_diagonal = []
    for index, coefficient in enumerate(coefficients):
        blocks = diagonal[index]
        lower = sum(blocks[:3])
        top = blocks[3]
        need(lower > 0 and top > 0, "positive diagonal blocks")
        lower_diagonal.append(lower)
        top_diagonal.append(top)
        pairing = coefficient * top
        target_norm += coefficient * coefficient * top
        projected_norm += pairing * pairing / (lower + top)
        norm_gap += coefficient * coefficient * top * lower / (lower + top)
    need(target_norm - projected_norm == norm_gap and norm_gap > 0, "full-Gram norm gap identity")
    payload = {
        "status": "PASS_EXACT_K24_SAMPLE257_KERNEL_RELATIVE_FULL_GRAM_EQUIVALENCE",
        "columns": 257,
        "synthetic_target": "sum of the 257 distributed literal source coefficients times their K24 orbit-sum columns",
        "G_lower": "diagonal G20+G22+G23",
        "lower_rank": 257,
        "lower_nullity": 0,
        "kernel_basis_columns": 0,
        "relative_gram_dimension": 0,
        "relative_route_bounded_membership": False,
        "full_gram_route_bounded_membership": False,
        "target_top_norm": fraction_text(target_norm),
        "full_gram_projected_norm": fraction_text(projected_norm),
        "exact_positive_norm_gap": fraction_text(norm_gap),
        "kernel_and_full_gram_routes_agree": True,
        "component_status": "INDUCED_SAMPLE_ONLY_NOT_AMBIENTLY_CLOSED",
        "global_verdict": "INCONCLUSIVE_INCOMPLETE_CLOSURE",
        "one_source_unit_lower_transfer_complete": False,
        "scope": "exact 257-column induced algebra control only; no global nonmembership or K24 claim",
    }
    temporary = Path(str(args.output) + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, args.output)
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
