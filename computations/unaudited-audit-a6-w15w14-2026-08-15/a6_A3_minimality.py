#!/usr/bin/env python3
"""A6 / TARGET A step 3b: is the seven-word certificate MINIMAL?

W15 claims leave-one-out minimality 6/6 ("dropping any word destroys
it").  That control fixes W15's multiplier.  A6 re-derives the kill and
finds a FIVE-mixed-word certificate (w4 = 12001200 is redundant):

    K^2 V01 V20 * H_{0^8}  in  ideal(H_w1, H_w2, H_w3, H_w5, H_w6)

with K = A07[1][0] A23[0][0] A56[2][0], V01 = A14[0][1], V20 = A14[2][0]
-- again a product of occupied cells.  Verified by exact expansion here,
and by an independent Singular reduction in a6_A4_singular.sing.

Also: exact rational point witnesses proving that none of the remaining
five words can be dropped (4-word subsets of this family do NOT kill).
"""
from __future__ import annotations

import json
import random
from fractions import Fraction

import a6_engine as E

T = E.M24
V = E.Vars(T)
out = {}

W = {1: (1, 0, 0, 0, 0, 2, 0, 0), 2: (1, 0, 0, 0, 1, 2, 0, 0),
     3: (1, 2, 0, 0, 0, 2, 0, 0), 4: (1, 2, 0, 0, 1, 2, 0, 0),
     5: (0, 0, 0, 0, 1, 2, 0, 0), 6: (1, 2, 0, 0, 0, 0, 0, 0)}
Z = (0,) * 8
H = {i: E.Hpoly(T, V, w) for i, w in W.items()}
G = E.Hpoly(T, V, Z)


def c(u, v, i, j):
    return {(V.v(E.EIDX[(u, v)], 3 * i + j),): 1}


def mm(*ps):
    r = {(): 1}
    for p in ps:
        r = E.pmul(r, p)
    return r


U0, U1 = c(0, 7, 0, 0), c(0, 7, 1, 0)
V00, V01, V20, V21 = c(1, 4, 0, 0), c(1, 4, 0, 1), c(1, 4, 2, 0), c(1, 4, 2, 1)
CC = c(2, 3, 0, 0)
S00, S20 = c(5, 6, 0, 0), c(5, 6, 2, 0)
K, Kp, Jj, Jp = mm(U1, CC, S20), mm(U0, CC, S20), mm(U1, CC, S00), mm(U0, CC, S00)

# ---------------- FIVE-WORD certificate:  K^2 V01 V20 G in I(E1,E2,E3,E5,E6)
A, B, C3, D, F = H[1], H[2], H[3], H[5], H[6]


def PL(x):
    return E.padd(E.padd(mm(c(0, 1, x[0], x[1]), c(2, 3, x[2], x[3])),
                         mm(c(0, 2, x[0], x[2]), c(1, 3, x[1], x[3]))),
                  mm(c(0, 3, x[0], x[3]), c(1, 2, x[1], x[2])))


def PR(y):
    return E.padd(mm(c(4, 5, y[0], y[1]), c(6, 7, y[2], y[3])),
                  mm(c(4, 7, y[0], y[3]), c(5, 6, y[1], y[2])))


L0, L1, L2 = PL((0, 0, 0, 0)), PL((1, 0, 0, 0)), PL((1, 2, 0, 0))
R0, Ra, Rb = PR((0, 0, 0, 0)), PR((0, 2, 0, 0)), PR((1, 2, 0, 0))

# CLOSED FORM of the five-word certificate (A6, derived by hand):
#  K^2 V01 V20 G = J K' V01 V20 E1 - L0 R0 L2 Ra E2 + K V01 L0 R0 E3
#                  + L1 Ra L2 R0 E5 - K' V01 L1 Ra E6
cof5 = {1: mm(Jj, Kp, V01, V20),
        2: E.pneg(mm(L0, R0, L2, Ra)),
        3: mm(K, V01, L0, R0),
        5: mm(L1, Ra, L2, R0),
        6: E.pneg(mm(Kp, V01, L1, Ra))}
mult5_cf = mm(K, K, V01, V20)
acc5 = {}
for i, cf in cof5.items():
    acc5 = E.padd(acc5, E.pmul(cf, H[i]))
out["FIVE_WORD_closed_form_verified"] = (acc5 == E.pmul(mult5_cf, G))
out["FIVE_WORD_closed_form"] = ("K^2 V01 V20 G = J K' V01 V20 E1 "
                                "- L0 R0 L2 Ra E2 + K V01 L0 R0 E3 "
                                "+ L1 Ra L2 R0 E5 - K' V01 L1 Ra E6")
# mutation controls on this checker
out["mc_five_sign_flip_fails"] = (
    E.padd(acc5, E.pmul(E.pmul({(): 2}, cof5[2]), H[2])) !=
    E.pmul(mult5_cf, G))
