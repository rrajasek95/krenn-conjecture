#!/usr/bin/env python3
"""W27 T2d -- IS THERE A SKELETON LAW AT N = 8?

T2c decided 377 live pairs of 26 diagonal X_3 skeletons at N = 8 exactly and
showed that W27-S1 (the N=6 law, a function of the two endpoint STARS only)
does NOT extend: 12 of the 63 endpoint-type cells are mixed.  This runner
rebuilds the same objects (same seed), attaches GLOBAL skeleton features, and
asks whether any of them separates witness from blocked at N = 8 -- and
whether the resulting rule restricts to W27-S1 at N = 6.
"""
from __future__ import annotations

import json
import random
import sys
from collections import Counter, defaultdict
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-penult-w27-2026-08-18")
sys.path.insert(0, BASE)
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-x3core-w25-2026-08-15")
import w27_core as W                                              # noqa: E402
import run_t2c_n8law as T2C                                       # noqa: E402
C = W.C

N = 8
G = W.Graph(N)
RES = {}
RAN = []
OUT = f"{BASE}/results_t2d_n8rule.json"


def control(name):
    if name not in RAN:
        RAN.append(name)


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def rich(Ls, p, q):
    e = tuple(sorted((p, q)))
    c1 = [c for c in range(3) if e in Ls[c]][0]
    c2, c3 = [c for c in range(3) if c != c1]
    deg = {v: [sum(1 for f in Ls[c] if v in f) for c in range(3)]
           for v in range(N)}
    rest = [x for x in range(N) if x not in (p, q)]
    mk = [G.mask(Ls[c]) for c in range(3)]
    npm_rest = [G.npm_on(mk[c], rest) for c in range(3)]
    npm_full = [G.npm_on(mk[c], list(range(N))) for c in range(3)]
    off = set(Ls[c2]) | set(Ls[c3])
    adj = defaultdict(set)
    for (a, b) in off:
        adj[a].add(b)
        adj[b].add(a)
    seen, comps = set(), []
    for v in range(N):
        if v in seen:
            continue
        st, comp = [v], {v}
        seen.add(v)
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in comp:
                    comp.add(y)
                    seen.add(y)
                    st.append(y)
        comps.append(sorted(comp))
    pc = [i for i, cc in enumerate(comps) if p in cc][0]
    qc = [i for i, cc in enumerate(comps) if q in cc][0]
    dp, dq = deg[p], deg[q]
    tp = (dp[c1], tuple(sorted([dp[c2], dp[c3]])))
    tq = (dq[c1], tuple(sorted([dq[c2], dq[c3]])))
    return {
        "colour": c1,
        "sizes": sorted(len(L) for L in Ls),
        "type_pair": str(tuple(sorted([tp, tq]))),
        "min_deg_c1": min(dp[c1], dq[c1]),
        "max_deg_c1": max(dp[c1], dq[c1]),
        "min_live_deg": min(sum(dp), sum(dq)),
        "max_live_deg": max(sum(dp), sum(dq)),
        "n_clean_endpoints": int(dp == [1, 1, 1]) + int(dq == [1, 1, 1]),
        "n_clean_vertices": sum(1 for v in range(N) if deg[v] == [1, 1, 1]),
        "npm_rest_c1": npm_rest[c1],
        "npm_rest_off": str(sorted([npm_rest[c2], npm_rest[c3]])),
        "npm_full_c1": npm_full[c1],
        "npm_full_off": str(sorted([npm_full[c2], npm_full[c3]])),
        "off_comp_sizes": str(sorted(len(x) for x in comps)),
        "off_same_comp": pc == qc,
        "off_comp_p": len(comps[pc]),
        "off_comp_q": len(comps[qc]),
        "off_deg_p": len(adj[p]), "off_deg_q": len(adj[q]),
        "min_off_deg": min(len(adj[p]), len(adj[q])),
        "n_live_edges": len(set(Ls[0]) | set(Ls[1]) | set(Ls[2])),
        "both_clean": (dp == [1, 1, 1]) and (dq == [1, 1, 1]),
    }


