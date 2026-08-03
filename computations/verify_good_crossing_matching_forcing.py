#!/usr/bin/env python3
"""Theorem C: the deletion identity with a saturating correction, and the
good-crossing-matching consequences.

Companion note: `notes/good-crossing-matching-forcing.md` (hand proofs).
Committed companion of the same cluster:
`notes/exact-source-live-split-forcing.md` with checker
`computations/verify_exact_source_live_split_forcing.py`, from which ALL
conventions and all machinery are imported verbatim (endpoint-ordered
blocks A_uv, `oriented`, `perfect_matchings`, `matching_tensor`, the
deleted endpoint star sigma_u^(v), and "good pair" = both stars
injective).  Nothing is re-implemented, so the two artifacts cannot
drift apart; a conventions probe below checks that the imported symbols
really are the endpoint-ordered ones.

What is established here, and at which strength:

  S1  THE DELETION IDENTITY (a polynomial identity in the block entries,
      proved by hand in the note).  For any block family, any edge set F
      and any word w,

        sum_{M in PM(B), M cap F = empty} prod_{uv in M} A_uv(w_u,w_v)
          = sum_{T subset F, T a matching}
              (-1)^{|T|} (prod_{e in T} A_e(w)) H_{B \\ V(T)}(w).

      Verified on 196 pseudorandom instances at N = 4, 6, 8.  The
      checker counts NONVACUOUS instances (nonzero common value) and
      instances whose T != empty correction is nonzero, and refuses to
      pass if either count is zero -- an identity checked only where
      both sides read 0 == 0 verifies nothing.

  S2  LEMMA F (multi-deletion purity chain), hand-proved in the note,
      verified on instances in BOTH branches:
        * same colour: 26 (packet, sub-family) instances carrying two
          and three disjoint (E1)/(E2)/(E3) pairs at N = 6, 8; the
          residue must be a pure colour-a tensor with the predicted
          nonzero coefficient;
        * distinct colours: an eight-site instance carrying (E1)+(E2) at
          two disjoint pairs of DIFFERENT essential colours and (E3) at
          one of them -- exactly the hypotheses the induction uses -- in
          which the forced residue H_{B\\V(T)} = 0 is a genuine
          CANCELLATION (all six residue blocks nonzero, two of the three
          matching terms nonzero), not a block that was zeroed.  A
          falsification probe perturbs one residue cell so that the
          conclusion breaks, and checks that a HYPOTHESIS ((E3)) then
          breaks too.

  S3  LEMMA G (one bad pair per site per colour) and the counting.
      Verified on the exact K_4 three-one-factorization source, where
      the 3N/2 bound is TIGHT (six bad pairs, every site in exactly one
      bad pair of each colour), and as a consistency check on both
      guards (not exact, so they test the code, not the hypothesis).
      The shape census (C4'/C5': the only shape with X <= 3N/2 is
      (0,2,N-2) with N <= 8) is re-verified by exhaustion to N = 200,
      side by side with the committed note's weaker X <= 2N table.

  S4  SATURATING COMBINATORICS.  |T| = 1 never saturates -- exhaustively
      over every ordered even split at N = 4, 6, 8, 10 -- and the
      shape-(0,2,N-2) census (only the big part's colour, only size 2).

  S5  THEOREM C's LEDGER on both guards: the committed 727/729 six-site
      guard (which breaks (E3)) and the new 720/729 stall guard (which
      keeps it).  Every surviving inclusion-exclusion term must be
      explained -- (E3) fails on T, or T is saturating -- and neither
      guard has a nonzero crossing matching all of whose crossing edges
      are good.  Also the single-bad-pair corollary
      sum_{M contains e} = A_e(chi) H_{B\\e}(chi), evaluated at every bad
      crossing pair of both guards.

  S6  THE STALL GUARD itself, built from the note's construction with
      its one free scalar SOLVED (not hard-coded) from the split
      equation.  All of its advertised properties are COMPUTED from its
      blocks: three pure anchors, liveness, the colouring equation,
      (E1)+(E2)+(E3) and badness at both bad crossing pairs, the 720/729
      exactness count, the Theorem C ledger with a single surviving
      saturating term of value +1 against -h_0h_1h_2 = -1, the scalar
      identity behind it, and the absence of a good-only crossing
      matching.

  This is a GUARD, not an exact source: no exact ternary source exists
  at N = 6 at all (`proofs/six-site-arbitrary-complex-obstruction.md`
  Theorem 1.1, cited, not re-run), so the packet cannot be and is not
  claimed to be exact.  Its role is to show that the saturating gap of
  Theorem C is not closable from the anchors, the split equation and
  (E1)-(E3).

Exact stdlib arithmetic only: int and Fraction.  No floats, no numpy, no
third-party imports, no bare asserts.  Krenn's conjecture remains open.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    # `python3 -I` does not prepend the script directory, so the sibling
    # companion module is imported through an explicit, file-relative path.
    sys.path.insert(0, _HERE)

from verify_exact_source_live_split_forcing import (  # noqa: E402
    COLORS,
    EXPECTED_LEDGER_SHA256 as COMPANION_LEDGER_SHA256,
    block_image,
    coefficient,
    content_hash,
    crossing_pairs,
    edge,
    essential_covectors,
    even_splits,
    exactness_defects,
    good_pairs,
    hafnian,
    is_good_pair,
    k4_one_factorization_packet,
    matching_tensor,
    oriented,
    part_map,
    perfect_matchings,
    pseudorandom_stream,
    require,
    set_cell,
    six_site_guard_packet,
    solve_six_site_guard,
    split_product,
    star_injective,
    transpose,
    zero_blocks,
    SIX_SITE_SITES,
    SIX_SITE_SPLIT,
)

EXPECTED_LEDGER_SHA256 = (
    "5d2ba758792054b0ddcf3bdee9dc81235bca91d8c1fe3ab8697db5644501fc73"
)


# ------------------------------------------------- conventions (imported)


def check_imported_conventions():
    """Pin the imported machinery to the endpoint-ordered convention.

    Everything below runs on symbols imported from the committed checker.
    If that import ever resolved to a different module -- or if the
    companion's convention changed -- every result here would silently
    change meaning.  This probe recomputes, from scratch, three facts
    that fix the convention: `oriented(u,v)` is the stored block and
    `oriented(v,u)` its transpose (and the two DIFFER on an asymmetric
    block, so the probe is not vacuous); `matching_tensor` on a two-site
    packet is the block itself; and `is_good_pair` agrees with the
    deleted-endpoint-star definition on a packet with a known bad pair.
    """
    sites = (0, 1)
    blocks = zero_blocks(sites)
    set_cell(blocks, 0, 1, 0, 2, 3)
    set_cell(blocks, 0, 1, 1, 1, 5)
    raw = blocks[(0, 1)]
    require(
        oriented(blocks, 0, 1) == raw,
        "conventions: oriented(u,v) with u < v must be the stored block",
    )
    require(
        oriented(blocks, 1, 0) == transpose(raw),
        "conventions: oriented(v,u) with u < v must be the transpose",
    )
    require(
        oriented(blocks, 0, 1) != oriented(blocks, 1, 0),
        "conventions probe is vacuous: the block is symmetric, so a dropped "
        "transpose could not be detected",
    )
    tensor = matching_tensor(blocks, sites)
    require(
        tensor == {(0, 2): Fraction(3), (1, 1): Fraction(5)},
        "conventions: matching_tensor on a two-site packet is not the block",
    )
    # A four-site packet whose only nonzero block is A_01: the stars of 2
    # and 3 are zero, so every pair is bad; the pair {0,1} is bad because
    # sigma_0^(1) reads only the (zero) blocks A_02, A_03.
    quad = (0, 1, 2, 3)
    probe = zero_blocks(quad)
    set_cell(probe, 0, 1, 0, 0, 1)
    require(
        not is_good_pair(probe, quad, 0, 1),
        "conventions: is_good_pair is not the deleted-endpoint-star notion",
    )
    # Goodness needs BOTH stars.  This packet has sigma_0^(1) injective and
    # sigma_1^(0) NOT injective, so a reading that consults only the first
    # argument's star would call {0,1} good in one argument order.  The
    # positive control differs from it in a single block and must read good,
    # so the probe cannot pass by always answering "bad".
    asymmetric = zero_blocks(quad)
    for colour in COLORS:
        set_cell(asymmetric, 0, 2, colour, colour, 1)
    set_cell(asymmetric, 1, 2, 0, 0, 1)
    control = zero_blocks(quad)
    for colour in COLORS:
        set_cell(control, 0, 2, colour, colour, 1)
        set_cell(control, 1, 2, colour, colour, 1)
    require(
        star_injective(asymmetric, quad, 0, 1),
        "conventions probe is vacuous: the first star of the asymmetric "
        "packet is not injective, so it cannot isolate the second one",
    )
    require(
        not star_injective(asymmetric, quad, 1, 0),
        "conventions probe is vacuous: the second star of the asymmetric "
        "packet is injective too, so a dropped second-star test would be "
        "invisible",
    )
    for x, y in ((0, 1), (1, 0)):
        require(
            not is_good_pair(asymmetric, quad, x, y),
            "conventions: is_good_pair ignored the second deleted endpoint "
            "star -- a pair with one non-injective star was called good",
        )
    require(
        is_good_pair(control, quad, 0, 1)
        and is_good_pair(control, quad, 1, 0),
        "conventions probe is vacuous: the positive control does not read "
        "good, so is_good_pair could be answering 'bad' unconditionally",
    )
    return {
        "oriented_forward": [[str(x) for x in row] for row in raw],
        "oriented_backward": [
            [str(x) for x in row] for row in oriented(blocks, 1, 0)
        ],
        "two_site_tensor": {str(k): str(v) for k, v in tensor.items()},
        "asymmetric_star_ranks": [
            star_injective(asymmetric, quad, 0, 1),
            star_injective(asymmetric, quad, 1, 0),
        ],
        "asymmetric_pair_is_good": is_good_pair(asymmetric, quad, 0, 1),
        "control_pair_is_good": is_good_pair(control, quad, 0, 1),
        "companion_ledger_sha256": COMPANION_LEDGER_SHA256,
    }


# --------------------------------------------------------------- vocabulary


def weight(blocks, matching, word):
    """prod_{uv in M} A_uv(word[u], word[v])."""
    term = Fraction(1)
    for u, v in matching:
        term *= blocks[(u, v)][word[u]][word[v]]
        if term == 0:
            return Fraction(0)
    return term


def sub_tensor_value(blocks, sites, word):
    """H_S(A)(word restricted to S); H_empty = 1."""
    sites = tuple(sorted(sites))
    if not sites:
        return Fraction(1)
    return coefficient(blocks, sites, {s: word[s] for s in sites})


def matchings_inside(edges):
    """Every subset of `edges` that is a matching, the empty one included."""
    edges = sorted(edges)
    out = [()]
    frontier = [((), frozenset())]
    while frontier:
        new = []
        for chosen, used in frontier:
            last = chosen[-1] if chosen else None
            for e in edges:
                if last is not None and e <= last:
                    continue
                if e[0] in used or e[1] in used:
                    continue
                item = (chosen + (e,), used | {e[0], e[1]})
                new.append(item)
                out.append(item[0])
        frontier = new
    return out


def avoiding_sum(blocks, sites, word, forbidden):
    """sum over perfect matchings M of `sites` with M cap forbidden = empty."""
    total = Fraction(0)
    for matching in perfect_matchings(sorted(sites)):
        if any(e in forbidden for e in matching):
            continue
        total += weight(blocks, matching, word)
    return total


def through_sum(blocks, sites, word, e):
    """sum over perfect matchings M containing the edge e."""
    total = Fraction(0)
    for matching in perfect_matchings(sorted(sites)):
        if e not in matching:
            continue
        total += weight(blocks, matching, word)
    return total


def inclusion_exclusion_sum(blocks, sites, word, forbidden):
    """(total, [(T, signed value)]) for the right side of the identity."""
    total = Fraction(0)
    terms = []
    for T in matchings_inside(forbidden):
        covered = {s for e in T for s in e}
        head = Fraction(1)
        for u, v in T:
            head *= blocks[(u, v)][word[u]][word[v]]
        if head == 0:
            value = Fraction(0)
        else:
            rest = tuple(s for s in sorted(sites) if s not in covered)
            value = head * sub_tensor_value(blocks, rest, word)
        sign = -1 if len(T) % 2 else 1
        total += sign * value
        terms.append((T, sign * value))
    return total, terms


def pseudorandom_packet(sites, seed, spread=7):
    nextint = pseudorandom_stream(seed)
    blocks = zero_blocks(sites)
    for u, v in combinations(sorted(sites), 2):
        for i in COLORS:
            for j in COLORS:
                set_cell(blocks, u, v, i, j, nextint(2 * spread + 1) - spread)
    return blocks


# ------------------------------------------------ S1 the deletion identity


def section_deletion_identity():
    """The identity on a pseudorandom instance family at N = 4, 6, 8."""
    record = {}
    instances = []
    checks = 0
    nonvacuous = 0
    with_correction = 0
    single_edge_checks = 0
    single_edge_nonvacuous = 0
    per_order = {}
    for order, seeds in ((4, (11, 12, 13)), (6, (21, 22)), (8, (31,))):
        sites = tuple(range(order))
        all_edges = [edge(u, v) for u, v in combinations(sites, 2)]
        order_nonvacuous = 0
        for seed in seeds:
            blocks = pseudorandom_packet(sites, seed)
            nextint = pseudorandom_stream(seed + 500)
            budget = 2 if order == 8 else 4
            forbidden_sets = [frozenset()]
            for _ in range(budget):
                forbidden_sets.append(
                    frozenset(e for e in all_edges if nextint(3) == 0)
                )
            forbidden_sets.append(frozenset(all_edges))
            words = []
            for _ in range(budget):
                words.append({s: nextint(3) for s in sites})
            for split in list(even_splits(sites))[:2]:
                words.append(part_map(split))
            for forbidden in forbidden_sets:
                for word in words:
                    left = avoiding_sum(blocks, sites, word, forbidden)
                    right, terms = inclusion_exclusion_sum(
                        blocks, sites, word, forbidden
                    )
                    require(
                        left == right,
                        "deletion identity failed: the F-avoiding matching sum "
                        "differs from the signed T-family sum (N=%d, seed=%d)"
                        % (order, seed),
                    )
                    correction = sum(
                        (value for T, value in terms if T), Fraction(0)
                    )
                    checks += 1
                    if left != 0:
                        nonvacuous += 1
                        order_nonvacuous += 1
                    if correction != 0:
                        with_correction += 1
                    instances.append([
                        order, seed, sorted(forbidden),
                        [word[s] for s in sites], str(left), str(correction),
                    ])
            # The |T| = 1 specialisation used by the unconditional
            # corollary: sum over matchings THROUGH e equals
            # A_e(w) H_{B \ e}(w).  Same identity with F = {e}, but it is
            # the shape the corollary consumes, so it is checked directly.
            for e in all_edges[:4]:
                for word in words[:2]:
                    left = through_sum(blocks, sites, word, e)
                    rest = tuple(s for s in sites if s not in e)
                    right = (
                        blocks[e][word[e[0]]][word[e[1]]]
                        * sub_tensor_value(blocks, rest, word)
                    )
                    require(
                        left == right,
                        "single-edge deletion identity failed: the sum through "
                        "an edge differs from A_e(w) H_{B minus e}(w)",
                    )
                    single_edge_checks += 1
                    if left != 0:
                        single_edge_nonvacuous += 1
        per_order[str(order)] = order_nonvacuous
    record["instances"] = checks
    record["nonvacuous_instances"] = nonvacuous
    record["instances_with_nonzero_correction"] = with_correction
    record["nonvacuous_by_order"] = per_order
    record["single_edge_checks"] = single_edge_checks
    record["single_edge_nonvacuous"] = single_edge_nonvacuous
    record["instance_sha256"] = content_hash(instances)
    require(
        nonvacuous > 0,
        "deletion identity checks are vacuous: every instance read 0 == 0",
    )
    require(
        all(value > 0 for value in per_order.values()),
        "deletion identity checks are vacuous at some order: no instance "
        "there had a nonzero common value",
    )
    require(
        with_correction > 0,
        "deletion identity checks never exercised a nonempty T: the identity "
        "would reduce to H_B = H_B and verify nothing about the correction",
    )
    require(
        single_edge_nonvacuous > 0,
        "single-edge deletion checks are vacuous: no matching through the "
        "tested edge had nonzero weight",
    )
    return record


# ---------------------------------------------------------- S2 Lemma F


def e3_holds(blocks, sites, u, v, a, lam):
    """(E3): H_{B \\ {u,v}} == lam^{-1} e_a^{tensor}?"""
    if lam == 0 or a is None:
        return False
    rest = tuple(s for s in sorted(sites) if s not in (u, v))
    return matching_tensor(blocks, rest) == {
        tuple([a] * len(rest)): Fraction(1) / lam
    }


def e1_holds(blocks, sites, u, v, a):
    """(E1): row a of A_ux vanishes for every x outside {u,v}."""
    return all(
        all(entry == 0 for entry in oriented(blocks, u, x)[a])
        for x in sorted(sites) if x not in (u, v)
    )


def e2_holds(blocks, u, v, a, lam):
    """(E2): row a of A_uv is lam e_a with lam != 0."""
    row = oriented(blocks, u, v)[a]
    return lam != 0 and row[a] == lam and all(
        row[j] == 0 for j in COLORS if j != a
    )


def chain_packet(order, k, a, lambdas, seed):
    """A packet with k disjoint pairs (2i, 2i+1) carrying (E1),(E2),(E3).

    A_{u_i x} = 0 for x outside {u_i, v_i}; A_{u_i v_i} = lambda_i E_aa;
    the blocks inside the residue are multiples of E_aa carrying the
    hafnian 1 / prod(lambda); every remaining block is pseudorandom.
    """
    sites = tuple(range(order))
    us = tuple(2 * i for i in range(k))
    vs = tuple(2 * i + 1 for i in range(k))
    rest = tuple(s for s in sites if s >= 2 * k)
    require(len(rest) % 2 == 0, "chain packet: the residue has odd size")
    nextint = pseudorandom_stream(seed)
    blocks = zero_blocks(sites)
    for u, v in combinations(sites, 2):
        for i in COLORS:
            for j in COLORS:
                set_cell(blocks, u, v, i, j, nextint(11) - 5)
    for index in range(k):
        u, v = us[index], vs[index]
        for x in sites:
            if x in (u, v):
                continue
            for p in COLORS:
                for q in COLORS:
                    set_cell(blocks, u, x, p, q, 0)
        for p in COLORS:
            for q in COLORS:
                set_cell(blocks, u, v, p, q,
                         lambdas[index] if (p, q) == (a, a) else 0)
    target = Fraction(1)
    for lam in lambdas:
        target /= lam
    for x, y in combinations(rest, 2):
        for p in COLORS:
            for q in COLORS:
                set_cell(blocks, x, y, p, q, 0)
    if rest:
        pairs = [(rest[2 * i], rest[2 * i + 1]) for i in range(len(rest) // 2)]
        for index, (x, y) in enumerate(pairs):
            set_cell(blocks, x, y, a, a, target if index == 0 else Fraction(1))
    else:
        require(target == 1, "chain packet: an empty residue needs prod lam = 1")
    return sites, blocks, us, vs


def section_purity_chain_same_colour():
    """Lemma F, equal-colour branch: the residue is pure and nonzero."""
    record = {"instances": 0, "packets": 0}
    digest_rows = []
    for order, k in ((6, 2), (8, 2), (8, 3)):
        for seed, lam in ((101, (Fraction(2), Fraction(3), Fraction(-5))),
                          (202, (Fraction(1), Fraction(-7), Fraction(4)))):
            a = 1
            lambdas = lam[:k]
            sites, blocks, us, vs = chain_packet(order, k, a, lambdas, seed)
            record["packets"] += 1
            pairs = [edge(us[i], vs[i]) for i in range(k)]
            for index in range(k):
                u, v = us[index], vs[index]
                require(
                    e1_holds(blocks, sites, u, v, a),
                    "Lemma F instance: (E1) is broken by the construction",
                )
                require(
                    e2_holds(blocks, u, v, a, lambdas[index]),
                    "Lemma F instance: (E2) is broken by the construction",
                )
                require(
                    e3_holds(blocks, sites, u, v, a, lambdas[index]),
                    "Lemma F instance: (E3) is broken by the construction",
                )
                require(
                    not is_good_pair(blocks, sites, u, v),
                    "Lemma F instance: a carrier pair is not a bad pair",
                )
            for size in range(1, k + 1):
                for T in combinations(pairs, size):
                    covered = {s for e in T for s in e}
                    residue = tuple(s for s in sites if s not in covered)
                    tensor = matching_tensor(blocks, residue)
                    pure_word = tuple([a] * len(residue))
                    expected = Fraction(1)
                    for index in range(k):
                        if pairs[index] in T:
                            expected /= lambdas[index]
                    require(
                        expected != 0,
                        "Lemma F instance: the predicted residue coefficient "
                        "is zero, so the purity check would be vacuous",
                    )
                    require(
                        set(tensor) <= {pure_word},
                        "Lemma F failed: the residue tensor is not pure "
                        "colour-a after deleting the family T",
                    )
                    require(
                        tensor.get(pure_word, Fraction(0)) == expected,
                        "Lemma F failed: the residue purity coefficient is not "
                        "the predicted product of inverse lambdas",
                    )
                    record["instances"] += 1
                    digest_rows.append([
                        order, k, seed, sorted(T),
                        {str(word): str(value) for word, value in tensor.items()},
                    ])
            digest_rows.append(block_image(blocks))
    record["residue_sha256"] = content_hash(digest_rows)
    require(
        record["instances"] > 0,
        "Lemma F equal-colour branch was never exercised",
    )
    return record


def distinct_colour_packet(a1, a2, lam1, lam2, alpha, beta, kappa, rho, tail):
    """Eight sites, two disjoint bad pairs of DIFFERENT essential colours.

    Pairs e1 = {0,1} of colour a1 and e2 = {2,3} of colour a2 != a1.
    (E1) and (E2) hold at both; (E3) holds at e1 exactly when the
    residue hafnian data below is arranged so that H_{2..7} is the pure
    tensor lam1^{-1} e_{a1}.  These are precisely the hypotheses the
    distinct-colour branch of Lemma F's induction consumes.

    The residue R = {4,5,6,7} carries SIX nonzero blocks whose hafnian
    cancels: haf = kappa*rho + 1*1 + 1*tail, so `tail = -1 - kappa*rho`
    makes H_R vanish by cancellation rather than by a zeroed block.
    """
    sites = tuple(range(8))
    blocks = zero_blocks(sites)
    # Pseudorandom junk on the blocks that neither hypothesis touches.
    nextint = pseudorandom_stream(4242)
    for u, v in ((0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
                 (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)):
        for i in COLORS:
            for j in COLORS:
                set_cell(blocks, u, v, i, j, nextint(7) - 3)
    # (E1) at (0,1): row a1 of A_0x vanishes off the pair.
    for x in range(2, 8):
        for j in COLORS:
            set_cell(blocks, 0, x, a1, j, 0)
    # (E2) at (0,1): row a1 of A_01 is lam1 e_{a1}.
    for j in COLORS:
        set_cell(blocks, 0, 1, a1, j, lam1 if j == a1 else 0)
    # (E1)/(E2) at (2,3), colour a2.
    for x in (0, 1, 4, 5, 6, 7):
        for j in COLORS:
            set_cell(blocks, 2, x, a2, j, 0)
    for j in COLORS:
        set_cell(blocks, 2, 3, a2, j, lam2 if j == a2 else 0)
    set_cell(blocks, 2, 3, a1, a1, 1)          # free: killed by H_R = 0
    # The route carrying the pure term of H_{2..7}: 2-4, 3-5, 6-7.
    set_cell(blocks, 2, 4, a1, a1, alpha)
    set_cell(blocks, 3, 5, a1, a1, beta)
    # The residue blocks, with a cancelling hafnian.
    set_cell(blocks, 4, 5, a1, a1, kappa)
    set_cell(blocks, 6, 7, a1, a1, rho)
    set_cell(blocks, 4, 6, a1, a1, 1)
    set_cell(blocks, 5, 7, a1, a1, 1)
    set_cell(blocks, 4, 7, a1, a1, 1)
    set_cell(blocks, 5, 6, a1, a1, tail)
    return sites, blocks


def section_purity_chain_distinct_colours():
    """Lemma F, distinct-colour branch: the residue is forced to zero."""
    a1, a2 = 0, 1
    lam1, lam2 = Fraction(1), Fraction(3)
    kappa, rho = Fraction(1), Fraction(1)
    tail = -1 - kappa * rho
    alpha, beta = Fraction(1), Fraction(1)
    sites, blocks = distinct_colour_packet(
        a1, a2, lam1, lam2, alpha, beta, kappa, rho, tail
    )
    record = {"blocks_sha256": content_hash(block_image(blocks))}
    # Hypotheses, all COMPUTED from the blocks.
    record["E1_at_e1"] = e1_holds(blocks, sites, 0, 1, a1)
    record["E2_at_e1"] = e2_holds(blocks, 0, 1, a1, lam1)
    record["E3_at_e1"] = e3_holds(blocks, sites, 0, 1, a1, lam1)
    record["E1_at_e2"] = e1_holds(blocks, sites, 2, 3, a2)
    record["E2_at_e2"] = e2_holds(blocks, 2, 3, a2, lam2)
    record["e1_is_bad"] = not is_good_pair(blocks, sites, 0, 1)
    record["e2_is_bad"] = not is_good_pair(blocks, sites, 2, 3)
    record["colours_differ"] = a1 != a2
    require(
        record["E1_at_e1"] and record["E2_at_e1"] and record["E3_at_e1"],
        "Lemma F distinct-colour instance: (E1)/(E2)/(E3) do not hold at the "
        "first pair, so the induction's hypotheses are not met",
    )
    require(
        record["E1_at_e2"] and record["E2_at_e2"],
        "Lemma F distinct-colour instance: (E1)/(E2) do not hold at the "
        "second pair",
    )
    require(
        record["e1_is_bad"] and record["e2_is_bad"] and record["colours_differ"],
        "Lemma F distinct-colour instance: the two carriers are not bad pairs "
        "of distinct essential colours",
    )
    # Conclusion: H_{B \ V(T)} == 0 for T = {e1, e2}.
    residue = (4, 5, 6, 7)
    tensor = matching_tensor(blocks, residue)
    record["residue_tensor"] = {str(k): str(v) for k, v in tensor.items()}
    require(
        not tensor,
        "Lemma F failed: disjoint bad pairs of distinct essential colours did "
        "not force the deleted tensor to vanish",
    )
    # ... and the vanishing is a CANCELLATION, not a zeroed block.
    residue_blocks = [
        (x, y) for x, y in combinations(residue, 2)
        if any(entry != 0 for row in blocks[(x, y)] for entry in row)
    ]
    record["nonzero_residue_blocks"] = len(residue_blocks)
    matching_terms = []
    for matching in perfect_matchings(residue):
        value = Fraction(1)
        for x, y in matching:
            value *= blocks[(x, y)][a1][a1]
        matching_terms.append(str(value))
    record["residue_matching_terms"] = matching_terms
    nonzero_terms = sum(1 for value in matching_terms if value != "0")
    record["nonzero_residue_matching_terms"] = nonzero_terms
    require(
        len(residue_blocks) == 6 and nonzero_terms >= 2,
        "Lemma F distinct-colour check is vacuous: the residue vanishes "
        "because its blocks are zero, not by cancellation",
    )
    # Falsification probe: break the conclusion and a hypothesis must go.
    _, broken = distinct_colour_packet(
        a1, a2, lam1, lam2, alpha, beta, kappa, rho, tail + 1
    )
    broken_tensor = matching_tensor(broken, residue)
    record["probe_residue_nonzero"] = bool(broken_tensor)
    record["probe_E3_at_e1"] = e3_holds(broken, sites, 0, 1, a1, lam1)
    record["probe_E1_at_e2"] = e1_holds(broken, sites, 2, 3, a2)
    record["probe_E2_at_e2"] = e2_holds(broken, 2, 3, a2, lam2)
    require(
        record["probe_residue_nonzero"],
        "Lemma F falsification probe is vacuous: perturbing the residue did "
        "not make the deleted tensor nonzero",
    )
    require(
        record["probe_E1_at_e2"] and record["probe_E2_at_e2"],
        "Lemma F falsification probe: the perturbation broke (E1)/(E2) at the "
        "second pair, so it does not isolate (E3)",
    )
    require(
        not record["probe_E3_at_e1"],
        "Lemma F falsification probe: a packet with a nonzero deleted tensor "
        "still satisfied (E3) at the first pair -- the lemma's hypotheses "
        "would then not be load-bearing",
    )
    return record


# ---------------------------------------------------------- S3 Lemma G


def bad_pair_table(blocks, sites):
    """{pair: (essential colour or None, lambda or None)} over all BAD pairs.

    Badness is `not is_good_pair`, i.e. the committed definition: some
    deleted endpoint star fails to be injective.  The essential colour is
    read only from a ONE-dimensional single-coloured kernel covector, and
    only when the two endpoints agree; otherwise it is recorded as None
    and the pair is still counted as bad.  (Lemma E makes every essential
    kernel of an EXACT source one-dimensional and single-coloured, so
    None can occur only on the guards, which are not exact.)
    """
    table = {}
    for u, v in combinations(sorted(sites), 2):
        if is_good_pair(blocks, sites, u, v):
            continue
        witnesses = []
        clean = True
        for x, y in ((u, v), (v, u)):
            basis = essential_covectors(blocks, sites, x, y)
            if not basis:
                continue
            if len(basis) != 1:
                clean = False
                continue
            support = [c for c in COLORS if basis[0][c] != 0]
            if len(support) != 1:
                clean = False
                continue
            witnesses.append((support[0], x, y))
        require(
            witnesses or not clean,
            "badness bookkeeping broken: a bad pair exhibited no essential "
            "covector at either endpoint",
        )
        colours = {c for c, _, _ in witnesses}
        if not clean or len(colours) != 1:
            table[edge(u, v)] = (None, None)
            continue
        a = colours.pop()
        x, y = next((x, y) for c, x, y in witnesses if c == a)
        table[edge(u, v)] = (a, oriented(blocks, x, y)[a][a])
    return table


def per_site_colour_census(table, sites):
    """site -> {colour: [pairs]} over the cleanly coloured bad pairs."""
    census = {site: {} for site in sites}
    uncoloured = 0
    for pair, (a, _lam) in sorted(table.items()):
        if a is None:
            uncoloured += 1
            continue
        for site in pair:
            census[site].setdefault(a, []).append(pair)
    return census, uncoloured


def check_lemma_g(blocks, sites, label, exact_expected):
    """Lemma G's per-(site, colour) bound and the 3N/2 consequence."""
    defects = exactness_defects(blocks, sites)
    table = bad_pair_table(blocks, sites)
    census, uncoloured = per_site_colour_census(table, sites)
    worst = 0
    violations = []
    for site in sites:
        for a, pairs in census[site].items():
            worst = max(worst, len(pairs))
            if len(pairs) > 1:
                violations.append([site, a, sorted(pairs)])
    record = {
        "label": label,
        "exact": not defects,
        "bad_pairs": len(table),
        "uncoloured_bad_pairs": uncoloured,
        "bound_3N_over_2": 3 * len(sites) // 2,
        "max_pairs_per_site_and_colour": worst,
        "violations": violations,
        "census_sha256": content_hash(
            {str(site): {str(a): sorted(p) for a, p in census[site].items()}
             for site in sorted(census)}
        ),
    }
    if exact_expected:
        require(
            not defects,
            "Lemma G was applied to a packet that is not exact: %s" % label,
        )
        require(
            uncoloured == 0,
            "Lemma G on an exact source: a bad pair had no clean essential "
            "colour, contradicting Lemma E",
        )
        require(
            not violations,
            "Lemma G failed: a site lies in two bad pairs of the same "
            "essential colour on %s" % label,
        )
        require(
            len(table) <= record["bound_3N_over_2"],
            "the 3N/2 bad-pair bound failed on %s" % label,
        )
    return record, table, census


