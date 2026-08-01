#!/usr/bin/env python3
"""The all-word four-hole form of the physical rows, and the grade ladder.

Attack line 2 of ``notes/terminal-bianchi-handoff-guide.md`` asks which
response grades of the four-hole vector the physical rows control, and where
they stop.  This checker settles both halves.

  A1  ALL-WORD IDENTITY (formal, all 729 words x 9 label pairs).  With
      q^w(x,y) = q(x,y,w_x,w_y), R^w_ij(x,y) = p_i(x,w_x)s_j(y,w_y) +
      p_i(y,w_y)s_j(x,w_x) and H(A)_e = haf(A[W\\e]),

          Row(i,j,w) = < (d_ij/3) q^w + R^w_ij , H(q^w) >,

      the pure-word statement verbatim.  Proof: the direct term is
      d_ij*haf(q^w) and <q^w,H(q^w)> = 3*haf(q^w) (Euler for the hafnian, one
      line: every perfect matching is recovered once from each of its three
      edges).  Nothing about colour is used, so the identity survives
      cross-colour internal edges; it is verified formally in both models.

  A2  CLASS FACTORIZATION (formal, monochromatic q only).  A word has 0 or 2
      odd colour classes.  For the 183 all-even words the row splits as a sum
      over colours of a class-restricted cap pairing times the hafnians of the
      other classes; for the 546 two-odd words the direct term dies and the
      row is the even class hafnian times a bilinear product of two one-hole
      star functionals.  Cross-colour edges break exactly this refinement, and
      the break is quantified.

  B1  R-AFFINENESS (formal).  Every monomial of every one of the 2 x 6561 row
      polynomials has p-degree <= 1, s-degree <= 1 and p-degree = s-degree.
      So a row is a *grade-0* four-hole pairing and nothing else, while
      chi = (alpha/2)<R,H_1> + (1/3)<R,H_2> is R-quadratic and R-cubic.

  B2  WEIGHT GRADING (formal).  Give q weight -1, p and s weight +1, d weight
      +3.  Every row monomial has weight 0; hence the substitution
      q -> q/tau, p -> tau p, s -> tau s, d -> tau^3 d fixes every coefficient
      of the eight-site matching tensor.  In the same weighting Q_k has weight
      3k-3, H_k has weight 3k-2, the jet J_k has weight 3k, and chi has weight
      6.  Therefore no function of the physical row values can equal chi, Q_2,
      Q_3, J_1, J_2 or J_3 except where those vanish: a landing theorem can
      only ever be a vanishing statement, never a formula, and no bound of the
      form |chi| <= Phi(row residuals) can hold.

  B3  THE GUARD IS A ONE-PARAMETER FAMILY.  All 105 = 7!! perfect matchings of
      the eight vertices have weight zero -- each is either the direct edge
      plus three internal edges or one star edge at each endpoint plus two
      internal edges -- so *every* chart of the array is fixed by the
      substitution, for every packet and every tau != 0; the deleted-pair chart
      that produces the 9 x 729 rows and the literal adjacent 27-row chart are
      both re-derived from their own code under a positive-coefficient probe
      and each collects all 105 matchings at exponent zero.  Applied to the audited
      seven-row guard it therefore preserves the eight-site matching tensor
      (still X_2), the whole GHZ residual ledger (still -X_0 at 00 and -X_1 at
      11), the rank-three endpoint stars, every Segre rectangle, the adjacent
      27-row decomposition and the all-word vanishing of the selected 01 row --
      all of it re-checked numerically at tau = 1, 2, -3, 1/2 -- while
      chi = -2 tau^6 runs over -2, -128, -1458, -1/32.

  C   THE PINNED RESIDUAL.  haf(alpha q + R) = alpha^2 * (alpha Q_0 + Q_1) +
      chi, and alpha Q_0 + Q_1 is literally the pure-word row value.  So for a
      selected row (i,j) at colour c, with alpha = d_ij,

          chi = haf(d_ij q_c + R^c_ij) - d_ij^2 * Row(i,j,c^6),

      an exact expression of chi as a row combination plus a residual; by B1
      and B2 that residual sits at four-hole grades 1 and 2, which no row
      controls.

Standard probes (handoff guide, section 5): the rank-two clean packet and the
seven-row chi=-2 guard are both exercised.  Everything here is an identity or
a negative (guard) statement, so both probes must and do pass.

No certified dependency is changed; Krenn's conjecture remains open.  Python
standard library only, exact Fraction arithmetic, deterministic, live under
``python -O``.
"""

from fractions import Fraction as Q
from itertools import combinations, permutations, product


def require(condition, message):
    if not condition:
        raise AssertionError(message)


COLORS = (0, 1, 2)
SITES = tuple(range(6))
PAIRS = tuple(combinations(SITES, 2))
LEFT, RIGHT = 6, 7
PURE = 2

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
# minimal exact sparse polynomial ring; a monomial is a sorted tuple of keys
# --------------------------------------------------------------------------
ONE = {(): Q(1)}


def var(key):
    return {(key,): Q(1)}


def padd(left, right):
    out = dict(left)
    for monomial, coefficient in right.items():
        total = out.get(monomial, Q(0)) + coefficient
        if total:
            out[monomial] = total
        elif monomial in out:
            del out[monomial]
    return out


def pmul(left, right):
    out = {}
    for m1, c1 in left.items():
        for m2, c2 in right.items():
            monomial = tuple(sorted(m1 + m2))
            total = out.get(monomial, Q(0)) + c1 * c2
            if total:
                out[monomial] = total
            elif monomial in out:
                del out[monomial]
    return out


def pscale(poly, factor):
    if not factor:
        return {}
    return {monomial: coefficient * factor for monomial, coefficient in poly.items()}


