#!/usr/bin/env python3
"""Exact full two-hole audit of the K8 witness-incidence countermodel.

Besides expanding all one- and two-hole identities, this checker isolates a
single genuinely cofactor-coupled coefficient, factors it on the weighted
support chart, and audits every coordinate-boundary branch of that factor.
"""

from __future__ import annotations

from itertools import combinations, permutations, product

import sympy as sp

from verify_witness_incidence_k8_countermodel import (
    PAIRS,
    nonzero_entries,
    oriented,
    perfect_matchings,
)


EXPECTED_FAILURES = {
    (0, 3, 5, 7): ("target", 1),
    (0, 4, 1, 5): ("correction", 9),
    (0, 5, 1, 4): ("correction", 9),
    (0, 5, 2, 3): ("target", 1),
    (1, 3, 5, 7): ("target", 1),
    (1, 4, 0, 5): ("correction", 9),
    (1, 4, 6, 7): ("target", 1),
    (1, 5, 0, 4): ("correction", 9),
    (1, 5, 2, 3): ("cofactor", 2),
    (2, 4, 1, 6): ("target", 1),
    (2, 5, 1, 6): ("target", 1),
    (3, 4, 1, 6): ("target", 1),
    (3, 5, 1, 6): ("target", 1),
}

# The eleven entries in the coefficient of x_0^4 y_1^4 in Q_11 for
# (p,q;w,z)=(1,5;2,3).  Each tuple is (lower vertex, upper vertex, row, col).
COFACTOR_FACTOR_CELLS = (
    (0, 1, 0, 0),
    (0, 3, 2, 1),
    (0, 5, 1, 1),
    (1, 4, 0, 0),
    (1, 6, 0, 2),
    (1, 7, 0, 0),
    (2, 4, 1, 2),
    (4, 5, 1, 1),
    (5, 6, 1, 0),
    (5, 7, 1, 2),
    (6, 7, 1, 1),
)


def cross(a: sp.Matrix, b: sp.Matrix):
    return sp.Matrix(
        [
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0],
        ]
    )


def scalar_hafnian(vertices, covectors, block=oriented):
    total = sp.Integer(0)
    for matching in perfect_matchings(tuple(vertices)):
        term = sp.Integer(1)
        for u, v in matching:
            term *= (covectors[u].T * block(u, v) * covectors[v])[0]
        total += term
    return sp.expand(total)


def one_site_partial(vertices, hole, covectors, block=oriented):
    out = sp.zeros(3, 1)
    for matching in perfect_matchings(tuple(vertices)):
        term = sp.Integer(1)
        vector = None
        for u, v in matching:
            matrix = block(u, v)
            if u == hole:
                vector = matrix * covectors[v]
            elif v == hole:
                vector = matrix.T * covectors[u]
            else:
                term *= (covectors[u].T * matrix * covectors[v])[0]
        out += term * vector
    return out.applyfunc(sp.expand)


def two_site_partial(vertices, w, z, covectors, block=oriented):
    out = sp.zeros(3, 3)
    for matching in perfect_matchings(tuple(vertices)):
        term = sp.Integer(1)
        vector_w = None
        vector_z = None
        direct = None
        for u, v in matching:
            matrix = block(u, v)
            if {u, v} == {w, z}:
                direct = matrix if (u, v) == (w, z) else matrix.T
            elif u == w:
                vector_w = matrix * covectors[v]
            elif v == w:
                vector_w = matrix.T * covectors[u]
            elif u == z:
                vector_z = matrix * covectors[v]
            elif v == z:
                vector_z = matrix.T * covectors[u]
            else:
                term *= (covectors[u].T * matrix * covectors[v])[0]
        out += term * (direct if direct is not None else vector_w * vector_z.T)
    return out.applyfunc(sp.expand)


