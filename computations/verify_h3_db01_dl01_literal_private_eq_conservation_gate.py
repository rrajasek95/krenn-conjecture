#!/usr/bin/env python3
"""Audit the literal private/Eq image of db01 and the next dL01 face.

There are two different questions which must not be conflated.  Coordinate
projection from the typed direct sum to the final AugP2 B/Eq block is
defined, and is zero on every off-grade response column.  A comparison
which *places* such a response column in B/Eq is not defined until a
source-labelled word/fine/repeated mapping cylinder is constructed.

The selected six-term db01 face and all eighteen endpoint/direction terms
are in response word 11:110000, while B/Eq is in cap word 01211222.  Hence
their literal B/Eq projections and delta.(B-Eq) values are exactly zero.
The first possibly bright datum is the missing mixed incidence of the
response-to-AugP2 mapping cylinder, not either bare response packet.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_selected_db01_normalized_gl3_bar_companion_gate.py":
        "620b3e54e8e6ee09a0b616d0259c8d109b0359645b20d35db5fb876c8e7e0311",
    "notes/h3-selected-db01-normalized-gl3-bar-companion-gate.md":
        "46aa4e74c52160cfaa74089727defb1a0d6c4d0051130374ec12dcc887de09de",
    "computations/verify_h3_maximal_pointed_balanced_same_grade_terminal_gate.py":
        "262e1dd08dd1842d60515d45aea53ea406d7e1e5ea55ab506bb6e81d64b07741",
    "notes/h3-maximal-pointed-balanced-same-grade-terminal-gate.md":
        "130f92e2a9bd2c7c5196bc730313a38d0b64a2ff0cf51804f316b74e26cee757",
    "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py":
        "bd3f008eb2faf00bbebccb09ef9692908f2e0ae4a795706de2c32f0b2ef342af",
    "notes/h3-shear-collision-augp2-packaging-map-gate.md":
        "9d5918605dd94d08d18c099966e5956fa0f1c62855b97fd81bf9ada54f2f45ad",
    "computations/verify_h3_balanced_square_private_eq_projection_gate.py":
        "bbfb690a73844169574351ad019171a6d9c5fe332e59cc9694a1f67dcf31cf8e",
    "notes/h3-balanced-square-private-eq-projection-gate.md":
        "6d740e7e30231204dbe1b79c4b7c21fe5f5b5ac45122ac714be3c7626afa7c31",
    "computations/verify_h3_h2_l01_endpoint_flag_s4_cplus_span_gate.py":
        "3ab94cb5293deeef5777588c15e308e4ac8974ffcff4272ee021432b6633089d",
    "notes/h3-h2-l01-endpoint-flag-s4-cplus-span-gate.md":
        "dcbb22545c23d209f2ee3cf654f00d4d76cae8b200dc886214abda9a7016c29f",
}
EXPECTED_DIGEST = "2c22082b85f64836b55cce7251c744cadb06660bc8f3319969baeadcd28589c6"

DELTA = tuple(map(Q, (1, 1, -1, -1)))
ZERO8 = (Q(0),) * 8


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


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


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def input_ledgers():
    db01 = load(
        "computations/verify_h3_selected_db01_normalized_gl3_bar_companion_gate.py",
        "db01_dl01_literal_db01",
    )
    db_ledger, db_digest = db01.audit()
    require(db_digest == db01.EXPECTED_LEDGER_SHA256,
            "the selected db01 ledger changed")

    maximal = load(
        "computations/verify_h3_maximal_pointed_balanced_same_grade_terminal_gate.py",
        "db01_dl01_literal_maximal",
    )
    maximal_ledger, maximal_digest = maximal.audit()
    require(maximal_digest == maximal.EXPECTED_LEDGER_SHA256,
            "the maximal typed ledger changed")

    packaging = load(
        "computations/verify_h3_shear_collision_augp2_packaging_map_gate.py",
        "db01_dl01_literal_packaging",
    )
    packaging_ledger, packaging_digest = packaging.audit()
    require(packaging_digest == packaging.EXPECTED_LEDGER_SHA256,
            "the response/AugP2 packaging ledger changed")

    private_eq = load(
        "computations/verify_h3_balanced_square_private_eq_projection_gate.py",
        "db01_dl01_literal_private_eq",
    )
    private_eq_ledger, private_eq_digest = private_eq.audit()
    require(private_eq_digest == private_eq.EXPECTED_LEDGER_SHA256,
            "the private/Eq ledger changed")

    endpoint = load(
        "computations/verify_h3_h2_l01_endpoint_flag_s4_cplus_span_gate.py",
        "db01_dl01_literal_endpoint",
    )
    endpoint_ledger, endpoint_digest = endpoint.audit()
    require(endpoint_digest == endpoint.EXPECTED_LEDGER_SHA256,
            "the endpoint dL01 ledger changed")
    return db_ledger, maximal_ledger, packaging_ledger, private_eq_ledger, endpoint_ledger


def typing_audit(db, maximal, packaging, _private_eq, endpoint):
    support = db["literal_support"]
    terms = tuple(tuple(term) for term in support["selected_db01_terms"])
    word = packaging["literal_word_and_fine_map"]
    typed = maximal["typed_projection_and_first_unmodeled_family"]
    representation = endpoint["representation"]
    require(len(terms) == len(set(terms)) == 6
            and all(sum(factor.startswith("dq") for factor in term) == 1
                    for term in terms)
            and support["selected_response_head_word"] == "11:110000"
            and support["repeated_edge_exponents"]["db01"] == "squarefree",
            "the literal six-term db01 packet changed")
    require(word["response_word_display"] == "11:110000"
            and word["canonical_cap_word"] == "01211222"
            and word["word_hamming_distance"] == 6
            and word["all_six_fine_degrees_change"]
            and not word["cap_word_in_existing_D4_cube"]
            and not word["literal_grade_preserving_map"],
            "the response/cap grade separation changed")
    require(typed["off_grade_named_columns_with_zero_B_Eq_projection"] == 121
            and maximal["fixed_window_switch_Weyl_response_RL_18face"]
                ["direction_terms"] == 18
            and maximal["fixed_window_switch_Weyl_response_RL_18face"]
                ["normalized_detector_on_18_direction_terms"] == "2"
            and representation["eighteen_term_representation"]
                == "[2,2] tensor trivial_tail",
            "the typed eighteen-term packet changed")
    return {
        "selected_db01_source_label": support["compatible_deletion_face"],
        "selected_db01_terms": [list(term) for term in terms],
        "selected_db01_term_count": len(terms),
        "db01_vertical_PP_degree": 1,
        "response_word": word["response_word_display"],
        "cap_B_Eq_word": word["canonical_cap_word"],
        "word_hamming_distance": word["word_hamming_distance"],
        "all_six_selected_cap_fine_degrees_change": True,
        "db01_repeated_grade": "squarefree",
        "literal_coordinate_projection_status": (
            "defined by zero-extension on the typed direct sum"
        ),
        "cross_grade_comparison_status": (
            "undefined: no source-labelled response-to-AugP2 word/fine/"
            "repeated mapping cylinder has been constructed"
        ),
        "dL01_terms": 18,
        "dL01_representation": representation["eighteen_term_representation"],
        "dL01_response_direction_profile": maximal[
            "fixed_window_switch_Weyl_response_RL_18face"
        ]["direction_primitive_profile"],
    }


def projection_audit(_db, maximal, _packaging, private_eq, _endpoint):
    projection = private_eq["projection"]
    require(projection["old_projection_rank"] == 7
            and projection["criterion"] == "delta dot (B-Eq) is nonzero",
            "the primitive B/Eq projection changed")

    diagonal = []
    for corner in range(4):
        basis = tuple(Q(1) if index == corner else Q(0)
                      for index in range(4))
        diagonal.append(basis + basis)
    companions = []
    for positive in (0, 1):
        for negative in (2, 3):
            edge = tuple(Q(1) if index in (positive, negative) else Q(0)
                         for index in range(4))
            companions.append(edge + (Q(0),) * 4)
    old = tuple(diagonal + companions)
    psi = DELTA + tuple(-value for value in DELTA)
    db01_images = (ZERO8,) * 6
    dl01_images = (ZERO8,) * 18
    require(rank(old) == 7
            and all(dot(psi, column) == 0 for column in old)
            and rank(old + db01_images) == 7
            and rank(old + db01_images + dl01_images) == 7
            and all(dot(psi, column) == 0
                    for column in db01_images + dl01_images),
            "an off-grade response face changed the cap projection")

    response = maximal["fixed_window_switch_Weyl_response_RL_18face"]
    require(response["normalized_detector_on_18_direction_terms"] == "2",
            "the response-side direction detector changed")
    return {
        "B_Eq_row_order": projection["row_order"],
        "primitive_chi": "delta.(B-Eq)",
        "delta": list(map(int, DELTA)),
        "old_cap_projection_rank": rank(old),
        "six_db01_literal_images": [[0] * 8 for _ in range(6)],
        "chi_on_each_db01_term": [0] * 6,
        "rank_after_db01": rank(old + db01_images),
        "eighteen_dL01_literal_images": "18 copies of zero_8",
        "chi_on_dL01_packet": 0,
        "normalized_Psi_on_dL01_packet": 0,
        "rank_after_db01_and_dL01": rank(old + db01_images + dl01_images),
        "response_side_normalized_detector_on_dL01": 2,
        "codomain_warning": (
            "the response detector value 2 and cap Psi value 0 are values "
            "of different typed covectors; they are not contradictory"
        ),
        "conservation": (
            "adjoining the literal db01 and dL01 response packets leaves "
            "delta.(B-Eq) and the cap rank-seven quotient unchanged"
        ),
    }


def landing_audit(_db, maximal, packaging, _private_eq, endpoint):
    package = packaging["augmented_packaging"]
    typed = maximal["typed_projection_and_first_unmodeled_family"]
    candidate = endpoint["candidate_span"]
    require(package["rank_before_mixed_cell"] == 2
            and package["rank_after_mixed_cell"] == 3
            and package["rank_after_labelled_ridge"] == 4
            and candidate["equals_L01_direction_primitive"]
            and candidate["conditional_C_plus_lower_landing"]
                == ["1/2", "1/2", "-1/4", "-1/4", "-1/4", "-1/4"],
            "the minimal landing quotient changed")

    b_only = DELTA + (Q(0),) * 4
    eq_only = (Q(0),) * 4 + DELTA
    tied = DELTA + DELTA
    psi_over_four = tuple(value / Q(4)
                          for value in DELTA + tuple(-x for x in DELTA))
    require(dot(psi_over_four, b_only) == 1
            and dot(psi_over_four, eq_only) == -1
            and dot(psi_over_four, tied) == 0,
            "the primitive mapping-cylinder controls changed")
    return {
        "minimal_missing_comparison_datum": (
            "one occurrence-local, source-labelled response-to-AugP2 PP "
            "mapping cylinder with a 11:110000 -> 01211222 word/fine "
            "diagonal and an explicit B/Eq image for its mixed incidence"
        ),
        "must_retain": typed["physical_family_must_also_carry"],
        "packaging_quotient_rows": package["packaging_quotient_rows"],
        "packaging_ranks_without_then_with_mixed_then_ridge": [
            package["rank_before_mixed_cell"],
            package["rank_after_mixed_cell"],
            package["rank_after_labelled_ridge"],
        ],
        "conditional_C_plus_response_coefficient": (
            "v_A/4=(1/2,1/2,-1/4,-1/4,-1/4,-1/4); this is still "
            "off-grade until its physical restriction/reinsertion is built"
        ),
        "first_deciding_scalar": "chi(mixed)=delta.(B(mixed)-Eq(mixed))",
        "normalized_controls": {
            "B_only_delta": 1,
            "Eq_only_delta": -1,
            "tied_delta": 0,
        },
        "terminal_alternative": (
            "if every completed cross-grade mixed incidence has chi=0, "
            "Psi=delta.(B-Eq)/4 remains the normalized terminal; any "
            "nonzero chi is the first literal breaker"
        ),
    }


def run(mode: str) -> str:
    pin_dependencies()
    inputs = input_ledgers()
    ledger = {}
    if mode in ("all", "typing"):
        ledger["strict_typing"] = typing_audit(*inputs)
    if mode in ("all", "projection"):
        ledger["literal_B_Eq_projection"] = projection_audit(*inputs)
    if mode in ("all", "landing"):
        ledger["minimal_comparison_and_terminal"] = landing_audit(*inputs)
    if mode == "all":
        ledger["theorem"] = (
            "literal db01/dL01 private-Eq conservation and first mixed "
            "mapping-cylinder breaker gate"
        )
        ledger["verdict"] = (
            "Strict typed projection proves conservation: selected db01 and "
            "all eighteen dL01 terms have zero B/Eq image and zero mismatch. "
            "Only a new source-labelled response-to-AugP2 mixed incidence "
            "can break delta.(B-Eq); its deciding scalar is not fixed by any "
            "currently constructed column."
        )
        ledger["scope"] = (
            "exact rational B/Eq projection of the selected six-term db01 "
            "and eighteen-term fixed-chart dL01 packets, with literal word/"
            "fine/repeated/source tags.  This does not construct or determine "
            "the missing cross-grade mapping-cylinder incidence."
        )
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if mode == "all" and EXPECTED_DIGEST != "TO_BE_FROZEN":
        require(digest == EXPECTED_DIGEST,
                ("db01/dL01 conservation ledger changed", digest))
    print(f"h3 db01/dL01 literal private-Eq gate ({mode}): PASS")
    if mode in ("all", "typing"):
        print("db01: six off-grade source-labelled terms; comparison arrow absent")
    if mode in ("all", "projection"):
        print("literal db01/dL01 delta.(B-Eq): 0/0; cap rank stays 7")
        print("response dL01 detector=2 is a different typed covector")
    if mode in ("all", "landing"):
        print("first possible breaker: cross-word mixed mapping-cylinder incidence")
    print("ledger_sha256=" + digest)
    return digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("all", "typing", "projection", "landing"),
        default="all",
    )
    arguments = parser.parse_args()
    run(arguments.mode)


if __name__ == "__main__":
    main()
