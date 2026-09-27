"""Exploration only: finite-field sections of the critical quadratic cone."""
from itertools import combinations, product
from random import Random
import json

P = 1009
W = next(x for x in range(2, P) if (x*x+x+1) % P == 0)
EDGES = tuple(combinations(range(5), 2))
Q = {(0, 1): 1, (2, 3): 1, (0, 2): W, (1, 3): W,
     (0, 3): W*W % P, (1, 2): W*W % P, **{(i, 4): 1 for i in range(4)}}
CELLS = tuple((i, j, a, b) for i, j in EDGES for a, b in product(range(2), repeat=2))
WORDS = tuple(product(range(2), repeat=5))
ROWS = tuple((i, a) for i in range(5) for a in range(2))


def nullspace(matrix):
    a = [[z % P for z in row] for row in matrix]
    pivots, r = [], 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][col], -1, P)
        a[r] = [z*inv % P for z in a[r]]
        for i in range(len(a)):
            if i != r and a[i][col]:
                d = a[i][col]
                a[i] = [(x-d*y) % P for x, y in zip(a[i], a[r])]
        pivots.append(col)
        r += 1
        if r == len(a):
            break
    basis = []
    for free in range(len(a[0])):
        if free in pivots:
            continue
        vector = [0]*len(a[0])
        vector[free] = 1
        for i, col in enumerate(pivots):
            vector[col] = -a[i][free] % P
        basis.append(vector)
    return basis


def matrix(row):
    out = [[0]*len(CELLS) for _ in WORDS]
    for w_index, word in enumerate(WORDS):
        for c_index, (i, j, a, b) in enumerate(CELLS):
            if word[i] != a or word[j] != b:
                continue
            rest = [v for v in range(5) if v not in (i, j)]
            for k in rest:
                e = tuple(v for v in rest if v != k)
                if all(word[v] == 0 for v in e):
                    out[w_index][c_index] += Q[e]*row[k, word[k]]
            out[w_index][c_index] %= P
    return out


def quartic(row, source):
    value = 0
    for (i, j), q in Q.items():
        word = [1]*5
        word[i] = word[j] = 0
        cubic = 0
        for k in range(5):
            rest = tuple(v for v in range(5) if v != k)
            for t in range(1, 4):
                e = (rest[0], rest[t])
                f = tuple(v for v in rest if v not in e)
                cubic += row[k, word[k]]*source[e[0], e[1], word[e[0]], word[e[1]]]*source[f[0], f[1], word[f[0]], word[f[1]]]
        value += source[i, j, 1, 1]*pow(2*q, -1, P)*cubic
    return value % P


def run():
    rng = Random(260926)
    cases = []
    rows = []
    for support_size in range(6):
        for a_support in (0, 1, 2, 5):
            for trial in range(3):
                active_b = rng.sample(range(5), support_size)
                active_a = rng.sample(range(5), a_support)
                row = {(i, h): rng.randrange(1, P) if i in (active_a if h == 0 else active_b) else 0
                       for i, h in ROWS}
                rows.append(row)
    special = {key: 0 for key in ROWS}
    for i, z in enumerate((1, -1, 1, -1, 0)):
        special[i, 0] = z % P
    rows.append(special)
    for row in rows:
        mat = matrix(row)
        basis = nullspace(mat)
        for _ in range(12):
            coefficients = [rng.randrange(P) for _ in basis]
            vector = [sum(c*b[j] for c, b in zip(coefficients, basis)) % P for j in range(len(CELLS))]
            if any(sum(x*y for x, y in zip(m, vector)) % P for m in mat):
                raise ValueError('Kernel reconstruction failed')
            f = quartic(row, dict(zip(CELLS, vector)))
            if f:
                return dict(status='COUNTEREXAMPLE_OVER_FINITE_FIELD', prime=P, omega=W,
                            root_row=[row[key] for key in ROWS], core_vector=vector, quartic=f,
                            interpretation='Exploratory; not yet a characteristic-zero or GHZ-arc result')
        cases.append(dict(nonzero_root_a=sum(bool(row[i, 0]) for i in range(5)),
                          nonzero_root_b=sum(bool(row[i, 1]) for i in range(5)), kernel_dimension=len(basis)))
    return dict(status='NO_COUNTEREXAMPLE_FOUND', prime=P, omega=W, sections=len(rows),
                tested_directions=12*len(rows), cases=cases,
                interpretation='Finite-field samples only; not a proof of quartic vanishing')


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
