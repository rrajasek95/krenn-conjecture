#!/usr/bin/env python3
"""Exact support-cover audit for the minimal N=8 D1 locus off Sigma.

The audit is field-independent.  It imports only the committed D1 artifact,
pins that artifact by SHA-256, and reconstructs the support problem without
using any historical scratch directory.

For an E1-admissible D1 packet, let m be the number of nonzero aggregate
cells outside the a-column class Sigma.  The two monochromatic output
equations force m >= 6.  At m = 6 this checker enumerates the 72 possible
three-cell residue covers for each colour, hence 72^2 = 5184 labelled
support signatures.  Exact residue purity, the two six-site Lemma-F purity
systems, and unique-monomial full-output certificates kill 5136.  The 48
remaining signatures form one orbit under the D1-preserving group
C2 x S4.  A canonical representative and its conservative exact polynomial
search input are frozen in the ledger.
"""

from __future__ import annotations

import importlib
import os
import sys
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    """Assertion which remains active under ``python -O``."""
    if not condition:
        raise RuntimeError(detail)


PINNED_D1_SHA256 = (
    "6320c3bdb795df3050952e52bd9c0fb9f4d5f2cdbf9eb543cd3467179630a745"
)
D1_PATH = os.path.join(HERE, "verify_n8_d2_kill_and_monochrome_rigidity.py")
with open(D1_PATH, "rb") as handle:
    D1_SHA256 = sha256(handle.read()).hexdigest()
require(D1_SHA256 == PINNED_D1_SHA256,
        "the committed D1 checker changed; refusing an unreviewed input")

D = importlib.import_module("verify_n8_d2_kill_and_monochrome_rigidity")
SITES = D.SITES
COLORS = D.COLORS
SMALL = D.D1_SMALL
RESIDUE = D.D1_RESIDUE
W1 = D.W1
W2 = D.W2

EXPECTED_LEDGER_SHA256 = (
    "69166fa61fad7499bf991aa803c6e6a138a1f64a51ba6e9e26cc9e0a86db0a88"
)


def cell(u, v, i, j):
    """Canonical endpoint-ordered cell A_uv(i,j)."""
    if u < v:
        return (u, v, i, j)
    return (v, u, j, i)


def e1_admissible(u, v, i, j):
    partner = D.D1_ESSENTIAL_PARTNER
    return not ((u in partner and i == 2 and v != partner[u])
                or (v in partner and j == 2 and u != partner[v]))


def reconstruct_support_domains():
    admissible = {
        (u, v, i, j)
        for u, v in combinations(SITES, 2)
        for i in COLORS for j in COLORS
        if e1_admissible(u, v, i, j)
    }
    sigma = set()
    for u, v in combinations(SMALL, 2):
        for i in COLORS:
            for j in COLORS:
                if e1_admissible(u, v, i, j):
                    sigma.add((u, v, i, j))
    for u in SMALL:
        for r in RESIDUE:
            for i in COLORS:
                if e1_admissible(u, r, i, 2):
                    sigma.add(cell(u, r, i, 2))
    for r, s in combinations(RESIDUE, 2):
        sigma.add((r, s, 2, 2))
    require(sigma == set(D.sigma_cells()),
            "independent Sigma reconstruction differs from committed D1")
    off_sigma = admissible - sigma
    kinds = Counter("RR" if u in RESIDUE else "SR"
                    for u, _v, _i, _j in off_sigma)
    require(len(admissible) == 217 and len(sigma) == 89
            and len(off_sigma) == 128
            and kinds == {"RR": 48, "SR": 80},
            "D1 support-domain census changed")
    return admissible, sigma, off_sigma, kinds


MATCHINGS = {
    tuple(domain): tuple(tuple(matching)
                         for matching in D.C.perfect_matchings(domain))
    for domain in (SITES, W1, W2, RESIDUE)
}


def matching_cells(matching, word):
    return tuple(cell(u, v, word[u], word[v]) for u, v in matching)


