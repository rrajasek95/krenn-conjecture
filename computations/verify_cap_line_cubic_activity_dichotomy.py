#!/usr/bin/env python3
"""The h=3 cap line E_ab + zI: the clean error is a cubic in z, and the
landing chi=0 is exactly its INACTIVE root.

Research evidence only.  Krenn's conjecture remains open, `SP-CLEAN-BRIDGE`
is untouched, and no certified dependency changes.

Setting.  A cap covector K in (V_p (x) V_q)^* has, in the notation of
notes/clean-pair-cap-exact-descent-target.md,

    s = <K, A_pq>,   kappa_c = K(e_c,e_c),
    R_ab = K |_ (A_p|a A_q|b + A_p|b A_q|a),   r = sum_{a<b} R_ab,
    x = sum_{a<b} A_ab,
    E = (1/2) s r^2 x + (1/6) r^3           (full-U-support part, h = 3),

and Theorem 1.1 of that note descends from any K with

    s kappa_0 kappa_1 kappa_2 != 0   (activity)   and   E = 0  (cleanliness).

What is verified here, as FORMAL polynomial identities in the 60 generic
symbols a fixed word exposes -- hence at every one of the 729 words, on
every packet:

  A1  E = s Q2 + Q3  with  Q_j = R^[j] q^[3-j], i.e. the descent note's (17)
      read in the square-free algebra agrees with the star-sector layers.
  A2  E(K)_w = haf_w(s q^w + R^w) - s^2 <K, H_B(A)>_w, and
      <K, H_B(A)>_w = sum_lm K_lm Row(l,m,w).  So under H_B(A) = Delta_{B,3}
      cleanliness is exactly  H_U(s q + R) = s^2 sum_c kappa_c X_c.
  A3  every coordinate cap E_ab is INACTIVE: kappa_0 kappa_1 kappa_2 = 0.
      On the line K_z = E_ab + zI one has kappa_c = delta_{a=b=c} + z.
  A4  E(K_z)_w is a CUBIC in z.  Its four coefficient tensors are the
      polarizations of Chi(sigma,X) = sigma X^[2] q + X^[3] along
      (alpha, A) -> (tau, B), with alpha = A_pq(a,b), tau = tr A_pq,
      A = R(E_ab), B = R(I).  In particular
          [z^0] E = alpha Q2 + Q3 = chi   (the star-sector terminal class)
          [z^3] E = tau B^[2] q + B^[3] = E(I),   independent of (a,b).
  A5  s(K_z) = alpha + z tau, so the scalar-zero point is z = -alpha/tau,
      i.e. K_1 = tau E_ab - alpha I, where E(K_1) = haf(R(K_1)).
      If tau = 0 the only inactive point of the AFFINE off-diagonal line is
      z = 0; the point at infinity K = I is inactive there too, since
      s(I) = tau = 0.
      Homogenising K(t,u) = t E_ab + u I, the point t = 0 is the IDENTITY cap
      K = I -- the POINT AT INFINITY of every cap line, not an affine point of
      one.  It is a common root exactly when the leading tensor c_3 = E(I)
      vanishes, and is ACTIVE exactly when tau != 0.  So E(I) = 0 with
      tau != 0 already gives the descent -- but see
      ``notes/clean-bridge-at-eight-is-the-open-case.md``: at h = 3 that
      statement is equivalent to the open (8,3) case, so it is not a usable
      intermediate target.
  A6  the target-stabilizing torus lambda_{p,l} = g_l, lambda_{q,m} = 1/g_m,
      lambda_{u,c} = 1 SCALES Row(l,m,.) by g_l/g_m.  It therefore fixes every
      l = m coefficient -- in particular every GHZ target -- and fixes the
      matching tensor of any NINE-ROW solution, where the l != m coefficients
      vanish.  It does NOT fix every row.  It sends
      c_k -> (g_i/g_j)^{3-k} c_k, hence  z -> (g_i/g_j) z, so a nonzero root
      of the gcd is not a function of the matching tensor ON AN OFF-DIAGONAL
      LINE.  For a = b the weight (3-k)(e_a - e_b) is zero: the torus fixes
      all four c_k and moves no root, so this argument gives NOTHING on a
      diagonal line.  Both halves are checked, formally and numerically.

Consequences recorded, then measured on the named packets:

  B1  rank criterion.  Let M be the 729x4 matrix of coefficient tensors.
      A clean point on the line requires rank M <= 3; rank M = 4 is the
      rootless branch.  Proving the landing chi = 0 in all 729 coordinates
      is exactly "column c_0 vanishes", which supplies that rank drop with
      the root z = 0 -- an inactive point.  An active clean point ON TOP of
      chi = 0 needs rank M <= 2.
  B2  the named packets.  Seven-row guard, alternating eight-cycle, pure-word
      anchor witness, packets B and C: exact gcd of the 729 cubics on all
      nine cap lines, and the exact activity verdict.
  B3  unconstrained random packets have rank M = 4 and gcd one.

None of this assumes or proves SP-CLEAN-BRIDGE.  The packets satisfy at most
6560 of the 6561 GHZ coefficients, so an active clean point on one of them is
calibration, not a contradiction.

Python standard library only, exact Fraction arithmetic, live under
``python3 -O`` and ``python3 -I -S``, deterministic across PYTHONHASHSEED.
"""

from fractions import Fraction as Q
from itertools import combinations, product

SITES = tuple(range(6))
COLORS = (0, 1, 2)
LEFT, RIGHT = 6, 7
PAIRS = tuple(combinations(SITES, 2))
WORDS = tuple(product(COLORS, repeat=6))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


# ==========================================================================
# 0.  perfect matchings and the all-ones normalization
# ==========================================================================
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    out = []
    first = vertices[0]
    for k, partner in enumerate(vertices[1:], start=1):
        rest = vertices[1:k] + vertices[k + 1:]
        for tail in perfect_matchings(rest):
            out.append(((first, partner),) + tail)
    return tuple(out)


M6 = perfect_matchings(SITES)
M4 = {p: perfect_matchings(tuple(s for s in SITES if s not in p)) for p in PAIRS}


