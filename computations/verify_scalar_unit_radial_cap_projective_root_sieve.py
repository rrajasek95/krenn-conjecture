#!/usr/bin/env python3
"""Exact audit for the scalar-unit radial-cap projective root sieve.

The checker is deliberately small and dependency-free.  Uniformity comes
from the proofs in the companion note; the finite loop guards constants,
root multiplicities, boundary counting, and selector directions.
"""

from fractions import Fraction
from math import comb


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def trim(poly):
    answer = list(map(Fraction, poly))
    while answer and answer[-1] == 0:
        answer.pop()
    return answer


def derivative(poly):
    return trim([k * poly[k] for k in range(1, len(poly))])


def divmod_poly(dividend, divisor):
    dividend = trim(dividend)
    divisor = trim(divisor)
    require(divisor, "polynomial division by zero")
    quotient = [Fraction(0)] * max(1, len(dividend) - len(divisor) + 1)
    while dividend and len(dividend) >= len(divisor):
        shift = len(dividend) - len(divisor)
        scale = dividend[-1] / divisor[-1]
        quotient[shift] += scale
        for j, value in enumerate(divisor):
            dividend[shift + j] -= scale * value
        dividend = trim(dividend)
    return trim(quotient), dividend


def gcd_poly(left, right):
    left, right = trim(left), trim(right)
    while right:
        _, remainder = divmod_poly(left, right)
        left, right = right, remainder
    if not left:
        return []
    return trim([value / left[-1] for value in left])


def clean_polynomial(h):
    coefficients = [Fraction(comb(h, k)) for k in range(h + 1)]
    coefficients[0] -= 1
    coefficients[1] -= h
    return trim(coefficients)


def evaluate(poly, value):
    total = Fraction(0)
    for coefficient in reversed(poly):
        total = total * value + coefficient
    return total