# --------------------------------------------------------------------------
# the symbolic packet: colour-decorated internal quadratic, endpoint stars,
# direct scalars.  Model copied from
# computations/verify_h3_diagonal_segre_second_transgression_seven_row_guard.py
# --------------------------------------------------------------------------
ALLOW_CROSS = [False]


def q_var(x, y, cx, cy):
    if x > y:
        x, y = y, x
        cx, cy = cy, cx
    if cx != cy:
        if ALLOW_CROSS[0]:
            return var(("X", x, y, cx, cy))
        return {}
    return var(("q", cx, x, y))


def p_var(i, x, c):
    return var(("p", i, x, c))


def s_var(j, y, c):
    return var(("s", j, y, c))


def d_var(i, j):
    return var(("d", i, j))


_HAF = {}


def haf_poly(sites, word):
    """haf(q^w[sites]) as a polynomial, cached on (sites, colours on sites)."""
    sites = tuple(sites)
    key = (ALLOW_CROSS[0], sites, tuple(word[x] for x in sites))
    cached = _HAF.get(key)
    if cached is not None:
        return cached
    total = {}
    for matching in matchings(sites):
        term = ONE
        for x, y in matching:
            term = pmul(term, q_var(x, y, word[x], word[y]))
            if not term:
                break
        total = padd(total, term)
    _HAF[key] = total
    return total


def four_hole(word):
    """H(q^w)_e = haf(q^w[W\\e]) for the fifteen pairs."""
    return {e: haf_poly(tuple(v for v in SITES if v not in e), word) for e in PAIRS}


_RESPONSE = {}


def response(i, j, x, y, word):
    key = (i, j, x, y, word[x], word[y])
    cached = _RESPONSE.get(key)
    if cached is None:
        cached = padd(pmul(p_var(i, x, word[x]), s_var(j, y, word[y])),
                      pmul(p_var(i, y, word[y]), s_var(j, x, word[x])))
        _RESPONSE[key] = cached
    return cached


def row_poly(i, j, word, holes):
    """d_ij*haf(q^w) + sum_e R^w_ij(e)*haf(q^w[W\\e]) -- the literal row."""
    total = pmul(d_var(i, j), haf_poly(SITES, word))
    for x, y in PAIRS:
        piece = holes[(x, y)]
        if not piece:
            continue
        term = response(i, j, x, y, word)
        if term:
            total = padd(total, pmul(term, piece))
    return total


def cap_pairing(i, j, word, holes):
    """< (d_ij/3) q^w + R^w_ij , H(q^w) >."""
    total = {}
    for x, y in PAIRS:
        piece = holes[(x, y)]
        if not piece:
            continue
        cap = padd(pscale(pmul(d_var(i, j), q_var(x, y, word[x], word[y])), Q(1, 3)),
                   response(i, j, x, y, word))
        if cap:
            total = padd(total, pmul(cap, piece))
    return total


# --------------------------------------------------------------------------
# 1.  normalization
# --------------------------------------------------------------------------
def audit_normalization():
    ones = {e: Q(1) for e in PAIRS}

    def plain(sites, entries):
        total = Q(0)
        for matching in matchings(tuple(sites)):
            term = Q(1)
            for x, y in matching:
                term *= entries[(min(x, y), max(x, y))]
            total += term
        return total

    require(plain(SITES, ones) == 15, "all-ones six-site hafnian is not 15")
    require(plain((0, 1, 2, 3), ones) == 3, "all-ones four-site hafnian is not 3")
    polar = {e: plain(tuple(v for v in SITES if v not in e), ones) for e in PAIRS}
    require(polar[(0, 1)] == 3, "all-ones polar entry is not 3")
    require(plain((2, 3, 4, 5), polar) == 27, "all-ones double polar is not 27")
    # cross-star B_ij of notes/three-anchor-apolar-double-polar-bianchi-reduction.md
    outside = (2, 3, 4, 5)
    cross_star = Q(0)
    for selected in combinations(outside, 2):
        term = Q(1)
        for site in selected:
            term *= ones[(min(0, site), max(0, site))]
        for site in outside:
            if site not in selected:
                term *= ones[(min(1, site), max(1, site))]
        cross_star += term
    require(cross_star == 6 and 27 - 15 * 1 == 2 * cross_star == 12,
            ("all-ones cross-star defect is not 12", cross_star))
    # Euler's identity on the all-ones array: <A,H(A)> = 3 haf(A).
    require(sum(ones[e] * polar[e] for e in PAIRS) == 3 * 15, "Euler failed on all ones")


# --------------------------------------------------------------------------
# 2.  A1/B1/B2: the all-word identity, R-affineness and the weight grading
# --------------------------------------------------------------------------
WEIGHT = {"q": -1, "X": -1, "p": 1, "s": 1, "d": 3}


def audit_allword_identity_and_weights():
    counts = {}
    for cross in (False, True):
        ALLOW_CROSS[0] = cross
        checked = 0
        for word in product(COLORS, repeat=6):
            holes = four_hole(word)
            for i, j in product(COLORS, repeat=2):
                literal = row_poly(i, j, word, holes)
                require(literal == cap_pairing(i, j, word, holes),
                        ("all-word four-hole identity failed", cross, i, j, word))
                for monomial in literal:
                    require(sum(WEIGHT[key[0]] for key in monomial) == 0,
                            ("a row monomial is not weight zero", cross, i, j, word,
                             monomial))
                    stars = sum(1 for key in monomial if key[0] == "p")
                    costars = sum(1 for key in monomial if key[0] == "s")
                    require(stars == costars <= 1,
                            ("a row monomial is not response-affine", cross, i, j,
                             word, monomial))
                checked += 1
        counts[cross] = checked
    ALLOW_CROSS[0] = False
    require(counts == {False: 9 * 729, True: 9 * 729}, ("row count changed", counts))


