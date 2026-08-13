#!/usr/bin/env python3
"""Correct the absolute-homogenizer scope of the centered pointed face gate.

The physical Krenn fibre has affine target equations H_c-delta_c=0.  The
symbol u in H_0-u is a homogenizer used by the graded EqSystem/Tate model;
the physical chart is obtained by dehomogenizing u=1.  Its relative
cotangent therefore has du=0.

For a marked occurrence graph coordinate z_f and aggregate Z, put

    B=dZ-du,
    P_f=d(z_f-u),
    gamma_c=90 dz_f-dZ.

In the absolute homogenized cone gamma_c=90 P_f-B+89 du, which is the rank
obstruction recorded in 1816162.  In the physical fixed-target cotangent
du=0, however,

    gamma_c=90 P_f-B.

Thus there is no independent centered-face obstruction after a physical
P_f is granted.  This does not construct P_f: the presentation-safe graph
transfers it to the mate slack -dG, and adjoining the marked/global
diagonal still changes the old physical fibre.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_centered_pointed_face_existing_conormal_cap_terminal_gate.py":
        "dabaf6c5132f835c6d681d1ecb30611eae8b0920b2c97272e487bcb9c9f068c9",
    "computations/verify_h3_direct_free_first_syzygy_multidegree_gate.py":
        "7308d9b55740644affedbda04c8085517bcc2a0881eb5a8c839fc6cdee5547e5",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "computations/verify_h3_p2_pointed_source_graph_slack_gate.py":
        "d36e26ef2c82b018b62228c159f1f17a63d0c19ed1fd342d7684cbf4e55b1098",
    "computations/verify_h3_scaled_occurrence_anchor_bridge_alternative.py":
        "ba01612572513e02c60bd5d9a319d8302013e3d73e6a52ae229af8b07dd02507",
}
EXPECTED_LEDGER_SHA256 = (
    "3c8f0e7c2546f38b91f343e0e42597d66593848f03954951ab14f7513a5e9f6e"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(left, right, right_scale=Q(1)):
    return tuple(Q(a) + Q(right_scale) * Q(b)
                 for a, b in zip(left, right, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


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


def absolute_and_relative_audit():
    # Absolute coordinates are (dz_f,dZ,du).
    symmetric = (Q(0), Q(1), Q(-1))
    pointed = (Q(1), Q(0), Q(-1))
    centered = (Q(90), Q(-1), Q(0))
    du = (Q(0), Q(0), Q(1))
    scale_tangent = (Q(1), Q(1), Q(1))
    require(centered
            == add(add(scale(90, pointed), symmetric, -1), du, 89),
            "the absolute homogenizer identity changed")
    require(rank((symmetric, pointed)) == 2
            and rank((symmetric, pointed, centered)) == 3
            and dot(scale_tangent, centered) == 89,
            "the absolute rank guard changed")

    # Restrict to the physical affine target chart u=1, hence du=0.  In
    # relative coordinates (dz_f,dZ), B=dZ, P_f=dz_f.
    symmetric_relative = (Q(0), Q(1))
    pointed_relative = (Q(1), Q(0))
    centered_relative = (Q(90), Q(-1))
    require(centered_relative
            == add(scale(90, pointed_relative), symmetric_relative, -1),
            "gamma_c=90P_f-B failed in the fixed-target cotangent")
    require(rank((symmetric_relative, pointed_relative)) == 2
            and rank((symmetric_relative, pointed_relative,
                      centered_relative)) == 2,
            "the fixed-target centered face raised rank")
    return {
        "absolute_homogenized_cone": {
            "coordinates": ["dz_f", "dZ", "du"],
            "identity": "gamma_c=90P_f-B+89du",
            "rank_B_Pf_then_gamma": [2, 3],
            "common_scale_tangent": [1, 1, 1],
            "scope": "includes variation of the target homogenizer",
        },
        "physical_affine_fibre": {
            "source_equation": "G_pure=H_pure-1=0",
            "dehomogenization": "u=1",
            "relative_cotangent": "du=0",
            "coordinates": ["dz_f", "dZ"],
            "identity": "gamma_c=90P_f-B",
            "rank_B_Pf_then_gamma": [2, 2],
        },
        "correction_to_1816162": (
            "the 89du class is an absolute cone-normalization direction, not "
            "an obstruction in the fixed-target physical cotangent"
        ),
    }


def remaining_physical_scope():
    return {
        "complete_response_normal_B": "already physical",
        "centered_face_after_granting_Pf": "constructed as 90P_f-B",
        "physical_Pf_status": "OPEN",
        "why_Pf_remains_open": (
            "the monic occurrence graph only transfers P_f=d(z_f-u) to "
            "the mate slack -dG; adjoining P_f kills an actual old tangent"
        ),
        "anchor_law": (
            "once P_f descends, fixed-target du=0 gives dz_f=0; equivalently "
            "the scaled centered law follows, so no separate factor-90 face"
        ),
        "cap_graph_status": (
            "still downstream and differently graded; this correction does "
            "not construct P_f or cross-word cap/ridge/q transport"
        ),
        "shortest_corrected_interface": (
            "construct one physical pointed occurrence conormal P_f in the "
            "complete word/fine/q/anchor comparison; the centered Maschke "
            "face then follows formally from the complete response normal"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "h3 centered pointed fixed-target normalization correction",
        "pins": PINS,
        "absolute_vs_relative": absolute_and_relative_audit(),
        "remaining_scope": remaining_physical_scope(),
        "verdict": (
            "The normalization loophole is real.  The physical source fibre "
            "has target coefficient one, so u is a graded homogenizer and "
            "du=0 in its relative cotangent.  Therefore gamma_c=90P_f-B and "
            "the centered face has no independent obstruction after P_f is "
            "granted.  The old P_f itself remains the sole pointed entry: "
            "the presentation-safe graph transfers it to a private mate "
            "slack but does not make it a physical boundary."
        ),
        "scope": (
            "canonical h=3 fixed-target affine physical fibre versus its "
            "absolute homogenized cone; does not construct P_f or later "
            "cross-word augmented faces"
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
    print("absolute cone: gamma_c=90P_f-B+89du (rank 2 -> 3)")
    print("physical affine fibre: du=0, gamma_c=90P_f-B (rank 2 -> 2)")
    print("1816162 extra 89du obstruction: SUPERSEDED IN FIXED TARGET")
    print("remaining pointed entry: PHYSICAL P_f")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
