#!/usr/bin/env python3
"""Numerical probe of least Frobenius norm in the n=6,q=2 exact fiber."""

from __future__ import annotations

import itertools

import numpy as np
from scipy.optimize import least_squares

from verify_binary_spinflip_cycle_identity import perfect_matchings


N = 6
Q = 2
EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {e: i for i, e in enumerate(EDGES)}
MATCHINGS = tuple(perfect_matchings(tuple(range(N))))
COLORINGS = np.array(tuple(itertools.product(range(Q), repeat=N)), dtype=np.int8)
TARGET = np.array([float(len(set(c)) == 1) for c in COLORINGS])


def amplitudes(x):
    a = x.reshape(len(EDGES), Q, Q)
    out = np.zeros(len(COLORINGS), dtype=x.dtype)
    for matching in MATCHINGS:
        term = np.ones(len(COLORINGS), dtype=x.dtype)
        for u, v in matching:
            term *= a[EDGE_INDEX[(u, v)], COLORINGS[:, u], COLORINGS[:, v]]
        out += term
    return out


def jacobian(x):
    a = x.reshape(len(EDGES), Q, Q)
    jac = np.zeros((len(COLORINGS), len(x)), dtype=x.dtype)
    rows = np.arange(len(COLORINGS))
    for matching in MATCHINGS:
        vals = [a[EDGE_INDEX[e], COLORINGS[:, e[0]], COLORINGS[:, e[1]]] for e in matching]
        for pos, e in enumerate(matching):
            derivative = np.ones(len(COLORINGS), dtype=x.dtype)
            for j, val in enumerate(vals):
                if j != pos:
                    derivative *= val
            local = COLORINGS[:, e[0]] * Q + COLORINGS[:, e[1]]
            cols = EDGE_INDEX[e] * Q * Q + local
            np.add.at(jac, (rows, cols), derivative)
    return jac


def regularize(x, mu):
    root = np.sqrt(mu)
    return least_squares(
        lambda z: np.r_[amplitudes(z) - TARGET, root * z],
        x,
        jac=lambda z: np.vstack((jacobian(z), root * np.eye(len(z)))),
        max_nfev=5000,
        ftol=1e-14,
        xtol=1e-14,
        gtol=1e-14,
    ).x


def standard():
    x = np.zeros(len(EDGES) * Q * Q)
    for e in ((0, 1), (2, 3), (4, 5)):
        x[EDGE_INDEX[e] * 4] = 1
    for e in ((0, 5), (1, 2), (3, 4)):
        x[EDGE_INDEX[e] * 4 + 3] = 1
    return x


def main():
    rng = np.random.default_rng(20260723)
    starts = [standard()]
    for _ in range(12):
        fit = least_squares(
            lambda z: amplitudes(z) - TARGET,
            rng.normal(scale=.4, size=len(EDGES) * 4),
            jac=jacobian,
            max_nfev=10000,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
        )
        if np.max(np.abs(amplitudes(fit.x) - TARGET)) < 1e-8:
            starts.append(fit.x)
    for index, x in enumerate(starts):
        before = np.linalg.norm(x)
        for mu in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8):
            x = regularize(x, mu)
        error = np.max(np.abs(amplitudes(x) - TARGET))
        print(index, "before", before, "after", np.linalg.norm(x), "maxerr", error)


if __name__ == "__main__":
    main()
