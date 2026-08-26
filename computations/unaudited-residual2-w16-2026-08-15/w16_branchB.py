#!/usr/bin/env python3
"""W16 -- m = 25: BRANCH B (the surviving branch after the vertex-6 dichotomy).

THE m=25 STRUCTURE (Theorem W16-1, R-side; verified exactly in w16_struct):

  Phi(x,y) = D_x[y4][y5] A67[y6][y7] + E_x[y4][y7] A56[y5][y6]      (identity)
  D_x = P_L(x) A45 + A03[x0][x3] * A14[x1][.] (x) A25[x2][.]
  E_x = P_L(x) A47 + A23[x2][x3] * A14[x1][.] (x) A07[x0][.]

STEP A (the dichotomy, proved by hand, re-verified here).  For x in X_free
(the four L-words clean against EVERY R-word) all 81 y are clean, so the
2-term identity holds on the full 3^4 box.  Freezing (b,c) gives
A56[b][c] E_x = -D_x[.][b] (x) A67[c][.] and A56[b][c] != 0, so rank E_x <= 1;
freezing (c,d) gives rank D_x <= 1.  If E_x != 0 the independence of the
freeze point forces rank A56 = rank A67 = 1 with PARALLEL 6-vectors, i.e.
VERTEX 6 FACTORS -> kill (mechanism W16-B).  Otherwise D_x = E_x = 0.

BRANCH B is  D_x = E_x = 0 for all x in X_free, i.e.
  A45 = mu * v (x) m,  A47 = nu * v (x) u,  v = A14[2][.], m = A25[0][.],
  u = A07[1][.],  and A07[2][.] parallel to u.

GAUGE (diagonal rescaling e_c^{(t)} -> lam_{t,c} e_c^{(t)}; preserves the
template, multiplies H_w by prod_t lam_{t,w_t} != 0, so WLOG):
  vertex 4 -> A14[2][.] = (1,1,1)      vertex 5 -> A25[0][.] = (1,1,1)
  vertex 7 -> A07[1][.] = (1,1,1)      vertex 0 -> A07[0][0] = A07[2][0] = 1
  vertex 1 -> A14[0][0] = A14[1][0] = 1
  vertex 2 -> A25[1][0] = A25[2][0] = 1
  vertex 6 -> A67[c][0] = 1 for c = 0,1,2
  vertex 3 -> A03[0][.] = (1,1,1)
Then A45 = mu*J, A47 = nu*J, A07[2][.] = (1,1,1), and

  Phi(x,y) = lam_x * g(b,c,d) + F_a * k_x(b,c,d)
  g(b,c,d)  = mu*A67[c][d] + nu*A56[b][c]
  k_x(b,c,d)= A03[x0][x3]*A25[x2][b]*A67[c][d] + A23[x2][x3]*A07[x0][d]*A56[b][c]
  F = A14[x1][.],  lam_x = P_L(x)  (treated as a FREE variable -- a sound
                                    relaxation: fewer constraints)
with (a,b,c,d) = (y4,y5,y6,y7).  VERTEX 4 FACTORS iff A14[0][.] and A14[1][.]
are constant vectors (in this gauge), which is again a kill.
"""
from __future__ import annotations
import os, sys, json, itertools, time
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w16_core import W8_IMMUNE, full_pm_indices, extras_at
from w16_sing import run_singular, SingularError, check_no_shadowing

HERE = os.path.dirname(os.path.abspath(__file__))
T25 = W8_IMMUNE[25]
FULLM25 = full_pm_indices(T25)

# ---- clean R-alphabets S4,S5,S6,S7 as a function of the L-word x ----------
# single cells of the family (identical for m=24..28), as (edge, cell):
#  04:(0,0) 05:(0,1) 06:(0,2) 15:(1,0) 16:(1,1) 17:(0,2)
#  24:(1,0) 26:(2,1) 27:(1,2) 34:(2,0) 35:(2,1) 37:(2,2)


def S_sets(x):
    x0, x1, x2, x3 = x
    a = (x0 == 0) or (x2 == 1) or (x3 == 2)          # blocks y4 = 0
    b = (x1 == 1)                                     # blocks y5 = 0
    c = (x0 == 0) or (x3 == 2)                        # blocks y5 = 1
    d = (x1 == 1) or (x2 == 2)                        # blocks y6 = 1
    e = (x0 == 0)                                     # blocks y6 = 2
    f = (x1 == 0) or (x2 == 1) or (x3 == 2)           # blocks y7 = 2
    S4 = [t for t in range(3) if not (t == 0 and a)]
    S5 = [t for t in range(3) if not ((t == 0 and b) or (t == 1 and c))]
    S6 = [t for t in range(3) if not ((t == 1 and d) or (t == 2 and e))]
    S7 = [t for t in range(3) if not (t == 2 and f)]
    return S4, S5, S6, S7


def check_S_sets():
    """control: S_sets must reproduce the exact word-clean predicate."""
    from w16_core import singles, word_clean
    act = singles(T25)
    bad = 0
    for x in itertools.product(range(3), repeat=4):
        S4, S5, S6, S7 = S_sets(x)
        for y in itertools.product(range(3), repeat=4):
            pred = (y[0] in S4 and y[1] in S5 and y[2] in S6 and y[3] in S7)
            if pred != word_clean(T25, tuple(x) + tuple(y), act):
                bad += 1
    return bad


# ------------------------------------------------------------- the ring ----
NAMES = []


def V(n):
    if n not in NAMES:
        NAMES.append(n)
    return n


A56 = [[V("s%d%d" % (i, j)) for j in range(3)] for i in range(3)]
A67 = [[("1" if j == 0 else V("t%d%d" % (i, j))) for j in range(3)]
       for i in range(3)]
