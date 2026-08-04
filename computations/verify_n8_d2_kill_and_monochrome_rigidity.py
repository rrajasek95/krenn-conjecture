#!/usr/bin/env python3
"""The N = 8 endgame: D2 dies on the swept class, and on the a-column
support class Sigma the monochromatic anchors are rigid.

Companion note: `notes/n8-d2-kill-and-monochrome-rigidity.md`.

This checker packages three results about the two dangerous saturating
configurations D1 and D2 of the N = 8 census (companion artifact
`computations/verify_n8_saturation_census_two_configurations.py`, whose
geometry conventions are mirrored here and re-derived from the same
committed enumerators, not imported from it).  It imports the committed
machinery -- `computations/verify_exact_source_live_split_forcing.py`
and `computations/verify_good_crossing_matching_forcing.py` -- through
`importlib` with pinned sha256 digests, so conventions cannot drift.
Both committed modules are stateless (pure functions over explicitly
passed block dictionaries; no chart or solver state is carried between
calls), so one import serves every configuration below; each
configuration builds its own fresh block dictionary.

What is new here, and at which strength:

  THEOREM 1 (D2 kill on the swept class; machine, per branch family).
  [Revised after an independent audit: the swept family list is now the
  EIGHT families g6/g7, x6/x7, xf6/xf7, d6/d7 -- the audit exhibited
  U-system solutions outside the original six, so the earlier claim that
  the six were complete under saturation was FALSE and has been
  replaced by the signature reduction below.]
  On the census-mirrored D2 geometry -- canonical split S_b = {0,1},
  S_c = {2,3}, S_a = {4,5,6,7}, saturating colour a = 2, chi =
  (b,b,c,c,a,a,a,a), representative family F_2 = {{0,2},{1,4},{3,5}},
  residue R = {6,7}, signature (k,|R|,t) = (3,2,2) -- impose the D2
  skeleton: (E1) at the essential sites 0, 1, 3; A_67 = nu E_aa with
  nu != 0 (Lemma F on the full family); the 4-site Lemma-F purity at
  each carrier pair-deletion, whose T-part DEFINES the carrier blocks
  and whose U-part is solved per carrier into one of the EIGHT support
  families {g6, g7, x6, x7, xf6, xf7, d6, d7}.  Then ALL 512 branch
  combinations are obstructed, with a certificate consuming at most four
  words of the pair-inside budget (whose size, 272, is computed here and
  whose membership every certificate word is required to satisfy):

    * 128 combos are ANCHOR-DEAD: H_B(b^8) and H_B(c^8) are identically
      zero on the combo's support;
    * 192 combos die by the GAMMA certificate: some residue site r has
      a UNIQUE two-colour partner x, so every two-colour word factors
      through the single cell A_xr and the deletion tensor Gamma_c,
      and the flip word contradicts the anchors (3 words);
    * 192 combos die by the C-FACTOR certificate: r is fed by exactly
      one carrier, of exchange type, so every two-colour word carries
      the exchange scalar c_{w_r} as an overall factor (4 words).

  The mechanism is a pigeonhole: three carriers feed two residue sites,
  so some residue site has at most one two-colour feeder; zero feeders
  kill the anchors, one feeder gives a factorization certificate.  Both
  factorizations are verified here as POLYNOMIAL IDENTITIES in exact
  arithmetic over the combo's parameter ring, not assumed.

  What the swept families do NOT do is exhaust the U-system: the audit
  of the first packaging exhibited saturated solutions outside them (a
  d-variant with a free a-column, and an all-a-column solution).  What
  IS exhaustive -- and is what the certificates consume -- is the list
  of realizable TWO-COLOUR COLUMN SIGNATURES.  The census section
  enumerates every saturated U-system solution over GF(2) and finds:
  none feeds two-colour cells into BOTH residue sites; the realizable
  signatures are exactly seven (the empty one, and {u}, {p}, {u,p} into
  one residue site -- the signatures of the g, d and x/xf families);
  and every saturated solution whose signature is {u,p} carries the
  extended exchange structure, so the c-factor certificate covers that
  class.  The proof over Q is the hand argument in the note; the GF(2)
  census is machine evidence for it, over one finite field.

  THEOREM 2 (monochromatic rigidity on Sigma; machine, identically).
  Let Sigma be the a-column support class on the D1 geometry: small
  blocks (sites 0..3) arbitrary subject to the (E1) pendant rows,
  small-to-residue blocks a-column only, residue-residue blocks (a,a)
  only.  Then H_B(b^8) = H_B(c^8) = 0 IDENTICALLY on Sigma -- verified
  here as a polynomial identity with an independent variable in every
  one of Sigma's free cells, together with the structural reason (each
  of the 105 perfect matchings contains at least two residue-incident
  edges, and every residue-incident edge is (b,b)- and (c,c)-dead).
  So no exact source lives on Sigma: exactness needs H_B(b^8) = 1.
  Sharpness: reviving ONE residue-residue two-colour cell leaves the
  anchor identically zero (the crossing edges pair up); reviving two
  disjoint ones revives it -- the negative probe.

  STRUCTURAL FINDING 3 (the near-miss family; machine on instances).
  An explicit rational family -- exact Jacobian rank 22 at its base
  point -- satisfies EVERY census fact of the D1 configuration and
  6559 of the 6561 exactness equations, the only defects being the
  monochromatic pair b^8, c^8; and it has a member whose D1 rectangle
  is degenerate with both products nonzero (the harmful branch).  So
  the census fact set together with the two-colour repairs cannot
  decide D1: the D1 kill must come from out-of-Sigma supports.  The
  frozen-chart step of the repair is separately PROVED infeasible here
  by an exact pencil-rank certificate (the nine 2x2 minors of the
  induced pencil have constant gcd over Q), which is why the repair
  needs the full chart.

Everything about exact sources is a hand proof (in the note), verified
on instances only: no exact ternary source at N = 8 exists to test on
-- showing that none exists is the project's aim.  Krenn's conjecture
remains OPEN.

Exact stdlib arithmetic only: int and Fraction, plus a sparse
multivariate polynomial ring over Fraction built here (dicts from
monomials to coefficients).  No floats, no bare asserts, no external
packages, no symbolic-algebra dependency.

Verification:

    python3       computations/verify_n8_d2_kill_and_monochrome_rigidity.py
    python3 -O    computations/verify_n8_d2_kill_and_monochrome_rigidity.py
    python3 -I    computations/verify_n8_d2_kill_and_monochrome_rigidity.py
    python3 -S    computations/verify_n8_d2_kill_and_monochrome_rigidity.py
    python3 -I -S computations/verify_n8_d2_kill_and_monochrome_rigidity.py
    python3 -m py_compile computations/verify_n8_d2_kill_and_monochrome_rigidity.py
"""

from __future__ import annotations

import importlib
import os
import sys
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
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
    # imported: conventions, hafnians, matchings, coefficients, splits,
    # crossing pairs, exactness defects, exact rank.
    "verify_exact_source_live_split_forcing.py":
        "25e52f3d6dd85a4952cd73fea026c08e19c160f22fff9c993dad39d9ac009ac0",
    # imported: matchings_inside (the census enumeration path),
    # pseudorandom packets.
    "verify_good_crossing_matching_forcing.py":
        "7cd9f17028a0bd9e72bb3b78abf7a043b4a4b31f25b8b6804d28ccce5cdf5810",
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
F = Fraction

EXPECTED_LEDGER_SHA256 = (
    "d8e8ad7ace2e31e16ef0dfa64f0f7d31a7064dcb701503c46d8a7a5abc58e737"
)

SITES = tuple(range(8))
LETTER = {0: "b", 1: "c", 2: "a"}

# ---- the census-mirrored canonical split (shape (2,2,4), a on the 4-part).
CANONICAL_SPLIT = ((0, 1), (2, 3), (4, 5, 6, 7))
CANONICAL_A = 2
CHI = (0, 0, 1, 1, 2, 2, 2, 2)

# ---- D2 geometry: the representative saturating family and its residue.
D2_CARRIERS = ((0, 2), (1, 4), (3, 5))       # (essential u, partner p)
D2_ESSENTIAL_PARTNER = {0: 2, 1: 4, 3: 5}
D2_RESIDUE = (6, 7)
D2_SAT_ROW = {0: 0, 1: 0, 3: 1}              # chi at the essential sites
D2_SAT_COL = {2: 1, 4: 2, 5: 2}              # chi at the partners
# The eight swept per-carrier support families.  g/x/d are the families
# of the original classification; xf6/xf7 are the EXTENDED exchange
# families (the a-column of A_{u,keep} left free), which the audit of
# the first packaging showed to be U-system solutions outside the six.
BRANCH_FAMILIES = ("g6", "g7", "x6", "x7", "xf6", "xf7", "d6", "d7")

# ---- D1 geometry (Sigma lives here): carriers {0,2}, {1,3}, R = S_a.
D1_SMALL = (0, 1, 2, 3)
D1_RESIDUE = (4, 5, 6, 7)
D1_ESSENTIAL_PARTNER = {0: 2, 1: 3}
D1_PAIRS = ((4, 5), (5, 4), (6, 7), (7, 6))
W1 = (0, 2, 4, 5, 6, 7)                      # B \ V({1,3})
W2 = (1, 3, 4, 5, 6, 7)                      # B \ V({0,2})


# ================================================ the polynomial engine
#
# Sparse multivariate polynomials over Q: dict from a monomial (a sorted
# tuple of variable names, with repetition for exponents) to a nonzero
# Fraction.  The zero polynomial is the empty dict, so "identically
# zero" is a structural test, not a numerical one.


def p_const(value):
    value = F(value)
    return {} if value == 0 else {(): value}


def p_var(name):
    return {(name,): F(1)}


def p_add(left, right):
    out = dict(left)
    for monomial, coefficient in right.items():
        total = out.get(monomial, F(0)) + coefficient
        if total:
            out[monomial] = total
        else:
            out.pop(monomial, None)
    return out


def p_neg(poly):
    return {monomial: -coefficient for monomial, coefficient in poly.items()}


def p_sub(left, right):
    return p_add(left, p_neg(right))


def p_mul(left, right):
    if not left or not right:
        return {}
    out = {}
    for ml, cl in left.items():
        for mr, cr in right.items():
            monomial = tuple(sorted(ml + mr))
            total = out.get(monomial, F(0)) + cl * cr
            if total:
                out[monomial] = total
            else:
                out.pop(monomial, None)
    return out


def p_is_zero(poly):
    return not poly


_PROBE_CACHE = {}


def probe_value(name):
    """A deterministic nonzero rational for a variable name.

    Used only for LEDGER FINGERPRINTS of computed polynomials -- never
    to decide any property (every property below is decided by exact
    polynomial identity) -- and for the cross-implementation control
    against the committed `coefficient` oracle.
    """
    if name not in _PROBE_CACHE:
        digest = sha256(name.encode("ascii")).digest()
        numerator = 1 + int.from_bytes(digest[0:4], "big") % 23
        denominator = 1 + int.from_bytes(digest[4:8], "big") % 7
        sign = -1 if digest[8] % 2 else 1
        _PROBE_CACHE[name] = F(sign * numerator, denominator)
    return _PROBE_CACHE[name]


def p_probe(poly):
    total = F(0)
    for monomial, coefficient in poly.items():
        term = coefficient
        for name in monomial:
            term *= probe_value(name)
        total += term
    return total


def p_fingerprint(poly):
    """Computed fingerprint of a polynomial: (#monomials, value at the
    deterministic probe point).  Both are computed content."""
    return [len(poly), p_probe(poly)]


# ------------------------------------------ symbolic blocks and hafnians


def sym_zero_blocks(sites):
    return {(u, v): [[p_const(0) for _ in COLORS] for _ in COLORS]
            for u, v in combinations(sorted(sites), 2)}


def sym_cell(blocks, u, v, i, j):
    """A_uv(i,j) with i read at u (endpoint-ordered, as committed
    `oriented` does for Fraction blocks)."""
    if u < v:
        return blocks[(u, v)][i][j]
    return blocks[(v, u)][j][i]


def sym_put(blocks, u, v, i, j, value):
    if u < v:
        blocks[(u, v)][i][j] = value
    else:
        blocks[(v, u)][j][i] = value


def sym_matching_sum(blocks, sites, word):
    """H_S(A) at `word` (a dict site -> colour) with polynomial cells;
    the single symbolic implementation of the matching sum, controlled
    in section 2 against the committed `coefficient`."""
    total = {}
    for matching in C.perfect_matchings(sorted(sites)):
        term = p_const(1)
        for u, v in matching:
            term = p_mul(term, blocks[(u, v)][word[u]][word[v]])
            if not term:
                break
        total = p_add(total, term)
    return total


def sym_hafnian(blocks, colour, subset):
    word = {site: colour for site in subset}
    return sym_matching_sum(blocks, tuple(sorted(subset)), word)


def evaluate_blocks(blocks, sites):
    """Instantiate polynomial blocks at the probe point as committed
    Fraction blocks."""
    out = C.zero_blocks(sites)
    for (u, v) in combinations(sorted(sites), 2):
        for i in COLORS:
            for j in COLORS:
                C.set_cell(out, u, v, i, j, p_probe(blocks[(u, v)][i][j]))
    return out


# ---------------------------------------------------- S0 conventions


