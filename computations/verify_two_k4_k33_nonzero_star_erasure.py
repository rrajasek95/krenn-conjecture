#!/usr/bin/env python3
"""Exact audits for the K3,3 nonzero-star erased-Hessian lemma."""

from __future__ import annotations

import itertools
from collections import Counter

import sympy as sp
from sympy.polys.matrices import DomainMatrix

import verify_exact_eight_residual_factorization as residual
import verify_two_k4_exact_eight_checkerboard_hessian as exact_eight
import verify_two_k4_four_singular_matching_hessian_obstruction as hessian


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


SITES = tuple(range(4))
COLORS = tuple(range(3))
EDGES = tuple(itertools.combinations(SITES, 2))
DOMAIN = exact_eight.DOMAIN
EIGHT_CELLS = exact_eight.EIGHT_CELLS


def exact_rank(matrix: sp.Matrix) -> int:
    return DomainMatrix.from_Matrix(matrix).rank()


def erased_matrix(first: tuple[sp.Matrix, ...]) -> sp.Matrix:
    identity = sp.eye(3)
    return hessian.erased_hessian_matrix(
        first, (identity,) * 4, EIGHT_CELLS
    )


def plane_multiplication_matrix(
    maps: tuple[sp.Matrix, ...],
) -> sp.Matrix:
    """Matrix of q -> (q r_x) for a two-dimensional star r."""

    require(
        all(matrix.shape == (3, 2) for matrix in maps),
        "all(matrix.shape == (3, 2) for matrix in maps)",
    )
    rows = []
    for x in range(2):
        for hole in SITES:
            present = tuple(site for site in SITES if site != hole)
            for word in itertools.product(COLORS, repeat=3):
                output = dict(zip(present, word, strict=True))
                row = []
                for (u, v), left, right in DOMAIN:
                    if (
                        hole in (u, v)
                        or output[u] != left
                        or output[v] != right
                    ):
                        row.append(0)
                        continue
                    third = next(
                        site
                        for site in SITES
                        if site not in (hole, u, v)
                    )
                    row.append(maps[third][output[third], x])
                rows.append(row)
    return sp.Matrix(rows)


def fixed_star_multiplication_matrix(
    vectors: tuple[sp.Matrix, ...],
) -> sp.Matrix:
    """Matrix of q -> q a for one four-site linear element a."""

    require(
        len(vectors) == 4,
        "len(vectors) == 4",
    )
    require(
        all(vector.shape == (3, 1) for vector in vectors),
        "all(vector.shape == (3, 1) for vector in vectors)",
    )
    rows = []
    for hole in SITES:
        present = tuple(site for site in SITES if site != hole)
        for word in itertools.product(COLORS, repeat=3):
            output = dict(zip(present, word, strict=True))
            row = []
            for (u, v), left, right in DOMAIN:
                if (
                    hole in (u, v)
                    or output[u] != left
                    or output[v] != right
                ):
                    row.append(0)
                    continue
                third = next(
                    site
                    for site in present
                    if site not in (u, v)
                )
                row.append(vectors[third][output[third], 0])
            rows.append(row)
    return sp.Matrix(rows)


def generalized_determinant_vector() -> sp.Matrix:
    """The four alternating cubic cofactors for the identity star."""

    return sp.Matrix(
        [
            (-1) ** hole * sp.LeviCivita(*word)
            for hole in SITES
            for word in itertools.product(COLORS, repeat=3)
        ]
    )


def edge_columns(edge: tuple[int, int]) -> tuple[int, ...]:
    return tuple(
        column
        for column, (current, _left, _right) in enumerate(DOMAIN)
        if current == edge
    )


