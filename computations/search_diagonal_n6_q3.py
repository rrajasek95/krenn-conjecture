"""Numerically probe the same-color (diagonal edge-matrix) subproblem."""

from __future__ import annotations

import argparse

import numpy as np
from scipy.optimize import least_squares

import search_n6_q3 as base


FULL_SIZE = len(base.EDGES) * base.Q * base.Q
ACTIVE = np.array([
    edge_index * base.Q * base.Q + color * base.Q + color
    for edge_index in range(len(base.EDGES))
    for color in range(base.Q)
])
ACTIVE_SIZE = len(ACTIVE)


def expand(z: np.ndarray) -> np.ndarray:
    result = np.zeros(FULL_SIZE, dtype=z.dtype)
    result[ACTIVE] = z
    return result


def run(seed: int, bound: float | None, max_evaluations: int, use_complex: bool) -> None:
    rng = np.random.default_rng(seed)
    x0 = rng.normal(scale=0.3, size=ACTIVE_SIZE * (2 if use_complex else 1))

    def decode(x: np.ndarray) -> np.ndarray:
        if use_complex:
            return x[:ACTIVE_SIZE] + 1j * x[ACTIVE_SIZE:]
        return x

    def residual(x: np.ndarray) -> np.ndarray:
        value = base.residual(expand(decode(x)))
        return np.concatenate((value.real, value.imag)) if use_complex else value

    def jacobian(x: np.ndarray) -> np.ndarray:
        value = base.jacobian(expand(decode(x)))[:, ACTIVE]
        return np.block([[value.real, -value.imag], [value.imag, value.real]]) if use_complex else value

    bounds = (-bound, bound) if bound is not None else (-np.inf, np.inf)
    fit = least_squares(
        residual,
        x0,
        jac=jacobian,
        bounds=bounds,
        tr_solver="lsmr",
        max_nfev=max_evaluations,
        ftol=1e-13,
        xtol=1e-13,
        gtol=1e-13,
    )
    parameters = expand(decode(fit.x))
    error = base.residual(parameters)
    print(
        f"seed={seed} cost={fit.cost:.12g} max_abs={np.max(np.abs(error)):.6g} "
        f"norm={np.linalg.norm(parameters):.6g} opt={fit.optimality:.3g} nfev={fit.nfev}"
    )
    if np.max(np.abs(error)) < 1e-3:
        suffix = "complex" if use_complex else "real"
        np.savez(f"candidate_diagonal_{suffix}_seed{seed}.npz", matrices=base.unpack(parameters), residual=error)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--bound", type=float)
    parser.add_argument("--max-evaluations", type=int, default=5000)
    parser.add_argument("--complex", action="store_true", dest="use_complex")
    args = parser.parse_args()
    for offset in range(args.starts):
        run(args.seed + offset, args.bound, args.max_evaluations, args.use_complex)
