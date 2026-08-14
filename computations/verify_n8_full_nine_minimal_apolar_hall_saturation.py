#!/usr/bin/env python3
"""Exact full-nine saturation on the support-minimal n=8 source fibre.

The fibre is the three-pure-matching packet from the Hamming-two audit,
with all thirteen displayed cells kept as independent variables.  The
checker enumerates all 3^6 residual words and all nine deleted-pair rows,
checks the contracted apolar packet, and verifies a polynomial
Nullstellensatz certificate for the first mixed off-diagonal row.
"""

import argparse
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json


SITES = tuple(range(6))
COLORS = tuple(range(3))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


# Sparse polynomials over Q.  Monomials are sorted tuples of variable names.
def clean(polynomial):
    return {monomial: value for monomial, value in polynomial.items() if value}


def constant(value):
    return {} if not value else {(): Q(value)}


def variable(name):
    return {(name,): Q(1)}


def add(left, right):
    answer = dict(left)
    for monomial, value in right.items():
        answer[monomial] = answer.get(monomial, Q(0)) + value
    return clean(answer)


def negate(polynomial):
    return {monomial: -value for monomial, value in polynomial.items()}


def subtract(left, right):
    return add(left, negate(right))


def multiply(left, right):
    answer = {}
    for first, first_value in left.items():
        for second, second_value in right.items():
            monomial = tuple(sorted(first + second))
            answer[monomial] = answer.get(monomial, Q(0)) + first_value * second_value
    return clean(answer)


def product_polynomials(factors):
    answer = constant(1)
    for factor in factors:
        answer = multiply(answer, factor)
    return answer


V = {name: variable(name) for name in (
    "a", "b", "c", "e", "f", "g",
    "P0", "S0", "P1", "S1", "P2", "S2", "D",
)}


# q has two internal edges in each pure colour.
Q_EDGE = {
    (2, 3, 0, 0): V["a"],
    (4, 5, 0, 0): V["b"],
    (0, 2, 1, 1): V["c"],
    (1, 4, 1, 1): V["e"],
    (0, 4, 2, 2): V["f"],
    (1, 3, 2, 2): V["g"],
}

# FIRST[(label, site, colour)] and SECOND likewise.
FIRST = {
    (0, 0, 0): V["P0"],
    (1, 5, 1): V["P1"],
    (2, 2, 2): V["P2"],
}
SECOND = {
    (0, 1, 0): V["S0"],
    (1, 3, 1): V["S1"],
    (2, 5, 2): V["S2"],
}
DIRECT = {(0, 1): V["D"]}


