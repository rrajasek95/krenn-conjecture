#!/usr/bin/env python3
"""Numerical discovery for the constrained polarized six-site equation.

The constraint is

    z = a q + 3 p s,

where (ps)_ij = p_i s_j^T + s_i p_j^T in the site-square-zero
algebra.  We ask whether z q^2 / 2 is Delta_(6,3).  This file is only a
discovery tool; any positive output still needs exact reconstruction.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


N = 6
C = 3
EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {e: k for k, e in enumerate(EDGES)}
COLORINGS = np.asarray(tuple(itertools.product(range(C), repeat=N)), dtype=np.int64)
TARGET = np.asarray([float(len(set(c)) == 1) for c in COLORINGS])
ROWS = np.arange(len(COLORINGS))
NQ = len(EDGES) * C * C
NP = N * C


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


def decode(raw):
    q = raw[:NQ].reshape(len(EDGES), C, C)
    p = raw[NQ : NQ + NP].reshape(N, C)
    s = raw[NQ + NP : NQ + 2 * NP].reshape(N, C)
    a = raw[-1]
    return q, p, s, a


def value_and_jac(raw, want_jac):
    q, p, s, a = decode(raw)
    value = np.zeros(len(COLORINGS))
    jac = np.zeros((len(COLORINGS), raw.size)) if want_jac else None

    for matching in MATCHINGS:
        ids = [EDGE_INDEX[e] for e in matching]
        qvals = [q[i, COLORINGS[:, u], COLORINGS[:, v]] for i, (u, v) in zip(ids, matching)]
        psvals = [
            p[u, COLORINGS[:, u]] * s[v, COLORINGS[:, v]]
            + s[u, COLORINGS[:, u]] * p[v, COLORINGS[:, v]]
            for u, v in matching
        ]
        zvals = [a * qv + 3.0 * pv for qv, pv in zip(qvals, psvals)]

        for distinguished in range(3):
            others = [k for k in range(3) if k != distinguished]
            qprod = qvals[others[0]] * qvals[others[1]]
            value += zvals[distinguished] * qprod
            if not want_jac:
                continue

            # q occurring through z = a q + 3ps.
            u, v = matching[distinguished]
            qcol = ids[distinguished] * C * C + COLORINGS[:, u] * C + COLORINGS[:, v]
            np.add.at(jac, (ROWS, qcol), a * qprod)

            # The two ordinary q factors.
            for pos, other in ((others[0], others[1]), (others[1], others[0])):
                u, v = matching[pos]
                qcol = ids[pos] * C * C + COLORINGS[:, u] * C + COLORINGS[:, v]
                np.add.at(jac, (ROWS, qcol), zvals[distinguished] * qvals[other])

            # p and s occurring through the distinguished ps edge.
            u, v = matching[distinguished]
            cu = COLORINGS[:, u]
            cv = COLORINGS[:, v]
            np.add.at(jac, (ROWS, NQ + u * C + cu), 3.0 * s[v, cv] * qprod)
            np.add.at(jac, (ROWS, NQ + v * C + cv), 3.0 * s[u, cu] * qprod)
            np.add.at(jac, (ROWS, NQ + NP + u * C + cu), 3.0 * p[v, cv] * qprod)
            np.add.at(jac, (ROWS, NQ + NP + v * C + cv), 3.0 * p[u, cu] * qprod)
            jac[:, -1] += qvals[distinguished] * qprod

    return jac if want_jac else value - TARGET


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--max-nfev", type=int, default=5000)
    parser.add_argument("--scale", type=float, default=0.3)
    parser.add_argument("--save-threshold", type=float, default=1e-9)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)

    for start in range(args.starts):
        x0 = rng.normal(scale=args.scale, size=NQ + 2 * NP + 1)
        fit = least_squares(
            lambda x: value_and_jac(x, False),
            x0,
            jac=lambda x: value_and_jac(x, True),
            max_nfev=args.max_nfev,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
        )
        residual = value_and_jac(fit.x, False)
        print(
            f"start={start} seed={args.seed} cost={fit.cost:.12g} "
            f"max={np.max(np.abs(residual)):.6g} norm={np.linalg.norm(fit.x):.6g} "
            f"nfev={fit.nfev}",
            flush=True,
        )
        if np.max(np.abs(residual)) < args.save_threshold:
            np.savez(f"candidate_polarized_paircap_{args.seed}_{start}.npz", raw=fit.x, residual=residual)


if __name__ == "__main__":
    main()
