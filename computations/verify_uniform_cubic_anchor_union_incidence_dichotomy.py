#!/usr/bin/env python3
"""Classify cubic decorated matchings inside a three-matching anchor union.

For three selected pure matchings Q0,Q1,Q2 on six sites and a physical
perfect matching R contained in their union, either R has a multiplicity-one
edge, or at least two Qc equal R.  In the latter case the third matching
shares 0, 1, or 3 edges with R, giving exactly the three multiplicity
patterns (2,2,2), (2,2,3), and (3,3,3).

At a multiplicity-one edge, the two other selected matchings block at most
two companion neighbours at either endpoint, leaving at least N-4=2 free
sites.  With the alternating target repair assumed by the anchor-edge
branch, c78fc9b lands unless every active product is trapped on those one
or two blocked neighbours.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_anchor_edge_offdiagonal_alternating_exit_dichotomy.py":
        "2de838ff96118a7c54df23c8df02202090a52a3b0ca83f62c400a7a8241f37b8",
    "notes/uniform-anchor-edge-offdiagonal-alternating-exit-dichotomy.md":
        "9b4d2dabf493845de4570008835d544cdb0a9591c5272758e5390f19e70bdc02",
    "computations/verify_uniform_diagonal_aggregate_offdiagonal_quadratic_defect.py":
        "cdf5a71f6f5dcef524c22c9790f0a29bf902ddf8e58bccb7b5233655f0359f07",
    "notes/uniform-diagonal-aggregate-offdiagonal-quadratic-defect.md":
        "9aa57c618f3ae8bca6b335fb050c881039e70449f6798240a50ba28429e667fb",
    "computations/verify_uniform_diagonal_aggregate_offdiagonal_cubic_defect.py":
        "9bea51acfdf30c679bcb1ceb1c5de693df18234359d5bfbac61175da3fccf987",
    "notes/uniform-diagonal-aggregate-offdiagonal-cubic-defect.md":
        "af29dafb11463813f9be0a37c22337659b9fdb5d6c6b40548cfea566eda92d04",
}
EXPECTED_LEDGER_SHA256 = (
    "fc2232f6fac0f896a7c70da2a557fdbb924c3be857cc6b3bd860450be4241336"
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
    left = vertices[0]
    for index in range(1, len(vertices)):
        right = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield tuple(sorted((edge(left, right),) + tail))


def partner(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError(f"site {site} is absent from {matching}")


def act_matching(matching, permutation):
    return tuple(sorted(edge(permutation[left], permutation[right])
                        for left, right in matching))


SITE_PERMUTATIONS = tuple(itertools.permutations(range(6)))
COLOUR_PERMUTATIONS = tuple(itertools.permutations(range(3)))


def canonical_state(selected, decorated):
    best = None
    for permutation in SITE_PERMUTATIONS:
        image_r = act_matching(decorated, permutation)
        image_q = tuple(act_matching(matching, permutation)
                        for matching in selected)
        for colour_permutation in COLOUR_PERMUTATIONS:
            state = (image_r, tuple(image_q[index]
                                    for index in colour_permutation))
            if best is None or state < best:
                best = state
    return best


def multiply_used_structure(selected, decorated, multiplicity):
    """Verify the two-equal-matchings proof, not merely its census."""
    shares = tuple(len(set(matching) & set(decorated))
                   for matching in selected)
    require(sum(shares) == sum(multiplicity[pair] for pair in decorated),
            "anchor incidence was not counted in both directions")
    require(max(shares) >= 2,
            "six decorated incidences did not pigeonhole into one colour")
    # Two perfect matchings sharing two edges on six sites share the third.
    for matching, shared in zip(selected, shares, strict=True):
        if shared >= 2:
            require(matching == decorated,
                    "a K6 perfect matching shared exactly two edges")
    equal = sum(matching == decorated for matching in selected)
    require(equal >= 2,
            "the first equal matching did not force a second one")
    third_intersection = next((len(set(matching) & set(decorated))
                               for matching in selected
                               if matching != decorated), 3)
    require(third_intersection in (0, 1, 3),
            "two K6 perfect matchings acquired a two-edge intersection")
    return {
        "selected_matching_intersections_with_R": sorted(shares),
        "selected_matchings_equal_R": equal,
        "third_matching_intersection": third_intersection,
    }


def unique_edge_free_sites(selected, decorated, multiplicity):
    audits = []
    for decorated_edge in decorated:
        colours = tuple(index for index, matching in enumerate(selected)
                        if decorated_edge in matching)
        if len(colours) != 1:
            continue
        colour = colours[0]
        others = tuple(index for index in range(3) if index != colour)
        for centre in decorated_edge:
            other_endpoint = (set(decorated_edge) - {centre}).pop()
            blocked = {partner(selected[index], centre) for index in others}
            require(other_endpoint not in blocked,
                    "a multiplicity-one edge remained in another matching")
            free = set(range(6)) - {centre, other_endpoint} - blocked
            require(len(free) >= 2,
                    "the other two colours blocked more than two sites")
            audits.append({
                "edge": decorated_edge,
                "selected_colour": colour,
                "centre": centre,
                "blocked_anchor_neighbours": tuple(sorted(blocked)),
                "free_active_sites": tuple(sorted(free)),
            })
    require(audits, "the declared unique-edge state had no unique edge")
    return audits


def audit_complete_k6_classification():
    matchings = tuple(perfect_matchings(range(6)))
    require(len(matchings) == 15, "the K6 matching count changed")
    pattern_histogram = Counter()
    fully_multiply_used_orbits = defaultdict(set)
    unique_states = 0
    minimum_free_sites = 6
    state_count = 0
    multiply_structure_records = {}

    for selected in itertools.product(matchings, repeat=3):
        multiplicity = Counter(pair for matching in selected
                               for pair in matching)
        union = set(multiplicity)
        for decorated in matchings:
            if not set(decorated) <= union:
                continue
            state_count += 1
            pattern = tuple(sorted(multiplicity[pair]
                                   for pair in decorated))
            pattern_histogram[pattern] += 1
            if min(pattern) == 1:
                unique_states += 1
                audits = unique_edge_free_sites(
                    selected, decorated, multiplicity)
                minimum_free_sites = min(
                    minimum_free_sites,
                    *(len(record["free_active_sites"])
                      for record in audits),
                )
                continue

            require(pattern in ((2, 2, 2), (2, 2, 3), (3, 3, 3)),
                    f"an unexpected fully multiply-used pattern appeared: {pattern}")
            structure = multiply_used_structure(
                selected, decorated, multiplicity)
            multiply_structure_records.setdefault(pattern, structure)
            fully_multiply_used_orbits[pattern].add(
                canonical_state(selected, decorated))

    expected_histogram = Counter({
        (1, 1, 1): 3600,
        (1, 1, 2): 4320,
        (1, 1, 3): 540,
        (1, 2, 2): 1080,
        (2, 2, 2): 360,
        (2, 2, 3): 270,
        (3, 3, 3): 15,
    })
    require(state_count == 10185,
            f"the anchor-union decorated-matching count changed: {state_count}")
    require(pattern_histogram == expected_histogram,
            f"the multiplicity histogram changed: {pattern_histogram}")
    require(unique_states == 9540 and minimum_free_sites == 2,
            "the unique-edge/free-site split changed")
    require({pattern: len(orbits)
             for pattern, orbits in fully_multiply_used_orbits.items()}
            == {(2, 2, 2): 1, (2, 2, 3): 1, (3, 3, 3): 1},
            "a fully multiply-used pattern split into another orbit")

    representatives = {
        "222": {
            "R": ((0, 1), (2, 3), (4, 5)),
            "selected": (
                ((0, 1), (2, 3), (4, 5)),
                ((0, 1), (2, 3), (4, 5)),
                ((0, 2), (1, 4), (3, 5)),
            ),
        },
        "223": {
            "R": ((0, 1), (2, 3), (4, 5)),
            "selected": (
                ((0, 1), (2, 3), (4, 5)),
                ((0, 1), (2, 3), (4, 5)),
                ((0, 1), (2, 4), (3, 5)),
            ),
        },
        "333": {
            "R": ((0, 1), (2, 3), (4, 5)),
            "selected": (
                ((0, 1), (2, 3), (4, 5)),
                ((0, 1), (2, 3), (4, 5)),
                ((0, 1), (2, 3), (4, 5)),
            ),
        },
    }
    for key, representative in representatives.items():
        pattern = tuple(sorted(Counter(
            pair for matching in representative["selected"]
            for pair in matching
        )[pair] for pair in representative["R"]))
        require("".join(map(str, pattern)) == key,
                f"the {key} representative has pattern {pattern}")

    return {
        "selected_matching_triples": len(matchings) ** 3,
        "anchor_union_decorated_matching_states": state_count,
        "multiplicity_pattern_histogram": {
            "".join(map(str, pattern)): count
            for pattern, count in sorted(pattern_histogram.items())
        },
        "states_with_a_multiplicity_one_edge": unique_states,
        "minimum_free_active_sites_at_a_unique_edge_endpoint":
            minimum_free_sites,
        "fully_multiply_used": {
            "states": sum(pattern_histogram[pattern]
                          for pattern in ((2, 2, 2),
                                          (2, 2, 3),
                                          (3, 3, 3))),
            "orbit_counts": {
                "".join(map(str, pattern)): len(orbits)
                for pattern, orbits in fully_multiply_used_orbits.items()
            },
            "structure": {
                "".join(map(str, pattern)): record
                for pattern, record in multiply_structure_records.items()
            },
            "representatives": representatives,
        },
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger = {
        "complete_k6_incidence_classification":
            audit_complete_k6_classification(),
        "uniform_dichotomy": (
            "a cubic decorated perfect matching inside Q0 union Q1 union "
            "Q2 either has a multiplicity-one edge, where c78fc9b leaves "
            "only active support trapped on at most two anchor neighbours, "
            "or at least two selected matchings equal the decorated "
            "matching and the third intersects it in 0, 1, or 3 edges"
        ),
        "finite_coefficient_residual": (
            "the three fully multiply-used web types 222, 223, 333, plus "
            "the multiplicity-one states whose active products are trapped"
        ),
        "concentrated_01_10_cubic_landing": (
            "the pinned cubic aggregate theorem gives an ordinary source "
            "unit for all 120 decorated perfect matchings in 32 exact "
            "orbits; in its selected-anchor specialization all 1960 "
            "decorated anchor-union configurations, including the 222 and "
            "223 multiply-used types and every trapped unique-edge type, "
            "are therefore coefficient-empty"
        ),
        "scope": (
            "physical selected-matching incidence on six residual sites; "
            "the alternating pure-target repair and nonzero active products "
            "are source hypotheses inherited from c78fc9b"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"cubic anchor-union incidence ledger changed: {digest}")
    print("uniform cubic anchor-union incidence dichotomy: PASS")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
