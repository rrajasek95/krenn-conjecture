#!/usr/bin/env python3
"""Light exact audit of the diagonal three-boundary routing ledger.

This uses only the standard library.  It checks the finite scalar,
coefficient, collision, jet-normalization, and certificate-degree
bookkeeping.  The note supplies the uniform divided-power and binary
complete-intersection arguments.
"""

from fractions import Fraction
from math import comb


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def matrix_pair(left, right):
    return sum(
        left[i][j] * right[i][j]
        for i in range(3)
        for j in range(3)
    )


def determinant(matrix):
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def diagonal_endpoints(block, a):
    alpha = block[a][a]
    require(alpha != 0, "selected diagonal entry must be nonzero")
    trace = sum(block[i][i] for i in range(3))
    beta = trace - alpha
    k0 = [[Fraction(int(i == a and j == a)) for j in range(3)] for i in range(3)]
    k1 = [
        [trace * k0[i][j] - alpha * int(i == j) for j in range(3)]
        for i in range(3)
    ]
    k2 = [
        [alpha * (int(i == a and j == a) - int(i == j)) for j in range(3)]
        for i in range(3)
    ]
    return alpha, trace, beta, k0, k1, k2


def add_matrix(left, right, left_scale=1, right_scale=1):
    return [
        [left_scale * left[i][j] + right_scale * right[i][j] for j in range(3)]
        for i in range(3)
    ]


def check_endpoint_geometry():
    samples = (
        ([[2, 3, -1], [5, 7, 11], [13, 17, 19]], 0),
        ([[3, 2, 5], [7, -5, -6], [13, 17, 2]], 1),
        # beta=0 collision at a=0: the other two diagonal entries sum to zero.
        ([[4, 2, 5], [7, 9, -6], [13, 17, -9]], 0),
    )
    saw_generic = False
    saw_collision = False
    for raw_block, a in samples:
        block = [[Fraction(value) for value in row] for row in raw_block]
        alpha, _, beta, k0, k1, k2 = diagonal_endpoints(block, a)
        require(matrix_pair(k0, block) == alpha, "wrong K0 direct scalar")
        require(matrix_pair(k1, block) == 0, "K1 is not scalar-zero")
        require(k2 == add_matrix(k1, k0, 1, -beta), "wrong binary boundary")
        require(
            [k1[i][i] for i in range(3)][a] == beta,
            "wrong selected diagonal at K1",
        )
        require(
            all(k1[c][c] == -alpha for c in range(3) if c != a),
            "wrong complementary diagonal at K1",
        )
        require(k2[a][a] == 0, "K2 is not missing the selected target")
        require(
            all(k2[c][c] == -alpha for c in range(3) if c != a),
            "K2 is not the binary boundary",
        )
        require(determinant(k1) == alpha * alpha * beta, "wrong K1 determinant")
        require(determinant(k2) == 0, "binary boundary should be singular")

        for t, u in ((1, 1), (2, -3), (0, 5), (7, 0), (-beta, 1)):
            cap = add_matrix(k0, k1, t, u)
            direct = alpha * t
            target_product = Fraction(1)
            for c in range(3):
                target_product *= cap[c][c]
            activity = direct * target_product
            expected = (alpha ** 3) * t * (u ** 2) * (t + beta * u)
            require(activity == expected, "wrong diagonal activity polynomial")

        if beta:
            saw_generic = True
            require(k1 != k2, "generic scalar-zero and binary points collided")
        else:
            saw_collision = True
            require(k1 == k2, "trace collision did not merge K1 and K2")
    require(saw_generic and saw_collision, "both geometry strata must be tested")


def scalar_zero_coefficients(h, alpha, beta):
    """Formal clean-error coefficients in (t,u).

    A dictionary entry ('mixed', j) denotes R^[j] F^[h-j].  Target
    entries are stored labelwise as 'unary' and 'complement'.
    """
    rows = []
    for j in range(h + 1):
        row = {("mixed", j): Fraction(1)}
        if j == 0:
            row["unary"] = -(alpha ** (h - 1))
        if j == 1:
            row["unary"] = -(alpha ** (h - 1)) * beta
            row["complement"] = alpha**h
        rows.append(row)
    return rows


def target_polynomial_coefficients(h, alpha, beta):
    """Coefficients of alpha^(h-1)(v-beta*w)^(h-1)(v*Xa-alpha*w*D)."""
    rows = []
    # Row j is the coefficient of v^(h-j) w^j.
    for j in range(h + 1):
        unary = Fraction(0)
        complement = Fraction(0)
        # Unary target contributes one v.
        power_w = j
        power_v = (h - 1) - power_w
        if power_v >= 0 and power_v + 1 == h - j:
            unary = (alpha ** (h - 1)) * comb(h - 1, power_w) * ((-beta) ** power_w)
        # Complementary target contributes one w and scalar -alpha.
        power_w = j - 1
        power_v = (h - 1) - power_w
        if power_w >= 0 and power_v == h - j:
            complement = (
                -(alpha**h)
                * comb(h - 1, power_w)
                * ((-beta) ** power_w)
            )
        rows.append((unary, complement))
    return rows


