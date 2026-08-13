#!/usr/bin/env python3
"""Reconcile ordinary Segre Tate cells with the relative centered cell.

For the local 2x3 Segre occurrence algebra ``A=S/I``, the ordinary Tate
generators ``d e_ij=F_ij`` preserve ``H0=A``.  A chain derivation extending
the centered shear ``D0(u)=-L`` would force ``D0(F_ij)`` to be zero in A.
Instead

    D0(F_ij)=-L*k_ij

is generically nonzero.  Hence no connective DGA resolution with unchanged
H0 can carry an honest lift of this shear.

There are exactly two algebraic outcomes.  Adding ``d epsilon=L`` makes the
defect a boundary and permits the recursive Tate lift, but changes H0 to
``A/(L)``.  Alternatively introduce a target/output coordinate ``t`` and a
mapping cylinder

    d epsilon=L-t.

This retains ``H0=A`` by identifying ``t=L``.  Setting
``D(e_ij)=-epsilon*k_ij`` then leaves the exact curvature

    [d,D](e_ij)=t*k_ij.

It is not an honest DGA lift: it exports the obstruction as a target class.
The local ``k_ij`` span the endpoint-odd times matching-standard rank-two
module, annihilated by every endpoint-only or matching-only aggregate row.
Thus the current scalar response target/output does not supply its physical
word/fine/repeated-grade terminal.  Adjoining that mixed target module would
be precisely the new terminal alternative, not a hidden old source lift.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_physical_pp_hasse_toric_tate_cofibrancy_gate.py":
        "1fb82a919cbf70c5d3323d441c1a1feefd83361d70cc1cdc65e2d0f2c1eca0a9",
    "notes/h3-physical-pp-hasse-toric-tate-cofibrancy-gate.md":
        "ae52988050207d59a597d0e3852fe24f59c6cffdbcd2e0a5cebb7581a57ac867",
    "computations/verify_h3_centered_shear_relative_tate_completion_gate.py":
        "5137f0aa5fa062a8310064b7e655bc87dbe9d1d6ec71741ff2bc53b39f1b16f6",
    "notes/h3-centered-shear-relative-tate-completion-gate.md":
        "ffd8a9a888c768c2cbffa7f19988ff1eefd4bde2dcc5d13712a7a771a578c2b4",
    "computations/verify_h3_universal_response_ks_augmented_readout_extension_gate.py":
        "4493274dfbda62cec0d6823272762fb01c3a798123a1da206559e91890ba9047",
    "notes/h3-universal-response-ks-augmented-readout-extension-gate.md":
        "f201fd4c4599a27173a824d7475ade679ef2de55e7c91bc3dd9cc917ac16ee37",
    "computations/verify_h3_segre_bright_private_site_incidence_tate_alternative.py":
        "e00e9b39740c22b2beacd874e13ab3b7e7c2f776724e19eece28f525400d6258",
    "notes/h3-segre-bright-private-site-incidence-tate-alternative.md":
        "95a8ee1a7603cb5e5af20b44cdf7668a42b22fb020f042839a58e5a8329baa99",
}
EXPECTED_LEDGER_SHA256 = (
    "783b96dc336332e84ce8037213e157a04c385705de4f285ce3ffc4440fa0cfa9"
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
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank width")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        pivot_value = rows[answer][column]
        rows[answer] = [value / pivot_value for value in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            coefficient = rows[row][column]
            rows[row] = [left - coefficient * right
                         for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def segre_tate_lift_obstruction_audit() -> dict[str, object]:
    # Generic physical Segre point u_rj=e_r*q_j.
    e0, e1 = Q(1), Q(2)
    q0, q1, q2 = Q(1), Q(3), Q(5)
    u = (e0*q0, e0*q1, e0*q2, e1*q0, e1*q1, e1*q2)
    minors = (
        u[0]*u[4] - u[1]*u[3],
        u[0]*u[5] - u[2]*u[3],
        u[1]*u[5] - u[2]*u[4],
    )
    require(minors == (0, 0, 0),
            "the test point left the physical Segre algebra")
    gradients = (
        (u[4], -u[3], 0, -u[1], u[0], 0),
        (u[5], 0, -u[3], -u[2], 0, u[0]),
        (0, u[5], -u[4], 0, -u[2], u[1]),
    )
    constant_shear = (Q(1),) * 6
    k_values = tuple(dot(gradient, constant_shear)
                     for gradient in gradients)
    require(k_values == (2, 4, 2),
            ("the Segre conormal readings changed", k_values))

    # Evaluation at a physical point kills every member of I.  Since the
    # shear derivative has a nonzero value here for L!=0, it is not in I.
    L = Q(7)
    shear_derivatives = tuple(-L * value for value in k_values)
    require(any(shear_derivatives),
            "the centered shear unexpectedly became tangent")
    return {
        "ordinary_tate_cells": [
            "d e01=F01", "d e02=F02", "d e12=F12"
        ],
        "ordinary_tate_H0": "S/(F01,F02,F12)=A",
        "physical_test_point": {
            "e": [1, 2], "q": [1, 3, 5],
            "u": [str(value) for value in u],
        },
        "F_values": [str(value) for value in minors],
        "constant_shear_k_values": [str(value) for value in k_values],
        "selected_nonzero_L": str(L),
        "D0_F_values": [str(value) for value in shear_derivatives],
        "D0_I_subset_I": False,
        "honest_chain_derivation_on_any_H0_equal_A_resolution": False,
        "reason": (
            "an honest chain derivation descends to H0; the displayed "
            "physical evaluation kills I but not D0(F)"
        ),
    }


def h0_and_cylinder_sign_audit() -> dict[str, object]:
    # Freeze the signs at the generic point.  With d epsilon=L-t and
    # D(e)=-epsilon*k, dD(e)=-L*k+t*k while Dd(e)=-L*k.
    L = Q(7)
    target = Q(11)
    k_values = (Q(2), Q(4), Q(2))
    d_epsilon = L - target
    d_D_e = tuple(-d_epsilon * value for value in k_values)
    D_d_e = tuple(-L * value for value in k_values)
    commutator = tuple(left - right
                       for left, right in zip(d_D_e, D_d_e, strict=True))
    target_curvature = tuple(target * value for value in k_values)
    require(commutator == target_curvature
            and any(target_curvature),
            ("the target-cylinder curvature sign changed",
             commutator, target_curvature))

    return {
        "ordinary_source_resolution": {
            "d_epsilon": None,
            "H0": "A",
            "honest_centered_shear_lift": False,
        },
        "relative_source_Koszul": {
            "d_epsilon": "L",
            "H0": "A/(L)",
            "honest_recursive_shear_lift": True,
            "preserves_original_H0": False,
        },
        "target_output_mapping_cylinder": {
            "new_degree_zero_output": "t",
            "d_epsilon": "L-t",
            "H0": "A[t]/(t-L) isomorphic to A",
            "D_eij": "-epsilon*k_ij",
            "commutator": "[d,D](e_ij)=t*k_ij",
            "honest_DGA_lift": False,
            "interpretation": "H0-preserving curved comparison / terminal export",
        },
        "numeric_sign_guard": {
            "L": str(L),
            "t": str(target),
            "d_epsilon": str(d_epsilon),
            "dD_e": [str(value) for value in d_D_e],
            "Dd_e": [str(value) for value in D_d_e],
            "commutator": [str(value) for value in commutator],
        },
        "no_third_honest_option": (
            "if a connective extension retains H0=A, no nonzero class "
            "L*k can become a boundary; if it becomes a boundary H0 changes"
        ),
    }


def target_representation_audit() -> dict[str, object]:
    # Coordinates are (Aq0,Aq1,Aq2,Bq0,Bq1,Bq2).  The three toric
    # characters have zero row and column sums and span the local
    # endpoint-odd tensor matching-standard module.
    xi01 = (Q(-1), Q(1), Q(0), Q(1), Q(-1), Q(0))
    xi02 = (Q(-1), Q(0), Q(1), Q(1), Q(0), Q(-1))
    xi12 = (Q(0), Q(-1), Q(1), Q(0), Q(1), Q(-1))
    characters = (xi01, xi02, xi12)
    endpoint_rows = (
        (Q(1), Q(1), Q(1), Q(0), Q(0), Q(0)),
        (Q(0), Q(0), Q(0), Q(1), Q(1), Q(1)),
    )
    matching_rows = tuple(
        tuple(Q(index % 3 == matching) for index in range(6))
        for matching in range(3)
    )
    aggregate_rows = endpoint_rows + matching_rows
    require(rank(characters) == 2 and rank(aggregate_rows) == 4
            and all(dot(character, row) == 0
                    for character in characters for row in aggregate_rows),
            "the local toric target character decomposition changed")

    return {
        "local_toric_character_rank": rank(characters),
        "local_aggregate_endpoint_matching_row_rank": rank(aggregate_rows),
        "toric_character_annihilates_all_aggregate_rows": True,
        "representation": (
            "endpoint-odd line tensor two-dimensional matching-standard"
        ),
        "global_covariant_orbit_rank": 30,
        "ordinary_response_target_representation": "aggregate scalar/trivial",
        "ordinary_target_or_Eq_on_Segre_Tate_cells": 0,
        "physical_q_anchor_shadow_on_mixed_character": 0,
        "existing_output_receives_t_times_k": False,
        "minimal_new_output": (
            "one covariant mixed target/terminal family t*k in the doubled "
            "word/fine/repeated Segre grade"
        ),
        "private_site_terminal_route": (
            "requires the still-open incidence from this mixed character "
            "to a decorated offdiagonal cell and its cofactor"
        ),
    }


def beta_scope_audit() -> dict[str, object]:
    return {
        "base_change": "all three alternatives remain exact over k[beta]",
        "beta_scaling_changes_character": False,
        "setting_target_t_equal_beta": (
            "would impose beta=L on H0 and is not an R-linear preservation "
            "of the physical source"
        ),
        "new_beta_Bockstein_from_formal_cylinder": False,
        "physical_beta_terminal_constructed": False,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    source = segre_tate_lift_obstruction_audit()
    cylinder = h0_and_cylinder_sign_audit()
    target = target_representation_audit()
    beta = beta_scope_audit()
    ledger = {
        "theorem": "centered shear H0 / target-cylinder no-third-option",
        "scope": "canonical h=3 Segre response block over characteristic zero",
        "pins": PINS,
        "ordinary_tate_lift_obstruction": source,
        "H0_and_mapping_cylinder": cylinder,
        "physical_target_representation": target,
        "beta_scope": beta,
        "conclusion": {
            "ordinary_Segre_Tate_preserves_A": True,
            "ordinary_Segre_Tate_lifts_centered_shear": False,
            "relative_epsilon_lifts_but_changes_H0": True,
            "target_cylinder_preserves_H0": True,
            "target_cylinder_is_honest_DGA_lift": False,
            "exported_terminal": "t*k_ij",
            "exported_terminal_in_existing_physical_output": False,
            "exact_alternative": (
                "tangent strict lift; or quotient by L; or retain A and "
                "accept the nonzero mixed target curvature t*k"
            ),
        },
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    return ledger, sha256(payload.encode()).hexdigest()


def main() -> None:
    ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    require(digest == EXPECTED_LEDGER_SHA256,
            ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger sha256: {digest}")
    print("ordinary Segre Tate: H0=A, centered shear lift IMPOSSIBLE")
    print("relative d(epsilon)=L: lift EXISTS, H0=A/(L)")
    print("target cylinder d(epsilon)=L-t: H0=A, curvature=t*k")
    print("current physical scalar output: missing mixed t*k terminal")


if __name__ == "__main__":
    main()
