#!/usr/bin/env python3
"""Numerical discovery search for a cyclic full-matrix K_5,5 realization.

There are five 3x3 matrices A_d, where d=j-i mod 5 for a left vertex i
and right vertex j.  The coefficient of a ten-site coloring is the
permanent of the selected 5x5 scalar matrix.  We minimize the exact GHZ_3
coefficient residual with an analytic reverse-mode gradient.  Any output is
only numerical evidence and must be recognized and certified separately.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import minimize


M = 5
Q = 3
PERMS = np.asarray(list(itertools.permutations(range(M))), dtype=np.int8)
COLORS = np.asarray(list(itertools.product(range(Q), repeat=2 * M)), dtype=np.int8)
TARGET = np.asarray([len(set(c)) == 1 for c in COLORS], dtype=float)
ROWS = np.arange(len(COLORS))


def value_gradient(z: np.ndarray, need_gradient: bool = True):
    matrices = z.reshape(M, Q, Q)
    output = np.zeros(len(COLORS), dtype=z.dtype)
    cache = []
    for perm in PERMS:
        values = []
        slots = []
        for i, j in enumerate(perm):
            d = (int(j) - i) % M
            a, b = COLORS[:, i], COLORS[:, M + int(j)]
            values.append(matrices[d, a, b])
            slots.append(d * Q * Q + a * Q + b)
        product_value = np.prod(values, axis=0)
        output += product_value
        if need_gradient:
            cache.append((values, slots))
    residual = output - TARGET
    loss = 0.5 * float(np.vdot(residual, residual).real)
    if not need_gradient:
        return loss, output
    gradient = np.zeros(z.size, dtype=z.dtype)
    for values, slots in cache:
        for k in range(M):
            derivative = np.ones(len(COLORS), dtype=z.dtype)
            for ell in range(M):
                if ell != k:
                    derivative *= values[ell]
            contribution = np.conjugate(residual) * derivative
            np.add.at(gradient, slots[k], contribution)
    return loss, output, gradient


def run(seed: int, complex_search: bool, maxiter: int, color_circulant: bool):
    rng = np.random.default_rng(seed)
    full_count = M * Q * Q
    count = M * Q if color_circulant else full_count

    def expand(z):
        if not color_circulant:
            return z
        small = z.reshape(M, Q)
        return np.asarray([
            small[d, (b - a) % Q]
            for d in range(M) for a in range(Q) for b in range(Q)
        ])

    def collapse(g):
        if not color_circulant:
            return g
        answer = np.zeros(count, dtype=g.dtype)
        for d in range(M):
            for a in range(Q):
                for b in range(Q):
                    answer[d * Q + (b - a) % Q] += g[d * Q * Q + a * Q + b]
        return answer
    if complex_search:
        x0 = rng.normal(scale=0.4, size=2 * count)

        def decode(x):
            return x[:count] + 1j * x[count:]

        def objective(x):
            loss, _out, g = value_gradient(expand(decode(x)))
            g = collapse(g)
            return loss, np.r_[g.real, -g.imag]
    else:
        x0 = rng.normal(scale=0.4, size=count)
        decode = lambda x: x

        def objective(x):
            loss, _out, g = value_gradient(expand(x))
            return loss, collapse(g).real

    result = minimize(
        objective,
        x0,
        method="L-BFGS-B",
        jac=True,
        options={"maxiter": maxiter, "ftol": 1e-15, "gtol": 1e-10,
                 "maxls": 40},
    )
    z = expand(decode(result.x))
    loss, output = value_gradient(z, False)
    residual = output - TARGET
    print(
        f"seed={seed} success={result.success} nit={result.nit} "
        f"loss={loss:.12g} max={np.max(np.abs(residual)):.6g} "
        f"norm={np.linalg.norm(z):.6g}",
        flush=True,
    )
    if np.max(np.abs(residual)) < 1e-5:
        np.savez(
            f"candidate_k55_cyclic_seed{seed}.npz",
            matrices=z.reshape(M, Q, Q), residual=residual,
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starts", type=int, default=1)
    parser.add_argument("--maxiter", type=int, default=1000)
    parser.add_argument("--complex", action="store_true", dest="complex_search")
    parser.add_argument("--color-circulant", action="store_true")
    args = parser.parse_args()
    for seed in range(args.seed, args.seed + args.starts):
        run(seed, args.complex_search, args.maxiter, args.color_circulant)


if __name__ == "__main__":
    main()