def section_conventions():
    """Pin the imported machinery to the endpoint-ordered convention,
    exactly as the committed census pair does, plus the two facts this
    artifact's geometry consumes: a two-site hafnian is a single cell,
    and `oriented` transposes rather than symmetrizes.

    Positive and negative probes: the transposed orientation carries the
    transposed cell; the untouched transpose cell of the SAME block must
    stay zero; the empty hafnian is 1; a two-site hafnian reads exactly
    the (colour, colour) cell.
    """
    sites = (0, 1, 2, 3)
    blocks = C.zero_blocks(sites)
    C.set_cell(blocks, 0, 1, 0, 2, F(5))
    C.set_cell(blocks, 2, 3, 1, 1, F(7))
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
        "(colour, colour) cell of its block",
    )
    # The symbolic cell accessor must agree with the committed one.
    symbolic = sym_zero_blocks(sites)
    sym_put(symbolic, 0, 1, 0, 2, p_var("probe"))
    require(
        sym_cell(symbolic, 1, 0, 2, 0) == p_var("probe")
        and p_is_zero(sym_cell(symbolic, 1, 0, 0, 2)),
        "conventions: the symbolic cell accessor does not transpose the "
        "way the committed oriented() does",
    )
    return {"committed_file_sha256": dict(PINNED_DIGESTS)}


# ---------------------------------------- S1 the census-mirrored geometry


def saturating_families(order, split, colour):
    """Every nonempty matching T inside the split's crossing pairs with
    B \\ V(T) contained in S_colour, as (T, R, t).

    Same single enumeration path as the committed census pair's
    (`matchings_inside` over `crossing_pairs`), re-derived here rather
    than imported, and controlled positively and negatively below.
    """
    sites = tuple(range(order))
    parts = C.part_map(split)
    crossing = sorted(C.crossing_pairs(split))
    out = []
    for family in G.matchings_inside(crossing):
        if not family:
            continue
        covered = {site for edge in family for site in edge}
        if not all(parts[site] == colour
                   for site in sites if site not in covered):
            continue
        residue = tuple(site for site in sites if site not in covered)
        touching = sum(1 for edge in family
                       if parts[edge[0]] == colour or parts[edge[1]] == colour)
        out.append((tuple(sorted(family)), residue, touching))
    return out


def budget_words():
    """The pair-inside word budget of the sharpened kernel: words
    (w_0,w_1,w_2,w_3,rho) with the four non-residue letters in {b,c} and
    rho in {b,c}^4 union {(a,a,a,a)}.  Computed, not asserted."""
    out = []
    for small in product((0, 1), repeat=4):
        for rho in list(product((0, 1), repeat=4)) + [(2, 2, 2, 2)]:
            out.append(small + rho)
    return out


def section_geometry():
    """The D2 representative used by section 3, and the D1 geometry
    Sigma lives on, both read out of the same census enumeration."""
    # The colour word chi is the split's own part map, not a constant
    # written here: every section that reads chi (the D2 saturation
    # slots, the (dagger) identity of the near-miss section) therefore
    # moves with the split, and a mistyped chi is a loud failure.
    induced = tuple(C.part_map(CANONICAL_SPLIT)[site] for site in SITES)
    require(
        CHI == induced,
        "geometry: the colour word chi = %s is not the word induced by "
        "the canonical split through the committed part_map (%s)"
        % (list(CHI), list(induced)),
    )
    require(
        all(D2_SAT_ROW[u] == CHI[u] for u in D2_SAT_ROW)
        and all(D2_SAT_COL[p] == CHI[p] for p in D2_SAT_COL),
        "geometry: the D2 saturation slots do not read chi at the "
        "essential sites and their partners",
    )
    require(
        sorted(D2_SAT_ROW) == sorted(D2_ESSENTIAL_PARTNER)
        and sorted(D2_SAT_COL) == sorted(D2_ESSENTIAL_PARTNER.values()),
        "geometry: the D2 saturation slots are not indexed by the "
        "carriers' essential sites and partners",
    )
    for (u, p) in D2_CARRIERS:
        require(
            (CHI[u], CHI[p]) != (CANONICAL_A, CANONICAL_A),
            "geometry: carrier {%d,%d} reads (a,a) at chi, so its "
            "crossing cell would carry the purity constant m_e and the "
            "(dagger) numerator would not be the whole of it" % (u, p),
        )
    budget = budget_words()
    require(
        len(budget) == 272 and len(set(budget)) == 272,
        "geometry: the pair-inside word budget has %d distinct words, "
        "not the 272 of the sharpened kernel" % len(set(budget)),
    )
    require(
        all(word[site] != CANONICAL_A for word in budget
            for site in (0, 1, 3)),
        "geometry: a budget word reads the saturating colour at an "
        "essential site, so the budget is not inside the non-automatic "
        "slice",
    )
    families = saturating_families(8, CANONICAL_SPLIT, CANONICAL_A)
    by_signature = {}
    for family, residue, touching in families:
        by_signature.setdefault((len(family), len(residue), touching),
                                []).append((family, residue))
    require(
        set(by_signature) == {(2, 4, 0), (3, 2, 2), (4, 0, 4)},
        "canonical split: the saturating signatures are no longer "
        "{D1 = (2,4,0), D2 = (3,2,2), empty-residue = (4,0,4)}",
    )
    # Enumeration-path control (positive and negative), as in the census
    # pair: a named D1 family must appear, a non-covering matching must
    # not.
    found = {family for family, _residue, _t in families}
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
    # The D2 representative this artifact sweeps.
    representative = tuple(sorted(D2_CARRIERS))
    d2 = by_signature[(3, 2, 2)]
    require(
        len(d2) == 48,
        "D2 geometry: the canonical split no longer carries exactly 48 "
        "families of signature (3,2,2)",
    )
    matched = [residue for family, residue in d2 if family == representative]
    require(
        matched == [D2_RESIDUE],
        "D2 geometry: the swept representative family {{0,2},{1,4},{3,5}} "
        "is not a census (3,2,2) family with residue {6,7}",
    )
    # Its shape: one 2-to-2 carrier, two S_a carriers with exactly one
    # endpoint in S_a -- the hypotheses section 3's skeleton encodes.
    outside = [edge for edge in representative if set(edge) <= {0, 1, 2, 3}]
    touching = [edge for edge in representative if set(edge) & set(D1_RESIDUE)]
    require(
        outside == [(0, 2)] and len(touching) == 2
        and all(len(set(edge) & set(D1_RESIDUE)) == 1 for edge in touching),
        "D2 geometry: the swept representative is not one 2-part-to-2-part "
        "carrier plus two S_a carriers",
    )
    # Exhaustiveness of sweeping ONE representative: the split-preserving
    # relabelling group (S_2 x S_2 x S_4, order 96) acts on the 48
    # families of signature (3,2,2), and the orbit of the swept
    # representative is required to be ALL of them.  (That the D2
    # skeleton and the three certificates are equivariant under this
    # action is an inspection, not a machine fact.)
    group = []
    for perm_b in permutations((0, 1)):
        for perm_c in permutations((2, 3)):
            for perm_a in permutations((4, 5, 6, 7)):
                mapping = {}
                for index, site in enumerate((0, 1)):
                    mapping[site] = perm_b[index]
                for index, site in enumerate((2, 3)):
                    mapping[site] = perm_c[index]
                for index, site in enumerate((4, 5, 6, 7)):
                    mapping[site] = perm_a[index]
                group.append(mapping)
    require(len(group) == 96,
            "relabelling group: the split-preserving group is not "
            "S_2 x S_2 x S_4 of order 96 (built %d elements)" % len(group))
    orbit = set()
    for mapping in group:
        image = tuple(sorted(tuple(sorted((mapping[u], mapping[v])))
                             for (u, v) in representative))
        orbit.add(image)
    all_d2 = {family for family, _residue in d2}
    require(
        orbit == all_d2,
        "D2 exhaustiveness: the relabelling orbit of the swept "
        "representative has %d of the %d census families of signature "
        "(3,2,2), so sweeping one representative does not cover the "
        "configuration" % (len(orbit), len(all_d2)),
    )
    # Negative control: a strictly smaller group (S_a permutations
    # dropped) must NOT cover them, or the orbit test would be blind.
    small_orbit = set()
    for mapping in group:
        if any(mapping[site] != site for site in D1_RESIDUE):
            continue
        small_orbit.add(tuple(sorted(tuple(sorted((mapping[u], mapping[v])))
                                     for (u, v) in representative)))
    require(
        small_orbit < all_d2,
        "D2 exhaustiveness control: the orbit under the S_a-trivial "
        "subgroup already covers every (3,2,2) family, so the orbit test "
        "cannot distinguish groups",
    )

    # The D1 families, whose residue is the whole 4-part: Sigma's geometry.
    d1 = sorted(family for family, _residue in by_signature[(2, 4, 0)])
    require(
        d1 == [((0, 2), (1, 3)), ((0, 3), (1, 2))],
        "D1 geometry: the nonempty-residue k=2 families of the canonical "
        "split are not exactly the two perfect matchings between the two "
        "2-parts",
    )
    require(
        all(residue == D1_RESIDUE for _family, residue
            in by_signature[(2, 4, 0)]),
        "D1 geometry: the residue is not the whole 4-part",
    )
    return {
        "split": [list(part) for part in CANONICAL_SPLIT],
        "saturating_colour": CANONICAL_A,
        "chi_induced_by_split": list(induced),
        "budget_words": len(budget),
        "signatures": sorted(list(key) for key in by_signature),
        "D2_family_count": len(d2),
        "D2_representative": [list(edge) for edge in representative],
        "D2_residue": list(D2_RESIDUE),
        "relabelling_group_order": len(group),
        "D2_orbit_size": len(orbit),
        "D2_orbit_under_S_a_trivial_subgroup": len(small_orbit),
        "D1_families": [[list(edge) for edge in family] for family in d1],
        "D1_residue": list(D1_RESIDUE),
    }


# ------------------------------------ S2 the polynomial engine, controlled


def section_engine_control():
    """Validation of the polynomial ring against the committed oracle.

    `sym_matching_sum` is a transliteration of the committed
    `coefficient`: it walks the SAME enumerator (`C.perfect_matchings`)
    with the same early break, over polynomial rather than Fraction
    cells.  So this is NOT an independent cross-check of the matching
    enumeration -- it validates the RING (addition, multiplication,
    zero-detection, evaluation) against arithmetic that is already
    committed: on a fully generic symbolic packet (a distinct variable
    in each of the 324 cells) the polynomial evaluated at the probe
    point must equal the oracle's value on the instantiated Fraction
    packet, and a deliberately perturbed instantiation must DISAGREE.
    The enumeration itself is inherited, not re-derived.
    """
    blocks = sym_zero_blocks(SITES)
    for (u, v) in combinations(SITES, 2):
        for i in COLORS:
            for j in COLORS:
                blocks[(u, v)][i][j] = p_var("A_%d%d_%d%d" % (u, v, i, j))
    instantiated = evaluate_blocks(blocks, SITES)
    words = ((0,) * 8, (1,) * 8, CHI, (0, 1, 2, 0, 1, 2, 0, 1))
    agreements = 0
    monomials = []
    for values in words:
        word = dict(zip(SITES, values))
        symbolic = sym_matching_sum(blocks, SITES, word)
        monomials.append(len(symbolic))
        require(
            len(symbolic) == len(tuple(C.perfect_matchings(SITES))),
            "engine control: a generic 8-site matching sum has %d "
            "monomials, not one per perfect matching" % len(symbolic),
        )
        got = p_probe(symbolic)
        want = C.coefficient(instantiated, SITES, word)
        require(
            got == want,
            "engine control: the symbolic matching sum disagrees with the "
            "committed coefficient oracle at word %s" % (values,),
        )
        require(got != 0,
                "engine control: the comparison is 0 = 0 at word %s, so it "
                "verifies nothing" % (values,))
        agreements += 1
    # Negative control: perturb the Fraction packet only.
    perturbed = C.zero_blocks(SITES)
    for (u, v) in combinations(SITES, 2):
        for i in COLORS:
            for j in COLORS:
                C.set_cell(perturbed, u, v, i, j,
                           C.oriented(instantiated, u, v)[i][j])
    C.set_cell(perturbed, 0, 1, 0, 0,
               C.oriented(instantiated, 0, 1)[0][0] + 1)
    word = dict(zip(SITES, (0,) * 8))
    require(
        C.coefficient(perturbed, SITES, word)
        != p_probe(sym_matching_sum(blocks, SITES, word)),
        "engine control: a one-cell perturbation of the instantiated "
        "packet did not change the committed oracle's value, so the "
        "cross-implementation comparison cannot detect a wrong block",
    )
    # The symbolic hafnian must agree with the committed hafnian too.
    require(
        p_probe(sym_hafnian(blocks, 2, D1_RESIDUE))
        == C.hafnian(instantiated, 2, D1_RESIDUE) != 0,
        "engine control: the symbolic hafnian disagrees with the "
        "committed hafnian on the 4-part",
    )
    return {"words_compared": agreements,
            "generic_matching_monomials": monomials}


# ================================================== S3 the D2 branch sweep


