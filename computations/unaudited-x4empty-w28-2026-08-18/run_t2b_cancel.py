#!/usr/bin/env python3
"""W28 T2b -- THE DIAGONAL CANCELLATION STRATUM AT N = 8.

Two attacks, both mandated by the ledger.

(1) THE ADVERSARIAL BUILDER (ledger 20).  On the diagonal stratum the source is
three weight functions t^c on E(K_8) and, at any site z, H_w is LINEAR in the
seven star weights t^c_{zy} of the colour c = w_z:

    H_w = sum_{y != z} t^c_{zy} * prod_d haf(t^d | S_d(w) - z - y).

So one exact 7-unknown solve per (site, colour) makes every k-near-constant
word with that colour at that site exact.  Cycling over the 8 sites and 3
colours is an exact coordinate descent on the whole diagonal X_k variety --
the strongest builder available, and it is run from many starts over Q AND
over Q(omega) (ledger 19: cube roots of unity are structural here).
CALIBRATION: the same walk is run at k = 2 and k = 3, where diagonal points
DO exist -- a builder that never succeeds anywhere would be worthless.

(2) THE SKELETON ENUMERATION with the cancellation filter (W25's technique
adapted).  A vanishing hafnian either has NO matching (npm = 0) or cancels
(npm >= 2): npm = 1 is impossible.  So every skeleton triple must satisfy

  (B') npm(L_c | V - e) != 1            for every c != d and e in L_d
  (C') not ( npm(L_c|S) = 1 and npm(L_d|V-S) = 1 )      c != d, |S| = 4
  (D') npm(L_c|S) != 1 whenever V - S splits into an L_d edge and an L_e edge

plus npm(L_c|V) >= 1.  W28-DEL (run_t2a) says the NO-cancellation case is
exactly the disjoint-PM enumeration (done, empty), so the residual stratum is
the one where some class has >= 2 matchings on some vanishing set.

argv: <stage: build|enum|all> [budget]
"""
from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x4empty-w28-2026-08-18")
sys.path.insert(0, BASE)
import w28_core as K                                              # noqa: E402

N = 8
V = tuple(range(N))
E = list(combinations(V, 2))
EI = {e: i for i, e in enumerate(E)}
RES = {}
RAN = []
OUT = None


def control(n):
    if n not in RAN:
        RAN.append(n)


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


# ----------------------------------------------------------------- builder

def partitions_for(z, c, kmax):
    """[(S_c, S_d, S_e)] on V - z with |S_c| odd; d, e the other colours."""
    VP = tuple(x for x in V if x != z)
    d, e = [x for x in range(3) if x != c]
    out = []
    for s in range(1, len(VP) + 1, 2):
        for S0 in combinations(VP, s):
            T = [x for x in VP if x not in S0]
            for m in range(0, len(T) + 1, 2):
                for S1 in combinations(T, m):
                    S2 = tuple(x for x in T if x not in S1)
                    w = [0] * N
                    w[z] = c
                    for y in S0:
                        w[y] = c
                    for y in S1:
                        w[y] = d
                    for y in S2:
                        w[y] = e
                    if K.offcount(tuple(w)) > kmax:
                        continue
                    out.append((S0, S1, S2, len(set(w)) == 1))
    return out


PARTS = {}


def star_solve(ts, z, c, kmax, zero, one):
    """Exact 7-unknown solve of the colour-c star at z.  Returns the new
    weights or None."""
    key = (z, c, kmax)
    if key not in PARTS:
        PARTS[key] = partitions_for(z, c, kmax)
    d, e = [x for x in range(3) if x != c]
    VP = [x for x in V if x != z]
    idx = {y: i for i, y in enumerate(VP)}
    rows, rhs = [], []
    for (S0, S1, S2, isc) in PARTS[key]:
        P = K.haf_w(ts[d], S1, zero, one) * K.haf_w(ts[e], S2, zero, one)
        if P == 0:
            continue
        row = [zero] * 7
        for y in S0:
            row[idx[y]] = P * K.haf_w(ts[c], [x for x in S0 if x != y],
                                      zero, one)
        if not any(x != 0 for x in row) and not isc:
            continue
        rows.append(row)
        rhs.append(one if isc else zero)
    part, kern = K.rref_solve(rows, rhs, 7)
    if part is None:
        return None
    out = [dict(x) for x in ts]
    for y in VP:
        v = part[idx[y]]
        ek = K.ekey(z, y)
        if v == 0:
            out[c].pop(ek, None)
        else:
            out[c][ek] = v
    return out


def diag_in_Xk(ts, k):
    src = K.zero_source(N)
    for c in range(3):
        for ee, v in ts[c].items():
            src[ee][c][c] = v
    return K.in_Xk(src, N, k)


def walk(ts, k, steps, rng, zero, one, order=None):
    cur = ts
    for s in range(steps):
        z = rng.randrange(N) if order is None else order[s % len(order)][0]
        c = rng.randrange(3) if order is None else order[s % len(order)][1]
        nxt = star_solve(cur, z, c, k, zero, one)
        if nxt is None:
            return None, s
        cur = nxt
    return cur, steps


