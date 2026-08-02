#!/usr/bin/env python3
"""Exact h=3 five-exposed two-chart selected-cap landing counterguard.

This checker deliberately tests a *selected scalar coefficient packet*, not
the full tensor-valued nine-row equations over every residual word.  On one
compatible residual word it verifies all nine ``pq`` cap coefficients and
all nine ``pr`` cap coefficients, the shared physical-block realization,
one complete crossed four-index zero slice, the diagonal target-frame
bookkeeping, and the connection/normal/curvature/direct-double identities.

The main specialization has the entire ``pr`` direct block equal to zero,
four injective endpoint-star triples, and nonzero curvature.  Its exact
anchor-cycle value is Theta=0, while chi*kappa is nonzero, so the proposed
grade-split landing row is not in the retained selected-coefficient row
span.  A second tilted specialization has nonzero selected entries in all
four curvature factors.  Neither packet is a full ternary source.
"""

from fractions import Fraction as F
from itertools import combinations, product


ZERO = F(0)
ONE = F(1)
COLOURS = (0, 1, 2)
INTERNAL = tuple(range(6))
P_SITE = 6
Q_SITE = 7
GLOBAL_SITES = tuple(range(8))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remainder):
            yield ((first, second),) + tail


def hafnian(edge_values, vertices):
    total = ZERO
    for matching in perfect_matchings(tuple(vertices)):
        term = ONE
        for left, right in matching:
            term *= edge_values.get(edge(left, right), ZERO)
            if not term:
                break
        total += term
    return total


def zeros(rows, columns):
    return [[ZERO for _ in range(columns)] for _ in range(rows)]


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


