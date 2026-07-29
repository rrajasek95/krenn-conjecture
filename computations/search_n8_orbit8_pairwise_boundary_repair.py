#!/usr/bin/env python3
"""Exact multi-term repair search above the 24-cell orbit-8 boundary.

The fixed boundary is ``sparse_seed(orbit=8)`` plus the twelve cells supplied
in ``BOUNDARY_EXTRA``.  It has 22 mixed binomials, no mixed singleton, and 12
unit odd Laurent triangles.  This script forces a genuine third term in every
inconsistent binomial core while allowing arbitrary larger fibres.

Consistent supports are reduced exactly in the signed Laurent quotient.  A
zero pure product gets the existing exact structural nogood.  A mixed
remainder consisting of one nonzero group-algebra monomial is also an exact
torus obstruction; its nogood retains every binomial and multi-term fibre
used by that certificate and requires at least one of them to change.
"""

from __future__ import annotations

import argparse
from collections import Counter

import search_n8_sparse_triple_completion as sparse
import search_n8_toric_binomial_lazy_cegar as toric_search
import search_parallel_binomial_nonzero_constants_cegar as toric


BOUNDARY_EXTRA = frozenset({
    (2, 6, 2, 1), (2, 6, 2, 2), (2, 7, 2, 1),
    (3, 6, 1, 2), (3, 7, 1, 1), (3, 7, 1, 2),
    (4, 6, 2, 1), (4, 7, 2, 1), (4, 7, 2, 2),
    (5, 6, 1, 1), (5, 6, 1, 2), (5, 7, 1, 2),
})


FIRST_CONSISTENT_EXTRA = frozenset({
    (0, 3, 0, 1), (0, 6, 0, 1), (0, 6, 0, 2),
    (0, 7, 0, 1), (0, 7, 0, 2), (1, 4, 0, 2),
    (1, 6, 0, 1), (1, 6, 0, 2), (1, 7, 0, 1),
    (1, 7, 0, 2),
})


class Orbit8RepairSearch(sparse.SparseCompletionSearch):
    def __init__(self, cap, solver_name):
        super().__init__(cap, solver_name, orbit=8)
        self.boundary = self.seed | BOUNDARY_EXTRA
        for cell in BOUNDARY_EXTRA:
            self.solver.add_clause([self.support[cell]])
        preferred = self.boundary | (
            FIRST_CONSISTENT_EXTRA if cap is None or cap >= 34 else frozenset()
        )
        self.solver.set_phases([
            self.support[cell] if cell in preferred else -self.support[cell]
            for cell in self.cells
        ])
        self.extra_term_gadgets = {}
        self.remainder_cuts = 0

    def extra_term_variable(self, colouring, pair_numbers, pair_cells):
        key = colouring, tuple(sorted(pair_numbers))
        previous = self.extra_term_gadgets.get(key)
        if previous is not None:
            return previous
        extra = self.pool.new()
        selectors = []
        new_variables = [extra]
        for number, decorated in enumerate(self.terms(colouring)):
            if number in pair_numbers:
                continue
            selector = self.pool.new()
            new_variables.append(selector)
            selectors.append(selector)
            for cell in frozenset(decorated) - pair_cells:
                self.solver.add_clause([-selector, self.support[cell]])
        self.solver.add_clause([-extra] + selectors)
        self.solver.set_phases([-variable for variable in new_variables])
        self.extra_term_gadgets[key] = extra
        return extra

    def add_core_break_gadget(self, mixed, row_indices):
        descriptions = []
        guard = set()
        for index in row_indices:
            colouring, present = mixed[index]
            assert len(present) == 2
            numbers = tuple(number for number, _decorated in present)
            pair_cells = frozenset(present[0][1]) | frozenset(present[1][1])
            guard.update(pair_cells)
            descriptions.append((colouring, numbers, pair_cells))
        key = tuple(sorted(
            (colouring, numbers)
            for colouring, numbers, _pair_cells in descriptions
        ))
        if key in self.core_gadgets:
            return False
        extras = [
            self.extra_term_variable(colouring, numbers, pair_cells)
            for colouring, numbers, pair_cells in descriptions
        ]
        self.solver.add_clause(
            [-self.support[cell] for cell in sorted(guard)] + extras
        )
        self.core_gadgets.add(key)
        return True

    def add_remainder_nogood(self, fibres, mixed, colouring):
        """Require a certified one-monomial quotient obstruction to change."""

        clause = set()
        relevant = list(mixed) + [(colouring, fibres[colouring])]
        for fibre_colouring, present_terms in relevant:
            present = {
                matching_number
                for matching_number, _decorated in present_terms
            }
            for matching_number in range(len(self.matchings)):
                indicator = self.term_indicator(
                    fibre_colouring, matching_number
                )
                clause.add(
                    -indicator if matching_number in present else indicator
                )
        self.solver.add_clause(sorted(clause))
        self.remainder_cuts += 1
        return len(clause)


