#!/usr/bin/env python3
"""W26 ADVERSARIAL LANE -- shared exact machinery.  UNAUDITED.

EXACT ONLY.  Every number here is a fractions.Fraction, a sympy exact
object, or an element of a small exact extension ring implemented below.
NO FLOATS ANYWHERE.

Contents
  * Q2   : exact ring Q[t]/(t^2+t+1)      (omega = primitive cube root of 1)
  * Qi   : exact ring Q[t]/(t^2+1)        (i)
  * Fp   : exact prime field F_p
  * generic-ring phi / coeff wrappers (w26_core is ring-generic already)
  * independent verification of a point straight from C.H_word
"""
from __future__ import annotations

import os
import sys
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.dirname(HERE)
sys.path.insert(0, UP)
sys.path.insert(0, HERE)
import w26_core as C                                              # noqa: E402
import w26_pts as PT                                             # noqa: E402
import w26_sub as SB                                             # noqa: E402

F = Fraction


# --------------------------------------------------------- extension rings
class _Ext:
    """Q[t]/(t^2 - A t - B):  x = c0 + c1 t."""
    A = F(0)
    B = F(0)
    NAME = "?"
    __slots__ = ("c0", "c1")

    def __init__(self, c0=0, c1=0):
        self.c0 = F(c0)
        self.c1 = F(c1)

    @classmethod
    def _mk(cls, x):
        if isinstance(x, cls):
            return x
        return cls(x, 0)

    def __add__(self, o):
        o = self._mk(o)
        return type(self)(self.c0 + o.c0, self.c1 + o.c1)
    __radd__ = __add__

    def __neg__(self):
        return type(self)(-self.c0, -self.c1)

    def __sub__(self, o):
        return self + (-self._mk(o))

    def __rsub__(self, o):
        return self._mk(o) + (-self)

    def __mul__(self, o):
        o = self._mk(o)
        # (a+bt)(c+dt) = ac + (ad+bc) t + bd t^2, t^2 = A t + B
        a, b, c, d = self.c0, self.c1, o.c0, o.c1
        return type(self)(a * c + b * d * type(self).B,
                          a * d + b * c + b * d * type(self).A)
    __rmul__ = __mul__

    def inv(self):
        # conjugate wrt t -> A - t
        a, b = self.c0, self.c1
        cj = type(self)(a + b * type(self).A, -b)
        nm = (self * cj)
        assert nm.c1 == 0, nm
        assert nm.c0 != 0, "zero divisor / not invertible"
        return type(self)(cj.c0 / nm.c0, cj.c1 / nm.c0)

    def __truediv__(self, o):
        return self * self._mk(o).inv()

    def __rtruediv__(self, o):
        return self._mk(o) * self.inv()

    def __eq__(self, o):
        try:
            o = self._mk(o)
        except Exception:
            return NotImplemented
        return self.c0 == o.c0 and self.c1 == o.c1

    def __ne__(self, o):
        r = self.__eq__(o)
        return r if r is NotImplemented else (not r)

    def __hash__(self):
        return hash((self.c0, self.c1, type(self).NAME))

    def __bool__(self):
        return self.c0 != 0 or self.c1 != 0

    def __repr__(self):
        return "%s(%s,%s)" % (type(self).NAME, self.c0, self.c1)

    def __str__(self):
        return "%s%+s*%s" % (self.c0, self.c1, type(self).NAME)


class Q2(_Ext):
    """omega^2 = -omega - 1  =>  t^2 = -t - 1  (A=-1, B=-1)."""
    A = F(-1)
    B = F(-1)
    NAME = "w"


class Qi(_Ext):
    """i^2 = -1  =>  t^2 = 0*t + (-1)."""
    A = F(0)
    B = F(-1)
    NAME = "i"


