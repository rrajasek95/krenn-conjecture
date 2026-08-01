#!/usr/bin/env python3
"""Exact star-sector repair analysis of the h=3 seven-row guard.

The audited seven-row guard packet of
``verify_h3_diagonal_segre_second_transgression_seven_row_guard.py`` has all
six off-diagonal rows, the complete 22 row, good Segre stars and chi=-2, and
fails exactly the two diagonal anchors (00 at 0^6 and 11 at 1^6).  The
handoff guide's next step is the *star-sector repair*: keep the whole
colour-2 slice, which is what pins chi, and try to restore the missing
anchors by adding colour-0 and colour-1 entries to both endpoint stars,
free colour-0/colour-1 internal quadratic edges, and arbitrary direct
scalars.

Call the six off-diagonal rows plus the complete 22 row, on all 729 words,
*the seven rows*.  The guard is a solution of that system, so it is
consistent, and everything below is an identity on a non-empty variety.
This checker proves:

  R1  the seven rows force twelve star entries and twenty internal edges to
      zero, collapsing each colour-c internal support into {04,05,14,15,23};
  R2  the anchor peels onto one edge:
          Row(c,c,c^6) = q_c(2,3) * rho_c(c,c, W\\{2,3});
  R3  the full trade family at the witness word, whose pure part reads
          d_ij * q_c(2,3) = 0   for (i,j) in {01,02,12,20}
          (1 + d_10) * q_c(2,3) = 0;
  R4  on the frozen slice the only caps with a nonzero terminal class are
      (0,1) with chi = -2*d_01 and (0,2) with chi = d_02/2;
  R5  hence the product identity  q_c(2,3) * chi = 0, literally -2 times a
      single row equation at a single word.

The anchor carrier and the terminal class annihilate each other.  The guard
sits at q_c(2,3) = 0, chi = -2.  Corollaries, by exhaustive branching: the
seven rows plus the *complete* colour-c anchor row are infeasible for both
c = 0 and c = 1, and so is the full nine-row system.

*Not verified here*, each established by the named sibling checker and
imported only as context: the hypothesis of R5 is attainable, seven rows plus
the colour-0 anchor at its pure word having an explicit witness with chi = 0
exactly as R5 predicts, while the same for colour 1 is impossible
(verify_h3_star_sector_pure_word_anchor_witness.py); the peel and the trade
are specific to this slice
(verify_h3_complementary_guard_star_sector_transport.py); and chi is in any
case invisible to the matching tensor
(verify_fourhole_allword_row_identity_grade_ladder.py).

Scope: this is the *monochromatic* ansatz throughout.  The last section
verifies that with cross-colour internal edges the collapse genuinely fails,
so nothing here is claimed beyond monochromatic internal quadratics.

No certified dependency is changed; Krenn's conjecture remains open.
Standard library only, exact Fraction arithmetic, live under ``python -O``.
"""

from fractions import Fraction as Q
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise AssertionError(message)


COLORS = (0, 1, 2)
SITES = tuple(range(6))
PURE = 2
ANCHOR_ROWS = ((0, 0), (1, 1))

# --- frozen colour-2 slice, copied from the audited guard checker ----------
Q2 = {(0, 1): Q(1), (4, 5): Q(1)}
P2 = {0: (Q(1), Q(1), Q(0), Q(0), Q(0), Q(0)),
      1: (Q(0), Q(0), Q(0), Q(0), Q(1), Q(0)),
      2: (Q(0), Q(0), Q(1), Q(1), Q(0), Q(0))}
S2 = {0: (Q(0), Q(0), Q(0), Q(0), Q(0), Q(1)),
      1: (Q(0), Q(0), Q(1), Q(-1), Q(0), Q(0)),
      2: (Q(0), Q(0), Q(1, 2), Q(1, 2), Q(0), Q(0))}


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


