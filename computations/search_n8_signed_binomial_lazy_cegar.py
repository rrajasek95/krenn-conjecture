#!/usr/bin/env python3
"""Lazy exact SAT search for signed-binomial parallel cells at n=8.

The base formula has only the 252 cell-support bits and 252 cell-sign bits.
For a selected target-matching orbit it forces one prescribed positive
constant matching in each colour and forbids every other constant matching.

Mixed-colouring constraints are added only when a SAT model violates them.
A singleton term gets a one-way selector gadget requiring an actual distinct
mate; an overfull fibre gets direct clauses forbidding its currently supported
matching triples.  An optional ``--learning exact`` mode instead installs a
complete {0,2}-cardinality gadget for a bad fibre.  If a fibre has two terms
of the same sign, a guarded XOR clause forces those two products to have
opposite signs whenever both remain supported.  Every learned clause is a
direct logical consequence of the requested signed-binomial condition;
UNSAT is therefore an exact exhaustive result for the chosen target orbit.

Any SAT model is checked independently by direct enumeration of all 3^8
colourings and 105 perfect matchings before it is printed.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, permutations, product
import json
from math import prod
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

import search_parallel_binomial_nonzero_constants_cegar as core
from search_parallel_binomial_signed_sat import parity_gate


N = 8
Q = 3


def decorated_term(coloring, matching):
    return tuple(
        (u, v, coloring[u], coloring[v]) for u, v in matching
    )


def target_automorphisms(targets):
    """Vertex/color permutations preserving the ordered colored target set."""

    target_sets = tuple(frozenset(matching) for matching in targets)
    answer = []
    for vertex_permutation in permutations(range(N)):
        images = tuple(
            frozenset(
                tuple(sorted((vertex_permutation[u], vertex_permutation[v])))
                for u, v in matching
            )
            for matching in targets
        )
        for color_permutation in permutations(range(Q)):
            if all(
                images[color] == target_sets[color_permutation[color]]
                for color in range(Q)
            ):
                answer.append((vertex_permutation, color_permutation))
    return tuple(answer)


def image_cell(cell, vertex_permutation, color_permutation):
    u, v, a, b = cell
    image_u = vertex_permutation[u]
    image_v = vertex_permutation[v]
    image_a = color_permutation[a]
    image_b = color_permutation[b]
    if image_u < image_v:
        return image_u, image_v, image_a, image_b
    return image_v, image_u, image_b, image_a


def add_lex_leader(clauses, pool, variables, image_variables):
    """Encode ``variables <=lex image_variables`` with false before true."""

    prefix = None  # The empty prefix is equal.
    for left, right in zip(variables, image_variables):
        if left == right:
            continue
        # An equal prefix may not be followed by (left,right)=(1,0).
        clause = [-left, right]
        if prefix is not None:
            clause.insert(0, -prefix)
        clauses.append(clause)

        new_prefix = pool.new()
        if prefix is not None:
            clauses.append([-new_prefix, prefix])
        clauses.extend((
            [-new_prefix, -left, right],
            [-new_prefix, left, -right],
        ))
        if prefix is None:
            clauses.extend((
                [-left, -right, new_prefix],
                [left, right, new_prefix],
            ))
        else:
            clauses.extend((
                [-prefix, -left, -right, new_prefix],
                [-prefix, left, right, new_prefix],
            ))
        prefix = new_prefix


class LazySearch:
    def __init__(self, orbit, solver_name="cadical195", max_cells=None,
                 proof_prefix=None, symmetry_lex=False,
                 unique_constants=True):
        self.orbit = orbit
        self.targets = core.target_orbits(N)[orbit]
        self.matchings = tuple(core.perfect_matchings(tuple(range(N))))
        assert len(self.matchings) == 105

        self.pool = core.Pool()
        self.cells = tuple(
            (u, v, a, b)
            for u, v in combinations(range(N), 2)
            for a, b in product(range(Q), repeat=2)
        )
        assert len(self.cells) == 252
        self.cell_index = {
            cell: index for index, cell in enumerate(self.cells)
        }
        self.support = {cell: self.pool.new() for cell in self.cells}
        self.sign = {cell: self.pool.new() for cell in self.cells}
        self.clauses = []
        self.unique_constants = unique_constants
        self.forced_support = frozenset(
            (u, v, color, color)
            for color, target in enumerate(self.targets)
            for u, v in target
        )

        # The prescribed constant matching is the unique term in its fibre.
        # Setting each of its four cell signs positive gauges its product to +1.
        for color, target in enumerate(self.targets):
            target_set = set(target)
            for u, v in target:
                cell = (u, v, color, color)
                self.clauses.append([self.support[cell]])
                self.clauses.append([-self.sign[cell]])
            coloring = (color,) * N
            if unique_constants:
                for matching in self.matchings:
                    if set(matching) == target_set:
                        continue
                    decorated = decorated_term(coloring, matching)
                    self.clauses.append(
                        [-self.support[cell] for cell in decorated]
                    )

        self.base_variables = self.pool.top
        assert self.base_variables == 504
        self.automorphisms = target_automorphisms(self.targets)
        if orbit == 39:
            assert len(self.automorphisms) == 8
        self.symmetry_lex = symmetry_lex
        if symmetry_lex:
            identity = (
                tuple(range(N)),
                tuple(range(Q)),
            )
            variables = (
                [self.support[cell] for cell in self.cells]
                + [self.sign[cell] for cell in self.cells]
            )
            for vertex_permutation, color_permutation in self.automorphisms:
                if (vertex_permutation, color_permutation) == identity:
                    continue
                image_variables = (
                    [
                        self.support[image_cell(
                            cell, vertex_permutation, color_permutation
                        )]
                        for cell in self.cells
                    ]
                    + [
                        self.sign[image_cell(
                            cell, vertex_permutation, color_permutation
                        )]
                        for cell in self.cells
                    ]
                )
                add_lex_leader(
                    self.clauses, self.pool, variables, image_variables
                )
        self.max_cells = max_cells
        if max_cells is not None:
            encoding = CardEnc.atmost(
                lits=[self.support[cell] for cell in self.cells],
                bound=max_cells,
                top_id=self.pool.top,
                encoding=EncType.kmtotalizer,
            )
            self.pool.top = encoding.nv
            self.clauses.extend(encoding.clauses)
        self.all_clauses = [tuple(clause) for clause in self.clauses]
        self.proof_prefix = proof_prefix
        self.fibre_terms = {}
        self.fibre_gadgets = set()
        self.mate_gadgets = set()
        self.overfull_cuts = set()
        self.structural_hits = Counter()
        self.parity_variables = {}
        self.pair_constraints = set()
        self.parity_core_cuts = set()
        self.solver = Solver(
            name=solver_name,
            bootstrap_with=self.clauses,
            with_proof=proof_prefix is not None,
        )
        # Sparse supports are the useful first models in this CEGAR loop.
        self.solver.set_phases(
            [-self.support[cell] for cell in self.cells]
            + [-self.sign[cell] for cell in self.cells]
        )

    def delete(self):
        self.solver.delete()

    def terms(self, coloring):
        answer = self.fibre_terms.get(coloring)
        if answer is None:
            answer = tuple(
                decorated_term(coloring, matching)
                for matching in self.matchings
            )
            self.fibre_terms[coloring] = answer
        return answer

    def add_clauses(self, clauses):
        for clause in clauses:
            self.solver.add_clause(clause)
            self.all_clauses.append(tuple(clause))

    def dump_unsat_certificate(self):
        """Write the final CNF and a deletion-free DRUP trace."""

        if self.proof_prefix is None:
            return None
        prefix = Path(self.proof_prefix)
        cnf_path = prefix.with_suffix(".cnf")
        proof_path = prefix.with_suffix(".drup")
        proof = self.solver.get_proof() or []
        # Deletions are optional in DRUP.  Dropping them is useful for a tiny
        # checker and remains sound because unit propagation is monotone when
        # clauses are retained.
        additions = [line for line in proof if not line.startswith("d ")]
        with cnf_path.open("w", encoding="ascii") as stream:
            stream.write(
                f"p cnf {self.pool.top} {len(self.all_clauses)}\n"
            )
            for clause in self.all_clauses:
                stream.write(" ".join(map(str, clause)) + " 0\n")
        with proof_path.open("w", encoding="ascii") as stream:
            for line in additions:
                stream.write(line.rstrip() + "\n")
        return cnf_path, proof_path, len(additions)

    def add_fibre_gadget(self, coloring):
        """Enforce exactly 0 or 2 supported terms in one mixed fibre."""

        assert len(set(coloring)) > 1
        if coloring in self.fibre_gadgets:
            return 0, 0
        old_top = self.pool.top
        clauses = []
        term_variables = []
        for decorated in self.terms(coloring):
            term = self.pool.new()
            term_variables.append(term)
            # term iff every one of its four decorated cells is supported.
            clauses.extend([-term, self.support[cell]] for cell in decorated)
            clauses.append(
                [-self.support[cell] for cell in decorated] + [term]
            )

        encoding = CardEnc.atmost(
            lits=term_variables,
            bound=2,
            top_id=self.pool.top,
            encoding=EncType.seqcounter,
        )
        self.pool.top = encoding.nv
        clauses.extend(encoding.clauses)

        # At most two is already imposed.  These implications exclude one:
        # each present term must have some distinct present mate.
        for index, term in enumerate(term_variables):
            clauses.append(
                [-term]
                + term_variables[:index]
                + term_variables[index + 1:]
            )

        self.add_clauses(clauses)
        self.solver.set_phases(
            [-variable for variable in range(old_top + 1, self.pool.top + 1)]
        )
        self.fibre_gadgets.add(coloring)
        return self.pool.top - old_top, len(clauses)

    def add_mate_gadget(self, coloring, trigger_number):
        """If one selected term remains, require an actual distinct mate.

        The selector variables need only imply the cells outside the trigger
        term.  Under the guarded long clause the trigger itself is present,
        so common cells are already true.  Reverse implications are neither
        needed nor imposed.
        """

        key = coloring, trigger_number
        if key in self.mate_gadgets:
            return 0, 0
        old_top = self.pool.top
        clauses = []
        terms = self.terms(coloring)
        trigger = set(terms[trigger_number])
        selectors = []
        for number, decorated in enumerate(terms):
            if number == trigger_number:
                continue
            selector = self.pool.new()
            selectors.append(selector)
            for cell in set(decorated) - trigger:
                clauses.append([-selector, self.support[cell]])
        clauses.append(
            [
                -self.support[cell]
                for cell in sorted(trigger - self.forced_support)
            ]
            + selectors
        )
        self.add_clauses(clauses)
        # Without an explicit phase, CDCL solvers often set many one-way
        # selectors true and thereby create a needlessly dense cell support.
        # False phases make the long clause choose one mate unless propagation
        # genuinely needs more; this changes search order, not the formula.
        self.solver.set_phases([-selector for selector in selectors])
        self.mate_gadgets.add(key)
        return self.pool.top - old_top, len(clauses)

    def add_overfull_cuts(self, coloring, terms, limit=512):
        """Forbid triples among the terms supported in the current model."""

        old_top = self.pool.top
        clauses = []
        numbers = tuple(number for number, _decorated in terms)
        for triple in combinations(numbers, 3):
            key = coloring, triple
            if key in self.overfull_cuts:
                continue
            union = set()
            for number in triple:
                union.update(self.terms(coloring)[number])
            clauses.append([
                -self.support[cell]
                for cell in sorted(union - self.forced_support)
            ])
            self.overfull_cuts.add(key)
            if len(clauses) >= limit:
                break
        assert clauses
        self.add_clauses(clauses)
        return self.pool.top - old_top, len(clauses)

    def add_opposite_pair(self, coloring, first, second):
        """Guard the exact odd-parity equation for one matching pair."""

        if first > second:
            first, second = second, first
        key = coloring, first, second
        if key in self.pair_constraints:
            return 0, 0

        left = self.terms(coloring)[first]
        right = self.terms(coloring)[second]
        left_set = set(left)
        right_set = set(right)
        difference = tuple(sorted(left_set ^ right_set))
        assert difference

        parity_key = tuple(self.sign[cell] for cell in difference)
        old_top = self.pool.top
        clauses = []
        parity = self.parity_variables.get(parity_key)
        if parity is None:
            parity = parity_gate(clauses, self.pool, list(parity_key))
            self.parity_variables[parity_key] = parity

        # If both terms occur, every support bit in their union is true and
        # their common sign factors cancel.  Odd parity on the symmetric
        # difference is exactly opposite product sign.
        guard = [
            -self.support[cell]
            for cell in sorted(
                (left_set | right_set) - self.forced_support
            )
        ]
        clauses.append(guard + [parity])
        self.add_clauses(clauses)
        self.pair_constraints.add(key)
        return self.pool.top - old_top, len(clauses)

    def parity_core(self, fibres):
        """Return an inconsistent subset of current binomial sign rows.

        Every mixed two-term fibre requires odd parity on the symmetric
        difference of its cell signs.  The twelve gauged target signs are
        unconditional zero rows.  Dependencies are tracked only for mixed
        equations; fixed rows may participate but need not enter the learned
        support guard.
        """

        equations = []
        for coloring, terms in sorted(fibres.items()):
            if len(set(coloring)) == 1 or len(terms) != 2:
                continue
            left = set(terms[0][1])
            right = set(terms[1][1])
            mask = 0
            for cell in left ^ right:
                mask ^= 1 << self.cell_index[cell]
            equations.append((coloring, terms, mask))

        basis = {}

        def insert(mask, rhs, dependency):
            while mask:
                pivot = mask.bit_length() - 1
                previous = basis.get(pivot)
                if previous is None:
                    basis[pivot] = (mask, rhs, dependency)
                    return None
                mask ^= previous[0]
                rhs ^= previous[1]
                dependency ^= previous[2]
            return dependency if rhs else None

        for color, target in enumerate(self.targets):
            for u, v in target:
                index = self.cell_index[u, v, color, color]
                contradiction = insert(1 << index, 0, 0)
                assert contradiction is None

        for index, (_coloring, _terms, mask) in enumerate(equations):
            contradiction = insert(mask, 1, 1 << index)
            if contradiction is not None:
                chosen = tuple(
                    row for row in range(len(equations))
                    if contradiction >> row & 1
                )
                assert chosen
                return equations, chosen
        return equations, None

    def add_parity_core_cut(self, fibres):
        """Block simultaneous support of an inconsistent parity core."""

        equations, core = self.parity_core(fibres)
        if core is None:
            return 0, 0, 0
        guarded_cells = set()
        for index in core:
            _coloring, terms, _mask = equations[index]
            guarded_cells.update(terms[0][1])
            guarded_cells.update(terms[1][1])
        keys = {frozenset(guarded_cells)}
        if self.symmetry_lex:
            for vertex_permutation, color_permutation in self.automorphisms:
                keys.add(frozenset(
                    image_cell(
                        cell, vertex_permutation, color_permutation
                    )
                    for cell in guarded_cells
                ))
        new_keys = keys - self.parity_core_cuts
        assert new_keys
        clauses = [
            [
                -self.support[cell]
                for cell in sorted(key - self.forced_support)
            ]
            for key in sorted(new_keys, key=lambda item: tuple(sorted(item)))
        ]
        self.add_clauses(clauses)
        self.parity_core_cuts.update(new_keys)
        return 0, len(clauses), len(core)

    def decode(self, model):
        positive = {literal for literal in model if literal > 0}
        selected = frozenset(
            cell for cell in self.cells if self.support[cell] in positive
        )
        weights = {
            cell: (-1 if self.sign[cell] in positive else 1)
            for cell in selected
        }
        return selected, weights

    def inspect(self, selected, weights):
        fibres = core.exact_fibres(N, selected, self.matchings)
        structural = []
        bad_sign = []
        for coloring, terms in fibres.items():
            if len(set(coloring)) == 1:
                continue
            if len(terms) != 2:
                structural.append((coloring, terms))
                continue
            values = []
            for _number, decorated in terms:
                value = 1
                for cell in decorated:
                    value *= weights[cell]
                values.append(value)
            if values[0] == values[1]:
                bad_sign.append((coloring, terms))
        return fibres, structural, bad_sign


def verify_solution(search, selected, weights):
    """Solver-independent direct audit of every constant and mixed fibre."""

    fibres = core.exact_fibres(N, selected, search.matchings)
    for color, target in enumerate(search.targets):
        terms = fibres.get((color,) * N, ())
        assert len(terms) == 1
        assert set(terms[0][1]) == {
            (u, v, color, color) for u, v in target
        }
        value = 1
        for cell in terms[0][1]:
            value *= weights[cell]
        assert value == 1
    for coloring, terms in fibres.items():
        if len(set(coloring)) == 1:
            continue
        assert len(terms) == 2
        values = []
        for _number, decorated in terms:
            value = 1
            for cell in decorated:
                value *= weights[cell]
            values.append(value)
        assert sum(values) == 0
    return fibres


def dump_near_model(path, search, round_number, selected, weights, fibres,
                    structural, bad_sign, score):
    """Write a complete, solver-independent snapshot of the best near model."""

    def encode_terms(terms):
        return [
            {
                "matching_number": matching_number,
                "cells": [list(cell) for cell in decorated],
                "product_sign": prod(weights[cell] for cell in decorated),
            }
            for matching_number, decorated in terms
        ]

    payload = {
        "n": N,
        "orbit": search.orbit,
        "targets": [
            [list(edge) for edge in matching] for matching in search.targets
        ],
        "max_cells": search.max_cells,
        "round": round_number,
        "score": list(score),
        "selected_cells": [
            {"cell": list(cell), "weight": weights[cell]}
            for cell in sorted(selected)
        ],
        "fibre_size_histogram": dict(sorted(
            Counter(len(terms) for terms in fibres.values()).items()
        )),
        "bad_structural_fibres": [
            {
                "coloring": list(coloring),
                "terms": encode_terms(terms),
            }
            for coloring, terms in structural
        ],
        "bad_sign_fibres": [
            {
                "coloring": list(coloring),
                "terms": encode_terms(terms),
            }
            for coloring, terms in bad_sign
        ],
    }
    destination = Path(path)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(payload, stream, indent=2, sort_keys=True)
        stream.write("\n")
    temporary.replace(destination)


def run(orbit, max_rounds, structural_batch, sign_batch, solver_name,
        learning, max_cells, proof_prefix, best_prefix, symmetry_lex):
    search = LazySearch(
        orbit,
        solver_name,
        max_cells,
        proof_prefix=proof_prefix,
        symmetry_lex=symmetry_lex,
    )
    print(
        f"orbit={orbit} targets={search.targets} matchings=105 cells=252",
        flush=True,
    )
    print(
        f"base variables={search.base_variables} "
        f"initial_variables={search.pool.top} clauses={len(search.clauses)} "
        f"max_cells={max_cells} automorphisms={len(search.automorphisms)} "
        f"symmetry_lex={symmetry_lex}",
        flush=True,
    )
    learned_clauses = 0
    best_score = None
    try:
        for round_number in range(max_rounds):
            if not search.solver.solve():
                certificate = search.dump_unsat_certificate()
                print(
                    f"UNSAT orbit={orbit} max_cells={max_cells} "
                    f"rounds={round_number} "
                    f"variables={search.pool.top} "
                    f"learned_clauses={learned_clauses} "
                    f"fibre_gadgets={len(search.fibre_gadgets)} "
                    f"mate_gadgets={len(search.mate_gadgets)} "
                    f"overfull_cuts={len(search.overfull_cuts)} "
                    f"parity_core_cuts={len(search.parity_core_cuts)} "
                    f"pair_constraints={len(search.pair_constraints)}",
                    flush=True,
                )
                if certificate is not None:
                    print(
                        f"certificate cnf={certificate[0]} "
                        f"proof={certificate[1]} "
                        f"proof_additions={certificate[2]}",
                        flush=True,
                    )
                return None

            selected, weights = search.decode(search.solver.get_model())
            fibres, structural, bad_sign = search.inspect(selected, weights)
            score = (
                len(structural) + len(bad_sign),
                len(structural),
                len(bad_sign),
                len(selected),
            )
            if best_prefix is not None and (
                best_score is None or score < best_score
            ):
                dump_near_model(
                    best_prefix,
                    search,
                    round_number,
                    selected,
                    weights,
                    fibres,
                    structural,
                    bad_sign,
                    score,
                )
                best_score = score
                print(
                    f"best_near_model={best_prefix} score={score}",
                    flush=True,
                )
            if not structural and not bad_sign:
                verified = verify_solution(search, selected, weights)
                print(
                    f"SAT EXACT orbit={orbit} round={round_number} "
                    f"cells={len(selected)} fibres={len(verified)}",
                    flush=True,
                )
                for cell in sorted(selected):
                    print(f"  {cell} {weights[cell]:+d}", flush=True)
                return selected, weights, verified

            new_variables = 0
            new_clauses = 0
            _variables, parity_clauses, parity_core_size = \
                search.add_parity_core_cut(fibres)
            new_clauses += parity_clauses
            # Larger bad fibres first; singleton fibres follow.  A fibre is
            # given a full exact gadget at most once.
            candidates = sorted(
                structural,
                key=lambda item: (-len(item[1]), item[0]),
            )
            added_structural = 0
            for coloring, terms in candidates:
                search.structural_hits[coloring] += 1
                promote = (
                    learning == "exact"
                    or (
                        learning == "hybrid"
                        and search.structural_hits[coloring] >= 2
                    )
                    or (learning == "hybrid" and len(terms) >= 3)
                )
                if promote:
                    if coloring in search.fibre_gadgets:
                        continue
                    variables, clauses = search.add_fibre_gadget(coloring)
                elif len(terms) == 1:
                    trigger = terms[0][0]
                    if (coloring, trigger) in search.mate_gadgets:
                        continue
                    variables, clauses = search.add_mate_gadget(
                        coloring, trigger
                    )
                else:
                    variables, clauses = search.add_overfull_cuts(
                        coloring, terms
                    )
                new_variables += variables
                new_clauses += clauses
                added_structural += 1
                if added_structural >= structural_batch:
                    break

            added_sign = 0
            for coloring, terms in bad_sign:
                first, second = terms[0][0], terms[1][0]
                if (coloring, min(first, second), max(first, second)) in \
                        search.pair_constraints:
                    continue
                variables, clauses = search.add_opposite_pair(
                    coloring, first, second
                )
                new_variables += variables
                new_clauses += clauses
                added_sign += 1
                if added_sign >= sign_batch:
                    break

            assert new_clauses
            learned_clauses += new_clauses
            if round_number < 20 or round_number % 10 == 0:
                histogram = Counter(len(terms) for terms in fibres.values())
                print(
                    f"round={round_number} cells={len(selected)} "
                    f"fibres={len(fibres)} sizes={dict(sorted(histogram.items()))} "
                    f"bad_structure={len(structural)} bad_sign={len(bad_sign)} "
                    f"add_structure={added_structural} add_pairs={added_sign} "
                    f"parity_core={parity_core_size} "
                    f"new_vars={new_variables} new_clauses={new_clauses}",
                    flush=True,
                )
        print(
            f"BOUNDARY orbit={orbit} reached max_rounds={max_rounds} "
            f"variables={search.pool.top} learned_clauses={learned_clauses} "
            f"fibre_gadgets={len(search.fibre_gadgets)} "
            f"mate_gadgets={len(search.mate_gadgets)} "
            f"overfull_cuts={len(search.overfull_cuts)} "
            f"parity_core_cuts={len(search.parity_core_cuts)} "
            f"pair_constraints={len(search.pair_constraints)}",
            flush=True,
        )
        return "boundary"
    finally:
        search.delete()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, default=39)
    parser.add_argument("--max-rounds", type=int, default=10000)
    parser.add_argument("--structural-batch", type=int, default=32)
    parser.add_argument("--sign-batch", type=int, default=256)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--max-cells", type=int)
    parser.add_argument("--proof-prefix")
    parser.add_argument("--best-prefix")
    parser.add_argument("--symmetry-lex", action="store_true")
    parser.add_argument(
        "--learning", choices=("mate", "hybrid", "exact"), default="hybrid"
    )
    args = parser.parse_args()
    run(
        args.orbit,
        args.max_rounds,
        args.structural_batch,
        args.sign_batch,
        args.solver,
        args.learning,
        args.max_cells,
        args.proof_prefix,
        args.best_prefix,
        args.symmetry_lex,
    )


if __name__ == "__main__":
    main()
