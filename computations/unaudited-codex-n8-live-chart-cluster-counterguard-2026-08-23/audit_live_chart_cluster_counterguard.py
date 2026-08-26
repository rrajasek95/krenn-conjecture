#!/usr/bin/env python3
"""Exact support audit for live pure-matching C4 components."""

from collections import Counter, deque
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ATLAS_PATH = (ROOT / "computations/unaudited-codex-n8-chart-c4-transition-2026-08-23"
              / "audit_chart_c4_transition.py")
ORBIT8_PATH = ROOT / "computations/verify_n8_orbit8_factorized_chart.py"
SPARSE_PATH = ROOT / "computations/search_n8_sparse_triple_completion.py"
CUBE_PATH = (ROOT / "computations"
             / "audit_n8_support28_cube_cut_permanent_triangle_unit_independent.py")
EXPECTED = {
    ATLAS_PATH: "9fed1ac370435a1cb1b0ca60fd5bf4591f1d659fd4c191ab929d8231b2697722",
    ORBIT8_PATH: "b904ce0cad8fd68bf3ad9466558b17659985430906f001bdf8d8a2ff3432f418",
    SPARSE_PATH: "906b778b61ae7beeaa3efb3a62e52defb9b4e8a5f2e4483236a662f1d44d6d56",
    CUBE_PATH: "cdad1bb93dba4f56cc441adab049d5eb35c16c55f5622badc6272b1e6f878489",
}
RESULT = HERE / "results_live_chart_cluster_counterguard.json"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ATLAS = load(ATLAS_PATH, "live_chart_c4_atlas")


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


MATCHINGS = tuple(tuple(sorted(matching))
                  for matching in perfect_matchings(range(8)))
ROWS = tuple(sorted(ATLAS.CHART.SOURCE.target_orbit_rows()))
ROW_INDEX = {row: index for index, row in enumerate(ROWS, 1)}

SEEDS = {
    "new24": (
        (((0, 1), (2, 3), (4, 5), (6, 7)),
         ((0, 2), (1, 3), (4, 6), (5, 7)),
         ((0, 3), (1, 4), (2, 7), (5, 6))),
        {(0, 1, 0, 1), (0, 1, 1, 0), (0, 1, 1, 1),
         (0, 2, 0, 0), (0, 2, 0, 1), (0, 2, 1, 0),
         (1, 3, 0, 0), (1, 3, 0, 1), (1, 3, 1, 0),
         (2, 3, 0, 1), (2, 3, 1, 0), (2, 3, 1, 1)},
    ),
    "new30": (
        (((0, 1), (2, 3), (4, 5), (6, 7)),
         ((0, 2), (1, 3), (4, 6), (5, 7)),
         ((0, 3), (1, 2), (4, 7), (5, 6))),
        {(0, 2, 2, 1), (0, 3, 1, 2), (0, 6, 1, 0),
         (0, 6, 2, 0), (2, 7, 1, 0), (3, 7, 2, 0),
         (4, 6, 1, 2), (4, 6, 2, 1), (4, 6, 2, 2),
         (4, 7, 1, 1), (4, 7, 1, 2), (4, 7, 2, 1),
         (5, 6, 1, 1), (5, 6, 1, 2), (5, 6, 2, 1),
         (5, 7, 1, 2), (5, 7, 2, 1), (5, 7, 2, 2)},
    ),
    "archived36": (
        (((0, 1), (2, 3), (4, 5), (6, 7)),
         ((0, 2), (1, 4), (3, 6), (5, 7)),
         ((0, 3), (1, 5), (2, 7), (4, 6))),
        {(2, 6, 2, 1), (2, 6, 2, 2), (2, 7, 2, 1),
         (3, 6, 1, 2), (3, 7, 1, 1), (3, 7, 1, 2),
         (4, 6, 2, 1), (4, 7, 2, 1), (4, 7, 2, 2),
         (5, 6, 1, 1), (5, 6, 1, 2), (5, 7, 1, 2),
         (0, 4, 1, 1), (0, 5, 2, 2), (1, 2, 1, 1),
         (1, 3, 2, 2),
         (0, 2, 2, 1), (0, 3, 1, 2), (0, 4, 2, 1),
         (0, 5, 1, 2), (1, 2, 2, 1), (1, 3, 1, 2),
         (1, 4, 2, 1), (1, 5, 1, 2)},
    ),
}


