#!/usr/bin/env python3
"""Three universal support rules, established at eight vertices and three colours.

PROVENANCE.  The three rules are external work.  They are the theorems
``star_anchored``, ``pair_pencil`` and ``full_column_anchored`` of
``KrennGuCertificate/UniversalRules.lean`` in the public Lean development
``algal/krenn-gu-6x3-certificate`` at commit
``c04696e515e0c02be140353fb52ea60c62e827b1``, where they are stated and proved
for ``EqSystemN 6 3``.  See ``notes/external-six-site-lean-certificate.md`` for
the statement match and the trust boundary of that development.  The Lean
source was READ here; the Lean build was NOT re-run, so every attribution below
is EXTERNAL and NOT MACHINE-RECHECKED in this repository.

WHAT THIS FILE ADDS.  The rules are restated for an arbitrary vertex count and
established at ``EqSystemN 8 3``, the system this project's chart model was
shown to be by ``verify_chart_model_is_official_eqsystem.py``.  Write
``W(u,v,i,c)`` for the weight of the edge ``{u,v}`` with colour ``i`` at ``u``
and colour ``c`` at ``v``, and ``M_{ru}[i][c] = W(r,u,i,c)`` for the incident
matrix seen from a root ``r``.  For ``W`` satisfying ``EqSystemN n 3`` with
``n`` even:

  R1 (star anchor).  For every vertex ``r`` and colour ``a`` there is a
     neighbour ``u`` with ``M_{ru}[a][a] != 0`` and ``M_{ru}[a][c] = 0`` for
     ``c != a``: some incident matrix has its ``a``-row a nonzero multiple of
     ``e_a``.

  R2 (pair pencil).  For every vertex ``r`` and distinct colours ``a, b``,
     either for each ``t`` in ``{a,b}`` some neighbour has the two rows
     ``{a,b}`` of its incident matrix nonzero and supported in column ``t``, or
     at every neighbour those two rows are supported in columns ``{a,b}``.

  R3 (full column).  For every vertex ``r`` and colour ``t`` there is a
     neighbour ``u`` with ``M_{ru}`` nonzero and supported entirely in column
     ``t``; equivalently ``M_{ru} = xi (x) e_t`` with ``xi != 0``.

None of the three mentions ``n``.  The only ``n``-dependence in their proofs is
a field-size bound: R1 needs none, R2 needs at least ``n`` field elements, R3
at least ``2 + (n-1)(d-1)``.  At ``n = 8, d = 3`` those are ``8`` and ``16``,
so the rules hold over the complex numbers, the rationals, and any field with
at least sixteen elements.  Hence NO Nullstellensatz certificates are needed at
eight vertices: the schema counts audited below (897 at six vertices, 9485 at
eight) price a division-free encoding layer that the released Lean proof does
not use.

STATUS OF EACH CLAIM.  Section by section: the contraction identity and the
GHZ identity are PROVED here as formal polynomial identities over all 688905
monomials in arbitrary formal weights and arbitrary formal vectors.  The kernel
constructions, the incidence fact, the degree bounds and the certificate counts
are PROVED as finite identities or exhaustive finite checks.  The guard
ledgers, the proof replays, the consistency witness, the chart translations and
the comparison witnesses are VERIFIED BY EXHAUSTIVE COMPUTATION on named
packets.  The general-``n`` proofs themselves are hand proofs written up in the
accompanying note; this file machine-checks their finite inputs at ``n = 8``,
not the induction-free prose.

WHAT IS ALREADY HERE.  R3 is NOT new to this repository: it is the forced
incident-edge theorem of ``notes/slice-cover.md``, equation (6), which proves
the same conclusion AND the activity clause ``C_{pj} != 0``.  The comparison is
audited in ``audit_slice_cover_is_stronger_than_r3``.  R1 appears here only as
a conditional branch -- conclusion 2 of Theorem 4.1 of
``notes/zero-row-pair-propagation.md`` derives exactly R1's two equations, but
under entry-minimality, gauge-rigidity and a full zero set.  No unconditional
form of R1, and nothing resembling R2, was located.  R1 and R2 are compared
against T2 of ``notes/monochromatic-internal-quadratic-structure-and-eight-cycle-guard.md``
and T6 of ``notes/monochromatic-colour-pencil-and-rank-two-reduction.md``.

Krenn's conjecture remains OPEN, ``SP-CLEAN-BRIDGE`` is untouched, and no
certified dependency changes.  Standard library only, exact ``Fraction``
arithmetic, live under ``python3 -O`` and ``python3 -I -S``.
"""

from fractions import Fraction as Q
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise AssertionError(message)


COLORS = (0, 1, 2)
VERTICES = 8
SITES = tuple(range(6))
LEFT = 6
RIGHT = 7


# --------------------------------------------------------------------------
# the official recursion, transcribed from the Lean source, and the matchings
# it enumerates
# --------------------------------------------------------------------------
def pm_sum_list_aux(weight, iota, fuel, vertices):
    if fuel == 0:
        return Q(1)
    if fuel == 1:
        return Q(0)
    if not vertices:
        return Q(1)
    if len(vertices) == 1:
        return Q(0)
    head, tail = vertices[0], vertices[1:]
    total = Q(0)
    for position, partner in enumerate(tail):
        rest = tail[:position] + tail[position + 1:]
        total += (weight(head, partner, iota[head], iota[partner])
                  * pm_sum_list_aux(weight, iota, fuel - 2, rest))
    return total


def official_matchings():
    """The matchings the literal head-pairing recursion enumerates."""
    collected = []

    def walk(vertices, chosen):
        if not vertices:
            collected.append(tuple(chosen))
            return
        head, tail = vertices[0], vertices[1:]
        for position, partner in enumerate(tail):
            walk(tail[:position] + tail[position + 1:], chosen + [(head, partner)])

    walk(tuple(range(VERTICES)), [])
    return tuple(collected)


OFFICIAL_MATCHINGS = official_matchings()


def tail_matchings(vertices):
    """A SECOND, independent enumeration: pair the LAST vertex, not the first."""
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    if len(vertices) % 2:
        return ()
    last, rest = vertices[-1], vertices[:-1]
    accumulated = []
    for position, partner in enumerate(rest):
        remainder = rest[:position] + rest[position + 1:]
        for tail in tail_matchings(remainder):
            accumulated.append(((partner, last),) + tail)
    return tuple(accumulated)


