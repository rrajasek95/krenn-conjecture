#!/usr/bin/env python3
"""W30 round 9: (alpha) evaluation-map rank ; (beta) pinning consistency.
UNAUDITED.  Exact integer / rational arithmetic.

(beta) PINNING CONSISTENCY.  Untriggered words at vertex 6 are indexed by
(x0..x3, y4, y5, y7) with y6 free.  Inside one (y5,y7) class with the L-part
x FIXED, the only free coordinate is y4.  B(w) = 0 pins
    hafL(x) = - A03[x0][x3] A14[x1][y4] A25[x2][y5] / A45[y4][y5],
so two words of the class with the same x and different y4 force

  (P1)  A14[x1][y4] A45[y4'][y5] = A14[x1][y4'] A45[y4][y5]
and from C(w) = 0 likewise
  (P2)  A14[x1][y4] A47[y4'][y7] = A14[x1][y4'] A47[y4][y7]

-- pure Gamma-cell BINOMIALS, hafL eliminated.  Ranging over y5 (resp. y7)
these force A45 and A47 RANK ONE with A14's rows along the same direction.

(alpha) EVALUATION MAP.  hafL(x) = m1(x) + m2(x) + m3(x) with
m1 = A01[x0][x1] A23[x2][x3], m2 = A02[x0][x2] A13[x1][x3],
m3 = A03[x0][x3] A12[x1][x2].  Branch T = vanishing at the 42 words of
X_{R6,25}.  Rows = words, columns = distinct degree-2 monomials, entries
0/1.  Its exact rank and kernel dimension say how much freedom Branch T has.
usage: w30_r9.py
"""
from __future__ import annotations
import json, os, sys
from collections import defaultdict
from fractions import Fraction as F
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path: sys.path.insert(0, _p)
import w30_lib as L, w30_lattice as LT, w30_elim as EL, w30_m25 as M
import w26_core as C
VN = EL.vname
DECL = ["R0_engine_selftest", "R1_beta_pairs_enumerated",
        "R2_beta_certificate", "R3_alpha_rank", "R4_negative_control"]

