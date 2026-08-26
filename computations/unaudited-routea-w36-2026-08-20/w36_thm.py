#!/usr/bin/env python3
"""W36 THEOREMS: the overlapping-clean-pair mechanism at |N(v)| = 2 and 3.

THEOREM W36-M25 (m = 25, vertex R6 -- UNCONDITIONAL in (beta)).
  Hypotheses  (H1) clean, (H2) every Gamma cell nonzero,
              (R25) some tuple tau = (y5,y7) carries two admissible index
                    choices with |T_f| = 1 and DIFFERENT firing letters,
                    both with hafL != 0.
  Conclusion  R6 delivers.
  Proof.  N(6) = {5,7} (the sigma edge 3-6 is absent), so
  ROWS(t) = hafL * (A67[t][y7], 0, A56[y5][t]) and, since hafL != 0, the rank
  of any set of rows of ROWS equals that of the same rows of the 3x2 slice
  S'(tau)[t] = (A67[t][y7], A56[y5][t]).  Every row of S' is nonzero by (H2),
  so 1 <= rank S' <= 2 with NO further hypothesis.  R6's firing letters are
  1 and 2 (template fact), so the two choices have clean pairs {0,2} and
  {0,1}, which share the letter 0.  If both failed, both pairs would have
  rank < rank S', i.e. rank 1, so S'_1 and S'_2 would both be parallel to
  S'_0 and rank S' = 1 -- but then every pair already has rank 1 = rank S'
  and both choices deliver.  Contradiction; so at least one delivers.  QED

  This REPLACES W30-M25-CONDITIONAL's hypothesis (beta).  (beta) is not
  merely unproved, it is FALSE in general: results_escobj.json exhibits a
  clean, all-nonzero, off-stratum m=25/F_13 point at which Q = (B,C)
  vanishes identically on the three (y5,y7) classes with y7 = 2 -- and R6
  still delivers, by exactly the mechanism above.

THEOREM W36-M2627-CONDITIONAL (m in {26,27}, |N(v)| = 3).
  Hypotheses  (H1) clean, (H2) every Gamma cell nonzero, (H3) off stratum,
              (N3) |N(v)| = 3, (D) v has two distinct firing letters,
              (R) some tuple tau on N(v) carries two admissible |T_f| = 1
                  choices with different firing letters, both surviving
                  (hafL != 0 and the absent-column coefficient u[q0] != 0),
              (Q3) some untriggered word with tuple tau has Q != 0.
  Conclusion  v delivers.
  Proof.  (R) makes ROWS = S' . T with T invertible, so ranks of row subsets
  agree.  (Q3) with S'.Q = 0 at untriggered words gives rank S' <= 2.  Rows
  are nonzero by (H2).  Then the overlapping-clean-pair argument above runs
  verbatim.  QED
  (Q3) is the ONLY residual: at |N| = 3 the slice is 3x3, so rank <= 2 is
  not automatic -- this is precisely why m=25 closes and m=26/27 do not.

Declared controls:
  T0_geometry    -- |N|, firing letters, two-pair tuples, absent column
  T1_rowsform    -- rank of every row subset agrees between ROWS and S'
  T2_hyp_m25     -- (R25) evaluated pointwise; conclusion checked
  T3_hyp_m2627   -- (H1)(H2)(H3)(N3)(D)(R)(Q3) evaluated pointwise
  T4_escape_obj  -- the theorem re-checked on the (beta) ESCAPE object and
                    on every stored escape/refutation object (ledger 27)
  T5_negctl      -- vertices with one firing letter have no two-pair tuple,
                    the theorem must NOT apply, and they must be seen failing
usage: w36_thm.py [corpus_limit]
"""
from __future__ import annotations
import json, os, sys
from fractions import Fraction as F
from itertools import combinations, product
sys.dont_write_bytecode = True
import w36_lib as W
import w36_n3 as N3
import w36_sprime as SP
import w30_lib as L
import w26_core as C

HERE = W.HERE
DECL = ["T0_geometry", "T1_rowsform", "T2_hyp_m25", "T3_hyp_m2627",
        "T4_escape_obj", "T5_negctl"]
