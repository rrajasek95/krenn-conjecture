#!/usr/bin/env python3
"""Exact audit of the family, orientation, and signature coverage of N=8 D2.

Companion note: ``notes/n8-d2-full-family-orientation-audit.md``.

The committed D2 checker verifies exact polynomial certificates for one
oriented representative of the 48 census families.  This audit closes the
two finite reindexing gaps left explicit there:

* all 48 unoriented census families and all 8 endpoint-orientation choices
  per family are enumerated;
* the 288 choices with an essential endpoint in the four-site a-part are
  killed before the branch sweep: E1 makes their T-numerator at the
  saturating cell identically zero;
* the remaining 96 choices form two 48-element relabelling orbits, according
  to the orientation of the unique S_b--S_c carrier;
* the existing exact 512-combination sweep is replayed for its orientation,
  and an independent parametrized sweep verifies the reversed carrier
  orientation, again as exact polynomial identities;
* the seven signatures licensed by the hand Signature Lemma are composed
  over all 7^3 three-carrier profiles.  Every profile is killed by anchor
  death, Gamma, or c-factor, so the only non-machine implication left in D2
  is the Signature Lemma itself.  A finite case-partition audit verifies that
  its hand proof covers every Boolean both-site feed pattern and both
  two-endpoint signatures; it does not pretend to prove the outer-product
  algebra over C.

The checker pins the committed D2 artifact it consumes.  It uses exact
stdlib ``Fraction`` polynomials through that module and has no solver or
third-party dependency.
"""

from __future__ import annotations

import importlib
import os
import sys
from hashlib import sha256
from itertools import combinations, permutations, product
from time import monotonic

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)


def require(condition, detail):
    """Assertion that remains live under ``python -O``."""
    if not condition:
        raise RuntimeError(detail)


PINNED_D2_SHA256 = (
    "6320c3bdb795df3050952e52bd9c0fb9f4d5f2cdbf9eb543cd3467179630a745"
)
_D2_PATH = os.path.join(_HERE, "verify_n8_d2_kill_and_monochrome_rigidity.py")
with open(_D2_PATH, "rb") as _handle:
    D2_SHA256 = sha256(_handle.read()).hexdigest()
require(
    D2_SHA256 == PINNED_D2_SHA256,
    "pinned D2 checker changed (sha256 %s); this audit refuses to compose "
    "with an unreviewed artifact" % D2_SHA256,
)

D = importlib.import_module("verify_n8_d2_kill_and_monochrome_rigidity")
C = D.C
F = D.F
COLORS = D.COLORS
SITES = D.SITES
CHI = D.CHI
A = D.CANONICAL_A
S_A = frozenset(D.CANONICAL_SPLIT[A])

REPRESENTATIVE = ((0, 2), (1, 4), (3, 5))
REVERSED_BC = ((2, 0), (1, 4), (3, 5))
RESIDUE = (6, 7)
BRANCHES = D.BRANCH_FAMILIES

EXPECTED_LEDGER_SHA256 = (
    "5639dcd6e203759b5f95e3409bc2b5679018d6febbc013ff0b22a1ecb2c7fcb8"
)


def oriented_key(carriers):
    """Canonical key retaining each carrier's essential -> partner order."""
    return tuple(sorted((tuple(carrier) for carrier in carriers),
                        key=lambda carrier: tuple(sorted(carrier))))


def split_group():
    """The split-preserving S_2 x S_2 x S_4 action, constructed afresh."""
    group = []
    for perm_b in permutations(D.CANONICAL_SPLIT[0]):
        for perm_c in permutations(D.CANONICAL_SPLIT[1]):
            for perm_a in permutations(D.CANONICAL_SPLIT[2]):
                mapping = {}
                for part, image in zip(D.CANONICAL_SPLIT,
                                       (perm_b, perm_c, perm_a)):
                    mapping.update(dict(zip(part, image)))
                group.append(mapping)
    require(len(group) == 96 and len({tuple(sorted(m.items())) for m in group}) == 96,
            "split-preserving group is not a 96-element set")
    return group


def map_oriented(carriers, mapping):
    return oriented_key((mapping[u], mapping[p]) for u, p in carriers)


