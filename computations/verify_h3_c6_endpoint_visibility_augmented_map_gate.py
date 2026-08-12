#!/usr/bin/env python3
"""Audit the augmented-map status of the canonical C6 z residual.

The fixed selected-port projection has a primitive occurrence-cokernel
separator.  It is not a terminal physical class: either of the first
legitimate word-changed endpoint columns pairs nontrivially with that
separator.  The complete physical object is instead the full endpoint
Jacobian, whose entries depend on every endpoint component and every
common-q cofactor and are not determined by the selected skeleton.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_c6_first_transgression_selected_port_boundary.py":
        "8729c85d5af458966942e567e5e840da9fe0acf0a9d89684b846bee82b791f9a",
    "notes/h3-c6-first-transgression-selected-port-boundary.md":
        "03bed57e2a1955795806b590e586c16e3a25948e719ff1d589a462460a8684b1",
    "computations/verify_h3_c6_z_spoke_hole_koszul_boundary.py":
        "85814705ad28631cccc13728f216adcbfc4ee94f65a01846e187253497fc5bfe",
    "notes/h3-c6-z-spoke-hole-koszul-boundary.md":
        "b0f80125431d59e5f393986161136f77c7e0d0db2401c0ca6c9298e5a46f720e",
    "computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py":
        "f24e9bd69ec4baef96104557571c154b399f87f34074edffda27e551f33c2205",
    "notes/uniform-multisite-endpoint-affine-hall-concentration-boundary.md":
        "241b46d9ecede656aa59f2be6d74bc288fbada2aa4843103a950441066763df2",
    "computations/verify_uniform_axis_circuit_third_component_rank_guard.py":
        "d9e852bad1b94c1918523fa834029abff04f4c288bde2f97c790def1bef2644f",
    "notes/uniform-axis-circuit-third-component-rank-guard.md":
        "f5d3e295bf86baff08c9afbae0e404b93bd7b73c56f919a085488028de3751dd",
    "computations/verify_uniform_axis_circuit_target_coloop_full_five_boundary.py":
        "4e84ec46bac4b9b97a69dbfa61899877c5b09f3960bf666af1ddf1ade01c54d6",
    "notes/uniform-axis-circuit-target-coloop-full-five-boundary.md":
        "865dbad8ccc90be052e78acbf839d32ca18e07802ce13862bbfccb1264baa8d9",
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "notes/uniform-five-lock-wedge-or-switch.md":
        "0871d5151a0fdb46fee0c9b15797a864e579a85c360a2638d458583479426914",
    "computations/verify_uniform_multisite_hall_k22_effective_hole_m3_boundary.py":
        "987c702e6f056cd5715ad2df95b680100aee4b168c4359b2300eaf7022370695",
    "notes/uniform-multisite-hall-k22-effective-hole-m3-boundary.md":
        "5df738886b3f6cdb84112abc99f35bc91b3a3e28cf820f01344cef8df90300ea",
}
EXPECTED_LEDGER_SHA256 = "ab0dc482dc78f11ee794c564e349da7c15f894f8b12e3bcb6d8ea2cc1b1f4ebf"

M = ((0, 1), (2, 3), (4, 5))
N = ((0, 5), (1, 2), (3, 4))
ANCHOR = (
    ((0, 1), (2, 4), (3, 5)),
    ((0, 2), (1, 3), (4, 5)),
    ((0, 2), (1, 4), (3, 5)),
    ((0, 2), (1, 5), (3, 4)),
    ((0, 5), (1, 3), (2, 4)),
    ((0, 5), (1, 4), (2, 3)),
)
BASIS = (M, N) + ANCHOR
INDEX = {matching: index for index, matching in enumerate(BASIS)}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def vector(*terms):
    answer = [0] * len(BASIS)
    for matching, coefficient in terms:
        answer[INDEX[matching]] += coefficient
    return answer


def rank(columns):
    if not columns:
        return 0
    matrix = [[Fraction(column[row]) for column in columns]
              for row in range(len(columns[0]))]
    rows = len(matrix)
    cols = len(matrix[0])
    pivot_row = 0
    for column in range(cols):
        pivot = next((row for row in range(pivot_row, rows)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right
                           for left, right in zip(matrix[row],
                                                  matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def audit_missing_coordinate_kernel_no_go():
    """A missing-coordinate kernel value need not give support descent."""
    # Complete response columns for three endpoint coordinates.  The first
    # two are occupied and independent; the third (the prospective
    # word-changed coordinate) is response-invisible.
    columns = ([1, 1], [0, -1], [0, 0])
    source = [1, 1, 0]
    target = [sum(coefficient * column[row]
                  for coefficient, column in zip(source, columns))
              for row in range(2)]
    missing_kernel = [0, 0, 1]

    require(target == [1, 0], "the affine guard lost its pure target")
    require(rank(list(columns)) == 2,
            "the affine guard complete-column rank changed")
    require(all(sum(coefficient * column[row]
                    for coefficient, column in zip(missing_kernel, columns))
                == 0 for row in range(2)),
            "the missing coordinate stopped being a kernel direction")
    require(missing_kernel[2] == 1,
            "the missing-coordinate readout stopped detecting the kernel")

    # Every point of the affine fibre is (1,1,t).  Its two occupied
    # coordinates are fixed and nonzero, so no point is supported on a
    # coordinate line and the kernel cannot delete an occupied component.
    require(source[0] == source[1] == 1
            and missing_kernel[0] == missing_kernel[1] == 0,
            "the affine fibre unexpectedly moves occupied support")
    return {
        "complete_columns": columns,
        "source_point": source,
        "target": target,
        "kernel_generator": missing_kernel,
        "missing_readout_on_kernel": 1,
        "affine_fibre": "(1,1,t)",
        "coordinate_line_intersection": False,
        "support_reducing_kernel_direction": False,
    }


def audit_conditional_sequential_potential():
    """Verify the exact well-founded part of the conditional interface."""
    checked = 0
    for support in range(1, 9):
        for components in range(1, 9):
            state = (support, components)
            if support > 1:
                kernel_move = (support - 1, components + 7)
                require(kernel_move < state,
                        "a support contraction stopped decreasing lex order")
                checked += 1
            if components > 1:
                exchange_move = (support, components - 1)
                require(exchange_move < state,
                        "a typed exchange stopped decreasing lex order")
                checked += 1
    return {
        "potential": "(endpoint support, unresolved typed components)",
        "kernel_move": "strictly lowers endpoint support; later coordinates arbitrary",
        "typed_exchange": "preserves support and lowers unresolved components",
        "four_good_or_unit": "terminal",
        "checked_finite_states": 8 * 8,
        "checked_decreasing_moves": checked,
        "excluded_nondecreasing_moves": [
            "bare effective-hole reselection",
            "unlanded Fitting carrier",
            "missing-coordinate-only kernel variation",
        ],
    }


def audit_occurrence_quotient():
    # After the seven external-offdiagonal routes, the unary z row is the
    # all-one relation on M,N and the six anchor-contained competitors.
    unary = [1] * len(BASIS)
    residual = vector((M, 1), (N, 1))

    # The unique primitive separator invariant under M<->N and permutation
    # of the six competitors.
    separator = [3, 3] + [-1] * len(ANCHOR)
    require(dot(separator, unary) == 0,
            "the symmetric separator stopped killing the unary row")
    require(dot(separator, residual) == 6,
            "the symmetric separator stopped detecting the C6 residual")
    require(rank([unary]) == 1 and rank([unary, residual]) == 2,
            "the frozen selected-port cokernel changed")

    # If p1@0:0 is present with the selected s1@1:1 component, the G11[z]
    # hole-01 coefficient has tails 23|45, 24|35, 25|34.  The last is an
    # already-routed external-offdiagonal matching, so its quotient column
    # is M + (01|24|35).
    g11_hole01 = vector((M, 1), (ANCHOR[0], 1))

    # If p2@3:1 is present with selected s1@1:1, the G21[z] hole-13
    # coefficient has tails 02|45, 04|25, 05|24.  The middle tail routes,
    # leaving the two displayed anchor-contained matching classes.
    g21_hole13 = vector((ANCHOR[1], 1), (ANCHOR[4], 1))

    require(dot(separator, g11_hole01) == 2,
            "the G11 word-change column became separator-invisible")
    require(dot(separator, g21_hole13) == -2,
            "the G21 word-change column became separator-invisible")
    require(rank([unary, g11_hole01, g21_hole13]) == 3,
            "the two word-change columns lost independence")

    return {
        "basis": BASIS,
        "unary_column": unary,
        "residual": residual,
        "selected_projection_rank": rank([unary]),
        "selected_projection_augmented_rank": rank([unary, residual]),
        "primitive_symmetric_separator": separator,
        "separator_on_residual": dot(separator, residual),
        "word_change_columns": {
            "G11_hole01_p1_0_0": g11_hole01,
            "G21_hole13_p2_3_1": g21_hole13,
        },
        "separator_on_word_change_columns": {
            "G11_hole01_p1_0_0": dot(separator, g11_hole01),
            "G21_hole13_p2_3_1": dot(separator, g21_hole13),
        },
        "rank_with_both_word_change_columns": rank(
            [unary, g11_hole01, g21_hole13]
        ),
    }


def main():
    for relative, expected in PINS.items():
        actual = file_sha256(ROOT / relative)
        require(actual == expected,
                f"dependency changed: {relative}: {actual} != {expected}")

    ledger = {
        "occurrence_quotient": audit_occurrence_quotient(),
        "missing_coordinate_kernel_no_go":
            audit_missing_coordinate_kernel_no_go(),
        "conditional_sequential_potential":
            audit_conditional_sequential_potential(),
        "complete_physical_map": {
            "domain": "E_p1+E_p2+E_s1+E_s2 (all 72 endpoint coordinates)",
            "map": (
                "J_A(dp,ds)_(ij,w) = "
                "[dp_i*s_j*q^[2] + p_i*ds_j*q^[2]]_w, "
                "for all i,j in {1,2} and all w in {0,1,2}^6"
            ),
            "codomain_dimension": 4 * (3 ** 6),
            "distinguished_coordinate_readouts": [
                "epsilon(p1@0:0)", "epsilon(p2@3:1)"
            ],
            "canonical_vector_readout": (
                "q_z=(epsilon(p1@0:0),epsilon(p2@3:1)); the six-base "
                "aggregate selects no canonical scalar projection"
            ),
            "kernel_scope": (
                "a nonzero q_z value on ker(J_A) only varies a missing "
                "coordinate.  Descent requires an anchor-safe affine "
                "translation with strictly smaller support or an affine "
                "coordinate-line hit"
            ),
            "scope": (
                "the unary q^[3] block is unchanged by endpoint-only "
                "corrections; anchor safety is an additional readout"
            ),
        },
        "verdict": (
            "the displayed selected-port occurrence separator is not "
            "stable under the first legitimate full-source word-change "
            "columns.  It "
            "is therefore a missing-column/affine-Fitting gate, not a "
            "physical B/C terminal class"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"endpoint visibility augmented-map ledger changed: {digest}")
    print("h3 C6 endpoint-visibility augmented-map gate: PASS")
    print("selected occurrence quotient: rank 1; residual raises rank to 2")
    print("primitive separator values on G11/G21 word-change columns: 2/-2")
    print("missing-coordinate kernel detection does not imply support descent")
    print("verdict: missing complete columns, not a B/C terminal class")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
