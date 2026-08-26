"""AUDIT A1 / CLAIM 1: W3's CRUX LEMMA L1.

W3's L1: "for GAUGE weights, every matching of a fixed word has the same
weight (a PM covers each vertex once) -- so gauge-initial systems are plain
support restrictions."

INDEPENDENT ROUTE.  W3 checks equality of integer vectors in Z^{3n}, one per
(word, matching).  I instead verify the *group-level* identity

     Phi_w(b . a)  =  ( prod_v b_{v, w(v)} ) . Phi_w(a)                (G)

in exact rational arithmetic, where Phi is computed by HAFNIAN RECURSION
(no matching list at all).  (G) for all a is equivalent to L1 (compare
monomials), and it is the statement actually used downstream (a 1-PS
b_{v,c} = t^{w_{v,c}} then rescales every equation by a single power of t).

Then, separately, an exhaustive multidegree check with a THIRD route (the
involution enumerator) at n = 6 and n = 8.

Every checker is run against planted mutations; a checker that fails to kill
its mutant is reported as USELESS.
"""

from __future__ import annotations

import random
import sys
from fractions import Fraction

from a1_core import (
    COLS,
    all_cells,
    all_words,
    cellkey,
    gauge_apply,
    matchings_via_involutions,
    phi,
    phi_by_enumeration,
)


def rand_a(n, rng, density=1.0):
    a = {}
    for k in all_cells(n):
        if rng.random() < density:
            a[k] = Fraction(rng.randint(-9, 9), rng.randint(1, 7))
    return a


def rand_b(n, rng):
    return {
        (v, c): Fraction(rng.randint(1, 9), rng.randint(1, 9))
        * (1 if rng.random() < 0.5 else -1)
        for v in range(n)
        for c in COLS
    }


# --------------------------------------------------------------- checker 1


def check_gauge_covariance(n, trials, seed, mutate=None):
    """Returns (#violations, #tests).  `mutate` is an optional string."""
    rng = random.Random(seed)
    viol = tests = 0
    W = all_words(n)
    for _ in range(trials):
        a = rand_a(n, rng, density=0.7)
        b = rand_b(n, rng)
        if mutate == "square_second":
            ga = {}
            for (u, v, i, j), val in a.items():
                ga[(u, v, i, j)] = b[(u, i)] * b[(v, j)] ** 2 * val
        elif mutate == "cellwise":
            # a Route-T style *cell* weight: one distinguished cell gets an
            # extra independent factor, i.e. not of gauge form
            extra = rng.choice(sorted(a.keys())) if a else None
            ga = gauge_apply(a, b, n)
            if extra is not None:
                ga[extra] = ga[extra] * Fraction(7, 3)
        elif mutate == "drop_one_node":
            ga = {}
            for (u, v, i, j), val in a.items():
                ga[(u, v, i, j)] = b[(u, i)] * val   # forgets the v endpoint
        else:
            ga = gauge_apply(a, b, n)
        for w in W:
            lhs = phi(ga, w, n, Fraction(0), Fraction(1))
            scal = Fraction(1)
            for v in range(n):
                scal *= b[(v, w[v])]
            rhs = scal * phi(a, w, n, Fraction(0), Fraction(1))
            tests += 1
            if lhs != rhs:
                viol += 1
    return viol, tests


# --------------------------------------------------------------- checker 2


def check_multidegree(n, mutate=None):
    """Exhaustive over all words and all perfect matchings: the multiset of
    nodes (v, colour) touched by the cells of the matching is exactly
    {(v, word[v]) : v}, each once.  Enumerator = involutions (route 3)."""
    MS = matchings_via_involutions(n)
    bad = tests = 0
    for w in all_words(n):
        target = sorted((v, w[v]) for v in range(n))
        for idx, M in enumerate(MS):
            nodes = []
            for e in M:
                u, v = sorted(e)
                nodes.append((u, w[u]))
                nodes.append((v, w[v]))
            if mutate == "double_first_vertex" and idx == 0:
                nodes[0] = nodes[1]
            if mutate == "near_matching" and idx == 0:
                # simulate a term that covers vertex 0 twice and vertex 1 not
                # at all (i.e. NOT a perfect matching)
                nodes = [x for x in nodes if x[0] != 1] + [(0, w[0])]
            tests += 1
            if sorted(nodes) != target:
                bad += 1
    return bad, tests


# --------------------------------------------------------------- checker 3