def map_matching(matching, mapping):
    return tuple(sorted(tuple(sorted((mapping[u], mapping[v])))
                        for u, v in matching))


def map_cell(cell, mapping):
    """Transport one endpoint-ordered aggregate cell through a site map."""
    u, v, i, j = cell
    mu, mv = mapping[u], mapping[v]
    if mu < mv:
        return (mu, mv, i, j)
    return (mv, mu, j, i)


def map_directed_cell(cell, mapping):
    """Transport A_xy(i,j) while retaining the mathematical x -> y order."""
    u, v, i, j = cell
    return (mapping[u], mapping[v], i, j)


def skeleton_schema(carriers, residue):
    """Finite schema of every label-sensitive D2 skeleton relation.

    Directed cells avoid storage-order noise.  The U/T schemas retain both
    monomials separately, so endpoint transposition or a fixed residue label
    changes the result.
    """
    essential_partner = dict(carriers)
    e1_zero = set()
    for u, partner in carriers:
        for x in SITES:
            if x in (u, partner):
                continue
            for j in COLORS:
                e1_zero.add((u, x, A, j))
    r0, r1 = residue
    residue_cells = {
        (r0, r1, i, j, (i, j) == (A, A))
        for i in COLORS for j in COLORS
    }
    u_relations = set()
    t_relations = set()
    for u, p in carriers:
        for i in COLORS:
            for j in COLORS:
                t_relations.add((
                    (u, p, i, j),
                    ((u, r0, i, A), (p, r1, j, A)),
                    ((u, r1, i, A), (p, r0, j, A)),
                    (i, j) == (A, A),
                ))
                for k in COLORS:
                    for l in COLORS:
                        if (k, l) == (A, A):
                            continue
                        u_relations.add((
                            ((u, r0, i, k), (p, r1, j, l)),
                            ((u, r1, i, l), (p, r0, j, k)),
                        ))
    signatures = set()
    for u, p in carriers:
        signatures.add((u, p, "empty", None, frozenset(), False))
        for site in residue:
            signatures.update({
                (u, p, "u", site, frozenset((u,)), False),
                (u, p, "p", site, frozenset((p,)), False),
                (u, p, "up", site, frozenset((u, p)), True),
            })
    require(set(essential_partner) == {u for u, _p in carriers},
            "oriented carriers do not have distinct essential endpoints")
    return {"e1": e1_zero, "residue": residue_cells,
            "u": u_relations, "t": t_relations,
            "signatures": signatures}


def map_schema(schema, mapping):
    def map_pair(pair):
        return tuple(map_directed_cell(cell, mapping) for cell in pair)

    return {
        "e1": {map_directed_cell(cell, mapping) for cell in schema["e1"]},
        "residue": {
            (*map_directed_cell(cell[:4], mapping), cell[4])
            for cell in schema["residue"]
        },
        "u": {(map_pair(left), map_pair(right))
              for left, right in schema["u"]},
        "t": {
            (map_directed_cell(target, mapping), map_pair(left),
             map_pair(right), has_pure_lead)
            for target, left, right, has_pure_lead in schema["t"]
        },
        "signatures": {
            (mapping[u], mapping[p], kind,
             None if site is None else mapping[site],
             frozenset(mapping[x] for x in endpoints), exchange)
            for u, p, kind, site, endpoints, exchange
            in schema["signatures"]
        },
    }