def audit_normalization():
    require(len(M6) == 15, "six-site all-ones hafnian is not 15")
    require(len(perfect_matchings((0, 1, 2, 3))) == 3, "four-site hafnian is not 3")
    require(len(perfect_matchings((0, 1))) == 1, "two-site hafnian is not 1")
    require(len(perfect_matchings(tuple(range(8)))) == 105, "eight-vertex count")
    ones = [[Q(0) if x == y else Q(1) for y in SITES] for x in SITES]
    haf = sum((Q(1) for _ in M6), Q(0))
    polar = [[Q(0) if x == y else
              sum((Q(1) for _ in M4[(min(x, y), max(x, y))]), Q(0))
              for y in SITES] for x in SITES]
    require(haf == 15 and polar[0][1] == 3, "polar normalization changed")
    # double polar: H(H(A)) for the all-ones array
    dbl = sum((Q(1) for _ in M4[(0, 1)]), Q(0))
    require(dbl == 3, "double-polar inner entry changed")
    hh = Q(0)
    for m in M4[(0, 1)]:
        term = Q(1)
        for x, y in m:
            term *= polar[x][y]
        hh += term
    require(hh == 27, "all-ones double polar is not 27")
    require(hh - haf * ones[0][1] == 12, "all-ones double-polar defect is not 12")


# ==========================================================================
# 1.  sparse multivariate polynomials over Q
# ==========================================================================
class P(object):
    __slots__ = ("t",)

    def __init__(self, terms=None):
        if terms is None:
            self.t = {}
        else:
            self.t = {m: c for m, c in terms.items() if c}

    @staticmethod
    def const(c):
        c = Q(c)
        return P({(): c}) if c else P()

    @staticmethod
    def var(name):
        return P({(name,): Q(1)})

    def __bool__(self):
        return bool(self.t)

    __nonzero__ = __bool__

    def __eq__(self, other):
        return self.t == other.t

    def __hash__(self):
        return hash(tuple(sorted(self.t.items())))

    def __add__(self, other):
        out = dict(self.t)
        for m, c in other.t.items():
            n = out.get(m, Q(0)) + c
            if n:
                out[m] = n
            else:
                out.pop(m, None)
        return P(out)

    def __neg__(self):
        return P({m: -c for m, c in self.t.items()})

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if not self.t or not other.t:
            return P()
        out = {}
        for m1, c1 in self.t.items():
            for m2, c2 in other.t.items():
                m = tuple(sorted(m1 + m2))
                n = out.get(m, Q(0)) + c1 * c2
                if n:
                    out[m] = n
                else:
                    out.pop(m, None)
        return P(out)

    def zsplit(self, zname):
        buckets = {}
        for m, c in self.t.items():
            k = sum(1 for v in m if v == zname)
            rest = tuple(v for v in m if v != zname)
            d = buckets.setdefault(k, {})
            n = d.get(rest, Q(0)) + c
            if n:
                d[rest] = n
            else:
                d.pop(rest, None)
        top = max(buckets) if buckets else 0
        return [P(buckets.get(k, {})) for k in range(top + 1)]


# ==========================================================================
# 2.  the block-array model (works over Fraction or over P)
# ==========================================================================
class Packet(object):
    """q[(x,y,cx,cy)], p[(l,x,c)], s[(m,y,c)], d[(l,m)]."""

    def __init__(self, q, p, s, d, symbolic=False):
        self.q, self.p, self.s, self.d = q, p, s, d
        self.symbolic = symbolic
        self.zero = P() if symbolic else Q(0)
        self.one = P.const(1) if symbolic else Q(1)

    def qe(self, x, y, cx, cy):
        if x > y:
            x, y, cx, cy = y, x, cy, cx
        return self.q.get((x, y, cx, cy), self.zero)

    def pe(self, l, x, c):
        return self.p.get((l, x, c), self.zero)

    def se(self, m, y, c):
        return self.s.get((m, y, c), self.zero)

    def de(self, l, m):
        return self.d.get((l, m), self.zero)

    def haf(self, value, verts=SITES):
        total = self.zero
        for matching in perfect_matchings(tuple(verts)):
            term = self.one
            for e in matching:
                term = term * value(*e)
                if not term:
                    break
            total = total + term
        return total

    def row(self, l, m, w):
        total = self.de(l, m) * self.haf(lambda x, y: self.qe(x, y, w[x], w[y]))
        for x, y in PAIRS:
            resp = (self.pe(l, x, w[x]) * self.se(m, y, w[y])
                    + self.pe(l, y, w[y]) * self.se(m, x, w[x]))
            if not resp:
                continue
            rest = tuple(v for v in SITES if v not in (x, y))
            total = total + resp * self.haf(
                lambda a, b: self.qe(a, b, w[a], w[b]), rest)
        return total

    def cap_s(self, K):
        total = self.zero
        for l, m in product(COLORS, repeat=2):
            if K[l][m]:
                total = total + K[l][m] * self.de(l, m)
        return total

    def cap_R(self, K, w):
        out = {}
        for x, y in PAIRS:
            total = self.zero
            for l, m in product(COLORS, repeat=2):
                if not K[l][m]:
                    continue
                v = (self.pe(l, x, w[x]) * self.se(m, y, w[y])
                     + self.pe(l, y, w[y]) * self.se(m, x, w[x]))
                if v:
                    total = total + K[l][m] * v
            out[(x, y)] = total
        return out

    def layers(self, R, w):
        qv = {e: self.qe(e[0], e[1], w[e[0]], w[e[1]]) for e in PAIRS}
        out = [self.zero] * 4
        for matching in M6:
            for flags in product((0, 1), repeat=3):
                term = self.one
                for f, e in zip(flags, matching):
                    term = term * (R[e] if f else qv[e])
                    if not term:
                        break
                if term:
                    k = sum(flags)
                    out[k] = out[k] + term
        return out

    def E_word(self, K, w):
        R = self.cap_R(K, w)
        layers = self.layers(R, w)
        return self.cap_s(K) * layers[2] + layers[3]

    def cap_row(self, K, w):
        R = self.cap_R(K, w)
        layers = self.layers(R, w)
        return self.cap_s(K) * layers[0] + layers[1]

    def cap_haf(self, K, w):
        sK = self.cap_s(K)
        R = self.cap_R(K, w)
        return self.haf(lambda x, y: sK * self.qe(x, y, w[x], w[y]) + R[(x, y)])


