#!/usr/bin/env python3
"""Numerically inspect weights on a support-closed selector repair candidate.

This historical search is retained for reproducibility.  The support is now
known to be exactly impossible; see ``verify_selector_candidate_obstruction.py``.
The least-squares infimum can therefore only approach the target through a
singular/border degeneration, never through an exact zero.
"""

import argparse
import itertools
from collections import defaultdict

import numpy as np
from scipy.optimize import least_squares


CELLS = [
    (0, 1, 0, 0), (0, 2, 1, 0), (0, 2, 1, 1), (0, 3, 2, 2),
    (0, 6, 1, 1), (0, 7, 0, 0), (1, 4, 1, 0), (1, 4, 1, 1),
    (1, 5, 2, 2), (1, 6, 0, 0), (1, 7, 1, 1), (2, 3, 0, 0),
    (2, 3, 0, 1), (2, 3, 1, 0), (2, 3, 1, 1), (2, 6, 2, 2),
    (3, 6, 0, 1), (3, 6, 1, 1), (4, 5, 0, 0), (4, 5, 0, 1),
    (4, 5, 1, 0), (4, 5, 1, 1), (4, 7, 2, 2), (5, 7, 0, 1),
    (5, 7, 1, 1), (6, 7, 0, 0),
]


def perfect_matchings(vertices):
    vertices = frozenset(vertices)
    if not vertices:
        yield ()
        return
    u = min(vertices)
    for v in sorted(vertices - {u}):
        for rest in perfect_matchings(vertices - {u, v}):
            yield tuple(sorted(((u, v),) + rest))


PMS = list(perfect_matchings(range(8)))
BY_EDGE = defaultdict(list)
for index, (u, v, a, b) in enumerate(CELLS):
    BY_EDGE[u, v].append((a, b, index))

TERMS = defaultdict(list)
for matching in PMS:
    choices = [BY_EDGE[e] for e in matching]
    if any(not choice for choice in choices):
        continue
    for decoration in itertools.product(*choices):
        coloring = [None] * 8
        indices = []
        for (u, v), (a, b, index) in zip(matching, decoration):
            coloring[u], coloring[v] = a, b
            indices.append(index)
        TERMS[tuple(coloring)].append(tuple(indices))

COLORINGS = sorted(TERMS)
TARGET = np.array([1.0 if len(set(c)) == 1 else 0.0 for c in COLORINGS])


def evaluate(z):
    return np.array([
        sum(np.prod(z[list(term)]) for term in TERMS[coloring])
        for coloring in COLORINGS
    ])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tries", type=int, default=30)
    parser.add_argument("--complex", action="store_true", dest="use_complex")
    args = parser.parse_args()
    rng = np.random.default_rng(49271)
    n = len(CELLS)
    for trial in range(args.tries):
        x0 = rng.normal(scale=0.7, size=n * (2 if args.use_complex else 1))

        def residual(x):
            if args.use_complex:
                z = x[:n] + 1j * x[n:]
                err = evaluate(z) - TARGET
                return np.r_[err.real, err.imag]
            return (evaluate(x) - TARGET).real

        result = least_squares(
            residual, x0, max_nfev=20000,
            gtol=1e-13, ftol=1e-13, xtol=1e-13,
        )
        print(trial, np.linalg.norm(result.fun), np.linalg.norm(result.x),
              result.optimality, result.nfev)
        if np.linalg.norm(result.fun) < 1e-9:
            print("SOLUTION")
            for cell, value in zip(CELLS, result.x[:n]):
                print(cell, repr(value))
            break


if __name__ == "__main__":
    print("cells", len(CELLS), "fibers", len(COLORINGS),
          "terms", sum(map(len, TERMS.values())))
    main()