def colour_classes(table, split, sites):
    """Per-colour classes of BAD CROSSING pairs, and which of them saturate."""
    crossing = crossing_pairs(split)
    parts = part_map(split)
    classes = {}
    for pair, (a, _lam) in sorted(table.items()):
        if pair in crossing and a is not None:
            classes.setdefault(a, []).append(pair)
    report = {}
    saturating = []
    for a, pairs in sorted(classes.items()):
        touched = [s for e in pairs for s in e]
        is_matching = len(touched) == len(set(touched))
        outside = {s for s in sites if parts[s] != a}
        covers = outside <= set(touched)
        report[str(a)] = {
            "F_a": sorted(pairs),
            "is_matching": is_matching,
            "covers_B_minus_S_a": covers,
        }
        if covers:
            saturating.append(a)
    return classes, report, saturating


def section_k4():
    """The exact K_4 source: Lemma G tight, Lemma F instances, no live split."""
    sites, blocks = k4_one_factorization_packet()
    record, table, census = check_lemma_g(blocks, sites, "K_4 (exact)", True)
    record["blocks_sha256"] = content_hash(block_image(blocks))
    record["tensor_sha256"] = content_hash(
        {str(word): str(value)
         for word, value in matching_tensor(blocks, sites).items()}
    )
    record["colours_per_site"] = {
        str(site): sorted(census[site]) for site in sorted(census)
    }
    record["every_site_carries_all_three_colours"] = all(
        sorted(census[site]) == list(COLORS) for site in sites
    )
    record["bound_is_tight"] = (
        record["bad_pairs"] == record["bound_3N_over_2"]
    )
    require(
        record["every_site_carries_all_three_colours"],
        "K_4 tightness: a site does not lie in a bad pair of every colour",
    )
    require(
        record["bound_is_tight"],
        "K_4 tightness: the number of bad pairs is not the 3N/2 bound, so the "
        "bound would not be witnessed as tight",
    )
    lives = [s for s in even_splits(sites) if split_product(blocks, s) != 0]
    record["live_splits"] = len(lives)
    require(
        not lives,
        "K_4: a live split appeared, which would change the vacuity claim",
    )
    # Lemma F on a genuinely exact source: (E3) at every bad pair, and the
    # two-pair chain over disjoint pairs.
    e3_instances = 0
    for pair, (a, lam) in sorted(table.items()):
        require(
            a is not None,
            "K_4: a bad pair has no clean essential colour",
        )
        require(
            e3_holds(blocks, sites, pair[0], pair[1], a, lam),
            "(E3) failed on the exact K_4 source",
        )
        e3_instances += 1
    # The chain, step by step.  At N = 4 the SECOND step leaves the EMPTY
    # residue, where H = {(): value} and the pure word is () whatever the
    # colour is: the purity (colour) claim is unfalsifiable there and only
    # the coefficient 1/(lam_1 lam_2) carries content.  The FIRST step
    # leaves two sites, so the colour claim is falsifiable there, and the
    # chain is checked at both steps rather than only at the end.
    same_colour = 0
    distinct_colour = 0
    chain_rows = []
    residue_sizes = set()
    for (p1, d1), (p2, d2) in combinations(sorted(table.items()), 2):
        if set(p1) & set(p2):
            continue
        a1, lam1 = d1
        a2, lam2 = d2
        first = tuple(s for s in sites if s not in set(p1))
        first_tensor = matching_tensor(blocks, first)
        require(
            len(first) > 0,
            "K_4 chain step one is vacuous: the one-pair residue is empty, so "
            "its colour claim could not be falsified",
        )
        require(
            first_tensor == {tuple([a1] * len(first)): Fraction(1) / lam1},
            "Lemma F failed on K_4: deleting one bad pair does not leave the "
            "pure colour-a tensor with coefficient 1/lambda",
        )
        residue = tuple(s for s in sites if s not in set(p1) | set(p2))
        residue_sizes.add(len(residue))
        tensor = matching_tensor(blocks, residue)
        if a1 == a2:
            require(
                tensor == {
                    tuple([a1] * len(residue)): Fraction(1) / (lam1 * lam2)
                },
                "Lemma F failed on K_4: the two-pair same-colour chain is not "
                "the pure tensor with coefficient 1/(lambda_1 lambda_2)",
            )
            same_colour += 1
        else:
            require(
                not tensor,
                "Lemma F failed on K_4: a distinct-colour chain is nonzero",
            )
            distinct_colour += 1
        chain_rows.append([
            sorted(p1), sorted(p2), a1, a2, str(lam1), str(lam2),
            {str(word): str(value) for word, value in first_tensor.items()},
            {str(word): str(value) for word, value in tensor.items()},
        ])
    record["E3_instances"] = e3_instances
    record["disjoint_same_colour_chains"] = same_colour
    record["disjoint_distinct_colour_chains"] = distinct_colour
    record["chain_sha256"] = content_hash(chain_rows)
    record["two_pair_residue_sizes"] = sorted(residue_sizes)
    record["two_pair_residue_is_empty"] = residue_sizes == {0}
    require(
        e3_instances > 0 and same_colour > 0,
        "K_4 Lemma F instances are vacuous",
    )
    return record


