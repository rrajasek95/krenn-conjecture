#!/usr/bin/env python3
"""Exact combinatorial audit of the arbitrary-support rank-one K6 obstruction."""

from __future__ import annotations

from itertools import combinations, permutations


VERTICES = tuple(range(6))
EDGES = tuple(combinations(VERTICES, 2))


def perfect_matchings(vertices=VERTICES):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


MATCHINGS = tuple(perfect_matchings())

K33_FACTORS = (
    ((0, 1), (2, 3), (4, 5)),
    ((0, 2), (1, 4), (3, 5)),
    ((0, 5), (1, 3), (2, 4)),
)
PRISM_FACTORS = (
    ((0, 1), (2, 3), (4, 5)),
    ((0, 2), (1, 4), (3, 5)),
    ((0, 3), (1, 5), (2, 4)),
)


def canonical_coloured_factors(factors):
    images = []
    for vertex_permutation in permutations(VERTICES):
        for colour_permutation in permutations(range(3)):
            image = [None] * 3
            for colour, matching in enumerate(factors):
                mapped = tuple(sorted(
                    tuple(sorted((vertex_permutation[u], vertex_permutation[v])))
                    for u, v in matching
                ))
                image[colour_permutation[colour]] = mapped
            images.append(tuple(image))
    return min(images)


def complement_edges(factors):
    return tuple(sorted(set(EDGES) - set().union(*(set(m) for m in factors))))


def compatible_matchings(factors, colouring, extra_edges):
    pure_colour = {
        edge: colour
        for colour, matching in enumerate(factors)
        for edge in matching
    }
    support = set(pure_colour) | set(extra_edges)
    return tuple(
        matching
        for matching in MATCHINGS
        if all(
            edge in support
            and (
                edge not in pure_colour
                or colouring[edge[0]] == colouring[edge[1]] == pure_colour[edge]
            )
            for edge in matching
        )
    )


def audit_two_orbits():
    triples = []
    for factors in combinations(MATCHINGS, 3):
        if len(set().union(*(set(matching) for matching in factors))) == 9:
            triples.append(factors)
    assert len(triples) == 80

    representatives = {
        canonical_coloured_factors(K33_FACTORS),
        canonical_coloured_factors(PRISM_FACTORS),
    }
    observed = {canonical_coloured_factors(factors) for factors in triples}
    assert observed == representatives


def support_automorphisms(factors):
    """Permutations preserving the three pure matchings, up to colour."""
    factors = tuple(frozenset(matching) for matching in factors)
    complement = complement_edges(factors)
    edge_index = {edge: index for index, edge in enumerate(complement)}
    actions = set()
    for permutation in permutations(VERTICES):
        images = tuple(
            frozenset(
                tuple(sorted((permutation[u], permutation[v])))
                for u, v in matching
            )
            for matching in factors
        )
        if set(images) != set(factors):
            continue
        actions.add(tuple(
            edge_index[tuple(sorted((permutation[u], permutation[v])))]
            for u, v in complement
        ))
    return tuple(sorted(actions))


def orbit(mask, actions):
    return frozenset(
        sum(((mask >> source) & 1) << target for source, target in enumerate(action))
        for action in actions
    )


def mask(indices):
    return sum(1 << index for index in indices)


# (present complementary-edge indices, orbit size, singleton word, singleton PM)
K33_SINGLETON_TABLE = (
    ((), 1, "002121", "01|24|35"),
    ((0,), 6, "002121", "01|24|35"),
    ((0, 1), 6, "002121", "01|24|35"),
    ((0, 2), 9, "000100", "03|12|45"),
    ((0, 1, 2), 18, "000100", "03|12|45"),
    ((2, 3, 4), 2, "002121", "01|24|35"),
    ((0, 1, 2, 3), 9, "000001", "04|15|23"),
    ((0, 2, 3, 4), 6, "000100", "03|12|45"),
    ((0, 1, 2, 3, 4), 6, "000001", "04|15|23"),
    ((0, 1, 2, 3, 4, 5), 1, "000102", "01|25|34"),
)

