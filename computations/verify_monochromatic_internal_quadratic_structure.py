#!/usr/bin/env python3
"""Structure theorems for a monochromatic internal quadratic on a residual chart.

Model (identical to the one audited in
``verify_h3_diagonal_segre_second_transgression_seven_row_guard.py`` and
``verify_h3_star_sector_anchor_terminal_trade.py``, but with *every* entry free):
six residual sites ``W = {0..5}`` and two endpoints; a packet carries an internal
quadratic ``q``, endpoint stars ``p_i(x,c)``, ``s_j(y,c)`` and a direct block
``d_ij``, and

    Row(i,j,w) = d_ij haf_w(q)
               + sum_{x<y} [p_i(x,w_x) s_j(y,w_y) + p_i(y,w_y) s_j(x,w_x)]
                 haf_w(q restricted to W\\{x,y}).

A *GHZ realization* is a packet with ``Row(i,j,w) = 1`` when ``i = j`` and
``w = i^6`` and ``0`` otherwise, on all 729 words and all 9 label pairs; it is an
eight-vertex three-colour realization of the GHZ state.  Whether one exists is
open (this is Krenn's conjecture at n = 8), and nothing here decides it.

This checker studies the *monochromatic* chart ``q(x,y,cx,cy) = 0`` for
``cx != cy``, i.e. ``q`` is three colour-indexed symmetric arrays ``q_c`` on
``K_6``, with the stars, the direct block and the monochromatic weights free over
an arbitrary field.  It proves, as formal polynomial identities in all 162
unknowns (no sampling), the facts that the accompanying report turns into the
structure theorems T1-T5, and it pins the residual support family that the
argument does not close.

Contents, in the order they run:

  1  all-ones hafnian normalization (15 on six sites, 3 on four, 1 on two);
  2  the symbolic system evaluated at the audited seven-row guard packet (which
     *is* monochromatic-internal) reproduces its committed two-entry ledger;
  3  T1, the class factorization: every one of the 9*729 rows equals its
     even/two-odd reduced form -- an identity over all monomials;
  4  the two-odd rows contain no direct-block monomial (the B-family is
     star-only, d-free);
  5  T2, the anchor cofactor lemma: Row(c,c,c^6) = d_cc h_c(W) + <R_c, H_c> and
     h_c(W) = sum_y q_c(x,y) H_c(x,y) for each site x, so all H_c(x,y) = 0
     forces Row(c,c,c^6) = 0 and the anchor dies -- star-independently;
  6  T3, the label-kernel identity: for a formal label covector a,
     sum_i a_i Row(i,j,w) has the direct term and the star term separated, the
     star term carrying only the contractions sum_i a_i p_i(x,c);
  7  T4, the handle family: for every site x, colour a, odd T subset W\\{x} and
     ordering (b,e) of the other two colours, the row at the word (a on x, b on
     T, e elsewhere) is the rank-two form h_e(R)*[p_i(x,a) s^b_j(T)
     + p^b_i(T) s_j(x,a)]; the named instances (distance one, distance two,
     three-three) are checked as literal specializations;
  8  the rank-one alternative behind T4, exhaustively over F_2 and F_3;
  9  the residual: the support conditions forced in the rank-two branch of T3
     are *satisfiable*, with an explicit surviving configuration -- so that
     branch is not closed here.

Research evidence only.  Krenn's conjecture remains open, no certified
dependency changes, and `SP-CLEAN-BRIDGE` is untouched.  Standard library only,
exact ``Fraction`` arithmetic, deterministic, live under ``python -O``.
"""

from fractions import Fraction as Q
from itertools import combinations, product

COLORS = (0, 1, 2)
SITES = tuple(range(6))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


# --------------------------------------------------------------------------
# matchings and a minimal exact sparse polynomial ring
# --------------------------------------------------------------------------
_MATCH = {}


def matchings(vertices):
    vertices = tuple(vertices)
    if vertices in _MATCH:
        return _MATCH[vertices]
    if not vertices:
        answer = ((),)
    elif len(vertices) % 2:
        answer = ()
    else:
        first = vertices[0]
        acc = []
        for position, partner in enumerate(vertices[1:], start=1):
            remainder = vertices[1:position] + vertices[position + 1:]
            for tail in matchings(remainder):
                acc.append(((first, partner),) + tail)
        answer = tuple(acc)
    _MATCH[vertices] = answer
    return answer


