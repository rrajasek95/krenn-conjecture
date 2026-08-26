#!/usr/bin/env python3
"""A3 -- (SC)-admissibility of the certified N=10 singleton-free templates,
cross-checked against W2's INDEPENDENT kill engine.

(SC) slice-cover admissibility (coordinator's statement): for every
(vertex p, colour r) slot there is an incident edge pj ALL of whose cells
carry colour r at the FAR endpoint j.  For a monomial template each edge has
one cell (a,b) -- a the colour at the smaller endpoint -- so (SC) at (p,r)
holds iff p has an incident edge whose far-endpoint colour is r.  For a
DIAGONAL template that is: every colour graph has min degree >= 1.

Also checked: min live degree >= 3 (the slice-cover forced-incidence input),
all 3N (vertex,colour) slots covered (W6's structural_ok), and the verdict of
W2's w2_monomial.analyse (a completely separate code path: fibre enumeration
+ integer Hermite + Q^* character closure).
"""
import json, sys
sys.path.insert(0, '.')
sys.path.insert(0, '/Users/rishi/workplace/krenn-conjecture/computations/unaudited-witness-splitting-w2-2026-08-15')
from a3_core import DiagonalTemplate
import w2_monomial as W2

N = 10


def sc_admissible(ce):
    """(ok, per-slot table) for a diagonal template given as 3 edge sets."""
    bad = []
    for v in range(N):
        for r in range(3):
            hit = any(v in e for e in ce[r])
            if not hit:
                bad.append((v, r))
    return (not bad), bad


def live_degrees(ce):
    deg = [0] * N
    for r in range(3):
        for u, v in ce[r]:
            deg[u] += 1
            deg[v] += 1
    return deg


def to_labels(ce):
    geo = W2.geometry(N)
    lab = [None] * len(geo.edges)
    for r in range(3):
        for e in ce[r]:
            lab[geo.index[tuple(sorted(e))]] = (r, r)
    return geo, lab


def main():
    src = {}
    for path, key in (("results_certify10.json", "hits"),
                      ("results_certify10_quick.json", None)):
        try:
            d = json.load(open(path))
        except Exception:
            continue
        d = d[key] if key else d
        for k, v in d.items():
            src.setdefault(str(k), v)
    out = {}
    for k, cert in sorted(src.items()):
        ce = [[tuple(e) for e in cert["colour_edges"][r]] for r in range(3)]
        ok, bad = sc_admissible(ce)
        deg = live_degrees(ce)
        geo, lab = to_labels(ce)
        verdict = W2.analyse(geo, lab)
        s_w2, hist_w2 = W2.fibre_profile(W2.fibres(geo, lab))
        row = dict(support=cert["support"], pures=cert["pures_product"],
                   singletons_A3=cert["singletons_product"],
                   singletons_W2=s_w2,
                   histograms_agree=(
                       {str(a): b for a, b in hist_w2.items()}
                       == cert["histogram_product"]),
                   SC_admissible=ok, SC_violations=bad,
                   min_live_degree=min(deg), live_degrees=deg,
                   W2_verdict=verdict["verdict"])
        out[k] = row
        print(f"{k}: support={row['support']} pures={row['pures']} "
              f"singletons A3={row['singletons_A3']} W2={row['singletons_W2']} "
              f"hist agree={row['histograms_agree']} | (SC)-admissible="
              f"{ok} | min live degree={row['min_live_degree']} | "
              f"W2 verdict={row['W2_verdict']}")
        if bad:
            print("    (SC) violations:", bad)
    json.dump(out, open("results_admissibility10.json", "w"), indent=1)
    print("wrote results_admissibility10.json")


if __name__ == "__main__":
    main()