def check_hafnian_vs_enumeration(n, trials, seed):
    """Sanity: the two independent evaluators of Phi agree."""
    rng = random.Random(seed)
    MS = matchings_via_involutions(n)
    bad = tests = 0
    W = all_words(n)
    for _ in range(trials):
        a = rand_a(n, rng, density=0.6)
        for w in rng.sample(W, min(40, len(W))):
            x = phi(a, w, n, Fraction(0), Fraction(1))
            y = phi_by_enumeration(a, w, n, MS, Fraction(0), Fraction(1))
            tests += 1
            if x != y:
                bad += 1
    return bad, tests


# ------------------------------------------------- initial form = restriction


def check_initial_is_restriction(n, trials, seed, mutate=None):
    """The claim actually used downstream.  For w admissible on S (every cell
    of S has weight >= 0), with S0 = {s in S : weight 0}:

        <w, pi_word> = 0  =>  Phi_word(a|S0) = Phi_word(a)
        <w, pi_word> > 0  =>  Phi_word(a|S0) = 0
        <w, pi_word> < 0  =>  impossible unless Phi_word(a) = 0

    Exact Fractions only.  Route: direct hafnian evaluation of both sides
    (W3 instead compares live-matching index sets).
    """
    rng = random.Random(seed)
    bad = tests = 0
    W = all_words(n)
    for _ in range(trials):
        wt = {}
        for c in COLS:
            vals = [rng.randint(-3, 3) for _ in range(n - 1)]
            vals.append(-sum(vals))          # <pi_c, w> = 0
            for v in range(n):
                wt[(v, c)] = vals[v]
        cw = lambda k: wt[(k[0], k[2])] + wt[(k[1], k[3])]
        a0 = rand_a(n, rng, density=0.5)
        S = {k for k in a0 if cw(k) >= 0}
        if mutate == "include_negative_cell":
            neg = [k for k in a0 if cw(k) < 0]
            if neg:
                S.add(rng.choice(sorted(neg)))
        a = {k: a0[k] for k in S}
        if not a:
            continue
        if mutate == "wrong_S0":
            # keep the weight-1 cells too: the "initial form" is then NOT the
            # restriction to the w-minimal cells
            S0 = {k for k in a if cw(k) <= 1}
        else:
            S0 = {k for k in a if cw(k) == 0}
        ares = {k: a[k] for k in S0}
        for word in W:
            mc = sum(wt[(v, word[v])] for v in range(n))
            full = phi(a, word, n, Fraction(0), Fraction(1))
            res = phi(ares, word, n, Fraction(0), Fraction(1))
            tests += 1
            if mc == 0:
                if res != full:
                    bad += 1
            elif mc > 0:
                if res != 0:
                    bad += 1
            else:
                if full != 0:
                    bad += 1
    return bad, tests


if __name__ == "__main__":
    print("AUDIT A1 / claim 1 (W3 crux lemma L1) -- independent checkers")
    print("=" * 72)

    for n in (6, 8):
        v, t = check_gauge_covariance(n, trials=(3 if n == 8 else 6), seed=11)
        print(f"[C1] gauge covariance  n={n}: violations={v} / tests={t}")

    print("  mutation controls for [C1] (a checker that does not kill these "
          "is useless):")
    for mut in ("square_second", "cellwise", "drop_one_node"):
        v, t = check_gauge_covariance(6, trials=2, seed=12, mutate=mut)
        verdict = "KILLED" if v > 0 else "*** SURVIVED (checker useless) ***"
        print(f"     mutant {mut:16s}: violations={v}/{t}  -> {verdict}")

    for n in (6, 8):
        b, t = check_multidegree(n)
        print(f"[C2] exhaustive multidegree  n={n}: bad={b} / (word,matching) "
              f"pairs={t}")
    for mut in ("double_first_vertex", "near_matching"):
        b, t = check_multidegree(6, mutate=mut)
        verdict = "KILLED" if b > 0 else "*** SURVIVED (checker useless) ***"
        print(f"     mutant {mut:20s}: bad={b}/{t} -> {verdict}")

    b, t = check_hafnian_vs_enumeration(6, trials=3, seed=13)
    print(f"[C3] hafnian == enumeration  n=6: bad={b}/{t}")

    for n in (6, 8):
        b, t = check_initial_is_restriction(n, trials=(6 if n == 6 else 2),
                                            seed=14)
        print(f"[C4] initial form == restriction  n={n}: bad={b}/{t}")
    for mut in ("include_negative_cell", "wrong_S0"):
        b, t = check_initial_is_restriction(6, trials=6, seed=14, mutate=mut)
        verdict = "KILLED" if b > 0 else "*** SURVIVED (checker useless) ***"
        print(f"     mutant {mut:22s}: bad={b}/{t} -> {verdict}")
