#!/usr/bin/env python3
"""Exact audit of the smallest dense recurrence-cancellation core."""

from __future__ import annotations

from functools import cache
from itertools import combinations


N = 6
FULL = (1 << N) - 1
CORE = sum(1 << vertex for vertex in (0, 1, 2, 3))
EDGES = tuple(combinations(range(N), 2))
WEIGHT = {edge: (-2 if edge == (0, 1) else 1) for edge in EDGES}


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


@cache
def hafnian(mask: int) -> int:
    if mask == 0:
        return 1
    first_bit = mask & -mask
    u = first_bit.bit_length() - 1
    answer = 0
    remainder = mask ^ first_bit
    while remainder:
        next_bit = remainder & -remainder
        v = next_bit.bit_length() - 1
        answer += WEIGHT[edge(u, v)] * hafnian(mask ^ first_bit ^ next_bit)
        remainder ^= next_bit
    return answer


def perfect_matchings(mask: int):
    if mask == 0:
        yield ()
        return
    first_bit = mask & -mask
    u = first_bit.bit_length() - 1
    remainder = mask ^ first_bit
    while remainder:
        next_bit = remainder & -remainder
        v = next_bit.bit_length() - 1
        for tail in perfect_matchings(mask ^ first_bit ^ next_bit):
            yield (edge(u, v),) + tail
        remainder ^= next_bit


def crossing_count(matching, shore: int) -> int:
    return sum(bool(shore >> u & 1) != bool(shore >> v & 1) for u, v in matching)


def main() -> None:
    even_masks = tuple(mask for mask in range(1 << N) if mask.bit_count() % 2 == 0)

    # Directly audit both support implications at every pivot and set.
    for mask in even_masks:
        if mask.bit_count() < 4:
            continue
        for u in range(N):
            if not (mask >> u) & 1:
                continue
            term_count = sum(
                WEIGHT[edge(u, v)] != 0
                and hafnian(mask ^ (1 << u) ^ (1 << v)) != 0
                for v in range(N)
                if v != u and (mask >> v) & 1
            )
            if hafnian(mask) != 0:
                assert term_count >= 1
            else:
                assert term_count != 1

    assert hafnian(0) == 1
    assert hafnian(CORE) == 0
    assert hafnian(FULL) == 6
    assert all(WEIGHT[selected_edge] != 0 for selected_edge in EDGES)
    assert len(tuple(perfect_matchings(CORE))) == 3
    assert len(tuple(perfect_matchings(FULL))) == 15

    # The core's deletion graph is K4: every edge leaves a nonzero pair.
    core_vertices = tuple(vertex for vertex in range(N) if CORE >> vertex & 1)
    deletion_edges = {
        edge(u, v)
        for u, v in combinations(core_vertices, 2)
        if hafnian(CORE ^ (1 << u) ^ (1 << v)) != 0
    }
    assert deletion_edges == set(combinations(core_vertices, 2))
    assert {
        sum(vertex in selected_edge for selected_edge in deletion_edges)
        for vertex in core_vertices
    } == {3}

    # K6 has no nontrivial tight cut.  The only possible nontrivial odd
    # shores are 3-sets, and both one- and three-crossing PMs occur.
    full_matchings = tuple(perfect_matchings(FULL))
    for vertices in combinations(range(N), 3):
        shore = sum(1 << vertex for vertex in vertices)
        assert {crossing_count(matching, shore) for matching in full_matchings} == {1, 3}

    # Split the full hafnian by its crossing number across CORE | {4,5}.
    contribution = {0: 0, 2: 0}
    for matching in full_matchings:
        crossings = crossing_count(matching, CORE)
        term = 1
        for selected_edge in matching:
            term *= WEIGHT[selected_edge]
        contribution[crossings] += term
    assert contribution == {0: 0, 2: 6}

    print(
        "minimal dense recurrence core: haf(core)=0, haf(full)=6, "
        "H(core)=K4, K6 has no nontrivial tight cut: PASS"
    )


if __name__ == "__main__":
    main()
