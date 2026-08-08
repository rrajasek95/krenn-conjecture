#!/usr/bin/env python3
"""Unrestricted numerical counterexample search for H_8(A)=Delta_{8,3}.

All 28 unordered vertex pairs carry independent 3 by 3 complex matrices.
The implementation uses the exact 105-matching expansion and its analytic
adjoint.  Numerical output is only for discovery; a candidate must be
recognized and independently verified over an exact number field.
"""

from __future__ import annotations

import argparse
import itertools
from pathlib import Path

import numpy as np
from scipy.optimize import minimize


N, Q = 8, 3
EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {edge: number for number, edge in enumerate(EDGES)}
COLORINGS = np.asarray(
    tuple(itertools.product(range(Q), repeat=N)), dtype=np.int8
)
TARGET = np.asarray([len(set(c)) == 1 for c in COLORINGS], dtype=float)
PARAMETERS = len(EDGES) * Q * Q


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings(tuple(range(N))))


def value_gradient(
    z: np.ndarray, need_gradient: bool = True
) -> tuple[np.ndarray, np.ndarray | None]:
    matrices = z.reshape(len(EDGES), Q, Q)
    output = np.zeros(len(COLORINGS), dtype=z.dtype)
    cache: list[tuple[list[np.ndarray], list[tuple[int, np.ndarray, np.ndarray]]]] = []
    for matching in MATCHINGS:
        values: list[np.ndarray] = []
        slots: list[tuple[int, np.ndarray, np.ndarray]] = []
        for u, v in matching:
            edge_number = EDGE_INDEX[u, v]
            aa, bb = COLORINGS[:, u], COLORINGS[:, v]
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


def border_point(t: float) -> np.ndarray:
    """First exact Laurent family from notes/n8-counterexample-recon.md."""
    matrices = np.zeros((len(EDGES), Q, Q), dtype=float)
    matchings = (
        ((0, 2), (1, 4), (3, 6), (5, 7)),
        ((0, 3), (1, 5), (2, 4), (6, 7)),
        ((0, 1), (2, 3), (4, 7), (5, 6)),
    )
    weights = {(3, 6): t, (1, 4): 1.0 / t}
    for color, matching in enumerate(matchings):
        for edge in matching:
            matrices[EDGE_INDEX[edge], color, color] = weights.get(edge, 1.0)
    return matrices.reshape(-1)


