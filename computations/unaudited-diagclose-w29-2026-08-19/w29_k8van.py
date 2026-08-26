#!/usr/bin/env python3
"""W29-K8VAN -- the vanishing-pattern abstraction of the WHOLE diagonal N = 8
problem (no site solve, no free-set case split, no normalisation).

A DIAGONAL source on K_8 is three symmetric weight functions T^0,T^1,T^2 on
the 28 edges of V = {0,...,7}.  For a word w the matching sum factorises,
H_w = prod_c haf(T^c | w^{-1}(c)), so the source is EXACT iff

  (P)  haf(T^c|V) = 1                                    for c = 0,1,2
  (M)  haf(T^0|S_0) haf(T^1|S_1) haf(T^2|S_2) = 0        for every ordered
       partition V = S_0+S_1+S_2 other than the three all-in-one ones.

A part of odd size contributes 0 automatically, so only the even profiles
(8,0,0), (6,2,0), (4,4,0), (4,2,2) carry content; each has a part of size >= 4,
i.e. off-count <= 4, so at N = 8 EXACT = X_4 for diagonal sources.

ABSTRACTION.  Boolean  Z(c,S) == "haf(T^c|S) = 0"  for every even S:

 (A0) Z(c, empty) is FALSE                                 (haf of nothing = 1)
 (A1) NOT Z(c, V)                                                       from (P)
 (A2) each (M) becomes the clause "some nonempty part has a vanishing hafnian"
 (A3) LAPLACE, for every w in S:  haf(T^c|S) = sum_u T^c_{wu} haf(T^c|S-w-u),
      so  Z(c,S) OR (some u with T^c_{wu} != 0 AND haf(T^c|S-w-u) != 0).

Every clause is an implication valid at every true point, in every
characteristic, so the abstraction is a RELAXATION: UNSAT proves that no
diagonal exact source exists on K_8 over ANY field.
"""
from __future__ import annotations

from itertools import combinations

NV = 8
V8 = tuple(range(NV))


