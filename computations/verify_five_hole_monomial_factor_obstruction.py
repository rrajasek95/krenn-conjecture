#!/usr/bin/env python3
"""Audit the coordinate-monomial boundary of the five-hole response.

In local species coordinates the response is the square-free coefficient

    [X Y D Q]_{1^5}.

This checker reconstructs its 90-dimensional linear support, proves that
the directed K_5 cut code governing multiplicity (2,2,1) has minimum
support four over characteristic zero, and exhausts the 6^5 possible local
coordinate permutations of a rank-three diagonal target.
"""

from __future__ import annotations

from itertools import combinations, permutations, product


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


SITES = tuple(range(5))
COLOURS = tuple(range(3))
WORDS = tuple(product(COLOURS, repeat=len(SITES)))
PERMUTATIONS = tuple(permutations(COLOURS))
PRIME = 1_000_003


def response_rows():
    """Return the exact Q-variable support of every response coefficient."""

    edges = tuple(combinations(SITES, 2))
    variables = tuple(
        (edge, left, right)
        for edge in edges
        for left in COLOURS
        for right in COLOURS
    )
    variable_index = {variable: index for index, variable in enumerate(variables)}
    rows = {word: set() for word in WORDS}
    for edge in edges:
        a, b = edge
        complement = tuple(site for site in SITES if site not in edge)
        for assignment in permutations(COLOURS):
            word = [None] * len(SITES)
            for site, colour in zip(complement, assignment, strict=True):
                word[site] = colour
            for left, right in product(COLOURS, repeat=2):
                word[a], word[b] = left, right
                rows[tuple(word)].add(
                    variable_index[edge, left, right]
                )
    require(
        len(variables) == 90,
        "len(variables) == 90",
    )
    return variables, rows


def directed_cut_matrix():
    """Return the 30 by 20 cut-sum map for one (2,2,1) colour type."""

    arcs = tuple((u, v) for u in SITES for v in SITES if u != v)
    arc_index = {arc: index for index, arc in enumerate(arcs)}
    labels = []
    matrix = []
    for singleton in SITES:
        remaining = tuple(site for site in SITES if site != singleton)
        for first_pair in combinations(remaining, 2):
            first = frozenset(first_pair)
            second = frozenset(remaining) - first
            row = [0] * len(arcs)
            for u in first:
                for v in second:
                    row[arc_index[u, v]] = 1
            labels.append((singleton, tuple(sorted(first)), tuple(sorted(second))))
            matrix.append(row)
    require(
        len(matrix) == 30 and len(arcs) == 20,
        "len(matrix) == 30 and len(arcs) == 20",
    )
    return arcs, labels, matrix


def rank_mod_prime(matrix):
    """Exact row rank modulo PRIME for small integer matrices."""

    work = [[value % PRIME for value in row] for row in matrix]
    if not work:
        return 0
    row = 0
    for column in range(len(work[0])):
        pivot = next(
            (candidate for candidate in range(row, len(work))
             if work[candidate][column]),
            None,
        )
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        inverse = pow(work[row][column], PRIME - 2, PRIME)
        work[row] = [(value * inverse) % PRIME for value in work[row]]
        for candidate in range(len(work)):
            if candidate == row or not work[candidate][column]:
                continue
            scale = work[candidate][column]
            work[candidate] = [
                (left - scale * right) % PRIME
                for left, right in zip(work[candidate], work[row], strict=True)
            ]
        row += 1
        if row == len(work):
            break
    return row


def audit_response_decomposition():
    variables, rows = response_rows()
    variable_index = {variable: index for index, variable in enumerate(variables)}

    full_matrix = [
        [int(variable in rows[word]) for variable in range(len(variables))]
        for word in WORDS
    ]
    require(
        rank_mod_prime(full_matrix) == 90,
        "rank_mod_prime(full_matrix) == 90",
    )

    for word, support in rows.items():
        counts = tuple(word.count(colour) for colour in COLOURS)
        if 0 in counts:
            require(
                not support,
                "not support",
            )
            continue
        repeated = [colour for colour, count in enumerate(counts) if count == 3]
        if repeated:
            repeated_colour, = repeated
            singleton_sites = [
                site for site in SITES if word[site] != repeated_colour
            ]
            require(
                len(singleton_sites) == 2,
                "len(singleton_sites) == 2",
            )
            swapped = list(word)
            left, right = singleton_sites
            swapped[left], swapped[right] = swapped[right], swapped[left]
            require(
                rows[tuple(swapped)] == support,
                "rows[tuple(swapped)] == support",
            )
            repeated_sites = [
                site for site in SITES if word[site] == repeated_colour
            ]
            expected = {
                variable_index[
                    tuple(sorted((u, v))), repeated_colour, repeated_colour
                ]
                for u, v in combinations(repeated_sites, 2)
            }
            require(
                support == expected,
                "support == expected",
            )
            continue

        require(
            sorted(counts) == [1, 2, 2],
            "sorted(counts) == [1, 2, 2]",
        )
        singleton_colour = counts.index(1)
        other = tuple(colour for colour in COLOURS if colour != singleton_colour)
        first_sites = [site for site in SITES if word[site] == other[0]]
        second_sites = [site for site in SITES if word[site] == other[1]]
        expected = set()
        for u in first_sites:
            for v in second_sites:
                if u < v:
                    variable = ((u, v), other[0], other[1])
                else:
                    variable = ((v, u), other[1], other[0])
                expected.add(variable_index[variable])
        require(
            support == expected,
            "support == expected",
        )