def run(
    seed: int,
    maxiter: int,
    scale: float,
    real_search: bool,
    border_start: bool,
    border_t: float,
    noise: float,
    entry_bound: float | None,
    l2_penalty: float,
    candidate_threshold: float,
    candidate_dir: Path,
) -> None:
    rng = np.random.default_rng(seed)
    base = border_point(border_t) if border_start else None
    if real_search:
        x0 = rng.normal(scale=noise if border_start else scale, size=PARAMETERS)
        if base is not None:
            x0 += base

        def decode(x: np.ndarray) -> np.ndarray:
            return x

        def objective(x: np.ndarray) -> tuple[float, np.ndarray]:
            output, gradient = value_gradient(x)
            assert gradient is not None
            residual = output - TARGET
            loss = 0.5 * float(np.vdot(residual, residual).real)
            if l2_penalty:
                loss += 0.5 * l2_penalty * float(np.vdot(x, x).real)
                gradient = gradient + l2_penalty * x
            return loss, gradient.real

    else:
        x0 = rng.normal(
            scale=noise if border_start else scale, size=2 * PARAMETERS
        )
        if base is not None:
            x0[:PARAMETERS] += base

        def decode(x: np.ndarray) -> np.ndarray:
            return x[:PARAMETERS] + 1j * x[PARAMETERS:]

        def objective(x: np.ndarray) -> tuple[float, np.ndarray]:
            output, gradient = value_gradient(decode(x))
            assert gradient is not None
            residual = output - TARGET
            loss = 0.5 * float(np.vdot(residual, residual).real)
            real_gradient = np.r_[gradient.real, -gradient.imag]
            if l2_penalty:
                loss += 0.5 * l2_penalty * float(np.vdot(x, x).real)
                real_gradient += l2_penalty * x
            return loss, real_gradient

    bounds = None
    if entry_bound is not None:
        if entry_bound <= 0:
            raise ValueError("entry_bound must be positive")
        bounds = [(-entry_bound, entry_bound)] * len(x0)
        x0 = np.clip(x0, -entry_bound, entry_bound)

    fit = minimize(
        objective,
        x0,
        method="L-BFGS-B",
        jac=True,
        bounds=bounds,
        options={
            "maxiter": maxiter,
            "ftol": 1e-15,
            "gtol": 1e-11,
            "maxls": 50,
            "maxcor": 40,
        },
    )
    z = decode(fit.x)
    output, _ = value_gradient(z, need_gradient=False)
    residual = output - TARGET
    maximum = float(np.max(np.abs(residual)))
    pure_residual_max = float(np.max(np.abs(residual[TARGET == 1])))
    mixed_residual_max = float(np.max(np.abs(residual[TARGET == 0])))
    max_entry = float(np.max(np.abs(z)))
    if entry_bound is None:
        boundary_coordinates = 0
    else:
        # L-BFGS-B bounds real and imaginary coordinates separately.  Report
        # proximity in those literal optimization coordinates, not in complex
        # modulus, so a run that leans on the compactification is visible.
        tolerance = max(1e-8, 1e-6 * entry_bound)
        boundary_coordinates = int(
            np.count_nonzero(np.abs(np.abs(fit.x) - entry_bound) <= tolerance)
        )
    print(
        f"seed={seed} nit={fit.nit} loss={0.5 * np.vdot(residual, residual).real:.12g} "
        f"max={maximum:.7g} pure_max={pure_residual_max:.7g} "
        f"mixed_max={mixed_residual_max:.7g} norm={np.linalg.norm(z):.7g} "
        f"max_entry={max_entry:.7g} boundary={boundary_coordinates} "
        f"penalty={l2_penalty:.3g} status={fit.status}",
        flush=True,
    )
    if maximum < candidate_threshold:
        candidate_dir.mkdir(parents=True, exist_ok=True)
        np.savez(
            candidate_dir / f"candidate_n8_full_seed{seed}.npz",
            matrices=z.reshape(len(EDGES), Q, Q),
            residual=residual,
            pure_values=output[TARGET == 1],
            seed=seed,
            entry_bound=np.nan if entry_bound is None else entry_bound,
            l2_penalty=l2_penalty,
            boundary_coordinates=boundary_coordinates,
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starts", type=int, default=1)
    parser.add_argument("--maxiter", type=int, default=5000)
    parser.add_argument("--scale", type=float, default=0.3)
    parser.add_argument("--real", action="store_true")
    parser.add_argument("--border-start", action="store_true")
    parser.add_argument("--border-t", type=float, default=0.3)
    parser.add_argument("--noise", type=float, default=0.02)
    parser.add_argument(
        "--entry-bound",
        type=float,
        help=(
            "bound every real optimization coordinate in [-B,B]; use a "
            "sequence of bounds to distinguish finite candidates from "
            "Laurent escape"
        ),
    )
    parser.add_argument(
        "--l2-penalty",
        type=float,
        default=0.0,
        help=(
            "optional discovery-only source norm penalty; raw residual loss "
            "is still reported and used for candidate acceptance"
        ),
    )
    parser.add_argument("--candidate-threshold", type=float, default=1e-7)
    parser.add_argument(
        "--candidate-dir", type=Path, default=Path("computations")
    )
    args = parser.parse_args()
    if args.l2_penalty < 0:
        parser.error("--l2-penalty must be nonnegative")
    if args.candidate_threshold <= 0:
        parser.error("--candidate-threshold must be positive")
    for seed in range(args.seed, args.seed + args.starts):
        run(
            seed,
            args.maxiter,
            args.scale,
            args.real,
            args.border_start,
            args.border_t,
            args.noise,
            args.entry_bound,
            args.l2_penalty,
            args.candidate_threshold,
            args.candidate_dir,
        )


if __name__ == "__main__":
    main()