TAIL_MATCHINGS = tail_matchings(tuple(range(VERTICES)))


def weight_of(blocks):
    def weight(u, v, cu, cv):
        if u > v:
            u, v, cu, cv = v, u, cv, cu
        return blocks.get((u, v, cu, cv), Q(0))
    return weight


def pm_sum(blocks, iota):
    weight = weight_of(blocks)
    total = Q(0)
    for matching in OFFICIAL_MATCHINGS:
        term = Q(1)
        for u, v in matching:
            term *= weight(u, v, iota[u], iota[v])
            if not term:
                break
        total += term
    return total


def ledger(blocks):
    """The failing equations of a packet, read from the official system."""
    out = []
    for letters in product(COLORS, repeat=VERTICES):
        target = Q(1) if len(set(letters)) == 1 else Q(0)
        value = pm_sum(blocks, list(letters))
        if value != target:
            out.append((letters, value - target))
    return sorted(out)


def incident(blocks, root, neighbor):
    weight = weight_of(blocks)
    return [[weight(root, neighbor, i, c) for c in COLORS] for i in COLORS]


# --------------------------------------------------------------------------
# the three rules as executable predicates
# --------------------------------------------------------------------------
def star_anchor_witnesses(blocks, root, color):
    found = []
    for u in range(VERTICES):
        if u == root:
            continue
        rows = incident(blocks, root, u)
        if rows[color][color] != 0 and all(rows[color][c] == 0
                                           for c in COLORS if c != color):
            found.append(u)
    return found


def full_column_witnesses(blocks, root, output):
    found = []
    for u in range(VERTICES):
        if u == root:
            continue
        rows = incident(blocks, root, u)
        if (any(rows[i][output] != 0 for i in COLORS)
                and all(rows[i][c] == 0
                        for i in COLORS for c in COLORS if c != output)):
            found.append(u)
    return found


def pair_pure_witnesses(blocks, root, first, second, output):
    found = []
    for u in range(VERTICES):
        if u == root:
            continue
        rows = incident(blocks, root, u)
        if ((rows[first][output] != 0 or rows[second][output] != 0)
                and all(rows[a][c] == 0
                        for a in (first, second) for c in COLORS if c != output)):
            found.append(u)
    return found


def pair_preserved(blocks, root, first, second):
    for u in range(VERTICES):
        if u == root:
            continue
        rows = incident(blocks, root, u)
        for a in (first, second):
            for c in COLORS:
                if c not in (first, second) and rows[a][c] != 0:
                    return False
    return True


def pair_pencil_holds(blocks, root, first, second):
    return ((bool(pair_pure_witnesses(blocks, root, first, second, first))
             and bool(pair_pure_witnesses(blocks, root, first, second, second)))
            or pair_preserved(blocks, root, first, second))


def rule_failures(blocks):
    star = [(r, a) for r in range(VERTICES) for a in COLORS
            if not star_anchor_witnesses(blocks, r, a)]
    column = [(r, t) for r in range(VERTICES) for t in COLORS
              if not full_column_witnesses(blocks, r, t)]
    pencil = [(r, a, b) for r in range(VERTICES)
              for a, b in combinations(COLORS, 2)
              if not pair_pencil_holds(blocks, r, a, b)]
    return sorted(star), sorted(column), sorted(pencil)


# --------------------------------------------------------------------------
# packets
# --------------------------------------------------------------------------
def put(blocks, x, y, cx, cy, value):
    if x > y:
        x, y, cx, cy = y, x, cy, cx
    blocks[(x, y, cx, cy)] = blocks.get((x, y, cx, cy), Q(0)) + Q(value)


def seven_row_guard():
    """The committed guard of
    verify_h3_diagonal_segre_second_transgression_seven_row_guard.py, copied
    verbatim from verify_chart_model_is_official_eqsystem.py."""
    blocks = {}
    put(blocks, 0, 1, 2, 2, 1)
    put(blocks, 4, 5, 2, 2, 1)
    put(blocks, LEFT, RIGHT, 0, 1, 1)
    put(blocks, LEFT, 0, 0, 2, 1)
    put(blocks, LEFT, 1, 0, 2, 1)
    put(blocks, LEFT, 4, 1, 2, 1)
    put(blocks, LEFT, 2, 2, 2, 1)
    put(blocks, LEFT, 3, 2, 2, 1)
    put(blocks, RIGHT, 5, 0, 2, 1)
    put(blocks, RIGHT, 2, 1, 2, 1)
    put(blocks, RIGHT, 3, 1, 2, -1)
    put(blocks, RIGHT, 2, 2, 2, Q(1, 2))
    put(blocks, RIGHT, 3, 2, 2, Q(1, 2))
    return blocks


def eight_cycle():
    """The alternating eight-cycle of
    monochromatic-internal-quadratic-structure-and-eight-cycle-guard.md."""
    blocks = {}
    put(blocks, LEFT, 0, 0, 0, 1)
    put(blocks, 0, 1, 1, 1, 1)
    put(blocks, 1, 2, 0, 0, 1)
    put(blocks, 2, 3, 1, 1, 1)
    put(blocks, 3, 4, 0, 0, 1)
    put(blocks, 4, 5, 1, 1, 1)
    put(blocks, RIGHT, 5, 0, 0, 1)
    put(blocks, LEFT, RIGHT, 1, 1, 1)
    return blocks


KOTZIG_FAMILIES = {0: ((0, 1), (2, 3), (4, 5), (6, 7)),
                   1: ((0, 2), (1, 3), (4, 6), (5, 7)),
                   2: ((0, 3), (1, 2), (4, 7), (5, 6))}


def kotzig_triple():
    """Three disjoint perfect matchings of K_8, the colour-c one carrying the
    single entry E_cc.  Used only as a consistency witness."""
    blocks = {}
    for color, edges in KOTZIG_FAMILIES.items():
        for u, v in edges:
            put(blocks, u, v, color, color, 1)
    return blocks


