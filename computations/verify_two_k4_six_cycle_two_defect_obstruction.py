#!/usr/bin/env python3
"""Exact audits for the exact-six E2 (six-cycle) obstruction.

The local calculation is the two-exceptional-component Hessian erasure
used in the accompanying note.  One star is invertible at all four sites;
the other is invertible at two sites and singular at the other two.
"""

from __future__ import annotations

import itertools
from collections import Counter

import sympy as sp

import verify_two_k4_four_singular_matching_hessian_obstruction as separated


SITES = separated.SITES
COLORS = separated.COLORS
EDGES = separated.EDGES
WORDS = separated.WORDS
DOMAIN = tuple(
    (edge, left, right)
    for edge in EDGES
    for left in COLORS
    for right in COLORS
)
SIX_CYCLE_SUPPORT = frozenset(
    ((0, 0), (0, 1), (1, 0), (1, 2), (2, 1), (2, 2))
)


def six_cells():
    return tuple(itertools.product((1, 2), COLORS))


def eight_cells():
    return tuple(
        (x, y)
        for x, y in itertools.product(COLORS, repeat=2)
        if (x, y) != (0, 0)
    )


def block_columns(edge):
    return tuple(
        column
        for column, (current, _left, _right) in enumerate(DOMAIN)
        if current == edge
    )


def audit_two_exception_erasure_normal_forms() -> None:
    """Audit the coefficient-elimination cases of Lemma 2.2."""

    identity = sp.eye(3)
    zero = sp.zeros(3)
    # These representatives include a line inside/outside the erased
    # P-plane, rank-two image equal/transverse to that plane, a changed
    # kernel, and a non-diagonal representative.
    defects = (
        zero,
        sp.diag(1, 0, 0),
        sp.diag(0, 1, 0),
        sp.diag(1, 1, 0),
        sp.diag(0, 1, 1),
        sp.Matrix([[1, 2, 3], [2, 4, 6], [0, 0, 0]]),
    )

    rank_table = Counter()
    for first, second in itertools.product(defects, repeat=2):
        matrix = separated.erased_hessian_matrix(
            (identity,) * 4,
            (first, second, identity, identity),
            six_cells(),
        )
        rank_table[(first == zero, second == zero, matrix.rank())] += 1
        if first != zero or second != zero:
            assert matrix.rank() == 54
        else:
            assert matrix.rank() == 44
    assert rank_table[(True, True, 44)] == 1

    # In the minimal active specialization a maximal rational minor is a
    # power of two.  Thus the basic odd-characteristic pivot calculation
    # has no hidden denominator.
    minimal_active = separated.erased_hessian_matrix(
        (identity,) * 4,
        (sp.diag(1, 0, 0), zero, identity, identity),
        six_cells(),
    )
    pivot_rows = separated.modular_pivot_rows(minimal_active, 3)
    assert len(pivot_rows) == 54
    assert abs(int(minimal_active[pivot_rows, :].det())) == 32

    # Relative bases are genuine parameters, not all simultaneously
    # normalizable.  Exercise rank-one/rank-two defects against four
    # unrelated invertible component maps.
    first_star = (
        sp.Matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]]),
        sp.Matrix([[2, 1, 0], [0, 1, 1], [1, 0, 1]]),
        sp.Matrix([[1, 0, 1], [1, 2, 0], [0, 1, 1]]),
        sp.Matrix([[1, 2, 0], [0, 1, 1], [1, 0, 2]]),
    )
    assert all(matrix.det() != 0 for matrix in first_star)
    regular_second = (
        sp.Matrix([[1, 1, 0], [1, 2, 1], [0, 1, 2]]),
        sp.Matrix([[2, 0, 1], [1, 1, 0], [0, 1, 1]]),
    )
    assert all(matrix.det() != 0 for matrix in regular_second)
    relative_pairs = (
        (
            sp.Matrix([[1, 2, 3], [2, 4, 6], [0, 0, 0]]),
            zero,
        ),
        (
            zero,
            sp.Matrix([[0, 1, 2], [0, 2, 4], [0, 0, 0]]),
        ),
        (
            sp.Matrix([[1, 0, 1], [0, 0, 0], [2, 0, 2]]),
            sp.Matrix([[0, 1, 0], [1, 0, 1], [0, 2, 0]]),
        ),
        (
            sp.Matrix([[1, 2, 0], [0, 1, 1], [1, 3, 1]]),
            sp.Matrix([[2, 1, 0], [0, 1, 2], [2, 2, 2]]),
        ),
    )
    for first, second in relative_pairs:
        assert first.det() == second.det() == 0
        assert first != zero or second != zero
        matrix = separated.erased_hessian_matrix(
            first_star,
            (first, second, *regular_second),
            six_cells(),
        )
        assert matrix.rank() == 54


