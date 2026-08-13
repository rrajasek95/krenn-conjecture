#!/usr/bin/env python3
"""Audit the all-h raw sum-channel target and activity-Hankel obstruction.

The checker proves two finite algebraic statements.

* The unique division-free extrapolation of the h=3 sum-channel row is

      2(h-1) Theta_h + chi_h (2 M0 - MH - MG) = 0,

  because 2M0-MH-MG=-(h-1)(KH+KG).  In the exact integral selector
  guard its assignment-sum class is 2(h-1), and the known Euler row
  carries it as (low,bad)=(c,-c).  The isolated low class has a primitive
  dual and is not in that row span.

* Once the selector and clean binary lines and a volume form are granted,
  the Cartan product of the selector quadratic with the activity covariant
  is the only natural bilinear top-order candidate.  On the pure-axis
  clean space its Macaulay shifts form the whole degree-(2h-1) space.
  Thus a correction using only the same colon quadratic, activity
  covariant, and parameter scalars can satisfy the Hankel equations only
  by cancelling the candidate to zero.

The paired note proves the identities for all h.  Bounded exact loops here
audit signs, ranks, and coefficients; they do not assert a physical source.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/adjacent_full_nine_h3_cycle_transgression.md":
        "492a5a36c580b388dc0301727caf37b34a4448f2ab6bf63402d131a11d97fbbb",
    "computations/verify_adjacent_full_nine_h3_cycle_transgression.py":
        "13b4226fe558536005478bf929b7962c259f55891cb1a88f2628d4f483cb6717",
    "notes/two-chart-selector-provenance-sum-channel-guard.md":
        "579423e82302cf06155133cad1085875f2dbdc99401324fd833db3d2e5c4c3c5",
    "computations/verify_two_chart_selector_provenance_sum_channel_guard.py":
        "41f41b0f5d32075adea679b0c1be15e46c4ee23844823ed38db75be477f6a9a7",
    "notes/uniform_adjacent_cycle_filtered_prolongation.md":
        "90926cce63f1dec2a6fe62900afa0c29bea454d642c5b68b9791c5f87904f8bc",
    "computations/verify_uniform_adjacent_cycle_filtered_prolongation.py":
        "2b2555fac43a5914469a857b3a6bf19aa715ab6576220dc1dfd66dd808cad86e",
    "notes/full-27-colon-cycle-macaulay-transfer-gap.md":
        "b1bfb66a7078cbee813aaf1b2d9a4fca5094329bcfcfb76827a75388a1e0dbdf",
    "computations/verify_full_27_colon_cycle_guard.py":
        "3beaaee3cae98ef342f98ad9ffbbd5e26f83721b91d7efb2d36130065a637567",
    "notes/odd-covariant-filtered-hankel-naturality-obstruction.md":
        "2ce57e3a1b30366831333ffcbf7ff7a0210c0b9db40ce60c9c8d6318ed9010f9",
    "computations/verify_odd_covariant_filtered_hankel_naturality_obstruction.py":
        "14727acc7d03240ef74c058a9a13a919db6dfeb81af07be4087a7a0c2e1bd50b",
    "notes/h3-jd-hasse-bianchi-totalization-uniform-spectator-gate.md":
        "8704921ca24946c17703ea1f8f2c92f557d5028c7e44c9fb18faa2c99420bf52",
    "computations/verify_h3_jd_hasse_bianchi_totalization_uniform_spectator_gate.py":
        "0a67d93f795600e1f406598fb22a3c0e0de5a29b5120b371a8e42be8f32a5213",
}
EXPECTED_LEDGER_SHA256 = "b4a984f8100d44a46914b3be284fa61fb57c1feea5f18461ddcfb4f31b9ec3d1"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def matrix_add(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def matrix_scale(scalar, matrix):
    scalar = Fraction(scalar)
    return [[scalar * entry for entry in row] for row in matrix]


def matrix_subtract(left, right):
    return matrix_add(left, matrix_scale(-1, right))


def matrix_rank(matrix) -> int:
    if not matrix:
        return 0
    work = [list(map(Fraction, row)) for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [entry / pivot_value for entry in work[rank]]
        for row in range(rows):
            if row == rank or not work[row][column]:
                continue
            coefficient = work[row][column]
            work[row] = [
                entry - coefficient * pivot_entry
                for entry, pivot_entry in zip(
                    work[row], work[rank], strict=True
                )
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def omega_d(matrix) -> Fraction:
    # d=[[1,1],[1,2]], so omega_d(X)=X_01-X_10.
    return matrix[0][1] - matrix[1][0]


def sum_channel_audit() -> dict[str, object]:
    d = [[Fraction(1), Fraction(1)],
         [Fraction(1), Fraction(2)]]
    h_table = [[Fraction(0), Fraction(1)],
               [Fraction(0), Fraction(1)]]
    g_table = [row[:] for row in h_table]
    b_table = matrix_add(h_table, g_table)
    u = Fraction(0)
    k_h = matrix_subtract(matrix_scale(u, d), h_table)
    k_g = matrix_subtract(matrix_scale(u, d), g_table)

    records = {}
    for h in range(3, 11):
        m0 = matrix_add(matrix_scale(h, b_table), matrix_scale(u, d))
        mh = matrix_add(
            matrix_add(h_table, matrix_scale(h, g_table)),
            matrix_scale(h * u, d),
        )
        mg = matrix_add(
            matrix_add(matrix_scale(h, h_table), g_table),
            matrix_scale(h * u, d),
        )
        assignment_sum = matrix_subtract(
            matrix_subtract(matrix_scale(2, m0), mh), mg
        )
        curvature_sum = matrix_add(k_h, k_g)
        expected = matrix_scale(-(h - 1), curvature_sum)
        require(assignment_sum == expected,
                ("all-h sum-channel identity changed", h))

        selector_class = omega_d(assignment_sum)
        require(selector_class == 2 * (h - 1),
                ("selector sum class changed", h, selector_class))

        # The known associated-graded Euler object has its nonzero selector
        # class in opposite low/bad grades.  The proposed raw cut wants the
        # low component alone.
        known_total = [selector_class, -selector_class]
        desired_low = [selector_class, Fraction(0)]
        require(matrix_rank([known_total]) == 1
                and matrix_rank([known_total, desired_low]) == 2,
                ("grade-split class entered known row span", h))
        primitive_dual = [Fraction(1), Fraction(1)]
        require(sum(x * y for x, y in zip(
                    primitive_dual, known_total, strict=True)) == 0
                and sum(x * y for x, y in zip(
                    primitive_dual, desired_low, strict=True))
                == selector_class,
                ("grade-split primitive dual changed", h))

        records[h] = {
            "omega_assignment_sum": int(selector_class),
            "known_Euler_grade_pair": [
                int(known_total[0]), int(known_total[1])
            ],
            "desired_isolated_low": [
                int(desired_low[0]), int(desired_low[1])
            ],
            "known_rank": 1,
            "augmented_rank": 2,
        }

    # At h=3 and equal adjacent curvatures kappa_H=kappa_G=kappa,
    # 2(h-1)Theta + chi*S = 4(Theta-chi*kappa).
    h = 3
    theta_coefficient = 2 * (h - 1)
    equal_curvature_coefficient = -2 * (h - 1)
    require((theta_coefficient, equal_curvature_coefficient) == (4, -4),
            "h=3 transgression specialization changed")
    return {
        "division_free_candidate": (
            "2(h-1) F0_h PsiC_h + chiC_h (2M0-MH-MG) = 0"
        ),
        "equal_curvature_form": (
            "F0_h PsiC_h - chiC_h (kappa_H+kappa_G)/2 = 0"
        ),
        "h3_specialization": "4(F0 PsiC-chiC kappa)=0",
        "integral_guard": records,
        "first_source_membership": (
            "the isolated low assignment-sum class must be hit after its "
            "internal/direct/normal mate is killed; the universal Euler "
            "packet contains only the paired (low,-bad) total"
        ),
    }


def poly_multiply(left, right):
    result = [Fraction(0) for _ in range(len(left) + len(right) - 1)]
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            result[i + j] += left_value * right_value
    return result


def poly_power(polynomial, exponent):
    result = [Fraction(1)]
    for _ in range(exponent):
        result = poly_multiply(result, polynomial)
    return result


def activity_hankel_audit() -> dict[str, object]:
    records = {}
    for h in range(3, 11):
        # Off-diagonal canonical line: s=u+2v and all three kappas=v.
        activity = poly_power([Fraction(1), Fraction(2)], 2 * h - 6)
        activity = [Fraction(0)] * 3 + activity
        require(len(activity) == 2 * h - 2 and any(activity),
                ("activity degree/nonzero changed", h))

        # Use the highest-weight selector quadratic u^2.  Its Cartan product
        # simply appends two u-degrees, so coefficients in v-degree are the
        # same list, now interpreted in degree 2h-1.
        theta = activity + [Fraction(0), Fraction(0)]
        require(len(theta) == 2 * h and any(theta),
                ("Cartan activity candidate changed", h))

        # For E_h=<u^h,v^h>, the h shifts of u^h occupy v-degrees 0..h-1
        # and those of v^h occupy h..2h-1.  The Macaulay matrix is a
        # permutation of the identity, hence the residual is theta.
        macaulay = [
            [Fraction(int(row == column)) for column in range(2 * h)]
            for row in range(2 * h)
        ]
        require(matrix_rank(macaulay) == 2 * h,
                ("pure-axis Macaulay rank changed", h))
        residual = [
            sum(row[column] * theta[column]
                for column in range(2 * h))
            for row in macaulay
        ]
        require(residual == theta and any(residual),
                ("activity candidate unexpectedly passed Hankel", h))

        # The top Sym^(2h-1) summand occurs with multiplicity one in
        # Sym^2 tensor Sym^(2h-3): its highest weight can only arise from
        # the unique tensor of the two highest-weight vectors.
        target_weight = 2 * h - 1
        auxiliary_degree = 2 * h - 3
        highest_weight_pairs = []
        for i in range(3):
            for j in range(auxiliary_degree + 1):
                weight = (2 - 2 * i) + (auxiliary_degree - 2 * j)
                if weight == target_weight:
                    highest_weight_pairs.append((i, j))
        require(highest_weight_pairs == [(0, 0)],
                ("top Cartan multiplicity changed", h, highest_weight_pairs))

        # Any natural bilinear "correction" formed from the same selector
        # quadratic, the same activity covariant, and scalar colon data is
        # c*theta.  theta+c*theta is Hankel only for c=-1, which kills its
        # required nonzero normalization.
        viable_scalars = []
        for correction in range(-4, 5):
            corrected = [
                (1 + correction) * coefficient for coefficient in theta
            ]
            if not any(corrected):
                viable_scalars.append(correction)
        require(viable_scalars == [-1],
                ("same-input correction alternatives changed", h,
                 viable_scalars))

        records[h] = {
            "activity_degree": 2 * h - 3,
            "terminal_degree": 2 * h - 1,
            "pure_axis_Macaulay_rank": 2 * h,
            "candidate_residual_nonzero": True,
            "top_Cartan_multiplicity": len(highest_weight_pairs),
            "only_same_input_Hankel_correction": -1,
            "corrected_terminal_is_nonzero": False,
        }
    return {
        "orders": records,
        "bare_colon_activity_correction": "cannot retain nonzero terminal",
        "reason": (
            "the top Cartan product is the unique natural bilinear output; "
            "static colon companions are clean-parameter scalars, and the "
            "pure-axis Macaulay map is injective"
        ),
        "first_positive_extra_datum": (
            "an independent source-derived auxiliary/covariant or a direct "
            "filtered transfer Tr_h whose image obeys every common Hankel "
            "shift; its source-boundary invariance must also be proved"
        ),
    }


def scope_audit() -> dict[str, object]:
    uniform = (ROOT / (
        "notes/uniform_adjacent_cycle_filtered_prolongation.md"
    )).read_text()
    sum_guard = (ROOT / (
        "notes/two-chart-selector-provenance-sum-channel-guard.md"
    )).read_text()
    transgression = (ROOT / (
        "notes/adjacent_full_nine_h3_cycle_transgression.md"
    )).read_text()
    full27 = (ROOT / (
        "notes/full-27-colon-cycle-macaulay-transfer-gap.md"
    )).read_text()
    spectator_faces = (ROOT / (
        "notes/h3-jd-hasse-bianchi-totalization-uniform-spectator-gate.md"
    )).read_text()
    require(r"\operatorname {pr}_{\rm bad}{\mathscr X}_h=dB_h"
            in uniform
            and r"\mu_{\mathcal E_h}^*(\Theta_h)=0" in uniform,
            "uniform target formulas changed")
    require("2M_0-M_H-M_G=-(h-1)(K_H+K_G)" in sum_guard,
            "general-h sum-channel identity changed")
    require(r"F_0\Psi_C={\chi_C\over2}(\kappa_H+\kappa_G)"
            in transgression,
            "h=3 sum-channel target changed")
    require(r"\operatorname {Tr}_h:" in full27
            and "source compatibility is the remaining" in full27,
            "colon-to-Hankel transfer status changed")
    require(r"d(TJ_D)=T\,dJ_D+(dT)J_D" in spectator_faces
            and "The second term is already nonzero" in spectator_faces
            and "one spectator" in spectator_faces,
            "the first spectator Hasse-face obstruction changed")
    return {
        "raw_all_h_row_constructed": False,
        "all_h_candidate_formula_is_forced": True,
        "first_obstruction_is_source_membership_not_scalar_arithmetic": True,
        "h3_suspension_first_extra_face": "(dT)J_D at h=4",
        "activity_Hankel_cut_constructed": False,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "uniform grade-split sum-channel and activity Hankel gate",
        "pins": PINS,
        "scope": scope_audit(),
        "sum_channel": sum_channel_audit(),
        "activity_hankel": activity_hankel_audit(),
        "verdict": (
            "The exact all-h raw-cut target is formulated, but it is not a "
            "consequence of the universal Bianchi/Euler packet.  Its first "
            "source obstruction is the nonzero isolated assignment-sum "
            "class in the selector quotient tensored with the low/bad grade "
            "cokernel.  The activity covariant cannot be repaired "
            "nontrivially by the existing colon cycle alone; a new "
            "source-derived common-Hankel transfer/covariant is required."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("uniform sum/Hankel ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("all-h sum-channel formula: FORCED TARGET, NOT CONSTRUCTED")
    print("first raw-cut obstruction: ISOLATED SELECTOR/GRADE CLASS")
    print("activity plus existing colon cycle: HANKEL NO-GO")
    print("next positive datum: PHYSICAL Tr_h OR INDEPENDENT AUXILIARY")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