def audit_determinant_response_split() -> tuple[tuple[int, int], ...]:
    """Certify both branches in the repaired determinant-response proof."""

    e0, e1 = sp.eye(3)[:, 0], sp.eye(3)[:, 1]
    zero = sp.zeros(3, 1)
    determinant = generalized_determinant_vector()
    cases = (
        (e0, e0, e0, e0),
        (zero, e0, e0, e0),
    )
    ranks = []
    for case_index, first in enumerate(cases):
        second = (e1, e1, e1, e1)
        first_matrix = fixed_star_multiplication_matrix(first)
        second_matrix = fixed_star_multiplication_matrix(second)

        if case_index == 0:
            # The full nonzero fixed-star kernel is the two-dimensional
            # scalar-edge kernel: only e0 tensor e0 coordinates occur.
            nullspace = first_matrix.nullspace()
            pure_columns = {
                column
                for column, (_edge, left, right) in enumerate(DOMAIN)
                if left == right == 0
            }
            require(
                len(nullspace) == 2,
                "len(nullspace) == 2",
            )
            require(
                all(
                    all(
                        vector[column] == 0
                        for column in range(54)
                        if column not in pure_columns
                    )
                    for vector in nullspace
                ),
                "all( all( vector[column] == 0 for column in range(54) if ...",
            )
        else:
            # With a_0=0 and the other three components nonzero, the odd
            # cycle kills every q block incident with site 0.
            nullspace = first_matrix.nullspace()
            incident = {
                column
                for column, (edge, _left, _right) in enumerate(DOMAIN)
                if 0 in edge
            }
            require(
                len(nullspace) == 8,
                "len(nullspace) == 8",
            )
            require(
                all(
                    all(vector[column] == 0 for column in incident)
                    for vector in nullspace
                ),
                "all( all(vector[column] == 0 for column in incident) for ...",
            )

        system = first_matrix.col_join(second_matrix)
        target = sp.zeros(system.rows, 1)
        target[first_matrix.rows :, 0] = determinant
        rank = exact_rank(system)
        augmented_rank = exact_rank(system.row_join(target))
        require(
            augmented_rank == rank + 1,
            "augmented_rank == rank + 1",
        )
        ranks.append((rank, augmented_rank))
    return tuple(ranks)


def audit_plane_annihilator_strata() -> None:
    """The 0/1/2/3 axial-site nullities are exactly 0,1,9,27."""

    rank_one_a = sp.Matrix([[1, 0], [0, 0], [1, 0]])
    rank_one_b = sp.Matrix([[0, 1], [0, 2], [0, 0]])
    rank_two = sp.Matrix([[1, 0], [0, 1], [1, 1]])
    injective = sp.Matrix([[1, 0], [0, 1], [0, 0]])
    zero = sp.zeros(3, 2)

    nonzero_choices = (rank_one_a, rank_one_b, rank_two)
    for axial_count, expected_nullity in enumerate((0, 1, 9, 27)):
        for shift in range(6):
            maps = []
            for site in range(3):
                if site < axial_count:
                    maps.append(zero)
                else:
                    maps.append(nonzero_choices[(site + shift) % 3])
            maps.append(injective)
            matrix = plane_multiplication_matrix(tuple(maps))
            require(
                54 - exact_rank(matrix) == expected_nullity,
                "54 - exact_rank(matrix) == expected_nullity",
            )

            nullspace = matrix.nullspace()
            if axial_count == 2:
                survivor = edge_columns((2, 3))
                require(
                    all(
                        all(vector[index] == 0 for index in range(54)
                            if index not in survivor)
                        for vector in nullspace
                    ),
                    "all( all(vector[index] == 0 for index in range(54) if ind...",
                )
            if axial_count == 3:
                survivors = set(
                    edge_columns((0, 3))
                    + edge_columns((1, 3))
                    + edge_columns((2, 3))
                )
                require(
                    all(
                        all(vector[index] == 0 for index in range(54)
                            if index not in survivors)
                        for vector in nullspace
                    ),
                    "all( all(vector[index] == 0 for index in range(54) if ind...",
                )


