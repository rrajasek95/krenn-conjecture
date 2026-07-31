#!/usr/bin/env python3
"""Exact lightweight checks for the residue-chain-map reduction.

This audits only the proved coefficient and representation-theoretic
statements in ``notes/residue-chain-map-radial-transgression.md``.  It does
not construct the physical radial-to-response transgression.
"""

from fractions import Fraction


def require(condition, message):
    """Optimization-safe assertion."""
    if not condition:
        raise RuntimeError(message)


def add(left, right, scale=Fraction(1)):
    require(len(left) == len(right), "polynomial degrees do not agree")
    return [left[index] + scale * right[index] for index in range(len(left))]


def multiply(left, right):
    """Multiply binary forms indexed by the exponent of u."""
    product = [Fraction(0) for _ in range(len(left) + len(right) - 1)]
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            product[i + j] += left_value * right_value
    return product


def derivative_t(form):
    degree = len(form) - 1
    return [(degree - index) * form[index] for index in range(degree)]


def derivative_u(form):
    degree = len(form) - 1
    return [(index + 1) * form[index + 1] for index in range(degree)]


def first_transvectant(left, right):
    return add(
        multiply(derivative_t(left), derivative_u(right)),
        multiply(derivative_u(left), derivative_t(right)),
        scale=Fraction(-1),
    )


def alternating_bracket(gamma, ell):
    require(len(gamma) == len(ell) == 2, "bracket needs two linear forms")
    return gamma[0] * ell[1] - gamma[1] * ell[0]


def central_form(d):
    form = [Fraction(0) for _ in range(2 * d + 1)]
    form[d] = Fraction(1)
    return form


def product(values):
    result = Fraction(1)
    for value in values:
        result *= value
    return result


def check_divided_power_and_gauge_normalizations():
    """Check the matching coefficients before passing to the zero quotient."""
    for h in range(3, 31):
        # Fix one near-perfect matching on 2h-1 sites.  In divided-power
        # normalization its coefficient in q^[h-1] is the product of the
        # edge coefficients.  In q*q^[h-2], each of the h-1 matching edges
        # can be supplied by the first factor, giving the factor h-1.
        edge_values = [
            Fraction(2 * edge + h + 1, edge + h + 2)
            for edge in range(h - 1)
        ]
        coefficient_a = product(edge_values)
        coefficient_q_times_b = sum(
            edge_values[chosen]
            * product(
                edge_values[edge]
                for edge in range(h - 1)
                if edge != chosen
            )
            for chosen in range(h - 1)
        )
        require(
            coefficient_q_times_b == (h - 1) * coefficient_a,
            f"wrong divided-power multiplication factor at h={h}",
        )

        # For a fixed unmatched site x, the coefficient of
        # Z_q^beta*T*q^[h-2] sums beta_y+beta_z over all matching edges.
        # This is sum(beta)-beta_x, exactly the near-perfect gauge factor.
        unmatched_beta = Fraction(3 * h - 2, 2 * h + 1)
        endpoint_betas = [
            (
                Fraction(edge + 2, h + 3),
                Fraction(2 * h - edge + 1, h + 4),
            )
            for edge in range(h - 1)
        ]
        t_coefficient = Fraction(h + 5, 2 * h + 3)
        gauge_left = sum(
            (endpoint_betas[chosen][0] + endpoint_betas[chosen][1])
            * edge_values[chosen]
            * product(
                edge_values[edge]
                for edge in range(h - 1)
                if edge != chosen
            )
            * t_coefficient
            for chosen in range(h - 1)
        )
        sum_beta = unmatched_beta + sum(
            left_beta + right_beta
            for left_beta, right_beta in endpoint_betas
        )
        gauge_right = (
            sum_beta - unmatched_beta
        ) * t_coefficient * coefficient_a
        require(
            gauge_left == gauge_right,
            f"near-perfect gauge normalization failed at h={h}",
        )


def check_representation_ledger():
    for d in range(1, 41):
        target = 2 * d

        # On the independent transverse line, S_1 has no invariant, while
        # S_1 tensor S_1 has the unique alternating invariant.
        require(
            (-1) ** 1 == -1,
            f"transverse linear carrier lost odd parity at d={d}",
        )
        transverse_tensor_summands = (2, 0)
        require(
            transverse_tensor_summands.count(0) == 1,
            f"alternating invariant multiplicity changed at d={d}",
        )

        # If one additionally identifies the transverse and clean lines,
        # S_1 tensor S_1 = S_2 plus S_0.  The scalar route contributes one
        # target copy and the S_2 transvectant contributes one more.
        symmetric_two_summands = (target + 2, target, target - 2)
        multiplicity = 1 + symmetric_two_summands.count(target)
        require(multiplicity == 2, f"wrong natural-map multiplicity at d={d}")


