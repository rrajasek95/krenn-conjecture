#!/usr/bin/env python3
"""The identity cap E(I): what the nine rows force, and why proving the target
is exactly as hard as the open case at h = 3.

The target "the nine rows force tau != 0 and E(I) = 0" is vacuously TRUE if the
nine-row variety is empty and FALSE otherwise -- so proving it is equivalent to
proving emptiness, i.e. to the open (8,3) case.  It is not a usable
intermediate step.  (A vacuously true statement is true; "unreachable" would be
the wrong word for it.)

Research evidence only.  Krenn's conjecture remains OPEN, `SP-CLEAN-BRIDGE` is
untouched, and no certified dependency changes.  Nothing here is a partial case
of the conjecture.

Continues ``notes/cap-line-cubic-and-why-the-landing-is-inactive.md``, whose
section 3 raises the identity cap K = I as the ACTIVE analogue of the
chi = 0 landing (section 3 below prices it, and the price is prohibitive): I lies on every cap line, kappa_c(I) = 1, s(I) = tr A_pq = tau, so
E(I) = 0 together with tau != 0 would give the descent on any pair.  Everything
below is re-derived from the definitions in
``notes/clean-pair-cap-exact-descent-target.md``; nothing is imported from a
committed checker, and every committed ledger it overlaps is reproduced here.

Notation (six residual sites W, two endpoints, three colours; PACKET =
q,p,s,d as in ``notes/chart-model-is-the-official-eqsystem.md``):

    Row(i,j,w) = d_ij haf_w(q)
               + sum_{x<y} [p_i(x,w_x)s_j(y,w_y) + p_i(y,w_y)s_j(x,w_x)]
                 haf_w(q|W\\{x,y}),
    s(K)   = sum_lm K_lm d_lm,          kappa_c(K) = K_cc,
    R(K)^w_{xy} = sum_lm K_lm [p_l(x,w_x)s_m(y,w_y) + p_l(y,w_y)s_m(x,w_x)],
    Q_j    = R^[j] q^[3-j],             E(K)_w = s(K) Q_2 + Q_3,
    B      = R(I),  i.e. B_{xy} = sum_l [p_l(x)s_l(y) + p_l(y)s_l(x)],
    tau    = tr A_pq = d_00 + d_11 + d_22.

The 9 x 729 system is the full 3^8 coefficient system H_B(A) = Delta_{B,3} at
eight vertices, so a "nine-row solution" is exactly an exact ternary aggregate
source on eight vertices.

--------------------------------------------------------------------------
A.  SETUP, reproduced (formal identities in the 60 generic symbols one word
    exposes -- 15 q, 18 p, 18 s, 9 d are distinct block entries whatever the
    word, so each identity holds at all 729 words on every packet, with
    cross-colour internal edges live).

  A1  (1/2) s r^2 x + (1/6) r^3, full-U-support, equals s Q_2 + Q_3, on the
      coordinate caps, on K = I, and on a whole cap line.
  A2  on K_z = E_ab + zI, E is a cubic in z with [z^0] = chi and
      [z^3] = E(I), the latter independent of (a,b) across all nine lines.
  A3  E(I) = tau B^[2] q + B^[3], with B = R(I) and s(I) = tau.
  A4  THE TRACE ROW.  sum_l Row(l,l,w) = tau haf_w(q) + <B, H(q^w)>
      = tau G_0 + G_1 with G_j = B^[j] q^[3-j].  Hence
          E(I)_w = haf(tau q^w + B^w) - tau^2 sum_l Row(l,l,w).
      So the rows control exactly the FIRST jet of the identity-cap array
      tau q + B, and E(I) is its second jet.
  A5  for a fully generic 9-symbol cap K,
          haf_w(s q^w + R^w) = s^2 sum_lm K_lm Row(l,m,w) + E(K)_w.
  A6  the committed tau-weight grading (w_q,w_p,w_s,w_d) = (-1,1,1,3) puts
      every row monomial at weight 0 and every E(I) monomial at weight 6.
      So E(I), like chi, is NOT a function of the matching tensor: a theorem
      about it can only be a vanishing statement.

B.  E(I) IN PERMANENTS, and the exact linearity gap.  With N^w = P_w^T S_w,
    i.e. N^w_{xy} = sum_l p_l(x,w_x) s_l(y,w_y),

        B^[3]   = sum_{|X|=3} perm N^w[X, W\\X],
        B^[2]q  = sum_{u<v} q^w_uv sum_{|X|=2, X in W\\{u,v}} perm N^w[X, .],
        E(I)_w  = tau (B^[2]q) + B^[3].

    Every row is LINEAR in N (the trace row is tau haf_w(q) + <H_w, N+N^T>,
    and the nine rows are the matrix identity haf_w(q) d + P_w H_w S_w^T
    = Delta(w)).  E(I) is quadratic plus cubic in N.  That degree gap, not a
    missing relation, is where the obstruction lives.

C.  THE CERTIFICATE CLOSURE.  Grade by site-colour degree together with the
    two endpoint-label degrees, as in
    ``notes/terminal-class-ideal-membership-multigrading-bounds.md``.

  C1  every Row(i,j,w) is multihomogeneous of degree (sigma(w), e_i, e_j) and
      has d-degree <= 1.  Checked on seven probe words, not all 729; the
      grading argument is structural and word-uniform.
  C2  every E(I)_w monomial has site-colour degree sigma(w), is label
      BALANCED (left degree = right degree = nu, |nu| = 3; all ten nu occur),
      and has d-degree <= 1.  Same seven probe words.
  C3  sigma(w') <= sigma(w) forces w' = w (checked on all 729^2 pairs), and
      the only monomials of site-colour degree zero are monomials in d.
  C4  hence at E(I)'s own multidegree (sigma(w), nu, nu) the ONLY available
      generators are the nine rows AT THE SAME WORD w with i,j in supp(nu),
      and each is forced to carry a d-monomial multiplier of degree exactly
      two.  Every such contribution has d-degree in {2,3}; every monomial of
      E(I) has d-degree in {0,1}.  So the row sector cannot contribute at
      E(I)'s own d-degrees {0,1}, and its {2,3} contribution has to cancel
      against the anchor multipliers: the target itself must be handed over
      by the three pure-word anchor multipliers' constants.

      This is the SAME conclusion, reached by the same filter, that
      ``notes/terminal-class-ideal-membership-multigrading-bounds.md``
      reaches for chi -- not a worse one.  There chi has one admissible
      generator d_01^2 Row(0,1,2^6); here E(I) has 36 across the ten
      balanced nu.  Both sit at d-degrees {2,3} against a target at {0,1},
      and both targets have an exact cap split:
          haf(alpha q + A) = alpha^2 Row(a,b,w) + chi,
          haf(tau q + B)   = tau^2 sum_l Row(l,l,w) + E(I).
      If anything E(I) has strictly MORE row-sector freedom than chi.
      Note also that the three anchor generators Row(c,c,c^6) - 1 are
      INHOMOGENEOUS, so the multigraded argument needs the two-component
      treatment (degree-D^* part and constant part) separately.

D.  WHAT THE FULL SYSTEM FORCES -- the decisive item.  This is the N = 8 base
    case of Corollary 5.1 of ``notes/clean-pair-cap-exact-descent-target.md``
    (`SP-DESCENT`), re-derived at the AGGREGATE level so that the decorated-
    source reconstruction of that note's Theorem 1.1 is not needed: the
    argument uses only A5, verified here, and the certified `SP-K6`
    (``proofs/six-site-arbitrary-complex-obstruction.md``).

      Let the packet satisfy all 6561 rows and let K be ANY cap with
      s kappa_0 kappa_1 kappa_2 != 0 and E(K) = 0.  By A5 the six-site
      aggregate array A_cap = s q + R(K) has
          H_6(A_cap) = sum_c s^2 kappa_c X_c^U .
      Rescaling the blocks at one site u_0 by mu_c = 1/(s^2 kappa_c) on its
      colour axis is invertible and, by multilinearity (D1 below), turns this
      into Delta_{6,3}.  `SP-K6` says no complex six-site block array has that
      matching tensor.  Contradiction.

    Hence, unconditionally:

      D2  NO solution of the nine-row system admits an active clean cap.  In
          particular, on the nine-row variety,  tau != 0  ==>  E(I) != 0.
      D3  "the nine rows force tau != 0 and E(I) = 0" is EQUIVALENT to the
          emptiness of the nine-row variety, i.e. to the open (8,3) case:
          it implies emptiness by D2, and is vacuously true if empty.
      D4  the same for every cap, so `SP-CLEAN-BRIDGE` AT N = 8 is equivalent
          to the (8,3) case.  Its first boundary cannot be crossed by any
          argument short of settling that case, and the identity-cap target
          inherits exactly that status.

    D1 (multilinearity of the diagonal site map) is verified here as a formal
    identity, and its normalization step is exercised on the alternating
    SIX-cycle, the SP-K6 near-miss whose tensor is X_0 + X_1.  D2-D4 are the
    one-line deductions above: they are recorded, not machine-checked, and
    they inherit `SP-K6`.

E.  THE PACKET TABLE, with the support-concentration caveat applied, and

F.  THE 6559-ROW GUARDS.  Packet C and the seven-row guard both have
    haf_w(q) = 0 at every word, so their whole direct block d is FREE: every
    d gives the same 6559-row ledger, failing exactly the anchors (0,0,0^6)
    and (1,1,1^6).  Then
      * packet C with d = I has tau = 3 != 0 and E(I) = -3 at the word 2^6
        (for EVERY d, since its B^[2]q vanishes) -- an ACTIVE, UNCLEAN
        identity cap;
      * the seven-row guard with d = I has tau = 3 != 0 and E(I) = 0 in all
        729 coordinates -- an ACTIVE, CLEAN identity cap.
    Both verdicts are reachable at 6559 rows, so 6559 rows decide nothing:
    the two pure-word anchors are exactly the load-bearing equations, which
    is the same conclusion the seven-row guard reaches for chi.

G.  THE KNOWN 6560 FAMILY.  All 56 endpoint charts of the alternating
    eight-cycle sit at 6560 rows, failing only the colour-2 anchor, and all 56
    have E(I) = 0 -- but NOT all for the same reason, and "by star-rank one"
    is false for 24 of them.  The census, by endpoint distance, is

        distance 1: 16 charts, tau = 1, at most 1 live edge per word
        distance 2: 16 charts, tau = 0, at most 1 live edge per word
        distance 3: 16 charts, tau = 0, 2 live edges at some word
        distance 4:  8 charts, tau = 0, 2 live edges at some word

    (live edges are counted PER WORD -- B^[2] and B^[3] at a word need two or
    three edges live at THAT word.)  So:

      * on the 32 charts of distance one and two, star-rank one applies:
        a single live response edge gives B^[2] = B^[3] = 0 identically;
      * on the 24 charts of distance three and four it does NOT.  There
        E(I) = 0 for a different reason: tau = 0 kills the tau B^[2] q term,
        and two live edges cannot fill a three-edge matching, so B^[3] = 0.

    The 16 distance-one charts are the only ACTIVE ones, so their clean
    identity cap is support concentration, not signal.

Krenn's conjecture remains open; the (8,3) system's feasibility is untouched.
Python standard library only, exact Fraction arithmetic, deterministic across
PYTHONHASHSEED, live under ``python3 -O`` and ``python3 -I -S``.
"""