@lru_cache(maxsize=None)
def matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, partner in enumerate(vertices[1:], start=1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in matchings(rest):
            answer.append(((first, partner),) + matching)
    return tuple(answer)


def q_edge(left, right, left_colour, right_colour):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return Q_EDGE.get((left, right, left_colour, right_colour), {})


def hafnian(word, vertices=SITES):
    answer = {}
    for matching in matchings(tuple(vertices)):
        term = constant(1)
        for left, right in matching:
            term = multiply(term, q_edge(left, right, word[left], word[right]))
        answer = add(answer, term)
    return answer


def response(row, column, word):
    answer = {}
    for p_site in SITES:
        p_value = FIRST.get((row, p_site, word[p_site]), {})
        if not p_value:
            continue
        for s_site in SITES:
            if s_site == p_site:
                continue
            s_value = SECOND.get((column, s_site, word[s_site]), {})
            if not s_value:
                continue
            complement = tuple(
                site for site in SITES if site not in (p_site, s_site)
            )
            answer = add(
                answer,
                multiply(multiply(p_value, s_value), hafnian(word, complement)),
            )
    return answer


def residual(row, column, word):
    direct = multiply(DIRECT.get((row, column), {}), hafnian(word))
    target = constant(
        row == column and all(colour == row for colour in word)
    )
    return subtract(add(direct, response(row, column, word)), target)


A0 = product_polynomials((V["P0"], V["S0"], V["a"], V["b"]))
A1 = product_polynomials((V["P1"], V["S1"], V["c"], V["e"]))
A2 = product_polynomials((V["P2"], V["S2"], V["f"], V["g"]))
ANCHORS = (subtract(A0, constant(1)), subtract(A1, constant(1)), subtract(A2, constant(1)))

WORD_G02 = (0, 1, 0, 0, 1, 2)
G02 = product_polynomials((V["P0"], V["S2"], V["a"], V["e"]))


def specialize_one(polynomial):
    return sum(polynomial.values(), Q(0))


def audit_source_rows():
    nonzero = {}
    for word in product(COLORS, repeat=6):
        for row, column in product(COLORS, repeat=2):
            value = residual(row, column, word)
            if value:
                nonzero[(word, row, column)] = value

    expected = {
        ((0,) * 6, 0, 0): ANCHORS[0],
        ((1,) * 6, 1, 1): ANCHORS[1],
        ((2,) * 6, 2, 2): ANCHORS[2],
        (WORD_G02, 0, 2): G02,
        ((2, 0, 0, 0, 2, 1), 1, 0):
            product_polynomials((V["P1"], V["S0"], V["a"], V["f"])),
        ((1, 2, 1, 2, 0, 0), 0, 1):
            product_polynomials((V["D"], V["b"], V["c"], V["g"])),
    }
    require(nonzero == expected, ("full 6561-row ledger changed", nonzero))
    require(residual(0, 2, WORD_G02) == G02, "first mixed row changed")

    unit_residuals = {
        key: specialize_one(value)
        for key, value in nonzero.items()
        if specialize_one(value)
    }
    require(len(unit_residuals) == 3, ("unit residual count", unit_residuals))
    require(all(value == 1 for value in unit_residuals.values()), unit_residuals)
    return nonzero, unit_residuals


def response_edge(row, column, left, right, left_colour, right_colour):
    if left == right:
        return {}
    return add(
        multiply(
            FIRST.get((row, left, left_colour), {}),
            SECOND.get((column, right, right_colour), {}),
        ),
        multiply(
            FIRST.get((row, right, right_colour), {}),
            SECOND.get((column, left, left_colour), {}),
        ),
    )


def contracted_edge(left, right, left_colour, right_colour):
    # a=E_01 gives tau=0, alpha=1, K_*=-I.
    answer = {}
    for label in COLORS:
        answer = subtract(
            answer,
            response_edge(label, label, left, right, left_colour, right_colour),
        )
    return answer


def contracted_cube(word):
    answer = {}
    for matching in matchings(SITES):
        term = constant(1)
        for left, right in matching:
            term = multiply(
                term,
                contracted_edge(left, right, word[left], word[right]),
            )
        answer = add(answer, term)
    return answer


def contracted_tangent(word):
    answer = {}
    for matching in matchings(SITES):
        for selected, (left, right) in enumerate(matching):
            term = contracted_edge(left, right, word[left], word[right])
            for position, (x, y) in enumerate(matching):
                if position != selected:
                    term = multiply(term, q_edge(x, y, word[x], word[y]))
            answer = add(answer, term)
    return answer


def audit_apolar_packet():
    cube = {}
    tangent = {}
    for word in product(COLORS, repeat=6):
        cube_value = contracted_cube(word)
        tangent_value = contracted_tangent(word)
        if cube_value:
            cube[word] = cube_value
        if tangent_value:
            tangent[word] = tangent_value
    require(cube == {}, ("contracted cube is not identically zero", cube))
    require(
        tangent == {
            (0,) * 6: negate(A0),
            (1,) * 6: negate(A1),
            (2,) * 6: negate(A2),
        },
        ("contracted common-power row changed", tangent),
    )
    return tangent


def audit_certificate():
    multiplier = product_polynomials((
        V["S0"], V["b"],
        V["P2"], V["f"], V["g"],
        V["P1"], V["S1"], V["c"],
    ))
    # M*G02=A0*A1*A2 and
    # A0*A1*A2-1=(A0-1)A1*A2+(A1-1)A2+(A2-1).
    right = subtract(
        multiply(multiplier, G02),
        add(
            multiply(ANCHORS[0], multiply(A1, A2)),
            add(multiply(ANCHORS[1], A2), ANCHORS[2]),
        ),
    )
    require(right == constant(1), ("Nullstellensatz identity changed", right))
    require(
        multiply(multiplier, G02) == multiply(A0, multiply(A1, A2)),
        "monomial saturation identity changed",
    )
    return multiplier


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("all", "source", "apolar", "certificate"),
        default="all",
    )
    args = parser.parse_args()

    nonzero = unit_residuals = tangent = multiplier = None
    if args.mode in ("all", "source"):
        nonzero, unit_residuals = audit_source_rows()
    if args.mode in ("all", "apolar"):
        tangent = audit_apolar_packet()
    if args.mode in ("all", "certificate"):
        multiplier = audit_certificate()

    ledger = {
        "mode": args.mode,
        "residual_words": None if nonzero is None else len(nonzero),
        "unit_specialization_failures": None if unit_residuals is None else len(unit_residuals),
        "contracted_cube_support": 0 if tangent is not None else None,
        "contracted_tangent_support": None if tangent is None else len(tangent),
        "certificate_multiplier_degree": None if multiplier is None else len(next(iter(multiplier))),
        "first_mixed_word": "010012",
        "first_mixed_row": "02",
        "certificate": "1=M*G02-(A0-1)A1A2-(A1-1)A2-(A2-1)",
    }
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print("n=8 minimal full-nine apolar/Hall saturation: PASS")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