def shape_census(max_order, ratio_num, ratio_den):
    """Even shapes a <= b <= c, a+b+c = N, c != N, with den*X <= num*N."""
    table = []
    for order in range(4, max_order + 1, 2):
        rows = []
        for a in range(0, order + 1, 2):
            for b in range(a, order + 1, 2):
                c = order - a - b
                if c < b or c == order:
                    continue
                value = a * b + a * c + b * c
                if ratio_den * value <= ratio_num * order:
                    rows.append([a, b, c, value])
        if rows:
            table.append([order, rows])
    return table


def section_shapes(max_order):
    """C4' / C5': the only shape with X <= 3N/2 is (0,2,N-2) with N <= 8."""
    sharp = shape_census(max_order, 3, 2)
    old = shape_census(20, 2, 1)
    record = {
        "max_order": max_order,
        "table_3N_over_2": sharp,
        "table_3N_over_2_sha256": content_hash(sharp),
        "table_2N_committed": old,
        "table_2N_sha256": content_hash(old),
    }
    surviving_orders = [order for order, _rows in sharp]
    record["orders_with_a_surviving_shape"] = surviving_orders
    record["all_surviving_orders_at_most_8"] = all(
        order <= 8 for order in surviving_orders
    )
    record["all_surviving_shapes_are_0_2_Nminus2"] = all(
        row[0] == 0 and row[1] == 2 and row[2] == order - 2
        for order, rows in sharp for row in rows
    )
    require(
        record["all_surviving_orders_at_most_8"],
        "C5' broken: a shape with X <= 3N/2 survives at some even N >= 10, so "
        "the unconditional good-crossing-pair claim at N >= 10 would fail",
    )
    require(
        record["all_surviving_shapes_are_0_2_Nminus2"],
        "C5' broken: a shape other than (0,2,N-2) has X <= 3N/2",
    )
    eight = [rows for order, rows in sharp if order == 8]
    record["N8_surviving_shapes"] = eight[0] if eight else []
    require(
        record["N8_surviving_shapes"] == [[0, 2, 6, 12]],
        "C5' broken: N = 8 does not reduce to the single shape (0,2,6)",
    )
    # The committed C4/C5 table is strictly weaker: check that the sharper
    # bound removes shapes the committed one kept.
    old_shapes = {(order, tuple(row[:3])) for order, rows in old for row in rows}
    sharp_shapes = {
        (order, tuple(row[:3])) for order, rows in sharp for row in rows
    }
    removed = sorted(old_shapes - sharp_shapes)
    record["shapes_removed_by_3N_over_2"] = [
        [order, list(shape)] for order, shape in removed
    ]
    require(
        removed,
        "the 3N/2 bound removed no shape at all, so it would not strengthen "
        "the committed 2N count",
    )
    return record