def anchor_signatures(colour):
    """All size-three off-Sigma traces of an 8-site monochrome matching.

    Such a matching has one residue-residue edge, two small-residue edges,
    and one small-small edge.  The returned record retains that fourth,
    Sigma-supported anchor factor, because the anchor equation makes it a
    unit on the minimal stratum.
    """
    records = []
    for rr in combinations(RESIDUE, 2):
        residue_left = tuple(r for r in RESIDUE if r not in rr)
        for crossing_small in combinations(SMALL, 2):
            small_left = tuple(u for u in SMALL if u not in crossing_small)
            anchor_factor = cell(*small_left, colour, colour)
            for residue_order in (residue_left, residue_left[::-1]):
                extras = frozenset({
                    cell(*rr, colour, colour),
                    cell(crossing_small[0], residue_order[0], colour, colour),
                    cell(crossing_small[1], residue_order[1], colour, colour),
                })
                records.append({
                    "rr": tuple(rr),
                    "crossing_small": tuple(crossing_small),
                    "residue_order": tuple(residue_order),
                    "extras": extras,
                    "anchor_factor": anchor_factor,
                })
    require(len(records) == 72
            and len({(r["extras"], r["anchor_factor"])
                     for r in records}) == 72,
            "a colour no longer has 72 minimal anchor signatures")
    return records


def minimum_support_audit():
    """Finite graph facts which prove m >= 6 and the 3+3 normal form."""
    full = MATCHINGS[SITES]
    trace_histogram = Counter()
    for matching in full:
        residue_edges = tuple(edge for edge in matching
                              if set(edge) & set(RESIDUE))
        rr_count = sum(set(edge) <= set(RESIDUE) for edge in residue_edges)
        trace_histogram[(rr_count, len(residue_edges))] += 1
    require(trace_histogram == {(2, 2): 9, (1, 3): 72, (0, 4): 24},
            "the 105 matchings no longer have the 2/3/4 residue-cover split")

    residue_matchings = [frozenset(matching)
                         for matching in MATCHINGS[RESIDUE]]
    require(len(residue_matchings) == 3,
            "the four-site residue no longer has three matchings")
    # A graph with <=3 residue edges cannot contain two distinct perfect
    # matchings.  This is the cancellation obstruction used when one colour
    # tries to cover the residue in only two off-Sigma cells.
    rr_edges = tuple(combinations(RESIDUE, 2))
    checked = 0
    for size in range(4):
        for chosen in combinations(rr_edges, size):
            count = sum(matching <= set(chosen)
                        for matching in residue_matchings)
            require(count <= 1,
                    "three residue edges unexpectedly contain two matchings")
            checked += 1
    require(checked == 42, "the <=3-edge residue graph census changed")
    return {"full_matching_trace_histogram": {
                "%d_RR_%d_trace" % key: value
                for key, value in sorted(trace_histogram.items())},
            "residue_graphs_up_to_three_edges": checked,
            "conclusion": "m >= 6; at m=6 both colour traces have size 3"}


BASE_UNITS = frozenset({
    cell(0, 1, 0, 0),  # live b-part
    cell(2, 3, 1, 1),  # live c-part
    cell(0, 2, 0, 1),  # first D1 carrier at chi
    cell(1, 3, 0, 1),  # second D1 carrier at chi
})


def unique_mandatory_certificate(allowed, mandatory):
    """Return a mixed full word with one allowed, mandatory matching term."""
    for matching in MATCHINGS[SITES]:
        choices = []
        for u, v in matching:
            on_edge = [entry for entry in sorted(mandatory)
                       if entry[:2] == (u, v)]
            if not on_edge:
                break
            choices.append(on_edge)
        else:
            for picked in product(*choices):
                word = {}
                for u, v, i, j in picked:
                    word[u], word[v] = i, j
                if len(set(word.values())) == 1:
                    continue
                supported = [
                    matching_cells(other, word)
                    for other in MATCHINGS[SITES]
                    if all(entry in allowed
                           for entry in matching_cells(other, word))
                ]
                if len(supported) == 1:
                    require(set(supported[0]) <= mandatory,
                            "unique certificate uses a non-mandatory cell")
                    return tuple(word[site] for site in SITES), supported[0]
    return None


def map_cell(entry, mapping):
    u, v, i, j = entry
    return cell(mapping[u], mapping[v], i, j)


def d1_group():
    group = []
    for swap in (False, True):
        small_map = ({0: 0, 1: 1, 2: 2, 3: 3} if not swap
                     else {0: 1, 1: 0, 2: 3, 3: 2})
        for perm in permutations(RESIDUE):
            group.append(small_map | dict(zip(RESIDUE, perm)))
    require(len(group) == 48
            and len({tuple(sorted(g.items())) for g in group}) == 48,
            "D1-preserving C2 x S4 group changed")
    return group