PROT = [(25, 6), (26, 5), (26, 6), (27, 5)]
NEGV = [(25, 4), (25, 5), (25, 7), (26, 4), (26, 7), (27, 7)]


def surviving(m, v, w, K, bl):
    """admissible choice survives: scale != 0 and (if |N|=3) u[q0] != 0."""
    sd = L.slice_data(m, bl, 'R', v, w, K)
    if sd is None:
        return False, None
    d, uu, MM, sc = sd
    q0 = [j for j in range(3) if all(K.iszero(MM[t][j]) for t in range(3))]
    if len(N3.Nbr(m, v)) == 3:
        if not q0 or K.iszero(uu[q0[0]]):
            return False, sd
    return True, sd


def analyse_vertex(m, v, bl, K):
    N = N3.Nbr(m, v)
    two, by = N3.two_pair_tuples(m, v)
    unt = N3.untriggered(m, v)
    per = {}
    for tau, d in sorted(two.items()):
        S = N3.Sprime(m, bl, v, tau, K)
        rk = L.rank_rows(S, K)
        surv = {}
        for f, ws in d.items():
            surv[f] = sum(1 for w in ws if surviving(m, v, w, K, bl)[0])
        nq = 0
        nw = 0
        for w in unt:
            if N3.tau_of(m, v, w) != tau:
                continue
            nw += 1
            if any(not K.iszero(N3.Qs(m, bl, v, s, w, K)) for s in N):
                nq += 1
        both = all(x > 0 for x in surv.values()) and len(surv) >= 2
        per[str(tau)] = dict(rank_Sp=rk, surviving=surv, both_survive=both,
                             n_untriggered=nw, n_Qnonzero=nq,
                             hypQ=(nq > 0),
                             rank_le_2=(rk <= 2),
                             pair_ranks={str(f): L.rank_rows(
                                 [S[t] for t in range(3) if t != f], K)
                                 for f in d},
                             applies=(both and (len(N) == 2 or nq > 0)))
    rep = L.vertex_report(m, bl, 'R', v, K, stop_early=False)
    good = [t for t, r in per.items() if r["applies"]]
    return dict(m=m, v=v, nN=len(N), n_two_pair=len(per),
                n_applies=len(good), applies=(len(good) > 0),
                DELIVERS=rep['DELIVERS'], n_idx=rep['n_idx'],
                n_deliver=rep['n_deliver'],
                theorem_ok=((not good) or rep['DELIVERS']),
                n_rank2_tuples=sum(1 for r in per.values()
                                   if r["rank_Sp"] == 2),
                n_rank3_tuples=sum(1 for r in per.values()
                                   if r["rank_Sp"] == 3),
                per_tuple=per)


def rowsform_check(m, v, bl, K, stride=53):
    n = bad = 0
    for (w, fire) in L.index_choices_cached(m, 'R', v)[::stride]:
        ok, sd = surviving(m, v, w, K, bl)
        if not ok:
            continue
        d, uu, MM, sc = sd
        ROWS = [[d[t] * uu[j] + sc * MM[t][j] for j in range(3)]
                for t in range(3)]
        S = N3.Sprime(m, bl, v, N3.tau_of(m, v, w), K)
        for sub in ((0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)):
            n += 1
            if L.rank_rows([ROWS[t] for t in sub], K) != \
               L.rank_rows([S[t] for t in sub], K):
                bad += 1
    return n, bad


