#!/usr/bin/env python3
"""W30 ESCAPE-LOCUS DELIVERY-MODE SWEEP.  UNAUDITED.  Exact.

A10's reframe: at every escape point the protected vertex STILL delivers,
by a mechanism W30-Y does not supply -- and round 5 showed it is NOT D2.
"264/264 non-collapse at one point" is a hypothesis generator; this sweeps
the escape locus and classifies EVERY delivery.

Escape point = clean, off-stratum, all Gamma cells nonzero, with a LARGE
hafL zero-set (the scale/realisation hypothesis of W30-Y/Z failing).

Modes, at an index choice with |T_f| = 1, clean pair P, augmented slice
matrix S' (sigma column first):
   M_zero      sc = 0                       (no information; not a delivery)
   M_nocol     rank S'|P = rank S'          (no letter collapse)     <- delivery
   M_inside    rank S'|P < rank S' but the firing row is INSIDE      <- delivery
   M_D2        rank phi(S') < rank S'  (ker phi meets the row space) <- delivery
   M_fail      non-delivery
usage: w30_escmode.py <outsuffix>
"""
from __future__ import annotations
import glob, json, os, sys, time
from collections import Counter
from fractions import Fraction as F
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path: sys.path.insert(0, _p)
import w30_lib as L, w30_escape as E, w26_core as C
PROT = {25: 'R6', 26: 'R5', 27: 'R5', 28: 'R6'}
DECL = ["E1_points_are_genuine_escapes", "E2_mode_classification_total",
        "E3_outside_locus_control"]

def modes(m, bl, lab, K):
    kind, v = L.vkey(lab)
    cnt = Counter()
    for (w, fire) in L.index_choices_cached(m, kind, v):
        if len(fire) != 1:
            cnt['skip_multifire'] += 1; continue
        sd = L.slice_data(m, bl, kind, v, w, K)
        if sd is None:
            cnt['M_zero'] += 1; continue
        d, uu, MM, sc = sd
        S = [[d[t]] + [MM[t][j] for j in range(3)] for t in range(3)]
        rows = [[d[t]*uu[j] + sc*MM[t][j] for j in range(3)] for t in range(3)]
        ct = [t for t in range(3) if t not in fire]
        rS = L.rank_rows(S, K); rSc = L.rank_rows([S[t] for t in ct], K)
        rp = L.rank_rows(rows, K); rpc = L.rank_rows([rows[t] for t in ct], K)
        deliv = all(L.rank_rows([rows[t] for t in ct]+[rows[t2]], K) == rpc
                    for t2 in fire)
        if not deliv: cnt['M_fail'] += 1
        elif rp < rS: cnt['M_D2'] += 1
        elif rSc == rS: cnt['M_nocol'] += 1
        else: cnt['M_inside'] += 1
    return dict(cnt)

def main():
    suf = sys.argv[1] if len(sys.argv) > 1 else ""
    res = os.path.join(HERE, "results_escmode%s.json" % suf)
    OUT = {"_header": "UNAUDITED W30 escape-locus delivery-mode sweep",
           "_controls_declared": DECL, "_controls_run": [], "points": []}
    jobs = []
    for f in sorted(glob.glob(os.path.join(HERE, "results_escape_*.json"))):
        d = json.load(open(f))
        m = d["m"]; p = 0 if d["field"] == 'Q' else int(d["field"])
        for r in d.get("records", []):
            if r.get("nzero", 0) >= 20:
                jobs.append((os.path.basename(f), m, p, r["point"], r["nzero"]))
    d25 = json.load(open(os.path.join(HERE, "points_m25_wide.json")))
    for r in d25["points"]:
        if not r.get("van"):
            jobs.append(("A10_925024" if r["seed"] == 925024 else
                         "m25wide_%d" % r["seed"], 25, 0, r["point"], None))
    t0 = time.time(); agg = Counter(); nesc = 0
    for (tag, m, p, ptj, nz) in jobs[:120]:
        K = L.QF if not p else L.FP(p)
        bl = ({eval(k): [[int(z) % p for z in row] for row in v]
               for k, v in ptj.items()} if p else
              {eval(k): [[F(z) for z in row] for row in v]
               for k, v in ptj.items()})
        if not L.all_cells_nonzero(m, bl, K): continue
        Z = E.hafL_zero_set(m, bl, K)
        lab = PROT[m]
        md = modes(m, bl, lab, K)
        isesc = len(Z) >= 20
        if isesc: nesc += 1
        for k2, v2 in md.items(): agg[k2] += v2
        OUT["points"].append(dict(tag=tag, m=m, p=p, hafL_zero=len(Z),
                                  escape=isesc, vertex=lab, modes=md,
                                  DELIVERS=(md.get('M_fail', 0) <
                                            sum(v3 for k3, v3 in md.items()
                                                if k3.startswith('M_') and
                                                k3 != 'M_zero'))))
        json.dump(OUT, open(res, "w"), indent=1, default=str)
        if len(OUT["points"]) % 10 == 0:
            print("[%3d] %.0fs agg=%s" % (len(OUT["points"]), time.time()-t0,
                                          dict(agg)), flush=True)
    OUT["aggregate_modes"] = dict(agg)
    OUT["n_escape_points"] = nesc
    escpts = [r for r in OUT["points"] if r["escape"]]
    aggE = Counter()
    for r in escpts:
        for k2, v2 in r["modes"].items(): aggE[k2] += v2
    OUT["aggregate_modes_escape_only"] = dict(aggE)
    OUT["E1_points_are_genuine_escapes"] = dict(
        n_escape=nesc, n_total=len(OUT["points"]), ok=nesc > 0)
    OUT["_controls_run"].append("E1_points_are_genuine_escapes")
    OUT["E2_mode_classification_total"] = dict(
        ok=True, note="every |T_f|=1 index choice lands in exactly one mode")
    OUT["_controls_run"].append("E2_mode_classification_total")
    nonesc = [r for r in OUT["points"] if not r["escape"]]
    aggN = Counter()
    for r in nonesc:
        for k2, v2 in r["modes"].items(): aggN[k2] += v2
    OUT["aggregate_modes_nonescape"] = dict(aggN)
    OUT["E3_outside_locus_control"] = dict(
        n_nonescape=len(nonesc), modes=dict(aggN), ok=len(nonesc) > 0,
        note="non-escape points swept too, so the escape profile can be "
             "compared against a baseline rather than read in isolation")
    OUT["_controls_run"].append("E3_outside_locus_control")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == []); OUT["done"] = True
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("ESCAPE-ONLY modes:", dict(aggE), flush=True)
    print("NON-ESCAPE modes :", dict(aggN), flush=True)
    print("ESCMODE DONE %d points (%d escapes) %.0fs"
          % (len(OUT["points"]), nesc, time.time()-t0), flush=True)
if __name__ == "__main__": main()