def support_cover_audit(sigma):
    b_signatures = anchor_signatures(0)
    c_signatures = anchor_signatures(1)
    tally = Counter()
    survivors = set()
    examples = {}
    without_anchor_units = 0

    for b_record in b_signatures:
        for c_record in c_signatures:
            tally["total"] += 1
            b_rr, c_rr = set(b_record["rr"]), set(c_record["rr"])
            if not (b_rr & c_rr):
                verdict = "residue_mixed_unique"
            elif (b_record["crossing_small"] in ((0, 2), (1, 3))
                  or c_record["crossing_small"] in ((0, 2), (1, 3))):
                verdict = "six_site_purity_unique"
            else:
                extras = b_record["extras"] | c_record["extras"]
                allowed = sigma | extras
                mandatory = (BASE_UNITS | extras
                             | {b_record["anchor_factor"],
                                c_record["anchor_factor"]})
                certificate = unique_mandatory_certificate(allowed, mandatory)
                old_certificate = unique_mandatory_certificate(
                    allowed, BASE_UNITS | extras)
                if old_certificate is not None:
                    without_anchor_units += 1
                if certificate is not None:
                    verdict = "full_word_unique"
                    examples.setdefault(verdict, {
                        "word": list(certificate[0]),
                        "matching_cells": [list(entry)
                                           for entry in certificate[1]],
                    })
                else:
                    verdict = "support_survivor"
                    survivors.add(tuple(sorted(extras)))
            tally[verdict] += 1

    expected = {
        "total": 5184,
        "residue_mixed_unique": 864,
        "six_site_purity_unique": 2400,
        "full_word_unique": 1872,
        "support_survivor": 48,
    }
    require(dict(tally) == expected,
            "minimal off-Sigma support-cover tally changed: %s" % tally)
    require(without_anchor_units == 1632,
            "anchor-factor dependency control changed")

    group = d1_group()
    representative = min(survivors)
    orbit = {
        tuple(sorted(map_cell(entry, mapping) for entry in representative))
        for mapping in group
    }
    require(orbit == survivors and len(orbit) == 48,
            "the residual signatures are not one 48-element orbit")
    expected_representative = (
        (0, 4, 1, 1), (1, 5, 1, 1),
        (2, 4, 0, 0), (3, 6, 0, 0),
        (5, 7, 0, 0), (6, 7, 1, 1),
    )
    require(representative == expected_representative,
            "the canonical minimal-support survivor changed: %s"
            % (representative,))
    return {"tally": dict(tally),
            "unique_full_word_example": examples["full_word_unique"],
            "without_anchor_factor_units": without_anchor_units,
            "anchor_factor_units_are_load_bearing_for": 240,
            "group_order": len(group),
            "survivor_orbits": 1,
            "representative_extras": [list(x) for x in representative]}, \
           representative


def polynomial_key(poly):
    return tuple(sorted((monomial, str(coefficient))
                        for monomial, coefficient in poly.items()))