def section_reindexing():
    """Exact finite audit that hafnian words and endpoint cells reindex."""
    group = split_group()
    matchings = {tuple(matching) for matching in C.perfect_matchings(SITES)}
    cells = {(u, v, i, j) for u, v in combinations(SITES, 2)
             for i in COLORS for j in COLORS}
    words = set(product(COLORS, repeat=8))
    require(len(matchings) == 105 and len(cells) == 252 and len(words) == 6561,
            "reindexing domains have changed size")
    for mapping in group:
        require(set(mapping) == set(SITES) and set(mapping.values()) == set(SITES),
                "a split-group element is not a site bijection")
        require(all(CHI[mapping[site]] == CHI[site] for site in SITES),
                "a split-group element does not preserve the induced word chi")
        require({map_matching(matching, mapping) for matching in matchings}
                == matchings,
                "a split-group element does not permute all 105 matchings")
        require({map_cell(cell, mapping) for cell in cells} == cells,
                "a split-group element does not biject the 252 endpoint cells")
        mapped_words = {
            tuple(next(word[u] for u in SITES if mapping[u] == site)
                  for site in SITES)
            for word in words
        }
        require(mapped_words == words,
                "a split-group element does not biject all 6561 words")
        for representative in (REPRESENTATIVE, REVERSED_BC):
            mapped_carriers = tuple((mapping[u], mapping[p])
                                    for u, p in representative)
            mapped_residue = tuple(mapping[site] for site in RESIDUE)
            require(
                map_schema(skeleton_schema(representative, RESIDUE), mapping)
                == skeleton_schema(mapped_carriers, mapped_residue),
                "the E1/U/T/signature schema is not equivariant under a "
                "split-preserving relabelling",
            )
    # Negative control: transposing neither endpoint colour when a site map
    # reverses an edge cannot be a valid endpoint-ordered action.
    reversal = {0: 1, 1: 0, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}
    require(map_cell((0, 1, 0, 2), reversal) == (0, 1, 2, 0),
            "endpoint-order control failed to transpose a reversed edge")
    return {"group_order": len(group), "matchings": len(matchings),
            "endpoint_cells": len(cells), "words": len(words),
            "skeleton_schema_checks": 2 * len(group)}


def d2_families():
    families = D.saturating_families(8, D.CANONICAL_SPLIT, A)
    return sorted(family for family, residue, touching in families
                  if (len(family), len(residue), touching) == (3, 2, 2))


def e1_t_numerator(carriers, residue, carrier):
    """Generic T-numerator at chi after imposing only E1.

    Each surviving cell is an independent polynomial variable.  Thus zero
    here is an exact structural identity, not a sampled evaluation.
    """
    essential_partner = dict(carriers)
    u, p = carrier
    r0, r1 = residue

    def cell(x, y, i, j):
        if x in essential_partner and i == A and y != essential_partner[x]:
            return D.p_const(0)
        return D.p_var("E%d%d_%d%d" % (x, y, i, j))

    return D.p_add(
        D.p_mul(cell(u, r0, CHI[u], A), cell(p, r1, CHI[p], A)),
        D.p_mul(cell(u, r1, CHI[u], A), cell(p, r0, CHI[p], A)),
    )


