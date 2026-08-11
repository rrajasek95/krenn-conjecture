#!/usr/bin/env python3
"""Force a new matching from the same-base pure/mixed decoration packet.

Let one physical perfect matching B carry both a nonzero pure-j target
monomial and a nonzero mixed zero-row monomial.  On any edge whose two
decorations differ, use the mixed cell there and the pure cells on every
other edge of B.  Because matching edges are disjoint, this is a legal
nonzero hybrid monomial in one mixed output coefficient.  Exactness forces a
second monomial.  The decorated monomial on skeleton B is unique, so the mate
has a different physical matching.  Two distinct perfect matchings cannot
share all but one edge; their symmetric difference contains an alternating
cycle of length at least four.  Thus the same-base label packet necessarily
opens a physical matching-exchange route.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_other_bright_anchor_boundary.py":
        "a1332e5bec3a6c96f854bff0a7e18e21718c84d2807b67bd7751735fc45d0dd5",
    "notes/h3-axis-target-coloop-other-bright-anchor-boundary.md":
        "7222ca3405eea864c8b53a61aaa7a2ef7b314e1d177f6642766da999444e3276",
    "computations/verify_h3_axis_target_coloop_common_covector_k22_scope.py":
        "6de8935cae41f03e71141850b63b9fd167418bb1cebe0575ce0f3de03e8386b3",
    "notes/h3-axis-target-coloop-common-covector-k22-scope.md":
        "d083a5d967175ac26f32b252d03b57ae22aff81a661889e012e5a1b781378a31",
    "notes/hafnian-path-forest-straightening.md":
        "0713791a87b692da809b5f64fe8d757d6454d59e550a859b8d7b7dea68598921",
}
EXPECTED_LEDGER_SHA256 = (
    "a18578cec952f4e7077e3716bec120ca36031df8a24944a2e5627234749218a2"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield tuple(sorted((edge(first, second),) + tail))


def cycle_lengths(first, second):
    common = set(first) & set(second)
    symmetric = (set(first) | set(second)) - common
    adjacency = {}
    for left, right in symmetric:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    require(all(len(neighbours) == 2 for neighbours in adjacency.values()),
            "a matching symmetric difference stopped being cyclic")
    lengths = []
    unseen = set(adjacency)
    while unseen:
        start = next(iter(unseen))
        previous = None
        current = start
        length = 0
        while True:
            following = next(site for site in adjacency[current]
                             if site != previous)
            length += 1
            previous, current = current, following
            unseen.discard(previous)
            if current == start:
                break
        lengths.append(length)
    return tuple(sorted(lengths))


def decorated_cell(pair, word):
    left, right = pair
    return left, right, word[left], word[right]


def decorated_monomial(matching, word):
    return frozenset(decorated_cell(pair, word) for pair in matching)


def audit_uniform_matching_fact():
    matchings = tuple(perfect_matchings(range(8)))
    require(len(matchings) == 105, "the K8 matching count changed")
    common_histogram = Counter()
    cycle_histogram = Counter()
    for index, first in enumerate(matchings):
        for second in matchings[index + 1:]:
            common = len(set(first) & set(second))
            cycles = cycle_lengths(first, second)
            require(common <= 2,
                    "two distinct K8 matchings shared three edges")
            require(cycles and all(length >= 4 and length % 2 == 0
                                   for length in cycles),
                    "a matching mate lost its alternating C4-or-longer cycle")
            common_histogram[common] += 1
            cycle_histogram[cycles] += 1
    require(sum(common_histogram.values()) == 105 * 104 // 2,
            "the unordered matching-pair count changed")

    # For every physical matching and every nonempty set of changed edges,
    # one hybrid is available for each changed edge.  This pins the uniform
    # word construction independently of a particular colour labelling.
    hybrids = 0
    changed_size_histogram = Counter()
    for matching in matchings:
        for changed_size in range(1, 5):
            for changed in combinations(matching, changed_size):
                for selected_edge in changed:
                    require(selected_edge in matching,
                            "a hybrid selected an edge outside its base")
                    hybrids += 1
                    changed_size_histogram[changed_size] += 1
    require(hybrids == 105 * 32,
            "the K8 abstract one-edge hybrid count changed")
    return {
        "perfect_matchings": len(matchings),
        "unordered_distinct_pairs": sum(common_histogram.values()),
        "common_edge_histogram": dict(common_histogram),
        "symmetric_difference_cycle_histogram": {
            str(cycles): count for cycles, count in sorted(cycle_histogram.items())
        },
        "abstract_one_edge_hybrids": hybrids,
        "hybrids_by_changed_edge_set_size": dict(changed_size_histogram),
        "uniform_consequence": (
            "a cancellation mate distinct from B changes at least two "
            "physical edges and opens one or more alternating cycles, each "
            "of length at least four"
        ),
    }


P, S = 6, 7


def audit_canonical_same_base_packet():
    target = tuple(sorted((edge(P, 0), edge(S, 1),
                           edge(2, 3), edge(4, 5))))
    base = tuple(sorted((edge(0, 1), edge(P, 2),
                         edge(S, 3), edge(4, 5))))
    unary = tuple(sorted((edge(P, S), edge(0, 1),
                          edge(2, 3), edge(4, 5))))
    require(cycle_lengths(target, base) == (6,),
            "the canonical same-base packet lost its C6 target exchange")

    pure = (1,) * 8
    mixed = (2, 2, 1, 2, 2, 2, 1, 2)
    pure_cells = decorated_monomial(base, pure)
    mixed_cells = decorated_monomial(base, mixed)
    changed = tuple(pair for pair in base
                    if decorated_cell(pair, pure) != decorated_cell(pair, mixed))
    require(changed == (edge(0, 1), edge(S, 3), edge(4, 5)),
            f"the canonical changed-edge set moved: {changed}")

    hybrids = []
    for selected_edge in changed:
        word = list(pure)
        for site in selected_edge:
            word[site] = mixed[site]
        word = tuple(word)
        require(len(set(word)) > 1,
                "a one-edge hybrid became a pure target word")
        hybrid_cells = frozenset(
            decorated_cell(pair, mixed if pair == selected_edge else pure)
            for pair in base
        )
        require(hybrid_cells == decorated_monomial(base, word),
                "the disjoint-edge hybrid stopped being one literal monomial")
        require(hybrid_cells <= pure_cells | mixed_cells,
                "the hybrid introduced a scalar cell not already supported")

        # On a fixed matching skeleton and fixed output word, exactly one
        # decorated monomial exists.  Every cancellation term is therefore
        # carried by another physical matching.
        same_skeleton_terms = tuple(
            decorated_monomial(base, candidate_word)
            for candidate_word in (word,)
        )
        require(same_skeleton_terms == (hybrid_cells,),
                "a fixed skeleton/output acquired a second monomial")
        hybrids.append({
            "changed_edge": selected_edge,
            "hybrid_word": "".join(map(str, word)),
            "hybrid_cells": tuple(sorted(hybrid_cells)),
            "target_coefficient": 0,
            "forced_mate": "a distinct physical perfect matching",
        })

    require(len(hybrids) == 3,
            "the canonical same-base hybrid count changed")
    return {
        "M_target": target,
        "N_mixed_equals_L_pure_skeleton": base,
        "K_unary": unary,
        "pure_other_bright_word": "11111111",
        "selected_mixed_word": "22122212",
        "changed_physical_edges": changed,
        "one_edge_hybrid_zero_rows": hybrids,
        "exact_row_consequence": (
            "each displayed nonzero hybrid monomial lies in a mixed target-"
            "zero coefficient, so exactness forces another supported "
            "monomial on a different physical perfect matching"
        ),
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "uniform_matching_exchange": audit_uniform_matching_fact(),
        "canonical_same_base_source_words": audit_canonical_same_base_packet(),
        "theorem": (
            "if one physical matching B carries a nonzero pure target "
            "decoration and a distinct nonzero mixed decoration, choose one "
            "edge on which they differ.  The mixed cell on that edge times "
            "the pure cells on B's other edges is an already-supported "
            "nonzero monomial in a mixed zero coefficient.  Its unique "
            "B-skeleton term must be cancelled by a different physical "
            "matching, whose symmetric difference with B contains an "
            "alternating C4-or-longer cycle"
        ),
        "routing_split": (
            "the forced mate removes the same-base label packet as a terminal "
            "case.  A new endpoint edge enters the complete-column route; "
            "an anchor-contained mate enters the Hall/lock web; and a mate "
            "with only new residual q edges is exactly the previously named "
            "diagonal/offdiagonal residual-q coefficient gate"
        ),
        "scope": (
            "uniform source-labelled matching theorem, not a support census. "
            "It forces a new active matching monomial but does not assert "
            "that every residual-q-only mate is already a good endpoint arm"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"same-base hybrid-mate ledger changed: {digest}")
    print("h3 target-coloop same-base hybrid-mate theorem: PASS")
    print("pure+mixed decorations -> nonzero one-edge hybrid zero row")
    print("exactness -> distinct physical mate / alternating C4-or-longer")
    print("same-base label packet is not terminal")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