class Poly:
    __slots__ = ("terms",)

    def __init__(self, terms=None):
        self.terms = {m: c for m, c in (terms or {}).items() if c}

    @staticmethod
    def const(value):
        value = Q(value)
        return Poly({(): value} if value else {})

    @staticmethod
    def var(nm):
        return Poly({(nm,): Q(1)})

    def __bool__(self):
        return bool(self.terms)

    def __add__(self, other):
        out = dict(self.terms)
        for m, c in other.terms.items():
            total = out.get(m, Q(0)) + c
            if total:
                out[m] = total
            else:
                out.pop(m, None)
        return Poly(out)

    def __sub__(self, other):
        return self + Poly({m: -c for m, c in other.terms.items()})

    def __mul__(self, other):
        out = {}
        for m1, c1 in self.terms.items():
            for m2, c2 in other.terms.items():
                m = tuple(sorted(m1 + m2))
                total = out.get(m, Q(0)) + c1 * c2
                if total:
                    out[m] = total
                else:
                    out.pop(m, None)
        return Poly(out)

    def evaluate(self, assignment):
        total = Q(0)
        for m, c in self.terms.items():
            term = c
            for v in m:
                term *= assignment.get(v, Q(0))
                if not term:
                    break
            total += term
        return total

    def __eq__(self, other):
        return self.terms == other.terms

    def __hash__(self):
        return hash(frozenset(self.terms.items()))


ZERO = Poly.const(0)
ONE = Poly.const(1)


def qvar(c, x, y):
    if x > y:
        x, y = y, x
    return Poly.var(("q", c, x, y))


def pvar(i, x, c):
    return Poly.var(("p", i, x, c))


def svar(j, y, c):
    return Poly.var(("s", j, y, c))


def dvar(i, j):
    return Poly.var(("d", i, j))


def avar(i):
    return Poly.var(("a", i))


# --------------------------------------------------------------------------
# the physical row, straight from the definition
# --------------------------------------------------------------------------
def q_entry(x, y, cx, cy):
    """Monochromatic internal quadratic: cross-colour entries are zero."""
    return ZERO if cx != cy else qvar(cx, x, y)


def haf_word(sites, word):
    total = ZERO
    for matching in matchings(tuple(sites)):
        term = ONE
        for x, y in matching:
            term = term * q_entry(x, y, word[x], word[y])
            if not term:
                break
        total = total + term
    return total


def row(i, j, word, sites=SITES):
    sites = tuple(sites)
    total = dvar(i, j) * haf_word(sites, word)
    for x, y in combinations(sites, 2):
        response = (pvar(i, x, word[x]) * svar(j, y, word[y])
                    + pvar(i, y, word[y]) * svar(j, x, word[x]))
        rest = tuple(v for v in sites if v not in (x, y))
        piece = haf_word(rest, word)
        if piece:
            total = total + response * piece
    return total


def ghz_target(i, j, word):
    return Q(i == j and all(c == i for c in word))


# --------------------------------------------------------------------------
# colour-separated ingredients used by the reduced form
# --------------------------------------------------------------------------
_HC = {}


def hc(c, T):
    """haf(q_c restricted to T); 1 on the empty set, 0 on odd sets."""
    T = tuple(sorted(T))
    key = (c, T)
    if key in _HC:
        return _HC[key]
    total = ZERO
    for matching in matchings(T):
        term = ONE
        for x, y in matching:
            term = term * qvar(c, x, y)
        total = total + term
    _HC[key] = total
    return total


def resp_layer(i, j, c, S):
    """[t^1] haf((q_c + t R^{ij}_c) restricted to S)."""
    total = ZERO
    S = tuple(sorted(S))
    for x, y in combinations(S, 2):
        response = pvar(i, x, c) * svar(j, y, c) + pvar(i, y, c) * svar(j, x, c)
        total = total + response * hc(c, tuple(v for v in S if v not in (x, y)))
    return total


def p_cof(i, c, S):
    """sum_{x in S} p_i(x,c) haf(q_c restricted to S\\{x})."""
    total = ZERO
    for x in S:
        total = total + pvar(i, x, c) * hc(c, tuple(v for v in S if v != x))
    return total


