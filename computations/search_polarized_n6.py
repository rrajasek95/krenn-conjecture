#!/usr/bin/env python3
"""Numerically test the polarized six-site equation D H_q[z] = Delta_3.

This is a discovery script, not a proof artifact.  It asks whether the
top-degree zeon equation z q^2 / 2 = Delta_(6,3) has a finite real or
complex solution.  A positive result would delimit pair-deletion induction;
a persistent positive residual motivates proving a polarized obstruction.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


N = 6
Q = 3
EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {edge: k for k, edge in enumerate(EDGES)}
COLORINGS = np.asarray(tuple(itertools.product(range(Q), repeat=N)), dtype=np.int64)
TARGET = np.asarray([float(len(set(c)) == 1) for c in COLORINGS])


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
PARAMS_ONE = len(EDGES) * Q * Q


def run(seed: int, starts: int, max_nfev: int, complex_mode: bool) -> None:
    rng = np.random.default_rng(seed)

    def decode(raw):
        if complex_mode:
            half = raw.size // 2
            zc = raw[:half] + 1j * raw[half:]
        else:
            zc = raw
        q, z = np.split(zc, 2)
        return q.reshape(len(EDGES), Q, Q), z.reshape(len(EDGES), Q, Q)

    def value_and_jac(raw, want_jac):
        q, z = decode(raw)
        dtype = np.complex128 if complex_mode else np.float64
        value = np.zeros(len(COLORINGS), dtype=dtype)
        jac_c = np.zeros((len(COLORINGS), 2 * PARAMS_ONE), dtype=dtype) if want_jac else None
        rows = np.arange(len(COLORINGS))
        for matching in MATCHINGS:
            ids = [EDGE_INDEX[e] for e in matching]
            vals_q = [q[i, COLORINGS[:, e[0]], COLORINGS[:, e[1]]] for i, e in zip(ids, matching)]
            vals_z = [z[i, COLORINGS[:, e[0]], COLORINGS[:, e[1]]] for i, e in zip(ids, matching)]
            for distinguished in range(3):
                others = [k for k in range(3) if k != distinguished]
                value += vals_z[distinguished] * vals_q[others[0]] * vals_q[others[1]]
                if not want_jac:
                    continue
                e = matching[distinguished]
                col = PARAMS_ONE + ids[distinguished] * Q * Q + COLORINGS[:, e[0]] * Q + COLORINGS[:, e[1]]
                np.add.at(jac_c, (rows, col), vals_q[others[0]] * vals_q[others[1]])
                for qpos in others:
                    other_q = others[1] if qpos == others[0] else others[0]
                    qe = matching[qpos]
                    qcol = ids[qpos] * Q * Q + COLORINGS[:, qe[0]] * Q + COLORINGS[:, qe[1]]
                    np.add.at(jac_c, (rows, qcol), vals_z[distinguished] * vals_q[other_q])
        if not want_jac:
            residual = value - TARGET
            return np.r_[residual.real, residual.imag] if complex_mode else residual
        if complex_mode:
            jac = np.block([[jac_c.real, -jac_c.imag], [jac_c.imag, jac_c.real]])
        else:
            jac = jac_c
        return jac

    raw_size = 2 * PARAMS_ONE * (2 if complex_mode else 1)
    for offset in range(starts):
        x0 = rng.normal(scale=0.2, size=raw_size)
        fit = least_squares(
            lambda x: value_and_jac(x, False),
            x0,
            jac=lambda x: value_and_jac(x, True),
            max_nfev=max_nfev,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
        )
        residual = value_and_jac(fit.x, False)
        if complex_mode:
            residual = residual[: len(TARGET)] + 1j * residual[len(TARGET) :]
        print(
            f"seed={seed + offset} complex={complex_mode} cost={fit.cost:.12g} "
            f"max={np.max(np.abs(residual)):.6g} norm={np.linalg.norm(fit.x):.6g} "
            f"nfev={fit.nfev}",
            flush=True,
        )
        if np.max(np.abs(residual)) < 1e-9:
            np.savez(
                f"candidate_polarized_n6_{'complex' if complex_mode else 'real'}_{seed + offset}.npz",
                raw=fit.x,
                residual=residual,
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starts", type=int, default=4)
    parser.add_argument("--max-nfev", type=int, default=2000)
    parser.add_argument("--complex", action="store_true")
    args = parser.parse_args()
    run(args.seed, args.starts, args.max_nfev, args.complex)


if __name__ == "__main__":
    main()