# ------------------------------------------- S4 saturating combinatorics


def section_saturation_characterisation():
    """Corollary C3's characterisation, on a configuration where it BITES.

    On both guards every colour class of bad crossing pairs happens to
    cover B \\ S_a, so "saturating iff F_a covers B \\ S_a" is never
    exercised in the negative direction there and the covering test could
    be replaced by `True` without any check noticing.  This purely
    combinatorial configuration -- a split, a set of bad crossing pairs
    and an essential colour for each -- has one covering class and one
    non-covering class, and requires that the brute-force enumeration of
    saturating families returns exactly the covering ones.
    """
    sites = (0, 1, 2, 3, 4, 5)
    split = ((0, 1), (2, 3), (4, 5))
    parts = part_map(split)
    table = {
        (2, 4): (0, Fraction(1)),
        (3, 5): (0, Fraction(1)),
        (0, 2): (1, Fraction(1)),
    }
    classes, report, saturating = colour_classes(table, split, sites)
    brute = set()
    for T in matchings_inside(sorted(table)):
        if not T:
            continue
        found = {table[e][0] for e in T}
        if len(found) != 1:
            continue
        a = found.pop()
        covered = {s for e in T for s in e}
        if all(parts[s] == a for s in sites if s not in covered):
            brute.add(tuple(sorted(T)))
    expected = {tuple(sorted(classes[a])) for a in saturating}
    record = {
        "split": [list(part) for part in split],
        "table": {str(pair): table[pair][0] for pair in sorted(table)},
        "colour_classes": report,
        "saturating_colours": sorted(saturating),
        "brute_force_families": sorted([sorted(T) for T in brute], key=repr),
        "characterisation_holds": brute == expected,
        "covering_classes": sorted(
            a for a, entry in report.items() if entry["covers_B_minus_S_a"]
        ),
        "non_covering_classes": sorted(
            a for a, entry in report.items() if not entry["covers_B_minus_S_a"]
        ),
    }
    require(
        record["covering_classes"] and record["non_covering_classes"],
        "the saturation characterisation probe is vacuous: every colour class "
        "covers B minus S_a, so the covering condition is never tested in the "
        "negative direction",
    )
    require(
        record["characterisation_holds"],
        "Corollary C3's characterisation failed: the saturating families are "
        "not exactly the colour classes F_a that cover B minus S_a",
    )
    return record


