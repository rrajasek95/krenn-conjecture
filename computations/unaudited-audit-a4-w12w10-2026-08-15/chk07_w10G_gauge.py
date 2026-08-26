#!/usr/bin/env python3
"""AUDIT A4 / CHECK 07 -- TARGET B: LEMMA W10-G and its corollaries.

LEMMA W10-G (as stated in W10's report): a mixed-exact source with all three
pure coefficients nonzero is gauge-equivalent, WITH THE SAME TEMPLATE, to a
fully exact source, via g_{0,c} = 1/H_{c^N} at one site.

Independent derivation (audited by hand, then machine-checked here):
  (G) the diagonal gauge A_uv[i][j] -> g_{u,i} g_{v,j} A_uv[i][j] multiplies
      H_w by prod_{v in B} g_{v,w_v}, because every perfect matching covers
      every site exactly once;
  (T) all g's are nonzero, so the support pattern (template) is unchanged;
  (Z) therefore H(g.A)_w = 0  <=>  H(A)_w = 0 for EVERY word -- mixed-
      exactness is preserved by ANY gauge, no hypothesis needed;
  (D) with g trivial except at site 0, H(g.A)_{c^N} = g_{0,c} H(A)_{c^N};
      the three constant words read the three factors g_{0,0}, g_{0,1},
      g_{0,2} SEPARATELY (site 0 has colour c in the word c^N and no other
      constant word touches g_{0,c}), so the three normalisations are
      independent -- no interaction, three equations in three free scalars.

Everything is verified with EXACT arithmetic over Q and over the Gaussian
rationals Q(i) (for complex phases).
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction as F
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a4_engine as E  # noqa: E402

out = {}
COLORS = (0, 1, 2)


# ------------------------------------------------- exact Gaussian rationals
class GQ:
    __slots__ = ("re", "im")

    def __init__(self, re=0, im=0):
        self.re = F(re)
        self.im = F(im)

    def __add__(self, o):
        o = _gq(o)
        return GQ(self.re + o.re, self.im + o.im)

    __radd__ = __add__

    def __neg__(self):
        return GQ(-self.re, -self.im)

    def __sub__(self, o):
        return self + (-_gq(o))

    def __rsub__(self, o):
        return _gq(o) + (-self)

    def __mul__(self, o):
        o = _gq(o)
        return GQ(self.re * o.re - self.im * o.im,
                  self.re * o.im + self.im * o.re)

    __rmul__ = __mul__

    def inv(self):
        n = self.re * self.re + self.im * self.im
        if n == 0:
            raise ZeroDivisionError
        return GQ(self.re / n, -self.im / n)

    def __truediv__(self, o):
        return self * _gq(o).inv()

    def __rtruediv__(self, o):
        return _gq(o) * self.inv()

    def __eq__(self, o):
        try:
            o = _gq(o)
        except TypeError:
            return NotImplemented
        return self.re == o.re and self.im == o.im

    def __hash__(self):
        return hash((self.re, self.im))

    def __bool__(self):
        return not (self.re == 0 and self.im == 0)

    def __repr__(self):
        return f"({self.re}{'+' if self.im >= 0 else ''}{self.im}i)"


def _gq(x):
    return x if isinstance(x, GQ) else GQ(x, 0)


# sanity for the field arithmetic
assert GQ(0, 1) * GQ(0, 1) == GQ(-1, 0)
assert GQ(3, 4) * GQ(3, 4).inv() == GQ(1, 0)
assert GQ(F(3, 5), F(4, 5)) * GQ(F(3, 5), F(-4, 5)) == GQ(1, 0)   # modulus 1


# ------------------------------------------------------------- the model
def edges_of(n):
    return list(combinations(range(n), 2))


PM_CACHE = {}


def pms(n):
    if n not in PM_CACHE:
        PM_CACHE[n] = [sorted(M) for M in E.all_perfect_matchings(range(n))]
    return PM_CACHE[n]


def H(source, n, word):
    """H_w = sum over perfect matchings of prod A_uv[w_u][w_v]  (exact)."""
    total = 0
    for M in pms(n):
        term = 1
        for (u, v) in M:
            term = term * source[(u, v)][word[u]][word[v]]
            if term == 0:
                break
        total = total + term
    return total


def apply_gauge(source, n, g):
    return {(u, v): [[g[u][i] * g[v][j] * source[(u, v)][i][j]
                      for j in COLORS] for i in COLORS]
            for (u, v) in edges_of(n)}


def template_of(source, n):
    return frozenset((u, v, i, j) for (u, v) in edges_of(n)
                     for i in COLORS for j in COLORS
                     if source[(u, v)][i][j] != 0)


def zero_set(source, n):
    return frozenset(w for w in product(COLORS, repeat=n) if H(source, n, w) == 0)


def pures(source, n):
    return [H(source, n, (c,) * n) for c in COLORS]


def rand_source(n, rng, complexq=False, zero_prob=0.35, big=None):
    src = {}
    for e in edges_of(n):
        blk = []
        for i in COLORS:
            row = []
            for j in COLORS:
                if rng.random() < zero_prob:
                    row.append(GQ(0) if complexq else F(0))
                elif complexq:
                    row.append(GQ(F(rng.randint(-5, 5)),
                                  F(rng.randint(-5, 5), rng.randint(1, 4))))
                else:
                    row.append(F(rng.randint(-9, 9), rng.randint(1, 5)))
            blk.append(row)
        src[e] = blk
    return src


# ============================================== (G) the gauge identity
print("=== W10-G step (G): H(g.A)_w = (prod_v g_{v,w_v}) H(A)_w ===")
rows = []
rng = random.Random(20260815)
for n, complexq, trials in ((4, False, 40), (4, True, 12),
                            (6, False, 12), (6, True, 6), (8, False, 3)):
    checked = viol = 0
    for _ in range(trials):
        src = rand_source(n, rng, complexq)
        one = GQ(1) if complexq else F(1)
        g = [[(GQ(F(rng.randint(-6, 6) or 3, rng.randint(1, 3)),
                  F(rng.randint(-4, 4), rng.randint(1, 3)))
               if complexq else F(rng.randint(-6, 6) or 3, rng.randint(1, 3)))
              for _ in COLORS] for _ in range(n)]
        for row in g:                      # gauges must be invertible
            for k, x in enumerate(row):
                if x == 0:
                    row[k] = one * 3
        A = apply_gauge(src, n, g)
        words = list(product(COLORS, repeat=n)) if n <= 6 else \
            [tuple(rng.randrange(3) for _ in range(n)) for _ in range(120)] + \
            [(c,) * n for c in COLORS]
        for w in words:
            lhs = H(A, n, w)
            fac = one
            for v in range(n):
                fac = fac * g[v][w[v]]
            rhs = fac * H(src, n, w)
            checked += 1
            if lhs != rhs:
                viol += 1
    rows.append({"n": n, "field": "Q(i)" if complexq else "Q",
                 "checked": checked, "violations": viol})
    print(f"  N={n} over {'Q(i)' if complexq else 'Q  '}: {checked} word "
          f"identities, {viol} violations")
out["G_identity"] = rows
assert all(r["violations"] == 0 for r in rows)

# MUTATION CONTROL: a NON-gauge transformation must break (G)
src = rand_source(6, rng, False, zero_prob=0.1)
g = [[F(rng.randint(1, 5)) for _ in COLORS] for _ in range(6)]
A = apply_gauge(src, 6, g)
A[(0, 1)][0][0] = A[(0, 1)][0][0] + F(1)      # not a gauge any more
bad = 0
tot = 0
for w in product(COLORS, repeat=6):
    fac = F(1)
    for v in range(6):
        fac *= g[v][w[v]]
    tot += 1
    if H(A, 6, w) != fac * H(src, 6, w):
        bad += 1
out["G_mutation_control"] = {"words": tot, "violations": bad}
print(f"  [MUTATION] non-gauge perturbation: {bad}/{tot} words now violate (G)"
      f"  (must be > 0)")
assert bad > 0

# MUTATION CONTROL: a gauge with a zero entry changes the template
g0 = [[F(1)] * 3 for _ in range(6)]
g0[0][0] = F(0)
out["G_zero_gauge_changes_template"] = (
    template_of(apply_gauge(src, 6, g0), 6) != template_of(src, 6))
print(f"  [MUTATION] gauge with a zero entry changes the template: "
      f"{out['G_zero_gauge_changes_template']}  (must be True)")


# ================================ (T)(Z)(D) the lemma's construction itself
print("\n=== W10-G steps (T)(Z)(D): the normalising gauge at site 0 ===")


def gauge_to_exact(source, n):
    p = pures(source, n)
    if any(x == 0 for x in p):
        return None, p
    one = p[0] * 0 + 1 if isinstance(p[0], GQ) else F(1)
    g = [[one for _ in COLORS] for _ in range(n)]
    for c in COLORS:
        g[0][c] = one / p[c]
    return apply_gauge(source, n, g), p


rows = []
for n, complexq, trials, tag in ((4, False, 30, "plain"),
                                 (4, True, 10, "complex"),
                                 (6, False, 12, "plain"),
                                 (6, True, 6, "complex"),
                                 (8, False, 3, "plain")):
    ok_t = ok_c = ok_z = 0
    tried = 0
    for _ in range(trials):
        src = rand_source(n, rng, complexq, zero_prob=0.15)
        B, p = gauge_to_exact(src, n)
        if B is None:
            continue
        tried += 1
        ok_t += (template_of(B, n) == template_of(src, n))
        ok_c += all(H(B, n, (c,) * n) == 1 for c in COLORS)
        if n <= 6:
            ok_z += (zero_set(B, n) == zero_set(src, n))
        else:
            sample = [tuple(rng.randrange(3) for _ in range(n))
                      for _ in range(200)]
            ok_z += all((H(B, n, w) == 0) == (H(src, n, w) == 0)
                        for w in sample)
    rows.append({"n": n, "kind": tag, "instances": tried,
                 "same_template": ok_t, "constants_all_one": ok_c,
                 "zero_set_preserved": ok_z})
    print(f"  N={n} {tag:7s}: {tried} instances -- same template {ok_t}, "
          f"all three constants = 1 {ok_c}, zero-set unchanged {ok_z}")
out["lemma_core"] = rows
assert all(r["instances"] == r["same_template"] == r["constants_all_one"]
           == r["zero_set_preserved"] for r in rows)

# EDGE CASES: huge / tiny / unimodular-complex pure coefficients
print("\n  EDGE CASES (extreme and complex pure coefficients):")
edge_rows = []
for label, scale in (("pure ~ 10^12", F(10) ** 12),
                     ("pure ~ 10^-12", F(10) ** -12),
                     ("pure ~ 1/(2^60)", F(1, 2 ** 60))):
    src = rand_source(6, rng, False, zero_prob=0.15)
    # scale site 0's colour-0 row so that H_{0^6} is scaled by `scale`
    for (u, v) in edges_of(6):
        if u == 0:
            for j in COLORS:
                src[(u, v)][0][j] *= scale
        if v == 0:
            for i in COLORS:
                src[(u, v)][i][0] *= scale
    B, p = gauge_to_exact(src, 6)
    ok = (B is not None and template_of(B, 6) == template_of(src, 6)
          and all(H(B, 6, (c,) * 6) == 1 for c in COLORS)
          and zero_set(B, 6) == zero_set(src, 6))
    edge_rows.append({"case": label, "pure0_digits": len(str(p[0])), "ok": ok})
    print(f"    {label:16s}: pure_0 has {len(str(p[0]))} characters; "
          f"lemma holds exactly: {ok}")
    assert ok
for label, ph in (("phase i", GQ(0, 1)),
                  ("phase (3+4i)/5", GQ(F(3, 5), F(4, 5))),
                  ("phase (1+i)", GQ(1, 1))):
    src = rand_source(6, rng, True, zero_prob=0.15)
    for (u, v) in edges_of(6):
        if u == 0:
            for j in COLORS:
                src[(u, v)][0][j] = src[(u, v)][0][j] * ph
        if v == 0:
            for i in COLORS:
                src[(u, v)][i][0] = src[(u, v)][i][0] * ph
    B, p = gauge_to_exact(src, 6)
    ok = (B is not None and template_of(B, 6) == template_of(src, 6)
          and all(H(B, 6, (c,) * 6) == 1 for c in COLORS)
          and zero_set(B, 6) == zero_set(src, 6))
    edge_rows.append({"case": label, "pure0": str(p[0]), "ok": ok})
    print(f"    {label:16s}: pure_0 = {p[0]}; lemma holds exactly: {ok}")
    assert ok
out["lemma_edge_cases"] = edge_rows

# THE SUBTLETY: the three constant words read three DISJOINT gauge factors.
print("\n  SUBTLETY CHECK: do the three normalisations interact?")
src = rand_source(6, rng, False, zero_prob=0.15)
base = pures(src, 6)
inter = []
for c in COLORS:
    g = [[F(1)] * 3 for _ in range(6)]
    g[0][c] = F(7, 3)
    q = pures(apply_gauge(src, 6, g), 6)
    inter.append([str(x) for x in q])
    changed = [d for d in COLORS if q[d] != base[d]]
    print(f"    scaling g[0][{c}] by 7/3 changes constants {changed} "
          f"(must be exactly [{c}])")
    assert changed == [c] or (base[c] == 0 and changed == [])
out["subtlety_diagonal_action"] = inter

# NEGATIVE CONTROL: with a vanishing pure the construction is undefined
zsrc = rand_source(6, rng, False, zero_prob=0.15)
for (u, v) in edges_of(6):
    if 0 in (u, v):
        for i in COLORS:
            for j in COLORS:
                if (u == 0 and i == 0) or (v == 0 and j == 0):
                    zsrc[(u, v)][i][j] = F(0)
B, p = gauge_to_exact(zsrc, 6)
out["negative_control_vanishing_pure"] = {"pures": [str(x) for x in p],
                                          "gauge_returns_none": B is None}
print(f"  [NEGATIVE CONTROL] a source with H_(0^6)=0: pures "
      f"{[str(x) for x in p]}; construction refuses: {B is None}  (True)")
assert B is None


# ===================== END-TO-END at N=4, where exact sources really exist
print("\n=== END-TO-END: Delta_{4,3}, de-normalised then re-normalised ===")


def delta43():
    src = {e: [[F(0)] * 3 for _ in COLORS] for e in edges_of(4)}
    for c, es in {0: ((0, 1), (2, 3)), 1: ((0, 2), (1, 3)),
                  2: ((0, 3), (1, 2))}.items():
        for e in es:
            src[e][c][c] = F(1)
    return src


d43 = delta43()
exact43 = (all(H(d43, 4, (c,) * 4) == 1 for c in COLORS)
           and all(H(d43, 4, w) == 0 for w in product(COLORS, repeat=4)
                   if E.is_mixed(w)))
print(f"  Delta_43 is an EXACT N=4 source (my own recomputation): {exact43}")
out["delta43_exact"] = exact43
assert exact43

passed = 0
trials = 0
for kind in ("rational", "complex", "extreme"):
    for _ in range(15):
        if kind == "complex":
            src = {e: [[GQ(x) for x in row] for row in d43[e]]
                   for e in edges_of(4)}
            g = [[GQ(F(rng.randint(-6, 6) or 3, rng.randint(1, 3)),
                     F(rng.randint(-4, 4), rng.randint(1, 3)))
                  for _ in COLORS] for _ in range(4)]
            for row in g:
                for k, x in enumerate(row):
                    if x == 0:
                        row[k] = GQ(2, 1)
        elif kind == "extreme":
            src = d43
            g = [[F(rng.choice([10 ** 9, 10 ** -9, 1, -1, F(1, 2 ** 40)]))
                  * F(rng.randint(1, 4)) for _ in COLORS] for _ in range(4)]
        else:
            src = d43
            g = [[F(rng.randint(-6, 6) or 3, rng.randint(1, 3))
                  for _ in COLORS] for _ in range(4)]
        A = apply_gauge(src, 4, g)
        assert all(H(A, 4, w) == 0 for w in product(COLORS, repeat=4)
                   if E.is_mixed(w)), "de-normalised object lost mixed-exactness"
        pA = pures(A, 4)
        assert all(x != 0 for x in pA)
        B, _ = gauge_to_exact(A, 4)
        trials += 1
        ok = (all(H(B, 4, (c,) * 4) == 1 for c in COLORS)
              and all(H(B, 4, w) == 0 for w in product(COLORS, repeat=4)
                      if E.is_mixed(w))
              and template_of(B, 4) == template_of(A, 4))
        passed += ok
print(f"  {passed}/{trials} de-normalised Delta_43 objects (rational, "
      f"Gaussian-complex, and extreme-modulus gauges) gauge back to EXACT "
      f"with the SAME template")
out["end_to_end_delta43"] = {"trials": trials, "passed": passed}
assert passed == trials

# MUTATION CONTROL: perturbing a cell must destroy exactness
mut = {e: [row[:] for row in d43[e]] for e in edges_of(4)}
mut[(0, 1)][0][0] += F(1, 3)
broken = any(H(mut, 4, w) != 0 for w in product(COLORS, repeat=4)
             if E.is_mixed(w)) or any(H(mut, 4, (c,) * 4) != 1 for c in COLORS)
out["mutation_control_exactness_checker"] = broken
print(f"  [MUTATION] perturbing one cell breaks exactness: {broken}  (True)")
assert broken

with open(os.path.join(HERE, "results_chk07.json"), "w") as fh:
    json.dump(out, fh, indent=1, default=str)
print("wrote results_chk07.json")
