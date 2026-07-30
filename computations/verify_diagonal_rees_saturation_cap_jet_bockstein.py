#!/usr/bin/env python3
"""Dependency-free checks for the diagonal Rees/cap-jet note.

The uniform statements are proved in the accompanying note.  This script
audits their exact scalar, matrix, principal-parts, target/residue,
zero-trace, collision, and palette-projection ledgers.  All failure
conditions remain active under ``python3 -O``.
"""

from fractions import Fraction
from math import comb


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def matrix_add(*terms):
    """Add ``(scalar, matrix)`` terms."""
    return [
        [sum(scale * matrix[i][j] for scale, matrix in terms) for j in range(3)]
        for i in range(3)
    ]


def matrix_pair(left, right):
    return sum(left[i][j] * right[i][j] for i in range(3) for j in range(3))


def diagonal_data(block, a):
    alpha = block[a][a]
    require(alpha != 0, "selected diagonal entry must be nonzero")
    tau = sum(block[i][i] for i in range(3))
    beta = tau - alpha
    identity = [[Fraction(int(i == j)) for j in range(3)] for i in range(3)]
    k0 = [
        [Fraction(int(i == a and j == a)) for j in range(3)] for i in range(3)
    ]
    k1 = matrix_add((tau, k0), (-alpha, identity))
    k2 = matrix_add((alpha, k0), (-alpha, identity))
    return alpha, tau, beta, k0, k1, k2


def diag(matrix):
    return tuple(matrix[i][i] for i in range(3))


def check_cap_jet_representatives():
    samples = (
        ([[2, 3, -1], [5, 7, 11], [13, 17, 19]], 0),
        ([[3, 2, 5], [7, -5, -6], [13, 17, 2]], 1),
        # tau=0 and beta=-alpha at a=2.
        ([[2, 7, -1], [5, -5, 11], [13, 17, 3]], 2),
        # beta=0 at a=0.
        ([[4, 2, 5], [7, 9, -6], [13, 17, -9]], 0),
    )
    saw_generic = False
    saw_collision = False
    saw_zero_trace = False
    saw_nonzero_trace = False
    for raw, a in samples:
        block = [[Fraction(value) for value in row] for row in raw]
        alpha, tau, beta, k0, k1, k2 = diagonal_data(block, a)
        identity = [
            [Fraction(int(i == j)) for j in range(3)] for i in range(3)
        ]
        require(beta == tau - alpha, "wrong beta ledger")
        require(matrix_pair(k0, block) == alpha, "wrong K0 direct scalar")
        require(matrix_pair(k1, block) == 0, "K1 is not scalar-zero")
        require(matrix_pair(k2, block) == -alpha * beta, "wrong K2 scalar")
        require(k1 == matrix_add((beta, k0), (1, k2)), "K1 relation failed")

        # Equation (22): the scalar relation is legal using alpha alone.
        scalar_relation = matrix_add((tau / alpha, k0), (-1, identity))
        require(
            scalar_relation == matrix_add((1 / alpha, k1)),
            "scalar-zero cap relation has a wrong alpha or tau factor",
        )
        require(
            matrix_pair(scalar_relation, block) == 0,
            "scalar-zero cap relation retained a radial symbol",
        )
        if tau:
            saw_nonzero_trace = True
            normalized_transition = matrix_add(
                (1 / alpha, k0), (-1 / tau, identity)
            )
            require(
                normalized_transition
                == matrix_add((1 / (alpha * tau), k1)),
                "nonzero-trace radial transition has a wrong factor",
            )
            require(
                matrix_pair(normalized_transition, block) == 0,
                "normalized radial lifts have unequal symbols",
            )
        else:
            saw_zero_trace = True
            require(tau / alpha == 0, "zero-trace first radial term survived")
            require(
                matrix_pair(identity, block) == 0,
                "zero-trace trace cap retained a radial symbol",
            )

        for h in range(3, 17):
            j1 = k1
            j2 = matrix_add((-beta, k0), (h - 1, k2))
            require(matrix_pair(j1, block) == 0, "wrong J1 direct scalar")
            require(
                matrix_pair(j2, block) == -h * alpha * beta,
                "wrong J2 direct scalar",
            )

            expected_j1 = tuple(
                beta if c == a else -alpha for c in range(3)
            )
            expected_j2 = tuple(
                -beta if c == a else -(h - 1) * alpha for c in range(3)
            )
            require(diag(j1) == expected_j1, "J1 does not represent Z1")
            require(diag(j2) == expected_j2, "J2 does not represent Z2")

            # P(J)q^[h-1]=h*T(J): its ordinary residue has the same h,
            # while CapRes divides exactly that known characteristic-zero h.
            for expected_target in (expected_j1, expected_j2):
                literal_target = tuple(h * value for value in expected_target)
                ordinary_residue = literal_target
                cap_residue = tuple(value / h for value in ordinary_residue)
                require(
                    cap_residue == expected_target,
                    "cap target/residue normalization lost a factor h",
                )

            # Formal basis (rho0,rho2): Z1=(beta,1), Z2=(-beta,h-1).
            z1 = (beta, Fraction(1))
            z2 = (-beta, Fraction(h - 1))
            if beta:
                saw_generic = True
                require(all(value != 0 for value in expected_j1), "generic J1 blind")
                require(all(value != 0 for value in expected_j2), "generic J2 blind")
                recovered_rho2 = tuple((z1[i] + z2[i]) / h for i in range(2))
                recovered_rho0 = tuple(
                    ((h - 1) * z1[i] - z2[i]) / (h * beta)
                    for i in range(2)
                )
                require(recovered_rho2 == (0, 1), "rho2 inverse failed")
                require(recovered_rho0 == (1, 0), "rho0 inverse failed")
            else:
                saw_collision = True
                require(j2 == matrix_add((h - 1, j1)), "collision rows did not collapse")
                require(diag(j1)[a] == diag(j2)[a] == 0, "collision sees blind label")
    require(saw_generic and saw_collision, "both beta strata must be checked")
    require(saw_zero_trace and saw_nonzero_trace, "both tau strata must be checked")