class Fp:
    """exact prime field F_p (p prime)."""
    __slots__ = ("v", "p")

    def __init__(self, v, p):
        self.p = p
        self.v = int(v) % p

    def _mk(self, x):
        return x if isinstance(x, Fp) else Fp(x, self.p)

    def __add__(self, o):
        return Fp(self.v + self._mk(o).v, self.p)
    __radd__ = __add__

    def __neg__(self):
        return Fp(-self.v, self.p)

    def __sub__(self, o):
        return Fp(self.v - self._mk(o).v, self.p)

    def __rsub__(self, o):
        return Fp(self._mk(o).v - self.v, self.p)

    def __mul__(self, o):
        return Fp(self.v * self._mk(o).v, self.p)
    __rmul__ = __mul__

    def __truediv__(self, o):
        o = self._mk(o)
        assert o.v != 0, "division by zero in F_%d" % self.p
        return Fp(self.v * pow(o.v, self.p - 2, self.p), self.p)

    def __rtruediv__(self, o):
        return self._mk(o) / self

    def __eq__(self, o):
        if isinstance(o, Fp):
            return self.v == o.v and self.p == o.p
        if isinstance(o, int):
            return self.v == o % self.p
        if isinstance(o, Fraction):
            return o.denominator == 1 and self.v == int(o) % self.p
        return NotImplemented

    def __ne__(self, o):
        r = self.__eq__(o)
        return r if r is NotImplemented else (not r)

    def __hash__(self):
        return hash((self.v, self.p))

    def __bool__(self):
        return self.v != 0

    def __lt__(self, o):
        return self.v < self._mk(o).v

    def __repr__(self):
        return "%d_%d" % (self.v, self.p)


def fp_ring(p):
    return Fp(0, p), Fp(1, p)


# --------------------------------------------------------------- helpers
def zero_one(bl):
    """detect the coefficient ring from a block dict."""
    x = bl[sorted(bl)[0]][0][0]
    if isinstance(x, Fp):
        return Fp(0, x.p), Fp(1, x.p)
    if isinstance(x, _Ext):
        return type(x)(0, 0), type(x)(1, 0)
    return F(0), F(1)


def phi_g(bl, gs, w):
    z, o = zero_one(bl)
    return C.haf_on(bl, gs, tuple(range(8)), w, z, o)


def coeff_g(bl, gs, e, w):
    z, o = zero_one(bl)
    rest = tuple(v for v in range(8) if v not in e)
    return C.haf_on(bl, gs, rest, w, z, o)


def all_nonzero(bl):
    return all(bl[e][i][j] != 0 for e in bl for i in range(3)
               for j in range(3))


def is_clean_g(m, bl):
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    if not all_nonzero(bl):
        return False
    return all(phi_g(bl, gs, w) == 0 for w in C.clean_words(m))


def vanishing_g(m, bl):
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    return all(phi_g(bl, gs, w) == 0 for w in C.WORDS)


def solo_report_g(m, bl, e):
    """ring-generic clone of SB.solo_report (identical logic)."""
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    z, _ = zero_one(bl)
    pure = badconst = 0
    ratios = set()
    for w in SB.solo_words(m, e):
        c = coeff_g(bl, gs, e, w)
        p = phi_g(bl, gs, w)
        if c == 0:
            if p != 0:
                badconst += 1
            continue
        r = (z - p) / c
        ratios.add(r)
        if r == 0:
            pure += 1
    return dict(n_solo=len(SB.solo_words(m, e)), n_pure=pure,
                n_badconst=badconst, n_distinct_ratios=len(ratios),
                ratios=[str(r) for r in list(ratios)[:4]],
                killed=bool(pure or badconst or len(ratios) > 1),
                survives=(not pure and not badconst and len(ratios) == 1
                          and not any(r == 0 for r in ratios)))


def case2b_g(m, bl):
    U, V = bl[(5, 6)], bl[(6, 7)]
    n02 = n01 = 0
    for y5 in range(3):
        for y7 in range(3):
            if U[y5][0] * V[2][y7] - U[y5][2] * V[0][y7] == 0:
                n02 += 1
            if U[y5][1] * V[0][y7] - U[y5][0] * V[1][y7] == 0:
                n01 += 1
    return (n02 == 9 and n01 == 0), n02, n01


