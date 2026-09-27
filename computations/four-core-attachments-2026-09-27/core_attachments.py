"""Exact attachment ranks, exceptional kernels, and the scalar determinant."""

from itertools import combinations, permutations, product
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "computations/flat-core-rigidity-2026-09-27"))
from algebra import (E, ZERO, ONE, OMEGA, clean, four_outputs, four_derivative,
                     rank, require, five_ground)


def attachment_matrix(core, q):
    columns = [(i, 4, a, b) for i in range(4)
               for a, b in product(range(q), repeat=2)]
    index = {c: j for j, c in enumerate(columns)}
    rows = []
    for triple in combinations(range(4), 3):
        for word in product(range(q), repeat=4):
            colors = dict(zip((*triple, 4), word))
            row = [ZERO]*len(columns)
            for i in triple:
                j, k = [v for v in triple if v != i]
                row[index[i, 4, colors[i], colors[4]]] += core.get(
                    (j, k, colors[j], colors[k]), ZERO)
            rows.append(row)
    return columns, rows


def scalar_core(weights, q, dense=False):
    vectors = [[E(i+a+1, (i+2*a) % 3) if dense
                else (ONE if a == 0 else ZERO) for a in range(q)] for i in range(4)]
    source = clean({(i, j, a, b): z*vectors[i][a]*vectors[j][b]
                    for (i, j), z in weights.items()
                    for a, b in product(range(q), repeat=2)})
    return source, vectors


def gram_core(q, full_rank_sites):
    # Pluecker identity: [01][23] - [02][13] + [03][12] = 0.
    factors = []
    lines = [(ONE, E(2)), (ONE, ZERO), (ZERO, ONE), (ONE, ONE)]
    for i in range(4):
        if i in full_rank_sites:
            factors.append([[ONE, ZERO], [ZERO, ONE]]
                           + [[E(a+1), E(i+a+2, 1)] for a in range(2, q)])
        else:
            factors.append([[E(a+i+1)*z for z in lines[i]] for a in range(q)])
    return clean({(i, j, a, b): (-ONE if (i, j) == (1, 3) else ONE) *
                  (factors[i][a][0]*factors[j][b][1]
                   - factors[i][a][1]*factors[j][b][0])
                  for i, j in combinations(range(4), 2)
                  for a, b in product(range(q), repeat=2)})


def fixtures(q):
    generic = {e: ONE for e in combinations(range(4), 2)}
    generic[1, 2] = E(-2)
    cube = {e: z for e, z in five_ground().items() if 4 not in e}
    cycle = {(0, 1): ONE, (2, 3): ONE, (0, 2): ONE, (1, 3): -ONE}
    result = []
    for name, weights, dense, exceptional in (
            ("scalar_full_generic", generic, False, False),
            ("cube", cube, False, True),
            ("dense_cube", cube, True, True),
            ("four_cycle", cycle, False, False)):
        source, vectors = scalar_core(weights, q, dense)
        result.append((name, source, exceptional, vectors))
    source, _ = scalar_core(cycle, q)
    result.append(("missing_edge_scalar_diagonal",
                   source | {(0, 3, 0, 0): ONE}, False, None))
    diagonal = {(0, 3, a, b): E(a+b+1, a+2*b)
                for a, b in product(range(q), repeat=2)}
    result.append(("missing_edge_dense_diagonal", source | diagonal, False, None))
    if q >= 2:
        for name, sites in (("all_invertible", {0, 1, 2, 3}),
                            ("invertible_triangle", {0, 1, 2}),
                            ("one_invertible_edge", {0, 1}),
                            ("rank_one_edges_distinct_directions", {0})):
            result.append((name, gram_core(q, sites), False, None))
    return result


def determinant_polynomial():
    """Check all coefficients in det M, in six independent scalar variables."""
    edges = list(combinations(range(4), 2))
    actual = {}
    for perm in permutations(range(4)):
        if any(i == j for i, j in enumerate(perm)):
            continue
        exponents = [0]*6
        for i, j in enumerate(perm):
            edge = tuple(v for v in range(4) if v not in (i, j))
            exponents[edges.index(edge)] += 1
        inversions = sum(perm[i] > perm[j] for i, j in combinations(range(4), 2))
        key = tuple(exponents)
        actual[key] = actual.get(key, 0)+(-1)**inversions
    actual = {key: z for key, z in actual.items() if z}
    products = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
    expected = {}
    for i in range(3):
        exponents = [0]*6
        for e in products[i]:
            exponents[edges.index(e)] += 2
        expected[tuple(exponents)] = 1
        for j in range(i+1, 3):
            exponents = [0]*6
            for e in (*products[i], *products[j]):
                exponents[edges.index(e)] += 1
            expected[tuple(exponents)] = -2
    require(actual == expected, "Full six-variable attachment determinant identity")
    require(len(actual) == 6, "All six determinant monomials accounted for")
    return len(actual)


def check():
    receipts, anchored = [], 0
    for q in (1, 2, 3):
        for name, core, exceptional, vectors in fixtures(q):
            require(not four_outputs(core, 4, q), "Core is exactly flat: "+name)
            support = {(i, j) for i, j, a, b in core}
            require(set.union(*(set(e) for e in support)) == set(range(4)),
                    "Exactly four active core sites")
            require(all(any(i not in edge for edge in support) for i in range(4)),
                    "Core support is not a star")
            columns, rows = attachment_matrix(core, q)
            actual_rank = rank(rows)
            require(actual_rank == 4*q*q-(q if exceptional else 0),
                    "Predicted attachment rank: "+name)

            # Compare a separately assembled insertion map with the full derivative.
            all_columns, derivative = four_derivative(core, 5, q)
            indices = [all_columns.index(c) for c in columns]
            independently_built = []
            for triple in combinations(range(4), 3):
                for word in product(range(q), repeat=4):
                    row = derivative.get(((*triple, 4), word), [ZERO]*len(all_columns))
                    independently_built.append([row[j] for j in indices])
            require(rows == independently_built, "Attachment map equals selected output derivative")

            if exceptional:
                for color in range(q):
                    kernel = [vectors[i][a] if b == color else ZERO
                              for i, r, a, b in columns]
                    require(any(kernel), "Nonzero exceptional attachment")
                    require(all(not sum((x*y for x, y in zip(row, kernel)), ZERO)
                                for row in rows), "Every explicit hidden direction is in the kernel")
                for i in range(4):
                    block_rows = [[ONE if j == k else ZERO for j in range(len(columns))]
                                  for k, c in enumerate(columns) if c[0] == i]
                    require(rank(rows+block_rows) == len(columns),
                            "Any one attachment block removes the whole kernel")
                    anchored += 1
            receipts.append(dict(palette=q, fixture=name, core_edges=len(support),
                                 attachment_variables=len(columns), rank=actual_rank,
                                 kernel_dimension=len(columns)-actual_rank))
    require(len(receipts) == 26 and anchored == 24, "Complete advertised fixture coverage")
    return dict(determinant_monomials=determinant_polynomial(),
                fixtures=receipts, full_rank_augmented_maps=anchored)
