#!/usr/bin/env python3
"""Exact first t-prolongation boundary of the frozen 49-row N8 dual."""

from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CHECKER = ROOT / "computations" / "verify_n8_chart26_normalized_degree7_closure.py"
PROVIDER = (ROOT / "computations" /
            "unaudited-codex-n8-normalized-dfs-degree7-2026-08-23")
PACKET = PROVIDER / "degree7_word_packet.txt"
SMALL_FAILURE = PROVIDER / "degree7_dfs_failure.txt"
ALL_FAILURE = PROVIDER / "degree7_all_mixed_root05a7_failure.txt"
OUT = HERE / "results_degree8_dual_prolongation.json"
DUAL_SHA = "b0f137c8827d8da94525a53636bd30791e7c56722b09a74e8cdfd0c792e75fb3"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_checker():
    spec = importlib.util.spec_from_file_location("degree7", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def invariant_seed(M):
    residual, _canonical_seed, _actual_seed = M.seed_residual()
    answer = {}
    for row, coefficient in residual.items():
        representative = M.canonical_normalized_row(row)
        require(representative not in answer or answer[representative] == coefficient,
                "seed residual stopped being invariant")
        answer[representative] = coefficient
    require(len(answer) == 564, "invariant seed census changed")
    return answer


def reconstruct_dual(M):
    """Replay the archived four-round exact construction, without degree 8."""
    target = invariant_seed(M)
    rows, columns, _layers = M.top_degree_closure(target)
    rank, remainder, _maximum, dual, pairing = M.exact_rank_and_target(
        rows, columns, target
    )
    forced = set()
    rounds = []
    while True:
        candidates, violating, _histogram = M.dual_violating_columns(
            dual, set(columns)
        )
        rounds.append((len(rows), len(columns), rank, len(dual),
                       len(candidates), len(violating)))
        if not violating:
            break
        forced.update(violating)
        rows, columns, _layers = M.top_degree_closure(
            target, forced_columns=forced
        )
        rank, remainder, _maximum, dual, pairing = M.exact_rank_and_target(
            rows, columns, target
        )
    require(rounds == [
        (20859, 298, 298, 3, 16, 13),
        (134041, 1849, 1849, 24, 38, 8),
        (216350, 2955, 2955, 37, 50, 6),
        (273857, 3721, 3721, 49, 56, 0),
    ], "archived degree-seven dual rounds changed")
    require(remainder == {b"": Fraction(-1)} and pairing == -1,
            "degree-seven target remainder changed")
    record = [
        [row.hex(), value.numerator, value.denominator]
        for row, value in sorted(dual.items())
    ]
    digest = hashlib.sha256(json.dumps(
        record, separators=(",", ":")
    ).encode()).hexdigest()
    require(digest == DUAL_SHA, "49-row dual digest changed")
    return target, dual, rounds


def column_entries(M, column, cache):
    if column in cache:
        return cache[column]
    answer = collections.defaultdict(int)
    for actual in M.normalized_column_orbit(column):
        for output, coefficient in M.normalized_column_outputs(actual):
            if output == M.canonical_normalized_row(output):
                answer[output] += coefficient
    cache[column] = dict(answer)
    return cache[column]


def pairing(weights, entries):
    return sum(weights.get(row, 0) * coefficient
               for row, coefficient in entries.items())


def word_label(M, code):
    return "".join(map(str, M.D5.decode_word(code)))


def word_profile(M, code):
    word = M.D5.decode_word(code)
    return tuple(sorted((word.count(colour) for colour in range(3)
                         if word.count(colour)), reverse=True))


def histogram(values):
    return {str(key): value for key, value in
            sorted(collections.Counter(values).items(), key=lambda item: str(item[0]))}


def parse_small_packet():
    codes = set()
    with PACKET.open(encoding="ascii") as stream:
        require(stream.readline().split() ==
                ["KRENN_N8_WORD_PACKET_V1", "78", "22"],
                "small word packet header changed")
        for line in stream:
            tag, code, _label = line.split()
            require(tag == "WORD", "small packet row changed")
            codes.add(int(code))
    require(len(codes) == 78, "small packet size changed")
    return codes


def root05a7_diagnosis(M, target, entry_cache):
    root = bytes.fromhex("05a7")
    require(root in target, "05a7 left the frozen tail")
    all_columns = M.bounded_incident_columns({root: Fraction(1)}, 7)
    require(len(all_columns) == 6, "all-word 05a7 option census changed")
    packet_codes = parse_small_packet()
    small_columns = {column for column in all_columns
                     if column[0] in packet_codes}
    require(len(small_columns) == 5, "small-packet 05a7 option census changed")
    missing = tuple(all_columns - small_columns)
    require(missing == ((3785, bytes.fromhex("07")),),
            f"first missing 05a7 orbit changed: {missing}")
    column = missing[0]
    entries = column_entries(M, column, entry_cache)
    tail_intersection = sorted(set(entries) & set(target))
    require(len(entries) == 55 and len(tail_intersection) == 4
            and entries[root] == 1,
            "missing 05a7 column geometry changed")

    provenance = []
    for actual_code, actual_multiplier in M.normalized_column_orbit(column):
        for raw_term in M.D5.iter_word_terms(actual_code):
            normalized = bytes(value for value in raw_term
                               if value not in M.D5.SUPPORT_IDS)
            if bytes(sorted(actual_multiplier + normalized)) != root:
                continue
            provenance.append({
                "actual_word": word_label(M, actual_code),
                "actual_multiplier": actual_multiplier.hex(),
                "raw_matching_term": raw_term.hex(),
                "normalized_term": normalized.hex(),
                "support_cells_deleted": [
                    f"{value:02x}" for value in raw_term
                    if value in M.D5.SUPPORT_IDS
                ],
                "matching_coordinates": [
                    list(M.D5.COORDINATES[value]) for value in raw_term
                ],
            })
    require(provenance == [{
        "actual_word": "21012012",
        "actual_multiplier": "05",
        "raw_matching_term": "3e6787a7",
        "normalized_term": "a7",
        "support_cells_deleted": ["3e", "67", "87"],
        "matching_coordinates": [
            [0, 7, 2, 2], [1, 6, 1, 1], [2, 5, 0, 0], [3, 4, 1, 2]
        ],
    }], "missing 05a7 matching provenance changed")
    return {
        "small_packet_options": len(small_columns),
        "all_mixed_options": len(all_columns),
        "unique_missing_column": {
            "canonical_word": word_label(M, column[0]),
            "word_code": column[0],
            "word_profile": list(word_profile(M, column[0])),
            "multiplier": column[1].hex(),
            "full_support": len(entries),
            "tail_root_intersection": [row.hex() for row in tail_intersection],
            "matching_provenance": provenance,
        },
        "small_packet_failure_sha256": sha256_file(SMALL_FAILURE),
        "all_mixed_failure_sha256": sha256_file(ALL_FAILURE),
        "all_mixed_guard": (
            "adding the unique profile-332 option does not create a leaf: "
            "the all-mixed root DFS reached the 10,000,001-call cap with no pivots"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()

    M = load_checker()
    target, dual, rounds = reconstruct_dual(M)
    entry_cache = {}

    degree7_columns = M.bounded_incident_columns(dual, 7)
    degree8_columns = M.bounded_incident_columns(dual, 8)
    new_columns = {column for column in degree8_columns
                   if len(column[1]) == 4}
    require(len(degree7_columns) == 56 and len(degree8_columns) == 246
            and len(new_columns) == 190,
            "degree-eight incident boundary census changed")

    crossing = []
    for column in sorted(new_columns):
        entries = column_entries(M, column, entry_cache)
        value = pairing(dual, entries)
        if value:
            crossing.append((column, value, entries))
    require(len(crossing) == 146, "t-shift crossing-column census changed")

    degree8_frequency = collections.Counter(
        row for column in new_columns
        for row in column_entries(M, column, entry_cache) if len(row) == 8
    )
    require(len(degree8_frequency) == 13254
            and collections.Counter(degree8_frequency.values())
            == {1: 12594, 2: 646, 3: 8, 4: 6},
            "degree-eight exchange-row frequency changed")

    extension = {}
    crossing_records = []
    private_count_histogram = collections.Counter()
    for column, value, entries in crossing:
        private_rows = sorted(
            row for row in entries
            if len(row) == 8 and degree8_frequency[row] == 1
        )
        require(private_rows, "a crossing column lost all private degree-eight rows")
        chosen = private_rows[0]
        coefficient = entries[chosen]
        require(chosen not in extension, "private exchange rows collided")
        extension[chosen] = -value / coefficient
        private_count_histogram[len(private_rows)] += 1
        old_hits = [row for row in entries if row in dual]
        crossing_records.append({
            "word": word_label(M, column[0]),
            "word_code": column[0],
            "word_profile": list(word_profile(M, column[0])),
            "multiplier": column[1].hex(),
            "t_shift_pairing": [value.numerator, value.denominator],
            "full_column_support": len(entries),
            "old_dual_rows_met": len(old_hits),
            "private_degree8_rows": len(private_rows),
            "chosen_private_row": chosen.hex(),
            "chosen_entry_coefficient": coefficient,
            "repair_weight": [extension[chosen].numerator,
                              extension[chosen].denominator],
        })

    # Private rows yield a literal diagonal 146 x 146 minor, hence exact
    # independence and an explicit first-shell prolongation, without a rank solve.
    extended = dict(dual)
    extended.update(extension)
    require(all(not pairing(extended, column_entries(M, column, entry_cache))
                for column in new_columns),
            "private-row exchange did not close the first boundary")

    # The repair is not a global degree-eight dual: its new rows expose the
    # next, still bounded incidence boundary.
    repair_incident = M.bounded_incident_columns(extension, 8)
    next_candidates = repair_incident | new_columns
    next_crossing = []
    for column in next_candidates:
        value = pairing(extended, column_entries(M, column, entry_cache))
        if value:
            next_crossing.append((column, value))
    require(len(repair_incident) == 407 and len(next_candidates) == 451
            and len(repair_incident - new_columns) == 261
            and len(next_crossing) == 252,
            "second exchange boundary census changed")

    root_diagnosis = root05a7_diagnosis(M, target, entry_cache)

    if args.mutate:
        require(len(crossing) == 145,
                "hostile degree-eight crossing mutation survived")

    result = {
        "verdict": "THE_49_ROW_T_SHIFT_FAILS_ON_146_INDEPENDENT_COLUMNS;A_146_PRIVATE_ROW_EXCHANGE_CLOSES_ONLY_THE_FIRST_BOUNDARY",
        "scope": (
            "exact first t-prolongation boundary of the archived degree-seven "
            "dual; no degree-eight ambient span solve and no saturation conclusion"
        ),
        "degree7_dual": {
            "support": len(dual),
            "sha256": DUAL_SHA,
            "degree_histogram": histogram(map(len, dual)),
            "coefficient_histogram": histogram(dual.values()),
            "archived_rounds": [list(item) for item in rounds],
        },
        "natural_t_shift": {
            "old_incident_columns": len(degree7_columns),
            "degree8_incident_columns": len(degree8_columns),
            "new_multiplier_degree4_columns": len(new_columns),
            "crossing_columns": len(crossing),
            "pairing_histogram": histogram(value for _column, value, _entries
                                           in crossing),
            "old_dual_support_intersection_histogram": histogram(
                sum(row in dual for row in entries)
                for _column, _value, entries in crossing
            ),
            "full_column_support_histogram": histogram(
                len(entries) for _column, _value, entries in crossing
            ),
            "word_profile_histogram": histogram(
                word_profile(M, column[0])
                for column, _value, _entries in crossing
            ),
            "direct_prolongation_valid": False,
        },
        "minimal_first_exchange_packet": {
            "independent_constraints": len(crossing),
            "exact_independence_certificate": (
                "each crossing has a selected degree-eight row occurring in "
                "no other one of the 190 new incident columns; these entries "
                "form a literal nonzero diagonal 146x146 minor"
            ),
            "available_degree8_rows": len(degree8_frequency),
            "row_incidence_frequency_histogram": histogram(
                degree8_frequency.values()
            ),
            "private_rows_per_crossing_histogram": dict(
                sorted(private_count_histogram.items())
            ),
            "repair_rows": len(extension),
            "repair_coefficient_histogram": histogram(extension.values()),
            "all_190_first_boundary_columns_annihilated_after_repair": True,
            "crossing_ledger": crossing_records,
        },
        "next_boundary_guard": {
            "columns_incident_to_repair_rows": len(repair_incident),
            "new_columns_beyond_first_boundary": len(repair_incident - new_columns),
            "total_candidates_after_first_repair": len(next_candidates),
            "new_crossings": len(next_crossing),
            "pairing_histogram": histogram(value for _column, value in
                                           next_crossing),
            "word_profile_histogram": histogram(
                word_profile(M, column[0]) for column, _value in next_crossing
            ),
            "global_degree8_prolongation_proved": False,
            "reason": (
                "the explicit private-row repair moves rather than closes the "
                "boundary: 252 further columns meet the extended functional"
            ),
        },
        "root05a7": root_diagnosis,
        "interpretation": (
            "the 05a7 cycle is a local manifestation of the global degree-seven "
            "class, not proof of t-torsion persistence. Multiplication by t "
            "immediately exposes 146 independent source columns, and private "
            "degree-eight outputs repair them one-for-one; the saturation "
            "question begins with the ensuing 252-column exchange boundary"
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = hashlib.sha256(logical.encode()).hexdigest()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        OUT.write_text(rendered, encoding="utf-8")
    if args.check_results:
        require(OUT.read_text(encoding="utf-8") == rendered,
                "frozen result differs")
    print(json.dumps({
        "degree8_new_crossing": [len(new_columns), len(crossing)],
        "private_repair_rows": len(extension),
        "next_boundary_crossings": len(next_crossing),
        "root05a7_options": [
            root_diagnosis["small_packet_options"],
            root_diagnosis["all_mixed_options"],
        ],
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
