#!/usr/bin/env python3
"""Exact lazy multi-term completion above a sparse three-matching seed.

The seed is one of the K8 triples whose 12 selected diagonal cells support
exactly five underlying perfect matchings: the three desired constant ones
and two mixed singletons.  Optional cells range over all 252 endpoint-colour
cells.  The SAT loop learns only sound conditions:

* every currently supported mixed singleton must acquire another matching;
* every inconsistent collection of exact mixed binomials must acquire a
  third term in at least one guarded fibre.

Fibres of size at least three are unrestricted.  Thus an UNSAT result at a
cell cap is an exact bounded obstruction, while a survivor is a concrete
support on which the remaining binomial subsystem is soluble over C*.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, product

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

import search_n8_signed_binomial_lazy_cegar as signed
import search_n8_toric_binomial_lazy_cegar as toric_search
import search_parallel_binomial_nonzero_constants_cegar as toric
import factorized_laurent_branches as factorized
from search_monomial_no_singleton_sat import colored_triple_orbits


N = 8
Q = 3


# A pairwise-Hamiltonian orbit-8 boundary found by the unrestricted search.
# Its first 24 cells have 22 mixed binomials and twelve odd unit triangles.
# The four final diagonal cells are a minimum cover of those twelve circuits.
# On the resulting 28-cell chart the original binomial subsystem is
# consistent, but four mixed singleton fibres and a one-row pure-zero
# certificate remain.  Fixing this profile gives a directed search for an
# extension that genuinely changes that certificate.
ORBIT8_BALANCED_REPAIR = frozenset({
    (2, 6, 2, 1), (2, 6, 2, 2), (2, 7, 2, 1),
    (3, 6, 1, 2), (3, 7, 1, 1), (3, 7, 1, 2),
    (4, 6, 2, 1), (4, 7, 2, 1), (4, 7, 2, 2),
    (5, 6, 1, 1), (5, 6, 1, 2), (5, 7, 1, 2),
    (0, 4, 1, 1), (0, 5, 2, 2),
    (1, 2, 1, 1), (1, 3, 2, 2),
})


def target_matchings(orbit=1):
    """One orbit from the exact coloured-triple classification at n=8."""

    return colored_triple_orbits(N)[orbit]


def sparse_seed(orbit=1):
    return frozenset(
        (u, v, colour, colour)
        for colour, matching in enumerate(target_matchings(orbit))
        for u, v in matching
    )


class SparseCompletionSearch:
    def __init__(self, cap, solver_name, orbit=1, fixed_cells=(),
                 seed_cells=None, forbidden_cells=()):
        self.pool = toric.Pool()
        self.cells = tuple(
            (u, v, a, b)
            for u, v in combinations(range(N), 2)
            for a, b in product(range(Q), repeat=2)
        )
        self.cell_index = {cell: index for index, cell in enumerate(self.cells)}
        self.support = {cell: self.pool.new() for cell in self.cells}
        self.matchings = tuple(toric.perfect_matchings(tuple(range(N))))
        self.orbit = orbit
        base_seed = (
            sparse_seed(orbit) if seed_cells is None
            else frozenset(seed_cells)
        )
        self.seed = base_seed | frozenset(fixed_cells)
        self.forbidden = frozenset(forbidden_cells)
        assert len(self.cells) == 252
        assert len(self.matchings) == 105
        assert self.seed <= set(self.cells)
        assert self.forbidden <= set(self.cells)
        assert self.seed.isdisjoint(self.forbidden)

        clauses = [[self.support[cell]] for cell in sorted(self.seed)]
        clauses.extend(
            [-self.support[cell]] for cell in sorted(self.forbidden)
        )
        if cap is not None:
            cardinality = CardEnc.atmost(
                lits=[self.support[cell] for cell in self.cells],
                bound=cap,
                top_id=self.pool.top,
                encoding=EncType.kmtotalizer,
            )
            self.pool.top = cardinality.nv
            clauses.extend(cardinality.clauses)
        self.solver = Solver(name=solver_name, bootstrap_with=clauses)
        self.solver.set_phases([
            self.support[cell] if cell in self.seed else -self.support[cell]
            for cell in self.cells
        ])
        self._terms = {}
        self.singleton_gadgets = set()
        self.core_gadgets = set()
        self.term_variables = {}
        self.zero_product_cuts = 0

    def delete(self):
        self.solver.delete()

    def terms(self, colouring):
        answer = self._terms.get(colouring)
        if answer is None:
            answer = tuple(
                tuple((u, v, colouring[u], colouring[v]) for u, v in matching)
                for matching in self.matchings
            )
            self._terms[colouring] = answer
        return answer

    def decode(self, model):
        positive = {literal for literal in model if literal > 0}
        return frozenset(
            cell for cell in self.cells if self.support[cell] in positive
        )

    def add_singleton_gadget(self, colouring, trigger_number):
        key = colouring, trigger_number
        if key in self.singleton_gadgets:
            return False
        trigger = frozenset(self.terms(colouring)[trigger_number])
        selectors = []
        new_variables = []
        for number, decorated in enumerate(self.terms(colouring)):
            if number == trigger_number:
                continue
            selector = self.pool.new()
            new_variables.append(selector)
            selectors.append(selector)
            for cell in frozenset(decorated) - trigger:
                self.solver.add_clause([-selector, self.support[cell]])
        self.solver.add_clause(
            [-self.support[cell] for cell in sorted(trigger)] + selectors
        )
        self.solver.set_phases([-variable for variable in new_variables])
        self.singleton_gadgets.add(key)
        return True

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

        selectors = []
        new_variables = []
        for colouring, pair_numbers, pair_cells in descriptions:
            for number, decorated in enumerate(self.terms(colouring)):
                if number in pair_numbers:
                    continue
                selector = self.pool.new()
                new_variables.append(selector)
                selectors.append(selector)
                for cell in frozenset(decorated) - pair_cells:
                    self.solver.add_clause([-selector, self.support[cell]])
        assert selectors
        self.solver.add_clause(
            [-self.support[cell] for cell in sorted(guard)] + selectors
        )
        self.solver.set_phases([-variable for variable in new_variables])
        self.core_gadgets.add(key)
        return True

    def block_exact_support(self, selected):
        self.solver.add_clause([
            -self.support[cell] if cell in selected else self.support[cell]
            for cell in self.cells
        ])

    def term_indicator(self, colouring, matching_number):
        """Return a Boolean exactly equivalent to one matching term."""

        key = colouring, matching_number
        answer = self.term_variables.get(key)
        if answer is not None:
            return answer
        answer = self.pool.new()
        decorated = self.terms(colouring)[matching_number]
        for cell in decorated:
            self.solver.add_clause([-answer, self.support[cell]])
        self.solver.add_clause(
            [answer] + [-self.support[cell] for cell in decorated]
        )
        self.term_variables[key] = answer
        return answer

    def add_zero_product_nogood(self, fibres, mixed, used_rows, colours):
        """Block an unchanged exact quotient certificate killing constants."""

        clause = set()
        for index in used_rows:
            colouring, terms = mixed[index]
            present = {
                matching_number for matching_number, _decorated in terms
            }
            for matching_number in range(len(self.matchings)):
                indicator = self.term_indicator(colouring, matching_number)
                clause.add(
                    -indicator if matching_number in present else indicator
                )

        for colour in colours:
            colouring = (colour,) * N
            present = {
                matching_number
                for matching_number, _decorated in fibres[colouring]
            }
            for matching_number in range(len(self.matchings)):
                indicator = self.term_indicator(colouring, matching_number)
                clause.add(
                    -indicator if matching_number in present else indicator
                )
        self.solver.add_clause(sorted(clause))
        self.zero_product_cuts += 1
        return len(clause)


def exact_fibres(search, selected):
    return toric.exact_fibres(N, selected, search.matchings)


def binomial_system(search, fibres):
    mixed = []
    rows = []
    for colouring, terms in sorted(fibres.items()):
        if len(set(colouring)) == 1 or len(terms) != 2:
            continue
        mixed.append((colouring, terms))
        rows.append(toric.exponent_row(
            terms[0][1], terms[1][1], search.cell_index, len(search.cells)
        ))
    return mixed, rows


def reduced_polynomial(search, terms, lattice):
    coefficients = {}
    for _number, decorated in terms:
        exponent = toric.exponent_vector(
            decorated, search.cell_index, len(search.cells)
        )
        signed_key = toric.quotient_key(tuple(exponent) + (0,), lattice)
        sign = signed_key[-1]
        key = signed_key[:-1]
        coefficients[key] = coefficients.get(key, 0) + (-1 if sign else 1)
    return {key: value for key, value in coefficients.items() if value}


def quotient_binomial_closure(search, fibres, initial_rows):
    """Adjoin every forced equal-magnitude two-class quotient equation."""

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
                "status": "inconsistent", "rounds": rounds,
                "rows": rows, "rhs": rhs, "lattice": lattice,
                "remainders": {},
            }
        remainders = {
            colouring: reduced_polynomial(search, terms, lattice)
            for colouring, terms in fibres.items()
            if len(set(colouring)) > 1
        }
        remainders = {
            colouring: remainder
            for colouring, remainder in remainders.items() if remainder
        }
        if not remainders:
            return {
                "status": "solved", "rounds": rounds,
                "rows": rows, "rhs": rhs, "lattice": lattice,
                "remainders": {},
            }

        new_equations = []
        for remainder in remainders.values():
            if len(remainder) != 2:
                continue
            items = sorted(remainder.items())
            (left, left_coefficient), (right, right_coefficient) = items
            if abs(left_coefficient) != abs(right_coefficient):
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
                "status": status, "rounds": rounds,
                "rows": rows, "rhs": rhs, "lattice": lattice,
                "remainders": remainders,
            }
        rows.extend(row for row, _bit in new_equations)
        rhs.extend(bit for _row, bit in new_equations)
        rounds += 1


def run(cap, solver_name, max_rounds, core_batch, stop_no_singletons,
        keep_survivors, orbit=1, fixed_cells=(), seed_cells=None,
        forbidden_cells=()):
    search = SparseCompletionSearch(
        cap, solver_name, orbit, fixed_cells, seed_cells, forbidden_cells
    )
    best = None
    try:
        seed_fibres = exact_fibres(search, search.seed)
        seed_histogram = Counter(
            len(terms) for colouring, terms in seed_fibres.items()
            if len(set(colouring)) > 1
        )
        if seed_cells is None:
            underlying = set().union(*map(set, target_matchings(orbit)))
            union_matchings = sum(
                set(matching) <= underlying for matching in search.matchings
            )
        else:
            union_matchings = "custom"
        print(
            f"orbit={orbit} seed_cells={len(search.seed)} "
            f"union_matchings={union_matchings} "
            f"mixed_histogram={dict(seed_histogram)} "
            f"cap={cap} variables={search.pool.top}",
            flush=True,
        )

        survivors = 0
        for round_number in range(max_rounds):
            if not search.solver.solve():
                print(
                    f"UNSAT cap={cap} rounds={round_number} "
                    f"singleton_gadgets={len(search.singleton_gadgets)} "
                    f"core_gadgets={len(search.core_gadgets)}",
                    flush=True,
                )
                return None

            selected = search.decode(search.solver.get_model())
            fibres = exact_fibres(search, selected)
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

            mixed, rows = binomial_system(search, fibres)
            consistent, lattice = toric.signed_quotient_lattice(
                rows, len(search.cells)
            )
            histogram = Counter(
                len(terms) for colouring, terms in fibres.items()
                if len(set(colouring)) > 1
            )
            if stop_no_singletons:
                print(
                    f"NO_SINGLETON cap={cap} round={round_number} "
                    f"cells={len(selected)} histogram={dict(sorted(histogram.items()))} "
                    f"binomials={len(rows)} consistent={consistent}",
                    flush=True,
                )
                print("EXTRA", sorted(selected - search.seed), flush=True)
                return selected

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
                        index for index, coefficient in enumerate(relation or ())
                        if coefficient
                    )
                    if not indices:
                        indices = tuple(range(len(rows)))
                    assert search.add_core_break_gadget(mixed, indices)
                    chosen = [indices]
                print(
                    f"round={round_number} cells={len(selected)} "
                    f"histogram={dict(sorted(histogram.items()))} "
                    f"inconsistent triangles={len(triangles)} "
                    f"add_cores={len(chosen)}",
                    flush=True,
                )
                continue

            multi_remainders = {
                colouring: reduced_polynomial(search, terms, lattice)
                for colouring, terms in fibres.items()
                if len(set(colouring)) > 1 and len(terms) >= 3
            }
            multi_remainders = {
                colouring: remainder
                for colouring, remainder in multi_remainders.items()
                if remainder
            }
            pure_product, _classes = toric.reduced_constant_product(
                N, fibres, lattice, search.cells, search.cell_index
            )
            if not pure_product:
                used_rows, colours = toric.minimize_zero_product_certificate(
                    N, fibres, rows, search.cells, search.cell_index
                )
                cut_size = search.add_zero_product_nogood(
                    fibres, mixed, used_rows, colours
                )
                print(
                    f"round={round_number} cells={len(selected)} "
                    f"zero_product rows={len(used_rows)}/{len(rows)} "
                    f"colours={colours} cut_size={cut_size}",
                    flush=True,
                )
                continue

            # First adjoin every forced equal-magnitude two-class quotient
            # equation.  This closure is necessary for any torus solution
            # and can itself become inconsistent, leave one monomial, solve
            # every mixed fibre, or force a pure coefficient to zero.
            closure = quotient_binomial_closure(search, fibres, rows)
            if closure["status"] in ("inconsistent", "monomial"):
                search.block_exact_support(selected)
                print(
                    f"round={round_number} cells={len(selected)} "
                    f"closure={closure['status']} "
                    f"closure_rounds={closure['rounds']} "
                    f"closure_rows={len(closure['rows'])} "
                    "exact_support_cut",
                    flush=True,
                )
                continue
            closure_pure, _closure_classes = toric.reduced_constant_product(
                N, fibres, closure["lattice"],
                search.cells, search.cell_index,
            )
            if not closure_pure:
                search.block_exact_support(selected)
                print(
                    f"round={round_number} cells={len(selected)} "
                    f"closure_zero_pure "
                    f"closure_rounds={closure['rounds']} "
                    f"closure_rows={len(closure['rows'])} "
                    "exact_support_cut",
                    flush=True,
                )
                continue
            if closure["status"] == "solved":
                print(
                    "EXACT_BINOMIAL_CLOSURE_SURVIVOR "
                    f"cells={len(selected)} "
                    f"closure_rounds={closure['rounds']} "
                    f"closure_rows={len(closure['rows'])}",
                    flush=True,
                )
                print("EXTRA", sorted(selected - search.seed), flush=True)
                return selected, fibres, closure["rows"], closure["lattice"]

            multi_remainders = closure["remainders"]
            # If every remaining polynomial factors into two signed Laurent
            # binomials, exhaust the resulting finite branch problem exactly.
            if multi_remainders:
                branch_result = factorized.solve_factorized_branches(
                    multi_remainders, closure["rows"], fibres, N,
                    search.cells, search.cell_index,
                    solver_name=solver_name,
                    base_rhs=closure["rhs"],
                )
                if branch_result.status == "exhausted":
                    search.block_exact_support(selected)
                    print(
                        f"round={round_number} cells={len(selected)} "
                        f"factorized_exhausted "
                        f"factors={len(branch_result.factors)} "
                        f"clauses={len(branch_result.clauses)} "
                        f"branches={branch_result.branches} "
                        f"inconsistent={branch_result.inconsistent_branches} "
                        f"pure_zero={branch_result.pure_zero_branches}",
                        flush=True,
                    )
                    continue
                if branch_result.status == "survivor":
                    assert all(
                        not reduced_polynomial(search, terms, branch_result.lattice)
                        for colouring, terms in fibres.items()
                        if len(set(colouring)) > 1
                    )
                    print(
                        "EXACT_FACTORIZED_TORIC_SURVIVOR "
                        f"cells={len(selected)} "
                        f"factors={len(branch_result.selected_factors)}",
                        flush=True,
                    )
                    print("EXTRA", sorted(selected - search.seed), flush=True)
                    return selected, fibres, rows, branch_result.lattice
            survivors += 1
            score = (len(multi_remainders), sum(map(len, multi_remainders.values())))
            if best is None or score < best[0]:
                best = score, selected
                print(
                    f"SURVIVOR number={survivors} cap={cap} round={round_number} "
                    f"cells={len(selected)} histogram={dict(sorted(histogram.items()))} "
                    f"binomials={len(rows)} multi_remainders={score} "
                    f"closure_rounds={closure['rounds']} "
                    f"pure_product_classes={len(closure_pure)}",
                    flush=True,
                )
                print("EXTRA", sorted(selected - search.seed), flush=True)
            if survivors >= keep_survivors:
                return best
            search.block_exact_support(selected)

        print(
            f"BOUNDARY cap={cap} rounds={max_rounds} "
            f"singleton_gadgets={len(search.singleton_gadgets)} "
            f"core_gadgets={len(search.core_gadgets)} "
            f"zero_product_cuts={search.zero_product_cuts} "
            f"best={best and best[0]}",
            flush=True,
        )
        return best
    finally:
        search.delete()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cap", type=int, default=32)
    parser.add_argument("--orbit", type=int, choices=range(13), default=1)
    parser.add_argument("--solver", default="cadical300")
    parser.add_argument("--max-rounds", type=int, default=5000)
    parser.add_argument("--core-batch", type=int, default=128)
    parser.add_argument("--stop-no-singletons", action="store_true")
    parser.add_argument("--keep-survivors", type=int, default=20)
    parser.add_argument(
        "--profile", choices=("none", "orbit8-balanced-repair"),
        default="none",
    )
    args = parser.parse_args()
    fixed_cells = ()
    if args.profile == "orbit8-balanced-repair":
        if args.orbit != 8:
            parser.error("orbit8-balanced-repair requires --orbit 8")
        fixed_cells = ORBIT8_BALANCED_REPAIR
    run(
        args.cap, args.solver, args.max_rounds, args.core_batch,
        args.stop_no_singletons, args.keep_survivors, args.orbit, fixed_cells,
    )


if __name__ == "__main__":
    main()
