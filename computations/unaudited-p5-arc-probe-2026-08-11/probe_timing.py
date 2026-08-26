#!/usr/bin/env python3
"""Feasibility probe: how expensive is the P5 Schur graph at higher order?

READ-ONLY with respect to the repo: it only imports the committed checkers.
"""

import importlib.util
import sys
import time
from pathlib import Path

COMP = Path("/Users/rishi/workplace/krenn-conjecture/computations")


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, COMP / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


t0 = time.time()
R4 = load_module("p5_r4_probe", "verify_n8_p5_generic_L_koszul_ward_r4.py")
print(f"load koszul_ward_r4 module: {time.time()-t0:.1f}s", flush=True)

G = R4.G
F2 = R4.F2
WARD = R4.WARD

t0 = time.time()
base = F2.audit(return_data=True)
print(f"F2.audit: {time.time()-t0:.1f}s", flush=True)
print("base keys:", sorted(base.keys()), flush=True)
print("normal rows", len(base["normal"]),
      "transverse", len(base["transverse"]),
      "obstruction", len(base["obstruction"]), flush=True)

for maximum_order in (7, 8, 9, 10):
    t0 = time.time()
    graph = G.source_graph(base, maximum_order=maximum_order,
                           additional_bends=1)
    dt = time.time() - t0
    terms = [sum(map(len, row)) for row in graph["compatibility_orders"]]
    print(f"maximum_order={maximum_order}: {dt:.1f}s, "
          f"compat terms per order={terms}", flush=True)
