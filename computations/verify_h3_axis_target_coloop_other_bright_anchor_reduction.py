#!/usr/bin/env python3
"""Add the mandatory other bright anchor to the 50 no-cross residuals.

For each of the 50 graph triples (M,N,K) left by the forced-unary E3
landing, superpose every possible other bright pure matching L.  The 4500
quadruples have a sharp incidence split.  Almost all expose an edge of the
active outside matching N beyond the three selected anchors M,K,L.  The
fully anchor-contained cases either contain literal crossed response bases,
or reduce to two forms: L=N as an undecorated matching, or L triangle N a
single residual C4 with identical endpoint ports.

The checker separates graph incidence from decorated activity.  An external
endpoint edge is an active good arm at a support-minimal representative; an
external residual q-edge requires the pinned off-diagonal theorem unless its
decoration is diagonal.  This scope guard is part of the theorem.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_one_sided_column_route.py":
        "1906c696dc6af9785fd850c20f148ad47034e518c4a94a38b3e668043ecb29a6",
    "notes/h3-axis-target-coloop-one-sided-column-route.md":
        "29f4e545480d87d75f3de687f38d4dcef5ef17ecc4039f337aa032806c138a02",
    "computations/verify_h3_axis_target_coloop_one_sided_companion_boundary.py":
        "6cb34278cccf9327bdfccdece0b254f3eff95d179e512e80e1c938d4fe0eef62",
    "notes/h3-axis-target-coloop-one-sided-companion-boundary.md":
        "ce93379f949002eaf05f24975b902760d9dcd7095e4150bf132259c73a498393",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
}
EXPECTED_LEDGER_SHA256 = (
    "f74c8f56ddb24cf6452eef80e7f89c346619683c99279cd81afd793b0e760af2"
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


def partner(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError((matching, site))


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


P, S = 6, 7
TARGET_HOLES = (0, 1)
OUTSIDE_HOLES = (2, 3)
COMMON = (4, 5)
CROSSED_PORTS = ((2, 1), (0, 3))


def response_pairs():
    records = []
    for target_tail in perfect_matchings(OUTSIDE_HOLES + COMMON):
        for outside_tail in perfect_matchings(TARGET_HOLES + COMMON):
            target = tuple(sorted((edge(P, 0), edge(S, 1)) + target_tail))
            outside = tuple(sorted((edge(P, 2), edge(S, 3)) + outside_tail))
            cycles = cycle_lengths(target, outside)
            if cycles in ((6,), (8,)):
                records.append((target, outside, cycles))
    require(len(records) == 7,
            "the single-C6/C8 response-pair count changed")
    return tuple(records)


def crossed_matchings(union, all_matchings):
    return tuple(matching for matching in all_matchings
                 if set(matching) <= union
                 and (partner(matching, P), partner(matching, S))
                 in CROSSED_PORTS)


def owner_word(matching, anchors):
    """Choose selected-anchor decorations and return the induced word.

    Each selected pure anchor has a constant colour.  For endpoint edges in
    a crossed matching the owner is forced by its port.  Residual edges may
    have several owners; choosing the least colour is enough to prove a
    literal nonzero selected-cell product exists.
    """
    word = [None] * 8
    owners = []
    for pair in matching:
        choices = tuple(sorted(colour for colour, anchor in anchors.items()
                               if pair in anchor))
        require(choices, "a contained crossed edge lost every anchor owner")
        if P in pair:
            other = pair[0] if pair[1] == P else pair[1]
            colour = 1 if other == 0 else 2
            require(colour in choices,
                    "a crossed P-port lost its selected pure owner")
        elif S in pair:
            other = pair[0] if pair[1] == S else pair[1]
            colour = 1 if other == 1 else 2
            require(colour in choices,
                    "a crossed S-port lost its selected pure owner")
        else:
            colour = choices[0]
        owners.append((pair, colour))
        word[pair[0]] = word[pair[1]] = colour
    require(all(value is not None for value in word),
            "the anchor-owned crossed matching did not fill its word")
    return tuple(word), tuple(owners)


def audit_other_bright_anchor_reduction():
    all_matchings = tuple(perfect_matchings(range(8)))
    unary_bases = tuple(tuple(sorted((edge(P, S),) + tail))
                        for tail in perfect_matchings(range(6)))
    bright_bases = tuple(matching for matching in all_matchings
                         if edge(P, S) not in matching)
    require(len(all_matchings) == 105 and len(unary_bases) == 15
            and len(bright_bases) == 90,
            "the K8/unary/bright matching counts changed")

    no_cross_triples = []
    for target, outside, cycles in response_pairs():
        for unary in unary_bases:
            union = set(target) | set(outside) | set(unary)
            if not crossed_matchings(union, all_matchings):
                no_cross_triples.append((target, outside, unary, cycles))
    require(len(no_cross_triples) == 50,
            "the pinned no-cross triple count changed")

    outcome = Counter()
    external_count = Counter()
    residual_forms = Counter()
    crossed_literal_records = []
    canonical = {}
    records = []
    for target, outside, unary, cycles in no_cross_triples:
        for bright in bright_bases:
            anchor_union = set(target) | set(unary) | set(bright)
            external = set(outside) - anchor_union
            endpoint_external = tuple(sorted(
                pair for pair in external if P in pair or S in pair
            ))
            residual_external = tuple(sorted(
                pair for pair in external if P not in pair and S not in pair
            ))
            external_count[(len(external), bool(endpoint_external))] += 1

            # A crossed matching is routed here only when it is already in
            # the *selected-anchor* union.  Allowing N to supply an edge
            # would be a bare graph recombination, not a product of selected
            # nonzero anchor decorations.
            crossed = crossed_matchings(anchor_union, all_matchings)
            if crossed:
                kind = "selected_anchor_crossed"
            elif endpoint_external:
                kind = "external_endpoint_arm"
            elif residual_external:
                kind = "external_residual_q_only"
            elif bright == outside:
                kind = "same_base_word_change"
            else:
                difference_cycles = cycle_lengths(bright, outside)
                require(partner(bright, P) == partner(outside, P) == 2
                        and partner(bright, S) == partner(outside, S) == 3,
                        "an anchor-contained residual changed endpoint ports")
                require(difference_cycles == (4,),
                        "an anchor-contained residual stopped being one C4")
                kind = "residual_C4_word_change"

            outcome[kind] += 1
            if kind in ("same_base_word_change", "residual_C4_word_change"):
                residual_forms[(cycles, kind)] += 1
                canonical.setdefault(kind, {
                    "M": target, "N": outside,
                    "K": unary, "L": bright,
                })
            if kind == "selected_anchor_crossed":
                anchors = {0: unary, 1: target, 2: bright}
                for matching in crossed:
                    word, owners = owner_word(matching, anchors)
                    endpoint_labels = (word[P], word[S])
                    require(endpoint_labels in ((2, 1), (1, 2)),
                            "a crossed selected-anchor monomial lost its labels")
                    require(len(set(word)) >= 2,
                            "a crossed selected-anchor word became pure")
                    crossed_literal_records.append({
                        "matching": matching,
                        "word": word,
                        "endpoint_labels": endpoint_labels,
                        "selected_anchor_owners": owners,
                    })
            records.append({
                "MN_cycle": cycles,
                "kind": kind,
                "outside_external_edges": tuple(sorted(external)),
                "crossed_matching_count": len(crossed),
            })

    require(len(records) == 50 * 90 == 4500,
            "the no-cross/other-bright quadruple census changed")
    require(outcome == Counter({
        "selected_anchor_crossed": 612,
        "external_endpoint_arm": 3778,
        "external_residual_q_only": 48,
        "same_base_word_change": 50,
        "residual_C4_word_change": 12,
    }), f"the other-bright outcome split changed: {outcome}")
    require(sum(outcome.values()) == 4500,
            "the other-bright outcomes stopped partitioning the census")
    require(len(crossed_literal_records) == 644
            and Counter(record["endpoint_labels"]
                        for record in crossed_literal_records)
            == Counter({(2, 1): 322, (1, 2): 322}),
            "the anchor-owned crossed monomials changed")
    require(residual_forms == Counter({
        ((8,), "same_base_word_change"): 40,
        ((6,), "same_base_word_change"): 10,
        ((8,), "residual_C4_word_change"): 8,
        ((6,), "residual_C4_word_change"): 4,
    }), f"the 62 residual cycle split changed: {residual_forms}")

    expected_same = {
        "M": ((0, 6), (1, 7), (2, 3), (4, 5)),
        "N": ((0, 1), (2, 6), (3, 7), (4, 5)),
        "K": ((0, 1), (2, 3), (4, 5), (6, 7)),
        "L": ((0, 1), (2, 6), (3, 7), (4, 5)),
    }
    expected_c4 = {
        "M": ((0, 6), (1, 7), (2, 3), (4, 5)),
        "N": ((0, 1), (2, 6), (3, 7), (4, 5)),
        "K": ((0, 1), (2, 3), (4, 5), (6, 7)),
        "L": ((0, 4), (1, 5), (2, 6), (3, 7)),
    }
    require(canonical == {
        "same_base_word_change": expected_same,
        "residual_C4_word_change": expected_c4,
    }, f"the canonical residual representatives changed: {canonical}")

    return {
        "no_cross_triples": len(no_cross_triples),
        "other_bright_bases": len(bright_bases),
        "quadruples": len(records),
        "outcome_histogram": dict(sorted(outcome.items())),
        "outside_edge_histogram_(count,has_endpoint)": {
            str(key): value for key, value in sorted(external_count.items())
        },
        "anchor_owned_crossed_cases": outcome["selected_anchor_crossed"],
        "anchor_owned_crossed_monomial_count": len(crossed_literal_records),
        "anchor_owned_crossed_monomial_endpoint_histogram": {
            str(key): value for key, value in sorted(Counter(
                record["endpoint_labels"]
                for record in crossed_literal_records
            ).items())
        },
        "anchor_owned_crossed_representative": crossed_literal_records[0],
        "residual_cycle_histogram": {
            str(key): value for key, value in sorted(residual_forms.items())
        },
        "canonical_residuals": canonical,
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
        "mandatory_other_bright_anchor": audit_other_bright_anchor_reduction(),
        "positive_routing": (
            "an endpoint edge of the active outside matching beyond all "
            "three selected anchors is an occupied outside star component. "
            "At support minimum its complete response column is nonzero, "
            "and the three anchor matchings give deleted-star rank three at "
            "both endpoints.  In the 612 selected-anchor-crossed "
            "quadruples, each crossed matching is a product of already selected "
            "nonzero anchor decorations and lies in a literal crossed zero row"
        ),
        "residual_q_guard": (
            "48 quadruples expose only residual q-edges of N after the "
            "selected-anchor-crossed cases are removed.  A nonzero "
            "off-diagonal decoration on one routes by the pinned nonanchor "
            "theorem.  If every such decoration is diagonal, graph incidence "
            "alone supplies neither an endpoint arm nor an active minor"
        ),
        "sharp_coefficient_gate": (
            "after the graph-positive routes, the fully anchor-contained "
            "no-cross boundary has exactly two forms: 50 same-base cases "
            "where N=L physically but the selected mixed and pure-bright "
            "decorations differ, and 12 cases where N and L have the same "
            "endpoint ports and differ by one residual C4.  The next source "
            "identity is respectively a same-base word-change or a labelled "
            "residual-C4 exchange; no other matching topology remains"
        ),
        "scope": (
            "exact h=3 physical matching-incidence theorem.  A graph-crossed "
            "case is promoted only because its displayed monomial uses "
            "selected nonzero anchor decorations.  The 82 diagonal "
            "residual-q exits and the 62 word-change forms remain coefficient "
            "gates; no decorated activity is inferred from a bare edge"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"other-bright-anchor ledger changed: {digest}")
    print("h3 target-coloop other-bright-anchor reduction: PASS")
    print("50 no-cross triples x 90 bright anchors = 4500 quadruples")
    print("anchor-cross / endpoint exit / residual-q-only / same / C4: 612/3778/48/50/12")
    print("anchor-contained coefficient gates: same-base word change or residual C4")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