def main():
    res = os.path.join(HERE, "results_r9.json")
    OUT = {"_header": "UNAUDITED W30 r9: (alpha) evaluation rank, "
                      "(beta) pinning consistency",
           "_controls_declared": DECL, "_controls_run": []}
    st = LT.selftest()
    OUT["R0_engine_selftest"] = dict(ok=st["infeasible_detected"] and
                                     st["feasible_not_flagged"])
    OUT["_controls_run"].append("R0_engine_selftest")
    # ---------------------------------------------------------- (beta)
    unt = M.untriggered()
    grp = defaultdict(list)          # (y5,y7,x) -> [y4,...]
    for w in unt:
        grp[(w[5], w[7], w[:4])].append(w[4])
    npair = 0
    gens = set()
    for (y5, y7, x), y4s in grp.items():
        y4s = sorted(set(y4s))
        for i in range(len(y4s)):
            for j in range(i + 1, len(y4s)):
                a, b = y4s[i], y4s[j]
                npair += 1
                gens.add("%s*%s - %s*%s" % (VN((1,4),x[1],a), VN((4,5),b,y5),
                                            VN((1,4),x[1],b), VN((4,5),a,y5)))
                gens.add("%s*%s - %s*%s" % (VN((1,4),x[1],a), VN((4,7),b,y7),
                                            VN((1,4),x[1],b), VN((4,7),a,y7)))
    gens = sorted(gens)
    vs = sorted({v for g in gens for v in
                 g.replace("*", " ").replace("-", " ").split()
                 if v.startswith("zza")})
    OUT["R1_beta_pairs_enumerated"] = dict(
        n_groups=len(grp), n_pairs=npair, n_generators=len(gens),
        n_vars=len(vs), ok=npair > 0)
    OUT["_controls_run"].append("R1_beta_pairs_enumerated")
    print("(beta) shared-L-part groups=%d, pairs=%d -> %d binomials in %d vars"
          % (len(grp), npair, len(gens), len(vs)), flush=True)
    rb = LT.find_certificate(gens, vs)
    OUT["R2_beta_certificate"] = dict(
        certificate=rb["found"], kernel_rank=rb.get("kernel_rank"),
        reverified=(LT.verify_certificate(gens, vs, rb["certificate"])
                    if rb["found"] else None), ok=True)
    OUT["_controls_run"].append("R2_beta_certificate")
    print("(beta) lattice certificate: %s" % rb["found"], flush=True)
    # structural consequence: do the generators force A45/A47/A14 rank one?
    y5s = sorted({k[0] for k in grp}); y7s = sorted({k[1] for k in grp})
    x1s = sorted({k[2][1] for k in grp})
    OUT["beta_structure"] = dict(
        distinct_y5=y5s, distinct_y7=y7s, distinct_x1=x1s,
        forces_A45_rank1=(len(y5s) >= 2), forces_A47_rank1=(len(y7s) >= 2),
        note="(P1) over >=2 values of y5 makes the columns of A45 pairwise "
             "proportional, i.e. A45 rank one; likewise A47 via (P2)")
    print("(beta) structure: y5 values=%s y7=%s x1=%s -> A45 rank1 forced=%s, "
          "A47 rank1 forced=%s" % (y5s, y7s, x1s, len(y5s) >= 2, len(y7s) >= 2),
          flush=True)
    # ---------------------------------------------------------- (alpha)
    kind, v = L.vkey('R6')
    X = set()
    for (w, fire) in L.index_choices_cached(25, kind, v):
        if len(fire) == 1: X.add(tuple(w[:4]))
    X = sorted(X)
    cols = {}
    rows = []
    for x in X:
        mons = [((0,1), x[0], x[1], (2,3), x[2], x[3]),
                ((0,2), x[0], x[2], (1,3), x[1], x[3]),
                ((0,3), x[0], x[3], (1,2), x[1], x[2])]
        r = {}
        for mo in mons:
            k = str(mo)
            if k not in cols: cols[k] = len(cols)
            r[cols[k]] = r.get(cols[k], 0) + 1
        rows.append(r)
    n = len(cols)
    M2 = [[F(rw.get(j, 0)) for j in range(n)] for rw in rows]
    # exact rank
    rk = 0; piv = []
    Mx = [row[:] for row in M2]
    for c in range(n):
        sel = None
        for i in range(rk, len(Mx)):
            if Mx[i][c] != 0: sel = i; break
        if sel is None: continue
        Mx[rk], Mx[sel] = Mx[sel], Mx[rk]
        pv = Mx[rk][c]; Mx[rk] = [z / pv for z in Mx[rk]]
        for i in range(len(Mx)):
            if i != rk and Mx[i][c] != 0:
                f = Mx[i][c]; Mx[i] = [a - f * b for a, b in zip(Mx[i], Mx[rk])]
        piv.append(c); rk += 1
        if rk == len(Mx): break
    OUT["R3_alpha_rank"] = dict(
        n_words=len(X), n_monomial_columns=n, exact_rank=rk,
        column_kernel_dim=n - rk, full_column_rank=(rk == n), ok=True,
        note="full column rank would force every monomial (a product of "
             "Gamma cells) to vanish, contradicting cells-nonzero")
    OUT["_controls_run"].append("R3_alpha_rank")
    print("(alpha) evaluation matrix: %d words x %d monomials, exact rank=%d, "
          "column-kernel dim=%d, full column rank=%s"
          % (len(X), n, rk, n - rk, rk == n), flush=True)
    rN = LT.find_certificate([gens[0]], vs) if gens else dict(found=False)
    OUT["R4_negative_control"] = dict(
        certificate=rN["found"], ok=(not rN["found"]),
        note="a single pinning binomial is satisfiable; no certificate allowed")
    OUT["_controls_run"].append("R4_negative_control")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == []); OUT["done"] = True
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("R9 DONE; manifest %s" % OUT["_controls_run"], flush=True)
if __name__ == "__main__": main()