def s_cof(j, c, S):
    total = ZERO
    for y in S:
        total = total + svar(j, y, c) * hc(c, tuple(v for v in S if v != y))
    return total


def colour_classes(word):
    return tuple(tuple(x for x in SITES if word[x] == c) for c in COLORS)


def reduced_row(i, j, word):
    """The claimed closed form (T1)."""
    S = colour_classes(word)
    odd = [c for c in COLORS if len(S[c]) % 2]
    if not odd:
        total = dvar(i, j) * (hc(0, S[0]) * hc(1, S[1]) * hc(2, S[2]))
        for a in COLORS:
            piece = resp_layer(i, j, a, S[a])
            if not piece:
                continue
            for b in COLORS:
                if b != a:
                    piece = piece * hc(b, S[b])
            total = total + piece
        return total
    a, b = odd
    e = [c for c in COLORS if c not in odd][0]
    return hc(e, S[e]) * (p_cof(i, a, S[a]) * s_cof(j, b, S[b])
                          + p_cof(i, b, S[b]) * s_cof(j, a, S[a]))


# --------------------------------------------------------------------------
# 1.  normalization
# --------------------------------------------------------------------------
def audit_normalization():
    def plain(sites):
        total = Q(0)
        for matching in matchings(tuple(sites)):
            total += Q(1)
        return total

    require(plain(SITES) == 15, "all-ones six-site hafnian is not 15")
    require(plain((0, 1, 2, 3)) == 3, "all-ones four-site hafnian is not 3")
    require(plain((0, 1)) == 1, "all-ones two-site hafnian is not 1")
    require(plain(()) == 1, "the empty hafnian is not 1")
    require(len(matchings((0, 1, 2, 3, 4))) == 0,
            "an odd vertex set has a matching")


# --------------------------------------------------------------------------
# 2.  agreement with the audited seven-row guard
# --------------------------------------------------------------------------
GUARD_Q2 = {(0, 1): Q(1), (4, 5): Q(1)}
GUARD_P2 = {0: (1, 1, 0, 0, 0, 0), 1: (0, 0, 0, 0, 1, 0), 2: (0, 0, 1, 1, 0, 0)}
GUARD_S2 = {0: (0, 0, 0, 0, 0, 1), 1: (0, 0, 1, -1, 0, 0),
            2: (0, 0, Q(1, 2), Q(1, 2), 0, 0)}


def guard_point():
    point = {}
    for (x, y), value in GUARD_Q2.items():
        point[("q", 2, x, y)] = Q(value)
    for i in COLORS:
        for x in SITES:
            if GUARD_P2[i][x]:
                point[("p", i, x, 2)] = Q(GUARD_P2[i][x])
            if GUARD_S2[i][x]:
                point[("s", i, x, 2)] = Q(GUARD_S2[i][x])
    point[("d", 0, 1)] = Q(1)
    return point


def audit_guard_ledger(system):
    """The guard packet is monochromatic-internal, so it lives in this chart."""
    point = guard_point()
    ledger = sorted((i, j, word, value)
                    for (i, j, word), poly in system.items()
                    for value in (poly.evaluate(point),)
                    if value)
    require(ledger == [(0, 0, (0,) * 6, Q(-1)), (1, 1, (1,) * 6, Q(-1))],
            ("the symbolic system does not reproduce the committed guard "
             "ledger", ledger))


# --------------------------------------------------------------------------
# 3-4.  T1, the class factorization, and the d-freeness of the two-odd rows
# --------------------------------------------------------------------------
def build_system():
    out = {}
    for word in product(COLORS, repeat=6):
        for i, j in product(COLORS, repeat=2):
            out[(i, j, word)] = row(i, j, word) - Poly.const(ghz_target(i, j, word))
    return out


def audit_class_factorization(system):
    even_words = 0
    odd_words = 0
    for word in product(COLORS, repeat=6):
        sizes = tuple(len(S) for S in colour_classes(word))
        parity = sum(1 for n in sizes if n % 2)
        require(parity in (0, 2),
                ("a word has an impossible odd-class count", word, parity))
        if parity:
            odd_words += 1
        else:
            even_words += 1
        for i, j in product(COLORS, repeat=2):
            literal = system[(i, j, word)] + Poly.const(ghz_target(i, j, word))
            require(literal == reduced_row(i, j, word),
                    ("the class factorization failed", i, j, word))
    require((even_words, odd_words) == (183, 546),
            ("word census changed", even_words, odd_words))
    # 183 = 3 pure + 180 non-pure all-even words, matching the leak note.
    require(even_words - 3 == 180, "non-pure all-even word count is not 180")


