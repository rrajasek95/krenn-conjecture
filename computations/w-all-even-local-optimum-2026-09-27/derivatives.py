"""Enumerate actual matchings for the all-even W design and its derivatives."""

from fractions import Fraction as Q
from itertools import combinations, product
from math import prod
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT/"computations/boundary-structure-2026-09-26"))
from exact import require, matchings


def double_factorial(n):
    return prod(range(1, n+1, 2))


def rational_rank(rows):
    pivots = {}
    for original in rows:
        row = {j: Q(z) for j, z in original.items() if z}
        while row:
            lead = min(row)
            if lead not in pivots:
                d = row[lead]
                pivots[lead] = {j: z/d for j, z in row.items()}
                break
            d = row[lead]
            for j, z in pivots[lead].items():
                row[j] = row.get(j, Q(0))-d*z
                if not row[j]:
                    del row[j]
    return len(pivots)


def build(N):
    n, g, c = N+1, N*N+1, double_factorial(N-2)
    cells = [(i, j, a, b) for i, j in combinations(range(n), 2)
             for a, b in product(range(2), repeat=2)]
    ix = {cell: i for i, cell in enumerate(cells)}
    base = [1 if i > 0 and a == b == 0 else N if i == 0 and (a, b) == (0, 1)
            else 1 if i == 0 and (a, b) == (1, 0) else 0 for i, j, a, b in cells]
    metric = [g if i > 0 else 1 for i, j, a, b in cells]
    active = {edge: [(a, b, base[ix[*edge, a, b]]) for a, b in product(range(2), repeat=2)
                     if base[ix[*edge, a, b]]]
              for edge in combinations(range(n), 2)}
    jac, output, hessian = {}, {}, {}
    for matching in matchings(tuple(range(n))):
        for choices in product(*(active[edge] for edge in matching)):
            word, value = [0]*n, 1
            for (i, j), (a, b, z) in zip(matching, choices):
                word[i], word[j] = a, b
                value *= z
            word = tuple(word)
            output[word] = output.get(word, 0)+value
        for p, varied in enumerate(matching):
            rest = [edge for j, edge in enumerate(matching) if j != p]
            for choices in product(*(active[edge] for edge in rest)):
                word, value = [0]*n, 1
                for (i, j), (a, b, z) in zip(rest, choices):
                    word[i], word[j] = a, b
                    value *= z
                i, j = varied
                for a, b in product(range(2), repeat=2):
                    word[i], word[j] = a, b
                    row = jac.setdefault(tuple(word), {})
                    col = ix[i, j, a, b]
                    row[col] = row.get(col, 0)+value
        # Only W words carry a nonzero Lagrange multiplier.
        for excited in range(n):
            word = [int(i == excited) for i in range(n)]
            indices = [ix[i, j, word[i], word[j]] for i, j in matching]
            dual_numerator = 1 if excited == 0 else N
            for p, q in combinations(range(len(matching)), 2):
                value = dual_numerator*prod(base[indices[j]] for j in range(len(matching))
                                           if j not in (p, q))
                if value:
                    pair = tuple(sorted((indices[p], indices[q])))
                    hessian[pair] = hessian.get(pair, 0)+value
    hessian = {pair: Q(value, c) for pair, value in hessian.items()}
    require(output == {tuple(int(i == j) for i in range(n)): N*c for j in range(n)},
            "Complete matching expansion gives exactly the W output")
    gradient = [Q(0)]*len(cells)
    for word, row in jac.items():
        if sum(word) == 1:
            multiplier = Q(1 if word[0] else N, c)
            for j, value in row.items():
                gradient[j] += multiplier*value
    require(gradient == [z*w for z, w in zip(base, metric)],
            "Exact stationarity in every source coordinate")
    rank = rational_rank(jac.values())
    require(rank == N*(N+1)+2, "Full Jacobian rank")
    return dict(N=N, cells=cells, index=ix, base=base, metric=metric,
                jacobian=jac, hessian=hessian, rank=rank)
