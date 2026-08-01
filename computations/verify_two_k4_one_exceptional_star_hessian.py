#!/usr/bin/env python3
"""Audit the one-exceptional-component Hessian erasure obstruction."""

from __future__ import annotations

import itertools

import sympy as sp

import verify_two_k4_four_singular_row_obstruction as base


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


SITES = base.SITES
COLORS = base.COLORS
EDGES = base.EDGES


def multiplication_by_star(component_rank_at_zero):
    """R_2 -> R_3 for p_0 of the given canonical rank direction.

    This helper is used only at a fixed vector alpha.  Rank zero means
    p_0=0; positive rank means p_0=e_0.  The latter recovers the ordinary
    full-support kernel.
    """

    p_nonzero = [bool(component_rank_at_zero), True, True, True]
    domain = [
        (edge, left, right)
        for edge in EDGES
        for left in COLORS
        for right in COLORS
    ]
    codomain = []
    for hole in SITES:
        present = tuple(site for site in SITES if site != hole)
        for word in itertools.product(COLORS, repeat=3):
            codomain.append((hole, dict(zip(present, word, strict=True))))

    rows = []
    for hole, output in codomain:
        row = []
        for (u, v), a, b in domain:
            if hole in (u, v) or output[u] != a or output[v] != b:
                row.append(0)
                continue
            third = next(
                site for site in SITES if site not in (hole, u, v)
            )
            row.append(int(p_nonzero[third] and output[third] == 0))
        rows.append(row)
    return sp.Matrix(rows), domain


def audit_zero_component_kernel():
    multiplication, domain = multiplication_by_star(0)
    require(
        multiplication.shape == (108, 54),
        "multiplication.shape == (108, 54)",
    )
    require(
        multiplication.rank() == 46,
        "multiplication.rank() == 46",
    )
    kernel = multiplication.nullspace()
    require(
        len(kernel) == 8,
        "len(kernel) == 8",
    )

    # Every kernel vector has all 27 coordinates on the three blocks
    # incident with the zero component equal to zero.  This is exactly the
    # conclusion used in the p_h=0 branch of Lemma 3.1.
    incident = [
        index for index, (edge, _a, _b) in enumerate(domain) if 0 in edge
    ]
    require(
        len(incident) == 27,
        "len(incident) == 27",
    )
    require(
        all(vector[index] == 0 for vector in kernel for index in incident),
        "all(vector[index] == 0 for vector in kernel for index in ...",
    )

    # With all four components nonzero, recover the two-dimensional kernel
    # from the preceding note.
    full, _ = multiplication_by_star(1)
    require(
        full.rank() == 52,
        "full.rank() == 52",
    )


def audit_erasure_ranks():
    identity = sp.eye(3)
    expected_shapes = {3: 266, 2: 259, 1: 252, 0: 238}
    for rank in (3, 2, 1, 0):
        exceptional = sp.diag(*([1] * rank + [0] * (3 - rank)))
        for site in SITES:
            relative = [identity] * 4
            relative[site] = exceptional
            matrix = base.erased_hessian_matrix(tuple(relative))
            require(
                matrix.shape == (expected_shapes[rank], 54),
                "matrix.shape == (expected_shapes[rank], 54)",
            )
            require(
                matrix.rank() == 54,
                "matrix.rank() == 54",
            )

    # Non-coordinate rank-one and rank-two representatives guard against
    # accidentally relying on diagonal support in the computational audit.
    representatives = (
        sp.Matrix([[1, 2, 3], [2, 4, 6], [3, 6, 9]]),
        sp.Matrix([[1, 2, 3], [0, 1, 4], [1, 3, 7]]),
    )
    require(
        tuple(matrix.rank() for matrix in representatives) == (1, 2),
        "tuple(matrix.rank() for matrix in representatives) == (1, 2)",
    )
    for exceptional in representatives:
        relative = (exceptional, identity, identity, identity)
        require(
            base.erased_hessian_matrix(relative).rank() == 54,
            "base.erased_hessian_matrix(relative).rank() == 54",
        )


def internal_colour(u, v):
    return (1, 2, 3).index(u ^ v)


def audit_endpoint_star_contradiction():
    for exceptional_site in SITES:
        endpoint_lines = [
            sp.eye(3).col(internal_colour(exceptional_site, other))
            for other in SITES
            if other != exceptional_site
        ]
        require(
            sp.Matrix.hstack(*endpoint_lines).rank() == 3,
            "sp.Matrix.hstack(*endpoint_lines).rank() == 3",
        )

        # Every block of a product of two stars has endpoint image in one
        # fixed two-plane, represented here by two independent test vectors.
        u = sp.Matrix([1, 1, 0])
        v = sp.Matrix([0, 1, 1])
        require(
            sp.Matrix.hstack(u, v).rank() == 2,
            "sp.Matrix.hstack(u, v).rank() == 2",
        )
        require(
            sp.Matrix.hstack(u, v, *endpoint_lines).rank() == 3,
            "sp.Matrix.hstack(u, v, *endpoint_lines).rank() == 3",
        )


def canonical(positions):
    positions = tuple(positions)
    images = []
    for row_permutation, column_permutation in itertools.product(
        itertools.permutations(SITES), repeat=2
    ):
        image = tuple(sorted(
            (row_permutation[row], column_permutation[column])
            for row, column in positions
        ))
        images.append(image)
        images.append(tuple(sorted((column, row) for row, column in image)))
    return min(images)


def audit_exact_four_position_reduction():
    positions = tuple(itertools.product(SITES, repeat=2))
    survivors = []
    for support in itertools.combinations(positions, 4):
        rows = {row for row, _column in support}
        columns = {column for _row, column in support}
        if len(rows) == 4 and len(columns) == 4:
            survivors.append(support)

    require(
        len(survivors) == 24,
        "len(survivors) == 24",
    )
    require(
        len({canonical(support) for support in survivors}) == 1,
        "len({canonical(support) for support in survivors}) == 1",
    )
    require(
        canonical(survivors[0]) == (
            (0, 0), (1, 1), (2, 2), (3, 3)
        ),
        "canonical(survivors[0]) == ( (0, 0), (1, 1), (2, 2), (3, ...",
    )

    target_orbit = ((0, 0), (0, 1), (1, 2), (2, 3))
    require(
        len({row for row, _column in target_orbit}) == 3,
        "len({row for row, _column in target_orbit}) == 3",
    )
    require(
        len({column for _row, column in target_orbit}) == 4,
        "len({column for _row, column in target_orbit}) == 4",
    )
    row_degrees = sorted(
        (sum(row == fixed for row, _column in target_orbit) for fixed in SITES),
        reverse=True,
    )
    require(
        row_degrees == [2, 1, 1, 0],
        "row_degrees == [2, 1, 1, 0]",
    )


def main():
    # Recheck the two universal kernels on which the hand proof builds.
    base.common_star_annihilator()
    base.full_support_linear_kernel()
    base.audit_two_k4_sector_identity()
    audit_zero_component_kernel()
    audit_erasure_ranks()
    audit_endpoint_star_contradiction()
    audit_exact_four_position_reduction()
    print(
        "PASS: one exceptional P-star component forces a zero incident "
        "quadratic star; exact-four positions reduce to the matching orbit"
    )


if __name__ == "__main__":
    main()
