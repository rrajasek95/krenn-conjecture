#!/usr/bin/env python3
"""Exact dependency-free checks for adaptive diagonal uncollision.

The accompanying note contains the uniform proofs.  This script audits the
endpoint-ordered existence construction, activity and determinant ledgers,
literal cap rows, two-jet inverse/visibility, coefficient degree bounds, and
the intrinsic collision.  Every check remains active under ``python -O``.
"""

from fractions import Fraction
from itertools import product
from math import comb


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def zeros():
    return [[Fraction(0) for _ in range(3)] for _ in range(3)]


def unit(i, j):
    result = zeros()
    result[i][j] = Fraction(1)
    return result


def matrix_add(*terms):
    return [
        [sum(scale * matrix[i][j] for scale, matrix in terms) for j in range(3)]
        for i in range(3)
    ]


def pairing(left, right):
    """The literal endpoint-ordered pairing sum L_ij A_ij."""
    return sum(left[i][j] * right[i][j] for i in range(3) for j in range(3))


def diag(matrix):
    return tuple(matrix[i][i] for i in range(3))


def det3(matrix):
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def complement(a):
    return tuple(i for i in range(3) if i != a)


def intrinsic(block, a):
    return all(
        block[i][j] == 0
        for i in range(3)
        for j in range(3)
        if (i, j) != (a, a)
    )


def scalar_zero_all_visible(block, candidate):
    """Whether a cap is scalar-zero with all three target labels visible."""
    return pairing(candidate, block) == 0 and all(
        value != 0 for value in diag(candidate)
    )


def choose_direction(block, a):
    """The division-free construction in Section 2, or None if intrinsic."""
    if intrinsic(block, a):
        return None
    b, c = complement(a)
    direction = zeros()
    direction[b][b] = Fraction(1)
    direction[c][c] = Fraction(1)
    if pairing(direction, block) != 0:
        return direction
    if block[b][b] != 0:
        direction[b][b] = Fraction(2)
        require(pairing(direction, block) != 0, "diagonal adjustment cancelled")
        return direction
    require(block[c][c] == 0, "zero initial contraction has wrong diagonal ledger")
    for i in range(3):
        for j in range(3):
            if (i, j) != (a, a) and block[i][j] != 0:
                direction[i][j] = Fraction(1)
                require(pairing(direction, block) != 0, "ordered cell was not detected")
                return direction
    raise RuntimeError("non-intrinsic block had no extra entry")


def check_existence_iff_and_ordering():
    def audit_block(block, a):
        direction = choose_direction(block, a)
        require(
            (direction is not None) == (not intrinsic(block, a)),
            "existence criterion failed",
        )
        if direction is None:
            return
        b, c = complement(a)
        require(direction[a][a] == 0, "D_aa must vanish")
        require(direction[b][b] != 0 and direction[c][c] != 0, "blind complement")
        require(pairing(direction, block) != 0, "constructed gamma vanished")
        alpha = block[a][a]
        gamma = pairing(direction, block)
        visible_cap = matrix_add(
            (gamma, unit(a, a)),
            (-alpha, direction),
        )
        require(
            scalar_zero_all_visible(block, visible_cap),
            "constructed scalar-zero cap lost a diagonal label",
        )

    # Exhaust the branch-determining complementary diagonal values and every
    # possible endpoint-ordered one-cell support.  The proof in the note
    # handles arbitrary superpositions; enumerating all 3^8 coefficient
    # patterns here would only repeat these three construction branches.
    for a in range(3):
        b, c = complement(a)
        for value_b, value_c in product(range(-2, 3), repeat=2):
            block = zeros()
            block[a][a] = Fraction(2)
            block[b][b] = Fraction(value_b)
            block[c][c] = Fraction(value_c)
            audit_block(block, a)

        for i in range(3):
            for j in range(3):
                if i == j:
                    continue
                for value in (-2, -1, 1, 2):
                    block = zeros()
                    block[a][a] = Fraction(2)
                    block[i][j] = Fraction(value)
                    audit_block(block, a)

    # The ordered cell, not its transpose, must be used.
    block = zeros()
    block[0][0] = Fraction(5)
    block[0][1] = Fraction(7)
    direction = choose_direction(block, 0)
    require(direction[0][1] != 0, "forward endpoint cell was not selected")
    require(direction[1][0] == 0, "endpoint order was transposed")
    require(pairing(direction, block) == 7, "forward ordered contraction is wrong")

    block = zeros()
    block[0][0] = Fraction(5)
    block[1][0] = Fraction(-3)
    direction = choose_direction(block, 0)
    require(direction[1][0] != 0, "reverse endpoint cell was not selected")
    require(direction[0][1] == 0, "reverse endpoint order was transposed")
    require(pairing(direction, block) == -3, "reverse ordered contraction is wrong")


