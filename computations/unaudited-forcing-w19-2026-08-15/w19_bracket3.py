#!/usr/bin/env python3
"""W19 -- bracket feasibility over GENERAL rational scalars s_e (not just
signs), for the (R) Gammas.  UNAUDITED.  Exact (Singular over Q).

Same question as w19_bracket2.py but with s_e free: is there s: E -> K^*
with sum_{M in F(Gamma)} (prod_{e in M} s_e) [M] == 0 identically?
Gauge s_uv -> lam_u lam_v s_uv lets us set s_e = 1 on a spanning tree.
POSITIVE CONTROL K_4 must come out FEASIBLE.
"""
import os, sys, json, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w19_core import EDGES, W8_IMMUNE, gamma_edges
from w19_bracket import (pdata, bracket_matrix, kernel_basis, rref,
                         multiplicative_in_kernel, matchings_of)

HERE = os.path.dirname(os.path.abspath(__file__))

def run(edges, n, name, timeout=1800):
    P = pdata(n, seed=7)
    words = list(itertools.product(range(3), repeat=n))
    Ms, rows = bracket_matrix(edges, n, P, words)
    ker = kernel_basis(rows, len(Ms))
    r = dict(name=name, n_matchings=len(Ms), kernel_dim=len(ker))
    if not ker:
        r["multiplicative"] = dict(empty=True, feasible=False,
                                   reason="kernel is zero")
    else:
        r["multiplicative"] = multiplicative_in_kernel(edges, n, Ms, rows,
                                                       timeout=timeout,
                                                       tag=name)
    return r

if __name__ == "__main__":
    out = {}
    K4 = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    out["CONTROL_K4"] = run(K4, 4, "K4 (positive control)")
    print("CONTROL K4:", out["CONTROL_K4"], flush=True)
    for m in (25, 26, 27, 28):
        ge = gamma_edges(W8_IMMUNE[m])
        out["W8_m%d" % m] = run(ge, 8, "W8 Gamma m=%d" % m, timeout=3600)
        print("W8 m=%d:" % m, out["W8_m%d" % m], flush=True)
    json.dump(out, open(os.path.join(HERE, "results_bracket3.json"), "w"),
              indent=1, default=str)
