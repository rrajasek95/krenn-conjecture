#!/usr/bin/env python3
"""Termwise-dead configurations are rank-3 and cubic, and K_4 is the only
cubic graph whose three colour classes are its only perfect matchings.

Companion note: `notes/termwise-rank3-cubic-uniqueness.md` (hand proofs of
Theorems A, B, C and the exact statement of the stall).

Conventions are those of
`proofs/diagonal-hafnian-recurrence-obstruction.md`: V is a vertex set of
even size n = 2k, W_0,W_1,W_2 are symmetric zero-diagonal scalar edge
matrices over a field, h_c(S) = haf W_c[S] with h_c(empty) = 1, and a
*split* is a proper ordered partition V = S_0 + S_1 + S_2 into even sets
(proper = no part equals V).  A split is LIVE when
h_0(S_0)h_1(S_1)h_2(S_2) != 0.  The packet is ANCHORED when h_c(V) != 0
for all three c, and TERMWISE-DEAD when no split is live.

WHAT THIS ARTIFACT ESTABLISHES

  A  THEOREM A (proved by hand in the note, verified here).  Let the
     packet be anchored.

       (A1)  termwise-dead  =>  TW2: if W_c(u,v) != 0 then
             h_{c'}(V\\{u,v}) = 0 for both c' != c.

     Assume anchored + TW2 from here (a strictly weaker hypothesis than
     anchored + termwise-dead, so the checks below run on far more
     instances than the dead ones).  Put
     E_c = { uv : W_c(u,v) != 0 and h_c(V\\{u,v}) != 0 } (the ESSENTIAL
     edges of colour c).  Then

       (A2)  every edge of E_c is monochromatic, and E_0,E_1,E_2 are
             pairwise disjoint;
       (A3)  every vertex carries an essential edge of every colour;
       (A4)  EVERY STAR HAS RANK EXACTLY 3 in the pencil
             L = x_0W_0 + x_1W_1 + x_2W_2;
       (A5)  an edge carrying two or more colours has
             h_c(V\\{u,v}) = 0 for ALL THREE c.

     CONSEQUENCE (mutual exclusivity).  A rank-2 star is exactly what the
     Fermat/pencil geometry of the session scratch needs: a vertex of
     rank 2 has a *pencil point* in P^2 (the annihilator of the 2-plane
     its star spans), and that scratch derives from it the Fermat
     membership of the point, the tangent lemma at an edge whose two
     endpoints share a point, and the collinearity relations.  By (A4)
     NO vertex of a termwise-dead configuration has a pencil point, so
     that entire geometry is vacuous there.  Section R makes this
     concrete: the 2k-cycle pencil counterexamples -- the packets that
     realize haf(L) = x_0^k + x_1^k + x_2^k over Q(zeta_2k) -- have
     ALL stars of rank exactly 2, verified k = 2..6, hence none of them
     is termwise-dead.

  B  THEOREM B (proved by hand in the note, verified here).  K_4 is the
     ONLY cubic graph whose three perfect matchings form a proper
     3-edge-colouring and are its only perfect matchings.  This is a
     standalone graph theorem; the note states it self-contained.
     Machine content: the subset-A characterisation of the perfect
     matchings of C_2k + chords validated against direct hafnian counts;
     exhaustion over every Hamiltonian-cycle cubic graph to k = 6; the
     staged (B1)+(B2) prune to k = 10; the (B3) minimal-arc search to
     k = 14; and exhaustion over ALL triples of pairwise disjoint perfect
     matchings (no Hamiltonicity assumed) at n = 4,6,8.

  C  THEOREM C (proved by hand in the note, verified here; uniform in k).
     Call W_c MATCHING-FAITHFUL when, for every even S, the existence of
     a perfect matching of G_c[S] = supp(W_c)[S] implies h_c(S) != 0.
     Nonnegative entries, 0/1 entries and algebraically independent
     entries are all matching-faithful.  THEN: for every k >= 3 there is
     NO anchored matching-faithful termwise-dead packet.  The proof chain
     is anchors -> essential monochromatic perfect matchings -> pairwise
     disjoint -> cubic union -> Theorem B supplies a fourth perfect
     matching -> faithfulness makes its induced split live.

     COMPLEMENTARITY with the committed SAT theorem of
     `proofs/diagonal-hafnian-recurrence-obstruction.md`: that theorem
     allows arbitrary cancellation but reaches only n in {6,8,10}, i.e.
     k <= 5.  Theorem C is uniform in k >= 3 but forbids cancellation.
     Neither contains the other.

  S  THE STALL (open, stated exactly).  What survives Theorems A/B/C at
     k >= 3 is a cancellation question: can h_c(S_c) = 0 be arranged on a
     MATCHED set S_c -- one that G_c[S_c] does perfectly match -- for
     EVERY extra perfect matching of the anchor cubic graph and EVERY
     choice of anchor matchings simultaneously?  Two narrowings are
     proved: (S1) a cancelling part has |S_c| >= 4; (S2) the cancelling
     colour needs an edge of G_c inside S_c outside M_c.  Measured here:
     at k = 3 every one of the 48 extra perfect matchings over all 32
     anchor cubic graphs has profile (2,2,2), so (S1) forbids every
     cancellation and k = 3 falls with no faithfulness hypothesis at all;
     at k = 4 not one of the 5832 extra perfect matchings over the 1884
     anchor graphs has all parts <= 2, so the same argument reproves
     nothing at k = 4,5 and the SAT theorem is still needed there.

  K  THE k = 2 BOUNDARY.  K_4 IS termwise-dead, so no theorem here may
     exclude it.  Theorem A holds at k = 2 (K_4 has rank 3 at every
     vertex).  Theorem C is stated for k >= 3.  Inside Theorem B the
     hypothesis k >= 3 enters at exactly two places, (B1) and (B2)/(B3),
     and section K exhibits both escapes machine-checked.

DISCIPLINE.  Exact stdlib arithmetic only: int, Fraction, and an exact
integer cyclotomic ring Z[s]/Phi_m(s) built here.  No floats, no numpy,
no bare asserts (every check goes through `require`, which raises and
therefore survives `python3 -O`).  No SAT solver and no third-party
import, so every section runs under every interpreter mode.  One frozen
sha256 ledger, hashing computed content; every boolean in it is
computed.  Krenn's conjecture remains open.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from hashlib import sha256

EXPECTED_LEDGER_SHA256 = (
    "021aa7b60891b2268578d96191dfeedbe7d001d64ca8e73c2862c28dfb75d619")


def require(condition, detail):
    """Assertion that survives `python3 -O` (never use a bare assert)."""
    if not condition:
        raise RuntimeError(detail)


# --------------------------------------------------------------- hashing


def canonical(value):
    """Canonical JSON-able image of exact data (Fractions become strings)."""
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, Fraction):
        return "F" + str(value)
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return {str(canonical(key)): canonical(item)
                for key, item in sorted(value.items(), key=lambda kv: str(kv[0]))}
    if isinstance(value, (list, tuple)):
        return [canonical(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted(str(canonical(item)) for item in value)
    raise RuntimeError("uncanonicalizable value in the ledger: %r" % (value,))


def content_hash(value):
    encoded = json.dumps(canonical(value), sort_keys=True, separators=(",", ":"))
    return sha256(encoded.encode("ascii")).hexdigest()


# -------------------------------------------------------------- hafnians


def hafnian_table(n, weight):
    """h[mask] = haf(W[mask]) for every even mask, by lowest-vertex pivot.

    Exact: the entries are whatever ring elements `weight` returns.  Odd
    masks are absent from the table by construction.  `zero` and `one`
    default to the integers; the cyclotomic sections pass their own.
    """
    table = {0: 1}
    for mask in range(1 << n):
        if mask.bit_count() % 2 or mask == 0:
            continue
        pivot = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << pivot)
        total = 0
        other = rest
        while other:
            bit = other & -other
            vertex = bit.bit_length() - 1
            other ^= bit
            cell = weight(pivot, vertex)
            if cell:
                total = total + cell * table[rest ^ bit]
        table[mask] = total
    return table


def ring_hafnian_table(n, entries, zero, one):
    """The same recursion over an arbitrary exact commutative ring."""
    table = {0: one}
    for mask in range(1 << n):
        if mask.bit_count() % 2 or mask == 0:
            continue
        pivot = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << pivot)
        total = zero
        other = rest
        while other:
            bit = other & -other
            vertex = bit.bit_length() - 1
            other ^= bit
            cell = entries.get(frozenset((pivot, vertex)))
            if cell is not None and cell:
                total = total + cell * table[rest ^ bit]
        table[mask] = total
    return table


def dict_weight(entries):
    """Edge-weight callable for a dict keyed by frozenset({u,v})."""

    def weight(u, v):
        return entries.get(frozenset((u, v)), 0)

    return weight


def matching_entries(matching):
    return {frozenset(edge): 1 for edge in matching}


def perfect_matchings(vertices):
    """Every perfect matching of a vertex list, as a tuple of ordered pairs."""
    vertices = list(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def pm_count_graph(n, edges):
    """The number of perfect matchings of a graph, as a 0/1 hafnian."""
    return hafnian_table(n, dict_weight({frozenset(edge): 1
                                         for edge in edges}))[(1 << n) - 1]


def deterministic_ints(seed, count, low=-4, high=4):
    """Tiny reproducible LCG; no `random`, no numpy, no floats."""
    state = seed
    out = []
    span = high - low + 1
    for _ in range(count):
        state = (1103515245 * state + 12345) % (1 << 31)
        out.append(low + state % span)
    return out


def one_factors(n):
    """Round-robin one-factorization of K_n: the n-1 factors F_0..F_{n-2}.

    Vertex n-1 plays the role of infinity; F_r pairs it with r and pairs
    x with 2r-x modulo m = n-1 for the other vertices.  The committed
    companion `notes/diagonal-termwise-census-and-pencil-guard.md` proves
    that the first three factors have pairwise Hamiltonian unions at every
    even n; that Hamiltonicity is RECOMPUTED here rather than cited, so the
    two artifacts corroborate each other.
    """
    require(n % 2 == 0 and n >= 4, "one_factors needs an even n >= 4")
    modulus = n - 1
    factors = []
    for r in range(modulus):
        matching = [(r, n - 1)]
        for offset in range(1, n // 2):
            first = (r + offset) % modulus
            second = (r - offset) % modulus
            matching.append((min(first, second), max(first, second)))
        factors.append(tuple(sorted(matching)))
    seen = set()
    for factor in factors:
        cover = set()
        for u, v in factor:
            require(u != v, "one-factor carries a loop")
            cover |= {u, v}
            require(frozenset((u, v)) not in seen,
                    "the round-robin factors are not pairwise disjoint")
            seen.add(frozenset((u, v)))
        require(cover == set(range(n)),
                "a round-robin factor is not a perfect matching")
    return tuple(factors)


def union_is_hamiltonian(n, first, second):
    """Is the union of two disjoint perfect matchings a single n-cycle?"""
    adjacency = {vertex: [] for vertex in range(n)}
    for u, v in list(first) + list(second):
        adjacency[u].append(v)
        adjacency[v].append(u)
    if any(len(neighbours) != 2 for neighbours in adjacency.values()):
        return False
    seen, current, previous = {0}, 0, None
    while True:
        following = next((w for w in adjacency[current] if w != previous), None)
        if following is None or following == 0:
            break
        if following in seen:
            return False
        seen.add(following)
        previous, current = current, following
    return len(seen) == n


# ------------------------------------------------ polynomials in x0,x1,x2


def poly_add(left, right):
    out = dict(left)
    for key, value in right.items():
        out[key] = out.get(key, 0) + value
    return {key: value for key, value in out.items() if value}


def poly_mul(left, right):
    out = {}
    for key_left, value_left in left.items():
        for key_right, value_right in right.items():
            key = (key_left[0] + key_right[0],
                   key_left[1] + key_right[1],
                   key_left[2] + key_right[2])
            out[key] = out.get(key, 0) + value_left * value_right
    return {key: value for key, value in out.items() if value}


def poly_hafnian(n, entry):
    """Hafnian of a matrix with polynomial entries, same pivot recursion."""
    table = {0: {(0, 0, 0): 1}}
    for mask in range(1 << n):
        if mask.bit_count() % 2 or mask == 0:
            continue
        pivot = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << pivot)
        total = {}
        other = rest
        while other:
            bit = other & -other
            vertex = bit.bit_length() - 1
            other ^= bit
            cell = entry(pivot, vertex)
            if cell:
                total = poly_add(total, poly_mul(cell, table[rest ^ bit]))
        table[mask] = total
    return table[(1 << n) - 1]


def pencil_entry(packet):
    """The entry callable of x_0 W_0 + x_1 W_1 + x_2 W_2."""

    def entry(u, v):
        key = frozenset((u, v))
        out = {}
        for colour in range(3):
            cell = packet[colour].get(key, 0)
            if cell:
                out[tuple(1 if index == colour else 0 for index in range(3))] = cell
        return out

    return entry


# ------------------------------------------------------------ rank by minors


def minor_rank(rows):
    """Rank of a list of 3-vectors over an integral DOMAIN, without division.

    Only ring operations and zero-tests are used, so this works verbatim
    over Z, over Q, and over the integer cyclotomic ring of section R
    (Z[s]/Phi_m(s), a domain because Phi_m is irreducible over Q).  The
    routine is cross-validated against an independent Fraction Gaussian
    elimination in `section_rank_controls`.
    """
    rows = [row for row in rows if any(row)]
    if not rows:
        return 0
    rank = 1
    for left, right in itertools.combinations(rows, 2):
        for i, j in itertools.combinations(range(3), 2):
            if left[i] * right[j] - left[j] * right[i]:
                rank = 2
                break
        if rank == 2:
            break
    if rank < 2:
        return 1
    for a, b, c in itertools.combinations(rows, 3):
        determinant = (a[0] * (b[1] * c[2] - b[2] * c[1])
                       - a[1] * (b[0] * c[2] - b[2] * c[0])
                       + a[2] * (b[0] * c[1] - b[1] * c[0]))
        if determinant:
            return 3
    return 2


def gaussian_rank(rows):
    """Independent rank over Q by elimination; the control for minor_rank."""
    working = [[Fraction(cell) for cell in row] for row in rows]
    rank = 0
    for column in range(3):
        pivot = None
        for index in range(rank, len(working)):
            if working[index][column]:
                pivot = index
                break
        if pivot is None:
            continue
        working[rank], working[pivot] = working[pivot], working[rank]
        head = working[rank]
        for index in range(len(working)):
            if index != rank and working[index][column]:
                factor = working[index][column] / head[column]
                working[index] = [a - factor * b
                                  for a, b in zip(working[index], head)]
        rank += 1
    return rank


# ------------------------------------------------ the packet and its structure


def packet_tables(n, packet):
    return [hafnian_table(n, dict_weight(entries)) for entries in packet]


def anchors_of(n, tables):
    full = (1 << n) - 1
    return tuple(table[full] for table in tables)


def cofactor(n, tables, colour, u, v):
    return tables[colour][((1 << n) - 1) ^ (1 << u) ^ (1 << v)]


def tw2_violations(n, packet, tables):
    """Pairs (uv, c, c') with W_c(u,v) != 0, c' != c and h_{c'}(V\\{u,v}) != 0.

    Each such triple names an explicitly live split of shape (0,2,n-2):
    {u,v} in colour c against V\\{u,v} in colour c'.
    """
    out = []
    for u in range(n):
        for v in range(u + 1, n):
            key = frozenset((u, v))
            for colour in range(3):
                if not packet[colour].get(key, 0):
                    continue
                for other in range(3):
                    if other != colour and cofactor(n, tables, other, u, v):
                        out.append(((u, v), colour, other))
    return out


def essential_edges(n, packet, tables, colour):
    """E_c = { uv : W_c(u,v) != 0 and h_c(V\\{u,v}) != 0 }."""
    return frozenset(frozenset((u, v))
                     for u in range(n) for v in range(u + 1, n)
                     if packet[colour].get(frozenset((u, v)), 0)
                     and cofactor(n, tables, colour, u, v))


def star_rows(n, packet, u):
    rows = []
    for v in range(n):
        if v == u:
            continue
        row = [packet[colour].get(frozenset((u, v)), 0) for colour in range(3)]
        if any(row):
            rows.append(row)
    return rows


def star_rank(n, packet, u):
    return minor_rank(star_rows(n, packet, u))


def proper_splits(n):
    """Every proper ordered even split of V, as a triple of masks."""
    full = (1 << n) - 1
    out = []
    for colouring in itertools.product(range(3), repeat=n):
        masks = [0, 0, 0]
        for vertex, colour in enumerate(colouring):
            masks[colour] |= 1 << vertex
        if any(mask.bit_count() % 2 for mask in masks):
            continue
        if any(mask == full for mask in masks):
            continue
        out.append(tuple(masks))
    return out


_SPLIT_CACHE = {}


def cached_splits(n):
    if n not in _SPLIT_CACHE:
        _SPLIT_CACHE[n] = proper_splits(n)
    return _SPLIT_CACHE[n]


def live_splits(n, tables):
    return [masks for masks in cached_splits(n)
            if tables[0][masks[0]] and tables[1][masks[1]]
            and tables[2][masks[2]]]


def termwise_dead(n, tables):
    for masks in cached_splits(n):
        if tables[0][masks[0]] and tables[1][masks[1]] and tables[2][masks[2]]:
            return False
    return True


# ============================================================== section A


def check_theorem_a(n, packet, label):
    """Verify (A1)-(A5) on one packet; returns its structure record.

    (A2)-(A5) are checked exactly when the packet is anchored and TW2-clean,
    which is what the hand proof assumes.  When it is not, the record says
    so and the star ranks are still recorded, so a caller can use the
    record as a NEGATIVE probe.
    """
    tables = packet_tables(n, packet)
    anchors = anchors_of(n, tables)
    anchored = all(anchors)
    violations = tw2_violations(n, packet, tables)
    essential = [essential_edges(n, packet, tables, colour) for colour in range(3)]
    ranks = {u: star_rank(n, packet, u) for u in range(n)}
    record = {
        "label": label,
        "n": n,
        "anchored": anchored,
        "tw2_violations": len(violations),
        "essential_sizes": [len(entry) for entry in essential],
        "star_ranks": sorted({rank for rank in ranks.values()}),
        "hypotheses_met": bool(anchored and not violations),
    }

    # (A1) is a derivation, not an assumption: termwise-deadness must imply
    # TW2-cleanness.  Whenever the packet is small enough to decide, both
    # directions of that implication are exercised -- a TW2 violation must
    # come with the live split its proof names.
    if n <= 12:
        dead = termwise_dead(n, tables)
        record["termwise_dead"] = dead
        require(not (dead and violations),
                "A1 fails on %s: the packet is termwise-dead yet a pair "
                "carries colour %s while its complement stays alive in "
                "colour %s" % (label, violations[0][1] if violations else None,
                               violations[0][2] if violations else None))
    for (u, v), colour, other in violations:
        # The split TW2's proof names: {u,v} in colour c, V\{u,v} in c'.
        pair_mask = (1 << u) | (1 << v)
        require(tables[colour][pair_mask]
                == packet[colour].get(frozenset((u, v)), 0),
                "the hafnian of a two-set disagrees with its edge weight on "
                "%s at the pair (%d,%d)" % (label, u, v))
        require(tables[colour][pair_mask]
                * tables[other][((1 << n) - 1) ^ pair_mask] != 0,
                "the split named by TW2's own proof is not live on %s at the "
                "pair (%d,%d)" % (label, u, v))

    if not record["hypotheses_met"]:
        return record, tables

    for colour in range(3):
        for edge in essential[colour]:
            u, v = sorted(edge)
            for other in range(3):
                if other == colour:
                    continue
                require(packet[other].get(edge, 0) == 0,
                        "A2 fails on %s: the essential edge (%d,%d) of colour "
                        "%d also carries colour %d, so essential edges are not "
                        "monochromatic" % (label, u, v, colour, other))
    for first, second in itertools.combinations(range(3), 2):
        require(not (essential[first] & essential[second]),
                "A2 fails on %s: the essential graphs of colours %d and %d "
                "are not disjoint" % (label, first, second))
    for u in range(n):
        for colour in range(3):
            require(any(u in edge for edge in essential[colour]),
                    "A3 fails on %s: vertex %d carries no essential edge of "
                    "colour %d although the anchor h_%d(V) is nonzero"
                    % (label, u, colour, colour))
    for u in range(n):
        require(ranks[u] == 3,
                "A4 fails on %s: the star at vertex %d has rank %d, not 3"
                % (label, u, ranks[u]))
    for u in range(n):
        for v in range(u + 1, n):
            edge = frozenset((u, v))
            carried = [colour for colour in range(3) if packet[colour].get(edge, 0)]
            if len(carried) < 2:
                continue
            for colour in range(3):
                require(cofactor(n, tables, colour, u, v) == 0,
                        "A5 fails on %s: the two-coloured edge (%d,%d) leaves "
                        "h_%d(V\\{u,v}) nonzero" % (label, u, v, colour))
    return record, tables


def k4_packet():
    """The three one-factors of K_4: the k = 2 termwise-dead configuration."""
    return [matching_entries(factor) for factor in one_factors(4)]


def section_k4():
    """K_4: termwise-dead, TW2-clean, rank 3 everywhere, exactly 3 matchings."""
    packet = k4_packet()
    record, tables = check_theorem_a(4, packet, "K_4 one-factorisation")
    require(record["termwise_dead"],
            "the K_4 one-factorisation is not termwise-dead, so the k=2 "
            "boundary case the theorems must not exclude has gone missing")
    require(record["anchored"] and record["tw2_violations"] == 0,
            "the K_4 one-factorisation is not anchored and TW2-clean")
    require(record["essential_sizes"] == [2, 2, 2],
            "K_4: an essential graph is not the full colour class")
    require(record["star_ranks"] == [3],
            "K_4: a star does not have rank 3")
    union = {}
    for entries in packet:
        union.update({edge: 1 for edge in entries})
    matchings = hafnian_table(4, dict_weight(union))[15]
    require(matchings == 3,
            "K_4 has %d perfect matchings, not the three colour classes"
            % matchings)
    pencil = poly_hafnian(4, pencil_entry(packet))
    require(pencil == {(2, 0, 0): 1, (0, 2, 0): 1, (0, 0, 2): 1},
            "K_4: haf(x_0W_0 + x_1W_1 + x_2W_2) is not x_0^2 + x_1^2 + x_2^2")
    record["perfect_matchings_of_the_union"] = matchings
    record["pencil"] = sorted([list(key), value]
                              for key, value in pencil.items())
    return record


def section_hamiltonian_family(orders):
    """D(n): TW2-clean, rank 3, NOT dead, and #live = #PM(union) - 3 exactly.

    D(n) is the 0/1 packet of the first three round-robin one-factors.  Its
    three colour supports are disjoint perfect matchings, so h_c(S) != 0
    exactly when S is a union of M_c-edges and then h_c(S) = 1.  Hence the
    live splits biject with the perfect matchings of the union that are not
    one of the three colour classes -- the PACKET DICTIONARY, whose exact
    count is required below.
    """
    records = []
    for n in orders:
        factors = one_factors(n)[:3]
        for first, second in itertools.combinations(range(3), 2):
            require(union_is_hamiltonian(n, factors[first], factors[second]),
                    "D(%d): the union of colours %d and %d is not a single "
                    "Hamiltonian cycle" % (n, first, second))
        packet = [matching_entries(factor) for factor in factors]
        record, tables = check_theorem_a(n, packet, "D(%d)" % n)
        require(record["anchored"] and record["tw2_violations"] == 0,
                "D(%d) is not anchored and TW2-clean, so Theorem A's "
                "hypotheses are not exercised on it" % n)
        require(record["star_ranks"] == [3],
                "D(%d): a star does not have rank 3" % n)
        require(record["termwise_dead"] is False,
                "D(%d) is termwise-dead, which would contradict Theorem C "
                "(its 0/1 entries are matching-faithful)" % n)
        union = {}
        for entries in packet:
            union.update({edge: 1 for edge in entries})
        matchings = hafnian_table(n, dict_weight(union))[(1 << n) - 1]
        live = live_splits(n, tables)
        require(len(live) == matchings - 3,
                "D(%d): the packet dictionary fails -- %d live splits against "
                "%d perfect matchings of the union" % (n, len(live), matchings))
        require(live, "D(%d): no live split at all, so the dictionary is "
                      "vacuous here" % n)
        shapes = {}
        for masks in live:
            shape = tuple(sorted(mask.bit_count() for mask in masks))
            shapes[shape] = shapes.get(shape, 0) + 1
        require(all(0 not in shape for shape in shapes),
                "D(%d): a live split has an empty part, contradicting the "
                "Hamiltonian-triple lemma of "
                "notes/diagonal-termwise-census-and-pencil-guard.md, "
                "recomputed above" % n)
        record["perfect_matchings_of_the_union"] = matchings
        record["live_splits"] = len(live)
        record["live_shapes"] = {str(list(shape)): count
                                 for shape, count in sorted(shapes.items())}
        records.append(record)
    return records


def section_exhaustive_n4():
    """EXHAUSTIVE over every 0/1 packet at n = 4: 2^18 = 262144 of them.

    The 2^6 = 64 symmetric 0/1 matrices on four vertices are enumerated
    once with their hafnian tables, and every ordered triple is examined.
    """
    n, full = 4, 15
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    matrices = []
    for bits in range(1 << len(pairs)):
        entries = {frozenset(pairs[index]): 1
                   for index in range(len(pairs)) if bits >> index & 1}
        matrices.append((entries, hafnian_table(n, dict_weight(entries))))
    require(len(matrices) == 64,
            "the n=4 census does not enumerate all 2^6 symmetric 0/1 matrices")
    splits = cached_splits(n)
    require(len(splits) == 18,
            "the n=4 census does not see all 18 proper ordered even splits")

    factor_supports = {frozenset(frozenset(edge) for edge in factor)
                       for factor in one_factors(4)}
    examined = anchored = clean = dead = 0
    dead_supports = []
    for first in range(64):
        for second in range(64):
            for third in range(64):
                examined += 1
                triple = (matrices[first], matrices[second], matrices[third])
                tables = [entry[1] for entry in triple]
                if not (tables[0][full] and tables[1][full] and tables[2][full]):
                    continue
                anchored += 1
                packet = [entry[0] for entry in triple]
                if tw2_violations(n, packet, tables):
                    continue
                clean += 1
                check_theorem_a(n, packet, "n=4 census %d/%d/%d"
                                % (first, second, third))
                if termwise_dead(n, tables):
                    dead += 1
                    dead_supports.append(tuple(
                        frozenset(edge for edge, cell in entries.items() if cell)
                        for entries in packet))
    require(examined == 1 << 18,
            "the n=4 census examined %d packets, not the 2^18 = 262144 it "
            "advertises" % examined)
    require(anchored > 0 and clean > 0,
            "the n=4 census is vacuous: no anchored TW2-clean packet was "
            "found, so (A2)-(A5) were never exercised on it")
    require(dead == 6,
            "the n=4 census found %d termwise-dead 0/1 packets, not the 6 "
            "colour-orderings of the K_4 one-factorisation" % dead)
    orderings = sum(1 for supports in dead_supports
                    if all(support in factor_supports for support in supports)
                    and len(set(supports)) == 3)
    require(orderings == dead,
            "%d of the %d termwise-dead 0/1 packets at n=4 are not ordered "
            "triples of distinct one-factors of K_4" % (dead - orderings, dead))
    return {"examined": examined, "anchored": anchored,
            "anchored_and_tw2_clean": clean, "termwise_dead": dead,
            "dead_that_are_k4_colour_orderings": orderings}


def _draws(seed, count):
    """A deterministic draw stream: `next(stream)` yields 0..999."""
    return iter(deterministic_ints(seed, count, low=0, high=999))


def _distinct_factor_indices(stream, total):
    chosen = []
    for _ in range(3):
        candidate = next(stream) % total
        while candidate in chosen:
            candidate = (candidate + 1) % total
        chosen.append(candidate)
    return chosen


def signed_packet(n, seed):
    """A deterministic signed packet: three one-factors plus a few extras."""
    factors = one_factors(n)
    stream = _draws(seed, 200)
    order = _distinct_factor_indices(stream, len(factors))
    weights = (1, -1, 2, -3)
    packet = []
    for colour in range(3):
        entries = {}
        for edge in factors[order[colour]]:
            entries[frozenset(edge)] = weights[next(stream) % 4]
        for _ in range(next(stream) % 3):
            u = next(stream) % n
            v = next(stream) % n
            weight = weights[next(stream) % 4]
            if u != v:
                entries.setdefault(frozenset((u, v)), weight)
        packet.append(entries)
    return packet


def section_signed_packets(trials):
    """Deterministic SIGNED packets at n = 6,8, with the clean ones counted."""
    examined = anchored = clean = 0
    rank_profile = {}
    for trial in range(trials):
        n = 6 if trial % 2 == 0 else 8
        packet = signed_packet(n, 20260803 + 7919 * trial)
        tables = packet_tables(n, packet)
        # A bookkeeping identity that pins the hafnian table itself:
        # h_c({u,v}) must equal W_c(u,v) for every pair and every colour.
        for colour in range(3):
            for u in range(n):
                for v in range(u + 1, n):
                    require(tables[colour][(1 << u) | (1 << v)]
                            == packet[colour].get(frozenset((u, v)), 0),
                            "the hafnian of a two-set disagrees with its edge "
                            "weight on signed packet %d" % trial)
        examined += 1
        if not all(anchors_of(n, tables)):
            continue
        anchored += 1
        if tw2_violations(n, packet, tables):
            continue
        clean += 1
        record, _tables = check_theorem_a(n, packet, "signed packet %d" % trial)
        key = str(record["star_ranks"])
        rank_profile[key] = rank_profile.get(key, 0) + 1
    require(clean > 0,
            "the signed-packet family is vacuous: not one packet is anchored "
            "and TW2-clean, so (A2)-(A5) were never exercised on it")
    require(rank_profile == {"[3]": clean},
            "a signed anchored TW2-clean packet has a star of rank other "
            "than 3: %s" % rank_profile)
    return {"trials": examined, "anchored": anchored,
            "anchored_and_tw2_clean": clean, "rank_profile": rank_profile}


def section_theorem_a_negative_probes():
    """Negative probes: each pins one direction of a definition.

    Without these the section would only ever confirm the conclusions on
    instances that satisfy the hypotheses, and a check that can never fire
    proves nothing.
    """
    probes = []

    # P1  A bichromatic essential edge.  Start from K_4 and paint the
    #     colour-0 edge {0,1} with colour 1 as well.  (A2)'s conclusion must
    #     now FAIL, the TW2 scan must see it, and the packet must lose its
    #     termwise-deadness with the live split TW2's proof names.
    packet = k4_packet()
    target = sorted(essential_edges(4, packet,
                                    packet_tables(4, packet), 0),
                    key=sorted)[0]
    packet[1] = dict(packet[1])
    packet[1][target] = 1
    tables = packet_tables(4, packet)
    require(all(anchors_of(4, tables)),
            "probe P1: the perturbed K_4 packet lost its anchors, so it "
            "probes nothing about (A2)")
    essential0 = essential_edges(4, packet, tables, 0)
    require(target in essential0,
            "probe P1 is not discriminating: the painted edge is not "
            "essential for colour 0 in the perturbed packet")
    require(packet[1].get(target, 0) != 0,
            "probe P1 is not discriminating: the second colour was not "
            "actually painted onto the essential edge")
    violations = tw2_violations(4, packet, tables)
    require(violations,
            "probe P1: an essential edge was made bichromatic and the TW2 "
            "scan still reports no violation, so the scan cannot fire")
    dead = termwise_dead(4, tables)
    require(not dead,
            "probe P1: a packet with a bichromatic essential edge is still "
            "termwise-dead, contradicting (A1)")
    probes.append({"probe": "P1 bichromatic essential edge",
                   "tw2_violations": len(violations),
                   "termwise_dead": dead})

    # P2  A rank-2 star.  Give every edge at vertex 0 the same two colours;
    #     the star at 0 then spans a 2-plane, (A4) fails, and the packet
    #     cannot be termwise-dead.
    packet = [
        {frozenset((0, 1)): 1, frozenset((2, 3)): 1},
        {frozenset((0, 2)): 1, frozenset((0, 3)): 2, frozenset((1, 3)): 1},
        {frozenset((0, 2)): 1, frozenset((0, 3)): 2, frozenset((1, 2)): 1},
    ]
    tables = packet_tables(4, packet)
    ranks = {u: star_rank(4, packet, u) for u in range(4)}
    require(ranks[0] == 2,
            "probe P2 is not discriminating: the designed rank-2 star at "
            "vertex 0 reports rank %d" % ranks[0])
    require(all(anchors_of(4, tables)),
            "probe P2: the rank-2 packet is not anchored, so (A4)'s "
            "hypotheses do not apply and it probes nothing")
    dead = termwise_dead(4, tables)
    require(not dead,
            "probe P2: an anchored packet with a rank-2 star is termwise-dead, "
            "contradicting (A4)")
    probes.append({"probe": "P2 rank-2 star", "ranks": sorted(ranks.values()),
                   "termwise_dead": dead})

    # P3  A vertex missing a colour.  Delete colour 2 from vertex 0's star
    #     entirely: (A3) must fail there, and the anchor h_2(V) must vanish,
    #     which is exactly the mechanism of (A3)'s Laplace proof.
    packet = k4_packet()
    packet[2] = {edge: cell for edge, cell in packet[2].items() if 0 not in edge}
    tables = packet_tables(4, packet)
    require(tables[2][15] == 0,
            "probe P3 is not discriminating: deleting colour 2 from vertex 0's "
            "star left the anchor h_2(V) nonzero")
    require(not essential_edges(4, packet, tables, 2),
            "probe P3: colour 2 still has an essential edge although its "
            "anchor vanished")
    probes.append({"probe": "P3 vertex missing a colour",
                   "anchor_2": tables[2][15],
                   "essential_2": len(essential_edges(4, packet, tables, 2))})

    return probes


def cofactor_terms(a, b, c):
    """The three signed cofactor terms of det[a;b;c], in position order."""
    return (a[0] * (b[1] * c[2] - b[2] * c[1]),
            -a[1] * (b[0] * c[2] - b[2] * c[0]),
            a[2] * (b[0] * c[1] - b[1] * c[0]))


# Designed SINGULAR triples with every row nonzero.  Each is rank 2, so
# `minor_rank` must return 2; and each has a NONZERO cofactor term in the
# positions listed, so corrupting the sign of a cofactor at one of those
# positions changes the determinant from 0 and makes the routine answer 3.
# Between them the three matrices cover all three positions, which closes
# the hole a sign flip in the determinant would otherwise slip through:
# without them the whole checker passes with a corrupted third cofactor.
SINGULAR_ALL_NONZERO = [
    ([[0, 1, 1], [1, 0, 1], [1, 1, 2]], (1, 2)),
    ([[1, 0, 1], [0, 1, 1], [1, 1, 2]], (0, 2)),
    ([[1, 1, 0], [1, 0, 1], [2, 1, 1]], (0, 1)),
]


def section_rank_controls():
    """minor_rank pinned in both directions, against an independent route."""
    designed = [
        ([], 0),
        ([[0, 0, 0], [0, 0, 0]], 0),
        ([[2, 0, 0], [-6, 0, 0]], 1),
        ([[1, 2, 3], [2, 4, 6], [-1, -2, -3]], 1),
        ([[1, 0, 0], [0, 1, 0], [1, 1, 0]], 2),
        ([[1, 1, 1], [1, 2, 4], [1, 3, 9], [2, 3, 5]], 3),
        ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 3),
    ]
    designed += [(rows, 2) for rows, _positions in SINGULAR_ALL_NONZERO]
    for rows, expected in designed:
        got = minor_rank(rows)
        require(got == expected,
                "minor_rank returned %d on a designed rank-%d input, so the "
                "rank routine is not pinned" % (got, expected))
        require(gaussian_rank(rows) == expected,
                "the independent Gaussian rank disagrees with the designed "
                "rank %d" % expected)

    # The determinant-sign controls are only worth anything if each of them
    # really does carry a nonzero cofactor at the positions it claims, and
    # if between them all three positions are covered.
    covered = set()
    for rows, positions in SINGULAR_ALL_NONZERO:
        require(all(any(cell for cell in row) for row in rows),
                "a determinant-sign control has a zero row, so it never "
                "reaches the 3x3 stage of minor_rank")
        terms = cofactor_terms(*rows)
        require(sum(terms) == 0,
                "a determinant-sign control is not singular, so it does not "
                "pin the rank-2 verdict")
        for position in positions:
            require(terms[position] != 0,
                    "the determinant-sign control claims a nonzero cofactor "
                    "at position %d but that term is zero, so a sign flip "
                    "there would go undetected" % position)
            covered.add(position)
    require(covered == {0, 1, 2},
            "the determinant-sign controls cover only the cofactor positions "
            "%s, so a sign flip at the remaining position is invisible"
            % sorted(covered))

    seen = {}
    # Twelve draws per case: nine entries and three keep-bits, so that whole
    # rows are sometimes zeroed and rank 0 actually occurs.
    values = deterministic_ints(31337, 12 * 400, low=-2, high=2)
    for trial in range(400):
        block = values[12 * trial:12 * trial + 12]
        rows = [block[0:3], block[3:6], block[6:9]]
        for index in range(3):
            if block[9 + index] <= 0:
                rows[index] = [0, 0, 0]
        by_minors = minor_rank(rows)
        by_elimination = gaussian_rank(rows)
        require(by_minors == by_elimination,
                "minor_rank and Gaussian elimination disagree on a "
                "deterministic 3x3 integer input: %d vs %d"
                % (by_minors, by_elimination))
        seen[by_minors] = seen.get(by_minors, 0) + 1
    require(set(seen) == {0, 1, 2, 3},
            "the minor_rank cross-validation never produced all four ranks, "
            "so it is not discriminating: %s" % seen)

    # A second batch with NO row zeroed, so that every case reaches the 3x3
    # determinant.  Zeroed rows short-circuit before it, which is why the
    # first batch alone leaves the determinant almost untested.
    nonzero_seen = {}
    values = deterministic_ints(90210, 9 * 400, low=-2, high=2)
    for trial in range(400):
        block = values[9 * trial:9 * trial + 9]
        rows = [block[0:3], block[3:6], block[6:9]]
        if not all(any(cell for cell in row) for row in rows):
            continue
        by_minors = minor_rank(rows)
        by_elimination = gaussian_rank(rows)
        require(by_minors == by_elimination,
                "minor_rank and Gaussian elimination disagree on a "
                "deterministic 3x3 integer input with three nonzero rows: "
                "%d vs %d" % (by_minors, by_elimination))
        nonzero_seen[by_minors] = nonzero_seen.get(by_minors, 0) + 1
    require(2 in nonzero_seen and 3 in nonzero_seen,
            "the three-nonzero-row batch never produced both a rank-2 and a "
            "rank-3 case, so the 3x3 determinant is not discriminated: %s"
            % nonzero_seen)
    return {"designed_cases": len(designed), "random_cases": 400,
            "rank_histogram": {str(key): value
                               for key, value in sorted(seen.items())},
            "cofactor_positions_covered": sorted(covered),
            "three_nonzero_row_cases": sum(nonzero_seen.values()),
            "three_nonzero_row_histogram": {
                str(key): value for key, value in sorted(nonzero_seen.items())}}


# ============================================================== section R


def integer_poly_divide(numerator, divisor):
    """Exact quotient of two integer polynomials (little-endian, monic)."""
    numerator = list(numerator)
    degree = len(divisor) - 1
    require(divisor[-1] == 1, "the divisor of an exact division is not monic")
    quotient = [0] * max(1, len(numerator) - degree)
    for index in range(len(numerator) - 1, degree - 1, -1):
        coefficient = numerator[index]
        if not coefficient:
            continue
        quotient[index - degree] = coefficient
        for offset in range(degree + 1):
            numerator[index - degree + offset] -= coefficient * divisor[offset]
    require(not any(numerator),
            "an exact polynomial division left a remainder")
    return tuple(quotient)


def cyclotomic_polynomial(order, _cache={}):
    """Phi_order, computed from s^order - 1 by exact division."""
    if order in _cache:
        return _cache[order]
    numerator = [0] * (order + 1)
    numerator[0] = -1
    numerator[order] = 1
    numerator = tuple(numerator)
    for divisor in range(1, order):
        if order % divisor:
            continue
        numerator = integer_poly_divide(numerator,
                                        cyclotomic_polynomial(divisor))
    _cache[order] = numerator
    return numerator


class CyclotomicInteger:
    """An element of Z[s]/Phi_m(s), exact over the integers.

    Phi_m is irreducible over Q (classical), so this ring embeds in the
    field Q(zeta_m) and is an INTEGRAL DOMAIN: an element is zero here
    exactly when its complex image under s -> exp(2 pi i / m) is zero.
    That is all `minor_rank` needs -- no inverses are ever taken, so no
    field arithmetic is implemented.
    """

    __slots__ = ("order", "coefficients")

    def __init__(self, order, coefficients):
        modulus = cyclotomic_polynomial(order)
        degree = len(modulus) - 1
        working = list(coefficients)
        for index in range(len(working) - 1, degree - 1, -1):
            coefficient = working[index]
            if not coefficient:
                continue
            for offset in range(degree + 1):
                working[index - degree + offset] -= coefficient * modulus[offset]
        working = working[:degree]
        while len(working) < degree:
            working.append(0)
        self.order = order
        self.coefficients = tuple(working)

    def _coerce(self, other):
        if isinstance(other, CyclotomicInteger):
            require(other.order == self.order,
                    "cyclotomic elements of different orders were combined")
            return other
        return CyclotomicInteger(self.order, [other])

    def __add__(self, other):
        other = self._coerce(other)
        return CyclotomicInteger(self.order,
                                 [a + b for a, b in zip(self.coefficients,
                                                        other.coefficients)])

    __radd__ = __add__

    def __neg__(self):
        return CyclotomicInteger(self.order,
                                 [-a for a in self.coefficients])

    def __sub__(self, other):
        return self + (-self._coerce(other))

    def __mul__(self, other):
        other = self._coerce(other)
        degree = len(self.coefficients)
        product = [0] * (2 * degree)
        for index, left in enumerate(self.coefficients):
            if not left:
                continue
            for offset, right in enumerate(other.coefficients):
                if right:
                    product[index + offset] += left * right
        return CyclotomicInteger(self.order, product)

    __rmul__ = __mul__

    def __bool__(self):
        return any(self.coefficients)

    def __eq__(self, other):
        if not isinstance(other, CyclotomicInteger):
            other = self._coerce(other)
        return (self.order == other.order
                and self.coefficients == other.coefficients)

    def __hash__(self):
        return hash((self.order, self.coefficients))

    def __repr__(self):
        return "Cyc_%d(%s)" % (self.order,
                               ",".join(str(v) for v in self.coefficients))


def cycle_pencil_packet(k):
    """The alternating 2k-cycle over Z[zeta_2k] with the pencil weights.

    Odd edges carry x_0; the i-th even edge carries x_1 - zeta_i x_2 with
    zeta_i = s^{2i+1}, the k distinct roots of t^k = -1.  A 2k-cycle has
    exactly two perfect matchings, so
    haf(L) = x_0^k + prod_i (x_1 - zeta_i x_2) = x_0^k + x_1^k + x_2^k.
    This is the pencil counterexample family of the session scratch.  Its
    exact FIELD version and its full polynomial hafnian are audited in the
    committed `computations/verify_diagonal_termwise_census_and_pencil_
    guard.py`; everything needed here -- the roots of t^k = -1, the product
    identity, the two perfect matchings of the support, the nonzero anchors
    and the star ranks -- is recomputed below over the integer ring, so the
    two artifacts corroborate rather than depend on each other.
    """
    order = 2 * k
    n = 2 * k
    one = CyclotomicInteger(order, [1])
    packet = [{}, {}, {}]
    roots = []
    for index in range(k):
        packet[0][frozenset((2 * index, 2 * index + 1))] = one
        edge = frozenset((2 * index + 1, (2 * index + 2) % n))
        coefficients = [0] * (2 * index + 2)
        coefficients[2 * index + 1] = 1
        root = CyclotomicInteger(order, coefficients)
        roots.append(root)
        packet[1][edge] = one
        packet[2][edge] = -root
    return order, n, packet, roots, one


def section_rank2_vacuity(max_k):
    """The pencil counterexamples are ALL rank 2, hence never termwise-dead."""
    records = []
    for k in range(2, max_k + 1):
        order, n, packet, roots, one = cycle_pencil_packet(k)
        zero = CyclotomicInteger(order, [])
        require(len({root.coefficients for root in roots}) == k,
                "cycle pencil k=%d: the k designated weights are not distinct"
                % k)
        for root in roots:
            power = one
            for _ in range(k):
                power = power * root
            require(power == -one,
                    "cycle pencil k=%d: a designated weight is not a root of "
                    "t^k = -1" % k)

        # The mechanism, computed from the packet's OWN weights: the k even
        # edges carry x_1 W_1 + x_2 W_2 = x_1 - zeta_i x_2, and the product of
        # those k linear forms must be x_1^k + x_2^k.
        product = {(0, 0, 0): one}
        for index in range(k):
            edge = frozenset((2 * index + 1, (2 * index + 2) % n))
            product = poly_mul(product, {(0, 1, 0): packet[1][edge],
                                         (0, 0, 1): packet[2][edge]})
        require(product == {(0, k, 0): one, (0, 0, k): one},
                "cycle pencil k=%d: prod_i (x_1 - zeta_i x_2) is not "
                "x_1^k + x_2^k, so the counterexample's mechanism is broken"
                % k)

        support = {}
        for entries in packet:
            for edge in entries:
                support[edge] = 1
        require(hafnian_table(n, dict_weight(support))[(1 << n) - 1] == 2,
                "cycle pencil k=%d: the support 2k-cycle does not have exactly "
                "two perfect matchings" % k)

        tables = [ring_hafnian_table(n, entries, zero, one) for entries in packet]
        full = (1 << n) - 1
        require(all(tables[colour][full] for colour in range(3)),
                "cycle pencil k=%d: a pure anchor vanishes, so (A4) does not "
                "apply and the packet proves nothing about vacuity" % k)

        ranks = sorted({minor_rank([[packet[colour].get(frozenset((u, v)), zero)
                                     for colour in range(3)]
                                    for v in range(n) if v != u
                                    and any(packet[colour].get(frozenset((u, v)))
                                            for colour in range(3))])
                        for u in range(n)})
        require(ranks == [2],
                "cycle pencil k=%d: the star ranks are %s, not all 2, so the "
                "mutual-exclusivity claim against (A4) does not hold here"
                % (k, ranks))

        # An independent second reason: TW2 already fails, with an explicit
        # live split of shape (0,2,n-2).
        violations = []
        for u in range(n):
            for v in range(u + 1, n):
                key = frozenset((u, v))
                for colour in range(3):
                    if not packet[colour].get(key):
                        continue
                    for other in range(3):
                        if other == colour:
                            continue
                        if tables[other][full ^ (1 << u) ^ (1 << v)]:
                            violations.append(((u, v), colour, other))
        require(violations,
                "cycle pencil k=%d: no TW2 violation, so the second and "
                "independent reason for non-deadness is missing" % k)
        (u, v), colour, other = violations[0]
        pair = (1 << u) | (1 << v)
        require(tables[colour][pair] and tables[other][full ^ pair],
                "cycle pencil k=%d: the split named by the TW2 violation is "
                "not live" % k)

        records.append({
            "k": k, "n": n, "field": "Z[zeta_%d]" % order,
            "degree": len(cyclotomic_polynomial(order)) - 1,
            "modulus": list(cyclotomic_polynomial(order)),
            "star_ranks": ranks,
            "tw2_violations": len(violations),
            "witness_split": [[u, v], colour, other],
            "product_monomials": sorted(list(key) for key in product),
        })
    return {"orders": [record["k"] for record in records], "detail": records}


# ============================================================== section B


def cycle_edges(n):
    return [(i, (i + 1) % n) for i in range(n)]


def crosses(first, second, n):
    """Do two chords of C_n cross?  (Exactly one endpoint strictly inside.)"""
    low, high = sorted(first)
    inside = sum(1 for vertex in second if low < vertex < high)
    return inside == 1


def pm_count_via_subsets(n, chords):
    """#PM of C_n + chords, via the subset-A characterisation.

    A subset A of the chords is LIVE iff every arc of C_n minus V(A) has an
    even number of vertices; then the arcs are matched by cycle edges in
    exactly one way.  A = {} contributes the two alternating matchings of
    C_n, every other live A contributes one matching.
    """
    total = 0
    for size in range(len(chords) + 1):
        for chosen in itertools.combinations(range(len(chords)), size):
            removed = sorted(vertex for index in chosen
                             for vertex in chords[index])
            if not removed:
                total += 2
                continue
            ok = True
            for position in range(len(removed)):
                gap = (removed[(position + 1) % len(removed)]
                       - removed[position] - 1) % n
                if gap % 2:
                    ok = False
                    break
            if ok:
                total += 1
    return total


def chord_matchings(n, same_parity_only=False):
    """Perfect matchings of V(C_n) using no edge of C_n."""
    cycle = {frozenset(edge) for edge in cycle_edges(n)}
    if same_parity_only:
        evens = list(range(0, n, 2))
        odds = list(range(1, n, 2))
        if len(evens) % 2:
            return
        for first in perfect_matchings(evens):
            for second in perfect_matchings(odds):
                yield first + second
        return
    for matching in perfect_matchings(list(range(n))):
        if any(frozenset(edge) in cycle for edge in matching):
            continue
        yield matching


def section_b_characterisation(max_k):
    """The subset-A count must agree with the direct hafnian PM count."""
    records = []
    for k in range(2, max_k + 1):
        n = 2 * k
        tested = 0
        counts = set()
        for chords in chord_matchings(n):
            direct = pm_count_graph(n, cycle_edges(n) + list(chords))
            via_subsets = pm_count_via_subsets(n, list(chords))
            require(direct == via_subsets,
                    "the subset-A characterisation disagrees with the direct "
                    "hafnian perfect-matching count at k=%d on the chord "
                    "matching %s: %d against %d"
                    % (k, chords, direct, via_subsets))
            counts.add(direct)
            tested += 1
        require(tested > 0,
                "no chord matching at k=%d, so the characterisation is "
                "vacuous there" % k)
        require(len(counts) > 1 or k == 2,
                "every chord matching at k=%d has the same PM count, so the "
                "comparison is not discriminating" % k)
        records.append({"k": k, "chord_matchings": tested,
                        "distinct_pm_counts": sorted(counts)})
    return records


def section_b1_b2(max_k):
    """(B1) singleton parity and (B2) balanced crossing, both directions."""
    records = []
    for k in range(3, max_k + 1):
        n = 2 * k
        singleton_live = singleton_dead = 0
        killed_by_parity = 0
        crossing_live = noncrossing_dead = 0
        proper_crossing = 0
        for chords in chord_matchings(n):
            chords = list(chords)
            for chord in chords:
                opposite = (chord[0] - chord[1]) % 2 == 1
                live = pm_count_via_subsets(n, [chord]) - 2 == 1
                require(opposite == live,
                        "B1 fails at k=%d on the chord %s: joining opposite "
                        "parities is %s but being a live singleton is %s"
                        % (k, chord, opposite, live))
                if live:
                    singleton_live += 1
                else:
                    singleton_dead += 1
            if any((chord[0] - chord[1]) % 2 for chord in chords):
                require(pm_count_via_subsets(n, chords) > 3,
                        "B1 fails at k=%d: a chord matching with an "
                        "opposite-parity chord still has only three perfect "
                        "matchings" % k)
                killed_by_parity += 1
                continue
            evens = [chord for chord in chords if chord[0] % 2 == 0]
            odds = [chord for chord in chords if chord[0] % 2 == 1]
            for first in evens:
                for second in odds:
                    crossing = crosses(first, second, n)
                    live = pm_count_via_subsets(n, [first, second]) - 2 == 1
                    require(crossing == live,
                            "B2 fails at k=%d on the mixed pair %s,%s: "
                            "crossing is %s but liveness is %s"
                            % (k, first, second, crossing, live))
                    if live:
                        crossing_live += 1
                        if len(chords) > 2:
                            proper_crossing += 1
                    else:
                        noncrossing_dead += 1
        require(singleton_live > 0 and singleton_dead > 0,
                "the B1 test at k=%d never saw both a live and a dead "
                "singleton, so it is not discriminating" % k)
        records.append({
            "k": k,
            "live_singletons": singleton_live,
            "dead_singletons": singleton_dead,
            "matchings_killed_by_an_opposite_parity_chord": killed_by_parity,
            "live_crossing_mixed_pairs": crossing_live,
            "dead_noncrossing_mixed_pairs": noncrossing_dead,
            "proper_live_crossing_pairs": proper_crossing,
        })
    require(any(record["live_crossing_mixed_pairs"] > 0 for record in records),
            "the B2 test never saw a live crossing mixed pair at any audited "
            "k, so (B2) is vacuous here")
    require(any(record["dead_noncrossing_mixed_pairs"] > 0
                for record in records),
            "the B2 test never saw a dead non-crossing mixed pair, so its "
            "'only if' direction is vacuous here")
    return records


def section_b_exhaustive(max_k, prune_to):
    """Exhaustive #PM over Hamiltonian-cycle cubic graphs, then the prune."""
    exhaustive = []
    for k in range(2, max_k + 1):
        n = 2 * k
        tested = exactly_three = 0
        minimum = None
        for chords in chord_matchings(n):
            count = pm_count_via_subsets(n, list(chords))
            tested += 1
            minimum = count if minimum is None else min(minimum, count)
            if count == 3:
                exactly_three += 1
        require((exactly_three > 0) == (k == 2),
                "Theorem B fails at k=%d: %d Hamiltonian-cycle cubic graphs "
                "have exactly three perfect matchings" % (k, exactly_three))
        exhaustive.append({"k": k, "n": n, "graphs": tested,
                           "minimum_pm_count": minimum,
                           "graphs_with_exactly_three": exactly_three})
    pruned = []
    for k in range(max_k + 1, prune_to + 1):
        n = 2 * k
        after_b1 = after_b2 = 0
        for chords in chord_matchings(n, same_parity_only=True):
            after_b1 += 1
            evens = [chord for chord in chords if chord[0] % 2 == 0]
            odds = [chord for chord in chords if chord[0] % 2 == 1]
            if all(not crosses(first, second, n)
                   for first in evens for second in odds):
                after_b2 += 1
        require((after_b1 == 0) == (k % 2 == 1),
                "the (B1) prune at k=%d left %d survivors, which does not "
                "match the parity obstruction" % (k, after_b1))
        require(after_b2 == 0,
                "the (B1)+(B2) prune at k=%d left %d survivors, so exactly "
                "three perfect matchings is not excluded there" % (k, after_b2))
        pruned.append({"k": k, "n": n, "after_b1": after_b1,
                       "after_b2": after_b2})
    return exhaustive, pruned


def signature_classes(k, even_arcs):
    """The gap-signature classes of a system of arcs on the even vertices.

    An arc (p,q), p < q, is the chord (2p, 2q) of C_2k.  The odd vertex
    2i+1 lies strictly inside that chord's short side iff p <= i < q, so
    the SIGNATURE of odd index i is the set of arcs straddling gap i.  Two
    odd vertices are non-crossing with every arc exactly when they have the
    same signature.  Hence a compatible non-crossing odd matching exists
    iff every signature class has even size.
    """
    signature = [0] * k
    for index, (p, q) in enumerate(even_arcs):
        if p > q:
            p, q = q, p
        for gap in range(p, q):
            signature[gap] |= 1 << index
    classes = {}
    for value in signature:
        classes[value] = classes.get(value, 0) + 1
    return classes


def noncrossing_partner_exists(k, even_arcs):
    return all(size % 2 == 0 for size in signature_classes(k, even_arcs).values())


def noncrossing_partner_bruteforce(k, even_arcs):
    """Direct search over odd matchings; the control for the signature test."""
    n = 2 * k
    chords = [(2 * min(p, q), 2 * max(p, q)) for p, q in even_arcs]
    odds = list(range(1, n, 2))
    for candidate in perfect_matchings(odds):
        if all(not crosses(chord, pair, n)
               for chord in chords for pair in candidate):
            return True
    return False


def section_b3(scan_to, control_to):
    """(B3): no same-parity chord matching is mixed-non-crossing.

    The signature reformulation is validated against the direct search over
    odd matchings on every even-arc SYSTEM (not only the matchings) up to
    `control_to`, where both answers occur, and then the matchings are
    scanned to `scan_to`.
    """
    control_agreements = yes = no = 0
    for k in range(2, control_to + 1, 2):
        arcs = [(p, q) for p in range(k) for q in range(p + 1, k)]
        for size in range(0, 4):
            for chosen in itertools.combinations(arcs, size):
                if len({vertex for arc in chosen for vertex in arc}) \
                        != 2 * len(chosen):
                    continue
                fast = noncrossing_partner_exists(k, list(chosen))
                slow = noncrossing_partner_bruteforce(k, list(chosen))
                require(fast == slow,
                        "the signature criterion disagrees with the direct "
                        "non-crossing search at k=%d on the arc system %s: "
                        "%s against %s" % (k, chosen, fast, slow))
                control_agreements += 1
                if fast:
                    yes += 1
                else:
                    no += 1
    require(yes > 0 and no > 0,
            "the (B3) signature control is not discriminating: it saw %d yes "
            "and %d no answers" % (yes, no))
    require(control_agreements > 0,
            "the (B3) signature control ran on no arc system at all")

    scans = []
    for k in range(2, scan_to + 1, 2):
        scanned = survivors = 0
        for arcs in perfect_matchings(list(range(k))):
            scanned += 1
            if noncrossing_partner_exists(k, list(arcs)):
                survivors += 1
        require(survivors == 0,
                "(B3) fails at k=%d: %d same-parity chord matchings are "
                "mixed-non-crossing, so exactly three perfect matchings is "
                "not excluded there" % (k, survivors))
        scans.append({"k": k, "even_matchings_scanned": scanned,
                      "mixed_non_crossing_survivors": survivors})
    require(scans[-1]["k"] == scan_to,
            "the (B3) scan did not reach the advertised k=%d" % scan_to)
    return {"control_agreements": control_agreements,
            "control_yes": yes, "control_no": no, "scans": scans}


def disjoint_pm_triples(n):
    """Every ordered triple of pairwise disjoint perfect matchings, M_0 fixed.

    Fixing M_0 = {01|23|...} costs no generality: relabelling carries any
    triple to one of these.
    """
    matchings = list(perfect_matchings(list(range(n))))
    first = tuple((2 * i, 2 * i + 1) for i in range(n // 2))
    used_first = {frozenset(edge) for edge in first}
    for second in matchings:
        if any(frozenset(edge) in used_first for edge in second):
            continue
        used_second = used_first | {frozenset(edge) for edge in second}
        for third in matchings:
            if any(frozenset(edge) in used_second for edge in third):
                continue
            yield first, second, third


def section_b_disjoint_triples(orders):
    """Exhaustive over ALL disjoint PM triples: no Hamiltonicity assumed."""
    records = []
    for n in orders:
        tested = exactly_three = 0
        hamiltonian_when_three = True
        for triple in disjoint_pm_triples(n):
            tested += 1
            edges = [edge for matching in triple for edge in matching]
            count = pm_count_graph(n, edges)
            if count == 3:
                exactly_three += 1
                hamiltonian_when_three &= all(
                    union_is_hamiltonian(n, first, second)
                    for first, second in itertools.combinations(triple, 2))
        require(tested > 0,
                "no disjoint perfect-matching triple at n=%d, so the "
                "exhaustion is vacuous there" % n)
        require((exactly_three > 0) == (n == 4),
                "Theorem B fails at n=%d: %d disjoint triples give exactly "
                "three perfect matchings" % (n, exactly_three))
        require(hamiltonian_when_three,
                "(B0) fails at n=%d: an exactly-three triple has a pairwise "
                "union that is not a single Hamiltonian cycle" % n)
        records.append({"n": n, "triples": tested,
                        "triples_with_exactly_three": exactly_three,
                        "all_of_those_pairwise_hamiltonian":
                            hamiltonian_when_three})
    return records


def section_packet_dictionary(orders):
    """termwise-dead <=> #PM(union) = 3, on 0/1 disjoint-matching packets."""
    records = []
    for n in orders:
        tested = dead = 0
        for triple in disjoint_pm_triples(n):
            packet = [matching_entries(matching) for matching in triple]
            tables = packet_tables(n, packet)
            live = live_splits(n, tables)
            count = pm_count_graph(n, [edge for matching in triple
                                       for edge in matching])
            require(len(live) == count - 3,
                    "the packet dictionary fails at n=%d: %d live splits "
                    "against %d perfect matchings of the union"
                    % (n, len(live), count))
            is_dead = termwise_dead(n, tables)
            require(is_dead == (count == 3),
                    "the packet dictionary fails at n=%d: termwise-dead is %s "
                    "while the union has %d perfect matchings"
                    % (n, is_dead, count))
            tested += 1
            dead += 1 if is_dead else 0
        require((dead > 0) == (n == 4),
                "the packet dictionary at n=%d found %d termwise-dead packets"
                % (n, dead))
        records.append({"n": n, "packets": tested, "termwise_dead": dead})
    return records


# ============================================================== section C


def matching_faithful_failures(n, entries):
    """Even sets S that G[S] perfectly matches while haf W[S] = 0.

    Empty when W is matching-faithful.  Also returns how many even S are
    matched at all, so a caller can refuse a vacuous verdict.
    """
    table = hafnian_table(n, dict_weight(entries))
    support = {edge for edge, cell in entries.items() if cell}
    failures = []
    matched = 0
    for mask in range(1 << n):
        if mask.bit_count() % 2:
            continue
        vertices = [v for v in range(n) if mask >> v & 1]
        has_matching = any(
            all(frozenset(edge) in support for edge in candidate)
            for candidate in perfect_matchings(vertices))
        if not has_matching:
            continue
        matched += 1
        if table[mask] == 0:
            failures.append(mask)
    return failures, matched


def section_faithfulness_probes():
    """Matching-faithfulness pinned in BOTH directions."""
    # Positive: a nonnegative packet is faithful, and nonvacuously so.
    nonnegative = {frozenset((0, 1)): 1, frozenset((2, 3)): 1,
                   frozenset((0, 2)): 1, frozenset((1, 3)): 1,
                   frozenset((0, 3)): 3, frozenset((1, 2)): 2}
    failures, matched = matching_faithful_failures(4, nonnegative)
    require(not failures,
            "the faithfulness probe found a nonnegative matrix that is not "
            "matching-faithful, which contradicts the absence of cancellation")
    require(matched >= 4,
            "the positive faithfulness probe is vacuous: only %d even sets "
            "are matched at all" % matched)

    # Negative: a signed matrix with a perfectly matched S and haf W[S] = 0.
    cancelling = {frozenset((0, 1)): 1, frozenset((2, 3)): 1,
                  frozenset((0, 2)): 1, frozenset((1, 3)): -1}
    failures, matched = matching_faithful_failures(4, cancelling)
    require(failures,
            "the NEGATIVE faithfulness probe is vacuous: the designed "
            "cancelling matrix is matching-faithful after all, so the "
            "definition is pinned in one direction only")
    require(15 in failures,
            "the negative faithfulness probe cancels somewhere other than the "
            "full vertex set, so it does not exhibit the intended failure")
    require(matched > len(failures),
            "the negative faithfulness probe fails on every matched set, so "
            "it is degenerate rather than discriminating")
    return {"positive_matched_sets": matched,
            "negative_failures": len(failures),
            "negative_failure_masks": sorted(failures)}


def support_matchings_inside(n, entries, mask):
    """Every perfect matching of G[S] = supp(W)[S], for S the given mask."""
    vertices = [vertex for vertex in range(n) if mask >> vertex & 1]
    return [candidate for candidate in perfect_matchings(vertices)
            if all(entries.get(frozenset(edge), 0) for edge in candidate)]


def step4_faithfulness_holds(n, entries, mask):
    """The Step-4 test, as a VERDICT rather than a bare assertion.

    Step 4 of Theorem C needs h_c(S_c) != 0 on a set that G_c perfectly
    matches; matching-faithfulness is exactly what supplies it.  Returning
    the verdict instead of asserting it lets `section_faithfulness_load_
    bearing` require the test to answer TRUE on a faithful packet and FALSE
    on a cancelling one of the SAME support -- so a neutered test is caught
    rather than silently passing.
    """
    return hafnian_table(n, dict_weight(entries))[mask] != 0


def a_perfect_matching(n, entries):
    """Some perfect matching of supp(W), or None."""
    for candidate in perfect_matchings(list(range(n))):
        if all(entries.get(frozenset(edge), 0) for edge in candidate):
            return candidate
    return None


def theorem_c_steps(n, packet, label):
    """Steps 1-4 of Theorem C on one anchored matching-faithful packet."""
    tables = packet_tables(n, packet)
    if not all(anchors_of(n, tables)):
        return None
    # Step 1: a nonzero anchor forces a perfect matching of the support.
    anchor_matchings = [a_perfect_matching(n, entries) for entries in packet]
    for colour in range(3):
        require(anchor_matchings[colour] is not None,
                "step 1 fails on %s: colour %d has a nonzero anchor but no "
                "perfect matching in its support" % (label, colour))
    # Step 2: faithfulness makes every anchor-matching edge essential.
    for colour in range(3):
        for u, v in anchor_matchings[colour]:
            require(cofactor(n, tables, colour, u, v) != 0,
                    "step 2 fails on %s: deleting the anchor-matching edge "
                    "(%d,%d) kills h_%d, which faithfulness forbids"
                    % (label, u, v, colour))
    # Step 2, first branch: a BICHROMATIC anchor-matching edge already ends
    # the proof, because the split ({u,v} in c', V\{u,v} in c) is then live.
    # This is weaker than global TW2-cleanness, and the proof needs no more.
    for colour in range(3):
        for u, v in anchor_matchings[colour]:
            for other in range(3):
                if other == colour or not packet[other].get(frozenset((u, v)), 0):
                    continue
                pair = (1 << u) | (1 << v)
                require(tables[other][pair] * tables[colour][
                            ((1 << n) - 1) ^ pair] != 0,
                        "step 2 fails on %s: the anchor-matching edge (%d,%d) "
                        "is bichromatic yet the split its proof names is not "
                        "live" % (label, u, v))
                return {"label": label, "n": n, "verdict": "bichromatic anchor",
                        "witness_pair": [u, v], "colours": [colour, other]}
    edge_sets = [frozenset(frozenset(edge) for edge in matching)
                 for matching in anchor_matchings]
    require(len(edge_sets[0] | edge_sets[1] | edge_sets[2]) == 3 * (n // 2),
            "step 2 fails on %s: the three anchor matchings are not pairwise "
            "disjoint" % label)
    # Step 3: the union is cubic and properly 3-edge-coloured.
    degrees = {vertex: 0 for vertex in range(n)}
    for edges in edge_sets:
        for edge in edges:
            for vertex in edge:
                degrees[vertex] += 1
    require(set(degrees.values()) == {3},
            "step 3 fails on %s: the union of the three anchor matchings is "
            "not cubic" % label)
    union = [tuple(sorted(edge)) for edges in edge_sets for edge in edges]
    count = pm_count_graph(n, union)
    require(count >= 3, "step 3 fails on %s: the anchor cubic graph has fewer "
                        "than three perfect matchings" % label)
    if n // 2 >= 3:
        require(count > 3,
                "step 3 fails on %s: the anchor cubic graph at k=%d has "
                "exactly three perfect matchings, contradicting Theorem B"
                % (label, n // 2))
    # Step 4: every extra matching induces a proper split, live by faithfulness.
    allowed = edge_sets[0] | edge_sets[1] | edge_sets[2]
    extra = 0
    faithfulness_load_bearing = 0
    for candidate in perfect_matchings(list(range(n))):
        chosen = frozenset(frozenset(edge) for edge in candidate)
        if not chosen <= allowed or chosen in edge_sets:
            continue
        extra += 1
        masks = [0, 0, 0]
        for edge in chosen:
            u, v = sorted(edge)
            for colour in range(3):
                if edge in edge_sets[colour]:
                    masks[colour] |= (1 << u) | (1 << v)
        require(sum(mask.bit_count() for mask in masks) == n,
                "step 4 fails on %s: the induced parts do not partition V"
                % label)
        for colour in range(3):
            require(masks[colour].bit_count() % 2 == 0,
                    "step 4 fails on %s: an induced part is odd" % label)
            require(masks[colour] != (1 << n) - 1,
                    "step 4 fails on %s: an extra perfect matching induces an "
                    "improper split" % label)
            require(step4_faithfulness_holds(n, packet[colour], masks[colour]),
                    "step 4 fails on %s: h_%d vanishes on the part that "
                    "P n M_%d perfectly matches, which faithfulness forbids"
                    % (label, colour, colour))
            # Faithfulness is LOAD-BEARING on this part only when G_c[S_c]
            # carries at least two perfect matchings.  With exactly one,
            # h_c(S_c) is a single product of nonzero cells and (S2) already
            # makes it nonzero -- no faithfulness hypothesis needed.
            if len(support_matchings_inside(n, packet[colour],
                                            masks[colour])) >= 2:
                faithfulness_load_bearing += 1
    require(extra == count - 3,
            "step 4 fails on %s: %d extra perfect matchings against a count "
            "of %d" % (label, extra, count))
    require(extra > 0 or n == 4,
            "step 4 fails on %s: no extra perfect matching at k >= 3"
            % label)
    return {"label": label, "n": n, "verdict": "clean",
            "anchor_cubic_pm_count": count, "extra_matchings": extra,
            "parts_with_two_or_more_matchings": faithfulness_load_bearing}


def nonnegative_packet(n, seed):
    """A deterministic packet with strictly positive entries (hence faithful)."""
    factors = one_factors(n)
    stream = _draws(seed, 200)
    order = _distinct_factor_indices(stream, len(factors))
    packet = []
    for colour in range(3):
        entries = {}
        for edge in factors[order[colour]]:
            entries[frozenset(edge)] = 1 + next(stream) % 4
        for _ in range(next(stream) % 4):
            u = next(stream) % n
            v = next(stream) % n
            weight = 1 + next(stream) % 4
            if u != v:
                entries.setdefault(frozenset((u, v)), weight)
        packet.append(entries)
    return packet


def section_theorem_c_instances(trials):
    """Steps 1-4 on deterministic NONNEGATIVE packets at n = 6,8."""
    verdicts = {}
    checked = clean = load_bearing = 0
    dead_checked = 0
    for trial in range(trials):
        n = 6 if trial % 2 == 0 else 8
        packet = nonnegative_packet(n, 5551212 + 104729 * trial)
        failures, matched = matching_faithful_failures(n, packet[0])
        require(not failures,
                "a nonnegative colour matrix at n=%d is not matching-faithful, "
                "contradicting the absence of cancellation" % n)
        require(matched > 0,
                "the faithfulness check on nonnegative packet %d is vacuous"
                % trial)
        record = theorem_c_steps(n, packet, "nonnegative packet %d" % trial)
        if record is None:
            continue
        checked += 1
        verdicts[record["verdict"]] = verdicts.get(record["verdict"], 0) + 1
        if record["verdict"] != "clean":
            continue
        clean += 1
        load_bearing += record["parts_with_two_or_more_matchings"]
        if n <= 8:
            tables = packet_tables(n, packet)
            require(not termwise_dead(n, tables),
                    "a matching-faithful anchored packet at k=%d is "
                    "termwise-dead, contradicting Theorem C" % (n // 2))
            dead_checked += 1
    require(clean > 0,
            "the Theorem C instance family is vacuous: not one packet reached "
            "the clean branch where steps 3 and 4 are exercised")
    require(dead_checked > 0,
            "the Theorem C conclusion was never confirmed by a full split "
            "census")
    # DISCLOSED: on this family faithfulness is never load-bearing.  Every
    # induced part here is perfectly matched by G_c in exactly ONE way, so
    # (S2) alone already makes h_c(S_c) nonzero and the faithfulness step is
    # inert.  The count is recorded, not required to be positive; the
    # genuinely load-bearing instances are built by hand in
    # `section_faithfulness_load_bearing`.
    return {"trials": trials, "checked": checked, "clean": clean,
            "verdicts": verdicts,
            "parts_with_two_or_more_matchings": load_bearing,
            "full_censuses_confirming_not_dead": dead_checked}


# The three hand-built configurations on which faithfulness really is what
# excludes cancellation.  Each names an anchor triple, a colour, an induced
# part that some extra perfect matching of the anchor cubic graph produces,
# and two EXTRA edges -- outside the anchor union, so no anchor edge becomes
# bichromatic and the proof does not exit early at step 2 -- which give
# G_c[S_c] a SECOND perfect matching.  `flip` names the extra edge whose
# sign is negated to build the cancelling twin.
LOAD_BEARING_INSTANCES = [
    {"label": "n=8 block triple, colour 0, part {0,1,2,3}",
     "n": 8,
     "triple": (((0, 1), (2, 3), (4, 5), (6, 7)),
                ((0, 2), (1, 3), (4, 6), (5, 7)),
                ((0, 4), (1, 5), (2, 6), (3, 7))),
     "colour": 0,
     "part": (0, 1, 2, 3),
     "extras": ((0, 3), (1, 2)),
     "flip": (0, 3)},
    {"label": "D(10), colour 1, part {0,1,2,4,7,9}",
     "n": 10,
     "triple": None,
     "colour": 1,
     "part": (0, 1, 2, 4, 7, 9),
     "extras": ((0, 7), (2, 4)),
     "flip": (0, 7)},
    {"label": "D(12), colour 0, part {3,4,7,8}",
     "n": 12,
     "triple": None,
     "colour": 0,
     "part": (3, 4, 7, 8),
     "extras": ((3, 7), (4, 8)),
     "flip": (3, 7)},
]


def section_second_matching_reach(orders):
    """How far (S2) reaches: which induced parts could carry a cancellation.

    A part S_c can cancel only if G_c[S_c] has a second perfect matching
    (S2), and the edges realising it must avoid the anchor union -- an edge
    inside the union belongs to another colour, so adding it to colour c
    would make an anchor edge bichromatic and the proof would already have
    stopped at step 2.  This measures, over EVERY anchor cubic graph, how
    many induced parts of size >= 4 admit such a second matching.  It is
    what explains why the deterministic instance family of
    `section_theorem_c_instances` never exercises faithfulness.
    """
    records = []
    for n in orders:
        parts = reachable = 0
        for triple in disjoint_pm_triples(n):
            edge_sets = [frozenset(frozenset(edge) for edge in matching)
                         for matching in triple]
            union = edge_sets[0] | edge_sets[1] | edge_sets[2]
            masks_list, _total = extra_matching_profiles(n, triple)
            for masks in masks_list:
                for colour in range(3):
                    if masks[colour].bit_count() < 4:
                        continue
                    parts += 1
                    inside = [v for v in range(n) if masks[colour] >> v & 1]
                    anchor = frozenset(frozenset(edge)
                                       for edge in edge_sets[colour]
                                       if set(edge) <= set(inside))
                    for candidate in perfect_matchings(inside):
                        chosen = frozenset(frozenset(edge)
                                           for edge in candidate)
                        if chosen == anchor:
                            continue
                        if all(edge not in union for edge in chosen):
                            reachable += 1
                            break
        records.append({"n": n, "induced_parts_of_size_at_least_4": parts,
                        "parts_admitting_a_second_matching": reachable})
    by_order = {record["n"]: record for record in records}
    require(by_order[6]["induced_parts_of_size_at_least_4"] == 0,
            "n=6 has an induced part of size >= 4, so the claim that (S1) "
            "alone settles every n=6 part is false")
    require(by_order[8]["parts_admitting_a_second_matching"] > 0,
            "no n=8 induced part admits a second perfect matching outside "
            "the union, so a load-bearing instance would be structurally "
            "impossible at n=8 and the note's explanation is wrong")
    return records


def section_faithfulness_load_bearing():
    """Instances on which the Step-4 faithfulness test is FALSIFIABLE.

    On each one the same support carries two packets: a positive one, which
    is matching-faithful, and its CANCELLING TWIN with a single weight
    negated, which is not.  The Step-4 test must answer TRUE on the first
    and FALSE on the second.  Requiring both directions is what makes the
    test falsifiable: a neutered faithfulness step passes the positive half
    silently, and is caught by the negative half.
    """
    records = []
    for spec in LOAD_BEARING_INSTANCES:
        n, colour = spec["n"], spec["colour"]
        triple = (spec["triple"] if spec["triple"] is not None
                  else one_factors(n)[:3])
        edge_sets = [frozenset(frozenset(edge) for edge in matching)
                     for matching in triple]
        for first, second in itertools.combinations(range(3), 2):
            require(not (edge_sets[first] & edge_sets[second]),
                    "%s: the anchor matchings are not pairwise disjoint"
                    % spec["label"])
        union = edge_sets[0] | edge_sets[1] | edge_sets[2]
        mask = sum(1 << vertex for vertex in spec["part"])

        packet = [dict(matching_entries(matching)) for matching in triple]
        for edge in spec["extras"]:
            key = frozenset(edge)
            require(key not in union,
                    "%s: the extra edge %s lies in the anchor union, so it "
                    "would make an anchor edge bichromatic and the proof "
                    "would exit at step 2 instead of reaching step 4"
                    % (spec["label"], edge))
            packet[colour][key] = 1

        # The part must be one an extra perfect matching really induces.
        masks_list, _total = extra_matching_profiles(n, triple)
        witnesses = [masks for masks in masks_list if masks[colour] == mask]
        require(witnesses,
                "%s: the named part is not induced by any extra perfect "
                "matching of the anchor cubic graph, so step 4 never asks "
                "about it" % spec["label"])
        witness = witnesses[0]

        # (S2) is satisfied: cancellation on this part is CONCEIVABLE.
        inside = support_matchings_inside(n, packet[colour], mask)
        require(len(inside) >= 2,
                "%s: G_c[S_c] has %d perfect matching(s), so (S2) already "
                "forces h_c(S_c) != 0 and faithfulness is not load-bearing "
                "here" % (spec["label"], len(inside)))
        anchor_inside = [edge for edge in triple[colour]
                         if set(edge) <= set(spec["part"])]
        require(len(anchor_inside) * 2 == len(spec["part"]),
                "%s: the anchor matching does not perfectly match the named "
                "part" % spec["label"])

        # Positive half: the faithful packet passes the Step-4 test.
        require(step4_faithfulness_holds(n, packet[colour], mask),
                "%s: the Step-4 faithfulness test fails on the POSITIVE "
                "packet, although its entries are positive" % spec["label"])
        tables = packet_tables(n, packet)
        require(tables[colour][mask] != 0,
                "%s: h_c(S_c) vanishes on the positive packet"
                % spec["label"])
        require(all(tables[index][witness[index]] for index in range(3)),
                "%s: the split the witness induces is not live on the "
                "positive packet" % spec["label"])
        failures, matched = matching_faithful_failures(n, packet[colour])
        require(not failures and matched > 0,
                "%s: the positive packet is not matching-faithful"
                % spec["label"])

        # Negative half: the cancelling twin, SAME support, one sign flipped.
        twin = [dict(entries) for entries in packet]
        flip = frozenset(spec["flip"])
        require(twin[colour].get(flip, 0) != 0,
                "%s: the flipped edge carries no weight" % spec["label"])
        twin[colour][flip] = -twin[colour][flip]
        require(set(twin[colour]) == set(packet[colour]),
                "%s: the cancelling twin does not have the same support as "
                "the positive packet, so it is not a controlled comparison"
                % spec["label"])
        require(len(support_matchings_inside(n, twin[colour], mask))
                == len(inside),
                "%s: the cancelling twin has a different number of perfect "
                "matchings inside the part" % spec["label"])
        require(not step4_faithfulness_holds(n, twin[colour], mask),
                "%s: the Step-4 faithfulness test still answers TRUE on the "
                "CANCELLING TWIN, so the test is inert and faithfulness is "
                "not what excludes cancellation here" % spec["label"])
        twin_failures, twin_matched = matching_faithful_failures(
            n, twin[colour])
        require(mask in twin_failures,
                "%s: the cancelling twin is matching-faithful on the named "
                "part, so it is not the counterexample it is advertised to be"
                % spec["label"])
        require(twin_matched > len(twin_failures),
                "%s: the cancelling twin cancels on every matched set, so it "
                "is degenerate rather than discriminating" % spec["label"])

        records.append({
            "label": spec["label"], "n": n, "colour": colour,
            "part": sorted(spec["part"]),
            "extras": sorted(sorted(edge) for edge in spec["extras"]),
            "matchings_inside_the_part": len(inside),
            "positive_h": str(tables[colour][mask]),
            "twin_h": str(hafnian_table(n, dict_weight(twin[colour]))[mask]),
            "twin_faithfulness_failures": len(twin_failures),
            "twin_matched_sets": twin_matched,
            "witness_masks": list(witness),
        })
    require(len(records) == len(LOAD_BEARING_INSTANCES),
            "not every load-bearing instance was audited")
    require(len({record["n"] for record in records}) >= 3,
            "the load-bearing instances all sit at one order, so the "
            "phenomenon is not shown to be generic")
    return records


def section_theorem_c_exhaustive_n6():
    """EXHAUSTIVE 0/1 census at n = 6 over anchor triples plus extra edges.

    For every ordered triple of pairwise disjoint perfect matchings (M_0
    fixed) and every assignment of the six remaining edges to one colour or
    to none, Theorem C's step-4 split must be live.  A subsample is
    additionally checked by a full census over all 3^6 colourings, so the
    shortcut is never trusted on its own.

    DISCLOSED RESTRICTION: an extra edge here carries at most one colour.
    A second census below allows extra edges to carry ANY subset of the
    three colours, on a smaller edge pool, so the multi-coloured case is
    covered too.
    """
    n = 6
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    return _c_census(n, pairs, palette=4, pool=6,
                     label="one colour per extra edge"), \
        _c_census(n, pairs, palette=8, pool=3,
                  label="any colour subset per extra edge")


def _c_census(n, pairs, palette, pool, label):
    packets = live = full_censuses = 0
    for triple in disjoint_pm_triples(n):
        edge_sets = [frozenset(frozenset(edge) for edge in matching)
                     for matching in triple]
        anchor_edges = edge_sets[0] | edge_sets[1] | edge_sets[2]
        rest = [pair for pair in pairs
                if frozenset(pair) not in anchor_edges][:pool]
        extras = []
        for candidate in perfect_matchings(list(range(n))):
            chosen = frozenset(frozenset(edge) for edge in candidate)
            if not chosen <= anchor_edges or chosen in edge_sets:
                continue
            masks = [0, 0, 0]
            for edge in chosen:
                u, v = sorted(edge)
                for colour in range(3):
                    if edge in edge_sets[colour]:
                        masks[colour] |= (1 << u) | (1 << v)
            extras.append(tuple(masks))
        require(extras,
                "the n=6 Theorem C census met an anchor cubic graph with no "
                "extra perfect matching, contradicting Theorem B")
        cache = {}

        def table_for(colour, bits):
            key = (colour, bits)
            if key not in cache:
                entries = {edge: 1 for edge in edge_sets[colour]}
                for index, pair in enumerate(rest):
                    if bits >> index & 1:
                        entries[frozenset(pair)] = 1
                cache[key] = hafnian_table(n, dict_weight(entries))
            return cache[key]

        for code in itertools.product(range(palette), repeat=len(rest)):
            bits = [0, 0, 0]
            for index, assignment in enumerate(code):
                if palette == 4:
                    if assignment:
                        bits[assignment - 1] |= 1 << index
                else:
                    for colour in range(3):
                        if assignment >> colour & 1:
                            bits[colour] |= 1 << index
            tables = [table_for(colour, bits[colour]) for colour in range(3)]
            packets += 1
            found = None
            for masks in extras:
                if (tables[0][masks[0]] and tables[1][masks[1]]
                        and tables[2][masks[2]]):
                    found = masks
                    break
            require(found is not None,
                    "the n=6 Theorem C census (%s) found a 0/1 packet with no "
                    "live step-4 split, which would contradict Theorem C"
                    % label)
            if found is not None:
                live += 1
            if packets % 4096 == 1:
                require(not termwise_dead(n, tables),
                        "the n=6 Theorem C census (%s) found a termwise-dead "
                        "0/1 packet" % label)
                full_censuses += 1
    require(packets > 0 and full_censuses > 0,
            "the n=6 Theorem C census (%s) is vacuous" % label)
    require(live == packets,
            "the n=6 Theorem C census (%s) found a live step-4 split on only "
            "%d of its %d packets" % (label, live, packets))
    return {"label": label, "packets": packets, "with_a_live_step4_split": live,
            "full_censuses_cross_checked": full_censuses}


# ============================================================== section S


def section_stall(profile_orders, family_orders):
    """The exact stall, its two narrowings, and the profile measurement."""
    # (S1) A part of size 0 or 2 can never cancel: h_c(empty) = 1, and
    # h_c({u,v}) = W_c(u,v), which is nonzero because uv lies in M_c.
    # Verified as a computation on the packet dictionary family.
    small_part_checks = 0
    for triple in disjoint_pm_triples(6):
        packet = [matching_entries(matching) for matching in triple]
        tables = packet_tables(6, packet)
        require(tables[0][0] == 1,
                "(S1) fails: the empty hafnian is not 1")
        for colour, matching in enumerate(triple):
            for u, v in matching:
                require(tables[colour][(1 << u) | (1 << v)] != 0,
                        "(S1) fails: a two-element part carried by an anchor "
                        "edge has a vanishing hafnian")
                small_part_checks += 1
    require(small_part_checks > 0, "(S1) was never exercised")

    # (S2) With G_c = M_c exactly, G_c[S_c] has a unique perfect matching, so
    # h_c(S_c) is a single nonzero product.  Verified as: the anchor-only
    # packet has EVERY extra-matching split live, at every audited order.
    s2_checks = 0
    for n in family_orders:
        factors = one_factors(n)[:3]
        packet = [matching_entries(factor) for factor in factors]
        tables = packet_tables(n, packet)
        for masks in extra_matching_profiles(n, factors)[0]:
            for colour in range(3):
                require(tables[colour][masks[colour]] != 0,
                        "(S2) fails at n=%d: an anchor-only colour cancels on "
                        "a part it perfectly matches" % n)
            s2_checks += 1
    require(s2_checks > 0, "(S2) was never exercised")

    # The measurement: profiles of the extra matchings, over ALL anchor cubic
    # graphs at the audited orders.
    profiles = []
    for n in profile_orders:
        histogram = {}
        graphs = unkillable_graphs = graphs_with_any_small = 0
        extras_total = extras_small = 0
        for triple in disjoint_pm_triples(n):
            graphs += 1
            masks_list, _count = extra_matching_profiles(n, triple)
            shapes = [tuple(sorted(mask.bit_count() for mask in masks))
                      for masks in masks_list]
            for shape in shapes:
                histogram[shape] = histogram.get(shape, 0) + 1
                extras_total += 1
                if unkillable_profile(shape):
                    extras_small += 1
            require(shapes,
                    "an anchor cubic graph at n=%d has no extra perfect "
                    "matching, contradicting Theorem B" % n)
            if all(unkillable_profile(shape) for shape in shapes):
                unkillable_graphs += 1
            if any(unkillable_profile(shape) for shape in shapes):
                graphs_with_any_small += 1
        profiles.append({
            "n": n, "k": n // 2, "anchor_cubic_graphs": graphs,
            "extra_matchings": extras_total,
            "extra_matchings_with_every_part_at_most_2": extras_small,
            "graphs_all_of_whose_extras_are_unkillable": unkillable_graphs,
            "graphs_with_some_unkillable_extra": graphs_with_any_small,
            "profile_histogram": {str(list(shape)): count
                                  for shape, count in sorted(histogram.items())},
        })
    by_k = {record["k"]: record for record in profiles}
    require(3 in by_k and 4 in by_k,
            "the stall measurement must cover both k=3 and k=4 to say "
            "anything about why k=4,5 are not reproved")
    require(by_k[3]["graphs_all_of_whose_extras_are_unkillable"]
            == by_k[3]["anchor_cubic_graphs"],
            "the k=3 unkillability measurement fails: only %d of %d anchor "
            "cubic graphs have every extra matching of profile (2,2,2)"
            % (by_k[3]["graphs_all_of_whose_extras_are_unkillable"],
               by_k[3]["anchor_cubic_graphs"]))
    require(by_k[3]["extra_matchings_with_every_part_at_most_2"]
            == by_k[3]["extra_matchings"],
            "the k=3 unkillability measurement fails: some extra matching has "
            "a part of size >= 4")
    require(by_k[4]["graphs_with_some_unkillable_extra"] == 0,
            "the k=4 measurement fails: %d anchor cubic graphs have an extra "
            "matching with every part <= 2, so the cancellation-free argument "
            "would extend to k=4 after all"
            % by_k[4]["graphs_with_some_unkillable_extra"])
    require(by_k[4]["extra_matchings"] > 0,
            "the k=4 measurement is vacuous")

    # D(n) profiles, for the record.
    family = []
    for n in family_orders:
        factors = one_factors(n)[:3]
        masks_list, count = extra_matching_profiles(n, factors)
        histogram = {}
        for masks in masks_list:
            shape = tuple(sorted(mask.bit_count() for mask in masks))
            histogram[shape] = histogram.get(shape, 0) + 1
        require(not any(unkillable_profile(shape) for shape in histogram)
                or n == 6,
                "D(%d): an extra matching is unkillable although n > 6, so "
                "(S1) alone would settle the order" % n)
        family.append({"n": n, "perfect_matchings_of_the_union": count,
                       "extra_matchings": len(masks_list),
                       "profile_histogram": {str(list(shape)): value
                                             for shape, value
                                             in sorted(histogram.items())}})
    return {"s1_two_element_parts_checked": small_part_checks,
            "s2_anchor_only_splits_checked": s2_checks,
            "profiles": profiles, "hamiltonian_family": family}


def unkillable_profile(shape):
    """(S1): a part of size 0 or 2 can never cancel, because h_c(empty) = 1
    and h_c({u,v}) = W_c(u,v) != 0 for the anchor edge uv.  So an extra
    perfect matching whose every part has size at most 2 forces a LIVE split
    with no faithfulness hypothesis at all -- it is UNKILLABLE.
    """
    return max(shape) <= 2


def extra_matching_profiles(n, triple):
    """Masks of the parts induced by each non-pure PM of the anchor cubic."""
    edge_sets = [frozenset(frozenset(edge) for edge in matching)
                 for matching in triple]
    allowed = edge_sets[0] | edge_sets[1] | edge_sets[2]
    out = []
    total = 0
    for candidate in perfect_matchings(list(range(n))):
        chosen = frozenset(frozenset(edge) for edge in candidate)
        if not chosen <= allowed:
            continue
        total += 1
        if chosen in edge_sets:
            continue
        masks = [0, 0, 0]
        for edge in chosen:
            u, v = sorted(edge)
            for colour in range(3):
                if edge in edge_sets[colour]:
                    masks[colour] |= (1 << u) | (1 << v)
        out.append(tuple(masks))
    return out, total


# ============================================================== section K


def section_k2_boundary():
    """Where k >= 3 enters Theorem B, and how K_4 escapes both places."""
    # (B1): the parity condition is satisfiable exactly when k is even, and
    # k = 2 is even.  The unique chord matching of C_4 is same-parity.
    chords = list(chord_matchings(4))
    require(len(chords) == 1,
            "C_4 has %d chord matchings, not the single one that makes K_4"
            % len(chords))
    only = list(chords[0])
    require(all((chord[0] - chord[1]) % 2 == 0 for chord in only),
            "the chord matching of C_4 is not same-parity, so K_4 would die "
            "at (B1)")
    require(pm_count_via_subsets(4, only) == 3,
            "C_4 plus its chords does not have exactly three perfect matchings")

    # (B2): at k = 2 the unique mixed pair IS the whole chord matching, so it
    # yields M_2 itself rather than a fourth matching.  That is the escape.
    evens = [chord for chord in only if chord[0] % 2 == 0]
    odds = [chord for chord in only if chord[0] % 2 == 1]
    require(len(evens) == 1 and len(odds) == 1,
            "the chord matching of C_4 does not split into one even and one "
            "odd chord")
    require(crosses(evens[0], odds[0], 4),
            "the two chords of C_4 do not cross, so (B2)'s live pair is "
            "missing at k = 2")
    pair_is_everything = len(evens) + len(odds) == len(only)
    require(pair_is_everything,
            "the mixed crossing pair at k=2 is not all of M_2, so K_4 would "
            "produce a fourth perfect matching")

    # At k >= 3 the same crossing pair is a PROPER subset whenever it exists;
    # (B3) then shows it always does not exist, which is the contradiction.
    proper_at_k3 = 0
    for k in (3, 4, 5, 6):
        n = 2 * k
        for candidate in chord_matchings(n):
            candidate = list(candidate)
            if any((chord[0] - chord[1]) % 2 for chord in candidate):
                continue
            even_chords = [c for c in candidate if c[0] % 2 == 0]
            odd_chords = [c for c in candidate if c[0] % 2 == 1]
            for first in even_chords:
                for second in odd_chords:
                    if crosses(first, second, n):
                        require(len(candidate) > 2,
                                "a crossing mixed pair at k=%d is all of M_2, "
                                "so (B2) would not force a fourth matching"
                                % k)
                        proper_at_k3 += 1
    require(proper_at_k3 > 0,
            "no proper crossing mixed pair was found at any k >= 3, so the "
            "k >= 3 entry point of (B2) is vacuous")

    # Theorem A must NOT exclude k = 2: K_4 satisfies all of (A1)-(A5).
    record, tables = check_theorem_a(4, k4_packet(), "k=2 boundary K_4")
    require(record["termwise_dead"] and record["star_ranks"] == [3],
            "Theorem A excludes the k = 2 configuration it must preserve")
    return {"chord_matchings_of_C4": len(chords),
            "k2_mixed_pair_is_all_of_M2": pair_is_everything,
            "proper_crossing_pairs_at_k_at_least_3": proper_at_k3,
            "k2_theorem_a_record": {"termwise_dead": record["termwise_dead"],
                                    "star_ranks": record["star_ranks"],
                                    "tw2_violations": record["tw2_violations"]}}


# ================================================================= ledger


def audit():
    ledger = {}
    ledger["rank_controls"] = section_rank_controls()
    ledger["k4"] = section_k4()
    ledger["hamiltonian_family"] = section_hamiltonian_family([6, 8, 10, 12])
    ledger["exhaustive_n4"] = section_exhaustive_n4()
    ledger["signed_packets"] = section_signed_packets(600)
    ledger["theorem_a_negative_probes"] = section_theorem_a_negative_probes()
    ledger["rank2_vacuity"] = section_rank2_vacuity(6)
    ledger["b_characterisation"] = section_b_characterisation(5)
    ledger["b1_b2"] = section_b1_b2(6)
    exhaustive, pruned = section_b_exhaustive(6, 10)
    ledger["b_exhaustive"] = exhaustive
    ledger["b_pruned"] = pruned
    ledger["b3"] = section_b3(14, 6)
    ledger["b_disjoint_triples"] = section_b_disjoint_triples([4, 6, 8])
    ledger["packet_dictionary"] = section_packet_dictionary([4, 6])
    ledger["faithfulness_probes"] = section_faithfulness_probes()
    ledger["theorem_c_instances"] = section_theorem_c_instances(300)
    ledger["second_matching_reach"] = section_second_matching_reach([6, 8])
    ledger["faithfulness_load_bearing"] = section_faithfulness_load_bearing()
    single, multi = section_theorem_c_exhaustive_n6()
    ledger["theorem_c_census_single_colour"] = single
    ledger["theorem_c_census_multi_colour"] = multi
    ledger["stall"] = section_stall([6, 8], [6, 8, 10, 12])
    ledger["k2_boundary"] = section_k2_boundary()
    ledger["proved"] = (
        "THEOREM A: for anchored packets, termwise-deadness implies TW2, and "
        "anchored + TW2 forces essential edges to be monochromatic with "
        "pairwise disjoint essential graphs, every vertex to carry an "
        "essential edge of every colour, EVERY STAR TO HAVE RANK EXACTLY 3, "
        "and every two-coloured edge to be inessential in all three colours.  "
        "THEOREM B: K_4 is the only cubic graph whose three perfect matchings "
        "form a proper 3-edge-colouring and are its only perfect matchings.  "
        "THEOREM C: for every k >= 3 there is no anchored matching-faithful "
        "termwise-dead packet.  All three are hand proofs, stated in the "
        "companion note and verified here on nonvacuous instances"
    )
    ledger["not_proved"] = (
        "The termwise condition with ARBITRARY CANCELLATION remains open for "
        "k >= 6: Theorem C assumes matching-faithfulness, and the committed "
        "SAT theorem of proofs/diagonal-hafnian-recurrence-obstruction.md "
        "covers cancellation only at k = 3,4,5.  The stall is precisely "
        "whether h_c(S_c) = 0 can be arranged on matched sets for every extra "
        "perfect matching and every anchor choice at once; (S1) and (S2) "
        "narrow it and the k = 3 profile measurement closes k = 3 without any "
        "faithfulness hypothesis, but the same measurement shows the route is "
        "unavailable already at k = 4.  Krenn's conjecture remains open"
    )
    ledger["scope"] = (
        "Everything here is about DIAGONAL packets -- symmetric zero-diagonal "
        "scalar edge matrices W_0,W_1,W_2 -- which is the shadow an exact "
        "ternary source induces through Theorem B of "
        "notes/exact-source-live-split-forcing.md, not an exact source "
        "itself.  Nothing here supplies a live split for a cancelling packet "
        "at any k >= 6, and nothing here touches the crossing-matching "
        "cluster.  The rank-2 vacuity statement is a statement about "
        "termwise-dead configurations only: the rank-2 pencil geometry is "
        "perfectly non-vacuous elsewhere, as the 2k-cycle counterexamples of "
        "section R show"
    )
    return ledger


def main():
    ledger = audit()
    digest = content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "termwise rank-3 cubic uniqueness ledger changed")

    print("termwise rank-3 cubic uniqueness: PASS (exact)")
    controls = ledger["rank_controls"]
    print("rank routine: %d designed cases and %d deterministic 3x3 integer "
          "cases agree with an independent Gaussian rank; ranks seen %s"
          % (controls["designed_cases"], controls["random_cases"],
             list(controls["rank_histogram"])))
    k4 = ledger["k4"]
    print("THEOREM A, k=2: K_4 is termwise-dead, TW2-clean, essential sizes "
          "%s, star ranks %s, %d perfect matchings of the union, haf(pencil) "
          "= %s" % (k4["essential_sizes"], k4["star_ranks"],
                    k4["perfect_matchings_of_the_union"],
                    " + ".join("%s x_0^%d x_1^%d x_2^%d" % (value, *key)
                               for key, value in k4["pencil"])))
    for record in ledger["hamiltonian_family"]:
        print("  D(%2d): TW2-clean, star ranks %s, termwise_dead=%s, "
              "#PM(union)=%d, #live=%d = #PM-3, live shapes %s"
              % (record["n"], record["star_ranks"], record["termwise_dead"],
                 record["perfect_matchings_of_the_union"],
                 record["live_splits"], record["live_shapes"]))
    census = ledger["exhaustive_n4"]
    print("  EXHAUSTIVE 0/1 packets at n=4: %d examined, %d anchored, %d also "
          "TW2-clean (A2-A5 verified on each), %d termwise-dead -- exactly the "
          "colour-orderings of the K_4 one-factorisation"
          % (census["examined"], census["anchored"],
             census["anchored_and_tw2_clean"], census["termwise_dead"]))
    signed = ledger["signed_packets"]
    print("  signed packets at n=6,8: %d built, %d anchored, %d also TW2-clean "
          "-- A2-A5 verified on all of those, star-rank profile %s"
          % (signed["trials"], signed["anchored"],
             signed["anchored_and_tw2_clean"], signed["rank_profile"]))
    for probe in ledger["theorem_a_negative_probes"]:
        print("  negative probe %s: fires as designed" % probe["probe"])
    vacuity = ledger["rank2_vacuity"]
    print("RANK-2 VACUITY: the 2k-cycle pencil counterexamples over "
          "Z[zeta_2k] have star ranks %s for k=%s, so by (A4) not one of them "
          "is termwise-dead; each also has %s TW2 violations, an independent "
          "second reason"
          % (sorted({tuple(record["star_ranks"])[0]
                     for record in vacuity["detail"]}), vacuity["orders"],
             [record["tw2_violations"] for record in vacuity["detail"]]))
    for record in ledger["b_characterisation"]:
        print("THEOREM B (char) k=%d: %d chord matchings, subset-A count == "
              "direct hafnian count, PM counts seen %s"
              % (record["k"], record["chord_matchings"],
                 record["distinct_pm_counts"]))
    for record in ledger["b1_b2"]:
        print("  k=%d: (B1) %d live / %d dead singletons, %d matchings killed "
              "by an opposite-parity chord; (B2) %d live crossing and %d dead "
              "non-crossing mixed pairs, %d of the live ones proper"
              % (record["k"], record["live_singletons"],
                 record["dead_singletons"],
                 record["matchings_killed_by_an_opposite_parity_chord"],
                 record["live_crossing_mixed_pairs"],
                 record["dead_noncrossing_mixed_pairs"],
                 record["proper_live_crossing_pairs"]))
    for record in ledger["b_exhaustive"]:
        print("  k=%2d (n=%2d): %8d Hamiltonian-cycle cubic graphs, min #PM=%d, "
              "with exactly three: %d%s"
              % (record["k"], record["n"], record["graphs"],
                 record["minimum_pm_count"],
                 record["graphs_with_exactly_three"],
                 "   <-- K_4" if record["k"] == 2 else ""))
    for record in ledger["b_pruned"]:
        print("  k=%2d (n=%2d): (B1) survivors %8d, (B1)+(B2) survivors %d"
              % (record["k"], record["n"], record["after_b1"],
                 record["after_b2"]))
    b3 = ledger["b3"]
    print("  (B3) signature criterion validated against direct search on %d "
          "arc systems (%d yes, %d no); scans: %s"
          % (b3["control_agreements"], b3["control_yes"], b3["control_no"],
             {record["k"]: record["even_matchings_scanned"]
              for record in b3["scans"]}))
    for record in ledger["b_disjoint_triples"]:
        print("  (B0) n=%2d: %8d disjoint PM triples, %d with exactly three "
              "perfect matchings, all pairwise Hamiltonian"
              % (record["n"], record["triples"],
                 record["triples_with_exactly_three"]))
    for record in ledger["packet_dictionary"]:
        print("  dictionary n=%d: %d packets, #live == #PM-3 and dead <=> "
              "#PM==3 on all of them; %d dead"
              % (record["n"], record["packets"], record["termwise_dead"]))
    probes = ledger["faithfulness_probes"]
    print("THEOREM C: matching-faithfulness pinned both ways -- a nonnegative "
          "matrix is faithful on %d matched even sets, and a designed "
          "cancelling matrix fails on %d of them (masks %s)"
          % (probes["positive_matched_sets"], probes["negative_failures"],
             probes["negative_failure_masks"]))
    instances = ledger["theorem_c_instances"]
    print("  steps 1-4 on %d nonnegative packets at n=6,8: %d anchored, "
          "verdicts %s, %d confirmed not termwise-dead by a full split "
          "census; induced parts carrying two or more matchings: %d "
          "(DISCLOSED: faithfulness is inert on this family)"
          % (instances["trials"], instances["checked"], instances["verdicts"],
             instances["full_censuses_confirming_not_dead"],
             instances["parts_with_two_or_more_matchings"]))
    for record in ledger["second_matching_reach"]:
        print("  (S2) reach at n=%d: %d induced parts of size >= 4, %d of "
              "them admit a second perfect matching avoiding the anchor union"
              % (record["n"], record["induced_parts_of_size_at_least_4"],
                 record["parts_admitting_a_second_matching"]))
    for record in ledger["faithfulness_load_bearing"]:
        print("  load-bearing %s: %d matchings inside the part, positive "
              "h_c(S_c)=%s, cancelling twin (same support, one sign flipped) "
              "h_c(S_c)=%s -- the Step-4 test answers TRUE then FALSE"
              % (record["label"], record["matchings_inside_the_part"],
                 record["positive_h"], record["twin_h"]))
    for key in ("theorem_c_census_single_colour",
                "theorem_c_census_multi_colour"):
        record = ledger[key]
        print("  EXHAUSTIVE n=6 census (%s): %d packets, all %d with a live "
              "step-4 split, %d cross-checked by a full 3^6 census"
              % (record["label"], record["packets"],
                 record["with_a_live_step4_split"],
                 record["full_censuses_cross_checked"]))
    stall = ledger["stall"]
    print("THE STALL: (S1) exercised on %d two-element parts, (S2) on %d "
          "anchor-only splits"
          % (stall["s1_two_element_parts_checked"],
             stall["s2_anchor_only_splits_checked"]))
    for record in stall["profiles"]:
        print("  k=%d: %d anchor cubic graphs, %d extra matchings, %d of them "
              "with every part <= 2; graphs whose extras are ALL unkillable: "
              "%d; profiles %s"
              % (record["k"], record["anchor_cubic_graphs"],
                 record["extra_matchings"],
                 record["extra_matchings_with_every_part_at_most_2"],
                 record["graphs_all_of_whose_extras_are_unkillable"],
                 record["profile_histogram"]))
    for record in stall["hamiltonian_family"]:
        print("  D(%2d): #PM(union)=%d, %d extra matchings, profiles %s"
              % (record["n"], record["perfect_matchings_of_the_union"],
                 record["extra_matchings"], record["profile_histogram"]))
    boundary = ledger["k2_boundary"]
    print("k=2 BOUNDARY: C_4 has %d chord matching, same-parity (so (B1) is "
          "satisfied), and its unique mixed crossing pair is all of M_2 (so "
          "(B2) yields no fourth matching); at k >= 3 there are %d proper "
          "crossing mixed pairs, and (B3) shows none survives"
          % (boundary["chord_matchings_of_C4"],
             boundary["proper_crossing_pairs_at_k_at_least_3"]))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
