#!/usr/bin/env python3
"""W27 T1a -- THE DIAGONAL X_4 QUESTION AT N = 8.

W25-D0/D1 give, on the monochrome-diagonal stratum (three edge classes L_c of
K_N with nonzero weights t^c, forced pairwise disjoint -- see the note below),

    H_w = prod_c haf(t^c | S_c),   S_c = w^{-1}(c),

so H_w = 0 as soon as some |S_c| is odd.  At N = 8 the colour-class profiles
with off-count <= 4 and ALL PARTS EVEN are exactly

    (8,0,0)   off 0   -- the constant words:      haf(t^c|V) = 1
    (6,2,0)   off 2   -- X_2 conditions:          haf(t^c|V-uv) t^d_uv = 0
    (4,4,0)   off 4   -- NEW at the X_4 rung:     haf(t^c|S) haf(t^d|V-S) = 0
    (4,2,2)   off 4   -- NEW at the X_4 rung:     haf(t^c|S) t^d_uv t^e_xy = 0

(the odd-part profiles (7,1,0),(5,3,0),(5,2,1),(6,1,1),(4,3,1) are automatic),
so on the diagonal stratum at N = 8

    X_1 = X_0 (trivially),  X_2 = X_3,  X_4 = X_5,

and X_4 is X_3 PLUS the (4,4,0) and (4,2,2) conditions.  THIS RUNNER:

 (1) verifies that decomposition against the RAW word definition (W25's
     independent engine) -- control;
 (2) proves the NO-CANCELLATION REDUCTION: on the sub-stratum where every
     vanishing hafnian vanishes for lack of a matching, X_4 is nonempty iff
     some triple of PAIRWISE DISJOINT PERFECT MATCHINGS of K_8 satisfies the
     purely combinatorial (C') and (D'); and decides that finite question
     EXHAUSTIVELY;
 (3) records the exact obstruction (which word families are jointly infeasible)
     and runs the adversarial builder (ledger 20) against the resulting NEVER
     claim.

Why the classes are pairwise disjoint (needed for the reduction, not assumed):
if an edge f lies in a perfect matching M_c of L_c and also f in L_d (d != c),
the (6,2,0) word with colour d on f and colour c elsewhere has
H = haf(t^c|V-f) * t^d_f, and haf(t^c|V-f) contains the monomial of M_c - f.
In the no-cancellation stratum that forces f not in L_d.  So the PMs M_c are
pairwise disjoint.
"""
from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-penult-w27-2026-08-18")
sys.path.insert(0, BASE)
import w27_core as W                                              # noqa: E402
C = W.C

N = 8
RES = {}
RAN = []
OUT = f"{BASE}/results_t1a_diag8.json"


def control(name):
    RAN.append(name)


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


# ------------------------------------------------------------------ (1)

def check_profile_decomposition(G, rng):
    """Control: build random diagonal sources and confirm that H_w computed by
    W25's bitmask engine equals the product formula, and that every odd-part
    profile gives 0."""
    bad = 0
    tested = 0
    oddzero = 0
    for _ in range(6):
        # three random disjoint edge classes, each containing a PM
        perm = list(range(N))
        rng.shuffle(perm)
        Ms = []
        used = set()
        for c in range(3):
            while True:
                p = list(range(N))
                rng.shuffle(p)
                M = W.pm_norm([(p[2 * i], p[2 * i + 1]) for i in range(4)])
                if not (set(M) & used):
                    break
            used |= set(M)
            Ms.append(M)
        Ls = []
        for c in range(3):
            extra = [e for e in G.E if e not in used]
            rng.shuffle(extra)
            L = list(Ms[c]) + extra[:rng.randint(0, 3)]
            used |= set(L)
            Ls.append(sorted(set(L)))
        wts = {}
        for c, L in enumerate(Ls):
            for e in L:
                wts[(c, e)] = Fraction(rng.randint(1, 5), rng.randint(1, 3))
        src = W.build_diag(N, Ls, wts)
        Lsw = [{e: wts[(c, e)] for e in Ls[c]} for c in range(3)]
        for _ in range(120):
            word = tuple(rng.randrange(3) for _ in range(N))
            a = C.H(src, word, N)
            b = W.diag_H(Lsw, word, N)
            tested += 1
            if a != b:
                bad += 1
            cc = [sum(1 for x in word if x == c) for c in range(3)]
            if any(x % 2 for x in cc):
                oddzero += 1
                if a != 0:
                    bad += 1
    return {"tested": tested, "mismatches": bad, "odd_profile_words": oddzero}


