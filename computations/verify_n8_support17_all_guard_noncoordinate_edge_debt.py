#!/usr/bin/env python3
"""Test noncoordinate one-edge insertions by inherited singleton debt.

For every pure-supported cap-dark completion in the 148 support-16 frontier,
insert each missing edge with each of the four noncoordinate ternary supports
01, 02, 12, and 012.  No cap formula is assumed for the inserted block.  The
checker adds its literal decorated matching occurrences and asks whether a
mixed singleton necessarily survives.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "853f09b21d73e1af50ee63aaf567e9525ff6b87d7e156744a92b1bb54013f27b"
COLORS = (0, 1, 2)
NONCOORDINATE_SUPPORTS = ((0, 1), (0, 2), (1, 2), (0, 1, 2))
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


RECURRENCE = load_local(
    "n8_support17_coordinate_recurrence_for_noncoordinate_debt",
    "verify_n8_support17_all_guard_one_edge_recurrence.py",
)
BINARY = RECURRENCE.BINARY
ORBIT = BINARY.ORBIT
PROTOTYPE = BINARY.PROTOTYPE


def matching_words(matchings, states, target_edge, target_support,
                   new_edge, new_support):
    words = Counter()
    for matching in matchings:
        choices = []
        for edge in matching:
            if edge == target_edge:
                choices.append(target_support)
            elif edge == new_edge:
                choices.append(new_support)
            else:
                choices.append((states[edge],))
        for colours in product(*choices):
            word = [None] * N
            for edge, colour in zip(matching, colours):
                word[edge[0]] = colour
                word[edge[1]] = colour
            require(None not in word,
                    ("noncoordinate insertion left blank site", matching,
                     colours, word))
            words[tuple(word)] += 1
    return words


def audit_noncoordinate_debt():
    terminal_records = ORBIT.terminal_two_rrx_records()
    candidates = RECURRENCE.support16_candidates(terminal_records)
    require(len(candidates) == 148,
            ("noncoordinate base-orbit count changed", len(candidates)))
    routes = Counter()
    completion_charts = Counter()
    base_singleton_histogram = Counter()
    unresolved = []

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
        all_edges = tuple(
            (left, right)
            for left in range(N) for right in range(left + 1, N)
        )
        missing = tuple(edge for edge in all_edges if edge not in set(edges))
        increments = tuple(
            (
                new_edge,
                RECURRENCE.new_matchings(
                    tuple(sorted(edges + (new_edge,))), new_edge
                ),
            )
            for new_edge in missing
        )

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
                        ("noncoordinate visitor lost base debt", candidate,
                         chart_name, completion))
                completion_charts[chart_name] += 1
                base_singleton_histogram[len(base_singletons)] += 1

                for new_edge, added_matchings in increments:
                    for new_support in NONCOORDINATE_SUPPORTS:
                        maximum_added = sum(
                            len(target_support) * len(new_support)
                            if candidate["incidence"][1] in matching
                            else len(new_support)
                            for matching in added_matchings
                        )
                        if len(base_singletons) > maximum_added:
                            routes["inherited-singleton-cardinality"] += 1
                            continue
                        added_words = matching_words(
                            added_matchings, states,
                            candidate["incidence"][1], target_support,
                            new_edge, new_support,
                        )
                        repaired = {
                            word for word in base_singletons
                            if added_words[word]
                        }
                        if repaired != base_singletons:
                            routes["inherited-singleton-literal"] += 1
                            continue
                        combined = Counter(base_words)
                        combined.update(added_words)
                        new_singletons = tuple(
                            word for word, multiplicity in combined.items()
                            if len(set(word)) > 1 and multiplicity == 1
                        )
                        if new_singletons:
                            routes["new-mixed-singleton"] += 1
                            continue
                        routes["unresolved-noncoordinate-counterguard"] += 1
                        if len(unresolved) < 16:
                            unresolved.append({
                                "graph_index": candidate["graph_index"],
                                "orbit_size": candidate["orbit_size"],
                                "incidence": candidate["incidence"],
                                "chart": chart_name,
                                "completion": completion,
                                "new_edge": new_edge,
                                "new_edge_support": new_support,
                                "base_singletons": tuple(
                                    sorted(base_singletons)
                                ),
                                "added_words": tuple(
                                    sorted(added_words.items())
                                ),
                            })

            witness, counts = BINARY.exact_source_guard_completion(
                edges, candidate["incidence"][1], faces,
                zero_coordinate, completion_visitor=visit,
            )
            require(witness is None,
                    ("support-16 exact guard survived in noncoordinate audit",
                     candidate, chart_name, witness))
            require(dict(counts).get("singleton_free_completions", 0) == 0,
                    ("support-16 base lost singleton theorem", candidate,
                     chart_name, counts))

    require(completion_charts == Counter({
        "support-two": 54891, "support-three": 26794,
    }), ("noncoordinate completion count changed", completion_charts))
    require(sum(routes.values()) == 81685 * 12 * 4,
            ("noncoordinate augmentation total changed", routes))
    require(routes == Counter({
        "inherited-singleton-cardinality": 3408610,
        "inherited-singleton-literal": 512270,
    }), ("noncoordinate debt route split changed", routes))
    require(not unresolved,
            ("noncoordinate exact-source counterguard survived", unresolved))
    return {
        "base_orbit_count": len(candidates),
        "completion_charts": tuple(sorted(completion_charts.items())),
        "base_singleton_histogram": tuple(
            sorted(base_singleton_histogram.items())
        ),
        "new_edge_supports": NONCOORDINATE_SUPPORTS,
        "augmentation_routes": tuple(sorted(routes.items())),
        "unresolved_counterguards": tuple(unresolved),
        "scope": (
            "matching-debt test only; unresolved cases require cap/root "
            "analysis for a genuinely noncoordinate inserted block"
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
    ledger = canonical(audit_noncoordinate_debt())
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("noncoordinate edge debt ledger changed", digest))
    print("N=8 support-17 all-guard noncoordinate-edge debt: PASS")
    print("  visited completion charts:", ledger["completion_charts"])
    print("  augmentation routes:", ledger["augmentation_routes"])
    print("  unresolved counterguards:",
          len(ledger["unresolved_counterguards"]))


if __name__ == "__main__":
    main()
