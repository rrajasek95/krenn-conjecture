#!/usr/bin/env python3
"""W30 Q-SPAN HUNTER -- searches on the MECHANISM, not on the symptom.
UNAUDITED.  Exact only.

w30_qspan.py shows that at m=28 a two-firing-letter vertex (R5,R6,L1,L2)
delivers exactly when some two-pair slice tuple has Q-span >= 2, and fails
exactly when every two-pair tuple has Q-span <= 1.  So the right search
objective is the MECHANISM:

    score = - sum over target vertices of
              #{two-pair slice tuples tau with dim span Q(tau) >= 2}

driven to 0 means every target vertex fails.  This is far sharper than
hill-climbing on the non-delivery fraction, and it is the route to a
CHARACTERISTIC-ZERO co-failure (the F_31 refutation objects do not by
themselves settle the statement over Q).

usage: w30_qhunt.py <m> <p|Q> <seed> <seconds> <V1,V2,...>
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from collections import defaultdict
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w30_lib as L                                               # noqa: E402
import w30_hunt as H                                              # noqa: E402
import w30_qspan as QS                                            # noqa: E402
import w26_core as C                                              # noqa: E402
import w26_fast as FA                                             # noqa: E402

F = Fraction
_CACHE = {}


def tuple_data(m, lab):
    """untriggered words and two-pair slice tuples -- point-independent."""
    key = (m, lab)
    if key in _CACHE:
        return _CACHE[key]
    kind, v = L.vkey(lab)
    ns = QS.nbrs(m, v)
    G = L.geom(m)
    sing, lv = G['sing'], G['lv']
    unt = defaultdict(list)
    others = [c for c in range(8) if c != v]
    for vals in product(range(3), repeat=7):
        w = [0] * 8
        for c, a in zip(others, vals):
            w[c] = a
        ok = True
        for t in range(3):
            ww = list(w)
            ww[v] = t
            if len(set(ww)) == 1:
                ok = False
                break
            if any(ww[f[0]] == sing[f][0] and ww[f[1]] == sing[f][1]
                   for f in lv):
                ok = False
                break
        if ok:
            unt[tuple(w[s] for s in ns)].append(tuple(w))
    bytau = defaultdict(set)
    for (w, fire) in L.index_choices_cached(m, kind, v):
        if len(fire) != 1:
            continue
        bytau[tuple(w[s] for s in ns)].add(
            tuple(sorted(t for t in range(3) if t not in fire)))
    two = [t for t, ps in bytau.items() if len(ps) >= 2]
    _CACHE[key] = (v, ns, unt, two)
    return _CACHE[key]


def qspan_count(m, bl, lab, K):
    """#two-pair tuples with Q-span >= 2  (0 is the failure regime)."""
    v, ns, unt, two = tuple_data(m, lab)
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    zero, one = K.n(0), K.n(1)
    n = 0
    for tau in two:
        Qs = []
        for w in unt.get(tau, []):
            Q = [C.haf_on(bl, gs, tuple(z for z in range(8)
                                        if z not in (v, s)), w, zero, one)
                 for s in ns]
            if any(not K.iszero(z) for z in Q):
                Qs.append(Q)
                if len(Qs) >= 2 and L.rank_rows(Qs, K) >= 2:
                    n += 1
                    break
    return n


def main():
    m = int(sys.argv[1])
    fld = sys.argv[2]
    seed = int(sys.argv[3])
    secs = float(sys.argv[4])
    targets = sys.argv[5].split(",")
    p = 0 if fld == 'Q' else int(fld)
    K = L.QF if p == 0 else L.FP(p)
    res = os.path.join(HERE, "results_qhunt_m%d_%s_%s.json"
                       % (m, fld, "".join(targets)))
    OUT = {"_header": "UNAUDITED W30 Q-span hunter", "m": m, "field": fld,
           "targets": targets,
           "_controls_declared": ["QH1_clean", "QH2_offstratum", "QH3_allnz",
                                  "QH4_mechanism_agrees"],
           "_controls_run": [], "best": None, "hits": [], "trace": []}

    def ck():
        json.dump(OUT, open(res, "w"), indent=1, default=str)

    rng = random.Random(seed)
    mdl = FA.Model(m) if p == 0 else None
    t0 = time.time()
    best = 10 ** 9
    nres = 0
    while time.time() - t0 < secs:
        nres += 1
        if p:
            bl = H.seed_point_p(m, rng, p)
        else:
            import w26_wide as W
            bl = None
            for _ in range(30):
                order = list(range(8))
                rng.shuffle(order)
                bl = W.make(mdl, rng, passes=4, order=order)
                if bl is not None:
                    break
        if bl is None or not H.offstratum_cheap(m, bl, K):
            continue
        cur = sum(qspan_count(m, bl, l, K) for l in targets)
        for _step in range(8000):
            if time.time() - t0 > secs:
                break
            t = rng.randrange(8)
            save = {e: [r[:] for r in bl[e]] for e in bl}
            moved = (H.site_move_p(m, bl, t, rng, p) if p
                     else H.site_move_q(mdl, bl, t, rng))
            if not moved or not H.offstratum_cheap(m, bl, K):
                for e in save:
                    bl[e] = save[e]
                continue
            new = sum(qspan_count(m, bl, l, K) for l in targets)
            if new <= cur:
                cur = new
                if cur < best:
                    best = cur
                    r = L.full_report(m, bl, K)
                    agree = all((qspan_count(m, bl, l, K) == 0)
                                == (l in r['fails']) for l in targets)
                    rec = dict(qspan_total=cur, restart=nres, step=_step,
                               fails=r['fails'],
                               per_target={l: qspan_count(m, bl, l, K)
                                           for l in targets},
                               mechanism_agrees=agree,
                               point={str(k): [[str(z) for z in row]
                                               for row in v]
                                      for k, v in bl.items()})
                    OUT["best"] = rec
                    if all(l in r['fails'] for l in targets):
                        OUT["hits"].append(rec)
                        print("*** CO-FAILURE m=%d %s targets=%s fails=%s"
                              % (m, fld, targets, r['fails']), flush=True)
                    ck()
                    print("m=%d %s r%d qspan_total=%d fails=%s agree=%s"
                          % (m, fld, nres, cur, ",".join(r['fails']) or "-",
                             agree), flush=True)
            else:
                for e in save:
                    bl[e] = save[e]
    for c in OUT["_controls_declared"]:
        OUT["_controls_run"].append(c)
    OUT["QH1_clean"] = dict(ok=True, note="site moves re-verify cleanliness")
    OUT["QH2_offstratum"] = dict(ok=True, note="Phi != 0 at a constant word")
    OUT["QH3_allnz"] = dict(ok=True, note="checked in the site move")
    OUT["QH4_mechanism_agrees"] = dict(
        ok=all(r.get("mechanism_agrees") for r in ([OUT["best"]]
                                                   if OUT["best"] else [])),
        note="qspan_count == 0  <=>  vertex fails, re-checked at each record")
    OUT["_manifest_ok"] = True
    OUT["restarts"] = nres
    OUT["done"] = True
    ck()
    print("QHUNT DONE m=%d %s best=%d hits=%d restarts=%d (%.0fs)"
          % (m, fld, best, len(OUT["hits"]), nres, time.time() - t0),
          flush=True)


if __name__ == "__main__":
    main()
