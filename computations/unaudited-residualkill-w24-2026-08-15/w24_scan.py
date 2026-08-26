#!/usr/bin/env python3
"""W24 -- large independent scan: fresh clean points from W24's OWN descent,
classified by regime, with every candidate minimal kill certificate tested.
UNAUDITED.  Exact only.

Per point we record
  regime A  <=>  haf_Gamma(w) = 0 on ALL 6561 words (equivalently the
                 multilinear form vanishes identically)
  full residual verdict (combinatorial deg<=1 rows only)
  sub-verdicts of every ROW-ISOLATING sub-system (grouped, and per single
  L-word) -- a kill in any sub-system implies the full kill
  whether a PURE row exists (Phi_w = 0, exactly one variable, coeff != 0)
  rank of the homogeneous coefficient matrix
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w24_core as C                                              # noqa: E402
import w24_pts as P                                               # noqa: E402
import w24_resid as RS                                            # noqa: E402
import w24_ident as ID                                            # noqa: E402

NPER = int(sys.argv[1]) if len(sys.argv) > 1 else 12
DEADLINE = time.time() + (int(sys.argv[2]) if len(sys.argv) > 2 else 3000)


def analyse(m, bl, tag):
    T = C.TEMPLATES[m]
    gam = C.gamma_edges(T)
    gam_set = set(gam)
    regimeA = all(C.phi(bl, gam_set, w) == 0 for w in C.WORDS)
    cells, rows, cleanw = RS.build_system(m, bl)
    n = len(cells)
    pure = [(w, cells[[k for k in range(n) if v[k] != 0][0]])
            for w, v, c in rows
            if c == 0 and len([k for k in range(n) if v[k] != 0]) == 1]
    coefrank = len(C.rref([list(v) for _, v, _ in rows], n)[0])
    d = RS.verdict(m, bl)
    iso, live = ID.isolating_words(m)
    sub, subx = {}, {}
    for i in (0, 1, 2, 3):
        grp = {}
        for x, can in iso[i]:
            grp.setdefault(can, []).append(x)
        for can, xs in grp.items():
            lab = "%d|%s" % (i, ",".join(str(e) for e in can))
            v = ID.sub_verdict(m, bl, xs, list(can))
            sub[lab] = None if v is None else (v["killed"], v["inconsistent"],
                                               tuple(v["forced"]))
            for x in xs:
                v1 = ID.sub_verdict(m, bl, [x], list(can))
                subx["%s@%s" % (lab, "".join(map(str, x)))] = (
                    None if v1 is None else (v1["killed"], v1["inconsistent"],
                                             tuple(v1["forced"])))
    return dict(m=m, tag=tag, regimeA=regimeA, killed=d["killed"],
                inconsistent=d["inconsistent"],
                n_forced=len(d["forced_zero"]), forced=d["forced_zero"],
                n_pure=len(pure), coef_rank=coefrank, n_unknowns=n,
                n_live=len(live), sub=sub, subx=subx)


def main():
    out = {"_header": "UNAUDITED W24 independent scan of fresh clean points."}
    recs = []
    for m in (25, 26, 27, 28):
        got = 0
        n = 0
        while got < NPER and time.time() < DEADLINE:
            n += 1
            rng = random.Random(24_000_000 + m * 10007 + n)
            order = list(range(8))
            rng.shuffle(order)
            bl, clean = P.descent(m, rng, order=order, passes=3)
            if bl is None:
                continue
            gam = C.gamma_edges(C.TEMPLATES[m])
            gam_set = set(gam)
            if any(C.phi(bl, gam_set, w) != 0 for w in clean):
                continue
            if not all(bl[e][i][j] != 0 for e in gam
                       for i in range(3) for j in range(3)):
                continue
            got += 1
            r = analyse(m, bl, "W24 descent n=%d" % n)
            r["point"] = {str(e): [[str(x) for x in row] for row in bl[e]]
                          for e in gam}
            recs.append(r)
            print("m=%d n=%-4d regimeA=%-5s KILLED=%-5s incons=%-5s forced=%2d "
                  "pure=%4d coefrank=%2d/%d subkills=%d/%d"
                  % (m, n, r["regimeA"], r["killed"], r["inconsistent"],
                     r["n_forced"], r["n_pure"], r["coef_rank"],
                     r["n_unknowns"],
                     sum(1 for v in r["sub"].values() if v and v[0]),
                     len(r["sub"])), flush=True)
    out["records"] = recs
    # aggregate
    agg = {}
    for r in recs:
        k = "m%d" % r["m"]
        a = agg.setdefault(k, dict(n=0, killed=0, regimeA=0, incons=0,
                                   pure_gt0=0, sub_all_kill=0,
                                   subx_all_kill=0))
        a["n"] += 1
        a["killed"] += r["killed"]
        a["regimeA"] += r["regimeA"]
        a["incons"] += r["inconsistent"]
        a["pure_gt0"] += (r["n_pure"] > 0)
        a["sub_all_kill"] += all(v[0] for v in r["sub"].values() if v)
        a["subx_all_kill"] += all(v[0] for v in r["subx"].values() if v)
    out["aggregate"] = agg
    print("AGGREGATE", json.dumps(agg, indent=1))
    # DICHOTOMY check
    bad = [r["tag"] for r in recs
           if r["regimeA"] != (not r["inconsistent"])]
    print("dichotomy violations (regimeA xor inconsistent):", len(bad))
    out["dichotomy_violations"] = bad
    json.dump(out, open(os.path.join(HERE, "results_scan.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
