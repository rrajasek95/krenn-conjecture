#!/usr/bin/env python3
r"""UNAUDITED PROBE (W19-CENSUS) -- independent control of the (SC) counter.

UNAUDITED.  Nothing here is a proved claim of the repository.

The census totals rest on ONE closed form: the inclusion-exclusion count of
(SC)-admissible completions of a given Gamma.  Here the same numbers are
recomputed by a COMPLETELY DIFFERENT exact algorithm -- a dynamic program
over the coverage state (which colours each vertex has already been given
by the edges processed so far) -- plus:
  * a zero control: any Gamma with a vertex of degree 5 must count 0;
  * a mutation control: a corrupted mask-multiplicity table must disagree.
"""
from __future__ import annotations

import json
import os
import sys
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w19c_lib import (  # noqa: E402
    EDGES, EIDX, N, NE, degseq, mask_to_edges, my_tokens, spanning_2conn,
)
from w19c_census import count_sc  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RES = {}

# multiplicity of each token pair among the 511 admissible masks (0..510),
# brute forced here rather than assumed
MULT = {}
for m in range(511):
    MULT[my_tokens(m)] = MULT.get(my_tokens(m), 0) + 1
RES["mask_multiplicities"] = {str(k): v for k, v in
                              sorted(MULT.items(), key=lambda t: str(t[0]))}
assert sum(MULT.values()) == 511


POPC = [bin(x).count("1") for x in range(8)]


def dp_count(gamma_mask, mult=None):
    """EXACT #(SC)-admissible completions, by DP over coverage states.

    Independent of the inclusion-exclusion closed form.  Feasibility pruning:
    a state is dead as soon as some vertex still needs more colours than it
    has remaining incident free edges."""
    if mult is None:
        mult = MULT
    free = [EDGES[ei] for ei in range(NE) if not (gamma_mask >> ei) & 1]
    free = sorted(free, key=lambda e: (e[1], e[0]))
    remain = [0] * N
    for (u, v) in free:
        remain[u] += 1
        remain[v] += 1
    states = {(0,) * N: 1}
    for (u, v) in free:
        remain[u] -= 1
        remain[v] -= 1
        nxt = {}
        for st, c in states.items():
            for (au, av), mu in mult.items():
                s2 = list(st)
                if au is not None:
                    s2[u] |= 1 << au
                if av is not None:
                    s2[v] |= 1 << av
                if 3 - POPC[s2[u]] > remain[u] or 3 - POPC[s2[v]] > remain[v]:
                    continue
                t = tuple(s2)
                nxt[t] = nxt.get(t, 0) + c * mu
        states = nxt
    return states.get((7,) * N, 0)


G = json.load(open(os.path.join(HERE, "results_gamma.json")))
ROWS = G["gamma_classes"]

print("independent DP vs the closed form:")
tests = []
sel = ([r for r in ROWS if r["n_edges"] == 16][:2]
       + [r for r in ROWS if r["n_edges"] == 15][:2]
       + [r for r in ROWS if r["n_edges"] == 14][:1])
for r in sel:
    a = dp_count(r["mask"])
    b = r["n_sc_completions"]
    c = count_sc(r["mask"])
    ok = (a == b == c)
    tests.append(dict(n_edges=r["n_edges"], dp=a, gamma_json=b, weighted=c,
                      agree=ok))
    print("  |Gamma|=%2d  DP=%-24d closed=%-24d %s"
          % (r["n_edges"], a, b, "OK" if ok else "MISMATCH"))
RES["dp_vs_closed_form"] = tests
RES["dp_all_agree"] = all(t["agree"] for t in tests)

# zero control: a Gamma with a degree-5 vertex admits NO (SC) completion
zc = []
found = 0
for r in ROWS:
    if found >= 2:
        break
    gm = r["mask"] | (1 << EIDX[EDGES[0]])
    es = mask_to_edges(gm)
    d = degseq(es)
    if max(d) < 5:
        continue
    found += 1
    zc.append(dict(maxdeg=max(d), dp=dp_count(gm), closed=count_sc(gm)))
# construct one directly: a vertex of degree 5
gm = 0
for j in range(1, 7):
    gm |= 1 << EIDX[(0, j)]
for e in [(1, 2), (3, 4), (5, 6), (2, 7), (4, 7)]:
    gm |= 1 << EIDX[e]
zc.append(dict(maxdeg=max(degseq(mask_to_edges(gm))), dp=dp_count(gm),
               closed=count_sc(gm)))
RES["zero_controls"] = zc
RES["zero_controls_all_zero"] = all(z["dp"] == 0 and z["closed"] == 0
                                    for z in zc)
print("zero control (max degree >= 5 => 0 completions):",
      RES["zero_controls_all_zero"], zc)

# mutation control: corrupt the multiplicity table, require disagreement.
# NB the corrupted entry must be REACHABLE for the instance used: at
# |Gamma| = 16 every free edge is forced to be a single, so perturbing the
# (None,None) multiplicity there changes nothing (first run of this control
# did not fire for exactly that reason -- recorded).
muts = []
for key in [(0, 0), (None, None), (1, None)]:
    BAD = dict(MULT)
    BAD[key] = BAD[key] - 1
    for r0 in sel:
        d = dp_count(r0["mask"], BAD)
        muts.append(dict(key=str(key), n_edges=r0["n_edges"],
                         differs=bool(d != r0["n_sc_completions"])))
mut = any(m["differs"] for m in muts)
RES["MUTATION_detail"] = muts
RES["MUTATION_bad_multiplicity_disagrees"] = mut
RES["MUTATION_single_entry_fires_at_16"] = any(
    m["differs"] for m in muts if m["key"] == "(0, 0)")
print("mutation control (corrupted multiplicity table disagrees):", mut,
      [m for m in muts if m["differs"]][:4])

json.dump(RES, open(os.path.join(HERE, "results_ctl_count.json"), "w"),
          indent=1)
print("written")