def classify_residual(target, g_quotient, correction, residual):
    cells = [(i, j) for i in range(3) for j in range(3) if residual[i, j] != 0]
    if all(
        target[i, j] != 0 and g_quotient[i, j] == 0 and correction[i, j] == 0
        for i, j in cells
    ):
        return "target", cells
    if all(target[i, j] == 0 and correction[i, j] != 0 for i, j in cells):
        return "correction", cells
    if all(
        target[i, j] == 0 and g_quotient[i, j] != 0 and correction[i, j] == 0
        for i, j in cells
    ):
        return "cofactor", cells
    raise AssertionError("unclassified two-hole residual")


def full_identity_audit():
    x = sp.Matrix(sp.symbols("x0:3"))
    y = sp.Matrix(sp.symbols("y0:3"))
    variables = tuple(x) + tuple(y)
    one_hole_systems = 0
    one_hole_scalar_equations = 0
    passes = []
    failures = {}
    representatives = {}

    for p, q in combinations(range(8), 2):
        remainder = [u for u in range(8) if u not in (p, q)]
        gammas = {
            u: cross(oriented(p, u).T * x, oriented(q, u).T * y)
            for u in remainder
        }
        g = (x.T * oriented(p, q) * y)[0]

        for hole in remainder:
            contracted = [u for u in remainder if u != hole]
            partial = one_site_partial(
                remainder, hole, {u: gammas[u] for u in contracted}
            )
            for color in range(3):
                lhs = x[color] * y[color] * sp.prod(
                    gammas[u][color] for u in contracted
                )
                assert sp.Poly(sp.expand(lhs - g * partial[color]), *variables).is_zero
                one_hole_scalar_equations += 1
            one_hole_systems += 1

        for w, z in combinations(remainder, 2):
            contracted = [u for u in remainder if u not in (w, z)]
            covectors = {u: gammas[u] for u in contracted}
            target = sp.diag(
                *[
                    x[color]
                    * y[color]
                    * sp.prod(gammas[u][color] for u in contracted)
                    for color in range(3)
                ]
            ).applyfunc(sp.expand)
            quotient = two_site_partial(remainder, w, z, covectors)
            h = scalar_hafnian(contracted, covectors)
            xw = oriented(p, w).T * x
            xz = oriented(p, z).T * x
            yw = oriented(q, w).T * y
            yz = oriented(q, z).T * y
            hole_matrix = xw * yz.T + yw * xz.T
            g_quotient = (g * quotient).applyfunc(sp.expand)
            correction = (h * hole_matrix).applyfunc(sp.expand)
            residual = (target - g_quotient - correction).applyfunc(sp.expand)
            key = (p, q, w, z)
            if residual == sp.zeros(3, 3):
                passes.append(key)
                continue
            kind, cells = classify_residual(target, g_quotient, correction, residual)
            failures[key] = (kind, len(cells))
            representatives.setdefault(kind, (key, cells[0], sp.factor(residual[cells[0]])))

    assert one_hole_systems == 168
    assert one_hole_scalar_equations == 504
    assert len(passes) == 407
    assert failures == EXPECTED_FAILURES
    assert sum(count for _, count in failures.values()) == 46
    assert {
        kind: sum(1 for failure_kind, _ in failures.values() if failure_kind == kind)
        for kind in ("target", "correction", "cofactor")
    } == {"target": 8, "correction": 4, "cofactor": 1}
    assert all(
        (p, q, w, z) in passes
        for p, q in PAIRS
        for w, z in combinations([u for u in range(8) if u not in (p, q)], 2)
    )

    # The unique cofactor-type failure is completely explicit.
    p, q, w, z = 1, 5, 2, 3
    remainder = [u for u in range(8) if u not in (p, q)]
    contracted = [u for u in remainder if u not in (w, z)]
    gammas = {
        u: cross(oriented(p, u).T * x, oriented(q, u).T * y)
        for u in remainder
    }
    quotient = two_site_partial(
        remainder, w, z, {u: gammas[u] for u in contracted}
    )
    assert quotient == -x[0] ** 4 * y[1] ** 4 * sp.diag(0, 1, 1)
    assert scalar_hafnian(contracted, {u: gammas[u] for u in contracted}) == 0
    assert all(
        x[color]
        * y[color]
        * sp.prod(gammas[u][color] for u in contracted)
        == 0
        for color in range(3)
    )

    return failures, representatives