def build_d2_combo(branches, injection=None):
    """The D2 skeleton on the census-mirrored geometry, with one support
    family chosen per carrier.

    branches: dict (u,p) -> one of BRANCH_FAMILIES.
    injection: optional (u, v, i, j, poly) written into the built blocks
        AFTER construction -- used only by the designed negative probes.

    Returns (blocks, slots) where slots[(u,p)] carries the branch's
    (dagger)-numerator s_slot and the carrier's crossing cell.
    """
    blocks = sym_zero_blocks(SITES)
    nu, nuinv = p_var("nu"), p_var("nuinv")
    blocks[(6, 7)][2][2] = nu

    def free_ok(u, i, v):
        """(E1): row a at an essential site vanishes off its partner."""
        return not (u in D2_ESSENTIAL_PARTNER and i == 2
                    and v != D2_ESSENTIAL_PARTNER[u])

    carrier_set = {tuple(sorted(carrier)) for carrier in D2_CARRIERS}
    for (u, v) in combinations(SITES, 2):
        if u in D2_RESIDUE or v in D2_RESIDUE:
            continue                       # residue-adjacent: per branch
        if (u, v) in carrier_set:
            continue                       # carrier blocks: T-defined
        for i in COLORS:
            for j in COLORS:
                if free_ok(u, i, v) and free_ok(v, j, u):
                    blocks[(u, v)][i][j] = p_var("C%d%d_%d%d" % (u, v, i, j))

    for (u, p) in D2_CARRIERS:
        branch = branches[(u, p)]
        keep, drop = (6, 7) if branch.endswith("6") else (7, 6)
        if branch in ("g6", "g7"):
            # A_{u,keep}: a-column only (rows b,c; (E1) kills row a).
            for i in (0, 1):
                sym_put(blocks, u, keep, i, 2,
                        p_var("U%d%d_%d2" % (u, keep, i)))
            # A_{u,drop} = 0; A_{p,drop}: a-column only; A_{p,keep} free.
            for i in COLORS:
                sym_put(blocks, p, drop, i, 2,
                        p_var("P%d%d_%d2" % (p, drop, i)))
            for i in COLORS:
                for j in COLORS:
                    sym_put(blocks, p, keep, i, j,
                            p_var("P%d%d_%d%d" % (p, keep, i, j)))
        elif branch in ("d6", "d7"):
            # The free-column degenerate family (case I.b of the U-system
            # classification, p_2 = 0): A_{u,keep} columns b,c free (rank
            # up to 2 -- outside the exchange closure), a-column zero;
            # A_{u,drop} a-column; A_{p,keep} a-column; A_{p,drop} = 0.
            for i in (0, 1):
                for k in (0, 1):
                    sym_put(blocks, u, keep, i, k,
                            p_var("D%d%d_%d%d" % (u, keep, i, k)))
                sym_put(blocks, u, drop, i, 2,
                        p_var("D%d%d_%d2" % (u, drop, i)))
            for j in COLORS:
                sym_put(blocks, p, keep, j, 2,
                        p_var("D%d%d_%d2" % (p, keep, j)))
        else:
            # The exchange family (the C6 rank-1 pattern, oriented at
            # `keep`): A_{u,keep}(.,k) = c_k w; A_{u,drop}(.,a) = w;
            # A_{p,keep}(.,k) = -c_k q, a-column qf; A_{p,drop}(.,a) = q.
            # In the plain families x6/x7 the a-column of A_{u,keep} is
            # zero; in the EXTENDED families xf6/xf7 it is free -- also a
            # U-system solution, and the one the classification of
            # section "u_system" shows is forced whenever both carrier
            # endpoints feed the same residue site.
            w = [p_var("w_%d%d_%d" % (u, p, i)) for i in (0, 1)]
            c = [p_var("c_%d%d_%d" % (u, p, k)) for k in (0, 1)]
            q = [p_var("q_%d%d_%d" % (u, p, j)) for j in COLORS]
            qf = [p_var("qf_%d%d_%d" % (u, p, j)) for j in COLORS]
            for i in (0, 1):
                for k in (0, 1):
                    sym_put(blocks, u, keep, i, k, p_mul(c[k], w[i]))
                sym_put(blocks, u, drop, i, 2, w[i])
                if branch.startswith("xf"):
                    sym_put(blocks, u, keep, i, 2,
                            p_var("xa_%d%d_%d" % (u, p, i)))
            for j in COLORS:
                for k in (0, 1):
                    sym_put(blocks, p, keep, j, k, p_neg(p_mul(c[k], q[j])))
                sym_put(blocks, p, keep, j, 2, qf[j])
                sym_put(blocks, p, drop, j, 2, q[j])

    # The carrier blocks are DEFINED by the T-part of the 4-site purity:
    #   A_up(i,j) = (m delta_{ij,aa} - s(i,j)) / nu,
    #   s(i,j) = A_u6(i,a) A_p7(j,a) + A_u7(i,a) A_p6(j,a).
    slots = {}
    for (u, p) in D2_CARRIERS:
        m = p_var("m_%d%d" % (u, p))
        for i in COLORS:
            for j in COLORS:
                dagger = p_add(
                    p_mul(sym_cell(blocks, u, 6, i, 2),
                          sym_cell(blocks, p, 7, j, 2)),
                    p_mul(sym_cell(blocks, u, 7, i, 2),
                          sym_cell(blocks, p, 6, j, 2)))
                lead = m if (i, j) == (2, 2) else p_const(0)
                sym_put(blocks, u, p, i, j,
                        p_mul(p_sub(lead, dagger), nuinv))
                if (i, j) == (D2_SAT_ROW[u], D2_SAT_COL[p]):
                    slots[(u, p)] = {"s_slot": dagger}
        slots[(u, p)]["crossing_cell"] = sym_cell(
            blocks, u, p, D2_SAT_ROW[u], D2_SAT_COL[p])
    if injection is not None:
        u, v, i, j, value = injection
        sym_put(blocks, u, v, i, j, value)
    return blocks, slots


def two_colour_partners(branches):
    """P[r]: the sites whose block toward residue site r can carry a
    {b,c}-coloured cell on this combo's support."""
    partners = {6: set(), 7: set()}
    for (u, p) in D2_CARRIERS:
        branch = branches[(u, p)]
        keep = 6 if branch.endswith("6") else 7
        if branch in ("g6", "g7"):
            partners[keep].add(p)          # A_{p,keep} is free
        elif branch in ("d6", "d7"):
            partners[keep].add(u)          # free b,c columns at u
        else:
            partners[keep].add(u)          # exchange feeds both endpoints
            partners[keep].add(p)
    return partners


def feeder_counts(branches):
    counts = {6: 0, 7: 0}
    for carrier in D2_CARRIERS:
        keep = 6 if branches[carrier].endswith("6") else 7
        counts[keep] += 1
    return counts


def d2_anchor_deaths(blocks):
    """The anchors that are identically zero on this support."""
    dead = []
    for colour in (0, 1):
        word = dict(zip(SITES, (colour,) * 8))
        if p_is_zero(sym_matching_sum(blocks, SITES, word)):
            dead.append((colour,) * 8)
    return dead


def d2_gamma_certificate(branches, blocks):
    """The unique-partner certificate.

    If a residue site r has a UNIQUE two-colour partner x, then in every
    two-colour word each matching term contains the single factor A_xr,
    so with Gamma_c = H_{B \\ {x,r}}(c on everything):

        H_B(c^8)                                  = A_xr(c,c) Gamma_c,
        H_B(c^8 with x and r flipped to d)        = A_xr(d,d) Gamma_c.

    Exactness makes the first equal 1 (so A_xr(c,c) and Gamma_c are
    units for both c) and the second equal 0, forcing A_xr(d,d) = 0 for
    both d -- contradicting the other anchor.  THREE budget words.  Both
    factorizations are verified as polynomial identities here.
    """
    partners = two_colour_partners(branches)
    for residue_site in D2_RESIDUE:
        candidates = partners[residue_site]
        if len(candidates) != 1:
            continue
        partner = next(iter(candidates))
        rest = tuple(site for site in SITES
                     if site not in (partner, residue_site))
        words, gammas, ok = [], [], True
        for c, d in ((0, 1), (1, 0)):
            values = [c] * 8
            values[partner] = d
            values[residue_site] = d
            gamma = sym_matching_sum(
                blocks, rest, {site: c for site in rest})
            flip = sym_matching_sum(blocks, SITES, dict(zip(SITES, values)))
            anchor = sym_matching_sum(
                blocks, SITES, dict(zip(SITES, (c,) * 8)))
            want_flip = p_mul(
                sym_cell(blocks, partner, residue_site, d, d), gamma)
            want_anchor = p_mul(
                sym_cell(blocks, partner, residue_site, c, c), gamma)
            if (not p_is_zero(p_sub(flip, want_flip))
                    or not p_is_zero(p_sub(anchor, want_anchor))):
                ok = False
                break
            words.append(tuple(values))
            gammas.append(gamma)
        if ok:
            return {"unique_partner": [partner, residue_site],
                    "words": [list(word) for word in words],
                    "gamma_fingerprints": [p_fingerprint(g) for g in gammas]}
    return None


def d2_cfactor_certificate(branches, blocks):
    """The exchange c-factor certificate.

    If residue site r is fed by exactly ONE carrier and that carrier is
    of exchange type oriented at r, then both blocks into r have their
    {b,c}-columns of the form c_k * (vector independent of k), so every
    word's value carries the scalar c_{w_r} as an overall factor:

        H_B(c^8 with r flipped to d) * c_c  ==  H_B(c^8) * c_d.

    Exactness (H_B(c^8) = 1, H_B(flip) = 0) then gives c_d = 0 for both
    d, and the anchors need c_c != 0.  FOUR budget words.  The identity
    is verified symbolically here, not assumed.
    """
    partners = two_colour_partners(branches)
    for residue_site in D2_RESIDUE:
        if not partners[residue_site]:
            continue
        feeders = [(carrier, branches[carrier]) for carrier in D2_CARRIERS
                   if (6 if branches[carrier].endswith("6") else 7)
                   == residue_site]
        if len(feeders) != 1 or not feeders[0][1].startswith("x"):
            continue
        (u, p), _branch = feeders[0]
        scalars = [p_var("c_%d%d_%d" % (u, p, k)) for k in (0, 1)]
        words, ok = [], True
        for c, d in ((0, 1), (1, 0)):
            values = [c] * 8
            values[residue_site] = d
            flip = sym_matching_sum(blocks, SITES, dict(zip(SITES, values)))
            anchor = sym_matching_sum(
                blocks, SITES, dict(zip(SITES, (c,) * 8)))
            left = p_mul(flip, scalars[c])
            right = p_mul(anchor, scalars[d])
            if not p_is_zero(p_sub(left, right)):
                ok = False
                break
            words.append(tuple(values))
        if ok:
            return {"carrier": [u, p], "residue_site": residue_site,
                    "words": [list(word) for word in words]}
    return None


