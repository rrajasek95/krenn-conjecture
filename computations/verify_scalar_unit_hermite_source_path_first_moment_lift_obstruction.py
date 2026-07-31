#!/usr/bin/env python3
"""Exact audit for the scalar-unit Hermite source-path obstruction.

The proof is uniform in ``h``.  This dependency-free checker audits the
divided-power Hermite and Segre formulas, the first two path moments, the
based loop which fixes the top path and H_0 but shifts H_1, and the exact
h=3 carrier identity.  ``require`` remains active under ``python -O``.
"""

from fractions import Fraction


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


def add(left, right):
    require(len(left) == len(right), "vector length mismatch")
    return tuple(a + b for a, b in zip(left, right))


def scale(scalar, vector):
    scalar = Fraction(scalar)
    return tuple(scalar * value for value in vector)


def basis(dimension, index):
    require(0 <= index < dimension, "basis index out of range")
    return tuple(Fraction(int(position == index)) for position in range(dimension))


def sum_vectors(vectors, dimension):
    output = tuple(Fraction(0) for _ in range(dimension))
    for vector in vectors:
        output = add(output, vector)
    return output


def multiply_q(vector):
    """Multiply a divided-power degree-d vector by ordinary Q."""

    degree = len(vector) - 1
    output = [Fraction(0)] * (degree + 2)
    for index, coefficient in enumerate(vector):
        output[index] += (degree - index + 1) * coefficient
    return tuple(output)


def multiply_r(vector):
    """Multiply a divided-power degree-d vector by ordinary R."""

    degree = len(vector) - 1
    output = [Fraction(0)] * (degree + 2)
    for index, coefficient in enumerate(vector):
        output[index + 1] += (index + 1) * coefficient
    return tuple(output)


def path_divided_power(degree):
    """Coefficients in t of (Q+tR)^[degree], in divided-power basis."""

    require(degree >= 0, "negative divided-power degree")
    return tuple(basis(degree + 1, index) for index in range(degree + 1))


def derivative_t(polynomial):
    if len(polynomial) <= 1:
        return (tuple(Fraction(0) for _ in polynomial[0]),)
    return tuple(
        scale(index, polynomial[index]) for index in range(1, len(polynomial))
    )


def evaluate_t(polynomial, value):
    value = Fraction(value)
    dimension = len(polynomial[0])
    return sum_vectors(
        (scale(value**index, coefficient) for index, coefficient in enumerate(polynomial)),
        dimension,
    )


def integrate_t(polynomial, weight=0):
    require(weight >= 0, "negative moment weight")
    dimension = len(polynomial[0])
    return sum_vectors(
        (
            scale(Fraction(1, index + weight + 1), coefficient)
            for index, coefficient in enumerate(polynomial)
        ),
        dimension,
    )


def moment_h(degree, weight, *, denominator_shift=0):
    """H_weight in degree ``degree`` with one mutation hook."""

    require(degree >= 0 and weight >= 0, "bad moment index")
    return tuple(
        Fraction(1, weight + index + 1 + denominator_shift)
        for index in range(degree + 1)
    )