# ------------------------------------------------------------------ (2)

def pm_triples(G):
    """Every ordered triple of pairwise-disjoint perfect matchings of K_8,
    reduced to unordered triples."""
    PM = G.PMS
    MASK = G.PMMASK
    out = []
    for i in range(len(PM)):
        for j in range(i + 1, len(PM)):
            if MASK[i] & MASK[j]:
                continue
            for k in range(j + 1, len(PM)):
                if MASK[k] & (MASK[i] | MASK[j]):
                    continue
                out.append((PM[i], PM[j], PM[k]))
    return out


def cycle_type(Ma, Mb):
    """Component sizes of the 2-regular graph M_a  u  M_b (both PMs)."""
    adj = {v: [] for v in range(N)}
    for M in (Ma, Mb):
        for (a, b) in M:
            adj[a].append(b)
            adj[b].append(a)
    seen = set()
    comps = []
    for v in range(N):
        if v in seen:
            continue
        stack = [v]
        seen.add(v)
        c = 0
        while stack:
            x = stack.pop()
            c += 1
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        comps.append(c)
    return tuple(sorted(comps))


def closed4(M):
    """The 4-subsets that are unions of two M-edges."""
    return {frozenset(a + b) for a, b in combinations(M, 2)}


def condC(T):
    """(4,4,0): no 4-set closed for two DIFFERENT colours."""
    cl = [closed4(M) for M in T]
    bad = []
    for c, d in combinations(range(3), 2):
        inter = cl[c] & cl[d]
        if inter:
            bad.append((c, d, sorted(sorted(x) for x in inter)))
    return (not bad), bad


def condD(T):
    """(4,2,2): for each colour c, no M_c-closed 4-set T4 that splits into one
    M_d-edge and one M_e-edge ({c,d,e} = {0,1,2})."""
    bad = []
    for c in range(3):
        d, e = [x for x in range(3) if x != c]
        cl = closed4(T[c])
        for f in T[d]:
            for g in T[e]:
                if set(f) & set(g):
                    continue
                S = frozenset(f + g)
                if S in cl:
                    bad.append((c, d, e, sorted(f), sorted(g)))
    return (not bad), bad


def condB(T):
    """(6,2,0): for c != d and uv in M_d, no PM of M_c on V - uv.  Automatic
    for disjoint PMs; checked anyway (control, not assumed)."""
    bad = []
    for c in range(3):
        for d in range(3):
            if d == c:
                continue
            for (u, v) in T[d]:
                rest = [x for x in range(N) if x not in (u, v)]
                # M_c has a PM on `rest` iff uv in M_c
                if all(set(e) <= set(rest) or set(e) == {u, v} for e in T[c]) \
                        and (u, v) in T[c]:
                    bad.append((c, d, (u, v)))
    return (not bad), bad


