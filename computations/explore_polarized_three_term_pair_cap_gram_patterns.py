#!/usr/bin/env python3
"""Explore all normalized three-term polarized supports on eight sites.

Fix the flagged colour-0 perfect matching by vertex symmetry.  Enumerate the
420 flagged perfect matchings for each of colours 1 and 2, retain exactly
the same-colour supports having only the three intended decorated terms,
and test whether the seven-entry two-dimensional Gram obstruction is visible
directly.  Nonzero weights do not change this support census.

This is reconnaissance: failure of the small pattern is not evidence that a
pair-cap solution exists.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, permutations, product
import time


SITES = tuple(range(8))
COLOURS = tuple(range(3))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        mate = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, mate),) + tail


MATCHINGS8 = tuple(perfect_matchings(SITES))
FLAGGED = tuple((matching, edge) for matching in MATCHINGS8 for edge in matching)
MATCHINGS_BY_DELETED_EDGE = {
    edge: tuple(perfect_matchings(tuple(site for site in SITES if site not in edge)))
    for edge in combinations(SITES, 2)
}


def base_stabilizer():
    """The 96 site permutations preserving the fixed flagged colour-0 pair."""
    result = []
    other_pairs = ((2, 3), (4, 5), (6, 7))
    for swap01 in (False, True):
        for pair_order in permutations(range(3)):
            for flips in product((False, True), repeat=3):
                mapping = {0: int(swap01), 1: int(not swap01)}
                for source_index, source_pair in enumerate(other_pairs):
                    target_pair = other_pairs[pair_order[source_index]]
                    if flips[source_index]:
                        target_pair = target_pair[::-1]
                    mapping[source_pair[0]] = target_pair[0]
                    mapping[source_pair[1]] = target_pair[1]
                result.append(tuple(mapping[site] for site in SITES))
    assert len(set(result)) == 96
    return tuple(result)


BASE_STABILIZER = base_stabilizer()


def transform_flagged(flagged, permutation):
    matching, distinguished = flagged
    transformed = tuple(sorted(
        tuple(sorted((permutation[u], permutation[v]))) for u, v in matching
    ))
    transformed_distinguished = tuple(sorted((
        permutation[distinguished[0]], permutation[distinguished[1]]
    )))
    return transformed, transformed_distinguished


def canonical_survivor(flagged1, flagged2):
    records = []
    for permutation in BASE_STABILIZER:
        first = transform_flagged(flagged1, permutation)
        second = transform_flagged(flagged2, permutation)
        records.append((first, second))
        records.append((second, first))
    return min(records)


def q_table(flagged_by_colour):
    table = defaultdict(list)
    cells = []
    for colour, (matching, distinguished) in enumerate(flagged_by_colour):
        for edge in matching:
            if edge == distinguished:
                continue
            table[edge].append(colour)
            cells.append((edge[0], edge[1], colour))
    return {edge: tuple(values) for edge, values in table.items()}, tuple(cells)


def unique_pure_completion(q_by_edge, distinguished, colour):
    found = []
    for matching in MATCHINGS_BY_DELETED_EDGE[distinguished]:
        options = tuple(q_by_edge.get(edge, ()) for edge in matching)
        for colours in product(*options):
            found.append((matching, colours))
            if len(found) > 1:
                return False
    return len(found) == 1 and found[0][1] == (colour, colour, colour)


def exact_polarized(flagged_by_colour, q_by_edge):
    return all(
        unique_pure_completion(q_by_edge, distinguished, colour)
        for colour, (_, distinguished) in enumerate(flagged_by_colour)
    )


def disjoint(cells):
    endpoints = [site for i, j, _ in cells for site in (i, j)]
    return len(endpoints) == len(set(endpoints))


def word_data(q_cells):
    word_map = defaultdict(list)
    for cells in combinations(q_cells, 3):
        if not disjoint(cells):
            continue
        used = {site for i, j, _ in cells for site in (i, j)}
        u, v = tuple(sorted(set(SITES) - used))
        fixed = {site: colour for i, j, colour in cells for site in (i, j)}
        for colour_u, colour_v in product(COLOURS, repeat=2):
            word = tuple(
                colour_u if site == u else
                colour_v if site == v else
                fixed[site]
                for site in SITES
            )
            word_map[word].append(((u, colour_u), (v, colour_v)))

    q_four = Counter()
    for cells in combinations(q_cells, 4):
        if not disjoint(cells):
            continue
        word = [None] * 8
        for i, j, colour in cells:
            word[i] = word[j] = colour
        q_four[tuple(word)] += 1
    return dict(word_map), q_four


def gram_pattern(flagged_by_colour, word_map, q_four):
    pure_variables = []
    for colour, (_, distinguished) in enumerate(flagged_by_colour):
        pure = (colour,) * 8
        contributors = word_map.get(pure, ())
        expected = ((distinguished[0], colour), (distinguished[1], colour))
        if len(contributors) != 1 or contributors[0] != expected or q_four[pure]:
            return False
        pure_variables.append(expected)

    forced_zero = set()
    for word, contributors in word_map.items():
        if len(contributors) != 1 or q_four[word] or word in {
            (0,) * 8, (1,) * 8, (2,) * 8
        }:
            continue
        forced_zero.add(contributors[0])

    # AB, CD, EF are the three nonzero pure Gram entries.  Try both
    # orientations of each physical edge and the contradiction pattern
    # AF=BF=AC=CF=0.
    for swaps in product((False, True), repeat=3):
        oriented = []
        for pair, swap in zip(pure_variables, swaps):
            oriented.append(pair[::-1] if swap else pair)
        (a, b), (c, _d), (_e, f) = oriented
        required = ((a, f), (b, f), (a, c), (c, f))
        normalized = tuple(
            pair if pair[0][0] < pair[1][0] else pair[::-1]
            for pair in required
        )
        if all(pair in forced_zero for pair in normalized):
            return True
    return False


def six_mode_zero_contradiction(flagged_by_colour, word_map, q_four):
    """Test the closure of zero orthogonality on the six pure endpoint modes."""
    pure_edges = []
    modes = []
    for colour, (_, distinguished) in enumerate(flagged_by_colour):
        pure = (colour,) * 8
        contributors = word_map.get(pure, ())
        expected = ((distinguished[0], colour), (distinguished[1], colour))
        if len(contributors) != 1 or contributors[0] != expected or q_four[pure]:
            return False
        pure_edges.append(expected)
        modes.extend(expected)
    assert len(set(modes)) == 6
    index = {mode: position for position, mode in enumerate(modes)}

    forced_zero = set()
    for word, contributors in word_map.items():
        if len(contributors) != 1 or q_four[word] or word in {
            (0,) * 8, (1,) * 8, (2,) * 8
        }:
            continue
        left, right = contributors[0]
        if left in index and right in index:
            forced_zero.add(tuple(sorted((index[left], index[right]))))
    required = {
        tuple(sorted((index[left], index[right]))) for left, right in pure_edges
    }

    parent = list(range(6))

    def find(value):
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    def union(left, right):
        left, right = find(left), find(right)
        if left == right:
            return False
        parent[right] = left
        return True

    changed = True
    while changed:
        changed = False
        # Every nonzero vector has a one-dimensional orthogonal complement,
        # so all of its nonzero zero-neighbours are proportional.
        for vertex in range(6):
            neighbours = []
            for left, right in forced_zero:
                if find(left) == find(vertex):
                    neighbours.append(right)
                if find(right) == find(vertex):
                    neighbours.append(left)
            if neighbours:
                first = neighbours[0]
                for other in neighbours[1:]:
                    changed |= union(first, other)

        # An internal zero makes a proportionality class isotropic; its
        # orthogonal complement is then itself.
        isotropic = set()
        for left, right in forced_zero:
            if find(left) == find(right):
                isotropic.add(find(left))
        for left, right in forced_zero:
            if find(left) in isotropic:
                changed |= union(left, right)
            if find(right) in isotropic:
                changed |= union(left, right)

    for edge in required:
        if edge in forced_zero:
            return True
        left, right = edge
        if find(left) == find(right):
            # The class is forbidden to be isotropic by this nonzero entry.
            if any(
                find(zero_left) == find(left) == find(zero_right)
                for zero_left, zero_right in forced_zero
            ):
                return True

    # Distinct proportionality classes cannot be simultaneously orthogonal
    # and required nonorthogonal.
    zero_class_pairs = {
        tuple(sorted((find(left), find(right)))) for left, right in forced_zero
    }
    for left, right in required:
        if tuple(sorted((find(left), find(right)))) in zero_class_pairs:
            return True
    return False


def main():
    started = time.monotonic()
    base_matching = ((0, 1), (2, 3), (4, 5), (6, 7))
    base = (base_matching, (0, 1))
    exact = 0
    gram = 0
    six_mode_closed = 0
    pure_nonsingleton = 0
    first_survivors = []
    survivor_orbits = Counter()

    for flagged1 in FLAGGED:
        for flagged2 in FLAGGED:
            flagged = (base, flagged1, flagged2)
            q_by_edge, q_cells = q_table(flagged)
            if not exact_polarized(flagged, q_by_edge):
                continue
            exact += 1
            word_map, q_four = word_data(q_cells)
            if any(len(word_map.get((colour,) * 8, ())) != 1 for colour in COLOURS):
                pure_nonsingleton += 1
            if gram_pattern(flagged, word_map, q_four):
                gram += 1
                six_mode_closed += 1
            elif six_mode_zero_contradiction(flagged, word_map, q_four):
                six_mode_closed += 1
            else:
                canonical = canonical_survivor(flagged1, flagged2)
                survivor_orbits[canonical] += 1
                if len(first_survivors) < 20:
                    first_survivors.append((canonical, len(word_map), dict(q_four)))

    assert exact > 0
    assert gram <= exact
    print("normalized weighted three-term support reconnaissance: PASS")
    print(f"flagged pairs scanned: {len(FLAGGED) ** 2}")
    print(f"combinatorially three-term supports: {exact}")
    print(f"pure-word nonsingleton supports: {pure_nonsingleton}")
    print(f"seven-entry Gram certificates: {gram}")
    print(f"all six-mode orthogonality certificates: {six_mode_closed}")
    print(f"uncertified supports: {exact - six_mode_closed}")
    print(f"uncertified stabilizer/colour-swap orbits: {len(survivor_orbits)}")
    print(f"orbit sizes: {Counter(survivor_orbits.values())}")
    print("canonical uncertified records:")
    for record, size in sorted(survivor_orbits.items()):
        print(size, record)
    print(f"wall time: {time.monotonic() - started:.3f}s")


if __name__ == "__main__":
    main()