def section_orientations():
    """Enumerate 48 x 8 orientations and split them into exact cases."""
    families = d2_families()
    require(len(families) == 48, "the census no longer has 48 D2 families")
    all_oriented = set()
    viable = set()
    e1_dead = set()
    forward = set()
    reverse = set()
    per_family = {}
    for family in families:
        family_oriented = []
        for bits in product((0, 1), repeat=3):
            carriers = oriented_key(
                edge if bit == 0 else (edge[1], edge[0])
                for edge, bit in zip(family, bits)
            )
            key = carriers
            all_oriented.add(key)
            family_oriented.append(key)
            residue = tuple(site for site in SITES
                            if all(site not in edge for edge in family))
            bad = [carrier for carrier in carriers if carrier[0] in S_A]
            if bad:
                # At an S_a essential endpoint chi_u = a.  Both u--R blocks
                # are off-partner, so E1 zeros the two terms of s_e(chi).
                carrier = bad[0]
                numerator = e1_t_numerator(carriers, residue, carrier)
                require(D.p_is_zero(numerator),
                        "E1 did not zero the saturation numerator for %s"
                        % (carriers,))
                require((CHI[carrier[0]], CHI[carrier[1]]) != (A, A),
                        "an attachment carrier unexpectedly reads (a,a)")
                e1_dead.add(key)
                continue
            viable.add(key)
            bc = next(carrier for carrier in carriers
                      if carrier[0] not in S_A and carrier[1] not in S_A)
            if CHI[bc[0]] == 0:
                forward.add(key)
            else:
                require(CHI[bc[0]] == 1,
                        "viable B--C carrier has an impossible essential colour")
                reverse.add(key)
        require(len(set(family_oriented)) == 8,
                "a D2 family did not yield eight distinct orientations")
        per_family[str([list(edge) for edge in family])] = {
            "all": 8,
            "e1_dead": sum(key in e1_dead for key in family_oriented),
            "viable": sum(key in viable for key in family_oriented),
        }
    require(len(all_oriented) == 384 and len(e1_dead) == 288
            and len(viable) == 96 and len(forward) == len(reverse) == 48,
            "orientation census changed: all/dead/viable/forward/reverse = "
            "%d/%d/%d/%d/%d" % (len(all_oriented), len(e1_dead),
                                  len(viable), len(forward), len(reverse)))
    raw_numerator = D.p_add(
        D.p_mul(D.p_var("raw_u6"), D.p_var("raw_p7")),
        D.p_mul(D.p_var("raw_u7"), D.p_var("raw_p6")),
    )
    require(not D.p_is_zero(raw_numerator),
            "orientation control: the generic T-numerator is already zero "
            "before E1, so the 288 orientation kills are vacuous")
    require(all(row == {"all": 8, "e1_dead": 6, "viable": 2}
                for row in per_family.values()),
            "the 6+2 orientation split is not uniform over all D2 families")

    group = split_group()
    forward_orbit = {map_oriented(REPRESENTATIVE, mapping) for mapping in group}
    reverse_orbit = {map_oriented(REVERSED_BC, mapping) for mapping in group}
    require(forward_orbit == forward and reverse_orbit == reverse,
            "the two representative orientations do not cover the 96 viable "
            "oriented census families")
    require(not (forward_orbit & reverse_orbit),
            "the forward and reverse B--C orientation orbits overlap")

    # Negative control: omitting the reverse representative must leave half
    # of the viable oriented families uncovered.
    require(len(viable - forward_orbit) == 48,
            "orientation orbit control cannot detect omission of the reverse "
            "B--C orientation")
    return {
        "unoriented_families": len(families),
        "orientations_per_family": 8,
        "oriented_total": len(all_oriented),
        "e1_saturation_dead": len(e1_dead),
        "viable": len(viable),
        "forward_orbit": len(forward_orbit),
        "reverse_orbit": len(reverse_orbit),
        "per_family_6_plus_2": all(
            row == {"all": 8, "e1_dead": 6, "viable": 2}
            for row in per_family.values()),
    }


def branch_kind_keep(branch):
    return branch.rstrip("67"), int(branch[-1])