def pencil_data(alpha, gamma, direction, a, t, u):
    k0 = unit(a, a)
    k1 = matrix_add((gamma, k0), (-alpha, direction))
    k2 = matrix_add((-alpha, direction))
    pencil = matrix_add((t, k0), (u, k1))
    return k0, k1, k2, pencil


def check_geometry_and_jets():
    samples = (
        # Old diagonal complement direction.
        (
            Fraction(2),
            Fraction(3),
            [[0, 0, 0], [0, 1, 0], [0, 0, -2]],
            0,
        ),
        # A non-diagonal direction with an extra determinant root.
        (
            Fraction(1),
            Fraction(1),
            [[0, 1, 0], [1, 1, 0], [0, 0, 1]],
            0,
        ),
        # A non-diagonal direction whose scalar-zero endpoint is singular.
        (
            Fraction(1),
            Fraction(1),
            [[0, 1, 0], [-1, 1, 0], [0, 0, 1]],
            0,
        ),
        # Vanishing complementary cofactor but invertible D.
        (
            Fraction(-2),
            Fraction(5, 3),
            [[0, 1, 0], [1, 1, 1], [0, 1, 1]],
            0,
        ),
        # A permuted selected label.
        (
            Fraction(3, 2),
            Fraction(-4),
            [[2, 0, 0], [1, 0, -1], [3, 2, -5]],
            1,
        ),
    )

    for alpha, gamma, raw_direction, a in samples:
        direction = [[Fraction(value) for value in row] for row in raw_direction]
        b, c = complement(a)
        require(direction[a][a] == 0, "sample D_aa is nonzero")
        require(direction[b][b] != 0 and direction[c][c] != 0, "sample is blind")
        k0, k1, k2, _ = pencil_data(alpha, gamma, direction, a, 0, 0)
        require(k1 == matrix_add((gamma, k0), (1, k2)), "K1 relation failed")
        expected_k1 = tuple(
            gamma if i == a else -alpha * direction[i][i] for i in range(3)
        )
        expected_k2 = tuple(
            Fraction(0) if i == a else -alpha * direction[i][i]
            for i in range(3)
        )
        require(diag(k1) == expected_k1, "wrong K1 diagonal")
        require(diag(k2) == expected_k2, "wrong K2 diagonal")

        # Build a block with the requested alpha and gamma, using D itself
        # when possible; this checks all direct-scalar identities literally.
        block = zeros()
        block[a][a] = alpha
        detector = next(
            (direction[i][j], i, j)
            for i in range(3)
            for j in range(3)
            if (i, j) != (a, a) and direction[i][j] != 0
        )
        value, i, j = detector
        block[i][j] = gamma / value
        require(pairing(direction, block) == gamma, "sample gamma construction failed")
        require(pairing(k0, block) == alpha, "K0 scalar is wrong")
        require(pairing(k1, block) == 0, "K1 is not scalar-zero")
        require(pairing(k2, block) == -alpha * gamma, "K2 scalar is wrong")

        for t, u in (
            (Fraction(1), Fraction(0)),
            (Fraction(0), Fraction(1)),
            (-gamma, Fraction(1)),
            (Fraction(7, 3), Fraction(-2, 5)),
        ):
            _, _, _, pencil = pencil_data(alpha, gamma, direction, a, t, u)
            direct = pairing(pencil, block)
            target_product = pencil[0][0] * pencil[1][1] * pencil[2][2]
            activity = direct * target_product
            expected_activity = (
                alpha**3
                * direction[b][b]
                * direction[c][c]
                * t
                * (u**2)
                * (t + gamma * u)
            )
            require(activity == expected_activity, "activity factorization failed")

            delta = (
                direction[b][b] * direction[c][c]
                - direction[b][c] * direction[c][b]
            )
            expected_det = (
                alpha**2
                * (u**2)
                * (delta * (t + gamma * u) - alpha * u * det3(direction))
            )
            require(det3(pencil) == expected_det, "determinant ledger failed")

        # Formal residue basis (rho0,rho2) and literal J rows.
        for h in range(3, 18):
            j1 = k1
            j2 = matrix_add((-gamma, k0), (h - 1, k2))
            expected_j2 = tuple(
                -gamma if i == a else -(h - 1) * alpha * direction[i][i]
                for i in range(3)
            )
            require(diag(j1) == expected_k1, "J1 residue is wrong")
            require(diag(j2) == expected_j2, "J2 residue is wrong")
            require(pairing(j1, block) == 0, "J1 scalar is wrong")
            require(
                pairing(j2, block) == -h * alpha * gamma,
                "J2 scalar is wrong",
            )
            require(all(value != 0 for value in diag(j1)), "J1 lost a label")
            require(all(value != 0 for value in diag(j2)), "J2 lost a label")

            z1 = (gamma, Fraction(1))
            z2 = (-gamma, Fraction(h - 1))
            determinant = z1[0] * z2[1] - z1[1] * z2[0]
            require(determinant == h * gamma, "two-jet determinant is wrong")
            rho2 = tuple((z1[i] + z2[i]) / h for i in range(2))
            rho0 = tuple(
                ((h - 1) * z1[i] - z2[i]) / (h * gamma)
                for i in range(2)
            )
            require(rho2 == (0, 1), "rho2 inverse failed")
            require(rho0 == (1, 0), "rho0 inverse failed")

            # Coefficient of v*w^(h-1) in
            # alpha^(h-1)(v-gamma*w)^(h-1)(v*T0+w*T2), written
            # in the formal (rho0,rho2) basis.
            unary_coefficient = alpha ** (h - 1) * ((-gamma) ** (h - 1))
            complementary_coefficient = (
                alpha ** (h - 1)
                * comb(h - 1, 1)
                * ((-gamma) ** (h - 2))
            )
            normalizer = alpha ** (h - 1) * ((-gamma) ** (h - 2))
            normalized_polar = (
                unary_coefficient / normalizer,
                complementary_coefficient / normalizer,
            )
            require(
                normalized_polar == (-gamma, h - 1),
                "binary-boundary polar normalization has a wrong sign or scalar",
            )