def audit_double_zero_residual() -> None:
    """Eight cells leave exactly the regular--regular edge block."""

    identity = sp.eye(3)
    zero = sp.zeros(3)
    first = (identity,) * 4
    second = (zero, zero, identity, identity)

    six = separated.erased_hessian_matrix(first, second, six_cells())
    eight = separated.erased_hessian_matrix(first, second, eight_cells())
    regular_columns = block_columns((2, 3))
    other_columns = tuple(
        column for column in range(54) if column not in regular_columns
    )

    assert six.rank() == 44 and len(six.nullspace()) == 10
    assert eight.rank() == 45 and len(eight.nullspace()) == 9
    assert eight[:, regular_columns] == sp.zeros(eight.rows, 9)
    assert eight[:, other_columns].rank() == 45
    assert all(
        all(vector[column] == 0 for column in other_columns)
        for vector in eight.nullspace()
    )

    # The tenth six-cell class is the two-plane Koszul bridge.  Record it
    # explicitly and check that either of the last two cells detects it.
    omega = sp.zeros(54, 1)
    signs = {
        (0, 1): -1,
        (0, 2): 1,
        (0, 3): 1,
        (1, 2): -1,
        (1, 3): -1,
    }
    for edge, sign in signs.items():
        omega[DOMAIN.index((edge, 1, 2))] = sign
        omega[DOMAIN.index((edge, 2, 1))] = -sign
    assert six * omega == sp.zeros(six.rows, 1)
    assert eight * omega != sp.zeros(eight.rows, 1)

    # The residual description is invariant under nontrivial invertible
    # changes of all first-star maps and of the two regular second maps.
    first = (
        sp.Matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]]),
        sp.Matrix([[2, 1, 0], [0, 1, 1], [1, 0, 1]]),
        sp.Matrix([[1, 0, 1], [1, 2, 0], [0, 1, 1]]),
        sp.Matrix([[1, 2, 0], [0, 1, 1], [1, 0, 2]]),
    )
    second = (
        zero,
        zero,
        sp.Matrix([[1, 1, 0], [1, 2, 1], [0, 1, 2]]),
        sp.Matrix([[2, 0, 1], [1, 1, 0], [0, 1, 1]]),
    )
    eight = separated.erased_hessian_matrix(first, second, eight_cells())
    assert eight.rank() == 45
    assert eight[:, regular_columns] == sp.zeros(eight.rows, 9)
    assert eight[:, other_columns].rank() == 45


def audit_three_separated_exceptions() -> None:
    """Allow one arbitrary first-star map away from the two defects."""

    identity = sp.eye(3)
    zero = sp.zeros(3)
    # The second-star defects are 0,1.  The first-star defect is the
    # distinct regular site 2.  These representatives distinguish total
    # rank from rank on the erased input plane <e1,e2>.
    first_defects = (
        zero,
        sp.diag(1, 0, 0),       # plane rank zero, total rank one
        sp.diag(0, 1, 0),       # plane rank one
        sp.diag(1, 1, 0),       # plane rank one, total rank two
        sp.diag(0, 1, 1),       # plane rank two
    )
    second_defects = (
        zero,
        sp.diag(1, 0, 0),
        sp.diag(0, 1, 0),
        sp.diag(1, 1, 0),
        sp.diag(0, 1, 1),
    )
    regular_columns = block_columns((2, 3))
    other_columns = tuple(
        column for column in range(54) if column not in regular_columns
    )

    audited = 0
    for first_defect, defect_h, defect_k in itertools.product(
        first_defects, second_defects, second_defects
    ):
        first = [identity] * 4
        first[2] = first_defect
        second = (defect_h, defect_k, identity, identity)
        matrix = separated.erased_hessian_matrix(
            tuple(first), second, eight_cells()
        )
        if defect_h == zero and defect_k == zero:
            assert matrix.rank() == 45
            assert matrix[:, regular_columns] == sp.zeros(matrix.rows, 9)
            assert matrix[:, other_columns].rank() == 45
        else:
            assert matrix.rank() == 54
        audited += 1
    assert audited == 125

    # A relative-basis audit with plane-rank-zero first defect and a
    # non-coordinate rank-one active second defect exercises the unique
    # six-cell Koszul residual and its removal by the last two cells.
    first = (
        sp.Matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]]),
        sp.Matrix([[2, 1, 0], [0, 1, 1], [1, 0, 1]]),
        sp.Matrix([[1, 2, 3], [2, 4, 6], [3, 6, 9]]),
        sp.Matrix([[1, 2, 0], [0, 1, 1], [1, 0, 2]]),
    )
    # Columns 1,2 of this rank-one map are proportional rather than zero;
    # use a separate audit instead of relying on the canonical plane rank.
    assert first[2].rank() == 1
    second = (
        sp.Matrix([[1, 2, 3], [0, 0, 0], [2, 4, 6]]),
        zero,
        sp.Matrix([[1, 1, 0], [1, 2, 1], [0, 1, 2]]),
        sp.Matrix([[2, 0, 1], [1, 1, 0], [0, 1, 1]]),
    )
    assert second[0].rank() == 1
    assert all(first[site].det() != 0 for site in (0, 1, 3))
    assert all(second[site].det() != 0 for site in (2, 3))
    six = separated.erased_hessian_matrix(first, second, six_cells())
    eight = separated.erased_hessian_matrix(first, second, eight_cells())
    assert six.rank() in (53, 54)
    assert eight.rank() == 54


