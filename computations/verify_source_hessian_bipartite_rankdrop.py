#!/usr/bin/env python3
"""Exact audit for the connected rank-three boundary lemma.

The proof in ``notes/source-hessian-bipartite-rankdrop.md`` is uniform.
This script checks two finite pieces which are useful for adversarial
auditing:

* the gauge-rigid / connected-bipartite-rank-three hypotheses occur on an
  exact rational four-site quadratic; and
* the bipartite antipodal normal form kills all six off-diagonal product
  systems and confines all nine pair responses to a two-dimensional span.

A rank lower bound modulo PRIME is also a rank lower bound over Q.  The
universal three-dimensional gauge kernel supplies the matching upper bound,
so the modular Hessian computation is an exact characteristic-zero
certificate of gauge rigidity for the displayed integer specialization.
"""

from __future__ import annotations

from itertools import combinations, product
from random import Random


PRIME = 1_000_003
N = 4
COLORS = range(3)
EDGES = tuple(combinations(range(N), 2))
LABELS = tuple((i, j, a, b) for i, j in EDGES for a, b in product(COLORS, repeat=2))
LABEL_INDEX = {label: index for index, label in enumerate(LABELS)}
WORDS = tuple(product(COLORS, repeat=N))
WORD_INDEX = {word: index for index, word in enumerate(WORDS)}
SHORE = (1, -1, 1, -1)


def det3(matrix):
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    ) % PRIME


def rank_mod(rows):
    values = [[entry % PRIME for entry in row] for row in rows]
    if not values:
        return 0
    rank = 0
    column_count = len(values[0])
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, len(values)) if values[row][column]),
            None,
        )
        if pivot is None:
            continue
        values[rank], values[pivot] = values[pivot], values[rank]
        inverse = pow(values[rank][column], PRIME - 2, PRIME)
        values[rank] = [entry * inverse % PRIME for entry in values[rank]]
        for row in range(len(values)):
            if row == rank or not values[row][column]:
                continue
            multiple = values[row][column]
            values[row] = [
                (entry - multiple * pivot_entry) % PRIME
                for entry, pivot_entry in zip(values[row], values[rank], strict=True)
            ]
        rank += 1
        if rank == len(values):
            break
    return rank


def matmul(left, right):
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right))) % PRIME
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def random_rank_three(rng):
    while True:
        matrix = [[rng.randrange(1, 23) for _ in COLORS] for _ in COLORS]
        if det3(matrix):
            return matrix


def random_rank_two(rng):
    while True:
        left = [[rng.randrange(1, 17) for _ in range(2)] for _ in COLORS]
        right = [[rng.randrange(1, 19) for _ in COLORS] for _ in range(2)]
        matrix = matmul(left, right)
        if det3(matrix):
            continue
        minors = [
            (matrix[i][j] * matrix[k][ell] - matrix[i][ell] * matrix[k][j]) % PRIME
            for i, k in combinations(COLORS, 2)
            for j, ell in combinations(COLORS, 2)
        ]
        if any(minors):
            return matrix


def candidate_q(rng):
    q = {}
    for edge in EDGES:
        same_shore = SHORE[edge[0]] == SHORE[edge[1]]
        q[edge] = random_rank_two(rng) if same_shore else random_rank_three(rng)
    return q


def qentry(q, i, a, j, b):
    if i < j:
        return q[i, j][a][b]
    return q[j, i][b][a]


def hessian_columns(q):
    """Columns of H_q: Z -> Zq on four sites."""
    columns = []
    for i, j, a, b in LABELS:
        remaining = tuple(vertex for vertex in range(N) if vertex not in (i, j))
        k, ell = remaining
        column = [0] * len(WORDS)
        for c, d in product(COLORS, repeat=2):
            word = [None] * N
            word[i], word[j], word[k], word[ell] = a, b, c, d
            column[WORD_INDEX[tuple(word)]] = qentry(q, k, c, ell, d)
        columns.append(column)
    return columns


def apply_hessian(columns, quadratic):
    output = [0] * len(WORDS)
    for coefficient, column in zip(quadratic, columns, strict=True):
        if not coefficient:
            continue
        for row, entry in enumerate(column):
            output[row] = (output[row] + coefficient * entry) % PRIME
    return output


def q_vector(q):
    return [q[i, j][a][b] % PRIME for i, j, a, b in LABELS]


def gauge_vectors(q):
    vectors = []
    for distinguished in range(N - 1):
        alpha = [0] * N
        alpha[distinguished] = 1
        alpha[-1] = -1
        vector = [0] * len(LABELS)
        for i, j in EDGES:
            scalar = (alpha[i] + alpha[j]) % PRIME
            for a, b in product(COLORS, repeat=2):
                vector[LABEL_INDEX[i, j, a, b]] = scalar * q[i, j][a][b] % PRIME
        vectors.append(vector)
    return vectors


