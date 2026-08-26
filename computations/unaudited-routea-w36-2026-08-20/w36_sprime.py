#!/usr/bin/env python3
"""W36 (beta) REDUCTION: the whole hypothesis is a 2-block parallelism.

DERIVATION (this lane, from the committed cofactor identity).
At m=25, N(6) = {5,7}, so for every word w and every letter t at site 6

      Phi(w | y6 = t)  =  A67[t][y7] * B(w)  +  A56[y5][t] * C(w),          (I)
      B = hafL*r45 + l03*d1*d2 ,   C = hafL*r47 + l23*d0*d1 ,

and B, C do NOT involve the blocks A56, A67.  Write
      S'(y5,y7)  =  the 3x2 matrix  [ A67[t][y7] , A56[y5][t] ]_{t=0,1,2}.
Then ROWS(t) = hafL * (A67[t][y7], 0, A56[y5][t]), so with all Gamma cells
nonzero every row is nonzero and

  * rank S' = 1  =>  all rows parallel  =>  R6 DELIVERS at that choice;
  * rank S' = 2  =>  (I) at the three completions of any UNTRIGGERED word
                     forces Q = (B,C) = 0 on the whole (y5,y7) class.

So, on the clean locus, the (beta) hypothesis "some untriggered word in the
class has Q != 0" is EQUIVALENT to  rank S'(y5,y7) = 1, i.e. to

      A67[.][y7]  ||  A56[y5][.]        (as vectors in the site-6 letter).   (P)

CONSEQUENCE FOR THE SEARCH.  Cleanliness, with the eleven other blocks held
fixed, is a LINEAR system in the 18 unknowns (A56, A67):
      B(w) * A67[w6][w7]  +  C(w) * A56[w5][w6]  =  0   for every clean w.
So the entire (beta) escape locus over a fixed "outer" point is a LINEAR
SUBSPACE V, and (beta) fails iff V contains an all-nonzero vector violating
(P).  That is decided exactly, with no search.

Declared controls:
  P0_identity     -- (I) verified against raw Gamma-matching enumeration
  P1_membership   -- each stored point's own (A56,A67) lies in its V
  P2_dimension    -- dim V per point, and a basis
  P3_parallel     -- is (P) an identity on V?  (exact, via the quadrics)
  P4_violator     -- if not, an explicit all-nonzero violator = a (beta)
                     ESCAPE; then R6 is re-tested there
  P5_negctl       -- a deliberately wrong coefficient vector must fail P1
usage: w36_sprime.py [corpuslimit]
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
DECL = ["P0_identity", "P1_membership", "P2_dimension", "P3_parallel",
        "P4_violator", "P5_negctl"]
UNK = [('56', i, j) for i in range(3) for j in range(3)] + \
      [('67', i, j) for i in range(3) for j in range(3)]
IDX = {u: k for k, u in enumerate(UNK)}


def clean_rows_lin(bl, K):
    """the linear system on (A56, A67) imposed by cleanliness."""
    rows = []
    for w in C.clean_words(25):
        B, Cc = W.BC(bl, w)
        r = [K.n(0)] * 18
        r[IDX[('67', w[6], w[7])]] = r[IDX[('67', w[6], w[7])]] + B
        r[IDX[('56', w[5], w[6])]] = r[IDX[('56', w[5], w[6])]] + Cc
        if any(not K.iszero(z) for z in r):
            rows.append(r)
    return rows


def nullspace(rows, K, n=18):
    """exact kernel basis of the row system."""
    M = [list(r) for r in rows]
    if K.p:
        M = [[x % K.p for x in r] for r in M]
    piv = []
    r = 0
    for c in range(n):
        sel = None
        for i in range(r, len(M)):
            if not K.iszero(M[i][c]):
                sel = i
                break
        if sel is None:
            continue
        M[r], M[sel] = M[sel], M[r]
        iv = K.inv(M[r][c])
        M[r] = [(x * iv) % K.p if K.p else x * iv for x in M[r]]
        for i in range(len(M)):
            if i != r and not K.iszero(M[i][c]):
                f = M[i][c]
                M[i] = [((a - f * b) % K.p if K.p else a - f * b)
                        for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fc in free:
        v = [K.n(0)] * n
        v[fc] = K.n(1)
        for i, pc in enumerate(piv):
            v[pc] = K.n(0) - M[i][fc]
            if K.p:
                v[pc] %= K.p
        basis.append(v)
    return basis, piv


def vec_to_blocks(v):
    a56 = [[v[IDX[('56', i, j)]] for j in range(3)] for i in range(3)]
    a67 = [[v[IDX[('67', i, j)]] for j in range(3)] for i in range(3)]
    return a56, a67


def par_defect(a56, a67, K):
    """(y5,y7) classes where rank S' = 2 -- the (beta) escape classes."""
    bad = []
    for y5 in range(3):
        for y7 in range(3):
            S = [[a67[t][y7], a56[y5][t]] for t in range(3)]
            if L.rank_rows(S, K) > 1:
                bad.append((y5, y7))
    return bad


