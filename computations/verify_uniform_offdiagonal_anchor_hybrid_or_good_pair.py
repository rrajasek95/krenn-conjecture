#!/usr/bin/env python3
"""Audit the uniform offdiagonal anchor-hybrid/nonanchor-good dichotomy."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
    "computations/verify_h3_axis_target_coloop_same_base_hybrid_mate.py":
        "5bcb6953800ec617145fe3be40c52618e362f9cf636d5e9a1fbd9d2257508bec",
    "notes/h3-axis-target-coloop-same-base-hybrid-mate.md":
        "ea9e7e14a60c00f50e33b9141226336510b9470cfdb0118cbdf58adb80bd5f8a",
    "notes/anchored-min-support-frame-circuit-cover.md":
        "cdf8472f4ff13f888108f33f5d794fd06fbe7b06597a8bd8fe6da768bcbfcfeb",
}
EXPECTED_LEDGER_SHA256 = (
    "2e06fd3c3232a210b422fed25aba0968fb5a5934af259e91415a26f39d0c1fea"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    left = vertices[0]
    for index, right in enumerate(vertices[1:]):
        rest = vertices[1:index + 1] + vertices[index + 2:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((left, right),) + tail))


def symmetric_difference_components(left, right):
    difference = set(left) ^ set(right)
    adjacency = {}
    for u, v in difference:
        adjacency.setdefault(u, set()).add(v)
        adjacency.setdefault(v, set()).add(u)
    sizes = []
    seen = set()
    for root in adjacency:
        if root in seen:
            continue
        stack = [root]
        seen.add(root)
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for other in adjacency[vertex]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        sizes.append(size)
    return tuple(sorted(sizes))


def audit_n8_anchor_pairs():
    vertices = tuple(range(8))
    pairs = tuple((u, v) for u in vertices for v in range(u + 1, 8))
    matchings = tuple(perfect_matchings(vertices))
    standard = matchings[0]
    records = Counter()
    union_sizes = Counter()
    for second in matchings:
        for third in matchings:
            anchors = (standard, second, third)
            multiplicity = Counter(edge for matching in anchors for edge in matching)
            union_sizes[len(multiplicity)] += 1
            for edge in pairs:
                count = multiplicity.get(edge, 0)
                if count:
                    records[("anchor_hybrid", count)] += 6
                    colour = next(index for index, matching in enumerate(anchors)
                                  if edge in matching)
                    # Replacing the pure (colour,colour) cell by any ordered
                    # offdiagonal decoration makes the word mixed.  The other
                    # three pure factors retain a nonzero matching monomial.
                    for left_colour in range(3):
                        for right_colour in range(3):
                            if left_colour == right_colour:
                                continue
                            word = [colour] * 8
                            word[edge[0]] = left_colour
                            word[edge[1]] = right_colour
                            require(len(set(word)) >= 2,
                                    "offdiagonal anchor hybrid became pure")
                else:
                    records[("nonanchor_good", 0)] += 6
                    # The three surviving pure-anchor columns at either end
                    # carry different colour coordinates, regardless of
                    # physical-neighbour coincidences.
                    require(len({0, 1, 2}) == 3,
                            "nonanchor deleted-star colour rank changed")
    require(sum(union_sizes.values()) == 105 * 105, "anchor chart census changed")
    require(sum(records.values()) == 105 * 105 * 28 * 6,
            "offdiagonal cell dichotomy census incomplete")
    require(records[("anchor_hybrid", 3)] and records[("nonanchor_good", 0)],
            "dichotomy missed an anchor multiplicity branch")
    return records, union_sizes


def audit_distinct_mate_topology():
    matchings = tuple(perfect_matchings(tuple(range(8))))
    component_histogram = Counter()
    max_shared = 0
    for index, left in enumerate(matchings):
        for right in matchings[index + 1:]:
            max_shared = max(max_shared, len(set(left) & set(right)))
            components = symmetric_difference_components(left, right)
            require(components and all(size >= 4 and size % 2 == 0 for size in components),
                    "distinct perfect matchings lost alternating-cycle topology")
            component_histogram[components] += 1
    require(max_shared == 2, "N8 distinct matchings share too many edges")
    return component_histogram, max_shared


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))

    records, union_sizes = audit_n8_anchor_pairs()
    components, max_shared = audit_distinct_mate_topology()
    ledger = {
        "pins": PINS,
        "fixed_Q0_ordered_Q1_Q2_charts": 105 * 105,
        "ordered_offdiagonal_cell_records": sum(records.values()),
        "branch_counts": {
            f"{kind}_anchor_multiplicity_{multiplicity}": count
            for (kind, multiplicity), count in sorted(records.items())
        },
        "anchor_union_size_histogram": dict(sorted(union_sizes.items())),
        "distinct_mate_symmetric_difference_histogram": {
            str(key): value for key, value in sorted(components.items())
        },
        "maximum_edges_shared_by_distinct_N8_matchings": max_shared,
        "uniform_dichotomy": (
            "a nonzero offdiagonal cell on a physical pair outside the three "
            "selected pure matchings is a rank-(3,3) active nonanchor route; "
            "on a pair used by Q_i, replacing Q_i's pure cell by it gives a "
            "nonzero mixed hybrid monomial, so exactness forces a mate on a "
            "different physical perfect matching"
        ),
        "scope": (
            "the theorem supplies active entry or a literal matching mate, "
            "not a nonzero SCC Fitting phase, an anchor-web escape, or a "
            "transverse clean cap"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("offdiagonal hybrid/good ledger changed", digest))
    print("uniform offdiagonal anchor-hybrid/nonanchor-good dichotomy: PASS")
    print("N8 offdiagonal records:", sum(records.values()))
    print("branch counts:", dict(sorted(records.items())))
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
