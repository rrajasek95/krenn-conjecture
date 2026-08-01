#!/usr/bin/env python3
"""The colour pencil form of the monochromatic 9x729 system, and what it forces.

Model (identical to the one audited in
``verify_monochromatic_internal_quadratic_structure.py`` and, through it, to
``verify_h3_diagonal_segre_second_transgression_seven_row_guard.py``): six
residual sites ``W = {0..5}`` and two endpoints; a packet carries an internal
quadratic ``q``, endpoint stars ``p_i(x,c)``, ``s_j(y,c)`` and a direct block
``d_ij``, and

    Row(i,j,w) = d_ij haf_w(q)
               + sum_{x<y} [p_i(x,w_x) s_j(y,w_y) + p_i(y,w_y) s_j(x,w_x)]
                 haf_w(q restricted to W\\{x,y}).

A *GHZ realization* is a packet with ``Row(i,j,w) = 1`` when ``i = j`` and
``w = i^6`` and ``0`` otherwise.  Whether one exists is open (this is Krenn's
conjecture at n = 8) and nothing here decides it.  This checker studies the
*monochromatic* chart ``q(x,y,cx,cy) = 0`` for ``cx != cy``.

What is verified, in the order it runs:

  1  all-ones hafnian normalization (15 on six sites, 3 on four, 1 on two);
  2  the symbolic system reproduces the committed seven-row guard ledger
     ``(00,0^6,-1)``, ``(11,1^6,-1)`` and the committed eight-cycle guard ledger
     ``(22,2^6,-1)`` -- this pins the model to the audited one;
  3  (G'), the colour pencil identity.  With
         Q_lam   = sum_c lam_c^2 q_c,
         X^lam   = sum_c lam_c X_c        (X_c is 3x6, entry p_i(x,c)),
         Y^lam   = sum_c lam_c Y_c        (Y_c is 3x6, entry s_j(y,c)),
         H(A)_xy = haf(A restricted to W\\{x,y}), H(A)_xx = 0,
     the 9x729 system implies the single matrix identity
         haf(Q_lam) d + X^lam H(Q_lam) (Y^lam)^T = diag(lam_0^6,lam_1^6,lam_2^6)
     holding identically in lam.  Verified as a formal identity in lam and in all
     162 packet unknowns, over all monomials, for all nine label pairs: the
     lam-multidegree (n0,n1,n2) part of entry (i,j) is exactly the sum of
     Row(i,j,w) - target(i,j,w) over the words w with n_c sites of colour c.
     So (G') is the *colour-census aggregate* of the rows -- 28 multidegrees
     times nine label pairs, 252 equations, not all 6561 -- and everything below
     that is derived from (G') is derived from a consequence of the system, not
     from an equivalent form of it;
  4  the Laplace expansion haf(Q_lam) = sum_y Q_lam(x,y) H(Q_lam)(x,y) at every
     site, as a formal identity in lam and q;
  5  T6, the pencil non-degeneracy lemma, and its two corollaries.  Steps 3 and 4
     give: if H(Q_lam) = 0 then also haf(Q_lam) = 0, so (G') reads
     diag(lam_0^6,lam_1^6,lam_2^6) = 0 and lam = 0.  Hence in any GHZ realization
     H(Q_lam) != 0 for every lam != 0, i.e. every nonzero member of the pencil
     spanned by q_0,q_1,q_2 has a nonzero four-hole cofactor.  Corollaries:
     (a) at lam = e_c this is exactly T2; (b) q_0,q_1,q_2 are linearly
     independent (over any field, by passing to the algebraic closure, where
     every mu_c is a square).  Machine-checked here: the four-hole matrix of the
     zero array is zero; every monomial of every four-hole cofactor is a product
     of two disjoint edges; and both committed guards violate T6 exactly at the
     colours whose anchors they fail;
  6  T3 in pencil form.  MACHINE-CHECKED HERE: only the word-level blind-label
     identity, namely that if a label j0 is blind for the first star then
     Row(j0,j,w) = d_{j0 j} haf_w(q) for every word.  The rest of this item is a
     SHORT HAND PROOF and is not verified by this script: row j0 of (G') then
     reads haf(Q_lam) d_{j0 j} = delta_{j0 j} lam_{j0}^6, and reading that off
     census by census gives T3's normalization -- for a common left kernel
     vector a of the star, h_j(W) (a^T d)_j = a_j and every other census of
     haf(Q_lam) is killed, so at most one a_j is nonzero, the kernel is a
     coordinate vector, and the kernel is at most one dimensional;
  7  the rank-two reduction RP2.  In the rank-two branch (some label j0 blind for
     the first star; the diagonal S_3 puts j0 = 0) the word-level identity of
     step 6 gives Row(0,0,w) = d_00 haf_w(q), hence d_00 h_0(W) = 1 and
     haf_w(q) = 0 for every single word w != 0^6, so the direct block drops out
     of every row at a word in colours {1,2}.  Restricting
     to labels {1,2} leaves a self-contained two-colour star-only system: 288
     equations in 78 unknowns, with no direct block and no colour-0 datum.
     Verified: the reduction identity, the census, and an explicit integer
     solution of RP2.  So RP2 is *satisfiable*, and the rank-two branch cannot
     be closed through its two-colour sector: everything the branch still
     contains lives in the colour-0 and label-0 equations.  The witness is the
     alternating eight-cycle carrying its two endpoints at cycle distance two,
     which uses no direct edge at all;
  8  the alternating eight-cycle guard is a four-member family, and none of it
     completes.  Placing the two endpoints at any two of the eight cycle
     vertices gives a monochromatic packet satisfying 6560 of the 6561
     equations and failing only the third colour's anchor; all 56 placements in
     colours {1,2} are checked, and only the distance-one placement -- the
     committed guard -- uses the direct edge.  Freezing each placement's
     colour-1/colour-2 sector and freeing the whole colour-0 sector plus all
     nine direct scalars (60 unknowns, every coefficient +-1) closes all 56
     systems with no open leaf, in at most 27 branch nodes.  SCOPE, inherited
     from the committed one-chart closure: cross-colour internal edges carrying
     the free colour at one end lie OUTSIDE the chart and are not covered.
     This generalizes
     the committed slice-specific completion statement from one placement to
     every placement, over any field.

Research evidence only.  Krenn's conjecture remains open, no certified
dependency changes, and `SP-CLEAN-BRIDGE` is untouched.  Standard library only,
exact ``Fraction`` arithmetic, deterministic, live under ``python -O``.
"""

