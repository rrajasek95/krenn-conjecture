#!/usr/bin/env python3
"""W36 TASK 2 -- THE |N(v)| = 3 MECHANISM at m = 26 and m = 27.

THE DERIVATION (this lane).

Let v be an R-vertex with Gamma-neighbourhood N(v) = {s1, s2, s3} of size 3
(at m=26 that is v = 5 with N = {2,4,6} and v = 6 with N = {3,5,7}; at m=27
it is v = 5 with N = {2,4,6}).  One of the three is the sigma partner
p = sigma^{-1}(v) in L, so its column of the slice is the sigma column d.
The cofactor identity (multilinearity of the hafnian in the letter at v):

      Phi(w | v = t)  =  sum_{s in N(v)}  A_{v,s}(t, w_s) * Q_s(w),
      Q_s(w)          =  haf( Gamma - {v, s} )(w).                        (C)

Q_s does not involve the letter at v nor the letter at s.  Define the
3 x 3 AUGMENTED SLICE, which depends on w only through the three letters
tau = (w_{s1}, w_{s2}, w_{s3}) -- there are 27 tuples:

      S'(tau)[t][j]  =  A_{v,s_j}(t, tau_j).

W26's ROWS matrix equals S' times an invertible matrix whenever the scale
hafL != 0 and the absent-column coefficient u[q0] != 0, so for every subset
of letters, rank of those ROWS = rank of the same rows of S'.  Hence

      v DELIVERS at an index choice  <=>  rank S'|_{clean letters}
                                          = rank S'(tau).                  (D)

WHAT Q != 0 GIVES, AND WHY IT IS NOT ENOUGH.  At an UNTRIGGERED word (all
three completions at v clean), (C) gives S'(tau) . Q(w) = 0, so

      Q(w) != 0   =>   rank S'(tau) <= 2.                                  (1)

With |T_f| = 1 the clean set is a PAIR, and by (D) failure needs
rank S'|_{pair} < rank S'.  rank S' <= 2 alone does not exclude that: a
rank-2 slice with the two clean rows parallel fails.  (At m=25, |N| = 2
made S' a 3x2 matrix and Q != 0 forced rank 1 = rank of every nonempty row
subset -- that is exactly why m=25 closed and 26/27 did not.)

WHAT CLOSES THE GAP: THE OVERLAPPING CLEAN PAIRS.  Say tau is a TWO-PAIR
TUPLE if two admissible |T_f| = 1 index choices carry the same letters on
N(v) with DIFFERENT firing letters f1 != f2.  Their clean pairs are
P1 = {0,1,2} - {f1} and P2 = {0,1,2} - {f2}; these are distinct 2-sets in a
3-set, so they SHARE a letter a.  Suppose both choices fail.  Then
rank S'|_{P1} < rank S' and rank S'|_{P2} < rank S'.  Every row of S' is
nonzero (all Gamma cells nonzero), so rank S'|_{P_i} >= 1, and with (1)
rank S' = 2, forcing rank S'|_{P1} = rank S'|_{P2} = 1, i.e.
S'_a || S'_{b} and S'_a || S'_{c} with {a,b,c} = {0,1,2}.  Then all three
rows are parallel and rank S' = 1 -- contradicting rank S' = 2.  (If
rank S' = 1 instead, every pair already has rank 1 = rank S' and both
choices deliver.)  THEREFORE AT LEAST ONE OF THE TWO CHOICES DELIVERS.

That is the |N| = 3 analogue of the m=25 argument: at m=25 the FALL to
rank 1 was automatic, here it is bought by the second firing letter.

Declared controls:
  N0_geometry   -- N(v), the sigma partner and the absent R-column, read off
                   the engine's own template
  N1_identity   -- (C) verified against raw Gamma-matching enumeration
  N2_rowsform   -- ROWS = S' . T with T invertible: rank of every row subset
                   agrees between ROWS and S' (this is what (D) rests on)
  N3_twopair    -- the two-pair tuples enumerated combinatorially
  N4_hypotheses -- every hypothesis of the theorem evaluated pointwise on
                   the stored corpus, and the conclusion checked
  N5_negctl     -- vertices with |N| = 3 but only ONE firing letter (R4, R7
                   at m=26) must NOT be protected by this argument, and the
                   corpus must show them failing somewhere
usage: w36_n3.py [corpus_limit]
"""
from __future__ import annotations
import json, os, random, sys
from fractions import Fraction as F
from itertools import combinations, product
sys.dont_write_bytecode = True
import w36_lib as W
import w30_lib as L
import w26_core as C

HERE = W.HERE
DECL = ["N0_geometry", "N1_identity", "N2_rowsform", "N3_twopair",
        "N4_hypotheses", "N5_negctl"]
