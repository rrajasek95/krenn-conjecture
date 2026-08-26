#!/usr/bin/env python3
"""W19 -- m = 25, BRANCH B: the lam-eliminated reduction, and the kill.
UNAUDITED.  Exact (Singular over Q, guarded).

W16's Branch B (their Theorem W16-A, gauge-fixed): after the vertex-6
dichotomy the surviving branch has

  A45 = mu * v (x) m,  A47 = nu * v (x) u,  v = A14[2][.], m = A25[0][.],
  u = A07[1][.],  A07[2][.] parallel to u,  and, in the gauge
  v = m = u = (1,1,1), A07[2][.] = (1,1,1), A03[0][.] = (1,1,1),
  A67[c][0] = 1, A14[x1][0] = 1 (x1 = 0,1), A25[x2][0] = 1 (x2 = 1,2),
  A07[0][0] = 1,

    Phi(x,y) = lam_x * g(b,c,d) + F_a * k_x(b,c,d)
    g(b,c,d)   = mu*A67[c][d] + nu*A56[b][c]
    k_x(b,c,d) = A03[x0][x3]*A25[x2][b]*A67[c][d]
                 + A23[x2][x3]*A07[x0][d]*A56[b][c]
    F_a = A14[x1][a],   (a,b,c,d) = (y4,y5,y6,y7),  lam_x = P_L(x) FREE
    (the lam relaxation is sound for forcing verdicts: it only drops
     constraints).

THE NEW STEP (W19).  Phi depends on a = y4 ONLY through F_a, and the
effectively clean set is a PRODUCT box S4 x S5 x S6 x S7 per L-word x.
So for a fixed x the clean equations are

    lam_x * G + F_a * K = 0   for every a in S4,  G = g|B, K = k_x|B,
    B = S5 x S6 x S7.

Eliminating the free scalar lam_x (and using F_a != 0, all cells nonzero):

  (E1)  G_i K_j - G_j K_i = 0            for all i, j in B      [solvable]
  (E2)  (F_a - F_a') K_i = 0             for all a,a' in S4, i in B

(E2) is the engine X_free could never reach: X_free consists exactly of
the four L-words with x1 = 2, where F_a = A14[2][a] = 1 identically, so
(E2) is VACUOUS there.  That is precisely why X_free is insufficient
(W16 measured the insufficiency; this identifies its cause).

CONSEQUENCE (proved by hand, verified below):
  if A14[0][.] and A14[1][.] are both constant -> SITE 4 FACTORS;
  otherwise (E2) forces k_x == 0 on the whole box B_x for the eight
  L-words x with that x1 and S4 = {0,1,2}, and that -- with (E1) at the
  L-words with x2 = 1 -- forces SITE 5 to factor.
Either way a factoring site exists at m = 25, and sites 4 and 5 both carry
(clean, k=1) pairs, so mechanism W16-B kills Branch B.
"""
from __future__ import annotations
import os
import sys
import json
import itertools
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w19_core import (W8_IMMUNE, EDGES, EIDX, VarMap, phi_poly, peval,
                      full_pm_indices, extras_at, gamma_edges)
from w19_sing import run_singular, check_no_shadowing, SingularError

T25 = W8_IMMUNE[25]
FULLM25 = full_pm_indices(T25)
GAM25 = gamma_edges(T25)

# ---------------------------------------------------------- clean boxes ---
# single cells of the m=24..28 family, as (edge, (row,col)):
#  04:(0,0) 05:(0,1) 06:(0,2) 15:(1,0) 16:(1,1) 17:(0,2)
#  24:(1,0) 26:(2,1) 27:(1,2) 34:(2,0) 35:(2,1) 37:(2,2)


_BOX = {}