from fractions import Fraction as Q
from itertools import combinations, product

COLORS = (0, 1, 2)
SITES = tuple(range(6))
EDGES = tuple(combinations(SITES, 2))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


# --------------------------------------------------------------------------
# matchings, and a minimal exact sparse polynomial ring on squarefree monomials
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


_VARS = []
_VIDX = {}


def _register(key):
    _VIDX[key] = len(_VARS)
    _VARS.append(key)


for _c in COLORS:
    for _e in EDGES:
        _register(("q", _c, _e[0], _e[1]))
for _i in COLORS:
    for _x in SITES:
        for _c in COLORS:
            _register(("p", _i, _x, _c))
for _j in COLORS:
    for _y in SITES:
        for _c in COLORS:
            _register(("s", _j, _y, _c))
for _i in COLORS:
    for _j in COLORS:
        _register(("d", _i, _j))

NVAR = len(_VARS)


def bit(key):
    return 1 << _VIDX[key]


def var_of_bit(one_bit):
    return _VARS[one_bit.bit_length() - 1]


def bits(mask):
    out = []
    while mask:
        low = mask & -mask
        out.append(low)
        mask ^= low
    return out


def padd(*polys):
    out = {}
    for poly in polys:
        for m, c in poly.items():
            total = out.get(m, 0) + c
            if total:
                out[m] = total
            else:
                out.pop(m, None)
    return out


def pmul(a, b):
    out = {}
    for m1, c1 in a.items():
        for m2, c2 in b.items():
            m = m1 | m2
            total = out.get(m, 0) + c1 * c2
            if total:
                out[m] = total
            else:
                out.pop(m, None)
    return out


def pvar(key):
    return {bit(key): 1}


ONE = {0: 1}


