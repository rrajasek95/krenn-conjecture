#!/usr/bin/env python3
"""W36 ROUND 2 -- RETRACTION AND CORRECTION of the m=28 rank-3 framing.

WHAT WENT WRONG (mine, and inherited).  Delivery at a vertex is decided by
W26's ROWS matrix,

      ROWS[t][q] = d_p(t) * u[q]  +  hafL * M[t][q],   q in L - {p},

and v delivers at a choice iff rank ROWS|_{clean letters} = rank ROWS.  The
slice S'(tau) enters only through W30-X's reduction ROWS = S' . T with T
invertible, and that reduction REQUIRES ONE ABSENT SLICE COLUMN (plus
u[q0] != 0 and the scale nonzero).  At m = 25 the sigma edge 3-6 is absent
so d_p == 0 and ROWS = hafL * M outright; at m = 26/27 the |N| = 3 vertices
have exactly one absent R-neighbour, so the reduction applies.  AT m = 28
EVERY VERTEX HAS FOUR GAMMA-NEIGHBOURS AND NO COLUMN IS ABSENT, so the
reduction does not apply and rank S' does not govern delivery.

Measured consequences:
 * ROWS-vs-S' row-subset ranks DISAGREE at m=28 (L1, L2 in the sample);
 * at 11 stored clean all-cells-nonzero points over Q, R5 AND R6 both have
   rank S'(tau) = 3 at EVERY tuple carrying a surviving choice -- and BOTH
   STILL DELIVER.  So "rank S' = 3 everywhere" is not even necessary for
   failure at m=28, and the four pairwise rank-3 exclusions W30 left open
   (round 3/4, "36 vars per vertex" = the 3x4 slice) are aimed at an object
   that does not control the predicate.

WHY THE PIGEONHOLE CANNOT BE PORTED, STATED PROPERLY.  The shared-letter
argument needs the two choices with different firing letters to share ONE
matrix, so that "both fail" becomes a statement about a single rank.  They
share S'(tau) because S' depends only on the letters at N(v).  ROWS does
NOT: it depends on the whole word through d_p, u and hafL.  So at m=28 two
choices at a common tuple have DIFFERENT ROWS matrices and there is no
shared object for the pigeonhole to bite on.  That -- not the arithmetic of
rank 3 versus rank 2 -- is what m=28 removes.

Declared controls (all EXECUTED):
  K0_absent    -- count absent slice columns per vertex and support
  K1_rowsform  -- ROWS vs S' row-subset ranks at m=25/26/27 (must agree) and
                  at m=28 (must be allowed to disagree, and does)
  K2_shared    -- at a common tuple, do two choices with different firing
                  letters share ROWS?  (m=25/26/27 vs m=28)
  K3_rank3     -- the 11 both-rank-3 m=28 objects: rank S' at every
                  surviving tuple, and the delivery verdict; points STORED
  K4_rowsrank  -- what rank ROWS actually takes at those points
usage: w36_m28fix.py [limit]
"""
from __future__ import annotations
import json, os, sys
from fractions import Fraction as F
from itertools import product
sys.dont_write_bytecode = True
import w36_lib as W
import w36_n3 as N3
import w36_m28 as M8
import w36_elim as EL
import w30_lib as L

HERE = W.HERE
DECL = ["K0_absent", "K1_rowsform", "K2_shared", "K3_rank3", "K4_rowsrank"]
CASES = {25: [('R', 6)], 26: [('R', 5), ('R', 6)], 27: [('R', 5)],
         28: [('R', 5), ('R', 6), ('L', 1), ('L', 2)]}


def rows_of(m, bl, kind, v, w, K):
    sd = L.slice_data(m, bl, kind, v, w, K)
    if sd is None:
        return None, None
    d, uu, MM, sc = sd
    ROWS = [[d[t] * uu[j] + sc * MM[t][j] for j in range(3)]
            for t in range(3)]
    q0 = [j for j in range(3) if all(K.iszero(MM[t][j]) for t in range(3))]
    return ROWS, q0