def audit_two_odd_rows_are_direct_free(system):
    seen = 0
    for word in product(COLORS, repeat=6):
        sizes = [len(S) for S in colour_classes(word)]
        if sum(1 for n in sizes if n % 2) != 2:
            continue
        seen += 1
        for i, j in product(COLORS, repeat=2):
            poly = system[(i, j, word)]
            require(all(v[0] != "d" for m in poly.terms for v in m),
                    ("a two-odd row carries a direct-block monomial",
                     i, j, word))
    require(seen == 546, ("two-odd word count changed", seen))


# --------------------------------------------------------------------------
# 5.  T2, the anchor cofactor lemma (star-independent)
# --------------------------------------------------------------------------
def four_hole(c, x, y):
    return hc(c, tuple(v for v in SITES if v not in (x, y)))


def audit_anchor_cofactor_lemma():
    for c in COLORS:
        pure = (c,) * 6
        # (a) the anchor row is spanned by h_c(W) and the four-hole cofactors
        expected = dvar(c, c) * hc(c, SITES)
        for x, y in combinations(SITES, 2):
            response = (pvar(c, x, c) * svar(c, y, c)
                        + pvar(c, y, c) * svar(c, x, c))
            expected = expected + response * four_hole(c, x, y)
        require(row(c, c, pure) == expected,
                ("the anchor row is not the cofactor form", c))
        # (b) Laplace expansion at every site: h_c(W) is a combination of them
        for x in SITES:
            total = ZERO
            for y in SITES:
                if y != x:
                    total = total + qvar(c, x, y) * four_hole(c, x, y)
            require(hc(c, SITES) == total,
                    ("the six-site Laplace expansion failed", c, x))
        # (c) so (a) and (b) together say: if every four-hole cofactor of q_c
        # vanishes, both h_c(W) and the whole anchor row vanish.  Each cofactor
        # is a nonzero polynomial, so this is a real condition on q_c and not a
        # bookkeeping artefact.
        cofactors = [four_hole(c, x, y) for x, y in combinations(SITES, 2)]
        require(len(cofactors) == 15, "there are not fifteen four-hole cofactors")
        require(all(cof for cof in cofactors),
                ("a four-hole cofactor is identically zero", c))


def audit_anchor_dies_without_cofactors():
    """Concrete form of T2: on any packet whose colour-c four-hole cofactors all
    vanish, the colour-c anchor row evaluates to 0, never to 1."""
    # Sample: every q_c support without two disjoint edges (a star or a
    # triangle) makes all four-hole cofactors vanish identically; check the
    # whole family of supports with no two disjoint edges.
    for support in _supports_without_two_disjoint_edges():
        point = {}
        for k, (x, y) in enumerate(sorted(support)):
            point[("q", 0, x, y)] = Q(k + 1)
        for i in COLORS:
            for x in SITES:
                point[("p", i, x, 0)] = Q(x + 2 * i + 1)
                point[("s", i, x, 0)] = Q(3 * x - i - 1)
        point[("d", 0, 0)] = Q(7)
        require(row(0, 0, (0,) * 6).evaluate(point) == 0,
                ("an anchor survived with no two disjoint edges", support))


def _supports_without_two_disjoint_edges():
    edges = list(combinations(SITES, 2))
    out = []
    for mask in range(1 << len(edges)):
        chosen = [edges[k] for k in range(len(edges)) if mask >> k & 1]
        ok = True
        for a in range(len(chosen)):
            for b in range(a + 1, len(chosen)):
                if not set(chosen[a]) & set(chosen[b]):
                    ok = False
                    break
            if not ok:
                break
        if ok:
            out.append(tuple(chosen))
    return out


