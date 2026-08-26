#!/usr/bin/env python3
"""A9-10: clause-level DIFF of the W29 encoder against mine (artifact audit).

Both CNFs are lifted to SEMANTIC literals -- ("Z",c,S) = "haf(t^c|S) = 0",
("NZ",c,S) = "!= 0", ("G+/-",c,S,w,u) for the Laplace auxiliaries -- and then
compared as sets of clauses.  Anything W29 has that I do not is checked for
validity by hand; anything I have that W29 does not only makes my UNSAT
stronger (it is my run that certifies the theorem).
"""
from __future__ import annotations

import json
import sys
import time
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-audit-a9-2026-08-20")
W29 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
       "unaudited-diagclose-w29-2026-08-19")
W28 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
       "unaudited-x4empty-w28-2026-08-18")
for p in (BASE, W29, W28):
    if p not in sys.path:
        sys.path.insert(0, p)
import a9_enc as E                                                   # noqa: E402
import run_c2_unified as U                                           # noqa: E402
import run_a9_03_sat as S                                            # noqa: E402

RES = {}
OUT = f"{BASE}/results_a9_10_diff.json"
T0 = time.time()


def mine_sem(e):
    out = {}
    for tag, cl in zip(e.tags, e.cls):
        lits = []
        for l in cl:
            key = e.vname[abs(l)]
            if key[0] == "p":
                _, c, m = key
                lits.append(("NZ" if l > 0 else "Z", c, E.bits(m)))
            else:
                _, c, m, w, u = key
                lits.append(("G+" if l > 0 else "G-", c, E.bits(m), w, u))
        out.setdefault(frozenset(lits), set()).add(tag[0])
    return out


def w29_sem(van):
    out = {}
    for (tag, cl) in van.tagged:
        lits = []
        for l in cl:
            key = van.names[abs(l)]
            if key[0] == "z":
                _, c, Sq = key
                lits.append(("Z" if l > 0 else "NZ", c, tuple(Sq)))
            elif key[0] == "q":
                _, c, Sq, w, u = key
                lits.append(("G+" if l > 0 else "G-", c, tuple(Sq), w, u))
            else:
                lits.append(("OTHER", str(key), l > 0))
        out.setdefault(frozenset(lits), set()).add(tag[0])
    return out


def diff_case(Rs, n=8, k=4):
    e = E.Enc(n, Rs, k=k).build()
    van = U.build_van(n, Rs, kmax=k, z=n - 1)
    A, B = mine_sem(e), w29_sem(van)
    only_w29 = {c: sorted(B[c]) for c in B if c not in A}
    only_mine = {c: sorted(A[c]) for c in A if c not in B}
    return {"mine_clauses": len(e.cls), "mine_distinct": len(A),
            "w29_clauses": len(van.cls), "w29_distinct": len(B),
            "only_w29_count": len(only_w29), "only_mine_count": len(only_mine),
            "only_w29_tags": sorted({t for v in only_w29.values() for t in v}),
            "only_mine_tags": sorted({t for v in only_mine.values()
                                      for t in v}),
            "only_w29_sample": [sorted(map(str, c))
                                for c in list(only_w29)[:4]],
            "only_mine_sample": [sorted(map(str, c))
                                 for c in list(only_mine)[:4]]}


def main():
    reps = S.orbit_reps(8)
    cases = [reps[0], reps[10], reps[40], reps[86], ((3, 4, 5, 6),) * 3]
    RES["cases"] = {}
    for Rs in cases:
        RES["cases"][str(Rs)] = diff_case(Rs)
        print(str(Rs), json.dumps(RES["cases"][str(Rs)])[:500], flush=True)
    # also compare the verdicts case by case over all 87 orbits
    agree, dis = 0, []
    for Rs in reps:
        a = E.Enc(8, Rs, k=4).build().solve_pysat()[0]
        b = not U.build_van(8, Rs, kmax=4, z=7).is_unsat()
        if a == b:
            agree += 1
        else:
            dis.append([list(r) for r in Rs])
    RES["verdict_agreement"] = {"orbits": len(reps), "agree": agree,
                                "disagreements": dis}
    print("verdicts", RES["verdict_agreement"]["agree"], "/", len(reps),
          flush=True)
    RES["seconds"] = round(time.time() - T0, 1)
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)


if __name__ == "__main__":
    main()
