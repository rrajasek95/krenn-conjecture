#!/usr/bin/env python3
"""W36 ROUND 2, TARGET 2 -- the m=28 JOINT-STAR rank condition, and its
elimination.

THE EXACT STATEMENT.  For an adjacent pair (v,v') of the four two-firing
letter vertices (they induce in Gamma the path L1 - L2 - R5 - R6, i.e.
1 - 2 - 5 - 6), let a COMMON CLASS be a set of words that are untriggered at
both v and v' and carry fixed tuples tau_v on N(v) and tau_v' on N(v').  Put
H_e(w) = haf(Gamma - e)(w) and let the STAR UNION be the
|N(v)| + |N(v')| - 1 = 7 edges incident to v or v'.  Then

  (JOINT)  rank S'(v,tau_v) = 3  AND  rank S'(v',tau_v') = 3
           =>  the n x 7 star-union matrix [H_e(w)]_{w in class, e in union}
               has RANK <= 2, and rank 1 whenever the shared kernel
               coordinates k^v_{v'}, k^{v'}_v are nonzero.

  Proof.  S'(v,tau).Q^v(w) = 0 at untriggered words and rank 3 leaves a
  1-dimensional kernel, so every Q^v(w) in the class is a multiple
  lambda(w) k^v of one 4-vector; likewise Q^{v'}(w) = mu(w) k^{v'}.  The
  edge (v,v') lies in both stars and H_{v,v'} = Q^v_{v'} = Q^{v'}_v, so
  lambda(w) k^v_{v'} = mu(w) k^{v'}_v, pinning mu to a constant multiple of
  lambda when those coordinates are nonzero.  Then every column of the
  union is a constant times lambda(w).  QED

So the pair (v,v') is EXCLUDED from being simultaneously rank-3 as soon as
one common class has joint star rank >= 2.  Counting: a class of n words
contributes 6(n-1) independent rank-one equations.

CANDIDATES.  Measured here from the templates:
  (1,2): 92 common words, 26 classes, every class of size >= 2, 396 eqs
  (5,6): 92 common words, 26 classes, every class of size >= 2, 396 eqs
  (2,5): 64 common words but ALL 64 classes are SINGLETONS -- 0 equations.
         The pair {L2,R5} is therefore PROVABLY SILENT for this object and
         is excluded from the candidate list.  (It is also the pair W26
         named and W30 refuted, so nothing is lost.)
Chosen: (5,6) = {R5,R6}, one of W30's four never-reached exclusions, and the
class free coordinates are exactly (w0,w1) -- so each H_e restricted to a
class is a 3x3 matrix in (w0,w1) and the ideal stays small.

Declared controls:
  E0_candidates  -- class census per adjacent pair; (2,5) shown silent
  E1_implication -- (JOINT) checked pointwise on the whole stored m=28
                    corpus, under the SHARPER rank-3 definition
  E2_prelaunch   -- NO stored m=28 object (co-failure points included) may
                    already satisfy the elimination target (ledger 27)
  E3_ideal       -- the ideal emitted: generators, variables, degrees
  E4_singular    -- the Singular verdict (char 0 and the primes 13, 31),
                    through the ledger-disciplined harness
  E5_negctl      -- a deliberately satisfiable sub-ideal must NOT come back
                    unit (guards against a mis-emitted system)
usage: w36_elim.py prelaunch | w36_elim.py emit | w36_elim.py run <ch> <secs>
"""
from __future__ import annotations
import json, os, sys, time
from fractions import Fraction as F
from itertools import combinations, product
sys.dont_write_bytecode = True
import w36_lib as W
import w36_n3 as N3
import w36_m28 as M8
import w30_lib as L
import w30_sing as SG
import w26_core as C

HERE = W.HERE
M = 28
DECL = ["E0_candidates", "E1_implication", "E2_prelaunch", "E3_ideal",
        "E4_singular", "E5_negctl"]
PATH = [(1, 2), (5, 6)]                 # (2,5) excluded: singleton classes
PAIR = (5, 6)


def vname(e, i, j):
    return "zza%d%d_%d%d" % (e[0], e[1], i, j)


def matchings(verts, gs):
    verts = list(verts)
    if not verts:
        return [[]]
    out = []
    a = verts[0]
    for k in range(1, len(verts)):
        b = verts[k]
        e = (min(a, b), max(a, b))
        if e not in gs:
            continue
        rest = verts[1:k] + verts[k + 1:]
        for mm in matchings(rest, gs):
            out.append([e] + mm)
    return out


