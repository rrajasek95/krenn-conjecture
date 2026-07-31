#!/usr/bin/env python3
"""Exact audit for the scalar-unit based-loop moment-lift torsor.

The accompanying proof is uniform in h.  This dependency-free checker
audits the Bernstein identity, the triangular based-loop moment map,
honest reparameterization pullback, legal divided-power multiplication,
and the filtered target-survival countermodel.  ``require`` remains active
under ``python -O``.
"""

from fractions import Fraction
from math import comb, factorial


def require(condition, message):
    """Raise in ordinary and optimized Python."""

    if not condition:
        raise RuntimeError(message)


def expect_failure(callback, label):
    """Require a deterministic mutation to be rejected."""

    try:
        callback()
    except RuntimeError:
        return
    raise RuntimeError(f"mutation was accepted: {label}")


# Polynomials in t, stored in increasing degree.
def clean(poly):
    values = [Fraction(value) for value in poly]
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values) if values else (Fraction(0),)


ZERO = clean((0,))
ONE = clean((1,))
T = clean((0, 1))
ONE_MINUS_T = clean((1, -1))


def poly_add(*polys):
    length = max((len(poly) for poly in polys), default=1)
    output = [Fraction(0)] * length
    for poly in polys:
        for degree, coefficient in enumerate(poly):
            output[degree] += coefficient
    return clean(output)


def poly_scale(poly, scalar):
    scalar = Fraction(scalar)
    return clean(tuple(scalar * coefficient for coefficient in poly))


def poly_mul(left, right):
    output = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, left_coefficient in enumerate(left):
        for j, right_coefficient in enumerate(right):
            output[i + j] += left_coefficient * right_coefficient
    return clean(output)


def poly_pow(poly, exponent):
    require(exponent >= 0, "negative polynomial exponent")
    output = ONE
    base = clean(poly)
    power = exponent
    while power:
        if power & 1:
            output = poly_mul(output, base)
        base = poly_mul(base, base)
        power //= 2
    return output


def poly_derivative(poly, order=1):
    require(order >= 0, "negative derivative order")
    output = clean(poly)
    for _ in range(order):
        if len(output) <= 1:
            output = ZERO
        else:
            output = clean(
                tuple(
                    Fraction(degree) * output[degree]
                    for degree in range(1, len(output))
                )
            )
    return output


def poly_integral_01(poly):
    return sum(
        (
            coefficient / Fraction(degree + 1)
            for degree, coefficient in enumerate(poly)
        ),
        Fraction(0),
    )


def poly_evaluate(poly, value):
    value = Fraction(value)
    answer = Fraction(0)
    for coefficient in reversed(poly):
        answer = answer * value + coefficient
    return answer


def poly_compose(poly, inner):
    output = ZERO
    for coefficient in reversed(clean(poly)):
        output = poly_add(poly_mul(output, inner), (coefficient,))
    return output


def monomial(exponent):
    require(exponent >= 0, "negative monomial exponent")
    return clean((Fraction(0),) * exponent + (Fraction(1),))


def eta(j, *, derivative_delta=0, omit_right_endpoint=False):
    """The based Rodrigues loop eta_j."""

    require(j >= 1, "Rodrigues index must be positive")
    seed = poly_pow(T, j)
    if not omit_right_endpoint:
        seed = poly_mul(seed, poly_pow(ONE_MINUS_T, j))
    return poly_derivative(seed, j - 1 + derivative_delta)


def delta_entry(s, j, **eta_options):
    require(s >= 0 and j >= 1, "bad moment-loop index")
    return poly_integral_01(
        poly_mul(monomial(s), poly_derivative(eta(j, **eta_options)))
    )


def delta_matrix(m, **eta_options):
    require(m >= 1, "empty higher-moment range")
    return [
        [delta_entry(s, j, **eta_options) for j in range(1, m + 1)]
        for s in range(1, m + 1)
    ]


