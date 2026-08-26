#!/usr/bin/env python3
"""UNAUDITED PROBE W29 (the diagonal closer) -- core engine.

Pinned HEAD: see PINNED_HEAD.txt.  All arithmetic EXACT (Fraction / Q(omega)
via w28_core.Cyc / sparse polynomials over Q / Singular char 0; mod-p only as
a screen, at 1-mod-3 primes per ledger 19).

INDEPENDENT re-implementation of the hafnian: explicit PERFECT-MATCHING
ENUMERATION with a memo of the matching lists per site tuple.  W28 recurses on
the lowest remaining site with a value memo; W25 uses a bitmask DP.  The
cross-check `check_haf_agreement` compares this engine against w28_core.haf_w
on random exact inputs (both Q and Q(omega)).

THE DIAGONAL PICTURE USED THROUGHOUT (W28-DEC, re-derived here).  A diagonal
source on K_N is three symmetric weight functions t^0, t^1, t^2 on the edges.
For a word w the matching sum factorises,

    H_w = prod_c haf(t^c | w^{-1}(c)),

so "EXACT" means: haf(t^c|V) = 1 for each c, and for EVERY ordered partition
V = S_0 + S_1 + S_2 that is not all-in-one-part,
prod_c haf(t^c|S_c) = 0.  Parts of odd size kill the product automatically, so
at N = 8 only the size profiles (8,0,0), (6,2,0), (4,4,0), (4,2,2) carry
content -- every one of them has a part of size >= 4, i.e. off-count <= 4:

    at N = 8, for DIAGONAL sources,  X_4 = EXACT.

Deleting a site z and looking at the star at z gives W28's picture on
V' = V - z (7 sites, 63 weights).
"""
from __future__ import annotations

import os
import random
import subprocess
import sys
import tempfile
from fractions import Fraction
from itertools import combinations

W28 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
       "unaudited-x4empty-w28-2026-08-18")
if W28 not in sys.path:
    sys.path.insert(0, W28)
import w28_core as K                                                # noqa: E402

NCOL = 3
Poly = K.Poly
Cyc = K.Cyc


def require(cond, detail):
    if not cond:
        raise AssertionError(detail)


def ekey(a, b):
    return (a, b) if a < b else (b, a)


# ---------------------------------------------------------------- hafnian
_PMS = {}


def pm_list(sites):
    """All perfect matchings of `sites` as tuples of sorted pairs (memoised)."""
    sites = tuple(sorted(sites))
    if sites in _PMS:
        return _PMS[sites]
    if not sites:
        out = [()]
    elif len(sites) % 2:
        out = []
    else:
        out = []
        h, rest = sites[0], sites[1:]
        for i in range(len(rest)):
            sub = rest[:i] + rest[i + 1:]
            e = ekey(h, rest[i])
            for M in pm_list(sub):
                out.append((e,) + M)
    _PMS[sites] = out
    return out


def haf(w, sites, zero=None, one=None):
    """Hafnian of the edge-weight dict w over `sites` by PM ENUMERATION."""
    if zero is None:
        zero = Fraction(0)
    if one is None:
        one = Fraction(1)
    tot = zero
    for M in pm_list(sites):
        p = one
        ok = True
        for e in M:
            v = w.get(e, zero)
            if v == 0:
                ok = False
                break
            p = p * v
        if ok:
            tot = tot + p
    return tot


def check_haf_agreement(trials=40, seed=11, n=8):
    """Cross-check this engine against w28_core.haf_w (Q and Q(omega))."""
    rng = random.Random(seed)
    V = tuple(range(n))
    bad = 0
    for t in range(trials):
        cyc = (t % 2 == 1)
        w = {}
        for e in combinations(V, 2):
            if rng.random() < 0.6:
                if cyc:
                    w[e] = Cyc(Fraction(rng.randint(-4, 4), rng.randint(1, 3)),
                               Fraction(rng.randint(-4, 4)))
                else:
                    w[e] = Fraction(rng.randint(-6, 6), rng.randint(1, 4))
        zero = Cyc(0, 0) if cyc else Fraction(0)
        one = Cyc(1, 0) if cyc else Fraction(1)
        for m in (4, 6, 8):
            S = tuple(rng.sample(V, m))
            a = haf(w, S, zero, one)
            b = K.haf_w(w, S, zero, one)
            if not (a - b == 0):
                bad += 1
    return bad


# ---------------------------------------------- the N = 8 diagonal EXACT test
def profiles_8():
    """Ordered even-size profiles (|S_0|,|S_1|,|S_2|) summing to 8."""
    out = []
    for a in range(0, 9, 2):
        for b in range(0, 9 - a, 2):
            c = 8 - a - b
            if c % 2 == 0:
                out.append((a, b, c))
    return out


def exact_violations(ts, n=8, zero=None, one=None, stop=True):
    """[] iff the diagonal source (t^0,t^1,t^2) is an EXACT source on K_n."""
    if zero is None:
        zero, one = Fraction(0), Fraction(1)
    V = tuple(range(n))
    bad = []
    for c in range(3):
        v = haf(ts[c], V, zero, one)
        if not (v - one == 0):
            bad.append(("PURE", c, v))
            if stop:
                return bad
    for S0sz in range(0, n + 1, 2):
        for S0 in combinations(V, S0sz):
            R = [x for x in V if x not in S0]
            for S1sz in range(0, len(R) + 1, 2):
                for S1 in combinations(R, S1sz):
                    S2 = tuple(x for x in R if x not in S1)
                    if S0sz == n or S1sz == n or len(S2) == n:
                        continue
                    p = (haf(ts[0], S0, zero, one) * haf(ts[1], S1, zero, one)
                         * haf(ts[2], S2, zero, one))
                    if p != 0:
                        bad.append(("MIX", S0, S1, S2, p))
                        if stop:
                            return bad
    return bad


# ------------------------------------------- the K_8 structure lemmas (W29-K8)
def H_pair(tc, a, b, n=8, zero=None, one=None):
    """haf(t^c | V - {a,b}) -- the hafnian adjugate entry."""
    V = tuple(x for x in range(n) if x not in (a, b))
    return haf(tc, V, zero, one)


def active_edges(ts, c, n=8, zero=None, one=None):
    """A_c = {e : t^c_e != 0 and haf(t^c|V-e) != 0} (W28-GOOD's good class)."""
    out = []
    for e in combinations(range(n), 2):
        if ts[c].get(e, 0) != 0 and H_pair(ts[c], e[0], e[1], n, zero, one) != 0:
            out.append(e)
    return out


# --------------------------------------------------------------- Singular
def run_singular(script, timeout=3600):
    """Ledger 6/11/14/22: parse stdout for '?' lines; RC 0 is NOT enough."""
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script + "\nquit;\n")
        path = fh.name
    try:
        proc = subprocess.run(["Singular", "-q", "--no-warn", path],
                              capture_output=True, text=True, timeout=timeout)
    finally:
        os.unlink(path)
    out = proc.stdout
    bad = [ln for ln in out.splitlines() if ln.strip().startswith("?")]
    if proc.returncode != 0 or bad:
        raise RuntimeError(f"Singular rc={proc.returncode} bad={bad[:6]} "
                           f"stderr={proc.stderr[:1000]}")
    return out


def no_shadow_guard(script, ringvars):
    return K.no_shadow_guard(script, ringvars)


__all__ = [n for n in dir() if not n.startswith("_")]