# --------------------------------------------------------------------------
# 3.  A2: class factorization, and the exact scope of the refinement
# --------------------------------------------------------------------------
_MONO = {}


def mono_haf(sites, colour):
    """haf(q_colour[sites]) -- one colour, monochromatic edges."""
    sites = tuple(sites)
    cached = _MONO.get((sites, colour))
    if cached is not None:
        return cached
    total = {}
    for matching in matchings(sites):
        term = ONE
        for x, y in matching:
            term = pmul(term, var(("q", colour, min(x, y), max(x, y))))
        total = padd(total, term)
    _MONO[(sites, colour)] = total
    return total


def restricted_cap_pairing(i, j, sites, colour):
    """< (d_ij/3) q_c + R^c_ij , H_0 >  restricted to pairs inside one class."""
    total = {}
    for x, y in combinations(sites, 2):
        piece = mono_haf(tuple(v for v in sites if v not in (x, y)), colour)
        if not piece:
            continue
        cap = padd(pscale(pmul(d_var(i, j), var(("q", colour, x, y))), Q(1, 3)),
                   padd(pmul(p_var(i, x, colour), s_var(j, y, colour)),
                        pmul(p_var(i, y, colour), s_var(j, x, colour))))
        if cap:
            total = padd(total, pmul(cap, piece))
    return total


def one_hole_functional(maker, label, sites, colour):
    """sum_{x in S} v_label(x,c) * haf(q_c[S\\{x}]) -- odd-class star functional."""
    total = {}
    for x in sites:
        piece = mono_haf(tuple(v for v in sites if v != x), colour)
        if piece:
            total = padd(total, pmul(maker(label, x, colour), piece))
    return total


def audit_class_factorization():
    ALLOW_CROSS[0] = False
    even_words = 0
    odd_words = 0
    for word in product(COLORS, repeat=6):
        classes = {c: tuple(x for x in SITES if word[x] == c) for c in COLORS}
        odd = tuple(c for c in COLORS if len(classes[c]) % 2)
        require(len(odd) in (0, 2), ("impossible class parity", word, odd))

        product_of_classes = ONE
        for c in COLORS:
            product_of_classes = pmul(product_of_classes, mono_haf(classes[c], c))
        require(haf_poly(SITES, word) == product_of_classes,
                ("class factorization of the hafnian failed", word))

        holes = four_hole(word)
        if not odd:
            even_words += 1
            for i, j in product(COLORS, repeat=2):
                expected = {}
                for c in COLORS:
                    if len(classes[c]) < 2:
                        continue
                    others = ONE
                    for other in COLORS:
                        if other != c:
                            others = pmul(others, mono_haf(classes[other], other))
                    if not others:
                        continue
                    expected = padd(expected,
                                    pmul(restricted_cap_pairing(i, j, classes[c], c),
                                         others))
                require(row_poly(i, j, word, holes) == expected,
                        ("even-word class form failed", i, j, word))
        else:
            odd_words += 1
            first, second = odd
            even = next(c for c in COLORS if c not in odd)
            bulk = mono_haf(classes[even], even)
            for i, j in product(COLORS, repeat=2):
                left = pmul(one_hole_functional(p_var, i, classes[first], first),
                            one_hole_functional(s_var, j, classes[second], second))
                right = pmul(one_hole_functional(p_var, i, classes[second], second),
                             one_hole_functional(s_var, j, classes[first], first))
                expected = pmul(bulk, padd(left, right))
                require(row_poly(i, j, word, holes) == expected,
                        ("odd-word star-product form failed", i, j, word))
    require((even_words, odd_words) == (183, 546),
            ("word parity census changed", even_words, odd_words))


def audit_cross_colour_break():
    """Exactly what cross-colour internal edges destroy, and what they do not."""
    ALLOW_CROSS[0] = False
    mono = {word: haf_poly(SITES, word) for word in product(COLORS, repeat=6)}
    witness = (0, 0, 0, 1, 1, 2)     # classes of sizes 3, 2, 1: two odd
    witness_holes = four_hole(witness)
    mono_rows = {(i, j, witness): row_poly(i, j, witness, witness_holes)
                 for i, j in product(COLORS, repeat=2)}

    ALLOW_CROSS[0] = True
    census = {}
    for word in product(COLORS, repeat=6):
        cross = haf_poly(SITES, word)
        require(len(cross) == 15, ("a cross-colour hafnian lost a matching", word))
        classes = {c: tuple(x for x in SITES if word[x] == c) for c in COLORS}
        odd = tuple(c for c in COLORS if len(classes[c]) % 2)
        surviving = len(mono[word])
        require(bool(odd) == (surviving == 0),
                ("class parity does not match hafnian support", word))
        census[surviving] = census.get(surviving, 0) + 1
    # of the fifteen matching monomials the monochromatic model keeps 0 (the 546
    # two-odd words), 1 (the ninety (2,2,2) words), 3 (the ninety (4,2,0) words)
    # or 15 (the three pure words); the cross-colour model always keeps all 15.
    require(sorted(census.items()) == [(0, 546), (1, 90), (3, 90), (15, 3)],
            ("cross-colour hafnian census changed", sorted(census.items())))

    # On a two-odd word the monochromatic row has no direct term at all; with a
    # cross-colour edge the direct term revives, so the star-product form dies.
    holes = four_hole(witness)
    revived_rows = 0
    for i, j in product(COLORS, repeat=2):
        literal = row_poly(i, j, witness, holes)
        require(literal != mono_rows[(i, j, witness)],
                ("cross-colour witness row did not move", i, j))
        direct = [m for m in literal if any(key[0] == "d" for key in m)]
        require(direct, ("the revived direct term is missing", i, j))
        require(not [m for m in mono_rows[(i, j, witness)]
                     if any(key[0] == "d" for key in m)],
                ("the monochromatic two-odd row had a direct term", i, j))
        revived_rows += 1
    require(revived_rows == 9, "cross-colour witness census changed")
    ALLOW_CROSS[0] = False


