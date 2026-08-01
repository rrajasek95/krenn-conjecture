#!/usr/bin/env python3
"""The colour-0 anchor can be restored at its pure word: an explicit witness.

Setting (the star-sector repair ansatz of
``verify_h3_star_sector_anchor_terminal_trade.py``): freeze the whole colour-2
slice of the audited seven-row guard -- q_2 = 01+45 and both endpoint stars --
and free the nine direct scalars, every colour-0/colour-1 star entry and the
two monochromatic colour-0/colour-1 internal quadratics (111 unknowns).  Call
the six off-diagonal rows together with the complete 22 row, imposed on all
729 residual words, **the seven rows**.

That note settles the *nine*-row question (infeasible) and records the trade
    Row(c,c,c^6) = q_c(2,3) * rho_c(c,c, W\\{2,3}),
    d_01 q_c(2,3) = d_02 q_c(2,3) = 0.
It leaves open whether the seven rows can be completed so that the colour-0
anchor is live *at its pure word alone*.  They can.  This checker exhibits and
audits a witness, and proves that the colour-1 mirror is impossible.

Outcome:

  W1  an explicit exact rational eight-vertex decorated block array -- the
      audited guard plus five entries -- whose matching tensor gets **all
      7 x 729 seven-row coefficients right on every word** and has
      Row(0,0,0^6) = 1.  So "seven rows + Row(0,0,0^6)=1" is FEASIBLE, and the
      conditional reading of the trade ("restoring the anchor forces chi = 0")
      is not vacuous: it has a model.
  W2  its complete GHZ failure ledger is two entries,
      (00, (2,0,0,0,0,0), +1) and (11, 1^6, -1);
      so the colour-0 anchor row is right on 728 of its 729 words, and the
      committed note's "seven + complete 00 row is infeasible" says 728 is the
      most that is available.  The one spurious coefficient IS the anchor's
      carrier: both equal q_0(2,3) * (q_0(1,5) s_0(4,0) + q_0(1,4) s_0(5,0)).
  W3  the witness keeps rank-three endpoint stars, every literal Segre
      rectangle, and a rank-one direct block -- but d_01 = d_02 = 0, so every
      admissible cap has terminal class chi = 0, exactly as the trade predicts.
  W4  the reference branch search on the same system -- propagate every
      single-variable monomial equation, then split each surviving
      single-monomial equation into its factors -- reproduces its 383 open
      leaves, and **all 383 are decided here**: 373 are feasible (one of four
      explicit rational solutions satisfies each), and the other 10 close on
      one exact identity,
          (that leaf's anchor equation) + 1 = p_0(4,0) * (another of its
          equations),
      which forces 1 = 0.  Open leaves were never evidence of feasibility; a
      witness is.
  W5  the colour-1 pure-word anchor is IMPOSSIBLE, by an ideal-membership
      certificate: modulo the 32 zeros the seven rows force,
        Row(1,1,1^6) = d_11 q_1(2,3) E3 + p_1(0,1) E4 + p_1(1,1) E5
                       + A' E6 + C' E7
      with E3..E7 five specific seven-row equations.  Hence Row(1,1,1^6)
      vanishes identically on the seven-row variety.  The same combination is
      verified NOT to exist for colour 0, which is the exact source of the
      asymmetry: for colour 1 the four needed words sit in the 01 row, which is
      supplied; for colour 0 they sit in the 00 row, which is not.

Nothing here is a counterexample to anything: the packet satisfies eight of the
nine GHZ rows minus one coefficient, and misses the colour-1 target entirely.
No certified dependency changes; Krenn's conjecture remains open.

Python standard library only, exact ``Fraction`` arithmetic, live under
``python3 -O`` and ``python3 -I -S``, deterministic across PYTHONHASHSEED.
"""

from fractions import Fraction
from itertools import combinations, permutations, product


Q = Fraction
SITES = tuple(range(6))
LEFT = 6
RIGHT = 7
VERTICES = tuple(range(8))
COLORS = (0, 1, 2)
PURE = 2
SEVEN = ((0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2))
ANCHOR_ROWS = ((0, 0), (1, 1))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


# ==========================================================================
# 0.  perfect matchings, built by canonicalising permutations
# ==========================================================================
_MATCHING_CACHE = {}


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    cached = _MATCHING_CACHE.get(vertices)
    if cached is not None:
        return cached
    require(len(vertices) % 2 == 0, ("odd vertex set", vertices))
    found = set()
    for order in permutations(vertices):
        found.add(tuple(sorted(
            (min(order[k], order[k + 1]), max(order[k], order[k + 1]))
            for k in range(0, len(order), 2))))
    answer = tuple(sorted(found))
    _MATCHING_CACHE[vertices] = answer
    return answer


