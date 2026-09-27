"""Pinned exact arithmetic from the preceding supporting package."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'computations/boundary-structure-2026-09-26'))
from exact import E, ZERO, ONE, OMEGA, Q, require, matchings, outputs, hafnian, cell
from examples import critical_core
import graphs


def solve(matrix, rhs):
    """Exact square solve, with an explicit nonsingularity check."""
    n = len(rhs)
    a = [[E.cast(z) for z in row]+[E.cast(b)] for row, b in zip(matrix, rhs)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        require(pivot is not None, 'Nonsingular fixture matrix')
        a[j], a[pivot] = a[pivot], a[j]
        d = a[j][j]
        a[j] = [z/d for z in a[j]]
        for i in range(n):
            if i != j and a[i][j]:
                d = a[i][j]
                a[i] = [x-d*y for x, y in zip(a[i], a[j])]
    return [row[-1] for row in a]


def mv(matrix, vector):
    return [sum((a*b for a, b in zip(row, vector)), ZERO) for row in matrix]


def dot(left, right):
    return sum((a*b for a, b in zip(left, right)), ZERO)


def energy(source):
    return sum(z.abs2() for z in source.values())
