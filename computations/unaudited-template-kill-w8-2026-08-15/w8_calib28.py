#!/usr/bin/env python3
"""UNAUDITED PROBE (W8) -- calibration: reproduce W2's m = 28 R_cell census.

Pinned HEAD: a1196b4dca9f83452483734a3273c0c43d5cf3b5

W2 (computations/unaudited-witness-splitting-w2-2026-08-15/REPORT.md item 1):
"Exactly 28 no-singleton templates exist over all 13 colour-triple orbits
(22 diagonal, 6 off-diagonal; all share fibre census {1:1,2:38,4:1,24:1});
every one carries an O1 circuit."

This script re-derives that census with the COMMITTED encoding
(computations/search_monomial_no_singleton_sat.py, untouched: imported, not
modified) and decides every model with the INDEPENDENT W8 engine
(w8_core.analyse, cell coordinates), then cross-checks against W2's engine.

R_cell at full support = every edge carries exactly one cell.  All 28 edges
are forced present.  Models are enumerated exhaustively per colour-triple
orbit with blocking clauses, so the census is an exhaustion given the
committed encoding (which itself fixes the three constant matchings, i.e.
quotients by the choice of colour triple).

Run: python3 w8_calib28.py
"""

from __future__ import annotations

import json
import sys
import time
from collections import Counter

sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations")
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-witness-splitting-w2-2026-08-15")

import w8_core as C
from w8_symmetry import canonical_fast

from search_monomial_no_singleton_sat import (ABSENT, build_formula,
                                              colored_triple_orbits)
from pysat.solvers import Solver
import w2_monomial as W2


def decode(model, state):
    positive = {lit for lit in model if lit > 0}
    return [next(value for value, variable in enumerate(row)
                 if variable in positive) for row in state]


def to_template(states):
    template = [0] * 28
    for e, value in enumerate(states):
        if value != ABSENT:
            a, b = divmod(value - 1, 3)
            template[e] = 1 << (3 * a + b)
    return tuple(template)


def to_labels(states):
    return [None if value == ABSENT else divmod(value - 1, 3)
            for value in states]


def main():
    geo = C.geometry(8)
    orbits = colored_triple_orbits(8)
    print(f"colour-triple orbits at N=8: {len(orbits)}")
    found = []
    start = time.time()
    for number, targets in enumerate(orbits):
        top, clauses, state, edges, edge_index, matchings = \
            build_formula(8, targets)
        with Solver(name="cadical153", bootstrap_with=clauses) as solver:
            for row in state:                      # force full support m = 28
                solver.add_clause([-row[ABSENT]])
            count = 0
            while solver.solve():
                model = solver.get_model()
                states = decode(model, state)
                template = to_template(states)
                found.append({"orbit": number, "template": list(template),
                              "states": states})
                count += 1
                solver.add_clause([-state[e][states[e]] for e in range(28)])
        print(f"  orbit {number:2d}: {count} no-singleton full-support models"
              f"   [{time.time() - start:.1f}s]", flush=True)

    print(f"\ntotal models: {len(found)}")
    verdicts = Counter()
    census = Counter()
    diagonal = 0
    for record in found:
        template = tuple(record["template"])
        compat = C.compat_matrix(geo, template)
        out = C.analyse(geo, template, compat=compat)
        record["w8_verdict"] = out["verdict"]
        record["w2_verdict"] = W2.analyse(W2.geometry(8),
                                          to_labels(record["states"]))["verdict"]
        table = C.fibre_table(geo, template, compat)
        full = Counter(len(v) for v in table.values())
        record["fibre_census"] = dict(sorted(full.items()))
        record["mixed_singletons"] = len(C.mixed_singletons(geo, template,
                                                            compat))
        record["diagonal"] = all(mask == 0 or (mask & 0b100010001) == mask
                                 for mask in template)
        record["audit"] = C.audit(geo, template, compat)
        diagonal += record["diagonal"]
        verdicts[out["verdict"]] += 1
        census[json.dumps(record["fibre_census"])] += 1

    print("W8 verdicts:", dict(verdicts))
    print("fibre censuses:", dict(census))
    print(f"diagonal: {diagonal}   off-diagonal: {len(found) - diagonal}")
    agree = sum(1 for r in found
                if r["w8_verdict"].split("-", 1)[-1] == r["w2_verdict"]
                or r["w8_verdict"].endswith(r["w2_verdict"]))
    print(f"W8 vs W2 engine agreement: {agree}/{len(found)}")

    # distinct up to the full S_8 x S_3 action
    canon = {}
    for record in found:
        key = canonical_fast(geo, tuple(record["template"]))
        canon.setdefault(key, []).append(record["orbit"])
    print(f"distinct up to S_8 x S_3: {len(canon)}")

    fie = sum(1 for r in found if r["audit"]["fie"])
    print(f"FIE-admissible among them: {fie}/{len(found)}")

    out = {"orbits": len(orbits), "models": len(found),
           "verdicts": dict(verdicts), "fibre_censuses": dict(census),
           "diagonal": diagonal, "s8s3_classes": len(canon),
           "fie_admissible": fie,
           "w8_w2_agreement": f"{agree}/{len(found)}",
           "records": found}
    with open("results_calib28.json", "w") as handle:
        json.dump(out, handle, indent=1, default=str)
    print("wrote results_calib28.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
