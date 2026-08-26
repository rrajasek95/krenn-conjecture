#!/usr/bin/env python3
"""W16 -- general gauge-fixed relaxed Phi-forcing engine for m = 25..28.

Phi(x,y) = sum over EVEN S subset L of  (prod_{i in S} c_i) *
           haf_L(L\\S)(x) * haf_R(R\\sigma S)(y),
c_i = A_{i,sigma(i)}[x_i][y_{sigma(i)}]  (0 if that cross edge is not in
Gamma), sigma = {0:7, 1:4, 2:5, 3:6}.  haf_L(L) = P_L(x) is REPLACED by a
free variable lam_x -- a sound RELAXATION (it drops the constraints linking
the four L-words through A02/A13/... , so the system can only get weaker;
a "forced" verdict therefore still holds for the true source).

GAUGE (diagonal rescaling, preserves the template): a valid sequential
chain is emitted per m and CHECKED (the checker recomputes the required
lambda's from a random exact point and verifies the normalisation lands).

VERDICT: if Phi at a mixed word with exactly ONE extra lies in
sat(I_clean, product of the occupied Gamma cells), that extra -- a product
of occupied cells -- is forced to vanish: contradiction.  KILL.
"""
from __future__ import annotations
import os, sys, json, itertools, time
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w16_core import (W8_IMMUNE, EDGES, EIDX, VarMap, phi_poly, peval,
                      full_pm_indices, extras_at, padd, pmul, psub, MIXED)
from w16_sing import run_singular

HERE = os.path.dirname(os.path.abspath(__file__))
L = (0, 1, 2, 3)
R = (4, 5, 6, 7)
SIG = {0: 7, 1: 4, 2: 5, 3: 6}


class Model:
    def __init__(self, m, gauge=True):
        self.m = m
        self.T = W8_IMMUNE[m]
        self.gamma = set(EDGES[i] for i, t in enumerate(self.T) if t == 511)
        self.fullm = full_pm_indices(self.T)
        self.fixed = {}                     # (edge, i, j) -> "1"
        if gauge:
            self._gauge()

    def ing(self, u, v):
        return (min(u, v), max(u, v)) in self.gamma

    def name(self, u, v, i, j):
        e = (min(u, v), max(u, v))
        if (u, v) != e:
            i, j = j, i
        if (e, i, j) in self.fixed:
            return "1"
        return "a%d%d_%d%d" % (e[0], e[1], i, j)

    def _fix(self, u, v, i, j):
        e = (min(u, v), max(u, v))
        if (u, v) != e:
            i, j = j, i
        self.fixed[(e, i, j)] = "1"

    def _gauge(self):
        # vertices 4,5,7 always normalise on their cross edge
        for c in range(3):
            self._fix(1, 4, 2, c)          # A14[2][c] = 1   (vertex 4)
            self._fix(2, 5, 0, c)          # A25[0][c] = 1   (vertex 5)
            self._fix(0, 7, 1, c)          # A07[1][c] = 1   (vertex 7)
        if self.m >= 26:                   # edge 36 is in Gamma
            for c in range(3):
                self._fix(3, 6, 2, c)      # A36[2][c] = 1   (vertex 6)
            for x3 in (0, 1):
                self._fix(3, 6, x3, 0)     # vertex 3
        else:
            for c in range(3):
                self._fix(6, 7, c, 0)      # A67[c][0] = 1   (vertex 6)
            for x3 in range(3):
                self._fix(0, 3, 0, x3)     # A03[0][x3] = 1  (vertex 3)
        for x1 in (0, 1):
            self._fix(1, 4, x1, 0)         # vertex 1
        for x2 in (1, 2):
            self._fix(2, 5, x2, 0)         # vertex 2
        for x0 in (0, 2):
            self._fix(0, 7, x0, 0)         # vertex 0

    # ---------------------------------------------------------- hafnians
    def hafL(self, S, x):
        rest = tuple(v for v in L if v not in S)
        if len(rest) == 4:                  # the full L hafnian -> free lam_x
            return "lam%d%d%d%d" % tuple(x)
        if len(rest) == 0:
            return "1"
        k, l = rest
        return self.name(k, l, x[k], x[l]) if self.ing(k, l) else None

    def hafR(self, S, y):
        rest = tuple(sorted(SIG[v] for v in L if v not in S))
        if len(rest) == 4:                  # the full R hafnian
            terms = []
            for pairing in (((4, 5), (6, 7)), ((4, 6), (5, 7)),
                            ((4, 7), (5, 6))):
                if all(self.ing(*p) for p in pairing):
                    terms.append("*".join(
                        self.name(p[0], p[1], y[p[0] - 4], y[p[1] - 4])
                        for p in pairing))
            return "(" + "+".join(terms) + ")" if terms else None
        if len(rest) == 0:
            return "1"
        p, q = rest
        return self.name(p, q, y[p - 4], y[q - 4]) if self.ing(p, q) else None

    def phi(self, x, y):
        terms = []
        for size in (0, 2, 4):
            for S in itertools.combinations(L, size):
                hl = self.hafL(S, x)
                if hl is None:
                    continue
                hr = self.hafR(S, y)
                if hr is None:
                    continue
                cs = []
                bad = False
                for i in S:
                    if not self.ing(i, SIG[i]):
                        bad = True
                        break
                    cs.append(self.name(i, SIG[i], x[i], y[SIG[i] - 4]))
                if bad:
                    continue
                parts = [p for p in cs + [hl, hr] if p != "1"]
                terms.append("*".join(parts) if parts else "1")
        return "(" + "+".join(terms) + ")" if terms else "0"

    def variables(self, exprs):
        import re
        vs = set()
        for e in exprs:
            vs.update(re.findall(r"[a-z]+[0-9_]*", e))
        return sorted(vs)

    def cell_vars(self, exprs):
        return [v for v in self.variables(exprs) if v.startswith("a")]


