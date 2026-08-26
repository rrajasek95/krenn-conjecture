#!/usr/bin/env python3
"""UNAUDITED PROBE W40 (Route B successor to W33) -- core.

Pinned HEAD: see PINNED_HEAD.txt.

INHERITS the W33 engine verbatim (bitmask subset DP `haf`, the explicit-PM
control engine `haf_pm`, star matrices/kernels, gauge action, Singular
hygiene, Manifest).  Nothing in w33_core is re-implemented here; this file
adds only the d=3 layer W40 needs:

  * `d5_point()`      -- the W33-D5 twisted 4+4 exact d=2 source (explicit).
  * `delta2_point()`  -- the Hamiltonian PM-pair Delta^2 source (calibration
                         background: a completion to an X_3 point EXISTS).
  * `off`, `words3`   -- the level-k system X_k of the N=8 campaign
                         (off(w) = N - max_c |w^{-1}(c)|; X_k imposes
                         off(w) <= k).
  * `Sym`             -- a minimal exact sparse multivariate polynomial ring
                         over Q (dict monomial -> Fraction) used to expand
                         hafnians whose cells are affine in the unknowns.
  * `completion_system` -- the third-colour completion generators over a
                         FIXED two-colour background.

SETTING.  A d=3 source on K_8 assigns A_uv (3x3), A_vu = A_uv^T.  X_k is the
system  H_w = 1 (w constant), H_w = 0 (off(w) <= k, w non-constant).
By W32-2COL every 2-colour restriction of an X_4 point at N=8 is an exact
d=2 source.  W40 asks the converse question for the ONE named dangerous
d=2 source: can the W33-D5 twisted 4+4 be the {0,1} restriction of an X_4
point?

THE TWO LINEAR LAYERS (inherited, W32 run_22 / W33 t11).  Words with EXACTLY
one site coloured 2 are all imposed at k=4 (the other seven sites split into
two colours, so some colour occurs >= 4 times, so off <= 4).  Such a word at
site j gives exactly the homogeneous star system of the {0,1} background at
j.  Hence:  the colour-2 star at j, i.e. the vector
(A_jr[2][e])_{r != j, e in {0,1}}, must lie in Ker_j of the background.
"""
from __future__ import annotations

import itertools
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
W33 = os.path.join(os.path.dirname(HERE), "unaudited-x4general-w33-2026-08-20")
sys.path.insert(0, W33)

from w33_core import (  # noqa: E402  (inherited engine, unmodified)
    Fp, Manifest, apply_perm, apply_swap, apply_torus, cell, copy_source,
    cycle_pm_pair, defects2, edges, ekey, haf, haf_pm, is_exact2,
    no_shadow_guard, nullspace, n_cross, one_like, require, rref,
    run_singular, setcell, star_kernel, star_matrix, support, words2,
    zero_like, zero_source,
)

N = 8
EDG = edges(N)


# --------------------------------------------------------------- d=2 seeds

def d5_point(sample=None):
    """W33-D5 / W33 t12: the twisted 4+4.

    Diagonal support = two disjoint 4-cycles 0-1-2-3-0 and 4-5-6-7-4, each
    alternating colour 0 / colour 1; plus exactly four CROSSING cross cells
    between the two cycles.  Stored verbatim from
    unaudited-x4general-w33-2026-08-20/results_SUMMARY.json ->
    t12_new_44_family.explicit_point.
    """
    src = zero_source(N, 2, sample)
    one = Fraction(1) if sample is None else one_like(sample)
    for (u, v, c) in ((0, 1, 0), (2, 3, 0), (4, 5, 0), (6, 7, 0),
                      (0, 3, 1), (1, 2, 1), (4, 7, 1), (5, 6, 1)):
        setcell(src, u, v, c, c, one)
    setcell(src, 0, 4, 0, 1, one)
    setcell(src, 0, 5, 1, 0, one)
    setcell(src, 1, 7, 0, 1, -one)
    setcell(src, 3, 4, 1, 0, -one)
    return src


D5_DIAG_CYCLES = ((0, 1, 2, 3), (4, 5, 6, 7))
D5_CROSS = (((0, 4), 0, 1), ((0, 5), 1, 0), ((1, 7), 0, 1), ((3, 4), 1, 0))


