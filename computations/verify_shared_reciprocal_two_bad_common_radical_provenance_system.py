#!/usr/bin/env python3
"""Freeze the common-q provenance ideal on the radical-pair branch.

Normalize the nondegenerate branch of the bright-pairing dichotomy by

    pi_t(Q_a)=pi_t(R_c)=e_0,
    pi_t(Q_t)=pi_t(R_t)=e_1.

The remaining local components are arbitrary.  This checker reconstructs
the complete five-site odd-star and nine full common-hafnian systems as
sparse integer polynomials (184 variables, 3645 rows), freezes their source
hash, and extracts the exact pure-target chord localization

    D_tt*R=1,  D_ac=0,  D_at=D_tc.

The latter has ordinary polynomial source certificates.  The checker does
not claim that the remaining 184-variable ideal is decided.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINNED_RADICAL_DICHOTOMY_SHA256 = (
    "ea5f5de02bd50e2a2eeb2cbc73d791b0899696d3769bb2d1937b5bc5f6b974ee"
)
PINNED_COMMON_HAFNIAN_SHA256 = (
    "9bc7f4c017ba797304057ec182112c5c4f0bfc210d3729243958d723cac1a1d6"
)
EXPECTED_SYSTEM_SHA256 = (
    "8089db4d27fb6babb25badd2081cc5fd80768d6e3f99f54ac90a5a26f5b3d214"
)
EXPECTED_LEDGER_SHA256 = "19bcdab49338f25ae6b28e3407994c288f7acfb54de9f1a77d6c35193254d1cc"

SITES = tuple(range(5))
COLOURS = tuple(range(3))
A, C, T = COLOURS
EDGES = tuple(itertools.combinations(SITES, 2))
ROW_NAMES = ("Qa", "Qc", "Qt", "Ra", "Rc", "Rt", "P")
Q_ROWS = ("Qa", "Qc", "Qt")
R_ROWS = ("Ra", "Rc", "Rt")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependencies():
    pins = {
        "computations/verify_shared_reciprocal_two_bad_bright_pairing_radical_dichotomy.py":
            PINNED_RADICAL_DICHOTOMY_SHA256,
        "computations/verify_shared_reciprocal_two_bad_common_hafnian.py":
            PINNED_COMMON_HAFNIAN_SHA256,
    }
    for relative, expected in pins.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"dependency changed: {relative}: {actual}")


def q_name(left, right, left_colour, right_colour):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return f"q{left}{right}{left_colour}{right_colour}"


Q_VARIABLES = tuple(
    q_name(left, right, left_colour, right_colour)
    for left, right in EDGES
    for left_colour in COLOURS for right_colour in COLOURS
)


def row_entry(row, site, colour):
    # Row operations within the two zero odd-star rows normalize the common
    # radical line and its complementary target direction.  All non-target
    # local entries, and every entry of the two affine bright rows and P,
    # remain free.
    if row in ("Qa", "Rc") and colour == T:
        return int(site == 0)
    if row in ("Qt", "Rt") and colour == T:
        return int(site == 1)
    return f"{row}{site}{colour}"


ROW_VARIABLES = tuple(sorted({
    value
    for row in ROW_NAMES for site in SITES for colour in COLOURS
    for value in (row_entry(row, site, colour),)
    if isinstance(value, str)
}))
D_VARIABLES = tuple(f"D{left}{right}"
                    for left in COLOURS for right in COLOURS)
VARIABLES = Q_VARIABLES + ROW_VARIABLES + D_VARIABLES


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def multiply(*factors):
    coefficient = 1
    variables = []
    for factor in factors:
        if factor == 0:
            return None
        if isinstance(factor, int):
            coefficient *= factor
        else:
            variables.append(factor)
    return coefficient, tuple(sorted(variables))


def add_term(polynomial, term, coefficient=1):
    if term is None:
        return
    term_coefficient, monomial = term
    polynomial[monomial] = (
        polynomial.get(monomial, 0) + coefficient * term_coefficient
    )
    if polynomial[monomial] == 0:
        del polynomial[monomial]


def add_polynomials(left, right, scale=1):
    answer = dict(left)
    for monomial, coefficient in right.items():
        answer[monomial] = answer.get(monomial, 0) + scale * coefficient
        if answer[monomial] == 0:
            del answer[monomial]
    return answer


def multiply_variable(polynomial, variable):
    answer = {}
    for monomial, coefficient in polynomial.items():
        add_term(answer, multiply(variable, *monomial), coefficient)
    return answer


def cofactor_polynomial(hole, word):
    vertices = tuple(site for site in SITES if site != hole)
    answer = {}
    for matching in perfect_matchings(vertices):
        add_term(answer, multiply(*(
            q_name(left, right, word[left], word[right])
            for left, right in matching
        )))
    require(len(answer) == 3,
            "a generic four-site cofactor lost a matching")
    return answer


def phi_polynomial(row, word):
    answer = {}
    for hole in SITES:
        entry = row_entry(row, hole, word[hole])
        for monomial, coefficient in cofactor_polynomial(hole, word).items():
            add_term(answer, multiply(entry, *monomial), coefficient)
    return answer


def product_polynomial(q_row, r_row, word):
    answer = {}
    for p_site, q_site, r_site in itertools.permutations(SITES, 3):
        residual = tuple(site for site in SITES
                         if site not in (p_site, q_site, r_site))
        require(len(residual) == 2,
                "a five-site kernel product lost its residual edge")
        add_term(answer, multiply(
            row_entry("P", p_site, word[p_site]),
            row_entry(q_row, q_site, word[q_site]),
            row_entry(r_row, r_site, word[r_site]),
            q_name(residual[0], residual[1],
                   word[residual[0]], word[residual[1]]),
        ))
    return answer


def build_system():
    words = tuple(itertools.product(COLOURS, repeat=5))
    equations = []
    labels = []
    odd_targets = {
        "Qa": None, "Qc": C, "Qt": None,
        "Ra": A, "Rc": None, "Rt": None,
    }
    for row in ("Qa", "Qc", "Qt", "Ra", "Rc", "Rt"):
        for word in words:
            polynomial = phi_polynomial(row, word)
            if odd_targets[row] is not None and word == (odd_targets[row],) * 5:
                polynomial = add_polynomials(polynomial, {(): -1})
            require(polynomial,
                    "a normalized odd-star source row vanished identically")
            equations.append(polynomial)
            labels.append(f"{row}:" + "".join(map(str, word)))

    for q_index, q_row in enumerate(Q_ROWS):
        for r_index, r_row in enumerate(R_ROWS):
            for word in words:
                polynomial = add_polynomials(
                    multiply_variable(phi_polynomial("P", word),
                                      f"D{q_index}{r_index}"),
                    product_polynomial(q_row, r_row, word),
                )
                if (q_index, r_index) == (T, T) and word == (T,) * 5:
                    polynomial = add_polynomials(polynomial, {(): -1})
                require(polynomial,
                        "a normalized full common-hafnian row vanished")
                equations.append(polynomial)
                labels.append(
                    f"F{q_index}{r_index}:" + "".join(map(str, word))
                )

    require(len(VARIABLES) == 184,
            "the normalized common-radical variable count changed")
    require(len(equations) == len(labels) == 3645,
            "the normalized common-radical source-row count changed")
    require(sum(len(polynomial) for polynomial in equations) == 139404,
            "the normalized common-radical sparse term count changed")
    return labels, equations


def system_digest(labels, equations):
    payload = json.dumps([
        (label, sorted((monomial, coefficient)
                       for monomial, coefficient in polynomial.items()))
        for label, polynomial in zip(labels, equations)
    ], separators=(",", ":"))
    return sha256(payload.encode()).hexdigest()


def polynomial_by_label(labels, equations, label):
    return equations[labels.index(label)]


def audit_pure_target_chord(labels, equations):
    target_word = "22222"
    k0 = cofactor_polynomial(0, (T,) * 5)
    k1 = cofactor_polynomial(1, (T,) * 5)
    require(polynomial_by_label(labels, equations, f"Qa:{target_word}") == k0,
            "the radical-line pure target kernel row changed")
    require(polynomial_by_label(labels, equations, f"Qt:{target_word}") == k1,
            "the complementary pure target kernel row changed")
    require(polynomial_by_label(labels, equations, f"Rc:{target_word}") == k0
            and polynomial_by_label(labels, equations, f"Rt:{target_word}") == k1,
            "the R-side pure target kernel rows changed")

    response = phi_polynomial("P", (T,) * 5)
    same_zero = multiply_variable(response, "D01")
    target = add_polynomials(
        multiply_variable(response, "D22"), {(): -1}
    )

    route = {}
    for p_site in (2, 3, 4):
        residual = tuple(site for site in SITES
                         if site not in (0, 1, p_site))
        add_term(route, multiply(
            row_entry("P", p_site, T),
            q_name(residual[0], residual[1], T, T),
        ))
    cross_02 = add_polynomials(
        multiply_variable(response, "D02"), route
    )
    cross_21 = add_polynomials(
        multiply_variable(response, "D21"), route
    )

    require(polynomial_by_label(labels, equations, f"F22:{target_word}") == target,
            "the all-target full equation acquired a tilted product term")
    require(polynomial_by_label(labels, equations, f"F01:{target_word}") == same_zero,
            "the same-radical full zero row changed")
    require(polynomial_by_label(labels, equations, f"F02:{target_word}") == cross_02,
            "the first crossed pure-target route changed")
    require(polynomial_by_label(labels, equations, f"F21:{target_word}") == cross_21,
            "the second crossed pure-target route changed")

    # Ordinary source certificates in the ideal generated by these rows:
    #   D01 = D22*(D01 R) - D01*(D22 R-1),
    #   D02-D21 = D22*((D02 R+S)-(D21 R+S))
    #              -(D02-D21)*(D22 R-1).
    d01_certificate = add_polynomials(
        multiply_variable(same_zero, "D22"),
        multiply_variable(target, "D01"), -1,
    )
    require(d01_certificate == {("D01",): 1},
            "the D_ac zero certificate changed")
    difference_rows = add_polynomials(cross_02, cross_21, -1)
    d_difference = {("D02",): 1, ("D21",): -1}
    difference_certificate = add_polynomials(
        multiply_variable(difference_rows, "D22"),
        {
            tuple(sorted(monomial + variable_monomial)): -coefficient * sign
            for monomial, coefficient in target.items()
            for variable_monomial, sign in ((('D02',), 1), (('D21',), -1))
        },
    )
    require(difference_certificate == d_difference,
            "the D_at=D_tc source certificate changed")

    return {
        "pure_kernel_rows": ["K0(2222)=0", "K1(2222)=0"],
        "response_R_terms": len(response),
        "cross_route_S_terms": len(route),
        "exact_consequences": [
            "D22*R=1", "D01=0", "D02=D21",
        ],
        "interpretation": (
            "the common-radical branch has a nonzero target chord D22 "
            "and nonzero controller response R; Q_t R_t q has zero raw "
            "all-target coefficient"
        ),
    }


def rational_rank(matrix):
    matrix = [[Fraction(value) for value in row] for row in matrix]
    row_count = len(matrix)
    column_count = len(matrix[0]) if matrix else 0
    pivot_row = 0
    pivot_columns = []
    for column in range(column_count):
        pivot = next((row for row in range(pivot_row, row_count)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                left - multiple * right
                for left, right in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return len(pivot_columns)


def audit_two_dimensional_projection_counterguard():
    # The shortcut X_a,X_c in im(Phi) => dim pi_t ker(Phi)<=1 is false
    # over Q, already for a seven-cell literal common quadratic.
    cells = {
        ((1, 2), 0, 0): Fraction(3, 5),
        ((0, 2), 0, 0): Fraction(4, 5),
        ((3, 4), 0, 0): Fraction(1),
        ((0, 1), 1, 1): Fraction(1),
        ((2, 3), 1, 1): Fraction(1),
        ((0, 2), 1, 0): Fraction(1),
        ((0, 2), 2, 0): Fraction(1),
    }
    words = tuple(itertools.product(COLOURS, repeat=5))
    labels = tuple(itertools.product(SITES, COLOURS))
    matrix = [[Fraction(0) for _ in labels] for _ in words]

    def cell_value(left, right, left_colour, right_colour):
        if left > right:
            left, right = right, left
            left_colour, right_colour = right_colour, left_colour
        return cells.get(((left, right), left_colour, right_colour),
                         Fraction(0))

    for word_index, word in enumerate(words):
        for hole in SITES:
            vertices = tuple(site for site in SITES if site != hole)
            coefficient = Fraction(0)
            for matching in perfect_matchings(vertices):
                term = Fraction(1)
                for left, right in matching:
                    term *= cell_value(left, right,
                                       word[left], word[right])
                coefficient += term
            matrix[word_index][labels.index((hole, word[hole]))] = coefficient

    rank = rational_rank(matrix)
    require(rank == 11,
            "the rational projection counterguard rank changed")

    def column_combination(vector):
        return [
            sum(row[index] * vector.get(label, 0)
                for index, label in enumerate(labels))
            for row in matrix
        ]

    pure = {
        colour: [Fraction(int(word == (colour,) * 5)) for word in words]
        for colour in COLOURS
    }
    require(column_combination({(0, A): Fraction(5, 3)}) == pure[A],
            "the rational counterguard lost X_a")
    require(column_combination({(4, C): Fraction(1)}) == pure[C],
            "the rational counterguard lost X_c")
    require(rational_rank([row + [pure[T][index]]
                           for index, row in enumerate(matrix)]) == rank + 1,
            "the rational counterguard acquired X_t in im(Phi)")

    kernel_rows = [
        {
            (0, A): Fraction(-4, 3),
            (0, C): Fraction(-5, 3),
            (0, T): Fraction(-5, 3),
            (1, A): Fraction(1),
        },
        {(3, A): Fraction(1)},
        {(3, C): Fraction(1)},
        {(3, T): Fraction(1)},
    ]
    zero = [Fraction(0)] * len(words)
    require(all(column_combination(vector) == zero
                for vector in kernel_rows),
            "a displayed counterguard kernel row stopped vanishing")
    target_projections = [
        [vector.get((site, T), 0) for site in SITES]
        for vector in kernel_rows
    ]
    require(rational_rank(target_projections) == 2,
            "the rational counterguard target projection changed")

    return {
        "cells": [
            [list(edge), left_colour, right_colour,
             [value.numerator, value.denominator]]
            for (edge, left_colour, right_colour), value in sorted(cells.items())
        ],
        "phi_rank": rank,
        "kernel_dimension": len(labels) - rank,
        "target_projection_dimension": 2,
        "pure_images": ["X_a", "X_c"],
        "excluded_pure": "X_t",
        "preimages": {"X_a": "(5/3)e_a@0", "X_c": "e_c@4"},
        "kernel_rows": [
            "(-4/3)e_a@0-(5/3)e_c@0-(5/3)e_t@0+e_a@1",
            "e_a@3", "e_c@3", "e_t@3",
        ],
        "verdict": (
            "literal rational q with X_a,X_c in im(Phi) and "
            "dim pi_t ker(Phi)=2; it does not satisfy the nine full rows"
        ),
    }


def format_polynomial(polynomial):
    terms = []
    for monomial, coefficient in sorted(polynomial.items()):
        atom = "*".join(monomial) if monomial else "1"
        if coefficient == 1:
            terms.append("+" + atom)
        elif coefficient == -1:
            terms.append("-" + atom)
        elif coefficient > 0:
            terms.append(f"+{coefficient}*{atom}")
        else:
            terms.append(f"{coefficient}*{atom}")
    answer = "".join(terms)
    return answer[1:] if answer.startswith("+") else answer


def emit_singular(path, equations):
    with path.open("w") as handle:
        handle.write(
            "ring r=0,(" + ",".join(VARIABLES) + "),dp; option(redSB);\n"
        )
        handle.write(
            "ideal I=" + ",".join(format_polynomial(polynomial)
                                   for polynomial in equations) + ";\n"
        )
        handle.write(
            'print(nvars(basering)); print(size(I));\n'
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-singular", type=Path)
    args = parser.parse_args()

    pin_dependencies()
    labels, equations = build_system()
    digest = system_digest(labels, equations)
    require(digest == EXPECTED_SYSTEM_SHA256,
            f"the normalized provenance system changed: {digest}")
    chord = audit_pure_target_chord(labels, equations)
    ledger = {
        "pinned_radical_dichotomy_sha256": PINNED_RADICAL_DICHOTOMY_SHA256,
        "pinned_common_hafnian_sha256": PINNED_COMMON_HAFNIAN_SHA256,
        "variables": len(VARIABLES),
        "source_rows": len(equations),
        "sparse_terms": sum(len(polynomial) for polynomial in equations),
        "system_sha256": digest,
        "normalization": {
            "pi_Qa": "e0", "pi_Rc": "e0",
            "pi_Qt": "e1", "pi_Rt": "e1",
        },
        "pure_target_chord_localization": chord,
        "dimW_le_one_counterguard": audit_two_dimensional_projection_counterguard(),
        "verdict": (
            "the complete normalized common-q provenance ideal is frozen; "
            "its pure-target rows force a nonzero literal target chord and "
            "controller response, but the remaining ideal is not decided"
        ),
        "excluded_branches": [
            "[X_t] in R_nt", "pi_t(Q_a)=0", "pi_t(R_c)=0",
        ],
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    ledger_digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(ledger_digest == EXPECTED_LEDGER_SHA256,
                f"the common-radical provenance ledger changed: {ledger_digest}")

    if args.emit_singular:
        emit_singular(args.emit_singular, equations)
    print("shared reciprocal common-radical provenance system: PASS")
    print("variables / source rows / sparse terms: 184 / 3645 / 139404")
    print("pure target: D22*R=1, D01=0, D02=D21")
    print(f"system sha256: {digest}")
    print(f"ledger sha256: {ledger_digest}")


if __name__ == "__main__":
    main()
