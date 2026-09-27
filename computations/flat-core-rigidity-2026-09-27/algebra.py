"""Exact matching tensors, derivatives, and canonical critical cores."""

from itertools import combinations, product
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "computations/boundary-structure-2026-09-26"))
from exact import E, ZERO, ONE, OMEGA, cell, hafnian, matchings, outputs, rank, require


def cells(n, q):
    return [(i, j, a, b) for i, j in combinations(range(n), 2)
            for a, b in product(range(q), repeat=2)]


def clean(source):
    return {key: value for key, value in source.items() if value}


def restrict(source, vertices):
    positions = {v: i for i, v in enumerate(vertices)}
    return {(positions[i], positions[j], a, b): value
            for (i, j, a, b), value in source.items()
            if i in positions and j in positions}


def four_outputs(source, n, q):
    return {(vertices, word): value
            for vertices in combinations(range(n), 4)
            for word, value in outputs(restrict(source, vertices), n=4, colors=q).items()}


def four_derivative(source, n, q):
    columns = cells(n, q)
    index = {c: j for j, c in enumerate(columns)}
    rows = {}
    for vertices in combinations(range(n), 4):
        for i, j in combinations(vertices, 2):
            k, l = [v for v in vertices if v not in (i, j)]
            for a, b, c, d in product(range(q), repeat=4):
                z = source.get((k, l, c, d), ZERO)
                if z:
                    word = tuple({i: a, j: b, k: c, l: d}[v] for v in vertices)
                    row = rows.setdefault((vertices, word), [ZERO]*len(columns))
                    row[index[i, j, a, b]] += z
    return columns, rows


def determinant(matrix):
    a = [row[:] for row in matrix]
    det = ONE
    for col in range(len(a)):
        pivot = next((i for i in range(col, len(a)) if a[i][col]), None)
        if pivot is None:
            return ZERO
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            det = -det
        d = a[col][col]
        det *= d
        for i in range(col+1, len(a)):
            factor = a[i][col]/d
            for j in range(col, len(a)):
                a[i][j] -= factor*a[col][j]
    return det


def five_ground():
    ground = {(0, 1): ONE, (2, 3): ONE, (0, 2): OMEGA,
              (1, 3): OMEGA, (0, 3): OMEGA*OMEGA, (1, 2): OMEGA*OMEGA}
    return ground | {(i, 4): ONE for i in range(4)}


def five_core(q=1, dense_vectors=False):
    vectors = [[E(i+a+1, (i+2*a) % 3) if dense_vectors
                else (ONE if a == 0 else ZERO) for a in range(q)] for i in range(5)]
    return clean({(i, j, a, b): z*vectors[i][a]*vectors[j][b]
                  for (i, j), z in five_ground().items()
                  for a, b in product(range(q), repeat=2)})


def four_core():
    I = [[ONE, ZERO], [ZERO, ONE]]
    J = [[ZERO, ONE], [-ONE, ZERO]]
    blocks = {(0, 1): I, (0, 2): I, (0, 3): I,
              (1, 2): J, (1, 3): [[-z for z in row] for row in J], (2, 3): J}
    return clean({(i, j, a, b): block[a][b] for (i, j), block in blocks.items()
                  for a, b in product(range(2), repeat=2)})


def star(n, q):
    return {(0, i, a, a): ONE for i in range(1, n) for a in range(q)}


def add_sources(*sources):
    result = {}
    for source in sources:
        for key, value in source.items():
            result[key] = result.get(key, ZERO)+value
    return clean(result)


def scale(source, value):
    return clean({key: value*z for key, z in source.items()})


def norm2(source):
    return sum(z.abs2() for z in source.values())
