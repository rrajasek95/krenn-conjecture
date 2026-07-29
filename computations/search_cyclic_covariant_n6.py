#!/usr/bin/env python3
"""Numerical discovery search for cyclic-covariant n=6, q=3 solutions.

This is not a proof artifact.  It restricts the full aggregate-matrix model
only by invariance under

    vertex v -> v+1 (mod 6),  color i -> i+s (mod 3).

The decorated edge coordinates are quotiented into exact orbits, including
the endpoint reversal that occurs when an unordered edge wraps around zero.
For s=1 or 2 there are 24 complex orbit parameters; for s=0 there are 27.
An exact-looking finite solution would be exported for symbolic recovery.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares


N = 6
Q = 3
EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
COLORINGS = np.asarray(
    tuple(itertools.product(range(Q), repeat=N)), dtype=np.int8
)
TARGET = np.asarray(
    [float(len(set(coloring)) == 1) for coloring in COLORINGS]
)


def perfect_matchings(vertices=tuple(range(N))):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings())


def pfaffian_sign(matching):
    crossings = 0
    for index, (a, b) in enumerate(matching):
        for c, d in matching[index + 1 :]:
            crossings += int(a < c < b < d or c < a < d < b)
    return -1 if crossings % 2 else 1


MATCHING_SIGNS = tuple(map(pfaffian_sign, MATCHINGS))


def rotate_coordinate(coordinate, color_shift, vertex_step):
    edge, left_color, right_color = coordinate
    u, v = edge
    uu = (u + vertex_step) % N
    vv = (v + vertex_step) % N
    aa = (left_color + color_shift) % Q
    bb = (right_color + color_shift) % Q
    if uu > vv:
        uu, vv = vv, uu
        aa, bb = bb, aa
    return (uu, vv), aa, bb


def orbit_map(color_shift, vertex_step):
    coordinates = tuple(
        (edge, a, b) for edge in EDGES for a in range(Q) for b in range(Q)
    )
    unseen = set(coordinates)
    orbits = []
    while unseen:
        start = min(unseen)
        orbit = []
        current = start
        while current not in orbit:
            orbit.append(current)
            current = rotate_coordinate(current, color_shift, vertex_step)
        assert current == start
        for coordinate in orbit:
            unseen.remove(coordinate)
        orbits.append(tuple(orbit))
    coordinate_to_orbit = {
        coordinate: orbit_index
        for orbit_index, orbit in enumerate(orbits)
        for coordinate in orbit
    }
    return tuple(orbits), coordinate_to_orbit


def run(color_shift, vertex_step, seed, starts, max_nfev, scale, pfaffian):
    orbits, coordinate_to_orbit = orbit_map(color_shift, vertex_step)
    parameter_count = len(orbits)
    entry_orbit = np.empty((len(EDGES), Q, Q), dtype=np.int16)
    for edge in EDGES:
        for a in range(Q):
            for b in range(Q):
                entry_orbit[EDGE_INDEX[edge], a, b] = coordinate_to_orbit[
                    (edge, a, b)
                ]

    matching_columns = []
    for matching in MATCHINGS:
        columns = []
        for edge in matching:
            u, v = edge
            columns.append(
                entry_orbit[
                    EDGE_INDEX[edge], COLORINGS[:, u], COLORINGS[:, v]
                ]
            )
        matching_columns.append(tuple(columns))

    def amplitudes(z):
        answer = np.zeros(len(COLORINGS), dtype=z.dtype)
        for matching_index, columns in enumerate(matching_columns):
            sign = MATCHING_SIGNS[matching_index] if pfaffian else 1
            answer += sign * z[columns[0]] * z[columns[1]] * z[columns[2]]
        return answer

    def complex_jacobian(z):
        jacobian = np.zeros(
            (len(COLORINGS), parameter_count), dtype=z.dtype
        )
        rows = np.arange(len(COLORINGS))
        for matching_index, columns in enumerate(matching_columns):
            sign = MATCHING_SIGNS[matching_index] if pfaffian else 1
            for position in range(3):
                others = [index for index in range(3) if index != position]
                derivative = (
                    sign
                    * z[columns[others[0]]]
                    * z[columns[others[1]]]
                )
                np.add.at(jacobian, (rows, columns[position]), derivative)
        return jacobian

    rng = np.random.default_rng(seed)
    print(
        f"shift={color_shift} vertex_step={vertex_step} "
        f"parameters={parameter_count} "
        f"orbit_sizes={sorted(map(len, orbits))}",
        flush=True,
    )
    for offset in range(starts):
        initial = rng.normal(scale=scale, size=2 * parameter_count)

        def decode(x):
            return x[:parameter_count] + 1j * x[parameter_count:]

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
        value = residual(fit.x)
        complex_value = value[: len(TARGET)] + 1j * value[len(TARGET) :]
        norm = np.linalg.norm(fit.x)
        maximum = np.max(np.abs(complex_value))
        print(
            f"start={seed + offset} cost={fit.cost:.10g} max={maximum:.5g} "
            f"norm={norm:.5g} optimality={fit.optimality:.3g} "
            f"nfev={fit.nfev}",
            flush=True,
        )
        if maximum < 1e-4 and norm < 1e5:
            np.savez(
                f"candidate_cyclic_shift{color_shift}_seed{seed + offset}.npz",
                parameters=decode(fit.x),
                entry_orbit=entry_orbit,
                residual=complex_value,
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shift", type=int, choices=(0, 1, 2), default=1)
    parser.add_argument("--vertex-step", type=int, choices=(1, 2), default=1)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--max-nfev", type=int, default=5000)
    parser.add_argument("--scale", type=float, default=0.3)
    parser.add_argument(
        "--pfaffian",
        action="store_true",
        help="use canonical Pfaffian matching signs instead of the hafnian sum",
    )
    args = parser.parse_args()
    run(
        args.shift,
        args.vertex_step,
        args.seed,
        args.starts,
        args.max_nfev,
        args.scale,
        args.pfaffian,
    )


if __name__ == "__main__":
    main()
