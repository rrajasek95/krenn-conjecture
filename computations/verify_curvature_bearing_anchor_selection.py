#!/usr/bin/env python3
"""Lightweight audit of curvature-bearing diagonal-anchor selection."""

from itertools import combinations, product


MOD = 3


def add_scaled(row, other, scale):
    return [(x + scale * y) % MOD for x, y in zip(row, other)]


def rref(generators, dimension):
    rows = [list(row) for row in generators if any(row)]
    pivot_row = 0
    for column in range(dimension):
        pivot = next(
            (index for index in range(pivot_row, len(rows)) if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = 1 if rows[pivot_row][column] == 1 else 2
        rows[pivot_row] = [(inverse * x) % MOD for x in rows[pivot_row]]
        for index, row in enumerate(rows):
            if index != pivot_row and row[column]:
                rows[index] = add_scaled(
                    row, rows[pivot_row], -row[column]
                )
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return tuple(tuple(row) for row in rows[:pivot_row])


def dot(left, right):
    return sum(x * y for x, y in zip(left, right)) % MOD


def span(basis, dimension):
    return {
        tuple(
            sum(coeff * basis[index][coordinate] for index, coeff in enumerate(coeffs))
            % MOD
            for coordinate in range(dimension)
        )
        for coeffs in product(range(MOD), repeat=len(basis))
    }


def audit_rank_one_update():
    checks = 0
    for entries in product(range(MOD), repeat=4):
        a, b, c, d = entries
        determinant = (a * d - b * c) % MOD
        cofactor = (d, -c % MOD, -b % MOD, a)
        assert dot(cofactor, entries) == 2 * determinant % MOD
        for left in product(range(MOD), repeat=2):
            for right in product(range(MOD), repeat=2):
                response = (
                    left[0] * right[0] % MOD,
                    left[0] * right[1] % MOD,
                    left[1] * right[0] % MOD,
                    left[1] * right[1] % MOD,
                )
                assert (response[0] * response[3] - response[1] * response[2]) % MOD == 0
                for x, scale in product(range(MOD), repeat=2):
                    matrix = tuple(
                        (x * direct + scale * star) % MOD
                        for direct, star in zip(entries, response)
                    )
                    actual = (matrix[0] * matrix[3] - matrix[1] * matrix[2]) % MOD
                    expected = (
                        x * x * determinant
                        + scale * x * dot(cofactor, response)
                    ) % MOD
                    assert actual == expected
                    checks += 1
    return checks


def audit_selection():
    cases = 0
    edge_checks = 0
    for dimension in range(1, 5):
        vectors = tuple(product(range(MOD), repeat=dimension))
        nonzero = vectors[1:]
        subspaces = {
            rref((direct, nuisance), dimension)
            for direct in nonzero
            for nuisance in vectors
        }
        subspaces = [basis for basis in subspaces if 1 <= len(basis) <= 2]
        target_masks = [
            mask
            for size in range(1, min(2, dimension) + 1)
            for mask in combinations(range(dimension), size)
        ]

        for basis in subspaces:
            subspace = span(basis, dimension)
            annihilator = [
                functional
                for functional in vectors
                if all(dot(functional, generator) == 0 for generator in basis)
            ]
            direct = basis[0]
            nuisance = basis[1] if len(basis) == 2 else (0,) * dimension

            for curvature in vectors:
                if curvature in subspace:
                    continue
                for target_mask in target_masks:
                    units = {
                        tuple(1 if coordinate == position else 0 for coordinate in range(dimension))
                        for position in target_mask
                    }
                    if units <= subspace:
                        continue
                    functional = next(
                        (
                            candidate
                            for candidate in annihilator
                            if dot(candidate, curvature)
                            and any(candidate[position] for position in target_mask)
                        ),
                        None,
                    )
                    assert functional is not None

                    # Realize K = U C - RQ and check the exact signed edge formula.
                    scalar_u = 2
                    response = tuple(
                        (scalar_u * c_entry - k_entry) % MOD
                        for c_entry, k_entry in zip(direct, curvature)
                    )
                    cap_edge = dot(
                        functional,
                        tuple((r + g) % MOD for r, g in zip(response, nuisance)),
                    )
                    assert cap_edge == -dot(functional, curvature) % MOD
                    assert any(functional[position] for position in target_mask)
                    cases += 1
                    edge_checks += 1
    return cases, edge_checks


def audit_invertible_radial_completion():
    """Audit the only rank comparison used in the radial 2x2 branch."""
    modulus = 5
    h = 3
    inverse_h = pow(h, -1, modulus)
    rank_checks = 0
    for matrix in product(range(modulus), repeat=4):
        a, b, c, d = matrix
        determinant = (a * d - b * c) % modulus
        if not determinant:
            continue
        for scalar_u in range(modulus):
            # If H=0, then RQ=-(U/h)C.  This right side must have rank <= 1.
            response = tuple(
                (-scalar_u * inverse_h * entry) % modulus for entry in matrix
            )
            response_determinant = (
                response[0] * response[3] - response[1] * response[2]
            ) % modulus
            if response_determinant == 0:
                assert scalar_u == 0
                assert response == (0, 0, 0, 0)
            rank_checks += 1

    # Once H is nonzero, one functional can detect H and a diagonal target.
    vectors = tuple(product(range(MOD), repeat=4))
    diagonal_positions = (0, 3)
    selection_checks = 0
    for edge_matrix in vectors[1:]:
        functional = next(
            (
                candidate
                for candidate in vectors
                if dot(candidate, edge_matrix)
                and (candidate[diagonal_positions[0]] or candidate[diagonal_positions[1]])
            ),
            None,
        )
        assert functional is not None
        selection_checks += 1
    return rank_checks, selection_checks


def main():
    determinant_checks = audit_rank_one_update()
    selection_cases, edge_checks = audit_selection()
    radial_rank_checks, radial_selection_checks = audit_invertible_radial_completion()
    print("curvature-bearing diagonal-anchor selection: PASS")
    print(f"rank-one-update checks: {determinant_checks}")
    print(f"simultaneous-selection cases: {selection_cases}")
    print(f"signed literal-edge checks: {edge_checks}")
    print(f"invertible radial rank checks: {radial_rank_checks}")
    print(f"radial target-selection checks: {radial_selection_checks}")


if __name__ == "__main__":
    main()