# --------------------------------------------------------------------------
# 4.  the grade ladder on thirty formal edge variables and a formal alpha
# --------------------------------------------------------------------------
ALPHA = var(("a",))


def edge_var(tag, e):
    return var((tag, e[0], e[1]))


def graded_layers():
    layers = [{} for _ in range(4)]
    for matching in matchings(SITES):
        for flags in product((0, 1), repeat=3):
            term = ONE
            for flag, e in zip(flags, matching):
                term = pmul(term, edge_var("R" if flag else "q", e))
            layers[sum(flags)] = padd(layers[sum(flags)], term)
    return layers


def graded_holes(e):
    rest = tuple(v for v in SITES if v not in e)
    layers = [{} for _ in range(3)]
    for matching in matchings(rest):
        for flags in product((0, 1), repeat=2):
            term = ONE
            for flag, f in zip(flags, matching):
                term = pmul(term, edge_var("R" if flag else "q", f))
            layers[sum(flags)] = padd(layers[sum(flags)], term)
    return layers


LADDER_WEIGHT = {"q": -1, "R": 2, "a": 3}


def homogeneous_weight(poly, name):
    weights = {sum(LADDER_WEIGHT[key[0]] for key in monomial) for monomial in poly}
    require(len(weights) == 1, ("not weight homogeneous", name, sorted(weights)))
    return weights.pop()


def audit_grade_ladder():
    layers = graded_layers()
    holes = {e: graded_holes(e) for e in PAIRS}

    def contract(tag, grade):
        total = {}
        for e in PAIRS:
            total = padd(total, pmul(edge_var(tag, e), holes[e][grade]))
        return total

    for k in range(3):
        require(contract("R", k) == pscale(layers[k + 1], Q(k + 1)),
                ("<R,H_k> = (k+1)Q_{k+1} failed", k))
        require(contract("q", k) == pscale(layers[k], Q(3 - k)),
                ("<q,H_k> = (3-k)Q_k failed", k))

    chi = padd(pmul(ALPHA, layers[2]), layers[3])
    require(chi == padd(pscale(pmul(ALPHA, contract("R", 1)), Q(1, 2)),
                        pscale(contract("R", 2), Q(1, 3))),
            "chi = (alpha/2)<R,H_1> + (1/3)<R,H_2> failed")

    # the only grade-1 contraction of weight zero is not new information
    require(contract("q", 1) == pscale(contract("R", 0), Q(2)),
            "<q,H_1> = 2<R,H_0> failed")

    def cap(e):
        return padd(pmul(ALPHA, edge_var("q", e)), edge_var("R", e))

    cap_haf = {}
    for matching in matchings(SITES):
        term = ONE
        for e in matching:
            term = pmul(term, cap(e))
        cap_haf = padd(cap_haf, term)
    source = padd(pmul(ALPHA, layers[0]), layers[1])
    require(cap_haf == padd(pmul(pmul(ALPHA, ALPHA), source), chi),
            "haf(A_cap) = alpha^2 * J_0 + chi failed")

    for e in PAIRS:
        rest = tuple(v for v in SITES if v not in e)
        value = {}
        for matching in matchings(rest):
            term = ONE
            for f in matching:
                term = pmul(term, cap(f))
            value = padd(value, term)
        require(value == padd(pmul(pmul(ALPHA, ALPHA), holes[e][0]),
                              padd(pmul(ALPHA, holes[e][1]), holes[e][2])),
                ("H(A_cap) = alpha^2 H_0 + alpha H_1 + H_2 failed", e))

    # the blindness ledger of notes/fourhole-cap-polarization-terminal-blindness.md
    cap_holes = {}
    for e in PAIRS:
        cap_holes[e] = padd(pmul(pmul(ALPHA, ALPHA), holes[e][0]),
                            padd(pmul(ALPHA, holes[e][1]), holes[e][2]))

    def cap_contract(tag):
        total = {}
        for e in PAIRS:
            total = padd(total, pmul(edge_var(tag, e), cap_holes[e]))
        return total

    require(cap_contract("R") == padd(pmul(pmul(ALPHA, ALPHA), layers[1]),
                                      padd(pscale(pmul(ALPHA, layers[2]), Q(2)),
                                           pscale(layers[3], Q(3)))),
            "<R,H(A_cap)> ledger failed")
    require(cap_contract("q") == padd(pscale(pmul(pmul(ALPHA, ALPHA), layers[0]), Q(3)),
                                      padd(pscale(pmul(ALPHA, layers[1]), Q(2)),
                                           layers[2])),
            "<q,H(A_cap)> ledger failed")

    # weights: Q_k = 3k-3, H_k = 3k-2, J_k = 3k, chi = 6, rows = 0
    require([homogeneous_weight(layers[k], "Q%d" % k) for k in range(4)]
            == [-3, 0, 3, 6], "layer weights changed")
    require([homogeneous_weight(holes[(0, 1)][k], "H%d" % k) for k in range(3)]
            == [-2, 1, 4], "four-hole grade weights changed")
    jets = [source,
            padd(pmul(ALPHA, layers[1]), pscale(layers[2], Q(2))),
            padd(pmul(ALPHA, layers[2]), pscale(layers[3], Q(3))),
            pmul(ALPHA, layers[3])]
    require([homogeneous_weight(jets[k], "J%d" % k) for k in range(4)]
            == [0, 3, 6, 9], "jet weights changed")
    require(homogeneous_weight(chi, "chi") == 6, "chi weight changed")
    require([homogeneous_weight(contract("R", k), "<R,H%d>" % k) for k in range(3)]
            == [0, 3, 6], "response contraction weights changed")
    require([homogeneous_weight(contract("q", k), "<q,H%d>" % k) for k in range(3)]
            == [-3, 0, 3], "internal contraction weights changed")

    # The response grades of the double-polar covariant.  By the audited
    # identity P(A) = H(H(A)) - 2B(A) = F(A)A of
    # notes/three-anchor-apolar-double-polar-bianchi-reduction.md, equation (6),
    # C_k = [t^k]P(q+tR) = Q_k q + Q_{k-1} R.  Each entry (here the 01 entry)
    # is weight 3k-4, and 3k-4 = 0 has no integer solution: no response grade
    # of the double-polar identity is weight zero, so no row sits on any.
    for k in range(5):
        component = {}
        if k <= 3:
            component = padd(component, pmul(layers[k], edge_var("q", (0, 1))))
        if k >= 1:
            component = padd(component, pmul(layers[k - 1], edge_var("R", (0, 1))))
        require(homogeneous_weight(component, "C%d" % k) == 3 * k - 4,
                ("double-polar grade weight changed", k))


