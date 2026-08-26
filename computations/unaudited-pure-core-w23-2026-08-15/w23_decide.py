#!/usr/bin/env python3
"""W23 -- INDEPENDENT exact decision of "does the pair (p,q) carry a witness?"

WITNESS at (p,q): an admissible cap K (s != 0 and kappa_0 kappa_1 kappa_2 != 0)
with E_pq(K) = 0 in every component.  Decided by Rabinowitsch saturation in
Singular over Q, and re-decided modulo two primes.

HAZARD FIXED HERE (hit while walking rational sources): W22's decider emits
sympy's default printing, so RATIONAL coefficients reach Singular as
`k20^2/9`, which its parser rejects (`poly ^ number failed`).  Every term of
E_pq(K) has the SAME total degree 2h in the blocks -- s is linear, R quadratic,
A linear, and a term with |J| = k contributes (h-k) + 2k + (h-k) = 2h -- so
scaling EVERY block by a common lambda scales E by lambda^{2h} and changes
neither admissibility nor the verdict.  We therefore clear denominators on the
source first and stay over Z.  (The scaling invariance is verified as a control
in run_t2c_walk.py.)
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction
from itertools import combinations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-pure-core-w23-2026-08-15")
sys.path.insert(0, BASE)
import w23_core as C                                          # noqa: E402

KVARS = tuple(f"zk{i}{j}" for i in range(3) for j in range(3))


def clear_denominators(src, ncol=3):
    L = 1
    for m in src.values():
        for row in m:
            for x in row:
                L = math.lcm(L, Fraction(x).denominator)
    out = {}
    for e, m in src.items():
        out[e] = [[int(Fraction(x) * L) for x in row] for row in m]
        for row in out[e]:
            for x in row:
                assert isinstance(x, int)
    return out, L


def sym_cap_error(src, p, q, sites, ncol=3):
    """E_pq(K) as sympy polynomials in the nine cap variables, plus s and the
    three kappas.  Works at every h (quadrics at h=2, cubics at h=3, ...)."""
    import sympy
    sites = tuple(sorted(sites))
    h = len(sites) // 2
    K = [[sympy.Symbol(KVARS[3 * i + j]) for j in range(ncol)]
         for i in range(ncol)]
    apq = C.oriented(src, p, q, ncol)
    s = sympy.expand(sum(K[i][j] * apq[i][j]
                         for i in range(ncol) for j in range(ncol)))
    R = {}
    for a, b in combinations(sites, 2):
        apa, aqa = C.oriented(src, p, a, ncol), C.oriented(src, q, a, ncol)
        apb, aqb = C.oriented(src, p, b, ncol), C.oriented(src, q, b, ncol)
        R[(a, b)] = [[sympy.expand(sum(K[i][j] * (apa[i][ca] * aqb[j][cb]
                                                  + aqa[j][ca] * apb[i][cb])
                                       for i in range(ncol) for j in range(ncol)))
                      for cb in range(ncol)] for ca in range(ncol)]
    A = {(a, b): C.oriented(src, a, b, ncol) for a, b in combinations(sites, 2)}

    def ent(tab, a, b, ca, cb):
        return tab[(a, b)][ca][cb] if a < b else tab[(b, a)][cb][ca]

    slot = {a: i for i, a in enumerate(sites)}
    eqs = []
    for word in product(range(ncol), repeat=len(sites)):
        tot = sympy.Integer(0)
        for M in C.perfect_matchings(sites):
            for size in range(2, h + 1):
                pref = s ** (h - size)
                for J in combinations(range(h), size):
                    Js = set(J)
                    term = pref
                    for i, (a, b) in enumerate(M):
                        term = term * ent(R if i in Js else A, a, b,
                                          word[slot[a]], word[slot[b]])
                    tot = tot + term
        tot = sympy.expand(tot)
        if tot != 0:
            eqs.append(tot)
    return eqs, s, [K[c][c] for c in range(ncol)]


def _sing(expr):
    import sympy
    e = sympy.expand(expr)
    txt = str(e).replace("**", "^").replace(" ", "")
    assert "/" not in txt, f"rational coefficient reached Singular: {txt[:80]}"
    return txt


def decide_pair(src, p, q, sites, tag, ncol=3, timeout=1800, primes=(32003,)):
    """Returns ('WITNESS'|'BLOCKED', dim, {prime: dim}).  Exact over Q; every
    verdict re-decided modulo the given primes."""
    isrc, _ = clear_denominators(src, ncol)
    eqs, s, kap = sym_cap_error(isrc, p, q, sites, ncol)
    gens = [_sing(e) for e in eqs]
    nz = "(" + _sing(s) + ")*(" + ")*(".join(_sing(k) for k in kap) + ")"
    out = {}
    verdict = None
    dimQ = None
    for char in (0,) + tuple(primes):
        lines = [f'ring zzR={char},({",".join(KVARS)},zzt),dp;',
                 "ideal zzI=" + (",".join(gens) if gens else "0") + ";",
                 f"ideal zzJ=zzI,zzt*({nz})-1;",
                 f'"DEC {tag} {char} "+string(dim(std(zzJ)));']
        script = "\n".join(lines)
        C.no_shadow_guard(script, set(KVARS) | {"zzt"})
        txt = C.run_singular(script, timeout=timeout)
        line = [ln for ln in txt.splitlines() if ln.startswith(f"DEC {tag} {char} ")]
        assert line, txt
        d = int(line[0].split()[-1])
        if char == 0:
            dimQ = d
            verdict = "BLOCKED" if d == -1 else "WITNESS"
        else:
            out[char] = d
    return verdict, dimQ, out


def live(src, p, q, ncol=3):
    return any(x != 0 for row in C.oriented(src, p, q, ncol) for x in row)
