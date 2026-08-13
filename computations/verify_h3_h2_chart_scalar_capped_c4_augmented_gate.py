#!/usr/bin/env python3
"""Split the endpoint-chart scalar into a capped C4 and block projector.

For

    A = D*q01,  B = p0*s1,  C = p1*s0,
    H = q23*q45 + q24*q35 + q25*q34,

the first proper face of the honest endpoint-chart cylinder is

    L01 = (2*A-B-C)*H.

The local response block is R01=(A+B+C)*H, so coefficientwise

    L01 = 3*A*H - R01.

But R01 is only nine terms of the complete 105-term response R.  It is not
an independently available physical row.  Modulo R, capping the DQ block
leaves the disjoint 96-term complement R-R01.  Hence a positive construction
needs both a source-valid R01 block projector and the capped C4 section (or
one combined pointed chart cell).

The known missing lower section U_C4 has boundary H in the Hasse[2](D,q01)
object.  Reaching A*H requires a source-valid cap/reinsertion by D*q01.  Its
PP Leibniz boundary has the two independent proper faces

    (delta D)*q01*U_C4,    D*(delta q01)*U_C4.

No pinned theorem supplies that capped cell with physical q/W/ridge and
terminal typing.  The cap/Cartan dual extension applies only after this
same-grade placement; a coefficient covector cannot be terminalized early.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_h2_full_site_chart_swap_pointed_scalar_guard.py":
        "bc35781e0f57bbd1202711e2dc818417d76fa87c69e33d3d4b01540e06865557",
    "notes/h3-h2-full-site-chart-swap-pointed-scalar-guard.md":
        "77771f8eee2a4bbaeb5a9575961efb9c7728833e28bca86d33102806aeffa6c2",
    "computations/verify_h3_h2_c4_trivial_tag_euler_scalar_face_gate.py":
        "47378f8ce904021bb802e0e4fd59de1591f0cd7333e1fcbc645e62cf40deb499",
    "notes/h3-h2-c4-trivial-tag-euler-scalar-face-gate.md":
        "3d16b7a1b77030eaaa5ba3fc342b927a7ee750db2c4f8091868591acc261477f",
    "computations/verify_h3_generic_symmetric_c4_placement_terminal_gate.py":
        "ecb8725715747c3270fb069545309283d1890fbac6e66dfb6ed2f53b609e0030",
    "notes/h3-generic-symmetric-c4-placement-terminal-gate.md":
        "dcf0ef4adf500b4bee46ca301b12241e95ed1343a509a4fe4110d5dd3a906e92",
    "computations/verify_h3_generic_symmetric_c4_core_saturation_tor_gate.py":
        "7307cb245996376f9847ff4852a4fdcd0a774152b4011ed92822022f93af03e5",
    "notes/h3-generic-symmetric-c4-core-saturation-tor-gate.md":
        "d0ea7112c33c94de2063e754e70dde9a6671d5fcd5213d4f2f1b62c51aa102bd",
    "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py":
        "8a9bfe47c934658d1b10ad42f283d6a017c27125bcb98615882e4bacd975f1eb",
    "notes/h3-o2-augmented-terminal-cap-cartan-extension-gate.md":
        "e9c0cf3c76cbe4c8061574d2b977bf1189a1fa299ef17ae1d2e463c08a313429",
    "computations/verify_h3_universal_response_ks_augmented_readout_extension_gate.py":
        "4493274dfbda62cec0d6823272762fb01c3a798123a1da206559e91890ba9047",
    "notes/h3-universal-response-ks-augmented-readout-extension-gate.md":
        "f201fd4c4599a27173a824d7475ade679ef2de55e7c91bc3dd9cc917ac16ee37",
}
EXPECTED_LEDGER_SHA256 = (
    "02b3e0eed50047490ddaa9c2b24cda3e7b95118f63cb3802627ec5afe0e0805d"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(height):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def scale(coefficient: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * entry for entry in vector)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((tuple(sorted((first, second))),) + tail))


def coefficient_reduction_audit() -> dict[str, object]:
    # Work in all 105 perfect-matching occurrence coordinates, not in the
    # tempting nine-coordinate local truncation.  The selected four-set is
    # {0,1,P=6,S=7}; its complement is {2,3,4,5}.
    matchings = tuple(perfect_matchings(tuple(range(8))))
    require(len(matchings) == len(set(matchings)) == 105,
            "the K8 response stopped having 105 occurrences")
    position = {matching: index for index, matching in enumerate(matchings)}
    directions = (
        ((6, 7), (0, 1)),  # A=D*q01
        ((0, 6), (1, 7)),  # B=p0*s1
        ((1, 6), (0, 7)),  # C=p1*s0
    )
    tails = tuple(perfect_matchings((2, 3, 4, 5)))
    require(len(tails) == 3, tails)
    local = tuple(
        tuple(sorted(tuple(sorted(edge)) for edge in direction + tail))
        for direction in directions for tail in tails
    )
    require(len(local) == len(set(local)) == 9
            and all(matching in position for matching in local),
            "the selected response block changed")

    def vector(entries: dict[tuple[tuple[int, int], ...], int]):
        answer = [Q(0)] * len(matchings)
        for matching, value in entries.items():
            answer[position[matching]] = Q(value)
        return tuple(answer)

    response = (Q(1),) * len(matchings)
    response_01 = vector({matching: 1 for matching in local})
    response_rest = add(response, scale(Q(-1), response_01))
    dq_symmetric = vector({matching: 1 for matching in local[:3]})
    l01 = vector({matching: coefficient for coefficient, start in
                  ((2, 0), (-1, 3), (-1, 6))
                  for matching in local[start:start + 3]})
    require(l01 == add(scale(Q(3), dq_symmetric),
                       scale(Q(-1), response_01)),
            "L01=3*DQ-C4-local-response changed")
    require(sum(l01, Q(0)) == 0
            and sum(value * value for value in l01) == 18,
            "the centered scalar normalization changed")
    require(sum(value != 0 for value in response_01) == 9
            and sum(value != 0 for value in response_rest) == 96,
            "the local/complement response split changed")

    # The local identity is not a quotient identity modulo the *complete*
    # response.  R, L01 and AH have rank three.  The remaining class after
    # subtracting 3AH is -R01, equivalently Rrest modulo R.
    require(rank((response,)) == 1
            and rank((response, l01)) == 2
            and rank((response, dq_symmetric)) == 2
            and rank((response, l01, dq_symmetric)) == 3
            and add(l01, scale(Q(-3), dq_symmetric))
                == scale(Q(-1), response_01)
            and add(l01, scale(Q(-3), dq_symmetric), response)
                == response_rest,
            "the complete-response residual changed")

    # A literal covector proves AH cannot replace L01 modulo R: take +1 on
    # one B occurrence and -1 on one occurrence outside the selected block.
    dual = [Q(0)] * len(matchings)
    dual[position[local[3]]] = Q(1)
    outside = next(matching for matching in matchings if matching not in local)
    dual[position[outside]] = Q(-1)
    dual = tuple(dual)
    dot = lambda left, right: sum((a * b for a, b in
                                   zip(left, right, strict=True)), Q(0))
    require(dot(dual, response) == 0
            and dot(dual, dq_symmetric) == 0
            and dot(dual, l01) == -1,
            "the complete-response separating covector changed")

    # Hasse[2](D,q01) removes the D,q01 factors from precisely the first
    # three monomials, leaving the symmetric residual C4 tail.
    h2345 = (Q(1), Q(1), Q(1))
    restricted_dq = tuple(dq_symmetric[position[matching]]
                          for matching in local[:3])
    require(restricted_dq == h2345,
            "the DQ Hasse restriction stopped being H2345")
    return {
        "nine_occurrence_order": [
            "Dq01*q23q45", "Dq01*q24q35", "Dq01*q25q34",
            "p0s1*q23q45", "p0s1*q24q35", "p0s1*q25q34",
            "p1s0*q23q45", "p1s0*q24q35", "p1s0*q25q34",
        ],
        "literal_identity": "L01=3*(Dq01*H2345)-R01",
        "complete_response_occurrences": len(matchings),
        "selected_block_occurrences": sum(value != 0 for value in response_01),
        "complement_occurrences": sum(value != 0 for value in response_rest),
        "response_rank": rank((response,)),
        "rank_with_L01": rank((response, l01)),
        "rank_with_DQ_symmetric": rank((response, dq_symmetric)),
        "rank_with_both": rank((response, l01, dq_symmetric)),
        "local_identity": "L01=3*Dq01*H2345-R01",
        "complete_response_quotient": (
            "[L01]-3[Dq01*H2345]=[R-R01], a 96-term complement"
        ),
        "separating_dual": (
            "+1 on one local B occurrence, -1 on one outside occurrence; "
            "it kills R and Dq01*H but reads -1 on L01"
        ),
        "local_block_is_a_physical_row": False,
        "L01_augmentation": str(sum(l01, Q(0))),
        "L01_squared_norm": str(sum(value * value for value in l01)),
        "primitive_coefficient_dual": "L01/18",
        "Hasse2_D_q01_face": "H2345=q23q45+q24q35+q25q34",
    }


def capped_section_gate() -> dict[str, object]:
    # The scalar and Hasse outputs are different graded objects.  A formal
    # reinsertion iota sends H to Dq01*H, but a physical PP module map must
    # also carry the two Leibniz faces.  Keeping these as independent rows
    # is the smallest exact guard against treating multiplication as a chain
    # map for free.
    # Coordinates: lower H, top DqH, (delta D)qH, D(delta q)H.
    raw_u = (Q(1), Q(0), Q(0), Q(0))
    desired_cap = (Q(1), Q(1), Q(1), Q(1))
    formal_top_only = (Q(0), Q(1), Q(0), Q(0))
    require(rank((raw_u,)) == 1
            and rank((raw_u, formal_top_only)) == 2
            and rank((raw_u, desired_cap)) == 2,
            "the cap/reinsertion independence changed")
    return {
        "lower_missing_column": "U_C4[D,Q01;2345] with boundary H2345",
        "capped_missing_column": "Uhat_C4=(D*q01) cap U_C4",
        "PP_Leibniz_boundary": (
            "delta((D*q01)U)=D*q01*delta(U)"
            "+(delta D)*q01*U+D*(delta q01)*U"
        ),
        "raw_lower_section_supplies_top": False,
        "formal_coefficient_reinsertion_exists": True,
        "physical_reinsertion_chain_map_constructed": False,
        "first_two_unassigned_faces": [
            "(delta D)*q01*U_C4", "D*(delta q01)*U_C4",
        ],
        "same_grade_unit_case": (
            "4e2ff27 constructs the lower U_C4 only if the entire retained "
            "core, including direction/reinsertion data, has a same-grade unit"
        ),
        "general_case": (
            "the surviving invariant is the one Tor/colon line; no pinned "
            "source column supplies its capped reinsertion"
        ),
        "independent_block_projector": (
            "even a completed cap supplies only Dq01*H2345; equation "
            "L01=3Dq01H2345-R01 also needs a source-valid projector/cylinder "
            "for the nine-term block R01 inside the 105-term response"
        ),
    }


def augmented_scope_audit() -> dict[str, object]:
    terminal = load(
        "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py",
        "chart_scalar_terminal",
    )
    terminal_ledger, terminal_digest = terminal.audit()
    require(terminal_digest == terminal.EXPECTED_LEDGER_SHA256,
            "the cap/Cartan terminal theorem changed")
    fork = terminal_ledger["post_placement_dichotomy"]
    require(fork["third_branch"] is False,
            "the post-placement fork acquired a third branch")

    response_augmented = load(
        "computations/verify_h3_universal_response_ks_augmented_readout_extension_gate.py",
        "chart_scalar_response_augmented",
    )
    response_ledger, response_digest = response_augmented.audit()
    require(response_digest == response_augmented.EXPECTED_LEDGER_SHA256,
            "the response-KS augmented guard changed")
    ambiguity = response_ledger["augmented_extension_ambiguity"]
    premature = response_ledger["premature_q_promotion_counterguard"]
    require(ambiguity["dimension_of_extension_ambiguity"] == 5
            and not premature["generator_or_Fredholm_promotion_valid"],
            "the premature terminal guard changed")
    return {
        "coefficient_target_augmentation": 0,
        "coefficient_target_safety_determines_physical_rows": False,
        "unassigned_before_capped_placement": [
            "word/fine/repeated target object", "anchor/ainc and physical q",
            "W", "labelled shifted ridge", "eta", "sigma",
        ],
        "independent_response_KS_readout_ambiguity": (
            ambiguity["dimension_of_extension_ambiguity"]
        ),
        "eta_sigma_rule": (
            "unique contractions after a labelled physical ridge is placed; "
            "coefficient naturality does not place that ridge"
        ),
        "4373ae6_after_same_grade_placement": {
            "q_ainc_Eq": 0,
            "target_j": "-mu_j",
            "W_j": "-mu_j",
            "ores_j": "mu_j",
            "ridge": "-sum alpha_j mu_j",
            "alternative": fork["exact_alternative"],
            "third_branch": fork["third_branch"],
        },
        "premature_terminalization_valid": False,
        "reason": (
            "before Uhat_C4 is a column in a complete physical relative "
            "domain, a q defect or coefficient dual can be supported on a "
            "formal graph generator with no physical kernel/cokernel witness"
        ),
    }


def pinned_frontier_audit() -> dict[str, object]:
    chart = load(
        "computations/verify_h3_h2_full_site_chart_swap_pointed_scalar_guard.py",
        "chart_scalar_swap",
    )
    chart_ledger, chart_digest = chart.audit()
    require(chart_digest == chart.EXPECTED_LEDGER_SHA256,
            "the endpoint-chart scalar guard changed")
    scalar = load(
        "computations/verify_h3_h2_c4_trivial_tag_euler_scalar_face_gate.py",
        "chart_scalar_face",
    )
    scalar_ledger, scalar_digest = scalar.audit()
    require(scalar_digest == scalar.EXPECTED_LEDGER_SHA256,
            "the C4 scalar face changed")
    generic = load(
        "computations/verify_h3_generic_symmetric_c4_placement_terminal_gate.py",
        "chart_scalar_uc4",
    )
    generic_ledger, generic_digest = generic.audit()
    require(generic_digest == generic.EXPECTED_LEDGER_SHA256,
            "the generic C4 placement gate changed")
    status = generic_ledger["missing_column_and_terminal_extension"][
        "one_explicit_missing_source_column"
    ]
    require(status["status"] == "NOT CONSTRUCTED BY ANY PINNED CELL",
            "U_C4 unexpectedly became physical")
    return {
        "chart_guard": chart_digest,
        "scalar_face_guard": scalar_digest,
        "generic_C4_guard": generic_digest,
        "endpoint_swap_target_defect": 0,
        "first_chart_proper_face": "L01",
        "lower_U_C4_status": status["status"],
        "new_reduction": (
            "coefficientwise L01=3Dq01H2345-R01, but R01 is not the complete "
            "response row; capped C4 alone leaves its 96-term complement"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 endpoint-chart scalar capped-C4/block-projector augmented gate",
        "pins": PINS,
        "pinned_frontier": pinned_frontier_audit(),
        "coefficient_reduction": coefficient_reduction_audit(),
        "physical_capped_section": capped_section_gate(),
        "augmented_scope": augmented_scope_audit(),
        "verdict": (
            "The exact local identity is L01=3 Dq01 H2345-R01, but R01 is "
            "only nine of the 105 response occurrences.  Modulo the complete "
            "response, a capped U_C4 leaves the disjoint 96-term complement. "
            "Thus the physical construction needs both the Dq01 cap with its "
            "two PP faces and a source-valid nine-term block projector, or one "
            "combined pointed chart cell.  The response presentation still "
            "does not assign physical q, W, or the labelled ridge.  The "
            "4373ae6 fork is exact only after that complete same-grade "
            "augmented placement; it cannot terminalize the bare coefficient class."
        ),
        "shortest_positive_theorem": (
            "construct one combined pointed cell whose C4 part has lower "
            "boundary H2345 and top Dq01 H2345, whose delta-D and delta-q01 "
            "Leibniz faces are cancelled, and whose occurrence-projector part "
            "isolates R01 inside the complete response.  Require physical "
            "word/fine/repeated, anchor/q, W, labelled-ridge and eta/sigma "
            "rows.  The local identity then lands L01 and 4373ae6 gives "
            "filler or terminal."
        ),
        "scope": (
            "exact canonical h=3 coefficient quotient and exact conditional "
            "augmented duality.  This does not construct the capped C4 cell "
            "or call a formal response covector a physical terminal."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("L01 = 3*(Dq01*H2345) - local R01: EXACT")
    print("complete response residual: 96-term complement")
    print("capped U_C4 plus R01 block projector: STILL MISSING")
    print("first PP faces: (delta D)q01 U and D(delta q01)U")
    print("q/W/labelled ridge: NOT ASSIGNED BEFORE PHYSICAL CAP")
    print("after complete same-grade cap: FILLER OR TERMINAL")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
