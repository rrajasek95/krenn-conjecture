#!/usr/bin/env python3
"""A12 TARGET 2 (d) -- the two sharp questions behind the m=28 retraction.
UNAUDITED.

N0_path      -- the four two-firing m=28 vertices and the Gamma path they
                induce; the common untriggered word classes of each adjacent
                pair, under W36's construction and under the honest one
N1_verdicts  -- the decisive measurement: at each surviving choice, compare
                the TRUE delivery verdict (computed on ROWS, the predicate of
                record) with the verdict the SLICE would give (same test run
                on S').  Where they differ, rank S' does not control the
                predicate.  Run at m=25/26/27 (must agree everywhere) and at
                m=28 on the stored both-rank-3 objects
N2_control   -- a positive control: the S'-verdict computation must be able
                to disagree (it does, at m=28), and a mutation of one slice
                cell must move at least one verdict
"""
from __future__ import annotations

import json
import os
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
W30 = os.path.join(ROOT, "unaudited-exclusion-w30-2026-08-19")
W36 = os.path.join(ROOT, "unaudited-routea-w36-2026-08-20")
sys.path.insert(0, HERE)
import a12_lib as A  # noqa: E402
from a12_t0 import Manifest  # noqa: E402
from a12_t4 import CASES, corpus, jointstar  # noqa: E402

DECL = ["N0_path", "N1_verdicts", "N2_control"]


def verdict_pair(tm, bl, kind, v, K, idx):
    """(ROWS verdict, S' verdict) per surviving choice."""
    out = []
    for (w, fire) in idx:
        R, sc, uu, MM = tm.rows_and_scale(bl, kind, v, w, K)
        if R is None:
            continue
        S = tm.Sprime(bl, v, tm.tau_of(v, w), K)
        cts = [t for t in range(3) if t not in fire]

        def dec(M):
            rc = A.rank([M[t] for t in cts], K)
            return all(A.rank([M[t] for t in cts] + [M[t2]], K) == rc
                       for t2 in sorted(fire))
        out.append((w, tuple(sorted(fire)), dec(R), dec(S)))
    return out


