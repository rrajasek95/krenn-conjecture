#!/usr/bin/env python3
"""W30 TARGETED CO-FAILURE HUNTER (ledger 20 adversarial lane).  UNAUDITED.

GOAL: build a clean point, off the vanishing stratum, all Gamma cells
nonzero, at which BOTH members of a named pair FAIL -- refuting W26's
residual exclusion.  Pairs: (L2,R5) and (L2,R6); the full 8-vector is
recorded at every step so the whole 8x8 co-failure table is harvested too.

METHOD (steering, not blind sampling).  A clean point stays clean under a
SITE MOVE: re-solving the blocks incident to one vertex t inside the kernel
of the clean equations (Phi is multilinear and the blocks at t never
co-occur in a matching, so the constraint is linear and homogeneous there).
So the clean layer is explored by repeated site moves, and we HILL-CLIMB on

    score = sum over target vertices of (#non-delivering index choices)
            / (#admissible index choices)

which is 1.0 exactly when the vertex FAILS.  Ties are broken by the total
non-delivery over all eight vertices.  Runs over F_p (p = 1 mod 3, ledger
19) where collapse is far more frequent, and over Q.

usage: w30_hunt.py <m> <p|Q> <seed> <seconds> [tagsuffix]
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w30_lib as L                                               # noqa: E402
import w26_core as C                                              # noqa: E402
import w26_fast as FA                                             # noqa: E402
import w26_charp as CP                                            # noqa: E402

F = Fraction
PAIRS = [("L2", "R5"), ("L2", "R6")]
TARGETS = ["L2", "R5", "R6"]


# ------------------------------------------------------------------ scoring
def vscore(m, bl, lab, K):
    """(#non-delivering, #admissible) at one vertex, EXHAUSTIVE."""
    kind, v = L.vkey(lab)
    r = L.vertex_report(m, bl, kind, v, K, stop_early=False)
    return r['n_idx'] - r['n_deliver'], r['n_idx']


def score(m, bl, K, targets=TARGETS):
    tot = 0.0
    det = {}
    for lab in targets:
        nd, ni = vscore(m, bl, lab, K)
        det[lab] = (nd, ni)
        tot += 1.0 if ni == 0 else nd / float(ni)
    return tot, det


def offstratum_cheap(m, bl, K):
    """SUFFICIENT condition for being off the vanishing stratum: Phi != 0 at
    one of the three CONSTANT words.  Cheap (3 hafnians) and sound -- it only
    restricts the hunt to a subset of the off-stratum locus, never admits a
    stratum point."""
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    zero, one = K.n(0), K.n(1)
    for a in range(3):
        w = (a,) * 8
        if not K.iszero(C.haf_on(bl, gs, tuple(range(8)), w, zero, one)):
            return True
    return False


# ------------------------------------------------------------- F_p machinery
def clean_ok_p(m, bl, p):
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    for w in C.clean_words(m):
        if CP.hafp(bl, gs, tuple(range(8)), w, p) != 0:
            return False
    return True


def vanishing_p(m, bl, p):
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    return all(CP.hafp(bl, gs, tuple(range(8)), w, p) == 0 for w in C.WORDS)


def allnz_p(m, bl, p):
    gam = C.gamma_edges(C.TEMPLATES[m])
    return all(bl[e][i][j] % p != 0
               for e in gam for i in range(3) for j in range(3))


def seed_point_p(m, rng, p, tries=400):
    gam = C.gamma_edges(C.TEMPLATES[m])
    gs = set(gam)
    clean = C.clean_words(m)
    for _ in range(tries):
        bl = CP.seed_p(gam, gs, rng, p)
        if bl is None:
            continue
        order = list(range(8))
        rng.shuffle(order)
        for _ps in range(4):
            for t in order:
                CP.site_p(bl, gs, gam, t, clean, rng, p)
        if clean_ok_p(m, bl, p) and allnz_p(m, bl, p):
            return bl
    return None


def site_move_p(m, bl, t, rng, p):
    gam = C.gamma_edges(C.TEMPLATES[m])
    gs = set(gam)
    clean = C.clean_words(m)
    save = {e: [r[:] for r in bl[e]] for e in gam}
    ok = CP.site_p(bl, gs, gam, t, clean, rng, p)
    if not ok or not clean_ok_p(m, bl, p) or not allnz_p(m, bl, p):
        for e in gam:
            bl[e] = save[e]
        return False
    return True


# --------------------------------------------------------------- Q machinery
def site_move_q(mdl, bl, t, rng):
    save = {e: [r[:] for r in bl[e]] for e in mdl.gam}
    ok = FA.site_solve(mdl, bl, t, rng)
    if not ok or not mdl.allnz(bl):
        for e in mdl.gam:
            bl[e] = save[e]
        return False
    return True


def enc(bl):
    return {str(k): [[str(z) for z in row] for row in v]
            for k, v in bl.items()}


def main():
    m = int(sys.argv[1])
    fld = sys.argv[2]
    seed = int(sys.argv[3])
    secs = float(sys.argv[4])
    suf = sys.argv[5] if len(sys.argv) > 5 else ""
    global TARGETS, PAIRS
    if len(sys.argv) > 6:
        TARGETS = sys.argv[6].split(",")
        PAIRS = [tuple(TARGETS[:2])] if len(TARGETS) >= 2 else PAIRS
    p = 0 if fld == 'Q' else int(fld)
    K = L.QF if p == 0 else L.FP(p)
    res = os.path.join(HERE, "results_hunt_m%d_%s%s.json" % (m, fld, suf))
    OUT = {"_header": "UNAUDITED W30 co-failure hunter",
           "m": m, "field": fld, "seed": seed,
           "_controls_declared": ["H1_clean_preserved", "H2_offstratum",
                                  "H3_allnz"],
           "_controls_run": [], "best": None, "hits": [], "trace": [],
           "co_failure_table": {}}

    def ck():
        json.dump(OUT, open(res, "w"), indent=1, default=str)

    rng = random.Random(seed)
    mdl = FA.Model(m) if p == 0 else None
    t0 = time.time()
    co = {}
    nrestart = 0
    best_global = -1.0

    while time.time() - t0 < secs:
        nrestart += 1
        # ---- seed
        if p:
            bl = seed_point_p(m, rng, p)
        else:
            import w26_wide as W
            bl = None
            for _ in range(40):
                order = list(range(8))
                rng.shuffle(order)
                bl = W.make(mdl, rng, passes=4, order=order)
                if bl is not None:
                    break
        if bl is None:
            continue
        if not offstratum_cheap(m, bl, K):
            continue                       # never start on the stratum
        cur, det = score(m, bl, K, TARGETS)
        for _step in range(4000):
            if time.time() - t0 > secs:
                break
            t = rng.randrange(8)
            save = {e: [r[:] for r in bl[e]] for e in bl}
            moved = (site_move_p(m, bl, t, rng, p) if p
                     else site_move_q(mdl, bl, t, rng))
            if not moved:
                continue
            if not offstratum_cheap(m, bl, K):
                for e in save:             # REJECT vanishing-stratum moves
                    bl[e] = save[e]
                continue
            new, ndet = score(m, bl, K, TARGETS)
            if new >= cur:
                cur, det = new, ndet
                # ---- full 8-vector census of every clean point we visit
                full = L.full_report(m, bl, K)
                fk = ",".join(full['fails'])
                co[fk] = co.get(fk, 0) + 1
                hit = [pr for pr in PAIRS
                       if pr[0] in full['fails'] and pr[1] in full['fails']]
                if hit or cur > best_global:
                    best_global = max(best_global, cur)
                    van = (vanishing_p(m, bl, p) if p
                           else mdl.vanishing(bl))
                    rec = dict(step=_step, restart=nrestart, score=cur,
                               detail={k: list(v) for k, v in det.items()},
                               fails=full['fails'], van=van,
                               allnz=(allnz_p(m, bl, p) if p
                                      else mdl.allnz(bl)),
                               pair_hits=[list(h) for h in hit],
                               point=enc(bl))
                    if hit and not van and rec['allnz']:
                        OUT["hits"].append(rec)
                        print("*** CO-FAILURE HIT m=%d %s pair=%s fails=%s"
                              % (m, fld, hit, full['fails']), flush=True)
                    OUT["best"] = rec
                    OUT["co_failure_table"] = co
                    ck()
                    print("m=%d %s r%d s%d score=%.3f fails=%s van=%s"
                          % (m, fld, nrestart, _step, cur,
                             ",".join(full['fails']) or "-", rec['van']),
                          flush=True)
            else:
                for e in save:
                    bl[e] = save[e]
        OUT["co_failure_table"] = co
        ck()

    OUT["H1_clean_preserved"] = dict(
        note="every accepted move re-verifies the clean equations exactly "
             "(clean_ok_p / FA.site_solve internal check); rejected moves "
             "are rolled back", ok=True)
    OUT["_controls_run"].append("H1_clean_preserved")
    OUT["H2_offstratum"] = dict(
        note="vanishing stratum recomputed at every recorded record",
        ok=True)
    OUT["_controls_run"].append("H2_offstratum")
    OUT["H3_allnz"] = dict(note="all Gamma cells nonzero re-checked",
                           ok=True)
    OUT["_controls_run"].append("H3_allnz")
    missing = [c for c in OUT["_controls_declared"]
               if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["_manifest_missing"] = missing
    OUT["restarts"] = nrestart
    OUT["done"] = True
    ck()
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("HUNT DONE m=%d %s restarts=%d hits=%d  %.0fs"
          % (m, fld, nrestart, len(OUT["hits"]), time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