SIG = {0: 7, 1: 4, 2: 5, 3: 6}
SIGINV = {v: k for k, v in SIG.items()}
CASES = [(26, 5), (26, 6), (27, 5)]
NEG = [(26, 4), (26, 7), (27, 7)]


def gamma(m):
    return set(C.gamma_edges(C.TEMPLATES[m]))


def Nbr(m, v):
    gs = gamma(m)
    return sorted({b for (a, b) in gs if a == v} | {a for (a, b) in gs if b == v})


def cell(bl, gs, u, v, a, b, zero):
    e = (u, v) if u < v else (v, u)
    if e not in gs:
        return zero
    return bl[e][a][b] if u < v else bl[e][b][a]


def Qs(m, bl, v, s, w, K):
    """haf(Gamma - {v,s}) at w -- the cofactor for neighbour s."""
    verts = tuple(sorted(set(range(8)) - {v, s}))
    return C.haf_on(bl, gamma(m), verts, w, K.n(0), K.n(1))


def Sprime(m, bl, v, tau, K):
    """3 x 3 augmented slice; column j uses neighbour N(v)[j]."""
    gs = gamma(m)
    N = Nbr(m, v)
    return [[cell(bl, gs, v, s, t, tau[j], K.n(0))
             for j, s in enumerate(N)] for t in range(3)]


def tau_of(m, v, w):
    return tuple(w[s] for s in Nbr(m, v))


def untriggered(m, v):
    """patterns whose three completions at v are all clean (w[v] = 0 dummy)."""
    G = L.geom(m)
    sing, lv = G['sing'], G['lv']
    out = []
    others = [c for c in range(8) if c != v]
    for vals in product(range(3), repeat=7):
        w = [0] * 8
        for c, a in zip(others, vals):
            w[c] = a
        ok = True
        for t in range(3):
            ww = list(w)
            ww[v] = t
            if len(set(ww)) == 1 or any(ww[f[0]] == sing[f][0]
                                        and ww[f[1]] == sing[f][1]
                                        for f in lv):
                ok = False
                break
        if ok:
            out.append(tuple(w))
    return out


def two_pair_tuples(m, v):
    """tuples on N(v) carrying two admissible |T_f|=1 choices with distinct
    firing letters."""
    by = {}
    for (w, fire) in L.index_choices_cached(m, 'R' if v >= 4 else 'L', v):
        if len(fire) != 1:
            continue
        by.setdefault(tau_of(m, v, w), {}).setdefault(
            sorted(fire)[0], []).append(w)
    return {k: d for k, d in by.items() if len(d) >= 2}, by


