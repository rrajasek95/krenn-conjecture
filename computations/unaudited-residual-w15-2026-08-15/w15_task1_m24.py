#!/usr/bin/env python3
"""W15 TASK 1 -- the m = 24 residual (R) instance: structure + kill.

Exact arithmetic only (Fraction / exact sparse polynomials).  No floats.

WHAT THIS ESTABLISHES (all machine-checked here):

 S1  the 'clean' words of the m=24 template (no single-cell block active)
     have fibre = the SEVEN full-block matchings, and
        H_w = P_L(x)*P_R(y) + A07[x0][y7]*A14[x1][y4]*A23[x2][x3]*A56[y5][y6]
     with P_L, P_R the half-permanents of L={0,1,2,3}, R={4,5,6,7}.
 S2  the CONSTANT word 0^8 is *effectively clean*: its fibre is the same
     seven matchings (the one active single cell a1 = A04[0][0] lies in no
     supported matching), so H_{0^8} has the SAME binomial shape.
 S3  six particular clean mixed words w1..w6 give six binomial equations
     whose cross-multiplication forces the 2x2 minor
        M = A14[0][0]A14[2][1] - A14[0][1]A14[2][0] = 0
     and then forces H_{0^8} = 0.  Packaged as the EXPLICIT IDENTITY
        A07[1][0]^4 * A23[0][0]^3 * A56[2][0]^3 * A14[2][1]^2 * H_{0^8}
             = sum_i lambda_i * H_{w_i}          in Z[occupied cells]
     with explicit cofactors lambda_i, verified by exact expansion.
 S4  hence no exact source has this template.
"""

import json
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w15_core import (W8_IMMUNE, EDGES, EIDX, MATCHINGS, MATCH_EIDX, VarMap,
                      cell_of, is_clean, single_cell_activity,
                      supported_matchings, word_polynomial, padd, pmul, psub,
                      pneg, pvar, pzero, piszero, pconst, pscale)

HERE = os.path.dirname(os.path.abspath(__file__))
T = W8_IMMUNE[24]
vm = VarMap(T)
LOG = []


def say(s=""):
    print(s)
    LOG.append(s)


def V(u, v, i, j):
    """polynomial variable for cell (i,j) of block A_uv (u<v)."""
    return pvar(vm.var(EIDX[(u, v)], 3 * i + j))


def word(x, y):
    return tuple(x) + tuple(y)


# ------------------------------------------------------------------ S1/S2
say("=" * 72)
say("W15 TASK 1 -- m = 24 residual instance (12 full blocks + 12 single "
    "cells)")
say("=" * 72)
act = single_cell_activity(T)
_actstr = {("%d-%d" % EDGES[e]): [list(p) for p in v]
           for e, v in act.items()}
say("single cells (edge -> (vertex,colour) pairs required): %s" % (_actstr,))

FULL_EDGES = [EDGES[i] for i, t in enumerate(T) if t == 511]
say(f"Gamma (full blocks, {len(FULL_EDGES)}): {FULL_EDGES}")

L, R = (0, 1, 2, 3), (4, 5, 6, 7)
# the 7 full-block matchings
FULLM = [mi for mi, m in enumerate(MATCHINGS)
         if all(T[EIDX[e]] == 511 for e in m)]
say(f"matchings all of whose blocks are FULL: {len(FULLM)} -> "
    f"{[MATCHINGS[i] for i in FULLM]}")


def P_L(x):
    """half-permanent of the K4 on L (all six blocks full)."""
    return padd(padd(pmul(V(0, 1, x[0], x[1]), V(2, 3, x[2], x[3])),
                     pmul(V(0, 2, x[0], x[2]), V(1, 3, x[1], x[3]))),
                pmul(V(0, 3, x[0], x[3]), V(1, 2, x[1], x[2])))


def P_R(y):
    """half-permanent of R: blocks 46 and 57 are EMPTY, so two terms."""
    return padd(pmul(V(4, 5, y[0], y[1]), V(6, 7, y[2], y[3])),
                pmul(V(4, 7, y[0], y[3]), V(5, 6, y[1], y[2])))


