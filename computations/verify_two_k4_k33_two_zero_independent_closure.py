#!/usr/bin/env python3
"""Independent exact audit of the two-zero K3,3 erasure closure.

The hand proof is in
``notes/two-k4-k33-two-zero-independent-closure.md``.  This script does
not import the primary K3,3 checker.  It rebuilds the erased-Hessian map,
checks the exact single-edge kernel in both restriction branches with
unrelated regular maps, verifies the supported cubic-plane boundary, and
audits the weighted endpoint and final matching-number claims.
"""

from __future__ import annotations

import itertools

import sympy as sp
from sympy.polys.matrices import DomainMatrix

import verify_two_k4_four_singular_matching_hessian_obstruction as hessian


SITES = tuple(range(4))
COLORS = tuple(range(3))
EDGES = tuple(itertools.combinations(SITES, 2))
WORDS = tuple(itertools.product(COLORS, repeat=4))
DOMAIN = tuple(
    (edge, left, right)
    for edge in EDGES
    for left in COLORS
    for right in COLORS
)
EIGHT_CELLS = tuple(
    (x, y)
    for x, y in itertools.product(COLORS, repeat=2)
    if (x, y) != (0, 0)
)


def exact_rank(matrix: sp.Matrix) -> int:
    return DomainMatrix.from_Matrix(matrix).rank()


def edge_columns(edge: tuple[int, int]) -> tuple[int, ...]:
    return tuple(
        index
        for index, (current, _left, _right) in enumerate(DOMAIN)
        if current == edge
    )


def invertible_examples() -> tuple[sp.Matrix, ...]:
    examples = (
        sp.eye(3),
        sp.Matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]]),
        sp.Matrix([[2, 0, 1], [1, 1, 0], [0, 1, 1]]),
        sp.Matrix([[1, 2, 1], [0, 1, 1], [1, 0, 2]]),
    )
    assert all(matrix.det() != 0 for matrix in examples)
    return examples


def erased_matrix(
    first: tuple[sp.Matrix, ...],
    second: tuple[sp.Matrix, ...],
) -> sp.Matrix:
    return hessian.erased_hessian_matrix(first, second, EIGHT_CELLS)


def audit_exact_two_zero_kernel() -> int:
    """Kernel is exactly edge 23 for arbitrary tested regular charts."""

    zero = sp.zeros(3)
    regular = invertible_examples()

    # The first four maps are nonzero on K=<e1,e2>; the last three are
    # nonzero globally but vanish on K.  Both branches of the invariant
    # proof are therefore exercised.
    active = (
        sp.diag(1, 1, 0),
        sp.Matrix([[0, 1, 2], [0, 2, 4], [1, 0, 1]]),
        sp.Matrix([[1, 0, 1], [0, 1, 1], [1, 1, 2]]),
        sp.Matrix([[1, 2, 0], [0, 1, 1], [1, 3, 1]]),
        sp.Matrix([[1, 0, 0], [2, 0, 0], [3, 0, 0]]),
        sp.Matrix([[0, 0, 0], [1, 0, 0], [2, 0, 0]]),
        sp.Matrix([[1, 0, 0], [-1, 0, 0], [2, 0, 0]]),
    )
    assert all(matrix != zero and matrix.det() == 0 for matrix in active)

    survivor = edge_columns((2, 3))
    other = tuple(index for index in range(54) if index not in survivor)
    audited = 0

    for index, exceptional in enumerate(active):
        p3 = regular[index % len(regular)]
        # Keep all four maps of the regular star unrelated.  This prevents
        # the audit from silently using a simultaneous identity chart.
        second = tuple(
            regular[(index + site + 1) % len(regular)] for site in SITES
        )
        first = (zero, zero, exceptional, p3)
        matrix = erased_matrix(first, second)

        assert matrix[:, survivor] == sp.zeros(matrix.rows, 9)
        assert exact_rank(matrix[:, other]) == 45
        assert exact_rank(matrix) == 45
        nullspace = matrix.nullspace()
        assert len(nullspace) == 9
        assert all(
            all(vector[column] == 0 for column in other)
            for vector in nullspace
        )
        audited += 1

    # Permute the unique nonzero exceptional component.  Site 3 remains
    # the regular endpoint, and the survivor follows the active site.
    identity = sp.eye(3)
    sample = active[0]
    for active_site in range(3):
        maps = [zero, zero, zero, identity]
        maps[active_site] = sample
        matrix = erased_matrix(tuple(maps), (identity,) * 4)
        expected = edge_columns(tuple(sorted((active_site, 3))))
        complement = tuple(i for i in range(54) if i not in expected)
        assert matrix[:, expected] == sp.zeros(matrix.rows, 9)
        assert exact_rank(matrix[:, complement]) == 45
        audited += 1

    return audited