def check_boundary_jets():
    for h in range(3, 65):
        for alpha in (Fraction(1), Fraction(-2), Fraction(3, 5)):
            for beta in (Fraction(0), Fraction(4), Fraction(-7, 3)):
                rows = scalar_zero_coefficients(h, alpha, beta)
                first = rows[1]
                require(
                    -first["unary"] == (alpha ** (h - 1)) * beta,
                    "wrong scalar-zero unary jet",
                )
                require(
                    -first["complement"] == -(alpha**h),
                    "wrong scalar-zero complementary jet",
                )

                transformed = target_polynomial_coefficients(h, alpha, beta)
                endpoint_unary, endpoint_complement = transformed[h]
                require(endpoint_unary == 0, "K2 endpoint acquired a unary target")
                require(
                    endpoint_complement == ((-1) ** h) * (alpha**h) * (beta ** (h - 1)),
                    "wrong K2 endpoint correction",
                )
                inward_unary, inward_complement = transformed[h - 1]
                require(
                    inward_unary == (alpha ** (h - 1)) * ((-beta) ** (h - 1)),
                    "wrong binary inward unary jet",
                )
                require(
                    inward_complement
                    == -(h - 1) * (alpha**h) * ((-beta) ** (h - 2)),
                    "wrong binary inward complementary jet",
                )

                if beta:
                    require(
                        beta != 0 and alpha != 0,
                        "generic jets must see the selected colour",
                    )
                    require(
                        -(h - 1) * alpha != 0,
                        "generic binary jet must see every complementary colour",
                    )
                    # Work in the formal basis (rho0,rho2).  Z1=(beta,1),
                    # Z2=(-beta,h-1), with determinant h*beta.
                    determinant_of_jets = beta * (h - 1) - (-beta)
                    require(determinant_of_jets == h * beta, "wrong two-jet determinant")
                    # Inverse formulas rho2=(Z1+Z2)/h and
                    # rho0=((h-1)Z1-Z2)/(h*beta).
                    z1 = (beta, Fraction(1))
                    z2 = (-beta, Fraction(h - 1))
                    rho2 = tuple((z1[i] + z2[i]) / h for i in range(2))
                    rho0 = tuple(((h - 1) * z1[i] - z2[i]) / (h * beta) for i in range(2))
                    require(rho2 == (0, 1), "failed to recover complementary residue")
                    require(rho0 == (1, 0), "failed to recover unary residue")
                else:
                    require(
                        inward_unary == inward_complement == 0,
                        "collision should kill the first binary target jet",
                    )


def check_certificate_degree_bounds():
    for d in range(0, 65):
        # Three distinct boundary lines.
        for a in range(d + 1):
            for b in range(d - a + 1):
                for c in range(d - a - b + 1):
                    gcd_degree = a + b + c
                    reduced_degree = d - gcd_degree
                    target_degree = 3 * d - gcd_degree
                    require(
                        target_degree >= 2 * reduced_degree - 1,
                        "three-boundary target misses the complete-intersection range",
                    )
                    require(
                        target_degree - reduced_degree == 2 * d,
                        "wrong three-boundary multiplier degree",
                    )

        # Collision: only two distinct boundary lines.
        for a in range(d + 1):
            for b in range(d - a + 1):
                gcd_degree = a + b
                reduced_degree = d - gcd_degree
                target_degree = 2 * d - gcd_degree
                require(
                    target_degree >= 2 * reduced_degree - 1,
                    "collision target misses the complete-intersection range",
                )
                require(
                    target_degree - reduced_degree == d,
                    "wrong collision multiplier degree",
                )

        # Generic asymmetric saturation: after removing r copies of the
        # third boundary line, the usual two-boundary theorem has residual
        # and multiplier degree e=d-r.
        for third_multiplicity in range(d + 1):
            saturated_degree = d - third_multiplicity
            for a in range(saturated_degree + 1):
                for b in range(saturated_degree - a + 1):
                    gcd_degree = a + b
                    reduced_degree = saturated_degree - gcd_degree
                    target_degree = 2 * saturated_degree - gcd_degree
                    require(
                        target_degree >= 2 * reduced_degree - 1,
                        "saturated chart misses the complete-intersection range",
                    )
                    require(
                        target_degree - reduced_degree == saturated_degree,
                        "wrong saturated two-boundary multiplier degree",
                    )


def main():
    check_endpoint_geometry()
    check_boundary_jets()
    check_certificate_degree_bounds()
    print("diagonal three-boundary inactive routing: PASS")
    print("  generic activity boundary: u * t * (t + beta*u)")
    print("  trace collision beta=0: scalar-zero = binary boundary")
    print("  generic normalized jet determinant: h*beta")
    print("  symmetric multiplier degree 2d; saturated chart degree e")


if __name__ == "__main__":
    main()
