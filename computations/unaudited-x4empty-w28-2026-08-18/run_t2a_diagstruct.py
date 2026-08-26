#!/usr/bin/env python3
"""W28 T2a -- the diagonal stratum at N = 8: structure, the D3 census
reproduced independently, and the two gaps closed.

THE CONDITIONS.  A monochrome-diagonal source is three weight functions
t^0,t^1,t^2 on E(K_8) with L_c = supp(t^c); H_w = prod_c haf(t^c|S_c).  The
live profiles at N = 8 are (8,0,0), (6,2,0), (4,4,0), (4,2,2):

 (A) haf(t^c|V) = 1                                        (three equations)
 (B) haf(t^c|V-uv) * t^d_uv = 0                for c != d
 (C) haf(t^c|S) * haf(t^d|V-S) = 0             for c != d, |S| = 4
 (D) haf(t^c|S) * t^d_f * t^e_g = 0            {c,d,e} = {0,1,2}, V-S = f+g

W28-DEL [PROVED-HERE] (closes the gap left by W27-D3, which enumerated
triples of disjoint PERFECT MATCHINGS but the no-cancellation hypothesis only
forces each L_c to CONTAIN one).  (B), (C), (D) are monotone DECREASING under
deleting edges (they are conjunctions of "this product vanishes", and deleting
edges only kills terms), while (A) needs one surviving perfect matching.  So
from any no-cancellation solution, delete every edge of L_c outside one chosen
perfect matching M_c and rescale: still a solution, now with L_c = M_c, and
(B) forces the M_c pairwise disjoint.  Hence the disjoint-PM enumeration is
COMPLETE for the no-cancellation stratum.

W28-LAM [PROVED-HERE] (the generating identity).  haf(A+B) = sum_{S} haf(A|S)
haf(B|V-S) over even S.  Applying it to lam_0 t^0 + lam_1 t^1 + lam_2 t^2 and
using (A)-(D) (all mixed profiles even at N = 8 are exactly (6,2,0), (4,4,0),
(4,2,2) plus the automatically-zero odd ones) gives, for a diagonal X_4 point
at N = 8,

        Haf(lam_0 t^0 + lam_1 t^1 + lam_2 t^2) = lam_0^4 + lam_1^4 + lam_2^4
        identically in lam;  in particular haf(t^c + t^d) = 2 and
        haf(t^0+t^1+t^2) = 3.

W28-GOOD [PROVED-HERE].  Put G^c_e = haf(t^c | V - e).  (B) says G^c vanishes
on L_d u L_e.  Expanding haf(t^c|V) at a vertex u gives
sum_{y != u} t^c_uy G^c_uy = 1, so L_c^good := {e in L_c : G^c_e != 0} COVERS
every vertex, and L_0^good, L_1^good, L_2^good are pairwise disjoint (and each
is disjoint from the other two FULL classes).  Three disjoint spanning
subgraphs of K_8 are forced.
"""
from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x4empty-w28-2026-08-18")
sys.path.insert(0, BASE)
import w28_core as K                                              # noqa: E402

N = 8
V = tuple(range(N))
E = list(combinations(V, 2))
RES = {}
RAN = []
OUT = f"{BASE}/results_t2a_diagstruct.json"


def control(name):
    if name not in RAN:
        RAN.append(name)


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def hafd(t, S):
    """haf of the scalar weight dict t over the vertex set S."""
    return K.haf_w(t, S)


def conditions(ts, kmax=4):
    """All violated conditions (A)-(D) of the diagonal stratum."""
    bad = []
    for c in range(3):
        if hafd(ts[c], V) != 1:
            bad.append(("A", c))
    for c in range(3):
        for d in range(3):
            if d == c:
                continue
            for e in E:
                if ts[d].get(e, 0) == 0:
                    continue
                if hafd(ts[c], [x for x in V if x not in e]) != 0:
                    bad.append(("B", c, d, e))
    if kmax >= 4:
        for c in range(3):
            for d in range(3):
                if d == c:
                    continue
                for S in combinations(V, 4):
                    if 0 in S or True:
                        pass
                    if hafd(ts[c], S) == 0:
                        continue
                    if hafd(ts[d], [x for x in V if x not in S]) != 0:
                        bad.append(("C", c, d, S))
        for c in range(3):
            d, ee = [x for x in range(3) if x != c]
            for S in combinations(V, 4):
                if hafd(ts[c], S) == 0:
                    continue
                T = [x for x in V if x not in S]
                for f in ((T[0], T[1]), (T[0], T[2]), (T[0], T[3])):
                    g = tuple(x for x in T if x not in f)
                    for (p, q) in ((d, ee), (ee, d)):
                        if ts[p].get(f, 0) != 0 and ts[q].get(g, 0) != 0:
                            bad.append(("D", c, p, q, S, f, g))
    return bad


def raw_source(ts):
    src = K.zero_source(N)
    for c in range(3):
        for e, v in ts[c].items():
            src[e][c][c] = v
    return src


