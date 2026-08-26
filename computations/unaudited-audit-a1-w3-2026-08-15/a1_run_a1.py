"""AUDIT A1 / CLAIM 2 driver: Theorem A.1 dichotomy, exactly."""

from __future__ import annotations

import random
import sys
from fractions import Fraction

from a1_core import COLS, all_cells, all_words, cellkey, nodes_of, phi
from a1_dichotomy import (
    build_D,
    build_P,
    classify,
    decide_D,
    decide_P,
    kempf_ness,
    random_support,
    verify_D,
    verify_P,
)
from a1_lp import solve

# ------------------------------------------------------------ 0. LP self-test


def lp_selftest():
    bad = 0
    # min -x1 - x2 st x1 + x2 + s = 1  -> optimum -1
    st, x, obj = solve([[1, 1, 1]], [1], [-1, -1, 0])
    if not (st == "optimal" and obj == -1):
        bad += 1
    # infeasible: x >= 0, x1 + x2 = -1  (after sign flip: -x1-x2 = 1)
    st, x, obj = solve([[1, 1]], [-1], [0, 0])
    if st != "infeasible":
        bad += 1
    # unbounded: min -x1 st x1 - x2 = 0
    st, x, obj = solve([[1, -1]], [0], [-1, 0])
    if st != "unbounded":
        bad += 1
    # exact rational optimum
    st, x, obj = solve([[3, 2, 1, 0], [1, 4, 0, 1]], [7, 5], [-2, -3, 0, 0])
    if st != "optimal" or obj != Fraction(-6):
        bad += 1
    return bad


# ---------------------------------------------- 1. exclusivity of D and P


def test_dichotomy(n, trials, seed, density):
    rng = random.Random(seed)
    tally = {}
    probs = []
    for _ in range(trials):
        S = random_support(n, rng, density)
        if not S:
            continue
        tag, cert = classify(n, S)
        tally[tag] = tally.get(tag, 0) + 1
        if tag in ("BOTH", "NEITHER") or tag.endswith("BAD"):
            probs.append((sorted(S), tag))
    return tally, probs


# ------------------------------------- 2. (D) really preserves every value


def test_D_preserves(n, trials, seed, density):
    rng = random.Random(seed)
    checked = bad = 0
    for _ in range(trials):
        S = random_support(n, rng, density)
        if not S:
            continue
        ok, w = decide_D(n, S)
        if not ok:
            continue
        good, _ = verify_D(n, S, w)
        if not good:
            bad += 1
            continue
        a = {s: Fraction(rng.randint(-9, 9), rng.randint(1, 6)) for s in S}
        for s in list(a):
            if a[s] == 0:
                a[s] = Fraction(1)
        S0 = {s for s in S if w[nodes_of(s)[0]] + w[nodes_of(s)[1]] == 0}
        ares = {s: a[s] for s in S0}
        for word in all_words(n):
            mc = sum(w[(v, word[v])] for v in range(n))
            full = phi(a, word, n, Fraction(0), Fraction(1))
            res = phi(ares, word, n, Fraction(0), Fraction(1))
            checked += 1
            if mc == 0 and res != full:
                bad += 1
            if mc > 0 and res != 0:
                bad += 1
            if mc < 0 and full != 0:
                bad += 1
    return bad, checked


# ------------------------------------------------- 3. the count "21 at n=8"


