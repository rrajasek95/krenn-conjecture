#!/usr/bin/env python3
"""W33 / T5 -- the ADVERSARIAL BUILDER, seeded from genuinely NON-DIAGONAL
exact d=2 sources (the most dangerous region of the squeeze picture).

Fix an exact d=2 source B on K_8 and install it as the {0,1} restriction of a
candidate X_4 point (W32-RES says the restrictions must be exact d=2 sources,
so this is the correct seed).  Unknowns: the five cells per edge that involve
colour 2 -- A_e[2][2], A_e[2][0], A_e[2][1], A_e[0][2], A_e[1][2].

Layers (each exactly solvable given the one above; no relaxation):
  L1  one site in colour 2 (profiles (k,7-k,1), always imposed): homogeneous
      linear -- the colour-2 star at j must lie in Ker_j(B,{0,1}).  Every
      colour-2 cross cell lies in exactly ONE such star, so
      (+)_j Ker_j is an exact parametrisation of the 112 cross cells.
  L2  two sites in colour 2 (imposed unless the {0,1} part splits 3-3):
      LINEAR in the 28 cells A_e[2][2] once L1 is fixed -- solve exactly.
  L3  the remaining imposed words (>= 3 sites in colour 2): the score.

Calibration (must fire): at k = 3 real sources exist, so the machine must
produce one; a builder that cannot fire on a satisfiable instance is not a
control (ledger 18/20).  Searches are never evidence -- only a HIT is.

Usage: run_05_builder.py <seconds> <seed> <tag> [k]
"""
from __future__ import annotations

import itertools
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w33_core import Manifest, edges, require  # noqa: E402

N = 8
V = tuple(range(N))
EDG = edges(N)
EIX = {e: i for i, e in enumerate(EDG)}
SEC = int(sys.argv[1]) if len(sys.argv) > 1 else 3600
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 55055
TAG = sys.argv[3] if len(sys.argv) > 3 else "A"
KLEV = int(sys.argv[4]) if len(sys.argv) > 4 else 4
OUT = os.path.join(HERE, f"results_t5_{TAG}.json")
PRIMES = (13, 31, 37, 43)       # all = 1 mod 3 (ledger 19)
rng = random.Random(SEED)
MAN = Manifest(["k3_calibration", "seed_nondiagonal", "independent_recheck"])

SUBS = [tuple(s) for k in range(0, N + 1, 2) for s in
        itertools.combinations(V, k)]
PM_CACHE = {}


def pms(sites):
    if sites in PM_CACHE:
        return PM_CACHE[sites]
    if not sites:
        out = [()]
    else:
        h, rest = sites[0], sites[1:]
        out = []
        for i, x in enumerate(rest):
            for M in pms(rest[:i] + rest[i + 1:]):
                out.append(((h, x),) + M)
    PM_CACHE[sites] = out
    return out


def offcount(w):
    return N - max(w.count(c) for c in range(3))


IMP = {k: [w for w in itertools.product(range(3), repeat=N)
           if offcount(w) <= k] for k in (3, 4)}


# ------------------------------------------------- 2-colour source as arrays
# B[i][j][a][b] with B[j][i][b][a] mirrored; entries are ints mod p.
def new_B(p):
    return [[[[0, 0], [0, 0]] for _ in range(N)] for _ in range(N)]


def setB(B, u, v, a, b, val):
    B[u][v][a][b] = val
    B[v][u][b][a] = val


def hafB_tables(B, p):
    """HB[S][code] = haf(B restricted to S) at the word coded in base 2 over
    the sites of S (in increasing order).  All even S."""
    HB = {}
    for S in SUBS:
        k = len(S)
        arr = [0] * (1 << k)
        if k == 0:
            arr[0] = 1
            HB[S] = arr
            continue
        idx = {s: i for i, s in enumerate(S)}
        Msub = pms(S)
        for code in range(1 << k):
            w = [(code >> i) & 1 for i in range(k)]
            tot = 0
            for M in Msub:
                pr = 1
                for (u, v) in M:
                    c = B[u][v][w[idx[u]]][w[idx[v]]]
                    if c == 0:
                        pr = 0
                        break
                    pr = pr * c % p
                if pr:
                    tot = (tot + pr) % p
            arr[code] = tot
        HB[S] = arr
    return HB