from fractions import Fraction as Q
from itertools import combinations, permutations, product

SITES = tuple(range(6))
COLORS = (0, 1, 2)
PAIRS = tuple(combinations(SITES, 2))
WORDS = tuple(product(COLORS, repeat=6))
PURE2 = (2,) * 6


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
M4 = {e: perfect_matchings(tuple(s for s in SITES if s not in e))
      for e in PAIRS}


def audit_normalization():
    require(len(M6) == 15, "six-site all-ones hafnian is not 15")
    require(len(perfect_matchings((0, 1, 2, 3))) == 3, "four-site is not 3")
    require(len(perfect_matchings(tuple(range(8)))) == 105, "K8 count")
    polar = {e: sum((Q(1) for _ in M4[e]), Q(0)) for e in PAIRS}
    require(sum((Q(1) for _ in M6), Q(0)) == 15, "haf normalization")
    require(polar[(0, 1)] == 3, "polar normalization")
    double = Q(0)
    for matching in M4[(0, 1)]:
        term = Q(1)
        for x, y in matching:
            term *= polar[(min(x, y), max(x, y))]
        double += term
    require(double == 27, "all-ones double polar is not 27")
    require(double - 15 * 1 == 12, "all-ones double-polar defect is not 12")


# ==========================================================================
# 1.  sparse multivariate polynomials over Q
# ==========================================================================
class P(object):
    __slots__ = ("t",)

    def __init__(self, terms=None):
        self.t = {} if terms is None else {m: c for m, c in terms.items() if c}

    @staticmethod
    def const(value):
        value = Q(value)
        return P({(): value}) if value else P()

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
        for mono, coeff in other.t.items():
            new = out.get(mono, Q(0)) + coeff
            if new:
                out[mono] = new
            else:
                out.pop(mono, None)
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
                mono = tuple(sorted(m1 + m2))
                new = out.get(mono, Q(0)) + c1 * c2
                if new:
                    out[mono] = new
                else:
                    out.pop(mono, None)
        return P(out)

    def split(self, name):
        buckets = {}
        for mono, coeff in self.t.items():
            k = sum(1 for v in mono if v == name)
            rest = tuple(v for v in mono if v != name)
            box = buckets.setdefault(k, {})
            new = box.get(rest, Q(0)) + coeff
            if new:
                box[rest] = new
            else:
                box.pop(rest, None)
        top = max(buckets) if buckets else 0
        return [P(buckets.get(k, {})) for k in range(top + 1)]