M8 = perfect_matchings(VERTICES)
M6 = perfect_matchings(SITES)
M4 = {pair: perfect_matchings(tuple(s for s in SITES if s not in pair))
      for pair in combinations(SITES, 2)}
require(len(M8) == 105, ("eight-vertex matching count", len(M8)))
require(len(M6) == 15, ("six-vertex matching count", len(M6)))
require(all(len(v) == 3 for v in M4.values()), "four-vertex matching count")


def audit_normalization():
    """all-ones hafnians: 15 on six sites, 3 on four, 1 on two."""
    def ones(vertices):
        return sum(1 for _ in perfect_matchings(vertices))
    require(ones(SITES) == 15, "all-ones six-site hafnian is not 15")
    require(ones((0, 1, 2, 3)) == 3, "all-ones four-site hafnian is not 3")
    require(ones((0, 1)) == 1, "all-ones two-site hafnian is not 1")


# ==========================================================================
# 1.  the packet: one explicit eight-vertex decorated block array
# ==========================================================================
BLOCK = {}


def put(u, v, cu, cv, value):
    if u > v:
        u, v, cu, cv = v, u, cv, cu
    key = (u, v, cu, cv)
    require(key not in BLOCK, ("duplicate block entry", key))
    BLOCK[key] = Q(value)


# --- frozen colour-2 slice, copied from the audited seven-row guard checker
FROZEN = (
    (0, 1, 2, 2, 1),                 # q_2 = z0 z1 + z4 z5
    (4, 5, 2, 2, 1),
    (LEFT, 0, 0, 2, 1),              # p_0 = z0 + z1
    (LEFT, 1, 0, 2, 1),
    (LEFT, 4, 1, 2, 1),              # p_1 = z4
    (LEFT, 2, 2, 2, 1),              # p_2 = z2 + z3
    (LEFT, 3, 2, 2, 1),
    (RIGHT, 5, 0, 2, 1),             # s_0 = z5
    (RIGHT, 2, 1, 2, 1),             # s_1 = z2 - z3
    (RIGHT, 3, 1, 2, -1),
    (RIGHT, 2, 2, 2, Q(1, 2)),       # s_2 = (z2 + z3)/2
    (RIGHT, 3, 2, 2, Q(1, 2)),
)
# --- the repair: four colour-0 decorations and one direct scalar
REPAIR = (
    (1, 5, 0, 0, 1),                 # q_0 = z1 z5 + z2 z3
    (2, 3, 0, 0, 1),
    (LEFT, 0, 0, 0, 1),              # p_0 gains z0 in colour 0
    (RIGHT, 4, 0, 0, 1),             # s_0 gains z4 in colour 0
    (LEFT, RIGHT, 1, 0, -1),         # d_10 = -1   (the guard had d_01 = +1)
)
for entry in FROZEN + REPAIR:
    put(*entry)


def weight(u, v, cu, cv):
    if u > v:
        u, v, cu, cv = v, u, cv, cu
    return BLOCK.get((u, v, cu, cv), Q(0))


def normal_key(u, v, cu, cv):
    if u > v:
        u, v, cu, cv = v, u, cv, cu
    return (u, v, cu, cv)


def audit_packet_shape():
    """the colour-2 slice is the guard's, verbatim, and nothing else is frozen"""
    require(len(BLOCK) == len(FROZEN) + len(REPAIR),
            ("block count changed", len(BLOCK)))
    require(set(BLOCK) == {normal_key(*entry[:4]) for entry in FROZEN + REPAIR},
            "the block key set changed")
    # the colour-2 slice: internal edges whose two site colours are both 2,
    # together with the endpoint-star entries whose *site* colour is 2.
    slice_two = {}
    for (u, v, cu, cv), value in BLOCK.items():
        if v <= 5:
            if cu == PURE and cv == PURE:
                slice_two[(u, v, cu, cv)] = value
        elif u <= 5:
            if cu == PURE:
                slice_two[(u, v, cu, cv)] = value
    require(slice_two == {normal_key(*e[:4]): Q(e[4]) for e in FROZEN},
            ("the frozen colour-2 slice changed", sorted(slice_two)))
    require(all(e[0] != LEFT or e[1] != RIGHT for e in FROZEN),
            "a direct scalar leaked into the frozen slice")
    require(sum(1 for i, j in product(COLORS, repeat=2)
                if weight(LEFT, RIGHT, i, j)) == 1,
            "the direct block is not a single matrix unit")
    require(weight(LEFT, RIGHT, 1, 0) == -1, "the direct scalar changed")
    require(weight(LEFT, RIGHT, 0, 1) == 0,
            "d_01 is nonzero: the trade forbids it once the anchor is live")


