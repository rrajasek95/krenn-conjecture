#!/usr/bin/env python3
"""Exact SAT search for monomial labelings with no mixed singleton fiber.

Each underlying edge has ten states: absent, or one of the nine ordered
endpoint-color labels in {0,1,2}^2.  Three edge-disjoint perfect matchings
are fixed to the constant labels (0,0), (1,1), and (2,2).  The SAT formula
requires every supported nonconstant perfect matching to have a distinct
supported perfect matching inducing exactly the same vertex coloring.

Run with an ephemeral dependency if python-sat is not installed:

    uv run --with python-sat python \
      computations/search_monomial_no_singleton_sat.py

The search proves both colored n=6 triple types unsatisfiable and finds the
K_8 counterexample audited by verify_monomial_n8_counterexample.py.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, permutations, product

try:
    from pysat.solvers import Solver
except ImportError as error:  # pragma: no cover - dependency diagnostic
    raise SystemExit(
        "python-sat is required; run with `uv run --with python-sat python ...`"
    ) from error


Q = 3
ABSENT = 0


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + matching))


def canonical_matching(size: int):
    return tuple((2 * index, 2 * index + 1) for index in range(size // 2))


def stabilizer_of_canonical_matching(size: int):
    half = size // 2
    for pair_permutation in permutations(range(half)):
        for flips in product(range(2), repeat=half):
            vertex_permutation = [0] * size
            for pair in range(half):
                for bit in range(2):
                    vertex_permutation[2 * pair + bit] = (
                        2 * pair_permutation[pair] + (bit ^ flips[pair])
                    )
            yield tuple(vertex_permutation)


def relabel_matching(matching, vertex_permutation):
    return tuple(sorted(
        (min(vertex_permutation[u], vertex_permutation[v]),
         max(vertex_permutation[u], vertex_permutation[v]))
        for u, v in matching
    ))


def colored_triple_orbits(size: int):
    """Fix color 0 canonically and quotient by its stabilizer and 1<->2."""

    vertices = tuple(range(size))
    matchings = tuple(perfect_matchings(vertices))
    first = canonical_matching(size)
    first_edges = set(first)
    stabilizer = tuple(stabilizer_of_canonical_matching(size))

    def canonical_pair(second, third):
        forms = []
        for vertex_permutation in stabilizer:
            image_second = relabel_matching(second, vertex_permutation)
            image_third = relabel_matching(third, vertex_permutation)
            forms.extend(((image_second, image_third),
                          (image_third, image_second)))
        return min(forms)

    representatives = {
        canonical_pair(second, third)
        for second in matchings
        if not first_edges & set(second)
        for third in matchings
        if not first_edges & set(third) and not set(second) & set(third)
    }
    return tuple((first,) + pair for pair in sorted(representatives))


class VariablePool:
    def __init__(self):
        self.top = 0

    def new(self):
        self.top += 1
        return self.top


def edge_state(label: tuple[int, int]) -> int:
    return 1 + Q * label[0] + label[1]


def build_formula(size: int, targets):
    vertices = tuple(range(size))
    edges = tuple(combinations(vertices, 2))
    edge_index = {edge: index for index, edge in enumerate(edges)}
    matchings = tuple(perfect_matchings(vertices))
    pool = VariablePool()
    clauses: list[list[int]] = []

    # Exactly one of absent and the nine labels is selected on every pair.
    state = [[pool.new() for _ in range(1 + Q * Q)] for _ in edges]
    for variables in state:
        clauses.append(variables.copy())
        clauses.extend([-left, -right] for left, right in combinations(variables, 2))

    # Endpoint-color indicators, derived exactly from the edge state.
    endpoint = {}
    for edge_number, _edge in enumerate(edges):
        for side in range(2):
            for color in range(Q):
                indicator = endpoint[edge_number, side, color] = pool.new()
                labels = [
                    state[edge_number][edge_state((left, right))]
                    for left, right in product(range(Q), repeat=2)
                    if (left, right)[side] == color
                ]
                clauses.append([-indicator] + labels)
                clauses.extend([-label, indicator] for label in labels)

    for color, matching in enumerate(targets):
        for edge in matching:
            clauses.append([state[edge_index[edge]][edge_state((color, color))]])

    supported = []
    constant_witnesses = []
    incidence = []
    for matching in matchings:
        local_incidence = {}
        for u, v in matching:
            local_incidence[u] = (edge_index[u, v], 0)
            local_incidence[v] = (edge_index[u, v], 1)
        incidence.append(local_incidence)

        support = pool.new()
        supported.append(support)
        clauses.extend(
            [-support, -state[edge_index[edge]][ABSENT]] for edge in matching
        )
        clauses.append(
            [support] + [state[edge_index[edge]][ABSENT] for edge in matching]
        )

        witnesses = []
        for color in range(Q):
            witness = pool.new()
            witnesses.append(witness)
            clauses.extend(
                [-witness, state[edge_index[edge]][edge_state((color, color))]]
                for edge in matching
            )
        constant_witnesses.append(witnesses)

    # A same-coloring witness may be true only for two supported matchings
    # whose endpoint colors agree at every named vertex.  The reverse
    # implication is unnecessary: a satisfying labeling can simply enable
    # the witnesses it uses in the coverage clauses below.
    same_witness = {}
    for first, second in combinations(range(len(matchings)), 2):
        witness = same_witness[first, second] = pool.new()
        clauses.extend(([-witness, supported[first]],
                        [-witness, supported[second]]))
        for vertex in vertices:
            edge_a, side_a = incidence[first][vertex]
            edge_b, side_b = incidence[second][vertex]
            if edge_a == edge_b:
                continue
            for color in range(Q):
                color_a = endpoint[edge_a, side_a, color]
                color_b = endpoint[edge_b, side_b, color]
                clauses.extend(([-witness, -color_a, color_b],
                                [-witness, -color_b, color_a]))

    for first in range(len(matchings)):
        mates = [
            same_witness[min(first, second), max(first, second)]
            for second in range(len(matchings))
            if first != second
        ]
        clauses.append(
            [-supported[first]] + constant_witnesses[first] + mates
        )

    return pool.top, clauses, state, edges, edge_index, matchings


def verify_model(size, model_states, edges, edge_index, matchings):
    fibers = Counter()
    for matching in matchings:
        if any(model_states[edge_index[edge]] == ABSENT for edge in matching):
            continue
        coloring = [-1] * size
        for u, v in matching:
            label = divmod(model_states[edge_index[u, v]] - 1, Q)
            coloring[u], coloring[v] = label
        fibers[tuple(coloring)] += 1
    mixed_singletons = [
        coloring for coloring, multiplicity in fibers.items()
        if len(set(coloring)) > 1 and multiplicity == 1
    ]
    assert not mixed_singletons
    return fibers


def solve_orbit(size: int, targets):
    variables, clauses, state, edges, edge_index, matchings = build_formula(
        size, targets
    )
    with Solver(name="cadical195", bootstrap_with=clauses) as solver:
        satisfiable = solver.solve()
        if not satisfiable:
            return None, variables, len(clauses)
        positive = {literal for literal in solver.get_model() if literal > 0}
    model_states = [
        next(value for value, variable in enumerate(variables_for_edge)
             if variable in positive)
        for variables_for_edge in state
    ]
    fibers = verify_model(size, model_states, edges, edge_index, matchings)
    return (model_states, edges, fibers), variables, len(clauses)


def run(size: int) -> None:
    orbits = colored_triple_orbits(size)
    print(f"n={size}: {len(orbits)} colored triple orbits")
    found = None
    for orbit, targets in enumerate(orbits):
        result, variables, clauses = solve_orbit(size, targets)
        print(
            f"  orbit {orbit}: {'SAT' if result else 'UNSAT'} "
            f"({variables} variables, {clauses} clauses)"
        )
        if result:
            found = orbit, targets, result
            break

    if size == 6:
        assert found is None
        print("  verified: every n=6 labeling has a mixed singleton")
        return

    assert found is not None
    orbit, targets, (model_states, edges, fibers) = found
    print(f"  first counterexample is on orbit {orbit}; target matchings={targets}")
    print("  fiber-size distribution:", dict(sorted(Counter(fibers.values()).items())))
    for edge, state_value in zip(edges, model_states):
        if state_value != ABSENT:
            print("   ", edge, divmod(state_value - 1, Q))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", choices=("6", "8", "both"), default="both")
    arguments = parser.parse_args()
    if arguments.n in ("6", "both"):
        run(6)
    if arguments.n in ("8", "both"):
        run(8)


if __name__ == "__main__":
    main()
