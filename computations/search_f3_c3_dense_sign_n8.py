#!/usr/bin/env python3
"""Optimized exact full-support F3 search in the joint-C3 n=8 slice.

When all 84 orbit entries are nonzero, write an entry as ``(-1)^x`` with one
Boolean sign bit x.  A coefficient with 105 matching terms is

    sum_M (-1)^{p_M} = 105 - 2 * #{M : p_M=1}
                           = #{M : p_M=1}  (mod 3).

Thus each target equation says that the number of negative matching products
is congruent to 0 (mixed) or 1 (pure) modulo 3.  This specialized encoding
uses shared XOR circuits and ternary accumulators, avoiding zero/product
variables from the general F3 search.  It imposes all 2187 orbit equations.

Full support contains the branch-3 matching automatically.  The equivariant
sign gauge normalizes its first three entries to +1, and its order-12 residual
centralizer supplies exact lex leaders.  Any SAT point is checked by the raw
105-matching evaluator on all 6561 colourings.
"""

from __future__ import annotations

import argparse
from collections import Counter

from pysat.formula import IDPool
from pysat.solvers import Solver

import search_f3_c3_equivariant_n8 as core
from search_f3_general import exactly_one, iff_xor


BRANCH = 3


def parity_key(monomial):
    counts = Counter(monomial)
    return tuple(sorted(index for index, count in counts.items() if count % 2))


def add_sign_lex_leaders(pool, clauses, signs):
    identity = tuple(range(core.N))
    for group_index, permutation in enumerate(core.RESIDUAL_RELABELINGS[BRANCH]):
        if permutation == identity:
            continue
        image = []
        for u, v, left, right in core.CELL_KEYS:
            cell = core.normalize_cell(permutation[u], permutation[v], left, right)
            image.append(core.CELL_INDEX[core.cell_orbit_key(*cell)])
        assert len(set(image)) == len(signs)
        prefix = pool.id(("lex-prefix", group_index, 0))
        clauses.append([prefix])
        for position, image_index in enumerate(image):
            left, right = signs[position], signs[image_index]
            # Boolean lex order 0 < 1.
            clauses.append([-prefix, -left, right])
            if position + 1 == len(signs):
                continue
            nxt = pool.id(("lex-prefix", group_index, position + 1))
            clauses.extend((
                [-nxt, prefix],
                [-nxt, -left, right],
                [-nxt, left, -right],
                [-prefix, left, right, nxt],
                [-prefix, -left, -right, nxt],
            ))
            prefix = nxt


def build_formula(use_lex=True):
    pool = IDPool()
    clauses = []
    signs = tuple(pool.id(("entry-sign", index))
                  for index in range(len(core.CELL_KEYS)))

    # Gauge-normalize the first three pure-zero entries of branch 3 to +1.
    for u, v in core.PURE_MATCHING_REPS[BRANCH][:3]:
        clauses.append([-signs[core.CELL_TO_INDEX[(u, v, 0, 0)]]])
    if use_lex:
        add_sign_lex_leaders(pool, clauses, signs)

    parity_cache = {}

    def parity_literal(monomial):
        key = parity_key(monomial)
        cached = parity_cache.get(key)
        if cached is not None:
            return cached
        if not key:
            parity_cache[key] = None
            return None
        parity = signs[key[0]]
        for position, index in enumerate(key[1:], start=1):
            nxt = pool.id(("term-parity", key, position))
            iff_xor(clauses, nxt, parity, signs[index])
            parity = nxt
        parity_cache[key] = parity
        return parity

    equation_term_count = 0
    for equation, (terms, target) in enumerate(
        zip(core.REPRESENTATIVE_TERMS, core.TARGETS)
    ):
        accumulator = tuple(
            pool.id(("acc", equation, 0, residue))
            for residue in range(core.Q)
        )
        clauses.extend((
            [accumulator[0]], [-accumulator[1]], [-accumulator[2]],
        ))
        position = 0
        for monomial, multiplicity in terms:
            parity = parity_literal(monomial)
            if parity is None:
                # A positive term contributes only its constant multiplicity.
                # Across all matching terms these constants total 105=0 mod3;
                # nevertheless handle this locally for generality.
                shift = 0
                # (-1)^0 contributes multiplicity, whereas the accumulator is
                # counting negative terms.  The coefficient identity above
                # already removed the common constant 105, so positive terms
                # contribute zero here.
                assert shift == 0
                continue
            position += 1
            equation_term_count += 1
            nxt = tuple(
                pool.id(("acc", equation, position, residue))
                for residue in range(core.Q)
            )
            exactly_one(clauses, nxt)
            for residue in range(core.Q):
                clauses.append([-accumulator[residue], parity, nxt[residue]])
                clauses.append([
                    -accumulator[residue], -parity,
                    nxt[(residue + multiplicity) % core.Q],
                ])
            accumulator = nxt
        clauses.append([accumulator[target]])
    return pool, clauses, signs, parity_cache, equation_term_count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--no-lex", action="store_true")
    parser.add_argument(
        "--phase",
        help="84 comma-separated entry values (1 for +, 2 for -)",
    )
    args = parser.parse_args()
    pool, clauses, signs, parities, term_count = build_formula(not args.no_lex)
    print(
        f"signs={len(signs)} parity_functions={len(parities)} "
        f"equation_terms={term_count} equations={len(core.COLOURING_REPS)} "
        f"variables={pool.top} clauses={len(clauses)} "
        f"residual_group={len(core.RESIDUAL_RELABELINGS[BRANCH])}",
        flush=True,
    )
    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        if args.phase:
            values = tuple(map(int, args.phase.split(",")))
            if len(values) != len(signs) or any(value not in (1, 2) for value in values):
                raise ValueError("--phase needs 84 comma-separated values in {1,2}")
            try:
                solver.set_phases([
                    variable if value == 2 else -variable
                    for variable, value in zip(signs, values)
                ])
            except NotImplementedError:
                print(f"solver={args.solver} does not support phase hints", flush=True)
        satisfiable = solver.solve()
        print(f"SAT={satisfiable}", flush=True)
        if not satisfiable:
            return
        positive = {literal for literal in solver.get_model() if literal > 0}
        entries = tuple(2 if variable in positive else 1 for variable in signs)
    core.verify_all_colourings(entries)
    print("direct_all_6561_colourings=PASS")
    print("entries=" + ",".join(map(str, entries)))


if __name__ == "__main__":
    main()