# ==========================================================================
# 2.  the matching tensor, straight from the definition
# ==========================================================================
def matching_tensor(i, j, word):
    """haf of the eight-vertex decorated array, LEFT coloured i, RIGHT j."""
    colour = {x: word[x] for x in SITES}
    colour[LEFT] = i
    colour[RIGHT] = j
    total = Q(0)
    for matching in M8:
        term = Q(1)
        for u, v in matching:
            term *= weight(u, v, colour[u], colour[v])
            if not term:
                break
        total += term
    return total


def residual_hafnian(word, vertices):
    total = Q(0)
    for matching in perfect_matchings(vertices):
        term = Q(1)
        for x, y in matching:
            term *= weight(x, y, word[x], word[y])
            if not term:
                break
        total += term
    return total


def chart_row(i, j, word):
    """the deleted-pair chart formula, an independent second computation"""
    total = weight(LEFT, RIGHT, i, j) * residual_hafnian(word, SITES)
    for x, y in combinations(SITES, 2):
        response = (weight(LEFT, x, i, word[x]) * weight(RIGHT, y, j, word[y])
                    + weight(LEFT, y, i, word[y]) * weight(RIGHT, x, j, word[x]))
        if not response:
            continue
        complement = tuple(s for s in SITES if s not in (x, y))
        total += response * residual_hafnian(word, complement)
    return total


def ghz_target(i, j, word):
    return Q(1) if (i == j and all(c == i for c in word)) else Q(0)


def audit_all_coefficients():
    ledger = []
    seven_checked = 0
    for word in product(COLORS, repeat=6):
        for i, j in product(COLORS, repeat=2):
            value = matching_tensor(i, j, word)
            require(value == chart_row(i, j, word),
                    ("the two computations disagree", i, j, word))
            if (i, j) in SEVEN:
                require(value == ghz_target(i, j, word),
                        ("SEVEN-ROW FAILURE", i, j, word, value))
                seven_checked += 1
            residual = value - ghz_target(i, j, word)
            if residual:
                ledger.append((i, j, word, residual))
    require(seven_checked == 7 * 729,
            ("wrong seven-row coefficient count", seven_checked))
    require(matching_tensor(0, 0, (0,) * 6) == 1,
            "the colour-0 anchor is not live at its pure word")
    require(sorted(ledger) == [
        (0, 0, (2, 0, 0, 0, 0, 0), Q(1)),
        (1, 1, (1,) * 6, Q(-1)),
    ], ("the GHZ failure ledger changed", sorted(ledger)))
    # the 00 row is right on 728 of its 729 words
    wrong = [w for w in product(COLORS, repeat=6)
             if matching_tensor(0, 0, w) != ghz_target(0, 0, w)]
    require(wrong == [(2, 0, 0, 0, 0, 0)], ("00-row leak set changed", wrong))
    # the single leak IS the anchor's carrier
    carrier = (weight(2, 3, 0, 0)
               * (weight(1, 5, 0, 0) * weight(RIGHT, 4, 0, 0)
                  + weight(1, 4, 0, 0) * weight(RIGHT, 5, 0, 0)))
    require(matching_tensor(0, 0, (2, 0, 0, 0, 0, 0)) == carrier,
            "the leak is not the anchor carrier")
    require(matching_tensor(0, 0, (0,) * 6)
            == weight(LEFT, 0, 0, 0) * carrier,
            "the anchor is not p_0(0,0) times the leak")


# ==========================================================================
# 3.  stars, Segre rectangles, terminal class
# ==========================================================================
def rank(rows):
    work = [[Q(x) for x in row] for row in rows]
    if not work:
        return 0
    pivot = 0
    for column in range(len(work[0])):
        chosen = next((r for r in range(pivot, len(work)) if work[r][column]),
                      None)
        if chosen is None:
            continue
        work[pivot], work[chosen] = work[chosen], work[pivot]
        scale = work[pivot][column]
        work[pivot] = [x / scale for x in work[pivot]]
        for r in range(len(work)):
            if r != pivot and work[r][column]:
                factor = work[r][column]
                work[r] = [a - factor * b for a, b in zip(work[r], work[pivot])]
        pivot += 1
    return pivot


