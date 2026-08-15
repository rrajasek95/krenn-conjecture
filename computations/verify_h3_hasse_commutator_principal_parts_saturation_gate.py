#!/usr/bin/env python3
"""Use [d,pi_top]N/t as a canonical Eq line and test t-saturation.

The auxiliary B/Eq split is avoided.  The cap Hasse totalization and its top
projection define a filtered commutator

    [d,pi_top]N = t E,                 t=H0-u.

The first t-adic coefficient E is invariant under replacing pi_top by a chain
homotopic projection and under adding split contractible stabilizations.  It
therefore defines a canonical one-dimensional principal-parts target once the
marked cap object (N,pi_top) is present.

The official 8,580-column order-six source block and all 48 squarefree
Macaulay/Schreyer slots contain no marked-cap/top-projection label, hence no
literal row of the comparison matrix lands in this commutator target.  Under
the smallest zero extension, E is not in im(J)+t*C0: modulo t the native row
has rank zero and adjoining E raises it to one.  The formal commutator column
tE and every relative dK=tE column also specialize to zero.

This is not yet a physical Fredholm separator.  The actual terminal RHS is an
occurrence/coefficient class and has no canonical map to the commutator line;
two stabilization-invariant readout completions give it values zero and one
while agreeing on all original labels.  Thus the exact remaining datum is a
source-derived pairing of the physical RHS and primitive boundaries with the
commutator target.  Once supplied, the saturation test is finite and exact.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_full_star_cap_totalization_eq_orbit_gate.py":
        "ce4d98c0160c86692c876879f90b69ae684d6d16bb3211d8ffe9a30fdc8c4e91",
    "computations/verify_h3_canonical_principal_parts_gammajet_enrichment_gate.py":
        "0163890e3ec1a7fd115e93f34f68c37a5c82eaf984b36c5b72531c39e5769a0f",
    "computations/verify_h3_order6_site_repeating_target_enrichment_current_tree.py":
        "f1bc7a9f8fdb9148fde5c4d79a4b7f59a3bd03cd6ff00dc1c2fb3c0e7f511ea9",
    "computations/verify_h3_order6_first_forbidden_face_exact_seed_cycle_gate.py":
        "0c3367ab48327bfbe308dc81191019d094eec054a04c3d1f2bd38f0e69faa2e9",
    "computations/verify_h3_eqsystem_occurrence_schreyer_intrinsic_psi_terminal_gate.py":
        "3fd68d8d8c84f0c9a8f76dff4e370279798f4ac9dbc811011a6cdfa344303c0f",
    "computations/verify_h3_gamma_cotangent_principal_parts_enrichment_foundation_gate.py":
        "3eb7bc5bd51a9affa3aa0cdab113efc2856375c0de9e083efc611aed7cd1058f",
}
EXPECTED_LEDGER_SHA256 = (
    "ce984713b77b86adfd0ebe4045f5d4bd5d413dd934b85c6b258e695ab509a177"
)
CAP_WORD = "01211222"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def rank(columns) -> int:
    columns = tuple(tuple(map(Q, column)) for column in columns)
    if not columns:
        return 0
    height = len(columns[0])
    rows = [[columns[column][row] for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def recursive_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, (tuple, list, set, frozenset)):
        for item in value:
            yield from recursive_strings(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from recursive_strings(key)
            yield from recursive_strings(item)


def canonical_commutator_target_audit(cap_ledger) -> dict[str, object]:
    ledger = cap_ledger
    defect = ledger["first_underived_module_associativity_defect"]
    faces = ledger["augmented_and_typed_faces"]
    require(defect["commutator"]
                == "[d,pi_top]N=(H_0-u)*e_Eq"
            and defect["commutator_polynomial_terms"] == 91
            and defect["homogenizer_coefficient"] == "-1"
            and defect["commutator_nonzero"], defect)

    # A two-step toy Hom differential models the universal identity
    # delta^2=0.  Therefore delta(pi+delta(h))=delta(pi), which is precisely
    # invariance of the commutator under chain homotopy of pi.
    hom_differential = lambda vector: (Q(0), Q(vector[0]))
    basis = ((Q(1), Q(0)), (Q(0), Q(1)))
    for projection in basis:
        for homotopy in basis:
            changed = tuple(left + right for left, right in
                            zip(projection, hom_differential(homotopy),
                                strict=True))
            require(hom_differential(changed)
                    == hom_differential(projection)
                    and hom_differential(hom_differential(homotopy))
                        == (Q(0), Q(0)),
                    (projection, homotopy, changed))
    return {
        "filtered_base": "R=Q[t], t=H0-u",
        "marked_object": "the literal translated cap Hasse totalization N",
        "projection": "pi_top to the physical cap top",
        "commutator": defect["commutator"],
        "commutator_polynomial_terms":
            defect["commutator_polynomial_terms"],
        "homogenizer_coefficient": defect["homogenizer_coefficient"],
        "smallest_target": (
            "C_comm=R{E}, with first jet gr_t^1(t*C_comm)=Q{tE}; "
            "divide the commutator by t and reduce mod t"
        ),
        "canonical_first_jet_generator": "E=[d,pi_top]N/t mod t",
        "uses_auxiliary_B_Eq_split": False,
        "chain_homotopy_invariant": True,
        "split_contractible_stabilization_invariant": True,
        "stability_reason": "delta_Hom^2=0 and split projections commute with d",
        "proper_faces_already_on_N": faces[
            "universal_proper_faces_supplied_by_N"],
        "target_obstruction_after_augmented_pair": faces[
            "target_obstruction_after_augmented_pair"],
        "physical_P2_landing_supplied_by_N": faces[
            "source_labelled_P2_landing_supplied_by_N"],
        "forced_dq23_value_if_landing_is_granted": faces[
            "forced_0102_dq23_face"]["detector_value"],
    }


def full_native_source_label_audit(site, seed) -> dict[str, object]:
    loaded = site.modules()
    loaded["site"] = site
    columns, shifts = site.build_operator_columns(loaded)
    metadata = seed.ordered_metadata(loaded, columns, shifts)
    require(len(columns) == len(shifts) == len(metadata) == 8580,
            (len(columns), len(shifts), len(metadata)))
    words = Counter(seed.word_of_negative_fine_shift(shift)
                    for shift in shifts)
    require(words == {"11111111": 6381, "11211211": 2199}, words)
    stage_histogram = Counter()
    row_union = set()
    native_strings = set()
    for column in columns:
        row_union.update(column)
        for row in column:
            stage_histogram[row[0]] += 1
            native_strings.update(recursive_strings(row))
    for datum in metadata:
        native_strings.update(recursive_strings(datum))
    forbidden = {"pi_top", "Eq", "commutator", "homogenizing", "cap"}
    require(not native_strings & forbidden, native_strings & forbidden)

    boolean_slots = tuple((fine, mask) for fine in range(6)
                          for mask in range(8))
    hasse_edges = tuple(
        ((fine, mask), (fine, mask | (1 << bit)))
        for fine in range(6) for mask in range(8) for bit in range(3)
        if not mask & (1 << bit)
    )
    require(len(boolean_slots) == 48 and len(hasse_edges) == 72,
            (len(boolean_slots), len(hasse_edges)))
    return {
        "operator_columns": len(columns),
        "literal_row_union": len(row_union),
        "source_word_histogram": dict(sorted(words.items())),
        "cap_word": CAP_WORD,
        "cap_word_occurs_in_native_operator_block": CAP_WORD in words,
        "operator_metadata_shape": (
            "(coefficient decorated cell, ordered tuple of decorated "
            "differential directions)"
        ),
        "literal_stage_incidence_histogram": {
            str(stage): count for stage, count in sorted(stage_histogram.items())
        },
        "literal_string_tags_found": sorted(native_strings),
        "commutator_or_pi_top_tagged_columns": 0,
        "squarefree_Macaulay_Schreyer_slots": len(boolean_slots),
        "Boolean_Hasse_edges": len(hasse_edges),
        "reverse_Macaulay_edges": len(hasse_edges),
        "commutator_or_pi_top_tagged_48_slots": 0,
        "native_target_axes": [
            "equation word", "matching occurrence", "decorated operator "
            "history", "principal-parts row stage",
        ],
        "missing_target_axis": (
            "a marked cap object and top-projection morphism whose Hom "
            "differential has a t-linear commutator"
        ),
        "literal_J_to_commutator_line_defined": False,
    }


def saturation_membership_audit() -> dict[str, object]:
    # In the smallest native zero extension every one of the 8580 columns and
    # 48 slots has commutator coordinate zero.  The formal N/K commutator
    # contributes t, whose constant term is also zero.  Thus the specialized
    # row has rank zero and E raises it to one.
    native_specialized_columns = ((Q(0),),) * (8580 + 48)
    formal_relative_column_mod_t = (Q(0),)
    e = (Q(1),)
    require(rank(native_specialized_columns) == 0
            and rank(native_specialized_columns
                     + (formal_relative_column_mod_t,)) == 0
            and rank(native_specialized_columns + (e,)) == 1,
            "one-row saturation rank changed")
    return {
        "membership_problem": "E in im(J)+t*C_comm",
        "native_zero_extension": {
            "8580_operator_commutator_entries": 0,
            "48_Schreyer_commutator_entries": 0,
            "rank_after_t_equals_zero": 0,
            "rank_after_adjoining_E": 1,
            "E_is_in_imJ_plus_tC0": False,
        },
        "formal_cap_commutator_column": "tE",
        "relative_K_column": "tE",
        "both_formal_columns_after_t_equals_zero": 0,
        "post_specialization_filler_requires": (
            "one source column a(t)E plus protected faces with a(0) nonzero"
        ),
        "equivalently": "a unit/absolute decorated Eq coefficient",
        "48_slot_higher_Schreyer_effect": (
            "resolves native coefficient kernels and cannot add a missing "
            "commutator target row"
        ),
        "normalized_commutator_dual": (
            "constant-term evaluation lambda_comm(E)=1; it kills tE and the "
            "native zero extension"
        ),
        "unconditional_physical_terminal": False,
        "why_conditional": (
            "zero is the smallest native extension, but the original source "
            "does not define the comparison row J_comm whose exhaustiveness a "
            "physical Fredholm claim would require"
        ),
    }


def physical_rhs_pairing_and_protected_gate(cap_ledger) -> dict[str, object]:
    ledger = cap_ledger
    faces = ledger["augmented_and_typed_faces"]
    require(faces["target_obstruction_after_augmented_pair"] == 0
            and not faces["source_labelled_P2_landing_supplied_by_N"]
            and faces["forced_0102_dq23_face"]["detector_value"] == "35/72",
            faces)

    # The same native scalar RHS has two lifts to occurrence plus commutator
    # target.  Contractible stabilization acts in the source and fixes both
    # target values, so commutator stability alone does not select a lift.
    rhs_zero_lift = (Q(1), Q(0))
    rhs_bright_lift = (Q(1), Q(1))
    forget = lambda value: value[0]
    require(forget(rhs_zero_lift) == forget(rhs_bright_lift) == Q(1)
            and rhs_zero_lift != rhs_bright_lift,
            (rhs_zero_lift, rhs_bright_lift))
    return {
        "commutator_class_itself_pairs_with_lambda_comm": 1,
        "physical_terminal_RHS_native_type": (
            "Gamma occurrence/coefficient and protected cap readouts"
        ),
        "physical_RHS_contains_marked_N_pi_top_datum": False,
        "canonical_map_physical_RHS_to_commutator_line": False,
        "two_stabilization_invariant_readout_completions": {
            "same_native_RHS": 1,
            "commutator_values": [0, 1],
            "all_original_equation_monomial_operator_labels_equal": True,
        },
        "therefore_lambda_comm_is_currently_a_physical_RHS_separator": False,
        "protected_faces_of_the_only_known_commutator_source": {
            "q23_q45": faces["universal_proper_faces_supplied_by_N"],
            "target_obstruction": faces[
                "target_obstruction_after_augmented_pair"],
            "physical_P2_landing": faces[
                "source_labelled_P2_landing_supplied_by_N"],
            "conditional_dq23_detector": faces[
                "forced_0102_dq23_face"]["detector_value"],
            "remaining_complete_Eq": faces["remaining_complete_Eq"],
            "remaining_labelled_residue": faces[
                "remaining_labelled_residue"],
        },
        "first_missing_pairing_datum": (
            "a stabilization-invariant source-derived natural transformation "
            "from the literal physical Gamma presentation to C_comm, sending "
            "the actual RHS and every primitive boundary to explicit "
            "commutator coefficients"
        ),
        "then_exact_test": (
            "solve Jx+t*y=E with the 8580 operator histories, 48 complement "
            "slots and all q/anchor/target/ores/W/ridge/eta/sigma faces"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    cap_gate = load(
        "computations/verify_h3_full_star_cap_totalization_eq_orbit_gate.py",
        "commutator_sat_cap",
    )
    site = load(
        "computations/verify_h3_order6_site_repeating_target_enrichment_current_tree.py",
        "commutator_sat_site",
    )
    seed = load(
        "computations/verify_h3_order6_first_forbidden_face_exact_seed_cycle_gate.py",
        "commutator_sat_seed",
    )
    cap_ledger, cap_digest = cap_gate.audit()
    require(cap_digest == cap_gate.EXPECTED_LEDGER_SHA256, cap_digest)
    ledger = {
        "theorem": (
            "the Hasse top commutator defines a stabilization-invariant "
            "first-jet Eq line without a B/Eq split, but the native 8580/48 "
            "source has no canonical comparison row or physical-RHS pairing "
            "to that line"
        ),
        "pins": PINS,
        "canonical_filtered_commutator_target":
            canonical_commutator_target_audit(cap_ledger),
        "full_8580_and_48_slot_native_source":
            full_native_source_label_audit(site, seed),
        "nonflat_membership_test": saturation_membership_audit(),
        "physical_RHS_and_protected_pairing":
            physical_rhs_pairing_and_protected_gate(cap_ledger),
        "verdict": (
            "Positive: E=[d,pi_top]N/t mod t is a canonical, chain-homotopy "
            "and split-stabilization invariant first-jet class once the marked "
            "cap projection is given. Negative: none of the complete 8580 "
            "native operator columns or 48 coefficient-complement slots "
            "contains that projection label, so the literal comparison row is "
            "undefined. Its smallest zero extension has specialized rank zero "
            "and does not contain E; tE from N or a relative K also vanishes. "
            "But the physical RHS has two equally stabilization-invariant "
            "lifts with commutator values zero and one. Hence lambda_comm is "
            "not yet a physical Fredholm separator. One source-derived RHS/"
            "boundary pairing to C_comm is the exact missing datum; after it "
            "is defined, Jx+t*y=E is the finite filler-or-terminal test."
        ),
        "scope": (
            "exact canonical h3 cap commutator (91 terms, u coefficient -1), "
            "exact full current 8580-column label scan and 48-slot Boolean "
            "resolution, exact one-row t-saturation ranks and all pinned "
            "q23/q45, target, Eq and residue faces. This proves a missing-"
            "pairing criterion, not nonexistence of a physical post-"
            "specialization filler and not Krenn's conjecture."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("commutator saturation ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "target", "source",
                                            "saturation", "rhs"),
                        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print("h3 Hasse commutator principal-parts saturation gate:",
              arguments.mode, "PASS")
        print("canonical stabilization-invariant E line: YES")
        print("native 8580/48 comparison row: UNDEFINED")
        print("E in native zero-extension image+tC0: NO")
        print("physical RHS paired canonically: NO")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