def evaluate(poly, point):
    total = Q(0)
    for m, c in poly.items():
        term = Q(c)
        for b in bits(m):
            term *= point.get(var_of_bit(b), Q(0))
            if not term:
                break
        total += term
    return total


# --------------------------------------------------------------------------
# the physical row, straight from the definition
# --------------------------------------------------------------------------
_HAF = {}


def haf_word(sites, word):
    sites = tuple(sites)
    key = (sites, tuple(word[v] for v in sites))
    if key in _HAF:
        return _HAF[key]
    out = {}
    for matching in matchings(sites):
        m = 0
        alive = True
        for x, y in matching:
            if word[x] != word[y]:
                alive = False
                break
            m |= bit(("q", word[x], min(x, y), max(x, y)))
        if alive:
            out[m] = out.get(m, 0) + 1
    out = {m: c for m, c in out.items() if c}
    _HAF[key] = out
    return out


_ROW = {}


def row(i, j, word):
    key = (i, j, tuple(word))
    if key in _ROW:
        return _ROW[key]
    out = {}
    dm = bit(("d", i, j))
    for m, c in haf_word(SITES, word).items():
        out[m | dm] = out.get(m | dm, 0) + c
    for x, y in combinations(SITES, 2):
        rest = tuple(v for v in SITES if v != x and v != y)
        piece = haf_word(rest, word)
        if not piece:
            continue
        for a, b in ((x, y), (y, x)):
            fm = bit(("p", i, a, word[a])) | bit(("s", j, b, word[b]))
            for m, c in piece.items():
                out[m | fm] = out.get(m | fm, 0) + c
    out = {m: c for m, c in out.items() if c}
    _ROW[key] = out
    return out


def ghz_target(i, j, word):
    return 1 if (i == j and all(c == i for c in word)) else 0


# --------------------------------------------------------------------------
# 1.  normalization
# --------------------------------------------------------------------------
def audit_normalization():
    require(len(matchings(SITES)) == 15, "six-site matching count is not 15")
    require(len(matchings((0, 1, 2, 3))) == 3, "four-site matching count is not 3")
    require(len(matchings((0, 1))) == 1, "two-site matching count is not 1")
    require(len(matchings(())) == 1, "the empty matching set is not a singleton")
    require(len(matchings((0, 1, 2, 3, 4))) == 0,
            "an odd vertex set has a matching")
    require(NVAR == 162, ("packet unknown count changed", NVAR))


# --------------------------------------------------------------------------
# 2.  agreement with the two committed guards
# --------------------------------------------------------------------------
GUARD_Q2 = {(0, 1): 1, (4, 5): 1}
GUARD_P2 = {0: (1, 1, 0, 0, 0, 0), 1: (0, 0, 0, 0, 1, 0), 2: (0, 0, 1, 1, 0, 0)}
GUARD_S2 = {0: (0, 0, 0, 0, 0, 1), 1: (0, 0, 1, -1, 0, 0),
            2: (0, 0, Q(1, 2), Q(1, 2), 0, 0)}

CYCLE = {("p", 0, 0, 0): Q(1), ("q", 1, 0, 1): Q(1), ("q", 0, 1, 2): Q(1),
         ("q", 1, 2, 3): Q(1), ("q", 0, 3, 4): Q(1), ("q", 1, 4, 5): Q(1),
         ("s", 0, 5, 0): Q(1), ("d", 1, 1): Q(1)}


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


def build_system():
    out = {}
    for word in product(COLORS, repeat=6):
        for i, j in product(COLORS, repeat=2):
            poly = dict(row(i, j, word))
            t = ghz_target(i, j, word)
            if t:
                poly[0] = poly.get(0, 0) - t
                if not poly[0]:
                    del poly[0]
            out[(i, j, word)] = poly
    return out


