#!/usr/bin/env python3
"""Test whether old P_f, the cap graph, or a terminal closes the centered face.

Write z_f for the private marked-occurrence graph coordinate, Z for the sum
of all occurrence graph coordinates, and u for the global central anchor.
The complete symmetric graph normal is B=dZ-du.  The retained centered face
from the Maschke cone is

    gamma_c = 90 dz_f-dZ,

or gamma_c=90 dz_f-du modulo B.  The old pointed face is instead

    P_f = dz_f-du.

Modulo B one has gamma_c=90 P_f+89 du.  Thus P_f does not kill gamma_c:
the surviving term is the global anchor itself.  In the literal three-row
model (dz_f,dZ,du), B and P_f have rank two, gamma_c raises it to three,
and the common-scale tangent (1,1,1) reads gamma_c as 89.  Adding gamma_c
therefore changes the old cotangent space; it is not a presentation-safe
consequence of P_f.

The physical cap graph T+rho is closed and has only target/residue values in
its cap word.  It is zero in the response-conormal, q, anchor and ridge
quotient, so it cannot cancel gamma_c before a cross-word comparison exists.
Finally, failure of source-conormal membership produces a tangent, not a
physical output/Fredholm covector.  The q/generator alternative applies only
after gamma_c has been placed as a complete physically typed comparison
column.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_centered_occurrence_endpoint_matching_maschke_pointed_gate.py":
        "1994697181c6034267d98a26a28ab4c69c3fcb979b657c8d7d06fc81b86650ed",
    "computations/verify_h3_scaled_occurrence_anchor_bridge_alternative.py":
        "ba01612572513e02c60bd5d9a319d8302013e3d73e6a52ae229af8b07dd02507",
    "computations/verify_h3_p2_pointed_source_graph_slack_gate.py":
        "d36e26ef2c82b018b62228c159f1f17a63d0c19ed1fd342d7684cbf4e55b1098",
    "computations/verify_h3_e14_cap_graph_two_parameter_flat_transport_gate.py":
        "42bf68eeb963d568d1c8d9156d4176bec31a114b6fe804744833364fe3633475",
    "computations/verify_h3_interface_ii_anchor_faithful_central_comparison.py":
        "fe77afbafa23656d8afd6aaa0218e6134776205ffe4525658273de80f9f004a6",
    "computations/verify_h3_augp2_primitive_cap_response_keq_reduction_gate.py":
        "4dabdae7b9060bdb92c0ed32b0016e7e2694750dc176e1857cc9a54cb8176587",
    "computations/verify_h3_derived_terminal_indeterminacy_or_relative_generator.py":
        "9327b57598a5264c11e5c3085e1afceaec8fd72c408f5fc1f1eaa2490a13a8b1",
}
EXPECTED_LEDGER_SHA256 = (
    "4cc227dbd17fd7e227beafe726a76455087de55daecad2d31d87e0c0ca3af316"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def add(left, right, right_scale=Q(1)):
    return tuple(Q(a) + Q(right_scale) * Q(b)
                 for a, b in zip(left, right, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def rank(columns) -> int:
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


def conormal_scale_audit():
    # Coordinates are (dz_f,dZ,du).  B is the symmetric complete-response
    # graph normal, P is the old unscaled marked/global diagonal, and gamma
    # is the centered face retained by the Maschke presentation-safe cone.
    symmetric = (Q(0), Q(1), Q(-1))
    pointed = (Q(1), Q(0), Q(-1))
    centered = (Q(90), Q(-1), Q(0))
    global_anchor = (Q(0), Q(0), Q(1))
    scale_tangent = (Q(1), Q(1), Q(1))

    require(add(scale(90, pointed), symmetric, -1)
            == add(centered, global_anchor, -89),
            "the centered/unscaled normalization identity changed")
    require(rank((symmetric, pointed)) == 2
            and rank((symmetric, pointed, centered)) == 3,
            "the centered pointed conormal rank changed")
    require(dot(symmetric, scale_tangent) == 0
            and dot(pointed, scale_tangent) == 0
            and dot(centered, scale_tangent) == 89,
            "the common-scale tangent certificate changed")

    # After quotienting by B, use coordinates (dz_f,du).
    pointed_reduced = (Q(1), Q(-1))
    centered_reduced = (Q(90), Q(-1))
    anchor_reduced = (Q(0), Q(1))
    require(centered_reduced
            == add(scale(90, pointed_reduced), anchor_reduced, 89),
            "[gamma]=90[P_f]+89[du] changed")
    require(rank((pointed_reduced, centered_reduced)) == 2,
            "P_f unexpectedly consumed the scaled centered face")

    return {
        "coordinate_order": ["dz_f", "dZ", "du"],
        "complete_symmetric_normal_B": [0, 1, -1],
        "old_unscaled_P_f": [1, 0, -1],
        "retained_centered_gamma_c": [90, -1, 0],
        "rank_B_Pf_then_gamma": [2, 3],
        "common_scale_tangent": [1, 1, 1],
        "tangent_values": {"B": 0, "P_f": 0, "gamma_c": 89},
        "quotient_identity": "[gamma_c]=90[P_f]+89[du] modulo B",
        "characteristic_zero_consequence": (
            "89 is a unit; killing gamma_c after P_f kills the surviving "
            "global-anchor scale rather than deriving a presentation face"
        ),
        "H0_verdict": (
            "B and P_f retain one common-scale tangent; adjoining gamma_c "
            "removes it, so gamma_c is not a presentation-safe consequence"
        ),
    }


def cap_and_grade_audit():
    # Coarse direct-sum rows are (response centered conormal, target,
    # cap ordinary residue, physical q, shifted ridge).  The cap graph has
    # no response/q/ridge projection.  Unknown q/ridge values of a sought
    # centered physical cell are deliberately not assigned here.
    centered_shadow = (Q(1), Q(0), Q(0), Q(0), Q(0))
    cap_graph = (Q(0), Q(1), Q(1), Q(0), Q(0))
    response_projection = (Q(1), Q(0), Q(0), Q(0), Q(0))
    require(rank((cap_graph,)) == 1
            and rank((cap_graph, centered_shadow)) == 2,
            "the cap graph entered the response centered line")
    require(dot(response_projection, cap_graph) == 0
            and dot(response_projection, centered_shadow) == 1,
            "the response word separator changed")

    return {
        "coarse_row_order": [
            "response centered conormal", "target", "cap scalar ores",
            "physical q", "shifted ridge",
        ],
        "centered_response_shadow": [1, 0, 0, 0, 0],
        "physical_cap_graph_T_plus_rho": [0, 1, 1, 0, 0],
        "rank_cap_then_centered": [1, 2],
        "response_word_separator": [1, 0, 0, 0, 0],
        "response_type": {
            "head_word": "11:110000",
            "first_PP": "dc01=30db01-dR (six literal dq terms)",
            "repeated_degree": "response squarefree q matching",
        },
        "cap_type": {
            "word": "01211222",
            "fine_degree": "t*q_(v,N)",
            "repeated_degree": "P3+K2",
            "boundary_W_Eq_lower_anchor_eta_sigma": 0,
            "target_scalar_ores": [1, 1],
        },
        "verdict": (
            "T+rho is a flat target/residue normalizer after cross-word "
            "placement; it has zero projection to gamma_c and cannot create "
            "the response pointed face"
        ),
    }


def terminal_variance_audit():
    # A nonmembership witness for source conormal rows is a tangent in ker A.
    # It need not carry physical q or ridge.  This smallest guard retains the
    # exact B/P/gamma values and sets the independent q/ridge readouts to zero.
    source_rows = (
        (Q(0), Q(1), Q(-1)),
        (Q(1), Q(0), Q(-1)),
    )
    centered = (Q(90), Q(-1), Q(0))
    witness = (Q(1), Q(1), Q(1))
    physical_q = (Q(0), Q(0), Q(0))
    shifted_ridge = (Q(0), Q(0), Q(0))
    require(all(dot(row, witness) == 0 for row in source_rows)
            and dot(centered, witness) == 89
            and dot(physical_q, witness) == dot(shifted_ridge, witness) == 0,
            "the terminal-typing counterguard changed")

    # Once a candidate is a column in a complete physical codomain, ordinary
    # finite duality is exhaustive.  This 2D sample checks both arms and is a
    # mutation guard for the variance statement.
    old_column = (Q(1), Q(0))
    internal_candidate = (Q(2), Q(0))
    external_candidate = (Q(0), Q(1))
    separator = (Q(0), Q(1))
    require(rank((old_column, internal_candidate)) == 1
            and rank((old_column, external_candidate)) == 2
            and dot(separator, old_column) == 0
            and dot(separator, external_candidate) == 1,
            "the complete-column membership/dual alternative changed")

    return {
        "source_nonmembership_witness": [1, 1, 1],
        "witness_values": {
            "B": 0, "P_f": 0, "gamma_c": 89,
            "physical_q_guard": 0, "shifted_ridge_guard": 0,
        },
        "variance_warning": (
            "a tangent detecting a missing source conormal is not a left "
            "covector on the physical correction codomain"
        ),
        "physical_terminal_available_now": False,
        "exact_conditional_alternative": (
            "after a source-labelled map places gamma_c as a column b in the "
            "complete augmented physical codomain E, either b is in im(J), "
            "or finite duality gives lambda J=0 and lambda(b)=1; only then "
            "q-kernel/generator versus Fredholm typing applies"
        ),
        "first_missing_terminal_mate": (
            "a complete word/fine/repeated physical landing of gamma_c with "
            "defined q, anchor, ridge, W, eta/sigma and residue readouts"
        ),
    }


def shortest_interface():
    return {
        "name": "scaled pointed centered-response attachment",
        "required_faces": [
            {
                "degree": 0,
                "face": "U_c=90e_f-1_90",
                "type": "selected response head/word 11:110000",
            },
            {
                "degree": 1,
                "face": "dU_c=gamma_c=90df-dR",
                "role": "scaled anchor/conormal",
            },
            {
                "degree": "matching first PP",
                "face": "dc01=30db01-dR",
                "role": "six-term aggregate physical-q face",
            },
            {
                "degree": "fixed-word endpoint paths",
                "face": "18-term target normal N_f and B-natural C2,C3",
                "role": "target correction after pointed entry",
            },
            {
                "degree": "cross-word cap",
                "face": "flat T+rho plus primitive cap placement",
                "type": "01211222 / t*q_(v,N) / P3+K2",
            },
            {
                "degree": "relative Kahler",
                "face": "gamma_v=-dOmega_v",
                "role": "ridge with unique eta/sigma contractions",
            },
        ],
        "not_a_required_new_face": (
            "nontrivial finite-group character directions: Maschke contracts "
            "them once the termwise physical action is supplied"
        ),
        "why_this_is_shortest": (
            "P_f has the wrong anchor normalization, T+rho has zero response "
            "projection, and terminal duality cannot be invoked before the "
            "complete augmented placement exists"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": (
            "h3 centered pointed face versus old P_f, cap graph and physical "
            "terminal gate"
        ),
        "pins": PINS,
        "conormal_scale": conormal_scale_audit(),
        "cap_and_grade": cap_and_grade_audit(),
        "terminal_variance": terminal_variance_audit(),
        "shortest_positive_interface": shortest_interface(),
        "verdict": (
            "None of the three proposed existing mechanisms consumes the "
            "retained centered face without an additional physical landing. "
            "Modulo the complete symmetric normal, gamma_c=90P_f+89du, so "
            "old P_f leaves the global-anchor scale and adjoining gamma_c "
            "changes the conormal rank.  T+rho is a differently graded flat "
            "target/residue normalizer with zero response projection.  A "
            "nonfill witness is a source tangent, not a physical Fredholm "
            "covector.  The shortest remaining theorem is one complete scaled "
            "pointed centered-response attachment with its PP/q, target, cap, "
            "anchor and shifted-ridge faces."
        ),
        "scope": (
            "canonical h=3 characteristic-zero response/cap comparison; exact "
            "at conormal rank and literal word/fine/repeated projections, but "
            "does not construct the missing augmented attachment"
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
    print("old P_f vs centered gamma_c: RANK 2 -> 3 (residual 89*du)")
    print("cap graph T+rho: ZERO RESPONSE-CONORMAL PROJECTION")
    print("nonfill dual: SOURCE TANGENT, NOT PHYSICAL TERMINAL")
    print("shortest theorem: SCALED POINTED CENTERED-RESPONSE ATTACHMENT")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