# --------------------------------------------------------------------------
# 5.  numeric packet machinery (both standard probes)
# --------------------------------------------------------------------------
def numeric_haf(sites, entries):
    total = Q(0)
    for matching in matchings(tuple(sites)):
        term = Q(1)
        for x, y in matching:
            term *= entries[(min(x, y), max(x, y))]
            if not term:
                break
        total += term
    return total


def numeric_layers(q, r):
    layers = [Q(0)] * 4
    for matching in matchings(SITES):
        for flags in product((0, 1), repeat=3):
            term = Q(1)
            for flag, (x, y) in zip(flags, matching):
                term *= (r if flag else q)[(x, y)]
            layers[sum(flags)] += term
    return tuple(layers)


def permanent(rows, columns, entries):
    total = Q(0)
    for assigned in permutations(columns):
        term = Q(1)
        for row, column in zip(rows, assigned):
            term *= entries[(min(row, column), max(row, column))]
        total += term
    return total


def theta(marked, a, b, q):
    """Copied from verify_three_anchor_apolar_double_polar_bianchi_reduction.py."""
    marked = tuple(sorted(marked))
    outside = tuple(x for x in SITES if x not in marked)
    value = Q(0)
    for inside in combinations(marked, 2):
        remaining = next(x for x in marked if x not in inside)
        for endpoint in outside:
            rest = tuple(x for x in outside if x != endpoint)
            value += (a[inside]
                      * b[(min(remaining, endpoint), max(remaining, endpoint))]
                      * q[rest])
    return value + permanent(marked, outside, b)


def audit_rank_two_clean_packet():
    """Standard probe one: the clean packet of the handoff guide, section 3."""
    q = {e: Q(0) for e in PAIRS}
    for e in ((0, 1), (2, 3), (4, 5)):
        q[e] = Q(1)
    u = (1, -1, 2, 0, 1, 1)
    v = (1, 2, -2, 1, -2, 1)
    r = {(x, y): Q(u[x] * v[y] + v[x] * u[y]) for x, y in PAIRS}
    alpha = Q(-2)
    layers = numeric_layers(q, r)
    require(layers == (Q(1), Q(2), Q(6), Q(12)), ("clean packet layers changed", layers))
    require(alpha * layers[0] + layers[1] == 0, "clean packet source row changed")
    chi = alpha * layers[2] + layers[3]
    require(chi == 0, ("the clean packet stopped being clean", chi))

    holes = {}
    for e in PAIRS:
        rest = tuple(x for x in SITES if x not in e)
        holes[e] = [Q(0)] * 3
        for matching in matchings(rest):
            for flags in product((0, 1), repeat=2):
                term = Q(1)
                for flag, f in zip(flags, matching):
                    term *= (r if flag else q)[f]
                holes[e][sum(flags)] += term
    for k in range(3):
        require(sum(r[e] * holes[e][k] for e in PAIRS) == (k + 1) * layers[k + 1],
                ("clean packet <R,H_k> failed", k))
        require(sum(q[e] * holes[e][k] for e in PAIRS) == (3 - k) * layers[k],
                ("clean packet <q,H_k> failed", k))
    require(alpha * Q(1, 2) * sum(r[e] * holes[e][1] for e in PAIRS)
            + Q(1, 3) * sum(r[e] * holes[e][2] for e in PAIRS) == chi,
            "clean packet chi grade split failed")
    cap = {e: alpha * q[e] + r[e] for e in PAIRS}
    require(numeric_haf(SITES, cap) == alpha ** 2 * (alpha * layers[0] + layers[1]) + chi,
            "clean packet cap split failed")

    # the twenty cut values of the audited note, and their weight-six behaviour
    second = {e: 2 * alpha * r[e] for e in PAIRS}
    cuts = [theta(marked, second, r, q) for marked in combinations(SITES, 3)]
    require(cuts == [Q(x) for x in (-12, -12, -12, -36, -20, 20, -28, 20, -4, -36,
                                    -44, -4, 20, -28, 20, -12, 20, 44, 52, 52)],
            ("the twenty cut values changed", cuts))
    require(sum(cuts) == 8 * chi == 0, "the twenty-cut aggregate changed")

    for tau in (Q(2), Q(-3), Q(1, 2)):
        scaled_q = {e: q[e] / tau for e in PAIRS}
        scaled_r = {e: r[e] * tau ** 2 for e in PAIRS}
        scaled_alpha = alpha * tau ** 3
        scaled = numeric_layers(scaled_q, scaled_r)
        require(all(scaled[k] == tau ** (3 * k - 3) * layers[k] for k in range(4)),
                ("clean packet layer weights failed", tau, scaled))
        require(scaled_alpha * scaled[0] + scaled[1] == 0,
                ("clean packet source row moved", tau))
        require(scaled_alpha * scaled[2] + scaled[3] == 0,
                ("clean packet stayed clean but chi moved", tau))
        scaled_second = {e: 2 * scaled_alpha * scaled_r[e] for e in PAIRS}
        for position, marked in enumerate(combinations(SITES, 3)):
            require(theta(marked, scaled_second, scaled_r, scaled_q)
                    == tau ** 6 * cuts[position],
                    ("a cut value is not weight six", tau, marked))


