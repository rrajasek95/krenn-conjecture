#!/usr/bin/env python3
"""W32 / T15 -- CROSS-TYPE STRATIFICATION, properly seeded.

REPLACES run_07's cell-type sweep, which its own control condemned: that
sweep drew backgrounds uniformly at random inside each cell-type stratum and
reached rung 0 in ALL 421 strata swept -- INCLUDING the diagonal stratum,
which is known to carry X_3 (F8, and the (C)-triples of run_03/CAL2).  A
sampler that cannot reach the rung in a stratum known to carry it measures
nothing (ledger 18; ledger 27: the pre-launch control must test the exact
target).  Recorded as a negative about the METHOD, not about the strata.

Corrected design: seed from the structures that DO carry the rung -- a
diagonal (C)-triple core with symbolic-free weights -- and stratify by which
of the six CROSS cell types (a,b), a != b, may be switched on.  Built-in
control: the m = 0 (empty cross-type set) stratum MUST reach rung 3.
"""
import itertools, json, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w32_bg as BG
from w32_core import perfect_matchings, require

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "results_t15.json")
SEC = int(sys.argv[1]) if len(sys.argv) > 1 else 3600
rng = random.Random(151515)
XT = [(a, b) for a in range(3) for b in range(3) if a != b]


def ham(A, B):
    adj = {i: [] for i in range(8)}
    for e in list(A) + list(B):
        adj[e[0]].append(e[1]); adj[e[1]].append(e[0])
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


PMs = perfect_matchings(tuple(range(8)))
idx = list(range(len(PMs))); rng.shuffle(idx)
CT = []
for i, j, k in itertools.combinations(idx, 3):
    A, B, C = PMs[i], PMs[j], PMs[k]
    if set(A) & set(B) or set(A) & set(C) or set(B) & set(C):
        continue
    if ham(A, B) and ham(A, C) and ham(B, C):
        CT.append((A, B, C))
        if len(CT) >= 120:
            break


def build(p, types, ncross):
    A, B, C = CT[rng.randrange(len(CT))]
    F = [[[0] * 3 for _ in range(3)] for _ in BG.EDGES]
    for c, M in enumerate((A, B, C)):
        for e in M:
            if e[0] < 7 and e[1] < 7:
                F[BG.EIDX[e]][c][c] = rng.randrange(1, p)
    placed = 0
    tries = 0
    while placed < ncross and tries < 60 and types:
        tries += 1
        i = rng.randrange(len(BG.EDGES))
        a, b = types[rng.randrange(len(types))]
        if F[i][a][b] == 0:
            F[i][a][b] = rng.randrange(1, p)
            placed += 1
    return F, placed


def rung(F, p):
    r = 0
    for k in (2, 3, 4):
        if BG.score(F, p, k=k) == 3:
            r = k
        else:
            break
    return r


S = {"strata": {}, "control_m0_rung": None, "k4_hits": [], "n_ctriples": len(CT)}
# CONTROL first: the diagonal core alone must reach rung 3
best0 = 0
for _ in range(60):
    p = rng.choice([13, 31])
    F, _ = build(p, [], 0)
    best0 = max(best0, rung(F, p))
S["control_m0_rung"] = best0
require(best0 >= 3, f"CONTROL FAILED: the (C)-triple core reaches only rung "
                    f"{best0}; the sampler measures nothing")
print("control: diagonal (C)-triple core reaches rung", best0)

subs = [tuple(XT[i] for i in range(6) if (m >> i) & 1) for m in range(1, 64)]
t0 = time.time(); last = 0
rounds = 0
while time.time() - t0 < SEC:
    rounds += 1
    for T in subs:
        if time.time() - t0 > SEC:
            break
        key = "|".join(f"{a}{b}" for a, b in T)
        d = S["strata"].setdefault(key, {"n": 0, "rung_hist": {}, "best": 0,
                                         "best_k4": 0, "size": len(T)})
        for _ in range(3):
            p = rng.choice([13, 31])
            nc = rng.randrange(1, 9)
            F, placed = build(p, list(T), nc)
            r = rung(F, p)
            s4 = BG.score(F, p, k=4)
            d["n"] += 1
            d["rung_hist"][str(r)] = d["rung_hist"].get(str(r), 0) + 1
            d["best"] = max(d["best"], r)
            d["best_k4"] = max(d["best_k4"], s4)
            if s4 == 3:
                S["k4_hits"].append({"types": key, "p": p, "F": F})
    if time.time() - last > 30:
        S["elapsed"] = time.time() - t0
        S["rounds"] = rounds
        with open(OUT + ".tmp", "w") as fh:
            json.dump(S, fh, indent=1, sort_keys=True)
        os.replace(OUT + ".tmp", OUT)
        last = time.time()
S["elapsed"] = time.time() - t0
S["rounds"] = rounds
with open(OUT, "w") as fh:
    json.dump(S, fh, indent=1, sort_keys=True)
print("strata:", len(S["strata"]), "rounds:", rounds,
      "k4 hits:", len(S["k4_hits"]))
print("best rung by stratum size:",
      {k: (v["best"], v["best_k4"]) for k, v in
       sorted(S["strata"].items(), key=lambda x: -x[1]["best"])[:10]})