def audit_guard_ledgers(system):
    point = guard_point()
    ledger = sorted((i, j, word, value)
                    for (i, j, word), poly in system.items()
                    for value in (evaluate(poly, point),) if value)
    require(ledger == [(0, 0, (0,) * 6, Q(-1)), (1, 1, (1,) * 6, Q(-1))],
            ("the symbolic system does not reproduce the seven-row guard ledger",
             ledger))
    ledger = sorted((i, j, word, value)
                    for (i, j, word), poly in system.items()
                    for value in (evaluate(poly, CYCLE),) if value)
    require(ledger == [(2, 2, (2,) * 6, Q(-1))],
            ("the symbolic system does not reproduce the eight-cycle guard "
             "ledger", ledger))


# --------------------------------------------------------------------------
# 3.  (G'), the colour pencil identity
# --------------------------------------------------------------------------
# a lam-graded polynomial is  dict (n0,n1,n2) -> polynomial in the 162 unknowns
def gadd(a, b):
    out = {k: dict(v) for k, v in a.items()}
    for k, v in b.items():
        merged = padd(out.get(k, {}), v)
        if merged:
            out[k] = merged
        else:
            out.pop(k, None)
    return out


def gmul(a, b):
    out = {}
    for k1, v1 in a.items():
        for k2, v2 in b.items():
            k = (k1[0] + k2[0], k1[1] + k2[1], k1[2] + k2[2])
            merged = padd(out.get(k, {}), pmul(v1, v2))
            if merged:
                out[k] = merged
            else:
                out.pop(k, None)
    return out


def glam(c, power):
    key = [0, 0, 0]
    key[c] = power
    return {tuple(key): dict(ONE)}


def Q_entry(x, y):
    """entry (x,y) of Q_lam = sum_c lam_c^2 q_c."""
    if x == y:
        return {}
    out = {}
    for c in COLORS:
        out = gadd(out, gmul(glam(c, 2), {(0, 0, 0): pvar(
            ("q", c, min(x, y), max(x, y)))}))
    return out


def Q_haf(sites):
    out = {}
    for matching in matchings(tuple(sites)):
        term = {(0, 0, 0): dict(ONE)}
        for x, y in matching:
            term = gmul(term, Q_entry(x, y))
        out = gadd(out, term)
    return out


def X_entry(i, x):
    out = {}
    for c in COLORS:
        out = gadd(out, gmul(glam(c, 1), {(0, 0, 0): pvar(("p", i, x, c))}))
    return out


def Y_entry(j, y):
    out = {}
    for c in COLORS:
        out = gadd(out, gmul(glam(c, 1), {(0, 0, 0): pvar(("s", j, y, c))}))
    return out


def audit_colour_pencil_identity(system):
    hfull = Q_haf(SITES)
    hhole = {}
    for x, y in combinations(SITES, 2):
        hhole[(x, y)] = Q_haf(tuple(v for v in SITES if v not in (x, y)))
    require(sorted(hfull) == [(0, 0, 6), (0, 2, 4), (0, 4, 2), (0, 6, 0),
                              (2, 0, 4), (2, 2, 2), (2, 4, 0), (4, 0, 2),
                              (4, 2, 0), (6, 0, 0)],
            ("haf(Q_lam) is not the expected ternary cubic in lam^2",
             sorted(hfull)))
    for i, j in product(COLORS, repeat=2):
        left = gmul({(0, 0, 0): pvar(("d", i, j))}, hfull)
        for x, y in combinations(SITES, 2):
            block = gadd(gmul(X_entry(i, x), Y_entry(j, y)),
                         gmul(X_entry(i, y), Y_entry(j, x)))
            left = gadd(left, gmul(block, hhole[(x, y)]))
        if i == j:
            key = [0, 0, 0]
            key[i] = 6
            left = gadd(left, {tuple(key): {0: -1}})
        right = {}
        for word in product(COLORS, repeat=6):
            key = tuple(sum(1 for v in SITES if word[v] == c) for c in COLORS)
            slot = right.setdefault(key, {})
            for m, c in system[(i, j, word)].items():
                total = slot.get(m, 0) + c
                if total:
                    slot[m] = total
                else:
                    slot.pop(m, None)
        right = {k: v for k, v in right.items() if v}
        require(left == right,
                ("the colour pencil identity (G') failed", i, j))
    return hfull, hhole