def deterministic_dense(seed):
    """A dense packet touching every edge and colour pair, from a fixed integer
    recurrence, so the checker stays deterministic."""
    blocks = {}
    state = seed
    for u, v in combinations(range(VERTICES), 2):
        for cu, cv in product(COLORS, repeat=2):
            state = (1103515245 * state + 12345) % 2147483648
            value = (state >> 16) % 7 - 3
            if value:
                blocks[(u, v, cu, cv)] = Q(value)
    return blocks


# --------------------------------------------------------------------------
# 1. the contraction identity, proved as a formal polynomial identity
# --------------------------------------------------------------------------
def audit_official_recursion_sanity():
    ones = lambda u, v, cu, cv: Q(1)
    require(pm_sum_list_aux(ones, [0] * VERTICES, VERTICES,
                            tuple(range(VERTICES))) == 105,
            "the literal official recursion does not count 105 perfect matchings")
    require(len(OFFICIAL_MATCHINGS) == 105 and len(TAIL_MATCHINGS) == 105,
            "a matching enumeration has the wrong length")
    as_sets = lambda ms: set(frozenset(frozenset(p) for p in m) for m in ms)
    require(as_sets(OFFICIAL_MATCHINGS) == as_sets(TAIL_MATCHINGS)
            and len(as_sets(OFFICIAL_MATCHINGS)) == 105,
            "the two independent matching enumerations disagree")
    probe = deterministic_dense(99)
    weight = weight_of(probe)
    for letters in ((0, 1, 2, 0, 1, 2, 0, 1), (2,) * 8, (0, 0, 1, 1, 2, 2, 0, 1)):
        require(pm_sum(probe, list(letters))
                == pm_sum_list_aux(weight, list(letters), VERTICES,
                                   tuple(range(VERTICES))),
                ("the extracted list disagrees with the literal recursion", letters))


def audit_unique_incident_edge():
    """Every perfect matching of K_8 meets every vertex in exactly one edge.

    This is the only combinatorial input the three proofs make of ``n``: it is
    why fixing the root vector and putting every neighbour vector in the kernel
    of its incident row kills EVERY matching term at once.
    """
    for matching in OFFICIAL_MATCHINGS:
        for root in range(VERTICES):
            touching = [pair for pair in matching if root in pair]
            require(len(touching) == 1,
                    ("a matching does not meet a vertex exactly once",
                     matching, root))


def audit_contraction_identity():
    """PROOF, over arbitrary formal weights and arbitrary formal vectors:

        sum over colourings iota of  (prod_u v_u(iota_u)) * pmSum_W(iota)
          = sum over matchings M of  prod_{uv in M} (v_u^T W_uv v_v),

        sum over colourings iota of  (prod_u v_u(iota_u)) * [iota constant]
          = sum over colours c of prod_u v_u(c).

    Both sides of the first identity are expanded to monomials in the 24 vector
    variables and 252 weight variables and compared exactly.  The two sides use
    the two INDEPENDENT matching enumerations above, so agreement tests the
    expansion rather than restating it.  Together with EqSystemN this gives the
    contraction identity the three rules run on:

        sum over matchings M of prod_{uv in M} (v_u^T W_uv v_v)
          = sum over colours c of prod_u v_u(c).
    """
    ids = {}

    def var(key):
        if key not in ids:
            ids[key] = len(ids)
        return ids[key]

    def wkey(u, v, cu, cv):
        if u > v:
            u, v, cu, cv = v, u, cv, cu
        return var(("w", u, v, cu, cv))

    vector = [[var(("v", u, c)) for c in COLORS] for u in range(VERTICES)]
    for u, v in combinations(range(VERTICES), 2):
        for cu, cv in product(COLORS, repeat=2):
            wkey(u, v, cu, cv)
    require(len(ids) == VERTICES * 3 + 28 * 9,
            ("wrong variable count", len(ids)))

    left = {}
    for iota in product(COLORS, repeat=VERTICES):
        base = [vector[u][iota[u]] for u in range(VERTICES)]
        for matching in OFFICIAL_MATCHINGS:
            key = tuple(sorted(base + [wkey(u, v, iota[u], iota[v])
                                       for u, v in matching]))
            left[key] = left.get(key, 0) + 1

    pairs = tuple(product(COLORS, repeat=2))
    right = {}
    for matching in TAIL_MATCHINGS:
        tables = [[(vector[a][ca], wkey(a, b, ca, cb), vector[b][cb])
                   for ca, cb in pairs] for a, b in matching]
        first, second, third, fourth = tables
        for x0 in first:
            for x1 in second:
                head = x0 + x1
                for x2 in third:
                    body = head + x2
                    for x3 in fourth:
                        key = tuple(sorted(body + x3))
                        right[key] = right.get(key, 0) + 1

    require(left == right, "the contraction identity fails as a polynomial identity")
    require(len(left) == 105 * 3 ** VERTICES,
            ("wrong monomial count", len(left)))
    require(all(coefficient == 1 for coefficient in left.values()),
            "a contraction monomial has a coefficient other than one")

    target = {}
    for iota in product(COLORS, repeat=VERTICES):
        if len(set(iota)) == 1:
            key = tuple(sorted(vector[u][iota[u]] for u in range(VERTICES)))
            target[key] = target.get(key, 0) + 1
    ghz = {}
    for c in COLORS:
        key = tuple(sorted(vector[u][c] for u in range(VERTICES)))
        ghz[key] = ghz.get(key, 0) + 1
    require(target == ghz and len(ghz) == 3,
            "the GHZ side of the contraction identity fails")


# --------------------------------------------------------------------------
# 2. the finite algebraic inputs of the three proofs
# --------------------------------------------------------------------------
def polynomial_product(left, right):
    out = {}
    for m1, c1 in left.items():
        for m2, c2 in right.items():
            key = tuple(sorted(m1 + m2))
            out[key] = out.get(key, Q(0)) + c1 * c2
    return {m: c for m, c in out.items() if c}


