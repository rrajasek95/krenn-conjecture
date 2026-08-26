#!/usr/bin/env python3
"""W15 -- COMPRESSED (half-permanent) model of the clean subsystem.

For these templates the full-block graph Gamma is  K4(L) u (R-internal) u
(a set C of disjoint full CROSS edges).  Hence for every word (x,y)

  Phi(x,y) = sum over even S <= C of
             (prod_{e in S} A_e[x_u][y_v]) * PL_{L\\S}(x) * PR_{R\\S}(y)

where PL_{L'}(x) is the half-permanent of the full L-blocks on L' (a single
CELL when |L'| = 2, the 3-term permanent P_L(x) when L' = L, and 1 when
L' is empty), and likewise PR.

COMPRESSION (a RELAXATION, hence sound for deriving necessary conditions):
introduce one fresh atom for each value  P_L(x)  and each  P_R(y)  used,
dropping the polynomial relations that express them through the cells.
Every other factor stays an honest occupied CELL and is required nonzero.
Any exact source gives a point of the compressed system, so infeasibility
of the compressed system kills the template.

Exact over Q (Singular).
"""

from __future__ import annotations

import os
import sys
from fractions import Fraction
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w15_core import EDGES, EIDX, FULL, single_cell_activity, is_clean
from w15_forcing import to_singular, run_singular

L, R = (0, 1, 2, 3), (4, 5, 6, 7)


def cross_full(T):
    return [e for e in EDGES if e[0] in L and e[1] in R and T[EIDX[e]] == FULL]


def _pm_pairs(vs):
    if not vs:
        return [()]
    out = []
    for k in range(1, len(vs)):
        rest = vs[1:k] + vs[k + 1:]
        for tail in _pm_pairs(rest):
            out.append(((vs[0], vs[k]),) + tail)
    return out


class Atoms:
    def __init__(self):
        self.ids = {}
        self.names = []
        self.iscell = []

    def get(self, key, iscell):
        if key not in self.ids:
            self.ids[key] = len(self.names)
            self.names.append(key)
            self.iscell.append(iscell)
        return self.ids[key]

    def cellvars(self):
        return [i for i, c in enumerate(self.iscell) if c]


def half_perm_atom(T, atoms, side, verts, word, which):
    """Atom(s) for the half-permanent of the FULL blocks on `verts`.
    Returns None if it is identically zero, else a polynomial."""
    if not verts:
        return {(): Fraction(1)}
    if len(verts) == 2:
        u, v = verts
        e = (u, v) if u < v else (v, u)
        if T[EIDX[e]] != FULL:
            return None
        cell = 3 * word[e[0]] + word[e[1]]
        return {(atoms.get(f"A{e[0]}{e[1]}_{cell//3}{cell%3}", True),):
                Fraction(1)}
    # |verts| == 4 : one fresh atom per (side, word restricted to verts)
    key = f"P{which}[{''.join(str(word[v]) for v in verts)}]"
    # only legitimate if at least one full-block matching exists there
    ok = False
    for pm in _pm_pairs(list(verts)):
        if all(T[EIDX[tuple(sorted(p))]] == FULL for p in pm):
            ok = True
    if not ok:
        return None
    return {(atoms.get(key, False),): Fraction(1)}


def phi_compressed(T, atoms, x, y):
    """Phi(x,y) in the compressed atoms."""
    w = tuple(x) + tuple(y)
    C = cross_full(T)
    out = {}
    for k in (0, 2, 4):
        for S in combinations(C, k):
            us = [e[0] for e in S]
            vs = [e[1] for e in S]
            if len(set(us)) != k or len(set(vs)) != k:
                continue
            lrest = tuple(v for v in L if v not in us)
            rrest = tuple(v for v in R if v not in vs)
            pl = half_perm_atom(T, atoms, "L", lrest, w, "L")
            if pl is None:
                continue
            pr = half_perm_atom(T, atoms, "R", rrest, w, "R")
            if pr is None:
                continue
            term = {(): Fraction(1)}
            for e in S:
                cell = 3 * w[e[0]] + w[e[1]]
                a = atoms.get(f"A{e[0]}{e[1]}_{cell//3}{cell%3}", True)
                term = {tuple(sorted(m + (a,))): c for m, c in term.items()}
            for fac in (pl, pr):
                new = {}
                for m1, c1 in term.items():
                    for m2, c2 in fac.items():
                        mm = tuple(sorted(m1 + m2))
                        new[mm] = new.get(mm, Fraction(0)) + c1 * c2
                term = new
            for m, c in term.items():
                out[m] = out.get(m, Fraction(0)) + c
    return {m: c for m, c in out.items() if c}