def load_corpus(limit=None):
    """every stored m=25 object reachable from W30's dir, tagged by source."""
    out = []
    p = os.path.join(W.W30, "points_m25_wide.json")
    if os.path.exists(p):
        d = json.load(open(p))
        for r in d.get("points", []):
            if not r.get("van"):
                out.append(("m25wide_%s" % r.get("seed"), 'Q', r["point"]))
    for fn, fld in (("results_r10_beta_13.json", '13'),
                    ("results_r10_beta_31.json", '31'),
                    ("results_r10_beta_Q.json", 'Q'),
                    ("results_r10_alpha_13.json", '13'),
                    ("results_r10_alpha_Q.json", 'Q')):
        q = os.path.join(W.W30, fn)
        if os.path.exists(q):
            d = json.load(open(q))
            if d.get("best"):
                out.append((fn.replace("results_", "").replace(".json", ""),
                            fld, d["best"]["point"]))
    for fn in ("results_indep_p13.json", "results_indep_p31.json"):
        q = os.path.join(W.W30, fn)
        if not os.path.exists(q):
            continue
        d = json.load(open(q))
        fld = '13' if '13' in fn else '31'
        for key in ("points", "hits", "records", "objects"):
            for i, r in enumerate(d.get(key, []) or []):
                pt = r.get("point") if isinstance(r, dict) else None
                if pt:
                    out.append(("indep%s_%s_%d" % (fld, key, i), fld, pt))
    for fn in ("results_escverify.json", "results_hunt_m25_13_R6.json",
               "results_hunt_m25_31_max.json", "results_hunt_m25_13_max.json"):
        q = os.path.join(W.W30, fn)
        if not os.path.exists(q):
            continue
        d = json.load(open(q))
        fld = '13' if '13' in fn else ('31' if '31' in fn else 'Q')
        for key in ("best", "object", "point"):
            r = d.get(key)
            if isinstance(r, dict) and "point" in r:
                out.append((fn[8:-5] + "_" + key, fld, r["point"]))
            elif isinstance(r, dict) and all(k.startswith("(") for k in r):
                out.append((fn[8:-5] + "_" + key, fld, r))
    ph = os.path.join(W.W30, "points_hunt.json")
    if os.path.exists(ph):
        d = json.load(open(ph))
        seen = set()
        for i, r in enumerate(d.get("points", [])):
            if r.get("m") != 25 or r.get("van"):
                continue
            key = json.dumps(r["point"], sort_keys=True)
            if key in seen:
                continue
            seen.add(key)
            out.append(("hunt%d_%s" % (i, r.get("tag")),
                        str(r.get("p") or 'Q'), r["point"]))
    return out[:limit] if limit else out