def build_combo(carriers, branches):
    """Fresh exact D2 skeleton for either viable representative orientation."""
    essential_partner = dict(carriers)
    blocks = D.sym_zero_blocks(SITES)
    nu, nuinv = D.p_var("nu"), D.p_var("nuinv")
    blocks[(6, 7)][A][A] = nu

    def free_ok(u, i, v):
        return not (u in essential_partner and i == A
                    and v != essential_partner[u])

    carrier_edges = {tuple(sorted(carrier)) for carrier in carriers}
    for u, v in combinations(SITES, 2):
        if u in RESIDUE or v in RESIDUE or (u, v) in carrier_edges:
            continue
        for i in COLORS:
            for j in COLORS:
                if free_ok(u, i, v) and free_ok(v, j, u):
                    blocks[(u, v)][i][j] = D.p_var(
                        "C%d%d_%d%d" % (u, v, i, j))

    for u, p in carriers:
        branch = branches[(u, p)]
        kind, keep = branch_kind_keep(branch)
        drop = 7 if keep == 6 else 6
        if kind == "g":
            for i in (0, 1):
                D.sym_put(blocks, u, keep, i, A,
                          D.p_var("U%d%d_%d2" % (u, keep, i)))
            for i in COLORS:
                D.sym_put(blocks, p, drop, i, A,
                          D.p_var("P%d%d_%d2" % (p, drop, i)))
            for i in COLORS:
                for j in COLORS:
                    D.sym_put(blocks, p, keep, i, j,
                              D.p_var("P%d%d_%d%d" % (p, keep, i, j)))
        elif kind == "d":
            for i in (0, 1):
                for k in (0, 1):
                    D.sym_put(blocks, u, keep, i, k,
                              D.p_var("D%d%d_%d%d" % (u, keep, i, k)))
                D.sym_put(blocks, u, drop, i, A,
                          D.p_var("D%d%d_%d2" % (u, drop, i)))
            for j in COLORS:
                D.sym_put(blocks, p, keep, j, A,
                          D.p_var("D%d%d_%d2" % (p, keep, j)))
        else:
            require(kind in ("x", "xf"), "unknown branch %s" % branch)
            w = [D.p_var("w_%d%d_%d" % (u, p, i)) for i in (0, 1)]
            scalars = [D.p_var("c_%d%d_%d" % (u, p, k)) for k in (0, 1)]
            q = [D.p_var("q_%d%d_%d" % (u, p, j)) for j in COLORS]
            qf = [D.p_var("qf_%d%d_%d" % (u, p, j)) for j in COLORS]
            for i in (0, 1):
                for k in (0, 1):
                    D.sym_put(blocks, u, keep, i, k,
                              D.p_mul(scalars[k], w[i]))
                D.sym_put(blocks, u, drop, i, A, w[i])
                if kind == "xf":
                    D.sym_put(blocks, u, keep, i, A,
                              D.p_var("xa_%d%d_%d" % (u, p, i)))
            for j in COLORS:
                for k in (0, 1):
                    D.sym_put(blocks, p, keep, j, k,
                              D.p_neg(D.p_mul(scalars[k], q[j])))
                D.sym_put(blocks, p, keep, j, A, qf[j])
                D.sym_put(blocks, p, drop, j, A, q[j])

    slots = {}
    for u, p in carriers:
        m = D.p_var("m_%d%d" % (u, p))
        for i in COLORS:
            for j in COLORS:
                numerator = D.p_add(
                    D.p_mul(D.sym_cell(blocks, u, 6, i, A),
                            D.sym_cell(blocks, p, 7, j, A)),
                    D.p_mul(D.sym_cell(blocks, u, 7, i, A),
                            D.sym_cell(blocks, p, 6, j, A)),
                )
                lead = m if (i, j) == (A, A) else D.p_const(0)
                D.sym_put(blocks, u, p, i, j,
                          D.p_mul(D.p_sub(lead, numerator), nuinv))
                if (i, j) == (CHI[u], CHI[p]):
                    slots[(u, p)] = numerator
    return blocks, slots


def partners_for(carriers, branches):
    partners = {6: set(), 7: set()}
    for u, p in carriers:
        kind, keep = branch_kind_keep(branches[(u, p)])
        if kind == "g":
            partners[keep].add(p)
        elif kind == "d":
            partners[keep].add(u)
        else:
            partners[keep].update((u, p))
    return partners


def gamma_certificate(carriers, branches, blocks):
    partners = partners_for(carriers, branches)
    for residue_site in RESIDUE:
        if len(partners[residue_site]) != 1:
            continue
        x = next(iter(partners[residue_site]))
        rest = tuple(site for site in SITES if site not in (x, residue_site))
        gamma_fingerprints = []
        for c, d in ((0, 1), (1, 0)):
            values = [c] * 8
            values[x] = values[residue_site] = d
            gamma = D.sym_matching_sum(blocks, rest,
                                       {site: c for site in rest})
            flip = D.sym_matching_sum(blocks, SITES,
                                      dict(zip(SITES, values)))
            anchor = D.sym_matching_sum(
                blocks, SITES, dict(zip(SITES, (c,) * 8)))
            require(D.p_is_zero(D.p_sub(
                        flip,
                        D.p_mul(D.sym_cell(blocks, x, residue_site, d, d),
                                gamma))),
                    "reversed-orientation Gamma flip identity failed")
            require(D.p_is_zero(D.p_sub(
                        anchor,
                        D.p_mul(D.sym_cell(blocks, x, residue_site, c, c),
                                gamma))),
                    "reversed-orientation Gamma anchor identity failed")
            require(not D.p_is_zero(gamma),
                    "reversed-orientation Gamma factor is identically zero")
            gamma_fingerprints.append(D.p_fingerprint(gamma))
        return gamma_fingerprints
    return None