# --------------------------------------------------------------------------
# minimal exact sparse polynomial ring over the repair unknowns
# --------------------------------------------------------------------------
class Poly:
    __slots__ = ("terms",)

    def __init__(self, terms=None):
        self.terms = {m: c for m, c in (terms or {}).items() if c}

    @staticmethod
    def const(value):
        value = Q(value)
        return Poly({(): value} if value else {})

    @staticmethod
    def var(name):
        return Poly({(name,): Q(1)})

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

    def scale(self, value):
        return Poly({m: c * Q(value) for m, c in self.terms.items()})

    def kill(self, zeros):
        return Poly({m: c for m, c in self.terms.items()
                     if not any(v in zeros for v in m)})

    def fix(self, variable, value):
        """Substitute a constant for one variable."""
        out = {}
        for m, c in self.terms.items():
            power = m.count(variable)
            key = tuple(v for v in m if v != variable) if power else m
            coefficient = c * (Q(value) ** power) if power else c
            total = out.get(key, Q(0)) + coefficient
            if total:
                out[key] = total
            else:
                out.pop(key, None)
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


ALLOW_CROSS = [False]


def q_edge(x, y, cx, cy):
    if x > y:
        x, y = y, x
        cx, cy = cy, cx
    if cx == PURE and cy == PURE:
        return Poly.const(Q2.get((x, y), 0))
    if cx != cy:
        if ALLOW_CROSS[0]:
            return Poly.var(("X", x, y, cx, cy))
        return Poly.const(0)
    return Poly.var(("q", cx, x, y))


def p_entry(i, x, c):
    return Poly.const(P2[i][x]) if c == PURE else Poly.var(("p", i, x, c))


def s_entry(j, y, c):
    return Poly.const(S2[j][y]) if c == PURE else Poly.var(("s", j, y, c))


def d_entry(i, j):
    return Poly.var(("d", i, j))


def haf(sites, word):
    total = Poly.const(0)
    for matching in matchings(tuple(sites)):
        term = Poly.const(1)
        for x, y in matching:
            term = term * q_edge(x, y, word[x], word[y])
            if not term:
                break
        total = total + term
    return total


def response(i, j, x, y, word):
    return (p_entry(i, x, word[x]) * s_entry(j, y, word[y])
            + p_entry(i, y, word[y]) * s_entry(j, x, word[x]))


def row(i, j, word, sites=SITES):
    sites = tuple(sites)
    total = d_entry(i, j) * haf(sites, word)
    for x, y in combinations(sites, 2):
        cell = response(i, j, x, y, word)
        if not cell:
            continue
        complement = tuple(v for v in sites if v not in (x, y))
        piece = haf(complement, word)
        if piece:
            total = total + cell * piece
    return total


def build_system():
    """The 9*729 GHZ row equations as polynomials that must all vanish."""
    out = {}
    for word in product(COLORS, repeat=6):
        for i, j in product(COLORS, repeat=2):
            target = Q(i == j and all(c == i for c in word))
            out[(i, j, word)] = row(i, j, word) - Poly.const(target)
    return out


SYSTEM = build_system()
SEVEN = {spot: poly for spot, poly in SYSTEM.items()
         if spot[:2] not in ANCHOR_ROWS}

# The guard is the origin of the repair chart: every repair unknown zero, and
# the single direct scalar d_01 = 1.
GUARD_POINT = {("d", 0, 1): Q(1)}


# --------------------------------------------------------------------------
# the branch search used for every infeasibility claim
# --------------------------------------------------------------------------
def branch_search(equations):
    """Exhaustively decide a polynomial system by splitting single-monomial
    equations into their factors, which is valid over a field, and
    propagating forced single-variable equations.  Returns (nodes, leaves)
    where leaves are the nodes at which no monomial equation remains; an
    empty leaf list is a proof of infeasibility."""
    seen = set()
    stack = [frozenset()]
    leaves = []
    nodes = 0
    while stack:
        start = stack.pop()
        if start in seen:
            continue
        seen.add(start)
        nodes += 1
        current = set(start)
        closed = False
        while True:
            live = []
            fresh = set()
            for poly in equations:
                reduced = poly.kill(current)
                if not reduced:
                    continue
                if len(reduced.terms) == 1:
                    monomial = next(iter(reduced.terms))
                    if not monomial:
                        closed = True
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
            leaves.append(frozenset(current))
            continue
        for factor in branch:
            stack.append(frozenset(current | {factor}))
    return nodes, leaves


