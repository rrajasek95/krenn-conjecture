#!/usr/bin/env python3
"""A7 -- TARGET 1(b): independent audit of W19's three-case Branch-B kill at m=25.

Everything below is re-derived from scratch (my own gauge check, my own
equations, my own Singular driver with the ledger-13 guard).

THE MODEL (Branch-B gauge; gauge legitimacy argued in REPORT.md).  42 free
block variables:
    A56[b][c] = s{b}{c}                      (9)
    A67[c][d] = 1 (d=0) else t{c}{d}         (6)
    A14[i][a] = 1 (a=0) else f{i}{a}, i=0,1;  A14[2] = (1,1,1)      (4)
    A25[i][b] = 1 (b=0) else g{i}{b}, i=1,2;  A25[0] = (1,1,1)      (4)
    A07[0][d] = 1 (d=0) else h{d};            A07[1] = A07[2] = (1,1,1) (2)
    A03[i][j] = p{i}{j}, i=1,2;               A03[0] = (1,1,1)      (6)
    A23[i][j] = q{i}{j}                                             (9)
    mu (=A45 entries), nu (=A47 entries)                            (2)
and one FREE scalar lam_x per L-word (the relaxation of P_L(x); sound: it
only drops constraints, so any FORCING verdict transfers to the true system).

CLEAN EQUATIONS.  Phi(x,y) = lam_x*g(b,c,d) + A14[x1][a]*k_x(b,c,d), with
  g   = mu*A67[c][d] + nu*A56[b][c]
  k_x = A03[x0][x3]*A25[x2][b]*A67[c][d] + A23[x2][x3]*A07[x0][d]*A56[b][c]
(re-derived here from the two-term identity; verified numerically).

ELIMINATION OF lam_x.  The clean equations say the vector (lam_x, 1) is in
the kernel of the matrix with rows (G_i, F_a K_i) over a in S4, i in B_x.
Hence ALL 2x2 minors vanish:
  (E1) G_i K_j - G_j K_i = 0,     (E2) (F_a - F_a') K_i = 0,
and the general minor G_i F_a' K_j - G_j F_a K_i is a combination of these,
so {E1, E2} is the COMPLETE elimination.  Both are consequences of the clean
equations -- sound for forcing.

*** DEFECT FOUND IN W19 ***  w19_branchB.base_eqs() appends, for x in XFREE,
the polynomial   mu*k_x + A03[x0][x3]*g   as an equation.  The correct
consequence of Branch B is  mu*k_x - A03[x0][x3]*g = (mu*A23[0][x3] -
nu*A03[x0][x3])*A56[b][c], which vanishes by the (valid) branch equation.
With the wrong sign, and using that same valid branch equation,
    mu*k_x + A03*g = 2*A03*g,
so the emitted equation forces g == 0 on the whole XFREE box after
saturation by the cells -- and g == 0 by itself already implies A67 = J and
A56 constant, i.e. SITE 6 FACTORS.  Every run that includes base_eqs()
therefore proves its conclusion from a false hypothesis.  Case 3 -- the only
case W19 could not settle without base_eqs() -- is exactly such a run.
"""
from __future__ import annotations
import os, sys, json, itertools
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a7_core import W8_IMMUNE, F_gamma, k_of, PM_E, cell_index, EDGES, EIDX
from a7_sing import guard, run as sing_run, SingularError

HERE = os.path.dirname(os.path.abspath(__file__))
T25 = W8_IMMUNE[25]
FG25 = F_gamma(T25)

# ------------------------------------------------------------- symbols ----
A56 = [["s%d%d" % (b, c) for c in range(3)] for b in range(3)]
A67 = [["1" if d == 0 else "t%d%d" % (c, d) for d in range(3)]
       for c in range(3)]
A14 = [["1" if a == 0 else "f%d%d" % (i, a) for a in range(3)] for i in (0, 1)] \
      + [["1", "1", "1"]]
A25 = [["1", "1", "1"]] + [["1" if b == 0 else "g%d%d" % (i, b)
                            for b in range(3)] for i in (1, 2)]
A07 = [["1" if d == 0 else "h%d" % d for d in range(3)],
       ["1", "1", "1"], ["1", "1", "1"]]
A03 = [["1", "1", "1"]] + [["p%d%d" % (i, j) for j in range(3)] for i in (1, 2)]
A23 = [["q%d%d" % (i, j) for j in range(3)] for i in range(3)]
MU, NU = "mu", "nu"
VARS = sorted({v for M in (A56, A67, A14, A25, A07, A03, A23) for r in M
               for v in r if v != "1"} | {MU, NU})
assert len(VARS) == 42, len(VARS)


def BOX(x):
    ys = [y for y in itertools.product(range(3), repeat=4)
          if k_of(T25, tuple(x) + tuple(y), FG25) == 0]
    if not ys:
        return [[], [], [], []]
    return [sorted({y[k] for y in ys}) for k in range(4)]


BOXES = {x: BOX(x) for x in itertools.product(range(3), repeat=4)}


def g_e(b, c, d):
    return "(%s*%s+%s*%s)" % (MU, A67[c][d], NU, A56[b][c])


