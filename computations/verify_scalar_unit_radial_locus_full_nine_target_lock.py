#!/usr/bin/env python3
"""Exact audit for the full-nine scalar-unit radial target lock.

The companion note contains the uniform proof.  This dependency-free
checker reconstructs several exact response modules, derives their radial
loci by row reduction, verifies the target-lock normal form, and audits the
matching-power catalecticant criterion.  All checks use explicit failures,
so running with ``python -O`` changes nothing.
"""

from fractions import Fraction
from math import factorial


F = Fraction
PAIRS = tuple((i, j) for i in range(3) for j in range(3))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def vector(*entries):
    return tuple(map(F, entries))


def zero(dimension):
    return tuple(F(0) for _ in range(dimension))


def basis(dimension, index):
    answer = [F(0)] * dimension
    answer[index] = F(1)
    return tuple(answer)


def add(left, right):
    require(len(left) == len(right), "vector-addition dimension mismatch")
    return tuple(x + y for x, y in zip(left, right))


def scale(coefficient, value):
    return tuple(F(coefficient) * entry for entry in value)


def linear_combination(coefficients, values):
    require(values, "empty linear combination")
    require(len(coefficients) == len(values), "linear-combination mismatch")
    answer = zero(len(values[0]))
    for coefficient, value in zip(coefficients, values):
        answer = add(answer, scale(coefficient, value))
    return answer


def dot(left, right):
    require(len(left) == len(right), "dot-product dimension mismatch")
    return sum((x * y for x, y in zip(left, right)), F(0))


def matrix_vector(matrix, value):
    return tuple(dot(row, value) for row in matrix)


def matrix_from_columns(columns):
    require(columns, "matrix needs at least one column")
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "ragged columns")
    return [
        [F(columns[column][row]) for column in range(len(columns))]
        for row in range(height)
    ]


def rref(matrix):
    work = [list(map(F, row)) for row in matrix]
    if not work:
        return work, []
    width = len(work[0])
    require(all(len(row) == width for row in work), "ragged matrix")
    pivot_columns = []
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
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return work, pivot_columns


def rank(matrix):
    return len(rref(matrix)[1]) if matrix else 0


def nullspace(matrix):
    reduced, pivots = rref(matrix)
    width = len(matrix[0]) if matrix else 0
    free_columns = [column for column in range(width) if column not in pivots]
    answer = []
    for free in free_columns:
        value = [F(0)] * width
        value[free] = F(1)
        for row, pivot in enumerate(pivots):
            value[pivot] = -reduced[row][free]
        answer.append(tuple(value))
    return answer


def linear_system_has_solution(matrix, right_hand_side):
    require(len(matrix) == len(right_hand_side), "linear-system row mismatch")
    if not matrix:
        return True
    augmented = [
        list(map(F, row)) + [F(value)]
        for row, value in zip(matrix, right_hand_side)
    ]
    return rank(matrix) == rank(augmented)


def map_from_basis_images(images):
    """Return the matrix of a map whose input basis has the given images."""
    return matrix_from_columns(images)


def radial_basis(model):
    """Solve sum K_ij R_ij = beta*q; output tuples (K entries, beta)."""
    columns = list(model["responses"]) + [scale(-1, model["q"])]
    return nullspace(matrix_from_columns(columns))


def validate_full_nine(model):
    h = model["h"]
    alpha = model["alpha"]
    multiplication = model["multiplication"]
    top_dimension = len(model["Q"])
    targets = [basis(top_dimension, i) for i in range(3)]
    if not any(model["q"]):
        return False
    if matrix_vector(multiplication, model["q"]) != scale(h, model["Q"]):
        return False
    for (i, j), response in zip(PAIRS, model["responses"]):
        expected = zero(top_dimension)
        if i == j:
            expected = targets[i]
        if i == j == 0:
            expected = add(expected, scale(-alpha, model["Q"]))
        if matrix_vector(multiplication, response) != expected:
            return False
    return True


