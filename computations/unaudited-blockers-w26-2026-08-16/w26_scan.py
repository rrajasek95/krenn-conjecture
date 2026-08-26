#!/usr/bin/env python3
"""W26 -- broad scan: stratum, six sub-systems, solo-family verdicts, the
Case-2b predicate.  Reproduces W24's tallies and locates its exceptions.
UNAUDITED.  Exact only."""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w26_core as C                                              # noqa: E402
import w26_pts as PT                                              # noqa: E402
import w26_sub as SB                                              # noqa: E402

OUT = {"_header": "UNAUDITED W26 scan."}
NFRESH = int(os.environ.get("W26_NFRESH", "14"))


def score(m, bl, tag):
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    van = PT.vanishing_stratum(m, bl)
    subs = SB.all_sub_verdicts(m, bl)
    full = C.verdict(m, bl)
    solo = {str(e): SB.solo_report(m, bl, e) for e in C.live_singles(m)}
    rec = dict(m=m, tag=tag, vanishing_stratum=van,
               full_killed=full["killed"],
               full_inconsistent=full["inconsistent"],
               full_forced=full["forced_zero"],
               subs={k: (v and v["killed"]) for k, v in subs.items()},
               subs_detail=subs,
               solo_killed={k: v["killed"] for k, v in solo.items()},
               solo_surv=[k for k, v in solo.items() if v["survives"]],
               solo_detail=solo,
               n_pure_rows=len(C.pure_rows(m, bl)))
    if m == 25:
        c2b, n02, n01 = SB.case2b(25, bl)
        rec["case2b"] = c2b
        rec["n_par_02"] = n02
        rec["n_par_01"] = n01
    return rec


def main():
    recs = []
    print("=" * 78)
    print("STORED POINTS (W20/W21 on disk)")
    for m, tag, bl in PT.stored_points():
        r = score(m, bl, tag)
        recs.append(r)
        print("  m=%d %-24s van=%-5s full_kill=%s  subs=%s  solo_surv=%s"
              % (m, tag[:24], r["vanishing_stratum"], r["full_killed"],
                 "".join("K" if v else ("." if v is not None else "-")
                         for v in r["subs"].values()),
                 r["solo_surv"]), flush=True)
    print("=" * 78)
    print("FRESH POINTS (own descent)")
    for m in (25, 26, 27, 28):
        pts = PT.fresh_points(m, NFRESH, seed0=26_000_000)
        print("  m=%d : %d fresh clean points" % (m, len(pts)), flush=True)
        for i, bl in enumerate(pts):
            r = score(m, bl, "fresh%d" % i)
            recs.append(r)
            print("    m=%d fresh%-3d van=%-5s full_kill=%s subs=%s "
                  "solo_surv=%s%s"
                  % (m, i, r["vanishing_stratum"], r["full_killed"],
                     "".join("K" if v else ("." if v is not None else "-")
                             for v in r["subs"].values()),
                     r["solo_surv"],
                     (" CASE2B=%s (par02=%d par01=%d)"
                      % (r["case2b"], r["n_par_02"], r["n_par_01"]))
                     if m == 25 else ""), flush=True)
    OUT["records"] = recs
    # ---------------------------------------------------------- tallies
    print("=" * 78)
    tot = len(recs)
    nvan = sum(1 for r in recs if r["vanishing_stratum"])
    nfull = sum(1 for r in recs if r["full_killed"])
    allsub = sum(1 for r in recs
                 if all(v for v in r["subs"].values() if v is not None))
    print("points %d | vanishing stratum %d | full system kills %d | "
          "ALL six sub-systems kill %d" % (tot, nvan, nfull, allsub))
    exc = [(r["m"], r["tag"], [k for k, v in r["subs"].items() if v is False])
           for r in recs if not all(v for v in r["subs"].values()
                                    if v is not None)]
    print("EXCEPTIONS (some sub-system does not kill):")
    for m, t, ks in exc:
        print("   m=%d %-24s  not killed by: %s" % (m, t[:24], ks))
    OUT["tally"] = dict(n=tot, n_vanishing=nvan, n_full_killed=nfull,
                        n_all_six=allsub,
                        exceptions=[(m, t, ks) for m, t, ks in exc])
    # solo survivors anywhere?
    ss = [(r["m"], r["tag"], r["solo_surv"]) for r in recs if r["solo_surv"]]
    print("SOLO-FAMILY SURVIVORS (constant nonzero ratio):", len(ss))
    for m, t, k in ss[:20]:
        print("   m=%d %-24s %s" % (m, t[:24], k))
    OUT["solo_survivors"] = ss
    # case2b tally
    c2 = [(r["tag"], r["n_par_02"], r["n_par_01"])
          for r in recs if r["m"] == 25]
    OUT["m25_case2b"] = c2
    print("m=25 Case-2b hits: %d/%d"
          % (sum(1 for r in recs if r.get("case2b")), len(c2)))
    json.dump(OUT, open(os.path.join(HERE, "results_scan.json"), "w"),
              indent=1, default=str)
    print("wrote results_scan.json")


if __name__ == "__main__":
    main()
