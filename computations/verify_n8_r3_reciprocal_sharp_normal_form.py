#!/usr/bin/env python3
"""Audit the sharp r=3 reciprocal incidence frontier at N=8.

This checker deliberately stops at the exact information supplied by the
selected witness graph and the essential-star lemma.  It does not pretend
that the constructed incidence packet is a solution of the matching ideal.
"""

from __future__ import annotations

from itertools import combinations, permutations, product


N = 8
ALL_EDGES = tuple(combinations(range(N), 2))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def endpoint_budget(good_edges, isolated_good_vertices):
    """Return the sharp essential-incidence feasibility ledger.

    At r=3 the selected graph has 21 edges.  A site with three essential
    neighbours has selected degree exactly three, hence cannot meet a good
    selected edge.  All other sites contribute at most two incidences.
    """

    bad_edges = 21 - good_edges
    max_triple_sites = isolated_good_vertices
    maximum_essential = 16 + max_triple_sites
    return bad_edges, max_triple_sites, maximum_essential


def sharp_shape_ledger():
    shapes = {
        "3K2+2K1": (3, 2),
        "4K2": (4, 0),
    }
    ledger = {}
    for name, (good_edges, isolates) in shapes.items():
        bad, max_triples, budget = endpoint_budget(good_edges, isolates)
        ledger[name] = (bad, max_triples, budget, bad <= budget)

    require(ledger["4K2"] == (17, 0, 16, False),
            "the 4K2 essential-budget exclusion changed")
    require(ledger["3K2+2K1"] == (18, 2, 18, True),
            "the 3K2+2K1 sharp equality ledger changed")
    return ledger


def canonical_selected_graph():
    """Build the forced equality topology, up to relabelling.

    Vertices 0,1 are the two three-essential (hence cubic) sites.  Their
    selected neighbours are disjoint triples only for convenience; the
    theorem below needs only that each has three outer neighbours.  Every
    outer-outer pair is selected and 01 is absent.
    """

    outer = tuple(range(2, 8))
    selected = set(combinations(outer, 2))
    selected.update((0, v) for v in (2, 3, 4))
    selected.update((1, v) for v in (5, 6, 7))
    selected = {tuple(sorted(edge)) for edge in selected}
    complement = set(ALL_EDGES) - selected

    require(len(selected) == 21 and len(complement) == 7,
            "canonical r=3 edge count changed")
    require((0, 1) in complement,
            "the two cubic sites unexpectedly became adjacent")
    require(all(tuple(sorted(edge)) in complement for edge in
                [(0, 5), (0, 6), (0, 7),
                 (1, 2), (1, 3), (1, 4)]),
            "the canonical complement is not the union of cubic stars")
    require(all(tuple(sorted(edge)) in selected
                for edge in combinations(outer, 2)),
            "the outer K6 is incomplete")
    return selected, complement


def essential_assignment(selected):
    """Realize equality: 18 bad edges, each charged exactly once."""

    outer = tuple(range(2, 8))
    good = {tuple(sorted(edge)) for edge in [(2, 5), (3, 6), (4, 7)]}
    essential = {(0, v) for v in (2, 3, 4)}
    essential.update((1, v) for v in (5, 6, 7))

    # K6 minus the opposite perfect matching is 4-regular.  Its cyclic
    # orientation has two outgoing edges per vertex and charges every bad
    # outer edge exactly once.
    for offset, u in enumerate(outer):
        for step in (1, 2):
            v = outer[(offset + step) % len(outer)]
            edge = tuple(sorted((u, v)))
            require(edge not in good,
                    "cyclic charge used a declared good edge")
            essential.add((u, v))

    bad = selected - good
    charged_edges = {tuple(sorted(pair)) for pair in essential}
    require(charged_edges == bad,
            "essential incidences do not cover exactly the bad edges")
    require(len(essential) == len(bad) == 18,
            "the sharp essential assignment is not one-to-one")

    counts = {u: 0 for u in range(N)}
    for u, _v in essential:
        counts[u] += 1
    require(counts == {0: 3, 1: 3, 2: 2, 3: 2,
                       4: 2, 5: 2, 6: 2, 7: 2},
            f"essential endpoint equality changed: {counts}")
    return good, essential


