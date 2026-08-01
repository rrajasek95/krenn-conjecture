#!/usr/bin/env python3
"""Is the star-sector anchor/terminal trade packet-specific or general?

`verify_h3_star_sector_anchor_terminal_trade.py` found, on the audited
seven-row guard (which supplies X_2 and misses X_0, X_1 and carries chi=-2),
that after freezing its colour-2 slice and freeing the colour-0/1 repair
sector:

  (a) the guard's own supplied rows collapse the free support;
  (b) each missing anchor peels onto one internal edge,
        Row(c,c,c^6) = q_c(2,3) * rho_c(c,c, W\\{2,3});
  (c) that edge annihilates the direct scalars carrying chi.

This checker transports the same experiment to two further packets and pins
exactly what recurs.

PACKET A -- the committed complementary all-word 8/9 guard, section 3 (G1)-(G5)
of `notes/tagged-incidence-cokernel-hamming-one-boundary.md`, audited by
`verify_tagged_incidence_cokernel_eight_row_guard.py`.  It supplies X_0, X_1
and misses X_2, the mirror image of the seven-row guard.  Freezing its
colour-0/1 slice and freeing the whole colour-2 sector plus all nine direct
scalars (60 unknowns), the eight supplied rows on all 729 words force 36
unknowns to zero; the colour-2 internal support collapses to the perfect
matching {05,13,24}; every colour-2 star entry off the sites {2,4} dies; the
missing anchor peels off a two-edge sub-matching,

        Row(2,2,2^6) = q_2(0,5) * q_2(1,3) * rho_2(2,2,{2,4}),

and the trade equations appear as d_ij * q_2(0,5) = 0 for all eight supplied
label pairs.  So the collapse, the peel and the trade all recur, with
different combinatorics.  What does *not* recur is their consequence: this
packet's terminal class is identically zero -- before and after the collapse
-- so there is nothing left to trade against, and the trade instead kills the
whole direct block and makes the anchor row the constant -1.

PACKETS B and C -- two perturbed seven-row guards built here.  Both have the
audited guard's missing ledger (00,0^6,-1), (11,1^6,-1), rank-three stars,
literal Segre responses and a nonzero terminal class; both differ from it only
in the colour-2 internal quadratic, which is no longer degenerate.  B uses
q_2=01+23+45 (hafnian 1, three live four-sets, chi=4 forced) and C uses
q_2=01+23+04+25 (hafnian 0, four live four-sets, chi=-4*d_01 with d_01 free --
the same cap profile as the audited guard).  On both, the collapse still
happens (44 and 40 forced zeros), but the anchor rows do **not** peel.  On B
no trade equation exists at all; on C trade equations do appear, but they
annihilate only d_10, d_20, d_21 and never the class carrier d_01.  So the
collapse is robust, while the peel and the class-killing trade are lost.
What governs them is the geometry of the collapsed support, NOT the number of
live four-sets: that count is neither necessary nor sufficient, and the
endpoint stars are what decide how far the collapse reaches.

Nothing here changes a certified dependency; Krenn's conjecture remains open.
Both ansaetze are infeasible outright, so neither produces a nine-row packet.
Standard library only, exact Fraction arithmetic, live under ``python -O``.
"""

from fractions import Fraction as Q
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise AssertionError(message)


COLORS = (0, 1, 2)
SITES = tuple(range(6))

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
        acc = []
        for position in range(1, len(vertices)):
            remainder = vertices[1:position] + vertices[position + 1:]
            for tail in matchings(remainder):
                acc.append(((vertices[0], vertices[position]),) + tail)
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

    def kill(self, zeros):
        return Poly({m: c for m, c in self.terms.items()
                     if not any(v in zeros for v in m)})

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


