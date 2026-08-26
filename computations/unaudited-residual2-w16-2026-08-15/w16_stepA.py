#!/usr/bin/env python3
"""W16 -- Step A (the vertex-6 dichotomy) + Branch-B mutation controls.

STEP A, as an exact ideal statement.  Let D, E, A56, A67 be 3x3 matrices and

    D[a][b] A67[c][d] + E[a][d] A56[b][c] = 0   for all a,b,c,d in {0,1,2}.

Let M6 be the 3x6 matrix whose row c is
    ( A56[0][c], A56[1][c], A56[2][c], A67[c][0], A67[c][1], A67[c][2] ),
so "VERTEX 6 FACTORS" (A56 = beta (x) gamma, A67 = gamma (x) k with the SAME
gamma up to scale) is exactly rank M6 <= 1.  CLAIM (Step A):

    every 2x2 minor of M6, times every entry of D and of E, lies in
    sat( ideal(the 81 equations), product of the 18 cells of A56, A67 ).

i.e. modulo cells-nonzero:  (D = E = 0)  OR  (vertex 6 factors).

MUTATION CONTROLS included for both this and the Branch-B computation.
"""
from __future__ import annotations
import os, sys, json, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w16_sing import run_singular

HERE = os.path.dirname(os.path.abspath(__file__))

S = [["s%d%d" % (i, j) for j in range(3)] for i in range(3)]     # A56
Tt = [["t%d%d" % (i, j) for j in range(3)] for i in range(3)]    # A67
D = [["d%d%d" % (i, j) for j in range(3)] for i in range(3)]
E = [["e%d%d" % (i, j) for j in range(3)] for i in range(3)]
ALL = [v for M in (S, Tt, D, E) for row in M for v in row]
CELLS = [v for M in (S, Tt) for row in M for v in row]


def eqs_stepA(mutate=None):
    out = []
    for a, b, c, d in itertools.product(range(3), repeat=4):
        if mutate == "drop_abcd" and (a, b, c, d) == (0, 0, 0, 0):
            continue
        coef = "2*" if (mutate == "coef" and (a, b, c, d) == (1, 1, 1, 1)) else ""
        out.append("%s*%s+%s%s*%s" % (D[a][b], Tt[c][d], coef, E[a][d],
                                      S[b][c]))
    return out


def M6_minors():
    rows = [[S[0][c], S[1][c], S[2][c], Tt[c][0], Tt[c][1], Tt[c][2]]
            for c in range(3)]
    out = []
    for c1, c2 in itertools.combinations(range(3), 2):
        for j1, j2 in itertools.combinations(range(6), 2):
            out.append("%s*%s-%s*%s" % (rows[c1][j1], rows[c2][j2],
                                        rows[c1][j2], rows[c2][j1]))
    return out


def run_stepA(mutate=None, timeout=1800):
    eqs = eqs_stepA(mutate)
    minors = M6_minors()
    tgts = ["(%s)*(%s)" % (mu, v) for mu in minors
            for v in [D[0][0], D[1][2], E[0][0], E[2][1]]]
    ll = ['LIB "elim.lib";', "ring r = 0,(%s),dp;" % ",".join(ALL)]
    for i, e in enumerate(eqs, 1):
        ll.append("poly g%d = %s;" % (i, e))
    ll.append("ideal Iid = %s;" % ",".join("g%d" % i
                                           for i in range(1, len(eqs) + 1)))
    ll.append("poly PP = %s;" % "*".join(CELLS))
    ll.append("ideal Jid = PP;")
    ll.append("list LL = sat(Iid,Jid);")
    ll.append("ideal GS = groebner(LL[1]);")
    ll.append("int bad = 0;")
    for i, t in enumerate(tgts, 1):
        ll.append("if (reduce(%s,GS) != 0) { bad = bad + 1; }" % t)
    ll.append('"NBAD:"; bad;')
    ll.append('"NTGT:"; %d;' % len(tgts))
    ll.append("quit;")
    t0 = time.time()
    out, st = run_singular("\n".join(ll) + "\n", timeout=timeout)
    if st == "TIMEOUT":
        return dict(verdict=None, secs=timeout)
    nbad = int(out.split("NBAD:")[1].strip().split()[0])
    return dict(n_targets=len(tgts), n_not_forced=nbad,
                step_A_holds=(nbad == 0), secs=round(time.time() - t0, 1))


def main():
    res = {}
    res["stepA"] = run_stepA()
    print("Step A:", res["stepA"])
    for mut in ("coef", "drop_abcd"):
        res["mutation_" + mut] = run_stepA(mutate=mut)
        print("  mutation %-10s ->" % mut, res["mutation_" + mut],
              "(step_A_holds must be False)")
    json.dump(res, open(os.path.join(HERE, "results_stepA.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
