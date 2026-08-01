#!/usr/bin/env python3
"""Exact audits for the four-singular matching Hessian obstruction."""

from __future__ import annotations

from functools import reduce
from collections import Counter
from itertools import combinations, product, permutations

import sympy as sp


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


SITES = tuple(range(4))
COLORS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))
WORDS = tuple(product(COLORS, repeat=4))


def internal_color(left: int, right: int) -> int:
    return (1, 2, 3).index(left ^ right)


def permanent(matrix: list[list[sp.Expr]]) -> sp.Expr:
    return sp.expand(sum(
        reduce(
            lambda value, row: value * matrix[row][permutation[row]],
            range(len(matrix)),
            sp.S.One,
        )
        for permutation in permutations(range(len(matrix)))
    ))


def erased_hessian_matrix(
    first_star: tuple[sp.Matrix, ...],
    second_star: tuple[sp.Matrix, ...],
    cells: tuple[tuple[int, int], ...],
) -> sp.Matrix:
    domain = [
        (edge, left, right)
        for edge in EDGES
        for left in COLORS
        for right in COLORS
    ]
    rows = []
    for x, y in cells:
        for output in WORDS:
            row = []
            for (u, v), left, right in domain:
                if output[u] != left or output[v] != right:
                    row.append(0)
                    continue
                i, j = tuple(site for site in SITES if site not in (u, v))
                row.append(
                    first_star[i][output[i], x]
                    * second_star[j][output[j], y]
                    + second_star[i][output[i], y]
                    * first_star[j][output[j], x]
                )
            if any(row):
                rows.append(row)
    return sp.Matrix(rows)


def modular_pivot_rows(matrix: sp.Matrix, prime: int) -> list[int]:
    """Return row indices independent over GF(prime)."""
    work = [[int(matrix[row, column]) % prime for row in range(matrix.rows)]
            for column in range(matrix.cols)]
    pivot_rows = []
    rank = 0
    for candidate in range(matrix.rows):
        pivot = next(
            (column for column in range(rank, matrix.cols)
             if work[column][candidate] % prime),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][candidate], -1, prime)
        work[rank] = [(entry * inverse) % prime for entry in work[rank]]
        for column in range(matrix.cols):
            if column == rank:
                continue
            coefficient = work[column][candidate] % prime
            if coefficient:
                work[column] = [
                    (entry - coefficient * base) % prime
                    for entry, base in zip(work[column], work[rank], strict=True)
                ]
        pivot_rows.append(candidate)
        rank += 1
        if rank == matrix.cols:
            break
    return pivot_rows


def audit_erasure_lemma() -> None:
    identity = sp.eye(3)
    zero = sp.zeros(3)
    six_cells = tuple((x, y) for x in (1, 2) for y in COLORS)
    eight_cells = tuple(
        (x, y) for x, y in product(COLORS, repeat=2) if (x, y) != (0, 0)
    )

    defects = (
        zero,
        sp.diag(1, 0, 0),
        sp.Matrix([[0, 1, 0], [0, 0, 0], [0, 0, 0]]),
        sp.diag(1, 1, 0),
    )
    audited = 0
    for first_defect, second_defect in product(defects, repeat=2):
        first = (identity, identity, first_defect, identity)
        second = (identity, identity, identity, second_defect)
        matrix = erased_hessian_matrix(first, second, eight_cells)
        require(
            matrix.rank() == 54,
            "matrix.rank() == 54",
        )
        audited += 1
    require(
        audited == 16,
        "audited == 16",
    )

    # In the maximally defective case the exact integer map has a
    # unimodular full-rank minor, so this specialization is full rank over
    # every field, including characteristics two and three.
    maximally_defective = erased_hessian_matrix(
        (identity, identity, zero, identity),
        (identity, identity, identity, zero),
        eight_cells,
    )
    pivot_rows = modular_pivot_rows(maximally_defective, 2)
    require(
        len(pivot_rows) == 54,
        "len(pivot_rows) == 54",
    )
    unimodular_minor = maximally_defective[pivot_rows, :]
    require(
        unimodular_minor.det() in (-1, 1),
        "unimodular_minor.det() in (-1, 1)",
    )

    # If P_r kills K=<e1,e2>, the six cells leave exactly the exterior
    # Koszul class on the other three sites.
    first = (identity, identity, sp.diag(1, 0, 0), identity)
    second = (identity, identity, identity, sp.diag(1, 1, 0))
    six_matrix = erased_hessian_matrix(first, second, six_cells)
    require(
        six_matrix.rank() == 53,
        "six_matrix.rank() == 53",
    )

    domain = [
        (edge, left, right)
        for edge in EDGES
        for left in COLORS
        for right in COLORS
    ]
    omega = sp.zeros(54, 1)
    triangle_signs = {(0, 1): -1, (0, 3): 1, (1, 3): -1}
    for edge, sign in triangle_signs.items():
        omega[domain.index((edge, 1, 2))] = sign
        omega[domain.index((edge, 2, 1))] = -sign
    require(
        six_matrix * omega == sp.zeros(six_matrix.rows, 1),
        "six_matrix * omega == sp.zeros(six_matrix.rows, 1)",
    )
    require(
        sp.Matrix.hstack(*six_matrix.nullspace()).columnspace() == [omega],
        "sp.Matrix.hstack(*six_matrix.nullspace()).columnspace() =...",
    )

    eight_matrix = erased_hessian_matrix(first, second, eight_cells)
    require(
        eight_matrix * omega != sp.zeros(eight_matrix.rows, 1),
        "eight_matrix * omega != sp.zeros(eight_matrix.rows, 1)",
    )
    require(
        eight_matrix.rank() == 54,
        "eight_matrix.rank() == 54",
    )

    # A nontrivial exact relative-basis audit, including rank-one and
    # rank-two separated defects.
    first = (
        identity,
        identity,
        sp.Matrix([[1, 2, 3], [2, 4, 6], [0, 0, 0]]),
        identity,
    )
    second = (
        sp.Matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]]),
        sp.Matrix([[2, 1, 0], [0, 1, 1], [1, 0, 1]]),
        sp.Matrix([[1, 0, 1], [1, 2, 0], [0, 1, 1]]),
        sp.Matrix([[1, 0, 0], [2, 0, 0], [3, 0, 0]]),
    )
    require(
        all(second[site].det() != 0 for site in (0, 1, 2)),
        "all(second[site].det() != 0 for site in (0, 1, 2))",
    )
    require(
        erased_hessian_matrix(first, second, eight_cells).rank() == 54,
        "erased_hessian_matrix(first, second, eight_cells).rank() ...",
    )