# --------------------------------------------------------------------------
# a repair ansatz: a frozen colour slice plus free colours
# --------------------------------------------------------------------------
class Ansatz:
    """Frozen data on the frozen colours; monochromatic free internal edges,
    free star entries on the free colours, and all nine free direct scalars."""

    def __init__(self, frozen_q, frozen_p, frozen_s, free_colours):
        self.frozen_q = frozen_q          # {(x, y, cx, cy): value}, x < y
        self.frozen_p = frozen_p          # {(i, x, c): value}
        self.frozen_s = frozen_s          # {(j, y, c): value}
        self.free = tuple(free_colours)

    def q_edge(self, x, y, cx, cy):
        if x > y:
            x, y, cx, cy = y, x, cy, cx
        if cx not in self.free and cy not in self.free:
            return Poly.const(self.frozen_q.get((x, y, cx, cy), 0))
        if cx != cy:
            return Poly.const(0)          # monochromatic ansatz
        return Poly.var(("q", cx, x, y))

    def p_entry(self, i, x, c):
        if c not in self.free:
            return Poly.const(self.frozen_p.get((i, x, c), 0))
        return Poly.var(("p", i, x, c))

    def s_entry(self, j, y, c):
        if c not in self.free:
            return Poly.const(self.frozen_s.get((j, y, c), 0))
        return Poly.var(("s", j, y, c))

    def haf(self, sites, word):
        total = Poly.const(0)
        for matching in matchings(tuple(sites)):
            term = Poly.const(1)
            for x, y in matching:
                term = term * self.q_edge(x, y, word[x], word[y])
                if not term:
                    break
            total = total + term
        return total

    def row(self, i, j, word, sites=SITES):
        sites = tuple(sites)
        total = Poly.var(("d", i, j)) * self.haf(sites, word)
        for x, y in combinations(sites, 2):
            response = (self.p_entry(i, x, word[x]) * self.s_entry(j, y, word[y])
                        + self.p_entry(i, y, word[y]) * self.s_entry(j, x, word[x]))
            if not response:
                continue
            complement = tuple(v for v in sites if v not in (x, y))
            piece = self.haf(complement, word)
            if piece:
                total = total + response * piece
        return total

    def system(self):
        out = {}
        for word in product(COLORS, repeat=6):
            for i, j in product(COLORS, repeat=2):
                target = Q(i == j and all(c == i for c in word))
                out[(i, j, word)] = self.row(i, j, word) - Poly.const(target)
        return out


def cap_layers(frozen_q, frozen_p, frozen_s, a, b, colour):
    """(Q_0,...,Q_3) with Q_k = R^[k] q^[3-k] on the pure colour word."""
    internal = [[Q(0)] * 6 for _ in SITES]
    response = [[Q(0)] * 6 for _ in SITES]
    for x, y in combinations(SITES, 2):
        value = frozen_q.get((x, y, colour, colour), Q(0))
        internal[x][y] = internal[y][x] = value
        cross = (frozen_p.get((a, x, colour), Q(0)) * frozen_s.get((b, y, colour), Q(0))
                 + frozen_p.get((a, y, colour), Q(0)) * frozen_s.get((b, x, colour), Q(0)))
        response[x][y] = response[y][x] = cross
    layers = []
    for used in range(4):
        total = Q(0)
        for matching in matchings(SITES):
            for flags in product((0, 1), repeat=3):
                if sum(flags) != used:
                    continue
                term = Q(1)
                for flag, (x, y) in zip(flags, matching):
                    term *= response[x][y] if flag else internal[x][y]
                total += term
        layers.append(total)
    return tuple(layers)


def propagate(system, rows_allowed):
    """Close the single-variable forcings using only the allowed rows."""
    zeros = set()
    while True:
        fresh = set()
        for (i, j, word), poly in system.items():
            if (i, j) not in rows_allowed:
                continue
            reduced = poly.kill(zeros)
            if len(reduced.terms) == 1:
                monomial = next(iter(reduced.terms))
                require(monomial, ("premature contradiction", i, j, word))
                if len(set(monomial)) == 1:
                    fresh.add(monomial[0])
        if not fresh - zeros:
            return zeros
        zeros |= fresh


def branch_search(system):
    """Exhaustive split of every single-monomial equation into its factors."""
    equations = list(system.items())
    seen, stack, open_leaves, nodes = set(), [frozenset()], [], 0
    while stack:
        start = stack.pop()
        if start in seen:
            continue
        seen.add(start)
        nodes += 1
        current, closed, live = set(start), False, []
        while True:
            live, fresh = [], set()
            for spot, poly in equations:
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
            open_leaves.append(frozenset(current))
            continue
        for factor in branch:
            stack.append(frozenset(current | {factor}))
    return nodes, open_leaves


