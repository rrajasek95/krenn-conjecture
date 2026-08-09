#!/usr/bin/env python3
"""Numerical N=8 search on a chart with the three pure anchors exact.

One diagonal entry in each colour is eliminated from its (affine) pure
hafnian equation.  The optimization therefore sees only the 6,558 mixed
coefficients; unlike an unconstrained least-squares run, it cannot improve
the objective by dropping one of the three pure target coefficients.

This is a discovery tool, not a proof.  Every candidate must still be
recognized exactly and audited on all 6,561 output words.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

import search_n8_full_complex as FULL


PIVOTS = (
    (FULL.EDGE_INDEX[(5, 7)] * 9 + 0),
    (FULL.EDGE_INDEX[(6, 7)] * 9 + 4),
    (FULL.EDGE_INDEX[(5, 6)] * 9 + 8),
)
FREE = np.asarray(
    [index for index in range(FULL.PARAMETERS) if index not in PIVOTS],
    dtype=np.int64,
)
PURE_ROWS = tuple(
    int(np.flatnonzero(np.all(FULL.COLORINGS == colour, axis=1))[0])
    for colour in range(FULL.Q)
)
MIXED_MASK = FULL.TARGET == 0


def pure_value_gradient(z: np.ndarray, colour: int) -> tuple[complex, np.ndarray]:
    """Return the colour-pure hafnian and its holomorphic gradient."""

    matrices = z.reshape(len(FULL.EDGES), FULL.Q, FULL.Q)
    value = z.dtype.type(0)
    gradient = np.zeros(FULL.PARAMETERS, dtype=z.dtype)
    for matching in FULL.MATCHINGS:
        slots = [FULL.EDGE_INDEX[edge] * 9 + 3 * colour + colour
                 for edge in matching]
        values = [matrices.reshape(-1)[slot] for slot in slots]
        value += np.prod(values)
        for position, slot in enumerate(slots):
            derivative = z.dtype.type(1)
            for other, factor in enumerate(values):
                if other != position:
                    derivative *= factor
            gradient[slot] += derivative
    return value, gradient


def anchored_point(free: np.ndarray, minimum_cofactor: float) -> tuple[
    np.ndarray, tuple[np.ndarray, ...], tuple[complex, ...]
]:
    """Install the three eliminated entries and return implicit derivatives."""

    z = np.zeros(FULL.PARAMETERS, dtype=free.dtype)
    z[FREE] = free
    implicit = []
    cofactors = []
    for colour, pivot in enumerate(PIVOTS):
        value, gradient = pure_value_gradient(z, colour)
        cofactor = gradient[pivot]
        if abs(cofactor) < minimum_cofactor:
            raise FloatingPointError(
                f"pure cofactor {colour} too small: {abs(cofactor):.3g}"
            )
        # The current pivot is zero, so value is the affine remainder.
        z[pivot] = (1 - value) / cofactor
        _pure, final_gradient = pure_value_gradient(z, colour)
        derivative = -final_gradient[FREE] / cofactor
        implicit.append(derivative)
        cofactors.append(cofactor)
    return z, tuple(implicit), tuple(cofactors)


def decode(x: np.ndarray, complex_mode: bool) -> np.ndarray:
    if complex_mode:
        return x[:len(FREE)] + 1j * x[len(FREE):]
    return x


def encode(z: np.ndarray, complex_mode: bool) -> np.ndarray:
    free = z[FREE]
    return np.r_[free.real, free.imag] if complex_mode else free.real


def objective_gradient(
    x: np.ndarray,
    complex_mode: bool,
    l2_penalty: float,
    minimum_cofactor: float,
    pivot_bound: float | None = None,
    pivot_bound_penalty: float = 1e3,
) -> tuple[float, np.ndarray]:
    free = decode(x, complex_mode)
    try:
        z, implicit, _cofactors = anchored_point(free, minimum_cofactor)
    except FloatingPointError:
        # The rational chart boundary is not part of this search.  Returning
        # a large smooth-enough radial penalty keeps L-BFGS-B away from it.
        return 1e30 + float(np.vdot(x, x).real), 2 * x

    output, full_gradient = FULL.value_gradient(z)
    assert full_gradient is not None
    residual = output - FULL.TARGET
    # The installed pure residuals are roundoff-zero.  Removing them here
    # makes the objective definition literal and avoids their tiny gradient.
    loss = 0.5 * float(np.vdot(residual[MIXED_MASK], residual[MIXED_MASK]).real)
    residual[~MIXED_MASK] = 0

    # Recompute the adjoint with the pure residuals exactly suppressed.
    # FULL.value_gradient forms its gradient from its own residual, so its
    # pure contribution is only roundoff.  It is harmless but subtracting
    # the three explicit rows makes the chain rule deterministic.
    for colour, row in enumerate(PURE_ROWS):
        _value, pure_gradient = pure_value_gradient(z, colour)
        full_gradient -= np.conjugate(output[row] - 1) * pure_gradient

    if l2_penalty:
        loss += 0.5 * l2_penalty * float(np.vdot(z, z).real)
        # FULL's complex adjoint G is converted to real coordinates as
        # (Re G, -Im G), so |z|^2 contributes conjugate(z) to G.
        full_gradient += l2_penalty * np.conjugate(z)
    if pivot_bound is not None:
        for pivot in PIVOTS:
            modulus = abs(z[pivot])
            if modulus <= pivot_bound:
                continue
            excess = modulus - pivot_bound
            loss += 0.5 * pivot_bound_penalty * excess * excess
            full_gradient[pivot] += (
                pivot_bound_penalty * excess
                * np.conjugate(z[pivot]) / modulus
            )

    effective = full_gradient[FREE].copy()
    for pivot, derivative in zip(PIVOTS, implicit):
        effective += full_gradient[pivot] * derivative
    if complex_mode:
        return loss, np.r_[effective.real, -effective.imag]
    return loss, effective.real


def run(args: argparse.Namespace, seed: int) -> None:
    rng = np.random.default_rng(seed)
    if args.border_start:
        base = FULL.border_point(args.border_t).astype(complex if not args.real else float)
        base += args.noise * (
            rng.normal(size=FULL.PARAMETERS)
            + (0 if args.real else 1j * rng.normal(size=FULL.PARAMETERS))
        )
    else:
        base = rng.normal(scale=args.scale, size=FULL.PARAMETERS).astype(
            complex if not args.real else float
        )
        if not args.real:
            base += 1j * rng.normal(scale=args.scale, size=FULL.PARAMETERS)
        # Keep the rational chart initially away from its cofactor boundary.
        base += FULL.border_point(1).astype(base.dtype)
    x0 = encode(base, not args.real)
    bounds = None
    if args.entry_bound is not None:
        bounds = [(-args.entry_bound, args.entry_bound)] * len(x0)
        x0 = np.clip(x0, -args.entry_bound, args.entry_bound)

    fit = minimize(
        objective_gradient,
        x0,
        args=(not args.real, args.l2_penalty, args.minimum_cofactor,
              args.pivot_bound, args.pivot_bound_penalty),
        method="L-BFGS-B",
        jac=True,
        bounds=bounds,
        options={"maxiter": args.maxiter, "ftol": 1e-15, "gtol": 1e-11,
                 "maxls": 50, "maxcor": 40},
    )
    free = decode(fit.x, not args.real)
    z, _implicit, cofactors = anchored_point(free, args.minimum_cofactor)
    output, _gradient = FULL.value_gradient(z, need_gradient=False)
    residual = output - FULL.TARGET
    maximum = float(np.max(np.abs(residual[MIXED_MASK])))
    pure_max = float(np.max(np.abs(residual[~MIXED_MASK])))
    boundary = 0
    if args.entry_bound is not None:
        tolerance = max(1e-8, 1e-6 * args.entry_bound)
        boundary = int(np.count_nonzero(
            np.abs(np.abs(fit.x) - args.entry_bound) <= tolerance
        ))
    print(
        f"seed={seed} nit={fit.nit} mixed_loss="
        f"{0.5 * np.vdot(residual[MIXED_MASK], residual[MIXED_MASK]).real:.12g} "
        f"mixed_max={maximum:.7g} pure_max={pure_max:.3g} "
        f"norm={np.linalg.norm(z):.7g} max_entry={np.max(np.abs(z)):.7g} "
        f"min_cofactor={min(map(abs, cofactors)):.7g} free_boundary={boundary} "
        f"penalty={args.l2_penalty:.3g} status={fit.status}",
        flush=True,
    )
    if maximum < args.candidate_threshold:
        args.candidate_dir.mkdir(parents=True, exist_ok=True)
        np.savez(
            args.candidate_dir / f"candidate_n8_anchored_seed{seed}.npz",
            matrices=z.reshape(len(FULL.EDGES), FULL.Q, FULL.Q),
            residual=residual,
            pure_values=output[~MIXED_MASK],
            seed=seed,
            entry_bound=np.nan if args.entry_bound is None else args.entry_bound,
            l2_penalty=args.l2_penalty,
        )


def audit_gradient(args: argparse.Namespace) -> None:
    rng = np.random.default_rng(args.seed)
    complex_mode = not args.real
    base = FULL.border_point(1).astype(complex if complex_mode else float)
    free = base[FREE] + args.noise * (
        rng.normal(size=len(FREE))
        + (0 if not complex_mode else 1j * rng.normal(size=len(FREE)))
    )
    x = np.r_[free.real, free.imag] if complex_mode else free.real
    direction = rng.normal(size=len(x))
    direction /= np.linalg.norm(direction)
    step = 2e-6
    value, gradient = objective_gradient(
        x, complex_mode, args.l2_penalty, args.minimum_cofactor,
        args.pivot_bound, args.pivot_bound_penalty
    )
    plus = objective_gradient(
        x + step * direction, complex_mode, args.l2_penalty,
        args.minimum_cofactor, args.pivot_bound, args.pivot_bound_penalty
    )[0]
    minus = objective_gradient(
        x - step * direction, complex_mode, args.l2_penalty,
        args.minimum_cofactor, args.pivot_bound, args.pivot_bound_penalty
    )[0]
    numerical = (plus - minus) / (2 * step)
    analytic = float(gradient @ direction)
    error = abs(numerical - analytic)
    print(
        f"gradient_audit value={value:.9g} numerical={numerical:.9g} "
        f"analytic={analytic:.9g} error={error:.3g}"
    )
    if error > 2e-7 * max(1, abs(numerical), abs(analytic)):
        raise RuntimeError("anchored analytic gradient audit failed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starts", type=int, default=1)
    parser.add_argument("--maxiter", type=int, default=3000)
    parser.add_argument("--scale", type=float, default=0.05)
    parser.add_argument("--noise", type=float, default=0.02)
    parser.add_argument("--real", action="store_true")
    parser.add_argument("--border-start", action="store_true")
    parser.add_argument("--border-t", type=float, default=0.3)
    parser.add_argument(
        "--entry-bound", type=float,
        help="hard bound on the 249 free real/complex coordinates",
    )
    parser.add_argument(
        "--pivot-bound", type=float,
        help="soft modulus bound on the three rationally eliminated entries",
    )
    parser.add_argument("--pivot-bound-penalty", type=float, default=1e3)
    parser.add_argument("--l2-penalty", type=float, default=0.0)
    parser.add_argument("--minimum-cofactor", type=float, default=1e-8)
    parser.add_argument("--candidate-threshold", type=float, default=1e-8)
    parser.add_argument(
        "--candidate-dir", type=Path,
        default=Path("/tmp/krenn-n8-anchored-candidates"),
    )
    parser.add_argument("--audit-gradient", action="store_true")
    args = parser.parse_args()
    if args.entry_bound is not None and args.entry_bound <= 0:
        parser.error("--entry-bound must be positive")
    if args.pivot_bound is not None and args.pivot_bound <= 0:
        parser.error("--pivot-bound must be positive")
    if args.pivot_bound_penalty <= 0:
        parser.error("--pivot-bound-penalty must be positive")
    if args.l2_penalty < 0:
        parser.error("--l2-penalty must be nonnegative")
    if args.minimum_cofactor <= 0:
        parser.error("--minimum-cofactor must be positive")
    if args.audit_gradient:
        audit_gradient(args)
        return
    for seed in range(args.seed, args.seed + args.starts):
        run(args, seed)


if __name__ == "__main__":
    main()
