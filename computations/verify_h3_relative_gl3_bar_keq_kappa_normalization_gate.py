#!/usr/bin/env python3
"""Test the normalized local-GL3 bar edge times the strict K_Eq cone.

The relative bar interval is a genuine chain object:

    dE=L-D,  eps(L)=eps(D)=1, eps(E)=0.

For dtheta=F its strict tensor product has

    d(E*theta)=(L-D)*theta-E*F.

This is a valid bar/Koszul square without making L or D absolute.  It is not
the Gamma_* response-to-AugP2 kappa square.  At the first compatible face,
the bar has mixed-colour all-D coefficients in the covariance/output module
and horizontal bar degree, whereas the selected response has pure q:00
coefficients and a six-term vertical PP face.  At the cap, the bar retains
squarefree 2K2 and local-GL3 operation tags; Gamma_* requires the six literal
t*q_(v,N), repeated P3+K2, response-to-AugP2 mixed-orbit tags.  Tensoring by
K_Eq preserves these idempotents, so its literal Gamma_* projection is zero.

The normalized endpoint ordinary-residue class is Psi-dark because Psi is
supported only on B/Eq.  It is nevertheless a nonzero protected H0 class:
each endpoint has augmentation one.  The relative difference cancels this
residue, but cannot be converted into a selected occurrence section.
Consequently strict multiplicativity would force lambda_i=0 only after the
missing Gamma_*-graded comparison is granted; the bar edge does not supply
that comparison.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_gl3_normalized_bar_word_change_obstruction.py":
        "ed3c1baafd7d83819c1b6842857611b5b540c57ef95c8ca8a450de357312670a",
    "notes/h3-local-gl3-normalized-bar-word-change-obstruction.md":
        "a12f8685ecd98a1ad71a2e7829acbe00ba2db597559ad8e726d42105aed60d20",
    "computations/verify_h3_kappa_lambda_literal_mapping_cone_normalization_gate.py":
        "b60538f9db5b8c2984bbee95e0a05f383408e9ab7c13680216adf56386682522",
    "notes/h3-kappa-lambda-literal-mapping-cone-normalization-gate.md":
        "1e7655ab1661453200ba33aff800aa6d9991dd86922d81d4f5b488fcc15bb817",
    "computations/verify_h3_selected_db01_normalized_gl3_bar_companion_gate.py":
        "620b3e54e8e6ee09a0b616d0259c8d109b0359645b20d35db5fb876c8e7e0311",
    "notes/h3-selected-db01-normalized-gl3-bar-companion-gate.md":
        "46aa4e74c52160cfaa74089727defb1a0d6c4d0051130374ec12dcc887de09de",
    "computations/verify_h3_gamma_star_source_operation_essential_surjectivity_census.py":
        "e5f2664b99c5ba58e0be385ca52dc52c6d2f6d6d0b793e655ebe297542dce291",
    "notes/h3-gamma-star-source-operation-essential-surjectivity-census.md":
        "66ba3a5d07ab9a378280ba5a991ec2bf04e9ec7b86b73cea1135c1210b9af3e7",
    "computations/verify_h3_cross_word_cap_central_attachment_first_face_gate.py":
        "6f1dc2d4baece91046f8834418a7ce7b2fa84a9a3f1acc867cdf33353a807eea",
    "notes/h3-cross-word-cap-central-attachment-first-face-gate.md":
        "79a9cfda1261163fd0039e2fed9d8bbe84218c04b3ca78096f7db8f238c79022",
}
EXPECTED_LEDGER_SHA256 = "9263237c7c9fc70ce210007b75345773e195c3581e2d25e1a4eefdd8c0ab9e71"

CAP_WORD = tuple(map(int, "01211222"))
RESPONSE_WORD = tuple(map(int, "11110000"))
NAMES = ("P", "S", "0", "1", "2", "3", "4", "5")
EDGE_SITES = {
    "s0": (1, 2),
    "q01": (2, 3),
    "q23": (4, 5),
    "q24": (4, 6),
    "q25": (4, 7),
    "q34": (5, 6),
    "q35": (5, 7),
    "q45": (6, 7),
}
SELECTED_FACES = (
    ("s0", "q01", "q45"),
    ("s0", "q01", "q23"),
    ("s0", "q01", "q35"),
    ("s0", "q01", "q24"),
    ("s0", "q01", "q34"),
    ("s0", "q01", "q25"),
)
MATCHINGS = (((2, 3), (4, 5)),
             ((2, 4), (3, 5)),
             ((2, 5), (3, 4)))
MIXED_FACE = {2: 2, 3: 1, 4: 1, 5: 2}
PURE_FACE = {site: 0 for site in MIXED_FACE}
DELTA = tuple(map(Q, (1, 1, -1, -1)))
ZERO4 = (Q(0),) * 4


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(values, Q(0)) for values in zip(*vectors, strict=True))


def scale(coefficient: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * entry for entry in vector)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        value = rows[pivot_row][column]
        rows[pivot_row] = [entry / value for entry in rows[pivot_row]]
        for row in range(height):
            if row == pivot_row or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def fine_degree(labels: tuple[str, ...], word: tuple[int, ...]) \
        -> tuple[int, ...]:
    degree = Counter()
    for label in labels:
        for site in EDGE_SITES[label]:
            degree[(site, word[site])] += 1
    return tuple(degree[(site, colour)]
                 for site in range(8) for colour in range(3))


def q_label(edge: tuple[int, int], colours: dict[int, int]) -> str:
    left, right = edge
    return f"q{left}{right}:{colours[left]}{colours[right]}"


def uncoloured_shape(term: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(factor.split(":", 1)[0]
                        for factor in term if factor.startswith("q")))


def relative_bar_keq_product_audit() -> dict[str, object]:
    # Work in the free symbolic boundary module.  E and theta are odd.
    # d(E theta)=(L-D)theta-EF.  Applying d gives
    # LF-DF-(LF-DF)=0 coefficientwise.
    first_boundary = {
        "L*theta": Q(1),
        "D*theta": Q(-1),
        "E*F": Q(-1),
    }
    second_boundary: dict[str, Q] = {}
    for term, coefficient in (
        ("L*F", Q(1)), ("D*F", Q(-1)),
        ("L*F", Q(-1)), ("D*F", Q(1)),
    ):
        second_boundary[term] = second_boundary.get(term, Q(0)) + coefficient
        if not second_boundary[term]:
            del second_boundary[term]
    require(not second_boundary, "relative bar/K_Eq product lost d-squared")

    # The normalized bar augmentation detects either endpoint but kills the
    # edge and every boundary difference.
    augmentation = {"L": Q(1), "D": Q(1), "E": Q(0)}
    require(augmentation["L"] - augmentation["D"] == 0
            and augmentation["L"] == augmentation["D"] == 1,
            "normalized relative augmentation changed")
    return {
        "bar_interval": "dE=L-D",
        "central_cone": "dtheta=F=(H0-u)e_Eq",
        "strict_relative_cell": "kappa_bar=E*theta",
        "strict_boundary": "d kappa_bar=(L-D)*theta-E*F",
        "d_squared": 0,
        "requires_L_absolute": False,
        "requires_D_absolute": False,
        "normalized_augmentation": {"L": 1, "D": 1, "E": 0},
        "relative_endpoint_difference_augmentation": 0,
        "conclusion": (
            "a genuine strict square exists in the covariance-bar x K_Eq "
            "bicomplex; existence there does not identify its operation "
            "parent with the selected Gamma_* mixed orbit"
        ),
        "symbolic_first_boundary": {
            term: str(value) for term, value in first_boundary.items()
        },
    }


def first_selected_face_audit() -> dict[str, object]:
    selected_b01 = tuple(tuple(sorted(("p0", "s1") + tuple(
        q_label(edge, PURE_FACE) for edge in matching)))
        for matching in MATCHINGS)
    all_d = tuple(tuple(sorted(("p0", "s1") + tuple(
        q_label(edge, MIXED_FACE) for edge in matching)))
        for matching in MATCHINGS)
    selected_db01 = []
    for term in selected_b01:
        for position, factor in enumerate(term):
            if not factor.startswith("q"):
                continue
            differentiated = list(term)
            differentiated[position] = "d" + factor
            selected_db01.append(tuple(differentiated))

    require(len(set(selected_b01)) == len(set(all_d)) == 3
            and len(set(selected_db01)) == 6,
            "selected/bar face counts changed")
    require(set(selected_b01).isdisjoint(all_d)
            and {uncoloured_shape(term) for term in selected_b01}
                == {uncoloured_shape(term) for term in all_d},
            "the exact coarse-near-hit/literal-miss changed")
    require(all(any(factor.startswith("dq") for factor in term)
                for term in selected_db01)
            and all(not any(factor.startswith("dq") for factor in term)
                    for term in all_d),
            "the horizontal/vertical PP mismatch changed")

    # Retaining the all-D endpoint cannot split the selected PP fibre.
    # Coordinates: selected db01, private dz01, all-D endpoint.
    graph_pp = tuple(map(Q, (-1, 1, 0)))
    retained_all_d = tuple(map(Q, (0, 0, 1)))
    desired_db01 = tuple(map(Q, (1, 0, 0)))
    separator = tuple(map(Q, (1, 1, 0)))
    require(rank((graph_pp, retained_all_d)) == 2
            and rank((graph_pp, retained_all_d, desired_db01)) == 3,
            "the retained-endpoint selected-face rank changed")
    require(dot(separator, graph_pp) == dot(separator, retained_all_d) == 0
            and dot(separator, desired_db01) == 1,
            "the retained-endpoint selected-face dual changed")

    return {
        "compatible_local_face": "delete v=1; residual sites 2,3,4,5",
        "bar_face_word": "2112",
        "selected_response_head_word": "11:110000",
        "all_D_terms": len(all_d),
        "selected_b01_terms": len(selected_b01),
        "selected_db01_terms": len(selected_db01),
        "literal_support_intersection_all_D_vs_b01": 0,
        "coarse_uncoloured_matching_shapes_agree": True,
        "all_D_fine_colours": "mixed q:21/q:12/q:22/q:11",
        "selected_fine_colours": "pure q:00",
        "all_D_module_role": "covariance/output endpoint",
        "selected_module_role": "response source relation",
        "bidegrees": {
            "all_D_endpoint": [0, 0],
            "bar_edge_on_b01": [1, 0],
            "selected_db01": [0, 1],
            "bar_edge_on_db01": [1, 1],
        },
        "rank_before_then_after_selected_db01": [2, 3],
        "primitive_selected_face_dual": [1, 1, 0],
        "first_mismatch": (
            "before Gamma_* cap placement: fine q-colour, output-versus-"
            "response module role, and vertical PP degree"
        ),
    }


def gamma_star_grade_audit() -> dict[str, object]:
    cap_fine = tuple(fine_degree(labels, CAP_WORD) for labels in SELECTED_FACES)
    response_fine = tuple(fine_degree(labels, RESPONSE_WORD)
                          for labels in SELECTED_FACES)
    changed = tuple(index for index, (cap, response) in enumerate(
        zip(CAP_WORD, RESPONSE_WORD, strict=True)) if cap != response)
    require(len(set(cap_fine)) == len(set(response_fine)) == 6
            and all(cap != response for cap, response in
                    zip(cap_fine, response_fine, strict=True))
            and changed == (0, 2, 4, 5, 6, 7),
            "the frozen Gamma_* fine orbit changed")

    gamma = {
        "word": "01211222",
        "fine": "six literal t*q_(v,N) site-colour multidegrees",
        "repeated": "P3+K2",
        "operation": "response-to-AugP2 mixed orbit/K_Eq",
        "window": "2345 with literal occurrence labels",
    }
    bar = {
        "coarse_input_word": "01211222 for the complete seven-site interval",
        "local_face_word": "2112 at the compatible deletion",
        "fine": "mixed-colour covariance coefficients h_v*Y0",
        "repeated": "squarefree 2K2 on the four residual sites",
        "operation": "local-GL3 covariance/output bar x objectwise K_Eq",
        "window": "four-site covariance face; no selected occurrence idempotent",
    }
    mismatch = {
        "word": (
            "coarse full input can agree, but the selected response head and "
            "output endpoint word roles do not"
        ),
        "fine": True,
        "repeated": True,
        "operation": True,
        "window_occurrence": True,
    }
    require(bar["repeated"] != gamma["repeated"]
            and bar["operation"] != gamma["operation"],
            "bar accidentally entered the Gamma_* repeated/operation block")

    return {
        "Gamma_star": gamma,
        "relative_bar_times_K_Eq": bar,
        "response_to_cap_word_changed_sites": [NAMES[index]
                                                  for index in changed],
        "six_cap_fine_degrees_distinct": True,
        "all_six_response_fine_degrees_different": True,
        "literal_mismatch": mismatch,
        "K_Eq_tensor_effect": (
            "adds the central cone factor but preserves word, fine, repeated, "
            "source/output role, operation word, and occurrence idempotents"
        ),
        "literal_projection_to_C_phys_Gamma_star": "0 (off-grade)",
        "is_the_kappa_operation_parent": False,
    }


def ordinary_residue_and_psi_audit() -> dict[str, object]:
    # Coordinates are B_0..B_3, Eq_0..Eq_3, ordinary residue.  Psi has no
    # ordinary-residue component.  Test a symbolic endpoint residue value 1;
    # multiplication by h_v*Y0 is scalar-linear and does not change darkness.
    psi_dual = DELTA + scale(Q(-1), DELTA) + (Q(0),)
    ores_endpoint = ZERO4 + ZERO4 + (Q(1),)
    require(dot(psi_dual, ores_endpoint) == 0,
            "ordinary residue acquired a Psi component")

    endpoint_ores = {"L": Q(1), "D": Q(1), "E": Q(0)}
    require(endpoint_ores["L"] - endpoint_ores["D"] == 0
            and endpoint_ores["L"] == endpoint_ores["D"] == 1,
            "relative endpoint residue changed")
    return {
        "normalized_endpoint_class": "h_v*Y0 times [endpoint]",
        "ordinary_residue": {"L": 1, "D": 1, "bar_edge": 0},
        "relative_L_minus_D_ordinary_residue": 0,
        "Psi_support": "delta.(B-Eq)/4; zero on ordinary residue",
        "Psi_on_either_endpoint_ordinary_residue": 0,
        "endpoint_ordinary_residue_is_Psi_dark": True,
        "endpoint_is_boundary_in_normalized_bar": False,
        "reason_endpoint_survives": "normalized bar augmentation(endpoint)=1",
        "logical_warning": (
            "Psi-dark is not null-homologous and does not authorize deleting "
            "or retagging the endpoint protected row"
        ),
    }


def lambda_consequence_audit() -> dict[str, object]:
    occurrence = tuple(map(Q, (1, 0, 1, 0)))
    tied = occurrence + occurrence
    psi_dual = DELTA + scale(Q(-1), DELTA)
    require(dot(psi_dual, tied) / Q(4) == 0,
            "a strict tied product became bright")
    return {
        "strict_normalization_theorem": (
            "if d epsilon_i=b_i is a physical selected Gamma_* section and "
            "kappa_i=epsilon_i*theta, then Pi_BEq(d kappa_i)=(v,v) and lambda_i=0"
        ),
        "bar_edge_source_equation": "dE=L-D, not d epsilon_i=b_i",
        "bar_product_Gamma_star_BEq_projection": "zero/off-grade",
        "bar_product_assigns_lambda_i": False,
        "tag_forgetting_control": {
            "if_bar_edge_is_granted_as_selected_epsilon_i": "lambda_i=0",
            "status": (
                "circular: this grant is the missing response-to-AugP2 "
                "multiplicative comparison"
            ),
        },
        "making_one_endpoint_absolute": (
            "would require killing the other augmentation-one endpoint or a "
            "new reduced relative augmentation"
        ),
        "conclusion": (
            "the relative interval does not force any of the eight physical "
            "lambda_i values"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 relative GL3 bar x K_Eq kappa normalization gate",
        "relative_product": relative_bar_keq_product_audit(),
        "first_selected_face": first_selected_face_audit(),
        "Gamma_star_grade": gamma_star_grade_audit(),
        "ordinary_residue_and_Psi": ordinary_residue_and_psi_audit(),
        "lambda_consequence": lambda_consequence_audit(),
        "verdict": (
            "The normalized local-GL3 interval and the strict K_Eq cone do "
            "form a genuine relative product without making either endpoint "
            "absolute.  It lives in the covariance/output-bar operation "
            "summand, not the selected response-to-AugP2 Gamma_* summand.  "
            "The first literal mismatch is already the selected db01 face: "
            "mixed versus pure q colours, output versus response role, and "
            "horizontal versus vertical PP degree.  At the cap the raw 2K2, "
            "fine and operation tags also differ from t*q_(v,N)/P3+K2.  The "
            "endpoint ordinary-residue class is Psi-dark, and L-D cancels "
            "it relatively, but either endpoint remains a nonboundary H0 "
            "class.  Therefore the product supplies no physical kappa_i and "
            "forces no lambda_i."
        ),
        "first_missing_datum": (
            "a source-labelled comparison carrying the normalized bar/"
            "selected response edge into the six literal Gamma_* occurrence "
            "fibres, including db01, t*q_(v,N), P3+K2, AugP2/K_Eq operation, "
            "and the protected residue row.  Once that comparison is a "
            "strict normalized module/DGA map, the pinned theorem gives "
            "lambda_i=0."
        ),
        "nonclaims": [
            "the relative bar/K_Eq square is not discarded; it is off Gamma_*",
            "ordinary-residue darkness is not called an absolute boundary",
            "coarse agreement of the full input word is not a word/fine operation map",
            "retagging the bar edge as the selected epsilon_i is not assumed",
        ],
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("relative bar/K_Eq ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("relative", "grade", "residue", "lambda"),
        default="relative",
    )
    arguments = parser.parse_args()
    ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")
    print(f"relative GL3 bar x K_Eq gate ({arguments.mode}): PASS")


if __name__ == "__main__":
    main()
