#!/usr/bin/env python3
"""W36 task 1 diagnostic: WHAT IS MISSING at W30's r10 (beta) best points.

Declared controls:
  G0_identity   -- Phi(w|y6=t) == <S'_t, Q(w)> by two independent routes
                   (closed form vs raw Gamma-matching enumeration)
  G1_inherit    -- the inherited points really are clean/off-stratum/allnz
                   and R6 delivers there (reproduces W30's claim)
  G2_perclass   -- per-(y5,y7) Q-vanishing profile (the EXACT (beta) object)
  G3_structure  -- the derived per-class escape conditions, each checked
  G4_negctl     -- a random non-escape point must score < 1 everywhere
usage: w36_diag.py
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
DECL = ["G0_identity", "G1_inherit", "G2_perclass", "G3_structure",
        "G4_negctl"]


def phi_raw(bl, w, K):
    G = L.geom(25)
    return C.haf_on(bl, G['gs'], tuple(range(8)), w, K.n(0), K.n(1))


def check_identity(bl, K, words):
    bad = 0
    n = 0
    for w in words:
        B, Cc = W.BC(bl, w)
        for t in range(3):
            ww = list(w)
            ww[6] = t
            lhs = phi_raw(bl, tuple(ww), K)
            rhs = bl[(6, 7)][t][w[7]] * B + bl[(5, 6)][w[5]][t] * Cc
            n += 1
            if not K.iszero(lhs - rhs):
                bad += 1
    return n, bad


def struct_conditions(bl, K, k57, ws):
    """the conditions the per-class escape FORCES, each measured separately.
    Derivation (this lane): within a class (y5,y7) fixed, for every
    untriggered w with hafL(x) != 0,
        hafL(x)*A45[y4][y5] = -A03[x0][x3]*A25[x2][y5]*A14[x1][y4]   (P1)
        hafL(x)*A47[y4][y7] = -A23[x2][x3]*A07[x0][y7]*A14[x1][y4]   (P2)
    so, on the index sets actually present in the class:
      (S1) col y5 of A45 || col y7 of A47 || row x1 of A14 (in the y4 index)
      (S2) rows of A03 (x0 in play) and rows of A23 (x2 in play) are all
           parallel to one common x3-direction g
      (S3) hafL factorises: hafL(x) = h[x1]*n0[x0]*m2[x2]*g[x3] on the box
    We report, per class, how many of P1/P2 hold word-by-word and the
    parallelism defects, so the missing component is named exactly."""
    y5, y7 = k57
    n_P1 = n_P2 = 0
    for w in ws:
        x, y = w[:4], w[4:]
        hl = W.hafL(bl, x)
        lhs1 = hl * bl[(4, 5)][y[0]][y5]
        rhs1 = -(bl[(0, 3)][x[0]][x[3]] * bl[(2, 5)][x[2]][y5]
                 * bl[(1, 4)][x[1]][y[0]])
        lhs2 = hl * bl[(4, 7)][y[0]][y7]
        rhs2 = -(bl[(2, 3)][x[2]][x[3]] * bl[(0, 7)][x[0]][y7]
                 * bl[(1, 4)][x[1]][y[0]])
        n_P1 += K.iszero(lhs1 - rhs1)
        n_P2 += K.iszero(lhs2 - rhs2)
    # index sets actually in play in this class
    X0 = sorted({w[0] for w in ws}); X1 = sorted({w[1] for w in ws})
    X2 = sorted({w[2] for w in ws}); X3 = sorted({w[3] for w in ws})
    Y4 = sorted({w[4] for w in ws})
    u = [bl[(4, 5)][a][y5] for a in Y4]
    v = [bl[(4, 7)][a][y7] for a in Y4]
    rows14 = [[bl[(1, 4)][b][a] for a in Y4] for b in X1]
    S1 = L.rank_rows([u, v] + rows14, K)
    r03 = [[bl[(0, 3)][a][c] for c in X3] for a in X0]
    r23 = [[bl[(2, 3)][a][c] for c in X3] for a in X2]
    S2 = L.rank_rows(r03 + r23, K)
    return dict(cls=str(k57), n=len(ws), n_P1=n_P1, n_P2=n_P2,
                S1_rank=S1, S1_target=1, S2_rank=S2, S2_target=1,
                Y4=Y4, X0=X0, X1=X1, X2=X2, X3=X3)


def main():
    OUT = {"_header": W.HEADER, "_task": "task1 (beta) diagnostic",
           "_controls_declared": DECL, "_controls_run": []}
    res = os.path.join(HERE, "results_diag.json")

    def ck():
        json.dump(OUT, open(res, "w"), indent=1, default=str)

    # ---------------------------------------------------- inherited points
    src = []
    for fld in ('13', '31', 'Q'):
        p = os.path.join(W.W30, "results_r10_beta_%s.json" % fld)
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        if d.get("best"):
            src.append(("r10beta_%s" % fld, fld, d["best"]))
    for fld in ('13', 'Q'):
        p = os.path.join(W.W30, "results_r10_alpha_%s.json" % fld)
        if os.path.exists(p):
            d = json.load(open(p))
            if d.get("best"):
                src.append(("r10alpha_%s" % fld, fld, d["best"]))
    OUT["n_inherited"] = len(src)

    ident_n = ident_bad = 0
    inherit = []
    perclass = {}
    struct = {}
    for (tag, fld, rec) in src:
        K = W.K_of(fld)
        bl = W.load_point(rec["point"], K)
        cls = W.classes25()
        smp = [ws[0] for ws in cls.values()] + [W.untriggered25()[i]
                                                for i in (0, 37, 111, 250, 375)]
        a, b = check_identity(bl, K, smp)
        ident_n += a
        ident_bad += b
        rep = L.vertex_report(25, bl, 'R', 6, K)
        inherit.append(dict(
            tag=tag, field=fld, clean=W.clean_ok(bl, K),
            allnz=W.allnz(bl, K), offstratum=W.offstratum(bl, K),
            R6_delivers=rep['DELIVERS'], R6_n_idx=rep['n_idx'],
            rank_A45=L.rank_rows(bl[(4, 5)], K),
            rank_A47=L.rank_rows(bl[(4, 7)], K),
            rank_A14=L.rank_rows(bl[(1, 4)], K),
            rank_A03=L.rank_rows(bl[(0, 3)], K),
            rank_A23=L.rank_rows(bl[(2, 3)], K),
            rank_A25=L.rank_rows(bl[(2, 5)], K),
            rank_A07=L.rank_rows(bl[(0, 7)], K)))
        prof = W.qzero_profile(bl, K)
        perclass[tag] = {str(k): v for k, v in prof.items()}
        best, bk = W.beta_escape_score(bl, K)
        inherit[-1]["beta_score"] = round(best, 4)
        inherit[-1]["beta_best_class"] = str(bk)
        struct[tag] = [struct_conditions(bl, K, k, ws)
                       for k, ws in sorted(cls.items())]
        print("%-14s %-2s clean=%s allnz=%s off=%s R6=%s  beta_score=%.3f@%s"
              % (tag, fld, inherit[-1]['clean'], inherit[-1]['allnz'],
                 inherit[-1]['offstratum'], rep['DELIVERS'], best, bk),
              flush=True)
        ck()

    OUT["G0_identity"] = dict(n_checks=ident_n, n_mismatch=ident_bad,
                              ok=(ident_bad == 0))
    OUT["_controls_run"].append("G0_identity")
    OUT["G1_inherit"] = inherit
    OUT["_controls_run"].append("G1_inherit")
    OUT["G2_perclass"] = perclass
    OUT["_controls_run"].append("G2_perclass")
    OUT["G3_structure"] = struct
    OUT["_controls_run"].append("G3_structure")

    # -------------------------------------------------- negative control
    import w30_hunt as H
    K = W.K_of('31')
    rng = random.Random(36001)
    negs = []
    for _ in range(6):
        bl = H.seed_point_p(25, rng, 31)
        if bl is None:
            continue
        s, k = W.beta_escape_score(bl, K)
        negs.append(dict(score=round(s, 4), cls=str(k)))
    OUT["G4_negctl"] = dict(n=len(negs), scores=negs,
                            ok=all(r["score"] < 1.0 for r in negs),
                            note="random clean points must not sit on the "
                                 "(beta)-escape locus")
    OUT["_controls_run"].append("G4_negctl")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["done"] = True
    ck()
    print("DIAG DONE identity %d/%d bad; manifest_ok=%s"
          % (ident_bad, ident_n, OUT["_manifest_ok"]), flush=True)
    assert not missing, "CONTROL MANIFEST FAILURE %s" % missing


if __name__ == "__main__":
    main()