class K8Van:
    def __init__(self, n=NV, ncol=3, prof_filter=None):
        self.n = n
        self.ncol = ncol
        self.prof_filter = prof_filter
        self.nvars = 0
        self.lit = {}
        self.names = {}
        self.cls = []
        self.tagged = []          # (tag, clause) for core extraction

    def new(self, key):
        self.nvars += 1
        self.lit[key] = self.nvars
        self.names[self.nvars] = key
        return self.nvars

    def z(self, c, S):
        S = tuple(sorted(S))
        key = ("z", c, S)
        if key not in self.lit:
            self.new(key)
        return self.lit[key]

    def add(self, tag, cl):
        self.cls.append(cl)
        self.tagged.append((tag, cl))

    def build(self):
        V = tuple(range(self.n))
        evens = [S for m in range(0, self.n + 1, 2)
                 for S in combinations(V, m)]
        for c in range(self.ncol):
            for S in evens:
                self.z(c, S)
            self.add(("A0", c), [-self.z(c, ())])
            self.add(("A1", c), [-self.z(c, V)])
        # (A3) Laplace
        for c in range(self.ncol):
            for S in evens:
                if len(S) < 4:
                    continue
                for w in S:
                    big = [self.z(c, S)]
                    for u in S:
                        if u == w:
                            continue
                        rest = tuple(x for x in S if x not in (w, u))
                        key = ("q", c, S, w, u)
                        if key not in self.lit:
                            self.new(key)
                        q = self.lit[key]
                        self.add(("A3q", c, S, w, u),
                                 [-q, -self.z(c, (min(w, u), max(w, u)))])
                        self.add(("A3q", c, S, w, u), [-q, -self.z(c, rest)])
                        big.append(q)
                    self.add(("A3", c, S, w), big)
        # (A2) the partition conditions
        for S0 in evens:
            R = [x for x in V if x not in S0]
            for m in range(0, len(R) + 1, 2):
                for S1 in combinations(R, m):
                    S2 = tuple(x for x in R if x not in S1)
                    parts = (S0, S1, S2)
                    if any(len(p) == self.n for p in parts):
                        continue
                    if self.prof_filter and not self.prof_filter(parts):
                        continue
                    cl = [self.z(c, parts[c]) for c in range(self.ncol)
                          if parts[c]]
                    self.add(("A2", S0, S1, S2), cl)
        return self

    def add_case(self, Rs, ys=(0, 1, 2), Qs=(3, 4, 5, 6), z=7):
        """The W29-B2 free-set case hypothesis, as unit clauses on K_8.

        Solve at site z.  The colour-c star entries are T^c_{z y} = x^c_y, and
        W28-FREE says x^c is supported on the free set F_c; W29-B2 normalises
        F_c = {y_c} + R_c with R_c inside Q and y_c = c, and picks y_c with
        x^c_{y_c} != 0 and h_c(y_c) = haf(T^c | V - z - y_c) != 0.  So:

            Z(c,{z,y}) is TRUE   for every y not in F_c        (x^c_y = 0)
            Z(c,{z,y_c}) is FALSE                          (x^c_{y_c} != 0)
            Z(c, V-z-y_c) is FALSE                            (h_c(y_c) != 0)

        Nothing is asserted about y in R_c: x^c_y may or may not vanish.
        """
        V = tuple(range(self.n))
        for c in range(self.ncol):
            F = set([ys[c]]) | set(Rs[c])
            for y in V:
                if y == z:
                    continue
                if y not in F:
                    self.add(("CASE0", c, y), [self.z(c, (min(y, z),
                                                          max(y, z)))])
            self.add(("CASEnz", c),
                     [-self.z(c, (min(ys[c], z), max(ys[c], z)))])
            self.add(("CASEh", c),
                     [-self.z(c, tuple(x for x in V
                                       if x not in (z, ys[c])))])
        return self

    def add_free(self, Rs, ys=(0, 1, 2), z=7):
        """W28-FREE, asserted for the whole hypothesised free set.

        y in F_c means EVERY even split (S_1,S_2) of V'-y has
        haf(T^d|S_1) haf(T^e|S_2) = 0 -- this is a property of the free SET,
        so it holds for the y in R_c as well, even where x^c_y = 0 makes the
        partition clause vacuous.  This is the information add_case cannot
        see, and it is what makes the abstraction bite.
        """
        V = tuple(range(self.n))
        VP = tuple(x for x in V if x != z)
        for c in range(self.ncol):
            d, e = [x for x in range(self.ncol) if x != c]
            for y in sorted(set([ys[c]]) | set(Rs[c])):
                W = tuple(x for x in VP if x != y)
                for m in range(0, len(W) + 1, 2):
                    for S1 in combinations(W, m):
                        S2 = tuple(x for x in W if x not in S1)
                        cl = []
                        if S1:
                            cl.append(self.z(d, S1))
                        if S2:
                            cl.append(self.z(e, S2))
                        if cl:
                            self.add(("FREE", c, y, S1, S2), cl)
        return self

    def add_xfree(self, Rs, ys=(0, 1, 2), z=7):
        """x^c_{y_c} != 0 collapses a whole family of hafnians.

        If S_0 (odd, inside V') meets F_c only in y_c then
        haf(T^c | {z} + S_0) = x^c_{y_c} haf(T^c | S_0 - y_c), so the two
        vanish together -- a BICONDITIONAL the Laplace rule cannot derive.
        """
        V = tuple(range(self.n))
        VP = tuple(x for x in V if x != z)
        for c in range(self.ncol):
            F = set([ys[c]]) | set(Rs[c])
            for s in (1, 3, 5, 7):
                for S0 in combinations(VP, s):
                    if sorted(F & set(S0)) != [ys[c]]:
                        continue
                    A = tuple(x for x in S0 if x != ys[c])
                    B = tuple(sorted(S0 + (z,)))
                    za, zb = self.z(c, A), self.z(c, B)
                    self.add(("XF", c, S0), [-za, zb])
                    self.add(("XF", c, S0), [za, -zb])
        return self

    # ------------------------------------------------------------- solving
    def is_unsat(self, solver="cadical153", clauses=None):
        from pysat.solvers import Solver
        with Solver(name=solver,
                    bootstrap_with=self.cls if clauses is None
                    else clauses) as S:
            return not S.solve()

    def model(self, solver="cadical153"):
        from pysat.solvers import Solver
        with Solver(name=solver, bootstrap_with=self.cls) as S:
            if not S.solve():
                return None
            return set(S.get_model())

    def decode(self, mod):
        out = {}
        for c in range(self.ncol):
            out[c] = {"supp": [list(S) for S in combinations(range(self.n), 2)
                               if -self.lit[("z", c, S)] in mod],
                      "nz4": [list(S) for S in
                              combinations(range(self.n), 4)
                              if -self.lit[("z", c, S)] in mod],
                      "nz6": [list(S) for S in
                              combinations(range(self.n), 6)
                              if -self.lit[("z", c, S)] in mod]}
        return out


def offcount_ok(parts, kmax):
    return NV - max(len(p) for p in parts) <= kmax


__all__ = [n for n in dir() if not n.startswith("_")]
