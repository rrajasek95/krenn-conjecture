#!/usr/bin/env python3
"""W16 -- the VERTEX-FACTORISATION kill (mechanism W16-B).

IDEA.  Every perfect matching of Gamma covers a vertex t by exactly one
Gamma-edge at t.  If all Gamma-blocks at t share a common "t-vector", i.e.
for every Gamma-neighbour s of t

        A_{ts}[c_t][c_s] = gamma_{c_t} * (something depending on c_s only,
                                          and on the edge)

-- equivalently every A_ts (t-index first) is RANK ONE with t-side vector
proportional to a single gamma -- then Phi(w) = gamma_{w_t} * Psi(w without
site t).  Consequently, for two words w, w' that AGREE off site t,

        Phi_w = 0   <=>   Phi_{w'} = 0        (gamma nowhere zero).

KILL: take w EFFECTIVELY CLEAN (so Phi_w = H_w = 0, w mixed) and w' with
exactly ONE extra (so H_{w'} = Phi_{w'} + monomial = 0).  Then Phi_{w'} = 0
forces that occupied-cell monomial to vanish -- impossible.

This module (1) enumerates, per site t, the (clean w, k=1 w') pairs that
differ only at t -- pure combinatorics, template only; and (2) records which
sites have Gamma-degree 2 (where the factorisation is a DICHOTOMY branch
rather than an extra hypothesis).
"""
from __future__ import annotations
import os, sys, json, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w16_core import (W8_IMMUNE, EDGES, EIDX, FULL, full_pm_indices,
                      extras_at, gamma_edges, MIXED)

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out = {}
    for m in (24, 25, 26, 27, 28):
        T = W8_IMMUNE[m]
        fullm = full_pm_indices(T)
        ge = gamma_edges(T)
        deg = {v: 0 for v in range(8)}
        for u, v in ge:
            deg[u] += 1
            deg[v] += 1
        kmap = {}
        for w in itertools.product(range(3), repeat=8):
            kmap[w] = len(extras_at(T, w, fullm))
        clean = set(w for w in MIXED if kmap[w] == 0)
        k1 = set(w for w in MIXED if kmap[w] == 1)
        k2 = set(w for w in MIXED if kmap[w] == 2)
        pairs = {}
        for t in range(8):
            got1, got2 = [], []
            for w in clean:
                for c in range(3):
                    if c == w[t]:
                        continue
                    wp = list(w); wp[t] = c; wp = tuple(wp)
                    if wp in k1:
                        got1.append(("".join(map(str, w)),
                                     "".join(map(str, wp))))
                    elif wp in k2:
                        got2.append(("".join(map(str, w)),
                                     "".join(map(str, wp))))
            pairs[t] = dict(gamma_degree=deg[t],
                            gamma_nbrs=sorted(x for e in ge for x in e
                                              if t in e and x != t),
                            n_clean_to_k1=len(got1),
                            n_clean_to_k2=len(got2),
                            example_k1=got1[:3], example_k2=got2[:3])
        out[m] = dict(gamma_degrees={str(v): deg[v] for v in range(8)},
                      n_clean=len(clean), n_k1=len(k1), n_k2=len(k2),
                      per_site=pairs)
        print("m=%d  gamma degrees %s" % (m, [deg[v] for v in range(8)]))
        for t in range(8):
            p = pairs[t]
            print("   site %d (deg %d, nbrs %s): clean->k1 pairs %4d ;"
                  " clean->k2 pairs %4d  %s"
                  % (t, p["gamma_degree"], p["gamma_nbrs"],
                     p["n_clean_to_k1"], p["n_clean_to_k2"],
                     p["example_k1"][:1]))
    json.dump(out, open(os.path.join(HERE, "results_vertex.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
