#!/usr/bin/env python3
"""Exact affine-fibre obstruction to one-bad star concentration.

After the anchor-safe two-bad retraction, anchors no longer have to be
preserved: any new one-bad source with the same four binary responses would
contradict the fixed-port cap theorem.  A natural attempt is therefore to
replace a multisite row by a literal coordinate port inside the affine joint
kernel of its two response maps.

This checker freezes the smallest physical common-square obstruction to that
step.  On six sites take

    q = 13:11 + 24:11 + 12:10 - 02:10 + 34:00,
    s = e_1 at site 5,
    p = e_1 at site 0 + e_1 at site 1.

Then q^[3]=0 and p*s*q^[2]=X_1.  The two p-components contribute X_1+Y
and -Y, respectively.  For the fixed physical q and s, the affine response
fibre has dimension nine but contains no scalar multiple of a literal target
coordinate port: its nine free directions are precisely response-zero
coordinate columns, while both displayed p-components are forced.

This is not a full one-bad packet: it omits the second response colour and
has zero unary top.  It identifies the exact missing theorem.  The full top
and all four response rows must rule out multisite cancellation circuits;
the aggregate response identities alone do not permit coordinate
concentration.
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
    "computations/verify_shared_reciprocal_two_bad_anchor_safe_retraction.py":
        "a280b40657f2ab02c9c9f6ecf50dd3326db12bcc20614cbbd12bddffac8a1b62",
    "computations/verify_n8_one_bad_direct_permanent_null_descent.py":
        "4d7ea4e4e992142780ffd58f685177d1e3c958f5eec5c1bab2afd4404feb1043",
}
EXPECTED_LEDGER_SHA256 = (
    "742dfea9c22dfee03112d9b89f8922a144a28eb7e9d39edce7c24041e2093ae0"
)

SITES = tuple(range(6))
COLOURS = tuple(range(3))
TARGET = 1
X_TARGET = (TARGET,) * 6
MIXED_DEBT = (1, 1, 0, 0, 0, 1)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"dependency changed: {relative}: {actual}")


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def cell(u, v, i, j):
    if u > v:
        u, v, i, j = v, u, j, i
    return u, v, i, j


def q_data():
    return {
        cell(1, 3, 1, 1): Fraction(1),
        cell(2, 4, 1, 1): Fraction(1),
        cell(1, 2, 1, 0): Fraction(1),
        cell(0, 2, 1, 0): Fraction(-1),
        cell(3, 4, 0, 0): Fraction(1),
    }


def hafnian_tensor(q, vertices):
    vertices = tuple(sorted(vertices))
    output = Counter()
    for matching in perfect_matchings(vertices):
        choices = []
        for u, v in matching:
            choices.append([
                (i, j, coefficient)
                for (a, b, i, j), coefficient in q.items()
                if (a, b) == (u, v) and coefficient
            ])
        for selected in itertools.product(*choices):
            word = {}
            coefficient = Fraction(1)
            for (u, v), (i, j, value) in zip(
                    matching, selected, strict=True):
                word[u], word[v] = i, j
                coefficient *= value
            output[tuple(word[u] for u in vertices)] += coefficient
    return Counter({word: coefficient
                    for word, coefficient in output.items() if coefficient})


def response(q, p, s):
    """Compute p*s*q^[2] with both ordered hole choices retained."""
    output = Counter()
    for u, i, p_coefficient in p:
        for v, j, s_coefficient in s:
            if u == v:
                continue
            complement = tuple(site for site in SITES if site not in (u, v))
            cofactor = hafnian_tensor(q, complement)
            for cofactor_word, coefficient in cofactor.items():
                word = [None] * 6
                word[u], word[v] = i, j
                for site, colour in zip(
                        complement, cofactor_word, strict=True):
                    word[site] = colour
                output[tuple(word)] += (
                    p_coefficient * s_coefficient * coefficient
                )
    return Counter({word: coefficient
                    for word, coefficient in output.items() if coefficient})


def matrix_rank(rows):
    matrix = [[Fraction(value) for value in row] for row in rows]
    if not matrix:
        return 0
    row = 0
    for column in range(len(matrix[0])):
        pivot = next((index for index in range(row, len(matrix))
                      if matrix[index][column]), None)
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        value = matrix[row][column]
        matrix[row] = [entry / value for entry in matrix[row]]
        for index in range(len(matrix)):
            if index == row or not matrix[index][column]:
                continue
            value = matrix[index][column]
            matrix[index] = [entry - value * pivot_entry
                             for entry, pivot_entry
                             in zip(matrix[index], matrix[row], strict=True)]
        row += 1
    return row


def affine_fibre_audit(q):
    s = ((5, 1, Fraction(1)),)
    p0 = ((0, 1, Fraction(1)),)
    p1 = ((1, 1, Fraction(1)),)
    p = p0 + p1
    contribution0 = response(q, p0, s)
    contribution1 = response(q, p1, s)
    require(contribution0 == Counter({
        X_TARGET: Fraction(1), MIXED_DEBT: Fraction(1),
    }), f"the first multisite contribution changed: {contribution0}")
    require(contribution1 == Counter({MIXED_DEBT: Fraction(-1)}),
            f"the cancelling multisite contribution changed: {contribution1}")
    require(response(q, p, s) == Counter({X_TARGET: Fraction(1)}),
            "the exact pure response changed")

    coordinate_columns = []
    words = {X_TARGET}
    for site in SITES:
        for colour in COLOURS:
            column = response(
                q, ((site, colour, Fraction(1)),), s
            )
            coordinate_columns.append((site, colour, column))
            words.update(column)
    words = tuple(sorted(words))
    matrix = [
        [column.get(word, Fraction(0))
         for _site, _colour, column in coordinate_columns]
        for word in words
    ]
    target = [Fraction(int(word == X_TARGET)) for word in words]
    rank = matrix_rank(matrix)
    augmented_rank = matrix_rank([
        row + [target[index]] for index, row in enumerate(matrix)
    ])
    zero_columns = [
        (site, colour) for site, colour, column in coordinate_columns
        if not column
    ]
    literal_target_columns = []
    for site, colour, column in coordinate_columns:
        if not column or any(word != X_TARGET for word in column):
            continue
        if column[X_TARGET]:
            literal_target_columns.append((site, colour, column[X_TARGET]))

    require((len(words), rank, augmented_rank) == (11, 9, 9),
            "the affine response rank ledger changed")
    require(len(zero_columns) == 9 and not literal_target_columns,
            "the affine fibre acquired a literal target coordinate")

    # The nine nonzero coordinate columns are independent.  Therefore the
    # affine solution fixes their coefficients uniquely; its nine-dimensional
    # kernel consists exactly of the response-zero coordinate columns.
    nonzero_matrix = [
        [column.get(word, Fraction(0))
         for _site, _colour, column in coordinate_columns if column]
        for word in words
    ]
    require(matrix_rank(nonzero_matrix) == 9,
            "a new nontrivial joint-kernel direction appeared")
    return {
        "q_cells": [
            f"{u}{v}:{i}{j}={coefficient}"
            for (u, v, i, j), coefficient in sorted(q.items())
        ],
        "fixed_s": "e1@5",
        "multisite_p": ["e1@0", "e1@1"],
        "p0_contribution": "X1+Y",
        "p1_contribution": "-Y",
        "Y_word": list(MIXED_DEBT),
        "response": "X1",
        "coordinate_domain_dimension": 18,
        "response_word_rows": len(words),
        "response_map_rank": rank,
        "affine_fibre_dimension": 18 - rank,
        "response_zero_coordinate_columns": [list(item)
                                               for item in zero_columns],
        "literal_target_columns": literal_target_columns,
        "forced_nonzero_coordinates": ["e1@0", "e1@1"],
    }


def symbolic_gate():
    # For fixed F=q^[2] and s=(s1,s2), define
    # L_s(v)=(v*s1*F,v*s2*F).  Replacing p_i by p_i+k is exact iff k lies
    # in the joint kernel.  This is an algebraic identity, checked here in a
    # formal two-output vector space rather than by a support implication.
    x1, x2 = (Fraction(2), Fraction(-3)), (Fraction(5), Fraction(7))
    k = (Fraction(11), Fraction(13))
    minus_k = tuple(-value for value in k)

    def add(left, right):
        return tuple(a + b for a, b in zip(left, right, strict=True))

    require(add(k, minus_k) == (0, 0),
            "the formal joint-kernel replacement identity changed")
    require(add(x1, add(k, minus_k)) == x1
            and add(x2, add(k, minus_k)) == x2,
            "joint-kernel translation stopped preserving responses")
    return {
        "left_affine_fibres": [
            "A1={v:L_s(v)=(X1,0)}=p1+ker(L_s)",
            "A2={v:L_s(v)=(0,X2)}=p2+ker(L_s)",
        ],
        "right_affine_fibres_after_left_choice": [
            "B1={w:M_p(w)=(X1,0)}",
            "B2={w:M_p(w)=(0,X2)}",
        ],
        "coordinate_concentration_criterion": (
            "each affine fibre must meet a target coordinate line; the four "
            "resulting candidate-site sets must have an SDR"
        ),
        "equations_supply": (
            "nonempty affine fibres only; they do not imply intersection "
            "with the union of target coordinate lines"
        ),
    }


def main():
    pin_dependencies()
    q = q_data()
    require(len(q) == 5, "the physical affine-fibre guard changed size")
    top = hafnian_tensor(q, SITES)
    require(top == Counter(), "the guard acquired a unary top coefficient")
    affine = affine_fibre_audit(q)
    gate = symbolic_gate()
    ledger = {
        "pins": PINS,
        "scope_correction": (
            "after the pinned anchor-safe reduction, a new one-bad source "
            "need not preserve anchors; only its unary top and four binary "
            "response tensors must remain exact"
        ),
        "affine_joint_kernel_gate": gate,
        "physical_common_square_guard": affine,
        "guard_q_cubed": 0,
        "verdict": (
            "aggregate response exactness does not by itself allow literal "
            "coordinate concentration: an exact physical q^[2] response "
            "fibre can force two multisite coordinates and contain no literal "
            "target port"
        ),
        "remaining_full_packet_theorem": (
            "use q^[3]=X0 together with the second diagonal response and both "
            "cross-zero responses to exclude every such multisite cancellation "
            "circuit, then prove Hall for four distinct candidate sites; or "
            "route the resulting nonzero second-insertion curvature through a "
            "second physical good pair"
        ),
        "scope": (
            "source-faithful counterguard to response-only affine "
            "concentration; it is not a full one-bad packet because the unary "
            "top and second response colour are absent"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"one-bad affine concentration guard changed: {digest}")

    print("N=8 one-bad affine coordinate-concentration guard: PASS")
    print("physical q cells / response rank / affine dimension: 5 / 9 / 9")
    print("exact response: (e1@0+e1@1)*(e1@5)*q^[2]=X1")
    print("literal target-coordinate ports in affine fibre: 0")
    print("remaining input: unary top + second diagonal + both cross zeros")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
