#!/usr/bin/env python3
"""Bounded lazy support search avoiding selected live chart orbits."""

from itertools import permutations
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "computations"))

import search_n8_sparse_triple_completion as sparse

import importlib.util


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ATLAS = load(
    ROOT / "computations/unaudited-codex-n8-chart-c4-transition-2026-08-23"
    / "audit_chart_c4_transition.py", "separating_c4_atlas"
)
FORBIDDEN = (11, 24, 25)
CAP = 36
OUT = HERE / "separating_support_cap36.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def site_transform(triple, sigma):
    return tuple(tuple(sorted(tuple(sorted((sigma[u], sigma[v])))
                              for u, v in matching))
                 for matching in triple)


def labelled_orbit(triple):
    answer = set()
    for sigma in permutations(range(8)):
        changed = site_transform(triple, sigma)
        for colour_permutation in permutations(range(3)):
            answer.add(tuple(changed[colour_permutation[c]] for c in range(3)))
    return answer


def main():
    rows = tuple(sorted(ATLAS.CHART.SOURCE.target_orbit_rows()))
    forbidden_triples = set()
    sizes = {}
    for chart in FORBIDDEN:
        orbit = labelled_orbit(ATLAS.chart_triple(rows[chart - 1]))
        sizes[chart] = len(orbit)
        forbidden_triples.update(orbit)
    require(sizes == {11: 7560, 24: 1260, 25: 30240}, sizes)
    require(len(forbidden_triples) == sum(sizes.values()), "chart orbits overlap")

    search = sparse.SparseCompletionSearch(
        CAP, "cadical300", seed_cells=frozenset()
    )
    try:
        # At least one literal pure perfect matching in each colour.
        for colour in range(3):
            word = (colour,) * 8
            search.solver.add_clause([
                search.term_indicator(word, number)
                for number in range(len(search.matchings))
            ])

        # No live pure triple in any of the three forbidden chart orbits.
        for triple in sorted(forbidden_triples):
            cells = [(u, v, colour, colour)
                     for colour, matching in enumerate(triple)
                     for u, v in matching]
            search.solver.add_clause([-search.support[cell] for cell in cells])

        for round_number in range(5000):
            if not search.solver.solve():
                payload = {
                    "status": "UNSAT_CAP36",
                    "round": round_number,
                    "cap": CAP,
                    "forbidden": list(FORBIDDEN),
                    "forbidden_labelled_triples": len(forbidden_triples),
                    "singleton_gadgets": len(search.singleton_gadgets),
                }
                OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
                print(json.dumps(payload, sort_keys=True), flush=True)
                return
            selected = search.decode(search.solver.get_model())
            fibres = sparse.exact_fibres(search, selected)
            singletons = [
                (word, terms[0][0])
                for word, terms in sorted(fibres.items())
                if len(set(word)) > 1 and len(terms) == 1
            ]
            if not singletons:
                pure = [len(fibres[(colour,) * 8]) for colour in range(3)]
                histogram = {}
                for word, terms in fibres.items():
                    if len(set(word)) > 1 and terms:
                        histogram[len(terms)] = histogram.get(len(terms), 0) + 1
                payload = {
                    "status": "SAT_SEPARATING_SUPPORT",
                    "round": round_number,
                    "cap": CAP,
                    "cells": len(selected),
                    "support": [list(cell) for cell in sorted(selected)],
                    "pure_fibre_sizes": pure,
                    "mixed_histogram": dict(sorted(histogram.items())),
                    "forbidden": list(FORBIDDEN),
                    "forbidden_orbit_sizes": sizes,
                    "forbidden_labelled_triples": len(forbidden_triples),
                    "singleton_gadgets": len(search.singleton_gadgets),
                }
                OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
                print(json.dumps({key: value for key, value in payload.items()
                                  if key != "support"}, sort_keys=True), flush=True)
                print("SUPPORT", sorted(selected), flush=True)
                return
            added = sum(search.add_singleton_gadget(word, trigger)
                        for word, trigger in singletons)
            require(added, "no new singleton gadget")
            if round_number < 20 or round_number % 20 == 0:
                print(f"round={round_number} cells={len(selected)} "
                      f"singletons={len(singletons)} add={added}", flush=True)
        raise RuntimeError("round cap")
    finally:
        search.delete()


if __name__ == "__main__":
    main()