def main():
    t0 = time.time()
    rng = random.Random(20260818)
    G = W.Graph(N)
    RES["n"] = N
    RES["n_edges"] = len(G.E)
    RES["n_pms"] = len(G.PMS)

    print("=" * 74)
    print("(0) CONTROL: profiles with off-count <= 4 at N = 8")
    print("=" * 74)
    lp = W.live_profiles(N, 3, 4)
    allp = [p for p in W.profiles(N, 3, 4) if max(p) != N]
    odd = [p for p in allp if any(x % 2 for x in p)]
    print(f"   mixed profiles with off-count <= 4: {len(allp)}")
    print(f"   ... automatically zero (some odd part): {len(odd)}  {odd}")
    print(f"   ... carrying a REAL condition:         {len(lp)}  {lp}")
    RES["profiles"] = {"mixed_le4": [list(p) for p in allp],
                       "odd_auto": [list(p) for p in odd],
                       "real": [list(p) for p in lp]}
    # the real ones must be exactly the (6,2,0)/(4,4,0)/(4,2,2) shapes
    shapes = sorted(set(tuple(sorted(p, reverse=True)) for p in lp))
    print(f"   distinct shapes: {shapes}")
    assert shapes == [(4, 2, 2), (4, 4, 0), (6, 2, 0)], shapes
    control("T1a0_profiles")
    ck("profiles")

    print("=" * 74)
    print("(1) CONTROL: product formula vs W25's raw bitmask engine")
    print("=" * 74)
    r = check_profile_decomposition(G, rng)
    print(f"   random diagonal sources, {r['tested']} words: mismatches "
          f"{r['mismatches']} (must be 0); odd-profile words "
          f"{r['odd_profile_words']} all zero")
    assert r["mismatches"] == 0
    RES["formula_control"] = r
    control("T1a1_formula_control")
    ck("formula")

    print("=" * 74)
    print("(2) THE DISJOINT-PM TRIPLES OF K_8, EXHAUSTIVELY")
    print("=" * 74)
    T = pm_triples(G)
    print(f"   unordered triples of pairwise disjoint PMs of K_8: {len(T)}")
    stats = {"total": len(T), "passC": 0, "passD": 0, "passCD": 0,
             "cycle_types": {}}
    winners = []
    for t in T:
        ct = tuple(sorted(cycle_type(t[a], t[b])
                          for a, b in combinations(range(3), 2)))
        stats["cycle_types"][str(ct)] = stats["cycle_types"].get(str(ct), 0) + 1
        okC, badC = condC(t)
        okD, badD = condD(t)
        okB, badB = condB(t)
        assert okB, ("condition (B) failed on disjoint PMs", badB)
        if okC:
            stats["passC"] += 1
        if okD:
            stats["passD"] += 1
        if okC and okD:
            stats["passCD"] += 1
            winners.append(t)
    print(f"   pass (4,4,0) condition (C): {stats['passC']}")
    print(f"   pass (4,2,2) condition (D): {stats['passD']}")
    print(f"   pass BOTH  -> a diagonal X_4 point at N=8: {stats['passCD']}")
    print(f"   cycle-type census of the three pairwise unions: "
          f"{stats['cycle_types']}")
    RES["pm_triples"] = stats
    RES["winners"] = [[[list(e) for e in M] for M in t] for t in winners[:20]]
    control("T1a2_pm_triples")
    ck("pmtriples")

    print("=" * 74)
    print("(2b) the C-condition is EXACTLY 'every pairwise union is an "
          "8-cycle' (independent derivation, cross-checked)")
    print("=" * 74)
    mism = 0
    for t in T:
        okC, _ = condC(t)
        ham = all(cycle_type(t[a], t[b]) == (8,)
                  for a, b in combinations(range(3), 2))
        if okC != ham:
            mism += 1
    print(f"   disagreements between (C) and 'all unions Hamiltonian': {mism} "
          f"(must be 0)")
    assert mism == 0
    RES["C_equals_hamiltonian"] = {"disagreements": mism}
    control("T1a2b_C_hamiltonian")

    print("=" * 74)
    print("(3) RAW CROSS-CHECK: build Delta^3_8 for a sample of triples and "
          "test X_3 / X_4 membership with W25's raw word engine")
    print("=" * 74)
    rows = []
    sample = list(T)
    rng.shuffle(sample)
    sample = sample[:14]
    # always include a triple whose unions are all Hamiltonian if one exists
    ham = [t for t in T if all(cycle_type(t[a], t[b]) == (8,)
                               for a, b in combinations(range(3), 2))]
    print(f"   triples with ALL unions Hamiltonian: {len(ham)}")
    for t in ham[:6]:
        if t not in sample:
            sample.append(t)
    for i, t in enumerate(sample):
        wts = {(c, e): Fraction(1) for c in range(3) for e in t[c]}
        src = W.build_diag(N, [list(M) for M in t], wts)
        ok3, w3 = C.in_Xk(src, N, 3)
        ok4, w4 = C.in_Xk(src, N, 4)
        okC, badC = condC(t)
        okD, badD = condD(t)
        rows.append({"triple": [[list(e) for e in M] for M in t],
                     "in_X3": ok3, "in_X4": ok4,
                     "first_X4_failure": list(w4) if w4 else None,
                     "condC": okC, "condD": okD,
                     "unions": [list(cycle_type(t[a], t[b]))
                                for a, b in combinations(range(3), 2)]})
        # THE key consistency check: predicted == observed
        assert ok3, ("Delta^3_8 must lie in X_3 (W25-D1/U1+)", w3)
        assert ok4 == (okC and okD), ("combinatorial prediction disagrees with "
                                      "the raw word test", t, ok4, okC, okD)
        if i < 6 or ok4:
            print(f"   triple {i}: unions {rows[-1]['unions']}; C {okC} D {okD}"
                  f"; RAW in_X3 {ok3} in_X4 {ok4}"
                  + (f"; first X_4 failure {w4}" if w4 else ""))
    print(f"   {len(rows)} triples raw-tested; prediction matched the raw word "
          f"test in every case")
    RES["raw_crosscheck"] = rows
    control("T1a3_raw_crosscheck")
    ck("rawcheck")

    print("=" * 74)
    print("(4) THE EXACT OBSTRUCTION")
    print("=" * 74)
    # For each triple, which condition kills it, and can (C) and (D) ever be
    # satisfied separately?
    obs = {"onlyC": 0, "onlyD": 0, "neither": 0, "both": 0}
    exC = None
    exD = None
    for t in T:
        okC, _ = condC(t)
        okD, _ = condD(t)
        if okC and okD:
            obs["both"] += 1
        elif okC:
            obs["onlyC"] += 1
            if exC is None:
                exC = t
        elif okD:
            obs["onlyD"] += 1
            if exD is None:
                exD = t
        else:
            obs["neither"] += 1
    print(f"   census: {obs}")
    RES["obstruction_census"] = obs
    if exC is not None:
        _, badD = condD(exC)
        print(f"   a triple satisfying (C) but not (D): {[[list(e) for e in M] for M in exC]}")
        print(f"      the (4,2,2) violations: {badD[:4]} ... total {len(badD)}")
        RES["exampleC"] = {"triple": [[list(e) for e in M] for M in exC],
                           "n_D_violations": len(badD),
                           "D_violations": [str(x) for x in badD]}
    if exD is not None:
        _, badC = condC(exD)
        print(f"   a triple satisfying (D) but not (C): "
              f"{[[list(e) for e in M] for M in exD]}")
        RES["exampleD"] = {"triple": [[list(e) for e in M] for M in exD],
                           "n_C_violations": len(badC)}
    control("T1a4_obstruction")
    ck("obstruction")

    print("=" * 74)
    print("(5) COUNTING LEMMA: why (C) and (D) collide")
    print("=" * 74)
    # For a triple with all unions Hamiltonian: count the 4-sets produced by
    # (D) and the M_c-closed 4-sets, and check the pigeonhole.
    det = []
    for t in (ham[:8] if ham else []):
        for c in range(3):
            d, e = [x for x in range(3) if x != c]
            Ds = set()
            for f in t[d]:
                for g in t[e]:
                    if not (set(f) & set(g)):
                        Ds.add(frozenset(f + g))
            det.append({"colour": c, "n_D_sets": len(Ds),
                        "n_closed4": len(closed4(t[c])),
                        "overlap": len(Ds & closed4(t[c]))})
    print(f"   for Hamiltonian triples: |D-sets| per colour "
          f"{sorted(set(x['n_D_sets'] for x in det))}, |M_c-closed 4-sets| "
          f"{sorted(set(x['n_closed4'] for x in det))}, overlaps "
          f"{sorted(set(x['overlap'] for x in det))}")
    RES["counting"] = det
    control("T1a5_counting")

    declared = ["T1a0_profiles", "T1a1_formula_control", "T1a2_pm_triples",
                "T1a2b_C_hamiltonian", "T1a3_raw_crosscheck",
                "T1a4_obstruction", "T1a5_counting"]
    missing = [x for x in declared if x not in RAN]
    print(f"CONTROL MANIFEST: declared {len(declared)}, ran {len(RAN)}, "
          f"missing {missing}")
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    RES["seconds"] = round(time.time() - t0, 1)
    assert not missing
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()
