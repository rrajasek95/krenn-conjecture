#!/usr/bin/env python3
"""W15 -- Phi-forcing, version 2: iterated single-variable SATURATION.

Same mechanism as w15_forcing.py but the decision is made by computing
I : (z_1 ... z_n)^infty  as iterated  sat(I, z_i)  (elim.lib) and then
reducing the target.  This is far cheaper than the one-shot Rabinowitsch
ideal, whose extra generator has degree = #variables.

Exact over Q.  A separate fast screen over F_p is available for search
only (labelled; carries no verdict).
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w15_core import VarMap, single_cell_activity, is_clean
from w15_forcing import (full_matchings, phi_poly, extras, y_free, x_ok,
                         to_singular, run_singular)


def build_rectangle(T, target, xs, ys):
    """Clean equations of the rectangle ({x*} u xs) x ({y*} u ys) minus the
    target, plus the target polynomial.  Returns (eqs, tgt, vmap)."""
    vm = VarMap(T)
    act = single_cell_activity(T)
    fullm = full_matchings(T)
    xstar, ystar = tuple(target[0]), tuple(target[1])
    X0 = [xstar] + [tuple(x) for x in xs if tuple(x) != xstar]
    Y0 = [ystar] + [tuple(y) for y in ys if tuple(y) != ystar]
    eqs = []
    for x in X0:
        for y in Y0:
            if (x, y) == (xstar, ystar):
                continue
            w = x + y
            assert is_clean(T, w, act), f"non-clean rectangle entry {w}"
            assert len(set(w)) > 1, f"constant rectangle entry {w}"
            eqs.append(phi_poly(T, vm, x, y, fullm))
    return eqs, phi_poly(T, vm, xstar, ystar, fullm), vm


def forcing_test_sat(T, target, xs, ys, timeout=1800, char=0,
                     extra_eqs=()):
    """Decide whether Phi(target) lies in  ideal(clean eqs) : (prod z)^infty.
    char=0 -> exact over Q (a verdict); char=p -> screen only."""
    eqs, tgt, vm = build_rectangle(T, target, xs, ys)
    eqs = list(eqs) + list(extra_eqs)
    used = set()
    for p in list(eqs) + [tgt]:
        for mon in p:
            used.update(mon)
    used = sorted(used)
    names = {v: f"z{i}" for i, v in enumerate(used)}
    lines = ['LIB "elim.lib";',
             f"ring r = {char},({','.join(names[v] for v in used)}),dp;"]
    for i, p in enumerate(eqs, 1):
        lines.append(f"poly q{i} = {to_singular(p, names)};")
    lines.append(f"poly tg = {to_singular(tgt, names)};")
    lines.append("ideal Jid = " +
                 ",".join(f"q{i}" for i in range(1, len(eqs) + 1)) + ";")
    lines.append("Jid = groebner(Jid);")
    for v in used:
        lines.append(f"Jid = groebner(sat(Jid,{names[v]})[1]);")
    lines.append("poly nf = reduce(tg,Jid);")
    lines.append('"PHI_FORCED_TO_VANISH:"; (nf==0);')
    lines.append('"SATURATED_IDEAL_IS_UNIT:"; (Jid[1]==1);')
    lines.append("quit;")
    raw = run_singular("\n".join(lines) + "\n", timeout=timeout)
    forced = unit = None
    if "PHI_FORCED_TO_VANISH:" in raw:
        forced = raw.split("PHI_FORCED_TO_VANISH:")[1].strip().split()[0] == "1"
    if "SATURATED_IDEAL_IS_UNIT:" in raw:
        unit = (raw.split("SATURATED_IDEAL_IS_UNIT:")[1].strip().split()[0]
                == "1")
    return forced, unit, len(used), len(eqs), raw