def check_determinant_is_not_activity():
    alpha = Fraction(1)
    gamma = Fraction(1)

    # det D=-1 and delta=1, so det K=u^2(t+2u).  The extra root
    # [t:u]=[-2:1] is physically active: t,u,t+u are all nonzero.
    direction = [
        [Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(1), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(1)],
    ]
    _, _, _, pencil = pencil_data(alpha, gamma, direction, 0, -2, 1)
    activity = (-2) * pencil[0][0] * pencil[1][1] * pencil[2][2]
    require(det3(pencil) == 0, "adversarial extra determinant root disappeared")
    require(activity != 0, "extra determinant root was mistaken for inactivity")

    # det D=delta=1 makes K1 singular although its diagonal is (1,-1,-1).
    direction = [
        [Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(-1), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(1)],
    ]
    _, k1, _, _ = pencil_data(alpha, gamma, direction, 0, 0, 0)
    require(det3(k1) == 0, "adversarial singular scalar-zero cap disappeared")
    require(all(value != 0 for value in diag(k1)), "target visibility disappeared")


def check_bounded_nondiagonal_ledger():
    """Audit all Boolean signed supports in all selected positions."""
    signed_supports = tuple(product((0, 1), repeat=6)) + tuple(
        product((0, -1), repeat=6)
    )
    for a in range(3):
        b, c = complement(a)
        off_diagonal = [(i, j) for i in range(3) for j in range(3) if i != j]
        for d_b, d_c in product((Fraction(-1), Fraction(1)), repeat=2):
            for values in signed_supports:
                direction = zeros()
                direction[b][b] = d_b
                direction[c][c] = d_c
                for (i, j), value in zip(off_diagonal, values):
                    direction[i][j] = Fraction(value)
                for alpha, gamma, t, u in (
                    (Fraction(1), Fraction(2), Fraction(3), Fraction(-1)),
                    (Fraction(-2), Fraction(3, 2), Fraction(-4), Fraction(5)),
                ):
                    _, _, _, pencil = pencil_data(
                        alpha, gamma, direction, a, t, u
                    )
                    delta = (
                        direction[b][b] * direction[c][c]
                        - direction[b][c] * direction[c][b]
                    )
                    expected_det = (
                        alpha**2
                        * (u**2)
                        * (
                            delta * (t + gamma * u)
                            - alpha * u * det3(direction)
                        )
                    )
                    require(
                        det3(pencil) == expected_det,
                        "exhaustive non-diagonal determinant ledger failed",
                    )
                    expected_activity = (
                        alpha**3
                        * d_b
                        * d_c
                        * t
                        * (u**2)
                        * (t + gamma * u)
                    )
                    literal_activity = (
                        (alpha * t)
                        * pencil[0][0]
                        * pencil[1][1]
                        * pencil[2][2]
                    )
                    require(
                        literal_activity == expected_activity,
                        "exhaustive non-diagonal activity ledger failed",
                    )