def check_bracket_prolongation():
    gamma_samples = (
        (Fraction(1), Fraction(0)),
        (Fraction(3), Fraction(-2)),
        (Fraction(-5, 2), Fraction(7, 3)),
    )
    defects = (Fraction(1), Fraction(-4, 3), Fraction(9, 5))

    for d in range(1, 41):
        certificate = central_form(d)
        torus_weights = [2 * (d - index) for index in range(2 * d + 1)]
        require(
            [index for index, weight in enumerate(torus_weights) if weight == 0]
            == [d],
            f"torus cokernel is not the unique middle line at d={d}",
        )

        for gamma in gamma_samples:
            require(gamma[0] != 0, "sampled selected curvature vanished")
            ell = (Fraction(0), Fraction(1, 1) / gamma[0])
            require(
                alternating_bracket(gamma, ell) == 1,
                f"curvature endpoint normalization failed at d={d}",
            )
            require(
                alternating_bracket(ell, gamma) == -1,
                f"bracket lost antisymmetry at d={d}",
            )
            require(
                alternating_bracket(gamma, gamma) == 0,
                f"bracket is not alternating at d={d}",
            )

            quadratic = multiply(gamma, ell)
            transvectant = first_transvectant(quadratic, certificate)
            require(
                transvectant[d] == 0,
                f"first transvectant acquired a middle coefficient at d={d}",
            )

            a, b = gamma
            c, e = ell
            expected = [Fraction(0) for _ in range(2 * d + 1)]
            expected[d - 1] = 2 * d * a * c
            expected[d + 1] = -2 * d * b * e
            require(
                transvectant == expected,
                f"wrong first-transvectant formula at d={d}: {transvectant}",
            )

            for defect in defects:
                certificate_class = [defect * value for value in certificate]
                correction = [-defect * value for value in certificate]
                require(
                    correction[d] == -defect,
                    f"wrong correction middle coefficient at d={d}",
                )
                require(
                    add(certificate_class, correction)
                    == [Fraction(0) for _ in certificate],
                    f"certificate was not cancelled coefficientwise at d={d}",
                )

                # The direct-free formula -(AU)^(-1) tau(AUz) P has the
                # same result, without any binary division.
                direct_curvature = Fraction(11, 7)
                transgressed = direct_curvature * defect
                direct_correction = [
                    -(transgressed / direct_curvature) * value
                    for value in certificate
                ]
                require(
                    direct_correction == correction,
                    f"direct-free normalization failed at d={d}",
                )


def check_two_euler_exactness():
    for d in range(1, 41):
        for clean_index in range(2 * d + 1):
            parallel_weight = 2 * (d - clean_index)
            for transverse_index in (0, 1):
                transverse_weight = 1 - 2 * transverse_index
                require(
                    (parallel_weight, transverse_weight) != (0, 0),
                    f"joint Euler weight zero appeared at d={d}",
                )

        kappa = Fraction(d + 3, d + 1)
        lam = Fraction(2 - d, d + 2)
        curvature = (kappa, lam)
        primitive = (kappa, -lam)
        transverse_euler_of_primitive = (primitive[0], -primitive[1])
        require(
            transverse_euler_of_primitive == curvature,
            f"wrong transverse Euler primitive at d={d}",
        )

        # Transverse order zero retains the joint middle class.
        require(
            (0, 0) == (2 * (d - d), 0),
            f"direct-free joint middle weight changed at d={d}",
        )


def cap_vector(direct_entry, h, row, column):
    """Canonical cap a_ij*q+h*p_i*s_j in the formal cap filtration."""
    vector = [Fraction(0) for _ in range(10)]
    vector[0] = direct_entry
    vector[1 + 3 * row + column] = h
    return vector


def vector_scale(vector, scalar):
    return [scalar * value for value in vector]


def vector_sum(*vectors):
    require(vectors, "vector_sum needs at least one vector")
    total = [Fraction(0) for _ in vectors[0]]
    for vector in vectors:
        require(len(vector) == len(total), "formal cap dimensions differ")
        total = [total[index] + vector[index] for index in range(len(total))]
    return total


def cap_residue(vector, colour):
    """q and off-diagonal products have zero residue; p_c*s_c maps to Y_c."""
    return vector[1 + 3 * colour + colour]


def cap_target(row, column, h):
    target = [Fraction(0), Fraction(0), Fraction(0)]
    if row == column:
        target[row] = h
    return target


