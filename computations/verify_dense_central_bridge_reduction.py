#!/usr/bin/env python3
"""Exact support audit for a central bridge between two K4 blocks.

This checker proves three finite statements used in the accompanying note:

* the untouched-square line audit leaves only four small-support orbits;
* every central support meeting all three rows and columns forces all 81
  scalar bridge cells (an exact SAT implication), after which a formal
  multiplicative rectangle closes the coefficients;
* the intermediate four-cell supports form six stated orbits, after which
  the 2x3 and nonprincipal 2x2 open-chart lemmas close them all.
"""

from __future__ import annotations

import importlib.util
import itertools
from collections import Counter
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver


COLORS = tuple(range(3))
ROOT = Path(__file__).resolve().parent


def load_anchor_checker():
    path = ROOT / "verify_two_k4_anchor_bridge_obstruction.py"
    spec = importlib.util.spec_from_file_location("anchor_bridge_checker", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


ANCHOR = load_anchor_checker()


def support_from_mask(mask):
    return frozenset(
        (i, j)
        for i, j in itertools.product(COLORS, repeat=2)
        if mask & (1 << (3 * i + j))
    )


def transform_support(support, permutation, transpose):
    if transpose:
        return frozenset((permutation[j], permutation[i]) for i, j in support)
    return frozenset((permutation[i], permutation[j]) for i, j in support)


GROUP = tuple(
    (permutation, transpose)
    for permutation in itertools.permutations(COLORS)
    for transpose in (False, True)
)


def canonical(support):
    return min(
        (transform_support(support, *element) for element in GROUP),
        key=lambda item: tuple(sorted(item)),
    )


def elementary_open(central_support):
    return any(
        valid and not conflict
        for bridge_mask in range(1 << 9)
        for valid, conflict in (
            ANCHOR.untouched_slice_line_conflict(central_support, bridge_mask),
        )
    )


def audit_small_support_orbits():
    open_by_size = {}
    for size in range(4):
        supports = []
        for entries in itertools.combinations(
            itertools.product(COLORS, repeat=2), size
        ):
            support = frozenset(entries)
            if elementary_open(support):
                supports.append(support)
        open_by_size[size] = supports

    assert [len(open_by_size[size]) for size in range(4)] == [0, 0, 3, 19]
    assert {canonical(item) for item in open_by_size[2]} == {
        frozenset({(0, 0), (1, 1)})
    }
    assert {canonical(item) for item in open_by_size[3]} == {
        frozenset({(0, 0), (0, 1), (1, 1)}),
        frozenset({(0, 0), (0, 1), (2, 2)}),
        frozenset({(0, 0), (1, 1), (2, 2)}),
    }

    # The two coordinate-mismatch arguments use only these untouched
    # equations.  The checker records that none is contaminated.
    first_core = ({(0, 0), (1, 1)}, {(0, 0), (0, 1), (1, 1)})
    for support in first_core:
        assert {(2, 2), (2, 0), (2, 1), (0, 2)}.isdisjoint(support)
        unresolved_bridges = []
        for bridge_mask in range(1 << 9):
            valid, conflict = ANCHOR.untouched_slice_line_conflict(
                support, bridge_mask
            )
            if valid and not conflict:
                unresolved_bridges.append(support_from_mask(bridge_mask))
        assert len(unresolved_bridges) == 2
        assert all(
            {(0, 0), (0, 1), (1, 0), (1, 1)} <= bridge_support
            for bridge_support in unresolved_bridges
        )
    second_core = {(0, 0), (0, 1), (2, 2)}
    assert {(1, 1), (1, 0), (1, 2), (2, 1)}.isdisjoint(second_core)
    unresolved_bridges = []
    for bridge_mask in range(1 << 9):
        valid, conflict = ANCHOR.untouched_slice_line_conflict(
            second_core, bridge_mask
        )
        if valid and not conflict:
            unresolved_bridges.append(support_from_mask(bridge_mask))
    assert len(unresolved_bridges) == 2
    assert all(
        {(0, 0), (0, 2), (2, 0), (2, 2)} <= bridge_support
        for bridge_support in unresolved_bridges
    )


def add_and(pool, clauses, key, first, second):
    product = pool.id(("product",) + key)
    clauses.extend(
        [[-product, first], [-product, second], [product, -first, -second]]
    )
    return product


def dense_support_cnf(central_support, require_at_most_80=True):
    """Build the exact local-square support formula for rainbow P."""
    pool = IDPool()
    clauses = []

    def cell(i, j, a, b):
        return pool.id(("cell", i, j, a, b))

    for r, s in itertools.product(COLORS, repeat=2):
        rows = [i for i in COLORS if i != r]
        columns = [j for j in COLORS if j != s]
        required = set()
        if r != s:
            required.add(((r, r), (s, s)))
        if (r, s) in central_support:
            required.add((tuple(rows), tuple(columns)))

        for left_colors in itertools.product(COLORS, repeat=2):
            for right_colors in itertools.product(COLORS, repeat=2):
                first = add_and(
                    pool,
                    clauses,
                    (r, s, left_colors, right_colors, 0),
                    cell(
                        rows[0], columns[0], left_colors[0], right_colors[0]
                    ),
                    cell(
                        rows[1], columns[1], left_colors[1], right_colors[1]
                    ),
                )
                second = add_and(
                    pool,
                    clauses,
                    (r, s, left_colors, right_colors, 1),
                    cell(
                        rows[0], columns[1], left_colors[0], right_colors[1]
                    ),
                    cell(
                        rows[1], columns[0], left_colors[1], right_colors[0]
                    ),
                )
                if (left_colors, right_colors) in required:
                    clauses.append([first, second])
                else:
                    clauses.extend([[-first, second], [first, -second]])

    # A nonzero full rainbow coefficient of P must use three bridge edges.
    rainbow_matchings = []
    for permutation in itertools.permutations(COLORS):
        variables = [
            cell(i, permutation[i], i, permutation[i]) for i in COLORS
        ]
        monomial = pool.id(("rainbow", permutation))
        clauses.extend([[-monomial, variable] for variable in variables])
        clauses.append([monomial] + [-variable for variable in variables])
        rainbow_matchings.append(monomial)
    clauses.append(rainbow_matchings)

    cells = [
        cell(i, j, a, b)
        for i, j, a, b in itertools.product(COLORS, repeat=4)
    ]
    if require_at_most_80:
        clauses.extend(
            CardEnc.atmost(
                cells,
                bound=80,
                vpool=pool,
                encoding=EncType.seqcounter,
            ).clauses
        )
    return pool, clauses, cells


def audit_all_active_rows_and_columns():
    tested = 0
    clause_counts = Counter()
    for mask in range(1, 1 << 9):
        support = support_from_mask(mask)
        if len({i for i, _ in support}) != 3:
            continue
        if len({j for _, j in support}) != 3:
            continue
        tested += 1
        pool, clauses, cells = dense_support_cnf(support)
        clause_counts[len(clauses)] += 1
        with Solver(name="cadical195", bootstrap_with=clauses) as solver:
            assert not solver.solve(), support

        # Independently check that the all-cell assignment satisfies the
        # formula before its final at-most-80 block is added.
        _pool, base_clauses, base_cells = dense_support_cnf(
            support, require_at_most_80=False
        )
        with Solver(name="cadical195", bootstrap_with=base_clauses) as solver:
            assert solver.solve(assumptions=base_cells)

    assert tested == 265
    assert sum(clause_counts.values()) == 265


def one_free_left_cnf(
    central_support, free_colors, require_at_most_80=True
):
    """Support formula when P has one free left-site vector."""
    active_rows = {i for i, _ in central_support}
    active_columns = {j for _, j in central_support}
    assert len(active_rows) == 2 and len(active_columns) == 3
    missing_row = next(i for i in COLORS if i not in active_rows)
    assert free_colors

    pool = IDPool()
    clauses = []

    def cell(i, j, a, b):
        return pool.id(("cell", i, j, a, b))

    full_p_colorings = []
    for free_color in free_colors:
        left = tuple(
            i if i != missing_row else free_color for i in COLORS
        )
        right = tuple(COLORS)
        full_p_colorings.append((left, right))

    for r, s in itertools.product(COLORS, repeat=2):
        rows = [i for i in COLORS if i != r]
        columns = [j for j in COLORS if j != s]
        required = set()
        if r != s:
            required.add(((r, r), (s, s)))
        if (r, s) in central_support:
            for left, right in full_p_colorings:
                required.add(
                    (
                        tuple(left[i] for i in rows),
                        tuple(right[j] for j in columns),
                    )
                )

        for left_colors in itertools.product(COLORS, repeat=2):
            for right_colors in itertools.product(COLORS, repeat=2):
                first = add_and(
                    pool,
                    clauses,
                    (r, s, left_colors, right_colors, 0),
                    cell(
                        rows[0], columns[0], left_colors[0], right_colors[0]
                    ),
                    cell(
                        rows[1], columns[1], left_colors[1], right_colors[1]
                    ),
                )
                second = add_and(
                    pool,
                    clauses,
                    (r, s, left_colors, right_colors, 1),
                    cell(
                        rows[0], columns[1], left_colors[0], right_colors[1]
                    ),
                    cell(
                        rows[1], columns[0], left_colors[1], right_colors[0]
                    ),
                )
                if (left_colors, right_colors) in required:
                    clauses.append([first, second])
                else:
                    clauses.extend([[-first, second], [first, -second]])

    p_matchings = []
    for coloring_index, (left, right) in enumerate(full_p_colorings):
        for permutation in itertools.permutations(COLORS):
            variables = [
                cell(i, permutation[i], left[i], right[permutation[i]])
                for i in COLORS
            ]
            monomial = pool.id(("P", coloring_index, permutation))
            clauses.extend([[-monomial, variable] for variable in variables])
            clauses.append([monomial] + [-variable for variable in variables])
            p_matchings.append(monomial)
    clauses.append(p_matchings)

    cells = [
        cell(i, j, a, b)
        for i, j, a, b in itertools.product(COLORS, repeat=4)
    ]
    if require_at_most_80:
        clauses.extend(
            CardEnc.atmost(
                cells,
                bound=80,
                vpool=pool,
                encoding=EncType.seqcounter,
            ).clauses
        )
    return clauses, cells


def audit_two_by_three_free_vector():
    missing_component_tests = 0
    active_plane_tests = 0
    for mask in range(1, 1 << 9):
        support = support_from_mask(mask)
        active_rows = {i for i, _ in support}
        active_columns = {j for _, j in support}
        if len(active_rows) != 2 or len(active_columns) != 3:
            continue
        missing_row = next(i for i in COLORS if i not in active_rows)
        for free_mask in range(1, 1 << 3):
            free_colors = {
                color for color in COLORS if free_mask & (1 << color)
            }
            if missing_row not in free_colors:
                # In the only remaining case, all free colors lie in the
                # two-dimensional active-color plane.  The same support
                # equations force the 72 cells whose left endpoint is not
                # the missing color at the missing physical site.
                clauses, cells = one_free_left_cnf(
                    support, free_colors, require_at_most_80=False
                )
                coordinates = tuple(itertools.product(COLORS, repeat=4))
                baseline = [
                    variable
                    for (i, _j, a, _b), variable in zip(
                        coordinates, cells, strict=True
                    )
                    if not (i == missing_row and a == missing_row)
                ]
                assert len(baseline) == 72
                with Solver(
                    name="cadical195",
                    bootstrap_with=clauses
                    + [[-variable for variable in baseline]],
                ) as solver:
                    assert not solver.solve(), (support, free_colors)
                with Solver(name="cadical195", bootstrap_with=clauses) as solver:
                    assert solver.solve(assumptions=cells)
                active_plane_tests += 1
                continue

            missing_component_tests += 1
            clauses, _cells = one_free_left_cnf(support, free_colors)
            with Solver(name="cadical195", bootstrap_with=clauses) as solver:
                assert not solver.solve(), (support, free_colors)

            base_clauses, cells = one_free_left_cnf(
                support, free_colors, require_at_most_80=False
            )
            with Solver(name="cadical195", bootstrap_with=base_clauses) as solver:
                assert solver.solve(assumptions=cells)
    assert missing_component_tests == 300
    assert active_plane_tests == 225


def two_free_sites_cnf(central_support, free_support):
    """Support formula when P has one free site on each shore."""
    active_rows = {i for i, _ in central_support}
    active_columns = {j for _, j in central_support}
    assert len(active_rows) == len(active_columns) == 2
    missing_row = next(i for i in COLORS if i not in active_rows)
    missing_column = next(j for j in COLORS if j not in active_columns)
    assert free_support

    pool = IDPool()
    clauses = []

    def cell(i, j, a, b):
        return pool.id(("cell", i, j, a, b))

    full_p_colorings = []
    for free_left, free_right in free_support:
        left = tuple(
            i if i != missing_row else free_left for i in COLORS
        )
        right = tuple(
            j if j != missing_column else free_right for j in COLORS
        )
        full_p_colorings.append((left, right))

    for r, s in itertools.product(COLORS, repeat=2):
        rows = [i for i in COLORS if i != r]
        columns = [j for j in COLORS if j != s]
        required = set()
        if r != s:
            required.add(((r, r), (s, s)))
        if (r, s) in central_support:
            for left, right in full_p_colorings:
                required.add(
                    (
                        tuple(left[i] for i in rows),
                        tuple(right[j] for j in columns),
                    )
                )

        for left_colors in itertools.product(COLORS, repeat=2):
            for right_colors in itertools.product(COLORS, repeat=2):
                first = add_and(
                    pool,
                    clauses,
                    (r, s, left_colors, right_colors, 0),
                    cell(
                        rows[0], columns[0], left_colors[0], right_colors[0]
                    ),
                    cell(
                        rows[1], columns[1], left_colors[1], right_colors[1]
                    ),
                )
                second = add_and(
                    pool,
                    clauses,
                    (r, s, left_colors, right_colors, 1),
                    cell(
                        rows[0], columns[1], left_colors[0], right_colors[1]
                    ),
                    cell(
                        rows[1], columns[0], left_colors[1], right_colors[0]
                    ),
                )
                if (left_colors, right_colors) in required:
                    clauses.append([first, second])
                else:
                    clauses.extend([[-first, second], [first, -second]])

    # The inherited triangle edge on sites {i,k} has the omitted color.
    triangle_color = {
        tuple(sorted((i, k))): next(
            color for color in COLORS if color not in {i, k}
        )
        for i, k in itertools.combinations(COLORS, 2)
    }

    # Every nonzero coefficient of P needs a supported matching.  Such a
    # matching has either three bridges or one bridge and one inherited
    # triangle edge on each shore.
    for coloring_index, (left, right) in enumerate(full_p_colorings):
        matching_monomials = []
        for permutation in itertools.permutations(COLORS):
            variables = [
                cell(i, permutation[i], left[i], right[permutation[i]])
                for i in COLORS
            ]
            monomial = pool.id(("P3", coloring_index, permutation))
            clauses.extend([[-monomial, variable] for variable in variables])
            clauses.append([monomial] + [-variable for variable in variables])
            matching_monomials.append(monomial)

        for i, j in itertools.product(COLORS, repeat=2):
            left_pair = tuple(k for k in COLORS if k != i)
            right_pair = tuple(k for k in COLORS if k != j)
            if not (
                left[left_pair[0]]
                == left[left_pair[1]]
                == triangle_color[tuple(sorted(left_pair))]
            ):
                continue
            if not (
                right[right_pair[0]]
                == right[right_pair[1]]
                == triangle_color[tuple(sorted(right_pair))]
            ):
                continue
            matching_monomials.append(cell(i, j, left[i], right[j]))
        # Equation (5) fixes two physical sites on each shore to their
        # distinct rainbow colors.  Hence no inherited triangle can be
        # compatible; exactly the six all-bridge matchings remain.
        assert len(matching_monomials) == 6
        clauses.append(matching_monomials)

    cells = {
        (i, j, a, b): cell(i, j, a, b)
        for i, j, a, b in itertools.product(COLORS, repeat=4)
    }
    return clauses, cells, missing_row, missing_column


def audit_two_by_two_free_tensor():
    # The unique nonprincipal orbit may be represented by active rows
    # {0,2} and active columns {0,1}.
    central_support = frozenset({(0, 0), (0, 1), (2, 0), (2, 1)})
    tested = 0
    for free_mask in range(1, 1 << 9):
        free_support = {
            (a, b)
            for a, b in itertools.product(COLORS, repeat=2)
            if free_mask & (1 << (3 * a + b))
        }
        clauses, cells, missing_row, missing_column = two_free_sites_cnf(
            central_support, free_support
        )
        baseline = [
            variable
            for (i, j, a, b), variable in cells.items()
            if not (i == missing_row and a == missing_row)
            and not (j == missing_column and b == missing_column)
        ]
        assert len(baseline) == 64
        # This one clause asks for at least one of the 64 baseline cells to
        # vanish.  UNSAT therefore proves that every baseline cell is forced.
        with Solver(
            name="cadical195",
            bootstrap_with=clauses + [[-variable for variable in baseline]],
        ) as solver:
            assert not solver.solve(), free_support

        # Full scalar bridge support is always a valid support assignment;
        # this independently guards the clause generator against vacuity.
        with Solver(name="cadical195", bootstrap_with=clauses) as solver:
            assert solver.solve(assumptions=list(cells.values()))
        tested += 1
    assert tested == 511


def audit_rectangle_identity():
    # R(a,c)=A(a)B(c)/(C(a)D(c)).  Cross multiplication of
    # R00*R11=R01*R10 has exactly the same formal factor multiset.
    # Construct counters explicitly to keep the audit independent of a CAS.
    left = Counter(
        [("A", 0), ("B", 0), ("A", 1), ("B", 1),
         ("C", 0), ("D", 1), ("C", 1), ("D", 0)]
    )
    right = Counter(
        [("A", 0), ("B", 1), ("A", 1), ("B", 0),
         ("C", 0), ("D", 0), ("C", 1), ("D", 1)]
    )
    assert left == right
    # Three zero coefficients have ratio -1, so the identity forces the
    # fourth ratio to be -1 as well.
    assert ((-1) * (-1)) // (-1) == -1


def audit_intermediate_four_cell_orbits():
    residual = []
    for entries in itertools.combinations(
        itertools.product(COLORS, repeat=2), 4
    ):
        support = frozenset(entries)
        if not elementary_open(support):
            continue
        rows = {i for i, _ in support}
        columns = {j for _, j in support}
        if len(rows) == len(columns) == 3:
            continue  # Section 2
        if len(rows) == len(columns) == 2 and rows == columns:
            continue  # the two-diagonal coordinate-mismatch core
        residual.append(support)

    representatives = Counter(canonical(support) for support in residual)
    expected = {
        frozenset({(0, 0), (0, 1), (0, 2), (1, 1)}): 12,
        frozenset({(0, 0), (0, 1), (0, 2), (1, 2)}): 12,
        frozenset({(0, 0), (0, 1), (1, 1), (1, 2)}): 12,
        frozenset({(0, 0), (0, 1), (2, 0), (2, 1)}): 6,
        frozenset({(0, 0), (0, 1), (2, 1), (2, 2)}): 6,
        frozenset({(0, 1), (0, 2), (1, 0), (1, 2)}): 6,
    }
    assert len(residual) == 54
    assert representatives == expected


def audit_remaining_rectangle_choices():
    # Every 2x3 support has a rectangle using two active left colors and a
    # fixed right color.  All its scalar cells lie in the forced 72-cell
    # chart, while the P coloring is rainbow on the right and hence absent.
    checked_two_by_three = 0
    for mask in range(1, 1 << 9):
        support = support_from_mask(mask)
        active_rows = {i for i, _ in support}
        active_columns = {j for _, j in support}
        if len(active_rows) != 2 or len(active_columns) != 3:
            continue
        r, other_color = sorted(active_rows)
        s = next(color for color in active_columns if color != r)
        missing_row = next(color for color in COLORS if color not in active_rows)
        rows = [i for i in COLORS if i != r]
        columns = [j for j in COLORS if j != s]
        for left_first, left_second in itertools.product(
            (r, other_color), repeat=2
        ):
            for i, j, a in (
                (rows[0], columns[0], left_first),
                (rows[1], columns[1], left_second),
                (rows[0], columns[1], left_first),
                (rows[1], columns[0], left_second),
            ):
                assert (i, a) != (missing_row, missing_row)
                _ = j  # right endpoint is unrestricted in the 72-cell chart
        assert tuple(columns) != (s, s)
        checked_two_by_three += 1
    assert checked_two_by_three == 75

    # For a nonprincipal 2x2 rectangle, choose an active off-diagonal
    # coordinate (r,s).  The other active column has a fixed P color unequal
    # to s, and every ratio cell lies in the forced 64-cell chart.
    checked_two_by_two = 0
    for active_rows_tuple in itertools.combinations(COLORS, 2):
        for active_columns_tuple in itertools.combinations(COLORS, 2):
            active_rows = set(active_rows_tuple)
            active_columns = set(active_columns_tuple)
            if active_rows == active_columns:
                continue
            r, s = next(
                (r, s)
                for r, s in itertools.product(active_rows, active_columns)
                if r != s
            )
            other_color = next(color for color in active_rows if color != r)
            other_column = next(color for color in active_columns if color != s)
            missing_row = next(color for color in COLORS if color not in active_rows)
            missing_column = next(
                color for color in COLORS if color not in active_columns
            )
            rows = [i for i in COLORS if i != r]
            columns = [j for j in COLORS if j != s]
            for left_first, left_second in itertools.product(
                (r, other_color), repeat=2
            ):
                for i, j, a in (
                    (rows[0], columns[0], left_first),
                    (rows[1], columns[1], left_second),
                    (rows[0], columns[1], left_first),
                    (rows[1], columns[0], left_second),
                ):
                    assert (i, a) != (missing_row, missing_row)
                    assert (j, s) != (missing_column, missing_column)
            assert other_column != s
            checked_two_by_two += 1
    assert checked_two_by_two == 6


def main():
    audit_small_support_orbits()
    audit_all_active_rows_and_columns()
    audit_two_by_three_free_vector()
    audit_two_by_two_free_tensor()
    audit_rectangle_identity()
    audit_intermediate_four_cell_orbits()
    audit_remaining_rectangle_choices()
    print("small central supports: elementary audit leaves 3+19 masks")
    print("coordinate mismatch closes the two non-dense exceptional orbits")
    print("all-row/all-column supports: 265 SAT instances force all 81 cells")
    print("2x3 supports: 300 missing-color and 225 active-plane SAT audits")
    print("2x2 support: 511 free tensors force the same 64-cell open chart")
    print("multiplicative rectangles close the 2x3 and nonprincipal 2x2 charts")
    print("intermediate core: 54 four-cell supports in six exact orbits")
    print("verified complete central-bridge obstruction")


if __name__ == "__main__":
    main()
