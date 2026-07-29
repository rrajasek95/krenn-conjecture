#!/usr/bin/env python3
"""Discovery search for (a q + p s) q^2/2 = Delta_(6,3).

The fixed q is the union of three monochromatic perfect matchings.  This is
the exact shape produced after capping two deleted vertices by a product
covector.  Numerical output is not a certificate.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


N = 6
Q = 3
EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {e: i for i, e in enumerate(EDGES)}
COLORINGS = np.asarray(tuple(itertools.product(range(Q), repeat=N)), dtype=np.int64)
TARGET = np.asarray([float(len(set(c)) == 1) for c in COLORINGS])
PMS = (
    ((0, 1), (2, 3), (4, 5)),
    ((0, 2), (1, 4), (3, 5)),
    ((0, 3), (1, 5), (2, 4)),
)


def perfect_matchings(vertices=tuple(range(N))):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for k, v in enumerate(vertices[1:], 1):
        rest = vertices[1:k] + vertices[k + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


MATCHINGS = tuple(perfect_matchings())
QMAT = np.zeros((len(EDGES), Q, Q))
for color, matching in enumerate(PMS):
    for edge in matching:
        QMAT[EDGE_INDEX[edge], color, color] = 1.0


def polarized_linear_map():
    answer = np.zeros((len(COLORINGS), len(EDGES) * Q * Q))
    rows = np.arange(len(COLORINGS))
    for matching in MATCHINGS:
        for d, edge in enumerate(matching):
            other = [f for k, f in enumerate(matching) if k != d]
            factor = np.ones(len(COLORINGS))
            for f in other:
                factor *= QMAT[
                    EDGE_INDEX[f], COLORINGS[:, f[0]], COLORINGS[:, f[1]]
                ]
            col = (
                EDGE_INDEX[edge] * Q * Q
                + COLORINGS[:, edge[0]] * Q
                + COLORINGS[:, edge[1]]
            )
            np.add.at(answer, (rows, col), factor)
    return answer


LINEAR = polarized_linear_map()


def unpack(x):
    p = x[: N * Q].reshape(N, Q)
    s = x[N * Q : 2 * N * Q].reshape(N, Q)
    a = x[-1]
    return p, s, a


def effective_z(x):
    p, s, a = unpack(x)
    z = a * QMAT.copy()
    for index, (u, v) in enumerate(EDGES):
        z[index] += np.outer(p[u], s[v]) + np.outer(s[u], p[v])
    return z


def run(seed, starts, max_nfev):
    rng = np.random.default_rng(seed)
    for offset in range(starts):
        x0 = rng.normal(scale=0.3, size=2 * N * Q + 1)
        fit = least_squares(
            lambda x: LINEAR @ effective_z(x).reshape(-1) - TARGET,
            x0,
            max_nfev=max_nfev,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
        )
        residual = LINEAR @ effective_z(fit.x).reshape(-1) - TARGET
        print(
            f"seed={seed + offset} cost={fit.cost:.12g} "
            f"max={np.max(np.abs(residual)):.6g} norm={np.linalg.norm(fit.x):.6g} "
            f"nfev={fit.nfev}",
            flush=True,
        )
        if np.max(np.abs(residual)) < 1e-9:
            np.savez(f"candidate_pair_cap_polarized_{seed + offset}.npz", raw=fit.x)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starts", type=int, default=20)
    parser.add_argument("--max-nfev", type=int, default=2000)
    args = parser.parse_args()
    run(args.seed, args.starts, args.max_nfev)


if __name__ == "__main__":
    main()
