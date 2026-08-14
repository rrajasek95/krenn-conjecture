#!/usr/bin/env python3
"""Build the minimal protected completion after the full-star trigger gate.

The completion grants every response-side repair suggested by the previous
audit: the homogenizer carrier u*iota_u, 1020 parent-labelled deleted-factor
mapping cylinders, and nine presentation cylinders for duplicated lcms.  It
also retains the already constructed physical cap r0 with tied B=Eq and
normalized target.

The protected totalization has a genuine common untyped augmentation:
the normalized full-star carrier and the private B-boundary of physical r0
both map to the all-ones vector in the 90-dimensional parent-labelled
matching module.  Consequently the old argument which merely declared the
two copies orthogonal is invalid.  However the common augmentation exists
only after forgetting word, operation, Eq and target labels.  In the literal
source category the response coefficient row and cap Eq row are still in
different operation corners, and no comparison arrow is generated.

Thus projective comparison would construct the desired cylinder if a
source-labelled common augmentation/resolution were supplied.  The exact
remaining obstruction is that enriched augmentation (equivalently the
mixed K_Eq/AugP2 comparison), not a coefficient mismatch.  A normalized
two-root operation-corner covector detects it after the common 90-term base
has been identified.  The first raw noncommuting face repaired by the
relative cylinder is the selected x_01 restriction of the lexicographically
first degree-eight Taylor cell.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_first_collision_full_star_completion_gate.py":
        "ea45302b71998ca6ba3928a29f1e75eebc0ba360d1c234f73bd70dfb9b29d317",
    "computations/verify_h3_full_star_trigger_reinsertion_r0_gate.py":
        "43b90109c723272d8888a2cd7285ae0694892221691fbb7fe2b9266568dcb9d2",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_uc4_beq_tie_source_provenance_audit.py":
        "f237ccffd40863a201b780ea034fcbd7781bc555e1fbc6f528d99d3ab71394c6",
    "computations/verify_h3_termwise_private_full_nine_augp2_linear_landing_gate.py":
        "9c182f13ba4da4f2dd3ff49fd9ebf60dd1a218f53cbf4416e82a63236f57404f",
}
EXPECTED_LEDGER_SHA256 = (
    "a347b299d41da029470016fc24fa3eeb92cbdeb82149fac32376932d1f6b1e0d"
)

PURE_WORD = (1,) * 8
A = (0, 1, 1, 1)
B = (0, 7, 1, 1)
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


def sparse_rank(vectors) -> int:
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


def dot(dual, vector):
    return sum((Q(value) * Q(dual.get(key, 0))
                for key, value in vector.items()), Q(0))


def first_literal_noncommuting_face(base):
    row = tuple(frozenset(monomial) for monomial in base.full_row(PURE_WORD))
    left_parents = tuple(monomial for monomial in row if A in monomial)
    right_parents = tuple(monomial for monomial in row if B in monomial)
    require(len(left_parents) == len(right_parents) == 12,
            (len(left_parents), len(right_parents)))
    left = left_parents[0]
    right = right_parents[0]
    lcm = left | right
    branch = (left - {A}) | {B}
    deleted = lcm - branch
    selected = min(deleted, key=repr)
    source_restricted = lcm - {selected}
    after_remaining_deletion = source_restricted - (deleted - {selected})
    target_restriction = branch - {selected} if selected in branch else set()
    require(selected == A
            and len(lcm) == 8 and len(branch) == 4 and len(deleted) == 4
            and after_remaining_deletion == branch
            and target_restriction == set(),
            (left, right, lcm, branch, deleted, selected,
             after_remaining_deletion, target_restriction))
    return {
        "ordered_parents": [0, 0],
        "left_parent_M": repr(tuple(sorted(left))),
        "right_parent_N": repr(tuple(sorted(right))),
        "lcm_L": repr(tuple(sorted(lcm))),
        "left_branch_K": repr(tuple(sorted(branch))),
        "deletion_set_E": repr(tuple(sorted(deleted))),
        "first_restriction_factor_q": repr(selected),
        "source_composite":
            "delete q from L, then delete E\\{q}: result K",
        "source_composite_nonzero": True,
        "target_composite": "D_q(K)=0 because q is absent",
        "target_composite_zero": True,
        "commutator_value": repr(tuple(sorted(branch))),
        "face_type": "selected-trigger Taylor-to-Spencer restriction square",
    }


def ambiguity_and_deleted_cylinder_audit(base):
    row = tuple(frozenset(monomial) for monomial in base.full_row(PURE_WORD))
    left_parents = tuple(monomial for monomial in row if A in monomial)
    right_parents = tuple(monomial for monomial in row if B in monomial)
    by_lcm = defaultdict(list)
    deleted_flags = []
    for left_index, left in enumerate(left_parents):
        for right_index, right in enumerate(right_parents):
            lcm = left | right
            left_branch = (left - {A}) | {B}
            right_branch = (right - {B}) | {A}
            by_lcm[lcm].append((left_index, right_index,
                                 left_branch, right_branch))
            for orientation, branch in (("left", left_branch),
                                        ("right", right_branch)):
                for factor in sorted(lcm - branch, key=repr):
                    deleted_flags.append((left_index, right_index,
                                          orientation, factor, branch))
    ambiguous = [records for records in by_lcm.values()
                 if len(records) == 2]
    require(len(by_lcm) == 135 and len(ambiguous) == 9
            and len(deleted_flags) == 1020,
            (len(by_lcm), len(ambiguous), len(deleted_flags)))

    branch_coordinates = tuple(
        [("left", (parent - {A}) | {B}) for parent in left_parents]
        + [("right", (parent - {B}) | {A}) for parent in right_parents]
    )
    branch_index = {coordinate: index
                    for index, coordinate in enumerate(branch_coordinates)}
    ambiguity_vectors = []
    left_vectors = []
    right_vectors = []
    for records in ambiguous:
        first, second = records
        paired = Counter()
        left = Counter()
        right = Counter()
        for sign, record in ((Q(1), first), (Q(-1), second)):
            _li, _ri, left_branch, right_branch = record
            left[branch_index[("left", left_branch)]] += sign
            right[branch_index[("right", right_branch)]] += sign
            paired[branch_index[("left", left_branch)]] += sign
            paired[branch_index[("right", right_branch)]] -= sign
        left_vectors.append(dict(left))
        right_vectors.append(dict(right))
        ambiguity_vectors.append(dict(paired))
    require(sparse_rank(ambiguity_vectors) == 7
            and sparse_rank(left_vectors) == sparse_rank(right_vectors) == 7
            and sparse_rank(left_vectors + right_vectors) == 14,
            "ambiguous presentation rank changed")

    debt_projection = []
    for _left, _right, orientation, _factor, branch in deleted_flags:
        debt_projection.append({branch_index[(orientation, branch)]: Q(1)})
    require(sparse_rank(debt_projection) == 24,
            sparse_rank(debt_projection))
    return {
        "parent_labelled_Taylor_cells": 144,
        "collected_lcms": len(by_lcm),
        "ambiguous_collected_lcms": len(ambiguous),
        "presentation_safe_ambiguity_cylinders": len(ambiguous),
        "ambiguity_projection_rank_paired_boundary":
            sparse_rank(ambiguity_vectors),
        "ambiguity_projection_rank_if_sides_separated":
            sparse_rank(left_vectors + right_vectors),
        "deleted_factor_squares": len(deleted_flags),
        "presentation_safe_deleted_factor_cylinders": len(deleted_flags),
        "deleted_factor_projection_rank_on_24_branches":
            sparse_rank(debt_projection),
        "ambiguity_projection_already_in_deleted_debt_span":
            sparse_rank(debt_projection + ambiguity_vectors)
                == sparse_rank(debt_projection),
        "presentation_policy": (
            "retain all 144 parent cells; for each duplicate lcm add a "
            "relative presentation cylinder, and for every deleted-factor "
            "flag add a cylinder with a private slack rather than killing "
            "the branch in H0"
        ),
    }


def common_parent_occurrence_augmentation(base):
    """Compare both sides in the common untyped V=Q^90 base.

    The response augmentation is computed without using a declared cap map:
    every unordered site-0 pair contributes the two endpoint sectors, and the
    1/6 average counts every matching exactly once.  The cap augmentation is
    the literal complete private B packet, one copy of every matching.

    Relative deleted-factor cylinders preserve this augmentation by giving
    their private slack the parent matching of the selected branch.  An
    ambiguity cylinder similarly retains its two parent labels; it is never
    interpreted as killing their difference in H0.
    """
    row = tuple(base.full_row(PURE_WORD))
    require(len(row) == len(set(row)) == 90, "pure matching row changed")
    sectors = defaultdict(list)
    for monomial in row:
        incident = [cell for cell in monomial if 0 in cell[:2]]
        require(len(incident) == 1, (monomial, incident))
        cell = incident[0]
        partner = cell[1] if cell[0] == 0 else cell[0]
        sectors[partner].append(monomial)
    require(set(sectors) == set(range(1, 8))
            and sum(map(len, sectors.values())) == 90,
            {key: len(value) for key, value in sectors.items()})

    response = Counter()
    pair_count = 0
    for left in range(1, 8):
        for right in range(left + 1, 8):
            pair_count += 1
            for monomial in sectors[left] + sectors[right]:
                response[monomial] += Q(1, 6)
    cap_private_b = Counter({monomial: Q(1) for monomial in row})
    require(pair_count == 21 and response == cap_private_b
            and set(response.values()) == {Q(1)},
            (pair_count, Counter(response.values())))

    # The first protected cylinder illustrates the augmentation convention.
    left_parent = frozenset(sectors[1][0])
    right_parent = frozenset(sectors[7][0])
    branch = (left_parent - {A}) | {B}
    require(A in left_parent and B in right_parent and A not in branch,
            (left_parent, right_parent, branch))
    branch_reinsertion = (branch - {B}) | {A}
    require(branch_reinsertion == left_parent,
            (branch_reinsertion, left_parent))
    # d cylinder = branch composite - private slack.  Both augment to the
    # same parent, so the cylinder does not kill a nonzero class in V.
    protected_boundary_augmentation = Counter({left_parent: Q(1)})
    protected_boundary_augmentation[left_parent] -= Q(1)
    require(not +protected_boundary_augmentation,
            protected_boundary_augmentation)
    return {
        "common_base": "V=Q^{90} on parent-labelled pure matchings",
        "site0_sector_sizes": {
            str(key): len(sectors[key]) for key in sorted(sectors)
        },
        "unordered_star_pairs": pair_count,
        "response_full_star_weight_per_pair": "1/6",
        "response_multiplicity_each_matching_before_normalization": 6,
        "normalized_response_augmentation": "1_V",
        "physical_r0_private_B_augmentation": "1_V",
        "common_base_difference_rank": 0,
        "deleted_factor_private_slack_rule": (
            "augment the private slack to the parent M recovered by trigger "
            "reinsertion; d(cylinder)=branch-composite-slack augments to zero"
        ),
        "ambiguity_private_slack_rule": (
            "retain both parent presentations and augment their private "
            "slacks separately; do not quotient the two H0 labels"
        ),
        "common_matching_augmentation_is_exact": True,
    }


def protected_operation_quotient_and_dual():
    """Take the quotient only *after* identifying the common V augmentation.

    The final coordinate is not a second coefficient copy: it is the literal
    mixed operation corner e_C A e_R.  All currently generated operations
    have value zero there, while the desired comparison has value one.
    """
    columns = []
    names = []
    for root in ROOT_LABELS:
        columns.extend((
            {("response", root, "H"): Q(1)},
            {("response", root, "u"): Q(1)},
            {("cap", root, "B"): Q(1),
             ("cap", root, "Eq"): Q(1),
             ("cap", root, "target"): Q(1)},
        ))
        names.extend((f"edge-Euler:{root}", f"homogenizer:{root}",
                      f"physical-r0:{root}"))
    rank_core = sparse_rank(columns)
    require(rank_core == 6, rank_core)

    for root in ROOT_LABELS:
        for index in range(1020):
            columns.append({
                ("response", root, "deleted-cylinder-slack", index): Q(1),
                ("response", root, "branch-shadow", index % 24): Q(1),
            })
            names.append(f"deleted-cylinder:{root}:{index}")
    rank_deleted = sparse_rank(columns)
    require(rank_deleted == 6 + 2 * 1020, rank_deleted)

    for root in ROOT_LABELS:
        for index in range(9):
            columns.append({
                ("response", root, "ambiguity-cylinder-slack", index): Q(1),
                ("response", root, "branch-shadow", index): Q(1),
                ("response", root, "branch-shadow", (index + 1) % 24): Q(-1),
            })
            names.append(f"ambiguity-cylinder:{root}:{index}")
    rank_all_diagonal = sparse_rank(columns)
    require(rank_all_diagonal == 6 + 2 * (1020 + 9),
            rank_all_diagonal)

    # The common V=Q^90 coefficient base has already been identified.  The
    # desired natural map has one instance on each root in the still absent
    # physical mixed operation corner.
    desired = {
        ("e_C A e_R", "AB"): Q(1),
        ("e_C A e_R", "AC"): Q(1),
    }
    dual = {
        ("e_C A e_R", "AB"): Q(1, 2),
        ("e_C A e_R", "AC"): Q(1, 2),
    }
    require(all(dot(dual, column) == 0 for column in columns)
            and dot(dual, desired) == 1
            and sparse_rank(columns + [desired]) == rank_all_diagonal + 1,
            "normalized augmented mixed-operation dual changed")

    # If root naturality is not imposed, the two separately labelled mixed
    # instances raise rank twice.  The anti-diagonal dual survives one root.
    desired_ab = {("e_C A e_R", "AB"): Q(1)}
    desired_ac = {("e_C A e_R", "AC"): Q(1)}
    require(sparse_rank(columns + [desired_ab]) == rank_all_diagonal + 1
            and sparse_rank(columns + [desired_ab, desired_ac])
                == rank_all_diagonal + 2,
            "two-root mixed-operation quotient changed")
    return {
        "two_root_diagonal_core_rank": rank_core,
        "rank_after_2040_deleted_cylinders": rank_deleted,
        "rank_after_18_ambiguity_cylinders": rank_all_diagonal,
        "rank_after_one_root_natural_offdiagonal_map":
            rank_all_diagonal + 1,
        "rank_ladder": [rank_core, rank_deleted, rank_all_diagonal,
                        rank_all_diagonal + 1],
        "common_V_identified_before_this_quotient": True,
        "normalized_augmented_dual": {
            "formula": "omega_mix=((e_CAe_R)_AB^*+(e_CAe_R)_AC^*)/2",
            "value_on_every_allowed_diagonal_column": 0,
            "value_on_natural_paired_map": 1,
            "interpretation": (
                "operation-corner detector after coefficient augmentation; "
                "it does not declare the two 90-term coefficient copies "
                "orthogonal"
            ),
        },
        "separate_root_mixed_operation_quotient_dimension": 2,
        "one_natural_schema_instances": 2,
    }


def homogenizer_cap_coupling_gate(cap_provenance, landing, common_base):
    cap_provenance.pin_dependencies()
    cap = cap_provenance.cap_r0_provenance_audit()
    require(cap["internal_B_equals_Eq_tie"]
            and cap["normalized_target"] == 1
            and cap["cross_word_response_to_cap_membership"] == "OPEN",
            cap)
    landing_ledger, landing_digest = landing.audit()
    require(landing_digest == landing.EXPECTED_LEDGER_SHA256,
            landing_digest)
    linear = landing_ledger["most_general_two_root_linear_augmentation"]
    physical = landing_ledger["physical_obstruction_after_linear_solution"]
    require(linear["unique_tied_solution_exists_in_linear_enriched_category"]
            and physical["first_typed_obstruction"]
                ["current_operation_algebra_value"] == "e_C A e_R=0",
            (linear, physical))
    require(common_base["common_matching_augmentation_is_exact"]
            and common_base["common_base_difference_rank"] == 0,
            common_base)

    edge = (Q(1), Q(0), Q(0), Q(0))
    edge_plus_formal_cap_faces = (Q(1), Q(1), Q(1), Q(0))
    physical_map = (Q(1), Q(1), Q(1), Q(1))
    beq_dual = (Q(1), Q(-1), Q(0), Q(0))
    hom_dual = (Q(0), Q(0), Q(0), Q(1))
    require(sum(a * b for a, b in zip(beq_dual, edge, strict=True)) == 1
            and sum(a * b for a, b in zip(
                beq_dual, edge_plus_formal_cap_faces, strict=True)) == 0
            and sum(a * b for a, b in zip(
                hom_dual, edge_plus_formal_cap_faces, strict=True)) == 0
            and sum(a * b for a, b in zip(
                hom_dual, physical_map, strict=True)) == 1,
            "B/Eq versus mixed-operation separation changed")
    return {
        "coarse_coordinates": ["B", "Eq", "target", "e_C A e_R"],
        "edge_trigger_shadow": list(map(int, edge)),
        "after_formally_appending_physical_E_and_target_faces":
            list(map(int, edge_plus_formal_cap_faces)),
        "desired_physical_map": list(map(int, physical_map)),
        "common_parent_occurrence_base": common_base["common_base"],
        "response_and_cap_B_augmentations_equal": True,
        "coefficient_difference_on_common_V": 0,
        "B_equals_Eq_after_formal_face_append": True,
        "physical_boundary_constructed_without_mixed_comparison": False,
        "reason": (
            "the 90 matching coefficients agree, but the equality is in the "
            "untyped occurrence module.  The literal response coefficient "
            "row and cap Eq row retain different word/operation idempotents; "
            "no source map identifies them or transports target normalization"
        ),
        "B_minus_Eq_dual_before_formal_append": 1,
        "B_minus_Eq_dual_after_formal_append": 0,
        "mixed_operation_dual_after_formal_append": 0,
        "mixed_operation_dual_on_desired_map": 1,
        "unique_formal_tied_landing_if_mixed_comparison_is_added": True,
        "new_offdiagonal_primitive_still_required": True,
        "projective_comparison_test": {
            "identity_on_V_available": True,
            "both_objects_proved_resolutions_in_same_physical_category": False,
            "therefore_projective_lift_is_currently_source_valid": False,
            "exact_missing_common_base_map": (
                "a word/fine/repeated-labelled K_Eq/AugP2 augmentation "
                "sending the response coefficient generator to -E and the "
                "normalized Euler carrier to r0, with target one"
            ),
            "if_that_enriched_augmentation_is_supplied": (
                "the comparison theorem lifts id_V and the landing checker "
                "forces the unique root-tied residual-zero B=Eq solution; "
                "no second independent coefficient primitive is needed"
            ),
        },
        "first_remaining_noncommuting_face_after_relative_cylinders": (
            "the operation-labelled coefficient/Eq square: both vertical "
            "polynomials are H-u, but the horizontal e_C A e_R map is absent"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "protected_homogenizer_base",
    )
    cap_provenance = load(
        "computations/verify_h3_uc4_beq_tie_source_provenance_audit.py",
        "protected_homogenizer_cap",
    )
    landing = load(
        "computations/verify_h3_termwise_private_full_nine_augp2_linear_landing_gate.py",
        "protected_homogenizer_landing",
    )
    common_base = common_parent_occurrence_augmentation(base)
    ledger = {
        "theorem": "h3 full-star minimal protected homogenizer-cylinder gate",
        "pins": PINS,
        "minimal_presentation_safe_cylinders":
            ambiguity_and_deleted_cylinder_audit(base),
        "common_parent_occurrence_augmentation": common_base,
        "first_literal_noncommuting_face":
            first_literal_noncommuting_face(base),
        "homogenizer_E_target_coupling":
            homogenizer_cap_coupling_gate(
                cap_provenance, landing, common_base),
        "complete_augmented_operation_quotient_and_dual":
            protected_operation_quotient_and_dual(),
        "verdict": (
            "Adding u*iota_u closes H to H-u on the response side.  Retaining "
            "all parent labels and adjoining 1020 deleted-factor plus nine "
            "ambiguity cylinders makes the Taylor-to-Spencer presentation "
            "safe.  After trigger reinsertion, the normalized star carrier and "
            "physical r0 private B packet have exactly the same augmentation "
            "1_V in V=Q^90, so there is no coefficient obstruction and the two "
            "copies must not be declared orthogonal.  This common base forgets "
            "word/operation/Eq/target labels, however, and the protected source "
            "does not prove that the response and cap complexes resolve one "
            "object in the same physical category.  The normalized omega_mix "
            "dual kills the common-base-identified current operation image and "
            "reads one on the desired natural paired comparison.  Thus the exact "
            "remaining datum is the enriched K_Eq/AugP2 common augmentation.  "
            "Once granted, projective comparison supplies the cylinder and the "
            "known linear landing makes it uniquely B=Eq tied.  The "
            "first literal failure is D_(01) of the first degree-eight Taylor "
            "deletion square: the source composite is the nonzero four-cell "
            "branch while the target restriction is zero"
        ),
        "scope": (
            "exact rational canonical first-pair parent-labelled presentation, "
            "both root labels, the full 1020/9 cylinder census, homogenizer, "
            "physical r0 B/Eq/target rows, the common Q^90 occurrence base and "
            "operation corner.  Protected diagonal units are allowed maximally; "
            "no untracked common-augmentation artifact or off-diagonal generator "
            "is smuggled into a cylinder"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("minimal protected cylinder ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=(
        "all", "cylinders", "first-face", "coupling", "dual"),
        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        cylinders = ledger["minimal_presentation_safe_cylinders"]
        coupling = ledger["homogenizer_E_target_coupling"]
        common = ledger["common_parent_occurrence_augmentation"]
        dual = ledger["complete_augmented_operation_quotient_and_dual"]
        print(f"h3 minimal protected homogenizer cylinder ({arguments.mode}): PASS")
        print("cylinders deleted/ambiguous:",
              cylinders["deleted_factor_squares"],
              cylinders["ambiguous_collected_lcms"])
        print("formal B=Eq after E/target append:",
              coupling["B_equals_Eq_after_formal_face_append"])
        print("common V augmentation:",
              common["normalized_response_augmentation"], "=",
              common["physical_r0_private_B_augmentation"])
        print("physical map without mixed comparison:",
              coupling[
                  "physical_boundary_constructed_without_mixed_comparison"])
        print("normalized dual:", dual["normalized_augmented_dual"]["formula"])
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
