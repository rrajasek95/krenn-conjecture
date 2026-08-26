#!/usr/bin/env python3
"""W29-VAN -- the VANISHING-PATTERN ABSTRACTION of a T1i case (exact, sound,
characteristic-free).

Every generator of a T1i case is a PRODUCT of hafnian factors haf(t^c|S)
(times, in the non-singleton cases, one linear form in the star unknowns).
Introduce a Boolean

        z(c,S)  ==  "haf(t^c|S) = 0"        (S an even subset of V', |S|<=6)

and abstract:

 (V1) z(c, empty) is FALSE                                   (haf of nothing = 1)
 (V2) a generator "product of factors = 0" becomes the CLAUSE
      "some factor vanishes"                                        [sound]
 (V3) LAPLACE.  haf(t^c|S) = sum_{u in S-w} t^c_{wu} haf(t^c|S-w-u) for any
      w in S, so if every term has a vanishing factor then haf(t^c|S) = 0:
          z(c,S)  OR  some u with NOT z(c,{w,u}) and NOT z(c,S-w-u)   [sound]
      (strictly stronger than "some perfect matching survives", because it is
      stated on the abstract z of the 4-sets, which cancellation can switch on)
 (V4) h_c(y_c) != 0 is the unit clause NOT z(c, V'-y_c).

Only IMPLICATIONS that hold at every true point are used, in either
direction, so the abstraction is a RELAXATION:  UNSAT  =>  the case has no
point over ANY field, in ANY characteristic -- a purely combinatorial kill,
with the UNSAT proof as the certificate.  SAT gives a candidate vanishing
pattern that then has to be handled algebraically.
"""
from __future__ import annotations

import sys
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-diagclose-w29-2026-08-19")
if BASE not in sys.path:
    sys.path.insert(0, BASE)
import w29_t1i as T                                                 # noqa: E402

VP = T.VP
YS = T.YS