def residual_search_input(sigma, representative):
    """Rebuild a conservative exact ideal input for the one residual orbit."""
    allowed = sigma | set(representative)
    blocks = D.sym_zero_blocks(SITES)
    for u, v, i, j in sorted(allowed):
        D.sym_put(blocks, u, v, i, j,
                  D.p_var("x_%d%d_%d%d" % (u, v, i, j)))

    generators = {}

    def add(poly, family):
        if D.p_is_zero(poly):
            return
        generators.setdefault(polynomial_key(poly), set()).add(family)

    for values in product(COLORS, repeat=8):
        word = dict(zip(SITES, values))
        target = D.p_const(1 if len(set(values)) == 1 else 0)
        add(D.p_sub(D.sym_matching_sum(blocks, SITES, word), target),
            "full_exactness")
    for domain in (W1, W2):
        for values in product(COLORS, repeat=6):
            word = dict(zip(domain, values))
            target = D.p_const(1 if set(values) == {2} else 0)
            add(D.p_sub(D.sym_matching_sum(blocks, domain, word), target),
                "lemma_F_six_site")
    for values in product(COLORS, repeat=4):
        word = dict(zip(RESIDUE, values))
        target = D.p_const(1 if set(values) == {2} else 0)
        add(D.p_sub(D.sym_matching_sum(blocks, RESIDUE, word), target),
            "residue_purity")

    for u, partner in sorted(D.D1_ESSENTIAL_PARTNER.items()):
        for size in (2, 4, 6, 8):
            for subset in combinations(SITES, size):
                if u in subset and partner not in subset:
                    add(D.sym_matching_sum(
                            blocks, subset, {site: 2 for site in subset}),
                        "a_pendant")

    h_residue = D.sym_matching_sum(
        blocks, RESIDUE, {site: 2 for site in RESIDUE})
    for u, partner in sorted(D.D1_ESSENTIAL_PARTNER.items()):
        left = D.p_mul(D.sym_cell(blocks, u, partner,
                                  D.CHI[u], D.CHI[partner]), h_residue)
        right = D.p_const(0)
        for r in RESIDUE:
            for rp in RESIDUE:
                if r == rp:
                    continue
                rest = tuple(site for site in RESIDUE
                             if site not in (r, rp))
                term = D.p_mul(
                    D.p_mul(D.sym_cell(blocks, u, r, D.CHI[u], 2),
                            D.sym_cell(blocks, partner, rp,
                                       D.CHI[partner], 2)),
                    D.sym_matching_sum(blocks, rest,
                                       {site: 2 for site in rest}),
                )
                right = D.p_add(right, term)
        add(D.p_add(left, right), "dagger")

    harm = D.p_sub(
        D.p_mul(D.sym_cell(blocks, 0, 2, 0, 1),
                D.sym_cell(blocks, 1, 3, 0, 1)),
        D.p_mul(D.sym_cell(blocks, 0, 1, 0, 0),
                D.sym_cell(blocks, 2, 3, 1, 1)),
    )
    add(harm, "D1_harm")

    family_counts = Counter()
    degree_term_counts = Counter()
    for key, families in generators.items():
        monomials = [monomial for monomial, _coefficient in key]
        degree = max((len(monomial) for monomial in monomials), default=0)
        degree_term_counts[(degree, len(key))] += 1
        for family in families:
            family_counts[family] += 1

    localization = set(representative) | set(BASE_UNITS) | {
        cell(0, 2, 2, 2), cell(1, 3, 2, 2),
    }
    require(len(allowed) == 95 and len(localization) == 12,
            "residual search input support/localization size changed")
    generator_digest = D.content_hash([
        [[list(monomial), coefficient] for monomial, coefficient in key]
        for key in sorted(generators)
    ])
    return {
        "field": "QQ (same combinatorial input over any field)",
        "variables": len(allowed),
        "allowed_support": "Sigma union representative_extras",
        "localize_nonzero_cells": [list(x) for x in sorted(localization)],
        "generator_count_after_deduplication": len(generators),
        "generator_family_memberships": dict(sorted(family_counts.items())),
        "degree_term_histogram": {
            "degree_%d_terms_%d" % key: value
            for key, value in sorted(degree_term_counts.items())
        },
        "generator_sha256": generator_digest,
        "scope": ("conservative exact D1 search input: full output, both "
                  "six-site purities, residue purity, a-pendant equations, "
                  "dagger, D1 harm, E1 by support, and the 12 open cells"),
    }


def audit():
    started = monotonic()
    _admissible, sigma, _off_sigma, kinds = reconstruct_support_domains()
    minimum = minimum_support_audit()
    cover, representative = support_cover_audit(sigma)
    search = residual_search_input(sigma, representative)
    ledger = {
        "pinned_D1_sha256": D1_SHA256,
        "domains": {"E1_admissible": 217, "Sigma": 89,
                    "off_Sigma": 128, "off_Sigma_kinds": dict(kinds)},
        "minimum": minimum,
        "minimal_six_cell_cover": cover,
        "residual_search_input": search,
        "proved": ("m >= 6; at m=6 exactly 5136 of 5184 labelled "
                   "anchor signatures are impossible and the remaining "
                   "48 are one symmetry orbit"),
        "open": ("emptiness of the one minimal-support orbit, every "
                 "off-Sigma support with m >= 7, and all higher orders"),
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "D1 minimal off-Sigma support-cover ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    tally = ledger["minimal_six_cell_cover"]["tally"]
    search = ledger["residual_search_input"]
    print("n8 D1 minimal off-Sigma support cover: PASS (exact)")
    print("support lower bound: m >= 6 outside Sigma")
    print("m=6: 5184 signatures = %d residue-purity + %d six-site-purity "
          "+ %d full-word kills + %d survivors"
          % (tally["residue_mixed_unique"],
             tally["six_site_purity_unique"], tally["full_word_unique"],
             tally["support_survivor"]))
    print("survivors: one 48-element D1-symmetry orbit")
    print("residual ideal input: %d variables, %d deduplicated generators, "
          "12 localized cells; sha256 %s"
          % (search["variables"], search["generator_count_after_deduplication"],
             search["generator_sha256"]))
    print("remaining: one m=6 orbit, all m>=7 supports, and all higher orders")
    print("sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
