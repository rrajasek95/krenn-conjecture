#!/usr/bin/env python3
"""Lift the support-17 one-edge debt recurrence across all 148 guards.

This is an augmentation audit, not a fresh support-17 graph census.  It
reuses every pure-supported mutual-coordinate completion from the exact
support-16 binary-cap search.  For each missing edge and each coordinate
colour it adds only the new perfect matchings containing that edge, then
tests whether inherited singleton mixed fibres are mated.  It also recomputes
all complete-private and complementary binary cap faces through the fixed
directed nonanchor.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "f1f20cb858ecc53e8e2b71fc1e9a78355ade4367d720af6d3231dd0c13054dc3"
COLORS = (0, 1, 2)
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
    "n8_support16_binary_cover_for_all_support17_augmentations",
    "verify_n8_support16_all_binary_residue_two_cap_cover.py",
)
ORBIT = BINARY.ORBIT
PROTOTYPE = BINARY.PROTOTYPE


def response_augmentation_data(edges, incidence):
    adjacency = ORBIT.adjacency_from_edges(edges)
    shapes = []
    private_caps = []
    for cap_edge in edges:
        if incidence[0] not in cap_edge:
            continue
        through, residue = PROTOTYPE.cap_shape(
            adjacency, edges, incidence, cap_edge
        )
        if not through:
            continue
        shapes.append((cap_edge, len(through), len(residue)))
        if not residue:
            private_caps.append(cap_edge)
    binary_faces = BINARY.binary_faces(
        adjacency, edges, incidence, tuple(shapes)
    )
    return tuple(shapes), tuple(private_caps), binary_faces


def new_matchings(edges, new_edge):
    edge_set = set(edges)
    return tuple(
        matching
        for raw_matching in ORBIT.BASE.perfect_matchings(tuple(range(N)))
        for matching in (
            tuple(tuple(sorted(edge)) for edge in raw_matching),
        )
        if new_edge in matching and all(edge in edge_set for edge in matching)
    )


def matching_words(matchings, states, target_edge, target_support):
    words = Counter()
    for matching in matchings:
        choices = tuple(
            target_support if edge == target_edge else (states[edge],)
            for edge in matching
        )
        for colours in product(*choices):
            word = [None] * N
            for edge, colour in zip(matching, colours):
                word[edge[0]] = colour
                word[edge[1]] = colour
            require(None not in word,
                    ("augmentation matching left blank site", matching,
                     colours, word))
            words[tuple(word)] += 1
    return words


def precompute_augmentations(edges, incidence):
    all_edges = tuple(
        (left, right)
        for left in range(N) for right in range(left + 1, N)
    )
    missing = tuple(edge for edge in all_edges if edge not in set(edges))
    answer = []
    for new_edge in missing:
        augmented_edges = tuple(sorted(edges + (new_edge,)))
        shapes, private_caps, binary_faces = response_augmentation_data(
            augmented_edges, incidence
        )
        added_matchings = new_matchings(augmented_edges, new_edge)
        require(added_matchings,
                ("new support edge belongs to no perfect matching", edges,
                 incidence, new_edge))
        answer.append({
            "new_edge": new_edge,
            "augmented_edges": augmented_edges,
            "response_shapes": shapes,
            "private_caps": private_caps,
            "binary_faces": binary_faces,
            "new_matchings": added_matchings,
        })
    return tuple(answer)


def support16_candidates(terminal_records):
    ORBIT.terminal_two_rrx_records = lambda: terminal_records
    audit = PROTOTYPE.audit_all_orbits()
    return tuple(
        item for item in audit["graph_ledgers"]
        if item["route"] != "forced-distinct-two-cap"
        and not item["private_face_count"]
        and len(item["prototype_faces"]) < 2
    )


def audit_all_augmentations():
    terminal_records = ORBIT.terminal_two_rrx_records()
    candidates = support16_candidates(terminal_records)
    require(len(candidates) == 148,
            ("support-16 augmentation base count changed", len(candidates)))
    global_routes = Counter()
    global_completions = Counter()
    global_base_singletons = Counter()
    global_repaired = Counter()
    unresolved = []
    orbit_ledgers = []

    for candidate in candidates:
        edges = tuple(
            terminal_records[candidate["graph_index"]][
                "representative_edges"
            ]
        )
        adjacency = ORBIT.adjacency_from_edges(edges)
        faces = BINARY.binary_faces(
            adjacency, edges, candidate["incidence"],
            candidate["all_source_response_shapes"]
        )
        augmentations = precompute_augmentations(
            edges, candidate["incidence"]
        )
        local_routes = Counter()
        local_completions = Counter()
        local_base_singletons = Counter()
        local_repaired = Counter()

        for chart_name, zero_coordinate, target_support in (
                ("support-two", 0, (1, 2)),
                ("support-three", None, COLORS)):

            def visit(completion, _pure, word_items, singleton_words,
                      *, chart_name=chart_name,
                      target_support=target_support):
                states = dict(completion)
                base_words = dict(word_items)
                base_singletons = set(singleton_words)
                require(base_singletons,
                        ("support-16 visitor lost singleton exit",
                         candidate, chart_name, completion))
                local_completions[chart_name] += 1
                global_completions[chart_name] += 1
                local_base_singletons[len(base_singletons)] += 1
                global_base_singletons[len(base_singletons)] += 1

                for augmentation in augmentations:
                    for colour in COLORS:
                        states[augmentation["new_edge"]] = colour
                        if augmentation["private_caps"] or any(
                                BINARY.face_lands(
                                    face, states, zero_coordinate
                                )
                                for face in augmentation["binary_faces"]):
                            route = "active-clean-cap"
                            repaired_count = 0
                        else:
                            maximum_added = sum(
                                len(target_support)
                                if candidate["incidence"][1] in matching
                                else 1
                                for matching in augmentation["new_matchings"]
                            )
                            if len(base_singletons) > maximum_added:
                                route = "inherited-singleton-cardinality"
                                repaired_count = 0
                            else:
                                added_words = matching_words(
                                    augmentation["new_matchings"], states,
                                    candidate["incidence"][1],
                                    target_support,
                                )
                                repaired = {
                                    word for word in base_singletons
                                    if added_words[word]
                                }
                                repaired_count = len(repaired)
                                if repaired != base_singletons:
                                    route = "inherited-singleton-literal"
                                else:
                                    combined = Counter(base_words)
                                    combined.update(added_words)
                                    new_singletons = tuple(
                                        word for word, multiplicity
                                        in combined.items()
                                        if len(set(word)) > 1
                                        and multiplicity == 1
                                    )
                                    if new_singletons:
                                        route = "new-mixed-singleton"
                                    else:
                                        route = (
                                            "unresolved-exact-source-"
                                            "necessary-guard"
                                        )
                                        if len(unresolved) < 8:
                                            unresolved.append({
                                                "graph_index": candidate[
                                                    "graph_index"
                                                ],
                                                "incidence": candidate[
                                                    "incidence"
                                                ],
                                                "chart": chart_name,
                                                "completion": completion,
                                                "new_edge": augmentation[
                                                    "new_edge"
                                                ],
                                                "new_edge_colour": colour,
                                                "base_singletons": tuple(
                                                    sorted(base_singletons)
                                                ),
                                                "added_words": tuple(
                                                    sorted(added_words.items())
                                                ),
                                                "response_shapes": (
                                                    augmentation[
                                                        "response_shapes"
                                                    ]
                                                ),
                                            })
                        del states[augmentation["new_edge"]]
                        local_routes[route] += 1
                        global_routes[route] += 1
                        local_repaired[repaired_count] += 1
                        global_repaired[repaired_count] += 1

            witness, counts = BINARY.exact_source_guard_completion(
                edges, candidate["incidence"][1], faces,
                zero_coordinate, completion_visitor=visit,
            )
            require(witness is None,
                    ("support-16 exact guard unexpectedly survived",
                     candidate, chart_name, witness))
            require(dict(counts).get("singleton_free_completions", 0) == 0,
                    ("support-16 singleton-free count changed", candidate,
                     chart_name, counts))

        orbit_ledgers.append({
            "graph_index": candidate["graph_index"],
            "orbit_size": candidate["orbit_size"],
            "incidence": candidate["incidence"],
            "role": candidate["role"],
            "base_binary_face_count": len(faces),
            "missing_edge_count": len(augmentations),
            "completion_charts": tuple(sorted(local_completions.items())),
            "base_singleton_histogram": tuple(
                sorted(local_base_singletons.items())
            ),
            "augmentation_routes": tuple(sorted(local_routes.items())),
            "repaired_debt_histogram": tuple(sorted(local_repaired.items())),
        })

    require(global_completions == Counter({
        "support-two": 54891, "support-three": 26794,
    }), ("support-16 completion visitor count changed", global_completions))
    require(global_routes == Counter({
        "active-clean-cap": 71751,
        "inherited-singleton-cardinality": 2868903,
        "inherited-singleton-literal": 6,
    }), ("support-17 augmentation route count changed", global_routes))
    require(sum(global_routes.values()) == 81685 * 36,
            ("augmentation total is not completions times 36",
             global_routes, global_completions))
    require(not unresolved,
            ("support-17 exact-source counterguard survived", unresolved))

    return {
        "base_orbit_count": len(candidates),
        "completion_charts": tuple(sorted(global_completions.items())),
        "base_singleton_histogram": tuple(
            sorted(global_base_singletons.items())
        ),
        "augmentation_routes": tuple(sorted(global_routes.items())),
        "repaired_debt_histogram": tuple(sorted(global_repaired.items())),
        "unresolved_counterguards": tuple(unresolved),
        "orbit_ledgers": tuple(orbit_ledgers),
        "recurrence": (
            "for every pure-supported cap-dark support-16 completion, each "
            "coordinate one-edge augmentation either creates an active clean "
            "cap or retains/creates a singleton mixed fibre"
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
    ledger = canonical(audit_all_augmentations())
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("all-guard support17 recurrence ledger changed", digest))
    routes = dict(ledger["augmentation_routes"])
    print("N=8 support-17 all-guard one-edge recurrence: PASS")
    print("  support-16 base orbits:", ledger["base_orbit_count"])
    print("  visited completion charts:", ledger["completion_charts"])
    print("  augmentation routes:", ledger["augmentation_routes"])
    print("  inherited base-singleton histogram:",
          ledger["base_singleton_histogram"])
    print("  exact-source necessary counterguards:",
          len(ledger["unresolved_counterguards"]))


if __name__ == "__main__":
    main()