# --------------------------------------------------------------------------
# 1.  normalization, and agreement with the committed guard ledger
# --------------------------------------------------------------------------
def audit_normalization_and_baseline():
    def plain_haf(sites):
        total = Q(0)
        for matching in matchings(tuple(sites)):
            total += Q(1)
        return total

    require(plain_haf(SITES) == 15, "all-ones six-site hafnian is not 15")
    require(plain_haf((0, 1, 2, 3)) == 3, "all-ones four-site hafnian is not 3")
    require(plain_haf((0, 1)) == 1, "all-ones two-site hafnian is not 1")

    ledger = sorted(
        (i, j, word, value)
        for (i, j, word), poly in SYSTEM.items()
        for value in (poly.evaluate(GUARD_POINT),)
        if value
    )
    require(
        ledger == [(0, 0, (0,) * 6, Q(-1)), (1, 1, (1,) * 6, Q(-1))],
        ("the symbolic system does not reproduce the committed guard ledger",
         ledger),
    )
    require(all(not poly.evaluate(GUARD_POINT) for poly in SEVEN.values()),
            "the guard does not satisfy the seven rows")


# --------------------------------------------------------------------------
# 2.  terminal class of every cap on the frozen colour-2 slice
# --------------------------------------------------------------------------
def cap_layers(a, b, alpha):
    u = P2[a]
    v = S2[b]
    internal = [[Q(0) if x == y else Q(Q2.get((min(x, y), max(x, y)), 0))
                 for y in SITES] for x in SITES]
    resp = [[Q(0) if x == y else u[x] * v[y] + v[x] * u[y]
             for y in SITES] for x in SITES]
    layers = []
    for used in range(4):
        value = Q(0)
        for matching in matchings(SITES):
            for flags in product((0, 1), repeat=3):
                if sum(flags) != used:
                    continue
                term = Q(1)
                for flag, (x, y) in zip(flags, matching):
                    term *= resp[x][y] if flag else Q(alpha) * internal[x][y]
                value += term
        layers.append(value)
    return tuple(layers)


def audit_terminal_class_table():
    # Layer j is exactly alpha^(3-j) * Q_j by construction, so it is a
    # polynomial of degree at most 3 in alpha; agreement at three distinct
    # values therefore decides the claimed linearity, and this is a proof
    # rather than a sample.
    profile = {}
    for a, b in product(COLORS, repeat=2):
        rows = {alpha: cap_layers(a, b, alpha) for alpha in (1, 2, -3)}
        q2, q3 = rows[1][2], rows[1][3]
        for alpha, layers in rows.items():
            require(layers[2] == Q(alpha) * q2,
                    ("layer two is not linear in the direct scalar", a, b))
            require(layers[3] == q3,
                    ("layer three depends on the direct scalar", a, b))
        # Q0 = haf(q_2) = 0 for every pair, because q_2 = 01+45 has no six-site
        # matching; only that makes "Q0 = Q1 = 0" equivalent to the source
        # relation alpha*Q0 + Q1 = 0.  Assert it rather than rely on it.
        require(rows[1][0] == 0,
                ("q_2 acquired a six-site matching, so Q0 = 0 no longer "
                 "reduces the source relation", a, b))
        profile[(a, b)] = (rows[1][1] == 0, q2, q3)

    require(profile[(0, 1)] == (True, Q(-2), Q(0)),
            ("selected (0,1) cap changed", profile[(0, 1)]))
    require(profile[(0, 2)] == (True, Q(1, 2), Q(0)),
            ("selected (0,2) cap changed", profile[(0, 2)]))
    require(profile[(2, 2)][0] is False,
            "the (2,2) cap unexpectedly satisfies the source relation")
    live = sorted(pair for pair, (ok, q2, q3) in profile.items()
                  if ok and (q2 or q3))
    require(live == [(0, 1), (0, 2)],
            ("the set of caps with a nonzero terminal class changed", live))


