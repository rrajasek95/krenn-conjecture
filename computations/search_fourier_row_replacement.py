#!/usr/bin/env python3
"""Numerically test the one-shore MOD_3 row-replacement problem.

For m base pairs, search matrices B,D with B upper triangular and

  per(matrix with rows I from D and other rows from B) = 1[|I| = 0 mod 3].

Upper-triangular B has a unique supported base permutation when its diagonal
is nonzero.  Thus a finite solution falsifies any attempted extension of the
isolated-vacuum tournament proof to merely unique base perfect matchings.
This script is a discovery tool, not a certificate.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


def permanent(matrix):
    n = len(matrix)
    answer = 0
    for permutation in itertools.permutations(range(n)):
        term = 1
        for i, j in enumerate(permutation):
            term *= matrix[i, j]
        answer += term
    return answer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("m", type=int, default=4)
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--max-nfev", type=int, default=10000)
    parser.add_argument("--fixed-unit-upper", action="store_true")
    parser.add_argument("--fixed-long-chord", action="store_true")
    parser.add_argument("--upper-bandwidth", type=int)
    args = parser.parse_args()
    m = args.m
    upper = tuple(
        (i, j)
        for i in range(m)
        for j in range(i, m)
        if args.upper_bandwidth is None or j - i <= args.upper_bandwidth
    )
    subsets = tuple(
        subset
        for size in range(m + 1)
        for subset in itertools.combinations(range(m), size)
    )
    fixed_b = args.fixed_unit_upper or args.fixed_long_chord
    p = m * m if fixed_b else len(upper) + m * m

    def decode(z):
        if fixed_b:
            if args.fixed_unit_upper:
                b = np.triu(np.ones((m, m), dtype=z.dtype))
            else:
                b = np.eye(m, dtype=z.dtype)
                b[0, m - 1] = 1
            d = z.reshape(m, m)
        else:
            b = np.zeros((m, m), dtype=z.dtype)
            for value, (i, j) in zip(z[: len(upper)], upper):
                b[i, j] = value
            d = z[len(upper) :].reshape(m, m)
        return b, d

    def values(z):
        b, d = decode(z)
        answer = []
        for subset in subsets:
            chosen = set(subset)
            matrix = np.asarray([d[i] if i in chosen else b[i] for i in range(m)])
            answer.append(permanent(matrix))
        return np.asarray(answer)

    target = np.asarray([float(len(subset) % 3 == 0) for subset in subsets])
    rng = np.random.default_rng(args.seed)
    for start in range(args.starts):
        initial = rng.normal(scale=0.4, size=2 * p)

        def unpack(x):
            return x[:p] + 1j * x[p:]

        def residual(x):
            value = values(unpack(x)) - target
            return np.r_[value.real, value.imag]

        fit = least_squares(
            residual,
            initial,
            max_nfev=args.max_nfev,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
        )
        raw = values(unpack(fit.x)) - target
        b, _ = decode(unpack(fit.x))
        print(
            f"start={start} cost={fit.cost:.6g} max={np.max(np.abs(raw)):.4g} "
            f"norm={np.linalg.norm(fit.x):.4g} min_diag={np.min(np.abs(np.diag(b))):.4g}",
            flush=True,
        )
        if np.max(np.abs(raw)) < 1e-7 and np.min(np.abs(np.diag(b))) > 1e-5:
            np.savez(
                f"candidate_fourier_rows_m{m}_seed{start}.npz",
                B=b,
                D=decode(unpack(fit.x))[1],
                residual=raw,
            )


if __name__ == "__main__":
    main()