def plane_boundary(
    maps: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    """Koszul boundary for three maps from a common two-plane."""

    u = tuple(matrix[:, 0] for matrix in maps)
    v = tuple(matrix[:, 1] for matrix in maps)
    return (
        u[0] * v[1].T - v[0] * u[1].T,
        -u[0] * v[2].T + v[0] * u[2].T,
        u[1] * v[2].T - v[1] * u[2].T,
    )


def audit_plane_boundary_kernels() -> None:
    """Audit the two-dimensional and exceptional four-dimensional kernels."""

    injective = sp.Matrix([[1, 0], [0, 1], [0, 0]])
    rank_one_u = sp.Matrix([[1, 0], [0, 0], [0, 0]])
    rank_one_v = sp.Matrix([[0, 1], [0, 0], [0, 0]])
    rank_two = sp.Matrix([[1, 0], [0, 1], [1, 1]])

    generic_cases = (
        (rank_one_u, rank_one_v, injective),
        (rank_one_u, rank_two, injective),
        (rank_two, rank_one_v, injective),
        (rank_two, rank_two, injective),
    )
    for maps in generic_cases:
        omega = plane_boundary(maps)
        matrix = residual.multiplication_matrix(omega)
        expected = sp.Matrix.hstack(
            *(
                sp.Matrix.vstack(*(current[:, column] for current in maps))
                for column in range(2)
            )
        )
        require(
            matrix.rank() == 7,
            "matrix.rank() == 7",
        )
        require(
            expected.rank() == 2,
            "expected.rank() == 2",
        )
        require(
            matrix * expected == sp.zeros(27, 2),
            "matrix * expected == sp.zeros(27, 2)",
        )

    # Both rank-one maps have the same source kernel.  The boundary has no
    # 01 block and its multiplication kernel consists of a common scalar on
    # sites 0,1 plus an arbitrary vector at site 2.
    exceptional_maps = (rank_one_u, rank_one_u, injective)
    exceptional = residual.multiplication_matrix(
        plane_boundary(exceptional_maps)
    )
    require(
        exceptional.rank() == 5,
        "exceptional.rank() == 5",
    )
    expected = sp.Matrix.hstack(
        sp.Matrix.vstack(
            rank_one_u[:, 0], rank_one_u[:, 0], injective[:, 0]
        ),
        *(
            sp.Matrix.vstack(sp.zeros(3, 1), sp.zeros(3, 1), sp.eye(3)[:, i])
            for i in range(3)
        ),
    )
    require(
        expected.rank() == 4,
        "expected.rank() == 4",
    )
    require(
        exceptional * expected == sp.zeros(27, 4),
        "exceptional * expected == sp.zeros(27, 4)",
    )


def cubic_plane_annihilator_matrix() -> tuple[sp.Matrix, list[tuple[int, tuple[int, ...]]]]:
    """Multiplication of a four-site cubic by the diagonal plane <e1,e2>."""

    domain = [
        (hole, colors)
        for hole in SITES
        for colors in itertools.product(COLORS, repeat=3)
    ]
    rows = []
    for y in (1, 2):
        for output in itertools.product(COLORS, repeat=4):
            row = []
            for hole, colors in domain:
                present = tuple(site for site in SITES if site != hole)
                row.append(
                    int(
                        all(output[site] == colors[index]
                            for index, site in enumerate(present))
                        and output[hole] == y
                    )
                )
            rows.append(row)
    return sp.Matrix(rows), domain


def audit_supported_cubic_annihilator() -> None:
    """If the hole-3 component is zero, the kernel is Omega_L tensor V3."""

    matrix, domain = cubic_plane_annihilator_matrix()
    columns = tuple(
        index for index, (hole, _colors) in enumerate(domain) if hole != 3
    )
    restricted = matrix[:, columns]
    require(
        len(columns) - restricted.rank() == 3,
        "len(columns) - restricted.rank() == 3",
    )

    e1, e2 = sp.eye(3)[:, 1], sp.eye(3)[:, 2]
    alternating = e1 * e2.T - e2 * e1.T
    omega = (alternating, -alternating, alternating)
    expected = []
    for color3 in COLORS:
        vector = sp.zeros(len(domain), 1)
        for edge, block in zip(((0, 1), (0, 2), (1, 2)), omega, strict=True):
            missing = next(site for site in (0, 1, 2) if site not in edge)
            hole = missing
            present = tuple(site for site in SITES if site != hole)
            for left, right in itertools.product(COLORS, repeat=2):
                if not block[left, right]:
                    continue
                output = {edge[0]: left, edge[1]: right, 3: color3}
                colors = tuple(output[site] for site in present)
                vector[domain.index((hole, colors))] = block[left, right]
        expected.append(vector[columns, :])
    expected_matrix = sp.Matrix.hstack(*expected)
    require(
        expected_matrix.rank() == 3,
        "expected_matrix.rank() == 3",
    )
    require(
        restricted * expected_matrix == sp.zeros(restricted.rows, 3),
        "restricted * expected_matrix == sp.zeros(restricted.rows, 3)",
    )


def rank_one_map(image: tuple[int, int, int], source: tuple[int, int, int]) -> sp.Matrix:
    return sp.Matrix(image) * sp.Matrix([source])


def audit_full_erasure_nonzero_maps() -> int:
    """Stress unrelated K/P3 positions on a broad exact rank-one family."""

    source_lines = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 1, 0),
        (1, 0, 1),
        (0, 1, 1),
    )
    image_lines = (
        (1, 0, 0),
        (0, 1, 0),
        (1, 1, 1),
    )
    p3_cases = (
        sp.eye(3),
        sp.Matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]]),
        sp.Matrix([[2, 0, 1], [1, 1, 0], [0, 1, 1]]),
    )
    require(
        all(matrix.det() != 0 for matrix in p3_cases),
        "all(matrix.det() != 0 for matrix in p3_cases)",
    )

    audited = 0
    for index, sources in enumerate(itertools.product(source_lines, repeat=3)):
        maps = tuple(
            rank_one_map(image_lines[(index + site) % 3], sources[site])
            for site in range(3)
        )
        for p3 in p3_cases:
            require(
                exact_rank(erased_matrix(maps + (p3,))) == 54,
                "exact_rank(erased_matrix(maps + (p3,))) == 54",
            )
            audited += 1

    # Positive-rank-two and mixed-rank unrelated specializations.
    rank_two = (
        sp.diag(1, 1, 0),
        sp.Matrix([[1, 2, 0], [0, 1, 1], [1, 3, 1]]),
        sp.Matrix([[0, 1, 2], [0, 2, 4], [1, 0, 1]]),
    )
    require(
        all(matrix.rank() == 2 for matrix in rank_two),
        "all(matrix.rank() == 2 for matrix in rank_two)",
    )
    for shift in range(18):
        maps = tuple(rank_two[(shift + site) % 3] for site in range(3))
        require(
            exact_rank(erased_matrix(maps + (p3_cases[shift % 3],))) == 54,
            "exact_rank(erased_matrix(maps + (p3_cases[shift % 3],))) ...",
        )
        audited += 1
    return audited