def support(seed, extras):
    answer = {(u, v, colour, colour)
              for colour, matching in enumerate(seed) for u, v in matching}
    answer.update(extras)
    return frozenset(answer)


def fibres(selected):
    pure = [0, 0, 0]
    mixed = Counter()
    for word in product(range(3), repeat=8):
        count = sum(all((u, v, word[u], word[v]) in selected
                        for u, v in matching)
                    for matching in MATCHINGS)
        if len(set(word)) == 1:
            pure[word[0]] = count
        elif count:
            mixed[count] += 1
    return pure, mixed


def live_matchings(selected):
    return tuple(tuple(matching for matching in MATCHINGS
                       if all((u, v, colour, colour) in selected
                              for u, v in matching))
                 for colour in range(3))


def components(selected):
    layers = live_matchings(selected)
    triples = tuple(product(*layers))
    triple_index = {triple: index for index, triple in enumerate(triples)}
    adjacency = [set() for _ in triples]
    for index, triple in enumerate(triples):
        for neighbor in ATLAS.flip_neighbors(triple):
            if neighbor in triple_index:
                adjacency[index].add(triple_index[neighbor])
    unseen = set(range(len(triples)))
    records = []
    while unseen:
        root = min(unseen)
        component = {root}
        queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for other in adjacency[vertex]:
                if other not in component:
                    component.add(other)
                    queue.append(other)
        unseen -= component
        orbit_counter = Counter(
            ROW_INDEX[ATLAS.chart_key(triples[index])] for index in component
        )
        records.append({
            "vertices": len(component),
            "chart_orbits": sorted(orbit_counter),
            "chart_orbit_multiplicity": {
                str(key): value for key, value in sorted(orbit_counter.items())
            },
        })
    return [len(layer) for layer in layers], records, triples


def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return sum((1 if permutation in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1)
               * matrix[0][permutation[0]]
               * matrix[1][permutation[1]]
               * matrix[2][permutation[2]]
               for permutation in ((0, 1, 2), (0, 2, 1), (1, 0, 2),
                                   (1, 2, 0), (2, 0, 1), (2, 1, 0)))


def rank_witness(selected, triples):
    checked = 0
    for triple in triples:
        for edge in combinations(range(8), 2):
            colours = [colour for colour, matching in enumerate(triple)
                       if edge in matching]
            if not colours:
                continue
            matrix = [[Fraction(1 if a == b else 1, 1 if a == b else 1000)
                       if edge + (a, b) in selected else Fraction(0)
                       for b in colours] for a in colours]
            require(determinant(matrix) != 0, (edge, colours, matrix))
            checked += 1
    return checked


def cube_control():
    coordinates = ((0, 0, 0), (0, 1, 1), (0, 1, 0), (0, 0, 1),
                   (1, 1, 0), (1, 1, 1), (1, 0, 0), (1, 0, 1))
    selected = frozenset((u, v, colour, colour)
                         for u, v in combinations(range(8), 2)
                         for colour in range(3)
                         if coordinates[u][colour] != coordinates[v][colour])
    pure, mixed = fibres(selected)
    layers = live_matchings(selected)
    require([len(layer) for layer in layers] == [24, 24, 24], "cube layers")
    orbit_counter = Counter(ROW_INDEX[ATLAS.chart_key(triple)]
                            for triple in product(*layers))
    require(set(orbit_counter) == set(range(1, 32)), "cube missed a chart")
    require(1 not in mixed and pure == [24, 24, 24], (pure, mixed))
    return {
        "cells": len(selected),
        "pure_fibre_sizes": pure,
        "mixed_histogram": {str(key): value for key, value in sorted(mixed.items())},
        "live_triples": 24 ** 3,
        "component_count": 1,
        "chart_orbits": list(range(1, 32)),
        "connectedness_reason": (
            "each colour is K4,4; its perfect-matching C4 flip graph is the "
            "connected transposition graph on S4, and the triple graph is "
            "their Cartesian product"
        ),
    }