def decide(T, eq_words, target_word, timeout=1800, char=0, tag=""):
    """Is Phi(target) forced to vanish, given Phi = 0 on eq_words and all
    CELLS nonzero?  Rabinowitsch over Q (char=0 -> a verdict)."""
    atoms = Atoms()
    eqs = [phi_compressed(T, atoms, w[:4], w[4:]) for w in eq_words]
    tgt = phi_compressed(T, atoms, target_word[:4], target_word[4:])
    used = sorted(set(i for p in eqs + [tgt] for m in p for i in m))
    names = {v: f"z{v}" for v in used}
    cells = [v for v in used if atoms.iscell[v]]
    lines = [f"ring r = {char},({','.join(names[v] for v in used)},uu),dp;"]
    for i, p in enumerate(eqs, 1):
        lines.append(f"poly q{i} = {to_singular(p, names)};")
    lines.append(f"poly tg = {to_singular(tgt, names)};")
    prod = "*".join(names[v] for v in cells)
    lines.append("ideal Jid = " +
                 ",".join(f"q{i}" for i in range(1, len(eqs) + 1)) +
                 f",uu*{prod}*tg-1;")
    lines.append("ideal GB = groebner(Jid);")
    lines.append('"FORCED:"; (GB[1]==1);')
    lines.append("quit;")
    script = "\n".join(lines) + "\n"
    raw = run_singular(script, timeout=timeout)
    v = None
    if "FORCED:" in raw:
        v = raw.split("FORCED:")[1].strip().split()[0] == "1"
    return v, len(used), len(cells), len(eqs), script, raw


def decide_sat(T, eq_words, target_word, timeout=1800, char=0):
    """Cheaper SUFFICIENT test: is Phi(target) in ideal(Phi(eq_words)) :
    (product of cell atoms)^infty ?  Computed as iterated single-variable
    saturation (elim.lib).  A 'True' is a genuine kill certificate (an
    explicit monomial multiple lies in the ideal); a 'False' is
    inconclusive (membership may still hold in the radical)."""
    atoms = Atoms()
    eqs = [phi_compressed(T, atoms, w[:4], w[4:]) for w in eq_words]
    tgt = phi_compressed(T, atoms, target_word[:4], target_word[4:])
    used = sorted(set(i for p in eqs + [tgt] for m in p for i in m))
    names = {v: f"z{v}" for v in used}
    cells = [v for v in used if atoms.iscell[v]]
    lines = ['LIB "elim.lib";',
             f"ring r = {char},({','.join(names[v] for v in used)}),dp;"]
    for i, p in enumerate(eqs, 1):
        lines.append(f"poly q{i} = {to_singular(p, names)};")
    lines.append(f"poly tg = {to_singular(tgt, names)};")
    lines.append("ideal Jid = " +
                 ",".join(f"q{i}" for i in range(1, len(eqs) + 1)) + ";")
    lines.append("Jid = groebner(Jid);")
    for v in cells:
        lines.append(f"Jid = groebner(sat(Jid,{names[v]})[1]);")
    lines.append("poly nf = reduce(tg,Jid);")
    lines.append('"FORCED:"; (nf==0);')
    lines.append('"UNITIDEAL:"; (Jid[1]==1);')
    lines.append("quit;")
    raw = run_singular("\n".join(lines) + "\n", timeout=timeout)
    v = u = None
    if "FORCED:" in raw:
        v = raw.split("FORCED:")[1].strip().split()[0] == "1"
    if "UNITIDEAL:" in raw:
        u = raw.split("UNITIDEAL:")[1].strip().split()[0] == "1"
    return v, u, len(used), len(cells), len(eqs), raw