def section_saturating_combinatorics():
    """|T| = 1 never saturates; the (0,2,N-2) census."""
    record = {}
    singles = 0
    split_count = 0
    pair_count = 0
    for order in (4, 6, 8, 10):
        sites = tuple(range(order))
        for split in even_splits(sites):
            parts = part_map(split)
            split_count += 1
            for u, v in combinations(sites, 2):
                if parts[u] == parts[v]:
                    continue
                pair_count += 1
                for a in COLORS:
                    rest = [s for s in sites if s not in (u, v)]
                    if all(parts[s] == a for s in rest):
                        singles += 1
    record["orders"] = [4, 6, 8, 10]
    record["splits_examined"] = split_count
    record["crossing_pairs_examined"] = pair_count
    record["size_one_saturating_families"] = singles
    require(
        pair_count > 0,
        "the |T| = 1 census examined no crossing pair at all",
    )
    require(
        singles == 0,
        "Corollary C2 broken: a size-one saturating family exists, so a "
        "single bad crossing pair could carry the whole split equation",
    )
    census = {}
    for order in (6, 8, 10):
        sites = tuple(range(order))
        split = ((), (0, 1), tuple(range(2, order)))
        parts = part_map(split)
        crossing = sorted(crossing_pairs(split))
        found = {}
        for a in COLORS:
            sizes = set()
            for T in matchings_inside(crossing):
                if not T:
                    continue
                covered = {s for e in T for s in e}
                if all(parts[s] == a for s in sites if s not in covered):
                    sizes.add(len(T))
            if sizes:
                found[str(a)] = sorted(sizes)
        census[str(order)] = found
        require(
            list(found) == ["2"] and found["2"] == [2],
            "the (0,2,N-2) census changed: a colour other than the big part's, "
            "or a size other than 2, can saturate",
        )
    record["shape_0_2_Nminus2_census"] = census
    shapes = {}
    for order in (6, 8):
        sites = tuple(range(order))
        seen = {}
        for split in even_splits(sites):
            shape = tuple(sorted(len(part) for part in split))
            if shape in seen:
                continue
            parts = part_map(split)
            crossing = sorted(crossing_pairs(split))
            ok = []
            for a in COLORS:
                for T in matchings_inside(crossing):
                    if not T:
                        continue
                    covered = {s for e in T for s in e}
                    if all(parts[s] == a for s in sites if s not in covered):
                        ok.append([a, len(T)])
                        break
            seen[str(list(shape))] = sorted(ok)
        shapes[str(order)] = seen
    record["shapes_admitting_a_saturating_family"] = shapes
    record["census_sha256"] = content_hash([census, shapes])
    return record


# ------------------------------------------------ S5 Theorem C's ledger


def theorem_c_ledger(blocks, sites, split, label):
    """Theorem C's inclusion-exclusion ledger over the bad crossing pairs."""
    word = part_map(split)
    crossing = crossing_pairs(split)
    parts = part_map(split)
    table = bad_pair_table(blocks, sites)
    F = sorted(e for e in table if e in crossing)
    record = {"label": label, "bad_crossing_pairs": F}
    e3 = {}
    for e in F:
        a, lam = table[e]
        e3[e] = e3_holds(blocks, sites, e[0], e[1], a, lam)
    record["E3_holds_at"] = [e for e in F if e3[e]]
    record["E3_fails_at"] = [e for e in F if not e3[e]]
    classes, class_report, saturating = colour_classes(table, split, sites)
    record["colour_classes"] = class_report
    record["saturating_colours"] = sorted(saturating)
    record["all_colour_classes_are_matchings"] = all(
        entry["is_matching"] for entry in class_report.values()
    )
    require(
        record["all_colour_classes_are_matchings"],
        "Lemma G consequence broken on %s: a colour class of bad crossing "
        "pairs is not a matching" % label,
    )
    saturating_families = {
        tuple(sorted(classes[a])) for a in saturating
    }
    # Corollary C3, checked rather than assumed: brute-force EVERY nonempty
    # monochromatic matching T inside F with B \ V(T) inside S_a, and
    # require that the result is exactly the set of whole colour classes.
    brute = set()
    colour_of = {pair: table[pair][0] for pair in F}
    for T in matchings_inside(F):
        if not T:
            continue
        found = {colour_of[e] for e in T}
        if len(found) != 1:
            continue
        a = found.pop()
        if a is None:
            continue
        covered = {s for e in T for s in e}
        if all(parts[s] == a for s in sites if s not in covered):
            brute.add(tuple(sorted(T)))
    record["saturating_families_by_brute_force"] = sorted(
        [sorted(T) for T in brute], key=repr
    )
    record["saturating_families_are_whole_colour_classes"] = (
        brute == saturating_families
    )
    require(
        record["saturating_families_are_whole_colour_classes"],
        "Corollary C3 broken on %s: a saturating family is not a whole colour "
        "class F_a" % label,
    )
    # (The "at most three saturating families" clause of C3 is not checked
    # here: with one family per colour it cannot fail, and the content is
    # carried by saturating_families_are_whole_colour_classes above.)
    # C4': #good crossing pairs >= X - 3N/2 on this split.
    sizes = [len(part) for part in split]
    crossing_count = (
        sizes[0] * sizes[1] + sizes[0] * sizes[2] + sizes[1] * sizes[2]
    )
    require(
        len(crossing) == crossing_count,
        "the crossing count is not |S_0||S_1| + |S_0||S_2| + |S_1||S_2| on %s"
        % label,
    )
    bad_crossing = sorted(crossing - good_pairs(blocks, sites))
    require(
        bad_crossing == F,
        "badness bookkeeping broken on %s: the bad crossing pairs read off "
        "the good-pair graph differ from the ones in the bad-pair table"
        % label,
    )
    record["X"] = crossing_count
    record["bad_crossing_pairs_by_goodness"] = bad_crossing
    record["good_crossing_pairs"] = crossing_count - len(bad_crossing)
    record["three_N_over_2"] = 3 * len(sites) // 2
    record["C4prime_slack"] = (
        record["good_crossing_pairs"]
        - (crossing_count - record["three_N_over_2"])
    )
    require(
        record["C4prime_slack"] >= 0,
        "C4' broken on %s: fewer good crossing pairs than X - 3N/2" % label,
    )
    left = avoiding_sum(blocks, sites, word, frozenset(F))
    right, terms = inclusion_exclusion_sum(blocks, sites, word, frozenset(F))
    require(
        left == right,
        "the deletion identity failed on %s" % label,
    )
    record["avoiding_sum"] = str(left)
    record["split_product"] = str(split_product(blocks, split))
    surviving = []
    for T, value in terms:
        if value == 0:
            continue
        reasons = []
        if any(not e3[e] for e in T):
            reasons.append("E3-fails-on-T")
        if tuple(sorted(T)) in saturating_families:
            reasons.append("T-saturating")
        if not T:
            reasons.append("T-empty")
        require(
            reasons,
            "an unexplained surviving Theorem C term on %s: it is neither the "
            "empty family, nor (E3)-broken, nor saturating" % label,
        )
        surviving.append([sorted(T), str(value), reasons])
    record["surviving_terms"] = surviving
    good = good_pairs(blocks, sites)
    all_good = 0
    nonzero_crossing = 0
    for matching in perfect_matchings(sorted(sites)):
        cross = [e for e in matching if e in crossing]
        if not cross or weight(blocks, matching, word) == 0:
            continue
        nonzero_crossing += 1
        if all(e in good for e in cross):
            all_good += 1
    record["nonzero_crossing_matchings"] = nonzero_crossing
    record["crossing_matchings_with_all_edges_good"] = all_good
    # The unconditional |T| = 1 corollary, instance by instance:
    # sum over matchings THROUGH e equals A_e(chi) H_{B \ e}(chi), and the
    # right factor vanishes exactly when (E3) holds and B \ e is not
    # inside S_a.
    per_pair = []
    for e in F:
        a, _lam = table[e]
        rest = tuple(s for s in sites if s not in e)
        cell = blocks[e][word[e[0]]][word[e[1]]]
        through = through_sum(blocks, sites, word, e)
        deleted = sub_tensor_value(blocks, rest, word)
        require(
            through == cell * deleted,
            "single-bad-pair identity failed on %s" % label,
        )
        inside = a is not None and all(parts[s] == a for s in rest)
        per_pair.append([
            list(e), None if a is None else a, str(cell), str(deleted),
            str(through), e3[e], inside,
        ])
    record["per_bad_pair"] = per_pair
    record["bad_pairs_with_nonzero_crossing_cell"] = sum(
        1 for row in per_pair if row[2] != "0"
    )
    record["bad_pairs_carrying_zero_through_sum"] = sum(
        1 for row in per_pair if row[4] == "0"
    )
    record["no_bad_pair_has_B_minus_e_inside_S_a"] = not any(
        row[6] for row in per_pair
    )
    # A C2 instance is NONVACUOUS only when the crossing cell A_e(chi) is
    # itself nonzero: then "the sum through e vanishes" is a statement about
    # the deleted tensor, not about a zero factor.
    record["nonvacuous_C2_instances"] = sum(
        1 for row in per_pair if row[5] and row[2] != "0"
    )
    require(
        record["bad_pairs_with_nonzero_crossing_cell"] > 0,
        "the single-bad-pair check is vacuous on %s: every bad crossing pair "
        "has a zero crossing cell" % label,
    )
    require(
        record["no_bad_pair_has_B_minus_e_inside_S_a"],
        "Corollary C2 broken on %s: B minus a single crossing edge lies "
        "inside one part" % label,
    )
    for row in per_pair:
        if row[5]:
            require(
                row[4] == "0",
                "Corollary C2 broken on %s: a bad crossing pair where (E3) "
                "holds still carries a nonzero sum of matchings through it"
                % label,
            )
    return record