# --------------------------------------------------------------------------
# 6.  T3, the label-kernel identity
# --------------------------------------------------------------------------
def audit_label_kernel_identity(system):
    """sum_i a_i Row(i,j,w) separates into a direct part and a star part whose
    only star dependence is through the contractions sum_i a_i p_i(x,c)."""
    for word in product(COLORS, repeat=6):
        for j in COLORS:
            left = ZERO
            for i in COLORS:
                literal = (system[(i, j, word)]
                           + Poly.const(ghz_target(i, j, word)))
                left = left + avar(i) * literal
            direct = ZERO
            for i in COLORS:
                direct = direct + avar(i) * dvar(i, j)
            right = direct * haf_word(SITES, word)
            for x, y in combinations(SITES, 2):
                cx = ZERO
                cy = ZERO
                for i in COLORS:
                    cx = cx + avar(i) * pvar(i, x, word[x])
                    cy = cy + avar(i) * pvar(i, y, word[y])
                block = cx * svar(j, y, word[y]) + cy * svar(j, x, word[x])
                rest = tuple(v for v in SITES if v not in (x, y))
                piece = haf_word(rest, word)
                if piece:
                    right = right + block * piece
            require(left == right,
                    ("the label-kernel separation failed", j, word))


def _kill(poly, dead):
    return Poly({m: c for m, c in poly.terms.items()
                 if not any(v in dead for v in m)})


def audit_blind_label_and_blind_colour():
    """The two specializations the report uses.

    (a) if the u-star is blind to a label j0 then every row (j0, j) is carried
        by the direct block alone: Row(j0,j,w) = d_{j0 j} haf_w(q);
    (b) if the u-star is blind to a colour a then the pure-word-a rows are
        carried by the direct block alone: Row(i,j,a^6) = d_ij h_a(W)."""
    for j0 in COLORS:
        dead = {("p", j0, x, c) for x in SITES for c in COLORS}
        for word in product(COLORS, repeat=6):
            for j in COLORS:
                require(_kill(row(j0, j, word), dead)
                        == dvar(j0, j) * haf_word(SITES, word),
                        ("a label-blind row is not purely direct", j0, j, word))
    for a in COLORS:
        dead = {("p", i, x, a) for x in SITES for i in COLORS}
        pure = (a,) * 6
        for i, j in product(COLORS, repeat=2):
            require(_kill(row(i, j, pure), dead) == dvar(i, j) * hc(a, SITES),
                    ("a colour-blind pure row is not purely direct", a, i, j))


# --------------------------------------------------------------------------
# 7.  T4, the handle family and its named instances
# --------------------------------------------------------------------------
def audit_handle_family():
    checked = 0
    for x in SITES:
        others = tuple(v for v in SITES if v != x)
        for a in COLORS:
            rest_colours = [c for c in COLORS if c != a]
            for b, e in ((rest_colours[0], rest_colours[1]),
                         (rest_colours[1], rest_colours[0])):
                for size in (1, 3, 5):
                    for T in combinations(others, size):
                        R = tuple(v for v in others if v not in T)
                        word = tuple(a if v == x else (b if v in T else e)
                                     for v in SITES)
                        for i, j in product(COLORS, repeat=2):
                            claim = hc(e, R) * (
                                pvar(i, x, a) * s_cof(j, b, T)
                                + p_cof(i, b, T) * svar(j, x, a))
                            require(row(i, j, word) == claim,
                                    ("the handle identity failed",
                                     x, a, b, e, T, i, j))
                        checked += 1
    require(checked == 6 * 3 * 2 * (5 + 10 + 1),
            ("handle census changed", checked))


def audit_named_instances():
    # distance one from a pure word: T = W\{x}, empty third class
    for x in SITES:
        for a in COLORS:
            for c in COLORS:
                if c == a:
                    continue
                word = tuple(a if v == x else c for v in SITES)
                T = tuple(v for v in SITES if v != x)
                for i, j in product(COLORS, repeat=2):
                    claim = (pvar(i, x, a) * s_cof(j, c, T)
                             + p_cof(i, c, T) * svar(j, x, a))
                    require(row(i, j, word) == claim,
                            ("the distance-one instance failed", x, a, c, i, j))
    # distance two, two distinct new colours: the (1,1,4) rank-two condition
    for x, y in combinations(SITES, 2):
        for c in COLORS:
            a, b = [t for t in COLORS if t != c]
            for (ca, cb) in ((a, b), (b, a)):
                word = tuple(ca if v == x else (cb if v == y else c)
                             for v in SITES)
                for i, j in product(COLORS, repeat=2):
                    claim = four_hole(c, x, y) * (
                        pvar(i, x, ca) * svar(j, y, cb)
                        + pvar(i, y, cb) * svar(j, x, ca))
                    require(row(i, j, word) == claim,
                            ("the (1,1,4) instance failed", x, y, c, ca, i, j))
    # three-three splits: the unconditional handles
    for A in combinations(SITES, 3):
        if 0 not in A:
            continue
        B = tuple(v for v in SITES if v not in A)
        for a in COLORS:
            for b in COLORS:
                if b == a:
                    continue
                word = tuple(a if v in A else b for v in SITES)
                for i, j in product(COLORS, repeat=2):
                    claim = (p_cof(i, a, A) * s_cof(j, b, B)
                             + p_cof(i, b, B) * s_cof(j, a, A))
                    require(row(i, j, word) == claim,
                            ("the three-three instance failed", A, a, b, i, j))