def audit_stars_and_segre():
    p_rows = [[weight(LEFT, x, label, c) for label in COLORS]
              for x in SITES for c in COLORS]
    s_rows = [[weight(RIGHT, y, label, c) for label in COLORS]
              for y in SITES for c in COLORS]
    require(rank(p_rows) == 3, "first endpoint star lost rank three")
    require(rank(s_rows) == 3, "second endpoint star lost rank three")

    def response_polynomial(i, j):
        answer = {}
        for x, y in combinations(SITES, 2):
            for cx, cy in product(COLORS, repeat=2):
                value = (weight(LEFT, x, i, cx) * weight(RIGHT, y, j, cy)
                         + weight(LEFT, y, i, cy) * weight(RIGHT, x, j, cx))
                if value:
                    answer[((x, cx), (y, cy))] = value
        return answer

    def product_polynomial(left, right):
        answer = {}
        for lm, lv in left.items():
            sites = {site for site, _ in lm}
            for rm, rv in right.items():
                if sites.intersection(site for site, _ in rm):
                    continue
                key = tuple(sorted(lm + rm))
                answer[key] = answer.get(key, Q(0)) + lv * rv
        return {k: v for k, v in answer.items() if v}

    responses = {(i, j): response_polynomial(i, j)
                 for i, j in product(COLORS, repeat=2)}
    checked = 0
    for i, k, j, ell in product(COLORS, repeat=4):
        require(product_polynomial(responses[i, j], responses[k, ell])
                == product_polynomial(responses[i, ell], responses[k, j]),
                ("literal Segre rectangle failed", i, k, j, ell))
        checked += 1
    require(checked == 81, ("Segre rectangle count", checked))


def cap_layers(colour, a, b):
    """(Q_0,..,Q_3) with Q_k = R^[k] q^[3-k] on the pure colour-`colour` word."""
    internal = [[Q(0) if x == y else weight(x, y, colour, colour) for y in SITES]
                for x in SITES]
    u = [weight(LEFT, x, a, colour) for x in SITES]
    v = [weight(RIGHT, y, b, colour) for y in SITES]
    response = [[Q(0) if x == y else u[x] * v[y] + v[x] * u[y] for y in SITES]
                for x in SITES]
    layers = []
    for used in range(4):
        value = Q(0)
        for matching in M6:
            for flags in product((0, 1), repeat=3):
                if sum(flags) != used:
                    continue
                term = Q(1)
                for flag, (x, y) in zip(flags, matching):
                    term *= response[x][y] if flag else internal[x][y]
                value += term
        layers.append(value)
    return tuple(layers)


def audit_terminal_class():
    """every admissible selected cap of the witness has chi = 0"""
    live = []
    table = {}
    for colour in COLORS:
        for a, b in product(COLORS, repeat=2):
            alpha = weight(LEFT, RIGHT, a, b)
            q0, q1, q2, q3 = cap_layers(colour, a, b)
            source = alpha * q0 + q1
            chi = alpha * q2 + q3
            table[(colour, a, b)] = (alpha, (q0, q1, q2, q3), source, chi)
            if source == 0 and chi:
                live.append((colour, a, b, chi))
    require(not live, ("a cap kept a nonzero terminal class", live))
    # the frozen-slice numbers of the audited trade note survive verbatim
    require(cap_layers(2, 0, 1)[2] == -2,
            "the (0,1) colour-2 cap no longer has Q_2 = -2")
    require(cap_layers(2, 0, 2)[2] == Q(1, 2),
            "the (0,2) colour-2 cap no longer has Q_2 = 1/2")
    require(table[(2, 0, 1)][0] == 0 and table[(2, 0, 2)][0] == 0,
            "d_01 or d_02 is nonzero, contradicting the trade")
    # the two live anchors fail the source relation, as diagonal caps must
    for colour, a, b in ((2, 2, 2), (0, 0, 0)):
        alpha = weight(LEFT, RIGHT, a, b)
        q0, q1, _, _ = cap_layers(colour, a, b)
        require(alpha * q0 + q1 != 0,
                ("a diagonal anchor cap became an admissible selected row",
                 colour, a, b))
    return table


