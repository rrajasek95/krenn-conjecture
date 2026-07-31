#!/usr/bin/env python3
"""Exact audit of the Hessian-kernel full-nine frame-transport guard.

The calculation uses only ``fractions.Fraction``.  It verifies a literal
fixed-block one-parameter packet with

* a nonzero Hessian-kernel internal tangent;
* constant six-site hafnian and every raw four-site cofactor;
* all nine mixed full-nine rows, zero normalized leakage, and constant
  normalized direct block;
* nonzero derivatives of all three normalized diagonal target frames; and
* zero two- and three-cycle holonomy of the induced frame-defect matrix.

It also audits the universal power-free source-overlap identities and the
minimal two-polar linear-algebra guard for full frame horizontality.
"""

from fractions import Fraction
from itertools import combinations, permutations


Q = Fraction
ZERO = Q(0)
ONE = Q(1)
VERTICES = tuple(range(6))
EDGES = tuple(combinations(VERTICES, 2))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def zeros(rows, columns):
    return [[ZERO for _ in range(columns)] for _ in range(rows)]


def identity(size):
    result = zeros(size, size)
    for index in range(size):
        result[index][index] = ONE
    return result


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matrix_add(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def matrix_scale(scalar, matrix):
    return [[scalar * entry for entry in row] for row in matrix]


def matrix_multiply(left, right):
    require(len(left[0]) == len(right), "matrix dimensions do not match")
    return [
        [
            sum(
                (left[i][k] * right[k][j] for k in range(len(right))),
                ZERO,
            )
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def matrix_vector(matrix, vector):
    return [
        sum((matrix[i][j] * vector[j] for j in range(len(vector))), ZERO)
        for i in range(len(matrix))
    ]


def dot(left, right):
    return sum((x * y for x, y in zip(left, right)), ZERO)


def matrix_inverse(matrix):
    size = len(matrix)
    augmented = [
        list(matrix[row])
        + [ONE if row == column else ZERO for column in range(size)]
        for row in range(size)
    ]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if augmented[row][column]),
            None,
        )
        require(pivot is not None, "matrix is singular")
        augmented[column], augmented[pivot] = (
            augmented[pivot],
            augmented[column],
        )
        value = augmented[column][column]
        augmented[column] = [entry / value for entry in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            value = augmented[row][column]
            augmented[row] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(
                    augmented[row], augmented[column]
                )
            ]
    return [row[size:] for row in augmented]


def matrix_rank(matrix):
    if not matrix:
        return 0
    work = [list(row) for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        value = work[rank][column]
        work[rank] = [entry / value for entry in work[rank]]
        for row in range(rows):
            if row == rank:
                continue
            value = work[row][column]
            if value:
                work[row] = [
                    entry - value * pivot_entry
                    for entry, pivot_entry in zip(work[row], work[rank])
                ]
        rank += 1
        if rank == rows:
            break
    return rank


def is_zero_matrix(matrix):
    return all(entry == ZERO for row in matrix for entry in row)


def unit_vector(index):
    return [ONE if position == index else ZERO for position in range(3)]


def outer(left, right):
    return [
        [left[i] * right[j] for j in range(len(right))]
        for i in range(len(left))
    ]


def edge(a, b):
    return tuple(sorted((a, b)))


def hafnian(edge_values, subset):
    subset = tuple(sorted(subset))
    if not subset:
        return ONE
    first = subset[0]
    total = ZERO
    for second in subset[1:]:
        remainder = tuple(
            vertex for vertex in subset if vertex not in (first, second)
        )
        total += edge_values.get(edge(first, second), ZERO) * hafnian(
            edge_values, remainder
        )
    return total


def edge_product(left, right):
    """Ordinary square-zero product of two scalar edge arrays."""
    result = {subset: ZERO for subset in combinations(VERTICES, 4)}
    for left_edge, left_value in left.items():
        for right_edge, right_value in right.items():
            if set(left_edge).isdisjoint(right_edge):
                subset = tuple(sorted(left_edge + right_edge))
                result[subset] += left_value * right_value
    return result


def cofactor_matrix(edge_values):
    result = zeros(6, 6)
    for i in VERTICES:
        for j in VERTICES:
            if i != j:
                complement = tuple(
                    vertex for vertex in VERTICES if vertex not in (i, j)
                )
                result[i][j] = hafnian(edge_values, complement)
    return result


def submatrix(matrix, rows, columns):
    return [[matrix[row][column] for column in columns] for row in rows]


def polynomial_matrix_product(left_coefficients, right_coefficients):
    degree = len(left_coefficients) + len(right_coefficients) - 2
    rows = len(left_coefficients[0])
    columns = len(right_coefficients[0][0])
    result = [zeros(rows, columns) for _ in range(degree + 1)]
    for left_degree, left in enumerate(left_coefficients):
        for right_degree, right in enumerate(right_coefficients):
            result[left_degree + right_degree] = matrix_add(
                result[left_degree + right_degree],
                matrix_multiply(left, right),
            )
    return result


def diagonal_matrix(entries):
    result = zeros(len(entries), len(entries))
    for index, value in enumerate(entries):
        result[index][index] = Q(value)
    return result


def transport_rows(form):
    """Rows of (X,Y) -> X^T form + form Y, with 18 variables."""
    rows = []
    for i in range(3):
        for j in range(3):
            row = [ZERO for _ in range(18)]
            for k in range(3):
                row[3 * k + i] += form[k][j]
                row[9 + 3 * k + j] += form[i][k]
            rows.append(row)
    return rows


def all_frame_rows():
    rows = []
    for colour in range(3):
        rows.extend(transport_rows(diagonal_matrix(
            [ONE if index == colour else ZERO for index in range(3)]
        )))
    return rows


def bilinear(matrix, left, right):
    return dot(left, matrix_vector(matrix, right))


def matrix_from_columns(columns):
    return [list(row) for row in zip(*columns)]


def block_system(q, z, n_matrix, y_matrix, direct):
    """Construct one literal fixed 8-site block array in physical bases."""
    base_colours = (0, 0, 1, 1, 2, 2)
    tangent_colours = (1, 1, 2, 2, 0, 0)
    bases = {}
    base_vectors = {}
    tangent_vectors = {}
    for site in VERTICES:
        first = base_colours[site]
        second = tangent_colours[site]
        third = next(colour for colour in range(3) if colour not in (first, second))
        basis = matrix_from_columns(
            (unit_vector(first), unit_vector(second), unit_vector(third))
        )
        bases[site] = basis
        base_vectors[site] = unit_vector(first)
        tangent_vectors[site] = unit_vector(second)

    blocks = {}

    def install(left, right, matrix):
        blocks[left, right] = matrix
        blocks[right, left] = transpose(matrix)

    install("p", "q", direct)

    for left, right in EDGES:
        adapted = zeros(3, 3)
        adapted[0][0] = q.get((left, right), ZERO)
        adapted[1][0] = z.get((left, right), ZERO)
        actual = matrix_multiply(
            transpose(matrix_inverse(bases[left])),
            matrix_multiply(adapted, matrix_inverse(bases[right])),
        )
        install(left, right, actual)

    for site in VERTICES:
        p_base = [ZERO, ZERO, ZERO]
        p_tangent = [ZERO, ZERO, ZERO]
        s_base = [ZERO, ZERO, ZERO]
        s_tangent = [ZERO, ZERO, ZERO]
        if site < 3:
            p_base[site] = ONE
            p_tangent = list(n_matrix[site])
        else:
            shore_index = site - 3
            s_base[shore_index] = ONE
            s_tangent = list(y_matrix[shore_index])

        p_adapted = zeros(3, 3)
        s_adapted = zeros(3, 3)
        for colour in range(3):
            p_adapted[colour][0] = p_base[colour]
            p_adapted[colour][1] = p_tangent[colour]
            s_adapted[colour][0] = s_base[colour]
            s_adapted[colour][1] = s_tangent[colour]
        install(
            "p", site,
            matrix_multiply(p_adapted, matrix_inverse(bases[site])),
        )
        install(
            "q", site,
            matrix_multiply(s_adapted, matrix_inverse(bases[site])),
        )

    return blocks, base_vectors, tangent_vectors


def add_elements(*elements):
    result = {}
    for element in elements:
        for monomial, coefficient in element.items():
            result[monomial] = result.get(monomial, ZERO) + coefficient
            if result[monomial] == ZERO:
                del result[monomial]
    return result


def scale_element(scalar, element):
    if scalar == ZERO:
        return {}
    return {
        monomial: scalar * coefficient
        for monomial, coefficient in element.items()
        if scalar * coefficient
    }


def multiply_elements(left, right):
    result = {}
    for left_monomial, left_coefficient in left.items():
        left_sites = {site for site, _ in left_monomial}
        for right_monomial, right_coefficient in right.items():
            right_sites = {site for site, _ in right_monomial}
            if not left_sites.isdisjoint(right_sites):
                continue
            monomial = tuple(sorted(left_monomial + right_monomial))
            result[monomial] = (
                result.get(monomial, ZERO)
                + left_coefficient * right_coefficient
            )
            if result[monomial] == ZERO:
                del result[monomial]
    return result


def linear_form(blocks, endpoint, colour, common_sites):
    result = {}
    for site in common_sites:
        matrix = blocks[endpoint, site]
        for local_colour in range(3):
            coefficient = matrix[colour][local_colour]
            if coefficient:
                result[((site, local_colour),)] = coefficient
    return result


def internal_quadratic(blocks, common_sites):
    result = {}
    for left, right in combinations(common_sites, 2):
        matrix = blocks[left, right]
        for left_colour in range(3):
            for right_colour in range(3):
                coefficient = matrix[left_colour][right_colour]
                if coefficient:
                    monomial = ((left, left_colour), (right, right_colour))
                    result[monomial] = coefficient
    return result


def audit_power_free_overlap(blocks):
    """Audit equations (7) of the automatic two-chart packet."""
    p_site = "p"
    q_site = "q"
    r_site = 0
    s_site = 1
    common = (2, 3, 4, 5)
    internal = internal_quadratic(blocks, common)
    checks = 0
    for i in range(3):
        x = linear_form(blocks, p_site, i, common)
        for j in range(3):
            y = linear_form(blocks, q_site, j, common)
            a_value = blocks[p_site, q_site][i][j]
            fij = add_elements(
                scale_element(a_value, internal),
                multiply_elements(x, y),
            )
            for k in range(3):
                t_form = linear_form(blocks, r_site, k, common)
                b_value = blocks[p_site, r_site][i][k]
                gik = add_elements(
                    scale_element(b_value, internal),
                    multiply_elements(x, t_form),
                )
                first_left = add_elements(
                    multiply_elements(fij, t_form),
                    scale_element(-ONE, multiply_elements(gik, y)),
                )
                at_minus_by = add_elements(
                    scale_element(a_value, t_form),
                    scale_element(-b_value, y),
                )
                first_residual = add_elements(
                    first_left,
                    scale_element(
                        -ONE, multiply_elements(at_minus_by, internal)
                    ),
                )
                require(not first_residual, "power-free overlap equation failed")
                checks += 1

                for ell in range(3):
                    v_form = linear_form(blocks, s_site, ell, common)
                    e_value = blocks[p_site, s_site][i][ell]
                    f_value = blocks[q_site, s_site][j][ell]
                    u_value = blocks[r_site, s_site][k][ell]
                    h_form = add_elements(
                        scale_element(a_value, v_form),
                        scale_element(e_value, y),
                        scale_element(f_value, x),
                    )
                    n_form = add_elements(
                        scale_element(b_value, v_form),
                        scale_element(e_value, t_form),
                        scale_element(u_value, x),
                    )
                    second_left = add_elements(
                        scale_element(u_value, fij),
                        multiply_elements(t_form, h_form),
                        scale_element(-f_value, gik),
                        scale_element(-ONE, multiply_elements(y, n_form)),
                    )
                    second_right = add_elements(
                        multiply_elements(at_minus_by, v_form),
                        scale_element(
                            a_value * u_value - b_value * f_value,
                            internal,
                        ),
                    )
                    residual = add_elements(
                        second_left, scale_element(-ONE, second_right)
                    )
                    require(not residual, "curvature overlap equation failed")
                    checks += 1
    require(checks == 108, "unexpected overlap check count")
    return checks


def audit_guard():
    q = {
        edge(0, 1): ONE,
        edge(0, 2): ONE,
        edge(0, 4): ONE,
        edge(0, 5): ONE,
        edge(1, 2): ONE,
        edge(1, 4): ONE,
        edge(2, 3): ONE,
        edge(3, 4): ONE,
        edge(3, 5): ONE,
    }
    z = {edge(0, 1): ONE, edge(1, 3): -ONE}
    require(any(z.values()), "the Hessian-kernel tangent vanished")
    require(
        all(value == ZERO for value in edge_product(z, q).values()),
        "z q is nonzero",
    )
    require(
        all(value == ZERO for value in edge_product(z, z).values()),
        "z squared is nonzero",
    )

    f_value = hafnian(q, VERTICES)
    require(f_value == Q(4), "unexpected six-site hafnian")
    hessian = cofactor_matrix(q)
    x_shore = (0, 1, 2)
    y_shore = (3, 4, 5)
    cross = submatrix(hessian, x_shore, y_shore)
    expected_cross = [
        [ZERO, ONE, Q(2)],
        [ZERO, Q(2), Q(2)],
        [ONE, ONE, ONE],
    ]
    require(cross == expected_cross, "wrong cross-cofactor matrix")
    require(matrix_rank(cross) == 3, "cross-cofactor matrix is singular")

    left_vector = [ONE, ONE, ONE]
    right_vector = [ONE, ONE, Q(-2)]
    n_matrix = outer(left_vector, right_vector)
    require(is_zero_matrix(matrix_multiply(n_matrix, n_matrix)), "N^2 != 0")
    y_matrix = matrix_scale(
        -ONE,
        matrix_multiply(
            matrix_multiply(matrix_inverse(cross), transpose(n_matrix)),
            cross,
        ),
    )
    require(is_zero_matrix(matrix_multiply(y_matrix, y_matrix)), "Y^2 != 0")
    require(
        is_zero_matrix(
            matrix_add(
                matrix_multiply(transpose(n_matrix), cross),
                matrix_multiply(cross, y_matrix),
            )
        ),
        "the connection does not stabilize the cross cofactor",
    )

    direct = matrix_scale(-ONE / f_value, cross)
    blocks, base_vectors, tangent_vectors = block_system(
        q, z, n_matrix, y_matrix, direct
    )

    # Audit the literal fixed-block evaluations.
    evaluated_q = {}
    evaluated_z = {}
    second_order = {}
    for left, right in EDGES:
        matrix = blocks[left, right]
        evaluated_q[left, right] = bilinear(
            matrix, base_vectors[left], base_vectors[right]
        )
        evaluated_z[left, right] = (
            bilinear(matrix, tangent_vectors[left], base_vectors[right])
            + bilinear(matrix, base_vectors[left], tangent_vectors[right])
        )
        second_order[left, right] = bilinear(
            matrix, tangent_vectors[left], tangent_vectors[right]
        )
    require(
        all(evaluated_q[e] == q.get(e, ZERO) for e in EDGES),
        "fixed blocks do not evaluate to q",
    )
    require(
        all(evaluated_z[e] == z.get(e, ZERO) for e in EDGES),
        "fixed blocks do not evaluate to z",
    )
    require(
        all(value == ZERO for value in second_order.values()),
        "the physical q-line has a quadratic correction",
    )

    p_base = zeros(6, 3)
    p_tangent = zeros(6, 3)
    s_base = zeros(6, 3)
    s_tangent = zeros(6, 3)
    for site in VERTICES:
        for colour in range(3):
            p_base[site][colour] = bilinear(
                blocks["p", site], unit_vector(colour), base_vectors[site]
            )
            p_tangent[site][colour] = bilinear(
                blocks["p", site], unit_vector(colour), tangent_vectors[site]
            )
            s_base[site][colour] = bilinear(
                blocks["q", site], unit_vector(colour), base_vectors[site]
            )
            s_tangent[site][colour] = bilinear(
                blocks["q", site], unit_vector(colour), tangent_vectors[site]
            )
    require(submatrix(p_base, x_shore, range(3)) == identity(3), "wrong A(0)")
    require(submatrix(p_tangent, x_shore, range(3)) == n_matrix, "wrong dot A")
    require(submatrix(s_base, y_shore, range(3)) == identity(3), "wrong B(0)")
    require(submatrix(s_tangent, y_shore, range(3)) == y_matrix, "wrong dot B")
    require(
        all(p_base[site] == [ZERO] * 3 and p_tangent[site] == [ZERO] * 3
            for site in y_shore),
        "P leaks onto the opposite shore",
    )
    require(
        all(s_base[site] == [ZERO] * 3 and s_tangent[site] == [ZERO] * 3
            for site in x_shore),
        "S leaks onto the opposite shore",
    )

    # Every pure target product is identically zero on the physical line.
    for colour in range(3):
        require(
            any(
                base_vectors[site][colour] == ZERO
                and tangent_vectors[site][colour] == ZERO
                for site in VERTICES
            ),
            "a pure target product survives",
        )

    # q_t^[2] and q_t^[3] are constant because z q = z^[2] = 0.
    for rational_time in (Q(-3, 2), ZERO, Q(2, 3), Q(5)):
        q_time = {
            e: q.get(e, ZERO) + rational_time * z.get(e, ZERO)
            for e in EDGES
        }
        require(hafnian(q_time, VERTICES) == f_value, "F(t) is not constant")
        require(
            cofactor_matrix(q_time) == hessian,
            "a raw cofactor changes on the kernel line",
        )

    # Audit all coefficients of the nine mixed full-nine rows.
    h_times_s0 = matrix_multiply(hessian, s_base)
    h_times_s1 = matrix_multiply(hessian, s_tangent)
    mixed_coefficients = [
        matrix_multiply(transpose(p_base), h_times_s0),
        matrix_add(
            matrix_multiply(transpose(p_tangent), h_times_s0),
            matrix_multiply(transpose(p_base), h_times_s1),
        ),
        matrix_multiply(transpose(p_tangent), h_times_s1),
    ]
    require(
        is_zero_matrix(matrix_add(mixed_coefficients[0], matrix_scale(f_value, direct))),
        "the base full-nine rows fail",
    )
    require(is_zero_matrix(mixed_coefficients[1]), "the first full-nine jet fails")
    require(is_zero_matrix(mixed_coefficients[2]), "the second full-nine jet fails")
    require(mixed_coefficients[0] == cross, "unexpected physical cofactor response")

    # A^-T and B^-1 are exact linear polynomials because N^2=Y^2=0.
    a_inverse_transpose = [identity(3), matrix_scale(-ONE, transpose(n_matrix))]
    b_inverse = [identity(3), matrix_scale(-ONE, y_matrix)]
    normalized_h = polynomial_matrix_product(
        polynomial_matrix_product(a_inverse_transpose, [cross]), b_inverse
    )
    normalized_c = polynomial_matrix_product(
        polynomial_matrix_product(a_inverse_transpose, [direct]), b_inverse
    )
    require(normalized_h[0] == cross, "wrong normalized cofactor base")
    require(normalized_c[0] == direct, "wrong normalized direct base")
    require(
        all(is_zero_matrix(coefficient) for coefficient in normalized_h[1:]),
        "normalized cofactor leakage is nonzero",
    )
    require(
        all(is_zero_matrix(coefficient) for coefficient in normalized_c[1:]),
        "normalized direct block drifts",
    )

    # Exact frame defects Delta_c = dot T_c.
    deltas = []
    for colour in range(3):
        matrix_unit = diagonal_matrix(
            [ONE if index == colour else ZERO for index in range(3)]
        )
        delta = matrix_scale(
            -ONE,
            matrix_add(
                matrix_multiply(transpose(n_matrix), matrix_unit),
                matrix_multiply(matrix_unit, y_matrix),
            ),
        )
        require(not is_zero_matrix(delta), f"frame {colour} is accidentally horizontal")
        deltas.append(delta)
    expected_deltas = [
        [
            [Q(-7, 2), Q(-10), Q(-25, 2)],
            [Q(-1), ZERO, ZERO],
            [Q(2), ZERO, ZERO],
        ],
        [
            [ZERO, Q(-1), ZERO],
            [ZERO, Q(-1), ZERO],
            [ZERO, Q(2), ZERO],
        ],
        [
            [ZERO, ZERO, Q(-1)],
            [ZERO, ZERO, Q(-1)],
            [Q(1, 2), Q(2), Q(9, 2)],
        ],
    ]
    require(deltas == expected_deltas, "exact frame-defect matrices changed")

    # Phi reconstructs the leakage connection modulo a diagonal coboundary.
    phi = zeros(3, 3)
    for i in range(3):
        for j in range(3):
            phi[i][j] = (
                -sum(
                    (deltas[k][i][k] * direct[k][j]
                     for k in range(3) if k != i),
                    ZERO,
                )
                -sum(
                    (direct[i][k] * deltas[k][k][j]
                     for k in range(3) if k != j),
                    ZERO,
                )
                -direct[i][j] * deltas[j][j][j]
            )
    expected_phi = [
        [ZERO, ZERO, Q(3, 2)],
        [ZERO, ZERO, Q(3, 2)],
        [Q(-3, 4), Q(-3, 4), ZERO],
    ]
    require(phi == expected_phi, "exact Phi matrix changed")
    leakage_connection = matrix_add(
        matrix_multiply(transpose(n_matrix), direct),
        matrix_multiply(direct, y_matrix),
    )
    require(is_zero_matrix(leakage_connection), "Lambda/F is nonzero")
    diagonal_connection = [n_matrix[index][index] for index in range(3)]
    reconstructed = zeros(3, 3)
    for i in range(3):
        for j in range(3):
            reconstructed[i][j] = (
                phi[i][j]
                + (diagonal_connection[i] - diagonal_connection[j])
                * direct[i][j]
            )
    require(reconstructed == leakage_connection, "Phi reconstruction failed")
    require(not is_zero_matrix(phi), "Phi is vacuously zero")

    two_cycle_checks = 0
    for i, j in combinations(range(3), 2):
        phi_holonomy = (
            direct[j][i] * phi[i][j]
            + direct[i][j] * phi[j][i]
        )
        leakage_holonomy = (
            direct[j][i] * leakage_connection[i][j]
            + direct[i][j] * leakage_connection[j][i]
        )
        require(phi_holonomy == leakage_holonomy == ZERO, "two-cycle holonomy survived")
        two_cycle_checks += 1

    three_cycle_checks = 0
    for i, j, k in permutations(range(3), 3):
        phi_holonomy = (
            direct[j][k] * direct[k][i] * phi[i][j]
            + direct[k][i] * direct[i][j] * phi[j][k]
            + direct[i][j] * direct[j][k] * phi[k][i]
        )
        leakage_holonomy = (
            direct[j][k] * direct[k][i] * leakage_connection[i][j]
            + direct[k][i] * direct[i][j] * leakage_connection[j][k]
            + direct[i][j] * direct[j][k] * leakage_connection[k][i]
        )
        require(phi_holonomy == leakage_holonomy == ZERO, "three-cycle holonomy survived")
        three_cycle_checks += 1
    selected_three_cycle_terms = (
        direct[1][2] * direct[2][0] * phi[0][1],
        direct[2][0] * direct[0][1] * phi[1][2],
        direct[0][1] * direct[1][2] * phi[2][0],
    )
    require(
        selected_three_cycle_terms
        == (ZERO, Q(3, 32), Q(-3, 32)),
        "the selected 0->1->2->0 cycle terms changed",
    )
    require(
        sum(selected_three_cycle_terms, ZERO) == ZERO
        and any(selected_three_cycle_terms),
        "the selected three-cycle cancellation is vacuous",
    )
    require(
        direct[2][0] * phi[0][2] != ZERO
        and direct[0][2] * phi[2][0] != ZERO,
        "the cycle cancellation is vacuous",
    )

    overlap_checks = audit_power_free_overlap(blocks)

    # Linear-algebra minimality: one diagonal polar leaves nine connection
    # dimensions; two regular diagonal polars leave exactly the reciprocal
    # diagonal three-torus, which is the full frame-horizontal kernel.
    frame_rows = all_frame_rows()
    polar_zero = transport_rows(diagonal_matrix((1, 1, 1)))
    polar_one = transport_rows(diagonal_matrix((1, 2, 4)))
    require(matrix_rank(frame_rows) == 15, "wrong frame-defect rank")
    require(matrix_rank(polar_zero) == 9, "one polar has the wrong rank")
    require(
        matrix_rank(polar_zero + polar_one) == 15,
        "two regular diagonal polars do not force horizontality",
    )
    require(
        matrix_rank(polar_zero + polar_one + frame_rows) == 15,
        "two-polar kernel differs from the horizontal kernel",
    )
    require(matrix_rank(transport_rows(cross)) == 9, "wrong mixed-row rank")
    require(
        matrix_rank(transport_rows(cross) + frame_rows) == 17,
        "the dense direct form has the wrong horizontal stabilizer",
    )

    return {
        "overlap_checks": overlap_checks,
        "two_cycles": two_cycle_checks,
        "three_cycles": three_cycle_checks,
        "frame_rank": matrix_rank(frame_rows),
    }


def main():
    result = audit_guard()
    print("hessian-kernel full-nine frame-transport defect guard: PASS")
    print("  nonzero kernel tangent; F and all raw cofactors constant")
    print("  nine mixed rows exact; normalized leakage/direct drift zero")
    print("  all three frame derivatives nonzero")
    print(
        "  Phi cycle holonomy: "
        f"{result['two_cycles']} two-cycles, "
        f"{result['three_cycles']} oriented three-cycles"
    )
    print(f"  universal source-overlap identities: {result['overlap_checks']}")
    print(f"  frame-defect rank: {result['frame_rank']} (kernel dimension 3)")


if __name__ == "__main__":
    main()
