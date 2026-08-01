#!/usr/bin/env python3
"""Cross-colour internal edges: what the seven-row guard still forces.

Section 7 item 2 of ``notes/h3-star-sector-anchor-terminal-class-trade.md``
leaves one boundary open.  That note settles the *monochromatic* star-sector
repair of the audited seven-row guard; when internal edges are allowed to
carry different colours at their two endpoints the note records only that the
collapse mechanism fails -- "the same seven-row propagation forces only 8
unknowns", the anchor rows no longer peel the edge {2,3}, and the branch
search did not terminate.

This checker does not decide that case either.  It proves four exact
statements which cut it down, all of them formal polynomial identities or
exhaustive branch searches over the full 9x729 cross-colour system, never
sampling:

  C0  model agreement.  The symbolic cross-colour system has 6438 nonzero
      equations in 201 unknowns (9 direct scalars, 72 star entries, 30
      monochromatic internal edges, 90 cross-colour internal edges), and at
      the guard point it reproduces the committed two-entry failure ledger
      (00, 0^6, -1), (11, 1^6, -1) exactly.  Specialised to monochromatic
      internal edges it reproduces the committed 32 forced zeros and the
      support collapse to {04,05,14,15,23}.

  C1  the forcing is 20, not 8.  Single-monomial propagation -- the rule used
      in the committed note -- forces 8 cross-colour edges.  Gaussian
      elimination of *all* degree-one equations forces 20 of them and adds
      the two relations
          q(2 at colour 2, 4 at colour c) + q(3 at colour 2, 4 at colour c) = 0
      for c = 0, 1.  So the recorded "only 8
      unknowns" understates what the guard rows already give; the 12 extra
      forcings come from two-term equations, which the single-monomial rule
      cannot see.

  C2  the terminal trade, in full.  Exhaustively over all 729 words, the
      combination Row(0,1,w) + lambda Row(0,2,w) collapses to
      (d_01 + lambda d_02) haf_w(q) for exactly fifteen words at each of
      lambda = +2 and lambda = -2, namely

          lambda = +2 : w_0 = w_1 = w_3 = 2, w_2 free, at most one of
                        w_4, w_5 off colour 2;
          lambda = -2 : w_0 = w_1 = w_2 = 2, w_3 free, same condition on
                        w_4, w_5.

      On the frozen slice the only admissible selected caps with a nonzero
      terminal class are (0,1) with chi = -2 d_01 and (0,2) with
      chi = d_02/2 (recomputed here from the definition), so chi is nonzero
      exactly when (d_01, d_02) != (0,0), and then at least one of the two
      linear forms d_01 +- 2 d_02 is nonzero.  Dividing, that whole family of
      hafnians must vanish.  Reduced by C1 the two families become six
      equations each, and each is a single monomial:

          d_01 + 2 d_02 != 0  ==>  q(2@c, 3@2) = 0 and
                                   q(2@c, 5@2) q(2@2, 4@c') = 0,
          d_01 - 2 d_02 != 0  ==>  q(2@2, 3@c) = 0 and
                                   q(3@c, 5@2) q(2@2, 4@c') = 0,

      for all c, c' in {0,1}, where q(x@a, y@b) is the internal edge {x,y}
      carrying colour a at x and colour b at y.  In particular a completion
      that keeps the edge {2,3} live in both orientations has chi = 0.

  C3  localisation.  An exhaustive branch search closes the whole 9x729
      cross-colour system under the single hypothesis

          every internal edge carrying colour 0 or colour 1 at site 2 or at
          site 3, and colour 2 at its other endpoint, vanishes

      -- twenty of the ninety cross-colour unknowns, none of them already
      forced by C1.  So a cross-colour completion must put 2-mixed internal
      mass on an edge whose *non-2* colour sits at site 2 or site 3: the two
      sites that carry no colour-2 internal edge and that carry the guard's
      anchor stars p_2 = z_2+z_3, s_1 = z_2-z_3.  The monochromatic
      infeasibility of the committed note is the special case in which all
      ninety cross-colour unknowns vanish.

What is NOT proved: the general cross-colour case remains open.  Section C4
records that as a live assertion -- the same propagation applied to the full
system reaches a non-empty residual system that is contradiction-free under
the deterministic closure, which is NOT a consistency proof.

No certified dependency is changed.  Krenn's conjecture remains open.
Standard library only, exact Fraction arithmetic, deterministic across hash
seeds, live under ``python -O`` and ``python -I -S``.
"""