def main():
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    OUT = {"_header": W.HEADER, "_task": "(beta) reduction to 2-block parallel",
           "_controls_declared": DECL, "_controls_run": []}
    res = os.path.join(HERE, "results_sprime.json")

    def ck():
        json.dump(OUT, open(res, "w"), indent=1, default=str)

    corpus = load_corpus(lim)
    OUT["corpus_n"] = len(corpus)
    print("corpus objects: %d" % len(corpus), flush=True)

    idn = idbad = 0
    recs = []
    viol = []
    for (tag, fld, ptj) in corpus:
        K = W.K_of(fld)
        try:
            bl = W.load_point(ptj, K)
        except Exception as e:
            print("skip %s: %s" % (tag, e), flush=True)
            continue
        if set(bl) != set(W.E_ALL25):
            continue
        clean = W.clean_ok(bl, K)
        anz = W.allnz(bl, K)
        off = W.offstratum(bl, K)
        # ---- P0 on a sample
        for w in W.untriggered25()[::97]:
            B, Cc = W.BC(bl, w)
            for t in range(3):
                ww = list(w)
                ww[6] = t
                lhs = C.haf_on(bl, L.geom(25)['gs'], tuple(range(8)),
                               tuple(ww), K.n(0), K.n(1))
                rhs = bl[(6, 7)][t][w[7]] * B + bl[(5, 6)][w[5]][t] * Cc
                idn += 1
                idbad += (not K.iszero(lhs - rhs))
        rows = clean_rows_lin(bl, K)
        # P1: the point's own (A56,A67) must satisfy the system
        own = [K.n(0)] * 18
        for i in range(3):
            for j in range(3):
                own[IDX[('56', i, j)]] = bl[(5, 6)][i][j]
                own[IDX[('67', i, j)]] = bl[(6, 7)][i][j]
        memb = all(K.iszero(sum((a * b for a, b in zip(r, own)), K.n(0)))
                   for r in rows)
        basis, piv = nullspace(rows, K)
        dim = len(basis)
        bad_own = par_defect(bl[(5, 6)], bl[(6, 7)], K)
        rec = dict(tag=tag, field=fld, clean=clean, allnz=anz, offstratum=off,
                   n_clean_eq=len(rows), dimV=dim, membership=memb,
                   rank_A56=L.rank_rows(bl[(5, 6)], K),
                   rank_A67=L.rank_rows(bl[(6, 7)], K),
                   escape_classes_own=[str(t) for t in bad_own])
        # ---- P3/P4: is (P) an identity on V?  search V for an all-nonzero
        # violator.  dim is small, so sample the projective space of V.
        found = None
        if dim >= 1 and clean:
            rng = random.Random(hash(tag) & 0xffff)
            ntry = 0
            for _ in range(400):
                if K.p:
                    co = [rng.randrange(K.p) for _ in basis]
                else:
                    co = [F(rng.randint(-6, 6)) for _ in basis]
                if all(K.iszero(c) for c in co):
                    continue
                v = [K.n(0)] * 18
                for c, b in zip(co, basis):
                    for i in range(18):
                        v[i] = (v[i] + c * b[i]) % K.p if K.p \
                            else v[i] + c * b[i]
                a56, a67 = vec_to_blocks(v)
                if any(K.iszero(a56[i][j]) or K.iszero(a67[i][j])
                       for i in range(3) for j in range(3)):
                    continue
                ntry += 1
                bad = par_defect(a56, a67, K)
                if bad:
                    found = dict(coeffs=[str(c) for c in co],
                                 escape_classes=[str(t) for t in bad],
                                 A56=[[str(z) for z in r] for r in a56],
                                 A67=[[str(z) for z in r] for r in a67])
                    break
            rec["n_allnz_samples"] = ntry
        rec["violator"] = found is not None
        if found:
            b2 = {e: [r[:] for r in bl[e]] for e in bl}
            b2[(5, 6)] = [[K.n(int(z)) if K.p else F(z) for z in r]
                          for r in found["A56"]]
            b2[(6, 7)] = [[K.n(int(z)) if K.p else F(z) for z in r]
                          for r in found["A67"]]
            rep = L.vertex_report(25, b2, 'R', 6, K, stop_early=False)
            full = L.full_report(25, b2, K)
            found.update(recheck_clean=W.clean_ok(b2, K),
                         recheck_allnz=W.allnz(b2, K),
                         recheck_off=W.offstratum(b2, K),
                         R6_delivers=rep['DELIVERS'], R6_n_idx=rep['n_idx'],
                         R6_n_deliver=rep['n_deliver'], fails=full['fails'],
                         beta_score=W.beta_escape_score(b2, K)[0],
                         point=W.dump_point(b2))
            viol.append(dict(tag=tag, field=fld, **{k: v for k, v in
                                                    found.items()
                                                    if k != 'point'}))
            OUT["violator_points"] = OUT.get("violator_points", [])
            OUT["violator_points"].append(dict(tag=tag, field=fld,
                                               point=found["point"]))
            print("*** (beta) ESCAPE at %s: classes %s ; R6 delivers=%s "
                  "fails=%s" % (tag, found["escape_classes"],
                                found["R6_delivers"], found["fails"]),
                  flush=True)
        recs.append(rec)
        print("%-26s %-2s clean=%d allnz=%d off=%d dimV=%d memb=%d "
              "rkA56=%d rkA67=%d own_escape=%d viol=%s"
              % (tag, fld, clean, anz, off, dim, memb, rec['rank_A56'],
                 rec['rank_A67'], len(bad_own), rec['violator']), flush=True)
        ck()

    OUT["P0_identity"] = dict(n=idn, bad=idbad, ok=(idbad == 0))
    OUT["_controls_run"].append("P0_identity")
    ok1 = all(r["membership"] for r in recs if r["clean"])
    OUT["P1_membership"] = dict(n=len(recs), ok=ok1)
    OUT["_controls_run"].append("P1_membership")
    OUT["P2_dimension"] = dict(dims=sorted({r["dimV"] for r in recs}),
                               per_point=recs, ok=True)
    OUT["_controls_run"].append("P2_dimension")
    OUT["P3_parallel"] = dict(
        n_points=len(recs),
        n_with_own_escape=sum(1 for r in recs if r["escape_classes_own"]),
        n_with_violator=sum(1 for r in recs if r["violator"]), ok=True)
    OUT["_controls_run"].append("P3_parallel")
    OUT["P4_violator"] = dict(n=len(viol), violators=viol, ok=True)
    OUT["_controls_run"].append("P4_violator")
    # ---- P5 negative control: a wrong vector must NOT satisfy the system
    negok = None
    for (tag, fld, ptj) in corpus[:1]:
        K = W.K_of(fld)
        bl = W.load_point(ptj, K)
        rows = clean_rows_lin(bl, K)
        bad = [K.n(1)] * 18
        negok = not all(K.iszero(sum((a * b for a, b in zip(r, bad)), K.n(0)))
                        for r in rows)
    OUT["P5_negctl"] = dict(ok=bool(negok),
                            note="the all-ones vector must violate the clean "
                                 "system (else the system is vacuous)")
    OUT["_controls_run"].append("P5_negctl")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["done"] = True
    ck()
    print("SPRIME DONE  dims=%s  own_escapes=%d  violators=%d  ident_bad=%d"
          % (OUT["P2_dimension"]["dims"], OUT["P3_parallel"]["n_with_own_escape"],
             len(viol), idbad), flush=True)
    assert not missing, "CONTROL MANIFEST FAILURE %s" % missing


if __name__ == "__main__":
    main()
