#!/usr/bin/env python3
"""Numerical search for a translation-invariant full-matrix n=8 source.

Vertices are Z/8.  A directed difference d=1,2,3 has an arbitrary 3x3
matrix C_d, difference -d uses its transpose, and the antipodal matrix C_4
is symmetric.  This is only a discovery search; any candidate needs exact
recognition and independent coefficient verification.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import minimize


N, Q = 8, 3
EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {e: i for i, e in enumerate(EDGES)}
COLORS = np.asarray(list(itertools.product(range(Q), repeat=N)), dtype=np.int8)
TARGET = np.asarray([len(set(c)) == 1 for c in COLORS], dtype=float)


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for k in range(1, len(vertices)):
        v = vertices[k]
        rest = vertices[1:k] + vertices[k + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


MATCHINGS = tuple(perfect_matchings(tuple(range(N))))
SYMMETRIC = tuple((a, b) for a in range(Q) for b in range(a, Q))
PARAMETERS = 3 * Q * Q + len(SYMMETRIC)


def expand_color_circulant(z):
    """Expand 3 circulant matrices and one symmetric circulant matrix."""
    answer = np.zeros(PARAMETERS, dtype=z.dtype)
    for d in range(3):
        for a in range(Q):
            for b in range(Q):
                answer[d * Q * Q + a * Q + b] = z[d * Q + (b - a) % Q]
    diagonal, off_diagonal = z[9], z[10]
    for k, (a, b) in enumerate(SYMMETRIC):
        answer[3 * Q * Q + k] = diagonal if a == b else off_diagonal
    return answer


def collapse_color_circulant(g):
    answer = np.zeros(11, dtype=g.dtype)
    for d in range(3):
        block = g[d * Q * Q:(d + 1) * Q * Q].reshape(Q, Q)
        for a in range(Q):
            for b in range(Q):
                answer[d * Q + (b - a) % Q] += block[a, b]
    for value, (a, b) in zip(g[3 * Q * Q:], SYMMETRIC):
        answer[9 if a == b else 10] += value
    return answer


def expand(z):
    c = [z[d * Q * Q:(d + 1) * Q * Q].reshape(Q, Q) for d in range(3)]
    c4 = np.zeros((Q, Q), dtype=z.dtype)
    for value, (a, b) in zip(z[3 * Q * Q:], SYMMETRIC):
        c4[a, b] = c4[b, a] = value
    matrices = []
    for u, v in EDGES:
        d = (v - u) % N
        if d <= 3:
            matrices.append(c[d - 1])
        elif d == 4:
            matrices.append(c4)
        else:
            matrices.append(c[N - d - 1].T)
    return np.asarray(matrices)


def collapse(g):
    answer = np.zeros(PARAMETERS, dtype=g.dtype)
    for edge_number, (u, v) in enumerate(EDGES):
        d = (v - u) % N
        block = g[edge_number]
        if d <= 3:
            answer[(d - 1) * Q * Q:d * Q * Q] += block.reshape(-1)
        elif d == 4:
            for k, (a, b) in enumerate(SYMMETRIC):
                answer[3 * Q * Q + k] += block[a, b]
                if a != b:
                    answer[3 * Q * Q + k] += block[b, a]
        else:
            dd = N - d
            answer[(dd - 1) * Q * Q:dd * Q * Q] += block.T.reshape(-1)
    return answer


def value_gradient(z, need_gradient=True):
    matrices = expand(z)
    output = np.zeros(len(COLORS), dtype=z.dtype)
    cache = []
    for matching in MATCHINGS:
        values, slots = [], []
        for u, v in matching:
            edge_number = EDGE_INDEX[u, v]
            a, b = COLORS[:, u], COLORS[:, v]
            values.append(matrices[edge_number, a, b])
            slots.append((edge_number, a, b))
        output += np.prod(values, axis=0)
        if need_gradient:
            cache.append((values, slots))
    residual = output - TARGET
    loss = 0.5 * float(np.vdot(residual, residual).real)
    if not need_gradient:
        return loss, output
    full_gradient = np.zeros_like(matrices)
    for values, slots in cache:
        for k, (edge_number, aa, bb) in enumerate(slots):
            derivative = np.ones(len(COLORS), dtype=z.dtype)
            for ell, value in enumerate(values):
                if ell != k:
                    derivative *= value
            np.add.at(full_gradient[edge_number], (aa, bb),
                      np.conjugate(residual) * derivative)
    return loss, output, collapse(full_gradient)


def run(seed, complex_search, maxiter, color_circulant):
    rng = np.random.default_rng(seed)
    count = 11 if color_circulant else PARAMETERS
    to_base = expand_color_circulant if color_circulant else (lambda z: z)
    from_base = collapse_color_circulant if color_circulant else (lambda z: z)
    if complex_search:
        x0 = rng.normal(scale=0.45, size=2 * count)

        def decode(x):
            return x[:count] + 1j * x[count:]

        def objective(x):
            loss, _output, g = value_gradient(to_base(decode(x)))
            g = from_base(g)
            return loss, np.r_[g.real, -g.imag]
    else:
        x0 = rng.normal(scale=0.45, size=count)
        decode = lambda x: x

        def objective(x):
            loss, _output, g = value_gradient(to_base(x))
            return loss, from_base(g).real
    result = minimize(objective, x0, method="L-BFGS-B", jac=True,
                      options={"maxiter": maxiter, "ftol": 1e-15,
                               "gtol": 1e-11, "maxls": 50})
    z = to_base(decode(result.x))
    loss, output = value_gradient(z, False)
    residual = output - TARGET
    print(f"seed={seed} nit={result.nit} loss={loss:.12g} "
          f"max={np.max(np.abs(residual)):.6g} norm={np.linalg.norm(z):.6g}",
          flush=True)
    if np.max(np.abs(residual)) < 1e-6:
        np.savez(f"candidate_cyclic_n8_seed{seed}.npz", parameters=z,
                 matrices=expand(z), residual=residual)


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
