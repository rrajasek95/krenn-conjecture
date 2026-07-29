#!/usr/bin/env python3
"""Numerical search on sparse n=8 supports near the prism border expansion.

This is only a counterexample-discovery tool.  The base support is the
3-regular vertex-to-triangle expansion of the six-vertex prism.  A chosen
perfect matching from its complement raises every degree to four, escaping
cubic-vertex rigidity while retaining only 14--16 perfect matchings.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


N = 8
Q = 3
BASE = {
    (0, 1), (0, 3), (0, 7),
    (1, 4), (1, 6),
    (2, 3), (2, 4), (2, 5),
    (3, 4),
    (5, 6), (5, 7),
    (6, 7),
}
EXTRAS = (
    ((0, 2), (1, 5), (3, 6), (4, 7)),
    ((0, 2), (1, 5), (3, 7), (4, 6)),
    ((0, 2), (1, 7), (3, 5), (4, 6)),
    ((0, 4), (1, 5), (2, 6), (3, 7)),
    ((0, 4), (1, 5), (2, 7), (3, 6)),
    ((0, 5), (1, 2), (3, 6), (4, 7)),
    ((0, 5), (1, 3), (2, 6), (4, 7)),
)
COLORINGS = np.asarray(list(itertools.product(range(Q), repeat=N)), dtype=np.int8)
TARGET = np.asarray([len(set(c)) == 1 for c in COLORINGS], dtype=float)


def perfect_matchings(vertices, edges):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for j in range(1, len(vertices)):
        v = vertices[j]
        edge = (u, v)
        if edge not in edges:
            continue
        rest = vertices[1:j] + vertices[j + 1 :]
        for tail in perfect_matchings(rest, edges):
            yield (edge,) + tail


def run(extra_index, seed, max_nfev, complex_search):
    edges = tuple(sorted(BASE | set(EXTRAS[extra_index])))
    edge_index = {edge: k for k, edge in enumerate(edges)}
    matchings = tuple(perfect_matchings(tuple(range(N)), set(edges)))
    parameter_count = len(edges) * Q * Q

    def unpack(z):
        return z.reshape(len(edges), Q, Q)

    def amplitudes(z):
        matrices = unpack(z)
        answer = np.zeros(len(COLORINGS), dtype=z.dtype)
        for matching in matchings:
            term = np.ones(len(COLORINGS), dtype=z.dtype)
            for u, v in matching:
                term *= matrices[
                    edge_index[u, v], COLORINGS[:, u], COLORINGS[:, v]
                ]
            answer += term
        return answer

    def derivative(z):
        matrices = unpack(z)
        jac = np.zeros((len(COLORINGS), parameter_count), dtype=z.dtype)
        rows = np.arange(len(COLORINGS))
        for matching in matchings:
            values = [
                matrices[edge_index[e], COLORINGS[:, e[0]], COLORINGS[:, e[1]]]
                for e in matching
            ]
            for position, edge in enumerate(matching):
                product = np.ones(len(COLORINGS), dtype=z.dtype)
                for other, value in enumerate(values):
                    if other != position:
                        product *= value
                local = (
                    COLORINGS[:, edge[0]].astype(np.int32) * Q
                    + COLORINGS[:, edge[1]].astype(np.int32)
                )
                columns = edge_index[edge] * Q * Q + local
                np.add.at(jac, (rows, columns), product)
        return jac

    rng = np.random.default_rng(seed)
    if complex_search:
        initial = rng.normal(scale=0.3, size=2 * parameter_count)

        def decode(x):
            return x[:parameter_count] + 1j * x[parameter_count:]

        def residual(x):
            value = amplitudes(decode(x)) - TARGET
            return np.r_[value.real, value.imag]

        def jacobian(x):
            value = derivative(decode(x))
            return np.block([[value.real, -value.imag], [value.imag, value.real]])
    else:
        initial = rng.normal(scale=0.3, size=parameter_count)
        decode = lambda x: x
        residual = lambda x: amplitudes(x) - TARGET
        jacobian = derivative

    fit = least_squares(
        residual,
        initial,
        jac=jacobian,
        max_nfev=max_nfev,
        ftol=1e-13,
        xtol=1e-13,
        gtol=1e-13,
        verbose=0,
    )
    raw = amplitudes(decode(fit.x)) - TARGET
    print(
        f"extra={extra_index} pm={len(matchings)} seed={seed} "
        f"cost={fit.cost:.9g} max={np.max(np.abs(raw)):.4g} "
        f"norm={np.linalg.norm(fit.x):.4g} nfev={fit.nfev}",
        flush=True,
    )
    if np.max(np.abs(raw)) < 1e-7 and np.linalg.norm(fit.x) < 1e5:
        np.savez(
            f"candidate_sparse_n8_extra{extra_index}_seed{seed}.npz",
            edges=np.asarray(edges),
            matrices=unpack(decode(fit.x)),
            residual=raw,
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--extra", type=int, default=0, choices=range(len(EXTRAS)))
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starts", type=int, default=1)
    parser.add_argument("--max-nfev", type=int, default=2000)
    parser.add_argument("--complex", action="store_true", dest="complex_search")
    args = parser.parse_args()
    for seed in range(args.seed, args.seed + args.starts):
        run(args.extra, seed, args.max_nfev, args.complex_search)


if __name__ == "__main__":
    main()