from fractions import Fraction as Q
from itertools import combinations, product


class Contradiction(Exception):
    pass


def require(condition, message):
    if not condition:
        raise AssertionError(message)


COLORS = (0, 1, 2)
SITES = tuple(range(6))
PURE = 2

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
    cached = _MATCH.get(vertices)
    if cached is not None:
        return cached
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
# exact sparse polynomials over integer-indexed unknowns
# --------------------------------------------------------------------------
NAMES = []
INDEX = {}


def vid(name):
    got = INDEX.get(name)
    if got is None:
        got = len(NAMES)
        INDEX[name] = got
        NAMES.append(name)
    return got


def const(value):
    value = Q(value)
    return {(): value} if value else {}


def var(name):
    return {(vid(name),): Q(1)}


def add(a, b):
    out = dict(a)
    for m, c in b.items():
        total = out.get(m)
        total = c if total is None else total + c
        if total:
            out[m] = total
        else:
            out.pop(m, None)
    return out


def scale(a, k):
    return {} if not k else {m: c * k for m, c in a.items()}


def mul(a, b):
    if not a or not b:
        return {}
    out = {}
    for m1, c1 in a.items():
        for m2, c2 in b.items():
            m = tuple(sorted(m1 + m2))
            total = out.get(m)
            total = c1 * c2 if total is None else total + c1 * c2
            if total:
                out[m] = total
            else:
                out.pop(m, None)
    return out


def degree(p):
    return max((len(m) for m in p), default=0)


def substitute(p, sub):
    if not any(v in sub for m in p for v in m):
        return p
    out = {}
    for m, c in p.items():
        term = {(): c}
        for v in m:
            replacement = sub.get(v)
            term = mul(term, {(v,): Q(1)} if replacement is None else replacement)
            if not term:
                break
        out = add(out, term)
    return out


def evaluate(p, assignment):
    total = Q(0)
    for m, c in p.items():
        term = c
        for v in m:
            term *= assignment.get(NAMES[v], Q(0))
            if not term:
                break
        total += term
    return total


# --------------------------------------------------------------------------
# the packet model
# --------------------------------------------------------------------------
ALLOW_CROSS = [True]


def q_edge(x, y, cx, cy):
    if x > y:
        x, y = y, x
        cx, cy = cy, cx
    if cx == PURE and cy == PURE:
        return const(Q2.get((x, y), 0))
    if cx != cy:
        if ALLOW_CROSS[0]:
            return var(("X", x, y, cx, cy))
        return const(0)
    return var(("q", cx, x, y))


def p_entry(i, x, c):
    return const(P2[i][x]) if c == PURE else var(("p", i, x, c))


def s_entry(j, y, c):
    return const(S2[j][y]) if c == PURE else var(("s", j, y, c))


def d_entry(i, j):
    return var(("d", i, j))


def haf(sites, word):
    total = {}
    for matching in matchings(tuple(sites)):
        term = const(1)
        for x, y in matching:
            term = mul(term, q_edge(x, y, word[x], word[y]))
            if not term:
                break
        total = add(total, term)
    return total


