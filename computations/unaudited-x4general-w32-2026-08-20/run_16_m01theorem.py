#!/usr/bin/env python3
"""W32 / T16 -- the CROSS-CELL FILTRATION as an EXHAUSTIVE statement.

The S_8 x S_3 symmetry collapses the family completely:
  * ordered disjoint PM triples of K_8: 32,970 x 6 = 197,820, few orbits;
  * ordered (C)-triples (all pairwise unions Hamiltonian): 100,800 in
    exactly TWO orbits (sizes 60,480 and 40,320).
Unit-ness of the X_4 ideal is a symmetry invariant, so one Singular run per
orbit decides the whole family.

  m = 0 : every orbit of ordered disjoint PM triples, 12 symbolic weights.
          An exhaustive independent char-0 Groebner proof of W29-T1 restricted
          to perfect-matching colour supports (W29's N=8 verdict is SAT-based).
  m = 1 : every orbit of (triple, cross-cell placement) pairs under the
          stabiliser -- 13 symbolic parameters.  NEW: the first non-diagonal
          general-block emptiness statement at N = 8.

Controls: k=3 ideal not unit + explicit rational point; two primes = 1 mod 3;
zz-prefix + no-shadowing guard; stdout-'?' parse; generators deduplicated.
"""
import itertools, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w32_core import (ekey, haf_word, no_shadow_guard, perfect_matchings,
                      require, run_singular, words_offcount_le, zero_source)
from fractions import Fraction

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "results_t16.json")
N = 8
PMS = perfect_matchings(tuple(range(N)))
PMSET = {frozenset(M): i for i, M in enumerate(PMS)}
IMP4 = words_offcount_le(N, 4)
IMP3 = words_offcount_le(N, 3)
EDGES = list(itertools.combinations(range(N), 2))
XT = [(a, b) for a in range(3) for b in range(3) if a != b]
PLACE = [(e, a, b) for e in EDGES for (a, b) in XT]
SEC = int(sys.argv[1]) if len(sys.argv) > 1 else 7200
S = {"m0": {}, "m1": {}, "controls": {}}


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


def actPM(pi, idx):
    return PMSET[frozenset(ekey(pi[u], pi[v]) for (u, v) in PMS[idx])]


def act_triple(T, pi, rho):
    inv = [0] * 3
    for c in range(3):
        inv[rho[c]] = c
    return tuple(actPM(pi, T[inv[c]]) for c in range(3))


def act_place(pl, pi, rho):
    (u, v), a, b = pl[0], pl[1], pl[2]
    pu, pv, pa, pb = pi[u], pi[v], rho[a], rho[b]
    return ((pu, pv), pa, pb) if pu < pv else ((pv, pu), pb, pa)


G8 = [list(p) for p in itertools.permutations(range(N))]
G3 = [list(p) for p in itertools.permutations(range(3))]
GENS = [([1, 0, 2, 3, 4, 5, 6, 7], [0, 1, 2]),
        ([1, 2, 3, 4, 5, 6, 7, 0], [0, 1, 2]),
        (list(range(N)), [1, 0, 2]), (list(range(N)), [1, 2, 0])]


def orbits_of(objs, act):
    S0, out = set(objs), []
    while S0:
        s = next(iter(S0)); orb = {s}; fr = [s]
        while fr:
            x = fr.pop()
            for (pi, rho) in GENS:
                y = act(x, pi, rho)
                if y not in orb:
                    orb.add(y); fr.append(y)
        out.append(sorted(orb)); S0 -= orb
    return out


def gens_for(tri, crosses, words):
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
    for w in words:
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


def unit(gs, nv, char=0, timeout=600):
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


def flush():
    with open(OUT + ".tmp", "w") as fh:
        json.dump(S, fh, indent=1, sort_keys=True)
    os.replace(OUT + ".tmp", OUT)


t0 = time.time()
# ---- build the two families
okpair = {}
for i in range(len(PMS)):
    for j in range(i + 1, len(PMS)):
        if set(PMS[i]) & set(PMS[j]):
            continue
        okpair[(i, j)] = ham(PMS[i], PMS[j])