# ==========================================================================
# PACKET A: the committed complementary all-word 8/9 guard
# ==========================================================================
# (G2) of notes/tagged-incidence-cokernel-hamming-one-boundary.md, copied
# verbatim from verify_tagged_incidence_cokernel_eight_row_guard.py.
A_Q = {(2, 3, 0, 0): Q(1), (4, 5, 0, 0): Q(1),
       (1, 2, 1, 1): Q(1), (3, 4, 1, 1): Q(1)}
A_P = {(0, 0, 0): Q(1), (1, 5, 1): Q(1), (2, 2, 2): Q(1)}
A_S = {(0, 1, 0): Q(1), (1, 0, 1): Q(1), (2, 4, 0): Q(1)}
A_D = {(0, 2): Q(1)}
A_MISSING = (2, 2)
A_SUPPLIED = tuple((i, j) for i in COLORS for j in COLORS if (i, j) != A_MISSING)

# repair chart: the guard point has d_02 = 1 and the single colour-2 star
# entry p_2(2) = 1; everything else in the free colour-2 sector is zero.
A_GUARD_POINT = {("d", 0, 2): Q(1), ("p", 2, 2, 2): Q(1)}

# Each forcing below is witnessed by one of the guard's eight *supplied* rows.
A_FORCED = (
    (("q", 2, 4, 5), (0, 0, (0, 0, 0, 0, 2, 2))),
    (("q", 2, 2, 5), (0, 0, (0, 0, 2, 1, 1, 2))),
    (("q", 2, 2, 3), (0, 0, (0, 0, 2, 2, 0, 0))),
    (("s", 0, 5, 2), (0, 0, (0, 1, 1, 1, 1, 2))),
    (("s", 0, 3, 2), (0, 0, (0, 1, 1, 2, 0, 0))),
    (("s", 0, 1, 2), (0, 0, (0, 2, 0, 0, 0, 0))),
    (("p", 0, 0, 2), (0, 0, (2, 0, 0, 0, 0, 0))),
    (("s", 1, 5, 2), (0, 1, (0, 1, 1, 1, 1, 2))),
    (("s", 1, 3, 2), (0, 1, (0, 1, 1, 2, 0, 0))),
    (("s", 1, 1, 2), (0, 1, (0, 2, 0, 0, 0, 0))),
    (("p", 0, 5, 2), (0, 1, (1, 1, 1, 1, 1, 2))),
    (("p", 0, 3, 2), (0, 1, (1, 1, 1, 2, 0, 0))),
    (("p", 0, 1, 2), (0, 1, (1, 2, 0, 0, 0, 0))),
    (("s", 2, 5, 2), (0, 2, (0, 1, 1, 1, 1, 2))),
    (("s", 2, 3, 2), (0, 2, (0, 1, 1, 2, 0, 0))),
    (("q", 2, 3, 5), (0, 2, (0, 1, 1, 2, 0, 2))),
    (("s", 2, 1, 2), (0, 2, (0, 2, 0, 0, 0, 0))),
    (("q", 2, 1, 5), (0, 2, (0, 2, 0, 0, 0, 2))),
    (("p", 1, 0, 2), (1, 0, (2, 0, 0, 0, 0, 0))),
    (("q", 2, 0, 4), (1, 0, (2, 0, 0, 0, 2, 1))),
    (("q", 2, 0, 2), (1, 0, (2, 0, 2, 1, 1, 1))),
    (("s", 0, 0, 2), (1, 0, (2, 1, 1, 1, 1, 1))),
    (("p", 1, 5, 2), (1, 1, (1, 1, 1, 1, 1, 2))),
    (("p", 1, 3, 2), (1, 1, (1, 1, 1, 2, 0, 0))),
    (("q", 2, 3, 4), (1, 1, (1, 1, 1, 2, 2, 1))),
    (("p", 1, 1, 2), (1, 1, (1, 2, 0, 0, 0, 0))),
    (("q", 2, 1, 4), (1, 1, (1, 2, 0, 0, 2, 1))),
    (("q", 2, 1, 2), (1, 1, (1, 2, 2, 1, 1, 1))),
    (("s", 1, 0, 2), (1, 1, (2, 1, 1, 1, 1, 1))),
    (("s", 2, 0, 2), (1, 2, (2, 1, 1, 1, 1, 1))),
    (("q", 2, 0, 3), (1, 2, (2, 1, 1, 2, 0, 1))),
    (("q", 2, 0, 1), (1, 2, (2, 2, 0, 0, 0, 1))),
    (("p", 2, 0, 2), (2, 0, (2, 0, 0, 0, 0, 0))),
    (("p", 2, 5, 2), (2, 1, (1, 1, 1, 1, 1, 2))),
    (("p", 2, 3, 2), (2, 1, (1, 1, 1, 2, 0, 0))),
    (("p", 2, 1, 2), (2, 1, (1, 2, 0, 0, 0, 0))),
)