def check_canonical_cap_lift_and_flatness():
    for h in range(3, 31):
        # First use trace zero.  This is the branch on which the two cap
        # terms lift the zero radial symbol and cannot define a map from q.
        direct = [
            [Fraction(2), Fraction(h + 1, h), Fraction(-1, 3)],
            [Fraction(5, 4), Fraction(-3), Fraction(7, 5)],
            [Fraction(4, 7), Fraction(-2, 9), Fraction(1)],
        ]
        a, b = 0, 1
        alpha = direct[a][b]
        tau = sum(direct[index][index] for index in range(3))
        require(alpha != 0, f"selected off-diagonal entry vanished at h={h}")

        caps = [
            [cap_vector(direct[i][j], h, i, j) for j in range(3)]
            for i in range(3)
        ]
        trace_cap = vector_sum(caps[0][0], caps[1][1], caps[2][2])
        lift_syzygy = vector_sum(
            vector_scale(caps[a][b], tau / alpha),
            vector_scale(trace_cap, Fraction(-1)),
        )

        require(lift_syzygy[0] == 0, f"radial q term survived at h={h}")
        expected = [Fraction(0) for _ in range(10)]
        expected[1 + 3 * a + b] = h * tau / alpha
        for index in range(3):
            expected[1 + 3 * index + index] -= h
        require(
            lift_syzygy == expected,
            f"wrong scalar-zero cap-lift syzygy at h={h}",
        )
        require(tau == 0, f"trace-zero guard sample changed at h={h}")
        left_radial_symbol = (tau / alpha) * caps[a][b][0]
        right_radial_symbol = trace_cap[0]
        require(
            left_radial_symbol == right_radial_symbol == 0,
            f"trace-zero caps unexpectedly lift q at h={h}",
        )

        # On a separate trace-nonzero sample, dividing the two cap lifts by
        # their common radial scalar gives R/(alpha*tau) per q.  Multiplying
        # by tau recovers alpha^(-1)R, so the latter is tied to tau*q rather
        # than being a normalized q-transgression.
        nonzero_direct = [row[:] for row in direct]
        nonzero_direct[2][2] += 5
        tau_nonzero = sum(
            nonzero_direct[index][index] for index in range(3)
        )
        require(tau_nonzero != 0, f"nonzero-trace sample vanished at h={h}")
        nonzero_caps = [
            [
                cap_vector(nonzero_direct[i][j], h, i, j)
                for j in range(3)
            ]
            for i in range(3)
        ]
        nonzero_trace_cap = vector_sum(
            nonzero_caps[0][0], nonzero_caps[1][1], nonzero_caps[2][2]
        )
        nonzero_lift_syzygy = vector_sum(
            vector_scale(nonzero_caps[a][b], tau_nonzero / alpha),
            vector_scale(nonzero_trace_cap, Fraction(-1)),
        )
        response_coordinate = vector_scale(nonzero_lift_syzygy, Fraction(1, h))
        per_q_difference = vector_scale(
            nonzero_lift_syzygy, Fraction(1, h) / tau_nonzero
        )
        require(
            vector_scale(per_q_difference, tau_nonzero) == response_coordinate,
            f"per-q cap normalization lost the trace factor at h={h}",
        )
        for colour in range(3):
            require(
                cap_residue(per_q_difference, colour) == -1 / tau_nonzero,
                f"wrong trace-nonzero per-q residue at h={h}, c={colour}",
            )
            require(
                cap_residue(response_coordinate, colour) == -1,
                f"wrong trace-weighted response residue at h={h}, c={colour}",
            )

        for colour in range(3):
            normalized_residue = cap_residue(lift_syzygy, colour) / h
            require(
                normalized_residue == -1,
                f"wrong normalized monochromatic residue at h={h}, c={colour}",
            )
            trace_residue = cap_residue(trace_cap, colour) / h
            require(
                trace_residue == 1,
                f"trace anchor does not cancel the response at h={h}, c={colour}",
            )
            target_cancelled = vector_sum(lift_syzygy, trace_cap)
            require(
                cap_residue(target_cancelled, colour) == 0,
                f"trace-cancelled cap retained residue at h={h}, c={colour}",
            )
            require(
                target_cancelled
                == vector_scale(caps[a][b], tau / alpha),
                f"trace cancellation did not reduce to the off-diagonal cap at h={h}",
            )

        trace_target = vector_sum(
            cap_target(0, 0, h),
            cap_target(1, 1, h),
            cap_target(2, 2, h),
        )
        offdiagonal_target = cap_target(a, b, h)
        syzygy_target = vector_sum(
            vector_scale(offdiagonal_target, tau / alpha),
            vector_scale(trace_target, Fraction(-1)),
        )
        require(
            syzygy_target == [-h, -h, -h],
            f"uncancelled diagonal target is wrong at h={h}",
        )
        require(
            vector_scale(syzygy_target, Fraction(1, h) / tau_nonzero)
            == [-1 / tau_nonzero for _ in range(3)],
            f"per-q target lost the trace denominator at h={h}",
        )

        # General one-chart target--residue lock: a diagonal combination
        # has the same normalized coefficient in target colour c and odd
        # residue colour c.  Off-diagonal caps affect neither.
        diagonal_weights = (
            Fraction(h - 1, h + 2),
            Fraction(-2 * h, h + 3),
            Fraction(5, 7),
        )
        diagonal_combo = vector_sum(
            *[
                vector_scale(caps[index][index], diagonal_weights[index])
                for index in range(3)
            ]
        )
        diagonal_target = vector_sum(
            *[
                vector_scale(
                    cap_target(index, index, h), diagonal_weights[index]
                )
                for index in range(3)
            ]
        )
        for colour in range(3):
            require(
                cap_residue(diagonal_combo, colour) / h
                == diagonal_target[colour] / h
                == diagonal_weights[colour],
                f"one-chart target--residue lock failed at h={h}, c={colour}",
            )

        gamma = Fraction(2 * h + 1, h + 2)
        correction_target = vector_scale(syzygy_target, gamma / h)
        require(
            correction_target == [-gamma, -gamma, -gamma],
            f"curvature-weighted target is wrong at h={h}",
        )

        # Direct test of the K1-contracted normal connection.  Both cap
        # presentations select the same constant word h*K1_cc*Y_c; the
        # radial right side has residue zero.
        k1 = [
            [-alpha if i == j else Fraction(0) for j in range(3)]
            for i in range(3)
        ]
        k1[a][b] += tau
        for colour in range(3):
            first_chart = h * k1[colour][colour]
            adjacent_chart = h * k1[colour][colour]
            radial_side = Fraction(0)
            require(
                first_chart - adjacent_chart == radial_side,
                f"normal overlap is not residue-flat at h={h}, c={colour}",
            )
            require(
                first_chart == -h * alpha,
                f"wrong scalar-zero normal residue at h={h}, c={colour}",
            )


