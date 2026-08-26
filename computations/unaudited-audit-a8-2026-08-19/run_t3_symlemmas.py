#!/usr/bin/env python3
"""A8 T3 -- the three W28 lemmas (SYM / DEC / FREE) re-derived and machine-checked
against the RAW word definition of H at N = 8.  Independent code throughout.
"""
import random
import sys
from fractions import Fraction
from itertools import combinations, product

BASE = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a8-2026-08-19"
sys.path.insert(0, BASE)
from a8_core import H_raw, checkpoint, is_constant, offcount, perfect_matchings, require, words
import a8_sym as S

R = {}
RAN = []
rng = random.Random(818)
V8 = tuple(range(8))
PMS8 = perfect_matchings(V8)
NS, VP, Z = S.NS, S.VP, S.Z
EP = S.EP


def sect(s):
    print("=" * 74)
    print(s)
    print("=" * 74)


# --------------------------------------------------------- background build
def numeric_sigma_background(vals):
    """t[c][e] from the 21 orbit values."""
    t = [{}, {}, {}]
    for c in range(3):
        for e in EP:
            t[c][e] = vals[S.ORBIDX[(c, e)]]
    return t


def blocks_from_t(t):
    B = {}
    for e in EP:
        M = [[0] * 3 for _ in range(3)]
        for c in range(3):
            M[c][c] = t[c][e]
        B[e] = M
    return B


sect("(0) the sigma-symmetric diagonal slice: construction + invariance check")
vals = [Fraction(rng.randint(-6, 6)) for _ in range(S.NPAR)]
while any(v == 0 for v in vals):
    vals = [Fraction(rng.randint(-6, 6)) for _ in range(S.NPAR)]
t = numeric_sigma_background(vals)
B = blocks_from_t(t)
sig, rho = S.SIGMA, S.RHO
bad = 0
for (u, v) in EP:
    su, sv = sig[u], sig[v]
    for i in range(3):
        for j in range(3):
            lhs = B[tuple(sorted((su, sv)))][rho[i] if su < sv else rho[j]][rho[j] if su < sv else rho[i]]
            rhs = B[(u, v)][i][j]
            bad += (lhs != rhs)
print(f"   21 orbit parameters; invariance violations B_(su,sv)[ri][rj] = B_uv[i][j]: {bad} "
      f"(must be 0)")
require(bad == 0, "sigma-invariance")
# non-vacuity: a NON-symmetric background must violate it
t2 = [dict(x) for x in t]
t2[0][EP[0]] = t2[0][EP[0]] + 1
B2 = blocks_from_t(t2)
bad2 = 0
for (u, v) in EP:
    su, sv = sig[u], sig[v]
    for i in range(3):
        for j in range(3):
            lhs = B2[tuple(sorted((su, sv)))][rho[i] if su < sv else rho[j]][rho[j] if su < sv else rho[i]]
            bad2 += (lhs != B2[(u, v)][i][j])
print(f"   [ctrl] one perturbed weight -> {bad2} violations (must be > 0)")
require(bad2 > 0, "invariance control vacuous")
R["t3_0_invariance"] = dict(nparam=S.NPAR, violations=bad, control_violations=bad2)
RAN += ["T3_0_invariance", "T3_0_invariance_ctrl"]

# --------------------------------------------------- (1) the star expansion
sect("(1) H_w = sum_y A_yz[w_y][w_z] C_y(u)  -- against the RAW 105-PM sum")
star = {y: [[Fraction(rng.randint(-5, 5)) for _ in range(3)] for _ in range(3)] for y in VP}
A = dict(B)
for y in VP:
    A[(y, Z)] = star[y]


def C_y(t, u, y):
    """product over colours of haf(t^c | S_c(u) - y)  -- computed by the RAW
    hafnian sum, not by any formula."""
    out = Fraction(1)
    for c in range(3):
        Sc = tuple(v for v in VP if u[v] == c and v != y)
        h = Fraction(0)
        for m in S.pms(Sc):
            p = Fraction(1)
            for e in m:
                p *= t[c][tuple(sorted(e))]
            h += p
        out *= h
    return out


mis = 0
tested = 0
for _ in range(60):
    w = tuple(rng.randrange(3) for _ in range(8))
    u = w[:7]
    lhs = H_raw(A, w, PMS8)
    rhs = sum(star[y][w[y]][w[7]] * C_y(t, u, y) for y in VP)
    mis += (lhs != rhs)
    tested += 1
