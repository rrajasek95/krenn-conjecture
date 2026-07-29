#!/usr/bin/env python3
"""Numerical search for diagonal q=3 constructions on 2m vertices.

The three full hafnians are normalized identically to one by rescaling the
star at vertex zero.  Only even color-class partitions can contribute.
This is a discovery tool, not a certificate.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


def matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for pos in range(1, len(vertices)):
        second = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1:]
        for tail in matchings(rest):
            yield ((first, second),) + tail


class System:
    def __init__(self, n: int):
        self.n = n
        self.edges = tuple(itertools.combinations(range(n), 2))
        self.edge_index = {edge: k for k, edge in enumerate(self.edges)}
        self.nvar = 3 * len(self.edges)
        self.subsets = tuple(
            tuple(i for i in range(n) if mask >> i & 1)
            for mask in range(1 << n)
            if mask.bit_count() % 2 == 0
        )
        self.subset_matchings = {
            subset: tuple(matchings(subset)) for subset in self.subsets
        }
        self.rows = tuple(
            c for c in itertools.product(range(3), repeat=n)
            if all(c.count(r) % 2 == 0 for r in range(3))
            and len(set(c)) > 1
        )

    def haf_derivative(self, w: np.ndarray, subset: tuple[int, ...]):
        value = 0.0 + 0.0j
        derivative = np.zeros(len(self.edges), dtype=complex)
        for matching in self.subset_matchings[subset]:
            indices = [self.edge_index[tuple(sorted(edge))] for edge in matching]
            factors = w[indices]
            value += np.prod(factors)
            for k, index in enumerate(indices):
                derivative[index] += np.prod(np.delete(factors, k)) if len(indices) > 1 else 1
        return value, derivative

    def complex_residual_jacobian(self, z: np.ndarray):
        weights = z.reshape(3, len(self.edges))
        cache = []
        full = []
        full_d = []
        all_vertices = tuple(range(self.n))
        for color in range(3):
            color_cache = {}
            for subset in self.subsets:
                color_cache[subset] = self.haf_derivative(weights[color], subset)
            cache.append(color_cache)
            full.append(color_cache[all_vertices][0])
            full_d.append(color_cache[all_vertices][1])

        residual = np.zeros(len(self.rows), dtype=complex)
        jacobian = np.zeros((len(self.rows), self.nvar), dtype=complex)
        for row, coloring in enumerate(self.rows):
            subsets = [tuple(i for i, c in enumerate(coloring) if c == r) for r in range(3)]
            values = [cache[r][subsets[r]][0] for r in range(3)]
            derivatives = [cache[r][subsets[r]][1] for r in range(3)]
            base = values[0] * values[1] * values[2]
            anchor_color = coloring[0]
            denominator = full[anchor_color]
            if abs(denominator) < 1e-10:
                denominator = 1e-10
            residual[row] = base / denominator
            for color in range(3):
                offset = color * len(self.edges)
                others = values[(color + 1) % 3] * values[(color + 2) % 3]
                jacobian[row, offset:offset + len(self.edges)] += others * derivatives[color] / denominator
            offset = anchor_color * len(self.edges)
            jacobian[row, offset:offset + len(self.edges)] -= base * full_d[anchor_color] / denominator**2
        return residual, jacobian, np.array(full)

    def unpack(self, x: np.ndarray):
        return x[:self.nvar] + 1j * x[self.nvar:]

    def residual(self, x: np.ndarray):
        r, _, _ = self.complex_residual_jacobian(self.unpack(x))
        return np.concatenate((r.real, r.imag))

    def jacobian(self, x: np.ndarray):
        _, j, _ = self.complex_residual_jacobian(self.unpack(x))
        return np.block([[j.real, -j.imag], [j.imag, j.real]])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=8)
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--max-evaluations", type=int, default=3000)
    parser.add_argument("--bound", type=float, default=20.0)
    args = parser.parse_args()
    system = System(args.n)
    print(f"n={args.n} complex_variables={system.nvar} mixed_even_equations={len(system.rows)}")
    for seed in range(args.starts):
        rng = np.random.default_rng(seed)
        z0 = rng.normal(scale=.35, size=system.nvar) + 1j*rng.normal(scale=.35, size=system.nvar)
        x0 = np.concatenate((z0.real, z0.imag))
        fit = least_squares(
            system.residual, x0, jac=system.jacobian,
            bounds=(-args.bound, args.bound), max_nfev=args.max_evaluations,
            ftol=1e-13, xtol=1e-13, gtol=1e-13, tr_solver="lsmr"
        )
        r, _, full = system.complex_residual_jacobian(system.unpack(fit.x))
        print(f"seed={seed} max_mixed={np.max(np.abs(r)):.6g} cost={fit.cost:.6g} "
              f"raw_full={full} norm={np.linalg.norm(fit.x):.6g} nfev={fit.nfev}")
        if np.max(np.abs(r)) < 1e-8 and np.min(np.abs(full)) > 1e-8:
            np.savez(f"candidate_diagonal_n{args.n}_seed{seed}.npz", raw=system.unpack(fit.x), full=full)


if __name__ == "__main__":
    main()
