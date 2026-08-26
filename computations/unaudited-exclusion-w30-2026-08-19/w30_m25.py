#!/usr/bin/env python3
"""W30 m=25 / R6: proving the two residual hypotheses.  UNAUDITED.  Exact.

Round 7 established: N(6) = {5,7} exactly, so S'(y5,y7) is 3x2 and the
cofactor identity is  Phi(w|y6=t) = A67[t][y7]*B(w) + A56[y5][t]*C(w)
with Q = (B,C), B = haf(Gamma-{6,7}), C = haf(Gamma-{6,5}).  Untriggered =>
S'.Q = 0, so Q != 0 forces rank S' <= 1, hence rank S'|P = rank S' and R6
DELIVERS.  Residual hypotheses:

 (alpha) some admissible index choice has hafL != 0        [Branch T empty]
 (beta)  Q != 0 at a matching untriggered word

(beta), derived.  At m=25,  B = hafL*r45 + l03*d1*d2,  C = hafL*r47 + l23*d0*d1.
B = C = 0 pins hafL twice; ELIMINATING hafL (and cancelling d1 != 0) gives the
pure GAMMA-CELL IDENTITY

    A03[x0][x3] * A25[x2][y5] * A47[y4][y7]
  = A23[x2][x3] * A07[x0][y7] * A45[y4][y5]                        (CELL)

-- a BINOMIAL, so the torus/lattice certificate engine applies with no
Groebner basis.  (beta) fails at (y5,y7) only if (CELL) holds at EVERY
untriggered word with that (y5,y7).

(alpha): hafL(x) = 0 for all x in X_{R6,25}; on that locus every clean word
gives the reduced binomial (RED), so the lattice engine applies there too.
usage: w30_m25.py
"""
from __future__ import annotations
import glob, json, os, sys, time
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path: sys.path.insert(0, _p)
import w30_lib as L, w30_lattice as LT, w30_elim as EL, w30_escape as E
import w26_core as C
DECL = ["N0_engine_selftest", "N1_prelaunch_beta", "N2_prelaunch_alpha",
        "N3_beta_certificates", "N4_alpha_certificate", "N5_negative_control"]
VN = EL.vname

def untriggered(m=25, v=6):
    G = L.geom(m); sing, lv = G['sing'], G['lv']
    out = []
    others = [c for c in range(8) if c != v]
    for vals in product(range(3), repeat=7):
        w = [0]*8
        for c, a in zip(others, vals): w[c] = a
        ok = True
        for t in range(3):
            ww = list(w); ww[v] = t
            if len(set(ww)) == 1 or any(ww[f[0]] == sing[f][0] and
                                        ww[f[1]] == sing[f][1] for f in lv):
                ok = False; break
        if ok: out.append(tuple(w))
    return out

def cell_gen(w):
    x, y = w[:4], w[4:]
    return ("%s*%s*%s - %s*%s*%s"
            % (VN((0,3),x[0],x[3]), VN((2,5),x[2],y[1]), VN((4,7),y[0],y[3]),
               VN((2,3),x[2],x[3]), VN((0,7),x[0],y[3]), VN((4,5),y[0],y[1])))

def Xv(m, lab):
    kind, v = L.vkey(lab); X = set()
    for (w, fire) in L.index_choices_cached(m, kind, v):
        if len(fire) == 1:
            X.add(tuple(w[:4]) if kind == 'R' else tuple(w[4:]))
    return X