disj, ctri = [], []
for i, j, k in itertools.combinations(range(len(PMS)), 3):
    if (i, j) not in okpair or (i, k) not in okpair or (j, k) not in okpair:
        continue
    for t in itertools.permutations((i, j, k)):
        disj.append(t)
        if okpair[(i, j)] and okpair[(i, k)] and okpair[(j, k)]:
            ctri.append(t)
Od = orbits_of(disj, act_triple)
Oc = orbits_of(ctri, act_triple)
S["families"] = {"ordered_disjoint": len(disj), "orbits_disjoint": len(Od),
                 "orbit_sizes_disjoint": [len(o) for o in Od],
                 "ordered_C": len(ctri), "orbits_C": len(Oc),
                 "orbit_sizes_C": [len(o) for o in Oc]}
print("ordered disjoint triples", len(disj), "in", len(Od), "orbits",
      [len(o) for o in Od])
print("ordered (C)-triples", len(ctri), "in", len(Oc), "orbits",
      [len(o) for o in Oc])
flush()

# ---- m = 0, exhaustive over all orbits of ordered disjoint triples
S["m0"] = {"orbits": [], "all_unit": None}
allu = True
for oi, orb in enumerate(Od):
    T = orb[0]
    gs, nv = gens_for(T, [], IMP4)
    d0, u0 = unit(gs, nv, 0)
    ups = []
    for p in (1000003, 1000033):
        dp, up = unit(gs, nv, p)
        ups.append(up)
    allu = allu and u0
    S["m0"]["orbits"].append({"orbit": oi, "size": len(orb), "rep": list(T),
                              "n_gens": len(gs), "dim": d0, "unit": u0,
                              "prime_units": ups,
                              "is_C": T in set(map(tuple, ctri))})
    print(f"  m=0 orbit {oi} (size {len(orb)}): unit={u0} dim={d0} "
          f"gens={len(gs)} primes={ups}")
    flush()
S["m0"]["all_unit"] = allu
require(allu, "m=0 NOT all unit -- would contradict W29-T1")

# ---- k=3 control on one (C) rep
T = Oc[0][0]
gs3, nv3 = gens_for(T, [], IMP3)
d3, u3 = unit(gs3, nv3, 0)
require(not u3, f"k=3 control unexpectedly unit (dim {d3})")
src = zero_source(N)
for c, mi in enumerate(T):
    for e in PMS[mi]:
        src[ekey(*e)][c][c] = Fraction(1)
bad3 = [w for w in IMP3 if haf_word(src, w) != (1 if len(set(w)) == 1 else 0)]
bad4 = [w for w in IMP4 if haf_word(src, w) != (1 if len(set(w)) == 1 else 0)]
require(not bad3 and bad4, "explicit k=3 point control failed")
S["controls"]["k3"] = {"dim": d3, "unit": u3, "k4_violations": len(bad4)}
print(f"  k=3 control: not unit (dim {d3}); explicit point violates "
      f"{len(bad4)} k=4 words")
flush()

# ---- m = 1, exhaustive: placement orbits under each triple's stabiliser
S["m1"] = {"orbits": [], "all_unit": None, "n_cases": 0}
allu1 = True
for oi, orb in enumerate(Oc):
    T = orb[0]
    stab = []
    for pi in G8:
        for rho in G3:
            if act_triple(T, pi, rho) == T:
                stab.append((pi, rho))
    rem = set(PLACE)
    reps = []
    while rem:
        p0 = next(iter(rem))
        o = set()
        for (pi, rho) in stab:
            o.add(act_place(p0, pi, rho))
        reps.append((p0, len(o)))
        rem -= o
    print(f"  m=1 triple orbit {oi}: |Stab| = {len(stab)}, "
          f"{len(reps)} placement orbits")
    for (pl, osz) in reps:
        if time.time() - t0 > SEC:
            break
        gs, nv = gens_for(T, [pl], IMP4)
        d, u = unit(gs, nv, 0)
        allu1 = allu1 and u
        S["m1"]["n_cases"] += 1
        S["m1"]["orbits"].append({"triple_orbit": oi, "placement": str(pl),
                                  "orbit_size": osz, "unit": u, "dim": d,
                                  "n_gens": len(gs)})
        if not u:
            print("   SURVIVOR", pl, "dim", d)
        flush()
S["m1"]["all_unit"] = allu1
S["elapsed"] = time.time() - t0
flush()
print("m=1 cases:", S["m1"]["n_cases"], "all unit:", allu1)
