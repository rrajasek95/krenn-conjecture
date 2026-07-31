#!/usr/bin/env python3
"""Exact audit of an h=3 adjacent-chart source-grade cycle module.

The module deliberately retains the source grades instead of identifying
their evaluated sums.  It couples

* compatible ``pq`` and ``pr`` selector words from one eight-site word;
* all three labelled diagonal four-cut defects and their 3-cycle;
* a cycle-projected target-zero row;
* the curvature/direct-double and connection/normal Euler pairs; and
* the canonical target-cubic Hankel candidate on the same binary cap line.

This direct-sum/source-grade representation is not one complete physical
full-nine source.  It satisfies every retained relation but has
``F0 * Psi = 0`` and ``chi * (AU-BF) = 1``.  A row-rank calculation isolates
an independent candidate transgression row in this presentation.  The final
calculation verifies that multiplication by the target cubic ``v^3`` leaves
three independent Hankel residuals at h=3.
"""

from fractions import Fraction
from itertools import combinations


Q = Fraction
ZERO = Q(0)
ONE = Q(1)


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


def is_zero_matrix(matrix):
    return all(entry == ZERO for row in matrix for entry in row)


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
        pivot_value = work[rank][column]
        work[rank] = [entry / pivot_value for entry in work[rank]]
        for row in range(rows):
            if row == rank:
                continue
            coefficient = work[row][column]
            if coefficient:
                work[row] = [
                    entry - coefficient * pivot_entry
                    for entry, pivot_entry in zip(work[row], work[rank])
                ]
        rank += 1
        if rank == rows:
            break
    return rank


def dot(left, right):
    return sum((x * y for x, y in zip(left, right)), ZERO)


def matrix_inner(left, right):
    return sum(
        (
            left[i][j] * right[i][j]
            for i in range(len(left))
            for j in range(len(left[0]))
        ),
        ZERO,
    )


def matrix_subtract(left, right):
    return matrix_add(left, matrix_scale(-ONE, right))


def matrix_column(matrix, column):
    return [row[column] for row in matrix]


def outer_product(left, right):
    return [[left_entry * right_entry for right_entry in right] for left_entry in left]


def edge(left, right):
    return tuple(sorted((left, right)))


