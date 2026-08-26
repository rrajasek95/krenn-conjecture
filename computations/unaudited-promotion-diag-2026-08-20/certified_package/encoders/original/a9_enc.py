#!/usr/bin/env python3
"""A9 AUDIT -- INDEPENDENT re-encoding of the W29 vanishing-pattern abstraction.

Nothing is imported from W29.  Own variable layout: bitmask-keyed, and the
POLARITY IS INVERTED w.r.t. W29 (their z(c,S) = "haf = 0"; my p(c,S) =
"haf(t^c|S) != 0"), so a sign slip in either encoder shows up as a mismatch.

DERIVATION (re-done by hand for this audit; see REPORT).  Diagonal source on
K_N, weights t^0,t^1,t^2 on the edges, H_w = prod_c haf(t^c|w^{-1}(c)).
EXACT: haf(t^c|V) = 1 and every mixed ordered even partition has product 0.
X_k: only the words of off-count N - max|part| <= k are imposed.

Solve site z; V' = V-z; x^c_y := t^c_{zy} = haf(t^c|{z,y}).
 W28-FREE   |S_0| = {y}: x^c_y haf(t^d|S_1) haf(t^e|S_2) = 0 for every even
            split of V'-y  =>  x^c_y = 0 unless y in F_c^{(k)}.
 W29-B1     y in F_c => haf(t^d|V'-y) = 0 for both d != c (split (V'-y, [])).
 W29-B2     haf(t^c|V) = sum_y x^c_y haf(t^c|V'-y) = 1 forces some y_c in F_c
            with x^c_{y_c} != 0 and h_c(y_c) != 0; B1 then makes y_0,y_1,y_2
            distinct and F_c subset {y_c} + Q.

CLAUSES (each a one-line implication valid at EVERY true point of EVERY case
over EVERY field -- the only facts used are "a field has no zero divisors",
"1 != 0", and haf(empty) = 1):

 A0   p(c, [])                                haf of nothing is 1
 A1   p(c, V)                                 haf(t^c|V) = 1 != 0
 A2   -p(0,S_0) v -p(1,S_1) v -p(2,S_2)       mixed even partition, off <= k
 A3   -p(c,S) v OR_u g(c,S,w,u)               Laplace at w in S, |S| >= 4
      g -> p(c,{w,u}),  g -> p(c,S-w-u)
 C0   -p(c,{z,y})            y in V' - F_c    W28-FREE support
 Cnz  p(c,{z,y_c})                            B2 choice
 Ch   p(c, V - z - y_c)                       B2 choice
 FR   -p(d,S_1) v -p(e,S_2)                   y in F_c, even split of V'-y,
                                              off <= k
 XF   p(c, S_0 + z)  <->  p(c, S_0 - y_c)     S_0 odd, S_0 cap F_c = {y_c}
"""
from __future__ import annotations

import itertools
import subprocess

TOOLS = ("/Users/rishi/workplace/krenn-conjecture/computations/"
         "unaudited-hygiene-h1-2026-08-15/tools")
CADICAL = f"{TOOLS}/cadical/build/cadical"
DRATTRIM = f"{TOOLS}/drat-trim/drat-trim"


def bits(mask):
    out = []
    i = 0
    while mask:
        if mask & 1:
            out.append(i)
        mask >>= 1
        i += 1
    return tuple(out)


def mask_of(S):
    m = 0
    for x in S:
        m |= 1 << x
    return m


def popcount(m):
    return bin(m).count("1")