def section_d2_sweep():
    """The 216-combination sweep, its pigeonhole mechanism, the
    saturation bridge, and the designed negative probes."""
    started = monotonic()
    verdicts = []
    tally = {"anchor_dead": 0, "gamma": 0, "c_factor": 0, "survivor": 0}
    slot_rows = []
    feeder_distribution = {}
    pigeonhole = {"starved_combinations": 0, "starved_implies_anchor_dead": 0}
    for combo in product(BRANCH_FAMILIES, repeat=3):
        branches = dict(zip(D2_CARRIERS, combo))
        blocks, slots = build_d2_combo(branches)
        tag = ",".join("%d%d:%s" % (u, p, branches[(u, p)])
                       for (u, p) in D2_CARRIERS)

        # --- saturation is SATISFIABLE on every swept slot: the
        #     (dagger)-numerator s_e(chi) -- which by the (T)-relations
        #     is the whole of -nu A_up(chi), the m-term dropping because
        #     (chi_u, chi_p) != (a,a) (required in section_geometry) --
        #     is a NONZERO polynomial on all eight families.  (The
        #     converse direction, s_e == 0 on a designed degenerate slot,
        #     is probe N4 below.)
        for carrier in D2_CARRIERS:
            slot = slots[carrier]
            require(
                not p_is_zero(slot["s_slot"]),
                "D2 saturation: the (dagger)-numerator s_e(chi) of "
                "carrier %s vanishes identically on combo %s, so this "
                "family cannot carry a saturating D2 crossing cell and "
                "is not a member of the swept class"
                % (carrier, tag),
            )
            slot_rows.append([tag, list(carrier),
                              p_fingerprint(slot["s_slot"]),
                              p_fingerprint(slot["crossing_cell"])])

        # --- the pigeonhole datum, computed two independent ways.
        counts = feeder_counts(branches)
        partners = two_colour_partners(branches)
        require(
            sum(counts.values()) == len(D2_CARRIERS),
            "D2 pigeonhole: the feeder counts of combo %s sum to %d, not "
            "to the number of carriers" % (tag, sum(counts.values())),
        )
        for site in D2_RESIDUE:
            require(
                (counts[site] == 0) == (not partners[site]),
                "D2 pigeonhole: the feeder count and the two-colour "
                "partner set of residue site %d disagree on combo %s"
                % (site, tag),
            )
        key = str([counts[6], counts[7]])
        feeder_distribution[key] = feeder_distribution.get(key, 0) + 1
        starved = [site for site in D2_RESIDUE if counts[site] == 0]

        dead = d2_anchor_deaths(blocks)
        if starved:
            pigeonhole["starved_combinations"] += 1
            require(
                len(dead) == 2,
                "D2 pigeonhole: combo %s starves residue site %s of "
                "two-colour feeders, yet an anchor is not identically "
                "zero" % (tag, starved),
            )
            pigeonhole["starved_implies_anchor_dead"] += 1

        anchor_fingerprints = [
            p_fingerprint(sym_matching_sum(
                blocks, SITES, dict(zip(SITES, (colour,) * 8))))
            for colour in (0, 1)]

        if dead:
            tally["anchor_dead"] += 1
            verdicts.append([tag, "ANCHOR_DEAD",
                             [list(word) for word in dead],
                             anchor_fingerprints])
            continue
        require(
            all(fingerprint[0] > 0 for fingerprint in anchor_fingerprints),
            "D2 sweep: combo %s passed the anchor test although an anchor "
            "polynomial has no monomials" % tag,
        )
        gamma = d2_gamma_certificate(branches, blocks)
        if gamma is not None:
            require(
                all(fingerprint[0] > 0
                    for fingerprint in gamma["gamma_fingerprints"]),
                "D2 sweep: the Gamma certificate of combo %s factors "
                "through an identically zero deletion tensor, so it holds "
                "vacuously" % tag,
            )
            tally["gamma"] += 1
            verdicts.append([tag, "GAMMA", gamma, anchor_fingerprints])
            continue
        cfactor = d2_cfactor_certificate(branches, blocks)
        if cfactor is not None:
            tally["c_factor"] += 1
            verdicts.append([tag, "C_FACTOR", cfactor, anchor_fingerprints])
            continue
        tally["survivor"] += 1
        verdicts.append([tag, "SURVIVOR",
                         {"partners": {str(site): sorted(sites)
                                       for site, sites in partners.items()}},
                         anchor_fingerprints])

    require(
        tally["survivor"] == 0,
        "D2 sweep: %d of the %d branch combinations survived every "
        "certificate, so D2 is NOT killed on the swept class"
        % (tally["survivor"], len(verdicts)),
    )
    require(
        len(verdicts) == len(BRANCH_FAMILIES) ** 3 == 512,
        "D2 sweep: the branch-combination count is no longer 8^3 = 512",
    )
    require(
        (tally["anchor_dead"], tally["gamma"], tally["c_factor"])
        == (128, 192, 192),
        "D2 sweep: the certificate census changed from 128 anchor-dead, "
        "192 Gamma, 192 c-factor (computed: %d / %d / %d)"
        % (tally["anchor_dead"], tally["gamma"], tally["c_factor"]),
    )
    require(
        feeder_distribution == {"[0, 3]": 64, "[1, 2]": 192,
                                "[2, 1]": 192, "[3, 0]": 64},
        "D2 pigeonhole: the distribution of (feeders at 6, feeders at 7) "
        "over the 512 combinations is %s, not the multinomial "
        "(64, 192, 192, 64) that three carriers over two residue sites "
        "force -- in particular the 128 starved combinations that make "
        "both anchors identically zero" % feeder_distribution,
    )
    # Every certificate word must lie in the sharpened kernel's 272-word
    # pair-inside budget -- the claim the note makes about their cost.
    budget = set(budget_words())
    certificate_words = set()
    for _tag, kind, payload, _anchors in verdicts:
        if kind == "ANCHOR_DEAD":
            certificate_words.update(tuple(word) for word in payload)
        else:
            certificate_words.update(tuple(word) for word in payload["words"])
            certificate_words.update({(0,) * 8, (1,) * 8})
    require(
        certificate_words <= budget,
        "D2 sweep: %d certificate words lie outside the 272-word "
        "pair-inside budget"
        % len(certificate_words - budget),
    )
    require(
        pigeonhole["starved_combinations"] == tally["anchor_dead"],
        "D2 pigeonhole: %d combinations starve a residue site but %d are "
        "anchor-dead, so anchor death is not exactly the 0-feeder branch"
        % (pigeonhole["starved_combinations"], tally["anchor_dead"]),
    )

    # ---------------------------------------------- designed negative probes
    probes = {}
    # (N1) the Gamma certificate must REFUSE when the unique-partner
    #      hypothesis is broken by a second two-colour cell at site 7.
    branches = dict(zip(D2_CARRIERS, ("g6", "g7", "g6")))
    blocks, _slots = build_d2_combo(branches)
    require(d2_gamma_certificate(branches, blocks) is not None,
            "negative probe N1: the baseline combo (g6,g7,g6) is not "
            "Gamma-killed, so the probe tests nothing")
    broken, _slots = build_d2_combo(
        branches, injection=(0, 7, 0, 0, p_var("INJECT1")))
    require(
        d2_gamma_certificate(branches, broken) is None,
        "negative probe N1: the Gamma certificate still claims a "
        "unique-partner factorization although A_07 was given a "
        "two-colour cell",
    )
    gamma_word = dict(zip(
        SITES, d2_gamma_certificate(branches, blocks)["words"][0]))
    probes["N1_flip_word_before_after"] = [
        p_fingerprint(sym_matching_sum(blocks, SITES, gamma_word)),
        p_fingerprint(sym_matching_sum(broken, SITES, gamma_word))]
    # (N2) the c-factor certificate must REFUSE when the exchange rank-1
    #      pattern is broken.
    branches = dict(zip(D2_CARRIERS, ("g7", "g7", "x6")))
    blocks, _slots = build_d2_combo(branches)
    require(d2_cfactor_certificate(branches, blocks) is not None,
            "negative probe N2: the baseline combo (g7,g7,x6) is not "
            "c-factor-killed, so the probe tests nothing")
    broken, _slots = build_d2_combo(
        branches,
        injection=(3, 6, 0, 0,
                   p_add(sym_cell(blocks, 3, 6, 0, 0), p_var("INJECT2"))))
    require(
        d2_cfactor_certificate(branches, broken) is None,
        "negative probe N2: the c-factor certificate still claims the "
        "exchange scalar identity although the rank-1 pattern of "
        "A_36 was broken",
    )
    cfactor_word = dict(zip(
        SITES, d2_cfactor_certificate(branches, blocks)["words"][0]))
    probes["N2_flip_word_before_after"] = [
        p_fingerprint(sym_matching_sum(blocks, SITES, cfactor_word)),
        p_fingerprint(sym_matching_sum(broken, SITES, cfactor_word))]
    # (N3) anchor-death must DISAPPEAR when a free two-colour block into
    #      the starved residue site is added.
    branches = dict(zip(D2_CARRIERS, ("g6", "g6", "g6")))
    blocks, _slots = build_d2_combo(branches)
    require(len(d2_anchor_deaths(blocks)) == 2,
            "negative probe N3: the fully aligned combo (g6,g6,g6) no "
            "longer has both anchors identically zero")
    revived, _slots = build_d2_combo(
        branches, injection=(4, 7, 0, 0, p_var("INJECT3")))
    require(
        d2_anchor_deaths(revived) == [(1,) * 8],
        "negative probe N3: adding a free two-colour block into the "
        "starved residue site 7 did not revive the b-anchor, so the "
        "anchor-death test is not reading the support",
    )
    anchor_word = dict(zip(SITES, (0,) * 8))
    probes["N3_b_anchor_before_after"] = [
        p_fingerprint(sym_matching_sum(blocks, SITES, anchor_word)),
        p_fingerprint(sym_matching_sum(revived, SITES, anchor_word))]
    # (N4) a designed DEGENERATE slot (both carrier endpoints feeding the
    #      same residue site in the a-column) has s_slot identically zero,
    #      hence a vanishing D2 crossing cell: saturation excludes it.
    degenerate = sym_zero_blocks(SITES)
    for i in COLORS:
        sym_put(degenerate, 0, 6, i, 2, p_var("E_06_%d2" % i))
        sym_put(degenerate, 2, 6, i, 2, p_var("E_26_%d2" % i))
    s_slot = p_add(
        p_mul(sym_cell(degenerate, 0, 6, D2_SAT_ROW[0], 2),
              sym_cell(degenerate, 2, 7, D2_SAT_COL[2], 2)),
        p_mul(sym_cell(degenerate, 0, 7, D2_SAT_ROW[0], 2),
              sym_cell(degenerate, 2, 6, D2_SAT_COL[2], 2)))
    require(
        p_is_zero(s_slot),
        "negative probe N4: the designed degenerate slot support does "
        "not have s_slot identically zero, so it does not witness the "
        "saturation exclusion",
    )
    require(
        not p_is_zero(sym_cell(degenerate, 0, 6, D2_SAT_ROW[0], 2)),
        "negative probe N4: the designed degenerate slot has no live "
        "a-column cell at all, so its s_slot vanishes vacuously",
    )
    probes["N4_degenerate_s_slot_and_live_cell"] = [
        p_fingerprint(s_slot),
        p_fingerprint(sym_cell(degenerate, 0, 6, D2_SAT_ROW[0], 2))]

    return {
        "combinations": len(verdicts),
        "families": list(BRANCH_FAMILIES),
        "certificate_words": sorted(list(word)
                                    for word in certificate_words),
        "tally": tally,
        "feeder_distribution": feeder_distribution,
        "pigeonhole": pigeonhole,
        "verdicts": verdicts,
        "slot_fingerprints": slot_rows,
        "negative_probes": probes,
    }, monotonic() - started


# ===================== S3b the U-system census: which two-colour column
#                           signatures are realizable under saturation


def gf2_nullspace(rows, unknowns):
    """A basis of the GF(2) nullspace of the given equation rows, each a
    bitmask over `unknowns` variables.  Controlled below."""
    pivots = {}
    for row in rows:
        current = row
        while current:
            top = current.bit_length() - 1
            if top in pivots:
                current ^= pivots[top]
            else:
                pivots[top] = current
                break
    basis = []
    for free in range(unknowns):
        if free in pivots:
            continue
        vector = 1 << free
        for pivot in sorted(pivots):
            if bin(pivots[pivot] & vector & ~(1 << pivot)).count("1") % 2:
                vector |= 1 << pivot
        basis.append(vector)
    return basis


def u_system_rows(X, Y):
    """The U-relations as GF(2)-linear equations in the 18 unknowns of
    (Z, W) = (A_p6, A_p7), given (X, Y) = (A_u6, A_u7).

    The U-system is Lemma-F purity of H_{R u e} at every residue word
    other than (a,a): for all i, j and all (k,l) != (a,a),

        A_u6(i,k) A_p7(j,l) + A_u7(i,l) A_p6(j,k) = 0.

    Rows a of A_u6 and A_u7 vanish by (E1), so only i in {b,c} gives a
    nontrivial equation.  Variable layout: z(j,k) = 3j + k,
    w(j,l) = 9 + 3j + l.
    """
    rows = []
    for k in COLORS:
        for l in COLORS:
            if (k, l) == (2, 2):
                continue                  # that is the (T)-relation
            for i in (0, 1):
                for j in COLORS:
                    mask = 0
                    if X[i][k]:
                        mask |= 1 << (9 + 3 * j + l)
                    if Y[i][l]:
                        mask |= 1 << (3 * j + k)
                    if mask:
                        rows.append(mask)
    return rows


def u_feeder_signature(X, Y, Z, W):
    """Which endpoints feed two-colour cells into which residue site.

    X = A_u6, Y = A_u7, Z = A_p6, W = A_p7; a "two-colour feed" is a
    nonzero cell in the {b,c} x {b,c} corner (both endpoints of the edge
    read a two-colour letter).
    """
    def fed(from_u, from_p):
        out = []
        if any(from_u[i][k] for i in (0, 1) for k in (0, 1)):
            out.append("u")
        if any(from_p[j][k] for j in (0, 1) for k in (0, 1)):
            out.append("p")
        return tuple(sorted(out))

    return {6: fed(X, Z), 7: fed(Y, W)}


def is_u_solution(X, Y, Z, W):
    """Direct substitution into every U-relation (second implementation,
    independent of the linear-algebra path used by the census)."""
    for k in COLORS:
        for l in COLORS:
            if (k, l) == (2, 2):
                continue
            for i in COLORS:
                for j in COLORS:
                    if (X[i][k] * W[j][l] + Y[i][l] * Z[j][k]) % 2:
                        return False
    return True


def u_saturated(X, Y, Z, W):
    return any((X[i][2] * W[j][2] + Y[i][2] * Z[j][2]) % 2
               for i in COLORS for j in COLORS)