# ==========================================================================
# 2.  the block-array model (Fraction or P entries)
# ==========================================================================
class Packet(object):
    """q[(x,y,cx,cy)] with x<y, p[(l,x,c)], s[(m,y,c)], d[(l,m)]."""

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

    def qword(self, w):
        return {e: self.qe(e[0], e[1], w[e[0]], w[e[1]]) for e in PAIRS}

    def haf(self, value, matchings=M6):
        total = self.zero
        for matching in matchings:
            term = self.one
            for x, y in matching:
                term = term * value[(x, y) if x < y else (y, x)]
                if not term:
                    break
            total = total + term
        return total

    def fourhole(self, qv):
        return {e: self.haf(qv, M4[e]) for e in PAIRS}

    def response(self, l, m, w):
        return {(x, y): (self.pe(l, x, w[x]) * self.se(m, y, w[y])
                         + self.pe(l, y, w[y]) * self.se(m, x, w[x]))
                for x, y in PAIRS}

    def row(self, l, m, w):
        qv = self.qword(w)
        holes = self.fourhole(qv)
        total = self.de(l, m) * self.haf(qv)
        resp = self.response(l, m, w)
        for e in PAIRS:
            if resp[e]:
                total = total + resp[e] * holes[e]
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
                value = (self.pe(l, x, w[x]) * self.se(m, y, w[y])
                         + self.pe(l, y, w[y]) * self.se(m, x, w[x]))
                if value:
                    total = total + K[l][m] * value
            out[(x, y)] = total
        return out

    def layers(self, R, w):
        qv = self.qword(w)
        out = [self.zero] * 4
        for matching in M6:
            for flags in product((0, 1), repeat=3):
                term = self.one
                for flag, (x, y) in zip(flags, matching):
                    key = (x, y) if x < y else (y, x)
                    term = term * (R[key] if flag else qv[key])
                    if not term:
                        break
                if term:
                    k = sum(flags)
                    out[k] = out[k] + term
        return out

    def E(self, K, w):
        L = self.layers(self.cap_R(K, w), w)
        return self.cap_s(K) * L[2] + L[3]

    def tau(self):
        return self.de(0, 0) + self.de(1, 1) + self.de(2, 2)

    def trace_response(self, w):
        out = {}
        for x, y in PAIRS:
            total = self.zero
            for l in COLORS:
                total = total + (self.pe(l, x, w[x]) * self.se(l, y, w[y])
                                 + self.pe(l, y, w[y]) * self.se(l, x, w[x]))
            out[(x, y)] = total
        return out


def identity_cap():
    return [[Q(1) if a == b else Q(0) for b in COLORS] for a in COLORS]


def ghz(l, m, w):
    return Q(1) if (l == m and all(c == l for c in w)) else Q(0)


def _star_tables(pk, w):
    """P_w[l][x] = p_l(x, w_x) and S_w[m][y] = s_m(y, w_y)."""
    return ([[pk.pe(l, x, w[x]) for x in SITES] for l in COLORS],
            [[pk.se(m, y, w[y]) for y in SITES] for m in COLORS])


def ledger(pk):
    """(Row - GHZ) over all 6561 coefficients, nonzero entries only."""
    out = []
    labels = tuple(product(COLORS, repeat=2))
    for w in WORDS:
        qv = pk.qword(w)
        full = pk.haf(qv)
        holes = pk.fourhole(qv)
        live = [e for e in PAIRS if holes[e]]
        if not full and not live:
            for l, m in labels:
                if ghz(l, m, w):
                    out.append((l, m, w, -ghz(l, m, w)))
            continue
        Pw, Sw = _star_tables(pk, w)
        for l, m in labels:
            value = pk.de(l, m) * full
            pl, sm = Pw[l], Sw[m]
            for x, y in live:
                resp = pl[x] * sm[y] + pl[y] * sm[x]
                if resp:
                    value += resp * holes[(x, y)]
            if value != ghz(l, m, w):
                out.append((l, m, w, value - ghz(l, m, w)))
    return sorted(out)


def trace_response_at(pk, w, Pw=None, Sw=None):
    if Pw is None:
        Pw, Sw = _star_tables(pk, w)
    out = {}
    for x, y in PAIRS:
        out[(x, y)] = sum((Pw[l][x] * Sw[l][y] + Pw[l][y] * Sw[l][x]
                           for l in COLORS), Q(0))
    return out


def live_trace_edges(pk):
    """the largest number of live trace-response edges over all words."""
    best = 0
    for w in WORDS:
        Pw, Sw = _star_tables(pk, w)
        if not any(any(row) for row in Pw) or not any(any(r) for r in Sw):
            continue
        B = trace_response_at(pk, w, Pw, Sw)
        best = max(best, sum(1 for e in PAIRS if B[e]))
    return best


def identity_cap_support(pk):
    """the words where E(I) != 0.  A word whose trace response has no two
    disjoint live edges has Q_2 = Q_3 = 0 and is skipped."""
    out = {}
    K = identity_cap()
    for w in WORDS:
        Pw, Sw = _star_tables(pk, w)
        if not any(any(row) for row in Pw) or not any(any(r) for r in Sw):
            continue
        B = trace_response_at(pk, w, Pw, Sw)
        live = [e for e in PAIRS if B[e]]
        if len(live) < 2:
            continue
        if not any(not (set(a) & set(b)) for a in live for b in live):
            continue
        value = pk.E(K, w)
        if value:
            out[w] = value
    return out


# ==========================================================================
# 3.  block A: the setup, formally, in the 60 generic symbols of one word
# ==========================================================================
GENERIC_WORD = (0,) * 6
_QS = {e: P.var("q_%d_%d" % e) for e in PAIRS}
_PS = {(l, x): P.var("p_%d_%d" % (l, x)) for l in COLORS for x in SITES}
_SS = {(m, y): P.var("s_%d_%d" % (m, y)) for m in COLORS for y in SITES}
_DS = {(l, m): P.var("d_%d_%d" % (l, m)) for l in COLORS for m in COLORS}
GEN = Packet(q={(x, y, 0, 0): v for (x, y), v in _QS.items()},
             p={(l, x, 0): v for (l, x), v in _PS.items()},
             s={(m, y, 0): v for (m, y), v in _SS.items()},
             d=dict(_DS), symbolic=True)
ZVAR = P.var("z")
IDENT_P = [[P.const(1) if a == b else P() for b in COLORS] for a in COLORS]
TAU_P = _DS[(0, 0)] + _DS[(1, 1)] + _DS[(2, 2)]