def audit_kernel_constructions():
    """PROOF of the two kernel families, as formal polynomial identities in a
    symbolic row ``(r_0, r_1, r_2)``.

    (a) two-coordinate kernel, used by R2 and R3: for distinct ``t, k`` the
        vector ``r_k e_t - r_t e_k`` annihilates ``r`` and has ``t``-coordinate
        ``r_k``.
    (b) star-anchor kernel, used by R1: if ``r_a = 0`` then ``e_a`` annihilates
        ``r``; otherwise, for a pivot ``k != a`` with ``r_k != 0``, the vector
        ``e_a - (r_a/r_k) e_k`` annihilates ``r``.  Cleared of denominators the
        identity is ``r_k * r_a + r_a * (-r_k) = 0``.
    """
    row = {c: {(("r", c),): Q(1)} for c in COLORS}
    zero = {}
    for t, k in product(COLORS, repeat=2):
        if t == k:
            continue
        vector = {t: row[k], k: {m: -c for m, c in row[t].items()}}
        total = {}
        for c in COLORS:
            piece = polynomial_product(row[c], vector.get(c, zero))
            for m, value in piece.items():
                total[m] = total.get(m, Q(0)) + value
        require(not {m: c for m, c in total.items() if c},
                ("the two-coordinate kernel fails", t, k))
        require(vector[t] == row[k], ("wrong t-coordinate", t, k))
    for a, k in product(COLORS, repeat=2):
        if a == k:
            continue
        cleared = {}
        for m, value in polynomial_product(row[k], row[a]).items():
            cleared[m] = cleared.get(m, Q(0)) + value
        for m, value in polynomial_product(row[a], row[k]).items():
            cleared[m] = cleared.get(m, Q(0)) - value
        require(not {m: c for m, c in cleared.items() if c},
                ("the star-anchor kernel fails", a, k))


def audit_finite_avoidance_degrees():
    """PROOF of the parameter bounds at eight vertices.

    R2 selects one affine-linear form per neighbour in a single parameter, so
    the product has degree at most ``n - 1 = 7``: at most seven bad values.
    R3 selects one form of degree at most ``d - 1 = 2`` per neighbour, times
    the parameter itself, so degree at most ``1 + (n-1)(d-1) = 15``: at most
    fifteen bad values.  Both bounds are attained, so they cannot be improved
    by counting alone.  Over any field with more than that many elements -- in
    particular over C and over Q -- a good parameter exists.
    """
    neighbours = VERTICES - 1
    require(neighbours == 7, "wrong neighbour count")
    require(neighbours * 1 == 7, "wrong pair-pencil degree bound")
    require(1 + neighbours * (len(COLORS) - 1) == 15,
            "wrong full-column degree bound")

    def degree(poly):
        return max(k for k, c in enumerate(poly) if c) if any(poly) else -1

    def multiply(first, second):
        out = [Q(0)] * (len(first) + len(second) - 1)
        for i, a in enumerate(first):
            for j, b in enumerate(second):
                out[i + j] += a * b
        return out

    pencil = [Q(1)]
    for _ in range(neighbours):
        pencil = multiply(pencil, [Q(1), Q(1)])
    require(degree(pencil) == 7, "the pair-pencil product degree is wrong")

    column = [Q(0), Q(1)]
    for _ in range(neighbours):
        column = multiply(column, [Q(1), Q(1), Q(1)])
    require(degree(column) == 15, "the full-column product degree is wrong")

    for poly, bound in ((pencil, 7), (column, 15)):
        values = [sum(c * Q(t) ** k for k, c in enumerate(poly))
                  for t in range(bound + 1)]
        require(any(v != 0 for v in values),
                "a nonzero polynomial vanished on the whole avoidance grid")


def audit_certificate_counts():
    """The exact-Nullstellensatz schema counts of the external note
    ``notes/2026-07-23-universal-nullstellensatz.md``, reproduced and scaled.

    That note records 897 certificates at six vertices, split star-anchor
    ``3^(n-1)``, pair-pencil ``(n-1) 3^(n-2)``, full-column direct
    ``3^(n-1) - 2``, one uniform hard core, and ``n + 1`` hard-core equations.
    The same formulas give 9485 at eight vertices, matching the estimate this
    task was asked to check.  The arithmetic is confirmed; the LAYER is not
    needed, since the released Lean development proves all three rules with no
    certificate at all -- ``UniversalRules.lean`` imports only the contraction
    module and ``Mathlib.Algebra.Polynomial.Roots``, and no Lean file in that
    release refers to the Nullstellensatz artifacts.  That reading is EXTERNAL
    and NOT MACHINE-RECHECKED here.
    """
    def schemas(n):
        star = 3 ** (n - 1)
        pencil = (n - 1) * 3 ** (n - 2)
        column = 3 ** (n - 1) - 2
        core = 1
        hard = n + 1
        return star, pencil, column, core, hard

    six = schemas(6)
    require(six == (243, 405, 241, 1, 7), ("six-vertex split changed", six))
    require(sum(six) == 897, ("six-vertex total changed", sum(six)))
    eight = schemas(8)
    require(eight == (2187, 5103, 2185, 1, 9), ("eight-vertex split", eight))
    require(sum(eight) == 9485, ("eight-vertex total", sum(eight)))


# --------------------------------------------------------------------------
# 3. the rules have teeth at eight vertices
# --------------------------------------------------------------------------
def audit_guard_ledgers_and_rule_failures():
    """The two committed guards, first pinned by their official ledgers, then
    measured against the three rules.

    The eight-cycle satisfies 6560 of 6561 equations, failing only the
    colour-2 anchor.  R1 and R3 fail on it at EXACTLY the eight pairs
    ``(vertex, 2)`` -- every vertex, and only colour 2.  R2 does not fail at
    all.  The seven-row guard fails the colour-0 and colour-1 anchors, and R1
    fails on it at exactly the sixteen pairs ``(vertex, 0)`` and
    ``(vertex, 1)``.  So the rules localize a near-solution's defect to the
    right colour, and R2 is strictly the weakest of the three.
    """
    require(ledger(seven_row_guard()) == [((0,) * 8, Q(-1)), ((1,) * 8, Q(-1))],
            "the seven-row guard's official ledger changed")
    require(ledger(eight_cycle()) == [((2,) * 8, Q(-1))],
            "the eight-cycle's official ledger changed")

    star, column, pencil = rule_failures(eight_cycle())
    require(star == [(r, 2) for r in range(VERTICES)],
            ("eight-cycle star-anchor failures", star))
    require(column == [(r, 2) for r in range(VERTICES)],
            ("eight-cycle full-column failures", column))
    require(pencil == [], ("eight-cycle pair-pencil failures", pencil))

    star, column, pencil = rule_failures(seven_row_guard())
    require(star == sorted((r, a) for r in range(VERTICES) for a in (0, 1)),
            ("seven-row star-anchor failures", star))
    require(len(column) == 10 and all(t in (0, 1) for _, t in column),
            ("seven-row full-column failures", column))
    require(len(pencil) == 10, ("seven-row pair-pencil failures", pencil))