def make_blocks() -> dict[tuple[int, int], sp.Matrix]:
    blocks = {}
    singular = (
        sp.zeros(3),
        sp.diag(1, 0, 0),
        sp.diag(1, 1, 0),
        sp.Matrix([[1, 2, 3], [2, 4, 6], [0, 0, 0]]),
    )
    for i, j in product(SITES, repeat=2):
        if i == j:
            blocks[i, j] = singular[i]
            require(
                blocks[i, j].det() == 0,
                "blocks[i, j].det() == 0",
            )
            continue
        matrix = sp.Matrix([
            [1 + i, 1 + j, i - j],
            [j - i, 2 + i + j, 1],
            [1, i + 2, j + 3],
        ])
        while matrix.det() == 0:
            matrix[2, 2] += 1
        blocks[i, j] = matrix
        require(
            matrix.det() != 0,
            "matrix.det() != 0",
        )
    return blocks


def beta_coefficient(
    quadratic: dict[tuple[int, int], sp.Matrix],
    first: dict[int, sp.Matrix],
    second: dict[int, sp.Matrix],
    output: tuple[int, ...],
) -> sp.Expr:
    value = 0
    for u, v in EDGES:
        i, j = tuple(site for site in SITES if site not in (u, v))
        value += quadratic[u, v][output[u], output[v]] * (
            first[i][output[i]] * second[j][output[j]]
            + second[i][output[i]] * first[j][output[j]]
        )
    return sp.expand(value)


def audit_two_k4_sector_identity() -> None:
    blocks = make_blocks()
    a, b, r, s = 0, 1, 2, 3
    c = internal_color(a, b)
    require(
        c == 0 and internal_color(r, s) == c,
        "c == 0 and internal_color(r, s) == c",
    )

    q_right = {}
    for u, v in EDGES:
        colour = internal_color(u, v)
        q_right[u, v] = sp.zeros(3)
        q_right[u, v][colour, colour] = 1

    pa = {site: blocks[a, site].row(c) for site in SITES}
    pb = {site: blocks[b, site].row(c) for site in SITES}
    q_effective = {
        (u, v): q_right[u, v] + pa[u].T * pb[v] + pb[u].T * pa[v]
        for u, v in EDGES
    }

    checked = 0
    for x, y in product(COLORS, repeat=2):
        left_word = [None] * 4
        left_word[a] = left_word[b] = c
        left_word[r], left_word[s] = x, y
        left_word = tuple(left_word)
        first = {site: blocks[r, site].row(x) for site in SITES}
        second = {site: blocks[s, site].row(y) for site in SITES}

        for right_word in WORDS:
            four_cross = permanent([
                [blocks[left, right][left_word[left], right_word[right]]
                 for right in SITES]
                for left in SITES
            ])
            two_cross = 0
            for u, v in EDGES:
                colour = internal_color(u, v)
                if right_word[u] != colour or right_word[v] != colour:
                    continue
                remaining = tuple(site for site in SITES if site not in (u, v))
                two_cross += permanent([
                    [blocks[left, right][left_word[left], right_word[right]]
                     for right in remaining]
                    for left in (r, s)
                ])
            pulled_back = beta_coefficient(
                q_effective, first, second, right_word
            )
            require(
                sp.expand(pulled_back - four_cross - two_cross) == 0,
                "sp.expand(pulled_back - four_cross - two_cross) == 0",
            )
            checked += 1
    require(
        checked == 729,
        "checked == 729",
    )

    # The separated star hypotheses hold for the two complementary rows.
    require(
        blocks[r, r].det() == 0 and blocks[s, s].det() == 0,
        "blocks[r, r].det() == 0 and blocks[s, s].det() == 0",
    )
    require(
        all(blocks[r, site].det() != 0 for site in SITES if site != r),
        "all(blocks[r, site].det() != 0 for site in SITES if site ...",
    )
    require(
        all(blocks[s, site].det() != 0 for site in SITES if site != s),
        "all(blocks[s, site].det() != 0 for site in SITES if site ...",
    )

    # q_R has three independent endpoint lines, whereas the product
    # correction has an endpoint image of dimension at most two.
    for site in SITES:
        internal_lines = [
            sp.eye(3)[:, internal_color(site, other)]
            for other in SITES
            if other != site
        ]
        product_plane = sp.Matrix.hstack(pa[site].T, pb[site].T)
        require(
            sp.Matrix.hstack(*internal_lines).rank() == 3,
            "sp.Matrix.hstack(*internal_lines).rank() == 3",
        )
        require(
            product_plane.rank() <= 2,
            "product_plane.rank() <= 2",
        )


