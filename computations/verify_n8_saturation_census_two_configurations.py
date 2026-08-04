#!/usr/bin/env python3
"""The N = 8 saturation census: Lemma H, identity (dagger), and the two
surviving configurations D1 and D2.

Companion note: `notes/n8-saturation-census-two-configurations.md`.

This checker packages the reduction of Theorem C's saturating gap at
N = 8 to TWO explicit scalar configurations.  It imports the committed
machinery -- `computations/verify_exact_source_live_split_forcing.py`
and `computations/verify_good_crossing_matching_forcing.py` -- so
conventions cannot drift, re-derives none of it, and pins the sha256
digest of every committed artifact it consumes or cites.

What is new here, and at which strength:

  Lemma H (empty-residue collapse; hand proof, verified on instances).
  Let A be an exact ternary source, (S_0,S_1,S_2) a live split, and F_a
  a saturating family of Theorem C (by Corollary C3 it is the whole
  colour-a class of bad crossing pairs, with B \\ V(F_a) contained in
  S_a).  If V(F_a) = B -- the residue R = B \\ V(F_a) is EMPTY -- then
  A_e(chi) = 0 for every e in F_a, so the saturating correction of
  Theorem C vanishes identically and Corollary C1 holds anyway.
  Proof.  By Corollary C2, |F_a| >= 2, so T' = F_a \\ {e} is a nonempty
  family of pairwise disjoint bad pairs of the one essential colour a.
  Lemma F gives H_{B \\ V(T')} = nu' e_a^tensor with nu' != 0, and
  B \\ V(T') = e = {u,v}, where H_{{u,v}}(i,j) = A_{uv}(i,j).  Hence
  A_uv = nu' E_aa.  The pair is crossing, so chi_u != chi_v and
  (chi_u, chi_v) != (a,a): A_e(chi) = 0.  []

  Identity (dagger) (general residue; hand proof, verified on
  instances).  With the same hypotheses, e = {u,v} in F_a and
  R = B \\ V(F_a) arbitrary,

    A_e(chi) h_a(R) = - sum_{r != r' in R}
        A_ur(chi_u, a) A_vr'(chi_v, a) h_a(R \\ {r, r'}).

  Proof.  Lemma F on T' = F_a \\ {e} gives H_{R u e} = nu' e_a^tensor.
  Evaluate at the word (chi on e, a on R): it is impure because the
  pair is crossing, so the value is 0; expand the (2 + |R|)-site
  matching sum by the partners of u and v.  The (u,v)-partnered terms
  give A_e(chi) h_a(R); the remaining terms pair u with some r in R
  and v with some r' != r.  []  Lemma H is the case R = empty.

  The census (exhaustive).  For every even N in {6, 8, 10}, every
  ordered even split (S_0,S_1,S_2) of {0..N-1} produced by the
  committed `even_splits` (all 3^N colourings with even parts, the
  constant colourings excluded), every colour a, and every nonempty
  matching T inside the crossing pairs of the split, the census counts
  T when B \\ V(T) is contained in S_a, and classifies it by
  (k, |R|, t) = (|T|, |B \\ V(T)|, #{edges of T meeting S_a}) under
  the key (sorted shape, |S_a|).  This is the combinatorial envelope
  of Theorem C's saturating families: by Corollary C3 an actual
  saturating family is such a T (namely F_a), so any (split, colour)
  the census clears carries no saturating family on ANY exact source.
  A configuration is DANGEROUS exactly when |R| > 0 -- Lemma H kills
  the rest.  Outcome at N = 8: shape (0,2,6) has one dangerous
  configuration but is excluded by the committed drop-(0,2,6) UNSAT
  machine theorem; shape (0,4,4) is completely clean; shape (2,2,4)
  is clean unless the saturating colour is the 4-part's colour, where
  exactly TWO configurations survive:

    D1 (k,|R|,t) = (2,4,0): F_a is a perfect matching between the two
       2-parts and the residue is the whole 4-part.  Harmful iff
       A_p1q1(b,c) A_p2q2(b,c) = A_p1p2(b,b) A_q1q2(c,c), both sides
       nonzero -- one source-block minor of
       notes/unconditional-curvature-line-selection.md eq. (3).
    D2 (k,|R|,t) = (3,2,2): one 2-part-to-2-part carrier plus two
       carriers from S_a, residue a 2-subset of S_a.  Harmful iff
       - A_f0(chi) A_f1(chi) A_f2(chi) h_a(R) = h_a(S_a) h_b(S_b) h_c(S_c).

  At N = 10 EVERY shape has dangerous configurations, so this
  reduction is N = 8 specific.

  The Boolean route is dead (solver section, SAT ledger).  The
  strengthened shape-restricted instance at n = 8 -- the committed
  recurrence shadow and units, shape (0,2,6) dropped exactly as in the
  committed drop-(0,2,6) theorem, the (0,4,4) and colour-mismatched
  (2,2,4) clauses kept dead by Lemma H, and the (2,2,4) dead clause
  weakened to "dead OR D1 OR D2" with ALL of Lemma F's residue-purity
  facts, the carrier nonvanishing facts and the a-pendant support
  facts loaded -- is SAT (73548 variables, 6101916 clauses), and stays
  SAT with every D2 option disabled.  Disabling every option restores
  the committed drop-(0,2,6) UNSAT, as a cross-check.  So no further
  support-level (Boolean) fact can close the gap: what remains in D1
  and D2 is scalar.

Everything about exact sources is a hand proof (in the note), verified
on instances only: constructed (E1)/(E2)/(E3) packets, pseudorandom
packets, the exact K_4 source and the two committed non-exact guards.
No exact ternary source at N = 8 exists to test on -- showing that
none exists is the project's aim.  Krenn's conjecture remains OPEN.

Exact stdlib arithmetic only: int and Fraction.  No floats, no bare
asserts.  The solver section is gated exactly like the committed
census pair's: it is skipped with a loud flag when python-sat is
unavailable (e.g. under `python3 -S`), and `--require-solver` makes
that a hard failure instead.

Verification:

    python3       computations/verify_n8_saturation_census_two_configurations.py
    python3 -O    computations/verify_n8_saturation_census_two_configurations.py
    python3 -I    computations/verify_n8_saturation_census_two_configurations.py
    python3 -S    computations/verify_n8_saturation_census_two_configurations.py
    python3 -I -S computations/verify_n8_saturation_census_two_configurations.py
    python3 -m py_compile computations/verify_n8_saturation_census_two_configurations.py
"""

from __future__ import annotations

import argparse
import importlib
import os
import sys
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from time import monotonic

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    # `python3 -I` does not prepend the script directory; the committed
    # companions are imported through an explicit, file-relative path.
    sys.path.insert(0, _HERE)


def require(condition, detail):
    """Assertion that survives `python3 -O` (never use a bare assert)."""
    if not condition:
        raise RuntimeError(detail)


# Digests of every committed artifact this checker imports or cites.
# Pinning them makes upstream drift a loud failure here rather than a
# silent change of meaning.
PINNED_SOURCES = {
    # imported: conventions, hafnians, splits, Lemma E/F machinery.
    "verify_exact_source_live_split_forcing.py":
        "25e52f3d6dd85a4952cd73fea026c08e19c160f22fff9c993dad39d9ac009ac0",
    # imported: matchings_inside, chain packets, (E1)-(E3) tests,
    # bad-pair table, the stall guard.
    "verify_good_crossing_matching_forcing.py":
        "7cd9f17028a0bd9e72bb3b78abf7a043b4a4b31f25b8b6804d28ccce5cdf5810",
    # imported by the solver section: the committed CNF engine.
    "verify_diagonal_recurrence_obstruction.py":
        "4421f3145c52dc64a4108687735064aaad93b5332f06135e59ce5c54311a25a1",
    # cited (step 2 of the composition): the drop-(0,2,6) UNSAT theorem.
    "verify_diagonal_termwise_census_and_pencil_guard.py":
        "8dbf8a11554a68f558e87653d5782b8b01dd2d0f2bd2bada0c9f9ff6ce42a560",
}