def _build_boxes():
    """EXACT effectively-clean alphabets per L-word.

    W16 used the WORD-clean predicate (no single-cell block active), which is
    strictly stronger; the exact effectively-clean set has 2624 words against
    2152 word-clean ones, and -- verified below -- it is still a PRODUCT box
    S4 x S5 x S6 x S7 for every one of the 81 L-words.  The extra 472 words
    matter: with the exact predicate there are 24 L-words with S4 = {0,1,2}
    covering ALL THREE values of x1 (W16's word-clean X_free had x1 = 2 only,
    where A14[2][.] = (1,1,1) makes the (E2) engine vacuous)."""
    for x in itertools.product(range(3), repeat=4):
        ys = [y for y in itertools.product(range(3), repeat=4)
              if not extras_at(T25, tuple(x) + tuple(y), FULLM25)]
        proj = [sorted({y[k] for y in ys}) for k in range(4)] if ys \
            else [[], [], [], []]
        n = 1
        for p in proj:
            n *= len(p)
        assert n == len(ys), ("clean set is not a product box", x)
        _BOX[tuple(x)] = proj


def S_sets(x):
    if not _BOX:
        _build_boxes()
    return _BOX[tuple(x)]


def control_S_sets():
    """S_sets must reproduce the EXACT effectively-clean predicate."""
    bad = 0
    tested = 0
    for x in itertools.product(range(3), repeat=4):
        S4, S5, S6, S7 = S_sets(x)
        for y in itertools.product(range(3), repeat=4):
            w = tuple(x) + tuple(y)
            pred = (y[0] in S4 and y[1] in S5 and y[2] in S6 and y[3] in S7)
            truth = not extras_at(T25, w, FULLM25)
            tested += 1
            if pred != truth:
                bad += 1
    return dict(tested=tested, mismatches=bad)


# --------------------------------------------------------- the symbols ----
MU, NU = "mu", "nu"
S = [["s%d%d" % (b, c) for c in range(3)] for b in range(3)]           # A56
Tt = [["1" if d == 0 else "t%d%d" % (c, d) for d in range(3)]
      for c in range(3)]                                              # A67
F = [["1" if a == 0 else "f%d%d" % (i, a) for a in range(3)]
     for i in range(2)] + [["1", "1", "1"]]                           # A14
G25 = [["1", "1", "1"]] + [["1" if b == 0 else "g%d%d" % (i, b)
                            for b in range(3)] for i in (1, 2)]       # A25
H = [["1" if d == 0 else "h%d" % d for d in range(3)],
     ["1", "1", "1"], ["1", "1", "1"]]                                # A07
P = [["1", "1", "1"]] + [["p%d%d" % (i, j) for j in range(3)]
                         for i in (1, 2)]                             # A03
QQ = [["q%d%d" % (i, j) for j in range(3)] for i in range(3)]         # A23

ALLVARS = sorted({v for M in (S, Tt, F, G25, H, P, QQ) for row in M
                  for v in row if v != "1"} | {MU, NU})
CELLS = [v for v in ALLVARS]


def g_expr(b, c, d):
    return "(%s*%s+%s*%s)" % (MU, Tt[c][d], NU, S[b][c])


def k_expr(x, b, c, d):
    x0, x1, x2, x3 = x
    return "(%s*%s*%s+%s*%s*%s)" % (P[x0][x3], G25[x2][b], Tt[c][d],
                                    QQ[x2][x3], H[x0][d], S[b][c])


# ------------------------------------------------- numeric control model --
def numeric_phi(env, x, y):
    """Phi from the Branch-B closed form, evaluated exactly."""
    a, b, c, d = y

    def V(e):
        return Fraction(1) if e == "1" else env[e]
    g = V(MU) * V(Tt[c][d]) + V(NU) * V(S[b][c])
    k = (V(P[x[0]][x[3]]) * V(G25[x[2]][b]) * V(Tt[c][d])
         + V(QQ[x[2]][x[3]]) * V(H[x[0]][d]) * V(S[b][c]))
    return env["lam%d%d%d%d" % tuple(x)] * g + V(F[x[1]][a]) * k


