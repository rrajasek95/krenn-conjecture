#!/usr/bin/env python3
"""Exact audit of the scalar-unit carrier moment-tower lemma.

The degree-(h-1) carrier rows are c_s=(r-2q)H_s.  Their degree-h
consequences are q*c_s and r*c_s.  All divided-power and ordinary-basis
calculations below use only Python's standard library.
"""

from fractions import Fraction
from math import comb, factorial


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def exact_rank(columns: list[list[Fraction]]) -> int:
    require(bool(columns), "rank called without columns")
    height = len(columns[0])
    require(height > 0, "rank called on empty vectors")
    require(
        all(len(column) == height for column in columns),
        "rank column-height mismatch",
    )
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


def in_span(target: list[Fraction], columns: list[list[Fraction]]) -> bool:
    return exact_rank(columns) == exact_rank(columns + [target])


def exact_determinant(columns: list[list[Fraction]]) -> Fraction:
    require(bool(columns), "determinant called without columns")
    size = len(columns)
    require(all(len(column) == size for column in columns), "determinant is not square")
    matrix = [
        [Fraction(columns[column][row]) for column in range(size)]
        for row in range(size)
    ]
    determinant = Fraction(1)
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if matrix[row][column] != 0),
            None,
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            determinant = -determinant
        pivot_value = matrix[column][column]
        determinant *= pivot_value
        matrix[column] = [value / pivot_value for value in matrix[column]]
        for row in range(column + 1, size):
            multiple = matrix[row][column]
            if multiple == 0:
                continue
            matrix[row] = [
                value - multiple * pivot_entry
                for value, pivot_entry in zip(matrix[row], matrix[column])
            ]
    return determinant


def add_vectors(*vectors: list[Fraction]) -> list[Fraction]:
    require(bool(vectors), "vector sum called without vectors")
    width = len(vectors[0])
    require(all(len(vector) == width for vector in vectors), "vector width mismatch")
    return [sum((vector[index] for vector in vectors), Fraction(0)) for index in range(width)]


def multiply_q(
    coefficients: list[Fraction], degree: int, *, weight_delta: int = 0
) -> list[Fraction]:
    """Multiply a degree-`degree` divided-power vector by ordinary q."""
    require(len(coefficients) == degree + 1, "q-product input width")
    answer = [Fraction(0) for _ in range(degree + 2)]
    for r_degree, coefficient in enumerate(coefficients):
        answer[r_degree] += (degree + 1 - r_degree + weight_delta) * coefficient
    return answer


def multiply_r(
    coefficients: list[Fraction], degree: int, *, weight_delta: int = 0
) -> list[Fraction]:
    """Multiply a degree-`degree` divided-power vector by ordinary r."""
    require(len(coefficients) == degree + 1, "r-product input width")
    answer = [Fraction(0) for _ in range(degree + 2)]
    for r_degree, coefficient in enumerate(coefficients):
        answer[r_degree + 1] += (r_degree + 1 + weight_delta) * coefficient
    return answer


def audit_divided_power_multipliers(
    degree: int, *, q_weight_delta: int = 0, r_weight_delta: int = 0
) -> None:
    """Check ordinary q,r multiplication on every divided-power basis row."""
    require(degree >= 0, "negative multiplier-audit degree")
    for r_degree in range(degree + 1):
        basis_vector = [Fraction(0) for _ in range(degree + 1)]
        basis_vector[r_degree] = Fraction(1)

        expected_q = [Fraction(0) for _ in range(degree + 2)]
        expected_q[r_degree] = Fraction(degree + 1 - r_degree)
        require(
            multiply_q(
                basis_vector, degree, weight_delta=q_weight_delta
            )
            == expected_q,
            "ordinary q lost a divided-power basis weight",
        )

        expected_r = [Fraction(0) for _ in range(degree + 2)]
        expected_r[r_degree + 1] = Fraction(r_degree + 1)
        require(
            multiply_r(
                basis_vector, degree, weight_delta=r_weight_delta
            )
            == expected_r,
            "ordinary r lost a divided-power basis weight",
        )


def moment(
    h: int,
    s: int,
    *,
    denominator_shift: int = 1,
    basis_reversed: int = 0,
) -> list[Fraction]:
    """H_s in the degree h-2 basis q^[h-2-l] r^[l]."""
    require(h >= 3, "moment tower starts at h=3")
    require(s >= 0, "negative moment index")
    require(basis_reversed in (0, 1), "moment-basis reversal flag")
    n = h - 2
    coefficients = [
        Fraction(1, s + ell + denominator_shift) for ell in range(n + 1)
    ]
    return list(reversed(coefficients)) if basis_reversed else coefficients


