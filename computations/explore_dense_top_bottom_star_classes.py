#!/usr/bin/env python3
"""Explore the five dense-top star obstruction classes at n=6.

This is a discovery helper.  It uses the exact top elimination from
``search_dense_top_bottom_endpoints`` and a fixed rationally valid pivot
chart for the correction columns.  The resulting 5 by 5 Schur complement
represents the five scalar D0 star columns modulo all D1,D2 corrections.
Its determinant is nonzero on the published top-only counterexample.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np

import search_dense_top_bottom_endpoints as endpoint


N = endpoint.N
X, Y, Z = endpoint.X, endpoint.Y, endpoint.Z

# These bases were selected at the rational top-only point.  All indices
# refer to the canonical ordering returned by ``transport_matrix``.
CORRECTION_COLUMNS = (
    0, 1, 2, 3, 4, 5, 8, 9, 12, 13, 16, 17,
    20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
    32, 33, 34, 35, 36, 37, 38, 39,
)
PIVOT_ROWS = tuple(range(1, 33))
OBSTRUCTION_ROWS = (0, 49, 53, 57, 69)


def coefficient_on(source, vertices, coloring):
    answer = 0j
    for matching in endpoint.perfect_matchings(vertices):
        term = 1 + 0j
        for edge in matching:
            term *= source[
                endpoint.EDGE_INDEX[edge], coloring[edge[0]], coloring[edge[1]]
            ]
        answer += term
    return answer


def transport_matrix(parameters, star=0):
    k = endpoint.decode_k(parameters)
    q0 = endpoint.eliminate_q0(k)
    source = q0 + k
    for edge, weight in endpoint.WEIGHTS.items():
        source[endpoint.EDGE_INDEX[edge], Z, Z] = weight

    columns = []
    decorations = (
        (0, ((Z, Z),)),
        (1, ((Z, X), (Z, Y), (X, Z), (Y, Z))),
        (2, ((X, X), (X, Y), (Y, X), (Y, Y))),
    )
    for grade, cells in decorations:
        for neighbor in endpoint.VERTICES:
            if neighbor == star:
                continue
            first, second = sorted((star, neighbor))
            for star_color, neighbor_color in cells:
                colors = (
                    (star_color, neighbor_color)
                    if star == first
                    else (neighbor_color, star_color)
                )
                columns.append((grade, neighbor, *colors))

    rows = []
    row_colorings = []
    for binary_count in (0, 1, 2):
        for binary_sites in itertools.combinations(endpoint.VERTICES, binary_count):
            for binary_colors in itertools.product((X, Y), repeat=binary_count):
                coloring = [Z] * N
                for site, color in zip(binary_sites, binary_colors):
                    coloring[site] = color
                row = []
                for _, neighbor, first_color, second_color in columns:
                    first, second = sorted((star, neighbor))
                    if (coloring[first], coloring[second]) != (
                        first_color,
                        second_color,
                    ):
                        row.append(0j)
                        continue
                    remaining = tuple(
                        vertex
                        for vertex in endpoint.VERTICES
                        if vertex not in (star, neighbor)
                    )
                    row.append(coefficient_on(source, remaining, coloring))
                rows.append(row)
                row_colorings.append(tuple(coloring))
    return np.asarray(rows), tuple(columns), tuple(row_colorings)


def obstruction_matrix(parameters):
    matrix, _, _ = transport_matrix(parameters)
    d0 = matrix[:, :5]
    correction = matrix[:, 5:]
    basis = correction[:, CORRECTION_COLUMNS]
    pivot = basis[np.ix_(PIVOT_ROWS, range(len(CORRECTION_COLUMNS)))]
    lift = np.linalg.solve(pivot, d0[list(PIVOT_ROWS)])
    return d0[list(OBSTRUCTION_ROWS)] - basis[
        np.ix_(OBSTRUCTION_ROWS, range(len(CORRECTION_COLUMNS)))
    ] @ lift


def top_only_parameters():
    target = np.zeros((len(endpoint.EDGES), 3, 3), dtype=complex)
    endpoint.set_directed_cell(target, 0, X, 1, 3)
    endpoint.set_directed_cell(target, 0, X, 2, -3)
    return np.linalg.lstsq(
        endpoint.K_BASIS.reshape(-1, len(endpoint.FREE)),
        target.reshape(-1),
        rcond=None,
    )[0]


def report(label, parameters):
    matrix, _, _ = transport_matrix(parameters)
    obstruction = obstruction_matrix(parameters)
    bottom, tangent, _, _ = endpoint.bottom_values(parameters)
    print(
        f"{label}: ranks full/correction/obstruction="
        f"{np.linalg.matrix_rank(matrix)}/"
        f"{np.linalg.matrix_rank(matrix[:, 5:])}/"
        f"{np.linalg.matrix_rank(obstruction)}; "
        f"det={np.linalg.det(obstruction):.12g}; "
        f"bottom_max={np.max(np.abs(bottom - endpoint.BOTTOM_TARGET)):.6g}; "
        f"tangent_max={np.max(np.abs(tangent)):.6g}"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("parameters", nargs="*")
    args = parser.parse_args()
    report("top-only", top_only_parameters())
    for path in args.parameters:
        value = np.load(path)
        if isinstance(value, np.lib.npyio.NpzFile):
            parameters = value["parameters"]
        else:
            parameters = value
        report(path, parameters)


if __name__ == "__main__":
    main()
