#!/usr/bin/env python3
"""W28 T2c -- the diagonal CANCELLATION-STRATUM enumeration, bitmasked.

A vanishing hafnian has npm = 0 or npm >= 2 (npm = 1 is a single nonzero
monomial), so every diagonal X_4 skeleton triple at N = 8 must satisfy

  (B') for c != d and e in L_d:                    npm(L_c | V - e)  != 1
  (C') for c != d and |S| = 4:      not( npm(L_c|S) = 1 and npm(L_d|V-S) = 1 )
  (D') for {c,d,e} and |S| = 4 with V - S = f + g, f in L_d, g in L_e:
                                                   npm(L_c|S) != 1
  (A') npm(L_c | V) >= 1.

All four become BITMASK tests once we precompute, per candidate class L:

    bad(L)   = { e : npm(L|V - e) = 1 }                   (28-bit mask)
    one4(L)  = { S : |S| = 4, npm(L|S) = 1 }              (70-bit mask)
    pos4(L)  = { S : |S| = 4, npm(L|S) >= 1 }
    spl(L,M) = { S : V - S = f + g with f in L, g in M }  (70-bit mask)

Then (B') is  L_d & bad(L_c) == 0,  (C') is  one4(L_c) & rev(one4(L_d)) == 0
with rev the complementation permutation of the 70 four-sets, and (D') is
one4(L_c) & rev(spl(L_d, L_e) | spl(L_e, L_d)) == 0.

W28-DEL (run_t2a) already showed the no-cancellation stratum reduces exactly
to the disjoint-PM triples, which are exhausted and empty; so every survivor
here would have to cancel.

argv: [budget seconds per profile]
"""
from __future__ import annotations

import json
import sys
import time
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x4empty-w28-2026-08-18")
sys.path.insert(0, BASE)
import w28_core as K                                              # noqa: E402

N = 8
V = tuple(range(N))
E = list(combinations(V, 2))
EI = {e: i for i, e in enumerate(E)}
FOURS = list(combinations(V, 4))
FI = {S: i for i, S in enumerate(FOURS)}
REV = [FI[tuple(x for x in V if x not in S)] for S in FOURS]
RES = {}
OUT = f"{BASE}/results_t2c_enum.json"


def ck(tag=""):
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def pm_masks(S):
    out = []
    for M in K.all_pms(S):
        m = 0
        for e in M:
            m |= 1 << EI[K.ekey(*e)]
        out.append(m)
    return out


PM_FULL = pm_masks(V)
PM_SIX = {}
for e in E:
    PM_SIX[e] = pm_masks(tuple(x for x in V if x not in e))
PM_FOUR = {S: pm_masks(S) for S in FOURS}
SPLITS = {}
for S in FOURS:
    T = tuple(x for x in V if x not in S)
    SPLITS[S] = [((T[0], T[1]), (T[2], T[3])),
                 ((T[0], T[2]), (T[1], T[3])),
                 ((T[0], T[3]), (T[1], T[2]))]


def npm(L, pms):
    return sum(1 for m in pms if m & L == m)


def profile_of(L):
    bad = 0
    for i, e in enumerate(E):
        if npm(L, PM_SIX[e]) == 1:
            bad |= 1 << i
    one4 = 0
    pos4 = 0
    for i, S in enumerate(FOURS):
        k = npm(L, PM_FOUR[S])
        if k == 1:
            one4 |= 1 << i
        if k >= 1:
            pos4 |= 1 << i
    return bad, one4, pos4


def rev_mask(m):
    out = 0
    i = 0
    while m:
        if m & 1:
            out |= 1 << REV[i]
        m >>= 1
        i += 1
    return out


def spl_mask(L, M):
    """4-sets S whose complement splits into an L-edge and an M-edge."""
    out = 0
    for i, S in enumerate(FOURS):
        for (f, g) in SPLITS[S]:
            fi, gi = 1 << EI[K.ekey(*f)], 1 << EI[K.ekey(*g)]
            if ((L & fi) and (M & gi)) or ((M & fi) and (L & gi)):
                out |= 1 << i
                break
    return out


