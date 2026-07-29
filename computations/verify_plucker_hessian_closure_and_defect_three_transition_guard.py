#!/usr/bin/env python3
"""Exact lightweight audit for the physical defect-three transition guard."""

from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations, product


COLORS = range(3)
SITES = tuple(range(12))
PLUS = (tuple(range(3)), tuple(range(3, 6)), tuple(range(6, 9)))
HUB = (9, 10, 11)
E = tuple(tuple(Q(int(a == c)) for a in COLORS) for c in COLORS)
ZERO = tuple(tuple(Q(0) for _ in COLORS) for _ in COLORS)
IDENTITY = tuple(tuple(Q(int(a == b)) for b in COLORS) for a in COLORS)


def outer(left, right):
    return tuple(tuple(left[a] * right[b] for b in COLORS) for a in COLORS)


def transpose(matrix):
    return tuple(tuple(matrix[b][a] for b in COLORS) for a in COLORS)


def determinant(matrix):
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


Q_BLOCKS = {}
for c in COLORS:
    for i in PLUS[c]:
        Q_BLOCKS[i, HUB[c]] = IDENTITY
for c, d in combinations(COLORS, 2):
    for i in PLUS[c]:
        for j in PLUS[d]:
            Q_BLOCKS[i, j] = outer(E[c], E[d])


def q_block(i, j):
    if i < j:
        return Q_BLOCKS.get((i, j), ZERO)
    return transpose(Q_BLOCKS.get((j, i), ZERO))


X = []
for c in COLORS:
    row = [(Q(0), Q(0), Q(0)) for _ in SITES]
    for i in PLUS[c]:
        row[i] = E[c]
    X.append(tuple(row))
X = tuple(X)


ZETA = []
for c in COLORS:
    zeta = [Q(0)] * len(SITES)
    for i in PLUS[c]:
        zeta[i] = Q(1)
    zeta[HUB[c]] = Q(-1)
    ZETA.append(tuple(zeta))
ZETA = tuple(ZETA)

COEFFICIENTS = {
    (0, 1): (Q(1, 2), Q(1, 2), Q(-1, 2)),
    (0, 2): (Q(1, 2), Q(-1, 2), Q(1, 2)),
    (1, 2): (Q(-1, 2), Q(1, 2), Q(1, 2)),
}


def alpha(c, d):
    coefficients = COEFFICIENTS[tuple(sorted((c, d)))]
    return tuple(sum(coefficients[k] * ZETA[k][i] for k in COLORS) for i in SITES)


def add_matrices(*matrices):
    return tuple(tuple(sum(matrix[a][b] for matrix in matrices)
                       for b in COLORS) for a in COLORS)


def product_block(left, right, i, j):
    return add_matrices(outer(left[i], right[j]), outer(right[i], left[j]))


def scale_matrix(scalar, matrix):
    return tuple(tuple(scalar * matrix[a][b] for b in COLORS) for a in COLORS)


def gamma_block(weights, i, j):
    return scale_matrix(weights[i] + weights[j], q_block(i, j))


