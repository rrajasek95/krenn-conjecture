#!/usr/bin/env python3
"""Test whether the normalized GL3 all-D endpoint is the selected db01 face.

The closest face is deletion v=1, with residual sites 2,3,4,5.  After giving
the bar every coarse advantage (multiply by the selected endpoint factor and
forget its pure-output tag), its all-D endpoint has the same three uncoloured
K4 matching *shapes* as b01.  Literally it has mixed q colours 2112 and is a
horizontal degree-zero output endpoint.  The selected response polynomial
b01 has q:00 colours in head/word 11:110000, and db01 is its six-term
vertical first-PP face.  The monic graph companion is dz01-db01, not all-D.

Thus retaining a principal companion does not repair the normalized bar:
the retained object must be the literal graph/PP companion.  Identifying it
with all-D would itself be the missing source-labelled comparison.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_cross_word_cap_central_attachment_first_face_gate.py":
        "6f1dc2d4baece91046f8834418a7ce7b2fa84a9a3f1acc867cdf33353a807eea",
    "notes/h3-cross-word-cap-central-attachment-first-face-gate.md":
        "79a9cfda1261163fd0039e2fed9d8bbe84218c04b3ca78096f7db8f238c79022",
    "computations/verify_h3_gl3_normalized_bar_word_change_obstruction.py":
        "ed3c1baafd7d83819c1b6842857611b5b540c57ef95c8ca8a450de357312670a",
    "notes/h3-local-gl3-normalized-bar-word-change-obstruction.md":
        "a12f8685ecd98a1ad71a2e7829acbe00ba2db597559ad8e726d42105aed60d20",
    "computations/verify_h3_sitewise_gl3_covariance_face_tau_no_go.py":
        "bda92248adc08434896a99d5dfd241321e9be926ab7e8117daf55ee9df74c685",
    "notes/h3-sitewise-gl3-covariance-face-tau-no-go.md":
        "b7052c310034500d1e720484c958a11ce167056a68db12be9a9b6129f384cbfd",
    "computations/verify_h3_e14_selected_fibre_graph_keq_koszul_gate.py":
        "9d57cbcfaeebb8d7f67d6efea87a124b4a46ad1dc054d5fc0954ab0c2338b157",
    "notes/h3-e14-selected-fibre-graph-keq-koszul-gate.md":
        "98cae28b58267abcffc47b571e52581a354950ef684df5f28b58dca88c60c6e7",
}
EXPECTED_LEDGER_SHA256 = "7f8fd35050f39a56dad2b3562d0b06e1e1fa3bbb0d60e4b2cd66a62439c1679c"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank width")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry/value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left-value*right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a*b for a, b in zip(left, right, strict=True)), Q(0))


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


MATCHINGS = (((2, 3), (4, 5)),
             ((2, 4), (3, 5)),
             ((2, 5), (3, 4)))
MIXED = {2: 2, 3: 1, 4: 1, 5: 2}


def q_label(edge: tuple[int, int], colours: dict[int, int]) -> str:
    left, right = edge
    return f"q{left}{right}:{colours[left]}{colours[right]}"


def shape(term: tuple[str, ...]) -> tuple[str, ...]:
    """Forget source/output role and q colours; retain matching edges only."""
    answer = []
    for factor in term:
        if not factor.startswith("q"):
            continue
        answer.append(factor.split(":", 1)[0])
    return tuple(sorted(answer))


def literal_support_audit() -> dict[str, object]:
    pure = {site: 0 for site in MIXED}
    b01 = tuple(tuple(sorted(("p0", "s1") + tuple(
        q_label(edge, pure) for edge in matching)))
        for matching in MATCHINGS)
    all_d_with_best_multiplier = tuple(tuple(sorted(("p0", "s1") + tuple(
        q_label(edge, MIXED) for edge in matching)))
        for matching in MATCHINGS)

    db01 = []
    for term in b01:
        q_positions = [index for index, factor in enumerate(term)
                       if factor.startswith("q")]
        require(len(q_positions) == 2, "b01 stopped being quadratic in q")
        for position in q_positions:
            differentiated = list(term)
            differentiated[position] = "d" + differentiated[position]
            db01.append(tuple(differentiated))

    require(len(set(b01)) == 3
            and len(set(all_d_with_best_multiplier)) == 3
            and len(set(db01)) == 6,
            "the selected/all-D/PP support counts changed")
    require(set(b01).isdisjoint(all_d_with_best_multiplier),
            "the mixed all-D endpoint entered the pure selected fibre")
    require({shape(term) for term in b01}
            == {shape(term) for term in all_d_with_best_multiplier},
            "the coarse three-matching near-hit disappeared")
    require(all(any(":00" in factor for factor in term) for term in b01)
            and all(any(":" in factor and not factor.endswith(":00")
                        for factor in term)
                    for term in all_d_with_best_multiplier),
            "the fine-colour obstruction changed")
    require(all(any(factor.startswith("dq") for factor in term)
                for term in db01)
            and all(not any(factor.startswith("dq") for factor in term)
                    for term in all_d_with_best_multiplier),
            "the first-PP obstruction changed")
    return {
        "compatible_deletion_face": "v=1, residual sites 2,3,4,5",
        "selected_response_head_word": "11:110000",
        "selected_b01_terms": [list(term) for term in b01],
        "selected_b01_term_count": len(b01),
        "selected_db01_terms": [list(term) for term in db01],
        "selected_db01_term_count": len(db01),
        "all_D_face_tag": "2112",
        "all_D_terms_after_granting_p0s1_multiplier": [
            list(term) for term in all_d_with_best_multiplier
        ],
        "all_D_term_count": len(all_d_with_best_multiplier),
        "literal_support_intersection": 0,
        "coarse_uncoloured_matching_shapes_agree": True,
        "coarse_agreement_forgets": [
            "q fine colours", "pure-output Y00000 tag",
            "source-relation versus output-endpoint role", "first-PP d label",
        ],
        "repeated_edge_exponents": {
            "b01": "squarefree", "all_D": "squarefree", "db01": "squarefree"
        },
        "sharp_obstruction": (
            "repeated degree is compatible, but fine colour, module role, and "
            "vertical PP degree are not"
        ),
    }


def graph_and_bicomplex_audit() -> dict[str, object]:
    # Coordinates are (selected db01, private dz01, all-D output endpoint).
    graph_pp = (Q(-1), Q(1), Q(0))
    all_d = (Q(0), Q(0), Q(1))
    desired_db01 = (Q(1), Q(0), Q(0))
    separator = (Q(1), Q(1), Q(0))
    require(rank((graph_pp, all_d)) == 2
            and rank((graph_pp, all_d, desired_db01)) == 3,
            "the graph/all-D selected-face rank changed")
    require(dot(separator, graph_pp) == dot(separator, all_d) == 0
            and dot(separator, desired_db01) == 1,
            "the selected-face separator changed")

    # The fibre-preserving centered route has the same obstruction.  In
    # coordinates (db01, sum of the other 29 PP fibres, all-D), the existing
    # complete response face is dR=(1,1,0).  Replacing the missing centered
    # face by all-D does not split the selected derivative.
    complete_dR = (Q(1), Q(1), Q(0))
    selected_in_fibre_coordinates = (Q(1), Q(0), Q(0))
    fibre_separator = (Q(1), Q(-1), Q(0))
    centered_dc01 = (Q(29), Q(-1), Q(0))
    require(rank((complete_dR, all_d)) == 2
            and rank((complete_dR, all_d,
                      selected_in_fibre_coordinates)) == 3,
            "the centered/all-D selected-fibre rank changed")
    require(dot(fibre_separator, complete_dR) == 0
            and dot(fibre_separator, all_d) == 0
            and dot(fibre_separator, selected_in_fibre_coordinates) == 1,
            "the centered selected-fibre separator changed")
    require(rank((complete_dR, centered_dc01)) == 2,
            "the genuine centered PP face stopped splitting db01")

    # Horizontal normalized bar degree and vertical PP degree are independent.
    bidegrees = {
        "b01": (0, 0),
        "all_D_endpoint": (0, 0),
        "db01": (0, 1),
        "dz01_minus_db01": (0, 1),
        "bar_edge_on_b01": (1, 0),
        "bar_edge_on_db01": (1, 1),
    }
    require(bidegrees["all_D_endpoint"] != bidegrees["db01"]
            and bidegrees["bar_edge_on_db01"] == (1, 1),
            "horizontal/vertical degrees collapsed")
    return {
        "coordinate_order": ["db01", "dz01", "all-D output endpoint"],
        "literal_graph_PP_column": [-1, 1, 0],
        "retained_all_D_endpoint": [0, 0, 1],
        "desired_selected_db01": [1, 0, 0],
        "rank_before_then_after_db01": [2, 3],
        "primitive_dual": [1, 1, 0],
        "horizontal_vertical_bidegrees": {
            key: list(value) for key, value in bidegrees.items()
        },
        "normalized_bar_on_vertical_face": (
            "d_bar H(db01)=L(db01)-D(db01), not db01"
        ),
        "principal_companion_verdict": (
            "retaining all-D is legitimate but it is not dz01-db01; a map "
            "identifying them is exactly the missing selected source face"
        ),
        "centered_route": {
            "coordinate_order": ["db01", "sum other PP fibres", "all-D"],
            "complete_dR": [1, 1, 0],
            "all_D": [0, 0, 1],
            "desired_db01": [1, 0, 0],
            "rank_before_then_after_db01": [2, 3],
            "primitive_dual": [1, -1, 0],
            "genuine_missing_dc01": [29, -1, 0],
            "identity": "db01=(dR+dc01)/30",
        },
    }


def augmentation_and_later_grade_audit() -> dict[str, object]:
    return {
        "normalized_bar_augmentation": {
            "all_D_endpoint": 1, "all_L_endpoint": 1, "bar_edge": 0,
        },
        "PP_zero_section": {"db01": 0, "dz01": 0},
        "augmentations_are_maps_on_different_summands": True,
        "may_not_identify_augmentation_one_with_PP_one_form": True,
        "first_face_status": "FAILS before D4/cap transport",
        "D4_cap_grade": "01211222 / P3+K2",
        "D4_cap_invoked_in_membership_test": False,
        "conditional_later_statement": (
            "after a genuine selected db01/graph source cell is supplied, the "
            "already isolated D4/cap/Cartan attachment remains the next face"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 selected db01 versus normalized GL3 all-D companion gate",
        "pins": PINS,
        "literal_support": literal_support_audit(),
        "graph_and_bicomplex": graph_and_bicomplex_audit(),
        "augmentation_and_scope": augmentation_and_later_grade_audit(),
        "verdict": (
            "The all-D endpoint is a three-term mixed-colour, pure-output, "
            "horizontal degree-zero class.  It agrees with b01 only after a "
            "nonphysical collapse forgetting colours, output/source role and PP "
            "degree.  The retained principal face is dz01-db01, a six-term "
            "vertical PP object.  Therefore the normalized bar does not construct "
            "db01; identifying its all-D endpoint with the graph companion would "
            "postulate precisely the missing source-labelled comparison."
        ),
        "scope": (
            "canonical h=3 selected endpoint fibre at grade g; D4/cap transport "
            "is deliberately not used before this first-face test"
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
    print("all-D vs b01: COARSE 3-MATCHING NEAR-HIT ONLY")
    print("all-D vs db01/graph PP face: LITERAL NO")
    print("first obstruction: fine colour + module role + vertical PP degree")
    print("D4/cap grade: NOT INVOKED BEFORE FIRST FACE")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