# --------------------------------------------------------------------------
# 4.  the Laplace expansion of haf(Q_lam)
# --------------------------------------------------------------------------
def audit_pencil_laplace(hfull, hhole):
    for x in SITES:
        total = {}
        for y in SITES:
            if y == x:
                continue
            key = (min(x, y), max(x, y))
            total = gadd(total, gmul(Q_entry(x, y), hhole[key]))
        require(total == hfull,
                ("the pencil Laplace expansion failed at a site", x))


# --------------------------------------------------------------------------
# 5.  T6, the pencil non-degeneracy lemma
# --------------------------------------------------------------------------
def audit_pencil_nondegeneracy(hhole):
    # (a) every monomial of every four-hole cofactor is a product of two
    #     *disjoint* edges of one colour -- so a colour whose support has no two
    #     disjoint edges has H = 0 identically, which is L0/T2's support form.
    for (x, y), graded in hhole.items():
        for key, poly in graded.items():
            require(sum(key) == 4, ("a four-hole cofactor has the wrong "
                                    "lam-degree", x, y, key))
            for m in poly:
                pieces = [var_of_bit(b) for b in bits(m)]
                require(len(pieces) == 2 and all(v[0] == "q" for v in pieces),
                        ("a four-hole monomial is not a pair of edges", pieces))
                e1 = {pieces[0][2], pieces[0][3]}
                e2 = {pieces[1][2], pieces[1][3]}
                require(not (e1 & e2),
                        ("a four-hole monomial uses two meeting edges", pieces))
    # (b) the four-hole matrix of the zero array is zero, so Q_lam = 0 forces
    #     H(Q_lam) = 0 and, by step 4, haf(Q_lam) = 0 as well.
    zero_point = {}
    for (x, y), graded in hhole.items():
        for key, poly in graded.items():
            require(evaluate(poly, zero_point) == 0,
                    ("a four-hole cofactor is nonzero on the zero array", x, y))
    # (c) both committed guards violate T6, exactly at the colours whose anchors
    #     they fail: the seven-row guard has q_0 = q_1 = 0 and fails the colour-0
    #     and colour-1 anchors; the eight-cycle guard has q_2 = 0 and fails the
    #     colour-2 anchor.
    guard = guard_point()
    dead = tuple(c for c in COLORS
                 if all(guard.get(("q", c, x, y), Q(0)) == 0 for x, y in EDGES))
    require(dead == (0, 1), ("the seven-row guard's dead colours changed", dead))
    dead = tuple(c for c in COLORS
                 if all(CYCLE.get(("q", c, x, y), Q(0)) == 0 for x, y in EDGES))
    require(dead == (2,), ("the eight-cycle guard's dead colours changed", dead))


# --------------------------------------------------------------------------
# 6.  T3 in pencil form
# --------------------------------------------------------------------------
def kill(poly, dead_mask):
    return {m: c for m, c in poly.items() if not (m & dead_mask)}


def audit_blind_label_pencil():
    """Row j0 of (G') is the lam-graded sum of the rows Row(j0,j,w), so killing
    every p_{j0} entry word by word is the same statement."""
    for j0 in COLORS:
        dead = 0
        for x in SITES:
            for c in COLORS:
                dead |= bit(("p", j0, x, c))
        for word in product(COLORS, repeat=6):
            for j in COLORS:
                require(kill(row(j0, j, word), dead)
                        == pmul(pvar(("d", j0, j)), haf_word(SITES, word)),
                        ("the label-blind row is not purely direct",
                         j0, j, word))


# --------------------------------------------------------------------------
# 7.  RP2, the rank-two residual
# --------------------------------------------------------------------------
def build_rp2():
    dmask = 0
    for i in COLORS:
        for j in COLORS:
            dmask |= bit(("d", i, j))
    equations = []
    for word in product((1, 2), repeat=6):
        w = tuple(word)
        for i, j in product((1, 2), repeat=2):
            literal = row(i, j, w)
            star = kill(literal, dmask)
            direct = {m: c for m, c in literal.items() if m & dmask}
            expect = pmul(pvar(("d", i, j)), haf_word(SITES, w))
            require(direct == expect,
                    ("the direct term of a two-colour row is not d*haf", i, j, w))
            poly = dict(star)
            t = ghz_target(i, j, w)
            if t:
                poly[0] = poly.get(0, 0) - t
                if not poly[0]:
                    del poly[0]
            if poly:
                equations.append(((i, j, w), poly))
        h = haf_word(SITES, w)
        if h:
            equations.append((("haf", w), dict(h)))
    return equations


