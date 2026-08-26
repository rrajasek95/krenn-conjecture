#!/usr/bin/env python3
"""W15 -- the PHI-FORCING engine (uniform mechanism for family (R)).

Every matching all of whose blocks are FULL is supported on EVERY word, so
for any word w = (x,y)

    H_w = Phi(x,y) + sum of the 'extra' monomials (matchings that use at
                     least one single-cell block and are supported at w)

where Phi = sum over the FULL-block matchings F(T).  A word is CLEAN when
no single-cell block is active on it; then H_w = Phi(x,y).

MECHANISM.  If the clean equations force Phi(x*,y*) = 0 at a target point
(x*,y*) where Phi is required to be nonzero, the template dies:
  k = 0 extras at a CONSTANT word  ->  H = 0, contradiction;
  k = 1 extra at a MIXED word      ->  a single monomial = 0, contradiction;
  k = 2 extras at a MIXED word     ->  a BINOMIAL relation (fibre collapse).

CERTIFICATE SHAPE (rectangle).  Let Yfree = R-words y such that (x,y) is
clean for every x, and for a target (x*,y*) let Xok = L-words x != x* with
(x,y*) clean.  Then every pair in ({x*} u X') x ({y*} u Y') other than the
target is clean, for X' <= Xok, Y' <= Yfree.  Feed those clean equations to
Singular and test, by Rabinowitsch, whether

    { clean equations = 0,  (prod of all occupied cells) * Phi(x*,y*) != 0 }

is infeasible over Q.  Infeasible  <=>  Phi(x*,y*) = 0 is forced.

Exact arithmetic throughout (Singular over Q; Fractions in python).
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w15_core import (EDGES, EIDX, FULL, MATCHINGS, MATCH_EIDX, VarMap,
                      cell_of, is_clean, single_cell_activity,
                      supported_matchings, pmul, pvar, Fraction)

L4 = tuple(product(range(3), repeat=4))


def full_matchings(T):
    return [mi for mi, m in enumerate(MATCHINGS)
            if all(T[EIDX[e]] == FULL for e in m)]


def phi_poly(T, vm, x, y, fullm):
    """sum over the FULL-block matchings of the monomial at word (x,y)."""
    w = tuple(x) + tuple(y)
    out = {}
    for mi in fullm:
        mon = tuple(sorted(vm.var(e, cell_of(e, w)) for e in MATCH_EIDX[mi]))
        out[mon] = out.get(mon, Fraction(0)) + 1
    return out


def extras(T, x, y, fullm):
    w = tuple(x) + tuple(y)
    return [mi for mi in supported_matchings(T, w) if mi not in set(fullm)]


def y_free(T, act):
    """R-words y such that (x,y) is clean for EVERY L-word x."""
    return [y for y in L4 if all(is_clean(T, tuple(x) + tuple(y), act)
                                 for x in L4)]


def x_ok(T, act, ystar):
    return [x for x in L4 if is_clean(T, tuple(x) + tuple(ystar), act)]


def to_singular(poly, names):
    if not poly:
        return "0"
    terms = []
    for mon, c in sorted(poly.items()):
        num = c.numerator
        assert c.denominator == 1
        s = ("+" if num > 0 else "-")
        if abs(num) != 1 or not mon:
            s += str(abs(num))
            if mon:
                s += "*"
        s += "*".join(names[v] for v in mon)
        terms.append(s)
    out = "".join(terms)
    return out[1:] if out.startswith("+") else out


def run_singular(script, timeout=900):
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script)
        path = fh.name
    try:
        p = subprocess.run(["Singular", "-q", "--no-warn", path],
                           capture_output=True, text=True, timeout=timeout)
        return p.stdout + p.stderr
    finally:
        os.unlink(path)


def forcing_test(T, target, xs, ys, timeout=900, extra_eqs=()):
    """Is Phi(target) forced to vanish by the clean equations on
    ({x*} u xs) x ({y*} u ys)?   Returns (verdict, n_vars, n_eqs, raw)."""
    vm = VarMap(T)
    act = single_cell_activity(T)
    fullm = full_matchings(T)
    xstar, ystar = target
    X0 = [tuple(xstar)] + [tuple(x) for x in xs if tuple(x) != tuple(xstar)]
    Y0 = [tuple(ystar)] + [tuple(y) for y in ys if tuple(y) != tuple(ystar)]
    eqs = []
    for x in X0:
        for y in Y0:
            if (x, y) == (tuple(xstar), tuple(ystar)):
                continue
            w = x + y
            assert is_clean(T, w, act), f"non-clean pair in rectangle: {w}"
            assert len(set(w)) > 1, f"constant word in rectangle: {w}"
            eqs.append(phi_poly(T, vm, x, y, fullm))
    eqs.extend(extra_eqs)
    tgt = phi_poly(T, vm, xstar, ystar, fullm)
    used = set()
    for p in eqs + [tgt]:
        for mon in p:
            used.update(mon)
    used = sorted(used)
    names = {v: f"z{i}" for i, v in enumerate(used)}
    lines = [f"ring r = 0,({','.join(names[v] for v in used)},uu),dp;"]
    for i, p in enumerate(eqs, 1):
        lines.append(f"poly q{i} = {to_singular(p, names)};")
    lines.append(f"poly tg = {to_singular(tgt, names)};")
    prod = "*".join(names[v] for v in used)
    lines.append(f"ideal Jid = {','.join(f'q{i}' for i in range(1, len(eqs)+1))}"
                 f",uu*{prod}*tg-1;")
    lines.append("ideal GB = groebner(Jid);")
    lines.append('"UNIT_IDEAL(1=forced):"; (GB[1]==1);')
    lines.append("quit;")
    raw = run_singular("\n".join(lines) + "\n", timeout=timeout)
    verdict = None
    if "UNIT_IDEAL(1=forced):" in raw:
        tail = raw.split("UNIT_IDEAL(1=forced):")[1].strip().split()[0]
        verdict = (tail == "1")
    return verdict, len(used), len(eqs), raw