# ==========================================================================
# 4.  symbolic sector: the seven rows over the 111 repair unknowns
# ==========================================================================
class Poly:
    __slots__ = ("terms",)

    def __init__(self, terms=None):
        self.terms = {m: c for m, c in (terms or {}).items() if c}

    @staticmethod
    def const(value):
        value = Q(value)
        return Poly({(): value}) if value else Poly()

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

    def substitute(self, values):
        out = {}
        for m, c in self.terms.items():
            coefficient = c
            rest = []
            for v in m:
                if v in values:
                    coefficient *= values[v]
                    if not coefficient:
                        break
                else:
                    rest.append(v)
            if not coefficient:
                continue
            key = tuple(sorted(rest))
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


def qvar(c, x, y):
    return "q%d_%d%d" % (c, min(x, y), max(x, y))


def pvar(i, x, c):
    return "p%d_%d_%d" % (i, x, c)


def svar(j, y, c):
    return "s%d_%d_%d" % (j, y, c)


def dvar(i, j):
    return "d%d%d" % (i, j)


FROZEN_Q2 = {(0, 1): Q(1), (4, 5): Q(1)}
FROZEN_P2 = {(0, 0): Q(1), (0, 1): Q(1), (1, 4): Q(1),
             (2, 2): Q(1), (2, 3): Q(1)}
FROZEN_S2 = {(0, 5): Q(1), (1, 2): Q(1), (1, 3): Q(-1),
             (2, 2): Q(1, 2), (2, 3): Q(1, 2)}


def sym_edge(x, y, cx, cy):
    if x > y:
        x, y, cx, cy = y, x, cy, cx
    if cx == PURE and cy == PURE:
        return Poly.const(FROZEN_Q2.get((x, y), 0))
    if cx != cy:
        return Poly()
    return Poly.var(qvar(cx, x, y))


def sym_p(i, x, c):
    return Poly.const(FROZEN_P2.get((i, x), 0)) if c == PURE \
        else Poly.var(pvar(i, x, c))


def sym_s(j, y, c):
    return Poly.const(FROZEN_S2.get((j, y), 0)) if c == PURE \
        else Poly.var(svar(j, y, c))


def sym_hafnian(vertices, word):
    total = Poly()
    for matching in perfect_matchings(vertices):
        term = Poly.const(1)
        for x, y in matching:
            term = term * sym_edge(x, y, word[x], word[y])
            if not term:
                break
        total = total + term
    return total


def sym_row(i, j, word, vertices=SITES):
    vertices = tuple(vertices)
    total = Poly.var(dvar(i, j)) * sym_hafnian(vertices, word)
    for x, y in combinations(vertices, 2):
        response = (sym_p(i, x, word[x]) * sym_s(j, y, word[y])
                    + sym_p(i, y, word[y]) * sym_s(j, x, word[x]))
        if not response:
            continue
        complement = tuple(v for v in vertices if v not in (x, y))
        piece = sym_hafnian(complement, word)
        if piece:
            total = total + response * piece
    return total


def build_symbolic_system():
    out = {}
    for word in product(COLORS, repeat=6):
        for i, j in product(COLORS, repeat=2):
            out[(i, j, word)] = sym_row(i, j, word)
    return out


def audit_symbolic_model(system):
    """the symbolic model reproduces the committed guard ledger and the witness"""
    guard = {dvar(0, 1): Q(1)}
    ledger = sorted((i, j, word, value)
                    for (i, j, word), poly in system.items()
                    for value in (poly.evaluate(guard) - ghz_target(i, j, word),)
                    if value)
    require(ledger == [(0, 0, (0,) * 6, Q(-1)), (1, 1, (1,) * 6, Q(-1))],
            ("the symbolic model misses the committed guard ledger", ledger))

    witness = {dvar(1, 0): Q(-1), qvar(0, 1, 5): Q(1), qvar(0, 2, 3): Q(1),
               pvar(0, 0, 0): Q(1), svar(0, 4, 0): Q(1)}
    for (i, j, word), poly in system.items():
        require(poly.evaluate(witness) == matching_tensor(i, j, word),
                ("the symbolic model disagrees with the packet", i, j, word))


