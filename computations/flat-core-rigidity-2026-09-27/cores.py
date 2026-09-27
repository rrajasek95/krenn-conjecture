"""Check canonical flat cores, exact minors, and derivative ranks."""

from itertools import combinations, product
from math import comb
from algebra import (E, ZERO, ONE, OMEGA, require, rank, cells, clean,
                     determinant, five_ground, five_core, four_core, star,
                     four_outputs, four_derivative)


def check():
    records = []
    for n, q in product((5, 6), (1, 2, 3)):
        source = five_core(q)
        require(not four_outputs(source, n, q), "Every canonical five-core response vanishes")
        columns, rows = four_derivative(source, n, q)
        actual = rank(list(rows.values()))
        require(actual == comb(n, 2)*q*q-5*q, "Five-core derivative rank")
        dense = five_core(q, dense_vectors=True)
        require(not four_outputs(dense, n, q), "Nontrivial local product-vector fixture")
        records.append(dict(family="five_core", sites=n, colors=q, rank=actual,
                            source_dimension=len(columns), kernel_dimension=5*q))
    columns, rows = four_derivative(five_core(), 5, 1)
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)]
    minor = [[rows[tuple(v for v in range(5) if v != omit), (0,)*4]
              [columns.index((*edge, 0, 0))] for edge in edges] for omit in range(5)]
    require(determinant(minor) == E(-4, -8), "Explicit nonzero five-core minor")
    ground = five_ground()
    insertion = [[ground[tuple(v for v in triple if v != i)] if i in triple else ZERO
                  for i in range(5)] for triple in combinations(range(5), 3)]
    require(rank(insertion) == 5, "Isolated-site insertion has no kernel")

    source = four_core()
    for i, j in combinations(range(4), 2):
        require(bool(determinant([[source.get((i, j, a, b), ZERO)
                                   for b in range(2)] for a in range(2)])),
                "All six binary core blocks are invertible")
    for n in (4, 5, 6):
        require(not four_outputs(source, n, 2), "All binary four-core responses vanish")
        columns, rows = four_derivative(source, n, 2)
        actual = rank(list(rows.values()))
        require(actual == 4*comb(n, 2)-13, "Binary four-core derivative rank")
        records.append(dict(family="binary_four_core", sites=n, colors=2, rank=actual,
                            source_dimension=len(columns), kernel_dimension=13))
    # Directly solve the four-site lemma with C of rank one and two.
    for C in ([[ONE, ZERO], [ZERO, ZERO]], [[E(2, 1), ONE], [OMEGA, E(3)]]):
        base = {(0, i, a, a): ONE for i in (1, 2) for a in range(2)}
        base.update({(0, 3, a, b): C[a][b] for a, b in product(range(2), repeat=2)})
        columns, rows = four_derivative(clean(base), 4, 2)
        leaf_columns = [j for j, c in enumerate(columns) if c[0] != 0]
        require(rank([[row[j] for j in leaf_columns] for row in rows.values()]) == 11,
                "Four-site lemma has exactly a one-dimensional solution")
        J = [[ZERO, ONE], [-ONE, ZERO]]
        JC = [[sum((J[a][c]*C[c][b] for c in range(2)), ZERO)
               for b in range(2)] for a in range(2)]
        for a, b in product(range(2), repeat=2):
            base[1, 2, a, b] = J[a][b]
            base[1, 3, a, b] = -JC[a][b]
            base[2, 3, a, b] = JC[a][b]
        require(not four_outputs(base, 4, 2), "Four-site lemma signs and coefficients")

    for n in (5, 6):
        source = star(n, 2)
        require(not four_outputs(source, n, 2), "A star has no four-site matchings")
        columns, rows = four_derivative(source, n, 2)
        actual = rank(list(rows.values()))
        require(actual == 4*comb(n, 2)-4*(n-1), "Binary star derivative rank")
        records.append(dict(family="binary_star", sites=n, colors=2, rank=actual,
                            source_dimension=len(columns), kernel_dimension=4*(n-1)))

    bad = five_core()
    bad[0, 1, 0, 0] += ONE
    require(bool(four_outputs(bad, 5, 1)), "Wrong cube-root core coefficient is rejected")
    bad = five_core() | {(0, 5, 0, 0): ONE}
    require(bool(four_outputs(bad, 6, 1)), "Nonzero outside edge violates isolation")
    bad = four_core()
    bad[1, 3, 0, 1] *= -1
    require(bool(four_outputs(bad, 4, 2)), "Wrong antisymmetric-core sign is rejected")
    return dict(derivative_ranks=records, five_core_minor=["-4", "-8"],
                insertion_rank=5, four_site_lemma_ranks=[11, 11],
                mutations=["cube-root coefficient rejected", "outside edge rejected",
                           "antisymmetric sign rejected"])
