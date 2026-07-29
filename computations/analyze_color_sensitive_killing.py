#!/usr/bin/env python3
"""Analyze the exact color-sensitive edge-deletion identity on SAT charts.

This is a discovery/audit helper.  For a Boolean support chart retained by
the rank-graph relaxation, it computes the largest collection of underlying
edges that can simultaneously be killed by diagonal infinitesimal target
stabilizers.  All linear algebra is over Q (SymPy), so a reported deletion
is exact.  The support chart is only a necessary relaxation; survivors are
not asserted to be realizations.
"""

from __future__ import annotations

import itertools

import sympy as sp
from pysat.solvers import Solver

import search_f5_support_sat as base
import verify_f4_support_obstruction as transfers


def support_chart(exceptional):
    formula, pool, active = base.support_formula(exceptional)
    signatures = transfers.formal_signatures(exceptional, pool)
    with Solver(name="cadical195", bootstrap_with=formula) as solver:
        survives, count = transfers.add_cancellation_transfers(
            solver, pool, signatures
        )
        if not survives:
            return None, count
        model = {literal for literal in solver.get_model() if literal > 0}
    supports = {}
    for u, v in base.ALL_EDGES:
        if (u, v) in exceptional:
            cells = {
                (a, b)
                for a, b in base.CELLS
                if pool.id(("entry", (u, v), a, b)) in model
            }
        else:
            left = {
                a
                for a in base.COLORS
                if pool.id(("factor", v, u, a)) in model
            }
            right = {
                b
                for b in base.COLORS
                if pool.id(("factor", u, v, b)) in model
            }
            cells = set(itertools.product(left, right))
        if cells:
            supports[u, v] = cells
    return supports, count


def equation_row(u, v, a, b):
    row = [0] * 18
    row[3 * u + a] = 1
    row[3 * v + b] = 1
    return row


SUM_ROWS = tuple(
    [int(index % 3 == color) for index in range(18)]
    for color in range(3)
)


def can_kill(supports, killed):
    rows = []
    rhs = []
    for edge in killed:
        u, v = edge
        for a, b in supports[edge]:
            rows.append(equation_row(u, v, a, b))
            rhs.append(0)
    rows.extend(SUM_ROWS)
    rhs.extend((1, 1, 1))
    matrix = sp.Matrix(rows)
    augmented = matrix.row_join(sp.Matrix(rhs))
    return matrix.rank() == augmented.rank()


def affine_solution(supports, killed):
    rows = []
    rhs = []
    for edge in killed:
        u, v = edge
        for a, b in supports[edge]:
            rows.append(equation_row(u, v, a, b))
            rhs.append(0)
    rows.extend(SUM_ROWS)
    rhs.extend((1, 1, 1))
    return sp.linsolve((sp.Matrix(rows), sp.Matrix(rhs)))


def maximum_kill(supports):
    edges = tuple(supports)
    for size in range(len(edges), -1, -1):
        for killed in itertools.combinations(edges, size):
            if can_kill(supports, killed):
                return killed
    raise AssertionError


def main():
    graph_families = [
        ("3P2", {(0, 1), (2, 3), (4, 5)}),
        ("P4+2P1", {(0, 1), (1, 2), (2, 3)}),
        ("P3+P2+P1", {(0, 1), (1, 2), (3, 4)}),
        ("P2+4P1", {(0, 1)}),
        ("empty", set()),
    ]
    for name, exceptional in graph_families:
        supports, count = support_chart(exceptional)
        if supports is None:
            print(f"{name}: support relaxation UNSAT; transfers={count}")
            continue
        killed = maximum_kill(supports)
        survivors = sorted(set(supports) - set(killed))
        print(
            f"{name}: active={len(supports)}, killed={len(killed)}, "
            f"survivors={survivors}, transfers={count}"
        )
        if len(survivors) <= 3:
            solution = next(iter(affine_solution(supports, killed)))
            parameters = sorted(
                set().union(*(value.free_symbols for value in solution)),
                key=str,
            )
            substitutions = {parameter: index + 2 for index, parameter in enumerate(parameters)}
            point = tuple(sp.simplify(value.subs(substitutions)) for value in solution)
            print(f"  alpha={point}")
            for edge in survivors:
                u, v = edge
                live = {
                    (a, b)
                    for a, b in supports[edge]
                    if sp.simplify(point[3 * u + a] + point[3 * v + b]) != 0
                }
                print(f"  edge {edge}: A-support={sorted(supports[edge])}, B-support={sorted(live)}")


if __name__ == "__main__":
    main()