def audit_forced_zeros(system):
    """the seven rows alone force 32 unknowns to zero, each in degree one"""
    seven = [(k, p) for k, p in system.items()
             if (k[0], k[1]) in SEVEN
             for p in (p - Poly.const(ghz_target(*k)),)]
    zeros = set()
    while True:
        fresh = set()
        for key, poly in seven:
            reduced = poly.kill(zeros)
            if len(reduced.terms) != 1:
                continue
            monomial = next(iter(reduced.terms))
            require(monomial, ("premature contradiction", key))
            if len(set(monomial)) == 1:
                require(len(monomial) == 1,
                        ("a forcing is not linear", key, monomial))
                fresh.add(monomial[0])
        if not fresh - zeros:
            break
        zeros |= fresh
    require(len(zeros) == 32, ("forced zero count", len(zeros), sorted(zeros)))
    for colour in (0, 1):
        alive = tuple(pair for pair in combinations(SITES, 2)
                      if qvar(colour, *pair) not in zeros)
        require(alive == ((0, 4), (0, 5), (1, 4), (1, 5), (2, 3)),
                ("colour-%d support collapse changed" % colour, alive))
    return zeros


def audit_peel(system, zeros):
    for colour in (0, 1):
        pure = (colour,) * 6
        anchor = system[(colour, colour, pure)].kill(zeros)
        word = {x: colour for x in SITES}
        rho = sym_row(colour, colour, word, vertices=(0, 1, 4, 5)).kill(zeros)
        require(anchor == Poly.var(qvar(colour, 2, 3)) * rho,
                ("the anchor peel identity failed", colour))


def audit_colour_one_certificate(system, zeros):
    """Row(1,1,1^6) lies in the ideal generated by the seven rows.

    Modulo the 32 forced zeros -- each of which is itself a degree-one seven-row
    equation, hence in that ideal -- the bare anchor polynomial is an explicit
    combination of five seven-row equations.  So it vanishes at every common
    zero of the seven rows and can never equal the target 1.
    """
    outcome = {}
    for colour in (0, 1):
        anchor = system[(colour, colour, (colour,) * 6)].kill(zeros)
        words = {
            "E3": tuple(PURE if x in (2, 3) else colour for x in SITES),
            "E4": tuple(PURE if x == 0 else colour for x in SITES),
            "E5": tuple(PURE if x == 1 else colour for x in SITES),
            "E6": tuple(PURE if x in (1, 4, 5) else colour for x in SITES),
            "E7": tuple(PURE if x in (0, 4, 5) else colour for x in SITES),
        }
        rows = {"E3": (2, 2), "E4": (0, 1), "E5": (0, 1),
                "E6": (0, 1), "E7": (0, 1)}
        pieces = {}
        for name, word in words.items():
            i, j = rows[name]
            require((i, j) in SEVEN, ("certificate used a non-supplied row", name))
            require(ghz_target(i, j, word) == 0, ("certificate word has a target",
                                                  name))
            pieces[name] = system[(i, j, word)].kill(zeros)
        require(pieces["E3"] == (Poly.var(qvar(colour, 0, 4))
                                 * Poly.var(qvar(colour, 1, 5))
                                 + Poly.var(qvar(colour, 0, 5))
                                 * Poly.var(qvar(colour, 1, 4))),
                ("E3 is not the four-site permanent", colour))
        a_p = (Poly.var(qvar(colour, 1, 5)) * Poly.var(pvar(colour, 4, colour))
               + Poly.var(qvar(colour, 1, 4)) * Poly.var(pvar(colour, 5, colour)))
        c_p = (Poly.var(qvar(colour, 0, 5)) * Poly.var(pvar(colour, 4, colour))
               + Poly.var(qvar(colour, 0, 4)) * Poly.var(pvar(colour, 5, colour)))
        combination = (
            Poly.var(dvar(colour, colour)) * Poly.var(qvar(colour, 2, 3))
            * pieces["E3"]
            + Poly.var(pvar(colour, 0, colour)) * pieces["E4"]
            + Poly.var(pvar(colour, 1, colour)) * pieces["E5"]
            + a_p * pieces["E6"]
            + c_p * pieces["E7"])
        outcome[colour] = (anchor == combination)
    require(outcome[1], "the colour-1 certificate failed")
    require(not outcome[0],
            "the colour-0 certificate unexpectedly closed -- the witness "
            "above would then contradict it")
    return outcome