def carrier(
    h: int,
    s: int,
    *,
    denominator_shift: int = 1,
    carrier_q_factor: int = 2,
    q_weight_delta: int = 0,
    r_weight_delta: int = 0,
    moment_basis_reversed: int = 0,
) -> list[Fraction]:
    """c_s=(r-carrier_q_factor*q)H_s in degree h-1."""
    h_vector = moment(
        h,
        s,
        denominator_shift=denominator_shift,
        basis_reversed=moment_basis_reversed,
    )
    q_part = multiply_q(h_vector, h - 2, weight_delta=q_weight_delta)
    r_part = multiply_r(h_vector, h - 2, weight_delta=r_weight_delta)
    return add_vectors(
        r_part,
        [Fraction(-carrier_q_factor) * value for value in q_part],
    )


def pre_carrier_columns(
    h: int,
    moment_indices: list[int],
    *,
    denominator_shift: int = 1,
    q_weight_delta: int = 0,
    r_weight_delta: int = 0,
    moment_basis_reversed: int = 0,
) -> list[list[Fraction]]:
    """The qH_s,rH_s columns in degree h-1, before multiplication by r-2q."""
    columns: list[list[Fraction]] = []
    for s in moment_indices:
        h_vector = moment(
            h,
            s,
            denominator_shift=denominator_shift,
            basis_reversed=moment_basis_reversed,
        )
        columns.append(multiply_q(h_vector, h - 2, weight_delta=q_weight_delta))
        columns.append(
            multiply_r(h_vector, h - 2, weight_delta=r_weight_delta)
        )
    return columns


def carrier_columns(
    h: int,
    moment_indices: list[int],
    *,
    denominator_shift: int = 1,
    carrier_q_factor: int = 2,
    q_weight_delta: int = 0,
    r_weight_delta: int = 0,
    moment_basis_reversed: int = 0,
) -> list[list[Fraction]]:
    """The q*c_s,r*c_s degree-h ideal consequences."""
    columns: list[list[Fraction]] = []
    for s in moment_indices:
        c_vector = carrier(
            h,
            s,
            denominator_shift=denominator_shift,
            carrier_q_factor=carrier_q_factor,
            q_weight_delta=q_weight_delta,
            r_weight_delta=r_weight_delta,
            moment_basis_reversed=moment_basis_reversed,
        )
        columns.append(multiply_q(c_vector, h - 1, weight_delta=q_weight_delta))
        columns.append(
            multiply_r(c_vector, h - 1, weight_delta=r_weight_delta)
        )
    return columns


def clean_vector(h: int, *, first_q_degree: int = 2) -> list[Fraction]:
    """u=sum_{k=first_q_degree}^h q^[k]r^[h-k], in r-degree order."""
    return [
        Fraction(int(h - r_degree >= first_q_degree))
        for r_degree in range(h + 1)
    ]


def target_vector(h: int, *, low_q_sign: int = 1) -> list[Fraction]:
    """M_0+M_1=r^[h]+q r^[h-1], in r-degree order."""
    answer = [Fraction(0) for _ in range(h + 1)]
    answer[h - 1] = Fraction(low_q_sign)
    answer[h] = Fraction(1)
    return answer


def certified_jet_clean_vector(h: int) -> list[Fraction]:
    """The existing normal jet: sum_{j=2}^h q^[h-j]r^[j]."""
    return [Fraction(int(r_degree >= 2)) for r_degree in range(h + 1)]


def certified_jet_target_vector(h: int) -> list[Fraction]:
    """The existing jet's complementary q^[h]+q^[h-1]r class."""
    return [Fraction(int(r_degree <= 1)) for r_degree in range(h + 1)]


def full_moment_indices(h: int, *, moment_drop: int = 0) -> list[int]:
    if h == 3:
        count = 2 - moment_drop
    else:
        count = h - 2 - moment_drop
    require(count >= 0, "too many moments dropped")
    return list(range(count))


