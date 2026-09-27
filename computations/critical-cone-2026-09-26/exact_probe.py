"""Lift the exploratory quadratic-cone section to Q(omega)."""
from itertools import combinations, product
from random import Random
from pathlib import Path
import sys
import json
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'higher-order-2026-09-26'))
from shared import E, Q, ZERO, ONE, OMEGA, require, critical_core, outputs, matchings
from probe import CELLS, WORDS, ROWS


def rref(matrix, rhs=None):
    n = len(matrix[0])
    a = [list(row)+([] if rhs is None else [b]) for row, b in zip(matrix, rhs or [ZERO]*len(matrix))]
    pivots, r = [], 0
    for col in range(n):
        pivot = next((i for i in range(r, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        d = a[r][col]
        a[r] = [z/d for z in a[r]]
        for i in range(len(a)):
            if i != r and a[i][col]:
                d = a[i][col]
                a[i] = [x-d*y for x, y in zip(a[i], a[r])]
        pivots.append(col)
        r += 1
        if r == len(a):
            break
    if rhs is not None and any(not any(row[:n]) and row[n] for row in a):
        return pivots, [], None
    basis = []
    for free in range(n):
        if free in pivots:
            continue
        v = [ZERO]*n
        v[free] = ONE
        for i, col in enumerate(pivots):
            v[col] = -a[i][free]
        basis.append(v)
    solution = [ZERO]*n
    if rhs is not None:
        for i, col in enumerate(pivots):
            solution[col] = a[i][n]
    return pivots, basis, solution


def matrix(row):
    q = critical_core()
    out = [[ZERO]*len(CELLS) for _ in WORDS]
    for wi, word in enumerate(WORDS):
        for ci, (i, j, a, b) in enumerate(CELLS):
            if word[i] != a or word[j] != b:
                continue
            rest = [v for v in range(5) if v not in (i, j)]
            for k in rest:
                edge = tuple(v for v in rest if v != k)
                if all(word[v] == 0 for v in edge):
                    out[wi][ci] += q[edge]*row[k, word[k]]
    return out


def quartic(source):
    h = outputs(source)
    value = ZERO
    for (i, j), q in critical_core().items():
        word = [1]*6
        word[i] = word[j] = 0
        value += source.get((i, j, 1, 1), ZERO)*h.get(tuple(word), ZERO)/(2*q)
    return value


def extension(source):
    base = {(i, j, 0, 0): z for (i, j), z in critical_core().items()}
    cells = tuple((i, j, a, b) for i, j in combinations(range(6), 2) for a, b in product(range(2), repeat=2))
    indexes = {c: i for i, c in enumerate(cells)}
    words = tuple(product(range(2), repeat=6))
    mat = []
    for word in words:
        row = [ZERO]*len(cells)
        for matching in matchings(tuple(range(6))):
            keys = [(i, j, word[i], word[j]) for i, j in matching]
            for k in range(3):
                i, j = [v for v in range(3) if v != k]
                row[indexes[keys[k]]] += base.get(keys[i], ZERO)*source.get(keys[j], ZERO)+base.get(keys[j], ZERO)*source.get(keys[i], ZERO)
        mat.append(row)
    h = outputs(source)
    rhs = [-h.get(word, ZERO) for word in words]
    pivots, basis, solution = rref(mat, rhs)
    witness = None
    if solution is not None:
        require(all(sum((x*y for x, y in zip(row, solution)), ZERO) == b for row, b in zip(mat, rhs)),
                'Third-order extension solves every binary output equation')
    else:
        _, dual_basis, _ = rref([list(row) for row in zip(*mat)])
        witness = next(v for v in dual_basis if sum((x*y for x, y in zip(v, rhs)), ZERO))
        require(all(sum((w*row[j] for w, row in zip(witness, mat)), ZERO) == ZERO for j in range(len(cells))),
                'Exact left-null obstruction')
    return dict(rank=len(pivots), consistent=solution is not None,
                source=None if solution is None else dict(zip(cells, solution)),
                witness=None if witness is None else dict(zip(words, witness)),
                pairing=None if witness is None else sum((x*y for x,y in zip(witness,rhs)),ZERO))


def encode(z):
    return [str(z.a), str(z.b)]


def run():
    row = {key: ZERO for key in ROWS}
    row[3, 0] = row[0, 1] = row[4, 1] = ONE
    mat = matrix(row)
    pivots, basis, _ = rref(mat)
    rng = Random(260926)
    candidates = []
    for i in range(len(basis)):
        coefficients = [0]*len(basis)
        coefficients[i] = 1
        candidates.append(coefficients)
    for i, j in combinations(range(len(basis)), 2):
        for sign in (1, -1):
            coefficients = [0]*len(basis)
            coefficients[i], coefficients[j] = 1, sign
            candidates.append(coefficients)
    candidates += [[rng.choice((-1, 0, 1)) for _ in basis] for _ in range(20)]
    def build(coefficients):
        vector = [sum((c*b[j] for c, b in zip(coefficients, basis)), ZERO) for j in range(len(CELLS))]
        source = dict(zip(CELLS, vector))
        source.update({(i, 5, h, 1): z for (i, h), z in row.items()})
        return vector, source
    for coefficients in candidates:
        vector, source = build(coefficients)
        require(all(sum((x*y for x, y in zip(m, vector)), ZERO) == ZERO for m in mat), 'Exact quadratic cone')
        value = quartic(source)
        if value:
            for i in range(len(coefficients)):
                trial = list(coefficients)
                trial[i] = 0
                if quartic(build(trial)[1]):
                    coefficients = trial
            vector, source = build(coefficients)
            value = quartic(source)
            ext = extension(source)
            return dict(status='EXACT_NONZERO_QUARTIC', kernel_dimension=len(basis), rank=len(pivots),
                        quartic=encode(value), first_jet={','.join(map(str,c)):encode(z) for c,z in source.items() if z},
                        binary_third_order_rank=ext['rank'], third_order_extension_exists=ext['consistent'],
                        obstruction=None if ext['witness'] is None else {''.join(map(str,w)):encode(z) for w,z in ext['witness'].items() if z},
                        obstruction_pairing=None if ext['pairing'] is None else encode(ext['pairing']),
                        second_jet=None if ext['source'] is None else {','.join(map(str,c)):encode(z) for c,z in ext['source'].items() if z},
                        scope='An exact binary cone direction, not a ternary GHZ arc')
    return dict(status='NO_EXACT_EXAMPLE_FOUND', kernel_dimension=len(basis), candidates=len(candidates))


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