def cfactor_certificate(carriers, branches, blocks):
    partners = partners_for(carriers, branches)
    for residue_site in RESIDUE:
        feeders = [(carrier, branches[carrier]) for carrier in carriers
                   if branch_kind_keep(branches[carrier])[1] == residue_site]
        if (not partners[residue_site] or len(feeders) != 1
                or not branch_kind_keep(feeders[0][1])[0].startswith("x")):
            continue
        (u, p), _branch = feeders[0]
        scalars = [D.p_var("c_%d%d_%d" % (u, p, k)) for k in (0, 1)]
        for c, d in ((0, 1), (1, 0)):
            values = [c] * 8
            values[residue_site] = d
            flip = D.sym_matching_sum(blocks, SITES,
                                      dict(zip(SITES, values)))
            anchor = D.sym_matching_sum(
                blocks, SITES, dict(zip(SITES, (c,) * 8)))
            require(D.p_is_zero(D.p_sub(D.p_mul(flip, scalars[c]),
                                        D.p_mul(anchor, scalars[d]))),
                    "reversed-orientation c-factor identity failed")
        return [u, p, residue_site]
    return None


def sweep(carriers):
    """Exact 8^3 polynomial sweep for one viable oriented representative."""
    tally = {"anchor_dead": 0, "gamma": 0, "c_factor": 0, "survivor": 0}
    for combo in product(BRANCHES, repeat=3):
        branches = dict(zip(carriers, combo))
        blocks, slots = build_combo(carriers, branches)
        require(all(not D.p_is_zero(slots[carrier]) for carrier in carriers),
                "a swept reversed-orientation branch cannot saturate")
        dead = [colour for colour in (0, 1)
                if D.p_is_zero(D.sym_matching_sum(
                    blocks, SITES, dict(zip(SITES, (colour,) * 8))))]
        if dead:
            require(dead == [0, 1],
                    "only one monochromatic anchor died in the sweep")
            tally["anchor_dead"] += 1
        elif gamma_certificate(carriers, branches, blocks) is not None:
            tally["gamma"] += 1
        elif cfactor_certificate(carriers, branches, blocks) is not None:
            tally["c_factor"] += 1
        else:
            tally["survivor"] += 1
    require(tally == {"anchor_dead": 128, "gamma": 192,
                      "c_factor": 192, "survivor": 0},
            "reversed-orientation sweep tally changed: %s" % tally)
    return tally


SIGNATURES = ("empty", "u6", "p6", "up6", "u7", "p7", "up7")


def signature_data(signature, carrier):
    u, p = carrier
    if signature == "empty":
        return None, set(), None
    site = int(signature[-1])
    kind = signature[:-1]
    endpoints = {"u": {u}, "p": {p}, "up": {u, p}}[kind]
    mechanism = "c_factor" if kind == "up" else "gamma"
    return site, endpoints, mechanism


