#!/usr/bin/env python3
"""Dependency-free exact check of the eight-site double-zero Gamma guard."""

from fractions import Fraction
from itertools import product


P_SITE, Q_SITE, R_SITE, S_SITE, A0, B0, C0, D0 = range(8)
SITES = tuple(range(8))
COLORS = range(3)


def zero_block():
    return [[0 for _ in COLORS] for _ in COLORS]


def e00():
    block = zero_block()
    block[0][0] = 1
    return block


def lower_identity():
    block = zero_block()
    block[1][1] = block[2][2] = 1
    return block


def lower_swap():
    block = zero_block()
    block[1][2] = block[2][1] = 1
    return block


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for pos in range(1, len(vertices)):
        second = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def rank(rows):
    matrix = [[Fraction(value) for value in row] for row in rows]
    if not matrix:
        return 0
    row_count, col_count = len(matrix), len(matrix[0])
    pivot_row = 0
    for col in range(col_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if matrix[row][col]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][col]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][col]:
                continue
            scale = matrix[row][col]
            matrix[row] = [
                left - scale * right
                for left, right in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def build_blocks(p_block):
    blocks = {
        (P_SITE, A0): e00(),
        (Q_SITE, B0): e00(),
        (R_SITE, S_SITE): e00(),
        (C0, D0): e00(),
        (P_SITE, Q_SITE): p_block,
        (P_SITE, R_SITE): lower_identity(),
        (Q_SITE, R_SITE): lower_identity(),
    }
    return blocks


def entry(blocks, left, right, left_color, right_color):
    if left < right:
        block = blocks.get((left, right))
        return 0 if block is None else block[left_color][right_color]
    block = blocks.get((right, left))
    return 0 if block is None else block[right_color][left_color]


def full_tensor(blocks):
    tensor = {}
    for matching in perfect_matchings(SITES):
        choices = []
        for left, right in matching:
            terms = [
                (left_color, right_color, entry(blocks, left, right, left_color, right_color))
                for left_color in COLORS
                for right_color in COLORS
                if entry(blocks, left, right, left_color, right_color)
            ]
            if not terms:
                break
            choices.append((left, right, terms))
        else:
            for selected in product(*(terms for _, _, terms in choices)):
                word = [None] * len(SITES)
                coefficient = 1
                for (left, right, _), (left_color, right_color, value) in zip(
                    choices, selected
                ):
                    word[left], word[right] = left_color, right_color
                    coefficient *= value
                key = tuple(word)
                tensor[key] = tensor.get(key, 0) + coefficient
    return {word: value for word, value in tensor.items() if value}


def pure_hafnian(blocks, residual, color=0):
    total = 0
    for matching in perfect_matchings(residual):
        term = 1
        for left, right in matching:
            term *= entry(blocks, left, right, color, color)
        total += term
    return total


def channel(blocks, endpoint, deleted, color=0):
    residual = [site for site in SITES if site not in (endpoint, deleted)]
    return {
        endpoint_color
        for endpoint_color in COLORS
        if any(
            entry(blocks, endpoint, site, endpoint_color, color)
            for site in residual
        )
    }


def star_rank(blocks, endpoint, deleted):
    residual = [site for site in SITES if site not in (endpoint, deleted)]
    rows = []
    for endpoint_color in COLORS:
        rows.append(
            [
                entry(blocks, endpoint, site, endpoint_color, site_color)
                for site in residual
                for site_color in COLORS
            ]
        )
    return rank(rows)


def gamma_cross(blocks, i, j, k):
    common = [site for site in SITES if site not in (P_SITE, Q_SITE, R_SITE)]
    total = 0
    # Marked forms from p, q, r occupy three distinct common sites; the
    # remaining two sites use the single internal edge z^[1].
    for p_site in common:
        for q_site in common:
            if q_site == p_site:
                continue
            for r_site in common:
                if r_site in (p_site, q_site):
                    continue
                remaining = [
                    site for site in common if site not in (p_site, q_site, r_site)
                ]
                total += (
                    entry(blocks, P_SITE, p_site, i, 0)
                    * entry(blocks, Q_SITE, q_site, j, 0)
                    * entry(blocks, R_SITE, r_site, k, 0)
                    * entry(blocks, remaining[0], remaining[1], 0, 0)
                )
    return total


def verify_case(name, p_block, selected):
    blocks = build_blocks(p_block)
    assert full_tensor(blocks) == {(0,) * 8: 1}

    pq_residual = [site for site in SITES if site not in (P_SITE, Q_SITE)]
    pr_residual = [site for site in SITES if site not in (P_SITE, R_SITE)]
    assert pure_hafnian(blocks, pq_residual) == 0
    assert pure_hafnian(blocks, pr_residual) == 0

    assert channel(blocks, P_SITE, Q_SITE) == {0}
    assert channel(blocks, Q_SITE, P_SITE) == {0}
    assert channel(blocks, P_SITE, R_SITE) == {0}
    assert channel(blocks, R_SITE, P_SITE) == {0}
    assert any(p_block[i][j] for i in (1, 2) for j in (1, 2))
    r_block = blocks[(P_SITE, R_SITE)]
    assert any(r_block[i][j] for i in (1, 2) for j in (1, 2))

    assert star_rank(blocks, P_SITE, Q_SITE) == 3
    assert star_rank(blocks, Q_SITE, P_SITE) == 3
    assert star_rank(blocks, P_SITE, R_SITE) == 3
    assert star_rank(blocks, R_SITE, P_SITE) == 3

    for i in COLORS:
        for j in COLORS:
            for k in COLORS:
                expected = int(i == j == k == 0)
                assert gamma_cross(blocks, i, j, k) == expected

    alpha, beta = selected
    direct_a = entry(blocks, P_SITE, Q_SITE, alpha, beta)
    direct_b = entry(blocks, P_SITE, R_SITE, alpha, 0)
    direct_f = entry(blocks, Q_SITE, S_SITE, beta, 0)
    direct_u = entry(blocks, R_SITE, S_SITE, 0, 0)
    assert direct_a != 0
    assert direct_a * direct_u - direct_b * direct_f == direct_a
    print(f"{name}: PASS")


def main():
    verify_case("diagonal selected cell", lower_identity(), (1, 1))
    verify_case("off-diagonal selected cell", lower_swap(), (1, 2))
    print("double-zero cross-Gamma guard: PASS")


if __name__ == "__main__":
    main()