def find_three_reciprocal_orientation(selected):
    """Orient the 21 selected pairs as 24 arcs of outdegree three.

    Three chosen pairs are doubled.  The remaining 18 pairs receive one
    orientation.  Requiring the doubled pairs to be disjoint shows that the
    sharp incidence packet need not contain a reciprocal hub.
    """

    edges = tuple(sorted(selected))

    def solve_singles(single_edges, needs, index, arcs):
        if index == len(single_edges):
            return tuple(arcs) if all(value == 0 for value in needs) else None

        u, v = single_edges[index]
        remaining_u = sum(u in edge for edge in single_edges[index:])
        remaining_v = sum(v in edge for edge in single_edges[index:])
        if needs[u] < 0 or needs[v] < 0:
            return None
        if needs[u] > remaining_u or needs[v] > remaining_v:
            return None

        if needs[u] > 0:
            next_needs = list(needs)
            next_needs[u] -= 1
            answer = solve_singles(single_edges, next_needs, index + 1,
                                   arcs + [(u, v)])
            if answer is not None:
                return answer
        if needs[v] > 0:
            next_needs = list(needs)
            next_needs[v] -= 1
            answer = solve_singles(single_edges, next_needs, index + 1,
                                   arcs + [(v, u)])
            if answer is not None:
                return answer
        return None

    # Put the reciprocal matching completely in the outer K6.  This is a
    # stronger guard than merely avoiding a reciprocal hub: neither cubic
    # site participates in a reciprocal pair.
    outer_edges = tuple(edge for edge in edges if min(edge) >= 2)
    for reciprocal in combinations(outer_edges, 3):
        used = [vertex for edge in reciprocal for vertex in edge]
        if len(set(used)) != 6:
            continue
        reciprocal_set = set(reciprocal)
        needs = [3] * N
        doubled_arcs = []
        for u, v in reciprocal:
            needs[u] -= 1
            needs[v] -= 1
            doubled_arcs.extend([(u, v), (v, u)])
        singles = tuple(edge for edge in edges if edge not in reciprocal_set)
        answer = solve_singles(singles, needs, 0, doubled_arcs)
        if answer is not None:
            arcs = set(answer)
            require(len(arcs) == 24, "oriented witness count changed")
            outdegree = {u: sum(a == u for a, _b in arcs) for u in range(N)}
            require(set(outdegree.values()) == {3},
                    f"witness outdegrees changed: {outdegree}")
            mutual = {tuple(sorted((u, v))) for u, v in arcs
                      if (v, u) in arcs}
            require(mutual == reciprocal_set and len(mutual) == 3,
                    "reciprocal-pair count changed")
            return reciprocal, tuple(sorted(arcs))
    raise RuntimeError("no three-reciprocal orientation of the sharp graph")


