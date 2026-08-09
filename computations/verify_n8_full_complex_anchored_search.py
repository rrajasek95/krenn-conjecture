#!/usr/bin/env python3
"""Independent sanity checks for the exact-pure anchored N=8 search chart."""

from __future__ import annotations

import numpy as np

import search_n8_full_complex as FULL
import search_n8_full_complex_anchored as ANCHORED


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def optimization_vector(free, complex_mode):
    return np.r_[free.real, free.imag] if complex_mode else free.real


def audit_mode(complex_mode, penalty, seed):
    rng = np.random.default_rng(seed)
    dtype = complex if complex_mode else float
    base = FULL.border_point(1).astype(dtype)
    free = base[ANCHORED.FREE] + 0.015 * rng.normal(
        size=len(ANCHORED.FREE)
    )
    if complex_mode:
        free += 0.015j * rng.normal(size=len(ANCHORED.FREE))

    z, implicit, cofactors = ANCHORED.anchored_point(free, 1e-10)
    output, _ = FULL.value_gradient(z, need_gradient=False)
    pure_error = max(abs(output[row] - 1) for row in ANCHORED.PURE_ROWS)
    require(pure_error < 2e-12, f"pure anchors drifted by {pure_error}")
    require(min(map(abs, cofactors)) > 1e-4,
            "audit point approached a pure-cofactor chart boundary")

    direction_free = rng.normal(size=len(free))
    if complex_mode:
        direction_free = direction_free + 1j * rng.normal(size=len(free))
    direction_free /= np.linalg.norm(direction_free)
    step = 1e-6
    plus = ANCHORED.anchored_point(free + step * direction_free, 1e-10)[0]
    minus = ANCHORED.anchored_point(free - step * direction_free, 1e-10)[0]
    numerical_pivots = (plus[list(ANCHORED.PIVOTS)]
                        - minus[list(ANCHORED.PIVOTS)]) / (2 * step)
    analytic_pivots = np.asarray([
        np.dot(derivative, direction_free) for derivative in implicit
    ])
    implicit_error = float(np.max(abs(numerical_pivots - analytic_pivots)))
    require(implicit_error < 2e-8,
            f"implicit pivot derivative error {implicit_error}")

    x = optimization_vector(free, complex_mode)
    direction = rng.normal(size=len(x))
    direction /= np.linalg.norm(direction)
    value, gradient = ANCHORED.objective_gradient(
        x, complex_mode, penalty, 1e-10
    )
    plus_value = ANCHORED.objective_gradient(
        x + step * direction, complex_mode, penalty, 1e-10
    )[0]
    minus_value = ANCHORED.objective_gradient(
        x - step * direction, complex_mode, penalty, 1e-10
    )[0]
    numerical = (plus_value - minus_value) / (2 * step)
    analytic = float(gradient @ direction)
    gradient_error = abs(numerical - analytic)
    require(
        gradient_error < 2e-7 * max(1, abs(numerical), abs(analytic)),
        f"objective gradient error {gradient_error}",
    )
    return {
        "value": value,
        "pure_error": pure_error,
        "implicit_error": implicit_error,
        "gradient_error": gradient_error,
    }


def main():
    require(len(ANCHORED.PIVOTS) == 3
            and len(set(ANCHORED.PIVOTS)) == 3,
            "the three pure pivots changed")
    require(len(ANCHORED.FREE) == FULL.PARAMETERS - 3,
            "the anchored chart dimension changed")
    real = audit_mode(False, 0.0, 7101)
    complex_row = audit_mode(True, 1e-4, 7102)
    print("N=8 exact-pure anchored numerical chart: PASS")
    print("real audit:", real)
    print("complex penalized audit:", complex_row)


if __name__ == "__main__":
    main()
