#!/usr/bin/env python3
"""Independent rectangle-12 transport and closure-scope referee; no solve."""
from __future__ import annotations

import hashlib
import itertools
import json
import os
import re
from collections import Counter
from pathlib import Path

if not __debug__:
    raise RuntimeError("assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMP = ROOT / "computations"
PRODUCER = COMP / "unaudited-codex-n8-x5-rectangle12-transport-census-2026-08-25"
BASE = COMP / "unaudited-codex-n8-x5-unmapped16-carrier-incidence-design-2026-08-25"
RANK3 = COMP / "unaudited-codex-n8-x5-rectangle-rank3-adjugate-exact-q-referee-2026-08-25"
RANK12 = COMP / "unaudited-codex-n8-x5-unmapped16-rectangle-rank12-incidence-ideal-design-2026-08-25"
RANK12_REF = COMP / "unaudited-codex-n8-x5-unmapped16-rectangle-rank12-incidence-ideal-referee-2026-08-25"
RANK1_O0 = COMP / "unaudited-codex-n8-x5-rectangle-rank1-orbit0-exact-q-run-2026-08-25"
RANK1_REMAINING = COMP / "unaudited-codex-n8-x5-rectangle-rank1-remaining4-exact-q-held-plan-referee-2026-08-25"


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


PINS = {
    PRODUCER / "MANIFEST.sha256": "afb6b789c12670b81078ff9adda4343b1ba600f2dd9c8a29abd5c09629b5feec",
    PRODUCER / "results_transport_census.json": "06f5ce489fe736d080af817c093adc0c3a3dc6b8ba699504fb53722ede4bfa3e",
    PRODUCER / "transport_ledger.json": "14dcbdd7a2ab777d1012459ca95187965dcc6a833b947d422a6220870346d837",
    BASE / "MANIFEST.sha256": "5cb72ac4af5a3ad3decbf3ba59ec858e23dcf2810c289d586feb14aeea1e61fe",
    BASE / "results_unmapped16_design.json": "2fe9e2a561397b58941b0f4210b3e4fb4a5457f377d4e23b7fc1dd6d0d22c008",
    RANK3 / "FINAL_MANIFEST.sha256": "94f1fe61337bfc8bb2b11aa3d528d219cd7b440d2ad19be2739109e693ab53a9",
    RANK3 / "results_referee.json": "459e403a6afc70d643ddfb37918513ded6eb79580169e796ab19be60a919b35f",
    RANK12 / "MANIFEST.sha256": "743f3e526b21890509e32077ed5bf0c38b1240d25d475e71e2e78520445c85cf",
    RANK12 / "results_rank12_incidence_design.json": "96b13ad342acd0fb02c37015b86303c9d6d7d880abe0e2a4e21f5e9e1aea5a28",
    RANK12_REF / "FINAL_MANIFEST.sha256": "e3e7974ae201f5915e7eeec95f7b01e3db37f0ddfe69619d00a4c1a84a92838f",
    RANK12_REF / "results_referee.json": "74394ce3858867c5221743483f7b765f49c9980c9e010e9d64262b56d09c03b4",
    RANK1_O0 / "FINAL_MANIFEST.sha256": "b129fdc2775a1fadb5659409ed9f953351cb47d591cef4fc50f5a09276bfbc07",
    RANK1_O0 / "AUDIT_RESULT.json": "4da4bf9c09cf10480eb8b79aa4d24a29a5c6d75749ae9d652e1b9eb9b1377b07",
    RANK1_REMAINING / "MANIFEST.sha256": "8221f60dbf9da3fbf7e7bcc55916119798758d736088ce2e757d844832b1eb7b",
    RANK1_REMAINING / "results_referee.json": "a7f15853b4ed1e5a01418b306829740d61dba5a25120097c2d41cef2f70b3898",
}

SITES = tuple(range(8))
SITE_PERMS = tuple(itertools.permutations(SITES))
COLOURS = tuple(range(3))
S3 = tuple(itertools.permutations(COLOURS))
FIXED = frozenset({(0, 3), (1, 6), (2, 7), (4, 5)})
VARIABLE_FAMILY = frozenset({(0, 4), (1, 2), (3, 5), (6, 7)})
A12 = (1, 2)


def edge(label):
    return tuple(map(int, label))


def label(value):
    return f"{value[0]}{value[1]}"


def move_edge(value, permutation):
    a, b = permutation[value[0]], permutation[value[1]]
    return tuple(sorted((a, b)))


def move_edges(values, permutation):
    return frozenset(move_edge(value, permutation) for value in values)


def added(record):
    return frozenset(edge(value) for value in record["added"])


def actual_variables(record):
    return frozenset(edge(value) for value in record["nonzero_variable_blocks"])


def support(record):
    return FIXED | added(record) | actual_variables(record)


def is_support_map(source, target, permutation):
    return (move_edges(FIXED, permutation) == FIXED and
            move_edges(VARIABLE_FAMILY, permutation) == VARIABLE_FAMILY and
            move_edges(added(source), permutation) == added(target) and
            move_edges(actual_variables(source), permutation) == actual_variables(target))


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        for tail in perfect_matchings(vertices[1:index] + vertices[index + 1:]):
            yield tuple(sorted(((first, vertices[index]),) + tail))


MATCHINGS = tuple(sorted(perfect_matchings(SITES)))
assert len(MATCHINGS) == 105


def supported_matchings(record):
    current = support(record)
    return tuple(matching for matching in MATCHINGS if set(matching) <= current)


def amplitude(record, word):
    polynomial = Counter()
    for matching in supported_matchings(record):
        factors = []
        for value in matching:
            i, j = word[value[0]], word[value[1]]
            if value in FIXED:
                if i != j:
                    break
            else:
                factors.append((value, i, j))
        else:
            polynomial[tuple(sorted(factors))] += 1
    return polynomial


def move_word(word, site_permutation, colour_permutation):
    answer = [None] * 8
    for source in SITES:
        answer[site_permutation[source]] = colour_permutation[word[source]]
    return tuple(answer)


def move_factor(factor, site_permutation, colour_permutation):
    value, i, j = factor
    a, b = site_permutation[value[0]], site_permutation[value[1]]
    if a < b:
        return ((a, b), colour_permutation[i], colour_permutation[j])
    return ((b, a), colour_permutation[j], colour_permutation[i])


def move_polynomial(polynomial, site_permutation, colour_permutation):
    answer = Counter()
    for monomial, coefficient in polynomial.items():
        mapped = tuple(sorted(move_factor(factor, site_permutation, colour_permutation) for factor in monomial))
        answer[mapped] += coefficient
    return answer


TERM = re.compile(r"^A(\d\d)(\^T)?\*K(\^T)?\*A(\d\d)(\^T)?$")


def parse_term(formula):
    match = TERM.match(formula)
    assert match, formula
    return (edge(match.group(1)), bool(match.group(2)), bool(match.group(3)), edge(match.group(4)), bool(match.group(5)))


def move_matrix(value, transpose, permutation):
    a, b = permutation[value[0]], permutation[value[1]]
    return tuple(sorted((a, b))), transpose ^ (a > b)


def move_term(term, permutation, k_transpose=False):
    left, left_t, k_t, right, right_t = term
    left, left_t = move_matrix(left, left_t, permutation)
    right, right_t = move_matrix(right, right_t, permutation)
    return (left, left_t, k_t ^ k_transpose, right, right_t)


def transpose_term(term):
    left, left_t, k_t, right, right_t = term
    return (right, not right_t, not k_t, left, not left_t)


def equation_terms(equation):
    return Counter(parse_term(term["formula"]) for term in equation["terms"])


def mapped_equation_matches(source, target, permutation, k_transpose=False):
    mapped = Counter(move_term(term, permutation, k_transpose) for term in equation_terms(source))
    direct = equation_terms(target)
    transposed = Counter(transpose_term(term) for term in direct)
    return mapped == direct or mapped == transposed


def select_carrier(record, cap="27", center=1):
    candidates = [item for item in record["two_sandwich_carriers"]
                  if item["kind"] == "star" and item["cap"] == cap and
                  item["defining_sites"] == [center] and item["identity_cap"]]
    assert len(candidates) == 1
    return candidates[0]


def strings_contain_A12(value):
    if isinstance(value, str):
        return value == "12" or "A12" in value
    if isinstance(value, list):
        return any(strings_contain_A12(item) for item in value)
    if isinstance(value, dict):
        return any(strings_contain_A12(item) for item in value.values())
    return False


def verify_guard_and_carrier(source, target, permutation):
    target_guard = {item["response_pair"]: item for item in target["guard_equations"]}
    k_choices = []
    for k_transpose in (False, True):
        if all(mapped_equation_matches(
            source_equation,
            target_guard[label(move_edge(edge(source_equation["response_pair"]), permutation))],
            permutation,
            k_transpose,
        ) for source_equation in source["guard_equations"]):
            k_choices.append(k_transpose)
    assert len(k_choices) == 1
    k_transpose = k_choices[0]
    for source_equation in source["guard_equations"]:
        mapped_response = label(move_edge(edge(source_equation["response_pair"]), permutation))
        assert mapped_response in target_guard
        assert mapped_equation_matches(source_equation, target_guard[mapped_response], permutation, k_transpose)
    source_carrier = select_carrier(source)
    mapped_cap = label(move_edge(edge(source_carrier["cap"]), permutation))
    mapped_center = permutation[source_carrier["defining_sites"][0]]
    target_carrier = select_carrier(target, mapped_cap, mapped_center)
    mapped_responses = sorted(label(move_edge(edge(item["response_pair"]), permutation)) for item in source_carrier["terms"])
    assert mapped_responses == sorted(item["response_pair"] for item in target_carrier["terms"])
    assert label(move_edge(edge(source_carrier["common_block"]), permutation)) == target_carrier["common_block"]
    # Each carrier term is transported literally, allowing transpose of the
    # response equation when the sorted response edge reverses.
    target_terms = {item["response_pair"]: item for item in target_carrier["terms"]}
    carrier_k_transposes = []
    for item in source_carrier["terms"]:
        mapped_response = label(move_edge(edge(item["response_pair"]), permutation))
        target_term = parse_term(target_terms[mapped_response]["formula"])
        choices = [flip for flip in (False, True)
                   if move_term(parse_term(item["formula"]), permutation, flip)
                   in (target_term, transpose_term(target_term))]
        assert len(choices) == 1
        carrier_k_transposes.append(choices[0])
    return target_carrier, k_transpose, carrier_k_transposes


def atomic_json(path, value):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


def main():
    for path, expected in PINS.items():
        actual = sha(path)
        assert actual == expected, (path, expected, actual)
    producer = json.loads((PRODUCER / "results_transport_census.json").read_text())
    producer_ledger = json.loads((PRODUCER / "transport_ledger.json").read_text())
    base = json.loads((BASE / "results_unmapped16_design.json").read_text())
    rank3 = json.loads((RANK3 / "results_referee.json").read_text())
    rank12 = json.loads((RANK12 / "results_rank12_incidence_design.json").read_text())
    rank12_ref = json.loads((RANK12_REF / "results_referee.json").read_text())
    rank1_o0 = json.loads((RANK1_O0 / "AUDIT_RESULT.json").read_text())
    rank1_remaining = json.loads((RANK1_REMAINING / "results_referee.json").read_text())
    assert producer["status"] == "PASS_ALL_12_TRANSPORTED_TWO_SOURCE_CLASSES"
    assert rank3["status"] == "PASS_EXACT_Q_UNIT_IDEAL_RANK3_TWO_LIFTS_ONLY"
    assert rank12["status"] == "PASS_EXACT_MATERIALIZATION_NO_SOLVE"
    assert rank12["scope"] == {"inputs_materialized": 10, "records_closed": 0, "solver_launches": 0}
    assert rank12_ref["status"] == "PASS_EXACT_FINITE_DESIGN_NO_SOLVE_NO_CLOSURE"
    assert rank1_o0["status"] == "PASS_UNIT_IDEAL_EXACT_Q_RANK1_ORBIT0_ONLY"
    assert rank1_o0["chart"]["rank"] == 1 and rank1_o0["chart"]["orbit"] == 0
    assert rank1_remaining["status"] == "PASS_APPROVED_HELD_ZERO_RUNS"
    assert rank1_remaining["held_state"]["solver_runs"] == 0
    records = base["records"]
    assert len(records) == 16
    rectangles = records[:12]
    excluded = records[12:]
    assert [item["record_index"] for item in rectangles] == list(range(12))
    assert all(item["classification"] == "NO_GUARD_ANCHOR_06_OR_07" for item in rectangles)
    assert [item["record_index"] for item in excluded] == [12, 13, 14, 15]
    assert all(item["classification"] == "NO_OUTSIDE_R6_R7_RECTANGLE" for item in excluded)
    present = [item["record_index"] for item in rectangles if "12" in item["nonzero_variable_blocks"]]
    absent = [item["record_index"] for item in rectangles if "12" not in item["nonzero_variable_blocks"]]
    assert present == [0, 1, 4, 5, 8, 9]
    assert absent == [2, 3, 6, 7, 10, 11]

    # Exhaust all 8! maps for all 144 ordered record pairs.
    matrix = {}
    unique_maps = {}
    site_trials = 0
    for source in rectangles:
        row = {}
        for target in rectangles:
            maps = []
            for permutation in SITE_PERMS:
                site_trials += 1
                if is_support_map(source, target, permutation):
                    maps.append(permutation)
            row[str(target["record_index"])] = len(maps)
            if maps:
                unique_maps[(source["record_index"], target["record_index"])] = maps[0]
        matrix[str(source["record_index"])] = row
    assert site_trials == 12 * 12 * 40320 == 5_806_080
    for group in (present, absent):
        assert all(matrix[str(a)][str(b)] == 1 for a in group for b in group)
    assert all(matrix[str(a)][str(b)] == 0 for a in present for b in absent)
    assert all(matrix[str(a)][str(b)] == 0 for a in absent for b in present)
    assert matrix == producer["source_support_isomorphism_counts"] == producer_ledger["source_support_isomorphism_counts"]

    # A12 is absent from every equation of the selected reduced ideal.
    a12_audit = []
    for record in rectangles:
        matchings = supported_matchings(record)
        assert all(A12 not in matching for matching in matchings)
        assert not strings_contain_A12(record["guard_equations"])
        reference_id = 0 if record["record_index"] in present else 2
        reference_map = unique_maps[(reference_id, record["record_index"])]
        selected = select_carrier(
            record,
            label(move_edge(edge("27"), reference_map)),
            reference_map[1],
        )
        assert not strings_contain_A12(selected)
        unused_with_a12 = sum(strings_contain_A12(item) for item in record["two_sandwich_carriers"] if item is not selected)
        assert unused_with_a12 == 8
        a12_audit.append({"record_index": record["record_index"],
                          "supported_matchings": len(matchings),
                          "matching_A12_occurrences": 0,
                          "guard_A12_occurrences": 0,
                          "selected_carrier_A12_occurrences": 0,
                          "unused_catalogue_carriers_mentioning_A12": unused_with_a12})

    # Literal transport from the reference of each A12 class.
    records_by_id = {item["record_index"]: item for item in rectangles}
    literal_checks = 0
    transport_records = []
    ledger_by_id = {item["record_index"]: item for item in producer_ledger["records"]}
    expected_outside = {0: ("47", "46"), 1: ("46", "47"), 2: ("47", "46"), 3: ("46", "47"),
                        4: ("37", "36"), 5: ("36", "37"), 6: ("37", "36"), 7: ("36", "37"),
                        8: ("56", "57"), 9: ("57", "56"), 10: ("56", "57"), 11: ("57", "56")}
    for target in rectangles:
        target_id = target["record_index"]
        reference_id = 0 if target_id in present else 2
        source = records_by_id[reference_id]
        permutation = unique_maps[(reference_id, target_id)]
        for colour_permutation in S3:
            for word in itertools.product(COLOURS, repeat=8):
                mapped_word = move_word(word, permutation, colour_permutation)
                mapped_polynomial = move_polynomial(amplitude(source, word), permutation, colour_permutation)
                assert mapped_polynomial == amplitude(target, mapped_word)
                literal_checks += 1
        selected_target, k_transpose, carrier_k_transposes = verify_guard_and_carrier(source, target, permutation)
        outside = label(move_edge(edge("47"), permutation))
        companion = label(move_edge(edge("46"), permutation))
        assert (outside, companion) == expected_outside[target_id]
        ledger = ledger_by_id[target_id]
        assert ledger["reference_record"] == reference_id
        assert ledger["site_permutation"] == list(permutation)
        assert ledger["mapped_outside_factor"] == outside and ledger["mapped_companion"] == companion
        assert ledger["word_generators_checked"] == 39366
        assert ledger["rank3"]["status"] == "CLOSED_BY_EXACT_Q_TRANSPORT"
        assert ledger["rank1"]["status"] == "EXACT_DESIGN_TRANSPORTED_NOT_SOLVED"
        assert ledger["rank2"]["status"] == "EXACT_DESIGN_TRANSPORTED_NOT_SOLVED"
        transport_records.append({"record_index": target_id, "reference_record": reference_id,
                                  "site_permutation": list(permutation), "outside_factor": outside,
                                  "companion_factor": companion,
                                  "selected_carrier_cap": selected_target["cap"],
                                  "guard_K_transposed_by_site_map": k_transpose,
                                  "carrier_term_K_transpose_conventions": carrier_k_transposes,
                                  "literal_word_transports": 39366})
    assert literal_checks == 12 * 6 * 6561 == 472392
    assert literal_checks == producer["word_generator_transport_checks"]
    assert rank12["counts"]["rank1"] == {"variables": 76, "generators": 6571, "canonical_inputs": 5}
    assert rank12["counts"]["rank2"] == {"variables": 80, "generators": 6574, "canonical_inputs": 5}

    result = {
        "schema": "KRENN_X5_RECTANGLE12_TRANSPORT_CENSUS_REFEREE_V1",
        "status": "PASS_EXACT_TRANSPORT_WITH_SELECTED_CARRIER_SCOPE_AND_CURRENT_CLOSURE_LEDGER",
        "producer": {"manifest_sha256": PINS[PRODUCER / "MANIFEST.sha256"],
                     "result_sha256": PINS[PRODUCER / "results_transport_census.json"],
                     "ledger_sha256": PINS[PRODUCER / "transport_ledger.json"]},
        "support_census": {"records": 12, "classes": [present, absent], "records_per_class": 6,
                           "site_permutations_per_ordered_pair": 40320,
                           "ordered_pairs": 144, "site_maps_tested": site_trials,
                           "unique_within_class": True, "cross_class_maps": 0,
                           "isomorphism_counts": matrix},
        "literal_transport": {"word_transports": literal_checks,
                              "guard_equations_literal": True,
                              "selected_identity_carrier_literal": True,
                              "outside_factor_maps": transport_records},
        "A12_reduced_ideal_audit": {
            "records": a12_audit,
            "supported_matching_equations_A12_free": True,
            "guard_equations_A12_free": True,
            "selected_carrier_equations_A12_free": True,
            "reduced_rank_ideal_A12_free": True,
            "entire_alternative_carrier_catalogue_A12_free": False,
            "scope_note": "Eight unused alternative-carrier records per source mention A12; they are not equations in the selected reduced rank ideal and are not used in the lift/transport theorem.",
            "lift": {"A12_present": "A12=I3", "A12_absent": "A12=0"}},
        "closure_ledger": {
            "rank3": {"canonical_orbit": "exact-Q closed", "transported_closed_records": 12},
            "rank1": {"design_transported_records": 12, "canonical_orbits_per_record": 5,
                      "closed_orbits": [0], "orbit0_transported_closed_records": 12,
                      "pending_orbits": [1, 2, 3, 4],
                      "pending_schedule_status": "APPROVED_HELD_ZERO_RUNS"},
            "rank2": {"design_transported_records": 12, "canonical_orbits_per_record": 5,
                      "closed_orbits": [], "pending_orbits": [0, 1, 2, 3, 4]},
            "nonrectangle_records_excluded": [12, 13, 14, 15],
            "full_conjecture_closed": False,
        },
        "exact_implication": "The exact-Q rank-3 certificate transports to all 12 rectangle records. Rank-1 and rank-2 chart ideals transport as exact designs. Current closure promotion is valid for rank-1 orbit0 across all 12 because that exact-Q orbit is independently closed for both A12 lifts; rank-1 orbits1-4 and every rank-2 orbit remain unclosed until their own solves succeed.",
        "scope": {"solver_runs_by_this_referee": 0, "new_closure_computations": 0,
                  "rectangle_records": list(range(12)), "excluded_nonrectangle_records": [12, 13, 14, 15],
                  "full_conjecture": False},
        "pins": {str(path.relative_to(ROOT)): expected for path, expected in PINS.items()},
    }
    atomic_json(HERE / "results_referee.json", result)
    print(json.dumps({"status": result["status"], "classes": 2, "site_maps_tested": site_trials,
                      "word_transports": literal_checks, "rank3_closed": 12,
                      "rank1_orbit0_closed": 12, "rank1_pending_orbits": [1,2,3,4],
                      "rank2_pending_orbits": [0,1,2,3,4], "solver_runs": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
