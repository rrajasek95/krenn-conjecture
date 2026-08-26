#!/usr/bin/env python3
"""Extract the Laurent binomial lattice of the 82-variable 1222-k4 target."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
INPUT = HERE / "results_phase_m7_1222_k4_sat_coefficient_target.json"
OUT = HERE / "results_phase_m7_1222_k4_toric.json"
SNF = HERE / "verify_phase_m7_1222_k4_toric_snf.sing"
GATE = HERE / "verify_phase_m7_1222_k4_toric_gate.sing"


def parse_q(label):
    label = label.replace("*", "")
    if "w" not in label:
        return Fraction(label), Fraction(0)
    if label.endswith("w"):
        prefix = label[:-1]
        split = max(prefix.rfind("+", 1), prefix.rfind("-", 1))
        if split >= 0:
            return Fraction(prefix[:split]), Fraction(prefix[split:] or "1")
        return Fraction(0), Fraction(prefix or "1")
    raise ValueError(label)


def rational_rank(rows, columns):
    matrix = [[Fraction(value) for value in row] for row in rows]
    rank = 0
    pivots = []
    for column in range(columns):
        pivot = next((row for row in range(rank, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        value = matrix[rank][column]
        matrix[rank] = [entry / value for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right
                           for left, right in zip(matrix[row], matrix[rank])]
        pivots.append(column)
        rank += 1
        if rank == len(matrix):
            break
    return rank, pivots


def monomial(term, names):
    counts = Counter(term["monomial"])
    factors = []
    for name, exponent in sorted(counts.items(), key=lambda item: names[item[0]]):
        variable = f"x{names[name] + 1}"
        factors.append(variable if exponent == 1 else f"{variable}^{exponent}")
    return "*".join(factors) or "1"


def singular_coefficient(label):
    return label.replace("*", "")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--snf", type=Path, default=SNF)
    parser.add_argument("--gate", type=Path, default=GATE)
    args = parser.parse_args()
    data = json.loads(args.input.read_text())["coefficient_system"]
    variables = data["variables"]
    names = {name: index for index, name in enumerate(variables)}
    binomials = [row for row in data["equations"] if len(row["terms"]) == 2]
    nonbinomials = [row for row in data["equations"] if len(row["terms"]) > 2]
    rows = []
    constants = []
    for row in binomials:
        left, right = row["terms"]
        vector = [0] * len(variables)
        for name in left["monomial"]:
            vector[names[name]] += 1
        for name in right["monomial"]:
            vector[names[name]] -= 1
        rows.append(vector)
        constants.append({
            "left": parse_q(left["coefficient"]),
            "right": parse_q(right["coefficient"]),
        })
    rank, pivots = rational_rank(rows, len(variables))

    flat = ",".join(str(value) for row in rows for value in row)
    snf_lines = [
        'LIB "multigrading.lib";',
        f"intmat A[{len(rows)}][{len(variables)}]={flat};",
        "list S=smithNormalForm(A,5);",
        'print("SNF_D_BEGIN");',
        "S[2];",
        'print("SNF_D_END");',
        'print("SNF_P_BEGIN");',
        "S[1];",
        'print("SNF_P_END");',
        'print("SNF_Q_BEGIN");',
        "S[3];",
        'print("SNF_Q_END");',
        "quit;",
    ]
    args.snf.write_text("\n".join(snf_lines) + "\n")

    ring_variables = [f"x{i + 1}" for i in range(len(variables))] + ["s"]
    equations = []
    for row in binomials:
        left, right = row["terms"]
        equations.append(
            f"({singular_coefficient(left['coefficient'])})*{monomial(left, names)}"
            f"+({singular_coefficient(right['coefficient'])})*{monomial(right, names)}"
        )
    product = "*".join(f"x{i + 1}" for i in range(len(variables)))
    gate_lines = [
        f"ring r=(0,w),({','.join(ring_variables)}),dp;",
        "minpoly=w2+w+1;",
        f"ideal B={','.join(equations)},s*{product}-1;",
        "option(redSB);",
        "ideal G=std(B);",
        'print("TORIC_GATE_BEGIN");',
        "size(G);",
        "dim(G);",
        "reduce(1,G);",
        'print("TORIC_GATE_END");',
        "quit;",
    ]
    args.gate.write_text("\n".join(gate_lines) + "\n")

    output = {
        "field": "Q(omega), omega^2+omega+1=0",
        "variables": len(variables),
        "equations": data["mixed_equation_count"],
        "binomial_rows": len(binomials),
        "nonbinomial_rows": len(nonbinomials),
        "nonbinomial_term_profile": dict(sorted(Counter(
            len(row["terms"]) for row in nonbinomials
        ).items())),
        "exponent_rank_Q": rank,
        "free_laurent_dimension_before_constant_check": len(variables) - rank,
        "pivot_columns_zero_based": pivots,
        "snf_script": args.snf.name,
        "toric_gate_script": args.gate.name,
        "constant_convention": "x^(left-right)=-c_right/c_left",
    }
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True, default=str) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