# --------------------------------------------------------------------------
# 3.  geometry of the frozen slice
# --------------------------------------------------------------------------
def audit_frozen_slice_geometry():
    word = {site: PURE for site in SITES}
    live = [T for T in combinations(SITES, 4) if haf(T, word)]
    require(live == [(0, 1, 4, 5)],
            ("the frozen colour-2 four-set support changed", live))
    require(haf((0, 1, 4, 5), word) == Poly.const(1),
            "the surviving colour-2 four-site hafnian is not 1")

    for i, j in product(COLORS, repeat=2):
        companion = (row(i, j, word, sites=(0, 1, 4, 5))
                     - d_entry(i, j) * haf((0, 1, 4, 5), word))
        expected = Poly.const(1) if (i, j) == (1, 0) else Poly.const(0)
        require(companion == expected,
                ("the frozen four-site companion changed", i, j))

    detecting = tuple(
        pair for pair in combinations(SITES, 2)
        if pair != (2, 3)
        and any(row(i, j, word, sites=tuple(v for v in SITES if v not in pair))
                for i, j in product(COLORS, repeat=2))
    )
    require(
        detecting == ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3),
                      (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)),
        ("the detecting-pair set changed", detecting),
    )


# --------------------------------------------------------------------------
# 4.  the collapse, forced by the seven rows alone
# --------------------------------------------------------------------------
FORCED_BY_SEVEN = {
    ("p", 0, 2, 0): (0, 1, (2, 2, 0, 2, 2, 2)),
    ("p", 0, 2, 1): (0, 1, (2, 2, 1, 2, 2, 2)),
    ("p", 0, 3, 0): (0, 1, (2, 2, 2, 0, 2, 2)),
    ("p", 0, 3, 1): (0, 1, (2, 2, 2, 1, 2, 2)),
    ("p", 1, 2, 0): (1, 2, (2, 2, 0, 2, 2, 2)),
    ("p", 1, 2, 1): (1, 2, (2, 2, 1, 2, 2, 2)),
    ("p", 1, 3, 0): (1, 2, (2, 2, 2, 0, 2, 2)),
    ("p", 1, 3, 1): (1, 2, (2, 2, 2, 1, 2, 2)),
    ("s", 0, 2, 0): (2, 0, (2, 2, 0, 2, 2, 2)),
    ("s", 0, 2, 1): (2, 0, (2, 2, 1, 2, 2, 2)),
    ("s", 0, 3, 0): (2, 0, (2, 2, 2, 0, 2, 2)),
    ("s", 0, 3, 1): (2, 0, (2, 2, 2, 1, 2, 2)),
    ("q", 0, 0, 1): (2, 2, (0, 0, 2, 2, 2, 2)),
    ("q", 0, 0, 2): (0, 1, (0, 2, 0, 2, 2, 2)),
    ("q", 0, 0, 3): (0, 1, (0, 2, 2, 0, 2, 2)),
    ("q", 0, 1, 2): (0, 1, (2, 0, 0, 2, 2, 2)),
    ("q", 0, 1, 3): (0, 1, (2, 0, 2, 0, 2, 2)),
    ("q", 0, 2, 4): (2, 0, (2, 2, 0, 2, 0, 2)),
    ("q", 0, 2, 5): (1, 2, (2, 2, 0, 2, 2, 0)),
    ("q", 0, 3, 4): (2, 0, (2, 2, 2, 0, 0, 2)),
    ("q", 0, 3, 5): (1, 2, (2, 2, 2, 0, 2, 0)),
    ("q", 0, 4, 5): (2, 2, (2, 2, 2, 2, 0, 0)),
    ("q", 1, 0, 1): (2, 2, (1, 1, 2, 2, 2, 2)),
    ("q", 1, 0, 2): (0, 1, (1, 2, 1, 2, 2, 2)),
    ("q", 1, 0, 3): (0, 1, (1, 2, 2, 1, 2, 2)),
    ("q", 1, 1, 2): (0, 1, (2, 1, 1, 2, 2, 2)),
    ("q", 1, 1, 3): (0, 1, (2, 1, 2, 1, 2, 2)),
    ("q", 1, 2, 4): (2, 0, (2, 2, 1, 2, 1, 2)),
    ("q", 1, 2, 5): (1, 2, (2, 2, 1, 2, 2, 1)),
    ("q", 1, 3, 4): (2, 0, (2, 2, 2, 1, 1, 2)),
    ("q", 1, 3, 5): (1, 2, (2, 2, 2, 1, 2, 1)),
    ("q", 1, 4, 5): (2, 2, (2, 2, 2, 2, 1, 1)),
}

