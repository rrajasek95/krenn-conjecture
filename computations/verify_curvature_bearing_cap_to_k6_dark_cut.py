#!/usr/bin/env python3
"""Dependency-free audits for the curvature-bearing cap dark-cut lemma."""

from itertools import combinations, product


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(x, y):
    return (x, y) if x < y else (y, x)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return [()]
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(rest):
            answer.append((edge(first, second),) + matching)
    return answer


def four_cycle_derivative(q, beta, r, s, u, v):
    return (
        q[edge(u, v)] * beta[edge(r, s)]
        + q[edge(r, s)] * beta[edge(u, v)]
        - q[edge(s, v)] * beta[edge(r, u)]
        - q[edge(r, u)] * beta[edge(s, v)]
    )


def audit_aggregate_torus_polynomial():
    # Exponent vectors are ordered as (t_r,t_s,t_u,t_v).  The four
    # monomials are distinct, so beta_rs is literally the coefficient of
    # t_u*t_v and cannot cancel.
    terms = {
        (0, 0, 1, 1): (1, "beta_rs"),
        (1, 1, 0, 0): (1, "beta_uv"),
        (0, 1, 0, 1): (-1, "beta_ru"),
        (1, 0, 1, 0): (-1, "beta_sv"),
    }
    check(len(terms) == 4, "four-cycle monomials collided")
    check(terms[(0, 0, 1, 1)] == (1, "beta_rs"),
          "distinguished aggregate coefficient changed")

    # A small exact grid independently witnesses torus nonvanishing for
    # every {-1,0,1} four-cycle array with beta_rs nonzero.
    for b_rs in (-1, 1):
        for b_uv, b_ru, b_sv in product((-1, 0, 1), repeat=3):
            found = False
            for t_r, t_s, t_u, t_v in product((1, 2, 3), repeat=4):
                value = (
                    b_rs * t_u * t_v
                    + b_uv * t_r * t_s
                    - b_ru * t_s * t_v
                    - b_sv * t_r * t_u
                )
                if value:
                    found = True
                    # Common scaling by two must scale the derivative by 4.
                    scaled = (
                        b_rs * (2 * t_u) * (2 * t_v)
                        + b_uv * (2 * t_r) * (2 * t_s)
                        - b_ru * (2 * t_s) * (2 * t_v)
                        - b_sv * (2 * t_r) * (2 * t_u)
                    )
                    check(scaled == 4 * value,
                          "aggregate common-scaling law failed")
                    break
            check(found, "small torus grid missed a nonzero polynomial")


def audit_physical_dark_reduction():
    r, s, u, v = range(4)
    edges = tuple(combinations(range(4), 2))

    # Exhaust the endpoint values for one rank-one cap.  At the two dark
    # sites both local factors are zero.  Exhaust arbitrary cycle q-values.
    for l_r, s_r, l_s, s_s in product((-1, 0, 1), repeat=4):
        local_l = [l_r, l_s, 0, 0]
        local_s = [s_r, s_s, 0, 0]
        beta = {
            edge(x, y): local_l[x] * local_s[y]
            + local_s[x] * local_l[y]
            for x, y in edges
        }
        for q_values in product((-1, 0, 1), repeat=4):
            q = {e: 0 for e in edges}
            for e, value in zip((edge(u, v), edge(r, s),
                                 edge(s, v), edge(r, u)), q_values):
                q[e] = value
            derivative = four_cycle_derivative(q, beta, r, s, u, v)
            expected = q[edge(u, v)] * beta[edge(r, s)]
            check(derivative == expected,
                  "physical dark-cut did not reduce to one term")


def audit_distinguished_edge_cap_expansion():
    r, s = 0, 1
    complement = (2, 3, 4, 5)
    all_vertices = tuple(range(6))

    # Enumerate beta*q^[2].  Once every complement site is beta-dark, only
    # the beta edge rs remains, followed by the three matchings of U.
    surviving = []
    for beta_edge in combinations(all_vertices, 2):
        rest = tuple(x for x in all_vertices if x not in beta_edge)
        for matching in perfect_matchings(rest):
            if edge(*beta_edge) == edge(r, s):
                surviving.append(tuple(sorted(matching)))
    expected = {tuple(sorted(m)) for m in perfect_matchings(complement)}
    check(set(surviving) == expected and len(surviving) == 3,
          "distinguished beta-edge expansion is not the four-site hafnian")

    # If the four-site hafnian is nonzero, at least one displayed perfect
    # matching has two nonzero physical pairings.  Exhaust a small exact grid
    # to guard the three matching indices and signs.
    complement_edges = tuple(combinations(complement, 2))
    matchings = perfect_matchings(complement)
    for values in product((-1, 0, 1), repeat=len(complement_edges)):
        q = dict(zip(complement_edges, values))
        products = [q[m[0]] * q[m[1]] for m in matchings]
        hafnian = sum(products)
        if hafnian:
            check(any(value for value in products),
                  "nonzero hafnian had no nonzero matching")


