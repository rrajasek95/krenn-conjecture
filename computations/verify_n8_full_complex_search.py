#!/usr/bin/env python3
"""Independent numerical sanity checks for search_n8_full_complex.py.

This verifies the matching expansion against a direct enumerator and checks
the analytic real and complex gradients by centered directional differences.
It is not a certificate for any search result.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH_PATH = HERE / "search_n8_full_complex.py"
SPEC = importlib.util.spec_from_file_location("n8_full_search", SEARCH_PATH)
assert SPEC is not None and SPEC.loader is not None
SEARCH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SEARCH)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def direct_output(z: np.ndarray) -> np.ndarray:
    matrices = z.reshape(len(SEARCH.EDGES), SEARCH.Q, SEARCH.Q)
    output = np.zeros(len(SEARCH.COLORINGS), dtype=z.dtype)
    for word_number, word in enumerate(SEARCH.COLORINGS):
        value = 0
        for matching in SEARCH.MATCHINGS:
            term = 1
            for u, v in matching:
                term *= matrices[SEARCH.EDGE_INDEX[u, v], word[u], word[v]]
            value += term
        output[word_number] = value
    return output


def loss_and_gradient(x: np.ndarray, complex_mode: bool, penalty: float):
    if complex_mode:
        z = x[: SEARCH.PARAMETERS] + 1j * x[SEARCH.PARAMETERS :]
    else:
        z = x
    output, gradient = SEARCH.value_gradient(z)
    assert gradient is not None
    residual = output - SEARCH.TARGET
    loss = 0.5 * float(np.vdot(residual, residual).real)
    if complex_mode:
        real_gradient = np.r_[gradient.real, -gradient.imag]
    else:
        real_gradient = gradient.real
    loss += 0.5 * penalty * float(np.vdot(x, x).real)
    real_gradient += penalty * x
    return loss, real_gradient


def check_gradient(rng: np.random.Generator, complex_mode: bool) -> float:
    size = SEARCH.PARAMETERS * (2 if complex_mode else 1)
    x = rng.normal(scale=0.08, size=size)
    direction = rng.normal(size=size)
    direction /= np.linalg.norm(direction)
    penalty = 3e-5
    _, gradient = loss_and_gradient(x, complex_mode, penalty)
    step = 2e-6
    plus, _ = loss_and_gradient(x + step * direction, complex_mode, penalty)
    minus, _ = loss_and_gradient(x - step * direction, complex_mode, penalty)
    numerical = (plus - minus) / (2 * step)
    analytic = float(np.dot(gradient, direction))
    error = abs(numerical - analytic)
    require(error < 2e-8, f"gradient error {error} in complex={complex_mode}")
    return error


def main() -> None:
    rng = np.random.default_rng(20260808)
    z = rng.normal(scale=0.1, size=SEARCH.PARAMETERS)
    actual, _ = SEARCH.value_gradient(z, need_gradient=False)
    independent = direct_output(z)
    expansion_error = float(np.max(np.abs(actual - independent)))
    require(expansion_error < 1e-13, "matching expansion disagrees")

    t = 0.125
    border = SEARCH.border_point(t)
    border_output, _ = SEARCH.value_gradient(border, need_gradient=False)
    border_residual = border_output - SEARCH.TARGET
    require(np.count_nonzero(np.abs(border_residual) > 1e-14) == 2,
            "the border seed no longer has exactly two residual words")
    require(abs(np.max(np.abs(border_residual)) - t) < 1e-14,
            "the border residual no longer equals t")

    real_error = check_gradient(rng, complex_mode=False)
    complex_error = check_gradient(rng, complex_mode=True)
    print("n=8 full-search sanity checks passed")
    print(f"  expansion max error : {expansion_error:.3g}")
    print(f"  real gradient error : {real_error:.3g}")
    print(f"  complex grad error  : {complex_error:.3g}")
    print("  border residual     : exactly two words of size 0.125")


if __name__ == "__main__":
    main()
