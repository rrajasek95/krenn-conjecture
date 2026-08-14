#!/usr/bin/env python3
"""Build the minimal first-collision EqSystem-to-AugP2 bimodule candidate.

At aggregate level the response collision and cap complexes are

    <C_ab,rho> --d--> <R_ab,rho>,
    <r0_rho>   --d--> <E_rho>.

A normalized chain map has coefficients a_rho,b_rho with a_rho=b_rho.
Full AB/AC naturality and one monic normalization make the four scalar
coefficients unique: all are one.

The literal fine expansion does not close with only the forced components.
The official collision has 30 terms.  Projection to the physical direct-free
chart retains 24 (12 per ordered branch).  Private deletion followed by
reinsertion maps those 24 terms to 24 distinct terms of the 90-term cap Eq
row, leaving an exact 66-term Eq complement per root.  Thus the coarse formal
bimodule is unique, but the minimal literal termwise candidate is not a chain
map; it has 132 unmatched Eq terms over AB and AC.

Before that coefficient debt can be interpreted physically, the candidate
also requires the four fixed-window DQ/PS K2,2 mates.  They form the exact
rank-three formal incidence orbit, but none is an implemented cross-profile
source boundary.  The first seed A_[a|b]->B is already rank-raising.  The
honest covariance bar either folds to zero or changes H0; its presentation-
safe form retains the missing carrier.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_first_site_repeating_collision_tate_augp2_operation_no_go.py":
        "7f32228b0c9c05d6ed12811bafb171b844fe7bc82647ace9a11ff9b6d9383161",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_uc4_beq_tie_source_provenance_audit.py":
        "f237ccffd40863a201b780ea034fcbd7781bc555e1fbc6f528d99d3ab71394c6",
    "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py":
        "2ac01c9ba571338b4c7b779dbc70d5d0eaacb2fe01a4035833970fa6b9826fe0",
    "computations/verify_h3_primitive_c4_covariance_pointed_bridge_gate.py":
        "a14339fee59134b28229fb17fcae2292bc544264ea829db60c953875f96fef41",
    "computations/verify_h3_phi_ks_r0_word_operation_reachability_no_go.py":
        "3b2cf3aa1cd6ee46f60c0e3621342f4eb15420d6d5d302546b2403d966703ba8",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "computations/verify_h3_termwise_private_full_nine_augp2_linear_landing_gate.py":
        "9c182f13ba4da4f2dd3ff49fd9ebf60dd1a218f53cbf4416e82a63236f57404f",
}
EXPECTED_LEDGER_SHA256 = "e43a61470a678509cf6f5351868e94797e17897cc8b72979cd1ac279375a4995"

A = (0, 1, 1, 1)
B = (0, 7, 1, 1)
PURE_ONE = (1,) * 8
ROOT_LABELS = ("AB", "AC")
MATE_NAMES = (
    "A_[a|b]->B", "A_[a|b]->C",
    "A_[b|a]->B", "A_[b|a]->C",
)


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


def rank(columns) -> int:
    columns = tuple(tuple(map(Q, column)) for column in columns)
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank width")
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


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def aggregate_chain_map_audit(first_collision, cap_provenance):
    first_ledger, first_digest = first_collision.audit()
    require(first_digest == first_collision.EXPECTED_LEDGER_SHA256,
            first_digest)
    collision = first_ledger["universal_mixed_collision_Tate_cell"]
    require(collision["boundary_support"] == 30
            and collision["primitive_second_Hasse_face"] == 0
            and collision["cap_r0_component"] == 0,
            collision)

    cap_provenance.pin_dependencies()
    cap = cap_provenance.cap_r0_provenance_audit()
    require(cap["internal_cap_differential"] == "d r_0=(H_0-u)e_Eq"
            and cap["internal_B_equals_Eq_tie"],
            cap)

    # Variables are (a_AB,b_AB,a_AC,b_AC), where Phi_1(C)=a*r0 and
    # Phi_0(R)=b*E.  Since dC=R and dr0=E, dPhi=Phi d gives a=b.
    equations = (
        (Q(1), Q(-1), Q(0), Q(0)),
        (Q(0), Q(0), Q(1), Q(-1)),
        (Q(1), Q(0), Q(-1), Q(0)),
        (Q(0), Q(1), Q(0), Q(-1)),
        (Q(1), Q(0), Q(0), Q(0)),  # monic inhomogeneous equation a_AB=1
    )
    homogeneous = equations[:-1]
    solution = (Q(1), Q(1), Q(1), Q(1))
    require(rank(equations) == 4
            and all(dot(row, solution) == 0 for row in homogeneous)
            and dot(equations[-1], solution) == 1,
            "aggregate bimodule solution changed")
    return {
        "response_complex": "<C_ab,rho> --d--> <R_ab,rho>",
        "cap_complex": "<r0_rho> --d--> <E_rho>",
        "variables": ["a_AB", "b_AB", "a_AC", "b_AC"],
        "chain_map_equations": ["a_AB=b_AB", "a_AC=b_AC"],
        "root_naturality": ["a_AB=a_AC", "b_AB=b_AC"],
        "normalization": "a_AB=1",
        "equation_rank": rank(equations),
        "formal_solution_dimension": 0,
        "unique_solution": [1, 1, 1, 1],
        "solution_text": (
            "C_ab,AB/AC -> r0_AB/AC and R_ab,AB/AC -> E_AB/AC"
        ),
        "B_Eq_tied": True,
        "coarse_formal_bimodule_exists_uniquely": True,
    }


def remove_one(monomial, cell):
    terms = list(monomial)
    require(cell in terms, ("cell missing", cell, monomial))
    terms.remove(cell)
    return tuple(sorted(terms))


def repeated_sites(monomial):
    counts = Counter(site for cell in monomial for site in cell[:2])
    return tuple(sorted(site for site, count in counts.items() if count > 1))


def literal_termwise_boundary_audit(base):
    cap_terms = tuple(base.full_row(PURE_ONE))
    cap_set = set(cap_terms)
    through_a = tuple(monomial for monomial in cap_terms if A in monomial)
    through_b = tuple(monomial for monomial in cap_terms if B in monomial)
    complement = tuple(monomial for monomial in cap_terms
                       if A not in monomial and B not in monomial)
    require(len(cap_terms) == 90
            and len(through_a) == len(through_b) == 12
            and not set(through_a) & set(through_b)
            and len(complement) == 66,
            (len(cap_terms), len(through_a), len(through_b), len(complement)))

    records = []
    source_terms = set()
    landed_cap_terms = set()
    for branch, selected, inserted, sign, monomials in (
        ("a|b", A, B, 1, through_a),
        ("b|a", B, A, -1, through_b),
    ):
        for monomial in monomials:
            remainder = remove_one(monomial, selected)
            source_term = tuple(sorted((inserted,) + remainder))
            require(repeated_sites(source_term),
                    ("collision face lost repeated site", source_term))
            # The orientation-corrected termwise map sends a signed source
            # face to sign times the reconstructed cap term, so the product
            # with its boundary coefficient contributes +1 to E.
            reconstructed = tuple(sorted((selected,) + remainder))
            require(reconstructed == monomial and reconstructed in cap_set,
                    "private deletion/reinsertion failed")
            source_terms.add((branch, source_term))
            landed_cap_terms.add(reconstructed)
            records.append({
                "branch": branch,
                "boundary_sign": sign,
                "map_sign": sign,
                "source_repeated_sites": list(repeated_sites(source_term)),
                "fine": repr(source_term),
                "cap_term": repr(reconstructed),
            })
    require(len(records) == len(source_terms) == len(landed_cap_terms) == 24,
            "direct-free collision face count changed")
    residual = cap_set - landed_cap_terms
    require(len(residual) == 66 and residual == set(complement),
            "cap Eq complement changed")

    # Root labels are literal direct-sum copies.  No cancellation is allowed
    # between them.
    root_records = tuple((root, record["branch"], record["fine"])
                         for root in ROOT_LABELS for record in records)
    root_residual = tuple((root, repr(monomial))
                          for root in ROOT_LABELS for monomial in residual)
    require(len(root_records) == 48 and len(set(root_records)) == 48
            and len(root_residual) == 132 and len(set(root_residual)) == 132,
            "root-labelled termwise counts changed")
    return {
        "official_collision_terms_before_chart_projection": 30,
        "direct_free_pair": sorted(base.DIRECT_FREE_PAIR),
        "physical_cap_Eq_terms_per_root": len(cap_terms),
        "collision_terms_per_ordered_branch_after_projection": [12, 12],
        "collision_terms_per_root_after_projection": len(records),
        "root_labels": list(ROOT_LABELS),
        "complete_root_labelled_collision_faces": len(root_records),
        "termwise_private_landing_terms_per_root": len(landed_cap_terms),
        "unmatched_cap_Eq_terms_per_root": len(residual),
        "complete_unmatched_root_labelled_Eq_terms": len(root_residual),
        "first_three_unmatched_Eq_terms": sorted(map(repr, residual))[:3],
        "private_face_rule": (
            "delete inserted a/b, reinsert selected b/a, and use the branch "
            "orientation twice so every landed Eq coefficient is +1"
        ),
        "dPhi_minus_Phi_d_on_landed_terms": 0,
        "dPhi_minus_Phi_d_on_Eq_complement": 1,
        "minimal_termwise_candidate_is_chain_map": False,
        "first_coefficient_boundary_debt": (
            "the 66 direct-free H_1 matching terms containing neither "
            "01:11 nor 07:11, separately on AB and AC"
        ),
    }


def four_mate_provenance_audit(bridge, reachability, fixed_window):
    bridge_ledger, bridge_digest = bridge.audit()
    require(bridge_digest == bridge.EXPECTED_LEDGER_SHA256,
            bridge_digest)
    chart = bridge_ledger["literal_chart_covariance"]
    interface = bridge_ledger["fixed_window_rank_interface"]
    groupoid = bridge_ledger["pointed_action_groupoid"]
    require(tuple(tuple(pair) for pair in chart["root_endpoint_covariance_orbit"])
                == (("A_[a|b]", "B"), ("A_[a|b]", "C"),
                    ("A_[b|a]", "B"), ("A_[b|a]", "C"))
            and chart["mate_incidence_rank"] == 3
            and chart["all_four_K22_mates_from_one_natural_schema"]
            and interface["formal_sequence"] == [46, 47, 48],
            (chart, interface))

    reach_ledger, reach_digest = reachability.audit()
    require(reach_digest == reachability.EXPECTED_LEDGER_SHA256,
            reach_digest)
    operation = reach_ledger["fixed_window_operation_gate"]
    first_edge = reach_ledger["first_new_edge"]
    require(operation["cross_profile_edges_present_in_internal_constructor"] == 0
            and tuple(operation["formal_cross_profile_edges"])
                == tuple([name.split("->") for name in MATE_NAMES])
            and first_edge["fixed_window_representative"] == "A_[a|b] -> B",
            (operation, first_edge))

    columns, _detector, candidate_h, candidate_r, packet = (
        fixed_window.audit_cartesian_physical_packet())
    switch = fixed_window.audit_operation_switch_boundary(
        columns, candidate_h, candidate_r)
    require(packet["internal_boundary_columns"] == 100
            and packet["internal_rank"] == 46
            and switch["operation_profile_changing_edges"] == 4
            and switch["rank_base_one_switch_candidate"] == [46, 47, 48],
            (packet, switch))

    mate_columns = (
        (Q(1), Q(0), Q(1), Q(0)),
        (Q(1), Q(0), Q(0), Q(1)),
        (Q(0), Q(1), Q(1), Q(0)),
        (Q(0), Q(1), Q(0), Q(1)),
    )
    balanced = (Q(1), Q(1), Q(-1), Q(-1))
    require(rank(mate_columns) == 3
            and all(dot(balanced, column) == 0 for column in mate_columns),
            "formal K2,2 mate incidence changed")
    return {
        "formal_mates": list(MATE_NAMES),
        "formal_mate_incidence_rank": rank(mate_columns),
        "balanced_covector": [1, 1, -1, -1],
        "all_four_forced_by_one_root_endpoint_natural_schema": True,
        "internal_fixed_window_columns_rank": [
            packet["internal_boundary_columns"], packet["internal_rank"]],
        "implemented_cross_profile_edges":
            operation["cross_profile_edges_present_in_internal_constructor"],
        "rank_after_first_formal_switch": interface["one_projected_switch_rank"],
        "rank_after_two_projected_switch_types":
            interface["both_projected_switches_rank"],
        "first_operation_unmatched_face": "A_[a|b]->B",
        "first_seed_is_rank_raising": True,
        "covariance_bar_test": {
            "canonical_fixed-object_fold_boundary_rank":
                groupoid["canonical_transport_to_fixed_endpoint_object"]
                    ["boundary_rank"],
            "raw_fold_B_minus_A_value":
                groupoid["raw_untransported_fold"]["B_minus_A_value"],
            "presentation_safe_carrier_retained":
                groupoid["presentation_safe_repair"]["carrier_retained"],
            "retained_differentials": [
                groupoid["presentation_safe_repair"]["dGamma_B"],
                groupoid["presentation_safe_repair"]["dGamma_C"],
            ],
        },
        "source_provenant_absolute_mates": False,
        "reason": (
            "canonical transport makes the covariance boundary zero; the raw "
            "fold changes H0; the unique presentation-safe descent retains "
            "t_B,t_C instead of producing an absolute DQ/PS edge"
        ),
    }


def downstream_guard(packaging):
    ledger, digest = packaging.audit()
    require(digest == packaging.EXPECTED_LEDGER_SHA256, digest)
    package = ledger["augmented_packaging"]
    require(package["packaging_quotient_rows"] == [
                "hidden lower/P2", "central Eq", "mixed incidence", "shifted ridge"
            ]
            and package["rank_before_mixed_cell"] == 2
            and package["rank_after_mixed_cell"] == 3
            and package["rank_after_labelled_ridge"] == 4,
            package)
    return {
        "four_packaging_directions": package["packaging_quotient_rows"],
        "status": "downstream only: not used to manufacture the four DQ/PS mates",
        "rank_sequence_after_word_operation_switch": [2, 3, 4],
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    first_collision = load(
        "computations/verify_h3_first_site_repeating_collision_tate_augp2_operation_no_go.py",
        "minimal_bimodule_first_collision",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "minimal_bimodule_base",
    )
    cap_provenance = load(
        "computations/verify_h3_uc4_beq_tie_source_provenance_audit.py",
        "minimal_bimodule_cap",
    )
    bridge = load(
        "computations/verify_h3_primitive_c4_covariance_pointed_bridge_gate.py",
        "minimal_bimodule_bridge",
    )
    reachability = load(
        "computations/verify_h3_phi_ks_r0_word_operation_reachability_no_go.py",
        "minimal_bimodule_reachability",
    )
    fixed_window = load(
        "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py",
        "minimal_bimodule_fixed_window",
    )
    packaging = load(
        "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py",
        "minimal_bimodule_packaging",
    )

    ledger = {
        "theorem": "h3 first-collision minimal EqSystem-to-AugP2 bimodule candidate",
        "pins": PINS,
        "coarse_mapping_cylinder":
            aggregate_chain_map_audit(first_collision, cap_provenance),
        "complete_repeated_fine_root_boundary":
            literal_termwise_boundary_audit(base),
        "four_primitive_DQ_PS_mate_provenance":
            four_mate_provenance_audit(bridge, reachability, fixed_window),
        "downstream_packaging_guard": downstream_guard(packaging),
        "verdict": (
            "The aggregate two-term EqSystem-to-AugP2 chain map exists uniquely "
            "after monic normalization and AB/AC naturality.  Expanding the "
            "same candidate in the literal physical chart exposes its first "
            "coefficient debt: the collision supplies 24 of the 90 cap Eq "
            "terms per root and leaves the 66 terms containing neither first-"
            "pair edge, hence 132 unmatched root-labelled faces.  Even before "
            "filling that debt physically, the mapping cylinder requires the "
            "four DQ/PS K2,2 mates.  They form the correct rank-three formal "
            "naturality orbit, but the implemented fixed-window constructor "
            "contains zero cross-profile edges; the first seed A_[a|b]->B is "
            "rank-raising, and covariance supplies only a retained relative "
            "carrier.  Therefore the smallest candidate is unique coarsely but "
            "not a source-provenant literal dg bimodule"
        ),
        "scope": (
            "exact canonical first pair, direct-free 90-term chart, two root "
            "labels, four fixed-window K2,2 mates and current source APIs.  "
            "The packaging quotient directions are checked only downstream; "
            "no arbitrary non-diagonal 90-by-24 formal map is admitted"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("minimal first-collision bimodule ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "coarse", "boundary",
                                           "mates", "downstream"),
                        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h3 first-collision minimal bimodule ({arguments.mode}): PASS")
        print("coarse normalized chain map: UNIQUE")
        print("literal direct-free collision faces: 24/root; Eq debt: 66/root")
        print("four formal DQ/PS mates: RANK 3; physical mates: ZERO")
        print("first operation face: A_[a|b]->B; relative carrier only")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