class Enc:
    """CNF for one case (Rs) at order n, level k, solve site z."""

    def __init__(self, n, Rs, k=None, z=None, ys=(0, 1, 2),
                 use=("A0", "A1", "A2", "A3", "C0", "Cnz", "Ch", "FR", "XF")):
        self.n = n
        self.k = k
        self.z = n - 1 if z is None else z
        self.ys = ys
        self.use = set(use)
        self.V = tuple(range(n))
        self.VP = tuple(x for x in self.V if x != self.z)
        self.F = tuple(sorted(set([ys[c]]) | set(Rs[c])) for c in range(3))
        self.Rs = tuple(tuple(sorted(R)) for R in Rs)
        self.nv = 0
        self.vmap = {}
        self.vname = {}
        self.cls = []
        self.tags = []

    # -------------------------------------------------------------- vars
    def _v(self, key):
        if key not in self.vmap:
            self.nv += 1
            self.vmap[key] = self.nv
            self.vname[self.nv] = key
        return self.vmap[key]

    def p(self, c, S):
        """literal for  haf(t^c|S) != 0  (S a tuple or a bitmask)."""
        m = S if isinstance(S, int) else mask_of(S)
        return self._v(("p", c, m))

    def g(self, c, m, w, u):
        return self._v(("g", c, m, w, u))

    def add(self, tag, cl):
        self.cls.append(tuple(cl))
        self.tags.append(tag)

    # ------------------------------------------------------------ builder
    def offcount(self, sizes):
        return self.n - max(sizes)

    def keep(self, sizes):
        return self.k is None or self.offcount(sizes) <= self.k

    def build(self):
        n, V, z, VP = self.n, self.V, self.z, self.VP
        full = (1 << n) - 1
        evens = [m for m in range(1 << n) if popcount(m) % 2 == 0]
        # --- A0 / A1
        for c in range(3):
            if "A0" in self.use:
                self.add(("A0", c), [self.p(c, 0)])
            if "A1" in self.use:
                self.add(("A1", c), [self.p(c, full)])
        # --- A3 Laplace
        if "A3" in self.use:
            for c in range(3):
                for m in evens:
                    if popcount(m) < 4:
                        continue
                    el = bits(m)
                    for w in el:
                        big = [-self.p(c, m)]
                        for u in el:
                            if u == w:
                                continue
                            gv = self.g(c, m, w, u)
                            self.add(("A3g", c, m, w, u),
                                     [-gv, self.p(c, (1 << w) | (1 << u))])
                            self.add(("A3g", c, m, w, u),
                                     [-gv, self.p(c, m & ~((1 << w) | (1 << u)))])
                            big.append(gv)
                        self.add(("A3", c, m, w), big)
        # --- A2 the exactness rows (all mixed even ordered partitions)
        if "A2" in self.use:
            for a in evens:
                rest = full & ~a
                sub = rest
                seen = set()
                # iterate subsets of rest
                s = rest
                while True:
                    if popcount(s) % 2 == 0:
                        b = s
                        cmask = rest & ~b
                        if popcount(cmask) % 2 == 0:
                            parts = (a, b, cmask)
                            sizes = [popcount(x) for x in parts]
                            if max(sizes) != n and self.keep(sizes):
                                cl = [-self.p(cc, parts[cc]) for cc in range(3)
                                      if parts[cc]]
                                self.add(("A2", parts), cl)
                    if s == 0:
                        break
                    s = (s - 1) & rest
        # --- the case hypothesis
        for c in range(3):
            yc = self.ys[c]
            Fc = set(self.F[c])
            if "C0" in self.use:
                for y in VP:
                    if y not in Fc:
                        self.add(("C0", c, y), [-self.p(c, (1 << z) | (1 << y))])
            if "Cnz" in self.use:
                self.add(("Cnz", c), [self.p(c, (1 << z) | (1 << yc))])
            if "Ch" in self.use:
                self.add(("Ch", c), [self.p(c, full & ~((1 << z) | (1 << yc)))])
            # --- FREE
            if "FR" in self.use:
                d, e = [x for x in range(3) if x != c]
                for y in sorted(Fc):
                    W = tuple(x for x in VP if x != y)
                    wm = mask_of(W)
                    s = wm
                    while True:
                        if popcount(s) % 2 == 0:
                            s1, s2 = s, wm & ~s
                            sizes = [2, popcount(s1), popcount(s2)]
                            if self.keep(sizes):
                                cl = []
                                if s1:
                                    cl.append(-self.p(d, s1))
                                if s2:
                                    cl.append(-self.p(e, s2))
                                assert cl, "empty FREE clause -- would be a kill"
                                self.add(("FR", c, y, s1, s2), cl)
                        if s == 0:
                            break
                        s = (s - 1) & wm
            # --- XF
            if "XF" in self.use:
                vpm = mask_of(VP)
                s = vpm
                while True:
                    if popcount(s) % 2 == 1:
                        inF = [y for y in bits(s) if y in Fc]
                        if inF == [yc]:
                            a = self.p(c, s & ~(1 << yc))
                            b = self.p(c, s | (1 << z))
                            self.add(("XF", c, s), [-a, b])
                            self.add(("XF", c, s), [a, -b])
                    if s == 0:
                        break
                    s = (s - 1) & vpm
        return self

    # ------------------------------------------------------------ solving
    def dimacs(self):
        head = f"p cnf {self.nv} {len(self.cls)}\n"
        body = "".join(" ".join(map(str, cl)) + " 0\n" for cl in self.cls)
        return head + body

    def solve_pysat(self, solver="cadical195"):
        from pysat.solvers import Solver
        with Solver(name=solver, bootstrap_with=[list(c) for c in self.cls]) as S:
            sat = S.solve()
            return sat, (set(S.get_model()) if sat else None)

    def solve_cadical(self, path, proof=None, timeout=600):
        with open(path, "w") as fh:
            fh.write(self.dimacs())
        cmd = [CADICAL, "-q"] + (["--no-binary"] if proof else []) + \
            [path] + ([proof] if proof else [])
        pr = subprocess.run(cmd, capture_output=True, text=True,
                            timeout=timeout)
        out = pr.stdout
        if pr.returncode == 20 or "s UNSATISFIABLE" in out:
            return "UNSAT", out
        if pr.returncode == 10 or "s SATISFIABLE" in out:
            return "SAT", out
        raise RuntimeError(f"cadical rc={pr.returncode} out={out[:400]} "
                           f"err={pr.stderr[:400]}")

    def drat_check(self, cnf, proof, timeout=1200):
        pr = subprocess.run([DRATTRIM, cnf, proof, "-f"], capture_output=True,
                            text=True, timeout=timeout)
        ok = "s VERIFIED" in pr.stdout
        return ok, pr.stdout.strip().splitlines()[-3:]

    # -------------------------------------------- validity at a real point
    def truth(self, ts, haf):
        """Assignment induced by a REAL diagonal source ts (dict of edges)."""
        A = {}
        for v, key in self.vname.items():
            if key[0] == "p":
                _, c, m = key
                A[v] = (haf(ts[c], bits(m)) != 0)
            else:
                _, c, m, w, u = key
                A[v] = (ts[c].get((min(w, u), max(w, u)), 0) != 0 and
                        haf(ts[c], bits(m & ~((1 << w) | (1 << u)))) != 0)
        return A

    def violations(self, A):
        bad = []
        for tag, cl in zip(self.tags, self.cls):
            if not any((lit > 0) == A[abs(lit)] for lit in cl):
                bad.append((tag, [self.vname[abs(l)] for l in cl]))
        return bad
