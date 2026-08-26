#!/usr/bin/env python3
"""Exact response-star audit on W40 X4 and W25-F8 X3 controls.

Outputs contain every raw X4 coefficient row and every 90 x 9 response-star
matrix used in a rank claim.  All arithmetic is Fraction arithmetic over Q.
"""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

from response_star_core import (
    COLOURS,
    SITES,
    activity_rows,
    cell,
    dot,
    hafnian,
    off_count,
    response_row,
    response_star_matrix,
    response_star_record,
    response_triangle_matrix,
    response_triangle_record,
    source_from_json_blocks,
    stringify,
)


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
W40_PATH = (
    ROOT / "computations/unaudited-x4general-w40-2026-08-20/results_t3.json"
)
W25_PATH = (
    ROOT
    / "computations/unaudited-x3core-w25-2026-08-15"
    / "OBJECT_W25-F8_n8_allblocked_X3.json"
)
PINNED = {
    "W40": "30ad242d62b5cb905858842ce4e8255b105862dc21a65c73c080557fa8c1617f",
    "W25-F8": "46d6e207e392deaa7e0bfc4221c7f5cc6735f11a2a14cc388292ca6850dd33f6",
}
DECLARED_CONTROLS = {
    "input_hashes",
    "raw_w40_x4",
    "raw_w25_x3_outside_x4",
    "w40_x4_sign_mutation_must_fire",
    "all_168_matrices_each_source",
    "all_560_triangle_matrices_each_source",
    "endpoint_reversal_all_choices",
    "endpoint_colour_mutation_must_fire",
    "w40_675_identity_cap",
    "w25_no_response_star_choice",
    "zero_pair_inactivity",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def canonical_digest(value):
    payload = json.dumps(stringify(value), sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode()).hexdigest()


def load_sources():
    require(digest(W40_PATH) == PINNED["W40"], "pinned W40 result changed")
    require(digest(W25_PATH) == PINNED["W25-F8"], "pinned W25-F8 changed")
    w40_data = json.loads(W40_PATH.read_text())
    w25_data = json.loads(W25_PATH.read_text())
    w40 = source_from_json_blocks(
        w40_data["engine_audit"]["witness_B_integral"]["source"]
    )
    w25 = source_from_json_blocks(w25_data["blocks"])
    return w40, w25


def raw_word_rows(source, source_name):
    records = []
    counts = Counter()
    for word in product(COLOURS, repeat=8):
        value = hafnian(source, word)
        target = Fraction(1) if len(set(word)) == 1 else Fraction(0)
        off = off_count(word)
        defect = value - target
        records.append({
            "source": source_name,
            "word": "".join(map(str, word)),
            "off_count": off,
            "amplitude": str(value),
            "target": str(target),
            "defect": str(defect),
        })
        counts[(off, bool(defect))] += 1
    return records, counts


def write_jsonl(path, rows):
    with path.open("w") as handle:
        for row in rows:
            handle.write(json.dumps(stringify(row), sort_keys=True) + "\n")


def transpose_cap_columns(row):
    return [row[3 * j + i] for i in COLOURS for j in COLOURS]


def full_response_support(source, p, q, cap):
    residual = tuple(site for site in SITES if site not in (p, q))
    support = []
    for a, b in combinations(residual, 2):
        for alpha in COLOURS:
            for beta in COLOURS:
                value = dot(
                    response_row(source, p, q, a, b, alpha, beta), cap
                )
                if value:
                    support.append({
                        "edge": [a, b],
                        "cell": [alpha, beta],
                        "value": str(value),
                    })
    return support


def source_profile(source, source_name):
    records = []
    reversal_checked = 0
    mutant_differences = 0
    for p, q in combinations(SITES, 2):
        residual = tuple(site for site in SITES if site not in (p, q))
        for centre in residual:
            record = response_star_record(source, p, q, centre)
            labels_rev, rows_rev = response_star_matrix(source, q, p, centre)
            require(labels_rev == record["row_labels"], (p, q, centre))
            expected_rev = [transpose_cap_columns(row) for row in record["rows"]]
            require(rows_rev == expected_rev, (source_name, p, q, centre))
            reversal_checked += 1

            _, mutant_rows = response_star_matrix(
                source, p, q, centre, mutant=True
            )
            mutant_differences += sum(
                left != right for left, right in zip(record["rows"], mutant_rows)
            )
            record["source"] = source_name
            record["matrix_sha256"] = canonical_digest({
                "labels": record["row_labels"], "rows": record["rows"]
            })
            records.append(record)
    require(len(records) == 168, (source_name, len(records)))
    return records, reversal_checked, mutant_differences


def source_triangle_profile(source, source_name):
    records = []
    reversal_checked = 0
    mutant_differences = 0
    for p, q in combinations(SITES, 2):
        residual = tuple(site for site in SITES if site not in (p, q))
        for triangle in combinations(residual, 3):
            record = response_triangle_record(source, p, q, triangle)
            labels_rev, rows_rev = response_triangle_matrix(
                source, q, p, triangle
            )
            require(labels_rev == record["row_labels"], (p, q, triangle))
            expected_rev = [transpose_cap_columns(row) for row in record["rows"]]
            require(rows_rev == expected_rev, (source_name, p, q, triangle))
            reversal_checked += 1
            _, mutant_rows = response_triangle_matrix(
                source, p, q, triangle, mutant=True
            )
            mutant_differences += sum(
                left != right for left, right in zip(record["rows"], mutant_rows)
            )
            record["source"] = source_name
            record["matrix_sha256"] = canonical_digest({
                "labels": record["row_labels"], "rows": record["rows"]
            })
            records.append(record)
    require(len(records) == 560, (source_name, len(records)))
    return records, reversal_checked, mutant_differences


def summarize_profile(records):
    passes = [record for record in records if record["passes"]]
    blocker_types = Counter()
    rank_histogram = Counter()
    for record in records:
        rank_histogram[record["rank"]] += 1
        blocker_types[tuple(record["activity_in_rowspan"])] += 1
    return {
        "choices": len(records),
        "passing_choices": len(passes),
        "rank_histogram": {str(key): value for key, value in sorted(rank_histogram.items())},
        "blocker_pattern_histogram": {
            "".join("1" if bit else "0" for bit in key): value
            for key, value in sorted(blocker_types.items())
        },
        "passes": [
            {
                "pair": record["pair"],
                **({"centre": record["centre"]} if "centre" in record else
                   {"triangle": record["triangle"]}),
                "rank": record["rank"],
                "cap": stringify(record["cap"]),
                "matrix_sha256": record["matrix_sha256"],
            }
            for record in passes
        ],
    }


def zero_pairs(source):
    return [
        [p, q]
        for p, q in combinations(SITES, 2)
        if all(cell(source, p, q, i, j) == 0 for i in COLOURS for j in COLOURS)
    ]


def main():
    controls_run = set()
    w40, w25 = load_sources()
    controls_run.add("input_hashes")

    w40_rows, w40_counts = raw_word_rows(w40, "W40-integral-X4")
    w25_rows, w25_counts = raw_word_rows(w25, "W25-F8-X3")
    write_jsonl(HERE / "raw_x4_rows_w40.jsonl", w40_rows)
    write_jsonl(HERE / "raw_x4_rows_w25_f8.jsonl", w25_rows)

    w40_x4_failures = [
        row for row in w40_rows if row["off_count"] <= 4 and row["defect"] != "0"
    ]
    require(not w40_x4_failures, w40_x4_failures[:3])
    controls_run.add("raw_w40_x4")

    w25_x3_failures = [
        row for row in w25_rows if row["off_count"] <= 3 and row["defect"] != "0"
    ]
    w25_x4_failures = [
        row for row in w25_rows if row["off_count"] <= 4 and row["defect"] != "0"
    ]
    require(not w25_x3_failures, w25_x3_failures[:3])
    require(len(w25_x4_failures) == 78, len(w25_x4_failures))
    controls_run.add("raw_w25_x3_outside_x4")

    mutant = deepcopy(w40)
    require(mutant[(2, 6)][2][2] == -1, mutant[(2, 6)][2][2])
    mutant[(2, 6)][2][2] = Fraction(1)
    mutant_failures = []
    for word in product(COLOURS, repeat=8):
        if off_count(word) > 4:
            continue
        target = Fraction(1) if len(set(word)) == 1 else Fraction(0)
        if hafnian(mutant, word) != target:
            mutant_failures.append("".join(map(str, word)))
    require(mutant_failures, "W40 q26 sign mutation did not break raw X4")
    controls_run.add("w40_x4_sign_mutation_must_fire")

    w40_profile, rev40, mut40 = source_profile(w40, "W40-integral-X4")
    w25_profile, rev25, mut25 = source_profile(w25, "W25-F8-X3")
    require(rev40 == rev25 == 168, (rev40, rev25))
    controls_run.add("all_168_matrices_each_source")
    controls_run.add("endpoint_reversal_all_choices")
    require(mut40 + mut25 > 0, "endpoint-colour mutant agrees everywhere")
    controls_run.add("endpoint_colour_mutation_must_fire")

    w40_triangles, trev40, tmut40 = source_triangle_profile(
        w40, "W40-integral-X4"
    )
    w25_triangles, trev25, tmut25 = source_triangle_profile(
        w25, "W25-F8-X3"
    )
    require(trev40 == trev25 == 560, (trev40, trev25))
    controls_run.add("all_560_triangle_matrices_each_source")
    require(tmut40 + tmut25 > 0, "triangle endpoint-colour mutant agrees everywhere")

    write_jsonl(HERE / "response_star_matrices_w40.jsonl", w40_profile)
    write_jsonl(HERE / "response_star_matrices_w25_f8.jsonl", w25_profile)
    write_jsonl(HERE / "response_triangle_matrices_w40.jsonl", w40_triangles)
    write_jsonl(HERE / "response_triangle_matrices_w25_f8.jsonl", w25_triangles)

    target = next(
        record for record in w40_profile
        if record["pair"] == [6, 7] and record["centre"] == 5
    )
    identity = [Fraction(int(i == j)) for i in COLOURS for j in COLOURS]
    require(all(dot(row, identity) == 0 for row in target["rows"]), target)
    activities = [dot(row, identity) for row in activity_rows(w40, 6, 7)]
    require(activities == [1, 1, 1, 1], activities)
    support = full_response_support(w40, 6, 7, identity)
    require(support, "W40 identity response unexpectedly zero")
    require(all(5 in item["edge"] for item in support), support)
    controls_run.add("w40_675_identity_cap")

    w40_summary = summarize_profile(w40_profile)
    w25_summary = summarize_profile(w25_profile)
    w40_triangle_summary = summarize_profile(w40_triangles)
    w25_triangle_summary = summarize_profile(w25_triangles)
    require(w40_summary["passing_choices"] > 0, w40_summary)
    require(w25_summary["passing_choices"] == 0, w25_summary)
    require(w25_triangle_summary["passing_choices"] == 0, w25_triangle_summary)
    controls_run.add("w25_no_response_star_choice")

    dead25 = zero_pairs(w25)
    require(len(dead25) == 7, dead25)
    for pair in dead25:
        pair_records = [record for record in w25_profile if record["pair"] == pair]
        require(len(pair_records) == 6, pair)
        require(all(record["activity_in_rowspan"][3] for record in pair_records), pair)
    controls_run.add("zero_pair_inactivity")

    require(controls_run == DECLARED_CONTROLS, {
        "declared": sorted(DECLARED_CONTROLS),
        "executed": sorted(controls_run),
    })
    result = {
        "status": "PASS",
        "classification": "UNAUDITED EXACT RATIONAL RESPONSE-STAR AUDIT",
        "criterion": {
            "matrix_shape": [90, 9],
            "activity_forms": ["K00", "K11", "K22", "<K,A_pq>"],
            "passes_iff": "all four augmented ranks equal rank(L)+1",
        },
        "inputs": {
            "W40": {"path": str(W40_PATH.relative_to(ROOT)), "sha256": PINNED["W40"]},
            "W25-F8": {"path": str(W25_PATH.relative_to(ROOT)), "sha256": PINNED["W25-F8"]},
        },
        "raw_rows": {
            "W40": {
                "path": "raw_x4_rows_w40.jsonl",
                "rows": len(w40_rows),
                "sha256": digest(HERE / "raw_x4_rows_w40.jsonl"),
                "off_defect_counts": {
                    f"off{off}:defect{int(defect)}": count
                    for (off, defect), count in sorted(w40_counts.items())
                },
            },
            "W25-F8": {
                "path": "raw_x4_rows_w25_f8.jsonl",
                "rows": len(w25_rows),
                "sha256": digest(HERE / "raw_x4_rows_w25_f8.jsonl"),
                "off_defect_counts": {
                    f"off{off}:defect{int(defect)}": count
                    for (off, defect), count in sorted(w25_counts.items())
                },
                "off_le_4_failures": len(w25_x4_failures),
            },
        },
        "response_star": {
            "W40": {
                **w40_summary,
                "matrix_ledger": "response_star_matrices_w40.jsonl",
                "matrix_ledger_sha256": digest(HERE / "response_star_matrices_w40.jsonl"),
            },
            "W25-F8": {
                **w25_summary,
                "zero_pairs": dead25,
                "matrix_ledger": "response_star_matrices_w25_f8.jsonl",
                "matrix_ledger_sha256": digest(HERE / "response_star_matrices_w25_f8.jsonl"),
            },
            "W40_pair67_centre5_identity": {
                "L_rank": target["rank"],
                "L_times_vecI": [str(dot(row, identity)) for row in target["rows"]],
                "activity_values": [str(value) for value in activities],
                "response_support": support,
                "all_response_edges_incident_to_5": True,
            },
            "triangle_extension": {
                "meaning": (
                    "kill all response edges outside a residual 3-set; the "
                    "surviving graph has matching number at most one"
                ),
                "W40": {
                    **w40_triangle_summary,
                    "matrix_ledger": "response_triangle_matrices_w40.jsonl",
                    "matrix_ledger_sha256": digest(
                        HERE / "response_triangle_matrices_w40.jsonl"
                    ),
                },
                "W25-F8": {
                    **w25_triangle_summary,
                    "matrix_ledger": "response_triangle_matrices_w25_f8.jsonl",
                    "matrix_ledger_sha256": digest(
                        HERE / "response_triangle_matrices_w25_f8.jsonl"
                    ),
                },
            },
        },
        "negative_controls": {
            "W40_q26_sign_mutant_x4_failures": mutant_failures,
            "endpoint_colour_mutant_differing_rows": (
                mut40 + mut25 + tmut40 + tmut25
            ),
        },
        "controls": {
            "declared": sorted(DECLARED_CONTROLS),
            "executed": sorted(controls_run),
            "all_ran": True,
        },
    }
    output = HERE / "results_response_star.json"
    output.write_text(json.dumps(stringify(result), indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "W40_passing_choices": w40_summary["passing_choices"],
        "W25_passing_choices": w25_summary["passing_choices"],
        "W40_triangle_passing_choices": w40_triangle_summary["passing_choices"],
        "W25_triangle_passing_choices": w25_triangle_summary["passing_choices"],
        "W25_X4_failures": len(w25_x4_failures),
        "controls": result["controls"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
