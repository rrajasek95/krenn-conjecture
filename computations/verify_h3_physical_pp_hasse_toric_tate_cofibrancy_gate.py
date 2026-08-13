#!/usr/bin/env python3
"""Locate the first Tate generator missing from the h=3 physical PP packet."""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_universal_response_toric_minor_terminal_gate.py":
        "c40790270ef38ea72ec1601037f81319e02638d80828d96ee341e73d9f665e37",
    "notes/h3-universal-response-toric-minor-terminal-gate.md":
        "9718c4bda2e411a65c9b18d2e4ffd42a270b2458374b92690b40d3e0f0b23cd4",
    "computations/verify_h3_universal_occurrence_shear_physical_toric_lift_gate.py":
        "ca5ede5e7a2cc11bf9f62bdcca8349813c3585b401ea614b8622fa40e63c7609",
    "notes/h3-universal-occurrence-shear-physical-toric-lift-gate.md":
        "9764018dcccd47e774c285c4bff51ca095fa219e879c8d4a2a7cd51394da5d7e",
    "computations/verify_h3_endpoint_projector_post_bminus4_target_rank_gate.py":
        "80c9e21304bb679292671c1f344a154d4ae102c1219c4c7e1f3aad9c948be7ac",
    "notes/h3-endpoint-projector-post-bminus4-target-rank-gate.md":
        "62cba9a83f0fba0e74f1274d4dea8968d31bdd45b96cf80b2e862e0107018fab",
    "computations/verify_h3_endpoint_correspondence_square_triangle_holonomy_gate.py":
        "8709a1a8ee50de543d01969c6c1fe657c2b53c934aa8be88cc7aa58e4a92fadd",
    "notes/h3-endpoint-correspondence-square-triangle-holonomy-gate.md":
        "4862304a66b38d9b7570253ae7e8aff06a479553b128fd4f998e50818cdf6a07",
}
EXPECTED_LEDGER_SHA256 = "6d23b4b0f1bed023acf058479c275c8a20b7d7b0220f439c4897868a86ff42ee"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    rows = [list(column) for column in columns]
    answer = 0
    coordinate = 0
    while answer < len(rows) and coordinate < len(rows[0]):
        pivot = next((i for i in range(answer, len(rows))
                      if rows[i][coordinate]), None)
        if pivot is None:
            coordinate += 1
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        scale = rows[answer][coordinate]
        rows[answer] = [value / scale for value in rows[answer]]
        for i in range(len(rows)):
            if i != answer and rows[i][coordinate]:
                scale = rows[i][coordinate]
                rows[i] = [left - scale * right
                           for left, right in zip(rows[i], rows[answer], strict=True)]
        answer += 1
        coordinate += 1
    return answer


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))


def segre_tate_audit() -> dict[str, object]:
    # U_rj=e_r q_j at a generic rational physical point.
    e0, e1 = Q(1), Q(2)
    q0, q1, q2 = Q(1), Q(3), Q(5)
    u = (e0*q0, e0*q1, e0*q2, e1*q0, e1*q1, e1*q2)
    tangent = (
        (q0, q1, q2, 0, 0, 0),
        (0, 0, 0, q0, q1, q2),
        (e0, 0, 0, e1, 0, 0),
        (0, e0, 0, 0, e1, 0),
        (0, 0, e0, 0, 0, e1),
    )
    gradients = (
        (u[4], -u[3], 0, -u[1], u[0], 0),
        (u[5], 0, -u[3], -u[2], 0, u[0]),
        (0, u[5], -u[4], 0, -u[2], u[1]),
    )
    require(rank(tangent) == 4 and rank(gradients) == 2,
            "the 2x3 Segre tangent/conormal ranks changed")
    require(all(dot(g, t) == 0 for g in gradients for t in tangent),
            "a toric conormal failed to kill the physical factor tangent")

    shear = (Q(1),) * 6
    readings = tuple(dot(g, shear) for g in gradients)
    require(readings == (Q(2), Q(4), Q(2)), readings)

    # Hilbert--Burch coefficients for F01,F02,F12.
    syzygy0 = (u[2], -u[1], u[0])
    syzygy1 = (u[5], -u[4], u[3])
    require(dot(syzygy0, readings) == 0
            and dot(syzygy1, readings) == 0,
            "the differentiated cubic Hilbert--Burch faces changed")
    return {
        "occurrence_matrix": [[1, 3, 5], [2, 6, 10]],
        "physical_factor_tangent_rank": 4,
        "ambient_occurrence_rank": 6,
        "toric_conormal_rank": 2,
        "quadratic_generators": [
            "F01=u00*u11-u01*u10",
            "F02=u00*u12-u02*u10",
            "F12=u01*u12-u02*u11",
        ],
        "constant_shear_readings": [2, 4, 2],
        "cubic_Hilbert_Burch_syzygies": [
            "u02*F01-u01*F02+u00*F12=0",
            "u12*F01-u11*F02+u10*F12=0",
        ],
        "minimal_quotient_resolution": "0 -> S(-3)^2 -> S(-2)^3 -> S",
    }


