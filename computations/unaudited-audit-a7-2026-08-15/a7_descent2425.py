#!/usr/bin/env python3
"""A7 -- independent second route to the m=25 witness: random descent on the
clean layer (W20-L machinery), starting from J-points, at m=24 and m=25.
If the descent reaches ZERO factoring sites, the hand-built witness of
a7_witness25.py is independently corroborated."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a7_core import W8_IMMUNE
from a7_w20 import descent

HERE = os.path.dirname(os.path.abspath(__file__))
out = {}
for m in (24, 25):
    runs = []
    for seed in (2, 5, 11, 23, 37):
        r, blocks, gam, clean = descent(W8_IMMUNE[m], seed, steps=120)
        r.pop("blocks")
        runs.append(r)
        print("m=%d seed=%d -> factoring %s clean_ok=%s nonzero=%s n_clean=%d"
              % (m, seed, r["factoring_sites"], r["clean_equations_hold"],
                 r["all_gamma_cells_nonzero"], r["n_clean"]), flush=True)
    out["m%d" % m] = runs
json.dump(out, open(os.path.join(HERE, "results_descent2425.json"), "w"),
          indent=1, default=str)
