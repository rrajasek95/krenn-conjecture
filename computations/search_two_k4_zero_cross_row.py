#!/usr/bin/env python3
"""Numerical probe of the full-zero-row two-K4 boundary.

This is discovery code only.  The four blocks B[0,j] are fixed to zero;
the twelve blocks B[i,j], i=1,2,3, are arbitrary complex 3 by 3 matrices.
The residual is evaluated through the equivalent three overlapping
six-site purity equations, which is much smaller than all 3^8 outputs.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product

import numpy as np
from scipy.optimize import least_squares


Q = 3
LEFT = (1, 2, 3)
RIGHT = (0, 1, 2, 3)
BLOCKS = tuple(product(LEFT, RIGHT))
BLOCK_INDEX = {block: index for index, block in enumerate(BLOCKS)}
WORDS = np.asarray(tuple(product(range(Q), repeat=6)), dtype=np.int8)
ROWS = np.arange(len(WORDS))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings(range(6)))


def internal_colour(u, v):
    return (1, 2, 3).index(u ^ v)


def pair_residual_and_jacobian(z, left_pair, colour, need_jacobian=True):
    """Matching tensor on (left_pair)+(right K4), minus e_colour^6."""

    matrices = z.reshape(len(BLOCKS), Q, Q)
    answer = np.zeros(len(WORDS), dtype=z.dtype)
    jacobian = (
        np.zeros((len(WORDS), z.size), dtype=z.dtype)
        if need_jacobian
        else None
    )

    # Local vertices 0,1 are the chosen left pair; 2,...,5 are right 0,...,3.
    for matching in MATCHINGS:
        values = []
        slots = []
        valid = True
        for u, v in matching:
            if u < 2 and v < 2:
                edge_colour = colour
                value = (
                    (WORDS[:, u] == edge_colour)
                    & (WORDS[:, v] == edge_colour)
                ).astype(z.dtype)
                slot = None
            elif u >= 2 and v >= 2:
                edge_colour = internal_colour(u - 2, v - 2)
                value = (
                    (WORDS[:, u] == edge_colour)
                    & (WORDS[:, v] == edge_colour)
                ).astype(z.dtype)
                slot = None
            elif u < 2 <= v:
                left = left_pair[u]
                right = v - 2
                aa, bb = WORDS[:, u], WORDS[:, v]
                block_number = BLOCK_INDEX[(left, right)]
                value = matrices[block_number, aa, bb]
                slot = (block_number, aa, bb)
            else:
                # The recursive matching order should never orient this way.
                valid = False
                break
            values.append(value)
            slots.append(slot)
        if not valid:
            continue
        answer += np.prod(values, axis=0)
        if jacobian is not None:
            for position, slot in enumerate(slots):
                if slot is None:
                    continue
                derivative = np.ones(len(WORDS), dtype=z.dtype)
                for other, value in enumerate(values):
                    if other != position:
                        derivative *= value
                block_number, aa, bb = slot
                columns = block_number * Q * Q + aa * Q + bb
                np.add.at(jacobian, (ROWS, columns), derivative)

    target = np.all(WORDS == colour, axis=1).astype(z.dtype)
    return answer - target, jacobian


PAIRS = (((2, 3), 0), ((1, 3), 1), ((1, 2), 2))


def residual_and_jacobian(z, need_jacobian=True):
    pieces = [
        pair_residual_and_jacobian(z, pair, colour, need_jacobian)
        for pair, colour in PAIRS
    ]
    residual = np.concatenate([piece[0] for piece in pieces])
    jacobian = (
        np.concatenate([piece[1] for piece in pieces], axis=0)
        if need_jacobian
        else None
    )
    return residual, jacobian


def run(seed, max_nfev, scale, complex_search):
    rng = np.random.default_rng(seed)
    parameter_count = len(BLOCKS) * Q * Q
    if complex_search:
        initial = rng.normal(scale=scale, size=2 * parameter_count)

        def decode(x):
            return x[:parameter_count] + 1j * x[parameter_count:]

        def residual(x):
            value, _ = residual_and_jacobian(decode(x), False)
            return np.r_[value.real, value.imag]

        def jacobian(x):
            _, value = residual_and_jacobian(decode(x), True)
            return np.block([[value.real, -value.imag], [value.imag, value.real]])
    else:
        initial = rng.normal(scale=scale, size=parameter_count)
        decode = lambda x: x
        residual = lambda x: residual_and_jacobian(x, False)[0]
        jacobian = lambda x: residual_and_jacobian(x, True)[1]

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
    decoded = decode(fit.x)
    raw, _ = residual_and_jacobian(decoded, False)
    print(
        f"seed={seed} cost={fit.cost:.12g} max={np.max(np.abs(raw)):.7g} "
        f"norm={np.linalg.norm(decoded):.7g} nfev={fit.nfev}",
        flush=True,
    )
    if np.max(np.abs(raw)) < 1e-8 and np.linalg.norm(decoded) < 1e5:
        np.savez(
            f"computations/candidate_two_k4_zero_row_seed{seed}.npz",
            blocks=np.asarray(BLOCKS),
            matrices=decoded.reshape(len(BLOCKS), Q, Q),
            residual=raw,
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starts", type=int, default=1)
    parser.add_argument("--max-nfev", type=int, default=2000)
    parser.add_argument("--scale", type=float, default=0.3)
    parser.add_argument("--complex", action="store_true", dest="complex_search")
    args = parser.parse_args()
    for seed in range(args.seed, args.seed + args.starts):
        run(seed, args.max_nfev, args.scale, args.complex_search)


if __name__ == "__main__":
    main()
