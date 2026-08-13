#!/usr/bin/env python3
"""Construct the presentation-safe pointed graph and isolate its slack.

Use physical functions f (marked occurrence), G (the mate aggregate), and
the normalized response target u with complete equation

    R=f+G-u.

Adjoin graph variables u_f,z_f and Koszul generators theta,pi:

    d theta = u_f-f,
    d pi    = z_f-G.

The two relations are monic in u_f,z_f, so this is a presentation-safe
resolution of the original algebra.  It gives

    [d(u_f-u)] = -[dz_f]

in the relative cotangent quotient, and on H0 one has z_f=G=u-f.  Thus the
relative graph exists constructively, but it transfers rather than kills the
pointed class.  Adding d kappa=z_f kills it only by changing the classical
fibre to G=0 (equivalently f=u).
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py":
        "c583279d8f4cb7efc24b7fc4784e480b63acb1ca7fe430ae1a7e2db2b854c11b",
    "computations/verify_h3_anchor_conormal_functoriality_bridge.py":
        "83879756547765878c36944c1ab14827ab77a1f217931bc05db0c72cb0af32a8",
    "computations/verify_h3_universal_graph_derived_base_change_physical_descent_gate.py":
        "9e60fb8410288a192b8be3b59938e5e7ba4ea42b455fee67b94ca6ef37777fde",
    "computations/verify_h3_trapped_carrier_occurrence_graph_hessian_cone_gate.py":
        "ce28ff5d25bf575c280a21c0e35c6dc1ebef54eb039ac94cdc25932a61b95829",
    "computations/verify_h3_scaled_occurrence_anchor_bridge_alternative.py":
        "ba01612572513e02c60bd5d9a319d8302013e3d73e6a52ae229af8b07dd02507",
    "computations/verify_h3_reduced_eq_occurrence_graph_tensor_gate.py":
        "5b6db94ecff07e5946007a0d7f95c4ffffb52acc74544d173d5b48cb0ccb0bc9",
}
EXPECTED_LEDGER_SHA256 = (
    "244a2305e08462e3a6e15888a6c539fcc57fc6073a045718d39110e6f0716f8f"
)

# Cotangent coordinate order: (f,G,u,u_f,z_f).
WIDTH = 5


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def add(*vectors):
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(rows) -> int:
    work = [list(map(Q, row)) for row in rows]
    answer = 0
    for column in range(WIDTH):
        pivot = next((row for row in range(answer, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(len(work)):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def in_span(rows, target) -> bool:
    return rank(rows) == rank(tuple(rows) + (tuple(target),))


def physical_and_graph_rows():
    response = tuple(map(Q, (1, 1, -1, 0, 0)))
    theta = tuple(map(Q, (-1, 0, 0, 1, 0)))
    pi = tuple(map(Q, (0, -1, 0, 0, 1)))
    pointed = tuple(map(Q, (0, 0, -1, 1, 0)))
    slack = tuple(map(Q, (0, 0, 0, 0, 1)))
    mate = tuple(map(Q, (0, 1, 0, 0, 0)))
    return response, theta, pi, pointed, slack, mate


def presentation_safe_graph_audit() -> dict[str, object]:
    response, theta, pi, pointed, slack, mate = (
        physical_and_graph_rows()
    )
    rows = (response, theta, pi)

    # The graph equations are triangular/monic in (u_f,z_f).  Their Jacobian
    # with respect to those new variables has determinant one.
    new_variable_jacobian = ((Q(1), Q(0)), (Q(0), Q(1)))
    determinant = (new_variable_jacobian[0][0]
                   * new_variable_jacobian[1][1]
                   - new_variable_jacobian[0][1]
                   * new_variable_jacobian[1][0])
    require(determinant == 1 and rank(rows) == 3,
            "the monic pointed graph resolution changed")

    # R+theta+pi=pointed+slack.  Hence the desired conormal is -dz_f in the
    # quotient.  Neither class is zero before a new z_f relation is imposed.
    require(add(response, theta, pi) == add(pointed, slack)
            and not in_span(rows, pointed)
            and not in_span(rows, slack)
            and in_span(rows + (slack,), pointed),
            "the pointed/slack cotangent identity changed")

    # Modulo R,theta,pi one has u=f+G, u_f=f, and z_f=G.  The cotangent
    # version is pointed=-mate; verify it in the row quotient.
    require(in_span(rows, add(pointed, mate))
            and not in_span(rows, mate),
            "the full-response reduction P_f=-G changed")

    return {
        "physical_equation": "R=f+G-u (equivalently H0=f+G and H0=u)",
        "graph_DGA": {
            "new_degree_zero": ["u_f", "z_f"],
            "degree_one": ["theta", "pi"],
            "d_theta": "u_f-f",
            "d_pi": "z_f-G",
            "new_variable_Jacobian_det": 1,
            "presentation_safe": True,
            "H0_elimination": "u_f=f, z_f=G=u-f",
        },
        "relative_cotangent_identity": "[d(u_f-u)]=-[dz_f]=-[dG]",
        "pointed_class_zero_in_original_graph": False,
        "interpretation": (
            "the relative cotangent Koszul cell exists, but it transfers "
            "the pointed class to the slack/basepoint coordinate z_f"
        ),
    }


def fibre_change_and_nonfill_audit() -> dict[str, object]:
    response, theta, pi, pointed, slack, mate = (
        physical_and_graph_rows()
    )
    rows = (response, theta, pi)

    # This tangent kills the full response and both safe graph relations, but
    # is seen by the pointed/slack/mate classes.
    tangent = tuple(map(Q, (1, 1, 2, 1, 1)))
    require(all(dot(row, tangent) == 0 for row in rows)
            and dot(pointed, tangent) == -1
            and dot(slack, tangent) == 1
            and dot(mate, tangent) == 1,
            "the graph-slack tangent separator changed")

    # A concrete point of the old graph which is deleted by z_f=0.
    point = {
        "f": Q(1), "G": Q(1), "u": Q(2),
        "u_f": Q(1), "z_f": Q(1),
    }
    require(point["u"] == point["f"] + point["G"]
            and point["u_f"] == point["f"]
            and point["z_f"] == point["G"]
            and point["z_f"] != 0,
            "the classical graph counterpoint changed")

    # Adding kappa with d kappa=z_f kills pointed, but raises conormal rank
    # and makes H0=A/(G), equivalently imposes f=u.
    require(rank(rows + (slack,)) == rank(rows) + 1
            and in_span(rows + (slack,), pointed)
            and in_span(rows + (slack,), mate),
            "the z_f basepoint attachment changed")

    # The separator lives on a private graph coordinate.  It is not one of
    # the literal physical terminal rows; forgetting z_f erases it.  This is
    # a sharp nonfill certificate, not yet a conjecture-level terminal.
    projected_tangent = tangent[:3]
    require(projected_tangent == (1, 1, 2),
            "the private slack projection changed")

    return {
        "kernel_witness_f_G_u_uf_zf": list(map(int, tangent)),
        "pointed_on_witness": -1,
        "slack_on_witness": 1,
        "mate_aggregate_on_witness": 1,
        "new_absolute_cell": "d kappa=z_f",
        "effect_on_H0": "A/(z_f)=A/(G)=A/(f-u)",
        "changes_classical_fibre": True,
        "deleted_old_graph_point": [1, 1, 2, 1, 1],
        "first_nonfill_dual": "evaluation on the displayed graph tangent",
        "physical_terminal_already_typed": False,
        "terminal_obstruction": (
            "z_f and the mate selector G are private occurrence coordinates, "
            "not literal q/ainc/word/ridge/eta/sigma/W terminal rows"
        ),
    }


def compare_scaled_orbit_route_audit() -> dict[str, object]:
    # The exact marked diagonal fails already in the one marked/mate quotient.
    # The all-occurrence centered orbit replaces it by the unit-scaled law
    # N du_f=du, which suffices for visibility but still needs physical descent.
    n = Q(90)
    marked_visibility = Q(1)
    central_visibility = n * marked_visibility
    require(central_visibility == 90,
            "the scaled anchor visibility coefficient changed")
    return {
        "exact_P_f_constructed_in_current_original_source_inventory": False,
        "exact_original_source_membership_criterion": (
            "dG belongs to the conormal span of the remaining complete "
            "physical source equations"
        ),
        "full_response_graph_alone_satisfies_criterion": False,
        "presentation_safe_relative_P_f_with_slack": True,
        "smallest_exact_absolute_extension": "one basepoint cell d kappa=z_f",
        "preferred_weaker_interface_II_route": (
            "physically descend the centered all-occurrence class, giving "
            "90[du_f]=[du]; scale 90 is a unit and preserves visibility"
        ),
        "weaker_route_already_constructed": False,
        "common_remaining_issue": (
            "physical occurrence selection/landing with complete augmented "
            "terminal typing"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "P2 pointed source graph slack gate",
        "pins": PINS,
        "presentation_safe_relative_construction":
            presentation_safe_graph_audit(),
        "absolute_nonfill_and_fibre_change":
            fibre_change_and_nonfill_audit(),
        "scaled_orbit_comparison": compare_scaled_orbit_route_audit(),
        "sharp_verdict": (
            "The graph/Koszul resolution with u_f,z_f is an explicit "
            "presentation-safe relative construction.  It does not fill "
            "P_f: the class becomes -dz_f=-dG.  Killing z_f is one new "
            "marked basepoint relation and changes the classical source "
            "fibre.  An old-source fill is equivalent to one explicit extra "
            "membership dG in the remaining physical conormal rows; no such "
            "membership is supplied by the graph/full response.  Its private "
            "tangent detector is not a physical terminal until the slack is "
            "landed in the complete augmented comparison."
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("pointed graph K(u_f-f,z_f-G): PRESENTATION-SAFE")
    print("relative cotangent: [d(u_f-u)]=-[dz_f]=-[dG]")
    print("absolute P_f from graph/full response alone: NOT FILLED")
    print("d kappa=z_f: FILLS BUT CHANGES FIBRE TO G=0")
    print("private slack dual: NOT YET A PHYSICAL TERMINAL")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
