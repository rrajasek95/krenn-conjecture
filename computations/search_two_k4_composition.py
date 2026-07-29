#!/usr/bin/env python3
"""Numerical discovery search for two K4 equality gadgets with cross blocks.

The twelve internal K4 cells are fixed at unit weight.  All sixteen cross
pairs carry arbitrary 3x3 aggregate matrices.  This is only a candidate
generator; any near-zero point must subsequently be recognized and checked
exactly.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


N = 8
Q = 3
LEFT = range(4)
RIGHT = range(4, 8)
CROSS = tuple((u, v) for u in LEFT for v in RIGHT)
INDEX = {edge: k for k, edge in enumerate(CROSS)}
COLORINGS = np.asarray(list(itertools.product(range(Q), repeat=N)), dtype=np.int8)
TARGET = np.asarray([len(set(c)) == 1 for c in COLORINGS], dtype=float)
ROWS = np.arange(len(COLORINGS))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for k in range(1, len(vertices)):
        v = vertices[k]
        rest = vertices[1:k] + vertices[k + 1 :]
        for matching in perfect_matchings(rest):
            yield ((u, v),) + matching


MATCHINGS = tuple(perfect_matchings(tuple(range(N))))


def internal_colour(u: int, v: int) -> int:
    if u >= 4:
        u, v = u - 4, v - 4
    return (1, 2, 3).index(u ^ v)


def run(seed: int, max_nfev: int, complex_search: bool) -> None:
    parameter_count = len(CROSS) * Q * Q

    def unpack(z):
        return z.reshape(len(CROSS), Q, Q)

    def edge_values(matrices, edge):
        u, v = edge
        if u < 4 <= v:
            return matrices[INDEX[edge], COLORINGS[:, u], COLORINGS[:, v]]
        colour = internal_colour(u, v)
        return ((COLORINGS[:, u] == colour) & (COLORINGS[:, v] == colour)).astype(matrices.dtype)

    def amplitudes(z):
        matrices = unpack(z)
        answer = np.zeros(len(COLORINGS), dtype=z.dtype)
        for matching in MATCHINGS:
            term = np.ones(len(COLORINGS), dtype=z.dtype)
            for edge in matching:
                term *= edge_values(matrices, edge)
            answer += term
        return answer

    def derivative(z):
        matrices = unpack(z)
        jac = np.zeros((len(COLORINGS), parameter_count), dtype=z.dtype)
        for matching in MATCHINGS:
            values = [edge_values(matrices, edge) for edge in matching]
            for position, edge in enumerate(matching):
                if not (edge[0] < 4 <= edge[1]):
                    continue
                product_value = np.ones(len(COLORINGS), dtype=z.dtype)
                for other, value in enumerate(values):
                    if other != position:
                        product_value *= value
                local = COLORINGS[:, edge[0]].astype(np.int32) * Q + COLORINGS[:, edge[1]].astype(np.int32)
                columns = INDEX[edge] * Q * Q + local
                np.add.at(jac, (ROWS, columns), product_value)
        return jac

    rng = np.random.default_rng(seed)
    if complex_search:
        initial = rng.normal(scale=0.35, size=2 * parameter_count)

        def decode(x):
            return x[:parameter_count] + 1j * x[parameter_count:]

        def residual(x):
            value = amplitudes(decode(x)) - TARGET
            return np.r_[value.real, value.imag]

        def jacobian(x):
            value = derivative(decode(x))
            return np.block([[value.real, -value.imag], [value.imag, value.real]])
    else:
        initial = rng.normal(scale=0.35, size=parameter_count)
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
    matrices = unpack(decode(fit.x))
    raw = amplitudes(decode(fit.x)) - TARGET
    maximum = np.max(np.abs(raw))
    print(
        f"seed={seed} cost={fit.cost:.10g} max={maximum:.5g} "
        f"norm={np.linalg.norm(fit.x):.5g} nfev={fit.nfev}",
        flush=True,
    )
    if maximum < 1e-7 and np.linalg.norm(fit.x) < 1e5:
        np.savez(
            f"candidate_two_k4_seed{seed}.npz",
            cross=np.asarray(CROSS),
            matrices=matrices,
            residual=raw,
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starts", type=int, default=1)
    parser.add_argument("--max-nfev", type=int, default=1000)
    parser.add_argument("--complex", action="store_true", dest="complex_search")
    args = parser.parse_args()
    for seed in range(args.seed, args.seed + args.starts):
        run(seed, args.max_nfev, args.complex_search)


if __name__ == "__main__":
    main()
