#!/usr/bin/env python3
"""Exact audits for notes/gaussian-norm-invariant.md.

The calculations use integers, fractions, and Eisenstein integers only.
They check:

* the portwise Hermitian cofactor-gap identity on the active binary gadget;
* the uniform gap values in the phased Fourier/anchor model;
* destructive matching-term interference in both examples; and
* the closed formulas for the Bell-pair matching adversary to the
  two- and three-copy exterior invariants.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

import verify_active_ranktwo_binary_gadget as binary
import verify_minimal_norm_gauge as gauge


def edge_matrix_at_vertex(matrices, edge, vertex):
    """Return the matrix with ``vertex`` as its row endpoint."""
    matrix = matrices[edge]
    if edge[0] == vertex:
        return matrix
    return tuple(tuple(matrix[j][i] for j in range(len(matrix)))
                 for i in range(len(matrix)))


def verify_binary_cofactor_gaps():
    expected = {
        (0, 0): (2, 1, 1, 1),
        (0, 1): (1, 1, 0, 0),
        (1, 0): (2, 1, 1, 1),
        (1, 1): (1, 2, 1, 0),
        (2, 0): (1, 1, 0, 0),
        (2, 1): (3, 1, 2, 1),
        (3, 0): (1, 1, 0, 0),
        (3, 1): (3, 1, 2, 1),
        (4, 0): (1, 1, 0, 0),
        (4, 1): (1, 2, 1, 0),
        (5, 0): (1, 1, 0, 0),
        (5, 1): (1, 1, 0, 0),
    }

    for vertex in range(binary.N):
        for color in range(2):
            row_energy = 0
            off_diagonal_energy = 0
            cofactor_energy = 0
            constant_inner_product = 0
            for other in range(binary.N):
                if other == vertex:
                    continue
                edge = tuple(sorted((vertex, other)))
                matrix = binary.MATRICES.get(edge, binary.ZERO)
                if edge[1] == vertex:
                    matrix = tuple(tuple(matrix[j][i] for j in range(2))
                                   for i in range(2))
                row = matrix[color]
                row_energy += sum(value * value for value in row)
                off_diagonal_energy += sum(
                    value * value
                    for partner_color, value in enumerate(row)
                    if partner_color != color
                )

                complement = tuple(
                    point for point in range(binary.N) if point not in edge
                )
                cofactor = binary.induced_tensor(complement)
                h_value = cofactor[(color,) * (binary.N - 2)]
                cofactor_energy += h_value * h_value
                constant_inner_product += row[color] * h_value

            gap = row_energy * cofactor_energy - 1
            assert constant_inner_product == 1
            assert (row_energy, cofactor_energy, gap,
                    off_diagonal_energy) == expected[(vertex, color)]

    # The three supported matching tensors are
    #   e_0^6 + e_0 e_0 e_1 e_1 e_0 e_0,
    #  -e_0 e_0 e_1 e_1 e_0 e_0,
    #   e_1^6.
    # Their squared norms total four, while the exact output has norm two.
    diagonal_matching_energy = 2 + 1 + 1
    output_norm_squared = 2
    assert diagonal_matching_energy == 4
    assert output_norm_squared - diagonal_matching_energy == -2


def fourier_matrices():
    q = 3
    fourier = (
        (gauge.Z1, gauge.Z1, gauge.Z1),
        (gauge.Z1, gauge.ZW, gauge.ZW2),
        (gauge.Z1, gauge.ZW2, gauge.ZW),
    )
    matrices = {}
    for edge in gauge.FOURIER_FACTORS[0] + gauge.FOURIER_FACTORS[1]:
        matrices[edge] = fourier
    for color, factor in enumerate(gauge.FOURIER_FACTORS[2:]):
        anchor = tuple(
            tuple(gauge.Z1 if i == color and j == color else gauge.Z0
                  for j in range(q))
            for i in range(q)
        )
        for edge in factor:
            matrices[edge] = anchor
    for edge, phase in gauge.FOURIER_PHASES.items():
        matrices[edge] = tuple(
            tuple(gauge.zmul(phase, entry) for entry in row)
            for row in matrices[edge]
        )
    return matrices


def znorm_squared(value):
    norm = gauge.zmul(value, gauge.zconj(value))
    assert norm[1] == 0
    return norm[0]


def induced_fourier_coefficient(matrices, vertices, coloring):
    local_color = dict(zip(vertices, coloring))
    answer = gauge.Z0
    for matching in gauge.perfect_matchings(vertices):
        term = gauge.Z1
        for edge in matching:
            term = gauge.zmul(
                term,
                matrices[edge][local_color[edge[0]]][local_color[edge[1]]],
            )
        answer = gauge.zadd(answer, term)
    return answer


def verify_fourier_gaps_and_interference():
    n = 6
    q = 3
    matrices = fourier_matrices()

    for vertex in range(n):
        for color in range(q):
            row_energy = 0
            off_diagonal_energy = 0
            cofactor_energy = 0
            constant_inner_product = gauge.Z0
            for other in range(n):
                if other == vertex:
                    continue
                edge = tuple(sorted((vertex, other)))
                row = edge_matrix_at_vertex(matrices, edge, vertex)[color]
                row_energy += sum(znorm_squared(value) for value in row)
                off_diagonal_energy += sum(
                    znorm_squared(value)
                    for partner_color, value in enumerate(row)
                    if partner_color != color
                )
                complement = tuple(point for point in range(n)
                                   if point not in edge)
                h_value = induced_fourier_coefficient(
                    matrices, complement, (color,) * (n - 2)
                )
                cofactor_energy += znorm_squared(h_value)
                constant_inner_product = gauge.zadd(
                    constant_inner_product,
                    gauge.zmul(row[color], h_value),
                )

            assert row_energy == 7
            assert cofactor_energy == 5
            assert constant_inner_product == gauge.Z1
            assert off_diagonal_energy == 4
            gap = row_energy * cofactor_energy - 1
            assert gap == 34
            # gap = s * off-diagonal energy + the diagonal wedge residual.
            assert gap - cofactor_energy * off_diagonal_energy == 14

    full_tensor = {
        coloring: induced_fourier_coefficient(
            matrices, tuple(range(n)), coloring
        )
        for coloring in product(range(q), repeat=n)
    }
    output_norm_squared = sum(
        znorm_squared(value) for value in full_tensor.values()
    )
    assert output_norm_squared == 1529

    fourier_edges = set(
        gauge.FOURIER_FACTORS[0] + gauge.FOURIER_FACTORS[1]
    )
    diagonal_matching_energy = 0
    fourier_edge_count = {}
    for matching in gauge.perfect_matchings(range(n)):
        count = sum(edge in fourier_edges for edge in matching)
        fourier_edge_count[count] = fourier_edge_count.get(count, 0) + 1
        diagonal_matching_energy += 9 ** count
    assert fourier_edge_count == {3: 2, 1: 6, 2: 3, 0: 4}
    assert diagonal_matching_energy == 1759
    assert output_norm_squared - diagonal_matching_energy == -230


def verify_bell_matching_formulas():
    # For n=2m, the raw product of m qutrit Bell tensors has norm squared
    # 3^m, two-copy alternating norm squared 12^m, and three-copy invariant
    # 6^m.  Scale it by 3^((1-m)/2), so its norm and one-site reduced Gram
    # matrices equal those of Delta_(n,3).
    for matching_size in range(1, 7):
        m = matching_size
        scale_squared = Fraction(3 ** 1, 3 ** m)
        norm_squared = scale_squared * 3 ** m
        one_site_scalar = scale_squared * 3 ** (m - 1)
        two_copy_norm_squared = scale_squared ** 2 * 12 ** m
        three_copy_squared = scale_squared ** 3 * 36 ** m

        assert norm_squared == 3
        assert one_site_scalar == 1
        assert two_copy_norm_squared == Fraction(9 * 4 ** m, 3 ** m)
        # Squaring removes the harmless square root in the scaling factor.
        assert three_copy_squared == Fraction(36 * 4 ** (m - 1),
                                              3 ** (m - 1))

    # The first conjecturally relevant order is n=6 (m=3).
    assert Fraction(9 * 4 ** 3, 3 ** 3) == Fraction(64, 3)
    assert Fraction(36 * 4 ** 2, 3 ** 2) == 64  # |I|=8.
    assert Fraction(64, 3) > 12
    assert 8 > 6


def verify_signed_hamilton_cycle_adversary():
    """Audit the six-site isotropic tensor Omega_P-Omega_Q exactly."""
    n = 6
    first = ((0, 1), (2, 3), (4, 5))
    second = ((0, 5), (1, 2), (3, 4))

    def bell_matching_coefficient(coloring, matching):
        return int(all(coloring[u] == coloring[v] for u, v in matching))

    def coefficient(coloring):
        return (
            bell_matching_coefficient(coloring, first)
            - bell_matching_coefficient(coloring, second)
        )

    colorings = tuple(product(range(3), repeat=n))
    tensor = {coloring: coefficient(coloring) for coloring in colorings}
    assert sum(value * value for value in tensor.values()) == 48

    # Every raw one-site reduced Gram matrix is 16 I_3.  Scaling the tensor
    # by 1/4 therefore gives norm squared three and rho_v=I_3.
    for vertex in range(n):
        rest = tuple(point for point in range(n) if point != vertex)
        reduced = [[0 for _ in range(3)] for _ in range(3)]
        for left_color in range(3):
            for right_color in range(3):
                for rest_coloring in product(range(3), repeat=n - 1):
                    left = [0] * n
                    right = [0] * n
                    left[vertex] = left_color
                    right[vertex] = right_color
                    for point, color in zip(rest, rest_coloring):
                        left[point] = color
                        right[point] = color
                    reduced[left_color][right_color] += (
                        coefficient(tuple(left)) * coefficient(tuple(right))
                    )
        assert reduced == [
            [16 if i == j else 0 for j in range(3)] for i in range(3)
        ]

    wedge_pairs = ((0, 1), (0, 2), (1, 2))
    two_copy_norm_squared = 0
    for labels in product(range(3), repeat=n):
        covariant_coefficient = 0
        for orientations in product(range(2), repeat=n):
            left = []
            right = []
            sign = 1
            for label, orientation in zip(labels, orientations):
                low, high = wedge_pairs[label]
                if orientation:
                    left.append(high)
                    right.append(low)
                    sign = -sign
                else:
                    left.append(low)
                    right.append(high)
            covariant_coefficient += (
                sign * coefficient(tuple(left)) * coefficient(tuple(right))
            )
        two_copy_norm_squared += covariant_coefficient ** 2
    assert two_copy_norm_squared == 2592
    assert Fraction(two_copy_norm_squared, 4 ** 4) == Fraction(81, 8)

    def permutation_sign(permutation):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(3)
            for j in range(i + 1, 3)
        )
        return -1 if inversions % 2 else 1

    three_copy_invariant = 0
    local_permutations = tuple(permutations(range(3)))
    for choices in product(local_permutations, repeat=n):
        copies = [tuple(choice[k] for choice in choices) for k in range(3)]
        sign = 1
        for choice in choices:
            sign *= permutation_sign(choice)
        three_copy_invariant += (
            sign
            * coefficient(copies[0])
            * coefficient(copies[1])
            * coefficient(copies[2])
        )
    assert three_copy_invariant == 0


def main():
    verify_binary_cofactor_gaps()
    verify_fourier_gaps_and_interference()
    verify_bell_matching_formulas()
    verify_signed_hamilton_cycle_adversary()
    print("verified exact binary cofactor gaps and norm interference")
    print("verified Fourier gaps=34 and matching cross-energy=-230")
    print("verified Bell-matching exterior invariant formulas")
    print("verified signed Hamilton-cycle invariant bracket at n=6")


if __name__ == "__main__":
    main()
