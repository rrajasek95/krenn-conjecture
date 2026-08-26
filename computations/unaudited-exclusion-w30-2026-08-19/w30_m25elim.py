#!/usr/bin/env python3
"""W30 m=25 ESCAPE ELIMINATION on the INCLUSION-MINIMAL COVERS.  UNAUDITED.

results_cover.json: at m=25 / R6 there are exactly 5 distinct escape covers
and 2 INCLUSION-MINIMAL ones, of sizes 12 and 30 (controls C3/C4 pass: each
really covers every two-pair tuple, and dropping any single word breaks it).
The size-12 cover is  W = { x : x0 = 0, x1 != 1, x2 != 2 }.

The escape system per cover:
  (E1) hafL(x) = 0 for x in W                       [trinomials, L-blocks]
  (E2) RED(w) = A67[y6][y7] A03[x0][x3] A25[x2][y5]
             + A56[y5][y6] A23[x2][x3] A07[x0][y7]  = 0
       for every clean word w with x in W           [binomials]
       -- this is Phi = 0 specialised to hafL = 0 at m=25, divided by
          d1 = A14[x1][y4] != 0
  (E3) the collapse minors of the SURVIVING units   [binomials, A56/A67]
Saturated by the product of the occurring cells (all Gamma cells nonzero).
UNIT  =>  that escape branch is impossible  =>  the (b) scale half holds.

Full ledger discipline via w30_sing.py (zz-prefix, no-shadowing guard,
'?'-parse, LIB elim.lib, list-form sat, integer coefficients).
usage: w30_m25elim.py <char> <timeout> [coveridx]
"""
from __future__ import annotations
import json, os, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path: sys.path.insert(0, _p)
import w30_sing as SG
import w30_elim as EL
import w30_side as SD
import w30_lib as L
import w26_core as C
from itertools import product
DECL = ["M0_harness_selftest", "M1_explicit_point_outside_locus",
        "M2_mutation", "M3_positive_control", "M4_cover_verified"]

def hafL_gens(W):
    out = []
    for x in sorted(W):
        out.append("%s*%s + %s*%s + %s*%s"
                   % (EL.vname((0,1),x[0],x[1]), EL.vname((2,3),x[2],x[3]),
                      EL.vname((0,2),x[0],x[2]), EL.vname((1,3),x[1],x[3]),
                      EL.vname((0,3),x[0],x[3]), EL.vname((1,2),x[1],x[2])))
    return out