SURVIVING_PAIRS = ((0, 4), (0, 5), (1, 4), (1, 5), (2, 3))


def audit_collapse():
    zeros = set()
    for variable, spot in FORCED_BY_SEVEN.items():
        require(spot[:2] not in ANCHOR_ROWS,
                ("a forcing used a restored anchor row", variable, spot))
        reduced = SYSTEM[spot].kill(zeros)
        monomial = next(iter(reduced.terms)) if len(reduced.terms) == 1 else None
        require(monomial is not None and monomial == (variable,),
                ("the forcing equation is not a single unknown", variable, spot))
        zeros.add(variable)
    require(len(zeros) == 32, ("wrong forced-zero count", len(zeros)))

    extra = set()
    for spot, poly in SEVEN.items():
        reduced = poly.kill(zeros)
        if len(reduced.terms) == 1:
            monomial = next(iter(reduced.terms))
            require(monomial, ("premature contradiction", spot))
            if len(set(monomial)) == 1 and monomial[0] not in zeros:
                extra.add(monomial[0])
    require(not extra, ("the collapse is not closed", sorted(map(str, extra))))

    for colour in (0, 1):
        alive = tuple(pair for pair in combinations(SITES, 2)
                      if ("q", colour) + pair not in zeros)
        require(alive == SURVIVING_PAIRS,
                ("colour-%d support collapse changed" % colour, alive))
    return zeros


# --------------------------------------------------------------------------
# 5.  the pure-word row is a grade-zero four-hole pairing
# --------------------------------------------------------------------------
def audit_fourhole_row_form():
    """Row(i,j,w) = <(d_ij/3) q^w + R^w_ij, H(q^w)>, with H(A)_e=haf(A[W\\e]).
    Proof: <q^w,H(q^w)> = 3 haf(q^w), each matching counted once per edge.
    Verified on all 729 words, not only the pure ones."""
    for letters in product(COLORS, repeat=6):
        word = {site: letters[site] for site in SITES}
        colour = letters[0] if len(set(letters)) == 1 else None
        h0 = {e: haf(tuple(v for v in SITES if v not in e), word)
              for e in combinations(SITES, 2)}
        pairing = Poly.const(0)
        for e in combinations(SITES, 2):
            pairing = pairing + q_edge(e[0], e[1], word[e[0]], word[e[1]]) * h0[e]
        require(pairing == haf(SITES, word).scale(3),
                ("<q,H> = 3 haf(q) failed", letters))
        for i, j in product(COLORS, repeat=2):
            built = Poly.const(0)
            for e in combinations(SITES, 2):
                probe = (d_entry(i, j)
                         * q_edge(e[0], e[1], word[e[0]], word[e[1]])).scale(Q(1, 3))
                built = built + (probe + response(i, j, e[0], e[1], word)) * h0[e]
            require(built == row(i, j, word),
                    ("the four-hole form of the row failed", i, j, letters))
        support = sorted(e for e in h0 if h0[e])
        if colour == PURE:
            require(support == [(2, 3)],
                    ("the frozen grade-0 four-hole support changed", support))