A_SURVIVING_EDGES = ((0, 5), (1, 3), (2, 4))
A_LIVE_STAR_SITES = (2, 4)
A_TRADE_WORD = (2, 1, 1, 1, 1, 2)


# ==========================================================================
# PACKETS B and C: perturbed seven-row guards
# ==========================================================================
# Same shape as the audited seven-row guard: only colour-2 material, so every
# row vanishes identically on any word carrying a non-2 colour and the whole
# content sits at the word 2^6.  Both have exactly the audited guard's missing
# ledger (00,0^6,-1), (11,1^6,-1), rank-three stars and literal Segre
# responses.  What differs is the colour-2 internal quadratic.
#
#   audited guard   q_2 = 01+45       haf = 0, ONE  live four-set
#   packet B        q_2 = 01+23+45    haf = 1, THREE live four-sets
#   packet C        q_2 = 01+23+04+25 haf = 0, FOUR live four-sets
#
# Packet C is the controlled comparison: like the audited guard it has
# haf(q_2) = 0, the (2,2) cap is the only one failing the source relation with
# layers (0,1,0,0), and the terminal class sits on the cap (0,1) as a multiple
# of the free scalar d_01.  Only the number of live four-sets differs.
MISSING_TWO = ((0, 0), (1, 1))
SUPPLIED_SEVEN = tuple((i, j) for i in COLORS for j in COLORS
                       if (i, j) not in MISSING_TWO)


def star_dicts(pvec, svec):
    return ({(i, x, 2): Q(v) for i, vec in pvec.items()
             for x, v in enumerate(vec) if v},
            {(j, y, 2): Q(v) for j, vec in svec.items()
             for y, v in enumerate(vec) if v})


B_Q = {(0, 1, 2, 2): Q(1), (2, 3, 2, 2): Q(1), (4, 5, 2, 2): Q(1)}
B_PVEC = {0: (1, 0, 0, 0, 1, 0), 1: (0, 0, 1, 0, 0, 0), 2: (0, 1, 0, 0, 0, 1)}
B_SVEC = {0: (0, -1, 0, 0, 0, 1), 1: (-1, 0, 0, 0, -1, 0), 2: (0, 0, 0, 0, 1, 0)}
B_P, B_S = star_dicts(B_PVEC, B_SVEC)
B_GUARD_POINT = {("d", 2, 1): Q(2)}
B_FOURSETS = [(0, 1, 2, 3), (0, 1, 4, 5), (2, 3, 4, 5)]

C_Q = {(0, 1, 2, 2): Q(1), (2, 3, 2, 2): Q(1),
       (0, 4, 2, 2): Q(1), (2, 5, 2, 2): Q(1)}
C_PVEC = {0: (-1, 0, -1, -1, 0, -1), 1: (0, 0, 0, -1, 0, -1),
          2: (0, 1, 0, 0, 0, 0)}
C_SVEC = {0: (-1, 0, 0, 0, 0, 0), 1: (0, -1, 0, 0, 1, 0),
          2: (0, 0, 0, 0, 0, 1)}
C_P, C_S = star_dicts(C_PVEC, C_SVEC)
C_GUARD_POINT = {("d", 0, 1): Q(1)}
C_FOURSETS = [(0, 1, 2, 3), (0, 1, 2, 5), (0, 2, 3, 4), (0, 2, 4, 5)]


