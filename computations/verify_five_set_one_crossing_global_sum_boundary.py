#!/usr/bin/env python3
"""Exact audit for global five-set one-crossing sector counts."""

from itertools import combinations
from fractions import Fraction
from math import comb


def crossing_count(matching, subset):
    subset = set(subset)
    return sum((x in subset) != (y in subset) for x, y in matching)


def standard_matching(m):
    return tuple((2 * i, 2 * i + 1) for i in range(m))


def matching_with_cut_count(m, k):
    """A matching crossing U={0,...,4} in exactly k edges."""
    inside = list(range(5))
    outside = list(range(5, 2 * m))
    assert k in (1, 3, 5)
    assert k <= len(outside)
    matching = list(zip(inside[:k], outside[:k]))
    inside_rest = inside[k:]
    outside_rest = outside[k:]
    assert len(inside_rest) % 2 == len(outside_rest) % 2 == 0
    matching.extend(zip(inside_rest[::2], inside_rest[1::2]))
    matching.extend(zip(outside_rest[::2], outside_rest[1::2]))
    assert len(matching) == m
    return tuple(matching)


def audit_counts():
    for m in range(3, 8):
        vertices = tuple(range(2 * m))
        matching = standard_matching(m)
        subsets = tuple(combinations(vertices, 5))
        for j in (1, 3, 5):
            actual = sum(crossing_count(matching, u) == j for u in subsets)
            expected = (
                2**j * comb(m, j) * comb(m - j, (5 - j) // 2)
                if m >= j
                else 0
            )
            assert actual == expected

        x = 0
        actual_vertex = sum(
            x in u and crossing_count(matching, u) == 1 for u in subsets
        )
        assert actual_vertex == 5 * comb(m - 1, 2)

        # A matched pair and an unmatched pair give the two coefficients
        # in the edge-localized identity.
        matched_pair = (0, 1)
        unmatched_pair = (0, 2)
        matched_count = sum(
            set(matched_pair) <= set(u) and crossing_count(matching, u) == 1
            for u in subsets
        )
        unmatched_count = sum(
            set(unmatched_pair) <= set(u)
            and crossing_count(matching, u) == 1
            for u in subsets
        )
        assert matched_count == 2 * (m - 1) * (m - 2)
        assert unmatched_count == 4 * (m - 2)


def audit_overlap_shells():
    for m in range(3, 9):
        vertices = tuple(range(2 * m))
        center = frozenset(range(5))
        five_sets = tuple(map(frozenset, combinations(vertices, 5)))
        for k in (1, 3, 5):
            if k > 2 * m - 5:
                continue
            matching = matching_with_cut_count(m, k)
            assert crossing_count(matching, center) == k
            shell_4 = sum(
                len(center & v) == 4 and crossing_count(matching, v) == 1
                for v in five_sets
            )
            shell_3 = sum(
                len(center & v) == 3 and crossing_count(matching, v) == 1
                for v in five_sets
            )
            expected_4 = {1: 2 * m - 1, 3: 6, 5: 0}[k]
            expected_3 = {
                1: 10 * (m - 3),
                3: 9 * m - 21,
                5: 30,
            }[k]
            assert shell_4 == expected_4
            assert shell_3 == expected_3

            # Coefficient of this matching atom in the radius-two
            # reconstruction formula.
            center_term = int(k == 1)
            reconstructed = (
                Fraction(6 * m * m - 57 * m + 137, 60) * center_term
                + Fraction(17 - 3 * m, 60) * shell_4
                + Fraction(1, 30) * shell_3
            )
            assert reconstructed == 1


def perfect_matchings(vertices, edges):
    vertices = frozenset(vertices)
    if not vertices:
        yield ()
        return
    x = min(vertices)
    for edge in edges:
        if x not in edge:
            continue
        y = edge[0] if edge[1] == x else edge[1]
        if y not in vertices:
            continue
        for rest in perfect_matchings(vertices - {x, y}, edges):
            yield (edge,) + rest


def audit_cube():
    vertices = tuple(range(8))
    coordinate_matchings = []
    for bit in range(3):
        matching = frozenset(
            (x, x ^ (1 << bit))
            for x in vertices
            if x < (x ^ (1 << bit))
        )
        assert len(matching) == 4
        coordinate_matchings.append(matching)

    cube_edges = frozenset().union(*coordinate_matchings)
    all_matchings = {
        frozenset(matching)
        for matching in perfect_matchings(vertices, cube_edges)
    }
    assert len(all_matchings) == 9
    assert all(matching in all_matchings for matching in coordinate_matchings)
    assert len(all_matchings - set(coordinate_matchings)) == 6

    # Symbolic edge-exponent audit of the three cube binomials.  Each edge
    # carries only the diagonal cell whose color is its coordinate bit.
    edge_order = tuple(sorted(cube_edges))
    edge_index = {edge: i for i, edge in enumerate(edge_order)}
    edge_color = {
        edge: color
        for color, matching in enumerate(coordinate_matchings)
        for edge in matching
    }
    word_exponents = {}
    for matching in all_matchings:
        word = [None] * 8
        exponent = [0] * len(edge_order)
        for edge in matching:
            color = edge_color[edge]
            for vertex in edge:
                word[vertex] = color
            exponent[edge_index[edge]] += 1
        word_exponents["".join(map(str, word))] = tuple(exponent)

    expected_words = {
        "00000000",
        "11111111",
        "22222222",
        "00001111",
        "11110000",
        "00220022",
        "22002200",
        "12121212",
        "21212121",
    }
    assert set(word_exponents) == expected_words

    def exponent_sum(left, right):
        return tuple(a + b for a, b in zip(
            word_exponents[left], word_exponents[right]
        ))

    assert exponent_sum("00001111", "11110000") == exponent_sum(
        "00000000", "11111111"
    )
    assert exponent_sum("00220022", "22002200") == exponent_sum(
        "00000000", "22222222"
    )
    assert exponent_sum("12121212", "21212121") == exponent_sum(
        "11111111", "22222222"
    )

    histogram = {0: 0, 1: 0, 2: 0}
    five_sets = tuple(map(frozenset, combinations(vertices, 5)))
    for complement in combinations(vertices, 3):
        complement = frozenset(complement)
        center = frozenset(vertices) - complement
        active = sum(
            any(x in complement and y in complement for x, y in matching)
            for matching in coordinate_matchings
        )
        assert active < 3
        histogram[active] += 1

        # Even though this center cut misses at least one constant row,
        # every retained cube atom obeys the radius-two reconstruction.
        for matching in coordinate_matchings:
            center_term = int(crossing_count(matching, center) == 1)
            shell_4 = sum(
                len(center & v) == 4 and crossing_count(matching, v) == 1
                for v in five_sets
            )
            shell_3 = sum(
                len(center & v) == 3 and crossing_count(matching, v) == 1
                for v in five_sets
            )
            reconstructed = (
                Fraction(1, 12) * (center_term + shell_4)
                + Fraction(1, 30) * shell_3
            )
            assert reconstructed == 1
    assert histogram == {0: 8, 1: 24, 2: 24}


def main():
    audit_counts()
    audit_overlap_shells()
    audit_cube()
    print("five-set global one-crossing sum boundary audit: PASS")


if __name__ == "__main__":
    main()