def main():
    t0 = time.time()
    man = Manifest(DECL)
    res = os.path.join(HERE, "results_t6.json")

    # -------------------------------------------------------------- N0
    tm28 = A.T(28)
    four = [1, 2, 5, 6]
    path = [(a, b) for a in four for b in four
            if a < b and tuple(sorted((a, b))) in tm28.gamma]
    n0 = dict(four_vertices=four, gamma_edges_among_them=[list(e) for e in path],
              is_path=(sorted(path) == [(1, 2), (2, 5), (5, 6)]))
    K = A.Rat
    pts = corpus(28, 1)
    bl = A.load_point(pts[0][2], A.K_of(pts[0][1]))
    Kp = A.K_of(pts[0][1])
    n0["pairs"] = {}
    for (a, b) in path:
        n0["pairs"][str((a, b))] = dict(
            w36=jointstar(tm28, bl, a, b, Kp, True),
            honest=jointstar(tm28, bl, a, b, Kp, False))
    man.record("N0_path", dict(
        **n0, ok=n0["is_path"],
        note="(2,5) is the pair W26 named; its common untriggered class is "
             "the one the joint object is silent about"))
    print("N0: path %s ; pair class counts %s"
          % (n0["gamma_edges_among_them"],
             {k: (v["w36"]["n_common"], v["w36"]["n_classes_ge2"],
                  v["honest"]["n_common"], v["honest"]["n_classes_ge2"])
              for k, v in n0["pairs"].items()}), flush=True)

    # -------------------------------------------------------------- N1
    per = {}
    for m in (25, 26, 27):
        tm = A.T(m)
        idxs = {(k, v): tm.index_choices(k, v) for (k, v) in CASES[m]}
        for (kind, v) in CASES[m]:
            n = dis = 0
            for (tag, fld, ptj) in corpus(m, 4):
                Kf = A.K_of(fld)
                b = A.load_point(ptj, Kf)
                if set(b) != set(tm.gamma) or not (tm.is_clean(b, Kf)
                                                   and tm.all_nonzero(b, Kf)):
                    continue
                for (_w, _f, rv, sv) in verdict_pair(tm, b, kind, v, Kf,
                                                     idxs[(kind, v)]):
                    n += 1
                    dis += (rv != sv)
            per["m%d_%s%d" % (m, kind, v)] = dict(n=n, disagreements=dis)
            print("N1 m=%d %s%d: %d choices, ROWS-vs-S' verdict "
                  "disagreements %d" % (m, kind, v, n, dis), flush=True)
    # m = 28 on the stored both-rank-3 objects
    tags = []
    pre = os.path.join(W36, "results_elim_prelaunch.json")
    if os.path.exists(pre):
        for r in (json.load(open(pre)).get("E2_prelaunch", {})
                  or {}).get("per_point", []):
            if r.get("satisfies_target"):
                tags.append(r["tag"])
    wide = {"wide28_%s" % r.get("seed"): r["point"]
            for r in json.load(open(os.path.join(
                W30, "points_m28_wide.json"))).get("points", [])
            if not r.get("van")}
    objs = [t for t in tags if t in wide][:4]
    idxs28 = {(k, v): tm28.index_choices(k, v) for (k, v) in CASES[28]}
    det = []
    for t in objs:
        b = A.load_point(wide[t], A.Rat)
        for (kind, v) in CASES[28]:
            n = dis = rows_deliv = sp_deliv = 0
            for (_w, _f, rv, sv) in verdict_pair(tm28, b, kind, v, A.Rat,
                                                 idxs28[(kind, v)]):
                n += 1
                dis += (rv != sv)
                rows_deliv += rv
                sp_deliv += sv
            det.append(dict(tag=t, vertex="%s%d" % (kind, v), n=n,
                            disagreements=dis,
                            n_deliver_by_ROWS=rows_deliv,
                            n_deliver_by_Sprime=sp_deliv,
                            DELIVERS_by_ROWS=rows_deliv > 0,
                            DELIVERS_by_Sprime=sp_deliv > 0))
            print("N1 m=28 %-16s %s: %d choices, disagreements %d, deliver "
                  "ROWS %d vs S' %d" % (t[:16], "%s%d" % (kind, v), n, dis,
                                        rows_deliv, sp_deliv), flush=True)
    man.record("N1_verdicts", dict(
        m25_26_27=per, m28=det,
        ok=all(v["disagreements"] == 0 for v in per.values()),
        m28_disagreements=sum(r["disagreements"] for r in det),
        m28_vertices_where_Sprime_says_FAIL_but_ROWS_delivers=[
            (r["tag"], r["vertex"]) for r in det
            if r["DELIVERS_by_ROWS"] and not r["DELIVERS_by_Sprime"]],
        note="the delivery predicate of record is computed on ROWS; this "
             "asks what the SLICE would have said"))

    # -------------------------------------------------------------- N2
    ctl = []
    for t in objs[:2]:
        b = A.load_point(wide[t], A.Rat)
        base = {(kind, v): [x[2] for x in verdict_pair(
            tm28, b, kind, v, A.Rat, idxs28[(kind, v)])]
            for (kind, v) in CASES[28]}
        b2 = {e: [list(r) for r in vv] for e, vv in b.items()}
        b2[(5, 6)][0][0] = b2[(5, 6)][0][0] + 1
        moved = {}
        for (kind, v) in CASES[28]:
            new = [x[2] for x in verdict_pair(tm28, b2, kind, v, A.Rat,
                                              idxs28[(kind, v)])]
            moved["%s%d" % (kind, v)] = sum(
                1 for a, c in zip(base[(kind, v)], new) if a != c)
        ctl.append(dict(tag=t, verdicts_moved=moved))
        print("N2 %s: verdicts moved by one perturbed slice cell %s"
              % (t[:16], moved), flush=True)
    man.record("N2_control", dict(
        per_object=ctl,
        ok=(bool(ctl) and all(any(v > 0 for v in r["verdicts_moved"].values())
                              for r in ctl)),
        note="one perturbed A56 cell must move at least one delivery verdict "
             "-- the verdict computation is live, not constant"))

    man.finish(res, extra={"elapsed_s": round(time.time() - t0, 1)})
    print("T6 DONE in %.1fs" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