def pin_committed_sources():
    digests = {}
    for name in sorted(PINNED_SOURCES):
        with open(os.path.join(_HERE, name), "rb") as handle:
            digests[name] = sha256(handle.read()).hexdigest()
        require(
            digests[name] == PINNED_SOURCES[name],
            "pinned committed artifact %s changed (sha256 %s): the "
            "conventions or theorems this checker consumes may have "
            "drifted, so it refuses to run" % (name, digests[name]),
        )
    return digests


PINNED_DIGESTS = pin_committed_sources()

C = importlib.import_module("verify_exact_source_live_split_forcing")
G = importlib.import_module("verify_good_crossing_matching_forcing")

COLORS = C.COLORS
content_hash = C.content_hash

EXPECTED_LEDGER_SHA256 = (
    "7819357369b7c17a16e6e62bf4bd8c0f837bd6479f2b79f395d562bc8a4b21ac"
)
EXPECTED_SAT_LEDGER_SHA256 = (
    "2b38816182bc6f54a156a4b354a91f14899d4e73f8e48d6ac27248eb8488d488"
)

# The canonical shape-(2,2,4) split used for the geometry section:
# S_b = {0,1}, S_c = {2,3}, S_a = {4,5,6,7} with a = 2 the 4-part colour.
CANONICAL_SPLIT = ((0, 1), (2, 3), (4, 5, 6, 7))
CANONICAL_A = 2


# ------------------------------------------------------- S0 conventions


def section_conventions():
    """Pin the imported machinery to the endpoint-ordered convention.

    Positive and negative probes: the transposed orientation must carry
    the transposed cell, the untouched transpose cell of the SAME block
    must stay zero (so a symmetric copy would be caught), the empty
    hafnian must be 1, and a two-site hafnian must read exactly the
    (colour, colour) cell -- the fact the D1 reduction consumes as
    h_b(S_b) = A_p1p2(b,b).
    """
    sites = (0, 1, 2, 3)
    blocks = C.zero_blocks(sites)
    C.set_cell(blocks, 0, 1, 0, 2, Fraction(5))
    C.set_cell(blocks, 2, 3, 1, 1, Fraction(7))
    require(
        C.oriented(blocks, 0, 1)[0][2] == 5
        and C.oriented(blocks, 1, 0)[2][0] == 5,
        "conventions: oriented(v,u) with u < v must be the transpose",
    )
    require(
        C.oriented(blocks, 0, 1)[2][0] == 0,
        "conventions: the untransposed cell (2,0) of an asymmetric block "
        "is nonzero, so oriented() would be symmetrizing, not transposing",
    )
    require(C.hafnian(blocks, 0, ()) == 1,
            "conventions: the empty hafnian must be 1")
    require(
        C.hafnian(blocks, 1, (2, 3)) == 7 and C.hafnian(blocks, 0, (2, 3)) == 0,
        "conventions: a two-site hafnian must read exactly the "
        "(colour, colour) cell of its block -- h_b(S_b) = A_p1p2(b,b) is "
        "what the D1 scalar reduction consumes",
    )
    return {"committed_file_sha256": dict(PINNED_DIGESTS)}


# --------------------------------------------------------- S1 the census


def saturating_families(order, split, colour):
    """Every nonempty matching T inside the split's crossing pairs with
    B \\ V(T) contained in S_colour, as (T, R, t) with T the sorted edge
    tuple, R the residue and t = #{edges of T meeting S_colour}.

    This is the single enumeration path used by the census, the
    geometry section and the controls; there is no other implementation
    of the saturation test in this artifact.
    """
    sites = tuple(range(order))
    parts = C.part_map(split)
    crossing = sorted(C.crossing_pairs(split))
    out = []
    for T in G.matchings_inside(crossing):
        if not T:
            continue
        covered = {s for e in T for s in e}
        if not all(parts[s] == colour for s in sites if s not in covered):
            continue
        R = tuple(s for s in sites if s not in covered)
        t = sum(1 for e in T
                if parts[e[0]] == colour or parts[e[1]] == colour)
        out.append((tuple(sorted(T)), R, t))
    return out


def saturating_census(order):
    """{(shape, |S_a|): sorted list of (k, |R|, t)} over ALL ordered even
    splits of {0..order-1} and all colours a."""
    out = {}
    for split in C.even_splits(tuple(range(order))):
        shape = tuple(sorted(len(part) for part in split))
        for colour in COLORS:
            for T, R, t in saturating_families(order, split, colour):
                out.setdefault((shape, len(split[colour])), set()).add(
                    (len(T), len(R), t))
    return {key: sorted(value) for key, value in out.items()}


def census_record(table):
    return {str([list(shape), size]): [list(config) for config in configs]
            for (shape, size), configs in sorted(table.items())}


def section_census():
    tables = {}
    record = {}
    for order in (6, 8, 10):
        table = saturating_census(order)
        tables[order] = table
        record[str(order)] = census_record(table)
        record[str(order) + "_dangerous"] = {
            key: [config for config in configs if config[1] > 0]
            for key, configs in census_record(table).items()
            if any(config[1] > 0 for config in configs)
        }
    eight = tables[8]
    require(
        set(eight) == {((0, 2, 6), 6), ((0, 4, 4), 0), ((0, 4, 4), 4),
                       ((2, 2, 4), 2), ((2, 2, 4), 4)},
        "N=8 census: the set of (shape, |S_a|) admitting a saturating "
        "family changed",
    )
    # Lemma H disposes of every family with an empty residue.
    for key in (((0, 4, 4), 0), ((0, 4, 4), 4), ((2, 2, 4), 2)):
        require(
            all(config[1] == 0 for config in eight[key]),
            "N=8 census: shape %s with |S_a|=%d acquired a saturating "
            "family with nonempty residue, so Lemma H no longer clears "
            "it" % key,
        )
    require(
        [config for config in eight[((2, 2, 4), 4)] if config[1] > 0]
        == [(2, 4, 0), (3, 2, 2)],
        "N=8 census: the dangerous configurations of shape (2,2,4) with "
        "the saturating colour on the 4-part are no longer exactly D1 = "
        "(2,4,0) and D2 = (3,2,2)",
    )
    require(
        [config for config in eight[((0, 2, 6), 6)] if config[1] > 0]
        == [(2, 4, 2)],
        "N=8 census: shape (0,2,6) changed its dangerous configuration",
    )
    # Positive direction: the census must not be empty, or the clearing
    # requirements above would hold vacuously.
    require(
        sum(len(configs) for configs in eight.values()) == 7,
        "N=8 census: the total number of saturating configurations is "
        "no longer 7",
    )
    # N=6: the stall guard's configuration must appear, dangerous.
    require(
        tables[6][((0, 2, 4), 4)] == [(2, 2, 2)],
        "N=6 census: shape (0,2,4) with |S_a|=4 is not exactly the stall "
        "guard's configuration (k,|R|,t) = (2,2,2)",
    )
    # N=10: EVERY shape has a dangerous configuration -- the reduction
    # to two configurations is N=8 specific, and this require keeps the
    # note honest about it.
    ten = tables[10]
    shapes_all = {shape for shape, _size in ten}
    shapes_dangerous = {
        shape for (shape, _size), configs in ten.items()
        if any(config[1] > 0 for config in configs)
    }
    require(
        shapes_all == shapes_dangerous
        == {(0, 2, 8), (0, 4, 6), (2, 2, 6), (2, 4, 4)},
        "N=10 census: some shape lost (or gained) its dangerous "
        "configurations, so the claim that the reduction is N=8-specific "
        "changed",
    )
    return record, tables