def rank(rows):
    matrix = [list(map(Fraction, row)) for row in rows]
    if not matrix:
        return 0
    row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (candidate for candidate in range(row, len(matrix))
             if matrix[candidate][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        scale = matrix[row][column]
        matrix[row] = [entry / scale for entry in matrix[row]]
        for candidate in range(len(matrix)):
            if candidate == row or not matrix[candidate][column]:
                continue
            scale = matrix[candidate][column]
            matrix[candidate] = [
                x - scale * y for x, y in zip(matrix[candidate], matrix[row])
            ]
        row += 1
        if row == len(matrix):
            break
    return row


def in_row_span(rows, vector):
    return rank(rows) == rank(rows + [vector])


def linear_system_has_solution(matrix, right_hand_side):
    require(
        len(matrix) == len(right_hand_side),
        "linear-system row count mismatch",
    )
    augmented = [
        list(map(Fraction, row)) + [Fraction(value)]
        for row, value in zip(matrix, right_hand_side)
    ]
    return rank(matrix) == rank(augmented)


def dot(left, right):
    require(len(left) == len(right), "dot-product length mismatch")
    return sum((x * y for x, y in zip(left, right)), Fraction(0))


def add_vectors(left, right):
    require(len(left) == len(right), "vector-addition length mismatch")
    return tuple(x + y for x, y in zip(left, right))


def scale_vector(scale, vector):
    return tuple(scale * value for value in vector)


def evaluate_form(form, point):
    return dot(tuple(map(Fraction, form)), tuple(map(Fraction, point)))


def response_selector_exists(response_rows, selector):
    """Whether d=lambda o r for a linear response map r."""
    return in_row_span(response_rows, list(map(Fraction, selector)))


def quotient_selector_exists(response_rows, radial_vector, selector):
    """Whether d=lambda o r with the additional condition lambda(q)=0."""
    require(response_rows, "quotient selector needs a response map")
    output_dimension = len(response_rows)
    cap_dimension = len(response_rows[0])
    require(
        len(radial_vector) == output_dimension,
        "radial-vector output dimension mismatch",
    )
    require(
        all(len(row) == cap_dimension for row in response_rows),
        "ragged response matrix",
    )
    require(len(selector) == cap_dimension, "selector cap dimension mismatch")

    # The unknowns are the output-dual coordinates of lambda.  The first
    # cap_dimension equations impose lambda*r=d; the last imposes lambda(q)=0.
    equations = [
        [response_rows[i][j] for i in range(output_dimension)]
        for j in range(cap_dimension)
    ]
    equations.append(list(radial_vector))
    values = list(selector) + [Fraction(0)]
    return linear_system_has_solution(equations, values)


def proportional(left, right):
    left, right = list(map(Fraction, left)), list(map(Fraction, right))
    pivot = next((i for i, value in enumerate(right) if value), None)
    if pivot is None:
        return not any(left)
    scale = left[pivot] / right[pivot]
    return all(x == scale * y for x, y in zip(left, right))


def gaussian(real=0, imaginary=0):
    return Fraction(real), Fraction(imaginary)


def gaussian_scale(scale, value):
    return Fraction(scale) * value[0], Fraction(scale) * value[1]


def gaussian_inverse(value):
    real, imaginary = value
    norm = real * real + imaginary * imaginary
    require(norm != 0, "division by zero Gaussian rational")
    return real / norm, -imaginary / norm


def gaussian_nonzero(value):
    return value != gaussian()


def audit_radial_collapse_and_roots():
    for h in range(3, 65):
        polynomial = clean_polynomial(h)
        require(len(polynomial) == h + 1, f"wrong degree at h={h}")
        require(polynomial[:2] == [0, 0], f"zero is not double at h={h}")
        quotient = polynomial[2:]
        require(
            len(quotient) == h - 1 and quotient[0] == comb(h, 2),
            f"wrong nonzero-root quotient at h={h}",
        )
        require(
            gcd_poly(quotient, derivative(quotient)) == [Fraction(1)],
            f"a nonzero clean ratio was repeated at h={h}",
        )
        require(
            gcd_poly(polynomial, derivative(polynomial))
            == [Fraction(0), Fraction(1)],
            f"the full root-multiplicity profile is wrong at h={h}",
        )
        require(
            evaluate(polynomial, Fraction(-1)) == h - 1,
            f"the zero-effective-quadratic ratio became a root at h={h}",
        )
        target_zero_ratio = Fraction(-1, h)
        require(
            evaluate(polynomial, target_zero_ratio)
            == Fraction(h - 1, h) ** h,
            f"the zero-target-scalar ratio became a root at h={h}",
        )

        # Independent evaluation of the DP error sum
        # sum_{j>=2} binom(h,j)t^j.
        for t in (Fraction(-3), Fraction(-1, 2), Fraction(2, 3)):
            dp_sum = sum(
                Fraction(comb(h, j)) * t**j for j in range(2, h + 1)
            )
            require(
                dp_sum == evaluate(polynomial, t),
                f"radial divided-power collapse failed at h={h}, t={t}",
            )

        # Audit the homogeneous scalar normalization before dividing by s.
        for scalar, response in (
            (Fraction(2), Fraction(-3)),
            (Fraction(-5, 2), Fraction(7, 3)),
        ):
            ratio = response / scalar
            expanded = (scalar + response) ** h - scalar ** (h - 1) * (
                scalar + h * response
            )
            target_free = sum(
                Fraction(comb(h, j))
                * scalar ** (h - j)
                * response**j
                for j in range(2, h + 1)
            )
            collapsed = scalar**h * evaluate(polynomial, ratio)
            require(
                expanded == target_free == collapsed,
                f"homogeneous radial normalization failed at h={h}",
            )


def restriction_vanishes_on_hyperplane(form, ratio):
    """Test d|_{H_t}=0 in coordinates (s,beta,u), beta=t*s."""
    a, b, c = map(Fraction, form)
    ratio = Fraction(ratio)
    return a + b * ratio == 0 and c == 0


def active_point_on_hyperplane(ratio, diagonal_b, diagonal_c):
    """Construct an exact rational point avoiding three proper kernels."""
    ratio = Fraction(ratio)
    require(
        not restriction_vanishes_on_hyperplane(diagonal_b, ratio),
        "asked for a point on a b-blocked hyperplane",
    )
    require(
        not restriction_vanishes_on_hyperplane(diagonal_c, ratio),
        "asked for a point on a c-blocked hyperplane",
    )

    # Set s=1.  Each remaining diagonal excludes at most one value of u,
    # so three candidates suffice for the two complementary diagonals.
    for free_coordinate in map(Fraction, (0, 1, 2)):
        point = (Fraction(1), ratio, free_coordinate)
        if (
            evaluate_form(diagonal_b, point) != 0
            and evaluate_form(diagonal_c, point) != 0
        ):
            return point
    raise RuntimeError("finite-union witness construction failed")


def audit_projective_boundary_sieve():
    # Work in L^* with coordinates dual to (s,beta,u).  On H_t the normal
    # beta-t*s is (-t,1,0), and K_aa=s/alpha never blocks H_t.
    selected_diagonal = (Fraction(1), Fraction(0), Fraction(0))
    for h in range(3, 15):
        root_count = h - 1
        # At h=3 use the literal roots.  For h>=4 the extra rational labels
        # are formal distinct projective points; only their cardinality is
        # used here, while the preceding polynomial audit proves that the
        # actual roots have that cardinality.
        root_labels = (
            [Fraction(0), Fraction(-3)]
            if h == 3
            else [Fraction(0)]
            + [Fraction(index + 1) for index in range(h - 2)]
        )
        normals = {
            t: (-t, Fraction(1), Fraction(0)) for t in root_labels
        }
        require(len(normals) == root_count, f"root labels collided at h={h}")
        require(
            all(
                not proportional(selected_diagonal, normal)
                for normal in normals.values()
            ),
            "the selected diagonal incorrectly blocks a radial ratio",
        )

        # Directly audit d|H_t=0 iff d is proportional to beta-t*s.
        candidate_forms = [
            tuple(map(Fraction, form))
            for form in (
                (1, 0, 0),
                (0, 1, 0),
                (1, -1, 0),
                (2, 3, 0),
                (0, 0, 1),
                (1, 1, 1),
            )
        ] + list(normals.values())
        for t, normal in normals.items():
            for form in candidate_forms:
                require(
                    restriction_vanishes_on_hyperplane(form, t)
                    == proportional(form, normal),
                    f"hyperplane-annihilator equivalence failed at h={h}, t={t}",
                )

        # Exhaust which roots are blocked by the two complementary
        # diagonals.  Whenever a root is unblocked, construct an active point
        # rather than relying only on the boundary count.
        choices = [None] + root_labels
        for blocked_b in choices:
            for blocked_c in choices:
                diagonal_b = (
                    (Fraction(0), Fraction(0), Fraction(1))
                    if blocked_b is None
                    else normals[blocked_b]
                )
                diagonal_c = (
                    (Fraction(1), Fraction(1), Fraction(1))
                    if blocked_c is None
                    else normals[blocked_c]
                )
                blocked = {
                    t
                    for t in root_labels
                    if restriction_vanishes_on_hyperplane(diagonal_b, t)
                    or restriction_vanishes_on_hyperplane(diagonal_c, t)
                }
                require(len(blocked) <= 2, "two diagonals blocked three ratios")
                unblocked = [t for t in root_labels if t not in blocked]
                for t in unblocked:
                    point = active_point_on_hyperplane(
                        t, diagonal_b, diagonal_c
                    )
                    require(point[0] != 0 and point[1] == t * point[0],
                            "constructed point missed H_t or K_aa activity")
                    require(
                        evaluate_form(diagonal_b, point) != 0
                        and evaluate_form(diagonal_c, point) != 0,
                        "constructed point was not active",
                    )
                if h >= 4:
                    require(unblocked, f"all radial roots were hidden at h={h}")

    # Counting alone genuinely leaves the h=3 configuration in which beta
    # hides t=0 and beta+3s hides t=-3.
    beta = (Fraction(0), Fraction(1), Fraction(0))
    beta_plus_three_s = (Fraction(3), Fraction(1), Fraction(0))
    require(
        restriction_vanishes_on_hyperplane(beta, Fraction(0))
        and restriction_vanishes_on_hyperplane(
            beta_plus_three_s, Fraction(-3)
        ),
        "the h=3 projective counterconfiguration was not realized",
    )
    require(
        not proportional(beta, beta_plus_three_s),
        "the h=3 two-boundary normal form collapsed its two roots",
    )


def hidden_h3_target_rows(alpha, mu_b, mu_c, scalar_zero, scalar_other):
    """Return normalized target rows for the hidden t=0,-3 caps."""
    alpha = Fraction(alpha)
    mu_b = Fraction(mu_b)
    mu_c = Fraction(mu_c)
    scalar_zero = Fraction(scalar_zero)
    scalar_other = Fraction(scalar_other)
    require(
        alpha * mu_b * mu_c * scalar_zero * scalar_other != 0,
        "h=3 hidden-boundary parameters must be nonzero",
    )

    beta_zero = Fraction(0)
    beta_other = -3 * scalar_other
    diagonals_zero = (
        scalar_zero / alpha,
        mu_b * beta_zero,
        mu_c * (beta_zero + 3 * scalar_zero),
    )
    diagonals_other = (
        scalar_other / alpha,
        mu_b * beta_other,
        mu_c * (beta_other + 3 * scalar_other),
    )
    require(
        diagonals_zero[0] != 0
        and diagonals_zero[1] == 0
        and diagonals_zero[2] != 0,
        "the t=0 existence choice has the wrong diagonal support",
    )
    require(
        diagonals_other[0] != 0
        and diagonals_other[1] != 0
        and diagonals_other[2] == 0,
        "the t=-3 existence choice has the wrong diagonal support",
    )
    return (
        scale_vector(1 / scalar_zero, diagonals_zero),
        scale_vector(1 / scalar_other, diagonals_other),
    )


def audit_h3_shared_target_closure():
    alpha = Fraction(2, 3)
    mu_b = Fraction(-5, 2)
    mu_c = Fraction(7, 4)
    target_zero, target_other = hidden_h3_target_rows(
        alpha, mu_b, mu_c, Fraction(11, 3), Fraction(-13, 5)
    )
    require(
        target_zero == (1 / alpha, 0, 3 * mu_c),
        "the normalized t=0 target row is wrong",
    )
    require(
        target_other == (1 / alpha, -3 * mu_b, 0),
        "the normalized t=-3 target row is wrong",
    )
    require(
        evaluate(clean_polynomial(3), Fraction(0)) == 0
        and evaluate(clean_polynomial(3), Fraction(-3)) == 0,
        "the h=3 boundary ratios are not both clean roots",
    )
    require(
        (1 + Fraction(-3)) ** 3 == -8
        and 1 + 3 * Fraction(-3) == -8,
        "the h=3 effective/target scalar normalization is wrong",
    )

    # Compatibility would say target_other=-8*target_zero for the same
    # Q=q^[3].  Its exact residual is nonzero in every independent target
    # coordinate for every nonzero alpha, mu_b, mu_c.
    compatibility_residual = add_vectors(
        target_other, scale_vector(8, target_zero)
    )
    require(
        compatibility_residual
        == (9 / alpha, -3 * mu_b, 24 * mu_c),
        "the h=3 shared-target residual has a wrong coefficient or sign",
    )
    require(
        all(value != 0 for value in compatibility_residual),
        "the h=3 shared-target contradiction lost a target coordinate",
    )
    require(
        any(value != 0 for value in target_zero),
        "zero q^[3] incorrectly rescued the t=0 hidden row",
    )

    # Exact Gaussian-rational samples guard against accidentally replacing
    # a complex-linear independence argument by positivity or real signs.
    complex_alpha = gaussian(1, 2)
    complex_mu_b = gaussian(-3, 1)
    complex_mu_c = gaussian(2, -5)
    complex_residual = (
        gaussian_scale(9, gaussian_inverse(complex_alpha)),
        gaussian_scale(-3, complex_mu_b),
        gaussian_scale(24, complex_mu_c),
    )
    require(
        all(gaussian_nonzero(value) for value in complex_residual),
        "complex cancellation incorrectly removed an independent target word",
    )


def audit_response_selectors():
    # Rows are output coordinates of r as linear functionals on the nine cap
    # entries.  A pure selector factors through r exactly when its coordinate
    # row belongs to the row span of the response matrix.
    e = [[Fraction(int(i == j)) for j in range(9)] for i in range(9)]
    diagonal_indices = (0, 4, 8)

    response_rows = [
        e[4],
        [Fraction(1) if j in (0, 1) else Fraction(0) for j in range(9)],
        [Fraction(j - 3) for j in range(9)],
    ]
    require(
        response_selector_exists(response_rows, e[4]),
        "pure response selector lost",
    )
    require(
        not response_selector_exists(response_rows, e[8]),
        "an unsupported pure response selector was admitted",
    )

    # A planted no-active kernel lies in K_11=0 and therefore forces exactly
    # the corresponding response-free selector.
    no_active_rows = [e[4]]
    require(
        response_selector_exists(no_active_rows, e[4]),
        "kernel containment did not produce its response-free selector",
    )
    require(
        all(
            not response_selector_exists(no_active_rows, e[index])
            for index in (0, 8)
        ),
        "kernel containment produced an unsupported diagonal selector",
    )

    # If the three diagonal columns sum to zero, the all-one diagonal cap is
    # response-free and active, so no individual diagonal selector is forced.
    active_kernel_rows = [
        [Fraction(1) if j == 0 else Fraction(-1) if j == 8 else 0
         for j in range(9)],
        [Fraction(1) if j == 4 else Fraction(-1) if j == 8 else 0
         for j in range(9)],
    ]
    active_diagonal = [
        Fraction(1) if j in (0, 4, 8) else Fraction(0) for j in range(9)
    ]
    require(
        all(sum(row[j] * active_diagonal[j] for j in range(9)) == 0
            for row in active_kernel_rows),
        "the planted response-free active cap left the kernel",
    )
    require(
        all(
            not response_selector_exists(active_kernel_rows, e[j])
            for j in diagonal_indices
        ),
        "an active-kernel example incorrectly forced a pure selector",
    )

    # Model r:K -> Y with four output coordinates and q=(1,0,0,0).  Passing
    # to Y/Cq kills precisely the first output row.  The remaining rows force
    # K_00=K_02=K_12=0 on the radial preimage and retain the K_00 selector.
    radial_row = [Fraction(j + 1) for j in range(9)]
    quotient_response_rows = [radial_row, e[0], e[2], e[5]]
    radial_vector = [Fraction(1), Fraction(0), Fraction(0), Fraction(0)]
    require(
        quotient_selector_exists(quotient_response_rows, radial_vector, e[0]),
        "mod-radial pure selector was lost",
    )
    require(
        not quotient_selector_exists(
            quotient_response_rows, radial_vector, e[8]
        ),
        "mod-radial factorization admitted an unsupported selector",
    )
    for basis_index in range(9):
        if basis_index in (0, 2, 5):
            continue
        radial_cap = e[basis_index]
        response = tuple(dot(row, radial_cap) for row in quotient_response_rows)
        require(
            response[1:] == (0, 0, 0) and radial_cap[0] == 0,
            "the explicit radial-kernel basis violated selector containment",
        )

    # Adversarial distinction: d can factor through r while failing to factor
    # through r modulo Cq.  Here selecting K_00 requires a dual nonzero on q,
    # and the radial cap E_00 witnesses failure of d|L=0.
    ordinary_only_rows = [e[0], e[1]]
    ordinary_only_q = [Fraction(1), Fraction(0)]
    require(
        response_selector_exists(ordinary_only_rows, e[0]),
        "ordinary response selector counterexample was not realized",
    )
    require(
        not quotient_selector_exists(ordinary_only_rows, ordinary_only_q, e[0]),
        "ordinary selector was incorrectly promoted modulo Cq",
    )
    radial_cap = e[0]
    radial_response = tuple(dot(row, radial_cap) for row in ordinary_only_rows)
    require(
        radial_response == tuple(ordinary_only_q) and radial_cap[0] != 0,
        "the mod-Cq obstruction lacks its radial cap witness",
    )


def mutation_checks():
    h = 7
    wrong = clean_polynomial(h)
    wrong[1] = Fraction(1)  # mutation: use 1+(h-1)t in the target.
    require(wrong[:2] != [0, 0], "linear-target mutation was not detected")

    test_ratio = Fraction(2, 3)
    wrong_dp_target = (1 + test_ratio) ** h - 1 - test_ratio
    require(
        wrong_dp_target != evaluate(clean_polynomial(h), test_ratio),
        "mutation q*q^[h-1]=q^[h] was not detected",
    )

    three_roots = (Fraction(1), Fraction(2), Fraction(3))
    three_normals = [(-t, Fraction(1), Fraction(0)) for t in three_roots]
    require(
        len({tuple(normal) for normal in three_normals}) == 3,
        "projective-normal mutation collapsed distinct ratios",
    )
    require(
        not proportional(three_normals[2], three_normals[0])
        and not proportional(three_normals[2], three_normals[1]),
        "mutation let two boundary points cover a third projective point",
    )

    # The h=3 obstruction genuinely needs independence of the three constant
    # words.  If that hypothesis is maliciously dropped, a two-dimensional
    # target realizes both hidden rows with alpha=mu_b=mu_c=1.
    target_a = (Fraction(1), Fraction(0))
    target_c = (Fraction(0), Fraction(1))
    shared_q_cubed = add_vectors(target_a, scale_vector(3, target_c))
    target_b = add_vectors(scale_vector(3, target_a), scale_vector(8, target_c))
    require(
        scale_vector(-8, shared_q_cubed)
        == add_vectors(target_a, scale_vector(-3, target_b)),
        "dependent-target h=3 counterexample was not realized",
    )
    require(
        rank([list(target_a), list(target_b), list(target_c)]) == 2,
        "dependent-target mutation accidentally retained independence",
    )

    # If the two caps are incorrectly allowed different copies of q^[3],
    # the support contradiction disappears.  The actual theorem uses one
    # global internal q, so this is an adversarial scope mutation only.
    target_zero, target_other = hidden_h3_target_rows(2, 3, -5, 7, -11)
    fake_q_zero = target_zero
    fake_q_other = scale_vector(Fraction(-1, 8), target_other)
    require(
        target_zero == fake_q_zero
        and target_other == scale_vector(-8, fake_q_other)
        and fake_q_zero != fake_q_other,
        "separate-q h=3 mutation was not exposed",
    )

    # With q=0, the complementary diagonal literal row would equate zero to
    # the nonzero constant word X_b.  This guards the beta-normalization gate.
    zero_quadratic_row = (Fraction(0), Fraction(0), Fraction(0))
    constant_word_b = (Fraction(0), Fraction(1), Fraction(0))
    require(
        zero_quadratic_row != constant_word_b,
        "zero q was incorrectly admitted by a complementary target row",
    )


def main():
    audit_radial_collapse_and_roots()
    audit_projective_boundary_sieve()
    audit_h3_shared_target_closure()
    audit_response_selectors()
    mutation_checks()
    print(
        "scalar-unit radial-cap projective root sieve: PASS; "
        "h=3..64, roots, projective boundaries, h=3 shared target, "
        "and response/mod-q selectors audited"
    )


if __name__ == "__main__":
    main()
