#!/usr/bin/env python3
"""Audit the exact transport gate for the physical dark-terminal readout.

The canonical h=3 relative grade has the physical covector

    q = sum_{i=1}^6 m_i - ainc.

For a placed Cartan prism in another grade, invariant normalized tail data
transport the Cartan residue/ridge packet, but do not by themselves define
q on the complete protected kernel.  The minimal extra datum is a protected
chain comparison which pulls back the aggregate physical q row.  Pullback of
the six-matching aggregate and physical anchor incidence separately is its
source-valid physical realization.  This checker audits that criterion and
a two-dimensional no-go guard for placement alone.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    # 83151bf
    "computations/verify_uniform_cartan_augmented_grade_naturality_gate.py":
        "d71b2ae71cdfc910e374b498a70edbb5e897867cf624dec49203c34e74647925",
    # 941f4b6
    "computations/verify_oo_dark_R_physical_generator_annihilator.py":
        "e4e1da1b1784f3c86d085965d9a556b17e4695c026daab8b109bcc4549c04abf",
    # 00db7ee
    "computations/verify_dark_cartan_terminal_safe_cancellation.py":
        "124963d21d779920322fcfc3d238351ce204093cc2587d1bba199ebc85b650d4",
    "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py":
        "647124e7c6646727653f7377d015d4f12010f39b8398b048a4ea065eedc73968",
    "computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py":
        "aea73ce5ff6ce183245d209393ed60192066d38eab7d4d203caa0c82cc5b16d6",
}
EXPECTED_LEDGER_SHA256 = (
    "cdaa9ccb732794fc2dd1a5e45983f0e9716245948e29a0c1a0252f90e5a51252"
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


def mat_vec(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def row_pullback(row, comparison):
    """Pull a canonical row back along comparison: L_new -> L_h3."""
    return tuple(sum(Q(row[index]) * Q(comparison[index][column])
                     for index in range(len(row)))
                 for column in range(len(comparison[0])))


def add_rows(rows):
    return tuple(sum(Q(row[column]) for row in rows)
                 for column in range(len(rows[0])))


def sub_rows(left, right):
    return tuple(Q(a) - Q(b)
                 for a, b in zip(left, right, strict=True))


def audit_pinned_interfaces(naturality, ridge, dark, cancellation, anchor):
    tail = naturality.audit_tail_residue_naturality()
    ridge_gate = naturality.audit_ridge_grade_naturality(ridge)
    branches = dark.audit_three_exact_branches()
    cancelled = cancellation.audit_instance(
        columns_c=((1, 0), (0, 1)),
        y=(1, 1),
        terminal_c=(0, 0),
        terminal_g=0,
        quotient_u=(1, 0),
        quotient_v=(0, 1),
    )
    physical = anchor.audit()

    require(tail["exact_factorization_criterion"] == "T=wT=sT=swT"
            and not tail["generic_tail_commutes"],
            "83151bf invariant-tail gate changed")
    require(not ridge_gate["arbitrary_common_tail_repairs_degree"]
            and "dT=0 and T=1" in ridge_gate["fixed_numeric_terminal_law"],
            "83151bf shifted-Kahler gate changed")
    require(branches["whole_kernel_killed"]["outcome"]
            == "physical_left_separator",
            "941f4b6 complete-kernel branch changed")
    require(cancelled["terminal_on_dark_kernel"] == "0"
            and cancelled["rank_full"] == cancelled["rank_quotient"],
            "00db7ee terminal-safe cancellation changed")
    require(physical["physical_covector"]
            == "Lambda=sum_6 selected matching rows - ainc"
            and physical["canonical_faces"] == [3, 5],
            "canonical h=3 physical q changed")

    return {
        "pinned_commits": {
            "83151bf": "invariant oriented tail and shifted-Kahler naturality gate",
            "941f4b6": "complete-kernel physical generator/Fredholm alternative",
            "00db7ee": "terminal-safe unit-kernel presentation cancellation",
        },
        "canonical_h3_faces": physical["canonical_faces"],
        "canonical_h3_fine_degree": physical["canonical_fine_degree"],
        "canonical_physical_q": physical["physical_covector"],
        "tail_criterion": tail["exact_factorization_criterion"],
        "orientation_rule": tail["orientation_rule"],
        "fixed_terminal_criterion": ridge_gate[
            "fixed_numeric_terminal_law"],
        "ordinary_common_tail_constructs_shifted_ridge": False,
    }


def audit_complete_comparison(dark):
    # Canonical domain coordinates are six literal matching rows, physical
    # ainc, and one additional relative coordinate.
    canonical_names = tuple(f"m{index}" for index in range(1, 7)) + (
        "ainc", "relative_aux")
    matching_rows = tuple(
        tuple(Q(int(column == index)) for column in range(8))
        for index in range(6)
    )
    ainc = tuple(Q(int(column == 6)) for column in range(8))
    q_canonical = sub_rows(add_rows(matching_rows), ainc)
    require(q_canonical == (1, 1, 1, 1, 1, 1, -1, 0),
            "canonical six-term row changed")

    # comparison is an explicit map L_new -> L_h3.  Its first two columns
    # carry protected data; the third maps to physical ainc and the fourth
    # is terminal-dark.  J_h3*comparison=J_new is the protected chain law.
    comparison = (
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    )
    protected_h3 = (
        (1, 0, 0, 0, 0, 0, 0, 0),
        (0, 1, 0, 0, 0, 0, 0, 0),
    )
    protected_new = tuple(row_pullback(row, comparison)
                          for row in protected_h3)
    require(protected_new == (
        (Q(1), Q(0), Q(0), Q(0)),
        (Q(0), Q(1), Q(0), Q(0)),
    ), "protected chain comparison changed")

    transported_matching_rows = tuple(
        row_pullback(row, comparison) for row in matching_rows)
    transported_ainc = row_pullback(ainc, comparison)
    transported_matching_sum = add_rows(transported_matching_rows)
    q_new_by_formula = sub_rows(
        transported_matching_sum, transported_ainc)
    q_new_by_pullback = row_pullback(q_canonical, comparison)
    require(q_new_by_formula == q_new_by_pullback
            == (Q(1), Q(1), Q(-1), Q(0)),
            "physical q failed rowwise transport")

    # Individual selected rows are stronger data than q needs.  Opposite
    # changes to two selected rows leave their aggregate, ainc, and q fixed.
    harmless_change = (Q(0), Q(0), Q(0), Q(1))
    regrouped_matching_rows = (
        tuple(a + b for a, b in zip(transported_matching_rows[0],
                                     harmless_change, strict=True)),
        tuple(a - b for a, b in zip(transported_matching_rows[1],
                                     harmless_change, strict=True)),
    ) + transported_matching_rows[2:]
    require(add_rows(regrouped_matching_rows) == transported_matching_sum,
            "aggregate row changed under harmless selected-row regrouping")

    anchor_kernel = (Q(0), Q(0), Q(1), Q(0))
    dark_kernel = (Q(0), Q(0), Q(0), Q(1))
    require(mat_vec(protected_new, anchor_kernel) == (Q(0), Q(0))
            and mat_vec(protected_h3,
                        mat_vec(comparison, anchor_kernel)) == (Q(0), Q(0)),
            "comparison stopped carrying protected kernels")
    require(dot(q_new_by_formula, anchor_kernel) == -1
            and dot(q_new_by_formula, dark_kernel) == 0,
            "transported kernel readouts changed")

    visible = dark.classify(protected_new, q_new_by_formula, anchor_kernel)
    terminal_dark = dark.classify(
        protected_new, q_new_by_formula, dark_kernel)
    require(visible[0] == "R_generator"
            and terminal_dark[0] == "other_kernel_generator",
            "transported complete-kernel alternatives changed")

    return {
        "canonical_domain_coordinates": list(canonical_names),
        "comparison_direction": "Phi:L_placed -> L_h3",
        "protected_chain_law": "J_h3 Phi=A J_placed (A=identity in the audit)",
        "minimal_exact_row_law": "q_placed=q_h3 Phi on the whole source domain",
        "source_valid_physical_realization": [
            "sum_i(m_i^placed)=(sum_i m_i^h3) Phi",
            "ainc^placed=ainc^h3 Phi",
        ],
        "individual_six_row_pullbacks_required": False,
        "individual_six_row_pullbacks_are_a_sufficient_labelled_refinement": True,
        "transported_q": [str(value) for value in q_new_by_formula],
        "kernel_transport": (
            "x in ker J_placed implies Phi(x) in ker J_h3; physical q values "
            "are equal before and after comparison"
        ),
        "visible_kernel_branch": visible[0],
        "dark_kernel_branch": terminal_dark[0],
        "what_then_transports_uniformly": [
            "the protected-zero property",
            "the physical six-term/ainc value",
            "normalization to the existing relative anchor",
            "the whole-kernel generator/Fredholm test",
            "terminal-safe cancellation of a q-dark unit kernel line",
        ],
    }


def audit_placement_only_counterguard(dark):
    # This is minimal: dimension one cannot retain a placed direction and an
    # independent protected-kernel direction.  Let e0 be the placed Cartan
    # coordinate and e1 the unresolved protected-kernel coordinate.
    protected = ((Q(1), Q(0)),)
    placed_cartan = (Q(1), Q(0))
    kernel = (Q(0), Q(1))
    component_charge = (Q(2), Q(1))
    matching_sum = (Q(1), Q(0))

    # Both possible ainc extensions agree on the placed Cartan coordinate.
    # They differ only on the kernel line, which placement never reads.
    ainc_dark = (Q(0), Q(0))
    ainc_visible = (Q(0), Q(-1))
    q_dark = sub_rows(matching_sum, ainc_dark)
    q_visible = sub_rows(matching_sum, ainc_visible)
    require(dot(q_dark, placed_cartan) == dot(q_visible, placed_cartan) == 1
            and dot(ainc_dark, placed_cartan)
            == dot(ainc_visible, placed_cartan) == 0,
            "two q extensions stopped agreeing on placed data")
    require(dot(q_dark, kernel) == 0 and dot(q_visible, kernel) == 1,
            "placement-only kernel ambiguity disappeared")

    dark_outcome = dark.classify(protected, q_dark, kernel)
    visible_outcome = dark.classify(protected, q_visible, kernel)
    require(dark_outcome[0] == "physical_left_separator"
            and visible_outcome[0] == "R_generator",
            "placement-only opposite Fredholm outcomes changed")

    # T=1 is already invariant, Kähler-constant, and normalized.  Therefore
    # this ambiguity remains even after imposing the strongest ordinary-tail
    # condition available from 83151bf.
    tail_orbit = (Q(1), Q(1), Q(1), Q(1))
    require(len(set(tail_orbit)) == 1,
            "identity tail stopped being invariant")

    return {
        "dimension": 2,
        "minimality": (
            "one placed coordinate plus one independent protected-kernel "
            "coordinate; dimension one cannot hide a kernel readout while "
            "holding the placed value fixed"
        ),
        "placed_cartan": [1, 0],
        "protected_map": [[1, 0]],
        "protected_kernel": [0, 1],
        "component_charge_chi": [2, 1],
        "component_charge_is_physical_q": False,
        "common_supplied_data": {
            "tail_orbit": [1, 1, 1, 1],
            "dT": 0,
            "terminal_T": 1,
            "matching_sum": [1, 0],
            "ainc_on_placed_cartan": 0,
            "q_on_placed_cartan": 1,
        },
        "unresolved_extensions": {
            "ainc_kernel_dark": {
                "ainc": [0, 0], "q": [1, 0],
                "q_on_kernel": 0, "outcome": dark_outcome[0],
            },
            "ainc_kernel_visible": {
                "ainc": [0, -1], "q": [1, 1],
                "q_on_kernel": 1, "outcome": visible_outcome[0],
            },
        },
        "verdict": (
            "critical placement and even an invariant normalized tail do "
            "not determine physical ainc, hence do not define q on the "
            "complete protected kernel"
        ),
    }


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    naturality = load(
        "computations/verify_uniform_cartan_augmented_grade_naturality_gate.py",
        "dark_q_naturality")
    ridge = load(
        "computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py",
        "dark_q_ridge")
    dark = load(
        "computations/verify_oo_dark_R_physical_generator_annihilator.py",
        "dark_q_fredholm")
    cancellation = load(
        "computations/verify_dark_cartan_terminal_safe_cancellation.py",
        "dark_q_cancellation")
    anchor = load(
        "computations/verify_h3_first_flat_physical_anchor_six_term_separator.py",
        "dark_q_anchor")

    ledger = {
        "theorem": "physical q transport needs an augmented row-preserving comparison",
        "pinned_interfaces": audit_pinned_interfaces(
            naturality, ridge, dark, cancellation, anchor),
        "sufficient_complete_comparison": audit_complete_comparison(dark),
        "minimal_placement_only_guard": audit_placement_only_counterguard(dark),
        "smallest_sufficient_condition": [
            "an augmented protected chain comparison Phi maps the whole placed source domain into the canonical h=3 repeated grade",
            "the exact minimal row law is q_placed=q_h3 Phi; a source-valid physical realization separately pulls back sum_6(m_i) and ainc",
        ],
        "complete_terminal_packet_adds": [
            "the tail is oriented and four-corner invariant: T=wT=sT=swT",
            "for fixed eta/sigma values it is Kahler-constant and normalized: dT=0 and T=1 in the terminal quotient",
            "the pq and xv halves are retained as separate shifted-Kahler labels and Omega, eta, sigma are transported together",
        ],
        "logical_separation": (
            "the tail/shifted-Kahler clauses transport the oriented residue/"
            "ridge packet.  They neither imply nor are needed for the q row "
            "alone.  Physical q is "
            "available on the complete protected kernel exactly after the "
            "six-matching aggregate and ainc are identified by the comparison; "
            "a critical-component charge remains a different functional"
        ),
        "sharp_frontier": (
            "in the canonical faces-(3,5), h=3 repeated grade the comparison "
            "is the identity and q is already physical.  Outside that grade, "
            "construct the labelled shifted-Kahler/anchor chain comparison; "
            "placement or invariant-tail multiplication alone cannot choose "
            "between the generator and Fredholm-annihilator outcomes"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("dark Cartan physical q transport ledger changed", digest))

    print("dark Cartan physical q transport: EXACT GATE")
    print("canonical h=3: q=sum_6(m_i)-ainc is defined")
    print("physical q: protected Phi + aggregate matching/ainc row law")
    print("complete terminal packet: add invariant normalized shifted ridge")
    print("placement/invariant tail alone: q on protected kernel UNDEFINED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