def evaluation_at_r_equals_2q(h: int, vector: list[Fraction]) -> Fraction:
    """Coefficient of q^[h] after the divided-power substitution r=2q."""
    require(len(vector) == h + 1, "evaluation input width")
    return sum(
        (
            vector[r_degree] * comb(h, r_degree) * 2**r_degree
            for r_degree in range(h + 1)
        ),
        Fraction(0),
    )


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    require(len(left) == len(right), "dot-product width mismatch")
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def positive_taylor_coefficient(n: int) -> Fraction:
    """[y^n](1+y)^(2n)(n+1-y)/(3+y), proved positive recursively."""
    require(n >= 1, "Taylor positivity starts at n=1")
    previous_r = (n + 1) * comb(2 * n, 0)
    coefficient = Fraction(previous_r, 3)
    require(coefficient > 0, "Taylor base coefficient is not positive")
    require(coefficient < previous_r, "Taylor base bound failed")
    for k in range(1, n + 1):
        current_r = (n + 1) * comb(2 * n, k) - comb(2 * n, k - 1)
        require(current_r > previous_r, "Taylor forcing coefficients not increasing")
        coefficient = Fraction(current_r - coefficient, 3)
        require(coefficient > 0, "Taylor coefficient lost positivity")
        require(coefficient < current_r, "Taylor coefficient upper bound failed")
        previous_r = current_r

    direct = (
        Fraction(n + 4)
        * sum(
            (
                Fraction((-1) ** k * comb(2 * n, n - k), 3 ** (k + 1))
                for k in range(n + 1)
            ),
            Fraction(0),
        )
        - comb(2 * n, n)
    )
    require(coefficient == direct, "Taylor recurrence/direct sum mismatch")
    return coefficient


def prefix_functional(h: int) -> list[Fraction]:
    n = h - 2
    return [Fraction(0)] + [
        Fraction((-1) ** (j - 1) * comb(n + j - 1, n))
        for j in range(1, n + 2)
    ]


def audit_rodrigues_functional(
    h: int, functional: list[Fraction]
) -> None:
    """Recover the functional from D^(n-1)(t^n(1-t)^n) exactly."""
    n = h - 2
    require(n >= 2, "Rodrigues audit starts at n=2")
    require(len(functional) == n + 2, "Rodrigues functional width")

    rodrigues = [Fraction(0) for _ in range(n + 2)]
    for k in range(n + 1):
        power = k + 1
        rodrigues[power] = Fraction(
            (-1) ** k
            * comb(n, k)
            * factorial(n + k),
            factorial(k + 1),
        )

    packaged = [
        Fraction(comb(n + 1, j)) * functional[j]
        for j in range(n + 2)
    ]
    scale = Fraction(factorial(n), n + 1)
    require(
        rodrigues == [scale * coefficient for coefficient in packaged],
        "Rodrigues/Jacobi functional normalization",
    )
    require(rodrigues[0] == 0, "Rodrigues polynomial misses t=0")
    require(sum(rodrigues, Fraction(0)) == 0, "Rodrigues polynomial misses t=1")
    for s in range(n - 1):
        moment_value = sum(
            (
                coefficient * Fraction(1, s + power + 1)
                for power, coefficient in enumerate(rodrigues)
            ),
            Fraction(0),
        )
        require(moment_value == 0, "Rodrigues moment orthogonality")


def audit_prefix_annihilator(h: int, functional: list[Fraction]) -> None:
    n = h - 2
    audit_rodrigues_functional(h, functional)
    for s in range(n - 1):
        h_ordinary = [Fraction(comb(n, ell), s + ell + 1) for ell in range(n + 1)]
        q_h = h_ordinary + [Fraction(0)]
        r_h = [Fraction(0)] + h_ordinary
        require(dot(functional, q_h) == 0, "Rodrigues functional misses qH_s")
        require(dot(functional, r_h) == 0, "Rodrigues functional misses rH_s")


def divide_by_z_minus_2(numerator: list[Fraction]) -> list[Fraction]:
    degree = len(numerator) - 1
    require(degree >= 1, "synthetic division degree")
    quotient = [Fraction(0) for _ in range(degree)]
    quotient[degree - 1] = numerator[degree]
    for current_degree in range(degree - 1, 0, -1):
        quotient[current_degree - 1] = (
            numerator[current_degree] + 2 * quotient[current_degree]
        )
    require(numerator[0] == -2 * quotient[0], "numerator not divisible by z-2")
    return quotient


