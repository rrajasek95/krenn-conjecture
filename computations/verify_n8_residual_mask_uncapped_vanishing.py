#!/usr/bin/env python3
"""Exact audit of erasing-coordinate consequences on residual K8 masks."""

from itertools import product

import verify_n8_witness_union_five_stages as stages


COLORS = tuple(range(3))


def cross(left, right):
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def outer(left, right):
    return [[left[i] * right[j] for j in range(3)] for i in range(3)]


def add(left, right):
    return [[left[i][j] + right[i][j] for j in range(3)]
            for i in range(3)]


def scale(value, matrix):
    return [[value * entry for entry in row] for row in matrix]


def determinant3(matrix):
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2]
                        - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2]
                          - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1]
                          - matrix[1][1] * matrix[2][0])
    )


def matmul(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(3))
             for j in range(3)] for i in range(3)]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


K = (
    ((0, 0, 0), (0, 0, 1), (0, -1, 0)),
    ((0, 0, -1), (0, 0, 0), (1, 0, 0)),
    ((0, 1, 0), (-1, 0, 0), (0, 0, 0)),
)


def rank_one_matrix(left, row):
    return outer(left, row)


def zero_mask(p_matrix, q_matrix):
    answer = 0
    for color in COLORS:
        value = matmul(matmul(p_matrix, K[color]), transpose(q_matrix))
        if not any(entry for row in value for entry in row):
            answer |= 1 << color
    return answer


def residual_assignments():
    answer = []
    for masks in stages.EXPECTED_RESIDUAL:
        for hard in stages.hard_assignments(masks):
            if stages.rank_two_certificate(masks, hard):
                continue
            if stages.free_plane_monomial_certificate(masks, hard):
                continue
            answer.append((masks, hard))
    return answer


def erasing_options(mask, hard_mask):
    if mask == stages.TRIPLE:
        assert hard_mask in (1, 2, 4)
        hard_color = hard_mask.bit_length() - 1
        return tuple(color for color in COLORS if color != hard_color)
    if mask.bit_count() == 2:
        return (next(color for color in COLORS if not (mask >> color & 1)),)
    return ()


def choose_erasing_pattern(masks, hard):
    sites = tuple(site for site, mask in enumerate(masks)
                  if erasing_options(mask, hard[site]))
    options = tuple(erasing_options(masks[site], hard[site]) for site in sites)
    if not options:
        return sites, ()
    # Prefer a pattern using as many distinct colors as possible.  This
    # certifies that every extension is nonconstant.
    choice = max(product(*options), key=lambda word: (len(set(word)), word))
    return sites, choice


def audit_residual_enumeration():
    assignments = residual_assignments()
    assert len(assignments) == 36
    sizes = []
    for masks, hard in assignments:
        sites, word = choose_erasing_pattern(masks, hard)
        sizes.append(len(sites))
        if len(sites) >= 4:
            assert len(set(word)) >= 2
        if len(sites) == 4:
            survivors = tuple(mask for site, mask in enumerate(masks)
                              if site not in sites)
            assert survivors == (0, 1)
        if len(sites) == 5:
            survivors = tuple(mask for site, mask in enumerate(masks)
                              if site not in sites)
            assert survivors == (0,)
    assert sizes.count(2) == 1
    assert sizes.count(4) == 11
    assert sizes.count(5) == 24


def audit_last_row_countermodel():
    e0, e1, e2 = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    ell_generic = (1, 1, 1)
    row_no_zero = (1, 2, 4)
    row_single_zero = (2, 1, 1)

    ell = [ell_generic, ell_generic, ell_generic, ell_generic, e1, e1]
    row = [row_no_zero, row_single_zero, row_single_zero,
           row_single_zero, e2, e2]
    p_left = [e0, e1, e2, e0, e0, e0]
    q_left = [e0, e1, e2, e2, e0, e0]
    p_blocks = [rank_one_matrix(p_left[u], ell[u]) for u in range(6)]
    q_blocks = [rank_one_matrix(q_left[u], row[u]) for u in range(6)]
    assert tuple(zero_mask(p_blocks[u], q_blocks[u]) for u in range(6)) == (
        0, 1, 1, 1, 6, 6
    )

    word = (0, 0, 0, 1, 0, 0)
    assert len(set(word)) > 1
    p_columns = [tuple(p_blocks[u][i][word[u]] for i in COLORS)
                 for u in range(6)]
    q_columns = [tuple(q_blocks[u][i][word[u]] for i in COLORS)
                 for u in range(6)]
    assert p_columns == [e0, e1, e2, e0, (0, 0, 0), (0, 0, 0)]
    assert q_columns == [e0, (0, 2, 0), (0, 0, 2), e2,
                         (0, 0, 0), (0, 0, 0)]

    # The internal coefficient graph at this word is the unique matching
    # 01|23|45, all with scalar weight one.  Its nonzero four-site
    # cofactors are exactly h_01=h_23=h_45=1.
    correction_01 = add(outer(p_columns[0], q_columns[1]),
                        outer(p_columns[1], q_columns[0]))
    correction_23 = add(outer(p_columns[2], q_columns[3]),
                        outer(p_columns[3], q_columns[2]))
    correction_45 = add(outer(p_columns[4], q_columns[5]),
                        outer(p_columns[5], q_columns[4]))
    correction = add(add(correction_01, correction_23), correction_45)
    expected = [[0, 2, 2], [1, 0, 0], [0, 0, 1]]
    assert correction == expected
    assert determinant3(correction) == -2
    a_pq = scale(-1, correction)
    assert determinant3(a_pq) == 2
    h_word = 1
    pair_slice = add(scale(h_word, a_pq), correction)
    assert pair_slice == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


def main():
    audit_residual_enumeration()
    audit_last_row_countermodel()
    print("PASS: residual erasure split 1 + 11 + 24 audited")
    print("PASS: exact integer last-row rank-three local countermodel audited")


if __name__ == "__main__":
    main()
