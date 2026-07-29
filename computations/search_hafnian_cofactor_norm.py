#!/usr/bin/env python3
"""Probe the norm cost of killing hafnian cofactors on a one-factor."""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares

from verify_binary_spinflip_cycle_identity import perfect_matchings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--starts", type=int, default=32)
    parser.add_argument("--complex", action="store_true")
    parser.add_argument("--all-subsets", action="store_true")
    args = parser.parse_args()
    n = args.n
    edges = tuple(itertools.combinations(range(n), 2))
    index = {edge: k for k, edge in enumerate(edges)}
    matchings = tuple(perfect_matchings(tuple(range(n))))
    reference = tuple((2 * k, 2 * k + 1) for k in range(n // 2))
    if args.all_subsets:
        constrained_sets = tuple(
            tuple(v for k in subset for v in reference[k])
            for size in range(1, len(reference))
            for subset in itertools.combinations(range(len(reference)), size)
        )
    else:
        constrained_sets = tuple(
            tuple(v for v in range(n) if v not in edge) for edge in reference
        )
    cofactor_families = tuple(
        tuple(perfect_matchings(vertices)) for vertices in constrained_sets
    )
    parameters = len(edges)

    def polynomials(z):
        values = []
        values.append(sum(np.prod([z[index[e]] for e in M]) for M in matchings) - 1)
        for family in cofactor_families:
            values.append(
                sum(np.prod([z[index[e]] for e in M]) for M in family)
            )
        return np.asarray(values)

    def complex_jacobian(z):
        rows = []
        families = (matchings,) + cofactor_families
        for family in families:
            row = np.zeros(parameters, dtype=z.dtype)
            for M in family:
                for position, edge in enumerate(M):
                    value = 1
                    for j, other in enumerate(M):
                        if j != position:
                            value *= z[index[other]]
                    row[index[edge]] += value
            rows.append(row)
        return np.asarray(rows)

    def decode(x):
        if args.complex:
            return x[:parameters] + 1j * x[parameters:]
        return x.astype(complex)

    def residual(x, mu=0):
        value = polynomials(decode(x))
        base = np.r_[value.real, value.imag]
        return np.r_[base, np.sqrt(mu) * x] if mu else base

    def jacobian(x, mu=0):
        value = complex_jacobian(decode(x))
        if args.complex:
            base = np.block([[value.real, -value.imag], [value.imag, value.real]])
        else:
            base = np.vstack((value.real, value.imag))
        return np.vstack((base, np.sqrt(mu) * np.eye(len(x)))) if mu else base

    rng = np.random.default_rng(20260724)
    dimension = 2 * parameters if args.complex else parameters
    for start in range(args.starts):
        x = rng.normal(scale=.6, size=dimension)
        fit = least_squares(
            lambda y: residual(y), x, jac=lambda y: jacobian(y),
            max_nfev=10000, ftol=1e-13, xtol=1e-13, gtol=1e-13,
        )
        if np.max(np.abs(polynomials(decode(fit.x)))) > 1e-7:
            continue
        x = fit.x
        for mu in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8):
            fit = least_squares(
                lambda y, mu=mu: residual(y, mu), x,
                jac=lambda y, mu=mu: jacobian(y, mu),
                max_nfev=10000, ftol=1e-13, xtol=1e-13, gtol=1e-13,
            )
            x = fit.x
        z = decode(x)
        error = np.max(np.abs(polynomials(z)))
        matrix = np.zeros((n, n), dtype=complex)
        for edge, value in zip(edges, z):
            matrix[edge] = value
            matrix[edge[::-1]] = value
        block_energy = []
        for block in reference:
            block_energy.append(
                sum(
                    abs(z[index[tuple(sorted((u, v)))]] ) ** 2
                    for u in block
                    for v in range(n)
                    if v not in block
                )
            )
        print(
            start, "norm2", float(np.vdot(z, z).real), "error", float(error),
            "block", np.round(block_energy, 6),
            "hadamard", float(np.prod(np.asarray(block_energy) / 2) ** .5),
            "det", np.round(np.linalg.det(matrix), 8),
            "largest", np.round(np.sort(np.abs(z))[::-1][:12], 6), flush=True,
        )


if __name__ == "__main__":
    main()