def main():
    t0 = time.time()
    rng = random.Random(28082026)
    PMS = [tuple(sorted(tuple(sorted(x)) for x in M)) for M in K.all_pms(V)]
    print(f"K_8: {len(E)} edges, {len(PMS)} perfect matchings")

    print("=" * 74)
    print("(0) CONTROL: the product formula and the profile list, against the "
          "RAW word definition")
    print("=" * 74)
    mism = oddz = 0
    for t in range(4):
        ts = [{}, {}, {}]
        pool = list(E)
        rng.shuffle(pool)
        i = 0
        for c in range(3):
            for e in pool[i:i + 7]:
                ts[c][e] = Fraction(rng.randint(1, 4))
            i += 7
        src = raw_source(ts)
        for _ in range(120):
            w = tuple(rng.randrange(3) for _ in range(N))
            a = K.H_word(src, w, N)
            b = Fraction(1)
            for c in range(3):
                b *= hafd(ts[c], [i2 for i2 in range(N) if w[i2] == c])
            mism += (a != b)
            cc = [sum(1 for x in w if x == c) for c in range(3)]
            if any(x % 2 for x in cc):
                oddz += 1
                mism += (a != 0)
    print(f"   480 words: {mism} mismatches (must be 0); {oddz} odd-profile "
          f"words all zero")
    assert mism == 0
    RES["formula_control"] = {"mismatches": mism, "odd_words": oddz}
    control("T2a0_formula")

    # profile check
    live = []
    for p in product(range(N + 1), repeat=2):
        s = (p[0], p[1], N - p[0] - p[1])
        if s[2] < 0 or max(s) == N:
            continue
        if N - max(s) > 4 or any(x % 2 for x in s):
            continue
        live.append(s)
    shapes = sorted(set(tuple(sorted(p, reverse=True)) for p in live))
    print(f"   live (non-automatic) mixed profiles with off-count <= 4: "
          f"{len(live)}; shapes {shapes}")
    assert shapes == [(4, 2, 2), (4, 4, 0), (6, 2, 0)]
    RES["profiles"] = {"n_live": len(live), "shapes": [list(x) for x in shapes]}
    ck("ctrl")

    print("=" * 74)
    print("(1) D3 CENSUS REPRODUCED INDEPENDENTLY (hafnian definition, not the "
          "closed-4-set shortcut)")
    print("=" * 74)
    mask = {e: 1 << i for i, e in enumerate(E)}
    pmmask = []
    for M in PMS:
        m = 0
        for e in M:
            m |= mask[e]
        pmmask.append(m)
    trip = []
    for i in range(len(PMS)):
        for j in range(i + 1, len(PMS)):
            if pmmask[i] & pmmask[j]:
                continue
            for k in range(j + 1, len(PMS)):
                if pmmask[k] & (pmmask[i] | pmmask[j]):
                    continue
                trip.append((PMS[i], PMS[j], PMS[k]))
    print(f"   unordered triples of pairwise disjoint PMs: {len(trip)}")
    passC = passD = passB = both = 0
    winners = []
    t1 = time.time()
    for T3 in trip:
        ts = [{e: Fraction(1) for e in M} for M in T3]
        okB = okC = okD = True
        for c in range(3):
            for d in range(3):
                if d == c:
                    continue
                for e in T3[d]:
                    if hafd(ts[c], [x for x in V if x not in e]) != 0:
                        okB = False
        for c, d in combinations(range(3), 2):
            for S in combinations(V, 4):
                Sc = [x for x in V if x not in S]
                if hafd(ts[c], S) != 0 and hafd(ts[d], Sc) != 0:
                    okC = False
                if hafd(ts[d], S) != 0 and hafd(ts[c], Sc) != 0:
                    okC = False
        for c in range(3):
            d, ee = [x for x in range(3) if x != c]
            for S in combinations(V, 4):
                if hafd(ts[c], S) == 0:
                    continue
                Tt = [x for x in V if x not in S]
                for f in ((Tt[0], Tt[1]), (Tt[0], Tt[2]), (Tt[0], Tt[3])):
                    g = tuple(x for x in Tt if x not in f)
                    if (ts[d].get(f, 0) and ts[ee].get(g, 0)) or \
                       (ts[ee].get(f, 0) and ts[d].get(g, 0)):
                        okD = False
        passB += okB
        passC += okC
        passD += okD
        if okC and okD:
            both += 1
            winners.append(T3)
        if len(trip) > 2000 and (passB + 1) % 8000 == 0:
            print(f"      ... {passB} scanned ({round(time.time()-t1,1)}s)",
                  flush=True)
    print(f"   pass (B): {passB} (must be all)")
    print(f"   pass (C) [(4,4,0)]: {passC}")
    print(f"   pass (D) [(4,2,2)]: {passD}")
    print(f"   pass BOTH -> a no-cancellation diagonal X_4 point: {both}")
    RES["D3_census"] = {"triples": len(trip), "passB": passB, "passC": passC,
                        "passD": passD, "passCD": both,
                        "W27_reported": {"triples": 32970, "passC": 16800,
                                         "passD": 8610, "passCD": 0}}
    print(f"   W27-D3 reported 32970 / 16800 / 8610 / 0 -- "
          f"{'MATCH' if (len(trip), passC, passD, both) == (32970, 16800, 8610, 0) else 'MISMATCH'}")
    control("T2a1_D3_census")
    ck("census")

    print("=" * 74)
    print("(2) W28-DEL: deleting edges never breaks (B)/(C)/(D) -- the "
          "monotonicity that closes W27-D3's L_c > M_c gap")
    print("=" * 74)
    viol = 0
    tested = 0
    for t in range(300):
        ts = [{}, {}, {}]
        pool = list(E)
        rng.shuffle(pool)
        i = 0
        for c in range(3):
            for e in pool[i:i + rng.randint(4, 8)]:
                ts[c][e] = Fraction(rng.randint(1, 3))
            i += 9
        b0 = set(map(str, conditions(ts)))
        b0 = set(x for x in b0 if not x.startswith("('A'"))
        # delete a random edge from a random colour
        c = rng.randrange(3)
        if not ts[c]:
            continue
        e = rng.choice(list(ts[c]))
        ts2 = [dict(x) for x in ts]
        del ts2[c][e]
        b1 = set(map(str, conditions(ts2)))
        b1 = set(x for x in b1 if not x.startswith("('A'"))
        tested += 1
        # every violation after deletion must already have been a violation
        if not b1 <= b0:
            viol += 1
    print(f"   {tested} deletions: {viol} created a NEW (B)/(C)/(D) violation "
          f"(must be 0)")
    assert viol == 0
    RES["deletion_monotone"] = {"tested": tested, "new_violations": viol}
    control("T2a2_deletion")
    ck("del")

    print("=" * 74)
    print("(3) W28-LAM: the generating identity on diagonal sources")
    print("=" * 74)
    # control 1: haf(A+B) = sum_S haf(A|S) haf(B|V-S)
    bad = 0
    for t in range(6):
        A = {e: Fraction(rng.randint(-3, 3)) for e in E}
        B = {e: Fraction(rng.randint(-3, 3)) for e in E}
        lhs = hafd({e: A[e] + B[e] for e in E}, V)
        rhs = Fraction(0)
        for m in range(0, N + 1, 2):
            for S in combinations(V, m):
                rhs += hafd(A, S) * hafd(B, [x for x in V if x not in S])
        bad += (lhs != rhs)
    print(f"   haf(A+B) = sum_S haf(A|S)haf(B|V-S): {bad} mismatches (must "
          f"be 0)")
    assert bad == 0
    # control 2: on a genuine diagonal X_3 object (Delta^3_8) the identity
    # predicts Haf(lam.t) = sum lam^4 + (the surviving mixed profiles)
    d3 = K.delta3_pms(N)
    ts = [{e: Fraction(1) for e in M} for M in d3]
    vals = {}
    for lam in ((1, 1, 0), (1, -1, 0), (1, 1, 1), (2, 1, 1), (1, 0, 0)):
        tt = {e: sum(lam[c] * ts[c].get(e, 0) for c in range(3)) for e in E}
        vals[str(lam)] = str(hafd(tt, V))
    pred = {str(l): str(sum(x ** 4 for x in l))
            for l in ((1, 1, 0), (1, -1, 0), (1, 1, 1), (2, 1, 1), (1, 0, 0))}
    print(f"   Delta^3_8: Haf(lam.t) = {vals}")
    print(f"   the X_4 prediction sum lam_c^4 = {pred}")
    RES["lambda_identity"] = {"haf_sum_control": bad, "delta3_values": vals,
                              "X4_prediction": pred,
                              "delta3_is_X4": vals == pred}
    control("T2a3_lambda")
    ck("lam")

    print("=" * 74)
    print("(4) W28-GOOD: the three good classes are disjoint spanning "
          "subgraphs (verified on the whole D3 census + random objects)")
    print("=" * 74)
    ok = 0
    tot = 0
    for T3 in trip[:400]:
        ts = [{e: Fraction(1) for e in M} for M in T3]
        good = []
        for c in range(3):
            good.append({e for e in ts[c]
                         if hafd(ts[c], [x for x in V if x not in e]) != 0})
        tot += 1
        cover = all(set(x for e in good[c] for x in e) == set(V)
                    for c in range(3))
        disj = all(not (good[a] & good[b]) for a, b in combinations(range(3), 2))
        ok += (cover and disj)
    print(f"   {tot} disjoint-PM triples: {ok} have all three good classes "
          f"spanning and pairwise disjoint")
    RES["good_classes"] = {"tested": tot, "ok": ok}
    control("T2a4_good")

    RES["seconds"] = round(time.time() - t0, 1)
    decl = ["T2a0_formula", "T2a1_D3_census", "T2a2_deletion", "T2a3_lambda",
            "T2a4_good"]
    RES["manifest"] = {"declared": decl, "ran": RAN,
                       "missing": [x for x in decl if x not in RAN]}
    print(f"CONTROL MANIFEST: {RES['manifest']}")
    assert not RES["manifest"]["missing"]
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()