def audit_certified_prefix_witness(h: int) -> None:
    """Rodrigues dual for the certified normal-jet clean orientation."""
    require(h >= 4, "Rodrigues prefix witness starts at h=4")
    n = h - 2
    functional = prefix_functional(h)
    audit_prefix_annihilator(h, functional)

    # In the certified orientation, h!X=1+h*z and
    # h!U=(1+z)^h-X.  Evaluation at z=2 gives B=1+2h.
    b_value = 1 + 2 * h
    numerator = [Fraction(-b_value * comb(h, degree)) for degree in range(h + 1)]
    numerator[0] += 3**h
    numerator[1] += 3**h * h
    quotient = divide_by_z_minus_2(numerator)
    witness_value = dot(functional, quotient)
    expected = Fraction(-3 * (2 * h + 1) * 2 ** (n - 1))
    require(witness_value == expected, "certified Rodrigues witness formula")
    require(witness_value != 0, "certified prefix witness unexpectedly vanished")


def audit_reversed_prefix_witness(h: int) -> None:
    """Rodrigues dual for the prompt's literally reversed M-indexing."""
    require(h >= 4, "reversed Rodrigues prefix witness starts at h=4")
    n = h - 2
    functional = prefix_functional(h)
    audit_prefix_annihilator(h, functional)

    # Scale the ordinary forms by h!: X=z^h+h*z^(h-1),
    # U=(1+z)^h-X.  The unique evaluation-compatible coefficient gives
    # the divisible numerator 3^h X-B(1+z)^h, B=2^(h-1)(h+2).
    b_value = 2 ** (h - 1) * (h + 2)
    numerator = [Fraction(-b_value * comb(h, degree)) for degree in range(h + 1)]
    numerator[h - 1] += 3**h * h
    numerator[h] += 3**h

    quotient = divide_by_z_minus_2(numerator)

    witness_value = dot(functional, quotient)
    taylor = positive_taylor_coefficient(n)
    expected = Fraction((-1) ** (h + 1) * 3**h) * taylor
    require(witness_value == expected, "Rodrigues witness evaluation formula")
    require(witness_value != 0, "prefix witness unexpectedly vanished")


def audit_h3_exception() -> None:
    """Check the two hand residuals when the prefix consists only of H_0."""
    h_zero = moment(3, 0)
    require(h_zero == [Fraction(1), Fraction(1, 2)], "h=3 H_0 formula")

    # Ascending r-degree in the ordinary basis.  Here
    # c_0=(r-2q)(q+r/2)=r^2/2-2q^2.
    c_zero = [
        -2 * h_zero[0],
        h_zero[0] - 2 * h_zero[1],
        h_zero[1],
    ]
    require(
        c_zero == [Fraction(-2), Fraction(0), Fraction(1, 2)],
        "h=3 c_0 formula",
    )
    q_c_zero = c_zero + [Fraction(0)]
    r_c_zero = [Fraction(0)] + c_zero

    jet_clean = [Fraction(0), Fraction(0), Fraction(3), Fraction(1)]
    jet_target = [Fraction(1), Fraction(3), Fraction(0), Fraction(0)]
    jet_rhs = add_vectors(
        [Fraction(1, 12) * value for value in jet_clean],
        [Fraction(-1, 2) * value for value in q_c_zero],
        [Fraction(-3, 2) * value for value in r_c_zero],
    )
    require(
        add_vectors(jet_target, [-value for value in jet_rhs])
        == [Fraction(0), Fraction(0), Fraction(0), Fraction(2, 3)],
        "h=3 certified-orientation residual",
    )

    reversed_clean = jet_target
    reversed_target = jet_clean
    reversed_rhs = add_vectors(
        [Fraction(12) * value for value in reversed_clean],
        [Fraction(6) * value for value in q_c_zero],
        [Fraction(2) * value for value in r_c_zero],
    )
    require(
        add_vectors(reversed_rhs, [-value for value in reversed_target])
        == [Fraction(0), Fraction(32), Fraction(0), Fraction(0)],
        "h=3 reversed-orientation residual",
    )


