#!/usr/bin/env python3
"""W21-M2-SING core: exact polynomial machinery for the C_8 cross-block
permanent systems + a guarded Singular harness.

UNAUDITED.  Exact arithmetic only (Fraction / integer-coefficient sparse
polynomials).  Floats are never used anywhere in this file.

LEDGER GUARDS BUILT IN
  L13  : every emitted generator is named zzg<k>, every ring variable zzv<k>
         (+ zzu for Rabinowitsch).  check_no_shadowing() is run on EVERY
         emitted script; the prefixes are disjoint by construction but the
         guard is still executed and its result reported.
  L11  : Singular prints errors on stdout and returns 0.  run_singular()
         scans for '?' lines / 'error occurred' and raises.
         LIB "elim.lib" is emitted whenever sat() is used, and sat is used
         as   list zzL = sat(I,J); ideal zzS = zzL[1];
  L6   : no identifier e1/mult/I is ever emitted; no leading unary '+'.
  L17  : nothing here decides vanishing by random specialisation.  Random
         points are used ONLY to CHECK identities that must hold for ALL
         points (equation-generator controls).
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from fractions import Fraction
from itertools import permutations, product

sys.dont_write_bytecode = True

_W21 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _W21 not in sys.path:
    sys.path.insert(0, _W21)
import w21_c8core as G                                    # read-only import

L, R = G.L, G.R
LPOS, RPOS = G.LPOS, G.RPOS
DEAD = G.DEAD
LFREE, RFREE = G.LFREE, G.RFREE
BIJ = tuple(permutations(R))          # sigma: L -> R given as tuple over LPOS


# ------------------------------------------------------------------ variables
def occ(i, j, c, d):
    return DEAD.get((i, j)) != (c, d)


CELLS = tuple((i, j, c, d) for i in L for j in R
              for c in range(3) for d in range(3) if occ(i, j, c, d))
CIDX = {cell: k for k, cell in enumerate(CELLS)}
assert len(CELLS) == 136


# ------------------------------------------------------------------ polynomials
# poly = dict {sorted tuple of cell-keys : int coefficient}.  Cell keys are the
# 4-tuples (i,j,c,d) themselves; substitution of 1 simply drops the key.
def p_add(a, b):
    out = dict(a)
    for m, c in b.items():
        v = out.get(m, 0) + c
        if v:
            out[m] = v
        else:
            out.pop(m, None)
    return out


def p_eval(poly, val):
    """val: dict cell -> Fraction.  Returns Fraction."""
    tot = Fraction(0)
    for mon, c in poly.items():
        t = Fraction(c)
        for v in mon:
            t *= val[v]
        tot += t
    return tot


def per_poly(x, y):
    """per B(x,y) as a polynomial in the cross cells.  x,y are 4-tuples of
    colours for L-sites 0..3 and R-sites 4..7 respectively."""
    out = {}
    for sig in BIJ:
        mon = []
        ok = True
        for k, i in enumerate(L):
            j = sig[k]
            cell = (i, j, x[k], y[RPOS[j]])
            if not occ(*cell):
                ok = False
                break
            mon.append(cell)
        if not ok:
            continue
        mon = tuple(sorted(mon))
        out[mon] = out.get(mon, 0) + 1
    return {m: c for m, c in out.items() if c}


def poly_vars(poly):
    s = set()
    for mon in poly:
        s.update(mon)
    return s


# ------------------------------------------------------------------ gauge
# The torus  A_{i,j}[c][d] -> lam[i,c]*mu[j,d]*A_{i,j}[c][d]  multiplies
# per B(x,y) by (prod_i lam[i,x_i])(prod_j mu[j,y_j]), so it preserves the
# whole vanishing problem and the zero pattern.  Nodes of the gauge graph:
# ('L',i,c) and ('R',j,d) -- 24 of them; the cell (i,j,c,d) is the edge
# between ('L',i,c) and ('R',j,d).  Fixing the cells of a SPANNING FOREST to 1
# is a valid slice: bipartite incidence matrices are totally unimodular, so
# the tree equations lam[i,c]*mu[j,d] = 1/A can be solved by walking the tree.
def gauge_nodes(cells):
    ns = set()
    for (i, j, c, d) in cells:
        ns.add(('L', i, c))
        ns.add(('R', j, d))
    return ns


def spanning_forest(cells):
    """Greedy union-find spanning forest over the given cell set.
    Returns (list of chosen cells, n_nodes, n_components)."""
    par = {}

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    for n in gauge_nodes(cells):
        par[n] = n
    chosen = []
    for cell in sorted(cells):
        (i, j, c, d) = cell
        a, b = find(('L', i, c)), find(('R', j, d))
        if a != b:
            par[a] = b
            chosen.append(cell)
    ncomp = len({find(n) for n in par})
    return chosen, len(par), ncomp


def gauge_apply(val, lam, mu):
    return {(i, j, c, d): lam[(i, c)] * mu[(j, d)] * v
            for (i, j, c, d), v in val.items()}


def gauge_to_slice(val, tree):
    """Given an all-nonzero assignment `val` (dict over a cell set) and a
    spanning forest `tree` of that cell set, produce (lam, mu) making every
    tree cell equal 1.  Walks each tree component from a root."""
    adj = {}
    for (i, j, c, d) in tree:
        adj.setdefault(('L', i, c), []).append((('R', j, d), (i, j, c, d)))
        adj.setdefault(('R', j, d), []).append((('L', i, c), (i, j, c, d)))
    scal = {}
    for n in gauge_nodes(val.keys()):
        if n in scal:
            continue
        scal[n] = Fraction(1)
        stack = [n]
        while stack:
            u = stack.pop()
            for (w, cell) in adj.get(u, ()):
                if w in scal:
                    continue
                # want scal[u]*scal[w]*val[cell] == 1
                scal[w] = 1 / (scal[u] * val[cell])
                stack.append(w)
    lam = {(i, c): scal[('L', i, c)] for (kind, i, c) in scal if kind == 'L'}
    mu = {(j, d): scal[('R', j, d)] for (kind, j, d) in scal if kind == 'R'}
    return lam, mu


# ------------------------------------------------------------------ Singular
class SingularError(RuntimeError):
    pass


def check_no_shadowing(varnames, gennames):
    """LEDGER 13 (SEVERE).  `poly g11 = ...` in a ring that HAS a variable
    named g11 silently rebinds -- no warning, return code 0, FALSE KILL."""
    clash = sorted(set(varnames) & set(gennames))
    if clash:
        raise SingularError("generator names shadow ring variables: %s"
                            % clash[:10])
    return len(clash)


def scan_script(script, varnames, gennames):
    """extra L13 guard: no declared identifier may equal a ring variable, and
    no reserved identifier may be used."""
    check_no_shadowing(varnames, gennames)
    reserved = {"e1", "mult", "I", "L", "R", "T", "M", "N", "K", "V", "W"}
    decl = set()
    for ln in script.splitlines():
        s = ln.strip()
        for kw in ("poly ", "ideal ", "list ", "int ", "matrix ", "number "):
            if s.startswith(kw):
                nm = s[len(kw):].split("=")[0].split("(")[0].strip()
                decl.add(nm)
    bad = sorted((decl & set(varnames)) | (decl & reserved))
    if bad:
        raise SingularError("declared identifier shadows ring var / reserved "
                            "word: %s" % bad)
    for ln in script.splitlines():
        s = ln.strip()
        if s.startswith("+"):
            raise SingularError("leading unary + (LEDGER 6): %r" % ln)
    return len(decl)


def run_singular(script, timeout=1800):
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False,
                                     dir=os.path.dirname(
                                         os.path.abspath(__file__))) as fh:
        fh.write(script)
        path = fh.name
    try:
        p = subprocess.run(["Singular", "-q", "--no-warn", path],
                           capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT"
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
    out = p.stdout + p.stderr
    bad = [ln for ln in out.splitlines()
           if ln.strip().startswith("?") or "error occurred" in ln]
    if bad:
        raise SingularError("Singular reported errors (LEDGER 11):\n"
                            + "\n".join(bad[:10])
                            + "\n--- output ---\n" + out[:3000])
    return out, "OK"


def sing_poly(poly, names):
    """poly = {mon tuple : int}.  names = {cell : identifier}.  Cells absent
    from `names` are understood to have been substituted to 1."""
    if not poly:
        return "0"
    terms = []
    for mon, c in sorted(poly.items()):
        fac = [names[v] for v in mon if v in names]
        s = "+" if c > 0 else "-"
        if abs(c) != 1 or not fac:
            s += str(abs(c))
            if fac:
                s += "*"
        s += "*".join(fac)
        terms.append(s)
    out = "".join(terms)
    return out[1:] if out.startswith("+") else out     # LEDGER 6: no lead '+'