def canonical_support(positions: tuple[tuple[int, int], ...]) -> tuple[tuple[int, int], ...]:
    images = []
    for row_permutation, column_permutation in product(
        permutations(SITES), repeat=2
    ):
        image = tuple(sorted(
            (row_permutation[row], column_permutation[column])
            for row, column in positions
        ))
        images.append(image)
        images.append(tuple(sorted((column, row) for row, column in image)))
    return min(images)


def support_degrees(
    positions: tuple[tuple[int, int], ...], side: int
) -> tuple[int, ...]:
    return tuple(sum(position[side] == vertex for position in positions) for vertex in SITES)


def erased_by_known_rules(positions: tuple[tuple[int, int], ...]) -> bool:
    """One-defect and separated-defect erasure, on both shores."""
    for transpose in (False, True):
        oriented = (
            tuple((column, row) for row, column in positions)
            if transpose
            else positions
        )
        degrees = support_degrees(oriented, 0)

        # A completely invertible row paired with a row having at most one
        # singular block is excluded by one-defect six-cell erasure.
        if any(
            degrees[row] == 0
            and any(other != row and degrees[other] <= 1 for other in SITES)
            for row in SITES
        ):
            return True

        # Two singleton rows with distinct defect sites are excluded by the
        # separated-defect eight-cell lemma.
        singleton_rows = tuple(row for row in SITES if degrees[row] == 1)
        defect_column = {
            row: next(column for current, column in oriented if current == row)
            for row in singleton_rows
        }
        if any(
            defect_column[first] != defect_column[second]
            for first, second in combinations(singleton_rows, 2)
        ):
            return True
    return False


def audit_exact_five_and_six_supports() -> None:
    positions = tuple(product(SITES, repeat=2))

    exact_five = tuple(
        support for support in combinations(positions, 5)
        if not erased_by_known_rules(support)
    )
    require(
        exact_five == (),
        "exact_five == ()",
    )

    exact_six = tuple(
        support for support in combinations(positions, 6)
        if not erased_by_known_rules(support)
    )
    require(
        len(exact_six) == 256,
        "len(exact_six) == 256",
    )
    orbits = Counter(canonical_support(support) for support in exact_six)
    expected = {
        ((0, 0), (0, 1), (0, 2), (1, 3), (2, 3), (3, 3)): 16,
        ((0, 0), (0, 1), (1, 0), (1, 1), (2, 2), (2, 3)): 144,
        ((0, 0), (0, 1), (1, 0), (1, 2), (2, 1), (2, 2)): 96,
    }
    require(
        dict(orbits) == expected,
        "dict(orbits) == expected",
    )
    for representative in expected:
        require(
            tuple(sorted(support_degrees(representative, 0), reverse=True)) in (
                (3, 1, 1, 1), (2, 2, 2, 0)
            ),
            "tuple(sorted(support_degrees(representative, 0), reverse=...",
        )


def main() -> None:
    audit_erasure_lemma()
    audit_two_k4_sector_identity()
    audit_exact_five_and_six_supports()
    print("separated-defect eight-cell Hessian erasure: rank 54/54")
    print("maximal-defect integer minor: determinant -1")
    print("two-K4 effective sector identity: 729 coefficients")
    print("four-singular transversal matching obstruction: PASS")
    print("exact-five supports: 0; exact-six residual: 256 supports in 3 orbits")


if __name__ == "__main__":
    main()