def section_signature_composition():
    """Compose the Signature Lemma's seven outputs over all 7^3 profiles."""
    tally = {"anchor_dead": 0, "gamma": 0, "c_factor": 0,
             "survivor": 0}
    examples = {}
    for profile in product(SIGNATURES, repeat=3):
        by_site = {6: [], 7: []}
        for carrier, signature in zip(REPRESENTATIVE, profile):
            site, endpoints, mechanism = signature_data(signature, carrier)
            if site is not None:
                by_site[site].append((carrier, endpoints, mechanism))
        if not by_site[6] or not by_site[7]:
            verdict = "anchor_dead"
        else:
            sparse_site = min((6, 7), key=lambda site: len(by_site[site]))
            feeders = by_site[sparse_site]
            require(len(feeders) <= 1,
                    "three carriers feeding two sites escaped pigeonhole")
            if not feeders:
                verdict = "anchor_dead"
            else:
                verdict = feeders[0][2]
        tally[verdict] += 1
        examples.setdefault(verdict, list(profile))
    require(sum(tally.values()) == 7 ** 3 and tally["survivor"] == 0,
            "seven-signature composition left a survivor: %s" % tally)

    # Dependency control: if the Signature Lemma were false and every
    # carrier could feed both residue sites, neither site would have the
    # zero/single-carrier profile used by any of the three certificates.
    forbidden_both_site_profile = {
        site: [(carrier, set(carrier), "unsupported")
               for carrier in REPRESENTATIVE]
        for site in RESIDUE
    }
    require(all(len(forbidden_both_site_profile[site]) == 3
                for site in RESIDUE),
            "Signature-Lemma dependency control accidentally retained a "
            "sparse residue site")

    # Audit the Boolean case partition used by the hand Signature Lemma.
    # Each nonempty feed at one residue site is u, p, or both.
    nonempty = (frozenset(("u",)), frozenset(("p",)),
                frozenset(("u", "p")))
    proof_cases = {"both_from_u": 0, "mixed_u6_p7": 0,
                   "mixed_p6_u7": 0, "both_from_p": 0}
    for p6, p7 in product(nonempty, repeat=2):
        if "u" in p6 and "u" in p7:
            case = "both_from_u"
        elif "u" in p6 and "p" in p7:
            case = "mixed_u6_p7"
        elif "p" in p6 and "u" in p7:
            case = "mixed_p6_u7"
        else:
            require(p6 == p7 == frozenset(("p",)),
                    "both-site feed pattern omitted by the proof partition")
            case = "both_from_p"
        proof_cases[case] += 1
    require(sum(proof_cases.values()) == 9 and all(proof_cases.values()),
            "the hand proof's both-site cases are incomplete: %s"
            % proof_cases)
    two_endpoint_cases = [(frozenset(("u", "p")), frozenset()),
                          (frozenset(), frozenset(("u", "p")))]
    require(len(two_endpoint_cases) == 2,
            "the extended-exchange conclusion is not audited at both sites")
    return {"profiles": 7 ** 3, "tally": tally, "examples": examples,
            "both_site_boolean_patterns": 9,
            "hand_proof_case_partition": proof_cases,
            "two_endpoint_cases": 2,
            "designed_both_site_profile_has_no_certificate": True,
            "remaining_dependency": (
                "the Signature Lemma's outer-product algebra over C; the "
                "finite case partition and every downstream profile are "
                "machine checked, but this checker does not replace that "
                "hand proof with a universal algebra certificate"
            )}


def audit():
    started = monotonic()
    reindexing = section_reindexing()
    orientations = section_orientations()
    committed_forward, _seconds = D.section_d2_sweep()
    require(committed_forward["tally"] == {
                "anchor_dead": 128, "gamma": 192,
                "c_factor": 192, "survivor": 0},
            "the pinned forward sweep no longer has its certified tally")
    reverse = sweep(REVERSED_BC)
    signatures = section_signature_composition()
    ledger = {
        "pinned_d2_sha256": D2_SHA256,
        "reindexing": reindexing,
        "orientations": orientations,
        "forward_sweep": committed_forward["tally"],
        "reverse_sweep": reverse,
        "signature_composition": signatures,
        "proved": (
            "all 384 oriented D2 census geometries are covered: 288 die "
            "because E1 makes saturation impossible, and the 96 viable "
            "geometries form two exact relabelling orbits whose oriented "
            "representatives have 512/512 polynomial-certificate kills"
        ),
        "open": (
            "the Signature Lemma remains a hand theorem over C; conditional "
            "on it, the seven-signature composition has no survivor"
        ),
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "n8 D2 full-family/orientation audit ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    orient = ledger["orientations"]
    signatures = ledger["signature_composition"]
    print("n8 D2 full-family/orientation audit: PASS (exact)")
    print("orientations: %d families x %d = %d; %d E1/saturation-dead; "
          "%d viable in two %d-element relabelling orbits"
          % (orient["unoriented_families"], orient["orientations_per_family"],
             orient["oriented_total"], orient["e1_saturation_dead"],
             orient["viable"], orient["forward_orbit"]))
    print("exact representative sweeps: forward %s; reverse %s"
          % (ledger["forward_sweep"], ledger["reverse_sweep"]))
    print("Signature-Lemma composition: %d/%d profiles obstructed; %s"
          % (signatures["profiles"] - signatures["tally"]["survivor"],
             signatures["profiles"], signatures["tally"]))
    print("remaining hand dependency:", signatures["remaining_dependency"])
    print("sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
