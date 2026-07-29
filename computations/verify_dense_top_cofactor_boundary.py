#!/usr/bin/env python3
"""Exact top-end solution on a one-cofactor boundary at n=6.

This scope test complements ``verify_dense_top_mixed_linear_branch.py``.
It constructs a scalar W with H(W)=1/32 and exactly C^W_45=0.  A two-site
K supplies the otherwise invisible target pair 45, while q0 is eliminated
on the other fourteen nonzero-cofactor pairs.  Thus the open-cofactor
mixed-linear certificate cannot simply be extended across its denominator.

The construction intentionally has no y cells and is not a bottom GHZ
endpoint.
"""

from __future__ import annotations

import itertools

import sympy as sp


N = 6
X, Y, Z = range(3)
VERTICES = tuple(range(N))
EDGES = tuple(itertools.combinations(VERTICES, 2))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, partner in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, partner),) + tail


def coefficient(source, vertices, coloring):
    answer = sp.Integer(0)
    for matching in perfect_matchings(vertices):
        term = sp.Integer(1)
        for u, v in matching:
            term *= source.get((u, v, coloring[u], coloring[v]), 0)
        answer += term
    return sp.simplify(answer)


def scalar_hafnian(weights, vertices):
    answer = sp.Integer(0)
    for matching in perfect_matchings(vertices):
        answer += sp.prod(weights[edge] for edge in matching)
    return sp.simplify(answer)


def add_directed_cell(source, binary_site, z_site, value):
    u, v = sorted((binary_site, z_site))
    colors = (X, Z) if binary_site == u else (Z, X)
    source[(u, v, *colors)] = sp.simplify(value)


def construct():
    radical = sp.sqrt(97793)
    a = (-255 + radical) / 128
    b = (-255 - radical) / 128
    weights = {edge: sp.Integer(1) for edge in EDGES}
    weights[(0, 1)] = a
    weights[(2, 3)] = b
    assert sp.simplify(a * b + 2) == 0
    assert scalar_hafnian(weights, VERTICES) == sp.Rational(1, 32)
    cofactors = {
        edge: scalar_hafnian(
            weights,
            tuple(vertex for vertex in VERTICES if vertex not in edge),
        )
        for edge in EDGES
    }
    assert {edge for edge, value in cofactors.items() if value == 0} == {(4, 5)}

    source = {edge + (Z, Z): value for edge, value in weights.items()}
    # For binary sites 4 and 5 use the same top-tangent direction first,
    # then rescale the second copy to normalize B_45^{xx}=1/8.
    ratio = -(b + 2) / (a + 2)
    add_directed_cell(source, 4, 0, 1)
    add_directed_cell(source, 4, 3, ratio)
    probe = dict(source)
    add_directed_cell(probe, 5, 0, 1)
    add_directed_cell(probe, 5, 3, ratio)
    pair_coloring = (Z, Z, Z, Z, X, X)
    unscaled = coefficient(probe, VERTICES, pair_coloring)
    assert sp.simplify(unscaled) != 0
    scale = sp.simplify(sp.Rational(1, 8) / unscaled)
    add_directed_cell(source, 5, 0, scale)
    add_directed_cell(source, 5, 3, scale * ratio)
    assert coefficient(source, VERTICES, pair_coloring) == sp.Rational(1, 8)

    # Every other pair has a nonzero direct cofactor and can be eliminated.
    for first, second in EDGES:
        if (first, second) == (4, 5):
            continue
        for first_color, second_color in itertools.product((X, Y), repeat=2):
            coloring = [Z] * N
            coloring[first] = first_color
            coloring[second] = second_color
            hessian = coefficient(source, VERTICES, tuple(coloring))
            target = (
                sp.Rational(1, 8)
                if first_color == second_color == X
                else sp.Integer(0)
            )
            source[(first, second, first_color, second_color)] = sp.simplify(
                (target - hessian) / cofactors[(first, second)]
            )
    return source, weights, cofactors, unscaled


def verify():
    source, weights, cofactors, unscaled = construct()
    audits = 0
    for binary_count in (0, 1, 2):
        for binary_sites in itertools.combinations(VERTICES, binary_count):
            for binary_colors in itertools.product((X, Y), repeat=binary_count):
                coloring = [Z] * N
                for site, color in zip(binary_sites, binary_colors):
                    coloring[site] = color
                value = coefficient(source, VERTICES, tuple(coloring))
                target = (
                    sp.Rational(1, 32)
                    if binary_count == 0
                    else sp.Rational(1, 8)
                    if binary_count == 2 and all(color == X for color in binary_colors)
                    else sp.Integer(0)
                )
                assert sp.simplify(value - target) == 0, (coloring, value, target)
                audits += 1
    assert coefficient(source, VERTICES, (Y,) * N) == 0
    print(
        f"verified {audits} top coefficients on boundary C_45=0; "
        f"w01={weights[(0, 1)]}, w23={weights[(2, 3)]}"
    )
    print(f"verified unscaled B_45^xx={sp.factor(unscaled)} is nonzero")
    print("verified boundary example deliberately fails the all-y bottom equation")


if __name__ == "__main__":
    verify()
