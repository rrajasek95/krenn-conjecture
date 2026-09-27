"""Exact four-arm response kernels, quadratic residuals, and a sharp example."""

from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT/"computations/flat-core-rigidity-2026-09-27"))
from algebra import (E, ZERO, ONE, OMEGA, require, rank, clean, norm2,
                     four_outputs, four_derivative, add_sources, scale)


def vector_product(vectors, coefficient):
    q = len(vectors[1])
    result = {}
    for word in product(range(q), repeat=4):
        value = coefficient
        for i, a in enumerate(word, start=1):
            value *= vectors[i][a]
        if value:
            result[(1, 2, 3, 4), word] = value
    return result


def fixture(q, mode, dense=False):
    e0 = [ONE]+[ZERO]*(q-1)
    e1 = ([ZERO, ONE]+[ZERO]*(q-2)) if q >= 2 else e0
    vectors = {i: [E(i+a+1, (i+2*a) % 3) if dense else (ONE if a == 0 else ZERO)
                   for a in range(q)] for i in range(1, 5)}
    source = {}
    for i in range(1, 5):
        u = e0
        if mode == "two_pairs":
            u = e0 if i <= 2 else e1
        elif mode == "three_one":
            u = e0 if i <= 3 else e1
        elif mode == "two_one_one":
            u = e0 if i <= 2 else e1 if i == 3 else [x+y for x, y in zip(e0, e1)]
        elif mode == "distinct":
            u = [ONE, E(i)]+[ZERO]*(q-2)
        for a, b in product(range(q), repeat=2):
            source[0, i, a, b] = u[a]*vectors[i][b]
        if mode == "one_rank_two" and i == 1:
            for a, b in product(range(q), repeat=2):
                source[0, i, a, b] = ONE if a == b and a < 2 else ZERO
    return clean(source), vectors


def leaf_kernel(vectors, x, y):
    z = -x-y
    weights = {(1, 2): x, (3, 4): x, (1, 3): y, (2, 4): y,
               (1, 4): z, (2, 3): z}
    q = len(vectors[1])
    return clean({(i, j, a, b): w*vectors[i][a]*vectors[j][b]
                  for (i, j), w in weights.items()
                  for a, b in product(range(q), repeat=2)})


def check_case(q, mode, dense=False):
    source, vectors = fixture(q, mode, dense)
    hidden = 2 if mode == "common" else 1 if mode == "two_pairs" else 0
    records = []
    for n in (5, 6):
        require(not four_outputs(source, n, q), "A star is four-site-flat")
        columns, rows = four_derivative(source, n, q)
        actual = rank(list(rows.values()))
        require(actual == q*q*(n-1)*(n-2)//2-hidden, "Complete four-arm derivative rank")
        basis = ([leaf_kernel(vectors, ONE, ZERO), leaf_kernel(vectors, ZERO, ONE)]
                 if hidden == 2 else [leaf_kernel(vectors, ZERO, ONE)] if hidden == 1 else [])
        for B in basis:
            require(all(not sum((row[j]*B.get(c, ZERO) for j, c in enumerate(columns)), ZERO)
                        for row in rows.values()), "Explicit hidden direction is in the derivative kernel")
        require(rank([[B.get(c, ZERO) for c in columns] for B in basis]) == hidden,
                "Hidden directions are independent")
        records.append(dict(sites=n, colors=q, arm_pattern=mode, dense_leaf_vectors=dense,
                            derivative_rank=actual, hidden_leaf_directions=hidden))
    if hidden:
        for x, y in ((ONE, ZERO), (ZERO, ONE), (ONE, ONE), (ONE, OMEGA)):
            if hidden == 1 and x:
                continue
            B = leaf_kernel(vectors, x, y)
            coefficient = x*x+y*y+(-x-y)*(-x-y)
            require(four_outputs(add_sources(source, B), 6, q) ==
                    vector_product(vectors, coefficient), "Every coefficient of the quadratic leaf response")
        if hidden == 2:
            cube = leaf_kernel(vectors, ONE, OMEGA)
            require(not four_outputs(add_sources(source, cube), 6, q),
                    "Common-center kernel contains actual five-core branches")
            require(bool(cube), "An unanchored linear distance claim would be false")
    return records


def check():
    records = []
    cases = [(1, "common", False), (2, "common", False), (2, "two_pairs", False),
             (2, "three_one", False), (2, "two_one_one", False),
             (2, "distinct", False), (2, "one_rank_two", False),
             (2, "common", True), (2, "two_pairs", True),
             (3, "common", False), (3, "two_pairs", False), (3, "one_rank_two", False)]
    for case in cases:
        records.extend(check_case(*case))
    base, vectors = fixture(2, "two_pairs")
    K = leaf_kernel(vectors, ZERO, ONE)
    sharp = []
    for tau in (Q(1), Q(1, 2), Q(1, 3), Q(1, 10), Q(1, 100)):
        B = scale(K, tau)
        response = four_outputs(add_sources(base, B), 6, 2)
        require(norm2(B) == 4*tau**2 and norm2(response) == 4*tau**4,
                "Exact square-root response-to-distance scaling")
        sharp.append(dict(tau=str(tau), leaf_distance_squared=str(norm2(B)),
                          response_squared=str(norm2(response)),
                          distance_over_response=str(1/tau)))
    anchor_checks = 0
    _, unit_vectors = fixture(2, "common")
    for x, y in product((ZERO, ONE, OMEGA, E(2, 1), E(-1, 2)), repeat=2):
        B = leaf_kernel(unit_vectors, x, y)
        q = x*x+y*y+(-x-y)*(-x-y)
        remainder = norm2(B)-24*x.abs2()
        require(remainder <= 0 or remainder**2 <= 36*q.abs2(),
                "Canonical anchored quadratic estimate")
        anchor_checks += 1
    return dict(rank_certificates=records, sharp_square_root_examples=sharp,
                anchored_kernel_fixtures=anchor_checks,
                scope_controls=["No Lipschitz distance bound in the two-pair case",
                                "An unanchored common-center kernel has exact five-core zeros"])
