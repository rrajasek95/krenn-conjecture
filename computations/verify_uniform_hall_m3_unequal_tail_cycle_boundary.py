#!/usr/bin/env python3
"""Exact cycle topology of the strict-Hall M3 unequal-tail branch.

The two-block theorem turns the first unmatched literal class into either
pure-anchor reselection or two typed crossing cells.  In the canonical
strict K2,2 anchor web, a two-shared pivot has exactly one anchor-contained
avoiding matching.  Its union with either anchor containing the pivot is an
even alternating cycle; deleting the pivot leaves an odd-edge path whose
first and last edges carry the two crossing cells.

This checker freezes the precise promotion boundary.  A common literal
complement class is closed by the signless-incidence theorem.  An unequal
class is not yet covered by the even-path theorem, because its cut path has
odd length.  At six residual sites a source-valid inward move could be used
at most twice (path lengths 5 -> 3 -> 1), but that target/ordinary-residue
preserving move is a new source identity and is not inferred here.
"""

from __future__ import annotations

from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_multisite_hall_k22_effective_hole_m3_boundary.py":
        "987c702e6f056cd5715ad2df95b680100aee4b168c4359b2300eaf7022370695",
    "notes/uniform-multisite-hall-k22-effective-hole-m3-boundary.md":
        "5df738886b3f6cdb84112abc99f35bc91b3a3e28cf820f01344cef8df90300ea",
    "computations/verify_uniform_hall_five_lock_signless_incidence_boundary.py":
        "34bf365f2a9e154a10feab8fa7cc83b0aba519f4124b8e28ed959f280a51e721",
    "notes/uniform-hall-five-lock-signless-incidence-boundary.md":
        "4da56337a9cc6b8434a06b6cf1e4c9118334ebf695f4679e8183232f4733cb1b",
    "computations/verify_uniform_two_block_word_cofactor_reselection.py":
        "504787810c94ed088b5184c988f8bfcf36adce99c3962f05f7cb605d71b306e3",
    "notes/uniform-two-block-word-cofactor-reselection.md":
        "48f1929fa88d55431484a7c4708eb0647ec69a031f0b3f444e3d227c512e8ce5",
    "computations/verify_uniform_hall_even_path_opposite_companion_wedge.py":
        "959d79389dbc635247a92cd708bf5c14b19cbfcf4f3de8f9e2bc74275156aa22",
    "notes/uniform-hall-even-path-opposite-companion-wedge.md":
        "7c8bfadc00b0d14a99c829b4682628819e9431d09fb3275a6e9fdf8f58a61652",
}
EXPECTED_LEDGER_SHA256 = "6d5b417de4be28bef7a6c14b923f36352397e1efae37e709b21d5671362691b7"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield tuple(sorted((edge(first, second),) + tail))


Q = {
    0: tuple(sorted((edge(0, 1), edge(2, 4), edge(3, 5)))),
    1: tuple(sorted((edge(0, 1), edge(2, 3), edge(4, 5)))),
    2: tuple(sorted((edge(0, 2), edge(1, 3), edge(4, 5)))),
}


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def partner(matching, vertex):
    for left, right in matching:
        if left == vertex:
            return right
        if right == vertex:
            return left
    raise RuntimeError((matching, vertex))


def alternating_component(first, second, start_edge):
    """Return the cyclic vertex order of the component containing edge."""
    adjacency = {vertex: [] for vertex in range(6)}
    for matching_index, matching in enumerate((first, second)):
        for left, right in matching:
            adjacency[left].append((right, matching_index))
            adjacency[right].append((left, matching_index))
    left, right = start_edge
    require(start_edge in first and start_edge not in second,
            "the marked edge is not a one-sided first-matching edge")
    order = [left, right]
    current = right
    wanted_matching = 1
    while current != left:
        choices = [other for other, kind in adjacency[current]
                   if kind == wanted_matching]
        require(len(choices) == 1,
                "the two matching union lost degree two")
        current = choices[0]
        if current != left:
            order.append(current)
        wanted_matching = 1 - wanted_matching
    require(len(order) % 2 == 0,
            "an alternating matching component became odd")
    return tuple(order)


def audit_anchor_web():
    anchor_union = set().union(*(set(matching) for matching in Q.values()))
    contained = tuple(matching for matching in perfect_matchings(range(6))
                      if set(matching) <= anchor_union)
    require(set(contained) == set(Q.values()),
            f"the strict anchor union gained a matching: {contained}")
    multiplicities = {
        pair: sum(pair in matching for matching in Q.values())
        for pair in anchor_union
    }
    shared = {pair: count for pair, count in multiplicities.items()
              if count == 2}
    require(shared == {edge(0, 1): 2, edge(4, 5): 2},
            f"the strict two-shared pivots changed: {shared}")
    return {
        "anchor_union_edges": len(anchor_union),
        "anchor_contained_perfect_matchings": {
            str(colour): Q[colour] for colour in sorted(Q)
        },
        "two_shared_pivots": sorted(shared),
    }