def k_e(x, b, c, d):
    return "(%s*%s*%s+%s*%s*%s)" % (A03[x[0]][x[3]], A25[x[2]][b], A67[c][d],
                                    A23[x[2]][x[3]], A07[x[0]][d], A56[b][c])


# ------------------------------------------------------- equation blocks --
def eqs_E1(Xs=None):
    out = []
    Xs = Xs or list(BOXES)
    for x in Xs:
        S4, S5, S6, S7 = BOXES[x]
        if not S4:
            continue
        B = [(b, c, d) for b in S5 for c in S6 for d in S7]
        for i in range(len(B)):
            for j in range(i + 1, len(B)):
                out.append("%s*%s-%s*%s" % (g_e(*B[i]), k_e(x, *B[j]),
                                            g_e(*B[j]), k_e(x, *B[i])))
    return out


def eqs_E2(Xs=None):
    out = []
    Xs = Xs or list(BOXES)
    for x in Xs:
        S4, S5, S6, S7 = BOXES[x]
        B = [(b, c, d) for b in S5 for c in S6 for d in S7]
        for ai in range(len(S4)):
            for aj in range(ai + 1, len(S4)):
                fa, fb = A14[x[1]][S4[ai]], A14[x[1]][S4[aj]]
                if fa == fb:
                    continue
                for i in B:
                    out.append("(%s-%s)*%s" % (fa, fb, k_e(x, *i)))
    return out


XFREE_WC = [(x0, 2, 0, x3) for x0 in (1, 2) for x3 in (0, 1)]
XFREE_EC = [(x0, x1, 0, x3) for x0 in (1, 2) for x1 in (0, 2) for x3 in (0, 1)]


def eqs_branch_correct():
    """Branch B, derived honestly.
    From D_x = 0 at the word-clean X_free (x1=2): lam_x*mu = -A03[x0][x3].
    From E_x = 0 there:                            lam_x*nu = -A23[0][x3].
    => nu*A03[x0][x3] - mu*A23[0][x3] = 0.
    From the EXTRA effectively-clean X_free words (x1=0, all 81 y clean):
      lam*mu + A03[x0][x3]*A14[0][a] = 0 for every a => A14[0][.] constant."""
    out = []
    for x0 in (1, 2):
        for x3 in (0, 1):
            out.append("%s*%s-%s*%s" % (NU, A03[x0][x3], MU, A23[0][x3]))
    return out


def eqs_A14_0_constant():
    return ["%s-1" % A14[0][a] for a in (1, 2)]


def eqs_branch_W19_signflip():
    """EXACTLY the extra equations w19_branchB.base_eqs() appends (the ones
    with the sign error), reproduced here so the defect can be demonstrated."""
    out = []
    for x in XFREE_WC:
        S4, S5, S6, S7 = BOXES[x]
        for b in S5:
            for c in S6:
                for d in S7:
                    out.append("%s*%s+%s*%s" % (MU, k_e(x, b, c, d),
                                                A03[x[0]][x[3]], g_e(b, c, d)))
    return out


def eqs_k_zero(x1):
    """(E2) consequence at the L-words with x1 and a FULL site-4 alphabet,
    valid exactly when A14[x1][.] is NOT constant."""
    out = []
    for x in BOXES:
        if x[1] != x1 or BOXES[x][0] != [0, 1, 2]:
            continue
        _, S5, S6, S7 = BOXES[x]
        for b in S5:
            for c in S6:
                for d in S7:
                    out.append(k_e(x, b, c, d))
    return out


# ------------------------------------------------------------- targets ----
def site_minor_targets(t):
    """columns = the site-t vectors of every Gamma block at t."""
    if t == 4:
        cols = [[A14[i][a] for a in range(3)] for i in range(3)] + \
               [["1", "1", "1"]]
    elif t == 5:
        cols = [[A25[i][b] for b in range(3)] for i in range(3)] + \
               [["1", "1", "1"]] + \
               [[A56[b][c] for b in range(3)] for c in range(3)]
    elif t == 6:
        cols = [[A56[b][c] for c in range(3)] for b in range(3)] + \
               [[A67[c][d] for c in range(3)] for d in range(3)]
    elif t == 7:
        cols = [[A07[i][d] for d in range(3)] for i in range(3)] + \
               [["1", "1", "1"]] + \
               [[A67[c][d] for d in range(3)] for c in range(3)]
    else:
        raise ValueError(t)
    out = []
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            for a in range(3):
                for b in range(a + 1, 3):
                    if (cols[i][a], cols[j][b]) == (cols[i][b], cols[j][a]):
                        continue
                    out.append("%s*%s-%s*%s" % (cols[i][a], cols[j][b],
                                                cols[i][b], cols[j][a]))
    return sorted(set(out))


