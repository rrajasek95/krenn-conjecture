#!/usr/bin/env python3
"""Numerically test whether an m-by-m vector permanent can equal GHZ_3."""

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


def tensor_from_vectors(flat: np.ndarray, m: int) -> np.ndarray:
    vectors = flat.reshape(m, m, 3)
    out = np.zeros((3,) * m, dtype=np.result_type(flat, 1.0))
    for perm in itertools.permutations(range(m)):
        term = np.array(1.0)
        for col, row in enumerate(perm):
            term = np.multiply.outer(term, vectors[row, col])
        out += term
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("m", type=int)
    parser.add_argument("--tries", type=int, default=20)
    parser.add_argument("--complex", action="store_true", dest="use_complex")
    args = parser.parse_args()
    target = np.zeros((3,) * args.m)
    for color in range(3):
        target[(color,) * args.m] = 1

    rng = np.random.default_rng(49207)
    best = None
    for trial in range(args.tries):
        nvar = 3 * args.m * args.m
        x0 = rng.normal(scale=0.5, size=nvar * (2 if args.use_complex else 1))

        def residual(x: np.ndarray) -> np.ndarray:
            if args.use_complex:
                z = x[:nvar] + 1j * x[nvar:]
                err = (tensor_from_vectors(z, args.m) - target).ravel()
                return np.concatenate((err.real, err.imag))
            return (tensor_from_vectors(x, args.m) - target).ravel()

        result = least_squares(
            residual,
            x0,
            max_nfev=5000,
            gtol=1e-12,
            ftol=1e-12,
            xtol=1e-12,
        )
        score = np.linalg.norm(result.fun)
        norm = np.linalg.norm(result.x)
        if best is None or score < best[0]:
            best = (score, norm, result.optimality, result.nfev)
        print(trial, score, norm, result.optimality, result.nfev)
    print("best", best)


if __name__ == "__main__":
    main()
