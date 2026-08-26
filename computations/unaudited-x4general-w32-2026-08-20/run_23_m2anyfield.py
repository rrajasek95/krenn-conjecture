#!/usr/bin/env python3
"""W32 / T17 -- the cross-cell filtration at m = 1 (ALL disjoint-PM-triple
orbits, not only the (C) ones) and m = 2 (exhaustive over placement-pair
orbits).  Resumable: every decided case is appended to results_t23.json."""
import itertools, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w32_core import (ekey, no_shadow_guard, perfect_matchings, require,
                      run_singular, words_offcount_le)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_t23.json")
N = 8
PMS = perfect_matchings(tuple(range(N)))
PMSET = {frozenset(M): i for i, M in enumerate(PMS)}
IMP4 = words_offcount_le(N, 4)
EDGES = list(itertools.combinations(range(N), 2))
XT = [(a, b) for a in range(3) for b in range(3) if a != b]
PLACE = [(e, a, b) for e in EDGES for (a, b) in XT]
SEC = int(sys.argv[1]) if len(sys.argv) > 1 else 28800
G8 = [list(p) for p in itertools.permutations(range(N))]
G3 = [list(p) for p in itertools.permutations(range(3))]
GENS = [([1, 0, 2, 3, 4, 5, 6, 7], [0, 1, 2]),
        ([1, 2, 3, 4, 5, 6, 7, 0], [0, 1, 2]),
        (list(range(N)), [1, 0, 2]), (list(range(N)), [1, 2, 0])]


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


def actPM(pi, i):
    return PMSET[frozenset(ekey(pi[u], pi[v]) for (u, v) in PMS[i])]


def act_triple(T, pi, rho):
    inv = [0] * 3
    for c in range(3):
        inv[rho[c]] = c
    return tuple(actPM(pi, T[inv[c]]) for c in range(3))


def act_place(pl, pi, rho):
    (u, v), a, b = pl
    pu, pv, pa, pb = pi[u], pi[v], rho[a], rho[b]
    return ((pu, pv), pa, pb) if pu < pv else ((pv, pu), pb, pa)


def gens_for(tri, crosses):
    cm = {e: [[None] * 3 for _ in range(3)] for e in EDGES}
    n = 0
    for c, mi in enumerate(tri):
        for e in PMS[mi]:
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


def unit(gs, nv, char="integer", timeout=600):
    base = "integer" if char in ("integer", "ZZ") else str(char)
    script = (f"ring R = {base}, (zzw(1..{nv})), dp;\n"
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


okpair = {}
for i in range(len(PMS)):
    for j in range(i + 1, len(PMS)):
        if not (set(PMS[i]) & set(PMS[j])):
            okpair[(i, j)] = ham(PMS[i], PMS[j])
disj = []
for i, j, k in itertools.combinations(range(len(PMS)), 3):
    if (i, j) in okpair and (i, k) in okpair and (j, k) in okpair:
        disj.extend(itertools.permutations((i, j, k)))
S0, ORB = set(disj), []
while S0:
    s = next(iter(S0)); o = {s}; fr = [s]
    while fr:
        x = fr.pop()
        for (pi, rho) in GENS:
            y = act_triple(x, pi, rho)
            if y not in o:
                o.add(y); fr.append(y)
    ORB.append(sorted(o)); S0 -= o
print("disjoint-triple orbits:", len(ORB), [len(o) for o in ORB], flush=True)

S = {"m1": {"n": 0, "unit": 0, "survivors": []},
     "m2": {"n": 0, "unit": 0, "survivors": [], "covered_orbits": []},
     "orbit_sizes": [len(o) for o in ORB], "n_ordered_triples": len(disj)}
if os.path.exists(OUT):
    try:
        S = json.load(open(OUT))
    except Exception:
        pass
t0 = time.time(); last = 0


def flush():
    global last
    S["elapsed"] = time.time() - t0
    with open(OUT + ".tmp", "w") as fh:
        json.dump(S, fh, indent=1, sort_keys=True)
    os.replace(OUT + ".tmp", OUT); last = time.time()


STAB, PREPS = [], []
for orb in ORB:
    T = orb[0]
    st = [(pi, rho) for pi in G8 for rho in G3 if act_triple(T, pi, rho) == T]
    STAB.append(st)
    rem, reps = set(PLACE), []
    while rem:
        p0 = next(iter(rem))
        o = {act_place(p0, pi, rho) for (pi, rho) in st}
        reps.append(p0); rem -= o
    PREPS.append(reps)
print("stab sizes", [len(s) for s in STAB], "placement-orbit counts",
      [len(r) for r in PREPS], flush=True)

# ---- m = 1 over ALL orbits
for oi, orb in enumerate(ORB):
    T = orb[0]
    for pl in PREPS[oi]:
        key = f"m1:{oi}:{pl}"
        if key in S.get("done", {}):
            continue
        if time.time() - t0 > SEC * 0.4:
            break
        gs, nv = gens_for(T, [pl])
        d, u = unit(gs, nv)
        S["m1"]["n"] += 1
        S["m1"]["unit"] += 1 if u else 0
        if not u:
            S["m1"]["survivors"].append({"orbit": oi, "pl": str(pl), "dim": d})
            print("  m1 SURVIVOR", oi, pl, d, flush=True)
        S.setdefault("done", {})[key] = u
        if time.time() - last > 30:
            flush()
print("m=1 all-orbit sweep:", S["m1"]["n"], "cases,", S["m1"]["unit"],
      "unit,", len(S["m1"]["survivors"]), "survivors", flush=True)
flush()

# ---- m = 2, exhaustive over placement-PAIR orbits, orbit by orbit
for oi, orb in enumerate(ORB):
    if time.time() - t0 > SEC:
        break
    T, st = orb[0], STAB[oi]
    rem = set(frozenset(p) for p in itertools.combinations(PLACE, 2))
    reps = []
    while rem:
        p0 = next(iter(rem))
        a, b = tuple(p0)
        o = {frozenset((act_place(a, pi, rho), act_place(b, pi, rho)))
             for (pi, rho) in st}
        reps.append((a, b)); rem -= o
    print(f"  m=2 orbit {oi}: {len(reps)} placement-pair orbits", flush=True)
    done = 0
    for (a, b) in reps:
        if time.time() - t0 > SEC:
            break
        key = f"m2:{oi}:{a}:{b}"
        if key in S.get("done", {}):
            continue
        gs, nv = gens_for(T, [a, b])
        try:
            d, u = unit(gs, nv, timeout=400)
        except Exception as ex:
            S.setdefault("errors", []).append(str(ex)[:80]); continue
        S["m2"]["n"] += 1
        S["m2"]["unit"] += 1 if u else 0
        done += 1
        if not u:
            S["m2"]["survivors"].append({"orbit": oi, "a": str(a),
                                         "b": str(b), "dim": d})
            print("  m2 SURVIVOR", oi, a, b, d, flush=True)
        S.setdefault("done", {})[key] = u
        if time.time() - last > 30:
            flush()
    if done >= len(reps):
        S["m2"]["covered_orbits"].append(oi)
    flush()
flush()
print("m=2:", S["m2"]["n"], "cases,", S["m2"]["unit"], "unit,",
      len(S["m2"]["survivors"]), "survivors; orbits fully covered:",
      S["m2"]["covered_orbits"], flush=True)
