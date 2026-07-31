#!/usr/bin/env python3
"""Exact audit of the separating 3+3 opposite-shore/Bianchi boundary."""

from fractions import Fraction as Q
from itertools import combinations


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def zero(rows, cols):
    return [[Q(0) for _ in range(cols)] for _ in range(rows)]


def eye(n):
    out = zero(n, n)
    for i in range(n):
        out[i][i] = Q(1)
    return out


def transpose(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [
        [a[i][j] + b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def sub(a, b):
    return [
        [a[i][j] - b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def scale(c, a):
    return [[c * value for value in row] for row in a]


def mul(a, b):
    return [
        [
            sum((a[i][k] * b[k][j] for k in range(len(b))), Q(0))
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


def equal(a, b):
    return a == b


def matrix_unit(i, j):
    out = zero(3, 3)
    out[i][j] = Q(1)
    return out


def bilinear(left, matrix, right):
    return sum(
        (
            left[i] * matrix[i][j] * right[j]
            for i in range(3)
            for j in range(3)
        ),
        Q(0),
    )


def hafnian(vertices, edge_values):
    vertices = tuple(vertices)
    if not vertices:
        return Q(1)
    first = vertices[0]
    total = Q(0)
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        edge = tuple(sorted((first, second)))
        total += edge_values.get(edge, Q(0)) * hafnian(rest, edge_values)
    return total


def hafnian_derivative(vertices, edge_values, edge_tangent):
    vertices = tuple(vertices)
    if not vertices:
        return Q(0)
    first = vertices[0]
    total = Q(0)
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        edge = tuple(sorted((first, second)))
        total += edge_tangent.get(edge, Q(0)) * hafnian(rest, edge_values)
        total += edge_values.get(edge, Q(0)) * hafnian_derivative(
            rest, edge_values, edge_tangent
        )
    return total


def cofactor_matrix(vertices, edge_values):
    out = zero(len(vertices), len(vertices))
    for i, first in enumerate(vertices):
        for j, second in enumerate(vertices):
            if i == j:
                continue
            remaining = [v for v in vertices if v not in (first, second)]
            out[i][j] = hafnian(remaining, edge_values)
    return out


def cofactor_derivative(vertices, edge_values, edge_tangent):
    out = zero(len(vertices), len(vertices))
    for i, first in enumerate(vertices):
        for j, second in enumerate(vertices):
            if i == j:
                continue
            remaining = [v for v in vertices if v not in (first, second)]
            out[i][j] = hafnian_derivative(
                remaining, edge_values, edge_tangent
            )
    return out


def quadratic_product(left, right):
    out = {}
    for edge_left, value_left in left.items():
        for edge_right, value_right in right.items():
            support_left = set(edge_left)
            support_right = set(edge_right)
            if support_left.isdisjoint(support_right):
                support = tuple(sorted(support_left | support_right))
                out[support] = out.get(support, Q(0)) + value_left * value_right
    return {support: value for support, value in out.items() if value}


def block_submatrix(a, rows, cols):
    return [[a[i][j] for j in cols] for i in rows]


def matrix_fingerprint(matrix):
    return tuple(tuple(entry for entry in row) for row in matrix)


def full_block_fingerprint(sites, blocks):
    pairs = tuple(combinations(sites, 2))
    require(set(blocks) == set(pairs), "fixed-block key manifest changed")
    return tuple(
        (left, right, matrix_fingerprint(blocks[(left, right)]))
        for left, right in pairs
    )


def expected_fixed_block_fingerprint(sites):
    z = zero(3, 3)
    e00 = matrix_unit(0, 0)
    e01 = matrix_unit(0, 1)
    e02 = matrix_unit(0, 2)
    e10 = matrix_unit(1, 0)
    e11 = matrix_unit(1, 1)
    e12 = matrix_unit(1, 2)
    e20 = matrix_unit(2, 0)
    e21 = matrix_unit(2, 1)
    e22 = matrix_unit(2, 2)
    direct = [[Q(-1, 3) for _ in range(3)] for _ in range(3)]
    expected = {
        ("p", "q"): direct,
        ("p", "x0"): e00,
        ("p", "x1"): e11,
        ("p", "x2"): e22,
        ("p", "y0"): z,
        ("p", "y1"): z,
        ("p", "y2"): z,
        ("q", "x0"): z,
        ("q", "x1"): z,
        ("q", "x2"): z,
        ("q", "y0"): e00,
        ("q", "y1"): e11,
        ("q", "y2"): e22,
        ("x0", "x1"): scale(Q(-1), e11),
        ("x0", "x2"): e12,
        ("x0", "y0"): e00,
        ("x0", "y1"): e01,
        ("x0", "y2"): e02,
        ("x1", "x2"): z,
        ("x1", "y0"): e10,
        ("x1", "y1"): e11,
        ("x1", "y2"): e12,
        ("x2", "y0"): e20,
        ("x2", "y1"): e21,
        ("x2", "y2"): e22,
        ("y0", "y1"): z,
        ("y0", "y2"): z,
        ("y1", "y2"): z,
    }
    return full_block_fingerprint(sites, expected)


def check_general_opposite_shore_expansion():
    h_xx = [[Q(2), Q(-1), Q(3)], [Q(4), Q(5), Q(-2)], [Q(1), Q(7), Q(6)]]
    h_xy = [[Q(-3), Q(2), Q(1)], [Q(5), Q(-4), Q(6)], [Q(7), Q(8), Q(-1)]]
    h_yy = [[Q(9), Q(1), Q(-5)], [Q(2), Q(3), Q(4)], [Q(-2), Q(6), Q(7)]]
    hdot_xy = [[Q(1), Q(3), Q(-2)], [Q(0), Q(5), Q(4)], [Q(7), Q(-1), Q(2)]]
    pdot_x = [[Q(2), Q(1), Q(0)], [Q(-1), Q(3), Q(4)], [Q(5), Q(-2), Q(1)]]
    pdot_y = [[Q(1), Q(-3), Q(2)], [Q(4), Q(0), Q(5)], [Q(-2), Q(6), Q(1)]]
    sdot_x = [[Q(3), Q(1), Q(-1)], [Q(2), Q(-4), Q(5)], [Q(0), Q(6), Q(2)]]
    sdot_y = [[Q(-2), Q(4), Q(1)], [Q(3), Q(5), Q(-1)], [Q(6), Q(0), Q(2)]]

    raw = hdot_xy
    mdot = add(
        add(
            add(mul(transpose(pdot_x), h_xy), hdot_xy),
            mul(h_xy, sdot_y),
        ),
        add(mul(h_xx, sdot_x), mul(transpose(pdot_y), h_yy)),
    )
    normalized = sub(
        sub(mdot, mul(transpose(pdot_x), h_xy)),
        mul(h_xy, sdot_y),
    )
    leakage = sub(normalized, raw)
    opposite = add(mul(h_xx, sdot_x), mul(transpose(pdot_y), h_yy))
    require(equal(leakage, opposite), "opposite-shore expansion failed")
    require(leakage != zero(3, 3), "generic expansion fixture became vacuous")
    return "general_opposite_shore_expansion"


def check_fixed_block_guard():
    sites = ("p", "q", "x0", "x1", "x2", "y0", "y1", "y2")
    order = {site: i for i, site in enumerate(sites)}
    blocks = {}

    def set_block(left, right, value):
        require(order[left] < order[right], "blocks must be stored forward")
        blocks[(left, right)] = value

    def get_block(left, right):
        if order[left] < order[right]:
            return blocks.get((left, right), zero(3, 3))
        return transpose(blocks.get((right, left), zero(3, 3)))

    all_one = [[Q(1) for _ in range(3)] for _ in range(3)]
    direct = scale(Q(-1, 3), all_one)
    set_block("p", "q", direct)
    for i in range(3):
        set_block("p", f"x{i}", matrix_unit(i, i))
        set_block("p", f"y{i}", zero(3, 3))
        set_block("q", f"x{i}", zero(3, 3))
        set_block("q", f"y{i}", matrix_unit(i, i))
        for j in range(3):
            set_block(f"x{i}", f"y{j}", matrix_unit(i, j))
    set_block("x0", "x1", scale(Q(-1), matrix_unit(1, 1)))
    set_block("x0", "x2", matrix_unit(1, 2))
    set_block("x1", "x2", zero(3, 3))
    for i, j in combinations(range(3), 2):
        set_block(f"y{i}", f"y{j}", zero(3, 3))
    require(
        full_block_fingerprint(sites, blocks)
        == expected_fixed_block_fingerprint(sites),
        "exact fixed-block fingerprint changed",
    )

    basis = eye(3)
    residual = ("x0", "x1", "x2", "y0", "y1", "y2")
    u = {f"x{i}": basis[i] for i in range(3)}
    u.update({f"y{i}": basis[i] for i in range(3)})
    du = {site: [Q(0), Q(0), Q(0)] for site in residual}
    du["x0"] = basis[1]

    def star(endpoint, vectors):
        return [
            [
                sum(
                    (
                        get_block(endpoint, site)[colour][k] * vectors[site][k]
                        for k in range(3)
                    ),
                    Q(0),
                )
                for colour in range(3)
            ]
            for site in residual
        ]

    p = star("p", u)
    s = star("q", u)
    pdot = star("p", du)
    sdot = star("q", du)
    x_rows = [0, 1, 2]
    y_rows = [3, 4, 5]
    require(block_submatrix(p, x_rows, range(3)) == eye(3), "P_X is not I")
    require(block_submatrix(p, y_rows, range(3)) == zero(3, 3), "P_Y is not zero")
    require(block_submatrix(s, x_rows, range(3)) == zero(3, 3), "S_X is not zero")
    require(block_submatrix(s, y_rows, range(3)) == eye(3), "S_Y is not I")
    require(pdot == zero(6, 3) and sdot == zero(6, 3), "selectors drifted")

    q0 = {}
    qdot = {}
    for left, right in combinations(residual, 2):
        edge = tuple(sorted((left, right), key=order.get))
        value = bilinear(u[left], get_block(left, right), u[right])
        tangent = bilinear(du[left], get_block(left, right), u[right])
        tangent += bilinear(u[left], get_block(left, right), du[right])
        if value:
            q0[edge] = value
        if tangent:
            qdot[edge] = tangent

    expected_q = {
        (f"x{i}", f"y{j}"): Q(1) for i in range(3) for j in range(3)
    }
    require(q0 == expected_q, "residual base is not the all-one K_3,3")
    require(
        qdot == {("x0", "x1"): Q(-1), ("x0", "x2"): Q(1)},
        "wrong physical Hessian-kernel tangent",
    )
    require(not quadratic_product(qdot, q0), "qdot*q is nonzero")

    f_haf = hafnian(residual, q0)
    fdot = hafnian_derivative(residual, q0, qdot)
    h = cofactor_matrix(residual, q0)
    hdot = cofactor_derivative(residual, q0, qdot)
    h_xx = block_submatrix(h, x_rows, x_rows)
    h_xy = block_submatrix(h, x_rows, y_rows)
    h_yy = block_submatrix(h, y_rows, y_rows)
    require(f_haf == 6 and fdot == 0, "wrong top hafnian jet")
    require(h_xx == zero(3, 3) and h_yy == zero(3, 3), "same-shore cofactor survived")
    require(h_xy == scale(Q(2), all_one), "wrong cross-shore cofactor")
    require(hdot == zero(6, 6), "raw cofactors were not stationary")

    m = mul(mul(transpose(p), h), s)
    mdot = add(
        add(mul(mul(transpose(pdot), h), s), mul(mul(transpose(p), hdot), s)),
        mul(mul(transpose(p), h), sdot),
    )

    target = zero(3, 3)
    target_dot = zero(3, 3)
    for colour in range(3):
        product = Q(1)
        for site in residual:
            product *= u[site][colour]
        target[colour][colour] = product
        derivative = Q(0)
        for varied in residual:
            term = du[varied][colour]
            for site in residual:
                if site != varied:
                    term *= u[site][colour]
            derivative += term
        target_dot[colour][colour] = derivative

    require(target == zero(3, 3) and target_dot == zero(3, 3), "target jet survived")
    require(m == sub(target, scale(f_haf, direct)), "base full-nine matrix failed")
    require(
        mdot == sub(target_dot, scale(fdot, direct)),
        "tangent full-nine matrix failed",
    )

    leakage = add(mul(h_xx, block_submatrix(sdot, x_rows, range(3))),
                  mul(transpose(block_submatrix(pdot, y_rows, range(3))), h_yy))
    require(leakage == zero(3, 3), "opposite-shore leakage is nonzero")

    # Read the physical curvature entries from the same eight-site blocks.
    a = get_block("p", "q")[0][0]
    b = get_block("p", "x1")[0][1]
    c = get_block("q", "x1")[0][1]
    e = get_block("p", "y1")[0][1]
    f_qs = get_block("q", "y1")[0][1]
    uu = get_block("x1", "y1")[1][1]
    curvature = a * uu - b * f_qs
    require(
        (a, b, c, e, f_qs, uu, curvature)
        == (Q(-1, 3), Q(0), Q(0), Q(0), Q(0), Q(1), Q(-1, 3)),
        "wrong fixed-block curvature packet",
    )
    return (
        "fixed_block_guard",
        (a, b, c, e, f_qs, uu, curvature),
    )


def poly_constant(value):
    return {} if value == 0 else {(0, 0, 0, 0, 0): Q(value)}


def poly_variable(index):
    exponent = [0, 0, 0, 0, 0]
    exponent[index] = 1
    return {tuple(exponent): Q(1)}


def poly_add(left, right):
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, Q(0)) + coefficient
        if out[monomial] == 0:
            del out[monomial]
    return out


def poly_scale(coefficient, polynomial):
    return {
        monomial: coefficient * value
        for monomial, value in polynomial.items()
        if coefficient * value
    }


def poly_sub(left, right):
    return poly_add(left, poly_scale(Q(-1), right))


def poly_mul(left, right):
    out = {}
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(
                monomial_left[i] + monomial_right[i] for i in range(5)
            )
            out[monomial] = (
                out.get(monomial, Q(0)) + coefficient_left * coefficient_right
            )
    return {monomial: value for monomial, value in out.items() if value}


def check_power_free_packet(a, b, c, e, f_qs, uu, curvature):
    x, y, t, v, z = (poly_variable(i) for i in range(5))
    r = Q(3)
    m_minus_two = Q(2)

    p_pq = poly_add(poly_scale(r, poly_mul(x, y)), poly_scale(a, z))
    p_pr = poly_add(poly_scale(r, poly_mul(x, t)), poly_scale(b, z))
    transition = poly_sub(poly_scale(a, t), poly_scale(b, y))
    l_pq_r = poly_add(
        poly_scale(r, poly_add(poly_scale(b, y), poly_scale(c, x))),
        poly_scale(a, t),
    )
    l_pr_q = poly_add(
        poly_scale(r, poly_add(poly_scale(a, t), poly_scale(c, x))),
        poly_scale(b, y),
    )
    l_pq_s = poly_add(
        poly_scale(r, poly_add(poly_scale(e, y), poly_scale(f_qs, x))),
        poly_scale(a, v),
    )
    l_pr_s = poly_add(
        poly_scale(r, poly_add(poly_scale(e, t), poly_scale(uu, x))),
        poly_scale(b, v),
    )

    connection = poly_sub(
        poly_sub(poly_mul(p_pq, t), poly_mul(p_pr, y)),
        poly_mul(transition, z),
    )
    require(not connection, "power-free connection failed")

    normal = poly_add(
        poly_sub(l_pq_r, l_pr_q), poly_scale(m_minus_two, transition)
    )
    require(not normal, "normal companion failed")

    curvature_left = poly_sub(
        poly_add(poly_scale(uu, p_pq), poly_mul(t, l_pq_s)),
        poly_add(poly_scale(f_qs, p_pr), poly_mul(y, l_pr_s)),
    )
    curvature_right = poly_add(
        poly_mul(transition, v), poly_scale(curvature, z)
    )
    require(
        not poly_sub(curvature_left, curvature_right),
        "four-site curvature row failed",
    )

    m_pq_rs = r * (b * f_qs + e * c) + a * uu
    m_pr_qs = r * (a * uu + e * c) + b * f_qs
    require(
        m_pq_rs - m_pr_qs == -m_minus_two * curvature,
        "direct-double companion failed",
    )
    require(
        (m_pq_rs, m_pr_qs) == (Q(-1, 3), Q(-1)),
        "wrong direct-double values",
    )
    return "power_free_packet"


def main():
    coverage = [check_general_opposite_shore_expansion()]
    fixed_block_section, packet = check_fixed_block_guard()
    coverage.append(fixed_block_section)
    coverage.append(check_power_free_packet(*packet))
    require(
        tuple(coverage)
        == (
            "general_opposite_shore_expansion",
            "fixed_block_guard",
            "power_free_packet",
        ),
        "checker section coverage manifest changed",
    )
    print(
        "separating 3+3 opposite-shore/Bianchi boundary: PASS; "
        "physical curvature=-1/3, every leakage cycle=0"
    )


if __name__ == "__main__":
    main()