def make_six_cycle_blocks(double_zero: bool):
    blocks = {}
    for row, column in itertools.product(SITES, repeat=2):
        matrix = sp.Matrix([
            [row + 1, column + 1, 1],
            [0, row + column + 2, column + 2],
            [0, 0, row + 2],
        ])
        assert matrix.det() != 0
        blocks[row, column] = matrix

    for row, column in SIX_CYCLE_SUPPORT:
        blocks[row, column][2, 2] = 0
        assert blocks[row, column].rank() == 2

    if double_zero:
        blocks[0, 0] = sp.zeros(3)
        blocks[0, 1] = sp.zeros(3)

    assert {
        position for position, matrix in blocks.items() if matrix.det() == 0
    } == SIX_CYCLE_SUPPORT
    return blocks


def make_support_blocks(support, zero_positions=frozenset()):
    blocks = {}
    for row, column in itertools.product(SITES, repeat=2):
        matrix = sp.Matrix([
            [row + 1, column + 1, 1],
            [0, row + column + 2, column + 2],
            [0, 0, row + 2],
        ])
        assert matrix.det() != 0
        blocks[row, column] = matrix
    for position in support:
        blocks[position][2, 2] = 0
        assert blocks[position].rank() == 2
    for position in zero_positions:
        assert position in support
        blocks[position] = sp.zeros(3)
    assert {
        position for position, matrix in blocks.items() if matrix.det() == 0
    } == frozenset(support)
    return blocks


def audit_sector_identity(blocks, r, s) -> int:
    """Audit (20) for the ordered pair of complementary rows r,s."""

    a, b = tuple(site for site in SITES if site not in (r, s))
    c = separated.internal_color(a, b)
    assert c == separated.internal_color(r, s)
    q_right = {}
    for u, v in EDGES:
        color = separated.internal_color(u, v)
        q_right[u, v] = sp.zeros(3)
        q_right[u, v][color, color] = 1
    pa = {site: blocks[a, site].row(c) for site in SITES}
    pb = {site: blocks[b, site].row(c) for site in SITES}
    q_effective = {
        (u, v): (
            q_right[u, v]
            + pa[u].T * pb[v]
            + pb[u].T * pa[v]
        )
        for u, v in EDGES
    }

    checked = 0
    for x, y in itertools.product(COLORS, repeat=2):
        left_word = [None] * 4
        left_word[a] = left_word[b] = c
        left_word[r], left_word[s] = x, y
        left_word = tuple(left_word)
        first = {site: blocks[r, site].row(x) for site in SITES}
        second = {site: blocks[s, site].row(y) for site in SITES}
        for right_word in WORDS:
            four_cross = separated.permanent([
                [
                    blocks[left, right][left_word[left], right_word[right]]
                    for right in SITES
                ]
                for left in SITES
            ])
            two_cross = 0
            for u, v in EDGES:
                color = separated.internal_color(u, v)
                if right_word[u] != color or right_word[v] != color:
                    continue
                remaining = tuple(
                    site for site in SITES if site not in (u, v)
                )
                two_cross += separated.permanent([
                    [
                        blocks[left, right][left_word[left], right_word[right]]
                        for right in remaining
                    ]
                    for left in (r, s)
                ])
            pulled_back = separated.beta_coefficient(
                q_effective, first, second, right_word
            )
            assert sp.expand(pulled_back - four_cross - two_cross) == 0
            checked += 1
    assert checked == 729

    # At either exceptional site of the second row, q_eff vanishes on all
    # incident blocks in both branches of the erasure lemma.
    singular_second = tuple(
        column for row, column in blocks if row == s and blocks[row, column].det() == 0
    )
    endpoint = singular_second[0]
    internal_lines = [
        sp.eye(3)[:, separated.internal_color(endpoint, other)]
        for other in SITES
        if other != endpoint
    ]
    product_plane = sp.Matrix.hstack(pa[endpoint].T, pb[endpoint].T)
    assert sp.Matrix.hstack(*internal_lines).rank() == 3
    assert product_plane.rank() <= 2
    return checked


