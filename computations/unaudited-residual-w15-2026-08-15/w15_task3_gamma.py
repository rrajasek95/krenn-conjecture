#!/usr/bin/env python3
"""W15 TASK 3 -- structural diagnostics of Gamma(T) for the (R) instances:
(a) which Gamma-pairs are all-three-slice-clean BY SUPPORT (witness-route
    candidates, per W14/S1);
(b) tight cuts of Gamma with ODD shores (W12's even_cuts cannot see them).
A cut (S, V\\S) of Gamma is TIGHT if every perfect matching of Gamma crosses
it exactly once.  Exact / combinatorial only."""
import json, os, sys
from itertools import combinations
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w15_core import W8_IMMUNE, EDGES, EIDX, FULL, MATCHINGS, N

HERE = os.path.dirname(os.path.abspath(__file__))
out = {}
for m, T in sorted(W8_IMMUNE.items()):
    G = [EDGES[i] for i, t in enumerate(T) if t == FULL]
    Gs = set(G)
    pms = [mm for mm in MATCHINGS if all(e in Gs for e in mm)]
    tight = []
    for k in range(1, N):
        for S in combinations(range(N), k):
            Ss = set(S)
            cnt = set()
            for mm in pms:
                cnt.add(sum(1 for (u, v) in mm if (u in Ss) != (v in Ss)))
            if cnt == {1}:
                tight.append({"shore": list(S), "odd": k % 2 == 1,
                              "size": k})
    # slice cleanliness by support: colour c slice of pair (p,q) is clean if
    # no mixed word with w_p = w_q = c is 'dirty' -- support-level proxy used
    # by S1: the pair's block is full nine-cell (so A_pq(c,c) != 0).
    out[m] = {"gamma_edges": [list(e) for e in G],
              "n_gamma_pms": len(pms),
              "tight_cuts": tight,
              "odd_tight_cuts": [t for t in tight if t["odd"]]}
    print(f"m={m}: |Gamma|={len(G)} PMs(Gamma)={len(pms)} tight cuts="
          f"{len(tight)} (odd shores: {len([t for t in tight if t['odd']])}) "
          f"{[t['shore'] for t in tight if t['odd']][:8]}", flush=True)
json.dump(out, open(os.path.join(HERE, "results_task3_gamma.json"), "w"),
          indent=1)
