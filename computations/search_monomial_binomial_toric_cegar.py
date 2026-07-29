#!/usr/bin/env python3
"""CEGAR search for an exact binomial monomial realization at n=8.

Every underlying pair is absent or carries one ordered ternary endpoint
label and one nonzero scalar weight.  Three edge-disjoint perfect matchings
are fixed inside the constant-color fibers.  Every mixed fiber is required
to have either zero or exactly two supported perfect matchings.

For a two-term fiber M,N the coefficient equation is x^(M-N)=-1.  These
equations have a solution in (C*)^E iff their prescribed signs define a
character on the integer row lattice.  A Smith decomposition checks that
condition exactly.  When an odd integer relation is found, the precise
collection of binomial fibers used by the relation is blocked and SAT
resumes.  Constant fibers are left unrestricted: once their three sums are
nonzero, local diagonal gauges normalize them without disturbing any mixed
zero equation.

This is a discovery/exhaustion tool for the monomial-binomial n=8 chart;
it is not a proof for arbitrary aggregate matrices.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations

from pysat.solvers import Solver
from sympy import Matrix, ZZ
from sympy.polys.domains import ZZ as POLY_ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

from search_monomial_no_singleton_sat import (
    ABSENT,
    Q,
    build_formula,
    colored_triple_orbits,
    edge_state,
)


def required_literals(matching, coloring, state, edge_index):
    return tuple(
        state[edge_index[edge]][edge_state((coloring[edge[0]], coloring[edge[1]]))]
        for edge in matching
    )


def decode_states(model, state):
    positive = {literal for literal in model if literal > 0}
    return tuple(
        next(value for value, variable in enumerate(row) if variable in positive)
        for row in state
    )


def exact_fibers(size, states, edges, edge_index, matchings):
    fibers = {}
    for number, matching in enumerate(matchings):
        if any(states[edge_index[edge]] == ABSENT for edge in matching):
            continue
        coloring = [-1] * size
        for u, v in matching:
            coloring[u], coloring[v] = divmod(states[edge_index[u, v]] - 1, Q)
        fibers.setdefault(tuple(coloring), []).append(number)
    return fibers


def exponent_row(first, second, edge_index, edge_count):
    row = [0] * edge_count
    for edge in first:
        row[edge_index[edge]] += 1
    if second is not None:
        for edge in second:
            row[edge_index[edge]] -= 1
    return row


def smith_relation(rows, rhs):
    """Return an odd saturated integer relation, or None if consistent."""

    # Relations among rows are the integer kernel of rows^T.  If
    # S rows^T T is Smith diagonal, the zero-diagonal columns of the
    # unimodular T are a saturated Z-basis of that kernel.
    transpose = list(map(list, zip(*rows)))
    dm = DomainMatrix(
        [[POLY_ZZ(value) for value in row] for row in transpose],
        (len(transpose), len(rows)),
        POLY_ZZ,
    )
    diagonal, _left, right = smith_normal_decomp(dm)
    diagonal_matrix = diagonal.to_Matrix()
    right_matrix = right.to_Matrix()
    rank = sum(
        1
        for index in range(min(diagonal_matrix.rows, diagonal_matrix.cols))
        if diagonal_matrix[index, index] != 0
    )
    for column in range(rank, right_matrix.cols):
        relation = [int(right_matrix[row, column]) for row in range(right_matrix.rows)]
        if sum(coefficient * bit for coefficient, bit in zip(relation, rhs)) % 2:
            assert all(
                sum(relation[row] * rows[row][column] for row in range(len(rows))) == 0
                for column in range(len(rows[0]))
            )
            return relation
    return None


def exact_phase_solution(rows, rhs):
    """Construct rational y with rows*y = rhs (mod 2), after consistency."""

    dm = DomainMatrix(
        [[POLY_ZZ(value) for value in row] for row in rows],
        (len(rows), len(rows[0])),
        POLY_ZZ,
    )
    diagonal, left, right = smith_normal_decomp(dm)
    diagonal_matrix = diagonal.to_Matrix()
    left_matrix = left.to_Matrix()
    right_matrix = right.to_Matrix()
    transformed_rhs = left_matrix * Matrix(rhs)
    rank = sum(
        1
        for index in range(min(diagonal_matrix.rows, diagonal_matrix.cols))
        if diagonal_matrix[index, index] != 0
    )
    for row in range(rank, diagonal_matrix.rows):
        assert int(transformed_rhs[row]) % 2 == 0
    internal = [Fraction(0) for _ in range(diagonal_matrix.cols)]
    for index in range(rank):
        internal[index] = Fraction(
            int(transformed_rhs[index]), int(diagonal_matrix[index, index])
        )
    # D*T*y' = b, hence the original logarithmic phase vector is T*y'.
    phases = []
    for row in range(right_matrix.rows):
        phases.append(sum(Fraction(int(right_matrix[row, col])) * internal[col]
                          for col in range(right_matrix.cols)))
    for row, bit in zip(rows, rhs):
        value = sum(Fraction(a) * y for a, y in zip(row, phases)) - bit
        assert value.denominator == 1 and value.numerator % 2 == 0
    return phases


def add_unique_constant_clauses(solver, targets, state, edge_index, matchings):
    target_sets = [set(matching) for matching in targets]
    for color in range(Q):
        constant_state = edge_state((color, color))
        for matching in matchings:
            if set(matching) == target_sets[color]:
                continue
            solver.add_clause([
                -state[edge_index[edge]][constant_state] for edge in matching
            ])


def run_orbit(
    size, orbit, targets, max_rounds, unique_constants=False,
    verbose_certificates=False,
):
    variables, clauses, state, edges, edge_index, matchings = build_formula(size, targets)
    solver = Solver(name="cadical195", bootstrap_with=clauses)
    if unique_constants:
        add_unique_constant_clauses(solver, targets, state, edge_index, matchings)
    learned_large = 0
    learned_lattice = 0

    for round_number in range(max_rounds):
        if not solver.solve():
            solver.delete()
            return None, (round_number, learned_large, learned_lattice)
        states = decode_states(solver.get_model(), state)
        fibers = exact_fibers(size, states, edges, edge_index, matchings)

        large = [
            (coloring, members)
            for coloring, members in fibers.items()
            if len(set(coloring)) > 1 and len(members) > 2
        ]
        if large:
            # At-most-two is learned from concrete triples.  The clause is
            # exact: retaining all required edge labels retains three terms
            # in this named coloring fiber.
            for coloring, members in large:
                for triple in combinations(members, 3):
                    literals = {
                        literal
                        for number in triple
                        for literal in required_literals(
                            matchings[number], coloring, state, edge_index
                        )
                    }
                    solver.add_clause([-literal for literal in literals])
                    learned_large += 1
            continue

        binomial = sorted(
            (coloring, tuple(members))
            for coloring, members in fibers.items()
            if len(set(coloring)) > 1
        )
        assert all(len(members) == 2 for _, members in binomial)
        rows = []
        rhs = []
        for _coloring, (first, second) in binomial:
            rows.append(exponent_row(
                matchings[first], matchings[second], edge_index, len(edges)
            ))
            rhs.append(1)

        relation = smith_relation(rows, rhs)
        if relation is None:
            phases = exact_phase_solution(rows, rhs)
            solver.delete()
            return (states, fibers, phases, edges), (
                round_number, learned_large, learned_lattice
            )

        used = [index for index in range(len(rows)) if relation[index] != 0]
        assert used
        if verbose_certificates:
            print(f"  odd relation {learned_lattice + 1}:", flush=True)
            for index in used:
                coloring, members = binomial[index]
                print(
                    f"    {relation[index]:+d} coloring={''.join(map(str, coloring))} "
                    f"matchings={matchings[members[0]]},{matchings[members[1]]}",
                    flush=True,
                )
        literals = set()
        for index in used:
            coloring, members = binomial[index]
            for number in members:
                literals.update(required_literals(
                    matchings[number], coloring, state, edge_index
                ))
        solver.add_clause([-literal for literal in literals])
        learned_lattice += 1

        if round_number % 100 == 0:
            distribution = Counter(len(members) for members in fibers.values())
            print(
                f"orbit={orbit} round={round_number} fibers={len(fibers)} "
                f"distribution={dict(sorted(distribution.items()))} "
                f"large_cuts={learned_large} lattice_cuts={learned_lattice}",
                flush=True,
            )

    solver.delete()
    raise RuntimeError(f"orbit {orbit} reached max_rounds={max_rounds}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, choices=(6, 8), default=8)
    parser.add_argument("--orbit", type=int)
    parser.add_argument("--max-rounds", type=int, default=100000)
    parser.add_argument("--unique-constants", action="store_true")
    parser.add_argument("--verbose-certificates", action="store_true")
    args = parser.parse_args()

    orbits = colored_triple_orbits(args.n)
    indices = range(len(orbits)) if args.orbit is None else (args.orbit,)
    print(f"n={args.n} orbits={len(orbits)}", flush=True)
    for orbit in indices:
        result, stats = run_orbit(
            args.n,
            orbit,
            orbits[orbit],
            args.max_rounds,
            args.unique_constants,
            args.verbose_certificates,
        )
        print(f"orbit={orbit} {'SAT' if result else 'UNSAT'} stats={stats}", flush=True)
        if result is None:
            continue
        states, fibers, phases, edges = result
        print("targets=", orbits[orbit])
        print("fiber_distribution=", dict(sorted(Counter(map(len, fibers.values())).items())))
        for edge, state_value, phase in zip(edges, states, phases):
            if state_value != ABSENT:
                print(edge, divmod(state_value - 1, Q), f"phase={phase}*pi")
        return
    print("all selected orbits UNSAT")


if __name__ == "__main__":
    main()