# ------------------------------------------- S2 the geometry of D1 and D2


def section_census_geometry():
    """The actual families behind the census signatures, on the
    canonical split S_b = {0,1}, S_c = {2,3}, S_a = {4,5,6,7}, a = 2.

    Also the positive/negative control of the single enumeration path:
    an explicitly named family must be found, an explicitly named
    non-covering matching must be rejected.
    """
    split = CANONICAL_SPLIT
    families = saturating_families(8, split, CANONICAL_A)
    by_signature = {}
    for T, R, t in families:
        by_signature.setdefault((len(T), len(R), t), []).append((T, R))
    require(
        set(by_signature) == {(2, 4, 0), (3, 2, 2), (4, 0, 4)},
        "canonical split: the saturating signatures are no longer "
        "{D1 = (2,4,0), D2 = (3,2,2), empty-residue = (4,0,4)}",
    )
    # --- the enumeration-path control (single implementation, S1).
    found = {T for T, _R, _t in families}
    require(
        ((0, 2), (1, 3)) in found,
        "census enumerator control: the explicitly named D1 family "
        "{{0,2},{1,3}} of the canonical split was not enumerated",
    )
    require(
        ((0, 2),) not in found,
        "census enumerator control: the single edge {0,2} leaves the "
        "sites 1 and 3 uncovered outside S_a, so counting it means the "
        "covering condition was dropped",
    )
    # --- D1: the two perfect matchings between the 2-parts.
    d1 = sorted(T for T, _R in by_signature[(2, 4, 0)])
    require(
        d1 == [((0, 2), (1, 3)), ((0, 3), (1, 2))],
        "D1 geometry: the nonempty-residue k=2 families of the canonical "
        "split are not exactly the two perfect matchings between the two "
        "2-parts",
    )
    for T, R in by_signature[(2, 4, 0)]:
        require(R == (4, 5, 6, 7),
                "D1 geometry: the residue is not the whole 4-part")
        require(
            all(set(e) <= {0, 1, 2, 3} and len(set(e) & {0, 1}) == 1
                for e in T),
            "D1 geometry: a family edge does not join the two 2-parts",
        )
    # --- D2: one 2-to-2 carrier plus two S_a carriers.
    d2 = by_signature[(3, 2, 2)]
    require(
        len(d2) == 48,
        "D2 geometry: the canonical split no longer carries exactly 48 "
        "k=3 families (4 outside carriers x 12 S_a attachments)",
    )
    for T, R in d2:
        require(len(R) == 2 and set(R) <= {4, 5, 6, 7},
                "D2 geometry: the residue is not a 2-subset of the 4-part")
        outside = [e for e in T if set(e) <= {0, 1, 2, 3}]
        require(
            len(outside) == 1 and len(set(outside[0]) & {0, 1}) == 1,
            "D2 geometry: not exactly one carrier joins the two 2-parts",
        )
        touching = [e for e in T if set(e) & {4, 5, 6, 7}]
        require(
            len(touching) == 2
            and all(len(set(e) & {4, 5, 6, 7}) == 1 for e in touching),
            "D2 geometry: the two S_a carriers are not S_a-to-outside "
            "edges",
        )
    # --- the empty-residue class Lemma H kills: full crossing matchings.
    empty = by_signature[(4, 0, 4)]
    require(
        all(R == () for _T, R in empty),
        "canonical split: an empty-residue family has a nonempty residue",
    )
    # --- the 2-part colours of the same split have only empty residues.
    for colour in (0, 1):
        other = saturating_families(8, split, colour)
        require(
            other and all(R == () and (len(T), t) == (4, 2)
                          for T, R, t in other),
            "canonical split: the saturating families of a 2-part colour "
            "are no longer all of signature (4,0,2), so Lemma H would no "
            "longer clear |S_a| = 2 at shape (2,2,4)",
        )
    return {
        "split": [list(part) for part in split],
        "saturating_colour": CANONICAL_A,
        "D1_families": [[list(e) for e in T] for T in d1],
        "D1_residue": [4, 5, 6, 7],
        "D2_family_count": len(d2),
        "D2_families": sorted([sorted([list(e) for e in T]), list(R)]
                              for T, R in d2),
        "empty_residue_family_count": len(empty),
    }


# ---------------------------------- S3 the hafnian expansion of (dagger)


def dagger_check(blocks, sites, family, colour, e, chi):
    """Both sides of identity (dagger) at the carrier e of `family`."""
    covered = {s for f in family for s in f}
    residue = tuple(s for s in sorted(sites) if s not in covered)
    u, v = e
    left = (C.oriented(blocks, u, v)[chi[u]][chi[v]]
            * C.hafnian(blocks, colour, residue))
    right = Fraction(0)
    for r in residue:
        for rp in residue:
            if r == rp:
                continue
            rest = tuple(s for s in residue if s not in (r, rp))
            right += (C.oriented(blocks, u, r)[chi[u]][colour]
                      * C.oriented(blocks, v, rp)[chi[v]][colour]
                      * C.hafnian(blocks, colour, rest))
    return left, -right


def section_dagger_expansion():
    """The hafnian expansion (dagger) rests on, checked where it has
    content.  For ANY packet, sites u != v and a set R disjoint from
    them,

        H_{R u {u,v}}(chi_u at u, chi_v at v, a on R)
          = A_uv(chi_u,chi_v) h_a(R)
            + sum_{r != r' in R} A_ur(chi_u,a) A_vr'(chi_v,a)
                                 h_a(R \\ {r,r'}).

    Identity (dagger) is this expansion with the left side killed by
    Lemma F's purity.  On the guards |R| <= 2, where every sub-hafnian
    h_a(R \\ {r,r'}) is the empty hafnian 1 -- so that factor is NOT
    load-bearing there.  The pseudorandom instances at |R| = 4 and 6
    are what make it load-bearing, and the sharpness probe requires
    that replacing the sub-hafnian by 1 actually breaks the expansion
    somewhere.
    """
    record = {"instances": 0, "nonvacuous": 0,
              "with_nontrivial_subhafnian": 0, "sharpness_disagreements": 0}
    for size in (0, 2, 4, 6):
        for seed in (11, 29):
            sites = tuple(range(size + 2))
            blocks = G.pseudorandom_packet(sites, seed)
            u, v = size, size + 1
            residue = tuple(range(size))
            for (ci, cj) in ((0, 1), (2, 0)):
                colour = 2 if ci != 2 else 1
                chi = {s: colour for s in residue}
                chi[u], chi[v] = ci, cj
                left = C.coefficient(blocks, sites,
                                     {s: chi[s] for s in sites})
                right = (C.oriented(blocks, u, v)[ci][cj]
                         * C.hafnian(blocks, colour, residue))
                dropped = right
                nontrivial = False
                for r in residue:
                    for rp in residue:
                        if r == rp:
                            continue
                        rest = tuple(s for s in residue
                                     if s not in (r, rp))
                        sub = C.hafnian(blocks, colour, rest)
                        if rest and sub != 1:
                            nontrivial = True
                        factor = (C.oriented(blocks, u, r)[ci][colour]
                                  * C.oriented(blocks, v, rp)[cj][colour])
                        right += factor * sub
                        dropped += factor
                require(
                    left == right,
                    "the (dagger) hafnian expansion failed: the "
                    "two-endpoint pivot of H_{R u e} does not reproduce "
                    "the packet coefficient",
                )
                record["instances"] += 1
                if left != 0:
                    record["nonvacuous"] += 1
                if nontrivial:
                    record["with_nontrivial_subhafnian"] += 1
                if dropped != right:
                    record["sharpness_disagreements"] += 1
    require(
        record["nonvacuous"] >= 8,
        "the (dagger) expansion instances are mostly 0 = 0, so they "
        "verify nothing about the correction",
    )
    require(
        record["with_nontrivial_subhafnian"] >= 4,
        "the (dagger) expansion was never exercised with a sub-hafnian "
        "h_a(R minus {r,r'}) different from the empty hafnian 1, so "
        "dropping that factor would be invisible",
    )
    require(
        record["sharpness_disagreements"] >= 4,
        "sharpness probe: replacing every sub-hafnian by 1 never changed "
        "the expansion, so that factor is not load-bearing on these "
        "instances",
    )
    return record


