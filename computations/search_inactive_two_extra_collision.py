#!/usr/bin/env python3
"""Probe collision two-jets over Hamilton bases with two inactive cells.

This is a discovery script, not a proof.  It fixes a six-site exact binary
base ``q0 = h + E + F`` where the extra scalar cells do not change
``H(q0)=2 X + Y``.  The one-z source is parametrized by the *exact* tangent
kernel of ``dH_q0``.  Least squares then searches only the two-z collision
equations

    dH_q0(W) + 1/2 d2H_q0(Z,Z) = X_2/2.

The output reports the best residual and, on success, writes a candidate
whose entries can subsequently be reconstructed over an exact field.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.linalg import null_space
from scipy.optimize import least_squares


N = 6
X, Y, Z = range(3)
EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, partner in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, partner),) + tail


MATCHINGS = tuple(perfect_matchings(range(N)))


def amplitude(matrices, coloring):
    answer = 0j
    for matching in MATCHINGS:
        term = 1 + 0j
        for u, v in matching:
            term *= matrices[EDGE_INDEX[(u, v)], coloring[u], coloring[v]]
        answer += term
    return answer


def hamilton_base(extra_cells):
    matrices = np.zeros((len(EDGES), 3, 3), dtype=complex)
    for position, edge in enumerate(((0, 1), (2, 3), (4, 5))):
        matrices[EDGE_INDEX[edge], X, X] = 2 if position == 0 else 1
    for edge in ((0, 5), (1, 2), (3, 4)):
        matrices[EDGE_INDEX[edge], Y, Y] = 1
    for u, v, cu, cv, weight in extra_cells:
        matrices[EDGE_INDEX[(u, v)], cu, cv] = weight
    return matrices


Q1_VARIABLES = tuple(
    (site, other, color)
    for site in range(N)
    for other in range(N)
    if other != site
    for color in (X, Y)
)
Q1_INDEX = {variable: index for index, variable in enumerate(Q1_VARIABLES)}
Q2_VARIABLES = EDGES


def q1_cell(matrices, site, other, color, value):
    u, v = sorted((site, other))
    if site == u:
        matrices[EDGE_INDEX[(u, v)], Z, color] += value
    else:
        matrices[EDGE_INDEX[(u, v)], color, Z] += value


def q2_cell(matrices, first, second, value):
    u, v = sorted((first, second))
    matrices[EDGE_INDEX[(u, v)], Z, Z] += value


def tangent_kernel(q0):
    """Return a block-diagonal orthonormal basis for every one-z sector."""
    blocks = []
    for site in range(N):
        variables = tuple(
            variable for variable in Q1_VARIABLES if variable[0] == site
        )
        colorings = []
        for rest in itertools.product((X, Y), repeat=N - 1):
            coloring = list(rest)
            coloring.insert(site, Z)
            colorings.append(tuple(coloring))
        matrix = np.zeros((len(colorings), len(variables)), dtype=complex)
        for column, (_, other, color) in enumerate(variables):
            probe = q0.copy()
            q1_cell(probe, site, other, color, 1)
            for row, coloring in enumerate(colorings):
                matrix[row, column] = amplitude(probe, coloring)
        kernel = null_space(matrix)
        # Embed this site's kernel in the global 60-coordinate q1 space.
        embedded = np.zeros((len(Q1_VARIABLES), kernel.shape[1]), dtype=complex)
        for local_row, variable in enumerate(variables):
            embedded[Q1_INDEX[variable], :] = kernel[local_row, :]
        blocks.append(embedded)
    return np.concatenate(blocks, axis=1), tuple(block.shape[1] for block in blocks)


PAIR_COLORINGS = tuple(
    coloring
    for coloring in itertools.product((X, Y, Z), repeat=N)
    if coloring.count(Z) == 2
)
PAIR_TARGET = np.asarray(
    [
        0.5 if all(color == X for color in coloring if color != Z) else 0
        for coloring in PAIR_COLORINGS
    ],
    dtype=complex,
)


def decode(real_vector, kernel):
    complex_count = kernel.shape[1] + len(Q2_VARIABLES)
    vector = real_vector[:complex_count] + 1j * real_vector[complex_count:]
    q1 = kernel @ vector[: kernel.shape[1]]
    q2 = vector[kernel.shape[1] :]
    return q1, q2


def pair_values(real_vector, q0, kernel):
    q1, q2 = decode(real_vector, kernel)
    source = q0.copy()
    for value, (site, other, color) in zip(q1, Q1_VARIABLES):
        q1_cell(source, site, other, color, value)
    for value, (first, second) in zip(q2, Q2_VARIABLES):
        q2_cell(source, first, second, value)
    return np.asarray(
        [amplitude(source, coloring) for coloring in PAIR_COLORINGS]
    )


def residual(real_vector, q0, kernel):
    value = pair_values(real_vector, q0, kernel) - PAIR_TARGET
    return np.r_[value.real, value.imag]


def parse_cell(specification):
    # Syntax: 02:xy or 02:xy:3/2.  Vertices are single digits at n=6.
    fields = specification.split(":")
    edge, decoration = fields[:2]
    weight = complex(eval(fields[2], {"__builtins__": {}}, {})) if len(fields) == 3 else 1
    u, v = int(edge[0]), int(edge[1])
    if u > v:
        u, v = v, u
        decoration = decoration[::-1]
    colors = {"x": X, "y": Y}
    return u, v, colors[decoration[0]], colors[decoration[1]], weight


def verify_base(q0):
    largest = 0.0
    for coloring in itertools.product((X, Y), repeat=N):
        target = 2 if all(c == X for c in coloring) else 1 if all(c == Y for c in coloring) else 0
        largest = max(largest, abs(amplitude(q0, coloring) - target))
    return largest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cells", nargs="*", default=("02:xx", "13:yy"))
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--max-nfev", type=int, default=5000)
    args = parser.parse_args()

    q0 = hamilton_base(tuple(parse_cell(cell) for cell in args.cells))
    base_residual = verify_base(q0)
    if base_residual > 1e-12:
        raise SystemExit(f"base is not exact: residual={base_residual:g}")
    kernel, dimensions = tangent_kernel(q0)
    complex_count = kernel.shape[1] + len(Q2_VARIABLES)
    print(
        f"cells={args.cells} tangent_dimensions={dimensions} "
        f"complex_variables={complex_count}",
        flush=True,
    )
    rng = np.random.default_rng(args.seed)
    best = np.inf
    for start in range(args.starts):
        initial_complex = 0.1 * (
            rng.normal(size=complex_count) + 1j * rng.normal(size=complex_count)
        )
        initial = np.r_[initial_complex.real, initial_complex.imag]
        fit = least_squares(
            residual,
            initial,
            args=(q0, kernel),
            max_nfev=args.max_nfev,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
        )
        value = pair_values(fit.x, q0, kernel) - PAIR_TARGET
        largest = np.max(np.abs(value))
        best = min(best, largest)
        print(
            f"start={start} cost={fit.cost:.8g} max={largest:.8g} "
            f"optimality={fit.optimality:.3g} nfev={fit.nfev}",
            flush=True,
        )
        if largest < 1e-8:
            np.savez(
                "/tmp/inactive_two_extra_collision.npz",
                q0=q0,
                q1=decode(fit.x, kernel)[0],
                q2=decode(fit.x, kernel)[1],
                kernel=kernel,
                parameters=fit.x,
            )
            break
    print(f"best_max_residual={best:.12g}")


if __name__ == "__main__":
    main()