A14 = [["1" if j == 0 else V("f%d%d" % (i, j)) for j in range(3)]
       for i in range(2)] + [["1", "1", "1"]]
A25 = [["1", "1", "1"]] + [["1" if j == 0 else V("g%d%d" % (i, j))
                            for j in range(3)] for i in (1, 2)]
A07 = [["1" if j == 0 else V("h%d" % j) for j in range(3)],
       ["1", "1", "1"], ["1", "1", "1"]]
A03 = [["1", "1", "1"]] + [[V("p%d%d" % (i, j)) for j in range(3)]
                           for i in (1, 2)]
A23 = [[V("q%d%d" % (i, j)) for j in range(3)] for i in range(3)]
MU, NU = V("mu"), V("nu")


def lam(x):
    return V("L%d%d%d%d" % x)


def g_expr(b, c, d):
    return "(%s*%s+%s*%s)" % (MU, A67[c][d], NU, A56[b][c])


def k_expr(x, b, c, d):
    x0, x1, x2, x3 = x
    return "(%s*%s*%s+%s*%s*%s)" % (A03[x0][x3], A25[x2][b], A67[c][d],
                                    A23[x2][x3], A07[x0][d], A56[b][c])


def phi_expr(x, y):
    a, b, c, d = y
    return "(%s*%s+%s*%s)" % (lam(x), g_expr(b, c, d), A14[x[1]][a],
                              k_expr(x, b, c, d))


def branchB_eqs(X):
    """clean equations for the chosen L-words + the Branch-B equations."""
    eqs = []
    for x in X:
        S4, S5, S6, S7 = S_sets(x)
        for a in S4:
            for b in S5:
                for c in S6:
                    for d in S7:
                        eqs.append(phi_expr(x, (a, b, c, d)))
    # Branch B: D_x = E_x = 0 on X_free   (x = (x0,2,0,x3))
    for x0 in (1, 2):
        for x3 in (0, 1):
            x = (x0, 2, 0, x3)
            eqs.append("(%s*%s+%s)" % (lam(x), MU, A03[x0][x3]))   # D_x = 0
            eqs.append("(%s*%s+%s)" % (lam(x), NU, A23[0][x3]))    # E_x = 0
    return eqs


NONZERO = None


def nonzero_list():
    out = [MU, NU]
    for M in (A56, A67, A14, A25, A07, A03, A23):
        for row in M:
            for e in row:
                if e != "1":
                    out.append(e)
    return sorted(set(out))


def run(X, target, mode="sat", timeout=3600, extra_eqs=(), tag=""):
    eqs = branchB_eqs(X) + list(extra_eqs)
    used = sorted(set(NAMES))
    nz = nonzero_list()
    check_no_shadowing(used, ["zzg%d" % i for i in range(1, len(eqs) + 1)]
                       + ["Iid", "PP", "Jid", "LL", "SS", "GS", "tt", "uu"])
    ll = ['LIB "elim.lib";',
          "ring r = 0,(%s),dp;" % ",".join(used)]
    for i, e in enumerate(eqs, 1):
        ll.append("poly zzg%d = %s;" % (i, e))
    ll.append("poly tt = %s;" % target)
    ll.append("ideal Iid = %s;" % ",".join("zzg%d" % i
                                           for i in range(1, len(eqs) + 1)))
    ll.append("poly PP = %s;" % "*".join(nz))
    if mode == "sat":
        ll.append("ideal Jid = PP;")
        ll.append("list LL = sat(Iid,Jid);")
        ll.append("ideal SS = LL[1];")
        ll.append("ideal GS = groebner(SS);")
        ll.append('"FORCED:"; (reduce(tt,GS)==0);')
        ll.append('"UNIT:"; (GS[1]==1);')
    else:
        ll.append("ideal Rab = Iid, uu*PP*tt-1;")
        ll.append('"EMPTY:"; (groebner(Rab)[1]==1);')
    ll.append("quit;")
    t0 = time.time()
    out, st = run_singular("\n".join(ll) + "\n", timeout=timeout)
    dt = time.time() - t0
    if st == "TIMEOUT":
        return dict(tag=tag, verdict=None, secs=round(dt, 1),
                    n_eqs=len(eqs), n_vars=len(used))
    res = dict(tag=tag, n_eqs=len(eqs), n_vars=len(used), secs=round(dt, 1))
    if mode == "sat":
        res["forced"] = out.split("FORCED:")[1].strip().split()[0] == "1"
        res["clean_layer_unit_ideal"] = \
            out.split("UNIT:")[1].strip().split()[0] == "1"
    return res


def main():
    print("CONTROL: S_sets vs exact word-clean predicate, mismatches =",
          check_S_sets())
    # the 81 L-words, ordered so the informative ones come first
    order = []
    for x1 in (2, 0, 1):
        for x2 in (0, 2, 1):
            for x0 in (1, 2, 0):
                for x3 in (0, 1, 2):
                    order.append((x0, x1, x2, x3))
    res = {}
    for nX in (8, 12, 16, 24, 36, 54, 81):
        X = order[:nX]
        NAMES.clear()
        for x in X:
            lam(x)
        # rebuild name table by touching every symbol
        _ = branchB_eqs(X)
        # target: the 2x2 minors of A14 (vertex 4 factorisation defect)
        tgt = "(%s-1)" % A14[0][1]
        r = run(X, tgt, timeout=1200, tag="A14[0][1]==1 with |X|=%d" % nX)
        print(r)
        res[nX] = r
        if r.get("forced") or r.get("clean_layer_unit_ideal"):
            break
    json.dump(res, open(os.path.join(HERE, "results_branchB.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