# --------------------------------------------------------------------------
# 6.  standard probe two: the seven-row guard, as a one-parameter family
# --------------------------------------------------------------------------
def guard_blocks(tau):
    """The audited seven-row guard packet, rescaled by the weight-zero family
    q -> q/tau, p -> tau p, s -> tau s, d -> tau^3 d.  Entries copied from
    verify_h3_diagonal_segre_second_transgression_seven_row_guard.py."""
    blocks = {}

    def put(x, y, cx, cy, value):
        if x > y:
            x, y = y, x
            cx, cy = cy, cx
        blocks[(x, y, cx, cy)] = blocks.get((x, y, cx, cy), Q(0)) + Q(value)

    internal = Q(1) / tau
    star = tau
    direct = tau ** 3
    put(0, 1, 2, 2, internal)
    put(4, 5, 2, 2, internal)
    put(LEFT, RIGHT, 0, 1, direct)
    put(LEFT, 0, 0, 2, star)
    put(LEFT, 1, 0, 2, star)
    put(LEFT, 4, 1, 2, star)
    put(LEFT, 2, 2, 2, star)
    put(LEFT, 3, 2, 2, star)
    put(RIGHT, 5, 0, 2, star)
    put(RIGHT, 2, 1, 2, star)
    put(RIGHT, 3, 1, 2, -star)
    put(RIGHT, 2, 2, 2, star * Q(1, 2))
    put(RIGHT, 3, 2, 2, star * Q(1, 2))
    return blocks


def block_edge(blocks, x, y, cx, cy):
    if x > y:
        x, y = y, x
        cx, cy = cy, cx
    return blocks.get((x, y, cx, cy), Q(0))


def block_haf(blocks, word, sites=SITES, cache=None):
    sites = tuple(sites)
    key = (sites, tuple(word[x] for x in sites))
    if cache is not None and key in cache:
        return cache[key]
    total = Q(0)
    for matching in matchings(sites):
        term = Q(1)
        for x, y in matching:
            term *= block_edge(blocks, x, y, word[x], word[y])
            if not term:
                break
        total += term
    if cache is not None:
        cache[key] = total
    return total


def block_row(blocks, i, j, word, cache=None):
    total = block_edge(blocks, LEFT, RIGHT, i, j) * block_haf(blocks, word,
                                                              cache=cache)
    for x, y in PAIRS:
        term = (block_edge(blocks, LEFT, x, i, word[x])
                * block_edge(blocks, RIGHT, y, j, word[y])
                + block_edge(blocks, LEFT, y, i, word[y])
                * block_edge(blocks, RIGHT, x, j, word[x]))
        if term:
            total += term * block_haf(blocks, word,
                                      tuple(v for v in SITES if v not in (x, y)),
                                      cache=cache)
    return total


