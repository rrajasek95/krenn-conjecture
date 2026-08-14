#!/usr/bin/env python3
"""Audit the fixed-face shortcut for the Gate-II relative-C4 remainder.

The switch-Weyl product leaves, on the fixed tail window 2345, the three
literal Hasse[2] direction packets

    -2 d(D Q01) H + d(P0 S1) H + d(P1 S0) H,

where H is the symmetric three-matching C4 tail.  At a fixed complex source
each scalar partner of a differentiated direction is either zero (so that
face vanishes) or a field unit.  This really removes the coefficient-core
colon obstruction on that face.

It does not construct the selected relative-C4 source column.  The checker
gives the minimal presentation-safe relative DGA dU=H-r, totalizes the two
Leibniz arrows in each Hasse[2] block, and records the exported retained
faces d(xy)r.  It then verifies an exact complete-row counterguard: after
arbitrary nonzero scalar normalization, a centered K2,2 companion component
still has no projector onto its selected common C4 core.  Thus scalar
localization and literal label placement do not imply physical source
projection.  No full physical K2,2 realization is asserted.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_gate_ii_switch_weyl_product_rule_idempotent_gate.py":
        "fbd4815eb5c6d46b8dbcd018f6e75237f004e3f52b1ccf47631479b698f9db35",
    "computations/verify_uniform_chart_cross_companion_relative_switch_dga_gate.py":
        "e0a8251128174d50b450b3bf85ce0a6870af00d4ab5565e7849fc3c8644c31c6",
    "computations/verify_h3_gate_ii_uniform_response_relative_carrier_landing_gate.py":
        "9b9c05a6789d2ade9359934f279eeb429591b2e85651ebaba8485195050417eb",
    "computations/verify_h3_generic_symmetric_c4_core_saturation_tor_gate.py":
        "7307cb245996376f9847ff4852a4fdcd0a774152b4011ed92822022f93af03e5",
    "computations/verify_uniform_recurrent_core_complete_row_projection_boundary.py":
        "3dc0ee0a0fbb7f0c1c1ea779bd6f3ee54114fece4f00a70877df8b2904cada2d",
}
EXPECTED_LEDGER_SHA256 = (
    "e62422ac6e684636a46f4d011062bd9d1e5120d0d97f540ec7cd1719eaecd592"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((vector[index] for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * value for value in vector)


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
            if row == answer or rows[row][column] == 0:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def in_span(columns: tuple[tuple[Q, ...], ...], vector: tuple[Q, ...]) -> bool:
    return rank(columns) == rank(columns + (vector,))


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def switch_graph_h0_audit() -> dict[str, object]:
    # Coordinates: uA,uB,uC,zA,zB,zC,tB,tC.  Columns are
    # dtheta_i=z_i-u_i and dphi_B=tB-(zB-zA), dphi_C=tC-(zC-zA).
    theta_a = (Q(-1), Q(0), Q(0), Q(1), Q(0), Q(0), Q(0), Q(0))
    theta_b = (Q(0), Q(-1), Q(0), Q(0), Q(1), Q(0), Q(0), Q(0))
    theta_c = (Q(0), Q(0), Q(-1), Q(0), Q(0), Q(1), Q(0), Q(0))
    phi_b = (Q(0), Q(0), Q(0), Q(1), Q(-1), Q(0), Q(1), Q(0))
    phi_c = (Q(0), Q(0), Q(0), Q(1), Q(0), Q(-1), Q(0), Q(1))
    columns = (theta_a, theta_b, theta_c, phi_b, phi_c)
    require(rank(columns) == 5 and 8 - rank(columns) == 3,
            "the presentation-safe switch graph changed H0")

    # d(G_B+G_C)=T+L with T=tB+tC and L=2uA-uB-uC.
    graph_sum = add(theta_b, scale(-1, theta_a), phi_b,
                    theta_c, scale(-1, theta_a), phi_c)
    t_plus_l = (Q(2), Q(-1), Q(-1), Q(0), Q(0), Q(0), Q(1), Q(1))
    require(graph_sum == t_plus_l,
            ("the T+L switch identity changed", graph_sum, t_plus_l))
    return {
        "degree_zero_coordinates": 8,
        "monic_graph_columns": 5,
        "H0_dimension": 3,
        "identity": "d(G_B+G_C)=tB+tC+L01",
        "consequence": (
            "the switch graph retains T=tB+tC; it does not set L01 or T "
            "to zero"
        ),
    }


def fixed_c4_and_scalar_audit() -> dict[str, object]:
    symmetric = (Q(1), Q(1), Q(1))
    epsilon = (Q(1, 3), Q(1, 3), Q(1, 3))
    differences = ((Q(1), Q(-1), Q(0)),
                   (Q(0), Q(1), Q(-1)))
    require(dot(epsilon, symmetric) == 1
            and all(dot(epsilon, value) == 0 for value in differences)
            and rank(differences + (symmetric,)) == 3,
            "the fixed C4 invariant/standard split changed")
    for permutation in permutations(range(3)):
        require(tuple(symmetric[index] for index in permutation) == symmetric,
                "the C4 tail stopped being covariant")

    packets = (
        ("Hasse[2](D,Q01)", Q(-2), "dD", "q01", "D", "dq01"),
        ("Hasse[2](P0,S1)", Q(1), "dp0", "s1", "p0", "ds1"),
        ("Hasse[2](P1,S0)", Q(1), "dp1", "s0", "p1", "ds0"),
    )
    require(sum(2 * len(symmetric) for _packet in packets) == 18,
            "the direction-face census changed")

    # At a fixed complex point, each of the six scalar partners is either
    # zero or invertible.  Enumerate every vanishing pattern: a zero partner
    # removes its three matching terms; a nonzero partner permits scalar
    # normalization.  This is a facewise statement and does not assert a
    # selected source preimage.
    patterns = []
    for mask in product((0, 1), repeat=6):
        active = sum(mask)
        patterns.append((active, 3 * active, 3 * (6 - active)))
    require(len(patterns) == 64
            and all(active_terms + vanished_terms == 18
                    for _active, active_terms, vanished_terms in patterns),
            "the scalar zero/unit dichotomy changed")

    # Conditional 4e2ff27 formula: if the three same-grade source rows
    # a*s,a*d01,a*d12 exist and a is a unit, they isolate all occurrences.
    a = Q(2)
    s, d01, d12 = symmetric, differences[0], differences[1]
    normalized = tuple(scale(Q(1, 2), scale(a, value))
                       for value in (s, d01, d12))
    isolated = (
        scale(Q(1, 3), add(normalized[0], scale(2, normalized[1]),
                           normalized[2])),
        scale(Q(1, 3), add(normalized[0], scale(-1, normalized[1]),
                           normalized[2])),
        scale(Q(1, 3), add(normalized[0], scale(-1, normalized[1]),
                           scale(-2, normalized[2]))),
    )
    require(isolated == ((Q(1), Q(0), Q(0)),
                         (Q(0), Q(1), Q(0)),
                         (Q(0), Q(0), Q(1))),
            "the conditional full-core unit construction changed")
    return {
        "fixed_window": [2, 3, 4, 5],
        "tail_occurrences": ["23|45", "24|35", "25|34"],
        "tail_vector": [1, 1, 1],
        "primitive_average_dual": ["1/3", "1/3", "1/3"],
        "literal_packets": [
            {
                "grade": packet[0],
                "chart_coefficient": str(packet[1]),
                "arrows": [f"{packet[2]}*{packet[3]}",
                           f"{packet[4]}*{packet[5]}"],
                "matching_terms": 6,
            }
            for packet in packets
        ],
        "direction_terms": 18,
        "fixed_point_scalar_dichotomy": (
            "partner=0 makes that three-term face zero; partner!=0 is a "
            "complex unit and removes the scalar-core colon on that face"
        ),
        "vanishing_patterns_checked": len(patterns),
        "conditional_unit_formula": (
            "if selected source rows a*s,a*d01,a*d12 already exist, "
            "a^{-1} and the 1/3 formulas isolate m0,m1,m2"
        ),
        "conditional_formula_verified": True,
    }


def relative_c4_dga_audit() -> dict[str, object]:
    # For one Hasse[2] pair x,y use dx=x', dy=y', dx'=dy'=0.  Let H be the
    # closed symmetric C4 tail.  The minimal presentation-safe attachment is
    # dU=H-r with r closed and retained.  Coordinate order below is
    # (x'y H, x y' H, x'y r, x y' r, x'y'U).
    #
    # K1=-x'yU and K2=-xy'U.  The two mixed x'y'U faces cancel exactly:
    # dK1=x'y(H-r)+x'y'U, dK2=xy'(H-r)-x'y'U.
    d_k1 = (Q(1), Q(0), Q(-1), Q(0), Q(1))
    d_k2 = (Q(0), Q(1), Q(0), Q(-1), Q(-1))
    total = add(d_k1, d_k2)
    require(total == (Q(1), Q(1), Q(-1), Q(-1), Q(0)),
            ("the two-arrow relative totalization changed", total))

    # One old H coordinate becomes (H,r) modulo the monic graph r-H.  H0 is
    # one-dimensional before and after.  Repeat independently in the three
    # central Hasse blocks.
    old_h0 = 3
    relative_boundaries = (
        (Q(-1), Q(0), Q(0), Q(1), Q(0), Q(0)),
        (Q(0), Q(-1), Q(0), Q(0), Q(1), Q(0)),
        (Q(0), Q(0), Q(-1), Q(0), Q(0), Q(1)),
    )
    new_h0 = 6 - rank(relative_boundaries)
    require((old_h0, new_h0) == (3, 3),
            "the relative C4 attachment changed H0")

    chart_coefficients = (Q(-2), Q(1), Q(1))
    block_total = tuple(scale(coefficient, total)
                        for coefficient in chart_coefficients)
    require(all(vector[-1] == 0 for vector in block_total),
            "a mixed reinsertion face survived the paired totalization")
    return {
        "relative_attachment": "dU_j=H_2345-r_j, dr_j=0",
        "blocks": [
            "Hasse[2](D,Q01)",
            "Hasse[2](P0,S1)",
            "Hasse[2](P1,S0)",
        ],
        "lift_in_each_block": "K_j=-d(x_j*y_j)*U_j",
        "exact_boundary": "dK_j=d(x_j*y_j)*(H_2345-r_j)",
        "mixed_face_cancellation": (
            "d(-x'_j*y_j*U_j) and d(-x_j*y'_j*U_j) have opposite "
            "x'_j*y'_j*U_j faces"
        ),
        "H0_old_relative": [old_h0, new_h0],
        "first_exported_faces": [
            "-2*((dD)*q01+D*(dq01))*r_DQ",
            "((dp0)*s1+p0*(ds1))*r_PS01",
            "((dp1)*s0+p1*(ds0))*r_PS10",
        ],
        "absolute_closure_needed": (
            "a physical column landing each retained r_j (or one covariant "
            "combined landing); setting r_j=0 is not presentation-safe"
        ),
    }


def selected_projection_counterguard() -> dict[str, object]:
    # Coordinates C,z00,z01,z10,z11.  These are normalized complete rows in
    # one fixed Hasse block and fixed four-site window.  Every companion is
    # paired.  The centered affine detector survives all nonzero scalar
    # normalizations and reads one on the selected common core C.
    f_a0 = (Q(1), Q(1), Q(1), Q(0), Q(0))
    f_a1 = (Q(1), Q(0), Q(0), Q(1), Q(1))
    f_b0 = (Q(1), Q(1), Q(0), Q(1), Q(0))
    f_b1 = (Q(1), Q(0), Q(1), Q(0), Q(1))
    rows = (f_a0, f_a1, f_b0, f_b1)
    core = (Q(1), Q(0), Q(0), Q(0), Q(0))
    detector = (Q(1), Q(-1, 2), Q(-1, 2), Q(-1, 2), Q(-1, 2))
    relation = add(f_a0, f_a1, scale(-1, f_b0), scale(-1, f_b1))
    require(relation == (Q(0),) * 5
            and rank(rows) == 3
            and not in_span(rows, core)
            and rank(rows + (core,)) == 4
            and all(dot(detector, row) == 0 for row in rows)
            and dot(detector, core) == 1,
            "the selected-core K2,2 counterguard changed")

    for scalar in (Q(-3), Q(-1), Q(1, 2), Q(1), Q(5)):
        scaled_rows = tuple(scale(scalar, row) for row in rows)
        scaled_core = scale(scalar, core)
        require(rank(scaled_rows) == rank(rows)
                and not in_span(scaled_rows, scaled_core)
                and all(dot(detector, row) == 0 for row in scaled_rows)
                and dot(detector, scaled_core) == scalar,
                ("scalar localization changed selected projection", scalar))

    # The direct-chart covector is the smaller actual Gate-II shadow:
    # endpoint charts B,C span rank two; A, hence R=A+B+C and L=2A-B-C,
    # adds an independent direction.  Nonzero rescaling does not change it.
    a = (Q(1), Q(0), Q(0))
    b = (Q(0), Q(1), Q(0))
    c = (Q(0), Q(0), Q(1))
    direct = (Q(1), Q(0), Q(0))
    r = add(a, b, c)
    l = add(scale(2, a), scale(-1, b), scale(-1, c))
    require(rank((b, c)) == 2
            and rank((b, c, r)) == rank((b, c, l)) == 3
            and tuple(dot(direct, vector) for vector in (b, c, r, l))
            == (Q(0), Q(0), Q(1), Q(2)),
            "the direct-chart selected-block detector changed")
    return {
        "normalized_complete_rows": [
            "F_A0=C+z00+z01",
            "F_A1=C+z10+z11",
            "F_B0=C+z00+z10",
            "F_B1=C+z01+z11",
        ],
        "centered_relation": "F_A0+F_A1-F_B0-F_B1=0",
        "normalized_detector": ["1", "-1/2", "-1/2", "-1/2", "-1/2"],
        "detector_on_rows_core": [0, 1],
        "rank_rows_after_core": [3, 4],
        "nonzero_scalar_normalizations_checked": 5,
        "direct_chart_detector_B_C_R_L": [0, 0, 1, 2],
        "sharp_consequence": (
            "inverting q01,D,p_i,or s_i normalizes coefficients but cannot "
            "delete complete-row companions or turn the selected codomain "
            "face supplied by T*H_W into a physical repair preimage"
        ),
        "scope": (
            "exact complete-row implication counterguard plus the actual "
            "three-chart rank shadow; the abstract K2,2 is not asserted to "
            "be a complete ternary decorated hafnian source component"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 Gate-II fixed-face relative-C4 localization/projection gate",
        "pins": PINS,
        "presentation_safe_switch_graph": switch_graph_h0_audit(),
        "fixed_C4_scalar_unit_split": fixed_c4_and_scalar_audit(),
        "minimal_relative_DGA": relative_c4_dga_audit(),
        "selected_projection_counterguard": selected_projection_counterguard(),
        "verdict": (
            "At a fixed complex source the partner coefficient on every one "
            "of the eighteen DQ/PS direction faces is zero or a field unit, "
            "so the coefficient-core colon disappears facewise.  The minimal "
            "relative attachment dU=H-r is literal, tail-covariant, PP-"
            "compatible and H0-preserving, and it exports exactly d(xy)r.  "
            "Neither scalar normalization nor the T*H_W label placement "
            "constructs the required physical landing of r: selected "
            "complete-row projection is an independent affine problem, with "
            "the centered K2,2 dual as the smallest face-complete guard."
        ),
        "shortest_positive_datum": (
            "one source-labelled column in each fixed DQ/PS block (or one "
            "covariant combined column) whose boundary has nonzero retained "
            "r_j component after all complete companion occurrences are kept"
        ),
        "nonclaims": [
            "the switch-Weyl face is not confused with a second repair preimage",
            "pointwise scalar inversion is not called selected occurrence projection",
            "the relative carrier graph is not called an absolute filler",
            "the K2,2 guard is not called a realized full GHZ source packet",
        ],
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
    print("fixed-face scalar zero/unit split: EXACT")
    print("minimal relative C4 DGA: EXPLICIT, H0 UNCHANGED")
    print("two DQ/PS arrows: TOTALIZED; retained r-faces EXPORTED")
    print("selected complete-row projection: INDEPENDENT / NOT CONSTRUCTED")
    print("smallest face-complete guard: CENTERED K2,2")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
