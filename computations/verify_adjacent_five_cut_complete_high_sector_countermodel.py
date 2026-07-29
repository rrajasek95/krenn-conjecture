#!/usr/bin/env python3
"""Exact audit for the adjacent complete high-sector countermodel.

The checker uses only integer coefficient dictionaries.  It verifies the
sector identities and the full restriction maps on bases of both cofactor
kernels, not merely the two displayed target-active witnesses.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import permutations, product


B = tuple(range(8))
S = tuple(range(6))
R = (6, 7)

MATCHINGS = {
    0: ((0, 1), (2, 3), (4, 5), (6, 7)),
    1: ((0, 2), (1, 4), (3, 6), (5, 7)),
    2: ((0, 4), (1, 3), (2, 7), (5, 6)),
}


def edge(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


EDGE_COLORS: dict[tuple[int, int], tuple[int, ...]] = {}
for color, matching in MATCHINGS.items():
    for pair in matching:
        assert edge(*pair) not in EDGE_COLORS
        EDGE_COLORS[edge(*pair)] = (color,)


Tensor = dict[tuple[int, ...], int]


def add_term(tensor: Tensor, word: tuple[int, ...], value: int = 1) -> None:
    new_value = tensor.get(word, 0) + value
    if new_value:
        tensor[word] = new_value
    elif word in tensor:
        del tensor[word]


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index, second in enumerate(vertices[1:]):
        rest = vertices[1:index + 1] + vertices[index + 2:]
        for matching in perfect_matchings(rest):
            answer.append((edge(first, second),) + matching)
    return tuple(answer)


def decorated_terms(vertices: tuple[int, ...]) -> list[
    tuple[tuple[tuple[int, int], ...], tuple[int, ...], int]
]:
    """All nonzero decorated matching terms on ``vertices``."""
    vertices = tuple(sorted(vertices))
    positions = {vertex: index for index, vertex in enumerate(vertices)}
    answer = []
    for matching in perfect_matchings(vertices):
        choices = [EDGE_COLORS.get(pair, ()) for pair in matching]
        if any(not colors for colors in choices):
            continue
        for colors in product(*choices):
            word = [-1] * len(vertices)
            for (a, b), color in zip(matching, colors):
                word[positions[a]] = color
                word[positions[b]] = color
            assert all(value >= 0 for value in word)
            answer.append((matching, tuple(word), 1))
    return answer


@lru_cache(maxsize=None)
def matching_tensor(vertices: tuple[int, ...]) -> Tensor:
    result: Tensor = {}
    for _matching, word, coefficient in decorated_terms(vertices):
        add_term(result, word, coefficient)
    return result


def full_word(
    vertices: tuple[int, ...], word: tuple[int, ...]
) -> tuple[int, ...]:
    values = [-1] * len(B)
    for vertex, color in zip(vertices, word):
        values[vertex] = color
    return tuple(values)


def tensor_sum(*tensors: Tensor) -> Tensor:
    result: Tensor = {}
    for tensor in tensors:
        for word, coefficient in tensor.items():
            add_term(result, word, coefficient)
    return result


def restrict_word(
    word: tuple[int, ...], vertices: tuple[int, ...]
) -> tuple[int, ...]:
    return tuple(word[vertex] for vertex in vertices)


def sector(cut_left: tuple[int, ...], crossings: int) -> Tensor:
    left = set(cut_left)
    result: Tensor = {}
    for matching, word, coefficient in decorated_terms(B):
        count = sum((a in left) != (b in left) for a, b in matching)
        if count == crossings:
            add_term(result, word, coefficient)
    return result


def even_pair_sector(a: int, b: int) -> Tensor:
    """The R|S two-crossing sector with S crossing sites exactly a,b."""
    result: Tensor = {}
    for matching, word, coefficient in decorated_terms(B):
        crossing_sites = {
            x
            for pair in matching
            if ((pair[0] in R) != (pair[1] in R))
            for x in pair
            if x in S
        }
        if crossing_sites == {a, b}:
            add_term(result, word, coefficient)
    return result


def direct_pair_formula(a: int, b: int) -> Tensor:
    """Equation (4), expanded from the actual edge maps."""
    result: Tensor = {}
    remaining = tuple(x for x in S if x not in (a, b))
    h_remaining = matching_tensor(remaining)
    for p_to_a, q_to_b in ((a, b), (b, a)):
        for color_pa in EDGE_COLORS.get(edge(6, p_to_a), ()):
            for color_qb in EDGE_COLORS.get(edge(7, q_to_b), ()):
                for h_word, coefficient in h_remaining.items():
                    word = [-1] * 8
                    word[6] = word[p_to_a] = color_pa
                    word[7] = word[q_to_b] = color_qb
                    for vertex, color in zip(remaining, h_word):
                        word[vertex] = color
                    if all(value >= 0 for value in word):
                        add_term(result, tuple(word), coefficient)
    return result


def direct_t3_formula(z: int) -> Tensor:
    """Equation (8), grouped by the unique internal edge of U_z."""
    u_set = tuple(x for x in S if x != z)
    c_set = (z, 6, 7)
    result: Tensor = {}
    for u_index, u in enumerate(u_set):
        for v in u_set[u_index + 1:]:
            internal_colors = EDGE_COLORS.get(edge(u, v), ())
            if not internal_colors:
                continue
            cross_targets = tuple(x for x in u_set if x not in (u, v))
            for target_order in permutations(cross_targets):
                cross_choices = [
                    EDGE_COLORS.get(edge(c, target), ())
                    for c, target in zip(c_set, target_order)
                ]
                if any(not colors for colors in cross_choices):
                    continue
                for internal_color in internal_colors:
                    for cross_colors in product(*cross_choices):
                        word = [-1] * 8
                        word[u] = word[v] = internal_color
                        for c, target, color in zip(
                            c_set, target_order, cross_colors
                        ):
                            word[c] = word[target] = color
                        assert all(value >= 0 for value in word)
                        add_term(result, tuple(word))
    return result


def cofactor_columns(u_set: tuple[int, ...]) -> list[Tensor]:
    """Coordinate dictionaries for V_u tensor H_(U-u), in U site order."""
    columns = []
    for hole in u_set:
        remaining = tuple(x for x in u_set if x != hole)
        h_remaining = matching_tensor(remaining)
        for color in range(3):
            column: Tensor = {}
            for h_word, coefficient in h_remaining.items():
                assignment = {hole: color}
                assignment.update(zip(remaining, h_word))
                word = tuple(assignment[x] for x in u_set)
                add_term(column, word, coefficient)
            columns.append(column)
    return columns


def coordinate_cofactor_support(u_set: tuple[int, ...]) -> set[tuple[int, ...]]:
    columns = [column for column in cofactor_columns(u_set) if column]
    assert all(len(column) == 1 for column in columns)
    support = {next(iter(column)) for column in columns}
    assert len(support) == len(columns)
    return support


def defect_color_support(u_set: tuple[int, ...]) -> set[int]:
    support = coordinate_cofactor_support(u_set)
    return {
        color for color in range(3) if (color,) * len(u_set) not in support
    }


def flatten_rows(tensor: Tensor, c_set: tuple[int, ...], u_set: tuple[int, ...]) -> dict[tuple[int, ...], Tensor]:
    rows: dict[tuple[int, ...], Tensor] = {}
    for word, coefficient in tensor.items():
        c_word = restrict_word(word, c_set)
        u_word = restrict_word(word, u_set)
        rows.setdefault(c_word, {})
        add_term(rows[c_word], u_word, coefficient)
    return rows


def contract_u(
    tensor: Tensor,
    c_set: tuple[int, ...],
    u_set: tuple[int, ...],
    beta_word: tuple[int, ...],
) -> Tensor:
    result: Tensor = {}
    for word, coefficient in tensor.items():
        if restrict_word(word, u_set) == beta_word:
            add_term(result, restrict_word(word, c_set), coefficient)
    return result


def contract_s(tensor: Tensor, eta_words: set[tuple[int, ...]]) -> Tensor:
    result: Tensor = {}
    for word, coefficient in tensor.items():
        if restrict_word(word, S) in eta_words:
            add_term(result, restrict_word(word, R), coefficient)
    return result


def audit_matching_tensor() -> None:
    terms = decorated_terms(B)
    assert len(terms) == 5
    observed = matching_tensor(B)
    expected = {
        (0, 0, 0, 0, 0, 0, 0, 0): 1,
        (1, 1, 1, 1, 1, 1, 1, 1): 1,
        (2, 2, 2, 2, 2, 2, 2, 2): 1,
        (0, 0, 2, 1, 0, 0, 1, 2): 1,
        (1, 2, 1, 2, 0, 0, 0, 0): 1,
    }
    assert observed == expected


def audit_sector_formulas() -> None:
    t0 = sector(R, 0)
    t2 = sector(R, 2)
    assert tensor_sum(t0, t2) == matching_tensor(B)

    pair_sectors = []
    for a in S:
        for b in S[a + 1:]:
            observed = even_pair_sector(a, b)
            expected = direct_pair_formula(a, b)
            assert observed == expected
            pair_sectors.append(observed)
    assert tensor_sum(*pair_sectors) == t2

    for z in S:
        u_set = tuple(x for x in S if x != z)
        c_set = (z, 6, 7)
        t1 = sector(c_set, 1)
        t3 = sector(c_set, 3)
        incident = [
            even_pair_sector(min(z, a), max(z, a))
            for a in S if a != z
        ]
        avoiding = [
            even_pair_sector(a, b)
            for a in u_set
            for b in u_set
            if a < b
        ]
        assert t1 == tensor_sum(t0, *incident)
        assert t3 == tensor_sum(*avoiding)
        assert t3 == direct_t3_formula(z)


def audit_cut(
    z: int,
    expected_cofactors: dict[int, Tensor],
    surviving_color: int,
    expected_t3: Tensor,
) -> None:
    u_set = tuple(x for x in S if x != z)
    c_set = (z, 6, 7)

    for hole in u_set:
        remaining = tuple(x for x in u_set if x != hole)
        assert matching_tensor(remaining) == expected_cofactors.get(hole, {})

    columns = cofactor_columns(u_set)
    nonzero_columns = [column for column in columns if column]
    assert len(nonzero_columns) == 9
    assert all(len(column) == 1 for column in nonzero_columns)
    support_words = coordinate_cofactor_support(u_set)
    assert len(support_words) == 9

    constant_words = {(color,) * 5 for color in range(3)}
    assert (surviving_color,) * 5 not in support_words
    assert constant_words - {(surviving_color,) * 5} <= support_words

    t1 = sector(c_set, 1)
    t3 = sector(c_set, 3)
    assert t3 == expected_t3

    # Every row of T1 belongs to the coordinate cofactor-insertion span.
    for row in flatten_rows(t1, c_set, u_set).values():
        assert set(row) <= support_words

    delta: Tensor = {(color,) * 8: 1 for color in range(3)}
    residual = tensor_sum(matching_tensor(B), {
        word: -coefficient for word, coefficient in delta.items()
    })
    for row in flatten_rows(residual, c_set, u_set).values():
        assert set(row) <= support_words

    # The coordinate duals outside the nine insertion words form a basis of K.
    for beta_word in product(range(3), repeat=5):
        if beta_word in support_words:
            continue
        high = contract_u(t3, c_set, u_set, beta_word)
        target: Tensor = {}
        for color in range(3):
            if beta_word == (color,) * 5:
                target[(color,) * 3] = 1
        assert high == target

    witness = (surviving_color,) * 5
    assert contract_u(t3, c_set, u_set, witness) == {
        (surviving_color,) * 3: 1
    }


def audit_two_complete_restrictions() -> None:
    audit_cut(
        z=2,
        expected_cofactors={
            0: {(2, 2, 0, 0): 1},
            3: {(0, 0, 0, 0): 1},
            5: {(2, 2, 2, 2): 1},
        },
        surviving_color=1,
        expected_t3={(1,) * 8: 1},
    )
    audit_cut(
        z=3,
        expected_cofactors={
            1: {(1, 1, 0, 0): 1},
            2: {(0, 0, 0, 0): 1},
            5: {(1, 1, 1, 1): 1},
        },
        surviving_color=2,
        expected_t3={(2,) * 8: 1},
    )


def audit_residual_decompositions() -> None:
    delta: Tensor = {(color,) * 8: 1 for color in range(3)}
    residual = tensor_sum(matching_tensor(B), {
        word: -coefficient for word, coefficient in delta.items()
    })

    u2 = (0, 1, 3, 4, 5)
    c2 = (2, 6, 7)
    rows2 = flatten_rows(residual, c2, u2)
    assert rows2 == {
        (2, 1, 2): {(0, 0, 1, 0, 0): 1},
        (1, 0, 0): {(1, 2, 2, 0, 0): 1},
    }

    u3 = (0, 1, 2, 4, 5)
    c3 = (3, 6, 7)
    rows3 = flatten_rows(residual, c3, u3)
    assert rows3 == {
        (1, 1, 2): {(0, 0, 2, 0, 0): 1},
        (2, 0, 0): {(1, 2, 1, 0, 0): 1},
    }


def audit_compatible_sum() -> None:
    t0 = sector(R, 0)
    t2 = sector(R, 2)
    eta_words = {(1,) * 6, (2,) * 6}
    assert contract_s(t0, eta_words) == {}
    assert contract_s(t2, eta_words) == {
        (1, 1): 1,
        (2, 2): 1,
    }

    cut2_high = contract_u(
        sector((2, 6, 7), 3),
        (2, 6, 7),
        (0, 1, 3, 4, 5),
        (1,) * 5,
    )
    cut3_high = contract_u(
        sector((3, 6, 7), 3),
        (3, 6, 7),
        (0, 1, 2, 4, 5),
        (2,) * 5,
    )
    # Contract the z slot by e_1^* and e_2^*, respectively.
    assert cut2_high == {(1, 1, 1): 1}
    assert cut3_high == {(2, 2, 2): 1}
    combined_r = {
        cut2_high_word[1:]: coefficient
        for cut2_high_word, coefficient in cut2_high.items()
    }
    for cut3_high_word, coefficient in cut3_high.items():
        add_term(combined_r, cut3_high_word[1:], coefficient)
    assert combined_r == contract_s(t2, eta_words)

    # L_2 has target support only in color one and L_3 only in color two.
    # Hence their common lifted-kernel intersection is target-zero, while
    # the summed family above remains target-active.
    target_support_l2 = defect_color_support((0, 1, 3, 4, 5))
    target_support_l3 = defect_color_support((0, 1, 2, 4, 5))
    assert target_support_l2 == {1}
    assert target_support_l3 == {2}
    assert target_support_l2.isdisjoint(target_support_l3)


def main() -> None:
    audit_matching_tensor()
    audit_sector_formulas()
    audit_two_complete_restrictions()
    audit_residual_decompositions()
    audit_compatible_sum()
    print("adjacent complete high-sector countermodel: PASS")
    print("two full T3|K = iota delta|K restriction maps: PASS")
    print("six-cut T1/T3 versus T0/T2 formulas: PASS")
    print("target-active summed-lift contraction of T2: PASS")
    print("common lifted-kernel intersection remains target-zero: PASS")


if __name__ == "__main__":
    main()
