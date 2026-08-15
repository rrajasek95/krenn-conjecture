#!/usr/bin/env python3
"""Exact-source audit of the tight-C6 rank-two transfer counterguard.

The checker separates three statements which must not be conflated:

1. the literal counterguard from bf8ccd3 has too small a Schmidt image to
   be the ternary GHZ tensor;
2. on a *closed diagonal C6*, the three normalized pure supports force at
   least six mixed debts, and every non-singleton two-colour debt is repaired
   only by one of two explicitly labelled C4 flips; and
3. rank-three matrix factorization alone does not align boundary states with
   the three distinguished GHZ colour lines.

The finite search over all 7^6 nonempty colour supports on the six cycle
edges is exact and uses only the Python standard library.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import permutations, product


N = 6
COLOURS = tuple(range(3))
VERTICES = tuple(range(N))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


MATCHINGS = tuple(sorted(perfect_matchings(VERTICES)))
A_CHANNEL = tuple(sorted((edge(0, 1), edge(2, 3), edge(4, 5))))
B_CHANNEL = tuple(sorted((edge(1, 2), edge(3, 4), edge(0, 5))))
CYCLE_EDGES = A_CHANNEL + B_CHANNEL
CHANNELS = (A_CHANNEL, B_CHANNEL)


def occurrence_cells(matching, word):
    if any(word[left] != word[right] for left, right in matching):
        return None
    return frozenset((endpoints, word[endpoints[0]])
                     for endpoints in matching)


def occurrence_ledger(support):
    answer = {}
    for word in product(COLOURS, repeat=N):
        occurrences = []
        for matching in MATCHINGS:
            cells = occurrence_cells(matching, word)
            if cells is not None and cells <= support:
                occurrences.append((matching, cells))
        if occurrences:
            answer[word] = tuple(occurrences)
    return answer


def cycle_ledger(edge_supports):
    """Decorated words using only the two C6 perfect matchings."""
    answer = Counter()
    for matching in CHANNELS:
        for assignment in product(*(edge_supports[endpoints]
                                    for endpoints in matching)):
            word = [None] * N
            for endpoints, colour in zip(matching, assignment, strict=True):
                for vertex in endpoints:
                    word[vertex] = colour
            answer[tuple(word)] += 1
    return answer


def matrix_rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(rank, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [value / scale for value in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [left - scale * right
                         for left, right in zip(work[row], work[rank],
                                                strict=True)]
        rank += 1
    return rank


def matmul(left, right):
    require(len(left[0]) == len(right), (len(left[0]), len(right)))
    return [[sum(left[row][middle] * right[middle][column]
                 for middle in range(len(right)))
             for column in range(len(right[0]))]
            for row in range(len(left))]


def transpose(matrix):
    return [list(row) for row in zip(*matrix, strict=True)]


def inverse(matrix):
    size = len(matrix)
    work = [
        [Fraction(value) for value in row_values]
        + [Fraction(row == column) for column in range(size)]
        for row, row_values in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(row for row in range(column, size)
                     if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        scale = work[column][column]
        work[column] = [value / scale for value in work[column]]
        for row in range(size):
            if row == column:
                continue
            scale = work[row][column]
            work[row] = [left - scale * right
                         for left, right in zip(work[row], work[column],
                                                strict=True)]
    return [row[size:] for row in work]


def ghz_schmidt_and_alignment_guard():
    shore_words = tuple(product(COLOURS, repeat=3))
    ghz = [[int(left == right and len(set(left)) == 1)
            for right in shore_words] for left in shore_words]
    require(matrix_rank(ghz) == 3, "ternary GHZ Schmidt rank changed")

    # A minimal inner dimension does not align its basis with GHZ colours.
    # In the three-dimensional constant-word subspaces take A=B=S and
    # Q=S^{-1}S^{-T}.  Both boundary bases mix two colour lines, yet
    # A Q B^T=I exactly.
    mixing = [
        [Fraction(1), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(1)],
        [Fraction(1), Fraction(0), Fraction(1)],
    ]
    mixing_inverse = inverse(mixing)
    transfer = matmul(mixing_inverse, transpose(mixing_inverse))
    recovered = matmul(matmul(mixing, transfer), transpose(mixing))
    identity = [[Fraction(row == column) for column in range(3)]
                for row in range(3)]
    require(recovered == identity, (recovered, identity))
    require(all(sum(value != 0 for value in column) == 2
                for column in transpose(mixing)), mixing)
    require(matrix_rank(transfer) == 3, transfer)
    return {
        "ghz_schmidt_rank": 3,
        "mixed_minimal_factorization_rank": matrix_rank(transfer),
        "boundary_column_supports": tuple(
            sum(value != 0 for value in column)
            for column in transpose(mixing)
        ),
    }


def literal_bf8ccd3_guard():
    supports = {
        edge(0, 1): {0}, edge(1, 2): {0},
        edge(2, 3): {0}, edge(0, 5): {0},
        edge(3, 4): {0, 1}, edge(4, 5): {0, 1},
    }
    support = frozenset((endpoints, colour)
                        for endpoints, colours in supports.items()
                        for colour in colours)
    ledger = occurrence_ledger(support)
    pure_counts = tuple(len(ledger.get((colour,) * N, ()))
                        for colour in COLOURS)
    singletons = tuple(word for word, occurrences in ledger.items()
                       if len(set(word)) > 1 and len(occurrences) == 1)
    require(pure_counts == (2, 0, 0), pure_counts)
    require(singletons == ((0, 0, 0, 0, 1, 1),
                           (0, 0, 0, 1, 1, 0)), singletons)

    shore_words = tuple(product(COLOURS, repeat=3))
    flattening = []
    for left in shore_words:
        row = []
        for right in shore_words:
            row.append(len(ledger.get(left + right, ())))
        flattening.append(row)
    require(matrix_rank(flattening) == 1, matrix_rank(flattening))

    # Polynomially the two tight-cut occurrences retain different labelled
    # shore cofactors q01 and q12.  Their occurrence module has rank two even
    # though the evaluated word flattening above has rank one.
    boundary_states = ((edge(2, 3), edge(0, 1)),
                       (edge(0, 5), edge(1, 2)))
    require(len({cofactor for _, cofactor in boundary_states}) == 2,
            boundary_states)
    return {
        "pure_multiplicities": pure_counts,
        "mixed_singleton_words": tuple("".join(map(str, word))
                                       for word in singletons),
        "evaluated_schmidt_rank": 1,
        "labelled_boundary_cofactor_rank": 2,
    }


def channel_pure_colours(edge_supports, channel):
    return frozenset.intersection(*(edge_supports[endpoints]
                                    for endpoints in channel))


def word_from_channel(channel, assignment):
    word = [None] * N
    for endpoints, colour in zip(channel, assignment, strict=True):
        for vertex in endpoints:
            word[vertex] = colour
    return tuple(word)


def compatible_matchings(word):
    return tuple(matching for matching in MATCHINGS
                 if occurrence_cells(matching, word) is not None)


def check_two_colour_debt(word, core_matching, support):
    counts = Counter(word)
    require(sorted(counts.values()) == [2, 4], (word, counts))
    minority = next(colour for colour, count in counts.items() if count == 2)
    minority_vertices = tuple(vertex for vertex, colour in enumerate(word)
                              if colour == minority)
    minority_edge = edge(*minority_vertices)
    compatible = compatible_matchings(word)
    require(len(compatible) == 3, (word, compatible))
    require(all(minority_edge in matching for matching in compatible),
            (word, minority_edge, compatible))
    require(core_matching in compatible, (word, core_matching, compatible))
    alternatives = tuple(matching for matching in compatible
                         if matching != core_matching)
    live_alternatives = []
    missing_cell_sets = []
    for matching in alternatives:
        cells = occurrence_cells(matching, word)
        missing = cells - support
        # The minority pair is retained.  Relative to the core occurrence,
        # each alternative changes exactly the other two matching edges: a
        # primitive C4 flip on the four majority-colour vertices.
        require(len(set(matching) ^ set(core_matching)) == 4,
                (word, core_matching, matching))
        require(minority_edge in set(matching) & set(core_matching),
                (word, minority_edge, core_matching, matching))
        missing_cell_sets.append(frozenset(missing))
        if not missing:
            live_alternatives.append(matching)
    return tuple(alternatives), tuple(missing_cell_sets), tuple(live_alternatives)


def exhaustive_closed_c6_audit():
    nonempty_subsets = tuple(
        frozenset(colour for colour in COLOURS if mask & (1 << colour))
        for mask in range(1, 1 << len(COLOURS))
    )
    pure_supported_count = 0
    singleton_histogram = Counter()
    minimum_singletons = None
    minimizers = []

    for support_tuple in product(nonempty_subsets, repeat=len(CYCLE_EDGES)):
        edge_supports = dict(zip(CYCLE_EDGES, support_tuple, strict=True))
        ledger = cycle_ledger(edge_supports)
        pure_words = tuple((colour,) * N for colour in COLOURS)
        pure_count = sum(word in ledger for word in pure_words)
        mixed_singletons = tuple(
            word for word, multiplicity in ledger.items()
            if len(set(word)) > 1 and multiplicity == 1
        )

        # The union of A and B is connected.  Hence a word compatible with
        # both matchings is constant, so every mixed cycle occurrence is a
        # literal singleton inside the closed component.
        require(all(multiplicity == 1
                    for word, multiplicity in ledger.items()
                    if len(set(word)) > 1), (support_tuple, ledger))
        if not mixed_singletons:
            require(pure_count <= 2, (support_tuple, pure_count))

        if pure_count != 3:
            continue
        pure_supported_count += 1
        singleton_count = len(mixed_singletons)
        singleton_histogram[singleton_count] += 1
        if minimum_singletons is None or singleton_count < minimum_singletons:
            minimum_singletons = singleton_count
            minimizers = [support_tuple]
        elif singleton_count == minimum_singletons:
            minimizers.append(support_tuple)

        channel_colours = tuple(channel_pure_colours(edge_supports, channel)
                                for channel in CHANNELS)
        require(set().union(*channel_colours) == set(COLOURS),
                (support_tuple, channel_colours))
        selected = max(range(2), key=lambda index: len(channel_colours[index]))
        colours = tuple(sorted(channel_colours[selected]))
        require(len(colours) >= 2, (support_tuple, channel_colours))
        channel = CHANNELS[selected]
        support = frozenset((endpoints, colour)
                            for endpoints, values in edge_supports.items()
                            for colour in values)
        if len(colours) == 3:
            # Each permutation of 0,1,2 gives a 2+2+2 word.  Even the full
            # K6 contains only its three forced same-colour pair edges.
            for assignment in permutations(colours):
                word = word_from_channel(channel, assignment)
                require(compatible_matchings(word) == (channel,),
                        (support_tuple, word, compatible_matchings(word)))
        else:
            first, second = colours[:2]
            assignments = tuple(assignment
                                for assignment in product((first, second),
                                                          repeat=3)
                                if len(set(assignment)) == 2)
            require(len(assignments) == 6, assignments)
            for assignment in assignments:
                word = word_from_channel(channel, assignment)
                alternatives, _, live = check_two_colour_debt(
                    word, channel, support
                )
                # A full exact source must either retain the singleton or
                # activate at least one of these two crossed C4 alternatives.
                require(len(alternatives) == 2, alternatives)
                if ledger[word] == 1:
                    require(not live, (support_tuple, word, live))

    require(pure_supported_count == 3037, pure_supported_count)
    require(minimum_singletons == 6, minimum_singletons)
    require(len(minimizers) == 6, len(minimizers))
    require(sum(singleton_histogram.values()) == pure_supported_count,
            singleton_histogram)

    # The six sharp supports form one D12 x S3 orbit.  A canonical member
    # puts one colour on all A edges and the other two on all B edges.
    canonical = (
        frozenset((0,)), frozenset((0,)), frozenset((0,)),
        frozenset((1, 2)), frozenset((1, 2)), frozenset((1, 2)),
    )
    require(canonical in minimizers, minimizers)
    dihedral = tuple(dict.fromkeys(
        tuple((vertex + shift) % N for vertex in VERTICES)
        for shift in range(N)
    )) + tuple(dict.fromkeys(
        tuple((shift - vertex) % N for vertex in VERTICES)
        for shift in range(N)
    ))
    orbit = set()
    canonical_supports = dict(zip(CYCLE_EDGES, canonical, strict=True))
    for vertex_permutation in dihedral:
        for colour_permutation in permutations(COLOURS):
            transformed = {}
            for endpoints, colours in canonical_supports.items():
                image = edge(vertex_permutation[endpoints[0]],
                             vertex_permutation[endpoints[1]])
                transformed[image] = frozenset(
                    colour_permutation[colour] for colour in colours
                )
            orbit.add(tuple(transformed[endpoints]
                            for endpoints in CYCLE_EDGES))
    require(set(minimizers) <= orbit and len(orbit) == 6,
            (len(orbit), len(minimizers)))
    return {
        "cycle_supports_checked": len(nonempty_subsets) ** len(CYCLE_EDGES),
        "three_pure_supports": pure_supported_count,
        "minimum_mixed_singletons": minimum_singletons,
        "sharp_supports": len(minimizers),
        "sharp_orbits_D12xS3": 1,
        "singleton_histogram": tuple(sorted(singleton_histogram.items())),
    }, canonical


def canonical_first_repair_layer(canonical):
    edge_supports = dict(zip(CYCLE_EDGES, canonical, strict=True))
    support = frozenset((endpoints, colour)
                        for endpoints, colours in edge_supports.items()
                        for colour in colours)
    ledger = occurrence_ledger(support)
    debts = tuple(sorted(word for word, occurrences in ledger.items()
                         if len(set(word)) > 1 and len(occurrences) == 1))
    expected_debts = (
        (1, 1, 1, 2, 2, 1), (1, 2, 2, 1, 1, 1),
        (1, 2, 2, 2, 2, 1), (2, 1, 1, 1, 1, 2),
        (2, 1, 1, 2, 2, 2), (2, 2, 2, 1, 1, 2),
    )
    require(debts == expected_debts, debts)

    repair_options = []
    labelled_options = []
    for word in debts:
        core_matching, _ = ledger[word][0]
        alternatives, missing, live = check_two_colour_debt(
            word, core_matching, support
        )
        require(not live and len(alternatives) == len(missing) == 2,
                (word, alternatives, missing, live))
        require(all(len(cells) == 2 for cells in missing), (word, missing))
        repair_options.append(missing)
        labelled_options.append(tuple(
            tuple(f"{endpoints[0]}{endpoints[1]};{colour}"
                  for endpoints, colour in sorted(cells))
            for cells in missing
        ))

    expected_labelled_options = (
        (("01;1", "25;1"), ("02;1", "15;1")),
        (("03;1", "45;1"), ("04;1", "35;1")),
        (("13;2", "24;2"), ("14;2", "23;2")),
        (("13;1", "24;1"), ("14;1", "23;1")),
        (("03;2", "45;2"), ("04;2", "35;2")),
        (("01;2", "25;2"), ("02;2", "15;2")),
    )
    require(tuple(labelled_options) == expected_labelled_options,
            labelled_options)

    histogram = Counter()
    minimum = None
    best = []
    added_cell_counts = set()
    for choices in product((0, 1), repeat=len(debts)):
        additions = frozenset().union(*(
            repair_options[index][choice]
            for index, choice in enumerate(choices)
        ))
        added_cell_counts.add(len(additions))
        repaired = support | additions
        repaired_ledger = occurrence_ledger(repaired)
        singletons = tuple(sorted(
            word for word, occurrences in repaired_ledger.items()
            if len(set(word)) > 1 and len(occurrences) == 1
        ))
        histogram[len(singletons)] += 1
        if minimum is None or len(singletons) < minimum:
            minimum = len(singletons)
            best = [(choices, additions, singletons)]
        elif len(singletons) == minimum:
            best.append((choices, additions, singletons))
    require(added_cell_counts == {12}, added_cell_counts)
    require(sum(histogram.values()) == 64, histogram)
    require(minimum == 6 and len(best) == 3, (minimum, len(best)))
    require(histogram == Counter({
        6: 3, 8: 6, 10: 6, 15: 8, 17: 12, 18: 1,
        19: 6, 23: 6, 24: 7, 28: 3, 30: 6,
    }), histogram)
    return {
        "initial_debts": tuple("".join(map(str, word)) for word in debts),
        "labelled_mate_pairs": expected_labelled_options,
        "mates_per_debt": 2,
        "cells_per_mate": 2,
        "minimal_repair_choices": 64,
        "new_cells_in_every_choice": 12,
        "minimum_next_layer_singletons": minimum,
        "best_choices": len(best),
        "next_singleton_histogram": tuple(sorted(histogram.items())),
    }


def main():
    require(len(MATCHINGS) == 15, len(MATCHINGS))
    cycle_matchings = tuple(matching for matching in MATCHINGS
                            if set(matching) <= set(CYCLE_EDGES))
    require(cycle_matchings == CHANNELS, cycle_matchings)

    schmidt = ghz_schmidt_and_alignment_guard()
    literal = literal_bf8ccd3_guard()
    exhaustive, canonical = exhaustive_closed_c6_audit()
    repairs = canonical_first_repair_layer(canonical)
    print("uniform terminal-C6 rank-two exact-source exit: PASS")
    print("Schmidt/alignment audit", schmidt)
    print("bf8ccd3 literal guard", literal)
    print("closed C6 support theorem", exhaustive)
    print("canonical first repair layer", repairs)
    print("terminal criterion: rank-one common tail, or explicit C4/outside exit")


if __name__ == "__main__":
    main()