def label_witness_arcs(arcs, selected, essential):
    """Realize the witness colours and the essential endpoint lines.

    An arc ``u -> v`` labelled ``a`` forces the endpoint line at ``v`` on
    the physical block ``uv`` to be the target axis ``e_a``.  At a
    two-essential site the two essential lines and the common nonessential
    line must be three different axes.  At a cubic site its three literal
    cells must be same-colour cells.  The small permutation search verifies
    that all of these source-labelled constraints are compatible.
    """

    outgoing = {
        u: sorted(v for source, v in arcs if source == u)
        for u in range(N)
    }
    incoming = {
        u: sorted(v for v, target in arcs if target == u)
        for u in range(N)
    }
    require(all(len(heads) == 3 for heads in outgoing.values()),
            "cannot label a non-cubic outgoing witness star")

    axis_permutations = tuple(permutations(range(3)))
    for local_permutations in product(axis_permutations, repeat=N):
        labelled = {
            (u, v): local_permutations[u][index]
            for u in range(N)
            for index, v in enumerate(outgoing[u])
        }
        endpoint_lines = {}
        feasible = True

        # An incoming selected witness fixes the line at its head.
        for u in range(N):
            for v in incoming[u]:
                endpoint_lines[(u, v)] = labelled[(v, u)]

        # The two cubic stars are same-colour coordinate cells.  Their
        # selected degree is three, so every arm is oriented outwards.
        for u in (0, 1):
            for v in outgoing[u]:
                colour = labelled[(u, v)]
                old = endpoint_lines.get((u, v))
                if old is not None and old != colour:
                    feasible = False
                    break
                endpoint_lines[(u, v)] = colour
            if not feasible:
                break
        if not feasible:
            continue

        # At each outer site, fill the two essential axes and the one common
        # nonessential axis, respecting every fixed incoming head label.
        for u in range(2, N):
            neighbours = sorted(v for v in range(N)
                                if tuple(sorted((u, v))) in selected)
            essential_neighbours = [v for v in neighbours
                                    if (u, v) in essential]
            nonessential_neighbours = [v for v in neighbours
                                       if (u, v) not in essential]
            fixed_essential = {
                endpoint_lines[(u, v)] for v in essential_neighbours
                if (u, v) in endpoint_lines
            }
            fixed_nonessential = {
                endpoint_lines[(u, v)] for v in nonessential_neighbours
                if (u, v) in endpoint_lines
            }
            if len(fixed_essential) != sum(
                    (u, v) in endpoint_lines for v in essential_neighbours):
                feasible = False
                break
            if len(fixed_nonessential) > 1:
                feasible = False
                break

            choices = fixed_nonessential or (
                set(range(3)) - fixed_essential
            )
            line = min(choices)
            if line in fixed_essential:
                feasible = False
                break
            remaining = sorted(set(range(3)) - {line} - fixed_essential)
            free_essential = [v for v in essential_neighbours
                              if (u, v) not in endpoint_lines]
            if len(remaining) != len(free_essential):
                feasible = False
                break
            for v in nonessential_neighbours:
                old = endpoint_lines.get((u, v))
                if old is not None and old != line:
                    feasible = False
                    break
                endpoint_lines[(u, v)] = line
            if not feasible:
                break
            for v, colour in zip(free_essential, remaining):
                endpoint_lines[(u, v)] = colour

        if not feasible:
            continue

        require(all(set(labelled[(u, v)] for v in outgoing[u])
                    == {0, 1, 2} for u in range(N)),
                "a witness star lost a colour")
        for u, v in arcs:
            require(endpoint_lines[(v, u)] == labelled[(u, v)],
                    "a selected head axis disagrees with its source label")
        for u in (0, 1):
            lines = {endpoint_lines[(u, v)] for v in outgoing[u]}
            require(lines == {0, 1, 2}, "a cubic star lost an axis")
            require(all(endpoint_lines[(u, v)] == endpoint_lines[(v, u)]
                        for v in outgoing[u]),
                    "a cubic arm is not a same-colour coordinate cell")
        for u in range(2, N):
            essential_lines = {endpoint_lines[(u, v)] for v in range(N)
                               if (u, v) in essential}
            other_lines = {endpoint_lines[(u, v)] for v in range(N)
                           if tuple(sorted((u, v))) in selected
                           and (u, v) not in essential}
            require(len(essential_lines) == 2 and len(other_lines) == 1
                    and essential_lines.isdisjoint(other_lines),
                    "an outer essential-star flag changed")
        return labelled, endpoint_lines

    raise RuntimeError("no source-labelled essential-line realization")


def main():
    ledger = sharp_shape_ledger()
    selected, complement = canonical_selected_graph()
    good, essential = essential_assignment(selected)
    reciprocal, arcs = find_three_reciprocal_orientation(selected)
    labels, endpoint_lines = label_witness_arcs(arcs, selected, essential)

    print("r=3 shape ledger:", ledger)
    print("surviving selected graph: two cubic sites plus outer K6")
    print("selected/complement/good/essential:",
          len(selected), len(complement), len(good), len(essential))
    print("three disjoint reciprocal pairs:", reciprocal)
    print("reciprocal endpoint labels:",
          [(edge, labels[(edge[0], edge[1])], labels[(edge[1], edge[0])])
           for edge in reciprocal])
    print("cubic same-colour cells:",
          [[(v, endpoint_lines[(u, v)]) for v in range(N)
            if tuple(sorted((u, v))) in selected] for u in (0, 1)])
    print("N=8 r=3 reciprocal sharp normal form: PASS")


if __name__ == "__main__":
    main()
