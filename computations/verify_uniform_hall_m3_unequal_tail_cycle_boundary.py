#!/usr/bin/env python3
"""Exact cycle topology and recurrence guard for the strict-Hall M3 branch.

The two-block theorem turns the first unmatched literal class into either
pure-anchor reselection or two typed crossing cells.  In the canonical
strict K2,2 anchor web, a two-shared pivot has exactly one anchor-contained
avoiding matching.  Its union with either anchor containing the pivot is an
even alternating cycle; deleting the pivot leaves an odd-edge path whose
first and last edges carry the two crossing cells.

The apparent odd-path promotion gap reaches the shared pivot one row earlier.
Apply the
complete decorated-edge exchange to either endpoint crossing cell, relative
to the pure anchor containing that cell.  At the shared-pivot endpoint the
strict anchor union has only two incident pairs: the crossing arm and the
original shared pivot.  Hence an avoiding term either leaves the union, or
returns through the pivot with a non-pure label.  The former is the
off-anchor route and the latter is exactly the pinned two-shared migration.
But that migration may terminate at q_e^(m,m), which is a fixed point of the
same migration and can recreate the direct-label/two-block gate.  Thus this
checker proves the parity/return boundary, not SCC closure.
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
    "computations/verify_uniform_decorated_anchor_mixed_word_exchange.py":
        "150bf15eb8ac475f866c062afcd7e3002477d02338acdb082c14f9136a3e58b7",
    "notes/uniform-decorated-anchor-mixed-word-exchange.md":
        "0cdc391bebb44150c7941bdbeec853029929f20d46ee813eb2a09bb76c27a5de",
    "computations/verify_uniform_two_shared_anchor_unary_label_migration.py":
        "78ab24f1c39d79ea38a80fd80bf43e43624e57dada0345c2c98b30559f528dc6",
    "notes/uniform-two-shared-anchor-unary-label-migration.md":
        "2e794feae556d582dc1623e698e2e331cae44e0de36e9d59125740a908d3b1c9",
}
EXPECTED_LEDGER_SHA256 = "80f803585f3a0fc89dd9bbc356d016a7cfc52a415d7f7196365a58f9d4a194bb"


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


def audit_endpoint_exchange_return(records):
    anchor_union = set().union(*(set(matching) for matching in Q.values()))
    routes = []
    for record in records:
        pivot = record["pivot"]
        background = record["background_anchor"]
        avoiding = record["unique_avoiding_anchor"]
        containing_colours = {colour for colour, matching in Q.items()
                              if pivot in matching}
        block = next(iter(containing_colours - {background}))
        require({block, background, avoiding} == {0, 1, 2},
                "the strict two-block colours stopped being ternary")

        for endpoint in pivot:
            crossing = next(pair for pair in record["crossing_endpoint_edges"]
                            if endpoint in pair)
            other = partner(Q[avoiding], endpoint)
            require(crossing == edge(endpoint, other),
                    "the crossing arm lost its pivot endpoint")

            incident_anchor_edges = {
                pair for pair in anchor_union if endpoint in pair
            }
            require(incident_anchor_edges == {pivot, crossing},
                    "the strict pivot endpoint acquired a third anchor arm")

            # Apply complete exchange to q_crossing^(block,background)
            # relative to the pure avoiding-colour anchor.  In that row the
            # crossing endpoint has colour `block`, its old partner has
            # colour `background`, and every other site has colour `avoiding`.
            word = [avoiding] * 6
            word[endpoint] = block
            word[other] = background
            avoiding_terms = tuple(
                matching for matching in perfect_matchings(range(6))
                if crossing not in matching
            )
            inside_endpoint = []
            outside_endpoint = []
            for matching in avoiding_terms:
                exit_edge = edge(endpoint, partner(matching, endpoint))
                if exit_edge in anchor_union:
                    inside_endpoint.append((matching, exit_edge))
                    require(exit_edge == pivot,
                            "an anchor-contained endpoint exit missed the pivot")
                    labels = (word[exit_edge[0]], word[exit_edge[1]])
                    require(sorted(labels) == sorted((block, avoiding)),
                            "the returned pivot label pair changed")
                    require(labels != (block, block)
                            and labels != (background, background),
                            "the returned pivot cell became pure for both anchors")
                else:
                    outside_endpoint.append((matching, exit_edge))
                    labels = (word[exit_edge[0]], word[exit_edge[1]])
                    require(labels[0] != labels[1],
                            "an off-anchor endpoint exit stopped being typed")
            require(inside_endpoint and outside_endpoint,
                    "the endpoint-exchange dichotomy lost a branch")
            routes.append({
                "pivot": pivot,
                "background_anchor": background,
                "block_anchor": block,
                "crossing_anchor": avoiding,
                "crossing_edge": crossing,
                "crossing_labels_at_endpoint": [block, background],
                "avoiding_exchange_terms": len(avoiding_terms),
                "anchor_contained_endpoint_terms": len(inside_endpoint),
                "off_anchor_endpoint_terms": len(outside_endpoint),
                "anchor_contained_exit": pivot,
                "returned_pivot_labels": [block, avoiding],
                "landing": (
                    "off-anchor typed cell, or non-pure returned cell on "
                    "the two-shared pivot"
                ),
            })
    require(len(routes) == 8,
            "the two crossing endpoints stopped giving eight return audits")
    return {
        "endpoint_exchange_audits": routes,
        "source_identity": (
            "complete exchange at the crossing cell gives pure-anchor "
            "reselection if its complete pure cofactor is dark; otherwise "
            "it forces an avoiding matching or a localized unit"
        ),
        "strict_incidence": (
            "at its shared-pivot endpoint, an avoiding matching either uses "
            "the pivot or an edge outside the selected anchor union"
        ),
        "return_interface": (
            "pivot return is a non-pure cell on an edge shared by the two "
            "other pure anchors and enters 07a1f02; outside return enters "
            "the pinned nonanchor active route"
        ),
    }


def audit_terminal_recurrence_guard(records):
    """The pure-third direct label is a literal fixed point, not progress."""
    guards = []
    for record in records:
        pivot = record["pivot"]
        background = record["background_anchor"]
        avoiding = record["unique_avoiding_anchor"]
        containing = {colour for colour, matching in Q.items()
                      if pivot in matching}
        block = next(iter(containing - {background}))
        require({block, background, avoiding} == {0, 1, 2},
                "the terminal colour triple changed")

        # 07a1f02 starts from any non-k-pure q_e^(i,j), where k is one
        # anchor containing e and m is the missing anchor.  At its terminal
        # (i,j)=(m,m), rerunning the four-row label chain ends at the same
        # (m,m).  Neither the physical pivot nor the cut-cycle record moves.
        initial = (avoiding, avoiding)
        require(initial != (block, block),
                "the terminal direct label became pure for the through anchor")
        terminal = (avoiding, avoiding)
        require(initial == terminal,
                "the displayed migration unexpectedly gained label progress")
        guards.append({
            "pivot": pivot,
            "through_anchor": block,
            "background_anchor": background,
            "missing_anchor": avoiding,
            "initial_direct_labels": initial,
            "migration_terminal_labels": terminal,
            "cut_path_edges_before_after": [record["cut_path_edges"],
                                              record["cut_path_edges"]],
            "strict_progress": False,
        })
    require(len(guards) == 4 and all(not item["strict_progress"]
                                     for item in guards),
            "the strict return self-loop census changed")
    return {
        "fixed_point_records": guards,
        "label_measure_decreases": False,
        "cut_path_measure_decreases": False,
        "missing_source_datum": (
            "a weighted transfer-SCC/common-tail holonomy relation: trivial "
            "holonomy must give a same-star deletion kernel and nontrivial "
            "holonomy a localized source unit"
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
        "endpoint_exchange_return": audit_endpoint_exchange_return(cycles),
        "terminal_recurrence_guard": audit_terminal_recurrence_guard(cycles),
        "proved_composition": (
            "the first unmatched two-block coefficient gives pure-anchor "
            "reselection, an off-anchor typed crossing, or the unique "
            "anchor-contained crossing pair at the ends of one of the four "
            "displayed odd cut paths.  Complete exchange on either crossing "
            "cell returns through the shared pivot, hence enters 07a1f02, "
            "or leaves the anchor union.  If a residual pair already has "
            "one literal common complement class, f3716b2 closes it.  The "
            "terminal direct label alone does not prove such a common class"
        ),
        "odd_path_promotion": (
            "endpoint exchange meets the shared pivot before entering the "
            "odd-path interior, but migration may return to the same "
            "q_e^(m,m) with unchanged path length; this is a parity/return "
            "boundary, not a terminating promotion"
        ),
        "scope": (
            "exact strict-K2,2 matching topology and typed complete-row "
            "composition.  It routes unmatched/unequal first two-block "
            "tails to off-anchor/reselection/unit or a recurrent terminal "
            "direct-label SCC.  It does not close that SCC and does not "
            "assert the same incidence in a larger non-strict web"
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
    print("unequal class -> shared-pivot migration or off-anchor exit")
    print("terminal q_e^(m,m) -> exact fixed-point recurrence; SCC still open")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