def ghz(l, m, w):
    return Q(1) if (l == m and all(c == l for c in w)) else Q(0)


# ==========================================================================
# 3.  formal identities in the 60 generic symbols of one word
# ==========================================================================
# For a FIXED word w the data q^w(a,b), p^w(l,a), s^w(m,a), d(l,m) are
# 15 + 18 + 18 + 9 = 60 DISTINCT entries of the block array, whatever w is.
# So an identity proved with generic symbols holds at all 729 words, on every
# packet, with cross-colour internal edges live.
ZED = "z"
GENERIC_WORD = (0,) * 6
_qs = {(x, y): P.var("q_%d_%d" % (x, y)) for x, y in PAIRS}
_ps = {(l, x): P.var("p_%d_%d" % (l, x)) for l in COLORS for x in SITES}
_ss = {(m, y): P.var("s_%d_%d" % (m, y)) for m in COLORS for y in SITES}
_ds = {(l, m): P.var("d_%d_%d" % (l, m)) for l in COLORS for m in COLORS}
GEN = Packet(
    q={(x, y, 0, 0): v for (x, y), v in _qs.items()},
    p={(l, x, 0): v for (l, x), v in _ps.items()},
    s={(m, y, 0): v for (m, y), v in _ss.items()},
    d=dict(_ds),
    symbolic=True,
)
ZVAR = P.var(ZED)
IDENT = [[P.const(1) if a == b else P() for b in COLORS] for a in COLORS]


def coord_cap(i, j):
    return [[P.const(1) if (a, b) == (i, j) else P() for b in COLORS]
            for a in COLORS]


def line_cap(i, j):
    return [[(P.const(1) if (a, b) == (i, j) else P())
             + (ZVAR if a == b else P()) for b in COLORS] for a in COLORS]


def _squarefree_mul(f, g):
    """product in the square-free algebra: keys are frozensets of sites."""
    out = {}
    for s1, v1 in f.items():
        for s2, v2 in g.items():
            if s1 & s2:
                continue
            key = s1 | s2
            cur = out.get(key)
            out[key] = (v1 * v2) if cur is None else cur + v1 * v2
    return {k: v for k, v in out.items() if v}


def audit_A1_descent_note_formula():
    """(1/2) s r^2 x + (1/6) r^3, full support, equals s Q2 + Q3."""
    full = frozenset(SITES)
    for i, j in ((0, 1), (2, 2)):
        K = coord_cap(i, j)
        R = GEN.cap_R(K, GENERIC_WORD)
        sK = GEN.cap_s(K)
        r = {frozenset(e): R[e] for e in PAIRS if R[e]}
        x = {frozenset(e): _qs[e] for e in PAIRS}
        r2 = _squarefree_mul(r, r)
        r2x = _squarefree_mul(r2, x)
        r3 = _squarefree_mul(r2, r)
        layers = GEN.layers(R, GENERIC_WORD)
        half = P.const(Q(1, 2))
        sixth = P.const(Q(1, 6))
        lhs = half * sK * r2x.get(full, P()) + sixth * r3.get(full, P())
        require(lhs == sK * layers[2] + layers[3],
                ("(1/2) s r^2 x + (1/6) r^3 is not s Q2 + Q3", i, j))
        # the two displayed pieces separately
        require(half * r2x.get(full, P()) == layers[2],
                ("r^2 x / 2 is not Q2", i, j))
        require(sixth * r3.get(full, P()) == layers[3],
                ("r^3 / 6 is not Q3", i, j))


def audit_A2_cap_reformulation():
    for i, j in ((0, 1), (2, 2), (1, 0)):
        for tag, K in (("coord", coord_cap(i, j)), ("line", line_cap(i, j))):
            E = GEN.E_word(K, GENERIC_WORD)
            sK = GEN.cap_s(K)
            alt = GEN.cap_haf(K, GENERIC_WORD) - sK * sK * GEN.cap_row(
                K, GENERIC_WORD)
            require(E == alt,
                    ("E != haf(sq+R) - s^2 <K,H_B(A)>", tag, i, j))
            lhs = GEN.cap_row(K, GENERIC_WORD)
            rhs = P()
            for l, m in product(COLORS, repeat=2):
                if K[l][m]:
                    rhs = rhs + K[l][m] * GEN.row(l, m, GENERIC_WORD)
            require(lhs == rhs,
                    ("<K,H_B(A)>_w != sum K_lm Row(l,m,w)", tag, i, j))


def audit_A3_activity_ledger():
    for a, b in product(COLORS, repeat=2):
        K = coord_cap(a, b)
        prod = P.const(1)
        for c in COLORS:
            prod = prod * K[c][c]
        require(prod == P(),
                ("coordinate cap E_%d%d is not inactive" % (a, b)))
        L = line_cap(a, b)
        want = [(P.const(1) if a == b == c else P()) + ZVAR for c in COLORS]
        require([L[c][c] for c in COLORS] == want,
                ("kappa ledger of the line changed", a, b))


def _polarized_coefficient(n, i, j):
    """the claimed [z^n] of E on the line, written from A, B, alpha, tau."""
    A = GEN.cap_R(coord_cap(i, j), GENERIC_WORD)
    B = GEN.cap_R(IDENT, GENERIC_WORD)
    alpha = _ds[(i, j)]
    tau = _ds[(0, 0)] + _ds[(1, 1)] + _ds[(2, 2)]
    pick = lambda flag: B if flag else A

    def lay2(f0, f1):
        total = P()
        for matching in M6:
            for k in range(3):
                rest = [matching[t] for t in range(3) if t != k]
                total = total + (pick(f0)[rest[0]] * pick(f1)[rest[1]]
                                 * _qs[matching[k]])
        return total

    def lay3(f0, f1, f2):
        total = P()
        for matching in M6:
            total = total + (pick(f0)[matching[0]] * pick(f1)[matching[1]]
                             * pick(f2)[matching[2]])
        return total

    out = P()
    for scalar, spow in ((alpha, 0), (tau, 1)):
        for f0, f1 in product((0, 1), repeat=2):
            if spow + f0 + f1 == n:
                out = out + scalar * lay2(f0, f1)
    for f0, f1, f2 in product((0, 1), repeat=3):
        if f0 + f1 + f2 == n:
            out = out + lay3(f0, f1, f2)
    return out


