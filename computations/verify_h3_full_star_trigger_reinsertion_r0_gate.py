#!/usr/bin/env python3
"""Test the trigger-labelled full-star reinsertion against physical cap r0.

For an ordered star branch i|j and a matching M containing x_0i, the branch
monomial is x_0j(M/x_0i).  Trigger deletion of x_0j followed by insertion of
x_0i recovers M exactly.  At carrier level this sends

    x_0j iota_0i(e) -> x_0i iota_0i(e).

The uniform 1/6 average over the 21 star pairs gives the edge-Euler carrier
sum_i x_0i iota_0i(e), whose boundary is H.  It does not give the
homogenizer term u iota_u(e), so it does not have boundary H-u.  More
importantly, the trigger operations remain response-internal and do not
produce the private B, Eq, normalized target and AugP2/K_Eq operation tags
of the physical r0.

The checker also classifies the smallest labelled Taylor-to-Spencer
deletion.  It is canonical on the 144 parent-labelled Taylor cells, but not
after collection to 135 lcms.  Nine degree-eight lcms have two different
parent presentations and two different collision outputs.  Ordinary
restriction commutes on kept branch factors and fails on every deleted
factor, giving the exact first mapping-cylinder face debt.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_first_collision_full_star_completion_gate.py":
        "ea45302b71998ca6ba3928a29f1e75eebc0ba360d1c234f73bd70dfb9b29d317",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_uc4_beq_tie_source_provenance_audit.py":
        "f237ccffd40863a201b780ea034fcbd7781bc555e1fbc6f528d99d3ab71394c6",
    "computations/verify_h3_termwise_private_full_nine_augp2_linear_landing_gate.py":
        "9c182f13ba4da4f2dd3ff49fd9ebf60dd1a218f53cbf4416e82a63236f57404f",
    "computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py":
        "cb328adc1f23b38f6f9f9305635ddbaef888178633f8db91c205fdfbdca1ff34",
}
EXPECTED_LEDGER_SHA256 = "728df1100bdaa7a621adb12b2d4cfb1b614dba30a494508934cd95e62c0a1fbc"

PURE_WORD = (1,) * 8
STAR_PARTNERS = tuple(range(1, 8))
ROOT_LABELS = ("AB", "AC")


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def rank(vectors) -> int:
    basis = {}
    for source in vectors:
        vector = {key: Q(value) for key, value in source.items() if value}
        while vector:
            pivot = min(vector, key=repr)
            if pivot not in basis:
                inverse = Q(1) / vector[pivot]
                basis[pivot] = {
                    key: value * inverse for key, value in vector.items()
                }
                break
            coefficient = vector[pivot]
            for key, value in basis[pivot].items():
                residue = vector.get(key, Q(0)) - coefficient * value
                if residue:
                    vector[key] = residue
                else:
                    vector.pop(key, None)
    return len(basis)


def star_cell(partner):
    return 0, partner, 1, 1


def remove_one(monomial, cell):
    terms = list(monomial)
    require(cell in terms, ("missing trigger", cell, monomial))
    terms.remove(cell)
    return frozenset(terms)


def matching_inventory(base):
    row = tuple(frozenset(monomial) for monomial in base.full_row(PURE_WORD))
    sectors = {
        partner: tuple(monomial for monomial in row
                       if star_cell(partner) in monomial)
        for partner in STAR_PARTNERS
    }
    require(len(row) == 90
            and sum(map(len, sectors.values())) == 90
            and set().union(*(set(values) for values in sectors.values()))
                == set(row),
            "star matching inventory changed")
    return row, sectors


def labelled_taylor_deletion_audit(base):
    _row, sectors = matching_inventory(base)
    a = star_cell(1)
    b = star_cell(7)
    left_parents = sectors[1]
    right_parents = sectors[7]
    presentations = []
    by_lcm = defaultdict(list)
    left_output_multiplicity = Counter()
    right_output_multiplicity = Counter()
    for left_index, left in enumerate(left_parents):
        for right_index, right in enumerate(right_parents):
            lcm = left | right
            left_branch = (left - {a}) | {b}
            right_branch = (right - {b}) | {a}
            left_deleted = lcm - left_branch
            right_deleted = lcm - right_branch
            require(not left_deleted & left_branch
                    and left_deleted | left_branch == lcm
                    and not right_deleted & right_branch
                    and right_deleted | right_branch == lcm
                    and len(left_branch) == len(right_branch) == 4
                    and len(left_deleted) == len(right_deleted)
                        == len(lcm) - 4,
                    (left_index, right_index, lcm, left_deleted,
                     right_deleted))
            record = {
                "left_parent": left_index,
                "right_parent": right_index,
                "lcm": lcm,
                "left_branch": left_branch,
                "right_branch": right_branch,
                "left_deleted": left_deleted,
                "right_deleted": right_deleted,
            }
            presentations.append(record)
            by_lcm[lcm].append(record)
            left_output_multiplicity[left_branch] += 1
            right_output_multiplicity[right_branch] += 1

    lcm_degree = Counter(len(record["lcm"]) for record in presentations)
    deletion_depth = Counter(
        len(record["left_deleted"]) for record in presentations)
    presentation_multiplicity = Counter(len(values)
                                        for values in by_lcm.values())
    ambiguous = []
    for lcm, records in by_lcm.items():
        if len(records) == 1:
            continue
        left_outputs = {record["left_branch"] for record in records}
        right_outputs = {record["right_branch"] for record in records}
        require(len(records) == len(left_outputs) == len(right_outputs) == 2,
                (lcm, records, left_outputs, right_outputs))
        ambiguous.append({
            "lcm_degree": len(lcm),
            "presentations": [(record["left_parent"],
                               record["right_parent"])
                              for record in records],
            "distinct_left_outputs": len(left_outputs),
            "distinct_right_outputs": len(right_outputs),
        })
    require(len(presentations) == 144 and len(by_lcm) == 135
            and lcm_degree == {6: 12, 7: 42, 8: 90}
            and deletion_depth == {2: 12, 3: 42, 4: 90}
            and presentation_multiplicity == {1: 126, 2: 9}
            and len(ambiguous) == 9
            and set(left_output_multiplicity.values()) == {12}
            and set(right_output_multiplicity.values()) == {12},
            (len(presentations), len(by_lcm), lcm_degree, deletion_depth,
             presentation_multiplicity, len(ambiguous),
             set(left_output_multiplicity.values()),
             set(right_output_multiplicity.values())))

    # For one ordered output, restriction commutes on the four kept branch
    # factors.  On a deleted lcm factor, source restriction followed by the
    # remaining deletion still gives the branch, whereas target restriction
    # is zero because that factor is absent.  This is the first cylinder debt.
    commuting_flags_one_side = sum(len(record["left_branch"])
                                   for record in presentations)
    deletion_debts_one_side = sum(len(record["left_deleted"])
                                  for record in presentations)
    require((commuting_flags_one_side, deletion_debts_one_side)
            == (576, 510),
            (commuting_flags_one_side, deletion_debts_one_side))
    return {
        "labelled_Taylor_parent_cells": len(presentations),
        "collected_lcms": len(by_lcm),
        "lcm_degree_histogram": {
            str(key): value for key, value in sorted(lcm_degree.items())},
        "minimal_deletion_depth_histogram": {
            str(key): value for key, value in sorted(deletion_depth.items())},
        "labelled_deletion_formula":
            "L_(M,N) -> x_0j*(M/x_0i), deleting L minus that branch",
        "labelled_insertion_after_deletion_is_identity": True,
        "each_ordered_branch_parent_multiplicity": 12,
        "normalized_parent_average": "(1/12) over the opposite parents",
        "collected_lcm_presentation_histogram": {
            str(key): value
            for key, value in sorted(presentation_multiplicity.items())},
        "ambiguous_collected_lcms": len(ambiguous),
        "ambiguous_lcm_degree": 8,
        "first_ambiguous_record": ambiguous[0],
        "canonical_with_parent_labels": True,
        "canonical_after_lcm_collection": False,
        "restriction_flags_one_ordered_side": {
            "commuting_kept_factors": commuting_flags_one_side,
            "noncommuting_deleted_factors": deletion_debts_one_side,
        },
        "restriction_flags_both_ordered_sides": {
            "commuting_kept_factors": 2 * commuting_flags_one_side,
            "noncommuting_deleted_factors": 2 * deletion_debts_one_side,
        },
        "first_mapping_cylinder_debt": (
            "for every q in the deletion set, D_q before deletion is nonzero "
            "but D_q of the four-cell branch is zero"
        ),
    }


def trigger_reinsertion_audit(base):
    row, sectors = matching_inventory(base)
    cap_multiplicity = Counter()
    edge_carrier_multiplicity = Counter()
    branch_count = 0
    remote_commuting_flags = 0
    trigger_faces = 0
    for left_partner, right_partner in combinations(STAR_PARTNERS, 2):
        for selected_partner, inserted_partner in (
            (left_partner, right_partner),
            (right_partner, left_partner),
        ):
            selected = star_cell(selected_partner)
            inserted = star_cell(inserted_partner)
            for parent in sectors[selected_partner]:
                branch = (parent - {selected}) | {inserted}
                require(inserted in branch and selected not in branch,
                        (selected_partner, inserted_partner, branch))
                after_trigger_deletion = remove_one(branch, inserted)
                after_selected_insertion = after_trigger_deletion | {selected}
                require(after_selected_insertion == parent,
                        (selected_partner, inserted_partner, parent,
                         after_selected_insertion))
                cap_multiplicity[parent] += 1
                branch_count += 1
                remote_commuting_flags += len(after_trigger_deletion)
                trigger_faces += 1
            edge_carrier_multiplicity[selected_partner] += 1

    require(branch_count == 540
            and len(cap_multiplicity) == 90
            and set(cap_multiplicity.values()) == {6}
            and edge_carrier_multiplicity
                == Counter({partner: 6 for partner in STAR_PARTNERS})
            and remote_commuting_flags == 1620
            and trigger_faces == 540,
            (branch_count, len(cap_multiplicity),
             set(cap_multiplicity.values()), edge_carrier_multiplicity,
             remote_commuting_flags, trigger_faces))

    # The edge-Euler carrier has boundary H.  The homogenized relation has
    # one further independent -u coordinate, not supplied by any star pair.
    edge_boundary = {("matching", repr(monomial)): Q(1)
                     for monomial in row}
    relation_boundary = dict(edge_boundary)
    relation_boundary[("homogenizer", "u")] = Q(-1)
    require(rank((edge_boundary,)) == 1
            and rank((edge_boundary, relation_boundary)) == 2,
            "homogenizer face stopped being independent")

    root_branch_count = len(ROOT_LABELS) * branch_count
    return {
        "trigger_operator":
            "T_(i|j)=I_(x_0i) D_(x_0j)",
        "termwise_identity":
            "T_(i|j)[x_0j*(M/x_0i)]=M",
        "carrier_identity":
            "T_(i|j)[x_0j*iota_0i(e)]=x_0i*iota_0i(e)",
        "full_star_branch_instances_per_root": branch_count,
        "full_star_branch_instances_two_roots": root_branch_count,
        "each_cap_matching_multiplicity": 6,
        "uniform_average": (
            "(1/6) sum_(i<j,ordered branches) T_(i|j) "
            "=sum_i x_0i*iota_0i on the carrier"
        ),
        "edge_Euler_boundary": "H",
        "homogenized_Euler_boundary": "H-u",
        "missing_homogenizer_carrier": "u*iota_u(e)",
        "star_average_equals_homogenized_G0": False,
        "remote_factor_restriction_squares_commuting": remote_commuting_flags,
        "trigger_changing_faces": trigger_faces,
        "coefficient_reinsertion_canonical": True,
    }


def physical_r0_gate(cap_provenance, landing, restriction):
    cap_provenance.pin_dependencies()
    cap = cap_provenance.cap_r0_provenance_audit()
    require(cap["literal_response_boundary"] == "private full-nine B packet"
            and cap["internal_cap_differential"]
                == "d r_0=(H_0-u)e_Eq"
            and cap["normalized_target"] == 1
            and cap["internal_B_equals_Eq_tie"]
            and cap["cross_word_response_to_cap_membership"] == "OPEN",
            cap)

    landing_ledger, landing_digest = landing.audit()
    require(landing_digest == landing.EXPECTED_LEDGER_SHA256,
            landing_digest)
    private = landing_ledger["private_insertion_restriction"]
    physical = landing_ledger["physical_obstruction_after_linear_solution"]
    require(private["restriction_after_insertion_is_identity"]
            and private["rank_on_residual"] == 7
            and physical["first_typed_obstruction"]
                ["current_operation_algebra_value"] == "e_C A e_R=0",
            (private, physical))

    centered = restriction.component_audit(3)
    require(centered["global_reconstruction"] == "sum_e I_e D_e = 2 id"
            and len(centered["marked_residual_cuts"]) == 2,
            centered)

    # In the coarse B/Eq/target/off-diagonal quotient, granting the matching
    # shadow alone gives only B.  The physical r0 has all four coordinates.
    formal_trigger_cap_shadow = (Q(1), Q(0), Q(0), Q(0))
    physical_r0 = (Q(1), Q(1), Q(1), Q(1))
    require(rank((dict(enumerate(formal_trigger_cap_shadow)),)) == 1
            and rank((dict(enumerate(formal_trigger_cap_shadow)),
                      dict(enumerate(physical_r0)))) == 2,
            "trigger shadow became physical r0")
    return {
        "coarse_coordinates": ["B", "Eq", "target", "e_C A e_R"],
        "trigger_after_formal_cap_retag": [1, 0, 0, 0],
        "physical_r0": [1, 1, 1, 1],
        "rank_trigger_then_physical_r0": [1, 2],
        "actual_r0_internal_tie": "B=Eq",
        "actual_r0_normalized_target": cap["normalized_target"],
        "actual_r0_operation": "AugP2/K_Eq cap",
        "trigger_operation": "EqSystem/response endomorphism",
        "private_full_nine_insertion_status": (
            "split monic as a 180-term readout, rank 7 on the residual, but "
            "not an operation-changing physical map"
        ),
        "first_categorical_failure": "e_C A e_R=0",
        "first_boundary_failure_after_formal_retag":
            "the independent -u*e_Eq homogenizer/central-Eq face",
        "first_protected_failure": "normalized target 1 is absent",
        "trigger_defines_actual_r0": False,
        "trigger_defines_new_response_Euler_copy": True,
        "centered_restriction_warning": {
            "marked_lower_cuts": len(centered["marked_residual_cuts"]),
            "meaning": (
                "on a centered occurrence carrier the existing I_eD_e law "
                "retains two lower centered faces; top reconstruction alone "
                "does not totalize them"
            ),
        },
        "smallest_positive_completion": (
            "a parent-labelled Taylor-to-Spencer deletion cylinder together "
            "with one root-natural mixed divided-Hasse map carrying the full "
            "edge-plus-homogenizer Euler carrier to the existing tied r0"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "trigger_r0_base",
    )
    cap_provenance = load(
        "computations/verify_h3_uc4_beq_tie_source_provenance_audit.py",
        "trigger_r0_cap",
    )
    landing = load(
        "computations/verify_h3_termwise_private_full_nine_augp2_linear_landing_gate.py",
        "trigger_r0_landing",
    )
    restriction = load(
        "computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py",
        "trigger_r0_restriction",
    )
    ledger = {
        "theorem": "h3 full-star trigger reinsertion to physical-r0 gate",
        "pins": PINS,
        "minimal_parent_labelled_Taylor_to_Spencer_deletion":
            labelled_taylor_deletion_audit(base),
        "full_star_trigger_reinsertion": trigger_reinsertion_audit(base),
        "physical_r0_comparison": physical_r0_gate(
            cap_provenance, landing, restriction),
        "verdict": (
            "Trigger-labelled I_iD_j is an exact split inverse on every "
            "four-cell missing/doubled branch and its 1/6 full-star average "
            "is the edge-Euler carrier.  A minimal Taylor-to-Spencer deletion "
            "is canonical only while the two parent matching labels are kept: "
            "nine collected degree-eight lcms have two incompatible outputs, "
            "and every deleted factor gives a noncommuting restriction face.  "
            "The star average has boundary H, not H-u; no pair supplies the "
            "homogenizer carrier.  Finally I_iD_j remains response-internal.  "
            "Even after formally calling its matching shadow B, its Eq, target "
            "and response-to-cap coordinates are zero, whereas physical r0 has "
            "(B,Eq,target,Hom)=(1,1,1,1).  Thus the trigger construction gives "
            "a response Euler copy, not the existing tied r0"
        ),
        "scope": (
            "exact rational first-pair 12x12 Taylor packet, full 21-pair "
            "direct-free star, both root labels, literal trigger/parent labels, "
            "ordinary restriction flags, and the pinned physical r0/private "
            "landing.  No dependency on the untracked common-augmentation WIP"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("trigger-r0 ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=(
        "all", "taylor", "trigger", "naturality", "cap"), default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        taylor = ledger[
            "minimal_parent_labelled_Taylor_to_Spencer_deletion"]
        trigger = ledger["full_star_trigger_reinsertion"]
        cap = ledger["physical_r0_comparison"]
        print(f"h3 full-star trigger -> r0 ({arguments.mode}): PASS")
        print("labelled Taylor deletion: CANONICAL; collected ambiguities:",
              taylor["ambiguous_collected_lcms"])
        print("trigger star average boundary:", trigger["edge_Euler_boundary"])
        print("physical r0 rank ladder:", cap[
            "rank_trigger_then_physical_r0"])
        print("first typed face:", cap["first_categorical_failure"])
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
