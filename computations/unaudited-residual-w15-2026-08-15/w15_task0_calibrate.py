#!/usr/bin/env python3
"""W15 TASK 0 -- calibration of the independent model against W8's audit.

Exact / combinatorial only.  Checks:
  C1  the hard-coded templates equal W8's results_immunity.json verbatim
  C2  m, Sigma, fibre histogram, min mixed fibre agree with W8's audit
  C3  Gamma(T) spanning-2-connected predicate: W12-C says a feasible cut
      exists iff Gamma is NOT spanning 2-connected; report per instance
  C4  mutation control: a mutated template must DISAGREE with W8's audit
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w15_core import (W8_IMMUNE, audit, gamma_graph, is_spanning_2_connected,
                      single_cell_activity, EDGES, FULL)

ROOT = "/Users/rishi/workplace/krenn-conjecture"
W8JSON = os.path.join(ROOT, "computations",
                      "unaudited-template-kill-w8-2026-08-15",
                      "results_immunity.json")

out = {"checks": {}, "instances": {}}
w8 = json.load(open(W8JSON))
w8map = {r["m"]: r for r in w8["results"]}

# ---- C1 templates verbatim
c1 = all(list(W8_IMMUNE[m]) == list(w8map[m]["template"]) for m in W8_IMMUNE)
out["checks"]["C1_templates_match_w8_json"] = bool(c1)
assert c1, "hard-coded templates differ from W8's JSON"

# ---- C2 audit agreement
agree = {}
for m, T in sorted(W8_IMMUNE.items()):
    a = audit(T)
    ref = w8map[m]["audit"]
    hist_ref = {int(k): v for k, v in ref["fibre_histogram"].items()}
    ok = (a["m"] == ref["m"] and a["sigma"] == ref["sigma"]
          and a["fibre_histogram"] == hist_ref
          and a["min_mixed_fibre"] == w8map[m]["min_mixed_fibre"])
    agree[m] = bool(ok)
    g = gamma_graph(T)
    sp, why = is_spanning_2_connected(g)
    out["instances"][m] = {
        "m": a["m"], "sigma": a["sigma"],
        "min_mixed_fibre": a["min_mixed_fibre"],
        "constant_fibres": a["constant_fibres"],
        "n_full": a["n_full"], "n_single": a["n_single"],
        "gamma_edges": [list(e) for e in g],
        "gamma_spanning_2connected": bool(sp), "gamma_reason": why,
        "single_cells": {f"{u}-{v}": c
                         for (u, v), c in a["single_cells"].items()},
        "audit_matches_w8": bool(ok),
    }
    print(f"m={m:2d} sigma={a['sigma']:3d} full={a['n_full']:2d} "
          f"single={a['n_single']:2d} minmixed={a['min_mixed_fibre']:2d} "
          f"constfib={a['constant_fibres']} "
          f"Gamma_sp2c={sp} ({why})  auditmatch={ok}")
out["checks"]["C2_audit_agrees_all"] = all(agree.values())
assert all(agree.values()), "audit disagreement with W8"

# ---- C4 mutation control: flip one bit of the m=24 template.
T = list(W8_IMMUNE[24])
mut_bad = 0
for e in range(28):
    for bit in range(9):
        T2 = list(T)
        T2[e] ^= (1 << bit)
        a2 = audit(T2)
        ref = w8map[24]["audit"]
        if (a2["sigma"] == ref["sigma"]
                and a2["fibre_histogram"] ==
                {int(k): v for k, v in ref["fibre_histogram"].items()}):
            mut_bad += 1
out["checks"]["C4_mutation_controls_tested"] = 28 * 9
out["checks"]["C4_mutations_falsely_matching"] = mut_bad
print(f"\nmutation control: {28*9} single-bit template mutations, "
      f"{mut_bad} falsely reproduce W8's m=24 audit (want 0)")
assert mut_bad == 0

json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "results_task0_calibrate.json"), "w"),
          indent=1)
print("\nCALIBRATION PASSED")
