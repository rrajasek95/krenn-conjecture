"""Numerical falsification search for a 6-party, 3-color hafnian realization.

This is deliberately not a certificate.  Its purpose is to test sparse and
generic ansatzes and to expose candidate exact patterns for later symbolic
work.  Variables are the 3x3 aggregate endpoint-color matrices on all 15
unordered vertex pairs.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


N = 6
Q = 3
EDGES = list(itertools.combinations(range(N), 2))
EDGE_INDEX = {edge: idx for idx, edge in enumerate(EDGES)}


def perfect_matchings(vertices: tuple[int, ...]) -> list[tuple[tuple[int, int], ...]]:
    if not vertices:
        return [()]
    u = vertices[0]
    result: list[tuple[tuple[int, int], ...]] = []
    for pos in range(1, len(vertices)):
        v = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for matching in perfect_matchings(rest):
            result.append(((u, v),) + matching)
    return result


MATCHINGS = perfect_matchings(tuple(range(N)))
COLORINGS = np.array(list(itertools.product(range(Q), repeat=N)), dtype=np.int8)
TARGET = np.array([1.0 if len(set(c)) == 1 else 0.0 for c in COLORINGS])
TERM_SIGNS = np.ones(len(MATCHINGS))


def pfaffian_sign(matching):
    edges = sorted((min(u, v), max(u, v)) for u, v in matching)
    crossings = sum(
        u < x < v < y or x < u < y < v
        for index, (u, v) in enumerate(edges)
        for x, y in edges[index + 1 :]
    )
    return -1.0 if crossings % 2 else 1.0


def unpack(x: np.ndarray) -> np.ndarray:
    return x.reshape(len(EDGES), Q, Q)


def edge_entry(matrices: np.ndarray, u: int, v: int, colors: np.ndarray) -> np.ndarray:
    if u < v:
        return matrices[EDGE_INDEX[(u, v)], colors[:, u], colors[:, v]]
    return matrices[EDGE_INDEX[(v, u)], colors[:, v], colors[:, u]]


def amplitudes(x: np.ndarray) -> np.ndarray:
    matrices = unpack(x)
    answer = np.zeros(len(COLORINGS), dtype=x.dtype)
    for matching_index, matching in enumerate(MATCHINGS):
        term = np.full(
            len(COLORINGS), TERM_SIGNS[matching_index], dtype=x.dtype
        )
        for u, v in matching:
            term *= edge_entry(matrices, u, v, COLORINGS)
        answer += term
    return answer


def residual(x: np.ndarray) -> np.ndarray:
    return amplitudes(x) - TARGET


def jacobian(x: np.ndarray) -> np.ndarray:
    matrices = unpack(x)
    jac = np.zeros((len(COLORINGS), len(x)), dtype=x.dtype)
    rows = np.arange(len(COLORINGS))
    for matching_index, matching in enumerate(MATCHINGS):
        values = [edge_entry(matrices, u, v, COLORINGS) for u, v in matching]
        for edge_pos, (u, v) in enumerate(matching):
            derivative = np.full(
                len(COLORINGS), TERM_SIGNS[matching_index], dtype=x.dtype
            )
            for other_pos, value in enumerate(values):
                if other_pos != edge_pos:
                    derivative *= value
            edge_idx = EDGE_INDEX[(min(u, v), max(u, v))]
            if u < v:
                local = COLORINGS[:, u] * Q + COLORINGS[:, v]
            else:
                local = COLORINGS[:, v] * Q + COLORINGS[:, u]
            cols = edge_idx * Q * Q + local
            np.add.at(jac, (rows, cols), derivative)
    return jac


def run(
    seed: int,
    scale: float,
    max_evaluations: int,
    bound: float | None,
    use_complex: bool,
) -> None:
    rng = np.random.default_rng(seed)
    parameter_count = len(EDGES) * Q * Q
    x0 = rng.normal(scale=scale, size=parameter_count * (2 if use_complex else 1))
    if use_complex:
        def to_complex(x: np.ndarray) -> np.ndarray:
            return x[:parameter_count] + 1j * x[parameter_count:]

        def fit_residual(x: np.ndarray) -> np.ndarray:
            value = residual(to_complex(x))
            return np.concatenate((value.real, value.imag))

        def fit_jacobian(x: np.ndarray) -> np.ndarray:
            value = jacobian(to_complex(x))
            return np.block([[value.real, -value.imag], [value.imag, value.real]])
    else:
        to_complex = lambda x: x
        fit_residual = residual
        fit_jacobian = jacobian
    bounds = (-bound, bound) if bound is not None else (-np.inf, np.inf)
    fit = least_squares(
        fit_residual,
        x0,
        jac=fit_jacobian,
        max_nfev=max_evaluations,
        verbose=0,
        ftol=1e-13,
        xtol=1e-13,
        gtol=1e-13,
        bounds=bounds,
    )
    fitted_parameters = to_complex(fit.x)
    r = residual(fitted_parameters)
    print(
        f"seed={seed} cost={fit.cost:.12g} max_abs={np.max(np.abs(r)):.6g} "
        f"norm_x={np.linalg.norm(fit.x):.6g} optimality={fit.optimality:.3g} "
        f"nfev={fit.nfev} status={fit.status}"
    )
    if np.max(np.abs(r)) < 1e-3:
        suffix = "complex" if use_complex else "real"
        np.savez(
            f"candidate_n6_q3_{suffix}_seed{seed}.npz",
            matrices=unpack(fitted_parameters),
            residual=r,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--scale", type=float, default=0.3)
    parser.add_argument("--max-evaluations", type=int, default=5000)
    parser.add_argument("--bound", type=float)
    parser.add_argument("--complex", action="store_true", dest="use_complex")
    parser.add_argument(
        "--pfaffian-signs",
        action="store_true",
        help="use the standard crossing signs instead of the unsigned hafnian",
    )
    args = parser.parse_args()
    if args.pfaffian_signs:
        TERM_SIGNS[:] = [pfaffian_sign(matching) for matching in MATCHINGS]
    for offset in range(args.starts):
        run(
            args.seed + offset,
            args.scale,
            args.max_evaluations,
            args.bound,
            args.use_complex,
        )
