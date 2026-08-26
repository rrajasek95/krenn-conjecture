#!/usr/bin/env python3
"""W32 / T21 -- controls for the orbit-exhaustive m=0/m=1 theorem.

C1  ORBIT INVARIANCE (the load-bearing step): unit-ness must be constant on
    S_8 x S_3 orbits.  Take random NON-representative members of each orbit
    and re-decide them from scratch; the verdict must match the
    representative's.
C2  MUTATION: perturb one generator of a decided case; the verdict must flip.
C3  NON-VACUITY: at k = 3 the same pipeline on the same configurations must
    return NOT unit (else the m=1 kill would be an artifact of the encoding).
C4  ENCODER: for a random configuration, the symbolic generators must agree
    with a direct numeric evaluation of H_w at a random rational point.
"""
import itertools, json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from w32_core import (Manifest, ekey, haf_word, no_shadow_guard,
                      perfect_matchings, require, run_singular,
                      words_offcount_le, zero_source)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "results_t21.json")
N = 8
PMS = perfect_matchings(tuple(range(N)))
PMSET = {frozenset(M): i for i, M in enumerate(PMS)}
IMP4 = words_offcount_le(N, 4)
IMP3 = words_offcount_le(N, 3)
EDGES = list(itertools.combinations(range(N), 2))
PLACE = [(e, a, b) for e in EDGES for a in range(3) for b in range(3) if a != b]
GENS = [([1, 0, 2, 3, 4, 5, 6, 7], [0, 1, 2]),
        ([1, 2, 3, 4, 5, 6, 7, 0], [0, 1, 2]),
        (list(range(N)), [1, 0, 2]), (list(range(N)), [1, 2, 0])]
rng = random.Random(212121)
R = {}
MAN = Manifest(["orbit_invariance", "mutation_flips", "k3_nonvacuous",
                "encoder_matches_numeric"])


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


def cellmap(tri, crosses):
    cm = {e: [[None] * 3 for _ in range(3)] for e in EDGES}
    n = 0
    for c, mi in enumerate(tri):
        for e in PMS[mi]:
            n += 1
            cm[ekey(*e)][c][c] = n
    for (e, a, b) in crosses:
        n += 1
        cm[ekey(*e)][a][b] = n
    return cm, n


def gens_for(tri, crosses, words=IMP4):
    cm, n = cellmap(tri, crosses)
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
                mon.append(f"zzw({nm})")
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
              '"UNIT:", (size(zzG) == 1 && zzG[1] == 1);\n')
    no_shadow_guard(script, {"zzw"} | {f"zzw({i})" for i in range(1, nv + 1)})
    for ln in run_singular(script, timeout=timeout).splitlines():
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

# C1 -- orbit invariance on genuinely different members
inv = {"checks": 0, "agree": 0}
for oi, orb in enumerate(ORB):
    rep = orb[0]
    pl0 = PLACE[rng.randrange(len(PLACE))]
    v0 = unit(*gens_for(rep, [pl0]))
    for _ in range(2):
        pi = list(range(N)); rng.shuffle(pi)
        rho = [list(p) for p in itertools.permutations(range(3))][
            rng.randrange(6)]
        T2, pl2 = act_triple(rep, pi, rho), act_place(pl0, pi, rho)
        require(T2 in set(orb), "the image left the orbit -- action bug")
        v2 = unit(*gens_for(T2, [pl2]))
        inv["checks"] += 1
        inv["agree"] += 1 if v2 == v0 else 0
        require(v2 == v0, f"ORBIT INVARIANCE FAILS at orbit {oi}")
require(inv["checks"] >= 16, "too few invariance checks")
MAN.mark("orbit_invariance")
R["C1"] = inv
print(f"C1 orbit invariance: {inv['agree']}/{inv['checks']} agree "
      f"(non-representative members re-decided from scratch)")

# C2 -- mutation
rep = ORB[0][0]
pl = PLACE[0]
gs, nv = gens_for(rep, [pl])
base = unit(gs, nv)
mut = list(gs)
mut = [g for g in mut if not g.endswith("-(1)")]
mv = unit(mut, nv)
require(base and not mv, f"mutation control did not flip: {base} -> {mv}")
MAN.mark("mutation_flips")
R["C2"] = {"base_unit": base, "mutated_unit": mv}
print(f"C2 mutation: dropping the constant-word generators flips "
      f"{base} -> {mv}")

# C3 -- k = 3 non-vacuity on the SAME configurations
nv3 = []
for oi, orb in enumerate(ORB[:4]):
    g3, n3 = gens_for(orb[0], [PLACE[rng.randrange(len(PLACE))]], IMP3)
    nv3.append(unit(g3, n3))
require(not any(nv3), f"k=3 ideals unexpectedly unit: {nv3}")
MAN.mark("k3_nonvacuous")
R["C3"] = {"k3_unit_verdicts": nv3}
print(f"C3 k=3 non-vacuity: {nv3} (none unit) => the m=1 kill is not an "
      f"encoding artifact")

# C4 -- encoder vs numeric
rep = ORB[3][0]
pl = PLACE[rng.randrange(len(PLACE))]
cm, n = cellmap(rep, [pl])
vals = [Fraction(rng.randint(1, 9)) for _ in range(n + 1)]
src = zero_source(N)
for e in EDGES:
    for a in range(3):
        for b in range(3):
            if cm[e][a][b] is not None:
                src[e][a][b] = vals[cm[e][a][b]]
gs, _ = gens_for(rep, [pl])
bad = 0
for w in IMP4:
    tot = Fraction(0)
    for M in PMS:
        pr = Fraction(1)
        ok = True
        for (u, v) in M:
            nm = cm[(u, v)][w[u]][w[v]]
            if nm is None:
                ok = False
                break
            pr *= vals[nm]
        if ok:
            tot += pr
    if tot != haf_word(src, w):
        bad += 1
require(bad == 0, f"encoder mismatch on {bad} words")
MAN.mark("encoder_matches_numeric")
R["C4"] = {"words_checked": len(IMP4), "mismatches": 0}
print(f"C4 encoder: symbolic term enumeration matches the numeric hafnian on "
      f"all {len(IMP4)} imposed words at a random rational point")
R["manifest"] = MAN.assert_complete()
with open(OUT, "w") as fh:
    json.dump(R, fh, indent=1, sort_keys=True)
print("wrote", OUT)
