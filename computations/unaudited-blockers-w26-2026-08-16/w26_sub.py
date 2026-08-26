#!/usr/bin/env python3
"""W26 -- the row-isolating sub-systems, the solo-row calculus, the
Case-2b predicate.  UNAUDITED.  Exact only.

DEFINITIONS (fixed here once and used everywhere):
  * live single: e with a Gamma perfect matching on V - e.
  * e-SOLO word: a mixed word at which e is the ONLY active live single.
    Its residual row reads   c_e(w) z_e + Phi(w) = 0.
  * PURE ROW at e: an e-solo word with Phi(w) = 0 and c_e(w) != 0
    (forces z_e = 0 -> kill).
  * BAD-CONST ROW at e: an e-solo word with c_e(w) = 0, Phi(w) != 0
    (inconsistent -> kill).
  * RATIO SPLIT at e: two e-solo words with c_e != 0 and different
    -Phi/c_e (inconsistent -> kill).
  The e-sub-system SURVIVES iff none of the three occurs, i.e. iff
  -Phi/c_e is a single NONZERO constant on the whole e-solo set and
  c_e never vanishes there.

  * SUB-SYSTEM i|Sc  (a row-isolating group): the rows at L-words x whose
    activatable live singles are exactly Sc (all at vertex i); unknowns Sc.
"""
from __future__ import annotations

import os
import sys
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w26_core as C                                              # noqa: E402

_SOLO = {}


def solo_words(m, e):
    """all e-solo mixed words."""
    key = (m, e)
    if key in _SOLO:
        return _SOLO[key]
    T = C.TEMPLATES[m]
    sing = C.single_edges(T)
    lv = set(C.live_singles(m))
    out = []
    for w in C.MIXED:
        act = tuple(f for f in lv
                    if w[f[0]] == sing[f][0] and w[f[1]] == sing[f][1])
        if act == (e,):
            out.append(w)
    _SOLO[key] = tuple(out)
    return _SOLO[key]


def solo_report(m, bl, e):
    """verdict for the e-solo family."""
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    pure = badconst = 0
    ratios = set()
    ex_pure = None
    for w in solo_words(m, e):
        c = C.coeff(bl, gs, e, w)
        p = C.phi(bl, gs, w)
        if c == 0:
            if p != 0:
                badconst += 1
            continue
        r = -p / c
        ratios.add(r)
        if r == 0:
            pure += 1
            if ex_pure is None:
                ex_pure = w
    return dict(n_solo=len(solo_words(m, e)), n_pure=pure,
                n_badconst=badconst, n_distinct_ratios=len(ratios),
                ratios=[str(r) for r in sorted(ratios)[:4]],
                killed=bool(pure or badconst or len(ratios) > 1),
                survives=(not pure and not badconst and len(ratios) == 1
                          and 0 not in ratios),
                example_pure=list(ex_pure) if ex_pure else None)


# ------------------------------------------------- row-isolating groups
_GRP = {}


def iso_groups(m):
    """{Sc: [x-words]} the row-isolating L-word groups."""
    if m in _GRP:
        return _GRP[m]
    T = C.TEMPLATES[m]
    sing = C.single_edges(T)
    lv = set(C.live_singles(m))
    grp = {}
    for x in product(range(3), repeat=4):
        can = tuple(sorted(f for f in lv if x[f[0]] == sing[f][0]))
        if not can or len({f[0] for f in can}) != 1:
            continue
        grp.setdefault(can, []).append(x)
    _GRP[m] = grp
    return grp


def sub_verdict(m, bl, xwords, targets):
    """residual sub-system on the given x-words in the unknowns `targets`."""
    T = C.TEMPLATES[m]
    gs = set(C.gamma_edges(T))
    sing = C.single_edges(T)
    lv = set(C.live_singles(m))
    idx = {e: k for k, e in enumerate(targets)}
    n = len(targets)
    rows = []
    for x in xwords:
        for y in product(range(3), repeat=4):
            w = tuple(x) + tuple(y)
            if len(set(w)) == 1:
                continue
            act = [f for f in lv
                   if w[f[0]] == sing[f][0] and w[f[1]] == sing[f][1]]
            if any(f not in idx for f in act):
                return None
            v = [Fraction(0)] * n
            for f in act:
                v[idx[f]] = C.coeff(bl, gs, f, w)
            cst = C.phi(bl, gs, w)
            if any(v) or cst != 0:
                rows.append(v + [-cst])
    if not rows:
        return dict(n_rows=0, inconsistent=False, forced=[], killed=False)
    Rw, piv = C.rref(rows, n + 1)
    if n in piv:
        return dict(n_rows=len(rows), rank=len(piv), inconsistent=True,
                    forced=[], killed=True)
    sol = [Fraction(0)] * n
    for k, pc in enumerate(piv):
        if pc < n:
            sol[pc] = Rw[k][n]
    ker = C.kernel_basis([r[:n] for r in rows], n)
    forced = [str(targets[k]) for k in range(n)
              if sol[k] == 0 and all(b[k] == 0 for b in ker)]
    return dict(n_rows=len(rows), rank=len(piv), inconsistent=False,
                solution_dim=len(ker), forced=forced, killed=bool(forced))


def all_sub_verdicts(m, bl):
    out = {}
    for can, xs in sorted(iso_groups(m).items()):
        lab = "%d|%s" % (can[0][0], ",".join(str(e) for e in can))
        v = sub_verdict(m, bl, xs, list(can))
        out[lab] = (None if v is None
                    else dict(killed=v["killed"],
                              inconsistent=v.get("inconsistent"),
                              forced=v.get("forced"), n_rows=v["n_rows"]))
    return out


# ------------------------------------------------------ the Case-2b test
def case2b(m, bl):
    """m=25 predicate:  v_c(y5,y7) = (A56[y5][c], A67[c][y7]);
    CASE 2b  <=>  v_0 || v_2 at all nine (y5,y7)  AND  v_1 not|| v_0 at
    all nine.  Returns (in_case2b, n_par02, n_par01)."""
    U = bl[(5, 6)]
    V = bl[(6, 7)]
    n02 = n01 = 0
    for y5 in range(3):
        for y7 in range(3):
            if U[y5][0] * V[2][y7] - U[y5][2] * V[0][y7] == 0:
                n02 += 1
            if U[y5][1] * V[0][y7] - U[y5][0] * V[1][y7] == 0:
                n01 += 1
    return (n02 == 9 and n01 == 0), n02, n01


def case2b_structure(bl):
    """the equivalent closed form of 'v_0 || v_2 at all nine':
    col0(A56) = mu col2(A56) and row0(A67) = mu row2(A67), one scalar mu."""
    U, V = bl[(5, 6)], bl[(6, 7)]
    if any(U[y5][2] == 0 for y5 in range(3)) or \
       any(V[2][y7] == 0 for y7 in range(3)):
        return None
    mus = {U[y5][0] / U[y5][2] for y5 in range(3)} | \
          {V[0][y7] / V[2][y7] for y7 in range(3)}
    return (len(mus) == 1), [str(x) for x in sorted(mus)]
