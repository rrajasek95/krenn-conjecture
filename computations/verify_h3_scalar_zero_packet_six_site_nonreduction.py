#!/usr/bin/env python3
"""Refute a literal reduction of the h=3 scalar-zero packet to H6(A)=Delta.

The packet r*q^[2]=Delta is the first polarization of the cubic hafnian
map.  An exact simultaneous guard has injective endpoint triples, invertible
channel pairing, and r^[3]!=0, but no nonzero member of the pencil uq+vr is
an ordinary ternary six-site source.  Coefficient extraction gives a linear
combination of four cubic hafnian values, not one value.  The guard also
fails the first uncontracted physical pair row, locating the extra datum a
vertex gadget would have to supply.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "proofs/six-site-arbitrary-complex-obstruction.md":
        "b36b2f9ccb577af0aebf897edfc9fa1f84d01ba0cf4ea49ac11799d992e00713",
    "notes/curved-rootless-line-uniform-response-resultant.md":
        "36d0c291156328afedbd71486998b5f7dbcc8444431d3cf7a94aaf3185da8cd7",
    "notes/curved-pure-binary-three-channel-common-power-independent-audit.md":
        "2686bf1ddce9d22eb3fc2cdf1cd7871560744ad28a409c98e80586a10a3645de",
}
EXPECTED_LEDGER_SHA256 = "27dbf2ba9ffccb3ba6d193e28327547444904b78158663a50dc77ffcae5c81b6"

SITES = tuple(range(6))
COLOURS = tuple(range(3))
WORDS = tuple(product(COLOURS, repeat=6))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


MATCHINGS = tuple(sorted(perfect_matchings(SITES)))

# Same-colour decorated edge tables.  These are the exact simultaneous
# counterguard from the independent three-channel/common-power audit.
R = {
    ((0, 4), 0, 0): Q(1),
    ((1, 3), 0, 0): Q(1),
    ((2, 5), 0, 0): Q(-1),
    ((0, 1), 1, 1): Q(1),
    ((0, 2), 2, 2): Q(1),
}
COMMON = {
    ((0, 4), 0, 0): Q(1),
    ((2, 5), 0, 0): Q(1),
    ((2, 4), 1, 1): Q(1),
    ((3, 5), 1, 1): Q(1),
    ((1, 3), 2, 2): Q(1),
    ((4, 5), 2, 2): Q(1),
}


def value(table, endpoints, left_colour, right_colour):
    return table.get((endpoints, left_colour, right_colour), Q(0))


def cube_coefficients(table):
    answer = {}
    for word in WORDS:
        coefficient = Q(0)
        for matching in MATCHINGS:
            term = Q(1)
            for endpoints in matching:
                term *= value(table, endpoints,
                              word[endpoints[0]], word[endpoints[1]])
            coefficient += term
        if coefficient:
            answer[word] = coefficient
    return answer


def tangent_coefficients(distinguished, common):
    """Coefficients of distinguished * common^[2]."""
    answer = {}
    for word in WORDS:
        coefficient = Q(0)
        for matching in MATCHINGS:
            for selected, endpoints in enumerate(matching):
                term = value(distinguished, endpoints,
                             word[endpoints[0]], word[endpoints[1]])
                for index, other in enumerate(matching):
                    if index == selected:
                        continue
                    term *= value(common, other,
                                  word[other[0]], word[other[1]])
                coefficient += term
        if coefficient:
            answer[word] = coefficient
    return answer


def word_name(word):
    return "".join(map(str, word))


# Gaussian rationals are pairs (real, imaginary).
ZERO = (Q(0), Q(0))
ONE = (Q(1), Q(0))
I = (Q(0), Q(1))


def gadd(left, right):
    return left[0] + right[0], left[1] + right[1]


def gmul(left, right):
    return (left[0] * right[0] - left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def gscale(scalar, item):
    return scalar * item[0], scalar * item[1]


def linear_sum(*forms):
    answer = defaultdict(lambda: ZERO)
    for form in forms:
        for port, coefficient in form.items():
            answer[port] = gadd(answer[port], coefficient)
    return {port: coefficient for port, coefficient in answer.items()
            if coefficient != ZERO}


def scaled_form(scalar, form):
    return {port: gmul(scalar, coefficient)
            for port, coefficient in form.items()}


def port(site, colour):
    return {(site, colour): ONE}


def response_factorization():
    u0 = linear_sum(port(0, 0), port(4, 0))
    v0 = linear_sum(port(0, 1), port(1, 1))
    u1 = linear_sum(port(1, 0), port(3, 0))
    v1 = linear_sum(port(0, 2), port(2, 2))
    p = (
        linear_sum(u0, scaled_form(I, v0)),
        linear_sum(u1, scaled_form(I, v1)),
        port(2, 0),
    )
    t = (
        linear_sum(
            scaled_form((Q(1, 2), Q(0)), u0),
            scaled_form((Q(0), Q(-1, 2)), v0),
        ),
        linear_sum(
            scaled_form((Q(1, 2), Q(0)), u1),
            scaled_form((Q(0), Q(-1, 2)), v1),
        ),
        scaled_form((Q(-1), Q(0)), port(5, 0)),
    )

    reconstructed = defaultdict(lambda: ZERO)
    channel_tables = []
    for left_form, right_form in zip(p, t, strict=True):
        channel = defaultdict(lambda: ZERO)
        for (left_site, left_colour), left_coefficient in left_form.items():
            for (right_site, right_colour), right_coefficient in right_form.items():
                if left_site == right_site:
                    continue
                coefficient = gmul(left_coefficient, right_coefficient)
                if left_site < right_site:
                    key = ((left_site, right_site), left_colour, right_colour)
                else:
                    key = ((right_site, left_site), right_colour, left_colour)
                channel[key] = gadd(channel[key], coefficient)
                reconstructed[key] = gadd(reconstructed[key], coefficient)
        channel_tables.append({key: item for key, item in channel.items()
                               if item != ZERO})
    expected = {key: (coefficient, Q(0)) for key, coefficient in R.items()}
    reconstructed = {key: item for key, item in reconstructed.items()
                     if item != ZERO}
    require(reconstructed == expected, (reconstructed, expected))

    # Pairwise-disjoint, nonempty port supports imply independence of both
    # triples.  The channel matrix is the identity, hence invertible.
    for triple in (p, t):
        supports = tuple(set(form) for form in triple)
        require(all(supports), supports)
        require(all(not (left & right)
                    for left, right in combinations(supports, 2)), supports)
    return p, t, tuple(channel_tables)


def serialize_coefficients(table):
    return tuple((word_name(word), str(coefficient))
                 for word, coefficient in sorted(table.items()))


def build_ledger():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    require(len(MATCHINGS) == 15, len(MATCHINGS))
    p, t, channels = response_factorization()

    q3 = cube_coefficients(COMMON)
    rq2 = tangent_coefficients(R, COMMON)
    qr2 = tangent_coefficients(COMMON, R)
    r3 = cube_coefficients(R)
    pure_target = {(colour,) * 6: Q(1) for colour in COLOURS}
    require(q3 == {tuple(map(int, "020200")): Q(1)}, q3)
    require(rq2 == pure_target, rq2)
    require(qr2 == {
        tuple(map(int, "020200")): Q(-1),
        tuple(map(int, "202022")): Q(1),
    }, qr2)
    require(r3 == {(0,) * 6: Q(-1)}, r3)

    # alpha=-1 gives rq^[2]=-alpha*Delta, while r^[3] is nonzero.
    alpha = Q(-1)
    require(rq2 == {word: -alpha * coefficient
                    for word, coefficient in pure_target.items()}, rq2)

    # The two mixed pencil coefficients prove that no nonzero uq+vr has a
    # pure cube: 202022 gives u*v^2=0; if u=0 the cube is unary -v^3 X0,
    # while if v=0, 020200 gives u^3!=0.
    pencil_guards = {
        "020200": (Q(1), Q(0), Q(-1), Q(0)),
        "202022": (Q(0), Q(0), Q(1), Q(0)),
        "000000": (Q(0), Q(1), Q(0), Q(-1)),
        "111111": (Q(0), Q(1), Q(0), Q(0)),
        "222222": (Q(0), Q(1), Q(0), Q(0)),
    }
    for label, expected in pencil_guards.items():
        word = tuple(map(int, label))
        actual = tuple(table.get(word, Q(0))
                       for table in (q3, rq2, qr2, r3))
        require(actual == expected, (label, actual, expected))

    # Exact rational coefficient extraction from four values of the pencil.
    points = (Q(-1), Q(0), Q(1), Q(2))
    weights = (Q(-1, 3), Q(-1, 2), Q(1), Q(-1, 6))
    require(tuple(sum(weight * point ** degree
                      for weight, point in zip(weights, points, strict=True))
                  for degree in range(4)) == (Q(0), Q(1), Q(0), Q(0)),
            (points, weights))
    for word in WORDS:
        coefficients = tuple(table.get(word, Q(0))
                             for table in (q3, rq2, qr2, r3))
        evaluations = tuple(sum(coefficient * point ** degree
                                for degree, coefficient in
                                enumerate(coefficients))
                            for point in points)
        extracted = sum(weight * evaluation
                        for weight, evaluation in
                        zip(weights, evaluations, strict=True))
        require(extracted == rq2.get(word, Q(0)),
                (word, coefficients, evaluations, extracted))

    # The first uncontracted K=I pair row already fails.  Its response
    # channel p0*t0 has q^[2]-image Y+X1, while q^[3]=Y.  No scalar direct
    # coefficient can turn a*Y+(Y+X1) into X0.
    first_channel = {key: coefficient[0]
                     for key, coefficient in channels[0].items()
                     if coefficient[1] == 0 and coefficient[0]}
    channel_q2 = tangent_coefficients(first_channel, COMMON)
    require(channel_q2 == {
        tuple(map(int, "020200")): Q(1),
        (1,) * 6: Q(1),
    }, channel_q2)

    return {
        "theorem": "h3 scalar-zero packet does not reduce to ordinary H6",
        "pins": PINS,
        "packet": {
            "alpha": str(alpha),
            "rq^[2]": serialize_coefficients(rq2),
            "r^[3]": serialize_coefficients(r3),
            "endpoint_triples_injective": True,
            "channel_pairing": "K=I_3, determinant 1",
        },
        "adjacent_polarizations": {
            "q^[3]": serialize_coefficients(q3),
            "rq^[2]": serialize_coefficients(rq2),
            "q r^[2]": serialize_coefficients(qr2),
            "r^[3]": serialize_coefficients(r3),
        },
        "ordinary_pencil_no_go": {
            "cube": "(u q+v r)^[3]=u^3 q3+u^2 v rq2+u v^2 qr2+v^3 r3",
            "guard_coefficients": {
                label: tuple(map(str, coefficients))
                for label, coefficients in pencil_guards.items()
            },
            "verdict": "no nonzero pencil member has ternary pure cube",
        },
        "finite_extraction": {
            "points": tuple(map(str, points)),
            "weights": tuple(map(str, weights)),
            "identity": "sum weights*(q+t r)^[3]=r q^[2]=Delta",
            "failure": "linear combination of four hafnian values, not one value",
        },
        "degeneration_guard": {
            "q^[3]_nonzero": True,
            "r^[3]_nonzero": True,
            "failure": (
                "the tangent requires subtracting q^[3]; projective pencil "
                "limits retain q^[3] or r^[3]"
            ),
        },
        "colour_marker_guard": {
            "edge_type_polynomial": "(a q+b r)^[3] has counts 0,1,2,3",
            "failure": (
                "forgetting the marker evaluates the polynomial and retains "
                "nonzero q3, q r2, and r3; selecting count1 is coefficient "
                "extraction, not a local colour algebra homomorphism"
            ),
        },
        "first_vertex_gadget_full_row_failure": {
            "q^[3]": serialize_coefficients(q3),
            "p0*t0*q^[2]": serialize_coefficients(channel_q2),
            "required": "a00*q^[3]+p0*t0*q^[2]=X0",
            "obstruction": "the X1 coefficient is 1 for every a00",
        },
        "scope": (
            "refutes reductions using only the contracted scalar-zero packet, "
            "its pencil/polarization, coefficient extraction, a forgotten "
            "edge-type colour, or the natural K=I pair gadget.  A theorem "
            "using the other eight shared physical pair rows is not refuted."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    parser.add_argument("--dump-ledger", action="store_true")
    arguments = parser.parse_args()
    ledger = build_ledger()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))
    print("h3 scalar-zero packet six-site nonreduction: PASS")
    print("mode", arguments.mode)
    print("packet rq2=Delta; r3=-X0; injective x injective, K=I")
    print("ordinary pencil / extraction / first full row",
          "NO / four-value linear span only / X1 obstruction")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
