#!/usr/bin/env python3
"""Exact local compatibility model for the balanced union-five row.

The witness masks are ``(1,3,5,6,6)`` after deleting the empty site.  The
three colors have hard triples 012, 134, and 234.  This script constructs
one common rational family of the fifteen internal edge matrices on these
five sites and the unique nonwitness site ``k``.  Its scalar common-
annihilator graph has every four-site hafnian zero, while its actual edge
row contractions give all three pure triangle responses.

This is deliberately only a model of the simultaneous two- and three-hole
consequences.  It does not satisfy, or claim to satisfy, the uncontracted
five-hole GHZ identity.
"""

from fractions import Fraction as Q
from itertools import combinations, product


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


COLORS = tuple(range(3))
WITNESSES = tuple(range(5))
K = 5
SITES = WITNESSES + (K,)
P = 6
QV = 7
ALL_SITES = SITES + (P, QV)
E = tuple(
    tuple(Q(int(i == j)) for i in COLORS)
    for j in COLORS
)
ZERO = (Q(0), Q(0), Q(0))


def add(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def scale(scalar, vector):
    return tuple(scalar * value for value in vector)


def dot(left, right):
    return sum(a * b for a, b in zip(left, right, strict=True))


def cross(left, right):
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def outer(left, right):
    return tuple(
        tuple(a * b for b in right)
        for a in left
    )


def matrix_add(*matrices):
    return tuple(
        tuple(sum(matrix[i][j] for matrix in matrices) for j in COLORS)
        for i in COLORS
    )


def matrix_scale(scalar, matrix):
    return tuple(tuple(scalar * value for value in row) for row in matrix)


def matrix_product(left, right):
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in COLORS) for j in COLORS)
        for i in COLORS
    )


def transpose(matrix):
    return tuple(tuple(matrix[j][i] for j in COLORS) for i in COLORS)


def matvec(matrix, vector):
    return tuple(
        sum(matrix[i][j] * vector[j] for j in COLORS)
        for i in COLORS
    )


def transpose_matvec(matrix, vector):
    return tuple(
        sum(matrix[i][j] * vector[i] for i in COLORS)
        for j in COLORS
    )


# Star rows at one incidence-field point.  Their cross-product zero masks
# are 1,3,5,6,6,0 respectively.
X = (
    E[0],
    E[0],
    E[2],
    E[1],
    E[2],
    (Q(1), Q(1), Q(1)),
)
Y = (
    add(E[1], E[2]),
    E[1],
    E[0],
    E[2],
    E[1],
    (Q(1), Q(2), Q(3)),
)

# Convenient generators of the common annihilator lines.  At site 4 this
# is the negative of X[4] cross Y[4], which of course spans the same line.
N = (
    (Q(0), Q(-1), Q(1)),
    E[2],
    E[1],
    E[0],
    E[0],
    (Q(1), Q(-2), Q(1)),
)

# Chosen dual vectors, N[i] dot DUAL[i] = 1.
DUAL = (
    E[2],
    E[2],
    E[1],
    E[0],
    E[0],
    E[0],
)


# L[(i,j)] is the vector at j obtained by contracting the i endpoint of
# A_ij by N[i].  Start with the pure k-star scalar graph: all witness-
# witness scalar contractions are zero and every ik scalar is one.
L = {(i, j): ZERO for i in SITES for j in SITES if i != j}
SCALAR = {}
for i, j in combinations(SITES, 2):
    SCALAR[i, j] = Q(1) if j == K else Q(0)
for i in WITNESSES:
    L[i, K] = DUAL[K]
    L[K, i] = DUAL[i]


# The directed witness-edge rows below simultaneously realize the three
# triangle normal forms.  Unlisted directed rows remain zero.
half = Q(1, 2)
L[3, 0] = scale(half, E[0])
L[3, 1] = scale(half, E[0])
L[3, 2] = scale(-half, E[2])

L[0, 1] = scale(half, E[1])
L[0, 3] = scale(-half, E[2])
L[0, 4] = scale(half, E[1])

L[0, 2] = scale(half, E[2])
L[1, 3] = scale(half, add(E[2], scale(Q(-1), E[1])))
L[1, 4] = scale(half, add(E[2], scale(Q(-1), E[1])))


def realizing_matrix(i, j):
    """Realize both directed rows when their scalar pairings agree.

    For ``a=N[j].L[i,j]=N[i].L[j,i]`` and duals ``u_i,u_j``, the formula

        u_i L_ij^T + L_ji u_j^T - a u_i u_j^T

    has exactly the two requested endpoint contractions.
    """

    a = SCALAR[i, j]
    require(
        dot(N[j], L[i, j]) == a,
        "dot(N[j], L[i, j]) == a",
    )
    require(
        dot(N[i], L[j, i]) == a,
        "dot(N[i], L[j, i]) == a",
    )
    return matrix_add(
        outer(DUAL[i], L[i, j]),
        outer(L[j, i], DUAL[j]),
        matrix_scale(-a, outer(DUAL[i], DUAL[j])),
    )