def audit_boundary(search):
    fibres = sparse.exact_fibres(search, search.boundary)
    histogram = Counter(
        len(terms)
        for colouring, terms in fibres.items()
        if len(set(colouring)) > 1
    )
    assert len(search.boundary) == 24
    assert histogram == {2: 22}
    mixed, rows = sparse.binomial_system(search, fibres)
    assert not toric.signed_quotient_lattice(
        rows, len(search.cells)
    )[0]
    triangles = toric_search.unit_triangle_circuits(rows)
    assert len(triangles) == 12
    return fibres, mixed, rows, triangles


def quotient_binomial_closure(search, fibres, initial_rows):
    """Iterate every forced two-class quotient equation to a fixed point.

    If a reduced mixed polynomial is ``a X^u + b X^v`` with
    ``abs(a) == abs(b)``, its vanishing is the Laurent equation
    ``X^(u-v) = -b/a``.  The right side is ``-1`` exactly when the two
    coefficients have the same sign.  All such equations are necessary and
    may therefore be adjoined simultaneously.  Every HNF consistency and
    polynomial reduction below is exact over the complex torus.
    """

    rows = [tuple(row) for row in initial_rows]
    rhs = [1] * len(rows)
    seen = {(row, bit) for row, bit in zip(rows, rhs)}
    rounds = 0
    while True:
        consistent, lattice = toric.signed_quotient_lattice(
            rows, len(search.cells), rhs
        )
        if not consistent:
            return {
                "status": "inconsistent",
                "rounds": rounds,
                "rows": rows,
                "rhs": rhs,
                "lattice": lattice,
                "remainders": {},
            }

        remainders = {
            colouring: sparse.reduced_polynomial(search, terms, lattice)
            for colouring, terms in fibres.items()
            if len(set(colouring)) > 1
        }
        remainders = {
            colouring: remainder
            for colouring, remainder in remainders.items()
            if remainder
        }
        if not remainders:
            return {
                "status": "solved",
                "rounds": rounds,
                "rows": rows,
                "rhs": rhs,
                "lattice": lattice,
                "remainders": {},
            }

        new_equations = []
        hard = {}
        for colouring, remainder in remainders.items():
            if len(remainder) != 2:
                hard[colouring] = remainder
                continue
            items = sorted(remainder.items())
            (left, left_coefficient), (right, right_coefficient) = items
            if abs(left_coefficient) != abs(right_coefficient):
                hard[colouring] = remainder
                continue
            row = tuple(a - b for a, b in zip(left, right))
            bit = int((left_coefficient > 0) == (right_coefficient > 0))
            equation = row, bit
            if equation not in seen:
                seen.add(equation)
                new_equations.append(equation)

        if not new_equations:
            status = "monomial" if any(
                len(remainder) == 1 for remainder in remainders.values()
            ) else "residual"
            return {
                "status": status,
                "rounds": rounds,
                "rows": rows,
                "rhs": rhs,
                "lattice": lattice,
                "remainders": remainders,
                "hard": hard,
            }
        rows.extend(row for row, _bit in new_equations)
        rhs.extend(bit for _row, bit in new_equations)
        rounds += 1


