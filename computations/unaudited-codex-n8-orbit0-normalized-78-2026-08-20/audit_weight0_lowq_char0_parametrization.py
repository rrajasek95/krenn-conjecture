#!/usr/bin/env python3
"""Exact characteristic-zero four-parameter low-Q cofactor family.

This is a pure-Python replay over K=Q(r,g), r^2=2, g^2=65.  It proves that
the proposed one-colour lemma "H nonzero plus cofactor viability implies at
least nine nonzero Q coordinates" is false in characteristic zero.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CORE_PATH = HERE / "audit_polarized_superpair_core_identity.py"
OUT = HERE / "results_weight0_lowq_char0_parametrization.json"
Q = Fraction
ZERO_K = (Q(0), Q(0), Q(0), Q(0))
ONE_K = (Q(1), Q(0), Q(0), Q(0))
R_K = (Q(0), Q(1), Q(0), Q(0))
G_K = (Q(0), Q(0), Q(1), Q(0))


def load_core():
    spec = importlib.util.spec_from_file_location("n8_lowq_core", CORE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE = load_core()


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def k_add(*values):
    return tuple(sum((value[index] for value in values), Q(0))
                 for index in range(4))


def k_neg(value):
    return tuple(-entry for entry in value)


def k_scale(value, scalar):
    scalar = Q(scalar)
    return tuple(scalar * entry for entry in value)


def k_mul(left, right):
    answer = [Q(0)] * 4
    basis = ((0, 0), (1, 0), (0, 1), (1, 1))
    for i, (ri, gi) in enumerate(basis):
        for j, (rj, gj) in enumerate(basis):
            coefficient = left[i] * right[j]
            if not coefficient:
                continue
            rsum, gsum = ri + rj, gi + gj
            if rsum >= 2:
                coefficient *= 2
                rsum -= 2
            if gsum >= 2:
                coefficient *= 65
                gsum -= 2
            index = {(0, 0): 0, (1, 0): 1,
                     (0, 1): 2, (1, 1): 3}[(rsum, gsum)]
            answer[index] += coefficient
    return tuple(answer)


def r_mul(left, right):
    return (left[0] * right[0] + 2 * left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def r_add(left, right):
    return (left[0] + right[0], left[1] + right[1])


def r_neg(value):
    return (-value[0], -value[1])


def r_inv(value):
    denominator = value[0] ** 2 - 2 * value[1] ** 2
    require(denominator != 0, "division by zero in Q(r)")
    return (value[0] / denominator, -value[1] / denominator)


def k_inv(value):
    x = (value[0], value[1])
    y = (value[2], value[3])
    denominator = r_add(r_mul(x, x),
                        r_neg((65 * r_mul(y, y)[0],
                               65 * r_mul(y, y)[1])))
    inverse_denominator = r_inv(denominator)
    x_part = r_mul(x, inverse_denominator)
    y_part = r_neg(r_mul(y, inverse_denominator))
    answer = (x_part[0], x_part[1], y_part[0], y_part[1])
    require(k_mul(value, answer) == ONE_K,
            "number-field inverse failed")
    return answer


def k_div(left, right):
    return k_mul(left, k_inv(right))


def k_is_zero(value):
    return value == ZERO_K


def k_encode(value):
    return [[entry.numerator, entry.denominator] for entry in value]


def k_string(value):
    names = ("1", "r", "g", "r*g")
    terms = []
    for coefficient, name in zip(value, names):
        if coefficient:
            terms.append(f"({coefficient})*{name}")
    return " + ".join(terms) if terms else "0"


# Laurent polynomials in (u,v,w,t), with K coefficients.
def lp_clean(poly):
    return {exponent: coefficient for exponent, coefficient in poly.items()
            if not k_is_zero(coefficient)}


def lp_const(value):
    return {} if k_is_zero(value) else {(0, 0, 0, 0): value}


def lp_monomial(coefficient, exponent):
    return {} if k_is_zero(coefficient) else {tuple(exponent): coefficient}


def lp_add(*polys):
    answer = {}
    for poly in polys:
        for exponent, coefficient in poly.items():
            answer[exponent] = k_add(answer.get(exponent, ZERO_K), coefficient)
    return lp_clean(answer)


def lp_neg(poly):
    return {exponent: k_neg(coefficient)
            for exponent, coefficient in poly.items()}


def lp_mul(*polys):
    answer = lp_const(ONE_K)
    for poly in polys:
        updated = {}
        for left_exponent, left_coefficient in answer.items():
            for right_exponent, right_coefficient in poly.items():
                exponent = tuple(left_exponent[index] + right_exponent[index]
                                 for index in range(4))
                coefficient = k_mul(left_coefficient, right_coefficient)
                updated[exponent] = k_add(updated.get(exponent, ZERO_K),
                                          coefficient)
        answer = lp_clean(updated)
    return answer


def lp_scale(poly, coefficient):
    return lp_clean({exponent: k_mul(coefficient, value)
                     for exponent, value in poly.items()})


def lp_inv_monomial(poly):
    require(len(poly) == 1, "attempt to invert a non-monomial Laurent poly")
    exponent, coefficient = next(iter(poly.items()))
    return lp_monomial(k_inv(coefficient), tuple(-value for value in exponent))


def lp_encode(poly):
    return [{"exponents_uvwt": list(exponent),
             "coefficient_1_r_g_rg": k_encode(coefficient),
             "coefficient": k_string(coefficient)}
            for exponent, coefficient in sorted(poly.items())]


def substitute(poly, entries):
    answer = {}
    for monomial, integer_coefficient in poly.items():
        term = lp_const(k_scale(ONE_K, integer_coefficient))
        for variable in monomial:
            term = lp_mul(term, entries[variable])
        answer = lp_add(answer, term)
    return answer


def derivative(poly, variable):
    answer = Counter()
    for monomial, coefficient in poly.items():
        multiplicity = monomial.count(variable)
        if multiplicity:
            reduced = list(monomial)
            reduced.remove(variable)
            answer[tuple(reduced)] += coefficient * multiplicity
    return Counter({monomial: coefficient for monomial, coefficient
                    in answer.items() if coefficient})


def main():
    rho = k_add(R_K, k_scale(ONE_K, -1))
    sigma = k_add(k_neg(R_K), k_scale(ONE_K, -1))
    eta = k_div(
        k_add(k_scale(rho, -5), k_scale(ONE_K, -12),
              k_mul(G_K, k_add(rho, k_scale(ONE_K, 2)))),
        k_scale(rho, 6),
    )
    require(k_mul(rho, rho) == k_add(k_scale(rho, -2), ONE_K),
            "rho relation changed")

    # b entries on the six edges; u,v,w,t exponent order.
    b = [
        lp_monomial(rho, (1, -1, 0, 0)),
        lp_monomial(sigma, (1, 0, -1, 0)),
        lp_monomial(ONE_K, (1, 0, 0, 0)),
        lp_monomial(sigma, (0, 1, -1, 0)),
        lp_monomial(ONE_K, (0, 1, 0, 0)),
        lp_monomial(ONE_K, (0, 0, 1, 0)),
    ]
    a = [None] * 6
    a[5] = lp_monomial(ONE_K, (0, 0, 0, 1))
    a[4] = lp_monomial(eta, (0, 1, -1, 1))
    a[3] = lp_monomial(k_add(k_mul(rho, eta), sigma), (0, 1, 0, 1))
    a2_coefficient = k_div(
        k_add(k_mul(k_add(k_scale(rho, -3), k_scale(ONE_K, -7)), eta),
              k_scale(rho, 5), k_scale(ONE_K, 13)),
        k_add(rho, k_scale(ONE_K, 5)),
    )
    a[2] = lp_monomial(a2_coefficient, (1, 0, -1, 1))
    a1_coefficient = k_div(
        k_add(k_mul(k_add(k_scale(rho, 7), k_scale(ONE_K, 3)), eta),
              k_scale(rho, -2), k_scale(ONE_K, -4)),
        k_add(rho, k_scale(ONE_K, 5)),
    )
    a[1] = lp_monomial(a1_coefficient, (1, 0, 0, 1))
    a[0] = lp_scale(lp_add(lp_mul(lp_monomial(ONE_K, (0, 1, 0, 0)), a[2]),
                               lp_mul(lp_monomial(ONE_K, (1, 0, 0, 0)), a[4])),
                    sigma)
    require(all(len(poly) == 1 for poly in a),
            "an a-entry ceased to be a Laurent monomial")

    entries = []
    blocks = []
    for edge in range(6):
        c = lp_neg(lp_inv_monomial(b[edge]))
        block = (a[edge], b[edge], c, {})
        blocks.append(block)
        entries.extend(block)
    require(len(entries) == 24, "entry census changed")

    z = CORE.pure_hafnian()
    orientation_bits = (1, 1, 0, 0, 1, 1)
    equations = []
    labels = []
    for edge in CORE.SUPER_EDGES:
        equations.append(CORE.e_pair(*edge))
        labels.append(f"e_{edge[0]}{edge[1]}")
    for triple in __import__("itertools").combinations(range(4), 3):
        equations.append(CORE.t_triple(*triple))
        labels.append("t_" + "".join(map(str, triple)))
    for edge_index, bit in enumerate(orientation_bits):
        selected = (1, 2) if bit else (0, 3)
        for entry in selected:
            equations.append(derivative(z, 4 * edge_index + entry))
            labels.append(f"cofactor_{edge_index}_{entry}")
    q_polys = [CORE.q_orientation(tuple((index >> (3 - site)) & 1
                                        for site in range(4)))
               for index in range(16)]
    q_zero_indices = (0, 2, 7, 8, 11, 13, 14, 15)
    for index in q_zero_indices:
        equations.append(q_polys[index])
        labels.append(f"Q_{index:04b}")
    evaluations = [substitute(poly, entries) for poly in equations]
    require(not any(evaluations),
            "a defining equation is nonzero on the parametrization")
    h_value = substitute(z, entries)
    require(h_value == lp_const(k_scale(ONE_K, 4)),
            "pure H is not the constant four")
    q_values = [substitute(poly, entries) for poly in q_polys]
    actual_q_zeros = tuple(index for index, value in enumerate(q_values)
                           if not value)
    require(actual_q_zeros == q_zero_indices,
            "Q zero support changed")
    require(all(len(value) == 1 for index, value in enumerate(q_values)
                if index not in q_zero_indices),
            "a live Q coordinate is not a Laurent unit")

    # A literal algebraic point is obtained by u=v=w=t=1.
    specialized_blocks = []
    for block in blocks:
        specialized_block = []
        for entry in block:
            value = ZERO_K
            for coefficient in entry.values():
                value = k_add(value, coefficient)
            specialized_block.append(value)
        specialized_blocks.append(specialized_block)

    result = {
        "status": "UNAUDITED exact characteristic-zero low-Q parametrization",
        "number_field": "K=Q(r,g), r^2=2, g^2=65",
        "basis_order": ["1", "r", "g", "r*g"],
        "rho": k_string(rho),
        "sigma": k_string(sigma),
        "eta": k_string(eta),
        "parameters": ["u", "v", "w", "t"],
        "parameter_domain": "u*v*w*t != 0",
        "edge_order": [list(edge) for edge in CORE.SUPER_EDGES],
        "block_formula": "M_e=[[a_e,b_e],[-1/b_e,0]]",
        "a_entries": [lp_encode(poly) for poly in a],
        "b_entries": [lp_encode(poly) for poly in b],
        "cofactor_orientation_bits_01_02_03_12_13_23": list(orientation_bits),
        "switching_class": 0,
        "triangle_parity_weight": 0,
        "defining_equations_checked": labels,
        "defining_equation_count": len(equations),
        "pure_H": lp_encode(h_value),
        "Q_zero_indices": list(actual_q_zeros),
        "Q_live_indices": [index for index in range(16)
                           if index not in actual_q_zeros],
        "Q_live_values": {str(index): lp_encode(q_values[index])
                          for index in range(16)
                          if index not in actual_q_zeros},
        "Q_support_size": 8,
        "specialization_u_v_w_t_equals_1": [
            [k_encode(entry) for entry in block]
            for block in specialized_blocks
        ],
        "conclusion": (
            "There is a four-parameter characteristic-zero family with all "
            "six permanents -1, all four triangle rows zero, the twelve "
            "chosen cofactor rows zero, H=4, and exactly eight nonzero Q "
            "coordinates. Therefore the proposed one-colour >=9-Q-support "
            "lemma is false in characteristic zero."
        ),
        "scope": (
            "This is a one-colour diagonal-block family. It does not provide "
            "a second breaker/cofactor-compatible live colour and is not a "
            "counterexample to the full normalized N=8 packet."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("weight-zero low-Q char0 parametrization: PASS")
    print("equations / H / Q support:", len(equations), 4,
          [index for index in range(16) if q_values[index]])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