def section_committed_guard():
    """The committed six-site 727/729 guard, re-read through Theorem C."""
    first, second = solve_six_site_guard()
    blocks = six_site_guard_packet(first, second)
    sites = SIX_SITE_SITES
    defects = exactness_defects(blocks, sites)
    record = theorem_c_ledger(
        blocks, sites, SIX_SITE_SPLIT,
        "committed six-site guard (breaks (E3))",
    )
    record["solved_cells"] = [str(first), str(second)]
    record["satisfied_equations"] = 3 ** len(sites) - len(defects)
    record["defect_sha256"] = content_hash(
        {str(word): [str(got), str(want)]
         for word, (got, want) in defects.items()}
    )
    record["blocks_sha256"] = content_hash(block_image(blocks))
    lemma_g, _table, _census = check_lemma_g(
        blocks, sites, "committed six-site guard", False
    )
    record["lemma_g"] = lemma_g
    require(
        record["crossing_matchings_with_all_edges_good"] == 0,
        "committed guard: a nonzero crossing matching with all crossing edges "
        "good appeared, which would refute the guard's role",
    )
    require(
        record["E3_fails_at"],
        "committed guard: (E3) no longer fails at any bad crossing pair, so it "
        "would not be the (E3)-breaking half of the pair of guards",
    )
    return record


# ------------------------------------------------------ S6 the stall guard


STALL_SITES = (0, 1, 2, 3, 4, 5)
STALL_BIG = (2, 3, 4, 5)
STALL_SPLIT = ((), (0, 1), STALL_BIG)
STALL_X1, STALL_X2, STALL_P, STALL_Q = 0, 1, 2, 3
STALL_A = 2                       # essential colour = the big part's colour


def _diag(d0, d1, d2):
    return [[Fraction(d0) if (i, j) == (0, 0) else
             Fraction(d1) if (i, j) == (1, 1) else
             Fraction(d2) if (i, j) == (2, 2) else Fraction(0)
             for j in COLORS] for i in COLORS]


def _cell(i, j, value):
    return [[Fraction(value) if (p, q) == (i, j) else Fraction(0)
             for q in COLORS] for p in COLORS]


def _add(*matrices):
    out = [[Fraction(0)] * 3 for _ in COLORS]
    for matrix in matrices:
        for i in COLORS:
            for j in COLORS:
                out[i][j] += matrix[i][j]
    return out


def stall_build(params):
    """The stall packet from its structural parameters.

    With nu = A_45(2,2), lam1 = A_02(2,2), lam2 = A_13(2,2) and
    lam1 lam2 nu = 1, the purity of the two deleted-pair tensors is
    imposed by

        A_45 = nu E_22,  A_15 = 0,  A_14 = u (x) e_2,  A_35 = v (x) e_2,
            A_13 = (mu1 E_22 - u (x) v) / nu,
        A_04 = 0,  A_05 = w (x) e_2,  A_24 = z (x) e_2,
            A_02 = (mu2 E_22 - w (x) z) / nu,

    with u_2 = w_2 = 0 (that is (E1) at row a).  A_01, A_03, A_12, A_23,
    A_25, A_34 stay free.
    """
    nu = params["nu"]
    lam1 = params["lam1"]
    lam2 = Fraction(1) / (lam1 * nu)
    mu1, mu2 = Fraction(1) / lam1, Fraction(1) / lam2
    u, v, w, z = params["u"], params["v"], params["w"], params["z"]
    require(
        u[STALL_A] == 0 and w[STALL_A] == 0,
        "stall packet: u_a and w_a must vanish, which is (E1) at row a",
    )
    blocks = zero_blocks(STALL_SITES)

    def put(x, y, matrix):
        for i in COLORS:
            for j in COLORS:
                set_cell(blocks, x, y, i, j, matrix[i][j])

    zero = [[Fraction(0)] * 3 for _ in COLORS]
    unit = [[Fraction(1) if (i, j) == (STALL_A, STALL_A) else Fraction(0)
             for j in COLORS] for i in COLORS]
    put(4, 5, [[nu * unit[i][j] for j in COLORS] for i in COLORS])
    put(1, 5, zero)
    put(1, 4, [[u[i] if j == STALL_A else Fraction(0) for j in COLORS]
               for i in COLORS])
    put(3, 5, [[v[i] if j == STALL_A else Fraction(0) for j in COLORS]
               for i in COLORS])
    put(1, 3, [[(mu1 * unit[i][j] - u[i] * v[j]) / nu for j in COLORS]
               for i in COLORS])
    put(0, 4, zero)
    put(0, 5, [[w[i] if j == STALL_A else Fraction(0) for j in COLORS]
               for i in COLORS])
    put(2, 4, [[z[i] if j == STALL_A else Fraction(0) for j in COLORS]
               for i in COLORS])
    put(0, 2, [[(mu2 * unit[i][j] - w[i] * z[j]) / nu for j in COLORS]
               for i in COLORS])
    for key, matrix in sorted(params["free"].items()):
        put(key[0], key[1], matrix)
    return blocks, lam1, lam2


def stall_base_params():
    """The hand-solved structural parameters; the free cells stay open."""
    return {
        "nu": Fraction(1),
        "lam1": Fraction(1),
        "u": (Fraction(0), Fraction(1), Fraction(0)),
        "v": (Fraction(0), Fraction(0), Fraction(1)),
        "w": (Fraction(0), Fraction(1), Fraction(0)),
        "z": (Fraction(0), Fraction(0), Fraction(1)),
        "free": {
            (0, 1): _diag(1, 0, 0),
            (0, 3): _cell(1, 2, -1),
            (1, 2): _cell(1, 2, 0),
            (2, 3): _diag(0, 0, 0),
            (2, 5): _diag(1, 1, 0),
            (3, 4): _diag(1, 1, 1),
        },
    }


def crossing_sum(blocks, sites, split):
    """Theorem A's crossing sum: the matchings with at least one crossing edge."""
    word = part_map(split)
    crossing = crossing_pairs(split)
    total = Fraction(0)
    for matching in perfect_matchings(sorted(sites)):
        if not any(e in crossing for e in matching):
            continue
        total += weight(blocks, matching, word)
    return total


def solve_stall_guard():
    """Solve the split colouring equation, and record the two coupled cells.

    Every crossing matching of the split (0,1 | 2,3,4,5) pairs x_1 = 0 and
    x_2 = 1 into the big part, so the crossing sum is
    C = sum_{r != s} alpha_r beta_s h_2(big minus {r,s}) with
    alpha_r = A_{0r}(1,2) and beta_s = A_{1s}(1,2).  C does NOT depend on
    A_01, which is an inside-S_1 block, so it is computed once from the
    base parameters.  The STALL condition is that every crossing term
    avoiding both designed carriers vanish; that is a condition on the
    free cells, and it is required, not assumed.  Theorem A then reads

        0 = H_B(chi) = h_0(S_0) h_1(S_1) h_2(S_2) + C
          = A_01(1,1) * h_2(big) + C          (S_0 empty, S_1 = {0,1}),

    i.e. the split colouring equation is  h_1(S_1) h_2(S_2) = -C, whose
    unique solution is  A_01(1,1) = -C / h_2(big).

    TWO cells are then fixed, not one: setting A_01(1,1) changes the
    colour-1 anchor h_1(B) = A_01(1,1) A_25(1,1) A_34(1,1), so A_25(1,1)
    is coupled to it as 1 / A_01(1,1) to keep h_1(B) = 1.  The
    construction is that much less free than the block table suggests;
    both cells are reported, and the anchors are recomputed afterwards.
    """
    params = stall_base_params()
    blocks, _lam1, _lam2 = stall_build(params)
    require(
        blocks[(0, 1)][1][1] == 0,
        "stall guard: the base parameters already carry A_01(1,1), so the "
        "solve would not be solving for it",
    )
    alpha = {s: oriented(blocks, STALL_X1, s)[1][STALL_A] for s in STALL_BIG}
    beta = {s: oriented(blocks, STALL_X2, s)[1][STALL_A] for s in STALL_BIG}
    # The crossing terms whose two crossing edges avoid both designed
    # carriers {x_1, p} and {x_2, q}: the stall needs all of them to vanish.
    good_sum = Fraction(0)
    for r in STALL_BIG:
        for s in STALL_BIG:
            if r == s or r == STALL_P or s == STALL_Q:
                continue
            rest = tuple(t for t in STALL_BIG if t not in (r, s))
            good_sum += alpha[r] * beta[s] * hafnian(blocks, STALL_A, rest)
    require(
        good_sum == 0,
        "stall guard: a crossing term avoiding both carriers is nonzero, so "
        "the packet would not stall",
    )
    total = crossing_sum(blocks, STALL_SITES, STALL_SPLIT)
    require(
        total != 0,
        "stall guard: the crossing sum vanishes, so the colouring equation "
        "would force a dead split",
    )
    big_hafnian = hafnian(blocks, STALL_A, STALL_BIG)
    require(
        big_hafnian != 0,
        "stall guard: h_2 of the big part vanished, so the split is dead",
    )
    solved = -total / big_hafnian
    require(
        solved != 0,
        "stall guard: the solved cell A_01(1,1) is zero, so the split would "
        "not be live",
    )
    params["free"][(0, 1)] = _add(_diag(1, 0, 0), _cell(1, 1, solved))
    params["free"][(2, 5)] = _diag(1, Fraction(1) / solved, 0)
    blocks, lam1, lam2 = stall_build(params)
    # The solve must not have disturbed the crossing sum it solved against.
    require(
        crossing_sum(blocks, STALL_SITES, STALL_SPLIT) == total,
        "stall guard: setting the solved cells changed the crossing sum, so "
        "the solve was not against the final packet",
    )
    # Uniqueness: the colouring equation is affine in A_01(1,1) with slope
    # h_2(big) != 0, so the solution is unique.  Check that a neighbouring
    # value really fails, so "solved" is a solve and not one of many.
    off = dict(params)
    off["free"] = dict(params["free"])
    off["free"][(0, 1)] = _add(_diag(1, 0, 0), _cell(1, 1, solved + 1))
    off_blocks, _o1, _o2 = stall_build(off)
    off_value = coefficient(off_blocks, STALL_SITES, part_map(STALL_SPLIT))
    require(
        off_value != 0,
        "stall guard: the colouring equation also holds one step away from "
        "the solved cell, so the solve does not pin it down",
    )
    coupled = {
        "A_01(1,1)": str(blocks[(0, 1)][1][1]),
        "A_25(1,1)": str(blocks[(2, 5)][1][1]),
        "crossing_sum_C": str(total),
        "h_2(big)": str(big_hafnian),
        "H_B(chi)_one_step_off": str(off_value),
    }
    return blocks, solved, lam1, lam2, alpha, beta, good_sum, coupled