def check_certificate_degree_bounds():
    for d in range(0, 65):
        for r in range(d + 1):
            for s in range(d - r + 1):
                for w in range(d - r - s + 1):
                    gcd_degree = r + s + w
                    reduced_degree = d - gcd_degree
                    divided_target_degree = 3 * d - gcd_degree
                    require(
                        divided_target_degree >= 2 * reduced_degree - 1,
                        "symmetric target misses the binary CI range",
                    )
                    require(
                        divided_target_degree - reduced_degree == 2 * d,
                        "symmetric multiplier degree is wrong",
                    )

        for third_multiplicity in range(d + 1):
            saturated_degree = d - third_multiplicity
            for r in range(saturated_degree + 1):
                for s in range(saturated_degree - r + 1):
                    gcd_degree = r + s
                    reduced_degree = saturated_degree - gcd_degree
                    divided_target_degree = 2 * saturated_degree - gcd_degree
                    require(
                        divided_target_degree >= 2 * reduced_degree - 1,
                        "chartwise target misses the binary CI range",
                    )
                    require(
                        divided_target_degree - reduced_degree == saturated_degree,
                        "chartwise multiplier degree is wrong",
                    )


def check_intrinsic_collision():
    for a in range(3):
        b, c = complement(a)
        for alpha in (Fraction(1), Fraction(-2), Fraction(3, 5)):
            block = zeros()
            block[a][a] = alpha
            require(choose_direction(block, a) is None, "intrinsic block found gamma")
            # Here sigma(K)=alpha*K_aa.  Exhaust a small diagonal family to
            # guard the converse: scalar-zero caps always lose label a.
            for diagonal in product((-2, -1, 0, 1, 2), repeat=3):
                candidate = zeros()
                for i, value in enumerate(diagonal):
                    candidate[i][i] = Fraction(value)
                if pairing(candidate, block) == 0:
                    require(
                        not all(value != 0 for value in diag(candidate)),
                        "intrinsic block admitted an all-visible scalar-zero cap",
                    )
            direction = zeros()
            direction[b][b] = Fraction(2)
            direction[c][c] = Fraction(-3)
            gamma = pairing(direction, block)
            require(gamma == 0, "intrinsic contraction should vanish")
            k0, k1, k2, _ = pencil_data(alpha, gamma, direction, a, 0, 0)
            require(k1 == k2, "intrinsic boundary did not collide")
            for h in range(3, 18):
                j2 = matrix_add((-gamma, k0), (h - 1, k2))
                require(j2 == matrix_add((h - 1, k1)), "collision jets did not collapse")
                require(diag(k1)[a] == diag(j2)[a] == 0, "blind label became visible")


def main():
    check_existence_iff_and_ordering()
    check_geometry_and_jets()
    check_determinant_is_not_activity()
    check_bounded_nondiagonal_ledger()
    check_certificate_degree_bounds()
    check_intrinsic_collision()
    print("adaptive diagonal uncollision cap routing: PASS")
    print("  D exists exactly off A = alpha E_aa, with endpoint order retained")
    print("  activity boundary: u * t * (t + gamma*u)")
    print("  generic two-jet determinant: h*gamma; every label visible")
    print("  non-diagonal determinant roots are not activity boundaries")
    print("  intrinsic coordinate block retains the collided blind-label gap")


if __name__ == "__main__":
    main()
