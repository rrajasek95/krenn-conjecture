#!/usr/bin/env python3
"""Exact CEGAR search for binomial fibres with nonzero constants.

This is the parallel decorated-cell analogue of
``search_monomial_binomial_toric_cegar.py``.  A support is a subset of the
``9 * binom(n,2)`` aggregate cells ``uv;ab``.  One constant matching of
each colour is fixed, and every mixed colouring fibre is required to have
zero or exactly two supported perfect matchings.

For the mixed binomials write ``D`` for the matrix of matching-exponent
differences.  The equations are ``x**D_i = -1``.  Smith reduction does two
jobs exactly:

* an odd integer dependence among the rows of ``D`` is a contradiction;
* if the signs are consistent, it reduces the product of the three full
  constant-fibre Laurent polynomials in the twisted group algebra
  ``C[Z^E / rowspan_Z(D)]``.

That reduced product is nonzero iff some nonzero complex cell weighting
cancels every mixed binomial while leaving all three constant sums nonzero.
Thus a survivor is an exact Krenn counterexample in this restricted chart.
When the product is zero, the learned clause is sound: it permits either a
used mixed binomial to disappear or the exact support of a constant fibre
to change.

The program is an exhaustive finite search only when it prints ``UNSAT``.
Any survivor should be copied into a small solver-independent verifier.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from functools import reduce
from itertools import combinations, permutations, product
from math import gcd

from pysat.solvers import Solver
from flint import fmpz_mat

from search_monomial_no_singleton_sat import (
    canonical_matching,
    perfect_matchings,
    relabel_matching,
    stabilizer_of_canonical_matching,
)


Q = 3


class Pool:
    def __init__(self):
        self.top = 0

    def new(self):
        self.top += 1
        return self.top


def target_orbits(size):
    """Triples of arbitrary perfect matchings modulo vertices and 1<->2."""

    matchings = tuple(perfect_matchings(tuple(range(size))))
    first = canonical_matching(size)
    stabilizer = tuple(stabilizer_of_canonical_matching(size))

    def canonical_pair(second, third):
        forms = []
        for vertex_permutation in stabilizer:
            image_second = relabel_matching(second, vertex_permutation)
            image_third = relabel_matching(third, vertex_permutation)
            forms.extend(((image_second, image_third),
                          (image_third, image_second)))
        return min(forms)

    representatives = {
        canonical_pair(second, third)
        for second in matchings
        for third in matchings
    }
    return tuple((first,) + pair for pair in sorted(representatives))


def build_formula(size, targets):
    pool = Pool()
    cells = tuple(
        (u, v, a, b)
        for u, v in combinations(range(size), 2)
        for a, b in product(range(Q), repeat=2)
    )
    cell_index = {cell: index for index, cell in enumerate(cells)}
    support = {cell: pool.new() for cell in cells}
    matchings = tuple(perfect_matchings(tuple(range(size))))
    clauses = []

    for color, matching in enumerate(targets):
        for u, v in matching:
            clauses.append([support[u, v, color, color]])

    term_variables = {}
    term_cells = {}
    for coloring in product(range(Q), repeat=size):
        fibre = []
        for matching_number, matching in enumerate(matchings):
            decorated = tuple(
                (u, v, coloring[u], coloring[v]) for u, v in matching
            )
            term = pool.new()
            term_variables[coloring, matching_number] = term
            term_cells[coloring, matching_number] = decorated
            fibre.append(term)
            for cell in decorated:
                clauses.append([-term, support[cell]])
            clauses.append([-support[cell] for cell in decorated] + [term])

        if len(set(coloring)) == 1:
            continue
        # A supported mixed term has a distinct mate; no third term exists.
        for term in fibre:
            clauses.append([-term] + [other for other in fibre if other != term])
        clauses.extend([-a, -b, -c] for a, b, c in combinations(fibre, 3))

    return (
        pool,
        clauses,
        cells,
        cell_index,
        support,
        matchings,
        term_variables,
        term_cells,
    )


def decode(model, support):
    positive = {literal for literal in model if literal > 0}
    return frozenset(
        cell for cell, variable in support.items() if variable in positive
    )


def exact_fibres(size, selected, matchings):
    answer = {}
    for coloring in product(range(Q), repeat=size):
        terms = []
        for matching_number, matching in enumerate(matchings):
            decorated = tuple(
                (u, v, coloring[u], coloring[v]) for u, v in matching
            )
            if set(decorated) <= selected:
                terms.append((matching_number, decorated))
        if terms:
            answer[coloring] = tuple(terms)
    return answer


def exponent_vector(decorated, cell_index, number_cells):
    answer = [0] * number_cells
    for cell in decorated:
        answer[cell_index[cell]] += 1
    return answer


def exponent_row(left, right, cell_index, number_cells):
    answer = exponent_vector(left, cell_index, number_cells)
    for cell in right:
        answer[cell_index[cell]] -= 1
    return answer


def signed_quotient_lattice(rows, number_cells, rhs=None):
    """Return consistency and HNF for the twisted binomial quotient.

    Adjoin a formal sign exponent ``epsilon``.  The row ``(d_i,1)`` encodes
    ``x**d_i = -1`` and ``(0,2)`` encodes ``epsilon**2=1``.  The equations
    are inconsistent exactly when the resulting lattice contains ``(0,1)``.
    This test, and all later reductions, need only the row HNF itself; no
    expensive transformation matrix is required.
    """

    if rhs is None:
        rhs = [1] * len(rows)
    assert len(rhs) == len(rows)
    augmented = [list(row) + [bit] for row, bit in zip(rows, rhs)]
    augmented.append([0] * number_cells + [2])
    hnf = fmpz_mat(augmented).hnf()
    hnf_rows = []
    pivots = []
    for row in range(hnf.nrows()):
        values = tuple(int(hnf[row, column]) for column in range(hnf.ncols()))
        if not any(values):
            continue
        pivot = next(column for column, value in enumerate(values) if value)
        assert values[pivot] > 0
        hnf_rows.append(values)
        pivots.append(pivot)
    assert pivots == sorted(pivots)
    lattice = (tuple(hnf_rows), tuple(pivots))
    sign_remainder = quotient_key((0,) * number_cells + (1,), lattice)
    consistent = any(sign_remainder)
    if consistent:
        assert sign_remainder == (0,) * number_cells + (1,)
    return consistent, lattice


def pfaffian_matching_bit(decorated):
    """Sign exponent of a matching in the ordered expanded stub set."""

    pairs = [
        tuple(sorted((Q * u + a, Q * v + b)))
        for u, v, a, b in decorated
    ]
    crossings = sum(
        left < other_left < right < other_right
        or other_left < left < other_right < right
        for index, (left, right) in enumerate(pairs)
        for other_left, other_right in pairs[index + 1:]
    )
    return crossings % 2


def pfaffian_orientation_audit(fibres, cell_index, number_cells):
    """Test global edge-sign coherence of all supported fibre matchings."""

    rows = []
    rhs = []
    for terms in fibres.values():
        for index in range(1, len(terms)):
            rows.append(exponent_row(
                terms[0][1], terms[index][1], cell_index, number_cells
            ))
            rhs.append(
                pfaffian_matching_bit(terms[0][1])
                ^ pfaffian_matching_bit(terms[index][1])
            )
    return signed_quotient_lattice(rows, number_cells, rhs)[0]


def flint_odd_relation(rows):
    """Fast exact odd relation from FLINT's rational-kernel basis.

    The returned relation is always independently checked.  Failure to find
    one is inconclusive because the displayed kernel basis need not be a
    saturated integer basis; ``signed_quotient_lattice`` is the exact test.
    """

    transpose = fmpz_mat([list(column) for column in zip(*rows)])
    kernel, nullity = transpose.nullspace()
    if not nullity:
        return None
    candidates = []
    for column in range(nullity):
        relation = [int(kernel[row, column]) for row in range(kernel.nrows())]
        divisor = reduce(gcd, (abs(value) for value in relation if value), 0)
        relation = [value // divisor for value in relation]
        candidates.append(relation)

    for relation in candidates:
        divisor = reduce(gcd, (abs(value) for value in relation if value), 0)
        if not divisor:
            continue
        relation = [value // divisor for value in relation]
        if sum(relation) % 2 == 0:
            continue
        assert all(
            sum(relation[index] * rows[index][column]
                for index in range(len(rows))) == 0
            for column in range(len(rows[0]))
        )
        return tuple(relation)
    return None


def quotient_key(exponent, lattice):
    """Canonical representative modulo the HNF row lattice."""

    hnf_rows, pivots = lattice
    remainder = list(exponent)
    for row, pivot in zip(hnf_rows, pivots):
        quotient, residue = divmod(remainder[pivot], row[pivot])
        if quotient:
            remainder = [
                value - quotient * basis_value
                for value, basis_value in zip(remainder, row)
            ]
        assert remainder[pivot] == residue
    return tuple(remainder)


def reduced_constant_product(
    size, fibres, lattice, cells, cell_index, colors=tuple(range(Q))
):
    """Return exact signed quotient classes of a product of pure fibres."""

    number_cells = len(cells)
    pure = [fibres[(color,) * size] for color in colors]
    classes = defaultdict(lambda: [0, 0])

    for triple in product(*pure):
        exponent = [0] * number_cells
        for _matching_number, decorated in triple:
            for cell in decorated:
                exponent[cell_index[cell]] += 1

        signed_class = quotient_key(tuple(exponent) + (0,), lattice)
        sign_coordinate = signed_class[-1]
        assert sign_coordinate in (0, 1)
        key = signed_class[:-1]
        classes[key][sign_coordinate] += 1

    remainder = {}
    for key, (positive, negative) in classes.items():
        signed_sum = positive - negative
        if signed_sum:
            remainder[key] = (signed_sum, positive, negative)
    return remainder, classes


def minimize_zero_product_certificate(
    size, fibres, rows, cells, cell_index
):
    """Shrink a zero product to colors and mixed rows that still force it."""

    full_lattice = signed_quotient_lattice(rows, len(cells))[1]

    def zero_for(colors, indices):
        selected_rows = [rows[index] for index in indices]
        consistent, lattice = signed_quotient_lattice(
            selected_rows, len(cells)
        )
        assert consistent  # Removing equations preserves consistency.
        remainder, _classes = reduced_constant_product(
            size,
            fibres,
            lattice,
            cells,
            cell_index,
            colors,
        )
        return not remainder

    chosen_colors = None
    for number_colors in range(1, Q + 1):
        vanishing_color_sets = []
        for colors in combinations(range(Q), number_colors):
            remainder, _classes = reduced_constant_product(
                size, fibres, full_lattice, cells, cell_index, colors
            )
            if not remainder:
                vanishing_color_sets.append(colors)
        if not vanishing_color_sets:
            continue

        # Search all minimum-cardinality vanishing color sets.  Picking the
        # first one before this scan can miss a one-row certificate supported
        # by a later color set, after which deletion minimization cannot add
        # that useful row back.
        for colors in vanishing_color_sets:
            for index in range(len(rows)):
                if zero_for(colors, (index,)):
                    return (index,), tuple(colors)
        chosen_colors = vanishing_color_sets[0]
        break
    assert chosen_colors is not None

    def still_zero(indices):
        return zero_for(chosen_colors, indices)

    active = list(range(len(rows)))
    granularity = 2
    while len(active) >= 2:
        chunk_size = (len(active) + granularity - 1) // granularity
        removed = False
        for start in range(0, len(active), chunk_size):
            discarded = set(active[start:start + chunk_size])
            trial = [index for index in active if index not in discarded]
            if still_zero(trial):
                active = trial
                granularity = max(2, granularity - 1)
                removed = True
                break
        if removed:
            continue
        if granularity >= len(active):
            break
        granularity = min(len(active), 2 * granularity)

    assert still_zero(active)
    return tuple(active), tuple(chosen_colors)


def exact_support_nogood(
    solver,
    size,
    fibres,
    mixed,
    used_rows,
    colors,
    term_variables,
    matchings,
):
    """Block unchanged mixed rows and unchanged three constant fibres."""

    clause = set()
    for index in used_rows:
        coloring, terms = mixed[index]
        for matching_number, _decorated in terms:
            clause.add(-term_variables[coloring, matching_number])

    for color in colors:
        coloring = (color,) * size
        present = {
            matching_number for matching_number, _decorated in fibres[coloring]
        }
        for matching_number in range(len(matchings)):
            literal = term_variables[coloring, matching_number]
            clause.add(-literal if matching_number in present else literal)

    solver.add_clause(sorted(clause))
    return len(clause)


def run_orbit(size, orbit, targets, max_rounds, verbose=False):
    if size != 6:
        raise NotImplementedError(
            "the explicit at-most-two encoding is currently intended for n=6"
        )
    (
        pool,
        clauses,
        cells,
        cell_index,
        support,
        matchings,
        term_variables,
        _term_cells,
    ) = build_formula(size, targets)
    solver = Solver(name="cadical195", bootstrap_with=clauses)
    lattice_cuts = 0
    zero_product_cuts = 0

    for round_number in range(max_rounds):
        if not solver.solve():
            solver.delete()
            return None, (round_number, lattice_cuts, zero_product_cuts)

        selected = decode(solver.get_model(), support)
        fibres = exact_fibres(size, selected, matchings)
        mixed = [
            (coloring, terms)
            for coloring, terms in sorted(fibres.items())
            if len(set(coloring)) > 1
        ]
        assert all(len(terms) == 2 for _coloring, terms in mixed)
        rows = [
            exponent_row(terms[0][1], terms[1][1], cell_index, len(cells))
            for _coloring, terms in mixed
        ]

        consistent, lattice = signed_quotient_lattice(rows, len(cells))
        if not consistent:
            relation = flint_odd_relation(rows)
            used = (
                [index for index, value in enumerate(relation) if value]
                if relation is not None else range(len(rows))
            )
            literals = {
                support[cell]
                for index in used
                for _matching_number, decorated in mixed[index][1]
                for cell in decorated
            }
            solver.add_clause([-literal for literal in literals])
            lattice_cuts += 1
            cut_kind = f"odd({len(used)}/{len(rows)})"
        else:
            remainder, classes = reduced_constant_product(
                size, fibres, lattice, cells, cell_index
            )
            if remainder:
                solver.delete()
                return (
                    selected,
                    fibres,
                    rows,
                    lattice,
                    remainder,
                ), (round_number, lattice_cuts, zero_product_cuts)
            used_rows, used_colors = minimize_zero_product_certificate(
                size, fibres, rows, cells, cell_index
            )
            pfaffian_coherent = pfaffian_orientation_audit(
                fibres, cell_index, len(cells)
            )
            cut_size = exact_support_nogood(
                solver,
                size,
                fibres,
                mixed,
                used_rows,
                used_colors,
                term_variables,
                matchings,
            )
            zero_product_cuts += 1
            cut_kind = (
                f"zero-product(colors={used_colors},rows={len(used_rows)},"
                f"{len(classes)} classes,{cut_size} lits,"
                f"pf={pfaffian_coherent})"
            )

        if verbose or round_number % 100 == 0:
            distribution = Counter(len(terms) for terms in fibres.values())
            print(
                f"orbit={orbit} round={round_number} cells={len(selected)} "
                f"fibres={dict(sorted(distribution.items()))} cut={cut_kind}",
                flush=True,
            )

    solver.delete()
    raise RuntimeError(f"orbit {orbit} reached max_rounds={max_rounds}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, choices=(6,), default=6)
    parser.add_argument("--orbit", type=int)
    parser.add_argument("--max-rounds", type=int, default=100000)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    orbits = target_orbits(args.n)
    indices = range(len(orbits)) if args.orbit is None else (args.orbit,)
    print(f"n={args.n} target_orbits={len(orbits)}", flush=True)
    for orbit in indices:
        result, stats = run_orbit(
            args.n,
            orbit,
            orbits[orbit],
            args.max_rounds,
            args.verbose,
        )
        print(
            f"orbit={orbit} {'SURVIVOR' if result else 'UNSAT'} stats={stats}",
            flush=True,
        )
        if result is None:
            continue
        selected, fibres, _rows, _lattice, remainder = result
        print("targets=", orbits[orbit])
        print(
            "fiber_distribution=",
            dict(sorted(Counter(map(len, fibres.values())).items())),
        )
        print("reduced_product_classes=", len(remainder))
        for cell in sorted(selected):
            print(cell)
        return
    print("all target orbits UNSAT")


if __name__ == "__main__":
    main()
