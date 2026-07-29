#!/usr/bin/env python3
"""Numerical search in the F_2^3-translation-invariant n=8 slice.

Vertices are the eight vectors of F_2^3, encoded by integers 0,...,7.
The block on {u,v} depends only on d=u xor v.  Translation by d swaps
the endpoints, so each of the seven blocks is an arbitrary symmetric 3x3
matrix.  This is a discovery search only; any candidate needs exact
recognition and an independent coefficient audit.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import minimize


N, Q = 8, 3
EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {edge: i for i, edge in enumerate(EDGES)}
COLORS = np.asarray(list(itertools.product(range(Q), repeat=N)), dtype=np.int8)
TARGET = np.asarray([len(set(word)) == 1 for word in COLORS], dtype=float)
SYMMETRIC = tuple((a, b) for a in range(Q) for b in range(a, Q))
PARAMETERS = 7 * len(SYMMETRIC)


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for k in range(1, len(vertices)):
        v = vertices[k]
        rest = vertices[1:k] + vertices[k + 1:]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


MATCHINGS = tuple(perfect_matchings(tuple(range(N))))


def expand(parameters):
    blocks = np.zeros((8, Q, Q), dtype=parameters.dtype)
    for difference in range(1, 8):
        offset = (difference - 1) * len(SYMMETRIC)
        for value, (a, b) in zip(
            parameters[offset:offset + len(SYMMETRIC)], SYMMETRIC
        ):
            blocks[difference, a, b] = value
            blocks[difference, b, a] = value
    return np.asarray([blocks[u ^ v] for u, v in EDGES])


def collapse(full_gradient):
    answer = np.zeros(PARAMETERS, dtype=full_gradient.dtype)
    for edge_number, (u, v) in enumerate(EDGES):
        offset = ((u ^ v) - 1) * len(SYMMETRIC)
        block = full_gradient[edge_number]
        for k, (a, b) in enumerate(SYMMETRIC):
            answer[offset + k] += block[a, b]
            if a != b:
                answer[offset + k] += block[b, a]
    return answer


def value_gradient(parameters, need_gradient=True):
    matrices = expand(parameters)
    output = np.zeros(len(COLORS), dtype=parameters.dtype)
    cache = []
    for matching in MATCHINGS:
        values, slots = [], []
        for u, v in matching:
            edge_number = EDGE_INDEX[u, v]
            aa, bb = COLORS[:, u], COLORS[:, v]
            values.append(matrices[edge_number, aa, bb])
            slots.append((edge_number, aa, bb))
        output += np.prod(values, axis=0)
        if need_gradient:
            cache.append((values, slots))
    residual = output - TARGET
    loss = 0.5 * float(np.vdot(residual, residual).real)
    if not need_gradient:
        return loss, output
    full_gradient = np.zeros_like(matrices)
    for values, slots in cache:
        for k, (edge_number, aa, bb) in enumerate(slots):
            derivative = np.ones(len(COLORS), dtype=parameters.dtype)
            for ell, value in enumerate(values):
                if ell != k:
                    derivative *= value
            np.add.at(
                full_gradient[edge_number],
                (aa, bb),
                np.conjugate(residual) * derivative,
            )
    return loss, output, collapse(full_gradient)


def run(seed, complex_search, maxiter):
    rng = np.random.default_rng(seed)
    if complex_search:
        initial = rng.normal(scale=0.4, size=2 * PARAMETERS)

        def decode(vector):
            return vector[:PARAMETERS] + 1j * vector[PARAMETERS:]

        def objective(vector):
            loss, _output, gradient = value_gradient(decode(vector))
            return loss, np.r_[gradient.real, -gradient.imag]
    else:
        initial = rng.normal(scale=0.4, size=PARAMETERS)
        decode = lambda vector: vector

        def objective(vector):
            loss, _output, gradient = value_gradient(vector)
            return loss, gradient.real

    result = minimize(
        objective,
        initial,
        method="L-BFGS-B",
        jac=True,
        options={"maxiter": maxiter, "ftol": 1e-15, "gtol": 1e-11, "maxls": 50},
    )
    parameters = decode(result.x)
    loss, output = value_gradient(parameters, False)
    residual = output - TARGET
    maximum = float(np.max(np.abs(residual)))
    print(
        f"seed={seed} nit={result.nit} loss={loss:.12g} "
        f"max={maximum:.6g} norm={np.linalg.norm(parameters):.6g}",
        flush=True,
    )
    if maximum < 1e-7:
        np.savez(
            f"candidate_f2cube_n8_seed{seed}.npz",
            parameters=parameters,
            matrices=expand(parameters),
            residual=residual,
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starts", type=int, default=1)
    parser.add_argument("--maxiter", type=int, default=1000)
    parser.add_argument("--complex", action="store_true", dest="complex_search")
    args = parser.parse_args()
    for seed in range(args.seed, args.seed + args.starts):
        run(seed, args.complex_search, args.maxiter)


if __name__ == "__main__":
    main()