def exact_rank(columns):
    require(bool(columns), "rank called without columns")
    height = len(columns[0])
    require(height > 0, "rank called on empty vectors")
    require(all(len(column) == height for column in columns), "rank height mismatch")
    matrix = [
        [Fraction(columns[column][row]) for column in range(len(columns))]
        for row in range(height)
    ]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next(
            (
                row
                for row in range(pivot_row, height)
                if matrix[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot_value for value in matrix[pivot_row]]
        for row in range(height):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                value - multiple * pivot_entry
                for value, pivot_entry in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == height:
            break
    return pivot_row


def exact_determinant(matrix):
    require(bool(matrix), "determinant called on empty matrix")
    size = len(matrix)
    require(all(len(row) == size for row in matrix), "determinant matrix not square")
    work = [[Fraction(value) for value in row] for row in matrix]
    determinant = Fraction(1)
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column] != 0),
            None,
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant *= pivot_value
        work[column] = [value / pivot_value for value in work[column]]
        for row in range(column + 1, size):
            multiple = work[row][column]
            if multiple == 0:
                continue
            work[row] = [
                value - multiple * pivot_entry
                for value, pivot_entry in zip(work[row], work[column])
            ]
    return determinant


def in_span(target, columns):
    return exact_rank(columns) == exact_rank(columns + [target])


def audit_based_loop_matrix(m, **eta_options):
    matrix = delta_matrix(m, **eta_options)
    for j in range(1, m + 1):
        loop = eta(j, **eta_options)
        require(poly_evaluate(loop, 0) == 0, f"left endpoint failed at j={j}")
        require(poly_evaluate(loop, 1) == 0, f"right endpoint failed at j={j}")
        require(delta_entry(0, j, **eta_options) == 0, f"c0 shifted at j={j}")
        for s in range(1, j):
            require(matrix[s - 1][j - 1] == 0, f"triangular zero failed at ({s},{j})")
        expected_diagonal = Fraction(
            (-1) ** j * factorial(j) ** 3,
            factorial(2 * j + 1),
        )
        require(
            matrix[j - 1][j - 1] == expected_diagonal,
            f"Rodrigues diagonal failed at j={j}",
        )
    require(exact_determinant(matrix) != 0, "based-loop moment map is singular")
    return matrix


def audit_reparameterization(max_j):
    phis = (
        clean((0, 2, -1)),  # 2t-t^2, zero terminal speed
        clean((0, Fraction(1, 2), Fraction(1, 2))),
        clean((0, Fraction(3, 2), Fraction(-1, 2))),
        # Bernstein controls (0,1,0,0,1): interval-valued but non-injective.
        clean((0, 4, -12, 12, -3)),
    )
    require(
        poly_evaluate(poly_derivative(phis[-1]), Fraction(1, 2)) < 0,
        "folding reparameterization lost its fold",
    )
    for phi in phis:
        require(poly_evaluate(phi, 0) == 0, "reparameterization moved t=0")
        require(poly_evaluate(phi, 1) == 1, "reparameterization moved t=1")
        for j in range(1, max_j + 1):
            loop = eta(j)
            pulled_d_loop = poly_derivative(poly_compose(loop, phi))
            for s in range(0, max_j + 1):
                pulled = poly_mul(poly_pow(phi, s), pulled_d_loop)
                require(
                    poly_integral_01(pulled) == delta_entry(s, j),
                    f"honest pullback failed for s={s}, j={j}",
                )


def audit_missing_jacobian_mutation():
    phi = clean((0, 2, -1))
    loop = eta(1)
    honest = poly_mul(phi, poly_derivative(poly_compose(loop, phi)))
    missing_jacobian = poly_mul(phi, poly_compose(poly_derivative(loop), phi))
    require(
        poly_integral_01(honest) != poly_integral_01(missing_jacobian),
        "missing pullback Jacobian escaped detection",
    )


def moment_vector(h, s, *, denominator_shift=1):
    """H_s in q^[n-l]r^[l] order."""

    require(h >= 3 and s >= 0, "bad carrier moment")
    n = h - 2
    return [Fraction(1, s + ell + denominator_shift) for ell in range(n + 1)]