A = {(i, j): realizing_matrix(i, j) for i, j in combinations(SITES, 2)}

# Complete the local data to one honest eight-site edge family.  The rank-one
# p- and q-stars have precisely the declared cross-matrix zero masks, and the
# selected rows alpha,beta produce X,Y.  This completion is used only to
# audit the stated contractions; its uncontracted matching tensor is not GHZ.
ALPHA = (Q(1), Q(1), Q(1))
BETA = (Q(1), Q(1, 2), Q(1))
APQ = (
    (Q(1), Q(0), Q(0)),
    (Q(0), Q(2), Q(0)),
    (Q(0), Q(0), Q(-2)),
)
PSTAR = tuple(outer(E[0], X[i]) for i in SITES)
QSTAR = tuple(outer(E[0], Y[i]) for i in SITES)
K_CROSS = (
    ((Q(0), Q(0), Q(0)), (Q(0), Q(0), Q(1)), (Q(0), Q(-1), Q(0))),
    ((Q(0), Q(0), Q(-1)), (Q(0), Q(0), Q(0)), (Q(1), Q(0), Q(0))),
    ((Q(0), Q(1), Q(0)), (Q(-1), Q(0), Q(0)), (Q(0), Q(0), Q(0))),
)
ZERO_MATRIX = ((Q(0), Q(0), Q(0)),) * 3


def edge_matrix(i, j):
    if i == P and j == QV:
        return APQ
    if i == QV and j == P:
        return transpose(APQ)
    if i == P and j in SITES:
        return PSTAR[j]
    if j == P and i in SITES:
        return transpose(PSTAR[i])
    if i == QV and j in SITES:
        return QSTAR[j]
    if j == QV and i in SITES:
        return transpose(QSTAR[i])
    if i < j:
        return A[i, j]
    return transpose(A[j, i])


def directed_row(i, j):
    return transpose_matvec(edge_matrix(i, j), N[i])


def scalar_edge(i, j):
    return dot(N[j], directed_row(i, j))


def hafnian4(vertices):
    a, b, c, d = vertices
    return (
        scalar_edge(a, b) * scalar_edge(c, d)
        + scalar_edge(a, c) * scalar_edge(b, d)
        + scalar_edge(a, d) * scalar_edge(b, c)
    )


def residual_vector(hole, contracted):
    """The actual residual vector in the three-hole response."""

    answer = ZERO
    for mate in contracted:
        other = tuple(site for site in contracted if site != mate)
        coefficient = scalar_edge(*other)
        answer = add(answer, scale(coefficient, directed_row(mate, hole)))
    return answer


def pair_response(i, j):
    return tuple(
        tuple(
            X[i][a] * Y[j][b] + Y[i][a] * X[j][b]
            for b in COLORS
        )
        for a in COLORS
    )


def triangle_response(holes, residuals):
    answer = {word: Q(0) for word in product(COLORS, repeat=3)}
    for omitted in range(3):
        pair = tuple(index for index in range(3) if index != omitted)
        matrix = pair_response(holes[pair[0]], holes[pair[1]])
        vector = residuals[holes[omitted]]
        for word in answer:
            answer[word] += (
                matrix[word[pair[0]]][word[pair[1]]]
                * vector[word[omitted]]
            )
    return answer


def pure_triangle(color):
    return {
        word: Q(int(word == (color, color, color)))
        for word in product(COLORS, repeat=3)
    }


def witness_mask(i):
    gamma = cross(X[i], Y[i])
    return sum(1 << color for color, value in enumerate(gamma) if value == 0)


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


MATCHINGS = tuple(perfect_matchings(ALL_SITES))


def direct_contracted_value(holes, word):
    coloring = dict(zip(holes, word, strict=True))
    capped = {P: ALPHA, QV: BETA}
    capped.update({site: N[site] for site in SITES if site not in holes})
    answer = Q(0)
    for matching in MATCHINGS:
        value = Q(1)
        for i, j in matching:
            matrix = edge_matrix(i, j)
            if i in capped and j in capped:
                value *= sum(
                    capped[i][a] * matrix[a][b] * capped[j][b]
                    for a in COLORS for b in COLORS
                )
            elif i in capped:
                value *= sum(
                    capped[i][a] * matrix[a][coloring[j]]
                    for a in COLORS
                )
            elif j in capped:
                value *= sum(
                    matrix[coloring[i]][b] * capped[j][b]
                    for b in COLORS
                )
            else:
                value *= matrix[coloring[i]][coloring[j]]
        answer += value
    return answer


def target_contracted_value(holes, word):
    if len(set(word)) != 1:
        return Q(0)
    color = word[0]
    return (
        ALPHA[color] * BETA[color]
        * product_value(
            N[site][color] for site in SITES if site not in holes
        )
    )


def product_value(values):
    answer = Q(1)
    for value in values:
        answer *= value
    return answer


