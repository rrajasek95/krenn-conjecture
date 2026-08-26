#!/usr/bin/env python3
"""W32 / T19 -- upgrade the m = 0 / m = 1 filtration verdicts from char 0 to
ANY FIELD.

A unit ideal in char 0 does NOT imply a unit ideal mod p (ledger: A8's
load-bearing note in reverse).  For each orbit representative we therefore
(a) recompute std over ZZ -- if 1 is in the strong Groebner basis over the
integers the ideal is unit over EVERY field -- and (b) fall back to a bank of
characteristics 2,3,5,7,11,13,32003,1000003,1000033 when the ZZ computation
is unavailable or times out.  Timeouts are 'unchecked', never 'refuted'
(ledger 23).
"""
import itertools, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w32_core import (ekey, no_shadow_guard, perfect_matchings, require,
                      run_singular, words_offcount_le)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_t19.json")
N = 8
PMS = perfect_matchings(tuple(range(N)))
PMSET = {frozenset(M): i for i, M in enumerate(PMS)}
IMP4 = words_offcount_le(N, 4)
EDGES = list(itertools.combinations(range(N), 2))
PLACE = [(e, a, b) for e in EDGES for a in range(3) for b in range(3) if a != b]
G8 = [list(p) for p in itertools.permutations(range(N))]
G3 = [list(p) for p in itertools.permutations(range(3))]
GENS = [([1, 0, 2, 3, 4, 5, 6, 7], [0, 1, 2]),
        ([1, 2, 3, 4, 5, 6, 7, 0], [0, 1, 2]),
        (list(range(N)), [1, 0, 2]), (list(range(N)), [1, 2, 0])]
CHARS = [0, 2, 3, 5, 7, 11, 13, 32003, 1000003, 1000033]
SEC = int(sys.argv[1]) if len(sys.argv) > 1 else 7200


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


def unit(gs, nv, char, timeout=400):
    base = "integer" if char == "ZZ" else str(char)
    script = (f"ring R = {base}, (zzw(1..{nv})), dp;\n"
              "ideal zzI = " + ",\n ".join(gs) + ";\n"
              "ideal zzG = std(zzI);\n"
              '"UNIT:", (size(zzG) == 1 && zzG[1] == 1);\n')
    no_shadow_guard(script, {"zzw"} | {f"zzw({i})" for i in range(1, nv + 1)})
    txt = run_singular(script, timeout=timeout)
    for ln in txt.splitlines():
        if ln.strip().startswith("UNIT:"):
            return int(ln.split(":")[1]) == 1
    raise RuntimeError("parse failure")


okp = {}
for i in range(len(PMS)):
    for j in range(i + 1, len(PMS)):
        if not (set(PMS[i]) & set(PMS[j])):
            okp[(i, j)] = ham(PMS[i], PMS[j])
disj = []
for i, j, k in itertools.combinations(range(len(PMS)), 3):
    if (i, j) in okp and (i, k) in okp and (j, k) in okp:
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

S = {"m0": [], "m1": [], "chars": CHARS, "unchecked": []}
t0 = time.time(); last = 0


def flush():
    global last
    S["elapsed"] = time.time() - t0
    with open(OUT + ".tmp", "w") as fh:
        json.dump(S, fh, indent=1, sort_keys=True)
    os.replace(OUT + ".tmp", OUT); last = time.time()


for oi, orb in enumerate(ORB):
    T = orb[0]
    gs, nv = gens_for(T, [])
    rec = {"orbit": oi, "size": len(orb), "verdicts": {}}
    try:
        rec["ZZ"] = unit(gs, nv, "ZZ", timeout=600)
    except Exception as ex:
        rec["ZZ"] = None
        S["unchecked"].append(f"m0 orbit {oi} ZZ: {str(ex)[:80]}")
    for ch in CHARS:
        try:
            rec["verdicts"][str(ch)] = unit(gs, nv, ch)
        except Exception as ex:
            rec["verdicts"][str(ch)] = None
            S["unchecked"].append(f"m0 orbit {oi} char {ch}: {str(ex)[:80]}")
    S["m0"].append(rec)
    print(f"m=0 orbit {oi}: ZZ={rec['ZZ']} chars={rec['verdicts']}", flush=True)
    flush()

STAB, PREPS = [], []
for orb in ORB:
    T = orb[0]
    st = [(pi, rho) for pi in G8 for rho in G3 if act_triple(T, pi, rho) == T]
    STAB.append(st)
    rem, reps = set(PLACE), []
    while rem:
        p0 = next(iter(rem))
        rem -= {act_place(p0, pi, rho) for (pi, rho) in st}
        reps.append(p0)
    PREPS.append(reps)

for oi, orb in enumerate(ORB):
    T = orb[0]
    for pl in PREPS[oi]:
        if time.time() - t0 > SEC:
            break
        gs, nv = gens_for(T, [pl])
        rec = {"orbit": oi, "pl": str(pl), "verdicts": {}}
        try:
            rec["ZZ"] = unit(gs, nv, "ZZ", timeout=400)
        except Exception as ex:
            rec["ZZ"] = None
            S["unchecked"].append(f"m1 {oi} {pl} ZZ: {str(ex)[:60]}")
        for ch in (0, 2, 3, 1000003):
            try:
                rec["verdicts"][str(ch)] = unit(gs, nv, ch)
            except Exception as ex:
                rec["verdicts"][str(ch)] = None
                S["unchecked"].append(f"m1 {oi} {pl} char {ch}: {str(ex)[:60]}")
        S["m1"].append(rec)
        if time.time() - last > 30:
            flush()
    print(f"m=1 orbit {oi}: done {len(S['m1'])} cases so far", flush=True)
    flush()
flush()
zz = [r for r in S["m1"] if r.get("ZZ") is True]
print("m=1 cases:", len(S["m1"]), "; ZZ-unit:", len(zz),
      "; unchecked:", len(S["unchecked"]), flush=True)
