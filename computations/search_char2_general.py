#!/usr/bin/env python3
"""Exact SAT search for a q=3 endpoint-colored realization over F_2.

In characteristic two the matching sum is the Pfaffian of the alternating
matrix on the 3n vertex/color modes, restricted to one mode at each vertex.
This script keeps completely arbitrary asymmetric 3x3 aggregate matrices.
It is a discovery/audit tool; a fixed-n UNSAT result is not a uniform proof.
"""

from __future__ import annotations

import argparse
import itertools
import time

from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


Q = 3


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for j in range(1, len(vertices)):
        v = vertices[j]
        rest = vertices[1:j] + vertices[j + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def add_iff_and(cnf, output, literals):
    for literal in literals:
        cnf.append([-output, literal])
    cnf.append([output] + [-literal for literal in literals])


def add_xor(cnf, pool, literals, target, tag):
    """Encode XOR(literals)=target by a chain of exact XOR gates."""
    assert literals
    parity = literals[0]
    for k, literal in enumerate(literals[1:], start=1):
        new = pool.id(("xor", tag, k))
        # new <-> parity xor literal
        cnf.extend(
            [
                [parity, literal, -new],
                [-parity, -literal, -new],
                [parity, -literal, new],
                [-parity, literal, new],
            ]
        )
        parity = new
    cnf.append([parity if target else -parity])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6, choices=(4, 6, 8))
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument(
        "--phase",
        choices=("none", "sparse", "dense"),
        default="sparse",
        help="initial phase for the 9*n*(n-1)/2 source-entry variables",
    )
    parser.add_argument(
        "--target-rank",
        type=int,
        default=3,
        choices=(1, 2, 3),
        help="number of nonzero monochromatic target coefficients",
    )
    parser.add_argument(
        "--target-kind",
        choices=("ghz", "w", "w-plus-product", "dicke2", "second-osculating"),
        default="ghz",
        help="target tensor family",
    )
    parser.add_argument(
        "--no-canonical",
        action="store_true",
        help="do not force the canonical color-zero perfect matching",
    )
    parser.add_argument(
        "--canonical-color",
        type=int,
        choices=range(Q),
        default=0,
        help="color of the forced canonical supported perfect matching",
    )
    parser.add_argument(
        "--fix-w-matching",
        action="store_true",
        help="force the canonical matching term in the W coloring (1,0,...,0)",
    )
    parser.add_argument(
        "--fix-osculating-matching",
        action="store_true",
        help="force the canonical term in the one-color-2 osculating fiber",
    )
    parser.add_argument(
        "--fix-dicke-matching",
        action="store_true",
        help="force the canonical term in the two-color-1 Dicke fiber",
    )
    parser.add_argument(
        "--fix-w-product-orbit",
        type=int,
        help="also fix a color-two matching orbit under the canonical W-term stabilizer",
    )
    parser.add_argument(
        "--require-uniform-support",
        type=int,
        choices=range(Q),
        help="require a nonzero matching monomial in this uniform fiber",
    )
    parser.add_argument(
        "--balanced-monomial",
        action="store_true",
        help="require nine active cells forming a perfect matching of all 3n ports",
    )
    parser.add_argument(
        "--support-only",
        action="store_true",
        help="enforce required fibers nonempty and forbidden fibers not singleton",
    )
    parser.add_argument(
        "--anchors",
        action="store_true",
        help="add the characteristic-independent coordinate-head anchor lemma",
    )
    parser.add_argument(
        "--fix-triple-orbit",
        type=int,
        help=(
            "fix a stabilizer-orbit representative of supported perfect "
            "matchings in colors 1 and 2"
        ),
    )
    parser.add_argument(
        "--fix-active-orbit",
        type=int,
        help="for n=6, fix one supported color-one matching orbit relative to color zero",
    )
    args = parser.parse_args()
    n = args.n
    vertices = tuple(range(n))
    matchings = tuple(perfect_matchings(vertices))

    pool = IDPool()
    cnf = CNF()

    def entry(u, v, a, b):
        if u < v:
            return pool.id(("entry", u, v, a, b))
        return pool.id(("entry", v, u, b, a))

    # Normalize one supported color-zero perfect matching.  A nonzero full
    # coefficient contains one; vertex relabeling sends it to this matching.
    canonical = tuple((2 * k, 2 * k + 1) for k in range(n // 2))
    if not args.no_canonical:
        for u, v in canonical:
            cnf.append(
                [entry(u, v, args.canonical_color, args.canonical_color)]
            )
    if args.fix_w_matching:
        cnf.append([entry(0, 1, 1, 0)])
        for u, v in canonical[1:]:
            cnf.append([entry(u, v, 0, 0)])
    if args.fix_osculating_matching:
        cnf.append([entry(0, 1, 2, 0)])
        for u, v in canonical[1:]:
            cnf.append([entry(u, v, 0, 0)])
    if args.fix_dicke_matching:
        cnf.append([entry(0, 1, 1, 1)])
        for u, v in canonical[1:]:
            cnf.append([entry(u, v, 0, 0)])
    if args.fix_w_product_orbit is not None:
        if n != 6:
            parser.error("--fix-w-product-orbit is implemented only for n=6")

        def act_w(matching, permutation):
            return tuple(
                sorted(
                    tuple(sorted((permutation[u], permutation[v])))
                    for u, v in matching
                )
            )

        stabilizer = [
            permutation
            for permutation in itertools.permutations(vertices)
            if permutation[0] == 0
            and permutation[1] == 1
            and act_w(canonical, permutation) == canonical
        ]
        remaining = set(matchings)
        representatives = []
        while remaining:
            representative = min(remaining)
            orbit = {act_w(representative, p) for p in stabilizer}
            representatives.append(representative)
            remaining.difference_update(orbit)
        index = args.fix_w_product_orbit
        if not 0 <= index < len(representatives):
            parser.error(f"W/product orbit must lie in [0,{len(representatives)-1}]")
        product_matching = representatives[index]
        for u, v in product_matching:
            cnf.append([entry(u, v, 2, 2)])
        print(
            f"w_product_orbit={index}/{len(representatives)} M2={product_matching}",
            flush=True,
        )

    if args.fix_triple_orbit is not None:
        def act(matching, permutation):
            return tuple(
                sorted(
                    tuple(sorted((permutation[u], permutation[v])))
                    for u, v in matching
                )
            )

        stabilizer = [
            permutation
            for permutation in itertools.permutations(vertices)
            if act(canonical, permutation) == canonical
        ]
        remaining = {(first, second) for first in matchings for second in matchings}
        representatives = []
        while remaining:
            representative = min(remaining)
            orbit = {
                (act(representative[0], p), act(representative[1], p))
                for p in stabilizer
            }
            representatives.append(representative)
            remaining.difference_update(orbit)
        if not 0 <= args.fix_triple_orbit < len(representatives):
            parser.error(f"triple orbit must lie in [0,{len(representatives)-1}]")
        first, second = representatives[args.fix_triple_orbit]
        for u, v in first:
            cnf.append([entry(u, v, 1, 1)])
        for u, v in second:
            cnf.append([entry(u, v, 2, 2)])
        print(
            f"triple_orbit={args.fix_triple_orbit}/{len(representatives)} "
            f"M1={first} M2={second}",
            flush=True,
        )

    if args.fix_active_orbit is not None:
        if n != 6:
            parser.error("--fix-active-orbit is implemented only for n=6")

        def act_one(matching, permutation):
            return tuple(
                sorted(
                    tuple(sorted((permutation[u], permutation[v])))
                    for u, v in matching
                )
            )

        stabilizer = [
            permutation
            for permutation in itertools.permutations(vertices)
            if act_one(canonical, permutation) == canonical
        ]
        remaining = set(matchings)
        representatives = []
        while remaining:
            representative = min(remaining)
            orbit = {act_one(representative, p) for p in stabilizer}
            representatives.append(representative)
            remaining.difference_update(orbit)
        if not 0 <= args.fix_active_orbit < len(representatives):
            parser.error(f"active orbit must lie in [0,{len(representatives)-1}]")
        first = representatives[args.fix_active_orbit]
        for u, v in first:
            cnf.append([entry(u, v, 1, 1)])
        print(
            f"active_orbit={args.fix_active_orbit}/{len(representatives)} M1={first}",
            flush=True,
        )

    if args.anchors:
        # Over the algebraic closure of F_2 the slice-cover lemma applies:
        # for each tail vertex p and target color r, an incident active
        # rank-one matrix has coordinate factor e_r at the opposite head.
        # We omit cofactor activity, so these clauses are a sound relaxation.
        for p in vertices:
            for r in range(Q):
                selectors = []
                for j in vertices:
                    if j == p:
                        continue
                    selector = pool.id(("anchor", p, r, j))
                    selectors.append(selector)
                    head_entries = []
                    for a in range(Q):
                        for b in range(Q):
                            value = entry(p, j, a, b)
                            # entry() takes colors in endpoint order p,j even
                            # when their numeric order is reversed.
                            if b == r:
                                head_entries.append(value)
                            else:
                                cnf.append([-selector, -value])
                    cnf.append([-selector] + head_entries)
                cnf.append(selectors)

    colorings = tuple(itertools.product(range(Q), repeat=n))
    uniform_terms = {}
    for coloring_index, coloring in enumerate(colorings):
        terms = []
        for matching_index, matching in enumerate(matchings):
            term = pool.id(("term", coloring_index, matching_index))
            add_iff_and(
                cnf,
                term,
                [entry(u, v, coloring[u], coloring[v]) for u, v in matching],
            )
            terms.append(term)
        if args.target_kind == "ghz":
            target = len(set(coloring)) == 1 and coloring[0] < args.target_rank
        elif args.target_kind in ("w", "w-plus-product"):
            target = coloring.count(1) == 1 and coloring.count(0) == n - 1
            if args.target_kind == "w-plus-product":
                target |= coloring == (2,) * n
        elif args.target_kind == "second-osculating":
            target = coloring.count(2) == 1 and coloring.count(0) == n - 1
            target |= coloring.count(1) == 2 and coloring.count(0) == n - 2
        else:
            target = coloring.count(1) == 2 and coloring.count(0) == n - 2
        if args.support_only:
            if target:
                cnf.append(terms)
            else:
                for index, term in enumerate(terms):
                    cnf.append([-term] + terms[:index] + terms[index + 1 :])
        else:
            add_xor(
                cnf,
                pool,
                terms,
                target=target,
                tag=coloring_index,
            )
        if len(set(coloring)) == 1:
            uniform_terms[coloring[0]] = terms

    if args.require_uniform_support is not None:
        cnf.append(uniform_terms[args.require_uniform_support])

    if args.balanced_monomial:
        selectors = {}
        for u, v in itertools.combinations(vertices, 2):
            for a, b in itertools.product(range(Q), repeat=2):
                selector = pool.id(("balanced", u, v, a, b))
                selectors[u, a, v, b] = selector
                cnf.append([-selector, entry(u, v, a, b)])
        for u in vertices:
            for a in range(Q):
                incident = []
                for v in vertices:
                    if u == v:
                        continue
                    for b in range(Q):
                        if u < v:
                            incident.append(selectors[u, a, v, b])
                        else:
                            incident.append(selectors[v, b, u, a])
                cnf.append(incident)
                for left, right in itertools.combinations(incident, 2):
                    cnf.append([-left, -right])

    print(
        f"n={n} matrices={n*(n-1)//2} matchings={len(matchings)} "
        f"vars={pool.top} clauses={len(cnf.clauses)}",
        flush=True,
    )
    started = time.time()
    with Solver(name=args.solver, bootstrap_with=cnf) as solver:
        if args.phase != "none":
            entry_phases = [
                entry(u, v, a, b)
                for u, v in itertools.combinations(vertices, 2)
                for a, b in itertools.product(range(Q), repeat=2)
            ]
            if args.phase == "sparse":
                entry_phases = [-literal for literal in entry_phases]
            solver.set_phases(entry_phases)
        sat = solver.solve()
        print(f"sat={sat} time={time.time()-started:.2f}s", flush=True)
        if not sat:
            return
        model = {lit for lit in solver.get_model() if lit > 0}
        matrices = {}
        for u, v in itertools.combinations(vertices, 2):
            cells = tuple(
                tuple(int(entry(u, v, a, b) in model) for b in range(Q))
                for a in range(Q)
            )
            if any(map(any, cells)):
                matrices[u, v] = cells
        print("matrices =", matrices)

        # Independent parity or support audit.
        for coloring in colorings:
            active_terms = 0
            for matching in matchings:
                term = 1
                for u, v in matching:
                    term &= matrices.get((u, v), ((0, 0, 0),) * 3)[coloring[u]][coloring[v]]
                active_terms += term
            if args.target_kind == "ghz":
                target = len(set(coloring)) == 1 and coloring[0] < args.target_rank
            elif args.target_kind in ("w", "w-plus-product"):
                target = coloring.count(1) == 1 and coloring.count(0) == n - 1
                if args.target_kind == "w-plus-product":
                    target |= coloring == (2,) * n
            elif args.target_kind == "second-osculating":
                target = coloring.count(2) == 1 and coloring.count(0) == n - 1
                target |= coloring.count(1) == 2 and coloring.count(0) == n - 2
            else:
                target = coloring.count(1) == 2 and coloring.count(0) == n - 2
            if args.support_only:
                assert active_terms >= 1 if target else active_terms != 1
            else:
                assert active_terms % 2 == target
        print(
            "independent support audit passed"
            if args.support_only
            else "independent exact F2 audit passed"
        )


if __name__ == "__main__":
    main()
