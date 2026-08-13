#!/usr/bin/env python3
"""Audit the order-two even Cartan/J* target-cone construction.

For h=2 the generic diagonal cap combination specializes to

    J*=(beta-alpha)J1+(beta+alpha)J2=-2 alpha beta I.

Conditional on the shifted source-labelled placement P2/iota, the even
Cartan cell

    C2+=(4 alpha beta)^-1 (1+S) H_w P2(J*)
       =-1/2 (1+S) H_w P2(I)

has target -2(w-1)Delta.  This cancels the two-orientation target normal
of one lower B-4 endpoint edge.  The Cartan identity leaves the exact first
principal-parts residual

    R2+=-1/2 (1+S) H_w d(P2(I)).

In the canonical reduced-Eq target-cone projection this is the familiar
conormal: a correction with target -2D also carries -2D(H0-u)Eq, so the
next required cell has +2D(H0-u)Eq.  The target construction is therefore
positive on the generic diagonal open, but its occurrence-local physical
placement is exactly the still-missing shifted comparison.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h2_lower_0112_bminus4_target_normal_gate.py":
        "8fffe45182c4bb304dabfbe9df568061a8049bec21949539bcae88f60f5d22e0",
    "notes/h2-lower-0112-bminus4-target-normal-gate.md":
        "bda5d506d3e7376b8314d37d9ddd37d7d48ae77319dda70b4ba550e84abf4e1e",
    "computations/verify_h3_generic_cartan_adjacent_target_label_prolongation.py":
        "ef63bd26210802cf300e263da44e178b4dd19abbf0fa5bba059b5d61afb9b782",
    "notes/h3-generic-cartan-adjacent-target-label-prolongation.md":
        "acbeaf6c50910244742ab00017b760bbaafd1f4ec6dccc8adb2ed8cefef7f8f3",
    "computations/verify_h3_reduced_eq_integral_rho_comparison_master_gate.py":
        "813419c756e7f21c09d63d3ec10f44c787e9580ca08c87809b7c4c550b908b4f",
    "notes/h3-reduced-eq-integral-rho-comparison-master-gate.md":
        "3fa8fdc6bcd17145bc1e40c608259b2312ee52f1482520fbe9e0f5a3cd1e7a76",
    "computations/verify_h3_selected_lower_quiver_kahler_mapping_cylinder_gate.py":
        "e5deda7162db47f229239dc91b419baaf00c3158249859cbafb03fe3af2cc958",
    "notes/h3-selected-lower-quiver-kahler-mapping-cylinder-gate.md":
        "1b5b44e4cc55af30cfaf26b0128af043d141896b2aa16a7ed3f2b1138ece039f",
    "computations/verify_h2_b4_cplus_shared_interface_gate.py":
        "ee48f2d1446d938fc97cda4e0977472081ee9823d31dc91f3f4c46829f3d8400",
    "notes/h2-b4-cplus-shared-interface-gate.md":
        "4c89253c18f4475371849a78c990e27b7d6af79193522cd5a583af80cc929fb8",
}
EXPECTED_LEDGER_SHA256 = (
    "a4187600dd8757791454dda6ca346ae88cd19ee914dd61a6dded04f76bbd3413"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def load_target_module():
    relative = (
        "computations/verify_h2_lower_0112_bminus4_target_normal_gate.py"
    )
    specification = importlib.util.spec_from_file_location(
        "h2_bminus4_target", ROOT / relative
    )
    require(specification is not None and specification.loader is not None,
            "cannot load lower target-normal module")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * entry for entry in vector)


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def matrix_add(*terms):
    """Terms are (coefficient,matrix)."""
    first = terms[0][1]
    return tuple(tuple(sum(
        Q(coefficient) * matrix[row][column]
        for coefficient, matrix in terms
    ) for column in range(len(first[0]))) for row in range(len(first)))


def identity(size=3):
    return tuple(tuple(Q(row == column) for column in range(size))
                 for row in range(size))


def h2_jstar_audit():
    one = identity()
    k0 = tuple(tuple(Q(row == column == 0) for column in range(3))
               for row in range(3))
    records = []
    for alpha, beta in (
        (Q(2), Q(3)), (Q(-5, 2), Q(7)),
        (Q(4, 3), Q(-2)), (Q(-3), Q(-5, 7)),
    ):
        k1 = matrix_add((alpha + beta, k0), (-alpha, one))
        k2 = matrix_add((alpha, k0), (-alpha, one))
        j1 = k1
        j2 = matrix_add((-beta, k0), (1, k2))
        jstar = matrix_add((beta - alpha, j1), (beta + alpha, j2))
        expected = matrix_add((-2 * alpha * beta, one),)
        require(jstar == expected,
                ("h2 J* trace identity changed", alpha, beta, jstar))

        target_j1 = (beta, -alpha, -alpha)
        target_j2 = (-beta, -alpha, -alpha)
        target_jstar = add(
            scale(beta - alpha, target_j1),
            scale(beta + alpha, target_j2),
        )
        require(target_jstar == (-2 * alpha * beta,) * 3,
                "h2 J* target identity changed")

        # P2 contributes the intrinsic order factor h=2.  Evenization
        # doubles once more because endpoint-role swap fixes the target.
        p2_target_scale = 2 * target_jstar[0]
        normalized_target_scale = Q(1, 4 * alpha * beta) * 2 * p2_target_scale
        require(normalized_target_scale == -2,
                "h2 normalized even Cartan target changed")
        normalized_remainder_coefficient = (
            Q(1, 4 * alpha * beta) * (-2 * alpha * beta)
        )
        require(normalized_remainder_coefficient == Q(-1, 2),
                "h2 trace remainder retained alpha/beta")
        records.append({
            "alpha": str(alpha),
            "beta": str(beta),
            "Jstar": "-2*alpha*beta*I",
            "T_Jstar": [str(value) for value in target_jstar],
            "P2_target": "-4*alpha*beta*Delta",
            "normalized_even_target": "-2*(w-1)Delta",
            "normalized_Rplus_coefficient": "-1/2",
        })

    # The polynomial J* vanishes on the two coordinate divisors.  At beta=0
    # J2=J1, so normalization does not define a regular physical cell.
    alpha, beta = Q(2), Q(0)
    target_j1 = (beta, -alpha, -alpha)
    target_j2 = (-beta, -alpha, -alpha)
    require(target_j1 == target_j2 == (Q(0), Q(-2), Q(-2)),
            "h2 beta-zero diagonal collision changed")
    return {
        "h2_formula": "J*=(beta-alpha)J1+(beta+alpha)J2",
        "full_matrix_identity": "J*=-2*alpha*beta*I",
        "generic_open": "alpha*beta != 0",
        "normalized_cell": (
            "C2+=(4 alpha beta)^-1(1+S)H_w P2(J*)="
            "-1/2(1+S)H_w P2(I)"
        ),
        "normalized_target": "-2*(w-1)Delta4",
        "first_formal_residual": "R2+=-1/2(1+S)H_w d(P2(I))",
        "beta_zero_regular_specialization": False,
        "records": records,
    }


def per_root_target_cancellation_audit():
    target = load_target_module()
    root_moves = ((0, 4), (0, 5), (1, 5))
    records = []
    total_b_even = target.ZERO_TARGET
    total_correction = target.ZERO_TARGET
    for left, right in root_moves:
        defect = target.target_defect(left, right)
        require(defect != target.ZERO_TARGET,
                ("a root move lost target defect", left, right))
        b_even_target = scale(2, defect)
        jstar_correction = scale(-2, defect)
        require(add(b_even_target, jstar_correction) == target.ZERO_TARGET,
                "h2 J* failed to cancel one even B target")
        total_b_even = add(total_b_even, b_even_target)
        total_correction = add(total_correction, jstar_correction)
        records.append({
            "sites": [left, right],
            "root_colours": [target.COLOUR[left], target.COLOUR[right]],
            "D_xt": target.sparse(defect),
            "even_B_target": target.sparse(b_even_target),
            "normalized_Jstar_target": target.sparse(jstar_correction),
        })
    marked = target.marked_local_normal_audit()
    marked_normal = add(*(target.target_defect(*move) for move in root_moves))
    require(target.sparse(marked_normal)
            == marked["marked_B_minus_4_target_normal"],
            "the three-root sum stopped being the marked target normal")
    require(total_b_even == scale(2, marked_normal)
            and add(total_b_even, total_correction) == target.ZERO_TARGET,
            "the full marked even target failed to cancel")
    return {
        "root_decorated_moves": records,
        "same_colour_move_1_to_4": "target-safe site bar; no J* root cone",
        "marked_even_B_target": target.sparse(total_b_even),
        "sum_of_Jstar_corrections": target.sparse(total_correction),
        "target_after_sum": {},
        "target_cancellation": "exact on alpha*beta != 0 after P2/iota",
    }


def even_cartan_internal_no_go_audit():
    # Orbit coordinates are (H_w,S H_w).  S fixes the Weyl target defect.
    target_row = (Q(1), Q(1))
    even = (Q(1), Q(1))
    odd = (Q(1), Q(-1))
    require(dot(target_row, even) == 2
            and dot(target_row, odd) == 0,
            "even/odd Cartan target split changed")
    # An internal correction to the signless vector which kills the target
    # necessarily lands in the odd line.  There is no nonzero even vector
    # in the target kernel.
    require(add(even, scale(-2, (Q(1), Q(0)))) == scale(-1, odd)
            and dot(target_row, add(even, scale(-2, (Q(1), Q(0))))) == 0,
            "internal target correction stopped collapsing to odd")
    return {
        "Cartan_orbit_basis": ["H_w", "S H_w"],
        "target_map": [1, 1],
        "even_line": [1, 1],
        "target_kernel": "Q*(1,-1), the odd line",
        "nonzero_even_target_safe_internal_combination": False,
        "consequence": (
            "the diagonal J* target-bearing input is independent; an "
            "internal correction of the old even prism recovers only the "
            "odd prism"
        ),
    }


def first_principal_parts_residual_audit():
    target = load_target_module()
    root_moves = ((0, 4), (0, 5), (1, 5))
    records = []
    marked_normal = target.ZERO_TARGET
    for left, right in root_moves:
        defect = target.target_defect(left, right)
        marked_normal = add(marked_normal, defect)
        # Symbolic row order is (reduced Eq coefficient of F=H0-u,
        # target coefficient of Y*w).  Root decoration is coefficientwise.
        old_cone = tuple((-2 * value, -2 * value) for value in defect)
        desired = tuple((Q(0), -2 * value) for value in defect)
        residual = tuple((left_pair[0] - right_pair[0],
                          left_pair[1] - right_pair[1])
                         for left_pair, right_pair in
                         zip(old_cone, desired, strict=True))
        require(all(pair == (-2 * value, Q(0))
                    for pair, value in zip(residual, defect, strict=True)),
                "one-root reduced-Eq conormal changed")
        records.append({
            "sites": [left, right],
            "target_correction": "-2*D_xt*Y*w",
            "canonical_cone_Eq_face": "-2*D_xt*(H0-u)*Eq",
            "required_next_correction": "+2*D_xt*(H0-u)*Eq",
        })

    # The exact even preimage has target normal N_v from the preceding gate.
    centered = target.centered_preimage_normal_audit()
    primitive_sparse = centered["primitive_target_normal"]
    primitive = tuple(Q(primitive_sparse.get("".join(map(str, word)), "0"))
                      for word in target.TARGET_WORDS)
    require(any(primitive), "the centered primitive normal vanished")
    formal_filler = tuple((-value, -value) for value in primitive)
    desired = tuple((Q(0), -value) for value in primitive)
    residual = tuple((left_pair[0] - right_pair[0],
                      left_pair[1] - right_pair[1])
                     for left_pair, right_pair in
                     zip(formal_filler, desired, strict=True))
    require(all(pair == (-value, Q(0))
                for pair, value in zip(residual, primitive, strict=True)),
            "centered reduced-Eq conormal changed")
    mixed_dual = target.target_unit((0, 0, 1, 1))
    require(dot(mixed_dual, primitive) == 2,
            "the centered Eq residual lost its primitive mixed detector")
    return {
        "Cartan_identity": (
            "dC2+=-2D - R2+, where "
            "R2+=-1/2(1+S)H_w d(P2(I))"
        ),
        "root_residuals": records,
        "canonical_two_row_projection": {
            "row_order": ["(H0-u)*Eq", "Y*w target"],
            "known_target_cone": ["-2D", "-2D"],
            "desired": ["0", "-2D"],
            "first_residual": ["-2D", "0"],
            "required_correction": "+2D*(H0-u)*Eq",
            "scope": (
                "this is the first residual of the known canonical "
                "target-cone filler, not a computation of the literal "
                "R2+ image before P2/iota is constructed"
            ),
        },
        "exact_centered_preimage": {
            "primitive_target_normal": primitive_sparse,
            "first_Eq_residual": "-N_v^prim*(H0-u)*Eq",
            "required_correction": "+N_v^prim*(H0-u)*Eq",
            "mixed_dual_value": 2,
        },
        "formal_residual_zero": False,
        "actual_R2_literal_reduced_Eq_value": "undefined before P2/iota",
    }


def physical_scope_audit():
    generic = (ROOT / (
        "notes/h3-generic-cartan-adjacent-target-label-prolongation.md"
    )).read_text()
    master = (ROOT / (
        "notes/h3-reduced-eq-integral-rho-comparison-master-gate.md"
    )).read_text()
    cylinder = (ROOT / (
        "notes/h3-selected-lower-quiver-kahler-mapping-cylinder-gate.md"
    )).read_text()
    shared = (ROOT / "notes/h2-b4-cplus-shared-interface-gate.md").read_text()
    require("source-labelled shifted comparison" in generic
            and "R_+=" in generic,
            "generic J* typing scope changed")
    require("canonical reduced-Eq Koszul core" in master
            and "one rho-equivariant" in master,
            "integral reduced-Eq comparison scope changed")
    require("dC=-e" in cylinder
            and "=+2D(H_0-u)" in cylinder,
            "mapping-cylinder reduced-Eq sign changed")
    require("B-4" in shared and "one-endpoint product-rule" in shared,
            "shared lower C-plus interface changed")
    return {
        "constructed_unconditionally": (
            "the h2 J*=-2 alpha beta I diagonal input, its parameter-free "
            "normalized Cartan formula, and the exact target/Eq residual"
        ),
        "constructed_conditionally": (
            "on alpha*beta!=0 and after the shifted source-labelled P2/iota, "
            "C2+ cancels every root-decorated even B target"
        ),
        "first_unavoidable_obstruction": (
            "the physical placement of P2(I) in the occurrence-local 0112 "
            "word/fine/repeated grade; the first known canonical cone "
            "candidate then requires the root-decorated reduced-Eq cell "
            "+2D(H0-u)Eq"
        ),
        "canonical_core_available": (
            "K_Eq with dK_Eq=(H0-u)Eq exists in the derived source"
        ),
        "physical_comparison_missing": (
            "the rho-even/root-decorated occurrence-local image of K_Eq, "
            "including lower landing, labelled residue, protected rows, "
            "and physical q"
        ),
        "beta_zero_scope": (
            "the normalized formula is not a regular construction at "
            "beta=0; the collision/unary branch remains separate"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "h2 lower even Cartan Jstar target-cone gate",
        "pins": PINS,
        "h2_diagonal_input": h2_jstar_audit(),
        "per_root_target_cancellation": per_root_target_cancellation_audit(),
        "internal_even_Cartan_no_go": even_cartan_internal_no_go_audit(),
        "first_principal_parts_residual":
            first_principal_parts_residual_audit(),
        "physical_scope": physical_scope_audit(),
        "verdict": (
            "At order two the generic diagonal combination is exactly "
            "J*=-2 alpha beta I.  Conditional on the source-labelled P2/iota, "
            "the parameter-free cell C2+=-1/2(1+S)H_wP2(I) cancels the "
            "natural +2(w-1)Delta target of every endpoint-even B edge.  "
            "No correction inside the old two-column Cartan orbit does so "
            "without becoming odd.  The exact first residual is "
            "R2+=-1/2(1+S)H_wd(P2(I)).  The known canonical target-cone "
            "candidate separately retains -2D(H0-u)Eq and needs the "
            "independent +2D(H0-u)Eq comparison; the literal value of R2+ "
            "cannot be identified with it before P2/iota.  Thus the target cone is "
            "formally constructed on the generic open, while physical "
            "occurrence placement and the regular beta-zero extension remain."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("h2 even Cartan Jstar ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h2 J*: -2 alpha beta I; normalized C2+: -1/2 even trace prism")
    print("even B target vs J* cone: EXACT CANCELLATION AFTER P2/IOTA")
    print("first residual: R2+=-1/2(1+S)H_w d(P2(I))")
    print("known cone candidate: needs +2D(H0-u)Eq")
    print("physical occurrence placement / beta-zero extension: OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