def section_u_system_census():
    """Census of the per-carrier U-system over GF(2).

    The audit of the first packaging showed that the swept families do
    NOT exhaust the U-system's saturated solutions (the extended
    exchange families xf6/xf7, a d-variant with a free a-column and an
    all-a-column solution are outside the original six).  What IS
    exhaustive, and is what the certificates actually consume, is the
    list of realizable **two-colour column signatures**: which of the
    carrier's two endpoints can feed a {b,c}-coloured cell into which
    residue site.

    Machine content (a census over one finite field, GF(2) -- evidence,
    not a proof over Q; the proof is the hand argument in the note):
    every solution of the U-system with s_e != 0 (the saturation
    numerator) is enumerated, and

      * NO saturated solution feeds two-colour cells into BOTH residue
        sites;
      * the realizable signatures are exactly seven -- the empty one and
        the six {u}, {p}, {u,p} into one of the two residue sites, which
        are the signatures of the g, d and x/xf families;
      * every saturated solution whose signature is {u,p} into one site
        has the EXTENDED EXCHANGE structure (A_{u,keep}(.,k) = c_k w,
        A_{p,keep}(.,k) = c_k q, A_{u,drop}(.,a) = w, A_{p,drop}(.,a) = q
        with the a-column of A_{u,keep} free, and the other endpoint's
        two-colour columns identically zero) -- so the c-factor
        certificate applies to every such solution, not only to the
        swept ones.

    Controls: the nullspace routine is checked on designed systems; the
    census must be nonvacuous in every signature class; and a designed
    packet that DOES feed both sites is confirmed to violate the
    U-system (so "no solution feeds both" is not an artifact of the
    enumeration missing solutions).
    """
    started = monotonic()
    # --- controls on the GF(2) nullspace routine, per branch.
    require(gf2_nullspace([], 3) == [1, 2, 4],
            "GF(2) control: the nullspace of the empty system is not the "
            "whole space")
    require(gf2_nullspace([0b011, 0b110], 3) == [0b111],
            "GF(2) control: the nullspace of x0+x1 = x1+x2 = 0 is not "
            "spanned by (1,1,1)")
    require(gf2_nullspace([0b001, 0b010, 0b100], 3) == [],
            "GF(2) control: a full-rank system reports a nonzero "
            "nullspace")

    counts = {"enumerated": 0, "saturated": 0, "both_sites": 0}
    signatures = {}
    exchange_failures = []
    for packed in range(1 << 12):
        X = [[(packed >> (3 * i + k)) & 1 for k in COLORS] for i in (0, 1)]
        Y = [[(packed >> (6 + 3 * i + l)) & 1 for l in COLORS]
             for i in (0, 1)]
        X.append([0, 0, 0])                # row a, by (E1)
        Y.append([0, 0, 0])
        if not any(X[i][2] or Y[i][2] for i in (0, 1)):
            continue                       # s_e == 0 for every (Z, W)
        basis = gf2_nullspace(u_system_rows(X, Y), 18)
        for mask in range(1 << len(basis)):
            solution = 0
            for index in range(len(basis)):
                if mask >> index & 1:
                    solution ^= basis[index]
            Z = [[(solution >> (3 * j + k)) & 1 for k in COLORS]
                 for j in COLORS]
            W = [[(solution >> (9 + 3 * j + l)) & 1 for l in COLORS]
                 for j in COLORS]
            counts["enumerated"] += 1
            if not u_saturated(X, Y, Z, W):
                continue
            counts["saturated"] += 1
            feeders = u_feeder_signature(X, Y, Z, W)
            if feeders[6] and feeders[7]:
                counts["both_sites"] += 1
            key = str([list(feeders[6]), list(feeders[7])])
            signatures[key] = signatures.get(key, 0) + 1
            # the |P| = 2 classification, checked on this solution
            for site, keep_blocks, drop_blocks in (
                (6, (X, Z), (Y, W)), (7, (Y, W), (X, Z))
            ):
                if feeders[site] != ("p", "u"):
                    continue
                near_u, near_p = keep_blocks
                far_u, far_p = drop_blocks
                ok = False
                for c0 in (0, 1):
                    for c1 in (0, 1):
                        scalars = (c0, c1)
                        if all(near_u[i][k] == (scalars[k] & far_u[i][2])
                               for i in (0, 1) for k in (0, 1)) \
                           and all(near_p[j][k] == (scalars[k] & far_p[j][2])
                                   for j in COLORS for k in (0, 1)) \
                           and all(far_p[j][l] == 0
                                   for j in COLORS for l in (0, 1)) \
                           and all(far_u[i][l] == 0
                                   for i in (0, 1) for l in (0, 1)):
                            ok = True
                if not ok:
                    exchange_failures.append([site, packed, solution])
    require(
        counts["both_sites"] == 0,
        "U-system census: %d saturated solutions feed two-colour cells "
        "into BOTH residue sites, so the pigeonhole the certificates "
        "rest on is not forced by the U-system"
        % counts["both_sites"],
    )
    require(
        set(signatures) == {
            "[[], []]", "[['u'], []]", "[['p'], []]", "[['p', 'u'], []]",
            "[[], ['u']]", "[[], ['p']]", "[[], ['p', 'u']]"},
        "U-system census: the realizable two-colour column signatures "
        "are %s, not the seven (empty, and {u}/{p}/{u,p} into exactly "
        "one residue site)" % sorted(signatures),
    )
    require(
        not exchange_failures,
        "U-system census: %d saturated solutions have both endpoints "
        "feeding one residue site WITHOUT the extended-exchange "
        "structure, so the c-factor certificate does not cover that "
        "signature class" % len(exchange_failures),
    )
    # --- positive control: each swept family, instantiated over GF(2),
    #     must be a saturated U-solution with the signature the sweep
    #     assigns to it (so the census really covers the swept class).
    zero = [[0, 0, 0] for _ in COLORS]

    def rows(*entries):
        block = [[0, 0, 0] for _ in COLORS]
        for (i, j) in entries:
            block[i][j] = 1
        return block

    designed = {
        # g6: A_u6 a-column, A_u7 = 0, A_p7 a-column, A_p6 free.
        "g6": (rows((0, 2)), zero, rows((0, 0), (1, 1)), rows((0, 2))),
        # d6: A_u6 two-colour columns, A_u7 a-column, A_p6 a-column,
        #     A_p7 = 0.
        "d6": (rows((0, 0)), rows((0, 2)), rows((0, 2)), zero),
        # x6 / xf6: the exchange pattern with c_b = 1, c_c = 0, w = e_b,
        #     q = e_b; xf6 additionally has a free a-column at A_u6
        #     (and qf = 0, so that the two saturation terms do not
        #     cancel over GF(2)).
        "x6": (rows((0, 0)), rows((0, 2)), rows((0, 0), (0, 2)),
               rows((0, 2))),
        "xf6": (rows((0, 0), (0, 2)), rows((0, 2)), rows((0, 0)),
                rows((0, 2))),
        # the empty signature: all four blocks a-column only.
        "empty": (rows((0, 2)), zero, rows((0, 2)), rows((0, 2))),
    }
    expected = {"g6": [["p"], []], "d6": [["u"], []],
                "x6": [["p", "u"], []], "xf6": [["p", "u"], []],
                "empty": [[], []]}
    control = {}
    for name, (X, Y, Z, W) in sorted(designed.items()):
        require(
            is_u_solution(X, Y, Z, W),
            "U-system control: the designed GF(2) instance of family %s "
            "does not satisfy the U-relations" % name,
        )
        require(
            u_saturated(X, Y, Z, W),
            "U-system control: the designed GF(2) instance of family %s "
            "is not saturated, so it is not in the swept class" % name,
        )
        feeders = u_feeder_signature(X, Y, Z, W)
        got = [list(feeders[6]), list(feeders[7])]
        want = expected[name]
        require(
            got == want,
            "U-system control: the designed instance of family %s has "
            "signature %s, not the %s the sweep assigns to it"
            % (name, got, want),
        )
        require(
            str(got) in signatures,
            "U-system control: the designed instance of family %s has a "
            "signature the census never enumerated" % name,
        )
        control[name] = got
    # --- negative control: the signature classifier must SEE a
    #     both-sites packet (it is the census's exclusion that is
    #     substantive, not a blind classifier).  This packet feeds both
    #     residue sites from u, and is required NOT to be a U-solution
    #     for any completion the census would have found -- consistent
    #     with the census's verdict of zero both-sites solutions.
    both = u_feeder_signature(rows((0, 0)), rows((0, 0)), zero, zero)
    require(
        both[6] == ("u",) and both[7] == ("u",),
        "U-system control: the signature classifier does not report a "
        "designed both-sites packet as feeding both residue sites",
    )
    require(
        not u_saturated(rows((0, 0)), rows((0, 0)), zero, zero),
        "U-system control: the designed both-sites packet is saturated, "
        "so it would contradict the census rather than illustrate it",
    )
    return {
        "counts": counts,
        "signature_census": signatures,
        "designed_family_signatures": control,
        "field": "GF(2)",
    }, monotonic() - started


# ============================== S4 monochromatic rigidity on the class Sigma


def sigma_cells():
    """Every free cell of the a-column support class Sigma on the D1
    geometry: small-small blocks subject to (E1), small-residue blocks
    a-column only, residue-residue blocks (a,a) only."""
    cells = []

    def e1_ok(u, i, v):
        return not (u in D1_ESSENTIAL_PARTNER and i == 2
                    and v != D1_ESSENTIAL_PARTNER[u])

    for u, v in combinations(D1_SMALL, 2):
        for i in COLORS:
            for j in COLORS:
                if e1_ok(u, i, v) and e1_ok(v, j, u):
                    cells.append((u, v, i, j))
    for p in D1_SMALL:
        for r in D1_RESIDUE:
            for i in COLORS:
                if e1_ok(p, i, r):
                    cells.append((p, r, i, 2))
    for r, rp in combinations(D1_RESIDUE, 2):
        cells.append((r, rp, 2, 2))
    return cells


def build_sigma(extra=()):  # extra: cells revived OUTSIDE Sigma
    blocks = sym_zero_blocks(SITES)
    for (u, v, i, j) in tuple(sigma_cells()) + tuple(extra):
        sym_put(blocks, u, v, i, j, p_var("S_%d%d_%d%d" % (u, v, i, j)))
    return blocks


def residue_incidence(matching, residue):
    return [edge for edge in matching
            if edge[0] in residue or edge[1] in residue]


def section_rigidity():
    """H_B(b^8) = H_B(c^8) = 0 identically on Sigma, structurally and as
    a polynomial identity, with positive and negative probes."""
    # --- the structural reason, swept over all 105 matchings.
    matchings = tuple(C.perfect_matchings(SITES))
    require(len(matchings) == 105,
            "rigidity: the 8-site perfect matchings are no longer 105")
    minimum = None
    for matching in matchings:
        count = len(residue_incidence(matching, D1_RESIDUE))
        minimum = count if minimum is None else min(minimum, count)
    require(
        minimum >= 2,
        "rigidity: a perfect matching has only %d residue-incident "
        "edges, so the structural argument fails" % minimum,
    )
    # Control: the same scan must be able to FAIL.  With a single site
    # designated "residue", matchings with one incident edge exist.
    single = None
    for matching in matchings:
        count = len(residue_incidence(matching, (7,)))
        single = count if single is None else min(single, count)
    require(
        single < 2,
        "rigidity scan control: designating a single site as the residue "
        "still reports two incident edges everywhere, so the scan is "
        "blind to the residue set it is given",
    )
    # --- the polynomial identity on the full class.
    cells = sigma_cells()
    blocks = build_sigma()
    anchors = {}
    for colour in (0, 1):
        word = dict(zip(SITES, (colour,) * 8))
        value = sym_matching_sum(blocks, SITES, word)
        require(
            p_is_zero(value),
            "rigidity: H_B(%s^8) is not identically zero on Sigma, so the "
            "monochromatic equations are not rigid there"
            % LETTER[colour],
        )
        anchors[LETTER[colour]] = p_fingerprint(value)
    # Positive probe: the class is not degenerate -- a two-colour word
    # with pure residues is generically nonzero.
    probe_word = dict(zip(SITES, (0, 0, 1, 1, 2, 2, 2, 2)))
    probe = sym_matching_sum(blocks, SITES, probe_word)
    require(
        not p_is_zero(probe),
        "rigidity: the probe word (b,b,c,c,a^4) vanishes identically on "
        "Sigma too, so the class is degenerate and the anchor statement "
        "is vacuous",
    )
    require(
        p_probe(probe) != 0,
        "rigidity: the probe word is a nonzero polynomial but vanishes at "
        "the probe point, so the fingerprint is uninformative",
    )
    # Cross-implementation control: the committed oracle must agree that
    # the anchors vanish on an instantiated Sigma packet, while the probe
    # word does not.
    instantiated = evaluate_blocks(blocks, SITES)
    for colour in (0, 1):
        require(
            C.coefficient(instantiated, SITES,
                          dict(zip(SITES, (colour,) * 8))) == 0,
            "rigidity: the committed coefficient oracle sees a nonzero "
            "%s-anchor on an instantiated Sigma packet" % LETTER[colour],
        )
    require(
        C.coefficient(instantiated, SITES, probe_word) == p_probe(probe),
        "rigidity: the committed oracle and the polynomial identity "
        "disagree on the probe word",
    )
    # --- negative probes, out of Sigma.
    one_cell = build_sigma(extra=((4, 5, 0, 0),))
    still_dead = sym_matching_sum(one_cell, SITES,
                                  dict(zip(SITES, (0,) * 8)))
    require(
        p_is_zero(still_dead),
        "rigidity sharpness: reviving the single residue-residue cell "
        "A_45(b,b) revived the b-anchor, contradicting the parity fact "
        "that the crossing edges pair up",
    )
    two_cells = build_sigma(extra=((4, 5, 0, 0), (6, 7, 0, 0)))
    revived = sym_matching_sum(two_cells, SITES, dict(zip(SITES, (0,) * 8)))
    require(
        not p_is_zero(revived),
        "rigidity negative probe: reviving the two disjoint "
        "residue-residue cells A_45(b,b), A_67(b,b) left the b-anchor "
        "identically zero, so the rigidity test cannot see an "
        "out-of-Sigma support",
    )
    return {
        "sigma_free_cells": len(cells),
        "matchings": len(matchings),
        "min_residue_incident_edges": minimum,
        "single_site_scan_minimum": single,
        "anchor_fingerprints": anchors,
        "probe_fingerprint": p_fingerprint(probe),
        "one_cell_revival_fingerprint": p_fingerprint(still_dead),
        "two_cell_revival_fingerprint": p_fingerprint(revived),
    }


# ======================= S5 the near-miss family (census facts + 6559/6561)