PRISM_SINGLETON_TABLE = (
    ((), 1, "002121", "01|24|35"),
    ((0,), 6, "002121", "01|24|35"),
    ((0, 1), 6, "002121", "01|24|35"),
    ((0, 2), 3, "000101", "04|12|35"),
    ((1, 2), 6, "002121", "01|24|35"),
    ((0, 1, 2), 12, "000101", "04|12|35"),
    ((0, 1, 4), 6, "002121", "01|24|35"),
    ((0, 3, 4), 2, "000001", "04|13|25"),
    ((0, 1, 2, 3), 3, "000101", "04|12|35"),
    ((0, 1, 2, 4), 6, "000101", "04|12|35"),
    ((0, 1, 3, 4), 6, "000001", "04|13|25"),
    ((0, 1, 2, 3, 4), 6, "000001", "04|13|25"),
)


def parse_word(word):
    return tuple(map(int, word))


def parse_matching(word):
    return tuple(sorted(tuple(sorted(map(int, edge))) for edge in word.split("|")))


def audit_singleton_orbit_table(factors, table, expected_covered):
    complement = complement_edges(factors)
    actions = support_automorphisms(factors)
    covered = set()
    for indices, expected_size, word, matching_word in table:
        representative = mask(indices)
        this_orbit = orbit(representative, actions)
        assert len(this_orbit) == expected_size
        assert covered.isdisjoint(this_orbit)
        covered.update(this_orbit)

        extra_edges = tuple(complement[index] for index in indices)
        colouring = parse_word(word)
        supported = compatible_matchings(factors, colouring, extra_edges)
        assert supported == (parse_matching(matching_word),)
        assert len(set(colouring)) > 1
    assert covered == expected_covered


def audit_sparse_singletons():
    # D_K33=(03,04,12,15,25,34).  Its ten rows cover all 64 subsets.
    audit_singleton_orbit_table(
        K33_FACTORS, K33_SINGLETON_TABLE, set(range(64))
    )
    # D_prism=(04,05,12,13,25,34).  Its twelve rows cover every proper
    # subset.  The sole omitted orbit is the complete six-cycle.
    audit_singleton_orbit_table(
        PRISM_FACTORS, PRISM_SINGLETON_TABLE, set(range(63))
    )


def audit_prism_rectangle():
    P = ((0, 4), (1, 3), (2, 5))
    Q = ((0, 5), (1, 2), (3, 4))
    S = ((0, 1), (2, 5), (3, 4))
    t = (0, 0, 0, 0, 0, 1)
    b = (0, 1, 0, 0, 0, 1)
    d = (1, 0, 0, 0, 0, 0)
    e = (1, 1, 0, 0, 0, 0)

    full_complement = complement_edges(PRISM_FACTORS)
    assert compatible_matchings(PRISM_FACTORS, b, full_complement) == (P, Q)
    assert compatible_matchings(PRISM_FACTORS, d, full_complement) == (P, Q)
    assert compatible_matchings(PRISM_FACTORS, e, full_complement) == (P, Q)
    assert compatible_matchings(PRISM_FACTORS, t, full_complement) == (S, P, Q)
    assert all(len(set(colouring)) > 1 for colouring in (t, b, d, e))

    # This is exactly the exponent identity R(t)R(e)=R(b)R(d): at each
    # vertex the two local colour multisets agree.
    for vertex in VERTICES:
        assert sorted((t[vertex], e[vertex])) == sorted(
            (b[vertex], d[vertex])
        )

    # Three binomial signs force the fourth ratio to be -1. Its two cycle
    # terms cancel and the supported S term remains nonzero.
    ratios = {b: -1, d: -1, e: -1}
    target_ratio = ratios[b] * ratios[d] // ratios[e]
    assert target_ratio == -1
    assert 1 + target_ratio == 0


def main():
    assert len(MATCHINGS) == 15
    audit_two_orbits()
    audit_sparse_singletons()
    audit_prism_rectangle()
    print(
        "PASS: all 128 complementary supports classified; all have a "
        "mixed singleton except the full prism, killed by its four-fibre rectangle"
    )


if __name__ == "__main__":
    main()
