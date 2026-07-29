#!/usr/bin/env python3
"""Numerical discovery for the Boolean Fourier shadow of a q=3 source.

After Fourier transforming every color mode and retaining charges 0 and 1,
an exact q=3 realization would give

    haf(A_uv(s_u,s_v)) = 1[sum_v s_v == 0 (mod 3)].

This script searches the larger problem in which every unordered vertex pair
has an arbitrary 2 by 2 covariance block.  It is only a falsification and
candidate-discovery tool; small floating residuals are not certificates.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


class System:
    def __init__(self, n: int):
        self.n = n
        self.edges = tuple(itertools.combinations(range(n), 2))
        self.edge_index = {edge: index for index, edge in enumerate(self.edges)}
        self.matchings = tuple(perfect_matchings(tuple(range(n))))
        self.states = np.asarray(
            tuple(itertools.product(range(2), repeat=n)), dtype=np.int8
        )
        self.target = np.asarray(
            [float(sum(state) % 3 == 0) for state in self.states]
        )
        self.parameter_count = 4 * len(self.edges)

    def edge_entries(self, matrices, edge):
        u, v = edge
        return matrices[
            self.edge_index[edge], self.states[:, u], self.states[:, v]
        ]

    def amplitudes(self, z):
        matrices = z.reshape(len(self.edges), 2, 2)
        answer = np.zeros(len(self.states), dtype=z.dtype)
        for matching in self.matchings:
            term = np.ones(len(self.states), dtype=z.dtype)
            for edge in matching:
                term *= self.edge_entries(matrices, edge)
            answer += term
        return answer

    def jacobian(self, z):
        matrices = z.reshape(len(self.edges), 2, 2)
        answer = np.zeros(
            (len(self.states), self.parameter_count), dtype=z.dtype
        )
        rows = np.arange(len(self.states))
        for matching in self.matchings:
            values = [self.edge_entries(matrices, edge) for edge in matching]
            for position, edge in enumerate(matching):
                derivative = np.ones(len(self.states), dtype=z.dtype)
                for other_position, value in enumerate(values):
                    if position != other_position:
                        derivative *= value
                u, v = edge
                local = 2 * self.states[:, u] + self.states[:, v]
                columns = 4 * self.edge_index[edge] + local
                np.add.at(answer, (rows, columns), derivative)
        return answer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--scale", type=float, default=0.3)
    parser.add_argument("--max-nfev", type=int, default=5000)
    parser.add_argument("--real", action="store_true")
    args = parser.parse_args()
    if args.n % 2:
        raise SystemExit("n must be even")

    system = System(args.n)
    rng = np.random.default_rng(args.seed)
    p = system.parameter_count
    print(
        f"n={args.n} variables={p} outputs={len(system.states)} "
        f"matchings={len(system.matchings)}",
        flush=True,
    )
    for offset in range(args.starts):
        initial = rng.normal(
            scale=args.scale, size=p if args.real else 2 * p
        )

        if args.real:
            decode = lambda x: x

            def residual(x):
                return system.amplitudes(x) - system.target

            jacobian = system.jacobian
        else:
            decode = lambda x: x[:p] + 1j * x[p:]

            def residual(x):
                value = system.amplitudes(decode(x)) - system.target
                return np.r_[value.real, value.imag]

            def jacobian(x):
                value = system.jacobian(decode(x))
                return np.block(
                    [[value.real, -value.imag], [value.imag, value.real]]
                )

        fit = least_squares(
            residual,
            initial,
            jac=jacobian,
            max_nfev=args.max_nfev,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
        )
        raw = system.amplitudes(decode(fit.x)) - system.target
        print(
            f"start={args.seed + offset} cost={fit.cost:.12g} "
            f"max={np.max(np.abs(raw)):.6g} norm={np.linalg.norm(fit.x):.6g} "
            f"optimality={fit.optimality:.3g} nfev={fit.nfev}",
            flush=True,
        )
        if np.max(np.abs(raw)) < 1e-5:
            kind = "real" if args.real else "complex"
            np.savez(
                f"candidate_fourier_binary_n{args.n}_{kind}_seed{args.seed + offset}.npz",
                matrices=decode(fit.x).reshape(len(system.edges), 2, 2),
                residual=raw,
            )


if __name__ == "__main__":
    main()