# ------------------------------------------- S4 Lemma H on built packets


def block_of(blocks, u, v):
    return [list(row) for row in C.oriented(blocks, u, v)]


def section_lemma_h():
    """Lemma H, nonvacuously: chain packets whose family covers B.

    Each carrier is checked to satisfy computed (E1)/(E2)/(E3); the
    Lemma-F step the proof consumes (drop one carrier, the residue IS
    that carrier, and its tensor is the pure nu E_aa with nu != 0) is
    recomputed from the blocks; the conclusion -- all six crossing
    cells of the carrier block vanish -- is swept cell by cell; and
    identity (dagger) is confirmed to degenerate to it at R = empty.
    A detector control perturbs one crossing cell of a copied block and
    requires the sweep to see it, so the six-zero check cannot be
    satisfied by reading the wrong block.
    """
    colour = 1
    record = {"instances": 0, "nonvacuous": 0, "dagger_instances": 0,
              "rows": []}
    for order, k, lambdas in (
        (8, 4, (Fraction(2), Fraction(3), Fraction(-1), Fraction(-1, 6))),
        (8, 4, (Fraction(-5), Fraction(1), Fraction(2), Fraction(-1, 10))),
        (6, 3, (Fraction(3), Fraction(-2), Fraction(-1, 6))),
    ):
        prod = Fraction(1)
        for lam in lambdas:
            prod *= lam
        require(prod == 1,
                "Lemma H packet: an empty residue needs prod(lambda) = 1")
        sites, blocks, us, vs = G.chain_packet(order, k, colour, lambdas,
                                               7 * order + k)
        family = [C.edge(us[i], vs[i]) for i in range(k)]
        for index in range(k):
            u, v = us[index], vs[index]
            require(G.e1_holds(blocks, sites, u, v, colour),
                    "Lemma H packet: (E1) is broken by the construction")
            require(G.e2_holds(blocks, u, v, colour, lambdas[index]),
                    "Lemma H packet: (E2) is broken by the construction")
            require(G.e3_holds(blocks, sites, u, v, colour, lambdas[index]),
                    "Lemma H packet: (E3) is broken by the construction")
        for index in range(k):
            e = family[index]
            others = [f for j, f in enumerate(family) if j != index]
            residue = tuple(s for s in sites
                            if s not in {x for f in others for x in f})
            require(
                set(residue) == set(e),
                "Lemma H: dropping one carrier of a full family must "
                "leave exactly that carrier's two sites",
            )
            nu = Fraction(1)
            for j, lam in enumerate(lambdas):
                if j != index:
                    nu /= lam
            require(
                C.matching_tensor(blocks, residue) == {(colour, colour): nu},
                "Lemma H: Lemma F on the family minus one carrier did not "
                "leave the pure colour-a tensor nu E_aa",
            )
            block = block_of(blocks, e[0], e[1])
            require(
                all(block[i][j] == (nu if (i, j) == (colour, colour) else 0)
                    for i in COLORS for j in COLORS),
                "Lemma H: the carrier block is not nu E_aa",
            )
            swept = 0
            for ci in COLORS:
                for cj in COLORS:
                    if ci == cj:
                        continue
                    require(
                        block[ci][cj] == 0,
                        "Lemma H: a crossing cell of the carrier block is "
                        "nonzero, so the saturating term need not vanish",
                    )
                    swept += 1
            require(swept == 6, "Lemma H: the crossing-cell sweep is empty")
            record["instances"] += 1
            if nu != 0:
                record["nonvacuous"] += 1
            record["rows"].append([order, k, index, nu])
            # (dagger) at R = empty is exactly Lemma H: both sides 0.
            chi = {s: 0 for s in sites}
            chi[e[0]], chi[e[1]] = 0, 2
            left, right = dagger_check(blocks, sites, family, colour, e, chi)
            require(left == right and left == 0,
                    "identity (dagger) failed at an empty residue")
            record["dagger_instances"] += 1
    # Detector control: the six-cell sweep must be able to see an impure
    # carrier.  Perturb one crossing cell on a fresh packet and look.
    sites, blocks, us, vs = G.chain_packet(
        6, 3, colour, (Fraction(3), Fraction(-2), Fraction(-1, 6)), 4242)
    C.set_cell(blocks, us[0], vs[0], 0, 2, Fraction(9))
    perturbed = block_of(blocks, us[0], vs[0])
    require(
        any(perturbed[i][j] != 0 for i in COLORS for j in COLORS if i != j),
        "Lemma H detector control: a deliberately impure carrier block "
        "shows no nonzero crossing cell, so the six-cell sweep is "
        "reading the wrong block",
    )
    # Where the empty-residue hypothesis is load-bearing: chain packets
    # force pure carrier blocks by construction even at 2k < order, so
    # the |R| > 0 contrast is carried by the stall guard (S6), whose
    # |R| = 2 carrier blocks have NONZERO crossing cells -- required
    # there, not here.
    record["load_bearing_note"] = (
        "chain_packet builds A_uv = lambda E_aa by hand, so the "
        "empty-residue hypothesis cannot be seen to matter on it; the "
        "stall guard (|R| = 2, nonzero carrier crossing cells, required "
        "in its section) is the witness that Lemma H fails without it")
    return record


# ------------------------------------- S5 the scalar forms of D1 and D2


