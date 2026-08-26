#!/usr/bin/env python3
r"""UNAUDITED PROBE (W19-CENSUS) -- controls for the stratum-(ii) Burnside sum.

UNAUDITED.  Nothing here is a proved claim of the repository.

The orbit count of stratum (ii) rests on the per-vertex-cycle factor

    Fix(pi, tau) = sum over cubic C with pi(C)=C of
                   prod over vertex cycles of pi of
                      [ cycletype(pi^L on E_p) == cycletype(tau^L) ]
                      * |C_{S_3}(tau^L)|.

Here that factor is BRUTE FORCED (independent DFS over all sigma) on cases
where it is NONZERO and pi != id -- the first run of this control only hit
zero cases, which is why it is repeated properly here -- plus the mutation
control (a wrong centraliser table must disagree).
"""
from __future__ import annotations

import json
import os
import sys
from itertools import permutations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w19c_lib import EDGES, EIDX, N, NE, edges_to_mask, S3  # noqa: E402
from w19c_low import cubic_graphs_labelled  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
BIJ = list(permutations(range(3)))
CENT_TRUE = {(1, 1, 1): 6, (1, 2): 2, (3,): 3}
CENT_BAD = {(1, 1, 1): 6, (1, 2): 3, (3,): 2}


def cyc_type_perm3(t):
    seen = [False] * 3
    ct = []
    for i in range(3):
        if seen[i]:
            continue
        L = 0
        j = i
        while not seen[j]:
            seen[j] = True
            j = t[j]
            L += 1
        ct.append(L)
    return tuple(sorted(ct))


def ppow(t, k):
    r = tuple(range(3))
    for _ in range(k):
        r = tuple(t[x] for x in r)
    return r


def incid(C):
    inc = {v: [] for v in range(N)}
    for e in C:
        u, v = min(e), max(e)
        inc[u].append((u, v))
        inc[v].append((u, v))
    for v in inc:
        inc[v].sort()
    return inc


def formula(C, pi, tau, CENT):
    inc = incid(C)
    seen = [False] * N
    prod = 1
    for p0 in range(N):
        if seen[p0]:
            continue
        L = 0
        j = p0
        while not seen[j]:
            seen[j] = True
            j = pi[j]
            L += 1
        # cycle type of pi^L acting on E_{p0}
        elts = inc[p0]
        idx = {e: i for i, e in enumerate(elts)}

        def piL(e):
            a, b = e
            for _ in range(L):
                a, b = pi[a], pi[b]
            return (min(a, b), max(a, b))

        s2 = [False] * len(elts)
        ct = []
        for i in range(len(elts)):
            if s2[i]:
                continue
            k = 0
            j2 = i
            while not s2[j2]:
                s2[j2] = True
                j2 = idx[piL(elts[j2])]
                k += 1
            ct.append(k)
        rho = tuple(sorted(ct))
        t = cyc_type_perm3(ppow(tau, L))
        if rho != t:
            return 0
        prod *= CENT[t]
    return prod


def brute(C, pi, tau):
    """count sigma with sigma_{pi(p)}(pi(e)) = tau(sigma_p(e)); DFS."""
    inc = incid(C)
    order = list(range(N))
    sig = [None] * N

    def cons_ok(p):
        for e in inc[p]:
            a, b = e
            pe = (min(pi[a], pi[b]), max(pi[a], pi[b]))
            q = pi[p]
            if sig[q] is None:
                continue
            i1 = inc[p].index(e)
            i2 = inc[q].index(pe)
            if sig[q][i2] != tau[sig[p][i1]]:
                return False
        # also the incoming constraint p = pi(p') for assigned p'
        for pp in range(N):
            if pi[pp] != p or sig[pp] is None:
                continue
            for e in inc[pp]:
                a, b = e
                pe = (min(pi[a], pi[b]), max(pi[a], pi[b]))
                i1 = inc[pp].index(e)
                i2 = inc[p].index(pe)
                if sig[p][i2] != tau[sig[pp][i1]]:
                    return False
        return True

    cnt = 0

    def rec(k):
        nonlocal cnt
        if k == N:
            cnt += 1
            return
        p = order[k]
        for b in BIJ:
            sig[p] = b
            if cons_ok(p):
                rec(k + 1)
        sig[p] = None

    rec(0)
    return cnt


CUBIC = cubic_graphs_labelled()
C0 = None
best = None
tests = []
# find (C, pi, tau) with pi != id and formula != 0
for C in CUBIC[:400]:
    m0 = edges_to_mask(C)
    for pi in permutations(range(N)):
        if pi == tuple(range(N)):
            continue
        nm = 0
        for (a, b) in C:
            x, y = pi[a], pi[b]
            nm |= 1 << EIDX[(min(x, y), max(x, y))]
        if nm != m0:
            continue
        for tau in S3:
            if tau == tuple(range(3)):
                continue          # need tau != id for the mutation to bite
            f = formula(C, pi, tau, CENT_TRUE)
            if f:
                tests.append((C, pi, tau, f))
        if len(tests) >= 6:
            break
    if len(tests) >= 6:
        break

RES = {"cases": []}
print("non-trivial (pi != id, Fix != 0) cases found:", len(tests))
allok = True
for (C, pi, tau, f) in tests[:6]:
    b = brute(C, pi, tau)
    ok = (b == f)
    allok = allok and ok
    print("  pi=%s tau=%s : formula=%d brute=%d  %s"
          % (pi, tau, f, b, "OK" if ok else "MISMATCH"))
    RES["cases"].append(dict(cubic=[list(e) for e in C], pi=list(pi),
                             tau=list(tau), formula=f, brute=b, agree=ok))
# identity case
Cid = CUBIC[0]
f = formula(Cid, tuple(range(N)), S3[0], CENT_TRUE)
b = brute(Cid, tuple(range(N)), S3[0])
print("  pi=id tau=id : formula=%d brute=%d (expect 6^8=%d)  %s"
      % (f, b, 6 ** 8, "OK" if f == b == 6 ** 8 else "MISMATCH"))
RES["identity_case"] = dict(formula=f, brute=b, expect=6 ** 8,
                            agree=(f == b == 6 ** 8))
allok = allok and f == b == 6 ** 8
RES["all_agree"] = allok

# MUTATION: wrong centraliser table must disagree on some nonzero case
mut_fires = False
for (C, pi, tau, f) in tests[:6]:
    if formula(C, pi, tau, CENT_BAD) != brute(C, pi, tau):
        mut_fires = True
        break
RES["MUTATION_wrong_centralisers_fires"] = mut_fires
print("MUTATION control (wrong centraliser table disagrees):", mut_fires)

json.dump(RES, open(os.path.join(HERE, "results_ctl_burnside.json"), "w"),
          indent=1)
