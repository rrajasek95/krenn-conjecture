#!/usr/bin/env python3
"""Numerically probe complex minimum-norm realizations of binary equality.

This is a discovery script.  It fits the exact coefficient equations and
then follows the Tikhonov path ``||Phi(A)-EQ||^2 + mu ||A||^2``.  The output
reports the norm and the edge/cell concentration, which distinguishes the
Hamilton value ``||A||^2=n`` from dense or cancellation-supported minima.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for k, v in enumerate(vertices[1:], 1):
        rest = vertices[1:k] + vertices[k + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def problem(n: int):
    q = 2
    edges = tuple(itertools.combinations(range(n), 2))
    edge_index = {edge: k for k, edge in enumerate(edges)}
    matchings = tuple(perfect_matchings(range(n)))
    colorings = np.asarray(tuple(itertools.product(range(q), repeat=n)), dtype=np.int8)
    target = np.asarray([float(len(set(c)) == 1) for c in colorings])
    parameters = len(edges) * q * q

    def amplitudes(z):
        a = z.reshape(len(edges), q, q)
        out = np.zeros(len(colorings), dtype=z.dtype)
        for matching in matchings:
            term = np.ones(len(colorings), dtype=z.dtype)
            for u, v in matching:
                term *= a[edge_index[(u, v)], colorings[:, u], colorings[:, v]]
            out += term
        return out

    def jacobian(z):
        a = z.reshape(len(edges), q, q)
        jac = np.zeros((len(colorings), parameters), dtype=z.dtype)
        rows = np.arange(len(colorings))
        for matching in matchings:
            values = [
                a[edge_index[e], colorings[:, e[0]], colorings[:, e[1]]]
                for e in matching
            ]
            for position, edge in enumerate(matching):
                derivative = np.ones(len(colorings), dtype=z.dtype)
                for j, value in enumerate(values):
                    if j != position:
                        derivative *= value
                local = colorings[:, edge[0]] * q + colorings[:, edge[1]]
                columns = edge_index[edge] * q * q + local
                np.add.at(jac, (rows, columns), derivative)
        return jac

    return edges, target, parameters, amplitudes, jacobian


def realify(value):
    return np.r_[value.real, value.imag]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--starts", type=int, default=12)
    parser.add_argument("--seed", type=int, default=20260724)
    parser.add_argument("--max-nfev", type=int, default=10000)
    parser.add_argument("--real", action="store_true")
    args = parser.parse_args()

    edges, target, parameters, amplitudes, complex_jacobian = problem(args.n)
    rng = np.random.default_rng(args.seed)

    def decode(x):
        if args.real:
            return x.astype(complex)
        return x[:parameters] + 1j * x[parameters:]

    def residual(x, mu=0.0):
        z = decode(x)
        base = realify(amplitudes(z) - target)
        if mu:
            return np.r_[base, np.sqrt(mu) * x]
        return base

    def jacobian(x, mu=0.0):
        value = complex_jacobian(decode(x))
        if args.real:
            base = np.vstack((value.real, value.imag))
        else:
            base = np.block([[value.real, -value.imag], [value.imag, value.real]])
        if mu:
            return np.vstack((base, np.sqrt(mu) * np.eye(len(x))))
        return base

    dimension = parameters if args.real else 2 * parameters
    for start in range(args.starts):
        x = rng.normal(scale=0.4, size=dimension)
        fit = least_squares(
            lambda y: residual(y),
            x,
            jac=lambda y: jacobian(y),
            max_nfev=args.max_nfev,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
        )
        if np.max(np.abs(amplitudes(decode(fit.x)) - target)) > 1e-7:
            print(start, "fit-failed", fit.cost)
            continue
        x = fit.x
        for mu in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8):
            fit = least_squares(
                lambda y, mu=mu: residual(y, mu),
                x,
                jac=lambda y, mu=mu: jacobian(y, mu),
                max_nfev=args.max_nfev,
                ftol=1e-13,
                xtol=1e-13,
                gtol=1e-13,
            )
            x = fit.x
        z = decode(x).reshape(len(edges), 2, 2)
        cell_magnitudes = np.sort(np.abs(z).ravel())[::-1]
        edge_norms = np.sort(np.linalg.norm(z.reshape(len(edges), 4), axis=1))[::-1]
        error = np.max(np.abs(amplitudes(z.ravel()) - target))
        print(
            start,
            "norm2", float(np.vdot(z, z).real),
            "error", float(error),
            "cells", np.round(cell_magnitudes[: min(16, len(cell_magnitudes))], 5),
            "edges", np.round(edge_norms[: min(12, len(edge_norms))], 5),
            flush=True,
        )


if __name__ == "__main__":
    main()
