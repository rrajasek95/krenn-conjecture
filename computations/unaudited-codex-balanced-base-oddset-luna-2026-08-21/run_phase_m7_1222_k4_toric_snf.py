#!/usr/bin/env python3
"""Parse SNF, check Laurent constants, and substitute the 1222-k4 target."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import argparse
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_balanced_base_oddset_luna import ZERO, ONE, qadd, qmul, qlabel  # noqa: E402
from audit_phase_m7_1222_k4_toric import parse_q  # noqa: E402


INPUT = HERE / "results_phase_m7_1222_k4_sat_coefficient_target.json"
SCRIPT = HERE / "verify_phase_m7_1222_k4_toric_snf.sing"
OUT = HERE / "results_phase_m7_1222_k4_toric_snf.json"


def qneg(value):
    return -value[0], -value[1]


def qinv(value):
    a, b = value
    norm = a * a - a * b + b * b
    if not norm:
        raise ZeroDivisionError(value)
    return (a - b) / norm, -b / norm


def qpow(value, exponent):
    if exponent < 0:
        return qpow(qinv(value), -exponent)
    answer = ONE
    base = value
    power = exponent
    while power:
        if power & 1:
            answer = qmul(answer, base)
        base = qmul(base, base)
        power //= 2
    return answer


def qdiv(left, right):
    return qmul(left, qinv(right))


def parse_matrix(stdout, begin, end, rows, columns):
    body = stdout.split(begin, 1)[1].split(end, 1)[0]
    values = []
    for token in body.replace("\n", ",").split(","):
        token = token.strip()
        if token:
            values.append(int(token))
    if len(values) != rows * columns:
        raise RuntimeError((begin, len(values), rows * columns))
    return [values[index * columns:(index + 1) * columns]
            for index in range(rows)]


def polynomial_after_substitution(row, variable_index, q_matrix, rank,
                                  x_constants):
    answer = defaultdict(lambda: ZERO)
    for term in row["terms"]:
        coefficient = parse_q(term["coefficient"])
        old_exponents = Counter(term["monomial"])
        free_exponents = [0] * (len(q_matrix) - rank)
        for name, exponent in old_exponents.items():
            index = variable_index[name]
            coefficient = qmul(coefficient, qpow(x_constants[index], exponent))
            for free in range(rank, len(q_matrix)):
                free_exponents[free - rank] += exponent * q_matrix[index][free]
        key = tuple(free_exponents)
        answer[key] = qadd(answer[key], coefficient)
    return {key: value for key, value in answer.items() if value != ZERO}


def term_json(exponents, coefficient):
    return {
        "coefficient": qlabel(coefficient),
        "laurent_exponents": {
            f"t{index + 1}": value for index, value in enumerate(exponents) if value
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--script", type=Path, default=SCRIPT)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    data = json.loads(args.input.read_text())["coefficient_system"]
    variables = data["variables"]
    binomial_rows = [row for row in data["equations"] if len(row["terms"]) == 2]
    row_count = len(binomial_rows)
    variable_count = len(variables)
    completed = subprocess.run(
        ["Singular", "-q", args.script.name], cwd=HERE, capture_output=True,
        text=True, timeout=120, check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError((completed.returncode, completed.stderr[-1000:]))
    d_matrix = parse_matrix(completed.stdout, "SNF_D_BEGIN", "SNF_D_END",
                            row_count, variable_count)
    p_matrix = parse_matrix(completed.stdout, "SNF_P_BEGIN", "SNF_P_END",
                            row_count, row_count)
    q_matrix = parse_matrix(completed.stdout, "SNF_Q_BEGIN", "SNF_Q_END",
                            variable_count, variable_count)
    invariants = [d_matrix[index][index]
                  for index in range(min(row_count, variable_count))
                  if d_matrix[index][index]]
    rank = len(invariants)
    variable_index = {name: index for index, name in enumerate(variables)}
    constants = []
    for row in binomial_rows:
        left, right = row["terms"]
        constants.append(qneg(qdiv(parse_q(right["coefficient"]),
                                   parse_q(left["coefficient"]))))
    transformed_constants = []
    for row in p_matrix:
        value = ONE
        for coefficient, exponent in zip(constants, row):
            value = qmul(value, qpow(coefficient, exponent))
        transformed_constants.append(value)
    bad_constant_rows = [index for index in range(rank, len(transformed_constants))
                         if transformed_constants[index] != ONE]
    constant_failure_certificates = []
    for index in bad_constant_rows:
        relation = []
        for binomial_index, exponent in enumerate(p_matrix[index]):
            if not exponent:
                continue
            row = binomial_rows[binomial_index]
            relation.append({
                "binomial_index": binomial_index,
                "word": row["word"],
                "degree": row["degree"],
                "power": exponent,
                "constant": qlabel(constants[binomial_index]),
                "equation_terms": row["terms"],
            })
        constant_failure_certificates.append({
            "snf_zero_row_zero_based": index,
            "relation_support": len(relation),
            "relation_l1_norm": sum(abs(item["power"]) for item in relation),
            "product_constant": qlabel(transformed_constants[index]),
            "contradiction_scalar": qlabel(qadd(transformed_constants[index], (-ONE[0], -ONE[1]))),
            "relation": relation,
        })
    constant_failure_certificates.sort(
        key=lambda item: (item["relation_support"], item["relation_l1_norm"],
                          item["snf_zero_row_zero_based"])
    )

    # Since every SNF invariant is one, y_i=k'_i for i<rank and the last
    # 82-rank y-coordinates are free.  Old x_j maps by the j-th row of Q.
    x_constants = []
    parameterization = []
    for variable, q_row in zip(variables, q_matrix):
        constant = ONE
        for index in range(rank):
            constant = qmul(constant,
                            qpow(transformed_constants[index], q_row[index]))
        x_constants.append(constant)
        parameterization.append({
            "source_variable": variable,
            "constant": qlabel(constant),
            "free_exponents": {
                f"t{index - rank + 1}": q_row[index]
                for index in range(rank, len(q_row)) if q_row[index]
            },
        })

    substituted = []
    binomial_failures = []
    residual_profile = Counter()
    monomial_rows = []
    for row in data["equations"]:
        polynomial = polynomial_after_substitution(
            row, variable_index, q_matrix, rank, x_constants,
        )
        record = {
            "word": row["word"], "degree": row["degree"],
            "terms": [term_json(exponents, coefficient)
                      for exponents, coefficient in sorted(polynomial.items())],
        }
        if len(row["terms"]) == 2:
            if polynomial:
                binomial_failures.append(record)
        elif polynomial:
            substituted.append(record)
            residual_profile[len(polynomial)] += 1
            if len(polynomial) == 1:
                monomial_rows.append(record)
    pure_row = {"terms": data["pure7"]}
    pure_polynomial = polynomial_after_substitution(
        pure_row, variable_index, q_matrix, rank, x_constants,
    )

    output = {
        "snf_invariants": invariants,
        "snf_rank": rank,
        "free_laurent_dimension": len(variables) - rank,
        "constant_relation_failures": bad_constant_rows,
        "constant_failure_certificates": constant_failure_certificates,
        "smallest_laurent_unit_certificate": (
            constant_failure_certificates[0] if constant_failure_certificates else None
        ),
        "binomial_substitution_failures": binomial_failures,
        "parameterization": parameterization,
        "residual_nonzero_rows": len(substituted),
        "residual_term_profile": {str(k): v for k, v in sorted(residual_profile.items())},
        "residual_monomial_rows": monomial_rows,
        "smallest_residual_row": min(
            substituted, key=lambda row: (len(row["terms"]), row["degree"], row["word"]),
            default=None,
        ),
        "pure7_after_substitution": [
            term_json(exponents, coefficient)
            for exponents, coefficient in sorted(pure_polynomial.items())
        ],
        "gate_rule": (
            "A residual monomial row is an exact Laurent unit obstruction. "
            "Otherwise dimension 23 exceeds the <=20 broad-gate guard."
        ),
    }
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "rank": rank,
        "invariants": dict(Counter(invariants)),
        "constant_failures": len(bad_constant_rows),
        "binomial_substitution_failures": len(binomial_failures),
        "free_dimension": len(variables) - rank,
        "residual_rows": len(substituted),
        "residual_profile": output["residual_term_profile"],
        "monomial_rows": len(monomial_rows),
        "pure7_terms": len(pure_polynomial),
        "smallest": output["smallest_residual_row"],
        "laurent_unit_certificate": output["smallest_laurent_unit_certificate"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
