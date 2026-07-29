#!/usr/bin/env python3
"""Full support-only SAT search for the n=8 signed-binomial chart.

Unlike the lazy CEGAR search, this program installs the structural condition
for all 3**8 - 3 = 6558 mixed colour fibres before its first SAT call.  Each
of the 105 matching terms in a fibre is equivalent to the conjunction of its
four decorated-cell support bits, and every mixed fibre has cardinality zero
or two.

Two exact cardinality encodings are available.  ``native`` (the default)
uses two native at-most constraints and two activation bits per fibre; it is
substantially smaller and works with MiniCard, Gluecard, and CaDiCaL's
BooleanEngine.  ``state`` is a portable pure-CNF exact unary-state counter.
Clauses are streamed directly into the solver so millions of Python clause
objects are never retained.

Signs are eliminated from the base formula.  Three post-solve modes keep the
scope explicit: ``--structural-only`` returns the first exact 0/2 support;
``--toric`` applies the integer Laurent-lattice consistency test appropriate
to arbitrary nonzero complex weights; and the default signed mode solves the
opposite-product equations over F_2.  A reported point is always audited by
direct enumeration of all colourings and matchings.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product
import json
from pathlib import Path
import resource
import sys
from time import monotonic

from flint import fmpz_mat
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

import search_n8_binomial_support_only as support_only
import search_n8_signed_binomial_lazy_cegar as signed
import search_n8_toric_binomial_lazy_cegar as toric_n8
import verify_n8_toric_orbit40_boundary as orbit40_boundary


N = signed.N
Q = signed.Q


ORBIT40_PHASE_CONSISTENT_SEED = frozenset({
    (0, 1, 0, 0), (0, 2, 1, 1), (0, 3, 0, 0), (0, 4, 2, 2),
    (0, 5, 0, 0), (0, 7, 0, 0), (1, 2, 0, 0), (1, 3, 1, 1),
    (1, 3, 1, 2), (1, 3, 2, 1), (1, 3, 2, 2), (1, 4, 0, 0),
    (1, 5, 1, 1), (1, 5, 1, 2), (1, 5, 2, 1), (1, 5, 2, 2),
    (1, 6, 0, 0), (2, 3, 0, 0), (2, 5, 0, 0), (2, 6, 2, 2),
    (2, 7, 0, 0), (3, 4, 0, 0), (3, 6, 0, 0), (3, 7, 1, 1),
    (3, 7, 1, 2), (3, 7, 2, 1), (3, 7, 2, 2), (4, 5, 0, 0),
    (4, 6, 1, 1), (4, 7, 0, 0), (5, 6, 0, 0), (5, 7, 1, 1),
    (5, 7, 1, 2), (5, 7, 2, 1), (5, 7, 2, 2), (6, 7, 0, 0),
})


def peak_rss_mib():
    """Return peak resident memory in MiB on macOS and Linux."""

    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return value / (1024 * 1024)
    return value / 1024


def add_zero_or_two_state(pool, add_clause, terms):
    """Portable CNF for ``sum(terms) in {0, 2}``.

    ``one`` and ``two`` are exact prefix predicates for seeing at least one
    and at least two true inputs.  A third true input is forbidden.  The last
    input is handled directly, saving two state variables per fibre.
    """

    assert len(terms) >= 3
    one = terms[0]
    two = None
    for index, term in enumerate(terms[1:-1], start=1):
        new_one = pool.new()
        # new_one <-> (one or term)
        add_clause([-one, new_one])
        add_clause([-term, new_one])
        add_clause([one, term, -new_one])

        new_two = pool.new()
        if index == 1:
            # No earlier pair exists: new_two <-> (one and term).
            add_clause([-new_two, one])
            add_clause([-new_two, term])
            add_clause([-one, -term, new_two])
        else:
            # new_two <-> (two or (one and term)).
            add_clause([-two, new_two])
            add_clause([-one, -term, new_two])
            add_clause([-new_two, two, one])
            add_clause([-new_two, two, term])
            # Once two inputs occurred, another input is forbidden.
            add_clause([-two, -term])
        one, two = new_one, new_two

    last = terms[-1]
    assert two is not None
    # Reject final counts one and three; counts zero and two remain.
    add_clause([one, -last])          # prefix zero and last true
    add_clause([-one, two, last])     # prefix one and last false
    add_clause([-two, -last])         # prefix two and last true


def hnf_odd_relation(rows, number_cells):
    """Extract a guaranteed integer odd relation using an HNF transform."""

    augmented = [list(row) + [1] for row in rows]
    augmented.append([0] * number_cells + [2])
    hnf, transform = fmpz_mat(augmented).hnf(transform=True)
    for row_number in range(hnf.nrows()):
        values = tuple(
            int(hnf[row_number, column])
            for column in range(hnf.ncols())
        )
        if any(values[:-1]) or values[-1] != 1:
            continue
        relation = tuple(
            int(transform[row_number, index])
            for index in range(len(rows))
        )
        epsilon_coefficient = int(
            transform[row_number, len(rows)]
        )
        assert sum(relation) + 2 * epsilon_coefficient == 1
        assert all(
            sum(
                relation[index] * rows[index][column]
                for index in range(len(rows))
            ) == 0
            for column in range(number_cells)
        )
        return relation
    return None


def _sparse_signed_sum(left, right, left_sign, right_sign):
    """Return a sparse tuple for a signed sum of two sparse row tuples."""

    answer = []
    left_index = right_index = 0
    while left_index < len(left) or right_index < len(right):
        if (right_index == len(right)
                or (left_index < len(left)
                    and left[left_index][0] < right[right_index][0])):
            column, value = left[left_index]
            value *= left_sign
            left_index += 1
        elif (left_index == len(left)
              or right[right_index][0] < left[left_index][0]):
            column, value = right[right_index]
            value *= right_sign
            right_index += 1
        else:
            column = left[left_index][0]
            value = (
                left_sign * left[left_index][1]
                + right_sign * right[right_index][1]
            )
            left_index += 1
            right_index += 1
        if value:
            answer.append((column, value))
    return tuple(answer)


def first_unit_triangle_circuit(rows):
    """Find one exact three-row odd relation with coefficients ``+/-1``.

    Exponent-difference rows have at most eight nonzero entries among 252
    columns.  Hashing their sparse forms avoids constructing a 252-tuple for
    each signed row pair.  Returning one circuit is enough for a sound CEGAR
    cut; failure to find one is *not* treated as lattice consistency.
    """

    if len(rows) < 3:
        return None
    sparse_rows = tuple(
        tuple((column, value) for column, value in enumerate(row) if value)
        for row in rows
    )
    locations = {}
    for index, row in enumerate(sparse_rows):
        locations.setdefault(row, []).append(index)

    for left in range(len(rows)):
        for right in range(left + 1, len(rows)):
            for left_sign in (-1, 1):
                for right_sign in (-1, 1):
                    target = _sparse_signed_sum(
                        sparse_rows[left], sparse_rows[right],
                        -left_sign, -right_sign,
                    )
                    for third in locations.get(target, ()):
                        if third == left or third == right:
                            continue
                        signed_indices = sorted((
                            (left, left_sign),
                            (right, right_sign),
                            (third, 1),
                        ))
                        indices = tuple(index for index, _sign in signed_indices)
                        signs = tuple(sign for _index, sign in signed_indices)
                        assert sum(signs) & 1
                        assert all(
                            sum(
                                sign * rows[index][column]
                                for index, sign in zip(indices, signs)
                            ) == 0
                            for column in range(len(rows[0]))
                        )
                        return indices, signs
    return None


class FullSupportSearch:
    def __init__(
        self,
        orbit,
        min_cells,
        max_cells,
        solver_name,
        encoding,
        symmetry_lex,
        progress_every,
        allow_extra_constants=False,
        monomial_seed=False,
        phase_consistent_seed=False,
    ):
        self.orbit = orbit
        self.targets = signed.core.target_orbits(N)[orbit]
        self.matchings = tuple(
            signed.core.perfect_matchings(tuple(range(N)))
        )
        assert len(self.matchings) == 105
        self.cells = tuple(
            (u, v, a, b)
            for u, v in combinations(range(N), 2)
            for a in range(Q)
            for b in range(Q)
        )
        assert len(self.cells) == 252
        self.cell_index = {
            cell: index for index, cell in enumerate(self.cells)
        }
        self.pool = signed.core.Pool()
        self.support = {cell: self.pool.new() for cell in self.cells}
        self.forced_support = frozenset(
            (u, v, color, color)
            for color, target in enumerate(self.targets)
            for u, v in target
        )
        self.automorphisms = signed.target_automorphisms(self.targets)
        if orbit == 39:
            assert len(self.automorphisms) == 8
        self.symmetry_lex = symmetry_lex
        self.allow_extra_constants = allow_extra_constants
        self.encoding = encoding
        self.max_cells = max_cells
        self.min_cells = min_cells
        self.solver = Solver(name=solver_name)
        self.clause_count = 0
        self.clause_literals = 0
        self.cardinality_count = 0
        self.cardinality_literals = 0
        self.parity_core_cuts = set()
        self.lattice_core_cuts = set()
        self.exact_support_cuts = set()
        self.pure_term_variables = {}
        self.pure_fibre_trigger_variables = {}
        self.seed_triangle_circuits = 0
        self.seed_triangle_clauses = 0
        self.target_dense_triangle_clauses = 0
        self.pure_zero_schema_clauses = 0
        self.pure_fibre_trigger_clauses = 0
        self.started = monotonic()

        if encoding == "native":
            if not self.solver.supports_atmost():
                try:
                    self.solver.activate_atmost()
                except (AttributeError, NotImplementedError):
                    pass
            if not self.solver.supports_atmost():
                self.solver.delete()
                raise ValueError(
                    f"solver {solver_name!r} has no native at-most support"
                )

        self._add_base(symmetry_lex)
        if self.allow_extra_constants:
            self._add_pure_term_variables()
        if max_cells is not None:
            literals = [self.support[cell] for cell in self.cells]
            if encoding == "native":
                self.add_atmost(literals, max_cells)
            else:
                cardinality = CardEnc.atmost(
                    lits=literals,
                    bound=max_cells,
                    top_id=self.pool.top,
                    encoding=EncType.kmtotalizer,
                )
                self.pool.top = cardinality.nv
                self.add_clauses(cardinality.clauses)
        if min_cells is not None:
            literals = [-self.support[cell] for cell in self.cells]
            bound = len(literals) - min_cells
            if encoding == "native":
                self.add_atmost(literals, bound)
            else:
                cardinality = CardEnc.atmost(
                    lits=literals,
                    bound=bound,
                    top_id=self.pool.top,
                    encoding=EncType.kmtotalizer,
                )
                self.pool.top = cardinality.nv
                self.add_clauses(cardinality.clauses)

        mixed = 0
        term_count = 0
        for coloring in product(range(Q), repeat=N):
            if len(set(coloring)) == 1:
                continue
            terms = []
            for matching in self.matchings:
                decorated = signed.decorated_term(coloring, matching)
                term = self.pool.new()
                terms.append(term)
                term_count += 1
                # Target cells are unit true.  Removing them from this
                # conjunction is a semantics-preserving propagation aid.
                variables = [
                    self.support[cell]
                    for cell in decorated
                    if cell not in self.forced_support
                ]
                if not variables:
                    self.add_clause([term])
                else:
                    for variable in variables:
                        self.add_clause([-term, variable])
                    self.add_clause(
                        [-variable for variable in variables] + [term]
                    )

            if encoding == "native":
                # With left == right, the two constraints say
                #   sum(terms) + 2*(not left) <= 2
                #   sum(not terms) + 2*left <= len(terms).
                # Hence sum(terms) is zero when left is false and exactly two
                # when it is true.  A distinct right bit avoids relying on
                # duplicate-literal handling in native cardinality solvers.
                left = self.pool.new()
                right = self.pool.new()
                self.add_clause([-left, right])
                self.add_clause([left, -right])
                self.add_atmost(terms + [-left, -right], 2)
                self.add_atmost(
                    [-term for term in terms] + [left, right], len(terms)
                )
            else:
                add_zero_or_two_state(self.pool, self.add_clause, terms)
            mixed += 1
            if progress_every and mixed % progress_every == 0:
                print(
                    f"build fibres={mixed}/6558 vars={self.pool.top} "
                    f"clauses={self.clause_count} "
                    f"native_atmost={self.cardinality_count} "
                    f"rss_mib={peak_rss_mib():.1f} "
                    f"seconds={monotonic() - self.started:.1f}",
                    flush=True,
                )
        assert mixed == Q ** N - Q == 6558
        assert term_count == mixed * len(self.matchings) == 688590
        self.mixed_fibres = mixed
        self.term_count = term_count
        if monomial_seed:
            self._install_orbit40_seed(phase_consistent_seed)
        else:
            self.solver.set_phases(
                [-self.support[cell] for cell in self.cells]
            )

    def _add_base(self, symmetry_lex):
        # Force the three target constant matchings and forbid every other
        # term in each constant fibre.  Forced literals are removed from the
        # forbidding clauses because they are unit true.
        for color, target in enumerate(self.targets):
            target_set = set(target)
            for u, v in target:
                self.add_clause([self.support[u, v, color, color]])
            if not self.allow_extra_constants:
                coloring = (color,) * N
                for matching in self.matchings:
                    if set(matching) == target_set:
                        continue
                    decorated = signed.decorated_term(coloring, matching)
                    clause = [
                        -self.support[cell]
                        for cell in decorated
                        if cell not in self.forced_support
                    ]
                    assert clause
                    self.add_clause(clause)

        if symmetry_lex:
            identity = tuple(range(N)), tuple(range(Q))
            variables = [self.support[cell] for cell in self.cells]
            for vertex_permutation, color_permutation in self.automorphisms:
                if (vertex_permutation, color_permutation) == identity:
                    continue
                images = [
                    self.support[signed.image_cell(
                        cell, vertex_permutation, color_permutation
                    )]
                    for cell in self.cells
                ]
                clauses = []
                signed.add_lex_leader(
                    clauses, self.pool, variables, images
                )
                self.add_clauses(clauses)

    def _install_orbit40_seed(self, phase_consistent_seed=False):
        """Phase the 28-cell boundary and preload its 48 odd triangles."""

        if self.orbit != 40 or not self.allow_extra_constants:
            raise ValueError(
                "--monomial-seed requires orbit 40 and "
                "--allow-extra-constants"
            )
        seed = (
            ORBIT40_PHASE_CONSISTENT_SEED
            if phase_consistent_seed
            else orbit40_boundary.boundary_support()
        )
        if self.symmetry_lex:
            images = (
                frozenset(
                    signed.image_cell(
                        cell, vertex_permutation, color_permutation
                    )
                    for cell in seed
                )
                for vertex_permutation, color_permutation
                in self.automorphisms
            )
            seed = min(
                images,
                key=lambda support_set: tuple(
                    cell in support_set for cell in self.cells
                ),
            )
        assert len(seed) == (36 if phase_consistent_seed else 28)
        assert self.forced_support <= seed
        self.solver.set_phases([
            self.support[cell] if cell in seed else -self.support[cell]
            for cell in self.cells
        ])
        boundary_seed = orbit40_boundary.boundary_support()
        fibres = signed.core.exact_fibres(
            N, boundary_seed, self.matchings
        )
        mixed, rows = toric_n8.exponent_rows(self, fibres)
        circuits = toric_n8.unit_triangle_circuits(rows)
        assert len(circuits) == 48
        boundary_guards = set()
        for indices in circuits:
            guarded = {
                cell
                for index in indices
                for _matching_number, decorated in mixed[index][1]
                for cell in decorated
            }
            assert len(guarded) == 10
            boundary_guards.add(frozenset(guarded))
        guards = set(toric_n8.global_triangle_guards())
        assert len(guards) == 181440
        assert boundary_guards <= guards
        dense_guards = set(
            toric_n8.target_dense_triangle_high_overlap_guards(
                self.targets, 3
            )
        )
        assert len(dense_guards) == 28800
        assert guards.isdisjoint(dense_guards)
        all_guards = guards | dense_guards
        # Retain only compact integer masks while deduplicating target-unit
        # simplifications.  The large guard frozensets are construction data,
        # not solver state, and are released before the first SAT call.
        reduced_masks = set()
        for original in all_guards:
            guard = frozenset(original - self.forced_support)
            assert guard
            mask = sum(1 << self.cell_index[cell] for cell in guard)
            assert mask not in reduced_masks
            reduced_masks.add(mask)
            self.add_clause([
                -self.support[cell] for cell in sorted(guard)
            ])
        self.seed_triangle_circuits = len(circuits)
        self.seed_triangle_clauses = len(reduced_masks)
        self.target_dense_triangle_clauses = len(dense_guards)
        assert self.seed_triangle_clauses == 210240
        # The production orbit factories are cached because their independent
        # verifiers reuse them.  This process only needs the emitted clauses;
        # release the much larger frozenset construction objects before
        # building the hybrid pure-zero schemas and entering the SAT loop.
        del guards, dense_guards, all_guards, reduced_masks, boundary_guards
        toric_n8.global_triangle_guards.cache_clear()
        toric_n8.global_diagonal_triangle_guards.cache_clear()
        toric_n8.global_additional_triangle_guards.cache_clear()
        toric_n8.target_dense_triangle_high_overlap_guards.cache_clear()
        self._install_one_row_pure_zero_schemas()

    def _install_one_row_pure_zero_schemas(self):
        """Preload all 35,328 target-compatible one-row pure-zero cuts."""

        matching_index = {
            frozenset(matching): number
            for number, matching in enumerate(self.matchings)
        }
        target_matching = {
            color: matching_index[frozenset(target)]
            for color, target in enumerate(self.targets)
        }
        schemas = toric_n8.target_complete_one_row_pure_zero_schemas(
            self.targets
        )
        # Factor each repeated exact-pure-fibre condition through one
        # existential trigger.  Four-cycle rows can annihilate unions of one,
        # two, or all three cancellation pairs, so the exact fibres here have
        # sizes 2, 4, and 6.  Eliminating the trigger recovers the original
        # 106--108-literal nogoods exactly.
        (
            self.pure_fibre_trigger_variables,
            self.pure_fibre_trigger_clauses,
        ) = toric_n8.install_pure_fibre_trigger_variables(
            self, self.pure_term_variables, schemas
        )
        assert len(self.pure_fibre_trigger_variables) == 204
        assert self.pure_fibre_trigger_clauses == 204

        seen = set()
        source_schemas = 0
        reduced_guard_sizes = {}
        for guard, color, present_matchings in schemas:
            source_schemas += 1
            present = frozenset(
                matching_index[matching] for matching in present_matchings
            )
            assert len(present) in (2, 4, 6)
            assert target_matching[color] in present
            reduced_guard = frozenset(guard - self.forced_support)
            reduced_guard_sizes[len(reduced_guard)] = (
                reduced_guard_sizes.get(len(reduced_guard), 0) + 1
            )
            support_mask = sum(
                1 << self.cell_index[cell] for cell in reduced_guard
            )
            key = support_mask, color, present
            assert key not in seen
            seen.add(key)
            clause = [
                -self.support[cell] for cell in sorted(reduced_guard)
            ]
            clause.append(-self.pure_fibre_trigger_variables[color, present])
            assert len(clause) == len(reduced_guard) + 1
            self.add_clause(clause)
        assert source_schemas == len(seen) == 35328
        assert reduced_guard_sizes == {2: 96, 3: 3840, 4: 31392}
        self.pure_zero_schema_clauses = len(seen)
        del schemas
        toric_n8.target_complete_one_row_pure_zero_schemas.cache_clear()
        toric_n8.target_one_row_pure_zero_schemas.cache_clear()

    def _add_pure_term_variables(self):
        """Install exact indicators for all 315 pure matching terms."""

        for color in range(Q):
            coloring = (color,) * N
            for matching_number, matching in enumerate(self.matchings):
                decorated = signed.decorated_term(coloring, matching)
                term = self.pool.new()
                self.pure_term_variables[color, matching_number] = term
                variables = [
                    self.support[cell]
                    for cell in decorated
                    if cell not in self.forced_support
                ]
                if not variables:
                    self.add_clause([term])
                else:
                    for variable in variables:
                        self.add_clause([-term, variable])
                    self.add_clause(
                        [-variable for variable in variables] + [term]
                    )
        assert len(self.pure_term_variables) == Q * len(self.matchings) == 315

    def add_clause(self, clause):
        self.solver.add_clause(clause)
        self.clause_count += 1
        self.clause_literals += len(clause)

    def add_clauses(self, clauses):
        for clause in clauses:
            self.add_clause(clause)

    def add_atmost(self, literals, bound):
        self.solver.add_atmost(literals, bound)
        self.cardinality_count += 1
        self.cardinality_literals += len(literals)

    def decode(self, model):
        positive = {literal for literal in model if literal > 0}
        return frozenset(
            cell for cell in self.cells
            if self.support[cell] in positive
        )

    def parity_core(self, fibres):
        """Return an inconsistent subset of mixed odd-parity equations."""

        equations = []
        for coloring, terms in sorted(fibres.items()):
            if len(set(coloring)) == 1:
                continue
            assert len(terms) == 2
            mask = 0
            for cell in set(terms[0][1]) ^ set(terms[1][1]):
                mask ^= 1 << self.cell_index[cell]
            equations.append((coloring, terms, mask))

        basis = {}

        def insert(mask, rhs, dependency):
            while mask:
                pivot = mask.bit_length() - 1
                previous = basis.get(pivot)
                if previous is None:
                    basis[pivot] = mask, rhs, dependency
                    return None
                mask ^= previous[0]
                rhs ^= previous[1]
                dependency ^= previous[2]
            return dependency if rhs else None

        # The target signs are gauged positive.
        for color, target in enumerate(self.targets):
            for u, v in target:
                index = self.cell_index[u, v, color, color]
                assert insert(1 << index, 0, 0) is None

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
        equations, core = self.parity_core(fibres)
        if core is None:
            return 0, 0
        guarded = set()
        for index in core:
            _coloring, terms, _mask = equations[index]
            guarded.update(terms[0][1])
            guarded.update(terms[1][1])
        return len(core), self._add_guarded_support_cut(
            guarded, self.parity_core_cuts
        )

    def _add_guarded_support_cut(self, guarded, seen):
        """Forbid a cell union and, under lex leaders, all its images."""

        keys = {frozenset(guarded)}
        if self.symmetry_lex:
            for vertex_permutation, color_permutation in self.automorphisms:
                keys.add(frozenset(
                    signed.image_cell(
                        cell, vertex_permutation, color_permutation
                    )
                    for cell in guarded
                ))
        new_keys = keys - seen
        for key in sorted(new_keys, key=lambda item: tuple(sorted(item))):
            self.add_clause([
                -self.support[cell]
                for cell in sorted(key - self.forced_support)
            ])
        seen.update(new_keys)
        return len(new_keys)

    def mixed_rows(self, fibres):
        mixed = [
            (coloring, terms)
            for coloring, terms in sorted(fibres.items())
            if len(set(coloring)) > 1
        ]
        assert all(len(terms) == 2 for _coloring, terms in mixed)
        rows = [
            signed.core.exponent_row(
                terms[0][1], terms[1][1], self.cell_index, len(self.cells)
            )
            for _coloring, terms in mixed
        ]
        return mixed, rows

    def add_lattice_core_cut(self, mixed, rows):
        """Block an exact integer odd relation among mixed binomials."""

        triangle = first_unit_triangle_circuit(rows)
        if triangle is not None:
            indices, _signs = triangle
            guarded = {
                cell
                for index in indices
                for _matching_number, decorated in mixed[index][1]
                for cell in decorated
            }
            cuts = self._add_guarded_support_cut(
                guarded, self.lattice_core_cuts
            )
            assert cuts
            return 3, cuts, "sparse-first-unit-triangle"

        relation = signed.core.flint_odd_relation(rows)
        source = "kernel"
        if relation is None:
            relation = hnf_odd_relation(rows, len(self.cells))
            source = "hnf-transform"
        assert relation is not None
        assert sum(relation) % 2
        used = tuple(
            index for index, value in enumerate(relation) if value
        )
        assert used
        guarded = {
            cell
            for index in used
            for _matching_number, decorated in mixed[index][1]
            for cell in decorated
        }
        cuts = self._add_guarded_support_cut(
            guarded, self.lattice_core_cuts
        )
        return len(used), cuts, source

    def add_exact_support_cut(self, selected):
        """Block one exact 252-bit support and optional symmetry images."""

        supports = {frozenset(selected)}
        if self.symmetry_lex:
            for vertex_permutation, color_permutation in self.automorphisms:
                supports.add(frozenset(
                    signed.image_cell(
                        cell, vertex_permutation, color_permutation
                    )
                    for cell in selected
                ))
        new_supports = supports - self.exact_support_cuts
        assert new_supports
        for support_set in sorted(
            new_supports, key=lambda item: tuple(sorted(item))
        ):
            self.add_clause([
                -self.support[cell] if cell in support_set
                else self.support[cell]
                for cell in self.cells
            ])
        self.exact_support_cuts.update(new_supports)
        return len(new_supports)

    def add_zero_product_cut(self, fibres, mixed, rows):
        """Preserve neither all mixed pairs nor the exact three pure fibres.

        An exact reducer first minimizes to mixed rows and pure colors whose
        product is still zero.  Keeping both terms of those mixed binomials
        preserves their Laurent rows because the full 0/2 formula forbids a
        third term.  Keeping the chosen pure matching indicators unchanged
        preserves those pure polynomials.  The quotient product therefore
        remains zero, so the negation is a sound toric nogood.
        """

        assert self.allow_extra_constants
        used_rows, used_colors = (
            signed.core.minimize_zero_product_certificate(
                N, fibres, rows, self.cells, self.cell_index
            )
        )
        guarded = {
            cell
            for index in used_rows
            for _matching_number, decorated in mixed[index][1]
            for cell in decorated
        }
        clause = [
            -self.support[cell]
            for cell in sorted(guarded - self.forced_support)
        ]
        for color in used_colors:
            present = {
                matching_number
                for matching_number, _decorated
                in fibres[(color,) * N]
            }
            for matching_number in range(len(self.matchings)):
                term = self.pure_term_variables[color, matching_number]
                clause.append(-term if matching_number in present else term)
        self.add_clause(clause)
        return (
            len(clause), len(guarded), len(used_rows), tuple(used_colors)
        )

    def verify_structural(self, selected):
        fibres = signed.core.exact_fibres(
            N, selected, self.matchings
        )
        for color, target in enumerate(self.targets):
            terms = fibres.get((color,) * N, ())
            target_cells = {
                (u, v, color, color) for u, v in target
            }
            if self.allow_extra_constants:
                assert any(
                    set(decorated) == target_cells
                    for _matching_number, decorated in terms
                )
            else:
                assert len(terms) == 1
                assert set(terms[0][1]) == target_cells
        for coloring, terms in fibres.items():
            if len(set(coloring)) > 1:
                assert len(terms) == 2
        return fibres

    def delete(self):
        self.solver.delete()


def write_solution(path, search, selected, rounds, mode, weights=None,
                   root_order=None, root_exponents=None, details=None):
    payload = {
        "n": N,
        "orbit": search.orbit,
        "targets": [
            [list(edge) for edge in matching]
            for matching in search.targets
        ],
        "max_cells": search.max_cells,
        "min_cells": search.min_cells,
        "allow_extra_constants": search.allow_extra_constants,
        "rounds": rounds,
        "mode": mode,
        "selected_cells": [],
    }
    for cell in sorted(selected):
        entry = {"cell": list(cell)}
        if weights is not None:
            entry["weight"] = weights[cell]
        if root_exponents is not None:
            entry["root_exponent"] = root_exponents[cell]
        payload["selected_cells"].append(entry)
    if root_order is not None:
        payload["root_order"] = root_order
    if details:
        payload.update(details)
    destination = Path(path)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n")
    temporary.replace(destination)


def run(args):
    search = FullSupportSearch(
        args.orbit,
        args.min_cells,
        args.max_cells,
        args.solver,
        args.encoding,
        args.symmetry_lex,
        args.progress_every,
        args.allow_extra_constants,
        args.monomial_seed,
        args.phase_consistent_seed,
    )
    if args.dense_phase:
        search.solver.set_phases([
            search.support[cell] for cell in search.cells
        ])
    if args.phase_support:
        phase_payload = json.loads(Path(args.phase_support).read_text())
        if phase_payload.get("n") != N or phase_payload.get("orbit") != args.orbit:
            raise ValueError("phase support has incompatible n/orbit")
        phase_selected = frozenset(
            tuple(entry["cell"])
            for entry in phase_payload["selected_cells"]
        )
        if not search.forced_support <= phase_selected:
            raise ValueError("phase support omits a forced target cell")
        if not phase_selected <= frozenset(search.cells):
            raise ValueError("phase support contains an unknown cell")
        if search.symmetry_lex:
            phase_selected = min(
                (
                    frozenset(
                        signed.image_cell(
                            cell, vertex_permutation, color_permutation
                        )
                        for cell in phase_selected
                    )
                    for vertex_permutation, color_permutation
                    in search.automorphisms
                ),
                key=lambda support_set: tuple(
                    cell in support_set for cell in search.cells
                ),
            )
        search.solver.set_phases([
            search.support[cell]
            if cell in phase_selected else -search.support[cell]
            for cell in search.cells
        ])
    print(
        f"BUILT orbit={args.orbit} min_cells={args.min_cells} "
        f"cap={args.max_cells} "
        f"mode={args.mode} encoding={args.encoding} "
        f"symmetry_lex={args.symmetry_lex} "
        f"dense_phase={args.dense_phase} "
        f"phase_support={args.phase_support} "
        f"extra_constants={args.allow_extra_constants} "
        f"fibres={search.mixed_fibres} terms={search.term_count} "
        f"pure_terms={len(search.pure_term_variables)} "
        f"variables={search.pool.top} clauses={search.clause_count} "
        f"clause_literals={search.clause_literals} "
        f"native_atmost={search.cardinality_count} "
        f"native_literals={search.cardinality_literals} "
        f"seed_triangles={search.seed_triangle_circuits}/"
        f"{search.seed_triangle_clauses} "
        f"target_dense_triangles={search.target_dense_triangle_clauses} "
        f"pure_zero_schemas={search.pure_zero_schema_clauses} "
        f"pure_fibre_triggers={search.pure_fibre_trigger_clauses} "
        f"rss_mib={peak_rss_mib():.1f} "
        f"seconds={monotonic() - search.started:.1f}",
        flush=True,
    )
    if args.build_only:
        search.delete()
        return None

    try:
        for round_number in range(args.max_rounds):
            solve_started = monotonic()
            if not search.solver.solve():
                print(
                    f"UNSAT EXACT mode={args.mode} orbit={args.orbit} "
                    f"max_cells={args.max_cells} rounds={round_number} "
                    f"variables={search.pool.top} "
                    f"clauses={search.clause_count} "
                    f"native_atmost={search.cardinality_count} "
                    f"rss_mib={peak_rss_mib():.1f} "
                    f"solve_seconds={monotonic() - solve_started:.1f}",
                    flush=True,
                )
                return None
            selected = search.decode(search.solver.get_model())
            fibres = search.verify_structural(selected)
            mixed, rows = search.mixed_rows(fibres)
            if args.candidate_output:
                write_solution(
                    args.candidate_output,
                    search,
                    selected,
                    round_number,
                    "structural",
                    details={
                        "mixed_fibres": len(mixed),
                        "candidate_for_mode": args.mode,
                    },
                )
                print(
                    f"STRUCTURAL_CANDIDATE round={round_number} "
                    f"cells={len(selected)} mixed_fibres={len(mixed)} "
                    f"path={args.candidate_output} "
                    f"solve_seconds={monotonic() - solve_started:.1f}",
                    flush=True,
                )

            if args.mode == "structural":
                print(
                    f"SAT STRUCTURAL EXACT orbit={args.orbit} "
                    f"max_cells={args.max_cells} cells={len(selected)} "
                    f"mixed_fibres={len(mixed)} rounds={round_number} "
                    f"solve_seconds={monotonic() - solve_started:.1f}",
                    flush=True,
                )
                for cell in sorted(selected):
                    print(f"  {cell}")
                if args.output:
                    write_solution(
                        args.output, search, selected, round_number,
                        "structural",
                        details={"mixed_fibres": len(mixed)},
                    )
                return selected, fibres

            if args.mode == "toric":
                consistent, lattice = signed.core.signed_quotient_lattice(
                    rows, len(search.cells)
                )
                if consistent:
                    remainder, classes = signed.core.reduced_constant_product(
                        N,
                        fibres,
                        lattice,
                        search.cells,
                        search.cell_index,
                    )
                    if not remainder:
                        assert search.allow_extra_constants
                        (
                            cut_size,
                            guarded_cells,
                            used_rows,
                            used_colors,
                        ) = search.add_zero_product_cut(
                            fibres, mixed, rows
                        )
                        print(
                            f"CONSTANT_PRODUCT_CUT round={round_number} "
                            f"cells={len(selected)} "
                            f"mixed_fibres={len(mixed)} "
                            f"raw_classes={len(classes)} "
                            f"guarded_cells={guarded_cells} "
                            f"used_rows={used_rows}/{len(rows)} "
                            f"used_colors={used_colors} "
                            f"cut_literals={cut_size} "
                            f"solve_seconds="
                            f"{monotonic() - solve_started:.1f}",
                            flush=True,
                        )
                        continue

                    if search.allow_extra_constants:
                        print(
                            f"SURVIVOR TORIC EXACT orbit={args.orbit} "
                            f"max_cells={args.max_cells} "
                            f"cells={len(selected)} "
                            f"mixed_fibres={len(mixed)} "
                            f"quotient_classes={len(remainder)} "
                            f"raw_classes={len(classes)} "
                            f"rounds={round_number} "
                            f"solve_seconds="
                            f"{monotonic() - solve_started:.1f}",
                            flush=True,
                        )
                        for cell in sorted(selected):
                            print(f"  {cell}")
                        if args.output:
                            write_solution(
                                args.output,
                                search,
                                selected,
                                round_number,
                                "toric-survivor",
                                details={
                                    "mixed_fibres": len(mixed),
                                    "quotient_classes": len(remainder),
                                    "raw_constant_classes": len(classes),
                                    "lattice_consistent": True,
                                    "constant_product_nonzero": True,
                                },
                            )
                        return selected, fibres, rows, lattice, remainder

                    # With unique pure fibres, reconstruct one explicit
                    # normalized root-of-unity point and audit it directly.
                    order, exponents = toric_n8.normalized_root_exponents(
                        search, fibres, rows
                    )
                    verified = toric_n8.verify_root_solution(
                        search, selected, order, exponents
                    )
                    assert verified == fibres
                    print(
                        f"SAT TORIC EXACT orbit={args.orbit} "
                        f"max_cells={args.max_cells} cells={len(selected)} "
                        f"mixed_fibres={len(mixed)} "
                        f"quotient_classes={len(remainder)} "
                        f"root_order={order} "
                        f"rounds={round_number} "
                        f"solve_seconds={monotonic() - solve_started:.1f}",
                        flush=True,
                    )
                    for cell in sorted(selected):
                        print(f"  {cell} zeta^{exponents[cell]}")
                    if args.output:
                        write_solution(
                            args.output,
                            search,
                            selected,
                            round_number,
                            "toric",
                            root_order=order,
                            root_exponents=exponents,
                            details={
                                "mixed_fibres": len(mixed),
                                "quotient_classes": len(remainder),
                                "raw_constant_classes": len(classes),
                                "lattice_consistent": True,
                            },
                        )
                    return selected, order, exponents
                used, cuts, relation_source = search.add_lattice_core_cut(
                    mixed, rows
                )
                print(
                    f"LATTICE_CUT round={round_number} "
                    f"cells={len(selected)} mixed_fibres={len(mixed)} "
                    f"used_rows={used}/{len(rows)} cuts={cuts} "
                    f"odd_relation_source={relation_source} "
                    f"solve_seconds={monotonic() - solve_started:.1f}",
                    flush=True,
                )
                continue

            weights = support_only.solve_signs(search, fibres)
            if weights is not None:
                weights = {cell: weights[cell] for cell in selected}
                signed.verify_solution(search, selected, weights)
                print(
                    f"SAT SIGNED EXACT orbit={args.orbit} "
                    f"max_cells={args.max_cells} cells={len(selected)} "
                    f"fibres={len(fibres)} rounds={round_number} "
                    f"solve_seconds={monotonic() - solve_started:.1f}",
                    flush=True,
                )
                for cell in sorted(selected):
                    print(f"  {cell} {weights[cell]:+d}")
                if args.output:
                    write_solution(
                        args.output,
                        search,
                        selected,
                        round_number,
                        "signed",
                        weights=weights,
                    )
                return selected, weights
            core_size, cuts = search.add_parity_core_cut(fibres)
            print(
                f"PARITY_CUT round={round_number} cells={len(selected)} "
                f"fibres={len(fibres)} core={core_size} cuts={cuts} "
                f"solve_seconds={monotonic() - solve_started:.1f}",
                flush=True,
            )
        print(f"BOUNDARY rounds={args.max_rounds}", flush=True)
        return "boundary"
    finally:
        search.delete()


def self_test_zero_or_two():
    """Exhaustively validate both small encodings against their truth table."""

    for encoding, solver_name in (("state", "cadical195"),
                                  ("native", "minicard")):
        pool = signed.core.Pool()
        terms = [pool.new() for _ in range(6)]
        solver = Solver(name=solver_name)
        if encoding == "native":
            left, right = pool.new(), pool.new()
            solver.add_clause([-left, right])
            solver.add_clause([left, -right])
            solver.add_atmost(terms + [-left, -right], 2)
            solver.add_atmost(
                [-term for term in terms] + [left, right], len(terms)
            )
        else:
            add_zero_or_two_state(pool, solver.add_clause, terms)
        for bits in product((0, 1), repeat=len(terms)):
            assumptions = [
                term if bit else -term for term, bit in zip(terms, bits)
            ]
            assert solver.solve(assumptions=assumptions) == (
                sum(bits) in (0, 2)
            ), (encoding, bits)
        solver.delete()
    print("PASS zero-or-two encodings", flush=True)


def self_test_pure_fibre_trigger():
    """Check the existential trigger factorization by truth table."""

    for present_count in (1, 3, 5):
        pool = signed.core.Pool()
        present_terms = [pool.new() for _ in range(present_count)]
        absent_terms = [pool.new() for _ in range(6 - present_count)]
        guard = [pool.new(), pool.new()]
        trigger = pool.new()
        solver = Solver(name="cadical195")
        solver.add_clause(
            [trigger]
            + [-term for term in present_terms]
            + absent_terms
        )
        solver.add_clause([-guard[0], -guard[1], -trigger])
        variables = present_terms + absent_terms + guard
        for bits in product((0, 1), repeat=len(variables)):
            assumptions = [
                variable if bit else -variable
                for variable, bit in zip(variables, bits)
            ]
            exact_fibre = (
                all(bits[:present_count])
                and not any(bits[present_count:6])
            )
            guarded = bits[6] and bits[7]
            assert solver.solve(assumptions=assumptions) == (
                not (exact_fibre and guarded)
            ), (present_count, bits)
        solver.delete()
    print("PASS pure-fibre trigger factorization", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, default=39)
    parser.add_argument("--min-cells", type=int)
    cap = parser.add_mutually_exclusive_group()
    cap.add_argument("--max-cells", type=int)
    cap.add_argument(
        "--no-cell-cap", dest="max_cells", action="store_const", const=None,
        help="omit the support-cardinality cap",
    )
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument(
        "--encoding", choices=("native", "state"), default="native"
    )
    parser.add_argument("--symmetry-lex", action="store_true")
    parser.add_argument(
        "--allow-extra-constants",
        action="store_true",
        help="allow extra pure matchings and use the quotient-product test",
    )
    parser.add_argument(
        "--monomial-seed",
        action="store_true",
        help="phase orbit 40 at its 28-cell boundary and preload 48 circuits",
    )
    parser.add_argument(
        "--phase-consistent-seed",
        action="store_true",
        help="phase orbit 40 toward the audited 36-cell zero-product chart",
    )
    parser.add_argument(
        "--dense-phase",
        action="store_true",
        help="override the support phase preference toward selected cells",
    )
    parser.add_argument(
        "--phase-support",
        help="override support phases from a saved structural JSON model",
    )
    parser.add_argument("--max-rounds", type=int, default=10000)
    parser.add_argument("--progress-every", type=int, default=500)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument(
        "--structural-only", dest="mode", action="store_const",
        const="structural",
    )
    modes.add_argument(
        "--toric", dest="mode", action="store_const", const="toric"
    )
    parser.set_defaults(mode="signed", max_cells=23)
    parser.add_argument("--build-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output")
    parser.add_argument(
        "--candidate-output",
        help="atomically checkpoint each direct-verified structural model",
    )
    args = parser.parse_args()
    if (args.min_cells is not None and args.max_cells is not None
            and args.min_cells > args.max_cells):
        parser.error("--min-cells cannot exceed --max-cells")
    if args.allow_extra_constants and args.mode == "signed":
        parser.error("--allow-extra-constants requires --toric or "
                     "--structural-only")
    if args.monomial_seed and not args.allow_extra_constants:
        parser.error("--monomial-seed requires --allow-extra-constants")
    if args.monomial_seed and args.mode != "toric":
        parser.error("--monomial-seed preloads Laurent cuts and requires "
                     "--toric")
    if args.phase_consistent_seed and not args.monomial_seed:
        parser.error("--phase-consistent-seed requires --monomial-seed")
    if args.dense_phase and args.phase_support:
        parser.error("--dense-phase and --phase-support are mutually exclusive")
    if (args.phase_consistent_seed and args.max_cells is not None
            and args.max_cells < len(ORBIT40_PHASE_CONSISTENT_SEED)):
        parser.error("--phase-consistent-seed needs --max-cells at least 36")
    if args.self_test:
        self_test_zero_or_two()
        self_test_pure_fibre_trigger()
        return
    run(args)


if __name__ == "__main__":
    main()
