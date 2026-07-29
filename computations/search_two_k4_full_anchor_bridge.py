#!/usr/bin/env python3
"""Search the unresolved full-anchor two-K4 bridge chart at n=8.

Vertices 0 and 4 are the anchors of two standard K4 realizations of
Delta_4.  The variable edges are all nine nonanchor-to-nonanchor bridges
and the anchor edge 04, each with an arbitrary 3 by 3 matrix.  The latter
is precisely the full-rank case not covered by the coordinate-pure anchor
obstruction.  Numerical candidates require exact reconstruction.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import minimize


N, Q = 8, 3
EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {edge: number for number, edge in enumerate(EDGES)}
VARIABLE_EDGES = ((0, 4),) + tuple(
    (left, right) for left in (1, 2, 3) for right in (5, 6, 7)
)
VARIABLE_INDEX = {edge: number for number, edge in enumerate(VARIABLE_EDGES)}
COLORINGS = np.asarray(
    tuple(itertools.product(range(Q), repeat=N)), dtype=np.int8
)
TARGET = np.asarray([len(set(c)) == 1 for c in COLORINGS], dtype=float)
PARAMETERS = len(VARIABLE_EDGES) * Q * Q
CELL_KEYS = tuple(
    (edge, a, b)
    for edge in VARIABLE_EDGES
    for a, b in itertools.product(range(Q), repeat=2)
)
CELL_NUMBER = {key: number for number, key in enumerate(CELL_KEYS)}


def c3_action(key: tuple[tuple[int, int], int, int]):
    edge, a, b = key
    vertex_map = {0: 0, 1: 2, 2: 3, 3: 1, 4: 4, 5: 6, 6: 7, 7: 5}
    u, v = vertex_map[edge[0]], vertex_map[edge[1]]
    if u > v:
        u, v, a, b = v, u, b, a
    return ((u, v), (a + 1) % Q, (b + 1) % Q)


def c3_orbits():
    unseen = set(CELL_KEYS)
    result = []
    while unseen:
        start = min(unseen)
        orbit = []
        current = start
        while current not in orbit:
            orbit.append(current)
            current = c3_action(current)
        assert current == start and len(orbit) == 3
        unseen.difference_update(orbit)
        result.append(tuple(orbit))
    return tuple(result)


C3_ORBITS = c3_orbits()


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings(tuple(range(N))))


def fixed_matrices(dtype: np.dtype) -> np.ndarray:
    matrices = np.zeros((len(EDGES), Q, Q), dtype=dtype)
    for offset in (0, 4):
        anchor = offset
        nonanchors = (offset + 1, offset + 2, offset + 3)
        for color in range(Q):
            partner = nonanchors[color]
            others = tuple(vertex for vertex in nonanchors if vertex != partner)
            matrices[EDGE_INDEX[tuple(sorted((anchor, partner)))], color, color] = 1
            matrices[EDGE_INDEX[tuple(sorted(others))], color, color] = 1
    return matrices


def expand(z: np.ndarray) -> np.ndarray:
    matrices = fixed_matrices(z.dtype)
    blocks = z.reshape(len(VARIABLE_EDGES), Q, Q)
    for number, edge in enumerate(VARIABLE_EDGES):
        matrices[EDGE_INDEX[edge]] = blocks[number]
    return matrices


def value_gradient(
    z: np.ndarray, need_gradient: bool = True
) -> tuple[np.ndarray, np.ndarray | None]:
    matrices = expand(z)
    output = np.zeros(len(COLORINGS), dtype=z.dtype)
    cache: list[tuple[list[np.ndarray], list[tuple[tuple[int, int], np.ndarray, np.ndarray]]]] = []
    for matching in MATCHINGS:
        values: list[np.ndarray] = []
        slots: list[tuple[tuple[int, int], np.ndarray, np.ndarray]] = []
        for edge in matching:
            u, v = edge
            aa, bb = COLORINGS[:, u], COLORINGS[:, v]
            values.append(matrices[EDGE_INDEX[edge], aa, bb])
            slots.append((edge, aa, bb))
        output += np.prod(values, axis=0)
        if need_gradient:
            cache.append((values, slots))

    if not need_gradient:
        return output, None

    residual = output - TARGET
    gradient = np.zeros((len(VARIABLE_EDGES), Q, Q), dtype=z.dtype)
    for values, slots in cache:
        for position, (edge, aa, bb) in enumerate(slots):
            if edge not in VARIABLE_INDEX:
                continue
            derivative = np.ones(len(COLORINGS), dtype=z.dtype)
            for other, value in enumerate(values):
                if other != position:
                    derivative *= value
            np.add.at(
                gradient[VARIABLE_INDEX[edge]],
                (aa, bb),
                np.conjugate(residual) * derivative,
            )
    return output, gradient.reshape(-1)


def run(
    seed: int, maxiter: int, scale: float, real_search: bool, c3: bool
) -> None:
    rng = np.random.default_rng(seed)
    count = len(C3_ORBITS) if c3 else PARAMETERS

    def to_full(z: np.ndarray) -> np.ndarray:
        if not c3:
            return z
        result = np.zeros(PARAMETERS, dtype=z.dtype)
        for value, orbit in zip(z, C3_ORBITS, strict=True):
            for key in orbit:
                result[CELL_NUMBER[key]] = value
        return result

    def from_full(g: np.ndarray) -> np.ndarray:
        if not c3:
            return g
        return np.asarray(
            [sum(g[CELL_NUMBER[key]] for key in orbit) for orbit in C3_ORBITS]
        )

    if real_search:
        x0 = rng.normal(scale=scale, size=count)

        def decode(x: np.ndarray) -> np.ndarray:
            return x

        def objective(x: np.ndarray) -> tuple[float, np.ndarray]:
            output, gradient = value_gradient(to_full(x))
            assert gradient is not None
            residual = output - TARGET
            return (
                0.5 * float(np.vdot(residual, residual).real),
                from_full(gradient).real,
            )

    else:
        x0 = rng.normal(scale=scale, size=2 * count)

        def decode(x: np.ndarray) -> np.ndarray:
            return x[:count] + 1j * x[count:]

        def objective(x: np.ndarray) -> tuple[float, np.ndarray]:
            output, gradient = value_gradient(to_full(decode(x)))
            assert gradient is not None
            gradient = from_full(gradient)
            residual = output - TARGET
            loss = 0.5 * float(np.vdot(residual, residual).real)
            return loss, np.r_[gradient.real, -gradient.imag]

    fit = minimize(
        objective,
        x0,
        method="L-BFGS-B",
        jac=True,
        options={
            "maxiter": maxiter,
            "ftol": 1e-15,
            "gtol": 1e-11,
            "maxls": 60,
            "maxcor": 40,
        },
    )
    z = to_full(decode(fit.x))
    output, _ = value_gradient(z, need_gradient=False)
    residual = output - TARGET
    maximum = float(np.max(np.abs(residual)))
    print(
        f"seed={seed} nit={fit.nit} loss={0.5 * np.vdot(residual, residual).real:.12g} "
        f"max={maximum:.7g} norm={np.linalg.norm(z):.7g} "
        f"status={fit.status}",
        flush=True,
    )
    if maximum < 1e-7:
        np.savez(
            f"computations/candidate_two_k4_full_anchor_seed{seed}.npz",
            variable_edges=np.asarray(VARIABLE_EDGES),
            matrices=z.reshape(len(VARIABLE_EDGES), Q, Q),
            residual=residual,
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starts", type=int, default=1)
    parser.add_argument("--maxiter", type=int, default=5000)
    parser.add_argument("--scale", type=float, default=0.3)
    parser.add_argument("--real", action="store_true")
    parser.add_argument("--c3", action="store_true")
    args = parser.parse_args()
    for seed in range(args.seed, args.seed + args.starts):
        run(seed, args.maxiter, args.scale, args.real, args.c3)


if __name__ == "__main__":
    main()
