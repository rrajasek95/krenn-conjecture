#!/usr/bin/env python3
"""A8 T5 -- the informativeness of the sigma slice, and EXPLICIT POINTS.

  (a) reproduce the 4^7 = 16,384 sigma-symmetric unit-weight pattern grid on a
      500-pattern sample with my own engine; compare the X_3 rate against
      W28's 2,124/16,384 = 12.96%;
  (b) for a pattern that reaches X_3 with all three colours, SOLVE the three
      site systems, build the full K_8 source and verify X_3 membership BY THE
      RAW WORD DEFINITION -- an explicit point (ledger 18) that also validates
      W27-R1 and proves the k=3 free-set ideal is NOT the unit ideal;
  (c) check that the same point is NOT in X_4 (it lies outside the asserted
      locus, which is what ledger 18 demands of a forcing-verdict control);
  (d) the soundness catch: exhibit the transport colour-0 <-> colour-1 under
      sigma and show the free sets are NOT sigma-invariant per colour.
"""
import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, product

BASE = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a8-2026-08-19"
sys.path.insert(0, BASE)
from a8_core import H_raw, checkpoint, is_constant, offcount, perfect_matchings, require, words
import a8_sym as S

R = {}
RAN = []
rng = random.Random(505)
VP, Z, EP = S.VP, S.Z, S.EP
PMS8 = perfect_matchings(range(8))


def sect(s):
    print("=" * 74)
    print(s)
    print("=" * 74)


# ---------------------------------------------------- edge orbits and blocks
EORB = []
seen = set()
for e in EP:
    if e in seen:
        continue
    o, ee = [], e
    for _ in range(3):
        o.append(ee)
        ee = tuple(sorted((S.SIGMA[ee[0]], S.SIGMA[ee[1]])))
    o = sorted(set(o))
    seen |= set(o)
    EORB.append(sorted(o))
print(f"sigma edge-orbits: {len(EORB)} (7 expected), sizes {[len(o) for o in EORB]}")
require(len(EORB) == 7, "7 edge orbits")
REPS = [o[0] for o in EORB]


def t_from_pattern(pat, wts=None):
    """pat[i] in {0,1,2,3}: block i is zero, or the diagonal unit in colour
    pat[i]-1 on the representative edge.  Propagated by (sigma, rho)."""
    vals = [Fraction(0)] * S.NPAR
    for i, p in enumerate(pat):
        if p:
            w = Fraction(1) if wts is None else wts[i]
            vals[S.ORBIDX[(p - 1, REPS[i])]] = w
    t = [{}, {}, {}]
    for c in range(3):
        for e in EP:
            t[c][e] = vals[S.ORBIDX[(c, e)]]
    return t, vals


def haf_num(tc, Sset):
    out = Fraction(0)
    for m in S.pms(tuple(sorted(Sset))):
        p = Fraction(1)
        for e in m:
            p *= tc[tuple(sorted(e))]
        out += p
    return out


ALLSUB = [tuple(x for x in VP if (msk >> x) & 1) for msk in range(128)]


def haf_table(t):
    """H[c][mask] = haf(t^c | that vertex subset), all 3*128 values."""
    return [[haf_num(t[c], Ssub) for Ssub in ALLSUB] for c in range(3)]


def C_y_tab(HT, masks, y):
    """masks = (m0,m1,m2) the colour classes of u inside V'."""
    out = Fraction(1)
    for c in range(3):
        m = masks[c] & ~(1 << y)
        out *= HT[c][m]
        if out == 0:
            return Fraction(0)
    return out


COLS = [(y, d) for y in VP for d in range(3)]
CIDX = {x: i for i, x in enumerate(COLS)}
WORDS7 = list(product(range(3), repeat=7))


def rows_all(t, c):
    """FULL 21-unknown colour-c system at k=4 (no DEC shortcut), each row
    tagged with the off-count of its 8-word so smaller rungs are sub-lists."""
    HT = haf_table(t)
    out = []
    for u in WORDS7:
        w = u + (c,)
        oc = offcount(w)
        if oc > 4:
            continue
        masks = [0, 0, 0]
        for i, d in enumerate(u):
            masks[d] |= 1 << i
        row = [Fraction(0)] * 21
        for y in VP:
            v = C_y_tab(HT, masks, y)
            if v:
                row[CIDX[(y, u[y])]] += v
        out.append((oc, row, Fraction(1) if is_constant(w) else Fraction(0)))
    return out


def rows_for_colour(t, c, k, cache={}):
    key = (id(t), c)
    if key not in cache:
        cache.clear()
        cache[key] = rows_all(t, c)
    sel = [(r, bb) for (oc, r, bb) in cache[key] if oc <= k]
    return [r for r, _ in sel], [bb for _, bb in sel], COLS


