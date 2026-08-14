#!/usr/bin/env python3
"""One-edge augmentations of the smallest support-16 local cap guard.

Start with graph 11 and directed block 2->02 from the complete support-16
binary-cap audit.  Its canonical two-coordinate anchor chart has twelve
singleton mixed fibres.  This checker adds each of the twelve missing graph
edges in each of the three coordinate colours, recomputes literal matching
fibres and every physical cap response through X20, and tests the complete
private/binary active-clean criteria.

The desired recurrence is exact at this first support-17 layer: every
augmentation either creates a certified cap landing or leaves a singleton
mixed fibre.  In particular no one edge can mate all debts while remaining
cap-dark.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "314147655e0b064446414ff99ad10f967b13d53a212e3f2840a18024e36291b3"
COLORS = (0, 1, 2)
NONANCHOR = -1
N = 8


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_local(module_name, filename):
    spec = spec_from_file_location(module_name, HERE / filename)
    require(spec is not None and spec.loader is not None,
            ("failed to load dependency", filename))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BINARY = load_local(
    "n8_support16_binary_cover_for_support17_augmentation",
    "verify_n8_support16_all_binary_residue_two_cap_cover.py",
)
ORBIT = BINARY.ORBIT
PROTOTYPE = BINARY.PROTOTYPE

BASE_EDGES = (
    (0, 1), (0, 2), (0, 3), (0, 5), (0, 7),
    (1, 3), (1, 4), (1, 5), (1, 6),
    (2, 4), (2, 5), (2, 7),
    (3, 4), (3, 7), (4, 6), (5, 6),
)
TARGET_INCIDENCE = (2, (0, 2))
TARGET_EDGE = TARGET_INCIDENCE[1]
BASE_STATES = {
    (0, 1): 0,
    (0, 2): NONANCHOR,
    (0, 3): 0,
    (0, 5): 1,
    (0, 7): 2,
    (1, 3): 1,
    (1, 4): 0,
    (1, 5): 0,
    (1, 6): 2,
    (2, 4): 0,
    (2, 5): 2,
    (2, 7): 1,
    (3, 4): 2,
    (3, 7): 0,
    (4, 6): 1,
    (5, 6): 0,
}
TARGET_SUPPORT = (1, 2)


def mixed_singletons(words):
    return tuple(sorted(
        word for word, multiplicity in words.items()
        if len(set(word)) > 1 and multiplicity == 1
    ))


def response_shapes_and_exits(edges, states):
    adjacency = ORBIT.adjacency_from_edges(edges)
    shapes = []
    private_caps = []
    for cap_edge in edges:
        if TARGET_INCIDENCE[0] not in cap_edge:
            continue
        through, residue = PROTOTYPE.cap_shape(
            adjacency, edges, TARGET_INCIDENCE, cap_edge
        )
        if not through:
            continue
        shapes.append((cap_edge, len(through), len(residue)))
        if not residue:
            private_caps.append(cap_edge)

    binary = BINARY.binary_faces(
        adjacency, edges, TARGET_INCIDENCE, tuple(shapes)
    )
    landing_binary = tuple(
        face for face in binary
        if BINARY.face_lands(face, states, zero_coordinate=0)
    )
    return {
        "response_shapes": tuple(shapes),
        "private_caps": tuple(private_caps),
        "binary_faces": binary,
        "landing_binary_faces": landing_binary,
    }


def audit_base_guard():
    terminal_records = ORBIT.terminal_two_rrx_records()
    require(tuple(terminal_records[11]["representative_edges"]) == BASE_EDGES,
            ("graph-11 support changed",
             terminal_records[11]["representative_edges"]))
    require(set(BASE_STATES) == set(BASE_EDGES),
            ("base anchor chart has wrong edge support", BASE_STATES,
             BASE_EDGES))
    words = BINARY.matching_word_histogram(
        BASE_EDGES, TARGET_EDGE, BASE_STATES, TARGET_SUPPORT
    )
    pure = tuple(words[(colour,) * N] for colour in COLORS)
    singletons = mixed_singletons(words)
    require(pure == (1, 1, 1) and len(singletons) == 12,
            ("base graph-11 word profile changed", pure, singletons, words))
    response = response_shapes_and_exits(BASE_EDGES, BASE_STATES)
    require(response["response_shapes"]
            == (((2, 4), 12, 4), ((2, 5), 4, 4))
            and response["private_caps"] == ()
            and response["binary_faces"] == (),
            ("base graph-11 cap obstruction changed", response))
    return {
        "representative_edges": BASE_EDGES,
        "directed_incidence": TARGET_INCIDENCE,
        "anchor_chart": tuple(sorted(BASE_STATES.items())),
        "target_support": TARGET_SUPPORT,
        "pure_occurrence_counts": pure,
        "singleton_mixed_words": singletons,
        "response": response,
    }


def audit_one_edge_augmentations(base):
    all_edges = tuple(
        (left, right)
        for left in range(N) for right in range(left + 1, N)
    )
    missing = tuple(edge for edge in all_edges if edge not in set(BASE_EDGES))
    require(missing == (
        (0, 4), (0, 6), (1, 2), (1, 7), (2, 3), (2, 6),
        (3, 5), (3, 6), (4, 5), (4, 7), (5, 7), (6, 7),
    ), ("graph-11 missing-edge ledger changed", missing))
    base_singletons = set(base["singleton_mixed_words"])
    route_counter = Counter()
    repaired_histogram = Counter()
    remaining_base_histogram = Counter()
    total_singleton_histogram = Counter()
    ledgers = []

    for new_edge in missing:
        for colour in COLORS:
            edges = tuple(sorted(BASE_EDGES + (new_edge,)))
            states = dict(BASE_STATES)
            states[new_edge] = colour
            words = BINARY.matching_word_histogram(
                edges, TARGET_EDGE, states, TARGET_SUPPORT
            )
            pure = tuple(words[(index,) * N] for index in COLORS)
            singletons = set(mixed_singletons(words))
            repaired = tuple(sorted(
                word for word in base_singletons if words[word] >= 2
            ))
            remaining_base = tuple(sorted(base_singletons & singletons))
            new_singletons = tuple(sorted(singletons - base_singletons))
            response = response_shapes_and_exits(edges, states)
            cap_landing = bool(
                response["private_caps"]
                or response["landing_binary_faces"]
            )
            if cap_landing:
                route = "active-clean-cap"
            elif singletons:
                route = "mixed-singleton"
            elif 0 in pure:
                route = "missing-pure-row"
            else:
                route = "unresolved-exact-source-necessary-guard"
            route_counter[route] += 1
            repaired_histogram[len(repaired)] += 1
            remaining_base_histogram[len(remaining_base)] += 1
            total_singleton_histogram[len(singletons)] += 1
            ledgers.append({
                "new_edge": new_edge,
                "new_edge_colour": colour,
                "pure_occurrence_counts": pure,
                "repaired_base_singletons": repaired,
                "remaining_base_singletons": remaining_base,
                "new_singletons": new_singletons,
                "all_singleton_mixed_words": tuple(sorted(singletons)),
                "response": response,
                "route": route,
            })

    require(len(ledgers) == 36,
            ("one-edge augmentation count changed", len(ledgers)))
    require(not any(
        item["route"] == "unresolved-exact-source-necessary-guard"
        for item in ledgers
    ), ("a one-edge exact-source guard survived", ledgers))
    require(all(
        item["response"]["private_caps"]
        or item["response"]["landing_binary_faces"]
        or item["all_singleton_mixed_words"]
        or 0 in item["pure_occurrence_counts"]
        for item in ledgers
    ), "one-edge cap/row recurrence failed")
    max_repaired = max(len(item["repaired_base_singletons"])
                       for item in ledgers)
    all_repaired = tuple(
        item for item in ledgers
        if len(item["repaired_base_singletons"]) == len(base_singletons)
    )
    require(not all_repaired,
            ("one added edge mated all base singleton debts", all_repaired))

    return {
        "missing_edges": missing,
        "augmentation_count": len(ledgers),
        "route_histogram": tuple(sorted(route_counter.items())),
        "repaired_base_singleton_histogram": tuple(
            sorted(repaired_histogram.items())
        ),
        "remaining_base_singleton_histogram": tuple(
            sorted(remaining_base_histogram.items())
        ),
        "total_singleton_histogram": tuple(
            sorted(total_singleton_histogram.items())
        ),
        "maximum_repaired_base_singletons": max_repaired,
        "all_base_singletons_repaired_count": len(all_repaired),
        "augmentations": tuple(ledgers),
        "recurrence": (
            "every coordinate one-edge augmentation creates an active clean "
            "private/binary cap, loses a pure row, or retains a singleton "
            "mixed fibre; none mates all twelve base debts"
        ),
    }


def canonical(value):
    if isinstance(value, dict):
        return {
            str(key): canonical(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (list, tuple)):
        return [canonical(item) for item in value]
    return value


def main():
    base = audit_base_guard()
    augmentations = audit_one_edge_augmentations(base)
    ledger = canonical({
        "base_guard": base,
        "one_edge_augmentations": augmentations,
    })
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("support17 one-edge augmentation ledger changed", digest))

    print("N=8 support-17 smallest-guard one-edge augmentation: PASS")
    print("  coordinate augmentations: 36")
    print("  routes:", augmentations["route_histogram"])
    print("  maximum base singleton debts repaired:",
          augmentations["maximum_repaired_base_singletons"], "/ 12")
    print("  exact-source necessary guards:",
          dict(augmentations["route_histogram"]).get(
              "unresolved-exact-source-necessary-guard", 0
          ))


if __name__ == "__main__":
    main()
