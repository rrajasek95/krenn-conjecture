#!/usr/bin/env python3
"""Affine correction and the smallest pointed-P_f coloop-pivot obstruction.

On the dehomogenized chart u=1 one has du=0, so the centered conormal is
exactly gamma=90 P_f-B.  Thus it creates no new relative cotangent class
after the pointed and complete graph normals exist.

The complete coloop pivot still does not construct P_f: it controls only
the aggregate U or V.  Two literal occurrences in either aggregate admit an
internal redistribution tangent which annihilates the coloop target, pure
and mixed complete rows, aggregate decomposition and affine normalization,
but evaluates nontrivially on the selected occurrence conormal.
"""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_centered_pointed_face_existing_conormal_cap_terminal_gate.py":
        "dabaf6c5132f835c6d681d1ecb30611eae8b0920b2c97272e487bcb9c9f068c9",
    "notes/h3-centered-pointed-face-existing-conormal-cap-terminal-gate.md":
        "9f41f22cc232beefca120c770c5815faa2aff0b80c738069cfd18a5c3557fa17",
    "computations/verify_h3_active_fan_coloop_complete_row_pivot.py":
        "d62fd630abac6e4d25bd6ffb0c1a2070311ec1c5d3c7764f56793283f78aa94a",
    "notes/h3-active-fan-coloop-complete-row-pivot.md":
        "2a68b7a9da9c61c67c4f63e666a6cbb1023344722943b9042f2ff15b2863e92e",
    "computations/verify_h3_trapped_carrier_actual_endpoint_map_boundary.py":
        "1735de099eeaec04a2197c613350fba4bd52d8955873c8a032894d8653087a0a",
    "notes/h3-trapped-carrier-actual-endpoint-map-boundary.md":
        "e3c3096592a42452e42703ed0e5c1e68e62182a7ab36a9c8277ea89b925bcab1",
    "computations/verify_h3_cross_word_cap_central_attachment_first_face_gate.py":
        "6f1dc2d4baece91046f8834418a7ce7b2fa84a9a3f1acc867cdf33353a807eea",
    "notes/h3-cross-word-cap-central-attachment-first-face-gate.md":
        "79a9cfda1261163fd0039e2fed9d8bbe84218c04b3ca78096f7db8f238c79022",
}
EXPECTED_LEDGER_SHA256 = "14240acd4a635abaddfb19b2b2d8b7067faf444a67fdf29d25637dd792e0e8f6"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right):
    return sum((F(a)*F(b)
                for a, b in zip(left, right, strict=True)), F(0))


