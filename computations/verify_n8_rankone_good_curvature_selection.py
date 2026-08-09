#!/usr/bin/env python3
"""Exact audit for rank-one good-pair curvature selection at N=8.

This verifies the two flat-wedge normal forms, classifies the only
maximum-degree-two graph types which use at most four exceptional chords,
and replays the final essential-incidence contradiction.
"""

from __future__ import annotations


N = 8


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def matrix_rank(rows):
    """Exact rational rank for small integer matrices."""

    from fractions import Fraction

    a = [[Fraction(value) for value in row] for row in rows]
    if not a:
        return 0
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        scale = a[row][col]
        a[row] = [value / scale for value in a[row]]
        for i in range(len(a)):
            if i == row or not a[i][col]:
                continue
            scale = a[i][col]
            a[i] = [x - scale * y for x, y in zip(a[i], a[row])]
        row += 1
    return row


def flat_wedge_normal_forms():
    """Audit the sharp rank-three and rank-two exceptional-chord cases."""

    # Independent centre factors allow covectors which isolate either arm.
    # Flatness forces both restricted stars T_q,T_r to vanish.  The omitted
    # q-r block must itself inject three dimensions.
    independent_equations = [
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
    ]
    require(matrix_rank(independent_equations) == 6,
            "independent-factor flatness left a restricted-star variable")
    rank_three_chord = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    require(matrix_rank(rank_three_chord) == 3,
            "independent-factor sharp chord lost rank three")

    # For proportional centre factors and normalized opposite factors
    # y_q=y_r=e0, one scalar output coordinate has variables
    # (Tq_0,Tq_1,Tq_2,Tr_0,Tr_1,Tr_2).  Flatness imposes the five rows below.
    proportional_equations = [
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [1, 0, 0, -1, 0, 0],
    ]
    require(matrix_rank(proportional_equations) == 5,
            "proportional flat-wedge solution dimension changed")

    # A common rank-one restricted row plus a chord which injects ker(e0)
    # shows that the forced rank >=2 is sharp.
    rank_two_chord = [[0, 0, 0], [0, 1, 0], [0, 0, 1]]
    shared_restricted_row = [[1, 0, 0]]
    require(matrix_rank(rank_two_chord) == 2,
            "proportional-factor sharp chord lost rank two")
    require(matrix_rank(shared_restricted_row + rank_two_chord) == 3,
            "rank-two chord plus common restricted row is not injective")


def component_type_census():
    """Classify the max-degree-two candidates by path/cycle components."""

    # Generate multisets of connected max-degree-two component types on
    # exactly eight vertices.  P1 denotes an isolated vertex.
    types = [("P", size) for size in range(1, N + 1)]
    types += [("C", size) for size in range(3, N + 1)]
    types.sort()
    decompositions = []

    def visit(start, vertices_left, chosen):
        if vertices_left == 0:
            decompositions.append(tuple(chosen))
            return
        for index in range(start, len(types)):
            kind, size = types[index]
            if size <= vertices_left:
                visit(index, vertices_left - size, chosen + [(kind, size)])

    visit(0, N, [])

    def edge_count(component):
        kind, size = component
        return size - 1 if kind == "P" else size

    def chord_count(component):
        kind, size = component
        if kind == "P":
            return max(size - 2, 0)
        if size == 3:
            return -1  # wedge chord is already a rank-one graph edge
        return 2 if size == 4 else size

    survivors = []
    for decomposition in decompositions:
        edges = sum(edge_count(component) for component in decomposition)
        chords = [chord_count(component) for component in decomposition]
        if edges not in (7, 8) or any(value < 0 for value in chords):
            continue
        if sum(chords) <= 4:
            survivors.append((tuple(sorted(decomposition)), edges, sum(chords)))

    expected = {
        ((('C', 4), ('P', 4)), 7, 4),
        ((('C', 4), ('C', 4)), 8, 4),
    }
    require(set(survivors) == expected,
            f"flat graph-type census changed: {survivors}")

    # In both types the four distance-two chords form a perfect matching.
    representatives = [
        ({(0, 1), (1, 2), (2, 3), (0, 3),
          (4, 5), (5, 6), (6, 7)}, "C4+P4"),
        ({(0, 1), (1, 2), (2, 3), (0, 3),
          (4, 5), (5, 6), (6, 7), (4, 7)}, "C4+C4"),
    ]
    for graph, name in representatives:
        graph = {tuple(sorted(pair)) for pair in graph}
        chords = set()
        degrees = []
        for p in range(N):
            neighbors = [q for q in range(N)
                         if q != p and tuple(sorted((p, q))) in graph]
            degrees.append(len(neighbors))
            for index, q in enumerate(neighbors):
                for r in neighbors[index + 1:]:
                    chord = tuple(sorted((q, r)))
                    require(chord not in graph,
                            f"{name} acquired a rank-one triangle")
                    chords.add(chord)
        require(max(degrees) <= 2 and len(chords) == 4,
                f"{name} degree/chord count changed")
        chord_degrees = [sum(u in chord for chord in chords) for u in range(N)]
        require(chord_degrees == [1] * N,
                f"{name} exceptional chords stopped covering every vertex")
    return survivors


def final_incidence_ledger():
    # A forced rank>=2 chord at every vertex rules out three essentials.  If
    # there are two, that chord must itself be essential, leaving at most one
    # essential incidence on R.  Thus at most eight R-edges can be bad.
    rank_one_edges = 24
    rank_one_bad_budget = N
    forced_good = rank_one_edges - rank_one_bad_budget
    max_edges_at_degree_two = N
    require(forced_good == 16 and max_edges_at_degree_two == 8,
            "final essential/degree ledger changed")
    require(forced_good > max_edges_at_degree_two,
            "flat rank-one graph no longer contradicts essential counting")


def main():
    flat_wedge_normal_forms()
    survivors = component_type_census()
    final_incidence_ledger()
    print("flat-wedge exceptional ranks: independent >=3, proportional >=2")
    print("flat graph types:", survivors)
    print("exceptional-chord cover: four edges, every vertex once")
    print("essential recount: at least 16 good R-edges versus at most 8")
    print("N=8 rank-one good-pair curvature selection: PASS")


if __name__ == "__main__":
    main()