def matrix_rank(matrix):
    work = [[Q(entry) for entry in row] for row in matrix]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((r for r in range(pivot_row, len(work)) if work[r][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for r in range(len(work)):
            if r == pivot_row or not work[r][column]:
                continue
            scale = work[r][column]
            work[r] = [entry - scale * pivot for entry, pivot
                       in zip(work[r], work[pivot_row])]
        pivot_row += 1
    return pivot_row


def response_dictionary(blocks, i, j):
    answer = {}
    for x, y in PAIRS:
        for cx, cy in product(COLORS, repeat=2):
            value = (block_edge(blocks, LEFT, x, i, cx) * block_edge(blocks, RIGHT, y, j, cy)
                     + block_edge(blocks, LEFT, y, i, cy) * block_edge(blocks, RIGHT, x, j, cx))
            if value:
                answer[((x, cx), (y, cy))] = value
    return answer


def dictionary_product(left, right):
    out = {}
    for ml, vl in left.items():
        used = {site for site, _ in ml}
        for mr, vr in right.items():
            if used.intersection(site for site, _ in mr):
                continue
            monomial = tuple(sorted(ml + mr))
            out[monomial] = out.get(monomial, Q(0)) + vl * vr
    return {m: v for m, v in out.items() if v}


def star_with_two_matchings(blocks, vertex, label, word, common):
    total = Q(0)
    for site in common:
        star = block_edge(blocks, vertex, site, label, word[site])
        if not star:
            continue
        rest = tuple(v for v in common if v != site)
        inner = Q(0)
        for matching in matchings(rest):
            term = Q(1)
            for x, y in matching:
                term *= block_edge(blocks, x, y, word[x], word[y])
            inner += term
        total += star * inner
    return total


def three_stars_one_edge(blocks, i, j, k, word, exposed, common):
    first, second, third = exposed
    total = Q(0)
    for a in common:
        va = block_edge(blocks, first, a, i, word[a])
        if not va:
            continue
        for b in common:
            if b == a:
                continue
            vb = block_edge(blocks, second, b, j, word[b])
            if not vb:
                continue
            for c in common:
                if c in (a, b):
                    continue
                vc = block_edge(blocks, third, c, k, word[c])
                if not vc:
                    continue
                rest = [s for s in common if s not in (a, b, c)]
                total += va * vb * vc * block_edge(blocks, rest[0], rest[1],
                                                   word[rest[0]], word[rest[1]])
    return total


def guard_report(blocks):
    tensor = []
    ledger = []
    cache = {}
    for word in product(COLORS, repeat=6):
        for i, j in product(COLORS, repeat=2):
            value = block_row(blocks, i, j, word, cache=cache)
            if value:
                tensor.append((i, j, word, value))
            residual = value - Q(i == j and all(c == i for c in word))
            if residual:
                ledger.append((i, j, word, residual))
        require(block_row(blocks, 0, 1, word, cache=cache) == 0,
                ("the selected 01 row is not all-word zero", word))

    stars = [[block_edge(blocks, LEFT, site, label, colour) for label in COLORS]
             for site in SITES for colour in COLORS]
    costars = [[block_edge(blocks, RIGHT, site, label, colour) for label in COLORS]
               for site in SITES for colour in COLORS]
    responses = {(i, j): response_dictionary(blocks, i, j)
                 for i, j in product(COLORS, repeat=2)}
    for i, k, j, l in product(COLORS, repeat=4):
        require(dictionary_product(responses[i, j], responses[k, l])
                == dictionary_product(responses[i, l], responses[k, j]),
                ("Segre rectangle failed", i, k, j, l))

    exposed = (LEFT, RIGHT, 2)
    common = tuple(site for site in SITES if site != 2)
    adjacent = 0
    for colours in product(COLORS, repeat=5):
        word = dict(zip(common, colours))
        for i, j, k in product(COLORS, repeat=3):
            value = (block_edge(blocks, LEFT, RIGHT, i, j)
                     * star_with_two_matchings(blocks, 2, k, word, common)
                     + block_edge(blocks, LEFT, 2, i, k)
                     * star_with_two_matchings(blocks, RIGHT, j, word, common)
                     + block_edge(blocks, RIGHT, 2, j, k)
                     * star_with_two_matchings(blocks, LEFT, i, word, common))
            value += three_stars_one_edge(blocks, i, j, k, word, exposed, common)
            require(value == Q(i == j == k == PURE and all(c == PURE for c in colours)),
                    ("literal adjacent 27-row failed", i, j, k, colours))
            adjacent += 1

    alpha = block_edge(blocks, LEFT, RIGHT, 0, 1)
    internal = {e: block_edge(blocks, e[0], e[1], PURE, PURE) for e in PAIRS}
    u = [block_edge(blocks, LEFT, x, 0, PURE) for x in SITES]
    v = [block_edge(blocks, RIGHT, x, 1, PURE) for x in SITES]
    r = {(x, y): u[x] * v[y] + v[x] * u[y] for x, y in PAIRS}
    layers = numeric_layers(internal, r)
    chi = alpha * layers[2] + layers[3]
    cap = {e: alpha * internal[e] + r[e] for e in PAIRS}
    require(numeric_haf(SITES, cap)
            == alpha ** 2 * (alpha * layers[0] + layers[1]) + chi,
            "guard cap split failed")
    require(block_row(blocks, 0, 1, (PURE,) * 6) == alpha * layers[0] + layers[1],
            "the pure-word row is not the source jet")
    jets = (alpha * layers[0] + layers[1], alpha * layers[1] + 2 * layers[2],
            alpha * layers[2] + 3 * layers[3], alpha * layers[3])
    return {"tensor": tensor, "ledger": ledger, "ranks": (matrix_rank(stars),
            matrix_rank(costars)), "adjacent": adjacent, "alpha": alpha,
            "layers": layers, "chi": chi, "jets": jets,
            "cap_haf": numeric_haf(SITES, cap)}


class Graded:
    """A formal sum of powers of tau with *positive* coefficients.

    No cancellation is possible, so a Graded value whose exponent set is a
    single point proves that every term of the computation that produced it
    carries that one weight."""

    __slots__ = ("terms",)

    def __init__(self, terms):
        self.terms = dict(terms)

    def __mul__(self, other):
        if isinstance(other, Graded):
            out = {}
            for e1, c1 in self.terms.items():
                for e2, c2 in other.terms.items():
                    out[e1 + e2] = out.get(e1 + e2, Q(0)) + c1 * c2
            return Graded(out)
        return Graded({e: c * other for e, c in self.terms.items()})

    __rmul__ = __mul__

    def __add__(self, other):
        if isinstance(other, Graded):
            out = dict(self.terms)
            for e, c in other.terms.items():
                out[e] = out.get(e, Q(0)) + c
            return Graded(out)
        require(other == 0, "a Graded value was added to a nonzero scalar")
        return self

    __radd__ = __add__

    def __bool__(self):
        return bool(self.terms)

    def exponents(self):
        return sorted(self.terms)


def block_weight(x, y):
    if y <= 5:
        return -1                             # internal quadratic edge
    if x <= 5:
        return 1                              # endpoint star edge
    return 3                                  # direct scalar


def audit_chart_weights():
    """The whole eight-site matching tensor is weight-homogeneous of weight nil.

    Master statement: every perfect matching of the eight vertices consists
    either of the direct edge plus three internal edges (3 - 3 = 0) or of one
    star edge at each endpoint plus two internal edges (1 + 1 - 2 = 0).  All
    105 = 7!! of them therefore have weight zero, so *every* chart of the array
    -- every choice of exposed vertices, every colour word, every label tuple
    -- is a sum of weight-zero monomials and is fixed by the substitution.

    The two audited charts are then re-derived from their own code with each
    block edge replaced by tau^(its weight) and coefficient one.  The
    substituted value depends only on the type of the edge and not on any
    colour, so one evaluation settles every word and label tuple; all
    coefficients stay positive, so a single exponent is a proof of homogeneity
    and not an accident of cancellation, and the coefficient 105 shows the
    probe really did see every perfect matching."""
    seen = 0
    for matching in matchings(tuple(range(8))):
        require(sum(block_weight(x, y) for x, y in matching) == 0,
                ("a perfect matching of the block array is not weight zero",
                 matching))
        seen += 1
    require(seen == 105, ("wrong perfect-matching count on eight vertices", seen))

    blocks = {}
    for x, y in combinations(range(8), 2):
        weight = block_weight(x, y)
        for cx, cy in product(COLORS, repeat=2):
            blocks[(x, y, cx, cy)] = Graded({weight: Q(1)})

    word = (0,) * 6
    value = block_row(blocks, 0, 0, word)
    require(value.exponents() == [0] and value.terms[0] == 105,
            ("the deleted-pair chart is not weight zero", value.terms))

    common = tuple(site for site in SITES if site != 2)
    exposed = (LEFT, RIGHT, 2)
    partial = {site: 0 for site in common}
    adjacent = (block_edge(blocks, LEFT, RIGHT, 0, 0)
                * star_with_two_matchings(blocks, 2, 0, partial, common)
                + block_edge(blocks, LEFT, 2, 0, 0)
                * star_with_two_matchings(blocks, RIGHT, 0, partial, common)
                + block_edge(blocks, RIGHT, 2, 0, 0)
                * star_with_two_matchings(blocks, LEFT, 0, partial, common))
    adjacent = adjacent + three_stars_one_edge(blocks, 0, 0, 0, partial,
                                               exposed, common)
    require(adjacent.exponents() == [0] and adjacent.terms[0] == 105,
            ("the adjacent chart is not weight zero", adjacent.terms))


def audit_seven_row_guard_family():
    base = guard_report(guard_blocks(Q(1)))
    require(base["tensor"] == [(2, 2, (PURE,) * 6, Q(1))],
            ("the guard physical tensor is not X_2", base["tensor"]))
    require(base["ledger"] == [(0, 0, (0,) * 6, Q(-1)), (1, 1, (1,) * 6, Q(-1))],
            ("the guard ledger changed", base["ledger"]))
    require(base["ranks"] == (3, 3), ("guard star ranks changed", base["ranks"]))
    require(base["adjacent"] == 27 * 243, "adjacent coefficient count changed")
    require(base["layers"] == (Q(0), Q(0), Q(-2), Q(0)),
            ("guard layers changed", base["layers"]))
    require(base["chi"] == -2 and base["cap_haf"] == -2, "guard chi changed")
    require(base["jets"] == (Q(0), Q(-4), Q(-2), Q(0)),
            ("guard jets changed", base["jets"]))

    for tau in (Q(2), Q(-3), Q(1, 2)):
        moved = guard_report(guard_blocks(tau))
        for key in ("tensor", "ledger", "ranks", "adjacent"):
            require(moved[key] == base[key],
                    ("the tau family moved the physical data", tau, key))
        require(moved["alpha"] == tau ** 3 * base["alpha"], ("alpha weight", tau))
        require(all(moved["layers"][k] == tau ** (3 * k - 3) * base["layers"][k]
                    for k in range(4)), ("layer weights", tau, moved["layers"]))
        require(all(moved["jets"][k] == tau ** (3 * k) * base["jets"][k]
                    for k in range(4)), ("jet weights", tau, moved["jets"]))
        require(moved["chi"] == tau ** 6 * base["chi"] == -2 * tau ** 6,
                ("chi is not weight six", tau, moved["chi"]))
        require(moved["cap_haf"] == moved["chi"], ("cap split moved", tau))

    # the negative reading, stated as an assertion: identical row data, four
    # different terminal classes.
    classes = sorted(guard_report(guard_blocks(tau))["chi"]
                     for tau in (Q(1), Q(2), Q(-3), Q(1, 2)))
    require(classes == [Q(-1458), Q(-128), Q(-2), Q(-1, 32)],
            ("the guard family terminal classes changed", classes))


def main():
    audit_normalization()
    audit_allword_identity_and_weights()
    audit_class_factorization()
    audit_cross_colour_break()
    audit_grade_ladder()
    audit_chart_weights()
    audit_rank_two_clean_packet()
    audit_seven_row_guard_family()
    print(
        "PASS: Row(i,j,w) = <(d_ij/3)q^w + R^w_ij, H(q^w)> formally on all 729 "
        "words x 9 pairs, with and without cross-colour edges; monochromatic "
        "class forms on 183 even and 546 two-odd words, and the exact "
        "cross-colour break; every row monomial is response-affine and of "
        "weight zero (q:-1, p,s:+1, d:+3) while Q_k, H_k, J_k, chi have "
        "weights 3k-3, 3k-2, 3k, 6; chi = (alpha/2)<R,H_1> + (1/3)<R,H_2> and "
        "haf(A_cap) = alpha^2*Row(i,j,c^6) + chi; all 105 perfect matchings of "
        "the block array are weight zero, so every chart is fixed by "
        "q->q/tau, p->tau p, s->tau s, d->tau^3 d; the clean packet stays "
        "clean and its twenty cut values are weight six; the seven-row guard "
        "is a one-parameter family with identical tensor, ledger, stars, Segre "
        "rectangles and adjacent 27-rows, and chi = -2*tau^6"
    )


if __name__ == "__main__":
    main()
