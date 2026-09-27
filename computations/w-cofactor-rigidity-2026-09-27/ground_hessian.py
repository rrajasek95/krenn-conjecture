"""Exact quadratic expansion of the unrestricted scalar W response cost."""

from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations
from math import prod
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT/"computations/boundary-structure-2026-09-26"))
from exact import E, ZERO, ONE, require


def plus(*jets):
    return tuple(sum((p[j] for p in jets), ZERO) for j in range(3))


def times(p, q):
    return tuple(sum((p[k]*q[j-k] for k in range(j+1)), ZERO) for j in range(3))


def power(p, n):
    result = (ONE, ZERO, ZERO)
    for _ in range(n):
        result = times(result, p)
    return result


def inverse(p):
    require(bool(p[0]), "Invertible constant term")
    return (ONE/p[0], -p[1]/(p[0]*p[0]),
            p[1]*p[1]/(p[0]*p[0]*p[0])-p[2]/(p[0]*p[0]))


def squared(p):
    result = times(p, tuple(z.conjugate() for z in p))
    require(all(not z.b for z in result), "Norm coefficients are real rationals")
    return result


def real2(z):
    return (z.a-z.b/2)**2


def imag2(z):
    return Q(3, 4)*z.b*z.b


def check_fixture(n, name, d, z):
    N, q, k, g = n-1, n//2-1, n-3, (n-1)**2+1
    c = prod(range(1, n-2, 2))
    require(not sum(z.values(), ZERO), "First-order root vector has zero sum")
    total = sum(d.values(), ZERO)
    row = {i: sum((value for edge, value in d.items() if i in edge), ZERO)
           for i in range(1, n)}
    alpha = total/Q(N*q)
    u = {i: (row[i]-(N-1)*alpha)/k for i in range(1, n)}
    h = {e: value-alpha-u[e[0]]-u[e[1]] for e, value in d.items()}
    require(not sum(u.values(), ZERO), "Site deformation has zero sum")
    require(all(not sum((value for e, value in h.items() if i in e), ZERO)
                for i in range(1, n)), "Residual core deformation has zero row sums")

    D = {e: (ONE, value, ZERO) for e, value in d.items()}
    for i in range(1, n):
        D[0, i] = (ZERO, z[i], ZERO)
    # The root hafnian is linear in the root vector. This correction
    # keeps the ground equation zero through second order.
    curvature = -sum((z[i]*(total-row[i])/k for i in range(1, n)), ZERO)
    D[0, N] = (ZERO, z[N], curvature)

    @lru_cache(None)
    def haf(vertices):
        if not vertices:
            return (ONE, ZERO, ZERO)
        i = vertices[0]
        return plus(*(times(D[i, j], haf(tuple(v for v in vertices if v not in (i, j))))
                      for j in vertices[1:]))

    require(not any(haf(tuple(range(n)))), "The chosen jet satisfies the zero-hafnian constraint")
    C = {e: haf(tuple(v for v in range(n) if v not in e))
         for e in combinations(range(n), 2)}
    rows = [plus(*(squared(value) for edge, value in C.items() if i in edge))
            for i in range(n)]
    a = plus(*(squared(value) for value in D.values()))
    beta = plus(*(inverse(r) for r in rows))
    F = times(power(a, q), beta)
    F0 = Q((N*q)**q*g, N*c*c)
    expected = (
        Q(2*(N**3-N**2+N-3), N*g)*sum(real2(v) for v in u.values())
        + Q(N-3, N*(N-2))*sum(real2(v) for v in h.values())
        + Q(N-1, N*(N-2))*sum(imag2(v) for v in h.values())
        + Q((N-4)*N*N+N-2, N*(N-2)*g)*sum(v.abs2() for v in z.values()))
    require(F[0] == E(F0) and not F[1], "Correct value and stationarity")
    require(F[2] == E(F0*expected), "Entire complex constrained Hessian formula")
    if name == "phase_and_scale":
        require(not expected, "Only equality-orbit directions in this fixture")
    else:
        require(expected > 0, "Strict positive second variation in the tested direction")
    return dict(sites=n, fixture=name, normalized_quadratic_cost=str(expected),
                zero_ground_jet_orders=[0, 1, 2])


def check():
    records = []
    for n in (6, 8, 10, 12):
        edges = list(combinations(range(1, n), 2))
        d = {e: E((2*e[0]+e[1]) % 5-2, (e[0]+2*e[1]) % 5-2) for e in edges}
        z = {i: E(i % 3-1, (2*i) % 5-2) for i in range(1, n-1)}
        z[n-1] = -sum(z.values(), ZERO)
        records.append(check_fixture(n, "dense_complex", d, z))
        records.append(check_fixture(n, "root_only", {e: ZERO for e in edges}, z))
        d = {(i, j): ONE+E(1, 2)*(i+j) for i, j in edges}
        records.append(check_fixture(n, "phase_and_scale", d,
                                     {i: ZERO for i in range(1, n)}))
    require(len(records) == 12, "All twelve constrained Hessian fixtures")
    return records
