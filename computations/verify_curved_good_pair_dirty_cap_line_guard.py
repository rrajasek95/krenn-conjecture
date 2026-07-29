#!/usr/bin/env python3
"""Exact audit of the curved full-good-fan dirty-cap root guard."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import product

from verify_multiresponse_inactive_core_evacuation import rref_nullspace
from verify_n8_rank_one_clean_cap_local_torus_obstruction import (
    cubic_sector,
    rational_rank,
    square_free_product,
)
from verify_polarized_paircap_counterexample import paircap_example, perfect_matchings


C = 3
SITES = tuple(range(8))
P_SITE = 6
Q_SITE = 7


def add_cell(blocks, u, v, a, b, value):
    if u > v:
        u, v, a, b = v, u, b, a
    blocks[u, v, a, b] += F(value)
    if not blocks[u, v, a, b]:
        del blocks[u, v, a, b]


def build_source():
    internal, p_star, q_star, _ = paircap_example()
    blocks = Counter()
    for ((u, v), a, b), value in internal.items():
        add_cell(blocks, u, v, a, b, value)

    for (u, a), value in p_star.items():
        add_cell(blocks, P_SITE, u, 0, a, 3 * value)
    for (u, a), value in q_star.items():
        add_cell(blocks, Q_SITE, u, 0, a, value)

    # The traceless diagonal padding leaves contraction by lambda I fixed.
    add_cell(blocks, P_SITE, Q_SITE, 0, 0, 3)
    add_cell(blocks, P_SITE, Q_SITE, 1, 1, 1)
    add_cell(blocks, P_SITE, Q_SITE, 2, 2, -1)

    # These two full-rank endpoint blocks make both stars injective at pq.
    # Their diagonal and (1,2) cap products collide at site 0.
    add_cell(blocks, P_SITE, 0, 1, 0, 1)
    add_cell(blocks, P_SITE, 0, 2, 2, 1)
    add_cell(blocks, Q_SITE, 0, 1, 0, 1)
    add_cell(blocks, Q_SITE, 0, 2, 2, 1)
    return dict(blocks)


def block_value(blocks, u, v, a, b):
    if u < v:
        return blocks.get((u, v, a, b), F(0))
    return blocks.get((v, u, b, a), F(0))


def matching_tensor(blocks, vertices):
    vertices = tuple(vertices)
    positions = {site: index for index, site in enumerate(vertices)}
    out = Counter()
    for matching in perfect_matchings(vertices):
        choices = []
        for u, v in matching:
            cells = []
            for a, b in product(range(C), repeat=2):
                value = block_value(blocks, u, v, a, b)
                if value:
                    cells.append((a, b, value))
            choices.append(cells)
        for selected in product(*choices):
            word = [None] * len(vertices)
            coefficient = F(1)
            for (u, v), (a, b, value) in zip(matching, selected):
                word[positions[u]] = a
                word[positions[v]] = b
                coefficient *= value
            out[tuple(word)] += coefficient
    return {word: value for word, value in out.items() if value}


def endpoint_form(blocks, endpoint, colour, retained):
    return {
        (site, local_colour): value
        for site in retained
        for local_colour in range(C)
        if (
            value := block_value(
                blocks, endpoint, site, colour, local_colour
            )
        )
    }


def add_quadratics(*terms):
    out = Counter()
    for scale, quadratic in terms:
        for cell, value in quadratic.items():
            out[cell] += scale * value
    return {cell: value for cell, value in out.items() if value}


def cap_data(blocks, cap):
    retained = tuple(range(6))
    p_forms = [endpoint_form(blocks, P_SITE, a, retained) for a in range(C)]
    q_forms = [endpoint_form(blocks, Q_SITE, b, retained) for b in range(C)]
    scalar = F(0)
    response_terms = []
    for a, b in product(range(C), repeat=2):
        coefficient = cap[3 * a + b]
        scalar += coefficient * block_value(blocks, P_SITE, Q_SITE, a, b)
        if coefficient:
            response_terms.append(
                (coefficient, square_free_product(p_forms[a], q_forms[b]))
            )
    return scalar, add_quadratics(*response_terms)


def clean_error(old_edges, scalar, response_edges):
    two_response = cubic_sector(old_edges, response_edges, 2)
    three_response = cubic_sector(old_edges, response_edges, 3)
    return {
        word: scalar * two_response.get(word, F(0))
        + three_response.get(word, F(0))
        for word in product(range(C), repeat=6)
        if scalar * two_response.get(word, F(0))
        + three_response.get(word, F(0))
    }


def residual_matrix(blocks, left, right):
    top = matching_tensor(blocks, SITES)
    rest = tuple(v for v in SITES if v not in (left, right))
    rows = []
    for word in product(range(C), repeat=len(rest)):
        row = []
        for a, b in product(range(C), repeat=2):
            full = dict(zip(rest, word))
            full[left] = a
            full[right] = b
            coefficient = top.get(tuple(full[v] for v in SITES), F(0))
            if a == b and word == (a,) * len(rest):
                coefficient -= 1
            row.append(coefficient)
        rows.append(row)
    return rows


def star_rank(blocks, endpoint, deleted_partner):
    columns = []
    for colour in range(C):
        column = []
        for site in SITES:
            if site in (endpoint, deleted_partner):
                continue
            for local_colour in range(C):
                column.append(
                    block_value(blocks, endpoint, site, colour, local_colour)
                )
        columns.append(column)
    rows = [list(row) for row in zip(*columns)]
    return C - len(rref_nullspace(rows))


def hessian_rows(old_edges):
    cells = tuple(
        ((u, v), a, b)
        for u in range(6)
        for v in range(u + 1, 6)
        for a, b in product(range(C), repeat=2)
    )
    rows = []
    for word in product(range(C), repeat=6):
        row = []
        for (u, v), a, b in cells:
            if (word[u], word[v]) != (a, b):
                row.append(F(0))
                continue
            retained = tuple(site for site in range(6) if site not in (u, v))
            value = F(0)
            for matching in perfect_matchings(retained):
                term = F(1)
                for i, j in matching:
                    term *= old_edges.get(((i, j), word[i], word[j]), F(0))
                value += term
            row.append(value)
        rows.append(row)
    return cells, rows


def audit_gauge_rigidity(old_edges):
    cells, rows = hessian_rows(old_edges)
    assert len(rref_nullspace(rows)) == 5

    gauges = []
    for distinguished in range(5):
        alpha = [F(0)] * 6
        alpha[distinguished] = F(1)
        alpha[5] = F(-1)
        gauge = tuple(
            (alpha[u] + alpha[v])
            * old_edges.get(((u, v), a, b), F(0))
            for (u, v), a, b in cells
        )
        gauges.append(gauge)
        assert all(
            sum(coefficient * value for coefficient, value in zip(row, gauge))
            == 0
            for row in rows
        )
    assert rational_rank(gauges) == 5

    # The exact nullity is five and these five rational gauges are
    # independent, so the Hessian kernel is precisely the zero-sum gauge
    # space.  No internal block has rank three.
    for u in range(6):
        for v in range(u + 1, 6):
            block_rows = [
                [old_edges.get(((u, v), a, b), F(0)) for b in range(C)]
                for a in range(C)
            ]
            assert rational_rank(block_rows) < 3


def quadratic_on(blocks, retained):
    retained = tuple(retained)
    return {
        ((u, v), a, b): value
        for u_index, u in enumerate(retained)
        for v in retained[u_index + 1 :]
        for a, b in product(range(C), repeat=2)
        if (value := block_value(blocks, u, v, a, b))
    }


def linear_combination(*terms):
    out = Counter()
    for scale, vector in terms:
        for coordinate, value in vector.items():
            out[coordinate] += scale * value
    return {coordinate: value for coordinate, value in out.items() if value}


def audit_four_site_connection(blocks):
    # Exposed sites and colours (p,q,r,s;a,b,c,d)=(6,7,0,1;0,0,1,0).
    p, q, r, s = P_SITE, Q_SITE, 0, 1
    a, b, c, d = 0, 0, 1, 0
    retained = (2, 3, 4, 5)
    degree = 3  # R=m-1 at N=8.

    A = block_value(blocks, p, q, a, b)
    B = block_value(blocks, p, r, a, c)
    C_direct = block_value(blocks, q, r, b, c)
    E = block_value(blocks, p, s, a, d)
    F_direct = block_value(blocks, q, s, b, d)
    U = block_value(blocks, r, s, c, d)
    assert (A, B, C_direct, E, F_direct, U) == (3, 0, 1, 3, 1, -1)

    first_curvature = A * U - B * F_direct
    second_curvature = A * U - E * C_direct
    third_curvature = B * F_direct - E * C_direct
    assert (first_curvature, second_curvature, third_curvature) == (-3, -6, -3)
    assert first_curvature - second_curvature + third_curvature == 0

    x = endpoint_form(blocks, p, a, retained)
    y = endpoint_form(blocks, q, b, retained)
    t = endpoint_form(blocks, r, c, retained)
    v = endpoint_form(blocks, s, d, retained)
    z = quadratic_on(blocks, retained)
    p_pq = add_quadratics((degree, square_free_product(x, y)), (A, z))
    p_pr = add_quadratics((degree, square_free_product(x, t)), (B, z))
    l_pq_s = linear_combination(
        (degree * E, y), (degree * F_direct, x), (A, v)
    )
    l_pr_s = linear_combination((degree * E, t), (degree * U, x), (B, v))
    transition = linear_combination((A, t), (-B, y))

    # Equation (9): U P_pq+t L_pq;s-F P_pr-y L_pr;s=Dv+kappa z.
    left = add_quadratics(
        (U, p_pq),
        (1, square_free_product(t, l_pq_s)),
        (-F_direct, p_pr),
        (-1, square_free_product(y, l_pr_s)),
    )
    right = add_quadratics(
        (1, square_free_product(transition, v)), (first_curvature, z)
    )
    assert left == right


def basis_cap(*entries):
    cap = [F(0)] * 9
    for a, b, value in entries:
        cap[3 * a + b] = F(value)
    return tuple(cap)


def main():
    blocks = build_source()
    fan = tuple(site for site in SITES if site != P_SITE)
    ranks = {
        neighbour: (
            star_rank(blocks, P_SITE, neighbour),
            star_rank(blocks, neighbour, P_SITE),
        )
        for neighbour in fan
    }
    assert set(ranks.values()) == {(3, 3)}
    audit_four_site_connection(blocks)

    identity = basis_cap((0, 0, 1), (1, 1, 1), (2, 2, 1))
    e00 = basis_cap((0, 0, 1))
    e12 = basis_cap((1, 2, 1))
    e21 = basis_cap((2, 1, 1))
    residual = residual_matrix(blocks, P_SITE, Q_SITE)
    compatible_kernel = rref_nullspace(residual)
    assert len(compatible_kernel) == 3
    assert set(compatible_kernel) == {e12, e21, identity}

    old_edges, _, _, _ = paircap_example()
    audit_gauge_rigidity(old_edges)
    s_identity, r_identity = cap_data(blocks, identity)
    s_e00, r_e00 = cap_data(blocks, e00)
    s_e12, r_e12 = cap_data(blocks, e12)
    s_e21, r_e21 = cap_data(blocks, e21)
    assert s_identity == s_e00 == 3
    assert r_identity == r_e00
    assert (s_e12, r_e12, s_e21, r_e21) == (0, {}, 0, {})

    error = clean_error(old_edges, s_identity, r_identity)
    expected_error = {
        (1, 0, 0, 1, 0, 0): F(9),
        (2, 0, 1, 1, 0, 2): F(54),
    }
    assert error == expected_error

    # K=lambda I+uE12+vE21 has error lambda^3*error and activity 3lambda^4.
    # K=E00+lambda I has error (1+lambda)^3*error; its sole clean value
    # lambda=-1 kills both s and kappa_0, so it is inactive.
    assert any(row[4] for row in residual)

    print(
        "curved full-good-fan dirty-cap guard: PASS; "
        f"fan={len(fan)} with ranks 3/3; curvature=-3; "
        "compatible cap plane=3; dirty support=2"
    )


if __name__ == "__main__":
    main()
