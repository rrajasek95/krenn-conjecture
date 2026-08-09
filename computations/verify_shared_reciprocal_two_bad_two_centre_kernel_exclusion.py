#!/usr/bin/env python3
"""Exclude the minimal one-site/two-centre pure kernel product.

This is the first non-atomic colour-diagonal stratum after
``verify_shared_reciprocal_two_bad_atomic_kernel_exclusion.py``.  Normalize
a nonzero pure product term to U at 0, the selected V entry at 1, P at 2,
and the internal t,t edge 34.  U is a one-site kernel, while V has a
minimal two-centre relation between holes 1 and z in {2,3,4}.  The two
known pure tensors have one-centre lifts.

The pure-lift centres are assumed disjoint from the kernel support.  For
each of 54 matching-witness configurations, a unique mixed coefficient
contradicts either K_0=0, purity of K_ha/K_hc, or proportionality of the
two inserted cofactor columns in the V relation.  Extra colour-diagonal
cells cannot cancel a two-colour 2+2 word, whose compatible matching is
unique.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITES = tuple(range(5))
U_SITE, V_SITE, P_SITE, LEFT, RIGHT = SITES
A, C, T = range(3)
T_EDGE = (LEFT, RIGHT)
PINNED_ATOMIC_SHA256 = (
    "513c0fa4cee2d2660635f72f1b1bd46da06e8a0520982b2c652e75e650c2a730"
)
EXPECTED_DIGEST = "74cea1d6fe951a0cce3bd9f06cbfc2b68abefbef04eb8e33149e46731bcd7460"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_atomic_dependency():
    path = ROOT / (
        "computations/"
        "verify_shared_reciprocal_two_bad_atomic_kernel_exclusion.py"
    )
    require(sha256(path.read_bytes()).hexdigest() == PINNED_ATOMIC_SHA256,
            "the atomic kernel exclusion dependency changed")


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    require(len(vertices) == 4, "only four-site matchings are used")
    first = vertices[0]
    answer = []
    for second in vertices[1:]:
        rest = tuple(site for site in vertices
                     if site not in (first, second))
        answer.append(tuple(sorted((tuple(sorted((first, second))),
                                    tuple(sorted(rest))))))
    require(len(answer) == 3 and len(set(answer)) == 3,
            "the four-site matching census changed")
    return tuple(answer)


def disjoint_pairs(mandatory, hole):
    for first, second in combinations(mandatory, 2):
        if set(first[0]) & set(second[0]):
            continue
        if hole in first[0] or hole in second[0]:
            continue
        yield first, second


def zero_or_pure_witness(mandatory, hole, cofactor):
    for first, second in disjoint_pairs(mandatory, hole):
        if first[1] == second[1]:
            continue
        return {
            "kind": cofactor,
            "hole": hole,
            "first": [first[2], list(first[0])],
            "second": [second[2], list(second[0])],
        }
    return None


def relation_repair_witness(mandatory, second_hole,
                            pure_a_site, pure_c_site):
    """Force and contradict a repair of the selected target slice.

    The vector at the second V centre is arbitrary.  Fix the known nonzero
    target component at the selected first centre.  A unique 2+2 word in
    K_1 must be cancelled by the other inserted cofactor column.  Its
    restriction after deleting the second centre is again 2+2, so there is
    one required diagonal matching.  Its new target-colour edge creates a
    unique forbidden mixed coefficient in a pure cofactor.
    """

    for first, second in disjoint_pairs(mandatory, V_SITE):
        if first[1] == second[1]:
            continue
        colours = {V_SITE: T}
        for edge, colour, _label in (first, second):
            for site in edge:
                colours[site] = colour
        require(set(colours) == set(SITES),
                "the selected inserted-cofactor word lost a site")

        remaining = tuple(site for site in SITES
                          if site != second_hole)
        colour_classes = {}
        for site in remaining:
            colour_classes.setdefault(colours[site], []).append(site)
        if sorted(map(len, colour_classes.values())) != [2, 2]:
            continue
        required = tuple(
            (tuple(sorted(sites)), colour, "relation-repair")
            for colour, sites in sorted(colour_classes.items())
        )
        repaired = mandatory + required
        contradiction = (
            zero_or_pure_witness(repaired, U_SITE, "zero-u")
            or zero_or_pure_witness(
                repaired, pure_a_site, "pure-a")
            or zero_or_pure_witness(
                repaired, pure_c_site, "pure-c")
        )
        if contradiction is None:
            continue
        return {
            "kind": "two-centre-repair",
            "selected_word": [colours[site] for site in SITES],
            "selected_first": [first[2], list(first[0])],
            "selected_second": [second[2], list(second[0])],
            "required_matching": [
                [entry[2], list(entry[0])] for entry in required
            ],
            "repair_contradiction": contradiction,
        }
    return None


def first_witness(extra_v_site, pure_a_site, matching_a,
                  pure_c_site, matching_c, omit=frozenset()):
    mandatory = (
        tuple((edge, A, "a") for edge in matching_a)
        + tuple((edge, C, "c") for edge in matching_c)
        + ((T_EDGE, T, "t"),)
    )
    candidates = []
    if "zero-u" not in omit:
        candidates.append(zero_or_pure_witness(
            mandatory, U_SITE, "zero-u"))
    if "pure-a" not in omit:
        candidates.append(zero_or_pure_witness(
            mandatory, pure_a_site, "pure-a"))
    if "pure-c" not in omit:
        candidates.append(zero_or_pure_witness(
            mandatory, pure_c_site, "pure-c"))
    if "two-centre-relation" not in omit:
        candidates.append(relation_repair_witness(
            mandatory, extra_v_site, pure_a_site, pure_c_site))
    return next((candidate for candidate in candidates if candidate), None)


def normalized_cases(omit=frozenset(), disjoint_pure_centres=True):
    cases = []
    histogram = Counter()
    survivors = []
    # z=0 would put the second V centre on the zero cofactor K_0.  Then
    # minimality fails and the atomic dependency handles the nonzero
    # component.  A genuinely two-centre relation therefore has z=2,3,4.
    for extra_v_site in (P_SITE, LEFT, RIGHT):
        if disjoint_pure_centres:
            possible_pure_centres = tuple(
                site for site in SITES
                if site not in (U_SITE, V_SITE, extra_v_site)
            )
            require(len(possible_pure_centres) == 2,
                    "the disjoint centre complement changed")
        else:
            possible_pure_centres = tuple(
                site for site in SITES if site != U_SITE
            )
        for pure_a_site, pure_c_site in permutations(
                possible_pure_centres, 2):
            for matching_a in perfect_matchings(
                    tuple(site for site in SITES
                          if site != pure_a_site)):
                for matching_c in perfect_matchings(
                        tuple(site for site in SITES
                              if site != pure_c_site)):
                    witness = first_witness(
                        extra_v_site, pure_a_site, matching_a,
                        pure_c_site, matching_c, omit)
                    record = {
                        "extra_v_site": extra_v_site,
                        "pure_a_site": pure_a_site,
                        "pure_c_site": pure_c_site,
                        "matching_a": [list(edge) for edge in matching_a],
                        "matching_c": [list(edge) for edge in matching_c],
                    }
                    if witness is None:
                        survivors.append(record)
                    else:
                        record["witness"] = witness
                        histogram[witness["kind"]] += 1
                        cases.append(record)
    return cases, histogram, survivors


def audit():
    pin_atomic_dependency()
    cases, histogram, survivors = normalized_cases()
    require(len(cases) == 54 and not survivors,
            "a minimal two-centre kernel configuration survived")
    require(histogram == Counter({
        "zero-u": 30,
        "pure-a": 16,
        "pure-c": 4,
        "two-centre-repair": 4,
    }), "the first-witness histogram changed")

    # The proportional-column relation is genuinely new: four cases survive
    # the atomic zero/purity witnesses when that relation is omitted.
    _cases, _histogram, relation_mutants = normalized_cases(
        frozenset(("two-centre-relation",)))
    require(len(relation_mutants) == 4,
            "the relation mutation census changed")

    relaxed_cases, _relaxed_histogram, overlap_survivors = normalized_cases(
        disjoint_pure_centres=False)
    require(len(relaxed_cases) == 308 and len(overlap_survivors) == 16,
            "the pure-centre overlap boundary changed")

    ledger = {
        "pinned_atomic_sha256": PINNED_ATOMIC_SHA256,
        "normalization": {
            "one_site_kernel": U_SITE,
            "selected_two_centre_entry": V_SITE,
            "selected_P_site": P_SITE,
            "selected_tt_edge": list(T_EDGE),
            "extra_two_centre_sites": [P_SITE, LEFT, RIGHT],
        },
        "cases": cases,
        "first_witness_histogram": dict(sorted(histogram.items())),
        "relation_omission_survivors": relation_mutants,
        "relaxed_pure_centre_cases_closed": len(relaxed_cases),
        "pure_centre_overlap_survivors": overlap_survivors,
        "verdict": (
            "no colour-diagonal packet with one one-site and one minimal "
            "two-centre kernel row, disjoint one-centre pure lifts, and "
            "a nonzero pure kernel-product coefficient"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"the two-centre kernel ledger changed: {digest}")
    return digest


def main():
    digest = audit()
    print("shared reciprocal two-bad two-centre kernel exclusion: PASS")
    print("54/54 minimal two-centre configurations have an exact unique word")
    print("relation-only witnesses / relation-omission survivors: 4 / 4")
    print("relaxed pure-centre overlap boundary: 308 closed / 16 open")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