def audit_rp2_census(equations):
    live = 0
    for _, poly in equations:
        for m in poly:
            live |= m
    names = sorted(var_of_bit(b) for b in bits(live))
    require(len(equations) == 288, ("RP2 equation count changed", len(equations)))
    require(len(names) == 78, ("RP2 unknown count changed", len(names)))
    kinds = {}
    for v in names:
        kinds[v[0]] = kinds.get(v[0], 0) + 1
    require(kinds == {"q": 30, "p": 24, "s": 24},
            ("RP2 unknown split changed", kinds))
    for v in names:
        require(v[0] != "d", "RP2 still carries a direct-block unknown")
        if v[0] == "q":
            require(v[1] in (1, 2), "RP2 still carries a colour-0 edge")
        else:
            require(v[1] in (1, 2) and v[3] in (1, 2),
                    ("RP2 still carries a label-0 or colour-0 star entry", v))


# --------------------------------------------------------------------------
# the monomial branching decision procedure (sound over every field)
# --------------------------------------------------------------------------
def decide(equations, zeros=0, nonzero=0, cap=200000):
    """Rules, all valid over any field:  drop monomials hitting a zero variable;
    close on a nonzero constant; close on a single monomial all of whose
    variables are known nonzero; force the last undetermined variable of a single
    monomial to zero; make a two-term equation with one known-nonzero side force
    the other side's variables nonzero; branch on a single monomial's factors as
    disjoint cases; otherwise branch one variable zero / nonzero."""
    stack = [(zeros, nonzero, equations)]
    seen = set()
    nodes = 0
    open_leaves = 0
    while stack:
        z, nz, eqs = stack.pop()
        if (z, nz) in seen:
            continue
        seen.add((z, nz))
        nodes += 1
        if nodes > cap:
            return ("capped", nodes, open_leaves)
        closed = False
        live = []
        while True:
            freshz = 0
            freshn = 0
            live = []
            for lab, poly in eqs:
                red = {m: c for m, c in poly.items() if not (m & z)}
                if not red:
                    continue
                if len(red) == 1:
                    m = next(iter(red))
                    f = m & ~nz
                    if f == 0:
                        closed = True
                        break
                    if f & (f - 1) == 0:
                        freshz |= f
                elif len(red) == 2:
                    m1, m2 = tuple(red)
                    if not (m1 & ~nz):
                        freshn |= m2 & ~nz
                    elif not (m2 & ~nz):
                        freshn |= m1 & ~nz
                live.append((lab, red))
            if closed:
                break
            if (freshz & nz) or (freshn & z) or (freshz & freshn):
                closed = True
                break
            newz = freshz & ~z
            newn = freshn & ~nz
            if not newz and not newn:
                break
            z |= newz
            nz |= newn
            eqs = live
        if closed:
            continue
        best = None
        bestn = 99
        for _, red in live:
            if len(red) == 1:
                f = next(iter(red)) & ~nz
                n = bin(f).count("1")
                if n < bestn:
                    bestn = n
                    best = f
        if best is not None:
            acc = 0
            for lb in bits(best):
                stack.append((z | lb, nz | acc, live))
                acc |= lb
            continue
        freq = {}
        for _, red in live:
            weight = 1000000 // (len(red) ** 2)
            for m in red:
                mask = m & ~nz
                while mask:
                    low = mask & -mask
                    mask ^= low
                    freq[low] = freq.get(low, 0) + weight
        if not freq:
            open_leaves += 1
            return ("open", nodes, open_leaves)
        pick = max(sorted(freq), key=lambda b: freq[b])
        stack.append((z | pick, nz, live))
        stack.append((z, nz | pick, live))
    return ("closed" if not open_leaves else "open", nodes, open_leaves)


