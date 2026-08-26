#!/usr/bin/env python3
"""UNAUDITED PROBE (W7) -- the torus lemmas the kill engine uses, verified.

Pinned HEAD: a41949965d41e5c63fb4bc1caf7b20c0df017856

LEMMA H4.  Let W be a symmetric zero-diagonal matrix on N >= 6 vertices over a
field of characteristic not 2 or 3, with EVERY off-diagonal entry nonzero.
Then haf(W[T]) != 0 for at least one 4-subset T.

  Proof.  Suppose haf(W[T]) = 0 for every 4-subset.  The scaling
  W_uv -> t_u t_v W_uv multiplies every 4-subset hafnian by t_a t_b t_c t_d, so
  we may normalise W_12 = W_13 = W_23 = 1.  For d outside {1,2,3} write
  p_d = W_1d, q_d = W_2d, r_d = W_3d.  The quadruple {1,2,3,d} gives
       W_12 r_d + W_13 q_d + W_23 p_d = p_d + q_d + r_d = 0.            (i)
  The quadruples {1,2,d,e}, {1,3,d,e}, {2,3,d,e} give
       W_de = -(p_d q_e + p_e q_d) = -(p_d r_e + p_e r_d)
                                   = -(q_d r_e + q_e r_d).              (ii)
  Substituting r = -(p+q) into the first two equalities of (ii) and dividing by
  2 (char != 2):   p_d p_e + p_d q_e + p_e q_d = 0;                     (iii)
  from the first and third:  p_d q_e + p_e q_d + q_d q_e = 0.           (iv)
  Subtracting, p_d p_e = q_d q_e for all d != e outside {1,2,3}.        (v)
  With N >= 6 there are three such vertices d,e,f; multiplying the (d,e) and
  (d,f) instances of (v) and dividing by the (e,f) instance gives p_d^2 = q_d^2,
  so q_d = eps_d p_d with eps_d = +-1, and (v) forces eps_d eps_e = 1, i.e. a
  common sign eps.  Then (iii) reads p_d p_e (1 + 2 eps) = 0, and p_d p_e != 0,
  so 1 + 2 eps = 0 -- impossible for eps = +-1 unless 3 = 0.  []

  SHARPNESS.  In characteristic 3 the conclusion FAILS: W_12=W_13=W_23=1,
  W_1d=W_2d=W_3d=p_d, W_de=p_d p_e is a solution with all entries nonzero.
  The script constructs it and checks it, so the characteristic hypothesis is
  exercised rather than decorative.

LEMMA P2.  Let X assign a nonzero value X(u,v) to every ordered pair of
distinct vertices.  If per(X[{a,b},{c,d}]) = X(a,c)X(b,d) + X(a,d)X(b,c) = 0
for every choice of disjoint 2-sets {a,b}, {c,d}, and at least three vertices
can serve as rows against a common pair of columns, then a contradiction.

  Proof.  The hypothesis says R(a,b;c,d) := X(a,c)X(b,d)/(X(a,d)X(b,c)) = -1.
  R is multiplicative in the row argument: R(a,b;c,d) R(b,e;c,d) = R(a,e;c,d).
  Three rows a,b,e against columns c,d give (-1)(-1) = -1, i.e. 1 = -1.  []

Both lemmas are additionally checked by exact/random computation below, and two
NEGATIVE controls are run: the level-6 analogue of H4 at N = 8 and the 3+3
analogue of P2 at N = 6 are shown SATISFIABLE with all entries nonzero, so the
engine is right to record them as residue rather than as kills.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations
import random

import sympy as sp


def haf(entries, verts):
    verts = tuple(verts)
    if not verts:
        return sp.Integer(1)
    total = 0
    first = verts[0]
    for i in range(1, len(verts)):
        rest = verts[1:i] + verts[i + 1:]
        total += entries[frozenset((first, verts[i]))] * haf(entries, rest)
    return total


def check_h4_proof():
    """Verify the algebraic steps (i)-(v) of Lemma H4 symbolically."""
    d, e = sp.symbols("pd qd rd pe qe re", positive=False)[:0] or (None, None)
    pd, qd, rd, pe, qe, re = sp.symbols("pd qd rd pe qe re")
    Wde = sp.symbols("Wde")
    # (i)
    eq_i_d = pd + qd + rd
    eq_i_e = pe + qe + re
    # (ii): the three expressions for W_de
    A = -(pd * qe + pe * qd)
    B = -(pd * re + pe * rd)
    C = -(qd * re + qe * rd)
    sub = {rd: -(pd + qd), re: -(pe + qe)}
    assert sp.simplify(eq_i_d.subs(sub)) == 0
    assert sp.simplify(eq_i_e.subs(sub)) == 0
    # (A-B)/2 and (A-C)/2 come out as MINUS the displayed forms (iii), (iv);
    # vanishing is the same statement, and the sign is checked here rather than
    # absorbed silently.
    iii = sp.expand((A - B).subs(sub) / 2)
    iv = sp.expand((A - C).subs(sub) / 2)
    assert sp.expand(iii + (pd * pe + pd * qe + pe * qd)) == 0, iii
    assert sp.expand(iv + (pd * qe + pe * qd + qd * qe)) == 0, iv
    v = sp.expand(iii - iv)
    assert sp.expand(v + (pd * pe - qd * qe)) == 0, v
    # final step with q = eps p
    for eps in (1, -1):
        val = sp.expand(iii.subs({qd: eps * pd, qe: eps * pe}))
        assert sp.expand(val + pd * pe * (1 + 2 * eps)) == 0
    return True


def char3_witness(nsites=8):
    """The characteristic-3 solution: all entries nonzero, all 4-subset
    hafnians zero.  Verified in F_3."""
    p = {v: (v % 2) + 1 for v in range(3, nsites)}  # nonzero mod 3
    entries = {}
    base = (0, 1, 2)
    for u, v in combinations(range(nsites), 2):
        if u in base and v in base:
            entries[frozenset((u, v))] = 1
        elif u in base:
            entries[frozenset((u, v))] = p[v]
        else:
            entries[frozenset((u, v))] = (p[u] * p[v]) % 3
    for value in entries.values():
        assert value % 3 != 0, "char-3 witness has a zero entry"
    bad = 0
    for T in combinations(range(nsites), 4):
        total = 0
        a, b, c, d = T
        total += entries[frozenset((a, b))] * entries[frozenset((c, d))]
        total += entries[frozenset((a, c))] * entries[frozenset((b, d))]
        total += entries[frozenset((a, d))] * entries[frozenset((b, c))]
        if total % 3 != 0:
            bad += 1
    return bad == 0


def h4_groebner(nsites=6):
    """Exact confirmation of Lemma H4 at N=6 over Q: the ideal generated by all
    4-subset hafnians, saturated at the product of all entries, is the unit
    ideal.  (Done by adding a Rabinowitsch variable.)"""
    names = {}
    gens = []
    for u, v in combinations(range(nsites), 2):
        s = sp.Symbol("w%d%d" % (u, v))
        names[frozenset((u, v))] = s
        gens.append(s)
    z = sp.Symbol("z")
    polys = []
    for T in combinations(range(nsites), 4):
        a, b, c, d = T
        polys.append(names[frozenset((a, b))] * names[frozenset((c, d))]
                     + names[frozenset((a, c))] * names[frozenset((b, d))]
                     + names[frozenset((a, d))] * names[frozenset((b, c))])
    prod = sp.Integer(1)
    for s in gens:
        prod *= s
    polys.append(z * prod - 1)
    G = sp.groebner(polys, *(gens + [z]), order="grevlex")
    return list(G.exprs) == [sp.Integer(1)]


def p2_check(nsites=6, trials=4000):
    """Random control for Lemma P2: search for X with all entries nonzero and
    all disjoint 2+2 permanents zero.  Must find none; the proof says none
    exists.  Also verify the multiplicativity identity symbolically."""
    xac, xbd, xad, xbc, xec, xed = sp.symbols("xac xbd xad xbc xec xed")
    R_ab = (xac * xbd) / (xad * xbc)
    R_be = (xbc * xed) / (xbd * xec)
    R_ae = (xac * xed) / (xad * xec)
    assert sp.simplify(R_ab * R_be - R_ae) == 0
    rng = random.Random(7)
    found = 0
    for _ in range(trials):
        X = {}
        for u in range(nsites):
            for v in range(nsites):
                if u != v:
                    X[(u, v)] = Fraction(rng.randint(-6, 6) or 1)
        ok = True
        for a, b in combinations(range(nsites), 2):
            for c, d in combinations([x for x in range(nsites)
                                      if x not in (a, b)], 2):
                if X[(a, c)] * X[(b, d)] + X[(a, d)] * X[(b, c)] != 0:
                    ok = False
                    break
            if not ok:
                break
        found += ok
    return found == 0


def negative_control_h6(nsites=8, trials=60):
    """NEGATIVE control: at N=8 there DOES exist W with all entries nonzero and
    every 6-subset hafnian zero -- so 'h_c vanishes on all (N-2)-subsets' is
    NOT by itself a contradiction and the engine must not treat it as one.
    Solved numerically by Newton from random starts (15 equations, 28
    unknowns), then the residual and the minimum |entry| are reported."""
    import numpy as np

    verts = list(range(nsites))
    pairs = list(combinations(verts, 2))
    index = {frozenset(p): i for i, p in enumerate(pairs)}

    def haf_num(vec, subset):
        subset = tuple(subset)
        if not subset:
            return 1.0
        total = 0.0
        first = subset[0]
        for i in range(1, len(subset)):
            rest = subset[1:i] + subset[i + 1:]
            total += vec[index[frozenset((first, subset[i]))]] * haf_num(vec, rest)
        return total

    sixes = list(combinations(verts, 6))
    rng = np.random.default_rng(11)
    best = None
    for _ in range(trials):
        x = rng.normal(size=len(pairs))
        for _ in range(200):
            F = np.array([haf_num(x, S) for S in sixes])
            if np.max(np.abs(F)) < 1e-13:
                break
            J = np.zeros((len(sixes), len(pairs)))
            eps = 1e-7
            for k in range(len(pairs)):
                xp = x.copy()
                xp[k] += eps
                J[:, k] = (np.array([haf_num(xp, S) for S in sixes]) - F) / eps
            step, *_ = np.linalg.lstsq(J, -F, rcond=None)
            x = x + step
        res = np.max(np.abs(np.array([haf_num(x, S) for S in sixes])))
        mn = np.min(np.abs(x))
        if res < 1e-10 and (best is None or mn > best[1]):
            best = (res, mn)
    return best


def negative_control_p3(nsites=6, trials=40):
    """NEGATIVE control: at N=6 there DOES exist X with all entries nonzero and
    per(X[P, V\\P]) = 0 for every 3-subset P."""
    import numpy as np

    verts = list(range(nsites))
    ordered = [(u, v) for u in verts for v in verts if u != v]
    index = {p: i for i, p in enumerate(ordered)}
    triples = [P for P in combinations(verts, 3) if 0 in P]

    def per_num(x, P, Q):
        total = 0.0
        for sigma in permutations(Q):
            term = 1.0
            for a, b in zip(P, sigma):
                term *= x[index[(a, b)]]
            total += term
        return total

    def system(x):
        out = []
        for P in triples:
            Q = tuple(v for v in verts if v not in P)
            out.append(per_num(x, P, Q))
            out.append(per_num(x, Q, P))
        return np.array(out)

    rng = np.random.default_rng(5)
    best = None
    for _ in range(trials):
        x = rng.normal(size=len(ordered))
        for _ in range(200):
            F = system(x)
            if np.max(np.abs(F)) < 1e-13:
                break
            J = np.zeros((len(F), len(x)))
            eps = 1e-7
            for k in range(len(x)):
                xp = x.copy()
                xp[k] += eps
                J[:, k] = (system(xp) - F) / eps
            step, *_ = np.linalg.lstsq(J, -F, rcond=None)
            x = x + step
        res = np.max(np.abs(system(x)))
        mn = np.min(np.abs(x))
        if res < 1e-10 and (best is None or mn > best[1]):
            best = (res, mn)
    return best


def main():
    print("UNAUDITED PROBE (W7) -- torus lemmas")
    print("LEMMA H4 algebraic steps verified symbolically :", check_h4_proof())
    print("LEMMA H4 char-3 sharpness witness at N=8 valid :", char3_witness())
    print("LEMMA H4 at N=6 over Q, Groebner + saturation  :", h4_groebner())
    print("LEMMA P2 identity + random control (N=6)       :", p2_check())
    print()
    print("NEGATIVE CONTROLS (these must SUCCEED in finding a solution, which is")
    print("why the engine records them as residue, not as kills)")
    got = negative_control_h6()
    print("  N=8, all 6-subset hafnians zero, entries nonzero:",
          "found (residual %.2e, min |entry| %.3f)" % got if got else "NOT FOUND")
    got = negative_control_p3()
    print("  N=6, all 3+3 permanents zero, entries nonzero  :",
          "found (residual %.2e, min |entry| %.3f)" % got if got else "NOT FOUND")


if __name__ == "__main__":
    main()
