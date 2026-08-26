#!/usr/bin/env python3
"""A11 follow-up: engine cross-check, the point-level escape system, and the
exact residual gap at the live r10 common-direction points.  UNAUDITED.

E1  my delivery engine against the stored hunter verdicts (external control).
E2  at the r10 points: the TRUE (point-level) untriggered set, the Q = 0
    census on it, and -- at a common-direction point -- the REDUCED escape
    system.  With A45 = v(x)a(y5), A47 = v(x)b(y7), A14[x1][.] = c*v,

        B = v[y4] * ( hafL(x)*a[y5] + A03[x0][x3]*c*A25[x2][y5] )
        C = v[y4] * ( hafL(x)*b[y7] + A23[x2][x3]*c*A07[x0][y7] )

    so B and C no longer depend on y4 and the whole escape collapses to two
    scalar systems in (x, y5) and (x, y7).  That is the exact residual.
E3  the control "Q = 0 forces hafL != 0" on points that really have Q = 0.
E4  the coverage forcing evaluated at the REAL live-tuple sets.
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from collections import Counter, defaultdict
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W30 = os.path.join(os.path.dirname(HERE), "unaudited-exclusion-w30-2026-08-19")
sys.path.insert(0, HERE)
import a11_lib as A      # noqa: E402
import a11_m25 as M      # noqa: E402

DECL = ["E1_engine_vs_stored_verdicts", "E2_point_level_escape",
        "E3_Q0_forces_hafL", "E4_coverage_at_real_live_sets",
        "E5_reduced_system_control"]


def point_untriggered(tm, bl, K):
    phi = {w: A.phi_gpm(tm, bl, w, K) for w in A.WORDS}
    other = [u for u in range(8) if u != 6]
    out = []
    for vals in product(range(3), repeat=7):
        w = [0] * 8
        for u, a in zip(other, vals):
            w[u] = a
        if all(K.iszero(phi[tuple(w[:6] + [t] + w[7:])]) for t in range(3)):
            out.append(tuple(w))
    return out


def coverage_for(unt, tuples):
    res = {}
    for x1 in range(3):
        ws = [w for w in unt if (w[5], w[7]) in tuples and w[1] == x1]
        out = {}
        for tag, idx in (("y5", 5), ("y7", 7)):
            per = {}
            for val in range(3):
                groups = defaultdict(set)
                for w in ws:
                    if w[idx] != val:
                        continue
                    groups[tuple(w[:4])].add(w[4])
                keys = list(groups)
                par = {k: k for k in keys}

                def find(a):
                    while par[a] != a:
                        par[a] = par[par[a]]
                        a = par[a]
                    return a
                for i in range(len(keys)):
                    for j in range(i + 1, len(keys)):
                        if groups[keys[i]] & groups[keys[j]]:
                            par[find(keys[i])] = find(keys[j])
                agg = defaultdict(set)
                for k in keys:
                    agg[find(k)] |= groups[k]
                per[val] = max([len(v) for v in agg.values()] or [0])
            out[tag] = per
        res[x1] = dict(n_words=len(ws),
                       y4_per_y5={str(k): v for k, v in out["y5"].items()},
                       y4_per_y7={str(k): v for k, v in out["y7"].items()},
                       forces_A45=all(v == 3 for v in out["y5"].values()),
                       forces_A47=all(v == 3 for v in out["y7"].values()))
    return res


def main():
    t0 = time.time()
    man = A.Manifest(DECL)
    rng = random.Random(987654)
    tm25 = A.T(25)
    unt_t = M.untriggered_template(25, 6)

    # ---------------------------------------------------- E1 engine control
    dat = json.load(open(os.path.join(W30, "points_hunt.json")))
    pool = dat["points"]
    rng.shuffle(pool)
    sel = []
    seen = Counter()
    for r in pool:
        k = (int(r["m"]), int(r["p"]))
        if seen[k] >= 6:
            continue
        seen[k] += 1
        sel.append(r)
        if len(sel) >= 36:
            break
    agree = 0
    dis = []
    for r in sel:
        m = int(r["m"])
        K = A.Rat if int(r["p"]) == 0 else A.Modp(int(r["p"]))
        tm = A.T(m)
        bl = A.load_point(r["point"], K)
        mine = A.full_verdict(tm, bl, K)['fails']
        stored = eval(r["fails_hunter"]) if isinstance(r["fails_hunter"], str)\
            else r["fails_hunter"]
        if sorted(mine) == sorted(stored):
            agree += 1
        else:
            dis.append(dict(tag=r["tag"], m=m, p=int(r["p"]),
                            mine=mine, stored=stored))
    man.record("E1_engine_vs_stored_verdicts", dict(
        n_points=len(sel), agree=agree, disagreements=dis,
        ok=(agree == len(sel)),
        note="my FAIL_primary engine vs the hunter's stored fails lists"))
    print("E1 engine agreement %d/%d ; disagreements %s"
          % (agree, len(sel), dis[:3]))

    # ------------------------------------------------ E2 point-level escape
    recs = {}
    for fn, fld in (("results_r10_beta_13.json", 13),
                    ("results_r10_beta_31.json", 31),
                    ("results_r10_beta_Q.json", 0),
                    ("results_r10_alpha_13.json", 13),
                    ("results_r10_alpha_Q.json", 0)):
        path = os.path.join(W30, fn)
        if not os.path.exists(path):
            continue
        d = json.load(open(path))
        if not d.get("best"):
            continue
        K = A.Rat if fld == 0 else A.Modp(fld)
        bl = A.load_point(d["best"]["point"], K)
        unt_p = point_untriggered(tm25, bl, K)
        zb = Counter()
        zc = Counter()
        bz = cz = 0
        for w in unt_p:
            B, C = M.BC_closed(tm25, bl, w, K)
            if K.iszero(B):
                bz += 1
            if K.iszero(C):
                cz += 1
            if K.iszero(B) and K.iszero(C):
                zb[(w[5], w[7])] += 1
            zc[(w[5], w[7])] += 1
        # is B independent of y4?  (the rank-one reduction's prediction)
        byfix = defaultdict(set)
        for w in unt_p:
            B, C = M.BC_closed(tm25, bl, w, K)
            byfix[(w[:4], w[5])].add(K.iszero(B))
        indep = all(len(s) == 1 for s in byfix.values())
        # the reduced scalar system, when A45 is rank one
        red = None
        if A.rank(bl[(4, 5)], K) == 1 and A.rank(bl[(1, 4)], K) == 1:
            sat = tot = 0
            for w in unt_p:
                x = w[:4]
                hl = A.hafL(tm25, bl, w, K)
                lhs = K.add(K.mul(hl, bl[(4, 5)][w[4]][w[5]]),
                            K.mul(bl[(0, 3)][x[0]][x[3]],
                                  K.mul(bl[(1, 4)][x[1]][w[4]],
                                        bl[(2, 5)][x[2]][w[5]])))
                tot += 1
                sat += 1 if K.iszero(lhs) else 0
            red = dict(n_words=tot, n_satisfying_B=sat)
        recs[fn] = dict(
            n_untriggered_point=len(unt_p),
            n_untriggered_template=len(unt_t),
            n_B_zero=bz, n_C_zero=cz, n_Q_zero=sum(zb.values()),
            Q_zero_by_tuple={str(k): v for k, v in sorted(zb.items())},
            B_vanishing_independent_of_y4=indep,
            reduced_system=red,
            rank_A45=A.rank(bl[(4, 5)], K), rank_A47=A.rank(bl[(4, 7)], K),
            rank_A14=A.rank(bl[(1, 4)], K))
        print("[E2 %s] untriggered(point)=%d B=0 at %d, C=0 at %d, both %d; "
              "B-indep-of-y4=%s reduced=%s"
              % (fn, len(unt_p), bz, cz, sum(zb.values()), indep, red),
              flush=True)
    man.record("E2_point_level_escape", dict(records=recs, ok=True))

    # ------------------------------------------------------- E3 Q0 control
    t2 = json.load(open(os.path.join(HERE, "results_t2.json")))
    inst = 0
    viol = 0
    checked = 0
    for r in t2["V2_A11_family"]["records"]:
        if r.get("Qzero_total_template", 0) == 0:
            continue
        K = A.Modp(13) if r["field"] == "F_13" else A.Modp(31)
        bl = A.load_point(r["point"], K)
        checked += 1
        for w in unt_t:
            B, C = M.BC_closed(tm25, bl, w, K)
            if K.iszero(B) and K.iszero(C):
                inst += 1
                if K.iszero(A.hafL(tm25, bl, w, K)):
                    viol += 1
    man.record("E3_Q0_forces_hafL", dict(
        points_checked=checked, Q0_instances=inst, hafL_zero_violations=viol,
        ok=(inst > 0 and viol == 0),
        note="on REAL points that actually carry Q = 0 words: every one has "
             "hafL != 0, as the algebra requires under all-cells-nonzero"))
    print("E3 Q0 instances %d on %d points, hafL=0 violations %d"
          % (inst, checked, viol))

    # -------------------------------------------- E4 coverage at live sets
    cov = {}
    src = [("r10_beta_13", "results_r10_beta_13.json", 13),
           ("r10_alpha_13", "results_r10_alpha_13.json", 13)]
    for tag, fn, fld in src:
        d = json.load(open(os.path.join(W30, fn)))
        K = A.Modp(fld)
        bl = A.load_point(d["best"]["point"], K)
        live = set()
        for (w, Tf, Tc) in A.admissible_cached(25, 'R', 6):
            if not K.iszero(A.hafL(tm25, bl, w, K)):
                live.add((w[5], w[7]))
        cov[tag] = dict(live_tuples=[list(t) for t in sorted(live)],
                        coverage=coverage_for(unt_t, live))
    # A10's Q point 925024
    dq = json.load(open(os.path.join(W30, "points_m25_wide.json")))
    for r in dq["points"]:
        if r["seed"] != 925024:
            continue
        K = A.Rat
        bl = A.load_point(r["point"], K)
        live = set()
        for (w, Tf, Tc) in A.admissible_cached(25, 'R', 6):
            if not K.iszero(A.hafL(tm25, bl, w, K)):
                live.add((w[5], w[7]))
        cov["Q_925024"] = dict(live_tuples=[list(t) for t in sorted(live)],
                               coverage=coverage_for(unt_t, live))
    man.record("E4_coverage_at_real_live_sets", dict(
        per_point=cov, ok=True,
        note="the round-10 forcing needs, at a fixed x1, the escape's word "
             "set to connect all three y4 values for each y5 and each y7"))
    for k, v in cov.items():
        print("E4 %s live tuples %d -> forcing %s"
              % (k, len(v['live_tuples']),
                 {x1: (r['forces_A45'], r['forces_A47'])
                  for x1, r in v['coverage'].items()}))

    # --------------------------------------------- E5 reduced-system control
    # a mutation control: perturb a single cell of A25 at a common-direction
    # point and confirm the reduced system's satisfied-count can move.
    d = json.load(open(os.path.join(W30, "results_r10_beta_13.json")))
    K = A.Modp(13)
    bl = A.load_point(d["best"]["point"], K)
    unt_p = point_untriggered(tm25, bl, K)

    def satcount(b):
        s = 0
        for w in unt_p:
            x = w[:4]
            hl = A.hafL(tm25, b, w, K)
            val = K.add(K.mul(hl, b[(4, 5)][w[4]][w[5]]),
                        K.mul(b[(0, 3)][x[0]][x[3]],
                              K.mul(b[(1, 4)][x[1]][w[4]],
                                    b[(2, 5)][x[2]][w[5]])))
            s += 1 if K.iszero(val) else 0
        return s
    base = satcount(bl)
    moved = 0
    tot = 0
    for a in range(3):
        for b in range(3):
            old = bl[(2, 5)][a][b]
            bl[(2, 5)][a][b] = K.add(old, 1)
            tot += 1
            if satcount(bl) != base:
                moved += 1
            bl[(2, 5)][a][b] = old
    man.record("E5_reduced_system_control", dict(
        base_satisfied=base, n_untriggered=len(unt_p),
        perturbations=tot, n_that_moved_the_count=moved,
        ok=(moved > 0),
        note="the reduced-system counter must respond to the cells it "
             "depends on, else the '0 satisfied' report would be vacuous"))
    print("E5 base satisfied %d/%d ; perturbations moving the count %d/%d"
          % (base, len(unt_p), moved, tot))

    man.finish(os.path.join(HERE, "results_t5.json"),
               extra={"_header": "UNAUDITED A11 follow-up: engine control, "
                                 "point-level escape, residual gap",
                      "elapsed_s": round(time.time() - t0, 1)})
    print("T5 DONE in %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
