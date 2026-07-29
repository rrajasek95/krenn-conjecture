#!/usr/bin/env python3
"""Numerical search for the full arbitrary-row 011166 boundary.

At a fixed point of each UFD/staircase model from
``notes/n8-011166-factor-allocation-boundary.md``, the contracted equation is

    Z Q^2 / 2 = sum_r (alpha_r beta_r) e_r^6,

where ``Z_uv=x_u y_v^T+y_u x_v^T`` is fixed and the fifteen internal edge
matrices in ``Q`` are optimized.  This is exploratory, not a certificate.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


N = 6
DIM = 3
SITES = tuple(range(N))
COLORS = tuple(range(DIM))
EDGES = tuple(itertools.combinations(SITES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
COLORINGS = np.asarray(
    tuple(itertools.product(COLORS, repeat=N)), dtype=np.int64
)
ROWS = np.arange(len(COLORINGS))


def perfect_matchings(vertices=SITES):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


MATCHINGS = tuple(perfect_matchings())


def fixed_case(name):
    e = np.eye(3)
    if name == "associate":
        alpha = np.asarray((1.0, 2.0, 3.0))
        beta = np.asarray((1.0, 1.0, 1.0))
        p_k = np.outer(e[1], e[1]) + np.outer(e[1], e[2])
        q_k = np.outer(e[0], e[0]) + np.outer(e[0], e[2])
        double_scalars = (2.0, 1.0, 3.0, 1.0)
    elif name == "split":
        alpha = np.asarray((1.0, 2.0, 3.0))
        beta = np.asarray((3.0, 3.0, 4.0))
        p_k = (
            np.outer(e[1], e[1])
            + np.outer(e[0] + e[1], e[2])
        )
        q_k = np.outer(e[0], e[0]) + np.outer(e[0], e[2])
        double_scalars = (3.0, 4.0, 3.0, 3.0)
    else:
        raise ValueError(name)

    # Site order: k, p-anchored singleton, q-anchored singleton, mixed
    # singleton, and the two crossed exact-double sites.
    a, b, c, d = double_scalars
    x = np.asarray((
        p_k.T @ alpha,
        alpha[0] * e[0],
        alpha[0] * np.ones(3),
        alpha[0] * np.ones(3),
        a * e[1],
        c * e[2],
    ))
    y = np.asarray((
        q_k.T @ beta,
        beta[0] * np.ones(3),
        beta[0] * e[0],
        beta[0] * np.asarray((2.0, 1.0, 1.0)),
        b * e[2],
        d * e[1],
    ))
    target = np.zeros(len(COLORINGS))
    for color in COLORS:
        target[np.all(COLORINGS == color, axis=1)] = alpha[color] * beta[color]
    z = np.asarray(tuple(
        np.outer(x[u], y[v]) + np.outer(y[u], x[v])
        for u, v in EDGES
    ))
    return x, y, z, target


def run(case, seed, starts, max_nfev, complex_mode):
    x, y, z, target = fixed_case(case)
    assert all(np.count_nonzero(np.cross(x[i], y[i])) == (3 if i == 0 else 2)
               for i in range(4))
    assert np.allclose(np.cross(x[4], y[4])[[1, 2]], 0)
    assert np.allclose(np.cross(x[5], y[5])[[1, 2]], 0)

    def decode(raw):
        if complex_mode:
            half = raw.size // 2
            raw = raw[:half] + 1j * raw[half:]
        return raw.reshape(len(EDGES), DIM, DIM)

    def value_and_jac(raw, want_jac):
        q = decode(raw)
        dtype = np.complex128 if complex_mode else np.float64
        value = np.zeros(len(COLORINGS), dtype=dtype)
        jac_c = (
            np.zeros((len(COLORINGS), len(EDGES) * DIM * DIM), dtype=dtype)
            if want_jac else None
        )
        for matching in MATCHINGS:
            ids = tuple(EDGE_INDEX[edge] for edge in matching)
            vals_q = tuple(
                q[index, COLORINGS[:, edge[0]], COLORINGS[:, edge[1]]]
                for index, edge in zip(ids, matching, strict=True)
            )
            vals_z = tuple(
                z[index, COLORINGS[:, edge[0]], COLORINGS[:, edge[1]]]
                for index, edge in zip(ids, matching, strict=True)
            )
            for distinguished in range(3):
                other = tuple(pos for pos in range(3) if pos != distinguished)
                value += (
                    vals_z[distinguished]
                    * vals_q[other[0]] * vals_q[other[1]]
                )
                if not want_jac:
                    continue
                for qpos, other_q in ((other[0], other[1]),
                                      (other[1], other[0])):
                    edge = matching[qpos]
                    columns = (
                        ids[qpos] * DIM * DIM
                        + COLORINGS[:, edge[0]] * DIM
                        + COLORINGS[:, edge[1]]
                    )
                    np.add.at(
                        jac_c,
                        (ROWS, columns),
                        vals_z[distinguished] * vals_q[other_q],
                    )
        residual = value - target
        if not want_jac:
            return (
                np.r_[residual.real, residual.imag]
                if complex_mode else residual
            )
        if complex_mode:
            return np.block(
                [[jac_c.real, -jac_c.imag], [jac_c.imag, jac_c.real]]
            )
        return jac_c

    rng = np.random.default_rng(seed)
    raw_size = len(EDGES) * DIM * DIM * (2 if complex_mode else 1)
    for start in range(starts):
        fit = least_squares(
            lambda raw: value_and_jac(raw, False),
            rng.normal(scale=0.2, size=raw_size),
            jac=lambda raw: value_and_jac(raw, True),
            max_nfev=max_nfev,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
        )
        residual = value_and_jac(fit.x, False)
        print(
            f"case={case} start={start} complex={complex_mode} "
            f"cost={fit.cost:.12g} max={np.max(np.abs(residual)):.6g} "
            f"nfev={fit.nfev}",
            flush=True,
        )
        largest = np.argsort(np.abs(residual))[-5:][::-1]
        print(
            "  residual words",
            tuple(
                (tuple(int(value) for value in COLORINGS[index]),
                 complex(residual[index]) if complex_mode
                 else float(residual[index]))
                for index in largest if abs(residual[index]) > 1e-7
            ),
            flush=True,
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=("associate", "split"),
                        default="associate")
    parser.add_argument("--seed", type=int, default=20260724)
    parser.add_argument("--starts", type=int, default=2)
    parser.add_argument("--max-nfev", type=int, default=500)
    parser.add_argument("--complex", action="store_true")
    args = parser.parse_args()
    run(args.case, args.seed, args.starts, args.max_nfev, args.complex)


if __name__ == "__main__":
    main()
