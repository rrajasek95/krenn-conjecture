#!/usr/bin/env python3
"""Exclude two minimal two-centre kernels in the diagonal bright chart.

The parity-straightening dependency makes each minimal two-centre kernel
bridge use the target axis.  Normalize a nonzero pure product monomial to

    selected U centre 0, selected V centre 1, P centre 2, q_34(t,t).

Enumerate the alternate U/V centres and the one-centre pure matching
witnesses.  Disjoint bridges leave too few pure centres.  For same/shared
bridges, a unique two-colour word contradicts a target bridge factor or a
pure cofactor in every configuration.  Extra diagonal cells cannot repair
such a 2+2 word.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITES = tuple(range(5))
U_SELECTED, V_SELECTED, P_SELECTED, LEFT, RIGHT = SITES
A, C, T = range(3)
T_EDGE = (LEFT, RIGHT)
PINNED_PARITY_SHA256 = (
    "ddf3c9b1dce264de5e29315d350e15bef56e91b699daf9c90439222b104c7f85"
)
EXPECTED_DIGEST = "08831d89bddee72c7d3d0c3a3f37d78cffdd54aad99c04153532babd02119cdb"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_parity_dependency():
    path = ROOT / (
        "computations/"
        "verify_shared_reciprocal_two_bad_two_centre_parity_straightening.py"
    )
    require(sha256(path.read_bytes()).hexdigest() == PINNED_PARITY_SHA256,
            "the two-centre parity-straightening dependency changed")


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


def first_unique_word(mandatory, constraints, omitted=frozenset()):
    for hole, kind, forced_target_site in constraints:
        if kind in omitted:
            continue
        for first, second in combinations(mandatory, 2):
            if first[1] == second[1]:
                continue
            if set(first[0]) & set(second[0]):
                continue
            if hole in first[0] or hole in second[0]:
                continue
            colours = {
                **{site: first[1] for site in first[0]},
                **{site: second[1] for site in second[0]},
            }
            if (forced_target_site is not None
                    and colours[forced_target_site] == T):
                continue
            return {
                "kind": kind,
                "hole": hole,
                "forced_target_site": forced_target_site,
                "first": [first[2], list(first[0])],
                "second": [second[2], list(second[0])],
            }
    return None


def enumerate_cases(omitted=frozenset()):
    cases = []
    survivors = []
    histogram = Counter()
    incidence = Counter()
    no_centre_pairs = []

    for extra_u in (V_SELECTED, P_SELECTED, LEFT, RIGHT):
        for extra_v in (U_SELECTED, P_SELECTED, LEFT, RIGHT):
            u_support = {U_SELECTED, extra_u}
            v_support = {V_SELECTED, extra_v}
            intersection = len(u_support & v_support)
            incidence[intersection] += 1
            union = u_support | v_support
            pure_centres = tuple(sorted(set(SITES) - union))
            if len(pure_centres) < 2:
                require(intersection == 0 and len(pure_centres) == 1,
                        "an unexpected bridge incidence lost pure centres")
                no_centre_pairs.append({
                    "extra_u": extra_u,
                    "extra_v": extra_v,
                    "u_support": sorted(u_support),
                    "v_support": sorted(v_support),
                })
                continue

            for pure_a, pure_c in permutations(pure_centres, 2):
                for matching_a in perfect_matchings(
                        tuple(site for site in SITES
                              if site != pure_a)):
                    for matching_c in perfect_matchings(
                            tuple(site for site in SITES
                                  if site != pure_c)):
                        mandatory = (
                            tuple((edge, A, "a") for edge in matching_a)
                            + tuple((edge, C, "c")
                                    for edge in matching_c)
                            + ((T_EDGE, T, "t"),)
                        )
                        constraints = (
                            (U_SELECTED, "U-left", extra_u),
                            (extra_u, "U-right", U_SELECTED),
                            (V_SELECTED, "V-left", extra_v),
                            (extra_v, "V-right", V_SELECTED),
                            (pure_a, "pure-a", None),
                            (pure_c, "pure-c", None),
                        )
                        witness = first_unique_word(
                            mandatory, constraints, omitted)
                        record = {
                            "extra_u": extra_u,
                            "extra_v": extra_v,
                            "intersection": intersection,
                            "pure_a": pure_a,
                            "pure_c": pure_c,
                            "matching_a": [list(edge)
                                           for edge in matching_a],
                            "matching_c": [list(edge)
                                           for edge in matching_c],
                        }
                        if witness is None:
                            survivors.append(record)
                        else:
                            record["witness"] = witness
                            cases.append(record)
                            histogram[witness["kind"]] += 1
    return cases, survivors, histogram, incidence, no_centre_pairs


def audit():
    pin_parity_dependency()
    cases, survivors, histogram, incidence, no_centre_pairs = (
        enumerate_cases()
    )
    require(incidence == Counter({1: 9, 0: 6, 2: 1}),
            "the two-bridge incidence census changed")
    require(len(no_centre_pairs) == 6,
            "the disjoint-bridge pure-centre obstruction changed")
    require(len(cases) == 216 and not survivors,
            "a same/shared two-bridge configuration survived")
    require(histogram == Counter({
        "U-left": 104,
        "U-right": 56,
        "V-left": 24,
        "V-right": 6,
        "pure-a": 26,
    }), "the two-bridge first-witness histogram changed")
    require(sum(case["intersection"] == 2 for case in cases) == 54,
            "the same-pair case count changed")
    require(sum(case["intersection"] == 1 for case in cases) == 162,
            "the shared-one-centre case count changed")

    _bridge_cases, bridge_mutants, *_rest = enumerate_cases(frozenset((
        "U-left", "U-right", "V-left", "V-right",
    )))
    require(len(bridge_mutants) == 80,
            "the bridge-factor mutation census changed")
    _pure_cases, pure_mutants, *_rest = enumerate_cases(frozenset((
        "pure-a", "pure-c",
    )))
    require(len(pure_mutants) == 26,
            "the pure-cofactor mutation census changed")

    ledger = {
        "pinned_parity_sha256": PINNED_PARITY_SHA256,
        "normalization": {
            "selected_u": U_SELECTED,
            "selected_v": V_SELECTED,
            "selected_p": P_SELECTED,
            "selected_tt_edge": list(T_EDGE),
        },
        "bridge_pair_incidence": dict(sorted(incidence.items())),
        "disjoint_bridge_pairs": no_centre_pairs,
        "same_shared_cases": cases,
        "first_witness_histogram": dict(sorted(histogram.items())),
        "bridge_factor_omission_survivors": bridge_mutants,
        "pure_cofactor_omission_survivors": pure_mutants,
        "verdict": (
            "no colour-diagonal packet with two minimal two-centre kernel "
            "rows, two distinct one-centre pure lifts, and a nonzero pure "
            "kernel-product coefficient"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"the two-by-two kernel ledger changed: {digest}")
    return digest


def main():
    digest = audit()
    print("shared reciprocal two-bad two-by-two kernel exclusion: PASS")
    print("bridge incidences same/shared/disjoint: 1 / 9 / 6")
    print("same/shared matching cases closed: 54 + 162 = 216")
    print("disjoint bridge pairs have fewer than two pure centres: 6 / 6")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
