#!/usr/bin/env python3
"""Exact F_3 search in the joint C3-equivariant n=8 slice.

The generator acts on vertices as ``(0 1 2)(3 4 5)`` and fixes 6,7.  It
acts simultaneously on colours as ``0 -> 1 -> 2 -> 0``.  Thus the 252
endpoint-colour cells form 84 orbits, and the 6561 colourings form 2187
orbits.  We impose one exact coefficient equation for each colouring orbit.

The search is incremental: a candidate is evaluated exactly on every one of
the 2187 representative colourings, and violated equations are added in
batches.  Each equation still contains all 105 perfect-matching monomials
(after merely collecting identical monomials modulo 3), so an UNSAT result is
an exact finite SAT result, not a sampling or numerical conclusion.

Every pure-colour coefficient equal to one has a supported perfect matching.
The centralizer of the vertex generator has seven orbits on the 105 perfect
matchings.  An equivariant diagonal sign gauge then normalizes the first three
entries of that matching to one, with the fourth merely nonzero.  The seven
``PURE_MATCHING_REPS`` therefore give an exhaustive symmetry split.  See
``verify_f3_c3_equivariant_orbits.py`` for an independent, solver-free audit
of these reductions.

A satisfying F_3 point is only a discovery result: it does not give a
characteristic-zero counterexample without a separate lift.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path

from pysat.formula import IDPool
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType

from search_f3_general import exactly_one, iff_and, iff_xor, perfect_matchings


N = 8
Q = 3
VERTICES = tuple(range(N))
GENERATOR = (1, 2, 0, 4, 5, 3, 6, 7)
MATCHINGS = tuple(perfect_matchings(VERTICES))
assert len(MATCHINGS) == 105

# Lexicographically least representatives of the seven centralizer orbits.
# Their completeness is regenerated from all 8! permutations in the
# independent verifier rather than trusted there as input.
PURE_MATCHING_REPS = (
    ((0, 1), (2, 3), (4, 5), (6, 7)),
    ((0, 1), (2, 3), (4, 6), (5, 7)),
    ((0, 1), (2, 6), (3, 4), (5, 7)),
    ((0, 3), (1, 4), (2, 5), (6, 7)),
    ((0, 3), (1, 4), (2, 6), (5, 7)),
    ((0, 3), (1, 5), (2, 4), (6, 7)),
    ((0, 3), (1, 5), (2, 6), (4, 7)),
)


def canonical_matching(matching):
    return tuple(sorted(
        (min(u, v), max(u, v)) for u, v in matching
    ))


CENTRALIZER = tuple(
    permutation
    for permutation in permutations(VERTICES)
    if all(
        permutation[GENERATOR[vertex]] == GENERATOR[permutation[vertex]]
        for vertex in VERTICES
    )
)
assert len(CENTRALIZER) == 36


def residual_relabellings(branch):
    """Centralizer subgroup preserving the normalized branch assumptions."""
    matching = PURE_MATCHING_REPS[branch]
    first_three = frozenset(matching[:3])
    last = matching[3]
    answer = []
    for permutation in CENTRALIZER:
        first_image = frozenset(canonical_matching(
            ((permutation[u], permutation[v]),)
        )[0] for u, v in matching[:3])
        last_image = canonical_matching(
            ((permutation[last[0]], permutation[last[1]]),)
        )[0]
        if first_image == first_three and last_image == last:
            answer.append(permutation)
    return tuple(answer)


RESIDUAL_RELABELINGS = tuple(
    residual_relabellings(branch) for branch in range(7)
)
assert tuple(map(len, RESIDUAL_RELABELINGS)) == (4, 1, 1, 12, 1, 12, 1)


def normalize_cell(u: int, v: int, left: int, right: int):
    """Put an endpoint-colour cell in the convention u < v."""
    if u < v:
        return u, v, left, right
    return v, u, right, left


def transform_cell(cell):
    """Apply the coupled vertex/colour generator to one cell."""
    u, v, left, right = cell
    return normalize_cell(
        GENERATOR[u], GENERATOR[v],
        (left + 1) % Q, (right + 1) % Q,
    )


def cell_orbit_key(u: int, v: int, left: int, right: int):
    cell = normalize_cell(u, v, left, right)
    orbit = []
    for _ in range(3):
        orbit.append(cell)
        cell = transform_cell(cell)
    assert cell == orbit[0]
    return min(orbit)


ALL_CELLS = tuple(
    (u, v, left, right)
    for u, v in combinations(VERTICES, 2)
    for left, right in product(range(Q), repeat=2)
)
CELL_KEYS = tuple(sorted({cell_orbit_key(*cell) for cell in ALL_CELLS}))
assert len(ALL_CELLS) == 252 and len(CELL_KEYS) == 84
CELL_INDEX = {key: index for index, key in enumerate(CELL_KEYS)}
CELL_TO_INDEX = {
    cell: CELL_INDEX[cell_orbit_key(*cell)] for cell in ALL_CELLS
}


def transform_colouring(colouring):
    """Return c' with c'_{g(v)} = c_v + 1."""
    image = [None] * N
    for vertex in VERTICES:
        image[GENERATOR[vertex]] = (colouring[vertex] + 1) % Q
    return tuple(image)


def colouring_orbit(colouring):
    orbit = []
    for _ in range(3):
        orbit.append(colouring)
        colouring = transform_colouring(colouring)
    assert colouring == orbit[0]
    return tuple(orbit)


COLOURING_REPS = tuple(
    colouring
    for colouring in product(range(Q), repeat=N)
    if colouring == min(colouring_orbit(colouring))
)
assert len(COLOURING_REPS) == 2187


def monomial_key(colouring, matching):
    """A matching monomial as a sorted 4-tuple of the 84 cell indices."""
    return tuple(sorted(
        CELL_TO_INDEX[(u, v, colouring[u], colouring[v])]
        for u, v in matching
    ))


def coefficient_terms(colouring):
    """Collect identical matching monomials, reducing multiplicities mod 3."""
    counts = Counter(monomial_key(colouring, matching) for matching in MATCHINGS)
    return tuple(sorted(
        (monomial, multiplicity % Q)
        for monomial, multiplicity in counts.items()
        if multiplicity % Q
    ))


# Integer cell indices make this cache much smaller than nested cell tuples.
REPRESENTATIVE_TERMS = tuple(
    coefficient_terms(colouring) for colouring in COLOURING_REPS
)
TARGETS = tuple(
    1 if len(set(colouring)) == 1 else 0
    for colouring in COLOURING_REPS
)


def evaluate_terms(entries, terms):
    total = 0
    for monomial, multiplicity in terms:
        term = multiplicity
        for cell_index in monomial:
            term = term * entries[cell_index] % Q
        total = (total + term) % Q
    return total


def evaluate_direct(entries, colouring):
    """Independent-looking raw 105-matching evaluation (no collection)."""
    total = 0
    for matching in MATCHINGS:
        term = 1
        for u, v in matching:
            cell_index = CELL_TO_INDEX[(u, v, colouring[u], colouring[v])]
            term = term * entries[cell_index] % Q
        total = (total + term) % Q
    return total


def verify_all_colourings(entries):
    for colouring in product(range(Q), repeat=N):
        obtained = evaluate_direct(entries, colouring)
        expected = 1 if len(set(colouring)) == 1 else 0
        if obtained != expected:
            raise AssertionError((colouring, obtained, expected))


class EquationEncoder:
    """Incremental exact CNF encoder with shared matching-product circuits."""

    def __init__(self, pool, solver, rows):
        self.pool = pool
        self.solver = solver
        self.rows = rows
        self.term_cache = {}
        self.encoded = set()
        self.clause_count = 0

    def term_variables(self, monomial, clauses):
        """Return (nonzero, parity_of_twos) for a four-entry product."""
        cached = self.term_cache.get(monomial)
        if cached is not None:
            return cached

        nonzero_literals = tuple(-self.rows[index][0] for index in monomial)
        negative_literals = tuple(self.rows[index][2] for index in monomial)
        nonzero = self.pool.id(("term-nonzero", monomial))
        iff_and(clauses, nonzero, nonzero_literals)

        parity = negative_literals[0]
        for position, literal in enumerate(negative_literals[1:], start=1):
            nxt = self.pool.id(("term-parity", monomial, position))
            iff_xor(clauses, nxt, parity, literal)
            parity = nxt
        answer = nonzero, parity
        self.term_cache[monomial] = answer
        return answer

    def add_equation(self, representative_index):
        if representative_index in self.encoded:
            return 0
        clauses = []
        accumulator = tuple(
            self.pool.id(("acc", representative_index, 0, residue))
            for residue in range(Q)
        )
        clauses.extend((
            [accumulator[0]], [-accumulator[1]], [-accumulator[2]],
        ))

        terms = REPRESENTATIVE_TERMS[representative_index]
        for position, (monomial, multiplicity) in enumerate(terms, start=1):
            nonzero, parity = self.term_variables(monomial, clauses)
            nxt = tuple(
                self.pool.id(("acc", representative_index, position, residue))
                for residue in range(Q)
            )
            exactly_one(clauses, nxt)
            for residue in range(Q):
                # Product zero: add 0.  Product nonzero with even/odd parity
                # is +1/-1, subsequently multiplied by its collected
                # multiplicity (1 or 2) in F_3.
                clauses.append([
                    -accumulator[residue], nonzero, nxt[residue],
                ])
                clauses.append([
                    -accumulator[residue], -nonzero, parity,
                    nxt[(residue + multiplicity) % Q],
                ])
                clauses.append([
                    -accumulator[residue], -nonzero, -parity,
                    nxt[(residue + 2 * multiplicity) % Q],
                ])
            accumulator = nxt

        clauses.append([accumulator[TARGETS[representative_index]]])
        self.solver.append_formula(clauses)
        self.encoded.add(representative_index)
        self.clause_count += len(clauses)
        return len(clauses)


def build_base(max_nonzero=None):
    pool = IDPool()
    clauses = []
    rows = []
    for cell_index in range(len(CELL_KEYS)):
        row = tuple(
            pool.id(("entry", cell_index, value)) for value in range(Q)
        )
        exactly_one(clauses, row)
        rows.append(row)
    if max_nonzero is not None:
        encoding = CardEnc.atmost(
            lits=[-row[0] for row in rows],
            bound=max_nonzero,
            top_id=pool.top,
            encoding=EncType.kmtotalizer,
        )
        clauses.extend(encoding.clauses)
        if encoding.nv > pool.top:
            pool.occupy(pool.top + 1, encoding.nv)
    return pool, clauses, tuple(rows)


def decode(model, rows):
    positive = {literal for literal in model if literal > 0}
    answer = []
    for row in rows:
        selected = [value for value, literal in enumerate(row)
                    if literal in positive]
        assert len(selected) == 1
        answer.append(selected[0])
    return tuple(answer)


def branch_assumptions(rows, branch):
    assumptions = []
    indices = []
    for position, (u, v) in enumerate(PURE_MATCHING_REPS[branch]):
        index = CELL_TO_INDEX[(u, v, 0, 0)]
        indices.append(index)
        # Equivariant vertex-colour sign gauges have arbitrary signs at
        # (v,0), subject only to product_v sign_v=1.  On a perfect matching
        # this normalizes any chosen first three nonzero edge entries to 1;
        # the last pair absorbs the product constraint.
        assumptions.append(rows[index][1] if position < 3 else -rows[index][0])
    assert len(set(indices)) == 4
    return tuple(assumptions)


def add_branch_lex_leaders(pool, solver, rows, branch):
    """Gate exact ternary lex leaders by a branch selector.

    The residual relabeling subgroup preserves the three value-one units and
    the fourth nonzero unit of this branch.  Every assignment orbit therefore
    has a lexicographically least member satisfying these constraints.
    """
    identity = tuple(range(N))
    group = RESIDUAL_RELABELINGS[branch]
    if len(group) == 1:
        return None, 0
    selector = pool.id(("branch-lex-selector", branch))
    clauses = []
    for group_index, permutation in enumerate(group):
        if permutation == identity:
            continue
        image = []
        for u, v, left, right in CELL_KEYS:
            transformed = normalize_cell(
                permutation[u], permutation[v], left, right
            )
            image.append(CELL_INDEX[cell_orbit_key(*transformed)])
        assert len(set(image)) == len(CELL_KEYS)

        prefix = pool.id(("lex-prefix", branch, group_index, 0))
        clauses.append([-selector, prefix])
        for position, (left_row, image_index) in enumerate(zip(rows, image)):
            right_row = rows[image_index]
            # If all earlier entries agree, left may not exceed right.
            for left_value in range(Q):
                for right_value in range(left_value):
                    clauses.append([
                        -selector, -prefix,
                        -left_row[left_value], -right_row[right_value],
                    ])
            if position + 1 == len(rows):
                continue
            nxt = pool.id(("lex-prefix", branch, group_index, position + 1))
            # nxt <=> prefix and (left entry == right entry).
            clauses.append([-selector, -nxt, prefix])
            for value in range(Q):
                clauses.append([
                    -selector, -nxt, -left_row[value], right_row[value],
                ])
                clauses.append([
                    -selector, -nxt, left_row[value], -right_row[value],
                ])
                clauses.append([
                    -selector, -prefix, -left_row[value], -right_row[value], nxt,
                ])
            prefix = nxt
    solver.append_formula(clauses)
    return selector, len(clauses)


def write_witness(path, entries, branch):
    payload = {
        "field": 3,
        "symmetry": "vertex (012)(345), fixed 6,7; global colour cycle",
        "pure_matching_branch": branch,
        "entries": [
            {"cell_orbit_representative": list(key), "value": entries[index]}
            for index, key in enumerate(CELL_KEYS)
        ],
    }
    Path(path).write_text(json.dumps(payload, indent=2) + "\n")


def run(args):
    if args.branch is None:
        branches = tuple(range(len(PURE_MATCHING_REPS)))
    else:
        branches = (args.branch,)

    pool, base_clauses, rows = build_base(args.max_nonzero)
    print(
        f"cell_orbits={len(CELL_KEYS)} colouring_orbits={len(COLOURING_REPS)} "
        f"matchings={len(MATCHINGS)} branches={branches} "
        f"base_variables={pool.top} base_clauses={len(base_clauses)} "
        f"max_nonzero={args.max_nonzero}",
        flush=True,
    )
    statuses = {}
    phase_values = None
    if args.entry_phase:
        phase_values = tuple(map(int, args.entry_phase.split(",")))
        if len(phase_values) != len(rows) or any(
            value not in range(Q) for value in phase_values
        ):
            raise ValueError("--entry-phase needs 84 comma-separated values in 0,1,2")
    with Solver(name=args.solver, bootstrap_with=base_clauses) as solver:
        if phase_values is not None:
            phase_literals = []
            for row, selected in zip(rows, phase_values):
                phase_literals.extend(
                    literal if value == selected else -literal
                    for value, literal in enumerate(row)
                )
            solver.set_phases(phase_literals)
        elif args.phase != "none":
            phase_literals = []
            for zero, one, two in rows:
                if args.phase == "sparse":
                    phase_literals.extend((zero, -one, -two))
                else:
                    phase_literals.extend((-zero, one, -two))
            solver.set_phases(phase_literals)

        encoder = EquationEncoder(pool, solver, rows)
        pure_index = COLOURING_REPS.index((0,) * N)
        encoder.add_equation(pure_index)

        branch_selectors = {}

        for branch in branches:
            selector, lex_clauses = add_branch_lex_leaders(
                pool, solver, rows, branch
            )
            branch_selectors[branch] = selector
            assumptions = list(branch_assumptions(rows, branch))
            if args.fix_phase_nonzero:
                if phase_values is None:
                    raise ValueError("--fix-phase-nonzero requires --entry-phase")
                assumptions.extend(
                    rows[index][value]
                    for index, value in enumerate(phase_values)
                    if value != 0
                )
            if args.full_support:
                assumptions.extend(-row[0] for row in rows)
            if selector is not None:
                assumptions.append(selector)
            assumptions = tuple(assumptions)
            print(
                f"branch={branch} residual_group={len(RESIDUAL_RELABELINGS[branch])} "
                f"lex_clauses={lex_clauses}",
                flush=True,
            )
            round_number = 0
            while True:
                round_number += 1
                satisfiable = solver.solve(assumptions=assumptions)
                if not satisfiable:
                    statuses[branch] = "UNSAT"
                    print(
                        f"branch={branch} SAT=False rounds={round_number} "
                        f"equations={len(encoder.encoded)} "
                        f"term_circuits={len(encoder.term_cache)} "
                        f"variables={pool.top} learned_clauses={encoder.clause_count}",
                        flush=True,
                    )
                    break

                entries = decode(solver.get_model(), rows)
                violated = [
                    index
                    for index, terms in enumerate(REPRESENTATIVE_TERMS)
                    if evaluate_terms(entries, terms) != TARGETS[index]
                ]
                if not violated:
                    verify_all_colourings(entries)
                    statuses[branch] = "SAT"
                    print(
                        f"branch={branch} SAT=True rounds={round_number} "
                        "direct_all_6561_colourings=PASS",
                        flush=True,
                    )
                    if args.witness:
                        write_witness(args.witness, entries, branch)
                        print(f"witness={args.witness}", flush=True)
                    for index, key in enumerate(CELL_KEYS):
                        print((*key, entries[index]), flush=True)
                    return statuses

                stale = [index for index in violated if index in encoder.encoded]
                if stale:
                    raise AssertionError(
                        f"CNF encoder mismatch on encoded equations {stale[:8]}"
                    )
                fresh = [index for index in violated if index not in encoder.encoded]
                selected = fresh if args.batch == 0 else fresh[:args.batch]
                added_clauses = sum(encoder.add_equation(index)
                                    for index in selected)
                print(
                    f"branch={branch} round={round_number} violated={len(violated)} "
                    f"added_equations={len(selected)} added_clauses={added_clauses} "
                    f"total_equations={len(encoder.encoded)} "
                    f"term_circuits={len(encoder.term_cache)} variables={pool.top} "
                    f"selected_indices={selected}",
                    flush=True,
                )
                if args.max_rounds and round_number >= args.max_rounds:
                    statuses[branch] = "UNKNOWN"
                    print(f"branch={branch} stopped_at_round_limit", flush=True)
                    break
    return statuses


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--phase", choices=("none", "sparse", "dense"),
                        default="sparse")
    parser.add_argument("--branch", type=int, choices=range(7))
    parser.add_argument(
        "--batch", type=int, default=128,
        help="violated equations learned per round; 0 means all",
    )
    parser.add_argument(
        "--max-rounds", type=int, default=0,
        help="0 means no round limit",
    )
    parser.add_argument("--witness", default="f3_c3_equivariant_witness.json")
    parser.add_argument(
        "--full-support", action="store_true",
        help="discovery subsearch with all 84 entry orbits nonzero",
    )
    parser.add_argument(
        "--entry-phase",
        help="84 comma-separated preferred F3 entry values",
    )
    parser.add_argument("--max-nonzero", type=int)
    parser.add_argument(
        "--fix-phase-nonzero", action="store_true",
        help="fix every nonzero entry supplied by --entry-phase",
    )
    args = parser.parse_args()
    statuses = run(args)
    print("statuses=" + json.dumps(statuses, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