def control_phi(seeds=(3, 19, 101)):
    """the Branch-B closed form must equal the model's Phi_w on an
    exact Branch-B point of the m=25 template."""
    vm = VarMap(T25)
    bad = tested = 0
    for seed in seeds:
        s = seed

        def rn():
            nonlocal s
            s = (1103515245 * s + 12345) % (1 << 31)
            return Fraction((s % 13) - 6 or 5, (s % 5) + 1)
        env = {v: rn() for v in ALLVARS}
        # build the full block set consistent with the Branch-B gauge
        B = {}

        def val(e):
            return Fraction(1) if e == "1" else env[e]
        B[(5, 6)] = [[val(S[b][c]) for c in range(3)] for b in range(3)]
        B[(6, 7)] = [[val(Tt[c][d]) for d in range(3)] for c in range(3)]
        B[(1, 4)] = [[val(F[i][a]) for a in range(3)] for i in range(3)]
        B[(2, 5)] = [[val(G25[i][b]) for b in range(3)] for i in range(3)]
        B[(0, 7)] = [[val(H[i][d]) for d in range(3)] for i in range(3)]
        B[(0, 3)] = [[val(P[i][j]) for j in range(3)] for i in range(3)]
        B[(2, 3)] = [[val(QQ[i][j]) for j in range(3)] for i in range(3)]
        B[(4, 5)] = [[env[MU] for _ in range(3)] for _ in range(3)]
        B[(4, 7)] = [[env[NU] for _ in range(3)] for _ in range(3)]
        for e in ((0, 1), (0, 2), (1, 2), (1, 3)):
            B[e] = [[rn() for _ in range(3)] for _ in range(3)]
        vals = {}
        for ei, e in enumerate(EDGES):
            if T25[ei] != 511:
                continue
            for cc in range(9):
                vals[vm.v(ei, cc)] = B[e][cc // 3][cc % 3]
        for x in itertools.product(range(3), repeat=4):
            PL = (B[(0, 1)][x[0]][x[1]] * B[(2, 3)][x[2]][x[3]]
                  + B[(0, 2)][x[0]][x[2]] * B[(1, 3)][x[1]][x[3]]
                  + B[(0, 3)][x[0]][x[3]] * B[(1, 2)][x[1]][x[2]])
            env["lam%d%d%d%d" % tuple(x)] = PL
            for y in itertools.product(range(3), repeat=4):
                got = numeric_phi(env, x, y)
                want = peval(phi_poly(T25, vm, tuple(x) + tuple(y), FULLM25),
                             vals)
                tested += 1
                if got != want:
                    bad += 1
    return dict(tested=tested, mismatches=bad)


# ------------------------------------------------------- the equations ----
XFREE = [(x0, 2, 0, x3) for x0 in (1, 2) for x3 in (0, 1)]


def base_eqs(include_E1=True, include_E2=True, Xs=None):
    eqs = []
    Xs = list(itertools.product(range(3), repeat=4)) if Xs is None else Xs
    for x in Xs:
        S4, S5, S6, S7 = S_sets(x)
        Bx = [(b, c, d) for b in S5 for c in S6 for d in S7]
        gs = [g_expr(*i) for i in Bx]
        ks = [k_expr(x, *i) for i in Bx]
        if include_E1:
            for i in range(len(Bx)):
                for j in range(i + 1, len(Bx)):
                    eqs.append("%s*%s-%s*%s" % (gs[i], ks[j], gs[j], ks[i]))
        if include_E2:
            for ai in range(len(S4)):
                for aj in range(ai + 1, len(S4)):
                    fa, fb = F[x[1]][S4[ai]], F[x[1]][S4[aj]]
                    if fa == fb:
                        continue
                    for kk in ks:
                        eqs.append("(%s-%s)*%s" % (fa, fb, kk))
    # Branch-B hypothesis: lam_x mu = -A03[x0][x3], lam_x nu = -A23[0][x3]
    for x in XFREE:
        x0, _, _, x3 = x
        eqs.append("%s*%s-%s*%s" % (NU, P[x0][x3], MU, QQ[0][x3]))
        S4, S5, S6, S7 = S_sets(x)
        for b in S5:
            for c in S6:
                for d in S7:
                    eqs.append("%s*%s+%s*%s" % (MU, k_expr(x, b, c, d),
                                                P[x0][x3], g_expr(b, c, d)))
    return [e for e in eqs if e.strip()]


# ----------------------------------------------------- factoring targets --
def site_minors(t):
    """2x2 minors of the matrix whose columns are the t-side vectors of all
    Gamma blocks at t (only sites 4,5,6,7 are visible in the relaxed model:
    the L-side blocks A01,A02,A12,A13 were absorbed into the free lam)."""
    if t == 4:                       # A14 (col), A45 = mu J, A47 = nu J
        cols = [[F[i][a] for i in range(3)] for a in range(3)]
        cols = [[F[i][a] for a in range(3)] for i in range(3)]
        # 4-side index is a: columns indexed by x1 and by the (constant)
        # A45, A47 columns (all-ones), so factoring <=> each A14[i][.] const
        cols = [[F[i][a] for a in range(3)] for i in range(3)] \
            + [["1", "1", "1"]]
    elif t == 5:                     # A25 (col b), A45 (col), A56 (row b)
        cols = [[G25[i][b] for b in range(3)] for i in range(3)] \
            + [["1", "1", "1"]] \
            + [[S[b][c] for b in range(3)] for c in range(3)]
    elif t == 6:                     # A56 (col c), A67 (row c)
        cols = [[S[b][c] for c in range(3)] for b in range(3)] \
            + [[Tt[c][d] for c in range(3)] for d in range(3)]
    elif t == 7:                     # A07 (col d), A47 (col), A67 (col d)
        cols = [[H[i][d] for d in range(3)] for i in range(3)] \
            + [["1", "1", "1"]] \
            + [[Tt[c][d] for d in range(3)] for c in range(3)]
    else:
        return []
    out = []
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            for a in range(3):
                for b in range(a + 1, 3):
                    if (cols[i][a], cols[j][b]) == (cols[i][b], cols[j][a]):
                        continue                      # identically zero
                    out.append("%s*%s-%s*%s" % (cols[i][a], cols[j][b],
                                                cols[i][b], cols[j][a]))
    return sorted(set(out))


# --------------------------------------------------------------- Singular
def forced(eqs, targets, tag, timeout=3600, extra_nonzero=()):
    gens = ["zzg%d" % i for i in range(1, len(eqs) + 1)]
    check_no_shadowing(ALLVARS, gens + ["zzI", "zzGB", "zzJ", "zzL", "zzS",
                                        "zzP", "zzt"])
    nz = sorted(set(list(CELLS) + list(extra_nonzero)))
    ll = ['LIB "elim.lib";', "ring r = 0,(%s),dp;" % ",".join(ALLVARS)]
    for i, e in enumerate(eqs, 1):
        ll.append("poly zzg%d = %s;" % (i, e))
    ll.append("ideal zzI = %s;" % ",".join(gens))
    ll.append("poly zzP = %s;" % "*".join(nz))
    ll.append("ideal zzJ = zzP;")
    ll.append("list zzL = sat(zzI,zzJ);")
    ll.append("ideal zzS = zzL[1];")
    ll.append("ideal zzGB = groebner(zzS);")
    ll.append("int nbad = 0;")
    for tg in targets:
        ll.append("if (reduce(%s,zzGB) != 0) { nbad = nbad + 1; }" % tg)
    ll.append('"NBAD:"; nbad;')
    ll.append('"UNIT:"; (zzGB[1]==1);')
    ll.append("quit;")
    t0 = time.time()
    out, st = run_singular("\n".join(ll) + "\n", timeout=timeout)
    if st == "TIMEOUT":
        return dict(tag=tag, verdict=None, secs=timeout, n_eqs=len(eqs),
                    n_targets=len(targets))
    nbad = int(out.split("NBAD:")[1].strip().split()[0])
    return dict(tag=tag, n_eqs=len(eqs), n_targets=len(targets),
                n_not_forced=nbad, all_forced=(nbad == 0),
                clean_layer_unit_ideal=(out.split("UNIT:")[1].strip()
                                        .split()[0] == "1"),
                secs=round(time.time() - t0, 1))


# ------------------------------------------------------------ the cases --
def full_S4_words(x1):
    out = []
    for x in itertools.product(range(3), repeat=4):
        if x[1] != x1:
            continue
        if S_sets(x)[0] == [0, 1, 2]:
            out.append(tuple(x))
    return out


def k_zero_eqs(x1):
    """(E2) with S4 = {0,1,2}: if A14[x1][.] is NOT constant then k_x
    vanishes on the whole clean box, for every L-word x with that x1 and a
    full site-4 alphabet."""
    eqs = []
    for x in full_S4_words(x1):
        _, S5, S6, S7 = S_sets(x)
        for b in S5:
            for c in S6:
                for d in S7:
                    eqs.append(k_expr(x, b, c, d))
    return eqs


def case_equations(case, with_E1=False, with_branch=True):
    """case 1: A14[0] and A14[1] both constant -> site 4 factors (immediate)
       case 2: A14[0] NOT constant  -> k_x == 0 on the full-S4 x1=0 boxes
       case 3: A14[0] constant, A14[1] NOT constant -> ditto with x1=1"""
    eqs = []
    if with_branch:
        for x in XFREE:
            x0, _, _, x3 = x
            eqs.append("%s*%s-%s*%s" % (NU, P[x0][x3], MU, QQ[0][x3]))
    if case == 1:
        for i in (0, 1):
            for a in (1, 2):
                eqs.append("%s-1" % F[i][a])
    elif case == 2:
        eqs += k_zero_eqs(0)
    elif case == 3:
        for a in (1, 2):
            eqs.append("%s-1" % F[0][a])
        eqs += k_zero_eqs(1)
    if with_E1:
        eqs += base_eqs(include_E1=True, include_E2=True)
    return [e for e in eqs if e.strip()]


def main():
    res = {}
    res["CONTROL_S_sets_is_product_box"] = "asserted in _build_boxes"
    res["CONTROL_phi_closed_form"] = control_phi()
    print("CONTROL Branch-B closed form vs model Phi:",
          res["CONTROL_phi_closed_form"], flush=True)
    res["full_S4_words"] = {i: [list(x) for x in full_S4_words(i)]
                            for i in range(3)}
    print("L-words with full site-4 alphabet, by x1:",
          {i: len(v) for i, v in res["full_S4_words"].items()}, flush=True)
    plan = [(1, (4,), False), (2, (6, 5, 4, 7), False),
            (3, (6, 5, 7, 4), False), (3, (6, 5, 7, 4), True)]
    done = set()
    for case, sites, withE1 in plan:
        if case in done:
            continue
        eqs = case_equations(case, with_E1=withE1)
        print("case %d (E1=%s): %d equations" % (case, withE1, len(eqs)),
              flush=True)
        for t in sites:
            tg = site_minors(t)
            r = forced(eqs, tg, "case%d E1=%s site%d" % (case, withE1, t),
                       timeout=2700)
            res["case%d_E1_%s_site%d" % (case, withE1, t)] = r
            print("   case %d -> site %d factors? %s" % (case, t, r),
                  flush=True)
            if r.get("all_forced"):
                done.add(case)
                break
    res["cases_resolved"] = sorted(done)
    json.dump(res, open(os.path.join(HERE, "results_branchB.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