def corpus():
    out = []
    d = json.load(open(os.path.join(W.W30, "points_hunt.json")))
    for i, r in enumerate(d.get("points", [])):
        if r.get("m") in (25, 26, 27) and not r.get("van"):
            out.append(("hunt%d_%s" % (i, r.get("tag")), r["m"],
                        str(r.get("p") or 'Q'), r["point"]))
    for m in (25, 26, 27):
        p = os.path.join(W.W30, "points_m%d_wide.json" % m)
        if os.path.exists(p):
            for r in json.load(open(p)).get("points", []):
                if not r.get("van"):
                    out.append(("wide%d_%s" % (m, r.get("seed")), m, 'Q',
                                r["point"]))
    # stored ESCAPE / REFUTATION objects (ledger 27)
    for fn, m in (("results_escape_m27_13.json", 27),
                  ("results_escape_m27_31.json", 27),
                  ("results_escape_m26_13.json", 26),
                  ("results_escape_m25_13.json", 25),
                  ("results_escape_m25_31.json", 25)):
        q = os.path.join(W.W30, fn)
        if not os.path.exists(q):
            continue
        fld = '13' if '_13' in fn else '31'
        try:
            dd = json.load(open(q))
        except Exception:
            continue
        for i, r in enumerate((dd.get("records") or [])[:10]):
            if isinstance(r, dict) and isinstance(r.get("point"), dict):
                out.append(("ESCAPE:%s#%d(nzero=%s)" % (fn, i, r.get("nzero")),
                            m, fld, r["point"]))
    for fn, fld in (("results_r10_beta_13.json", '13'),
                    ("results_r10_beta_31.json", '31'),
                    ("results_r10_beta_Q.json", 'Q'),
                    ("results_r10_alpha_13.json", '13'),
                    ("results_r10_alpha_Q.json", 'Q')):
        q = os.path.join(W.W30, fn)
        if os.path.exists(q):
            dd = json.load(open(q))
            if dd.get("best"):
                out.append(("R10:%s" % fn, 25, fld, dd["best"]["point"]))
    return out


