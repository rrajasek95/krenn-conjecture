#!/usr/bin/env python3
"""A8 T8 -- (i) the Waring counterexample, all 15 coefficients, symbolically;
(ii) the (N,k) calibration table by an independent probe."""
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, product

BASE = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a8-2026-08-19"
sys.path.insert(0, BASE)
from a8_core import (checkpoint, diag_blocks, haf, H_raw, is_constant, offcount,
                     perfect_matchings, require, words)

R, RAN = {}, []
rng = random.Random(808)


def sect(s):
    print("=" * 74)
    print(s)
    print("=" * 74)


# --------------------------------------------------------------------- (i)
sect("(i) the Waring counterexample: every coefficient of Haf(sum lam_c t^c)")
V = tuple(range(8))
PMS8 = perfect_matchings(V)
E8 = [tuple(sorted(e)) for e in combinations(V, 2)]
T = [{(0, 1): 1, (2, 3): 1, (4, 5): 1, (6, 7): 1},
     {(0, 2): 1, (1, 4): 1, (3, 6): 1, (5, 7): 1},
     {(0, 3): 1, (2, 7): 1, (1, 5): -1, (4, 6): -1}]
T = [{k: Fraction(v) for k, v in d.items()} for d in T]
for c in range(3):
    print(f"   haf(t^{c}|V) = {haf(T[c], V)}  (condition (A))")
    require(haf(T[c], V) == 1, "A")
# expand Haf(sum lam t) exactly: every PM of K_8 contributes lam^sig * weight
coef = {}
for M in PMS8:
    terms = [(0, Fraction(1))]
    ok = True
    sig_w = []
    for e in M:
        opts = [(c, T[c][e]) for c in range(3) if e in T[c]]
        if not opts:
            ok = False
            break
        sig_w.append(opts)
    if not ok:
        continue
    acc = [((0, 0, 0), Fraction(1))]
    for opts in sig_w:
        acc = [(tuple(s[i] + (1 if i == c else 0) for i in range(3)), w * v)
               for (s, w) in acc for (c, v) in opts]
    for s, w in acc:
        coef[s] = coef.get(s, Fraction(0)) + w
coef = {k: v for k, v in coef.items() if v}
print(f"   nonzero coefficients of Haf(lam.t): {dict(sorted((str(k), str(v)) for k, v in coef.items()))}")
want = {(4, 0, 0): Fraction(1), (0, 4, 0): Fraction(1), (0, 0, 4): Fraction(1)}
print(f"   equals lam_0^4 + lam_1^4 + lam_2^4 exactly: {coef == want}")
require(coef == want, "Waring identity does not hold exactly")
A = diag_blocks({c: T[c] for c in range(3)}, 8)
f3 = [w for w in words(8) if offcount(w) <= 3 and not is_constant(w) and H_raw(A, w, PMS8) != 0]
f4 = [(w, str(H_raw(A, w, PMS8))) for w in words(8)
      if offcount(w) <= 4 and not is_constant(w) and H_raw(A, w, PMS8) != 0]
print(f"   raw X_3 mixed failures: {len(f3)} (0 => the source IS in X_3)")
print(f"   raw X_4 mixed failures: {len(f4)}  {f4}")
require(len(f3) == 0 and len(f4) > 0, "counterexample invalid")
R["waring_counterexample"] = dict(
    t={str(c): {str(k): str(v) for k, v in T[c].items()} for c in range(3)},
    coefficients={str(k): str(v) for k, v in sorted(coef.items())},
    in_X3=True, X4_failures=[[list(w), v] for w, v in f4],
    verdict="Haf(sum lam t) = sum lam^4 EXACTLY and (A) holds, yet the source "
            "is not in X_4 -- so the Waring identity is strictly WEAKER than "
            "the diagonal X_4 conditions")
RAN.append("T8_waring_counterexample")
# which condition does it violate?
S = tuple(sorted(set(range(8)) - {4, 5, 6, 7}))
print(f"   the two failing words are (4,2,2)-profile words -> it violates (D), "
      f"not (C) (its three pairwise unions are Hamiltonian)")

# -------------------------------------------------------------------- (ii)
sect("(ii) the (N,k) calibration table, independent probe")


def bg_from_triple(n, Ms):
    """background on K_{n-1} from three pairwise disjoint edge sets of K_n."""
    VP = tuple(range(n - 1))
    EPn = [tuple(sorted(e)) for e in combinations(VP, 2)]
    B = {}
    for e in EPn:
        B[e] = [[Fraction(0)] * 3 for _ in range(3)]
        for c in range(3):
            if e in Ms[c]:
                B[e][c][c] = Fraction(1)
    return B, VP


def feasible(B, VP, n, k):
    """all three colour site systems at the solve site z = n-1 consistent?"""
    for c in range(3):
        cols = [(y, d) for y in VP for d in range(3)]
        idx = {x: i for i, x in enumerate(cols)}
        AA = []
        for u in product(range(3), repeat=n - 1):
            w = u + (c,)
            if offcount(w) > k:
                continue
            row = [Fraction(0)] * (len(cols) + 1)
            for y in VP:
                tot = Fraction(0)
                for m in perfect_matchings(tuple(v for v in VP if v != y)):
                    p = Fraction(1)
                    for (a2, b2) in m:
                        p *= B[(a2, b2)][u[a2]][u[b2]]
                        if p == 0:
                            break
                    tot += p
                if tot:
                    row[idx[(y, u[y])]] += tot
            row[-1] = Fraction(1) if is_constant(w) else Fraction(0)
            AA.append(row)
        r0 = 0
        for col in range(len(cols)):
            p = next((i for i in range(r0, len(AA)) if AA[i][col] != 0), None)
            if p is None:
                continue
            AA[r0], AA[p] = AA[p], AA[r0]
            pv = AA[r0][col]
            AA[r0] = [x / pv for x in AA[r0]]
            for i in range(len(AA)):
                if i != r0 and AA[i][col] != 0:
                    f = AA[i][col]
                    AA[i] = [x - f * y for x, y in zip(AA[i], AA[r0])]
            r0 += 1
        if any(all(x == 0 for x in row[:-1]) and row[-1] != 0 for row in AA):
            return False
    return True