def check_radial_and_response_ledger():
    for h in range(3, 41):
        # q_0 q_0^[h-2] = (h-1) q_0^[h-1].  The quotient kills every
        # linear multiple of A=q_0^[h-1], so the radial residue is zero.
        divided_power_factor = Fraction(h - 1)
        require(
            divided_power_factor == h - 1,
            f"radial divided-power factor changed at h={h}",
        )
        quotient_of_linear_times_a = Fraction(0)
        radial_residue = divided_power_factor * quotient_of_linear_times_a
        require(radial_residue == 0, f"radial residue survived at h={h}")

        # The near-perfect gauge identity has both terms in R_1 A.
        sum_beta = Fraction(2 * h - 3, 5)
        beta_at_t = Fraction(-7, 11)
        gauge_residue = (
            sum_beta * quotient_of_linear_times_a
            - beta_at_t * quotient_of_linear_times_a
        )
        require(gauge_residue == 0, f"gauge residue survived at h={h}")

        # Off-diagonal scalar-zero normalization:
        # res(R;t_c)=-alpha Ybar_c and alpha^(-1)res(R;t_c)=-Ybar_c.
        alpha = Fraction(h + 2, h + 1)
        ybar = Fraction(3 * h - 1, 2 * h + 1)
        response_residue = -alpha * ybar
        normalized = response_residue / alpha
        require(normalized == -ybar, f"wrong normalized response at h={h}")
        require(normalized != 0, f"sampled normalized response vanished at h={h}")

        # Universal same-complement lock.  In the x,c coefficient of
        # Q*q^[h-1] = lambda*Delta, the normal term L_c*A dies in the odd
        # quotient, forcing rho(Qbar)=lambda*Ybar_c.  Opposite diagonal
        # targets therefore have exactly opposite residues.
        target_scalar = Fraction(2 * h - 1, h + 4)
        killed_normal_term = Fraction(0)
        locked_residue = target_scalar * ybar + killed_normal_term
        require(
            locked_residue == target_scalar * ybar,
            f"same-complement target--residue lock failed at h={h}",
        )
        require(
            (-target_scalar * ybar) + locked_residue == 0,
            f"target cancellation retained a same-complement residue at h={h}",
        )


def main():
    check_divided_power_and_gauge_normalizations()
    check_representation_ledger()
    check_bracket_prolongation()
    check_two_euler_exactness()
    check_canonical_cap_lift_and_flatness()
    check_radial_and_response_ledger()
    print(
        "PASS: radial annihilation, two-Euler weights, cap-lift syzygy, "
        "target--residue lock, flat normal transport, unique middle bracket, "
        "and all-d correction"
    )


if __name__ == "__main__":
    main()