def H_mono(e, w, gs):
    """haf(Gamma - e)(w) as a list of monomials, each a tuple of cell names."""
    verts = sorted(set(range(8)) - set(e))
    out = []
    for mm in matchings(verts, gs):
        out.append(tuple(sorted(vname(f, w[f[0]], w[f[1]]) for f in mm)))
    return out


def classes(a, b):
    Ua = set(N3.untriggered(M, a))
    Ub = set(N3.untriggered(M, b))
    cols = sorted({tuple(sorted((a, s))) for s in N3.Nbr(M, a)}
                  | {tuple(sorted((b, s))) for s in N3.Nbr(M, b)})
    by = {}
    for w in sorted(Ua & Ub):
        key = (tuple(w[s] for s in N3.Nbr(M, a)),
               tuple(w[s] for s in N3.Nbr(M, b)))
        by.setdefault(key, []).append(w)
    return by, cols


def poly_str(mons, sign=1):
    if not mons:
        return "0"
    return ("+" if sign > 0 else "-").join([""] + ["*".join(m)
                                                   for m in mons])[1:] \
        if sign > 0 else "-" + ("-".join("*".join(m) for m in mons))


def minor_poly(Hs, wi, wj, ci, cj):
    """H[wi][ci]*H[wj][cj] - H[wi][cj]*H[wj][ci], expanded."""
    pos = [tuple(sorted(m1 + m2)) for m1 in Hs[wi][ci] for m2 in Hs[wj][cj]]
    neg = [tuple(sorted(m1 + m2)) for m1 in Hs[wi][cj] for m2 in Hs[wj][ci]]
    cnt = {}
    for m in pos:
        cnt[m] = cnt.get(m, 0) + 1
    for m in neg:
        cnt[m] = cnt.get(m, 0) - 1
    terms = []
    for m, c in sorted(cnt.items()):
        if c == 0:
            continue
        s = "*".join(m)
        terms.append(("+" if c > 0 else "-")
                     + (("%d*" % abs(c)) if abs(c) != 1 else "") + s)
    if not terms:
        return None
    t = "".join(terms)
    return t[1:] if t[0] == "+" else t


def corpus28(lim=None):
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
               "results_hunt_m28_31_four.json", "results_hunt_m28_31_l1l2.json",
               "results_hunt_m28_13_l1r5.json", "results_hunt_m28_31_r6.json",
               "results_hunt_m28_13_r6.json", "results_hunt_m28_Q_q.json",
               "results_cover.json"):
        q = os.path.join(W.W30, fn)
        if not os.path.exists(q):
            continue
        fld = '13' if '_13' in fn else ('Q' if '_Q' in fn else '31')
        try:
            dd = json.load(open(q))
        except Exception:
            continue
        r = dd.get("best")
        if isinstance(r, dict) and isinstance(r.get("point"), dict):
            cp.append(("REFUT:%s" % fn, fld, r["point"]))
        for i, r in enumerate((dd.get("hits") or [])[:6]):
            if isinstance(r, dict) and isinstance(r.get("point"), dict):
                cp.append(("COFAIL:%s#%d" % (fn, i), fld, r["point"]))
    return cp[:lim] if lim else cp


def two_pair_tuples(v):
    by = {}
    for (w, fire) in L.index_choices_cached(M, 'R' if v >= 4 else 'L', v):
        if len(fire) != 1:
            continue
        by.setdefault(tuple(w[s] for s in N3.Nbr(M, v)), {}) \
            .setdefault(sorted(fire)[0], []).append(w)
    return {k: d for k, d in by.items() if len(d) >= 2}