def bernstein_moment_vector(h, s, *, reverse_density=False):
    """Expand the endpoint Bernstein formula back into the q/r DP basis."""

    n = h - 2
    output = [Fraction(0) for _ in range(n + 1)]
    for j in range(n + 1):
        density_j = n - j if reverse_density else j
        beta = Fraction(
            factorial(s + density_j) * factorial(n - density_j),
            factorial(s + n + 1),
        )
        # q^[n-j] (q+r)^[j], expanded in q^[n-l] r^[l].
        for ell in range(j + 1):
            output[ell] += beta * comb(n - ell, n - j)
    return output


def audit_bernstein_identity():
    for h in range(3, 19):
        for s in range(0, min(h, 8)):
            require(
                bernstein_moment_vector(h, s) == moment_vector(h, s),
                f"Bernstein endpoint identity failed at h={h}, s={s}",
            )
    require(
        bernstein_moment_vector(7, 2, reverse_density=True) != moment_vector(7, 2),
        "endpoint reversal did not change a weighted moment",
    )


def audit_moment_denominators(h, *, denominator_shift=1):
    """Compare the claimed moments with independent beta integration."""

    for s in range(0, min(h, 8)):
        require(
            moment_vector(h, s, denominator_shift=denominator_shift)
            == bernstein_moment_vector(h, s),
            f"moment denominator failed at h={h}, s={s}",
        )


def vector_add(*vectors):
    require(bool(vectors), "vector sum without vectors")
    width = len(vectors[0])
    require(all(len(vector) == width for vector in vectors), "vector width mismatch")
    return [
        sum((Fraction(vector[index]) for vector in vectors), Fraction(0))
        for index in range(width)
    ]


def vector_scale(vector, scalar):
    scalar = Fraction(scalar)
    return [scalar * Fraction(value) for value in vector]


def multiply_q(vector, degree, *, weight_delta=0):
    require(len(vector) == degree + 1, "q multiplier input width")
    output = [Fraction(0) for _ in range(degree + 2)]
    for r_degree, coefficient in enumerate(vector):
        output[r_degree] += (degree + 1 - r_degree + weight_delta) * coefficient
    return output


def multiply_r(vector, degree, *, weight_delta=0):
    require(len(vector) == degree + 1, "r multiplier input width")
    output = [Fraction(0) for _ in range(degree + 2)]
    for r_degree, coefficient in enumerate(vector):
        output[r_degree + 1] += (r_degree + 1 + weight_delta) * coefficient
    return output


def audit_divided_power_multiplication(degree, *, weight_delta=0):
    for r_degree in range(degree + 1):
        basis = [Fraction(0) for _ in range(degree + 1)]
        basis[r_degree] = Fraction(1)

        expected_q = [Fraction(0) for _ in range(degree + 2)]
        expected_q[r_degree] = Fraction(degree + 1 - r_degree)
        require(
            multiply_q(basis, degree, weight_delta=weight_delta) == expected_q,
            f"illegal q multiplier at degree={degree}, r-degree={r_degree}",
        )

        expected_r = [Fraction(0) for _ in range(degree + 2)]
        expected_r[r_degree + 1] = Fraction(r_degree + 1)
        require(
            multiply_r(basis, degree, weight_delta=weight_delta) == expected_r,
            f"illegal r multiplier at degree={degree}, r-degree={r_degree}",
        )


def carrier_vector(h, s, *, denominator_shift=1):
    h_s = moment_vector(h, s, denominator_shift=denominator_shift)
    return vector_add(
        multiply_r(h_s, h - 2),
        vector_scale(multiply_q(h_s, h - 2), -2),
    )


def clean_vector(h):
    # Basis order q^[h-j]r^[j].
    return [Fraction(int(j >= 2)) for j in range(h + 1)]


