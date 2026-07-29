#!/usr/bin/env python3
"""Numerically test a binary projection of ternary GHZ against H_n.

This is only a discovery/falsification script.  The target is

    e_0^n + e_1^n + (e_0+e_1)^n,

obtained from the fixed local projection of the three ternary basis vectors.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20260724)
    parser.add_argument("--max-nfev", type=int, default=10000)
    parser.add_argument("--real", action="store_true")
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()

    n = args.n
    q = 2
    edges = tuple(itertools.combinations(range(n), 2))
    edge_index = {edge: index for index, edge in enumerate(edges)}
    matchings = tuple(perfect_matchings(tuple(range(n))))
    colorings = np.asarray(tuple(itertools.product(range(q), repeat=n)), dtype=np.int8)
    target = np.ones(len(colorings), dtype=float)
    target[np.all(colorings == 0, axis=1)] += 1
    target[np.all(colorings == 1, axis=1)] += 1
    parameters = 4 * len(edges)

    def amplitudes(z: np.ndarray) -> np.ndarray:
        matrices = z.reshape(len(edges), q, q)
        result = np.zeros(len(colorings), dtype=z.dtype)
        for matching in matchings:
            term = np.ones(len(colorings), dtype=z.dtype)
            for u, v in matching:
                term *= matrices[edge_index[(u, v)], colorings[:, u], colorings[:, v]]
            result += term
        return result

    def complex_jacobian(z: np.ndarray) -> np.ndarray:
        matrices = z.reshape(len(edges), q, q)
        jac = np.zeros((len(colorings), parameters), dtype=z.dtype)
        rows = np.arange(len(colorings))
        for matching in matchings:
            values = [
                matrices[edge_index[e], colorings[:, e[0]], colorings[:, e[1]]]
                for e in matching
            ]
            for position, edge in enumerate(matching):
                derivative = np.ones(len(colorings), dtype=z.dtype)
                for other, value in enumerate(values):
                    if other != position:
                        derivative *= value
                local = 2 * colorings[:, edge[0]] + colorings[:, edge[1]]
                columns = 4 * edge_index[edge] + local
                np.add.at(jac, (rows, columns), derivative)
        return jac

    rng = np.random.default_rng(args.seed)
    dimension = parameters if args.real else 2 * parameters

    def decode(x: np.ndarray) -> np.ndarray:
        if args.real:
            return x.astype(complex)
        return x[:parameters] + 1j * x[parameters:]

    def residual(x: np.ndarray) -> np.ndarray:
        value = amplitudes(decode(x)) - target
        return np.r_[value.real, value.imag]

    def jacobian(x: np.ndarray) -> np.ndarray:
        value = complex_jacobian(decode(x))
        if args.real:
            return np.vstack((value.real, value.imag))
        return np.block([[value.real, -value.imag], [value.imag, value.real]])

    for start in range(args.starts):
        x0 = rng.normal(scale=0.35, size=dimension)
        fit = least_squares(
            residual,
            x0,
            jac=jacobian,
            max_nfev=args.max_nfev,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
        )
        error = amplitudes(decode(fit.x)) - target
        print(
            start,
            "cost", fit.cost,
            "max", float(np.max(np.abs(error))),
            "norm", float(np.linalg.norm(fit.x)),
            "rankJ", int(np.linalg.matrix_rank(jacobian(fit.x), tol=1e-8)),
            flush=True,
        )
        if args.save and np.max(np.abs(error)) < 1e-8:
            np.savez(
                f"/tmp/binary_rank3_projection_n{n}_start{start}.npz",
                matrices=decode(fit.x).reshape(len(edges), 2, 2),
                residual=error,
            )


if __name__ == "__main__":
    main()
