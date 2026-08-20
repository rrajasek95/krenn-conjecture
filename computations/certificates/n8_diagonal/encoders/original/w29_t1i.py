#!/usr/bin/env python3
"""W29 T1i -- THE THREE-COLOUR FREE-SET CASE SPLIT (the replacement for T1h).

W28-DEC.  For a DIAGONAL background t = (t^0,t^1,t^2) on V' = V - z = {0..6},
colour c is X_4-feasible at z iff there is x in C^{V'} with

  (M)  haf(t^d|S_1) haf(t^e|S_2) * sum_{y in S_0} haf(t^c|S_0 - y) x_y = 0
       for every partition V' = S_0+S_1+S_2, |S_0| odd < 7, |S_1|,|S_2| even,
  (K)  sum_{y in V'} haf(t^c|V' - y) x_y = 1.                 ({d,e} != c)

W28-FREE.  |S_0| = 1 gives haf(t^d|S_1)haf(t^e|S_2) x_y = 0, so x is supported
on the FREE SET  F_c = {y : every even split of V'-y has the product 0}.

NEW HERE
--------
W29-B1 [PROVED-HERE].  y in F_c  =>  haf(t^d|V'-y) = 0 for BOTH d != c
(the split (S_1,S_2) = (V'-y, empty) resp. (empty, V'-y)).

W29-B2 [PROVED-HERE].  Write h_c(y) = haf(t^c|V'-y).  (K) forces some y in
F_c with h_c(y) x_y != 0.  Fix such a y_c for each colour.  By W29-B1,
h_c(y_c) != 0 keeps y_c out of F_d for every d != c, so y_0, y_1, y_2 are
DISTINCT, and moreover  F_c is contained in {y_c} + Q  where Q = V' minus
{y_0,y_1,y_2}.  The diagonal family is S_7-invariant, so WLOG
(y_0,y_1,y_2) = (0,1,2) and Q = {3,4,5,6}:

    ****  THE FREE-SET TRIPLE IS  ({0}+R_0, {1}+R_1, {2}+R_2)  WITH
          R_c SUBSET OF A FIXED 4-SET -- exactly 16^3 = 4096 CASES,
          and the residual symmetry S_4(Q) x S_3(colour) cuts that to a
          few dozen orbits.  ****

That is the case ledger this module builds.  In each case:

  (G1) FREE      haf(t^d|S_1)haf(t^e|S_2),  y in F_c, split of V'-y
  (G2) XFREE     haf(t^d|S_1)haf(t^e|S_2) haf(t^c|S_0-y_c)  for the S_0 with
                 S_0 cap F_c = {y_c}   [legitimate: x_{y_c} != 0 by choice]
  (G3) MIXED     haf(t^d|S_1)haf(t^e|S_2) * sum_{y in S_0 cap F_c}
                 haf(t^c|S_0-y) x_y     for the remaining S_0
  (G4) CONST     sum_{y in F_c} h_c(y) x_y - 1
  (G5) RAB       zr_c * h_c(y_c) * x_{y_c} - 1     (x_{y_c} != 0 AND
                 h_c(y_c) != 0 in one variable)

T1h is the sub-ideal (G1 at y_c only) + (h_c(y_c) != 0): W29-A1 shows THAT is
not the unit ideal, so (G2)-(G5) are exactly what was missing.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations, permutations

W28 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
       "unaudited-x4empty-w28-2026-08-18")
BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-diagclose-w29-2026-08-19")
for p in (BASE, W28):
    if p not in sys.path:
        sys.path.insert(0, p)
import w28_core as K                                                # noqa: E402
import w29_core as C                                                # noqa: E402

NS = 7
VP = tuple(range(NS))
YS = (0, 1, 2)
Q = (3, 4, 5, 6)
EDGES = tuple(combinations(VP, 2))
EIDX = {e: i for i, e in enumerate(EDGES)}
NW = 3 * len(EDGES)                                    # 63 weight parameters


def widx(c, e):
    return 21 * c + EIDX[C.ekey(*e)]


def wname(c, e):
    e = C.ekey(*e)
    return f"zt{c}_{e[0]}{e[1]}"


def offcount8(S0, S1, S2, c):
    """off-count of the 8-site word (colour c at z, S_0 -> c, S_1 -> d, ...)"""
    return 8 - max(len(S0) + 1, len(S1), len(S2))


def even_splits(W):
    out = []
    for m in range(0, len(W) + 1, 2):
        for S1 in combinations(W, m):
            out.append((S1, tuple(x for x in W if x not in S1)))
    return out


def odd_sets(proper=True):
    out = []
    for s in (1, 3, 5, 7):
        if proper and s == NS:
            continue
        out.extend(combinations(VP, s))
    return out


# ------------------------------------------------------------ the case ideal
class Case:
    """norm=True uses the TORUS NORMALISATION instead of Rabinowitsch.

    Every FREE/XFREE/MIXED generator is multi-homogeneous for the grading by
    colour degree (t^c has degree e_c, x^c degree -3 e_c), so the variety is
    invariant under (t^0,t^1,t^2) -> (l_0 t^0, l_1 t^1, l_2 t^2) with
    x^c -> l_c^{-3} x^c.  haf(t^c|V'-y_c) is homogeneous of degree 3 in t^c,
    so over an algebraically closed field "h_c(y_c) != 0" can be normalised to
    "h_c(y_c) = 1" -- ONE 15-term generator and NO extra variable, instead of
    a Rabinowitsch relation.  (Proving "no point over any extension of Q" is
    exactly a statement over the algebraic closure, so this is sound; the
    cube root needed is available there in every characteristic.)
    """

    def __init__(self, Rs, kmax=4, xfree_only=False, norm=True):
        self.Rs = tuple(tuple(sorted(R)) for R in Rs)
        self.F = tuple(tuple(sorted((YS[c],) + self.Rs[c])) for c in range(3))
        self.kmax = kmax
        self.xfree_only = xfree_only
        self.norm = norm
        self.names = [wname(c, e) for c in range(3) for e in EDGES]
        # a colour whose free set is a SINGLETON needs no star unknown at all:
        # x_{y_c} != 0 divides out of every row and CONST becomes h_c(y_c) != 0
        self.hasx = tuple((not xfree_only) and len(self.F[c]) > 1
                          for c in range(3))
        self.xpos = {}
        n = NW
        for c in range(3):
            if self.hasx[c]:
                for y in self.F[c]:
                    self.xpos[(c, y)] = n
                    self.names.append(f"zx{c}_{y}")
                    n += 1
        self.rpos = {}
        for c in range(3):
            if norm and not self.hasx[c]:
                continue          # NORM needs no Rabinowitsch variable here
            self.rpos[c] = n
            self.names.append(f"zr{c}")
            n += 1
        self.nv = n
        self._hc = {}

    # ---- polynomial helpers
    def zero(self):
        return K.Poly.const(self.nv, 0)

    def one(self):
        return K.Poly.const(self.nv, 1)

    def hafp(self, c, S):
        S = tuple(sorted(S))
        key = (c, S)
        if key not in self._hc:
            w = {e: K.Poly.var(self.nv, widx(c, e)) for e in EDGES}
            self._hc[key] = C.haf(w, S, self.zero(), self.one())
        return self._hc[key]

    def xvar(self, c, y):
        return K.Poly.var(self.nv, self.xpos[(c, y)])

    def build(self):
        """[(tag, poly)] -- the full generator list of this case."""
        gens = []
        for c in range(3):
            d, e = [x for x in range(3) if x != c]
            F = set(self.F[c])
            yc = YS[c]
            # ---- (G1) FREE at every hypothesised free site
            for y in sorted(F):
                W = tuple(x for x in VP if x != y)
                for (S1, S2) in even_splits(W):
                    if offcount8((y,), S1, S2, c) > self.kmax:
                        continue
                    g = self.hafp(d, S1) * self.hafp(e, S2)
                    if g.t:
                        gens.append((("FREE", c, y, S1, S2), g))
            # ---- (G2)/(G3) the mixed rows
            for S0 in odd_sets():
                inF = sorted(F & set(S0))
                if not inF:
                    continue
                R = tuple(x for x in VP if x not in S0)
                for (S1, S2) in even_splits(R):
                    if offcount8(S0, S1, S2, c) > self.kmax:
                        continue
                    P = self.hafp(d, S1) * self.hafp(e, S2)
                    if not P.t:
                        continue
                    if inF == [yc]:
                        g = P * self.hafp(c, tuple(x for x in S0 if x != yc))
                        if g.t:
                            gens.append((("XFREE", c, S0, S1, S2), g))
                    elif self.hasx[c]:
                        q = self.zero()
                        for y in inF:
                            q = q + self.hafp(
                                c, tuple(x for x in S0 if x != y)) \
                                * self.xvar(c, y)
                        if q.t:
                            g = P * q
                            if g.t:
                                gens.append((("MIXED", c, S0, S1, S2), g))
            # ---- (G4) the constant equation
            if self.hasx[c]:
                q = self.zero()
                for y in sorted(F):
                    q = q + self.hafp(c, tuple(x for x in VP if x != y)) \
                        * self.xvar(c, y)
                gens.append((("CONST", c), q - self.one()))
            # ---- (G5) h_c(y_c) != 0, as a normalisation or a Rabinowitsch
            hc = self.hafp(c, tuple(x for x in VP if x != yc))
            if self.norm:
                gens.append((("NORM", c), hc - self.one()))
                if c in self.rpos:
                    gens.append((("RABX", c),
                                 K.Poly.var(self.nv, self.rpos[c])
                                 * self.xvar(c, yc) - self.one()))
            else:
                r = K.Poly.var(self.nv, self.rpos[c]) * hc
                if self.hasx[c]:
                    r = r * self.xvar(c, yc)
                gens.append((("RAB", c), r - self.one()))
        return gens


# --------------------------------------------------------- symmetry / orbits
def case_orbit_reps():
    """Orbits of (R_0,R_1,R_2), R_c subset of Q, under S_4(Q) x S_3(colours)."""
    allR = [tuple(S) for k in range(5) for S in combinations(Q, k)]
    seen, reps = set(), []
    for R0 in allR:
        for R1 in allR:
            for R2 in allR:
                trip = (R0, R1, R2)
                if trip in seen:
                    continue
                orb = set()
                for sig in permutations(Q):
                    m = dict(zip(Q, sig))
                    img = tuple(tuple(sorted(m[y] for y in R))
                                for R in trip)
                    for pi in permutations(range(3)):
                        orb.add(tuple(img[pi[i]] for i in range(3)))
                seen |= orb
                reps.append((trip, len(orb)))
    return reps


# ------------------------------------------------------------- Singular glue
def emit(polys, names, char, method="std", timeout_note=""):
    polys = K.clear_denoms(list(polys))[0]
    lines = [f"ring zzR = {char}, ({','.join(names)}), dp;",
             "option(redSB);",
             "ideal zzJ = " + ",\n  ".join(p.sing(names) for p in polys) + ";"]
    if method == "slimgb":
        lines.append("ideal zzG = slimgb(zzJ);")
    elif method == "modStd":
        lines.append('LIB "modstd.lib";')
        lines.append("ideal zzG = modStd(zzJ);")
    else:
        lines.append("ideal zzG = std(zzJ);")
    lines += ['"NGENS "; size(zzG);',
              '"ISUNIT "; int zzu = 0; if (size(zzG)==1 and zzG[1]==1)'
              ' { zzu = 1; } zzu;',
              '"DIM "; dim(zzG);']
    sc = "\n".join(lines)
    C.no_shadow_guard(sc, set(names))
    return sc


def decide(polys, names, char, method="std", timeout=1800):
    out = C.run_singular(emit(polys, names, char, method), timeout=timeout)
    tk = out.split()
    return {"isunit": tk[tk.index("ISUNIT") + 1],
            "dim": tk[tk.index("DIM") + 1],
            "ngens_std": tk[tk.index("NGENS") + 1],
            "char": char, "method": method}


def compress(polys, names):
    """Drop the variables that do not occur (ring compression)."""
    used = set()
    for p in polys:
        for k2 in p.t:
            for i, e in enumerate(k2):
                if e:
                    used.add(i)
    used = sorted(used)
    nvc = len(used)
    out = [K.Poly(nvc, {tuple(k2[v] for v in used): val
                        for k2, val in p.t.items()}) for p in polys]
    return out, [names[v] for v in used]


__all__ = [n for n in dir() if not n.startswith("_")]