def rational_rank(rows):
    rows = [list(map(Q, row)) for row in rows]
    rank = 0
    for column in range(len(rows[0])):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        value = rows[rank][column]
        rows[rank] = [entry / value for entry in rows[rank]]
        for r in range(len(rows)):
            if r == rank or not rows[r][column]:
                continue
            value = rows[r][column]
            rows[r] = [a - value * b for a, b in zip(rows[r], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return rank


def flatten_quadratic(block_function):
    return tuple(block_function(i, j)[a][b]
                 for i, j in combinations(SITES, 2)
                 for a, b in product(COLORS, repeat=2))


def has_perfect_matching(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return True
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        if q_block(first, second) == ZERO:
            continue
        rest = vertices[1:index] + vertices[index + 1:]
        if has_perfect_matching(rest):
            return True
    return False


# Sparse square-free elements use sorted tuples ((site, colour), ...).
def clean(element):
    return {key: value for key, value in element.items() if value}


def add_elements(left, right, right_scale=Q(1)):
    out = dict(left)
    for key, value in right.items():
        out[key] = out.get(key, Q(0)) + right_scale * value
    return clean(out)


def multiply(left, right):
    out = {}
    for key_left, value_left in left.items():
        sites_left = {site for site, _ in key_left}
        for key_right, value_right in right.items():
            if sites_left & {site for site, _ in key_right}:
                continue
            key = tuple(sorted(key_left + key_right))
            out[key] = out.get(key, Q(0)) + value_left * value_right
    return clean(out)


def linear_element(row):
    return {(i, a): value for i in SITES for a, value in enumerate(row[i]) if value}


def linear_product(left, right):
    left_element = {((i, a),): value for (i, a), value in linear_element(left).items()}
    right_element = {((i, a),): value for (i, a), value in linear_element(right).items()}
    return multiply(left_element, right_element)


def q_element():
    out = {}
    for (i, j), matrix in Q_BLOCKS.items():
        for a, b in product(COLORS, repeat=2):
            if matrix[a][b]:
                out[((i, a), (j, b))] = matrix[a][b]
    return out


def k_operator(weights, quadratic):
    sigma = sum(weights, Q(0))
    return {
        key: (sigma - sum(weights[site] for site, _ in key)) * value
        for key, value in quadratic.items()
        if (sigma - sum(weights[site] for site, _ in key)) * value
    }


Q_ELEMENT = q_element()


@lru_cache(maxsize=None)
def q_top(vertices):
    """The divided power of q on exactly the displayed even vertex set."""
    vertices = tuple(vertices)
    if not vertices:
        return {(): Q(1)}
    first = vertices[0]
    out = {}
    for index in range(1, len(vertices)):
        second = vertices[index]
        block = q_block(first, second)
        if block == ZERO:
            continue
        rest = vertices[1:index] + vertices[index + 1:]
        tail = q_top(rest)
        for a, b in product(COLORS, repeat=2):
            coefficient = block[a][b]
            if not coefficient:
                continue
            head = ((first, a), (second, b))
            for key, value in tail.items():
                full_key = tuple(sorted(head + key))
                out[full_key] = out.get(full_key, Q(0)) + coefficient * value
    return clean(out)


def hessian(quadratic):
    out = {}
    for key, coefficient in quadratic.items():
        used = {site for site, _ in key}
        tail = q_top(tuple(site for site in SITES if site not in used))
        for rest, value in tail.items():
            full_key = tuple(sorted(key + rest))
            out[full_key] = out.get(full_key, Q(0)) + coefficient * value
    return clean(out)


def audit_responses_and_activity():
    rank_three_edges = {
        pair for pair in combinations(SITES, 2) if determinant(q_block(*pair))
    }
    assert rank_three_edges == {
        tuple(sorted((i, HUB[c]))) for c in COLORS for i in PLUS[c]
    }
    assert tuple(sum(zeta, Q(0)) for zeta in ZETA) == (Q(2), Q(2), Q(2))

    primitives = []
    responses = []
    for c in COLORS:
        for d in COLORS:
            if c == d:
                continue
            weights = alpha(c, d)
            assert sum(weights, Q(0)) == 1
            for i, j in combinations(SITES, 2):
                assert product_block(X[c], X[d], i, j) == gamma_block(weights, i, j)
            primitives.append(weights)
            responses.append(flatten_quadratic(
                lambda i, j, c=c, d=d: product_block(X[c], X[d], i, j)
            ))
    assert rational_rank(primitives) == 3
    assert rational_rank(responses) == 3
    assert all(sum(any(vector) for vector in row) == 3 for row in X)

    assert q_top(SITES)
    for deleted in combinations(SITES, 2):
        remaining = tuple(site for site in SITES if site not in deleted)
        assert has_perfect_matching(remaining)
        assert q_top(remaining)

    target = q_top(SITES)
    for c, d in combinations(COLORS, 2):
        response = linear_product(X[c], X[d])
        assert hessian(response) == target


def audit_transition_law():
    checks = 0
    for c in COLORS:
        for d in COLORS:
            if c == d:
                continue
            weights = alpha(c, d)
            for v in SITES:
                for e in COLORS:
                    a_uv = X[d][v][e]
                    a_rv = X[c][v][e]
                    for i in SITES:
                        if i == v:
                            continue
                        star = q_block(v, i)[e]
                        left = tuple(a_uv * X[c][i][a] + a_rv * X[d][i][a]
                                     for a in COLORS)
                        right = tuple((weights[i] + weights[v]) * star[a]
                                      for a in COLORS)
                        assert left == right
                        checks += 1
            assert -sum(weights, Q(0)) == -1
    return checks


def audit_planes_and_plucker_kernel():
    z01 = linear_product(X[0], X[1])
    z02 = linear_product(X[0], X[2])
    z12 = linear_product(X[1], X[2])
    z11 = linear_product(X[1], X[1])
    assert multiply(z01, z12) == multiply(z02, z11)

    # L_i=span{x_0i,x_1i} is zero on P_2, but z_02 is nonzero there.
    assert all(X[0][i] == X[1][i] == (Q(0), Q(0), Q(0)) for i in PLUS[2])
    assert any(product_block(X[0], X[2], i, j) != ZERO
               for i in PLUS[0] for j in PLUS[2])

    annihilator = add_elements(
        k_operator(alpha(0, 1), z12),
        k_operator(alpha(0, 2), z11),
        right_scale=Q(-1),
    )
    assert annihilator
    i, j = PLUS[1][0], PLUS[1][1]
    assert q_block(i, j) == ZERO
    assert annihilator[((i, 1), (j, 1))] == -4
    assert hessian(annihilator) == {}
    return len(annihilator)


def main():
    audit_responses_and_activity()
    transition_checks = audit_transition_law()
    annihilator_terms = audit_planes_and_plucker_kernel()
    print("Plücker-Hessian defect-three transition guard: PASS")
    print(f"transition vector checks={transition_checks}; "
          f"non-gauge annihilator cells={annihilator_terms}")


if __name__ == "__main__":
    main()
