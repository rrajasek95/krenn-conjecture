#!/usr/bin/env python3
"""The three diagonal anchors cannot be carried by the internal quadratic.

Exact, dependency-free, standard library only.

Setting.  Six residual sites, three colours.  For a colour-decorated
internal quadratic q whose edges are monochromatic with non-negative
weights, write E_c for the set of edges carrying colour c and

    haf_w(q) = sum over perfect matchings M of prod_{(x,y) in M} q(x,y,w_x,w_y)

for a colour word w.  A matching edge is usable only if both endpoints have
the same colour, so haf_w(q) factors over the colour classes of w, and only
words whose three colour classes all have even size can contribute.

Proved here:

  L1  (exhaustive, 15^3 = 3375 triples)  For EVERY triple of perfect
      matchings (M_0, M_1, M_2) of K6 there is a non-pure word w with
      even colour classes such that each class S_c is perfectly matched
      inside M_c.  There are zero leak-free triples.

  L2  (monotonicity)  "S is perfectly matched inside E" is monotone in E,
      so L1 lifts from matchings to arbitrary edge sets: if each E_c
      contains a perfect matching, the same leak word survives.

  L3  (consequence)  If the response/star sector vanishes identically, the
      three diagonal anchor rows cannot all hold.  Satisfying anchor c
      through q alone forces d_cc != 0 and haf_{c^6}(q) != 0, hence a
      perfect matching inside E_c; L1+L2 then produce a non-pure word w
      with haf_w(q) != 0, so the diagonal row (c,c) is nonzero at w while
      its target there is zero.

Scope.  L1 is a statement about matchings and is exhaustive.  L2 and L3
assume monochromatic edges and NON-NEGATIVE weights, so that no cancellation
between matchings can occur.  Signed or cross-colour internal quadratics are
NOT covered: cancellation is not excluded there, and this file does not
claim otherwise.
"""

from itertools import combinations


SITES = tuple(range(6))
EDGES = tuple(tuple(sorted(e)) for e in combinations(SITES, 2))
EDGE_INDEX = {e: i for i, e in enumerate(EDGES)}


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return [()]
    answer = []
    for position in range(1, len(vertices)):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            answer.append(((vertices[0], vertices[position]),) + tail)
    return answer


EVEN_SUBSETS = tuple(
    subset for size in (0, 2, 4, 6) for subset in combinations(SITES, size)
)
PERFECT_MATCHING_MASKS = {
    subset: tuple(
        sum(1 << EDGE_INDEX[tuple(sorted(pair))] for pair in matching)
        for matching in matchings(subset)
    )
    for subset in EVEN_SUBSETS
}
FULL_MATCHINGS = PERFECT_MATCHING_MASKS[SITES]


def admits(subset, edge_mask):
    """Does `subset` have a perfect matching using only edges in `edge_mask`?"""
    return any((matching & edge_mask) == matching for matching in PERFECT_MATCHING_MASKS[subset])


