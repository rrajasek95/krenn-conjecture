#!/usr/bin/env python3
"""W28 -- symmetric backgrounds on K_7 and the AVERAGING REDUCTION.

Site z = 7 is the solve site; the background lives on V' = {0,...,6}.

GROUP-SYMMETRIC BACKGROUNDS.  A symmetry is a pair (pi, rho) with pi a
permutation of V' and rho a permutation of the 3 colours; the background is
(pi, rho)-symmetric iff

        B_{pi(u) pi(v)}[rho(i)][rho(j)] = B_{uv}[i][j]      (for ordered u,v)

together with the standing convention B_{vu} = B_{uv}^T.  Given generators we
close the group, split the 42 ordered pairs into orbits, pair each orbit with
its transpose-orbit, and build the background from one free 3x3 matrix per
transpose-pair of orbits (an orbit that is its own transpose-partner would
impose a linear condition; we ASSERT that case away and verify invariance of
every constructed background explicitly).

    sigma-slice  (W27)  sigma = (0 1 2)(3 4 5)(6), rho = (0 1 2)  ->  7 blocks
    Z_7-slice           pi = (x -> x+1),           rho = id       ->  3 blocks
    F_21-slice          the above PLUS (x -> 2x, rho)             ->  1 block

W28-SYM (the averaging lemma).  Let H be a group of symmetries with TRIVIAL
colour action (rho = id) acting transitively on V'.  The colour-c system at z
is H-equivariant with an H-invariant right-hand side, so if it has a solution
it has an H-invariant one; transitivity makes an invariant star constant,
x_{y,d} = x_d.  Hence

    colour-c system feasible  <=>  the THREE-unknown averaged system
        sum_d  ( sum_{y : u_y = d} C_y(u) )  x_d  =  [u constant]
    is consistent,

where u ranges over the words on V' whose extension by c at z is
k-near-constant.  Both directions are checked numerically in run_t1a.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x4empty-w28-2026-08-18")
if BASE not in sys.path:
    sys.path.insert(0, BASE)
import w28_core as K                                              # noqa: E402

NS = 7                      # background sites 0..6
Z = 7                       # the solve site
N = 8


# ------------------------------------------------------------------- groups

def close_group(gens, ns=NS):
    """Closure of (site perm as tuple, colour perm as tuple) generators."""
    ident = (tuple(range(ns)), (0, 1, 2))
    seen = {ident}
    frontier = [ident]
    while frontier:
        g = frontier.pop()
        for h in gens:
            comp = (tuple(h[0][g[0][i]] for i in range(ns)),
                    tuple(h[1][g[1][i]] for i in range(3)))
            if comp not in seen:
                seen.add(comp)
                frontier.append(comp)
    return sorted(seen)


def pair_orbits(group, ns=NS):
    """Orbits of ORDERED pairs (u,v), u != v, under the group."""
    pairs = [(u, v) for u in range(ns) for v in range(ns) if u != v]
    seen, orbs = set(), []
    for p in pairs:
        if p in seen:
            continue
        orb = set()
        for (pi, rho) in group:
            orb.add((pi[p[0]], pi[p[1]]))
        seen |= orb
        orbs.append(sorted(orb))
    return orbs


class Slice:
    """A group-symmetric family of backgrounds on K_7."""

    def __init__(self, name, gens, ns=NS):
        self.name = name
        self.ns = ns
        self.group = close_group(gens, ns)
        self.orbs = pair_orbits(self.group, ns)
        # pair each orbit with its transpose-orbit
        omap = {}
        for i, o in enumerate(self.orbs):
            for p in o:
                omap[p] = i
        self.reps = []                  # list of orbit indices carrying a free block
        used = set()
        for i, o in enumerate(self.orbs):
            if i in used:
                continue
            j = omap[(o[0][1], o[0][0])]
            K.require(j != i, f"{name}: transpose-stable orbit (unsupported)")
            used.add(i)
            used.add(j)
            self.reps.append(i)
        self.nblocks = len(self.reps)
        self.nparam = 9 * self.nblocks
        # precompute, for each ordered pair, (block index, colour perm, transpose?)
        self.rule = {}
        for bi, i in enumerate(self.reps):
            u0, v0 = self.orbs[i][0]
            for (pi, rho) in self.group:
                a, b = pi[u0], pi[v0]
                # B_{a b}[rho i][rho j] = M[i][j]
                for key, val in (((a, b), (bi, rho, False)),
                                 ((b, a), (bi, rho, True))):
                    old = self.rule.get(key)
                    K.require(old is None or old == val,
                              f"{name}: non-free action at {key} "
                              f"({old} vs {val}) -- would impose a linear "
                              f"condition on the free block")
                    self.rule[key] = val
        K.require(len(self.rule) == ns * (ns - 1),
                  f"{name}: rule incomplete {len(self.rule)}")

    def build(self, blocks):
        """blocks[bi] = 3x3 matrix (the free parameter block)."""
        src = {}
        for (a, b), (bi, rho, tr) in self.rule.items():
            if a > b:
                continue
            M = blocks[bi]
            out = [[None] * 3 for _ in range(3)]
            for i in range(3):
                for j in range(3):
                    if tr:
                        out[rho[j]][rho[i]] = M[i][j]
                    else:
                        out[rho[i]][rho[j]] = M[i][j]
            src[(a, b)] = out
        return src

    def check(self, src):
        """Number of violated symmetry equations (must be 0)."""
        bad = 0
        for (pi, rho) in self.group:
            for u in range(self.ns):
                for v in range(self.ns):
                    if u == v:
                        continue
                    A = K.oriented(src, u, v)
                    Bm = K.oriented(src, pi[u], pi[v])
                    for i in range(3):
                        for j in range(3):
                            if Bm[rho[i]][rho[j]] != A[i][j]:
                                bad += 1
        return bad


def cyc7(k=1):
    return tuple((x + k) % 7 for x in range(7))


def mul7(a=2):
    return tuple((x * a) % 7 for x in range(7))


SIGMA_W27 = (1, 2, 0, 4, 5, 3, 6)          # (0 1 2)(3 4 5)(6)
RHO = (1, 2, 0)


def slice_sigma():
    return Slice("sigma331", [(SIGMA_W27, RHO)])


def slice_z7():
    return Slice("Z7", [(cyc7(1), (0, 1, 2))])


def slice_f21():
    return Slice("F21", [(cyc7(1), (0, 1, 2)), (mul7(2), RHO)])


#  NOTE: attaching rho to the 7-CYCLE itself generates (id, rho) (7 = 1 mod 3),
#  which forces circulant blocks -- a linear condition on the free block, so
#  that slice is not of the "one free block per transpose-pair" shape and is
#  excluded here on purpose.


# --------------------------------------------------- words / averaged system

def word_orbits(group, ns=NS):
    """Group orbits on words u in {0,1,2}^7 ((g.u)_{pi(y)} = rho(u_y)).
    Returns one representative per orbit."""
    seen, reps = set(), []
    for u in product(range(3), repeat=ns):
        if u in seen:
            continue
        orb = set()
        for (pi, rho) in group:
            v = [0] * ns
            for y in range(ns):
                v[pi[y]] = rho[u[y]]
            orb.add(tuple(v))
        seen |= orb
        reps.append(u)
    return reps


def constrained_u(c, k=4, ns=NS):
    """Words u on V' whose extension by colour c at z is k-near-constant and
    MIXED, plus (first) the constant one."""
    out = []
    const = (c,) * ns
    for u in product(range(3), repeat=ns):
        w = u + (c,)
        if K.offcount(w) > k:
            continue
        out.append(u)
    out.sort(key=lambda u: (u != const, sum(1 for x in u if x != c), u))
    K.require(out[0] == const, "constant word missing")
    return out


def cof_all(src, u, sample=None):
    """C_y(u) = Haf over V' \\ {y} at word u, for y in V'."""
    if sample is None:
        sample = src[(0, 1)][0][0]
    out = []
    for y in range(NS):
        S = tuple(x for x in range(NS) if x != y)
        out.append(K.haf_on(src, {a: u[a] for a in S}, S))
    return out


def averaged_rows(src, c, k=4, uorder=None):
    """[(row3, rhs)] for the averaged (3-unknown) colour-c system."""
    if uorder is None:
        uorder = constrained_u(c, k)
    zz = K.zeroe(src[(0, 1)][0][0])
    out = []
    for u in uorder:
        cof = cof_all(src, u)
        row = [zz, zz, zz]
        for y in range(NS):
            row[u[y]] = row[u[y]] + cof[y]
        out.append((row, 1 if all(x == c for x in u) else 0))
    return out


def averaged_feasible(src, c, k=4, uorder=None, early=True):
    """Exact feasibility of the averaged 3-unknown system.

    Returns (feasible, rank_mixed, rconst).  Mixed rows first; the moment the
    mixed rank hits 3 the system is infeasible (only x = 0 solves it)."""
    if uorder is None:
        uorder = constrained_u(c, k)
    const = (c,) * NS
    rows = []
    rconst = None
    for u in uorder:
        cof = cof_all(src, u)
        row = [Fraction(0)] * 3
        for y in range(NS):
            row[u[y]] = row[u[y]] + cof[y]
        if u == const:
            rconst = row
            continue
        if any(x != 0 for x in row):
            rows.append(row)
            if early and _rank3(rows) == 3:
                return False, 3, rconst
    r = _rank3(rows)
    if rconst is None or all(x == 0 for x in rconst):
        return False, r, rconst
    return (_rank3(rows + [rconst]) > r), r, rconst


def _rank3(rows):
    m = [list(r) for r in rows]
    rk = 0
    for c in range(3):
        p = None
        for i in range(rk, len(m)):
            if m[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        m[rk], m[p] = m[p], m[rk]
        pv = m[rk][c]
        for i in range(len(m)):
            if i != rk and m[i][c] != 0:
                f = m[i][c] / pv
                m[i] = [a - f * b for a, b in zip(m[i], m[rk])]
        rk += 1
    return rk


# ------------------------------------------------- the full 21-unknown system

def full_feasible(src8, c, k=4, n=N, z=Z):
    """Exact feasibility of the colour-c 21-unknown system at z (background
    given as an 8-site source whose blocks at z are irrelevant)."""
    rows, rhs, tags, cols = K.site_rows_exact(src8, z, c, n, k)
    part, kern = K.rref_solve(rows, rhs, len(cols))
    return part is not None, (None if part is None else len(kern))


def lift(src7, n=N):
    """Background on K_7 -> 8-site source with zero blocks at z."""
    out = K.zero_source(n)
    for e, m in src7.items():
        out[e] = [r[:] for r in m]
    return out
