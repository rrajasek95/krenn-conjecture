#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- verify PROPOSITION W12-C as a combinatorial fact.

CLAIM: an even bipartition (L,R) of B whose Gamma-crossing edges pairwise
intersect exists  <=>  Gamma (the graph of FULL nine-cell blocks) is NOT a
spanning 2-connected subgraph of K_N.
Checked by brute force on random graphs Gamma (this is a statement about
Gamma alone, so it is tested directly on graphs, not on templates)."""
from __future__ import annotations
import json, os, random, sys
from itertools import combinations
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import w12_cut as CUT           # noqa: E402
from run_t7_filters import components   # noqa: E402

N = 8
ALL = list(combinations(range(N), 2))


def spanning_2connected(G):
    verts = set()
    for e in G:
        verts.update(e)
    if verts != set(range(N)):
        return False
    if len(components(list(range(N)), G)) > 1:
        return False
    for x in range(N):
        rest = [v for v in range(N) if v != x]
        sub = [e for e in G if x not in e]
        if len(components(rest, sub)) > 1:
            return False
    return True


def feasible_cut(G):
    for (L, R) in CUT.even_cuts(N):
        cross = [e for e in G if (e[0] in L) != (e[1] in L)]
        if CUT.no_two_disjoint(cross):
            return True
    return False


rng = random.Random(17)
bad = []
n2c = 0
for trial in range(4000):
    k = rng.randrange(0, 20)
    G = rng.sample(ALL, k)
    a = spanning_2connected(G)
    b = feasible_cut(G)
    n2c += a
    if a == b:
        bad.append([sorted(map(list, G)), a, b])
out = {"trials": 4000, "spanning_2connected_seen": n2c,
       "counterexamples": bad[:5], "n_counterexamples": len(bad),
       "equivalence_holds": not bad}
print(f"random graphs tested: 4000; spanning-2-connected: {n2c}; "
      f"violations of the equivalence: {len(bad)}")
# deterministic controls
print("C8 (spanning 2-connected, 8 edges):",
      spanning_2connected([(i, (i + 1) % 8) for i in range(8)]),
      feasible_cut([(i, (i + 1) % 8) for i in range(8)]))
print("two disjoint 4-cycles (W8's m=20 Gamma):",
      spanning_2connected([(0,1),(1,2),(2,3),(0,3),(4,5),(5,6),(6,7),(4,7)]),
      feasible_cut([(0,1),(1,2),(2,3),(0,3),(4,5),(5,6),(6,7),(4,7)]))
json.dump(out, open(os.path.join(HERE, "results_t9_propcheck.json"), "w"),
          indent=1)
print("wrote results_t9_propcheck.json")