def code_of(S, w):
    c = 0
    for i, s in enumerate(S):
        if w[s]:
            c |= 1 << i
    return c


def is_exact2_arr(B, p):
    HB = hafB_tables(B, p)
    arr = HB[V]
    for code in range(256):
        tgt = 1 if code in (0, 255) else 0
        if arr[code] % p != tgt:
            return False, HB
    return True, HB


# ------------------------------------------------------- linear algebra F_p
def rref_p(rows, rhs, nc, p):
    m = [list(r) + [b] for r, b in zip(rows, rhs)]
    piv, rr = [], 0
    for c in range(nc):
        pr = None
        for i in range(rr, len(m)):
            if m[i][c] % p:
                pr = i
                break
        if pr is None:
            continue
        m[rr], m[pr] = m[pr], m[rr]
        inv = pow(m[rr][c], p - 2, p)
        m[rr] = [x * inv % p for x in m[rr]]
        for i in range(len(m)):
            if i != rr and m[i][c] % p:
                f = m[i][c]
                m[i] = [(x - f * y) % p for x, y in zip(m[i], m[rr])]
        piv.append(c)
        rr += 1
    ok = all(not (m[i][nc] % p and not any(x % p for x in m[i][:nc]))
             for i in range(len(m)))
    return piv, m, ok


def kernel_p(rows, nc, p):
    piv, m, _ = rref_p(rows, [0] * len(rows), nc, p)
    out = []
    for f in [c for c in range(nc) if c not in piv]:
        v = [0] * nc
        v[f] = 1
        for i, c in enumerate(piv):
            v[c] = (-m[i][f]) % p
        out.append(v)
    return out


def star_kernels(HB, p):
    """Ker_j for every site: columns (r, d), r != j, d in {0,1}."""
    out = []
    for j in range(N):
        VP = [x for x in range(N) if x != j]
        cols = [(r, d) for r in VP for d in range(2)]
        cix = {c: i for i, c in enumerate(cols)}
        rows = []
        for code in range(1 << 7):
            u = {VP[i]: (code >> i) & 1 for i in range(7)}
            row = [0] * 14
            nz = False
            for r in VP:
                S = tuple(x for x in range(N) if x != j and x != r)
                cc = 0
                for i, s in enumerate(S):
                    if u[s]:
                        cc |= 1 << i
                val = HB[S][cc]
                if val % p:
                    row[cix[(r, u[r])]] = val % p
                    nz = True
            if nz:
                rows.append(row)
        out.append((cols, kernel_p(rows, 14, p)))
    return out