def section_d1_d2_scalar_forms():
    """The scalar content of the two dangerous configurations.

    Hand derivation (note, section 4), consuming committed Theorem C
    and Lemma F only.  The checker fixes the SIGNS from the census
    ((-1)^k with the computed k), re-reads the two-site hafnian
    convention from an actual pseudorandom packet, and probes each
    harmful condition with a nonvacuous positive instance (the
    Theorem-C total vanishes, every factor nonzero) and a negative
    instance (one cell perturbed, the total is nonzero).

      D1 harmful:  A_p1q1(b,c) A_p2q2(b,c) = A_p1p2(b,b) A_q1q2(c,c),
                   both sides nonzero;
      D2 harmful:  - A_f0(chi) A_f1(chi) A_f2(chi) h_a(R)
                   = h_a(S_a) h_b(S_b) h_c(S_c).
    """
    families = saturating_families(8, CANONICAL_SPLIT, CANONICAL_A)
    ks = sorted({len(T) for T, R, _t in families if R})
    require(ks == [2, 3],
            "scalar forms: the dangerous family sizes at the canonical "
            "split are no longer k = 2 (D1) and k = 3 (D2)")
    sign_d1 = (-1) ** ks[0]
    sign_d2 = (-1) ** ks[1]
    require((sign_d1, sign_d2) == (1, -1),
            "scalar forms: the Theorem-C signs (-1)^k of D1 and D2 are "
            "no longer +1 and -1")
    # The 2-site hafnian convention on real blocks (h_b(S_b) = A_p1p2(b,b)).
    blocks = G.pseudorandom_packet(tuple(range(8)), 23)
    h_b = C.hafnian(blocks, 0, (0, 1))
    h_c = C.hafnian(blocks, 1, (2, 3))
    require(
        h_b == C.oriented(blocks, 0, 1)[0][0] and h_b != 0
        and h_c == C.oriented(blocks, 2, 3)[1][1] and h_c != 0,
        "scalar forms: h_b(S_b) does not read the (b,b) cell of the "
        "2-part block nonvacuously, so the D1 reduction's substitution "
        "h_b(S_b) = A_p1p2(b,b) is not the convention in force",
    )
    # D1: total = -h_a h_b h_c + (+1) A_e1 A_e2 h_a with h_b = A_p1p2(b,b),
    # h_c = A_q1q2(c,c).
    h_a = Fraction(7, 3)
    a_e1, a_e2 = Fraction(2, 3), Fraction(3, 5)
    b_cell, c_cell = Fraction(1, 2), Fraction(4, 5)
    require(a_e1 * a_e2 == b_cell * c_cell != 0,
            "scalar forms: the designed D1 instance does not satisfy the "
            "minor identity with both sides nonzero")
    total = -h_a * b_cell * c_cell + sign_d1 * a_e1 * a_e2 * h_a
    require(total == 0,
            "scalar forms: on a D1-harmful instance the Theorem-C total "
            "does not vanish -- the stated D1 condition or its sign is "
            "wrong")
    perturbed = (-h_a * b_cell * c_cell
                 + sign_d1 * (a_e1 + 1) * a_e2 * h_a)
    require(perturbed != 0,
            "scalar forms: perturbing one D1 cell left the total zero, "
            "so the positive probe is vacuous")
    # D2: total = -h_a h_b h_c + (-1) A_f0 A_f1 A_f2 h_a(R).
    a_f0, a_f1, a_f2 = Fraction(2), Fraction(3), Fraction(-1)
    h_r = Fraction(1, 2)
    h_a2, h_b2, h_c2 = Fraction(3), Fraction(1), Fraction(1)
    require(-a_f0 * a_f1 * a_f2 * h_r == h_a2 * h_b2 * h_c2 != 0,
            "scalar forms: the designed D2 instance does not satisfy the "
            "product identity with both sides nonzero")
    total2 = -h_a2 * h_b2 * h_c2 + sign_d2 * a_f0 * a_f1 * a_f2 * h_r
    require(total2 == 0,
            "scalar forms: on a D2-harmful instance the Theorem-C total "
            "does not vanish -- the stated D2 condition or its sign is "
            "wrong")
    perturbed2 = (-h_a2 * h_b2 * h_c2
                  + sign_d2 * (a_f0 + 1) * a_f1 * a_f2 * h_r)
    require(perturbed2 != 0,
            "scalar forms: perturbing one D2 cell left the total zero, "
            "so the positive probe is vacuous")
    return {
        "signs": [sign_d1, sign_d2],
        "packet_h_b": h_b,
        "packet_h_c": h_c,
        "D1_condition": "A_p1q1(b,c) A_p2q2(b,c) = A_p1p2(b,b) A_q1q2(c,c),"
                        " both sides nonzero (one source-block minor of"
                        " unconditional-curvature-line-selection.md eq. (3))",
        "D2_condition": "-A_f0(chi) A_f1(chi) A_f2(chi) h_a(R)"
                        " = h_a(S_a) h_b(S_b) h_c(S_c)",
        "D1_instance": [h_a, a_e1, a_e2, b_cell, c_cell],
        "D2_instance": [h_r, a_f0, a_f1, a_f2, h_a2, h_b2, h_c2],
    }


# --------------------------------------------------- S6 the stall guard


def section_stall():
    """Where the committed stall guard sits in the census, and identity
    (dagger) on it.

    The guard satisfies (E1)+(E2)+(E3) at both carriers -- everything
    Lemma H's proof consumes -- and still has nonzero carrier crossing
    cells.  It escapes Lemma H purely on the residue count |R| = 2;
    that consistency is REQUIRED here, not assumed, and its computed
    configuration is cross-checked against the abstract census in the
    audit.
    """
    blocks, solved, lam1, lam2, _alpha, _beta, _good, coupled = \
        G.solve_stall_guard()
    sites = G.STALL_SITES
    split = G.STALL_SPLIT
    parts = C.part_map(split)
    colour = G.STALL_A
    record = {"solved_cell": solved, "coupled": coupled}
    table = G.bad_pair_table(blocks, sites)
    crossing = C.crossing_pairs(split)
    bad_crossing = sorted(e for e in table if e in crossing)
    record["bad_crossing_pairs"] = [list(e) for e in bad_crossing]
    family = sorted(e for e in bad_crossing if table[e][0] == colour)
    record["colour_%d_class" % colour] = [list(e) for e in family]
    require(family == [(0, 2), (1, 3)],
            "stall guard: the colour-2 class of bad crossing pairs "
            "changed")
    covered = {s for e in family for s in e}
    residue = tuple(s for s in sites if s not in covered)
    t = sum(1 for e in family
            if parts[e[0]] == colour or parts[e[1]] == colour)
    record["k_R_t"] = [len(family), len(residue), t]
    record["residue"] = list(residue)
    require(
        (len(family), len(residue), t) == (2, 2, 2),
        "stall guard: its saturating configuration is no longer "
        "(k,|R|,t) = (2,2,2), so the census entry it must match has "
        "moved",
    )
    require(
        len(residue) > 0,
        "stall guard: the residue is empty, so Lemma H would apply to it "
        "and the guard would contradict Lemma H",
    )
    # Lemma F on the whole family: H_R is the pure block nu E_aa.
    nu = Fraction(1) / (lam1 * lam2)
    tensor = C.matching_tensor(blocks, residue)
    require(tensor == {(colour, colour): nu},
            "stall guard: H_R is not the pure colour-a tensor Lemma F "
            "predicts")
    record["H_R"] = {str(list(word)): value for word, value in tensor.items()}
    record["nu"] = nu
    # The carrier blocks are NOT pure: exactly what Lemma H forbids at
    # R = empty, so |R| = 2 is the whole escape.
    chi = C.part_map(split)
    crossing_cells = {}
    for e in family:
        u, v = e
        crossing_cells[str(list(e))] = C.oriented(blocks, u, v)[chi[u]][chi[v]]
    record["carrier_crossing_cells"] = crossing_cells
    require(
        all(value != 0 for value in crossing_cells.values()),
        "stall guard: a carrier's crossing cell vanished, so the guard "
        "would no longer witness that Lemma H's empty-residue hypothesis "
        "is load-bearing",
    )
    # Identity (dagger) at both carriers, nonvacuously.
    dagger = {}
    for e in family:
        left, right = dagger_check(blocks, sites, family, colour, e, chi)
        dagger[str(list(e))] = [left, right]
        require(left == right,
                "identity (dagger) failed on the stall guard at carrier "
                "%s" % (e,))
        require(left != 0,
                "identity (dagger) on the stall guard is 0 = 0 at a "
                "carrier, so it verifies nothing there")
    record["dagger"] = dagger
    # Exactness defects: the guard is NOT exact (it cannot be -- no
    # exact source exists at N = 6), and no defect word reads the
    # essential colour at a carrier site, so Lemma H's inputs are the
    # (E1)-(E3) facts the guard SATISFIES: the escape is |R| = 2 alone.
    defects = C.exactness_defects(blocks, sites)
    record["defect_count"] = len(defects)
    record["defect_words"] = sorted(list(word) for word in defects)
    require(len(defects) == 9,
            "stall guard: the defect count is not 9 (720 of 729)")
    require(
        all(word[0] != colour and word[1] != colour for word in defects),
        "stall guard: a defect word reads the essential colour at site 0 "
        "or 1, although (E1)+(E2)+(E3) force every such equation",
    )
    inputs_hold = all(
        G.e1_holds(blocks, sites, e[0], e[1], colour)
        and G.e2_holds(blocks, e[0], e[1], colour, table[e][1])
        and G.e3_holds(blocks, sites, e[0], e[1], colour, table[e][1])
        for e in family
    )
    record["lemma_h_inputs_hold"] = inputs_hold
    require(
        inputs_hold,
        "stall guard: (E1)/(E2)/(E3) do not all hold at both carriers, "
        "so the statement that it escapes Lemma H purely on |R| = 2 "
        "would be vacuous",
    )
    return record


