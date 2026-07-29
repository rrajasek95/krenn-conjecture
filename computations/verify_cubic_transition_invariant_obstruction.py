#!/usr/bin/env python3
"""Exact audit for cubic/Penrose invariants under a selected-triple rewrite.

The locally-rainbow prism and Petersen networks are the two terms of the
binomial replacement in ``notes/triple-matching-rewrite.md``.  This script
checks three candidate state multipliers on that exact pair:

* the oriented Penrose contraction (signed proper 3-edge-colourings),
* the perfect-matching two-factor cycle polynomial, and
* the sign character which records colour-mismatched occurrence edges.

The source weights of the two states are 1 and -1.  Hence a state multiplier
can be pulled through this binomial relation only if it has the same value on
the two networks.  All three candidates fail, exactly over the integers.
"""

from __future__ import annotations

from collections import Counter

from verify_triple_matching_rewrite import (
    FOURTH,
    MATE,
    MIXED_COLORING,
    SELECTED,
    VERTICES,
    components,
    perfect_matchings,
)


def epsilon(values: tuple[int, int, int]) -> int:
    """Levi-Civita sign on (0,1,2), and zero on a repetition."""

    if len(set(values)) != 3:
        return 0
    inversions = sum(
        values[i] > values[j]
        for i in range(3)
        for j in range(i + 1, 3)
    )
    return -1 if inversions % 2 else 1


def is_perfect_matching(edges) -> bool:
    degrees = Counter(vertex for edge in edges for vertex in edge)
    return len(edges) == len(VERTICES) // 2 and all(
        degrees[vertex] == 1 for vertex in VERTICES
    )


def oriented_penrose(edges, port_label) -> tuple[int, int]:
    """Return (number of proper edge 3-colourings, signed Penrose sum)."""

    edges = frozenset(edges)
    count = 0
    signed_sum = 0
    for colour_zero in perfect_matchings(VERTICES, edges):
        remainder = edges - set(colour_zero)
        for colour_one in perfect_matchings(VERTICES, remainder):
            colour_two = tuple(sorted(remainder - set(colour_one)))
            if not is_perfect_matching(colour_two):
                continue
            edge_colour = {edge: 0 for edge in colour_zero}
            edge_colour.update({edge: 1 for edge in colour_one})
            edge_colour.update({edge: 2 for edge in colour_two})
            sign = 1
            for vertex in VERTICES:
                incident = sorted(
                    (edge for edge in edges if vertex in edge),
                    key=lambda edge: port_label[(vertex, edge)],
                )
                sign *= epsilon(tuple(edge_colour[edge] for edge in incident))
            assert sign in (-1, 1)
            count += 1
            signed_sum += sign
    return count, signed_sum


def two_factor_signature(edges) -> Counter[tuple[int, ...]]:
    """Coefficient table of sum_M product_{C in G-M} t_|C|."""

    edges = frozenset(edges)
    answer: Counter[tuple[int, ...]] = Counter()
    for matching in perfect_matchings(VERTICES, edges):
        cycle_lengths = tuple(
            sorted(map(len, components(VERTICES, edges - set(matching))))
        )
        answer[cycle_lengths] += 1
    return answer


def edge_character(edges, port_label, matrix) -> int:
    answer = 1
    for edge in edges:
        u, v = edge
        answer *= matrix[port_label[(u, edge)]][port_label[(v, edge)]]
    return answer


def main() -> None:
    prism = frozenset().union(*map(frozenset, SELECTED))
    complement = prism - set(FOURTH)
    petersen = frozenset(complement | set(MATE))

    # The half-edge labels are the selected constant colours.  On a new mate
    # edge, the label at v is the fixed colour MIXED_COLORING[v] of its port.
    prism_labels = {}
    for label, matching in enumerate(SELECTED):
        for edge in matching:
            for vertex in edge:
                prism_labels[(vertex, edge)] = label
    petersen_labels = {
        key: value
        for key, value in prism_labels.items()
        if key[1] in complement
    }
    for edge in MATE:
        for vertex in edge:
            petersen_labels[(vertex, edge)] = MIXED_COLORING[vertex]

    for edges, labels in (
        (prism, prism_labels),
        (petersen, petersen_labels),
    ):
        for vertex in VERTICES:
            incident_labels = {
                labels[(vertex, edge)] for edge in edges if vertex in edge
            }
            assert incident_labels == {0, 1, 2}

    # With the local port order 0,1,2, every proper prism colouring has
    # positive Penrose sign.  Petersen has none.
    assert oriented_penrose(prism, prism_labels) == (30, 30)
    assert oriented_penrose(petersen, petersen_labels) == (0, 0)

    # Thus the length-refined perfect-matching transition polynomials are
    #   prism:   5 t_4 t_6 + 5 t_10 + t_5^2,
    #   Petersen:                              6 t_5^2.
    prism_signature = Counter({(4, 6): 5, (10,): 5, (5, 5): 1})
    petersen_signature = Counter({(5, 5): 6})
    assert two_factor_signature(prism) == prism_signature
    assert two_factor_signature(petersen) == petersen_signature

    # In the one-variable circuit-count specialization this is
    # 6*x^2 + 5*x versus 6*x^2, unequal for every nonzero x over C.
    for x in (1, 2, -1, 7):
        prism_value = sum(count * x ** len(partition) for partition, count in prism_signature.items())
        petersen_value = sum(count * x ** len(partition) for partition, count in petersen_signature.items())
        assert prism_value - petersen_value == 5 * x

    # A tempting cycle-space character gives -1 to a colour-mismatched edge.
    # The prism has no mismatches; the Petersen mate has exactly the three
    # transition types 01, 12, and 20.
    mismatch_sign = tuple(
        tuple(1 if i == j else -1 for j in range(3))
        for i in range(3)
    )
    assert edge_character(prism, prism_labels, mismatch_sign) == 1
    assert edge_character(petersen, petersen_labels, mismatch_sign) == -1

    # Rank-one edge characters are the replacement-neutral ones.  This
    # numerical instance also checks that their value on every locally
    # rainbow state is the same vertex product (a0*a1*a2)^|V|.
    a = (2, 3, 5)
    rank_one = tuple(tuple(a[i] * a[j] for j in range(3)) for i in range(3))
    common_value = (a[0] * a[1] * a[2]) ** len(VERTICES)
    assert edge_character(prism, prism_labels, rank_one) == common_value
    assert edge_character(petersen, petersen_labels, rank_one) == common_value

    # The underlying binomial source relation is W(prism)+W(Petersen)=1-1=0.
    # Weighting it by the three nontrivial candidates destroys cancellation.
    assert 1 - 1 == 0
    assert 1 * 30 + (-1) * 0 == 30
    assert 1 * 1 + (-1) * (-1) == 2

    print("verified oriented Penrose values: prism 30, Petersen 0")
    print("verified cycle polynomials: prism 6*x^2+5*x, Petersen 6*x^2")
    print("verified mismatch sign: prism +1, Petersen -1")
    print("verified rank-one edge characters are equal on both networks")


if __name__ == "__main__":
    main()