# ==========================================================================
# audits
# ==========================================================================
def audit_normalization():
    def plain(sites):
        total = Q(0)
        for matching in matchings(tuple(sites)):
            total += Q(1)
        return total

    require(plain(SITES) == 15, "all-ones six-site hafnian is not 15")
    require(plain((0, 1, 2, 3)) == 3, "all-ones four-site hafnian is not 3")
    require(plain((0, 1)) == 1, "all-ones two-site hafnian is not 1")


def audit_packet_a_baseline(system):
    ledger = sorted(
        (i, j, word, value)
        for (i, j, word), poly in system.items()
        for value in (poly.evaluate(A_GUARD_POINT),)
        if value
    )
    require(
        ledger == [(2, 2, (2,) * 6, Q(-1))],
        ("packet A does not reproduce the committed 8/9 ledger", ledger),
    )
    require(sorted(A_D) == [(0, 2)], "packet A direct block is not E_02")


def audit_packet_a_terminal_class():
    """chi is identically zero on the committed 8/9 guard, and the only caps
    failing the source relation are its two supplied anchors."""
    failures = []
    for colour in COLORS:
        for a, b in product(COLORS, repeat=2):
            alpha = A_D.get((a, b), Q(0))
            layers = cap_layers(A_Q, A_P, A_S, a, b, colour)
            chi = alpha * layers[2] + layers[3]
            require(chi == 0,
                    ("packet A acquired a terminal class", colour, a, b, chi))
            if alpha * layers[0] + layers[1]:
                failures.append((colour, a, b, layers))
    require(
        [(c, a, b) for c, a, b, _ in failures] == [(0, 0, 0), (1, 1, 1)],
        ("packet A source-relation failures changed",
         [(c, a, b) for c, a, b, _ in failures]),
    )
    for _, _, _, layers in failures:
        require(layers == (Q(0), Q(1), Q(0), Q(0)),
                ("a packet A anchor cap is not (0,1,0,0)", layers))


def audit_packet_a_collapse(system):
    zeros = set()
    for variable, (i, j, word) in A_FORCED:
        require((i, j) in A_SUPPLIED,
                ("a forcing used the missing anchor row", variable, i, j))
        reduced = system[(i, j, word)].kill(zeros)
        monomial = next(iter(reduced.terms)) if len(reduced.terms) == 1 else None
        require(
            monomial is not None and set(monomial) == {variable}
            and len(monomial) == 1,
            ("the forcing equation is not a single unknown", variable, i, j, word),
        )
        zeros.add(variable)
    require(len(zeros) == 36, ("packet A forced-zero count", len(zeros)))
    require(zeros == propagate(system, A_SUPPLIED),
            "the listed packet A forcings are not the closure of the eight rows")

    alive_edges = tuple(pair for pair in combinations(SITES, 2)
                        if ("q", 2, pair[0], pair[1]) not in zeros)
    require(alive_edges == A_SURVIVING_EDGES,
            ("packet A colour-2 support collapse changed", alive_edges))
    alive_p = sorted({x for i in COLORS for x in SITES
                      if ("p", i, x, 2) not in zeros})
    alive_s = sorted({y for j in COLORS for y in SITES
                      if ("s", j, y, 2) not in zeros})
    require(alive_p == list(A_LIVE_STAR_SITES) and alive_s == list(A_LIVE_STAR_SITES),
            ("packet A star collapse changed", alive_p, alive_s))
    require(all(("d", i, j) not in zeros for i in COLORS for j in COLORS),
            "packet A collapse unexpectedly killed a direct scalar")
    return zeros