def outer(left, right):
    return [[x * y % PRIME for y in right] for x in left]


def add_matrices(left, right):
    return [
        [(left[i][j] + right[i][j]) % PRIME for j in COLORS]
        for i in COLORS
    ]


def product_quadratic(left, right):
    """Square-free product of two site-linear vector families."""
    vector = [0] * len(LABELS)
    for i, j in EDGES:
        block = add_matrices(outer(left[i], right[j]), outer(right[i], left[j]))
        for a, b in product(COLORS, repeat=2):
            vector[LABEL_INDEX[i, j, a, b]] = block[a][b]
    return vector


def scale_site_family(family, scalar):
    return [
        [scalar * coordinate % PRIME for coordinate in local]
        for local in family
    ]


def add_vectors(left, right, left_scale=1, right_scale=1):
    return [
        (left_scale * x + right_scale * y) % PRIME
        for x, y in zip(left, right, strict=True)
    ]


def find_gauge_rigid_specialization():
    rng = Random(20260724)
    domain_dimension = len(LABELS)
    expected_rank = domain_dimension - (N - 1)
    for trial in range(1, 101):
        q = candidate_q(rng)
        columns = hessian_columns(q)
        # rank_mod receives row vectors.  Transposing the column list is not
        # needed: row rank of this 54 by 81 array is the column rank of H_q.
        if rank_mod(columns) == expected_rank:
            assert all(
                bool(det3(q[edge])) == (SHORE[edge[0]] != SHORE[edge[1]])
                for edge in EDGES
            )
            gauges = gauge_vectors(q)
            assert rank_mod(gauges) == N - 1
            assert all(not any(apply_hessian(columns, gauge)) for gauge in gauges)
            return trial, q, columns
    raise AssertionError("no gauge-rigid bipartite-rank-three specialization found")


def audit_antipodal_response(q, columns):
    z = (
        (1, 2, 3),
        (2, 5, 7),
        (3, 7, 11),
        (5, 11, 13),
    )
    t = (2, 3, 5)
    u = (7, 11, 13)
    p = [scale_site_family(z, scalar) for scalar in t]
    signed_z = [
        [SHORE[i] * coordinate % PRIME for coordinate in z[i]]
        for i in range(N)
    ]
    s = [scale_site_family(signed_z, scalar) for scalar in u]

    # All six local rows are nonzero at every site.
    assert all(any(local) for family in p + s for local in family)

    rank_three_edges = [
        edge for edge in EDGES if SHORE[edge[0]] != SHORE[edge[1]]
    ]
    for c, d in product(COLORS, repeat=2):
        star_product = product_quadratic(p[c], s[d])
        if c != d:
            for i, j in rank_three_edges:
                block = [
                    star_product[LABEL_INDEX[i, j, a, b]]
                    for a, b in product(COLORS, repeat=2)
                ]
                assert not any(block)

    common_product = product_quadratic(z, signed_z)
    common_response = apply_hessian(columns, common_product)
    star_responses = []
    for c, d in product(COLORS, repeat=2):
        response = apply_hessian(columns, product_quadratic(p[c], s[d]))
        expected = [t[c] * u[d] * entry % PRIME for entry in common_response]
        assert response == expected
        star_responses.append(response)
    assert rank_mod(star_responses) == 1

    # Q=q^2/2 and one arbitrary direct 3 by 3 block add only one further
    # output direction to the nine responses.
    q_squared = apply_hessian(columns, q_vector(q))
    inverse_two = pow(2, PRIME - 2, PRIME)
    matching_power = [inverse_two * entry % PRIME for entry in q_squared]
    direct = (
        (1, 4, 7),
        (2, 5, 8),
        (3, 6, 10),
    )
    responses = []
    for c, d in product(COLORS, repeat=2):
        responses.append(
            add_vectors(
                matching_power,
                common_response,
                left_scale=direct[c][d],
                right_scale=t[c] * u[d],
            )
        )
    assert rank_mod([matching_power, common_response]) == 2
    assert rank_mod(responses) == 2

    targets = []
    for c in COLORS:
        vector = [0] * len(WORDS)
        vector[WORD_INDEX[(c,) * N]] = 1
        targets.append(vector)
    assert rank_mod(targets) == 3


def main():
    trial, q, columns = find_gauge_rigid_specialization()
    audit_antipodal_response(q, columns)
    print(
        "verified: four-site integer q, trial="
        f"{trial}, Hessian rank=51/54, kernel=gauge dimension 3"
    )
    print("verified: rank-three graph K_2,2; same-shore blocks have rank 2")
    print("verified: six off-diagonal zero-block systems; response ranks 1+1=2<3")


if __name__ == "__main__":
    main()