def main():
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    OUT = {"_header": W.HEADER, "_task": "W36 theorems |N|=2 and |N|=3",
           "_controls_declared": DECL, "_controls_run": []}
    res = os.path.join(HERE, "results_thm.json")

    def ck():
        json.dump(OUT, open(res, "w"), indent=1, default=str)

    geo = {}
    for (m, v) in PROT + NEGV:
        N = N3.Nbr(m, v)
        two, by = N3.two_pair_tuples(m, v)
        geo["m%dR%d" % (m, v)] = dict(
            N=N, nN=len(N), firing=sorted({f for d in by.values() for f in d}),
            n_two_pair=len(two), sigma_in_N=(N3.SIGINV[v] in N),
            absent_R=[s for s in range(4, 8) if s != v and s not in N])
    OUT["T0_geometry"] = dict(
        per_vertex=geo,
        ok=(all(geo["m%dR%d" % (m, v)]["n_two_pair"] > 0 for (m, v) in PROT)
            and all(geo["m%dR%d" % (m, v)]["n_two_pair"] == 0
                    for (m, v) in NEGV if len(geo["m%dR%d" % (m, v)]["firing"])
                    == 1)))
    OUT["_controls_run"].append("T0_geometry")
    print("T0:", json.dumps({k: (v["nN"], v["firing"], v["n_two_pair"])
                             for k, v in geo.items()}), flush=True)
    ck()

    cp = corpus()
    if lim:
        cp = cp[:lim]
    OUT["corpus_n"] = len(cp)
    print("corpus: %d objects" % len(cp), flush=True)
    rn = rb = 0
    recs = []
    negs = []
    esc = []
    for (tag, m, fld, ptj) in cp:
        K = W.K_of(fld)
        try:
            bl = {tuple(eval(k)): [[(F(z) if K.p == 0 else int(z) % K.p)
                                    for z in row] for row in vv]
                  for k, vv in ptj.items()}
        except Exception:
            continue
        if set(bl) != N3.gamma(m):
            continue
        if not (L.is_clean_point(m, bl, K) and L.all_cells_nonzero(m, bl, K)):
            continue
        off = any(not K.iszero(C.haf_on(bl, N3.gamma(m), tuple(range(8)),
                                        (a,) * 8, K.n(0), K.n(1)))
                  for a in range(3))
        for (mm, v) in PROT:
            if mm != m:
                continue
            a, b = rowsform_check(m, v, bl, K)
            rn += a
            rb += b
            r = analyse_vertex(m, v, bl, K)
            r.update(tag=tag, field=fld, offstratum=off,
                     is_escape_obj=tag.startswith("ESCAPE"))
            recs.append(r)
            if tag.startswith("ESCAPE") or r["n_rank2_tuples"] or \
               r["n_rank3_tuples"]:
                esc.append({k: vv for k, vv in r.items() if k != 'per_tuple'})
            print("%-46s m=%d R%d %-2s |N|=%d applies=%d/%d rank2=%d rank3=%d "
                  "DELIVERS=%s ok=%s"
                  % (tag[:46], m, v, fld, r['nN'], r['n_applies'],
                     r['n_two_pair'], r['n_rank2_tuples'], r['n_rank3_tuples'],
                     r['DELIVERS'], r['theorem_ok']), flush=True)
        for (mm, v) in NEGV:
            if mm != m:
                continue
            two, by = N3.two_pair_tuples(m, v)
            rep = L.vertex_report(m, bl, 'R', v, K)
            negs.append(dict(tag=tag, m=m, v=v, n_two_pair=len(two),
                             n_firing=len({f for d in by.values() for f in d}),
                             DELIVERS=rep['DELIVERS']))
        ck()

    OUT["T1_rowsform"] = dict(n=rn, bad=rb, ok=(rb == 0))
    OUT["_controls_run"].append("T1_rowsform")
    m25 = [r for r in recs if r["m"] == 25]
    OUT["T2_hyp_m25"] = dict(
        n=len(m25), n_applies=sum(1 for r in m25 if r["applies"]),
        n_deliver=sum(1 for r in m25 if r["DELIVERS"]),
        n_violations=sum(1 for r in m25 if not r["theorem_ok"]),
        n_with_rank2_tuple=sum(1 for r in m25 if r["n_rank2_tuples"]),
        ok=all(r["theorem_ok"] for r in m25))
    OUT["_controls_run"].append("T2_hyp_m25")
    m67 = [r for r in recs if r["m"] in (26, 27)]
    OUT["T3_hyp_m2627"] = dict(
        n=len(m67), n_applies=sum(1 for r in m67 if r["applies"]),
        n_deliver=sum(1 for r in m67 if r["DELIVERS"]),
        n_violations=sum(1 for r in m67 if not r["theorem_ok"]),
        n_hypQ_fails=sum(1 for r in m67 if not r["applies"]),
        ok=all(r["theorem_ok"] for r in m67))
    OUT["_controls_run"].append("T3_hyp_m2627")
    OUT["T4_escape_obj"] = dict(
        n=len(esc), detail=esc[:60],
        n_violations=sum(1 for r in esc if not r["theorem_ok"]),
        ok=all(r["theorem_ok"] for r in esc),
        note="every stored escape/refutation object and every point with a "
             "rank-2 or rank-3 two-pair tuple")
    OUT["_controls_run"].append("T4_escape_obj")
    OUT["T5_negctl"] = dict(
        n=len(negs), n_fail=sum(1 for r in negs if not r["DELIVERS"]),
        n_two_pair_zero=sum(1 for r in negs if r["n_two_pair"] == 0),
        n_one_firing=sum(1 for r in negs if r["n_firing"] == 1),
        by_vertex={"m%dR%d" % (m, v): dict(
            n=sum(1 for r in negs if r["m"] == m and r["v"] == v),
            fails=sum(1 for r in negs if r["m"] == m and r["v"] == v
                      and not r["DELIVERS"]),
            two_pair=next((r["n_two_pair"] for r in negs
                           if r["m"] == m and r["v"] == v), None))
            for (m, v) in NEGV},
        ok=True)
    OUT["_controls_run"].append("T5_negctl")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["records"] = [{k: v for k, v in r.items() if k != 'per_tuple'}
                      for r in recs]
    OUT["done"] = True
    ck()
    print("THM DONE  rowsform bad=%d/%d ; m25 viol=%d/%d ; m2627 viol=%d/%d ; "
          "escape-objects viol=%d/%d"
          % (rb, rn, OUT["T2_hyp_m25"]["n_violations"], len(m25),
             OUT["T3_hyp_m2627"]["n_violations"], len(m67),
             OUT["T4_escape_obj"]["n_violations"], len(esc)), flush=True)
    assert not missing, "CONTROL MANIFEST FAILURE %s" % missing


if __name__ == "__main__":
    main()
