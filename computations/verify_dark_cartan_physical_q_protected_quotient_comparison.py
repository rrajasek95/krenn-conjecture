#!/usr/bin/env python3
"""Characterize the weakest protected comparison transporting physical q.

Write q=M-a, where M is the aggregate of the six selected literal matching
rows and a is physical anchor incidence.  Given a protected comparison

    Phi:L -> L_h3,       J_h3 Phi = A J,

q needs to agree only on ker(J) for the dark-kernel/Fredholm alternative.
The exact condition is

    [(M-M_h3 Phi)] = [(a-a_h3 Phi)] in L^*/row(J),

or equivalently q-q_h3 Phi=lambda J.  Separate descent of M and a is a
source-transparent sufficient condition, but is stronger than necessary.
The difference of the two quotient classes is the first exact obstruction.
If both q rows are physically typed and Phi is a map of the complete
relative source domains, a nonzero obstruction is already positive: its
kernel witness, or its Phi-image, normalizes to a relative generator.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    # 3b74774
    "computations/verify_dark_cartan_physical_q_transport_gate.py":
        "8dc8e1e25316fd32ac27d86ebfff1ca77c870c302ff7becd9f10751d8567046c",
    # bcc75e1
    "computations/verify_global_dark_cartan_component_absorption.py":
        "2064044fee36392a6a73448409a8f33c7cec7c60e5b8700a43e1f4e6a8420165",
    "computations/verify_h3_repeated_component_six_term_separators.py":
        "b8c3eff88b44a9a12d45f61b44449ac8a0b3a4c3e9a6d351a50ef19293ce2d25",
    "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py":
        "647124e7c6646727653f7377d015d4f12010f39b8398b048a4ea065eedc73968",
    "computations/verify_h3_six_term_exhaustive_relative_extension_alternative.py":
        "bcc55b05c10ba1ac6f3c4415c18a70274ecc29dd506fbed8e69d471b5f0a5607",
    "computations/verify_oo_dark_R_physical_generator_annihilator.py":
        "e4e1da1b1784f3c86d085965d9a556b17e4695c026daab8b109bcc4549c04abf",
}
EXPECTED_LEDGER_SHA256 = (
    "bada633c6b28040aa5b67ba279a1d8a48042ac8b3eaa5eccd2cfd72e97369163"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def row_sub(left, right):
    return tuple(Q(a) - Q(b)
                 for a, b in zip(left, right, strict=True))


def rref(rows):
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return (), ()
    pivots = []
    pivot_row = 0
    for column in range(len(work[0])):
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
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return tuple(tuple(row) for row in work), tuple(pivots)


def nullspace(rows, width):
    if not rows:
        return tuple(tuple(Q(int(column == free)) for column in range(width))
                     for free in range(width))
    reduced, pivots = rref(rows)
    free = tuple(column for column in range(width) if column not in pivots)
    basis = []
    for free_column in free:
        vector = [Q(0)] * width
        vector[free_column] = Q(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column]
        basis.append(tuple(vector))
    require(all(all(dot(row, vector) == 0 for row in rows)
                for vector in basis), "nullspace reconstruction failed")
    return tuple(basis)


def solve_row_combination(rows, target):
    """Return lambda such that lambda*rows=target, or None."""
    if not rows:
        return () if not any(target) else None
    variables = len(rows)
    equations = [list(column) + [Q(value)] for column, value in
                 zip(zip(*rows, strict=True), target, strict=True)]
    reduced, pivots = rref(equations)
    if any(not any(row[:variables]) and row[variables] for row in reduced):
        return None
    answer = [Q(0)] * variables
    for row, pivot in enumerate(pivots):
        if pivot < variables:
            answer[pivot] = reduced[row][variables]
    require(all(sum(answer[row] * Q(rows[row][column])
                    for row in range(variables)) == Q(target[column])
                for column in range(len(target))),
            "row-combination reconstruction failed")
    return tuple(answer)


def mat_mul(left, right):
    if not left:
        return ()
    columns = tuple(zip(*right, strict=True))
    return tuple(tuple(dot(row, column) for column in columns)
                 for row in left)


def row_pullback(row, comparison):
    return tuple(dot(row, column)
                 for column in zip(*comparison, strict=True))


def obstruction_record(protected, matching_defect, ainc_defect):
    width = len(matching_defect)
    require(len(ainc_defect) == width
            and all(len(row) == width for row in protected),
            "protected quotient width changed")
    q_defect = row_sub(matching_defect, ainc_defect)
    matching_homotopy = solve_row_combination(protected, matching_defect)
    ainc_homotopy = solve_row_combination(protected, ainc_defect)
    q_homotopy = solve_row_combination(protected, q_defect)
    kernel = nullspace(protected, width)
    witness = next((vector for vector in kernel if dot(q_defect, vector)), None)
    require((q_homotopy is not None) == (witness is None),
            "row-space/kernel-annihilator duality changed")
    return {
        "matching_defect": [str(value) for value in matching_defect],
        "ainc_defect": [str(value) for value in ainc_defect],
        "q_defect": [str(value) for value in q_defect],
        "matching_descends_separately": matching_homotopy is not None,
        "ainc_descends_separately": ainc_homotopy is not None,
        "q_transports_on_protected_kernel": q_homotopy is not None,
        "q_row_homotopy": (None if q_homotopy is None else
                           [str(value) for value in q_homotopy]),
        "kernel_witness": (None if witness is None else
                           [str(value) for value in witness]),
        "q_defect_on_witness": (None if witness is None else
                                str(dot(q_defect, witness))),
    }


def audit_augmented_comparison_construction(dark):
    # Source and canonical protected complexes have one protected row and a
    # two-dimensional kernel.  Phi is identity here; the theorem allows any
    # source-valid grade-preserving Phi with Jc Phi=A J.
    protected = ((Q(1), Q(0), Q(0)),)
    protected_h3 = protected
    comparison = (
        (Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0)),
        (Q(0), Q(0), Q(1)),
    )
    protected_target_map = ((Q(1),),)
    require(mat_mul(protected_h3, comparison)
            == mat_mul(protected_target_map, protected),
            "protected comparison square stopped commuting")

    matching_h3 = (Q(0), Q(1), Q(0))
    ainc_h3 = (Q(0), Q(0), Q(1))
    q_h3 = row_sub(matching_h3, ainc_h3)

    # Separate row-homotopy descent: the two defects are protected rows.
    matching = (Q(2), Q(1), Q(0))
    ainc = (Q(-3), Q(0), Q(1))
    matching_defect = row_sub(
        matching, row_pullback(matching_h3, comparison))
    ainc_defect = row_sub(ainc, row_pullback(ainc_h3, comparison))
    separate = obstruction_record(protected, matching_defect, ainc_defect)
    require(separate["matching_descends_separately"]
            and separate["ainc_descends_separately"]
            and separate["q_transports_on_protected_kernel"]
            and separate["q_row_homotopy"] == ["5"],
            "separate aggregate/ainc descent stopped transporting q")

    q = row_sub(matching, ainc)
    q_defect = row_sub(q, row_pullback(q_h3, comparison))
    lam = tuple(Q(value) for value in separate["q_row_homotopy"])
    require(q_defect == tuple(sum(lam[row] * protected[row][column]
                                  for row in range(len(protected)))
                              for column in range(len(q))),
            "terminal row homotopy failed to reconstruct q defect")

    # The row homotopy constructs an honest augmented target comparison:
    # (J_h3 Phi, q_h3 Phi) = [[A,0],[-lambda,1]] (J,q).
    source_augmented = protected + (q,)
    canonical_after_phi = mat_mul(
        protected_h3 + (q_h3,), comparison)
    augmented_target_map = (
        (Q(1), Q(0)),
        (-lam[0], Q(1)),
    )
    require(canonical_after_phi
            == mat_mul(augmented_target_map, source_augmented),
            "row homotopy stopped constructing the augmented comparison")

    # Weakest q-only descent: both constituent defects represent the same
    # nonzero quotient class.  Neither descends separately, but q does.
    common = (Q(0), Q(1), Q(0))
    q_only = obstruction_record(protected, common, common)
    require(not q_only["matching_descends_separately"]
            and not q_only["ainc_descends_separately"]
            and q_only["q_transports_on_protected_kernel"],
            "equal nonzero constituent defects stopped cancelling in q")

    # First obstruction: matching transports exactly, while physical ainc
    # differs on a kernel coordinate.  Phi is still a protected chain map,
    # but q cannot be transported even modulo protected rows.
    ainc_obstruction = obstruction_record(
        protected,
        matching_defect=(Q(0), Q(0), Q(0)),
        ainc_defect=(Q(0), Q(-1), Q(0)),
    )
    require(ainc_obstruction["kernel_witness"] == ["0", "1", "0"]
            and ainc_obstruction["q_defect_on_witness"] == "1",
            "physical ainc obstruction lost its kernel witness")

    matching_obstruction = obstruction_record(
        protected,
        matching_defect=(Q(0), Q(0), Q(1)),
        ainc_defect=(Q(0), Q(0), Q(0)),
    )
    require(matching_obstruction["kernel_witness"] == ["0", "0", "1"]
            and matching_obstruction["q_defect_on_witness"] == "1",
            "aggregate matching obstruction lost its kernel witness")

    # A nonzero obstruction is a positive generator branch when both q rows
    # and Phi are physical on the complete relative domains.  Since
    # J_h3 Phi=A J, x in ker J implies Phi*x in ker J_h3.  A nonzero value
    # q(x)-q_h3(Phi*x) forces one of the two physical terminals to be nonzero.
    source_wins_q = (Q(0), Q(1), Q(0))
    canonical_dark_q = (Q(0), Q(0), Q(0))
    x = (Q(0), Q(1), Q(0))
    phi_x = tuple(sum(comparison[row][column] * x[column]
                      for column in range(len(x)))
                  for row in range(len(comparison)))
    require(all(dot(row, x) == 0 for row in protected)
            and all(dot(row, phi_x) == 0 for row in protected_h3),
            "obstruction witness stopped transporting to protected kernel")
    require(dot(source_wins_q, x) - dot(canonical_dark_q, phi_x) == 1,
            "source-visible obstruction value changed")
    source_branch = dark.classify(protected, source_wins_q, x)
    require(source_branch[0] == "R_generator",
            "source obstruction witness stopped normalizing")

    source_dark_q = (Q(0), Q(0), Q(0))
    canonical_wins_q = (Q(0), Q(-1), Q(0))
    require(dot(source_dark_q, x) - dot(canonical_wins_q, phi_x) == 1,
            "canonical-visible obstruction value changed")
    canonical_branch = dark.classify(
        protected_h3, canonical_wins_q, phi_x)
    require(canonical_branch[0] == "R_generator",
            "canonical obstruction image stopped normalizing")

    return {
        "protected_square": "J_h3 Phi=A J",
        "weakest_terminal_law": "q-q_h3 Phi=lambda J",
        "constructed_augmented_target_map": "[[A,0],[-lambda,1]]",
        "separate_aggregate_and_ainc_descent": separate,
        "q_only_equal_nonzero_defect_classes": q_only,
        "first_ainc_obstruction": ainc_obstruction,
        "first_matching_aggregate_obstruction": matching_obstruction,
        "nonzero_obstruction_closure": {
            "identity": (
                "o_q(x)=q(x)-q_h3(Phi x)!=0 with x in ker J and "
                "Phi x in ker J_h3"
            ),
            "forced_alternative": (
                "q(x)!=0 or q_h3(Phi x)!=0; normalize x in the first "
                "case or Phi x in the second"
            ),
            "source_visible_example": source_branch[0],
            "canonical_visible_example": canonical_branch[0],
            "load_bearing_physicality": [
                "q is the physical sum_6(m_i)-ainc terminal on L",
                "q_h3 is the physical canonical terminal on L_h3",
                "Phi maps the complete physical relative source L into L_h3",
                "J_h3 Phi=A J on all protected rows",
            ],
            "presentation_only_Phi_suffices": False,
        },
    }


def audit_exhaustive_quotient_duality():
    counts = Counter()
    cases = 0
    for height in range(3):
        for width in range(1, 5):
            for matrix_bits in product((0, 1), repeat=height * width):
                protected = tuple(
                    tuple(Q(matrix_bits[row * width + column])
                          for column in range(width))
                    for row in range(height)
                )
                for defect_bits in product((0, 1), repeat=2 * width):
                    matching_defect = tuple(Q(value) for value in
                                            defect_bits[:width])
                    ainc_defect = tuple(Q(value) for value in
                                        defect_bits[width:])
                    record = obstruction_record(
                        protected, matching_defect, ainc_defect)
                    separate = (record["matching_descends_separately"]
                                and record["ainc_descends_separately"])
                    transported = record[
                        "q_transports_on_protected_kernel"]
                    if separate:
                        require(transported,
                                "separate row descent failed to transport q")
                        counts["separate_descent"] += 1
                    elif transported:
                        counts["q_only_common_class"] += 1
                    else:
                        require(record["kernel_witness"] is not None,
                                "a quotient obstruction lost its witness")
                        counts["quotient_obstruction"] += 1
                    cases += 1
    require(cases == 74924 and all(counts[label] for label in (
        "separate_descent", "q_only_common_class", "quotient_obstruction"
    )), ("exhaustive quotient census changed", cases, counts))
    return {
        "binary_packets": cases,
        "heights": [0, 1, 2],
        "widths": [1, 2, 3, 4],
        "outcomes": dict(sorted(counts.items())),
        "verified_equivalence": (
            "[delta_M]=[delta_ainc] in L^*/row(J) iff "
            "(delta_M-delta_ainc) kills ker(J) iff q-q_h3 Phi=lambda J"
        ),
    }


def audit_pinned_physical_scope(transport, absorption, repeated, anchor,
                                exhaustive):
    transport_ledger = transport.audit_complete_comparison(
        load("computations/verify_oo_dark_R_physical_generator_annihilator.py",
             "protected_quotient_dark"))
    absorption_ledger, absorption_digest = absorption.audit()
    repeated_ledger = repeated.audit()
    anchor_ledger = anchor.audit()
    exhaustive_matrix = exhaustive.audit_binary_matrices()
    require(absorption_digest == absorption.EXPECTED_LEDGER_SHA256
            and absorption_ledger["dark_example"]["outcome"]
            == "global_unit_kernel",
            "global dark absorption interface changed")
    require(repeated_ledger["five_distinct_fine_grades"]
            and len(repeated_ledger["records"]) == 5,
            "five aggregate matching rows changed")
    require(anchor_ledger["physical_covector"]
            == "Lambda=sum_6 selected matching rows - ainc",
            "canonical physical q changed")
    require(exhaustive_matrix["binary_complete_maps"] == 5050,
            "exhaustive physical Fredholm interface changed")
    require(transport_ledger["minimal_exact_row_law"]
            == "q_placed=q_h3 Phi on the whole source domain",
            "3b74774 exact row law changed")
    return {
        "canonical_q": anchor_ledger["physical_covector"],
        "old_repeated_grades_with_literal_matching_aggregate":
            [record["faces"] for record in repeated_ledger["records"]],
        "global_dark_output": "one unit kernel of the exhaustive physical map",
        "exhaustive_Fredholm_packets":
            exhaustive_matrix["binary_complete_maps"],
        "scope_boundary": (
            "the old repeated grades have literal aggregate rows, but global "
            "component absorption does not construct a source-valid Phi or "
            "identify physical ainc on every new relative component grade"
        ),
    }


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    transport = load(
        "computations/verify_dark_cartan_physical_q_transport_gate.py",
        "protected_quotient_transport")
    absorption = load(
        "computations/verify_global_dark_cartan_component_absorption.py",
        "protected_quotient_absorption")
    repeated = load(
        "computations/verify_h3_repeated_component_six_term_separators.py",
        "protected_quotient_repeated")
    anchor = load(
        "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py",
        "protected_quotient_anchor")
    exhaustive = load(
        "computations/verify_h3_six_term_exhaustive_relative_extension_alternative.py",
        "protected_quotient_exhaustive")

    ledger = {
        "theorem": "weakest protected-kernel comparison for physical q",
        "pinned_physical_scope": audit_pinned_physical_scope(
            transport, absorption, repeated, anchor, exhaustive),
        "exact_construction_and_obstructions":
            audit_augmented_comparison_construction(
                load("computations/verify_oo_dark_R_physical_generator_annihilator.py",
                     "protected_quotient_closure_dark")),
        "exhaustive_mutation_guard": audit_exhaustive_quotient_duality(),
        "sharp_theorem": (
            "for any source-valid grade-preserving protected comparison "
            "Phi with J_h3 Phi=A J, physical q transports on the complete "
            "protected kernel iff the aggregate-matching defect and physical-"
            "ainc defect have the same class in L^*/row(J).  Equivalently "
            "q-q_h3 Phi=lambda J, which constructs the augmented target map "
            "[[A,0],[-lambda,1]].  If the classes differ, their difference "
            "has a protected-kernel witness x.  Provided Phi and both q rows "
            "are physical on the exhaustive relative domains, J_h3 Phi x=0 "
            "and q(x)-q_h3(Phi x)!=0, so x or Phi x is already a normalized "
            "relative generator"
        ),
        "reduction": {
            "separate_matching_aggregate_chain_map": "sufficient, not necessary",
            "separate_physical_ainc_chain_map": "sufficient, not necessary",
            "weakest_joint_condition": "their quotient defect classes agree",
            "residue_or_ridge_hypothesis_used": False,
        },
        "remaining_physical_input": (
            "construct one source-valid word/fine/repeated-grade protected Phi "
            "for each noncanonical exhaustive Cartan component, or compute "
            "the displayed quotient obstruction.  Component charges and the "
            "global potential do not determine either defect class"
        ),
        "closed_dichotomy": (
            "physical protected Phi + nonzero quotient obstruction gives a "
            "relative generator on one side; zero obstruction constructs q "
            "transport and feeds the complete generator/Fredholm alternative"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("physical q protected quotient ledger changed", digest))

    print("dark Cartan physical q protected comparison: EXACT QUOTIENT GATE")
    print("weakest law: [matching defect]=[ainc defect] mod row(J)")
    print("equivalently: q-q_h3 Phi=lambda J")
    print("mismatched classes + physical Phi: generator on one side")
    print("residue/ridge input: NONE")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