def rank(rows):
    rows = [list(map(F, row)) for row in rows]
    if not rows:
        return 0
    pivot_row = 0
    for column in range(len(rows[0])):
        pivot = next((index for index in range(pivot_row, len(rows))
                      if rows[index][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        value = rows[pivot_row][column]
        rows[pivot_row] = [entry/value for entry in rows[pivot_row]]
        for index in range(len(rows)):
            if index == pivot_row or not rows[index][column]:
                continue
            value = rows[index][column]
            rows[index] = [left-value*right for left, right in
                           zip(rows[index], rows[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def in_row_span(rows, target):
    return rank(tuple(rows)) == rank(tuple(rows)+(tuple(target),))


def affine_centered_conormal_audit():
    # Before dehomogenization use coordinates (dz_f,dZ,du).
    pointed_projective = (F(1), F(0), F(-1))
    complete_projective = (F(0), F(1), F(-1))
    centered_projective = (F(90), F(-1), F(0))
    anchor = (F(0), F(0), F(1))
    require(tuple(90*pointed_projective[i]-complete_projective[i]
                  + 89*anchor[i] for i in range(3))
            == centered_projective,
            "the projective centered decomposition changed")

    # On u=1, du=0 and relative cotangent coordinates are (dz_f,dZ).
    pointed = (F(1), F(0))
    complete = (F(0), F(1))
    centered = (F(90), F(-1))
    require(tuple(90*pointed[i]-complete[i] for i in range(2)) == centered
            and rank((pointed, complete))
            == rank((pointed, complete, centered)) == 2,
            "the affine centered conormal relation changed")
    forbidden_old_tangent = (F(1), F(1), F(1))
    require(dot(anchor, forbidden_old_tangent) == 1,
            "the old scale tangent unexpectedly preserves u=1")
    return {
        "projective_identity": "gamma=90*P_f-B+89*du",
        "affine_chart": "u=1, hence du=0",
        "relative_identity": "gamma=90*P_f-B",
        "relative_ranks": {"P_f_and_B": 2, "after_gamma": 2},
        "old_scale_tangent": (
            "(1,1,1) is not tangent to u=1 because it has du=1"
        ),
        "conclusion": (
            "the centered conormal adds no relative cotangent class once a "
            "physical pointed P_f comparison and complete graph normal B exist"
        ),
        "degree_zero_warning": (
            "this is a conormal/PP correction: before differentiation the "
            "centered function differs from 90(z_f-u)-(Z-u) by the fixed "
            "constant 89; it does not manufacture a selected occurrence"
        ),
    }


def pivot_rows(point, split):
    # Coordinates:
    # (dalpha, ddiagonal, dC, dCc, dU, dV, df, dg, du).
    alpha, diagonal, cofactor, coloop_cofactor, U, V, _f, _g, _u = point
    rows = [
        # d(alpha*Cc-u)=0
        (coloop_cofactor, 0, 0, alpha, 0, 0, 0, 0, -1),
        # d(diagonal*C+U-u)=0
        (0, cofactor, diagonal, 0, 1, 0, 0, 0, -1),
        # d(alpha*C+V)=0
        (cofactor, 0, alpha, 0, 0, 1, 0, 0, 0),
        # affine normalization du=0
        (0, 0, 0, 0, 0, 0, 0, 0, 1),
    ]
    if split == "U":
        rows.append((0, 0, 0, 0, 1, 0, -1, -1, 0))
    elif split == "V":
        rows.append((0, 0, 0, 0, 0, 1, -1, -1, 0))
    else:
        raise RuntimeError(split)
    return tuple(tuple(map(F, row)) for row in rows)


def verify_point(point):
    alpha, diagonal, cofactor, coloop_cofactor, U, V, f, g, u = point
    require(alpha*coloop_cofactor == u
            and diagonal*cofactor+U == u
            and alpha*cofactor+V == 0,
            ("point is not on the complete coloop packet", point))
    return {
        "alpha*Cc-u": alpha*coloop_cofactor-u,
        "d*C+U-u": diagonal*cofactor+U-u,
        "alpha*C+V": alpha*cofactor+V,
        "U_or_V_split": f+g,
    }


def redistribution_guard(split):
    if split == "U":
        point = tuple(map(F, (1, 0, 0, 1, 1, 0,
                              F(1, 2), F(1, 2), 1)))
        require(point[6]+point[7] == point[4], point)
    else:
        point = tuple(map(F, (1, 1, 1, 1, 0, -1,
                              F(-1, 2), F(-1, 2), 1)))
        require(point[6]+point[7] == point[5], point)
    values = verify_point(point)
    rows = pivot_rows(point, split)
    tangent = tuple(map(F, (0, 0, 0, 0, 0, 0, 1, -1, 0)))
    pointed = tuple(map(F, (0, 0, 0, 0, 0, 0, 1, 0, -1)))
    require(all(dot(row, tangent) == 0 for row in rows)
            and dot(pointed, tangent) == 1
            and not in_row_span(rows, pointed),
            (split, rows, tangent, pointed))

    # The eliminated pivot is already in the row span.  At the chosen point
    # d(alpha U-d V-alpha u)=0 (where d denotes the diagonal cell).
    alpha, diagonal, _C, _Cc, U, V, _f, _g, u = point
    eliminated = (U-u, -V, 0, 0, alpha, -diagonal, 0, 0, -alpha)
    require(in_row_span(rows, eliminated)
            and dot(eliminated, tangent) == 0,
            ("the eliminated pivot changed", split, eliminated))
    return {
        "bright_aggregate": split,
        "point": [str(value) for value in point],
        "equation_values": {name: str(value)
                            for name, value in values.items()},
        "row_rank": rank(rows),
        "selected_P_f_in_row_span": False,
        "redistribution_tangent": [str(value) for value in tangent],
        "P_f_on_tangent": 1,
        "meaning": (
            "the complete pivot fixes the aggregate but cannot distinguish "
            "two literal occurrences inside it"
        ),
    }


def pointed_gate_audit():
    return {
        "U_bright_guard": redistribution_guard("U"),
        "V_bright_guard": redistribution_guard("V"),
        "general_obstruction": (
            "whenever the chosen nonzero aggregate contains two effective "
            "occurrences f,g, the tangent df=1,dg=-1 preserves U (or V), "
            "the coloop target, both complete rows and u=1, but reads one "
            "on P_f=df-du"
        ),
        "sharp_positive_cases": [
            "the pivot aggregate has a single effective occurrence",
            "an additional physical word/fine row separates the selected occurrence",
            "the full endpoint-plus-q map makes e_f^* a physical row-space selector",
        ],
        "smallest_missing_theorem": (
            "pointed occurrence isolation: in every trapped coloop packet, "
            "either select a singleton literal pivot term, obtain an anchor-"
            "safe redistribution dependence, or prove e_f^* lies in the row "
            "span of the complete physical endpoint-plus-q map; failure must "
            "extend to the accepted augmented terminal, not merely a protected selector"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "h3 affine centered conormal and pointed P_f coloop-pivot gate",
        "pins": PINS,
        "affine_centered_correction": affine_centered_conormal_audit(),
        "pointed_pivot_obstruction": pointed_gate_audit(),
        "corrected_frontier": {
            "retired": (
                "a separate centered conormal class after physical P_f and B"
            ),
            "still_open": (
                "construct the selected pointed P_f occurrence comparison "
                "inside the full trapped coloop packet"
            ),
            "first_later_face": (
                "after P_f is physical, matching incidence gives the selected "
                "db01 face; cross-word cap/central-Eq placement remains later"
            ),
        },
        "verdict": (
            "Affine normalization removes the 89du obstruction exactly: in "
            "the relative cotangent gamma=90P_f-B, so centeredness is not a "
            "new class after P_f exists.  The coloop pivot alpha U-dV=alpha "
            "does not itself construct P_f.  Its smallest exact U-bright and "
            "V-bright packets each have two literal occurrences and an "
            "internal redistribution tangent invisible to every pivot row "
            "and to du=0, but visible to P_f.  A singleton occurrence or an "
            "additional physical occurrence-separating row/full endpoint-q "
            "rank theorem is therefore necessary."
        ),
        "scope": (
            "canonical h=3 affine chart and the complete two-row coloop pivot; "
            "the counterguards prove nonimplication from that pivot, not "
            "nonexistence in the full physical endpoint-plus-q source map"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                (digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("affine du=0: gamma=90 P_f-B, NO NEW CENTERED CONORMAL")
    print("coloop pivot -> pointed P_f: FAILS ON TWO-OCCURRENCE REDISTRIBUTION")
    print("both U-bright and V-bright guards: EXACT")
    print("remaining: occurrence isolation in full endpoint-plus-q map")
    print("ledger_sha256="+digest)


if __name__ == "__main__":
    main()
