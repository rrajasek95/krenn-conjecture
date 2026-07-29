#!/usr/bin/env python3
"""Clean-room exact audit of the uniform full-nine incidence invariant.

The script does not import the primary checker.  It reconstructs matching
contractions with endpoint-ordered nonsymmetric blocks, checks the local-ideal
coverage behind the Cauchy--Binet determinant, tests non-coordinate incident
spans by an explicit adapted-coordinate filtration, exhausts the incidence
count, and audits the total-source double count and aggregate-star distinction.
"""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
from math import comb
from pathlib import Path

import sympy as sy


PRIMARY_HASHES = {
    "notes/uniform-full-nine-target-incidence-invariant.md":
        "25c73e8e8ecacdbb8156ed27a093d62e107e219fcd3451c3a45ab381649f679e",
    "computations/verify_uniform_full_nine_target_incidence_invariant.py":
        "67eccb70f90dc1c89b6eb33cf06b6c38e61224258e4d131b709cb4c3979e9a59",
}


def canonical_edge(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Enumerate matchings by pairing the largest remaining vertex."""
    if not vertices:
        return ((),)
    pivot = vertices[-1]
    result: list[tuple[tuple[int, int], ...]] = []
    for position, partner in enumerate(vertices[:-1]):
        remainder = vertices[:position] + vertices[position + 1 : -1]
        for tail in perfect_matchings(remainder):
            result.append(tuple(sorted((canonical_edge(pivot, partner),) + tail)))
    return tuple(sorted(result))


def matching_sum(
    vertices: tuple[int, ...], edge_weights: dict[tuple[int, int], sy.Rational]
) -> sy.Rational:
    return sy.expand(
        sum(
            sy.prod(edge_weights[edge] for edge in matching)
            for matching in perfect_matchings(vertices)
        )
    )


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> sy.Integer:
    return sy.Integer(sum(a * b for a, b in zip(left, right, strict=True)))


def bilinear(
    left: tuple[int, int, int],
    matrix: tuple[tuple[int, int, int], ...],
    right: tuple[int, int, int],
) -> sy.Integer:
    return sy.Integer(
        sum(left[row] * matrix[row][column] * right[column]
            for row in range(3) for column in range(3))
    )


def make_endpoint_data(
    number_sites: int, case: int
) -> tuple[
    dict[tuple[int, int], tuple[tuple[int, int, int], ...]],
    tuple[tuple[int, int, int], ...],
    tuple[tuple[tuple[int, int, int], ...], ...],
    tuple[tuple[tuple[int, int, int], ...], ...],
]:
    """Deterministic exact data with nonsymmetric and zero physical blocks."""
    blocks: dict[tuple[int, int], tuple[tuple[int, int, int], ...]] = {}
    for left, right in combinations(range(number_sites), 2):
        if (3 * left + 5 * right + case) % 11 == 0:
            matrix = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
        else:
            matrix = tuple(
                tuple(
                    ((case + 2) * (left + 1) + (right + 2) * (row + 1)
                     - (left + 3) * (column + 2) + row * column) % 13 - 6
                    for column in range(3)
                )
                for row in range(3)
            )
        blocks[(left, right)] = matrix

    covectors = tuple(
        tuple(((site + 2) * (coordinate + case + 1) + 2 * coordinate) % 9 - 4
              for coordinate in range(3))
        for site in range(number_sites)
    )
    p = tuple(
        tuple(
            tuple(((colour + 1) * (site + 2) + (coordinate + 1) * (case + 3)) % 11 - 5
                  for coordinate in range(3))
            for site in range(number_sites)
        )
        for colour in range(3)
    )
    s = tuple(
        tuple(
            tuple(((colour + 3) * (site + 1) - (coordinate + 2) * (case + 1)) % 13 - 6
                  for coordinate in range(3))
            for site in range(number_sites)
        )
        for colour in range(3)
    )
    return blocks, covectors, p, s


def audit_endpoint_ordered_scalarization(number_sites: int, case: int) -> int:
    blocks, covectors, p, s = make_endpoint_data(number_sites, case)
    assert any(
        matrix[row][column] != matrix[column][row]
        for matrix in blocks.values()
        for row in range(3)
        for column in range(3)
    )

    edge_weights: dict[tuple[int, int], sy.Rational] = {}
    for (left, right), matrix in blocks.items():
        forward = bilinear(covectors[left], matrix, covectors[right])
        transpose = tuple(tuple(matrix[column][row] for column in range(3))
                          for row in range(3))
        reverse = bilinear(covectors[right], transpose, covectors[left])
        assert forward == reverse
        edge_weights[(left, right)] = forward

    all_sites = tuple(range(number_sites))
    cofactor: dict[tuple[int, int], sy.Rational] = {}
    for left in all_sites:
        for right in all_sites:
            if left == right:
                cofactor[(left, right)] = sy.Integer(0)
            else:
                remainder = tuple(site for site in all_sites if site not in (left, right))
                cofactor[(left, right)] = matching_sum(remainder, edge_weights)
    for left, right in combinations(all_sites, 2):
        assert cofactor[(left, right)] == cofactor[(right, left)]

    p_scalar = [[dot(p[colour][site], covectors[site]) for site in all_sites]
                for colour in range(3)]
    s_scalar = [[dot(s[colour][site], covectors[site]) for site in all_sites]
                for colour in range(3)]

    # First reconstruction: expand the endpoint choices and every remaining
    # perfect matching directly.
    brute = [[sy.Integer(0) for _ in range(3)] for _ in range(3)]
    for row, column in product(range(3), repeat=2):
        for p_site in all_sites:
            for s_site in all_sites:
                if p_site == s_site:
                    continue
                remainder = tuple(
                    site for site in all_sites if site not in (p_site, s_site)
                )
                for matching in perfect_matchings(remainder):
                    brute[row][column] += (
                        p_scalar[row][p_site]
                        * s_scalar[column][s_site]
                        * sy.prod(edge_weights[edge] for edge in matching)
                    )

    # Second reconstruction: ordinary P C S^T multiplication.
    matrix_product = [[sy.Integer(0) for _ in range(3)] for _ in range(3)]
    for row, column in product(range(3), repeat=2):
        matrix_product[row][column] = sy.expand(sum(
            p_scalar[row][left] * cofactor[(left, right)] * s_scalar[column][right]
            for left in all_sites for right in all_sites
        ))
    assert brute == matrix_product

    # q q^[m-1] counts each full matching once for each of its m edges.
    q_top = matching_sum(all_sites, edge_weights)
    pointed = sy.Integer(0)
    for edge in combinations(all_sites, 2):
        remainder = tuple(site for site in all_sites if site not in edge)
        pointed += edge_weights[edge] * matching_sum(remainder, edge_weights)
    assert sy.expand(pointed - (number_sites // 2) * q_top) == 0
    return sum(matrix != ((0, 0, 0), (0, 0, 0), (0, 0, 0))
               for matrix in blocks.values())


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def audit_rank_three_determinant_identity() -> None:
    q = sy.Symbol("q")
    x = sy.symbols("x0:3")
    a = [[sy.Symbol(f"a{row}{column}") for column in range(3)] for row in range(3)]
    entries = [[(x[row] if row == column else 0) - q * a[row][column]
                for column in range(3)] for row in range(3)]
    determinant = sum(
        permutation_sign(permutation)
        * sy.prod(entries[row][permutation[row]] for row in range(3))
        for permutation in permutations(range(3))
    )
    diagonal_cofactors = [
        a[(index + 1) % 3][(index + 1) % 3]
        * a[(index + 2) % 3][(index + 2) % 3]
        - a[(index + 1) % 3][(index + 2) % 3]
        * a[(index + 2) % 3][(index + 1) % 3]
        for index in range(3)
    ]
    determinant_a = sum(
        permutation_sign(permutation)
        * sy.prod(a[row][permutation[row]] for row in range(3))
        for permutation in permutations(range(3))
    )
    displayed = x[0] * x[1] * x[2]
    displayed -= q * sum(a[index][index]
                         * sy.prod(x[other] for other in range(3) if other != index)
                         for index in range(3))
    displayed += q**2 * sum(diagonal_cofactors[index] * x[index]
                            for index in range(3))
    displayed -= q**3 * determinant_a
    assert sy.expand(determinant - displayed) == 0


def audit_cauchy_binet_local_coverage(number_sites: int) -> tuple[int, int]:
    """Check every potentially nonzero determinant term before cancellation."""
    sites = tuple(range(number_sites))
    term_count = 0
    minimum_coverage = 3
    for rows in combinations(sites, 3):
        for columns in combinations(sites, 3):
            for permutation in permutations(range(3)):
                omitted_pairs = tuple(
                    (rows[position], columns[permutation[position]])
                    for position in range(3)
                )
                if any(left == right for left, right in omitted_pairs):
                    continue  # C_uu=0.
                term_count += 1
                for site in sites:
                    coverage = sum(site not in pair for pair in omitted_pairs)
                    expected = 3 - int(site in rows) - int(site in columns)
                    assert coverage == expected
                    assert coverage >= 1
                    minimum_coverage = min(minimum_coverage, coverage)
    return term_count, minimum_coverage


def audit_zero_incident_site(number_sites: int) -> None:
    """If every q-block at one site is zero, each C-minor term vanishes."""
    sites = tuple(range(number_sites))
    for zero_site in sites:
        active_edges = {
            edge for edge in combinations(sites, 2) if zero_site not in edge
        }
        assert not any(
            all(edge in active_edges for edge in matching)
            for matching in perfect_matchings(sites)
        )
        cofactor_nonzero: dict[tuple[int, int], bool] = {}
        for left in sites:
            for right in sites:
                if left == right:
                    cofactor_nonzero[(left, right)] = False
                    continue
                remainder = tuple(site for site in sites if site not in (left, right))
                cofactor_nonzero[(left, right)] = any(
                    all(edge in active_edges for edge in matching)
                    for matching in perfect_matchings(remainder)
                )
        for rows in combinations(sites, 3):
            for columns in combinations(sites, 3):
                for permutation in permutations(range(3)):
                    assert not all(
                        cofactor_nonzero[(rows[position], columns[permutation[position]])]
                        for position in range(3)
                    )


def audit_noncoordinate_ideal_order() -> tuple[int, int, int]:
    """Compute a global J-adic order after non-coordinate basis changes."""
    matrices_and_ranks = (
        (sy.Matrix.hstack(sy.Matrix([1, 0, 0]), sy.Matrix([0, 1, 1]), sy.Matrix([0, 0, 1])), 2),
        (sy.Matrix.hstack(sy.Matrix([0, 1, 0]), sy.Matrix([1, 0, 2]), sy.Matrix([0, 0, 1])), 2),
        (sy.Matrix.hstack(sy.Matrix([0, 0, 1]), sy.Matrix([1, -1, 0]), sy.Matrix([0, 1, 0])), 2),
        (sy.Matrix.hstack(sy.Matrix([1, 1, 1]), sy.Matrix([0, 1, 0]), sy.Matrix([0, 0, 1])), 1),
        (sy.eye(3), 0),
        (sy.Matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]]), 3),
    )
    t = sy.Symbol("t")
    y = tuple(tuple(sy.Symbol(f"y{site}{coordinate}") for coordinate in range(3))
              for site in range(len(matrices_and_ranks)))
    orders: list[int] = []
    for colour in range(3):
        target = sy.eye(3)[:, colour]
        incidence_count = 0
        filtered_product = sy.Integer(1)
        for site, (basis, rank) in enumerate(matrices_and_ranks):
            assert basis.det() != 0
            coordinates = basis.inv() * target
            belongs = all(coordinates[index] == 0 for index in range(rank, 3))
            incidence_count += int(belongs)
            target_form = sum(
                coordinates[index]
                * (t * y[site][index] if index < rank else y[site][index])
                for index in range(3)
            )
            filtered_product *= target_form
        polynomial = sy.Poly(sy.expand(filtered_product), t)
        order = min(monomial[0] for monomial, coefficient in polynomial.terms()
                    if coefficient != 0)
        assert order == incidence_count
        orders.append(order)
    assert orders == [2, 2, 2]
    return tuple(orders)


def audit_incidence_sets(number_sites: int) -> tuple[int, int]:
    """Exhaust all triples of complements of size at most two."""
    sites = frozenset(range(number_sites))
    possible_missing = tuple(
        frozenset(missing)
        for size in range(3)
        for missing in combinations(sorted(sites), size)
    )
    survivors = 0
    minimum_full = number_sites
    for missing in product(possible_missing, repeat=3):
        if missing[0] & missing[1] & missing[2]:
            continue  # The union of the three D_i does not cover the boundary.
        incidence = [3 - sum(site in missing_colour for missing_colour in missing)
                     for site in sites]
        assert min(incidence) >= 1
        counts = {rank: incidence.count(rank) for rank in (1, 2, 3)}
        total = sum(number_sites - len(missing_colour) for missing_colour in missing)
        assert total == counts[1] + 2 * counts[2] + 3 * counts[3]
        assert total >= 3 * (number_sites - 2)
        assert counts[3] >= counts[1] + number_sites - 6
        minimum_full = min(minimum_full, counts[3])
        survivors += 1
    assert minimum_full == max(0, number_sites - 6)
    return survivors, minimum_full


def audit_total_source_double_count() -> int:
    """Audit (25), the directed-pair count, and its first forced threshold."""
    first_forced = None
    for number_sites in range(10, 51):
        largest_b = (6 * (number_sites - 1)) // (number_sites - 2)
        assert largest_b == 6
        directed_budget = number_sites * largest_b
        forced = comb(number_sites, 2) > directed_budget
        if forced and first_forced is None:
            first_forced = number_sites
        if number_sites >= 14:
            assert forced
        else:
            assert not forced

        # Directly sum the (t,u) ledger for every arithmetically allowed b_r.
        for deficient_count in range(number_sites):
            ledger = deficient_count * (number_sites - 2)
            if ledger <= 6 * (number_sites - 1):
                assert deficient_count <= 6
    assert first_forced == 14
    return first_forced


def audit_aggregate_star_distinction() -> tuple[int, tuple[int, int, int]]:
    """Aggregate injectivity need not make any individual block rank three."""
    blocks = (
        sy.diag(1, 0, 0),
        sy.diag(0, 1, 0),
        sy.diag(0, 0, 1),
    )
    endpoint_span = sy.Matrix.hstack(*blocks)
    aggregate_map = sy.Matrix.vstack(*(block.T for block in blocks))
    assert endpoint_span.rank() == 3
    assert aggregate_map.rank() == 3
    block_ranks = tuple(block.rank() for block in blocks)
    assert block_ranks == (1, 1, 1)
    assert all(any(all(block[row, column] == 0 for column in range(3))
                   for row in range(3)) for block in blocks)
    # The same construction can be installed independently at both endpoints
    # of a selected pair; direct-sum rank remains three at each endpoint.
    second_endpoint_map = sy.Matrix.vstack(*(block.T for block in reversed(blocks)))
    assert second_endpoint_map.rank() == 3
    return aggregate_map.rank(), block_ranks


def audit_frozen_inputs() -> None:
    root = Path(__file__).resolve().parents[1]
    for relative_path, expected in PRIMARY_HASHES.items():
        actual = sha256((root / relative_path).read_bytes()).hexdigest()
        assert actual == expected, (relative_path, expected, actual)


def main() -> None:
    audit_frozen_inputs()
    scalar_ledgers = {
        number_sites: tuple(
            audit_endpoint_ordered_scalarization(number_sites, case)
            for case in range(1, 4)
        )
        for number_sites in (4, 6)
    }
    audit_rank_three_determinant_identity()
    determinant_ledgers = {
        number_sites: audit_cauchy_binet_local_coverage(number_sites)
        for number_sites in (4, 6, 8)
    }
    for number_sites in (4, 6):
        audit_zero_incident_site(number_sites)
    ideal_orders = audit_noncoordinate_ideal_order()
    incidence_ledgers = {
        number_sites: audit_incidence_sets(number_sites)
        for number_sites in (4, 6, 8, 10)
    }
    threshold = audit_total_source_double_count()
    aggregate_rank, block_ranks = audit_aggregate_star_distinction()
    print("endpoint-ordered nonzero-block ledgers:", scalar_ledgers)
    print("Cauchy--Binet local-cover ledgers:", determinant_ledgers)
    print("non-coordinate J-orders:", ideal_orders)
    print("incidence survivors/minimum n3:", incidence_ledgers)
    print("first directed-count threshold:", threshold)
    print("aggregate rank / individual ranks:", aggregate_rank, block_ranks)
    print("uniform full-nine target-incidence independent audit: PASS")


if __name__ == "__main__":
    main()