def row(i, j, word, sites=SITES):
    sites = tuple(sites)
    total = mul(d_entry(i, j), haf(sites, word))
    for x, y in combinations(sites, 2):
        complement = tuple(v for v in sites if v not in (x, y))
        piece = haf(complement, word)
        if not piece:
            continue
        response = add(mul(p_entry(i, x, word[x]), s_entry(j, y, word[y])),
                       mul(p_entry(i, y, word[y]), s_entry(j, x, word[x])))
        if response:
            total = add(total, mul(response, piece))
    return total


def build_system(allow_cross):
    """All 9*729 GHZ row polynomials that must vanish, keyed (i, j, word)."""
    ALLOW_CROSS[0] = allow_cross
    out = {}
    for word in product(COLORS, repeat=6):
        full = haf(SITES, word)
        holes = {}
        for x, y in combinations(SITES, 2):
            complement = tuple(v for v in SITES if v not in (x, y))
            holes[(x, y)] = haf(complement, word)
        for i, j in product(COLORS, repeat=2):
            total = mul(d_entry(i, j), full)
            for x, y in combinations(SITES, 2):
                piece = holes[(x, y)]
                if not piece:
                    continue
                response = add(
                    mul(p_entry(i, x, word[x]), s_entry(j, y, word[y])),
                    mul(p_entry(i, y, word[y]), s_entry(j, x, word[x])))
                if response:
                    total = add(total, mul(response, piece))
            if i == j and all(c == i for c in word):
                total = add(total, const(-1))
            if total:
                out[(i, j, word)] = total
    return out


GUARD_POINT = {("d", 0, 1): Q(1)}
ANCHOR_ROWS = ((0, 0), (1, 1))


def sorted_keys(system):
    """Deterministic ordering of the row equations, independent of hashing."""
    return sorted(system, key=lambda k: (k[0], k[1], k[2]))


# --------------------------------------------------------------------------
# C0.  normalisation, guard-point agreement, monochromatic specialisation
# --------------------------------------------------------------------------
def audit_normalisation():
    def plain(sites):
        total = Q(0)
        for matching in matchings(tuple(sites)):
            total += Q(1)
        return total

    require(plain(SITES) == 15, "all-ones six-site hafnian is not 15")
    require(plain((0, 1, 2, 3)) == 3, "all-ones four-site hafnian is not 3")
    require(plain((0, 1)) == 1, "all-ones two-site hafnian is not 1")


def audit_model_agreement(cross):
    require(len(cross) == 6438,
            ("cross-colour system size changed", len(cross)))
    kinds = {}
    for name in NAMES:
        if name[0] == "X":
            key = "cross-2mixed" if (name[3] == PURE) != (name[4] == PURE) \
                else "cross-01"
        else:
            key = name[0]
        kinds[key] = kinds.get(key, 0) + 1
    require(kinds == {"d": 9, "p": 36, "s": 36, "q": 30,
                      "cross-2mixed": 60, "cross-01": 30},
            ("unknown census changed", sorted(kinds.items())))

    ledger = sorted((i, j, word, value)
                    for (i, j, word), poly in cross.items()
                    for value in (evaluate(poly, GUARD_POINT),) if value)
    require(ledger == [(0, 0, (0,) * 6, Q(-1)), (1, 1, (1,) * 6, Q(-1))],
            ("the cross-colour model does not reproduce the guard ledger",
             ledger))


def single_monomial_closure(system):
    """The propagation rule of the committed note: only equations that reduce
    to one monomial in one repeated variable force anything."""
    zeros = set()
    while True:
        fresh = set()
        for key in sorted_keys(system):
            reduced = {m: c for m, c in system[key].items()
                       if not any(v in zeros for v in m)}
            if len(reduced) == 1:
                m = next(iter(reduced))
                require(m, ("premature contradiction", key))
                if len(set(m)) == 1:
                    fresh.add(m[0])
        if not fresh - zeros:
            return zeros
        zeros |= fresh


MONO_SUPPORT = ((0, 4), (0, 5), (1, 4), (1, 5), (2, 3))


