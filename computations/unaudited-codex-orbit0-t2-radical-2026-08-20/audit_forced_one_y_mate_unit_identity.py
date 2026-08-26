#!/usr/bin/env python3
"""Exact universal unit identity for the forced one-y diagonal mate.

Fix the left branch-51 one-y axis with Q support
{0,1,3,5,6,9,10,12}.  Its literal entry/cofactor support forces a mate to
have zero entries {3,7,9,10,13,14,19,23}; the 4+4 packet forces Q3=Q5=0.
This checker rebuilds the normalized diagonal source rows from raw endpoint
order and verifies an integral polynomial identity putting 2 in that ideal.
No selected cofactor-branch equation or H inverse is used, so the identity
simultaneously excludes the three support-level mate branches 7,25,42.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_forced_one_y_mate_unit_identity.json"
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
FORCED_ZERO_CELLS = (3, 7, 9, 10, 13, 14, 19, 23)
MATE_Q_SUPPORT = (0, 1, 2, 4, 7, 8, 11, 13)
MATE_BRANCHES = (7, 25, 42)

Poly = Counter[tuple[int, ...]]
ONE: Poly = Counter({(): 1})


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def clean(poly):
    return Counter({monomial: coefficient
                    for monomial, coefficient in poly.items() if coefficient})


def add(*polys):
    answer = Counter()
    for poly in polys:
        answer.update(poly)
    return clean(answer)


def scale(poly, scalar):
    return clean(Counter({monomial: scalar * coefficient
                          for monomial, coefficient in poly.items()}))


def multiply(*polys):
    answer = ONE
    for poly in polys:
        updated = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in poly.items():
                updated[tuple(sorted(left + right))] += (
                    left_coefficient * right_coefficient
                )
        answer = clean(updated)
    return answer


def variable(index):
    return Counter({(index,): 1})


def entry(i, j, clone_i, clone_j, offset=0):
    if i > j:
        i, j = j, i
        clone_i, clone_j = clone_j, clone_i
    return variable(offset + 4 * EDGE_INDEX[(i, j)]
                    + 2 * clone_i + clone_j)


def permanent(i, j):
    return add(multiply(entry(i, j, 0, 0), entry(i, j, 1, 1)),
               multiply(entry(i, j, 0, 1), entry(i, j, 1, 0)))


def e_row(i, j):
    return add(ONE, permanent(i, j))


def triangle(i, j, k):
    answer = Counter()
    for x, y, z in product((0, 1), repeat=3):
        answer = add(answer, multiply(
            entry(i, j, x, y),
            entry(i, k, 1 - x, z),
            entry(j, k, 1 - y, 1 - z),
        ))
    return answer


def t_row(i, j, k):
    return add(ONE, permanent(i, j), permanent(i, k), permanent(j, k),
               triangle(i, j, k))


def q_row(index, offset=0):
    bits = tuple((index >> (3 - site)) & 1 for site in range(4))
    answer = Counter()
    for (i, j), (k, l) in (((0, 1), (2, 3)),
                           ((0, 2), (1, 3)),
                           ((0, 3), (1, 2))):
        answer = add(answer, multiply(
            entry(i, j, bits[i], bits[j], offset),
            entry(k, l, bits[k], bits[l], offset),
        ))
    return answer


def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        answer.extend((((first, second),) + tail)
                      for tail in perfect_matchings(rest))
    return tuple(answer)


PM8 = perfect_matchings(tuple(range(8)))


def one_colour_word_row(word, active_colour=0):
    """Diagonal specialization: internal anchors are 1, mixed edges are 0."""
    answer = Counter()
    for matching in PM8:
        term = ONE
        for u, v in matching:
            if word[u] != word[v]:
                term = Counter()
                break
            super_u, clone_u = divmod(u, 2)
            super_v, clone_v = divmod(v, 2)
            if super_u == super_v:
                continue
            # Only active_colour appears on more than one supervertex in the
            # six labels below.  This guard catches a bad label silently
            # introducing a second block family.
            require(word[u] == active_colour,
                    "source label uses an unexpected repeated colour")
            term = multiply(term, entry(super_u, super_v,
                                        clone_u, clone_v))
        answer = add(answer, term)
    return answer


def two_colour_word_row(word, left_colour=0, mate_colour=1):
    """Literal diagonal 4+4 row with independent left/mate 24-cell blocks."""
    answer = Counter()
    for matching in PM8:
        term = ONE
        for u, v in matching:
            if word[u] != word[v]:
                term = Counter()
                break
            super_u, clone_u = divmod(u, 2)
            super_v, clone_v = divmod(v, 2)
            require(super_u != super_v,
                    "a 4+4 word unexpectedly used an internal anchor")
            colour = word[u]
            require(colour in (left_colour, mate_colour),
                    "unexpected colour in 4+4 label")
            offset = 0 if colour == left_colour else 24
            term = multiply(term, entry(super_u, super_v,
                                        clone_u, clone_v, offset))
        answer = add(answer, term)
    return answer


def serialize(poly):
    return [{"coefficient": coefficient, "variables": list(monomial)}
            for monomial, coefficient in sorted(poly.items())]


# Exact Q(r), r^2+2r-1=0 arithmetic for the punctured one-y axis.  Thus this
# r is sqrt(2)-1, not the sqrt(2) basis element used in some sibling files.
def qr(value=0, r_coefficient=0):
    return (Fraction(value), Fraction(r_coefficient))


def qr_add(left, right):
    return (left[0] + right[0], left[1] + right[1])


def qr_mul(left, right):
    return (left[0] * right[0] + left[1] * right[1],
            left[0] * right[1] + left[1] * right[0]
            - 2 * left[1] * right[1])


def evaluate(poly, values):
    answer = qr()
    for monomial, coefficient in poly.items():
        term = qr(coefficient)
        for index in monomial:
            term = qr_mul(term, values[index])
        answer = qr_add(answer, term)
    return answer


def derivative(poly, index):
    answer = Counter()
    for monomial, coefficient in poly.items():
        multiplicity = monomial.count(index)
        if multiplicity:
            reduced = list(monomial)
            reduced.remove(index)
            answer[tuple(reduced)] += coefficient * multiplicity
    return clean(answer)


def main():
    require(len(PM8) == 105, "raw perfect-matching count changed")

    # Rebuild the fixed left signature rather than accepting its masks as an
    # external combinatorial input.  This is the Q1 punctured axis at scale
    # one in the exact d=0 normal form.
    r = qr(0, 1)
    left_a = (qr(Fraction(27, 40), Fraction(13, 40)),
              qr(Fraction(1, 40), Fraction(-13, 40)),
              qr(Fraction(-1, 10)), qr(Fraction(3, 10)),
              qr(Fraction(-9, 40), Fraction(-1, 40)),
              qr(Fraction(-7, 40), Fraction(1, 40)))
    left_b = (r, qr(-2, -1), qr(1), qr(-2, -1), qr(1), qr(1))
    left_c = (qr(-2, -1), r, qr(-1), r, qr(-1), qr(-1))
    left_values = []
    for edge in range(6):
        left_values.extend((left_a[edge], left_b[edge],
                            left_c[edge], qr()))
    left_values = tuple(left_values)
    pure_h = one_colour_word_row((0,) * 8)
    left_cofactors = tuple(evaluate(derivative(pure_h, index), left_values)
                           for index in range(24))
    left_q = tuple(evaluate(q_row(index), left_values)
                   for index in range(16))
    left_entry_live = tuple(index for index, value in enumerate(left_values)
                            if value != qr())
    left_cofactor_live = tuple(index for index, value
                               in enumerate(left_cofactors) if value != qr())
    left_q_live = tuple(index for index, value in enumerate(left_q)
                        if value != qr())
    require(left_entry_live ==
            (0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14,
             16, 17, 18, 20, 21, 22),
            "normalized one-y entry signature changed")
    require(left_cofactor_live == (3, 7, 9, 10, 13, 14, 19, 23),
            "normalized one-y cofactor signature changed")
    require(left_q_live == (0, 1, 3, 5, 6, 9, 10, 12),
            "normalized one-y Q signature changed")
    require(evaluate(pure_h, left_values) == qr(4),
            "normalized one-y H changed")

    source_words = {
        "e01": "00001122",
        "e02": "00110022",
        "e12": "11000022",
        "e13": "11002200",
        "e23": "11220000",
        "t123": "11000000",
        # Colour 0 is the fixed left axis and colour 1 is the mate.  Thus
        # these factor as Q12(left)Q3(mate) and Q10(left)Q5(mate).
        "Q3_mate_with_Q12_left": "10100101",
        "Q5_mate_with_Q10_left": "10011001",
    }
    expected_one_colour = {
        "e01": e_row(0, 1), "e02": e_row(0, 2),
        "e12": e_row(1, 2), "e13": e_row(1, 3),
        "e23": e_row(2, 3), "t123": t_row(1, 2, 3),
    }
    for label, expected in expected_one_colour.items():
        word = tuple(map(int, source_words[label]))
        require(one_colour_word_row(word) == expected,
                f"raw source label changed for {label}")

    q3_word = tuple(map(int, source_words["Q3_mate_with_Q12_left"]))
    q5_word = tuple(map(int, source_words["Q5_mate_with_Q10_left"]))
    require(two_colour_word_row(q3_word) ==
            multiply(q_row(12), q_row(3, 24)),
            "raw Q12(left)Q3(mate) factorization changed")
    require(two_colour_word_row(q5_word) ==
            multiply(q_row(10), q_row(5, 24)),
            "raw Q10(left)Q5(mate) factorization changed")

    x = tuple(variable(index) for index in range(24))
    source_row_multipliers = {
        "e01": multiply(x[15], x[16], x[21]),
        "e02": multiply(x[15], x[17], x[20]),
        "e12": ONE, "e13": ONE, "e23": ONE,
        "t123": scale(ONE, -1),
        "Q3": scale(multiply(x[6], x[15], x[20]), -1),
        "Q5": scale(multiply(x[2], x[15], x[16]), -1),
    }
    source_rows = {
        "e01": e_row(0, 1), "e02": e_row(0, 2),
        "e12": e_row(1, 2), "e13": e_row(1, 3),
        "e23": e_row(2, 3), "t123": t_row(1, 2, 3),
        "Q3": q_row(3), "Q5": q_row(5),
    }
    core = add(*(multiply(source_row_multipliers[label], row)
                 for label, row in source_rows.items()))
    entry_correction_multipliers = {
        3: scale(multiply(x[0], x[15], x[16], x[21]), -1),
        7: scale(multiply(x[4], x[15], x[17], x[20]), -1),
        13: add(multiply(x[6], x[9], x[15], x[20]),
                multiply(x[18], x[21])),
        14: add(multiply(x[2], x[9], x[15], x[16]),
                multiply(x[17], x[22])),
        19: add(multiply(x[2], x[4], x[15], x[16]),
                multiply(x[13], x[20]), multiply(x[12], x[22])),
        23: add(multiply(x[0], x[6], x[15], x[20]),
                multiply(x[14], x[16]), multiply(x[12], x[18])),
    }
    certificate = core
    for index, multiplier in entry_correction_multipliers.items():
        certificate = add(certificate, multiply(multiplier, x[index]))
    require(certificate == scale(ONE, 2),
            "forced-mate integral unit identity failed")
    require(set(entry_correction_multipliers) <= set(FORCED_ZERO_CELLS),
            "certificate used a cell not forced zero by the left signature")
    require(3 not in MATE_Q_SUPPORT and 5 not in MATE_Q_SUPPORT,
            "certificate Q rows are not forced by the mate support")

    # A sign mutation must break the literal identity.
    mutated = add(certificate, scale(t_row(1, 2, 3), 2))
    require(mutated != scale(ONE, 2), "t123 sign mutation did not fire")

    result = {
        "status": "UNAUDITED exact universal forced-one-y mate unit",
        "raw_endpoint_order": "supervertices 0,1,2,3; clones 0,1; cell 4*edge+2*x+y",
        "edge_order": [list(edge) for edge in EDGES],
        "fixed_left": {
            "branch_mask": 51,
            "Q_support": [0, 1, 3, 5, 6, 9, 10, 12],
            "entry_live_cells": [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13,
                                 14, 16, 17, 18, 20, 21, 22],
            "cofactor_live_cells": [3, 7, 9, 10, 13, 14, 19, 23],
            "raw_Qsqrt2_signature_rebuilt": True,
            "H": 4,
        },
        "forced_mate": {
            "Q_support": list(MATE_Q_SUPPORT),
            "branch_masks": list(MATE_BRANCHES),
            "entry_zero_cells": list(FORCED_ZERO_CELLS),
            "Q_zero_rows_used": [3, 5],
        },
        "source_words": source_words,
        "source_row_interpretation": {
            "eij": "literal pair-constant row specialized to 1+perm(Mij)",
            "t123": "literal triple row specialized to 1+P12+P13+P23+C123",
            "Q3": "word 10100101 is Q12(left)*Q3(mate); Q12(left) is live",
            "Q5": "word 10011001 is Q10(left)*Q5(mate); Q10(left) is live",
        },
        "unit_identity_mod_forced_entries": (
            "2 = x15*x16*x21*e01 + x15*x17*x20*e02 + e12 + e13 + e23 "
            "- t123 - x6*x15*x20*Q3 - x2*x15*x16*Q5"
        ),
        "source_row_multipliers": {
            label: serialize(multiplier)
            for label, multiplier in source_row_multipliers.items()
        },
        "entry_correction_multipliers": {
            str(index): serialize(multiplier)
            for index, multiplier in entry_correction_multipliers.items()
        },
        "certificate_polynomial": serialize(certificate),
        "certificate_equals": 2,
        "selected_cofactor_rows_used": 0,
        "H_inverse_used": False,
        "mutation_control": "flipping the t123 coefficient changes the polynomial",
        "conclusion": (
            "The forced mate ideal is the unit ideal over every field of "
            "characteristic not two before imposing any selected cofactor "
            "branch or H inverse. Hence branches 7,25,42 are all excluded."
        ),
        "scope": (
            "Exact on the normalized diagonal packet for the fixed one-y "
            "left axis. The identity is not a claim about off-diagonal source tails."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("forced one-y mate unit identity: PASS")
    print("raw source labels:", source_words)
    print("mate branches / forced zeros:", MATE_BRANCHES, FORCED_ZERO_CELLS)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