def audit_packet_a_peel(system, zeros):
    """Row(2,2,2^6) = q_2(0,5) * q_2(1,3) * rho_2(2,2,{2,4})."""
    anchor = system[(2, 2, (2,) * 6)].kill(zeros)
    word = {site: 2 for site in SITES}
    ansatz = PACKET_A
    rho = ansatz.row(2, 2, word, sites=(2, 4)).kill(zeros)
    carrier = Poly.var(("q", 2, 0, 5)) * Poly.var(("q", 2, 1, 3))
    require(anchor == carrier * rho - Poly.const(1),
            "the packet A anchor peel identity failed")
    require(len(rho.terms) == 3, ("packet A rho term count", len(rho.terms)))
    loose = [m for m in anchor.terms
             if m and not {("q", 2, 0, 5), ("q", 2, 1, 3)} <= set(m)]
    require(not loose, ("a packet A anchor monomial avoids the carrier", loose))
    require(len(anchor.terms) == 4, ("packet A anchor term count", len(anchor.terms)))


def audit_packet_a_trade(system, zeros):
    """d_ij * q_2(0,5) = 0 for all eight supplied label pairs."""
    edge = Poly.var(("q", 2, 0, 5))
    for i, j in A_SUPPLIED:
        traded = system[(i, j, A_TRADE_WORD)].kill(zeros)
        require(traded == Poly.var(("d", i, j)) * edge,
                ("packet A trade equation changed", i, j, traded.terms))
    # the same word in the missing row supplies the ninth trade equation
    require(system[(2, 2, A_TRADE_WORD)].kill(zeros)
            == Poly.var(("d", 2, 2)) * edge,
            "the packet A ninth trade equation changed")


def audit_packet_a_conclusion(system, zeros):
    """A live anchor forces q_2(0,5) != 0, which kills the whole direct block
    and both live p-entries, leaving the anchor row equal to the constant -1."""
    killed = set(zeros)
    killed |= {("d", i, j) for i in COLORS for j in COLORS}
    killed |= {("p", i, x, 2) for i in COLORS for x in A_LIVE_STAR_SITES}
    anchor = system[(2, 2, (2,) * 6)].kill(killed)
    require(anchor == Poly.const(-1),
            ("the packet A anchor did not collapse to -1", anchor.terms))

    # the killers themselves are consequences of q_2(0,5) != 0
    for i, j in A_SUPPLIED:
        require(system[(i, j, A_TRADE_WORD)].kill(zeros).terms
                == {(("d", i, j), ("q", 2, 0, 5)): Q(1)},
                ("packet A direct-scalar killer changed", i, j))
    for i in COLORS:
        for x, spot in ((2, (i, 0, (2, 0, 2, 1, 1, 2))),
                        (4, (i, 0, (2, 0, 0, 0, 2, 2)))):
            reduced = system[spot].kill(zeros)
            require(reduced.terms == {(("p", i, x, 2), ("q", 2, 0, 5)): Q(1)},
                    ("packet A star killer changed", i, x, reduced.terms))

    # and the terminal class is already dead after the collapse: every
    # surviving colour-2 response sits on the single site pair {2,4}, so
    # R^[2] = R^[3] = 0 and chi = 0 for every cap.
    live_pairs = {tuple(sorted((x, y)))
                  for x in A_LIVE_STAR_SITES for y in A_LIVE_STAR_SITES if x != y}
    require(live_pairs == {(2, 4)},
            ("packet A surviving response support changed", live_pairs))


def audit_packet_a_infeasible(system):
    nodes, open_leaves = branch_search(system)
    require(not open_leaves,
            ("packet A branch search left open leaves", len(open_leaves)))
    require(nodes == 15, ("packet A branch node count changed", nodes))


def sub_hafnian(quadratic, sites):
    total = Q(0)
    for matching in matchings(tuple(sites)):
        term = Q(1)
        for x, y in matching:
            term *= quadratic.get((min(x, y), max(x, y), 2, 2), Q(0))
        total += term
    return total