def model_automorphisms():
    """Automorphisms allowing a vertex permutation and one global color permutation."""

    automorphisms = []
    for group_permutation in permutations(range(4)):
        for flips in product(range(2), repeat=4):
            vertex_permutation = {}
            for group, (u, v) in enumerate(PAIRS):
                target = PAIRS[group_permutation[group]]
                vertex_permutation[u] = target[flips[group]]
                vertex_permutation[v] = target[1 - flips[group]]
            for color_permutation in permutations(range(3)):
                permutation_matrix = sp.zeros(3, 3)
                for old, new in enumerate(color_permutation):
                    permutation_matrix[new, old] = 1
                if all(
                    oriented(vertex_permutation[u], vertex_permutation[v])
                    == permutation_matrix * oriented(u, v) * permutation_matrix.T
                    for u in range(8)
                    for v in range(u + 1, 8)
                ):
                    automorphisms.append(
                        (
                            tuple(vertex_permutation[u] for u in range(8)),
                            color_permutation,
                        )
                    )
    assert automorphisms == [(tuple(range(8)), tuple(range(3)))]
    return automorphisms


def weighted_blocks():
    blocks = {}
    symbols = {}
    for u in range(8):
        for v in range(u + 1, 8):
            support = oriented(u, v)
            block = sp.zeros(3, 3)
            for i in range(3):
                for j in range(3):
                    if support[i, j]:
                        symbol = sp.symbols(f"a{u}{v}{i}{j}")
                        block[i, j] = symbol
                        symbols[u, v, i, j] = symbol
            blocks[u, v] = block

    def block(u, v):
        return blocks[u, v] if u < v else blocks[v, u].T

    return block, symbols


def cofactor_factorization():
    block, symbols = weighted_blocks()
    x = sp.Matrix(sp.symbols("x0:3"))
    y = sp.Matrix(sp.symbols("y0:3"))
    p, q, w, z = 1, 5, 2, 3
    remainder = [u for u in range(8) if u not in (p, q)]
    contracted = [u for u in remainder if u not in (w, z)]
    gammas = {
        u: cross(block(p, u).T * x, block(q, u).T * y) for u in remainder
    }
    covectors = {u: gammas[u] for u in contracted}

    target_diagonal = [
        sp.expand(
            x[color]
            * y[color]
            * sp.prod(gammas[u][color] for u in contracted)
        )
        for color in range(3)
    ]
    h = scalar_hafnian(contracted, covectors, block)
    g = sp.expand((x.T * block(p, q) * y)[0])
    assert target_diagonal == [0, 0, 0]
    assert h == 0
    assert g == symbols[1, 5, 0, 1] * x[0] * y[1]

    # Keep the perfect-matching source of the coefficient visible.  There is
    # exactly one contributor, so no hidden cancellation was factored away.
    contributors = []
    for matching in perfect_matchings(tuple(remainder)):
        term = sp.Integer(1)
        vector_w = None
        vector_z = None
        direct = None
        for u, v in matching:
            matrix = block(u, v)
            if {u, v} == {w, z}:
                direct = matrix if (u, v) == (w, z) else matrix.T
            elif u == w:
                vector_w = matrix * covectors[v]
            elif v == w:
                vector_w = matrix.T * covectors[u]
            elif u == z:
                vector_z = matrix * covectors[v]
            elif v == z:
                vector_z = matrix.T * covectors[u]
            else:
                term *= (covectors[u].T * matrix * covectors[v])[0]
        matrix_term = term * (
            direct if direct is not None else vector_w * vector_z.T
        )
        coefficient = sp.Poly(
            sp.expand(matrix_term[1, 1]), *tuple(x), *tuple(y)
        ).coeff_monomial(x[0] ** 4 * y[1] ** 4)
        if coefficient:
            contributors.append((matching, sp.factor(coefficient)))

    expected_factor = -sp.prod(symbols[cell] for cell in COFACTOR_FACTOR_CELLS)
    assert contributors == [(((0, 3), (2, 4), (6, 7)), expected_factor)]
    return expected_factor