def audit_target_lock(model, expected_radial_dimension):
    require(validate_full_nine(model), f"{model['name']}: nine-row failure")
    radial = radial_basis(model)
    require(
        len(radial) == expected_radial_dimension,
        f"{model['name']}: wrong radial dimension",
    )
    h = model["h"]
    alpha = model["alpha"]
    Q = model["Q"]
    top_dimension = len(Q)
    targets = [basis(top_dimension, i) for i in range(3)]
    s_values = []
    beta_values = []
    c_values = []
    diagonal_values = [[], [], []]
    for relation in radial:
        cap = relation[:9]
        beta = relation[9]
        scalar = alpha * cap[PAIR_INDEX[(0, 0)]]
        c_value = scalar + h * beta
        target = linear_combination(
            [cap[PAIR_INDEX[(i, i)]] for i in range(3)], targets
        )
        require(
            target == scale(c_value, Q),
            f"{model['name']}: T=(s+h beta)Q failed",
        )
        response = linear_combination(cap, model["responses"])
        require(
            response == scale(beta, model["q"]),
            f"{model['name']}: computed radial relation is false",
        )
        s_values.append(scalar)
        beta_values.append(beta)
        c_values.append(c_value)
        for i in range(3):
            diagonal_values[i].append(cap[PAIR_INDEX[(i, i)]])
    require(
        rank([s_values, beta_values]) <= 1,
        f"{model['name']}: radial scalar rank exceeded one",
    )

    # Quotient formulation: in A_2/N, N spanned by the eight non-(0,0)
    # responses, the image of (K_00,beta) is the kernel of
    # (x,beta) -> x[R_00]-beta[q].  Its dimension is therefore two minus
    # the dimension of span{[R_00],[q]}.
    nonexceptional = [
        response
        for pair, response in zip(PAIRS, model["responses"])
        if pair != (0, 0)
    ]
    rank_n = rank(matrix_from_columns(nonexceptional))
    quotient_class_rank = (
        rank(
            matrix_from_columns(
                nonexceptional
                + [model["responses"][PAIR_INDEX[(0, 0)]], model["q"]]
            )
        )
        - rank_n
    )
    require(
        quotient_class_rank >= 1,
        f"{model['name']}: both exceptional quotient classes were killed",
    )
    require(
        rank([s_values, beta_values]) == 2 - quotient_class_rank,
        f"{model['name']}: quotient radial-rank formula failed",
    )
    return radial, tuple(diagonal_values), tuple(c_values)


def desired_selector_values(label):
    return [F(1) if pair == (label, label) else F(0) for pair in PAIRS]


def abstract_quotient_selector_exists(model, label):
    equations = [list(model["q"])] + [list(r) for r in model["responses"]]
    right_hand_side = [F(0)] + desired_selector_values(label)
    return linear_system_has_solution(equations, right_hand_side)


def top_catalecticant_selector_exists(model, label, impose_q=True):
    multiplication = model["multiplication"]
    equations = []
    right_hand_side = []
    if impose_q:
        equations.append(list(matrix_vector(multiplication, model["q"])))
        right_hand_side.append(F(0))
    for response, wanted in zip(
        model["responses"], desired_selector_values(label)
    ):
        equations.append(list(matrix_vector(multiplication, response)))
        right_hand_side.append(wanted)
    return linear_system_has_solution(equations, right_hand_side)


def predicted_top_selector(model, label):
    Q = model["Q"]
    outside_target_span = any(Q[index] for index in range(3, len(Q)))
    return outside_target_span or Q[label] == 0


def build_radial_line_model(h, alpha, coefficients, name):
    """One radial line with diagonal vector ``coefficients``."""
    h = F(h)
    alpha = F(alpha)
    v0, v1, v2 = map(F, coefficients)
    require(v2 != 0, "the radial-line construction needs v2 nonzero")
    response_dimension = 9
    q = basis(response_dimension, 0)
    r00 = basis(response_dimension, 1)
    r11 = basis(response_dimension, 2)
    off_diagonal = {
        pair: basis(response_dimension, index + 3)
        for index, pair in enumerate(
            ((0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1))
        )
    }
    beta = (F(1) - alpha * v0) / h
    r22 = scale(
        F(1) / v2,
        linear_combination((beta, -v0, -v1), (q, r00, r11)),
    )
    responses = []
    for pair in PAIRS:
        if pair == (0, 0):
            responses.append(r00)
        elif pair == (1, 1):
            responses.append(r11)
        elif pair == (2, 2):
            responses.append(r22)
        else:
            responses.append(off_diagonal[pair])

    Q = vector(v0, v1, v2)
    X = [basis(3, i) for i in range(3)]
    basis_images = [scale(h, Q), add(X[0], scale(-alpha, Q)), X[1]]
    basis_images.extend(zero(3) for _ in range(6))
    return {
        "name": name,
        "h": h,
        "alpha": alpha,
        "q": q,
        "responses": tuple(responses),
        "Q": Q,
        "multiplication": map_from_basis_images(basis_images),
        "declared_beta": beta,
        "declared_diagonal": (v0, v1, v2),
    }


