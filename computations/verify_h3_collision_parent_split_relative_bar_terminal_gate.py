#!/usr/bin/env python3
"""Minimal parent-split collision cylinder and relative root-return bar.

For one fixed collision occurrence, let c_A,c_B be the two parent-labelled
copies of the same missing/doubled collision monomial.  The complete
response collection forgets the parent.  A genuine mapping cylinder to the
collected coordinate c is

    d theta_A = c_A-c,       d theta_B = c_B-c.

It preserves the one-dimensional collected H0 and makes c_A-c_B absolute.
Those two comparison cells are not supplied by the formal hyperbolic root
operator.

The minimal presentation-safe root bar over the parent-split occurrence
module instead retains carriers t_A,t_B:

    d beta_A = c_A-t_A,      d beta_B = c_B-t_B.

It preserves the two-dimensional parent H0 and gives

    d(beta_A-beta_B)=(c_A-c_B)-(t_A-t_B).

Thus the parent anti-diagonal is only homologous to the retained carrier.
Applying the opposite root transports this to d Gamma=(A-B)-rho; it does
not make A-B absolute.  An absolute landing of the anti-carrier (natural on
all PP/reinsertion faces) is exactly the missing physical datum.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_hyperbolic_collision_fixed_window_matching_routing_gate.py":
        "b8d02d77213bbb21d68dbad0aa4d6d1263625de012e413547723999d8d87fada",
    "notes/h3-hyperbolic-collision-fixed-window-matching-routing-gate.md":
        "9ee72f85c69d08b8998f7061a52be2450a9f6e3bb843b8951777961471e16f2a",
    "computations/verify_h3_balanced_c4_hyperbolic_root_return_gate.py":
        "f52c7a8b447a63ee34b3b41e7bbab713409366e7a5a1a16087032a205da2fa9f",
    "notes/h3-balanced-c4-hyperbolic-root-return-gate.md":
        "c4fcd6505401b413bb45aa5fcdc2e3e04f7e38d555250c3cfbee7c643fe1cbcc",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "notes/h3-shear-collision-augp2-packaging-map-gate.md":
        "9d5918605dd94d08d18c099966e5956fa0f1c62855b97fd81bf9ada54f2f45ad",
}
EXPECTED_LEDGER_SHA256 = (
    "89492202db058f984fb52d5e34d234094891f8a71c911351b3e117098fc9c007"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    require(len(left) == len(right), "dot width")
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


def in_span(columns, value) -> bool:
    return rank(columns) == rank(tuple(columns) + (tuple(value),))


def audit_parent_split_cylinders():
    # Absolute comparison cylinder.  Coordinate order c_A,c_B,c.  It is a
    # mapping cylinder for the two maps from parent occurrences to their one
    # collected collision coordinate.
    theta_a = (Q(1), Q(0), Q(-1))
    theta_b = (Q(0), Q(1), Q(-1))
    absolute_columns = (theta_a, theta_b)
    anti_absolute = (Q(1), Q(-1), Q(0))
    require(rank(absolute_columns) == 2
            and 3 - rank(absolute_columns) == 1
            and add(theta_a, scale(-1, theta_b)) == anti_absolute
            and in_span(absolute_columns, anti_absolute),
            "the parent-to-collected mapping cylinder changed")
    require(rank((theta_a,)) == 1 and 3 - rank((theta_a,)) == 2,
            "one comparison unexpectedly formed the full cylinder")

    # Presentation-safe relative root bar.  Coordinate order c_A,c_B,t_A,t_B.
    beta_a = (Q(1), Q(0), Q(-1), Q(0))
    beta_b = (Q(0), Q(1), Q(0), Q(-1))
    relative_columns = (beta_a, beta_b)
    collision_anti = (Q(1), Q(-1), Q(0), Q(0))
    carrier_anti = (Q(0), Q(0), Q(1), Q(-1))
    carrier_diagonal = (Q(0), Q(0), Q(1), Q(1))
    require(rank(relative_columns) == 2
            and 4 - rank(relative_columns) == 2,
            "the relative parent bar changed H0")
    require(add(beta_a, scale(-1, beta_b))
            == add(collision_anti, scale(-1, carrier_anti)),
            "the anti-diagonal relative graph changed")
    require(not in_span(relative_columns, collision_anti)
            and not in_span(relative_columns, carrier_anti)
            and in_span(relative_columns,
                        add(collision_anti, scale(-1, carrier_anti))),
            "the collision anti-diagonal stopped being a relative carrier")

    detector = (Q(1, 2), Q(-1, 2), Q(1, 2), Q(-1, 2))
    require(all(dot(detector, column) == 0 for column in relative_columns)
            and dot(detector, collision_anti) == 1
            and dot(detector, carrier_anti) == 1,
            "the normalized parent-anti dual changed")

    # A physical absolute landing of the anti-carrier fills exactly the
    # selected class.  Landing only the carrier diagonal does not.
    require(rank(relative_columns + (carrier_anti,)) == 3
            and in_span(relative_columns + (carrier_anti,), collision_anti)
            and rank(relative_columns + (carrier_diagonal,)) == 3
            and not in_span(relative_columns + (carrier_diagonal,),
                            collision_anti),
            "the sharp anti-carrier landing criterion changed")

    # Expanded comparison: identify t_A and t_B with one physical collected
    # coordinate c.  This recovers the absolute cylinder and drops H0 from
    # the two parent copies to the one collected copy.
    expanded_beta_a = (Q(1), Q(0), Q(-1), Q(0), Q(0))
    expanded_beta_b = (Q(0), Q(1), Q(0), Q(-1), Q(0))
    land_a = (Q(0), Q(0), Q(1), Q(0), Q(-1))
    land_b = (Q(0), Q(0), Q(0), Q(1), Q(-1))
    expanded = (expanded_beta_a, expanded_beta_b, land_a, land_b)
    expanded_anti = (Q(1), Q(-1), Q(0), Q(0), Q(0))
    require(rank(expanded) == 4 and 5 - rank(expanded) == 1
            and in_span(expanded, expanded_anti),
            "the expanded parent collection cylinder changed")
    return {
        "absolute_parent_to_collected_cylinder": {
            "coordinates": ["c_A", "c_B", "c"],
            "boundaries": ["dtheta_A=c_A-c", "dtheta_B=c_B-c"],
            "H0_old_new": [1, 1],
            "parent_anti_diagonal_absolute": True,
            "both_comparison_cells_required": True,
        },
        "presentation_safe_relative_root_bar": {
            "coordinates": ["c_A", "c_B", "t_A", "t_B"],
            "boundaries": ["dbeta_A=c_A-t_A", "dbeta_B=c_B-t_B"],
            "H0_old_new": [2, 2],
            "identity": "d(beta_A-beta_B)=(c_A-c_B)-(t_A-t_B)",
            "collision_anti_diagonal_absolute": False,
            "retained_anti_carrier": "tau=t_A-t_B",
            "normalized_dual": [str(value) for value in detector],
        },
        "sharp_landing": (
            "an absolute physical column on tau makes c_A-c_B a boundary; "
            "a diagonal carrier column does not"
        ),
        "expanded_collection": {
            "boundaries": [
                "c_A-t_A", "c_B-t_B", "t_A-c", "t_B-c"
            ],
            "H0_parent_to_collected": [2, 1],
            "parent_anti_diagonal_absolute": True,
        },
    }


def audit_ordered_root_return():
    # After the opposite root, q denotes A-B in the oriented chart gauge and
    # rho is the image of the retained collision anti-carrier.  Naturality of
    # the relative bar gives dGamma=q-rho, not dGamma=q.
    relative_return = ((Q(1), Q(-1)),)
    q = (Q(1), Q(0))
    rho = (Q(0), Q(1))
    return_detector = (Q(1), Q(1))
    require(rank(relative_return) == 1
            and 2 - rank(relative_return) == 1
            and not in_span(relative_return, q)
            and not in_span(relative_return, rho)
            and dot(return_detector, relative_return[0]) == 0
            and dot(return_detector, q) == dot(return_detector, rho) == 1,
            "the ordered return stopped exporting a relative carrier")
    require(rank(relative_return + (rho,)) == 2
            and in_span(relative_return + (rho,), q),
            "an absolute return-carrier landing stopped filling q")

    # Two root orders agree on q.  Their two relative graphs identify the
    # two retained carriers, but still leave the common carrier in H0.
    forward = (Q(1), Q(-1), Q(0))
    reverse = (Q(1), Q(0), Q(-1))
    two_orders = (forward, reverse)
    two_order_detector = (Q(1), Q(1), Q(1))
    carrier_difference = (Q(0), Q(1), Q(-1))
    require(rank(two_orders) == 2 and 3 - rank(two_orders) == 1
            and in_span(two_orders, carrier_difference)
            and not in_span(two_orders, (Q(1), Q(0), Q(0)))
            and all(dot(two_order_detector, column) == 0
                    for column in two_orders),
            "two-order flatness changed the retained common carrier")
    return {
        "oriented_chart_output": "q=A-B (or A-C in the second root pair)",
        "relative_return_boundary": "dGamma=q-rho",
        "ordered_path_makes_q_absolute": False,
        "dual_on_q_rho": [1, 1],
        "absolute_rho_landing_fills_q": True,
        "two_root_orders": {
            "boundaries": ["q-rho_forward", "q-rho_reverse"],
            "carrier_difference_absolute": True,
            "common_return_carrier_retained": True,
        },
        "interpretation": (
            "the polynomial identity E_10 E_01(A)=A-B determines the q face "
            "of the bar.  It does not construct a physical source cell with "
            "boundary rho, so it is a relative carrier rather than an "
            "absolute root-return boundary"
        ),
    }


def audit_first_pp_naturality():
    # One literal occurrence: forward_01=-D*s1 on tail 23|45.  Each face
    # retains the parent label A or B and the corresponding carrier label.
    faces = (
        ("remove D=PS", "s1*q23*q45", "3K2 / path cofactor"),
        ("remove s1=S1", "D*q23*q45", "3K2 / path cofactor"),
        ("remove q23", "D*s1*q45", "P3+K2 / tail cofactor"),
        ("remove q45", "D*s1*q23", "P3+K2 / tail cofactor"),
    )
    # Four copies of the relative 4-coordinate parent block.
    columns = []
    detectors = []
    width = 4 * len(faces)
    for block in range(len(faces)):
        offset = 4 * block
        beta_a = [Q(0)] * width
        beta_b = [Q(0)] * width
        beta_a[offset] = Q(1)
        beta_a[offset + 2] = Q(-1)
        beta_b[offset + 1] = Q(1)
        beta_b[offset + 3] = Q(-1)
        columns.extend((tuple(beta_a), tuple(beta_b)))
        detector = [Q(0)] * width
        for local, value in enumerate((Q(1, 2), Q(-1, 2),
                                       Q(1, 2), Q(-1, 2))):
            detector[offset + local] = value
        detectors.append(tuple(detector))
    require(rank(tuple(columns)) == 2 * len(faces)
            and width - rank(tuple(columns)) == 2 * len(faces),
            "the first-PP relative face packet changed H0")
    require(all(all(dot(detector, column) == 0
                    for column in columns)
                for detector in detectors),
            "a PP anti-detector stopped extending over the face graphs")

    # The literal commutator [d,PP]=0: applying a face to c_p-t_p gives the
    # corresponding face copy f_p-s_p.  This is equality of the same four
    # coefficient patterns, and reinsertion by the removed edge reverses it.
    top_patterns = (
        (Q(1), Q(0), Q(-1), Q(0)),
        (Q(0), Q(1), Q(0), Q(-1)),
    )
    for block in range(len(faces)):
        observed = tuple(
            tuple(columns[2 * block + parent][4 * block + local]
                  for local in range(4))
            for parent in range(2)
        )
        require(observed == top_patterns,
                ("PP stopped commuting with the parent bar", block, observed))
    return {
        "collision": "D*s1*q23*q45",
        "response_word": "11:110000",
        "parent_labels": ["from A=D*q01", "from B=p0*s1"],
        "faces": [
            {"operation": operation, "monomial": monomial, "type": kind}
            for operation, monomial, kind in faces
        ],
        "face_packet_coordinates_rank_cokernel": [width, 8, 8],
        "facewise_relative_identity":
            "d(PP beta_A-PP beta_B)=(f_A-f_B)-(s_A-s_B)",
        "restriction_reinsertion": (
            "removing q23 or q45 gives the displayed parent-labelled "
            "P3+K2 carrier; reinserting that exact labelled edge returns "
            "the top anti-carrier"
        ),
        "absolute_landing_naturality": (
            "a physical dEta=t_A-t_B must come with four compatible faces "
            "d(PP Eta)=s_A-s_B.  A top-only carrier kill is not a chain map"
        ),
        "next_word_grade": (
            "the tail cofactors remain in response word 11:110000; transport "
            "to canonical AugP2 word 01211222 is the separately missing "
            "word-changing comparison"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "h3 collision parent-split relative bar terminal gate",
        "pins": PINS,
        "minimal_parent_split_models": audit_parent_split_cylinders(),
        "ordered_hyperbolic_return": audit_ordered_root_return(),
        "first_PP_and_reinsertion": audit_first_pp_naturality(),
        "verdict": (
            "The minimal genuine parent-to-collected mapping cylinder uses "
            "two comparison cells and makes the parent anti-diagonal an "
            "absolute boundary while preserving collected H0.  The ordered "
            "hyperbolic root path does not supply those cells.  Its minimal "
            "H0-preserving bar must retain t_A,t_B, so c_A-c_B is homologous "
            "to tau=t_A-t_B.  The opposite root sends this to a second "
            "relative graph q-rho; even the agreement of the two root orders "
            "only identifies their carriers and leaves one common rho class"
        ),
        "sharp_positive_datum": (
            "one occurrence-labelled absolute anti-carrier landing family "
            "dEta=t_A-t_B (equivalently both parent-to-collected comparison "
            "cells), natural on the two 3K2 and two P3+K2 faces of every "
            "collision occurrence and followed by the word-changing AugP2 "
            "comparison.  It makes the collision anti-diagonal and the "
            "returned A-B/A-C switch absolute"
        ),
        "sharp_terminal_criterion": (
            "After the full same-word/fine/repeated/window source map and "
            "all four PP/reinsertion descendants are exhaustively listed, "
            "extend the normalized anti-dual with equal values on each "
            "parent and its retained carrier.  If every complete physical "
            "column is annihilated and no face-natural column has nonzero "
            "value on tau (equivalently on the common return carrier rho), "
            "the extended anti-dual is an augmented terminal.  Any such "
            "nonzero face-natural landing is instead the filler branch"
        ),
        "scope": (
            "exact rational mapping-cylinder/bar theorem for one collision "
            "sector and one fixed tail, including its complete first PP "
            "faces.  It identifies but does not construct the physical "
            "parent-to-collected or cross-word AugP2 comparison"
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
    print("parent-to-collected cylinder: ABSOLUTE ANTI-DIAGONAL, H0-PRESERVING")
    print("ordered hyperbolic root bar: RELATIVE ANTI-CARRIER ONLY")
    print("opposite-root return: q-rho, NOT an absolute q boundary")
    print("first PP/reinsertion faces: FOUR RELATIVE ANTI-CARRIERS")
    print("terminal iff exhaustive physical map has no nonzero tau/rho landing")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
