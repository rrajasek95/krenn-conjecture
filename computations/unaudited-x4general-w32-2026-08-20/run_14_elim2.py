#!/usr/bin/env python3
"""W32 / T14 -- the CROSS-CELL FILTRATION, extended.

Same stratum as run_11 (three disjoint PMs with pairwise Hamiltonian unions,
12 symbolic weights) with m symbolic cross cells added.  Extends run_11's
result (m = 1: 504/504 unit, exhaustive over all 168 placements for 3 triples)
to more triples and to m = 2, 3, and re-checks a sample in two primes = 1 mod 3.
"""
import itertools, json, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w32_core import (ekey, no_shadow_guard, perfect_matchings, require,
                      run_singular, words_offcount_le)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "results_t14.json")
N = 8
PMS = perfect_matchings(tuple(range(N)))
IMP4 = words_offcount_le(N, 4)
rng = random.Random(987654)
SEC = int(sys.argv[1]) if len(sys.argv) > 1 else 5400
EDGES = list(itertools.combinations(range(N), 2))
XT = [(a, b) for a in range(3) for b in range(3) if a != b]
PLACE = [(e, a, b) for e in EDGES for (a, b) in XT]


def ham(A, B):
    adj = {i: [] for i in range(N)}
    for e in list(A) + list(B):
        adj[e[0]].append(e[1]); adj[e[1]].append(e[0])
    seen, cur, prev = {0}, 0, None
    for _ in range(N - 1):
        nxt = [x for x in adj[cur] if x != prev]
        if not nxt:
            return False
        prev, cur = cur, nxt[0]
        if cur in seen:
            return False
        seen.add(cur)
    return len(seen) == N


def gens(tri, crosses):
    cm = {e: [[None] * 3 for _ in range(3)] for e in EDGES}
    n = 0
    for c, M in enumerate(tri):
        for e in M:
            n += 1
            cm[ekey(*e)][c][c] = f"zzw({n})"
    for (e, a, b) in crosses:
        n += 1
        cm[ekey(*e)][a][b] = f"zzw({n})"
    out = []
    for w in IMP4:
        terms = []
        for M in PMS:
            mon, ok = [], True
            for (u, v) in M:
                nm = cm[(u, v)][w[u]][w[v]]
                if nm is None:
                    ok = False
                    break
                mon.append(nm)
            if ok:
                terms.append("*".join(sorted(mon)))
        tgt = 1 if len(set(w)) == 1 else 0
        if not terms and tgt == 0:
            continue
        out.append(f"({'+'.join(terms) if terms else '0'})-({tgt})")
    return sorted(set(out)), n


def unit(gs, nv, char=0, timeout=400):
    script = (f"ring R = {char}, (zzw(1..{nv})), dp;\n"
              "ideal zzI = " + ",\n ".join(gs) + ";\n"
              "ideal zzG = std(zzI);\n"
              '"DIM:", dim(zzG);\n'
              '"UNIT:", (size(zzG) == 1 && zzG[1] == 1);\n')
    no_shadow_guard(script, {"zzw"} | {f"zzw({i})" for i in range(1, nv + 1)})
    txt = run_singular(script, timeout=timeout)
    d = u = None
    for ln in txt.splitlines():
        ln = ln.strip()
        if ln.startswith("DIM:"):
            d = int(ln.split(":")[1])
        if ln.startswith("UNIT:"):
            u = int(ln.split(":")[1]) == 1
    require(d is not None and u is not None, "parse failure")
    return d, u


idx = list(range(len(PMS))); rng.shuffle(idx)
CT = []
for i, j, k in itertools.combinations(idx, 3):
    A, B, C = PMS[i], PMS[j], PMS[k]
    if set(A) & set(B) or set(A) & set(C) or set(B) & set(C):
        continue
    if ham(A, B) and ham(A, C) and ham(B, C):
        CT.append((A, B, C))
        if len(CT) >= 40:
            break

S = {"m1": {"n": 0, "unit": 0, "survivors": [], "triples": 0},
     "m2": {"n": 0, "unit": 0, "survivors": []},
     "m3": {"n": 0, "unit": 0, "survivors": []},
     "prime_recheck": {"n": 0, "agree": 0, "primes": [1000003, 1000033]},
     "timeouts": 0}
t0 = time.time(); last = 0


def flush():
    global last
    S["elapsed"] = time.time() - t0
    with open(OUT + ".tmp", "w") as fh:
        json.dump(S, fh, indent=1, sort_keys=True)
    os.replace(OUT + ".tmp", OUT)
    last = time.time()


# ---- m = 1, exhaustive over placements, as many triples as fit in 45% budget
for ti, tri in enumerate(CT):
    if time.time() - t0 > SEC * 0.45:
        break
    S["m1"]["triples"] += 1
    for pl in PLACE:
        if time.time() - t0 > SEC * 0.45:
            break
        gs, nv = gens(tri, [pl])
        try:
            d, u = unit(gs, nv, 0)
        except Exception:
            S["timeouts"] += 1
            continue
        S["m1"]["n"] += 1
        if u:
            S["m1"]["unit"] += 1
        else:
            S["m1"]["survivors"].append({"triple": ti, "pl": str(pl), "dim": d})
        if time.time() - last > 30:
            flush()

# ---- m = 2 and m = 3, sampled
for m, share in ((2, 0.8), (3, 1.0)):
    while time.time() - t0 < SEC * share:
        tri = CT[rng.randrange(len(CT))]
        cr = rng.sample(PLACE, m)
        if len({(e, a, b) for (e, a, b) in cr}) < m:
            continue
        gs, nv = gens(tri, cr)
        try:
            d, u = unit(gs, nv, 0, timeout=500)
        except Exception:
            S["timeouts"] += 1
            continue
        key = f"m{m}"
        S[key]["n"] += 1
        if u:
            S[key]["unit"] += 1
        else:
            S[key]["survivors"].append({"cr": str(cr), "dim": d})
        if time.time() - last > 30:
            flush()

# ---- two-prime recheck on a random sample of m=1 configurations
rc = 0
while rc < 40 and time.time() - t0 < SEC * 1.15:
    tri = CT[rng.randrange(len(CT))]
    pl = PLACE[rng.randrange(len(PLACE))]
    gs, nv = gens(tri, [pl])
    try:
        d0, u0 = unit(gs, nv, 0)
        ok = True
        for p in (1000003, 1000033):
            dp, up = unit(gs, nv, p)
            ok = ok and (up == u0)
    except Exception:
        S["timeouts"] += 1
        continue
    S["prime_recheck"]["n"] += 1
    S["prime_recheck"]["agree"] += 1 if ok else 0
    rc += 1
flush()
print(json.dumps({k: (v if not isinstance(v, dict) else
                      {kk: (vv if kk != "survivors" else len(vv))
                       for kk, vv in v.items()}) for k, v in S.items()},
                 indent=1))
