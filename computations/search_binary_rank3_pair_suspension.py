#!/usr/bin/env python3
"""Search the fixed-source pair suspension from the exact n=6 binary point.

The internal six-site source is the exact C3-equivariant realization of
``e0^6 + e1^6 + (e0+e1)^6``.  Only the two deleted stars and their direct
edge vary.  This is a numerical discovery script, not a certificate.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares

from verify_binary_rank3_projection_exact import source


N = 6
Q = 2
VERTICES = tuple(range(N))
EDGES = tuple(itertools.combinations(VERTICES, 2))
COLORINGS = np.asarray(tuple(itertools.product(range(Q), repeat=N)), dtype=np.int8)
ROWS = np.arange(len(COLORINGS))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


INTERNAL = {
    edge: np.asarray(matrix.evalf(), dtype=complex)
    for edge, matrix in source().items()
}


def matching_tensor(vertices: tuple[int, ...]) -> np.ndarray:
    answer = np.zeros(len(COLORINGS), dtype=complex)
    for matching in perfect_matchings(vertices):
        term = np.ones(len(COLORINGS), dtype=complex)
        for u, v in matching:
            term *= INTERNAL[u, v][COLORINGS[:, u], COLORINGS[:, v]]
        answer += term
    return answer


H6 = matching_tensor(VERTICES)
COFACTORS = {
    (u, v): matching_tensor(tuple(w for w in VERTICES if w not in (u, v)))
    for u, v in EDGES
}
VECTORS = (
    np.asarray((1.0, 0.0)),
    np.asarray((0.0, 1.0)),
    np.asarray((1.0, 1.0)),
)
TARGET = np.zeros((Q, Q, len(COLORINGS)), dtype=complex)
for vector in VECTORS:
    internal = np.prod(vector[COLORINGS], axis=1)
    TARGET += np.outer(vector, vector)[:, :, None] * internal[None, None, :]

STAR_SIZE = Q * N * Q
EDGE_SIZE = Q * Q
PARAMETERS = 2 * STAR_SIZE + EDGE_SIZE


def unpack(z: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    left = z[:STAR_SIZE].reshape(Q, N, Q)
    right = z[STAR_SIZE : 2 * STAR_SIZE].reshape(Q, N, Q)
    direct = z[-EDGE_SIZE:].reshape(Q, Q)
    return left, right, direct


def value_and_jacobian(
    z: np.ndarray, *, need_jacobian: bool
) -> tuple[np.ndarray, np.ndarray] | np.ndarray:
    left, right, direct = unpack(z)
    output = direct[:, :, None] * H6[None, None, :]
    jac = (
        np.zeros((Q, Q, len(COLORINGS), PARAMETERS), dtype=complex)
        if need_jacobian
        else None
    )
    if jac is not None:
        for i, j in itertools.product(range(Q), repeat=2):
            jac[i, j, :, 2 * STAR_SIZE + Q * i + j] = H6

    for u, v in EDGES:
        cu = COLORINGS[:, u]
        cv = COLORINGS[:, v]
        cofactor = COFACTORS[u, v]
        for i, j in itertools.product(range(Q), repeat=2):
            left_u = left[i, u, cu]
            left_v = left[i, v, cv]
            right_u = right[j, u, cu]
            right_v = right[j, v, cv]
            output[i, j] += (left_u * right_v + left_v * right_u) * cofactor
            if jac is None:
                continue
            np.add.at(
                jac[i, j],
                (ROWS, i * N * Q + u * Q + cu),
                right_v * cofactor,
            )
            np.add.at(
                jac[i, j],
                (ROWS, i * N * Q + v * Q + cv),
                right_u * cofactor,
            )
            np.add.at(
                jac[i, j],
                (ROWS, STAR_SIZE + j * N * Q + u * Q + cu),
                left_v * cofactor,
            )
            np.add.at(
                jac[i, j],
                (ROWS, STAR_SIZE + j * N * Q + v * Q + cv),
                left_u * cofactor,
            )
    if jac is None:
        return output
    return output, jac.reshape(Q * Q * len(COLORINGS), PARAMETERS)


def realify(value: np.ndarray) -> np.ndarray:
    return np.r_[value.real.ravel(), value.imag.ravel()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260724)
    parser.add_argument("--starts", type=int, default=4)
    parser.add_argument("--max-nfev", type=int, default=5000)
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)

    def decode(x: np.ndarray) -> np.ndarray:
        return x[:PARAMETERS] + 1j * x[PARAMETERS:]

    def residual(x: np.ndarray) -> np.ndarray:
        return realify(value_and_jacobian(decode(x), need_jacobian=False) - TARGET)

    def jacobian(x: np.ndarray) -> np.ndarray:
        complex_jac = value_and_jacobian(decode(x), need_jacobian=True)[1]
        return np.block(
            [[complex_jac.real, -complex_jac.imag],
             [complex_jac.imag, complex_jac.real]]
        )

    for start in range(args.starts):
        z0 = rng.normal(scale=0.25, size=2 * PARAMETERS)
        fit = least_squares(
            residual,
            z0,
            jac=jacobian,
            max_nfev=args.max_nfev,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
        )
        error = residual(fit.x)
        print(
            start,
            "cost",
            fit.cost,
            "max",
            float(np.max(np.abs(error))),
            "norm",
            float(np.linalg.norm(fit.x)),
            "nfev",
            fit.nfev,
            "rankJ",
            int(np.linalg.matrix_rank(jacobian(fit.x), tol=1e-8)),
            flush=True,
        )


if __name__ == "__main__":
    main()