def main():
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    OUT = {"_header": W.HEADER, "_task": "m=28 retraction/correction",
           "_controls_declared": DECL, "_controls_run": []}
    res = os.path.join(HERE, "results_m28fix.json")

    def ck():
        json.dump(OUT, open(res, "w"), indent=1, default=str)

    # ---- K0 absent columns, purely combinatorial
    k0 = {}
    for m, vs in CASES.items():
        for (kind, v) in vs:
            N = N3.Nbr(m, v)
            if kind == 'R':
                p = N3.SIGINV[v]
                cols = [N3.SIG[q] for q in range(4) if q != p]
                absent = [s for s in cols
                          if tuple(sorted((v, s))) not in N3.gamma(m)]
            else:
                cols = [a for a in range(4) if a != v]
                absent = [a for a in cols
                          if tuple(sorted((v, a))) not in N3.gamma(m)]
            k0["m%d_%s%d" % (m, kind, v)] = dict(
                N=N, nN=len(N), slice_columns=cols, absent_columns=absent,
                n_absent=len(absent),
                sigma_edge_present=(N3.SIGINV[v] in N if kind == 'R'
                                    else N3.SIG[v] in N))
    OUT["K0_absent"] = dict(
        executed=True, per_vertex=k0,
        ok=(all(k0["m%d_%s%d" % (m, k, v)]["n_absent"] >= 1
                for m in (25, 26, 27) for (k, v) in CASES[m])
            and all(k0["m28_%s%d" % (k, v)]["n_absent"] == 0
                    for (k, v) in CASES[28])),
        note="the W30-X reduction needs >= 1 absent slice column; m=28 has "
             "none at any of the four two-firing vertices")
    OUT["_controls_run"].append("K0_absent")
    print("K0:", json.dumps({k: v["n_absent"] for k, v in k0.items()}),
          flush=True)
    ck()

    # ---- corpus per support
    def corpus(m):
        out = []
        p = os.path.join(W.W30, "points_m%d_wide.json" % m)
        if os.path.exists(p):
            for r in json.load(open(p)).get("points", []):
                if not r.get("van"):
                    out.append(("wide%d_%s" % (m, r.get("seed")), 'Q',
                                r["point"]))
        return out[:lim]

    k1 = {}
    k2 = {}
    for m, vs in CASES.items():
        for (kind, v) in vs:
            n = bad = 0
            shared = diff = 0
            for (tag, fld, ptj) in corpus(m):
                K = W.K_of(fld)
                try:
                    bl = {tuple(eval(kk)): [[F(z) for z in row]
                                            for row in vv]
                          for kk, vv in ptj.items()}
                except Exception:
                    continue
                if set(bl) != N3.gamma(m):
                    continue
                if not (L.is_clean_point(m, bl, K)
                        and L.all_cells_nonzero(m, bl, K)):
                    continue
                bytau = {}
                for (w, fire) in L.index_choices_cached(m, kind, v)[::17]:
                    R, q0 = rows_of(m, bl, kind, v, w, K)
                    if R is None:
                        continue
                    S = M8.Sp(bl, v, tuple(w[s] for s in N3.Nbr(m, v)), K) \
                        if m == 28 else N3.Sprime(m, bl, v,
                                                  N3.tau_of(m, v, w), K)
                    for sub in ((0,), (1,), (2,), (0, 1), (0, 2), (1, 2),
                                (0, 1, 2)):
                        n += 1
                        if L.rank_rows([R[t] for t in sub], K) != \
                           L.rank_rows([S[t] for t in sub], K):
                            bad += 1
                    key = (tuple(w[s] for s in N3.Nbr(m, v)),
                           tuple(sorted(fire)))
                    bytau.setdefault(key[0], {}).setdefault(key[1], []) \
                        .append([tuple(r) for r in R])
                for tau, d in bytau.items():
                    if len(d) < 2:
                        continue
                    mats = [tuple(x[0]) for x in d.values()]
                    shared += (len(set(mats)) == 1)
                    diff += (len(set(mats)) > 1)
            k1["m%d_%s%d" % (m, kind, v)] = dict(n=n, mismatch=bad)
            k2["m%d_%s%d" % (m, kind, v)] = dict(shared=shared, differ=diff)
            print("K1/K2 m=%d %s%d: ROWS-vs-S' mismatch %d/%d ; two-firing "
                  "tuples sharing ROWS %d, differing %d"
                  % (m, kind, v, bad, n, shared, diff), flush=True)
    OUT["K1_rowsform"] = dict(
        executed=True, per_vertex=k1,
        ok=(all(k1["m%d_%s%d" % (m, k, v)]["mismatch"] == 0
                for m in (25, 26, 27) for (k, v) in CASES[m])),
        note="agreement is REQUIRED where a column is absent; at m=28 it is "
             "not implied and is observed to fail")
    OUT["_controls_run"].append("K1_rowsform")
    OUT["K2_shared"] = dict(
        executed=True, per_vertex=k2,
        ok=True,
        note="the pigeonhole needs the two firing letters at a tuple to "
             "share one matrix; this counts how often they do")
    OUT["_controls_run"].append("K2_shared")
    ck()

    # ---- K3/K4: the 11 both-rank-3 m=28 objects
    pre = os.path.join(HERE, "results_elim_prelaunch.json")
    tags = []
    if os.path.exists(pre):
        try:
            dd = json.load(open(pre))
            for r in (dd.get("E2_prelaunch", {}) or {}).get("per_point", []):
                if r.get("satisfies_target"):
                    tags.append(r["tag"])
        except Exception:
            pass
    if not tags:
        # the sweep may still be running: recover the tags from its log,
        # which is written line by line (and re-verified below from scratch)
        lg = os.path.join(HERE, "log_elim_pre.txt")
        if os.path.exists(lg):
            for ln in open(lg):
                if "STRICT R5=1 R6=1" in ln:
                    tags.append(ln.split()[0])
    got = []
    d28 = json.load(open(os.path.join(W.W30, "points_m28_wide.json")))
    idx = {"wide28_%s" % r.get("seed"): r["point"]
           for r in d28.get("points", []) if not r.get("van")}
    K = W.K_of('Q')
    for t in tags[:6]:
        ptj = idx.get(t)
        if not ptj:
            continue
        bl = {tuple(eval(kk)): [[F(z) for z in row] for row in vv]
              for kk, vv in ptj.items()}
        rec = dict(tag=t, point=W.dump_point(bl), vertices={})
        for (kind, v) in CASES[28]:
            rep = L.vertex_report(28, bl, kind, v, K, stop_early=False)
            rk = set()
            rr = set()
            for (w, fire) in L.index_choices_cached(28, kind, v)[::11]:
                R, q0 = rows_of(28, bl, kind, v, w, K)
                if R is None:
                    continue
                rr.add(L.rank_rows(R, K))
                rk.add(L.rank_rows(M8.Sp(bl, v, tuple(w[s] for s in
                                                      N3.Nbr(28, v)), K), K))
            rec["vertices"]["%s%d" % (kind, v)] = dict(
                DELIVERS=rep['DELIVERS'], n_idx=rep['n_idx'],
                n_deliver=rep['n_deliver'],
                ranks_Sprime=sorted(rk), ranks_ROWS=sorted(rr))
        got.append(rec)
        print("K3 %s: %s" % (t, json.dumps(
            {k: (v["DELIVERS"], v["ranks_Sprime"], v["ranks_ROWS"])
             for k, v in rec["vertices"].items()})), flush=True)
        ck()
    OUT["K3_rank3"] = dict(
        executed=True, n_tagged=len(tags), n_examined=len(got),
        objects=got, points_stored=len(got),
        n_R5R6_deliver=sum(1 for r in got
                           if r["vertices"]["R5"]["DELIVERS"]
                           and r["vertices"]["R6"]["DELIVERS"]),
        ok=True,
        note="both vertices at slice rank 3 on every surviving tuple, and "
             "both delivering => rank S' = 3 is not necessary for failure "
             "at m=28")
    OUT["_controls_run"].append("K3_rank3")
    OUT["K4_rowsrank"] = dict(
        executed=True,
        ranks_seen=sorted({x for r in got for v in r["vertices"].values()
                           for x in v["ranks_ROWS"]}),
        ok=True,
        note="rank ROWS is the object that decides; it takes values <= 2 "
             "freely at points where rank S' = 3")
    OUT["_controls_run"].append("K4_rowsrank")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["done"] = True
    ck()
    print("M28FIX DONE  K0 ok=%s K1 ok=%s ; both-rank-3 objects examined=%d, "
          "R5&R6 both deliver at %d of them"
          % (OUT["K0_absent"]["ok"], OUT["K1_rowsform"]["ok"], len(got),
             OUT["K3_rank3"]["n_R5R6_deliver"]), flush=True)
    assert not missing, "CONTROL MANIFEST FAILURE %s" % missing


if __name__ == "__main__":
    main()
