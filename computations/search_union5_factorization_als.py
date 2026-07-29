#!/usr/bin/env python3
"""Exploratory ALS search for Delta_5 = X Y D Q in the square-free algebra.

This is deliberately a discovery script, not an exact certificate.  It can
either optimize all three five-site linear factors or hold the first two
fixed at the row-011166 witness used in the union-five audit.
"""

from __future__ import annotations

import argparse
from itertools import combinations, permutations

import numpy as np


SITES = tuple(range(5))
COLORS = tuple(range(3))
PAIRS = tuple(combinations(SITES, 2))
TARGET = np.zeros((3,) * 5)
for color in COLORS:
    TARGET[(color,) * 5] = 1


def response(x, y, d, edge):
    answer = np.zeros_like(TARGET)
    for pair_index, (a, b) in enumerate(PAIRS):
        complement = tuple(site for site in SITES if site not in (a, b))
        for u, v, w in permutations(complement):
            raw = np.einsum(
                "ij,k,l,m->ijklm", edge[pair_index], x[u], y[v], d[w]
            )
            raw_axes = (a, b, u, v, w)
            answer += raw.transpose(
                tuple(raw_axes.index(site) for site in SITES)
            )
    return answer


def design(block, x, y, d, edge):
    arrays = {"x": x, "y": y, "d": d, "edge": edge}
    shape = arrays[block].shape
    matrix = np.zeros((TARGET.size, int(np.prod(shape))))
    original = arrays[block]
    for column in range(matrix.shape[1]):
        basis = np.zeros(shape)
        basis.ravel()[column] = 1
        arrays[block] = basis
        matrix[:, column] = response(
            arrays["x"], arrays["y"], arrays["d"], arrays["edge"]
        ).ravel()
    arrays[block] = original
    return matrix


FIXED_011166 = np.asarray(
    (
        ((-1, 0, 0), (-1, -1, 1)),
        ((-1, -1, 1), (-1, 0, 0)),
        ((-1, 0, 0), (-1, 1, -1)),
        ((0, 1, 0), (0, 0, -1)),
        ((0, 0, -1), (0, 1, 0)),
    ),
    dtype=float,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=10)
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--fixed-011166", action="store_true")
    parser.add_argument("--seed", type=int, default=20260724)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)

    best = None
    for trial in range(args.trials):
        if args.fixed_011166:
            x, y = FIXED_011166[:, 0].copy(), FIXED_011166[:, 1].copy()
        else:
            x, y = rng.normal(size=(5, 3)), rng.normal(size=(5, 3))
        d = rng.normal(size=(5, 3))
        edge = rng.normal(size=(10, 3, 3))
        blocks = ("edge", "d") if args.fixed_011166 else (
            "edge", "x", "y", "d"
        )
        for iteration in range(args.iterations):
            for block in blocks:
                matrix = design(block, x, y, d, edge)
                solution = np.linalg.lstsq(
                    matrix, TARGET.ravel(), rcond=1e-12
                )[0]
                if block == "edge":
                    edge = solution.reshape(edge.shape)
                elif block == "x":
                    x = solution.reshape(x.shape)
                elif block == "y":
                    y = solution.reshape(y.shape)
                else:
                    d = solution.reshape(d.shape)
            error = np.linalg.norm(response(x, y, d, edge) - TARGET)
            if error < 1e-11:
                break
        record = (error, trial, iteration, x, y, d, edge)
        if best is None or error < best[0]:
            best = record
        print("trial", trial, "iterations", iteration + 1, "residual", error,
              flush=True)

    error, trial, iteration, x, y, d, edge = best
    print("best residual", error, "trial", trial, "iteration", iteration)
    if error < 1e-8:
        np.set_printoptions(precision=12, suppress=True)
        print("x=", x)
        print("y=", y)
        print("d=", d)
        print("edge=", edge)


if __name__ == "__main__":
    main()
