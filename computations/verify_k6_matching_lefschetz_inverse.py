"""Exact check of the K6 matching-algebra middle-Lefschetz inverse."""

from fractions import Fraction
from itertools import combinations


EDGES = tuple(combinations(range(6), 2))
VERTICES = tuple(range(6))


def disjointness_matrix():
    """Rows are complements of four-sets; columns are edges."""
    return [
        [Fraction(int(set(row).isdisjoint(col))) for col in EDGES]
        for row in EDGES
    ]


def inverse_candidate():
    def entry(left, right):
        overlap = len(set(left) & set(right))
        if overlap == 2:
            return Fraction(1, 2)
        if overlap == 1:
            return Fraction(-1, 6)
        return Fraction(1, 6)

    return [[entry(row, col) for col in EDGES] for row in EDGES]


def multiply(left, right):
    size = len(left)
    return [
        [sum(left[i][k] * right[k][j] for k in range(size))
         for j in range(size)]
        for i in range(size)
    ]


def diagonal_left(diagonal, matrix):
    return [
        [diagonal[row] * value for value in matrix[row]]
        for row in range(len(matrix))
    ]


def diagonal_right(matrix, diagonal):
    return [
        [value * diagonal[col] for col, value in enumerate(row)]
        for row in matrix
    ]


def determinant(matrix):
    work = [row[:] for row in matrix]
    value = Fraction(1)
    size = len(work)

    for col in range(size):
        pivot = next(row for row in range(col, size) if work[row][col])
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            value = -value

        pivot_value = work[col][col]
        value *= pivot_value
        for entry in range(col, size):
            work[col][entry] /= pivot_value

        for row in range(col + 1, size):
            scale = work[row][col]
            if not scale:
                continue
            for entry in range(col, size):
                work[row][entry] -= scale * work[col][entry]

    return value


def main():
    matrix = disjointness_matrix()
    candidate = inverse_candidate()
    identity = [
        [Fraction(int(i == j)) for j in range(len(EDGES))]
        for i in range(len(EDGES))
    ]

    assert multiply(matrix, candidate) == identity
    assert multiply(candidate, matrix) == identity
    assert determinant(matrix) == -1458

    # Index a four-set by its complementary edge.  At a vertex-factor
    # point q_xy=t_x*t_y, the weighted multiplication map is
    # diag(t_V) * matrix * diag(1/t_e).
    weights = tuple(map(Fraction, (2, 3, 5, 7, 11, 13)))
    total_weight = Fraction(1)
    for value in weights:
        total_weight *= value
    edge_weight = [weights[x] * weights[y] for x, y in EDGES]
    four_set_weight = [total_weight / value for value in edge_weight]

    weighted = diagonal_right(
        diagonal_left(four_set_weight, matrix),
        [1 / value for value in edge_weight],
    )
    weighted_inverse = diagonal_right(
        diagonal_left(edge_weight, candidate),
        [1 / value for value in four_set_weight],
    )
    assert multiply(weighted, weighted_inverse) == identity
    assert multiply(weighted_inverse, weighted) == identity

    # The same point has physical probe differential
    # dQ_xy=t_x*t_y*(eta_x+eta_y).  For every requested own edge, a
    # weighted four-cycle covector annihilates this image but not that edge.
    for edge_index, (x, y) in enumerate(EDGES):
        z, w = tuple(v for v in VERTICES if v not in (x, y))[:2]
        signs = {
            tuple(sorted((x, y))): Fraction(1),
            tuple(sorted((z, w))): Fraction(1),
            tuple(sorted((x, z))): Fraction(-1),
            tuple(sorted((y, w))): Fraction(-1),
        }
        sign_vector = [signs.get(edge, Fraction(0)) for edge in EDGES]

        # Four-cycles lie in the eigenvalue-one summand of the Kneser
        # disjointness matrix, so the inverse does not spread their support.
        assert [
            sum(matrix[row][col] * sign_vector[col]
                for col in range(len(EDGES)))
            for row in range(len(EDGES))
        ] == sign_vector

        cycle = {
            edge: sign / edge_weight[EDGES.index(edge)]
            for edge, sign in signs.items()
        }
        for vertex in VERTICES:
            pairing = sum(
                cycle.get(edge, Fraction(0)) * edge_weight[index]
                for index, edge in enumerate(EDGES)
                if vertex in edge
            )
            assert pairing == 0
        assert cycle[tuple(sorted((x, y)))] != 0
        assert edge_index == EDGES.index(tuple(sorted((x, y))))

        # lambda*T_q^{-1}=c*diag(1/t_V): the inverse transports the
        # weighted edge obstruction to the same four complementary cuts.
        transported = [
            sum(
                cycle.get(edge, Fraction(0))
                * weighted_inverse[index][column]
                for index, edge in enumerate(EDGES)
            )
            for column in range(len(EDGES))
        ]
        expected = [
            sign_vector[column] / four_set_weight[column]
            for column in range(len(EDGES))
        ]
        assert transported == expected

        # The same covector is the normalized derivative of the
        # four-site curvature q_xy*q_zw-q_xz*q_yw.
        beta = [Fraction(index + 1) for index in range(len(EDGES))]
        four_vertex_weight = weights[x] * weights[y] * weights[z] * weights[w]
        curvature_derivative = sum(
            sign * four_vertex_weight / edge_weight[EDGES.index(edge)]
            * beta[EDGES.index(edge)]
            for edge, sign in signs.items()
        )
        cycle_pairing = sum(
            cycle.get(edge, Fraction(0)) * beta[index]
            for index, edge in enumerate(EDGES)
        )
        assert curvature_derivative == four_vertex_weight * cycle_pairing

    print("K6 matching Lefschetz inverse and provenance guard: PASS")


if __name__ == "__main__":
    main()
