#!/usr/bin/env python3
"""Audit the direct primitive-C4/full-site-covariance bridge.

On the four sites P,S,0,1 the direction pairs are the three matchings

    A = PS|01,  B = P0|S1,  C = P1|S0.

The physical site swaps (P 1) and (P 0) send A to B and C respectively.
They fix the response word 11110000 and the residual tail 2345.  Hence one
formal A_[a|b]->B seed, natural under root/endpoint transpose, has all four
K2,2 mates.  In the fixed-window quotient this is exactly the 46->47->48
rank completion.

The covariance is nevertheless a two-object action-groupoid bar.  Canonical
transport to the fixed endpoint object sends its boundary to zero.  The raw
fold has boundary B-A, but lowers H0; the presentation-safe fold necessarily
retains a new carrier t with dGamma=t-(B-A).  Thus covariance organizes the
missing operation-changing generator but does not make it absolute.  The
failure precedes the two response-to-cap word sections and the mixed K_Eq
incidence.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py":
        "2ac01c9ba571338b4c7b779dbc70d5d0eaacb2fe01a4035833970fa6b9826fe0",
    "computations/verify_h3_h2_full_site_groupoid_tag_contraction.py":
        "eb2acb53ca9364ff4639985996f75321800d74b798858cda04084e997a15aa23",
    "computations/verify_h2_endpoint_role_groupoid_pointed_bar_gate.py":
        "24c5504111da4f284d9d01a535de544a44ea1bae75430d98761e093cc6ca8482",
    "computations/verify_uniform_chart_cross_companion_relative_switch_dga_gate.py":
        "e0a8251128174d50b450b3bf85ce0a6870af00d4ab5565e7849fc3c8644c31c6",
    "computations/verify_h3_hyperbolic_root_pair_cross_word_eq_ridge_gate.py":
        "0760703ace1498cc9c255dd8a2017395ece9a7750ab6a21c88233518e1314bba",
    "computations/verify_h3_relative_gl3_bar_keq_kappa_normalization_gate.py":
        "e17de52244d324a26ff6a8b08f9226283b89d1737a6dc3916359991e777efb17",
}
EXPECTED_LEDGER_SHA256 = (
    "3fca6419d4bced6bb90220af649da2bb63ea079e210f34b2dfe18cb4d98ad822"
)

SITES = ("P", "S", "0", "1", "2", "3", "4", "5")
RESPONSE_WORD = tuple(map(int, "11110000"))
CHARTS = (
    frozenset((frozenset(("P", "S")), frozenset(("0", "1")))),
    frozenset((frozenset(("P", "0")), frozenset(("S", "1")))),
    frozenset((frozenset(("P", "1")), frozenset(("S", "0")))),
)
CHART_NAMES = ("A=PS|01", "B=P0|S1", "C=P1|S0")


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def rank(columns) -> int:
    columns = tuple(columns)
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
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


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def apply_site_permutation(chart, permutation):
    return frozenset(frozenset(permutation.get(site, site) for site in edge)
                     for edge in chart)


def apply_word_permutation(word, permutation):
    by_site = dict(zip(SITES, word, strict=True))
    moved = {permutation.get(site, site): colour
             for site, colour in by_site.items()}
    return tuple(moved[site] for site in SITES)


def chart_covariance_audit() -> dict[str, object]:
    sigma_b = {"P": "1", "1": "P"}
    sigma_c = {"P": "0", "0": "P"}
    images_b = tuple(CHARTS.index(apply_site_permutation(chart, sigma_b))
                     for chart in CHARTS)
    images_c = tuple(CHARTS.index(apply_site_permutation(chart, sigma_c))
                     for chart in CHARTS)
    require(images_b == (1, 0, 2) and images_c == (2, 1, 0),
            (images_b, images_c))
    require(apply_word_permutation(RESPONSE_WORD, sigma_b) == RESPONSE_WORD
            and apply_word_permutation(RESPONSE_WORD, sigma_c) == RESPONSE_WORD,
            "endpoint-residual swaps changed the response word")
    require(all(sigma_b.get(site, site) == site
                and sigma_c.get(site, site) == site
                for site in ("2", "3", "4", "5")),
            "a covariance swap moved the fixed C4 tail")

    # Duplicate A by root order.  Root-order and endpoint-chart transpose
    # act independently, so the orbit of one edge is all of K2,2.
    corners = ("A_[a|b]", "A_[b|a]", "B", "C")
    seed = frozenset((0, 2))
    root_flip = (1, 0, 2, 3)
    endpoint_flip = (0, 1, 3, 2)

    def act(edge, permutation):
        return frozenset(permutation[index] for index in edge)

    orbit = {seed}
    changed = True
    while changed:
        before = len(orbit)
        orbit.update(act(edge, root_flip) for edge in tuple(orbit))
        orbit.update(act(edge, endpoint_flip) for edge in tuple(orbit))
        changed = len(orbit) != before
    expected = {
        frozenset((0, 2)), frozenset((0, 3)),
        frozenset((1, 2)), frozenset((1, 3)),
    }
    require(orbit == expected, orbit)
    rows = tuple(tuple(Q(index in edge) for index in range(4))
                 for edge in sorted(orbit, key=lambda value: tuple(value)))
    delta = tuple(map(Q, (1, 1, -1, -1)))
    require(rank(rows) == 3 and all(dot(delta, row) == 0 for row in rows),
            "the covariance mate orbit stopped being the primitive K2,2")
    return {
        "direction_pair_dictionary": {
            "A": "Hasse[2](D=PS,Q01) = PS|01",
            "B": "Hasse[2](P0,S1) = P0|S1",
            "C": "Hasse[2](P1,S0) = P1|S0",
        },
        "site_covariances": {
            "sigma_B": "swap P and residual 1; A<->B, C fixed",
            "sigma_C": "swap P and residual 0; A<->C, B fixed",
        },
        "response_word": "11110000",
        "both_site_covariances_fix_response_word": True,
        "both_site_covariances_fix_tail_2345": True,
        "one_seed": "A_[a|b] -> B",
        "root_endpoint_covariance_orbit": [
            [corners[index] for index in sorted(edge)]
            for edge in sorted(orbit, key=lambda value: tuple(value))
        ],
        "all_four_K22_mates_from_one_natural_schema": True,
        "mate_incidence_rank": rank(rows),
        "formal_alternating_charge": [1, 1, -1, -1],
    }


def fixed_window_rank_audit() -> dict[str, object]:
    fixed = load(
        "computations/verify_h3_fixed_window_centered_k22_physical_routing_gate.py",
        "primitive_covariance_fixed_window",
    )
    columns, detector, candidate_h, candidate_r, packet = (
        fixed.audit_cartesian_physical_packet()
    )
    switch = fixed.audit_operation_switch_boundary(
        columns, candidate_h, candidate_r
    )
    values = tuple(value for _name, value in columns)
    ab = fixed.chart_h_vector(0, fixed.AB_SWITCH)
    ac = fixed.chart_h_vector(0, fixed.AC_SWITCH)
    require(rank(values) == 46
            and rank(values + (ab,)) == 47
            and rank(values + (ab, ac)) == 48
            and dot(detector, candidate_h) == 6,
            "the 46->47->48 primitive switch interface changed")
    require(switch["rank_base_one_switch_candidate"] == [46, 47, 48]
            and switch["rank_base_two_switches_candidate"] == [46, 48, 48],
            switch)
    return {
        "fixed_window_coordinates": packet["physical_output_coordinates"],
        "old_internal_columns": packet["internal_boundary_columns"],
        "old_internal_rank": packet["internal_rank"],
        "one_projected_switch_rank": rank(values + (ab,)),
        "both_projected_switches_rank": rank(values + (ab, ac)),
        "formal_sequence": [46, 47, 48],
        "four_mates_project_to_two_rows": ["A+B", "A+C"],
        "candidate_L_detector_before_switch": str(dot(detector, candidate_h)),
        "coefficient_completion_if_raw_switches_are_absolute": True,
    }


def pointed_groupoid_audit() -> dict[str, object]:
    # One covariance object has chart order (A,B,C), and the other is the
    # sigma_B image.  Its honest bar has three independent boundaries in the
    # six-coordinate two-object module.
    sigma = (1, 0, 2)
    bar = []
    for index in range(3):
        column = [Q(0)] * 6
        column[index] = Q(-1)
        column[3 + sigma[index]] = Q(1)
        bar.append(tuple(column))
    require(rank(bar) == 3 and 6 - rank(bar) == 3,
            "the honest two-object covariance bar changed")

    # Canonical transport applies sigma^{-1}=sigma and sends every boundary
    # to zero.  The raw fold forgets the object without transporting labels;
    # it produces B-A and lowers H0.
    canonical = []
    raw = []
    for column in bar:
        canonical.append(tuple(column[index] + column[3 + sigma[index]]
                               for index in range(3)))
        raw.append(tuple(column[index] + column[3 + index]
                         for index in range(3)))
    require(all(column == (Q(0),) * 3 for column in canonical)
            and rank(raw) == 1
            and raw[0] == tuple(map(Q, (-1, 1, 0))),
            (canonical, raw))

    response = tuple(map(Q, (1, 1, 1)))
    raw_ab = raw[0]
    raw_ac = tuple(map(Q, (-1, 0, 1)))
    require(rank((response,)) == 1
            and 3 - rank((response,)) == 2
            and rank((response, raw_ab, raw_ac)) == 3,
            "absolute raw folds stopped killing the two H0 chart classes")

    # Presentation-safe relative graph with t_B,t_C.  It preserves the old
    # H0 dimension two; imposing t_B=t_C=0 afterward kills it.
    response_ext = tuple(map(Q, (1, 1, 1, 0, 0)))
    graph_b = tuple(map(Q, (-1, 1, 0, -1, 0)))
    graph_c = tuple(map(Q, (-1, 0, 1, 0, -1)))
    t_b_zero = tuple(map(Q, (0, 0, 0, 1, 0)))
    t_c_zero = tuple(map(Q, (0, 0, 0, 0, 1)))
    relative = (response_ext, graph_b, graph_c)
    require(rank(relative) == 3 and 5 - rank(relative) == 2
            and rank(relative + (t_b_zero, t_c_zero)) == 5,
            "the presentation-safe relative switch graph changed")

    # A mixed target-zero complete response does not force the selected raw
    # fold to vanish.  This is the smallest pointed-evaluation guard.
    evaluation = tuple(map(Q, (1, -1, 0)))
    require(dot(response, evaluation) == 0
            and dot(raw_ab, evaluation) == -2,
            "the pointed raw-fold counterevaluation changed")
    return {
        "honest_covariance_bar": {
            "objects": 2,
            "degree_zero_dimension": 6,
            "bar_rank": rank(bar),
            "H0_dimension": 6 - rank(bar),
        },
        "canonical_transport_to_fixed_endpoint_object": {
            "boundary_rank": rank(canonical),
            "result": "zero: transported B is relabelled back to A",
        },
        "raw_untransported_fold": {
            "selected_boundary": "B-A",
            "rank": rank(raw),
            "old_chart_H0_dimension": 2,
            "H0_after_both_absolute_raw_switches": 0,
            "pointed_mixed_evaluation": {"A": 1, "B": -1, "C": 0},
            "complete_response_value": 0,
            "B_minus_A_value": -2,
        },
        "presentation_safe_repair": {
            "dGamma_B": "t_B-(B-A)",
            "dGamma_C": "t_C-(C-A)",
            "extended_dimension": 5,
            "boundary_rank": rank(relative),
            "H0_dimension": 5 - rank(relative),
            "setting_t_B_t_C_zero_H0_dimension": 0,
            "carrier_retained": True,
        },
        "first_unavoidable_failure": (
            "full-site covariance is an honest bar between endpoint-choice "
            "objects, but its only pointed fold either has zero boundary "
            "(canonical transport) or changes H0 (raw fold); the monic "
            "relative fold retains exactly the missing operation carrier"
        ),
    }


def downstream_augmented_audit() -> dict[str, object]:
    hyperbolic = load(
        "computations/verify_h3_hyperbolic_root_pair_cross_word_eq_ridge_gate.py",
        "primitive_covariance_hyperbolic",
    )
    word = hyperbolic.word_section_rank_audit()
    augmented = hyperbolic.paired_reduced_eq_and_ridge_audit()
    require(word["old_relative_cross_word_rank"] == 0
            and word["rank_after_two_root_labelled_arrows"] == 2,
            word)
    require(augmented["strong_grant_base_rank"] == 4
            and augmented["rank_after_paired_mixed_comparison"] == 5
            and augmented["rank_after_paired_shifted_ridge"] == 6,
            augmented)

    bar_keq = load(
        "computations/verify_h3_relative_gl3_bar_keq_kappa_normalization_gate.py",
        "primitive_covariance_bar_keq",
    )
    strict = bar_keq.relative_bar_keq_product_audit()
    grade = bar_keq.gamma_star_grade_audit()
    require(strict["d_squared"] == 0
            and grade["literal_projection_to_C_phys_Gamma_star"]
                == "0 (off-grade)",
            (strict, grade))
    return {
        "operation_switch_stage": (
            "not passed physically: covariance leaves t_B,t_C retained"
        ),
        "conditional_two_root_word_sections": {
            "response_word": word["full_response_word"],
            "cap_word": word["full_cap_word"],
            "old_rank": word["old_relative_cross_word_rank"],
            "rank_after_both_root_labelled_arrows":
                word["rank_after_two_root_labelled_arrows"],
            "supplied_by_site_covariance_bridge": False,
        },
        "conditional_mixed_K_Eq_and_ridge": {
            "base_to_paired_mixed": [4, 5],
            "after_paired_ridge": 6,
            "mixed_detector_value": 1,
            "ridge_detector_value": 1,
            "supplied_by_objectwise_bar_times_K_Eq": False,
        },
        "strict_bar_times_K_Eq_control": {
            "strict_relative_square_exists": True,
            "d_squared": strict["d_squared"],
            "Gamma_star_projection":
                grade["literal_projection_to_C_phys_Gamma_star"],
            "reason": (
                "multiplication by K_Eq preserves the endpoint-choice/bar, "
                "fine, repeated and operation idempotents; it does not "
                "create the response-to-cap mixed incidence"
            ),
        },
        "protected_readouts": {
            "target": (
                "the response word is mixed and fixed by both site swaps; "
                "the honest two-object bar is target-safe"
            ),
            "fixed_tail": "2345 and its three C4 matchings are fixed",
            "word_fine_repeated_operation": (
                "the raw fold changes Hasse[2](D,Q01) to Hasse[2](P,S); "
                "this is the missing operation idempotent, not an old face"
            ),
            "q_anchor_W_ordinary_residue_ridge_eta_sigma": (
                "no value is inferred: the obstruction occurs before a "
                "fixed-source operation column on which these maps act"
            ),
        },
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 primitive-C4/full-site-covariance pointed bridge gate",
        "pins": PINS,
        "literal_chart_covariance": chart_covariance_audit(),
        "fixed_window_rank_interface": fixed_window_rank_audit(),
        "pointed_action_groupoid": pointed_groupoid_audit(),
        "downstream_word_K_Eq_and_readouts": downstream_augmented_audit(),
        "verdict": (
            "The full-site covariance idea is coefficient-exact and stronger "
            "than the fixed-chart C4 shadow: endpoint-residual site swaps fix "
            "word 11110000 and tail 2345, send DQ to the two PS charts, and "
            "the symmetry orbit of one A_[a|b]->B seed gives all four K2,2 "
            "mates.  If the two raw folds were absolute they would realize "
            "the exact rank 46->47->48 completion.  They are not absolute "
            "physical boundaries.  The honest covariance bar lives between "
            "endpoint-choice objects; canonical transport makes its boundary "
            "zero, while the untransported fold B-A changes H0.  The unique "
            "presentation-safe descent retains t_B,t_C, exactly the missing "
            "operation-changing carriers.  Therefore primitive C4 plus "
            "covariance does not construct even the first physical switch; "
            "the two root word sections and mixed K_Eq/ridge ranks remain "
            "strictly downstream independent increments."
        ),
        "shortest_positive_datum": (
            "a pointed endpoint-choice descent/augmentation functor whose "
            "fixed-source fold sends the honest covariance bar to B-A and "
            "C-A while preserving H0; equivalently, a physical landing for "
            "the retained relative carriers t_B,t_C.  Once one seed landing "
            "is natural under root and endpoint transpose, all four mates and "
            "the 46->48 coefficient completion follow automatically."
        ),
        "scope": (
            "exact h3 fixed-window rational rank, literal K8 site-action, "
            "pointed groupoid/H0, two-root word-section and mixed K_Eq/ridge "
            "quotients.  It does not classify an unwritten higher physical "
            "operation or promote the local H0 detector to a terminal."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "chart", "groupoid", "downstream"),
                        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        key = {
            "chart": "fixed_window_rank_interface",
            "groupoid": "pointed_action_groupoid",
            "downstream": "downstream_word_K_Eq_and_readouts",
        }.get(arguments.mode)
        payload = ledger if key is None else ledger[key]
        print(json.dumps({"mode": arguments.mode, "ledger": payload,
                          "sha256": digest}, indent=2, sort_keys=True))
        return
    print(f"primitive-C4/covariance bridge ({arguments.mode}): PASS")
    print("one seed covariance orbit: all four K2,2 mates")
    print("formal fixed-window ranks: 46 -> 47 -> 48")
    print("pointed fixed-source fold: RELATIVE ONLY; t_B,t_C retained")
    print("root word sections and mixed K_Eq incidence: DOWNSTREAM OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
