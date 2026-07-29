#!/usr/bin/env python3
"""Support-first lazy search for the orbit-39 signed-binomial n=8 chart.

This uses the sound structural gadgets from
``search_n8_signed_binomial_lazy_cegar`` but eliminates sign variables by
Gaussian elimination whenever a complete {0,2}-fibre support is reached.
An inconsistent partial parity core is already a support obstruction and is
learned immediately.  A returned point is independently checked by the
original direct enumerator.
"""

from __future__ import annotations

import argparse
from collections import Counter

import search_n8_signed_binomial_lazy_cegar as signed


def solve_signs(search, fibres):
    """Solve target-zero and mixed-pair odd-parity equations over F_2."""

    rows = []
    for color, target in enumerate(search.targets):
        for u, v in target:
            rows.append((1 << search.cell_index[u, v, color, color], 0))
    for colouring, terms in sorted(fibres.items()):
        if len(set(colouring)) == 1:
            continue
        assert len(terms) == 2
        mask = 0
        for cell in set(terms[0][1]) ^ set(terms[1][1]):
            mask ^= 1 << search.cell_index[cell]
        rows.append((mask, 1))

    basis = {}
    for mask, rhs in rows:
        while mask:
            pivot = mask.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (mask, rhs)
                break
            mask ^= basis[pivot][0]
            rhs ^= basis[pivot][1]
        else:
            if rhs:
                return None

    # Free variables are zero.  Solve pivots in increasing order, since each
    # stored row has no bit above its pivot but may have lower bits.
    value_mask = 0
    for pivot in sorted(basis):
        mask, rhs = basis[pivot]
        lower = mask & ~(1 << pivot)
        parity = (lower & value_mask).bit_count() & 1
        if rhs ^ parity:
            value_mask |= 1 << pivot
    return {
        cell: (-1 if value_mask >> index & 1 else 1)
        for cell, index in search.cell_index.items()
    }


def run(orbit, max_cells, solver_name, max_rounds, batch, symmetry_lex):
    search = signed.LazySearch(
        orbit, solver_name, max_cells, symmetry_lex=symmetry_lex
    )
    learned = 0
    best = None
    try:
        for round_number in range(max_rounds):
            if not search.solver.solve():
                print(
                    f"UNSAT max_cells={max_cells} rounds={round_number} "
                    f"variables={search.pool.top} learned={learned}",
                    flush=True,
                )
                return None
            selected, _irrelevant = search.decode(search.solver.get_model())
            fibres = signed.core.exact_fibres(
                signed.N, selected, search.matchings
            )
            structural = [
                (colouring, terms)
                for colouring, terms in fibres.items()
                if len(set(colouring)) > 1 and len(terms) != 2
            ]

            _v, clauses, core_size = search.add_parity_core_cut(fibres)
            learned += clauses
            if not structural and not clauses:
                weights = solve_signs(search, fibres)
                assert weights is not None
                weights = {cell: weights[cell] for cell in selected}
                signed.verify_solution(search, selected, weights)
                print(
                    f"SAT EXACT cells={len(selected)} fibres={len(fibres)} "
                    f"round={round_number}",
                    flush=True,
                )
                for cell in sorted(selected):
                    print(f"  {cell} {weights[cell]:+d}")
                return selected, weights

            score = (len(structural), len(selected))
            if best is None or score < best:
                best = score
                print(
                    f"best round={round_number} cells={len(selected)} "
                    f"fibres={len(fibres)} structural={len(structural)} "
                    f"parity_core={core_size}",
                    flush=True,
                )

            added = 0
            for colouring, _terms in sorted(
                structural, key=lambda item: (-len(item[1]), item[0])
            ):
                if colouring in search.fibre_gadgets:
                    continue
                _variables, new_clauses = search.add_fibre_gadget(colouring)
                learned += new_clauses
                added += 1
                if added >= batch:
                    break
            assert clauses or added
            if round_number < 20 or round_number % 10 == 0:
                histogram = Counter(len(terms) for terms in fibres.values())
                print(
                    f"round={round_number} cells={len(selected)} "
                    f"sizes={dict(sorted(histogram.items()))} "
                    f"structural={len(structural)} add={added} "
                    f"parity_core={core_size}",
                    flush=True,
                )
        print(f"BOUNDARY rounds={max_rounds} best={best}", flush=True)
        return "boundary"
    finally:
        search.delete()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, default=39)
    parser.add_argument("--max-cells", type=int, default=23)
    parser.add_argument("--solver", default="cadical300")
    parser.add_argument("--max-rounds", type=int, default=5000)
    parser.add_argument("--batch", type=int, default=256)
    parser.add_argument("--symmetry-lex", action="store_true")
    args = parser.parse_args()
    run(
        args.orbit, args.max_cells, args.solver, args.max_rounds, args.batch,
        args.symmetry_lex,
    )


if __name__ == "__main__":
    main()
