#!/usr/bin/env python3
"""Search for a binary module that absorbs a third-color perfect matching.

Fix P={01,23,45} and set its binary matrices to zero.  We seek binary
matrices on K6-P such that the full matching tensor is Delta_(6,2), while
the induced four-site matching tensor left after deleting either endpoint
pair of P is zero.  If found exactly, adding e2 tensor e2 on every P edge
would give an exact three-color counterexample: every proper use of P has a
zero binary cofactor.

This script is numerical discovery only; it saves small finite residuals for
subsequent symbolic recovery.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


N = 6
Q = 2
VERTICES = tuple(range(N))
CAP = ((0, 1), (2, 3), (4, 5))
CAP_SET = set(CAP)
EDGES = tuple(
    edge for edge in itertools.combinations(VERTICES, 2) if edge not in CAP_SET
)
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        edge = tuple(sorted((first, second)))
        if edge not in EDGE_INDEX:
            continue
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield (edge,) + tail


SUBSYSTEMS = ((VERTICES, "full"),) + tuple(
    (
        tuple(vertex for vertex in VERTICES if vertex not in cap_edge),
        f"cofactor-{cap_edge[0]}{cap_edge[1]}",
    )
    for cap_edge in CAP
)


def build_rows():
    rows = []
    targets = []
    metadata = []
    for vertices, name in SUBSYSTEMS:
        matchings = tuple(perfect_matchings(vertices))
        for coloring_values in itertools.product(range(Q), repeat=len(vertices)):
            coloring = dict(zip(vertices, coloring_values, strict=True))
            columns = tuple(
                tuple(
                    EDGE_INDEX[edge] * Q * Q
                    + coloring[edge[0]] * Q
                    + coloring[edge[1]]
                    for edge in matching
                )
                for matching in matchings
            )
            rows.append(columns)
            if name == "full":
                targets.append(float(len(set(coloring_values)) == 1))
            else:
                targets.append(0.0)
            metadata.append((name, coloring_values))
    return tuple(rows), np.asarray(targets), tuple(metadata)


ROWS, TARGET, METADATA = build_rows()
PARAMETERS = len(EDGES) * Q * Q


def amplitudes(z):
    answer = np.zeros(len(ROWS), dtype=z.dtype)
    for row_index, matching_columns in enumerate(ROWS):
        total = 0
        for columns in matching_columns:
            term = 1
            for column in columns:
                term *= z[column]
            total += term
        answer[row_index] = total
    return answer


def complex_jacobian(z):
    jacobian = np.zeros((len(ROWS), PARAMETERS), dtype=z.dtype)
    for row_index, matching_columns in enumerate(ROWS):
        for columns in matching_columns:
            for position, column in enumerate(columns):
                derivative = 1
                for other_position, other_column in enumerate(columns):
                    if other_position != position:
                        derivative *= z[other_column]
                jacobian[row_index, column] += derivative
    return jacobian


def run(seed, starts, max_nfev, scale):
    rng = np.random.default_rng(seed)
    for offset in range(starts):
        initial = rng.normal(scale=scale, size=2 * PARAMETERS)

        def decode(x):
            return x[:PARAMETERS] + 1j * x[PARAMETERS:]

        def residual(x):
            value = amplitudes(decode(x)) - TARGET
            return np.r_[value.real, value.imag]

        def jacobian(x):
            value = complex_jacobian(decode(x))
            return np.block(
                [[value.real, -value.imag], [value.imag, value.real]]
            )

        fit = least_squares(
            residual,
            initial,
            jac=jacobian,
            max_nfev=max_nfev,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
        )
        z = decode(fit.x)
        raw = amplitudes(z) - TARGET
        maximum = np.max(np.abs(raw))
        norm = np.linalg.norm(fit.x)
        print(
            f"seed={seed + offset} cost={fit.cost:.10g} max={maximum:.5g} "
            f"norm={norm:.5g} opt={fit.optimality:.3g} nfev={fit.nfev}",
            flush=True,
        )
        if maximum < 1e-5 and norm < 1e5:
            np.savez(
                f"candidate_binary_absorber_seed{seed + offset}.npz",
                edges=np.asarray(EDGES),
                matrices=z.reshape(len(EDGES), Q, Q),
                residual=raw,
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--max-nfev", type=int, default=5000)
    parser.add_argument("--scale", type=float, default=0.4)
    args = parser.parse_args()
    run(args.seed, args.starts, args.max_nfev, args.scale)


if __name__ == "__main__":
    main()
