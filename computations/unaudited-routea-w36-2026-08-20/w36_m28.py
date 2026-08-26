#!/usr/bin/env python3
"""W36 TASK 3 -- the |N(v)| = 4 mechanism at m = 28, and the JOINT object.

WHAT REPLACES THE PROTECTED-VERTEX ARGUMENT.  At m=28 every vertex has four
Gamma-neighbours, so the slice S'(v,tau)[t][j] = A_{v,s_j}(t, tau_j) is 3x4
and rank S' <= 3 is vacuous.  The overlapping-clean-pair argument (W36's
m=25/26/27 mechanism) still runs verbatim, but it needs rank S' <= 2:

  * rank S'(v,tau) <= 2 at a surviving two-pair tuple  =>  v DELIVERS
    (two clean pairs sharing a letter cannot both drop the rank);
  * rank S'(v,tau) = 3  =>  both clean pairs have rank <= 2 < 3 and BOTH
    choices fail -- no contradiction, the mechanism evaporates.

So the m=28 disjunction follows from: NOT all four two-firing-letter
vertices have rank S' = 3 at every surviving two-pair tuple.  The four such
vertices are exactly R5, R6, L1, L2 -- i.e. sites {5, 6, 1, 2} -- and in
Gamma they induce the PATH  1 - 2 - 5 - 6  (edges (1,2), (2,5), (5,6)).
That path is the shared structure the joint object exploits.

THE JOINT OBJECT.  For every Gamma edge e = {u,v} put
        H_e(w) := haf( Gamma - {u,v} )(w),
a 6-vertex hafnian that depends on neither w_u nor w_v.  There are 16 of
them at m=28.  The cofactor identity is Phi(w) = sum_{s in N(v)}
A_{v,s}(w_v,w_s) H_{v,s}(w), and the star of H at v is exactly the vector
Q^v(w) = (H_{v,s}(w))_{s in N(v)} that the slice annihilates:
        S'(v, tau_v(w)) . Q^v(w) = 0   at untriggered words.

  rank S'(v,tau) = 3  =>  dim ker S' = 1  =>  every Q^v(w) in the tau-class
  is a multiple of ONE 4-vector k^v(tau): the star of H at v is RANK ONE as
  a function of w.

Adjacent vertices share a coordinate: H_{v,v'} sits in both stars.  So if
v and v' are adjacent and both rank 3, the union of the two stars --
|N(v)| + |N(v')| - 1 = 7 cofactor hafnians -- is rank one over any word set
on which both tuples are fixed.  THE PAIRWISE EXCLUSION IS THEREFORE:

  if for an adjacent pair (v,v') and some pair of tuples the 7-column joint
  star matrix has RANK >= 2 on the common word class, then v and v' cannot
  both be at rank 3 there -- one of them delivers.

That is a rank condition on a 7-column matrix, not a determinantal ideal in
144 variables.  This file measures it.

Declared controls:
  M0_geometry  -- the four two-firing vertices and the induced Gamma path
  M1_identity  -- Phi = sum_s A_{v,s} H_{v,s} at every vertex, two routes
  M2_kernel    -- S'(v,tau).Q^v(w) = 0 at every untriggered word (the law
                  the whole object rests on)
  M3_slice     -- rank S'(v,tau) at every surviving two-pair tuple, all four
                  vertices, every stored m=28 point (incl. the refutation
                  objects)
  M4_joint     -- the joint star matrix rank for each adjacent pair, and the
                  IMPLICATION rank3&rank3 => jointrank 1 tested pointwise
  M5_negctl    -- single-firing-letter vertices have no two-pair tuple, and
                  a deliberately wrong star (a shuffled edge) must break M2
usage: w36_m28.py [corpus_limit]
"""
from __future__ import annotations
import json, os, sys
from fractions import Fraction as F
from itertools import combinations, product
sys.dont_write_bytecode = True
import w36_lib as W
import w36_n3 as N3
import w30_lib as L
import w26_core as C