_LINE_E = {}


def line_E(i, j):
    if (i, j) not in _LINE_E:
        _LINE_E[(i, j)] = GEN.E_word(line_cap(i, j), GENERIC_WORD).zsplit(ZED)
    return _LINE_E[(i, j)]


def audit_A4_four_coefficient_tensors():
    top = None
    for i, j in product(COLORS, repeat=2):
        coeffs = line_E(i, j)
        require(len(coeffs) == 4, ("E is not a cubic in z", i, j))
        if (i, j) in ((0, 1), (2, 2)):
            for n in range(4):
                require(coeffs[n] == _polarized_coefficient(n, i, j),
                        ("[z^%d] E is not the claimed polarization" % n, i, j))
        # z^0 is exactly the star-sector terminal class chi = alpha Q2 + Q3
        Kc = coord_cap(i, j)
        Rc = GEN.cap_R(Kc, GENERIC_WORD)
        lay = GEN.layers(Rc, GENERIC_WORD)
        chi = _ds[(i, j)] * lay[2] + lay[3]
        require(coeffs[0] == chi, ("[z^0] E is not chi", i, j))
        require(GEN.cap_haf(Kc, GENERIC_WORD)
                == _ds[(i, j)] * _ds[(i, j)] * (_ds[(i, j)] * lay[0] + lay[1])
                + chi,
                ("cap split haf(alpha q + R) = alpha^2 J0 + chi failed", i, j))
        if top is None:
            top = coeffs[3]
        else:
            require(coeffs[3] == top, ("[z^3] E depends on (i,j)", i, j))
    require(top == GEN.E_word(IDENT, GENERIC_WORD),
            "[z^3] E is not the identity cap's terminal class")


def audit_A5_scalar_zero_point():
    tau = _ds[(0, 0)] + _ds[(1, 1)] + _ds[(2, 2)]
    for i, j in ((0, 1), (2, 2)):
        alpha = _ds[(i, j)]
        s_line = GEN.cap_s(line_cap(i, j)).zsplit(ZED)
        require(s_line[0] == alpha and s_line[1] == tau,
                ("s(K_z) is not alpha + z tau", i, j))
        K1 = [[(tau if (a, b) == (i, j) else P())
               - (alpha if a == b else P()) for b in COLORS] for a in COLORS]
        require(GEN.cap_s(K1) == P(),
                ("K_1 = tau E_ab - alpha I is not the scalar-zero point", i, j))
        R1 = GEN.cap_R(K1, GENERIC_WORD)
        require(GEN.E_word(K1, GENERIC_WORD) == GEN.layers(R1, GENERIC_WORD)[3]
                == GEN.haf(lambda x, y: R1[(min(x, y), max(x, y))]),
                ("E(K_1) is not haf(R(K_1))", i, j))


def audit_A6_target_stabilizing_torus():
    """every monomial of Row(l,m,w) carries exactly one p_l and one s_m, or
    the single symbol d_lm.  Hence the torus p_l -> g_l p_l, s_m -> s_m/g_m,
    d_lm -> (g_l/g_m) d_lm scales Row(l,m,w) by g_l/g_m and fixes it whenever
    l = m -- in particular it fixes every nonzero GHZ target."""
    for l, m in product(COLORS, repeat=2):
        poly = GEN.row(l, m, GENERIC_WORD)
        require(poly.t, ("the generic row is empty", l, m))
        for monomial in poly.t:
            plist = [v for v in monomial if v.startswith("p_")]
            slist = [v for v in monomial if v.startswith("s_")]
            dlist = [v for v in monomial if v.startswith("d_")]
            if dlist:
                require(dlist == ["d_%d_%d" % (l, m)] and not plist and not slist,
                        ("a direct monomial is not d_lm", l, m, monomial))
            else:
                require(len(plist) == 1 and len(slist) == 1,
                        ("a star monomial is not p_l s_m", l, m, monomial))
                require(plist[0].startswith("p_%d_" % l), ("wrong p label", l, m))
                require(slist[0].startswith("s_%d_" % m), ("wrong s label", l, m))
    # and the induced action on the cubic: c_k -> (g_i/g_j)^{3-k} c_k.
    # DIAGONAL PAIRS ARE INCLUDED DELIBERATELY.  There the target weight is
    # (3-k)(e_i - e_j) = 0, so the torus fixes all four c_k and moves no root:
    # this note's "a root may not be named" argument gives NOTHING on a
    # diagonal line, and the check below is what establishes that.
    for i, j in ((0, 1), (2, 1), (0, 2), (0, 0), (1, 1), (2, 2)):
        coeffs = line_E(i, j)
        for k, coeff in enumerate(coeffs):
            for monomial in coeff.t:
                weight = [0, 0, 0]
                for v in monomial:
                    parts = v.split("_")
                    if v.startswith("p_"):
                        weight[int(parts[1])] += 1
                    elif v.startswith("s_"):
                        weight[int(parts[1])] -= 1
                    elif v.startswith("d_"):
                        weight[int(parts[1])] += 1
                        weight[int(parts[2])] -= 1
                want = [0, 0, 0]
                want[i] += 3 - k
                want[j] -= 3 - k
                require(weight == want,
                        ("c_%d is not (g_i/g_j)-homogeneous of weight %d"
                         % (k, 3 - k), i, j, monomial, weight))


# ==========================================================================
# 4.  univariate exact arithmetic in Q[z]
# ==========================================================================
def pnorm(a):
    a = tuple(a)
    while a and not a[-1]:
        a = a[:-1]
    return a


def pdivmod(a, b):
    a, b = list(pnorm(a)), list(pnorm(b))
    require(b, "division by the zero polynomial")
    quot = [Q(0)] * max(0, len(a) - len(b) + 1)
    while a and len(a) >= len(b):
        k = len(a) - len(b)
        c = a[-1] / b[-1]
        quot[k] = c
        for idx, bc in enumerate(b):
            a[k + idx] -= c * bc
        a = list(pnorm(a))
    return pnorm(quot), pnorm(a)


