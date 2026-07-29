#!/usr/bin/env python3
"""Numerically test extensions of the exact q=2 cancellation support.

The fixed eight-edge support is the signed Delta_{6,2} gadget from
verify_cancellation_example.py.  For each chosen perfect matching we activate
its underlying edges as well, but allow a completely arbitrary 3x3 aggregate
matrix on every active edge.  This is only a discovery tool, not a proof.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares

import search_n6_q3 as base


BASE_EDGES = {
    (0, 1), (2, 3), (4, 5), (0, 2),
    (1, 3), (0, 5), (1, 2), (3, 4),
}


def fit_graph(active_edges: tuple[tuple[int, int], ...], seed: int,
              max_evaluations: int, bound: float | None) -> tuple[float, float, float]:
    active_coordinates = np.array([
        base.EDGE_INDEX[edge] * base.Q * base.Q + local
        for edge in active_edges
        for local in range(base.Q * base.Q)
    ])
    rng = np.random.default_rng(seed)
    x0 = rng.normal(scale=0.25, size=len(active_coordinates))

    def expand(z: np.ndarray) -> np.ndarray:
        answer = np.zeros(len(base.EDGES) * base.Q * base.Q)
        answer[active_coordinates] = z
        return answer

    def residual(z: np.ndarray) -> np.ndarray:
        return base.residual(expand(z))

    def jacobian(z: np.ndarray) -> np.ndarray:
        return base.jacobian(expand(z))[:, active_coordinates]

    limits = (-bound, bound) if bound is not None else (-np.inf, np.inf)
    result = least_squares(
        residual, x0, jac=jacobian, bounds=limits,
        max_nfev=max_evaluations, ftol=1e-13, xtol=1e-13, gtol=1e-13,
        tr_solver="lsmr",
    )
    error = residual(result.x)
    return float(np.max(np.abs(error))), float(np.linalg.norm(result.x)), float(result.cost)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=3)
    parser.add_argument("--max-evaluations", type=int, default=1500)
    parser.add_argument("--bound", type=float, default=10.0)
    args = parser.parse_args()

    seen: set[tuple[tuple[int, int], ...]] = set()
    for added_matching in base.MATCHINGS:
        graph = tuple(sorted(BASE_EDGES | set(added_matching)))
        if graph in seen or set(added_matching) <= BASE_EDGES:
            continue
        seen.add(graph)
        supported = sum(set(matching) <= set(graph) for matching in base.MATCHINGS)
        trials = [fit_graph(graph, 1000 * len(seen) + seed,
                            args.max_evaluations, args.bound)
                  for seed in range(args.starts)]
        best = min(trials)
        print(
            f"added={added_matching} edges={len(graph)} pms={supported} "
            f"max_abs={best[0]:.8g} norm={best[1]:.6g} cost={best[2]:.8g}"
        )


if __name__ == "__main__":
    main()