# ------------------------------------------------------------ the machine
def build(B, HB, KER, p, words3, rngl, l1=None, a22=None):
    """One L1 sample -> (A, nbad, kerdim_total) or None if L2 infeasible."""
    A = [[[[0] * 3 for _ in range(3)] for _ in range(N)] for _ in range(N)]
    for u in range(N):
        for v in range(N):
            if u == v:
                continue
            for a in range(2):
                for b in range(2):
                    A[u][v][a][b] = B[u][v][a][b]
    tot = 0
    for j in range(N):
        cols, basis = KER[j]
        tot += len(basis)
        if l1 is not None:
            vec = [0] * len(cols)
            for i, (r, d) in enumerate(cols):
                vec[i] = l1[j][r][d] % p
        else:
            if not basis:
                continue
            vec = [0] * len(cols)
            for bv in basis:
                lam = rngl.randrange(p)
                if lam:
                    vec = [(x + lam * y) % p for x, y in zip(vec, bv)]
        for i, (r, d) in enumerate(cols):
            A[j][r][2][d] = vec[i]
            A[r][j][d][2] = vec[i]
    # ---- L2: linear in the 28 cells A_e[2][2]
    rows, rhs = [], []
    for (u, v) in EDG:
        rest = tuple(x for x in range(N) if x not in (u, v))
        for code in range(1 << 6):
            w = [0] * N
            w[u] = w[v] = 2
            for i, s in enumerate(rest):
                w[s] = (code >> i) & 1
            if offcount(tuple(w)) > KLEV:
                continue
            row = [0] * len(EDG)
            row[EIX[(u, v)]] = HB[rest][code]
            val = 0
            for ri, r in enumerate(rest):
                c1 = A[u][r][2][w[r]]
                if not c1:
                    continue
                for si, s in enumerate(rest):
                    if s == r:
                        continue
                    c2 = A[v][s][2][w[s]]
                    if not c2:
                        continue
                    left = tuple(x for x in rest if x not in (r, s))
                    val = (val + c1 * c2 * HB[left][code_of(left, w)]) % p
            if not row[EIX[(u, v)]] % p and not val % p:
                continue
            rows.append(row)
            rhs.append((-val) % p)
    ncol = len(EDG)
    basis = [None] * ncol
    for r0, b0 in zip(rows, rhs):
        v = list(r0) + [b0]
        for c in range(ncol):
            if not v[c] % p:
                continue
            if basis[c] is None:
                inv = pow(v[c], p - 2, p)
                basis[c] = [x * inv % p for x in v]
                v = None
                break
            f = v[c]
            v = [(x - f * y) % p for x, y in zip(v, basis[c])]
        if v is not None and v[ncol] % p:
            return None, tot
    piv = [c for c in range(ncol) if basis[c] is not None]
    free = [c for c in range(ncol) if basis[c] is None]
    sol = [0] * ncol
    if a22 is None:
        for c in free:
            sol[c] = rngl.choice([0, 0, 1, p - 1, rngl.randrange(p)])
    else:
        for c in free:
            sol[c] = a22[c] % p
    for c in range(ncol - 1, -1, -1):
        if basis[c] is None:
            continue
        acc = basis[c][ncol]
        for c2 in range(c + 1, ncol):
            if basis[c][c2] % p:
                acc = (acc - basis[c][c2] * sol[c2]) % p
        sol[c] = acc % p
    if a22 is not None:
        for c in piv:
            if (sol[c] - a22[c]) % p:
                return None, tot
    for i, (u, v) in enumerate(EDG):
        A[u][v][2][2] = sol[i]
        A[v][u][2][2] = sol[i]
    # ---- L3: score the words with >= 3 sites in colour 2
    nbad = 0
    bad0 = None
    for w in words3:
        const = len(set(w)) == 1
        tot_h = 0
        for M in PM_V:
            pr = 1
            for (x, y) in M:
                c = A[x][y][w[x]][w[y]]
                if c == 0:
                    pr = 0
                    break
                pr = pr * c % p
            if pr:
                tot_h = (tot_h + pr) % p
        # amplitude form: the constant word only has to be NONZERO (the
        # colour-2 block can then be rescaled by an 8th root, over an
        # extension if necessary); every other imposed word must vanish.
        if (tot_h == 0) if const else (tot_h != 0):
            nbad += 1
            if bad0 is None:
                bad0 = w
            if nbad > 40:
                break
    return (A, nbad, tot, len(EDG) - len(piv))


PM_V = pms(V)


# ------------------------------------------------------------------- seeds
def cycle_seed(p, perm=None):
    B = new_B(p)
    perm = list(range(N)) if perm is None else perm
    for i in range(N):
        u, v = perm[i], perm[(i + 1) % N]
        a = i % 2
        setB(B, u, v, a, a, 1)
    return B


