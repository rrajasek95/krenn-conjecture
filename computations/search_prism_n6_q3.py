"""Search for a finite q=3 realization supported on the triangular prism."""

from __future__ import annotations

import argparse

import numpy as np
from scipy.optimize import least_squares

import search_n6_q3 as base


PRISM_EDGES = [(0, 4), (1, 2), (3, 5), (0, 5), (1, 4), (2, 3), (0, 3), (1, 5), (2, 4)]
FULL_SIZE = len(base.EDGES) * base.Q * base.Q


def expand(z: np.ndarray, active_coordinates: np.ndarray) -> np.ndarray:
    result = np.zeros(FULL_SIZE, dtype=z.dtype)
    result[active_coordinates] = z
    return result


def complexify(x: np.ndarray, use_complex: bool, active_size: int) -> np.ndarray:
    if not use_complex:
        return x
    return x[:active_size] + 1j * x[active_size:]


def run(seed: int, scale: float, max_evaluations: int, bound: float | None, use_complex: bool, extra_edges: list[tuple[int, int]]) -> None:
    rng = np.random.default_rng(seed)
    active_edges = PRISM_EDGES + extra_edges
    active_coordinates = np.array([
        base.EDGE_INDEX[edge] * base.Q * base.Q + local
        for edge in active_edges
        for local in range(base.Q * base.Q)
    ])
    active_size = len(active_coordinates)
    x0 = rng.normal(scale=scale, size=active_size * (2 if use_complex else 1))

    def residual(x: np.ndarray) -> np.ndarray:
        value = base.residual(expand(complexify(x, use_complex, active_size), active_coordinates))
        return np.concatenate((value.real, value.imag)) if use_complex else value

    def jacobian(x: np.ndarray) -> np.ndarray:
        value = base.jacobian(expand(complexify(x, use_complex, active_size), active_coordinates))[:, active_coordinates]
        if use_complex:
            return np.block([[value.real, -value.imag], [value.imag, value.real]])
        return value

    bounds = (-bound, bound) if bound is not None else (-np.inf, np.inf)
    fit = least_squares(
        residual,
        x0,
        jac=jacobian,
        bounds=bounds,
        max_nfev=max_evaluations,
        ftol=1e-13,
        xtol=1e-13,
        gtol=1e-13,
        tr_solver="lsmr",
    )
    parameters = expand(complexify(fit.x, use_complex, active_size), active_coordinates)
    error = base.residual(parameters)
    print(
        f"seed={seed} cost={fit.cost:.12g} max_abs={np.max(np.abs(error)):.6g} "
        f"norm={np.linalg.norm(parameters):.6g} opt={fit.optimality:.3g} nfev={fit.nfev}"
    )
    if np.max(np.abs(error)) < 1e-3:
        suffix = "complex" if use_complex else "real"
        np.savez(
            f"candidate_prism_{suffix}_seed{seed}.npz",
            matrices=base.unpack(parameters),
            residual=error,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--scale", type=float, default=0.3)
    parser.add_argument("--max-evaluations", type=int, default=3000)
    parser.add_argument("--bound", type=float)
    parser.add_argument("--complex", action="store_true", dest="use_complex")
    parser.add_argument("--extra", action="append", default=[], help="extra edge as uv, for example 01")
    args = parser.parse_args()
    for offset in range(args.starts):
        extras = [tuple(sorted((int(edge[0]), int(edge[1])))) for edge in args.extra]
        run(args.seed + offset, args.scale, args.max_evaluations, args.bound, args.use_complex, extras)
