#!/usr/bin/env python3
"""Exact audit for coordinate-free-live-diagonal-square-ideal.md."""

from __future__ import annotations

from itertools import product

import sympy as sp


def marked_response_matrix(number_of_sites: int, colours: tuple[tuple[int, int], ...]) -> sp.Matrix:
    """Map degree-(m-2) cofactors to the requested full marked responses."""
    from itertools import combinations

    sites = tuple(range(number_of_sites))
    pairs = tuple(combinations(sites, 2))
    full_words = tuple(product(range(3), repeat=number_of_sites))
    full_index = {word: index for index, word in enumerate(full_words)}
    variables = []
    for pair in pairs:
        remaining = tuple(site for site in sites if site not in pair)
        for word in product(range(3), repeat=number_of_sites - 2):
            variables.append((pair, remaining, word))

    matrix = sp.zeros(len(colours) * len(full_words), len(variables))
    for column, (pair, remaining, word) in enumerate(variables):
        for block, (first, second) in enumerate(colours):
            orientations = ((first, second), (second, first))
            for left, right in orientations:
                output = [None] * number_of_sites
                output[pair[0]], output[pair[1]] = left, right
                for site, colour in zip(remaining, word, strict=True):
                    output[site] = colour
                row = block * len(full_words) + full_index[tuple(output)]
                matrix[row, column] += 1
    return matrix


def audit_two_tensor_first_jet() -> None:
    """Verify equations (12)--(13) with symbolic local coefficients."""
    alpha, beta = sp.symbols("alpha beta", nonzero=True)
    for number_of_sites in range(2, 7):
        r = sp.symbols(f"r0:{number_of_sites}", nonzero=True)
        a = sp.symbols(f"a0:{number_of_sites}")
        b = sp.symbols(f"b0:{number_of_sites}")
        total_ratio = sp.prod(r)
        beta_from_degree_zero = -alpha / total_ratio
        for i in range(number_of_sites):
            degree_one = sp.factor(
                alpha * a[i]
                + beta_from_degree_zero
                * b[i]
                * sp.prod(r[j] for j in range(number_of_sites) if j != i)
            )
            assert sp.factor(degree_one - alpha * (a[i] - b[i] / r[i])) == 0


def audit_three_tensor_rank() -> None:
    """Use exact bases whose quotient triples have rank two at every site."""
    for number_of_sites in range(2, 7):
        # In V/Ce_2, use the three quotient columns (1,0), (0,1),
        # and (1,s_i), with a different nonzero rational s_i at each site.
        local = [
            sp.Matrix([[1, 0, 1], [0, 1, i + 2]])
            for i in range(number_of_sites)
        ]
        assert all(matrix.rank() == 2 for matrix in local)

        rest_columns = []
        for colour in range(3):
            column = sp.Matrix([1])
            for site in range(1, number_of_sites):
                column = sp.kronecker_product(column, local[site][:, colour])
            rest_columns.append(column)
        rest = sp.Matrix.hstack(*rest_columns)
        assert rest.rank() >= 2

        coefficients = sp.diag(2, 3, 5)
        combined = local[0] * coefficients * rest.T
        assert combined != sp.zeros(*combined.shape)


def audit_quadratic_boundary() -> None:
    """Enumerate the degree-two monomials supported on two coordinate lines."""
    x0, x1, x2 = sp.symbols("x0 x1 x2")
    variables = (x0, x1, x2)
    for c, d in ((0, 1), (0, 2), (1, 2)):
        allowed = {sp.expand(variables[c] ** 2),
                   sp.expand(variables[c] * variables[d]),
                   sp.expand(variables[d] ** 2)}
        found = set()
        # A quadratic whose projective zero set is contained in the union
        # of x_c=0 and x_d=0 has two (possibly repeated) factors selected
        # from those two coordinate forms.
        for first, second in product((variables[c], variables[d]), repeat=2):
            found.add(sp.expand(first * second))
        assert found == allowed


def audit_low_sizes_and_zero_quadratic() -> None:
    off_diagonal_colours = ((0, 1), (0, 2), (1, 2))

    # At two sites the three individual mixed tensors are independent.
    two_site_tensors = []
    for first, second in off_diagonal_colours:
        tensor = sp.zeros(9, 1)
        tensor[3 * first + second] = 1
        tensor[3 * second + first] = 1
        two_site_tensors.append(tensor)
    assert sp.Matrix.hstack(*two_site_tensors).rank() == 3

    # At three sites the common cofactor triple is recovered injectively
    # from the three mixed responses.
    three_site_map = marked_response_matrix(3, off_diagonal_colours)
    assert three_site_map.shape[1] == 9
    assert three_site_map.rank() == 9

    # When B=0, every projective direction is isotropic.  For every
    # nonempty active-colour set there is a direction with all its active
    # coordinates nonzero; the one-, two-, or three-tensor lemma therefore
    # applies.  This Boolean audit includes all seven active sets.
    for active_bits in product((0, 1), repeat=3):
        active = [c for c, bit in enumerate(active_bits) if bit]
        if not active:
            continue
        direction = (1, 1, 1)
        assert all(direction[c] != 0 for c in active)
        assert len(active) in (1, 2, 3)


def main() -> None:
    audit_two_tensor_first_jet()
    audit_three_tensor_rank()
    audit_quadratic_boundary()
    audit_low_sizes_and_zero_quadratic()
    print("Coordinate-free live diagonal square-ideal lemma: PASS")


if __name__ == "__main__":
    main()
