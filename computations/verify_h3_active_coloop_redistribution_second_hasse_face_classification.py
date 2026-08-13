#!/usr/bin/env python3
"""Classify every literal second-Hasse face of the h=3 matching tensor.

For six residual sites the pure target has 15 q-perfect-matchings.  A fixed
response coefficient has the 15 direct d*q^3 occurrences and the 90 ordered
p*s*q^2 occurrences.  Enumerating unordered pairs of scalar directions
shows that every nonzero second Hasse term belongs to one of five smaller
literal packets:

  QQ target : one residual q edge;
  QQ response: d*q plus the two endpoint orientations;
  DQ or PS response: a three-matching four-site hafnian;
  PQ response: a three-term one-endpoint insertion;
  SQ response: its endpoint reverse.

All other pairs are occurrence-incompatible and have zero second face.
The classification preserves the pair tag, residual sites, matching tail,
word colours and endpoint heads; colours do not change the site census.

This does not prove that every surviving lower packet is already terminal.
The QQ-response packet is the lower C2+ interface, the four-site packets are
C4 cofactors, and the one-endpoint packets are P2.  Existing physical audits
leave their occurrence-local placement open.  Thus the first exact residual
after literal classification is a smaller, named h<=2 source cell, not an
abstract cokernel and not automatically an active-fan/four-good landing.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_pf_dark_kernel_support_lowering_hasse_coloop_gate.py":
        "5feb07c35c4e5ce304a305f0146441de7af5a9dc2d5466a794d315d99b626e48",
    "computations/verify_h3_active_fan_coloop_complete_row_pivot.py":
        "d62fd630abac6e4d25bd6ffb0c1a2070311ec1c5d3c7764f56793283f78aa94a",
    "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py":
        "8ec18f05034b6483512644c49d0009b4b166b0d6b978f6895195321ca9d8417a",
    "computations/verify_h2_b4_cplus_shared_interface_gate.py":
        "ee48f2d1446d938fc97cda4e0977472081ee9823d31dc91f3f4c46829f3d8400",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
}
EXPECTED_LEDGER_SHA256 = (
    "1d0b6c58c558f9df8fed57b608ecc0ec278772a0c4e0d3c7225c27c868528792"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def q(u, v):
    return ("q", min(u, v), max(u, v))


def p(u):
    return ("p", u)


def s(u):
    return ("s", u)


D = ("d",)
SITES = tuple(range(6))
Q_CELLS = tuple(q(u, v) for u in SITES for v in SITES if u < v)
P_CELLS = tuple(p(u) for u in SITES)
S_CELLS = tuple(s(u) for u in SITES)
VARIABLES = Q_CELLS + P_CELLS + S_CELLS + (D,)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append((q(first, second),) + tail)
    return tuple(answer)


def source_monomials():
    target = tuple(tuple(sorted(matching))
                   for matching in perfect_matchings(SITES))
    direct = tuple(tuple(sorted((D,) + matching))
                   for matching in perfect_matchings(SITES))
    endpoint = []
    for u in SITES:
        for v in SITES:
            if u == v:
                continue
            remaining = tuple(site for site in SITES if site not in (u, v))
            for matching in perfect_matchings(remaining):
                endpoint.append(tuple(sorted((p(u), s(v)) + matching)))
    response = direct + tuple(endpoint)
    require(len(target) == 15 and len(direct) == 15
            and len(endpoint) == 90 and len(response) == 105,
            (len(target), len(direct), len(endpoint), len(response)))
    return target, response


def pair_index(monomials):
    answer = defaultdict(list)
    for monomial in monomials:
        for pair in itertools.combinations(monomial, 2):
            complement = tuple(variable for variable in monomial
                               if variable not in pair)
            answer[frozenset(pair)].append(complement)
    return answer


def pair_shape(pair):
    kinds = tuple(sorted(variable[0] for variable in pair))
    if kinds == ("q", "q"):
        left, right = sorted(pair)
        left_sites = set(left[1:])
        right_sites = set(right[1:])
        return "QQ-disjoint" if left_sites.isdisjoint(right_sites) else "QQ-incident"
    if kinds == ("p", "s"):
        pv = next(variable for variable in pair if variable[0] == "p")
        sv = next(variable for variable in pair if variable[0] == "s")
        return "PS-distinct" if pv[1] != sv[1] else "PS-same-site"
    if kinds in (("p", "q"), ("q", "s")):
        endpoint = next(variable for variable in pair
                        if variable[0] in ("p", "s"))
        qcell = next(variable for variable in pair if variable[0] == "q")
        prefix = "PQ" if endpoint[0] == "p" else "SQ"
        return prefix + ("-disjoint" if endpoint[1] not in qcell[1:]
                         else "-incident")
    return "".join(k.upper() for k in kinds)


def canonical_complements(index, first, second):
    return tuple(index[frozenset((first, second))])


def exact_pair_census():
    target, response = source_monomials()
    target_index = pair_index(target)
    response_index = pair_index(response)

    all_pairs = tuple(frozenset(pair)
                      for pair in itertools.combinations(VARIABLES, 2))
    require(len(all_pairs) == 378, len(all_pairs))
    target_profiles = Counter()
    response_profiles = Counter()
    for pair in all_pairs:
        target_profiles[(pair_shape(pair), len(target_index[pair]))] += 1
        response_profiles[(pair_shape(pair), len(response_index[pair]))] += 1

    nonzero_response = Counter()
    zero_response = Counter()
    for pair in all_pairs:
        shape = pair_shape(pair)
        if response_index[pair]:
            nonzero_response[(shape, len(response_index[pair]))] += 1
        else:
            zero_response[shape] += 1
    expected_nonzero = {
        ("QQ-disjoint", 3): 45,
        ("DQ", 3): 15,
        ("PS-distinct", 3): 30,
        ("PQ-disjoint", 3): 60,
        ("SQ-disjoint", 3): 60,
    }
    require(dict(nonzero_response) == expected_nonzero,
            (nonzero_response, expected_nonzero))
    require(sum(zero_response.values()) == 168, zero_response)

    target_nonzero = {key: value for key, value in target_profiles.items()
                      if key[1]}
    require(target_nonzero == {("QQ-disjoint", 1): 45}, target_nonzero)

    # Double-count every Hasse-pair incidence in two ways.
    require(sum(len(monomial) * (len(monomial) - 1) // 2
                for monomial in target) == 45,
            "target pair double count")
    require(sum(len(monomial) * (len(monomial) - 1) // 2
                for monomial in response) == 630,
            "response pair double count")
    require(sum(count * support for (_shape, support), count
                in nonzero_response.items()) == 630,
            "response profile double count")

    examples = {
        "QQ_target": canonical_complements(target_index, q(0, 1), q(2, 3)),
        "QQ_response": canonical_complements(response_index, q(0, 1), q(2, 3)),
        "DQ_response": canonical_complements(response_index, D, q(0, 1)),
        "PS_response": canonical_complements(response_index, p(0), s(1)),
        "PQ_response": canonical_complements(response_index, p(0), q(1, 2)),
        "SQ_response": canonical_complements(response_index, s(0), q(1, 2)),
    }
    expected = {
        "QQ_target": ((("q", 4, 5),),),
        "QQ_response": (
            (("d",), ("q", 4, 5)),
            (("p", 4), ("s", 5)),
            (("p", 5), ("s", 4)),
        ),
        "DQ_response": (
            (("q", 2, 3), ("q", 4, 5)),
            (("q", 2, 4), ("q", 3, 5)),
            (("q", 2, 5), ("q", 3, 4)),
        ),
        "PS_response": (
            (("q", 2, 3), ("q", 4, 5)),
            (("q", 2, 4), ("q", 3, 5)),
            (("q", 2, 5), ("q", 3, 4)),
        ),
        "PQ_response": (
            (("q", 4, 5), ("s", 3)),
            (("q", 3, 5), ("s", 4)),
            (("q", 3, 4), ("s", 5)),
        ),
        "SQ_response": (
            (("p", 3), ("q", 4, 5)),
            (("p", 4), ("q", 3, 5)),
            (("p", 5), ("q", 3, 4)),
        ),
    }
    for name in expected:
        require(set(examples[name]) == set(expected[name]),
                (name, examples[name], expected[name]))

    return {
        "scalar_direction_variables": len(VARIABLES),
        "repeated_same_variable_second_pairs": {
            "count": len(VARIABLES),
            "value": 0,
            "reason": "every source occurrence is scalar-cell multiaffine",
        },
        "unordered_direction_pairs": len(all_pairs),
        "target_matching_occurrences": len(target),
        "response_occurrences": {
            "direct_d_q3": 15,
            "ordered_p_s_q2": 90,
            "total": len(response),
        },
        "target_nonzero_pair_profiles": {
            "QQ_disjoint_pairs_with_one_residual_q": 45,
        },
        "response_nonzero_pair_profiles": {
            "QQ_disjoint_pairs_with_three_term_C2plus_tail": 45,
            "D_Q_pairs_with_three_matching_C4_tail": 15,
            "P_S_distinct_pairs_with_three_matching_C4_tail": 30,
            "P_Q_disjoint_pairs_with_three_term_P2_tail": 60,
            "S_Q_disjoint_pairs_with_three_term_P2_tail": 60,
        },
        "response_occurrence_incompatible_pairs": sum(zero_response.values()),
        "literal_pair_incidences": {"target": 45, "response": 630},
        "canonical_complements": {
            name: [[str(variable) for variable in monomial]
                   for monomial in examples[name]]
            for name in examples
        },
    }


def physical_route_classification():
    return {
        "occurrence_incompatible": {
            "pairs": [
                "incident QQ", "same-row PP or SS", "same-site PS",
                "incident PQ or SQ", "DP", "DS",
                "a repeated scalar label (by multiaffinity)",
            ],
            "second_face": 0,
            "positive_use": (
                "if every pair in supp(xi) is of this kind, the complete "
                "matching tensor is affine on x+t*xi and f77c2ed gives the "
                "occupied anchor-safe support deletion"
            ),
        },
        "QQ_target": {
            "literal_tail": "one q cell on the two residual sites",
            "routes_if": (
                "that base cell is offdiagonal (target augmentation supplies "
                "a private-site fan, then four-good-or-coloop), or its "
                "physical hole is outside the trapped shore"
            ),
            "internal_pure_residual": "one-edge restricted coloop face",
        },
        "QQ_response": {
            "literal_tail": "d*q_uv + p_u*s_v + p_v*s_u",
            "named_packet": "two-site target-normal C2+ packet",
            "unconditional_terminal": False,
        },
        "DQ_or_PS_response": {
            "literal_tail": (
                "q_ab*q_cd + q_ac*q_bd + q_ad*q_bc on four residual sites"
            ),
            "named_packet": "four-site C4 hafnian/cofactor packet",
            "unconditional_terminal": False,
        },
        "PQ_or_SQ_response": {
            "literal_tail": (
                "s_a*q_bc+s_b*q_ac+s_c*q_ab, or the p-reverse"
            ),
            "named_packet": "one-endpoint P2 insertion packet",
            "unconditional_terminal": False,
        },
        "literal_routing_rule": (
            "choose a nonzero base-tail monomial in a nonzero second-face "
            "coefficient.  Any offdiagonal base q enters the target-augmented "
            "private-site fan and hence four-good-or-coloop alternative; an "
            "endpoint/hole outside the closed Hall shore enters finite "
            "saturation.  If all base factors are pure and trapped, the term "
            "remains in the named lower packet above"
        ),
        "typing": (
            "the direction pair plus its complement reconstructs one original "
            "matching occurrence, so output word, fine colours, endpoint heads, "
            "physical sites and common matching tail are retained literally"
        ),
    }


def lower_packet_counterguard():
    # Saturate the Hall shore to all 15 holes and use only pure q base cells.
    # Each atomic profile can be nonzero without an offdiagonal base q or an
    # outside hole.  These are literal coefficient points, not a full source.
    values = {
        "q23": 1, "q24": 0, "q25": 0,
        "q34": 0, "q35": 0, "q45": 1,
        "d": 1, "p3": 1, "p4": 0, "p5": 0,
        "s3": 1, "s4": 0, "s5": 0,
    }
    c4 = (values["q23"] * values["q45"]
          + values["q24"] * values["q35"]
          + values["q25"] * values["q34"])
    p2 = (values["s3"] * values["q45"]
          + values["s4"] * values["q35"]
          + values["s5"] * values["q34"])
    c2plus = values["d"] * values["q45"]
    require(c4 == p2 == c2plus == 1, (c4, p2, c2plus))
    return {
        "closed_Hall_shore": "all 15 residual holes",
        "base_q_colours": "pure diagonal only",
        "nonzero_atomic_faces": {
            "C2plus": c2plus,
            "C4_hafnian": c4,
            "P2_insertion": p2,
        },
        "offdiagonal_base_q": False,
        "outside_Hall_hole": False,
        "conclusion": (
            "literal second-face classification alone cannot force the "
            "active/four-good or outside-hole branches; a pure trapped lower "
            "packet survives"
        ),
        "existing_physical_status": (
            "the pinned h2 P2 audit leaves an occurrence-private one-endpoint "
            "section, and the pinned B4/C2+ audit leaves the common target-"
            "bearing even cell.  The coefficient shadows are exact but their "
            "source-labelled placements are not yet theorems"
        ),
        "scope": (
            "an exact full-matching-face quotient guard, not a complete GHZ "
            "source point"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": (
            "h3 active-coloop redistribution literal second-Hasse face "
            "classification"
        ),
        "pins": PINS,
        "exact_census": exact_pair_census(),
        "physical_route_classification": physical_route_classification(),
        "pure_trapped_lower_packet_guard": lower_packet_counterguard(),
        "verdict": (
            "Every literal second Hasse term of the full h=3 target/response "
            "matching tensor is classified without a cokernel projection.  "
            "Occurrence-incompatible pairs vanish and give the exact affine "
            "deletion criterion of f77c2ed.  Every compatible pair descends "
            "to one of QQ one-edge, C2+, C4, or P2 packets with exact word, "
            "head and matching-tail provenance.  Offdiagonal base tails and "
            "outside holes route as desired, but a pure trapped lower packet "
            "survives; current physical results do not fill its occurrence-"
            "local C2+/P2 placement.  Hence the proposed exhaustive terminal "
            "routing is conditional on those named lower cells, not proved "
            "by the second-face census alone."
        ),
        "shortest_remaining_theorem": (
            "construct a source-natural restriction map taking the pure "
            "trapped H2 packet to its C2+/C4/P2 lower cell in the same word/"
            "fine/protected grade, or show its first nonzero literal mate "
            "contains an offdiagonal private cofactor or an outside Hall hole"
        ),
        "scope": (
            "canonical h=3 six-residual-site matching tensor; exact support "
            "and source-label census, not an all-h terminal theorem"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("full matching second-Hasse pair incidences: target 45, response 630")
    print("occurrence-incompatible direction pairs: AFFINE-DELETION ARM")
    print("compatible faces: QQ / C2+ / C4 / P2 LOWER PACKETS")
    print("pure trapped lower packet: SURVIVES LITERAL ROUTE CENSUS")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