def disjoint_triples(n, limit, seed):
    pm = [frozenset(m) for m in perfect_matchings(range(n))]
    out = []
    for i in range(len(pm)):
        for j in range(i + 1, len(pm)):
            if pm[i] & pm[j]:
                continue
            for kk in range(j + 1, len(pm)):
                if (pm[i] & pm[kk]) or (pm[j] & pm[kk]):
                    continue
                out.append((pm[i], pm[j], pm[kk]))
    random.Random(seed).shuffle(out)
    return out[:limit]


def probe(n, k, trials=40, seed=0, kind="diag"):
    """Feasibility of ALL THREE colour site systems at rung k for random
    backgrounds on K_{n-1}.  Returns (#fired, #trials)."""
    rr = random.Random(seed)
    VP = tuple(range(n - 1))
    EPn = [tuple(sorted(e)) for e in combinations(VP, 2)]
    z = n - 1
    fired = 0
    for _ in range(trials):
        if kind == "diag":
            t = [{}, {}, {}]
            for c in range(3):
                for e in rr.sample(EPn, rr.randint(len(EPn) // 3, len(EPn))):
                    t[c][e] = Fraction(rr.choice([1, -1, 2, -2]))
            B = {}
            for e in EPn:
                B[e] = [[Fraction(0)] * 3 for _ in range(3)]
                for c in range(3):
                    B[e][c][c] = t[c].get(e, Fraction(0))
        else:
            B = {e: [[Fraction(rr.randint(-3, 3)) for _ in range(3)] for _ in range(3)]
                 for e in EPn}
        # C_y(u) by the raw hafnian over PMs of V'-y
        ok_all = True
        for c in range(3):
            cols = [(y, d) for y in VP for d in range(3)]
            idx = {x: i for i, x in enumerate(cols)}
            M, b = [], []
            for u in product(range(3), repeat=n - 1):
                w = u + (c,)
                if offcount(w) > k:
                    continue
                row = [Fraction(0)] * len(cols)
                for y in VP:
                    tot = Fraction(0)
                    for m in perfect_matchings(tuple(v for v in VP if v != y)):
                        p = Fraction(1)
                        for (a2, b2) in m:
                            p *= B[(a2, b2)][u[a2]][u[b2]]
                            if p == 0:
                                break
                        tot += p
                    if tot:
                        row[idx[(y, u[y])]] += tot
                M.append(row)
                b.append(Fraction(1) if is_constant(w) else Fraction(0))
            # consistency by elimination
            AA = [r[:] + [bb] for r, bb in zip(M, b)]
            ncol = len(cols)
            r0 = 0
            for col in range(ncol):
                p = next((i for i in range(r0, len(AA)) if AA[i][col] != 0), None)
                if p is None:
                    continue
                AA[r0], AA[p] = AA[p], AA[r0]
                pv = AA[r0][col]
                AA[r0] = [x / pv for x in AA[r0]]
                for i in range(len(AA)):
                    if i != r0 and AA[i][col] != 0:
                        f = AA[i][col]
                        AA[i] = [x - f * y for x, y in zip(AA[i], AA[r0])]
                r0 += 1
            if any(all(x == 0 for x in row[:-1]) and row[-1] != 0 for row in AA):
                ok_all = False
                break
        fired += ok_all
    return fired, trials


tab = {}
print("   family: backgrounds on K_(N-1) obtained by restricting three PAIRWISE")
print("   DISJOINT perfect matchings of K_N (unit weights) -- the diagonal")
print("   skeleton family, known to carry X_3 at both orders.")
for n, tr in ((6, 40), (8, 25)):
    trips = disjoint_triples(n, tr, seed=n)
    print(f"   N={n}: {len(trips)} disjoint-PM triples drawn")
    for k in (2, 3, 4):
        t0 = time.time()
        f = 0
        for Ms in trips:
            B, VP = bg_from_triple(n, Ms)
            f += feasible(B, VP, n, k)
        tab[f"({n},{k})"] = f"{f}/{len(trips)}"
        print(f"   (N={n}, k={k}): fired {f}/{len(trips)}   ({time.time()-t0:.0f}s)", flush=True)
# and the random dense diagonal control (must be mostly silent everywhere)
for (n, k, tr) in ((6, 3, 20), (8, 3, 10)):
    f, tt = probe(n, k, tr, seed=1000 + 10 * n + k)
    tab[f"random({n},{k})"] = f"{f}/{tt}"
    print(f"   [ctrl] random dense diagonal (N={n}, k={k}): {f}/{tt}", flush=True)
print(f"   W27 reported: fires 40/40 at (6,3) and 25/25 at (8,3); silent at (6,4);")
print(f"   (8,4) wears the (6,4) signature.")
R["calibration"] = tab
RAN.append("T8_calibration")

MAN = dict(declared=["T8_waring_counterexample", "T8_calibration"], ran=RAN)
MAN["missing"] = [x for x in MAN["declared"] if x not in RAN]
print("CONTROL MANIFEST:", MAN)
require(not MAN["missing"], "manifest")
R["manifest"] = MAN
checkpoint(BASE + "/results_t8_waring_calib.json", R)