# --------------------------------------------------------------------------
# 8.  the rank-one alternative behind T4
# --------------------------------------------------------------------------
def audit_rank_one_alternative():
    """The two conditional forms actually used by T4, for u_k, v_k in F^3 with
    u1 v1^T + u2 v2^T = 0.  This is NOT a trichotomy -- u1 = v2 = 0 with
    u2 = v1 nonzero satisfies the hypothesis and none of the three clauses one
    might expect.  What is asserted, and verified exhaustively over F_2 and
    F_3, is: if u1 and v1 are both nonzero then either u2 = v2 = 0 or
    (u2, v2) is proportional to (u1, -v1); and in particular 'u1 and v1 both
    nonzero while exactly one of u2, v2 vanishes' is impossible."""
    for modulus in (2, 3):
        vectors = [tuple(v) for v in product(range(modulus), repeat=3)]
        for u1 in vectors:
            for v1 in vectors:
                base = [[u1[r] * v1[c] % modulus for c in range(3)]
                        for r in range(3)]
                for u2 in vectors:
                    for v2 in vectors:
                        ok = True
                        for r in range(3):
                            for c in range(3):
                                if (base[r][c] + u2[r] * v2[c]) % modulus:
                                    ok = False
                                    break
                            if not ok:
                                break
                        if not ok:
                            continue
                        zero = (0, 0, 0)
                        half = ((u2 == zero) != (v2 == zero))
                        require(not (u1 != zero and v1 != zero and half),
                                ("a forbidden half-degenerate solution exists",
                                 modulus, u1, v1, u2, v2))
                        if u1 != zero and v1 != zero:
                            # u2 = t u1 and v1 = -t v2 for a common t
                            witnesses = [t for t in range(modulus)
                                         if all((u2[r] - t * u1[r]) % modulus == 0
                                                for r in range(3))
                                         and all((v1[c] + t * v2[c]) % modulus == 0
                                                 for c in range(3))]
                            require(witnesses,
                                    ("no common scalar", modulus, u1, v1, u2, v2))


# --------------------------------------------------------------------------
# 9.  the residual support family of the rank-two branch
# --------------------------------------------------------------------------
EDGES = tuple(frozenset(e) for e in combinations(SITES, 2))


def _pairings(vertices):
    return [tuple(frozenset(e) for e in M) for M in matchings(tuple(sorted(vertices)))]


PM6 = _pairings(SITES)


def minimal_edge_covers():
    out = set()
    n = len(EDGES)
    for mask in range(1 << n):
        chosen = [EDGES[k] for k in range(n) if mask >> k & 1]
        covered = set()
        for e in chosen:
            covered |= e
        if len(covered) != 6:
            continue
        minimal = True
        for drop in range(len(chosen)):
            sub = set()
            for k, e in enumerate(chosen):
                if k != drop:
                    sub |= e
            if len(sub) == 6:
                minimal = False
                break
        if minimal:
            out.add(frozenset(chosen))
    return out


