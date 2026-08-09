#!/usr/bin/env python3
"""Exact bounded chart-cover facts for three pure N=8 anchor matchings.

The checker classifies triples of pure perfect matchings modulo S_8 x S_3,
audits their target-torus character quotients, and enumerates the mixed
coefficient monomials already created by the anchors.  It also guards the
essential distinction between the diagonal anchor sub-polynomial and a full
endpoint-coloured fibre.  It uses only exact integer/Fraction arithmetic and
exhaustive finite enumeration.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import reduce
from itertools import permutations, product


Q = Fraction
N = 8
COLOURS = range(3)
STANDARD = ((0, 1), (2, 3), (4, 5), (6, 7))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    left = vertices[0]
    for position, right in enumerate(vertices[1:]):
        rest = vertices[1 : position + 1] + vertices[position + 2 :]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((left, right),) + tail))


MATCHINGS = tuple(perfect_matchings(tuple(range(N))))
ALL_CELLS = tuple(
    (left, right, left_colour, right_colour)
    for left in range(N)
    for right in range(left + 1, N)
    for left_colour in COLOURS
    for right_colour in COLOURS
)


def standard_stabilizer():
    answer = []
    for pair_permutation in permutations(range(4)):
        for flips in product(range(2), repeat=4):
            vertex_permutation = [None] * N
            for pair in range(4):
                target = pair_permutation[pair]
                vertex_permutation[2 * pair] = 2 * target + flips[pair]
                vertex_permutation[2 * pair + 1] = 2 * target + 1 - flips[pair]
            answer.append(tuple(vertex_permutation))
    require(len(answer) == 384, "standard matching stabilizer changed")
    return tuple(answer)


STABILIZER = standard_stabilizer()


def matching_image(matching, vertex_permutation):
    return tuple(
        sorted(
            tuple(sorted((vertex_permutation[left], vertex_permutation[right])))
            for left, right in matching
        )
    )


def ordered_key(second, third):
    return min(
        (matching_image(second, permutation), matching_image(third, permutation))
        for permutation in STABILIZER
    )


def maps_to_standard(matching):
    answer = []
    for pair_permutation in permutations(range(4)):
        for flips in product(range(2), repeat=4):
            vertex_permutation = [None] * N
            for pair, (left, right) in enumerate(matching):
                target = pair_permutation[pair]
                vertex_permutation[left] = 2 * target + flips[pair]
                vertex_permutation[right] = 2 * target + 1 - flips[pair]
            answer.append(tuple(vertex_permutation))
    return tuple(answer)


MAPS_TO_STANDARD = {matching: maps_to_standard(matching) for matching in MATCHINGS}


def colour_unordered_key(triple):
    candidates = []
    for colour_permutation in permutations(COLOURS):
        first, second, third = (triple[index] for index in colour_permutation)
        candidates.append(
            min(
                (
                    matching_image(second, vertex_permutation),
                    matching_image(third, vertex_permutation),
                )
                for vertex_permutation in MAPS_TO_STANDARD[first]
            )
        )
    return min(candidates)


def anchor_orbits():
    # Traverse the 384-element stabilizer orbits once instead of reducing all
    # 11,025 pairs separately.
    unseen = {(second, third) for second in MATCHINGS for third in MATCHINGS}
    ordered = set()
    while unseen:
        second, third = min(unseen)
        orbit = {
            (matching_image(second, permutation), matching_image(third, permutation))
            for permutation in STABILIZER
        }
        ordered.add(min(orbit))
        unseen.difference_update(orbit)
    require(len(ordered) == 86, "ordered anchor-orbit count changed")
    representatives = {
        colour_unordered_key((STANDARD, second, third))
        for second, third in ordered
    }
    require(len(representatives) == 31, "S8 x S3 anchor-orbit count changed")
    return tuple(sorted((STANDARD, second, third) for second, third in representatives))


def cell_character(cell):
    left, right, left_colour, right_colour = cell
    vector = [Q(0)] * (3 * N)
    vector[3 * left + left_colour] += 1
    vector[3 * right + right_colour] += 1
    return tuple(vector)


def rational_basis(vectors):
    basis = {}
    for original in vectors:
        vector = list(original)
        for pivot in sorted(basis):
            coefficient = vector[pivot]
            if coefficient:
                vector = [
                    entry - coefficient * basis_entry
                    for entry, basis_entry in zip(vector, basis[pivot])
                ]
        pivot = next((index for index, entry in enumerate(vector) if entry), None)
        if pivot is None:
            continue
        coefficient = vector[pivot]
        basis[pivot] = tuple(entry / coefficient for entry in vector)
    return basis


def quotient_remainder(vector, basis):
    remainder = list(vector)
    for pivot in sorted(basis):
        coefficient = remainder[pivot]
        if coefficient:
            remainder = [
                entry - coefficient * basis_entry
                for entry, basis_entry in zip(remainder, basis[pivot])
            ]
    return tuple(remainder)


def oriented_ray(vector):
    pivot = next((index for index, entry in enumerate(vector) if entry), None)
    if pivot is None:
        return ()
    scale = abs(vector[pivot])
    return tuple(entry / scale for entry in vector)


def add_vectors(*vectors):
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors))


def negate(vector):
    return tuple(-entry for entry in vector)


def anchor_cells(triple):
    return frozenset(
        (left, right, colour, colour)
        for colour, matching in enumerate(triple)
        for left, right in matching
    )


def relative_circuit_census(triple):
    anchors = anchor_cells(triple)
    basis = rational_basis(cell_character(cell) for cell in sorted(anchors))
    require(len(basis) == 12, "pure-anchor character rank changed")
    absent = tuple(cell for cell in ALL_CELLS if cell not in anchors)
    remainders = {
        cell: quotient_remainder(cell_character(cell), basis) for cell in absent
    }
    rays = {oriented_ray(vector) for vector in remainders.values() if any(vector)}
    by_vector = {vector: cell for cell, vector in remainders.items()}
    require(len(by_vector) == len(absent), "relative coordinate characters collided")
    vector_set = frozenset(by_vector)
    vectors = tuple(vector_set)

    sizes = Counter()
    witnesses = {}
    for cell, vector in remainders.items():
        if not any(vector):
            size = 1
            weighted_cells = ((Q(1), cell),)
        elif negate(oriented_ray(vector)) in rays:
            size = 2
            opposite = next(
                candidate
                for candidate in vectors
                if oriented_ray(candidate) == negate(oriented_ray(vector))
            )
            coefficient = -vector[next(index for index, entry in enumerate(vector) if entry)] / opposite[
                next(index for index, entry in enumerate(vector) if entry)
            ]
            require(coefficient > 0, "opposing-ray coefficient is not positive")
            require(
                not any(add_vectors(vector, tuple(coefficient * entry for entry in opposite))),
                "opposing-ray relation failed",
            )
            weighted_cells = ((Q(1), cell), (coefficient, by_vector[opposite]))
        else:
            target = negate(vector)
            size = 99
            weighted_cells = ()
            for left in vectors:
                if not any(left):
                    continue
                right = tuple(target_entry - left_entry for target_entry, left_entry in zip(target, left))
                if any(right) and right in vector_set:
                    size = 3
                    weighted_cells = (
                        (Q(1), cell),
                        (Q(1), by_vector[left]),
                        (Q(1), by_vector[right]),
                    )
                    break
        sizes[size] += 1
        witnesses[cell] = weighted_cells

        # A zero quotient remainder says that the positive extra incidence is
        # constant on the two endpoints of each pure-anchor edge.  Raising the
        # target degree in that colour then gives positive weights on all
        # twelve anchors and an explicit strictly balanced 14/15-cell support.
        incidence = [Q(0)] * (3 * N)
        for coefficient, witness_cell in weighted_cells:
            for index, entry in enumerate(cell_character(witness_cell)):
                incidence[index] += coefficient * entry
        for colour, matching in enumerate(triple):
            endpoint_values = []
            for left, right in matching:
                require(
                    incidence[3 * left + colour] == incidence[3 * right + colour],
                    "relative circuit is not in the anchor span",
                )
                endpoint_values.append(incidence[3 * left + colour])
            target_degree = max(endpoint_values) + 1
            anchor_weights = tuple(target_degree - value for value in endpoint_values)
            require(all(weight > 0 for weight in anchor_weights), "anchor lift is not strict")
    require(99 not in sizes, "a coordinate lacks a three-extra unit circuit")
    require(sum(sizes.values()) == 240, "relative circuit census is incomplete")
    return sizes, witnesses, len(vectors)


def coloured_anchor_matchings(triple):
    colours_by_edge = {}
    for colour, matching in enumerate(triple):
        for edge in matching:
            colours_by_edge.setdefault(edge, []).append(colour)
    records = []
    for matching in MATCHINGS:
        if not all(edge in colours_by_edge for edge in matching):
            continue
        for edge_colours in product(*(colours_by_edge[edge] for edge in matching)):
            colouring = [None] * N
            for (left, right), colour in zip(matching, edge_colours):
                colouring[left] = colour
                colouring[right] = colour
            records.append((matching, tuple(edge_colours), tuple(colouring)))
    require(len({record[2] for record in records}) == len(records), "anchor fibre is not singleton")
    return tuple(records)


def component_sizes(edges, vertex_count=N):
    adjacency = {vertex: set() for vertex in range(vertex_count)}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen = set()
    sizes = []
    for vertex in range(vertex_count):
        if vertex in seen:
            continue
        stack = [vertex]
        seen.add(vertex)
        size = 0
        while stack:
            current = stack.pop()
            size += 1
            for neighbour in adjacency[current]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        sizes.append(size)
    return tuple(sorted(sizes))


def graph_girth(edges, vertex_count):
    adjacency = {vertex: set() for vertex in range(vertex_count)}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    best = vertex_count + 1
    for root in range(vertex_count):
        distance = {root: 0}
        parent = {root: None}
        queue = [root]
        for current in queue:
            for neighbour in adjacency[current]:
                if neighbour not in distance:
                    distance[neighbour] = distance[current] + 1
                    parent[neighbour] = current
                    queue.append(neighbour)
                elif parent[current] != neighbour:
                    best = min(best, distance[current] + distance[neighbour] + 1)
    return best if best <= vertex_count else None


def anchor_graph_signature(triple):
    multiplicities = Counter(edge for matching in triple for edge in matching)
    pair_intersections = tuple(
        sorted(
            len(set(triple[left]) & set(triple[right]))
            for left in COLOURS
            for right in range(left)
        )
    )
    return (
        pair_intersections,
        tuple(sorted(Counter(multiplicities.values()).items())),
        component_sizes(multiplicities),
    )


def fibre_monomials(colouring, support):
    monomials = []
    for matching in MATCHINGS:
        monomial = tuple(
            sorted(
                (left, right, colouring[left], colouring[right])
                for left, right in matching
            )
        )
        if all(cell in support for cell in monomial):
            monomials.append(monomial)
    return tuple(sorted(monomials))


def offdiagonal_cancellation_guard(triple):
    """Freeze a binomial cancellation invisible to the diagonal sub-fibre."""
    colouring = (0, 0, 0, 0, 2, 1, 2, 1)
    anchor_monomial = (
        (0, 1, 0, 0),
        (2, 3, 0, 0),
        (4, 6, 2, 2),
        (5, 7, 1, 1),
    )
    mate_monomial = (
        (0, 4, 0, 2),
        (1, 5, 0, 1),
        (2, 6, 0, 2),
        (3, 7, 0, 1),
    )
    anchors = anchor_cells(triple)
    require(set(anchor_monomial) <= anchors, "sharp anchor monomial changed")
    require(all(cell[2] != cell[3] for cell in mate_monomial), "mate is not off-diagonal")
    support = anchors | frozenset(mate_monomial)

    # A full general endpoint-coloured fibre has one possible cell monomial
    # for each of the 105 physical perfect matchings, not only matchings whose
    # edges stay inside colour classes.
    full_formal_fibre = tuple(
        tuple(
            sorted(
                (left, right, colouring[left], colouring[right])
                for left, right in matching
            )
        )
        for matching in MATCHINGS
    )
    require(len(set(full_formal_fibre)) == 105, "full mixed fibre count changed")
    supported = fibre_monomials(colouring, support)
    require(
        supported == tuple(sorted((anchor_monomial, mate_monomial))),
        "off-diagonal guard fibre is not the expected binomial",
    )

    weights = {cell: Q(1) for cell in support}
    weights[mate_monomial[0]] = Q(-1)
    products = tuple(
        product_value
        for monomial in supported
        for product_value in (
            reduce(
                lambda left, right: left * right,
                (weights[cell] for cell in monomial),
                Q(1),
            ),
        )
    )
    require(products == (Q(1), Q(-1)), "off-diagonal guard weights changed")
    require(sum(products, Q(0)) == 0, "off-diagonal binomial does not cancel")

    # The four mixed cells cannot enter a constant output word, so all three
    # selected pure anchor coefficients remain literal unit monomials.
    for colour in COLOURS:
        pure = fibre_monomials((colour,) * N, support)
        require(len(pure) == 1, "off-diagonal mate changed a pure anchor fibre")
        require(
            reduce(
                lambda left, right: left * right,
                (weights[cell] for cell in pure[0]),
                Q(1),
            )
            == 1,
            "pure anchor product changed",
        )
    return len(full_formal_fibre), len(supported)


def heawood_guard():
    # Incidence graph of the cyclic difference set {0,1,3} in Z/7.  Its
    # three shifts are perfect matchings and its girth is six.
    shifts = (0, 1, 3)
    triple = tuple(
        tuple(tuple(sorted((left, 7 + (left + shift) % 7))) for left in range(7))
        for shift in shifts
    )
    edges = set().union(*(set(matching) for matching in triple))
    require(len(edges) == 21, "Heawood anchor graph lost simplicity")
    require(graph_girth(edges, 14) == 6, "Heawood anchor girth changed")
    pair_cycles = tuple(
        component_sizes(set(triple[left]) | set(triple[right]), 14)
        for left in range(3)
        for right in range(left)
    )
    require(pair_cycles == ((14,), (14,), (14,)), "Heawood two-colour cycles changed")
    return pair_cycles


def high_girth_voltage_guard():
    # An exact 11-fold cyclic cover of the Heawood anchor graph.  The frozen
    # voltages remove every cycle of length 4, 6, or 8.  This is an explicit
    # guard against any uniform pure-anchor extraction of a bounded short
    # overlap: all three two-colour unions are Hamilton cycles on 154 sites.
    modulus = 11
    shifts = (0, 1, 3)
    voltages = (
        6, 5, 1, 5, 4, 2, 0,
        0, 1, 7, 1, 10, 10, 6,
        9, 7, 0, 3, 4, 9, 1,
    )
    triple = []
    for colour, shift in enumerate(shifts):
        matching = []
        for base_left in range(7):
            base_right = (base_left + shift) % 7
            voltage = voltages[7 * colour + base_left]
            for sheet in range(modulus):
                left = modulus * base_left + sheet
                right = 7 * modulus + modulus * base_right + (sheet + voltage) % modulus
                matching.append((left, right))
        triple.append(tuple(matching))
    triple = tuple(triple)
    edges = set().union(*(set(matching) for matching in triple))
    require(all(len(matching) == 77 for matching in triple), "lifted factor size changed")
    require(len(edges) == 231, "lifted anchor graph is not simple")
    require(component_sizes(edges, 154) == (154,), "lifted anchor graph disconnected")
    require(graph_girth(edges, 154) == 10, "lifted anchor girth changed")
    pair_cycles = tuple(
        component_sizes(set(triple[left]) | set(triple[right]), 154)
        for left in range(3)
        for right in range(left)
    )
    require(pair_cycles == ((154,), (154,), (154,)), "lifted two-colour cycles changed")

    # Flip Q0 around one explicit ten-cycle whose non-Q0 half uses both other
    # colours.  This gives a mixed singleton anchor fibre, so the coefficient
    # equations are nonvacuous even on the high-girth guard.
    directed_cycle = (
        (0, 17, 1, 88),
        (17, 28, 1, 106),
        (28, 41, 1, 112),
        (41, 66, 2, 143),
        (66, 0, 1, 83),
    )
    require(
        all(
            (left, right) in triple[colour] and (following, right) in triple[0]
            for left, following, colour, right in directed_cycle
        ),
        "lifted mixed ten-cycle changed",
    )
    removed = {(following, right) for _left, following, _colour, right in directed_cycle}
    added = {(left, right) for left, _following, _colour, right in directed_cycle}
    mixed_matching = (set(triple[0]) - removed) | added
    require(len(mixed_matching) == 77, "lifted mixed matching size changed")
    require(
        Counter(vertex for edge in mixed_matching for vertex in edge) == Counter(range(154)),
        "lifted mixed matching is not perfect",
    )
    colour_partition = Counter({0: 154})
    for _left, _following, colour, _right in directed_cycle:
        colour_partition[0] -= 2
        colour_partition[colour] += 2
    require(colour_partition == Counter({0: 144, 1: 8, 2: 2}), "lifted mixed partition changed")
    return pair_cycles, tuple(sorted(colour_partition.items()))


def main() -> None:
    require(len(MATCHINGS) == 105, "K8 perfect-matching count changed")
    representatives = anchor_orbits()
    signature_histogram = Counter()
    circuit_histogram = Counter()
    mixed_count_histogram = Counter()
    mixed_partition_totals = Counter()
    simple_girths = Counter()
    minimal_mixed_representatives = []

    for triple in representatives:
        signature_histogram[anchor_graph_signature(triple)] += 1
        multiplicities = Counter(edge for matching in triple for edge in matching)
        if len(multiplicities) == 12:
            simple_girths[graph_girth(multiplicities, N)] += 1

        sizes, _witnesses, vector_classes = relative_circuit_census(triple)
        circuit_histogram[(tuple(sorted(sizes.items())), vector_classes)] += 1

        records = coloured_anchor_matchings(triple)
        mixed = [record for record in records if len(set(record[2])) > 1]
        mixed_count_histogram[len(mixed)] += 1
        if len(mixed) == 2:
            minimal_mixed_representatives.append(triple)
        for _matching, _edge_colours, colouring in mixed:
            partition = tuple(
                sorted(
                    (sum(value == colour for value in colouring) for colour in COLOURS),
                    reverse=True,
                )
            )
            require(partition in {(6, 2, 0), (4, 4, 0), (4, 2, 2)}, "mixed partition changed")
            mixed_partition_totals[partition] += 1

    require(len(signature_histogram) == 18, "coarse anchor-signature count changed")
    require(sum(signature_histogram.values()) == 31, "anchor signatures lost an orbit")
    require(simple_girths == Counter({3: 4, 4: 4}), "simple cubic anchor girths changed")
    require(
        circuit_histogram
        == Counter(
            {
                (((2, 216), (3, 24)), 240): 8,
                (((2, 218), (3, 22)), 240): 4,
                (((2, 220), (3, 20)), 240): 6,
                (((2, 222), (3, 18)), 240): 4,
                (((2, 224), (3, 16)), 240): 4,
                (((2, 226), (3, 14)), 240): 1,
                (((2, 228), (3, 12)), 240): 2,
                (((2, 232), (3, 8)), 240): 1,
                (((2, 240),), 240): 1,
            }
        ),
        "relative moment-circuit patterns changed",
    )
    require(
        mixed_count_histogram
        == Counter(
            {
                2: 2, 3: 2, 4: 3, 5: 2, 6: 5, 7: 1, 9: 2, 10: 2,
                11: 1, 12: 2, 14: 1, 15: 1, 21: 1, 22: 2, 24: 2,
                42: 1, 78: 1,
            }
        ),
        "mixed anchor-matching orbit histogram changed",
    )
    require(
        mixed_partition_totals
        == Counter({(6, 2, 0): 162, (4, 4, 0): 110, (4, 2, 2): 132}),
        "mixed anchor partition census changed",
    )
    require(
        minimal_mixed_representatives
        == [
            (
                STANDARD,
                ((0, 2), (1, 3), (4, 6), (5, 7)),
                ((0, 3), (1, 4), (2, 7), (5, 6)),
            ),
            (
                STANDARD,
                ((0, 2), (1, 4), (3, 6), (5, 7)),
                ((0, 3), (1, 5), (2, 7), (4, 6)),
            ),
        ],
        "minimal mixed-fibre anchor representatives changed",
    )
    heawood_cycles = heawood_guard()
    lifted_cycles, lifted_partition = high_girth_voltage_guard()
    offdiagonal_guard = offdiagonal_cancellation_guard(minimal_mixed_representatives[1])

    print("N=8 balanced three-anchor chart cover: PASS (exact)")
    print("anchor orbits: ordered=86, modulo S8 x S3=31, coarse signatures=18")
    print("simple cubic anchor girths:", dict(sorted(simple_girths.items())))
    print("relative moment-circuit patterns:", dict(sorted(circuit_histogram.items(), key=str)))
    print("mixed anchor-matching counts by orbit:", dict(sorted(mixed_count_histogram.items())))
    print("mixed anchor colour partitions:", dict(sorted(mixed_partition_totals.items())))
    print("two minimal mixed-fibre orbits:", minimal_mixed_representatives)
    print("sharp orbit full/supported off-diagonal guard terms:", offdiagonal_guard)
    print("N=14 high-girth guard: Heawood girth=6; two-colour components=", heawood_cycles)
    print(
        "N=154 pure-combinatorial guard: girth=10; two-colour components=",
        lifted_cycles,
        "; mixed anchor partition=",
        lifted_partition,
    )
    print("verdict: moment balance is bounded; no same-colour repair follows in the general model")


if __name__ == "__main__":
    main()