def coord_cap(i, j):
    return [[P.const(1) if (a, b) == (i, j) else P() for b in COLORS]
            for a in COLORS]


def line_cap(i, j):
    return [[(P.const(1) if (a, b) == (i, j) else P())
             + (ZVAR if a == b else P()) for b in COLORS] for a in COLORS]


def squarefree_mul(f, g):
    out = {}
    for s1, v1 in f.items():
        for s2, v2 in g.items():
            if s1 & s2:
                continue
            key = s1 | s2
            out[key] = out.get(key, P()) + v1 * v2
    return {k: v for k, v in out.items() if v}


def audit_A1_descent_note_formula():
    full = frozenset(SITES)
    for K, tag in ((coord_cap(0, 1), "E_01"), (coord_cap(2, 2), "E_22"),
                   (IDENT_P, "I"), (line_cap(1, 0), "E_10 + zI")):
        R = GEN.cap_R(K, GENERIC_WORD)
        sK = GEN.cap_s(K)
        r = {frozenset(e): R[e] for e in PAIRS if R[e]}
        x = {frozenset(e): _QS[e] for e in PAIRS}
        r2 = squarefree_mul(r, r)
        L = GEN.layers(R, GENERIC_WORD)
        require(P.const(Q(1, 2)) * squarefree_mul(r2, x).get(full, P()) == L[2],
                ("r^2 x / 2 is not Q_2", tag))
        require(P.const(Q(1, 6)) * squarefree_mul(r2, r).get(full, P()) == L[3],
                ("r^3 / 6 is not Q_3", tag))
        lhs = (P.const(Q(1, 2)) * sK * squarefree_mul(r2, x).get(full, P())
               + P.const(Q(1, 6)) * squarefree_mul(r2, r).get(full, P()))
        require(lhs == sK * L[2] + L[3],
                ("(1/2) s r^2 x + (1/6) r^3 is not s Q_2 + Q_3", tag))


def audit_A2_cap_line_cubic():
    top = None
    for i, j in product(COLORS, repeat=2):
        coeffs = GEN.E(line_cap(i, j), GENERIC_WORD).split("z")
        require(len(coeffs) == 4, ("E is not a cubic in z", i, j))
        Rc = GEN.cap_R(coord_cap(i, j), GENERIC_WORD)
        Lc = GEN.layers(Rc, GENERIC_WORD)
        require(coeffs[0] == _DS[(i, j)] * Lc[2] + Lc[3],
                ("[z^0] E is not chi", i, j))
        if top is None:
            top = coeffs[3]
        else:
            require(coeffs[3] == top, ("[z^3] E depends on (a,b)", i, j))
        kappa = [line_cap(i, j)[c][c] for c in COLORS]
        require(kappa == [(P.const(1) if i == j == c else P()) + ZVAR
                          for c in COLORS], ("kappa ledger changed", i, j))
        require(GEN.cap_s(line_cap(i, j)).split("z")
                == [_DS[(i, j)], TAU_P], ("s(K_z) is not alpha + z tau", i, j))
    require(top == GEN.E(IDENT_P, GENERIC_WORD),
            "[z^3] E is not the identity cap's clean error")


def audit_A3_identity_cap_layers():
    B = GEN.trace_response(GENERIC_WORD)
    require(B == GEN.cap_R(IDENT_P, GENERIC_WORD), "B is not R(I)")
    require(GEN.cap_s(IDENT_P) == TAU_P, "s(I) is not tr A_pq")
    L = GEN.layers(B, GENERIC_WORD)
    require(GEN.E(IDENT_P, GENERIC_WORD) == TAU_P * L[2] + L[3],
            "E(I) is not tau B^[2] q + B^[3]")


def audit_A4_trace_row():
    trace_row = P()
    for l in COLORS:
        trace_row = trace_row + GEN.row(l, l, GENERIC_WORD)
    qv = GEN.qword(GENERIC_WORD)
    holes = GEN.fourhole(qv)
    B = GEN.trace_response(GENERIC_WORD)
    paired = P()
    for e in PAIRS:
        paired = paired + B[e] * holes[e]
    require(trace_row == TAU_P * GEN.haf(qv) + paired,
            "sum_l Row(l,l,w) is not tau haf(q) + <B, H(q)>")
    L = GEN.layers(B, GENERIC_WORD)
    require(trace_row == TAU_P * L[0] + L[1],
            "the trace row is not tau G_0 + G_1")
    cap_array = {e: TAU_P * qv[e] + B[e] for e in PAIRS}
    require(GEN.haf(cap_array)
            == TAU_P * TAU_P * trace_row + GEN.E(IDENT_P, GENERIC_WORD),
            "haf(tau q + B) is not tau^2 (trace row) + E(I)")


def audit_A5_generic_cap_reformulation():
    KS = [[P.var("K_%d_%d" % (l, m)) for m in COLORS] for l in COLORS]
    sK = GEN.cap_s(KS)
    R = GEN.cap_R(KS, GENERIC_WORD)
    qv = GEN.qword(GENERIC_WORD)
    rowsum = P()
    for l, m in product(COLORS, repeat=2):
        rowsum = rowsum + KS[l][m] * GEN.row(l, m, GENERIC_WORD)
    L = GEN.layers(R, GENERIC_WORD)
    require(sK * L[0] + L[1] == rowsum,
            "s Q_0 + Q_1 is not sum_lm K_lm Row(l,m,w)")
    cap_array = {e: sK * qv[e] + R[e] for e in PAIRS}
    require(GEN.haf(cap_array) == sK * sK * rowsum + GEN.E(KS, GENERIC_WORD),
            "haf(s q + R) is not s^2 <K, H_B(A)> + E(K)")


def audit_A6_tau_weight():
    weight = {"q": -1, "p": 1, "s": 1, "d": 3}
    for l, m in product(COLORS, repeat=2):
        poly = GEN.row(l, m, GENERIC_WORD)
        require(poly.t, ("the generic row is empty", l, m))
        for mono in poly.t:
            require(sum(weight[v[0]] for v in mono) == 0,
                    ("a row monomial is not tau-weight zero", l, m, mono))
    for K, tag in ((IDENT_P, "E(I)"), (coord_cap(0, 1), "chi")):
        poly = GEN.E(K, GENERIC_WORD)
        require(poly.t, ("the generic clean error is empty", tag))
        for mono in poly.t:
            require(sum(weight[v[0]] for v in mono) == 6,
                    ("a clean-error monomial is not tau-weight six", tag, mono))


# ==========================================================================
# 4.  block B: the permanent formula and the linearity gap
# ==========================================================================
_QF = {(x, y, a, b): P.var("q.%d.%d.%d.%d" % (x, y, a, b))
       for x, y in PAIRS for a in COLORS for b in COLORS}
