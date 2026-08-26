#!/usr/bin/env python3
"""W24 -- INDEPENDENT residual linear test + row-level diagnostics.
UNAUDITED.  Exact only.

Built from w24_core (from-the-definition engine).  Two differences from
w21_resid, both deliberate and both STRICTER:
  * rows are the COMBINATORIAL degree-<=1 words (point-independent), so a
    verdict here uses a subset of w21's rows -- a kill here implies a kill
    there;
  * every coefficient is recomputed as haf_Gamma(V - i - j)(w) directly.
"""
from __future__ import annotations

import json
import os
import sys
from fractions import Fraction
from itertools import combinations

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w24_core as C                                              # noqa: E402

_CACHE = {}


def row_skeleton(m):
    """[(w, (singles appearing linearly))] for the combinatorial deg<=1
    words that CARRY at least one variable, plus the list of clean words."""
    if m in _CACHE:
        return _CACHE[m]
    T = C.TEMPLATES[m]
    gam_set = set(C.gamma_edges(T))
    sing = C.single_edges(T)
    live = [e for e in sing
            if C.has_pm(gam_set, tuple(v for v in range(8) if v not in e))]
    rows, cleanw = [], []
    for w in C.MIXED:
        act = [e for e in sing
               if w[e[0]] == sing[e][0] and w[e[1]] == sing[e][1]]
        ones = [e for e in act if e in live]
        if not ones:
            cleanw.append(w)
            continue
        # combinatorial degree >= 2?
        deg2 = False
        for a, b in combinations(act, 2):
            if len(set(a) | set(b)) != 4:
                continue
            rest = tuple(v for v in range(8) if v not in set(a) | set(b))
            if C.has_pm(gam_set, rest):
                deg2 = True
                break
        if not deg2:
            rows.append((w, tuple(sorted(ones))))
    _CACHE[m] = (tuple(rows), tuple(cleanw), tuple(sorted(sing)),
                 tuple(sorted(live)))
    return _CACHE[m]


def build_system(m, bl):
    """returns (cells, rows) with rows = (w, coeff-vector, constant)."""
    T = C.TEMPLATES[m]
    gam_set = set(C.gamma_edges(T))
    rows_sk, cleanw, cells, live = row_skeleton(m)
    idx = {e: i for i, e in enumerate(cells)}
    n = len(cells)
    out = []
    for w, ones in rows_sk:
        v = [Fraction(0)] * n
        for e in ones:
            rest = tuple(x for x in range(8) if x not in e)
            v[idx[e]] = C.haf_on(bl, gam_set, rest, w)
        c = C.phi(bl, gam_set, w)
        if any(v) or c != 0:
            out.append((w, v, c))
    return cells, out, cleanw


def verdict(m, bl, want_detail=False):
    cells, rows, cleanw = build_system(m, bl)
    n = len(cells)
    aug = [list(v) + [-c] for _, v, c in rows]
    R, piv = C.rref(aug, n + 1)
    if n in piv:
        d = dict(n_unknowns=n, n_rows=len(rows), rank=len(piv),
                 inconsistent=True, forced_zero=[], killed=True)
    else:
        sol = [Fraction(0)] * n
        for i, pc in enumerate(piv):
            if pc < n:
                sol[pc] = R[i][n]
        ker = C.kernel_basis([list(v) for _, v, _ in rows], n)
        forced = [str(cells[i]) for i in range(n)
                  if sol[i] == 0 and all(b[i] == 0 for b in ker)]
        d = dict(n_unknowns=n, n_rows=len(rows), rank=len(piv),
                 inconsistent=False, solution_dim=len(ker),
                 forced_zero=forced, killed=bool(forced))
    if want_detail:
        pure, badconst, mixed = [], [], []
        for w, v, c in rows:
            nv = [i for i in range(n) if v[i] != 0]
            if not nv and c != 0:
                badconst.append((w, str(c)))
            elif len(nv) == 1 and c == 0:
                pure.append((w, str(cells[nv[0]])))
            elif nv:
                mixed.append((w, [str(cells[i]) for i in nv], c != 0))
        d["n_pure_monomial"] = len(pure)
        d["n_zero_row_nonzero_const"] = len(badconst)
        d["cells_hit_by_pure"] = sorted({p[1] for p in pure})
        d["pure_examples"] = [(list(w), s) for w, s in pure[:6]]
        d["badconst_examples"] = [(list(w), s) for w, s in badconst[:6]]
    return d