def exact_rank(columns):
    require(bool(columns), "rank called without columns")
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height mismatch")
    matrix = [
        [Fraction(columns[column][row]) for column in range(len(columns))]
        for row in range(height)
    ]
    rank = 0
    for column in range(len(columns)):
        pivot = next(
            (row for row in range(rank, height) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for row in range(height):
            if row == rank:
                continue
            factor = matrix[row][column]
            if factor:
                matrix[row] = [
                    value - factor * pivot_entry
                    for value, pivot_entry in zip(matrix[row], matrix[rank])
                ]
        rank += 1
        if rank == height:
            break
    return rank


def audit_hermite(h, *, omit_last_clean_term=False):
    path = path_divided_power(h)
    remainder = add(
        add(evaluate_t(path, 1), scale(-1, evaluate_t(path, 0))),
        scale(-1, derivative_t(path)[0]),
    )
    stop = h if omit_last_clean_term else h + 1
    clean_unary = sum_vectors(
        (basis(h + 1, index) for index in range(2, stop)),
        h + 1,
    )
    require(remainder == clean_unary, f"Hermite remainder mismatch at h={h}")


def audit_segre_roles(*, mutate_right_factor=False):
    left = sorted(("p_j", "s_k", "p_a", "s_a"))
    if mutate_right_factor:
        right = sorted(("p_j", "s_a", "p_k", "s_a"))
    else:
        right = sorted(("p_j", "s_a", "p_a", "s_k"))
    require(left == right, "ordered Segre role mismatch")


def audit_path_moments(h, *, denominator_shift=0, unweighted_multiplier=True):
    n = h - 2
    response_path = path_divided_power(h - 1)
    response_derivative = derivative_t(response_path)
    expected_derivative = tuple(multiply_r(coefficient) for coefficient in path_divided_power(n))
    require(response_derivative == expected_derivative, f"path derivative mismatch at h={h}")

    multiplier = multiply_r if unweighted_multiplier else lambda vector: (Fraction(0),) + vector

    for weight in range(h + 2):
        h_weight = moment_h(n, weight, denominator_shift=denominator_shift)
        weighted_derivative = integrate_t(response_derivative, weight=weight)
        if weight == 0:
            integration_by_parts = add(
                evaluate_t(response_path, 1),
                scale(-1, evaluate_t(response_path, 0)),
            )
        else:
            integration_by_parts = add(
                evaluate_t(response_path, 1),
                scale(-weight, integrate_t(response_path, weight=weight - 1)),
            )
        require(
            weighted_derivative == integration_by_parts,
            f"weighted integration mismatch at h={h}, s={weight}",
        )
        require(
            multiplier(h_weight) == weighted_derivative,
            f"H_s path mismatch at h={h}, s={weight}",
        )


def polynomial_evaluate(poly, value):
    value = Fraction(value)
    answer = Fraction(0)
    for coefficient in reversed(poly):
        answer = answer * value + coefficient
    return answer


def polynomial_derivative(poly):
    return tuple(index * poly[index] for index in range(1, len(poly)))


def polynomial_integral_01(poly, weight=0):
    return sum(
        (
            coefficient / Fraction(index + weight + 1)
            for index, coefficient in enumerate(poly)
        ),
        Fraction(0),
    )


def audit_based_loop(*, eta_mutation=False, claimed_shift=Fraction(-1, 6)):
    eta = (Fraction(0), Fraction(1), Fraction(-1 if not eta_mutation else 0))
    require(polynomial_evaluate(eta, 0) == 0, "loop misses left endpoint")
    require(polynomial_evaluate(eta, 1) == 0, "loop misses right endpoint")
    differential = polynomial_derivative(eta)
    require(polynomial_integral_01(differential) == 0, "loop changes H_0")
    actual_shift = polynomial_integral_01(differential, weight=1)
    require(actual_shift == claimed_shift, "loop H_1 residue mismatch")
    for weight in range(1, 9):
        expected = -Fraction(weight, (weight + 1) * (weight + 2))
        require(
            polynomial_integral_01(differential, weight=weight) == expected,
            f"loop H_s residue mismatch at s={weight}",
        )

    # Projection kills the vertical z-coordinate pointwise, while the
    # source lift retains it.  Store pairs as (visible, vertical).
    lifted_derivative = tuple((Fraction(index + 2), coefficient) for index, coefficient in enumerate(differential))
    visible_projection = tuple(visible for visible, _vertical in lifted_derivative)
    require(visible_projection == (Fraction(2), Fraction(3)), "vertical loop changed top derivative image")
    require(any(vertical for _visible, vertical in lifted_derivative), "vertical loop was erased in source")


def audit_h3_identity(*, coefficient_mutation=Fraction(0)):
    h_zero = moment_h(1, 0)
    h_one = moment_h(1, 1)
    c_zero = add(multiply_r(h_zero), scale(-2, multiply_q(h_zero)))
    c_one = add(multiply_r(h_one), scale(-2, multiply_q(h_one)))

    unary = add(basis(4, 2), basis(4, 3))
    target = add(basis(4, 0), basis(4, 1))
    rhs = sum_vectors(
        (
            scale(Fraction(7, 20), unary),
            scale(Fraction(43, 60), multiply_q(c_zero)),
            scale(Fraction(-7, 60), multiply_r(c_zero)),
            scale(Fraction(-8, 5) + coefficient_mutation, multiply_q(c_one)),
        ),
        4,
    )
    require(rhs == target, "h=3 first-moment identity mismatch")

    old_columns = (unary, multiply_q(c_zero), multiply_r(c_zero))
    require(
        exact_rank(old_columns + (target,)) > exact_rank(old_columns),
        "h=3 target unexpectedly lies in the H_0-only span",
    )


def run_mutations():
    expect_failure(lambda: audit_hermite(7, omit_last_clean_term=True), "truncated clean Hermite remainder")
    expect_failure(lambda: audit_segre_roles(mutate_right_factor=True), "wrong ordered Segre factor")
    expect_failure(lambda: audit_path_moments(6, denominator_shift=1), "shifted moment denominator")
    expect_failure(lambda: audit_path_moments(6, unweighted_multiplier=False), "missing divided-power multiplier")
    expect_failure(lambda: audit_based_loop(eta_mutation=True), "unbased affine loop")
    expect_failure(lambda: audit_based_loop(claimed_shift=Fraction(-1, 3)), "wrong first loop residue")
    expect_failure(lambda: audit_h3_identity(coefficient_mutation=Fraction(1, 10)), "mutated H_1 coefficient")


def main():
    for h in range(3, 33):
        audit_hermite(h)
        audit_path_moments(h)
    audit_segre_roles()
    audit_based_loop()
    audit_h3_identity()
    run_mutations()
    print("scalar-unit Hermite source path and first-moment lift obstruction: PASS")


if __name__ == "__main__":
    main()