def pgcd(a, b):
    a, b = pnorm(a), pnorm(b)
    while b:
        a, b = b, pdivmod(a, b)[1]
    if not a:
        return ()
    return tuple(c / a[-1] for c in a)


def gcd_all(polys):
    g = ()
    for poly in polys:
        poly = pnorm(poly)
        if not poly:
            continue
        g = pgcd(g, poly) if g else poly
        if len(g) == 1:
            return (Q(1),)
    return tuple(c / g[-1] for c in g) if g else ()


def pmul(a, b):
    a, b = pnorm(a), pnorm(b)
    if not a or not b:
        return ()
    out = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    out[i + j] += x * y
    return pnorm(out)


def strip_activity(g, act):
    """divide out of g every factor shared with the activity divisor."""
    if not g or not act:
        return g
    cur = g
    while True:
        d = pgcd(cur, act)
        if len(d) <= 1:
            return cur
        cur = pdivmod(cur, d)[0]


def rank_of(rows, ncol):
    work = [list(r) + [Q(0)] * (ncol - len(r)) for r in rows]
    pivot = 0
    for col in range(ncol):
        sel = None
        for r in range(pivot, len(work)):
            if work[r][col]:
                sel = r
                break
        if sel is None:
            continue
        work[pivot], work[sel] = work[sel], work[pivot]
        scale = work[pivot][col]
        work[pivot] = [e / scale for e in work[pivot]]
        for r in range(len(work)):
            if r != pivot and work[r][col]:
                f = work[r][col]
                work[r] = [e - f * pe for e, pe in zip(work[r], work[pivot])]
        pivot += 1
    return pivot


# ==========================================================================
# 5.  the cubic table of one cap line of one numeric packet
# ==========================================================================
def line_cubics(pk, i, j):
    tau = sum((pk.de(c, c) for c in COLORS), Q(0))
    s = pnorm((pk.de(i, j), tau))
    kappa = {c: pnorm(((Q(1) if (i, j) == (c, c) else Q(0)), Q(1)))
             for c in COLORS}
    # a site can carry a response edge only if it carries a star entry
    star_live = [[any(pk.pe(l, x, c) or pk.se(l, x, c) for l in COLORS)
                  for c in COLORS] for x in SITES]
    cubics = {}
    for w in WORDS:
        if sum(1 for x in SITES if star_live[x][w[x]]) < 4:
            cubics[w] = ()          # fewer than two disjoint response edges
            continue
        R = {}
        live = 0
        for x, y in PAIRS:
            A = (pk.pe(i, x, w[x]) * pk.se(j, y, w[y])
                 + pk.pe(i, y, w[y]) * pk.se(j, x, w[x]))
            B = sum((pk.pe(l, x, w[x]) * pk.se(l, y, w[y])
                     + pk.pe(l, y, w[y]) * pk.se(l, x, w[x]) for l in COLORS),
                    Q(0))
            R[(x, y)] = pnorm((A, B))
            if R[(x, y)]:
                live += 1
        if live < 2:                       # Q2 = Q3 = 0 needs two R edges
            cubics[w] = ()
            continue
        qv = {e: pk.qe(e[0], e[1], w[e[0]], w[e[1]]) for e in PAIRS}
        Q2, Q3 = (), ()
        for matching in M6:
            for flags in product((0, 1), repeat=3):
                if sum(flags) < 2:
                    continue
                term = (Q(1),)
                for f, e in zip(flags, matching):
                    term = pmul(term, R[e]) if f else pnorm(
                        [c * qv[e] for c in term])
                    if not term:
                        break
                if not term:
                    continue
                if sum(flags) == 2:
                    Q2 = pnorm([a + b for a, b in zip(
                        list(Q2) + [Q(0)] * (len(term) - len(Q2)),
                        list(term) + [Q(0)] * (len(Q2) - len(term)))])
                else:
                    Q3 = pnorm([a + b for a, b in zip(
                        list(Q3) + [Q(0)] * (len(term) - len(Q3)),
                        list(term) + [Q(0)] * (len(Q3) - len(term)))])
        prod = pmul(s, Q2)
        n = max(len(prod), len(Q3))
        cubics[w] = pnorm([
            (prod[k] if k < len(prod) else Q(0))
            + (Q3[k] if k < len(Q3) else Q(0)) for k in range(n)])
    return cubics, s, kappa


_VERDICT_CACHE = {}


def packet_fingerprint(pk):
    """A key that depends on the packet's VALUES, not on its address.

    Keying this cache on ``id(pk)`` is a correctness bug, not an optimization
    detail: transient packets are garbage-collected and CPython reuses their
    addresses, so a later packet silently inherits an earlier packet's verdict.
    That made part of the random census self-fulfilling -- a rank drop in a
    recycled slot would never have been noticed.
    """

    return (
        tuple(sorted(pk.q.items())),
        tuple(sorted(pk.p.items())),
        tuple(sorted(pk.s.items())),
        tuple(sorted(pk.d.items())),
    )


def line_verdict(pk, i, j):
    key = (packet_fingerprint(pk), i, j)
    if key in _VERDICT_CACHE:
        return _VERDICT_CACHE[key]
    answer = _line_verdict(pk, i, j)
    _VERDICT_CACHE[key] = answer
    return answer


