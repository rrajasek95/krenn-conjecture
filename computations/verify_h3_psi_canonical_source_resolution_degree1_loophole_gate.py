#!/usr/bin/env python3
"""Separate canonical source-resolution exhaustiveness from physical descent.

At the fixed Gamma_* grade, the coefficient-equation/Macaulay/PP grammar
has a canonical finite free presentation.  Once its degree-one map d1 is
fixed, ordinary C2 and higher syzygies land in ker(d1) and cannot enlarge
im(d1) or change a chi-annihilator.  This checker verifies that statement on
the exact rank-seven B/Eq cap presentation and a redundant C2/C3 resolution.

The remaining loophole is relative degree one: a physical response-to-cap
comparison, or a shifted mapping-cone cell, can have zero canonical source
shadow and a new B/Eq output.  The eight kappa instances are the known such
type, but choosing a canonical coefficient resolution does not prove that
they exhaust the relative physical degree-one quotient.  A smallest bright
exotic extension is recorded as a logical/source-grammar counterguard; it
is not asserted to be a physical GHZ cell.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_psi_source_grade_macaulay_exhaustiveness_terminal_gate.py":
        "2ae3d0fe36ca6ab92ee506b4a4441d6476ecb09567a1441c66f54793e304980d",
    "notes/h3-psi-source-grade-macaulay-exhaustiveness-terminal-gate.md":
        "de47eeafdfcffbd043f3b2472f3be54b7ec94ad546fe2bab7194e8b64bd9c98a",
    "computations/verify_h3_cross_word_mapping_cylinder_d2_augmentation_freedom_gate.py":
        "3704235f1030a07556aaebed3225bec8ea0fb9fa4d6a4d3aa124a7727a3bebec",
    "notes/h3-cross-word-mapping-cylinder-d2-augmentation-freedom-gate.md":
        "ef33bdd1f600fb3f58e91ca191a2fcfcfab516d5680907661a006ca5d358cec0",
    "computations/verify_h3_six_term_dual_absolute_resolution_exhaustivity.py":
        "d1b545f25603930a6247a286c5be70c7d16e20caab053401eeeb650bb53559d6",
    "notes/h3-six-term-dual-absolute-resolution-exhaustivity.md":
        "6b7df12daf54ffe8e7724ebadb9642db2de2e191aca8036c82abc21ea9ab91bd",
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
    "notes/h3-hasse-coproduct-cosimplicial-totalization.md":
        "9bb749b3b45a6b0248699bf54364cb304f89e01a4a4ad654963aad3534893ba4",
    "computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py":
        "c62ca38edf160f706d7aed237a923737ca46fe7b906fb0bb48bdf400e2ea7854",
    "notes/h3-gate-ii-chiw-nonfill-full-augmented-dual.md":
        "f7fd790075f7cf3d31b9d4a6035fa6bc476a3bdc16ce4bda97b777b153664568",
}
EXPECTED_LEDGER_SHA256 = "6741838df9c2c3e8d9ac5965853240d0004241d72db5422d9727ee338e0ad26f"

DELTA = tuple(map(Q, (1, 1, -1, -1)))
ZERO4 = (Q(0),) * 4
ZERO8 = (Q(0),) * 8


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    columns = tuple(tuple(map(Q, column)) for column in columns)
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    matrix = [[columns[column][row] for column in range(len(columns))]
              for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(height):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == height:
            break
    return pivot_row


def matrix_from_columns(columns):
    columns = tuple(tuple(map(Q, column)) for column in columns)
    if not columns:
        return ()
    return tuple(tuple(column[row] for column in columns)
                 for row in range(len(columns[0])))


def matvec(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def nullspace(columns):
    """Return a rational basis of relations among the given columns."""
    columns = tuple(tuple(map(Q, column)) for column in columns)
    if not columns:
        return ()
    matrix = [list(row) for row in matrix_from_columns(columns)]
    row_count = len(matrix)
    column_count = len(columns)
    pivots = []
    pivot_row = 0
    for column in range(column_count):
        pivot = next((row for row in range(pivot_row, row_count)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    free = [column for column in range(column_count) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [Q(0)] * column_count
        vector[free_column] = Q(1)
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -matrix[row][free_column]
        require(matvec(matrix_from_columns(columns), tuple(vector))
                == (Q(0),) * len(columns[0]),
                "nullspace relation failed")
        basis.append(tuple(vector))
    require(len(basis) == column_count - rank(columns),
            "nullity changed")
    return tuple(basis)


def add(left, right):
    return tuple(Q(a) + Q(b) for a, b in zip(left, right, strict=True))


def old_cap_columns():
    diagonal = []
    for corner in range(4):
        basis = tuple(Q(1) if index == corner else Q(0)
                      for index in range(4))
        diagonal.append(basis + basis)
    companions = []
    for direct in (0, 1):
        for endpoint in (2, 3):
            edge = tuple(Q(1) if index in (direct, endpoint) else Q(0)
                         for index in range(4))
            companions.append(edge + ZERO4)
    return tuple(diagonal + companions)


def canonical_grammar_audit(psi_source) -> dict[str, object]:
    records = psi_source.literal_family_records()
    unknown = tuple(record for record in records
                    if record["projection_reason"].startswith("UNCLASSIFIED"))
    require(len(records) == 12 and len(unknown) == 1
            and "kappa_mix" in unknown[0]["family"],
            "the 629bf8c grammar frontier changed")

    # At fixed polynomial degree three the Macaulay part is finite.  The
    # PP/Hasse coproduct and Koszul closure are functorial operations on this
    # declared generator list.  Recursively resolving kernels gives a free
    # resolution without changing C1 or d1.
    degree_partitions = tuple((relation, 3 - relation)
                              for relation in range(4))
    require(degree_partitions == ((0, 3), (1, 2), (2, 1), (3, 0)),
            "fixed-grade Macaulay partitions changed")
    return {
        "canonical_fixed_grade": psi_source.CAP_GRADE,
        "coefficient_Macaulay_degree_partitions": [
            list(pair) for pair in degree_partitions
        ],
        "declared_atomic_family_count": len(records),
        "classified_dark_atomic_families": len(records) - len(unknown),
        "declared_relative_atomic_type": unknown[0]["family"],
        "literal_instances_of_declared_relative_type": 8,
        "canonical_resolution_construction": [
            "C1 is free on every fixed-grade complete coefficient equation/multiple and declared PP/Koszul comparison atom",
            "d1 is its literal complete augmented output boundary",
            "C2 is free on a homogeneous generating basis of ker(d1)",
            "Cn+1 recursively resolves ker(dn)",
        ],
        "what_is_exhaustive_by_construction": (
            "the module presented by the declared coefficient/Macaulay/PP grammar"
        ),
        "what_is_not_proved_by_the_choice": (
            "that every physical response-to-cap comparison belongs to the declared grammar"
        ),
    }


def higher_syzygy_image_audit() -> dict[str, object]:
    old = old_cap_columns()
    dark_kappas = (ZERO8,) * 8
    d1_columns = old + dark_kappas
    chi = DELTA + tuple(-value for value in DELTA)
    require(rank(old) == rank(d1_columns) == 7
            and all(dot(chi, column) == 0 for column in d1_columns),
            "the rank-seven canonical d1 changed")

    kernel_basis = nullspace(d1_columns)
    require(len(kernel_basis) == 9, "canonical C1 kernel dimension changed")

    # Use a deliberately redundant C2 presentation, then resolve its two
    # redundancies by C3.  This is stronger than a minimal-resolution check.
    d2_columns = (kernel_basis
                  + (kernel_basis[0], add(kernel_basis[0], kernel_basis[1])))
    d1_matrix = matrix_from_columns(d1_columns)
    require(rank(d2_columns) == 9
            and all(matvec(d1_matrix, column) == ZERO8
                    for column in d2_columns),
            "d1*d2 stopped vanishing")
    d3_columns = nullspace(d2_columns)
    d2_matrix = matrix_from_columns(d2_columns)
    require(len(d3_columns) == 2
            and all(matvec(d2_matrix, column) == (Q(0),) * len(d1_columns)
                    for column in d3_columns),
            "redundant C2 resolution did not produce the expected C3")

    # Every putative C0 output produced by composing a higher syzygy with d1
    # is zero.  In particular chi cannot acquire a new pullback this way.
    composed_outputs = tuple(matvec(d1_matrix, column) for column in d2_columns)
    require(set(composed_outputs) == {ZERO8}
            and rank(d1_columns + composed_outputs) == rank(d1_columns),
            "a higher syzygy enlarged im(d1)")
    return {
        "C0_dimension": 8,
        "C1_generators_old_plus_dark_kappa": len(d1_columns),
        "rank_d1": rank(d1_columns),
        "kernel_d1_dimension": len(kernel_basis),
        "redundant_C2_generators_rank": [len(d2_columns), rank(d2_columns)],
        "C3_generators": len(d3_columns),
        "d1_d2": "zero on every generator",
        "d2_d3": "zero on every generator",
        "rank_im_d1_after_all_higher_composites":
            rank(d1_columns + composed_outputs),
        "chi_on_im_d1": "zero",
        "theorem": (
            "for a fixed C1->C0 presentation, ordinary C2 and higher syzygies only resolve kernels and cannot add any C1->C0 image"
        ),
    }


def relative_degree_one_counterguard() -> dict[str, object]:
    old = old_cap_columns()
    b_delta = DELTA + ZERO4
    chi = DELTA + tuple(-value for value in DELTA)
    normalized_psi = tuple(value / Q(4) for value in chi)
    require(rank(old) == 7
            and rank(old + (b_delta,)) == 8
            and dot(chi, b_delta) == 4
            and dot(normalized_psi, b_delta) == 1,
            "the primitive relative degree-one control changed")
    nonzero = [abs(value.numerator) for value in b_delta if value]
    require(gcd(*nonzero) == 1, "the exotic control stopped being primitive")

    # Add the exact physical-q relation rows (M,ainc,q).  The dark and bright
    # extensions have identical zero canonical square shadow, all protected
    # external values zero, and both obey q=M-ainc.  Only the B/Eq augmentation
    # differs.  This is a logical grammar guard, not a claimed physical cell.
    dark = ZERO8 + (Q(0), Q(0), Q(0))
    bright = b_delta + (Q(0), Q(0), Q(0))
    require(dark[-1] == dark[-3] - dark[-2]
            and bright[-1] == bright[-3] - bright[-2],
            "q=M-ainc failed on the two grammar extensions")
    require(dot(normalized_psi + (Q(0), Q(0), Q(0)), dark) == 0
            and dot(normalized_psi + (Q(0), Q(0), Q(0)), bright) == 1,
            "the dark/bright grammar counterguard changed")
    return {
        "known_relative_degree_one_space": "span(kappa_0,...,kappa_7)",
        "needed_exhaustiveness_equation": (
            "C1_phys,Gamma*/(C1_can,Gamma* + chi-dark generators) is spanned by the eight kappa classes"
        ),
        "smallest_unexcluded_exotic": {
            "homological_status": "new primitive total-degree-one comparison generator epsilon",
            "canonical_coefficient_PP_shadow": "zero",
            "B_Eq_output": "(delta,0)",
            "target_W_ores_ridge_eta_sigma_anchor_values": "zero",
            "M_ainc_q": [0, 0, 0],
            "q_equals_M_minus_ainc": True,
            "chi": "4",
            "normalized_Psi": "1",
            "rank_effect": "7 -> 8",
        },
        "dark_control_with_same_canonical_shadow": {
            "B_Eq_output": "zero",
            "all_external_values": "zero",
            "normalized_Psi": "0",
        },
        "logical_consequence": (
            "coefficient equations, ordinary PP/Koszul syzygies, d^2, and q=M-ainc do not decide absence of an additional bright physical comparison generator"
        ),
        "scope_guard": (
            "epsilon is an exact extension of the presentation grammar, not an asserted source-provenant GHZ operation"
        ),
    }


def cone_shift_and_terminal_audit(gate_ii_dual) -> dict[str, object]:
    dual_ledger, dual_digest = gate_ii_dual.audit()
    require(dual_digest == gate_ii_dual.EXPECTED_LEDGER_SHA256
            and not dual_ledger["physical_q_anchor_terminal_separation"][
                "q_or_anchor_generator_detected"],
            "the physical-q terminal separation changed")
    return {
        "ordinary_first_quadrant_total_degree_one_bidegrees": [
            [1, 0], [0, 1]
        ],
        "ordinary_syzygy_of_resolution_degree_at_least_two_can_enter_total_C1": False,
        "exception": (
            "a mapping-cone/desuspension can move an old C2 class to total degree one; after that shift it is a new relative C1 generator and must be included in the degree-one census"
        ),
        "physical_q_status": {
            "Psi_coefficient_on_q_M_ainc": [0, 0, 0],
            "q_equals_M_minus_ainc_compatible": True,
            "q_or_anchor_detects_the_missing_class": False,
        },
        "accepted_Fredholm_requires": [
            "one fixed exhaustive physical augmented map J_phys,Gamma*",
            "the literal physical candidate/RHS b in the same codomain",
            "a covector Psi with Psi*J_phys,Gamma*=0 and Psi(b)=1",
            "all target, W, residue, M, anchor, q, ridge, eta and sigma rows retained",
        ],
        "why_canonical_source_resolution_is_insufficient": (
            "it fixes the algebraic source ideal and its syzygies, but supplies neither the exhaustive relative comparison domain nor the physical candidate/RHS map"
        ),
    }


def audit():
    pin_dependencies()
    psi_source = load(
        "computations/verify_h3_psi_source_grade_macaulay_exhaustiveness_terminal_gate.py",
        "psi_degree1_source",
    )
    gate_ii_dual = load(
        "computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py",
        "psi_degree1_q_dual",
    )
    ledger = {
        "theorem": "h3 Psi canonical source resolution / relative degree-one loophole gate",
        "pins": PINS,
        "canonical_declared_source_grammar": canonical_grammar_audit(psi_source),
        "ordinary_higher_syzygies": higher_syzygy_image_audit(),
        "relative_degree_one_counterguard": relative_degree_one_counterguard(),
        "mapping_cone_and_physical_terminal":
            cone_shift_and_terminal_audit(gate_ii_dual),
        "verdict": (
            "Choosing the canonical coefficient-equation/Macaulay/Koszul-PP free resolution makes its declared fixed-grade grammar exhaustive and proves that C2 and all higher ordinary syzygies cannot alter im(d1) or chi.  It does not prove that this algebraic grammar is essentially surjective onto the physical augmented response-to-cap comparison complex.  The eight kappa_i are known relative total-degree-one instances; the precise remaining loophole is an additional primitive or cone-shifted degree-one physical comparison with zero canonical shadow and nonzero delta.(B-Eq).  The q=M-ainc row is compatible but dark on this class, so no accepted Fredholm terminal follows until that relative degree-one quotient and the literal physical RHS map are exhausted."
        ),
        "scope": (
            "Exact rational fixed-grade presentation/resolution theorem and smallest augmented grammar counterguard at canonical h=3.  It uses no symmetry or localization argument.  It does not assert that the exotic control is physical, nor prove the missing essential-surjectivity/source-generation theorem."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("Psi canonical-resolution ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 Psi canonical source resolution degree-one loophole gate: PASS")
    print("canonical coefficient/Macaulay/Koszul-PP grammar: EXHAUSTIVE FOR ITS PRESENTED MODULE")
    print("ordinary C2 and higher syzygies: CANNOT CHANGE im(d1) OR chi")
    print("physical relative degree-one quotient beyond eight kappa_i: NOT EXHAUSTED")
    print("q=M-ainc: COMPATIBLE BUT DOES NOT PROMOTE Psi")
    print("accepted Fredholm terminal: NEEDS RELATIVE C1 CENSUS + PHYSICAL RHS")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