def contract_matchings(blocks, vectors):
    weight = weight_of(blocks)
    total = Q(0)
    for matching in OFFICIAL_MATCHINGS:
        term = Q(1)
        for u, v in matching:
            edge = Q(0)
            for cu in COLORS:
                if not vectors[u][cu]:
                    continue
                for cv in COLORS:
                    if vectors[v][cv]:
                        edge += vectors[u][cu] * weight(u, v, cu, cv) * vectors[v][cv]
            term *= edge
            if not term:
                break
        total += term
    return total


def product_over(values):
    out = Q(1)
    for value in values:
        out *= value
    return out


def ghz_value(vectors):
    return sum((product_over([vectors[u][c] for u in range(VERTICES)])
                for c in COLORS), Q(0))


def weighted_defect(entries, vectors):
    total = Q(0)
    for letters, residual in entries:
        total += product_over([vectors[u][letters[u]]
                               for u in range(VERTICES)]) * residual
    return total


def star_anchor_vectors(blocks, root, color):
    """The vector family the R1 proof builds when the anchor is missing."""
    vectors = {root: [Q(1) if c == color else Q(0) for c in COLORS]}
    for u in range(VERTICES):
        if u == root:
            continue
        row = incident(blocks, root, u)[color]
        if row[color] == 0:
            vectors[u] = [Q(1) if c == color else Q(0) for c in COLORS]
        else:
            pivot = next((c for c in COLORS if c != color and row[c] != 0), None)
            require(pivot is not None,
                    ("no pivot at a neighbour without an anchor", root, color, u))
            entry = [Q(0)] * len(COLORS)
            entry[color] = Q(1)
            entry[pivot] = -row[color] / row[pivot]
            vectors[u] = entry
    return vectors


def audit_proof_replay():
    """Run the R1 proof on the two guards and read what saves them.

    With no anchor at ``(root, colour)`` the constructed vectors kill every
    matching term, so the left side of the contraction identity is 0, while the
    GHZ side is 1.  For a genuine solution that is ``0 = 1``.  For a guard the
    identity carries a defect term, and the replay shows the defect is exactly
    the guard's own failing equations: for the eight-cycle the single residual
    ``-1`` at ``2^8``.
    """
    for blocks, name, colors in ((eight_cycle(), "eight-cycle", (2,)),
                                 (seven_row_guard(), "seven-row", (0, 1))):
        entries = ledger(blocks)
        for root in range(VERTICES):
            for color in colors:
                require(not star_anchor_witnesses(blocks, root, color),
                        ("unexpected anchor", name, root, color))
                vectors = star_anchor_vectors(blocks, root, color)
                left = contract_matchings(blocks, vectors)
                ghz = ghz_value(vectors)
                defect = weighted_defect(entries, vectors)
                require(left == ghz + defect,
                        ("contraction identity with defect failed", name, root, color))
                require(left == 0, ("matchings not killed", name, root, color))
                require(ghz == 1, ("GHZ contraction is not one", name, root, color))
                require(defect == -1, ("unexpected defect", name, root, color, defect))


def audit_rules_alone_do_not_close_eight():
    """The three rules are jointly SATISFIABLE at eight vertices, so none of
    them, and no combination of them, is a proof of the (8,3) case.

    Witness: three disjoint perfect matchings of K_8, the colour-c one carrying
    the single entry E_cc.  All three rules hold at every vertex and every
    colour, or colour pair -- and so does the STRONGER slice-cover conclusion,
    with its activity clause.  The packet is nevertheless not a solution: it
    fails exactly six of the 6561 equations, at the split colourings
    ``c^4 c'^4``.
    """
    blocks = kotzig_triple()
    star, column, pencil = rule_failures(blocks)
    require(star == [] and column == [] and pencil == [],
            ("the consistency witness violates a rule", star, column, pencil))
    for root in range(VERTICES):
        for color in COLORS:
            active = [u for u in full_column_witnesses(blocks, root, color)
                      if complementary_tensor_nonzero(blocks, root, u)]
            require(active,
                    ("the consistency witness has no ACTIVE rank-one incident "
                     "block", root, color))
    failures = ledger(blocks)
    require(len(failures) == 6, ("consistency witness ledger", len(failures)))
    expected = sorted(((c,) * 4 + (d,) * 4, Q(1))
                      for c in COLORS for d in COLORS if c != d)
    require(failures == expected, ("consistency witness ledger", failures))
    for color, edges in KOTZIG_FAMILIES.items():
        covered = sorted(v for pair in edges for v in pair)
        require(covered == list(range(VERTICES)),
                ("a Kotzig family is not a perfect matching", color))
    all_edges = [frozenset(pair) for edges in KOTZIG_FAMILIES.values()
                 for pair in edges]
    require(len(set(all_edges)) == 12, "the Kotzig families are not disjoint")