def section_stall_guard():
    """Everything the note claims about the stall guard, computed."""
    blocks, solved, lam1, lam2, alpha, beta, good_sum, coupled = (
        solve_stall_guard()
    )
    sites = STALL_SITES
    split = STALL_SPLIT
    word = part_map(split)
    record = {
        "solved_A01_1_1": str(solved),
        "coupled_solved_cells": coupled,
        "carrier_avoiding_part_of_the_crossing_sum": str(good_sum),
        "alpha": {str(k): str(v) for k, v in sorted(alpha.items())},
        "beta": {str(k): str(v) for k, v in sorted(beta.items())},
        "blocks_sha256": content_hash(block_image(blocks)),
        "nonzero_blocks": sorted(
            "A_%d%d(%d,%d)=%s" % (u, v, i, j, blocks[(u, v)][i][j])
            for (u, v) in blocks for i in COLORS for j in COLORS
            if blocks[(u, v)][i][j] != 0
        ),
    }
    anchors = [hafnian(blocks, colour, sites) for colour in COLORS]
    record["anchors"] = [str(value) for value in anchors]
    record["anchors_all_one"] = all(value == 1 for value in anchors)
    require(
        record["anchors_all_one"],
        "stall guard: a pure anchor h_c(B) is not 1, so Lemma 0's full "
        "conclusion fails",
    )
    product_value = split_product(blocks, split)
    record["split_product"] = str(product_value)
    record["split_is_live"] = product_value != 0
    require(
        record["split_is_live"],
        "stall guard: the split is dead, so Theorem C would say nothing here",
    )
    colouring = coefficient(blocks, sites, word)
    record["H_B_chi"] = str(colouring)
    record["colouring_equation_holds"] = colouring == 0
    require(
        record["colouring_equation_holds"],
        "stall guard: the live split violates its colouring equation",
    )
    # The equation the solve of A_01(1,1) was against, in the form it was
    # solved: h_1(S_1) h_2(S_2) = -C, with C the full crossing sum.
    total = crossing_sum(blocks, sites, split)
    record["crossing_sum"] = str(total)
    record["split_equation_h1h2_equals_minus_C"] = (
        hafnian(blocks, 1, split[1]) * hafnian(blocks, STALL_A, split[2])
        == -total
    )
    require(
        total != 0,
        "stall guard: the crossing sum is zero, so the solved equation would "
        "read 0 = 0",
    )
    require(
        record["split_equation_h1h2_equals_minus_C"],
        "stall guard: h_1(S_1) h_2(S_2) does not equal minus the crossing "
        "sum, so the solved cell does not satisfy Theorem A",
    )
    defects = exactness_defects(blocks, sites)
    record["total_words"] = 3 ** len(sites)
    record["satisfied_equations"] = record["total_words"] - len(defects)
    record["defects"] = sorted(
        "".join(str(c) for c in w) for w in defects
    )
    record["defect_sha256"] = content_hash(
        {str(w): [str(got), str(want)] for w, (got, want) in defects.items()}
    )
    record["is_exact"] = not defects
    require(
        not record["is_exact"],
        "stall guard: the packet came out EXACT at N = 6, contradicting "
        "Theorem 1.1 of proofs/six-site-arbitrary-complex-obstruction.md -- "
        "the packet is a guard and must not be presented as an exact source",
    )
    record["every_defect_avoids_w0_or_w1_equal_a"] = all(
        w[STALL_X1] != STALL_A and w[STALL_X2] != STALL_A for w in defects
    )
    require(
        record["every_defect_avoids_w0_or_w1_equal_a"],
        "stall guard: an exactness equation with w_0 = a or w_1 = a fails, "
        "although (E1)+(E2)+(E3) at both carriers force all of them",
    )
    # (E1), (E2), (E3) and badness at both bad crossing pairs, computed.
    structure = {}
    for x, y, lam in ((STALL_X1, STALL_P, lam1), (STALL_X2, STALL_Q, lam2)):
        basis = essential_covectors(blocks, sites, x, y)
        structure["%d-%d" % (x, y)] = {
            "lambda": str(lam),
            "kernel_dimension": len(basis),
            "E1": e1_holds(blocks, sites, x, y, STALL_A),
            "E2": e2_holds(blocks, x, y, STALL_A, lam),
            "E3": e3_holds(blocks, sites, x, y, STALL_A, lam),
            "is_bad": not is_good_pair(blocks, sites, x, y),
        }
    record["structure"] = structure
    require(
        all(entry["E1"] and entry["E2"] and entry["E3"] and entry["is_bad"]
            and entry["kernel_dimension"] == 1
            for entry in structure.values()),
        "stall guard: (E1), (E2), (E3) or badness fails at a carrier pair, so "
        "the guard would not keep the essentiality structure intact",
    )
    ledger = theorem_c_ledger(
        blocks, sites, split, "stall guard (keeps (E3))"
    )
    record["theorem_c"] = ledger
    require(
        ledger["E3_fails_at"] == [],
        "stall guard: (E3) fails at a bad crossing pair, so it would not be "
        "complementary to the committed guard",
    )
    require(
        ledger["saturating_colours"] == [STALL_A],
        "stall guard: the saturating colour class is not exactly the big "
        "part's colour",
    )
    require(
        len(ledger["surviving_terms"]) == 1,
        "stall guard: Theorem C's ledger does not reduce to a single "
        "surviving term",
    )
    term, value, reasons = ledger["surviving_terms"][0]
    record["surviving_family"] = term
    record["surviving_value"] = value
    record["surviving_reasons"] = reasons
    require(
        reasons == ["T-saturating"],
        "stall guard: the surviving Theorem C term is not explained by "
        "saturation alone",
    )
    # Theorem C reads  crossing avoiding sum = -h_0h_1h_2 + correction.
    # Here the correction equals +h_0h_1h_2 exactly, so the two cancel and
    # the good-only crossing sum is zero.
    record["correction_cancels_main_term"] = Fraction(value) == product_value
    record["crossing_avoiding_sum"] = str(
        Fraction(ledger["avoiding_sum"]) - product_value
    )
    require(
        record["crossing_avoiding_sum"] == "0",
        "stall guard: the crossing part of the F-avoiding sum is nonzero, so "
        "a good-only crossing matching would exist",
    )
    require(
        record["correction_cancels_main_term"],
        "stall guard: the saturating correction does not equal h_0h_1h_2, so "
        "the crossing sum would not stall",
    )
    require(
        ledger["crossing_matchings_with_all_edges_good"] == 0,
        "stall guard: a nonzero crossing matching with every crossing edge "
        "good exists, so the guard would not block the conjecture",
    )
    require(
        ledger["nonzero_crossing_matchings"] > 0,
        "stall guard: there is no nonzero crossing matching at all, so the "
        "absence of a good-only one would be vacuous",
    )
    # The scalar identity behind the stall:
    #   h_1(S_1) h_2(S_2) = A_{x1 p}(chi) A_{x2 q}(chi) h_2(S_2 \ {p,q}).
    left = (
        hafnian(blocks, 1, split[1]) * hafnian(blocks, STALL_A, split[2])
    )
    rest = tuple(t for t in STALL_BIG if t not in (STALL_P, STALL_Q))
    right = (
        oriented(blocks, STALL_X1, STALL_P)[1][STALL_A]
        * oriented(blocks, STALL_X2, STALL_Q)[1][STALL_A]
        * hafnian(blocks, STALL_A, rest)
    )
    record["scalar_identity"] = {
        "left_h1_h2": str(left),
        "right_two_cells_times_deleted_hafnian": str(right),
        "holds": left == right,
        "nonvacuous": left != 0,
    }
    require(
        record["scalar_identity"]["nonvacuous"],
        "stall guard: the scalar stall identity reads 0 = 0 and verifies "
        "nothing",
    )
    require(
        record["scalar_identity"]["holds"],
        "stall guard: the scalar stall identity fails, although the crossing "
        "sum stalls",
    )
    return blocks, record


# ------------------------------------------------------------------ main


