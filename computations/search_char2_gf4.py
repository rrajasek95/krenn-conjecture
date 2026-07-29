#!/usr/bin/env python3
"""Exact bit-blasted search for a six-vertex realization over GF(4).

GF(4)=GF(2)[a]/(a^2+a+1); elements are encoded as low/high bits.  This is
a discovery tool for testing whether the characteristic-two obstruction
survives extension of the prime field.
"""

from __future__ import annotations

import argparse
import itertools
import time

from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


N = 6
Q = 3


def perfect_matchings(vertices=tuple(range(N))):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def and_gate(cnf, pool, left, right, tag):
    out = pool.id(("and", tag))
    cnf.extend(([-out, left], [-out, right], [out, -left, -right]))
    return out


def xor_gate(cnf, pool, literals, tag):
    assert literals
    if len(literals) == 1:
        return literals[0]
    value = literals[0]
    for index, literal in enumerate(literals[1:]):
        out = pool.id(("xor", tag, index))
        cnf.extend(
            (
                [value, literal, -out],
                [-value, -literal, -out],
                [value, -literal, out],
                [-value, literal, out],
            )
        )
        value = out
    return value


def multiply(cnf, pool, left, right, tag):
    a0, a1 = left
    b0, b1 = right
    p00 = and_gate(cnf, pool, a0, b0, (tag, "00"))
    p01 = and_gate(cnf, pool, a0, b1, (tag, "01"))
    p10 = and_gate(cnf, pool, a1, b0, (tag, "10"))
    p11 = and_gate(cnf, pool, a1, b1, (tag, "11"))
    return (
        xor_gate(cnf, pool, (p00, p11), (tag, "low")),
        xor_gate(cnf, pool, (p01, p10, p11), (tag, "high")),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--anchors", action="store_true")
    parser.add_argument("--fix-triple-orbit", type=int)
    parser.add_argument("--fix-reference-matching", action="store_true")
    parser.add_argument(
        "--target-kind",
        choices=("ghz", "w-plus-product", "second-osculating"),
        default="ghz",
    )
    args = parser.parse_args()
    pool = IDPool()
    cnf = CNF()
    matchings = tuple(perfect_matchings())

    def entry(u, v, a, b):
        if u > v:
            u, v, a, b = v, u, b, a
        return (pool.id(("entry", u, v, a, b, 0)), pool.id(("entry", u, v, a, b, 1)))

    # Normalize one nonzero target monomial, using target symmetry.
    canonical = ((0, 1), (2, 3), (4, 5))
    canonical_edges = set(canonical)
    if args.target_kind == "ghz":
        canonical_cells = tuple((u, v, 0, 0) for u, v in canonical)
    elif args.target_kind == "w-plus-product":
        canonical_cells = ((0, 1, 1, 0), (2, 3, 0, 0), (4, 5, 0, 0))
    else:
        canonical_cells = ((0, 1, 2, 0), (2, 3, 0, 0), (4, 5, 0, 0))
    for u, v, a, b in canonical_cells:
        lo, hi = entry(u, v, a, b)
        if args.fix_reference_matching:
            cnf.extend(([lo], [-hi]))
        else:
            cnf.append([lo, hi])
    if args.fix_reference_matching:
        for u, v in itertools.combinations(range(N), 2):
            if (u, v) in canonical_edges:
                continue
            lo, hi = entry(u, v, 0, 0)
            cnf.extend(([-lo], [-hi]))

    if args.fix_triple_orbit is not None:
        def act(matching, permutation):
            return tuple(
                sorted(
                    tuple(sorted((permutation[u], permutation[v])))
                    for u, v in matching
                )
            )

        stabilizer = tuple(
            permutation
            for permutation in itertools.permutations(range(N))
            if act(canonical, permutation) == canonical
        )
        remaining = {(first, second) for first in matchings for second in matchings}
        representatives = []
        while remaining:
            representative = min(remaining)
            orbit = {
                (act(representative[0], permutation), act(representative[1], permutation))
                for permutation in stabilizer
            }
            representatives.append(representative)
            remaining.difference_update(orbit)
        if not 0 <= args.fix_triple_orbit < len(representatives):
            parser.error(f"triple orbit must lie in [0,{len(representatives)-1}]")
        first, second = representatives[args.fix_triple_orbit]
        for color, matching in ((1, first), (2, second)):
            for u, v in matching:
                lo, hi = entry(u, v, color, color)
                cnf.append([lo, hi])
        print(
            f"triple_orbit={args.fix_triple_orbit}/{len(representatives)} "
            f"M1={first} M2={second}",
            flush=True,
        )

    if args.anchors:
        for p in range(N):
            for target_color in range(Q):
                selectors = []
                for neighbor in range(N):
                    if neighbor == p:
                        continue
                    selector = pool.id(("anchor", p, target_color, neighbor))
                    selectors.append(selector)
                    head_bits = []
                    for tail_color in range(Q):
                        for head_color in range(Q):
                            bits = entry(p, neighbor, tail_color, head_color)
                            if head_color == target_color:
                                head_bits.extend(bits)
                            else:
                                for bit in bits:
                                    cnf.append([-selector, -bit])
                    cnf.append([-selector] + head_bits)
                cnf.append(selectors)

    for coloring_index, coloring in enumerate(itertools.product(range(Q), repeat=N)):
        terms = []
        for matching_index, matching in enumerate(matchings):
            cells = [entry(u, v, coloring[u], coloring[v]) for u, v in matching]
            pair = multiply(
                cnf, pool, cells[0], cells[1], (coloring_index, matching_index, "pair")
            )
            term = multiply(
                cnf, pool, pair, cells[2], (coloring_index, matching_index, "term")
            )
            terms.append(term)
        if args.target_kind == "ghz":
            target = len(set(coloring)) == 1
        elif args.target_kind == "w-plus-product":
            target = coloring.count(1) == 1 and coloring.count(0) == N - 1
            target |= coloring == (2,) * N
        else:
            target = coloring.count(2) == 1 and coloring.count(0) == N - 1
            target |= coloring.count(1) == 2 and coloring.count(0) == N - 2
        for bit in range(2):
            parity = xor_gate(
                cnf,
                pool,
                tuple(term[bit] for term in terms),
                ("sum", coloring_index, bit),
            )
            cnf.append([parity if target and bit == 0 else -parity])

    print(f"vars={pool.top} clauses={len(cnf.clauses)}", flush=True)
    started = time.time()
    with Solver(name="cadical195", bootstrap_with=cnf) as solver:
        sat = solver.solve()
        print(f"sat={sat} time={time.time()-started:.2f}s", flush=True)
        if not sat:
            return
        model = {literal for literal in solver.get_model() if literal > 0}
        matrices = {}
        for u, v in itertools.combinations(range(N), 2):
            table = tuple(
                tuple(
                    sum((bit in model) << index for index, bit in enumerate(entry(u, v, a, b)))
                    for b in range(Q)
                )
                for a in range(Q)
            )
            if any(any(row) for row in table):
                matrices[u, v] = table
        print("matrices =", matrices)


if __name__ == "__main__":
    main()
