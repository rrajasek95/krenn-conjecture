#!/usr/bin/env python3
"""C3-equivariant search for the binary rank-three GHZ projection at n=6.

The combined symmetry rotates vertices (0 2 4)(1 3 5) and acts on the
binary space by h=[[0,1],[-1,1]], which projectively cycles the three local
vectors e0,e0+e1,e1.  A discrete fourth-root edge cocycle leaves five seed
matrices (20 complex parameters).
"""

from __future__ import annotations

import itertools

import numpy as np
from scipy.optimize import least_squares

from search_binary_rank3_projection import perfect_matchings


N = 6
EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {edge: k for k, edge in enumerate(EDGES)}
MATCHINGS = tuple(perfect_matchings(tuple(range(N))))
COLORINGS = np.asarray(tuple(itertools.product(range(2), repeat=N)), dtype=np.int8)
TARGET = np.ones(len(COLORINGS), dtype=float)
TARGET[np.all(COLORINGS == 0, axis=1)] += 1
TARGET[np.all(COLORINGS == 1, axis=1)] += 1

RHO = (2, 3, 4, 5, 0, 1)
H = np.asarray(((0, 1), (-1, 1)), dtype=complex)
SEEDS = ((0, 1), (0, 2), (0, 3), (0, 5), (1, 3))
Q = {
    (0, 1): -1j, (2, 3): 1, (4, 5): 1j,
    (0, 2): 1j, (2, 4): -1, (0, 4): 1j,
    (0, 3): -1j, (2, 5): 1j, (1, 4): 1,
    (0, 5): 1, (1, 2): 1, (3, 4): 1,
    (1, 3): -1, (3, 5): -1j, (1, 5): -1j,
}


def oriented_put(answer, u, v, matrix):
    if u < v:
        answer[u, v] = matrix
    else:
        answer[v, u] = matrix.T


def expand(seed_vector):
    seeds = seed_vector.reshape(len(SEEDS), 2, 2)
    answer = {}
    for (u0, v0), seed in zip(SEEDS, seeds):
        u, v = u0, v0
        matrix = seed
        for _ in range(3):
            oriented_put(answer, u, v, matrix)
            q = Q[tuple(sorted((u, v)))]
            matrix = q * H @ matrix @ H.T
            u, v = RHO[u], RHO[v]
        assert np.linalg.norm(matrix - seed) < 1e-8 * max(1, np.linalg.norm(seed))
    assert set(answer) == set(EDGES)
    return np.asarray([answer[edge] for edge in EDGES])


def build_linear_map():
    result = np.zeros((4 * len(EDGES), 4 * len(SEEDS)), dtype=complex)
    for j in range(result.shape[1]):
        seed = np.zeros(result.shape[1], dtype=complex)
        seed[j] = 1
        result[:, j] = expand(seed).ravel()
    return result


LINEAR = build_linear_map()


def amplitudes(source_vector):
    matrices = source_vector.reshape(len(EDGES), 2, 2)
    result = np.zeros(len(COLORINGS), dtype=complex)
    for matching in MATCHINGS:
        term = np.ones(len(COLORINGS), dtype=complex)
        for u, v in matching:
            term *= matrices[
                EDGE_INDEX[(u, v)], COLORINGS[:, u], COLORINGS[:, v]
            ]
        result += term
    return result


def source_jacobian(source_vector):
    matrices = source_vector.reshape(len(EDGES), 2, 2)
    jacobian = np.zeros((len(COLORINGS), len(source_vector)), dtype=complex)
    rows = np.arange(len(COLORINGS))
    for matching in MATCHINGS:
        values = [
            matrices[EDGE_INDEX[e], COLORINGS[:, e[0]], COLORINGS[:, e[1]]]
            for e in matching
        ]
        for position, edge in enumerate(matching):
            derivative = np.ones(len(COLORINGS), dtype=complex)
            for k, value in enumerate(values):
                if k != position:
                    derivative *= value
            local = 2 * COLORINGS[:, edge[0]] + COLORINGS[:, edge[1]]
            columns = 4 * EDGE_INDEX[edge] + local
            np.add.at(jacobian, (rows, columns), derivative)
    return jacobian


def decode(x):
    count = 4 * len(SEEDS)
    return x[:count] + 1j * x[count:]


def residual(x, mu=0):
    seeds = decode(x)
    source = LINEAR @ seeds
    value = amplitudes(source) - TARGET
    base = np.r_[value.real, value.imag]
    if mu:
        # Penalize the actual source norm, not the seed-coordinate norm.
        actual = np.r_[source.real, source.imag]
        return np.r_[base, np.sqrt(mu) * actual]
    return base


def jacobian(x, mu=0):
    source = LINEAR @ decode(x)
    value = source_jacobian(source) @ LINEAR
    base = np.block([[value.real, -value.imag], [value.imag, value.real]])
    if mu:
        real_linear = np.block(
            [[LINEAR.real, -LINEAR.imag], [LINEAR.imag, LINEAR.real]]
        )
        return np.vstack((base, np.sqrt(mu) * real_linear))
    return base


def candidate_seeds():
    data = np.load("/tmp/binary_rank3_projection_n6_start2.npz")["matrices"]
    source = {edge: matrix for edge, matrix in zip(EDGES, data)}
    # Gauge recovered from the numerical projective C3 action.
    log_magnitude = np.asarray(
        (0.01917494, -0.00281421, 0.02414756, -0.00771367, -0.04332250, 0.01052787)
    )
    phase = np.asarray(
        (-1.16390372, 0.37036871, 0.32395769, 0.08569323, 0.83994603, -0.45606194)
    )
    gauge = np.exp(log_magnitude + 1j * phase)
    gauged = {
        edge: matrix * gauge[edge[0]] * gauge[edge[1]]
        for edge, matrix in source.items()
    }
    return np.asarray([gauged[edge] for edge in SEEDS]).ravel()


def main():
    seeds = candidate_seeds()
    x = np.r_[seeds.real, seeds.imag]
    print("initial", np.max(np.abs(residual(x))), np.linalg.norm(LINEAR @ seeds))
    for mu in (0, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 0):
        fit = least_squares(
            lambda y, mu=mu: residual(y, mu), x,
            jac=lambda y, mu=mu: jacobian(y, mu),
            max_nfev=20000, ftol=1e-14, xtol=1e-14, gtol=1e-14,
        )
        x = fit.x
        seeds = decode(x)
        source = LINEAR @ seeds
        print(
            "mu", mu, "error", np.max(np.abs(amplitudes(source) - TARGET)),
            "norm", np.linalg.norm(source), "rank", np.linalg.matrix_rank(jacobian(x), tol=1e-9),
        )
    for edge, matrix in zip(SEEDS, decode(x).reshape(len(SEEDS), 2, 2)):
        print(edge, np.round(matrix, 12))
    np.savez("/tmp/binary_rank3_projection_c3.npz", seeds=decode(x), matrices=(LINEAR @ decode(x)).reshape(15, 2, 2))


if __name__ == "__main__":
    main()
