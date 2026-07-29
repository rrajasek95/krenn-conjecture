#!/usr/bin/env python3
"""Exact audit of minimum direct repairs of the n=8 border seed.

The seed and colour convention are exactly those of equations (3)--(5) in
``notes/n8-counterexample-recon.md``.  A *direct repair* chooses a distinct
perfect matching in each of the two singleton mixed fibres and adjoins every
decorated cell missing from the seed.  The calculation is purely finite: it
enumerates all 105 perfect matchings and every supported output fibre.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import permutations, product


N = 8
Q = 3


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


MATCHINGS = tuple(perfect_matchings(range(N)))
TARGET_MATCHINGS = (
    ((0, 2), (1, 4), (3, 6), (5, 7)),
    ((0, 3), (1, 5), (2, 4), (6, 7)),
    ((0, 1), (2, 3), (4, 7), (5, 6)),
)
SEED = frozenset(
    (u, v, colour, colour)
    for colour, matching in enumerate(TARGET_MATCHINGS)
    for u, v in matching
)

# A lexicographically first minimum direct repair having the minimum possible
# number (four) of newly-created singleton fibres.
MINIMUM_REPAIR = frozenset({
    (0, 2, 2, 1),
    (1, 4, 2, 1),
    (1, 7, 1, 2),
    (4, 5, 2, 1),
})

# The orbit-8 boundary from ``n8-orbit8-pairwise-boundary-repair.md``,
# transported to the vertex labels used here, followed by the two-cell
# minimum mate of the two singletons created by adjoining MINIMUM_REPAIR.
TRANSPORTED_BOUNDARY_EXTRA = frozenset({
    (0, 1, 2, 1), (0, 4, 2, 1), (0, 4, 2, 2),
    (1, 2, 1, 1), (1, 2, 2, 1), (1, 5, 2, 1),
    (1, 7, 1, 2), (1, 7, 2, 2), (2, 4, 1, 2),
    (4, 5, 1, 1), (4, 5, 2, 1), (4, 7, 1, 2),
})
STRUCTURED_BASE = (
    SEED | MINIMUM_REPAIR | TRANSPORTED_BOUNDARY_EXTRA
    | {(3, 5, 0, 0), (6, 7, 0, 0)}
)
NO_SINGLETON_32_EXTRA = frozenset({
    (3, 6, 0, 1), (5, 7, 0, 1),
    (6, 7, 0, 1), (6, 7, 1, 0),
})


def image_cell(cell, vertex_permutation, colour_permutation):
    u, v, a, b = cell
    image_u, image_v = vertex_permutation[u], vertex_permutation[v]
    image_a, image_b = colour_permutation[a], colour_permutation[b]
    if image_u < image_v:
        return image_u, image_v, image_a, image_b
    return image_v, image_u, image_b, image_a


def image_support(support, vertex_permutation, colour_permutation):
    return frozenset(
        image_cell(cell, vertex_permutation, colour_permutation)
        for cell in support
    )


def decorated_term(colouring, matching):
    return tuple(
        (u, v, colouring[u], colouring[v]) for u, v in matching
    )


def supported_fibres(support):
    """Enumerate all supported terms, grouped by their output colouring."""

    cells_by_edge = defaultdict(list)
    for u, v, a, b in support:
        cells_by_edge[u, v].append((a, b))

    fibres = defaultdict(list)
    for matching_number, matching in enumerate(MATCHINGS):
        choices = [cells_by_edge[edge] for edge in matching]
        if any(not edge_choices for edge_choices in choices):
            continue
        for endpoint_colours in product(*choices):
            colouring = [None] * N
            decorated = []
            for (u, v), (a, b) in zip(matching, endpoint_colours):
                colouring[u] = a
                colouring[v] = b
                decorated.append((u, v, a, b))
            fibres[tuple(colouring)].append(
                (matching_number, tuple(decorated))
            )
    return fibres


def mixed_histogram(fibres):
    return Counter(
        len(terms)
        for colouring, terms in fibres.items()
        if len(set(colouring)) > 1
    )


def coefficient_table(support, weights):
    answer = {}
    for colouring, terms in supported_fibres(support).items():
        coefficient = sum(
            product_weight(weights, decorated)
            for _matching_number, decorated in terms
        )
        if coefficient:
            answer[colouring] = coefficient
    return answer


def product_weight(weights, decorated):
    answer = 1
    for cell in decorated:
        answer *= weights[cell]
    return answer


def laurent_seed_table():
    """Return exact Laurent-polynomial coefficients as exponent counters."""

    exponent = {cell: 0 for cell in SEED}
    exponent[(3, 6, 0, 0)] = 1
    exponent[(1, 4, 0, 0)] = -1
    table = {}
    for colouring, terms in supported_fibres(SEED).items():
        polynomial = Counter(
            sum(exponent[cell] for cell in decorated)
            for _matching_number, decorated in terms
        )
        table[colouring] = polynomial
    return table


def main():
    assert len(MATCHINGS) == 105
    assert len(SEED) == 12

    # Recheck equations (3)--(5), including all unlisted output fibres.
    laurent = laurent_seed_table()
    expected = {
        (0,) * N: Counter({0: 1}),
        (1,) * N: Counter({0: 1}),
        (2,) * N: Counter({0: 1}),
        (2, 2, 1, 0, 1, 0, 0, 0): Counter({1: 1}),
        (0, 1, 0, 0, 2, 1, 0, 2): Counter({1: 1}),
    }
    assert laurent == expected

    seed_fibres = supported_fibres(SEED)
    singleton_fibres = [
        (colouring, terms[0])
        for colouring, terms in seed_fibres.items()
        if len(set(colouring)) > 1 and len(terms) == 1
    ]
    assert {colouring for colouring, _term in singleton_fibres} == {
        (2, 2, 1, 0, 1, 0, 0, 0),
        (0, 1, 0, 0, 2, 1, 0, 2),
    }

    # For each singleton, list the missing-cell set of every possible mate.
    mate_options = []
    for colouring, (trigger_number, _trigger) in singleton_fibres:
        options = []
        for matching_number, matching in enumerate(MATCHINGS):
            if matching_number == trigger_number:
                continue
            decorated = decorated_term(colouring, matching)
            options.append(
                (matching_number, frozenset(decorated) - SEED)
            )
        assert Counter(len(missing) for _number, missing in options) == {
            2: 12,
            3: 32,
            4: 60,
        }
        mate_options.append(options)

    # Exhaust all 104^2 pairs, rather than assuming separately-minimum mates
    # remain jointly minimum.
    minimum_added = min(
        len(left_missing | right_missing)
        for (_left_number, left_missing), (_right_number, right_missing)
        in product(*mate_options)
    )
    minimum_supports = {
        left_missing | right_missing
        for (_left_number, left_missing), (_right_number, right_missing)
        in product(*mate_options)
        if len(left_missing | right_missing) == minimum_added
    }
    assert minimum_added == 4
    assert len(minimum_supports) == 144

    # Every minimum direct repair creates fresh singleton mixed fibres.  The
    # complete distribution is a compact, independently reproducible audit.
    new_singleton_distribution = Counter()
    for added in minimum_supports:
        fibres = supported_fibres(SEED | added)
        new_singleton_distribution[mixed_histogram(fibres)[1]] += 1
    assert new_singleton_distribution == {
        4: 8,
        5: 20,
        6: 75,
        7: 13,
        8: 20,
        9: 8,
    }

    # The displayed minimum repair really cancels every binomial fibre with
    # rational signs and keeps all three pure coefficients normalized.  Its
    # only failures are the four unavoidable nonzero singleton coefficients.
    repair_support = SEED | MINIMUM_REPAIR
    repair_fibres = supported_fibres(repair_support)
    assert mixed_histogram(repair_fibres) == {1: 4, 2: 3}
    weights = {cell: 1 for cell in repair_support}
    weights[(0, 2, 2, 1)] = -1
    weights[(1, 7, 1, 2)] = -1
    coefficients = coefficient_table(repair_support, weights)
    target = {(colour,) * N: 1 for colour in range(Q)}
    residual = {
        colouring: coefficient
        for colouring, coefficient in coefficients.items()
        if colouring not in target
    }
    assert all(coefficients[colouring] == value for colouring, value in target.items())
    assert residual == {
        (0, 2, 0, 0, 1, 0, 0, 0): 1,
        (1, 1, 1, 1, 1, 2, 2, 2): -1,
        (2, 0, 1, 0, 0, 0, 0, 0): -1,
        (2, 2, 2, 2, 2, 1, 1, 1): 1,
    }

    # The support has only one nontrivial target-preserving automorphism.  It
    # swaps colours 1 and 2 while permuting vertices; the displayed rational
    # signs break even that involution.
    support_automorphisms = []
    signed_automorphisms = []
    for colour_permutation in permutations(range(Q)):
        for vertex_permutation in permutations(range(N)):
            if image_support(
                repair_support, vertex_permutation, colour_permutation
            ) != repair_support:
                continue
            support_automorphisms.append(
                (vertex_permutation, colour_permutation)
            )
            if all(
                weights[image_cell(
                    cell, vertex_permutation, colour_permutation
                )] == value
                for cell, value in weights.items()
            ):
                signed_automorphisms.append(
                    (vertex_permutation, colour_permutation)
                )
    involution = (
        (2, 4, 0, 3, 1, 7, 6, 5),
        (0, 2, 1),
    )
    assert support_automorphisms == [
        (tuple(range(N)), tuple(range(Q))), involution
    ]
    assert signed_automorphisms == [
        (tuple(range(N)), tuple(range(Q)))
    ]

    # Continue from the four residual singletons.  Dynamic programming over
    # unions of exact mate requirements exhausts all 104^4 choices without
    # assuming that separately smallest mates are jointly optimal.
    residual_singletons = sorted(
        (colouring, terms[0])
        for colouring, terms in repair_fibres.items()
        if len(set(colouring)) > 1 and len(terms) == 1
    )
    assert len(residual_singletons) == 4
    residual_options = []
    for colouring, (trigger_number, _trigger) in residual_singletons:
        options = {
            frozenset(decorated_term(colouring, matching)) - repair_support
            for matching_number, matching in enumerate(MATCHINGS)
            if matching_number != trigger_number
        }
        assert len(options) == 104
        assert Counter(map(len, options)) == {2: 12, 3: 32, 4: 60}
        residual_options.append(options)

    bounded_unions = {}
    for cap in (4, 5, 6):
        states = {frozenset()}
        layer_sizes = []
        for options in residual_options:
            states = {
                state | option
                for state in states
                for option in options
                if len(state | option) <= cap
            }
            layer_sizes.append(len(states))
        bounded_unions[cap] = states, tuple(layer_sizes)
    assert bounded_unions[4][1] == (104, 144, 24, 0)
    assert bounded_unions[5][1] == (104, 912, 88, 0)
    assert bounded_unions[6][1] == (104, 3376, 2284, 288)
    minimum_second_repairs = bounded_unions[6][0]
    assert len(minimum_second_repairs) == 288
    assert all(len(added) == 6 for added in minimum_second_repairs)

    # Quotient the 288 supports by the residual support involution.
    vertex_involution, colour_involution = involution
    seen = set()
    orbits = []
    for added in sorted(
        minimum_second_repairs, key=lambda support: tuple(sorted(support))
    ):
        if added in seen:
            continue
        orbit = {
            added,
            image_support(
                added, vertex_involution, colour_involution
            ),
        }
        assert orbit <= minimum_second_repairs
        seen.update(orbit)
        orbits.append(orbit)
    assert len(orbits) == 144
    assert all(len(orbit) == 2 for orbit in orbits)

    second_singleton_distribution = Counter()
    for added in minimum_second_repairs:
        fibres = supported_fibres(repair_support | added)
        second_singleton_distribution[mixed_histogram(fibres)[1]] += 1
    assert second_singleton_distribution == {
        14: 2, 15: 2, 16: 16, 17: 20, 18: 20, 19: 36,
        20: 50, 21: 54, 22: 30, 23: 22, 24: 12, 25: 10,
        26: 8, 27: 2, 28: 2, 29: 2,
    }

    # A structured closure reaches a genuinely singleton-free 32-cell
    # support.  Its exact binomial subsystem is nevertheless contradictory.
    assert len(STRUCTURED_BASE) == 28
    structured_fibres = supported_fibres(STRUCTURED_BASE)
    assert mixed_histogram(structured_fibres) == {
        1: 3, 2: 35, 3: 1, 4: 3, 6: 1,
    }
    singleton_free_support = STRUCTURED_BASE | NO_SINGLETON_32_EXTRA
    assert len(singleton_free_support) == 32
    singleton_free_fibres = supported_fibres(singleton_free_support)
    assert mixed_histogram(singleton_free_fibres) == {
        2: 65, 4: 12, 6: 4,
    }
    assert tuple(
        len(singleton_free_fibres[(colour,) * N])
        for colour in range(Q)
    ) == (2, 2, 2)

    triangle_colourings = (
        (0, 1, 0, 0, 1, 1, 0, 2),
        (1, 1, 1, 1, 1, 1, 0, 0),
        (1, 1, 1, 1, 1, 2, 2, 2),
    )
    triangle_pairs = []
    for colouring in triangle_colourings:
        terms = singleton_free_fibres[colouring]
        assert len(terms) == 2
        left, right = map(lambda term: frozenset(term[1]), terms)
        common = left & right
        triangle_pairs.append((left - common, right - common))

    expected_triangle_pairs = (
        (
            frozenset({(1, 5, 1, 1), (4, 7, 1, 2)}),
            frozenset({(1, 7, 1, 2), (4, 5, 1, 1)}),
        ),
        (
            frozenset({(1, 2, 1, 1), (4, 5, 1, 1)}),
            frozenset({(1, 5, 1, 1), (2, 4, 1, 1)}),
        ),
        (
            frozenset({(1, 2, 1, 1), (4, 7, 1, 2)}),
            frozenset({(1, 7, 1, 2), (2, 4, 1, 1)}),
        ),
    )
    assert tuple(triangle_pairs) == expected_triangle_pairs

    exponent_differences = []
    for left, right in triangle_pairs:
        difference = Counter(left)
        difference.subtract(right)
        exponent_differences.append(difference)
    relation = Counter(exponent_differences[0])
    relation.update(exponent_differences[1])
    relation.subtract(exponent_differences[2])
    assert not +relation and not -relation
    # Each binomial says its Laurent ratio is -1.  The exponent relation
    # d_1+d_2-d_3=0 would therefore say 1=(-1)(-1)/(-1)=-1.

    print(
        "PASS: seed direct repairs=144, residual automorphisms=2/1, "
        "second direct repairs=288/144 orbits, fresh singletons>=14, "
        "structured singleton-free 32-cell support has odd triangle"
    )


if __name__ == "__main__":
    main()