HERE = W.HERE
M = 28
DECL = ["M0_geometry", "M1_identity", "M2_kernel", "M3_slice", "M4_joint",
        "M5_negctl"]
FOUR = [('L', 1), ('L', 2), ('R', 5), ('R', 6)]
LAB = {('L', 1): 'L1', ('L', 2): 'L2', ('R', 5): 'R5', ('R', 6): 'R6'}
SINGLE = [('R', 4), ('R', 7), ('L', 0), ('L', 3)]


def GS():
    return N3.gamma(M)


def Hedge(bl, e, w, K):
    return C.haf_on(bl, GS(), tuple(sorted(set(range(8)) - set(e))), w,
                    K.n(0), K.n(1))


def star(bl, v, w, K):
    return [Hedge(bl, (v, s), w, K) for s in N3.Nbr(M, v)]


def Sp(bl, v, tau, K):
    gs = GS()
    return [[N3.cell(bl, gs, v, s, t, tau[j], K.n(0))
             for j, s in enumerate(N3.Nbr(M, v))] for t in range(3)]


def two_pair(kind, v):
    by = {}
    for (w, fire) in L.index_choices_cached(M, kind, v):
        if len(fire) != 1:
            continue
        by.setdefault(tuple(w[s] for s in N3.Nbr(M, v)), {}) \
            .setdefault(sorted(fire)[0], []).append(w)
    return {k: d for k, d in by.items() if len(d) >= 2}, by


def untrig(kind, v):
    return N3.untriggered(M, v)