out["mc_five_drop_E1_term_fails"] = (
    E.psub(acc5, E.pmul(cof5[1], H[1])) != E.pmul(mult5_cf, G))
out["mc_five_multiplier_K1_fails"] = (
    acc5 != E.pmul(mm(K, V01, V20), G))

# ------------------------------------------------- point witnesses: 4 is not enough
# Build exact rational points satisfying four of the five equations with
# G != 0 and every occupied cell nonzero.
FULLE = [(0, 1), (0, 2), (0, 3), (0, 7), (1, 2), (1, 3), (1, 4), (2, 3),
         (4, 5), (4, 7), (5, 6), (6, 7)]


def rand_point(rng):
    val = {}
    for (u, v) in FULLE:
        for i in range(3):
            for j in range(3):
                val[V.v(E.EIDX[(u, v)], 3 * i + j)] = Fraction(
                    rng.randint(1, 9), rng.randint(1, 5)) * rng.choice([1, -1])
    return val


def ev(p, val):
    return E.peval(p, val)


def setv(val, poly1var, x):
    (mon,), = [(k,) for k in poly1var]
    val[mon[0]] = x


# variable ids of the cells we solve for
id_V00 = V.v(E.EIDX[(1, 4)], 0 * 3 + 0)
id_V01 = V.v(E.EIDX[(1, 4)], 0 * 3 + 1)
id_V20 = V.v(E.EIDX[(1, 4)], 2 * 3 + 0)
id_V21 = V.v(E.EIDX[(1, 4)], 2 * 3 + 1)
id_A01_00 = V.v(E.EIDX[(0, 1)], 0)          # occurs in L0 only (x=(0,0,0,0))
id_A45_00 = V.v(E.EIDX[(4, 5)], 0)          # occurs in R0 only (y=(0,0,0,0))
id_A23_00 = V.v(E.EIDX[(2, 3)], 0)


def solve_linear(poly, var, val):
    """Solve poly = 0 for `var` (poly must be linear in var)."""
    a = Fraction(0)
    b = Fraction(0)
    for mon, co in poly.items():
        k = mon.count(var)
        if k == 0:
            t = Fraction(co)
            for v in mon:
                t *= val[v]
            b += t
        elif k == 1:
            t = Fraction(co)
            for v in mon:
                if v != var:
                    t *= val[v]
            a += t
        else:
            raise SystemExit("not linear")
    if a == 0:
        return None
    return -b / a


rng = random.Random(20260815)
witness = {}
for drop in (1, 2, 3, 5, 6):
    keep = [i for i in (1, 2, 3, 5, 6) if i != drop]
    found = None
    for _ in range(4000):
        val = rand_point(rng)
        # solve the kept equations one at a time for dedicated free cells
        order = {1: (id_V00, H[1]), 2: (id_V01, H[2]), 3: (id_V20, H[3]),
                 5: (id_A01_00, H[5]), 6: (id_A45_00, H[6])}
        ok = True
        for i in keep:
            var, poly = order[i]
            x = solve_linear(poly, var, val)
            if x is None or x == 0:
                ok = False
                break
            val[var] = x
        if not ok:
            continue
        if any(v == 0 for v in val.values()):
            continue
        if any(ev(H[i], val) != 0 for i in keep):
            continue
        g = ev(G, val)
        if g != 0:
            found = dict(drop=drop, kept=keep, G=str(g),
                         all_cells_nonzero=True,
                         kept_all_zero=True,
                         point={V.name[k]: str(v) for k, v in sorted(val.items())})
            break
    witness[drop] = ({"found": True, "G_value": found["G"]} if found
                     else {"found": False})
    if found:
        json.dump(found, open("witness_drop_w%d.json" % drop, "w"), indent=1)
out["four_word_subsets_do_not_kill"] = witness

# and the control: with ALL FIVE kept, no such point can exist
val = rand_point(rng)
cnt = 0
for _ in range(300):
    val = rand_point(rng)
    ok = True
    for i, (var, poly) in {1: (id_V00, H[1]), 2: (id_V01, H[2]),
                           3: (id_V20, H[3]), 5: (id_A01_00, H[5]),
                           6: (id_A45_00, H[6])}.items():
        x = solve_linear(poly, var, val)
        if x is None or x == 0:
            ok = False
            break
        val[var] = x
    if not ok:
        continue
    if any(ev(H[i], val) != 0 for i in (1, 2, 3, 5, 6)):
        continue
    cnt += 1
    if ev(G, val) != 0:
        out["CONTROL_five_word_point_with_G_nonzero"] = "FOUND (would refute)"
        break
else:
    out["CONTROL_five_word_points_tested"] = cnt
    out["CONTROL_five_word_all_have_G_zero"] = True

json.dump(out, open("results_A3_minimality.json", "w"), indent=1)
print(json.dumps(out, indent=1))