def rank_exact(rows):
    rows = [list(map(Fraction, r)) for r in rows]
    m = len(rows)
    ncol = len(rows[0]) if m else 0
    r = 0
    for c in range(ncol):
        piv = None
        for i in range(r, m):
            if rows[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        pv = rows[r][c]
        rows[r] = [x / pv for x in rows[r]]
        for i in range(m):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
    return r


def count_conditions(n):
    nodes = [(v, c) for v in range(n) for c in COLS]
    nid = {x: i for i, x in enumerate(nodes)}
    # U = {w : sum_v w_{v,c} = 0}: rank of the 3 constraints
    cons = []
    for c in COLS:
        row = [0] * len(nodes)
        for v in range(n):
            row[nid[(v, c)]] = 1
        cons.append(row)
    rk = rank_exact(cons)
    dimU = len(nodes) - rk
    # balance conditions: load(v,c) - load(0,c) = 0 for v >= 1, all c
    bal = []
    for c in COLS:
        for v in range(1, n):
            row = [0] * len(nodes)
            row[nid[(v, c)]] = 1
            row[nid[(0, c)]] = -1
            bal.append(row)
    return dimU, rank_exact(bal), len(nodes)


# --------------------------------------------------------- mutation controls


def mutant_bad_D_cert(n, S):
    """A w that is admissible but NOT pure-neutral -- verify_D must reject."""
    w = {(v, c): Fraction(1) for v in range(n) for c in COLS}
    return verify_D(n, S, w)


def mutant_bad_P_cert(n, S):
    """y with a zero entry -- verify_P must reject."""
    Sl = sorted(S)
    y = {s: Fraction(1) for s in Sl}
    y[Sl[0]] = Fraction(0)
    L = {}
    return verify_P(n, S, (y, [Fraction(0)] * 3))


def mutant_D_no_pure_constraint(n, S):
    """Drop the three pure-neutrality rows from (D): the alternative must
    then STOP being exclusive (an all-ones w is admissible on every S)."""
    rows, rhs, Sl, nodes = build_D(n, S)
    rows2 = rows[: len(Sl)] + rows[len(Sl) + 3:]
    rhs2 = rhs[: len(Sl)] + rhs[len(Sl) + 3:]
    from a1_lp import feasible

    ok, _ = feasible(rows2, rhs2)
    return ok


if __name__ == "__main__":
    print("AUDIT A1 / claim 2 (Theorem A.1) -- independent exact checkers")
    print("=" * 72)
    print(f"[0] exact simplex self-test failures: {lp_selftest()}")

    dimU, rkbal, nn = count_conditions(8)
    print(f"[3] n=8: #nodes={nn}  dim U = 3n-3 = {dimU}  "
          f"rank(balance conditions) = {rkbal}   (W3 claims 21)")
    dimU6, rkbal6, nn6 = count_conditions(6)
    print(f"    n=6: #nodes={nn6}  dim U = {dimU6}  rank(balance) = {rkbal6}")

    for n, dens, tr in ((6, 0.10, 40), (6, 0.25, 25), (8, 0.05, 12)):
        tally, probs = test_dichotomy(n, tr, seed=100 + n, density=dens)
        print(f"[1] n={n} density={dens}: {tally}")
        for p in probs[:3]:
            print("    PROBLEM:", p)

    b, c = test_D_preserves(6, trials=12, seed=7, density=0.15)
    print(f"[2] (D) preserves every equation value  n=6: bad={b} / {c} checks")
    b, c = test_D_preserves(8, trials=3, seed=8, density=0.05)
    print(f"[2] (D) preserves every equation value  n=8: bad={b} / {c} checks")

    print()
    print("MUTATION CONTROLS")
    rng = random.Random(5)
    S = random_support(6, rng, 0.2)
    ok, msg = mutant_bad_D_cert(6, S)
    print(f"  bogus (D) cert (not pure-neutral): accepted={ok}  ({msg}) -> "
          + ("*** SURVIVED ***" if ok else "KILLED"))
    ok, msg = mutant_bad_P_cert(6, S)
    print(f"  bogus (P) cert (zero weight):      accepted={ok}  ({msg}) -> "
          + ("*** SURVIVED ***" if ok else "KILLED"))
    n_both = 0
    for _ in range(10):
        S = random_support(6, rng, 0.2)
        if mutant_D_no_pure_constraint(6, S) and decide_P(6, S)[0]:
            n_both += 1
    print(f"  (D) without pure-neutrality: supports where BOTH now hold: "
          f"{n_both}/10 -> " + ("KILLED" if n_both else "*** SURVIVED ***"))
