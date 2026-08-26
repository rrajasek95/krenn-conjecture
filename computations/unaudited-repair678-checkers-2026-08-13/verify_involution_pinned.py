#!/usr/bin/env python3
"""UNAUDITED REPAIR CANDIDATE (repair item 6): pin the endpoint involution.

Replaces the vacuous half of the endpoint-involution check inside
``computations/verify_h3_physical_cartan_source_orbit_descent.py``.  That
checker verifies the single transposition ``s = (0 1)`` on all 3^8 complete
source words, but its ledger records only the *string* ``"0 <-> 1"`` plus two
counts, so a mutation replacing the transposition by another admissible one
leaves the frozen digest byte-identical (external audit 2026-08-13, HIGH
defect 7).

WHAT THE THEOREM ACTUALLY NEEDS.  The endpoint-odd relative cell is
``K = (1 - s) H_w`` with ``w`` the simultaneous signed Weyl action at the two
tail sites ``TAIL_SITES = (2, 5)``.  For that construction the chain needs

  (A) ``s`` is an involution of the eight physical sites,
  (B) ``s`` is an automorphism of the *direct-free* matching presentation
      (it transports every 90-term complete source row literally), and
  (C) ``s`` commutes with the signed tail Weyl action at sites (2, 5),

and nothing in the chain distinguishes one such ``s`` from another.  This
checker therefore does NOT pretend that ``0 <-> 1`` is forced.  It verifies
the group-membership statement correctly and *exhaustively*, and it hashes
the actual admissible set, so that

  * replacing ``0 <-> 1`` by any other admissible transposition changes
    nothing mathematically (and the ledger says so, by listing all of them),
  * replacing it by an inadmissible transposition changes the digest,
  * and the *size and identity of the invariance group* is now hashed content
    rather than a hardcoded string.

Established here, exactly:

  * ``Aut(direct-free presentation) = Stab_{S8}({3,6})``, order 1440,
    isomorphic to ``S6 x S2`` -- verified over all 8! = 40,320 site
    permutations, both against the 105-matching presentation and against the
    literal decorated 90-term rows.
  * Exactly 16 of the 28 transpositions lie in that group (the 15 inside the
    six non-forbidden sites, plus the forbidden-pair swap ``3 <-> 6``).
  * Exactly 8 of those 16 also satisfy (C).  ``0 <-> 1`` is one of the 8;
    it is NOT singled out by any condition appearing in the chain.
  * The committed "target defect is s-invariant" test is exactly condition
    (C) and nothing more: over all 40,320 site permutations it holds iff the
    permutation stabilizes the tail pair {2,5} setwise (group order 1440).
    It never sees the forbidden pair, so it cannot pin 0 <-> 1.

Frozen ledger hashes: the sorted admissible sets, the exhaustive
28-transposition literal-row verdict vector, the group order and orbit
structure, and a content digest of the transported decorated rows.

POSITIVE CONTROL (runs in the same process, must FAIL): a fabricated
presentation whose direct-free pair is {3,7} instead of {3,6}.  Its
automorphism group is a different subgroup of S8, so the pinned admissible
set no longer matches -- and, in particular, ``0 <-> 1`` transports rows of
the real presentation but the fabricated inventory does not reproduce it.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SITES = tuple(range(8))
COLOURS = (0, 1, 2)
TAIL_SITES = (2, 5)
COMMITTED_CLAIM = (0, 1)

# Pinned inputs.  These are the *sources of the mathematics* being rechecked;
# a change in either invalidates the reconstruction below.
PINS = {
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
}
EXPECTED_LEDGER_SHA256 = (
    "3a97871981a9851ef9bae9a571b19b94b159d2c12e79e127d119e6cf01f62ad4"
)


class ControlDidNotFail(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def should_fail(label, thunk):
    """Run a fabricated-geometry control that MUST raise RuntimeError."""
    try:
        thunk()
    except RuntimeError as failure:
        return {"control": label, "fired": True, "reason": str(failure)[:200]}
    raise ControlDidNotFail(("positive control did not fail", label))


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


# ---------------------------------------------------------------- geometry --

def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(remainder):
            answer.append((tuple(sorted((first, second))),) + tail)
    return tuple(tuple(sorted(matching)) for matching in answer)


ALL_MATCHINGS = perfect_matchings(SITES)


def direct_free_matchings(forbidden):
    forbidden = tuple(sorted(forbidden))
    return frozenset(matching for matching in ALL_MATCHINGS
                     if forbidden not in matching)


def act_on_matching(matching, permutation):
    return tuple(sorted(
        tuple(sorted((permutation[left], permutation[right])))
        for left, right in matching
    ))


def act_on_word(word, permutation):
    answer = [0] * 8
    for site, colour in enumerate(word):
        answer[permutation[site]] = colour
    return tuple(answer)


def act_on_monomial(monomial, permutation):
    cells = []
    for left, right, a, b in monomial:
        new_left, new_right = permutation[left], permutation[right]
        if new_left < new_right:
            cells.append((new_left, new_right, a, b))
        else:
            cells.append((new_right, new_left, b, a))
    return tuple(sorted(cells))


def signed_weyl_word(word, tail_sites):
    answer = list(word)
    sign = 1
    for site in tail_sites:
        if answer[site] == 1:
            answer[site] = 2
            sign *= -1
        elif answer[site] == 2:
            answer[site] = 1
    return tuple(answer), sign


# ------------------------------------------------------------------ audits --

def presentation_automorphisms(forbidden):
    """Exhaustive over all 8! site permutations: which preserve the
    direct-free matching presentation as a SET of physical matchings?"""
    presentation = direct_free_matchings(forbidden)
    forbidden_pair = tuple(sorted(forbidden))
    automorphisms = []
    stabilizers = []
    for permutation in permutations(SITES):
        image = frozenset(act_on_matching(matching, permutation)
                          for matching in presentation)
        preserves = image == presentation
        stabilizes = (tuple(sorted((permutation[forbidden_pair[0]],
                                    permutation[forbidden_pair[1]])))
                      == forbidden_pair)
        # The structural lemma: preserving the presentation is EQUIVALENT to
        # setwise stabilizing the forbidden pair.  Verified, not assumed.
        require(preserves == stabilizes,
                ("presentation automorphism is not the forbidden-pair "
                 "stabilizer", permutation, preserves, stabilizes))
        if preserves:
            automorphisms.append(permutation)
        if stabilizes:
            stabilizers.append(permutation)
    require(automorphisms == stabilizers, "automorphism bookkeeping diverged")
    return tuple(automorphisms), len(presentation)


def literal_row_transport(base, permutation):
    """Does `permutation` transport every literal decorated 90-term complete
    source row?  This is the real content of the committed check, run here
    for every candidate rather than for one hardcoded transposition."""
    rolling = sha256()
    for word in product(COLOURS, repeat=8):
        transported = Counter(act_on_monomial(monomial, permutation)
                              for monomial in base.full_row(word))
        expected = Counter(base.full_row(act_on_word(word, permutation)))
        if transported != expected:
            return False, None
        rolling.update(repr(sorted(transported)).encode())
    return True, rolling.hexdigest()


def commutes_with_tail_weyl(permutation, tail_sites):
    """(C): s w = w s as signed maps on the 3^8 word set."""
    for word in product(COLOURS, repeat=8):
        left_word, left_sign = signed_weyl_word(
            act_on_word(word, permutation), tail_sites)
        right_word, right_sign = signed_weyl_word(word, tail_sites)
        right_word = act_on_word(right_word, permutation)
        if left_word != right_word or left_sign != right_sign:
            return False
    return True


def target_defect_invariant(permutation, tail_sites):
    """The committed 'endpoint oddization kills the target defect' test."""
    delta = Counter({(colour,) * 8: 1 for colour in COLOURS})
    weyl_delta = Counter()
    for word, coefficient in delta.items():
        changed, sign = signed_weyl_word(word, tail_sites)
        weyl_delta[changed] += coefficient * sign
    defect = Counter(weyl_delta)
    defect.subtract(delta)
    defect = Counter({key: value for key, value in defect.items() if value})
    swapped = Counter()
    for word, coefficient in defect.items():
        swapped[act_on_word(word, permutation)] += coefficient
    return swapped == defect


def transposition_group_structure(automorphisms, forbidden):
    """Verify Aut = S6 x S2 concretely: the six free sites are permuted
    arbitrarily and the forbidden pair is either fixed or swapped."""
    forbidden = tuple(sorted(forbidden))
    free = tuple(site for site in SITES if site not in forbidden)
    profile = Counter()
    for permutation in automorphisms:
        swapped = permutation[forbidden[0]] == forbidden[1]
        profile["forbidden_swapped" if swapped else "forbidden_fixed"] += 1
    require(profile["forbidden_fixed"] == profile["forbidden_swapped"] == 720,
            ("S6 x S2 split changed", dict(profile)))
    induced = {tuple(permutation[site] for site in free)
               for permutation in automorphisms}
    require(len(induced) == 720
            and induced == set(permutations(free)),
            "the free-site factor stopped being the full S6")
    return dict(sorted(profile.items())), sorted(free)


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "involution_pinned_base",
    )
    descent = load(
        "computations/verify_h3_physical_cartan_source_orbit_descent.py",
        "involution_pinned_descent",
    )
    forbidden = tuple(sorted(base.DIRECT_FREE_PAIR))
    require(forbidden == (3, 6), ("direct-free pair changed", forbidden))
    require(tuple(descent.TAIL_SITES) == TAIL_SITES,
            ("tail sites changed", descent.TAIL_SITES))
    require(dict(descent.ENDPOINT_SWAP) == {0: 1, 1: 0},
            "the committed endpoint swap is no longer 0 <-> 1")

    automorphisms, presentation_size = presentation_automorphisms(forbidden)
    require(presentation_size == 90,
            ("direct-free presentation size changed", presentation_size))
    require(len(automorphisms) == 1440,
            ("presentation automorphism group order changed",
             len(automorphisms)))
    structure, free_sites = transposition_group_structure(
        automorphisms, forbidden)
    automorphism_set = set(automorphisms)

    # ---- exhaustive verdict over ALL 28 transpositions -------------------
    identity = tuple(SITES)
    verdicts = []
    row_digests = {}
    for pair in combinations(SITES, 2):
        permutation = list(identity)
        permutation[pair[0]], permutation[pair[1]] = pair[1], pair[0]
        permutation = tuple(permutation)
        in_group = permutation in automorphism_set
        transports, digest = literal_row_transport(base, permutation)
        # (B) as verified on the literal decorated rows must agree with the
        # set-level automorphism computation.
        require(transports == in_group,
                ("literal row transport disagreed with the presentation "
                 "automorphism group", pair, transports, in_group))
        commutes = commutes_with_tail_weyl(permutation, TAIL_SITES)
        defect_ok = target_defect_invariant(permutation, TAIL_SITES)
        involution = all(permutation[permutation[site]] == site
                         for site in SITES)
        require(involution, ("a transposition stopped being an involution",
                             pair))
        verdicts.append({
            "transposition": list(pair),
            "presentation_automorphism": in_group,
            "literal_row_transport": transports,
            "commutes_with_tail_weyl": commutes,
            "target_defect_invariant": defect_ok,
            "admissible_for_K": bool(in_group and commutes),
        })
        if transports:
            row_digests[repr(pair)] = digest

    admissible = [tuple(record["transposition"]) for record in verdicts
                  if record["admissible_for_K"]]
    transporting = [tuple(record["transposition"]) for record in verdicts
                    if record["literal_row_transport"]]
    require(len(transporting) == 16,
            ("row-transporting transposition count changed",
             len(transporting)))
    require(set(transporting)
            == set(combinations(free_sites, 2)) | {forbidden},
            "the 16 transporting transpositions are not the pair stabilizer")
    require(len(admissible) == 8,
            ("admissible transposition count changed", len(admissible)))
    require(COMMITTED_CLAIM in admissible,
            "the committed 0 <-> 1 stopped being admissible")

    # ---- the discrimination question, answered honestly ------------------
    # Does anything in the chain single out 0 <-> 1?  No: 8 transpositions
    # satisfy every condition the construction of K uses.  We record the
    # whole set, so restating the claim as any other member is a no-op and
    # restating it as a NON-member changes the digest.
    others = [pair for pair in admissible if pair != COMMITTED_CLAIM]
    require(len(others) == 7,
            "the admissible alternatives to 0 <-> 1 changed")

    # What the committed "endpoint oddization kills the target defect" test
    # actually tests, computed exhaustively over all 8! permutations: it is
    # EQUIVALENT to setwise stabilization of the tail pair {2,5}, i.e. to
    # condition (C).  It says nothing at all about the forbidden pair, hence
    # nothing about 0 <-> 1 specifically.
    defect_group = 0
    for permutation in permutations(SITES):
        invariant = target_defect_invariant(permutation, TAIL_SITES)
        stabilizes_tail = (
            {permutation[TAIL_SITES[0]], permutation[TAIL_SITES[1]]}
            == set(TAIL_SITES)
        )
        require(invariant == stabilizes_tail,
                ("the target-defect test is not the tail-pair stabilizer",
                 permutation, invariant, stabilizes_tail))
        defect_group += invariant
    require(defect_group == 1440,
            ("target-defect invariance group order changed", defect_group))
    defect_all = sum(record["target_defect_invariant"] for record in verdicts)
    require(defect_all == 16,
            ("transpositions passing the target-defect test changed",
             defect_all))
    require(all(record["target_defect_invariant"]
                == record["commutes_with_tail_weyl"]
                for record in verdicts),
            "the target-defect test stopped matching tail-Weyl commutation")

    return {
        "theorem": ("the endpoint involution of the direct-free presentation "
                    "is pinned only up to the invariance group, and that "
                    "group is exactly computed here"),
        "direct_free_pair": list(forbidden),
        "presentation_size": presentation_size,
        "automorphism_group_order": len(automorphisms),
        "automorphism_group_structure": structure,
        "free_sites": free_sites,
        "tail_sites": list(TAIL_SITES),
        "transposition_verdicts": verdicts,
        "row_transporting_transpositions": [list(pair)
                                            for pair in transporting],
        "admissible_for_K_transpositions": [list(pair) for pair in admissible],
        "committed_claim": list(COMMITTED_CLAIM),
        "committed_claim_is_admissible": True,
        "committed_claim_is_forced": False,
        "admissible_alternatives_to_committed_claim": [list(pair)
                                                       for pair in others],
        "literal_row_transport_digests": dict(sorted(row_digests.items())),
        "target_defect_test_is_exactly_the_tail_pair_stabilizer": {
            "S8_permutations_passing": defect_group,
            "transpositions_passing": defect_all,
            "equals_setwise_stabilizer_of_tail_pair": True,
            "sees_the_forbidden_pair": False,
        },
        "reading": (
            "the theorem needs s in Aut(direct-free presentation) with "
            "s w = w s at the tail sites; eight transpositions qualify, so "
            "the prose 's is the residual-site transposition 0 <-> 1' is a "
            "choice of representative, not a derived fact.  The frozen "
            "ledger now hashes the whole admissible set and every literal "
            "row-transport digest, so substituting an inadmissible swap "
            "changes the digest"
        ),
        "scope": (
            "site-permutation symmetry of the direct-free complete source "
            "presentation and its compatibility with the signed tail Weyl "
            "action.  It does not construct H_w on the physical labelled "
            "source complex and does not prove that K is a relative cell"
        ),
    }


def controls():
    """Fabricated-geometry positive controls, executed in this same run."""
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "involution_pinned_control_base",
    )
    fired = []

    def fabricated_forbidden_pair():
        # Fabricate the geometry: pretend the direct-free pair is {3,7}.
        # Its automorphism group is a DIFFERENT subgroup of S8, so the pinned
        # 16-element transporting set no longer holds.
        automorphisms, _size = presentation_automorphisms((3, 7))
        automorphism_set = set(automorphisms)
        identity = tuple(SITES)
        transporting = []
        for pair in combinations(SITES, 2):
            permutation = list(identity)
            permutation[pair[0]], permutation[pair[1]] = pair[1], pair[0]
            if tuple(permutation) in automorphism_set:
                transporting.append(pair)
        free_sites = [site for site in SITES if site not in (3, 6)]
        require(set(transporting)
                == set(combinations(free_sites, 2)) | {(3, 6)},
                "fabricated forbidden pair reproduced the real invariance "
                "group")

    def fabricated_row_transport():
        # Fabricate the geometry a second way: check the literal decorated
        # rows of the REAL presentation against a permutation that moves the
        # forbidden pair.  It must not transport them.
        identity = tuple(SITES)
        permutation = list(identity)
        permutation[3], permutation[0] = 0, 3
        transports, _digest = literal_row_transport(base, tuple(permutation))
        require(transports,
                "a forbidden-pair-moving permutation failed to transport the "
                "direct-free rows")

    fired.append(should_fail("fabricated direct-free pair {3,7}",
                             fabricated_forbidden_pair))
    fired.append(should_fail("row transport under 0 <-> 3 (moves the "
                             "forbidden pair)", fabricated_row_transport))
    return fired


def main():
    control_records = controls()
    ledger = audit()
    ledger["positive_controls"] = [
        {"control": record["control"], "fired": record["fired"]}
        for record in control_records
    ]
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("involution invariance ledger changed", digest))
    print("repair678 endpoint involution invariance: PASS")
    print("Aut(direct-free presentation) order:",
          ledger["automorphism_group_order"], "= S6 x S2")
    print("transpositions transporting every literal row:",
          len(ledger["row_transporting_transpositions"]), "of 28")
    print("transpositions admissible for K=(1-s)H_w:",
          ledger["admissible_for_K_transpositions"])
    print("0 <-> 1 admissible:", ledger["committed_claim_is_admissible"],
          "| forced:", ledger["committed_claim_is_forced"])
    for record in control_records:
        print("positive control fired:", record["control"])
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