def audit_two_shared_cut_cycles():
    records = []
    for marked in (edge(0, 1), edge(4, 5)):
        containing = [colour for colour, matching in Q.items()
                      if marked in matching]
        avoiding = [colour for colour, matching in Q.items()
                    if marked not in matching]
        require(len(containing) == 2 and len(avoiding) == 1,
                "a two-shared pivot lost its unique avoiding anchor")
        avoid_colour = avoiding[0]
        for background_colour in containing:
            cycle = alternating_component(
                Q[background_colour], Q[avoid_colour], marked)
            cut_path = cycle
            path_edges = len(cycle) - 1
            require(path_edges in (3, 5) and path_edges % 2 == 1,
                    "the two-block crossing path stopped being odd")
            left_cross = edge(cycle[0], cycle[-1])
            # In the returned cyclic order, marked joins cycle[0]-cycle[1].
            # Removing it leaves the reverse path cycle[1]...cycle[0].  Its
            # endpoint edges are both in the avoiding matching.
            path_vertices = cycle[1:] + cycle[:1]
            endpoint_edges = (
                edge(path_vertices[0], path_vertices[1]),
                edge(path_vertices[-2], path_vertices[-1]),
            )
            require(all(pair in Q[avoid_colour]
                        for pair in endpoint_edges),
                    "the two crossing cells left the avoiding anchor arms")
            common_tail = tuple(sorted(set(Q[background_colour])
                                       & set(Q[avoid_colour])))
            records.append({
                "pivot": marked,
                "background_anchor": background_colour,
                "unique_avoiding_anchor": avoid_colour,
                "alternating_cycle_vertices": cycle,
                "cycle_edges": len(cycle),
                "cut_path_edges": path_edges,
                "crossing_endpoint_edges": endpoint_edges,
                "literal_common_diagonal_tail": common_tail,
                "maximum_inward_moves_at_h3": (path_edges - 1) // 2,
            })
    require(len(records) == 4,
            "the strict two-shared cycle family changed")
    require({record["cycle_edges"] for record in records} == {4, 6},
            "the strict cycle lengths changed")
    return records


def audit_all_two_block_labels(records):
    labelled = []
    for record in records:
        left, right = record["pivot"]
        for block_colour, background in itertools.permutations(range(3), 2):
            word = [background] * 6
            word[left] = word[right] = block_colour
            crossing_labels = []
            for pair in record["crossing_endpoint_edges"]:
                crossing_labels.append((word[pair[0]], word[pair[1]]))
            require(all(a != b for a, b in crossing_labels),
                    "a two-block endpoint cell stopped being off-diagonal")
            require(sum(label == block_colour for labels in crossing_labels
                        for label in labels) == 2,
                    "the two block endpoints stopped occurring once each")
            labelled.append({
                "pivot": record["pivot"],
                "block_background": (block_colour, background),
                "crossing_labels": crossing_labels,
            })
    require(len(labelled) == 24,
            "the ternary strict-cycle label audit changed")
    return {
        "labelled_strict_cycles": len(labelled),
        "each_avoiding_term_has_two_typed_crossings": True,
        "sample": labelled[:2],
    }


def audit_parity_boundary(records):
    lengths = sorted({record["cut_path_edges"] for record in records})
    require(lengths == [3, 5],
            "the odd cut-path frontier changed")
    inward = {length: tuple(range(length, 0, -2)) for length in lengths}
    require(inward == {3: (3, 1), 5: (5, 3, 1)},
            "the bounded inward length measure changed")
    return {
        "cut_path_lengths": lengths,
        "strictly_decreasing_candidate_measure": inward,
        "common_class_landing": (
            "same literal complement tail gives the pinned signless block: "
            "bipartite/even supplies an exact deletion kernel and odd "
            "supplies a localized 2*pivot unit"
        ),
        "unequal_class_boundary": (
            "the even-path theorem starts with an even-edge open path; the "
            "two-block pivot cuts an even cycle to an odd-edge path.  A "
            "new complete-row inward homotopy is required to pass from "
            "length 5 to 3 or 3 to 1 while retaining source provenance"
        ),
    }


def main():
    pin_dependencies()
    anchor_web = audit_anchor_web()
    cycles = audit_two_shared_cut_cycles()
    ledger = {
        "strict_anchor_web": anchor_web,
        "two_shared_cut_cycles": cycles,
        "ternary_labels": audit_all_two_block_labels(cycles),
        "parity_and_measure": audit_parity_boundary(cycles),
        "proved_composition": (
            "the first unmatched two-block coefficient gives pure-anchor "
            "reselection, an off-anchor typed crossing, or the unique "
            "anchor-contained crossing pair at the ends of one of the four "
            "displayed odd cut paths.  If that pair has one literal common "
            "complement class, f3716b2 closes it"
        ),
        "first_missing_source_row": (
            "for unequal literal tails, a target- and old-ordinary-residue-"
            "preserving complete-row homotopy moving both crossing fronts "
            "inward by one alternating Q_l/Q_m edge pair.  Its existence is "
            "not a consequence of path parity or of the two-block factorization"
        ),
        "scope": (
            "exact strict-K2,2 matching topology and typed complete-row "
            "boundary, not a claim that unequal tail classes are already "
            "synchronized.  No support census or new source cell is assumed"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"M3 unequal-tail cycle ledger changed: {digest}")
    print("uniform Hall M3 unequal-tail cycle boundary: PASS")
    print("two-block mate -> reselection/offanchor or unique typed cycle pair")
    print("common literal class -> signless deletion/unit")
    print("unequal class -> odd cut path; inward source homotopy still missing")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
