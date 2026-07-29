#!/usr/bin/env python3
"""Discovery search for the extremal twelve-vertex planar support.

The graph is C4 x P3.  Its middle C4 vertices have degree four and the
eight outer vertices have degree three.  Cubic-vertex rigidity forces each
edge incident with an outer vertex to be a same-colour basis edge, with the
three colours occurring once at every outer vertex.  Only the four middle
cycle matrices remain arbitrary.  This script enumerates the proper shell
edge-colourings and numerically solves the resulting (at most quadratic)
coefficient equations.

It is a discovery tool only: a small numerical residual is not a proof.
"""

from __future__ import annotations

import argparse
import itertools
from collections import defaultdict

import numpy as np
from scipy.optimize import least_squares


Q = 3
CORE = tuple(range(4))
INNER = tuple(range(4, 8))
OUTER = tuple(range(8, 12))
VERTICES = CORE + INNER + OUTER
CORE_EDGES = tuple(tuple(sorted((i, (i + 1) % 4))) for i in CORE)
CORE_INDEX = {edge: index for index, edge in enumerate(CORE_EDGES)}


def cycle_edges(base: int) -> tuple[tuple[int, int], ...]:
    return tuple(
        tuple(sorted((base + i, base + (i + 1) % 4))) for i in range(4)
    )


INNER_EDGES = cycle_edges(4)
OUTER_EDGES = cycle_edges(8)
INNER_SPOKES = tuple((i, 4 + i) for i in CORE)
OUTER_SPOKES = tuple((i, 8 + i) for i in CORE)
EDGES = set(
    CORE_EDGES + INNER_EDGES + OUTER_EDGES + INNER_SPOKES + OUTER_SPOKES
)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        edge = tuple(sorted((first, second)))
        if edge not in EDGES:
            continue
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield (edge,) + tail


MATCHINGS = tuple(perfect_matchings(VERTICES))


def shell_colourings():
    """Return (cycle-edge colours, spoke colours) for a cubic C4 shell."""
    answer = []
    for edge_colours in itertools.product(range(Q), repeat=4):
        if any(edge_colours[i] == edge_colours[(i - 1) % 4] for i in CORE):
            continue
        spoke_colours = tuple(
            3 - edge_colours[i] - edge_colours[(i - 1) % 4] for i in CORE
        )
        answer.append((edge_colours, spoke_colours))
    return tuple(answer)


SHELL_COLOURINGS = shell_colourings()


def shell_edge_map(inner_index: int, outer_index: int) -> dict[tuple[int, int], int]:
    inner_cycle, inner_spokes = SHELL_COLOURINGS[inner_index]
    outer_cycle, outer_spokes = SHELL_COLOURINGS[outer_index]
    answer = {}
    answer.update(zip(INNER_EDGES, inner_cycle, strict=True))
    answer.update(zip(OUTER_EDGES, outer_cycle, strict=True))
    answer.update(zip(INNER_SPOKES, inner_spokes, strict=True))
    answer.update(zip(OUTER_SPOKES, outer_spokes, strict=True))
    return answer


def build_rows(inner_index: int, outer_index: int):
    """Sparse coefficient rows as lists of core-variable monomials."""
    shell = shell_edge_map(inner_index, outer_index)
    rows: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for matching in MATCHINGS:
        core = tuple(edge for edge in matching if edge in CORE_INDEX)
        fixed = [-1] * len(VERTICES)
        consistent = True
        for edge in matching:
            if edge in CORE_INDEX:
                continue
            colour = shell[edge]
            for vertex in edge:
                if fixed[vertex] not in (-1, colour):
                    consistent = False
                fixed[vertex] = colour
        if not consistent:
            continue
        for endpoint_colours in itertools.product(range(Q), repeat=2 * len(core)):
            colouring = fixed.copy()
            monomial = []
            for position, edge in enumerate(core):
                a, b = endpoint_colours[2 * position : 2 * position + 2]
                u, v = edge
                if colouring[u] not in (-1, a) or colouring[v] not in (-1, b):
                    consistent = False
                    break
                colouring[u] = a
                colouring[v] = b
                monomial.append(CORE_INDEX[edge] * Q * Q + a * Q + b)
            if consistent:
                assert -1 not in colouring
                rows[tuple(colouring)].append(tuple(monomial))
            consistent = True
    for colour in range(Q):
        rows.setdefault((colour,) * len(VERTICES), [])
    colourings = tuple(rows)
    monomials = tuple(tuple(rows[colouring]) for colouring in colourings)
    target = np.asarray([len(set(colouring)) == 1 for colouring in colourings])
    return colourings, monomials, target