def solve_exact(M, b):
    """Gaussian elimination; returns (consistent, solution or None)."""
    n = len(M[0])
    A = [row[:] + [bb] for row, bb in zip(M, b)]
    piv = []
    r = 0
    for col in range(n):
        p = next((i for i in range(r, len(A)) if A[i][col] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        pv = A[r][col]
        A[r] = [x / pv for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][col] != 0:
                f = A[i][col]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv.append(col)
        r += 1
    for row in A:
        if all(x == 0 for x in row[:-1]) and row[-1] != 0:
            return False, None
    sol = [Fraction(0)] * n
    for i, col in enumerate(piv):
        sol[col] = A[i][-1]
    return True, sol


sect("(a) 500 of the 16,384 sigma unit-weight patterns, my own engine")
allpats = list(product(range(4), repeat=7))
require(len(allpats) == 16384, "4^7")
sample = rng.sample(allpats, 500)
t0 = time.time()
cnt = {}
x3_all3 = []
for pat in sample:
    t, _ = t_from_pattern(pat)
    prof = []
    for k in (1, 2, 3, 4):
        nfeas = 0
        for c in range(3):
            M, b, _ = rows_for_colour(t, c, k)
            ok, _ = solve_exact(M, b)
            nfeas += ok
        prof.append(nfeas)
    cnt[str(prof)] = cnt.get(str(prof), 0) + 1
    if prof[2] == 3:
        x3_all3.append(pat)
    if prof[3] > 0:
        print(f"   *** k=4 FEASIBLE pattern {pat}")
print(f"   profiles over 500 patterns: {cnt}  ({time.time()-t0:.0f}s)")
print(f"   patterns reaching X_3 with all three colours: {len(x3_all3)} "
      f"({100*len(x3_all3)/500:.2f}%)   W28: 2124/16384 = 12.96%")
print(f"   patterns with ANY colour feasible at k=4: 0 expected")
R["t5_a"] = dict(sampled=500, profiles=cnt, x3_all3=len(x3_all3),
                 rate=len(x3_all3) / 500, w28_rate=2124 / 16384)
RAN.append("T5a_pattern_sweep")

sect("(b) explicit point: solve the three systems and check X_3 RAW at N=8")
require(x3_all3, "no X_3 pattern in the sample")
pat = x3_all3[0]
t, vals = t_from_pattern(pat)
A = {}
for e in EP:
    A[e] = [[Fraction(0)] * 3 for _ in range(3)]
    for c in range(3):
        A[e][c][c] = t[c][e]
star = {y: [[Fraction(0)] * 3 for _ in range(3)] for y in VP}
for c in range(3):
    M, b, cols = rows_for_colour(t, c, 3)
    ok, sol = solve_exact(M, b)
    require(ok, f"colour {c} inconsistent")
    for i, (y, d) in enumerate(cols):
        star[y][d][c] = sol[i]
for y in VP:
    A[(y, Z)] = star[y]
badw = None
for w in words(8):
    if offcount(w) > 3:
        continue
    val = H_raw(A, w, PMS8)
    tgt = 1 if is_constant(w) else 0
    if val != tgt:
        badw = (w, str(val), tgt)
        break
print(f"   pattern {pat}: RAW X_3 membership at N=8 -> {'IN X_3' if badw is None else badw}")
require(badw is None, f"raw X_3 check failed: {badw}")
bad4 = None
for w in words(8):
    if offcount(w) > 4:
        continue
    val = H_raw(A, w, PMS8)
    tgt = 1 if is_constant(w) else 0
    if val != tgt:
        bad4 = (w, str(val), tgt, offcount(w))
        break
print(f"   the SAME point at k=4: {'IN X_4 (!!)' if bad4 is None else 'not in X_4, first failure ' + str(bad4)}")
R["t5_b"] = dict(pattern=list(pat), in_X3_raw=True, in_X4=bad4 is None,
                 first_X4_failure=str(bad4))
RAN.append("T5b_explicit_X3_point")
require(bad4 is not None, "an X_4 point in the sigma slice would REFUTE W28-T1")

sect("(c) free sets of that point, per colour, and the sigma transport")


def free_set(t, c):
    """{y : every even split (S1,S2) of V'-y has haf(t^d|S1)haf(t^e|S2) = 0},
    where (d,e) are the two colours != c in the order (c+1, c+2)."""
    d, e = (c + 1) % 3, (c + 2) % 3
    F = []
    for y in VP:
        W = tuple(x for x in VP if x != y)
        if all(haf_num(t[d], S1) * haf_num(t[e], S2) == 0
               for (S1, S2) in S.even_splits(W)):
            F.append(y)
    return F


Fc = {c: free_set(t, c) for c in range(3)}
sig = S.SIGMA
print(f"   free sets: colour 0 {Fc[0]}, colour 1 {Fc[1]}, colour 2 {Fc[2]}")
print(f"   sigma(F_0) = {sorted(sig[y] for y in Fc[0])}   (must equal F_1 -- the transport)")
print(f"   F_0 sigma-invariant? {sorted(sig[y] for y in Fc[0]) == sorted(Fc[0])}")
R["t5_c"] = dict(free_sets={str(c): Fc[c] for c in range(3)},
                 sigmaF0=sorted(sig[y] for y in Fc[0]),
                 transport_ok=sorted(sig[y] for y in Fc[0]) == sorted(Fc[1]),
                 F0_sigma_invariant=sorted(sig[y] for y in Fc[0]) == sorted(Fc[0]))
RAN.append("T5c_transport")

# scan the whole X_3 sample for a case where sigma(F_0) != F_0 (unsoundness)
witness = None
for p2 in x3_all3:
    tt, _ = t_from_pattern(p2)
    F0 = free_set(tt, 0)
    F1 = free_set(tt, 1)
    if sorted(sig[y] for y in F0) != sorted(F0):
        witness = (p2, F0, F1, sorted(sig[y] for y in F0))
        break
print(f"   WITNESS that per-colour free sets are not sigma-invariant: {witness}")
R["t5_c_witness"] = str(witness)
RAN.append("T5c_unsoundness_witness")

MAN = dict(declared=["T5a_pattern_sweep", "T5b_explicit_X3_point", "T5c_transport",
                     "T5c_unsoundness_witness"], ran=RAN)
MAN["missing"] = [x for x in MAN["declared"] if x not in RAN]
print("CONTROL MANIFEST:", MAN)
require(not MAN["missing"], "manifest")
R["manifest"] = MAN
R["explicit_point"] = dict(pattern=list(pat), orbit_values=[str(v) for v in vals],
                           star={str(y): [[str(x) for x in row] for row in star[y]] for y in VP})
checkpoint(BASE + "/results_t5_sweep.json", R)