_PF = {(l, x, c): P.var("p.%d.%d.%d" % (l, x, c))
       for l in COLORS for x in SITES for c in COLORS}
_SF = {(m, y, c): P.var("s.%d.%d.%d" % (m, y, c))
       for m in COLORS for y in SITES for c in COLORS}
_DF = {(l, m): P.var("d.%d.%d" % (l, m)) for l in COLORS for m in COLORS}
WORDED = Packet(q=dict(_QF), p=dict(_PF), s=dict(_SF), d=dict(_DF),
                symbolic=True)
TAU_F = _DF[(0, 0)] + _DF[(1, 1)] + _DF[(2, 2)]
IDENT_F = IDENT_P
PROBES = ((0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1), (2, 2, 2, 2, 2, 2),
          (0, 1, 2, 0, 1, 2), (2, 0, 0, 1, 2, 1), (0, 1, 1, 2, 2, 0),
          (1, 2, 0, 0, 0, 2))


def _N(w):
    return {(x, y): sum((_PF[(l, x, w[x])] * _SF[(l, y, w[y])]
                         for l in COLORS), P())
            for x in SITES for y in SITES if x != y}


def _perm_block(N, X, Y):
    total = P()
    for pi in permutations(tuple(sorted(Y))):
        term = P.const(1)
        for x, y in zip(tuple(sorted(X)), pi):
            term = term * N[(x, y)]
            if not term:
                break
        total = total + term
    return total


def audit_B_permanent_formula():
    for w in PROBES[:4]:
        N = _N(w)
        qv = WORDED.qword(w)
        cubic = P()
        for X in combinations(SITES, 3):
            cubic = cubic + _perm_block(
                N, X, tuple(s for s in SITES if s not in X))
        quad = P()
        for u, v in PAIRS:
            rest = tuple(s for s in SITES if s not in (u, v))
            inner = P()
            for X in combinations(rest, 2):
                inner = inner + _perm_block(
                    N, X, tuple(s for s in rest if s not in X))
            quad = quad + qv[(u, v)] * inner
        L = WORDED.layers(WORDED.trace_response(w), w)
        require(cubic == L[3], ("B^[3] is not sum_X perm N[X, X^c]", w))
        require(quad == L[2], ("B^[2]q is not the permanent sum", w))
        require(TAU_F * quad + cubic == WORDED.E(IDENT_F, w),
                ("the permanent formula for E(I) failed", w))


def audit_B_rows_are_linear_in_N():
    for w in PROBES[:3]:
        qv = WORDED.qword(w)
        holes = WORDED.fourhole(qv)
        N = _N(w)
        lhs = P()
        for l in COLORS:
            lhs = lhs + WORDED.row(l, l, w)
        rhs = TAU_F * WORDED.haf(qv)
        for x, y in PAIRS:
            rhs = rhs + holes[(x, y)] * (N[(x, y)] + N[(y, x)])
        require(lhs == rhs,
                ("the trace row is not tau haf(q) + <H, N + N^T>", w))
        # and the nine rows are the matrix identity haf(q) d + P H S^T
        for i, j in product(COLORS, repeat=2):
            star = P()
            for x in SITES:
                for y in SITES:
                    if x != y:
                        star = star + (_PF[(i, x, w[x])] * holes[
                            (min(x, y), max(x, y))] * _SF[(j, y, w[y])])
            require(WORDED.row(i, j, w) == _DF[(i, j)] * WORDED.haf(qv) + star,
                    ("Row is not haf(q) d + (P H S^T)", i, j, w))


# ==========================================================================
# 5.  block C: the multigrading closure
# ==========================================================================
def multidegree(mono):
    """(site-colour vector, left-label vector, right-label vector, d-degree)"""
    sc = [0] * 18
    left = [0, 0, 0]
    right = [0, 0, 0]
    ddeg = 0
    for v in mono:
        f = v.split(".")
        if f[0] == "q":
            x, y, a, b = int(f[1]), int(f[2]), int(f[3]), int(f[4])
            sc[3 * x + a] += 1
            sc[3 * y + b] += 1
        elif f[0] == "p":
            sc[3 * int(f[2]) + int(f[3])] += 1
            left[int(f[1])] += 1
        elif f[0] == "s":
            sc[3 * int(f[2]) + int(f[3])] += 1
            right[int(f[1])] += 1
        else:
            left[int(f[1])] += 1
            right[int(f[2])] += 1
            ddeg += 1
    return tuple(sc), tuple(left), tuple(right), ddeg


def sigma(w):
    sc = [0] * 18
    for x in SITES:
        sc[3 * x + w[x]] += 1
    return tuple(sc)


def audit_C1_rows_multihomogeneous():
    for w in PROBES:
        for i, j in product(COLORS, repeat=2):
            poly = WORDED.row(i, j, w)
            require(poly.t, ("empty row", i, j, w))
            ei = tuple(1 if c == i else 0 for c in COLORS)
            ej = tuple(1 if c == j else 0 for c in COLORS)
            for mono in poly.t:
                sc, left, right, ddeg = multidegree(mono)
                require((sc, left, right) == (sigma(w), ei, ej),
                        ("row multidegree", i, j, w, mono))
                require(ddeg <= 1, ("row monomial with d-degree > 1", mono))


def audit_C2_identity_error_balanced():
    seen = set()
    for w in PROBES:
        poly = WORDED.E(IDENT_F, w)
        require(poly.t, ("empty E(I)", w))
        for mono in poly.t:
            sc, left, right, ddeg = multidegree(mono)
            require(sc == sigma(w), ("E(I) site-colour degree", w, mono))
            require(left == right, ("E(I) monomial is not balanced", w, mono))
            require(sum(left) == 3, ("E(I) label degree is not three", w, mono))
            require(ddeg <= 1, ("E(I) monomial with d-degree > 1", w, mono))
            seen.add(left)
    balanced = {nu for nu in product(range(4), repeat=3) if sum(nu) == 3}
    require(seen == balanced and len(balanced) == 10,
            ("not all ten balanced label degrees occur", len(seen)))


def audit_C3_site_colour_order():
    live = {w: frozenset(3 * x + w[x] for x in SITES) for w in WORDS}
    for w in WORDS:
        require(sum(sigma(w)) == 6 and len(live[w]) == 6,
                ("sigma(w) is not a one-per-site indicator", w))
        target = live[w]
        for wp in WORDS:
            if wp != w and live[wp] <= target:
                raise AssertionError(("a second word sits below sigma(w)",
                                      w, wp))
    for table in (_QF, _PF, _SF):
        for v in table.values():
            sc = multidegree(list(v.t)[0])[0]
            require(sum(sc) > 0,
                    "a non-direct variable has site-colour degree zero")
    for v in _DF.values():
        sc, _, _, ddeg = multidegree(list(v.t)[0])
        require(sum(sc) == 0 and ddeg == 1,
                "a direct scalar has nonzero site-colour degree")


