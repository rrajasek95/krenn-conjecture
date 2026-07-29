#!/usr/bin/env python3
"""Exact audit of the matching-hole, zero-cross paired-Pfaffian obstruction.

After grouping the six sites into the three edges of the pure hole matching,
the proper four-site equations put each of the three particle cross blocks
in one of five components: rank one, or one of four site-isolating linear
components.  For all 5^3 component triples this checker constructs the
formal full particle Pfaffian tensor over Z and finds a nontrivial physical
cut whose flattening has rank at most one identically.
"""

from __future__ import annotations

import itertools
from collections import Counter, defaultdict


N = 6
GROUPS = ((0, 1), (2, 3), (4, 5))
GROUP_PAIRS = ((0, 1), (1, 2), (2, 0))
COMPONENTS = ("rank1", "left0", "left1", "right0", "right1")
COLORINGS = tuple(itertools.product((0, 1), repeat=N))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


MATCHINGS = tuple(perfect_matchings(tuple(range(N))))


def pfaffian_sign(matching) -> int:
    crossings = sum(
        a < c < b < d or c < a < d < b
        for (a, b), (c, d) in itertools.combinations(matching, 2)
    )
    return (-1) ** crossings


# A sparse polynomial is a Counter from a sorted tuple of formal variable
# labels to its integer coefficient.
def variable(label) -> Counter:
    return Counter({(label,): 1})


def normalize(polynomial: Counter) -> Counter:
    return Counter(
        {monomial: coefficient for monomial, coefficient in polynomial.items() if coefficient}
    )


def multiply(left: Counter, right: Counter) -> Counter:
    answer = Counter()
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            answer[monomial] += left_coefficient * right_coefficient
    return normalize(answer)


def subtract(left: Counter, right: Counter) -> Counter:
    answer = left.copy()
    answer.subtract(right)
    return normalize(answer)


def component_entry(
    pair_index: int,
    component: str,
    left_site: int,
    left_color: int,
    right_site: int,
    right_color: int,
) -> Counter:
    if component == "rank1":
        left = variable((pair_index, "L", left_site, left_color))
        right = variable((pair_index, "R", right_site, right_color))
        return multiply(left, right)
    side, isolated = component[:-1], int(component[-1])
    if (side == "left" and left_site == isolated) or (
        side == "right" and right_site == isolated
    ):
        return Counter()
    return variable(
        (
            pair_index,
            "S",
            left_site,
            left_color,
            right_site,
            right_color,
        )
    )


def generic_tensor(component_triple) -> dict[tuple[int, ...], Counter]:
    blocks = {
        pair: (index, component)
        for index, (pair, component) in enumerate(
            zip(GROUP_PAIRS, component_triple)
        )
    }
    site_group = {
        vertex: group for group, vertices in enumerate(GROUPS) for vertex in vertices
    }

    def edge_entry(u: int, v: int, coloring) -> Counter:
        group_u, group_v = site_group[u], site_group[v]
        if group_u == group_v:
            return Counter()
        if (group_u, group_v) in blocks:
            left_group, right_group = group_u, group_v
            left_vertex, right_vertex = u, v
        else:
            left_group, right_group = group_v, group_u
            left_vertex, right_vertex = v, u
        pair_index, component = blocks[left_group, right_group]
        return component_entry(
            pair_index,
            component,
            GROUPS[left_group].index(left_vertex),
            coloring[left_vertex],
            GROUPS[right_group].index(right_vertex),
            coloring[right_vertex],
        )

    answer = {}
    for coloring in COLORINGS:
        coefficient = Counter()
        for matching in MATCHINGS:
            term = Counter({(): pfaffian_sign(matching)})
            for u, v in matching:
                term = multiply(term, edge_entry(u, v, coloring))
                if not term:
                    break
            coefficient.update(term)
        answer[coloring] = normalize(coefficient)
    return answer


def flatten(tensor, selected):
    selected = tuple(selected)
    complement = tuple(vertex for vertex in range(N) if vertex not in selected)
    matrix = []
    for left_coloring in itertools.product((0, 1), repeat=len(selected)):
        row = []
        for right_coloring in itertools.product((0, 1), repeat=len(complement)):
            coloring = [0] * N
            for vertex, color in zip(selected, left_coloring):
                coloring[vertex] = color
            for vertex, color in zip(complement, right_coloring):
                coloring[vertex] = color
            row.append(tensor[tuple(coloring)])
        matrix.append(row)
    return matrix


def has_rank_at_most_one(matrix) -> bool:
    pivot = next(
        (
            (row, column)
            for row in range(len(matrix))
            for column in range(len(matrix[0]))
            if matrix[row][column]
        ),
        None,
    )
    if pivot is None:
        return True
    pivot_row, pivot_column = pivot
    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            left = multiply(matrix[row][column], matrix[pivot_row][pivot_column])
            right = multiply(matrix[row][pivot_column], matrix[pivot_row][column])
            if subtract(left, right):
                return False
    return True


def candidate_cuts():
    # A cut and its complement give the same matrix rank, so among triples
    # keep only those containing vertex zero.
    for size in (1, 2):
        yield from itertools.combinations(range(N), size)
    yield from (
        selected
        for selected in itertools.combinations(range(N), 3)
        if 0 in selected
    )


def main() -> None:
    counts = defaultdict(Counter)
    audited = 0
    for component_triple in itertools.product(COMPONENTS, repeat=3):
        tensor = generic_tensor(component_triple)
        witness = next(
            (
                selected
                for selected in candidate_cuts()
                if has_rank_at_most_one(flatten(tensor, selected))
            ),
            None,
        )
        assert witness is not None, component_triple
        counts[component_triple.count("rank1")][len(witness)] += 1
        audited += 1

    assert audited == 125
    assert sum(sum(counter.values()) for counter in counts.values()) == 125
    print("audited all 5^3=125 cross-block component triples over Z")
    for rank_one_blocks in sorted(counts, reverse=True):
        print(
            f"rank-one blocks={rank_one_blocks}: witness-cut sizes "
            f"{dict(sorted(counts[rank_one_blocks].items()))}"
        )
    print("every formal six-site tensor has a nontrivial flattening of rank <= 1")


if __name__ == "__main__":
    main()