class Van:
    def __init__(self, case):
        self.case = case
        self.n = 0
        self.lit = {}
        self.cls = []
        self.names = {}

    def new(self, key=None):
        self.n += 1
        if key is not None:
            self.lit[key] = self.n
            self.names[self.n] = key
        return self.n

    def z(self, c, S):
        S = tuple(sorted(S))
        key = ("z", c, S)
        if key not in self.lit:
            v = self.new(key)
            if not S:                       # haf(empty) = 1 -- never zero
                self.cls.append([-v])
        return self.lit[key]

    def var(self, key):
        if key not in self.lit:
            self.new(key)
        return self.lit[key]

    # ---------------------------------------------------------- construction
    def build(self):
        cs = self.case
        for c in range(3):
            for m in (0, 2, 4, 6):
                for S in combinations(VP, m):
                    self.z(c, S)
        # (V3) Laplace expansions
        for c in range(3):
            for m in (4, 6):
                for S in combinations(VP, m):
                    for w in S:
                        big = [self.z(c, S)]
                        for u in S:
                            if u == w:
                                continue
                            rest = tuple(x for x in S if x not in (w, u))
                            q = self.var(("q", c, S, w, u))
                            self.cls.append([-q, -self.z(c, (w, u))])
                            self.cls.append([-q, -self.z(c, rest)])
                            big.append(q)
                        self.cls.append(big)
        # (V2)/(V4) the generators
        gens = cs.build()
        self.gen_tags = []
        for (tag, _poly) in gens:
            kind = tag[0]
            if kind == "FREE":
                _, c, y, S1, S2 = tag
                d, e = [x for x in range(3) if x != c]
                self.cls.append(self._factor_clause([(d, S1), (e, S2)]))
            elif kind == "XFREE":
                _, c, S0, S1, S2 = tag
                d, e = [x for x in range(3) if x != c]
                A = tuple(x for x in S0 if x != YS[c])
                self.cls.append(self._factor_clause(
                    [(d, S1), (e, S2), (c, A)]))
            elif kind == "MIXED":
                _, c, S0, S1, S2 = tag
                d, e = [x for x in range(3) if x != c]
                cl = self._factor_clause([(d, S1), (e, S2)])
                cl.append(self.var(("u", c, S0)))
                self.cls.append(cl)
            elif kind == "NORM":
                c = tag[1]
                self.cls.append([-self.z(c, tuple(x for x in VP
                                                  if x != YS[c]))])
            elif kind == "RAB":
                c = tag[1]
                self.cls.append([-self.z(c, tuple(x for x in VP
                                                  if x != YS[c]))])
                if cs.hasx[c]:
                    self.cls.append([self.var(("xnz", c, YS[c]))])
            elif kind == "RABX":
                c = tag[1]
                self.cls.append([self.var(("xnz", c, YS[c]))])
            elif kind == "CONST":
                c = tag[1]
                big = []
                for y in cs.F[c]:
                    b = self.var(("b", c, y))
                    self.cls.append([-b, -self.z(c, tuple(x for x in VP
                                                          if x != y))])
                    self.cls.append([-b, self.var(("xnz", c, y))])
                    big.append(b)
                self.cls.append(big)
        # link the star linear forms u(c,S0) to their terms
        for c in range(3):
            if not cs.hasx[c]:
                continue
            F = set(cs.F[c])
            for S0 in T.odd_sets():
                inF = sorted(F & set(S0))
                if len(inF) < 1 or ("u", c, S0) not in self.lit:
                    continue
                tns = []
                for y in inF:
                    A = tuple(x for x in S0 if x != y)
                    tn = self.var(("tn", c, S0, y))
                    self.cls.append([-tn, -self.z(c, A)])
                    self.cls.append([-tn, self.var(("xnz", c, y))])
                    self.cls.append([self.z(c, A),
                                     -self.var(("xnz", c, y)), tn])
                    tns.append(tn)
                u = self.var(("u", c, S0))
                for i, tn in enumerate(tns):
                    self.cls.append([-u, -tn] + [t2 for j, t2 in
                                                 enumerate(tns) if j != i])
        return self

    def _factor_clause(self, facs):
        cl = []
        for (c, S) in facs:
            if len(S) == 0:
                continue                    # haf(empty) = 1, never vanishes
            cl.append(self.z(c, S))
        return cl if cl else [1, -1]         # (cannot happen)

    # --------------------------------------------------------------- solving
    def solve(self, budget=1, solver="cadical153"):
        from pysat.solvers import Solver
        out = []
        with Solver(name=solver, bootstrap_with=self.cls) as S:
            while len(out) < budget and S.solve():
                mod = set(S.get_model())
                out.append(self.decode(mod))
                blk = [-l for l in mod if abs(l) in self.names
                       and self.names[abs(l)][0] == "z"]
                if not blk:
                    break
                S.add_clause(blk)
        return out

    def is_unsat(self, solver="cadical153"):
        from pysat.solvers import Solver
        with Solver(name=solver, bootstrap_with=self.cls) as S:
            return not S.solve()

    def decode(self, mod):
        """{'supp': {c: [edges with t^c != 0]}, 'nz4', 'nz6'}"""
        out = {"supp": {}, "nz4": {}, "nz6": {}}
        for c in range(3):
            out["supp"][c] = [S for S in combinations(VP, 2)
                              if -self.lit[("z", c, S)] in mod]
            out["nz4"][c] = [S for S in combinations(VP, 4)
                             if -self.lit[("z", c, S)] in mod]
            out["nz6"][c] = [S for S in combinations(VP, 6)
                             if -self.lit[("z", c, S)] in mod]
        return out


def van_for(Rs, kmax=4, norm=True):
    return Van(T.Case(Rs, kmax=kmax, norm=norm)).build()


__all__ = [n for n in dir() if not n.startswith("_")]
