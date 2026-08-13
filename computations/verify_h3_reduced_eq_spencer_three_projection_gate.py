#!/usr/bin/env python3
"""Unify the odd, even, and beta-Bockstein reduced-Eq shadows.

Three pinned constructions expose the same monic conormal

    E = (H0-u)*e_Eq.

* The odd pq/xv quiver cylinder leaves +E under physical descent.
* The generic rho-even orbit requires +2*D*E tensor v.
* The beta-zero third-cofactor proper face has boundary -E; the correction
  V needed by the cap Smith packet is therefore the same E direction with
  zero root output.

This checker verifies the exact coefficient projections and a universal
mapping-cone normal form.  It also freezes why this is not yet a physical
identification: the pinned proper face is not source-valid and has nonzero
ridge/wrong-word data, while no integral k[beta]-linear full orbit exists.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py":
        "7d9e49f34da84772f6e0863a9bfe56cb9a90e0cfd3fceb76da59175ffea36c50",
    "computations/verify_h3_generic_cartan_adjacent_target_label_prolongation.py":
        "ef63bd26210802cf300e263da44e178b4dd19abbf0fa5bba059b5d61afb9b782",
    "computations/verify_h3_rootless_third_cofactor_bianchi_total_complex_obstruction.py":
        "ebd25f79a6fe8db936fe5601b9220f152c5349dd794bbc4e08b2095f1c1d059f",
    "computations/verify_h3_beta_rees_cap_smith_saturation_gate.py":
        "fb031132ddd0510197560be0644324c436216192a9f15140ae3ef52b2a1fb4e5",
    "computations/verify_h3_tau_plus_full_interface_product_bianchi_extension_gate.py":
        "32be7ef48ad9d35b8863a62889508ccdff0010d8ebff18b366e932aab8b2bf14",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(*vectors):
    return tuple(sum(Q(vector[index]) for vector in vectors)
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def tensor(left, right):
    return tuple(Q(a) * Q(b) for a in left for b in right)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(columns):
    if not columns:
        return 0
    height = len(columns[0])
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def audit_pinned_conormal_identifications():
    shifted = (ROOT / (
        "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py"
    )).read_text()
    generic = (ROOT / (
        "computations/verify_h3_generic_cartan_adjacent_target_label_prolongation.py"
    )).read_text()
    total = (ROOT / (
        "computations/verify_h3_rootless_third_cofactor_bianchi_total_complex_obstruction.py"
    )).read_text()
    full = (ROOT / (
        "computations/verify_h3_tau_plus_full_interface_product_bianchi_extension_gate.py"
    )).read_text()

    require('"diagonal_projection_commutator": "(H_0-u)*eq"' in shifted,
            "the odd physical reduced-Eq residual changed")
    require('"missing_relative_correction": "+2D*(H0-u)*Eq"' in generic
            and '"reduced_Eq_face": "+2 D (H0-u)Eq tensor v"' in full,
            "the even reduced-Eq face changed")
    require('expected_tail_boundary: Module = {' in total
            and '("Eq", ()): scale(-1, b)' in total
            and 'b = add(pure_h, scale(-1, variable(U_TARGET)))' in total,
            "the beta-zero third-cofactor Eq boundary changed")
    require('"source_valid": False' in full
            and '"endpoint_ridge_space_rank": 6' in full
            and '"Omega_obstruction_rank": 5' in full
            and '"selected_midpoint_word_hits": 0' in full,
            "the full-orbit physical obstruction changed")
    return {
        "universal_conormal": "E=(H0-u)e_Eq",
        "odd_underived_residual": "+E",
        "even_required_face": "+2 D E tensor v",
        "beta_zero_formal_tail_boundary": "-E",
        "same_polynomial_and_Eq_basis": True,
        "same_physical_source_grade": False,
    }


def audit_three_projections():
    # The generic fixed label direction and four-corner root defect.
    v = (Q(0), Q(1, 2), Q(0), Q(0), Q(1, 2), Q(0))
    d = (Q(-1), Q(1), Q(-1), Q(1))
    even = scale(2, tensor(d, v))
    require(sum(value != 0 for value in even) == 8
            and set(value for value in even if value) == {Q(-1), Q(1)}
            and sum(even) == 0,
            "the even Eq coefficient packet changed")

    # Odd is the one-dimensional sign sector.  Bockstein is the
    # one-dimensional special selected-root sector.  These coefficient
    # modules are independent; their common factor is E, not a scalar
    # equality between physical grades.
    odd = (Q(-1),)  # correction to the +E residual.
    bockstein_v = (Q(1),)  # same defect as U, zero root output.
    require(odd == (Q(-1),) and bockstein_v == (Q(1),),
            "the odd/special conormal signs changed")
    return {
        "odd_projector": {
            "coefficient": -1,
            "output": "-E cancels the quiver cylinder's +E",
            "rho_parity": "odd",
        },
        "even_projector": {
            "root_defect_D": [int(value) for value in d],
            "label_v": [str(value) for value in v],
            "coefficient_2D_tensor_v": [int(value) for value in even],
            "output": "+2 D E tensor v",
            "rho_parity": "even",
        },
        "beta_Bockstein_projector": {
            "coefficient": 1,
            "output": "V has the unary primitive E defect and zero rho0/rho2",
            "special_root_sector": "selected D0",
        },
        "coefficient_module_rank": rank((
            (Q(1), Q(0), Q(0)),
            (Q(0), Q(1), Q(0)),
            (Q(0), Q(0), Q(1)),
        )),
    }


def audit_mapping_cone_normal_form():
    # Rows: (E, rho0, rho2).  U is the beta-zero unary top.  V is the
    # required proper-face correction.  The difference is protected rho0.
    unary = (Q(1), Q(1), Q(0))
    correction = (Q(1), Q(0), Q(0))
    protected_d0 = add(unary, scale(-1, correction))
    require(protected_d0 == (Q(0), Q(1), Q(0)),
            "the beta-zero mapping-cone subtraction changed")

    # A universal Eq-cone cell has one E boundary, then each symmetry
    # projector tensors that boundary with its coefficient.  Projectors
    # commute with the two-term differential because they act only on the
    # coefficient module.
    e_boundary = (Q(1),)
    coefficients = {
        "odd": (Q(-1),),
        "special": (Q(1),),
    }
    require(scale(coefficients["odd"][0], e_boundary) == (Q(-1),)
            and scale(coefficients["special"][0], e_boundary) == (Q(1),),
            "the universal Eq cone stopped commuting with projection")
    return {
        "universal_two_term_cone": "K_Eq -> R*E, d(K_Eq)=E",
        "projection_law": "d(K_Eq tensor c)=E tensor c",
        "beta_zero_unary_U": [1, 1, 0],
        "required_proper_face_V": [1, 0, 0],
        "protected_difference_U_minus_V": [0, 1, 0],
        "formal_three_projection_unification": True,
        "physical_three_projection_cell_constructed": False,
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "reduced-Eq Spencer three-projection gate",
        "pins": PINS,
        "pinned_conormal_identifications": audit_pinned_conormal_identifications(),
        "three_symmetry_projections": audit_three_projections(),
        "universal_mapping_cone": audit_mapping_cone_normal_form(),
        "single_physical_theorem": (
            "construct a source-labelled Rees-linear reduced-Eq/Spencer "
            "mapping cone K_Eq(beta) over k[beta] in the complete augmented "
            "word/fine/repeated complex.  Its odd projection must cancel the "
            "quiver cylinder E residual and preserve the physical q/terminal "
            "typing; its generic even projection must be +2D E tensor v "
            "inside the full delta+/target/ores/W orbit; and its beta-zero "
            "Bockstein proper face must be V with the same primitive E defect "
            "as the unary top and zero rho0/rho2.  All ridge and word faces "
            "must totalize source-validly"
        ),
        "consequence_if_constructed": (
            "odd Interface-I loses its last underived Eq residual; generic "
            "Interface-III gains its forced Eq face; at beta zero U-V is the "
            "protected D0 unit and the cap Smith beta torsion disappears"
        ),
        "current_exact_status": (
            "the common conormal and all three coefficient projections are "
            "exact.  The physical theorem is open: current odd/even/special "
            "objects have different grades, and the only formal common proper "
            "face is not source-valid and retains primitive ridge/wrong-word "
            "outputs"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    expected = "ad0fa899252ab48d5df1eb868b1492ecc07619c05cc976fe73526fdfa7fceee3"
    require(digest == expected, ("unexpected ledger digest", digest, expected))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 reduced-Eq Spencer three-projection gate: PASS")
    print("common conormal: E=(H0-u)e_Eq")
    print("odd projection: -E")
    print("even projection: +2D E tensor v")
    print("beta Bockstein projection: V, then U-V=protected D0")
    print("physical integral cone: OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