def audit_perturbed_is_a_seven_row_guard(name, system, quadratic, pvec, svec,
                                         guard_point, foursets, live_caps_want):
    ledger = sorted(
        (i, j, word, value)
        for (i, j, word), poly in system.items()
        for value in (poly.evaluate(guard_point),)
        if value
    )
    require(
        ledger == [(0, 0, (0,) * 6, Q(-1)), (1, 1, (1,) * 6, Q(-1))],
        ("%s is not a seven-row guard with the audited ledger" % name, ledger),
    )

    live = [T for T in combinations(SITES, 4) if sub_hafnian(quadratic, T)]
    require(live == foursets, ("%s four-set support changed" % name, live))
    require(len(live) > 1,
            "%s is as degenerate as the audited guard" % name)

    for vectors in (pvec, svec):
        rows = [[Q(vectors[i][x]) for i in COLORS] for x in SITES]
        require(matrix_rank(rows) == 3, "%s star is not good" % name)

    pure = sub_hafnian(quadratic, SITES)
    stars = star_dicts(pvec, svec)
    # (a, b, Q_0, Q_1, Q_2, Q_3) for every label pair whose cap could carry a
    # terminal class.  Diagonal pairs are scanned too: a diagonal cap can have
    # Q_2 != 0 and be neutralized only through the source relation
    # alpha*Q_0 + Q_1 = 0, which pins alpha rather than killing the cap, so it
    # must be recorded rather than filtered away.
    live_caps = []
    for a, b in product(COLORS, repeat=2):
        layers = cap_layers(quadratic, stars[0], stars[1], a, b, 2)
        require(layers[0] == pure, ("%s pure hafnian changed" % name, a, b))
        # Scan every label pair, diagonal ones included: a diagonal cap can
        # carry Q_2 != 0 and be neutralized only by the source relation
        # alpha*Q_0 + Q_1 = 0, so that relation has to be checked, not assumed.
        if layers[2] or layers[3]:
            live_caps.append((a, b, layers[0], layers[1], layers[2], layers[3]))
    require(live_caps == live_caps_want,
            ("%s terminal-class table changed" % name, live_caps))


def matrix_rank(rows):
    a = [list(row) for row in rows]
    if not a:
        return 0
    height, width = len(a), len(a[0])
    pivot = 0
    for column in range(width):
        row = next((r for r in range(pivot, height) if a[r][column]), None)
        if row is None:
            continue
        a[pivot], a[row] = a[row], a[pivot]
        scale = a[pivot][column]
        a[pivot] = [entry / scale for entry in a[pivot]]
        for r in range(height):
            if r != pivot and a[r][column]:
                factor = a[r][column]
                a[r] = [e - factor * g for e, g in zip(a[r], a[pivot])]
        pivot += 1
    return pivot


def audit_perturbed_no_peel(name, system, zeros_count, anchor_counts,
                            traded_scalars, class_carrier, nodes_want,
                            pinned_direct=()):
    zeros = propagate(system, SUPPLIED_SEVEN)
    require(len(zeros) == zeros_count,
            ("%s forced-zero count changed" % name, len(zeros)))
    dead_d = sorted((i, j) for i in COLORS for j in COLORS
                    if ("d", i, j) in zeros)
    require(dead_d == list(pinned_direct),
            ("%s pinned direct block changed" % name, dead_d))

    # the anchor rows do NOT peel: no variable divides every monomial
    for colour, expected in anchor_counts:
        anchor = system[(colour, colour, (colour,) * 6)].kill(zeros)
        monomials = [m for m in anchor.terms if m]
        require(len(monomials) == expected,
                ("%s anchor monomial count changed" % name, colour,
                 len(monomials)))
        common = set(monomials[0])
        for m in monomials[1:]:
            common &= set(m)
        require(not common,
                ("%s anchor unexpectedly peeled" % name, colour,
                 sorted(map(str, common))))

    # which direct scalars are annihilated by a single-monomial equation?
    traded = set()
    for (i, j, word), poly in system.items():
        if (i, j) not in SUPPLIED_SEVEN:
            continue
        reduced = poly.kill(zeros)
        if len(reduced.terms) == 1:
            monomial = next(iter(reduced.terms))
            for v in monomial:
                if v[0] == "d":
                    traded.add((v[1], v[2]))
    require(sorted(traded) == list(traded_scalars),
            ("%s traded direct scalars changed" % name, sorted(traded)))
    require(class_carrier not in traded,
            ("%s traded away its class carrier" % name, class_carrier))

    nodes, open_leaves = branch_search(system)
    require(not open_leaves,
            ("%s branch search left open leaves" % name, len(open_leaves)))
    require(nodes == nodes_want, ("%s branch node count changed" % name, nodes))