# --------------------------------------- S7 the K_4 and omega controls


def section_controls():
    """The two committed packets on which the census must be vacuous,
    each for its own stated reason."""
    record = {}
    sites, blocks = C.k4_one_factorization_packet()
    require(C.exactness_defects(blocks, sites) == {},
            "K_4: the one-factorization packet is not an exact ternary "
            "source")
    live = C.live_splits(blocks, sites)
    record["k4_live_splits"] = [[list(part) for part in split]
                                for split in live]
    require(
        live == [],
        "K_4: a live split appeared, so the census and Lemma H would no "
        "longer be vacuous there for the reason stated",
    )
    record["k4_note"] = ("exact, but no live split: Theorem C and Lemma H "
                         "are vacuous on K_4")
    osites, oblocks, _names = C.omega_guard_packet()
    olive = C.live_splits(oblocks, osites)
    otable = G.bad_pair_table(oblocks, osites)
    counts = []
    for split in olive:
        cross = C.crossing_pairs(split)
        counts.append(len([e for e in otable if e in cross]))
    record["omega_live_splits"] = len(olive)
    record["omega_bad_crossing_pairs_per_live_split"] = sorted(set(counts))
    require(
        counts and set(counts) == {0},
        "omega guard: it acquired a bad crossing pair, so the statement "
        "that no saturating family exists there changes",
    )
    record["omega_note"] = ("live splits but zero bad crossing pairs: "
                            "F_a is empty, no saturating family exists, "
                            "and Theorem C already yields the good "
                            "crossing matching")
    return record


# ===================================================== solver section


def import_solver():
    """Lazy import of PySAT and the committed engine, as one unit."""
    try:
        from pysat.formula import CNF, IDPool
        from pysat.solvers import Solver
        engine = importlib.import_module(
            "verify_diagonal_recurrence_obstruction")
    except ImportError as error:
        return None, "%s: %s" % (type(error).__name__, error)
    return (CNF, IDPool, Solver, engine), ""


def build_strengthened(solver_api, n):
    """The strengthened shape-restricted instance at n = 8.

    Recurrence shadow and units verbatim from the committed engine;
    shape (0,2,n-2) dropped exactly as the committed drop-(0,2,6) mode
    does; every other non-(2,2,4) shape gets the plain dead clause
    (Lemma H: no dangerous saturating family exists there); each
    (2,2,4) colouring gets  dead OR D1 OR D2, where every option
    carries the full Boolean shadow of its configuration:

      * residue purity (Lemma F on every nonempty sub-family):
        z_a(res) = 1, z_b(res) = z_c(res) = 0;
      * carrier nonvanishing: z_a(carrier) = 1 (lambda != 0);
      * a-pendant support: (E1) at a carrier (u,v) makes W_a(u,x) = 0
        for x != v, so every even T with u in T, v not in T has
        z_a(T) = 0.
    """
    CNF, IDPool, _Solver, engine = solver_api
    pool = IDPool()
    cnf = CNF()
    evens = engine.even_masks(n)
    full = (1 << n) - 1

    def z(colour, mask):
        return pool.id(("z", colour, mask))

    for colour in range(3):
        cnf.append([z(colour, 0)])
        cnf.append([z(colour, full)])
        for mask in evens:
            if mask.bit_count() < 4:
                continue
            vertices = tuple(v for v in range(n) if mask >> v & 1)
            for pivot in vertices:
                terms = []
                for other in vertices:
                    if other == pivot:
                        continue
                    edge_mask = (1 << pivot) | (1 << other)
                    rest = mask ^ edge_mask
                    term = pool.id(("term", colour, mask, edge_mask))
                    engine.add_iff_and(cnf, term, z(colour, edge_mask),
                                       z(colour, rest))
                    terms.append(term)
                cnf.append([-z(colour, mask)] + terms)
                engine.add_zero_forbids_unique(cnf, z(colour, mask), terms)

    def mask_of(pair_sites):
        mask = 0
        for site in pair_sites:
            mask |= 1 << site
        return mask

    stats = {"free_026": 0, "dead_other": 0, "cond_224": 0,
             "d1_options": 0, "d2_options": 0}
    options = {}
    for colouring in product(range(3), repeat=n):
        masks = [0, 0, 0]
        for vertex, colour in enumerate(colouring):
            masks[colour] |= 1 << vertex
        if any(mask.bit_count() % 2 for mask in masks):
            continue
        if any(mask == full for mask in masks):
            continue
        shape = tuple(sorted(mask.bit_count() for mask in masks))
        dead = [-z(colour, masks[colour]) for colour in range(3)]
        if shape == (0, 2, n - 2):
            stats["free_026"] += 1
            continue                    # dropped: the committed UNSAT mode
        if shape != (2, 2, 4):
            cnf.append(dead)            # Lemma H leaves nothing dangerous
            stats["dead_other"] += 1
            continue
        stats["cond_224"] += 1
        colour_a = next(colour for colour in range(3)
                        if masks[colour].bit_count() == 4)
        colour_b, colour_c = [colour for colour in range(3)
                              if colour != colour_a]
        part_a = tuple(v for v in range(n) if masks[colour_a] >> v & 1)
        part_b = tuple(v for v in range(n) if masks[colour_b] >> v & 1)
        part_c = tuple(v for v in range(n) if masks[colour_c] >> v & 1)

        def residue_purity(option, mask):
            cnf.append([-option, z(colour_a, mask)])
            cnf.append([-option, -z(colour_b, mask)])
            cnf.append([-option, -z(colour_c, mask)])

        def pendant_facts(option, u, v):
            for even_mask in evens:
                if (even_mask >> u & 1) and not (even_mask >> v & 1):
                    cnf.append([-option, -z(colour_a, even_mask)])

        d1_vars, d2_vars = [], []
        # D1: F_a a perfect matching between the two 2-parts, R = S_a.
        for j in (0, 1):
            edges = ((part_b[0], part_c[j]), (part_b[1], part_c[1 - j]))
            for pend in product((0, 1), repeat=2):
                option = pool.id(("D1", colouring, j, pend))
                residue_purity(option, masks[colour_a])
                for index, e in enumerate(edges):
                    edge_mask = mask_of(e)
                    cnf.append([-option, z(colour_a, edge_mask)])
                    residue_purity(option, full ^ edge_mask)
                    pendant_facts(option, e[pend[index]],
                                  e[1 - pend[index]])
                d1_vars.append(option)
                stats["d1_options"] += 1
        # D2: one 2-to-2 carrier plus two S_a carriers, R in C(S_a, 2).
        for res in combinations(part_a, 2):
            res_mask = mask_of(res)
            s_pair = tuple(v for v in part_a if v not in res)
            for i0 in (0, 1):
                for j0 in (0, 1):
                    f0 = (part_b[i0], part_c[j0])
                    x, y = part_b[1 - i0], part_c[1 - j0]
                    for swap in (0, 1):
                        s1, s2 = s_pair[swap], s_pair[1 - swap]
                        option = pool.id(("D2", colouring, res, i0, j0, swap))
                        residue_purity(option, res_mask)
                        family_masks = [mask_of(f)
                                        for f in (f0, (s1, x), (s2, y))]
                        for family_mask in family_masks:
                            cnf.append([-option, z(colour_a, family_mask)])
                        for size in (1, 2):
                            for sub in combinations(range(3), size):
                                cover = 0
                                for index in sub:
                                    cover |= family_masks[index]
                                residue_purity(option, full ^ cover)
                        for (u, v) in ((x, s1), (y, s2)):
                            pendant_facts(option, u, v)
                        d2_vars.append(option)
                        stats["d2_options"] += 1
        options[colouring] = {"D1": tuple(d1_vars), "D2": tuple(d2_vars),
                              "masks": tuple(masks)}
        cnf.append(dead + d1_vars + d2_vars)
    return pool, cnf, z, stats, options


