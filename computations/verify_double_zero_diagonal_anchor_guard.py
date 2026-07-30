#!/usr/bin/env python3
"""Exact, dependency-free audit of the diagonal-only double-zero guard."""

from fractions import Fraction
from itertools import product


if not __debug__:
    raise RuntimeError("run this exact checker without Python -O")


P, Q, R, A, B, C, D, E = range(8)
SITES = tuple(range(8))
COLORS = tuple(range(3))
COMMON = (A, B, C, D, E)


def zero_block():
    return [[0 for _ in COLORS] for _ in COLORS]


def build_blocks():
    blocks = {}

    def add(left, right, left_color, right_color, value=1):
        if left > right:
            left, right = right, left
            left_color, right_color = right_color, left_color
        block = blocks.setdefault((left, right), zero_block())
        block[left_color][right_color] += value

    for left, right in ((P, A), (Q, B), (R, C), (D, E)):
        add(left, right, 0, 0)
    for left, right in ((P, Q), (P, R)):
        add(left, right, 1, 2)
        add(left, right, 2, 1)
    add(Q, R, 1, 1)
    add(Q, R, 2, 2)
    for left, right in ((P, E), (A, B), (C, D)):
        add(left, right, 1, 1)
    for left, right in ((P, D), (A, C), (B, E)):
        add(left, right, 2, 2)
    return blocks


BLOCKS = build_blocks()


def entry(left, right, left_color, right_color):
    if left < right:
        block = BLOCKS.get((left, right))
        return 0 if block is None else block[left_color][right_color]
    block = BLOCKS.get((right, left))
    return 0 if block is None else block[right_color][left_color]


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def matching_tensor(vertices):
    vertices = tuple(vertices)
    tensor = {}
    for matching in perfect_matchings(vertices):
        choices = []
        for left, right in matching:
            decorated = [
                (left_color, right_color, entry(left, right, left_color, right_color))
                for left_color in COLORS
                for right_color in COLORS
                if entry(left, right, left_color, right_color)
            ]
            if not decorated:
                break
            choices.append((left, right, decorated))
        else:
            for selected in product(*(decorated for _, _, decorated in choices)):
                word = {}
                coefficient = 1
                for (left, right, _), (left_color, right_color, value) in zip(
                    choices, selected
                ):
                    word[left] = left_color
                    word[right] = right_color
                    coefficient *= value
                key = tuple(word[site] for site in vertices)
                tensor[key] = tensor.get(key, 0) + coefficient
    return {word: coefficient for word, coefficient in tensor.items() if coefficient}


def matrix_rank(rows):
    matrix = [[Fraction(value) for value in row] for row in rows]
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def channel(endpoint, deleted, pure_color=0):
    residual = [site for site in SITES if site not in (endpoint, deleted)]
    return {
        endpoint_color
        for endpoint_color in COLORS
        if any(
            entry(endpoint, site, endpoint_color, pure_color)
            for site in residual
        )
    }


def star_rank(endpoint, deleted):
    residual = [site for site in SITES if site not in (endpoint, deleted)]
    rows = [
        [
            entry(endpoint, site, endpoint_color, residual_color)
            for site in residual
            for residual_color in COLORS
        ]
        for endpoint_color in COLORS
    ]
    return matrix_rank(rows)


def pure_hafnian(vertices, color=0):
    total = 0
    for matching in perfect_matchings(vertices):
        term = 1
        for left, right in matching:
            term *= entry(left, right, color, color)
        total += term
    return total


def pure_star_cohafnian(endpoint, endpoint_color):
    total = 0
    for occupied in COMMON:
        residual = [site for site in COMMON if site != occupied]
        total += entry(endpoint, occupied, endpoint_color, 0) * pure_hafnian(residual)
    return total


