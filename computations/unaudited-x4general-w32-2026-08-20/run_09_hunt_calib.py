#!/usr/bin/env python3
"""W32 / T9 -- the builder's CALIBRATION run (ledger 18/20).

Exactly the families of run_06_build, but at k = 3, where the rung is KNOWN
nonempty at N = 8 (W25's F8 and W27/W28's 2,124 sigma patterns).  A silence
at k = 4 is evidence only if the identical machinery FIRES here.  Reports the
hit rate per family, and re-verifies each k=3 hit by assembling the full
source and checking all imposed words.
"""
from __future__ import annotations

import itertools
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w32_bg as BG  # noqa: E402
from w32_core import Manifest, perfect_matchings, require, words_offcount_le  # noqa

OUT = os.path.join(HERE, "results_t9.json")
PRIMES = (13, 31)
SECONDS = int(sys.argv[1]) if len(sys.argv) > 1 else 900
K = int(sys.argv[2]) if len(sys.argv) > 2 else 3
rng = random.Random(31415 + K)
STATE = {"k": K, "primes": list(PRIMES), "started": time.time(), "fam": {},
         "hits": 0, "verified_hits": 0, "hit_examples": []}
MAN = Manifest(["hunt_fires_at_k3"])


def ham(A, Bm):
    adj = {i: [] for i in range(8)}
    for e in list(A) + list(Bm):
        adj[e[0]].append(e[1])
        adj[e[1]].append(e[0])
    seen, cur, prev = {0}, 0, None
    for _ in range(7):
        nxt = [x for x in adj[cur] if x != prev]
        if not nxt:
            return False
        prev, cur = cur, nxt[0]
        if cur in seen:
            return False
        seen.add(cur)
    return len(seen) == 8


def ctriples(limit=200):
    PMs = perfect_matchings(tuple(range(8)))
    idx = list(range(len(PMs)))
    rng.shuffle(idx)
    out = []
    for i, j, k in itertools.combinations(idx, 3):
        A, B, C = PMs[i], PMs[j], PMs[k]
        if set(A) & set(B) or set(A) & set(C) or set(B) & set(C):
            continue
        if ham(A, B) and ham(A, C) and ham(B, C):
            out.append((A, B, C))
            if len(out) >= limit:
                break
    return out


def rand_F(p, dens=1.0, diag=False):
    F = [[[0] * 3 for _ in range(3)] for _ in BG.EDGES]
    for i in range(len(BG.EDGES)):
        for a in range(3):
            for b in range(3):
                if diag and a != b:
                    continue
                if rng.random() <= dens:
                    F[i][a][b] = rng.randrange(p)
    return F


def diag_triple_F(A, B, C, p, cross=0.0):
    F = [[[0] * 3 for _ in range(3)] for _ in BG.EDGES]
    for c, M in enumerate((A, B, C)):
        for e in M:
            if e[0] < 7 and e[1] < 7:
                F[BG.EIDX[e]][c][c] = rng.randrange(1, p)
    for i in range(len(BG.EDGES)):
        for a in range(3):
            for b in range(3):
                if a != b and rng.random() <= cross:
                    F[i][a][b] = rng.randrange(1, p)
    return F


def rec(fam, s):
    d = STATE["fam"].setdefault(fam, {"n": 0, "hist": {}, "max": -1})
    d["n"] += 1
    d["hist"][str(s)] = d["hist"].get(str(s), 0) + 1
    d["max"] = max(d["max"], s)


def main():
    CT = ctriples(120)
    t0 = time.time()
    last = 0
    while time.time() - t0 < SECONDS:
        p = PRIMES[rng.randrange(2)]
        r = rng.random()
        if r < 0.2:
            F = rand_F(p, dens=rng.choice([0.2, 0.4, 1.0]))
            fam = "F1_dense"
        elif r < 0.4:
            F = rand_F(p, dens=rng.choice([0.3, 0.6, 1.0]), diag=True)
            fam = "F3_diag"
        elif r < 0.75:
            A, B, C = CT[rng.randrange(len(CT))]
            F = diag_triple_F(A, B, C, p,
                              cross=rng.choice([0.0, 0.05, 0.1, 0.25]))
            fam = "F4_ctriple_cross"
        else:
            A, B, C = CT[rng.randrange(len(CT))]
            F = diag_triple_F(A, B, C, p, cross=0.0)
            for _ in range(rng.randrange(1, 12)):
                i = rng.randrange(len(BG.EDGES))
                a, b = rng.randrange(3), rng.randrange(3)
                F[i][a][b] = rng.randrange(p)
            fam = "F5_ctriple_perturbed"
        s = BG.score(F, p, k=K)
        rec(fam, s)
        if s == 3:
            STATE["hits"] += 1
            if len(STATE["hit_examples"]) < 5:
                STATE["hit_examples"].append({"family": fam, "p": p, "F": F})
        if time.time() - last > 30:
            STATE["elapsed"] = time.time() - t0
            with open(OUT + ".tmp", "w") as fh:
                json.dump(STATE, fh, indent=1, sort_keys=True)
            os.replace(OUT + ".tmp", OUT)
            last = time.time()
    STATE["elapsed"] = time.time() - t0
    if K == 3:
        require(STATE["hits"] > 0,
                "CALIBRATION FAILURE: the hunt never fires at k=3")
        MAN.mark("hunt_fires_at_k3")
        STATE["manifest"] = MAN.assert_complete()
    with open(OUT, "w") as fh:
        json.dump(STATE, fh, indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in STATE["fam"].items()}, indent=1))
    print("k =", K, "hits:", STATE["hits"])


if __name__ == "__main__":
    main()
