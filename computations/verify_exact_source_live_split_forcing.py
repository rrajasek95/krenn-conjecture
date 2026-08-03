#!/usr/bin/env python3
"""Live-split forcing for exact ternary sources, and the essentiality
structure lemma (E1)-(E3).

Companion note: `notes/exact-source-live-split-forcing.md` (hand proofs).

Conventions are those of
`computations/verify_target_flattening_essential_star_pair_bound.py`:
endpoint-ordered blocks A_uv in V_u (x) V_v with `oriented(...)` putting
the u-mode on the left, `perfect_matchings`, `matching_tensor`, and the
deleted endpoint star sigma_u^(v) of
`notes/target-flattening-essential-star-pair-bound.md` equation (2).  A
pair {u,v} is GOOD when both sigma_u^(v) and sigma_v^(u) are injective.

What this checker establishes, and at which strength:

  * Lemma 0 and Theorem A are POLYNOMIAL IDENTITIES in the block
    entries.  They are proved by hand in the note; here they are
    verified on MATCHING-SUPPORTED degree-two monomial packets at N = 4
    (both sides of (5) and (6) are degree-two multilinear in the block
    entries at N = 4, so a SINGLE-cell packet makes both sides vanish
    identically and checks nothing; the 243 packets used here put one
    cell on each edge of a perfect matching of K_4, so each has nonzero
    H_B) and on deterministic pseudorandom integer packets at
    N = 4, 6, 8, over every ordered even partition.  The checker counts
    and reports how many of the checked equations are NONVACUOUS (some
    side nonzero) and refuses to pass if that count is zero.  The parity
    fact ("a matching with a crossing edge has at least two") is
    verified EXHAUSTIVELY over all (split, matching) pairs at N = 4 and
    N = 6 -- it is a statement about matchings alone, so this is a
    complete check of the combinatorial content at those orders.

  * The live-split reduction combines Lemma 0 with the UNSAT theorem of
    `proofs/diagonal-hafnian-recurrence-obstruction.md` (n in {6,8,10}).
    This checker does NOT re-run that SAT proof.  It verifies the side
    that belongs here: that the Boolean shadow z_c(S) = [haf W_c[S] != 0]
    read off EACH OF SEVEN block families really is a model of the
    recurrence constraints (5)-(7) of that proof, at every colour, every
    even subset and every pivot -- so UNSAT applies to those -- and that
    Lemma 0 supplies its units z_c(B) = 1.  The claim for an ARBITRARY
    block family is the note's hand proof, not this machine check.

  * The essentiality structure lemma -- identity (*), (E1), (E2), (E3),
    colour injectivity, the disjoint-bad-pair rigidity, the proposition
    "essential colour != own part colour" (C2) and the counting bound
    (C4) -- is proved by hand in the note.  Here it is VERIFIED ON
    INSTANCES: on the exact K_4 three-one-factorization source (a
    genuinely exact ternary source: H_B(A) = Delta_{B,3} with zero
    defects).  C2 and C4 concern live splits, and are VACUOUS on the
    omega guard, whose crossing graph equals its good-pair graph (zero
    bad crossing pairs, so their requires read 0 <= 16 and 16 >= 0);
    they carry content only on the six-site guard, which has six bad
    crossing pairs.  The checker records the number of C2 instances
    actually exercised per packet so this is visible in the ledger.

  * Two guards are verified.  On the eight-site omega packet of
    `notes/curved-two-chart-omega-diagonal-row-guard.md` (6), single-
    colouredness, (E1) and (E2) hold at all 21 essential ordered pairs,
    while identity (*) and (E3) fail at all 21.  So what the packet's
    satisfied rows fail to imply is specifically (E3) -- not the whole
    structure lemma.  A new six-site integer packet satisfies 727 of the
    729 exactness equations -- including all three pure anchors and
    every live-split colouring equation -- yet both cells forced by
    Theorem A sit on BAD crossing pairs.  So the weak form of the
    crossing-pairs-are-good lemma is REFUTED under those weak
    hypotheses.  (E3) is exactly what that guard breaks too, and it
    breaks it exactly at the two pairs carrying the forced cells.

Exact stdlib arithmetic only: int and Fraction.  No floats, no numpy,
no third-party imports, no bare asserts.  Krenn's conjecture remains
open.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json


COLORS = (0, 1, 2)

EXPECTED_LEDGER_SHA256 = (
    "a0bf3107ad8a8c175bb5c905f725b458bd10c6bed44ddaf0273837c0a74bb5fd"
)


def require(condition, detail):
    """Assertion that survives `python3 -O` (never use a bare assert)."""
    if not condition:
        raise RuntimeError(detail)


# --------------------------------------------------------------- hashing


def canonical(value):
    """Canonical JSON-able image of exact data (Fractions become strings)."""
    if value is None:
        # "undetermined" (e.g. a multi-dimensional essential kernel); hashes
        # as JSON null, which no colour or count can collide with.
        return None
    if isinstance(value, Fraction):
        return "F" + str(value)
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return [
            [canonical(key), canonical(value[key])]
            for key in sorted(value, key=repr)
        ]
    if isinstance(value, (set, frozenset)):
        return sorted((canonical(item) for item in value), key=repr)
    if isinstance(value, (list, tuple)):
        return [canonical(item) for item in value]
    raise RuntimeError("canonical: unsupported value type %r" % (type(value),))


def content_hash(value):
    encoded = json.dumps(canonical(value), sort_keys=True,
                         separators=(",", ":"))
    return sha256(encoded.encode("ascii")).hexdigest()


# ---------------------------------------------------------- linear algebra


def rank(rows):
    matrix = [[Fraction(entry) for entry in row] for row in rows]
    if not matrix:
        return 0
    width = len(matrix[0])
    pivot_row = 0
    for column in range(width):
        pivot = None
        for index in range(pivot_row, len(matrix)):
            if matrix[index][column] != 0:
                pivot = index
                break
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for index in range(len(matrix)):
            if index == pivot_row:
                continue
            factor = matrix[index][column]
            if factor == 0:
                continue
            matrix[index] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(matrix[index], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def left_nullspace(rows):
    """Basis of {phi in Q^3 : sum_i phi_i rows[i] = 0}, tracked by augmenting."""
    require(len(rows) == 3, "left_nullspace expects the three colour rows")
    width = len(rows[0])
    require(width > 0, "left_nullspace on an empty star is not used here")
    augmented = [
        [Fraction(entry) for entry in rows[index]]
        + [Fraction(int(index == column)) for column in COLORS]
        for index in COLORS
    ]
    pivot_row = 0
    for column in range(width):
        pivot = None
        for index in range(pivot_row, 3):
            if augmented[index][column] != 0:
                pivot = index
                break
        if pivot is None:
            continue
        augmented[pivot_row], augmented[pivot] = (
            augmented[pivot], augmented[pivot_row],
        )
        scale = augmented[pivot_row][column]
        augmented[pivot_row] = [
            entry / scale for entry in augmented[pivot_row]
        ]
        for index in range(3):
            if index == pivot_row:
                continue
            factor = augmented[index][column]
            if factor:
                augmented[index] = [
                    entry - factor * pivot_entry
                    for entry, pivot_entry in zip(
                        augmented[index], augmented[pivot_row]
                    )
                ]
        pivot_row += 1
        if pivot_row == 3:
            break
    basis = []
    for index in range(pivot_row, 3):
        require(
            all(entry == 0 for entry in augmented[index][:width]),
            "left_nullspace produced a nonzero residual row",
        )
        basis.append(tuple(augmented[index][width:]))
    return basis


# ----------------------------------------------------------------- blocks


def edge(u, v):
    return (u, v) if u < v else (v, u)


def transpose(matrix):
    return tuple(tuple(matrix[j][i] for j in COLORS) for i in COLORS)


def oriented(blocks, u, v):
    """A_uv with the u-mode on the left (endpoint-ordered convention)."""
    matrix = blocks[edge(u, v)]
    return matrix if u < v else transpose(matrix)


def zero_blocks(sites):
    return {
        (u, v): tuple(tuple(Fraction(0) for _ in COLORS) for _ in COLORS)
        for u, v in combinations(sorted(sites), 2)
    }


def set_cell(blocks, u, v, i, j, value):
    """Set A_uv(i,j) = value with i read at u and j at v."""
    key = edge(u, v)
    matrix = [list(row) for row in blocks[key]]
    if u < v:
        matrix[i][j] = Fraction(value)
    else:
        matrix[j][i] = Fraction(value)
    blocks[key] = tuple(tuple(row) for row in matrix)


def block_image(blocks):
    return {
        "%d-%d" % key: [[str(entry) for entry in row] for row in blocks[key]]
        for key in sorted(blocks)
    }


# -------------------------------------------------------------- matchings


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(remainder):
            yield (edge(first, second),) + tail


def coefficient(blocks, sites, word):
    """H_S(A) evaluated at the word `word` (dict site -> colour)."""
    total = Fraction(0)
    for matching in perfect_matchings(sorted(sites)):
        term = Fraction(1)
        for u, v in matching:
            term *= blocks[(u, v)][word[u]][word[v]]
            if term == 0:
                break
        total += term
    return total


def matching_tensor(blocks, sites):
    """H_S(A) as a dict of nonzero coefficients keyed by the word."""
    sites = tuple(sorted(sites))
    matchings = tuple(perfect_matchings(sites))
    tensor = {}
    for values in product(COLORS, repeat=len(sites)):
        word = dict(zip(sites, values))
        total = Fraction(0)
        for matching in matchings:
            term = Fraction(1)
            for u, v in matching:
                term *= blocks[(u, v)][word[u]][word[v]]
                if term == 0:
                    break
            total += term
        if total:
            tensor[values] = total
    return tensor


def hafnian(blocks, colour, subset):
    """haf(W_colour[subset]) with W_c(u,v) = A_uv(c,c) and haf(empty) = 1."""
    subset = tuple(sorted(subset))
    if len(subset) % 2:
        return Fraction(0)
    total = Fraction(0)
    for matching in perfect_matchings(subset):
        term = Fraction(1)
        for u, v in matching:
            term *= blocks[(u, v)][colour][colour]
            if term == 0:
                break
        total += term
    return total


def target_tensor(sites):
    return {tuple([c] * len(sites)): Fraction(1) for c in COLORS}


def exactness_defects(blocks, sites):
    """Words where H_S(A) differs from Delta_{S,3}."""
    tensor = matching_tensor(blocks, sites)
    target = target_tensor(sites)
    defects = {}
    for word in set(tensor) | set(target):
        got = tensor.get(word, Fraction(0))
        want = target.get(word, Fraction(0))
        if got != want:
            defects[word] = (got, want)
    return defects


# --------------------------------------------------------------- goodness


def star_matrix(blocks, sites, endpoint, omitted):
    """Matrix of sigma_endpoint^(omitted); rows indexed by the u-mode colour."""
    rows = [[] for _ in COLORS]
    for site in sorted(sites):
        if site == endpoint or site == omitted:
            continue
        matrix = oriented(blocks, endpoint, site)
        for i in COLORS:
            rows[i].extend(matrix[i])
    return rows


def star_injective(blocks, sites, endpoint, omitted):
    return rank(star_matrix(blocks, sites, endpoint, omitted)) == 3


def is_good_pair(blocks, sites, u, v):
    return star_injective(blocks, sites, u, v) and star_injective(
        blocks, sites, v, u
    )


def good_pairs(blocks, sites):
    return {
        edge(u, v)
        for u, v in combinations(sorted(sites), 2)
        if is_good_pair(blocks, sites, u, v)
    }


# ----------------------------------------------------------------- splits


def even_splits(sites):
    """Ordered partitions (S_0,S_1,S_2) into even parts, constant excluded."""
    sites = tuple(sorted(sites))
    order = len(sites)
    for assignment in product(COLORS, repeat=order):
        parts = ([], [], [])
        for site, colour in zip(sites, assignment):
            parts[colour].append(site)
        if any(len(part) % 2 for part in parts):
            continue
        if max(len(part) for part in parts) == order:
            continue
        yield tuple(tuple(part) for part in parts)


def split_product(blocks, split):
    value = Fraction(1)
    for colour in COLORS:
        value *= hafnian(blocks, colour, split[colour])
        if value == 0:
            return Fraction(0)
    return value


def live_splits(blocks, sites):
    return [
        split for split in even_splits(sites)
        if split_product(blocks, split) != 0
    ]


def part_map(split):
    table = {}
    for colour in COLORS:
        for site in split[colour]:
            table[site] = colour
    return table


def split_word(split, sites):
    table = part_map(split)
    return tuple(table[site] for site in sorted(sites))


def crossing_pairs(split):
    table = part_map(split)
    return {
        edge(u, v)
        for u, v in combinations(sorted(table), 2)
        if table[u] != table[v]
    }


def crossing_matchings_terms(blocks, sites, split):
    """(matching, crossing edges, term) over nonzero crossing matchings."""
    table = part_map(split)
    output = []
    for matching in perfect_matchings(sorted(sites)):
        crossing = tuple(
            e for e in matching if table[e[0]] != table[e[1]]
        )
        if not crossing:
            continue
        term = Fraction(1)
        for u, v in matching:
            term *= blocks[(u, v)][table[u]][table[v]]
            if term == 0:
                break
        if term:
            output.append((matching, crossing, term))
    return output


# ---------------------------------------------------------------- packets


def k4_one_factorization_packet():
    """The exact K_4 three-one-factor source.

    `notes/adaptive-diagonal-uncollision-cap-routing.md`, guard 1 of the
    two complementary guards ("The exact K_4 three-one-factor source is
    entry-minimal ... its selected pairs are not good").
    """
    sites = (0, 1, 2, 3)
    blocks = zero_blocks(sites)
    factors = {0: [(0, 1), (2, 3)], 1: [(0, 2), (1, 3)], 2: [(0, 3), (1, 2)]}
    for colour, pairs in factors.items():
        for u, v in pairs:
            set_cell(blocks, u, v, colour, colour, 1)
    return sites, blocks


def omega_guard_packet():
    """`notes/curved-two-chart-omega-diagonal-row-guard.md`, packet (5)-(6)."""
    names = ("p", "q", "a", "b", "c", "d", "r", "s")
    index = {name: position for position, name in enumerate(names)}
    table = {
        0: ("pq", "pr", "pa", "qb", "cd", "rs"),
        1: ("pd", "qs", "ac", "br"),
        2: ("pc", "qr", "ad", "bs"),
    }
    sites = tuple(range(8))
    blocks = zero_blocks(sites)
    for colour, pairs in table.items():
        for pair in pairs:
            set_cell(blocks, index[pair[0]], index[pair[1]], colour, colour, 1)
    return sites, blocks, names


SIX_SITE_SITES = tuple(range(6))
SIX_SITE_FACTORS = {
    0: ((0, 1), (2, 3), (4, 5)),
    1: ((2, 4), (0, 3), (1, 5)),
    2: ((3, 5), (0, 2), (1, 4)),
}
SIX_SITE_SPLIT = ((0, 1), (2, 4), (3, 5))
SIX_SITE_CARRIERS = ((0, 3), (1, 5))


def six_site_guard_packet(first, second):
    """A prism one-factorization plus two off-diagonal crossing cells.

    The diagonal part is a one-factorization of the TRIANGULAR PRISM
    (triangles {0,2,3} and {1,4,5} joined by the matching 01|24|35), not
    of K_6: its nine edges are a cubic subgraph of K_6, and a K_6
    one-factorization would need five factors, not three.  It is chosen
    so that S_0 = {0,1}, S_1 = {2,4}, S_2 = {3,5} is a live split; the
    two extra cells A_03(0,2) and A_15(0,2) are the off-diagonal freedom.
    """
    blocks = zero_blocks(SIX_SITE_SITES)
    for colour, pairs in SIX_SITE_FACTORS.items():
        for u, v in pairs:
            set_cell(blocks, u, v, colour, colour, 1)
    set_cell(blocks, 0, 3, 0, 2, first)
    set_cell(blocks, 1, 5, 0, 2, second)
    return blocks


# ------------------------------------------------- section 1: identities


def pseudorandom_stream(seed):
    """Deterministic stdlib-free integer stream (no `random`, no floats)."""
    state = seed & 0x7FFFFFFF

    def nextint(modulus):
        nonlocal state
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        return (state >> 7) % modulus

    return nextint


def pseudorandom_blocks(sites, nextint, spread):
    blocks = zero_blocks(sites)
    for key in sorted(blocks):
        blocks[key] = tuple(
            tuple(Fraction(nextint(2 * spread + 1) - spread) for _ in COLORS)
            for _ in COLORS
        )
    return blocks


def check_parity_exhaustive(sites):
    """Every matching leaves each even part an even number of times."""
    checked = 0
    matchings = tuple(perfect_matchings(sorted(sites)))
    for split in even_splits(sites):
        table = part_map(split)
        for matching in matchings:
            for colour in COLORS:
                leaving = sum(
                    1 for e in matching
                    if (table[e[0]] == colour) != (table[e[1]] == colour)
                )
                require(
                    leaving % 2 == 0,
                    "parity: odd number of matching edges leaves an even part",
                )
            crossing = [e for e in matching if table[e[0]] != table[e[1]]]
            require(
                len(crossing) != 1,
                "parity: a matching had exactly one crossing edge",
            )
            checked += 1
    return checked


def check_identities(blocks, sites):
    """Lemma 0 and Theorem A as identities on one block family.

    Returns (splits checked, nonvacuous Theorem A equations, nonvacuous
    Lemma 0 equations).  An equation is NONVACUOUS when its common value
    is nonzero; a check that is 0 == 0 verifies nothing, so the caller
    is expected to require that the nonvacuous counts are positive.
    """
    lemma0_nonvacuous = 0
    for colour in COLORS:
        word = {site: colour for site in sites}
        left = coefficient(blocks, sites, word)
        require(
            left == hafnian(blocks, colour, sites),
            "Lemma 0 identity failed: constant word != full hafnian",
        )
        if left != 0:
            lemma0_nonvacuous += 1
    splits = 0
    nonvacuous = 0
    for split in even_splits(sites):
        word = dict(zip(sorted(sites), split_word(split, sites)))
        left = coefficient(blocks, sites, word)
        product_part = Fraction(1)
        for colour in COLORS:
            product_part *= hafnian(blocks, colour, split[colour])
        crossing_part = sum(
            (term for _, _, term in
             crossing_matchings_terms(blocks, sites, split)),
            Fraction(0),
        )
        require(
            left == product_part + crossing_part,
            "Theorem A identity failed: split coefficient != product + "
            "crossing sum",
        )
        splits += 1
        if left != 0 or product_part != 0 or crossing_part != 0:
            nonvacuous += 1
    return splits, nonvacuous, lemma0_nonvacuous


def matching_supported_monomial_packets(sites):
    """Degree-two monomial packets with a nonzero H_B, at N = 4.

    Both sides of Lemma 0 and of Theorem A are degree-two multilinear in
    the block entries at N = 4, so a packet with a single nonzero cell
    makes every term vanish and checks nothing.  Instead put one cell on
    each edge of a perfect matching: for each of the three perfect
    matchings of K_4 and each of the 9 x 9 cell choices, the resulting
    packet has exactly one nonzero matching term (the three perfect
    matchings of K_4 are pairwise edge-disjoint), hence H_B(A) != 0.
    """
    packets = []
    for matching in perfect_matchings(sorted(sites)):
        for cells in product(product(COLORS, repeat=2), repeat=len(matching)):
            blocks = zero_blocks(sites)
            for (u, v), (i, j) in zip(matching, cells):
                set_cell(blocks, u, v, i, j, 1)
            packets.append(blocks)
    return packets


def section_identities():
    nextint = pseudorandom_stream(20260803)
    record = {}
    for order in (4, 6):
        sites = tuple(range(order))
        record["parity_pairs_N%d" % order] = check_parity_exhaustive(sites)

    sites = tuple(range(4))
    packets = matching_supported_monomial_packets(sites)
    monomial_nonvacuous = 0
    monomial_lemma0 = 0
    for blocks in packets:
        require(
            matching_tensor(blocks, sites),
            "matching-supported monomial packet has H_B = 0, so its identity "
            "checks would be vacuous",
        )
        _, nonvacuous, lemma0 = check_identities(blocks, sites)
        monomial_nonvacuous += nonvacuous
        monomial_lemma0 += lemma0
    record["monomial_packets_N4"] = len(packets)
    record["monomial_theoremA_nonvacuous"] = monomial_nonvacuous
    record["monomial_lemma0_nonvacuous"] = monomial_lemma0
    require(
        monomial_nonvacuous > 0 and monomial_lemma0 > 0,
        "monomial identity checks are vacuous: every equation read 0 == 0",
    )

    used = []
    nonvacuous_total = {}
    for order, trials, spread in ((4, 12, 3), (6, 5, 3), (8, 2, 2)):
        sites = tuple(range(order))
        splits = 0
        nonvacuous = 0
        lemma0 = 0
        for _ in range(trials):
            blocks = pseudorandom_blocks(sites, nextint, spread)
            used.append(block_image(blocks))
            splits, packet_nonvacuous, packet_lemma0 = check_identities(
                blocks, sites
            )
            nonvacuous += packet_nonvacuous
            lemma0 += packet_lemma0
        record["even_splits_N%d" % order] = splits
        record["random_packets_N%d" % order] = trials
        record["random_theoremA_nonvacuous_N%d" % order] = nonvacuous
        record["random_lemma0_nonvacuous_N%d" % order] = lemma0
        nonvacuous_total[order] = (nonvacuous, lemma0)
    require(
        all(value > 0 for pair in nonvacuous_total.values() for value in pair),
        "pseudorandom identity checks are vacuous at some order",
    )
    record["random_packet_sha256"] = content_hash(used)
    return record


# --------------------------------------- section 2: Boolean shadow model


def boolean_shadow(blocks, sites, colour):
    """z_c(S) = [haf W_c[S] != 0] over every even subset S."""
    shadow = {}
    sites = tuple(sorted(sites))
    for size in range(0, len(sites) + 1, 2):
        for subset in combinations(sites, size):
            shadow[subset] = hafnian(blocks, colour, subset) != 0
    return shadow


def check_shadow_is_a_model(blocks, sites, colour):
    """Constraints (5)-(7) of proofs/diagonal-hafnian-recurrence-obstruction.

    For every even S and every pivot u in S, with
    t(S;u,v) = z({u,v}) and z(S \\ {u,v}):
      (i)  z(S) = 1 forces at least one true t;
      (ii) z(S) = 0 forbids exactly one true t.
    """
    shadow = boolean_shadow(blocks, sites, colour)
    checked = 0
    for subset, live in shadow.items():
        for pivot in subset:
            terms = 0
            for other in subset:
                if other == pivot:
                    continue
                rest = tuple(s for s in subset if s not in (pivot, other))
                if shadow[edge(pivot, other)] and shadow[rest]:
                    terms += 1
            if live:
                require(
                    terms >= 1,
                    "Boolean shadow: a live hafnian had no supported pivot "
                    "term",
                )
            else:
                require(
                    terms != 1,
                    "Boolean shadow: a dead hafnian had exactly one supported "
                    "pivot term",
                )
            checked += 1
    return checked, shadow


def section_boolean_shadow(packets):
    nextint = pseudorandom_stream(915217)
    record = {"checks": 0, "packets": 0}
    families = list(packets)
    drawn = []
    for order, spread in ((6, 2), (8, 2)):
        sites = tuple(range(order))
        for index in range(2):
            blocks = pseudorandom_blocks(sites, nextint, spread)
            drawn.append(block_image(blocks))
            families.append(
                ("pseudorandom N=%d #%d" % (order, index), sites, blocks)
            )
    # The drawn packets are hashed into the ledger, so changing the seed
    # or the stream changes the frozen digest.
    record["pseudorandom_packet_sha256"] = content_hash(drawn)
    units = {}
    for label, sites, blocks in families:
        record["packets"] += 1
        for colour in COLORS:
            checked, shadow = check_shadow_is_a_model(blocks, sites, colour)
            record["checks"] += checked
            units.setdefault(label, []).append(shadow[tuple(sorted(sites))])
    return record, units


# ------------------------------ section 3: essentiality structure lemma


def contract(blocks, u, x, phi):
    matrix = oriented(blocks, u, x)
    return tuple(
        sum((phi[i] * matrix[i][j] for i in COLORS), Fraction(0))
        for j in COLORS
    )


def star_identity_holds(blocks, sites, u, v, phi):
    """Identity (*): phi_j [y == constant j] = psi(j) H_{B\\{u,v}}(y)."""
    rest = tuple(site for site in sorted(sites) if site not in (u, v))
    tensor = matching_tensor(blocks, rest)
    psi = contract(blocks, u, v, phi)
    for j in COLORS:
        for word in product(COLORS, repeat=len(rest)):
            left = phi[j] if all(colour == j for colour in word) else Fraction(0)
            right = psi[j] * tensor.get(word, Fraction(0))
            if left != right:
                return False
    return True


def essential_covectors(blocks, sites, u, v):
    """A basis of ker sigma_u^(v); its length is the kernel dimension."""
    return left_nullspace(star_matrix(blocks, sites, u, v))


def essential_table(blocks, sites):
    """site -> {neighbour: essential colour, or None when undetermined}.

    None is recorded whenever the kernel has dimension > 1 or its basis
    covector is not supported on a single colour; nothing is ever
    silently overwritten, so a multi-dimensional kernel cannot be
    mistaken for a clean single-colour one.  Lemma E says an EXACT
    source never produces a None here; the guards are not exact, so the
    None branch is real and every consumer of this table checks for it.
    """
    table = {site: {} for site in sites}
    for u, v in combinations(sorted(sites), 2):
        for x, y in ((u, v), (v, u)):
            basis = essential_covectors(blocks, sites, x, y)
            if not basis:
                continue
            if len(basis) > 1:
                table[x][y] = None
                continue
            support = [c for c in COLORS if basis[0][c] != 0]
            table[x][y] = support[0] if len(support) == 1 else None
    return table


def structure_status(blocks, sites, x, y, phi):
    """(single-colour?, colour a, (E1)?, (E2)?, (E3)?) for one covector."""
    support = [c for c in COLORS if phi[c] != 0]
    if len(support) != 1:
        return False, None, False, False, False
    a = support[0]
    e1 = all(
        all(entry == 0 for entry in oriented(blocks, x, z)[a])
        for z in sorted(sites) if z not in (x, y)
    )
    row = oriented(blocks, x, y)[a]
    lam = row[a]
    e2 = lam != 0 and all(row[j] == 0 for j in COLORS if j != a)
    rest = tuple(s for s in sorted(sites) if s not in (x, y))
    tensor = matching_tensor(blocks, rest)
    e3 = lam != 0 and tensor == {
        tuple([a] * len(rest)): Fraction(1) / lam
    }
    return True, a, e1, e2, e3


def structure_census(blocks, sites):
    """Per-ordered-pair (*) / single-colour / (E1) / (E2) / (E3) tallies."""
    tally = {
        "covectors": 0, "single_colour": 0, "star": 0,
        "E1": 0, "E2": 0, "E3": 0,
    }
    detail = {}
    for u, v in combinations(sorted(sites), 2):
        for x, y in ((u, v), (v, u)):
            for index, phi in enumerate(
                essential_covectors(blocks, sites, x, y)
            ):
                tally["covectors"] += 1
                star = star_identity_holds(blocks, sites, x, y, phi)
                single, _, e1, e2, e3 = structure_status(
                    blocks, sites, x, y, phi
                )
                tally["star"] += int(star)
                tally["single_colour"] += int(single)
                tally["E1"] += int(e1)
                tally["E2"] += int(e2)
                tally["E3"] += int(e3)
                detail["%d-%d#%d" % (x, y, index)] = [
                    star, single, e1, e2, e3
                ]
    return tally, detail


def kernel_dimension_census(blocks, sites):
    """Multiset of ker sigma_u^(v) dimensions over all ordered pairs."""
    census = {}
    for u, v in combinations(sorted(sites), 2):
        for x, y in ((u, v), (v, u)):
            dimension = len(essential_covectors(blocks, sites, x, y))
            census[dimension] = census.get(dimension, 0) + 1
    return {str(key): census[key] for key in sorted(census)}


def check_multidimensional_kernel_probe():
    """Exercise the multi-dimensional-kernel branch of essential_table.

    On every packet the note actually reasons about, Lemma E makes each
    essential kernel one-dimensional, so that branch would be dead code
    and its safety unverifiable.  This probe -- a four-site packet whose
    only nonzero cell is A_01(0,0) = 1 -- has stars of kernel dimension
    two and three, whose basis covectors ARE individually single-coloured
    (e_1, e_2).  Reading a colour off basis[0] would therefore look
    perfectly healthy and be wrong; the table must record None instead.
    """
    sites = (0, 1, 2, 3)
    blocks = zero_blocks(sites)
    set_cell(blocks, 0, 1, 0, 0, 1)
    census = kernel_dimension_census(blocks, sites)
    require(
        any(int(key) > 1 for key in census),
        "multi-dimensional kernel probe produced no kernel of dimension > 1, "
        "so essential_table's multi-kernel branch stays untested",
    )
    table = essential_table(blocks, sites)
    multi = 0
    for u, v in combinations(sorted(sites), 2):
        for x, y in ((u, v), (v, u)):
            basis = essential_covectors(blocks, sites, x, y)
            if len(basis) <= 1:
                continue
            multi += 1
            singles = [
                c for phi in basis for c in COLORS
                if phi[c] != 0 and sum(1 for d in COLORS if phi[d] != 0) == 1
            ]
            require(
                singles,
                "probe: expected single-coloured basis covectors, which is "
                "what makes the unsafe reading tempting",
            )
            require(
                table[x][y] is None,
                "essential_table read a colour off a multi-dimensional "
                "kernel: a covector basis is not a canonical colour",
            )
    return {
        "kernel_dimensions": census,
        "multi_dimensional_stars": multi,
        "table_sha256": content_hash(
            {"%d-%d" % (x, y): table[x][y]
             for x in table for y in table[x]}
        ),
    }


def check_endpoint_order_convention():
    """Pin the endpoint-ordered convention, including contract()'s use of it.

    `oriented` and `contract` are the two places where endpoint order is
    consumed.  Both packets that carry off-diagonal cells happen not to
    expose the difference through their essential covectors, so without
    this probe `contract`'s transpose path is dead code: replacing
    `oriented(blocks, u, x)` by the raw `blocks[edge(u, x)]` would change
    nothing anyone checks.  Here an explicitly asymmetric block is
    contracted from BOTH endpoints and the two answers are required to
    be the transposed pair -- and to differ, so the check is not vacuous.
    """
    sites = (0, 1)
    blocks = zero_blocks(sites)
    set_cell(blocks, 0, 1, 0, 2, 3)
    set_cell(blocks, 0, 1, 1, 1, 5)
    raw = blocks[(0, 1)]
    require(
        oriented(blocks, 0, 1) == raw,
        "endpoint order: oriented(u, v) with u < v must be the stored block",
    )
    require(
        oriented(blocks, 1, 0) == transpose(raw),
        "endpoint order: oriented(v, u) with u < v must be the transpose",
    )
    phi = (Fraction(1), Fraction(0), Fraction(0))
    forward = contract(blocks, 0, 1, phi)
    backward = contract(blocks, 1, 0, phi)
    expected_forward = tuple(raw[0][j] for j in COLORS)
    expected_backward = tuple(raw[j][0] for j in COLORS)
    require(
        forward == expected_forward,
        "endpoint order: contract at the left endpoint did not read the "
        "u-mode row of A_uv",
    )
    require(
        backward == expected_backward,
        "endpoint order: contract at the right endpoint did not read the "
        "u-mode row of A_vu = A_uv^T -- contract must go through oriented()",
    )
    require(
        forward != backward,
        "endpoint order probe is vacuous: the two contractions agree, so it "
        "cannot detect a dropped transpose",
    )
    return {
        "forward": [str(value) for value in forward],
        "backward": [str(value) for value in backward],
        "asymmetric": forward != backward,
    }


def check_structure_lemma_on_exact(blocks, sites, label):
    """(*), (E1), (E2), (E3) at every essential ordered pair of an exact A."""
    defects = exactness_defects(blocks, sites)
    require(
        not defects,
        "structure lemma applied to a packet that is not exact: %s" % label,
    )
    records = []
    for u, v in combinations(sorted(sites), 2):
        for x, y in ((u, v), (v, u)):
            for phi in essential_covectors(blocks, sites, x, y):
                require(
                    star_identity_holds(blocks, sites, x, y, phi),
                    "identity (*) failed on the exact packet %s" % label,
                )
                support = [c for c in COLORS if phi[c] != 0]
                require(
                    len(support) == 1,
                    "(E0) kernel covector is not supported on one colour",
                )
                a = support[0]
                for other in sorted(sites):
                    if other in (x, y):
                        continue
                    require(
                        all(entry == 0 for entry in oriented(blocks, x, other)[a]),
                        "(E1) failed: essential row does not vanish off the pair",
                    )
                row = oriented(blocks, x, y)[a]
                lam = row[a]
                require(lam != 0, "(E2) failed: lambda = 0 on the direct block")
                require(
                    all(row[j] == 0 for j in COLORS if j != a),
                    "(E2) failed: direct row is not proportional to e_a",
                )
                rest = tuple(s for s in sorted(sites) if s not in (x, y))
                tensor = matching_tensor(blocks, rest)
                require(
                    tensor == {tuple([a] * len(rest)): Fraction(1) / lam},
                    "(E3) failed: deleted-pair tensor is not the pure "
                    "lambda^{-1} e_a tensor",
                )
                records.append((x, y, a, str(lam)))
    return records


def check_colour_injectivity(records, label):
    """Distinct essential neighbours of a site carry distinct colours."""
    by_site = {}
    for x, y, a, _ in records:
        by_site.setdefault(x, {})[y] = a
    for site, neighbours in by_site.items():
        colours = list(neighbours.values())
        require(
            len(set(colours)) == len(colours),
            "colour injectivity failed on %s: two essential neighbours "
            "shared a colour" % label,
        )
        require(
            len(neighbours) <= 3,
            "a site had more than three essential neighbours on %s" % label,
        )
    return {str(site): sorted(by_site[site].items()) for site in sorted(by_site)}


def check_disjoint_rigidity(blocks, sites, table, label):
    """Disjoint bad pairs of distinct essential colours force H_{B\\4} = 0."""
    colour_of = {}
    for x, neighbours in table.items():
        for y, a in neighbours.items():
            if a is not None:
                colour_of[frozenset((x, y))] = a
    same_colour = 0
    forced_zero = 0
    for left, right in combinations(sorted(colour_of, key=sorted), 2):
        if left & right:
            continue
        rest = tuple(s for s in sorted(sites) if s not in (left | right))
        tensor = matching_tensor(blocks, rest)
        if colour_of[left] == colour_of[right]:
            same_colour += 1
            continue
        require(
            not tensor,
            "disjoint-bad-pair rigidity failed on %s: distinct colours but "
            "H_{B minus four} != 0" % label,
        )
        forced_zero += 1
    return same_colour, forced_zero


# ----------------------------- section 4: crossing pairs and the counting


def check_crossing_facts(blocks, sites, label):
    """The proposition a != chi_u and the #bad <= 2N counting bound."""
    table = essential_table(blocks, sites)
    good = good_pairs(blocks, sites)
    report = []
    c2_instances = 0
    for split in live_splits(blocks, sites):
        part = part_map(split)
        crossing = crossing_pairs(split)
        sizes = [len(split[c]) for c in COLORS]
        expected = (
            sizes[0] * sizes[1] + sizes[0] * sizes[2] + sizes[1] * sizes[2]
        )
        require(
            len(crossing) == expected,
            "crossing count != |S_0||S_1| + |S_0||S_2| + |S_1||S_2| on %s"
            % label,
        )
        bad = crossing - good
        degree = {site: 0 for site in sites}
        for u, v in bad:
            for x, y in ((u, v), (v, u)):
                a = table[x].get(y)
                if a is None:
                    continue
                require(
                    a != part[x],
                    "proposition failed on %s: essential colour equals the "
                    "endpoint's own part colour" % label,
                )
                c2_instances += 1
                degree[x] += 1
        worst = max(degree.values())
        require(
            worst <= 2,
            "a site had more than two crossing essential neighbours on %s"
            % label,
        )
        require(
            len(bad) <= 2 * len(sites),
            "bad crossing pairs exceeded the 2N bound on %s" % label,
        )
        require(
            len(crossing) - len(bad) >= expected - 2 * len(sites),
            "the #good >= X - 2N counting bound failed on %s" % label,
        )
        report.append({
            "split": [list(part) for part in split],
            "crossing": len(crossing),
            "bad_crossing": len(bad),
            "X": expected,
            "two_N": 2 * len(sites),
            "max_crossing_essential_degree": worst,
        })
    # C2 and C4 are VACUOUS on a packet with no bad crossing pair: the
    # requires above then read 0 <= 2N and X - 0 >= X - 2N.  The count is
    # reported so the ledger shows where they carry content.
    return {"splits": report, "c2_instances": c2_instances}


def failing_shapes(max_order):
    """Even split shapes with X = ab+ac+bc <= 2N: where counting alone dies."""
    table = []
    for order in range(6, max_order + 1, 2):
        failing = []
        for first in range(0, order + 1, 2):
            for second in range(first, order - first + 1, 2):
                third = order - first - second
                if third < second or third % 2:
                    continue
                if third == order:
                    continue
                value = first * second + first * third + second * third
                if value <= 2 * order:
                    failing.append([first, second, third, value])
        table.append([order, failing])
    return table


def check_shape_claim(max_order):
    """For even N >= 10 the only failing shape is (0, 2, N-2), X = 2N-4.

    Hand proof (note, section 6).  Let a <= b <= c be even with
    a + b + c = N and c != N.
      * a >= 2:  X - 2N = a(b-2) + b(c-2) + c(a-2) >= 0, with equality
        only when a = b = c = 2, i.e. N = 6.  So X > 2N for N >= 8.
      * a = 0:   c != N forces b >= 2, and X = b(N-b) is increasing on
        [2, N/2].  b = 2 gives X = 2N-4 <= 2N (the surviving shape);
        b = 4 gives X = 4N-16 > 2N exactly when N > 8.
    This function re-verifies the conclusion by exhaustion up to
    `max_order` -- it does not replace the proof, it guards it.
    """
    for order, failing in failing_shapes(max_order):
        if order < 10:
            continue
        if failing != [[0, 2, order - 2, 2 * order - 4]]:
            return False
    return True


# ------------------------------------------------- section 5: the guards


def section_omega_guard():
    sites, blocks, names = omega_guard_packet()
    record = {"names": list(names)}
    anchors = [str(hafnian(blocks, colour, sites)) for colour in COLORS]
    require(
        all(value == "1" for value in anchors),
        "omega guard: a pure anchor haf(W_c[B]) is not 1",
    )
    record["anchors"] = anchors
    defects = exactness_defects(blocks, sites)
    non_constant = {
        word: value for word, value in defects.items() if len(set(word)) > 1
    }
    require(
        len(non_constant) == len(defects),
        "omega guard: a constant-word equation is violated",
    )
    record["defect_count"] = len(defects)
    record["defect_sha256"] = content_hash(
        {str(word): [str(got), str(want)]
         for word, (got, want) in defects.items()}
    )
    part_a = tuple(sorted(names.index(n) for n in ("p", "a", "c", "d")))
    part_b = tuple(sorted(names.index(n) for n in ("q", "b", "r", "s")))
    for word in defects:
        classes = {}
        for site, colour in enumerate(word):
            classes.setdefault(colour, set()).add(site)
        shape = sorted(tuple(sorted(part)) for part in classes.values())
        require(
            shape == sorted([part_a, part_b]),
            "omega guard: a violation is not from the pacd|qbrs bipartition",
        )
    good = good_pairs(blocks, sites)
    record["good_pairs"] = len(good)
    record["total_pairs"] = len(list(combinations(sites, 2)))
    lives = live_splits(blocks, sites)
    record["live_splits"] = len(lives)
    unordered = {
        frozenset(frozenset(part) for part in split if part) for split in lives
    }
    record["live_splits_up_to_order"] = len(unordered)
    crossing_matching_counts = []
    for split in lives:
        word = dict(zip(sorted(sites), split_word(split, sites)))
        value = coefficient(blocks, sites, word)
        product_part = split_product(blocks, split)
        terms = crossing_matchings_terms(blocks, sites, split)
        crossing_sum = sum((term for _, _, term in terms), Fraction(0))
        require(
            value == product_part + crossing_sum,
            "omega guard: Theorem A identity failed",
        )
        require(
            crossing_pairs(split) == good,
            "omega guard: the crossing graph is not the good-pair graph",
        )
        crossing_matching_counts.append(len(terms))
    record["nonzero_crossing_matchings"] = sorted(set(crossing_matching_counts))
    record["crossing_graph_equals_good_graph"] = bool(lives) and all(
        crossing_pairs(split) == good for split in lives
    )
    require(
        record["crossing_graph_equals_good_graph"],
        "omega guard: the crossing graph is not the good-pair graph",
    )
    live_words = {split_word(split, sites) for split in lives}
    record["live_words_are_the_defects"] = live_words == set(defects)
    require(
        record["live_words_are_the_defects"],
        "omega guard: the live-split words are not the violated words",
    )
    tally, detail = structure_census(blocks, sites)
    record["essential_kernel_basis_covectors"] = tally["covectors"]
    record["kernel_dimensions"] = kernel_dimension_census(blocks, sites)
    record["structure_tally"] = tally
    record["structure_detail_sha256"] = content_hash(detail)
    # The precise negative statement: single-colouredness, (E1) and (E2)
    # DO hold at every essential ordered pair of this packet; identity
    # (*) and (E3) fail at every one of them.  So what the packet's
    # satisfied rows fail to imply is specifically (E3).
    record["single_colour_holds_everywhere"] = (
        tally["covectors"] > 0
        and tally["single_colour"] == tally["covectors"]
    )
    record["E1_holds_everywhere"] = tally["E1"] == tally["covectors"]
    record["E2_holds_everywhere"] = tally["E2"] == tally["covectors"]
    record["E3_fails_everywhere"] = tally["E3"] == 0
    record["star_identity_fails_everywhere"] = tally["star"] == 0
    require(
        record["single_colour_holds_everywhere"]
        and record["E1_holds_everywhere"]
        and record["E2_holds_everywhere"],
        "omega guard: single-colouredness, (E1) or (E2) already fails, so "
        "the packet would not isolate (E3)",
    )
    negatives = (
        record["E3_fails_everywhere"]
        and record["star_identity_fails_everywhere"]
    )
    require(
        negatives,
        "omega guard: identity (*) or (E3) did not fail at every essential "
        "pair -- (E3) would then follow from the guard's satisfied rows",
    )
    crossing = check_crossing_facts(blocks, sites, "omega guard")
    record["crossing_report"] = crossing["splits"]
    record["c2_instances"] = crossing["c2_instances"]
    # C2 and C4 are vacuous here: the crossing graph equals the good-pair
    # graph, so there is no bad crossing pair to test them on.
    record["c2_c4_vacuous"] = crossing["c2_instances"] == 0
    require(
        record["c2_c4_vacuous"],
        "omega guard: expected zero bad crossing pairs (C2/C4 vacuous here); "
        "if this fires the guard's good-pair graph has changed",
    )
    record["blocks_sha256"] = content_hash(block_image(blocks))
    return sites, blocks, record


def solve_six_site_guard():
    """Solve the live-split colouring equation H_B(chi) = 0 exactly in s."""
    word = dict(zip(SIX_SITE_SITES, split_word(SIX_SITE_SPLIT, SIX_SITE_SITES)))
    at_zero = coefficient(
        six_site_guard_packet(Fraction(1), Fraction(0)), SIX_SITE_SITES, word
    )
    at_one = coefficient(
        six_site_guard_packet(Fraction(1), Fraction(1)), SIX_SITE_SITES, word
    )
    slope = at_one - at_zero
    require(
        slope != 0,
        "six-site guard: the split coefficient does not depend on the second "
        "off-diagonal cell",
    )
    second = -at_zero / slope
    return Fraction(1), second


def section_six_site_guard():
    first, second = solve_six_site_guard()
    blocks = six_site_guard_packet(first, second)
    sites = SIX_SITE_SITES
    record = {"cell_A03_0_2": str(first), "cell_A15_0_2": str(second)}
    require(
        second.denominator == 1,
        "six-site guard: the solved off-diagonal cell is not an integer",
    )
    anchors = [str(hafnian(blocks, colour, sites)) for colour in COLORS]
    require(
        all(value == "1" for value in anchors),
        "six-site guard: a pure anchor haf(W_c[B]) is not 1",
    )
    record["anchors"] = anchors

    defects = exactness_defects(blocks, sites)
    total_words = 3 ** len(sites)
    record["total_words"] = total_words
    record["satisfied_equations"] = total_words - len(defects)
    record["defect_count"] = len(defects)
    record["defects"] = sorted(
        ["".join(str(c) for c in word) + ":" + str(got)
         for word, (got, _) in defects.items()]
    )
    record["all_defects_non_constant"] = all(
        len(set(word)) > 1 for word in defects
    )
    require(
        record["all_defects_non_constant"],
        "six-site guard: a constant-word equation is violated",
    )
    require(
        defects,
        "six-site guard: the packet is exact -- that would contradict "
        "Theorem 1.1 of proofs/six-site-arbitrary-complex-obstruction.md "
        "(no complex block family realizes Delta_{6,3}).  The diagonal "
        "hafnian recurrence obstruction is NOT the right citation here: "
        "this packet has off-diagonal cells and a live split, so it falls "
        "outside that note's hypotheses",
    )

    lives = live_splits(blocks, sites)
    record["live_splits"] = len(lives)
    require(
        len(lives) == 1,
        "six-site guard: the live split is not unique",
    )
    split = lives[0]
    require(
        split == SIX_SITE_SPLIT,
        "six-site guard: the live split is not the designed one",
    )
    part = part_map(split)
    good = good_pairs(blocks, sites)
    record["good_pairs"] = sorted("%d-%d" % pair for pair in good)

    word = dict(zip(sorted(sites), split_word(split, sites)))
    value = coefficient(blocks, sites, word)
    product_part = split_product(blocks, split)
    terms = crossing_matchings_terms(blocks, sites, split)
    crossing_sum = sum((term for _, _, term in terms), Fraction(0))
    require(
        value == product_part + crossing_sum,
        "six-site guard: Theorem A identity failed",
    )
    require(
        value == 0,
        "six-site guard: the live split violates its colouring equation",
    )
    require(
        product_part != 0,
        "six-site guard: the live split product vanished",
    )
    record["split_product"] = str(product_part)
    record["crossing_sum"] = str(crossing_sum)
    record["nonzero_crossing_matchings"] = len(terms)
    record["min_crossing_edges"] = min(len(edges) for _, edges, _ in terms)
    require(
        record["min_crossing_edges"] >= 2,
        "six-site guard: a nonzero crossing matching had fewer than two "
        "crossing edges (parity fact violated)",
    )

    forced = sorted({e for _, edges, _ in terms for e in edges})
    record["forced_crossing_cells"] = [
        "A_%d%d(%d,%d)" % (u, v, part[u], part[v]) for u, v in forced
    ]
    record["forced_cells_all_bad"] = all(pair not in good for pair in forced)
    require(
        record["forced_cells_all_bad"],
        "six-site guard: a forced crossing cell sits on a good pair -- the "
        "weak crossing-pairs-are-good lemma would survive",
    )
    require(
        sorted(forced) == sorted(SIX_SITE_CARRIERS),
        "six-site guard: the forced crossing cells are not the two carriers",
    )

    crossing = crossing_pairs(split)
    bad = sorted(crossing - good)
    record["crossing_pairs"] = len(crossing)
    record["bad_crossing_pairs"] = ["%d-%d" % pair for pair in bad]
    table = essential_table(blocks, sites)
    witnesses = []
    for u, v in bad:
        for x, y in ((u, v), (v, u)):
            a = table[x].get(y)
            require(
                a is not None,
                "six-site guard: a bad crossing endpoint has no single-colour "
                "essential covector",
            )
            require(
                a != part[x],
                "six-site guard: the proved proposition a != chi_u failed",
            )
            witnesses.append([x, y, a, part[x], part[y]])
    record["essential_witnesses"] = witnesses
    record["essential_colour_is_third_colour"] = all(
        row[2] not in (row[3], row[4]) for row in witnesses
    )

    e3_status = {}
    for u, v in bad:
        for x, y in ((u, v), (v, u)):
            for phi in essential_covectors(blocks, sites, x, y):
                single, _, e1, e2, e3 = structure_status(
                    blocks, sites, x, y, phi
                )
                require(
                    single,
                    "six-site guard: kernel covector is not single-colour",
                )
                e3_status[edge(x, y)] = (e1, e2, e3)
    record["E1_holds_on_all_bad_crossing_pairs"] = all(
        status[0] for status in e3_status.values()
    )
    record["E2_holds_on_all_bad_crossing_pairs"] = all(
        status[1] for status in e3_status.values()
    )
    e3_failures = sorted(
        pair for pair, status in e3_status.items() if not status[2]
    )
    record["E3_failing_pairs"] = ["%d-%d" % pair for pair in e3_failures]
    record["E3_fails_exactly_on_the_carriers"] = (
        e3_failures == sorted(SIX_SITE_CARRIERS)
    )
    require(
        record["E1_holds_on_all_bad_crossing_pairs"]
        and record["E2_holds_on_all_bad_crossing_pairs"],
        "six-site guard: (E1) or (E2) already fails, so the guard would not "
        "isolate (E3)",
    )
    require(
        record["E3_fails_exactly_on_the_carriers"],
        "six-site guard: (E3) does not fail exactly at the two pairs carrying "
        "the forced cells",
    )

    same_colour, forced_zero = check_disjoint_rigidity(
        blocks, sites, table, "six-site guard"
    )
    record["disjoint_same_colour"] = same_colour
    record["disjoint_distinct_colour_forced_zero"] = forced_zero
    crossing_facts = check_crossing_facts(blocks, sites, "six-site guard")
    record["crossing_report"] = crossing_facts["splits"]
    record["c2_instances"] = crossing_facts["c2_instances"]
    require(
        record["c2_instances"] > 0,
        "six-site guard: C2 was not exercised here either -- with the omega "
        "guard vacuous, the proposition would then be untested",
    )

    # Identity (*) on this packet.  Unlike both symmetric packets above,
    # this one has genuinely off-diagonal cells, so evaluating (*) here
    # exercises the transpose branch of oriented() inside contract().
    # (*) is a consequence of exactness, and this packet is not exact, so
    # it must fail somewhere; recording WHERE is a guard fact.
    tally, detail = structure_census(blocks, sites)
    record["essential_kernel_basis_covectors"] = tally["covectors"]
    record["kernel_dimensions"] = kernel_dimension_census(blocks, sites)
    record["structure_tally"] = tally
    record["structure_detail_sha256"] = content_hash(detail)
    record["star_identity_failures"] = tally["covectors"] - tally["star"]
    record["star_identity_fails_somewhere"] = tally["star"] < tally["covectors"]
    require(
        record["star_identity_fails_somewhere"],
        "six-site guard: identity (*) held at every essential pair, but the "
        "packet is not exact -- (*) is an exactness consequence",
    )
    star_fail_pairs = sorted(
        {key.split("#")[0] for key, value in detail.items() if not value[0]}
    )
    record["star_identity_failing_ordered_pairs"] = star_fail_pairs
    record["blocks_sha256"] = content_hash(block_image(blocks))
    return sites, blocks, record


# ------------------------------------------------------------------ main


def audit():
    convention = check_endpoint_order_convention()
    kernel_probe = check_multidimensional_kernel_probe()
    identities = section_identities()

    k4_sites, k4_blocks = k4_one_factorization_packet()
    k4_defects = exactness_defects(k4_blocks, k4_sites)
    require(
        not k4_defects,
        "the K_4 one-factorization packet is not an exact ternary source",
    )
    k4_records = check_structure_lemma_on_exact(k4_blocks, k4_sites, "K_4")
    k4_injectivity = check_colour_injectivity(k4_records, "K_4")
    k4_table = essential_table(k4_blocks, k4_sites)
    k4_same, k4_forced = check_disjoint_rigidity(
        k4_blocks, k4_sites, k4_table, "K_4"
    )
    k4_lives = live_splits(k4_blocks, k4_sites)
    k4_good = good_pairs(k4_blocks, k4_sites)
    k4 = {
        "blocks_sha256": content_hash(block_image(k4_blocks)),
        "tensor_sha256": content_hash(
            {str(word): str(value)
             for word, value in matching_tensor(k4_blocks, k4_sites).items()}
        ),
        "exactness_defects": len(k4_defects),
        # One entry per BASIS covector of ker sigma_u^(v), not per pair:
        # single-colouredness is a property of basis covectors, and the
        # kernel dimension census below records that every kernel here is
        # in fact one-dimensional.
        "essential_kernel_basis_covectors": len(k4_records),
        "kernel_dimensions": kernel_dimension_census(k4_blocks, k4_sites),
        "essential_table_sha256": content_hash(k4_injectivity),
        "live_splits": len(k4_lives),
        "good_pairs": len(k4_good),
        "disjoint_same_colour_pairs": k4_same,
        "disjoint_distinct_colour_pairs": k4_forced,
        "structure_lemma_verified": len(k4_records) > 0,
    }
    require(
        k4["essential_kernel_basis_covectors"] == 12,
        "K_4: expected all twelve ordered pairs to be essential",
    )
    require(
        list(k4["kernel_dimensions"]) == ["1"],
        "K_4: expected every deleted endpoint star to have a one-dimensional "
        "kernel",
    )
    require(
        not k4_lives,
        "K_4: expected no live split (its N=4 order is outside {6,8,10})",
    )
    require(
        not k4_good,
        "K_4: expected every pair to be bad",
    )
    require(
        k4_forced == 0 and k4_same > 0,
        "K_4: disjoint bad pairs must share their essential colour, since "
        "H_empty = 1 is nonzero",
    )

    omega_sites, omega_blocks, omega = section_omega_guard()
    six_sites, six_blocks, six = section_six_site_guard()

    shadow_packets = [
        ("K_4 exact source", k4_sites, k4_blocks),
        ("omega guard", omega_sites, omega_blocks),
        ("six-site guard", six_sites, six_blocks),
    ]
    shadow, shadow_units = section_boolean_shadow(shadow_packets)
    require(
        all(shadow_units["K_4 exact source"]),
        "Boolean shadow: Lemma 0's units z_c(B) = 1 failed on the exact "
        "K_4 source",
    )
    require(
        all(shadow_units["omega guard"]) and all(shadow_units["six-site guard"]),
        "Boolean shadow: the guards' anchors do not give the units z_c(B) = 1",
    )

    shapes = failing_shapes(24)
    shape_claim_max_order = 200
    shape_claim = check_shape_claim(shape_claim_max_order)
    require(
        shape_claim,
        "failing-shape claim broken: some even N >= 10 has a shape other "
        "than (0, 2, N-2) with X <= 2N",
    )

    ledger = {
        "convention": (
            "endpoint-ordered blocks, oriented()/perfect_matchings/"
            "matching_tensor copied from computations/"
            "verify_target_flattening_essential_star_pair_bound.py; a pair is "
            "good iff both deleted endpoint stars sigma_u^(v), sigma_v^(u) "
            "are injective (notes/target-flattening-essential-star-pair-"
            "bound.md eq. (2))"
        ),
        "endpoint_order_probe": convention,
        "multidimensional_kernel_probe": kernel_probe,
        "identities": identities,
        "boolean_shadow": shadow,
        "boolean_shadow_units": {
            label: list(values) for label, values in sorted(shadow_units.items())
        },
        "k4_exact_source": k4,
        "omega_guard": omega,
        "six_site_guard": six,
        "failing_shape_table": shapes,
        "failing_shape_sha256": content_hash(shapes),
        "failing_shape_claim_max_order": shape_claim_max_order,
        "failing_shape_claim_only_0_2_Nminus2": shape_claim,
        "sat_input_cited_not_rerun": (
            "proofs/diagonal-hafnian-recurrence-obstruction.md, Theorem (3): "
            "the Boolean system {units z_c(V)=1, recurrence (5)-(7), split "
            "clauses (8)} is UNSAT for n in {6,8,10}; this checker verifies "
            "only that the hafnian shadow of each tested block family is a "
            "model of (5)-(7) and that Lemma 0 supplies the units.  "
            "Separately, proofs/six-site-arbitrary-complex-obstruction.md "
            "Theorem 1.1 rules out ANY complex block family with "
            "H_6(A) = Delta_{6,3}, unconditionally; so Theorem B of the note "
            "is VACUOUS at N=6 and carries content only at N=8 and N=10"
        ),
        "proved_by_hand_verified_here_on_instances": (
            "Lemma 0, Theorem A and the parity fact are identities.  They "
            "are verified on 243 matching-supported degree-two monomial "
            "packets at N=4 (single-cell packets would be vacuous: both "
            "sides are degree-two multilinear there) and on pseudorandom "
            "packets at N=4,6,8, with nonvacuous-equation counts recorded; "
            "parity exhaustively at N=4,6.  The essentiality structure "
            "lemma (*), (E1)-(E3), colour injectivity and the disjoint-bad-"
            "pair rigidity are hand proofs verified here on the exact K_4 "
            "source.  C2 (a != chi_u) and C4 (#good >= X - 2N) concern live "
            "splits and are VACUOUS on the omega guard (zero bad crossing "
            "pairs); they are exercised only on the six-site guard.  The "
            "universal quantifier over exact sources is NOT machine-verified"
        ),
        "conjectured_not_proved": (
            "the full crossing-pairs-are-good lemma (every cell forced by "
            "Theorem A on a live split sits on a good pair) is CONJECTURED; "
            "its weak form -- forced by pure anchors plus the live-split "
            "colouring equations alone -- is REFUTED by the six-site guard "
            "here, which satisfies 727 of the 729 exactness equations"
        ),
        "scope": (
            "live-split existence is available only at N in {6,8,10}, and is "
            "vacuous at N=6 where non-existence is already unconditional; "
            "uniformity in N is open.  The structure lemma is proved for "
            "exact sources but machine-checked only on instances, and the "
            "only exact instance available is K_4 at N=4, which has no live "
            "split, so C2 and C4 are checked only on a non-exact guard.  The "
            "label-split application still needs the goodness of a forced "
            "crossing cell, not merely its existence.  Krenn's conjecture "
            "remains open"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(
            digest == EXPECTED_LEDGER_SHA256,
            "exact-source live-split forcing ledger changed",
        )
    return ledger, digest


def main():
    ledger, digest = audit()
    identities = ledger["identities"]
    print("exact-source live-split forcing: PASS (exact)")
    print("Lemma 0 / Theorem A identities: %d matching-supported monomial "
          "packets at N=4 (%d nonvacuous Theorem A equations, %d nonvacuous "
          "Lemma 0 equations)"
          % (identities["monomial_packets_N4"],
             identities["monomial_theoremA_nonvacuous"],
             identities["monomial_lemma0_nonvacuous"]))
    print("  pseudorandom packets: %d/%d/%d even splits at N=4/6/8, "
          "%d/%d/%d nonvacuous Theorem A equations"
          % (identities["even_splits_N4"],
             identities["even_splits_N6"],
             identities["even_splits_N8"],
             identities["random_theoremA_nonvacuous_N4"],
             identities["random_theoremA_nonvacuous_N6"],
             identities["random_theoremA_nonvacuous_N8"]))
    print("parity fact exhaustive: %d (split, matching) pairs at N=4, "
          "%d at N=6"
          % (identities["parity_pairs_N4"], identities["parity_pairs_N6"]))
    print("Boolean recurrence shadow: %d pivot constraints over %d packets"
          % (ledger["boolean_shadow"]["checks"],
             ledger["boolean_shadow"]["packets"]))
    k4 = ledger["k4_exact_source"]
    print("exact K_4 source: %d defects, %d essential kernel basis covectors "
          "(dims %s), (*),(E1)-(E3) verified, %d disjoint same-colour pairs"
          % (k4["exactness_defects"],
             k4["essential_kernel_basis_covectors"],
             k4["kernel_dimensions"],
             k4["disjoint_same_colour_pairs"]))
    omega = ledger["omega_guard"]
    print("omega guard: %d good pairs of %d, %d live splits (%d up to order); "
          "of %d essential covectors, single-colour/E1/E2 hold at all, "
          "(*) and E3 at none; C2/C4 vacuous (%d instances)"
          % (omega["good_pairs"], omega["total_pairs"], omega["live_splits"],
             omega["live_splits_up_to_order"],
             omega["essential_kernel_basis_covectors"],
             omega["c2_instances"]))
    six = ledger["six_site_guard"]
    print("six-site guard: A_03(0,2) = %s, A_15(0,2) = %s; %d of %d equations"
          % (six["cell_A03_0_2"], six["cell_A15_0_2"],
             six["satisfied_equations"], six["total_words"]))
    print("  forced cells %s all on BAD pairs: %s; (E3) fails exactly at %s"
          % (six["forced_crossing_cells"], six["forced_cells_all_bad"],
             six["E3_failing_pairs"]))
    print("  C2 exercised on %d ordered bad-crossing endpoints; identity (*) "
          "fails at %d of %d essential covectors"
          % (six["c2_instances"], six["star_identity_failures"],
             six["essential_kernel_basis_covectors"]))
    print("failing-shape claim ((0,2,N-2) only, even N >= 10) verified to "
          "N = %d: %s"
          % (ledger["failing_shape_claim_max_order"],
             ledger["failing_shape_claim_only_0_2_Nminus2"]))
    print("endpoint-order probe: contract left %s / right %s (asymmetric: %s); "
          "multi-kernel probe: %d stars of dimension > 1, all recorded as None"
          % (ledger["endpoint_order_probe"]["forward"],
             ledger["endpoint_order_probe"]["backward"],
             ledger["endpoint_order_probe"]["asymmetric"],
             ledger["multidimensional_kernel_probe"]
                   ["multi_dimensional_stars"]))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