def audit_cut_code_distance():
    arcs, labels, matrix = directed_cut_matrix()
    require(
        rank_mod_prime(matrix) == 20,
        "rank_mod_prime(matrix) == 20",
    )

    # If a characteristic-zero cut vector had support at most three, pad
    # that support to three rows.  The other 27 rows would annihilate its
    # arc weights.  Every such 27 by 20 matrix has full rank modulo PRIME,
    # hence also over the rationals, forcing all weights to vanish.
    for omitted in combinations(range(len(matrix)), 3):
        omitted = frozenset(omitted)
        retained = [
            row for number, row in enumerate(matrix) if number not in omitted
        ]
        require(
            rank_mod_prime(retained) == 20,
            omitted,
        )

    # The bound is sharp.  This integral directed-edge weighting has four
    # nonzero cut sums, so the exact minimum support is four.
    weights = {
        (0, 1): -1, (0, 2): 1, (0, 3): 1, (0, 4): 1,
        (1, 0): 1, (1, 2): -1, (1, 3): -1, (1, 4): -1,
        (2, 0): 1, (2, 1): 1, (2, 3): -1, (2, 4): -1,
        (3, 0): 1, (3, 1): 1, (3, 2): -1, (3, 4): -1,
        (4, 0): -1, (4, 1): -1, (4, 2): 1, (4, 3): 1,
    }
    values = [
        sum(entry * weights[arc] for entry, arc in zip(row, arcs, strict=True))
        for row in matrix
    ]
    support = tuple(number for number, value in enumerate(values) if value)
    require(
        support == (0, 1, 8, 29),
        "support == (0, 1, 8, 29)",
    )
    require(
        tuple(values[number] for number in support) == (-4, -4, 4, 4),
        "tuple(values[number] for number in support) == (-4, -4, 4...",
    )
    require(
        tuple(labels[number] for number in support) == (
            (0, (1, 2), (3, 4)),
            (0, (1, 3), (2, 4)),
            (1, (0, 4), (2, 3)),
            (4, (2, 3), (0, 1)),
        ),
        "tuple(labels[number] for number in support) == ( (0, (1, ...",
    )


def inverse_permutation(permutation):
    inverse = [None] * len(permutation)
    for source, image in enumerate(permutation):
        inverse[image] = source
    return tuple(inverse)


def audit_all_monomial_targets():
    stages = {"nonsurjective": 0, "three_one_one": 0, "two_two_one": 0}
    for local_permutations in product(PERMUTATIONS, repeat=len(SITES)):
        inverses = tuple(map(inverse_permutation, local_permutations))
        target_words = tuple(
            tuple(inverses[site][colour] for site in SITES)
            for colour in COLOURS
        )
        require(
            all(
                sum(left != right for left, right in zip(target_words[a], target_words[b]))
                == len(SITES)
                for a, b in combinations(COLOURS, 2)
            ),
            "all( sum(left != right for left, right in zip(target_word...",
        )
        multiplicities = tuple(
            tuple(word.count(colour) for colour in COLOURS)
            for word in target_words
        )
        if any(0 in counts for counts in multiplicities):
            # The response has no nonsurjective coefficient at all.
            stages["nonsurjective"] += 1
            continue
        if any(sorted(counts) == [1, 1, 3] for counts in multiplicities):
            # Swapping the two singleton sites gives an equal response
            # coefficient.  It is not another target word, since distinct
            # target words disagree at every site.
            stages["three_one_one"] += 1
            continue
        require(
            all(sorted(counts) == [1, 2, 2] for counts in multiplicities),
            "all(sorted(counts) == [1, 2, 2] for counts in multiplicit...",
        )
        # In each fixed colour-multiplicity block the target has support at
        # most three, whereas a nonzero directed-cut response has support at
        # least four.
        stages["two_two_one"] += 1

    require(
        stages == {
            "nonsurjective": 5316,
            "three_one_one": 1560,
            "two_two_one": 900,
        },
        "stages == { \"nonsurjective\": 5316, \"three_one_one\": 1560,...",
    )
    return stages


def main():
    audit_response_decomposition()
    audit_cut_code_distance()
    stages = audit_all_monomial_targets()
    print(
        "PASS five-hole monomial obstruction: response decomposition exact; "
        "directed-cut minimum support=4; all 7776 local permutation targets "
        f"excluded in stages {stages}"
    )


if __name__ == "__main__":
    main()
