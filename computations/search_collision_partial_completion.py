#!/usr/bin/env python3
"""Numerically probe the unrestricted six-site collision two-jet system.

The variables are arbitrary 3 by 3 edge matrices in the basis x,y,z.  We
constrain exactly the output coefficients with at most two z sites:

    z-degree 0: 2 X + Y
    z-degree 1: 0
    z-degree 2: X_2 / 2.

Thus a zero residual is precisely an unrestricted q0/q1/q2 collision jet;
coefficients of z-degree at least three are deliberately ignored.  This is
a numerical discovery/falsification probe, not a certificate.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


N = 6
EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {edge: position for position, edge in enumerate(EDGES)}


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


MATCHINGS = tuple(perfect_matchings(range(N)))
ALL_COLORINGS = np.asarray(
    tuple(itertools.product(range(3), repeat=N)), dtype=np.int8
)
COLORINGS = ALL_COLORINGS[
    np.count_nonzero(ALL_COLORINGS == 2, axis=1) <= 2
]
TARGET = np.zeros(len(COLORINGS), dtype=complex)
for row, coloring in enumerate(COLORINGS):
    z_count = np.count_nonzero(coloring == 2)
    if z_count == 0:
        if np.all(coloring == 0):
            TARGET[row] = 2
        elif np.all(coloring == 1):
            TARGET[row] = 1
    elif z_count == 2 and np.all(coloring[coloring != 2] == 0):
        TARGET[row] = 0.5

PARAMETER_COUNT = 9 * len(EDGES)
ROWS = np.arange(len(COLORINGS))


def amplitudes(vector):
    matrices = vector.reshape(len(EDGES), 3, 3)
    answer = np.zeros(len(COLORINGS), dtype=complex)
    for matching in MATCHINGS:
        term = np.ones(len(COLORINGS), dtype=complex)
        for u, v in matching:
            term *= matrices[
                EDGE_INDEX[(u, v)], COLORINGS[:, u], COLORINGS[:, v]
            ]
        answer += term
    return answer


def complex_jacobian(vector):
    matrices = vector.reshape(len(EDGES), 3, 3)
    answer = np.zeros(
        (len(COLORINGS), PARAMETER_COUNT), dtype=complex
    )
    for matching in MATCHINGS:
        values = [
            matrices[
                EDGE_INDEX[edge],
                COLORINGS[:, edge[0]],
                COLORINGS[:, edge[1]],
            ]
            for edge in matching
        ]
        for position, edge in enumerate(matching):
            derivative = np.ones(len(COLORINGS), dtype=complex)
            for other_position, value in enumerate(values):
                if position != other_position:
                    derivative *= value
            columns = (
                9 * EDGE_INDEX[edge]
                + 3 * COLORINGS[:, edge[0]]
                + COLORINGS[:, edge[1]]
            )
            np.add.at(answer, (ROWS, columns), derivative)
    return answer


def decode(real_vector):
    return (
        real_vector[:PARAMETER_COUNT]
        + 1j * real_vector[PARAMETER_COUNT:]
    )


def residual(real_vector):
    value = amplitudes(decode(real_vector)) - TARGET
    return np.r_[value.real, value.imag]


def jacobian(real_vector):
    value = complex_jacobian(decode(real_vector))
    return np.block(
        [[value.real, -value.imag], [value.imag, value.real]]
    )


def hamilton_seed(rng, scale):
    matrices = np.zeros((len(EDGES), 3, 3), dtype=complex)
    px = ((0, 1), (2, 3), (4, 5))
    py = ((0, 5), (1, 2), (3, 4))
    for position, edge in enumerate(px):
        matrices[EDGE_INDEX[edge], 0, 0] = 2 if position == 0 else 1
    for edge in py:
        matrices[EDGE_INDEX[edge], 1, 1] = 1
    matrices += scale * (
        rng.normal(size=matrices.shape)
        + 1j * rng.normal(size=matrices.shape)
    )
    return matrices.ravel()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--scale", type=float, default=0.05)
    parser.add_argument("--max-nfev", type=int, default=5000)
    parser.add_argument("--random", action="store_true")
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    print(
        f"constrained_coefficients={len(COLORINGS)} "
        f"complex_variables={PARAMETER_COUNT}",
        flush=True,
    )
    for start in range(args.starts):
        if args.random:
            source = args.scale * (
                rng.normal(size=PARAMETER_COUNT)
                + 1j * rng.normal(size=PARAMETER_COUNT)
            )
        else:
            source = hamilton_seed(rng, args.scale)
        initial = np.r_[source.real, source.imag]
        fit = least_squares(
            residual,
            initial,
            jac=jacobian,
            max_nfev=args.max_nfev,
            ftol=1e-14,
            xtol=1e-14,
            gtol=1e-14,
        )
        value = amplitudes(decode(fit.x)) - TARGET
        print(
            f"start={args.seed + start} cost={fit.cost:.12g} "
            f"max={np.max(np.abs(value)):.8g} "
            f"optimality={fit.optimality:.3g} nfev={fit.nfev} "
            f"norm={np.linalg.norm(decode(fit.x)):.6g}",
            flush=True,
        )
        if np.max(np.abs(value)) < 1e-7:
            np.savez(
                "/tmp/collision_partial_n6.npz",
                matrices=decode(fit.x).reshape(len(EDGES), 3, 3),
                residual=value,
            )
            break


if __name__ == "__main__":
    main()
