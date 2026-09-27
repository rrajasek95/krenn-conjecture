"""Exact six-site fixed-core matrices and rational certificate verification."""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('frontier_arithmetic',
    ROOT / 'computations/quantitative-proof-identities-2026-09-26/verify.py')
arithmetic = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = arithmetic
spec.loader.exec_module(arithmetic)
C, ZERO, ONE = arithmetic.C, arithmetic.ZERO, arithmetic.ONE


def require(value, message):
    if not value:
        raise ValueError(message)


def conj(z):
    z = C.cast(z)
    return C(z.re, -z.im)


def decode(z):
    return C(Q(z[0]), Q(z[1])) if isinstance(z, list) else C(Q(z))


def encode(z):
    z = C.cast(z)
    return [str(z.re), str(z.im)]


def matchings(vs):
    if not vs:
        yield ()
        return
    for j in range(1, len(vs)):
        for rest in matchings(vs[1:j]+vs[j+1:]):
            yield ((vs[0], vs[j]),)+rest


def read_source(entries):
    source = {}
    for row in entries:
        key = tuple(row['cell'])
        require(len(key) == 4 and all(isinstance(k, int) for k in key), 'Integer cell indices')
        p, q, i, j = key
        require(0 <= p < q < 6 and 0 <= i < 3 and 0 <= j < 3, 'Valid endpoint-color cell')
        require(key not in source, 'Duplicate source cell')
        source[key] = decode(row['value'])
    return source


def matrices(source, root):
    require(root in range(6), 'Valid root')
    require(all(root not in key[:2] for key in source), 'Core excludes all incident cells')
    vertices = tuple(v for v in range(6) if v != root)
    columns = tuple(product(vertices, range(3)))
    words = tuple(product(range(3), repeat=5))
    response = []
    for word in words:
        colors = dict(zip(vertices, word))
        row = []
        for p, color in columns:
            value = ZERO
            if colors[p] == color:
                for matching in matchings(tuple(v for v in vertices if v != p)):
                    term = ONE
                    for a, b in matching:
                        term *= source.get((a, b, colors[a], colors[b]), ZERO)
                    value += term
            row.append(value)
        response.append(row)
    gram = [[ZERO]*15 for _ in range(15)]
    for row in response:
        active = [(i, v) for i, v in enumerate(row) if v]
        for i, v in active:
            for j, w in active:
                gram[i][j] += conj(v)*w
    target = [conj(v) for h in range(3) for v in response[words.index((h,)*5)]]
    K = [[gram[i % 15][j % 15] if i//15 == j//15 else ZERO
          for j in range(45)] for i in range(45)]
    U = [[v*conj(w)/3 for w in target] for v in target]
    energy = sum(v.abs2() for v in source.values())
    require(energy > 0, 'Positive core energy')
    return dict(T=response, gram=gram, K=K, U=U, target=target, energy=energy)


def dot(v, w):
    return sum((conj(x)*y for x, y in zip(v, w)), ZERO)


def apply(matrix, v):
    return [sum((x*y for x, y in zip(row, v)), ZERO) for row in matrix]


def quadratic(matrix, v):
    out = dot(v, apply(matrix, v))
    require(not out.im, 'Hermitian quadratic form must be real')
    return out.re


def solve(matrix, rhs):
    """One exact solution, allowing a singular consistent matrix."""
    a = [list(row)+[value] for row, value in zip(matrix, rhs)]
    n, pivot_row, pivots = len(matrix), 0, []
    for col in range(n):
        found = next((i for i in range(pivot_row, n) if a[i][col]), None)
        if found is None:
            continue
        a[pivot_row], a[found] = a[found], a[pivot_row]
        pivot = a[pivot_row][col]
        a[pivot_row] = [v/pivot for v in a[pivot_row]]
        for i in range(n):
            if i != pivot_row and a[i][col]:
                factor = a[i][col]
                a[i] = [v-factor*w for v, w in zip(a[i], a[pivot_row])]
        pivots.append(col)
        pivot_row += 1
    require(all(any(row[:n]) or not row[n] for row in a), 'Consistent normal equations')
    result = [ZERO]*n
    for i, col in enumerate(pivots):
        result[col] = a[i][n]
    require(apply(matrix, result) == rhs, 'Normal equation residual')
    return result


def fidelity_ceiling(data):
    value = ZERO
    for h in range(3):
        v = data['target'][15*h:15*(h+1)]
        value += dot(v, solve(data['gram'], v))
    require(not value.im, 'Real fidelity ceiling')
    return value.re/3


def psd(matrix):
    """Exact Hermitian Schur pivots; rejects negative or invalid zero pivots."""
    a = [row[:] for row in matrix]
    n = len(a)
    require(all(len(row) == n for row in a), 'Square matrix')
    require(all(a[i][j] == conj(a[j][i]) for i in range(n) for j in range(n)), 'Hermitian matrix')
    positive, zeros = 0, 0
    for k in range(n):
        d = a[k][k]
        require(not d.im and d.re >= 0, 'Nonnegative Schur pivot')
        if not d:
            require(all(not a[i][k] for i in range(k+1, n)), 'Zero pivot has zero column')
            zeros += 1
            continue
        positive += 1
        active = [i for i in range(k+1, n) if a[i][k]]
        for i in active:
            for j in active:
                a[i][j] -= a[i][k]*conj(a[j][k])/d
    return dict(positive_pivots=positive, zero_pivots=zeros)


def verify_certificate(payload):
    source = read_source(payload['core'])
    data = matrices(source, payload['root'])
    F0 = Q(payload['fidelity_floor'])
    require(0 <= F0 <= 1, 'Fidelity floor range')
    ceiling = fidelity_ceiling(data)
    require(F0 <= ceiling, 'Requested fidelity is feasible')
    mu, c = Q(payload['mu']), Q(payload['upper_eigenvalue'])
    require(mu >= 0, 'Nonnegative dual multiplier')
    K, U = data['K'], data['U']
    slack = [[C(c if i == j else 0)-K[i][j]-mu*(U[i][j]-F0*K[i][j])
              for j in range(45)] for i in range(45)]
    pivots = psd(slack)
    v = [decode(x) for x in payload['witness']]
    require(len(v) == 45, 'All 45 incident cells are represented')
    norm2, strength, signal = dot(v, v).re, quadratic(K, v), quadratic(U, v)
    require(norm2 > 0 and strength > 0 and signal >= F0*strength, 'Feasible nonzero witness')
    factor = Q(4, 27)/data['energy']**2
    lower, upper = factor*strength/norm2, factor*c
    require(lower <= upper, 'Primal-dual ordering')
    return dict(fidelity_floor=str(F0), fixed_core_fidelity_ceiling=str(ceiling),
                witness_fidelity=str(signal/strength), core_energy=str(data['energy']),
                optimal_incident_energy=str(data['energy']/2),
                rate_lower=str(lower), rate_upper=str(upper),
                relative_gap=str((upper-lower)/lower), psd=pivots)