def target_vector(h):
    return [Fraction(int(j in (0, 1))) for j in range(h + 1)]


def required_max_index(h):
    return 1 if h == 3 else h - 3


def density_carrier_coefficient(h, ell):
    """[t^ell] (r-2q)(q+tr)^[h-2] in divided-power order."""

    n = h - 2
    require(0 <= ell <= n, "density coefficient out of range")
    basis = [Fraction(0) for _ in range(n + 1)]
    basis[ell] = Fraction(1)
    return vector_add(
        multiply_r(basis, n),
        vector_scale(multiply_q(basis, n), -2),
    )


def derivative_coefficient_matrix(n):
    """Rows are t-degrees 0..n; columns are eta'_1,...,eta'_n."""

    require(n >= 1, "empty coefficientwise loop space")
    rows = [[Fraction(0) for _ in range(n)] for _ in range(n + 1)]
    for j in range(1, n + 1):
        derivative = poly_derivative(eta(j))
        require(len(derivative) <= n + 1, f"loop derivative too large at j={j}")
        for ell, coefficient in enumerate(derivative):
            rows[ell][j - 1] = coefficient
    return rows


def audit_derivative_kernel(n):
    """Audit image(d:B_n -> K[t]_{<=n}) = kernel(integral)."""

    rows = derivative_coefficient_matrix(n)
    columns = [
        [rows[ell][j] for ell in range(n + 1)]
        for j in range(n)
    ]
    require(exact_rank(columns) == n, f"based derivative lost rank at n={n}")

    integration_weights = [Fraction(1, ell + 1) for ell in range(n + 1)]
    for j, column in enumerate(columns, start=1):
        require(
            sum(
                (
                    integration_weights[ell] * column[ell]
                    for ell in range(n + 1)
                ),
                Fraction(0),
            )
            == 0,
            f"based derivative changed c0 at n={n}, j={j}",
        )

    # Coefficientwise integration recovers the same Rodrigues residues.
    for s in range(0, n + 1):
        weights = [Fraction(1, s + ell + 1) for ell in range(n + 1)]
        for j, column in enumerate(columns, start=1):
            residue = sum(
                (weights[ell] * column[ell] for ell in range(n + 1)),
                Fraction(0),
            )
            require(
                residue == delta_entry(s, j),
                f"coefficient/moment residue mismatch at n={n}, s={s}, j={j}",
            )
    return rows


def c0_boundary_columns(h):
    c0 = carrier_vector(h, 0)
    return [
        clean_vector(h),
        multiply_q(c0, h - 1),
        multiply_r(c0, h - 1),
    ]


def filtered_boundary_columns(h, derivative_rows, *, include_vertical=True):
    """Degree-h coefficient-cell boundaries in (C_h)_0.

    The first block is the q/r divided-power polynomial block.  Each
    vertical z_j block has the independent coordinates q*z_j and r*z_j.
    """

    n = h - 2
    require(
        len(derivative_rows) == n + 1
        and all(len(row) == n for row in derivative_rows),
        "derivative coefficient-matrix size",
    )
    first_width = h + 1
    vertical_width = 2 * n if include_vertical else 0
    total_width = first_width + vertical_width

    def embed_first(vector):
        require(len(vector) == first_width, "first-block width")
        return list(vector) + [Fraction(0) for _ in range(vertical_width)]

    columns = [embed_first(clean_vector(h))]  # u_h=0 in Sbar.
    for ell in range(n + 1):
        c_ell = density_carrier_coefficient(h, ell)
        for multiplier_index, first_part in enumerate(
            (multiply_q(c_ell, h - 1), multiply_r(c_ell, h - 1))
        ):
            column = embed_first(first_part)
            if include_vertical:
                for j in range(n):
                    # z_j is a free shifted S-generator: q*z_j and r*z_j
                    # are named coordinates, with no divided-power rescaling.
                    offset = first_width + 2 * j + multiplier_index
                    column[offset] = derivative_rows[ell][j]
            columns.append(column)
    target = embed_first(target_vector(h))
    return target, columns