def delta2_point(sample=None):
    """Delta^2 on the 8-cycle 0-1-...-7-0 (the CALIBRATION background: the
    block-diagonal PM-triple X_3 point restricts to it)."""
    return cycle_pm_pair(N, sample=sample)


# ----------------------------------------------------------- the X_k system

def off(w):
    return N - max(w.count(c) for c in range(3))


def words3(k, need_colour=None):
    """All w in {0,1,2}^8 with off(w) <= k (optionally: containing colour
    `need_colour`)."""
    out = []
    for w in itertools.product(range(3), repeat=N):
        if off(w) > k:
            continue
        if need_colour is not None and need_colour not in w:
            continue
        out.append(w)
    return out


def pm_all(vs):
    vs = list(vs)
    if not vs:
        return [()]
    h, rest = vs[0], vs[1:]
    out = []
    for i, x in enumerate(rest):
        for M in pm_all(rest[:i] + rest[i + 1:]):
            out.append((ekey(h, x),) + M)
    return out


PMS = [tuple(sorted(M)) for M in pm_all(range(N))]
require(len(PMS) == 105, "PM count")


# --------------------------------------------- sparse exact polynomial ring

class Sym:
    """Sparse multivariate polynomial over Q.  Monomial = sorted tuple of
    variable indices with repetition (total degree <= 4 here)."""

    __slots__ = ("t",)

    def __init__(self, t=None):
        self.t = dict(t) if t else {}

    @staticmethod
    def const(c):
        c = Fraction(c)
        return Sym({(): c}) if c != 0 else Sym()

    @staticmethod
    def var(i):
        return Sym({(i,): Fraction(1)})

    def __bool__(self):
        return bool(self.t)

    def __add__(self, o):
        r = dict(self.t)
        for m, c in o.t.items():
            nc = r.get(m, Fraction(0)) + c
            if nc:
                r[m] = nc
            else:
                r.pop(m, None)
        return Sym(r)

    def __mul__(self, o):
        r = {}
        for m1, c1 in self.t.items():
            for m2, c2 in o.t.items():
                m = tuple(sorted(m1 + m2))
                nc = r.get(m, Fraction(0)) + c1 * c2
                if nc:
                    r[m] = nc
                else:
                    r.pop(m, None)
        return Sym(r)

    def scale(self, c):
        c = Fraction(c)
        if c == 0:
            return Sym()
        return Sym({m: v * c for m, v in self.t.items()})

    def subtract_const(self, c):
        return self + Sym.const(-Fraction(c))

    def evaluate(self, vals):
        tot = Fraction(0)
        for m, c in self.t.items():
            p = c
            for i in m:
                p *= vals[i]
            tot += p
        return tot

    def clear_denoms(self):
        """Integer-coefficient copy (ledger 22: Singular's parser rejects
        sympy-style rationals; and the target is homogeneous per generator
        up to the constant term, so scaling changes no verdict ONLY when the
        generator is homogeneous -- here we scale the WHOLE generator
        including its constant, which is a unit multiple, so the ideal is
        unchanged)."""
        from math import gcd
        den = 1
        for c in self.t.values():
            den = den * c.denominator // gcd(den, c.denominator)
        num = 0
        out = {}
        for m, c in self.t.items():
            v = c * den
            require(v.denominator == 1, "denominator not cleared")
            out[m] = int(v)
            num = gcd(num, abs(int(v)))
        if num > 1:
            out = {m: v // num for m, v in out.items()}
        return out

    def to_singular(self, names):
        ints = self.clear_denoms()
        if not ints:
            return "0"
        parts = []
        for m, c in sorted(ints.items()):
            mon = "*".join(names[i] for i in m)
            if not mon:
                parts.append(f"{c}")
            elif c == 1:
                parts.append(mon)
            elif c == -1:
                parts.append(f"-{mon}")
            else:
                parts.append(f"{c}*{mon}")
        s = parts[0]
        for p in parts[1:]:
            s += p if p.startswith("-") else "+" + p
        return s

    def ndeg(self):
        return max((len(m) for m in self.t), default=0)


# ----------------------------------------- the third-colour completion data

def kernel_bases(bg, sample=None):
    """Per site j: (cols, basis) of Ker_j of the two-colour background."""
    out = {}
    for j in range(N):
        dim, basis, cols, zcols = star_kernel(bg, j, N, sample=sample)
        out[j] = {"dim": dim, "basis": basis, "cols": cols, "zcols": zcols}
    return out


def build_variables(kb):
    """Free variables: the kernel coefficients lam[j][i] (site j, basis
    vector i) and the pure colour-2 diagonal weights q[e] (e an edge).
    Returns (names, ncell, qidx, lamidx)."""
    names, lamidx = [], {}
    for j in range(N):
        for i in range(kb[j]["dim"]):
            lamidx[(j, i)] = len(names)
            names.append(f"zzv({len(names) + 1})")
    qidx = {}
    for e in EDG:
        qidx[e] = len(names)
        names.append(f"zzv({len(names) + 1})")
    return names, lamidx, qidx


def cell_forms(bg, kb, lamidx, qidx):
    """cellf[(u, v)][a][b] : Sym for the (a,b) cell of A_uv in the d=3
    source, with the {0,1} block FIXED to the background and the colour-2
    row/column carried by the free variables.  Convention as in w33_core:
    index a is the colour at u, b the colour at v."""
    cf = {e: [[Sym() for _ in range(3)] for _ in range(3)] for e in EDG}
    for (u, v) in EDG:
        for a in range(2):
            for b in range(2):
                cf[(u, v)][a][b] = Sym.const(cell(bg, u, v, a, b))
        cf[(u, v)][2][2] = Sym.var(qidx[(u, v)])
    # colour-2 star at j: coefficients over columns (r, e)
    for j in range(N):
        cols = kb[j]["cols"]
        for i, vec in enumerate(kb[j]["basis"]):
            t = Sym.var(lamidx[(j, i)])
            for ci, (r, e) in enumerate(cols):
                c = vec[ci]
                if c == 0:
                    continue
                term = t.scale(c)
                if j < r:
                    cf[(j, r)][2][e] = cf[(j, r)][2][e] + term
                else:
                    cf[(r, j)][e][2] = cf[(r, j)][e][2] + term
    return cf


def haf_sym(cf, w, sites=None):
    """H_w as a Sym, by explicit PM enumeration over `sites` (default all 8).
    Deliberately the CONTROL engine's code path (haf_pm), so the generator
    construction is cross-checkable against the DP engine `haf` at points."""
    if sites is None:
        mask = (1 << N) - 1
    else:
        mask = 0
        for s in sites:
            mask |= 1 << s
    tot = Sym()
    for M in PMS:
        m = 0
        for (u, v) in M:
            m |= (1 << u) | (1 << v)
        if m != mask:
            continue
        pr = Sym.const(1)
        for (u, v) in M:
            f = cf[(u, v)][w[u]][w[v]]
            if not f:
                pr = Sym()
                break
            pr = pr * f
        if pr:
            tot = tot + pr
    return tot


def completion_generators(cf, k, skip_pure_bg=True):
    """The X_k generators of the d=3 completion over a fixed background.
    Words entirely in {0,1} are satisfied identically by the background
    (checked separately by a control), so they are skipped."""
    gens, meta = [], []
    for w in words3(k):
        if skip_pure_bg and 2 not in w:
            continue
        tgt = 1 if len(set(w)) == 1 else 0
        g = haf_sym(cf, w).subtract_const(tgt)
        if not g.t:
            continue
        gens.append(g)
        meta.append(w)
    return gens, meta


def singular_decide(gens, names, base, timeout, want_dim=False,
                    extra=""):
    body = ",\n ".join(g.to_singular(names) for g in gens)
    script = (f"ring R = {base}, (zzv(1..{len(names)})), dp;\n"
              f"ideal zzI = {body};\n"
              "ideal zzG = std(zzI);\n"
              '"UNIT:", (size(zzG) == 1 && zzG[1] == 1);\n'
              + ('"DIM:", dim(zzG);\n' if want_dim else "") + extra)
    no_shadow_guard(script, set(names))
    txt = run_singular(script, timeout=timeout)
    out = {}
    for ln in txt.splitlines():
        ln = ln.strip()
        for key in ("UNIT", "DIM", "EVAL", "NF"):
            if ln.startswith(key + ":"):
                out[key] = ln.split(":", 1)[1].strip()
    require("UNIT" in out, f"parse failure: {txt[:400]}")
    return out


def sing_rat(x):
    """Emit a rational constant for Singular.

    W40 HAZARD (new; sibling of ledger 22, and worse because it is SILENT):
    inside a `poly`/`ideal` context Singular parses a PARENTHESISED quotient
    as POLYNOMIAL division and truncates it --

        poly a = (1)/(2);   ==>  a == 0      (rc 0, no '?' line)
        poly a = 1/2;       ==>  a == 1/2    (correct)

    So the natural "(num)/(den)" spelling of a rational point silently
    substitutes ZERO for every non-integral coordinate.  In an
    explicit-point control that can manufacture a FALSE PASS whenever the
    generators are homogeneous in the zeroed coordinates (every term dies),
    as well as the false alarm that exposed it here.  Always emit the bare
    form, and never a parenthesised quotient.
    """
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else \
        f"{x.numerator}/{x.denominator}"


def rational_emission_guard(timeout=120):
    """Mandatory pre-flight control for this hazard: Singular must reproduce
    a known rational product through the exact emission path used below."""
    vals = [Fraction(-2), Fraction(1, 2), Fraction(-2), Fraction(1, 2)]
    sub = ",".join(sing_rat(v) for v in vals)
    script = ("ring R = 0, (zzv(1..4)), dp;\n"
              "poly zzf = zzv(1)*zzv(2)*zzv(3)*zzv(4)-1;\n"
              f"ideal zzP = {sub};\n"
              "map zzM = R, zzP;\n"
              "poly zzg = zzM(zzf);\n"
              '"UNIT:", 0;\n'
              '"NF:", string(zzg);\n')
    no_shadow_guard(script, {f"zzv({i})" for i in range(1, 5)})
    txt = run_singular(script, timeout=timeout)
    nf = None
    for ln in txt.splitlines():
        if ln.strip().startswith("NF:"):
            nf = ln.split(":", 1)[1].strip()
    require(nf == "0", f"RATIONAL EMISSION GUARD FAILED: got {nf!r} for "
                       f"(-2)(1/2)(-2)(1/2)-1, expected 0")
    return True


def singular_eval_point(gens, names, vals, timeout=900):
    """Ledger 13(b)/27: evaluate the EXACT target generators at a stored
    point inside Singular (independent of the Python expander).  Returns the
    number of generators that do NOT vanish."""
    rational_emission_guard()
    body = ",\n ".join(g.to_singular(names) for g in gens)
    sub = ",".join(sing_rat(vals[i]) for i in range(len(names)))
    script = (f"ring R = 0, (zzv(1..{len(names)})), dp;\n"
              f"ideal zzI = {body};\n"
              f"ideal zzP = {sub};\n"
              "map zzM = R, zzP;\n"
              "ideal zzE = zzM(zzI);\n"
              '"UNIT:", 0;\n'
              '"PCOLS:", ncols(zzP);\n'
              '"EVAL:", size(simplify(zzE,2));\n')
    no_shadow_guard(script, set(names))
    txt = run_singular(script, timeout=timeout)
    got = {}
    for ln in txt.splitlines():
        for k in ("EVAL", "PCOLS"):
            if ln.strip().startswith(k + ":"):
                got[k] = int(ln.split(":", 1)[1].strip())
    require(got.get("PCOLS") == len(names),
            f"substitution vector truncated: {got}")
    require("EVAL" in got, "EVAL parse failure")
    return got["EVAL"]


def install_d3(cf, vals):
    """Materialise the d=3 source at a point (list of Fractions)."""
    src = {e: [[Fraction(0)] * 3 for _ in range(3)] for e in EDG}
    for e in EDG:
        for a in range(3):
            for b in range(3):
                src[e][a][b] = cf[e][a][b].evaluate(vals)
    return src


def haf3(src, w):
    """H_w for a d=3 source, via the INHERITED DP engine."""
    return haf(src, w, n=N, sample=Fraction(0))