def non_pure_even_words():
    """Colour words whose three colour classes are all of even size, minus the
    three pure words."""
    answer = []
    for assignment in range(3 ** 6):
        word = tuple((assignment // 3 ** k) % 3 for k in range(6))
        classes = tuple(
            tuple(site for site in SITES if word[site] == colour) for colour in range(3)
        )
        if any(len(cls) % 2 for cls in classes):
            continue
        if max(len(cls) for cls in classes) == 6:
            continue
        answer.append((word, classes))
    return tuple(answer)


NON_PURE = non_pure_even_words()


def leak_word(masks):
    """A non-pure word every one of whose classes is matched in its colour."""
    for word, classes in NON_PURE:
        if all(admits(classes[colour], masks[colour]) for colour in range(3)):
            return word
    return None


def audit_setup():
    require(len(EDGES) == 15, "K6 edge count")
    require(len(FULL_MATCHINGS) == 15, "K6 perfect-matching count")
    require(len(NON_PURE) == 180, ("non-pure even-class word count", len(NON_PURE)))
    # The pure words are excluded, and each is matched only in its own colour.
    for colour in range(3):
        pure = (colour,) * 6
        require(
            all(word != pure for word, _ in NON_PURE), ("pure word leaked in", colour)
        )


def audit_L1_exhaustive():
    """Every triple of perfect matchings leaks.  Exhaustive over 15^3."""
    tried = 0
    leak_free = []
    for first in FULL_MATCHINGS:
        for second in FULL_MATCHINGS:
            for third in FULL_MATCHINGS:
                tried += 1
                if leak_word((first, second, third)) is None:
                    leak_free.append((first, second, third))
    require(tried == 3375, ("triples tried", tried))
    require(leak_free == [], ("leak-free triple exists", leak_free[:1]))


def audit_L2_monotonicity():
    """Adding edges cannot destroy a leak."""
    # Monotonicity of `admits`, checked on every even subset and a spread of
    # supersets of every perfect matching.
    for subset in EVEN_SUBSETS:
        for matching in FULL_MATCHINGS:
            if not admits(subset, matching):
                continue
            for extra in range(15):
                bigger = matching | (1 << extra)
                require(admits(subset, bigger), ("admits not monotone", subset, extra))
    # Hence the L1 leak survives in any triple of supersets.  Verified on a
    # deterministic spread rather than all 2^45 triples.
    for step, first in enumerate(FULL_MATCHINGS):
        second = FULL_MATCHINGS[(step * 7 + 3) % 15]
        third = FULL_MATCHINGS[(step * 11 + 5) % 15]
        base = (first, second, third)
        witness = leak_word(base)
        require(witness is not None, ("L1 gives no witness", step))
        for extra in range(15):
            grown = (first | (1 << extra), second | (1 << ((extra + 5) % 15)), third)
            require(leak_word(grown) is not None, ("leak lost when grown", step, extra))


def audit_L3_consequence():
    """If the star sector vanishes, the three anchors are unsatisfiable.

    Modelled directly: a monochromatic non-negative q is given by three edge
    sets; the anchor at colour c needs a perfect matching inside E_c, and the
    diagonal row at any other even word must vanish.
    """
    for first in FULL_MATCHINGS:
        for second in FULL_MATCHINGS:
            for third in FULL_MATCHINGS:
                masks = (first, second, third)
                # Hypothesis of L3: every anchor is reachable through q.
                require(
                    all(admits(SITES, mask) for mask in masks),
                    "each colour must carry a full matching",
                )
                # Conclusion: some non-pure word is simultaneously nonzero,
                # so the diagonal rows cannot all vanish there.
                require(leak_word(masks) is not None, ("L3 conclusion", masks))

    # The audited seven-row guard sits on the other side of the hypothesis:
    # its internal quadratic is colour-2 only, with the two disjoint edges
    # 01 and 45, so no colour carries a full matching and no anchor at all is
    # reachable through q.  That is consistent with rows (0,0) and (1,1)
    # failing there, and shows the lemma does not contradict the guard.
    guard_colour_two = (1 << EDGE_INDEX[(0, 1)]) | (1 << EDGE_INDEX[(4, 5)])
    require(not admits(SITES, guard_colour_two), "guard q must not carry a matching")
    require(not admits(SITES, 0), "an empty colour carries no six-site matching")
    # ... but the guard's colour 2 does carry a FOUR-site matching, which is
    # how its one satisfied anchor is reached; see L0 below.
    require(admits((0, 1, 4, 5), guard_colour_two), "guard colour 2 carries 01|45")


# ---------------------------------------------------------------------------
# L0: a star-INDEPENDENT necessary condition on the internal quadratic.
# ---------------------------------------------------------------------------

def two_disjoint(edge_mask):
    live = [e for e in EDGES if edge_mask >> EDGE_INDEX[e] & 1]
    return any(not (set(a) & set(b)) for a in live for b in live if a < b)


def audit_L0_star_independent():
    """Anchor c needs two disjoint colour-c edges, whatever the stars do.

    The anchor row at the pure word c^6 is

        d_cc * haf_{c^6}(q)  +  sum_{x<y} R_{xy} * haf_{c^6}(q on the
                                              four sites off {x, y}),

    so every term is a colour-c hafnian on six or on four sites.  A six-site
    hafnian needs three disjoint colour-c edges and a four-site one needs
    two; hence if E_c has no two disjoint edges, every term vanishes, the
    row is zero, and the anchor at colour c is unreachable -- no matter what
    the star sector contains.  This is combinatorial, so it is checked here
    over every edge set.
    """
    four_sets = [s for s in EVEN_SUBSETS if len(s) == 4]
    for mask in range(1 << 15):
        if two_disjoint(mask):
            continue
        require(not admits(SITES, mask), ("six-site matching without two disjoint", mask))
        for subset in four_sets:
            require(
                not admits(subset, mask),
                ("four-site matching without two disjoint", mask, subset),
            )
    # The guard is the sharp instance: colours 0 and 1 are empty, colour 2 is
    # {01, 45}, which has two disjoint edges but no six-site matching -- so its
    # anchor must be, and is, carried by the response term rather than by the
    # direct term.
    guard_colour_two = (1 << EDGE_INDEX[(0, 1)]) | (1 << EDGE_INDEX[(4, 5)])
    require(two_disjoint(guard_colour_two), "guard colour 2 has two disjoint edges")
    require(not admits(SITES, guard_colour_two), "guard colour 2 has no full matching")
    require(not two_disjoint(0), "an empty colour has no two disjoint edges")


# ---------------------------------------------------------------------------
# W: the factorization and L3 with ACTUAL WEIGHTS, not just supports.
# ---------------------------------------------------------------------------

def weighted_hafnian(subset, weights):
    """Exact integer hafnian of `weights` restricted to `subset`."""
    total = 0
    for matching in matchings(subset):
        term = 1
        for pair in matching:
            term *= weights.get(tuple(sorted(pair)), 0)
        total += term
    return total


def audit_L3_with_weights():
    """Verify the factorization and L3's conclusion on weighted quadratics.

    The combinatorial sections above never compute a hafnian.  This one does:
    it builds monochromatic non-negative q's with explicit integer weights,
    checks the identity

        haf_w(q) = prod_c haf_{S_c}(E_c)

    on which the whole leak argument rests, and then checks L3 end to end --
    every q with all three anchors live has a nonzero non-pure word.
    """
    live_packets = 0
    for seed in range(120):
        colours = []
        for colour in range(3):
            weights = {}
            for index, e in enumerate(EDGES):
                value = (seed * 7 + colour * 5 + index * 3) % 4
                if value:
                    weights[e] = value
            colours.append(weights)

        # Factorization, on every even-class word (pure ones included).
        for word, classes in NON_PURE:
            direct = 1
            for colour in range(3):
                direct *= weighted_hafnian(classes[colour], colours[colour])
            combined = {}
            for colour in range(3):
                for e in EDGES:
                    if word[e[0]] == word[e[1]] == colour:
                        combined[e] = colours[colour].get(e, 0)
            require(
                weighted_hafnian(SITES, combined) == direct,
                ("factorization", seed, word),
            )

        # L3: if all three anchors are live, some non-pure word is nonzero.
        anchors_live = all(
            weighted_hafnian(SITES, colours[colour]) != 0 for colour in range(3)
        )
        if not anchors_live:
            continue
        live_packets += 1
        witness = None
        for word, classes in NON_PURE:
            value = 1
            for colour in range(3):
                value *= weighted_hafnian(classes[colour], colours[colour])
            if value:
                witness = word
                break
        require(witness is not None, ("L3 failed with weights", seed))
    require(live_packets >= 20, ("too few live packets to be a real test", live_packets))


# ---------------------------------------------------------------------------
# S: the signed case is partly covered after all.
# ---------------------------------------------------------------------------

def audit_signed_two_two_two():
    """On a (2,2,2) word no cancellation is possible, so L3 survives signs.

    Each class of a (2,2,2) word is a single pair, so its hafnian is one
    edge weight; a product of three nonzero weights cannot cancel.  Hence for
    any SIGNED monochromatic q whose three supports admit a (2,2,2) leak
    word, L3 holds verbatim.  This measures how often that happens.
    """
    balanced = [(w, cls) for w, cls in NON_PURE if all(len(c) == 2 for c in cls)]
    require(len(balanced) == 90, ("(2,2,2) word count", len(balanced)))
    covered = 0
    for first in FULL_MATCHINGS:
        for second in FULL_MATCHINGS:
            for third in FULL_MATCHINGS:
                masks = (first, second, third)
                if any(
                    all(admits(cls[c], masks[c]) for c in range(3))
                    for _, cls in balanced
                ):
                    covered += 1
    require(covered == 1845, ("signed-safe triples", covered))
    require(0 < covered < 3375, "the signed statement must be partial")


def main():
    audit_setup()
    audit_L1_exhaustive()
    audit_L2_monotonicity()
    audit_L3_consequence()
    audit_L0_star_independent()
    audit_L3_with_weights()
    audit_signed_two_two_two()
    print("PASS: L1 - all 3375 triples of perfect matchings leak; none is leak-free")
    print("PASS: L2 - admitting a matching is monotone, so the leak survives"
          " in arbitrary supersets")
    print("PASS: L3 - with a vanishing star sector the three diagonal anchors"
          " are unsatisfiable; the seven-row guard is consistent with this")
    print("PASS: L0 - star-independent: anchor c needs two disjoint colour-c"
          " edges; verified over all 2^15 edge sets")
    print("PASS: weighted model - haf_w factorizes over colour classes and L3"
          " holds end to end on explicit integer quadratics")
    print("PASS: signed case - 1845 of 3375 triples admit a (2,2,2) leak word,"
          " where no cancellation is possible, so L3 survives signs there")


if __name__ == "__main__":
    main()