def audit_monochromatic_specialisation():
    mono = build_system(False)
    zeros = single_monomial_closure(mono)
    require(len(zeros) == 32,
            ("monochromatic forced-zero count changed", len(zeros)))
    for colour in (0, 1):
        alive = tuple(pair for pair in combinations(SITES, 2)
                      if vid(("q", colour) + pair) not in zeros)
        require(alive == MONO_SUPPORT,
                ("colour-%d support collapse changed" % colour, alive))
    ALLOW_CROSS[0] = True          # restore the cross-colour model
    return mono


# --------------------------------------------------------------------------
# C1.  the linear closure forces twenty, not eight
# --------------------------------------------------------------------------
def gauss(rows):
    """Solve a linear system; return {var: linear polynomial}."""
    pivots = {}
    for original in rows:
        r = dict(original)
        while True:
            reducible = None
            for v in sorted(u for m in r if m for u in m):
                if v in pivots and r.get((v,)):
                    reducible = v
                    break
            if reducible is None:
                break
            r = add(r, scale(pivots[reducible], -r[(reducible,)]))
        live = sorted(v for m in r if m for v in m)
        if not live:
            if r.get(()):
                # an inconsistent linear part closes the branch; it must not
                # abort the run, so raise the exception the search catches
                raise Contradiction("the linear subsystem is inconsistent")
            continue
        head = live[0]
        pivots[head] = scale(r, Q(1) / r[(head,)])
    resolved = {}
    for v in sorted(pivots, reverse=True):
        expr = {}
        for m, c in pivots[v].items():
            if m != (v,):
                expr = add(expr, {m: -c})
        resolved[v] = substitute(expr, resolved)
    return resolved


def linear_closure(system):
    """Iterate Gaussian elimination of every degree<=1 equation."""
    system = dict(system)
    subs = {}
    while True:
        rows = [system[k] for k in sorted_keys(system) if degree(system[k]) <= 1]
        if not rows:
            return system, subs
        resolved = gauss(rows)
        if not resolved:
            return system, subs
        for v in list(subs):
            subs[v] = substitute(subs[v], resolved)
        subs.update(resolved)
        fresh = {}
        for k in sorted_keys(system):
            reduced = substitute(system[k], resolved)
            require(not reduced or any(m for m in reduced),
                    ("linear closure produced a nonzero constant", k))
            if reduced:
                fresh[k] = reduced
        system = fresh


WEAK_ZEROS = (("X", 0, 1, 0, 2), ("X", 0, 1, 1, 2),
              ("X", 0, 1, 2, 0), ("X", 0, 1, 2, 1),
              ("X", 4, 5, 0, 2), ("X", 4, 5, 1, 2),
              ("X", 4, 5, 2, 0), ("X", 4, 5, 2, 1))

STRONG_ZEROS = WEAK_ZEROS + (
    ("X", 0, 2, 0, 2), ("X", 0, 2, 1, 2), ("X", 0, 3, 0, 2), ("X", 0, 3, 1, 2),
    ("X", 1, 2, 0, 2), ("X", 1, 2, 1, 2), ("X", 1, 3, 0, 2), ("X", 1, 3, 1, 2),
    ("X", 2, 5, 2, 0), ("X", 2, 5, 2, 1), ("X", 3, 5, 2, 0), ("X", 3, 5, 2, 1))


def audit_forcing_strength(cross):
    weak = single_monomial_closure(cross)
    require(sorted(NAMES[v] for v in weak) == sorted(WEAK_ZEROS),
            ("the note's single-monomial propagation changed",
             sorted(str(NAMES[v]) for v in weak)))

    reduced, subs = linear_closure(cross)
    zeros = sorted(NAMES[v] for v, e in subs.items() if not e)
    require(zeros == sorted(STRONG_ZEROS),
            ("the linear closure forced-zero set changed", zeros))
    relations = sorted(
        (NAMES[v], sorted((NAMES[m[0]], c) for m, c in e.items()))
        for v, e in subs.items() if e)
    require(relations == [
        (("X", 3, 4, 2, 0), [(("X", 2, 4, 2, 0), Q(-1))]),
        (("X", 3, 4, 2, 1), [(("X", 2, 4, 2, 1), Q(-1))]),
    ], ("the linear closure relations changed", relations))
    require(set(weak) < {vid(n) for n in STRONG_ZEROS},
            "the strengthened forcing does not extend the recorded one")
    return reduced