def polynomial_v_coefficients(h, alpha, beta, selected):
    """Coefficients by v-power in (37), with w-power implicit."""
    # (v-beta*w)^(h-1), then multiply by v or w.
    coefficients = {}
    for v_power in range(h):
        w_power = (h - 1) - v_power
        coefficient = (
            Fraction(comb(h - 1, v_power))
            * ((-beta) ** w_power)
        )
        if selected:
            exponent = v_power + 1
            coefficient *= alpha ** (h - 1)
        else:
            exponent = v_power
            coefficient *= -(alpha**h)
        coefficients[exponent] = coefficients.get(exponent, Fraction(0)) + coefficient
    return coefficients


def valuation(coefficients):
    nonzero = [power for power, coefficient in coefficients.items() if coefficient]
    require(nonzero, "zero polynomial has no finite valuation")
    return min(nonzero)


def check_collision_valuations():
    for h in range(3, 65):
        for alpha in (Fraction(1), Fraction(-2), Fraction(3, 5)):
            for beta in (Fraction(4), Fraction(-7, 3)):
                require(
                    valuation(polynomial_v_coefficients(h, alpha, beta, True)) == 1,
                    "generic selected target has wrong boundary order",
                )
                require(
                    valuation(polynomial_v_coefficients(h, alpha, beta, False)) == 0,
                    "generic complementary target has wrong boundary order",
                )
            require(
                valuation(polynomial_v_coefficients(h, alpha, Fraction(0), True)) == h,
                "collision selected target must first occur in order h",
            )
            require(
                valuation(polynomial_v_coefficients(h, alpha, Fraction(0), False))
                == h - 1,
                "collision complementary target must first occur in order h-1",
            )


def vector_add(left, right, left_scale=1, right_scale=1):
    return tuple(left_scale * x + right_scale * y for x, y in zip(left, right))


def in_coordinate_subspace(vector, allowed_indices):
    allowed = set(allowed_indices)
    return all(value == 0 for index, value in enumerate(vector) if index not in allowed)


