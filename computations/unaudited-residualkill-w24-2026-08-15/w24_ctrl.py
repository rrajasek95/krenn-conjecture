#!/usr/bin/env python3
"""W24 -- CONTROLS.  UNAUDITED.  Exact only.

 C1  template equality with w21_core (independent re-typing).
 C2  engine cross-check: W24's from-the-definition Phi / residual verdict vs
     W21's engine on every stored exact clean point (T5).
 C3  MULTI-CHARACTERISTIC (ledger 19): the identity W24-C and the
     non-degeneracy det M = 2 X0 X1 X2 checked over F_p for p = 7, 13, 31
     (all = 1 mod 3, so a primitive cube root of unity EXISTS there -- the
     exact residue that broke W21's F_5 sweep) and over F_2 (where the
     statement is FALSE, so the control fires).
 C4  ledger-18 / T1 explicit-point control on the OTHER side: relaxations of
     the residual system that ARE consistent with a nonzero cell must be
     reported NOT KILLED by the same verdict function.
 C5  positive control: a synthetic 12-unknown system with an all-nonzero
     solution must report 0 forced cells and consistent.
 C6  mutation control: perturbing one Gamma cell of a clean point must break
     the clean layer (so the clean hypothesis is not vacuous).
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
W21 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
       "unaudited-finishing-w21-2026-08-15")
sys.path.insert(0, W21)
import w24_core as C                                              # noqa: E402
import w24_pts as P                                               # noqa: E402
import w24_resid as RS                                            # noqa: E402
import w24_ident as ID                                            # noqa: E402

out = {"_header": "UNAUDITED W24 controls."}

# ---------------------------------------------------------------- C1
import w21_core as K                                              # noqa: E402
c1 = all(list(C.TEMPLATES[m]) == list(K.W8_IMMUNE[m])
         for m in (24, 25, 26, 27, 28))
c1b = (list(C.PMS) == list(K.PMS)) and (list(C.MIXED) == list(K.MIXED))
print("C1 templates/PMS/MIXED identical to w21_core:", c1, c1b)
out["C1_templates_match"] = bool(c1 and c1b)

# ---------------------------------------------------------------- C2
import w21_resid as WR                                            # noqa: E402
rows = []
mism = 0
for m, tag, bl in P.stored_points():
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    T = K.W8_IMMUNE[m]
    gam = K.gamma_edges(T)
    r21 = WR.residual_linear_test(T, bl)
    k21 = r21["inconsistent"] or bool(r21.get("forced_zero_cells"))
    r24 = RS.verdict(m, bl)
    # phi cross-check on 200 words
    rng = random.Random(99 + m)
    ws = [tuple(rng.randrange(3) for _ in range(8)) for _ in range(200)]
    dphi = sum(1 for w in ws
               if C.phi(bl, gs, w) != K.phi_value(bl, gam, w))
    mism += dphi
    rows.append(dict(m=m, tag=tag, w21_killed=k21, w24_killed=r24["killed"],
                     agree=(k21 == r24["killed"]), phi_mismatches=dphi))
n_ag = sum(1 for r in rows if r["agree"])
print("C2 engine cross-check on %d stored points: verdict agreement %d/%d, "
      "Phi mismatches %d/%d words"
      % (len(rows), n_ag, len(rows), mism, 200 * len(rows)))
out["C2"] = dict(n=len(rows), agree=n_ag, phi_mismatches=mism,
                 rows=rows)

# ---------------------------------------------------------------- C3
SIG = {0: 7, 1: 4, 2: 5, 3: 6}
L = (0, 1, 2, 3)


def mod_check(p, m, trials=200, seed=7):
    """identity W24-C and det M = 2 X0X1X2 over F_p."""
    gam = C.gamma_edges(C.TEMPLATES[m])
    gs = set(gam)
    rng = random.Random(seed)
    bad = 0
    zerodet = 0
    tot = 0
    for _ in range(trials):
        bl = {e: [[Fraction(rng.randrange(1, p)) for _ in range(3)]
                  for _ in range(3)] for e in gam}
        w = tuple(rng.randrange(3) for _ in range(8))
        x, y = w[:4], w[4:]
        for i in L:
            ps = [q for q in L if q != i]
            p1, p2, p3 = ps
            F = {a: ID.cell(bl, gs, SIG[a], SIG[i], y[SIG[a] - 4],
                            y[SIG[i] - 4]) for a in ps}
            D = {a: ID.cell(bl, gs, a, SIG[a], x[a], y[SIG[a] - 4])
                 for a in ps}
            G = {(min(a, b), max(a, b)):
                 ID.cell(bl, gs, min(a, b), max(a, b),
                         x[min(a, b)], x[max(a, b)])
                 for a in ps for b in ps if a < b}
            c = [ID.coeff(bl, gs, (i, SIG[q]), w) for q in ps]
            lhs = F[p1] * c[0] - F[p2] * c[1] + F[p3] * c[2]
            rhs = 2 * G[(min(p1, p3), max(p1, p3))] * D[p2] * F[p1] * F[p3]
            tot += 1
            if (lhs - rhs).numerator % p != 0:
                bad += 1
            X = [G[(min(b, cc), max(b, cc))] * D[a]
                 for a in ps for (b, cc) in
                 [tuple(sorted(set(ps) - {a}))]]
            det = 2 * X[0] * X[1] * X[2]
            if det.numerator % p == 0:
                zerodet += 1
    return bad, zerodet, tot


c3 = {}
for p in (2, 7, 13, 31):
    b, z, t = mod_check(p, 28)
    c3["p=%d" % p] = dict(identity_failures=b, zero_dets=z, tests=t)
    print("C3 char %-3d: identity failures %d/%d, det M = 0 in %d/%d draws "
          "(all block entries drawn NONZERO mod p)%s"
          % (p, b, t, z, t, "   <-- control fires (char 2)"
             if p == 2 else ""))
out["C3_multichar"] = c3

# ---------------------------------------------------------------- C4/C5
m, tag, bl = [r for r in P.stored_points() if r[0] == 28][0]
cells, allrows, cleanw = RS.build_system(28, bl)
n = len(cells)


def verdict_rows(rws, n):
    aug = [list(v) + [-c] for _, v, c in rws]
    R, piv = C.rref(aug, n + 1)
    if n in piv:
        return dict(inconsistent=True, forced=[], killed=True)
    sol = [Fraction(0)] * n
    for k, pc in enumerate(piv):
        if pc < n:
            sol[pc] = R[k][n]
    ker = C.kernel_basis([list(v) for _, v, _ in rws], n)
    f = [k for k in range(n) if sol[k] == 0 and all(b[k] == 0 for b in ker)]
    return dict(inconsistent=False, forced=f, killed=bool(f),
                sol=[str(s) for s in sol])


full = verdict_rows(allrows, n)
# relaxation: keep only ONE row, which has a single variable and a NONZERO
# constant -> consistent with that cell nonzero, so NOT killed.
cand = [r for r in allrows
        if r[2] != 0 and len([k for k in range(n) if r[1][k] != 0]) == 1]
rel = verdict_rows(cand[:1], n) if cand else None
print("C4 relaxation control: full system killed=%s ; keeping ONE row with a "
      "nonzero constant and one variable -> killed=%s (want False), solution "
      "coordinate nonzero=%s"
      % (full["killed"], rel and rel["killed"],
         rel and any(s != "0" for s in rel["sol"])))
out["C4_relaxation"] = dict(full_killed=full["killed"],
                            relaxed_killed=rel and rel["killed"],
                            n_candidate_rows=len(cand))
# a bigger consistent relaxation: all rows of ONE single e whose ratios agree
from collections import defaultdict                              # noqa: E402
byc = defaultdict(list)
for r in allrows:
    nz = [k for k in range(n) if r[1][k] != 0]
    if len(nz) == 1:
        byc[nz[0]].append(r)
best = None
for k, rs in byc.items():
    ratios = {(-r[2] / r[1][k]) for r in rs}
    if len(ratios) == 1 and 0 not in ratios:
        best = (k, len(rs))
print("C4b any single-cell family that is consistent with a NONZERO value:",
      best)
out["C4b_consistent_family"] = best

rng = random.Random(5150)
tgt = [Fraction(rng.randint(1, 9)) for _ in range(12)]
srows = []
for _ in range(300):
    rr = [Fraction(rng.randint(-5, 5)) for _ in range(12)]
    srows.append((None, rr, -sum(rr[i] * tgt[i] for i in range(12))))
sv = verdict_rows(srows, 12)
print("C5 positive control (system with an all-nonzero solution): killed=%s "
      "(want False), forced=%d (want 0), solution recovered=%s"
      % (sv["killed"], len(sv["forced"]),
         [str(t) for t in tgt] == sv["sol"]))
out["C5_positive"] = dict(killed=sv["killed"], n_forced=len(sv["forced"]),
                          recovered=([str(t) for t in tgt] == sv["sol"]))

# ---------------------------------------------------------------- C6
gs = set(C.gamma_edges(C.TEMPLATES[28]))
clean = P.w21_clean(28)
base = sum(1 for w in clean if C.phi(bl, gs, w) != 0)
bad = {e: [r[:] for r in bl[e]] for e in bl}
bad[(4, 5)][0][0] = bad[(4, 5)][0][0] + Fraction(1, 7)
mut = sum(1 for w in clean if C.phi(bad, gs, w) != 0)
print("C6 mutation control: clean violations before %d (want 0), after "
      "perturbing A_45[0][0] by 1/7: %d (want > 0)" % (base, mut))
out["C6_mutation"] = dict(before=base, after=mut)

json.dump(out, open(os.path.join(HERE, "results_ctrl.json"), "w"),
          indent=1, default=str)
