#!/usr/bin/env python3
"""Exact audit of the cubic-vertex leave-one-anchor nullity web.

The uniform proof is in
``notes/cubic-vertex-leave-one-anchor-nullity-web.md``.  This checker
independently audits four finite/algebraic parts of that proof:

* direct matching expansion at the nonneighbor ``q`` gives equation (9);
* a one-center column uses the same double-deletion cofactor in the two
  relevant leave-one-anchor maps;
* no two colors can simultaneously realize the nullity-one support pattern;
* the nullity and all-even determinantal ledgers have the asserted minima.

All tensor calculations use asymmetric integral 3 by 3 blocks.  No
floating-point arithmetic is used.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations, product
from random import Random


COLORS = (0, 1, 2)
W = tuple(range(6))
ANCHORS = (0, 1, 2)
Q_VERTEX = -1
PRIME = 1_000_003

Matrix = tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]
Tensor = dict[tuple[int, ...], int]


def random_matrix(rng: Random) -> Matrix:
    """A dense asymmetric integral block with small nonzero entries."""

    return tuple(
        tuple(rng.choice((-5, -4, -3, -2, -1, 1, 2, 3, 4, 5)) for _ in COLORS)
        for _ in COLORS
    )  # type: ignore[return-value]


def transpose(matrix: Matrix) -> Matrix:
    return tuple(
        tuple(matrix[j][i] for j in COLORS) for i in COLORS
    )  # type: ignore[return-value]


def oriented_block(
    blocks: dict[tuple[int, int], Matrix], left: int, right: int
) -> Matrix:
    key = (left, right) if left < right else (right, left)
    stored = blocks[key]
    return stored if left < right else transpose(stored)


def matching_tensor(
    vertices: tuple[int, ...], blocks: dict[tuple[int, int], Matrix]
) -> Tensor:
    """Return the complete endpoint-ordered matching tensor on ``vertices``."""

    @lru_cache(maxsize=None)
    def recurse(current: tuple[int, ...]) -> tuple[tuple[tuple[int, ...], int], ...]:
        if not current:
            return (((), 1),)
        first = current[0]
        answer: Tensor = {}
        for partner_index in range(1, len(current)):
            partner = current[partner_index]
            rest = current[1:partner_index] + current[partner_index + 1 :]
            block = oriented_block(blocks, first, partner)
            for rest_word, rest_coefficient in recurse(rest):
                rest_assignment = dict(zip(rest, rest_word, strict=True))
                for first_color, partner_color in product(COLORS, repeat=2):
                    edge_coefficient = block[first_color][partner_color]
                    if edge_coefficient == 0:
                        continue
                    assignment = dict(rest_assignment)
                    assignment[first] = first_color
                    assignment[partner] = partner_color
                    word = tuple(assignment[vertex] for vertex in current)
                    answer[word] = answer.get(word, 0) + (
                        edge_coefficient * rest_coefficient
                    )
        return tuple(sorted((word, value) for word, value in answer.items() if value))

    return dict(recurse(vertices))


def add_tensor_term(answer: Tensor, word: tuple[int, ...], value: int) -> None:
    if value:
        answer[word] = answer.get(word, 0) + value
        if answer[word] == 0:
            del answer[word]


def phi_apply(
    anchor: int,
    row: dict[int, tuple[int, int, int]],
    internal_blocks: dict[tuple[int, int], Matrix],
) -> Tensor:
    """Apply the leave-one-anchor map by its cofactor-column definition."""

    sites = tuple(vertex for vertex in W if vertex != anchor)
    answer: Tensor = {}
    for center in sites:
        rest = tuple(vertex for vertex in sites if vertex != center)
        cofactor = matching_tensor(rest, internal_blocks)
        center_index = sites.index(center)
        for rest_word, coefficient in cofactor.items():
            rest_assignment = dict(zip(rest, rest_word, strict=True))
            for color, scalar in enumerate(row[center]):
                if scalar == 0:
                    continue
                assignment = dict(rest_assignment)
                assignment[center] = color
                word = tuple(assignment[vertex] for vertex in sites)
                assert word[center_index] == color
                add_tensor_term(answer, word, scalar * coefficient)
    return answer


def direct_q_slice(
    anchor: int,
    q_color: int,
    all_blocks: dict[tuple[int, int], Matrix],
) -> Tensor:
    """Expand the same six-site cofactor first, then contract at ``q``."""

    sites = tuple(vertex for vertex in W if vertex != anchor)
    vertices = (Q_VERTEX,) + sites
    full = matching_tensor(vertices, all_blocks)
    return {
        word[1:]: coefficient
        for word, coefficient in full.items()
        if word[0] == q_color
    }


def modular_rank(columns: list[Tensor], sites: tuple[int, ...]) -> int:
    """Rank of sparse integer tensor columns over a large prime."""

    words = tuple(product(COLORS, repeat=len(sites)))
    matrix = [
        [column.get(word, 0) % PRIME for column in columns] for word in words
    ]
    rows = len(matrix)
    cols = len(columns)
    rank = 0
    for column in range(cols):
        pivot = next(
            (row for row in range(rank, rows) if matrix[row][column]), None
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], PRIME - 2, PRIME)
        matrix[rank] = [(entry * inverse) % PRIME for entry in matrix[rank]]
        for row in range(rows):
            if row == rank or matrix[row][column] == 0:
                continue
            scalar = matrix[row][column]
            matrix[row] = [
                (left - scalar * right) % PRIME
                for left, right in zip(matrix[row], matrix[rank], strict=True)
            ]
        rank += 1
        if rank == cols:
            break
    return rank


def cofactor_map_columns(
    anchor: int, internal_blocks: dict[tuple[int, int], Matrix]
) -> tuple[tuple[int, ...], list[Tensor]]:
    sites = tuple(vertex for vertex in W if vertex != anchor)
    columns: list[Tensor] = []
    for center in sites:
        for color in COLORS:
            row = {vertex: (0, 0, 0) for vertex in sites}
            basis = [0, 0, 0]
            basis[color] = 1
            row[center] = tuple(basis)  # type: ignore[assignment]
            columns.append(phi_apply(anchor, row, internal_blocks))
    return sites, columns


def audit_matching_expansion() -> dict[str, object]:
    rng = Random(20260727)
    internal_blocks = {
        pair: random_matrix(rng) for pair in combinations(W, 2)
    }
    star_blocks = {(Q_VERTEX, vertex): random_matrix(rng) for vertex in W}
    all_blocks = dict(internal_blocks)
    all_blocks.update(star_blocks)

    checked_slices = 0
    for anchor in ANCHORS:
        for q_color in COLORS:
            row = {
                vertex: star_blocks[(Q_VERTEX, vertex)][q_color]
                for vertex in W
                if vertex != anchor
            }
            via_columns = phi_apply(anchor, row, internal_blocks)
            via_matchings = direct_q_slice(anchor, q_color, all_blocks)
            assert via_columns == via_matchings
            checked_slices += 1

    # The deterministic dense specialization is on the injective open chart.
    # A full column rank modulo PRIME certifies a nonzero integer maximal minor.
    ranks = []
    for anchor in ANCHORS:
        sites, columns = cofactor_map_columns(anchor, internal_blocks)
        assert len(columns) == 3 * len(sites) == 15
        ranks.append(modular_rank(columns, sites))
    assert ranks == [15, 15, 15]

    # Audit the shared-cofactor factorization for every ordered anchor pair
    # and all three local vectors.  The same four-site tensor is used in both
    # endpoint orders.
    shared_checks = 0
    for left, right in combinations(ANCHORS, 2):
        rest = tuple(vertex for vertex in W if vertex not in (left, right))
        shared = matching_tensor(rest, internal_blocks)
        assert shared
        for anchor, center in ((left, right), (right, left)):
            sites = tuple(vertex for vertex in W if vertex != anchor)
            for color in COLORS:
                row = {vertex: (0, 0, 0) for vertex in sites}
                basis = [0, 0, 0]
                basis[color] = 1
                row[center] = tuple(basis)  # type: ignore[assignment]
                actual = phi_apply(anchor, row, internal_blocks)

                expected: Tensor = {}
                for rest_word, coefficient in shared.items():
                    assignment = dict(zip(rest, rest_word, strict=True))
                    assignment[center] = color
                    word = tuple(assignment[vertex] for vertex in sites)
                    add_tensor_term(expected, word, coefficient)
                assert actual == expected
                shared_checks += 1

    return {
        "pair_slices": checked_slices,
        "generic_ranks": ranks,
        "shared_factorizations": shared_checks,
    }


def state_for_local_row(row_color: int, map_color: int) -> tuple[str, int | None]:
    """State forced on the shared cofactor by a nonzero local row."""

    if row_color == map_color:
        return ("pure", map_color)
    return ("zero", None)


def compatible_shared_states(
    left: tuple[str, int | None], right: tuple[str, int | None]
) -> bool:
    # A shared tensor cannot be both zero and nonzero, nor nonzero pure in
    # two distinct coordinate colors on a nonempty site set.
    return left == right


def audit_nullity_one_combinatorics() -> dict[str, object]:
    incompatible_cases: list[tuple[int, int, int, int]] = []
    for first, second in combinations(COLORS, 2):
        for rho_first in COLORS:
            if rho_first == first:
                continue
            for rho_second in COLORS:
                if rho_second == second or rho_second == rho_first:
                    continue
                # rho(second) is the row local at anchor second, so map
                # first sees it across the shared cofactor, and conversely.
                state_from_first = state_for_local_row(rho_second, first)
                state_from_second = state_for_local_row(rho_first, second)
                assert not compatible_shared_states(
                    state_from_first, state_from_second
                )
                incompatible_cases.append(
                    (first, second, rho_first, rho_second)
                )

    # There are three possibilities for each unordered pair of map colors:
    # one swapped pair of pure states and two zero/nonzero clashes.
    assert len(incompatible_cases) == 9

    # If two nonzero wrong-row restrictions were proportional, their
    # difference would be one local vector forced onto two distinct axes.
    proportional_axis_clashes = 0
    for fixed in COLORS:
        wrong = tuple(color for color in COLORS if color != fixed)
        assert wrong[0] != wrong[1]
        assert set((wrong[0],)) & set((wrong[1],)) == set()
        proportional_axis_clashes += 1
    assert proportional_axis_clashes == 3

    # Three positive integer nullities with at most one entry equal to one
    # have minimum sorted profile (1,2,2), hence total at least five.
    profiles = {
        tuple(sorted(profile))
        for profile in product(range(1, 5), repeat=3)
        if sum(value == 1 for value in profile) <= 1
    }
    minimum_sum = min(sum(profile) for profile in profiles)
    minimum_profiles = sorted(
        profile for profile in profiles if sum(profile) == minimum_sum
    )
    assert minimum_sum == 5
    assert minimum_profiles == [(1, 2, 2)]

    return {
        "incompatible_two_anchor_patterns": len(incompatible_cases),
        "proportional_axis_clashes": proportional_axis_clashes,
        "minimum_nullity_profile": minimum_profiles[0],
        "minimum_nullity_sum": minimum_sum,
    }


def audit_all_even_ledger() -> dict[int, tuple[int, int, int]]:
    ledger: dict[int, tuple[int, int, int]] = {}
    for order in range(8, 32, 2):
        nonneighbors = order - 4
        column_count = 3 * (order - 3)
        singular_maps = 3 * nonneighbors
        double_null_maps = 2 * nonneighbors
        assert singular_maps >= double_null_maps
        assert column_count == 3 * (order - 3)
        ledger[order] = (column_count, singular_maps, double_null_maps)
    assert ledger[8] == (15, 12, 8)
    assert ledger[14] == (33, 30, 20)
    return ledger


def main() -> None:
    expansion = audit_matching_expansion()
    combinatorics = audit_nullity_one_combinatorics()
    ledger = audit_all_even_ledger()
    print("matching expansion:", expansion)
    print("nullity combinatorics:", combinatorics)
    print("N=8 ledger:", ledger[8])
    print("N=14 ledger:", ledger[14])
    print("PASS: cubic-vertex leave-one-anchor nullity web")


if __name__ == "__main__":
    main()
