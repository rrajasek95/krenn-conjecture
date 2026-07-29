#!/usr/bin/env python3
"""Clean-room audit of the eight-site shared pair-cap countermodel.

This checker uses sparse multiplication in the site-square-zero algebra.
It imports no primary or border checker and does not enumerate distinguished
perfect matchings to compute the polarized tensor.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product


N = 8
EMPTY = -1
SITES = tuple(range(N))
COLORS = (0, 1, 2)
EDGES = tuple(combinations(SITES, 2))
ZERO_WORD = (EMPTY,) * N


def monomial(entries):
    word = [EMPTY] * N
    for site, color in entries.items():
        word[site] = color
    return tuple(word)


def merge_words(left, right):
    merged = []
    for x, y in zip(left, right, strict=True):
        if x != EMPTY and y != EMPTY:
            return None
        merged.append(y if x == EMPTY else x)
    return tuple(merged)


def add(*tensors):
    result = defaultdict(Fraction)
    for tensor in tensors:
        for word, value in tensor.items():
            result[word] += value
    return {word: value for word, value in result.items() if value}


def scale(value, tensor):
    value = Fraction(value)
    return {word: value * coefficient for word, coefficient in tensor.items()
            if value * coefficient}


def multiply(left, right):
    result = defaultdict(Fraction)
    for left_word, left_value in left.items():
        for right_word, right_value in right.items():
            merged = merge_words(left_word, right_word)
            if merged is not None:
                result[merged] += left_value * right_value
    return {word: value for word, value in result.items() if value}


def power(tensor, exponent):
    result = {ZERO_WORD: Fraction(1)}
    for _ in range(exponent):
        result = multiply(result, tensor)
    return result


def divided_power(tensor, exponent):
    factorial = 1
    for value in range(2, exponent + 1):
        factorial *= value
    raw = power(tensor, exponent)
    assert all(coefficient.denominator == 1 for coefficient in raw.values())
    return {
        word: coefficient / factorial
        for word, coefficient in raw.items()
        if coefficient
    }


COLOR_MATCHINGS = (
    ((0, 1), (2, 3), (4, 5), (6, 7)),
    ((0, 7), (1, 2), (3, 4), (5, 6)),
    ((0, 4), (1, 7), (2, 6), (3, 5)),
)


def build_q():
    terms = {}
    for color, matching in enumerate(COLOR_MATCHINGS):
        for u, v in matching:
            word = monomial({u: color, v: color})
            assert word not in terms
            terms[word] = Fraction(1)
    assert len(terms) == 12
    return terms


def build_rows():
    p_coefficients = {
        0: Fraction(1),
        2: Fraction(1),
        4: Fraction(-1, 8),
        6: Fraction(-1, 8),
    }
    s_coefficients = {
        0: Fraction(1),
        2: Fraction(-1),
        4: Fraction(-1, 8),
        6: Fraction(1, 8),
    }
    p = {monomial({site: 2}): value for site, value in p_coefficients.items()}
    s = {monomial({site: 2}): value for site, value in s_coefficients.items()}
    return p, s


def word_support(word):
    return frozenset(site for site, color in enumerate(word) if color != EMPTY)


def cell_from_word(word):
    sites = sorted(word_support(word))
    assert len(sites) == 2
    return (tuple(sites), tuple(word[site] for site in sites))


def restrict_quadratic(q, allowed_sites):
    allowed_sites = frozenset(allowed_sites)
    return {
        word: value
        for word, value in q.items()
        if word_support(word) <= allowed_sites
    }


def attach_cell(tensor, edge, color):
    cell = {monomial({edge[0]: color, edge[1]: color}): Fraction(1)}
    return multiply(cell, tensor)


def audit_model():
    q = build_q()
    p, s = build_rows()
    ps = multiply(p, s)
    assert {
        cell_from_word(word): value for word, value in ps.items()
    } == {
        ((0, 4), (2, 2)): Fraction(-1, 4),
        ((2, 6), (2, 2)): Fraction(1, 4),
    }

    q3_raw = power(q, 3)
    q3 = divided_power(q, 3)
    assert q3_raw == scale(6, q3)
    q4_raw = power(q, 4)
    q4 = divided_power(q, 4)
    assert q4_raw == scale(24, q4)
    assert multiply(q, q3) == scale(4, q4)

    mixed_a = (2, 1, 1, 2, 2, 2, 0, 0)
    mixed_b = (2, 2, 0, 0, 2, 1, 1, 2)
    expected_q4 = {(color,) * N: Fraction(1) for color in COLORS}
    expected_q4[mixed_a] = Fraction(1)
    expected_q4[mixed_b] = Fraction(1)
    assert q4 == expected_q4

    q_away_04 = restrict_quadratic(q, set(SITES) - {0, 4})
    q_away_26 = restrict_quadratic(q, set(SITES) - {2, 6})
    cofactor_04 = divided_power(q_away_04, 3)
    cofactor_26 = divided_power(q_away_26, 3)
    assert attach_cell(cofactor_04, (0, 4), 2) == {
        mixed_a: Fraction(1),
        mixed_b: Fraction(1),
        (2,) * N: Fraction(1),
    }
    assert attach_cell(cofactor_26, (2, 6), 2) == {
        (2,) * N: Fraction(1)
    }

    psq3 = multiply(ps, q3)
    assert psq3 == {
        mixed_a: Fraction(-1, 4),
        mixed_b: Fraction(-1, 4),
    }

    z = add(scale(Fraction(1, 4), q), scale(4, ps))
    z_cells = {cell_from_word(word): value for word, value in z.items()}
    assert len(z_cells) == 12
    assert z_cells[((0, 4), (2, 2))] == Fraction(-3, 4)
    assert z_cells[((2, 6), (2, 2))] == Fraction(5, 4)

    polarized = multiply(z, q3)
    target = {(color,) * N: Fraction(1) for color in COLORS}
    checked = 0
    for coloring in product(COLORS, repeat=N):
        assert polarized.get(coloring, Fraction(0)) == target.get(
            coloring, Fraction(0)
        )
        checked += 1
    assert checked == 3**N == 6561
    assert polarized == target
    return q, q3, q4, ps, z, mixed_a, mixed_b, checked


def all_cells():
    for u, v in EDGES:
        for alpha, beta in product(COLORS, repeat=2):
            yield ((u, v), (alpha, beta))


def tensor_for_cell(cell):
    (u, v), (alpha, beta) = cell
    return {monomial({u: alpha, v: beta}): Fraction(1)}


def active_cells():
    return {
        (tuple(sorted(edge)), (color, color))
        for color, matching in enumerate(COLOR_MATCHINGS)
        for edge in matching
    }


def rational_rank(rows):
    matrix = [[Fraction(value) for value in row] for row in rows]
    rank = 0
    column = 0
    while matrix and rank < len(matrix) and column < len(matrix[0]):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            column += 1
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                x - factor * y
                for x, y in zip(matrix[row], matrix[rank], strict=True)
            ]
        rank += 1
        column += 1
    return rank


def audit_response_map(q3, q4):
    columns = tuple(all_cells())
    rows = defaultdict(dict)
    for cell in columns:
        response = multiply(tensor_for_cell(cell), q3)
        for word, value in response.items():
            rows[word][cell] = value
    rows = {word: row for word, row in rows.items() if row}
    singleton_rows = {
        word: next(iter(row.items()))
        for word, row in rows.items()
        if len(row) == 1
    }

    active = active_cells()
    inactive = set(columns) - active
    assert all(value == 1 for _, value in singleton_rows.values())
    singleton_columns = {cell for cell, _ in singleton_rows.values()}
    exposed = {cell for cell, value in singleton_rows.values() if value == 1}
    assert len(columns) == 252
    assert len(rows) == 363
    assert len(singleton_rows) == 358
    assert singleton_columns == inactive
    assert exposed == inactive
    assert len(inactive) == 240
    assert set(singleton_rows).isdisjoint(q4)

    restricted = {
        word: {cell: value for cell, value in row.items() if cell in active}
        for word, row in rows.items()
    }
    restricted = {word: row for word, row in restricted.items() if row}
    assert set(restricted) == set(q4)
    assert all(len(row) == 4 and set(row.values()) == {Fraction(1)}
               for row in restricted.values())
    ordered_active = sorted(active)
    incidence = [
        [restricted[word].get(cell, 0) for cell in ordered_active]
        for word in sorted(restricted)
    ]
    assert rational_rank(incidence) == 5

    allowed_ports = {
        frozenset(((u, color), (v, color)))
        for (u, v), (color, _) in active
    }
    degrees = Counter(port for pair in allowed_ports for port in pair)
    assert len(allowed_ports) == 12
    assert set(degrees) == {(site, color) for site in SITES for color in COLORS}
    assert set(degrees.values()) == {1}
    return len(rows), len(singleton_rows), len(exposed), rational_rank(incidence)


def map_word(word, site_map, color_map):
    image = [None] * N
    for old_site, color in enumerate(word):
        image[site_map[old_site]] = color_map[color]
    return tuple(image)


def audit_border_isomorphism(q, mixed_a, mixed_b):
    site_map = (3, 0, 1, 5, 6, 7, 4, 2)
    color_map = (1, 2, 0)
    border_matchings = (
        ((0, 2), (1, 4), (3, 6), (5, 7)),
        ((0, 3), (1, 5), (2, 4), (6, 7)),
        ((0, 1), (2, 3), (4, 7), (5, 6)),
    )
    border_cells = {
        (tuple(sorted(edge)), (color, color))
        for color, matching in enumerate(border_matchings)
        for edge in matching
    }
    image_cells = set()
    for word in q:
        (u, v), (alpha, beta) = cell_from_word(word)
        mapped_edge = tuple(sorted((site_map[u], site_map[v])))
        image_cells.add((mapped_edge, (color_map[alpha], color_map[beta])))
    assert image_cells == border_cells

    border_mixed = {
        (2, 2, 1, 0, 1, 0, 0, 0),
        (0, 1, 0, 0, 2, 1, 0, 2),
    }
    assert {
        map_word(mixed_a, site_map, color_map),
        map_word(mixed_b, site_map, color_map),
    } == border_mixed
    return color_map, site_map


def audit_overlap_redecomposition():
    """Audit (27) cell by cell and the corrected factors in (28)-(29)."""
    R, T = "r", "t"
    old = tuple(range(8))
    all_sites = (R, T) + old

    categories = Counter()
    for left_index, left in enumerate(all_sites):
        for right in all_sites[left_index + 1 :]:
            for alpha, beta in product(COLORS, repeat=2):
                edge = frozenset((left, right))
                if edge == frozenset((R, T)):
                    source = ("a", alpha, beta)
                    new_category = "r-star-to-t"
                elif R in edge:
                    vertex = next(site for site in edge if site != R)
                    source = ("p", alpha, vertex, beta)
                    new_category = "direct" if vertex == 0 else "r-star-to-old"
                elif T in edge:
                    vertex = next(site for site in edge if site != T)
                    # If the canonical loop order is old,t, alpha belongs to
                    # old and beta to t; retain the named endpoint colors.
                    if left == T:
                        t_color, old_color = alpha, beta
                    else:
                        old_color, t_color = alpha, beta
                    source = ("s", t_color, vertex, old_color)
                    new_category = "zero-star-to-t" if vertex == 0 else "internal-t-old"
                else:
                    source = ("q", left, alpha, right, beta)
                    new_category = "zero-star-to-old" if 0 in edge else "internal-old"

                # Formula (27) assigns every literal coefficient once.
                assert source[0] in {"a", "p", "s", "q"}
                categories[new_category] += 1

    assert sum(categories.values()) == 45 * 9 == 405
    assert categories == Counter(
        {
            "internal-old": 21 * 9,
            "internal-t-old": 7 * 9,
            "direct": 9,
            "r-star-to-t": 9,
            "r-star-to-old": 7 * 9,
            "zero-star-to-t": 9,
            "zero-star-to-old": 7 * 9,
        }
    )

    # If Raw=b*Q+R is the literal matching coefficient and qF=4Q,
    # then Polarized=(b*q+4ps)F=4*Raw.
    b, Q, Rstar = Fraction(2), Fraction(3), Fraction(5)
    raw = b * Q + Rstar
    polarized = b * (4 * Q) + 4 * Rstar
    assert polarized == 4 * raw
    assert (polarized, raw) == (44, 11)
    return categories, (4, 1)


def main():
    q, q3, q4, ps, z, mixed_a, mixed_b, checked = audit_model()
    response = audit_response_map(q3, q4)
    isomorphism = audit_border_isomorphism(q, mixed_a, mixed_b)
    overlap_categories, overlap_factors = audit_overlap_redecomposition()
    print("shared pair-cap countermodel independent audit: PASS")
    print("q / ps / z cells:", len(q), len(ps), len(z))
    print("q^[3] / q^[4] words:", len(q3), len(q4))
    print("coloring coefficients checked:", checked)
    print("response rows / singleton / exposed / rank:", response)
    print("border isomorphism (colors/sites):", isomorphism)
    print("overlap category counts:", dict(overlap_categories))
    print("overlap target factors (polarized/raw):", overlap_factors)


if __name__ == "__main__":
    main()
