#!/usr/bin/env python3
"""Combine the even target cone and K_Eq face at the canonical E14 S-pair.

The derived Cartan/Spencer triangle closes target and reduced Eq, but has no
E14 occurrence boundary.  The canonical unary S-pair gives an exact identity

    B = U + R,

where B is the twelve-tail E14 target, U is an old unary column, and
R=(p1*s1)u35*v24*(1-v04) is the private return.  Hence a physical K_Eq
dressing lands the required companion if and only if its lower/private face
is placed on R.  The nearest physical dressing then leaves exactly one
word-resolved labelled-residue row.  This checker freezes both alternatives
and their primitive duals.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_e14_first_hit_dual_endpoint_q_extension_gate.py":
        "4d25b285b22e8a166a5e005a20e59cec11f463d25840f45a8acc4547d9e649ec",
    "notes/h3-e14-first-hit-dual-endpoint-q-extension-gate.md":
        "e841abbfe5d9da98ff041a448959d56ebb3059121ce080a28c0e8608a76c2605",
    "computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py":
        "767aa83dce1daee7e615cbeb5684662714bb0e377822805541172581adc2490f",
    "notes/h2-sigma-even-cartan-spencer-cone-residual.md":
        "5e70446f93f2f7c348c43653cfe05a20033ae292c845e924e02b4afca35b4dcb",
    "computations/verify_h3_cplus_root_even_koszul_physical_dressing_gate.py":
        "9bd2c9f482dc3277d07bd96a4e2189034e766f97e7800d3864179a75e03cef17",
    "notes/h3-cplus-root-even-koszul-physical-dressing-gate.md":
        "c21d7e3e140d2d86d040f9928c787011a7b49e9c58493f812086065c05715e9b",
    "computations/verify_h3_cplus_q_ridge_w_terminal_reduction.py":
        "b2ace6e49aa5ec1b8347a0e88cc39f36e5d773e1aab1d82f424533de8ce52a9a",
    "notes/h3-cplus-q-ridge-w-terminal-reduction.md":
        "856a4932b1c28dfba34195fa2b37dbf0b3a54cbc98e1f80fe0195535885a7e69",
}
EXPECTED_LEDGER_SHA256 = (
    "c044c59891a25d2618cf0a881150089117bd4da1f273f020eca7d20e11b96885"
)

ENDPOINT = ("p1_0_1", "s1_1_1")
COMPANION = (ENDPOINT, ("u05_01", "v1301", "v2411"))
RETURN = {
    (ENDPOINT, ("u35_11", "v2411")): Q(1),
    (ENDPOINT, ("u35_11", "v0400", "v2411")): Q(-1),
}


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


def sparse_add(*terms):
    answer = {}
    for coefficient, vector in terms:
        for coordinate, value in vector.items():
            total = answer.get(coordinate, Q(0)) + Q(coefficient) * Q(value)
            if total:
                answer[coordinate] = total
            elif coordinate in answer:
                del answer[coordinate]
    return answer


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(columns):
    require(columns, "rank needs columns")
    rows = [list(map(Q, row)) for row in zip(*columns, strict=True)]
    height = len(rows)
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


def e14_spair_identity(endpoint_q):
    data = endpoint_q.reconstruct_first_hit()
    target = data["target"]
    unary = data["columns"][data["selected_name"]]
    private_return = sparse_add((1, target), (-1, unary))
    require(private_return == RETURN,
            ("the canonical unary S-pair return changed", private_return))
    require(target[COMPANION] == unary[COMPANION] == -1
            and COMPANION not in private_return,
            "the required companion coefficient changed")
    require(endpoint_q.pair(data["dual"], unary) == 0
            and endpoint_q.pair(data["dual"], private_return) == -1
            and endpoint_q.pair(data["dual"], target) == -1,
            "the unary/private/target dual identity changed")

    # Even an unrealistically generous grant of every literal unary and G11
    # target-readout coordinate cannot supply R: the same two-term private
    # return remains.  This proves that the first missing row is occurrence,
    # not target-normal, after the formal target/Eq cone is closed.
    first = data["first"]
    coordinates = set(target)
    for column in data["columns"].values():
        coordinates.update(column)
    target_coordinates = sorted(
        coordinate for coordinate in coordinates
        if coordinate[0][0].startswith("target")
    )
    pivots = {}
    for column in data["columns"].values():
        first.add_exact_column(column, pivots)
    old_rank = len(pivots)
    for coordinate in target_coordinates:
        first.add_exact_column({coordinate: Q(1)}, pivots)
    target_granted_rank = len(pivots)
    reduced_after_target_grant = first.exact_reduce(target, pivots)
    require(old_rank == 269 and len(target_coordinates) == 24
            and target_granted_rank == 293
            and reduced_after_target_grant == RETURN,
            ("the strongest target-readout grant changed",
             old_rank, target_granted_rank, reduced_after_target_grant))
    return data, {
        "old_unary_column": "U[000101]*v24_11",
        "exact_identity": "B_E14=U[000101]*v24_11+R_E14",
        "private_return": (
            "R_E14=(p1_0_1*s1_1_1)*u35_11*v24_11*(1-v04_00)"
        ),
        "companion": list(COMPANION[1]),
        "companion_coefficient_in_U_and_B": -1,
        "companion_coefficient_in_R": 0,
        "dual_values": {"U": 0, "R": -1, "B": -1},
        "all_target_readout_coordinates_granted": len(target_coordinates),
        "rank_after_all_target_readout_units": target_granted_rank,
        "remainder_after_all_target_readout_units": (
            "R_E14, unchanged"
        ),
    }


def derived_target_eq_combination(sigma_cone):
    cone_ledger, cone_digest = sigma_cone.audit()
    require(cone_digest == sigma_cone.EXPECTED_LEDGER_SHA256,
            "the sigma-even target/Eq cone ledger changed")
    cone = cone_ledger["minimal_target_Eq_cone"]
    require(cone["target_closed"] and cone["root_reduced_Eq_closed"],
            "the derived target/Eq cone stopped closing")

    # Quotient rows are (lambda_E14, Eq_D, target_D, ores_word).  Normalize
    # one nonzero component of 2D tensor (B1+B4)/2 to one.  The target cone
    # and clean derived K_Eq correction close Eq and leave target, but have
    # zero E14 occurrence coefficient.
    cartan_cone = (Q(0), Q(-1), Q(-1), Q(0))
    clean_k_eq = (Q(0), Q(1), Q(0), Q(0))
    formal_total = tuple(left + right for left, right in
                         zip(cartan_cone, clean_k_eq, strict=True))
    desired = (Q(-1), Q(0), Q(-1), Q(0))
    occurrence_dual = (Q(1), Q(0), Q(0), Q(0))
    require(formal_total == (Q(0), Q(0), Q(-1), Q(0))
            and rank((cartan_cone, clean_k_eq)) == 2
            and rank((cartan_cone, clean_k_eq, desired)) == 3
            and all(dot(occurrence_dual, column) == 0
                    for column in (cartan_cone, clean_k_eq))
            and dot(occurrence_dual, desired) == -1,
            "the formal target/Eq occurrence obstruction changed")
    return {
        "quotient_rows": ["lambda_E14", "Eq_D", "target_D", "ores_word"],
        "target_bearing_Cplus": [0, -1, -1, 0],
        "clean_K_Eq_face": [0, 1, 0, 0],
        "formal_sum": [0, 0, -1, 0],
        "required_E14_augmented_boundary": [-1, 0, -1, 0],
        "known_rank": 2,
        "rank_with_required_boundary": 3,
        "primitive_dual": [1, 0, 0, 0],
        "full_first_hit_rank_before_after": [269 + 2, 269 + 3],
        "required_companion_coefficient_after_formal_sum": 0,
        "first_remaining_row": "occurrence/private R_E14",
    }


def conditional_physical_assembly(data, dressing):
    dressing_ledger = dressing.audit()
    nearest = dressing_ledger["nearest_checked_physical_lift"]
    require(nearest == {
        "formula": "O_{-E}, E=2 D_root tensor v",
        "lower_private": "+E",
        "Eq": "+E",
        "W": "0 coefficientwise",
        "target": "0 coefficientwise",
        "word_resolved_labelled_ores": "-E (nonzero)",
        "coarse_six_label_ores": "0",
        "global_anchor_incidence": "0",
    }, "the nearest physical K_Eq dressing changed")
    require(dressing_ledger["nonzero_word_label_coefficients"] == 8,
            "the root-even unit-coefficient support changed")

    # Conditional on the one missing source-labelled placement E -> R_E14,
    # the nearest physical lift has the following selected-component row.
    # Its occurrence value is lambda(R)=-1.  Adding the old unary column is
    # literally B=U+R, hence the required companion coefficient is -1.
    cartan_cone = (Q(0), Q(-1), Q(-1), Q(0))
    placed_k_eq = (Q(-1), Q(1), Q(0), Q(-1))
    desired = (Q(-1), Q(0), Q(-1), Q(0))
    assembled = tuple(left + right for left, right in
                      zip(cartan_cone, placed_k_eq, strict=True))
    residue_dual = (Q(1), Q(0), Q(0), Q(-1))
    residue_unit = (Q(0), Q(0), Q(0), Q(1))
    require(assembled == (Q(-1), Q(0), Q(-1), Q(-1))
            and rank((cartan_cone, placed_k_eq)) == 2
            and rank((cartan_cone, placed_k_eq, desired)) == 3
            and all(dot(residue_dual, column) == 0
                    for column in (cartan_cone, placed_k_eq))
            and dot(residue_dual, desired) == -1
            and rank((cartan_cone, placed_k_eq, residue_unit))
            == rank((cartan_cone, placed_k_eq, residue_unit, desired)) == 3,
            "the conditional residue obstruction changed")

    target = data["target"]
    unary = data["columns"][data["selected_name"]]
    require(sparse_add((1, unary), (1, RETURN)) == target
            and target[COMPANION] == -1,
            "placing the private return stopped producing the companion")
    return {
        "missing_occurrence_map": {
            "F=H0-u": "1-v04_00",
            "e_Eq": "(p1_0_1*s1_1_1)*u35_11*v24_11",
            "image": "R_E14",
            "source_labelled_map_constructed": False,
        },
        "coefficient_normalization": (
            "2*D_root*(B1+B4)/2 has eight nonzero coefficients +/-1, "
            "so there is no scalar mismatch with the unit R_E14 return"
        ),
        "placed_K_Eq_quotient_column": [-1, 1, 0, -1],
        "Cplus_plus_placed_K_Eq": [-1, 0, -1, -1],
        "old_unary_plus_R_equals_full_E14_target": True,
        "required_companion_coefficient_after_occurrence_placement": -1,
        "first_row_after_occurrence_placement": (
            "word-resolved labelled ordinary residue -E"
        ),
        "primitive_residue_dual": [1, 0, 0, -1],
        "placed_rank_before_after_required_boundary": [2, 3],
        "full_first_hit_rank_before_after": [269 + 2, 269 + 3],
        "pure_labelled_residue_section_closes_this_quotient": True,
        "anchor_on_nearest_lift": 0,
        "W_on_nearest_lift": 0,
        "target_on_nearest_lift": 0,
    }


def downstream_scope(cplus):
    ledger, digest = cplus.audit()
    require(digest == cplus.EXPECTED_LEDGER_SHA256,
            "the C-plus q/ridge/W ledger changed")
    require(not ledger["physical_q"][
                "independent_q_construction_after_hypotheses"]
            and ledger["eta_sigma_ridge"]["order6_mixed_commutator"] == 0,
            "the downstream q/ridge scope changed")
    return {
        "physical_q": (
            "not an earlier independent row after a fully augmented P2/KEq "
            "comparison; handled by the committed q-defect alternative"
        ),
        "anchor": (
            "zero on the nearest word-resolved K_Eq lift; pointed conormal "
            "typing remains a later comparison condition"
        ),
        "ridge": (
            "strictly commutes with the Hasse tower, but its labelled shifted "
            "physical placement remains downstream"
        ),
        "ordering": (
            "occurrence/private first; after that placement, labelled "
            "ordinary residue; only then anchor/ridge/terminal completion"
        ),
    }


def audit():
    pin_dependencies()
    endpoint_q = load(
        "computations/verify_h3_e14_first_hit_dual_endpoint_q_extension_gate.py",
        "e14_keq_endpoint_q",
    )
    sigma_cone = load(
        "computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py",
        "e14_keq_sigma_cone",
    )
    dressing = load(
        "computations/verify_h3_cplus_root_even_koszul_physical_dressing_gate.py",
        "e14_keq_dressing",
    )
    cplus = load(
        "computations/verify_h3_cplus_q_ridge_w_terminal_reduction.py",
        "e14_keq_cplus",
    )
    data, identity = e14_spair_identity(endpoint_q)
    ledger = {
        "theorem": "canonical E14 Cplus/K_Eq companion assembly gate",
        "pins": PINS,
        "canonical_E14_S_pair": identity,
        "derived_target_Eq_combination": derived_target_eq_combination(
            sigma_cone),
        "conditional_physical_assembly": conditional_physical_assembly(
            data, dressing),
        "downstream_scope": downstream_scope(cplus),
        "verdict": (
            "the target-bearing Cartan cone plus the clean derived K_Eq face "
            "does not have the E14 companion: its first missing row is the "
            "occurrence/private placement E->R_E14.  If that single map is "
            "granted, the old unary S-pair gives the companion with coefficient "
            "-1 exactly, and the first remaining row becomes word-resolved "
            "labelled ordinary residue"
        ),
        "scope": (
            "canonical h=3 word-000101 first-hit packet and one normalized "
            "nonzero component of the generic root-even cone.  No construction "
            "of the occurrence placement, residue section, beta-zero family, "
            "or full terminal comparison is claimed"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("derived Cplus+K_Eq companion coefficient: 0")
    print("first missing row: occurrence/private E -> R_E14")
    print("after conditional placement companion coefficient: -1 (EXACT)")
    print("next row after placement: word-resolved labelled residue")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