def audit_one_zero_incidence() -> int:
    """One zero exceptional map leaves no kernel incident with that site."""

    zero = sp.zeros(3)
    identity = sp.eye(3)
    source_lines = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 1, 0),
        (1, 0, 1),
        (0, 1, 1),
    )
    image_lines = ((1, 0, 0), (0, 1, 0), (1, 1, 1))
    incident = tuple(
        column
        for column, (edge, _left, _right) in enumerate(DOMAIN)
        if 0 in edge
    )
    away = tuple(column for column in range(54) if column not in incident)
    audited = 0
    for first_source, second_source in itertools.product(source_lines, repeat=2):
        p1 = rank_one_map(image_lines[audited % 3], first_source)
        p2 = rank_one_map(image_lines[(audited + 1) % 3], second_source)
        p3 = identity if audited % 2 == 0 else sp.Matrix(
            [[1, 1, 0], [0, 1, 1], [1, 0, 1]]
        )
        matrix = erased_matrix((zero, p1, p2, p3))
        rank = exact_rank(matrix)
        require(
            rank - exact_rank(matrix[:, away]) == len(incident),
            "rank - exact_rank(matrix[:, away]) == len(incident)",
        )
        audited += 1
    return audited


def audit_two_zero_residual() -> int:
    """Two zero exceptional maps leave exactly the remaining edge to 3."""

    zero = sp.zeros(3)
    source_lines = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 1, 0),
        (1, 0, 1),
        (0, 1, 1),
    )
    image_lines = ((1, 0, 0), (0, 1, 0), (1, 1, 1))
    rank_two = (
        sp.diag(1, 1, 0),
        sp.Matrix([[1, 2, 0], [0, 1, 1], [1, 3, 1]]),
        sp.Matrix([[0, 1, 2], [0, 2, 4], [1, 0, 1]]),
    )
    p3_cases = (
        sp.eye(3),
        sp.Matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]]),
        sp.Matrix([[2, 0, 1], [1, 1, 0], [0, 1, 1]]),
    )
    survivor = set(edge_columns((2, 3)))
    audited = 0
    maps = [
        rank_one_map(image, source)
        for image, source in itertools.product(image_lines, source_lines)
    ] + list(rank_two)
    for index, p2 in enumerate(maps):
        matrix = erased_matrix((zero, zero, p2, p3_cases[index % 3]))
        nullspace = matrix.nullspace()
        require(
            len(nullspace) == 9,
            "len(nullspace) == 9",
        )
        require(
            all(
                all(vector[column] == 0 for column in range(54)
                    if column not in survivor)
                for vector in nullspace
            ),
            "all( all(vector[column] == 0 for column in range(54) if c...",
        )
        require(
            matrix[:, tuple(sorted(survivor))] == sp.zeros(
                matrix.rows, len(survivor)
            ),
            "matrix[:, tuple(sorted(survivor))] == sp.zeros( matrix.ro...",
        )
        audited += 1
    return audited


