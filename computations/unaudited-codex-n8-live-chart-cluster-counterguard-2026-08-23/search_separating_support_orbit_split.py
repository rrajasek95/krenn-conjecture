#!/usr/bin/env python3
"""Exhaustive 28-orbit pure-triple split for the chart-separator support SAT."""

from hashlib import sha256
import json
from pathlib import Path
import sys
import threading
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "computations"))

import search_n8_sparse_triple_completion as sparse
import search_separating_support_symbreak as S

OUT = HERE / "separating_support_cap36_orbit_split.json"
PROGRESS = HERE / "separating_support_cap36_orbit_split_progress.json"
ALLOWED = tuple(chart for chart in range(1, 32) if chart not in S.FORBIDDEN)
DEADLINE_SECONDS = 130
CALL_SECONDS = 2


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def seed_cells(triple):
    return frozenset((u, v, colour, colour)
                     for colour, matching in enumerate(triple)
                     for u, v in matching)


def write_progress(start, calls, active, cases, gadgets, last):
    payload = {
        "format": "n8-live-chart-separator-orbit-split-progress-v1",
        "elapsed_seconds": time.monotonic() - start,
        "solver_calls": calls,
        "active_cases": sorted(active),
        "case_calls": {str(case): cases[case]["calls"] for case in ALLOWED},
        "case_status": {str(case): cases[case]["status"] for case in ALLOWED},
        "case_timeouts": {str(case): cases[case]["timeouts"] for case in ALLOWED},
        "singleton_gadgets": gadgets,
        "last_model": last,
        "forbidden_labelled_triples": 39060,
        "cap": S.CAP,
    }
    PROGRESS.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main():
    start = time.monotonic()
    rows = tuple(sorted(S.ATLAS.CHART.SOURCE.target_orbit_rows()))
    triples = {chart: S.ATLAS.chart_triple(rows[chart - 1])
               for chart in range(1, 32)}
    seeds = {chart: seed_cells(triples[chart]) for chart in ALLOWED}
    require(len(ALLOWED) == 28 and all(len(seed) == 12 for seed in seeds.values()),
            (len(ALLOWED), {key: len(value) for key, value in seeds.items()}))

    forbidden_triples = set()
    sizes = {}
    for chart in S.FORBIDDEN:
        orbit = S.labelled_orbit(triples[chart])
        sizes[chart] = len(orbit)
        forbidden_triples.update(orbit)
    require(sizes == {11: 7560, 24: 1260, 25: 30240}, sizes)
    require(len(forbidden_triples) == 39060, len(forbidden_triples))

    search = sparse.SparseCompletionSearch(S.CAP, "maplesat",
                                           seed_cells=frozenset())
    cases = {chart: {"status": "ACTIVE", "calls": 0, "timeouts": 0}
             for chart in ALLOWED}
    active = set(ALLOWED)
    calls = 0
    last = None
    try:
        for triple in sorted(forbidden_triples):
            cells = [(u, v, colour, colour)
                     for colour, matching in enumerate(triple)
                     for u, v in matching]
            search.solver.add_clause([-search.support[cell] for cell in cells])

        write_progress(start, calls, active, cases, 0, last)
        while active:
            for chart in tuple(sorted(active)):
                if time.monotonic() - start >= DEADLINE_SECONDS:
                    payload = {
                        "format": "n8-live-chart-separator-orbit-split-v1",
                        "status": "TIMEOUT_UNRESOLVED_28_ORBIT_SPLIT",
                        "solver_calls": calls,
                        "elapsed_seconds": time.monotonic() - start,
                        "cap": S.CAP,
                        "active_cases": sorted(active),
                        "case_calls": {str(key): cases[key]["calls"]
                                       for key in ALLOWED},
                        "case_status": {str(key): cases[key]["status"]
                                        for key in ALLOWED},
                        "case_timeouts": {str(key): cases[key]["timeouts"]
                                          for key in ALLOWED},
                        "singleton_gadgets": len(search.singleton_gadgets),
                        "forbidden": list(S.FORBIDDEN),
                        "forbidden_labelled_triples": len(forbidden_triples),
                        "scope": (
                            "No SAT/UNSAT inference for active cases. UNSAT "
                            "labels, if any, are exact under their seeded orbit."
                        ),
                    }
                    OUT.write_text(json.dumps(payload, indent=2,
                                              sort_keys=True) + "\n")
                    print(json.dumps(payload, sort_keys=True), flush=True)
                    return
                assumptions = [search.support[cell] for cell in sorted(seeds[chart])]
                cases[chart]["calls"] += 1
                calls += 1
                timer = threading.Timer(CALL_SECONDS, search.solver.interrupt)
                timer.start()
                try:
                    solved = search.solver.solve_limited(
                        assumptions=assumptions, expect_interrupt=True)
                finally:
                    timer.cancel()
                    search.solver.clear_interrupt()
                if solved is None:
                    cases[chart]["timeouts"] += 1
                    cases[chart]["status"] = "ACTIVE_AFTER_CALL_TIMEOUT"
                    print(f"case={chart} CALL_TIMEOUT calls={cases[chart]['calls']} "
                          f"active={len(active)} gadgets={len(search.singleton_gadgets)}",
                          flush=True)
                    continue
                if not solved:
                    cases[chart]["status"] = "UNSAT"
                    active.remove(chart)
                    print(f"case={chart} UNSAT calls={cases[chart]['calls']} "
                          f"active={len(active)} gadgets={len(search.singleton_gadgets)}",
                          flush=True)
                    continue

                selected = search.decode(search.solver.get_model())
                fibres = sparse.exact_fibres(search, selected)
                singletons = [(word, terms[0][0])
                              for word, terms in sorted(fibres.items())
                              if len(set(word)) > 1 and len(terms) == 1]
                last = {"case": chart, "cells": len(selected),
                        "singletons": len(singletons)}
                if not singletons:
                    require(seeds[chart] <= selected, "seed missing")
                    require(len(selected) <= S.CAP, "cap violation")
                    require(all(fibres[(colour,) * 8] for colour in range(3)),
                            "seeded pure liveness failed")
                    for forbidden in forbidden_triples:
                        cells = {(u, v, colour, colour)
                                 for colour, matching in enumerate(forbidden)
                                 for u, v in matching}
                        require(not cells <= selected,
                                ("forbidden live triple", forbidden))
                    pure = [len(fibres[(colour,) * 8]) for colour in range(3)]
                    histogram = {}
                    for word, terms in fibres.items():
                        if len(set(word)) > 1 and terms:
                            histogram[len(terms)] = histogram.get(len(terms), 0) + 1
                    payload = {
                        "format": "n8-live-chart-separator-orbit-split-v1",
                        "status": "SAT_SEPARATING_SUPPORT",
                        "seed_chart_orbit": chart,
                        "solver_calls": calls,
                        "elapsed_seconds": time.monotonic() - start,
                        "cap": S.CAP,
                        "cells": len(selected),
                        "support": [list(cell) for cell in sorted(selected)],
                        "pure_fibre_sizes": pure,
                        "mixed_histogram": dict(sorted(histogram.items())),
                        "forbidden": list(S.FORBIDDEN),
                        "forbidden_orbit_sizes": sizes,
                        "forbidden_labelled_triples": len(forbidden_triples),
                        "singleton_gadgets": len(search.singleton_gadgets),
                        "case_calls": {str(key): cases[key]["calls"] for key in ALLOWED},
                        "symmetry_justification": (
                            "Choose one live pure matching in each colour. Their "
                            "ordered triple lies in one of 31 S8xS3 atlas orbits. "
                            "The three forbidden types cannot occur, leaving these "
                            "28 seeded representatives exhaustively WLOG."
                        ),
                    }
                    logical = json.dumps(payload, sort_keys=True,
                                         separators=(",", ":"))
                    payload["logical_sha256"] = sha256(logical.encode()).hexdigest()
                    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
                    print(json.dumps({key: value for key, value in payload.items()
                                      if key != "support"}, sort_keys=True), flush=True)
                    print("SUPPORT", sorted(selected), flush=True)
                    return

                added = sum(search.add_singleton_gadget(word, trigger)
                            for word, trigger in singletons)
                require(added, ("no new singleton gadget", chart, last))
                if calls < 50 or calls % 100 == 0:
                    print(f"calls={calls} case={chart} cells={len(selected)} "
                          f"singletons={len(singletons)} add={added} "
                          f"active={len(active)} gadgets={len(search.singleton_gadgets)}",
                          flush=True)
                    write_progress(start, calls, active, cases,
                                   len(search.singleton_gadgets), last)

        payload = {
            "format": "n8-live-chart-separator-orbit-split-v1",
            "status": "UNSAT_CAP36_ALL_28_ORBITS",
            "solver_calls": calls,
            "elapsed_seconds": time.monotonic() - start,
            "cap": S.CAP,
            "forbidden": list(S.FORBIDDEN),
            "forbidden_orbit_sizes": sizes,
            "forbidden_labelled_triples": len(forbidden_triples),
            "singleton_gadgets": len(search.singleton_gadgets),
            "singleton_gadget_keys": [[list(word), trigger]
                                      for word, trigger in sorted(search.singleton_gadgets)],
            "case_calls": {str(key): cases[key]["calls"] for key in ALLOWED},
            "case_status": {str(key): cases[key]["status"] for key in ALLOWED},
            "symmetry_justification": (
                "Choose one live pure matching in each colour. Their ordered "
                "triple lies in one of 31 S8xS3 atlas orbits. The three forbidden "
                "types cannot occur, leaving these 28 seeded representatives "
                "exhaustively WLOG."
            ),
        }
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print(json.dumps({key: value for key, value in payload.items()
                          if key != "singleton_gadget_keys"}, sort_keys=True),
              flush=True)
    finally:
        write_progress(start, calls, active, cases,
                       len(search.singleton_gadgets), last)
        search.delete()


if __name__ == "__main__":
    main()
