#!/usr/bin/env python3
"""One bounded separator SAT with the sound colour-0 matching symmetry break."""

from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import sys
import time

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


ATLAS_PATH = (ROOT / "computations/unaudited-codex-n8-chart-c4-transition-2026-08-23"
              / "audit_chart_c4_transition.py")
ATLAS = load(ATLAS_PATH, "separating_c4_atlas_symbreak")
FORBIDDEN = (11, 24, 25)
CAP = 36
BASE_MATCHING = ((0, 1), (2, 3), (4, 5), (6, 7))
BASE_CELLS = frozenset((u, v, 0, 0) for u, v in BASE_MATCHING)
OUT = HERE / "separating_support_cap36_symbreak.json"
PROGRESS = HERE / "separating_support_cap36_symbreak_progress.json"
SOURCE_PATH = HERE / "search_separating_support.py"


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


def write_progress(start, round_number, selected_cells, singletons, gadgets,
                   forbidden_count, phase):
    payload = {
        "format": "n8-live-chart-separator-symbreak-progress-v1",
        "phase": phase,
        "elapsed_seconds": time.monotonic() - start,
        "round": round_number,
        "selected_cells": selected_cells,
        "singletons_in_last_model": singletons,
        "singleton_gadgets": gadgets,
        "forbidden_labelled_triples": forbidden_count,
        "cap": CAP,
        "fixed_colour0_matching": [list(edge) for edge in BASE_MATCHING],
    }
    PROGRESS.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def validate_support(search, selected, forbidden_triples):
    require(BASE_CELLS <= selected, "base matching missing")
    require(len(selected) <= CAP, "cap violation")
    fibres = sparse.exact_fibres(search, selected)
    require(all(fibres[(colour,) * 8] for colour in range(3)),
            "pure liveness failed")
    singletons = [(word, terms[0][0]) for word, terms in fibres.items()
                  if len(set(word)) > 1 and len(terms) == 1]
    require(not singletons, ("mixed singletons", singletons[:3]))
    for triple in forbidden_triples:
        cells = {(u, v, colour, colour)
                 for colour, matching in enumerate(triple)
                 for u, v in matching}
        require(not cells <= selected, ("forbidden live triple", triple))
    return fibres


def main():
    start = time.monotonic()
    rows = tuple(sorted(ATLAS.CHART.SOURCE.target_orbit_rows()))
    forbidden_triples = set()
    sizes = {}
    for chart in FORBIDDEN:
        orbit = labelled_orbit(ATLAS.chart_triple(rows[chart - 1]))
        sizes[chart] = len(orbit)
        forbidden_triples.update(orbit)
    require(sizes == {11: 7560, 24: 1260, 25: 30240}, sizes)
    require(len(forbidden_triples) == 39060, len(forbidden_triples))

    search = sparse.SparseCompletionSearch(
        CAP, "cadical300", fixed_cells=BASE_CELLS, seed_cells=frozenset()
    )
    try:
        # Colour 0 is already live by the fixed matching.  Colours 1 and 2
        # retain their complete existential matching clauses.
        for colour in (1, 2):
            word = (colour,) * 8
            search.solver.add_clause([
                search.term_indicator(word, number)
                for number in range(len(search.matchings))
            ])

        for triple in sorted(forbidden_triples):
            cells = [(u, v, colour, colour)
                     for colour, matching in enumerate(triple)
                     for u, v in matching]
            search.solver.add_clause([-search.support[cell] for cell in cells])

        write_progress(start, -1, None, None, 0, len(forbidden_triples),
                       "INITIALIZED")
        for round_number in range(10000):
            if not search.solver.solve():
                payload = {
                    "format": "n8-live-chart-separator-symbreak-v1",
                    "status": "UNSAT_CAP36_SYMBREAK",
                    "round": round_number,
                    "elapsed_seconds": time.monotonic() - start,
                    "cap": CAP,
                    "fixed_colour0_matching": [list(edge) for edge in BASE_MATCHING],
                    "forbidden": list(FORBIDDEN),
                    "forbidden_orbit_sizes": sizes,
                    "forbidden_labelled_triples": len(forbidden_triples),
                    "singleton_gadgets": len(search.singleton_gadgets),
                    "singleton_gadget_keys": [
                        [list(word), trigger]
                        for word, trigger in sorted(search.singleton_gadgets)
                    ],
                    "symmetry_justification": (
                        "Every admissible support has a live colour-0 perfect "
                        "matching; an S8 permutation sends it to 01|23|45|67. "
                        "The cap, pure liveness, singleton condition, and the "
                        "S8xS3-invariant forbidden set are preserved."
                    ),
                }
                OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
                print(json.dumps({key: value for key, value in payload.items()
                                  if key != "singleton_gadget_keys"},
                                 sort_keys=True), flush=True)
                return

            selected = search.decode(search.solver.get_model())
            fibres = sparse.exact_fibres(search, selected)
            singletons = [(word, terms[0][0])
                          for word, terms in sorted(fibres.items())
                          if len(set(word)) > 1 and len(terms) == 1]
            if not singletons:
                fibres = validate_support(search, selected, forbidden_triples)
                pure = [len(fibres[(colour,) * 8]) for colour in range(3)]
                histogram = {}
                for word, terms in fibres.items():
                    if len(set(word)) > 1 and terms:
                        histogram[len(terms)] = histogram.get(len(terms), 0) + 1
                payload = {
                    "format": "n8-live-chart-separator-symbreak-v1",
                    "status": "SAT_SEPARATING_SUPPORT",
                    "round": round_number,
                    "elapsed_seconds": time.monotonic() - start,
                    "cap": CAP,
                    "cells": len(selected),
                    "support": [list(cell) for cell in sorted(selected)],
                    "pure_fibre_sizes": pure,
                    "mixed_histogram": dict(sorted(histogram.items())),
                    "fixed_colour0_matching": [list(edge) for edge in BASE_MATCHING],
                    "forbidden": list(FORBIDDEN),
                    "forbidden_orbit_sizes": sizes,
                    "forbidden_labelled_triples": len(forbidden_triples),
                    "singleton_gadgets": len(search.singleton_gadgets),
                    "symmetry_justification": (
                        "Every admissible support has a live colour-0 perfect "
                        "matching; an S8 permutation sends it to 01|23|45|67. "
                        "The cap, pure liveness, singleton condition, and the "
                        "S8xS3-invariant forbidden set are preserved."
                    ),
                    "source_sha256": {
                        str(ATLAS_PATH.relative_to(ROOT)):
                            sha256(ATLAS_PATH.read_bytes()).hexdigest(),
                        str(SOURCE_PATH.relative_to(ROOT)):
                            sha256(SOURCE_PATH.read_bytes()).hexdigest(),
                    },
                }
                logical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
                payload["logical_sha256"] = sha256(logical.encode()).hexdigest()
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
                      f"singletons={len(singletons)} add={added} "
                      f"gadgets={len(search.singleton_gadgets)}", flush=True)
                write_progress(start, round_number, len(selected),
                               len(singletons), len(search.singleton_gadgets),
                               len(forbidden_triples), "SOLVING")
        raise RuntimeError("round cap")
    finally:
        search.delete()


if __name__ == "__main__":
    main()