# --------------------------------------------------------------------------
# C2.  the trade identities at the edge {2,3}
# --------------------------------------------------------------------------
def flip_word(site, colour):
    return tuple(colour if x == site else PURE for x in SITES)


def audit_trade_identities(cross):
    """The full terminal-trade family, exhaustive over all 729 words.

    Rows (0,1) and (0,2) differ only in the second star label, and on the
    frozen slice s_1 and s_2 are proportional site by site: s_1 = 2 s_2 at
    site 2, s_1 = -2 s_2 at site 3, and both vanish at sites 0, 1, 4, 5.  So
    for lambda = -2 the whole colour-2 star contact at site 2 cancels in
    Row(0,1) + lambda Row(0,2), and for lambda = +2 the contact at site 3
    does.  Whenever no *other* contact survives, the combination collapses to
    (d_01 + lambda d_02) * haf_w(q).  This function determines exactly which
    words that happens for.
    """
    d01, d02 = var(("d", 0, 1)), var(("d", 0, 2))
    families = {}
    for lam in (Q(2), Q(-2)):
        scalar = add(d01, scale(d02, lam))
        found = []
        for word in product(COLORS, repeat=6):
            left = add(cross.get((0, 1, word), {}),
                       scale(cross.get((0, 2, word), {}), lam))
            if left == mul(scalar, haf(SITES, word)):
                found.append(word)
        families[lam] = sorted(found)

    def described(pinned):
        out = []
        for word in product(COLORS, repeat=6):
            if word[0] != PURE or word[1] != PURE or word[pinned] != PURE:
                continue
            if word[4] != PURE and word[5] != PURE:
                continue
            out.append(word)
        return sorted(out)

    require(families[Q(2)] == described(3),
            ("the lambda=+2 trade family changed", len(families[Q(2)])))
    require(families[Q(-2)] == described(2),
            ("the lambda=-2 trade family changed", len(families[Q(-2)])))
    require(len(families[Q(2)]) == 15 and len(families[Q(-2)]) == 15,
            "the trade families are not of size fifteen")

    # the one-flip members are the two named trade equations of the note
    for colour in (0, 1):
        g = var(("X", 2, 3, colour, PURE))
        w = flip_word(2, colour)
        require(haf(SITES, w) == g, ("site-2 flip hafnian changed", colour))
        require(cross[(1, 0, w)] == mul(g, add(const(1), var(("d", 1, 0)))),
                ("site-2 (1,0) trade identity changed", colour))
        require(cross[(0, 0, w)] == mul(g, var(("d", 0, 0))),
                ("site-2 (0,0) trade identity changed", colour))
        h = var(("X", 2, 3, PURE, colour))
        w = flip_word(3, colour)
        require(haf(SITES, w) == h, ("site-3 flip hafnian changed", colour))
        require(cross[(1, 0, w)] == mul(h, add(const(1), var(("d", 1, 0)))),
                ("site-3 (1,0) trade identity changed", colour))
        require(cross[(0, 0, w)] == mul(h, var(("d", 0, 0))),
                ("site-3 (0,0) trade identity changed", colour))
    return families