def audit_filtered_countermodel(h):
    n = h - 2
    m = required_max_index(h)
    delta = audit_based_loop_matrix(m)
    derivative_rows = audit_derivative_kernel(n)

    # Granting only c0 (and legal q/r multiplication) does not kill x.
    c0_target = target_vector(h)
    c0_only_columns = c0_boundary_columns(h)
    require(
        not in_span(c0_target, c0_only_columns),
        f"c0-only guard lost exceptional target at h={h}",
    )

    # The one coefficientwise source cell integrates to every required
    # moment cell, with the exact vertical Rodrigues residue.
    density_coefficients = [
        density_carrier_coefficient(h, ell) for ell in range(n + 1)
    ]
    for s in range(0, m + 1):
        integrated = [
            sum(
                (
                    density_coefficients[ell][row] / Fraction(s + ell + 1)
                    for ell in range(n + 1)
                ),
                Fraction(0),
            )
            for row in range(h)
        ]
        require(
            integrated == carrier_vector(h, s),
            f"coefficientwise cell lost moment c_{s} at h={h}",
        )
        for j in range(1, m + 1):
            residue = sum(
                (
                    derivative_rows[ell][j - 1] / Fraction(s + ell + 1)
                    for ell in range(n + 1)
                ),
                Fraction(0),
            )
            require(
                residue == (Fraction(0) if s == 0 else delta[s - 1][j - 1]),
                f"wrong integrated lower residue at h={h}, s={s}, j={j}",
            )

    # At the zero-lower-term / associated-graded point the stronger
    # coefficientwise carrier boundary closes the exceptional target.
    gr_target, gr_columns = filtered_boundary_columns(
        h, derivative_rows, include_vertical=False
    )
    require(
        in_span(gr_target, gr_columns),
        f"associated-graded coefficientwise closure failed at h={h}",
    )

    # The universal based-loop coefficient matrix retains x in total.
    total_target, total_columns = filtered_boundary_columns(
        h, derivative_rows, include_vertical=True
    )
    require(
        not in_span(total_target, total_columns),
        f"filtered torsor failed to retain exceptional target at h={h}",
    )


def run_mutation_guards():
    expect_failure(
        lambda: audit_based_loop_matrix(4, derivative_delta=1),
        "wrong Rodrigues derivative order",
    )
    expect_failure(
        lambda: audit_based_loop_matrix(3, omit_right_endpoint=True),
        "missing right endpoint factor",
    )
    expect_failure(
        lambda: audit_moment_denominators(7, denominator_shift=2),
        "shifted moment denominator",
    )
    expect_failure(
        lambda: audit_divided_power_multiplication(6, weight_delta=1),
        "wrong divided-power multiplier weights",
    )

    n = 8 - 2
    derivative_rows = audit_derivative_kernel(n)
    singular = [list(row) for row in derivative_rows]
    for row in singular:
        row[-1] = Fraction(0)
    singular_columns = [
        [singular[ell][j] for ell in range(n + 1)]
        for j in range(n)
    ]
    require(
        exact_rank(singular_columns) < n,
        "missing coefficientwise loop mutation stayed injective",
    )

    # Removing every vertical lower term is detectably the closing point.
    zero = [[Fraction(0) for _ in range(n)] for _ in range(n + 1)]
    target, columns = filtered_boundary_columns(8, zero, include_vertical=True)
    require(in_span(target, columns), "zero-lower-term mutation did not kill target")

    audit_missing_jacobian_mutation()


def main():
    audit_bernstein_identity()
    audit_reparameterization(7)
    for degree in range(0, 18):
        audit_divided_power_multiplication(degree)
    for h in range(3, 19):
        audit_filtered_countermodel(h)
    run_mutation_guards()
    print(
        "scalar-unit moment transgression source-lift based-loop torsor: PASS "
        "(Bernstein, reparametrization, triangular residues, filtered target)"
    )


if __name__ == "__main__":
    main()