def symmetry_branches(solver_api, n, z):
    """The committed engine's exhaustive symmetry branches, verbatim."""
    _CNF, _IDPool, _Solver, engine = solver_api
    base = engine.edge_assumptions(z, 0, engine.canonical_matching(n))
    types = tuple(engine.integer_partitions(n // 2))
    coincident = (1,) * (n // 2)
    branches = []
    for cycle_type in types:
        first = engine.edge_assumptions(
            z, 1, engine.matching_of_cycle_type(n, cycle_type))
        if cycle_type != coincident:
            branches.append((str(cycle_type), base + first))
            continue
        for third_type in types:
            third = engine.edge_assumptions(
                z, 2, engine.matching_of_cycle_type(n, third_type))
            branches.append(("%s; colour2=%s" % (cycle_type, third_type),
                             base + first + third))
    return branches


def audit_model(solver_api, n, z, cnf, model, assumptions, options, mode):
    """Independently re-audit a SAT model: every clause and assumption
    is re-checked semantically, the danger clause of every Boolean-live
    (2,2,4) colouring must be discharged by a true option, and the live
    shapes are read off and confined to the dropped/conditional ones."""
    _CNF, _IDPool, _Solver, engine = solver_api
    model_set = set(model)
    for clause in cnf.clauses:
        if not any(literal in model_set for literal in clause):
            raise RuntimeError(
                "SAT model audit (%s): the solver's model violates a "
                "clause of its own formula" % mode)
    require(all(literal in model_set for literal in assumptions),
            "SAT model audit (%s): the model violates a symmetry-branch "
            "or option assumption" % mode)
    live = saved_d1 = saved_d2 = 0
    for _colouring, data in options.items():
        if not all(z(colour, mask) in model_set
                   for colour, mask in enumerate(data["masks"])):
            continue
        live += 1
        d1_true = any(option in model_set for option in data["D1"])
        d2_true = any(option in model_set for option in data["D2"])
        require(
            d1_true or d2_true,
            "SAT model audit (%s): a Boolean-live (2,2,4) colouring is "
            "saved by no danger option, so the danger clause is violated "
            "semantically" % mode,
        )
        saved_d1 += d1_true
        saved_d2 += d2_true
    full = (1 << n) - 1
    families = tuple(
        sorted(mask for mask in engine.even_masks(n)
               if z(colour, mask) in model_set)
        for colour in range(3))
    family_sets = tuple(frozenset(family) for family in families)
    live_shapes = {}
    for colouring in product(range(3), repeat=n):
        masks = [0, 0, 0]
        for vertex, colour in enumerate(colouring):
            masks[colour] |= 1 << vertex
        if any(mask.bit_count() % 2 for mask in masks):
            continue
        if any(mask == full for mask in masks):
            continue
        if all(masks[colour] in family_sets[colour]
               for colour in range(3)):
            shape = tuple(sorted(mask.bit_count() for mask in masks))
            live_shapes[shape] = live_shapes.get(shape, 0) + 1
    require(
        set(live_shapes) <= {(0, 2, n - 2), (2, 2, 4)},
        "SAT model audit (%s): the model has a Boolean-live shape other "
        "than the dropped (0,2,6) and the conditional (2,2,4), so a dead "
        "clause is violated" % mode,
    )
    require(
        live_shapes.get((2, 2, 4), 0) == live,
        "SAT model audit (%s): the option-table scan and the family scan "
        "disagree on the number of Boolean-live (2,2,4) colourings" % mode,
    )
    return {
        "live_224_colourings": live,
        "saved_by_D1": saved_d1,
        "saved_by_D2": saved_d2,
        "live_shapes": {str(list(shape)): count
                        for shape, count in sorted(live_shapes.items())},
        "model_hash": content_hash([list(family) for family in families]),
    }


def section_sat(solver_api):
    """SAT / SAT / UNSAT: the Boolean route past D1 and D2 is dead.

    One CNF, three assumption regimes over the committed symmetry
    branches: the full strengthened instance (SAT), the instance with
    every D2 option disabled (SAT: D1 alone still saturates the
    relaxation), and the instance with every option disabled, which is
    semantically the committed drop-(0,2,6) instance (UNSAT: the
    cross-check tying this encoder to the committed machine theorem).
    """
    _CNF, _IDPool, Solver, _engine = solver_api
    n = 8
    started = monotonic()
    pool, cnf, z, stats, options = build_strengthened(solver_api, n)
    require(
        (pool.top, len(cnf.clauses)) == (73548, 6101916),
        "the strengthened n=8 instance no longer has the recorded size "
        "(73548 variables, 6101916 clauses): the encoding drifted",
    )
    require(
        (stats["free_026"], stats["dead_other"], stats["cond_224"],
         stats["d1_options"], stats["d2_options"])
        == (168, 210, 1260, 10080, 60480),
        "the strengthened n=8 instance no longer has the recorded clause "
        "census (168 dropped (0,2,6) colourings, 210 dead (0,4,4), 1260 "
        "conditional (2,2,4), 10080 D1 and 60480 D2 options)",
    )
    branches = symmetry_branches(solver_api, n, z)
    require(len(branches) == 9,
            "the n=8 symmetry branch count is not the committed engine's 9")
    d1_all = [option for data in options.values() for option in data["D1"]]
    d2_all = [option for data in options.values() for option in data["D2"]]
    regimes = (
        ("strengthened", [], "SAT",
         "the strengthened n=8 instance (all Lemma F residue purity, "
         "carrier nonvanishing and a-pendant facts loaded) is no longer "
         "SAT: the Boolean route would not be dead and the reduction to "
         "scalar content would be understated"),
        ("strengthened-no-D2", [-option for option in d2_all], "SAT",
         "the strengthened n=8 instance with every D2 option disabled is "
         "no longer SAT: D1 alone would no longer saturate the Boolean "
         "relaxation"),
        ("no-danger-options", [-option for option in d1_all + d2_all],
         "UNSAT",
         "the strengthened n=8 instance with every danger option "
         "disabled is not UNSAT, although it is semantically the "
         "committed drop-(0,2,6) instance: the encoder no longer agrees "
         "with the committed machine theorem"),
    )
    runs = []
    with Solver(name="cadical195", bootstrap_with=cnf) as solver:
        for mode, extra, expected, complaint in regimes:
            verdicts = []
            audit = None
            for label, assumptions in branches:
                satisfiable = solver.solve(assumptions=assumptions + extra)
                verdicts.append((label, satisfiable))
                if satisfiable:
                    audit = audit_model(solver_api, n, z, cnf,
                                        solver.get_model(),
                                        assumptions + extra, options, mode)
                    break
            verdict = "SAT" if any(flag for _l, flag in verdicts) else "UNSAT"
            require(verdict == expected, complaint)
            if verdict == "SAT":
                # Positive control on the live-colouring scan: the
                # no-danger-options regime is UNSAT, so every model of a
                # SAT regime must be Boolean-live at some (2,2,4)
                # colouring; a blind scan would make the danger-clause
                # audit pass vacuously.
                require(
                    audit is not None
                    and audit["live_224_colourings"] >= 1,
                    "SAT model audit (%s): the model has no Boolean-live "
                    "(2,2,4) colouring, although the no-danger-options "
                    "UNSAT forces one -- the live-colouring scan is "
                    "blind" % mode,
                )
            if verdict == "UNSAT":
                require(
                    len(verdicts) == len(branches),
                    "strengthened SAT census: mode %s is UNSAT but did "
                    "not exhaust its symmetry branches" % mode,
                )
            if mode == "strengthened-no-D2" and audit is not None:
                require(
                    audit["saved_by_D2"] == 0,
                    "strengthened SAT census: a D2 option is true although "
                    "every D2 option was disabled by assumption",
                )
            runs.append({
                "mode": mode,
                "verdict": verdict,
                "disabled_options": len(extra),
                "branches_solved": len(verdicts),
                "sat_branch": (verdicts[-1][0] if verdict == "SAT"
                               else None),
                "model_audit": audit,
            })
    return {
        "n": n,
        "variables": pool.top,
        "clauses": len(cnf.clauses),
        "colouring_census": stats,
        "branches": len(branches),
        "runs": runs,
    }, monotonic() - started


# ============================================================== audit


def audit(require_solver=False):
    conventions = section_conventions()
    census, tables = section_census()
    geometry = section_census_geometry()
    dagger = section_dagger_expansion()
    lemma_h = section_lemma_h()
    scalars = section_d1_d2_scalar_forms()
    stall = section_stall()
    controls = section_controls()
    # Cross-implementation control: the stall guard's configuration,
    # computed from its BLOCKS (bad-pair table + crossing pairs), must
    # be the unique entry the abstract census enumerator reports for its
    # (shape, |S_a|) -- two independent paths to the same object.
    require(
        tables[6][((0, 2, 4), 4)] == [tuple(stall["k_R_t"])],
        "cross-check: the stall guard's configuration computed from its "
        "blocks is not the unique census entry at shape (0,2,4) with "
        "|S_a| = 4 -- the two independent enumeration paths disagree",
    )
    ledger = {
        "conventions": conventions,
        "census": census,
        "census_geometry": geometry,
        "dagger_expansion": dagger,
        "lemma_H": lemma_h,
        "d1_d2_scalar_forms": scalars,
        "stall_guard": stall,
        "controls": controls,
        "proved": (
            "Lemma H (empty-residue collapse) and identity (dagger) are "
            "hand proofs from committed Lemma F / Corollaries C2-C3, "
            "verified on instances; the census and the D1/D2 geometry "
            "are exhaustive machine facts over all ordered even splits "
            "at N = 6, 8, 10"
        ),
        "open": (
            "the minimal open statement at N = 8: rule out D1 and D2 on "
            "an exact source with live split (4,2,2).  Krenn's "
            "conjecture remains open"
        ),
    }
    digest = content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "n8 saturation census ledger changed")
    solver_api, reason = import_solver()
    if solver_api is None:
        if require_solver:
            raise SystemExit(
                "python-sat is required; run with `uv run --with "
                "python-sat python ...` (import failed: %s)" % reason)
        sat_ledger = {"status": "SKIPPED", "reason": reason}
        sat_digest = None
        seconds = None
    else:
        sat_ledger, seconds = section_sat(solver_api)
        sat_ledger["status"] = "RUN"
        sat_digest = content_hash(sat_ledger)
        if EXPECTED_SAT_LEDGER_SHA256 != "TO_BE_FROZEN":
            require(sat_digest == EXPECTED_SAT_LEDGER_SHA256,
                    "n8 saturation census SAT ledger changed")
    return ledger, digest, sat_ledger, sat_digest, seconds


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-solver", action="store_true",
                        help="fail, as the committed engine does, when "
                             "PySAT is unavailable instead of skipping "
                             "the solver section")
    arguments = parser.parse_args()
    ledger, digest, sat_ledger, sat_digest, seconds = audit(
        arguments.require_solver)

    print("n8 saturation census, two configurations: PASS (exact)")
    print("census: N=8 dangerous configurations %s at shape (2,2,4) with "
          "the saturating colour on the 4-part, plus %s at the excluded "
          "shape (0,2,6); shapes (0,4,4) and (2,2,4)|S_a|=2 clean "
          "(Lemma H); N=10 dangerous in every shape"
          % (ledger["census"]["8_dangerous"]["[[2, 2, 4], 4]"],
             ledger["census"]["8_dangerous"]["[[0, 2, 6], 6]"]))
    geometry = ledger["census_geometry"]
    print("geometry (canonical split): D1 = %s (residue = the 4-part), "
          "D2 = %d families (one 2-to-2 carrier + two S_a carriers, "
          "residue a 2-subset of S_a)"
          % (geometry["D1_families"], geometry["D2_family_count"]))
    dagger = ledger["dagger_expansion"]
    print("(dagger) expansion: %d instances (%d nonvacuous, %d with a "
          "nontrivial sub-hafnian, %d sharpness disagreements)"
          % (dagger["instances"], dagger["nonvacuous"],
             dagger["with_nontrivial_subhafnian"],
             dagger["sharpness_disagreements"]))
    lemma_h = ledger["lemma_H"]
    print("Lemma H: %d carrier instances on full-cover chain packets, all "
          "nonvacuous (%d), (dagger) degenerate at R = empty on all %d"
          % (lemma_h["instances"], lemma_h["nonvacuous"],
             lemma_h["dagger_instances"]))
    stall = ledger["stall_guard"]
    print("stall guard: configuration (k,|R|,t) = %s matches the census, "
          "escapes Lemma H purely on |R| = 2 (carrier crossing cells %s, "
          "(E1)-(E3) hold at both carriers, 9 defect words none reading "
          "the essential colour at a carrier site)"
          % (tuple(stall["k_R_t"]),
             {k: str(v) for k, v in stall["carrier_crossing_cells"].items()}))
    print("sha256:", digest)

    if sat_ledger["status"] == "SKIPPED":
        print("strengthened SAT census: SKIPPED -- %s" % sat_ledger["reason"])
        print("  the three verdicts (strengthened SAT, no-D2 SAT, "
              "no-danger-options UNSAT) are NOT ESTABLISHED in this run; "
              "they require python-sat.  Re-run with a solver, or with "
              "--require-solver to make this a hard failure.")
        print("  the 'Boolean route is dead' claim of the note is "
              "therefore conditional on that census in this run.")
        return
    print("strengthened SAT instance: %d variables, %d clauses, %s; "
          "branches %d; %.1f s"
          % (sat_ledger["variables"], sat_ledger["clauses"],
             sat_ledger["colouring_census"], sat_ledger["branches"],
             seconds))
    for run in sat_ledger["runs"]:
        audit_line = ""
        if run["model_audit"] is not None:
            audit_line = (" live(2,2,4)=%d savedD1=%d savedD2=%d shapes=%s"
                          % (run["model_audit"]["live_224_colourings"],
                             run["model_audit"]["saved_by_D1"],
                             run["model_audit"]["saved_by_D2"],
                             run["model_audit"]["live_shapes"]))
        print("  %-22s %-5s (options disabled: %d, branches solved: %d)%s"
              % (run["mode"], run["verdict"], run["disabled_options"],
                 run["branches_solved"], audit_line))
    print("sat sha256:", sat_digest)


if __name__ == "__main__":
    main()