# --------------------------------------------------------------------------
# 6.  the anchor peel, the full trade family, and the product identity
# --------------------------------------------------------------------------
def anchor_carrier(colour):
    return Poly.var(("q", colour, 2, 3))


def witness_word(colour):
    return tuple(colour if site in (2, 3) else PURE for site in SITES)


def audit_peel_trade_and_product(zeros):
    complement = (0, 1, 4, 5)
    for colour in (0, 1):
        pure = (colour,) * 6
        anchor = SYSTEM[(colour, colour, pure)].kill(zeros)
        four_site_word = {site: colour for site in SITES}
        rho = row(colour, colour, four_site_word, sites=complement).kill(zeros)
        # the note displays rho as ten explicit monomials; rebuild them
        literal = d_entry(colour, colour) * (
            Poly.var(("q", colour, 0, 4)) * Poly.var(("q", colour, 1, 5))
            + Poly.var(("q", colour, 0, 5)) * Poly.var(("q", colour, 1, 4)))
        for edge_key, x, y in ((("q", colour, 0, 4), 1, 5),
                               (("q", colour, 0, 5), 1, 4),
                               (("q", colour, 1, 4), 0, 5),
                               (("q", colour, 1, 5), 0, 4)):
            literal = literal + Poly.var(edge_key) * (
                p_entry(colour, x, colour) * s_entry(colour, y, colour)
                + p_entry(colour, y, colour) * s_entry(colour, x, colour))
        require(rho == literal,
                ("the literal rho reconstruction failed", colour))
        edge = anchor_carrier(colour)
        require(anchor == edge * rho - Poly.const(1),
                ("the anchor peel identity failed", colour))
        require(not [m for m in anchor.terms if m and ("q", colour, 2, 3) not in m],
                ("an anchor monomial avoids the peeled edge", colour))
        require(len(anchor.terms) == 11,
                ("anchor term count changed", colour, len(anchor.terms)))

        # the full trade family at the witness word
        word = witness_word(colour)
        pure_trade = {(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 0)}
        for i, j in product(COLORS, repeat=2):
            reduced = SYSTEM[(i, j, word)].kill(zeros)
            if (i, j) in pure_trade:
                require(reduced == d_entry(i, j) * edge,
                        ("pure trade equation changed", colour, i, j))
            elif (i, j) == (1, 0):
                require(reduced == edge + d_entry(1, 0) * edge,
                        ("shifted trade equation changed", colour))
            else:
                bracket = (p_entry(2, 2, colour) * s_entry(j, 3, colour)
                           + p_entry(2, 3, colour) * s_entry(j, 2, colour))
                require(reduced == d_entry(i, j) * edge + bracket,
                        ("star-corrected trade equation changed", colour, i, j))
                require(i == 2 and j in (1, 2),
                        ("unexpected star-corrected pair", colour, i, j))

        # only four of the pure trade equations come from the seven rows
        from_seven = sorted(pair for pair in pure_trade
                            if pair not in ANCHOR_ROWS)
        require(from_seven == [(0, 1), (0, 2), (1, 2), (2, 0)],
                ("seven-row trade set changed", from_seven))

        # the product identity, as an exact multiple of one row equation
        for pair, factor in (((0, 1), Q(-2)), ((0, 2), Q(1, 2))):
            chi = d_entry(*pair).scale(factor)
            require(edge * chi == SYSTEM[(pair[0], pair[1], word)].kill(zeros).scale(factor),
                    ("the product identity failed", colour, pair))