def prelaunch(lim=None):
    OUT = {"_header": W.HEADER, "_task": "m=28 joint-star elimination, "
           "candidates + pre-launch", "_controls_declared": DECL,
           "_controls_run": []}
    res = os.path.join(HERE, "results_elim_prelaunch.json")
    cand = {}
    for (a, b) in [(1, 2), (2, 5), (5, 6)]:
        by, cols = classes(a, b)
        sz = sorted((len(v) for v in by.values()), reverse=True)
        cand[str((a, b))] = dict(
            n_common=sum(sz), n_classes=len(by), n_cols=len(cols),
            cols=[str(c) for c in cols], sizes=sz[:10],
            n_classes_ge2=sum(1 for s in sz if s >= 2),
            n_equations=6 * sum(s - 1 for s in sz if s >= 2),
            silent=(all(s < 2 for s in sz)))
    OUT["E0_candidates"] = dict(
        per_pair=cand, chosen=str(PAIR),
        excluded_silent=[k for k, v in cand.items() if v["silent"]],
        ok=(cand[str((2, 5))]["silent"] and not cand[str(PAIR)]["silent"]))
    OUT["_controls_run"].append("E0_candidates")
    print("E0:", json.dumps({k: (v["n_classes"], v["n_classes_ge2"],
                                 v["n_equations"], v["silent"])
                             for k, v in cand.items()}), flush=True)

    a, b = PAIR
    by, cols = classes(a, b)
    tp5 = two_pair_tuples(a)
    tp6 = two_pair_tuples(b)
    cp = corpus28(lim)
    OUT["corpus_n"] = len(cp)
    print("m=28 corpus: %d" % len(cp), flush=True)
    gs = N3.gamma(M)
    imp_n = imp_bad = 0
    recs = []
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
        # THE SHARPER rank-3 definition.  v can only FAIL if rank S'(v,tau)
        # = 3 at EVERY tuple carrying a SURVIVING admissible choice -- not
        # merely at the two-pair ones.  Delivery may perfectly well come
        # from a non-two-pair tuple, so restricting to two-pair tuples is a
        # strictly weaker (and wrong) test.
        rk = {}
        surv_tuples = {}
        for v, tp in ((a, tp5), (b, tp6)):
            kind = 'R' if v >= 4 else 'L'
            st = set()
            for (w, fire) in L.index_choices_cached(M, kind, v):
                if L.slice_data(M, bl, kind, v, w, K) is None:
                    continue
                st.add(tuple(w[s] for s in N3.Nbr(M, v)))
            surv_tuples[v] = st
            rk[v] = {t: L.rank_rows(M8.Sp(bl, v, t, K), K)
                     for t in (set(tp) | st)}
        all3 = {v: (bool(surv_tuples[v])
                    and all(rk[v][t] == 3 for t in surv_tuples[v]))
                for v in (a, b)}
        all3_twopair = {v: all(rk[v][t] == 3 for t in (tp5 if v == a else tp6))
                        for v in (a, b)}
        n_ok = n_cls = n_target = 0
        for key, ws in by.items():
            if len(ws) < 2:
                continue
            n_cls += 1
            Mx = [[M8.Hedge(bl, e, w, K) for e in cols] for w in ws]
            jr = L.rank_rows(Mx, K)
            both3 = (rk[a].get(key[0]) == 3 and rk[b].get(key[1]) == 3)
            if both3:
                imp_n += 1
                if jr > 2:
                    imp_bad += 1
            if jr <= 1:
                n_ok += 1
            # the elimination target: only classes whose BOTH tuples are
            # surviving two-pair tuples matter
            if key[0] in tp5 and key[1] in tp6:
                n_target += 1
        recs.append(dict(tag=tag, field=fld,
                         all_rank3_strict={str(k): v for k, v in all3.items()},
                         all_rank3_twopair={str(k): v for k, v
                                            in all3_twopair.items()},
                         n_surv_tuples={str(k): len(v) for k, v
                                        in surv_tuples.items()},
                         n_classes=n_cls, n_joint_rank_le1=n_ok,
                         n_target_classes=n_target,
                         satisfies_target=(all3[a] and all3[b]),
                         satisfies_weak=(all3_twopair[a] and all3_twopair[b]),
                         point=(W.dump_point(bl) if (all3[a] and all3[b])
                                else None),
                         fails=L.full_report(M, bl, K)['fails']))
        print("%-40s %-2s STRICT R5=%d R6=%d | weak R5=%d R6=%d | "
              "jr<=1 %d/%d fails=%s"
              % (tag[:40], fld, all3[a], all3[b], all3_twopair[a],
                 all3_twopair[b], n_ok, n_cls,
                 ",".join(recs[-1]['fails']) or "-"), flush=True)
        json.dump(OUT | {"E1_partial": recs}, open(res, "w"), indent=1,
                  default=str)
    OUT["E1_implication"] = dict(
        n=imp_n, bad=imp_bad, ok=(imp_bad == 0),
        note="both tuples at rank 3 => joint star rank <= 2")
    OUT["_controls_run"].append("E1_implication")
    OUT["E2_prelaunch"] = dict(
        n=len(recs),
        n_satisfy=sum(1 for r in recs if r["satisfies_target"]),
        n_all_rank1_classes=sum(1 for r in recs
                                if r["n_joint_rank_le1"] == r["n_classes"]
                                and r["n_classes"]),
        max_rank1_fraction=max([(r["n_joint_rank_le1"] / r["n_classes"])
                                for r in recs if r["n_classes"]] or [0]),
        per_point=recs,
        ok=not any(r["satisfies_target"] for r in recs),
        note="no stored object may already have BOTH R5 and R6 all-rank-3")
    OUT["_controls_run"].append("E2_prelaunch")
    OUT["_manifest_ok"] = True
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    print("PRELAUNCH DONE  implication bad=%d/%d ; objects satisfying the "
          "target = %d/%d ; objects with EVERY class at joint rank<=1 = %d"
          % (imp_bad, imp_n, OUT["E2_prelaunch"]["n_satisfy"], len(recs),
             OUT["E2_prelaunch"]["n_all_rank1_classes"]), flush=True)