def generic_cofactor(deleted, block):
    remaining = tuple(v for v in range(8) if v not in deleted)
    tensor = {}
    for matching in perfect_matchings(remaining):
        terms = [((), 1)]
        for u, v in matching:
            matrix = block(u, v)
            entries = [
                (i, j, int(matrix[i, j]))
                for i in range(3)
                for j in range(3)
                if matrix[i, j]
            ]
            terms = [
                (assignment + ((u, i), (v, j)), value * coefficient)
                for assignment, value in terms
                for i, j, coefficient in entries
            ]
        for assignment, value in terms:
            key = tuple(sorted(assignment))
            tensor[key] = tensor.get(key, 0) + value
    return {key: value for key, value in tensor.items() if value}


def audit_coordinate_boundary(deleted_cell):
    edge_u, edge_v, row, column = deleted_cell

    def block(u, v):
        lower, upper = sorted((u, v))
        matrix = oriented(lower, upper).copy()
        if (lower, upper) == (edge_u, edge_v):
            matrix[row, column] = 0
        return matrix if u < v else matrix.T

    cofactors = {
        (u, v): generic_cofactor((u, v), block)
        for u in range(8)
        for v in range(u + 1, 8)
    }
    assert all(cofactors.values())

    anchor_counts = []
    for p in range(8):
        for color in range(3):
            count = 0
            for u in range(8):
                if u == p:
                    continue
                matrix = block(p, u)
                other_columns = [c for c in range(3) if c != color]
                if (
                    matrix.rank() == 1
                    and matrix[:, other_columns] == sp.zeros(3, 2)
                    and cofactors[tuple(sorted((p, u)))]
                ):
                    count += 1
            anchor_counts.append(count)
    assert min(anchor_counts) >= 1

    star_ranks = []
    star_sizes = []
    for p in range(8):
        atoms = []
        for u in range(8):
            if u == p:
                continue
            matrix = block(p, u)
            cofactor = cofactors[tuple(sorted((p, u)))]
            for color_p in range(3):
                for color_u in range(3):
                    if matrix[color_p, color_u] == 0:
                        continue
                    atom = {}
                    for assignment, value in cofactor.items():
                        coloring = [0] * 8
                        coloring[p] = color_p
                        coloring[u] = color_u
                        for vertex, color in assignment:
                            coloring[vertex] = color
                        index = 0
                        for color in coloring:
                            index = 3 * index + color
                        atom[index] = atom.get(index, 0) + value
                    atoms.append(atom)
        rows = sorted(set().union(*(set(atom) for atom in atoms)))
        star_matrix = sp.Matrix(
            [[atom.get(row, 0) for atom in atoms] for row in rows]
        )
        star_ranks.append(star_matrix.rank())
        star_sizes.append(len(atoms))
    assert star_ranks == star_sizes
    return min(anchor_counts), tuple(star_sizes)


def main():
    failures, representatives = full_identity_audit()
    automorphisms = model_automorphisms()
    factor = cofactor_factorization()
    boundary_data = {
        cell: audit_coordinate_boundary(cell) for cell in COFACTOR_FACTOR_CELLS
    }

    print("verified all 168 one-hole systems (504 scalar equations)")
    print("verified 407 passing and 13 failing full two-hole identities")
    print("failure classes: 8 target, 4 correction, 1 cofactor")
    print("representative residuals:", representatives)
    print("verified model automorphism group is trivial; 13 literal singleton orbits")
    print("verified unique cofactor coefficient factor:", factor)
    print("verified all 11 coordinate-boundary branches retain active anchors and star independence")
    print("boundary audit:", boundary_data)


if __name__ == "__main__":
    main()