# ------------------------------------------- INDEPENDENT verification path
def phi_from_Hword(m, bl, w):
    """Phi(w) recomputed from the RAW 105-matching definition C.H_word with
    every single set to 0 (then only the Gamma matchings survive)."""
    T = C.TEMPLATES[m]
    z = {e: F(0) for e in C.single_edges(T)}
    return C.H_word(bl, T, z, w)


def coeff_from_Hword(m, bl, e, w):
    """c_e(w) from the raw definition: H(z=1_e) - H(z=0).
    NOTE this equals c_e(w) only at words where e is ACTIVE (otherwise no
    matching can use e at all and the difference is 0)."""
    T = C.TEMPLATES[m]
    z0 = {f: F(0) for f in C.single_edges(T)}
    z1 = dict(z0)
    z1[e] = F(1)
    return C.H_word(bl, T, z1, w) - C.H_word(bl, T, z0, w)


def is_active(m, e, w):
    cell = C.single_edges(C.TEMPLATES[m])[e]
    return w[e[0]] == cell[0] and w[e[1]] == cell[1]


def independent_verify(m, bl, verbose=True):
    """re-derive EVERYTHING from C.H_word over all 6558 mixed words +
    the 3 constant words.  Returns a dict of raw-definition facts."""
    T = C.TEMPLATES[m]
    clean = set(C.clean_words(m))
    z0 = {e: F(0) for e in C.single_edges(T)}
    nz_clean = 0
    nz_any = 0
    phis = {}
    for w in C.WORDS:
        h = C.H_word(bl, T, z0, w)
        phis[w] = h
        if h != 0:
            nz_any += 1
            if w in clean:
                nz_clean += 1
    ok_cells = all(bl[e][i][j] != 0 for e in C.gamma_edges(T)
                   for i in range(3) for j in range(3))
    out = dict(all_gamma_cells_nonzero=ok_cells,
               n_clean_words=len(clean),
               n_clean_words_with_Phi_nonzero=nz_clean,
               n_words_with_Phi_nonzero_of_6561=nz_any,
               is_clean_point_rawdef=(ok_cells and nz_clean == 0),
               identically_vanishing_rawdef=(nz_any == 0))
    if verbose:
        print("  [H_word raw definition] Gamma cells all nonzero : %s"
              % ok_cells)
        print("  [H_word raw definition] clean words with Phi!=0 : %d / %d"
              % (nz_clean, len(clean)))
        print("  [H_word raw definition] words with Phi!=0       : %d / 6561"
              % nz_any)
    return out, phis


def cross_check_helpers(m, bl, nsample=None):
    """assert C.phi / C.coeff agree with the raw C.H_word route."""
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    ws = C.WORDS if nsample is None else C.WORDS[::max(1, 6561 // nsample)]
    bad = 0
    for w in ws:
        if C.phi(bl, gs, w) != phi_from_Hword(m, bl, w):
            bad += 1
    badc = ncmp = 0
    for e in C.live_singles(m):
        for w in ws:
            if not is_active(m, e, w):
                continue                    # H_word cannot see c_e there
            ncmp += 1
            if C.coeff(bl, gs, e, w) != coeff_from_Hword(m, bl, e, w):
                badc += 1
    return bad, badc, ncmp


# ------------------------------------------------------------ serialising
def dump_point(bl):
    return {str(e): [[str(x) for x in row] for row in bl[e]]
            for e in sorted(bl)}


def load_point(d):
    return {tuple(int(t) for t in k.strip("()").split(",")):
            [[F(x) for x in row] for row in v] for k, v in d.items()}


def mutate(bl, e, i, j, delta=F(1)):
    nb = {f: [r[:] for r in bl[f]] for f in bl}
    nb[e][i][j] = nb[e][i][j] + delta
    return nb


def blocks_grid(m):
    return C.gamma_edges(C.TEMPLATES[m])


def outer(x, y):
    return [[x[i] * y[j] for j in range(3)] for i in range(3)]
