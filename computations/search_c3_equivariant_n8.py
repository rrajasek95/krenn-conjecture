#!/usr/bin/env python3
"""Numerical n=8 search equivariant under a joint order-three symmetry.

The vertex permutation is (0 1 2)(3 4 5), fixing 6 and 7, and is coupled
to the cyclic permutation of the three colors.  This forces the three
constant coefficients to agree while retaining 84 complex parameters.
Numerical output is only for discovery and requires exact certification.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares, minimize


N, Q = 8, 3
EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {e: i for i, e in enumerate(EDGES)}
COLORS = np.asarray(list(itertools.product(range(Q), repeat=N)), dtype=np.int8)
TARGET = np.asarray([len(set(c)) == 1 for c in COLORS], dtype=float)
G = (1, 2, 0, 4, 5, 3, 6, 7)


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for k in range(1, len(vertices)):
        v = vertices[k]
        rest = vertices[1:k] + vertices[k + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


MATCHINGS = tuple(perfect_matchings(tuple(range(N))))


def edge_image(edge):
    u, v = G[edge[0]], G[edge[1]]
    return (min(u, v), max(u, v)), u > v


def edge_orbits():
    unseen = set(EDGES)
    answer = []
    while unseen:
        start = min(unseen)
        orbit = []
        edge, reversed_orientation = start, False
        for power in range(3):
            orbit.append((edge, power, reversed_orientation))
            unseen.discard(edge)
            edge, flipped = edge_image(edge)
            reversed_orientation ^= flipped
        # Fixed edge 67 appears three times; every other orbit has length 3.
        unique = []
        seen = set()
        for item in orbit:
            if item[0] not in seen:
                unique.append(item)
                seen.add(item[0])
        answer.append(tuple(unique))
    return tuple(answer)


ORBITS = edge_orbits()
FIXED = tuple(k for k, orbit in enumerate(ORBITS) if len(orbit) == 1)
assert len(ORBITS) == 10 and len(FIXED) == 1 and ORBITS[FIXED[0]][0][0] == (6, 7)
PARAMETERS = 9 * (len(ORBITS) - 1) + 3


def shift_matrix(base, power, transpose):
    result = np.empty_like(base)
    for a in range(Q):
        for b in range(Q):
            result[(a + power) % Q, (b + power) % Q] = base[a, b]
    return result.T if transpose else result


def expand(z):
    matrices = np.zeros((len(EDGES), Q, Q), dtype=z.dtype)
    position = 0
    for orbit in ORBITS:
        if len(orbit) == 1:
            values = z[position:position + 3]
            position += 3
            base = np.asarray([[values[(b - a) % Q] for b in range(Q)]
                               for a in range(Q)])
        else:
            base = z[position:position + 9].reshape(Q, Q)
            position += 9
        for edge, power, transpose in orbit:
            matrices[EDGE_INDEX[edge]] = shift_matrix(base, power, transpose)
    assert position == PARAMETERS
    return matrices


def unshift_gradient(block, power, transpose):
    if transpose:
        block = block.T
    result = np.empty_like(block)
    for a in range(Q):
        for b in range(Q):
            result[a, b] = block[(a + power) % Q, (b + power) % Q]
    return result


def collapse(g):
    answer = np.zeros(PARAMETERS, dtype=g.dtype)
    position = 0
    for orbit in ORBITS:
        total = np.zeros((Q, Q), dtype=g.dtype)
        for edge, power, transpose in orbit:
            total += unshift_gradient(g[EDGE_INDEX[edge]], power, transpose)
        if len(orbit) == 1:
            for a in range(Q):
                for b in range(Q):
                    answer[position + (b - a) % Q] += total[a, b]
            position += 3
        else:
            answer[position:position + 9] = total.reshape(-1)
            position += 9
    return answer


def value_gradient(z, need_gradient=True):
    matrices = expand(z)
    output = np.zeros(len(COLORS), dtype=z.dtype)
    cache = []
    for matching in MATCHINGS:
        values, slots = [], []
        for u, v in matching:
            e = EDGE_INDEX[u, v]
            a, b = COLORS[:, u], COLORS[:, v]
            values.append(matrices[e, a, b])
            slots.append((e, a, b))
        output += np.prod(values, axis=0)
        if need_gradient:
            cache.append((values, slots))
    residual = output - TARGET
    loss = 0.5 * float(np.vdot(residual, residual).real)
    if not need_gradient:
        return loss, output
    full_gradient = np.zeros_like(matrices)
    for values, slots in cache:
        for k, (edge, aa, bb) in enumerate(slots):
            derivative = np.ones(len(COLORS), dtype=z.dtype)
            for ell, value in enumerate(values):
                if ell != k:
                    derivative *= value
            np.add.at(full_gradient[edge], (aa, bb),
                      np.conjugate(residual) * derivative)
    return loss, output, collapse(full_gradient)


def output_jacobian(z):
    matrices = expand(z)
    output = np.zeros(len(COLORS), dtype=z.dtype)
    full = np.zeros((len(COLORS), len(EDGES), Q, Q), dtype=z.dtype)
    rows = np.arange(len(COLORS))
    for matching in MATCHINGS:
        values, slots = [], []
        for u, v in matching:
            e = EDGE_INDEX[u, v]
            a, b = COLORS[:, u], COLORS[:, v]
            values.append(matrices[e, a, b])
            slots.append((e, a, b))
        output += np.prod(values, axis=0)
        for k, (edge, aa, bb) in enumerate(slots):
            derivative = np.ones(len(COLORS), dtype=z.dtype)
            for ell, value in enumerate(values):
                if ell != k:
                    derivative *= value
            np.add.at(full, (rows, edge, aa, bb), derivative)
    jac = np.zeros((len(COLORS), PARAMETERS), dtype=z.dtype)
    for row in range(len(COLORS)):
        jac[row] = collapse(full[row])
    return output, jac


def run(seed, complex_search, maxiter, use_least_squares, normalize_target):
    rng = np.random.default_rng(seed)
    if complex_search:
        x0 = rng.normal(scale=0.35, size=2 * PARAMETERS)

        def decode(x):
            return x[:PARAMETERS] + 1j * x[PARAMETERS:]

        def objective(x):
            if normalize_target:
                output, jac = output_jacobian(decode(x))
                h = output[0]
                if abs(h) < 1e-10:
                    return 1e20, np.zeros_like(x)
                q = output / h - TARGET
                loss = 0.5 * float(np.vdot(q, q).real)
                w = np.conjugate(q) / h
                w[0] -= np.sum(np.conjugate(q) * output) / (h * h)
                g = w @ jac
            else:
                loss, _output, g = value_gradient(decode(x))
            return loss, np.r_[g.real, -g.imag]
    else:
        x0 = rng.normal(scale=0.35, size=PARAMETERS)
        decode = lambda x: x

        def objective(x):
            if normalize_target:
                output, jac = output_jacobian(x)
                h = output[0]
                if abs(h) < 1e-10:
                    return 1e20, np.zeros_like(x)
                q = output / h - TARGET
                loss = 0.5 * float(np.dot(q, q))
                w = q / h
                w[0] -= np.dot(q, output) / (h * h)
                g = w @ jac
            else:
                loss, _output, g = value_gradient(x)
            return loss, g.real
    if use_least_squares:
        if complex_search:
            def residual_function(x):
                value, _jac = output_jacobian(decode(x))
                if normalize_target:
                    value = value / value[0]
                r = value - TARGET
                return np.r_[r.real, r.imag]

            def jacobian_function(x):
                value, jac = output_jacobian(decode(x))
                if normalize_target:
                    h = value[0]
                    jac = jac / h - np.outer(value / (h * h), jac[0])
                return np.block([[jac.real, -jac.imag],
                                 [jac.imag, jac.real]])
        else:
            def residual_function(x):
                value = output_jacobian(x)[0]
                if normalize_target:
                    value = value / value[0]
                return value - TARGET

            def jacobian_function(x):
                value, jac = output_jacobian(x)
                if normalize_target:
                    h = value[0]
                    jac = jac / h - np.outer(value / (h * h), jac[0])
                return jac
        result = least_squares(
            residual_function, x0, jac=jacobian_function,
            max_nfev=maxiter, ftol=1e-13, xtol=1e-13, gtol=1e-13,
        )
        iterations = result.nfev
    else:
        result = minimize(objective, x0, method="L-BFGS-B", jac=True,
                          options={"maxiter": maxiter, "ftol": 1e-15,
                                   "gtol": 1e-11, "maxls": 50})
        iterations = result.nit
    z = decode(result.x)
    loss, output = value_gradient(z, False)
    if normalize_target:
        output = output / output[0]
        residual = output - TARGET
        loss = 0.5 * float(np.vdot(residual, residual).real)
    else:
        residual = output - TARGET
    print(f"seed={seed} nit={iterations} loss={loss:.12g} "
          f"max={np.max(np.abs(residual)):.6g} norm={np.linalg.norm(z):.6g}",
          flush=True)
    if np.max(np.abs(residual)) < 1e-6:
        np.savez(f"candidate_c3_equivariant_n8_seed{seed}.npz",
                 parameters=z, matrices=expand(z), residual=residual)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starts", type=int, default=1)
    parser.add_argument("--maxiter", type=int, default=1000)
    parser.add_argument("--complex", action="store_true", dest="complex_search")
    parser.add_argument("--least-squares", action="store_true")
    parser.add_argument("--normalize-target", action="store_true")
    args = parser.parse_args()
    for seed in range(args.seed, args.seed + args.starts):
        run(seed, args.complex_search, args.maxiter, args.least_squares,
            args.normalize_target)


if __name__ == "__main__":
    main()
