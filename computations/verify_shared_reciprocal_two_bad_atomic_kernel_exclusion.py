#!/usr/bin/env python3
"""Close the atomic pure-kernel-product subcase of the two-bad packet.

Work on five sites.  The common internal quadratic is assumed to contain
only same-colour endpoint cells.  The two kernel rows U,V are supported at
one site each, and the two known pure tensors have one-centre preimages.
If P*U*V*q has a nonzero all-third-colour coefficient, choose one of its
matching monomials.  After S5 normalization its sites are

    U:0, V:1, P:2, q_22:34.

The pure preimage centres must be two distinct sites in {2,3,4}.  Choose a
nonzero monochromatic matching term in each pure cofactor.  A mixed word in
a colour-diagonal four-site hafnian has at most one compatible matching:
the two equal-colour pairs must match to each other.  The checker exhausts
the 6 centre orders and 3x3 matching witnesses and finds such a forbidden
mixed term in one of K_0,K_1,K_ha,K_hc in all 54 cases.

This is a finite hand-reduction audit, not a search over supports or
coefficients.  Extra diagonal cells cannot repair the unique mixed term.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json


SITES = tuple(range(5))
Y, Z, X, L, M = SITES
A, C, T = range(3)
T_EDGE = (L, M)
EXPECTED_DIGEST = "194c56c58619b8f0973adc4ae2d92eef97011176a4a1b61546220be41100735b"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    require(len(vertices) == 4, "only four-site matchings are used")
    first = vertices[0]
    answer = []
    for second in vertices[1:]:
        rest = tuple(vertex for vertex in vertices
                     if vertex not in (first, second))
        answer.append(tuple(sorted((tuple(sorted((first, second))),
                                    tuple(sorted(rest))))))
    require(len(answer) == 3 and len(set(answer)) == 3,
            "four-site matching census changed")
    return tuple(answer)


def first_forbidden_mixed(ha, matching_a, hc, matching_c,
                          omitted=frozenset()):
    mandatory = (
        tuple((edge, A, "a") for edge in matching_a)
        + tuple((edge, C, "c") for edge in matching_c)
        + ((T_EDGE, T, "t"),)
    )
    cofactors = (
        (Y, "zero-y"),
        (Z, "zero-z"),
        (ha, "pure-a"),
        (hc, "pure-c"),
    )
    for hole, kind in cofactors:
        if kind in omitted:
            continue
        vertices = set(SITES) - {hole}
        for (edge, colour, label), (other, other_colour, other_label) \
                in combinations(mandatory, 2):
            if colour == other_colour:
                continue
            if not set(edge).isdisjoint(other):
                continue
            if not (set(edge) | set(other)) <= vertices:
                continue
            # In a colour-diagonal source the displayed mixed word has two
            # sites of each colour.  Its only compatible matching is the
            # pair of same-colour edges shown here, so no extra diagonal
            # support can supply a cancellation mate.
            return {
                "cofactor": kind,
                "hole": hole,
                "first": [label, list(edge)],
                "second": [other_label, list(other)],
            }
    return None


def first_forbidden_pure_bridge(ha, matching_a, hc, matching_c):
    """Find the same obstruction for a target-line two-centre kernel.

    If ``e_t@0-e_t@1`` is a nonzero two-centre syzygy, its Koszul normal
    form is ``K_0=e_t@1 tensor Z`` and ``K_1=e_t@0 tensor Z`` after
    rescaling.  Thus a mixed coefficient of K_0 whose colour at site 1 is
    not t, or of K_1 whose colour at site 0 is not t, is forbidden.
    """

    mandatory = (
        tuple((edge, A, "a") for edge in matching_a)
        + tuple((edge, C, "c") for edge in matching_c)
        + ((T_EDGE, T, "t"),)
    )
    cofactors = (
        (Y, "bridge-y", Z),
        (Z, "bridge-z", Y),
        (ha, "pure-a", None),
        (hc, "pure-c", None),
    )
    for hole, kind, forced_site in cofactors:
        vertices = set(SITES) - {hole}
        for (edge, colour, label), (other, other_colour, other_label) \
                in combinations(mandatory, 2):
            if colour == other_colour:
                continue
            if not set(edge).isdisjoint(other):
                continue
            if not (set(edge) | set(other)) <= vertices:
                continue
            if forced_site is not None:
                site_colours = {
                    **{site: colour for site in edge},
                    **{site: other_colour for site in other},
                }
                if site_colours[forced_site] == T:
                    continue
            return {
                "cofactor": kind,
                "hole": hole,
                "first": [label, list(edge)],
                "second": [other_label, list(other)],
            }
    return None


def audit():
    cases = []
    histogram = Counter()
    remaining = (X, L, M)
    for ha, hc in permutations(remaining, 2):
        for matching_a in perfect_matchings(
                tuple(site for site in SITES if site != ha)):
            for matching_c in perfect_matchings(
                    tuple(site for site in SITES if site != hc)):
                witness = first_forbidden_mixed(
                    ha, matching_a, hc, matching_c)
                require(witness is not None,
                        "atomic pure-kernel configuration survived")
                histogram[witness["cofactor"]] += 1
                cases.append({
                    "ha": ha,
                    "hc": hc,
                    "matching_a": [list(edge) for edge in matching_a],
                    "matching_c": [list(edge) for edge in matching_c],
                    "witness": witness,
                })

    require(len(cases) == 54, "normalized atomic case count changed")
    require(histogram == Counter({"zero-y": 30,
                                  "zero-z": 18,
                                  "pure-a": 6}),
            "first-witness histogram changed")

    # Both one-site kernel equations are load-bearing.  Omitting either
    # zero cofactor leaves four mandatory-witness configurations.  The pure
    # cofactor equations have redundant mixed-word coverage, so omitting one
    # of them does not provide the analogous mutation test.
    mutation = {}
    for omitted in ("zero-y", "zero-z"):
        survivors = 0
        for ha, hc in permutations(remaining, 2):
            for matching_a in perfect_matchings(
                    tuple(site for site in SITES if site != ha)):
                for matching_c in perfect_matchings(
                        tuple(site for site in SITES if site != hc)):
                    survivors += first_forbidden_mixed(
                        ha, matching_a, hc, matching_c,
                        frozenset((omitted,))) is None
        require(survivors == 4,
                f"mutation census changed after omitting {omitted}")
        mutation[omitted] = survivors

    bridge_cases = []
    bridge_histogram = Counter()
    for ha, hc in permutations(remaining, 2):
        for matching_a in perfect_matchings(
                tuple(site for site in SITES if site != ha)):
            for matching_c in perfect_matchings(
                    tuple(site for site in SITES if site != hc)):
                witness = first_forbidden_pure_bridge(
                    ha, matching_a, hc, matching_c)
                require(witness is not None,
                        "target-line two-centre bridge survived")
                bridge_histogram[witness["cofactor"]] += 1
                bridge_cases.append({
                    "ha": ha,
                    "hc": hc,
                    "matching_a": [list(edge) for edge in matching_a],
                    "matching_c": [list(edge) for edge in matching_c],
                    "witness": witness,
                })
    require(len(bridge_cases) == 54,
            "normalized target-line bridge case count changed")
    require(bridge_histogram == Counter({"bridge-y": 30,
                                         "bridge-z": 18,
                                         "pure-a": 6}),
            "target-line bridge first-witness histogram changed")

    ledger = {
        "normalization": {
            "kernel_sites": [Y, Z],
            "selected_P_site": X,
            "selected_tt_edge": list(T_EDGE),
            "pure_centres": list(remaining),
        },
        "cases": cases,
        "first_witness_histogram": dict(sorted(histogram.items())),
        "kernel_mutation_survivors": mutation,
        "target_line_two_centre_bridge": {
            "cases": bridge_cases,
            "first_witness_histogram": dict(sorted(
                bridge_histogram.items()
            )),
        },
        "verdict": (
            "no colour-diagonal packet with two one-centre distinct pure "
            "lifts and nonzero pure kernel-product coefficient when the "
            "kernel rows are one-site or include a target-line two-centre "
            "Koszul bridge"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"atomic-kernel ledger changed: {digest}")
    return digest


def main():
    digest = audit()
    print("shared reciprocal two-bad atomic kernel exclusion: PASS")
    print("54/54 normalized witness configurations have a unique mixed row")
    print("54/54 target-line two-centre bridge configurations also fail")
    print("survivor complexity: mixed internal cell, tilted/more-centre kernel, or multi-centre lift")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