# ------------------------------------------------------------- controls
def control_phi(m, seeds=(3, 11, 777)):
    """the symbolic Phi (with lam -> P_L) must equal w16_core's Phi.

    Run WITHOUT the gauge so that every cell is a live symbol."""
    M = Model(m, gauge=False)
    T = M.T
    vm = VarMap(T)
    def lcg(s0):
        s = s0
        while True:
            s = (1103515245 * s + 12345) % (1 << 31)
            yield s
    bad = tested = 0
    for seed in seeds:
        r = lcg(seed)
        def rn():
            return Fraction((next(r) % 15) - 7 or 4, (next(r) % 6) + 1)
        blocks = {e: [[rn() for _ in range(3)] for _ in range(3)]
                  for e in M.gamma}
        env = {}
        for e in M.gamma:
            for i in range(3):
                for j in range(3):
                    env["a%d%d_%d%d" % (e[0], e[1], i, j)] = blocks[e][i][j]
        vals = {}
        for ei, e in enumerate(EDGES):
            if T[ei] != 511:
                continue
            for c in range(9):
                vals[vm.v(ei, c)] = blocks[e][c // 3][c % 3]
        for x in itertools.product(range(3), repeat=4):
            PL = sum(blocks[(0, 1)][x[0]][x[1]] * blocks[(2, 3)][x[2]][x[3]]
                     for _ in [0]) \
                + blocks[(0, 2)][x[0]][x[2]] * blocks[(1, 3)][x[1]][x[3]] \
                + blocks[(0, 3)][x[0]][x[3]] * blocks[(1, 2)][x[1]][x[2]]
            env["lam%d%d%d%d" % tuple(x)] = PL
            for y in itertools.product(range(3), repeat=4):
                expr = M.phi(x, y)
                got = eval(expr.replace("^", "**"),
                           {"__builtins__": {}}, dict(env, **{"1": 1}))
                want = peval(phi_poly(T, vm, tuple(x) + tuple(y), M.fullm),
                             vals)
                tested += 1
                if got != want:
                    bad += 1
    return dict(tested=tested, mismatches=bad)


def gauge_control(m, seed=9):
    """the gauge chain must be achievable: recompute the lambdas and check."""
    M = Model(m)
    def lcg(s0):
        s = s0
        while True:
            s = (1103515245 * s + 12345) % (1 << 31)
            yield s
    r = lcg(seed)
    def rn():
        return Fraction((next(r) % 15) - 7 or 4, (next(r) % 6) + 1)
    B = {e: [[rn() for _ in range(3)] for _ in range(3)] for e in M.gamma}
    lam = {(t, c): Fraction(1) for t in range(8) for c in range(3)}
    def val(u, v, i, j):
        e = (min(u, v), max(u, v))
        if (u, v) != e:
            i, j = j, i
        return B[e][i][j] * lam[(e[0], i)] * lam[(e[1], j)]
    order = []
    for c in range(3):
        order += [(4, c, (1, 4), 2, c), (5, c, (2, 5), 0, c),
                  (7, c, (0, 7), 1, c)]
    order += [(1, x1, (1, 4), x1, 0) for x1 in (0, 1)]
    order += [(2, x2, (2, 5), x2, 0) for x2 in (1, 2)]
    order += [(0, x0, (0, 7), x0, 0) for x0 in (0, 2)]
    if m >= 26:
        order += [(6, c, (3, 6), 2, c) for c in range(3)]
        order += [(3, x3, (3, 6), x3, 0) for x3 in (0, 1)]
    else:
        order += [(6, c, (6, 7), c, 0) for c in range(3)]
        order += [(3, x3, (0, 3), 0, x3) for x3 in range(3)]
    for (t, c, e, i, j) in order:
        cur = val(e[0], e[1], i, j)
        assert cur != 0
        lam[(t, c)] = lam[(t, c)] / cur
        assert val(e[0], e[1], i, j) == 1, (t, c, e, i, j)
    bad = 0
    for ((e, i, j), _) in M.fixed.items():
        if val(e[0], e[1], i, j) != 1:
            bad += 1
    return dict(normalised_cells=len(M.fixed), not_landing=bad)


def main():
    out = {}
    for m in (25, 26, 27, 28):
        out[m] = dict(phi_control=control_phi(m, seeds=(3,)),
                      gauge_control=gauge_control(m))
        print("m=%d  Phi control %s   gauge control %s"
              % (m, out[m]["phi_control"], out[m]["gauge_control"]))
    json.dump(out, open(os.path.join(HERE, "results_gen_controls.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()


# --------------------------------------------------------- forcing driver
def clean_ys(M, x):
    """R-words y with (x,y) EFFECTIVELY clean (exact criterion)."""
    return [y for y in itertools.product(range(3), repeat=4)
            if not extras_at(M.T, tuple(x) + tuple(y), M.fullm)]


def kmapM(M):
    return {w: len(extras_at(M.T, w, M.fullm))
            for w in itertools.product(range(3), repeat=8)}


def forcing(m, X, target, timeout=3600, mode="sat"):
    M = Model(m)
    eqs = []
    for x in X:
        for y in clean_ys(M, x):
            w = tuple(x) + tuple(y)
            if len(set(w)) > 1:
                eqs.append(M.phi(x, y))
    tgt = M.phi(tuple(target[:4]), tuple(target[4:]))
    allv = M.variables(eqs + [tgt])
    cells = [v for v in allv if v.startswith("a")]
    ll = ['LIB "elim.lib";', "ring r = 0,(%s),dp;" % ",".join(allv)]
    for i, e in enumerate(eqs, 1):
        ll.append("poly g%d = %s;" % (i, e))
    ll.append("poly tt = %s;" % tgt)
    ll.append("ideal Iid = %s;"
              % ",".join("g%d" % i for i in range(1, len(eqs) + 1)))
    ll.append("poly PP = %s;" % "*".join(cells))
    ll.append("ideal Jid = PP;")
    ll.append("list LL = sat(Iid,Jid);")
    ll.append("ideal GS = groebner(LL[1]);")
    ll.append('"FORCED:"; (reduce(tt,GS)==0);')
    ll.append('"UNIT:"; (GS[1]==1);')
    ll.append("quit;")
    t0 = time.time()
    out, st = run_singular("\n".join(ll) + "\n", timeout=timeout)
    dt = round(time.time() - t0, 1)
    if st == "TIMEOUT":
        return dict(m=m, verdict=None, secs=dt, n_eqs=len(eqs),
                    n_vars=len(allv))
    return dict(m=m, n_eqs=len(eqs), n_vars=len(allv), secs=dt,
                forced=out.split("FORCED:")[1].strip().split()[0] == "1",
                unit=out.split("UNIT:")[1].strip().split()[0] == "1")
