#!/usr/bin/env python3
"""Lightweight audit for the full missing-square cap carrier resonance.

This checks only the stated matrix identities and finite-dimensional
selection lemmas.  The displayed survivor is intentionally not asserted to
be a full-nine decorated matching source.
"""

from fractions import Fraction
from itertools import product


if not __debug__:
    raise RuntimeError("run without -O: this audit uses assertions")


MOD = 3
VECTORS2 = tuple(product(range(MOD), repeat=2))
MATRICES = tuple(product(range(MOD), repeat=4))
NONZERO_MATRICES = MATRICES[1:]
E11 = (1, 0, 0, 0)
E22 = (0, 0, 0, 1)


def add(left, right, modulus=None):
    values = tuple(x + y for x, y in zip(left, right))
    return values if modulus is None else tuple(x % modulus for x in values)


def scale(scalar, matrix, modulus=None):
    values = tuple(scalar * x for x in matrix)
    return values if modulus is None else tuple(x % modulus for x in values)


def outer(left, right, modulus=None):
    values = (
        left[0] * right[0],
        left[0] * right[1],
        left[1] * right[0],
        left[1] * right[1],
    )
    return values if modulus is None else tuple(x % modulus for x in values)


def determinant(matrix, modulus=None):
    value = matrix[0] * matrix[3] - matrix[1] * matrix[2]
    return value if modulus is None else value % modulus


def wedge(left, right, modulus=None):
    value = left[0] * right[1] - left[1] * right[0]
    return value if modulus is None else value % modulus


def dot(left, right):
    return sum(x * y for x, y in zip(left, right)) % MOD


def span(generators):
    return {
        tuple(
            sum(coeff * generator[index] for coeff, generator in zip(coeffs, generators))
            % MOD
            for index in range(4)
        )
        for coeffs in product(range(MOD), repeat=len(generators))
    }


def audit_basic_identity():
    """Check hW=-hK+((h+1)uC+hG) without division."""
    checks = 0
    samples = (
        (1, 0, 0, 1),
        (0, 1, 1, 0),
        (1, 0, 1, 1),
        (1, 1, 1, 1),
    )
    for h in (3, 4, 7):
        for scalar_u in (-2, 0, 3):
            for direct, first, reverse in product(samples, repeat=3):
                curvature = add(scale(scalar_u, direct), scale(-1, first))
                h_edge = add(
                    add(scale(scalar_u, direct), scale(h, first)),
                    scale(h, reverse),
                )
                h_nuisance = add(
                    scale((h + 1) * scalar_u, direct), scale(h, reverse)
                )
                assert h_edge == add(scale(-h, curvature), h_nuisance)
                checks += 1
    return checks


def audit_signed_selection():
    """Exhaust the line selector in dimension four over F_3."""
    checks = 0
    witnesses = 0
    for nuisance in MATRICES:
        nuisance_line = span((nuisance,))
        for curvature in NONZERO_MATRICES:
            exists = any(
                dot(functional, nuisance) == 0
                and dot(functional, curvature) != 0
                and (functional[0] != 0 or functional[3] != 0)
                for functional in MATRICES
            )
            expected = curvature not in nuisance_line
            assert exists == expected
            checks += 1
            witnesses += exists
    return checks, witnesses


def audit_general_carrier_selection():
    """Check that nonzero W,K and the diagonal target can be co-detected."""
    checks = 0
    for edge_matrix in NONZERO_MATRICES:
        for curvature in NONZERO_MATRICES:
            functional = next(
                (
                    candidate
                    for candidate in MATRICES
                    if dot(candidate, edge_matrix) != 0
                    and dot(candidate, curvature) != 0
                    and (candidate[0] != 0 or candidate[3] != 0)
                ),
                None,
            )
            assert functional is not None
            checks += 1
    return checks


def audit_target_plane():
    """Classify D <= span(C,G) for nonzero rank-at-most-one G."""
    checks = 0
    aligned = 0
    rank_one = tuple(
        matrix
        for matrix in NONZERO_MATRICES
        if determinant(matrix, MOD) == 0
    )
    for direct in NONZERO_MATRICES:
        for reverse in rank_one:
            plane = span((direct, reverse))
            actual = E11 in plane and E22 in plane
            expected = (
                direct[1] == direct[2] == 0
                and reverse[1] == reverse[2] == 0
                and len(plane) == MOD * MOD
            )
            assert actual == expected
            checks += 1
            aligned += actual
    return checks, aligned


def audit_rank_one_pencil():
    checks = 0
    transverse = 0
    rank_one_sum = 0
    for left_h, left_g, right_h, right_g in product(VECTORS2, repeat=4):
        first = outer(left_h, right_h, MOD)
        reverse = outer(left_g, right_g, MOD)
        total = add(first, reverse, MOD)
        determinant_formula = (
            wedge(left_h, left_g, MOD) * wedge(right_h, right_g, MOD)
        ) % MOD
        assert determinant(total, MOD) == determinant_formula
        if determinant_formula:
            assert first != (0, 0, 0, 0)
            assert reverse != (0, 0, 0, 0)
            transverse += 1
        elif total != (0, 0, 0, 0):
            assert determinant(total, MOD) == 0
            rank_one_sum += 1
        checks += 1
    return checks, transverse, rank_one_sum


def audit_explicit_resonance():
    first = (1, 0, 0, 0)
    reverse = (0, 0, 1, 1)
    direct = add(first, reverse)
    assert direct == (1, 0, 1, 1)
    assert determinant(first) == determinant(reverse) == 0
    assert determinant(direct) == 1

    checks = 0
    for h in (3, 4, 7):
        scalar_u = -h
        edge = add(
            add(scale(Fraction(scalar_u, h), direct), first), reverse
        )
        curvature = add(scale(scalar_u, direct), scale(-1, first))
        nuisance = add(
            scale(Fraction(h + 1, h) * scalar_u, direct), reverse
        )
        expected_curvature = (-(h + 1), 0, -h, -h)
        assert edge == (0, 0, 0, 0)
        assert curvature == nuisance == expected_curvature
        assert direct[2] == 1 and curvature[2] == -h
        assert determinant(curvature) == h * (h + 1)
        checks += 1

    # The u=0 resonance is a genuinely different, cancelling branch.
    arbitrary_invertible_direct = (1, 1, 0, 1)
    first = (1, 2, 0, 0)
    reverse = scale(-1, first)
    assert determinant(arbitrary_invertible_direct) == 1
    assert add(first, reverse) == (0, 0, 0, 0)
    assert scale(-1, first) != (0, 0, 0, 0)  # K=-H is nonzero.
    checks += 1
    return checks


def main():
    identity_checks = audit_basic_identity()
    selector_checks, selector_witnesses = audit_signed_selection()
    carrier_checks = audit_general_carrier_selection()
    target_checks, target_aligned = audit_target_plane()
    pencil_checks, transverse, rank_one_sum = audit_rank_one_pencil()
    resonance_checks = audit_explicit_resonance()
    print("full missing-square cap carrier resonance: PASS")
    print(f"scaled W=-K+Z identity checks: {identity_checks}")
    print(
        "signed line-selector checks/witnesses: "
        f"{selector_checks}/{selector_witnesses}"
    )
    print(f"general carrier co-detection checks: {carrier_checks}")
    print(f"target-plane checks/aligned: {target_checks}/{target_aligned}")
    print(
        "rank-one pencil checks/transverse/rank-one-sum: "
        f"{pencil_checks}/{transverse}/{rank_one_sum}"
    )
    print(f"explicit resonance branch checks: {resonance_checks}")


if __name__ == "__main__":
    main()
