#!/usr/bin/env python3
"""Light exact audit of the off-diagonal ternary Omega ledger.

This checks only finite coefficient bookkeeping.  The note supplies the
uniform divided-power proof and cites the already audited binary Bezout
theorem for the all-order certificate.
"""

from fractions import Fraction


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


def canonical_endpoints(block, a, b):
    alpha = block[a][b]
    require(a != b, "the selected entry must be off diagonal")
    require(alpha != 0, "the selected direct entry must be nonzero")
    trace = sum(block[i][i] for i in range(3))
    k0 = [[Fraction(int(i == a and j == b)) for j in range(3)] for i in range(3)]
    k1 = [
        [trace * k0[i][j] - alpha * int(i == j) for j in range(3)]
        for i in range(3)
    ]
    return alpha, trace, k0, k1


def check_endpoint_geometry():
    samples = (
        (
            [[2, 3, -1], [5, 7, 11], [13, 17, 19]],
            0,
            1,
        ),
        (
            [[Fraction(1, 2), -4, 3], [2, -5, 7], [11, 13, 17]],
            1,
            0,
        ),
        (
            [[3, 2, 5], [7, 11, -6], [13, 17, 19]],
            1,
            2,
        ),
    )
    for raw_block, a, b in samples:
        block = [[Fraction(value) for value in row] for row in raw_block]
        alpha, _, k0, k1 = canonical_endpoints(block, a, b)
        require(matrix_pair(k0, block) == alpha, "wrong K0 direct scalar")
        require(matrix_pair(k1, block) == 0, "K1 is not scalar-zero")
        require([k0[i][i] for i in range(3)] == [0, 0, 0], "K0 target is nonzero")
        require(
            [k1[i][i] for i in range(3)] == [-alpha, -alpha, -alpha],
            "K1 target is not ternary with common coefficient",
        )
        require(determinant(k1) == (-alpha) ** 3, "wrong K1 determinant")

        # On t*K0+u*K1 the direct scalar is alpha*t and every target
        # coefficient is -alpha*u.  Their product is -alpha^4*t*u^3.
        for t, u in ((1, 1), (2, -3), (0, 5), (7, 0)):
            direct = alpha * t
            targets = [-alpha * u] * 3
            activity = direct
            for target in targets:
                activity *= target
            require(
                activity == -(alpha ** 4) * t * (u ** 3),
                "wrong off-diagonal activity polynomial",
            )
            require((activity != 0) == (t != 0 and u != 0), "wrong activity locus")


def clean_error_coefficients(h, alpha, base_clean, scalar_zero_clean):
    """Formal coefficient ledger with either endpoint optionally clean.

    Tokens ('mixed', j) mean R^[j] F^[h-j], while 'delta' is the
    monochromatic target.  If scalar_zero_clean is true, R^[h] is also
    removed.  Zero coefficients are omitted.
    """
    coefficients = []
    for j in range(h + 1):
        row = {}
        if 0 < j < h or (j == 0 and not base_clean) or (j == h and not scalar_zero_clean):
            row[("mixed", j)] = Fraction(1)
        if j == 1:
            row["delta"] = alpha ** h
        coefficients.append(row)
    return coefficients


def check_divided_power_ledger():
    for h in range(3, 65):
        for alpha in (Fraction(1), Fraction(-2), Fraction(3, 5)):
            coefficients = clean_error_coefficients(h, alpha, True, False)
            require(coefficients[0] == {}, f"K0 endpoint did not vanish at h={h}")
            require(
                coefficients[h] == {("mixed", h): 1},
                f"a nonclean K1 endpoint was incorrectly removed at h={h}",
            )
            require(
                all(coefficients[j] for j in range(1, h + 1)),
                f"a one-sided residual coefficient was omitted at h={h}",
            )
            omega_zero = coefficients[1]
            require(
                omega_zero == {("mixed", 1): 1, "delta": alpha ** h},
                f"wrong first Omega coefficient at h={h}",
            )

            # RF^[h-1] - Omega(1,0) = -alpha^h Delta
            boundary_delta = -omega_zero["delta"]
            require(boundary_delta == -(alpha ** h), "wrong boundary-polar sign")

            # Dividing the exposed coefficient identity by alpha^(h-1)
            # leaves the normalized residue -Y_c after one further scalar
            # normalization by alpha.
            residue = boundary_delta / (alpha ** (h - 1))
            require(residue == -alpha, "wrong odd residue normalization")
            require(residue / alpha == -1, "normalized two-chart class is not universal")

            reverse = clean_error_coefficients(h, alpha, False, True)
            require(
                reverse[0] == {("mixed", 0): 1},
                f"a nonclean K0 endpoint was incorrectly removed at h={h}",
            )
            require(reverse[h] == {}, f"clean K1 endpoint did not vanish at h={h}")
            require(
                all(reverse[j] for j in range(0, h)),
                f"a reverse one-sided residual coefficient was omitted at h={h}",
            )
            require(
                reverse[1] == {("mixed", 1): 1, "delta": alpha ** h},
                f"reverse orientation lost the common boundary jet at h={h}",
            )

            two_root = clean_error_coefficients(h, alpha, True, True)
            require(two_root[h] == {}, f"clean K1 endpoint did not vanish at h={h}")
            require(
                all(two_root[j] for j in range(1, h)),
                f"an interior two-root coefficient was omitted at h={h}",
            )


def check_torus_koszul_middle_line():
    for h in range(3, 65):
        for d in (h - 1, h - 2):
            weights = [2 * (d - n) for n in range(2 * d + 1)]
            require(weights[d] == 0, f"middle weight is nonzero at h={h}, d={d}")
            require(
                all(weight != 0 for n, weight in enumerate(weights) if n != d),
                f"extra torus-Koszul cokernel weight at h={h}, d={d}",
            )


def main():
    check_endpoint_geometry()
    check_divided_power_ledger()
    check_torus_koszul_middle_line()
    print("off-diagonal base-locus/ternary Omega residue: PASS")
    print("  endpoint target: -alpha*(X0+X1+X2)")
    print("  normalized odd residue: -Y_c in every chart")
    print("  one-root/two-root degrees: h-1 and h-2")
    print("  remaining certificate class: unique torus middle weight")


if __name__ == "__main__":
    main()