def audit_trade_residue(cross, families, forced_zero):
    """After C1 the two families reduce to an explicit short list."""
    zeros = {vid(name): {} for name in forced_zero}
    zeros[vid(("X", 3, 4, 2, 0))] = scale(var(("X", 2, 4, 2, 0)), Q(-1))
    zeros[vid(("X", 3, 4, 2, 1))] = scale(var(("X", 2, 4, 2, 1)), Q(-1))
    residue = {}
    for lam, words in families.items():
        live = []
        for word in words:
            reduced = substitute(haf(SITES, word), zeros)
            if reduced:
                live.append((word, reduced))
        residue[lam] = live
    plus = sorted((w, sorted((tuple(sorted(NAMES[v] for v in m)), c)
                             for m, c in p.items()))
                  for w, p in residue[Q(2)])
    minus = sorted((w, sorted((tuple(sorted(NAMES[v] for v in m)), c)
                              for m, c in p.items()))
                   for w, p in residue[Q(-2)])
    expected_plus = [
        ((2, 2, 0, 2, 0, 2), [((("X", 2, 4, 2, 0), ("X", 2, 5, 0, 2)), Q(-1))]),
        ((2, 2, 0, 2, 1, 2), [((("X", 2, 4, 2, 1), ("X", 2, 5, 0, 2)), Q(-1))]),
        ((2, 2, 0, 2, 2, 2), [((("X", 2, 3, 0, 2),), Q(1))]),
        ((2, 2, 1, 2, 0, 2), [((("X", 2, 4, 2, 0), ("X", 2, 5, 1, 2)), Q(-1))]),
        ((2, 2, 1, 2, 1, 2), [((("X", 2, 4, 2, 1), ("X", 2, 5, 1, 2)), Q(-1))]),
        ((2, 2, 1, 2, 2, 2), [((("X", 2, 3, 1, 2),), Q(1))]),
    ]
    expected_minus = [
        ((2, 2, 2, 0, 0, 2), [((("X", 2, 4, 2, 0), ("X", 3, 5, 0, 2)), Q(1))]),
        ((2, 2, 2, 0, 1, 2), [((("X", 2, 4, 2, 1), ("X", 3, 5, 0, 2)), Q(1))]),
        ((2, 2, 2, 0, 2, 2), [((("X", 2, 3, 2, 0),), Q(1))]),
        ((2, 2, 2, 1, 0, 2), [((("X", 2, 4, 2, 0), ("X", 3, 5, 1, 2)), Q(1))]),
        ((2, 2, 2, 1, 1, 2), [((("X", 2, 4, 2, 1), ("X", 3, 5, 1, 2)), Q(1))]),
        ((2, 2, 2, 1, 2, 2), [((("X", 2, 3, 2, 1),), Q(1))]),
    ]
    require(plus == expected_plus,
            ("the reduced lambda=+2 trade family changed", plus))
    require(minus == expected_minus,
            ("the reduced lambda=-2 trade family changed", minus))
    return plus, minus


