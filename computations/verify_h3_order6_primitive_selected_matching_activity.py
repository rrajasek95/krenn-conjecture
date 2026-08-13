#!/usr/bin/env python3
"""Land almost every dark Cartan packet on a selected pure matching.

The corrected signed primitive A0^2 polynomial has two nonzero restrictions
to the 90 direct-free pure matching tori.  After fixing the candidate site u
as canonical site 0, these two tori represent exactly the selected bright
matchings for which u is not the P-neighbour.  Bright-colour conjugation
gives the same statement for the second selected matching.

Across the 151,200 formerly unresolved incidence packets, 150,930 contain a
target-full candidate site with this property in at least one colour.  The
270 residual packets have the exact double-coloop form: both bright
matchings share their S-neighbour n and P-neighbour p, and F={n,p}.  Their
remaining four-site tails are either identical or differ by one C4.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
P, S = 6, 7
INTERNAL = tuple(range(6))
PRIMITIVE_PAIR = ((0, 7, 1, 1), (2, 4, 1, 1))
PINS = {
    "computations/verify_h3_order6_primitive_face_literal_boundary.py":
        "d85722196cd05b14e835efc08d37a2fde4d083d46ac1d0a177267f499bd26663",
    "notes/h3-order6-primitive-face-literal-boundary.md":
        "ab8769933ba4930ffb12c3c7c971660d3b1453fcaf3592be2b041844aad839a6",
    "computations/verify_h3_physical_cartan_active_overlap_landing.py":
        "8161ab2f2b1c8de0db01a358d0ed4aad5b48779d04355ef0fc16a186b92c8cbd",
    "notes/h3-physical-cartan-active-overlap-landing.md":
        "8dea46f9b1d606ac4295afbee64865bc0967447be641de17246465361d7ab866",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
}
EXPECTED_LEDGER_SHA256 = (
    "9578425a3b572da1f2809f0ae353b8dc7d955b9ec52f01d916b78b7bba5e6e63"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def normalize_matching(matching):
    return tuple(sorted(tuple(sorted(edge)) for edge in matching))


def primitive_output():
    literal = load(
        "computations/verify_h3_order6_primitive_face_literal_boundary.py",
        "selected_activity_literal",
    )
    terms, pair_shadow, repair, _base, system = literal.exact_solution_context()
    require(pair_shadow[tuple(sorted(PRIMITIVE_PAIR))] == 1,
            "primitive symbolic coefficient changed")
    output = Counter()
    for weight, coefficient, directions in terms:
        remaining = list(directions)
        for selected in PRIMITIVE_PAIR:
            remaining.remove(selected)
        for tail, value in repair.derivatives(
                system["products"][0], tuple(remaining)).items():
            output[tuple(sorted(coefficient + tail))] += weight * value
    output = Counter({monomial: value for monomial, value in output.items()
                      if value})
    require(len(output) == 167
            and sum(abs(value) for value in output.values()) == Q(3272, 3),
            "corrected signed primitive output changed")
    return output, system


def evaluate_matching_torus(output, matching):
    selected = {(left, right, 1, 1)
                for left, right in normalize_matching(matching)}
    supported = [(monomial, coefficient)
                 for monomial, coefficient in output.items()
                 if all(cell in selected for cell in monomial)]
    # The fixed site profile determines at most one exponent vector on a
    # matching coordinate torus.
    require(len(supported) <= 1,
            ("pure matching torus acquired two exponent vectors", matching))
    return supported[0][1] if supported else Q(0)


def canonical_relabelling(matching, site):
    """Map a non-P-neighbour candidate to the active 02|13|47|56 torus."""
    matching = normalize_matching(matching)
    by_site = {}
    for left, right in matching:
        by_site[left] = right
        by_site[right] = left
    neighbour_s = by_site[S]
    neighbour_p = by_site[P]
    neighbour_site = by_site[site]
    require(site not in (neighbour_s, neighbour_p),
            "active relabelling received a selected endpoint neighbour")
    fixed = {
        S: 7,
        P: 6,
        neighbour_s: 4,
        neighbour_p: 5,
        site: 0,
        neighbour_site: 2,
    }
    remaining = tuple(value for value in INTERNAL if value not in fixed)
    require(len(remaining) == 2, "active relabelling complement changed")
    fixed[remaining[0]] = 1
    fixed[remaining[1]] = 3
    image = normalize_matching(
        (fixed[left], fixed[right]) for left, right in matching
    )
    require(image == ((0, 2), (1, 3), (4, 7), (5, 6)),
            ("selected matching missed the active canonical torus", image))
    return fixed, image


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    output, system = primitive_output()
    landing = load(
        "computations/verify_h3_physical_cartan_active_overlap_landing.py",
        "selected_activity_landing",
    )
    direct = tuple(sorted((P, S)))
    bright = tuple(
        normalize_matching(matching)
        for matching in landing.matchings(tuple(range(8)))
        if direct not in normalize_matching(matching)
    )
    values = {matching: evaluate_matching_torus(output, matching)
              for matching in bright}
    active = {matching: value for matching, value in values.items() if value}
    require(active == {
        ((0, 2), (1, 3), (4, 7), (5, 6)): Q(-4),
        ((0, 2), (1, 6), (3, 5), (4, 7)): Q(-2),
    }, ("primitive pure-matching activity tori changed", active))

    # Verify the relabelling theorem on every matching/candidate pair.
    candidate_matching_pairs = Counter()
    for matching in bright:
        neighbour_s = landing.neighbour(matching, S)
        neighbour_p = landing.neighbour(matching, P)
        for site in INTERNAL:
            if site == neighbour_s:
                continue
            if site == neighbour_p:
                candidate_matching_pairs["P_neighbour_dark"] += 1
            else:
                _mapping, image = canonical_relabelling(matching, site)
                require(values[image] == -4,
                        "canonical selected activity coefficient changed")
                candidate_matching_pairs["selected_matching_active"] += 1
    require(candidate_matching_pairs == {
        "selected_matching_active": 360,
        "P_neighbour_dark": 90,
    }, ("matching/candidate activity split changed", candidate_matching_pairs))

    packet_branches = Counter()
    residual_shapes = Counter()
    residual_examples = []
    for matching1 in bright:
        neighbour1 = landing.neighbour(matching1, S)
        p_neighbour1 = landing.neighbour(matching1, P)
        for matching2 in bright:
            neighbour2 = landing.neighbour(matching2, S)
            p_neighbour2 = landing.neighbour(matching2, P)
            for size in range(2, 7):
                for target_full_tuple in combinations(INTERNAL, size):
                    target_full = set(target_full_tuple)
                    selected_full = target_full & {neighbour1, neighbour2}
                    if neighbour1 != neighbour2 and selected_full:
                        packet_branches["upstream_selected_arm"] += 1
                        continue
                    candidates = target_full - {neighbour1, neighbour2}
                    require(candidates,
                            "rank-three residual lost every outside candidate")
                    visible = tuple(site for site in candidates if not (
                        landing.neighbour(matching1, site) == P
                        and landing.neighbour(matching2, site) == P
                    ))
                    if visible:
                        site = visible[0]
                        if landing.neighbour(matching1, site) != P:
                            canonical_relabelling(matching1, site)
                        else:
                            canonical_relabelling(matching2, site)
                        packet_branches["selected_pure_matching_activity"] += 1
                        continue

                    require(neighbour1 == neighbour2
                            and p_neighbour1 == p_neighbour2
                            and target_full == {neighbour1, p_neighbour1},
                            ("activity residual was not the double coloop",
                             matching1, matching2, target_full))
                    common_endpoints = {
                        tuple(sorted((S, neighbour1))),
                        tuple(sorted((P, p_neighbour1))),
                    }
                    tail1 = set(matching1) - common_endpoints
                    tail2 = set(matching2) - common_endpoints
                    require(len(tail1) == len(tail2) == 2,
                            "double-coloop tail inventory changed")
                    if tail1 == tail2:
                        shape = "same_two_edge_tail"
                    else:
                        require(len(tail1 ^ tail2) == 4,
                                "double-coloop tails stopped differing by C4")
                        shape = "one_C4_tail_switch"
                    residual_shapes[shape] += 1
                    packet_branches["double_coloop_residual"] += 1
                    if len(residual_examples) < 2:
                        residual_examples.append({
                            "matching1": [list(edge) for edge in matching1],
                            "matching2": [list(edge) for edge in matching2],
                            "target_full": sorted(target_full),
                            "shape": shape,
                        })

    require(packet_branches == {
        "upstream_selected_arm": 310500,
        "selected_pure_matching_activity": 150930,
        "double_coloop_residual": 270,
    }, ("complete selected-activity packet split changed", packet_branches))
    require(residual_shapes == {
        "same_two_edge_tail": 90,
        "one_C4_tail_switch": 180,
    }, ("double-coloop residual shapes changed", residual_shapes))

    return {
        "theorem": "selected pure-matching activity of the primitive Cartan face",
        "corrected_signed_primitive_support": len(output),
        "direct_free_matching_tori": len(bright),
        "active_canonical_tori": {
            repr(matching): str(value) for matching, value in active.items()
        },
        "matching_candidate_split": dict(sorted(candidate_matching_pairs.items())),
        "all_selected_packets": sum(packet_branches.values()),
        "packet_branches": dict(sorted(packet_branches.items())),
        "residual_shapes": dict(sorted(residual_shapes.items())),
        "residual_examples": residual_examples,
        "activity_reason": (
            "if a target-full candidate u is not the P-neighbour in one "
            "selected bright matching, physical site relabelling sends that "
            "matching to 02|13|47|56, where the corrected primitive A0^2 "
            "coefficient is -4.  Global bright-colour conjugation covers "
            "either selected colour"
        ),
        "residual": (
            "both bright matchings share their S and P neighbours and the "
            "target-full set is exactly those two sites.  The residual "
            "four-site tails are identical or one C4 apart"
        ),
        "scope": (
            "the complete selected-matching/target-full incidence packet "
            "after physical Cartan source descent.  The 270 double-coloop "
            "packets still require a crossed-row/unit/dependence theorem"
        ),
    }


def main():
    ledger = audit()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("selected primitive activity ledger changed", digest))
    print("h3 order-six selected pure-matching activity: PASS")
    print("packet branches:", ledger["packet_branches"])
    print("residual shapes:", ledger["residual_shapes"])
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
