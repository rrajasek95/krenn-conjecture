#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- free filters + the Gamma-connectivity diagnostic.

Filters applied to every target, in the coordinator's priority order:
  (F1) lattice screen  -- mixed singleton / binomial-lattice inconsistency
  (F2) (SC+)  [W11]    -- every (vertex,colour) demand needs a serving edge pj
                          with B\\{p,j} still carrying a template perfect
                          matching (else the activity cofactor C_pj vanishes)
  (F3) J.1d BUDGET     -- beta >= 24 - m + |H|, |H| = # blocks whose cell set
                          is NOT a combinatorial rectangle (A2's rank-one
                          realisability criterion)
  (F4) Gamma DIAGNOSTIC -- Gamma(T) = graph of the FULL nine-cell blocks.
                          The cut mechanism of w12_cut can only fire when some
                          even bipartition has its Gamma-crossing edges
                          pairwise intersecting, i.e. when Gamma is
                          disconnected or has a cut vertex.  This is the
                          exact structural boundary of the method.
"""

from __future__ import annotations

import json
import os
import sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w12_core as C          # noqa: E402
import w12_cut as CUT         # noqa: E402
import w12_targets as TG      # noqa: E402
from run_t4_calibration import load_survivor, load_immunity  # noqa: E402


def is_rectangle(mask):
    rows = sorted({i for i, _ in C.cells(mask)})
    cols = sorted({j for _, j in C.cells(mask)})
    return bin(mask).count("1") == len(rows) * len(cols)


def budget_check(geo, template):
    """(ok, beta, H, required)  for  beta >= 24 - m + |H|."""
    m = C.support(template)
    beta = sum(1 for mask in template if bin(mask).count("1") == 1)
    H = sum(1 for mask in template if mask and not is_rectangle(mask))
    need = 3 * geo.size - m + H
    return (beta >= need), beta, H, need


def gamma_graph(geo, template):
    return [geo.edges[e] for e, mask in enumerate(template) if mask == C.FULL9]


def components(vertices, edges):
    parent = {v: v for v in vertices}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        a, b = find(u), find(v)
        if a != b:
            parent[a] = b
    groups = {}
    for v in vertices:
        groups.setdefault(find(v), []).append(v)
    return list(groups.values())


def gamma_diagnostic(geo, template):
    """Where Gamma sits: 'empty' | 'disconnected' | 'cut-vertex' |
    '2-connected'.  Also reports whether an EVEN bipartition exists whose
    Gamma-crossing edges pairwise intersect (the precise cut hypothesis)."""
    G = gamma_graph(geo, template)
    verts = list(range(geo.size))
    comps = components(verts, G)
    nontrivial = [c for c in comps if len(c) > 1]
    status = "empty" if not G else ("disconnected" if len(nontrivial) +
                                    sum(1 for c in comps if len(c) == 1) > 1
                                    else "connected")
    cutverts = []
    if status == "connected":
        touched = {v for e in G for v in e}
        for x in touched:
            rest = [v for v in touched if v != x]
            sub = [e for e in G if x not in e]
            if len(components(rest, sub)) > 1:
                cutverts.append(x)
        status = "cut-vertex" if cutverts else "2-connected"
    feasible = []
    for (L, R) in CUT.even_cuts(geo.size):
        cross = [e for e in G if (e[0] in L) != (e[1] in L)]
        if CUT.no_two_disjoint(cross):
            feasible.append(sorted(L))
    return {"gamma_edges": [list(e) for e in G], "gamma_size": len(G),
            "status": status, "cut_vertices": sorted(cutverts),
            "even_cuts_with_star_gamma_crossing": feasible[:8],
            "n_feasible_cuts": len(feasible)}


def main():
    geo = C.geometry()
    targets = [("survivor_m20", load_survivor())]
    targets += [(f"immunity_m{m}", t) for m, t, _ in load_immunity()]
    targets += TG.load_w11_witnesses()
    targets += [(n, t) for n, t, _ in TG.load_w8_m17_classes()]
    rows = []
    for name, tmpl in targets:
        a = C.audit(geo, tmpl)
        scp_ok, scp_bad = TG.sc_plus(geo, tmpl)
        b_ok, beta, H, need = budget_check(geo, tmpl)
        g = gamma_diagnostic(geo, tmpl)
        rows.append({"name": name, "m": a["m"], "sigma": a["sigma"],
                     "beta": a["beta"], "min_mixed_fibre": a["min_mixed_fibre"],
                     "sc_plus": scp_ok, "sc_plus_failures": scp_bad,
                     "budget_ok": b_ok, "budget": [beta, H, need],
                     "gamma": g})
    # summary
    import collections
    print("=== filter summary over", len(rows), "targets ===")
    print("(SC+) failures :", sum(1 for r in rows if not r["sc_plus"]))
    print("budget failures:", sum(1 for r in rows if not r["budget_ok"]))
    print("gamma status   :", dict(collections.Counter(
        r["gamma"]["status"] for r in rows)))
    print("no feasible cut:", [r["name"] for r in rows
                               if r["gamma"]["n_feasible_cuts"] == 0])
    print("\nname                   m   S  beta minfib  SC+ budget  gamma")
    for r in rows:
        if not r["name"].startswith("m17_class"):
            print(f"{r['name']:22s} {r['m']:2d} {r['sigma']:3d} {r['beta']:3d} "
                  f"{r['min_mixed_fibre']:5d}  {'Y' if r['sc_plus'] else 'N'}"
                  f"    {'Y' if r['budget_ok'] else 'N'}    "
                  f"{r['gamma']['status']} (|G|={r['gamma']['gamma_size']}, "
                  f"cuts={r['gamma']['n_feasible_cuts']})")
    with open(os.path.join(HERE, "results_t7_filters.json"), "w") as fh:
        json.dump(rows, fh, indent=1)
    print("wrote results_t7_filters.json")


if __name__ == "__main__":
    main()
