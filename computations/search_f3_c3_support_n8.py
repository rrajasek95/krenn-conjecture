#!/usr/bin/env python3
"""Exact support-only necessary-condition search for the joint-C3 F3 slice.

For every mixed colouring, a realization cannot have exactly one supported
perfect-matching term: that lone nonzero monomial could not sum to zero over
any field.  A pure coefficient equal to one must have at least one supported
term.  UNSAT of all seven exhaustive pure-matching branches therefore rules
out the full F3-valued C3-equivariant system (indeed, the same supports over
any field).  SAT is only a support survivor, not a realization.
"""

from __future__ import annotations

import argparse
from collections import Counter

from pysat.formula import IDPool
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType

import search_f3_c3_equivariant_n8 as core
from search_f3_general import iff_and


def cell_image(permutation):
    answer = []
    for u, v, left, right in core.CELL_KEYS:
        cell = core.normalize_cell(permutation[u], permutation[v], left, right)
        answer.append(core.CELL_INDEX[core.cell_orbit_key(*cell)])
    assert len(set(answer)) == len(core.CELL_KEYS)
    return tuple(answer)


def matching_stabilizer(branch):
    matching = core.PURE_MATCHING_REPS[branch]
    return tuple(
        permutation for permutation in core.CENTRALIZER
        if core.canonical_matching(
            (permutation[u], permutation[v]) for u, v in matching
        ) == matching
    )


SUPPORT_STABILIZERS = tuple(matching_stabilizer(branch) for branch in range(7))
assert tuple(map(len, SUPPORT_STABILIZERS)) == (4, 1, 2, 12, 2, 12, 2)


def add_gated_boolean_lex(pool, clauses, support, branch):
    group = SUPPORT_STABILIZERS[branch]
    if len(group) == 1:
        return None
    selector = pool.id(("branch-selector", branch))
    identity = tuple(range(core.N))
    for group_index, permutation in enumerate(group):
        if permutation == identity:
            continue
        image = cell_image(permutation)
        prefix = pool.id(("prefix", branch, group_index, 0))
        clauses.append([-selector, prefix])
        for position, image_index in enumerate(image):
            left, right = support[position], support[image_index]
            clauses.append([-selector, -prefix, -left, right])
            if position + 1 == len(support):
                continue
            nxt = pool.id(("prefix", branch, group_index, position + 1))
            clauses.extend((
                [-selector, -nxt, prefix],
                [-selector, -nxt, -left, right],
                [-selector, -nxt, left, -right],
                [-selector, -prefix, left, right, nxt],
                [-selector, -prefix, -left, -right, nxt],
            ))
            prefix = nxt
    return selector


def build_formula(max_cells=None):
    pool = IDPool()
    clauses = []
    support = tuple(pool.id(("cell-support", index))
                    for index in range(len(core.CELL_KEYS)))
    term_variables = {}

    def term_variable(monomial):
        variable = term_variables.get(monomial)
        if variable is not None:
            return variable
        variable = pool.id(("term-support", monomial))
        iff_and(clauses, variable, tuple(support[index] for index in monomial))
        term_variables[monomial] = variable
        return variable

    for colouring, target in zip(core.COLOURING_REPS, core.TARGETS):
        counts = Counter(
            core.monomial_key(colouring, matching)
            for matching in core.MATCHINGS
        )
        terms = {monomial: term_variable(monomial) for monomial in counts}
        if target == 1:
            clauses.append(list(terms.values()))
            continue
        # If a multiplicity-one term is supported, at least one other
        # matching occurrence must be supported.  Terms of multiplicity >=2
        # can serve as that partner and themselves never create total count 1.
        for monomial, multiplicity in counts.items():
            if multiplicity != 1:
                continue
            clauses.append(
                [-terms[monomial]]
                + [variable for other, variable in terms.items()
                   if other != monomial]
            )

    selectors = tuple(
        add_gated_boolean_lex(pool, clauses, support, branch)
        for branch in range(7)
    )
    if max_cells is not None:
        encoding = CardEnc.atmost(
            lits=list(support), bound=max_cells, top_id=pool.top,
            encoding=EncType.kmtotalizer,
        )
        clauses.extend(encoding.clauses)
        if encoding.nv > pool.top:
            pool.occupy(pool.top + 1, encoding.nv)
    return pool, clauses, support, term_variables, selectors


def branch_assumptions(support, selectors, branch):
    assumptions = [
        support[core.CELL_TO_INDEX[(u, v, 0, 0)]]
        for u, v in core.PURE_MATCHING_REPS[branch]
    ]
    if selectors[branch] is not None:
        assumptions.append(selectors[branch])
    return assumptions


def verify_support(selected):
    histograms = Counter()
    for colouring, target in zip(core.COLOURING_REPS, core.TARGETS):
        count = sum(
            all(core.CELL_TO_INDEX[(u, v, colouring[u], colouring[v])] in selected
                for u, v in matching)
            for matching in core.MATCHINGS
        )
        if target:
            assert count >= 1
        else:
            assert count != 1
        histograms[count] += 1
    return histograms


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--branch", type=int, choices=range(7))
    parser.add_argument("--phase", choices=("sparse", "dense", "none"),
                        default="sparse")
    parser.add_argument("--max-cells", type=int)
    args = parser.parse_args()
    branches = range(7) if args.branch is None else (args.branch,)
    pool, clauses, support, terms, selectors = build_formula(args.max_cells)
    print(
        f"support_variables={len(support)} term_variables={len(terms)} "
        f"variables={pool.top} clauses={len(clauses)} max_cells={args.max_cells} "
        f"stabilizers={[len(group) for group in SUPPORT_STABILIZERS]}",
        flush=True,
    )
    statuses = {}
    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        if args.phase == "sparse":
            solver.set_phases([-variable for variable in support])
        elif args.phase == "dense":
            solver.set_phases(list(support))
        for branch in branches:
            assumptions = branch_assumptions(support, selectors, branch)
            satisfiable = solver.solve(assumptions=assumptions)
            statuses[branch] = satisfiable
            print(f"branch={branch} SAT={satisfiable}", flush=True)
            if satisfiable:
                positive = {literal for literal in solver.get_model() if literal > 0}
                selected = {index for index, variable in enumerate(support)
                            if variable in positive}
                histogram = verify_support(selected)
                print(
                    f"branch={branch} direct_support_verification=PASS "
                    f"cells={len(selected)} histogram={dict(sorted(histogram.items()))}",
                    flush=True,
                )
                print(
                    f"branch={branch} selected_indices={sorted(selected)} "
                    f"selected_keys={[core.CELL_KEYS[index] for index in sorted(selected)]}",
                    flush=True,
                )
    print(f"statuses={statuses}", flush=True)


if __name__ == "__main__":
    main()