def audit_C4_row_sector_inert():
    """At (sigma(w), nu, nu) the only generators below are the same word's
    rows with i,j in supp(nu); each is forced to carry a degree-two
    d-monomial multiplier, so contributes only d-degrees {2,3}, while every
    E(I) monomial has d-degree in {0,1}."""
    nus = [nu for nu in product(range(4), repeat=3) if sum(nu) == 3]
    require(len(nus) == 10, "there are not ten balanced label degrees")
    census = {}
    for nu in nus:
        support = [c for c in COLORS if nu[c] > 0]
        admissible = 0
        for i, j in product(COLORS, repeat=2):
            left = tuple(nu[c] - (1 if c == i else 0) for c in COLORS)
            right = tuple(nu[c] - (1 if c == j else 0) for c in COLORS)
            if min(left) < 0 or min(right) < 0:
                require(i not in support or j not in support,
                        ("a supported label was rejected", nu, i, j))
                continue
            require(i in support and j in support,
                    ("an unsupported label was admitted", nu, i, j))
            require(sum(left) == 2 and sum(right) == 2,
                    "the forced multiplier is not of degree two")
            monomials = [(a, b) for a in product(COLORS, repeat=2)
                         for b in product(COLORS, repeat=2)
                         if (tuple(sum(1 for t in (a[0], b[0]) if t == c)
                                   for c in COLORS) == left
                             and tuple(sum(1 for t in (a[1], b[1]) if t == c)
                                       for c in COLORS) == right)]
            require(monomials, ("no d-monomial realizes the multiplier",
                                nu, i, j))
            admissible += 1
        require(admissible == len(support) ** 2,
                ("admissible generator count", nu, admissible))
        census[nu] = admissible
    # 3 x 1^2 (nu = 3e_c) + 6 x 2^2 (nu = 2e_a + e_b) + 1 x 3^2 (nu = 1,1,1)
    require(sum(census.values()) == 36,
            ("total admissible generator census changed", sum(census.values())))
    # a degree-two d-multiplier puts every row contribution at d-degree 2 or 3,
    # while every monomial of E(I) has d-degree 0 or 1: the sectors are
    # disjoint, so the row sector is inert at E(I)'s multidegree.
    for w in PROBES[:2]:
        for i, j in product(COLORS, repeat=2):
            for mono in WORDED.row(i, j, w).t:
                require(multidegree(mono)[3] + 2 in (2, 3),
                        ("row contribution d-degree", i, j, w, mono))
        for mono in WORDED.E(IDENT_F, w).t:
            require(multidegree(mono)[3] in (0, 1),
                    ("E(I) d-degree", w, mono))


# ==========================================================================
# 6.  block D: the SP-K6 obstruction (its one formal ingredient)
# ==========================================================================
def audit_D1_diagonal_site_map():
    """Rescaling the blocks at one site by mu on its colour axis multiplies
    every coordinate H_6(A)_w by mu_{w(u0)}."""
    mu = [P.var("mu_%d" % c) for c in COLORS]
    blank = Packet(q={}, p={}, s={}, d={}, symbolic=True)
    for u0 in (0, 3, 5):
        for w in ((0,) * 6, (0, 1, 2, 0, 1, 2), (2, 2, 1, 0, 0, 1)):
            A = {e: P.var("A.%d.%d.%d.%d" % (e[0], e[1], w[e[0]], w[e[1]]))
                 for e in PAIRS}
            scaled = {e: (mu[w[u0]] * A[e] if u0 in e else A[e]) for e in PAIRS}
            require(blank.haf(scaled) == mu[w[u0]] * blank.haf(A),
                    ("the diagonal site map is not multilinear", u0, w))


def _tensor(blocks):
    """H_6 of a six-site block array, as a dict word -> coefficient."""
    out = {}
    for w in WORDS:
        total = Q(0)
        for matching in M6:
            term = Q(1)
            for x, y in matching:
                a, b = (x, y) if x < y else (y, x)
                term *= blocks[(a, b)][w[a]][w[b]]
                if not term:
                    break
            total += term
        if total:
            out[w] = total
    return out


def audit_D_normalization_on_the_six_cycle():
    """The normalization step of block D, exercised on a real object: the
    alternating six-cycle has H_6 = X_0 + X_1, the SP-K6 near-miss at six
    vertices.  Rescaling one site's blocks by mu on its colour axis sends
    H_6 to sum_c mu_c t_c X_c, so mu_c = 1/t_c reaches Delta on the support.
    (No array with all three t_c nonzero exists -- that is SP-K6.)"""
    edge_colour = {(min(i, (i + 1) % 6), max(i, (i + 1) % 6)): i % 2
                   for i in SITES}
    blocks = {}
    for e in PAIRS:
        colour = edge_colour.get(e)
        blocks[e] = [[Q(1) if (colour is not None and a == b == colour)
                      else Q(0) for b in COLORS] for a in COLORS]
    base = _tensor(blocks)
    require(base == {(0,) * 6: Q(1), (1,) * 6: Q(1)},
            ("the alternating six-cycle tensor changed", base))
    for u0 in (0, 2, 5):
        for mu in ((Q(2), Q(-3), Q(7)), (Q(1, 5), Q(4), Q(-1))):
            moved = {e: [[(mu[a] if u0 == e[0] else
                           (mu[b] if u0 == e[1] else Q(1))) * blocks[e][a][b]
                          for b in COLORS] for a in COLORS] for e in PAIRS}
            require(_tensor(moved)
                    == {w: mu[w[u0]] * v for w, v in base.items()},
                    ("the diagonal site map did not scale H_6 coordinatewise",
                     u0, mu))
            inverse = tuple(1 / m for m in mu)
            back = {e: [[(inverse[a] if u0 == e[0] else
                          (inverse[b] if u0 == e[1] else Q(1)))
                         * moved[e][a][b] for b in COLORS] for a in COLORS]
                    for e in PAIRS}
            require(_tensor(back) == base,
                    ("the diagonal site map is not invertible", u0, mu))


# ==========================================================================
# 7.  block E/F/G: the named packets, the guards, the eight-cycle family
# ==========================================================================
def _q(entries):
    out = {}
    for x, y, cx, cy, value in entries:
        if x > y:
            x, y, cx, cy = y, x, cy, cx
        out[(x, y, cx, cy)] = Q(value)
    return out


GUARD = Packet(_q([(0, 1, 2, 2, 1), (4, 5, 2, 2, 1)]),
               {(0, 0, 2): Q(1), (0, 1, 2): Q(1), (1, 4, 2): Q(1),
                (2, 2, 2): Q(1), (2, 3, 2): Q(1)},
               {(0, 5, 2): Q(1), (1, 2, 2): Q(1), (1, 3, 2): Q(-1),
                (2, 2, 2): Q(1, 2), (2, 3, 2): Q(1, 2)},
               {(0, 1): Q(1)})
