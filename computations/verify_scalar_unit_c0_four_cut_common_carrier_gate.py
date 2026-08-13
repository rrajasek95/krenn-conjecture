#!/usr/bin/env python3
"""Audit physical c0 descent from the two oriented four-cut carriers.

The two oriented curvature factors sum to 2q-r.  If both annihilate one
common carrier H0, their sum gives c0=(r-2q)H0=0.  Literal four-cut rows
instead live on two restricted carriers.  This checker records the exact
mismatch identity and the finite common-lift membership/dual alternative.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/scalar-unit-full-normal-jet-unary-anchor-ledger.md":
        "a40064cfba52c4df551bf6ed0aec989cd926c50855cfc59c2be617f8eda5607d",
    "computations/verify_scalar_unit_full_normal_jet_unary_anchor_ledger.py":
        "f9debc5f966a218fee0f94b7bf710dbdfd3aa3c7796f61ffaed0b70c0a1360e4",
    "notes/scalar-unit-carrier-torsion-obstruction.md":
        "99a3a3f935db47e9f7925c1ffa08934ec8f5cabeb67f26c1553abbdda8213061",
    "computations/verify_scalar_unit_carrier_torsion_obstruction.py":
        "4c175a1193c5dae370696b7120976ade2ab8c32338a51d05a2e60dc60e460e94",
    "notes/scalar-unit-complementary-pivot-essential-pair.md":
        "afff30038185cbad082281e67edc6f59e5b3fcb8af3f3c28d303bff6d4871d18",
    "computations/verify_scalar_unit_complementary_pivot_essential_pair.py":
        "de5c55404793af69ddc96c5366a2c0898ead18fe33dbe34ac22ab853d53aad63",
    "notes/scalar-unit-catalecticant-four-cut-localization.md":
        "2a47fa0daa238db400e94981a11c2d350281ce1536abc13b091e4838c7cc6600",
    "computations/verify_scalar_unit_catalecticant_four_cut_localization.py":
        "20fb784b756d7e91bb0da7f76a37571e06ae223247967ea34dcd3724a2332ecd",
    "notes/scalar-unit-moment-transgression-source-lift-based-loop-torsor.md":
        "8df4b715775194282542cf1ea057b8305223744504687e5e480c4c262fcecd4a",
    "computations/verify_scalar_unit_moment_transgression_source_lift_based_loop_torsor.py":
        "4bff53e1568a74cfe262fac185558aa14337fe1a2e31e6c46141645e78e8e839",
    "notes/uniform-hasse-moment-augmented-membership-gate.md":
        "2b111d884b3cb8ad332cbdaf8b96b3a8d442517e20171bbad7ad4cfe542f054f",
    "computations/verify_uniform_hasse_moment_augmented_membership_gate.py":
        "f5f663715507d46e6d96b37a1a05c21e9f0b045dcedd878bf657dfb4b32091c3",
    "notes/h3-centered-endpoint-projector-primitive-cap-lift-gate.md":
        "48e39dd9e2667208eb2a08d98aa5dc58151daeaa7029437270d92a966c9e2542",
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
}
EXPECTED_LEDGER_SHA256 = (
    "497cf2cd836e1f3e51d318daa672eecaf8c30cec5c4f9788fb68b720831ff2e3"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def matrix_rank(columns: list[list[Fraction]]) -> int:
    require(columns, "empty rank matrix")
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [list(entries) for entries in zip(*columns, strict=True)]
    row_count = len(rows)
    column_count = len(columns)
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [entry / pivot_value for entry in rows[rank]]
        for row in range(row_count):
            if row == rank or not rows[row][column]:
                continue
            coefficient = rows[row][column]
            rows[row] = [
                entry - coefficient * pivot_entry
                for entry, pivot_entry in zip(
                    rows[row], rows[rank], strict=True
                )
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def orientation_audit() -> dict[str, object]:
    # Basis q,r,x for K_right=q-x and K_left=q-r+x.
    right = [Fraction(1), Fraction(0), Fraction(-1)]
    left = [Fraction(1), Fraction(-1), Fraction(1)]
    summed = [a + b for a, b in zip(right, left, strict=True)]
    require(summed == [Fraction(2), Fraction(-1), Fraction(0)],
            "oriented curvature sum changed")
    carrier_factor = [-entry for entry in summed]
    require(carrier_factor == [Fraction(-2), Fraction(1), Fraction(0)],
            "c0 carrier factor changed")

    # Exact mismatch identity under two restricted annihilations.
    samples = [
        # q, r, x, H
        (Fraction(3), Fraction(5), Fraction(1), Fraction(7)),
        (Fraction(2), Fraction(7), Fraction(-1), Fraction(5)),
        (Fraction(5), Fraction(4), Fraction(2), Fraction(-3)),
    ]
    records = []
    for q, r, x, h_zero in samples:
        k_right = q - x
        k_left = q - r + x
        require(k_right and k_left, "degenerate test curvature")
        # h_or=H+delta_or and k_or*h_or=0.
        delta_right = -h_zero
        delta_left = -h_zero
        require(k_right * (h_zero + delta_right) == 0
                and k_left * (h_zero + delta_left) == 0,
                "restricted row did not annihilate")
        c_zero = (r - 2 * q) * h_zero
        mismatch = k_right * delta_right + k_left * delta_left
        require(c_zero == mismatch, "carrier mismatch identity changed")
        records.append({
            "q": str(q), "r": str(r), "x": str(x), "H0": str(h_zero),
            "c0": str(c_zero), "mismatch": str(mismatch),
        })
    return {
        "K_right_basis_qrx": [str(entry) for entry in right],
        "K_left_basis_qrx": [str(entry) for entry in left],
        "K_right_plus_K_left": "2q-r",
        "common_carrier_consequence": "(r-2q)H0=0",
        "restricted_carrier_identity": (
            "c0=K_right*delta_right+K_left*delta_left"
        ),
        "samples": records,
    }


def common_lift_and_dual_audit() -> dict[str, object]:
    # Two two-dimensional restrictions.  The common restriction map is the
    # diagonal P -> P_right direct_sum P_left.
    diagonal = [
        [Fraction(1), Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0), Fraction(1)],
    ]
    common_pair = [Fraction(1), Fraction(0), Fraction(1), Fraction(0)]
    mismatch_pair = [Fraction(1), Fraction(0), Fraction(1), Fraction(1)]
    require(matrix_rank(diagonal) == matrix_rank(diagonal + [common_pair]),
            "common pair failed to descend")
    require(matrix_rank(diagonal) + 1
            == matrix_rank(diagonal + [mismatch_pair]),
            "mismatched pair unexpectedly descended")

    # lambda=(0,-1;0,+1) kills every diagonal common restriction and detects
    # the private left carrier component.
    separator = [Fraction(0), Fraction(-1), Fraction(0), Fraction(1)]
    require(all(dot(separator, column) == 0 for column in diagonal),
            "mismatch separator sees common carrier")
    require(dot(separator, mismatch_pair) == 1,
            "mismatch separator lost the private carrier")
    require(dot(separator, common_pair) == 0,
            "mismatch separator sees a descended pair")

    # A zero-shadow correction in the private left component repairs this
    # toy mismatch.  In the physical test such columns must be sourced.
    correction = [Fraction(0), Fraction(0), Fraction(0), Fraction(1)]
    require(matrix_rank(diagonal + [correction])
            == matrix_rank(diagonal + [correction, mismatch_pair]),
            "zero-shadow correction did not repair mismatch")
    return {
        "common_restriction_columns": [
            [str(entry) for entry in column] for column in diagonal
        ],
        "mismatch_pair": [str(entry) for entry in mismatch_pair],
        "mismatch_dual": [str(entry) for entry in separator],
        "dual_value": str(dot(separator, mismatch_pair)),
        "finite_criterion": (
            "rank([B_common C_phys])=rank([B_common C_phys | "
            "(H_right,H_left)])"
        ),
        "scope": (
            "the dual is physical only when B_common and C_phys are the "
            "complete source-valid augmented maps"
        ),
    }


def source_scope_audit() -> dict[str, object]:
    normal = (ROOT / "notes/scalar-unit-full-normal-jet-unary-anchor-ledger.md").read_text()
    torsion = (ROOT / "notes/scalar-unit-carrier-torsion-obstruction.md").read_text()
    pivot = (ROOT / "notes/scalar-unit-complementary-pivot-essential-pair.md").read_text()
    localization = (ROOT / "notes/scalar-unit-catalecticant-four-cut-localization.md").read_text()
    loops = (ROOT / "notes/scalar-unit-moment-transgression-source-lift-based-loop-torsor.md").read_text()
    projector = (ROOT / "notes/h3-centered-endpoint-projector-primitive-cap-lift-gate.md").read_text()
    require(r"\boxed{\Theta_a=R_{aa}H_a" in normal
            and r"\Theta_a\ne0" in normal,
            "normal-jet active carrier changed")
    require("both complete oriented quadratic forms annihilate the same complete" in torsion
            and "Actual four-cut layers are weaker" in torsion,
            "oriented common-carrier scope changed")
    require("literal nonzero" in pivot
            and "physical oriented four-cut carrier layer" in pivot,
            "essential-pair active restricted carrier changed")
    require("need not survive in\nthe full normal-jet carrier" in localization
            and "\\kappa_e^\\rightarrow\\nu(efH_0)=0" in localization,
            "localized carrier cancellation guard changed")
    require("common carrier needs a chain-level base-change square" in loops.lower()
            and "No current endpoint row provides that square" in loops,
            "based-loop common-carrier frontier changed")
    require("surviving `H_0` base class" in projector
            and "one primitive reduced companion" in projector
            and "No such cell is in the current inventory" in projector,
            "centered endpoint-projector cap frontier changed")
    return {
        "actual_clean_packet": "Theta=r*H0 is nonzero",
        "strongest_positive_four_cut": (
            "on the essential 2-by-2 packet one orientation has a literal "
            "nonzero restricted curvature-carrier coefficient"
        ),
        "strongest_negative_guard": (
            "a nonzero leading adjacent-q coefficient can cancel after "
            "replacement by the full H0 carrier"
        ),
        "missing_map": (
            "one all-label restriction-insertion/base-change comparison "
            "for both orientations, before evaluation"
        ),
        "conditional_alternative": (
            "common lift plus both oriented annihilations gives c0=0; "
            "a transported nonzero essential-pair coefficient gives an "
            "active clean line; failure of common lift leaves the finite "
            "carrier-mismatch dual"
        ),
        "centered_endpoint_projector_unification": (
            "conditional: a source-valid primitive cap/centered-occurrence "
            "lift whose two orientation projections are K_right*H0 and "
            "K_left*H0 gives active-clean if either is nonzero, and c0=0 "
            "if both vanish"
        ),
        "c1_scope": (
            "not a proved face of the current endpoint projector; c1 is "
            "the first t-weighted moment of a polynomial horizontal "
            "one-form, while the committed projector supplies only the "
            "unweighted H0 base augmentation"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "scalar-unit c0 four-cut common-carrier gate",
        "pins": PINS,
        "scope": source_scope_audit(),
        "orientation": orientation_audit(),
        "common_lift": common_lift_and_dual_audit(),
        "verdict": (
            "The two oriented curvature factors give c0 only after their "
            "restricted carriers descend from one common augmented H0. "
            "The strongest actual four-cut results do not supply that "
            "base-change square: one detects a nonzero restricted carrier, "
            "and another exact packet shows that it can cancel on full H0. "
            "Failure is a finite common-lift membership defect with an "
            "explicit cokernel dual; it is a physical separator only after "
            "the complete protected/terminal/q source maps are included."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("c0 common-carrier ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("common carrier + two oriented annihilations => c0=0")
    print("actual two restricted carriers: NOT YET COMPARED")
    print("finite carrier-mismatch dual: SURVIVES")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