def _line_verdict(pk, i, j):
    cubics, s, kappa = line_cubics(pk, i, j)
    act = s
    for c in COLORS:
        act = pmul(act, kappa[c])
    nonzero = [c for c in cubics.values() if c]
    rank = rank_of(list(cubics.values()), 4)
    if not nonzero:
        gcd = None
    else:
        gcd = gcd_all(nonzero)
    residual = ()
    tau = sum((pk.de(c, c) for c in COLORS), Q(0))
    # homogenising K(t,u) = t E_ab + u I, the point t = 0 is K = I; it is a
    # common root exactly when every c_3 vanishes, and it is ACTIVE exactly
    # when tau = tr A_pq != 0 (there kappa_c = 1 and s = tau).
    infinity_root = all(len(c) < 4 for c in cubics.values())
    if not act:
        verdict = "line entirely inactive (s == 0)"
    elif gcd is None:
        verdict = "E vanishes identically: ACTIVE clean point at generic z"
    elif infinity_root and tau:
        verdict = "ACTIVE clean point at K = I"
    elif len(gcd) <= 1:
        verdict = "rootless (gcd one)"
    else:
        residual = strip_activity(gcd, act)
        if len(residual) > 1:
            residual = tuple(c / residual[-1] for c in residual)
            verdict = "ACTIVE clean point"
        else:
            residual = ()
            verdict = "clean points exist, ALL INACTIVE"
    return dict(cubics=cubics, s=s, kappa=kappa, act=act, gcd=gcd,
                rank=rank, nonzero=len(nonzero), verdict=verdict,
                residual=residual)


# ==========================================================================
# 6.  the named packets, copied from the committed checkers
# ==========================================================================
def _q(entries):
    out = {}
    for x, y, cx, cy, v in entries:
        if x > y:
            x, y, cx, cy = y, x, cy, cx
        out[(x, y, cx, cy)] = Q(v)
    return out


# seven-row guard: verify_h3_diagonal_segre_second_transgression_seven_row_guard
GUARD = Packet(
    _q([(0, 1, 2, 2, 1), (4, 5, 2, 2, 1)]),
    {(0, 0, 2): Q(1), (0, 1, 2): Q(1), (1, 4, 2): Q(1),
     (2, 2, 2): Q(1), (2, 3, 2): Q(1)},
    {(0, 5, 2): Q(1), (1, 2, 2): Q(1), (1, 3, 2): Q(-1),
     (2, 2, 2): Q(1, 2), (2, 3, 2): Q(1, 2)},
    {(0, 1): Q(1)},
)
# alternating eight-cycle: verify_monochromatic_internal_quadratic_structure
CYCLE = Packet(
    _q([(0, 1, 1, 1, 1), (1, 2, 0, 0, 1), (2, 3, 1, 1, 1),
        (3, 4, 0, 0, 1), (4, 5, 1, 1, 1)]),
    {(0, 0, 0): Q(1)}, {(0, 5, 0): Q(1)}, {(1, 1): Q(1)},
)
# pure-word anchor witness: verify_h3_star_sector_pure_word_anchor_witness
WITNESS = Packet(
    _q([(0, 1, 2, 2, 1), (4, 5, 2, 2, 1), (1, 5, 0, 0, 1), (2, 3, 0, 0, 1)]),
    {(0, 0, 2): Q(1), (0, 1, 2): Q(1), (1, 4, 2): Q(1),
     (2, 2, 2): Q(1), (2, 3, 2): Q(1), (0, 0, 0): Q(1)},
    {(0, 5, 2): Q(1), (1, 2, 2): Q(1), (1, 3, 2): Q(-1),
     (2, 2, 2): Q(1, 2), (2, 3, 2): Q(1, 2), (0, 4, 0): Q(1)},
    {(1, 0): Q(-1)},
)


def _stars(pvec, svec):
    return ({(i, x, 2): Q(v) for i, vec in pvec.items()
             for x, v in enumerate(vec) if v},
            {(j, y, 2): Q(v) for j, vec in svec.items()
             for y, v in enumerate(vec) if v})


# packets B and C: verify_h3_complementary_guard_star_sector_transport
_BP, _BS = _stars(
    {0: (1, 0, 0, 0, 1, 0), 1: (0, 0, 1, 0, 0, 0), 2: (0, 1, 0, 0, 0, 1)},
    {0: (0, -1, 0, 0, 0, 1), 1: (-1, 0, 0, 0, -1, 0), 2: (0, 0, 0, 0, 1, 0)})
PACKET_B = Packet(
    _q([(0, 1, 2, 2, 1), (2, 3, 2, 2, 1), (4, 5, 2, 2, 1)]),
    _BP, _BS, {(2, 1): Q(2)})
_CP, _CS = _stars(
    {0: (-1, 0, -1, -1, 0, -1), 1: (0, 0, 0, -1, 0, -1), 2: (0, 1, 0, 0, 0, 0)},
    {0: (-1, 0, 0, 0, 0, 0), 1: (0, -1, 0, 0, 1, 0), 2: (0, 0, 0, 0, 0, 1)})
PACKET_C = Packet(
    _q([(0, 1, 2, 2, 1), (2, 3, 2, 2, 1), (0, 4, 2, 2, 1), (2, 5, 2, 2, 1)]),
    _CP, _CS, {(0, 1): Q(1)})

# handoff-guide standard probe: the rank-two clean packet
_U = (1, -1, 2, 0, 1, 1)
_V = (1, 2, -2, 1, -2, 1)
RANK_TWO = Packet(
    _q([(0, 1, 2, 2, 1), (2, 3, 2, 2, 1), (4, 5, 2, 2, 1)]),
    {(0, x, 2): Q(v) for x, v in enumerate(_U) if v},
    {(1, y, 2): Q(v) for y, v in enumerate(_V) if v},
    {(0, 1): Q(-2)},
)

PURE2 = (2,) * 6
LEDGERS = {
    "seven-row guard": [(0, 0, (0,) * 6, Q(-1)), (1, 1, (1,) * 6, Q(-1))],
    "alternating eight-cycle": [(2, 2, (2,) * 6, Q(-1))],
    "pure-word anchor witness": [(0, 0, (2, 0, 0, 0, 0, 0), Q(1)),
                                 (1, 1, (1,) * 6, Q(-1))],
    "packet B": [(0, 0, (0,) * 6, Q(-1)), (1, 1, (1,) * 6, Q(-1))],
    "packet C": [(0, 0, (0,) * 6, Q(-1)), (1, 1, (1,) * 6, Q(-1))],
}
NAMED = (("seven-row guard", GUARD, (0, 1)),
         ("alternating eight-cycle", CYCLE, (1, 1)),
         ("pure-word anchor witness", WITNESS, (1, 0)),
         ("packet B", PACKET_B, (2, 1)),
         ("packet C", PACKET_C, (0, 1)))

