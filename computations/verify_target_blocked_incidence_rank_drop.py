#!/usr/bin/env python3
"""Lightweight exact audits for target-blocked rank-drop incidence."""

from itertools import combinations, product


FIELD = 3
SITES = tuple(range(6))
COLORS = tuple(range(3))


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def rank_mod(rows, modulus=FIELD):
    matrix = [[entry % modulus for entry in row] for row in rows]
    if not matrix:
        return 0
    columns = len(matrix[0])
    rank = 0
    for column in range(columns):
        pivot = next(
            (index for index in range(rank, len(matrix))
             if matrix[index][column] % modulus),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column] % modulus, -1, modulus)
        matrix[rank] = [inverse * value % modulus
                        for value in matrix[rank]]
        for index in range(len(matrix)):
            if index == rank:
                continue
            multiple = matrix[index][column] % modulus
            if multiple:
                matrix[index] = [
                    (left - multiple * right) % modulus
                    for left, right in zip(matrix[index], matrix[rank])
                ]
        rank += 1
    return rank


def mat_vec(matrix, vector, modulus=FIELD):
    return tuple(
        sum(row[index] * vector[index] for index in range(len(vector)))
        % modulus
        for row in matrix
    )


def transpose(matrix):
    return tuple(zip(*matrix))


def mat_mul(left, right, modulus=FIELD):
    right_t = transpose(right)
    return tuple(
        tuple(sum(a * b for a, b in zip(row, column)) % modulus
              for column in right_t)
        for row in left
    )


def dot(left, right, modulus=FIELD):
    return sum(a * b for a, b in zip(left, right)) % modulus


def det2(matrix, modulus=FIELD):
    return (matrix[0][0] * matrix[1][1]
            - matrix[0][1] * matrix[1][0]) % modulus


def proportional(left, right, modulus=FIELD):
    flat_left = tuple(value % modulus for row in left for value in row)
    flat_right = tuple(value % modulus for row in right for value in row)
    if not any(flat_right):
        return not any(flat_left)
    pivot = next(index for index, value in enumerate(flat_right) if value)
    scalar = flat_left[pivot] * pow(flat_right[pivot], -1, modulus) % modulus
    return all(a == scalar * b % modulus
               for a, b in zip(flat_left, flat_right))


def audit_local_predicate():
    vectors = tuple(product(range(FIELD), repeat=2))
    targets = ((1, 0, 0), (0, 1, 0))
    checks = 0
    for left2 in vectors:
        for right2 in vectors:
            left = left2 + (0,)
            right = right2 + (0,)
            wedge = (left2[0] * right2[1]
                     - left2[1] * right2[0]) % FIELD
            # The proposed 3-by-3 determinant is structurally zero.
            for target_index, target in enumerate(targets):
                blocked = rank_mod((left, right, target)) \
                    == rank_mod((left, right))
                other = 1 - target_index
                coordinate_line = (
                    left2[other] == 0
                    and right2[other] == 0
                    and (any(left2) or any(right2))
                )
                predicted = wedge != 0 or (wedge == 0 and coordinate_line)
                check(blocked == predicted,
                      "rank-drop/coordinate-line predicate failed")
                checks += 1
    return checks


def audit_invertible_kernel():
    j_matrix = ((0, 1), (-1, 0))
    matrices = tuple(
        ((a, b), (c, d))
        for a, b, c, d in product(range(FIELD), repeat=4)
    )
    nonzero_vectors = tuple(
        vector for vector in product(range(FIELD), repeat=2) if any(vector)
    )
    checks = 0
    for c_matrix in matrices:
        if det2(c_matrix) == 0:
            continue
        parameter_map = mat_mul(j_matrix, transpose(c_matrix))
        for n_matrix in matrices:
            vanishes = True
            for xi in nonzero_vectors:
                eta = mat_vec(parameter_map, xi)
                if dot(xi, mat_vec(n_matrix, eta)):
                    vanishes = False
                    break
            check(vanishes == proportional(n_matrix, c_matrix),
                  "invertible-conic kernel is not span(C)")
            checks += 1
    return checks


def outer(left, right, modulus=FIELD):
    return tuple(tuple(a * b % modulus for b in right) for a in left)


def is_left_aligned(matrix, vector, modulus=FIELD):
    # Every column belongs to span(vector).
    columns = transpose(matrix)
    return all(rank_mod((vector, column), modulus) <= 1
               for column in columns)


def is_right_aligned(matrix, vector, modulus=FIELD):
    # Every row belongs to span(vector).
    return all(rank_mod((vector, row), modulus) <= 1 for row in matrix)


def audit_rank_one_rulings():
    matrices = tuple(
        ((a, b), (c, d))
        for a, b, c, d in product(range(FIELD), repeat=4)
    )
    nonzero_vectors = tuple(
        vector for vector in product(range(FIELD), repeat=2) if any(vector)
    )
    checks = 0
    for a_vector in nonzero_vectors:
        xi_zero = (a_vector[1], -a_vector[0])
        for n_matrix in matrices:
            left_vanishes = all(
                dot(xi_zero, mat_vec(n_matrix, eta)) == 0
                for eta in nonzero_vectors
            )
            check(left_vanishes == is_left_aligned(n_matrix, a_vector),
                  "left ruling alignment classification failed")
            checks += 1
    for b_vector in nonzero_vectors:
        eta_zero = (b_vector[1], -b_vector[0])
        for n_matrix in matrices:
            right_vanishes = all(
                dot(xi, mat_vec(n_matrix, eta_zero)) == 0
                for xi in nonzero_vectors
            )
            check(right_vanishes == is_right_aligned(n_matrix, b_vector),
                  "right ruling alignment classification failed")
            checks += 1
    return checks


