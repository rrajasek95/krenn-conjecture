#!/usr/bin/env python3
"""Track least-squares continuation away from the projected n=8 border source.

This is a numerical discovery script, not an exact certificate.  It starts
from the first Laurent family audited by ``verify_sparse_n8_border_attractors``
after applying the binary projection

    0 -> (1, 0),  1 -> (0, 1),  2 -> (1, 1).

The checkpoints expose whether a small residual is attained at bounded norm
or merely accompanies an escape to infinity.
"""

from __future__ import annotations

import argparse
import itertools
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares


N = 8
Q = 2
EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
COLORINGS = np.asarray(tuple(itertools.product(range(Q), repeat=N)), dtype=np.int8)
TARGET = np.ones(len(COLORINGS))
TARGET[0] = 2
TARGET[-1] = 2
COLOR_MATCHINGS = (
    ((0, 2), (1, 4), (3, 6), (5, 7)),
    ((0, 3), (1, 5), (2, 4), (6, 7)),
    ((0, 1), (2, 3), (4, 7), (5, 6)),
)
POSITIVE_EDGE = (3, 6)
NEGATIVE_EDGE = (1, 4)
PROJECTED_VECTORS = (
    np.asarray((1.0, 0.0)),
    np.asarray((0.0, 1.0)),
    np.asarray((1.0, 1.0)),
)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


MATCHINGS = tuple(perfect_matchings(tuple(range(N))))


def amplitudes(z: np.ndarray) -> np.ndarray:
    matrices = z.reshape(len(EDGES), Q, Q)
    result = np.zeros(len(COLORINGS), dtype=z.dtype)
    for matching in MATCHINGS:
        term = np.ones(len(COLORINGS), dtype=z.dtype)
        for u, v in matching:
            term *= matrices[EDGE_INDEX[u, v], COLORINGS[:, u], COLORINGS[:, v]]
        result += term
    return result


def jacobian(z: np.ndarray) -> np.ndarray:
    matrices = z.reshape(len(EDGES), Q, Q)
    answer = np.zeros((len(COLORINGS), len(z)), dtype=z.dtype)
    rows = np.arange(len(COLORINGS))
    for matching in MATCHINGS:
        values = [
            matrices[EDGE_INDEX[edge], COLORINGS[:, edge[0]], COLORINGS[:, edge[1]]]
            for edge in matching
        ]
        for position, edge in enumerate(matching):
            derivative = np.ones(len(COLORINGS), dtype=z.dtype)
            for other, value in enumerate(values):
                if other != position:
                    derivative *= value
            local = Q * COLORINGS[:, edge[0]] + COLORINGS[:, edge[1]]
            columns = Q * Q * EDGE_INDEX[edge] + local
            np.add.at(answer, (rows, columns), derivative)
    return answer


def border_source(t: float) -> np.ndarray:
    matrices = np.zeros((len(EDGES), Q, Q))
    for color, matching in enumerate(COLOR_MATCHINGS):
        vector = PROJECTED_VECTORS[color]
        for edge in matching:
            weight = 1.0
            if edge == POSITIVE_EDGE:
                weight = t
            elif edge == NEGATIVE_EDGE:
                weight = 1.0 / t
            matrices[EDGE_INDEX[edge]] = weight * np.outer(vector, vector)
    return matrices.ravel()


def diagnostics(z: np.ndarray) -> tuple[float, float, int, float, float]:
    residual = amplitudes(z) - TARGET
    singular_values = np.linalg.svd(jacobian(z), compute_uv=False)
    rank = int(np.count_nonzero(singular_values > 1e-8))
    return (
        float(np.max(np.abs(residual))),
        float(np.linalg.norm(z)),
        rank,
        float(singular_values[rank - 1]),
        float(singular_values[rank]) if rank < len(singular_values) else 0.0,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--t", type=float, default=1.0)
    parser.add_argument("--chunk", type=int, default=250)
    parser.add_argument("--chunks", type=int, default=16)
    parser.add_argument("--load", type=Path)
    parser.add_argument("--save", type=Path)
    args = parser.parse_args()

    if args.load is None:
        z = border_source(args.t)
    else:
        z = np.load(args.load)["matrices"].ravel()
    print("step nfev maxerr norm rank sigma_last sigma_next optimality", flush=True)
    error, norm, rank, sigma_last, sigma_next = diagnostics(z)
    print(0, 0, error, norm, rank, sigma_last, sigma_next, "-", flush=True)
    total_nfev = 0
    for step in range(1, args.chunks + 1):
        fit = least_squares(
            lambda x: amplitudes(x) - TARGET,
            z,
            jac=jacobian,
            max_nfev=args.chunk,
            ftol=1e-15,
            xtol=1e-15,
            gtol=1e-15,
        )
        z = fit.x
        total_nfev += fit.nfev
        error, norm, rank, sigma_last, sigma_next = diagnostics(z)
        print(
            step,
            total_nfev,
            error,
            norm,
            rank,
            sigma_last,
            sigma_next,
            fit.optimality,
            flush=True,
        )
    if args.save is not None:
        np.savez(args.save, matrices=z.reshape(len(EDGES), Q, Q), residual=amplitudes(z) - TARGET)


if __name__ == "__main__":
    main()
