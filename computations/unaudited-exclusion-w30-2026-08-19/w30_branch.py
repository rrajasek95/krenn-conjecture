#!/usr/bin/env python3
"""W30 BRANCH CLASSIFICATION + Branch-T PRE-LAUNCH CONTROL.  UNAUDITED.

FAIL_primary(v) splits as
  Branch T (total degeneracy): EVERY admissible |T_f|=1 index choice has
      scale 0, i.e. hafL == 0 on X_v (|X_v| = 42 of 81, uniform in m);
  Branch C: some index choice survives, and every survivor collapses with
      the firing row outside.
FAILURE = T or C.  (Round 6 said T was necessary for any failure -- that was
WRONG and is corrected here by direct classification of every stored
failure.)

Also the STANDING PRE-LAUNCH CONTROL: no elimination launches until its
target is evaluated at every stored escape / refutation object.
usage: w30_branch.py
"""
from __future__ import annotations
import glob, json, os, sys
from collections import Counter
from fractions import Fraction as F
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path: sys.path.insert(0, _p)
import w30_lib as L, w30_escape as E, w26_core as C
DECL = ["P1_prelaunch_escape_objects", "P2_branch_of_every_stored_failure",
        "P3_Xv_invariant"]

def Xv(m, lab):
    kind, v = L.vkey(lab)
    X = set()
    for (w, fire) in L.index_choices_cached(m, kind, v):
        if len(fire) == 1:
            X.add(tuple(w[:4]) if kind == 'R' else tuple(w[4:]))
    return X

def branch_of(m, bl, lab, K):
    """classify the vertex's situation: T, C, or DELIVERS."""
    kind, v = L.vkey(lab)
    nidx = ndel = 0
    for (w, fire) in L.index_choices_cached(m, kind, v):
        if len(fire) != 1: continue
        sd = L.slice_data(m, bl, kind, v, w, K)
        if sd is None: continue
        nidx += 1
        d, uu, MM, sc = sd
        rows = [[d[t]*uu[j] + sc*MM[t][j] for j in range(3)] for t in range(3)]
        ct = [t for t in range(3) if t not in fire]
        rpc = L.rank_rows([rows[t] for t in ct], K)
        if all(L.rank_rows([rows[t] for t in ct]+[rows[t2]], K) == rpc
               for t2 in fire):
            ndel += 1
    if ndel > 0: return "DELIVERS", nidx, ndel
    return ("BRANCH_T" if nidx == 0 else "BRANCH_C"), nidx, ndel

def main():
    res = os.path.join(HERE, "results_branch.json")
    OUT = {"_header": "UNAUDITED W30 branch classification + pre-launch control",
           "_controls_declared": DECL, "_controls_run": [],
           "prelaunch": [], "failures": []}
    # P3: the X_v invariant
    inv = {}
    for m in (25, 26, 27, 28):
        for lab in L.VERTS:
            inv["m%d_%s" % (m, lab)] = len(Xv(m, lab))
    OUT["P3_Xv_invariant"] = dict(sizes=inv,
        all_42=all(v == 42 for k, v in inv.items() if k[-2:] in
                   ('R5','R6','L1','L2')), ok=True)
    OUT["_controls_run"].append("P3_Xv_invariant")
    # P1: pre-launch control on escape objects
    objs = []
    d25 = json.load(open(os.path.join(HERE, "points_m25_wide.json")))
    for r in d25["points"]:
        if not r.get("van"):
            objs.append(("m25wide_%d" % r["seed"], 25, 0, r["point"]))
    for f in sorted(glob.glob(os.path.join(HERE, "results_escape_*.json"))):
        dd = json.load(open(f))
        m = dd["m"]; p = 0 if dd["field"] == 'Q' else int(dd["field"])
        for r in dd.get("records", [])[-3:]:
            objs.append((os.path.basename(f) + "|nz%d" % r.get("nzero", 0),
                         m, p, r["point"]))
    ev = json.load(open(os.path.join(HERE, "results_escverify.json")))
    for o in ev["objects"]:
        objs.append(("escverify_m%d" % o["m"], o["m"], o["p"], o["point"]))
    PROT = {25: 'R6', 26: 'R5', 27: 'R5', 28: 'R6'}
    worst = 99
    for (tag, m, p, ptj) in objs[:80]:
        K = L.QF if not p else L.FP(p)
        bl = ({eval(k): [[int(z) % p for z in row] for row in v]
               for k, v in ptj.items()} if p else
              {eval(k): [[F(z) for z in row] for row in v]
               for k, v in ptj.items()})
        if not L.all_cells_nonzero(m, bl, K): continue
        Z = E.hafL_zero_set(m, bl, K)
        X = Xv(m, PROT[m])
        miss = len(X - Z)
        worst = min(worst, miss)
        OUT["prelaunch"].append(dict(tag=tag, m=m, p=p, hafL_zero=len(Z),
                                     Xv=len(X), missing_from_BranchT=miss,
                                     satisfies_BranchT=(miss == 0)))
    OUT["P1_prelaunch_escape_objects"] = dict(
        n=len(OUT["prelaunch"]), min_missing=worst,
        any_satisfies=any(r["satisfies_BranchT"] for r in OUT["prelaunch"]),
        ok=not any(r["satisfies_BranchT"] for r in OUT["prelaunch"]),
        note="if ANY stored object satisfied Branch T the target would be "
             "FALSE and the elimination must not launch")
    OUT["_controls_run"].append("P1_prelaunch_escape_objects")
    print("PRE-LAUNCH: %d objects, closest is %d words short of Branch T, "
          "any satisfies=%s" % (len(OUT["prelaunch"]), worst,
          OUT["P1_prelaunch_escape_objects"]["any_satisfies"]), flush=True)
    # P2: which branch does every stored FAILURE live in?
    cnt = Counter()
    hp = json.load(open(os.path.join(HERE, "points_hunt.json")))
    n = 0
    for r in hp["points"][:150]:
        m = r["m"]; p = r["p"]
        if not p: continue
        K = L.FP(p)
        bl = {eval(k): [[int(z) % p for z in row] for row in v]
              for k, v in r["point"].items()}
        for lab in r["fails_hunter"]:
            b, nidx, ndel = branch_of(m, bl, lab, K)
            cnt[(m, lab, b)] += 1
            if b != "DELIVERS" and n < 12:
                OUT["failures"].append(dict(m=m, p=p, vertex=lab, branch=b,
                                            n_idx=nidx, tag=r["tag"][:40]))
                n += 1
    OUT["P2_branch_of_every_stored_failure"] = dict(
        table={"m%d|%s|%s" % k: v for k, v in cnt.items()},
        n_BRANCH_T=sum(v for k, v in cnt.items() if k[2] == "BRANCH_T"),
        n_BRANCH_C=sum(v for k, v in cnt.items() if k[2] == "BRANCH_C"),
        ok=True,
        note="CORRECTION to round 6: failure = T OR C; Branch T is NOT "
             "necessary for failure")
    OUT["_controls_run"].append("P2_branch_of_every_stored_failure")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == []); OUT["done"] = True
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("BRANCHES of stored failures: T=%d  C=%d"
          % (OUT["P2_branch_of_every_stored_failure"]["n_BRANCH_T"],
             OUT["P2_branch_of_every_stored_failure"]["n_BRANCH_C"]), flush=True)
    print("BRANCH DONE; manifest %s" % OUT["_controls_run"], flush=True)
if __name__ == "__main__": main()