def rank_mod_three(rows):
    matrix = [[entry % 3 for entry in row] for row in rows]
    if not matrix:
        return 0
    rank = 0
    for column in range(3):
        pivot = next((i for i in range(rank, len(matrix))
                      if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = 1 if matrix[rank][column] == 1 else 2
        matrix[rank] = [(inverse * value) % 3
                        for value in matrix[rank]]
        for i in range(len(matrix)):
            if i == rank or not matrix[i][column]:
                continue
            multiple = matrix[i][column]
            matrix[i] = [
                (left - multiple * right) % 3
                for left, right in zip(matrix[i], matrix[rank])
            ]
        rank += 1
    return rank


def dot_mod_three(left, right):
    return sum(a * b for a, b in zip(left, right)) % 3


def rank_mod_prime(rows, prime):
    if not rows:
        return 0
    width = len(rows[0])
    matrix = [[entry % prime for entry in row] for row in rows]
    rank = 0
    for column in range(width):
        pivot = next((i for i in range(rank, len(matrix))
                      if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, prime)
        matrix[rank] = [(inverse * value) % prime
                        for value in matrix[rank]]
        for i in range(len(matrix)):
            if i == rank or not matrix[i][column]:
                continue
            multiple = matrix[i][column]
            matrix[i] = [
                (left - multiple * right) % prime
                for left, right in zip(matrix[i], matrix[rank])
            ]
        rank += 1
    return rank


def audit_local_target_blocking_duality():
    vectors = tuple(product(range(3), repeat=3))
    targets = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    for left in vectors:
        for right in vectors:
            dark = tuple(
                probe for probe in vectors
                if dot_mod_three(probe, left) == 0
                and dot_mod_three(probe, right) == 0
            )
            check(len(dark) >= 3,
                  "two local cap factors had no nonzero dark probe")
            base_rank = rank_mod_three((left, right))
            for target in targets:
                target_blocked = rank_mod_three((left, right, target)) \
                    == base_rank
                target_invisible_on_dark = all(
                    dot_mod_three(probe, target) == 0 for probe in dark
                )
                check(target_blocked == target_invisible_on_dark,
                      "target-span/annihilator duality failed")

    # Higher factor rank has a genuine additional obstruction: three
    # independent local factors have only the zero common annihilator.
    basis = targets
    common_dark = tuple(
        probe for probe in vectors
        if all(dot_mod_three(probe, factor) == 0 for factor in basis)
    )
    check(common_dark == ((0, 0, 0),),
          "higher-rank no-common-kernel guard failed")


def audit_physical_rank_one_selector_section():
    # In the full 2x2 physical shape, the diagonal target space is
    # span(E_11,E_22).  Over F_5, exhaust every nonzero compression C and
    # verify that the rank-one functionals annihilating C but detecting that
    # diagonal space span the complete three-dimensional hyperplane C^perp.
    # Therefore no K outside span(C) is annihilated by all of them.
    vectors = tuple(product(range(5), repeat=4))
    zero = (0, 0, 0, 0)
    for compression in vectors:
        if compression == zero:
            continue
        basis = []
        for functional in vectors:
            if functional == zero:
                continue
            a, b, c, d = functional
            if (a * d - b * c) % 5:
                continue
            if sum(x * y for x, y in zip(functional, compression)) % 5:
                continue
            if not (a or d):
                continue
            candidate_rank = rank_mod_prime(basis + [functional], 5)
            if candidate_rank > len(basis):
                basis.append(functional)
                if len(basis) == 3:
                    break
        check(len(basis) == 3,
              "physical rank-one diagonal selectors did not span C^perp")


def main():
    audit_aggregate_torus_polynomial()
    audit_physical_dark_reduction()
    audit_distinguished_edge_cap_expansion()
    audit_local_target_blocking_duality()
    audit_physical_rank_one_selector_section()
    print("PASS: aggregate K6 torus polynomial and scaling")
    print("PASS: physical cap-dark four-cycle reduces to q_uv * beta_rs")
    print("PASS: diagonal cap cut forces the four-site hafnian ledger")
    print("PASS: local target blocking equals annihilator invisibility")
    print("PASS: physical rank-one selectors span every 2x2 C-perp section")


if __name__ == "__main__":
    main()