def one_factorisation():
    """The standard 1-factorisation of K_8 into 7 perfect matchings."""
    out = []
    for r in range(7):
        M = [K.ekey(7, r)]
        for i in range(1, 4):
            M.append(K.ekey((r + i) % 7, (r - i) % 7))
        out.append([K.ekey(*x) for x in M])
    return out


def stage_build(budget):
    rng = random.Random(2808)
    print("=" * 74)
    print("(1) THE ADVERSARIAL BUILDER: exact diagonal site-linear walk")
    print("=" * 74)
    zero, one = Fraction(0), Fraction(1)
    order = [(z, c) for z in range(N) for c in range(3)]
    out = {}
    for k in (2, 3, 4):
        succ = 0
        tried = 0
        examples = []
        t0 = time.time()
        for t in range(budget):
            ts = [{}, {}, {}]
            style = t % 4
            if style == 0:                       # three disjoint PMs + noise
                pms = K.delta3_pms(N)
                for c in range(3):
                    for ee in pms[c]:
                        ts[c][ee] = Fraction(rng.choice([1, -1, 2]))
                for c in range(3):
                    for _ in range(rng.randint(0, 3)):
                        ts[c][rng.choice(E)] = Fraction(rng.randint(-2, 2))
            elif style == 1:                     # random sparse
                for c in range(3):
                    for ee in rng.sample(E, rng.randint(4, 9)):
                        ts[c][ee] = Fraction(rng.randint(-3, 3))
            elif style == 2:                     # random dense
                for c in range(3):
                    for ee in E:
                        if rng.random() < 0.35:
                            ts[c][ee] = Fraction(rng.randint(-2, 2))
            else:            # CANCELLATION-TARGETED: each class is a union of
                             # two disjoint PMs from a 1-factorisation of K_8,
                             # so npm(L_c) >= 2 and genuine cancellation is
                             # available on every vanishing hafnian
                F = one_factorisation()
                rng.shuffle(F)
                for c in range(3):
                    for ee in F[2 * c] + F[2 * c + 1]:
                        ts[c][ee] = Fraction(rng.choice([1, -1, 2, -2, 3]))
            ts = [{kk: vv for kk, vv in x.items() if vv != 0} for x in ts]
            tried += 1
            res, st = walk(ts, k, 24, rng, zero, one, order)
            if res is None:
                continue
            ok, bad = diag_in_Xk(res, k)
            if ok:
                succ += 1
                if len(examples) < 3:
                    examples.append({str(c): {str(kk): str(vv)
                                              for kk, vv in res[c].items()}
                                     for c in range(3)})
                if k == 4:
                    ok5, _ = diag_in_Xk(res, 5)
                    print(f"      *** DIAGONAL X_4 POINT AT N=8 FOUND: "
                          f"{res}; also X_5 {ok5}", flush=True)
        print(f"   k={k}: {tried} starts, {succ} landed in the diagonal X_{k} "
              f"({round(time.time()-t0,1)}s)")
        out[str(k)] = {"tried": tried, "success": succ,
                       "examples": examples[:2]}
        RES["builder"] = out
        ck(f"build{k}")
    assert out["2"]["success"] > 0 or out["3"]["success"] > 0, \
        "builder never succeeds -- worthless (ledger 20)"
    control("T2b1_builder_Q")

    print("   ... repeating over Q(omega) (ledger 19)")
    zero, one = K.Cyc(0, 0), K.Cyc(1, 0)
    outo = {}
    for k in (3, 4):
        succ = tried = 0
        for t in range(max(20, budget // 4)):
            ts = [{}, {}, {}]
            pms = K.delta3_pms(N)
            for c in range(3):
                for ee in pms[c]:
                    ts[c][ee] = K.Cyc(rng.randint(-2, 2), rng.randint(-2, 2))
                for _ in range(rng.randint(0, 4)):
                    ts[c][rng.choice(E)] = K.Cyc(rng.randint(-2, 2),
                                                 rng.randint(-2, 2))
            ts = [{kk: vv for kk, vv in x.items() if vv} for x in ts]
            tried += 1
            res, st = walk(ts, k, 18, rng, zero, one, order)
            if res is None:
                continue
            ok, bad = diag_in_Xk(res, k)
            succ += ok
            if ok and k == 4:
                print(f"      *** DIAGONAL X_4 POINT OVER Q(omega): {res}",
                      flush=True)
        print(f"   Q(omega) k={k}: {tried} starts, {succ} landed")
        outo[str(k)] = {"tried": tried, "success": succ}
        RES["builder_omega"] = outo
        ck(f"buildom{k}")
    control("T2b1b_builder_omega")


# --------------------------------------------------------------- enumeration

def masks_of(L):
    return [E[i] for i in range(28) if L >> i & 1]


def build_npm_tables():
    """npm over every vertex subset of even size, as a function of the edge
    mask -- computed on demand with memoisation."""
    subs = {}
    for m in (4, 6, 8):
        for S in combinations(V, m):
            subs[S] = [tuple(sorted(tuple(sorted(x)) for x in M))
                       for M in K.all_pms(S)]
    pmmask = {}
    for S, Ms in subs.items():
        arr = []
        for M in Ms:
            mm = 0
            for ee in M:
                mm |= 1 << EI[ee]
            arr.append(mm)
        pmmask[S] = arr
    return pmmask


PMMASK = None


def npm_mask(L, S):
    n = 0
    for mm in PMMASK[S]:
        if mm & L == mm:
            n += 1
    return n


def stage_enum(budget):
    global PMMASK
    print("=" * 74)
    print("(2) SKELETON ENUMERATION with the cancellation filter")
    print("=" * 74)
    PMMASK = build_npm_tables()
    FULLV = tuple(V)
    allpm = PMMASK[FULLV]
    print(f"   {len(allpm)} perfect matchings of K_8")
    # candidate classes: a PM plus up to `extra` further edges
    stats = {}
    for extra in (0, 1, 2):
        cands = set()
        for mm in allpm:
            rest = [i for i in range(28) if not (mm >> i & 1)]
            if extra == 0:
                cands.add(mm)
            elif extra == 1:
                for i in rest:
                    cands.add(mm | (1 << i))
            else:
                for i, j in combinations(rest, 2):
                    cands.add(mm | (1 << i) | (1 << j))
        cands = sorted(cands)
        print(f"   |L| = {4+extra}: {len(cands)} candidate classes "
              f"(a PM plus {extra} edges)", flush=True)
        stats[str(4 + extra)] = len(cands)
        RES["candidate_counts"] = stats
        ck(f"cand{extra}")
    # the full search: L_0 from the smallest family, L_1, L_2 disjoint
    fams = {}
    for extra in (0, 1, 2):
        f = set()
        for mm in allpm:
            rest = [i for i in range(28) if not (mm >> i & 1)]
            if extra == 0:
                f.add(mm)
            elif extra == 1:
                for i in rest:
                    f.add(mm | (1 << i))
            else:
                for i, j in combinations(rest, 2):
                    f.add(mm | (1 << i) | (1 << j))
        fams[extra] = sorted(f)

    def filterB(Lc, Ld):
        for ee in masks_of(Ld):
            S = tuple(x for x in V if x not in ee)
            if npm_mask(Lc, S) == 1:
                return False
        return True

    def filterCD(L):
        for S in combinations(V, 4):
            Sc = tuple(x for x in V if x not in S)
            for c, d in combinations(range(3), 2):
                if npm_mask(L[c], S) == 1 and npm_mask(L[d], Sc) == 1:
                    return False
                if npm_mask(L[d], S) == 1 and npm_mask(L[c], Sc) == 1:
                    return False
            for c in range(3):
                d, e2 = [x for x in range(3) if x != c]
                if npm_mask(L[c], S) != 1:
                    continue
                for f in ((Sc[0], Sc[1]), (Sc[0], Sc[2]), (Sc[0], Sc[3])):
                    g = tuple(x for x in Sc if x not in f)
                    fi, gi = 1 << EI[f], 1 << EI[K.ekey(*g)]
                    if ((L[d] & fi) and (L[e2] & gi)) or \
                       ((L[e2] & fi) and (L[d] & gi)):
                        return False
        return True

    t0 = time.time()
    for prof in ((0, 0, 1), (0, 1, 1), (0, 0, 2), (1, 1, 1), (0, 1, 2)):
        n = 0
        surv = []
        A, B, C = (fams[prof[0]], fams[prof[1]], fams[prof[2]])
        for L0 in A:
            for L1 in B:
                if L0 & L1:
                    continue
                if not (filterB(L0, L1) and filterB(L1, L0)):
                    continue
                for L2 in C:
                    if L2 & (L0 | L1):
                        continue
                    n += 1
                    if not (filterB(L0, L2) and filterB(L2, L0)
                            and filterB(L1, L2) and filterB(L2, L1)):
                        continue
                    if not filterCD((L0, L1, L2)):
                        continue
                    surv.append((L0, L1, L2))
            if time.time() - t0 > budget:
                print(f"      ... budget reached in profile {prof}",
                      flush=True)
                break
        print(f"   sizes {tuple(4+p for p in prof)}: {n} disjoint triples "
              f"scanned, {len(surv)} pass the cancellation filter "
              f"({round(time.time()-t0,1)}s)", flush=True)
        RES.setdefault("enumeration", {})[str(prof)] = {
            "scanned": n, "survivors": len(surv),
            "examples": [[sorted(masks_of(x)) for x in s] for s in surv[:5]]}
        ck(f"enum{prof}")
    control("T2b2_enumeration")


def main():
    global OUT
    t0 = time.time()
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    budget = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    OUT = f"{BASE}/results_t2b_cancel_{stage}.json"
    if stage in ("all", "build"):
        stage_build(budget)
    if stage in ("all", "enum"):
        stage_enum(budget * 20)
    RES["seconds"] = round(time.time() - t0, 1)
    RES["manifest"] = {"ran": RAN}
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()