def audit_residual_support_family():
    require(len(minimal_edge_covers()) == 171,
            "the minimal edge cover count of K_6 is not 171")
    # The explicit surviving configuration.
    P0 = {frozenset((0, 1)), frozenset((2, 3)), frozenset((4, 5))}
    P1 = {frozenset((1, 4)), frozenset((3, 5))}
    P2 = set(P1)
    supports = {0: P0, 1: P1, 2: P2}

    def four_set_matched(support, hole):
        T = [v for v in SITES if v not in hole]
        for M in _pairings(T):
            if all(e in support for e in M):
                return True
        return False

    dhat = {c: {e for e in EDGES if four_set_matched(supports[c], e)}
            for c in COLORS}
    require(dhat[0] == P0, ("D-hat of colour 0 changed", dhat[0]))
    require(dhat[1] == {frozenset((0, 2))}, ("D-hat of colour 1 changed", dhat[1]))
    require(dhat[2] == {frozenset((0, 2))}, ("D-hat of colour 2 changed", dhat[2]))
    for a in COLORS:
        require(dhat[a], ("colour %d has no live four-hole" % a))
        for b in COLORS:
            if b != a:
                require(not (dhat[a] & supports[b]),
                        ("the cross-exclusion D_a cap P_b failed", a, b))
    covered = set()
    for e in dhat[0] & P0:
        covered |= e
    require(covered == set(SITES),
            "the distinguished colour's live support is not an edge cover")
    rainbow = False
    for M in PM6:
        for perm in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)):
            if all(M[k] in supports[perm[k]] for k in range(3)):
                rainbow = True
    require(not rainbow, "the surviving configuration has a rainbow matching")
    # and it really is a monochromatic support triple with three live anchors
    require(len(P0) == 3 and len(P1) == 2 and len(P2) == 2,
            "the surviving configuration changed shape")


# --------------------------------------------------------------------------
# 10.  the two-colour scope guard, and the impossibility of completing it
# --------------------------------------------------------------------------
# The eight-cycle u-0-1-2-3-4-5-v-u with alternating monochromatic colours 0,1
# is the classical two-colour GHZ realization.  It lives in the monochromatic
# chart, so it bounds the target from below.
CYCLE = {("p", 0, 0, 0): Q(1), ("q", 1, 0, 1): Q(1), ("q", 0, 1, 2): Q(1),
         ("q", 1, 2, 3): Q(1), ("q", 0, 3, 4): Q(1), ("q", 1, 4, 5): Q(1),
         ("s", 0, 5, 0): Q(1), ("d", 1, 1): Q(1)}


def audit_two_colour_scope_guard(system):
    ledger = sorted((i, j, word, value)
                    for (i, j, word), poly in system.items()
                    for value in (poly.evaluate(CYCLE),)
                    if value)
    require(ledger == [(2, 2, (2,) * 6, Q(-1))],
            ("the eight-cycle packet does not fail exactly the colour-2 anchor",
             ledger))


FROZEN_Q = {(0, (1, 2)): Q(1), (0, (3, 4)): Q(1),
            (1, (0, 1)): Q(1), (1, (2, 3)): Q(1), (1, (4, 5)): Q(1)}
FROZEN_P = {(0, 0, 0): Q(1)}
FROZEN_S = {(0, 5, 0): Q(1)}


def frozen_q_entry(x, y, cx, cy):
    if x > y:
        x, y = y, x
        cx, cy = cy, cx
    if cx != cy:
        return ZERO
    if cx == 2:
        return qvar(2, x, y)
    return Poly.const(FROZEN_Q.get((cx, (x, y)), 0))


def frozen_haf(sites, word):
    total = ZERO
    for matching in matchings(tuple(sites)):
        term = ONE
        for x, y in matching:
            term = term * frozen_q_entry(x, y, word[x], word[y])
            if not term:
                break
        total = total + term
    return total


def frozen_row(i, j, word):
    total = dvar(i, j) * frozen_haf(SITES, word)
    for x, y in combinations(SITES, 2):
        pe_x = (pvar(i, x, word[x]) if word[x] == 2
                else Poly.const(FROZEN_P.get((i, x, word[x]), 0)))
        pe_y = (pvar(i, y, word[y]) if word[y] == 2
                else Poly.const(FROZEN_P.get((i, y, word[y]), 0)))
        se_x = (svar(j, x, word[x]) if word[x] == 2
                else Poly.const(FROZEN_S.get((j, x, word[x]), 0)))
        se_y = (svar(j, y, word[y]) if word[y] == 2
                else Poly.const(FROZEN_S.get((j, y, word[y]), 0)))
        response = pe_x * se_y + pe_y * se_x
        if not response:
            continue
        piece = frozen_haf(tuple(v for v in SITES if v not in (x, y)), word)
        if piece:
            total = total + response * piece
    return total