def clean_shape(x, y):
    cross = pmul(pmul(V(0, 7, x[0], y[3]), V(1, 4, x[1], y[0])),
                 pmul(V(2, 3, x[2], x[3]), V(5, 6, y[1], y[2])))
    return padd(pmul(P_L(x), P_R(y)), cross)


# --- S1: verify the shape on EVERY clean word
n_clean, n_clean_mixed, bad = 0, 0, 0
from itertools import product as iproduct
for x in iproduct(range(3), repeat=4):
    for y in iproduct(range(3), repeat=4):
        w = word(x, y)
        if not is_clean(T, w, act):
            continue
        n_clean += 1
        if len(set(w)) > 1:
            n_clean_mixed += 1
        if not piszero(psub(word_polynomial(T, vm, w), clean_shape(x, y))):
            bad += 1
say(f"\nS1: clean words = {n_clean} (mixed {n_clean_mixed}); "
    f"H_w != P_L*P_R + A07 A14 A23 A56 on {bad} of them  [want 0]")
assert bad == 0

# --- S2: the constant word 0^8
w0 = (0,) * 8
sup0 = supported_matchings(T, w0)
say(f"S2: 0^8 is clean? {is_clean(T, w0, act)}   |fibre(0^8)| = {len(sup0)}")
say(f"    fibre(0^8) matchings = {[MATCHINGS[i] for i in sup0]}")
say(f"    fibre(0^8) == the 7 full-block matchings: {sorted(sup0) == sorted(FULLM)}")
assert sorted(sup0) == sorted(FULLM)
G = word_polynomial(T, vm, w0)
assert piszero(psub(G, clean_shape((0, 0, 0, 0), (0, 0, 0, 0))))
say("    => H_{0^8} = P_L(0000) P_R(0000) + A07[0][0]A14[0][0]A23[0][0]A56[0][0]")
say("    (the single cell A04[0][0] IS active on 0^8 but lies in no "
    "supported matching)")

# ------------------------------------------------------------------ S3
say("\nS3: the six-word certificate")
W1 = ((1, 0, 0, 0), (0, 2, 0, 0))
W2 = ((1, 0, 0, 0), (1, 2, 0, 0))
W3 = ((1, 2, 0, 0), (0, 2, 0, 0))
W4 = ((1, 2, 0, 0), (1, 2, 0, 0))
W5 = ((0, 0, 0, 0), (1, 2, 0, 0))
W6 = ((1, 2, 0, 0), (0, 0, 0, 0))
WS = [W1, W2, W3, W4, W5, W6]
for i, (x, y) in enumerate(WS, 1):
    w = word(x, y)
    say(f"  w{i} = {w}  mixed={len(set(w))>1}  clean={is_clean(T,w,act)}  "
        f"|fibre|={len(supported_matchings(T,w))}")
    assert len(set(w)) > 1 and is_clean(T, w, act)
    assert sorted(supported_matchings(T, w)) == sorted(FULLM)

E = [word_polynomial(T, vm, word(x, y)) for x, y in WS]

# abbreviations as polynomials
U1 = V(0, 7, 1, 0)
U0 = V(0, 7, 0, 0)
V00, V01, V20, V21 = V(1, 4, 0, 0), V(1, 4, 0, 1), V(1, 4, 2, 0), V(1, 4, 2, 1)
C = V(2, 3, 0, 0)
S00, S20 = V(5, 6, 0, 0), V(5, 6, 2, 0)
L0, L1, L2 = P_L((0, 0, 0, 0)), P_L((1, 0, 0, 0)), P_L((1, 2, 0, 0))
R0, Ra, Rb = P_R((0, 0, 0, 0)), P_R((0, 2, 0, 0)), P_R((1, 2, 0, 0))
K = pmul(pmul(U1, C), S20)
Kp = pmul(pmul(U0, C), S20)
J = pmul(pmul(U1, C), S00)
Jp = pmul(pmul(U0, C), S00)