# --------------------------------------------------------------------------
# 4. chart translation
# --------------------------------------------------------------------------
def audit_chart_translation():
    """The three rules, rewritten in this project's chart coordinates.

    The chart is six residual sites plus two endpoints, with ``d_ij`` on the
    direct edge, ``p_i(x,c)`` and ``s_j(y,c)`` on the star edges and an
    internal quadratic on the site edges.  The incident matrices are then
    ``M_{LEFT,RIGHT}[i][j] = d_ij``, ``M_{LEFT,x}[i][c] = p_i(x,c)``,
    ``M_{x,LEFT}[c][i] = p_i(x,c)``, and similarly for RIGHT and s.  Each
    restatement below is checked to be EQUIVALENT to the vertex-level predicate
    on every named packet, so it is a translation, not a new claim.

    R1 at the endpoint LEFT and label ``i``: either ``d_ii != 0`` and
    ``d_ij = 0`` for ``j != i``, or some site ``x`` has ``p_i(x,i) != 0`` and
    ``p_i(x,c) = 0`` for ``c != i``.

    R3 at the endpoint LEFT and colour ``t``: either the whole direct block is
    supported in column ``t``, or some site ``x`` has the whole star block
    ``[p_i(x,c)]_{i,c}`` supported in site-colour ``t`` and nonzero.  Since the
    three witnesses are distinct and RIGHT can serve only one colour, AT LEAST
    TWO SITES have a star block concentrated in a single site-colour.

    R3 at an internal site ``x`` and colour ``t``, with a monochromatic
    internal quadratic ``q``: either some site ``y`` has ``q_t(x,y) != 0`` and
    ``q_c(x,y) = 0`` for both ``c != t``, or the star at ``x`` is carried by
    label ``t`` alone at LEFT, or at RIGHT.  Since LEFT and RIGHT serve at most
    one colour each, EVERY SITE HAS A COLOUR-PURE INTERNAL EDGE for at least
    one colour.
    """
    def endpoint_star_anchor(blocks, label):
        direct = incident(blocks, LEFT, RIGHT)
        if direct[label][label] != 0 and all(direct[label][j] == 0
                                             for j in COLORS if j != label):
            return True
        for x in SITES:
            row = incident(blocks, LEFT, x)[label]
            if row[label] != 0 and all(row[c] == 0 for c in COLORS if c != label):
                return True
        return False

    def endpoint_full_column(blocks, output):
        direct = incident(blocks, LEFT, RIGHT)
        if (any(direct[i][output] != 0 for i in COLORS)
                and all(direct[i][j] == 0
                        for i in COLORS for j in COLORS if j != output)):
            return True
        for x in SITES:
            star = incident(blocks, LEFT, x)
            if (any(star[i][output] != 0 for i in COLORS)
                    and all(star[i][c] == 0
                            for i in COLORS for c in COLORS if c != output)):
                return True
        return False

    packets = [("seven-row", seven_row_guard()), ("eight-cycle", eight_cycle()),
               ("kotzig", kotzig_triple()), ("dense 1", deterministic_dense(1)),
               ("dense 2", deterministic_dense(7))]
    for name, blocks in packets:
        for label in COLORS:
            require(endpoint_star_anchor(blocks, label)
                    == bool(star_anchor_witnesses(blocks, LEFT, label)),
                    ("chart R1 translation at LEFT differs", name, label))
        for output in COLORS:
            require(endpoint_full_column(blocks, output)
                    == bool(full_column_witnesses(blocks, LEFT, output)),
                    ("chart R3 translation at LEFT differs", name, output))

    # the "at least two sites" and "colour-pure internal edge" corollaries are
    # counting consequences of the witnesses being distinct; check the counting
    # step itself, which is the only place the chart enters.
    for name, blocks in packets:
        for root in range(VERTICES):
            witnesses = {t: set(full_column_witnesses(blocks, root, t))
                         for t in COLORS}
            for t, other in combinations(COLORS, 2):
                require(not (witnesses[t] & witnesses[other]),
                        ("a neighbour served two colours at once", name, root,
                         t, other))


def complementary_tensor_nonzero(blocks, p, j):
    """Whether ``C_pj = H_{B minus {p,j}}(A)`` is a nonzero tensor."""
    rest = tuple(v for v in range(VERTICES) if v not in (p, j))
    weight = weight_of(blocks)
    pairings = tail_matchings(rest)
    for word in product(COLORS, repeat=len(rest)):
        colour = dict(zip(rest, word))
        total = Q(0)
        for matching in pairings:
            term = Q(1)
            for u, v in matching:
                term *= weight(u, v, colour[u], colour[v])
                if not term:
                    break
            total += term
        if total:
            return True
    return False


def star_at_one_vertex():
    """A packet whose only nonzero blocks are three single entries at vertex 0:
    ``A_01 = E_10``, ``A_02 = E_21``, ``A_03 = E_02``.

    Viewed from vertex 0 these are rank-one blocks whose far-side factors are
    ``e_0, e_1, e_2``, so R3 holds at vertex 0 for all three colours.  No
    ``a``-row of any of them is a nonzero multiple of ``e_a``, so R1 fails at
    vertex 0 for all three colours.  And every other vertex pair carries the
    zero block, so every complementary tensor ``C_0j`` vanishes.  One packet
    therefore separates R3 from R1 and from the slice-cover activity clause.
    """
    blocks = {}
    put(blocks, 0, 1, 1, 0, 1)
    put(blocks, 0, 2, 2, 1, 1)
    put(blocks, 0, 3, 0, 2, 1)
    return blocks


def audit_slice_cover_is_stronger_than_r3():
    """R3 is already in this repository, in a stronger form.

    ``notes/slice-cover.md`` proves the forced incident-edge theorem: for every
    vertex ``p`` and colour ``r`` there is a neighbour ``j`` with
    ``A_pj = a (x) e_r``, ``a != 0``, AND the complementary matching tensor
    ``C_pj = H_{B minus {p,j}}(A)`` nonzero.  The first half is exactly R3, so
    slice-cover implies R3 and R3 is not new here.  The containment is strict:
    on ``star_at_one_vertex`` R3 holds at vertex 0 for every colour while no
    witness is active.  On the two committed guards the active witnesses are,
    as they must be, a sub-family of the R3 witnesses.
    """
    separating = star_at_one_vertex()
    for output in COLORS:
        witnesses = full_column_witnesses(separating, 0, output)
        require(witnesses, ("R3 must hold at vertex 0", output))
        require(not any(complementary_tensor_nonzero(separating, 0, u)
                        for u in witnesses),
                ("a witness should be inactive", output))

    for name, blocks in (("eight-cycle", eight_cycle()),
                         ("kotzig", kotzig_triple())):
        for root in range(VERTICES):
            for output in COLORS:
                witnesses = full_column_witnesses(blocks, root, output)
                active = [u for u in witnesses
                          if complementary_tensor_nonzero(blocks, root, u)]
                require(set(active) <= set(witnesses),
                        ("activity is not a refinement", name, root, output))


