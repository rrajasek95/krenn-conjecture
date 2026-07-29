#!/usr/bin/env python3
"""Numerical falsification search on the residual all-rank-one C6 chart.

This is discovery-only: floating-point output is never a proof certificate.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares

import search_n6_q3 as full


CYCLE = {(0, 3), (0, 5), (1, 4), (1, 5), (2, 3), (2, 4)}
LABELS = {
    (0, 1): (2, 1),
    (0, 2): (0, 0),
    (0, 4): (0, 2),
    (1, 2): (1, 1),
    (1, 3): (1, 0),
    (2, 5): (0, 2),
    (3, 4): (2, 0),
    (3, 5): (2, 2),
    (4, 5): (1, 1),
}


SUPPORTS = {
    edge: (
        (tuple(range(3)), tuple(range(3)))
        if edge in CYCLE
        else ((LABELS[edge][0],), (LABELS[edge][1],))
    )
    for edge in full.EDGES
}


PARAMETERS = []
for edge in full.EDGES:
    left, right = SUPPORTS[edge]
    PARAMETERS.extend((edge, "a", color) for color in left[1:])
    PARAMETERS.extend((edge, "b", color) for color in right)
PARAMETER_INDEX = {key: index for index, key in enumerate(PARAMETERS)}


def matrices_and_chain(parameters):
    matrices = np.zeros((len(full.EDGES), 3, 3), dtype=parameters.dtype)
    chain = np.zeros((len(full.EDGES) * 9, len(PARAMETERS)), dtype=parameters.dtype)
    for edge_index, edge in enumerate(full.EDGES):
        left, right = SUPPORTS[edge]
        a = {left[0]: parameters.dtype.type(1)}
        a.update(
            {
                color: parameters[PARAMETER_INDEX[edge, "a", color]]
                for color in left[1:]
            }
        )
        b = {
            color: parameters[PARAMETER_INDEX[edge, "b", color]]
            for color in right
        }
        for i, j in itertools.product(left, right):
            matrices[edge_index, i, j] = a[i] * b[j]
            row = edge_index * 9 + 3 * i + j
            if i != left[0]:
                chain[row, PARAMETER_INDEX[edge, "a", i]] = b[j]
            chain[row, PARAMETER_INDEX[edge, "b", j]] = a[i]
    return matrices, chain


def values_and_jacobian(parameters):
    matrices, chain = matrices_and_chain(parameters)
    flat = matrices.reshape(-1)
    return full.amplitudes(flat), full.jacobian(flat) @ chain


def run(seed, max_nfev):
    rng = np.random.default_rng(seed)
    count = len(PARAMETERS)
    initial = rng.normal(scale=0.5, size=2 * count)

    def unpack(real):
        return real[:count] + 1j * real[count:]

    def residual(real):
        values, _ = values_and_jacobian(unpack(real))
        answer = values - full.TARGET
        return np.concatenate((answer.real, answer.imag))

    def jacobian(real):
        _, value = values_and_jacobian(unpack(real))
        return np.block([[value.real, -value.imag], [value.imag, value.real]])

    fit = least_squares(
        residual,
        initial,
        jac=jacobian,
        max_nfev=max_nfev,
        ftol=1e-13,
        xtol=1e-13,
        gtol=1e-13,
    )
    error = residual(fit.x)
    print(
        f"seed={seed} cost={fit.cost:.12g} max={np.max(np.abs(error)):.4g} "
        f"norm={np.linalg.norm(fit.x):.4g} nfev={fit.nfev}"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--max-nfev", type=int, default=5000)
    args = parser.parse_args()
    for offset in range(args.starts):
        run(args.seed + offset, args.max_nfev)


if __name__ == "__main__":
    main()