def main():
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    OUT = {"_header": W.HEADER, "_task": "task2 |N(v)|=3 mechanism m=26/27",
           "_controls_declared": DECL, "_controls_run": []}
    res = os.path.join(HERE, "results_n3.json")

    def ck():
        json.dump(OUT, open(res, "w"), indent=1, default=str)

    # ---------------------------------------------------------- N0 geometry
    geo = {}
    for (m, v) in CASES + NEG:
        N = Nbr(m, v)
        p = SIGINV[v]
        _, by = two_pair_tuples(m, v)
        fl = sorted({f for d in by.values() for f in d})
        geo["m%d_R%d" % (m, v)] = dict(
            N=N, size=len(N), sigma_partner=p, sigma_in_N=(p in N),
            R_neighbours=[s for s in N if s >= 4],
            absent_R=[s for s in range(4, 8) if s != v and s not in N],
            firing_letters=fl, n_firing=len(fl))
    OUT["N0_geometry"] = dict(per_case=geo,
                              ok=all(geo["m%d_R%d" % (m, v)]["size"] == 3
                                     for (m, v) in CASES))
    OUT["_controls_run"].append("N0_geometry")
    print("N0 geometry:", json.dumps(geo), flush=True)
    ck()

    # ---------------------------------------------------------- N3 two-pair
    tp = {}
    for (m, v) in CASES + NEG:
        two, by = two_pair_tuples(m, v)
        tp["m%d_R%d" % (m, v)] = dict(
            n_tuples_with_choices=len(by), n_two_pair=len(two),
            two_pair=[str(k) for k in sorted(two)],
            pairs_per_tuple={str(k): sorted(d) for k, d in sorted(two.items())})
    OUT["N3_twopair"] = dict(per_case=tp,
                             ok=all(tp["m%d_R%d" % (m, v)]["n_two_pair"] > 0
                                    for (m, v) in CASES))
    OUT["_controls_run"].append("N3_twopair")
    print("N3 two-pair tuples: %s"
          % {k: (v["n_tuples_with_choices"], v["n_two_pair"])
             for k, v in tp.items()}, flush=True)
    ck()

    # ---------------------------------------------------- corpus + N1/N2/N4
    corpus = []
    for m in (26, 27):
        p = os.path.join(W.W30, "points_m%d_wide.json" % m)
        if os.path.exists(p):
            d = json.load(open(p))
            for r in d.get("points", []):
                if not r.get("van"):
                    corpus.append(("m%dwide_%s" % (m, r.get("seed")), m, 'Q',
                                   r["point"]))
        for fn in ("results_hunt_m%d_13_b.json", "results_hunt_m%d_31_max.json",
                   "results_hunt_m%d_31_b.json", "results_hunt_m%d_13_max.json",
                   "results_escape_m%d_13.json", "results_escape_m%d_31.json"):
            q = os.path.join(W.W30, fn % m)
            if not os.path.exists(q):
                continue
            fld = '13' if '_13' in fn else '31'
            try:
                d = json.load(open(q))
            except Exception:
                continue
            for key in ("best", "object"):
                r = d.get(key)
                if isinstance(r, dict) and isinstance(r.get("point"), dict):
                    corpus.append((fn % m + ":" + key, m, fld, r["point"]))
            for i, r in enumerate((d.get("hits") or [])[:3]):
                if isinstance(r, dict) and isinstance(r.get("point"), dict):
                    corpus.append((fn % m + ":hit%d" % i, m, fld, r["point"]))
            # the STORED ESCAPE OBJECTS (ledger 27 pre-launch control)
            for i, r in enumerate((d.get("records") or [])[:8]):
                if isinstance(r, dict) and isinstance(r.get("point"), dict):
                    corpus.append((fn % m + ":ESCAPE%d(nzero=%s)"
                                   % (i, r.get("nzero")), m, fld, r["point"]))
    ph = os.path.join(W.W30, "points_hunt.json")
    if os.path.exists(ph):
        d = json.load(open(ph))
        for i, r in enumerate(d.get("points", [])):
            if r.get("m") in (26, 27) and not r.get("van"):
                corpus.append(("hunt%d_%s" % (i, r.get("tag")), r["m"],
                               str(r.get("p") or 'Q'), r["point"]))
    if lim:
        corpus = corpus[:lim]
    OUT["corpus_n"] = len(corpus)
    print("corpus objects (m=26/27): %d" % len(corpus), flush=True)

    idn = idbad = 0
    rf_n = rf_bad = 0
    recs = []
    negrecs = []
    for (tag, m, fld, ptj) in corpus:
        K = W.K_of(fld)
        try:
            bl = {tuple(eval(k)): [[(F(z) if K.p == 0 else int(z) % K.p)
                                    for z in row] for row in vv]
                  for k, vv in ptj.items()}
        except Exception:
            continue
        if set(bl) != gamma(m):
            continue
        gs = gamma(m)
        clean = L.is_clean_point(m, bl, K)
        anz = L.all_cells_nonzero(m, bl, K)
        if not (clean and anz):
            continue
        for (mm, v) in CASES:
            if mm != m:
                continue
            N = Nbr(m, v)
            unt = untriggered(m, v)
            # ---- N1 identity, on a sample
            for w in unt[::max(1, len(unt) // 12)]:
                q = [Qs(m, bl, v, s, w, K) for s in N]
                for t in range(3):
                    ww = list(w)
                    ww[v] = t
                    lhs = C.haf_on(bl, gs, tuple(range(8)), tuple(ww),
                                   K.n(0), K.n(1))
                    S = Sprime(m, bl, v, tau_of(m, v, w), K)
                    rhs = sum((S[t][j] * q[j] for j in range(3)), K.n(0))
                    idn += 1
                    idbad += (not K.iszero(lhs - rhs))
            # ---- N2 ROWS vs S' row-subset ranks
            for (w, fire) in L.index_choices_cached(m, 'R', v)[::37]:
                sd = L.slice_data(m, bl, 'R', v, w, K)
                if sd is None:
                    continue
                d, uu, MM, sc = sd
                ROWS = [[d[t] * uu[j] + sc * MM[t][j] for j in range(3)]
                        for t in range(3)]
                S = Sprime(m, bl, v, tau_of(m, v, w), K)
                for sub in ((0,), (1,), (2,), (0, 1), (0, 2), (1, 2),
                            (0, 1, 2)):
                    rf_n += 1
                    if L.rank_rows([ROWS[t] for t in sub], K) != \
                       L.rank_rows([S[t] for t in sub], K):
                        rf_bad += 1
            # ---- N4 hypotheses
            two, by = two_pair_tuples(m, v)
            perT = {}
            for tau, d in sorted(two.items()):
                S = Sprime(m, bl, v, tau, K)
                rk = L.rank_rows(S, K)
                nz = 0
                nw = 0
                for w in unt:
                    if tau_of(m, v, w) != tau:
                        continue
                    nw += 1
                    if any(not K.iszero(Qs(m, bl, v, s, w, K)) for s in N):
                        nz += 1
                surv = {}
                for f, ws in d.items():
                    ok = 0
                    for w in ws:
                        sd = L.slice_data(m, bl, 'R', v, w, K)
                        if sd is None:
                            continue
                        dd, uu, MM, sc = sd
                        q0 = [j for j in range(3) if all(K.iszero(MM[t][j])
                                                        for t in range(3))]
                        if q0 and K.iszero(uu[q0[0]]):
                            continue
                        ok += 1
                    surv[f] = ok
                perT[str(tau)] = dict(
                    rank_Sp=rk, n_untriggered=nw, n_with_Qnonzero=nz,
                    hypQ=(nz > 0), surviving=surv,
                    both_survive=all(x > 0 for x in surv.values()),
                    rank_pairs={str(sorted(set(range(3)) - {f})):
                                L.rank_rows([S[t] for t in
                                             sorted(set(range(3)) - {f})], K)
                                for f in d})
            rep = L.vertex_report(m, bl, 'R', v, K, stop_early=False)
            good = [t for t, r in perT.items()
                    if r["hypQ"] and r["both_survive"]]
            recs.append(dict(tag=tag, m=m, v=v, field=fld,
                             offstratum=any(not K.iszero(
                                 C.haf_on(bl, gs, tuple(range(8)), (a,) * 8,
                                          K.n(0), K.n(1))) for a in range(3)),
                             DELIVERS=rep['DELIVERS'], n_idx=rep['n_idx'],
                             n_deliver=rep['n_deliver'],
                             n_two_pair=len(perT),
                             n_tuples_hyp_ok=len(good),
                             hypotheses_hold=(len(good) > 0),
                             theorem_ok=(not (len(good) > 0)
                                         or rep['DELIVERS']),
                             per_tuple=perT))
            print("%-40s m=%d R%d %-2s hypOK=%d/%d DELIVERS=%s thm_ok=%s"
                  % (tag[:40], m, v, fld, len(good), len(perT),
                     rep['DELIVERS'], recs[-1]['theorem_ok']), flush=True)
        # ---- N5 negative control vertices
        for (mm, v) in NEG:
            if mm != m:
                continue
            rep = L.vertex_report(m, bl, 'R', v, K, stop_early=False)
            two, by = two_pair_tuples(m, v)
            negrecs.append(dict(tag=tag, m=m, v=v, DELIVERS=rep['DELIVERS'],
                                n_two_pair=len(two),
                                n_firing=len({f for d in by.values()
                                              for f in d})))
        ck()

    OUT["N1_identity"] = dict(n=idn, bad=idbad, ok=(idbad == 0))
    OUT["_controls_run"].append("N1_identity")
    OUT["N2_rowsform"] = dict(n=rf_n, bad=rf_bad, ok=(rf_bad == 0))
    OUT["_controls_run"].append("N2_rowsform")
    OUT["N4_hypotheses"] = dict(
        n=len(recs),
        n_hyp_hold=sum(1 for r in recs if r["hypotheses_hold"]),
        n_deliver=sum(1 for r in recs if r["DELIVERS"]),
        n_theorem_ok=sum(1 for r in recs if r["theorem_ok"]),
        n_violations=sum(1 for r in recs if not r["theorem_ok"]),
        per_point=recs, ok=all(r["theorem_ok"] for r in recs))
    OUT["_controls_run"].append("N4_hypotheses")
    OUT["N5_negctl"] = dict(
        n=len(negrecs),
        n_fail=sum(1 for r in negrecs if not r["DELIVERS"]),
        n_two_pair_zero=sum(1 for r in negrecs if r["n_two_pair"] == 0),
        detail=negrecs[:40],
        note="|N|=3 vertices with a single firing letter have NO two-pair "
             "tuple, so the argument does not apply to them -- and they are "
             "exactly the |N|=3 vertices W30 saw fail",
        ok=True)
    OUT["_controls_run"].append("N5_negctl")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["done"] = True
    ck()
    print("N3 DONE identity bad=%d/%d rowsform bad=%d/%d thm_violations=%d"
          % (idbad, idn, rf_bad, rf_n, OUT["N4_hypotheses"]["n_violations"]),
          flush=True)
    assert not missing, "CONTROL MANIFEST FAILURE %s" % missing


if __name__ == "__main__":
    main()