CYCLE = Packet(_q([(0, 1, 1, 1, 1), (1, 2, 0, 0, 1), (2, 3, 1, 1, 1),
                   (3, 4, 0, 0, 1), (4, 5, 1, 1, 1)]),
               {(0, 0, 0): Q(1)}, {(0, 5, 0): Q(1)}, {(1, 1): Q(1)})
WITNESS = Packet(_q([(0, 1, 2, 2, 1), (4, 5, 2, 2, 1), (1, 5, 0, 0, 1),
                     (2, 3, 0, 0, 1)]),
                 {(0, 0, 2): Q(1), (0, 1, 2): Q(1), (1, 4, 2): Q(1),
                  (2, 2, 2): Q(1), (2, 3, 2): Q(1), (0, 0, 0): Q(1)},
                 {(0, 5, 2): Q(1), (1, 2, 2): Q(1), (1, 3, 2): Q(-1),
                  (2, 2, 2): Q(1, 2), (2, 3, 2): Q(1, 2), (0, 4, 0): Q(1)},
                 {(1, 0): Q(-1)})


def _stars(pvec, svec):
    return ({(i, x, 2): Q(v) for i, vec in pvec.items()
             for x, v in enumerate(vec) if v},
            {(j, y, 2): Q(v) for j, vec in svec.items()
             for y, v in enumerate(vec) if v})


_BP, _BS = _stars(
    {0: (1, 0, 0, 0, 1, 0), 1: (0, 0, 1, 0, 0, 0), 2: (0, 1, 0, 0, 0, 1)},
    {0: (0, -1, 0, 0, 0, 1), 1: (-1, 0, 0, 0, -1, 0), 2: (0, 0, 0, 0, 1, 0)})
PACKET_B = Packet(_q([(0, 1, 2, 2, 1), (2, 3, 2, 2, 1), (4, 5, 2, 2, 1)]),
                  _BP, _BS, {(2, 1): Q(2)})
_CP, _CS = _stars(
    {0: (-1, 0, -1, -1, 0, -1), 1: (0, 0, 0, -1, 0, -1), 2: (0, 1, 0, 0, 0, 0)},
    {0: (-1, 0, 0, 0, 0, 0), 1: (0, -1, 0, 0, 1, 0), 2: (0, 0, 0, 0, 0, 1)})
PACKET_C = Packet(_q([(0, 1, 2, 2, 1), (2, 3, 2, 2, 1), (0, 4, 2, 2, 1),
                      (2, 5, 2, 2, 1)]), _CP, _CS, {(0, 1): Q(1)})
_U = (1, -1, 2, 0, 1, 1)
_V = (1, 2, -2, 1, -2, 1)
RANK_TWO = Packet(_q([(0, 1, 2, 2, 1), (2, 3, 2, 2, 1), (4, 5, 2, 2, 1)]),
                  {(0, x, 2): Q(v) for x, v in enumerate(_U) if v},
                  {(1, y, 2): Q(v) for y, v in enumerate(_V) if v},
                  {(0, 1): Q(-2)})

PUBLISHED = {
    "seven-row guard": [(0, 0, (0,) * 6, Q(-1)), (1, 1, (1,) * 6, Q(-1))],
    "alternating eight-cycle": [(2, 2, (2,) * 6, Q(-1))],
    "pure-word anchor witness": [(0, 0, (2, 0, 0, 0, 0, 0), Q(1)),
                                 (1, 1, (1,) * 6, Q(-1))],
    "packet B": [(0, 0, (0,) * 6, Q(-1)), (1, 1, (1,) * 6, Q(-1))],
    "packet C": [(0, 0, (0,) * 6, Q(-1)), (1, 1, (1,) * 6, Q(-1))],
}
NAMED = (("seven-row guard", GUARD), ("alternating eight-cycle", CYCLE),
         ("pure-word anchor witness", WITNESS), ("packet B", PACKET_B),
         ("packet C", PACKET_C), ("rank-two clean packet", RANK_TWO))

# (tau, {word: E(I)}, max live trace-response edges, #words with haf_w(q) != 0)
PACKET_TABLE = {
    "seven-row guard": (Q(0), {}, 5, 0),
    "alternating eight-cycle": (Q(1), {}, 1, 1),
    "pure-word anchor witness": (Q(0), {(0, 2, 2, 2, 0, 2): Q(2),
                                        (2, 2, 2, 2, 0, 2): Q(2)}, 5, 1),
    "packet B": (Q(0), {}, 5, 1),
    "packet C": (Q(0), {(2,) * 6: Q(-3)}, 7, 0),
    "rank-two clean packet": (Q(0), {}, 0, 1),
}


def audit_standard_probes():
    K01 = [[Q(1) if (l, m) == (0, 1) else Q(0) for m in COLORS]
           for l in COLORS]
    layers = RANK_TWO.layers(RANK_TWO.cap_R(K01, PURE2), PURE2)
    require(layers == [Q(1), Q(2), Q(6), Q(12)],
            "rank-two clean packet layers changed")
    require(RANK_TWO.E(K01, PURE2) == 0,
            "the rank-two clean packet is no longer clean")
    require(GUARD.E(K01, PURE2) == -2,
            "the seven-row guard terminal class is no longer -2")
    require(PACKET_C.E(K01, PURE2) == -4, "packet C terminal class changed")
    require(PACKET_B.E([[Q(1) if (l, m) == (2, 1) else Q(0) for m in COLORS]
                        for l in COLORS], PURE2) == 4,
            "packet B terminal class changed")


def audit_packet_table():
    for name, pk in NAMED:
        lg = ledger(pk)
        if name in PUBLISHED:
            require(lg == sorted(PUBLISHED[name]),
                    ("published GHZ ledger not reproduced", name, lg))
        tau, support, live, hafcount = PACKET_TABLE[name]
        require(pk.tau() == tau, ("tau changed", name, pk.tau()))
        require(identity_cap_support(pk) == support,
                ("E(I) support changed", name, identity_cap_support(pk)))
        measured = live_trace_edges(pk)
        require(measured == live, ("live trace-response edges", name, measured))
        measured_haf = sum(1 for w in WORDS if pk.haf(pk.qword(w)))
        require(measured_haf == hafcount,
                ("words with haf_w(q) != 0", name, measured_haf))