RP2_WITNESS = {("q", 1, 1, 2): Q(1), ("q", 1, 3, 4): Q(1),
               ("q", 2, 0, 1): Q(1), ("q", 2, 2, 3): Q(1),
               ("p", 1, 0, 1): Q(1), ("p", 2, 5, 2): Q(1),
               ("s", 2, 4, 2): Q(1), ("s", 1, 5, 1): Q(1)}


def audit_rp2_is_satisfiable(equations):
    """RP2 has an explicit integer solution, so it does NOT close the rank-two
    branch: everything the branch still contains lives in the colour-0 and
    label-0 sector.  The witness is the alternating eight-cycle with its two
    endpoints at cycle distance two, which carries no direct edge at all."""
    for lab, poly in equations:
        require(evaluate(poly, RP2_WITNESS) == 0,
                ("the RP2 witness fails an RP2 equation", lab))
    # it is a genuine packet of the full chart, failing exactly one row
    ledger = []
    for word in product(COLORS, repeat=6):
        for i, j in product(COLORS, repeat=2):
            value = evaluate(row(i, j, word), RP2_WITNESS) - ghz_target(i, j, word)
            if value:
                ledger.append((i, j, word, value))
    require(sorted(ledger) == [(0, 0, (0,) * 6, Q(-1))],
            ("the RP2 witness does not fail exactly the colour-0 anchor",
             sorted(ledger)))
    require(all(k[0] != "d" for k in RP2_WITNESS),
            "the RP2 witness uses a direct scalar")


# --------------------------------------------------------------------------
# 8.  the alternating eight-cycle guard is a family, and none of it completes
# --------------------------------------------------------------------------
CYCLE_COLOURS = (1, 2)
FREE_COLOUR = 0


def cycle_packet(u, v, shift):
    """The alternating monochromatic eight-cycle 0-1-...-7-0 in colours 1,2 with
    the two endpoints placed at cycle vertices u and v."""
    sites = [k for k in range(8) if k not in (u, v)]
    seat = {k: n for n, k in enumerate(sites)}
    point = {}
    for k in range(8):
        a, b = k, (k + 1) % 8
        c = CYCLE_COLOURS[(k + shift) % 2]
        if a in (u, v) and b in (u, v):
            point[("d", c, c)] = Q(1)
        elif a == u or b == u:
            x = b if a == u else a
            point[("p", c, seat[x], c)] = Q(1)
        elif a == v or b == v:
            x = b if a == v else a
            point[("s", c, seat[x], c)] = Q(1)
        else:
            lo, hi = sorted((seat[a], seat[b]))
            point[("q", c, lo, hi)] = Q(1)
    return point


def audit_cycle_family(system):
    """Every placement of the two endpoints on the alternating eight-cycle gives
    a monochromatic packet satisfying 6560 of the 6561 equations, failing only
    the third colour's anchor.  The committed guard is the distance-one member,
    the only one that uses the direct edge."""
    seen = {}
    for u, v in combinations(range(8), 2):
        for shift in (0, 1):
            point = cycle_packet(u, v, shift)
            ledger = sorted((i, j, word, value)
                            for (i, j, word), poly in system.items()
                            for value in (evaluate(poly, point),) if value)
            require(ledger == [(FREE_COLOUR, FREE_COLOUR,
                                (FREE_COLOUR,) * 6, Q(-1))],
                    ("an eight-cycle placement does not fail exactly the free "
                     "colour's anchor", u, v, shift, ledger))
            distance = min((v - u) % 8, (u - v) % 8)
            uses_direct = any(k[0] == "d" for k in point)
            seen.setdefault(distance, set()).add(uses_direct)
    require(sorted(seen) == [1, 2, 3, 4],
            ("the endpoint distance census changed", sorted(seen)))
    require(seen[1] == {True} and seen[2] == {False}
            and seen[3] == {False} and seen[4] == {False},
            ("only the distance-one placement should use the direct edge", seen))