def rand_seed(p, kind, rngl):
    """Exact d=2 source over F_p by site completion; kind in
    {diag, nondiag, chords}."""
    for _ in range(40):
        perm = list(range(N))
        rngl.shuffle(perm)
        B = cycle_seed(p, perm)
        if kind == "chords":
            # the free one-class chord family (W33-D2): all cells on the
            # chords inside ONE bipartition class of the cycle
            cls = [perm[i] for i in range(0, N, 2)] if rngl.random() < .5 \
                else [perm[i] for i in range(1, N, 2)]
            for (u, v) in itertools.combinations(cls, 2):
                for a in range(2):
                    for b in range(2):
                        if rngl.random() < 0.6:
                            setB(B, u, v, a, b, rngl.randrange(1, p))
            ok, HB = is_exact2_arr(B, p)
            if ok:
                return B, HB
            continue
        j = rngl.randrange(N)
        if kind == "nondiag":
            for _ in range(rngl.randrange(1, 8)):
                (u, v) = EDG[rngl.randrange(len(EDG))]
                if j in (u, v):
                    continue
                setB(B, u, v, rngl.randrange(2), rngl.randrange(2),
                     rngl.randrange(1, p))
        for r in range(N):
            if r != j:
                for a in range(2):
                    for b in range(2):
                        setB(B, j, r, a, b, 0)
        HB = hafB_tables(B, p)
        # solve the two inhomogeneous star systems at j
        VP = [x for x in range(N) if x != j]
        cols = [(r, d) for r in VP for d in range(2)]
        cix = {c: i for i, c in enumerate(cols)}
        rows, rhs = [], {0: [], 1: []}
        for code in range(1 << 7):
            u = {VP[i]: (code >> i) & 1 for i in range(7)}
            row = [0] * 14
            for r in VP:
                S = tuple(x for x in range(N) if x != j and x != r)
                cc = 0
                for i, s in enumerate(S):
                    if u[s]:
                        cc |= 1 << i
                row[cix[(r, u[r])]] = HB[S][cc] % p
            rows.append(row)
            const = len(set(u.values())) == 1
            for c in range(2):
                rhs[c].append(1 if (const and list(u.values())[0] == c) else 0)
        good = True
        for c in range(2):
            piv, m, ok = rref_p(rows, rhs[c], 14, p)
            if not ok:
                good = False
                break
            sol = [0] * 14
            for i, cc in enumerate(piv):
                sol[cc] = m[i][14]
            ker = kernel_p(rows, 14, p)
            for bv in ker:
                lam = rngl.randrange(p)
                if lam:
                    sol = [(x + lam * y) % p for x, y in zip(sol, bv)]
            for i, (r, d) in enumerate(cols):
                setB(B, j, r, c, d, sol[i])
        if not good:
            continue
        ok, HB = is_exact2_arr(B, p)
        if ok:
            return B, HB
    return None, None


def ncross_of(B, p):
    return sum(1 for (u, v) in EDG for a in range(2) for b in range(2)
               if a != b and B[u][v][a][b] % p)


