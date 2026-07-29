#!/usr/bin/env python3
"""Numerical probe of the two-K4 chart with eight prescribed zero blocks.

This is a discovery script only.  A small residual must be reconstructed
and checked exactly before it has mathematical force.
"""

from __future__ import annotations

import argparse

import numpy as np
from scipy.optimize import least_squares

import search_two_k4_composition as base


def positions(encoded: str) -> frozenset[tuple[int, int]]:
    return frozenset((int(cell[0]), int(cell[1]) + 4) for cell in encoded.split())


MASKS = {
    "c8": frozenset(
        {(0, 4), (0, 5), (1, 5), (1, 6),
         (2, 6), (2, 7), (3, 7), (3, 4)}
    ),
    "c4c4": frozenset(
        {(0, 4), (0, 5), (1, 4), (1, 5),
         (2, 6), (2, 7), (3, 6), (3, 7)}
    ),
    # The remaining eight S_4 x S_4 x C_2 position orbits surviving all
    # exact-seven erasure consequences.  Names record their orbit sizes;
    # a/b disambiguate equal-size orbits.  Columns are shifted to 4,...,7.
    "o288a": positions("00 01 02 10 11 20 22 33"),
    "o576a": positions("00 01 02 10 11 20 23 32"),
    "o1152": positions("00 01 02 10 11 20 23 33"),
    "o576b": positions("00 01 02 10 11 22 23 32"),
    "o576c": positions("00 01 02 10 13 20 31 33"),
    "o288b": positions("00 01 02 10 13 21 23 33"),
    "o576d": positions("00 01 02 10 11 22 23 33"),
    "o576e": positions("00 01 02 10 13 21 23 32"),
}


def run(mask_name: str, seed: int, max_nfev: int, complex_search: bool) -> None:
    zero_edges = MASKS[mask_name]
    live_edges = tuple(edge for edge in base.CROSS if edge not in zero_edges)
    live_index = {edge: k for k, edge in enumerate(live_edges)}
    parameter_count = len(live_edges) * base.Q * base.Q

    def unpack(z: np.ndarray) -> np.ndarray:
        return z.reshape(len(live_edges), base.Q, base.Q)

    def edge_values(matrices: np.ndarray, edge: tuple[int, int]) -> np.ndarray:
        u, v = edge
        if u < 4 <= v:
            if edge in zero_edges:
                return np.zeros(len(base.COLORINGS), dtype=matrices.dtype)
            return matrices[
                live_index[edge], base.COLORINGS[:, u], base.COLORINGS[:, v]
            ]
        colour = base.internal_colour(u, v)
        return (
            (base.COLORINGS[:, u] == colour)
            & (base.COLORINGS[:, v] == colour)
        ).astype(matrices.dtype)

    def amplitudes(z: np.ndarray) -> np.ndarray:
        matrices = unpack(z)
        answer = np.zeros(len(base.COLORINGS), dtype=z.dtype)
        for matching in base.MATCHINGS:
            term = np.ones(len(base.COLORINGS), dtype=z.dtype)
            for edge in matching:
                term *= edge_values(matrices, edge)
            answer += term
        return answer

    def derivative(z: np.ndarray) -> np.ndarray:
        matrices = unpack(z)
        jac = np.zeros((len(base.COLORINGS), parameter_count), dtype=z.dtype)
        for matching in base.MATCHINGS:
            values = [edge_values(matrices, edge) for edge in matching]
            for position, edge in enumerate(matching):
                if edge not in live_index:
                    continue
                product_value = np.ones(len(base.COLORINGS), dtype=z.dtype)
                for other, value in enumerate(values):
                    if other != position:
                        product_value *= value
                local = (
                    base.COLORINGS[:, edge[0]].astype(np.int32) * base.Q
                    + base.COLORINGS[:, edge[1]].astype(np.int32)
                )
                columns = live_index[edge] * base.Q * base.Q + local
                np.add.at(jac, (base.ROWS, columns), product_value)
        return jac

    rng = np.random.default_rng(seed)
    if complex_search:
        initial = rng.normal(scale=0.4, size=2 * parameter_count)

        def decode(xx: np.ndarray) -> np.ndarray:
            return xx[:parameter_count] + 1j * xx[parameter_count:]

        def residual(xx: np.ndarray) -> np.ndarray:
            value = amplitudes(decode(xx)) - base.TARGET
            return np.r_[value.real, value.imag]

        def jacobian(xx: np.ndarray) -> np.ndarray:
            value = derivative(decode(xx))
            return np.block([[value.real, -value.imag], [value.imag, value.real]])

    else:
        initial = rng.normal(scale=0.4, size=parameter_count)
        decode = lambda xx: xx
        residual = lambda xx: amplitudes(xx) - base.TARGET
        jacobian = derivative

    fit = least_squares(
        residual,
        initial,
        jac=jacobian,
        max_nfev=max_nfev,
        ftol=1e-13,
        xtol=1e-13,
        gtol=1e-13,
        verbose=0,
    )
    z = decode(fit.x)
    raw = amplitudes(z) - base.TARGET
    maximum = float(np.max(np.abs(raw)))
    print(
        f"mask={mask_name} seed={seed} cost={fit.cost:.10g} "
        f"max={maximum:.6g} norm={np.linalg.norm(z):.6g} nfev={fit.nfev}",
        flush=True,
    )
    if maximum < 1e-8 and np.linalg.norm(z) < 1e6:
        np.savez(
            f"computations/candidate_two_k4_{mask_name}_{seed}.npz",
            live_edges=np.asarray(live_edges),
            matrices=unpack(z),
            residual=raw,
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mask", choices=tuple(MASKS), default="c8")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starts", type=int, default=1)
    parser.add_argument("--max-nfev", type=int, default=1000)
    parser.add_argument("--complex", action="store_true", dest="complex_search")
    args = parser.parse_args()
    for seed in range(args.seed, args.seed + args.starts):
        run(args.mask, seed, args.max_nfev, args.complex_search)


if __name__ == "__main__":
    main()