def hitting_sets(edges):
    universe = range(1, 32)
    for size in range(1, 32):
        hits = [choice for choice in combinations(universe, size)
                if all(set(choice) & edge for edge in edges)]
        if hits:
            return size, hits
    raise RuntimeError("no hitting set")


def audit(mutate=False):
    for path, digest in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == digest,
                f"source drift {path}")
    expected = {
        "new24": (24, [2, 2, 1], {2: 30}, [2, 2, 1], [[17, 25]]),
        "new30": (30, [1, 2, 2], {2: 82}, [1, 2, 2], [[11, 24]]),
        "archived36": (36, [1, 4, 4], {2: 16, 4: 94}, [1, 4, 4],
                       [[25, 26, 30]]),
    }
    records = {}
    component_edges = []
    for name, (seed, extras) in SEEDS.items():
        selected = support(seed, extras)
        if mutate and name == "new24":
            selected = frozenset(set(selected) - {min(extras)})
        pure, mixed = fibres(selected)
        layer_sizes, component_records, triples = components(selected)
        observed = (len(selected), pure, dict(mixed), layer_sizes,
                    [item["chart_orbits"] for item in component_records])
        require(observed == expected[name], (name, observed))
        minor_checks = rank_witness(selected, triples)
        records[name] = {
            "cells": len(selected),
            "support": [list(cell) for cell in sorted(selected)],
            "pure_fibre_sizes": pure,
            "mixed_histogram": {
                str(key): value for key, value in sorted(mixed.items())
            },
            "no_mixed_singleton": 1 not in mixed,
            "live_matchings_per_colour": layer_sizes,
            "live_triples": len(triples),
            "components": component_records,
            "rank_respecting_minor_checks": minor_checks,
            "rank_witness": (
                "put 1 on live diagonal cells and 1/1000 on live off-diagonal "
                "cells; every selected repeated-edge principal minor is nonzero"
            ),
        }
        component_edges.extend(set(item["chart_orbits"])
                               for item in component_records)
    minimum, transversals = hitting_sets(component_edges)
    require((minimum, transversals) ==
            (2, [(11, 25), (24, 25)]), (minimum, transversals))

    result = {
        "format": "n8-live-chart-c4-cluster-counterguard-v1",
        "status": "EXACT_FIXED_BASE_FALSE_HITTING_NUMBER_AT_LEAST_TWO",
        "supports": records,
        "archived_cube_control": cube_control(),
        "component_hypergraph": {
            "edges": [sorted(edge) for edge in component_edges],
            "minimum_hitting_number_for_frozen_family": minimum,
            "minimum_hitting_sets": [list(item) for item in transversals],
            "consequence": (
                "No one chart orbit meets every certified live component. "
                "In particular chart1 and chart26 both fail."
            ),
        },
        "bounded_separating_search": {
            "cap": 36,
            "forbidden_chart_orbits": [11, 24, 25],
            "forbidden_labelled_triples": 39060,
            "terminal": "TIME_CAP_UNRESOLVED",
            "elapsed_seconds": 300,
            "last_round": 1340,
            "claim": (
                "No SAT/UNSAT conclusion. Therefore hitting number >=3 is "
                "not proved, and {11,25}/{24,25} remain candidate two-chart "
                "hitting sets for the audited family only."
            ),
        },
        "smallest_scope": (
            "24 cells is the smallest landed rank-respecting singleton-free "
            "counterguard in this bounded audit. The cap23 run was stopped "
            "unresolved, so 24 is not a certified global or seeded minimum."
        ),
        "scope": (
            "Exact finite support/fibre/rank-minor/C4-component theorem. None "
            "of the supports is asserted to solve the mixed coefficient "
            "equations; support feasibility is not an X5 source."
        ),
        "source_sha256": {str(path.relative_to(ROOT)): digest
                          for path, digest in EXPECTED.items()},
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate)
    if args.write_results:
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if args.check_results:
        require(RESULT.exists() and json.loads(RESULT.read_text()) == result,
                "stored result drift")
    print(result["status"])
    print(result["component_hypergraph"])
    print(result["logical_sha256"])


if __name__ == "__main__":
    main()
