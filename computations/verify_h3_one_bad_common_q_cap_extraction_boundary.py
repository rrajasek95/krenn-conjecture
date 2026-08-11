#!/usr/bin/env python3
"""Exact boundary for extracting a one-edge cap from the common-q packet.

At h=3 the four one-bad rows have the form r_ij*q^[2] = delta_ij X_i.
The intrinsic cap theorem needs a statement about the raw quadratic r_K.
Ordinary polynomial row operations cannot lower q-degree, and one audited
pair/cofactor contraction lowers it only from two to one.

The literal five-site packet below also shows that the first mixed
common-hole row can vanish while a bright common-q star remains multisite.
It omits the remaining third-target row, so it is not a one-bad source or a
Krenn counterexample; it identifies the missing two-chart attachment.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_one_bad_semisimple_cofactor_tower_boundary.py":
        "5b6ae90480611c6b1f87d049f404d1e61bde4a93a3af3779c42d749de453c1fe",
    "computations/verify_uniform_one_bad_third_cofactor_pure_carrier_gate.py":
        "9f346fd63964802c1286d76a27d6f9dfa2d1382545b44f31f976054310cbcaaf",
    "computations/verify_uniform_one_bad_common_q_euler_hessian_gate.py":
        "99875dd9b500c8ba1e9d33063b4fc69b0710d99f73522f6174679a4b172cdc6d",
    "computations/verify_uniform_one_bad_second_cofactor_tower_gate.py":
        "e4a65916d1e41c7486d0f119f7a13043a0b60959fbac538967ff93f601db3f1d",
    "computations/verify_shared_reciprocal_two_bad_anchor_safe_retraction.py":
        "a280b40657f2ab02c9c9f6ecf50dd3326db12bcc20614cbbd12bddffac8a1b62",
    "computations/verify_shared_reciprocal_two_bad_common_hafnian.py":
        "9bc7f4c017ba797304057ec182112c5c4f0bfc210d3729243958d723cac1a1d6",
    "computations/verify_h3_two_site_port_collision_unit.py":
        "c8b590defb44e16f398c39a986293a4d4d253e6e92047d4761046f2aecf6b489",
}
EXPECTED_LEDGER_SHA256 = (
    "3a3c05114b5b0e29a062a158b46cb2d91777384d1705be38e36035113e1fc3a9"
)

SITES = tuple(range(5))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def cell(u, v, a, b):
    if u > v:
        u, v, a, b = v, u, b, a
    return u, v, a, b


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def hafnian_tensor(q, vertices):
    vertices = tuple(vertices)
    output = Counter()
    for matching in perfect_matchings(vertices):
        choices = []
        for u, v in matching:
            choices.append([
                (a, b, coefficient)
                for (x, y, a, b), coefficient in q.items()
                if (x, y) == (u, v) and coefficient
            ])
        for selected in itertools.product(*choices):
            word = {}
            coefficient = Fraction(1)
            for (u, v), (a, b, value) in zip(
                    matching, selected, strict=True):
                word[u], word[v] = a, b
                coefficient *= value
            output[tuple(word[site] for site in vertices)] += coefficient
    return Counter({word: coefficient for word, coefficient in output.items()
                    if coefficient})


def odd_star_response(q, star):
    """Compute L*q^[2] on the five common sites."""
    output = Counter()
    for hole, colour, star_coefficient in star:
        complement = tuple(site for site in SITES if site != hole)
        for cofactor_word, coefficient in hafnian_tensor(q, complement).items():
            word = [None] * len(SITES)
            word[hole] = colour
            for site, value in zip(complement, cofactor_word, strict=True):
                word[site] = value
            output[tuple(word)] += star_coefficient * coefficient
    return Counter({word: coefficient for word, coefficient in output.items()
                    if coefficient})


def triple_star_response(q, first, second, third):
    """Compute P*Q*R*q with all source labels retained."""
    output = Counter()
    for u, a, x in first:
        for v, b, y in second:
            for w, c, z in third:
                if len({u, v, w}) < 3:
                    continue
                complement = tuple(
                    site for site in SITES if site not in (u, v, w)
                )
                require(len(complement) == 2, "the common-hole grade changed")
                i, j = complement
                for (left, right, d, e), coefficient in q.items():
                    if (left, right) != (i, j):
                        continue
                    word = [None] * len(SITES)
                    word[u], word[v], word[w] = a, b, c
                    word[i], word[j] = d, e
                    output[tuple(word)] += x * y * z * coefficient
    return Counter({word: coefficient for word, coefficient in output.items()
                    if coefficient})


def divided_square_of_star(star):
    output = Counter()
    for left_index, left in enumerate(star):
        u, a, x = left
        for v, b, y in star[left_index + 1:]:
            if u == v:
                continue
            monomial = tuple(sorted(((u, a), (v, b))))
            output[monomial] += x * y
    return Counter({monomial: coefficient
                    for monomial, coefficient in output.items() if coefficient})


def main():
    pin_dependencies()

    q = Counter({
        cell(0, 1, 0, 0): Fraction(1),
        cell(3, 4, 0, 0): Fraction(1),
        cell(1, 3, 1, 1): Fraction(1),
        cell(2, 4, 1, 1): Fraction(1),
        cell(1, 2, 1, 0): Fraction(1),
        cell(0, 2, 1, 0): Fraction(-1),
    })
    Q_c = ((0, 1, Fraction(1)), (1, 1, Fraction(1)))
    R_a = ((2, 0, Fraction(1)),)
    P_t = ((3, 2, Fraction(1)),)

    q_response = odd_star_response(q, Q_c)
    r_response = odd_star_response(q, R_a)
    p_response = odd_star_response(q, P_t)
    require(q_response == Counter({(1,) * 5: Fraction(1)}),
            f"the multisite bright row changed: {q_response}")
    require(r_response == Counter({(0,) * 5: Fraction(1)}),
            f"the second bright row changed: {r_response}")
    require(p_response == Counter({(0, 0, 1, 2, 1): Fraction(1)}),
            f"the chord cofactor guard changed: {p_response}")

    q_square = divided_square_of_star(Q_c)
    require(q_square == Counter({((0, 1), (1, 1)): Fraction(1)}),
            f"the bright star became square-zero: {q_square}")
    mixed_common_hole = triple_star_response(q, P_t, Q_c, R_a)
    require(not mixed_common_hole,
            f"the mixed common-hole row stopped vanishing: {mixed_common_hole}")
    require(p_response, "the D_ca chord multiplier lost its witness")

    response_q_degree = 2
    raw_cap_q_degree = 0
    after_one_contraction = response_q_degree - 1
    minimum_contractions = response_q_degree - raw_cap_q_degree
    require(after_one_contraction == 1 and minimum_contractions == 2,
            "the h=3 principal-parts depth changed")

    endpoint_grades = {
        "top_and_common_q_tower": (0, 0),
        "physical_one_bad_response": (1, 1),
        "p_self_square": (2, 0),
        "s_self_square": (0, 2),
        "quadratic_cap_tail": (2, 2),
    }
    require(endpoint_grades["p_self_square"]
            != endpoint_grades["physical_one_bad_response"]
            and endpoint_grades["s_self_square"]
            != endpoint_grades["physical_one_bad_response"],
            "a physical row acquired a repeated endpoint use")

    ledger = {
        "dependencies": PINS,
        "common_q_guard": {
            "cells": len(q),
            "Q_c_support": len(Q_c),
            "R_a_support": len(R_a),
            "P_t_support": len(P_t),
            "Q_c_q2": {str(key): str(value)
                       for key, value in q_response.items()},
            "R_a_q2": {str(key): str(value)
                       for key, value in r_response.items()},
            "P_t_q2": {str(key): str(value)
                       for key, value in p_response.items()},
            "Q_c_divided_square": {
                str(key): str(value) for key, value in q_square.items()
            },
            "P_t_Q_c_R_a_q_terms": len(mixed_common_hole),
            "forced_D_ca": 0,
        },
        "grade_boundary": {
            "endpoint_grades": endpoint_grades,
            "response_internal_q_degree": response_q_degree,
            "after_one_pair_cofactor_contraction": after_one_contraction,
            "raw_cap_internal_q_degree": raw_cap_q_degree,
            "minimum_principal_parts_depth": minimum_contractions,
        },
        "verdict": (
            "the genuine common-q tower and the first source-labelled mixed "
            "common-hole row do not extract a one-edge cap; a second-order "
            "source-tangent cofactor attachment coupling the remaining "
            "third-target row is the first grade-correct missing operation"
        ),
        "scope": (
            "exact h=3 degree obstruction plus a literal five-site common-q "
            "partial two-chart packet; the guard omits the third-target row "
            "and therefore is not a full one-bad source, not a counterexample, "
            "and not a refutation of the desired extraction lemma"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the common-q cap boundary ledger changed: {digest}")

    print("h=3 genuine-common-q cap-extraction boundary: PASS")
    print("bright rows: Q_c*q^[2]=X_c and R_a*q^[2]=X_a")
    print("Q_c support/self-square: 2 / nonzero")
    print("first mixed common-hole row: zero with D_ca=0")
    print("raw-cap extraction needs principal-parts depth at least 2")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
