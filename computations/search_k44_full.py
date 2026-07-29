#!/usr/bin/env python3
"""Numerical search for a full-matrix K_{4,4} n=8 counterexample.

The support consists of all sixteen cross edges between vertices 0,...,3
and 4,...,7.  Every edge carries an arbitrary 3 by 3 aggregate matrix.
This is only a discovery calculation: any small-residual point must be
recognized exactly and checked coefficient by coefficient.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import minimize


M, Q = 4, 3
LEFT = tuple(range(M))
RIGHT = tuple(range(M, 2 * M))
EDGES = tuple((u, M + j) for u in LEFT for j in range(M))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
PERMUTATIONS = tuple(itertools.permutations(range(M)))
COLORINGS = np.asarray(
    tuple(itertools.product(range(Q), repeat=2 * M)), dtype=np.int8
)
TARGET = np.asarray([len(set(c)) == 1 for c in COLORINGS], dtype=float)
PARAMETERS = len(EDGES) * Q * Q


def amplitudes_and_gradient(
    z: np.ndarray, need_gradient: bool = True
) -> tuple[np.ndarray, np.ndarray | None]:
    matrices = z.reshape(len(EDGES), Q, Q)
    output = np.zeros(len(COLORINGS), dtype=z.dtype)
    cache: list[tuple[list[np.ndarray], list[tuple[int, np.ndarray, np.ndarray]]]] = []
    for permutation in PERMUTATIONS:
        values: list[np.ndarray] = []
        slots: list[tuple[int, np.ndarray, np.ndarray]] = []
        for u, j in enumerate(permutation):
            edge_number = EDGE_INDEX[(u, M + j)]
            aa = COLORINGS[:, u]
            bb = COLORINGS[:, M + j]
            values.append(matrices[edge_number, aa, bb])
            slots.append((edge_number, aa, bb))
        output += np.prod(values, axis=0)
        if need_gradient:
            cache.append((values, slots))

    if not need_gradient:
        return output, None

    residual = output - TARGET
    gradient = np.zeros_like(matrices)
    for values, slots in cache:
        for position, (edge_number, aa, bb) in enumerate(slots):
            derivative = np.ones(len(COLORINGS), dtype=z.dtype)
            for other, value in enumerate(values):
                if other != position:
                    derivative *= value
            np.add.at(
                gradient[edge_number],
                (aa, bb),
                np.conjugate(residual) * derivative,
            )
    return output, gradient.reshape(-1)


def run(seed: int, complex_search: bool, maxiter: int, scale: float) -> None:
    rng = np.random.default_rng(seed)
    count = PARAMETERS
    if complex_search:
        x0 = rng.normal(scale=scale, size=2 * count)

        def decode(x: np.ndarray) -> np.ndarray:
            return x[:count] + 1j * x[count:]

        def objective(x: np.ndarray) -> tuple[float, np.ndarray]:
            output, gradient = amplitudes_and_gradient(decode(x))
            assert gradient is not None
            residual = output - TARGET
            loss = 0.5 * float(np.vdot(residual, residual).real)
            return loss, np.r_[gradient.real, -gradient.imag]

    else:
        x0 = rng.normal(scale=scale, size=count)

        def decode(x: np.ndarray) -> np.ndarray:
            return x

        def objective(x: np.ndarray) -> tuple[float, np.ndarray]:
            output, gradient = amplitudes_and_gradient(x)
            assert gradient is not None
            residual = output - TARGET
            loss = 0.5 * float(np.vdot(residual, residual).real)
            return loss, gradient.real

    result = minimize(
        objective,
        x0,
        method="L-BFGS-B",
        jac=True,
        options={
            "maxiter": maxiter,
            "ftol": 1e-15,
            "gtol": 1e-11,
            "maxls": 50,
            "maxcor": 30,
        },
    )
    z = decode(result.x)
    output, _ = amplitudes_and_gradient(z, need_gradient=False)
    residual = output - TARGET
    maximum = float(np.max(np.abs(residual)))
    print(
        f"seed={seed} nit={result.nit} loss={0.5 * np.vdot(residual, residual).real:.12g} "
        f"max={maximum:.7g} norm={np.linalg.norm(z):.7g} "
        f"status={result.status}",
        flush=True,
    )
    if maximum < 1e-7:
        np.savez(
            f"computations/candidate_k44_full_seed{seed}.npz",
            matrices=z.reshape(len(EDGES), Q, Q),
            residual=residual,
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starts", type=int, default=1)
    parser.add_argument("--maxiter", type=int, default=3000)
    parser.add_argument("--scale", type=float, default=0.35)
    parser.add_argument("--complex", action="store_true", dest="complex_search")
    args = parser.parse_args()
    for seed in range(args.seed, args.seed + args.starts):
        run(seed, args.complex_search, args.maxiter, args.scale)


if __name__ == "__main__":
    main()