# verify the binomial normal forms of the six equations + the constant
checks = [
    ("w1", E[0], padd(pmul(L1, Ra), pmul(K, V00))),
    ("w2", E[1], padd(pmul(L1, Rb), pmul(K, V01))),
    ("w3", E[2], padd(pmul(L2, Ra), pmul(K, V20))),
    ("w4", E[3], padd(pmul(L2, Rb), pmul(K, V21))),
    ("w5", E[4], padd(pmul(L0, Rb), pmul(Kp, V01))),
    ("w6", E[5], padd(pmul(L2, R0), pmul(J, V20))),
    ("0^8", G, padd(pmul(L0, R0), pmul(Jp, V00))),
]
for name, lhs, rhs in checks:
    ok = piszero(psub(lhs, rhs))
    say(f"  normal form {name:>3}: {ok}")
    assert ok

# --- the explicit cofactors, derived by hand and verified by expansion
M = psub(pmul(V00, V21), pmul(V01, V20))          # the 2x2 minor of A14

# (1)  K^2 * M = E1 E4 - E2 E3 - L2 Rb E1 + L2 Ra E2 + L1 Rb E3 - L1 Ra E4
lhs1 = pmul(pmul(K, K), M)
rhs1 = padd(padd(psub(pmul(E[0], E[3]), pmul(E[1], E[2])),
                 psub(pmul(pmul(L2, Ra), E[1]), pmul(pmul(L2, Rb), E[0]))),
            psub(pmul(pmul(L1, Rb), E[2]), pmul(pmul(L1, Ra), E[3])))
ok1 = piszero(psub(lhs1, rhs1))
say(f"\n  identity (1)  K^2 * minor(A14) in ideal(w1..w4): {ok1}")
assert ok1

# (2)  Rb*(L0 U1 V21 - L2 U0 V01) = U1 V21 E5 - U0 V01 E4
lhs2 = pmul(Rb, psub(pmul(pmul(L0, U1), V21), pmul(pmul(L2, U0), V01)))
rhs2 = psub(pmul(pmul(U1, V21), E[4]), pmul(pmul(U0, V01), E[3]))
ok2 = piszero(psub(lhs2, rhs2))
say(f"  identity (2)  Rb*(L0 U1 V21 - L2 U0 V01) in ideal(w4,w5): {ok2}")
assert ok2

# (3)  Rb L2 U1 V21 * G = <ideal(E4,E5,E6)> - K V21 P M ,  P = U0 U1 C S00
P = pmul(pmul(pmul(U0, U1), C), S00)
lhs3 = pmul(pmul(pmul(pmul(Rb, L2), U1), V21), G)
ideal3 = padd(
    padd(pmul(pmul(pmul(Rb, L2), pmul(U0, V01)), E[5]),
         pmul(pmul(L2, R0), psub(pmul(pmul(U1, V21), E[4]),
                                 pmul(pmul(U0, V01), E[3])))),
    padd(pneg(pmul(pmul(pmul(J, U0), pmul(V20, V01)), E[3])),
         pmul(pmul(pmul(U1, V21), pmul(Jp, V00)), E[3])))
rhs3 = psub(ideal3, pmul(pmul(pmul(K, V21), P), M))
ok3 = piszero(psub(lhs3, rhs3))
say(f"  identity (3)  Rb L2 U1 V21 * H_0^8 = ideal(w4,w5,w6) - K V21 P M: "
    f"{ok3}")
assert ok3

# --- assemble:  K^3 U1 V21^2 * G  in ideal(E1..E6)
# K^2*(3):  K^2 Rb L2 U1 V21 G = K^2*ideal3 - K V21 P (K^2 M)
#                              = K^2*ideal3 - K V21 P * rhs1     (in ideal)
# and       K^2 Rb L2 U1 V21 G = K^2 U1 V21 G (E4 - K V21)
# =>        K^3 U1 V21^2 G = K^2 U1 V21 G E4 - [K^2*ideal3 - K V21 P rhs1]
lhs4 = pmul(pmul(pmul(pmul(K, pmul(K, K)), U1), pmul(V21, V21)), G)
rhs4 = psub(pmul(pmul(pmul(pmul(K, K), U1), pmul(V21, G)), E[3]),
            psub(pmul(pmul(K, K), ideal3),
                 pmul(pmul(pmul(K, V21), P), rhs1)))
ok4 = piszero(psub(lhs4, rhs4))
say(f"  identity (4)  K^3 U1 V21^2 * H_0^8 in ideal(w1..w6): {ok4}")
assert ok4