def run(cap, solver_name, max_rounds, core_batch, keep_survivors):
    search = Orbit8RepairSearch(cap, solver_name)
    best = None
    survivors = 0
    try:
        _fibres, base_mixed, _rows, base_triangles = audit_boundary(search)
        for triangle in base_triangles:
            assert search.add_core_break_gadget(base_mixed, triangle)
        print(
            f"PRELOAD cap={cap} boundary_cells=24 triangles=12 "
            f"variables={search.pool.top}",
            flush=True,
        )

        for round_number in range(max_rounds):
            if not search.solver.solve():
                print(
                    f"UNSAT cap={cap} rounds={round_number} "
                    f"singletons={len(search.singleton_gadgets)} "
                    f"cores={len(search.core_gadgets)} "
                    f"zero_product_cuts={search.zero_product_cuts} "
                    f"remainder_cuts={search.remainder_cuts}",
                    flush=True,
                )
                return None

            selected = search.decode(search.solver.get_model())
            fibres = sparse.exact_fibres(search, selected)
            singletons = [
                (colouring, terms[0][0])
                for colouring, terms in sorted(fibres.items())
                if len(set(colouring)) > 1 and len(terms) == 1
            ]
            if singletons:
                added = sum(
                    search.add_singleton_gadget(colouring, trigger)
                    for colouring, trigger in singletons
                )
                assert added
                if round_number < 20 or round_number % 20 == 0:
                    print(
                        f"round={round_number} cells={len(selected)} "
                        f"singletons={len(singletons)} add={added}",
                        flush=True,
                    )
                continue

            mixed, rows = sparse.binomial_system(search, fibres)
            consistent, lattice = toric.signed_quotient_lattice(
                rows, len(search.cells)
            )
            histogram = Counter(
                len(terms)
                for colouring, terms in fibres.items()
                if len(set(colouring)) > 1
            )
            if not consistent:
                triangles = toric_search.unit_triangle_circuits(rows)
                chosen = []
                for indices in triangles:
                    if len(chosen) >= core_batch:
                        break
                    if search.add_core_break_gadget(mixed, indices):
                        chosen.append(indices)
                if not chosen:
                    relation = toric.flint_odd_relation(rows)
                    indices = tuple(
                        index for index, value in enumerate(relation or ())
                        if value
                    ) or tuple(range(len(rows)))
                    assert search.add_core_break_gadget(mixed, indices)
                    chosen = [indices]
                print(
                    f"round={round_number} cells={len(selected)} "
                    f"inconsistent triangles={len(triangles)} "
                    f"add_cores={len(chosen)}",
                    flush=True,
                )
                continue

            pure_product, _classes = toric.reduced_constant_product(
                sparse.N, fibres, lattice, search.cells, search.cell_index
            )
            if not pure_product:
                used_rows, colours = toric.minimize_zero_product_certificate(
                    sparse.N, fibres, rows, search.cells, search.cell_index
                )
                cut_size = search.add_zero_product_nogood(
                    fibres, mixed, used_rows, colours
                )
                print(
                    f"round={round_number} cells={len(selected)} "
                    f"zero_pure rows={len(used_rows)} colours={colours} "
                    f"cut_size={cut_size}",
                    flush=True,
                )
                print(
                    "ZERO_PURE_EXTRA",
                    sorted(selected - search.boundary),
                    flush=True,
                )
                continue

            closure = quotient_binomial_closure(search, fibres, rows)
            if closure["status"] in ("inconsistent", "monomial"):
                search.block_exact_support(selected)
                print(
                    f"round={round_number} cells={len(selected)} "
                    f"closure={closure['status']} "
                    f"closure_rounds={closure['rounds']} "
                    f"closure_rows={len(closure['rows'])} "
                    f"exact_support_cut=1",
                    flush=True,
                )
                continue

            closure_pure, _closure_classes = toric.reduced_constant_product(
                sparse.N, fibres, closure["lattice"],
                search.cells, search.cell_index
            )
            if not closure_pure:
                search.block_exact_support(selected)
                print(
                    f"round={round_number} cells={len(selected)} "
                    f"closure_zero_pure closure_rounds={closure['rounds']} "
                    f"closure_rows={len(closure['rows'])} "
                    f"exact_support_cut=1",
                    flush=True,
                )
                continue

            remainders = closure["remainders"]

            survivors += 1
            score = len(remainders), sum(map(len, remainders.values()))
            if best is None or score < best[0]:
                best = score, selected
                print(
                    f"SURVIVOR number={survivors} cap={cap} "
                    f"round={round_number} cells={len(selected)} "
                    f"histogram={dict(sorted(histogram.items()))} "
                    f"binomials={len(rows)} closure_rows={len(closure['rows'])} "
                    f"closure_rounds={closure['rounds']} "
                    f"remainder_score={score} "
                    f"pure_classes={len(closure_pure)}",
                    flush=True,
                )
                print(
                    "EXTRA", sorted(selected - search.boundary), flush=True
                )
            if not remainders:
                print("EXACT_TORIC_SURVIVOR", flush=True)
                return selected, fibres, rows, lattice
            if survivors >= keep_survivors:
                return best
            search.block_exact_support(selected)

        print(f"BOUNDARY rounds={max_rounds} best={best and best[0]}")
        return best
    finally:
        search.delete()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cap", type=int, default=34)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--max-rounds", type=int, default=5000)
    parser.add_argument("--core-batch", type=int, default=64)
    parser.add_argument("--keep-survivors", type=int, default=20)
    parser.add_argument("--audit-boundary", action="store_true")
    args = parser.parse_args()
    if args.audit_boundary:
        search = Orbit8RepairSearch(None, args.solver)
        try:
            _fibres, _mixed, _rows, triangles = audit_boundary(search)
            print(
                f"PASS boundary cells={len(search.boundary)} "
                f"mixed_binomials=22 odd_triangles={len(triangles)}"
            )
        finally:
            search.delete()
        return
    run(
        args.cap, args.solver, args.max_rounds,
        args.core_batch, args.keep_survivors,
    )


if __name__ == "__main__":
    main()