PACKET_A = Ansatz(A_Q, A_P, A_S, free_colours=(2,))
PACKET_B = Ansatz(B_Q, B_P, B_S, free_colours=(0, 1))
PACKET_C = Ansatz(C_Q, C_P, C_S, free_colours=(0, 1))


def main():
    audit_normalization()

    system_a = PACKET_A.system()
    audit_packet_a_baseline(system_a)
    audit_packet_a_terminal_class()
    zeros_a = audit_packet_a_collapse(system_a)
    audit_packet_a_peel(system_a, zeros_a)
    audit_packet_a_trade(system_a, zeros_a)
    audit_packet_a_conclusion(system_a, zeros_a)
    audit_packet_a_infeasible(system_a)

    # Packet B: haf(q_2) = 1, three live four-sets.  The pure word pins the
    # direct block, so chi = 2*d_21 = 4 is forced.  No peel, and no direct
    # scalar is traded at all.
    system_b = PACKET_B.system()
    audit_perturbed_is_a_seven_row_guard(
        "packet B", system_b, B_Q, B_PVEC, B_SVEC, B_GUARD_POINT, B_FOURSETS,
        [(0, 0, Q(1), Q(0), Q(-2), Q(0)),
         (2, 1, Q(1), Q(-2), Q(2), Q(0))])
    require(system_b[(2, 1, (2,) * 6)] == Poly.var(("d", 2, 1)) - Poly.const(2),
            "packet B does not pin its class carrier at the pure word")
    audit_perturbed_no_peel(
        "packet B", system_b, 44, ((0, 20), (1, 9)), [], (2, 1), 18,
        pinned_direct=[(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)])

    # Packet C: the controlled comparison.  haf(q_2) = 0 and the cap profile is
    # the audited guard's -- only (2,2) fails the source relation with layers
    # (0,1,0,0), and the class sits on (0,1) as a multiple of the free d_01.
    # Only the number of live four-sets differs (four instead of one).  Trade
    # equations do appear here, but they miss the class carrier d_01.
    system_c = PACKET_C.system()
    audit_perturbed_is_a_seven_row_guard(
        "packet C", system_c, C_Q, C_PVEC, C_SVEC, C_GUARD_POINT, C_FOURSETS,
        [(0, 1, Q(0), Q(0), Q(-4), Q(0))])
    require(system_c[(2, 2, (2,) * 6)] == Poly.const(0),
            "packet C anchor cap layer profile changed")
    audit_perturbed_no_peel(
        "packet C", system_c, 40, ((0, 8), (1, 8)),
        [(1, 0), (2, 0), (2, 1)], (0, 1), 85)

    print(
        "PASS: (A) the committed complementary all-word 8/9 guard (X_0,X_1 "
        "supplied, X_2 missing) has chi=0 on every cap and every pure colour; "
        "freeing its colour-2 sector, its eight supplied rows force 36 zeros, "
        "collapsing the colour-2 support to the matching {05,13,24} and both "
        "stars to the sites {2,4}; the missing anchor peels, "
        "Row(2,2,2^6)=q_2(0,5)*q_2(1,3)*rho_2(2,2,{2,4}); the trade equations "
        "d_ij*q_2(0,5)=0 hold for all nine label pairs, so a live anchor kills "
        "the whole direct block and makes the anchor row the constant -1; "
        "infeasible over 15 branch nodes.  (B) a perturbed seven-row guard with "
        "the audited ledger, chi=4 and q_2=01+23+45 (haf 1, three live "
        "four-sets) collapses (44 zeros) with NO peel and NO trade; infeasible "
        "over 18 nodes.  (C) the controlled comparison, same ledger, same cap "
        "profile, chi=-4*d_01 free, q_2=01+23+04+25 (haf 0, four live "
        "four-sets), collapses (40 zeros) with NO peel; trade equations do "
        "appear but annihilate only d_10,d_20,d_21 and never the class carrier "
        "d_01; infeasible over 85 nodes.  Hence the collapse is general, while "
        "the peel and the class-killing trade are lost on B and C; they are "
        "governed by the geometry of the collapsed support, not by the number "
        "of live four-sets"
    )


if __name__ == "__main__":
    main()