def audit_order(
    h: int,
    *,
    denominator_shift: int = 1,
    carrier_q_factor: int = 2,
    clean_first_q_degree: int = 2,
    moment_drop: int = 0,
    q_weight_delta: int = 0,
    r_weight_delta: int = 0,
    moment_basis_reversed: int = 0,
    target_low_q_sign: int = 1,
    certified_target_reversed: int = 0,
) -> None:
    require(h >= 3, "moment-tower audit starts at h=3")
    n = h - 2

    # The canonical H_0 is the divided difference of the adjacent powers.
    h_zero = moment(
        h,
        0,
        denominator_shift=denominator_shift,
        basis_reversed=moment_basis_reversed,
    )
    adjacent_difference = [Fraction(0)] + [Fraction(1) for _ in range(h - 1)]
    require(
        multiply_r(h_zero, n, weight_delta=r_weight_delta)
        == adjacent_difference,
        "H_0 lost its canonical divided-difference normalization",
    )

    # Independently retain the two endpoint orders q-x and q-r+x.
    forward = (1, 0, -1)
    backward = (1, -1, 1)
    orientation_sum = tuple(a + b for a, b in zip(forward, backward))
    require(
        orientation_sum == (carrier_q_factor, -1, 0),
        "carrier factor no longer matches the two-orientation sum",
    )

    # Check both literal divided-power multipliers, independently of ranks,
    # in the degrees used before and after the carrier correction.
    audit_divided_power_multipliers(
        n,
        q_weight_delta=q_weight_delta,
        r_weight_delta=r_weight_delta,
    )
    audit_divided_power_multipliers(
        h - 1,
        q_weight_delta=q_weight_delta,
        r_weight_delta=r_weight_delta,
    )

    u_vector = clean_vector(h, first_q_degree=clean_first_q_degree)
    target = target_vector(h, low_q_sign=target_low_q_sign)
    require(
        add_vectors(u_vector, target) == [Fraction(1) for _ in range(h + 1)],
        "clean/target complementary ledger changed",
    )

    u_evaluation = evaluation_at_r_equals_2q(h, u_vector)
    target_evaluation = evaluation_at_r_equals_2q(h, target)
    require(
        target_evaluation == 2 ** (h - 1) * (h + 2),
        "target evaluation at the carrier root",
    )
    require(
        u_evaluation == 3**h - target_evaluation,
        "clean evaluation at the carrier root",
    )
    require(u_evaluation != 0, "clean form became divisible by r-2q")

    indices = full_moment_indices(h, moment_drop=moment_drop)
    moment_columns = [
        moment(
            h,
            s,
            denominator_shift=denominator_shift,
            basis_reversed=moment_basis_reversed,
        )
        for s in indices
    ]
    expected_moment_rank = 2 if h == 3 else n
    require(exact_rank(moment_columns) == expected_moment_rank, "Cauchy moment rank")

    pre_columns = pre_carrier_columns(
        h,
        indices,
        denominator_shift=denominator_shift,
        q_weight_delta=q_weight_delta,
        r_weight_delta=r_weight_delta,
        moment_basis_reversed=moment_basis_reversed,
    )
    require(exact_rank(pre_columns) == h, "qW+rW does not fill degree h-1")

    relation_columns = carrier_columns(
        h,
        indices,
        denominator_shift=denominator_shift,
        carrier_q_factor=carrier_q_factor,
        q_weight_delta=q_weight_delta,
        r_weight_delta=r_weight_delta,
        moment_basis_reversed=moment_basis_reversed,
    )
    require(
        all(
            evaluation_at_r_equals_2q(h, column) == 0
            for column in relation_columns
        ),
        "carrier column misses the r=2q hyperplane",
    )
    require(exact_rank(relation_columns) == h, "carrier multiplication lost rank")
    full_columns = [u_vector] + relation_columns
    require(exact_rank(full_columns) == h + 1, "moment tower does not span degree h")
    require(in_span(target, full_columns), "M_0+M_1 missing from full tower")

    # The task's literal M-index orientation is reversed from the certified
    # scalar-unit normal jet.  The full carrier hyperplane closes that
    # source orientation too, but the two clean/target ledgers must not be
    # silently identified.
    jet_u = certified_jet_clean_vector(h)
    jet_target = (
        target_vector(h)
        if certified_target_reversed
        else certified_jet_target_vector(h)
    )
    require(
        add_vectors(jet_u, jet_target) == [Fraction(1) for _ in range(h + 1)],
        "certified-jet clean/target complement",
    )
    require(
        evaluation_at_r_equals_2q(h, jet_u) == 3**h - 1 - 2 * h,
        "certified-jet clean evaluation",
    )
    jet_columns = [jet_u] + relation_columns
    require(exact_rank(jet_columns) == h + 1, "tower misses certified-jet orientation")
    require(in_span(jet_target, jet_columns), "certified-jet target missing from tower")

    if (
        denominator_shift == 1
        and carrier_q_factor == 2
        and clean_first_q_degree == 2
        and moment_drop == 0
        and q_weight_delta == 0
        and r_weight_delta == 0
        and moment_basis_reversed == 0
        and target_low_q_sign == 1
        and certified_target_reversed == 0
    ):
        prefix = [0] if h == 3 else list(range(n - 1))
        prefix_columns = [u_vector] + carrier_columns(h, prefix)
        require(
            not in_span(target, prefix_columns),
            "proper initial moment prefix already contains the target",
        )
        if h >= 4:
            audit_reversed_prefix_witness(h)

        jet_prefix_columns = [jet_u] + carrier_columns(h, prefix)
        require(
            not in_span(certified_jet_target_vector(h), jet_prefix_columns),
            "proper prefix already contains the certified-jet target",
        )
        if h >= 4:
            audit_certified_prefix_witness(h)