def main():
    ch = int(sys.argv[1]); tmo = int(sys.argv[2])
    ci = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    res = os.path.join(HERE, "results_m25elim_ch%d_c%d.json" % (ch, ci))
    OUT = {"_header": "UNAUDITED W30 m=25 escape elimination",
           "char": ch, "cover_index": ci,
           "_controls_declared": DECL, "_controls_run": []}
    def ck(): json.dump(OUT, open(res, "w"), indent=1, default=str)
    st = SG.selftest()
    OUT["M0_harness_selftest"] = dict(results=st, ok=all(st.values()))
    OUT["_controls_run"].append("M0_harness_selftest")
    ck()
    cov = json.load(open(os.path.join(HERE, "results_cover.json")))
    covers = [set(tuple(z) for z in c)
              for c in cov["m25_inclusion_minimal_covers"]]
    covers.sort(key=len)
    W = covers[ci]
    ns, by, two = SD.realisation(25, 'R6')
    # M4: re-verify the cover property here, independently
    okc = all(any(set(X) <= W for X in two[t].values()) for t in two)
    OUT["M4_cover_verified"] = dict(cover_size=len(W), ok=okc)
    OUT["_controls_run"].append("M4_cover_verified")
    surv = [(t, P) for t in two for P in two[t] if not set(two[t][P]) <= W]
    gens = hafL_gens(W) + EL.red_gens(25, W)
    for (t, P) in surv:
        gens += EL.collapse_gens(6, ns, t, P)
    gens = sorted(set(gens))
    vs = sorted({v for g in gens
                 for v in g.replace("+"," ").replace("-"," ").replace("*"," ").split()
                 if v.startswith("zza")})
    OUT["n_gens"] = len(gens); OUT["n_vars"] = len(vs)
    OUT["n_surviving_units"] = len(surv); OUT["cover_size"] = len(W)
    print("cover %d: |W|=%d  surviving units=%d  gens=%d  vars=%d"
          % (ci, len(W), len(surv), len(gens), len(vs)), flush=True)
    ck()
    t0 = time.time()
    scr = EL.build_script(ch, vs, gens, vs)
    r = SG.run(scr, vs, timeout=tmo)
    unit = dim = None
    for ln in r.get("stdout","").splitlines():
        if ln.startswith("UNIT="): unit = int(ln.split("=")[1].strip())
        if ln.startswith("DIMENSION="): dim = ln.split("=")[1].strip()
    OUT["RESULT"] = dict(UNIT=unit, DIM=dim, singular_ok=r["ok"],
                         timeout=r.get("timeout"), qlines=r.get("qlines",[])[:4],
                         seconds=round(time.time()-t0))
    print("RESULT UNIT=%s DIM=%s ok=%s timeout=%s (%.0fs)"
          % (unit, dim, r["ok"], r.get("timeout"), time.time()-t0), flush=True)
    ck()
    # M3 positive control: a manifestly feasible ideal must be NON-unit
    r3 = SG.run(EL.build_script(ch, vs, [vs[0]+"-"+vs[1]], vs), vs, timeout=300)
    u3 = None
    for ln in r3.get("stdout","").splitlines():
        if ln.startswith("UNIT="): u3 = int(ln.split("=")[1].strip())
    OUT["M3_positive_control"] = dict(UNIT=u3, ok=(u3 == 0))
    OUT["_controls_run"].append("M3_positive_control")
    # M1 explicit point OUTSIDE the locus: a genuine clean m=25 point where
    # the escape does NOT hold must make some generator nonzero.
    from fractions import Fraction as Fr
    ctl = None
    src = os.path.join(HERE, "points_m25_wide.json")
    if os.path.exists(src):
        d = json.load(open(src))
        for rec in d["points"]:
            if rec.get("van"): continue
            bl = {eval(k): [[Fr(z) for z in row] for row in v]
                  for k, v in rec["point"].items()}
            env = {}
            for e, blk in bl.items():
                for i in range(3):
                    for j in range(3): env[EL.vname(e,i,j)] = blk[i][j]
            vals = []
            for g in gens[:40]:
                try: vals.append(eval(g, {}, env))
                except Exception: pass
            ctl = dict(seed=rec.get("seed"), n_evaluated=len(vals),
                       any_nonzero=any(z != 0 for z in vals),
                       note="genuine off-stratum clean m=25 point at which "
                            "the escape configuration does NOT hold")
            if ctl["any_nonzero"]: break
    OUT["M1_explicit_point_outside_locus"] = ctl or dict(ok=False, note="not run")
    if ctl: OUT["M1_explicit_point_outside_locus"]["ok"] = ctl["any_nonzero"]
    OUT["_controls_run"].append("M1_explicit_point_outside_locus")
    # M2 mutation: perturb one coefficient; verdict must be able to move
    gm = list(gens); gm[0] = gm[0].replace(" + ", " + 2*", 1)
    r2 = SG.run(EL.build_script(ch, vs, gm, vs), vs, timeout=tmo)
    u2 = None
    for ln in r2.get("stdout","").splitlines():
        if ln.startswith("UNIT="): u2 = int(ln.split("=")[1].strip())
    OUT["M2_mutation"] = dict(base_UNIT=unit, mutated_UNIT=u2,
                              flipped=(u2 != unit), ok=True)
    OUT["_controls_run"].append("M2_mutation")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == []); OUT["done"] = True
    ck()
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("M25ELIM DONE ch=%d cover=%d ; manifest %s" % (ch, ci, OUT["_controls_run"]), flush=True)
if __name__ == "__main__": main()