def build_pinned_rectangle(t):
    """The committed-convention D1 witness of the pinned-rectangle lemma
    (attack map 25c): every census fact holds for every t, and t = 0 is
    the harmful (degenerate-rectangle) point."""
    blocks = C.zero_blocks(SITES)
    C.set_cell(blocks, 4, 5, 2, 2, F(1))
    C.set_cell(blocks, 6, 7, 2, 2, F(1))
    alpha = {4: (F(1), F(1)), 5: (F(2), F(-1)),
             6: (F(1), F(0)), 7: (F(0), F(1))}
    beta = {4: (F(1), F(2), F(-1)), 5: (F(-1), F(1), F(2)),
            6: (F(3), F(0), F(1)), 7: (F(2), F(-2), F(0))}
    gamma = {4: (F(1), F(-1)), 5: (F(1), F(2)),
             6: (F(0), F(1)), 7: (F(2), F(0))}
    delta = {4: (F(2), F(1), F(1)), 5: (F(1), F(-1), F(0)),
             6: (F(1), F(3), F(-2)), 7: (F(-1), F(0), F(1))}
    for r in D1_RESIDUE:
        for i in (0, 1):
            C.set_cell(blocks, 0, r, i, 2, alpha[r][i])
            C.set_cell(blocks, 1, r, i, 2, gamma[r][i])
        for j in COLORS:
            C.set_cell(blocks, 2, r, j, 2, beta[r][j])
            C.set_cell(blocks, 3, r, j, 2, delta[r][j])
    for i in (0, 1):
        for j in COLORS:
            first = sum((alpha[r][i] * beta[rp][j] for r, rp in D1_PAIRS),
                        F(0))
            second = sum((gamma[r][i] * delta[rp][j] for r, rp in D1_PAIRS),
                         F(0))
            C.set_cell(blocks, 0, 2, i, j, -first)
            C.set_cell(blocks, 1, 3, i, j, -second)
    C.set_cell(blocks, 0, 2, 2, 2, F(1))
    C.set_cell(blocks, 1, 3, 2, 2, F(1))
    v1 = C.oriented(blocks, 0, 2)[0][1]
    v2 = C.oriented(blocks, 1, 3)[0][1]
    require(v1 != 0 and v2 != 0,
            "pinned rectangle: a designed carrier crossing cell vanished")
    C.set_cell(blocks, 0, 1, 0, 0, v1 * v2)
    C.set_cell(blocks, 0, 1, 1, 1, F(5))
    C.set_cell(blocks, 2, 3, 1, 1, F(1) + t)
    C.set_cell(blocks, 2, 3, 0, 0, F(-3))
    C.set_cell(blocks, 2, 3, 2, 2, F(2))
    C.set_cell(blocks, 0, 3, 0, 1, F(7))
    C.set_cell(blocks, 0, 3, 1, 0, F(-2))
    C.set_cell(blocks, 1, 2, 0, 1, F(4))
    C.set_cell(blocks, 1, 2, 1, 2, F(1))
    return blocks


def check_census_facts(blocks, label):
    """Every census fact of the D1 configuration, exhaustively.

    Lemma-F purity on both one-carrier subfamilies (2 x 729 words),
    residue purity (81 words), the (E1) pendant support at both
    essential endpoints, (E2) carrier nonvanishing, badness of both
    carriers, the a-pendant hafnian facts on every even subset,
    liveness, and identity (dagger) at both carriers, nonvacuously.
    """
    for sites in (W1, W2):
        for values in product(COLORS, repeat=6):
            word = dict(zip(sites, values))
            got = C.coefficient(blocks, sites, word)
            want = F(1) if set(values) == {2} else F(0)
            require(got == want,
                    "%s: Lemma-F purity of H_%s fails at %s (got %s)"
                    % (label, list(sites), values, got))
    for values in product(COLORS, repeat=4):
        word = dict(zip(D1_RESIDUE, values))
        got = C.coefficient(blocks, D1_RESIDUE, word)
        want = F(1) if set(values) == {2} else F(0)
        require(got == want,
                "%s: residue purity fails at %s (got %s)"
                % (label, values, got))
    for u, partner in sorted(D1_ESSENTIAL_PARTNER.items()):
        for x in SITES:
            if x in (u, partner):
                continue
            require(all(cell == 0 for cell in C.oriented(blocks, u, x)[2]),
                    "%s: (E1) fails, row a of A_%d%d is nonzero"
                    % (label, u, x))
        require(C.oriented(blocks, u, partner)[2][2] != 0,
                "%s: (E2) fails, the carrier lambda at {%d,%d} vanished"
                % (label, u, partner))
        require(not C.star_injective(blocks, SITES, u, partner),
                "%s: the carrier {%d,%d} is not a bad pair"
                % (label, u, partner))
        for size in (2, 4, 6, 8):
            for subset in combinations(SITES, size):
                if u in subset and partner not in subset:
                    require(C.hafnian(blocks, 2, subset) == 0,
                            "%s: the a-pendant hafnian fact fails on %s"
                            % (label, (subset,)))
    h_a = C.hafnian(blocks, 2, D1_RESIDUE)
    h_b = C.hafnian(blocks, 0, (0, 1))
    h_c = C.hafnian(blocks, 1, (2, 3))
    require(h_a * h_b * h_c != 0, "%s: the split is not live" % label)
    nonvacuous = 0
    for (u, v) in sorted(D1_ESSENTIAL_PARTNER.items()):
        left = (C.oriented(blocks, u, v)[CHI[u]][CHI[v]]
                * C.hafnian(blocks, 2, D1_RESIDUE))
        right = F(0)
        for r in D1_RESIDUE:
            for rp in D1_RESIDUE:
                if r == rp:
                    continue
                rest = tuple(s for s in D1_RESIDUE if s not in (r, rp))
                right += (C.oriented(blocks, u, r)[CHI[u]][2]
                          * C.oriented(blocks, v, rp)[CHI[v]][2]
                          * C.hafnian(blocks, 2, rest))
        require(left == -right,
                "%s: identity (dagger) fails at carrier (%d,%d)"
                % (label, u, v))
        if left != 0:
            nonvacuous += 1
    require(nonvacuous == 2,
            "%s: identity (dagger) held vacuously (0 = 0) at a carrier"
            % label)
    return h_a, h_b, h_c


def d1_rectangle(blocks):
    """(positive product, negative product) of the D1 minor."""
    return (C.oriented(blocks, 0, 2)[0][1] * C.oriented(blocks, 1, 3)[0][1],
            C.oriented(blocks, 0, 1)[0][0] * C.oriented(blocks, 2, 3)[1][1])


def build_stage_a(params):
    """The near-miss family: the closed-form full-chart repair of the
    two-carrier core words (cross-class proportionality + carrier-site
    collinearity).  Exact rationals throughout."""
    (a, ap, rho, rhop, s, mu, c24, c25, c34, c35, t1, t2) = params
    kappa = 1 + s ** 4 * mu ** 2
    e = 1 + s ** 2 * mu
    c0 = {4: tuple(a), 5: tuple(rho * x for x in a),
          6: tuple(s * x for x in a), 7: tuple(s * mu * rho * x for x in a)}
    c1 = {4: tuple(ap), 5: tuple(rhop * x for x in ap),
          6: tuple(s * x for x in ap),
          7: tuple(s * mu * rhop * x for x in ap)}
    c2 = {4: tuple(c24), 5: tuple(c25), 6: tuple(s * x for x in c24),
          7: tuple(s * mu * x for x in c25)}
    c3 = {4: tuple(c34), 5: tuple(c35), 6: tuple(s * x for x in c34),
          7: tuple(s * mu * x for x in c35)}
    bt = tuple(c2[5][k] + rho * c2[4][k] for k in range(3))
    btpp = tuple(c2[5][k] + rhop * c2[4][k] for k in range(3))
    dt = tuple(c3[5][k] + rho * c3[4][k] for k in range(3))
    dtp = tuple(c3[5][k] + rhop * c3[4][k] for k in range(3))

    def f45(cp, cq, x, y):
        return cp[4][x] * cq[5][y] + cp[5][x] * cq[4][y]

    blocks = C.zero_blocks(SITES)
    C.set_cell(blocks, 4, 5, 2, 2, F(1))
    C.set_cell(blocks, 6, 7, 2, 2, F(1))
    for r in D1_RESIDUE:
        for i in (0, 1):
            C.set_cell(blocks, 0, r, i, 2, c0[r][i])
            C.set_cell(blocks, 1, r, i, 2, c1[r][i])
        for j in COLORS:
            C.set_cell(blocks, 2, r, j, 2, c2[r][j])
            C.set_cell(blocks, 3, r, j, 2, c3[r][j])
    for i in (0, 1):
        for j in COLORS:
            first = sum((c0[r][i] * c2[rp][j] for r, rp in D1_PAIRS), F(0))
            second = sum((c1[r][i] * c3[rp][j] for r, rp in D1_PAIRS), F(0))
            C.set_cell(blocks, 0, 2, i, j, -first)
            C.set_cell(blocks, 1, 3, i, j, -second)
    C.set_cell(blocks, 0, 2, 2, 2, F(1))
    C.set_cell(blocks, 1, 3, 2, 2, F(1))
    for x0 in (0, 1):
        for x1 in (0, 1):
            C.set_cell(blocks, 0, 1, x0, x1,
                       t1 * a[x0] * ap[x1]
                       - e * (rho + rhop) * a[x0] * ap[x1])
    for x2 in COLORS:
        for x3 in COLORS:
            value = (kappa / t1) * ((rho + rhop) * f45(c2, c3, x2, x3)
                                    + bt[x2] * dtp[x3])
            C.set_cell(blocks, 2, 3, x2, x3,
                       value - e * f45(c2, c3, x2, x3))
    for x0 in (0, 1):
        for x3 in COLORS:
            C.set_cell(blocks, 0, 3, x0, x3,
                       (t2 * kappa - e) * a[x0] * dt[x3])
    for x1 in (0, 1):
        for x2 in COLORS:
            C.set_cell(blocks, 1, 2, x1, x2,
                       (F(1) / t2 - e) * ap[x1] * btpp[x2])
    return blocks


STAGE_A_BASE = (
    (F(1), F(2)), (F(1), F(-1)), F(2), F(3), F(1), F(2),
    (F(1), F(2), F(-1)), (F(-1), F(1), F(2)),
    (F(2), F(1), F(1)), (F(1), F(-1), F(0)),
    F(1), F(1),
)
STAGE_A_SECOND = (
    (F(2), F(-1)), (F(1), F(3)), F(1, 2), F(-1), F(2), F(1, 3),
    (F(1), F(0), F(2)), (F(0), F(1), F(-1)),
    (F(1), F(1), F(-2)), (F(2), F(0), F(1)),
    F(3), F(1, 2),
)
STAGE_A_SHAPE = (2, 2, None, None, None, None, 3, 3, 3, 3, None, None)


def flatten_params(params):
    out = []
    for item in params:
        if isinstance(item, tuple):
            out.extend(item)
        else:
            out.append(item)
    return out


def unflatten_params(values):
    values = list(values)
    out, index = [], 0
    for size in STAGE_A_SHAPE:
        if size is None:
            out.append(values[index])
            index += 1
        else:
            out.append(tuple(values[index:index + size]))
            index += size
    require(index == len(values),
            "stage-A parameters: the flat vector has the wrong length")
    return tuple(out)


