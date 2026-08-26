#!/usr/bin/env python3
r"""UNAUDITED PROBE (W19-CENSUS) -- non-emptiness decision for every Gamma.

UNAUDITED.  Nothing here is a proved claim of the repository.
Exact integer arithmetic only (numpy int64 bit masks + Python int).

For each of the 794 admissible Gamma iso-classes:
  * if |F(Gamma)| >= 3 the thickness shortcut says EVERY (SC)-admissible
    completion is in (R); we still BUILD one and check it exactly
    (explicit-point control, 719 times);
  * if |F(Gamma)| <= 2 we search the space of MAXIMAL configurations
    (server selection + dead cells; see the monotone reduction in
    w19c_low.py) by hill-climbing on the number of bad words.

A "server selection" assigns to each of the 24 demands (p,r) an incident
NON-Gamma edge, with the three demands at a vertex going to three distinct
edges.  The mask of an edge is then forced to be the LARGEST compatible one:
   both endpoints select it -> the single cell;
   one endpoint selects it  -> that full column / full row;
   neither                  -> FULL minus one (free) cell.
By the monotone reduction, (R) has a member with this Gamma IFF some such
configuration is in (R).
"""
from __future__ import annotations

import json
import os
import random
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w19c_lib import (  # noqa: E402
    EDGES, EIDX, N, NE, FULL, MIXED_POS, CONST_POS, in_R, fast_in_R,
    fibres_all_words, fast_audit, mask_to_edges, my_sc_ok, spanning_2conn,
    my_npm_graph, canon_mask,
)

HERE = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(20260815)

COL = [(1 | 8 | 64) << j for j in range(3)]     # full column j
ROW = [7 << (3 * i) for i in range(3)]          # full row i


class Inst:
    def __init__(self, gamma_mask):
        self.gam = gamma_mask
        self.free = [ei for ei in range(NE) if not (gamma_mask >> ei) & 1]
        self.inc = {p: [ei for ei in self.free if p in EDGES[ei]]
                    for p in range(N)}
        self.ok = all(len(self.inc[p]) >= 3 for p in range(N))

    def build(self, server, dead):
        req = {}
        for (p, r), ei in server.items():
            req.setdefault(ei, {})[p] = r
        T = [0] * NE
        for ei in range(NE):
            if (self.gam >> ei) & 1:
                T[ei] = FULL
        for ei in self.free:
            u, v = EDGES[ei]
            rq = req.get(ei, {})
            au = rq.get(u)
            av = rq.get(v)
            if au is not None and av is not None:
                T[ei] = 1 << (3 * av + au)
            elif au is not None:
                T[ei] = COL[au]
            elif av is not None:
                T[ei] = ROW[av]
            else:
                T[ei] = FULL ^ (1 << dead[ei])
        return T

    def rand_state(self):
        server = {}
        for p in range(N):
            es = rng.sample(self.inc[p], 3)
            cols = [0, 1, 2]
            rng.shuffle(cols)
            for r, ei in zip(cols, es):
                server[(p, r)] = ei
        dead = {ei: rng.randrange(9) for ei in self.free}
        return server, dead


def nbad(T):
    f = fibres_all_words(T)
    return (int((f[MIXED_POS] < 3).sum()) + int((f[CONST_POS] < 1).sum()))


def search(inst, budget=6000, restarts=8, seed_states=()):
    best = (10 ** 9, None, None)
    states = list(seed_states)
    for _ in range(restarts):
        states.append(inst.rand_state())
    used = 0
    for server0, dead0 in states:
        server = dict(server0)
        dead = dict(dead0)
        cur = nbad(inst.build(server, dead))
        used += 1
        if cur < best[0]:
            best = (cur, dict(server), dict(dead))
        if cur == 0:
            return best, used
        stall = 0
        while used < budget and stall < 900:
            if rng.random() < 0.5:
                p = rng.randrange(N)
                r = rng.randrange(3)
                others = {server[(p, rr)] for rr in range(3) if rr != r}
                cand = [e for e in inst.inc[p] if e not in others]
                if len(cand) < 2:
                    continue
                old = server[(p, r)]
                new = rng.choice(cand)
                if new == old:
                    continue
                server[(p, r)] = new
                v = nbad(inst.build(server, dead))
                used += 1
                if v <= cur:
                    if v < cur:
                        stall = 0
                    else:
                        stall += 1
                    cur = v
                else:
                    server[(p, r)] = old
                    stall += 1
            else:
                ei = rng.choice(inst.free)
                old = dead[ei]
                new = rng.randrange(9)
                if new == old:
                    continue
                dead[ei] = new
                v = nbad(inst.build(server, dead))
                used += 1
                if v <= cur:
                    if v < cur:
                        stall = 0
                    else:
                        stall += 1
                    cur = v
                else:
                    dead[ei] = old
                    stall += 1
            if cur < best[0]:
                best = (cur, dict(server), dict(dead))
            if cur == 0:
                return best, used
        if used >= budget:
            break
    return best, used


def main():
    G = json.load(open(os.path.join(HERE, "results_gamma.json")))
    rows = G["gamma_classes"]
    out = []
    t0 = time.time()
    nonempty_high = 0
    fail_high = []
    for idx, r in enumerate(rows):
        gm = r["mask"]
        inst = Inst(gm)
        assert inst.ok, ("Gamma with a vertex of degree > 4 slipped through",
                         r["edges"])
        if r["pms"] >= 3:
            # thickness shortcut: any (SC)-completion works.  Build one and
            # CHECK it (explicit-point control, run for all 719 classes).
            server, dead = inst.rand_state()
            T = inst.build(server, dead)
            good = fast_in_R(T)
            if good:
                nonempty_high += 1
            else:
                fail_high.append(r["edges"])
            out.append(dict(mask=gm, n_edges=r["n_edges"], pms=r["pms"],
                            nonempty=bool(good), how="thickness",
                            template=[int(x) for x in T] if good else None))
        else:
            (bb, server, dead), used = search(inst)
            T = inst.build(server, dead) if server else None
            good = bool(T is not None and fast_in_R(T))
            out.append(dict(mask=gm, n_edges=r["n_edges"], pms=r["pms"],
                            nonempty=good, how="search", best_bad=bb,
                            evals=used,
                            template=[int(x) for x in T] if good else None))
            print("  lowF |E|=%2d |F|=%d  bad=%-5d %s  (%.0fs)"
                  % (r["n_edges"], r["pms"], bb, "IN (R)" if good else "----",
                     time.time() - t0), flush=True)
    RES = dict(n_classes=len(out),
               high_pm_nonempty=nonempty_high,
               high_pm_failures=fail_high,
               low=[o for o in out if o["pms"] < 3],
               all_nonempty=all(o["nonempty"] for o in out),
               n_nonempty=sum(1 for o in out if o["nonempty"]))
    # keep one representative template per Gamma class
    RES["reps"] = {str(o["mask"]): o["template"] for o in out if o["template"]}
    json.dump(RES, open(os.path.join(HERE, "results_decide.json"), "w"))
    print("\nGamma classes: %d ; non-empty: %d ; |F|>=3 checked-nonempty: %d"
          % (len(out), RES["n_nonempty"], nonempty_high))
    print("classes with NO member found:",
          [(o["n_edges"], o["pms"], o["best_bad"])
           for o in out if not o["nonempty"]])


if __name__ == "__main__":
    main()