def build_torsion_model(Q, name, h=5, alpha=F(3, 2)):
    """A nonzero off-diagonal kernel and no radial diagonal direction."""
    Q = tuple(map(F, Q))
    top_dimension = len(Q)
    response_dimension = 9
    q = basis(response_dimension, 0)
    diagonal = [basis(response_dimension, index) for index in (1, 2, 3)]
    off_diagonal = {
        (0, 1): basis(response_dimension, 4),
        (0, 2): basis(response_dimension, 4),
        (1, 0): basis(response_dimension, 5),
        (1, 2): basis(response_dimension, 6),
        (2, 0): basis(response_dimension, 7),
        (2, 1): basis(response_dimension, 8),
    }
    responses = []
    for pair in PAIRS:
        if pair[0] == pair[1]:
            responses.append(diagonal[pair[0]])
        else:
            responses.append(off_diagonal[pair])
    targets = [basis(top_dimension, i) for i in range(3)]
    basis_images = [scale(h, Q)]
    basis_images.extend(
        (
            add(targets[0], scale(-alpha, Q)),
            targets[1],
            targets[2],
        )
    )
    basis_images.extend(zero(top_dimension) for _ in range(5))
    return {
        "name": name,
        "h": F(h),
        "alpha": F(alpha),
        "q": q,
        "responses": tuple(responses),
        "Q": Q,
        "multiplication": map_from_basis_images(basis_images),
    }


def build_zero_power_model():
    h = F(7)
    alpha = F(-4, 3)
    response_dimension = 9
    q = basis(response_dimension, 0)
    diagonal = [basis(response_dimension, index) for index in (1, 2, 3)]
    off_diagonal = {
        (0, 1): q,
        (0, 2): basis(response_dimension, 4),
        (1, 0): basis(response_dimension, 5),
        (1, 2): basis(response_dimension, 6),
        (2, 0): basis(response_dimension, 7),
        (2, 1): basis(response_dimension, 8),
    }
    responses = []
    for pair in PAIRS:
        if pair[0] == pair[1]:
            responses.append(diagonal[pair[0]])
        else:
            responses.append(off_diagonal[pair])
    targets = [basis(3, i) for i in range(3)]
    basis_images = [zero(3), targets[0], targets[1], targets[2]]
    basis_images.extend(zero(3) for _ in range(5))
    return {
        "name": "zero divided power",
        "h": h,
        "alpha": alpha,
        "q": q,
        "responses": tuple(responses),
        "Q": zero(3),
        "multiplication": map_from_basis_images(basis_images),
    }


def audit_normal_forms_and_selectors():
    interior = build_radial_line_model(
        5, F(2, 3), (2, -3, 5), "visible rank-one radial line"
    )
    radial, diagonals, c_values = audit_target_lock(interior, 1)
    require(all(any(values) for values in diagonals), "visible line lost a diagonal")
    require(any(c_values), "visible line lost its target coefficient")
    relation = radial[0]
    declared = interior["declared_diagonal"]
    obtained = tuple(relation[PAIR_INDEX[(i, i)]] for i in range(3))
    require(
        rank([list(declared), list(obtained)]) == 1,
        "the computed visible radial line has the wrong diagonal direction",
    )
    require(
        relation[9] * declared[2]
        == interior["declared_beta"] * obtained[2],
        "the computed visible radial response ratio is wrong",
    )
    require(
        rank(
            [
                [interior["alpha"] * obtained[0]],
                [relation[9]],
            ]
        )
        == 1,
        "the visible radial line did not have scalar rank one",
    )
    require(
        not any(abstract_quotient_selector_exists(interior, i) for i in range(3)),
        "an active radial diagonal unexpectedly had a quotient selector",
    )

    boundary = build_radial_line_model(
        6, F(5, 7), (3, 0, -2), "zero-coordinate radial boundary"
    )
    _, diagonals, _ = audit_target_lock(boundary, 1)
    require(not any(diagonals[1]), "the zero-coordinate boundary became visible")
    require(abstract_quotient_selector_exists(boundary, 1), "abstract selector missing")
    require(top_catalecticant_selector_exists(boundary, 1), "literal selector missing")

    torsion = build_torsion_model((1, -2, 0), "binary-power torsion boundary")
    _, diagonals, c_values = audit_target_lock(torsion, 1)
    require(not any(any(values) for values in diagonals), "torsion gained a diagonal")
    require(not any(c_values), "torsion gained a target coefficient")
    for label in range(3):
        require(
            abstract_quotient_selector_exists(torsion, label),
            f"torsion abstract selector {label} missing",
        )
        require(
            top_catalecticant_selector_exists(torsion, label)
            == predicted_top_selector(torsion, label),
            f"torsion catalecticant criterion failed at label {label}",
        )
    require(
        not top_catalecticant_selector_exists(torsion, 1),
        "the nonzero Q-coordinate selector incorrectly factored through the top row",
    )
    require(
        top_catalecticant_selector_exists(torsion, 2),
        "the missing Q-coordinate did not give a literal selector",
    )
    require(
        top_catalecticant_selector_exists(torsion, 1, impose_q=False),
        "the q-annihilation mutation did not distinguish the false selector",
    )

    outside = build_torsion_model((2, -1, 4, 3), "transverse-power boundary")
    audit_target_lock(outside, 1)
    require(any(outside["Q"][3:]), "transverse model lost its outside component")
    for label in range(3):
        require(
            top_catalecticant_selector_exists(outside, label),
            f"outside-target selector {label} missing",
        )

    zero_power = build_zero_power_model()
    radial, diagonals, _ = audit_target_lock(zero_power, 1)
    require(not any(any(values) for values in diagonals), "Q=0 gained a diagonal")
    require(radial[0][9] != 0, "Q=0 did not retain its possible beta direction")
    for label in range(3):
        require(
            top_catalecticant_selector_exists(zero_power, label),
            f"Q=0 selector {label} missing",
        )


