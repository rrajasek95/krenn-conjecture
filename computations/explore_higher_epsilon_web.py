#!/usr/bin/env python3
"""Exact higher-copy epsilon/web audits for selected-triple replacements.

The first audit gives one choice of two epsilon brackets at every vertex
which both

* has a nonzero coefficient on the square of the decorated Petersen cubic
  monomial in the six-copy matching expansion, and
* evaluates nontrivially on Delta_3.

The second audit gives a six-vertex binomial replacement whose resulting
locally-rainbow cubic occurrence multigraph has a bridge.  No positive
multiple of that state can be decomposed into perfect matchings with uniform
edge multiplicity.

There are only six perfect matchings and 6! source orderings in the first
audit, while the target has 3^6 colour assignments, so all arithmetic is
exact and tiny.
"""

from __future__ import annotations

from itertools import combinations, permutations, product


VERTICES = tuple(range(10))
SELECTED = (
    ((0, 1), (2, 3), (4, 9), (5, 6), (7, 8)),
    ((0, 4), (1, 2), (3, 8), (5, 9), (6, 7)),
    ((0, 5), (1, 6), (2, 7), (3, 4), (8, 9)),
)
FOURTH = ((0, 5), (1, 6), (2, 7), (3, 8), (4, 9))
MATE = ((0, 5), (1, 8), (2, 6), (3, 9), (4, 7))
MIXED_COLORING = (2, 2, 2, 1, 0, 2, 2, 2, 1, 0)


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices, edges):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for i, v in enumerate(vertices[1:], 1):
        e = edge(u, v)
        if e not in edges:
            continue
        rest = vertices[1:i] + vertices[i + 1 :]
        for tail in perfect_matchings(rest, edges):
            yield tuple(sorted((e,) + tail))


def epsilon(word: tuple[int, int, int]) -> int:
    if set(word) != {0, 1, 2}:
        return 0
    inversions = sum(word[i] > word[j] for i in range(3) for j in range(i + 1, 3))
    return -1 if inversions % 2 else 1


def bracket_partitions():
    """The ten unoriented partitions of six slots into two triples."""
    answer = []
    slots = frozenset(range(6))
    for first in combinations(range(1, 6), 2):
        block = (0,) + first
        other = tuple(sorted(slots - set(block)))
        answer.append((block, other))
    assert len(answer) == 10
    return tuple(answer)


PARTITIONS = bracket_partitions()

# Two bracket blocks at vertices 0,...,9.  The integers index PARTITIONS.
# This witness was found by an exhaustive-integer search and is verified from
# scratch below; the verifier itself is deterministic.
PETERSEN_WEB = (6, 4, 6, 3, 1, 3, 1, 4, 4, 3)


def bracket_value(partition, word) -> int:
    return epsilon(tuple(word[i] for i in partition[0])) * epsilon(
        tuple(word[i] for i in partition[1])
    )


def verify_petersen_web() -> None:
    selected_edges = set().union(*(set(m) for m in SELECTED))
    replacement = frozenset(selected_edges - set(FOURTH) | set(MATE))
    matchings = tuple(perfect_matchings(VERTICES, replacement))
    assert len(matchings) == 6

    # Petersen has the exact 2-cover by all six of its perfect matchings.
    for e in replacement:
        assert sum(e in matching for matching in matchings) == 2

    # The all-once multiset is the unique multiset of six Petersen perfect
    # matchings whose incidence vector is twice the all-edge vector.
    multiplicity_solutions = []
    for counts in product(range(7), repeat=6):
        if sum(counts) != 6:
            continue
        if all(
            sum(counts[i] * (e in matchings[i]) for i in range(6)) == 2
            for e in replacement
        ):
            multiplicity_solutions.append(counts)
    assert multiplicity_solutions == [(1, 1, 1, 1, 1, 1)]

    endpoint_label = {}
    for colour, matching in enumerate(SELECTED):
        for u, v in matching:
            endpoint_label[(edge(u, v), u)] = colour
            endpoint_label[(edge(u, v), v)] = colour
    for u, v in MATE:
        e = edge(u, v)
        endpoint_label[(e, u)] = MIXED_COLORING[u]
        endpoint_label[(e, v)] = MIXED_COLORING[v]

    # Only labels on replacement occurrences matter.  Each vertex sees one
    # incident edge of each local colour.
    for v in VERTICES:
        labels = [endpoint_label[(e, v)] for e in replacement if v in e]
        assert sorted(labels) == [0, 1, 2]

    local_words = []
    for v in VERTICES:
        word = []
        for matching in matchings:
            (e,) = tuple(e for e in matching if v in e)
            word.append(endpoint_label[(e, v)])
        assert sorted(word) == [0, 0, 1, 1, 2, 2]
        local_words.append(tuple(word))

    admissible = [
        tuple(i for i, part in enumerate(PARTITIONS) if bracket_value(part, word))
        for word in local_words
    ]
    assert all(options for options in admissible)

    orders = tuple(permutations(range(6)))
    target_words = tuple(product(range(3), repeat=6))
    source_tables = []
    target_tables = []
    for v in VERTICES:
        source_tables.append(
            tuple(
                tuple(
                    bracket_value(PARTITIONS[p], tuple(local_words[v][i] for i in order))
                    for order in orders
                )
                for p in range(10)
            )
        )
        target_tables.append(
            tuple(
                tuple(bracket_value(PARTITIONS[p], word) for word in target_words)
                for p in range(10)
            )
        )

    def values(choice):
        source = sum(
            product_int(source_tables[v][choice[v]][j] for v in VERTICES)
            for j in range(len(orders))
        )
        target = sum(
            product_int(target_tables[v][choice[v]][j] for v in VERTICES)
            for j in range(len(target_words))
        )
        return source, target

    assert all(PETERSEN_WEB[v] in admissible[v] for v in VERTICES)
    source, target = values(PETERSEN_WEB)
    assert source == 2
    assert target == -6

    print("verified Petersen exact two-cover: its six perfect matchings use every edge twice")
    print("verified degree-six local web: Petersen-square coefficient 2, target value -6")


