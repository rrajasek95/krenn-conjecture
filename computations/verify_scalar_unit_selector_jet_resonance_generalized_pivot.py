#!/usr/bin/env python3
"""Exact audits for selector resonance and generalized scalar-unit pivots.

The companion note contains the uniform proofs. This dependency-free
checker solves the affine top-selector constraints over the rationals,
computes their common blind spaces, verifies the simultaneous left-right
GL2 absorption criterion, checks the stricter monomial criterion and the
two sharp packet guards, checks the alpha^(1-h) adjacent-power scaling,
audits the split-anchor flattening rank test, and keeps dense
coordinate-anchor loss explicitly below exactness.
The packet guards do not construct one common site-square-zero carrier
realizing all four jets; that first omitted physical constraint is stated
explicitly in the companion note.

Every check uses an explicit runtime failure, so python -O changes nothing.
"""

from fractions import Fraction
from itertools import product


F = Fraction


def require(condition, message):
    """Raise explicitly, including when Python assertions are disabled."""

    if not condition:
        raise RuntimeError(message)


def zero(dimension):
    return tuple(F(0) for _ in range(dimension))


def basis(dimension, index):
    answer = [F(0)] * dimension
    answer[index] = F(1)
    return tuple(answer)


def add(left, right):
    require(len(left) == len(right), "vector dimension mismatch")
    return tuple(x + y for x, y in zip(left, right))


def scale(coefficient, value):
    return tuple(F(coefficient) * entry for entry in value)


def dot(left, right):
    require(len(left) == len(right), "dot-product dimension mismatch")
    return sum((x * y for x, y in zip(left, right)), F(0))


