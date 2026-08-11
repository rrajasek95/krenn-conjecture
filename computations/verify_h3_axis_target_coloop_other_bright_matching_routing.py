#!/usr/bin/env python3
"""Route the mandatory other-bright pure matching through the 50 residuals.

For every no-cross triple (M,N,K) from the physical unary E3 landing, add
every physical perfect matching L which can support the other bright pure
target.  Matchings containing P--S are excluded because the normalized
direct block has only its 00 cell.

Classify in proof priority: a crossed response skeleton in the three-pure-
anchor union; otherwise an active endpoint arm of N outside that union;
otherwise an external edge of N is only a residual-q edge; otherwise a
distinct N matching inside the pure-anchor union (the anchor-contained Hall
web); otherwise the only remaining possibility is L=N.  The residual-q and
same-skeleton cases are genuine label obstructions: physical incidence alone
does not determine the q-cell decorations needed by the downstream routes.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_common_covector_k22_scope.py":
        "6de8935cae41f03e71141850b63b9fd167418bb1cebe0575ce0f3de03e8386b3",
    "notes/h3-axis-target-coloop-common-covector-k22-scope.md":
        "d083a5d967175ac26f32b252d03b57ae22aff81a661889e012e5a1b781378a31",
    "computations/verify_h3_axis_target_coloop_one_sided_companion_boundary.py":
        "6cb34278cccf9327bdfccdece0b254f3eff95d179e512e80e1c938d4fe0eef62",
    "notes/h3-axis-target-coloop-one-sided-companion-boundary.md":
        "ce93379f949002eaf05f24975b902760d9dcd7095e4150bf132259c73a498393",
    "computations/verify_uniform_hall_terminal_transfer_bistar_curvature_boundary.py":
        "aa1da69a09c3c34f90024a42b27ab0d0a30b0c1263a6a059d256ff085084c048",
    "notes/uniform-hall-terminal-transfer-bistar-curvature-boundary.md":
        "07523ffcef85b86c0b0808ddec43f1731c99f4426451f0e22171f864e82949aa",
}
EXPECTED_LEDGER_SHA256 = "1b20cd6d8ca11706716617efafcf8729db2642e9391e7917ad40d089c8dd29e1"


P, S = 6, 7
TARGET_HOLES = (0, 1)
OUTSIDE_HOLES = (2, 3)
COMMON = (4, 5)


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


def crossed_port(matching):
    return (partner(matching, P), partner(matching, S)) in ((0, 3), (2, 1))


def response_pairs():
    target_tails = tuple(perfect_matchings(OUTSIDE_HOLES + COMMON))
    outside_tails = tuple(perfect_matchings(TARGET_HOLES + COMMON))
    records = []
    for target_tail in target_tails:
        for outside_tail in outside_tails:
            target = tuple(sorted((edge(P, 0), edge(S, 1)) + target_tail))
            outside = tuple(sorted((edge(P, 2), edge(S, 3)) + outside_tail))
            cycles = cycle_lengths(target, outside)
            if cycles in ((6,), (8,)):
                records.append((target, outside, cycles[0]))
    require(len(records) == 7, "the single-cycle response count changed")
    return tuple(records)


def no_cross_unary_triples(all_matchings):
    unary = tuple(tuple(sorted((edge(P, S),) + tail))
                  for tail in perfect_matchings(range(6)))
    records = []
    for target, outside, cycle in response_pairs():
        for direct in unary:
            union = set(target) | set(outside) | set(direct)
            contained = tuple(matching for matching in all_matchings
                              if set(matching) <= union)
            if not any(crossed_port(matching) for matching in contained):
                records.append((target, outside, direct, cycle))
    require(len(records) == 50,
            "the no-cross unary triple count changed")
    require(Counter(record[3] for record in records)
            == Counter({8: 40, 6: 10}),
            "the no-cross C6/C8 split changed")
    return tuple(records)


def classify_other_bright_matchings():
    all_matchings = tuple(perfect_matchings(range(8)))
    bright_matchings = tuple(matching for matching in all_matchings
                             if edge(P, S) not in matching)
    require(len(all_matchings) == 105 and len(bright_matchings) == 90,
            "the full/bright matching counts changed")

    categories = Counter()
    by_cycle = Counter()
    records = []
    label_obstructions = []
    residual_q_obstructions = []
    hall_records = []
    raw_residual_q_only = Counter()
    for triple_index, (target, outside, direct, cycle) in enumerate(
            no_cross_unary_triples(all_matchings)):
        for other_bright in bright_matchings:
            pure_anchor_union = (
                set(target) | set(direct) | set(other_bright)
            )
            anchor_matchings = tuple(
                matching for matching in all_matchings
                if set(matching) <= pure_anchor_union
            )
            crossed = tuple(matching for matching in anchor_matchings
                            if crossed_port(matching))
            outside_edges = tuple(sorted(set(outside) - pure_anchor_union))
            outside_endpoint_edges = tuple(
                exterior for exterior in outside_edges
                if P in exterior or S in exterior
            )
            q_only_external = bool(outside_edges) and not outside_endpoint_edges
            if q_only_external:
                raw_residual_q_only[(cycle, bool(crossed))] += 1

            if crossed:
                category = "crossed_response_skeleton"
            elif outside_endpoint_edges:
                category = "active_N_has_external_endpoint_arm"
            elif outside_edges:
                category = "external_residual_q_only"
                require(q_only_external,
                        "a residual-q record acquired an endpoint arm")
                residual_q_obstructions.append({
                    "triple": triple_index,
                    "cycle": cycle,
                    "M": target,
                    "N": outside,
                    "K": direct,
                    "L": other_bright,
                    "external_residual_q_edges": outside_edges,
                })
            elif other_bright != outside:
                category = "anchor_contained_strict_Hall_web"
                require(outside in anchor_matchings
                        and outside not in (target, direct, other_bright),
                        "a claimed strict Hall record lost its fourth matching")
                hall_records.append({
                    "triple": triple_index,
                    "cycle": cycle,
                    "M": target,
                    "N": outside,
                    "K": direct,
                    "L": other_bright,
                    "anchor_union_matching_count": len(anchor_matchings),
                })
            else:
                category = "same_skeleton_label_obstruction"
                require(other_bright == outside
                        and not crossed and not outside_edges,
                        "the label obstruction classification changed")
                label_obstructions.append({
                    "triple": triple_index,
                    "cycle": cycle,
                    "M": target,
                    "N_mixed_and_L_other_bright": outside,
                    "K": direct,
                    "anchor_union_matching_count": len(anchor_matchings),
                })
            categories[category] += 1
            by_cycle[(cycle, category)] += 1
            records.append((triple_index, other_bright, category))

    expected = Counter({
        "crossed_response_skeleton": 612,
        "active_N_has_external_endpoint_arm": 3778,
        "external_residual_q_only": 48,
        "anchor_contained_strict_Hall_web": 12,
        "same_skeleton_label_obstruction": 50,
    })
    require(categories == expected,
            f"the mandatory-other-bright routing count changed: {categories}")
    require(len(records) == 50 * 90 == 4500,
            "the mandatory-other-bright census size changed")
    require(by_cycle == Counter({
        (6, "crossed_response_skeleton"): 130,
        (6, "active_N_has_external_endpoint_arm"): 746,
        (6, "external_residual_q_only"): 10,
        (6, "anchor_contained_strict_Hall_web"): 4,
        (6, "same_skeleton_label_obstruction"): 10,
        (8, "crossed_response_skeleton"): 482,
        (8, "active_N_has_external_endpoint_arm"): 3032,
        (8, "external_residual_q_only"): 38,
        (8, "anchor_contained_strict_Hall_web"): 8,
        (8, "same_skeleton_label_obstruction"): 40,
    }), f"the C6/C8 routing split changed: {by_cycle}")
    require(len(label_obstructions) == 50
            and {record["triple"] for record in label_obstructions}
            == set(range(50)),
            "one no-cross triple lost its L=N label obstruction")
    require(len(hall_records) == 12,
            "the strict Hall web record count changed")
    require(len(residual_q_obstructions) == 48,
            "the priority residual-q obstruction count changed")
    require(raw_residual_q_only == Counter({
        (6, False): 10,
        (6, True): 4,
        (8, False): 38,
        (8, True): 30,
    }), f"the raw residual-q guard changed: {raw_residual_q_only}")

    first = label_obstructions[0]
    require(first == {
        "triple": 0,
        "cycle": 6,
        "M": ((0, 6), (1, 7), (2, 3), (4, 5)),
        "N_mixed_and_L_other_bright":
            ((0, 1), (2, 6), (3, 7), (4, 5)),
        "K": ((0, 1), (2, 3), (4, 5), (6, 7)),
        "anchor_union_matching_count": 3,
    }, "the smallest same-skeleton label obstruction changed")

    first_q = residual_q_obstructions[0]
    require(first_q == {
        "triple": 3,
        "cycle": 6,
        "M": ((0, 6), (1, 7), (2, 3), (4, 5)),
        "N": ((0, 1), (2, 6), (3, 7), (4, 5)),
        "K": ((0, 2), (1, 3), (4, 5), (6, 7)),
        "L": ((0, 4), (1, 5), (2, 6), (3, 7)),
        "external_residual_q_edges": ((0, 1),),
    }, "the smallest external residual-q obstruction changed")

    return {
        "no_cross_triples": 50,
        "allowed_other_bright_matchings_per_triple": 90,
        "total_quadruples": len(records),
        "priority_routing_counts": dict(categories),
        "cycle_routing_counts": {
            f"C{cycle}:{category}": count
            for (cycle, category), count in sorted(by_cycle.items())
        },
        "strict_Hall_records": hall_records,
        "raw_residual_q_only_count": sum(raw_residual_q_only.values()),
        "raw_residual_q_only_crossed_overlap": sum(
            count for (cycle, has_crossed), count in raw_residual_q_only.items()
            if has_crossed
        ),
        "residual_q_obstructions": residual_q_obstructions,
        "label_obstructions": label_obstructions,
        "smallest_residual_q_obstruction": first_q,
        "smallest_label_obstruction": first,
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    routing = classify_other_bright_matchings()
    ledger = {
        "pins": PINS,
        "mandatory_other_bright_routing": routing,
        "theorem": (
            "after selecting a literal other-bright pure target matching L, "
            "612 pure-anchor unions contain a crossed response skeleton; "
            "3778 leave an active endpoint arm of N off the pure anchors; "
            "48 leave only external residual-q edges; 12 contain N as a "
            "genuinely fourth anchor-contained matching and enter the "
            "strict Hall matching web; and 50 have L=N.  Thus topology "
            "routes 4402 cases and leaves 98 label-sensitive packets"
        ),
        "label_obstruction": (
            "there are two sharp physical-incidence boundaries.  In 48 "
            "priority cases N has external edges, but every such edge is a "
            "residual-q edge whose decoration may be diagonal; no endpoint-"
            "arm or offdiagonal-label route is certified.  Separately, every "
            "one of the 50 no-cross triples admits the same-skeleton escape: the physical "
            "outside matching N also carries the other-bright pure "
            "decoration.  It adds no physical matching or edge.  Deciding "
            "this branch requires coefficient labels/common-q rows, not "
            "another perfect-matching union theorem"
        ),
        "route_scope": (
            "crossed skeleton is a physical landing candidate and the "
            "external-endpoint category has a literal active N arm.  Of 82 "
            "raw residual-q-only external-edge cases, 34 already lie in the "
            "crossed category and 48 remain after priority.  The 12 Hall "
            "records are exact four-base anchor-contained matching webs; "
            "their downstream source typing is delegated to the pinned "
            "Hall/lock theorems.  No coefficient feasibility is asserted "
            "for the 48 residual-q or 50 same-skeleton label packets"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"other-bright matching routing ledger changed: {digest}")
    print("h3 target-coloop mandatory other-bright routing: PASS")
    print("4500 cases -> crossed 612 / endpoint 3778 / q-only 48 / Hall 12 / label 50")
    print("raw residual-q-only 82 = crossed overlap 34 + priority residual 48")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
