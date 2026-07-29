#!/usr/bin/env python3
"""Exact arbitrary-matrix Krenn search over F_3.

Every aggregate entry is represented by a one-hot value in {0,1,2}.  A
matching monomial is zero unless all of its entries are nonzero; otherwise
its value is determined by the parity of the entries equal to 2.  A
three-state sequential accumulator imposes each coefficient sum modulo 3.

This is a discovery tool.  A SAT point is verified directly and can then be
tested for 3-adic lifting; UNSAT at a fixed order is not a uniform complex
proof.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver


Q = 3


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


def pfaffian_sign(matching):
    crossings = sum(
        a < c < b < d or c < a < d < b
        for index, (a, b) in enumerate(matching)
        for c, d in matching[index + 1 :]
    )
    return -1 if crossings % 2 else 1


def exactly_one(clauses, literals):
    clauses.append(list(literals))
    for left, right in combinations(literals, 2):
        clauses.append([-left, -right])


def iff_and(clauses, output, literals):
    for literal in literals:
        clauses.append([-output, literal])
    clauses.append([output] + [-literal for literal in literals])


def iff_xor(clauses, output, left, right):
    clauses.extend((
        [left, right, -output],
        [-left, -right, -output],
        [left, -right, output],
        [-left, right, output],
    ))


def build_formula(n, symmetry_break=False, k4_extension=False, k4_core=False,
                  k4_support=False, max_nonzero=None, pfaffian=False):
    vertices = tuple(range(n))
    edges = tuple(combinations(vertices, 2))
    matchings = tuple(perfect_matchings(vertices))
    colorings = tuple(product(range(Q), repeat=n))
    pool = IDPool()
    clauses = []

    values = {}
    for u, v in edges:
        for a, b in product(range(Q), repeat=2):
            row = tuple(pool.id(("entry", u, v, a, b, value)) for value in range(3))
            values[u, v, a, b] = row
            exactly_one(clauses, row)

    # A nonzero all-zero coefficient has a supported matching.  Vertex
    # relabeling sends one such matching to the canonical one.
    canonical = tuple((2 * index, 2 * index + 1) for index in range(n // 2))
    for u, v in canonical:
        zero, one, two = values[u, v, 0, 0]
        clauses.append([one, two])

    if symmetry_break:
        # Once a nonzero pure-0 matching has been relabeled to ``canonical``,
        # the local diagonal target stabilizer may normalize all but one of
        # its entries.  Indeed, scaling color 0 at vertex v by lambda_v
        # preserves Delta exactly when product_v lambda_v = 1.  On the
        # disjoint canonical pairs this lets us set the first m-1 products
        # lambda_u lambda_v A_uv(0,0) to 1; the last pair absorbs the product
        # constraint.  Over F_3 every stipulated entry is already nonzero.
        for u, v in canonical[:-1]:
            _zero, one, _two = values[u, v, 0, 0]
            clauses.append([one])

    if k4_extension or k4_core or k4_support:
        assert n == 6
        edge_colour = {
            (0, 1): 0, (2, 3): 0,
            (0, 2): 1, (1, 3): 1,
            (0, 3): 2, (1, 2): 2,
        }
        for edge, colour in edge_colour.items():
            for a, b in product(range(Q), repeat=2):
                row = values[edge + (a, b)]
                if a == b == colour and k4_support:
                    clauses.append([row[1], row[2]])
                else:
                    selected = 1 if a == b == colour else 0
                    clauses.append([row[selected]])
        if k4_extension:
            for a, b in product(range(Q), repeat=2):
                clauses.append([values[4, 5, a, b][0]])

    for coloring_number, coloring in enumerate(colorings):
        accumulator = (pool.id(("acc", coloring_number, 0, 0)),
                       pool.id(("acc", coloring_number, 0, 1)),
                       pool.id(("acc", coloring_number, 0, 2)))
        clauses.append([accumulator[0]])
        clauses.append([-accumulator[1]])
        clauses.append([-accumulator[2]])

        for matching_number, matching in enumerate(matchings, start=1):
            nonzero_literals = []
            negative_literals = []
            for u, v in matching:
                zero, one, two = values[u, v, coloring[u], coloring[v]]
                nonzero_literals.append(-zero)
                negative_literals.append(two)

            nonzero = pool.id(("nz", coloring_number, matching_number))
            iff_and(clauses, nonzero, nonzero_literals)

            parity = negative_literals[0]
            for position, literal in enumerate(negative_literals[1:], start=1):
                nxt = pool.id(("par", coloring_number, matching_number, position))
                iff_xor(clauses, nxt, parity, literal)
                parity = nxt

            plus = pool.id(("plus", coloring_number, matching_number))
            minus = pool.id(("minus", coloring_number, matching_number))
            iff_and(clauses, plus, (nonzero, -parity))
            iff_and(clauses, minus, (nonzero, parity))
            if pfaffian and pfaffian_sign(matching) < 0:
                plus, minus = minus, plus

            nxt_acc = tuple(
                pool.id(("acc", coloring_number, matching_number, residue))
                for residue in range(3)
            )
            exactly_one(clauses, nxt_acc)
            for residue in range(3):
                # A zero term leaves the residue unchanged.  The plus and
                # minus cases add 1 and 2 respectively.
                clauses.append([-accumulator[residue], nonzero, nxt_acc[residue]])
                clauses.append([-accumulator[residue], -plus,
                                nxt_acc[(residue + 1) % 3]])
                clauses.append([-accumulator[residue], -minus,
                                nxt_acc[(residue + 2) % 3]])
            accumulator = nxt_acc

        target = 1 if len(set(coloring)) == 1 else 0
        clauses.append([accumulator[target]])

    if max_nonzero is not None:
        encoding = CardEnc.atmost(
            lits=[-row[0] for row in values.values()],
            bound=max_nonzero,
            top_id=pool.top,
            encoding=EncType.kmtotalizer,
        )
        clauses.extend(encoding.clauses)
        if encoding.nv > pool.top:
            pool.occupy(pool.top + 1, encoding.nv)

    return pool, clauses, values, edges, matchings, colorings


def verify(n, assignment, values, edges, matchings, colorings, pfaffian=False):
    positive = {literal for literal in assignment if literal > 0}
    entries = {}
    for key, row in values.items():
        selected = [value for value, variable in enumerate(row) if variable in positive]
        assert len(selected) == 1
        entries[key] = selected[0]

    for coloring in colorings:
        total = 0
        for matching in matchings:
            term = 1
            for u, v in matching:
                term = (term * entries[u, v, coloring[u], coloring[v]]) % 3
            if pfaffian and pfaffian_sign(matching) < 0:
                term = (-term) % 3
            total = (total + term) % 3
        expected = 1 if len(set(coloring)) == 1 else 0
        assert total == expected, (coloring, total, expected)
    return entries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, choices=(4, 6, 8), default=6)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--symmetry-break", action="store_true")
    parser.add_argument("--k4-extension", action="store_true")
    parser.add_argument("--k4-core", action="store_true")
    parser.add_argument("--k4-support", action="store_true")
    parser.add_argument("--max-nonzero", type=int)
    parser.add_argument("--pfaffian", action="store_true")
    args = parser.parse_args()

    pool, clauses, values, edges, matchings, colorings = build_formula(
        args.n, args.symmetry_break, args.k4_extension, args.k4_core,
        args.k4_support, args.max_nonzero, args.pfaffian
    )
    print(f"n={args.n} entries={len(values)} matchings={len(matchings)} "
          f"variables={pool.top} clauses={len(clauses)}", flush=True)
    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        satisfiable = solver.solve()
        print(f"SAT={satisfiable}", flush=True)
        if not satisfiable:
            return
        entries = verify(
            args.n, solver.get_model(), values, edges, matchings, colorings,
            args.pfaffian,
        )
    print("direct F3 verification: PASS", flush=True)
    for key in sorted(entries):
        if entries[key]:
            print(key, entries[key])


if __name__ == "__main__":
    main()
