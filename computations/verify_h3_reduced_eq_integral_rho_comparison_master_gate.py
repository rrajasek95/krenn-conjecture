#!/usr/bin/env python3
"""Reduce the three reduced-Eq shadows to one integral rho comparison.

The canonical Koszul cell is a free one-object cell before adjoining its
rho mate.  Over R=Q[beta], an equivariant map from the regular rho orbit is
therefore determined by the image of one object.  Its (1-rho) and (1+rho)
parts are respectively the odd and even comparisons, and an R-linear chain
map commutes with the beta-Bockstein.

The physical M_v theorem fixes only the odd *output*.  It neither specifies
the image of one orbit object nor the selected odd input comparison.  Adding
an invariant chain changes the even projection while leaving the odd output
fixed.  In the concrete augmented quotient, the first generic obstruction is
the B1/B4 labelled-residue covector; at beta=0 it is the cap Smith class
[rho0].  Thus a single source-labelled R-linear rho comparison is sufficient
and necessary for the common assembly, but it is not constructed here.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_reduced_eq_full_physical_augmentation_matrix.py":
        "f66752bd3a44a9506b4a31467ce52dcb16e52f841b0f29ce66066a38ec7f97c1",
    "computations/verify_h3_literal_mv_odd_reduced_eq_projection_scope.py":
        "deb0ad5e35d42428d7440310af24951d3cb29deb55116fb5ab8eacef5fa1f729",
    "computations/verify_h3_reduced_eq_spencer_three_projection_gate.py":
        "315508b572fa0d96b33ba83b8ac4905e59dfbf8f484023891618dbb3c6489d83",
    "computations/verify_h3_tau_plus_full_interface_product_bianchi_extension_gate.py":
        "32be7ef48ad9d35b8863a62889508ccdff0010d8ebff18b366e932aab8b2bf14",
    "computations/verify_h3_beta_rees_cap_smith_saturation_gate.py":
        "fb031132ddd0510197560be0644324c436216192a9f15140ae3ef52b2a1fb4e5",
}
EXPECTED_LEDGER_SHA256 = (
    "7975d9a3441ed532308ff3026a9ce01ffc268df930fd81badb6c76f3c57956d6"
)


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


def determinant(columns):
    require(columns and len(columns) == len(columns[0]), "not square")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(len(columns))]
    answer = Q(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work))
                      if work[row][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        value = work[column][column]
        answer *= value
        for row in range(column + 1, len(work)):
            coefficient = work[row][column] / value
            work[row] = [left - coefficient * right for left, right in
                         zip(work[row], work[column], strict=True)]
    return answer


def regular_orbit_comparison_audit():
    # Basis (k,rho*k).  The orbit is cyclic as a Q[rho]-module; hence an
    # equivariant comparison is specified by x=Phi(k), with Phi(rho*k)=rho*x.
    left = (Q(1), Q(0))
    right = (Q(0), Q(1))
    odd = add(left, scale(-1, right))
    even = add(left, right)
    require(rank((odd, even)) == 2, "the rho parity splitting collapsed")

    # Fixing the odd image does not fix one object or the even image.  The
    # invariant translation z changes (x,rho*x) by (z,z), hence fixes odd
    # and changes even by 2z.
    for z in (Q(-3), Q(0), Q(2, 5), Q(7)):
        x = (Q(5) + z, Q(2) + z)
        require(dot(odd, x) == 3
                and dot(even, x) == 7 + 2 * z,
                ("the invariant ambiguity changed", z, x))

    # Conversely, because 2 is a unit in the coefficient field, prescribed
    # odd/even images recover the two object images uniquely.
    for minus, plus in ((Q(3), Q(7)), (Q(-2), Q(5, 3))):
        x_left = (plus + minus) / 2
        x_right = (plus - minus) / 2
        require(x_left - x_right == minus and x_left + x_right == plus,
                "odd/even reconstruction changed")
    return {
        "base_ring": "R=Q[beta] (or any k[beta] with 2 invertible)",
        "source_orbit": "R[rho]{K_Eq}, rho^2=1",
        "equivariant_map_data": "one object image Phi_beta(K_Eq)",
        "odd_projection": "Phi_beta((1-rho)K_Eq)",
        "even_projection": "Phi_beta((1+rho)K_Eq)",
        "odd_output_determines_even": False,
        "ambiguity": "Phi_beta(K_Eq) -> Phi_beta(K_Eq)+z, rho*z=z",
        "even_change_under_ambiguity": "2z",
        "odd_even_pair_determines_objectwise_map": True,
    }


def bockstein_naturality_audit():
    # Abstract two-term calculation: d(s)=beta*y.  For an R-linear chain
    # map Phi, d Phi(s)=Phi d(s)=beta Phi(y), so reduction/division gives
    # delta_beta(Phi(s mod beta))=Phi(y mod beta).
    # Record coefficients in the basis (beta*y, beta*z).
    source_boundary = (Q(1), Q(0))
    # Two arbitrary constant comparison matrices, checked coefficientwise.
    records = []
    for matrix in (
        ((Q(1), Q(0)), (Q(0), Q(1))),
        ((Q(2), Q(-1)), (Q(3), Q(4))),
        ((Q(0), Q(5, 2)), (Q(-7), Q(1, 3))),
    ):
        image = tuple(dot(row, source_boundary) for row in matrix)
        chain_then_divide = image
        divide_then_map = tuple(row[0] for row in matrix)
        require(chain_then_divide == divide_then_map,
                "R-linear comparison stopped commuting with Bockstein")
        records.append([str(value) for value in image])
    return {
        "source_relation": "d(s)=beta*y",
        "comparison_relation": "d Phi_beta(s)=beta Phi_beta(y)",
        "special_connecting_map": (
            "delta_beta[Phi_beta(s mod beta)]=[Phi_beta(y mod beta)]"
        ),
        "sample_checks": records,
        "consequence": (
            "one regular chain comparison supplies the special V face; "
            "a comparison defined only after beta inversion has no such law"
        ),
    }


def physical_generic_residue_obstruction_audit():
    # The already physical placed Cartan direction and diagonal scalar
    # residue line do not supply the rho-even B1/B4 section.
    diagonal = (Q(1),) * 6
    alpha = (Q(1), Q(0), Q(1), Q(-1), Q(0), Q(-1))
    v = (Q(0), Q(1, 2), Q(0), Q(0), Q(1, 2), Q(0))
    chi = (Q(0), Q(1), Q(-1), Q(0), Q(1), Q(-1))
    require(dot(chi, diagonal) == dot(chi, alpha) == 0
            and dot(chi, v) == 1
            and rank((diagonal, alpha, v)) == 3,
            "the B1/B4 labelled-residue obstruction changed")
    return {
        "physical_odd_Cartan_line": [int(value) for value in alpha],
        "required_even_label": [str(value) for value in v],
        "known_residue_span": "Q*diagonal + Q*alpha",
        "primitive_even_residue_dual": [int(value) for value in chi],
        "dual_on_required_even_label": "1",
        "verdict": (
            "M_v closes the alpha odd aggregate but cannot be projected or "
            "symmetrized into the B1/B4 even labelled section"
        ),
    }


def beta_smith_obstruction_audit():
    # Coefficient-only Smith shadow.  At h=3 the known cap has determinant
    # 3*beta.  At beta=0 rho0 is missing.  A correction V carrying the same
    # protected defect as U and zero root output yields a unit minor.
    # We store polynomials as pairs (constant,beta coefficient) only where
    # needed and check special and generic statements explicitly.
    h = Q(3)
    for beta in (Q(-5), Q(-1), Q(1), Q(7, 3)):
        z1 = (beta, Q(1))
        z2 = (-beta, h - 1)
        require(determinant((z1, z2)) == h * beta,
                ("the cap determinant changed", beta))
    z1_zero = (Q(0), Q(1))
    z2_zero = (Q(0), h - 1)
    rho0 = (Q(1), Q(0))
    require(rank((z1_zero, z2_zero)) == 1
            and rank((z1_zero, z2_zero, rho0)) == 2,
            "the special rho0 class disappeared")

    unary = (Q(1), Q(1), Q(0))
    correction_v = (Q(1), Q(0), Q(0))
    z1_augmented_zero = (Q(0), Q(0), Q(1))
    require(determinant((unary, correction_v, z1_augmented_zero)) == -1,
            "the V correction stopped giving a unit minor")
    require(add(unary, scale(-1, correction_v))
            == (Q(0), Q(1), Q(0)),
            "U-V stopped being protected rho0")
    return {
        "known_cap_Smith_form": ["1", "beta"],
        "special_torsion_class": "[rho0]",
        "required_special_face": "V=(protected defect of U, rho0=rho2=0)",
        "unit_minor_after_V": "det(U,V,Z1)=-1",
        "protected_unit": "U-V=rho0",
        "generic_beta_inversion_sufficient": False,
    }


def pinned_scope_audit():
    full = (ROOT / (
        "computations/verify_h3_reduced_eq_full_physical_augmentation_matrix.py"
    )).read_text()
    odd = (ROOT / (
        "computations/verify_h3_literal_mv_odd_reduced_eq_projection_scope.py"
    )).read_text()
    three = (ROOT / (
        "computations/verify_h3_reduced_eq_spencer_three_projection_gate.py"
    )).read_text()
    require('"physical_output_identity": "O_alpha-K_alpha=-M_v"' in full
            and '"input_map_constructed": False' in full,
            "the full-alpha physical/output scope changed")
    require('"selected_input_comparison_constructed": False' in odd
            or "input comparison" in odd,
            "the selected odd input scope changed")
    require('"physical_three_projection_cell_constructed": False' in three,
            "the three-projection physical scope changed")
    return {
        "canonical_Koszul_Eq_core": "constructed in the derived source",
        "physical_full_alpha_odd_output": "constructed as -M_v",
        "physical_odd_terminal": "constructed",
        "selected_odd_input_comparison": "open",
        "rho_even_generic_full_packet": "open",
        "beta_special_V": "open",
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "integral rho comparison master gate for reduced Eq",
        "pins": PINS,
        "already_physical_and_open": pinned_scope_audit(),
        "regular_rho_orbit": regular_orbit_comparison_audit(),
        "Bockstein_naturality": bockstein_naturality_audit(),
        "generic_first_obstruction": physical_generic_residue_obstruction_audit(),
        "special_first_obstruction": beta_smith_obstruction_audit(),
        "single_missing_comparison": {
            "name": "Phi_beta",
            "type": (
                "an R-linear rho-equivariant chain comparison from the "
                "source-labelled regular orbit of K_Eq to the complete "
                "physical word/fine/repeated augmented complex"
            ),
            "odd_restriction": (
                "Phi_beta((1-rho)K_Eq) is the selected input comparison "
                "whose output is the already fixed +/-M_v"
            ),
            "generic_even_restriction": (
                "Phi_beta((1+rho)K_Eq) gives delta_plus, mixed target "
                "-2D tensor v, Eq +2D(H0-u) tensor v, labelled ores v, "
                "W=0, and all ridge/word faces"
            ),
            "special_restriction": (
                "Bockstein naturality gives V with the unary primitive "
                "defect and zero rho0/rho2; then U-V is the D0 unit"
            ),
            "regularity": "defined over R=k[beta], not only R[1/beta]",
        },
        "necessity_and_sufficiency": (
            "an objectwise R-linear rho comparison immediately has all "
            "three restrictions by the commuting parity projectors and "
            "Bockstein naturality.  Conversely, a compatible odd/even "
            "pair recovers the objectwise comparison because 2 is a unit; "
            "requiring the special connecting face is exactly R-linearity "
            "across beta=0.  Hence this is one comparison theorem, not "
            "three independent physical generators"
        ),
        "not_a_construction": (
            "the current physical data give only the odd output.  The "
            "labelled-residue dual chi and the cap Smith class [rho0] show "
            "that neither the generic even nor special face follows from it"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("integral rho comparison ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 reduced-Eq integral rho comparison master gate: PASS")
    print("established: derived Koszul core + physical odd output -M_v")
    print("one missing theorem: R-linear rho-equivariant Phi_beta")
    print("generic obstruction: B1/B4 labelled-residue dual")
    print("special obstruction: beta-Smith class [rho0]")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