def cap_layers(a, b, alpha):
    """(Q0,Q1,Q2,Q3)-graded layers of haf(alpha*q2 + R_ab) on the pure word."""
    u = P2[a]
    v = S2[b]
    internal = [[Q(0) if x == y else Q(Q2.get((min(x, y), max(x, y)), 0))
                 for y in SITES] for x in SITES]
    response = [[Q(0) if x == y else u[x] * v[y] + v[x] * u[y]
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
                    term *= response[x][y] if flag else alpha * internal[x][y]
                value += term
        layers.append(value)
    return tuple(layers)


def audit_terminal_class_table():
    profile = {}
    for a, b in product(COLORS, repeat=2):
        rows = {alpha: cap_layers(a, b, Q(alpha)) for alpha in (1, 2, -3)}
        q2, q3 = rows[1][2], rows[1][3]
        for alpha, layers in rows.items():
            require(layers[2] == Q(alpha) * q2,
                    ("layer two is not linear in the direct scalar", a, b))
            require(layers[3] == q3,
                    ("layer three depends on the direct scalar", a, b))
        profile[(a, b)] = (rows[1][0] == 0 and rows[1][1] == 0, q2, q3)
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


def audit_trade_corollary(cross):
    """g and h both live force d_01 = d_02 = 0, hence chi = 0 on every cap.

    The two terminal trade identities are g*(d_01+2d_02) and h*(d_01-2d_02).
    In an integral domain a nonzero g and a nonzero h leave the linear system
    d_01+2d_02 = d_01-2d_02 = 0, whose only solution is d_01 = d_02 = 0; the
    terminal class of the two admissible caps is -2*d_01 and d_02/2."""
    for gc, hc in product((0, 1), repeat=2):
        require(("X", 2, 3, gc, PURE) in INDEX and ("X", 2, 3, PURE, hc) in INDEX,
                ("a trade edge is missing from the model", gc, hc))
        require(cross[(0, 1, flip_word(2, gc))] and cross[(0, 1, flip_word(3, hc))],
                ("a trade row vanished identically", gc, hc))
    plus = add(var(("d", 0, 1)), scale(var(("d", 0, 2)), Q(2)))
    minus = add(var(("d", 0, 1)), scale(var(("d", 0, 2)), Q(-2)))
    solved = gauss([plus, minus])
    require(sorted((NAMES[v], sorted(e.items())) for v, e in solved.items())
            == [(("d", 0, 1), []), (("d", 0, 2), [])],
            ("the two trade relations do not force both direct scalars",
             sorted(str(NAMES[v]) for v in solved)))


# --------------------------------------------------------------------------
# C3.  exhaustive branch search under the localisation hypothesis
# --------------------------------------------------------------------------
def propagate(system, nonzero):
    """Deterministic closure: single-monomial forcing, division by known
    nonzero common factors, and Gaussian elimination of all linear rows."""
    system = dict(system)
    while True:
        changed = False
        forced = {}
        for key in sorted(system, key=repr):
            poly = system[key]
            if len(poly) == 1:
                m = next(iter(poly))
                if not m:
                    raise Contradiction("nonzero constant equation")
                unknown = sorted(set(m) - nonzero)
                if not unknown:
                    raise Contradiction("a product of nonzero unknowns is zero")
                if len(unknown) == 1:
                    forced[unknown[0]] = {}
                continue
            common = None
            for m in poly:
                common = set(m) if common is None else (common & set(m))
                if not common:
                    break
            if common:
                good = sorted(common & nonzero)
                if good:
                    v = good[0]
                    stripped = {}
                    for m, c in poly.items():
                        rest = list(m)
                        rest.remove(v)
                        stripped[tuple(rest)] = c
                    if stripped and not any(m for m in stripped):
                        raise Contradiction("nonzero constant after division")
                    system[key] = stripped
                    changed = True
        if forced:
            for v in forced:
                if v in nonzero:
                    raise Contradiction("forced a nonzero unknown to zero")
            system = apply_subs(system, forced)
            continue
        rows = [system[k] for k in sorted(system, key=repr)
                if degree(system[k]) <= 1]
        if rows:
            resolved = gauss(rows)
            if resolved:
                for v in resolved:
                    if v in nonzero and not resolved[v]:
                        raise Contradiction("forced a nonzero unknown to zero")
                system = apply_subs(system, resolved)
                continue
        if not changed:
            return system


def apply_subs(system, sub):
    out = {}
    for key in sorted(system, key=repr):
        poly = substitute(system[key], sub)
        if poly and not any(m for m in poly):
            raise Contradiction("nonzero constant equation")
        if poly:
            out[key] = poly
    return out


def choose_branch(system, nonzero):
    best = None
    for key in sorted(system, key=repr):
        poly = system[key]
        if len(poly) != 1:
            continue
        unknown = tuple(sorted(set(next(iter(poly))) - nonzero))
        if best is None or len(unknown) < len(best):
            best = unknown
    return best


def branch_search(system, node_limit):
    """Exhaustive: every single-monomial equation splits into its factors."""
    try:
        root = propagate(system, frozenset())
    except Contradiction:
        return 1, 0, 0
    stack = [(root, frozenset())]
    nodes = 0
    undecided = 0
    solved = 0
    while stack:
        system, nonzero = stack.pop()
        nodes += 1
        if nodes > node_limit:
            return nodes, undecided, solved
        if not system:
            solved += 1
            continue
        factors = choose_branch(system, nonzero)
        if factors is None:
            undecided += 1
            continue
        # propagate() closes any node whose single-monomial equation has all
        # of its factors already known nonzero, so the split below is over a
        # non-empty list and is exhaustive.
        require(factors, "branching on an empty factor list")
        seen = []
        for v in factors:
            try:
                child = propagate(apply_subs(system, {v: {}}),
                                  nonzero | frozenset(seen))
            except Contradiction:
                seen.append(v)
                continue
            stack.append((child, nonzero | frozenset(seen)))
            seen.append(v)
    return nodes, undecided, solved


def two_mixed(name):
    """A cross edge with exactly one endpoint at colour 2, and the site that
    carries the other colour."""
    x, y, cx, cy = name[1], name[2], name[3], name[4]
    if (cx == PURE) == (cy == PURE):
        return None
    return x if cx != PURE else y


def audit_localisation(cross):
    killed = {}
    named = []
    for name in NAMES:
        if name[0] != "X":
            continue
        site = two_mixed(name)
        if site in (2, 3):
            killed[vid(name)] = {}
            named.append(name)
    require(len(named) == 20,
            ("the localisation hypothesis changed size", len(named)))
    require(("X", 2, 3, 0, PURE) in named and ("X", 2, 3, PURE, 0) in named,
            "the localisation hypothesis misses the edge {2,3}")
    system = apply_subs(cross, killed)
    nodes, undecided, solved = branch_search(system, 20000)
    require(solved == 0,
            ("the localisation branch search produced a solution leaf", solved))
    require(undecided == 0,
            ("the localisation branch search left undecided leaves", undecided))
    require(nodes == 106, ("localisation node count changed", nodes))
    return nodes


# --------------------------------------------------------------------------
# C4.  live scope guard: the general cross-colour case is NOT decided here
# --------------------------------------------------------------------------
def audit_scope(cross):
    residual = propagate(cross, frozenset())
    require(len(residual) > 1000,
            ("the unconditional cross-colour system unexpectedly collapsed",
             len(residual)))
    factors = choose_branch(residual, frozenset())
    require(factors is not None and len(factors) >= 2,
            "the unconditional system unexpectedly has a single-variable forcing")
    return len(residual)


def main():
    audit_normalisation()
    cross = build_system(True)
    audit_model_agreement(cross)
    audit_monochromatic_specialisation()
    audit_forcing_strength(cross)
    families = audit_trade_identities(cross)
    plus, minus = audit_trade_residue(cross, families, STRONG_ZEROS)
    audit_terminal_class_table()
    audit_trade_corollary(cross)
    nodes = audit_localisation(cross)
    residual = audit_scope(cross)
    print(
        "PASS: cross-colour model reproduces the committed guard ledger and "
        "the monochromatic 32-zero collapse; the guard rows force 20 "
        "cross-colour edges (not 8) plus q(2@2,4@c)+q(3@2,4@c)=0; the edge "
        "{2,3} trade extends to two fifteen-word families forcing "
        "q(2@c,3@2)=q(2@c,5@2)q(2@2,4@c\')=0 when d_01+2d_02 != 0 and the "
        "mirror list when d_01-2d_02 != 0, so a completion live on {2,3} in "
        "both orientations has chi=0; killing the "
        "twenty internal edges that carry a non-2 colour at site 2 or site 3 "
        "against a colour-2 partner closes the whole 9x729 system over %d "
        "branch nodes; the unconditional cross-colour case is left open with "
        "%d residual equations" % (nodes, residual)
    )


if __name__ == "__main__":
    main()
