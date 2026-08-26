#!/usr/bin/env python3
"""ADVERSARIAL W24 -- routes 1/2/3/5: hunt for a point whose residual linear
system is CONSISTENT with all twelve z_e nonzero.

SCORE(point) = number of singles e whose SOLO rows all give one and the SAME
NONZERO ratio  z_e = -Phi_w / c_e(w).   SCORE = 12 is necessary (not
sufficient -- the mixed rows must also agree) for a survivor.
A single with a unique ratio 0 is FORCED-DEAD; a single with >=2 distinct
ratios makes the system INCONSISTENT.

Seeds: (a) own random descent, (b) the stored W20/W21/A7 exact points,
(c) Q(omega) and Q(i) descents, (d) deliberately-factoring rank-one starts.
EXACT only.  UNAUDITED.
"""
from __future__ import annotations

import glob
import json
import os
import random
import sys
import time
from fractions import Fraction

sys.dont_write_bytecode = True
W24 = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-residualkill-w24-2026-08-15"
sys.path.insert(0, W24)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w24_core as C                                              # noqa: E402
import w24_pts as P                                               # noqa: E402
import w24_resid as RS                                            # noqa: E402
import adv_field as F                                             # noqa: E402
import adv_probe as PR                                            # noqa: E402


def score_point(m, bl, one=Fraction(1), zero=Fraction(0)):
    """returns (score, per-single record, full verdict-ish info)."""
    T = C.TEMPLATES[m]
    gam_set = set(C.gamma_edges(T))
    rows_sk, cleanw, cells, live = RS.row_skeleton(m)
    idx = {e: i for i, e in enumerate(cells)}
    n = len(cells)
    allv = tuple(range(8))
    rows = []
    for w, ones in rows_sk:
        v = [zero] * n
        for e in ones:
            rest = tuple(x for x in allv if x not in e)
            v[idx[e]] = F.haf_gen(bl, gam_set, rest, w, one, zero)
        c = F.haf_gen(bl, gam_set, allv, w, one, zero)
        if any(bool(x) for x in v) or c:
            rows.append((w, v, c))
    per = {}
    for w, v, c in rows:
        nz = [i for i in range(n) if v[i]]
        if len(nz) != 1:
            continue
        e = cells[nz[0]]
        per.setdefault(e, set()).add(c / v[nz[0]] * -1)
    rec, score = {}, 0
    for e in cells:
        s = per.get(e)
        if s is None:
            rec[str(e)] = "no-solo-rows(free)"
            score += 1                     # vacuously survivable
        elif len(s) > 1:
            rec[str(e)] = "MULTI(%d)" % len(s)
        elif not list(s)[0]:
            rec[str(e)] = "ZERO"
        else:
            rec[str(e)] = "OK:" + str(list(s)[0])
            score += 1
    # full system
    aug = [list(v) + [-c] for _, v, c in rows]
    R, piv = F.rref_gen(aug, n + 1, zero, one)
    incons = n in piv
    forced = []
    if not incons:
        sol = [zero] * n
        for i, pc in enumerate(piv):
            if pc < n:
                sol[pc] = R[i][n]
        ker = F.kernel_gen([list(v) for _, v, _ in rows], n, zero, one)
        forced = [str(cells[i]) for i in range(n)
                  if not sol[i] and all(not b[i] for b in ker)]
    return score, rec, dict(n_rows=len(rows), rank=len(piv),
                            inconsistent=incons, forced=forced)


def dump(bl):
    return {str(e): [[str(x) for x in r] for r in bl[e]] for e in bl}


def main():
    t0 = time.time()
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 700.0
    out = {"_header": "ADVERSARIAL W24 hunt. UNAUDITED, exact only.",
           "best": {}, "runs": []}
    best = {}

    def consider(m, tag, bl, cls=None):
        one = Fraction(1) if cls is None else cls(1, 0)
        zero = Fraction(0) if cls is None else cls(0, 0)
        gam = C.gamma_edges(C.TEMPLATES[m])
        gs = set(gam)
        if not all(bl[e][i][j] for e in gam for i in range(3)
                   for j in range(3)):
            return None
        allv = tuple(range(8))
        cv = sum(1 for w in P.w21_clean(m)
                 if F.haf_gen(bl, gs, allv, w, one, zero))
        if cv:
            return None
        sc, rec, info = score_point(m, bl, one, zero)
        nphi = sum(1 for w in C.WORDS if F.haf_gen(bl, gs, allv, w, one, zero))
        r = dict(m=m, tag=tag, score=sc, nphi=nphi,
                 regime=("A" if nphi == 0 else "B"), **info)
        out["runs"].append(r)
        print("m=%d %-26s SCORE=%2d/12 reg=%s incons=%-5s forced=%2d "
              "nphi=%4d" % (m, tag[:26], sc, r["regime"], info["inconsistent"],
                            len(info["forced"]), nphi), flush=True)
        k = m
        if k not in best or sc > best[k][0]:
            best[k] = (sc, r, rec, dump(bl))
        if sc == 12 and not info["inconsistent"] and not info["forced"]:
            print("*** SURVIVOR *** m=%d %s" % (m, tag), flush=True)
            out.setdefault("SURVIVORS", []).append(
                dict(m=m, tag=tag, point=dump(bl), rec=rec, info=info))
        return r

    # ---------------------------------------------------- (b) stored points
    for (m, tag, bl) in P.stored_points():
        consider(m, "stored:" + tag, bl)
        if time.time() - t0 > budget * .25:
            break

    # ------------------------------------------------ (a) own descents (Q)
    seed = 0
    while time.time() - t0 < budget * .6:
        seed += 1
        for m in (28, 27, 26, 25):
            rng = random.Random(50000 + 97 * seed + m)
            order = list(range(8))
            rng.shuffle(order)
            lo, hi = rng.choice([(-7, 7), (-2, 2), (-1, 1), (-20, 20)])
            try:
                bl, _ = P.descent(m, rng, order=order, passes=3, lo=lo, hi=hi)
            except Exception:
                continue
            if bl is None:
                continue
            consider(m, "descentQ s=%d" % seed, bl)
            if time.time() - t0 > budget * .6:
                break

    # ------------------------------------- (c) Q(omega) and Q(i) descents
    for cls, nm in ((F.Om, "Qw"), (F.Gi, "Qi")):
        s = 0
        while time.time() - t0 < budget * (.8 if nm == "Qw" else 1.0):
            s += 1
            for m in (28, 26):
                rng = random.Random(900 + 13 * s + m)
                order = list(range(8))
                rng.shuffle(order)
                try:
                    bl, _ = descent_field(m, rng, cls, order)
                except Exception as ex:
                    print("  %s descent m=%d failed: %r" % (nm, m, ex),
                          flush=True)
                    continue
                if bl is None:
                    continue
                consider(m, "%s s=%d" % (nm, s), bl, cls)
                if time.time() - t0 > budget:
                    break

    out["best"] = {str(k): dict(score=v[0], rec=v[1], per_single=v[2],
                                point=v[3]) for k, v in best.items()}
    json.dump(out, open(os.path.join(HERE, "results_hunt.json"), "w"),
              indent=1, default=str)
    print("BEST SCORES", {k: v[0] for k, v in best.items()}, flush=True)


def descent_field(m, rng, cls, order):
    return PR.descent_gen(m, rng, cls, order=order, passes=3)


if __name__ == "__main__":
    main()