def audit_weighted_endpoint_and_exact_nine_closure() -> None:
    """Nonzero weights retain three endpoint lines; the all-zero graph is low matching."""

    lambda_left = sp.Symbol("lambda_left", nonzero=True)
    right_weights = sp.symbols("rho_0:3", nonzero=True)
    endpoint_lines = sp.diag(
        *(lambda_left * weight for weight in right_weights)
    )
    require(
        sp.factor(endpoint_lines.det()) == (
            lambda_left**3 * sp.prod(right_weights)
        ),
        "sp.factor(endpoint_lines.det()) == ( lambda_left**3 * sp....",
    )
    require(
        endpoint_lines.rank() == 3,
        "endpoint_lines.rank() == 3",
    )

    # If all nine top-left blocks are literal zero, only row or column 3
    # remains in the nonzero graph.  Its matching number is exactly two.
    graph = {
        (3, column) for column in range(4)
    } | {
        (row, 3) for row in range(3)
    }
    maximum = 0
    for length in range(5):
        for edges in itertools.combinations(graph, length):
            if (
                len({row for row, _column in edges}) == length
                and len({column for _row, column in edges}) == length
            ):
                maximum = max(maximum, length)
    require(
        maximum == 2,
        "maximum == 2",
    )


def main() -> None:
    audit_plane_annihilator_strata()
    audit_plane_boundary_kernels()
    audit_supported_cubic_annihilator()
    response_ranks = audit_determinant_response_split()
    audited = audit_full_erasure_nonzero_maps()
    one_zero = audit_one_zero_incidence()
    two_zero = audit_two_zero_residual()
    audit_weighted_endpoint_and_exact_nine_closure()
    print("K3,3 plane-star annihilators: nullities 0/1/9/27 exactly")
    print("three-site plane-boundary kernels: dimensions 2 or 4 exactly")
    print("supported cubic plane annihilator: Omega_L tensor V3, dimension 3")
    print(
        "determinant-response split: inconsistent ranks "
        + "/".join(f"{rank}->{augmented}" for rank, augmented in response_ranks)
    )
    print(f"nonzero-star unrelated-plane erasures: {audited} exact full-rank cases")
    print(f"one-zero incident-block erasures: {one_zero} exact cases")
    print(f"two-zero single-edge residuals: {two_zero} exact cases")
    print("weighted endpoint lines: rank 3; all-zero K3,3 graph: matching number 2")
    print("two-K4 K3,3 nonzero-star erasure audit: PASS")


if __name__ == "__main__":
    main()