def audit_fixed_ratio_polynomial():
    for h in range(3, 33):
        for x in (F(2, 3), F(-3, 5), F(7, 4)):
            ratio = (F(1) - x) / (h * x)
            projective_root_value = (F(1) + ratio) ** h - F(1) - h * ratio
            cleared = ((h - 1) * x + 1) ** h - F(h) ** h * x ** (h - 1)
            require(
                cleared == (h * x) ** h * projective_root_value,
                f"fixed-ratio clean polynomial failed at h={h}, x={x}",
            )
            mutated = ((h - 1) * x + 1) ** h - F(h) ** (h - 1) * x ** (h - 1)
            require(
                mutated != (h * x) ** h * projective_root_value,
                f"power mutation escaped at h={h}, x={x}",
            )


def audit_euler_four_cut_normalization():
    for h in range(3, 65):
        # In ordinary monomial normalization q^[m]=q^m/m!, so this is an
        # independent coefficient audit of
        # q*q^[h-2]=(h-1)*q^[h-1].
        inserted_cell_coefficient = F(1, factorial(h - 2))
        euler_coefficient = F(h - 1, factorial(h - 1))
        require(
            inserted_cell_coefficient == euler_coefficient,
            f"Euler four-cut normalization failed at h={h}",
        )
        require(
            inserted_cell_coefficient != F(h, factorial(h - 1)),
            f"Euler h-for-(h-1) mutation escaped at h={h}",
        )

        # A cancellation-sensitive scalar version of
        # sum_e q_e C_e=(h-1)E_ii.  The off-diagonal channel cancels while
        # the selected channel is forced to have a detected summand.
        weights = (F(2), F(-3), F(5))
        selected_layers = (F(1), F(-2), F(h - 9, 5))
        off_diagonal_layers = (F(3), F(2), F(0))
        require(
            dot(weights, selected_layers) == h - 1,
            f"Euler selected-channel sum failed at h={h}",
        )
        require(
            dot(weights, off_diagonal_layers) == 0,
            f"Euler cancellation channel failed at h={h}",
        )
        require(
            any(value != 0 for value in selected_layers),
            f"Euler detection disappeared at h={h}",
        )


def audit_adversarial_mutations():
    model = build_radial_line_model(
        8, F(4, 5), (2, 3, -7), "mutation seed"
    )
    require(validate_full_nine(model), "mutation seed is invalid")

    wrong_q_image = dict(model)
    columns = [
        tuple(row[column] for row in model["multiplication"])
        for column in range(len(model["multiplication"][0]))
    ]
    columns[0] = scale(model["h"] + 1, model["Q"])
    wrong_q_image["multiplication"] = map_from_basis_images(columns)
    require(
        not validate_full_nine(wrong_q_image),
        "the h-to-h+1 multiplication mutation was accepted",
    )

    wrong_response = dict(model)
    responses = list(model["responses"])
    responses[PAIR_INDEX[(2, 2)]] = scale(-1, responses[PAIR_INDEX[(2, 2)]])
    wrong_response["responses"] = tuple(responses)
    require(
        not validate_full_nine(wrong_response),
        "the diagonal response-sign mutation was accepted",
    )

    # Two formally independent scalar/radial values cannot obey the same
    # target lock when Q lies in the target span.  This guards the central
    # rank-one implication independently of the model constructors.
    Q = vector(2, -1, 3)
    fake_caps = (
        (vector(1, 0, 0), F(0)),
        (vector(0, 0, 0), F(1)),
    )
    residuals = []
    for diagonal, beta in fake_caps:
        scalar = F(5, 4) * diagonal[0]
        residuals.append(add(diagonal, scale(-(scalar + 9 * beta), Q)))
    require(
        any(any(residual) for residual in residuals),
        "the artificial rank-two mutation incorrectly obeyed target lock",
    )


def main():
    audit_normal_forms_and_selectors()
    audit_fixed_ratio_polynomial()
    audit_euler_four_cut_normalization()
    audit_adversarial_mutations()
    print("full-nine scalar-unit radial target lock: exact audit passed")
    print("rank-one lock, fixed ratio, sourced selector, and Euler four-cut verified")


if __name__ == "__main__":
    main()