def rref(matrix):
    work = [list(map(F, row)) for row in matrix]
    if not work:
        return work, []
    width = len(work[0])
    require(all(len(row) == width for row in work), "ragged matrix")
    pivots = []
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        divisor = work[pivot_row][column]
        work[pivot_row] = [entry / divisor for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                x - multiplier * y
                for x, y in zip(work[row], work[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return work, pivots


def rank(vectors):
    return len(rref(vectors)[1]) if vectors else 0


def nullspace(matrix, width=None):
    if matrix:
        width = len(matrix[0])
    require(width is not None, "nullspace needs a width")
    if not matrix:
        return [basis(width, index) for index in range(width)]
    reduced, pivots = rref(matrix)
    free_columns = [column for column in range(width) if column not in pivots]
    answer = []
    for free in free_columns:
        value = [F(0)] * width
        value[free] = F(1)
        for row, pivot in enumerate(pivots):
            value[pivot] = -reduced[row][free]
        answer.append(tuple(value))
    return answer


def same_span(left, right):
    return rank(left) == rank(right) == rank(list(left) + list(right))


def affine_solution(matrix, right_hand_side):
    """Return one solution and a direction basis, or None."""

    require(len(matrix) == len(right_hand_side), "affine row mismatch")
    require(matrix, "affine system must have rows")
    width = len(matrix[0])
    augmented = [
        list(map(F, row)) + [F(value)]
        for row, value in zip(matrix, right_hand_side)
    ]
    reduced, pivots = rref(augmented)
    if any(not any(row[:width]) and row[width] for row in reduced):
        return None
    base = [F(0)] * width
    for row, pivot in enumerate(pivots):
        if pivot < width:
            base[pivot] = reduced[row][width]
    return tuple(base), nullspace(matrix)


def selector_family(q_top, label):
    """Solve nu(Q)=0 and nu(X_j)=delta_ij."""

    dimension = len(q_top)
    targets = [basis(dimension, index) for index in range(3)]
    matrix = [q_top] + targets
    right = [F(0)] + [F(index == label) for index in range(3)]
    return affine_solution(matrix, right)


def family_rows(family):
    base, directions = family
    return [base] + list(directions)


def blind_basis(families, dimension):
    rows = []
    for family in families:
        rows.extend(family_rows(family))
    return nullspace(rows, width=dimension)


def family_misses(family, value):
    return all(not dot(row, value) for row in family_rows(family))


def validate_family(q_top, label, family):
    dimension = len(q_top)
    targets = [basis(dimension, index) for index in range(3)]
    base, directions = family
    require(not dot(base, q_top), "selector base does not kill Q")
    require(
        [dot(base, target) for target in targets]
        == [F(index == label) for index in range(3)],
        "selector base has wrong target values",
    )
    for direction in directions:
        require(not dot(direction, q_top), "selector direction sees Q")
        require(
            not any(dot(direction, target) for target in targets),
            "selector direction sees D",
        )


def audit_transverse_selectors():
    dimension = 7
    targets = [basis(dimension, index) for index in range(3)]
    q_top = (F(2), F(-1), F(3), F(5), F(0), F(-4), F(7))
    require(rank(targets + [q_top]) == 4, "transverse Q entered D")

    families = []
    for label in range(3):
        family = selector_family(q_top, label)
        require(family is not None, "transverse selector family is empty")
        validate_family(q_top, label, family)
        families.append(family)

        explicit = add(
            targets[label],
            scale(-q_top[label] / q_top[3], basis(dimension, 3)),
        )
        require(
            dot(explicit, q_top) == 0
            and [dot(explicit, target) for target in targets]
            == [F(index == label) for index in range(3)],
            "explicit two-coordinate selector is outside the torsor",
        )
        require(
            rank(
                list(family[1])
                + [add(explicit, scale(-1, family[0]))]
            )
            == rank(family[1]),
            "explicit selector difference is not a torsor direction",
        )
        expected_single = [q_top] + [
            targets[index] for index in range(3) if index != label
        ]
        require(
            same_span(blind_basis([family], dimension), expected_single),
            f"wrong single-label blind space for label {label}",
        )

    joint = blind_basis(families, dimension)
    require(same_span(joint, [q_top]), "transverse joint blind space is not C Q")
    require(
        all(family_misses(family, scale(11, q_top)) for family in families),
        "a selector detected a radial multiple",
    )
    for target in targets:
        require(
            any(not family_misses(family, target) for family in families),
            "a nonzero target vector escaped all transverse selectors",
        )

    wrong = add(targets[1], scale(q_top[1] / q_top[3], basis(dimension, 3)))
    require(dot(wrong, q_top) != 0, "selector sign mutation survived")


def audit_target_selectors():
    dimension = 7
    targets = [basis(dimension, index) for index in range(3)]

    regimes = (
        ((F(0), F(2), F(-3), F(0), F(0), F(0), F(0)), (0,)),
        ((F(0), F(5), F(0), F(0), F(0), F(0), F(0)), (0, 2)),
        (zero(dimension), (0, 1, 2)),
    )
    for q_top, expected_labels in regimes:
        families = []
        for label in range(3):
            family = selector_family(q_top, label)
            require(
                (family is not None) == (label in expected_labels),
                "target-case admissible-label criterion failed",
            )
            if family is not None:
                validate_family(q_top, label, family)
                expected_single = [
                    targets[index] for index in range(3) if index != label
                ]
                require(
                    same_span(blind_basis([family], dimension), expected_single),
                    "wrong target single-label blind space",
                )
                families.append(family)

        support = [targets[index] for index in range(3) if q_top[index]]
        require(
            same_span(blind_basis(families, dimension), support),
            "joint target blind space is not the nonzero-coordinate span",
        )

    full_support_q = add(add(targets[0], scale(2, targets[1])), scale(-1, targets[2]))
    require(
        all(selector_family(full_support_q, label) is None for label in range(3)),
        "full-support target Q unexpectedly admitted a selector",
    )
    require(
        same_span(
            blind_basis([], dimension),
            [basis(dimension, index) for index in range(dimension)],
        ),
        "the empty selector family did not have the vacuous full blind space",
    )
    require(
        not same_span(blind_basis([], dimension), targets),
        "the empty selector family was incorrectly narrowed to D",
    )
    two_support_q = add(targets[1], targets[2])
    family = selector_family(two_support_q, 0)
    require(family is not None, "two-support target lost its zero-label selector")
    nonradial_blind = add(targets[1], scale(-1, targets[2]))
    require(
        family_misses(family, nonradial_blind),
        "the two-dimensional target resonance was narrowed to C Q",
    )
    require(
        rank([two_support_q, nonradial_blind]) == 2,
        "nonradial target guard collapsed to C Q",
    )


def mat(entries):
    require(len(entries) == 2 and all(len(row) == 2 for row in entries), "not 2x2")
    return tuple(tuple(map(F, row)) for row in entries)


ZERO2 = mat(((0, 0), (0, 0)))
E11 = mat(((1, 0), (0, 0)))
E22 = mat(((0, 0), (0, 1)))
IDENTITY2 = mat(((1, 0), (0, 1)))


def mat_add(left, right):
    return mat(
        tuple(
            tuple(left[row][column] + right[row][column] for column in range(2))
            for row in range(2)
        )
    )


def mat_scale(coefficient, value):
    return mat(
        tuple(
            tuple(F(coefficient) * value[row][column] for column in range(2))
            for row in range(2)
        )
    )


def transpose(value):
    return mat(
        tuple(tuple(value[column][row] for column in range(2)) for row in range(2))
    )


def mat_mul(left, right):
    return mat(
        tuple(
            tuple(
                sum(
                    (left[row][inner] * right[inner][column] for inner in range(2)),
                    F(0),
                )
                for column in range(2)
            )
            for row in range(2)
        )
    )


def determinant(value):
    return value[0][0] * value[1][1] - value[0][1] * value[1][0]


def mat_rank(value):
    return rank([list(value[0]), list(value[1])])


def inverse(value):
    determinant_value = determinant(value)
    require(determinant_value, "singular 2x2 inverse")
    return mat_scale(
        F(1) / determinant_value,
        mat(
            (
                (value[1][1], -value[0][1]),
                (-value[1][0], value[0][0]),
            )
        ),
    )


def outer(left, right):
    return mat(
        tuple(
            tuple(F(left[row]) * F(right[column]) for column in range(2))
            for row in range(2)
        )
    )


def columns(left, right):
    return mat(((left[0], right[0]), (left[1], right[1])))


def factor_rank_one(value):
    require(mat_rank(value) == 1, "rank-one factorization got wrong rank")
    pivot = next(
        (entry for entry in product(range(2), repeat=2) if value[entry[0]][entry[1]]),
        None,
    )
    require(pivot is not None, "rank-one matrix unexpectedly zero")
    pivot_row, pivot_column = pivot
    left = tuple(value[row][pivot_column] for row in range(2))
    divisor = value[pivot_row][pivot_column]
    right = tuple(value[pivot_row][column] / divisor for column in range(2))
    require(outer(left, right) == value, "rank-one factorization failed")
    return left, right


def gl2_absorbable(matrices):
    a_matrix, b_matrix, c_matrix = matrices
    return (
        a_matrix == ZERO2
        and mat_rank(b_matrix) == 1
        and mat_rank(c_matrix) == 1
        and determinant(mat_add(b_matrix, c_matrix)) != 0
    )


def normalizer(matrices):
    require(gl2_absorbable(matrices), "normalizer called on obstructed packet")
    _, b_matrix, c_matrix = matrices
    u_b, v_b = factor_rank_one(b_matrix)
    u_c, v_c = factor_rank_one(c_matrix)
    left = inverse(columns(u_b, u_c))
    right = inverse(columns(v_b, v_c))
    return left, right


def transform_packet(matrices, left, right):
    return tuple(
        mat_mul(mat_mul(left, value), transpose(right))
        for value in matrices
    )


def nonzero_positions(value):
    return [
        (row, column)
        for row, column in product(range(2), repeat=2)
        if value[row][column]
    ]


def monomial_absorbable(matrices):
    a_matrix, b_matrix, c_matrix = matrices
    if a_matrix != ZERO2:
        return False
    b_positions = nonzero_positions(b_matrix)
    c_positions = nonzero_positions(c_matrix)
    if len(b_positions) != 1 or len(c_positions) != 1:
        return False
    b_row, b_column = b_positions[0]
    c_row, c_column = c_positions[0]
    return b_row != c_row and b_column != c_column


def pencil_coefficients(left, right):
    """Coefficients of det(x*left+y*right) in x^2,xy,y^2 order."""

    cross = (
        left[0][0] * right[1][1]
        + right[0][0] * left[1][1]
        - left[0][1] * right[1][0]
        - right[0][1] * left[1][0]
    )
    return determinant(left), cross, determinant(right)


def quadratic_discriminant(coefficients):
    x2, xy, y2 = coefficients
    return xy * xy - 4 * x2 * y2


def change_binary_variables(coefficients, change):
    """Substitute x=pX+qY, y=rX+sY in a binary quadratic."""

    x2, xy, y2 = coefficients
    p, q = change[0]
    r, s = change[1]
    return (
        x2 * p * p + xy * p * r + y2 * r * r,
        2 * x2 * p * q + xy * (p * s + q * r) + 2 * y2 * r * s,
        x2 * q * q + xy * q * s + y2 * s * s,
    )


def audit_gl2_classification():
    canonical = (ZERO2, E11, E22)
    require(gl2_absorbable(canonical), "canonical packet failed GL2 criterion")
    require(monomial_absorbable(canonical), "canonical failed monomial criterion")

    trials = (
        (columns((1, 3), (2, 5)), columns((2, 1), (-1, 4))),
        (columns((1, -2), (3, 1)), columns((4, 1), (1, -1))),
        (columns((2, 5), (-3, 2)), columns((1, 7), (2, 3))),
    )
    for left_factors, right_factors in trials:
        require(determinant(left_factors), "singular planted left factors")
        require(determinant(right_factors), "singular planted right factors")
        b_matrix = outer(
            (left_factors[0][0], left_factors[1][0]),
            (right_factors[0][0], right_factors[1][0]),
        )
        c_matrix = outer(
            (left_factors[0][1], left_factors[1][1]),
            (right_factors[0][1], right_factors[1][1]),
        )
        packet = (ZERO2, b_matrix, c_matrix)
        require(gl2_absorbable(packet), "transverse rank-one pair rejected")
        left, right = normalizer(packet)
        require(
            transform_packet(packet, left, right) == canonical,
            "constructed GL2 normalizer failed",
        )

    mutations = (
        (E11, E11, E22),
        (ZERO2, IDENTITY2, E22),
        (ZERO2, E11, mat(((0, 1), (0, 0)))),
        (ZERO2, E11, mat(((0, 0), (2, 0)))),
        (ZERO2, ZERO2, E22),
    )
    require(
        all(not gl2_absorbable(packet) for packet in mutations),
        "a zero/rank/transversality mutation passed",
    )

    cross_units = (
        ZERO2,
        mat(((0, 2), (0, 0))),
        mat(((0, 0), (-3, 0))),
    )
    require(gl2_absorbable(cross_units), "crossed units lost GL2 absorption")
    require(monomial_absorbable(cross_units), "crossed units lost monomial absorption")


def audit_selector_blind_no_go():
    dimension = 7
    x_b = basis(dimension, 1)
    families = [selector_family(x_b, label) for label in (0, 2)]
    require(all(family is not None for family in families), "Q=X_b selector missing")

    jet_b = mat(((-1, 1), (1, -1)))
    require(mat_rank(jet_b) == 1, "no-go jet slice is not rank one")
    for coefficient in (entry for row in jet_b for entry in row):
        jet_entry = scale(coefficient, x_b)
        require(
            all(family_misses(family, jet_entry) for family in families),
            "an admissible selector detected the blind no-go packet",
        )

    b_matrix = mat_add(E11, jet_b)
    c_matrix = E22
    packet = (ZERO2, b_matrix, c_matrix)
    require(mat_rank(b_matrix) == 2, "corrected no-go matrix lost rank two")
    require(not gl2_absorbable(packet), "rank-two no-go packet was absorbed")
    require(not monomial_absorbable(packet), "rank-two no-go became monomial")

    coefficients = pencil_coefficients(b_matrix, c_matrix)
    require(coefficients == (F(-1), F(0), F(0)), "wrong no-go pencil")
    require(
        quadratic_discriminant(coefficients) == 0,
        "repeated-root no-go pencil acquired nonzero discriminant",
    )
    canonical_coefficients = pencil_coefficients(E11, E22)
    require(
        canonical_coefficients == (F(0), F(1), F(0)),
        "wrong canonical pencil",
    )
    require(
        quadratic_discriminant(canonical_coefficients) != 0,
        "canonical pencil lost its two distinct roots",
    )

    for change in (
        mat(((1, 1), (0, 1))),
        mat(((2, -1), (3, 1))),
        mat(((-1, 2), (1, 1))),
    ):
        changed = change_binary_variables(coefficients, change)
        require(
            quadratic_discriminant(changed)
            == determinant(change) ** 2 * quadratic_discriminant(coefficients),
            "binary-pencil discriminant covariance failed",
        )
        changed_canonical = change_binary_variables(canonical_coefficients, change)
        require(
            quadratic_discriminant(changed_canonical)
            == determinant(change) ** 2
            * quadratic_discriminant(canonical_coefficients),
            "canonical discriminant covariance failed",
        )


def audit_dense_absorbable_guard():
    dimension = 7
    x_b = basis(dimension, 1)
    x_c = basis(dimension, 2)
    q_top = add(x_b, x_c)
    family = selector_family(q_top, 0)
    require(family is not None, "Q=X_b+X_c lost its a-selector")

    b_matrix = mat(((1, 0), (1, 0)))
    c_matrix = mat(((0, 1), (0, -1)))
    packet = (ZERO2, b_matrix, c_matrix)
    require(gl2_absorbable(packet), "dense guard should be GL2 absorbable")
    require(
        not monomial_absorbable(packet),
        "dense guard unexpectedly became monomial absorbable",
    )
    left = mat(((F(1, 2), F(1, 2)), (F(1, 2), F(-1, 2))))
    require(
        transform_packet(packet, left, IDENTITY2) == (ZERO2, E11, E22),
        "explicit dense normalizer failed",
    )

    jet_b = mat_add(b_matrix, mat_scale(-1, E11))
    jet_c = mat_add(c_matrix, mat_scale(-1, E22))
    for row, column in product(range(2), repeat=2):
        jet_entry = add(
            scale(jet_b[row][column], x_b),
            scale(jet_c[row][column], x_c),
        )
        require(
            family_misses(family, jet_entry),
            "zero-label selector detected the blind dense guard",
        )


def audit_adjacent_power_scaling():
    """Check the formal divided-power coefficient alpha^(1-h)."""

    for alpha in (F(-3), F(-2), F(2), F(3)):
        for h in range(3, 10):
            degree = h - 1
            # Coefficients of q^[degree-k] R_aa^[k] in
            # (alpha^-1(alpha*q+R_aa))^[degree].
            direct = [alpha ** (-k) for k in range(degree + 1)]
            theta = [F(0)] + [
                alpha ** (degree - k) for k in range(1, degree + 1)
            ]
            transformed = [F(1)] + [
                alpha ** (1 - h) * coefficient for coefficient in theta[1:]
            ]
            require(
                direct == transformed,
                "the alpha^(1-h) adjacent-power scaling failed",
            )
            wrong = [F(1)] + [
                alpha ** (-h) * coefficient for coefficient in theta[1:]
            ]
            require(
                direct != wrong,
                "the alpha^-h exponent mutation survived",
            )


def mutual_anchor_count(edges):
    """Count edges whose two labelled endpoints both have degree one."""

    degree = {}
    for left, right in edges:
        degree[left] = degree.get(left, 0) + 1
        degree[right] = degree.get(right, 0) + 1
    return sum(
        degree[left] == 1 and degree[right] == 1
        for left, right in edges
    )


def audit_split_anchor_flattening():
    """Audit the rank count used by the exact split-anchor lemma."""

    samples = [
        tuple(map(F, coefficients))
        for coefficients in product((-1, 0, 1), repeat=3)
        if coefficients != (0, 0, 0)
    ]
    for coefficients in samples:
        flattening = [
            [coefficients[row] if row == column else F(0) for column in range(3)]
            for row in range(3)
        ]
        flattening_rank = rank(flattening)
        nonzero_labels = [
            index for index, coefficient in enumerate(coefficients) if coefficient
        ]
        require(
            flattening_rank == len(nonzero_labels),
            "target contraction rank is not its number of live colours",
        )
        if flattening_rank == 1:
            selected = nonzero_labels[0]
            nonzero_rows = [
                row for row in range(3) if any(flattening[row])
            ]
            nonzero_columns = [
                column
                for column in range(3)
                if any(flattening[row][column] for row in range(3))
            ]
            require(
                nonzero_rows == [selected] and nonzero_columns == [selected],
                "rank-one target contraction did not force one coordinate line",
            )
            # In the reverse contraction, a rank-one coordinate covector
            # nonzero on that forced line must have the same label.
            compatible = []
            for reverse in product((-1, 0, 1), repeat=3):
                live = [index for index, value in enumerate(reverse) if value]
                if len(live) == 1 and reverse[selected]:
                    compatible.append(live[0])
            require(
                set(compatible) == {selected},
                "symmetric split-anchor contraction changed the colour",
            )

    # Dense block-diagonal endpoint maps keep the old split lines and the
    # selected direct line independent, which is the counting input after
    # exactness turns them back into coordinate axes.
    selected_line = (F(1), F(0), F(0))
    first_dense_line = (F(0), F(1), F(1))
    second_dense_line = (F(0), F(1), F(-1))
    require(
        rank([selected_line, first_dense_line, second_dense_line]) == 3,
        "dense endpoint map merged distinct split-anchor lines",
    )


def audit_pre_exactness_anchor_loss():
    p_b = ("p", "b")
    p_c = ("p", "c")
    u = ("u", "d")
    v = ("v", "e")
    before = ((p_b, u), (p_c, v))
    require(mutual_anchor_count(before) == 2, "planted anchors are not mutual")

    after_dense = ((p_b, u), (p_b, v), (p_c, u), (p_c, v))
    require(
        mutual_anchor_count(after_dense) == 0,
        "dense row mixing unexpectedly preserved an anchor",
    )
    direct_anchor = (("p", "a"), ("q", "a"))
    require(
        mutual_anchor_count(after_dense + (direct_anchor,)) == 1,
        "new direct anchor count is wrong",
    )
    require(
        mutual_anchor_count(after_dense + (direct_anchor,))
        < mutual_anchor_count(before),
        "raw dense incidence did not exhibit its pre-exactness anchor loss",
    )

    after_swap = ((p_c, u), (p_b, v))
    require(
        mutual_anchor_count(after_swap) == mutual_anchor_count(before),
        "monomial row relabelling changed the anchor count",
    )


def main():
    audit_transverse_selectors()
    audit_target_selectors()
    audit_gl2_classification()
    audit_selector_blind_no_go()
    audit_dense_absorbable_guard()
    audit_adjacent_power_scaling()
    audit_split_anchor_flattening()
    audit_pre_exactness_anchor_loss()
    print("selector torsors and exact common blind spaces: PASS")
    print("GL2 and monomial generalized-pivot criteria: PASS")
    print("selector-blind rank-one-jet no-go and dense guard: PASS")
    print("adjacent-power scaling and split-anchor flattening inputs: PASS")
    print("pre-exactness dense anchor loss: PASS")


if __name__ == "__main__":
    main()
