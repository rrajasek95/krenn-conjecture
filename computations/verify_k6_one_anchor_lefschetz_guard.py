"""Exact lightweight check of the dense K6 one-anchor provenance guard."""

from fractions import Fraction
from functools import lru_cache
from itertools import permutations, product

from verify_k6_matching_lefschetz_inverse import (
    EDGES,
    determinant,
    disjointness_matrix,
)


N = 6
COLORS = range(3)
OMEGA = (1, 1, 0, 0, 0, 0)
ZERO_WORD = (0,) * N


def add(*vectors):
    return tuple(sum(entries, Fraction(0)) for entries in zip(*vectors))


def scale(scalar, vector):
    return tuple(scalar * entry for entry in vector)


def outer(left, right):
    return [
        [left[i] * right[j] for j in COLORS]
        for i in COLORS
    ]


def determinant3(matrix):
    return (
        matrix[0][0] * (
            matrix[1][1] * matrix[2][2]
            - matrix[1][2] * matrix[2][1]
        )
        - matrix[0][1] * (
            matrix[1][0] * matrix[2][2]
            - matrix[1][2] * matrix[2][0]
        )
        + matrix[0][2] * (
            matrix[1][0] * matrix[2][1]
            - matrix[1][1] * matrix[2][0]
        )
    )


def permanent3(matrix):
    return sum(
        matrix[0][perm[0]] * matrix[1][perm[1]] * matrix[2][perm[2]]
        for perm in permutations(COLORS)
    )


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matrix_multiply(left, right):
    return [
        [
            sum(left[i][k] * right[k][j] for k in COLORS)
            for j in COLORS
        ]
        for i in COLORS
    ]


def solve_transpose(matrix, target):
    """Solve matrix^T x=target by exact Cramer elimination."""
    work = [
        [matrix[col][row] for col in COLORS] + [target[row]]
        for row in COLORS
    ]
    for col in COLORS:
        pivot = next(row for row in range(col, 3) if work[row][col])
        work[col], work[pivot] = work[pivot], work[col]
        value = work[col][col]
        work[col] = [entry / value for entry in work[col]]
        for row in COLORS:
            if row == col:
                continue
            value = work[row][col]
            work[row] = [
                work[row][entry] - value * work[col][entry]
                for entry in range(4)
            ]
    return tuple(work[row][3] for row in COLORS)


def build_stars():
    eps = tuple(
        tuple(Fraction(int(i == j)) for i in COLORS)
        for j in COLORS
    )
    u = {
        0: eps[1],
        1: eps[2],
        2: scale(Fraction(1, 2), add(eps[0], scale(-1, eps[1]), scale(-1, eps[2]))),
    }
    v = {
        3: eps[1],
        4: eps[2],
        5: add(eps[0], scale(-1, eps[1]), scale(-1, eps[2])),
    }
    U = add(*(u[x] for x in range(3)))
    V = add(*(v[x] for x in range(3, 6)))
    B0 = add(U, scale(-1, u[0]))
    B1 = add(U, scale(-1, u[1]))

    p = {}
    s = {}
    for label in COLORS:
        for site in range(N):
            for color in COLORS:
                p[label, site, color] = Fraction(0)
                s[label, site, color] = Fraction(0)

    def add_component(star, site, color, vector):
        for label in COLORS:
            star[label, site, color] += vector[label]

    add_component(p, 0, 1, u[0])
    add_component(p, 0, 0, B0)
    add_component(s, 0, 0, scale(-1, V))
    add_component(p, 1, 1, u[1])
    add_component(p, 1, 0, scale(Fraction(-1, 3), B1))
    add_component(s, 1, 0, scale(Fraction(1, 3), V))
    add_component(p, 2, 0, u[2])
    for site in range(3, 6):
        add_component(s, site, 0, v[site])

    return p, s, u, v, U, V


@lru_cache(maxsize=None)
def hafnian(vertices, word):
    if not vertices:
        return Fraction(1)
    first = vertices[0]
    answer = Fraction(0)
    for position in range(1, len(vertices)):
        second = vertices[position]
        if word[first] != OMEGA[first] or word[second] != OMEGA[second]:
            continue
        rest = vertices[1:position] + vertices[position + 1:]
        answer += hafnian(rest, word)
    return answer


def verify_tensor(p, s, direct):
    vertices = tuple(range(N))
    checked = 0
    for word in product(COLORS, repeat=N):
        q3 = hafnian(vertices, word)
        for i in COLORS:
            for j in COLORS:
                response = Fraction(0)
                for x in vertices:
                    for y in vertices:
                        if x == y:
                            continue
                        complement = tuple(
                            z for z in vertices if z not in (x, y)
                        )
                        response += (
                            p[i, x, word[x]]
                            * s[j, y, word[y]]
                            * hafnian(complement, word)
                        )
                target = Fraction(int(i == 0 and j == 0 and word == ZERO_WORD))
                assert direct[i][j] * q3 + response == target
                checked += 1
    assert checked == 9 * 3**6


def main():
    p, s, u, v, U, V = build_stars()
    direct = [
        [Fraction(-1, 5) * entry for entry in row]
        for row in outer(U, V)
    ]
    verify_tensor(p, s, direct)

    selector_p = [list(u[x]) for x in range(3)]
    selector_s = [list(v[x]) for x in range(3, 6)]
    assert determinant3(selector_p) == Fraction(1, 2)
    assert determinant3(selector_s) == Fraction(1)
    assert all(s[i, x, OMEGA[x]] == 0 for i in COLORS for x in range(3))
    assert all(p[i, y, OMEGA[y]] == 0 for i in COLORS for y in range(3, 6))
    assert all(
        not all(OMEGA[y] == color for y in range(N) if y != x)
        for color in COLORS
        for x in range(N)
    )

    alpha = direct[1][0]
    trace = sum(direct[i][i] for i in COLORS)
    cap = [
        [
            trace * int(i == 1 and j == 0) - alpha * int(i == j)
            for j in COLORS
        ]
        for i in COLORS
    ]
    response = matrix_multiply(
        matrix_multiply(selector_p, cap),
        transpose(selector_s),
    )
    assert permanent3(response) == Fraction(7, 2000)

    assert solve_transpose(selector_p, (1, 0, 0)) == (1, 1, 2)
    assert solve_transpose(selector_s, (1, 0, 0)) == (1, 1, 1)

    incidence = disjointness_matrix()
    assert determinant(incidence) == -1458
    for x, y in EDGES:
        z, w = tuple(site for site in range(N) if site not in (x, y))[:2]
        cycle = {
            tuple(sorted((x, y))): 1,
            tuple(sorted((z, w))): 1,
            tuple(sorted((x, z))): -1,
            tuple(sorted((y, w))): -1,
        }
        for site in range(N):
            assert sum(
                cycle.get(edge, 0) for edge in EDGES if site in edge
            ) == 0
        assert cycle[tuple(sorted((x, y)))] == 1

    print("dense K6 one-anchor Lefschetz provenance guard: PASS")


if __name__ == "__main__":
    main()
