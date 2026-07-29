"""Enumerate maximal triples of K6 edge sets with no rainbow perfect matching.

This is a support-classification aid for the diagonal q=3 subproblem.  A
variable (color, edge) says that the corresponding diagonal aggregate entry
is nonzero.  Each forbidden rainbow perfect matching is a negative 3-clause.
"""

from __future__ import annotations

import itertools
import json

from pysat.solvers import Solver


VERTICES = tuple(range(6))
EDGES = list(itertools.combinations(VERTICES, 2))
EDGE_INDEX = {edge: idx for idx, edge in enumerate(EDGES)}


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for pos in range(1, len(vertices)):
        v = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for matching in perfect_matchings(rest):
            yield ((u, v),) + matching


MATCHINGS = list(perfect_matchings(VERTICES))


def variable(color: int, edge: tuple[int, int]) -> int:
    return 1 + color * len(EDGES) + EDGE_INDEX[edge]


def has_perfect_matching(model: set[int], color: int) -> bool:
    return any(all(variable(color, edge) in model for edge in matching) for matching in MATCHINGS)


def canonical_key(model: set[int]) -> tuple[int, ...]:
    masks = []
    for vertex_perm in itertools.permutations(VERTICES):
        edge_map = {
            edge: tuple(sorted((vertex_perm[edge[0]], vertex_perm[edge[1]])))
            for edge in EDGES
        }
        for color_perm in itertools.permutations(range(3)):
            mask = 0
            for color in range(3):
                for edge in EDGES:
                    if variable(color, edge) in model:
                        image = variable(color_perm[color], edge_map[edge]) - 1
                        mask |= 1 << image
            masks.append(mask)
    minimum = min(masks)
    return (minimum,)


def main() -> None:
    clauses = []
    for matching in MATCHINGS:
        for color_order in itertools.permutations(range(3)):
            clauses.append([
                -variable(color, edge)
                for color, edge in zip(color_order, matching, strict=True)
            ])

    maximal_models: list[set[int]] = []
    orbit_representatives: dict[tuple[int, ...], set[int]] = {}
    with Solver(name="g4", bootstrap_with=clauses) as solver:
        while solver.solve():
            positive = {literal for literal in solver.get_model() if literal > 0 and literal <= 45}
            for candidate in range(1, 46):
                if candidate in positive:
                    continue
                if solver.solve(assumptions=list(positive | {candidate})):
                    positive.add(candidate)
            maximal_models.append(positive)
            if all(has_perfect_matching(positive, color) for color in range(3)):
                orbit_representatives.setdefault(canonical_key(positive), positive)
            # Exclude this maximal model and all of its subsets.
            solver.add_clause([candidate for candidate in range(1, 46) if candidate not in positive])

    output = []
    for model in orbit_representatives.values():
        output.append([
            [list(EDGES[(var - 1) % len(EDGES)]) for var in sorted(model) if (var - 1) // len(EDGES) == color]
            for color in range(3)
        ])
    output.sort(key=lambda item: tuple(len(edges) for edges in item))
    print(f"maximal_models={len(maximal_models)} pm_orbits={len(output)}")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