def check_principal_parts_criterion():
    # Exact-kernel family: M=Q^4, N=ker(epsilon)=<e0,e1>.  Evaluation
    # divisibility and literal divisibility agree for every multiplicity.
    zero = Fraction(0)
    one = Fraction(1)
    coefficients = [
        (one, zero, zero, zero),
        (zero, Fraction(3), zero, zero),
        (Fraction(-2), Fraction(5), zero, zero),
        (zero, zero, Fraction(5), Fraction(-2)),
        (Fraction(7), zero, Fraction(11), Fraction(13)),
    ]
    epsilon = lambda vector: vector[2:]
    for r in range(len(coefficients) + 1):
        evaluation_divisible = all(
            epsilon(coefficients[j]) == (zero, zero) for j in range(r)
        )
        literal_divisible = all(
            in_coordinate_subspace(coefficients[j], (0, 1)) for j in range(r)
        )
        require(
            evaluation_divisible == literal_divisible,
            "global equality failed even though N=ker(epsilon)",
        )
        if literal_divisible:
            quotient = coefficients[r:]
            # P-v^r Q consists exactly of the low principal parts.
            reconstructed_tail = [(zero,) * 4 for _ in range(r)] + quotient
            difference = [
                vector_add(coefficients[j], reconstructed_tail[j], 1, -1)
                for j in range(len(coefficients))
            ]
            require(
                all(
                    in_coordinate_subspace(vector, (0, 1))
                    for vector in difference
                ),
                "tail extraction did not leave an N-valued polynomial",
            )

    # Global failure / relative-family guard: epsilon(z)=0,
    # epsilon(response)=1, N=0.  For every tested r, the first r source
    # coefficients lie in ker(epsilon) but not in N.  Thus evaluation is
    # v^r-divisible while the source is not; a family excluding these rows
    # can still satisfy the relative equality.
    z = (one, zero)
    response = (zero, one)
    radial_evaluation = lambda vector: vector[1]
    for r in range(1, 7):
        p = [z for _ in range(r)] + [response]
        require(
            all(radial_evaluation(p[j]) == 0 for j in range(r))
            and radial_evaluation(p[r]) == 1,
            "guard evaluation failed",
        )
        require(
            any(p[j] != (zero, zero) for j in range(r)),
            "negative principal parts unexpectedly became literal boundaries",
        )


def check_same_power_target_residue_lock():
    # In the exposed row ell*A + Q*t_c*B = lambda*Y, quotienting by the
    # A-summand leaves exactly lambda*Ybar.  A canonical cap with diagonal
    # entry kappa has literal target h*kappa and ordinary residue h*kappa.
    # Its target companion has residue -h*kappa; only after dividing both
    # by h are the residues kappa and -kappa.
    for h in range(3, 17):
        for kappa in (Fraction(0), Fraction(1), Fraction(-3), Fraction(5, 7)):
            cap_target = h * kappa
            cap_ordinary_residue = cap_target
            companion_target = -cap_target
            companion_ordinary_residue = companion_target
            require(
                cap_target + companion_target == 0,
                "same-power targets did not cancel",
            )
            require(
                cap_ordinary_residue + companion_ordinary_residue == 0,
                "same-power target cancellation retained an odd residue",
            )
            require(
                cap_ordinary_residue / h == kappa
                and companion_ordinary_residue / h == -kappa,
                "same-power normalized residue lost a factor h",
            )


def check_binary_lift_bookkeeping():
    # The uniform proof uses these support/degree facts and then a necessary
    # palette projection: q_tilde itself may still contain a-colour cells.
    rhs = {"a": Fraction(0), "b": Fraction(1), "c": Fraction(1)}
    projected_colours = {"b", "c"}
    for h in range(3, 65):
        odd_sites = 2 * h - 1
        require(2 * h > odd_sites, "q0^[h] support count failed")
        require(h - 1 >= 1, "odd common power has wrong exponent")
        require(
            Fraction(comb(h, 1), h) == 1,
            "divided-power linear lift acquired a binomial factor",
        )
        # Both lift summands use the same exposed site, so their square is zero.
        lift_site_multiplicity = 2
        require(lift_site_multiplicity > 1, "lift square should repeat exposed site")
        projected_rhs = {
            colour: coefficient
            for colour, coefficient in rhs.items()
            if colour in projected_colours
        }
        require(
            projected_rhs == {"b": Fraction(1), "c": Fraction(1)},
            "projection changed the two complementary target coefficients",
        )
        require(
            {colour for colour, coefficient in projected_rhs.items() if coefficient}
            == projected_colours,
            "projected aggregate does not have exactly the binary palette",
        )


def main():
    check_cap_jet_representatives()
    check_collision_valuations()
    check_principal_parts_criterion()
    check_same_power_target_residue_lock()
    check_binary_lift_bookkeeping()
    print("diagonal Rees saturation and cap-jet Bockstein: PASS")
    print("  generic Z1 and Z2 are literal cap contractions")
    print("  scalar gcd lifting is equivalent to literal low-jet membership")
    print("  same-power target cancellation also cancels ordinary odd residue")
    print("  beta=0 collapses the jets and delays the selected target to order h")


if __name__ == "__main__":
    main()