def occurrence_matchings(vertices, occurrences):
    """Perfect matchings of an occurrence multigraph (parallel cells allowed)."""
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for occurrence in occurrences:
        a, b = occurrence[0]
        if u not in (a, b):
            continue
        v = b if u == a else a
        if v not in vertices:
            continue
        rest = tuple(x for x in vertices if x not in (u, v))
        for tail in occurrence_matchings(rest, occurrences):
            yield (occurrence,) + tail


def verify_bridged_replacement() -> None:
    """Audit a binomial selected rewrite whose mate state has a bridge."""
    vertices = tuple(range(6))
    selected = (
        ((0, 4), (1, 2), (3, 5)),
        ((0, 5), (1, 4), (2, 3)),
        ((0, 3), (1, 5), (2, 4)),
    )

    # An occurrence is (underlying pair, left colour, right colour, weight,
    # name), with pair endpoints in increasing order.
    occurrences = []
    selected_by_name = {}
    for colour, matching in enumerate(selected):
        for pair in matching:
            name = f"s{colour}_{pair[0]}{pair[1]}"
            occurrence = (pair, colour, colour, 1, name)
            occurrences.append(occurrence)
            selected_by_name[name] = occurrence

    add_12 = ((1, 2), 2, 1, -1, "a12")
    add_35 = ((3, 5), 1, 2, 1, "a35")
    occurrences.extend((add_12, add_35))

    matchings = tuple(occurrence_matchings(vertices, tuple(occurrences)))

    def term_data(matching):
        colouring = [-1] * len(vertices)
        weight = 1
        for (u, v), left, right, scalar, _name in matching:
            colouring[u], colouring[v] = left, right
            weight *= scalar
        return tuple(colouring), weight, frozenset(o[4] for o in matching)

    fibres = {}
    for matching in matchings:
        colouring, weight, names = term_data(matching)
        fibres.setdefault(colouring, []).append((names, weight))

    for colour in range(3):
        fibre = fibres[(colour,) * 6]
        assert len(fibre) == 1 and fibre[0][1] == 1

    mixed = (0, 2, 1, 1, 0, 2)
    fourth_names = frozenset(("s0_04", "s2_15", "s1_23"))
    mate_names = frozenset(("s0_04", "a12", "a35"))
    assert sorted(fibres[mixed], key=lambda item: sorted(item[0])) == sorted(
        ((fourth_names, 1), (mate_names, -1)), key=lambda item: sorted(item[0])
    )

    # Remove the selected mixed matching and insert its mate.  The six
    # remaining selected occurrences form triangles 0-3-5 and 1-2-4; the
    # shared occurrence 04 is their unique connection and hence a bridge.
    q_names = {
        occurrence[4] for occurrence in occurrences[:9]
    } - set(fourth_names)
    replacement_names = q_names | set(mate_names)
    replacement = tuple(o for o in occurrences if o[4] in replacement_names)
    bridge = selected_by_name["s0_04"]
    without_bridge = tuple(o for o in replacement if o != bridge)

    def components(edges):
        unseen = set(vertices)
        answer = []
        while unseen:
            seed = unseen.pop()
            component = {seed}
            frontier = [seed]
            while frontier:
                u = frontier.pop()
                for (a, b), *_rest in edges:
                    if a == u and b in unseen:
                        unseen.remove(b)
                        component.add(b)
                        frontier.append(b)
                    elif b == u and a in unseen:
                        unseen.remove(a)
                        component.add(a)
                        frontier.append(a)
            answer.append(frozenset(component))
        return tuple(answer)

    assert len(components(replacement)) == 1
    assert set(components(without_bridge)) == {frozenset((0, 3, 5)), frozenset((1, 2, 4))}
    replacement_matchings = tuple(occurrence_matchings(vertices, replacement))
    assert len(replacement_matchings) == 4
    assert all(bridge in matching for matching in replacement_matchings)

    print("verified six-vertex selected mixed fibre: exactly +1 and -1")
    print("verified its replacement occurrence state has a forced bridge in every perfect matching")


def product_int(values) -> int:
    answer = 1
    for value in values:
        answer *= value
        if not answer:
            break
    return answer


if __name__ == "__main__":
    verify_petersen_web()
    verify_bridged_replacement()