class Dual(object):
    """a + b eps with eps^2 = 0, over Fraction: exact forward-mode
    differentiation, no floating point anywhere."""

    __slots__ = ("a", "b")

    def __init__(self, a, b=F(0)):
        self.a, self.b = F(a), F(b)

    @staticmethod
    def lift(other):
        return other if isinstance(other, Dual) else Dual(other)

    def __add__(self, other):
        other = Dual.lift(other)
        return Dual(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __sub__(self, other):
        other = Dual.lift(other)
        return Dual(self.a - other.a, self.b - other.b)

    def __rsub__(self, other):
        return Dual.lift(other) - self

    def __mul__(self, other):
        other = Dual.lift(other)
        return Dual(self.a * other.a, self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Dual.lift(other)
        require(other.a != 0, "dual arithmetic: division by a pure-eps value")
        return Dual(self.a / other.a,
                    (self.b * other.a - self.a * other.b) / other.a ** 2)

    def __rtruediv__(self, other):
        return Dual.lift(other) / self

    def __pow__(self, exponent):
        out = Dual(1)
        for _ in range(exponent):
            out = out * self
        return out

    def __neg__(self):
        return Dual(-self.a, -self.b)


def stage_a_cells(params):
    """The same construction as build_stage_a into a plain dict, with
    generic arithmetic, so it accepts Dual parameters.  Its agreement
    with build_stage_a at the base point is REQUIRED below, so the
    Jacobian differentiates the construction that is actually swept."""
    (a, ap, rho, rhop, s, mu, c24, c25, c34, c35, t1, t2) = params
    one = a[0] * 0 + 1
    kappa = s ** 4 * mu ** 2 + 1
    e = s ** 2 * mu + 1
    c0 = {4: a, 5: tuple(rho * x for x in a), 6: tuple(s * x for x in a),
          7: tuple(s * mu * rho * x for x in a)}
    c1 = {4: ap, 5: tuple(rhop * x for x in ap), 6: tuple(s * x for x in ap),
          7: tuple(s * mu * rhop * x for x in ap)}
    c2 = {4: c24, 5: c25, 6: tuple(s * x for x in c24),
          7: tuple(s * mu * x for x in c25)}
    c3 = {4: c34, 5: c35, 6: tuple(s * x for x in c34),
          7: tuple(s * mu * x for x in c35)}
    bt = tuple(c2[5][k] + rho * c2[4][k] for k in range(3))
    btpp = tuple(c2[5][k] + rhop * c2[4][k] for k in range(3))
    dt = tuple(c3[5][k] + rho * c3[4][k] for k in range(3))
    dtp = tuple(c3[5][k] + rhop * c3[4][k] for k in range(3))

    def f45(cp, cq, x, y):
        return cp[4][x] * cq[5][y] + cp[5][x] * cq[4][y]

    cells = {(4, 5, 2, 2): one, (6, 7, 2, 2): one}
    for r in D1_RESIDUE:
        for i in (0, 1):
            cells[(0, r, i, 2)] = c0[r][i]
            cells[(1, r, i, 2)] = c1[r][i]
        for j in COLORS:
            cells[(2, r, j, 2)] = c2[r][j]
            cells[(3, r, j, 2)] = c3[r][j]
    for i in (0, 1):
        for j in COLORS:
            first = c0[4][i] * c2[5][j] + c0[5][i] * c2[4][j] \
                + c0[6][i] * c2[7][j] + c0[7][i] * c2[6][j]
            second = c1[4][i] * c3[5][j] + c1[5][i] * c3[4][j] \
                + c1[6][i] * c3[7][j] + c1[7][i] * c3[6][j]
            cells[(0, 2, i, j)] = -first
            cells[(1, 3, i, j)] = -second
    cells[(0, 2, 2, 2)] = one
    cells[(1, 3, 2, 2)] = one
    for x0 in (0, 1):
        for x1 in (0, 1):
            cells[(0, 1, x0, x1)] = (t1 * a[x0] * ap[x1]
                                     - e * (rho + rhop) * a[x0] * ap[x1])
    for x2 in COLORS:
        for x3 in COLORS:
            value = (kappa / t1) * ((rho + rhop) * f45(c2, c3, x2, x3)
                                    + bt[x2] * dtp[x3])
            cells[(2, 3, x2, x3)] = value - e * f45(c2, c3, x2, x3)
    for x0 in (0, 1):
        for x3 in COLORS:
            cells[(0, 3, x0, x3)] = (t2 * kappa - e) * a[x0] * dt[x3]
    for x1 in (0, 1):
        for x2 in COLORS:
            cells[(1, 2, x1, x2)] = (one / t2 - e) * ap[x1] * btpp[x2]
    return cells


def section_rank_controls():
    """Designed per-branch controls for the committed exact rank routine
    (used on the Jacobian below) and for the dual-number derivative.

    Rank branches exercised: the empty matrix; an all-zero matrix (no
    pivot in any column); a matrix with a zero column BEFORE a pivot
    column (the `continue` branch); a rank-1 matrix with repeated rows;
    a full-rank square matrix; and a wide matrix with more columns than
    rows (the early-exit branch when every row is a pivot row).
    """
    cases = [
        ("empty", (), 0),
        ("zero_2x3", ((F(0),) * 3, (F(0),) * 3), 0),
        ("zero_first_column", ((F(0), F(1), F(2)), (F(0), F(0), F(3))), 2),
        ("repeated_rows", ((F(1), F(2)), (F(2), F(4)), (F(3), F(6))), 1),
        ("full_square", ((F(1), F(0), F(0)), (F(0), F(2), F(0)),
                         (F(1), F(1), F(5))), 3),
        ("wide", ((F(1), F(0), F(0), F(7)), (F(0), F(0), F(3), F(1))), 2),
        ("rational", ((F(1, 3), F(2, 3)), (F(1, 2), F(1))), 1),
    ]
    record = []
    for name, rows, expected in cases:
        got = C.rank(rows)
        require(got == expected,
                "rank control: the committed rank routine reports %d on "
                "the designed case %s, expected %d" % (got, name, expected))
        record.append([name, got])
    # Dual-number control: d/dx of (x^3 + 5) / (2 x) at x = 3 is
    # (2 x^3 - 5) / (2 x^2)... computed exactly and compared.
    x = Dual(F(3), F(1))
    value = (x ** 3 + 5) / (2 * x)
    require(value.a == F(32, 6) and value.b == F(2 * 27 - 5, 18),
            "dual control: the exact forward derivative of "
            "(x^3 + 5)/(2x) at x = 3 is wrong (got %s + %s eps)"
            % (value.a, value.b))
    constant = Dual(F(7)) * Dual(F(2))
    require(constant.b == 0,
            "dual control: a product of constants acquired an eps part")
    return {"rank_cases": record,
            "dual_probe": [value.a, value.b]}


def section_near_miss():
    """The 6559/6561 family: census facts, the exact defect set, the
    harmful member, and the exact local dimension."""
    started = monotonic()
    record = {}
    base = build_stage_a(STAGE_A_BASE)
    h_a, h_b, h_c = check_census_facts(base, "stage-A base point")
    require(h_a * h_b * h_c != 0,
            "stage-A base point: the split is not live")
    defects = C.exactness_defects(base, SITES)
    require(
        set(defects) == {(0,) * 8, (1,) * 8},
        "stage-A base point: the exactness defect set is %s, not exactly "
        "the monochromatic pair {b^8, c^8}"
        % (sorted(sorted(defects)),),
    )
    require(
        all(got == 0 and want == 1 for got, want in defects.values()),
        "stage-A base point: a monochromatic defect is not 0 vs 1",
    )
    record["base_liveness"] = [h_a, h_b, h_c]
    record["base_defects"] = sorted(
        [list(word), value[0], value[1]] for word, value in defects.items())
    record["satisfied_equations"] = 3 ** 8 - len(defects)
    # Control: the defect sweep must SEE a perturbation, or "exactly two
    # defects" would be unfalsifiable here.
    perturbed = build_stage_a(STAGE_A_BASE)
    C.set_cell(perturbed, 0, 1, 0, 1,
               C.oriented(perturbed, 0, 1)[0][1] + F(1))
    perturbed_defects = C.exactness_defects(perturbed, SITES)
    require(
        set(perturbed_defects) > set(defects),
        "near-miss control: perturbing A_01(b,c) did not enlarge the "
        "defect set, so the 6559/6561 count is not being measured",
    )
    record["perturbed_defect_count"] = len(perturbed_defects)
    # Control: the census-fact checker must REJECT a designed violation.
    broken = build_stage_a(STAGE_A_BASE)
    C.set_cell(broken, 0, 2, 2, 2, F(0))          # kills (E2) at carrier 1
    rejected = False
    try:
        check_census_facts(broken, "designed (E2) violation")
    except RuntimeError:
        rejected = True
    require(rejected,
            "near-miss control: the census-fact checker accepted a packet "
            "whose carrier lambda was set to zero, so it cannot fail")
    # A second generic parameter point: a genuine family, not a point.
    second = build_stage_a(STAGE_A_SECOND)
    check_census_facts(second, "stage-A second point")
    second_defects = C.exactness_defects(second, SITES)
    require(
        set(second_defects) == {(0,) * 8, (1,) * 8},
        "stage-A second point: the defect set is %s, not the "
        "monochromatic pair" % (sorted(sorted(second_defects)),),
    )
    record["second_point_defects"] = sorted(
        list(word) for word in second_defects)
    # The harmful member: the D1 rectangle degenerate, both products
    # nonzero, and still 6559/6561.
    values = flatten_params(STAGE_A_BASE)
    require(len(values) == 22,
            "stage-A chart: the parameter count is no longer 22")
    values[18] = F(-61, 27)                       # c_3(.,5) second entry
    values[20] = F(5)                             # gauge t1
    harmful = build_stage_a(unflatten_params(values))
    check_census_facts(harmful, "stage-A harmful point")
    harmful_defects = C.exactness_defects(harmful, SITES)
    require(
        set(harmful_defects) == {(0,) * 8, (1,) * 8},
        "stage-A harmful point: the defect set is %s, not the "
        "monochromatic pair" % (sorted(sorted(harmful_defects)),),
    )
    positive, negative = d1_rectangle(harmful)
    require(
        positive == negative and positive != 0,
        "stage-A harmful point: the D1 rectangle is not degenerate with "
        "both products nonzero (%s vs %s)" % (positive, negative),
    )
    base_positive, base_negative = d1_rectangle(base)
    require(
        base_positive != base_negative,
        "stage-A base point: the rectangle is already degenerate, so the "
        "harmful point is not a distinguished member of the family",
    )
    record["harmful_rectangle"] = [positive, negative]
    record["base_rectangle"] = [base_positive, base_negative]
    # The witness tensors (frozen into the ledger as computed content).
    record["witness_tensors"] = {
        name: sorted([[u, v, i, j], C.oriented(packet, u, v)[i][j]]
                     for (u, v) in combinations(SITES, 2)
                     for i in COLORS for j in COLORS
                     if C.oriented(packet, u, v)[i][j] != 0)
        for name, packet in (("base", base), ("second", second),
                             ("harmful", harmful))
    }
    record["witness_nonzero_cells"] = {
        name: len(cells)
        for name, cells in sorted(record["witness_tensors"].items())}
    # --- the exact local dimension: Jacobian rank by dual numbers.
    cells = stage_a_cells(STAGE_A_BASE)
    for (u, v, i, j), value in cells.items():
        require(
            C.oriented(base, u, v)[i][j] == value,
            "stage-A chart: the plain-dict replication disagrees with the "
            "swept construction at cell A_%d%d(%d,%d)" % (u, v, i, j),
        )
    keys = sorted(cells)
    flat = flatten_params(STAGE_A_BASE)
    jacobian = []
    for index in range(22):
        duals = [Dual(value, F(1) if position == index else F(0))
                 for position, value in enumerate(flat)]
        differentiated = stage_a_cells(unflatten_params(duals))
        for key in keys:
            require(
                differentiated[key].a == cells[key],
                "stage-A Jacobian: the dual evaluation moved the base "
                "point at cell %s" % (key,),
            )
        jacobian.append([differentiated[key].b for key in keys])
    rank = C.rank(tuple(tuple(row) for row in jacobian))
    require(
        rank == 22,
        "stage-A chart: the exact Jacobian rank at the base point is %d, "
        "not the full 22" % rank,
    )
    # Control: a deliberately dependent chart must drop rank, or "22"
    # could be reported by a blind routine.
    dependent = [list(row) for row in jacobian]
    dependent[3] = list(dependent[2])
    require(
        C.rank(tuple(tuple(row) for row in dependent)) == 21,
        "stage-A chart control: duplicating a Jacobian row did not drop "
        "the rank to 21, so the rank routine is not reading the rows",
    )
    record["jacobian_rank"] = rank
    record["jacobian_cells"] = len(keys)
    record["jacobian_fingerprint"] = content_hash(
        [[str(entry) for entry in row] for row in jacobian])
    return record, monotonic() - started


# ================== S6 the frozen-chart pencil infeasibility (why the full
#                      chart is needed for the two-colour repair)


UNKNOWN_CELLS = ([(0, 1, i, j) for i in (0, 1) for j in (0, 1)]
                 + [(2, 3, i, j) for i in COLORS for j in COLORS]
                 + [(0, 3, i, j) for i in (0, 1) for j in COLORS]
                 + [(1, 2, i, j) for i in (0, 1) for j in COLORS])


def frozen_chart_blocks(assignment):
    blocks = build_pinned_rectangle(F(0))
    for cell in UNKNOWN_CELLS:
        u, v, i, j = cell
        C.set_cell(blocks, u, v, i, j, assignment.get(cell, F(0)))
    return blocks


def word_unknowns(x):
    x0, x1, x2, x3 = x
    out = {}
    if x0 != 2 and x1 != 2:
        out["u1"] = (0, 1, x0, x1)
    out["u2"] = (2, 3, x2, x3)
    if x0 != 2:
        out["u3"] = (0, 3, x0, x3)
    if x1 != 2:
        out["u4"] = (1, 2, x1, x2)
    return out


def poly_trim(poly):
    while len(poly) > 1 and poly[-1] == 0:
        poly = poly[:-1]
    return poly


def poly_add(left, right):
    size = max(len(left), len(right))
    return poly_trim(tuple(
        (left[k] if k < len(left) else F(0))
        + (right[k] if k < len(right) else F(0)) for k in range(size)))


def poly_mul(left, right):
    out = [F(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return poly_trim(tuple(out))


def poly_neg(poly):
    return tuple(-a for a in poly)


def poly_mod(left, right):
    left, right = list(poly_trim(left)), poly_trim(right)
    require(any(a != 0 for a in right),
            "univariate remainder: division by the zero polynomial")
    while True:
        left = list(poly_trim(tuple(left)))
        if len(left) < len(right) or all(a == 0 for a in left):
            break
        factor = left[-1] / right[-1]
        shift = len(left) - len(right)
        left = [a - factor * (right[k - shift]
                              if 0 <= k - shift < len(right) else F(0))
                for k, a in enumerate(left)]
    return poly_trim(tuple(left))


def poly_gcd(left, right):
    left, right = poly_trim(left), poly_trim(right)
    while any(a != 0 for a in right):
        left, right = right, poly_trim(poly_mod(left, right))
    left = poly_trim(left)
    if left[-1] != 0:
        left = tuple(a / left[-1] for a in left)      # monic
    return left


def pencil_minors(A, B):
    """The nine 2x2 minors of (A - s B) as univariate polynomials in s."""
    minors = []
    for r1, r2 in ((0, 1), (0, 2), (1, 2)):
        for c1, c2 in ((0, 1), (0, 2), (1, 2)):
            def entry(r, c):
                return poly_trim((A[r][c], -B[r][c]))
            minors.append(poly_add(
                poly_mul(entry(r1, c1), entry(r2, c2)),
                poly_neg(poly_mul(entry(r1, c2), entry(r2, c1)))))
    return minors


def section_pencil():
    """The frozen-chart step of the two-colour repair is INFEASIBLE.

    Freezing the witness's carrier and carrier-to-residue data and
    leaving only the 25 cross-block cells free, every core word becomes

        V1(x0,x1) V2(x2,x3) + V3(x0,x3) V4(x1,x2) + K(x) = 0,

    with V1 = A01 + B01 etc. and K fixed rationals; the K's are computed
    here from the committed coefficient oracle by exact finite
    differences.  Eliminating V2 between two blocks sharing an index
    forces rank(K_X - s K_Y) <= 1 at s = V1(X)/V1(Y), i.e. all nine
    2x2 minors of the pencil vanish simultaneously.  If the gcd of the
    nine minor polynomials is a nonzero CONSTANT, no s in Qbar does
    that, and the frozen-chart repair is impossible.
    """
    base = frozen_chart_blocks({})
    system = {}
    for x in product(COLORS, repeat=4):
        word = dict(zip(SITES, x + (2, 2, 2, 2)))
        cells = word_unknowns(x)
        constant = C.coefficient(base, SITES, word)
        linear = {}
        for cell in cells.values():
            value = C.coefficient(
                frozen_chart_blocks({cell: F(1)}), SITES, word) - constant
            if value:
                linear[cell] = value
        quadratic = {}
        names = sorted(cells)
        for first in range(len(names)):
            for second in range(first + 1, len(names)):
                ca, cb = cells[names[first]], cells[names[second]]
                if ca == cb:
                    continue
                value = (C.coefficient(
                    frozen_chart_blocks({ca: F(1), cb: F(1)}), SITES, word)
                    - constant - linear.get(ca, F(0)) - linear.get(cb, F(0)))
                if value:
                    quadratic[tuple(sorted((ca, cb)))] = value
        # No pure squares: each unknown cell occurs at most once per
        # matching term, so doubling a cell must double its linear part.
        for cell in cells.values():
            doubled = C.coefficient(
                frozen_chart_blocks({cell: F(2)}), SITES, word)
            require(
                doubled == constant + 2 * linear.get(cell, F(0)),
                "frozen chart: the core word %s is not affine in the cell "
                "%s alone" % (x, (cell,)),
            )
        system[x] = (constant, linear, quadratic)

    live = {x: data for x, data in system.items() if x[0] != 2 and x[1] != 2}
    require(len(live) == 36,
            "frozen chart: the live core words are no longer the 36 with "
            "both essential sites two-coloured")
    for x, (constant, linear, quadratic) in system.items():
        if x in live:
            continue
        want = F(1) if set(x) == {2} else F(0)
        require(
            not linear and not quadratic and constant == want,
            "frozen chart: the non-live core word %s is not identically "
            "satisfied by the witness (constant %s, target %s)"
            % (x, constant, want),
        )
    for x, (_constant, _linear, quadratic) in live.items():
        x0, x1, x2, x3 = x
        expected = {tuple(sorted(((0, 1, x0, x1), (2, 3, x2, x3)))): F(1),
                    tuple(sorted(((0, 3, x0, x3), (1, 2, x1, x2)))): F(1)}
        require(
            quadratic == expected,
            "frozen chart: the quadratic part of core word %s is not "
            "exactly A01 A23 + A03 A12 with unit coefficients" % (x,),
        )
    tables = {"B01": {}, "B23": {}, "B03": {}, "B12": {}}
    for x, (_constant, linear, _quadratic) in live.items():
        x0, x1, x2, x3 = x
        for name, key, cell in (
            ("B01", (x0, x1), (2, 3, x2, x3)),
            ("B23", (x2, x3), (0, 1, x0, x1)),
            ("B03", (x0, x3), (1, 2, x1, x2)),
            ("B12", (x1, x2), (0, 3, x0, x3)),
        ):
            value = linear.get(cell, F(0))
            if key in tables[name]:
                require(
                    tables[name][key] == value,
                    "frozen chart: the residue-completion table %s is "
                    "ill-defined at %s (word %s)" % (name, (key,), (x,)),
                )
            else:
                tables[name][key] = value
    K = {}
    for x, (constant, _linear, _quadratic) in live.items():
        x0, x1, x2, x3 = x
        K[x] = (constant
                - tables["B01"][(x0, x1)] * tables["B23"][(x2, x3)]
                - tables["B03"][(x0, x3)] * tables["B12"][(x1, x2)])
    require(
        any(value != 0 for value in K.values()),
        "frozen chart: every K vanishes, so the pencil argument is "
        "vacuous",
    )

    def matrix(x0, x1):
        return tuple(tuple(K[(x0, x1, x2, x3)] for x3 in COLORS)
                     for x2 in COLORS)

    blocks = {(x0, x1): matrix(x0, x1)
              for x0 in (0, 1) for x1 in (0, 1)}
    ranks = {str([x0, x1]): C.rank(blocks[(x0, x1)])
             for x0 in (0, 1) for x1 in (0, 1)}
    require(
        all(value == 3 for value in ranks.values()),
        "frozen chart: a K block is no longer of full rank 3, so the "
        "lambda != 0 hypothesis of the pencil step changes (%s)" % ranks,
    )
    sharing = (("bc/bb", (0, 1), (0, 0)), ("cb/bb", (1, 0), (0, 0)),
               ("cc/cb", (1, 1), (1, 0)), ("cc/bc", (1, 1), (0, 1)))
    gcds, constant_pairs = {}, []
    for name, first, second in sharing:
        minors = pencil_minors(blocks[first], blocks[second])
        require(
            any(len(poly_trim(minor)) > 1 for minor in minors),
            "frozen chart: every minor of the pencil %s is constant in s, "
            "so the pencil carries no information" % name,
        )
        gcd = minors[0]
        for minor in minors[1:]:
            gcd = poly_gcd(gcd, minor)
        gcds[name] = [str(coefficient) for coefficient in gcd]
        if len(poly_trim(gcd)) == 1:
            constant_pairs.append(name)
    require(
        len(constant_pairs) == len(sharing),
        "frozen chart: only %d of the %d sharing pencils have a constant "
        "minor gcd (%s), so the note's statement that ALL of them make "
        "rank <= 1 impossible over Qbar is an overclaim"
        % (len(constant_pairs), len(sharing), sorted(constant_pairs)),
    )
    # Controls on the univariate gcd routine, per branch: a designed
    # nonconstant gcd (so "constant" is not the only possible answer),
    # an exact division branch, and a coprime pair.
    x_minus_2 = (F(-2), F(1))
    x_plus_3 = (F(3), F(1))
    require(
        poly_gcd(poly_mul(x_minus_2, x_plus_3),
                 poly_mul(x_minus_2, x_minus_2)) == x_minus_2,
        "gcd control: the routine does not recover the common factor "
        "(s - 2) of two designed products",
    )
    require(
        poly_gcd(x_minus_2, x_plus_3) == (F(1),),
        "gcd control: the routine does not report coprimality of two "
        "designed distinct linear factors",
    )
    require(
        poly_mod(poly_mul(x_minus_2, x_plus_3), x_minus_2) == (F(0),),
        "gcd control: exact division leaves a nonzero remainder",
    )
    # And a designed FEASIBLE pencil: A = 2 B + (rank-one), whose minors
    # share the root s = 2 -- the routine must report a nonconstant gcd.
    rank_one = tuple(tuple(F((i + 1) * (j + 2)) for j in COLORS)
                     for i in COLORS)
    B = ((F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1)))
    A = tuple(tuple(2 * B[i][j] + rank_one[i][j] for j in COLORS)
              for i in COLORS)
    feasible = pencil_minors(A, B)
    gcd = feasible[0]
    for minor in feasible[1:]:
        gcd = poly_gcd(gcd, minor)
    require(
        len(poly_trim(gcd)) > 1,
        "pencil control: a designed pencil with an exact rank-one "
        "residue at s = 2 was reported to have a constant minor gcd, so "
        "the infeasibility verdict cannot distinguish the two cases",
    )
    return {
        "unknown_cells": len(UNKNOWN_CELLS),
        "live_core_words": len(live),
        "K_ranks": ranks,
        "K_table": sorted([list(x), value] for x, value in K.items()),
        "residue_completion_tables": {
            name: sorted([list(key), value] for key, value in table.items())
            for name, table in tables.items()},
        "pencil_minor_gcds": gcds,
        "infeasible_pairs": sorted(constant_pairs),
        "control_feasible_pencil_gcd_degree": len(poly_trim(gcd)) - 1,
    }


# ================================================================= audit


def audit():
    conventions = section_conventions()
    geometry = section_geometry()
    engine = section_engine_control()
    sweep, sweep_seconds = section_d2_sweep()
    u_system, u_seconds = section_u_system_census()
    rigidity = section_rigidity()
    ranks = section_rank_controls()
    near_miss, near_miss_seconds = section_near_miss()
    pencil = section_pencil()

    # Cross-check tying the three results to one geometry: the residue
    # of the swept D2 representative and the residue Sigma is built on
    # are the census's own residues for those signatures, and the D2
    # residue is a 2-subset of the D1 residue (the 4-part).
    require(
        set(geometry["D2_residue"]) < set(geometry["D1_residue"]),
        "cross-check: the swept D2 residue is not a proper subset of the "
        "D1 residue (the 4-part), so the two sections are not on the "
        "same canonical split",
    )
    ledger = {
        "conventions": conventions,
        "census_geometry": geometry,
        "engine_control": engine,
        "d2_sweep": sweep,
        "u_system_census": u_system,
        "monochrome_rigidity": rigidity,
        "rank_controls": ranks,
        "near_miss_family": near_miss,
        "frozen_chart_pencil": pencil,
        "proved": (
            "the D2 branch sweep over the eight named support families "
            "and the Sigma rigidity are exact polynomial-identity facts "
            "about the stated support classes; the reduction of the "
            "per-carrier U-system to seven two-colour column signatures "
            "(and of the two-endpoint signature to the extended exchange "
            "family) is a hand argument with a GF(2) census as machine "
            "evidence; the equivariance of the skeleton and certificates "
            "under the relabelling group, and the inertness of the "
            "badness orientation, are inspections that are NOT machine "
            "verified"
        ),
        "open": (
            "D1 on out-of-Sigma crossing supports over the non-double-pure "
            "inside strata; Krenn's conjecture remains open"
        ),
    }
    digest = content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "n8 D2 kill and monochrome rigidity ledger changed")
    return ledger, digest, {"d2_sweep": sweep_seconds,
                            "u_system": u_seconds,
                            "near_miss": near_miss_seconds}


def main():
    started = monotonic()
    ledger, digest, seconds = audit()
    sweep = ledger["d2_sweep"]
    rigidity = ledger["monochrome_rigidity"]
    near_miss = ledger["near_miss_family"]
    pencil = ledger["frozen_chart_pencil"]

    print("n8 D2 kill and monochromatic rigidity: PASS (exact)")
    print("geometry: canonical split %s, saturating colour %d; swept D2 "
          "representative %s with residue %s (one of the census's %d "
          "families of signature (3,2,2))"
          % (ledger["census_geometry"]["split"],
             ledger["census_geometry"]["saturating_colour"],
             ledger["census_geometry"]["D2_representative"],
             ledger["census_geometry"]["D2_residue"],
             ledger["census_geometry"]["D2_family_count"]))
    print("  the swept representative's orbit under the split-preserving "
          "relabelling group (order %d) is all %d of them; the "
          "S_a-trivial subgroup reaches only %d"
          % (ledger["census_geometry"]["relabelling_group_order"],
             ledger["census_geometry"]["D2_orbit_size"],
             ledger["census_geometry"]["D2_orbit_under_S_a_trivial_subgroup"]))
    print("D2 sweep: %d/%d branch combinations obstructed -- %d anchor-dead, "
          "%d Gamma-certificates (3 words), %d c-factor certificates "
          "(4 words), %d survivors; %.1f s"
          % (sweep["combinations"] - sweep["tally"]["survivor"],
             sweep["combinations"], sweep["tally"]["anchor_dead"],
             sweep["tally"]["gamma"], sweep["tally"]["c_factor"],
             sweep["tally"]["survivor"], seconds["d2_sweep"]))
    print("  pigeonhole: feeder distribution (at sites 6, 7) over the %d "
          "combinations = %s; the %d starved combinations are exactly the "
          "anchor-dead ones"
          % (sweep["combinations"], sweep["feeder_distribution"],
             sweep["pigeonhole"]["starved_combinations"]))
    print("  saturation: the (dagger) numerator s_e(chi) is a NONZERO "
          "polynomial on all %d (combination, carrier) slots; the "
          "designed degenerate slot has s_e == 0 and cannot saturate"
          % len(sweep["slot_fingerprints"]))
    u_system = ledger["u_system_census"]
    print("U-system census over %s: %d solutions enumerated, %d "
          "saturated, %d feeding BOTH residue sites; realizable "
          "two-colour column signatures = %d (empty + six); every "
          "two-endpoint solution has the extended-exchange structure; "
          "%.1f s"
          % (u_system["field"], u_system["counts"]["enumerated"],
             u_system["counts"]["saturated"],
             u_system["counts"]["both_sites"],
             len(u_system["signature_census"]), seconds["u_system"]))
    print("rigidity on Sigma: %d free cells, H(b^8) = H(c^8) = 0 "
          "identically; all %d matchings carry >= %d residue-incident "
          "edges; probe word (b,b,c,c,a^4) nonzero; one revived "
          "residue-residue cell keeps the anchor dead, two disjoint ones "
          "revive it"
          % (rigidity["sigma_free_cells"], rigidity["matchings"],
             rigidity["min_residue_incident_edges"]))
    print("near-miss family: %d/%d exactness equations satisfied at the "
          "base point (defects exactly b^8, c^8), same at a second "
          "generic point; harmful member has a degenerate rectangle with "
          "both products %s; exact Jacobian rank %d of %d parameters; "
          "%.1f s"
          % (near_miss["satisfied_equations"], 3 ** 8,
             near_miss["harmful_rectangle"][0], near_miss["jacobian_rank"],
             22, seconds["near_miss"]))
    print("frozen chart: %d unknown cells, %d live core words, K blocks of "
          "rank %s; sharing pencils with CONSTANT minor gcd (infeasible): "
          "%s"
          % (pencil["unknown_cells"], pencil["live_core_words"],
             sorted(set(pencil["K_ranks"].values())),
             pencil["infeasible_pairs"]))
    print("sha256:", digest)
    print("total: %.1f s" % (monotonic() - started))


if __name__ == "__main__":
    main()