# The exact per-line verdicts on each packet's own selected line, as measured;
# these are regression tripwires.  Residuals are monic, low degree first: the
# monic factor of the gcd left after every activity-divisor factor is removed.
#   guard  z^2 + 1/2      (roots z^2 = -1/2, active since s = 1 and kappa = z)
#   B      z^2 + z - 1    (roots (-1 +- sqrt 5)/2)
#   C      z^3 + 10/3 z^2 + 11/3 z + 4/3 = (z+1)^2 (z+4/3)
EXPECTED = {
    ("seven-row guard", (0, 1)):
        ("ACTIVE clean point", 1, 1, (Q(1, 2), Q(0), Q(1))),
    ("pure-word anchor witness", (1, 0)):
        ("clean points exist, ALL INACTIVE", 3, 7, ()),
    ("packet B", (2, 1)):
        ("ACTIVE clean point", 1, 1, (Q(-1), Q(1), Q(1))),
    ("packet C", (0, 1)):
        ("ACTIVE clean point", 1, 1, (Q(4, 3), Q(11, 3), Q(10, 3), Q(1))),
}


def all_rows(pk):
    """all 9 x 729 row coefficients, sharing the per-word hafnian tables."""
    out = {}
    for w in WORDS:
        qv = {e: pk.qe(e[0], e[1], w[e[0]], w[e[1]]) for e in PAIRS}
        full = Q(0)
        for matching in M6:
            term = Q(1)
            for e in matching:
                term *= qv[e]
                if not term:
                    break
            full += term
        rest = {}
        for e in PAIRS:
            total = Q(0)
            for matching in M4[e]:
                term = Q(1)
                for f in matching:
                    term *= qv[f]
                    if not term:
                        break
                total += term
            rest[e] = total
        for l, m in product(COLORS, repeat=2):
            value = pk.de(l, m) * full
            for x, y in PAIRS:
                resp = (pk.pe(l, x, w[x]) * pk.se(m, y, w[y])
                        + pk.pe(l, y, w[y]) * pk.se(m, x, w[x]))
                if resp:
                    value += resp * rest[(x, y)]
            out[(l, m, w)] = value
    return out


def audit_packet_ledgers():
    for name, pk, _sel in NAMED:
        rows = all_rows(pk)
        # cross-check the shared-table computation against the definition
        for probe in ((0, 1, (2,) * 6), (2, 2, (2,) * 6),
                      (1, 0, (2, 0, 0, 0, 0, 0))):
            require(rows[probe] == pk.row(*probe),
                    ("the shared-table row disagrees with the definition",
                     name, probe))
        ledger = sorted((l, m, w, v) for (l, m, w), v in rows.items()
                        for v in (v - ghz(l, m, w),) if v)
        require(ledger == sorted(LEDGERS[name]),
                ("published GHZ ledger not reproduced", name, ledger))


def audit_standard_probes():
    K01 = [[Q(1) if (l, m) == (0, 1) else Q(0) for m in COLORS] for l in COLORS]
    R = RANK_TWO.cap_R(K01, PURE2)
    require(RANK_TWO.layers(R, PURE2) == [Q(1), Q(2), Q(6), Q(12)],
            "rank-two clean packet layers changed")
    require(RANK_TWO.E_word(K01, PURE2) == 0,
            "rank-two clean packet is no longer clean")
    require(GUARD.E_word(K01, PURE2) == -2,
            "seven-row guard terminal class is no longer -2")
    require(PACKET_B.E_word(
        [[Q(1) if (l, m) == (2, 1) else Q(0) for m in COLORS] for l in COLORS],
        PURE2) == 4, "packet B terminal class changed")
    require(PACKET_C.E_word(K01, PURE2) == -4, "packet C terminal class changed")


def audit_named_lines():
    for name, pk, selected in NAMED:
        table = {}
        for i, j in product(COLORS, repeat=2):
            table[(i, j)] = line_verdict(pk, i, j)
        for i, j in product(COLORS, repeat=2):
            info = table[(i, j)]
            key = (name, (i, j))
            if key in EXPECTED:
                want_verdict, want_rank, want_nz, want_res = EXPECTED[key]
                require(info["verdict"] == want_verdict,
                        ("verdict changed", key, info["verdict"]))
                require(info["rank"] == want_rank and info["nonzero"] == want_nz,
                        ("rank/support changed", key, info["rank"],
                         info["nonzero"]))
                require(info["residual"] == want_res,
                        ("active residual changed", key, info["residual"]))
        # the eight-cycle has r^2 = 0, hence E == 0 on every line
        if name == "alternating eight-cycle":
            for i, j in product(COLORS, repeat=2):
                require(table[(i, j)]["gcd"] is None,
                        ("the eight-cycle lost E == 0", i, j))
            require(sum((CYCLE.de(c, c) for c in COLORS), Q(0)) == 1,
                    "the eight-cycle trace changed")
        # chi = 0 exactly on the witness, chi != 0 on the guard/B/C
        if name in ("seven-row guard", "packet B", "packet C"):
            info = table[selected]
            require(info["cubics"][PURE2] and info["cubics"][PURE2][0],
                    ("chi is zero on a guard packet", name))
        if name == "pure-word anchor witness":
            info = table[selected]
            for w in WORDS:
                c = info["cubics"][w]
                require(not c or c[0] == 0,
                        ("the witness has a nonzero chi coordinate", w))
            require(info["gcd"] == (Q(0), Q(1)),
                    ("the witness gcd is not exactly z", info["gcd"]))


# ==========================================================================
# 7.  rank criterion, and an unconstrained random census
# ==========================================================================
IDENTITY_LEDGER = {                       # (tr A_pq, #words with E(I) != 0)
    "seven-row guard": (Q(0), 0),
    "alternating eight-cycle": (Q(1), 0),
    "pure-word anchor witness": (Q(0), 2),
    "packet B": (Q(0), 0),
    "packet C": (Q(0), 1),
}