def freeze(point):
    """Substitute the frozen colour-1/colour-2 entries; leave q_0, p_i(x,0),
    s_j(y,0) and all nine direct scalars free."""
    equations = []
    for word in product(COLORS, repeat=6):
        for i, j in product(COLORS, repeat=2):
            out = {}
            for m, c in row(i, j, word).items():
                coefficient = c
                mask = 0
                for b in bits(m):
                    key = var_of_bit(b)
                    frozen = ((key[0] == "q" and key[1] in CYCLE_COLOURS)
                              or (key[0] in ("p", "s") and key[3] in CYCLE_COLOURS))
                    if frozen:
                        coefficient *= point.get(key, Q(0))
                        if coefficient == 0:
                            break
                    else:
                        mask |= b
                if coefficient == 0:
                    continue
                out[mask] = out.get(mask, 0) + coefficient
            out = {m: c for m, c in out.items() if c}
            t = ghz_target(i, j, word)
            if t:
                out[0] = out.get(0, 0) - t
                if not out[0]:
                    del out[0]
            if out:
                equations.append(((i, j, word), out))
    return equations


def audit_cycle_completions():
    """Freeze each placement's colour-1/colour-2 sector, free the whole colour-0
    sector and all nine direct scalars, and decide the 9x729 rows.  Every one of
    the 56 frozen systems closes with no open leaf; every coefficient is +-1, so
    the closures are characteristic-independent.  This generalizes the committed
    slice-specific statement from one placement to all of them."""
    nodes_seen = set()
    for u, v in combinations(range(8), 2):
        for shift in (0, 1):
            equations = freeze(cycle_packet(u, v, shift))
            live = 0
            coefficients = set()
            for _, poly in equations:
                for m, c in poly.items():
                    live |= m
                    coefficients.add(c)
            require(len(bits(live)) == 60,
                    ("the frozen unknown count changed", u, v, shift,
                     len(bits(live))))
            require(coefficients == {1, -1},
                    ("a frozen system has a coefficient other than +-1",
                     u, v, shift, sorted(coefficients)))
            status, nodes, leaves = decide(equations, cap=20000)
            require(status == "closed" and leaves == 0,
                    ("an eight-cycle completion did not close", u, v, shift,
                     status))
            nodes_seen.add(nodes)
    require(max(nodes_seen) <= 27,
            ("a completion took more branch nodes than recorded",
             sorted(nodes_seen)))


def main():
    audit_normalization()
    system = build_system()
    audit_guard_ledgers(system)
    hfull, hhole = audit_colour_pencil_identity(system)
    audit_pencil_laplace(hfull, hhole)
    audit_pencil_nondegeneracy(hhole)
    audit_blind_label_pencil()
    rp2 = build_rp2()
    audit_rp2_census(rp2)
    audit_rp2_is_satisfiable(rp2)
    audit_cycle_family(system)
    audit_cycle_completions()
    print(
        "PASS: colour pencil form verified -- both committed guard ledgers are "
        "reproduced; the colour pencil identity (G') holds as a formal identity "
        "in lam and in all 162 unknowns on all nine label pairs, so the whole "
        "9x729 system implies the single matrix identity haf(Q_lam) d + X^lam "
        "H(Q_lam) (Y^lam)^T = diag(lam_0^6,lam_1^6,lam_2^6) as the colour-census "
        "aggregate of the 6561 rows; the pencil Laplace "
        "expansion holds at every site, giving T6: H(Q_lam) != 0 for every "
        "lam != 0, whose coordinate case is T2 and whose corollary is the linear "
        "independence of q_0,q_1,q_2 (both committed guards violate T6 exactly "
        "at the colours whose anchors they fail); a blind label reduces row j0 "
        "of (G') to haf(Q_lam) d_{j0 j} = delta_{j0 j} lam_{j0}^6; and the "
        "rank-two branch reduces to RP2, a two-colour star-only residual of 288 "
        "equations in 78 unknowns with no direct block, which is SATISFIABLE "
        "over Z -- so that reduction is sharp and the branch's remaining "
        "content is exactly its colour-0 and label-0 sector; finally the "
        "alternating eight-cycle guard is a family of 56 placements, each "
        "failing only the third colour's anchor and only the distance-one "
        "member using the direct edge, and every one of the 56 frozen "
        "completion problems (60 unknowns, all coefficients +-1) closes with no "
        "open leaf in at most 27 branch nodes, over any field"
    )


if __name__ == "__main__":
    main()
