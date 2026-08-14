#!/usr/bin/env python3
"""Audit the Gate-II product ``T * H_W`` in the relative switch DGA.

The presentation-safe chart graph retains

    T=t_B+t_C=(B-A)+(C-A)=-L01.

Multiplication by the target-safe signed-Weyl telescope is legal in that
extended DGA and fixes the earlier matching-constant problem.  In the total
PP/Cartan bicomplex its differential is not only the desired top term:

    D(T H_W)=(d_PP T) H_W + T (W-1).

The first term is mandatory.  The exact ``dT`` packet has eighteen residual-
edge and eighteen direction-factor faces.  The residual-edge part has the
known C2+/P2 topology.  The direction part consists of six faces in each of
the DQ, PS01, and PS10 Hasse[2] objects.  A Weyl/Cartan colour action changes
the word but preserves the direction-pair and repeated-edge label, so those
eighteen faces remain in the relative-C4 central idempotent.  The labelled
P2 square lies in the orthogonal PQ/SQ repeated-P3+K2 idempotent.

Thus ``T*H_W`` is a positive formal top decoration, but it does not totalize
the full product rule into the existing P2 square.  The first typed remainder
is the same-grade relative-C4 restriction/insertion face.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_chart_odd_carrier_gate_collapse.py":
        "67b86d1f9d8f22fa46e45582bea90435dfdebad86dcea47c76518a087bf200b9",
    "computations/verify_uniform_chart_cross_companion_relative_switch_dga_gate.py":
        "e0a8251128174d50b450b3bf85ce0a6870af00d4ab5565e7849fc3c8644c31c6",
    "computations/verify_h3_gate_ii_signed_weyl_telescope_matching_constant_gate.py":
        "092c90da62c9bd900939388a1ec7110de28f50c7b070d5029069ea3c3c9373a1",
    "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py":
        "59babf6e706973f2eaa8a8fdd7cdb624ddf88560c08243c5fcd05c3a5425a5d7",
    "computations/verify_h2_p2_relative_occurrence_graph_resolution_gate.py":
        "4dfb2846c698e5603dadeb1a73add17a7984ccedbad25e3bb09b6aa4170e62ce",
    "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py":
        "8ec18f05034b6483512644c49d0009b4b166b0d6b978f6895195321ca9d8417a",
    "computations/verify_h3_pure_trapped_h2_c2_c4_p2_descent_reduction.py":
        "026eb42fac96e2c21e6466f51322a18d45d975bcf5f48e0dc33f9cfa740d8d41",
    "computations/verify_uniform_chart_switch_word_target_affine_gate.py":
        "c0f0eb10c26816d7ad7033fc22f8d8ff8fe45a9825ef9e158dfe8d739db409a4",
}
EXPECTED_LEDGER_SHA256 = (
    "d9cb04b3aa0bba20b225776edf73f8142b0f88286e00b1c79f962ed774bce58a"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*chains: Counter[str]) -> Counter[str]:
    answer: Counter[str] = Counter()
    for chain in chains:
        answer.update(chain)
    return Counter({label: value for label, value in answer.items() if value})


def scale(value: int, chain: Counter[str]) -> Counter[str]:
    return Counter({label: value * coefficient
                    for label, coefficient in chain.items()
                    if value * coefficient})


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank width")
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


def presentation_safe_product_audit() -> dict[str, object]:
    collapse = load(
        "computations/verify_uniform_chart_odd_carrier_gate_collapse.py",
        "switch_weyl_chart_collapse",
    )
    h3 = collapse.h3_gate_ii_graph()
    require(h3 == {
        "extended_coordinates": 8,
        "graph_rank": 5,
        "h0_dimension": 3,
        "carrier_quotient_rank": 1,
    }, ("the presentation-safe Gate-II switch graph changed", h3))

    switch = load(
        "computations/verify_uniform_chart_cross_companion_relative_switch_dga_gate.py",
        "switch_weyl_relative_dga",
    )
    switch_ledger, switch_digest = switch.audit()
    relative = switch_ledger["relative_switch_DGA"]
    require(switch_digest == switch.EXPECTED_LEDGER_SHA256
            and relative["d_squared"] == 0
            and "monic" in relative["presentation_safe"]
            and switch_ledger["PP_functoriality"]["commutator_with_d"] == 0,
            "the relative switch DGA changed")

    # Tensor-product totalization.  Put K=W-1.  The first differential is
    # D(TH)=dT*H+T*K.  Since dT is odd, D(dT*H)=-dT*K, while
    # D(T*K)=+dT*K.  Omitting the first summand would break D^2=0.
    first = Counter({"dT*H_W": 1, "T*(W-1)": 1})
    second_from_dt_h = Counter({"dT*(W-1)": -1})
    second_from_t_k = Counter({"dT*(W-1)": 1})
    require(not add(second_from_dt_h, second_from_t_k)
            and add(scale(-1, Counter({"T*(W-1)": 1})), first)
                == Counter({"dT*H_W": 1}),
            "the PP/Cartan Leibniz totalization changed")
    return {
        "relative_switch_graph": {
            "extended_coordinates": h3["extended_coordinates"],
            "graph_rank": h3["graph_rank"],
            "H0_dimension": h3["h0_dimension"],
            "T": "t_B+t_C=-L01 modulo the graph boundary",
            "T_is_retained_not_set_to_zero": True,
        },
        "candidate": "T*H_W",
        "total_differential": "D(T*H_W)=(d_PP T)*H_W+T*(W-1)",
        "first_boundary_terms": dict(first),
        "D_squared": 0,
        "dt_term_optional": False,
        "formal_product_in_extended_DGA": True,
        "absolute_boundary_for_T": False,
    }


def signed_weyl_scope_audit() -> dict[str, object]:
    telescope = load(
        "computations/verify_h3_gate_ii_signed_weyl_telescope_matching_constant_gate.py",
        "switch_weyl_telescope",
    )
    ledger, digest = telescope.audit()
    target = ledger["target_telescope"]
    provenance = ledger["physical_provenance"]
    require(digest == telescope.EXPECTED_LEDGER_SHA256
            and target["target_safe"]
            and target["all_pair_product_fixes_global_Delta"]
            and "H2 direction-pair tag" in provenance["colour_action_preserves"]
            and not provenance["connected_SL3_or_Weyl_changes_B_label"],
            "the signed-Weyl scope changed")
    return {
        "target_safe": target["target_safe"],
        "all_pair_product_fixes_global_Delta":
            target["all_pair_product_fixes_global_Delta"],
        "top_product_effect": (
            "multiplication by retained T supplies the missing matching-"
            "centered factor to the chi_w/W-1 telescope boundary"
        ),
        "Weyl_preserves": provenance["colour_action_preserves"],
        "Weyl_changes_word_colours": True,
        "Weyl_changes_H2_direction_pair_or_repeated_tag": False,
    }


def full_dt_face_inventory() -> dict[str, object]:
    curvature = load(
        "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py",
        "switch_weyl_curvature",
    )
    matchings, directions, tails, l01, _r01, _ah = curvature.polynomial_data()
    d_l01 = curvature.differential(l01)
    selected_sites = {0, 1, 6, 7}
    tail_half = {
        label: -coefficient for label, coefficient in d_l01.items()
        if set(label[1]).isdisjoint(selected_sites)
    }
    direction_half = {
        label: -coefficient for label, coefficient in d_l01.items()
        if set(label[1]).issubset(selected_sites)
    }
    require(len(matchings) == 105
            and len(tail_half) == len(direction_half) == 18
            and set(tail_half).isdisjoint(direction_half),
            "the dT=-dL01 18+18 split changed")

    chart_names = ("DQ", "PS01", "PS10")
    chart_coefficients = (Q(-2), Q(1), Q(1))
    tail_topologies = ("C2plus", "P2", "P2")
    records = []
    direction_union = set()
    tail_union = set()
    for name, chart, coefficient, tail_topology in zip(
            chart_names, directions, chart_coefficients, tail_topologies,
            strict=True):
        chart_matchings = {tuple(sorted(chart + tail)) for tail in tails}
        tail_labels = {label for label in tail_half
                       if label[0] in chart_matchings}
        direction_labels = {label for label in direction_half
                            if label[0] in chart_matchings}
        require(len(tail_labels) == len(direction_labels) == 6
                and all(tail_half[label] == coefficient
                        for label in tail_labels)
                and all(direction_half[label] == coefficient
                        for label in direction_labels),
                ("the chartwise dT face census changed", name))
        tail_union.update(tail_labels)
        direction_union.update(direction_labels)
        records.append({
            "source_Hasse2_direction_pair": name,
            "coefficient_in_dT": str(coefficient),
            "tail_derivative_faces": len(tail_labels),
            "tail_face_topology": tail_topology,
            "direction_factor_faces": len(direction_labels),
            "direction_face_topology": "C4",
        })
    require(tail_union == set(tail_half)
            and direction_union == set(direction_half),
            "a dT face escaped the three chart packets")

    direction_marginals = {}
    for (_matching, edge), coefficient in direction_half.items():
        direction_marginals[edge] = (
            direction_marginals.get(edge, Q(0)) + coefficient
        )
    ordered_edges = ((6, 7), (0, 1), (0, 6), (1, 7), (1, 6), (0, 7))
    values = tuple(direction_marginals[edge] for edge in ordered_edges)
    require(values == tuple(map(Q, (-6, -6, 3, 3, 3, 3))),
            ("the dT direction marginals changed", values))
    return {
        "identity": "T=t_B+t_C=B+C-2A=-L01",
        "full_dT_support": len(tail_half) + len(direction_half),
        "residual_edge_half": {
            "support": len(tail_half),
            "topology_counts": {"C2plus": 6, "P2": 12},
            "status": (
                "formally reduces to the labelled P2 carrier orbit; its "
                "physical augmented landing remains open"
            ),
        },
        "direction_factor_half": {
            "support": len(direction_half),
            "topology_counts": {"C4": 18},
            "chart_supports": {"DQ": 6, "PS01": 6, "PS10": 6},
            "marginal_order": ["dD", "dq01", "dp0", "ds1", "dp1", "ds0"],
            "marginals": [str(value) for value in values],
            "primitive_profile": [-2, -2, 1, 1, 1, 1],
        },
        "chart_records": records,
    }


def idempotent_and_word_gate() -> dict[str, object]:
    # Central labelled idempotents in the physical Hasse category.  The
    # candidate direction faces occupy the first three objects.  The known
    # P2 square occupies the last two.  Colour Weyl actions are block
    # diagonal in this decomposition.
    labels = ("C4:DQ", "C4:PS01", "C4:PS10", "P2:PQ", "P2:SQ")
    identity = tuple(tuple(Q(row == column) for column in range(len(labels)))
                     for row in range(len(labels)))
    e_c4 = tuple(map(Q, (1, 1, 1, 0, 0)))
    e_p2 = tuple(map(Q, (0, 0, 0, 1, 1)))
    candidate = tuple(map(Q, (-2, 1, 1, 0, 0)))
    p2_sample = tuple(map(Q, (0, 0, 0, 1, -1)))

    def project(mask, vector):
        return tuple(a * b for a, b in zip(mask, vector, strict=True))

    require(all(sum(identity[row][middle] * identity[middle][column]
                    for middle in range(len(labels)))
                == identity[row][column]
                for row in range(len(labels)) for column in range(len(labels)))
            and project(e_c4, e_p2) == (Q(0),) * len(labels)
            and project(e_c4, candidate) == candidate
            and project(e_p2, candidate) == (Q(0),) * len(labels)
            and project(e_c4, p2_sample) == (Q(0),) * len(labels)
            and project(e_p2, p2_sample) == p2_sample,
            "the C4/P2 central idempotent split changed")

    p2 = load(
        "computations/verify_h2_p2_relative_occurrence_graph_resolution_gate.py",
        "switch_weyl_p2_graph",
    )
    p2_ledger, p2_digest = p2.audit()
    root = p2_ledger["root_PP_functoriality"]
    landing = p2_ledger["remaining_carrier_landing"]
    require(p2_digest == p2.EXPECTED_LEDGER_SHA256
            and root["labelled_cobar_square_generated"]
            and "augmented physical comparison" in landing["first_needed_map"],
            "the relative P2 square scope changed")

    lower = load(
        "computations/verify_h3_pure_trapped_h2_c2_c4_p2_descent_reduction.py",
        "switch_weyl_lower_types",
    )
    lower_ledger, lower_digest = lower.audit()
    residual = lower_ledger["C4"]["generic_flat_internal_residual"]
    require(lower_digest == lower.EXPECTED_LEDGER_SHA256
            and "relative-C4" in residual["missing_cell"]
            and "operation type and repeated-edge grade differ"
                in residual["why_not_P2_by_relabeling"],
            "the C4/P2 type separation changed")

    word_gate = load(
        "computations/verify_uniform_chart_switch_word_target_affine_gate.py",
        "switch_weyl_word_gate",
    )
    word_ledger, word_digest = word_gate.audit()
    grade = word_ledger["decisive_mixed_Hasse_grade_audit"]
    examples = grade["literal_counterguards"]
    require(word_digest == word_gate.EXPECTED_LEDGER_SHA256
            and grade["first_precise_mismatch"].startswith(
                "Hasse order/direction-pair component")
            and examples["DQ_response_C4"]["mixed_output_word"] == "001122"
            and examples["PS_response_C4"]["mixed_output_word"] == "001122"
            and examples["PQ_response_P2"]["mixed_output_word"] == "001122"
            and examples["SQ_response_P2"]["mixed_output_word"] == "001122"
            and examples["DQ_response_C4"]["second_Hasse_value"] == "1"
            and examples["PQ_response_P2"]["second_Hasse_value"] == "1",
            "the same-word Hasse idempotent counterguard changed")
    return {
        "central_label_basis": list(labels),
        "relative_C4_idempotent": list(map(int, e_c4)),
        "P2_idempotent": list(map(int, e_p2)),
        "orthogonal": True,
        "direction_candidate_chart_projection": list(map(int, candidate)),
        "projection_of_direction_candidate_to_P2": [0, 0, 0, 0, 0],
        "Weyl_action_block_diagonal_in_direction_pair_tag": True,
        "existing_P2_square": {
            "source_side_labelled_cobar_generated": True,
            "operation_tags": ["PQ", "SQ"],
            "physical_augmented_carrier_landing": False,
        },
        "same_word_counterguard": {
            "word": "001122",
            "nonzero_Hasse2_packets": ["DQ/C4", "PS/C4", "PQ/P2", "SQ/P2"],
            "direct_sum_separation": "direction-pair component of repeated grade",
            "word_head_fine_coincidence_identifies_packets": False,
        },
        "first_surviving_typed_face": residual["missing_cell"],
        "why_not_existing_P2": residual["why_not_P2_by_relabeling"],
    }


def p2_representative_scope() -> dict[str, object]:
    placement = load(
        "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py",
        "switch_weyl_p2_placement",
    )
    ledger, digest = placement.audit()
    face = ledger["one_endpoint_Hasse_faces"]
    dual = ledger["representative_dual"]
    require(digest == placement.EXPECTED_LEDGER_SHA256
            and face["representative_word"] == "0102"
            and face["surviving_wordwise_private_classes"] == 8
            and dual["value"] == "-13/6"
            and not dual["physical_terminal"],
            "the labelled P2 representative scope changed")
    return {
        "lower_word": ledger["physical_cut"]["lower_word"],
        "representative_word": face["representative_word"],
        "top_grade": ledger["physical_cut"]["top_grade"],
        "private_detector_value": dual["value"],
        "meaning": (
            "even in the P2 idempotent the existing square is a relative "
            "source graph whose physical augmented carrier landing is open; "
            "it cannot absorb an orthogonal C4 face"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 Gate-II switch-Weyl product-rule idempotent gate",
        "pins": PINS,
        "presentation_safe_product": presentation_safe_product_audit(),
        "signed_Weyl_scope": signed_weyl_scope_audit(),
        "full_dt_face_inventory": full_dt_face_inventory(),
        "first_typed_gate": idempotent_and_word_gate(),
        "existing_labelled_P2_scope": p2_representative_scope(),
        "verdict": (
            "The product T*H_W is a legitimate and useful cell in the "
            "presentation-safe relative switch DGA.  Its T*(W-1) boundary "
            "supplies the matching-centered root/Weyl decoration which the "
            "matching-constant telescope lacked.  It is not a totalization "
            "of Gate II by itself.  The mandatory Leibniz term (dT)*H_W has "
            "thirty-six PP faces.  The eighteen residual-edge faces have the "
            "known C2plus/P2 formal reduction.  The other eighteen are C4 "
            "direction-factor faces in the DQ/PS Hasse[2] idempotents.  Since "
            "H_W only recolours literal factors, it preserves these operation "
            "and repeated labels.  They have zero projection to the existing "
            "PQ/SQ labelled P2 square even when output word, head, and fine "
            "labels coincide.  The product therefore stops at the already "
            "isolated same-grade relative-C4 restriction/insertion face"
        ),
        "sharp_positive_part": (
            "T is now a source-provenant centered multiplier, so T*H_W "
            "removes the old matching-constant/circular-projector objection "
            "and constructs the formal target-safe top Weyl decoration"
        ),
        "first_precise_failure": (
            "the direction-pair/repeated central idempotent: C4 Hasse[2](DQ,PS) "
            "versus P2 Hasse[2](PQ,SQ).  The surviving face is one tail-"
            "covariant same-grade protected relative-C4 restriction/insertion "
            "primitive, with support 18 before its three chart components are folded"
        ),
        "accepted_terminal_now": False,
        "scope": (
            "exact h=3 switch graph, all-pair signed-Weyl telescope, 36-term "
            "first-PP product rule, labelled P2 relative square, and same-word "
            "Hasse-grade counterguard.  No physical P2 or relative-C4 carrier "
            "landing, q/W/ridge promotion, or accepted terminal is asserted"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("switch-Weyl product ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("Gate-II T*H_W product in retained switch DGA: FORMALLY VALID")
    print("top T*(W-1): MATCHING-CENTERED AND TARGET-SAFE")
    print("full dT product rule: 18 TAIL + 18 DIRECTION FACES")
    print("tail half: C2plus/P2 FORMAL ORBIT")
    print("direction half: C4 DQ/PS IDEMPOTENT, NOT P2")
    print("first remaining cell: SAME-GRADE RELATIVE-C4 PRIMITIVE")
    print("accepted terminal: " + str(ledger["accepted_terminal_now"]).upper())
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
