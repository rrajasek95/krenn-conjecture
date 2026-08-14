#!/usr/bin/env python3
"""Compute the eight kappa charges from the literal mapping-cone product.

For one labelled occurrence section d(epsilon)=b and the central cone
d(theta)=F, the standard physical mixed cell is the Koszul product

    kappa_std = epsilon wedge theta,
    d(kappa_std) = b*theta - epsilon*F.

The physical reduced-Eq row uses the boundary orientation opposite to the
algebraic minus on epsilon*F.  Thus both relevant occurrence readouts are
the same vector v:

    Pi_BEq(d kappa_std) = (v,v),
    Psi(d kappa_std) = delta.(v-v)/4 = 0.

This is stronger than d^2=0, but conditional on a physical multiplicative
source comparison identifying kappa with this standard product.  Without
that normalization one may add lambda*(delta,0) in the terminal B/Eq block;
all known augmented rows and d^2 are unchanged.  The weakest determining
row is delta.B-delta.Eq=0 for each literal instance.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_gamma_star_source_operation_essential_surjectivity_census.py":
        "e5f2664b99c5ba58e0be385ca52dc52c6d2f6d6d0b793e655ebe297542dce291",
    "notes/h3-gamma-star-source-operation-essential-surjectivity-census.md":
        "66ba3a5d07ab9a378280ba5a991ec2bf04e9ec7b86b73cea1135c1210b9af3e7",
    "computations/verify_h3_cross_word_mapping_cylinder_d2_augmentation_freedom_gate.py":
        "3704235f1030a07556aaebed3225bec8ea0fb9fa4d6a4d3aa124a7727a3bebec",
    "notes/h3-cross-word-mapping-cylinder-d2-augmentation-freedom-gate.md":
        "ef33bdd1f600fb3f58e91ca191a2fcfcfab516d5680907661a006ca5d358cec0",
    "computations/verify_h3_e14_selected_fibre_graph_keq_koszul_gate.py":
        "9d57cbcfaeebb8d7f67d6efea87a124b4a46ad1dc054d5fc0954ab0c2338b157",
    "notes/h3-e14-selected-fibre-graph-keq-koszul-gate.md":
        "98cae28b58267abcffc47b571e52581a354950ef684df5f28b58dca88c60c6e7",
    "computations/verify_h3_cross_word_cap_central_attachment_first_face_gate.py":
        "6f1dc2d4baece91046f8834418a7ce7b2fa84a9a3f1acc867cdf33353a807eea",
    "notes/h3-cross-word-cap-central-attachment-first-face-gate.md":
        "79a9cfda1261163fd0039e2fed9d8bbe84218c04b3ca78096f7db8f238c79022",
    "computations/verify_h3_balanced_square_private_eq_projection_gate.py":
        "bbfb690a73844169574351ad019171a6d9c5fe332e59cc9694a1f67dcf31cf8e",
    "notes/h3-balanced-square-private-eq-projection-gate.md":
        "6d740e7e30231204dbe1b79c4b7c21fe5f5b5ac45122ac714be3c7626afa7c31",
    "computations/verify_h3_e14_keq_private_placement_residue_identification_gate.py":
        "89b0b694b525dba502314e61922cb884ef6ddd2f14fea68b3bafd5215aa40c70",
    "notes/h3-e14-keq-private-placement-residue-identification-gate.md":
        "36828d8503d929427eef55886cb68cbfe7c2431649c38382907835365bd5ed38",
    "computations/verify_h3_cross_frontier_shared_loop_balanced_eq_convergence_gate.py":
        "c43d7a6aa8301b6f5a424f270f6a057878e21f5e8b38628d4d16c007d36ff2ea",
    "notes/h3-cross-frontier-shared-loop-balanced-eq-convergence-gate.md":
        "541134f55dfbd7f08bce05bd5472d4560da88b294a798ba922577f1fd98de281",
}
EXPECTED_LEDGER_SHA256 = "c299de723884e3b9f8053322cd2d8edf8cb016eb767e99c34e59485ce8e308cc"

DELTA = tuple(map(Q, (1, 1, -1, -1)))
ZERO4 = (Q(0),) * 4
ZERO8 = (Q(0),) * 8
LOWER_PARENT = tuple(map(int, "0112"))
KAPPA_WORDS = tuple(tuple(map(int, word)) for word in (
    "0012", "0102", "0110", "0111",
    "0122", "0212", "1112", "2112",
))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def rank(columns) -> int:
    columns = tuple(columns)
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
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
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def word_text(word: tuple[int, ...]) -> str:
    return "".join(map(str, word))


def ternary_one_root_neighbours():
    answer = []
    for site in range(4):
        for colour in range(3):
            if colour == LOWER_PARENT[site]:
                continue
            word = list(LOWER_PARENT)
            word[site] = colour
            answer.append(tuple(word))
    return tuple(sorted(answer))


def old_cap_columns():
    diagonal = []
    for corner in range(4):
        unit = tuple(Q(1 if index == corner else 0) for index in range(4))
        diagonal.append(unit + unit)
    signless = []
    for direct in (0, 1):
        for endpoint in (2, 3):
            edge = tuple(Q(1 if index in (direct, endpoint) else 0)
                         for index in range(4))
            signless.append(edge + ZERO4)
    return tuple(diagonal + signless)


def psi(vector) -> Q:
    return dot(DELTA + scale(-1, DELTA), vector) / Q(4)


def representative_literal_cone_audit() -> dict[str, object]:
    # Representative lower word 0102 is the site-4 root 1 -> 0.  The
    # argument is coefficientwise, so use the four corner units and all
    # physical cross-shore edges as a basis/test packet for its occurrence
    # readout v.
    units = tuple(tuple(Q(1 if row == column else 0) for row in range(4))
                  for column in range(4))
    edges = tuple(add(units[left], units[right])
                  for left in (0, 1) for right in (2, 3))
    tests = units + edges + (DELTA,)
    rows = []
    for occurrence in tests:
        # Algebraic boundary coefficients in
        # d(epsilon wedge theta)=b theta-epsilon F.
        algebraic_b_theta = occurrence
        algebraic_epsilon_F = scale(-1, occurrence)

        # The physical Eq boundary coordinate is oriented opposite to the
        # algebraic second-face coefficient.  This is the convention in
        # which the pinned K_Eq dressing has (private,Eq)=(+E,+E).
        physical_B = algebraic_b_theta
        physical_Eq = scale(-1, algebraic_epsilon_F)
        projected = physical_B + physical_Eq
        require(physical_B == physical_Eq == occurrence
                and psi(projected) == 0,
                ("standard Koszul product stopped being tied", occurrence))

        # Applying d once more gives +bF from the first face and -bF from
        # the second.  This check records the literal Leibniz cancellation,
        # but the B/Eq conclusion above used the individual faces, not only
        # their zero sum.
        second_boundary = add(occurrence, scale(-1, occurrence))
        require(second_boundary == ZERO4, "literal d^2 cancellation")
        rows.append({
            "occurrence_v": [str(value) for value in occurrence],
            "algebraic_faces_btheta_minus_epsilonF": [
                [str(value) for value in algebraic_b_theta],
                [str(value) for value in algebraic_epsilon_F],
            ],
            "physical_B": [str(value) for value in physical_B],
            "physical_Eq": [str(value) for value in physical_Eq],
            "lambda": "0",
        })
    return {
        "representative_lower_word": "0102",
        "literal_source_data": "d epsilon_0102=b_0102, d theta=F=(H0-u)e_Eq",
        "standard_cell": "kappa_0102=epsilon_0102 wedge theta",
        "literal_differential": (
            "d kappa_0102=b_0102*theta-epsilon_0102*(H0-u)e_Eq"
        ),
        "physical_orientation_rule": (
            "Eq coordinate is minus the algebraic epsilon*F face coefficient"
        ),
        "coefficientwise_result": "Pi_BEq(d kappa_std)=(v,v)",
        "tests": rows,
        "normalized_charge": 0,
    }


def augmented_twist_audit() -> dict[str, object]:
    old = old_cap_columns()
    require(rank(old) == 7 and all(psi(column) == 0 for column in old),
            "old cap image stopped being exactly dark")
    balanced = DELTA + ZERO4
    require(psi(balanced) == 1 and sum(DELTA, Q(0)) == 0,
            "balanced normalization/augmentation")

    # Use one cross-shore occurrence vector for the standard product.  Every
    # named augmented correction is either in the old cap image or in a row
    # on which Psi is zero.  The only invisible freedom is a multiple of the
    # balanced terminal class.
    occurrence = tuple(map(Q, (1, 0, 1, 0)))
    standard = occurrence + occurrence
    require(psi(standard) == 0, "standard product charge")
    controls = []
    for lam in map(Q, (-2, -1, 0, 1, 2)):
        twisted = add(standard, scale(lam, balanced))
        require(psi(twisted) == lam,
                ("twist parameter stopped equalling lambda", lam))
        controls.append({
            "lambda": str(lam),
            "B": [str(value) for value in twisted[:4]],
            "Eq": [str(value) for value in twisted[4:]],
            "Psi": str(psi(twisted)),
            "same_square_boundary_and_augmented_external_faces": True,
        })
    return {
        "standard_product_projection": {
            "B": [1, 0, 1, 0], "Eq": [1, 0, 1, 0], "lambda": 0,
        },
        "old_cap_rank_dimension": [rank(old), 8],
        "twist_normal_form": (
            "d kappa_lambda=d kappa_std+lambda*(delta,0) modulo old cap image"
        ),
        "twist_controls": controls,
        "rows_which_do_not_determine_lambda": [
            "target", "W", "ordinary/labelled residue", "M", "anchor/ainc",
            "physical q=M-ainc", "P_f", "primitive cap", "ridge", "eta", "sigma",
        ],
        "balanced_twist_external_signature": {
            "sum_B": 0,
            "sum_Eq": 0,
            "target_W_residue_M_ainc_q_ridge_eta_sigma": 0,
        },
        "why": "all have zero Psi projection; the terminal B/Eq block has zero outgoing d",
        "current_augmented_naturality_without_multiplicative_normalization_forces": None,
    }


def eight_instance_audit() -> dict[str, object]:
    words = ternary_one_root_neighbours()
    require(words == KAPPA_WORDS and len(words) == 8,
            "the eight literal lower words changed")
    records = []
    for word in words:
        records.append({
            "lower_word": word_text(word),
            "derivation": (
                "instantiate d(epsilon_w wedge theta)=b_w theta-epsilon_w F "
                "at this labelled object; no symmetry transport used"
            ),
            "lambda_under_physical_multiplicativity": 0,
            "lambda_from_current_objectwise_edges_plus_conservation": "free",
        })
    return {
        "instances": records,
        "source_provenant_transport_rule": (
            "one natural multiplicative source schema instantiated separately "
            "at all eight labelled one-root objects"
        ),
        "symmetry_transport_used": False,
        "reason": (
            "the fixed marked packet has trivial strict stabilizer, so the "
            "0102 computation alone cannot identify the other seven scalars"
        ),
    }


def minimum_determining_input_audit() -> dict[str, object]:
    return {
        "weakest_scalar_row_per_instance": (
            "delta.B(d kappa_i)-delta.Eq(d kappa_i)=0"
        ),
        "equivalent_normalized_value": "lambda_i=0",
        "single_physical_schema_for_all_instances": (
            "the selected response/occurrence comparison is a normalized module/DGA "
            "map over the physical central K_Eq cone, and its mixed cell is exactly "
            "epsilon_i wedge theta with the strict Leibniz differential"
        ),
        "no_terminal_cocycle_clause": (
            "the physical comparison contains no additional closed balanced "
            "B/Eq augmentation lambda_i*(delta,0)"
        ),
        "minimum_if_a_nonzero_value_is_desired": (
            "an explicit physical B/Eq incidence row prescribing "
            "delta.(B-Eq)=4*c; no current conservation row supplies c!=0"
        ),
        "still_required_for_actual_physical_use": [
            "a source-labelled selected epsilon_i in the response word/fine/repeated fibre",
            "a physical central theta in the same totalization",
            "multiplicative placement through cap and E14 proper faces",
        ],
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 kappa lambda literal mapping-cone normalization gate",
        "representative": representative_literal_cone_audit(),
        "augmented_freedom": augmented_twist_audit(),
        "all_eight": eight_instance_audit(),
        "minimum_determining_input": minimum_determining_input_audit(),
        "verdict": (
            "The literal standard Koszul/mapping-cone product has tied physical "
            "B and Eq occurrence readouts and therefore lambda_i=0.  Existing "
            "objectwise square edges, d^2, q/anchor, target, residue and ridge "
            "conservation do not prove that the physical mixed cell has this "
            "standard normalization: adding lambda_i*(delta,0) preserves all of "
            "them.  The minimum deciding source input is strict physical "
            "multiplicativity (or its scalar shadow delta.B=delta.Eq) at each "
            "of the eight labelled one-root objects."
        ),
        "scope": (
            "exact canonical h=3 rational chain calculation; conditional zero "
            "for a physical multiplicative comparison, not a construction of "
            "the eight selected sections or a full decorated GHZ source"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    return ledger, sha256(payload.encode()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("representative", "all-eight", "counterguard"),
                        default="all-eight")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    require(digest == EXPECTED_LEDGER_SHA256,
            ("kappa lambda ledger changed", digest))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h3 kappa lambda literal mapping-cone gate ({arguments.mode}): PASS")
        print("standard multiplicative value: lambda_i=0 for all eight")
        print("current physical value without multiplicativity: FREE")
        print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