def main():
    rng = random.Random(4242)
    objs = []
    for t in range(200):
        Ms = T2C.rand_disjoint_pms(rng)
        if Ms is None:
            continue
        Ls = [list(M) for M in Ms] if t % 3 == 0 else T2C.enlarge(Ms, rng)
        if not T2C.x2_ok(Ls):
            continue
        wts = T2C.weights(Ls, rng)
        if wts is None:
            continue
        src = W.build_diag(N, Ls, wts)
        if not C.in_Xk(src, N, 3)[0]:
            continue
        preds = {}
        for c in range(3):
            for e in Ls[c]:
                preds[f"{e[0]},{e[1]}"] = T2C.predict(Ls, *e)
        objs.append({"Ls": Ls, "preds": preds, "nB": sum(
            1 for v in preds.values() if v[0] == "BLOCKED"),
            "sizes": [len(L) for L in Ls]})
        if len(objs) >= 26:
            break
    objs.sort(key=lambda o: -o["nB"])

    with open(f"{BASE}/results_t2c_n8law.json") as fh:
        dec = json.load(fh)["decisions"]
    rows = []
    mism = 0
    for r in dec:
        o = objs[r["obj"]]
        p, q = (int(x) for x in r["pair"].split(","))
        f = rich(o["Ls"], p, q)
        if f["colour"] != r["colour"]:
            mism += 1
        rows.append({"verdict": r["decided"], "predicted_S1": r["predicted"],
                     "obj": r["obj"], "pair": r["pair"], **f})
    print(f"rebuilt objects and joined {len(rows)} decisions; colour "
          f"mismatches {mism} (must be 0 -- proves the rebuild is identical)")
    assert mism == 0
    nW = sum(1 for r in rows if r["verdict"] == "WITNESS")
    print(f"   WITNESS {nW}, BLOCKED {len(rows) - nW}")
    RES["n_rows"] = len(rows)
    RES["n_witness"] = nW
    RES["table"] = rows
    control("T2d0_join")
    ck("join")

    print("=" * 74)
    print("(1) does ANY single feature separate at N = 8?")
    print("=" * 74)
    keys = [k for k in rows[0] if k not in ("verdict", "predicted_S1", "obj",
                                            "pair")]
    best = []
    for k in keys:
        cw = Counter(json.dumps(r[k]) for r in rows if r["verdict"] == "WITNESS")
        cb = Counter(json.dumps(r[k]) for r in rows if r["verdict"] == "BLOCKED")
        overlap = sum(min(cw[v], cb[v]) for v in set(cw) & set(cb))
        best.append((overlap, k, len(set(cw) | set(cb))))
    best.sort()
    for ov, k, nv in best[:12]:
        print(f"   overlap {ov:4d} (of {len(rows)})  {k}  ({nv} values)")
    RES["single_feature_overlap"] = [{"overlap": o, "feature": k,
                                      "n_values": nv} for o, k, nv in best]
    print(f"   PERFECT single-feature separators: "
          f"{[k for o, k, _ in best if o == 0]}")
    control("T2d1_singles")
    ck("singles")

    print("=" * 74)
    print("(2) sound one-sided features (sufficient for WITNESS / BLOCKED)")
    print("=" * 74)
    suff_w, suff_b = [], []
    for k in keys:
        vals = set(json.dumps(r[k]) for r in rows)
        for v in vals:
            sel = [r for r in rows if json.dumps(r[k]) == v]
            if not sel:
                continue
            if all(r["verdict"] == "WITNESS" for r in sel) and len(sel) >= 3:
                suff_w.append((len(sel), f"{k}=={v}"))
            if all(r["verdict"] == "BLOCKED" for r in sel) and len(sel) >= 3:
                suff_b.append((len(sel), f"{k}=={v}"))
    suff_w.sort(reverse=True)
    suff_b.sort(reverse=True)
    print(f"   sufficient-for-WITNESS: {len(suff_w)}; strongest "
          f"{[x[1] for x in suff_w[:5]]} covering {[x[0] for x in suff_w[:5]]}")
    print(f"   sufficient-for-BLOCKED: {len(suff_b)}; strongest "
          f"{[x[1] for x in suff_b[:5]]} covering {[x[0] for x in suff_b[:5]]}")
    RES["sufficient_witness"] = [{"n": n, "pred": s} for n, s in suff_w[:25]]
    RES["sufficient_blocked"] = [{"n": n, "pred": s} for n, s in suff_b[:25]]
    control("T2d2_onesided")
    ck("onesided")

    print("=" * 74)
    print("(3) the both-clean fragment (W25-U3, proved at every N) at N = 8")
    print("=" * 74)
    bc = [r for r in rows if r["both_clean"]]
    print(f"   pairs with both endpoints clean: {len(bc)}; witnesses "
          f"{sum(1 for r in bc if r['verdict'] == 'WITNESS')} (must be all)")
    assert all(r["verdict"] == "WITNESS" for r in bc)
    RES["both_clean"] = {"n": len(bc)}
    control("T2d3_bothclean")

    print("=" * 74)
    print("(4) the mixed cells of the N=6 law: what distinguishes them?")
    print("=" * 74)
    tab = defaultdict(list)
    for r in rows:
        tab[r["type_pair"]].append(r)
    lines = []
    for k, v in sorted(tab.items()):
        nw = sum(1 for r in v if r["verdict"] == "WITNESS")
        if 0 < nw < len(v):
            inner = []
            for k2 in keys:
                cw = Counter(json.dumps(r[k2]) for r in v
                             if r["verdict"] == "WITNESS")
                cb = Counter(json.dumps(r[k2]) for r in v
                             if r["verdict"] == "BLOCKED")
                if not (set(cw) & set(cb)):
                    inner.append(k2)
            line = (f"   type {k}: W{nw} B{len(v) - nw}; features that "
                    f"separate INSIDE the cell: {inner[:6]}")
            print(line)
            lines.append(line)
    RES["mixed_cells"] = lines
    control("T2d4_mixed_cells")

    declared = ["T2d0_join", "T2d1_singles", "T2d2_onesided", "T2d3_bothclean",
                "T2d4_mixed_cells"]
    missing = [x for x in declared if x not in RAN]
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    print(f"CONTROL MANIFEST: declared {len(declared)}, ran {len(RAN)}, "
          f"missing {missing}")
    assert not missing
    ck("final")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
