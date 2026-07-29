#!/usr/bin/env python3
"""Search a strict C3-equivariant n=8 source for the canonical binary target.

The color action is ``h = [[0,1],[-1,1]]`` and the vertex action is
``(0 2 4)(1 3 5)(6)(7)``.  This is a numerical discovery script.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


N = 8
Q = 2
H = np.asarray(((0.0, 1.0), (-1.0, 1.0)))
RHO = (2, 3, 4, 5, 0, 1, 6, 7)
EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
COLORINGS = np.asarray(tuple(itertools.product(range(Q), repeat=N)), dtype=np.int8)
TARGET = np.ones(len(COLORINGS), dtype=complex)
TARGET[0] = 2
TARGET[-1] = 2


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


def rotate_edge(edge: tuple[int, int]) -> tuple[tuple[int, int], bool]:
    u, v = RHO[edge[0]], RHO[edge[1]]
    return ((u, v), False) if u < v else ((v, u), True)


def edge_orbits() -> tuple[tuple[tuple[tuple[int, int], bool], ...], ...]:
    unseen = set(EDGES)
    answer = []
    while unseen:
        seed = min(unseen)
        orbit = []
        edge = seed
        transposed = False
        while edge not in {item[0] for item in orbit}:
            orbit.append((edge, transposed))
            unseen.remove(edge)
            edge, flipped = rotate_edge(edge)
            transposed ^= flipped
        answer.append(tuple(orbit))
    return tuple(answer)


ORBITS = edge_orbits()
FIXED_BASIS = (
    np.asarray(((1.0, 1.0), (0.0, 1.0))),
    np.asarray(((0.0, -1.0), (1.0, 0.0))),
)
PARAMETERS = sum(2 if len(orbit) == 1 else 4 for orbit in ORBITS)


def expand(parameters: np.ndarray) -> np.ndarray:
    matrices = np.zeros((len(EDGES), Q, Q), dtype=parameters.dtype)
    cursor = 0
    for orbit in ORBITS:
        if len(orbit) == 1:
            seed = parameters[cursor] * FIXED_BASIS[0] + parameters[cursor + 1] * FIXED_BASIS[1]
            cursor += 2
        else:
            seed = parameters[cursor : cursor + 4].reshape(Q, Q)
            cursor += 4
        matrix = seed
        edge = orbit[0][0]
        for _ in range(len(orbit)):
            matrices[EDGE_INDEX[edge]] = matrix
            rotated, flipped = rotate_edge(edge)
            matrix = H @ matrix @ H.T
            if flipped:
                matrix = matrix.T
            edge = rotated
    assert cursor == PARAMETERS
    return matrices


def expansion_matrix() -> np.ndarray:
    answer = np.zeros((4 * len(EDGES), PARAMETERS))
    for column in range(PARAMETERS):
        unit = np.zeros(PARAMETERS)
        unit[column] = 1
        answer[:, column] = expand(unit).ravel()
    return answer


EXPANSION = expansion_matrix()


def amplitudes(parameters: np.ndarray) -> np.ndarray:
    matrices = expand(parameters)
    result = np.zeros(len(COLORINGS), dtype=parameters.dtype)
    for matching in MATCHINGS:
        term = np.ones(len(COLORINGS), dtype=parameters.dtype)
        for u, v in matching:
            term *= matrices[EDGE_INDEX[u, v], COLORINGS[:, u], COLORINGS[:, v]]
        result += term
    return result


def jacobian(parameters: np.ndarray) -> np.ndarray:
    matrices = expand(parameters)
    full = np.zeros((len(COLORINGS), 4 * len(EDGES)), dtype=parameters.dtype)
    rows = np.arange(len(COLORINGS))
    for matching in MATCHINGS:
        values = [
            matrices[EDGE_INDEX[edge], COLORINGS[:, edge[0]], COLORINGS[:, edge[1]]]
            for edge in matching
        ]
        for position, edge in enumerate(matching):
            derivative = np.ones(len(COLORINGS), dtype=parameters.dtype)
            for other, value in enumerate(values):
                if other != position:
                    derivative *= value
            local = Q * COLORINGS[:, edge[0]] + COLORINGS[:, edge[1]]
            columns = 4 * EDGE_INDEX[edge] + local
            np.add.at(full, (rows, columns), derivative)
    return full @ EXPANSION


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260724)
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--max-nfev", type=int, default=5000)
    args = parser.parse_args()

    print("orbits", [len(orbit) for orbit in ORBITS], "parameters", PARAMETERS)
    rng = np.random.default_rng(args.seed)

    def decode(x: np.ndarray) -> np.ndarray:
        return x[:PARAMETERS] + 1j * x[PARAMETERS:]

    def residual(x: np.ndarray) -> np.ndarray:
        value = amplitudes(decode(x)) - TARGET
        return np.r_[value.real, value.imag]

    def real_jacobian(x: np.ndarray) -> np.ndarray:
        value = jacobian(decode(x))
        return np.block([[value.real, -value.imag], [value.imag, value.real]])

    for start in range(args.starts):
        x0 = rng.normal(scale=0.35, size=2 * PARAMETERS)
        fit = least_squares(
            residual,
            x0,
            jac=real_jacobian,
            max_nfev=args.max_nfev,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
        )
        error = residual(fit.x)
        print(
            start,
            "cost",
            fit.cost,
            "max",
            float(np.max(np.abs(error))),
            "norm",
            float(np.linalg.norm(fit.x)),
            "nfev",
            fit.nfev,
            "rankJ",
            int(np.linalg.matrix_rank(real_jacobian(fit.x), tol=1e-8)),
            flush=True,
        )


if __name__ == "__main__":
    main()
