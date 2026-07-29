#!/usr/bin/env python3
"""Discovery search for a diagonal K_{m,m} realization of GHZ_3.

For each color r there is an m by m scalar matrix C[r].  A balanced
coloring contributes the product of the permanents of the three induced
color blocks.  This script is numerical only; any candidate must later be
made exact.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


def permutations(k: int) -> tuple[tuple[int, ...], ...]:
    return tuple(itertools.permutations(range(k)))


def permanent_and_derivative(a: np.ndarray) -> tuple[complex, np.ndarray]:
    """Return per(a) and its entry derivatives, for a square small matrix."""
    k = a.shape[0]
    if k == 0:
        return 1.0 + 0.0j, np.zeros((0, 0), dtype=complex)
    value = 0.0 + 0.0j
    derivative = np.zeros_like(a, dtype=complex)
    for sigma in permutations(k):
        factors = np.array([a[i, sigma[i]] for i in range(k)], dtype=complex)
        value += np.prod(factors)
        for i in range(k):
            if k == 1:
                derivative[i, sigma[i]] += 1
            else:
                derivative[i, sigma[i]] += np.prod(np.delete(factors, i))
    return value, derivative


class System:
    def __init__(self, m: int):
        self.m = m
        self.nvar = 3 * m * m
        self.rows: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
        for left in itertools.product(range(3), repeat=m):
            counts = tuple(left.count(r) for r in range(3))
            for right in itertools.product(range(3), repeat=m):
                if tuple(right.count(r) for r in range(3)) == counts:
                    self.rows.append((left, right))

    def complex_residual_jacobian(self, z: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        c = z.reshape(3, self.m, self.m)
        residual = np.zeros(len(self.rows), dtype=complex)
        jacobian = np.zeros((len(self.rows), self.nvar), dtype=complex)
        for row, (left, right) in enumerate(self.rows):
            values: list[complex] = []
            derivatives: list[tuple[np.ndarray, tuple[int, ...], tuple[int, ...]]] = []
            for color in range(3):
                rr = tuple(i for i, x in enumerate(left) if x == color)
                cc = tuple(j for j, x in enumerate(right) if x == color)
                block = c[color][np.ix_(rr, cc)]
                value, derivative = permanent_and_derivative(block)
                values.append(value)
                derivatives.append((derivative, rr, cc))
            actual = np.prod(values)
            expected = complex(all(x == left[0] for x in left) and left == right)
            residual[row] = actual - expected
            for color, (derivative, rr, cc) in enumerate(derivatives):
                other = values[(color + 1) % 3] * values[(color + 2) % 3]
                for ii, i in enumerate(rr):
                    for jj, j in enumerate(cc):
                        column = color * self.m * self.m + i * self.m + j
                        jacobian[row, column] = other * derivative[ii, jj]
        return residual, jacobian

    def unpack(self, x: np.ndarray) -> np.ndarray:
        return x[: self.nvar] + 1j * x[self.nvar :]

    def normalize(self, z: np.ndarray) -> np.ndarray:
        c = z.reshape(3, self.m, self.m).copy()
        for color in range(3):
            value, _ = permanent_and_derivative(c[color])
            if abs(value) < 1e-12:
                value = 1e-12
            c[color, 0, :] /= value
        return c.reshape(-1)

    def residual(self, x: np.ndarray) -> np.ndarray:
        r, _ = self.complex_residual_jacobian(self.unpack(x))
        return np.concatenate((r.real, r.imag))

    def jacobian(self, x: np.ndarray) -> np.ndarray:
        _, j = self.complex_residual_jacobian(self.unpack(x))
        return np.block([[j.real, -j.imag], [j.imag, j.real]])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m", type=int, default=4)
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--max-evaluations", type=int, default=3000)
    parser.add_argument("--bound", type=float, default=20.0)
    parser.add_argument("--permutation-start", action="store_true")
    parser.add_argument("--normalize", action="store_true")
    args = parser.parse_args()

    system = System(args.m)
    print(f"m={args.m} complex_variables={system.nvar} equations={len(system.rows)}")
    for seed in range(args.starts):
        rng = np.random.default_rng(seed)
        z0 = rng.normal(scale=0.08 if args.permutation_start else 0.35,
                        size=system.nvar) + 1j * rng.normal(
            scale=0.08 if args.permutation_start else 0.35,
            size=system.nvar
        )
        if args.permutation_start:
            z0 = z0.reshape(3, args.m, args.m)
            for color in range(3):
                sigma = rng.permutation(args.m)
                z0[color, np.arange(args.m), sigma] += 1
            z0 = z0.reshape(-1)
        x0 = np.concatenate((z0.real, z0.imag))
        residual_function = system.residual
        jacobian_function: object = system.jacobian
        if args.normalize:
            def residual_function(x: np.ndarray) -> np.ndarray:
                z = system.normalize(system.unpack(x))
                r, _ = system.complex_residual_jacobian(z)
                # The three constant equations are identically normalized.
                return np.concatenate((r.real, r.imag))
            jacobian_function = "2-point"
        result = least_squares(
            residual_function,
            x0,
            jac=jacobian_function,
            bounds=(-args.bound, args.bound),
            max_nfev=args.max_evaluations,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
            tr_solver="lsmr",
            verbose=0,
        )
        r = residual_function(result.x)
        z = system.unpack(result.x)
        if args.normalize:
            z = system.normalize(z)
        print(
            f"seed={seed} max_abs={np.max(np.abs(r)):.6g} "
            f"norm={np.linalg.norm(z):.6g} cost={result.cost:.6g} "
            f"optimality={result.optimality:.3g} nfev={result.nfev}"
        )
        if np.max(np.abs(r)) < 1e-8 and np.linalg.norm(z) < args.bound:
            np.savez(f"candidate_bipartite_m{args.m}_seed{seed}.npz", matrices=z)


if __name__ == "__main__":
    main()