# ------------------------------------------------------------- Singular ---
def forcing(eqs, targets, tag, timeout=3600):
    gens = ["zzg%d" % i for i in range(1, len(eqs) + 1)]
    aux = ["zzI", "zzJ", "zzL", "zzS", "zzGB", "zzP", "zznbad"]
    guard(VARS, gens + aux)
    ll = ['LIB "elim.lib";', "ring zzr = 0,(%s),dp;" % ",".join(VARS)]
    for i, e in enumerate(eqs, 1):
        ll.append("poly zzg%d = %s;" % (i, e))
    ll.append("ideal zzI = %s;" % ",".join(gens))
    ll.append("poly zzP = %s;" % "*".join(VARS))
    ll.append("ideal zzJ = zzP;")
    ll.append("list zzL = sat(zzI,zzJ);")
    ll.append("ideal zzS = zzL[1];")
    ll.append("ideal zzGB = groebner(zzS);")
    ll.append("int zznbad = 0;")
    for tg in targets:
        ll.append("if (reduce(%s,zzGB) != 0) { zznbad = zznbad + 1; }" % tg)
    ll.append('"NBAD:"; zznbad;')
    ll.append('"UNIT:"; (zzGB[1]==1);')
    ll.append("quit;")
    out, st, dt = sing_run("\n".join(ll) + "\n", timeout=timeout)
    if st == "TIMEOUT":
        return dict(tag=tag, verdict=None, secs=timeout, n_eqs=len(eqs),
                    n_targets=len(targets))
    nbad = int(out.split("NBAD:")[1].strip().split()[0])
    return dict(tag=tag, n_eqs=len(eqs), n_targets=len(targets),
                n_not_forced=nbad, all_forced=(nbad == 0),
                unit_ideal=(out.split("UNIT:")[1].strip().split()[0] == "1"),
                secs=round(dt, 1))


def main():
    res = {}
    print("VARS (%d): %s" % (len(VARS), " ".join(VARS)), flush=True)

    # --- 0. demonstrate the sign defect symbolically ---------------------
    import sympy
    syms = {v: sympy.Symbol(v) for v in VARS}

    def ev(expr):
        return sympy.sympify(expr, locals=syms)
    x = XFREE_WC[0]
    b, c, d = 1, 2, 1
    kk, gg = ev(k_e(x, b, c, d)), ev(g_e(b, c, d))
    branch = ev("%s*%s-%s*%s" % (NU, A03[x[0]][x[3]], MU, A23[0][x3_ := x[3]]))
    good = sympy.expand(syms[MU] * kk - ev(A03[x[0]][x[3]]) * gg)
    badv = sympy.expand(syms[MU] * kk + ev(A03[x[0]][x[3]]) * gg)
    # reduce modulo the branch relation nu*A03 = mu*A23  (substitute q0x3)
    sub = {syms[A23[0][x[3]]]: syms[NU] * ev(A03[x[0]][x[3]]) / syms[MU]}
    good_r = sympy.simplify(good.subs(sub))
    bad_r = sympy.simplify(badv.subs(sub) - 2 * ev(A03[x[0]][x[3]]) * gg)
    res["defect_symbolic"] = dict(
        good_reduces_to_zero=bool(good_r == 0),
        bad_equals_2_A03_g=bool(bad_r == 0),
        good=str(good), bad=str(badv))
    print("DEFECT: (mu*k - A03*g) mod branch == 0 :", res["defect_symbolic"]
          ["good_reduces_to_zero"])
    print("DEFECT: (mu*k + A03*g) mod branch == 2*A03*g :",
          res["defect_symbolic"]["bad_equals_2_A03_g"], flush=True)

    # --- 1. the sign-flipped equations ALONE force site 6 to factor ------
    r = forcing(eqs_branch_correct() + eqs_branch_W19_signflip(),
                site_minor_targets(6), "signflip-alone -> site6", timeout=1800)
    res["signflip_alone_forces_site6"] = r
    print("W19's sign-flipped equations ALONE:", r, flush=True)

    # --- 2. the honest case analysis -------------------------------------
    honest_base = eqs_branch_correct() + eqs_A14_0_constant()
    # case A: A14[1] constant -> site 4 factors (definitional)
    rA = forcing(honest_base + ["%s-1" % A14[1][a] for a in (1, 2)],
                 site_minor_targets(4), "caseA site4", timeout=900)
    res["caseA_A14_1_constant_site4"] = rA
    print("case A (A14[1] constant) -> site 4:", rA, flush=True)
    # case B: A14[1] NOT constant -> k_x == 0 on the x1=1 full-S4 boxes
    caseB = honest_base + eqs_k_zero(1)
    for t in (6, 5, 4, 7):
        r = forcing(caseB, site_minor_targets(t), "caseB(no E1) site%d" % t,
                    timeout=900)
        res["caseB_noE1_site%d" % t] = r
        print("case B (no E1) -> site %d:" % t, r, flush=True)
    # case B with the FULL valid E1+E2 system
    caseB_full = caseB + eqs_E1() + eqs_E2()
    print("case B full system: %d equations" % len(caseB_full), flush=True)
    for t in (6, 4, 5, 7):
        r = forcing(caseB_full, site_minor_targets(t),
                    "caseB(E1+E2) site%d" % t, timeout=5400)
        res["caseB_E1E2_site%d" % t] = r
        print("case B (E1+E2) -> site %d:" % t, r, flush=True)
        if r.get("all_forced"):
            break
    json.dump(res, open(os.path.join(HERE, "results_w19case.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
