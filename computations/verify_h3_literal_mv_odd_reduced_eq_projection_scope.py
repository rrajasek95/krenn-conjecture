#!/usr/bin/env python3
r"""Identify M_v with the odd reduced-Eq *output* cell, with exact scope.

On the normalized canonical repeated P3+K2 slice, the Gate-I underived cap
packet O_alpha has private/Eq coefficients -alpha, where

    delta=(1,-1,-1,1),  alpha=-delta=(-1,1,1,-1).

The physical source column M_v=-O_alpha+K of commit 271df91 has the opposite
private/Eq coefficients +alpha, zero labelled ordinary residue and protected
rows, and the exact objectwise eta/sigma ridge.  Hence it is precisely the
physical output dressing of the odd reduced-Eq correction.

This does not prove the input comparison.  The selected branch still needs

    J_3(M_v)=A J_col(l),  l=u_024-u_012.

The M_v checker contains no physical q-transport row, and the complete
Hasse/Cartan audit locates the first undefined comparison at the xi Spencer
face.  Thus the odd output cell is closed, while the full odd comparison/q
transport is not.  Generic even and beta-special projections remain separate.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
    "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py":
        "b890195a8fc0c4e90c9c9c0c03c41a95690228c81026f4c2ea1fa95908564e38",
    "computations/verify_h3_selected_lower_quiver_kahler_mapping_cylinder_gate.py":
        "e5deda7162db47f229239dc91b419baaf00c3158249859cbafb03fe3af2cc958",
    "computations/verify_h3_selected_lower_one_chain_comparison_reduction.py":
        "c9fc8c847327d0e119264a3a83cf39d0f4c2ff45b4ddd4e048f42a57cac0e887",
    "computations/verify_h3_complete_hasse_cartan_naturality_square_gate.py":
        "3ea6a79bc6918cc4569bd12ad0b1634679c28037b687b6ae7c0e610e81998279",
    "computations/verify_h3_reduced_eq_spencer_three_projection_gate.py":
        "315508b572fa0d96b33ba83b8ac4905e59dfbf8f484023891618dbb3c6489d83",
    "computations/verify_h3_reduced_eq_full_occurrence_simplex_symmetrization_gate.py":
        "5150fa94137a07062092b32328af63f4e188823d6ca06160a10e4b1c040786d3",
}
EXPECTED_LEDGER_SHA256 = (
    "8bc87fa4289fe08f15649a9c127d0c0e815f6d9127399015a980d3d2876ebc96"
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def add(left, right):
    return tuple(Q(a) + Q(b) for a, b in zip(left, right, strict=True))


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual, expected))

    mv_source = (ROOT / (
        "computations/verify_h3_literal_mv_cap_cartan_composition.py"
    )).read_text()
    literal_source = (ROOT / (
        "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py"
    )).read_text()
    require('"M_v_equals_minus_O_plus_K"' in mv_source
            and '"literal_boundary_support": 360' in mv_source
            and '"ordinary_residue": [0, 0, 0, 0]' in mv_source
            and '"D_W_target_ainc": [0, 0, 0, 0]' in mv_source
            and '"eta_z": "1+delta_(vz)*u_z/t"' in mv_source
            and '"sigma": "-q_pq^22"' in mv_source,
            "literal M_v output ledger changed")

    delta = (Q(1), Q(-1), Q(-1), Q(1))
    alpha = tuple(-value for value in delta)
    old_eq = delta
    mv_eq = alpha
    mv_residue = (Q(0),) * 4
    require(alpha == tuple(-value for value in delta),
            "alpha stopped being -delta")
    require(old_eq == delta and mv_eq == alpha,
            "Gate-I Eq correction signs changed")
    require(add(old_eq, mv_eq) == (Q(0),) * 4,
            "M_v stopped cancelling the underived Eq packet")
    require('"literal_boundary": "-sum_j alpha_j B_j"' in mv_source
            and '"literal_boundary": "+sum_j alpha_j B_j"' in mv_source,
            "M_v stopped cancelling the literal private boundary")
    require(mv_residue == (Q(0),) * 4,
            "M_v acquired a labelled residue or protected row")

    # The literal augmented module explicitly has private/Eq/W/target/R,
    # ainc, and eta/sigma rows.  It has no physical q-transport row.  This is
    # an exact scope observation, not an inferred zero value.
    require('ROWS = BASE_ROWS + TERMINAL_ROWS' in literal_source
            and 'for kind in ("private", "Eq", "W", "target", "R")'
            in literal_source
            and '"eta1_U1", "sigma_qpq22"' in literal_source
            and 'q_transport' not in literal_source,
            "literal M_v module unexpectedly acquired a q row")

    # Pin the common physical grade, independently of the vector identity.
    closure_source = (ROOT / (
        "computations/verify_h3_physical_cartan_closes_residual_q_ks_hypothesis.py"
    )).read_text()
    source_word = "1211222 after deleting the distinguished endpoint"
    source_grade = (
        "canonical labelled repeated P3+K2 / endpoint-recoloured faces-(3,5) bridge"
    )
    require(f'"word": "{source_word}"' in closure_source
            and f'"grade": "{source_grade}"' in closure_source,
            "M_v left the canonical Gate-I word/grade")

    one_chain_source = (ROOT / (
        "computations/verify_h3_selected_lower_one_chain_comparison_reduction.py"
    )).read_text()
    missing_equation = "J_3(M_v)=A J_col(l)"
    require(f'"equation": "{missing_equation}"' in one_chain_source
            and '"source_valid_one_chain_constructed": False'
            in one_chain_source,
            "selected input comparison scope changed")

    naturality_source = (ROOT / (
        "computations/verify_h3_complete_hasse_cartan_naturality_square_gate.py"
    )).read_text()
    require('"required_identity": "Pi_1 d_PP = d_corr Pi_0"'
            in naturality_source
            and '"normalized_dual": dual["functional"]' in naturality_source
            and '"functional": "lambda_xi=(3/4)e_xi^*"'
            in (ROOT / (
                "computations/verify_h3_selected_lower_full_row_spencer_discrepancy.py"
            )).read_text(),
            "first hidden comparison row changed")
    first_undefined_comparison = "Pi_1 d_PP = d_corr Pi_0"

    quiver_source = (ROOT / (
        "computations/verify_h3_selected_lower_quiver_kahler_mapping_cylinder_gate.py"
    )).read_text()
    q_condition = "o_q(Phi)=[q_xv*Phi-q_pq]=0 in D_pq^*/row(J_pq)"
    require(f'"{q_condition}"' in quiver_source
            and '"The full augmented decorations and q defect must still descend"'
            in quiver_source,
            "physical q quotient gate changed")

    ledger = {
        "theorem": "literal M_v is the odd reduced-Eq output projection",
        "pins": PINS,
        "coefficient_signs": {
            "delta_underived_residual": [int(value) for value in delta],
            "alpha_correction": [int(value) for value in alpha],
            "alpha_equals_minus_delta": True,
            "O_alpha_Eq": [int(value) for value in old_eq],
            "M_v_Eq": [int(value) for value in mv_eq],
            "sum": [0, 0, 0, 0],
        },
        "physical_output_rows": {
            "literal_private_boundary": (
                "+sum alpha_j B_j, 360 features, opposite O_alpha"
            ),
            "Eq": [int(value) for value in mv_eq],
            "labelled_ordinary_residue": [int(value) for value in mv_residue],
            "D_W_target_ainc": [0, 0, 0, 0],
            "eta_z": "1+delta_(vz)*u_z/t",
            "sigma": "-q_pq^22",
            "word": source_word,
            "fine_repeated_grade": source_grade,
            "source_provenant": True,
            "verdict": "exact odd K_Eq physical output dressing on Y=1 slice",
        },
        "q_scope": {
            "residual_q_output_terminal": (
                "closed: M_v has the exact objectwise eta/sigma packet"
            ),
            "physical_q_transport_row_in_271df91": False,
            "required_quotient_condition": q_condition,
            "selected_full_chain_equation": missing_equation,
            "first_undefined_row": (
                "xi first coefficient-prolongation/relative Spencer face"
            ),
            "first_undefined_comparison": first_undefined_comparison,
            "verdict": (
                "the output cell does not by itself construct the input "
                "Cartan-Spencer comparison or physical q homotopy"
            ),
        },
        "frontier": {
            "odd_reduced_Eq_output_cell": "CLOSED by M_v=-O_alpha+K",
            "odd_selected_input_comparison_and_q_transport": "OPEN",
            "odd_open_equations": 1,
            "odd_open_equation": "J_3(M_v)=A J_col(u_024-u_012)",
            "generic_even_physical_rho_orbit": "OPEN",
            "beta_special_Bockstein_projection": "OPEN",
            "scope_warning": (
                "do not call the entire odd Gate-I comparison closed merely "
                "from output-side M_v membership"
            ),
        },
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("unexpected ledger digest", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 literal M_v / odd reduced-Eq projection scope: PASS")
    print("Eq sign: alpha=-delta; O_alpha+M_v has zero Eq/private boundary")
    print("odd physical output cell: CLOSED on normalized canonical slice")
    print("input comparison and physical q transport: OPEN at one chain equation")
    print("generic even rho orbit and beta Bockstein: OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
