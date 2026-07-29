#!/usr/bin/env python3
"""Search for an eight-site pair suspension over the six-site prism chart.

This is a discovery script, not a certificate.  The internal six-site edge
family is the unit specialization of the standard prism border family, so
its matching tensor is Delta_3 plus one mixed basis tensor.  We optimize the
two deleted stars and their direct edge in the exact pair expansion

    A_pq H_6(x) + p_i q_j H_4(x) = delta_ij e_i^6.

The parametrization retains the full three-vector at every endpoint of both
stars, but keeps the six internal matrices fixed.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


N = 6
Q = 3
VERTICES = tuple(range(N))
EDGES = tuple(itertools.combinations(VERTICES, 2))
COLORINGS = np.asarray(list(itertools.product(range(Q), repeat=N)), dtype=np.int8)
ROWS = np.arange(len(COLORINGS))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for k in range(1, len(vertices)):
        v = vertices[k]
        rest = vertices[1:k] + vertices[k + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def internal_source():
    matrices = {(u, v): np.zeros((Q, Q)) for u, v in EDGES}
    for color, matching in enumerate(
        (
            ((0, 4), (1, 2), (3, 5)),
            ((0, 5), (1, 4), (2, 3)),
            ((0, 3), (1, 5), (2, 4)),
        )
    ):
        for edge in matching:
            matrices[edge][color, color] = 1.0
    return matrices


INTERNAL = internal_source()
MATCHINGS = tuple(perfect_matchings(VERTICES))


def matching_tensor(vertices):
    answer = np.zeros(len(COLORINGS))
    for matching in perfect_matchings(vertices):
        term = np.ones(len(COLORINGS))
        for u, v in matching:
            term *= INTERNAL[u, v][COLORINGS[:, u], COLORINGS[:, v]]
        answer += term
    return answer


H6 = matching_tensor(VERTICES)
COFACTORS = {}
for u, v in EDGES:
    rest = tuple(w for w in VERTICES if w not in (u, v))
    COFACTORS[u, v] = matching_tensor(rest)

TARGET = np.zeros((Q, Q, len(COLORINGS)))
for color in range(Q):
    TARGET[color, color, np.all(COLORINGS == color, axis=1)] = 1.0

P_SIZE = Q * N * Q
S_SIZE = Q * N * Q
A_SIZE = Q * Q
PARAMETERS = P_SIZE + S_SIZE + A_SIZE


def unpack(z):
    p = z[:P_SIZE].reshape(Q, N, Q)
    s = z[P_SIZE:P_SIZE + S_SIZE].reshape(Q, N, Q)
    a = z[-A_SIZE:].reshape(Q, Q)
    return p, s, a


def value_and_jacobian(z, need_jacobian=True):
    p, s, a = unpack(z)
    output = a[:, :, None] * H6[None, None, :]
    jac = np.zeros((Q, Q, len(COLORINGS), PARAMETERS)) if need_jacobian else None
    if need_jacobian:
        for i in range(Q):
            for j in range(Q):
                jac[i, j, :, P_SIZE + S_SIZE + i * Q + j] = H6

    for u, v in EDGES:
        cu = COLORINGS[:, u]
        cv = COLORINGS[:, v]
        cofactor = COFACTORS[u, v]
        for i in range(Q):
            pu = p[i, u, cu]
            pv = p[i, v, cv]
            for j in range(Q):
                qv = s[j, v, cv]
                qu = s[j, u, cu]
                output[i, j] += (pu * qv + pv * qu) * cofactor
                if not need_jacobian:
                    continue
                np.add.at(
                    jac[i, j],
                    (ROWS, i * N * Q + u * Q + cu),
                    qv * cofactor,
                )
                np.add.at(
                    jac[i, j],
                    (ROWS, i * N * Q + v * Q + cv),
                    qu * cofactor,
                )
                np.add.at(
                    jac[i, j],
                    (ROWS, P_SIZE + j * N * Q + v * Q + cv),
                    pu * cofactor,
                )
                np.add.at(
                    jac[i, j],
                    (ROWS, P_SIZE + j * N * Q + u * Q + cu),
                    pv * cofactor,
                )
    if need_jacobian:
        return output, jac.reshape(Q * Q * len(COLORINGS), PARAMETERS)
    return output


def initial_point(rng):
    z = rng.normal(scale=0.05, size=PARAMETERS)
    p, s, _a = unpack(z)
    # Each chosen private prism edge differentiates to one target ray.
    for color, (u, v) in enumerate(((1, 2), (0, 5), (0, 3))):
        p[color, u, color] += 1.0
        s[color, v, color] += 1.0
    return z


def run(seed, max_nfev):
    rng = np.random.default_rng(seed)
    z0 = initial_point(rng)

    def residual(z):
        return (value_and_jacobian(z, False) - TARGET).reshape(-1)

    def jacobian(z):
        return value_and_jacobian(z, True)[1]

    fit = least_squares(
        residual,
        z0,
        jac=jacobian,
        max_nfev=max_nfev,
        ftol=1e-13,
        xtol=1e-13,
        gtol=1e-13,
        verbose=0,
    )
    raw = residual(fit.x)
    print(
        f"seed={seed} cost={fit.cost:.10g} max={np.max(np.abs(raw)):.5g} "
        f"norm={np.linalg.norm(fit.x):.5g} nfev={fit.nfev}",
        flush=True,
    )
    if np.max(np.abs(raw)) < 1e-8 and np.linalg.norm(fit.x) < 1e6:
        np.savez(
            f"candidate_pair_suspension_seed{seed}.npz",
            internal=np.asarray([INTERNAL[e] for e in EDGES]),
            parameters=fit.x,
            residual=raw,
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starts", type=int, default=1)
    parser.add_argument("--max-nfev", type=int, default=1000)
    args = parser.parse_args()
    for seed in range(args.seed, args.seed + args.starts):
        run(seed, args.max_nfev)


if __name__ == "__main__":
    main()
