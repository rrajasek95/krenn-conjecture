#!/usr/bin/env python3
"""Exact compact unit on the parity-weight-four, d=0 Laurent chart.

Use branch mask 11 (bits 110100 in edge order 01,02,03,12,13,23) and

    M_e = [[a_e,b_e],[-1/b_e,0]],  product b_e != 0.

Literal substitution and monomial denominator clearing leave thirteen source
rows.  Five of them satisfy the compact identity checked below.  Their
combination is z*product(b_e), so adjoining z*product(b_e)-1 gives a unit.
No pure-H localization is used.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20"
DZERO_PATH = SOURCE / "analyze_weight0_dzero_lowq_chart.py"
OUT = HERE / "results_weight4_dzero_unit_identity.json"
BRANCH_MASK = 11
VARIABLE_COUNT = 13  # a0..a5,b0..b5,z
Q = Fraction


def load_dzero():
    spec = importlib.util.spec_from_file_location("n8_weight4_dzero_core",
                                                  DZERO_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DZERO = load_dzero()
CORE = DZERO.SCREEN.CORE
PROBE = DZERO.SCREEN.PROBE
ONE = {(0,) * VARIABLE_COUNT: Q(1)}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def clean(poly):
    return {monomial: coefficient for monomial, coefficient in poly.items()
            if coefficient}


def add(*polys):
    answer = Counter()
    for poly in polys:
        answer.update(poly)
    return clean(answer)


def scale(poly, coefficient):
    coefficient = Q(coefficient)
    return clean({monomial: coefficient * value
                  for monomial, value in poly.items()})


def multiply(*polys):
    answer = ONE
    for poly in polys:
        updated = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in poly.items():
                exponent = tuple(left[index] + right[index]
                                 for index in range(VARIABLE_COUNT))
                updated[exponent] += left_coefficient * right_coefficient
        answer = clean(updated)
    return answer


def variable(index, exponent=1):
    powers = [0] * VARIABLE_COUNT
    powers[index] = exponent
    return {tuple(powers): Q(1)}


def monomial(coefficient, **powers):
    answer = scale(ONE, coefficient)
    for name, exponent in powers.items():
        index = 12 if name == "z" else 6 + int(name[1:])
        answer = multiply(answer, variable(index, exponent))
    return answer


def embed(poly):
    return {tuple(exponent) + (0,): Q(coefficient)
            for exponent, coefficient in poly.items()}


def serialize(poly):
    return [{"exponents_a0_a5_b0_b5_z": list(exponent),
             "coefficient": [coefficient.numerator, coefficient.denominator]}
            for exponent, coefficient in sorted(poly.items())]


def main():
    bits = DZERO.SCREEN.branch_bits(BRANCH_MASK)
    equations, _ = PROBE.equations(bits)
    labels = (["e_" + "".join(map(str, edge))
               for edge in CORE.SUPER_EDGES]
              + ["t_" + "".join(map(str, triple))
                 for triple in combinations(range(4), 3)]
              + [f"cofactor_{edge}_{position}"
                 for edge, bit in enumerate(bits)
                 for position in ((1, 2) if bit else (0, 3))])
    derived = {}
    for label, raw in zip(labels, equations):
        substituted = DZERO.substitute(raw)
        if substituted:
            derived[label] = embed(DZERO.clear_denominators(substituted))
    expected_labels = (
        "t_012", "t_013", "t_023", "t_123",
        "cofactor_0_1", "cofactor_0_2", "cofactor_1_1",
        "cofactor_1_2", "cofactor_2_3", "cofactor_3_1",
        "cofactor_3_2", "cofactor_4_3", "cofactor_5_3",
    )
    require(tuple(derived) == expected_labels,
            "literal surviving-row labels changed")

    z = variable(12)
    coefficient_t013 = multiply(z, add(
        monomial(Q(-3, 8), b0=1, b3=2, b5=1),
        monomial(Q(3, 8), b0=1, b3=1, b4=1),
        monomial(Q(-1, 4), b1=1, b3=1, b5=1),
        monomial(1, b2=1, b3=1),
        monomial(Q(1, 4), b1=1, b4=1),
    ))
    coefficient_t023 = multiply(z, add(
        monomial(Q(-1, 8), b0=1, b3=2, b5=1),
        monomial(Q(-1, 8), b0=1, b3=1, b4=1),
        monomial(Q(-1, 4), b1=1, b3=1, b5=1),
        monomial(-1, b2=1, b3=1),
        monomial(Q(-1, 4), b1=1, b4=1),
    ))
    coefficient_c02 = multiply(z, add(
        monomial(Q(1, 8), b0=2, b3=1, b4=1),
        monomial(Q(1, 8), b0=1, b1=1, b3=1, b5=1),
        monomial(Q(1, 2), b0=1, b2=1, b3=1),
        monomial(Q(1, 4), b0=1, b1=1, b4=1),
        monomial(Q(1, 4), b1=2, b5=1),
        monomial(1, b1=1, b2=1),
    ))
    coefficient_c12 = multiply(z, add(
        monomial(Q(-3, 8), b0=2, b3=1, b4=1),
        monomial(Q(-1, 8), b0=1, b1=1, b3=1, b5=1),
        monomial(Q(-5, 4), b0=1, b2=1, b3=1),
        monomial(Q(-1, 4), b0=1, b1=1, b4=1),
        monomial(Q(1, 4), b1=2, b5=1),
        monomial(Q(1, 2), b1=1, b2=1),
    ))
    coefficient_c32 = multiply(z, add(
        monomial(Q(-1, 4), b0=1, b3=2, b5=1),
        monomial(Q(-1, 2), b1=1, b4=1),
    ))
    packet = add(
        multiply(coefficient_t013, derived["t_013"]),
        multiply(coefficient_t023, derived["t_023"]),
        multiply(coefficient_c02, derived["cofactor_0_2"]),
        multiply(coefficient_c12, derived["cofactor_1_2"]),
        multiply(coefficient_c32, derived["cofactor_3_2"]),
    )
    b_product = multiply(*(variable(6 + edge) for edge in range(6)))
    target = multiply(z, b_product)
    require(packet == target,
            "the parity-weight-four Laurent unit identity failed")

    # Removing the last packet summand must break the identity.
    mutation = add(packet,
                   scale(multiply(coefficient_c32,
                                  derived["cofactor_3_2"]), -1))
    require(mutation != target, "packet mutation did not fire")

    source_terms = (
        ("t_013", coefficient_t013),
        ("t_023", coefficient_t023),
        ("cofactor_0_2", coefficient_c02),
        ("cofactor_1_2", coefficient_c12),
        ("cofactor_3_2", coefficient_c32),
    )
    result = {
        "status": "UNAUDITED exact parity-weight-four d=0 unit identity",
        "branch_mask": BRANCH_MASK,
        "branch_bits_01_02_03_12_13_23": list(bits),
        "triangle_parity_weight": 4,
        "localized_chart": "M_e=[[a_e,b_e],[-1/b_e,0]], product b_e != 0",
        "literal_surviving_row_labels": list(derived),
        "identity": "sum five displayed source multiples = z*b0*b1*b2*b3*b4*b5",
        "source_terms": [
            {"label": label, "multiplier": serialize(multiplier),
             "cleared_source_row": serialize(derived[label])}
            for label, multiplier in source_terms
        ],
        "source_term_count": len(source_terms),
        "collected_packet_term_count": len(packet),
        "target": serialize(target),
        "conclusion": (
            "After adjoining z*product(b_e)-1, these five literal cleared "
            "source rows generate 1. Therefore this Laurent chart is empty "
            "over every characteristic-zero field; H localization is not "
            "needed."
        ),
        "scope": (
            "This closes branch mask 11 on the uniform d=0 cell chart and, "
            "by the anchor stabilizer, its transforms. It does not close "
            "other joint cofactor/cell-zero charts."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("weight-four d=0 unit identity: PASS")
    print("surviving / used rows / collected terms:", len(derived),
          len(source_terms), len(packet))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