def hafnian(edge_values, vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ONE
    first = vertices[0]
    total = ZERO
    for second in vertices[1:]:
        remainder = tuple(
            vertex for vertex in vertices if vertex not in (first, second)
        )
        total += edge_values.get(edge(first, second), ZERO) * hafnian(
            edge_values, remainder
        )
    return total


def edge_product(left, right, vertices):
    result = {subset: ZERO for subset in combinations(vertices, 4)}
    for left_edge, left_value in left.items():
        for right_edge, right_value in right.items():
            if set(left_edge).isdisjoint(right_edge):
                subset = tuple(sorted(left_edge + right_edge))
                result[subset] += left_value * right_value
    return result


def cofactor_matrix(edge_values, vertices):
    result = zeros(len(vertices), len(vertices))
    for i in vertices:
        for j in vertices:
            if i != j:
                complement = tuple(v for v in vertices if v not in (i, j))
                result[i][j] = hafnian(edge_values, complement)
    return result


def submatrix(matrix, rows, columns):
    return [[matrix[row][column] for column in columns] for row in rows]


def poly_add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for mask, coefficient in polynomial.items():
            result[mask] = result.get(mask, ZERO) + coefficient
    return {mask: value for mask, value in result.items() if value}


def poly_scale(scalar, polynomial):
    return {
        mask: scalar * coefficient
        for mask, coefficient in polynomial.items()
        if scalar * coefficient
    }


def poly_multiply(left, right):
    result = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = result.get(mask, ZERO) + left_value * right_value
    return {mask: value for mask, value in result.items() if value}


def monomial(*sites):
    mask = 0
    for site in sites:
        require(not (mask & (1 << site)), "a square-zero monomial repeated a site")
        mask |= 1 << site
    return {mask: ONE}


def poly_coefficient(polynomial, *sites):
    mask = 0
    for site in sites:
        mask |= 1 << site
    return polynomial.get(mask, ZERO)


def check_compatible_words():
    global_word = {
        "p": 0,
        "q": 1,
        "r": 1,
        "s": 2,
        "d0": 0,
        "d1": 0,
        "d2": 1,
        "d3": 2,
    }
    pq_sites = ("d0", "d1", "r", "d2", "s", "d3")
    pr_sites = ("d0", "d1", "q", "d2", "s", "d3")
    pq_word = tuple(global_word[site] for site in pq_sites)
    pr_word = tuple(global_word[site] for site in pr_sites)
    expected = (0, 0, 1, 1, 2, 2)
    require(pq_word == pr_word == expected, "the adjacent selector words disagree")
    require(
        all(pq_word.count(colour) == 2 for colour in range(3)),
        "the pq selector word is not separating",
    )
    require(
        all(pr_word.count(colour) == 2 for colour in range(3)),
        "the pr selector word is not separating",
    )
    shared_sites = ("s", "d0", "d1", "d2", "d3")
    require(
        tuple(global_word[site] for site in shared_sites) == (2, 0, 0, 1, 2),
        "the charts do not retain one common-complement word",
    )
    exposed_labels = tuple(global_word[site] for site in ("p", "q", "r", "s"))
    require(
        exposed_labels == (0, 1, 1, 2) and len(set(exposed_labels)) > 1,
        "the crossed four-index target is not zero",
    )
    return "compatible_words"


def three_cycle(direct, matrix):
    return (
        direct[1][2] * direct[2][0] * matrix[0][1]
        + direct[2][0] * direct[0][1] * matrix[1][2]
        + direct[0][1] * direct[1][2] * matrix[2][0]
    )


def phi_from_deltas(deltas, direct):
    phi = zeros(3, 3)
    for i in range(3):
        for j in range(3):
            phi[i][j] = (
                -sum(
                    (
                        deltas[colour][i][colour] * direct[colour][j]
                        for colour in range(3)
                        if colour != i
                    ),
                    ZERO,
                )
                -sum(
                    (
                        direct[i][colour] * deltas[colour][colour][j]
                        for colour in range(3)
                        if colour != j
                    ),
                    ZERO,
                )
                -direct[i][j] * deltas[j][j][j]
            )
    return phi


def check_frame_anchor_cycle():
    vertices = tuple(range(6))
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
    tangent = {edge(0, 1): ONE, edge(1, 3): -ONE}
    require(
        all(value == ZERO for value in edge_product(tangent, q, vertices).values()),
        "the internal tangent is not in the hafnian Hessian kernel",
    )

    f0 = hafnian(q, vertices)
    require(f0 == Q(4), "the base six-site hafnian changed")
    cofactor = cofactor_matrix(q, vertices)
    cross = submatrix(cofactor, (0, 1, 2), (3, 4, 5))
    expected_cross = [
        [ZERO, ONE, Q(2)],
        [ZERO, Q(2), Q(2)],
        [ONE, ONE, ONE],
    ]
    require(cross == expected_cross, "the cross-cofactor matrix changed")
    direct = matrix_scale(-ONE / f0, cross)

    x_connection = [
        [ONE, ONE, Q(-2)],
        [ONE, ONE, Q(-2)],
        [ONE, ONE, Q(-2)],
    ]
    y_connection = [
        [Q(5, 2), Q(10), Q(25, 2)],
        [ZERO, ZERO, ZERO],
        [Q(-1, 2), Q(-2), Q(-5, 2)],
    ]
    require(
        is_zero_matrix(
            matrix_add(
                matrix_multiply(transpose(x_connection), cross),
                matrix_multiply(cross, y_connection),
            )
        ),
        "the selector connection does not stabilize the raw cofactor",
    )
    leakage_over_f0 = matrix_add(
        matrix_multiply(transpose(x_connection), direct),
        matrix_multiply(direct, y_connection),
    )
    require(is_zero_matrix(leakage_over_f0), "the normalized leakage is nonzero")

    deltas = []
    for colour in range(3):
        matrix_unit = zeros(3, 3)
        matrix_unit[colour][colour] = ONE
        delta = matrix_scale(
            -ONE,
            matrix_add(
                matrix_multiply(transpose(x_connection), matrix_unit),
                matrix_multiply(matrix_unit, y_connection),
            ),
        )
        require(not is_zero_matrix(delta), f"anchor cut {colour} vanished")
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
    require(deltas == expected_deltas, "the labelled four-cut anchors changed")

    phi = phi_from_deltas(deltas, direct)
    expected_phi = [
        [ZERO, ZERO, Q(3, 2)],
        [ZERO, ZERO, Q(3, 2)],
        [Q(-3, 4), Q(-3, 4), ZERO],
    ]
    require(phi == expected_phi, "the reconstructed Phi matrix changed")

    anchor_contributions = []
    for retained_colour in range(3):
        partial_deltas = []
        for colour in range(3):
            partial_deltas.append(
                deltas[colour] if colour == retained_colour else zeros(3, 3)
            )
        partial_phi = phi_from_deltas(partial_deltas, direct)
        anchor_contributions.append(three_cycle(direct, partial_phi))
    require(
        anchor_contributions == [Q(-9, 64), Q(-3, 32), Q(15, 64)],
        "the three labelled anchor contributions changed",
    )
    require(
        all(anchor_contributions) and sum(anchor_contributions, ZERO) == ZERO,
        "the three-anchor cancellation is vacuous",
    )

    psi_cycle = three_cycle(direct, phi)
    leakage_cycle = three_cycle(direct, leakage_over_f0)
    require(psi_cycle == leakage_cycle == ZERO, "the target-zero cycle survived")
    return {
        "tag": "frame_anchor_cycle",
        "f0": f0,
        "direct": direct,
        "psi": psi_cycle,
        "leakage_cycle": leakage_cycle,
        "anchor_contributions": anchor_contributions,
    }


def check_bianchi_euler_pairs(selected_direct_entry):
    # Four common-complement sites.  z has a nonzero divided square, while
    # t*v*z is also nonzero, so neither Euler cancellation is vacuous.
    z = poly_add(monomial(0, 1), monomial(2, 3))
    t = monomial(0)
    v = monomial(1)
    x = {}
    y = {}
    one = monomial()

    a_entry = selected_direct_entry
    b_entry = ZERO
    c_entry = ZERO
    e_entry = ZERO
    f_entry = ZERO
    u_entry = Q(-4)
    kappa = a_entry * u_entry - b_entry * f_entry
    require(kappa == ONE, "the selected curvature is not normalized to one")

    p_pq = poly_add(
        poly_scale(Q(3), poly_multiply(x, y)), poly_scale(a_entry, z)
    )
    p_pr = poly_add(
        poly_scale(Q(3), poly_multiply(x, t)), poly_scale(b_entry, z)
    )
    transition = poly_add(
        poly_scale(a_entry, t), poly_scale(-b_entry, y)
    )
    require(
        poly_add(
            poly_multiply(p_pq, t),
            poly_scale(-ONE, poly_multiply(p_pr, y)),
        )
        == poly_multiply(transition, z),
        "the power-free pq-to-pr connection failed",
    )

    l_pq_r = poly_add(
        poly_scale(Q(3), poly_add(poly_scale(b_entry, y), poly_scale(c_entry, x))),
        poly_scale(a_entry, t),
    )
    l_pr_q = poly_add(
        poly_scale(Q(3), poly_add(poly_scale(a_entry, t), poly_scale(c_entry, x))),
        poly_scale(b_entry, y),
    )
    require(
        poly_add(l_pq_r, poly_scale(-ONE, l_pr_q))
        == poly_scale(Q(-2), transition),
        "the h=3 normal companion has the wrong coefficient",
    )

    l_pq_s = poly_add(
        poly_scale(Q(3), poly_add(poly_scale(e_entry, y), poly_scale(f_entry, x))),
        poly_scale(a_entry, v),
    )
    l_pr_s = poly_add(
        poly_scale(Q(3), poly_add(poly_scale(e_entry, t), poly_scale(u_entry, x))),
        poly_scale(b_entry, v),
    )
    curvature_left = poly_add(
        poly_scale(u_entry, p_pq),
        poly_multiply(t, l_pq_s),
        poly_scale(-f_entry, p_pr),
        poly_scale(-ONE, poly_multiply(y, l_pr_s)),
    )
    curvature_right = poly_add(
        poly_multiply(transition, v), poly_scale(kappa, z)
    )
    require(curvature_left == curvature_right, "the curvature row failed")

    m_pq = Q(3) * (b_entry * f_entry + e_entry * c_entry) + a_entry * u_entry
    m_pr = Q(3) * (a_entry * u_entry + e_entry * c_entry) + b_entry * f_entry
    require(m_pq - m_pr == Q(-2) * kappa, "the direct-double sign is wrong")

    z0 = poly_scale(Q(1, 2), poly_multiply(z, z))
    z1 = z
    z2 = one
    high_curvature = poly_scale(kappa, poly_multiply(z, z1))
    high_direct = poly_scale(Q(-2) * kappa, z0)
    transition_v = poly_multiply(transition, v)
    low_connection = poly_multiply(transition_v, poly_multiply(z, z2))
    low_normal = poly_scale(-ONE, poly_multiply(transition_v, z1))
    require(
        poly_add(high_curvature, high_direct) == {},
        "the curvature/direct-double Euler pair did not cancel",
    )
    require(
        poly_add(low_connection, low_normal) == {},
        "the connection/normal Euler pair did not cancel",
    )

    top_sites = (0, 1, 2, 3)
    top_values = [
        poly_coefficient(high_curvature, *top_sites),
        poly_coefficient(high_direct, *top_sites),
        poly_coefficient(low_connection, *top_sites),
        poly_coefficient(low_normal, *top_sites),
    ]
    require(
        top_values == [Q(2), Q(-2), Q(-1, 4), Q(1, 4)],
        "the two nonvacuous Euler pairs changed",
    )
    return {
        "tag": "bianchi_euler_pairs",
        "kappa": kappa,
        "top_values": top_values,
    }


def check_transgression_rank(frame_result, bianchi_result):
    # Use coordinates
    #   (Theta, Xi, kappa, curvature, direct, connection, normal),
    # where Theta=F0*Psi and Xi is the cycle projection of the physical
    # crossed row.  Anchor reconstruction gives Theta=Xi, and the crossed
    # target-zero row gives Xi=0.  At h=3 and chi=1, curvature=2*kappa
    # and direct=-2*kappa.  The low pair is another Euler boundary.
    relations = [
        [ONE, -ONE, ZERO, ZERO, ZERO, ZERO, ZERO],
        [ZERO, ONE, ZERO, ZERO, ZERO, ZERO, ZERO],
        [ZERO, ZERO, Q(-2), ONE, ZERO, ZERO, ZERO],
        [ZERO, ZERO, Q(2), ZERO, ONE, ZERO, ZERO],
        [ZERO, ZERO, ZERO, ZERO, ZERO, ONE, ONE],
    ]
    high_boundary = [ZERO, ZERO, ZERO, ONE, ONE, ZERO, ZERO]
    total_boundary = [ZERO, ZERO, ZERO, ONE, ONE, ONE, ONE]
    require(
        matrix_rank(relations + [high_boundary, total_boundary])
        == matrix_rank(relations),
        "an evaluated Euler boundary unexpectedly adds a source-grade row",
    )

    desired = [ONE, ZERO, -ONE, ZERO, ZERO, ZERO, ZERO]
    base_rank = matrix_rank(relations)
    extended_rank = matrix_rank(relations + [desired])
    require(base_rank == 5 and extended_rank == 6, "wrong transgression rank jump")

    witness = [
        frame_result["f0"] * frame_result["psi"],
        frame_result["leakage_cycle"],
        bianchi_result["kappa"],
        *bianchi_result["top_values"],
    ]
    require(
        all(dot(row, witness) == ZERO for row in relations),
        "the rational witness violates a retained source-grade row",
    )
    require(
        dot(desired, witness) == Q(-1),
        "the witness does not separate the proposed transgression",
    )
    require(
        frame_result["f0"] * frame_result["psi"] == ZERO
        and bianchi_result["kappa"] == ONE,
        "the displayed counteridentity changed",
    )

    # Granting the second adjacent curvature and its complete high Euler
    # pair still leaves the common (sum-channel) curvature free.  In the
    # coordinates (Theta,kH,kG,dH,cH,dG,cG), the crossed/Bianchi row only
    # sees kH-kG.
    two_curvature_relations = [
        [ZERO, ONE, -ONE, ZERO, ZERO, ZERO, ZERO],
        [ZERO, Q(2), ZERO, ONE, ZERO, ZERO, ZERO],
        [ZERO, Q(-2), ZERO, ZERO, ONE, ZERO, ZERO],
        [ZERO, ZERO, Q(2), ZERO, ZERO, ONE, ZERO],
        [ZERO, ZERO, Q(-2), ZERO, ZERO, ZERO, ONE],
    ]
    two_curvature_desired = [ONE, -ONE, ZERO, ZERO, ZERO, ZERO, ZERO]
    require(
        matrix_rank(two_curvature_relations) == 5
        and matrix_rank(two_curvature_relations + [two_curvature_desired]) == 6,
        "the two-curvature sum-channel obstruction changed",
    )
    two_curvature_witness = [ZERO, ONE, ONE, Q(-2), Q(2), Q(-2), Q(2)]
    require(
        all(dot(row, two_curvature_witness) == ZERO for row in two_curvature_relations)
        and dot(two_curvature_desired, two_curvature_witness) == -ONE,
        "the common-curvature witness no longer separates the sum channel",
    )
    return "transgression_rank"


def check_pure_reinsertion_route(frame_result):
    contributions = frame_result["anchor_contributions"]

    # Retaining the three labelled target summands would be the identity
    # map.  The actual cycle-projected crossed row is only their sum.  The
    # rotating-frame packet lies nontrivially in the resulting kernel.
    pure_reinsertion = identity(3)
    cycle_projection = [[ONE, ONE, ONE]]
    contribution_column = [[entry] for entry in contributions]
    require(matrix_rank(pure_reinsertion) == 3, "pure reinsertion lost rank")
    require(matrix_rank(cycle_projection) == 1, "cycle projection has wrong rank")
    require(
        matrix_multiply(cycle_projection, contribution_column) == [[ZERO]]
        and matrix_multiply(pure_reinsertion, contribution_column)
        != [[ZERO], [ZERO], [ZERO]],
        "the anchor kernel witness changed",
    )

    # Three target labels do not force three different pure-factor sites.
    # This is the incidence pattern of the exact two-site collision guard:
    # L supplies colours 0,1 at sites 0,1 and S supplies colours 0,2 at
    # the same sites.
    anchor_incidence = {
        ("L", 0): 0,
        ("L", 1): 1,
        ("S", 0): 0,
        ("S", 2): 1,
    }
    require(
        {colour for _, colour in anchor_incidence} == {0, 1, 2}
        and set(anchor_incidence.values()) == {0, 1},
        "the three-label/two-site collision pattern changed",
    )

    # A formal nine-row selector-family witness: all three diagonal target
    # directions and one crossed direction are killed by z, while the
    # missing vertical/sum direction is detected.  This is a source-grade
    # rank witness, not a complete matching source.
    direct = [
        [ONE, ONE, ZERO],
        [ONE, Q(2), ZERO],
        [ZERO, ZERO, ONE],
    ]
    crossed = [
        [ZERO, ONE, ZERO],
        [ONE, ZERO, ZERO],
        [ZERO, ZERO, ZERO],
    ]
    vertical = [
        [ZERO, ONE, ZERO],
        [-ONE, ZERO, ZERO],
        [ZERO, ZERO, ZERO],
    ]
    separator = [
        [ZERO, ONE, ZERO],
        [-ONE, ZERO, ZERO],
        [ZERO, ZERO, ZERO],
    ]
    require(matrix_inner(separator, direct) == ZERO, "separator sees the direct row")
    require(matrix_inner(separator, crossed) == ZERO, "separator sees the crossed row")
    for colour in range(3):
        diagonal = zeros(3, 3)
        diagonal[colour][colour] = ONE
        require(
            matrix_inner(separator, diagonal) == ZERO,
            "separator sees a diagonal target anchor",
        )
    require(
        matrix_inner(separator, vertical) == Q(2),
        "the vertical character is no longer separated",
    )
    return "pure_reinsertion_route"


def check_sum_channel_and_opposite_shore():
    # Embed the exact two-label D/C guard into three physical labels.  The
    # third diagonal direction is present, and H,G remain literal outer
    # products of shared block columns (the static Segre factorization).
    d = [
        [ONE, ONE, ZERO],
        [ONE, Q(2), ZERO],
        [ZERO, ZERO, ONE],
    ]
    c = [
        [ZERO, ONE, ZERO],
        [ONE, Q(2), ZERO],
        [ZERO, ZERO, ONE],
    ]
    d0 = matrix_column(d, 0)
    c0 = matrix_column(c, 0)
    h_assignment = outer_product(d0, c0)
    g_assignment = outer_product(d0, c0)
    assignment_sum = matrix_add(h_assignment, g_assignment)
    crossed_difference = matrix_subtract(h_assignment, g_assignment)

    def omega(matrix, direct_matrix):
        return (
            direct_matrix[1][0] * matrix[0][1]
            - direct_matrix[0][1] * matrix[1][0]
        )

    require(omega(d, d) == ZERO, "omega does not kill the direct matrix")
    require(
        omega(crossed_difference, d) == ZERO
        and omega(assignment_sum, d) == Q(2),
        "the D/C sum-channel class changed",
    )
    for colour in range(3):
        diagonal = zeros(3, 3)
        diagonal[colour][colour] = ONE
        require(omega(diagonal, d) == ZERO, "omega sees the third-label anchor")

    u = c[0][0]
    m0 = matrix_add(matrix_scale(Q(3), assignment_sum), matrix_scale(u, d))
    mh = matrix_add(
        matrix_add(h_assignment, matrix_scale(Q(3), g_assignment)),
        matrix_scale(Q(3) * u, d),
    )
    mg = matrix_add(
        matrix_add(matrix_scale(Q(3), h_assignment), g_assignment),
        matrix_scale(Q(3) * u, d),
    )
    require(
        (omega(m0, d), omega(mh, d), omega(mg, d)) == (Q(6), Q(4), Q(4)),
        "the direct-double sum-channel ledger changed",
    )

    # On the opposite-shore sr chart the two assignment tables add to the
    # new direct matrix modulo the third diagonal anchor.  Thus that chart
    # sees another difference channel, not the missing pq sum class.
    opposite_h = outer_product(c0, d0)
    opposite_g = outer_product(d0, c0)
    opposite_sum = matrix_add(opposite_h, opposite_g)
    third_diagonal = zeros(3, 3)
    third_diagonal[2][2] = ONE
    require(
        opposite_sum == matrix_subtract(c, third_diagonal)
        and omega(opposite_sum, c) == ZERO,
        "the opposite-shore selector quotient unexpectedly sees the sum",
    )

    # Formal raw coefficient audit.  Commutativity identifies UA=AU and
    # FB=BF, so pq->pr and sr->sq have exactly the same high-grade split.
    m_pq = {"AU": ONE, "BF": Q(3), "EC": Q(3)}
    m_pr = {"AU": Q(3), "BF": ONE, "EC": Q(3)}
    m_sr = {"AU": ONE, "BF": Q(3), "EC": Q(3)}
    m_sq = {"AU": Q(3), "BF": ONE, "EC": Q(3)}
    require(m_pq == m_sr and m_pr == m_sq, "opposite raw four-cuts differ")
    raw_difference = {
        key: m_pq[key] - m_pr[key] for key in ("AU", "BF", "EC")
    }
    require(
        raw_difference == {"AU": Q(-2), "BF": Q(2), "EC": ZERO},
        "the opposite-shore direct-double sign changed",
    )

    # The two filtered representatives have the same high pair and two
    # different low Euler pairs.  Any combination killing the direct term
    # therefore kills the curvature term as well.
    pq_representative = [Q(2), Q(-2), Q(-1, 4), Q(1, 4), ZERO, ZERO]
    opposite_representative = [Q(2), Q(-2), ZERO, ZERO, Q(3, 5), Q(-3, 5)]
    high_component_map = [
        [pq_representative[0], opposite_representative[0]],
        [pq_representative[1], opposite_representative[1]],
    ]
    require(
        matrix_rank(high_component_map) == 1
        and dot([ONE, -ONE], high_component_map[0]) == ZERO
        and dot([ONE, -ONE], high_component_map[1]) == ZERO,
        "opposite-shore subtraction no longer kills both high components",
    )

    # At the h=3 root, the top off-diagonal row removes only the first two
    # divided-power layers.  The lowest nonlinear response-degree candidate
    # exposed by this ledger is alpha*R^[2]q+R^[3].
    alpha = ONE
    full_root_expansion = [alpha**3, alpha**2, alpha, ONE]
    top_row_multiple = [alpha**3, alpha**2, ZERO, ZERO]
    nonlinear_residual = [
        full_root_expansion[index] - top_row_multiple[index]
        for index in range(4)
    ]
    require(
        nonlinear_residual == [ZERO, ZERO, ONE, ONE],
        "the h=3 exceptional root candidate changed",
    )
    return "sum_channel_opposite_shore"


def check_selected_cross_detector():
    # Exact scalar reduction of the six-site selected-star support fibre in
    # the audited scalar-unit carrier guard.  Retained anchors/goodness make
    # P,T,S nonzero; the restored cc row supplies D,u nonzero.  The selected
    # mixed word and common carrier have the same factor Aw+Bx.  Marked
    # curvature z-AS is independent.
    values = {
        "x": Q(2),
        "y": ONE,
        "z": -ONE,
        "w": ONE,
        "u": ONE,
        "v": ONE,
        "P": ONE,
        "T": ONE,
        "C": ONE,
        "D": ONE,
        "A": ONE,
        "B": ZERO,
        "S": -ONE,
    }
    require(
        all(values[name] != ZERO for name in ("P", "T", "S")),
        "the retained anchor/goodness factors must be nonzero",
    )
    require(
        values["D"] != ZERO and values["u"] != ZERO,
        "the restored cc factors must be nonzero",
    )

    def fibre_invariants(parameters):
        bb = parameters["P"] * parameters["T"] * (
            parameters["x"] * parameters["y"]
            + parameters["z"] * parameters["w"]
        )
        cc = (
            parameters["C"]
            * parameters["D"]
            * parameters["u"]
            * parameters["v"]
        )
        common_factor = (
            parameters["A"] * parameters["w"]
            + parameters["B"] * parameters["x"]
        )
        selected_cross = parameters["D"] * parameters["u"] * common_factor
        carrier = (
            parameters["P"]
            * parameters["T"]
            * parameters["S"]
            * common_factor
        )
        marked_curvature = parameters["z"] - parameters["A"] * parameters["S"]
        conservation_left = (
            parameters["P"]
            * parameters["T"]
            * parameters["S"]
            * selected_cross
        )
        conservation_right = parameters["D"] * parameters["u"] * carrier
        require(
            conservation_left == conservation_right,
            "selected-cross/carrier conservation changed",
        )
        return bb, cc, selected_cross, carrier, marked_curvature

    original = fibre_invariants(values)
    require(
        original == (ONE, ONE, ONE, -ONE, ZERO),
        "the exact-cancellation selected-cross guard changed",
    )

    repaired_values = dict(values)
    repaired_values["B"] = Q(-1, 2)
    repaired = fibre_invariants(repaired_values)
    require(
        repaired == (ONE, ONE, ZERO, ZERO, ZERO),
        "the selected-cross repair no longer kills only the carrier",
    )
    return "selected_cross_detector"


def check_selected_word_cohafnian_guard():
    # A single mixed word can satisfy the complete nine-entry cohafnian
    # identity with rank-three endpoint stars while its response cubic is
    # nonzero.  Thus one word alone does not kill the second/third response
    # layers.  Selected-cross carrier detection is checked separately and
    # only in its audited selected-star support fibre.
    vertices = tuple(range(6))
    q_edges = {
        edge(i, j): ONE
        for i in vertices
        for j in vertices
        if i < j
    }
    q_hafnian = hafnian(q_edges, vertices)
    q_cohafnian = cofactor_matrix(q_edges, vertices)
    require(q_hafnian == Q(15), "the all-one six-site hafnian changed")
    require(
        all(
            q_cohafnian[i][j] == (ZERO if i == j else Q(3))
            for i in vertices
            for j in vertices
        ),
        "the all-one cohafnian matrix changed",
    )

    p = [
        [ONE, ZERO, ZERO],
        [ZERO, ZERO, ZERO],
        [ZERO, ONE, ZERO],
        [ZERO, ZERO, ZERO],
        [ZERO, ZERO, ONE],
        [ZERO, ZERO, ZERO],
    ]
    s = [
        [ZERO, ZERO, ZERO],
        [ONE, ZERO, ZERO],
        [ZERO, ZERO, ZERO],
        [ZERO, ONE, ZERO],
        [ZERO, ZERO, ZERO],
        [ZERO, ZERO, Q(-2)],
    ]
    mixed_cohafnian = matrix_multiply(
        matrix_multiply(transpose(p), q_cohafnian), s
    )
    expected = [
        [Q(3), Q(3), Q(-6)],
        [Q(3), Q(3), Q(-6)],
        [Q(3), Q(3), Q(-6)],
    ]
    require(mixed_cohafnian == expected, "the selected-word cohafnian changed")
    direct = matrix_scale(Q(-1, 15), mixed_cohafnian)
    require(
        matrix_add(mixed_cohafnian, matrix_scale(q_hafnian, direct))
        == zeros(3, 3),
        "the complete mixed-word nine-entry identity failed",
    )
    require(
        direct[0][1] == Q(-1, 5)
        and sum((direct[i][i] for i in range(3)), ZERO) == ZERO,
        "the selected scalar-zero direct block changed",
    )

    def response_for(contracting_matrix):
        forward = matrix_multiply(
            matrix_multiply(p, contracting_matrix), transpose(s)
        )
        return matrix_add(forward, transpose(forward))

    scalar_zero_matrix = matrix_scale(Q(1, 5), identity(3))
    response_matrix = response_for(scalar_zero_matrix)
    response_edges = {
        edge(i, j): response_matrix[i][j]
        for i in vertices
        for j in vertices
        if i < j and response_matrix[i][j]
    }
    require(
        response_edges
        == {edge(0, 1): Q(1, 5), edge(2, 3): Q(1, 5), edge(4, 5): Q(-2, 5)},
        "the selected-word response matching changed",
    )
    response_hafnian = hafnian(response_edges, vertices)
    response_derivative = sum(
        (
            response_matrix[i][j] * q_cohafnian[i][j]
            for i in vertices
            for j in vertices
            if i < j
        ),
        ZERO,
    )
    require(
        response_derivative == ZERO and response_hafnian == Q(-2, 125),
        "the selected word no longer separates tangent from response cubic",
    )

    # The sharper guard has nonzero direct scalar.  Contract the same fixed
    # block with K=diag(1,1,1/2).  Its response matching has weights
    # (1,1,-1), while sigma=-1/5.  The admitted top row cancels exactly, but
    # the next two response layers leave residual -4/5.
    nonzero_scalar_matrix = [
        [ONE, ZERO, ZERO],
        [ZERO, ONE, ZERO],
        [ZERO, ZERO, Q(1, 2)],
    ]
    direct_scalar = matrix_inner(direct, nonzero_scalar_matrix)
    nonzero_response = response_for(nonzero_scalar_matrix)
    nonzero_response_edges = {
        edge(i, j): nonzero_response[i][j]
        for i in vertices
        for j in vertices
        if i < j and nonzero_response[i][j]
    }
    require(
        direct_scalar == Q(-1, 5)
        and nonzero_response_edges
        == {edge(0, 1): ONE, edge(2, 3): ONE, edge(4, 5): -ONE},
        "the nonzero-scalar response matching changed",
    )
    nonzero_derivative = sum(
        (
            nonzero_response[i][j] * q_cohafnian[i][j]
            for i in vertices
            for j in vertices
            if i < j
        ),
        ZERO,
    )
    top_row = q_hafnian * direct_scalar + nonzero_derivative
    response_squared_times_q = sum(
        (
            q_edges[edge(i, j)]
            * hafnian(
                nonzero_response_edges,
                tuple(vertex for vertex in vertices if vertex not in (i, j)),
            )
            for i in vertices
            for j in vertices
            if i < j
        ),
        ZERO,
    )
    response_cubic = hafnian(nonzero_response_edges, vertices)
    nonlinear_residual = (
        direct_scalar * response_squared_times_q + response_cubic
    )
    require(
        nonzero_derivative == Q(3)
        and top_row == ZERO
        and response_squared_times_q == -ONE
        and response_cubic == -ONE
        and nonlinear_residual == Q(-4, 5),
        "the nonzero-direct-scalar selected-word guard changed",
    )
    return "selected_word_cohafnian_guard"


def check_hankel_candidate():
    # On the off-diagonal canonical line K=u E_01+v I, all three target
    # forms are v.  Granting diagonal local maps at three distinct selector
    # sites therefore gives kappa_0*kappa_1*kappa_2=v^3.
    target_forms = [(ZERO, ONE), (ZERO, ONE), (ZERO, ONE)]
    target_cubic = [ONE]
    for linear_form in target_forms:
        updated = [ZERO] * (len(target_cubic) + 1)
        for degree, coefficient in enumerate(target_cubic):
            updated[degree] += coefficient * linear_form[0]
            updated[degree + 1] += coefficient * linear_form[1]
        target_cubic = updated
    require(target_cubic == [ZERO, ZERO, ZERO, ONE], "the target cubic is not v^3")

    # Formula (19) of the odd-covariant ledger, specialized to the cubic
    # k=(0,0,0,1), maps Psi=(q0,q1,q2) to
    # Theta=(0,0,0,q0,4q1,10q2).
    cartan = [
        [ZERO, ZERO, ZERO],
        [ZERO, ZERO, ZERO],
        [ZERO, ZERO, ZERO],
        [ONE, ZERO, ZERO],
        [ZERO, Q(4), ZERO],
        [ZERO, ZERO, Q(10)],
    ]
    require(matrix_rank(cartan) == 3, "the target-cubic Cartan map lost rank")

    # Clean coordinates u^3 and v^3 have all six shifts as coordinate
    # functionals on a quintic.  Thus their Hankel map is the identity.
    hankel = identity(6)
    residual = matrix_multiply(hankel, cartan)
    require(residual == cartan, "the six clean Hankel shifts changed")
    require(
        residual[3:] == [
            [ONE, ZERO, ZERO],
            [ZERO, Q(4), ZERO],
            [ZERO, ZERO, Q(10)],
        ],
        "the three v^3 shifts do not give diag(1,4,10)",
    )

    hypothetical_psi = [[Q(1, 4)], [ZERO], [ZERO]]
    theta = matrix_multiply(cartan, hypothetical_psi)
    hankel_residual = matrix_multiply(hankel, theta)
    require(
        theta == [[ZERO], [ZERO], [ZERO], [Q(1, 4)], [ZERO], [ZERO]],
        "the normalized hypothetical cycle has the wrong Cartan product",
    )
    require(
        hankel_residual[3] == [Q(1, 4)]
        and any(entry[0] for entry in hankel_residual),
        "the canonical Hankel candidate accidentally annihilates the clean line",
    )
    return "hankel_candidate"


def main():
    audit_tags = {check_compatible_words()}
    frame_result = check_frame_anchor_cycle()
    audit_tags.add(frame_result["tag"])
    bianchi_result = check_bianchi_euler_pairs(frame_result["direct"][0][1])
    audit_tags.add(bianchi_result["tag"])
    audit_tags.add(check_transgression_rank(frame_result, bianchi_result))
    audit_tags.add(check_pure_reinsertion_route(frame_result))
    audit_tags.add(check_sum_channel_and_opposite_shore())
    audit_tags.add(check_selected_cross_detector())
    audit_tags.add(check_selected_word_cohafnian_guard())
    audit_tags.add(check_hankel_candidate())
    expected_tags = {
        "compatible_words",
        "frame_anchor_cycle",
        "bianchi_euler_pairs",
        "transgression_rank",
        "pure_reinsertion_route",
        "sum_channel_opposite_shore",
        "selected_cross_detector",
        "selected_word_cohafnian_guard",
        "hankel_candidate",
    }
    require(audit_tags == expected_tags, "the audit coverage manifest is incomplete")
    print("adjacent h=3 source-grade cycle transgression: RANK OBSTRUCTION")
    print("  scope: direct-sum packet, not one complete physical full-nine source")
    print("  F0*Psi_C = 0, chi*(AU-BF) = 1")
    print("  anchor contributions: -9/64, -3/32, 15/64")
    print("  Euler top pairs: (2,-2), (-1/4,1/4)")
    print("  proposed transgression raises source-grade row rank 5 -> 6")
    print("  opposite-shore splitting is identical in the high Euler pair")
    print("  third anchor + static Segre still leave the sum channel free")
    print("  selected-cross detects the carrier only in the audited support fibre")
    print("  nonzero-s word: 15s+D_haf=0 but nonlinear residual=-4/5")
    print("  v^3 Hankel residual on Psi=(q0,q1,q2): (q0,4q1,10q2)")


if __name__ == "__main__":
    main()