def emit(which=0):
    """build the ideal for the classes of PAIR whose both tuples are
    surviving two-pair tuples; report size, and write the Singular script."""
    a, b = PAIR
    by, cols = classes(a, b)
    tp5, tp6 = two_pair_tuples(a), two_pair_tuples(b)
    gs = N3.gamma(M)
    keys = [k for k, ws in sorted(by.items())
            if len(ws) >= 2 and k[0] in tp5 and k[1] in tp6]
    out = dict(n_classes_total=len(by), n_target_classes=len(keys))
    gens = []
    used = set()
    per = []
    for k in keys:
        ws = by[k]
        Hs = [[H_mono(e, w, gs) for e in cols] for w in ws]
        g0 = []
        for wi, wj in combinations(range(len(ws)), 2):
            for ci, cj in combinations(range(len(cols)), 2):
                p = minor_poly(Hs, wi, wj, ci, cj)
                if p:
                    g0.append(p)
        gens.extend(g0)
        per.append(dict(cls=str(k), n_words=len(ws), n_gens=len(g0)))
        for w in ws:
            for e in cols:
                for m in H_mono(e, w, gs):
                    used.update(m)
    out.update(n_generators=len(gens), n_variables=len(used),
               per_class=per[:8], degree=6,
               vars_sample=sorted(used)[:10])
    return gens, sorted(used), out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'prelaunch'
    if mode == 'prelaunch':
        prelaunch(int(sys.argv[2]) if len(sys.argv) > 2 else None)
        return
    gens, vs, info = emit()
    print("E3 ideal: %s" % json.dumps({k: v for k, v in info.items()
                                       if k != 'per_class'}), flush=True)
    json.dump(info, open(os.path.join(HERE, "results_elim_ideal.json"), "w"),
              indent=1, default=str)
    if mode == 'emit':
        return
    ch = sys.argv[2] if len(sys.argv) > 2 else '0'
    secs = int(sys.argv[3]) if len(sys.argv) > 3 else 3600
    res = os.path.join(HERE, "results_elim_run_ch%s.json" % ch)
    OUT = {"_header": W.HEADER, "char": ch, "ideal": info,
           "_controls_declared": ["E4_singular", "E5_negctl"],
           "_controls_run": []}
    st = SG.selftest()
    OUT["harness_selftest"] = st
    script = ('LIB "elim.lib";\n' + SG.ringdecl(ch, vs)
              + "ideal zzi = " + ",\n  ".join(gens) + ";\n"
              + "ideal zzprod = " + "*".join(vs[:60]) + ";\n"
              + SG.sat_and_test("zzi", "zzprod") + "quit;\n")
    open(os.path.join(HERE, "elim_ch%s.sing" % ch), "w").write(script)
    t0 = time.time()
    r = SG.run(script, vs, timeout=secs)
    OUT["E4_singular"] = dict(ok=r["ok"], timeout=r.get("timeout"),
                              qlines=r.get("qlines", [])[:6],
                              stdout=r.get("stdout", "")[-3000:],
                              seconds=round(time.time() - t0))
    OUT["_controls_run"].append("E4_singular")
    # E5: a single class's minors alone must NOT be unit (it is satisfiable
    # -- many stored points have a class at joint rank 1)
    g1, v1, i1 = emit()
    sub = g1[:max(1, len(g1) // len(i1['per_class'] or [1]))]
    s2 = ('LIB "elim.lib";\n' + SG.ringdecl(ch, vs)
          + "ideal zzj = " + ",\n  ".join(sub) + ";\n"
          + "ideal zzk = std(zzj);\n"
          + '"UNIT=", (size(zzk)==1 and leadmonom(zzk[1])==1);\nquit;\n')
    r2 = SG.run(s2, vs, timeout=min(secs, 900))
    OUT["E5_negctl"] = dict(ok=("UNIT= 1" not in r2.get("stdout", "")
                                .replace("  ", " ")),
                            stdout=r2.get("stdout", "")[-800:],
                            timeout=r2.get("timeout"))
    OUT["_controls_run"].append("E5_negctl")
    OUT["_manifest_ok"] = True
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    print("ELIM ch=%s: ok=%s timeout=%s\n%s"
          % (ch, r["ok"], r.get("timeout"), r.get("stdout", "")[-1200:]),
          flush=True)


if __name__ == "__main__":
    main()