def audit_star_anchor_is_not_implied_by_r3():
    """R1 is NOT a consequence of R3, nor of the slice-cover theorem.

    R3 gives ``A_pj = a (x) e_t`` with the near-side factor ``a`` arbitrary --
    ``notes/slice-cover.md`` says so explicitly, and warns that it is not even
    known to be a coordinate vector.  The ``a``-row of such a block is
    ``a_a e_t``, a star anchor only when ``t = a`` and ``a_a != 0``.  On
    ``star_at_one_vertex`` R3 holds at vertex 0 for all three colours and R1
    fails there for all three, so no amount of R3 gives R1.
    """
    blocks = star_at_one_vertex()
    for output in COLORS:
        require(full_column_witnesses(blocks, 0, output),
                ("R3 must hold at vertex 0", output))
        require(not star_anchor_witnesses(blocks, 0, output),
                ("R1 must fail at vertex 0", output))


# --------------------------------------------------------------------------
# 5. comparison with T2 and T6
# --------------------------------------------------------------------------
def four_hole_cofactors(blocks, color):
    """haf(q_c restricted to the six sites minus a pair): the fifteen four-hole
    cofactors of T2."""
    weight = weight_of(blocks)
    out = {}
    for hole in combinations(SITES, 2):
        rest = [x for x in SITES if x not in hole]
        total = Q(0)
        for pairing in (((rest[0], rest[1]), (rest[2], rest[3])),
                        ((rest[0], rest[2]), (rest[1], rest[3])),
                        ((rest[0], rest[3]), (rest[1], rest[2]))):
            term = Q(1)
            for x, y in pairing:
                term *= weight(x, y, color, color)
            total += term
        out[hole] = total
    return out


def monochromatic_packet(internal, stars=(), costars=(), direct=()):
    blocks = {}
    for color, edges in internal.items():
        for x, y in edges:
            put(blocks, x, y, color, color, 1)
    for label, site, color, value in stars:
        put(blocks, LEFT, site, label, color, value)
    for label, site, color, value in costars:
        put(blocks, RIGHT, site, label, color, value)
    for i, j, value in direct:
        put(blocks, LEFT, RIGHT, i, j, value)
    return blocks


def audit_comparison_with_t2():
    """R1 and T2 are INCOMPARABLE as predicates on packets.

    T2 (``monochromatic-internal-quadratic-structure-and-eight-cycle-guard.md``)
    says every colour has a nonzero four-hole cofactor of its internal
    quadratic; T6 (``monochromatic-colour-pencil-and-rank-two-reduction.md``)
    extends that to every nonzero combination.  Both are hafnian
    non-degeneracy statements about the six site edges only.  R1 is a support
    statement about one row of one incident matrix, at every vertex including
    the two endpoints.

    Because the (8,3) system may well have no solution at all, the IMPLICATIONS
    between the rules could be vacuously true; what is separated here is the
    CONCLUSIONS, as predicates on arbitrary packets.  Two witnesses:

    A: R1 holds at every site and colour, yet colour 2 has all fifteen
       four-hole cofactors zero.  So R1 does not give T2's conclusion.
    B: every colour has a nonzero four-hole cofactor, yet R1 fails at a site
       and at both endpoints.  So T2's conclusion does not give R1.
    """
    packet_a = monochromatic_packet(
        {0: [(0, 1), (2, 3), (4, 5)],
         1: [(0, 2), (1, 3), (4, 5)],
         2: [(0, 1)]},
        stars=[(2, x, 2, Q(1)) for x in (2, 3, 4, 5)],
        direct=[(2, 2, Q(1))])
    require(all(value == 0 for value in four_hole_cofactors(packet_a, 2).values()),
            "witness A should have all colour-2 four-hole cofactors zero")
    missing = [(r, c) for r in SITES for c in COLORS
               if not star_anchor_witnesses(packet_a, r, c)]
    require(missing == [], ("witness A should satisfy R1 at every site", missing))

    packet_b = monochromatic_packet({0: [(0, 1), (2, 3)],
                                     1: [(0, 2), (1, 3)],
                                     2: [(0, 3), (1, 2)]})
    for color in COLORS:
        require(any(value != 0 for value in four_hole_cofactors(packet_b, color).values()),
                ("witness B should satisfy T2's conclusion", color))
    missing = [(r, c) for r in range(VERTICES) for c in COLORS
               if not star_anchor_witnesses(packet_b, r, c)]
    require((4, 2) in missing and (5, 2) in missing
            and (LEFT, 0) in missing and (RIGHT, 0) in missing,
            ("witness B should fail R1 at sites 4,5 and both endpoints", missing))


def audit_t2_covers_four_of_six_sites():
    """The precise overlap between T2's conclusion and R1's internal branch.

    A nonzero four-hole cofactor of ``q_c`` means a 4-set on which ``q_c`` has a
    nonzero hafnian, hence two disjoint nonzero ``q_c`` edges, hence at least
    four sites carry a nonzero ``q_c`` edge.  So T2 delivers R1's internal
    branch at four of the six sites and says nothing about the other two, while
    R1 covers all six but allows a star branch.  Checked exhaustively over all
    support patterns of a symmetric six-site graph with at most three edges,
    which is enough to exhibit the extremal case.
    """
    edges = tuple(combinations(SITES, 2))
    seen_four = False
    for size in range(0, 4):
        for support in combinations(edges, size):
            blocks = {}
            for x, y in support:
                put(blocks, x, y, 0, 0, 1)
            cofactors = four_hole_cofactors(blocks, 0)
            covered = sorted({v for pair in support for v in pair})
            if any(value != 0 for value in cofactors.values()):
                require(len(covered) >= 4,
                        ("a nonzero four-hole cofactor with fewer than four "
                         "covered sites", support))
                if len(covered) == 4:
                    seen_four = True
    require(seen_four, "the extremal four-site case was not reached")