def decide_pow(T, eq_words, target_word, kmax=6, timeout=1800, char=0):
    """SUFFICIENT test with an EXPLICIT certificate: for k = 1..kmax ask
    whether  (prod of cell atoms)^k * Phi(target)  reduces to 0 modulo a
    Groebner basis of the clean equations.  'True at k' is a monomial
    certificate: since every cell is nonzero, Phi(target) = 0 follows."""
    atoms = Atoms()
    eqs = [phi_compressed(T, atoms, w[:4], w[4:]) for w in eq_words]
    tgt = phi_compressed(T, atoms, target_word[:4], target_word[4:])
    used = sorted(set(i for p in eqs + [tgt] for m in p for i in m))
    names = {v: f"z{v}" for v in used}
    cells = [v for v in used if atoms.iscell[v]]
    lines = [f"ring r = {char},({','.join(names[v] for v in used)}),dp;"]
    for i, p in enumerate(eqs, 1):
        lines.append(f"poly q{i} = {to_singular(p, names)};")
    lines.append(f"poly tg = {to_singular(tgt, names)};")
    lines.append("poly pr = " + "*".join(names[v] for v in cells) + ";")
    lines.append("ideal Jid = " +
                 ",".join(f"q{i}" for i in range(1, len(eqs) + 1)) + ";")
    lines.append("ideal GB = groebner(Jid);")
    lines.append("poly acc = tg;")
    for k in range(1, kmax + 1):
        lines.append("acc = reduce(acc*pr,GB);")
        lines.append(f'"K{k}:"; (acc==0);')
    lines.append("quit;")
    raw = run_singular("\n".join(lines) + "\n", timeout=timeout)
    kfound = None
    for k in range(1, kmax + 1):
        tag = f"K{k}:"
        if tag in raw and raw.split(tag)[1].strip().split()[0] == "1":
            kfound = k
            break
    return kfound, len(used), len(cells), len(eqs), raw


def eff_clean_words(T):
    """Words whose fibre is contained in the FULL-block matchings; on these
    H_w = Phi(x,y) exactly.  Strictly larger than the clean set."""
    from w15_core import WORDS, supported_matchings
    from w15_forcing import full_matchings
    F = set(full_matchings(T))
    return [w for w in WORDS if set(supported_matchings(T, w)) <= F]


def decide_full(T, eq_words, nonzero_words, timeout=1800, char=0):
    """THE Phi-SYSTEM DECISION.  Infeasibility over Qbar of

        Phi(w) = 0            for every effectively-clean MIXED word w
        Phi(t) != 0           for every t in nonzero_words
        every occupied CELL   != 0

    decided by Rabinowitsch (one auxiliary variable).  Unit ideal => no
    exact source with this template.  (For a constant word t, Phi(t) = H_t
    when t is effectively clean; for a mixed word t with exactly one extra
    supported matching, H_t = 0 forces Phi(t) = -monomial != 0.)"""
    atoms = Atoms()
    eqs = [phi_compressed(T, atoms, w[:4], w[4:]) for w in eq_words]
    tgts = [phi_compressed(T, atoms, w[:4], w[4:]) for w in nonzero_words]
    used = sorted(set(i for p in eqs + tgts for m in p for i in m))
    names = {v: f"z{v}" for v in used}
    cells = [v for v in used if atoms.iscell[v]]
    lines = [f"ring r = {char},({','.join(names[v] for v in used)},uu),dp;"]
    for i, p in enumerate(eqs, 1):
        lines.append(f"poly q{i} = {to_singular(p, names)};")
    for i, p in enumerate(tgts, 1):
        lines.append(f"poly t{i} = {to_singular(p, names)};")
    facs = [names[v] for v in cells] + [f"t{i}" for i in range(1, len(tgts)+1)]
    lines.append("poly pr = " + ("*".join(facs) if facs else "1") + ";")
    lines.append("ideal Jid = " +
                 ",".join(f"q{i}" for i in range(1, len(eqs) + 1)) +
                 ",uu*pr-1;")
    lines.append("ideal GB = groebner(Jid);")
    lines.append('"INFEASIBLE:"; (GB[1]==1);')
    lines.append("quit;")
    raw = run_singular("\n".join(lines) + "\n", timeout=timeout)
    v = None
    if "INFEASIBLE:" in raw:
        v = raw.split("INFEASIBLE:")[1].strip().split()[0] == "1"
    return v, len(used), len(cells), len(eqs), raw