def viable_constant_support(inner_index: int, outer_index: int) -> bool:
    _, monomials, target = build_rows(inner_index, outer_index)
    return all(monomials[i] for i, value in enumerate(target) if value)


def solve_pair(inner_index: int, outer_index: int, seed: int, max_nfev: int):
    colourings, monomials, target = build_rows(inner_index, outer_index)
    variables = len(CORE_EDGES) * Q * Q

    def complex_values(z: np.ndarray) -> np.ndarray:
        answer = np.zeros(len(monomials), dtype=complex)
        for row, terms in enumerate(monomials):
            answer[row] = sum(np.prod(z[list(term)]) for term in terms)
        return answer

    def complex_jacobian(z: np.ndarray) -> np.ndarray:
        answer = np.zeros((len(monomials), variables), dtype=complex)
        for row, terms in enumerate(monomials):
            for term in terms:
                for position, column in enumerate(term):
                    product = 1.0 + 0.0j
                    for other_position, other in enumerate(term):
                        if other_position != position:
                            product *= z[other]
                    answer[row, column] += product
        return answer

    rng = np.random.default_rng(seed)
    initial_z = rng.normal(scale=0.4, size=variables) + 1j * rng.normal(
        scale=0.4, size=variables
    )
    initial = np.r_[initial_z.real, initial_z.imag]

    def decode(x: np.ndarray) -> np.ndarray:
        return x[:variables] + 1j * x[variables:]

    def residual(x: np.ndarray) -> np.ndarray:
        value = complex_values(decode(x)) - target
        return np.r_[value.real, value.imag]

    def jacobian(x: np.ndarray) -> np.ndarray:
        value = complex_jacobian(decode(x))
        return np.block([[value.real, -value.imag], [value.imag, value.real]])

    fit = least_squares(
        residual,
        initial,
        jac=jacobian,
        max_nfev=max_nfev,
        ftol=1e-13,
        xtol=1e-13,
        gtol=1e-13,
    )
    raw = complex_values(decode(fit.x)) - target
    maximum = float(np.max(np.abs(raw)))
    print(
        f"inner={inner_index} outer={outer_index} rows={len(colourings)} "
        f"seed={seed} max={maximum:.5g} cost={fit.cost:.8g} "
        f"norm={np.linalg.norm(fit.x):.5g} nfev={fit.nfev}",
        flush=True,
    )
    if maximum < 1e-7 and np.linalg.norm(fit.x) < 1e5:
        np.savez(
            f"candidate_planar_c4xp3_i{inner_index}_o{outer_index}_s{seed}.npz",
            inner=np.asarray(SHELL_COLOURINGS[inner_index]),
            outer=np.asarray(SHELL_COLOURINGS[outer_index]),
            matrices=decode(fit.x).reshape(len(CORE_EDGES), Q, Q),
            residual=raw,
        )
    return maximum


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inner", type=int)
    parser.add_argument("--outer", type=int)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starts", type=int, default=1)
    parser.add_argument("--max-nfev", type=int, default=2000)
    parser.add_argument("--scan", action="store_true")
    args = parser.parse_args()

    if args.scan:
        pairs = [
            (inner, outer)
            for inner in range(len(SHELL_COLOURINGS))
            for outer in range(len(SHELL_COLOURINGS))
            if viable_constant_support(inner, outer)
        ]
    else:
        if args.inner is None or args.outer is None:
            raise SystemExit("give --inner and --outer, or use --scan")
        pairs = [(args.inner, args.outer)]
    print(f"matchings={len(MATCHINGS)} viable_pairs={len(pairs)}")
    for inner, outer in pairs:
        for seed in range(args.seed, args.seed + args.starts):
            solve_pair(inner, outer, seed, args.max_nfev)


if __name__ == "__main__":
    main()