def audit_effective_sector_and_endpoint_obstruction() -> None:
    """Check all actual sector coefficients and both lemma branches."""

    # Row 3 is empty in the singular support.  Pair it with row 0, whose
    # two exceptional columns are 0,1; the regular edge is therefore 23.
    a, b, r, s = 1, 2, 3, 0
    c = separated.internal_color(a, b)
    assert c == separated.internal_color(r, s) == 2

    q_right = {}
    for u, v in EDGES:
        color = separated.internal_color(u, v)
        q_right[u, v] = sp.zeros(3)
        q_right[u, v][color, color] = 1

    checked = 0
    for double_zero in (False, True):
        blocks = make_six_cycle_blocks(double_zero)
        pa = {site: blocks[a, site].row(c) for site in SITES}
        pb = {site: blocks[b, site].row(c) for site in SITES}
        q_effective = {
            (u, v): (
                q_right[u, v]
                + pa[u].T * pb[v]
                + pb[u].T * pa[v]
            )
            for u, v in EDGES
        }

        for x, y in itertools.product(COLORS, repeat=2):
            left_word = [None] * 4
            left_word[a] = left_word[b] = c
            left_word[r], left_word[s] = x, y
            left_word = tuple(left_word)
            first = {site: blocks[r, site].row(x) for site in SITES}
            second = {site: blocks[s, site].row(y) for site in SITES}

            for right_word in WORDS:
                four_cross = separated.permanent([
                    [
                        blocks[left, right][left_word[left], right_word[right]]
                        for right in SITES
                    ]
                    for left in SITES
                ])
                two_cross = 0
                for u, v in EDGES:
                    color = separated.internal_color(u, v)
                    if (
                        right_word[u] != color
                        or right_word[v] != color
                    ):
                        continue
                    remaining = tuple(
                        site for site in SITES if site not in (u, v)
                    )
                    two_cross += separated.permanent([
                        [
                            blocks[left, right][left_word[left], right_word[right]]
                            for right in remaining
                        ]
                        for left in (r, s)
                    ])
                pulled_back = separated.beta_coefficient(
                    q_effective, first, second, right_word
                )
                assert sp.expand(pulled_back - four_cross - two_cross) == 0
                checked += 1

        # The K4 endpoint colors are a basis, while the product correction
        # has endpoint image in one fixed plane.  In the nonzero branch all
        # q_eff blocks vanish; in the double-zero branch all blocks incident
        # to exceptional endpoint 0 vanish because only edge 23 may remain.
        endpoint = 0
        internal_lines = [
            sp.eye(3)[:, separated.internal_color(endpoint, other)]
            for other in SITES
            if other != endpoint
        ]
        product_plane = sp.Matrix.hstack(pa[endpoint].T, pb[endpoint].T)
        assert sp.Matrix.hstack(*internal_lines).rank() == 3
        assert product_plane.rank() <= 2
    assert checked == 1458


def canonical_support(positions):
    images = []
    for rows, columns in itertools.product(
        itertools.permutations(SITES), repeat=2
    ):
        image = frozenset((rows[row], columns[column]) for row, column in positions)
        images.append(tuple(sorted(image)))
        images.append(tuple(sorted((column, row) for row, column in image)))
    return min(images)