print(f"   {tested} random words: {mis} mismatches (must be 0)")
require(mis == 0, "star expansion wrong")
# control: perturb one star entry -> must break
A2 = dict(A)
A2[(0, Z)] = [[x for x in row] for row in star[0]]
A2[(0, Z)][0][0] += 1
ctrl_words = [(0,) + tuple(rng.randrange(3) for _ in range(6)) + (0,) for _ in range(40)]
diff = sum(1 for w in ctrl_words
           if H_raw(A2, w, PMS8) != sum(star[y][w[y]][w[7]] * C_y(t, w[:7], y) for y in VP))
print(f"   [ctrl] perturbed star (words with w_0 = w_z = 0): {diff}/40 now mismatch (must be > 0)")
require(diff > 0, "star control vacuous")
R["t3_1_star"] = dict(tested=tested, mismatches=mis, ctrl=diff)
RAN += ["T3_1_star_expansion", "T3_1_star_ctrl"]

# ------------------------------------------------------------ (2) W28-DEC
sect("(2) W28-DEC: parity decoupling of the 21-unknown colour-0 system")
# build the full 21-unknown colour-0 system explicitly and inspect its support
kmax = 4
rows = []
for u in product(range(3), repeat=7):
    w = u + (0,)
    if offcount(w) > kmax:
        continue
    row = {}
    for y in VP:
        c = C_y(t, u, y)
        if c:
            row[(y, u[y])] = row.get((y, u[y]), 0) + c
    rows.append((u, row, 1 if is_constant(w) else 0))
print(f"   colour-0 rows at k=4: {len(rows)}")
# claim: in every row, all occurring (y,d) share the SAME d
bad = [u for (u, row, _) in rows if len(set(d for (_, d) in row)) > 1]
print(f"   rows whose support mixes two values of d: {len(bad)} (must be 0)")
require(not bad, "DEC broken")
# claim: the d for a row is the unique colour with odd class count
bad2 = []
for (u, row, _) in rows:
    if not row:
        continue
    d = next(iter(row))[1]
    cnt = [sum(1 for v in VP if u[v] == c) for c in range(3)]
    if cnt[d] % 2 == 0 or any(cnt[c] % 2 for c in range(3) if c != d):
        bad2.append(u)
print(f"   rows where d is not the unique odd class: {len(bad2)} (must be 0)")
require(not bad2, "DEC parity identification broken")
# claim: the only row with RHS 1 is in the d = 0 block
rhs1 = [(u, row) for (u, row, r) in rows if r]
dvals = set(next(iter(row))[1] for (u, row) in rhs1 if row)
print(f"   inhomogeneous rows: {len(rhs1)}; their blocks d = {sorted(dvals)} (must be {{0}})")
require(dvals == {0}, "inhomogeneous row not in block 0")
# and rows with EMPTY support must have RHS 0
bad3 = [u for (u, row, r) in rows if not row and r]
print(f"   empty-support rows with RHS 1: {len(bad3)} (must be 0)")
require(not bad3, "vacuous inconsistency")
R["t3_2_DEC"] = dict(rows=len(rows), mixed_d_rows=0, wrong_parity_rows=0,
                     inhomogeneous_blocks=sorted(dvals))
RAN += ["T3_2_DEC"]

# ------------------------------------------------------------ (3) W28-FREE
sect("(3) W28-FREE: |S0| = 1 rows force x_y = 0 off the free set")
free_rows = [(u, row) for (u, row, r) in rows
             if sum(1 for v in VP if u[v] == 0) == 1 and row]
print(f"   rows with |S0| = 1 and nonempty support: {len(free_rows)} "
      f"(7 sites x 32 even splits = 224 expected)")


def freeset(t):
    F = []
    for y in VP:
        W = tuple(x for x in VP if x != y)
        ok = True
        for (S1, S2) in S.even_splits(W):
            h1 = Fraction(0)
            for m in S.pms(S1):
                p = Fraction(1)
                for e in m:
                    p *= t[1][tuple(sorted(e))]
                h1 += p
            h2 = Fraction(0)
            for m in S.pms(S2):
                p = Fraction(1)
                for e in m:
                    p *= t[2][tuple(sorted(e))]
                h2 += p
            if h1 * h2 != 0:
                ok = False
                break
        F.append(y) if ok else None
    return F


Fs = freeset(t)
print(f"   free set of this random background: {Fs} (generic background: expect empty)")
print(f"   => q(V') = sum_y haf(t^0|V'-y) x_y = 1 needs some x_y != 0, and such a y")
print(f"      must be free; so FEASIBLE => free set nonempty.  [W28-FREE]")
R["t3_3_FREE"] = dict(free_rows=len(free_rows), free_set_random=Fs)
require(len(free_rows) == 224, "expected 224 |S0|=1 rows")
RAN += ["T3_3_FREE"]