# --------------------------------------------------------------------------
# 7.  infeasibility corollaries
# --------------------------------------------------------------------------
LIVE_ANCHOR_ZEROS = {("d", 0, 1), ("d", 0, 2), ("d", 1, 2), ("d", 2, 0)}


def audit_anchor_row_infeasibility(zeros):
    """Seven rows plus the complete colour-c anchor row have no solution."""
    for colour, expected in ((0, 486), (1, 2636)):
        edge = ("q", colour, 2, 3)
        # branch A: the carrier vanishes, and the anchor equation is -1
        dead = SYSTEM[(colour, colour, (colour,) * 6)].kill(zeros | {edge})
        require(dead == Poly.const(-1),
                ("branch A did not close on -1", colour, dead.terms))
        # branch B: the carrier is nonzero, so the trade substitutions apply
        subsystem = []
        for spot, poly in SYSTEM.items():
            if spot[:2] in ANCHOR_ROWS and spot[:2] != (colour, colour):
                continue
            reduced = poly.kill(zeros | LIVE_ANCHOR_ZEROS).fix(("d", 1, 0), -1)
            if reduced:
                subsystem.append(reduced)
        nodes, leaves = branch_search(subsystem)
        require(not leaves,
                ("branch B left open leaves", colour, len(leaves)))
        require(nodes == expected,
                ("branch B node count changed", colour, nodes))


def audit_nine_row_infeasibility():
    nodes, leaves = branch_search(list(SYSTEM.values()))
    require(not leaves, ("the nine-row search left open leaves", len(leaves)))
    require(nodes == 533, ("nine-row node count changed", nodes))


def audit_pure_word_anchor_leaf_census(zeros):
    """The seven rows plus the colour-0 anchor at its pure word ONLY are not
    decided by this branch search: it terminates with open leaves, which are
    not evidence of feasibility.  That system is in fact feasible, by the
    explicit witness of
    verify_h3_star_sector_pure_word_anchor_witness.py, which also decides
    every one of these leaves -- 373 feasible, 10 closed, *not verified
    here*.  The census is kept
    here as the regression tripwire for the search itself."""
    subsystem = []
    for spot, poly in SYSTEM.items():
        if spot[:2] in ANCHOR_ROWS and spot != (0, 0, (0,) * 6):
            continue
        reduced = poly.kill(zeros | LIVE_ANCHOR_ZEROS).fix(("d", 1, 0), -1)
        if reduced:
            subsystem.append(reduced)
    nodes, leaves = branch_search(subsystem)
    require(nodes == 11290 and len(leaves) == 383,
            ("the leaf census changed", nodes, len(leaves)))


