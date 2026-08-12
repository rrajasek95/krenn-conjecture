#!/usr/bin/env python3
"""Exact audit of the minimum-distance matching-base separator lemma.

The proof is elementary and appears in the matching-base attack note.  This
checker freezes the complete perfect-matching topology at h=3 and h=4 and
audits the component-switch and shortening-chord inequalities through C20.
It deliberately says nothing about source typing: a physical C4 is not yet
a certified identical-tail/opposite-orientation exchange cell.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json


EXPECTED_LEDGER_SHA256 = (
    "eccd682b613d3932f43d06b37d169c9173634962d47c6477fd172c1491078ba0"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return (frozenset(),)
    first = vertices[0]
    result = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            result.append(frozenset((edge(first, second),)) | tail)
    return tuple(result)


def alternating_components(first, second):
    symmetric = first ^ second
    adjacency = {}
    for left, right in symmetric:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    require(all(len(neighbours) == 2 for neighbours in adjacency.values()),
            "a matching symmetric difference stopped being cyclic")
    components = []
    unseen = set(adjacency)
    while unseen:
        root = min(unseen)
        stack = [root]
        vertices = set()
        while stack:
            current = stack.pop()
            if current in vertices:
                continue
            vertices.add(current)
            stack.extend(adjacency[current] - vertices)
        unseen -= vertices
        components.append(frozenset(vertices))
    return tuple(sorted(components, key=lambda item: (len(item), tuple(item))))


def flip_distance(first, second):
    return sum(len(component) // 2 - 1
               for component in alternating_components(first, second))


def switch_components(first, second, selected_components):
    selected_vertices = set().union(*selected_components)
    retained = frozenset(e for e in first
                         if not set(e) <= selected_vertices)
    inserted = frozenset(e for e in second
                         if set(e) <= selected_vertices)
    switched = retained | inserted
    vertices = [site for e in switched for site in e]
    require(len(vertices) == len(set(vertices)),
            "component switching stopped being a perfect matching")
    return switched


def topology_name(first, second):
    lengths = tuple(sorted(len(component)
                           for component in alternating_components(first, second)))
    return "+".join(f"C{length}" for length in lengths)


def audit_complete_topologies(order):
    matchings = perfect_matchings(range(2 * order))
    histogram = Counter()
    switch_checks = 0
    for left_index, first in enumerate(matchings):
        for second in matchings[left_index + 1:]:
            components = alternating_components(first, second)
            histogram[topology_name(first, second)] += 1
            if len(components) <= 1:
                continue
            total = flip_distance(first, second)
            for component in components:
                switched = switch_components(first, second, (component,))
                require(flip_distance(first, switched) < total,
                        "a proper component switch did not approach the first base")
                require(flip_distance(switched, second) < total,
                        "a proper component switch did not approach the second base")
                switch_checks += 1
    expected = {
        3: Counter({"C4": 45, "C6": 60}),
        4: Counter({"C4": 630, "C6": 1680,
                    "C8": 2520, "C4+C4": 630}),
    }[order]
    require(histogram == expected,
            f"order-{order} matching topology changed: {histogram}")
    return {
        "matching_count": len(matchings),
        "pair_topologies": dict(sorted(histogram.items())),
        "proper_component_switch_checks": switch_checks,
    }


def cycle_pair(half_length):
    vertices = tuple(range(2 * half_length))
    first = frozenset(edge(2 * index, 2 * index + 1)
                      for index in range(half_length))
    second = frozenset(
        edge(2 * index + 1, (2 * index + 2) % (2 * half_length))
        for index in range(half_length)
    )
    require(topology_name(first, second) == f"C{2 * half_length}",
            "the canonical alternating cycle changed")
    return vertices, first, second


def shortening_matching(half_length):
    _vertices, first, second = cycle_pair(half_length)
    # Chord 0--3, followed by the second matching on 1--2 and the first
    # matching on all later pairs.  This is the standard C_(2r) shortening.
    shortened = {edge(0, 3), edge(1, 2)}
    shortened.update(edge(2 * index, 2 * index + 1)
                     for index in range(2, half_length))
    shortened = frozenset(shortened)
    require(topology_name(first, shortened) == "C4",
            "the shortening matching lost its C4 side")
    require(topology_name(shortened, second) == f"C{2 * (half_length - 1)}",
            "the shortening matching lost its shorter-cycle side")
    require(flip_distance(first, shortened) == 1,
            "the C4 flip distance changed")
    require(flip_distance(shortened, second) == half_length - 2,
            "the shortened flip distance changed")
    require(flip_distance(first, second) == half_length - 1,
            "the original cycle flip distance changed")
    return {
        "cycle": f"C{2 * half_length}",
        "distance": half_length - 1,
        "shortening_sides": ["C4", f"C{2 * (half_length - 1)}"],
        "shortened_distance": half_length - 2,
    }


def audit():
    ledger = {
        "definition": (
            "delta(M,N)=sum_C(|C|/2-1) over alternating components of "
            "the symmetric difference"
        ),
        "order3": audit_complete_topologies(3),
        "order4": audit_complete_topologies(4),
        "shortening_cycles": [shortening_matching(r) for r in range(3, 11)],
        "theorem": (
            "a minimum-distance unjoined same-word matching base differs "
            "from its joined component by one alternating cycle; any "
            "supported same-word distance-three shortening chord also "
            "contradicts minimality"
        ),
        "scope_guard": (
            "this is matching topology only.  It does not promote a "
            "physical C4 to a source-certified identical-tail/opposite-"
            "orientation exchange, nor force a shortening chord to exist"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"first-separator distance ledger changed: {digest}")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("matching-base first-separator distance: PASS (exact)")
    print("h=3 topologies:", ledger["order3"]["pair_topologies"])
    print("h=4 topologies:", ledger["order4"]["pair_topologies"])
    print("single-cycle and supported-chord reductions audited through C20")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
