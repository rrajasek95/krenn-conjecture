#!/usr/bin/env python3
"""Search for exact monomial cancellation by root-of-unity pairing.

This strengthens ``search_monomial_no_singleton_sat.py``.  In addition to
choosing absent/ordered-label edge states, it gives every supported edge a
phase in Z/modulus and pairs all mixed perfect matchings.  Paired matchings
must induce the same named-vertex coloring and have monomial phases differing
by ``modulus/2``.  Their contributions therefore cancel exactly.

Constant fibers may also be paired, except that each color must leave at
least one phase-zero matching unpaired.  Thus every mixed coefficient is
zero while each constant coefficient is a positive integer.

The n=8 instances are finite sufficient searches for a weighted
counterexample; UNSAT does not exclude cancellation of an unpaired fiber
with more than two terms.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product

try:
    from pysat.solvers import Solver
except ImportError as error:  # pragma: no cover - dependency diagnostic
    raise SystemExit(
        "python-sat is required; run with `uv run --with python-sat python ...`"
    ) from error

from search_monomial_no_singleton_sat import (
    ABSENT,
    Q,
    VariablePool,
    colored_triple_orbits,
    edge_state,
    perfect_matchings,
)


def exactly_one(clauses, literals):
    clauses.append(list(literals))
    clauses.extend([-left, -right] for left, right in combinations(literals, 2))


def modular_matching_phase(clauses, pool, edge_phases, edge_numbers, modulus):
    """One-hot phase for the modular sum of the listed edge phases."""

    previous = edge_phases[edge_numbers[0]]
    for edge_number in edge_numbers[1:]:
        current = [pool.new() for _ in range(modulus)]
        exactly_one(clauses, current)
        for left, right in product(range(modulus), repeat=2):
            clauses.append([
                -previous[left],
                -edge_phases[edge_number][right],
                current[(left + right) % modulus],
            ])
        previous = current
    return previous


def sequential_at_most_one(clauses, pool, literals):
    previous = None
    for literal in literals:
        current = pool.new()
        clauses.append([-literal, current])
        if previous is not None:
            clauses.extend(([-previous, current], [-literal, -previous]))
        previous = current


def build_formula(size: int, targets, modulus: int):
    vertices = tuple(range(size))
    edges = tuple(combinations(vertices, 2))
    edge_index = {edge: index for index, edge in enumerate(edges)}
    matchings = tuple(perfect_matchings(vertices))
    pool = VariablePool()
    clauses: list[list[int]] = []

    states = [[pool.new() for _ in range(1 + Q * Q)] for _ in edges]
    edge_phases = [[pool.new() for _ in range(modulus)] for _ in edges]
    for variables in states:
        exactly_one(clauses, variables)
    for variables in edge_phases:
        exactly_one(clauses, variables)

    endpoint = {}
    for edge_number, _edge in enumerate(edges):
        for side in range(2):
            for color in range(Q):
                indicator = endpoint[edge_number, side, color] = pool.new()
                labels = [
                    states[edge_number][edge_state((left, right))]
                    for left, right in product(range(Q), repeat=2)
                    if (left, right)[side] == color
                ]
                clauses.append([-indicator] + labels)
                clauses.extend([-label, indicator] for label in labels)

    for color, matching in enumerate(targets):
        for edge in matching:
            clauses.append([states[edge_index[edge]][edge_state((color, color))]])

    supported = []
    constant = []
    matching_phases = []
    unpaired = []
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
            [-support, -states[edge_index[edge]][ABSENT]] for edge in matching
        )
        clauses.append(
            [support] + [states[edge_index[edge]][ABSENT] for edge in matching]
        )

        witnesses = []
        for color in range(Q):
            witness = pool.new()
            witnesses.append(witness)
            constant_state = edge_state((color, color))
            clauses.extend(
                [-witness, states[edge_index[edge]][constant_state]]
                for edge in matching
            )
            clauses.append(
                [witness]
                + [-states[edge_index[edge]][constant_state] for edge in matching]
            )
        constant.append(witnesses)
        matching_phase = modular_matching_phase(
            clauses,
            pool,
            edge_phases,
            [edge_index[edge] for edge in matching],
            modulus,
        )
        matching_phases.append(matching_phase)
        unpaired_row = []
        for color, witness in enumerate(witnesses):
            unpaired_witness = pool.new()
            unpaired_row.append(unpaired_witness)
            clauses.extend((
                [-unpaired_witness, witness],
                [-unpaired_witness, matching_phase[0]],
            ))
        unpaired.append(unpaired_row)

    # At least one positive unpaired matching survives in each constant
    # fiber.  All remaining constant matchings may cancel in pairs below.
    for color in range(Q):
        clauses.append([row[color] for row in unpaired])

    pairs = {}
    incident_pairs = [[] for _ in matchings]
    half_turn = modulus // 2
    for first, second in combinations(range(len(matchings)), 2):
        pair = pairs[first, second] = pool.new()
        incident_pairs[first].append(pair)
        incident_pairs[second].append(pair)
        clauses.extend(([-pair, supported[first]], [-pair, supported[second]]))

        for phase in range(modulus):
            clauses.append([
                -pair,
                -matching_phases[first][phase],
                matching_phases[second][(phase + half_turn) % modulus],
            ])

        for vertex in vertices:
            edge_a, side_a = incidence[first][vertex]
            edge_b, side_b = incidence[second][vertex]
            if edge_a == edge_b:
                continue
            for color in range(Q):
                color_a = endpoint[edge_a, side_a, color]
                color_b = endpoint[edge_b, side_b, color]
                clauses.extend(([-pair, -color_a, color_b],
                                [-pair, -color_b, color_a]))

    for matching_number in range(len(matchings)):
        clauses.append(
            [-supported[matching_number]]
            + unpaired[matching_number]
            + incident_pairs[matching_number]
        )
        sequential_at_most_one(
            clauses,
            pool,
            unpaired[matching_number] + incident_pairs[matching_number],
        )

    return (
        pool.top,
        clauses,
        states,
        edge_phases,
        edges,
        edge_index,
        matchings,
    )


def verify_model(size, modulus, positive, data):
    _, _, states, edge_phases, edges, edge_index, matchings = data
    state_values = [
        next(value for value, variable in enumerate(row) if variable in positive)
        for row in states
    ]
    phase_values = [
        next(value for value, variable in enumerate(row) if variable in positive)
        for row in edge_phases
    ]
    fibers = {}
    for matching in matchings:
        if any(state_values[edge_index[edge]] == ABSENT for edge in matching):
            continue
        coloring = [-1] * size
        phase = 0
        for u, v in matching:
            number = edge_index[u, v]
            coloring[u], coloring[v] = divmod(state_values[number] - 1, Q)
            phase += phase_values[number]
        fibers.setdefault(tuple(coloring), []).append(phase % modulus)

    for coloring, phases in fibers.items():
        counts = [phases.count(phase) for phase in range(modulus)]
        if len(set(coloring)) > 1:
            assert all(
                counts[phase] == counts[(phase + modulus // 2) % modulus]
                for phase in range(modulus)
            )
        else:
            half_turn = modulus // 2
            assert counts[0] > counts[half_turn]
            assert all(
                counts[phase] == counts[(phase + half_turn) % modulus]
                for phase in range(1, half_turn)
            )
    return state_values, phase_values, fibers


def run(size: int, modulus: int) -> None:
    orbits = colored_triple_orbits(size)
    print(f"n={size}, modulus={modulus}: {len(orbits)} triple orbits")
    for orbit, targets in enumerate(orbits):
        data = build_formula(size, targets, modulus)
        variables, clauses = data[:2]
        with Solver(name="cadical195", bootstrap_with=clauses) as solver:
            satisfiable = solver.solve()
            print(
                f"  orbit {orbit}: {'SAT' if satisfiable else 'UNSAT'} "
                f"({variables} variables, {len(clauses)} clauses)",
                flush=True,
            )
            if not satisfiable:
                continue
            positive = {literal for literal in solver.get_model() if literal > 0}
        state_values, phase_values, fibers = verify_model(
            size, modulus, positive, data
        )
        print("  targets:", targets)
        for edge, state_value, phase in zip(data[4], state_values, phase_values):
            if state_value != ABSENT:
                print(
                    "   ", edge, divmod(state_value - 1, Q),
                    f"phase={phase}/{modulus}",
                )
        print("  supported coloring fibers:", len(fibers))
        return
    print("  all orbits UNSAT")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, choices=(6, 8), default=8)
    parser.add_argument("--modulus", type=int, choices=(2, 4, 8), default=2)
    arguments = parser.parse_args()
    run(arguments.n, arguments.modulus)


if __name__ == "__main__":
    main()
