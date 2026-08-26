#!/usr/bin/env python3
"""W32 / T12 -- reach of the hunt on backgrounds that genuinely carry CROSS
cells (the general, non-diagonal directions), at k = 3 (calibration) and
k = 4 (target).  W25's F8 -- a real N=8 X_3 source -- has 12 cross cells, so
the non-diagonal directions demonstrably carry the penultimate rung."""
import itertools, json, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w32_bg as BG
from w32_core import perfect_matchings

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "results_t12.json")
SEC = int(sys.argv[1]) if len(sys.argv) > 1 else 2400
rng = random.Random(5150)


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
        if len(CT) >= 80:
            break
S = {"tried": 0, "by_ncross": {}, "k3_hits": 0, "k3_hits_with_cross": 0,
     "k4_max": 0, "k4_score_hist": {}, "maxcross_at_k3_hit": 0,
     "n_ctriples": len(CT)}
t0 = time.time(); last = 0
while time.time() - t0 < SEC:
    p = rng.choice([13, 31])
    A, B, C = CT[rng.randrange(len(CT))]
    F = [[[0] * 3 for _ in range(3)] for _ in BG.EDGES]
    for c, M in enumerate((A, B, C)):
        for e in M:
            if e[0] < 7 and e[1] < 7:
                F[BG.EIDX[e]][c][c] = rng.randrange(1, p)
    for _ in range(rng.randrange(1, 9)):
        i = rng.randrange(len(BG.EDGES)); a = rng.randrange(3); b = rng.randrange(3)
        if a != b:
            F[i][a][b] = rng.randrange(1, p)
    nc = sum(1 for blk in F for a in range(3) for b in range(3)
             if a != b and blk[a][b])
    S["tried"] += 1
    s3 = BG.score(F, p, k=3); s4 = BG.score(F, p, k=4)
    S["k4_max"] = max(S["k4_max"], s4)
    S["k4_score_hist"][str(s4)] = S["k4_score_hist"].get(str(s4), 0) + 1
    d = S["by_ncross"].setdefault(str(nc), {"n": 0, "k3": 0, "k4max": 0})
    d["n"] += 1; d["k4max"] = max(d["k4max"], s4)
    if s3 == 3:
        S["k3_hits"] += 1; d["k3"] += 1
        if nc > 0:
            S["k3_hits_with_cross"] += 1
            S["maxcross_at_k3_hit"] = max(S["maxcross_at_k3_hit"], nc)
    if time.time() - last > 30:
        S["elapsed"] = time.time() - t0
        with open(OUT + ".tmp", "w") as fh:
            json.dump(S, fh, indent=1, sort_keys=True)
        os.replace(OUT + ".tmp", OUT)
        last = time.time()
S["elapsed"] = time.time() - t0
with open(OUT, "w") as fh:
    json.dump(S, fh, indent=1, sort_keys=True)
print(json.dumps(S, indent=1))
