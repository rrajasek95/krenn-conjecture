#!/usr/bin/env python3
"""Search a sharply factored F_3 extension of the K4 ternary source.

On vertices 0,1,2,3 use the standard one-factorization, with a unit
same-colour cell on each edge.  Vertices 4 and 5 are never paired together.
Write X_u=A_{u4} and Y_u=A_{u5}.  For an old pair u<v the two ways of
matching u,v to 4,5 give

  B_uv(a,b,c,d) = X_u(a,c)Y_v(b,d) + Y_u(a,d)X_v(b,c).

We ask for B_23=e_0^4, B_13=e_1^4, B_12=e_2^4 and all other B_uv=0.
The complementary old edges 01,02,03 then produce exactly Delta_6, while
the complementary edges 23,13,12 contribute zero.  Thus a SAT point is an
exact characteristic-three Krenn source (a discovery object for lifting).
"""

from __future__ import annotations

import argparse
from itertools import combinations, product

from pysat.formula import IDPool
from pysat.solvers import Solver


def exactly_one(clauses, row):
    clauses.append(list(row))
    for left, right in combinations(row, 2):
        clauses.append([-left, -right])


def build():
    pool = IDPool()
    clauses = []
    variables = {}
    for family in ("X", "Y"):
        for u, a, b in product(range(4), repeat=3):
            row = tuple(pool.id((family, u, a, b, value)) for value in range(3))
            variables[family, u, a, b] = row
            exactly_one(clauses, row)

    desired = {(2, 3): 0, (1, 3): 1, (1, 2): 2}
    equations = 0
    for u, v in combinations(range(4), 2):
        for a, b, c, d in product(range(3), repeat=4):
            target = int(
                desired.get((u, v)) == a == b == c == d
            )
            rows = (
                variables["X", u, a, c],
                variables["Y", v, b, d],
                variables["Y", u, a, d],
                variables["X", v, b, c],
            )
            for values in product(range(3), repeat=4):
                if (values[0] * values[1] + values[2] * values[3]) % 3 == target:
                    continue
                clauses.append([-row[value] for row, value in zip(rows, values)])
            equations += 1
    return pool, clauses, variables, equations


def decode(model, variables):
    positive = {literal for literal in model if literal > 0}
    answer = {}
    for key, row in variables.items():
        selected = [value for value, literal in enumerate(row) if literal in positive]
        assert len(selected) == 1
        answer[key] = selected[0]
    return answer


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for index in range(1, len(vertices)):
        v = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def direct_verify(entries):
    edge_colour = {
        (0, 1): 0, (2, 3): 0,
        (0, 2): 1, (1, 3): 1,
        (0, 3): 2, (1, 2): 2,
    }
    matchings = tuple(perfect_matchings(range(6)))

    def edge_value(u, v, a, b):
        if v < 4:
            return int(a == b == edge_colour[u, v])
        if v == 4 and u < 4:
            return entries["X", u, a, b]
        if v == 5 and u < 4:
            return entries["Y", u, a, b]
        return 0

    for colouring in product(range(3), repeat=6):
        total = 0
        for matching in matchings:
            term = 1
            for u, v in matching:
                term = term * edge_value(u, v, colouring[u], colouring[v]) % 3
            total = (total + term) % 3
        expected = int(len(set(colouring)) == 1)
        assert total == expected, (colouring, total, expected)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", default="cadical195")
    args = parser.parse_args()
    pool, clauses, variables, equations = build()
    print(f"variables={pool.top} clauses={len(clauses)} equations={equations}", flush=True)
    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        satisfiable = solver.solve()
        print(f"SAT={satisfiable}", flush=True)
        if not satisfiable:
            return
        entries = decode(solver.get_model(), variables)
    direct_verify(entries)
    print("direct F3 verification: PASS")
    for key, value in sorted(entries.items()):
        if value:
            print(key, value)


if __name__ == "__main__":
    main()
