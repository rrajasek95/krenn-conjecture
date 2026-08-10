#!/usr/bin/env python3
"""Classify the minimum binary projections of the N=8 one-bad packet.

On six residual sites audit

    H^[3] = 0,
    p_i s_j H^[2] = delta_ij X_i,  i,j in {0,1}.

Nonzero diagonal coefficients force at least two i-coloured internal cells
and one entry in each of p_i,s_i.  The minimum therefore has four internal
cells and four star entries.  We exhaust its 8,100 labelled channel choices,
find 2,160 coefficient-exact packets in two
S6 x S2(colour) x S2(endpoint) orbits, and replay a rational representative.

An independent direct enumeration of the sharp seven-cell ternary equality
boundary finds 3,960 top-pure supports and 1,440 oriented packets satisfying
both diagonal responses.  They form two source-oriented orbits, and both
off-diagonal rows of every packet contain one private nonzero monomial.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_lemma_e_unary_top_channel_synchronization.py":
        "822c9ff2b0839f3c91fe317218b5ddf4861bd737f912a9b85e9b51e324db243e",
    "computations/verify_shared_reciprocal_two_bad_anchor_safe_retraction.py":
        "a280b40657f2ab02c9c9f6ecf50dd3326db12bcc20614cbbd12bddffac8a1b62",
}
EXPECTED_DIGEST = "fbe288446b472e0d6959afab5f023e6c72b012f80305577873ff94d28d737d8e"

SITES = tuple(range(6))
B, C, A = 0, 1, 2


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def matching_tensor(edges, number, fixed=()):
    """Expand `number` decorated edges plus fixed one-site star entries."""
    answer = Counter()
    for indices in itertools.combinations(range(len(edges)), number):
        chosen = [edges[index] for index in indices]
        occupied = [site for edge, colour in chosen for site in edge]
        occupied += [site for site, colour in fixed]
        if len(occupied) != 6 or len(set(occupied)) != 6:
            continue
        word = [None] * 6
        for edge, colour in chosen:
            for site in edge:
                word[site] = colour
        for site, colour in fixed:
            word[site] = colour
        answer[tuple(word)] += 1
    return answer


def configuration_exact(configuration):
    pb, sb, b_matching, pc, sc, c_matching = configuration
    edges = tuple((edge, B) for edge in b_matching) + tuple(
        (edge, C) for edge in c_matching
    )
    if matching_tensor(edges, 3):
        return False
    for left_colour, left_hole in ((B, pb), (C, pc)):
        for right_colour, right_hole in ((B, sb), (C, sc)):
            actual = (Counter() if left_hole == right_hole else
                      matching_tensor(
                          edges, 2,
                          ((left_hole, left_colour),
                           (right_hole, right_colour)),
                      ))
            expected = Counter({(left_colour,) * 6: 1}) \
                if left_colour == right_colour else Counter()
            if actual != expected:
                return False
    return True


def component_type(configuration):
    edges = configuration[2] + configuration[5]
    adjacency = {site: set() for site in SITES}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen = set()
    sizes = []
    for root in SITES:
        if root in seen:
            continue
        stack = [root]
        seen.add(root)
        size = 0
        while stack:
            site = stack.pop()
            size += 1
            for neighbour in adjacency[site]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        sizes.append(size)
    return tuple(sorted(sizes, reverse=True))


def transform(configuration, permutation, swap_colours, swap_endpoints):
    pb, sb, b_matching, pc, sc, c_matching = configuration

    def edge_map(edge):
        return tuple(sorted((permutation[edge[0]], permutation[edge[1]])))

    pb, sb, pc, sc = (permutation[pb], permutation[sb],
                      permutation[pc], permutation[sc])
    b_matching = tuple(sorted(edge_map(edge) for edge in b_matching))
    c_matching = tuple(sorted(edge_map(edge) for edge in c_matching))
    if swap_colours:
        pb, sb, b_matching, pc, sc, c_matching = (
            pc, sc, c_matching, pb, sb, b_matching
        )
    if swap_endpoints:
        pb, sb, pc, sc = sb, pb, sc, pc
    return pb, sb, b_matching, pc, sc, c_matching


REPRESENTATIVES = (
    (0, 1, ((2, 3), (4, 5)), 1, 2, ((0, 4), (3, 5))),
    (0, 1, ((2, 3), (4, 5)), 2, 4, ((0, 5), (1, 3))),
)


def audit_minimum_orbits():
    configurations = set()
    for pb, sb in itertools.permutations(SITES, 2):
        for b_matching in perfect_matchings(set(SITES) - {pb, sb}):
            for pc, sc in itertools.permutations(SITES, 2):
                for c_matching in perfect_matchings(set(SITES) - {pc, sc}):
                    configuration = (
                        pb, sb, tuple(sorted(b_matching)),
                        pc, sc, tuple(sorted(c_matching)),
                    )
                    if configuration_exact(configuration):
                        configurations.add(configuration)
    require(len(configurations) == 2160,
            f"the minimum binary packet census changed: {len(configurations)}")

    signatures = Counter()
    for configuration in configurations:
        intersection = len(
            {configuration[0], configuration[1]} &
            {configuration[3], configuration[4]}
        )
        signatures[intersection, component_type(configuration)] += 1
    expected_signatures = {
        (1, (5, 1)): 1440,
        (0, (3, 3)): 720,
    }
    require(dict(signatures) == expected_signatures,
            "the two minimum binary signatures changed")

    permutations = tuple(itertools.permutations(SITES))
    orbits = []
    covered = set()
    for representative in REPRESENTATIVES:
        orbit = {
            transform(representative, permutation,
                      swap_colours, swap_endpoints)
            for permutation in permutations
            for swap_colours in (False, True)
            for swap_endpoints in (False, True)
        }
        require(orbit <= configurations,
                "a proposed binary orbit contains a non-packet")
        require(not (covered & orbit), "two binary orbit representatives merged")
        covered |= orbit
        orbits.append(len(orbit))
    require(covered == configurations,
            "the two binary orbits do not cover the exact census")
    require(orbits == [1440, 720],
            "the minimum binary orbit sizes changed")
    return {
        "labelled_channel_choices": 8100,
        "exact_minimum_packets": len(configurations),
        "orbit_count": len(orbits),
        "orbit_sizes": orbits,
        "signature_counts": [
            [intersection, list(components), count]
            for (intersection, components), count
            in sorted(expected_signatures.items())
        ],
        "minimum_internal_cells": 4,
        "minimum_star_entries": 4,
    }, configurations


VALID_SILENT_GUARD = (
    0, 1, ((2, 4), (3, 5)),
    2, 3, ((0, 5), (1, 4)),
)


def audit_valid_guard(configurations):
    require(VALID_SILENT_GUARD in configurations,
            "the rational guard left the exact census")
    pb, sb, b_matching, pc, sc, c_matching = VALID_SILENT_GUARD
    edges = tuple((edge, B) for edge in b_matching) + tuple(
        (edge, C) for edge in c_matching
    )
    require(matching_tensor(edges, 3) == Counter(),
            "the guard H acquired a top matching")
    table = {}
    for left_colour, left_hole in ((B, pb), (C, pc)):
        for right_colour, right_hole in ((B, sb), (C, sc)):
            actual = (Counter() if left_hole == right_hole else
                      matching_tensor(
                          edges, 2,
                          ((left_hole, left_colour),
                           (right_hole, right_colour)),
                      ))
            table[f"{left_colour}{right_colour}"] = [
                [list(word), coefficient]
                for word, coefficient in sorted(actual.items())
            ]
    require(table == {
        "00": [[[0, 0, 0, 0, 0, 0], 1]],
        "01": [], "10": [],
        "11": [[[1, 1, 1, 1, 1, 1], 1]],
    }, "the guard response table changed")
    return {
        "H": ["24:00", "35:00", "05:11", "14:11"],
        "stars": ["p0=e0@0", "s0=e0@1", "p1=e1@2", "s1=e1@3"],
        "H_cubed": 0,
        "response_table": table,
        "hole_intersection": 0,
        "union_components": list(component_type(VALID_SILENT_GUARD)),
        "support": 8,
    }


SHARP_REPRESENTATIVES = (
    (
        ((0, 1), (2, 3), (4, 5)),
        ((0, 2), (1, 4)), (3, 5),
        ((0, 3), (1, 5)), (2, 4),
    ),
    (
        ((0, 1), (2, 3), (4, 5)),
        ((0, 2), (1, 4)), (3, 5),
        ((0, 3), (1, 5)), (4, 2),
    ),
)


def transform_sharp(packet, permutation, swap_colours):
    a_matching, b_matching, b_holes, c_matching, c_holes = packet

    def edge_map(edge):
        return tuple(sorted((permutation[edge[0]], permutation[edge[1]])))

    a_matching = tuple(sorted(edge_map(edge) for edge in a_matching))
    b_matching = tuple(sorted(edge_map(edge) for edge in b_matching))
    c_matching = tuple(sorted(edge_map(edge) for edge in c_matching))
    b_holes = tuple(permutation[site] for site in b_holes)
    c_holes = tuple(permutation[site] for site in c_holes)
    if swap_colours:
        b_matching, b_holes, c_matching, c_holes = (
            c_matching, c_holes, b_matching, b_holes
        )
    return a_matching, b_matching, b_holes, c_matching, c_holes


def audit_sharp_seven_cell_boundary():
    perfect = tuple(perfect_matchings(SITES))
    near = tuple(
        (holes, matching)
        for holes in itertools.combinations(SITES, 2)
        for matching in perfect_matchings(set(SITES) - set(holes))
    )
    require((len(perfect), len(near)) == (15, 45),
            "the six-site perfect/near-perfect census changed")

    top_pure_supports = 0
    diagonal_packets = set()
    for a_matching in perfect:
        for b_hole_set, b_matching in near:
            for c_hole_set, c_matching in near:
                edges = (tuple((edge, A) for edge in a_matching) +
                         tuple((edge, B) for edge in b_matching) +
                         tuple((edge, C) for edge in c_matching))
                if matching_tensor(edges, 3) != Counter({(A,) * 6: 1}):
                    continue
                top_pure_supports += 1
                for b_holes in (b_hole_set, b_hole_set[::-1]):
                    for c_holes in (c_hole_set, c_hole_set[::-1]):
                        b_response = matching_tensor(
                            edges, 2,
                            ((b_holes[0], B), (b_holes[1], B)),
                        )
                        c_response = matching_tensor(
                            edges, 2,
                            ((c_holes[0], C), (c_holes[1], C)),
                        )
                        if (b_response == Counter({(B,) * 6: 1}) and
                                c_response == Counter({(C,) * 6: 1})):
                            diagonal_packets.add((
                                tuple(sorted(a_matching)),
                                tuple(sorted(b_matching)), b_holes,
                                tuple(sorted(c_matching)), c_holes,
                            ))
    require((top_pure_supports, len(diagonal_packets)) == (3960, 1440),
            "the sharp seven-cell top/diagonal census changed")

    for packet in diagonal_packets:
        a_matching, b_matching, b_holes, c_matching, c_holes = packet
        edges = (tuple((edge, A) for edge in a_matching) +
                 tuple((edge, B) for edge in b_matching) +
                 tuple((edge, C) for edge in c_matching))
        bc = matching_tensor(
            edges, 2,
            ((b_holes[0], B), (c_holes[1], C)),
        ) if b_holes[0] != c_holes[1] else Counter()
        cb = matching_tensor(
            edges, 2,
            ((c_holes[0], C), (b_holes[1], B)),
        ) if c_holes[0] != b_holes[1] else Counter()
        require(len(bc) == len(cb) == 1,
                "a sharp packet lost its two private cross monomials")
        require(next(iter(bc.values())) == next(iter(cb.values())) == 1,
                "a private cross coefficient stopped being a unit monomial")

    permutations = tuple(itertools.permutations(SITES))
    covered = set()
    orbit_sizes = []
    for representative in SHARP_REPRESENTATIVES:
        orbit = {
            transform_sharp(representative, permutation, swap_colours)
            for permutation in permutations
            for swap_colours in (False, True)
        }
        require(orbit <= diagonal_packets,
                "a sharp representative orbit left the diagonal packet")
        require(not (covered & orbit), "the two sharp oriented orbits merged")
        covered |= orbit
        orbit_sizes.append(len(orbit))
    require(covered == diagonal_packets and orbit_sizes == [720, 720],
            "the sharp seven-cell orbit coverage changed")

    representative_crosses = []
    for packet in SHARP_REPRESENTATIVES:
        a_matching, b_matching, b_holes, c_matching, c_holes = packet
        edges = (tuple((edge, A) for edge in a_matching) +
                 tuple((edge, B) for edge in b_matching) +
                 tuple((edge, C) for edge in c_matching))
        crosses = []
        for left_colour, right_colour, left_hole, right_hole in (
                (B, C, b_holes[0], c_holes[1]),
                (C, B, c_holes[0], b_holes[1])):
            tensor = matching_tensor(
                edges, 2,
                ((left_hole, left_colour),
                 (right_hole, right_colour)),
            )
            crosses.append(list(next(iter(tensor))))
        representative_crosses.append(crosses)

    return {
        "seven_cell_support_choices": 15 * 45 * 45,
        "top_pure_supports": top_pure_supports,
        "oriented_diagonal_packets": len(diagonal_packets),
        "source_orbits": 2,
        "orbit_sizes": orbit_sizes,
        "cross_rows_per_packet": 2,
        "cross_status": "one private unit monomial in each ordered row",
        "canonical_representative_cross_words": representative_crosses,
        "verdict": "the sharp 3h-2=7 one-bad boundary is empty",
    }


def main():
    pin_dependencies()
    census, configurations = audit_minimum_orbits()
    guard = audit_valid_guard(configurations)
    sharp = audit_sharp_seven_cell_boundary()
    ledger = {
        "pins": PINS,
        "minimum_binary_census": census,
        "valid_rational_guard": guard,
        "sharp_seven_cell_boundary": sharp,
        "verdict": (
            "the six-site binary projection is feasible at the sharp "
            "eight-entry support in two exact orbits; binary algebra alone "
            "cannot close the one-bad packet"
        ),
        "remaining_equations": [
            "d*H^[2]+d^[2]*H+d^[3]=X_a",
            "p_i*s_j*(d*H+d^[2])=0 for i,j in {b,c}",
        ],
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"minimum binary counterguard ledger changed: {digest}")

    print("N=8 one-bad minimum binary projection counterguards: PASS")
    print("minimum exact packets / orbits: 2160 / 2")
    print("valid 4-cell H + 4-star guard: exact")
    print("sharp seven-cell packets: 1440 in 2 orbits; all cross-obstructed")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