# --------------------------------------------------------------------------
# 8.  scope guard: the collapse is monochromatic-only
# --------------------------------------------------------------------------
def audit_cross_colour_scope():
    ALLOW_CROSS[0] = True
    try:
        cross = build_system()
    finally:
        ALLOW_CROSS[0] = False

    cross_seven = {spot: poly for spot, poly in cross.items()
                   if spot[:2] not in ANCHOR_ROWS}
    zeros = set()
    while True:
        fresh = set()
        for spot, poly in cross_seven.items():
            reduced = poly.kill(zeros)
            if len(reduced.terms) == 1:
                monomial = next(iter(reduced.terms))
                require(monomial, ("cross-colour contradiction", spot))
                if len(set(monomial)) == 1:
                    fresh.add(monomial[0])
        if not fresh - zeros:
            break
        zeros |= fresh

    require(len(zeros) == 8,
            ("cross-colour forced-zero count changed", len(zeros)))
    require(all(v[0] == "X" for v in zeros),
            "cross-colour forcing unexpectedly touched a star or a monochromatic edge")

    # That count of 8 is a property of the propagation rule above, NOT of the
    # system: the rule only absorbs equations that reduce to a single repeated
    # variable.  Full elimination of the degree-one equations forces 20 and
    # leaves two relations, so the honest scope statement uses this number.
    linear = [poly for poly in cross.values()
              if poly and max(len(m) for m in poly.terms) == 1
              and () not in poly.terms]
    require(len(linear) == 22, ("degree-one count changed", len(linear)))
    names = sorted({v for poly in linear for m in poly.terms for v in m}, key=repr)
    column = {v: k for k, v in enumerate(names)}
    rows = []
    for poly in linear:
        entry = [Q(0)] * len(names)
        for m, c in poly.terms.items():
            entry[column[m[0]]] += c
        rows.append(entry)
    pivot = 0
    pivots = []
    for col in range(len(names)):
        found = next((r for r in range(pivot, len(rows)) if rows[r][col]), None)
        if found is None:
            continue
        rows[pivot], rows[found] = rows[found], rows[pivot]
        scale = rows[pivot][col]
        rows[pivot] = [x / scale for x in rows[pivot]]
        for r in range(len(rows)):
            if r != pivot and rows[r][col]:
                factor = rows[r][col]
                rows[r] = [a - factor * b for a, b in zip(rows[r], rows[pivot])]
        pivots.append(col)
        pivot += 1
    eliminated, relations = [], []
    for k, col in enumerate(pivots):
        support = [names[c] for c in range(len(names)) if rows[k][c]]
        (eliminated if len(support) == 1 else relations).append(support)
    require(len(eliminated) == 20,
            ("cross-colour linear elimination changed", len(eliminated)))
    require(sorted(relations) == [[("X", 2, 4, 2, 0), ("X", 3, 4, 2, 0)],
                                 [("X", 2, 4, 2, 1), ("X", 3, 4, 2, 1)]],
            ("cross-colour residual relations changed", relations))

    # even after the stronger elimination the anchor does not peel
    strong = {v for support in eliminated for v in support}
    for colour in (0, 1):
        anchor = cross[(colour, colour, (colour,) * 6)].kill(zeros)
        loose = [m for m in anchor.terms if m and ("q", colour, 2, 3) not in m]
        require(len(loose) == 90,
                ("cross-colour anchor leakage changed", colour, len(loose)))
        anchor = cross[(colour, colour, (colour,) * 6)].kill(strong)
        loose = [m for m in anchor.terms if m and ("q", colour, 2, 3) not in m]
        require(loose, ("the cross-colour anchor unexpectedly peeled", colour))


def main():
    audit_normalization_and_baseline()
    audit_terminal_class_table()
    audit_frozen_slice_geometry()
    zeros = audit_collapse()
    audit_fourhole_row_form()
    audit_peel_trade_and_product(zeros)
    audit_anchor_row_infeasibility(zeros)
    audit_nine_row_infeasibility()
    audit_pure_word_anchor_leaf_census(zeros)
    audit_cross_colour_scope()
    print(
        "PASS: guard ledger reproduced symbolically and the guard satisfies the "
        "seven rows; caps (0,1),(0,2) carry chi=-2*d_01, d_02/2 and no others; "
        "the seven rows alone force 32 zeros collapsing each colour support to "
        "{04,05,14,15,23}; pure-word rows are grade-0 four-hole pairings and "
        "|supp H0_2|=1; anchor peel Row(c,c,c^6)=q_c(2,3)*rho_c(c,c,W\\{2,3}); "
        "full trade family; product identity q_c(2,3)*chi=0; seven rows plus "
        "either complete anchor row infeasible (486/2636 nodes) and the nine-row "
        "system infeasible (533); the pure-word-only anchor "
        "not decided by this search (383 leaves; decided elsewhere); "
        "cross-colour scope guard (8 by monomial propagation, 20 plus two "
        "relations by full linear elimination, and still no peel)"
    )


if __name__ == "__main__":
    main()