def audit_two_colour_completion_is_impossible():
    """Freeze the eight-cycle's whole colour-0/colour-1 sector; free the whole
    colour-2 sector and all nine direct scalars; decide the 9*729 rows."""
    equations = []
    coefficients = set()
    for word in product(COLORS, repeat=6):
        for i, j in product(COLORS, repeat=2):
            poly = frozen_row(i, j, word) - Poly.const(ghz_target(i, j, word))
            coefficients |= set(poly.terms.values())
            equations.append(((i, j, word), poly))
    unknowns = {v for _, p in equations for m in p.terms for v in m}
    require(len(unknowns) == 60, ("frozen unknown count changed", len(unknowns)))
    require(coefficients == {Q(1), Q(-1)},
            ("the frozen system has a coefficient other than +-1",
             sorted(coefficients)))
    # the eight-cycle point sits in this chart and fails exactly one equation
    ledger = sorted((spot, value) for spot, poly in equations
                    for value in (poly.evaluate({("d", 1, 1): Q(1)}),) if value)
    require(ledger == [(((2, 2, (2,) * 6)), Q(-1))],
            ("the frozen chart lost the eight-cycle point", ledger))

    seen = set()
    stack = [frozenset()]
    open_leaves = 0
    nodes = 0
    closures = set()
    while stack:
        zeros = stack.pop()
        if zeros in seen:
            continue
        seen.add(zeros)
        nodes += 1
        current = set(zeros)
        closed = False
        live = []
        while True:
            live = []
            fresh = set()
            for spot, poly in equations:
                reduced = Poly({m: c for m, c in poly.terms.items()
                                if not any(v in current for v in m)})
                if not reduced:
                    continue
                if len(reduced.terms) == 1:
                    monomial = next(iter(reduced.terms))
                    if not monomial:
                        closed = True
                        closures.add(reduced.terms[monomial])
                        break
                    if len(set(monomial)) == 1:
                        fresh.add(monomial[0])
                live.append(reduced)
            if closed or not fresh - current:
                break
            current |= fresh
        if closed:
            continue
        branch = None
        for reduced in live:
            if len(reduced.terms) == 1:
                factors = tuple(sorted(set(next(iter(reduced.terms))), key=repr))
                if branch is None or len(factors) < len(branch):
                    branch = factors
        if branch is None:
            open_leaves += 1
            continue
        for factor in branch:
            stack.append(frozenset(current | {factor}))
    require(open_leaves == 0,
            ("the eight-cycle completion search left open leaves", open_leaves))
    require(nodes == 695, ("branch node count changed", nodes))
    require(closures == {Q(-1)},
            ("a branch closed on something other than -1", sorted(closures)))


def main():
    audit_normalization()
    system = build_system()
    audit_guard_ledger(system)
    audit_class_factorization(system)
    audit_two_odd_rows_are_direct_free(system)
    audit_anchor_cofactor_lemma()
    audit_anchor_dies_without_cofactors()
    audit_label_kernel_identity(system)
    audit_blind_label_and_blind_colour()
    audit_handle_family()
    audit_named_instances()
    audit_rank_one_alternative()
    audit_residual_support_family()
    audit_two_colour_scope_guard(system)
    audit_two_colour_completion_is_impossible()
    print(
        "PASS: monochromatic chart verified -- guard ledger reproduced; class "
        "factorization holds on all 9x729 rows (183 all-even words, 3 pure and "
        "180 not, 546 two-odd words); two-odd rows are direct-block free; the "
        "anchor row is spanned by the fifteen four-hole cofactors and dies "
        "whenever they all vanish; the label-kernel separation is exact; the "
        "label-blind and colour-blind rows are purely direct; the "
        "handle family and its distance-one, (1,1,4) and three-three instances "
        "are identities; the rank-one alternative is exhaustive over F_2 and "
        "F_3; the rank-two support conditions are satisfiable, so that branch "
        "stays open; the alternating eight-cycle is a monochromatic packet "
        "failing exactly the colour-2 anchor; and freezing its colour-0/1 "
        "sector, no colour-2 completion exists over any field (695 branch "
        "nodes, all coefficients +-1, every closure on -1)"
    )


if __name__ == "__main__":
    main()
