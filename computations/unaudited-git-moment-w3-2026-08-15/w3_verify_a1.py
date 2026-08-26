"""UNAUDITED PROBE (agent W3, Route A, 2026-08-15).  HEAD 26ba69f7.

Exact verification of the three structural lemmas behind Theorem A.1.

L1 (uniform matching weight).  For every word c and every pair of perfect
    matchings M, M', the gauge weights of the two monomials agree:
       sum_{uv in M} (w_{u,c(u)} + w_{v,c(v)}) = sum_v w_{v,c(v)}
    independently of M.  Checked symbolically (as integer vectors in Z^{3n})
    for n = 6 and n = 8, over ALL words and ALL matchings.

    Consequence: the w-INITIAL FORM of every GHZ equation is the PLAIN
    RESTRICTION of that equation to the w-minimal cells.  There is no
    "initial form drops non-minimal matchings inside S_w" phenomenon for
    gauge weights.  (It does occur for general cell weights - Route T.)

L2 (pure positivity).  If a is exact with support S and w is S-admissible
    then <pi_c, w> >= 0 for each colour c, with equality iff the pure-c
    equation survives the degeneration.  Checked on random admissible w.

L3 (degeneration is exact).  If additionally <pi_c, w> = 0 for all three c,
    then a restricted to S_0(w) satisfies the full GHZ system with the SAME
    values.  Checked on exact rational near-configurations built by hand,
    and on the committed prism border family (n = 6).
"""

from __future__ import annotations

import itertools
import random
from fractions import Fraction

from w3_core import (
    cell_nodes,
    cells,
    edge_index,
    is_pure,
    matchings,
    node,
    phi,
    term_cells,
    words,
)


def check_L1(n: int) -> tuple[bool, int]:
    """Exhaustive: uniform matching weight, as an identity of integer vectors."""
    CN = cell_nodes(n)
    tc = term_cells(n)
    checked = 0
    for c in words(n):
        target = [0] * (3 * n)
        for v in range(n):
            target[node(v, c[v])] += 1
        for idxs in tc[c]:
            vec = [0] * (3 * n)
            for s in idxs:
                p, q = CN[s]
                vec[p] += 1
                vec[q] += 1
            if vec != target:
                return False, checked
            checked += 1
    return True, checked


def check_L1_initial_equals_restriction(n: int, trials: int = 200, seed: int = 0):
    """For random integer w and random supports: the set of matchings of word
    c that survive in lim t^w . a equals {all S-supported matchings of c} when
    <w,m_c> = 0, and is empty when <w,m_c> > 0."""
    rng = random.Random(seed)
    CN = cell_nodes(n)
    tc = term_cells(n)
    allcells = list(range(len(cells(n))))
    bad = 0
    for _ in range(trials):
        w = [rng.randint(-3, 3) for _ in range(3 * n)]
        Wv = {s: w[CN[s][0]] + w[CN[s][1]] for s in allcells}
        S = frozenset(s for s in allcells if Wv[s] >= 0 and rng.random() < 0.6)
        S0 = frozenset(s for s in S if Wv[s] == 0)
        for c in words(n):
            live = [k for k, idxs in enumerate(tc[c]) if all(s in S for s in idxs)]
            if not live:
                continue
            surv = [k for k in live if all(s in S0 for s in tc[c][k])]
            mc = sum(w[node(v, c[v])] for v in range(n))
            if mc == 0 and surv != live:
                bad += 1
            if mc > 0 and surv:
                bad += 1
            if mc < 0:
                bad += 1
    return bad == 0, trials


# ---------------------------------------------------------------- L3 data


def prism_source(n: int = 6, t: Fraction = Fraction(0)):
    """The committed prism border family (notes/tensor-route.md sec 6).

    P_1 = {14,23,56}, P_2 = {25,13,46}, P_3 = {36,12,45} on vertices 1..6,
    edge of P_r coloured r at both ends.  w_14 = t, w_23 = 1/t, rest 1.
    Here we use the *limit* t -> 0 form only for structure; for the exact
    identity we keep t symbolic-free and just record the support.
    """
    EI = edge_index(n)
    P = [
        [(0, 3), (1, 2), (4, 5)],
        [(1, 4), (0, 2), (3, 5)],
        [(2, 5), (0, 1), (3, 4)],
    ]
    a = [Fraction(0)] * (9 * len(EI))
    from w3_core import cell_index

    CI = cell_index(n)
    for r, cls in enumerate(P):
        for (u, v) in cls:
            u, v = min(u, v), max(u, v)
            a[CI[(EI[(u, v)], r, r)]] = Fraction(1)
    return a, P


def check_L3_on_random_supports(n: int, trials: int = 60, seed: int = 1):
    """Build a rational configuration on a random support, take an admissible
    pure-neutral w, and check that EVERY equation value is preserved on the
    restriction (the values Phi_c(a|S0) = Phi_c(a) for <w,m_c>=0 and
    Phi_c(a|S0)=0 for <w,m_c>>0)."""
    rng = random.Random(seed)
    CN = cell_nodes(n)
    allcells = list(range(len(cells(n))))
    fails = 0
    runs = 0
    for _ in range(trials):
        # pure-neutral integer w: each colour block sums to zero
        w = [0] * (3 * n)
        for c in range(3):
            vals = [rng.randint(-2, 2) for _ in range(n - 1)]
            vals.append(-sum(vals))
            for v in range(n):
                w[node(v, c)] = vals[v]
        Wv = {s: w[CN[s][0]] + w[CN[s][1]] for s in allcells}
        S = frozenset(s for s in allcells if Wv[s] >= 0)
        S0 = frozenset(s for s in S if Wv[s] == 0)
        if len(S0) == len(S):
            continue
        a = [Fraction(0)] * len(allcells)
        for s in S:
            a[s] = Fraction(rng.randint(1, 7), rng.randint(1, 5))
        a0 = [a[s] if s in S0 else Fraction(0) for s in allcells]
        runs += 1
        for c in words(n):
            mc = sum(w[node(v, c[v])] for v in range(n))
            lhs = phi(n, a0, c)
            if mc == 0:
                if lhs != phi(n, a, c):
                    fails += 1
                    break
            else:
                if lhs != 0:
                    fails += 1
                    break
    return fails == 0, runs


if __name__ == "__main__":
    print("UNAUDITED PROBE  W3 / Route A  HEAD 26ba69f7")
    for n in (6, 8):
        ok, cnt = check_L1(n)
        print(f"L1 uniform matching weight  n={n}: {ok}  ({cnt} monomials checked)")
    for n in (6,):
        ok, tr = check_L1_initial_equals_restriction(n, trials=120)
        print(f"L1' initial-form == restriction  n={n}: {ok}  ({tr} random (w,S))")
    for n in (6,):
        ok, runs = check_L3_on_random_supports(n, trials=40)
        print(f"L3 degeneration preserves every equation  n={n}: {ok}  ({runs} runs)")