def audit():
    conventions = check_imported_conventions()
    identity = section_deletion_identity()
    purity_same = section_purity_chain_same_colour()
    purity_distinct = section_purity_chain_distinct_colours()
    k4 = section_k4()
    shapes = section_shapes(200)
    characterisation = section_saturation_characterisation()
    saturating = section_saturating_combinatorics()
    committed = section_committed_guard()
    stall_blocks, stall = section_stall_guard()

    stall_lemma_g, _table, _census = check_lemma_g(
        stall_blocks, STALL_SITES, "stall guard", False,
    )
    c2_instances = (
        committed["nonvacuous_C2_instances"]
        + stall["theorem_c"]["nonvacuous_C2_instances"]
    )
    require(
        c2_instances > 0,
        "Corollary C2 has no nonvacuous instance: every bad crossing pair "
        "where (E3) holds had a zero crossing cell, so the vanishing of the "
        "sum through it would say nothing",
    )

    ledger = {
        "conventions": conventions,
        "convention_note": (
            "all machinery is IMPORTED from computations/"
            "verify_exact_source_live_split_forcing.py: endpoint-ordered "
            "blocks A_uv(i,j) reading i at u, oriented()/perfect_matchings/"
            "matching_tensor, the deleted endpoint star sigma_u^(v) of "
            "notes/target-flattening-essential-star-pair-bound.md eq. (2), "
            "and 'good pair' = both stars injective.  Badness here is "
            "exactly 'not is_good_pair'; the essential colour is read only "
            "off a one-dimensional single-coloured kernel and is recorded "
            "as None otherwise"
        ),
        "deletion_identity": identity,
        "lemma_f_same_colour": purity_same,
        "lemma_f_distinct_colours": purity_distinct,
        "k4_exact_source": k4,
        "shapes": shapes,
        "saturation_characterisation": characterisation,
        "saturating_combinatorics": saturating,
        "committed_six_site_guard": committed,
        "stall_guard": stall,
        "stall_guard_lemma_g": stall_lemma_g,
        "nonvacuous_C2_instances": c2_instances,
        "proved_by_hand_verified_here_on_instances": (
            "The deletion identity is a POLYNOMIAL IDENTITY, proved by hand "
            "in the note and verified here on 196 pseudorandom instances at "
            "N = 4,6,8 with the nonvacuous and nonzero-correction counts "
            "recorded.  Lemma F (both branches), Lemma G, C4' (#good "
            "crossing >= X - 3N/2), C5' (only the shape (0,2,N-2) with "
            "N <= 8), Theorem C and its corollaries C1-C3 are HAND PROOFS "
            "about arbitrary EXACT sources; they are verified here only on "
            "instances -- the exact K_4 source (where the 3N/2 bound is "
            "tight), constructed (E1)/(E2)/(E3) packets, and two non-exact "
            "guards.  No exact ternary source at N in {8,10} is available, "
            "so the universal quantifier over exact sources is NOT "
            "machine-verified anywhere in this artifact"
        ),
        "guards_are_not_exact_sources": (
            "both guards are GUARDS, not sources: proofs/"
            "six-site-arbitrary-complex-obstruction.md Theorem 1.1 (cited, "
            "not re-run) already excludes every complex six-site block "
            "family with H_6(A) = Delta_{6,3}, so no six-site packet can be "
            "exact.  The committed guard satisfies 727 of the 729 exactness "
            "equations and breaks (E3) at the two carriers; the stall guard "
            "satisfies 720 and keeps (E1),(E2),(E3) at both of its bad "
            "crossing pairs while defeating Theorem C on the saturating "
            "term.  They are complementary, not comparable"
        ),
        "conjectured_not_proved": (
            "the saturating case of Theorem C, and with it the full "
            "crossing-pairs-are-good lemma, remain CONJECTURED.  The "
            "COUNTING route (C4' + C5') leaves no shape at all at even "
            "N >= 10 and exactly one, (0,2,6), at N = 8; on a saturating "
            "colour class there the correction term would have to satisfy "
            "the single scalar identity h_1(S_1)h_2(S_2) = A_{x1 p}(chi) "
            "A_{x2 q}(chi) h_2(S_2 minus {p,q}).  The stall guard realises "
            "exactly that coincidence at N = 6, so it cannot be excluded "
            "from the anchors, the split equation and (E1)-(E3) alone.  "
            "Note the counting route yields only the EXISTENCE of a good "
            "crossing pair, which is strictly weaker than Theorem C's "
            "conclusion that some nonzero crossing matching has ALL its "
            "crossing edges good; the saturation analysis is the bridge "
            "between the two.  Krenn's conjecture remains open"
        ),
        "scope": (
            "Theorem C is uniform in N, but the supply of a live split is "
            "Theorem B of the committed note and is available only at "
            "N in {6,8,10} (vacuous at N = 6); uniformity in N is open and "
            "not addressed here.  Instance checks use one genuinely exact "
            "source (K_4, N = 4, which has no live split, so Theorem C is "
            "vacuous there), constructed packets satisfying (E1)-(E3), and "
            "two non-exact guards.  Krenn's conjecture remains open"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(
            digest == EXPECTED_LEDGER_SHA256,
            "good-crossing-matching forcing ledger changed",
        )
    return ledger, digest


def main():
    ledger, digest = audit()
    identity = ledger["deletion_identity"]
    print("good-crossing-matching forcing: PASS (exact)")
    print("deletion identity: %d instances at N=4,6,8 (%d nonvacuous, %d with "
          "a nonzero T != empty correction); %d single-edge instances (%d "
          "nonvacuous)"
          % (identity["instances"], identity["nonvacuous_instances"],
             identity["instances_with_nonzero_correction"],
             identity["single_edge_checks"],
             identity["single_edge_nonvacuous"]))
    same = ledger["lemma_f_same_colour"]
    distinct = ledger["lemma_f_distinct_colours"]
    print("Lemma F: %d equal-colour (packet, sub-family) instances over %d "
          "packets; distinct-colour residue = 0 by cancellation over %d "
          "nonzero blocks (%d nonzero matching terms), probe breaks (E3): %s"
          % (same["instances"], same["packets"],
             distinct["nonzero_residue_blocks"],
             distinct["nonzero_residue_matching_terms"],
             not distinct["probe_E3_at_e1"]))
    k4 = ledger["k4_exact_source"]
    print("Lemma G on the exact K_4 source: %d bad pairs = the 3N/2 bound %d "
          "(tight: %s), max per (site,colour) = %d, %d live splits"
          % (k4["bad_pairs"], k4["bound_3N_over_2"], k4["bound_is_tight"],
             k4["max_pairs_per_site_and_colour"], k4["live_splits"]))
    shapes = ledger["shapes"]
    print("C4'/C5': shapes with X <= 3N/2 verified to N = %d -> orders %s, "
          "N=8 leaves %s; the committed X <= 2N table additionally kept %s"
          % (shapes["max_order"], shapes["orders_with_a_surviving_shape"],
             shapes["N8_surviving_shapes"],
             shapes["shapes_removed_by_3N_over_2"]))
    characterisation = ledger["saturation_characterisation"]
    print("Corollary C3 characterisation probe: covering colour classes %s "
          "saturate, non-covering %s do not; brute-force families %s"
          % (characterisation["covering_classes"],
             characterisation["non_covering_classes"],
             characterisation["brute_force_families"]))
    sat = ledger["saturating_combinatorics"]
    print("saturating families: %d size-one families over %d splits and %d "
          "crossing pairs at N=4,6,8,10; shape (0,2,N-2) census %s"
          % (sat["size_one_saturating_families"], sat["splits_examined"],
             sat["crossing_pairs_examined"], sat["shape_0_2_Nminus2_census"]))
    committed = ledger["committed_six_site_guard"]
    print("committed guard: %d/%d equations, bad crossing pairs %s, (E3) fails "
          "at %s, surviving terms %s, good-only crossing matchings %d"
          % (committed["satisfied_equations"], 729,
             committed["bad_crossing_pairs"], committed["E3_fails_at"],
             [row[0] for row in committed["surviving_terms"]],
             committed["crossing_matchings_with_all_edges_good"]))
    stall = ledger["stall_guard"]
    print("stall guard: crossing sum C = %s, h_2(big) = %s, so the split "
          "equation h_1h_2 = -C solves to A_01(1,1) = %s with the coupled "
          "A_25(1,1) = %s"
          % (stall["coupled_solved_cells"]["crossing_sum_C"],
             stall["coupled_solved_cells"]["h_2(big)"],
             stall["coupled_solved_cells"]["A_01(1,1)"],
             stall["coupled_solved_cells"]["A_25(1,1)"]))
    print("  anchors %s, h_0h_1h_2 = %s, H_B(chi) = %s, %d/%d equations"
          % (stall["anchors"], stall["split_product"], stall["H_B_chi"],
             stall["satisfied_equations"], stall["total_words"]))
    print("  (E1)/(E2)/(E3) at %s; saturating colours %s; surviving family %s "
          "of value %s against -h_0h_1h_2; good-only crossing matchings %d of "
          "%d nonzero crossing matchings"
          % (sorted(stall["structure"]),
             stall["theorem_c"]["saturating_colours"],
             stall["surviving_family"], stall["surviving_value"],
             stall["theorem_c"]["crossing_matchings_with_all_edges_good"],
             stall["theorem_c"]["nonzero_crossing_matchings"]))
    print("  scalar stall identity h_1h_2 = A_x1p A_x2q h_2(rest): %s = %s"
          % (stall["scalar_identity"]["left_h1_h2"],
             stall["scalar_identity"]["right_two_cells_times_deleted_hafnian"]))
    print("Lemma G on the guards (consistency, not exact): committed %d bad "
          "pairs (%d uncoloured), stall %d (%d uncoloured), bound %d"
          % (committed["lemma_g"]["bad_pairs"],
             committed["lemma_g"]["uncoloured_bad_pairs"],
             ledger["stall_guard_lemma_g"]["bad_pairs"],
             ledger["stall_guard_lemma_g"]["uncoloured_bad_pairs"],
             ledger["stall_guard_lemma_g"]["bound_3N_over_2"]))
    print("Corollary C2 (|T| = 1 never saturates): %d nonvacuous instances "
          "across the two guards -- a bad crossing pair with (E3), a nonzero "
          "crossing cell, and a zero sum of matchings through it"
          % ledger["nonvacuous_C2_instances"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