def cubic_plane_matrix() -> tuple[sp.Matrix, tuple[tuple[int, tuple[int, ...]], ...]]:
    """Cubic multiplication by s_e1 and s_e2 with every S_i=I."""

    domain = tuple(
        (hole, colors)
        for hole in SITES
        for colors in itertools.product(COLORS, repeat=3)
    )
    rows = []
    for y in (1, 2):
        for output in WORDS:
            row = []
            for hole, colors in domain:
                present = tuple(site for site in SITES if site != hole)
                row.append(int(
                    output[hole] == y
                    and all(
                        output[site] == colors[position]
                        for position, site in enumerate(present)
                    )
                ))
            rows.append(row)
    return sp.Matrix(rows), domain


def audit_supported_cubic_boundary() -> None:
    """A cubic containing site 3 has exactly Omega_012 tensor V3 kernel."""

    matrix, domain = cubic_plane_matrix()
    # A cubic component indexed by ``hole != 3`` contains site 3.
    supported = tuple(
        index for index, (hole, _colors) in enumerate(domain) if hole != 3
    )
    restricted = matrix[:, supported]
    assert len(supported) == 81
    assert exact_rank(restricted) == 78

    e1 = sp.eye(3)[:, 1]
    e2 = sp.eye(3)[:, 2]
    alternating = e1 * e2.T - e2 * e1.T
    blocks = {
        (0, 1): alternating,
        (0, 2): -alternating,
        (1, 2): alternating,
    }
    expected = []
    for color3 in COLORS:
        vector = sp.zeros(len(domain), 1)
        for edge, block in blocks.items():
            hole = next(site for site in (0, 1, 2) if site not in edge)
            present = tuple(site for site in SITES if site != hole)
            for left, right in itertools.product(COLORS, repeat=2):
                coefficient = block[left, right]
                if coefficient == 0:
                    continue
                output = {
                    edge[0]: left,
                    edge[1]: right,
                    3: color3,
                }
                colors = tuple(output[site] for site in present)
                vector[domain.index((hole, colors))] = coefficient
        expected.append(vector[supported, :])

    expected_matrix = sp.Matrix.hstack(*expected)
    assert expected_matrix.rank() == 3
    assert restricted * expected_matrix == sp.zeros(restricted.rows, 3)
    assert all(
        any(vector[domain.index((hole, colors))] != 0
            for colors in itertools.product(COLORS, repeat=3))
        for vector in expected
        for hole in (0, 1, 2)
    )


def internal_color(left: int, right: int) -> int:
    return (1, 2, 3).index(left ^ right)


def audit_weighted_endpoint() -> None:
    """Independent nonzero weights retain three distinct endpoint lines."""

    left_weight = sp.Symbol("lambda_ab", nonzero=True)
    right_weights = {
        other: sp.Symbol(f"rho_h{other}", nonzero=True)
        for other in (1, 2, 3)
    }
    endpoint = sp.zeros(3)
    for other in (1, 2, 3):
        color = internal_color(0, other)
        endpoint[color, color] = left_weight * right_weights[other]

    assert {internal_color(0, other) for other in (1, 2, 3)} == set(COLORS)
    assert sp.factor(endpoint.det()) == (
        left_weight**3 * sp.prod(right_weights.values())
    )

    # A product of two stars has endpoint image in their two-column span.
    u = sp.Matrix([1, 1, 0])
    v = sp.Matrix([0, 1, 1])
    assert sp.Matrix.hstack(u, v).rank() == 2
    assert sp.Matrix.hstack(u, v, *sp.eye(3).columnspace()).rank() == 3


def audit_final_cross_graph() -> None:
    """The all-zero top-left square leaves matching number exactly two."""

    graph = {
        (3, column) for column in SITES
    } | {
        (row, 3) for row in range(3)
    }
    maximum = 0
    perfect_matchings = 0
    for length in range(5):
        for chosen in itertools.combinations(graph, length):
            if (
                len({row for row, _column in chosen}) == length
                and len({column for _row, column in chosen}) == length
            ):
                maximum = max(maximum, length)
    for permutation in itertools.permutations(SITES):
        perfect_matchings += int(all(
            (row, permutation[row]) in graph for row in SITES
        ))
    assert len(graph) == 7
    assert maximum == 2
    assert perfect_matchings == 0


def main() -> None:
    audited = audit_exact_two_zero_kernel()
    audit_supported_cubic_boundary()
    audit_weighted_endpoint()
    audit_final_cross_graph()
    print(f"independent two-zero erased kernels: {audited} exact charts, nullity 9")
    print("supported cubic boundary: rank 78/81, kernel Omega_012 tensor V3")
    print("weighted endpoint lines: determinant lambda_ab^3 product(rho_hj) != 0")
    print("all-zero K3,3 cross graph: seven edges, matching number 2")
    print("independent K3,3 two-zero closure audit: PASS")


if __name__ == "__main__":
    main()