# --------------------------------------------------------------------------
# 6. what the rules give the descent
# --------------------------------------------------------------------------
def audit_descent_interface():
    """The two facts the descent could use, checked as exact identities.

    ``notes/clean-pair-cap-exact-descent-target.md`` needs a pair ``p,q`` and a
    cap covector ``K`` with ``s * kappa_0 * kappa_1 * kappa_2 != 0`` and
    vanishing clean error, where ``kappa_c = K(e_c,e_c)`` and
    ``s = <K, A_pq>``.  Section 7 of
    ``notes/canonical-transition-pencil-fan-dichotomy.md`` builds the candidate
    line ``K_lambda = e*_{p,a} (x) e*_{q,b} + lambda sum_i e*_{p,i} (x) e*_{q,i}``
    from an entry ``A_pq(a,b) != 0``.

    (i) R1 supplies such an entry unconditionally, on the DIAGONAL: for every
        ``p`` and every ``a`` there is a ``q`` with ``A_pq(a,a) != 0`` and the
        rest of that row zero.  On the resulting line
        ``kappa_i = [i = a] + lambda`` and
        ``s(K_lambda) = A_pq(a,a) + lambda tr A_pq``, so activity fails at at
        most three values of ``lambda`` -- the same count as before.  The gain
        is the supply of lines, not the activity count.

    (ii) R3 pins the correction tensor.  If ``A_pa = xi (x) e_t`` then the
        ``V_a`` slot of ``K contracted with A_{p|a}`` lies on the coordinate
        line ``C e_t``.  Since the three R3 witnesses at ``p`` are distinct and
        at most one is ``q``, at least two sites of ``U`` have that slot pinned.

    Both are identities about the cap ingredients.  Neither says anything about
    a common root of the clean-error coordinates, which is what
    ``SP-CLEAN-BRIDGE`` asks for.
    """
    # (i) exact cap-line coefficients on a diagonal anchor.
    for anchor in COLORS:
        entries = {(i, j): Q(2 + 3 * i + j) for i in COLORS for j in COLORS}
        for j in COLORS:
            if j != anchor:
                entries[(anchor, j)] = Q(0)
        require(entries[(anchor, anchor)] != 0, "the anchor entry must be nonzero")
        for numerator in range(-4, 5):
            lam = Q(numerator, 3)
            cap = {(i, j): (Q(1) if (i, j) == (anchor, anchor) else Q(0))
                   + (lam if i == j else Q(0)) for i in COLORS for j in COLORS}
            kappa = [cap[(c, c)] for c in COLORS]
            require(kappa == [(Q(1) if c == anchor else Q(0)) + lam
                              for c in COLORS],
                    ("kappa formula", anchor, lam))
            s = sum((cap[(i, j)] * entries[(i, j)]
                     for i in COLORS for j in COLORS), Q(0))
            require(s == entries[(anchor, anchor)]
                    + lam * sum((entries[(i, i)] for i in COLORS), Q(0)),
                    ("s formula", anchor, lam))
            product_kappa = product_over(kappa)
            require((product_kappa == 0) == (lam in (Q(0), Q(-1))),
                    ("kappa_0 kappa_1 kappa_2 = lambda^2 (1 + lambda)",
                     anchor, lam))
        # s is affine in lambda with nonzero constant term, so it has at most
        # one root; the kappa product has exactly two.  At most three inactive
        # values of lambda, exactly as the pencil note records.
        require(entries[(anchor, anchor)] != 0, "s(0) must be nonzero")

    # (ii) a rank-one incident block pins one slot of the correction tensor.
    for t in COLORS:
        xi = [Q(3), Q(-1), Q(5)]
        star = {(i, c): (xi[i] if c == t else Q(0))
                for i in COLORS for c in COLORS}
        for cap in ({(i, j): Q(1 + i * 3 + j) for i in COLORS for j in COLORS},
                    {(i, j): Q((-1) ** (i + j) * (i + 2 * j + 1))
                     for i in COLORS for j in COLORS}):
            for j in COLORS:
                slot = [sum((cap[(i, j)] * star[(i, c)] for i in COLORS), Q(0))
                        for c in COLORS]
                scale = sum((cap[(i, j)] * xi[i] for i in COLORS), Q(0))
                require(slot == [scale if c == t else Q(0) for c in COLORS],
                        ("the contracted slot is not on the coordinate line", t, j))


# --------------------------------------------------------------------------
def main():
    audit_official_recursion_sanity()
    audit_unique_incident_edge()
    audit_contraction_identity()
    audit_kernel_constructions()
    audit_finite_avoidance_degrees()
    audit_certificate_counts()
    audit_guard_ledgers_and_rule_failures()
    audit_proof_replay()
    audit_rules_alone_do_not_close_eight()
    audit_chart_translation()
    audit_slice_cover_is_stronger_than_r3()
    audit_star_anchor_is_not_implied_by_r3()
    audit_comparison_with_t2()
    audit_t2_covers_four_of_six_sites()
    audit_descent_interface()
    print(
        "PASS: the product-vector contraction identity holds at eight vertices "
        "as a POLYNOMIAL identity in arbitrary formal weights and vectors, on "
        "all 688905 monomials, with the two sides expanded through two "
        "independent matching enumerations; every perfect matching of K_8 meets "
        "every vertex exactly once; the two kernel families and the parameter "
        "degree bounds 7 and 15 are exact identities, so the star-anchor, "
        "pair-pencil and full-column rules of algal/krenn-gu-6x3-certificate "
        "hold verbatim at EqSystemN 8 3 with NO certificates -- the 897 and "
        "9485 schema counts are reproduced but are not needed.  The rules have "
        "teeth: on the alternating eight-cycle, which satisfies 6560 of 6561 "
        "equations, the star-anchor and full-column rules fail at exactly the "
        "eight pairs (vertex, 2) and the proof replay shows the defect is "
        "exactly the guard's single residual -1 at 2^8; on the seven-row guard "
        "the star-anchor rule fails at exactly (vertex, 0) and (vertex, 1).  "
        "The rules are jointly satisfiable at eight vertices -- a Kotzig triple "
        "meets all three, and the stronger slice-cover form with its activity "
        "clause, yet fails six equations -- so none of them is a proof of "
        "the (8,3) case.  The full-column rule is already here, in the stronger "
        "form of the forced incident-edge theorem of notes/slice-cover.md; the "
        "star-anchor rule is not implied by it, and is incomparable with T2 and "
        "T6, with explicit witnesses in both directions.  Krenn's conjecture "
        "remains OPEN and SP-CLEAN-BRIDGE is untouched"
    )


if __name__ == "__main__":
    main()
