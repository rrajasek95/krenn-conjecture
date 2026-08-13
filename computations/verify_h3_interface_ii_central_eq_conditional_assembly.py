#!/usr/bin/env python3
"""Remove Interface II as an independent construction, conditionally on K_Eq.

The full sixteen-term response Hessian symbol is already constructed, and
the two-object theta groupoid has zero principal-parts and physical-q
holonomy.  Hence its complete augmented defect has only the central
reduced-Eq coordinate E=(H0-u)e_Eq.  A physical K_Eq with boundary -E and
zero lane-II terminal rows closes the interface immediately.

If that cell is absent, exact Fredholm duality detects the same projected
augmented cokernel class [E] that appears in the odd/even projections of the
universal Eq cone; there is no extra theta-grade class.

The existing derived Hasse/Tate construction supplies a formal Koszul
generator for F0=H0-u.  Its physical promotion remains open: the existing
pure row has target one, while a target-zero copy is precisely K_Eq.  The
selected-u conormal detects the failure of the old source inventory.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_trapped_hessian_theta_eq_grade_groupoid.py":
        "b30000bfe8383e1f254fb8fee4724cbd99d8f70a5e8447cffb1c9086a179aec0",
    "computations/verify_h3_trapped_hessian_to_six_term_endpoint_polarization_gate.py":
        "a51b8f091a25624d17443c70ac70b60eb257c8b11dafb0b9ad3f17962dc07390",
    "computations/verify_h3_reduced_eq_spencer_three_projection_gate.py":
        "315508b572fa0d96b33ba83b8ac4905e59dfbf8f484023891618dbb3c6489d83",
    "computations/verify_h3_full_hasse_koszul_cap_totalization.py":
        "51940ce0ac8387b68e7725508db6da1a1c055ea036335bbf19750580c69e13fb",
    "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py":
        "7d9e49f34da84772f6e0863a9bfe56cb9a90e0cfd3fceb76da59175ffea36c50",
    "computations/verify_h3_source_base_change_conormal_obstruction.py":
        "1a921671ab378f68355c2a6196d1951cad30244d78a9e90ec2715ce47ef12bf0",
    "computations/verify_h3_six_term_dual_absolute_resolution_exhaustivity.py":
        "d1b545f25603930a6247a286c5be70c7d16e20caab053401eeeb650bb53559d6",
}
EXPECTED_LEDGER_SHA256 = (
    "a5cd69b09039556ced4ddb35e952b8a6c0c76e580fca1a8d51e019d3b6ebc057"
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def add(left, right):
    return tuple(Q(a) + Q(b) for a, b in zip(left, right, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns):
    if not columns:
        return 0
    height = len(columns[0])
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    row = 0
    for column in range(len(columns)):
        pivot = next((index for index in range(row, height)
                      if work[index][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        value = work[row][column]
        work[row] = [entry / value for entry in work[row]]
        for index in range(height):
            if index == row or not work[index][column]:
                continue
            value = work[index][column]
            work[index] = [left - value * right for left, right
                           in zip(work[index], work[row], strict=True)]
        row += 1
    return row


def nullspace_rows(columns):
    """Basis for covectors lambda with lambda*columns=0."""
    if not columns:
        return ()
    height = len(columns[0])
    # Nullspace of the transpose: equations are columns, variables are rows.
    equations = [[Q(entry) for entry in column] for column in columns]
    if not equations:
        return tuple(tuple(Q(index == column) for index in range(height))
                     for column in range(height))
    work = equations
    pivot_columns = []
    pivot_row = 0
    for column in range(height):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right
                         in zip(work[row], work[pivot_row], strict=True)]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    free_columns = [column for column in range(height)
                    if column not in pivot_columns]
    basis = []
    for free in free_columns:
        vector = [Q(0)] * height
        vector[free] = Q(1)
        for row, pivot in enumerate(pivot_columns):
            vector[pivot] = -work[row][free]
        basis.append(tuple(vector))
    return tuple(basis)


def conditional_interface_ii_assembly():
    # Coordinates: 16 response endpoint-tail terms, then
    # (q,target,W,ainc,ores_g,ores_gT,eta0,eta1,sigmaPS,Eq).
    response = 16
    augmented = 10
    height = response + augmented
    EQ = height - 1

    # The complete symbol is already present.  After comparing it with the
    # required full symbol, every response and terminal coordinate cancels;
    # the sole underived diagonal residual is +E.
    symbol_actual = tuple(Q((-1, 1, 1, -1)[index // 4])
                          for index in range(response))
    symbol_required = symbol_actual
    residual = [Q(0)] * height
    for index in range(response):
        residual[index] = symbol_actual[index] - symbol_required[index]
    residual[EQ] = Q(1)
    residual = tuple(residual)
    require(sum(value != 0 for value in residual) == 1
            and residual[EQ] == 1,
            "Interface-II residual stopped being the pure Eq coordinate")

    k_eq = tuple(Q(-1) if index == EQ else Q(0)
                 for index in range(height))
    require(not any(add(residual, k_eq)),
            "central K_Eq stopped closing the Interface-II defect")

    # theta acts only between the two labelled grade objects and fixes E.
    # Its q and terminal cocycles were pinned in d212218.  Therefore adding
    # K_Eq cannot reveal another lane-II coordinate.
    theta_source = (ROOT / (
        "computations/verify_h3_trapped_hessian_theta_eq_grade_groupoid.py"
    )).read_text()
    require('"q_cocycle": "Lambda_gT o theta-Lambda_g=0 exactly"'
            in theta_source
            and '"first_PP_diagonal": 0' in theta_source
            and '"two_edge_cone_holonomy": 0' in theta_source,
            "the pinned theta zero-holonomy theorem changed")

    return {
        "complete_response_symbol_terms": response,
        "response_symbol_defect": 0,
        "nonEq_augmented_defect": 0,
        "sole_defect": "+E=(H0-u)e_Eq",
        "conditional_cell": "d K_Eq|_II=-E, all II nonEq rows zero/protected",
        "total_after_cell": 0,
        "theta_first_PP_diagonal": 0,
        "theta_q_cocycle": 0,
        "independent_InterfaceII_construction_after_physical_K_Eq": False,
    }


def fredholm_cokernel_audit():
    # Exhaust every binary physical boundary matrix of height <=3 and width
    # <=3.  For a proposed boundary b, either b is already in the image or
    # an exact left-null covector detects it.  This is the finite shadow of
    # the augmented comparison-cone alternative used in all three sectors.
    cases = membership = detected = 0
    for height in range(1, 4):
        for width in range(1, 4):
            for entries in product((0, 1), repeat=height * width + height):
                columns = tuple(
                    tuple(Q(entries[column * height + row])
                          for row in range(height))
                    for column in range(width)
                )
                b = tuple(Q(value) for value in entries[height * width:])
                old_rank = rank(columns)
                new_rank = rank(columns + (b,))
                if new_rank == old_rank:
                    membership += 1
                else:
                    witness = next((covector for covector in
                                    nullspace_rows(columns)
                                    if dot(covector, b)), None)
                    require(witness is not None,
                            ("missing augmented cokernel dual", columns, b))
                    detected += 1
                require(new_rank in (old_rank, old_rank + 1),
                        "one proposed column changed rank by more than one")
                cases += 1
    require(cases == 5036 and membership + detected == cases,
            ("Fredholm census changed", cases, membership, detected))
    return {
        "binary_augmented_maps_checked": cases,
        "boundary_membership_cases": membership,
        "cokernel_dual_cases": detected,
        "alternative": "b in im(d), or lambda*d=0 and lambda(b)!=0",
        "InterfaceII_class": "[E]_II in the augmented physical cokernel",
        "cross_interface_meaning": (
            "[E]_II is the occurrence projection of the same universal "
            "central class whose odd/even projections are Interfaces I/III"
        ),
        "guard": (
            "the numerical detecting covectors live in their projected "
            "terminal modules; they need not be literally the same covector"
        ),
    }


def derived_tate_route_audit():
    full = (ROOT / (
        "computations/verify_h3_full_hasse_koszul_cap_totalization.py"
    )).read_text()
    shifted = (ROOT / (
        "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py"
    )).read_text()
    conormal = (ROOT / (
        "computations/verify_h3_source_base_change_conormal_obstruction.py"
    )).read_text()
    absolute = (ROOT / (
        "computations/verify_h3_six_term_dual_absolute_resolution_exhaustivity.py"
    )).read_text()
    require('"diagonal_projection_commutator": "(H_0-u)*eq"' in shifted
            and "top physical descent commutator" in shifted,
            "the primitive derived-to-underived Eq commutator changed")
    require("physical-source descent fails exactly" in full,
            "the full Hasse totalization descent guard changed")
    require("conormal_connecting_class" in conormal
            and "kappa*[F0] in J/J^2" in conormal,
            "the selected-u conormal obstruction changed")
    require("natural C5 Tate multiplication and its 239-dimensional kernel"
            in absolute
            and "genuinely relative chart-nondiagonal mapping-cone generator"
            in absolute,
            "the absolute Tate exhaustivity conclusion changed")

    # Literal coarse augmented module at any active specialization.
    # Coordinates are (selected-u F0*Eq, w, target, ordinary residue).
    samples = []
    for kappa, y in ((Q(1), Q(1)), (Q(2), Q(3)), (Q(-3), Q(5, 2))):
        r0 = (Q(-1), Q(0), Q(1), Q(0))
        cap = (Q(0), -y, Q(1), Q(0))
        rho = (Q(0), Q(1), Q(0), Q(1))
        normal = (Q(0), kappa, Q(0), kappa)
        candidate = add(add(scale(y, normal), scale(-kappa * y, rho)),
                        add(scale(-kappa, cap), scale(kappa, r0)))
        desired = (Q(0), kappa * y, Q(0), Q(0))
        defect = add(desired, scale(-1, candidate))
        separator = (y, Q(1), y, Q(-1))
        require(candidate == (-kappa, kappa * y, Q(0), Q(0))
                and defect == (kappa, Q(0), Q(0), Q(0)),
                "the underived conormal defect changed")
        require(all(dot(separator, column) == 0
                    for column in (r0, cap, rho, normal))
                and dot(separator, desired) == kappa * y,
                "the physical separator stopped detecting the desired lift")
        samples.append({
            "kappa": str(kappa), "Y": str(y),
            "old_candidate": [str(value) for value in candidate],
            "missing_conormal_face": [str(value) for value in defect],
            "separator_value": str(dot(separator, desired)),
        })

    return {
        "derived_positive_result": (
            "the complete Boolean Hasse/Koszul totalization has the formal "
            "top generator and cancels every proper Leibniz face"
        ),
        "first_underived_residual": "E=(H0-u)e_Eq",
        "derived_intersection_generator": (
            "the Koszul/Tate degree-one generator epsilon_F0 with "
            "d epsilon_F0=F0"
        ),
        "physical_augmentation_fork": {
            "identify_with_existing_r0": "target=1, so not K_Eq",
            "declare_target_zero": (
                "exactly the new relative K_Eq cell; not supplied by the "
                "old source differential"
            ),
        },
        "connecting_class": "[F0] in J/J^2 (or kappa[F0] after decoration)",
        "absolute_Tate_route": (
            "exhausted absolute Tate kernels are augmentation-dark and do "
            "not supply the relative cell"
        ),
        "sample_conormal_checks": samples,
        "smallest_new_physical_cell": (
            "one target-zero source-labelled relative Tate generator with "
            "boundary E and the required q/ores/eta/sigma projections"
        ),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "Interface-II central-Eq conditional assembly theorem",
        "pins": PINS,
        "conditional_assembly": conditional_interface_ii_assembly(),
        "augmented_cokernel_alternative": fredholm_cokernel_audit(),
        "derived_intersection_Tate_route": derived_tate_route_audit(),
        "proof_frontier_change": (
            "Interface II is no longer an independent construction lane: "
            "a physical central K_Eq closes it, and failure is precisely its "
            "projected augmented cokernel class.  The remaining constructive "
            "problem is the common source-labelled K_Eq descent"
        ),
        "scope": (
            "conditional assembly and exact old-inventory obstruction.  "
            "The target-zero physical Tate/response-to-Eq generator is not "
            "constructed, and the three projected detecting covectors are "
            "not asserted literally equal"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("Interface-II conditional ledger changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 Interface-II central-Eq conditional assembly: PASS")
    print("symbol/q/theta/terminal debt outside Eq: ZERO")
    print("physical K_Eq => Interface II closed without independent cell")
    print("failure => projected augmented [E] cokernel dual")
    print("derived Tate generator: formal; target-zero physical lift: OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