def family(extra):
    """PM plus `extra` further edges, deduplicated."""
    out = set()
    for m in PM_FULL:
        rest = [i for i in range(28) if not (m >> i & 1)]
        if extra == 0:
            out.add(m)
        elif extra == 1:
            for i in rest:
                out.add(m | (1 << i))
        elif extra == 2:
            for i, j in combinations(rest, 2):
                out.add(m | (1 << i) | (1 << j))
        else:
            for t in combinations(rest, extra):
                mm = m
                for i in t:
                    mm |= 1 << i
                out.add(mm)
    return sorted(out)


def main():
    t0 = time.time()
    budget = int(sys.argv[1]) if len(sys.argv) > 1 else 900
    fams = {}
    info = {}
    for extra in (0, 1, 2):
        f = family(extra)
        fams[extra] = f
        info[extra] = {}
        t1 = time.time()
        for L in f:
            info[extra][L] = profile_of(L)
        print(f"   |L| = {4+extra}: {len(f)} classes, invariants precomputed "
              f"({round(time.time()-t1,1)}s)", flush=True)
    RES["families"] = {str(4 + k): len(v) for k, v in fams.items()}
    ck("fams")
    allinfo = {}
    for k, d in info.items():
        allinfo.update(d)
    revone = {L: rev_mask(v[1]) for L, v in allinfo.items()}

    for prof in ((0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 0, 2), (0, 1, 2),
                 (1, 1, 1), (0, 2, 2), (1, 1, 2)):
        t1 = time.time()
        A, B, C = fams[prof[0]], fams[prof[1]], fams[prof[2]]
        scanned = 0
        pairs = 0
        surv = []
        stop = False
        for L0 in A:
            b0, o0, p0 = allinfo[L0]
            r0 = revone[L0]
            for L1 in B:
                if L0 & L1:
                    continue
                b1, o1, p1 = allinfo[L1]
                if (L1 & b0) or (L0 & b1):
                    continue
                if (o0 & revone[L1]) or (o1 & r0):
                    continue
                pairs += 1
                used = L0 | L1
                for L2 in C:
                    if L2 & used:
                        continue
                    scanned += 1
                    b2, o2, p2 = allinfo[L2]
                    if (L2 & b0) or (L2 & b1) or (used & b2):
                        continue
                    if (o0 & revone[L2]) or (o2 & r0):
                        continue
                    if (o1 & revone[L2]) or (o2 & revone[L1]):
                        continue
                    # (D')
                    if o0 & rev_mask(spl_mask(L1, L2)):
                        continue
                    if o1 & rev_mask(spl_mask(L0, L2)):
                        continue
                    if o2 & rev_mask(spl_mask(L0, L1)):
                        continue
                    surv.append((L0, L1, L2))
                    print(f"      *** SURVIVOR {prof}: "
                          f"{[sorted(E[i] for i in range(28) if L >> i & 1) for L in (L0,L1,L2)]}",
                          flush=True)
            if time.time() - t0 > budget * (1 + list(
                    ((0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 0, 2), (0, 1, 2),
                     (1, 1, 1), (0, 2, 2), (1, 1, 2))).index(prof)):
                stop = True
                break
        print(f"   sizes {tuple(4+p for p in prof)}: {pairs} surviving pairs, "
              f"{scanned} triples scanned, {len(surv)} survivors"
              f"{' [BUDGET CUT]' if stop else ' [COMPLETE]'} "
              f"({round(time.time()-t1,1)}s)", flush=True)
        RES.setdefault("profiles", {})[str(tuple(4 + p for p in prof))] = {
            "pairs": pairs, "scanned": scanned, "survivors": len(surv),
            "complete": not stop,
            "examples": [[sorted(E[i] for i in range(28) if L >> i & 1)
                          for L in s] for s in surv[:3]]}
        ck(f"prof{prof}")
    RES["seconds"] = round(time.time() - t0, 1)
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()