def edge(x, y):
    return (x, y) if x < y else (y, x)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


MATCHINGS = tuple(perfect_matchings(SITES))

# Guard (24): local coefficient dictionaries for the two cap factors.
LOCAL_L = {
    (0, 0): 1,
    (2, 0): 1,
    (4, 0): 1,
}
LOCAL_S = {
    (1, 0): 1,
    (2, 1): 1,
    (4, 1): 1,
}
Q = {
    (2, 3, 0, 0): 1,
    (4, 5, 0, 0): 1,
}


def beta_coefficient(x, y, color_x, color_y):
    return (
        LOCAL_L.get((x, color_x), 0) * LOCAL_S.get((y, color_y), 0)
        + LOCAL_S.get((x, color_x), 0) * LOCAL_L.get((y, color_y), 0)
    )


def q_coefficient(x, y, color_x, color_y):
    if x > y:
        x, y = y, x
        color_x, color_y = color_y, color_x
    return Q.get((x, y, color_x, color_y), 0)


def tangent_coefficient(word):
    total = 0
    for matching in MATCHINGS:
        for distinguished in range(3):
            term = 1
            for index, (x, y) in enumerate(matching):
                if index == distinguished:
                    term *= beta_coefficient(x, y, word[x], word[y])
                else:
                    term *= q_coefficient(x, y, word[x], word[y])
            total += term
    return total


def local_vectors(site):
    left = tuple(LOCAL_L.get((site, color), 0) for color in COLORS)
    right = tuple(LOCAL_S.get((site, color), 0) for color in COLORS)
    return left, right


def annihilator_basis(site):
    left, right = local_vectors(site)
    return tuple(
        probe for probe in product((-1, 0, 1), repeat=3)
        if any(probe) and dot(probe, left, 0x7FFFFFFF) == 0
        and dot(probe, right, 0x7FFFFFFF) == 0
    )


def integer_dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def audit_exact_guard():
    support = {}
    for word in product(COLORS, repeat=6):
        value = tangent_coefficient(word)
        if value:
            support[word] = value
    check(support == {(0, 0, 0, 0, 0, 0): 1},
          "guard cap identity is not beta*q^[2] = X_0")
    check(beta_coefficient(0, 1, 0, 0) == 1,
          "distinguished cap coefficient changed")

    target = (1, 0, 0)
    for site in (2, 4):
        left, right = local_vectors(site)
        check(rank_mod((left, right)) == 2,
              "guard blocking site lost its missing-plane rank")
        check(rank_mod((left, right, target)) == 2,
              "guard target is no longer blocked")

    # Use explicit integer annihilator vectors; at sites 2 and 4 they all
    # kill colour zero, so both supported q-edges vanish on dark products.
    dark = {
        2: ((0, 0, 1),),
        3: ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        4: ((0, 0, 1),),
        5: ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
    }
    for site, probes in dark.items():
        left, right = local_vectors(site)
        check(all(integer_dot(probe, left) == 0
                  and integer_dot(probe, right) == 0
                  for probe in probes),
              "listed dark basis does not annihilate the cap")
    for x, y in combinations((2, 3, 4, 5), 2):
        for probe_x in dark[x]:
            for probe_y in dark[y]:
                value = sum(
                    coefficient * probe_x[color_x] * probe_y[color_y]
                    for (u, v, color_x, color_y), coefficient in Q.items()
                    if (u, v) == edge(x, y)
                )
                check(value == 0, "dark complement acquired a q-edge")

    # The endpoint triples in (30) are visibly independent; audit their
    # coefficient vectors in the 18-dimensional decorated port space.
    def form_vector(table):
        return tuple(table.get((site, color), 0)
                     for site in SITES for color in COLORS)

    unit_31 = {(3, 1): 1}
    unit_52 = {(5, 2): 1}
    p_rows = (form_vector(LOCAL_L), form_vector(unit_31),
              form_vector(unit_52))
    s_rows = (form_vector(LOCAL_S), form_vector(unit_31),
              form_vector(unit_52))
    check(rank_mod(p_rows) == 3 and rank_mod(s_rows) == 3,
          "good-star extensions lost injectivity")

    # Selector/curvature matrices from (28)--(29).
    c_matrix = ((0, 0), (0, 1))
    k_matrix = ((-1, 0), (0, 0))
    ell_matrix = ((1, 0), (0, 0))
    pairing = lambda left, right: sum(
        left[i][j] * right[i][j] for i in range(2) for j in range(2)
    )
    check(pairing(ell_matrix, c_matrix) == 0,
          "guard selector is not isotropic")
    check(pairing(ell_matrix, k_matrix) == -1,
          "guard selector lost nonradial curvature")
    check(not proportional(k_matrix, c_matrix),
          "guard curvature became radial")
    check(local_vectors(0)[1] == (0, 0, 0)
          and local_vectors(1)[0] == (0, 0, 0),
          "guard lost its T=0 triangular orientation")
    return len(support)


def main():
    local_checks = audit_local_predicate()
    invertible_checks = audit_invertible_kernel()
    ruling_checks = audit_rank_one_rulings()
    audit_exact_guard()
    print(f"PASS: {local_checks} exact local blocking predicates")
    print(f"PASS: {invertible_checks} invertible-conic kernel checks")
    print(f"PASS: {ruling_checks} singular ruling alignment checks")
    print("PASS: 729-word target-blocked T=0 dark-complement guard")


if __name__ == "__main__":
    main()