def audit_identity_cap():
    """K = I is the POINT AT INFINITY of the homogenization of every cap line;
    it is active iff tr A_pq != 0, and clean iff the leading tensor E(I)
    vanishes.  Only the eight-cycle has both."""
    ident = [[Q(1) if a == b else Q(0) for b in COLORS] for a in COLORS]
    for name, pk, _sel in NAMED:
        tau = sum((pk.de(c, c) for c in COLORS), Q(0))
        nonzero = sum(1 for w in WORDS if pk.E_word(ident, w))
        require((tau, nonzero) == IDENTITY_LEDGER[name],
                ("identity-cap ledger changed", name, tau, nonzero))
        if tau and not nonzero:
            require(name == "alternating eight-cycle",
                    ("an unexpected packet has an active clean identity cap",
                     name))


def audit_rank_criterion():
    """rank M <= 4 - deg gcd; so rank 4 forces gcd one (the rootless branch),
    and chi = 0 (a zero first column) forces rank <= 3 with root z = 0."""
    for name, pk, selected in NAMED:
        info = line_verdict(pk, *selected)
        gcd = info["gcd"]
        if gcd is not None and len(gcd) > 1:
            require(info["rank"] <= 4 - (len(gcd) - 1),
                    ("rank criterion violated", name, info["rank"], gcd))


class LCG(object):
    """explicit deterministic generator: no dependence on the random module."""

    def __init__(self, seed):
        self.state = seed & ((1 << 64) - 1)

    def next(self, bound):
        self.state = (6364136223846793005 * self.state + 1442695040888963407) \
            & ((1 << 64) - 1)
        return (self.state >> 33) % bound


def random_packet(gen, values=(-2, -1, 1, 2)):
    q, p, s, d = {}, {}, {}, {}
    for x, y in PAIRS:
        for cx, cy in product(COLORS, repeat=2):
            q[(x, y, cx, cy)] = Q(values[gen.next(len(values))])
    for l in COLORS:
        for x in SITES:
            for c in COLORS:
                p[(l, x, c)] = Q(values[gen.next(len(values))])
                s[(l, x, c)] = Q(values[gen.next(len(values))])
    for l, m in product(COLORS, repeat=2):
        d[(l, m)] = Q(values[gen.next(len(values))])
    return Packet(q, p, s, d)


def audit_random_census(trials=25):
    gen = LCG(20260801)
    seen = set()
    for trial in range(trials):
        pk = random_packet(gen)
        seen.add(packet_fingerprint(pk))
        info = line_verdict(pk, 0, 1)
        require(info["rank"] == 4,
                ("an unconstrained random packet dropped rank", trial,
                 info["rank"]))
        require(info["gcd"] == (Q(1),),
                ("an unconstrained random packet is not rootless", trial,
                 info["gcd"]))
    require(len(seen) == trials,
            ("the census drew a repeated packet, so the sample is smaller "
             "than advertised", len(seen), trials))


def torus_image(pk, g):
    """Apply the endpoint torus: p_l -> g_l p_l, s_m -> s_m / g_m, d_lm ->
    (g_l / g_m) d_lm, internal edges fixed."""

    p = {(l, x, c): g[l] * v for (l, x, c), v in pk.p.items()}
    s = {(m, y, c): v / g[m] for (m, y, c), v in pk.s.items()}
    d = {(l, m): g[l] / g[m] * v for (l, m), v in pk.d.items()}
    return Packet(dict(pk.q), p, s, d)


def audit_A6_numeric_diagonal_and_offdiagonal():
    """The claim the note makes about DIAGONAL lines, actually verified.

    On a diagonal line every one of the 729 cubics must be unchanged by the
    endpoint torus; on an off-diagonal line coefficient c_k must scale by
    (g_i/g_j)^{3-k}.  Without the diagonal half, the note's restriction of
    "a root may not be named" to off-diagonal lines has no artifact behind it.
    """

    gen = LCG(4242424)
    g = {0: Q(2), 1: Q(-3), 2: Q(5)}
    moved_offdiagonal = 0
    for trial in range(2):
        pk = random_packet(gen)
        img = torus_image(pk, g)
        for a in COLORS:
            base, _, _ = line_cubics(pk, a, a)
            shot, _, _ = line_cubics(img, a, a)
            require(base == shot,
                    ("the endpoint torus moved a diagonal-line cubic",
                     trial, a))
        for i, j in ((0, 1), (2, 1), (0, 2)):
            base, _, _ = line_cubics(pk, i, j)
            shot, _, _ = line_cubics(img, i, j)
            ratio = g[i] / g[j]
            require(set(base) == set(shot), "word sets differ under the torus")
            for w in base:
                require(len(base[w]) == len(shot[w]),
                        ("cubic degree changed under the torus", trial, i, j, w))
                for k, coeff in enumerate(base[w]):
                    want = coeff * ratio ** (3 - k)
                    require(shot[w][k] == want,
                            ("c_%d did not scale by (g_i/g_j)^%d"
                             % (k, 3 - k), trial, i, j, w))
                    if coeff and want != coeff:
                        moved_offdiagonal += 1
    require(moved_offdiagonal,
            "no off-diagonal coefficient actually moved -- the test is vacuous")


def main():
    audit_normalization()
    audit_A1_descent_note_formula()
    audit_A2_cap_reformulation()
    audit_A3_activity_ledger()
    audit_A4_four_coefficient_tensors()
    audit_A5_scalar_zero_point()
    audit_A6_target_stabilizing_torus()
    audit_A6_numeric_diagonal_and_offdiagonal()
    audit_packet_ledgers()
    audit_standard_probes()
    audit_named_lines()
    audit_identity_cap()
    audit_rank_criterion()
    audit_random_census()
    print(
        "PASS: E = (1/2)s r^2 x + (1/6)r^3 = s Q2 + Q3 formally; "
        "[z^0]E = chi and [z^3]E = E(I); every coordinate cap inactive; "
        "kappa_c(K_z) = delta + z; s(K_z) = alpha + z tau; "
        "rows are (g_i/g_j)-homogeneous so c_k -> (g_i/g_j)^{3-k} c_k; "
        "guard/B/C carry active clean points, the chi = 0 witness carries "
        "only the inactive root z = 0 with gcd exactly z; "
        "random packets have rank 4 and gcd one"
    )


if __name__ == "__main__":
    main()