def gamma(i, j, k):
    total = 0
    for p_site in COMMON:
        for q_site in COMMON:
            if q_site == p_site:
                continue
            for r_site in COMMON:
                if r_site in (p_site, q_site):
                    continue
                residual = [
                    site for site in COMMON if site not in (p_site, q_site, r_site)
                ]
                total += (
                    entry(P, p_site, i, 0)
                    * entry(Q, q_site, j, 0)
                    * entry(R, r_site, k, 0)
                    * entry(residual[0], residual[1], 0, 0)
                )
    return total


def fixed_site_times_internal(fixed_site, fixed_color):
    residual = [site for site in COMMON if site != fixed_site]
    tensor = matching_tensor(residual)
    output = {}
    for word, coefficient in tensor.items():
        decorated = {site: color for site, color in zip(residual, word)}
        decorated[fixed_site] = fixed_color
        key = tuple(decorated[site] for site in COMMON)
        output[key] = output.get(key, 0) + coefficient
    return output


def main():
    expected_words = {
        tuple(map(int, word)): 1
        for word in (
            "00000000",
            "11111111",
            "22222222",
            "01102112",
            "02202112",
            "10220200",
            "12011000",
            "12211111",
            "20120200",
            "21011000",
            "21122222",
        )
    }
    tensor = matching_tensor(SITES)
    assert tensor == expected_words

    for left, right in ((P, Q), (P, R)):
        for color in COLORS:
            fiber = {
                word: coefficient
                for word, coefficient in tensor.items()
                if word[left] == word[right] == color
            }
            assert fiber == {(color,) * 8: 1}
        for i in COLORS:
            for j in COLORS:
                if i != j:
                    assert any(word[left] == i and word[right] == j for word in tensor)

    pq_residual = (R, A, B, C, D, E)
    pr_residual = (Q, A, B, C, D, E)
    assert matching_tensor(pq_residual) == {(0, 1, 1, 0, 0, 0): 1}
    assert matching_tensor(pr_residual) == {(0, 2, 0, 2, 0, 0): 1}
    assert pure_hafnian(pq_residual) == pure_hafnian(pr_residual) == 0

    for endpoint, deleted in ((P, Q), (Q, P), (P, R), (R, P)):
        assert channel(endpoint, deleted) == {0}
        assert star_rank(endpoint, deleted) == 3

    lower_pq = [[entry(P, Q, i, j) for j in (1, 2)] for i in (1, 2)]
    lower_pr = [[entry(P, R, i, j) for j in (1, 2)] for i in (1, 2)]
    assert lower_pq == lower_pr == [[0, 1], [1, 0]]

    for i in COLORS:
        for j in COLORS:
            for k in COLORS:
                assert gamma(i, j, k) == int(i == j == k == 0)

    # tau, upsilon, chi in the note all vanish, while T=A_qr is nonzero.
    assert all(pure_star_cohafnian(endpoint, color) == 0 for endpoint in (P, Q, R) for color in COLORS)
    assert entry(Q, R, 1, 1) == entry(Q, R, 2, 2) == 1

    direct_a = entry(P, Q, 1, 2)
    direct_b = entry(P, R, 1, 0)
    direct_f = entry(Q, C, 2, 0)
    direct_u = entry(R, C, 0, 0)
    assert direct_a * direct_u - direct_b * direct_f == 1

    # The two diagonal targets are normal rows; their odd-residue classes
    # vanish because they are already a linear form times z^[2].
    assert fixed_site_times_internal(E, 1) == {(1, 1, 1, 1, 1): 1}
    assert fixed_site_times_internal(D, 2) == {(2, 2, 2, 2, 2): 1}
    assert entry(P, Q, 1, 1) == entry(P, Q, 2, 2) == 0
    assert entry(P, R, 1, 1) == entry(P, R, 2, 2) == 0
    for endpoint in (Q, R):
        for endpoint_color in (1, 2):
            assert all(
                entry(endpoint, site, endpoint_color, site_color) == 0
                for site in COMMON
                for site_color in COLORS
            )

    print("double-zero diagonal-anchor guard: PASS")


if __name__ == "__main__":
    main()
