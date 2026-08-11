#!/usr/bin/env python3
"""Exact reduced-companion/Tor gate for the Component-IV chain.

The endpoint bars leave fifteen matching-labelled companions q_(v,N).
Matching incidence/Euler reduces them to five face classes h_v.  This
checker follows the complete natural next layer (the cubic C5 first Tor and
its unique degree-five compatibility), and then states the exact universal
denominator transgression needed for a physical augmentation.

It does not declare the missing relative cells and does not treat the two
rational Tor packets as points of the full source scheme.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

import verify_h3_component_iv_endpoint_word_change_cokernel as ENDPOINT
import verify_h3_component_iv_first_new_source_row_no_go as OLD_NO_GO
import verify_h3_denominator_tor_transgression_fitting_gate as TRANS
import verify_h3_rootless_five_cycle_denominator_pp_aggregate_no_go as PP
import verify_h3_rootless_five_cycle_first_tor_multidegree_gate as FIRST_TOR
import verify_h3_rootless_five_ridge_common_q_euler_cokernel as EULER


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_DIGEST = "2758e19f5a91abf7637ff5388d006ca53f6d03479825d379d30bc4e93b33e4ac"
PINS = {
    "computations/verify_h3_component_iv_endpoint_word_change_cokernel.py":
        "e452467b235391fa434ddd10364bd27a35fe32791fab8e07e5c4576dd5f5b5eb",
    "computations/verify_h3_component_iv_first_new_source_row_no_go.py":
        "42d168c0f5ee3f18ca5e9e1e2990efcdf1ab8a581fb8ed47ce354b036a5afe5b",
    "computations/verify_h3_rootless_five_ridge_common_q_euler_cokernel.py":
        "caed56942bf3f74aa2942c7924200d8cfac6190665fe7f53e47bb9ccd36b5e27",
    "computations/verify_h3_rootless_five_cycle_first_tor_multidegree_gate.py":
        "a5d9021664b904f895323c29806a825545afd16085c971dc573353bb6c11a81f",
    "computations/verify_h3_rootless_five_cycle_denominator_pp_aggregate_no_go.py":
        "4f691d119469e76436e36566a1ca7307bc49a52f66b0687c1554a9e6531ec4de",
    "computations/verify_h3_rootless_five_cycle_tate_anchor_obstruction.py":
        "a1383c13a732ec34eda5614c4346fecfd99b960480727ba26ac7089690844936",
    "computations/verify_h3_denominator_tor_transgression_fitting_gate.py":
        "33cd6ac3de85f83ee16189601930938d73f35f2fef5db20253380801bdd78459",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))


def matching_to_face_reduction():
    endpoint = ENDPOINT.complete_source_routes()
    chart25 = ENDPOINT.chart25_scope_guard()
    module = endpoint["module"]
    require(module["ambient_rank"] == 20
            and module["route_columns"] == 15
            and module["available_rank"] == 15
            and module["primitive_cokernel_rank"] == 5
            and module["cokernel"] == "Z^5",
            "endpoint companion module changed")

    polynomials = EULER.common_q_polynomials()
    euler = EULER.integral_module()
    require(len(polynomials) == 5
            and euler["ambient_rank"] == 110
            and euler["available_rank"] == 105
            and euler["primitive_cokernel_rank"] == 5
            and euler["cokernel"] == "Z^5"
            and euler["pure_H_intersection"]
            == "relation span intersects span{H_1,...,H_5} in 0",
            "complete matching/Euler quotient changed")
    return {
        "matching_labelled_routes": 15,
        "endpoint_ambient_rank": 20,
        "endpoint_rank": 15,
        "after_all_matching_Euler_and_two_chart_rows": {
            "ambient_rank": 110,
            "rank": 105,
            "cokernel": "Z^5",
            "surviving_classes": [f"h_{v}" for v in range(1, 6)],
        },
        "chart25_scope_guard": chart25,
        "interpretation": (
            "the three q_(v,N) labels on one face package into h_v, but "
            "no old incidence/Euler/chart row removes that face class"
        ),
    }


def derived_cycle_inventory():
    generators = FIRST_TOR.c5_generators()
    syzygies, resolution = FIRST_TOR.first_tor_resolution(generators)
    augmentation = FIRST_TOR.augmentation_and_diagonal_guard(
        syzygies, generators
    )
    selected, _records = PP.specialized_denominator_inventory()
    pp_records, ridge_columns, residual_columns = PP.pp_to_first_tor(selected)
    pp_guard = PP.selector_and_readout_no_go(ridge_columns, residual_columns)

    require(resolution["first_Betti"] == {"edge_degree_3": 5}
            and resolution["unique_second_syzygy"]["edge_degree"] == 5,
            "minimal C5 resolution changed")
    require(augmentation["first_syzygy_augmentation_rank"] == 4
            and augmentation["ridge_relation_rank_at_guard"] == 4
            and augmentation["surviving_covector"] == "sum_v lambda_v",
            "first-Tor primitive quotient changed")
    require(len(pp_records) == 5
            and pp_guard["ridge_rank_after_all_cubic_PP_pairs"] == 4
            and pp_guard["surviving_fifth_aggregate"] == "sum_v lambda_v",
            "physical PP realization changed")

    # On the Laurent diagonal point, the five cubic cells are the oriented
    # incidence columns of C5.  The unique degree-five cell is a relation
    # among those columns, so it adds no new image.  Appending one primitive
    # face basis vector raises rank from four to five with determinant +/-1.
    incidence = []
    for index in range(5):
        column = [0] * 5
        column[index] = -1
        column[(index + 1) % 5] = 1
        incidence.append(column)
    require(FIRST_TOR.rank(incidence) == 4
            and all(sum(column) == 0 for column in incidence),
            "C5 incidence separator changed")
    primitive = [1, 0, 0, 0, 0]
    require(FIRST_TOR.rank(incidence + [primitive]) == 5,
            "primitive face stopped closing the C5 quotient")

    return {
        "specialized_companions": [list(value) for value in generators],
        "minimal_resolution": "5 generators at degree 2; 5 at degree 3; 1 at degree 5",
        "physical_cubic_PP_cells": len(pp_records),
        "cubic_boundary_rank": 4,
        "degree_five_cell": (
            "the unique compatibility among the five cubic cells; its "
            "boundary is already in their kernel and adds no face image"
        ),
        "surviving_primitive_separator": "(1,1,1,1,1)",
        "rank_after_entire_C5_resolution": 4,
        "rank_after_one_primitive_face_augmentation": 5,
        "source_multidegree_of_first_visible_cells": "P3 disjoint-union K2",
    }


def exact_transgression_gate():
    universal = TRANS.universal_audit()
    direct_free = TRANS.packet_audit("direct_free")
    tilted = TRANS.packet_audit("tilted")
    require(universal["full_rank"] == 15
            and universal["unselected_rank"] == 10,
            "universal denominator presentation changed")
    require(direct_free["transgression_rank"] == 4
            and tilted["transgression_rank"] == 3,
            "packet transgression counterguards changed")

    # This is the exact algebraic form of a reduced augmentation.  With
    # C_sel generated by d_(v,m_v), cap projection is the selected
    # coefficient.  A lift of every basis vector is equivalent to
    # b_sel(S^5) being contained in im(b_oth), i.e. surjectivity of tau.
    selected = [f"d_({v},{TRANS.MIXED[v - 1]})" for v in TRANS.SITES]
    return {
        "universal_b_rank": universal["full_rank"],
        "universal_unselected_rank": universal["unselected_rank"],
        "universal_kernel": 0,
        "selected_generators": selected,
        "source_ring": "S=(full-nine source quotient)[kappa^-1]",
        "five_augmentation_condition": (
            "for every v, b(d_(v,m_v)) belongs to im(b_oth) over S"
        ),
        "equivalent_condition": (
            "tau: Tor_1(coker b,S)=ker(b tensor S) -> S^5 is onto"
        ),
        "required_kernel_vectors": (
            "k_v=d_(v,m_v)+sum_(u,c!=m_u) z_(u,c)d_(u,c), "
            "b(k_v)=0, tau(k_v)=e_v"
        ),
        "direct_free_counterguard": {
            "is_full_source_point": False,
            "tor_dimension": direct_free["tor1_dimension"],
            "transgression_rank": direct_free["transgression_rank"],
            "cokernel_dimension": direct_free["transgression_cokernel_dimension"],
        },
        "tilted_counterguard": {
            "is_full_source_point": False,
            "tor_dimension": tilted["tor1_dimension"],
            "transgression_rank": tilted["transgression_rank"],
            "cokernel_dimension": tilted["transgression_cokernel_dimension"],
        },
    }


def ordinary_row_scope():
    lock = OLD_NO_GO.all_word_polynomial_lock()
    require(lock["EqSystem_rows"] == 3 ** 8
            and lock["verdict"]
            == "no chain has (boundary,target,ores)=(kappa*Y*w,0,0)",
            "ordinary full-word no-go changed")
    return {
        "ordinary_EqSystem_rows": lock["EqSystem_rows"],
        "arbitrary_polynomial_multipliers": True,
        "verdict": "the completed n_c cannot be assembled inside the old row-plus-cap module",
        "remaining_scope": (
            "a new relative/Tor cell created by the full-source quotient is not excluded"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "scope": "h=3 Component-IV reduced companion augmentation",
        "matching_to_face_reduction": matching_to_face_reduction(),
        "complete_next_derived_inventory": derived_cycle_inventory(),
        "ordinary_row_scope": ordinary_row_scope(),
        "exact_missing_transgression": exact_transgression_gate(),
        "verdict": {
            "five_source_provenant_augmentations_constructed": False,
            "primitive_separator_persists": True,
            "first_new_transgression": (
                "five full-source denominator Tor kernel vectors whose "
                "selected cap projections form the identity of S^5"
            ),
            "not_licensed": (
                "the cubic formal C5 syzygies, degree-five Tate relation, "
                "or chart-25 projection cannot be renamed as those vectors"
            ),
        },
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, ("ledger changed", digest))

    print("h=3 Component-IV reduced companion/Tor gate: PASS")
    print("old matching/Euler/bar module: primitive coker Z^5")
    print("cubic PP + degree-five C5 compatibility: rank 4, one aggregate survives")
    print("five physical reduced augmentations: NOT CONSTRUCTED")
    print("exact next test: five selected denominator-column memberships over the full-source quotient")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