def main():
    require(
        tuple(witness_mask(i) for i in SITES) == (1, 3, 5, 6, 6, 0),
        "tuple(witness_mask(i) for i in SITES) == (1, 3, 5, 6, 6, 0)",
    )
    for i in SITES:
        require(
            dot(N[i], X[i]) == dot(N[i], Y[i]) == 0,
            "dot(N[i], X[i]) == dot(N[i], Y[i]) == 0",
        )
        require(
            dot(N[i], DUAL[i]) == 1,
            "dot(N[i], DUAL[i]) == 1",
        )
        require(
            transpose_matvec(PSTAR[i], ALPHA) == X[i],
            "transpose_matvec(PSTAR[i], ALPHA) == X[i]",
        )
        require(
            transpose_matvec(QSTAR[i], BETA) == Y[i],
            "transpose_matvec(QSTAR[i], BETA) == Y[i]",
        )
        cross_zeros = tuple(
            matrix_product(
                matrix_product(PSTAR[i], K_CROSS[color]),
                transpose(QSTAR[i]),
            ) == ZERO_MATRIX
            for color in COLORS
        )
        require(
            sum(
                1 << color for color in COLORS if cross_zeros[color]
            ) == (1, 3, 5, 6, 6, 0)[i],
            "sum( 1 << color for color in COLORS if cross_zeros[color]...",
        )
    require(
        APQ[0][0] * APQ[1][1] * APQ[2][2] != 0,
        "APQ[0][0] * APQ[1][1] * APQ[2][2] != 0",
    )
    require(
        sum(
            ALPHA[a] * APQ[a][b] * BETA[b]
            for a in COLORS for b in COLORS
        ) == 0,
        "sum( ALPHA[a] * APQ[a][b] * BETA[b] for a in COLORS for b...",
    )

    # Audit the actual matrices against every declared directed row and
    # scalar contraction.
    for i, j in combinations(SITES, 2):
        require(
            directed_row(i, j) == L[i, j],
            "directed_row(i, j) == L[i, j]",
        )
        require(
            directed_row(j, i) == L[j, i],
            "directed_row(j, i) == L[j, i]",
        )
        require(
            scalar_edge(i, j) == SCALAR[i, j],
            "scalar_edge(i, j) == SCALAR[i, j]",
        )

    # The scalar graph is a pure star centered at k, hence every one of its
    # fifteen complementary four-site hafnians vanishes.
    for vertices in combinations(SITES, 4):
        require(
            hafnian4(vertices) == 0,
            "hafnian4(vertices) == 0",
        )

    # These are the actual fifteen zero two-hole contractions of the one
    # common eight-site edge family, not separately chosen scalar models.
    for holes in combinations(SITES, 2):
        for word in product(COLORS, repeat=2):
            require(
                direct_contracted_value(holes, word) == 0,
                "direct_contracted_value(holes, word) == 0",
            )
            require(
                target_contracted_value(holes, word) == 0,
                "target_contracted_value(holes, word) == 0",
            )

    cases = (
        ((0, 1, 2), (3, 4, K), 0),
        ((1, 3, 4), (0, 2, K), 1),
        ((2, 3, 4), (0, 1, K), 2),
    )
    for holes, contracted, color in cases:
        residuals = {
            hole: residual_vector(hole, contracted)
            for hole in holes
        }
        require(
            triangle_response(holes, residuals) == pure_triangle(color),
            "triangle_response(holes, residuals) == pure_triangle(color)",
        )
        for word in product(COLORS, repeat=3):
            expected = Q(int(word == (color, color, color)))
            require(
                target_contracted_value(holes, word) == expected,
                "target_contracted_value(holes, word) == expected",
            )
            require(
                direct_contracted_value(holes, word) == expected,
                "direct_contracted_value(holes, word) == expected",
            )

    expected_residuals = (
        {
            0: scale(half, E[0]),
            1: scale(half, E[0]),
            2: scale(-half, E[2]),
        },
        {
            1: scale(half, E[1]),
            3: scale(-half, E[2]),
            4: scale(half, E[1]),
        },
        {
            2: scale(half, E[2]),
            3: scale(-half, E[1]),
            4: scale(half, E[2]),
        },
    )
    for (holes, contracted, _), expected in zip(
        cases, expected_residuals, strict=True
    ):
        require(
            {
                hole: residual_vector(hole, contracted)
                for hole in holes
            } == expected,
            "{ hole: residual_vector(hole, contracted) for hole in hol...",
        )

    # Exhibit an off-diagonal coefficient left by the uncontracted row, so
    # the precise scope of this countermodel is also machine checked.
    off_diagonal = (0, 0, 1, 0, 1, 0)
    require(
        direct_contracted_value(SITES, off_diagonal) == 1,
        "direct_contracted_value(SITES, off_diagonal) == 1",
    )
    require(
        target_contracted_value(SITES, off_diagonal) == 0,
        "target_contracted_value(SITES, off_diagonal) == 0",
    )

    print("balanced masks 1,3,5,6,6 and all 15 zero two-hole rows: exact PASS")
    print("three overlapping shared-edge triangle responses: exact PASS")
    print("scope: local two-/three-hole model, not the full five-hole identity")


if __name__ == "__main__":
    main()
