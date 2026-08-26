#!/usr/bin/env python3
"""W16 T4b -- audit the NEW (R) members and test the W16-B kill on them.

For every template produced by w16_enumR (single cells on a cubic skeleton C
with a proper 3-edge-colouring, Gamma = K_8 \\ C, everything else empty) and
for its sub-templates (Gamma minus j edges), report:
  m, Sigma, |F(Gamma)|, in (R)?, Gamma degree sequence, #effectively-clean
  mixed words, #k=1 words, #k=2 words, and per-site the number of
  (effectively-clean w, k=1 w') pairs differing ONLY at that site
  -- the input of mechanism W16-B (vertex factorisation).
"""
from __future__ import annotations
import os, sys, json, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w16_core import (EDGES, EIDX, FULL, W8_IMMUNE, MIXED, support,
                      gamma_edges, spanning_2conn, full_pm_indices,
                      extras_at)
from w16_enumR import audit_R, CUBIC_NAMED, proper_3_edge_colourings, \
    template_from

HERE = os.path.dirname(os.path.abspath(__file__))


def profile(T):
    fullm = full_pm_indices(T)
    km = {w: len(extras_at(T, w, fullm))
          for w in itertools.product(range(3), repeat=8)}
    clean = set(w for w in MIXED if km[w] == 0)
    k1 = set(w for w in MIXED if km[w] == 1)
    k2 = set(w for w in MIXED if km[w] == 2)
    ge = gamma_edges(T)
    deg = [0] * 8
    for u, v in ge:
        deg[u] += 1
        deg[v] += 1
    pairs = {}
    for t in range(8):
        n1 = n2 = 0
        for w in clean:
            for c in range(3):
                if c == w[t]:
                    continue
                wp = tuple(list(w[:t]) + [c] + list(w[t + 1:]))
                if wp in k1:
                    n1 += 1
                elif wp in k2:
                    n2 += 1
        pairs[t] = (n1, n2)
    a = audit_R(T)
    return dict(m=a["m"], sigma=a["sigma"], in_R=a["in_R"],
                gamma_pms=a["gamma_pms"], min_mixed=a["min_mixed_fibre"],
                gamma_deg=deg, n_clean=len(clean), n_k1=len(k1),
                n_k2=len(k2),
                w16B_pairs={str(t): list(pairs[t]) for t in range(8)},
                has_deg2_site=[t for t in range(8) if deg[t] == 2],
                w16B_usable_sites=[t for t in range(8) if pairs[t][0] > 0])


def main():
    out = {}
    for nm, C in CUBIC_NAMED.items():
        C = [(min(u, v), max(u, v)) for (u, v) in C]
        chis = proper_3_edge_colourings(C)
        gamma = [e for e in EDGES if e not in set(C)]
        rows = []
        # the full member and a chain of sub-templates (drop Gamma edges)
        for drop in range(0, 9):
            g = gamma[:len(gamma) - drop] if drop else gamma
            T = template_from(C, chis[0], g)
            p = profile(T)
            p["dropped"] = drop
            rows.append(p)
            if not p["in_R"]:
                break
        out[nm] = dict(n_colourings=len(chis), rows=rows,
                       template_m28=list(template_from(C, chis[0], gamma)))
        print("== %s (|chi|=%d)" % (nm, len(chis)))
        for p in rows:
            print("   m=%2d Sig=%3d inR=%-5s |F(G)|=%2d minfib=%2d deg=%s "
                  "clean=%4d k1=%4d k2=%4d  W16-B sites=%s"
                  % (p["m"], p["sigma"], p["in_R"], p["gamma_pms"],
                     p["min_mixed"], p["gamma_deg"], p["n_clean"],
                     p["n_k1"], p["n_k2"], p["w16B_usable_sites"]))
    json.dump(out, open(os.path.join(HERE, "results_newR.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