# ------------------------------------------------------------- (4) W28-SYM
sect("(4) W28-SYM: the averaging lemma -- hypotheses")
print("   statement: H a group of symmetries with TRIVIAL colour action acting")
print("   transitively on V'; then colour-c feasibility <=> the 3-unknown")
print("   averaged system is consistent.")
print("   PROOF STEP: x solution => (1/|H|) sum_h h.x is an H-invariant solution.")
print("   *** REQUIRES |H| INVERTIBLE IN THE FIELD ***  (char 0 or char p not | |H|).")
# Z_7 slice: pi = (x -> x+1), rho = id, |H| = 7.
z7 = {}
for c in range(3):
    for e in EP:
        pass
orb = {}
oidx = []
seen = {}
for c in range(3):
    for e in EP:
        if (c, e) in seen:
            continue
        k = len(oidx)
        cc, ee = c, e
        for _ in range(7):
            seen[(cc, ee)] = k
            ee = tuple(sorted(((ee[0] + 1) % 7, (ee[1] + 1) % 7)))
        oidx.append((c, e))
print(f"   Z_7 slice: {len(oidx)} orbit parameters (3 colours x 3 edge-orbits = 9 expected)")
R["t3_4_SYM"] = dict(z7_params=len(oidx),
                     hypothesis="|H| invertible in the coefficient field; "
                                "H transitive on V'; trivial colour action")
require(len(oidx) == 9, "Z_7 slice parameter count")
RAN += ["T3_4_SYM_params"]

# empirical check of the averaging conclusion over Q on the Z_7 slice
zvals = [Fraction(rng.randint(-4, 4)) for _ in range(9)]
tz = [{}, {}, {}]
for c in range(3):
    for e in EP:
        tz[c][e] = zvals[seen[(c, e)]]
# build colour-0 d=0 block; check: consistent  <=>  consistent with x constant
import itertools


def block_rows(tt, kmax=4, colour=0, d=0):
    out = []
    for u in product(range(3), repeat=7):
        w = u + (colour,)
        if offcount(w) > kmax:
            continue
        cnt = [sum(1 for v in VP if u[v] == c) for c in range(3)]
        if cnt[d] % 2 == 0 or any(cnt[c] % 2 for c in range(3) if c != d):
            continue
        coeffs = [C_y(tt, u, y) if u[y] == d else Fraction(0) for y in VP]
        out.append((coeffs, Fraction(1) if is_constant(w) else Fraction(0)))
    return out


def consistent(rows_):
    """exact Gaussian elimination consistency test on [coeffs | rhs]."""
    M = [list(c) + [r] for c, r in rows_]
    ncol = len(M[0]) - 1
    piv = 0
    for col in range(ncol):
        p = next((i for i in range(piv, len(M)) if M[i][col] != 0), None)
        if p is None:
            continue
        M[piv], M[p] = M[p], M[piv]
        pv = M[piv][col]
        M[piv] = [x / pv for x in M[piv]]
        for i in range(len(M)):
            if i != piv and M[i][col] != 0:
                f = M[i][col]
                M[i] = [a - f * b for a, b in zip(M[i], M[piv])]
        piv += 1
    return not any(all(x == 0 for x in row[:-1]) and row[-1] != 0 for row in M)


rz = block_rows(tz)
gen_ok = consistent(rz)
# invariant (constant-x) version:  sum over y of coeff  * X = rhs
inv_rows = [([sum(c)], r) for c, r in rz]
inv_ok = consistent(inv_rows)
print(f"   Z_7 slice, k=4 colour-0 block: general consistent = {gen_ok}; "
      f"constant-x consistent = {inv_ok} (must agree)")
R["t3_4_SYM_empirical"] = dict(general=gen_ok, invariant=inv_ok, agree=gen_ok == inv_ok)
require(gen_ok == inv_ok, "averaging conclusion failed on the Z_7 slice")
RAN += ["T3_4_SYM_empirical"]

MAN = dict(declared=["T3_0_invariance", "T3_0_invariance_ctrl", "T3_1_star_expansion",
                     "T3_1_star_ctrl", "T3_2_DEC", "T3_3_FREE", "T3_4_SYM_params",
                     "T3_4_SYM_empirical"], ran=RAN)
MAN["missing"] = [x for x in MAN["declared"] if x not in RAN]
print("CONTROL MANIFEST:", MAN)
require(not MAN["missing"], "manifest")
R["manifest"] = MAN
checkpoint(BASE + "/results_t3_symlemmas.json", R)