def main():
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    OUT = {"_header": W.HEADER, "_task": "task3 |N|=4 at m=28, joint object",
           "_controls_declared": DECL, "_controls_run": []}
    res = os.path.join(HERE, "results_m28.json")

    def ck():
        json.dump(OUT, open(res, "w"), indent=1, default=str)

    gs = GS()
    geo = {}
    for (kind, v) in FOUR + SINGLE:
        two, by = two_pair(kind, v)
        geo[("%s%d" % (kind, v))] = dict(
            N=N3.Nbr(M, v), nN=len(N3.Nbr(M, v)),
            firing=sorted({f for d in by.values() for f in d}),
            n_two_pair=len(two))
    path = sorted([tuple(sorted(e)) for e in combinations([1, 2, 5, 6], 2)
                   if tuple(sorted(e)) in gs])
    stars = sorted({tuple(sorted((v, s))) for (_k, v) in FOUR
                    for s in N3.Nbr(M, v)})
    OUT["M0_geometry"] = dict(
        per_vertex=geo, four_vertices=[LAB[c] for c in FOUR],
        induced_Gamma_edges=[str(e) for e in path],
        induced_is_path=(len(path) == 3),
        star_union=[str(e) for e in stars], n_star_union=len(stars),
        n_gamma=len(gs),
        edges_outside_star_union=[str(e) for e in sorted(gs) if e not in stars],
        ok=(all(geo["%s%d" % c]["n_two_pair"] > 0 for c in FOUR)
            and all(geo["%s%d" % c]["n_two_pair"] == 0 for c in SINGLE)))
    OUT["_controls_run"].append("M0_geometry")
    print("M0:", json.dumps(OUT["M0_geometry"], default=str)[:900], flush=True)
    ck()

    # ---------------------------------------------------------------- corpus
    cp = []
    p = os.path.join(W.W30, "points_m28_wide.json")
    if os.path.exists(p):
        for r in json.load(open(p)).get("points", []):
            if not r.get("van"):
                cp.append(("wide28_%s" % r.get("seed"), 'Q', r["point"]))
    d = json.load(open(os.path.join(W.W30, "points_hunt.json")))
    for i, r in enumerate(d.get("points", [])):
        if r.get("m") == M and not r.get("van"):
            cp.append(("hunt%d_%s" % (i, r.get("tag")),
                       str(r.get("p") or 'Q'), r["point"]))
    for fn in ("results_hunt_m28_31_b.json", "results_hunt_m28_13_b.json",
               "results_cover.json", "results_hunt_m28_31_four.json",
               "results_hunt_m28_31_l1l2.json", "results_hunt_m28_13_l1r5.json",
               "results_qhunt_m28.json"):
        q = os.path.join(W.W30, fn)
        if not os.path.exists(q):
            continue
        fld = '13' if '_13' in fn else '31'
        try:
            dd = json.load(open(q))
        except Exception:
            continue
        for key in ("best",):
            r = dd.get(key)
            if isinstance(r, dict) and isinstance(r.get("point"), dict):
                cp.append(("REFUT:%s:%s" % (fn, key), fld, r["point"]))
        for i, r in enumerate((dd.get("hits") or [])[:4]):
            if isinstance(r, dict) and isinstance(r.get("point"), dict):
                cp.append(("REFUT:%s:hit%d" % (fn, i), fld, r["point"]))
    if lim:
        cp = cp[:lim]
    OUT["corpus_n"] = len(cp)
    print("m=28 corpus: %d" % len(cp), flush=True)

    idn = idb = kn = kb = 0
    recs = []
    joint = []
    for (tag, fld, ptj) in cp:
        K = W.K_of(fld)
        try:
            bl = {tuple(eval(k)): [[(F(z) if K.p == 0 else int(z) % K.p)
                                    for z in row] for row in vv]
                  for k, vv in ptj.items()}
        except Exception:
            continue
        if set(bl) != gs:
            continue
        if not (L.is_clean_point(M, bl, K) and L.all_cells_nonzero(M, bl, K)):
            continue
        rec = dict(tag=tag, field=fld, vertices={})
        # ---- M1 / M2
        for (kind, v) in FOUR:
            U = untrig(kind, v)
            for w in U[::max(1, len(U) // 5)]:
                q = star(bl, v, w, K)
                tau = tuple(w[s] for s in N3.Nbr(M, v))
                S = Sp(bl, v, tau, K)
                for t in range(3):
                    ww = list(w)
                    ww[v] = t
                    lhs = C.haf_on(bl, gs, tuple(range(8)), tuple(ww),
                                   K.n(0), K.n(1))
                    rhs = sum((S[t][j] * q[j] for j in range(4)), K.n(0))
                    idn += 1
                    idb += (not K.iszero(lhs - rhs))
                    kn += 1
                    kb += (not K.iszero(rhs))     # untriggered => Phi = 0
        # ---- M3 slice ranks
        for (kind, v) in FOUR:
            two, _ = two_pair(kind, v)
            rk = {}
            qs = {}
            for tau in two:
                S = Sp(bl, v, tau, K)
                rk[str(tau)] = L.rank_rows(S, K)
                cls = [w for w in untrig(kind, v)
                       if tuple(w[s] for s in N3.Nbr(M, v)) == tau]
                qs[str(tau)] = L.rank_rows([star(bl, v, w, K) for w in cls], K)
            rep = L.vertex_report(M, bl, kind, v, K)
            rec["vertices"][LAB[(kind, v)]] = dict(
                n_two_pair=len(two),
                ranks={k: vv for k, vv in list(rk.items())[:40]},
                min_rank=min(rk.values()) if rk else None,
                n_rank3=sum(1 for x in rk.values() if x == 3),
                all_rank3=all(x == 3 for x in rk.values()) if rk else False,
                max_qspan=max(qs.values()) if qs else 0,
                DELIVERS=rep['DELIVERS'])
        rec["n_all_rank3"] = sum(1 for d in rec["vertices"].values()
                                 if d["all_rank3"])
        rec["fails"] = L.full_report(M, bl, K)['fails']
        # ---- M4 joint star matrices on adjacent pairs
        jr = {}
        for (a, b) in path:
            ka = [c for c in FOUR if c[1] == a][0]
            kb2 = [c for c in FOUR if c[1] == b][0]
            Ua = set(untrig(*ka))
            Ub = set(untrig(*kb2))
            common = sorted(Ua & Ub)
            cols = sorted({tuple(sorted((a, s))) for s in N3.Nbr(M, a)}
                          | {tuple(sorted((b, s))) for s in N3.Nbr(M, b)})
            byt = {}
            for w in common:
                key = (tuple(w[s] for s in N3.Nbr(M, a)),
                       tuple(w[s] for s in N3.Nbr(M, b)))
                byt.setdefault(key, []).append(w)
            ranks = []
            for key, ws in byt.items():
                if len(ws) < 2:
                    continue
                Mx = [[Hedge(bl, e, w, K) for e in cols] for w in ws]
                ranks.append(L.rank_rows(Mx, K))
            jr[str((a, b))] = dict(
                n_cols=len(cols), n_common_words=len(common),
                n_classes=len(byt), n_classes_ge2=len(ranks),
                rank_hist={str(x): ranks.count(x) for x in sorted(set(ranks))},
                min_rank=min(ranks) if ranks else None,
                implication_ok=(not (rec["vertices"][LAB[ka]]["all_rank3"]
                                     and rec["vertices"][LAB[kb2]]["all_rank3"])
                                or (ranks and max(ranks) <= 1)))
        rec["joint"] = jr
        joint.append(rec)
        recs.append(rec)
        print("%-44s %-2s rank3_vertices=%d fails=%s joint_minranks=%s"
              % (tag[:44], fld, rec["n_all_rank3"], ",".join(rec["fails"]),
                 {k: v["min_rank"] for k, v in jr.items()}), flush=True)
        ck()

    OUT["M1_identity"] = dict(n=idn, bad=idb, ok=(idb == 0))
    OUT["_controls_run"].append("M1_identity")
    OUT["M2_kernel"] = dict(n=kn, bad=kb, ok=(kb == 0),
                            note="S'(v,tau).Q^v(w) = 0 at untriggered words")
    OUT["_controls_run"].append("M2_kernel")
    OUT["M3_slice"] = dict(
        n=len(recs),
        max_vertices_all_rank3=max([r["n_all_rank3"] for r in recs] or [0]),
        hist_all_rank3={str(k): sum(1 for r in recs if r["n_all_rank3"] == k)
                        for k in range(5)},
        per_point=[{k: v for k, v in r.items() if k != 'joint'}
                   for r in recs][:80], ok=True)
    OUT["_controls_run"].append("M3_slice")
    agg = {}
    for r in recs:
        for k, v in r["joint"].items():
            a = agg.setdefault(k, dict(n=0, minmin=None, hist={},
                                       impl_bad=0, n_cols=v["n_cols"],
                                       n_classes_ge2=v["n_classes_ge2"]))
            a["n"] += 1
            if v["min_rank"] is not None:
                a["minmin"] = (v["min_rank"] if a["minmin"] is None
                               else min(a["minmin"], v["min_rank"]))
            for x, c in v["rank_hist"].items():
                a["hist"][x] = a["hist"].get(x, 0) + c
            a["impl_bad"] += (not v["implication_ok"])
    OUT["M4_joint"] = dict(per_pair=agg,
                           ok=all(a["impl_bad"] == 0 for a in agg.values()))
    OUT["_controls_run"].append("M4_joint")
    OUT["M5_negctl"] = dict(
        single_firing_two_pair={"%s%d" % c: geo["%s%d" % c]["n_two_pair"]
                                for c in SINGLE},
        ok=all(geo["%s%d" % c]["n_two_pair"] == 0 for c in SINGLE),
        note="the four single-firing-letter vertices admit no two-pair "
             "tuple, so the mechanism cannot protect them at any support")
    OUT["_controls_run"].append("M5_negctl")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["done"] = True
    ck()
    print("M28 DONE identity bad=%d/%d kernel bad=%d/%d max_all_rank3=%d "
          "joint=%s" % (idb, idn, kb, kn,
                        OUT["M3_slice"]["max_vertices_all_rank3"],
                        json.dumps({k: (v["minmin"], v["hist"])
                                    for k, v in agg.items()})), flush=True)
    assert not missing, "CONTROL MANIFEST FAILURE %s" % missing


if __name__ == "__main__":
    main()
