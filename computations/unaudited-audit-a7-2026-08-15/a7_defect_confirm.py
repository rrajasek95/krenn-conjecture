#!/usr/bin/env python3
"""A7 -- pin the W19 case-3 defect against the explicit witness.

Evaluates, at the A7 m=25 witness point (all cells nonzero, all 2,624 clean
equations exact, no factoring site, A14[0] constant / A14[1] not):
  * W19's Branch-B *consistency* equations  nu*A03 - mu*A23      (must hold)
  * W19's case-3 hypothesis equations (A14[0] constant, k_x == 0 on the
    x1 = 1 full-S4 boxes)                                         (must hold)
  * W19's E1 and E2 equations for all 81 L-words                  (must hold)
  * W19's sign-flipped extra equations  mu*k_x + A03*g            (MUST FAIL)
  * W19's site-6 minor targets                                    (MUST FAIL)
If the first four hold and the last two fail, the witness is inside the exact
locus W19 claimed to have killed, and the kill came only from the invalid
equations.
"""
from __future__ import annotations
import os, sys, json, itertools
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a7_witness25 as W
from a7_core import EDGES, EIDX
import a7_w19case as C

HERE = os.path.dirname(os.path.abspath(__file__))


def env_from(B, A):
    """map the 42 Branch-B gauge symbols to their values at the witness."""
    e = {}
    for b in range(3):
        for c in range(3):
            e["s%d%d" % (b, c)] = B[(5, 6)][b][c]
    for c in range(3):
        for d in (1, 2):
            e["t%d%d" % (c, d)] = B[(6, 7)][c][d]
    for i in (0, 1):
        for a in (1, 2):
            e["f%d%d" % (i, a)] = B[(1, 4)][i][a]
    for i in (1, 2):
        for b in (1, 2):
            e["g%d%d" % (i, b)] = B[(2, 5)][i][b]
    for d in (1, 2):
        e["h%d" % d] = B[(0, 7)][0][d]
    for i in (1, 2):
        for j in range(3):
            e["p%d%d" % (i, j)] = B[(0, 3)][i][j]
    for i in range(3):
        for j in range(3):
            e["q%d%d" % (i, j)] = B[(2, 3)][i][j]
    e["mu"] = B[(4, 5)][0][0]
    e["nu"] = B[(4, 7)][0][0]
    return e


def ev(expr, env):
    return eval(expr, {"__builtins__": {}}, env)


def gauge_ok(B):
    """the witness must already be in the Branch-B gauge (else the symbolic
    equations do not apply to it verbatim)."""
    ok = {}
    ok["A14_2_ones"] = B[(1, 4)][2] == [Fr(1)] * 3
    ok["A25_0_ones"] = B[(2, 5)][0] == [Fr(1)] * 3
    ok["A07_1_ones"] = B[(0, 7)][1] == [Fr(1)] * 3
    ok["A07_2_ones"] = B[(0, 7)][2] == [Fr(1)] * 3
    ok["A03_0_ones"] = B[(0, 3)][0] == [Fr(1)] * 3
    ok["A14_i0_one"] = all(B[(1, 4)][i][0] == 1 for i in (0, 1))
    ok["A25_i0_one"] = all(B[(2, 5)][i][0] == 1 for i in (1, 2))
    ok["A07_00_one"] = B[(0, 7)][0][0] == 1
    ok["A67_c0_one"] = all(B[(6, 7)][c][0] == 1 for c in range(3))
    ok["A45_const"] = len({v for r in B[(4, 5)] for v in r}) == 1
    ok["A47_const"] = len({v for r in B[(4, 7)] for v in r}) == 1
    return ok


def main():
    A, B = W.build()
    env = env_from(B, A)
    res = {"gauge_checks": {k: bool(v) for k, v in gauge_ok(B).items()}}
    print("gauge:", res["gauge_checks"])

    def tally(name, eqs, expect_zero):
        vals = [ev(e, dict(env)) for e in eqs]
        nz = sum(1 for v in vals if v != 0)
        res[name] = dict(n=len(eqs), n_nonzero=nz,
                         verdict="OK" if ((nz == 0) == expect_zero) else "MISMATCH")
        print("%-38s n=%5d nonvanishing=%5d  expected_all_zero=%s  -> %s"
              % (name, len(eqs), nz, expect_zero, res[name]["verdict"]))
        return nz

    tally("branch_consistency (valid)", C.eqs_branch_correct(), True)
    tally("A14[0] constant (valid)", C.eqs_A14_0_constant(), True)
    tally("case3 k_x==0 at x1=1 (valid)", C.eqs_k_zero(1), True)
    tally("E1 all 81 L-words (valid)", C.eqs_E1(), True)
    tally("E2 all 81 L-words (valid)", C.eqs_E2(), True)
    tally("W19 sign-flipped extras (INVALID)", C.eqs_branch_W19_signflip(),
          False)
    tally("site-6 minors (target)", C.site_minor_targets(6), False)
    tally("site-4 minors (target)", C.site_minor_targets(4), False)
    tally("site-5 minors (target)", C.site_minor_targets(5), False)
    tally("site-7 minors (target)", C.site_minor_targets(7), False)
    json.dump(res, open(os.path.join(HERE, "results_defect_confirm.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
