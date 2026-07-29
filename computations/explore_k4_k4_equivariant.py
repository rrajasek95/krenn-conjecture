#!/usr/bin/env python3
"""Exact coefficient ideal for an equivariant two-K4 composition ansatz.

Each shore is the unit diagonal K4 one-factorization, with vertices labelled
by F_2^2 and the three colours labelled by its nonzero elements.  Cross
blocks satisfy simultaneous AGL(2,2) equivariance.  They therefore depend on
seven scalar parameters.  The script enumerates every matching coefficient,
deduplicates the resulting integer polynomials, and computes a Groebner
basis over Q.  It is an exploration script until a compact certificate is
extracted from its output.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import product

import sympy as sp


PARAMS = ("a", "b", "c", "d", "e", "f", "g")
ZERO_EXP = (0,) * len(PARAMS)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for k in range(1, len(vertices)):
        v = vertices[k]
        rest = vertices[1:k] + vertices[k + 1 :]
        for matching in perfect_matchings(rest):
            yield ((u, v),) + matching


def colour_of_difference(z: int) -> int:
    # Nonzero F_2^2 elements 1,2,3 correspond to colours 0,1,2.
    return (1, 2, 3).index(z)


def canonical_colour_permutation(z: int) -> tuple[int, int, int]:
    """A permutation sending difference 1 to z.

    The base cross block for difference 1 is invariant under swapping the
    other two colours, so the resulting transported block is independent of
    this representative choice.
    """
    target = colour_of_difference(z)
    if target == 0:
        return (0, 1, 2)
    if target == 1:
        return (1, 0, 2)
    return (2, 1, 0)


def parameter_index_for_cross(diff: int, row: int, col: int) -> int:
    if diff == 0:
        return 0 if row == col else 1

    perm = canonical_colour_permutation(diff)
    inv = [0, 0, 0]
    for old, new in enumerate(perm):
        inv[new] = old
    i, j = inv[row], inv[col]

    # Base block C_1 = [[c,d,d],[e,f,g],[e,g,f]].
    if i == 0 and j == 0:
        return 2
    if i == 0:
        return 3
    if j == 0:
        return 4
    if i == j:
        return 5
    return 6


def add_exp(exp: tuple[int, ...], index: int) -> tuple[int, ...]:
    out = list(exp)
    out[index] += 1
    return tuple(out)


def enumerate_coefficients():
    coefficients: dict[tuple[int, ...], Counter] = defaultdict(Counter)
    matching_hist = Counter()

    for matching in perfect_matchings(tuple(range(8))):
        cross = [(u, v) for u, v in matching if (u < 4) != (v < 4)]
        matching_hist[len(cross)] += 1

        fixed = [-1] * 8
        cross_edges = []
        valid = True
        for u, v in matching:
            if (u < 4) == (v < 4):
                x, y = (u, v) if u < 4 else (u - 4, v - 4)
                colour = colour_of_difference(x ^ y)
                if fixed[u] not in (-1, colour) or fixed[v] not in (-1, colour):
                    valid = False
                    break
                fixed[u] = fixed[v] = colour
            else:
                if u >= 4:
                    u, v = v, u
                cross_edges.append((u, v - 4))
        if not valid:
            continue

        for local_colours in product(range(3), repeat=2 * len(cross_edges)):
            word = fixed[:]
            exp = ZERO_EXP
            for k, (x, y) in enumerate(cross_edges):
                row = local_colours[2 * k]
                col = local_colours[2 * k + 1]
                word[x] = row
                word[y + 4] = col
                exp = add_exp(exp, parameter_index_for_cross(x ^ y, row, col))
            coefficients[tuple(word)][exp] += 1

    # Subtract the desired ternary diagonal tensor.
    for colour in range(3):
        coefficients[(colour,) * 8][ZERO_EXP] -= 1
    coefficients = {w: p for w, p in coefficients.items() if any(p.values())}
    return coefficients, matching_hist


def canonical_polynomial(counter: Counter) -> tuple[tuple[tuple[int, ...], int], ...]:
    terms = tuple(sorted((exp, coeff) for exp, coeff in counter.items() if coeff))
    if not terms:
        return ()
    first = terms[0][1]
    if first < 0:
        terms = tuple((exp, -coeff) for exp, coeff in terms)
    common = 0
    for _, coeff in terms:
        common = int(sp.gcd(common, abs(coeff)))
    if common > 1:
        terms = tuple((exp, coeff // common) for exp, coeff in terms)
    return terms


def to_sympy(poly, symbols):
    result = 0
    for exp, coeff in poly:
        monomial = sp.Integer(coeff)
        for symbol, power in zip(symbols, exp):
            monomial *= symbol**power
        result += monomial
    return sp.expand(result)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--groebner", action="store_true")
    parser.add_argument("--order", default="grevlex", choices=("lex", "grlex", "grevlex"))
    parser.add_argument("--prime", type=int)
    args = parser.parse_args()

    coefficients, matching_hist = enumerate_coefficients()
    unique = {}
    for word, counter in coefficients.items():
        key = canonical_polynomial(counter)
        unique.setdefault(key, word)

    degree_hist = Counter(max(sum(exp) for exp, _ in poly) for poly in unique)
    term_hist = Counter(len(poly) for poly in unique)
    print(f"matchings_by_cross={dict(sorted(matching_hist.items()))}")
    print(f"nonzero_coefficient_equations={len(coefficients)}")
    print(f"unique_equations={len(unique)} degrees={dict(sorted(degree_hist.items()))} terms={dict(sorted(term_hist.items()))}")

    symbols = sp.symbols(" ".join(PARAMS))
    polys = [to_sympy(poly, symbols) for poly in unique]
    for word, poly in list((unique[key], to_sympy(key, symbols)) for key in unique)[:30]:
        print("".join(map(str, word)), poly)

    if args.groebner:
        domain = sp.GF(args.prime) if args.prime else sp.QQ
        print(f"computing_groebner order={args.order} domain={domain}", flush=True)
        basis = sp.groebner(polys, *symbols, order=args.order, domain=domain)
        print(f"groebner_size={len(basis.polys)}")
        for poly in basis.polys:
            print(poly.as_expr())
        print(f"contains_one={basis.contains(sp.Integer(1))}")


if __name__ == "__main__":
    main()