def main():
    global KLEV
    t0 = time.time()
    R = {"tag": TAG, "seed": SEED, "k": KLEV, "status": "UNAUDITED",
         "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")).read()
         .strip(), "hits": []}
    W = {k: [w for w in IMP[k] if sum(1 for x in w if x == 2) >= 3]
         for k in (3, 4)}
    print("imposed k=4", len(IMP[4]), "L3 words", len(W[4]),
          "| k=3", len(IMP[3]), "L3", len(W[3]), flush=True)

    # ---------- calibration (must fire): the DIAGONAL PM-TRIPLE is a real
    # X_3 point (every colour class of an off-count<=3 word has odd size or
    # is not a union of its own PM's edges), so the layered machine must
    # accept it at k=3 -- and must REJECT it at k=4, where the profile
    # (4,2,2) words break it (ledger 18: a control on both sides).
    keep = KLEV
    p = 13
    B = cycle_seed(p)
    ok, HB = is_exact2_arr(B, p)
    require(ok, "cycle seed is not an exact d=2 source")
    KER = star_kernels(HB, p)
    M2 = [(0, 2), (1, 3), (4, 6), (5, 7)]
    a22 = [0] * len(EDG)
    for e in M2:
        a22[EIX[e]] = 1
    l1 = [[[0, 0] for _ in range(N)] for _ in range(N)]
    KLEV = 3
    out = build(B, HB, KER, p, W[3], rng, l1=l1, a22=a22)
    require(out[0] is not None, "k=3 calibration: L2 rejected the known "
                                "X_3 point")
    A3, nbad3, td, nf = out
    require(nbad3 == 0, f"k=3 CALIBRATION FAILED: known X_3 point scored "
                        f"{nbad3} violations")
    # independent full recheck of every imposed word at k=3
    badc = 0
    for w in IMP[3]:
        tgt = 1 if len(set(w)) == 1 else 0
        tt = 0
        for M in PM_V:
            pr = 1
            for (x, y) in M:
                c = A3[x][y][w[x]][w[y]]
                if c == 0:
                    pr = 0
                    break
                pr = pr * c % p
            tt = (tt + pr) % p
        if tt != tgt:
            badc += 1
    require(badc == 0, "k=3 witness fails the independent full recheck")
    KLEV = 4
    out4 = build(B, HB, KER, p, W[4], rng, l1=l1, a22=a22)
    nbad4 = out4[1] if out4[0] is not None else -1
    require(nbad4 != 0, "k=4 control FAILED: the known X_3 point was "
                        "accepted at k=4 (the machine is vacuous there)")
    MAN.mark("k3_calibration")
    MAN.mark("independent_recheck")
    R["calibration"] = {"k3_nbad": nbad3, "k3_full_recheck_bad": badc,
                        "k4_nbad_on_X3_point": nbad4, "kerdim_total": td}
    print("calibration: k=3 accepts the diagonal PM-triple (0 violations); "
          "k=4 rejects it with", nbad4, "violations", flush=True)
    KLEV = keep
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)

    # ---------- the hunt at k = KLEV from NON-DIAGONAL seeds
    best = {"nbad": 10 ** 9}
    hist, tried, nondiag = {}, 0, 0
    while time.time() - t0 < SEC:
        p = PRIMES[rng.randrange(len(PRIMES))]
        kind = rng.choice(["nondiag", "chords", "chords", "nondiag", "diag"])
        B, HB = rand_seed(p, kind, rng)
        if B is None:
            hist["no_seed"] = hist.get("no_seed", 0) + 1
            continue
        nc = ncross_of(B, p)
        if nc:
            nondiag += 1
        KER = star_kernels(HB, p)
        kd = [len(KER[j][1]) for j in range(N)]
        tag = f"{kind}_ncross{min(nc,8)}_ker{sum(kd)}"
        for _ in range(10):
            tried += 1
            out = build(B, HB, KER, p, W[KLEV], rng)
            if out[0] is None:
                hist["L2_infeasible"] = hist.get("L2_infeasible", 0) + 1
                continue
            A, nbad, td, nf = out
            hist[tag] = hist.get(tag, 0) + 1
            if nbad < best["nbad"]:
                best = {"nbad": nbad, "p": p, "seed_ncross": nc,
                        "kerdims": kd, "kind": kind, "free_A22": nf}
                print("  best nbad", nbad, best, flush=True)
            if nbad == 0:
                R["hits"].append({"p": p, "kind": kind, "kerdims": kd,
                                  "seed_ncross": nc,
                                  "cells": {f"{u}{v}": A[u][v]
                                            for (u, v) in EDG}})
                print("*** HIT at k =", KLEV, "p =", p, flush=True)
        if tried % 40 < 10:
            R["progress"] = {"tried": tried, "elapsed": time.time() - t0,
                             "nondiag_seeds": nondiag, "best": best,
                             "hist": hist}
            with open(OUT + ".tmp", "w") as fh:
                json.dump(R, fh, indent=1, sort_keys=True)
            os.replace(OUT + ".tmp", OUT)
    require(nondiag > 0, "no non-diagonal seed was ever produced -- the "
                         "builder never entered its target region")
    MAN.mark("seed_nondiagonal")
    R["progress"] = {"tried": tried, "elapsed": time.time() - t0,
                     "nondiag_seeds": nondiag, "best": best, "hist": hist}
    R["manifest"] = MAN.assert_complete()
    with open(OUT + ".tmp", "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    os.replace(OUT + ".tmp", OUT)
    print("wrote", OUT, best, "hits", len(R["hits"]))


if __name__ == "__main__":
    main()