say("\n  MULTIPLIER = A07[1][0]^4 * A23[0][0]^3 * A56[2][0]^3 * A14[2][1]^2")
say("  (K = A07[1][0]*A23[0][0]*A56[2][0]); every factor is an OCCUPIED cell,")
say("  hence nonzero on any exact source with this template.")
say("\n  => H_{w1..w6} = 0 (mixed)  ==>  H_{0^8} = 0.  But H_{0^8} != 0 is")
say("     required (constant word).  CONTRADICTION.")
say("\nVERDICT m=24: NO EXACT SOURCE HAS THIS TEMPLATE.  [PROVED-HERE]")

# ------------------------------------------------------- extra structure
# (recorded, not needed for the kill): the full clean system forces
# rank A45 = rank A56 = rank A67 = rank A07 = rank A14 = 1.
say("\nS5 (structure, for the family analysis): the clean system also "
    "forces rank-one blocks; see w15_task1b_structure.py")

# ------------------------------------------------------- Singular export
def to_singular(poly, names):
    """Singular syntax.  NB: a LEADING unary '+' is a parse error in
    Singular 4.4, and e1/mult/I are reserved names -- hence q1.., mm, Jid."""
    if not poly:
        return "0"
    terms = []
    for mon, c in sorted(poly.items()):
        num, den = c.numerator, c.denominator
        assert den == 1
        s = ("+" if num > 0 else "-") + (f"{abs(num)}" if abs(num) != 1
                                         or not mon else "")
        if mon:
            if abs(num) != 1:
                s += "*"
            s += "*".join(names[v] for v in mon)
        terms.append(s)
    out = "".join(terms)
    return out[1:] if out.startswith("+") else out


used = set()
for poly in E + [G]:
    for mon in poly:
        used.update(mon)
used = sorted(used)
local = {v: f"z{i}" for i, v in enumerate(used)}
names = {v: local[v] for v in used}
mult = pmul(pmul(pmul(pmul(K, pmul(K, K)), U1), pmul(V21, V21)), pconst(1))
sing = []
sing.append(f"ring r = 0,({','.join(local[v] for v in used)}),dp;")
for i, poly in enumerate(E, 1):
    sing.append(f"poly q{i} = {to_singular(poly, names)};")
sing.append(f"poly gc = {to_singular(G, names)};")
sing.append(f"poly mm = {to_singular(mult, names)};")
sing.append("ideal Jid = q1,q2,q3,q4,q5,q6;")
sing.append("ideal GB = groebner(Jid);")
sing.append("poly nf = reduce(mm*gc, GB);")
sing.append('"multiplier_times_constant_word_reduces_to_zero:"; (nf==0);')
sing.append("poly nf2 = reduce(gc, GB);")
sing.append('"CONTROL_constant_word_alone_reduces_to_zero(expect 0):"; '
            "(nf2==0);")
# leave-one-out controls: each of the six words must be load-bearing
for drop in range(1, 7):
    keep = ",".join(f"q{i}" for i in range(1, 7) if i != drop)
    sing.append(f"ideal Jd{drop} = {keep};")
    sing.append(f"poly nd{drop} = reduce(mm*gc, groebner(Jd{drop}));")
    sing.append(f'"CONTROL_drop_w{drop}_still_reduces_to_zero(expect 0):"; '
                f"(nd{drop}==0);")
sing.append("quit;")
open(os.path.join(HERE, "sing_m24_membership.sing"), "w").write(
    "\n".join(sing) + "\n")
say(f"\nSingular script written (variables used: {len(used)}).")

open(os.path.join(HERE, "log_task1_m24.txt"), "w").write("\n".join(LOG) + "\n")
json.dump({"verdict_m24": "killed",
           "certificate_words": [list(word(x, y)) for x, y in WS],
           "constant_word_killed": list(w0),
           "multiplier": "A07[1][0]^4*A23[0][0]^3*A56[2][0]^3*A14[2][1]^2",
           "identities_verified": [ok1, ok2, ok3, ok4],
           "clean_words": n_clean, "clean_mixed_words": n_clean_mixed,
           "n_vars_in_certificate": len(used)},
          open(os.path.join(HERE, "results_task1_m24.json"), "w"), indent=1)