def audit_asymmetry(system, zeros):
    """the four certificate words sit in the 01 row for colour 1 and in the
    00 row for colour 0 -- that is the whole of the asymmetry."""
    for colour in (0, 1):
        for site in (0, 1):
            # p_0 carries frozen colour-2 weight 1 at sites 0 and 1; the word
            # with colour 2 at exactly that site therefore reads off one
            # component of q_c|_{{0,1}x{4,5}} applied to s_label|_{{4,5}}.
            word = tuple(PURE if x == site else colour for x in SITES)
            partner = 1 - site
            edge = Poly.var(qvar(colour, 2, 3))
            for label in (0, 1):
                expected = edge * (
                    Poly.var(qvar(colour, partner, 5))
                    * Poly.var(svar(label, 4, colour))
                    + Poly.var(qvar(colour, partner, 4))
                    * Poly.var(svar(label, 5, colour)))
                got = system[(0, label, word)].kill(zeros)
                require(got == expected,
                        ("the one-colour-2-site row changed", colour, site, label))
    # the 01 row is supplied on every word; the 00 row is not supplied at all
    require((0, 1) in SEVEN and (0, 0) not in SEVEN, "row bookkeeping changed")


def audit_trade(system, zeros):
    """the five trade equations, from the seven rows at the witness word"""
    for colour in (0, 1):
        word = tuple(colour if x in (2, 3) else PURE for x in SITES)
        edge = Poly.var(qvar(colour, 2, 3))
        for (i, j), factor in (
                ((0, 1), Poly.var(dvar(0, 1))),
                ((0, 2), Poly.var(dvar(0, 2))),
                ((1, 2), Poly.var(dvar(1, 2))),
                ((2, 0), Poly.var(dvar(2, 0))),
                ((1, 0), Poly.var(dvar(1, 0)) + Poly.const(1))):
            require(system[(i, j, word)].kill(zeros) == factor * edge,
                    ("trade equation changed", colour, i, j))


TRADE = {dvar(0, 1): Q(0), dvar(0, 2): Q(0), dvar(1, 2): Q(0),
         dvar(2, 0): Q(0), dvar(1, 0): Q(-1)}


def branch_search(equations):
    """Exhaustive search: propagate every c*v^k = 0 to v = 0, then split each
    surviving single-monomial equation into its distinct factors.  Both steps
    are valid over a field, so the enumeration of leaves is exhaustive: every
    solution of `equations` satisfies some leaf's system."""
    seen = set()
    stack = [frozenset()]
    leaves = []
    while stack:
        start = stack.pop()
        if start in seen:
            continue
        seen.add(start)
        current = set(start)
        closed = False
        live = []
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
        if current != set(start):
            key = frozenset(current)
            if key in seen:
                continue
            seen.add(key)
        branch = None
        for reduced in live:
            if len(reduced.terms) == 1:
                factors = tuple(sorted(set(next(iter(reduced.terms)))))
                if branch is None or len(factors) < len(branch):
                    branch = factors
        if branch is None:
            leaves.append((frozenset(current), tuple(live)))
            continue
        for factor in branch:
            stack.append(frozenset(current | {factor}))
    return leaves


def audit_leaf_decision(system, zeros):
    """decide every open leaf of the reference branch search.

    The searched system is the seven rows on all 729 words together with
    Row(0,0,0^6) - 1, reduced by the 32 zeros the seven rows force and by the
    trade substitution TRADE.  That substitution is legitimate: the peel makes
    the anchor equation force q_0(2,3) != 0, and `audit_trade` shows the seven
    rows then read d_01 = d_02 = d_12 = d_20 = 0 and d_10 = -1.  So the reduced
    system has exactly the solutions of the original one.
    """
    keys = [(i, j, word) for word in product(COLORS, repeat=6)
            for i, j in product(COLORS, repeat=2) if (i, j) in SEVEN]
    keys.append((0, 0, (0,) * 6))
    equations = []
    for i, j, word in keys:
        reduced = (system[(i, j, word)] - Poly.const(ghz_target(i, j, word))) \
            .kill(zeros).substitute(TRADE)
        if reduced:
            equations.append(reduced)
    leaves = branch_search(equations)
    require(len(leaves) == 383, ("open-leaf count changed", len(leaves)))

    # four explicit rational solutions of the whole target system
    solutions = []
    for edge, p_site, s_site in (((1, 5), 0, 4), ((0, 5), 1, 4),
                                 ((1, 4), 5, 0), ((0, 4), 5, 1)):
        point = {dvar(1, 0): Q(-1), qvar(0, *edge): Q(1), qvar(0, 2, 3): Q(1),
                 pvar(0, p_site, 0): Q(1), svar(0, s_site, 0): Q(1)}
        for (i, j, word), poly in system.items():
            value = poly.evaluate(point)
            if (i, j) in SEVEN:
                require(value == ghz_target(i, j, word),
                        ("a carrier fails a seven row", edge, i, j, word))
        require(system[(0, 0, (0,) * 6)].evaluate(point) == 1,
                ("a carrier does not restore the anchor", edge))
        solutions.append(point)

    feasible = 0
    infeasible = []
    for index, (leaf_zeros, live) in enumerate(sorted(leaves,
                                                      key=lambda t: sorted(t[0]))):
        hit = False
        for point in solutions:
            if any(point.get(v) for v in leaf_zeros):
                continue
            if all(not poly.evaluate(point) for poly in live):
                hit = True
                break
        if hit:
            feasible += 1
            continue
        # every remaining leaf closes on one exact identity:
        #     (anchor equation) + 1 == p_0(4,0) * (another live equation),
        # so 1 = 0 at any common zero.
        constant_bearing = [poly for poly in live if () in poly.terms]
        require(len(constant_bearing) == 1,
                ("not exactly one constant-bearing equation", index))
        shifted = constant_bearing[0] + Poly.const(1)
        multiplier = Poly.var(pvar(0, 4, 0))
        certificate = any(poly is not constant_bearing[0]
                          and multiplier * poly == shifted for poly in live)
        require(certificate, ("no certificate at leaf", index))
        infeasible.append(index)
    require(feasible == 373, ("feasible leaf count", feasible))
    require(len(infeasible) == 10, ("infeasible leaf count", len(infeasible)))


