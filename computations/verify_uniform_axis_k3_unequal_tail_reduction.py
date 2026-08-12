#!/usr/bin/env python3
"""Bounded audit of the theorem-level unequal-tail reduction.

For two nonzero decorated matching terms in one physical coefficient word,
every switch of a whole alternating component is again a nonzero term in
that same coefficient.  A single alternating C_(2r), r>=3, shortens after
adjoining only the distance-three chord (0,3): replacing 01|23 by 03|12
gives a C4 against the old matching and a C_(2r-2) against the other.

The checker audits the formulas; the proof is uniform.  It deliberately does
not assert that the needed chord is nonzero or that determinant terms from
different output words can be synchronized.  Those are the exact remaining
source lemmas.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_axis_k3_minor_common_tail_boundary.py":
        "6a4454c324744d68457579b7aa613d026ea17457d95746d14743766a12a5710e",
    "notes/uniform-axis-k3-minor-common-tail-boundary.md":
        "19e2293461893fd6275335dc19564cd68050c44eab2e386429720a079317cf96",
}
EXPECTED_LEDGER_SHA256 = (
    "65431ee6c2d09f4dee90effa31be774bd8214b35affb4d5690049702b1379ced"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def alternating_cycle_matchings(length):
    require(length >= 4 and length % 2 == 0, length)
    first = tuple(edge(site, site + 1)
                  for site in range(0, length, 2))
    second = tuple(edge(site, (site + 1) % length)
                   for site in range(1, length, 2))
    return tuple(sorted(first)), tuple(sorted(second))


def alternating_components(first, second):
    difference = set(first) ^ set(second)
    adjacency = {}
    for left, right in difference:
        adjacency.setdefault(left, []).append(right)
        adjacency.setdefault(right, []).append(left)
    unseen = set(adjacency)
    components = []
    while unseen:
        start = next(iter(unseen))
        previous = None
        current = start
        vertices = []
        while True:
            unseen.discard(current)
            vertices.append(current)
            neighbours = adjacency[current]
            require(len(neighbours) == 2,
                    "a matching difference stopped being even cycles")
            following = (neighbours[0] if neighbours[0] != previous
                         else neighbours[1])
            previous, current = current, following
            if current == start:
                break
        components.append(tuple(vertices))
    return tuple(sorted((len(component) for component in components)))


def is_matching(matching, vertices):
    used = [site for pair in matching for site in pair]
    return len(used) == len(set(used)) == len(vertices) and set(used) == set(vertices)


def audit_single_cycle_shortening():
    audits = []
    for length in range(6, 22, 2):
        first, second = alternating_cycle_matchings(length)
        # The new matching uses one edge of the second matching (12), one
        # new distance-three chord (03), and every unaffected first edge.
        shortened = set(first)
        shortened.remove(edge(0, 1))
        shortened.remove(edge(2, 3))
        shortened.add(edge(0, 3))
        shortened.add(edge(1, 2))
        shortened = tuple(sorted(shortened))
        require(is_matching(shortened, range(length)),
                f"the shortening stopped being a matching at C{length}")
        require(alternating_components(first, shortened) == (4,),
                f"the first shortening side stopped being C4 at C{length}")
        require(alternating_components(shortened, second) == (length - 2,),
                f"the residual cycle did not shorten at C{length}")
        require(set(shortened) - (set(first) | set(second)) == {edge(0, 3)},
                f"more than one genuinely new chord appeared at C{length}")
        audits.append({
            "input_cycle": length,
            "new_chord": [0, 3],
            "first_difference": 4,
            "residual_difference": length - 2,
            "other_inserted_edge_already_in_second": [1, 2],
        })
    return audits


def audit_component_switch():
    first4, second4 = alternating_cycle_matchings(4)
    # Put a second disjoint C4 on sites 4..7.
    translate = lambda matching: tuple(
        edge(left + 4, right + 4) for left, right in matching
    )
    first = tuple(sorted(first4 + translate(first4)))
    second = tuple(sorted(second4 + translate(second4)))
    require(alternating_components(first, second) == (4, 4),
            "the two-component guard changed")
    intermediate = tuple(sorted(second4 + translate(first4)))
    require(alternating_components(first, intermediate) == (4,)
            and alternating_components(intermediate, second) == (4,),
            "whole-component switching stopped splitting C4+C4")
    require(set(intermediate) <= set(first) | set(second),
            "component switching introduced a new physical cell")
    return {
        "input_components": [4, 4],
        "intermediate_uses_only_existing_cells": True,
        "two_steps": [[4], [4]],
        "uniform_statement": (
            "switching any proper subset of alternating components uses "
            "only cells already nonzero in the two selected same-word terms"
        ),
    }


def audit_decorated_chord_typing():
    # In one fixed output word, an edge decoration is determined by its two
    # endpoint colours.  A nonzero shortening chord is private-site active
    # when its endpoints have different colours; equal colours leave the
    # coordinate-diagonal cycle web.
    histogram = Counter(
        "offdiagonal_active" if left != right else "diagonal_web"
        for left in range(3) for right in range(3)
    )
    require(histogram == Counter({
        "offdiagonal_active": 6, "diagonal_web": 3,
    }), "the shortening-chord typing split changed")
    return dict(histogram)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "single_cycle_shortening": audit_single_cycle_shortening(),
        "multiple_component_reduction": audit_component_switch(),
        "shortening_chord_typing": audit_decorated_chord_typing(),
        "theorem": (
            "two nonzero matching monomials in one decorated coefficient "
            "word reduce componentwise without new cells; a remaining "
            "single C_(2r), r>=3, reduces to C4 plus C_(2r-2) after one "
            "nonzero distance-three chord"
        ),
        "source_validity": (
            "whole-component switches preserve the output word and use only "
            "already nonzero decorated cells; the chorded switch also "
            "preserves the word, and uses exactly one new decorated cell"
        ),
        "exact_missing_lemma": (
            "for a nonzero k3 quotient-minor contribution not already in "
            "the common-tail class, synchronize its two determinant "
            "orientations into one output word and force a nonzero "
            "distance-three shortening chord, or prove that their selected "
            "hole families are cross-intersecting and hence star/triangle/"
            "K2,2 Hall; if every available chord is diagonal, the residual "
            "is the diagonal cycle web"
        ),
        "scope": (
            "uniform matching-exchange proof with bounded formula audits; "
            "does not infer a chord from the five aggregate response rows"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"unequal-tail reduction ledger changed: {digest}")
    print("uniform k3 unequal-tail reduction: PASS")
    print("multi-component tails reduce with no new cells")
    print("C_(2r) shortens via one chord to C4+C_(2r-2)")
    print("missing lemma: word synchronization + chord-or-Hall")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
