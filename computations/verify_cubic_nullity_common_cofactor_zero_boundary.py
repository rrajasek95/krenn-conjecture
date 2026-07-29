#!/usr/bin/env python3
"""Exact audit of the cubic two-nonneighbor common-cofactor boundary.

The proof is in
``notes/cubic-nullity-common-cofactor-zero-boundary.md``.  This checker:

* verifies the endpoint-ordered Hessian gluing identity with asymmetric
  integral blocks;
* audits the uniform scalar hafnian and double-cofactor formulas;
* constructs the dense cancellation family at several even orders and
  computes the full sparse matching tensors and exact cofactor-map ranks;
* checks that the two deletion kernels are exactly the opposite local
  three-ports; and
* verifies directly that an arbitrary asymmetric direct block is silent
  when the common complete cofactor vanishes.

No floating-point arithmetic is used.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from random import Random

import sympy as sp


COLORS = (0, 1, 2)
Matrix = tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]
Tensor = dict[tuple[int, ...], int]


ZERO: Matrix = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
E00: Matrix = ((1, 0, 0), (0, 0, 0), (0, 0, 0))
E01: Matrix = ((0, 1, 0), (0, 0, 0), (0, 0, 0))
DIRECT: Matrix = ((1, 2, 0), (0, 1, 3), (4, 0, 1))


def transpose(matrix: Matrix) -> Matrix:
    return tuple(
        tuple(matrix[j][i] for j in COLORS) for i in COLORS
    )  # type: ignore[return-value]


def scale(matrix: Matrix, scalar: int) -> Matrix:
    return tuple(
        tuple(scalar * matrix[i][j] for j in COLORS) for i in COLORS
    )  # type: ignore[return-value]


def put_oriented(
    blocks: dict[tuple[int, int], Matrix], left: int, right: int, matrix: Matrix
) -> None:
    assert left != right
    if left < right:
        blocks[(left, right)] = matrix
    else:
        blocks[(right, left)] = transpose(matrix)


def oriented(
    blocks: dict[tuple[int, int], Matrix], left: int, right: int
) -> Matrix:
    key = (left, right) if left < right else (right, left)
    matrix = blocks.get(key, ZERO)
    return matrix if left < right else transpose(matrix)


def add(answer: Tensor, word: tuple[int, ...], coefficient: int) -> None:
    if not coefficient:
        return
    answer[word] = answer.get(word, 0) + coefficient
    if answer[word] == 0:
        del answer[word]


def matching_tensor(
    vertices: tuple[int, ...], blocks: dict[tuple[int, int], Matrix]
) -> Tensor:
    """Complete endpoint-ordered matching tensor."""

    @lru_cache(maxsize=None)
    def recurse(current: tuple[int, ...]) -> tuple[tuple[tuple[int, ...], int], ...]:
        if not current:
            return (((), 1),)
        first = current[0]
        answer: Tensor = {}
        for partner_index in range(1, len(current)):
            partner = current[partner_index]
            rest = current[1:partner_index] + current[partner_index + 1 :]
            block = oriented(blocks, first, partner)
            for rest_word, rest_coefficient in recurse(rest):
                assignment = dict(zip(rest, rest_word, strict=True))
                for first_color, partner_color in product(COLORS, repeat=2):
                    edge_coefficient = block[first_color][partner_color]
                    if not edge_coefficient:
                        continue
                    full_assignment = dict(assignment)
                    full_assignment[first] = first_color
                    full_assignment[partner] = partner_color
                    word = tuple(full_assignment[vertex] for vertex in current)
                    add(answer, word, edge_coefficient * rest_coefficient)
        return tuple(sorted(answer.items()))

    return dict(recurse(vertices))


def insert_factors(
    sites: tuple[int, ...], factors: dict[int, int], rest: tuple[int, ...], word: tuple[int, ...]
) -> tuple[int, ...]:
    assignment = dict(zip(rest, word, strict=True))
    assignment.update(factors)
    return tuple(assignment[site] for site in sites)


def phi_columns(
    sites: tuple[int, ...], blocks: dict[tuple[int, int], Matrix]
) -> list[tuple[int, int, Tensor]]:
    columns: list[tuple[int, int, Tensor]] = []
    for center in sites:
        rest = tuple(site for site in sites if site != center)
        cofactor = matching_tensor(rest, blocks)
        for color in COLORS:
            column: Tensor = {}
            for word, coefficient in cofactor.items():
                full_word = insert_factors(sites, {center: color}, rest, word)
                add(column, full_word, coefficient)
            columns.append((center, color, column))
    return columns


def phi_apply(
    sites: tuple[int, ...],
    vector: dict[int, tuple[int, int, int]],
    blocks: dict[tuple[int, int], Matrix],
) -> Tensor:
    answer: Tensor = {}
    for center, color, column in phi_columns(sites, blocks):
        scalar = vector[center][color]
        for word, coefficient in column.items():
            add(answer, word, scalar * coefficient)
    return answer


def contract(
    tensor: Tensor, sites: tuple[int, ...], site: int, color: int
) -> tuple[tuple[int, ...], Tensor]:
    index = sites.index(site)
    remaining = tuple(vertex for vertex in sites if vertex != site)
    answer: Tensor = {}
    for word, coefficient in tensor.items():
        if word[index] == color:
            add(answer, word[:index] + word[index + 1 :], coefficient)
    return remaining, answer


def tensor_rank(columns: list[Tensor]) -> int:
    words = sorted({word for column in columns for word in column})
    matrix = [
        [Fraction(column.get(word, 0)) for column in columns] for word in words
    ]
    if not matrix:
        return 0
    row_count = len(matrix)
    column_count = len(columns)
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if matrix[row][column]), None
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [entry / pivot_value for entry in matrix[rank]]
        for row in range(row_count):
            if row == rank or not matrix[row][column]:
                continue
            scalar = matrix[row][column]
            matrix[row] = [
                left - scalar * right
                for left, right in zip(matrix[row], matrix[rank], strict=True)
            ]
        rank += 1
    return rank


def odd_double_factorial(value: int) -> int:
    assert value % 2 == 1 and value >= -1
    answer = 1
    while value > 0:
        answer *= value
        value -= 2
    return answer


def cancellation_blocks(r: int) -> tuple[tuple[int, ...], dict[tuple[int, int], Matrix]]:
    assert r >= 4 and r % 2 == 0
    local = tuple(range(r))
    blocks: dict[tuple[int, int], Matrix] = {}
    for left, right in combinations(local, 2):
        weight = -(r - 2) if (left, right) == (0, 1) else 1
        put_oriented(blocks, left, right, scale(E00, weight))
    return local, blocks


def expected_double_cofactor(r: int, left: int, right: int) -> int:
    if {left, right} & {0, 1}:
        return odd_double_factorial(r - 3)
    return -2 * odd_double_factorial(r - 5)


def add_marker_star(
    blocks: dict[tuple[int, int], Matrix], local: tuple[int, ...], terminal: int
) -> None:
    for vertex in local:
        # This is e_0 at the terminal and e_1 at the local endpoint.
        put_oriented(blocks, terminal, vertex, E01)


def expected_marker_column(
    local: tuple[int, ...], terminal: int, center: int, color: int
) -> Tensor:
    sites = local + (terminal,)
    answer: Tensor = {}
    if center == terminal:
        return answer
    r = len(local)
    for marker in local:
        if marker == center:
            continue
        assignment = {site: 0 for site in sites}
        assignment[center] = color
        assignment[marker] = 1
        word = tuple(assignment[site] for site in sites)
        add(answer, word, expected_double_cofactor(r, center, marker))
    return answer


def random_matrix(rng: Random) -> Matrix:
    return tuple(
        tuple(rng.randrange(-3, 4) for _ in COLORS) for _ in COLORS
    )  # type: ignore[return-value]


def audit_hessian_gluing_identity() -> int:
    """Audit (7) without using the special cancellation family."""

    rng = Random(20260727)
    local = (0, 1, 2, 3)
    terminal = 4
    sites = local + (terminal,)
    blocks: dict[tuple[int, int], Matrix] = {}
    for left, right in combinations(local, 2):
        put_oriented(blocks, left, right, random_matrix(rng))
    for vertex in local:
        put_oriented(blocks, terminal, vertex, random_matrix(rng))

    vector = {
        site: tuple(rng.randrange(-4, 5) for _ in COLORS) for site in sites
    }
    actual_full = phi_apply(sites, vector, blocks)
    common = matching_tensor(local, blocks)
    checks = 0

    for terminal_color in COLORS:
        remaining, actual = contract(
            actual_full, sites, terminal, terminal_color
        )
        assert remaining == local
        expected: Tensor = {}

        # Local-center term z_terminal tensor P.
        terminal_scalar = vector[terminal][terminal_color]
        for word, coefficient in common.items():
            add(expected, word, terminal_scalar * coefficient)

        # Complete ordered Hessian response on L.
        for center in local:
            for partner in local:
                if partner == center:
                    continue
                rest = tuple(
                    site for site in local if site not in (center, partner)
                )
                cofactor = matching_tensor(rest, blocks)
                terminal_row = oriented(blocks, terminal, partner)[terminal_color]
                for center_color, center_scalar in enumerate(vector[center]):
                    if not center_scalar:
                        continue
                    for partner_color, partner_scalar in enumerate(terminal_row):
                        if not partner_scalar:
                            continue
                        for word, coefficient in cofactor.items():
                            full_word = insert_factors(
                                local,
                                {center: center_color, partner: partner_color},
                                rest,
                                word,
                            )
                            add(
                                expected,
                                full_word,
                                center_scalar * partner_scalar * coefficient,
                            )
        assert actual == expected
        checks += len(actual) + len(expected)

    assert common
    # For P nonzero, no nonzero local terminal basis vector is killed.
    for terminal_color in COLORS:
        vector_local = {site: (0, 0, 0) for site in sites}
        basis = [0, 0, 0]
        basis[terminal_color] = 1
        vector_local[terminal] = tuple(basis)  # type: ignore[assignment]
        image = phi_apply(sites, vector_local, blocks)
        assert image
    return checks


def audit_uniform_formulas() -> dict[int, tuple[int, int]]:
    # This symbolic factorization audits the determinant for arbitrary
    # terminal_count=r-2 and nonzero d=(r-5)!!.  Hence the rank argument is
    # uniform in even r, rather than inferred from the finite ledger below.
    terminal_count, d_symbol = sp.symbols(
        "terminal_count d", integer=True, positive=True
    )
    special_value = (terminal_count - 1) * d_symbol
    ordinary_value = -2 * d_symbol
    constant_plane_determinant = sp.expand(
        special_value * ordinary_value * (terminal_count - 1)
        - 2 * terminal_count * special_value**2
    )
    assert sp.factor(constant_plane_determinant) == (
        -2
        * (terminal_count - 1) ** 2
        * (terminal_count + 1)
        * d_symbol**2
    )
    full_determinant = sp.factor(
        (-special_value)
        * (2 * d_symbol) ** (terminal_count - 1)
        * constant_plane_determinant
    )
    expected_full_determinant = (
        2**terminal_count
        * d_symbol ** (terminal_count + 2)
        * (terminal_count - 1) ** 3
        * (terminal_count + 1)
    )
    assert sp.simplify(full_determinant - expected_full_determinant) == 0

    ledger: dict[int, tuple[int, int]] = {}
    for r in range(4, 26, 2):
        all_ones = odd_double_factorial(r - 1)
        through_special = -(r - 2) * odd_double_factorial(r - 3)
        avoiding_special = all_ones - odd_double_factorial(r - 3)
        assert through_special + avoiding_special == 0

        d = odd_double_factorial(r - 5)
        determinant = (2 ** (r - 2)) * ((r - 3) ** 3) * (r - 1) * (d**r)
        assert determinant != 0
        assert all(
            expected_double_cofactor(r, left, right) != 0
            for left, right in combinations(range(r), 2)
        )
        ledger[r + 4] = (determinant, 3 * r)
    assert ledger[8] == (12, 12)
    return ledger


def audit_physical_family(r: int) -> dict[str, int]:
    local, base = cancellation_blocks(r)
    q, q_prime = r, r + 1

    common = matching_tensor(local, base)
    assert common == {}

    for left, right in combinations(local, 2):
        rest = tuple(site for site in local if site not in (left, right))
        cofactor = matching_tensor(rest, base)
        expected_word = (0,) * len(rest)
        assert cofactor == {
            expected_word: expected_double_cofactor(r, left, right)
        }

    deletion_ranks: list[int] = []
    zero_local_columns = 0
    for terminal in (q, q_prime):
        blocks = dict(base)
        add_marker_star(blocks, local, terminal)
        sites = local + (terminal,)
        tagged_columns = phi_columns(sites, blocks)
        for center, color, column in tagged_columns:
            assert column == expected_marker_column(
                local, terminal, center, color
            )
            if center == terminal:
                assert column == {}
                zero_local_columns += 1
            else:
                assert column
        rank = tensor_rank([column for _, _, column in tagged_columns])
        assert rank == 3 * r
        assert len(tagged_columns) - rank == 3
        deletion_ranks.append(rank)

    # Put both terminals into one physical complete-support array and check
    # directly that the asymmetric q-q' block contributes DIRECT tensor P=0.
    both = dict(base)
    add_marker_star(both, local, q)
    add_marker_star(both, local, q_prime)
    put_oriented(both, q, q_prime, DIRECT)
    full_sites = local + (q, q_prime)
    with_direct = matching_tensor(full_sites, both)
    without_direct_blocks = dict(both)
    put_oriented(without_direct_blocks, q, q_prime, ZERO)
    without_direct = matching_tensor(full_sites, without_direct_blocks)
    assert with_direct == without_direct
    assert with_direct
    assert oriented(both, q_prime, q) == transpose(DIRECT)

    # This is exactly the mixed tensor displayed in equation (16), not a
    # pure cubic-anchor cofactor.  The two crossing assignments contribute
    # the coefficient 2*h_vw.
    expected_full: Tensor = {}
    for left, right in combinations(local, 2):
        assignment = {site: 0 for site in full_sites}
        assignment[left] = 1
        assignment[right] = 1
        word = tuple(assignment[site] for site in full_sites)
        add(
            expected_full,
            word,
            2 * expected_double_cofactor(r, left, right),
        )
    assert with_direct == expected_full
    constant_words = {(color,) * len(full_sites) for color in COLORS}
    assert not (set(with_direct) & constant_words)

    expected_edge_count = (r + 2) * (r + 1) // 2
    actual_nonzero_blocks = sum(matrix != ZERO for matrix in both.values())
    assert actual_nonzero_blocks == expected_edge_count

    return {
        "order": r + 4,
        "common_terms": len(common),
        "double_cofactors": r * (r - 1) // 2,
        "deletion_rank": deletion_ranks[0],
        "kernel_each": 3,
        "zero_local_columns": zero_local_columns,
        "support_edges": actual_nonzero_blocks,
        "silent_full_terms": len(with_direct),
    }


def main() -> None:
    gluing_checks = audit_hessian_gluing_identity()
    ledger = audit_uniform_formulas()
    physical = [audit_physical_family(r) for r in (4, 6, 8)]
    print("asymmetric Hessian gluing tensor entries checked:", gluing_checks)
    print("uniform kernel-rank determinant factorization: symbolic PASS")
    print("all-even formula ledger N=8..28:", ledger)
    for record in physical:
        print("physical boundary:", record)
    print("PASS: cubic common-cofactor-zero boundary and sharp local kernels")


if __name__ == "__main__":
    main()