def audit_mutations():
    """each of the five repair entries is load-bearing, and the trade bites"""
    pure_zero = (0,) * 6
    witness_word = (PURE, PURE, 0, 0, PURE, PURE)
    for key in (normal_key(1, 5, 0, 0), normal_key(2, 3, 0, 0),
                normal_key(LEFT, 0, 0, 0), normal_key(RIGHT, 4, 0, 0)):
        saved = BLOCK.pop(key)
        try:
            require(matching_tensor(0, 0, pure_zero) == 0,
                    ("deleting %s did not kill the anchor" % (key,)))
        finally:
            BLOCK[key] = saved
    require(matching_tensor(0, 0, pure_zero) == 1, "the anchor was not restored")

    # d_10 = -1 is forced: the guard's value 0 breaks the supplied 10 row
    key = normal_key(LEFT, RIGHT, 1, 0)
    saved = BLOCK.pop(key)
    try:
        require(matching_tensor(1, 0, witness_word) == 1,
                "dropping d_10 did not break the supplied 10 row")
    finally:
        BLOCK[key] = saved

    # the trade: reinstating the guard's terminal-class carrier d_01 = 1
    # immediately breaks the supplied 01 row at the same word
    key = normal_key(LEFT, RIGHT, 0, 1)
    require(key not in BLOCK, "d_01 is already present")
    BLOCK[key] = Q(1)
    try:
        require(matching_tensor(0, 1, witness_word) == 1,
                "d_01 = 1 did not break the supplied 01 row")
        require(cap_layers(2, 0, 1)[2] == -2, "the (0,1) cap layer moved")
    finally:
        del BLOCK[key]
    require(matching_tensor(0, 1, witness_word) == 0, "d_01 was not removed")


# ==========================================================================
def main():
    audit_normalization()
    audit_packet_shape()
    audit_all_coefficients()
    audit_stars_and_segre()
    audit_terminal_class()
    audit_mutations()

    system = build_symbolic_system()
    audit_symbolic_model(system)
    zeros = audit_forced_zeros(system)
    audit_peel(system, zeros)
    audit_trade(system, zeros)
    audit_colour_one_certificate(system, zeros)
    audit_asymmetry(system, zeros)
    audit_leaf_decision(system, zeros)

    print(
        "PASS: witness verified twice (eight-vertex hafnian and deleted-pair "
        "chart) on all 9*729 coefficients; all 7*729 seven-row coefficients "
        "correct and Row(0,0,0^6)=1, so seven rows + the pure-word colour-0 "
        "anchor is FEASIBLE; ledger exactly (00,(2,0,0,0,0,0),+1) and "
        "(11,1^6,-1), the leak being the anchor's own carrier; stars rank 3/3, "
        "all 81 literal Segre rectangles, direct block -E_10, every admissible "
        "cap has chi=0 (d_01=d_02=0, Q_2 still -2 and 1/2); the reference "
        "search's 383 open leaves are all decided, 373 feasible by explicit "
        "solution and 10 closed by a p_0(4,0) identity; and the colour-1 "
        "pure-word anchor is impossible by an explicit five-term ideal "
        "certificate that provably has no colour-0 analogue"
    )


if __name__ == "__main__":
    main()