def mutation_rejected(**mutation: int) -> bool:
    try:
        for h in range(3, 9):
            audit_order(h, **mutation)
    except RuntimeError:
        return True
    return False


def audit_non_setwise_minimality() -> None:
    """The initial prefix is sharp, but the listed set is not irredundant."""
    h = 6
    u_vector = clean_vector(h)
    target = target_vector(h)
    sparse_indices = [0, 1, 3]
    require(
        set(sparse_indices) < set(full_moment_indices(h)),
        "h=6 sparse set is not a proper subset of the full tower",
    )
    require(
        sparse_indices != [0, 1, 2],
        "h=6 scope guard lost its nonconsecutive set",
    )
    sparse_columns = [u_vector] + carrier_columns(h, sparse_indices)
    require(
        exact_determinant(sparse_columns) == Fraction(473, 78400),
        "h=6 sparse moment determinant",
    )
    require(exact_rank(sparse_columns) == h + 1, "h=6 sparse moment basis rank")
    require(in_span(target, sparse_columns), "h=6 sparse moment target membership")
    require(
        not in_span(target, [u_vector] + carrier_columns(h, [0, 1, 2])),
        "h=6 proper initial prefix unexpectedly succeeds",
    )

    jet_sparse_columns = [certified_jet_clean_vector(h)] + carrier_columns(
        h, sparse_indices
    )
    require(
        exact_determinant(jet_sparse_columns) == Fraction(179, 19600),
        "h=6 certified sparse moment determinant",
    )
    require(
        exact_rank(jet_sparse_columns) == h + 1,
        "h=6 certified sparse moment basis rank",
    )
    require(
        in_span(certified_jet_target_vector(h), jet_sparse_columns),
        "h=6 certified sparse moment target membership",
    )
    require(
        not in_span(
            certified_jet_target_vector(h),
            [certified_jet_clean_vector(h)]
            + carrier_columns(h, [0, 1, 2]),
        ),
        "h=6 certified initial prefix unexpectedly succeeds",
    )


def main() -> None:
    for h in range(3, 25):
        audit_order(h)

    audit_h3_exception()
    audit_non_setwise_minimality()

    require(
        mutation_rejected(denominator_shift=2),
        "moment-denominator mutation survived",
    )
    require(
        mutation_rejected(moment_basis_reversed=1),
        "moment-basis reversal mutation survived",
    )
    require(
        mutation_rejected(carrier_q_factor=1),
        "two-orientation carrier mutation survived",
    )
    require(
        mutation_rejected(clean_first_q_degree=3),
        "clean endpoint mutation survived",
    )
    require(
        mutation_rejected(moment_drop=1),
        "last-moment deletion mutation survived",
    )
    require(
        mutation_rejected(q_weight_delta=1),
        "divided-power q-multiplication mutation survived",
    )
    require(
        mutation_rejected(r_weight_delta=1),
        "divided-power r-multiplication mutation survived",
    )
    require(
        mutation_rejected(target_low_q_sign=-1),
        "target-sign mutation survived",
    )
    require(
        mutation_rejected(certified_target_reversed=1),
        "certified clean/reversed-target mutation survived",
    )

    print(
        "scalar-unit carrier moment tower: PASS; h=3..24, exact "
        "Hilbert/Cauchy ranks, Rodrigues/Jacobi prefix witnesses, both "
        "index orientations, h=3 residuals, h=6 scope guard, and 9 "
        "mutations audited"
    )


if __name__ == "__main__":
    main()