def matrix_rank(matrix):
    if not matrix:
        return 0
    work = [list(row) for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        value = work[rank][column]
        work[rank] = [entry / value for entry in work[rank]]
        for row in range(row_count):
            if row == rank:
                continue
            value = work[row][column]
            if value:
                work[row] = [
                    entry - value * pivot_entry
                    for entry, pivot_entry in zip(work[row], work[rank])
                ]
        rank += 1
        if rank == row_count:
            break
    return rank


def vector_rank(vectors):
    return matrix_rank([list(vector) for vector in vectors])


def dot(left, right):
    return sum((left[i] * right[i] for i in range(len(left))), ZERO)


def matrix_inner(left, right):
    return sum(
        (
            left[i][j] * right[i][j]
            for i in range(len(left))
            for j in range(len(left[0]))
        ),
        ZERO,
    )


def outer(left, right):
    return [[left[i] * right[j] for j in range(len(right))] for i in range(len(left))]


def cofactor_matrix(edge_values, vertices):
    vertices = tuple(vertices)
    result = zeros(len(vertices), len(vertices))
    for i, left in enumerate(vertices):
        for j, right in enumerate(vertices):
            if i == j:
                continue
            complement = tuple(v for v in vertices if v not in (left, right))
            result[i][j] = hafnian(edge_values, complement)
    return result


def pair_response(left_star, right_star, internal_edges, vertices):
    vertices = tuple(vertices)
    total = ZERO
    for left in vertices:
        for right in vertices:
            if left == right:
                continue
            complement = tuple(v for v in vertices if v not in (left, right))
            total += (
                left_star.get(left, ZERO)
                * right_star.get(right, ZERO)
                * hafnian(internal_edges, complement)
            )
    return total


def direct_from_stars(left_stars, right_stars, internal_edges, vertices):
    base = hafnian(internal_edges, vertices)
    require(base != ZERO, "cannot solve a cap table with zero internal hafnian")
    return [
        [
            -pair_response(left_stars[i], right_stars[j], internal_edges, vertices)
            / base
            for j in COLOURS
        ]
        for i in COLOURS
    ]


# Site-square-zero polynomials on a fixed four-site complement.  A mask is
# the set of occupied sites; repeated-site products vanish.
def poly_add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for mask, coefficient in polynomial.items():
            result[mask] = result.get(mask, ZERO) + coefficient
            if result[mask] == ZERO:
                del result[mask]
    return result


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
            if result[mask] == ZERO:
                del result[mask]
    return result


def linear_polynomial(values, sites):
    return {
        1 << site: values.get(site, ZERO)
        for site in sites
        if values.get(site, ZERO)
    }


def quadratic_polynomial(edge_values, sites):
    site_set = set(sites)
    return {
        (1 << left) | (1 << right): value
        for (left, right), value in edge_values.items()
        if left in site_set and right in site_set and value
    }


def top_coefficient(polynomial, sites):
    mask = sum(1 << site for site in sites)
    return polynomial.get(mask, ZERO)


Q_EDGES = {
    edge(*pair): ONE
    for pair in (
        (0, 1), (0, 2), (0, 4), (0, 5), (1, 2),
        (1, 4), (2, 3), (3, 4), (3, 5),
    )
}
RESIDUAL_LABELS = (0, 1, 2, 0, 1, 2)


def base_left_stars():
    return (
        {0: ONE},
        {1: ONE},
        {2: ONE},
    )


def base_right_stars():
    return (
        {3: ONE},
        {4: ONE},
        {5: ONE},
    )


def sparse_linear(*pairs):
    return {site: F(value) for site, value in pairs if value}


def make_cell_key(left, right, left_colour, right_colour):
    if left < right:
        return (left, right, left_colour, right_colour)
    return (right, left, right_colour, left_colour)


def put_cell(cells, left, right, left_colour, right_colour, value):
    value = F(value)
    key = make_cell_key(left, right, left_colour, right_colour)
    if key in cells:
        require(cells[key] == value, f"inconsistent shared cell {key}")
    elif value:
        cells[key] = value


def get_cell(cells, left, right, left_colour, right_colour):
    return cells.get(
        make_cell_key(left, right, left_colour, right_colour), ZERO
    )


def restricted_edges(cells, vertices, assignment):
    return {
        edge(left, right): get_cell(
            cells, left, right, assignment[left], assignment[right]
        )
        for left, right in combinations(vertices, 2)
        if get_cell(cells, left, right, assignment[left], assignment[right])
    }


def matching_coefficient(cells, assignment):
    edges = restricted_edges(cells, tuple(sorted(assignment)), assignment)
    return hafnian(edges, tuple(sorted(assignment)))


def chart_decomposition(cells, deleted, deleted_colours, residual_assignment):
    left, right = deleted
    left_colour, right_colour = deleted_colours
    residual = tuple(sorted(residual_assignment))
    internal_edges = restricted_edges(cells, residual, residual_assignment)
    left_star = {
        site: get_cell(cells, left, site, left_colour, residual_assignment[site])
        for site in residual
    }
    right_star = {
        site: get_cell(cells, right, site, right_colour, residual_assignment[site])
        for site in residual
    }
    direct = get_cell(cells, left, right, left_colour, right_colour)
    internal_hafnian = hafnian(internal_edges, residual)
    response = pair_response(left_star, right_star, internal_edges, residual)
    assignment = dict(residual_assignment)
    assignment[left] = left_colour
    assignment[right] = right_colour
    global_value = matching_coefficient(cells, assignment)
    require(
        global_value == direct * internal_hafnian + response,
        f"chart decomposition failed for {deleted}, {deleted_colours}",
    )
    return global_value, internal_hafnian, response


def build_packet(kind):
    require(kind in ("direct_free", "tilted"), "unknown packet kind")
    left_stars = base_left_stars()
    right_stars = base_right_stars()
    if kind == "tilted":
        left_stars = (
            {0: ONE, 1: ONE},
            {1: ONE},
            {2: ONE},
        )
        right_stars = (
            {3: ONE},
            {2: ONE, 4: ONE},
            {5: ONE},
        )

    direct_pq = direct_from_stars(
        left_stars, right_stars, Q_EDGES, INTERNAL
    )
    require(hafnian(Q_EDGES, INTERNAL) == F(4), "the pq hafnian changed")

    if kind == "direct_free":
        r_site = 3
        s_site = 2
        q_colour = r_colour = 0
        p_colour = 2
        s_colour = 2
        x_site = 0
        # The pr internal quadratic has an isolated q-site.  The fixed
        # r-colour row is the literal q row at site 3.  Two further rows
        # lie in the exact cofactor kernel and keep the r-star injective.
        right_pr_stars = (
            {Q_SITE: ONE, 2: ONE, 4: ONE, 5: ONE},
            {0: ONE},
            {1: ONE},
        )
        direct_pr = zeros(3, 3)
    else:
        r_site = 1
        s_site = 2
        q_colour = r_colour = 1
        p_colour = 0
        s_colour = 2
        x_site = 0
        right_pr_stars = (
            {3: ONE},
            {0: ONE, 2: ONE, 4: ONE},
            {5: ONE},
        )
        # Filled below from the literal pr internal quadratic.
        direct_pr = None

    common = tuple(site for site in INTERNAL if site != r_site)
    pr_vertices = (Q_SITE,) + common
    pr_assignment = {Q_SITE: q_colour}
    pr_assignment.update({site: RESIDUAL_LABELS[site] for site in common})

    pr_internal = {
        edge(left, right): value
        for (left, right), value in Q_EDGES.items()
        if left != r_site and right != r_site
    }
    for site, value in right_stars[q_colour].items():
        if site != r_site and value:
            pr_internal[edge(Q_SITE, site)] = value

    left_pr_stars = []
    for colour in COLOURS:
        values = {
            Q_SITE: direct_pq[colour][q_colour],
            **{
                site: left_stars[colour].get(site, ZERO)
                for site in common
                if left_stars[colour].get(site, ZERO)
            },
        }
        left_pr_stars.append({site: value for site, value in values.items() if value})
    left_pr_stars = tuple(left_pr_stars)

    if kind == "direct_free":
        require(hafnian(pr_internal, pr_vertices) == ZERO, "pr is not direct-free")
        for i in COLOURS:
            for k in COLOURS:
                require(
                    pair_response(
                        left_pr_stars[i], right_pr_stars[k], pr_internal, pr_vertices
                    )
                    == ZERO,
                    f"direct-free pr response {(i, k)} survived",
                )
    else:
        direct_pr = direct_from_stars(
            left_pr_stars, right_pr_stars, pr_internal, pr_vertices
        )
        require(hafnian(pr_internal, pr_vertices) != ZERO, "tilted pr hafnian vanished")

    # The pq chart sees the selected r colour as one residual port, so its
    # p-r and q-r columns must be the same physical cells as the pr chart.
    for i in COLOURS:
        require(
            direct_pr[i][r_colour] == left_stars[i].get(r_site, ZERO),
            f"shared p-r column failed for colour {i}",
        )
    for j in COLOURS:
        require(
            right_stars[j].get(r_site, ZERO)
            == right_pr_stars[r_colour].get(Q_SITE, ZERO)
            if j == q_colour
            else right_stars[j].get(r_site, ZERO) == ZERO,
            f"shared q-r selected column failed for colour {j}",
        )

    cells = {}
    for (left, right), value in Q_EDGES.items():
        put_cell(
            cells,
            left,
            right,
            RESIDUAL_LABELS[left],
            RESIDUAL_LABELS[right],
            value,
        )
    for i in COLOURS:
        for site, value in left_stars[i].items():
            put_cell(cells, P_SITE, site, i, RESIDUAL_LABELS[site], value)
    for j in COLOURS:
        for site, value in right_stars[j].items():
            put_cell(cells, Q_SITE, site, j, RESIDUAL_LABELS[site], value)
    for i in COLOURS:
        for j in COLOURS:
            put_cell(cells, P_SITE, Q_SITE, i, j, direct_pq[i][j])
    for k in COLOURS:
        for site, value in right_pr_stars[k].items():
            if site == Q_SITE:
                put_cell(cells, Q_SITE, r_site, q_colour, k, value)
            else:
                put_cell(
                    cells, r_site, site, k, RESIDUAL_LABELS[site], value
                )
    for i in COLOURS:
        for k in COLOURS:
            put_cell(cells, P_SITE, r_site, i, k, direct_pr[i][k])

    return {
        "kind": kind,
        "cells": cells,
        "left_stars": left_stars,
        "right_stars": right_stars,
        "direct_pq": direct_pq,
        "left_pr_stars": left_pr_stars,
        "right_pr_stars": right_pr_stars,
        "direct_pr": direct_pr,
        "r": r_site,
        "s": s_site,
        "x": x_site,
        "q_colour": q_colour,
        "r_colour": r_colour,
        "p_colour": p_colour,
        "s_colour": s_colour,
        "pr_vertices": pr_vertices,
        "pr_assignment": pr_assignment,
        "pr_internal": pr_internal,
    }


def check_selected_cap_rows(packet):
    cells = packet["cells"]
    pq_residual = {site: RESIDUAL_LABELS[site] for site in INTERNAL}
    pr_residual = dict(packet["pr_assignment"])
    pq_word = tuple(pq_residual[site] for site in INTERNAL)
    pr_word = tuple(pr_residual[site] for site in packet["pr_vertices"])
    require(
        sorted(pq_word) == sorted(pr_word) == [0, 0, 1, 1, 2, 2],
        "the two selected residual words are not separating 001122 words",
    )

    pq_values = []
    pr_values = []
    for i in COLOURS:
        for j in COLOURS:
            value, _, _ = chart_decomposition(
                cells, (P_SITE, Q_SITE), (i, j), pq_residual
            )
            pq_values.append(value)
            require(value == ZERO, f"selected pq cap row {(i, j)} is nonzero")
    for i in COLOURS:
        for k in COLOURS:
            value, _, _ = chart_decomposition(
                cells,
                (P_SITE, packet["r"]),
                (i, k),
                pr_residual,
            )
            pr_values.append(value)
            require(value == ZERO, f"selected pr cap row {(i, k)} is nonzero")
    require(len(pq_values) == len(pr_values) == 9, "did not audit all 18 rows")

    # On this mixed residual word every diagonal GHZ target coefficient is
    # zero.  This is the selected scalar evaluation of the diagonal targets,
    # not the full tensor-valued diagonal equation.
    target_values = []
    for word in (pq_word, pr_word):
        for colour in COLOURS:
            target_values.append(ONE if all(entry == colour for entry in word) else ZERO)
    require(target_values == [ZERO] * 6, "a selected diagonal target survived")

    # Five exposed sites are p,q,r,s,x.  The remaining D5 has three sites.
    exposed = {P_SITE, Q_SITE, packet["r"], packet["s"], packet["x"]}
    d5 = tuple(site for site in GLOBAL_SITES if site not in exposed)
    require(len(exposed) == 5 and len(d5) == 3, "wrong five-exposed split")

    # A complete crossed four-index row: fix p,q,r,s at the selected mixed
    # labels and enumerate the entire 3^4 complementary tensor.
    boundary = {
        P_SITE: packet["p_colour"],
        Q_SITE: packet["q_colour"],
        packet["r"]: packet["r_colour"],
        packet["s"]: packet["s_colour"],
    }
    complement = tuple(site for site in GLOBAL_SITES if site not in boundary)
    crossed_values = []
    for word in product(COLOURS, repeat=len(complement)):
        assignment = dict(boundary)
        assignment.update(dict(zip(complement, word)))
        crossed_values.append(matching_coefficient(cells, assignment))
    require(
        crossed_values == [ZERO] * (3 ** 4),
        "the complete crossed four-index target-zero row failed",
    )

    require(
        vector_rank(
            tuple(tuple(star.get(site, ZERO) for site in INTERNAL)
                  for star in packet["left_stars"])
        ) == 3,
        "pq left star is not injective",
    )
    require(
        vector_rank(
            tuple(tuple(star.get(site, ZERO) for site in INTERNAL)
                  for star in packet["right_stars"])
        ) == 3,
        "pq right star is not injective",
    )
    pr_order = packet["pr_vertices"]
    require(
        vector_rank(
            tuple(tuple(star.get(site, ZERO) for site in pr_order)
                  for star in packet["left_pr_stars"])
        ) == 3,
        "pr left star is not injective",
    )
    require(
        vector_rank(
            tuple(tuple(star.get(site, ZERO) for site in pr_order)
                  for star in packet["right_pr_stars"])
        ) == 3,
        "pr right star is not injective",
    )
    return {"pq_word": pq_word, "pr_word": pr_word, "d5": d5}


def selected_overlap_data(packet):
    cells = packet["cells"]
    i = packet["p_colour"]
    j = packet["q_colour"]
    k = packet["r_colour"]
    ell = packet["s_colour"]
    r_site = packet["r"]
    s_site = packet["s"]
    common = tuple(site for site in INTERNAL if site not in (r_site, s_site))

    a = get_cell(cells, P_SITE, Q_SITE, i, j)
    b = get_cell(cells, P_SITE, r_site, i, k)
    c = get_cell(cells, Q_SITE, r_site, j, k)
    e_value = get_cell(cells, P_SITE, s_site, i, ell)
    f_value = get_cell(cells, Q_SITE, s_site, j, ell)
    u = get_cell(cells, r_site, s_site, k, ell)
    kappa = a * u - b * f_value
    require(a != ZERO and u != ZERO and kappa != ZERO, "curvature minor vanished")

    z_edges = restricted_edges(
        cells,
        common,
        {site: RESIDUAL_LABELS[site] for site in common},
    )
    z = quadratic_polynomial(z_edges, common)

    def star(endpoint, colour):
        return {
            site: get_cell(
                cells, endpoint, site, colour, RESIDUAL_LABELS[site]
            )
            for site in common
            if get_cell(cells, endpoint, site, colour, RESIDUAL_LABELS[site])
        }

    x = linear_polynomial(star(P_SITE, i), common)
    y = linear_polynomial(star(Q_SITE, j), common)
    t = linear_polynomial(star(r_site, k), common)
    v = linear_polynomial(star(s_site, ell), common)

    f_pq = poly_add(poly_scale(a, z), poly_multiply(x, y))
    g_pr = poly_add(poly_scale(b, z), poly_multiply(x, t))
    transition = poly_add(poly_scale(a, t), poly_scale(-b, y))
    require(
        poly_add(
            poly_multiply(f_pq, t),
            poly_scale(-ONE, poly_multiply(g_pr, y)),
        )
        == poly_multiply(transition, z),
        "power-free connection failed",
    )

    h = F(3)
    l_pq_r = poly_add(
        poly_scale(h * b, y), poly_scale(h * c, x), poly_scale(a, t)
    )
    l_pr_q = poly_add(
        poly_scale(h * a, t), poly_scale(h * c, x), poly_scale(b, y)
    )
    require(
        poly_add(l_pq_r, poly_scale(-ONE, l_pr_q))
        == poly_scale(F(-2), transition),
        "normal companion failed",
    )

    h_pq_s = poly_add(
        poly_scale(a, v), poly_scale(e_value, y), poly_scale(f_value, x)
    )
    n_pr_s = poly_add(
        poly_scale(b, v), poly_scale(e_value, t), poly_scale(u, x)
    )
    curvature_left = poly_add(
        poly_scale(u, f_pq),
        poly_multiply(t, h_pq_s),
        poly_scale(-f_value, g_pr),
        poly_scale(-ONE, poly_multiply(y, n_pr_s)),
    )
    curvature_right = poly_add(
        poly_multiply(transition, v), poly_scale(kappa, z)
    )
    require(curvature_left == curvature_right, "curvature row failed")

    m_pq = h * (b * f_value + e_value * c) + a * u
    m_pr = h * (a * u + e_value * c) + b * f_value
    require(m_pq - m_pr == F(-2) * kappa, "direct-double row failed")

    z_squared = poly_multiply(z, z)
    z_divided_two = poly_scale(F(1, 2), z_squared)
    high_curvature = poly_scale(kappa, z_squared)
    high_direct = poly_scale(F(-2) * kappa, z_divided_two)
    low_connection = poly_multiply(poly_multiply(transition, v), z)
    low_normal = poly_scale(-ONE, low_connection)
    require(poly_add(high_curvature, high_direct) == {}, "high Euler pair failed")
    require(poly_add(low_connection, low_normal) == {}, "low Euler pair failed")

    chi = hafnian(z_edges, common)
    require(chi != ZERO, "the selected curvature cofactor chi vanished")
    top_values = tuple(
        top_coefficient(polynomial, common)
        for polynomial in (high_curvature, high_direct, low_connection, low_normal)
    )
    require(top_values[0] == F(2) * chi * kappa, "wrong curvature top value")
    require(top_values[1] == F(-2) * chi * kappa, "wrong direct top value")
    require(top_values[2] == -top_values[3], "low Euler top values do not cancel")
    return {
        "A": a,
        "B": b,
        "C": c,
        "E": e_value,
        "F": f_value,
        "U": u,
        "kappa": kappa,
        "chi": chi,
        "top_values": top_values,
    }


def three_cycle(direct, matrix):
    return (
        direct[1][2] * direct[2][0] * matrix[0][1]
        + direct[2][0] * direct[0][1] * matrix[1][2]
        + direct[0][1] * direct[1][2] * matrix[2][0]
    )


def phi_from_deltas(deltas, direct):
    phi = zeros(3, 3)
    for i in COLOURS:
        for j in COLOURS:
            phi[i][j] = (
                -sum(
                    (
                        deltas[colour][i][colour] * direct[colour][j]
                        for colour in COLOURS
                        if colour != i
                    ),
                    ZERO,
                )
                -sum(
                    (
                        direct[i][colour] * deltas[colour][colour][j]
                        for colour in COLOURS
                        if colour != j
                    ),
                    ZERO,
                )
                -direct[i][j] * deltas[j][j][j]
            )
    return phi


def check_diagonal_anchor_cycle(packet):
    # This is the exact diagonal target-frame module used by the preceding
    # adjacent-cycle guard.  It is attached to the base pq selector chart.
    # It does not assert the tensor-valued target equations at other words.
    require(packet["kind"] == "direct_free", "anchor cycle uses the base chart")
    cofactor = cofactor_matrix(Q_EDGES, INTERNAL)
    cross = [[cofactor[i][j] for j in (3, 4, 5)] for i in (0, 1, 2)]
    expected_cross = [
        [ZERO, ONE, F(2)],
        [ZERO, F(2), F(2)],
        [ONE, ONE, ONE],
    ]
    require(cross == expected_cross, "the cross-cofactor matrix changed")
    direct = matrix_scale(F(-1, 4), cross)
    require(direct == packet["direct_pq"], "physical pq direct block changed")

    x_connection = [
        [ONE, ONE, F(-2)],
        [ONE, ONE, F(-2)],
        [ONE, ONE, F(-2)],
    ]
    y_connection = [
        [F(5, 2), F(10), F(25, 2)],
        [ZERO, ZERO, ZERO],
        [F(-1, 2), F(-2), F(-5, 2)],
    ]
    stabilized = matrix_add(
        matrix_multiply(transpose(x_connection), cross),
        matrix_multiply(cross, y_connection),
    )
    require(stabilized == zeros(3, 3), "the selector connection moved the cofactor")
    leakage = matrix_add(
        matrix_multiply(transpose(x_connection), direct),
        matrix_multiply(direct, y_connection),
    )
    require(leakage == zeros(3, 3), "normalized direct leakage survived")

    diagonal_targets = []
    deltas = []
    for colour in COLOURS:
        target = zeros(3, 3)
        target[colour][colour] = ONE
        diagonal_targets.append(target)
        delta = matrix_scale(
            -ONE,
            matrix_add(
                matrix_multiply(transpose(x_connection), target),
                matrix_multiply(target, y_connection),
            ),
        )
        require(delta != zeros(3, 3), f"diagonal target defect {colour} vanished")
        deltas.append(delta)
    require(
        matrix_rank([sum(target, []) for target in diagonal_targets]) == 3,
        "the three diagonal target rows lost rank",
    )

    phi = phi_from_deltas(deltas, direct)
    contributions = []
    for retained in COLOURS:
        partial = [deltas[c] if c == retained else zeros(3, 3) for c in COLOURS]
        contributions.append(three_cycle(direct, phi_from_deltas(partial, direct)))
    require(
        contributions == [F(-9, 64), F(-3, 32), F(15, 64)],
        "the three diagonal anchor contributions changed",
    )
    require(all(contributions) and sum(contributions, ZERO) == ZERO,
            "the diagonal anchor cancellation became vacuous")
    psi = three_cycle(direct, phi)
    xi = three_cycle(direct, leakage)
    theta = F(4) * psi
    require(theta == xi == ZERO, "the anchor/crossed cycle should vanish")
    return {"theta": theta, "xi": xi, "contributions": tuple(contributions)}


def check_landing_row_rank(anchor, overlap):
    chi = overlap["chi"]
    relations = [
        [ONE, -ONE, ZERO, ZERO, ZERO, ZERO, ZERO],
        [ZERO, ONE, ZERO, ZERO, ZERO, ZERO, ZERO],
        [ZERO, ZERO, F(-2) * chi, ONE, ZERO, ZERO, ZERO],
        [ZERO, ZERO, F(2) * chi, ZERO, ONE, ZERO, ZERO],
        [ZERO, ZERO, ZERO, ZERO, ZERO, ONE, ONE],
    ]
    desired = [ONE, ZERO, -chi, ZERO, ZERO, ZERO, ZERO]
    require(matrix_rank(relations) == 5, "retained grade-row rank changed")
    require(matrix_rank(relations + [desired]) == 6, "landing row entered the span")

    witness = [
        anchor["theta"],
        anchor["xi"],
        overlap["kappa"],
        *overlap["top_values"],
    ]
    require(len(witness) == 7, "wrong grade witness length")
    require(all(dot(row, witness) == ZERO for row in relations),
            "the physical witness violates a retained grade row")
    residual = dot(desired, witness)
    require(residual == anchor["theta"] - chi * overlap["kappa"],
            "landing residual has the wrong normalization")
    require(residual != ZERO, "the grade-split landing row accidentally holds")
    return residual


def check_packet(kind):
    packet = build_packet(kind)
    cap = check_selected_cap_rows(packet)
    overlap = selected_overlap_data(packet)
    if kind == "direct_free":
        require(
            packet["direct_pr"] == zeros(3, 3),
            "the entire pr direct block is not zero",
        )
        anchor = check_diagonal_anchor_cycle(packet)
        residual = check_landing_row_rank(anchor, overlap)
    else:
        a, b, f_value, u = (
            overlap["A"], overlap["B"], overlap["F"], overlap["U"]
        )
        require(all(value != ZERO for value in (a, b, f_value, u)),
                "the tilted curvature square has a zero corner")
        residual = None
    return packet, cap, overlap, residual


def main():
    direct_free, _, direct_free_overlap, residual = check_packet("direct_free")
    tilted, _, tilted_overlap, _ = check_packet("tilted")
    print("h=3 five-exposed selected-cap landing counterguard: PASS")
    print("  scope                         : 18 selected scalar cap coefficients")
    print(f"  direct-free crossed labels   : {(2, 0, 0, 2)}")
    print(f"  direct-free (chi,kappa)      : {(direct_free_overlap['chi'], direct_free_overlap['kappa'])}")
    print(f"  landing residual             : {residual}")
    print(f"  entire pr direct block zero  : {direct_free['direct_pr'] == zeros(3, 3)}")
    print(f"  tilted (A,B,F,U;kappa)       : {(tilted_overlap['A'], tilted_overlap['B'], tilted_overlap['F'], tilted_overlap['U'], tilted_overlap['kappa'])}")
    print(f"  tilted pr direct rank        : {matrix_rank(tilted['direct_pr'])}")
    print("  full tensor-valued EqSystem  : NOT CLAIMED")


if __name__ == "__main__":
    main()