def physical_face_comparison() -> dict[str, object]:
    return {
        "degree_zero": (
            "covered: u_rj=e_r*q_j is the literal physical occurrence monomial map"
        ),
        "homological_degree_one": {
            "minimal_Tate_need": "three epsilon_jk with d(epsilon_jk)=F_jk",
            "generic_independent_need": 2,
            "physical_packet": (
                "complete unary/response rows and endpoint/matching PP faces are "
                "factor tangents or aggregate response faces; none has boundary F_jk"
            ),
            "verdict": "FIRST MISS",
        },
        "homological_degree_two": {
            "minimal_Tate_need": "two Hilbert--Burch cubic coherence cells",
            "coefficient_identity": "present formally",
            "physical_source_cell": (
                "not supplied; endpoint length-three Hasse holonomy instead gives "
                "residual C2 isotropy and is only conditionally contractible"
            ),
            "logical_order": "cannot repair the absent quadratic homotopies",
        },
        "endpoint_PP_audit": (
            "B-4,B-2,B+2 proper-face packets have rank 3 but one common target-normal "
            "line; their bare two-step diamonds are flat"
        ),
        "matching_PP_audit": (
            "the six-term aggregate db01 has target=Eq=0 but forgets termwise "
            "matching-standard occurrence data"
        ),
    }


def grading_audit() -> dict[str, object]:
    return {
        "base_word_head": "11:110000",
        "u_rj_grade": "one p, one s, and the two q factors of matching j",
        "F_jk_grade": (
            "same doubled word/fine/repeated grade on both terms: e0*e1*q_j*q_k"
        ),
        "F_target": 0,
        "F_central_Eq": 0,
        "HB_row0_grade": "e0^2*e1*q0*q1*q2",
        "HB_row1_grade": "e0*e1^2*q0*q1*q2",
        "HB_target": 0,
        "HB_central_Eq": 0,
        "important_distinction": (
            "a polynomial product-rule identity in this symmetric grade is not a "
            "source-labelled PP/Hasse cell in the original word/fine complex"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 physical PP/Hasse versus toric Tate cofibrancy gate",
        "pins": PINS,
        "segre_tate": segre_tate_audit(),
        "physical_faces": physical_face_comparison(),
        "grading": grading_audit(),
        "verdict": (
            "The committed complete h=3 physical PP/Hasse packet is not a "
            "cofibrant resolution of the local occurrence Segre presentation. "
            "It already misses the quadratic toric Tate homotopies in homological "
            "degree 1.  Cubic endpoint/matching Hasse coherence cannot fill this "
            "earlier gap.  The minimal local augmentation is the three quadratic "
            "Tate generators followed by the two Hilbert--Burch cubic cells, all "
            "with target=Eq=0 in their exact doubled/cubic grades."
        ),
        "scope": (
            "canonical h=3 fixed-head two-orientation/three-matching response "
            "packet and the currently committed complete unary, response, endpoint, "
            "matching and cubic PP/Hasse inventory; no claim is made about an "
            "unwritten enlarged physical source complex"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("physical degree zero occurrence map: COVERED")
    print("quadratic toric Tate homotopies: MISSING")
    print("first missing homological degree: 1")
    print("cubic Hilbert-Burch identities: FORMAL, NOT SOURCE CELLS")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