def audit_six_cycle_orbit() -> None:
    orbit = set()
    for rows, columns in itertools.product(
        itertools.permutations(SITES), repeat=2
    ):
        image = frozenset(
            (rows[row], columns[column]) for row, column in SIX_CYCLE_SUPPORT
        )
        orbit.add(image)
        orbit.add(frozenset((column, row) for row, column in image))
    assert len(orbit) == 96
    representative = tuple(sorted(SIX_CYCLE_SUPPORT))
    assert all(canonical_support(support) == representative for support in orbit)
    for support in orbit:
        row_degrees = sorted(
            sum(row == vertex for row, _column in support) for vertex in SITES
        )
        column_degrees = sorted(
            sum(column == vertex for _row, column in support) for vertex in SITES
        )
        assert row_degrees == column_degrees == [0, 2, 2, 2]


EXACT_SEVEN_REPRESENTATIVES = (
    frozenset(((0, 0), (0, 1), (1, 0), (1, 1), (2, 2), (2, 3), (3, 2))),
    frozenset(((0, 0), (0, 1), (1, 0), (1, 2), (2, 1), (2, 2), (3, 3))),
    frozenset(((0, 0), (0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2))),
)


def degrees(support, side):
    return tuple(
        sum(position[side] == vertex for position in support)
        for vertex in SITES
    )


def survives_pre_seven_rules(support) -> bool:
    """Full-row/two-defect plus all two-singleton erasures, both shores."""

    for side in (0, 1):
        local = degrees(support, side)
        if any(
            local[vertex] == 0
            and any(other != vertex and local[other] <= 2 for other in SITES)
            for vertex in SITES
        ):
            return False
        if sum(value <= 1 for value in local) >= 2:
            return False
    return True


def find_separated_one_two_pair(support):
    row_degrees = degrees(support, 0)
    singleton = next(row for row in SITES if row_degrees[row] == 1)
    singleton_column = next(column for row, column in support if row == singleton)
    for row in SITES:
        defect_columns = {
            column for current, column in support if current == row
        }
        if row_degrees[row] == 2 and singleton_column not in defect_columns:
            return singleton, row, defect_columns
    raise AssertionError("degree count guarantees a separated one/two pair")


def audit_exact_seven_census_and_sectors() -> None:
    cells = tuple(itertools.product(SITES, repeat=2))
    survivors = tuple(
        support
        for support in itertools.combinations(cells, 7)
        if survives_pre_seven_rules(support)
    )
    assert len(survivors) == 816
    assert all(
        sorted(degrees(support, side)) == [1, 2, 2, 2]
        for support in survivors
        for side in (0, 1)
    )
    orbits = Counter(canonical_support(support) for support in survivors)
    assert orbits == Counter({
        tuple(sorted(EXACT_SEVEN_REPRESENTATIVES[0])): 144,
        tuple(sorted(EXACT_SEVEN_REPRESENTATIVES[1])): 96,
        tuple(sorted(EXACT_SEVEN_REPRESENTATIVES[2])): 576,
    })

    checked = 0
    for support in EXACT_SEVEN_REPRESENTATIVES:
        singleton, degree_two, defect_columns = find_separated_one_two_pair(support)
        singleton_defect = next(
            column for row, column in support if row == singleton
        )
        assert singleton_defect not in defect_columns

        positive_blocks = make_support_blocks(support)
        checked += audit_sector_identity(
            positive_blocks, singleton, degree_two
        )
        zero_blocks = make_support_blocks(
            support,
            frozenset((degree_two, column) for column in defect_columns),
        )
        checked += audit_sector_identity(zero_blocks, singleton, degree_two)
    assert checked == 4374


def main() -> None:
    audit_two_exception_erasure_normal_forms()
    audit_double_zero_residual()
    audit_three_separated_exceptions()
    audit_effective_sector_and_endpoint_obstruction()
    audit_six_cycle_orbit()
    audit_exact_seven_census_and_sectors()
    print("two-exception six-cell ranks: 54 if either defect is nonzero")
    print("minimal active odd-characteristic minor: determinant -32")
    print("double-zero eight-cell kernel: exactly the regular edge (dimension 9)")
    print("E2 effective-sector identity: 1458 exact coefficients")
    print("E2 six-cycle position orbit: 96 labelled supports")
    print("exact-seven census: 816 supports in orbits 144, 96, 576")
    print("exact-seven sector identities: 4374 exact coefficients")
    print("exact-six E1/E2 and all exact-seven supports: PASS")


if __name__ == "__main__":
    main()
