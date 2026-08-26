#!/usr/bin/env python3
"""W21-M2-SING: EVIDENCE-ONLY numerical probe of the fixed-y slices.

*** FLOATS.  NOTHING HERE IS A VERDICT (LEDGER 17).  It only tells me where to
*** point the exact Singular computation.  Any hit is re-derived exactly.

The fixed-y slice is MULTILINEAR: each of the 30 equations contains exactly one
vector g[i][c] from each of the four groups, linearly.  So the system is LINEAR
in each of the 12 vectors separately, and alternating least squares + Newton is
a strong solver for it.
"""
import json
import sys
from itertools import product

sys.dont_write_bytecode = True
import m2core as M
import m2sys as S

try:
    import numpy as np
except ImportError:
    print("numpy unavailable -- probe skipped")
    sys.exit(0)

rngseed = 12345


def slice_data(y):
    """returns (cells, eqs) for the fixed-y slice, cells sorted."""
    e, cl, lb = S.sys_fixed_y(y)
    return cl, e


def make_funcs(cells, eqs):
    idx = {c: k for k, c in enumerate(cells)}
    terms = []
    for p in eqs:
        terms.append([(c, tuple(idx[v] for v in mon))
                      for mon, c in p.items()])
    n = len(cells)

    def F(z):
        out = np.empty(len(terms))
        for k, tl in enumerate(terms):
            s = 0.0
            for c, mon in tl:
                t = float(c)
                for v in mon:
                    t *= z[v]
                s += t
            out[k] = s
        return out

    def J(z):
        out = np.zeros((len(terms), n))
        for k, tl in enumerate(terms):
            for c, mon in tl:
                for a in range(len(mon)):
                    t = float(c)
                    for b, v in enumerate(mon):
                        if b != a:
                            t *= z[v]
                    out[k, mon[a]] += t
        return out
    return F, J, n


def probe(y, ntry=400, seed=0):
    cells, eqs = slice_data(y)
    F, J, n = make_funcs(cells, eqs)
    rng = np.random.default_rng(rngseed + seed)
    best = None
    for t in range(ntry):
        z = rng.normal(size=n)
        z = np.where(np.abs(z) < 0.3, 0.7, z)
        for it in range(220):
            f = F(z)
            r = float(np.max(np.abs(f)))
            if r < 1e-13:
                break
            g = J(z)
            try:
                dz = np.linalg.lstsq(g, -f, rcond=None)[0]
            except np.linalg.LinAlgError:
                break
            st = 1.0
            for _ in range(30):
                z2 = z + st * dz
                if float(np.max(np.abs(F(z2)))) < r:
                    break
                st *= 0.5
            else:
                break
            z = z + st * dz
            nz = float(np.min(np.abs(z)))
            if nz < 1e-4:                     # drifting to a zero cell: push out
                z = z + 1e-3 * rng.normal(size=n)
        f = F(z)
        r = float(np.max(np.abs(f)))
        mn = float(np.min(np.abs(z)))
        sc = float(np.max(np.abs(z)))
        # scale-invariant residual: the equations are quartic homogeneous
        rr = r / max(sc, 1e-12) ** 4
        if rr < 1e-11 and mn / max(sc, 1e-12) > 1e-3:
            return {"y": ''.join(map(str, y)), "hit": True, "res": rr,
                    "minabs": mn / sc, "tries": t + 1}
        if best is None or (rr, -mn) < best[0]:
            best = ((rr, -mn), mn / max(sc, 1e-12))
    return {"y": ''.join(map(str, y)), "hit": False, "best_res": best[0][0],
            "best_minabs": best[1], "tries": ntry}


if __name__ == "__main__":
    out = {"_header": "UNAUDITED W21-M2-SING EVIDENCE-ONLY numerical probe "
                      "(floats; never a verdict)"}
    ys = sys.argv[1].split(",") if len(sys.argv) > 1 else \
        ["0101", "0200", "0201", "1101", "0100", "2020", "0001"]
    for ys1 in ys:
        y = tuple(int(ch) for ch in ys1)
        r = probe(y, ntry=int(sys.argv[2]) if len(sys.argv) > 2 else 250)
        print("  y=%s  %s" % (ys1, r))
        out.setdefault("probes", []).append(r)
    json.dump(out, open("results_probe.json", "w"), indent=1, default=str)