def audit_free_direct_block_and_guards():
    """Packet C and the seven-row guard have haf_w(q) = 0 at every word, so
    their entire direct block is free; both 6559-row verdicts are reachable."""
    for name, base in (("packet C", PACKET_C), ("seven-row guard", GUARD)):
        require(all(not base.haf(base.qword(w)) for w in WORDS),
                ("haf_w(q) does not vanish at every word", name))
        reference = ledger(base)
        for direct in ({(l, m): Q(1) if l == m else Q(0)
                        for l in COLORS for m in COLORS},
                       {(0, 0): Q(5), (1, 2): Q(-7)},
                       {(2, 2): Q(-1)}):
            moved = Packet(base.q, base.p, base.s, direct)
            require(ledger(moved) == reference,
                    ("changing the direct block changed the ledger", name))
    unit = {(l, m): Q(1) if l == m else Q(0) for l in COLORS for m in COLORS}
    # F1: an ACTIVE UNCLEAN identity cap at 6559 rows
    unclean = Packet(PACKET_C.q, PACKET_C.p, PACKET_C.s, unit)
    lg = ledger(unclean)
    require(len(lg) == 2, ("the guard is not at 6559 rows", len(lg)))
    require([(l, m, w) for l, m, w, _v in lg]
            == [(0, 0, (0,) * 6), (1, 1, (1,) * 6)],
            ("the guard's missing rows are not the two pure anchors", lg))
    require(unclean.tau() == 3, "the guard's identity cap is inactive")
    require(identity_cap_support(unclean) == {(2,) * 6: Q(-3)},
            "the guard's identity cap became clean")
    # and it is unclean for EVERY direct block, since its B^[2]q vanishes
    for w in WORDS:
        layers = PACKET_C.layers(PACKET_C.trace_response(w), w)
        require(not layers[2], ("packet C has a live B^[2]q", w))
    # F2: an ACTIVE CLEAN identity cap at 6559 rows
    clean = Packet(GUARD.q, GUARD.p, GUARD.s, unit)
    require(len(ledger(clean)) == 2, "the calibration packet moved off 6559")
    require(clean.tau() == 3 and not identity_cap_support(clean),
            "the calibration packet is no longer active and clean")


# ---- the 56 endpoint charts of the alternating eight-cycle ----------------
V8 = tuple(range(8))
CYCLE_EDGES = {(min(i, (i + 1) % 8), max(i, (i + 1) % 8)): i % 2 for i in V8}


def _cycle_block(u, v, cu, cv):
    colour = CYCLE_EDGES.get((min(u, v), max(u, v)))
    if colour is None:
        return Q(0)
    return Q(1) if (cu == colour and cv == colour) else Q(0)


def _chart(pend, qend):
    sites = tuple(v for v in V8 if v not in (pend, qend))
    qq, pp, ss, dd = {}, {}, {}, {}
    for xi, yi in PAIRS:
        for a, b in product(COLORS, repeat=2):
            value = _cycle_block(sites[xi], sites[yi], a, b)
            if value:
                qq[(xi, yi, a, b)] = value
    for l in COLORS:
        for xi in SITES:
            for c in COLORS:
                value = _cycle_block(pend, sites[xi], l, c)
                if value:
                    pp[(l, xi, c)] = value
                value = _cycle_block(qend, sites[xi], l, c)
                if value:
                    ss[(l, xi, c)] = value
    for l, m in product(COLORS, repeat=2):
        value = _cycle_block(pend, qend, l, m)
        if value:
            dd[(l, m)] = value
    return Packet(qq, pp, ss, dd)


def audit_eight_cycle_family():
    census = {}
    for pend, qend in product(V8, repeat=2):
        if pend == qend:
            continue
        pk = _chart(pend, qend)
        lg = ledger(pk)
        require(len(lg) == 1 and lg[0][:3] == (2, 2, (2,) * 6),
                ("a chart does not fail exactly the colour-2 anchor",
                 pend, qend))
        active = pk.tau() != 0
        live = live_trace_edges(pk)
        distance = min((qend - pend) % 8, (pend - qend) % 8)
        require(not (active and live >= 2),
                ("an active chart has two live response edges", pend, qend))
        require(active == (distance == 1),
                ("activity is not exactly the distance-one charts",
                 pend, qend))
        require(not identity_cap_support(pk),
                ("a chart has a nonzero E(I)", pend, qend))
        census[(distance, active, live)] = census.get(
            (distance, active, live), 0) + 1
    require(census == {(1, True, 1): 16, (2, False, 1): 16,
                       (3, False, 2): 16, (4, False, 2): 8},
            ("the eight-cycle chart census changed", census))
    # Star-rank one is the reason for only 32 of the 56.  On the other 24 the
    # reason is tau = 0 plus "two edges cannot fill a three-edge matching";
    # asserting star-rank one for all 56 would be false.
    star_rank_one = sum(n for (_, _, live), n in census.items() if live <= 1)
    two_edge = sum(n for (_, _, live), n in census.items() if live >= 2)
    require(star_rank_one == 32 and two_edge == 24,
            ("the star-rank split is not 32/24", star_rank_one, two_edge))
    require(all(not active for (_, active, live) in census if live >= 2),
            "a chart with two live edges is active, so tau does not kill Q_2")


# ==========================================================================
def main():
    audit_normalization()
    audit_A1_descent_note_formula()
    audit_A2_cap_line_cubic()
    audit_A3_identity_cap_layers()
    audit_A4_trace_row()
    audit_A5_generic_cap_reformulation()
    audit_A6_tau_weight()
    audit_B_permanent_formula()
    audit_B_rows_are_linear_in_N()
    audit_C1_rows_multihomogeneous()
    audit_C2_identity_error_balanced()
    audit_C3_site_colour_order()
    audit_C4_row_sector_inert()
    audit_D1_diagonal_site_map()
    audit_D_normalization_on_the_six_cycle()
    audit_standard_probes()
    audit_packet_table()
    audit_free_direct_block_and_guards()
    audit_eight_cycle_family()
    print(
        "PASS: E(I) = tau B^[2]q + B^[3] = [z^3] of every cap line, "
        "(a,b)-independent; sum_l Row(l,l,w) = tau G_0 + G_1 so "
        "E(I) = haf(tau q + B) - tau^2 (trace row); rows are tau-weight 0 and "
        "E(I) is tau-weight 6; E(I) is a permanent form in N = P^T S while "
        "every row is linear in N; at E(I)'s multidegree the row sector is "
        "inert (forced degree-two d-multipliers, d-degree {2,3} against "
        "E(I)'s {0,1}); the diagonal site map is multilinear, so by SP-K6 no "
        "nine-row solution has an active clean cap; packet C with d = I gives "
        "an ACTIVE UNCLEAN identity cap at 6559 rows and the seven-row guard "
        "with d = I an ACTIVE CLEAN one, so these 6559 rows decide neither "
        "verdict; all 56 eight-cycle charts sit at 6560 with E(I) = 0, by "
        "star-rank one on 32 of them and by tau = 0 with only two live edges "
        "on the other 24"
    )


if __name__ == "__main__":
    main()