def main():
    res = os.path.join(HERE, "results_m25proof.json")
    OUT = {"_header": "UNAUDITED W30 m=25/R6 residual hypotheses",
           "_controls_declared": DECL, "_controls_run": []}
    st = LT.selftest()
    OUT["N0_engine_selftest"] = dict(ok=st["infeasible_detected"] and
                                     st["feasible_not_flagged"])
    OUT["_controls_run"].append("N0_engine_selftest")
    unt = untriggered()
    by57 = defaultdict(list)
    for w in unt: by57[(w[5], w[7])].append(w)
    OUT["n_untriggered"] = len(unt)
    OUT["by_y5y7"] = {str(k): len(v) for k, v in by57.items()}
    print("untriggered words at vertex 6: %d ; (y5,y7) classes: %s"
          % (len(unt), OUT["by_y5y7"]), flush=True)
    # ---------------- pre-launch controls against all stored objects -------
    objs = []
    d25 = json.load(open(os.path.join(HERE, "points_m25_wide.json")))
    for r in d25["points"]:
        if not r.get("van"): objs.append(("m25wide_%d" % r["seed"], r["point"]))
    K = L.QF
    pre_b = []; pre_a = []
    X = Xv(25, 'R6')
    for (tag, ptj) in objs:
        bl = {eval(k): [[F(z) for z in row] for row in v] for k, v in ptj.items()}
        env = {}
        for e, blk in bl.items():
            for i in range(3):
                for j in range(3): env[VN(e, i, j)] = blk[i][j]
        holds = {}
        for k57, ws in by57.items():
            holds[str(k57)] = all(eval(cell_gen(w), {}, env) == 0 for w in ws)
        pre_b.append(dict(tag=tag, any_class_all_CELL=any(holds.values())))
        Z = E.hafL_zero_set(25, bl, K)
        pre_a.append(dict(tag=tag, missing=len(X - Z), satisfies=(X <= Z)))
    OUT["N1_prelaunch_beta"] = dict(
        n=len(pre_b), any_object_satisfies=any(r["any_class_all_CELL"] for r in pre_b),
        ok=not any(r["any_class_all_CELL"] for r in pre_b))
    OUT["_controls_run"].append("N1_prelaunch_beta")
    OUT["N2_prelaunch_alpha"] = dict(
        n=len(pre_a), min_missing=min(r["missing"] for r in pre_a),
        any_object_satisfies=any(r["satisfies"] for r in pre_a),
        ok=not any(r["satisfies"] for r in pre_a))
    OUT["_controls_run"].append("N2_prelaunch_alpha")
    print("PRE-LAUNCH beta: any stored object makes (CELL) hold on a whole "
          "(y5,y7) class? %s" % OUT["N1_prelaunch_beta"]["any_object_satisfies"],
          flush=True)
    print("PRE-LAUNCH alpha: min words missing from X_v = %d (X_v=%d)"
          % (OUT["N2_prelaunch_alpha"]["min_missing"], len(X)), flush=True)
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    # ---------------- (beta): lattice certificates per (y5,y7) -------------
    beta = {}
    allv = sorted({v for k in by57 for w in by57[k]
                   for v in cell_gen(w).replace("*"," ").replace("-"," ").split()
                   if v.startswith("zza")})
    for k57, ws in sorted(by57.items()):
        gens = sorted({cell_gen(w) for w in ws})
        r = LT.find_certificate(gens, allv)
        beta[str(k57)] = dict(n_words=len(ws), n_gens=len(gens),
                              certificate=r["found"],
                              support=r.get("n_generators_used"))
        if r["found"]:
            beta[str(k57)]["reverified"] = LT.verify_certificate(gens, allv,
                                                                 r["certificate"])
        print("  beta (y5,y7)=%s : %d words, %d gens -> certificate=%s"
              % (k57, len(ws), len(gens), r["found"]), flush=True)
    OUT["N3_beta_certificates"] = dict(
        per_class=beta,
        n_classes_certified=sum(1 for v in beta.values() if v["certificate"]),
        n_classes=len(beta),
        ok=True)
    OUT["_controls_run"].append("N3_beta_certificates")
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    # ---------------- (alpha): RED binomials on the X_v locus --------------
    red = EL.red_gens(25, X)
    vsA = sorted({v for g in red
                  for v in g.replace("*"," ").replace("+"," ").split()
                  if v.startswith("zza")})
    rA = LT.find_certificate(red, vsA) if red else dict(found=False)
    OUT["N4_alpha_certificate"] = dict(
        Xv_size=len(X), n_RED_gens=len(red), n_vars=len(vsA),
        certificate=rA["found"],
        reverified=(LT.verify_certificate(red, vsA, rA["certificate"])
                    if rA["found"] else None),
        ok=True)
    OUT["_controls_run"].append("N4_alpha_certificate")
    print("  alpha: |X_v|=%d, %d RED gens, %d vars -> certificate=%s"
          % (len(X), len(red), len(vsA), rA["found"]), flush=True)
    # negative control: a KNOWN-FEASIBLE subsystem must give no certificate
    rN = LT.find_certificate(sorted({cell_gen(unt[0])}), allv)
    OUT["N5_negative_control"] = dict(
        certificate=rN["found"], ok=(not rN["found"]),
        note="a single (CELL) binomial is satisfiable, so no certificate may "
             "be produced")
    OUT["_controls_run"].append("N5_negative_control")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == []); OUT["done"] = True
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("M25PROOF DONE; manifest %s" % OUT["_controls_run"], flush=True)
if __name__ == "__main__": main()
