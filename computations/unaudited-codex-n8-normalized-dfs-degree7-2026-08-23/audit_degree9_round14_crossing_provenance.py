#!/usr/bin/env python3
"""Read-only provenance audit of the frozen degree-nine round-14 checkpoint.

The checkpoint stores the cumulative selected set but not per-round column
labels.  This checker classifies the exact cumulative post-initial packet,
audits private physical leaves and private top rows, exports one literal
collision cell, and gives a finite counterexample to recovering the last
2,452 labels from the archived aggregate ledger alone.  It performs no rank
or CEGAR solve.
"""

from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
from time import monotonic


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_degree8_dual_extension.py"
INITIAL_PATH = HERE / "results_degree9_initial_census.json"
CHECKPOINT_PATH = HERE / "results_degree9_rust_cegar_checkpoint.json"
RESULT_PATH = HERE / "results_degree9_rust_cegar.json"
OUTPUT_PATH = HERE / "results_degree9_round14_crossing_provenance.json"
EXPECTED_CHECKPOINT_SHA256 = "9100c0624464d0a82c0e11bde9a2782d555d1f1d7b7f7368b603a343928034a5"
EXPECTED_RESULT_SHA256 = "aaac0523fc590bf3ce5923972d8c2fd79639f6736c212d68f0bb9640340e6baf"
LAST_CROSSINGS = 2452


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def word_digits(code):
    digits = [0] * 8
    for index in range(7, -1, -1):
        digits[index] = code % 3
        code //= 3
    return tuple(digits)


def word_profile(code):
    counts = Counter(word_digits(code))
    return "".join(map(str, sorted((counts.get(c, 0) for c in range(3)), reverse=True)))


def partition(values):
    return "+".join(map(str, sorted(Counter(values).values(), reverse=True)))


def column_geometry(column, coordinates):
    cells = [coordinates[value] for value in column[1]]
    physical_edges = [(left, right) for left, right, _a, _b in cells]
    degrees = Counter(site for edge in physical_edges for site in edge)
    return {
        "word_profile": word_profile(column[0]),
        "physical_edge_multiplicity": partition(physical_edges),
        "exact_cell_multiplicity": partition(column[1]),
        "has_repeated_physical_edge": len(set(physical_edges)) < len(physical_edges),
        "has_repeated_exact_cell": len(set(column[1])) < len(column[1]),
        "has_private_leaf_site": any(value == 1 for value in degrees.values()),
        "private_leaf_sites": tuple(sorted(site for site, value in degrees.items() if value == 1)),
        "site_degree_partition": "+".join(map(str, sorted(degrees.values(), reverse=True))),
    }


def profile_census(columns, coordinates):
    answer = Counter()
    for column in columns:
        geometry = column_geometry(column, coordinates)
        key = (
            geometry["word_profile"],
            geometry["physical_edge_multiplicity"],
            geometry["site_degree_partition"],
            "private" if geometry["has_private_leaf_site"] else "no-private",
        )
        answer[key] += 1
    return [
        {
            "word_profile": key[0],
            "physical_edge_multiplicity": key[1],
            "site_degree_partition": key[2],
            "private_leaf_status": key[3],
            "count": count,
        }
        for key, count in sorted(answer.items())
    ]


def compact_census(columns, coordinates):
    word = Counter()
    edge = Counter()
    private = Counter()
    exact_repeat = Counter()
    for column in columns:
        geometry = column_geometry(column, coordinates)
        word[geometry["word_profile"]] += 1
        edge[geometry["physical_edge_multiplicity"]] += 1
        private[geometry["has_private_leaf_site"]] += 1
        exact_repeat[geometry["has_repeated_exact_cell"]] += 1
    return {
        "columns": len(columns),
        "word_profiles": dict(sorted(word.items())),
        "physical_edge_multiplicity": dict(sorted(edge.items())),
        "private_leaf_site": {str(key).lower(): value for key, value in sorted(private.items())},
        "repeated_exact_cell": {str(key).lower(): value for key, value in sorted(exact_repeat.items())},
    }


def source_record(column, coordinates):
    return {
        "word_code": column[0],
        "word": "".join(map(str, word_digits(column[0]))),
        "word_profile": word_profile(column[0]),
        "multiplier_hex": column[1].hex(),
        "multiplier_cells": [
            {
                "coordinate_id": value,
                "edge": [coordinates[value][0], coordinates[value][1]],
                "ordered_colours": [coordinates[value][2], coordinates[value][3]],
            }
            for value in column[1]
        ],
        "geometry": column_geometry(column, coordinates),
    }


def main():
    started = monotonic()
    require(sha256(CHECKPOINT_PATH.read_bytes()).hexdigest() == EXPECTED_CHECKPOINT_SHA256,
            "degree9 checkpoint digest changed")
    require(sha256(RESULT_PATH.read_bytes()).hexdigest() == EXPECTED_RESULT_SHA256,
            "degree9 terminal result digest changed")
    audit = load(AUDIT_PATH, "degree9_provenance_audit")
    source = audit.load_d7()
    coordinates = source.D5.COORDINATES
    initial_json = json.loads(INITIAL_PATH.read_text())
    checkpoint = json.loads(CHECKPOINT_PATH.read_text())
    terminal = json.loads(RESULT_PATH.read_text())
    require(checkpoint["completed_round"] == terminal["completed_round"] == 14,
            "terminal round changed")
    require(checkpoint["rounds"][-1]["new_violating_columns"] == LAST_CROSSINGS,
            "last crossing count changed")
    selected = sorted(
        (word, bytes.fromhex(multiplier))
        for word, multiplier in checkpoint["selected_columns"]
    )
    initial = {
        (item["word_code"], bytes.fromhex(item["multiplier_hex"]))
        for item in initial_json["violating_columns"]
    }
    added = sorted(set(selected) - initial)
    require(len(selected) == 53_995 and len(initial) == 2_308
            and len(added) == 51_687, "selected/initial/addition census changed")

    # The exact non-identifiability witness: the archive records only the
    # final union and per-round cardinalities.  Reassigning the lex-first or
    # lex-last 2,452 post-initial labels to round 14 preserves every archived
    # count while changing the literal profile census.
    hypothetical_first = added[:LAST_CROSSINGS]
    hypothetical_last = added[-LAST_CROSSINGS:]
    require(set(hypothetical_first).isdisjoint(hypothetical_last),
            "hypothetical histories unexpectedly overlap")
    first_profile = compact_census(hypothetical_first, coordinates)
    last_profile = compact_census(hypothetical_last, coordinates)
    require(first_profile != last_profile,
            "two provenance histories did not separate")

    # Literal top-incidence census on the cumulative post-initial packet.
    # Counts saturate at two because only privacy/collision is required.
    row_counts = {}
    top_nnz = 0
    coefficient_histogram = Counter()
    for index, column in enumerate(added, 1):
        for row, coefficient in audit.invariant_entries(source, column).items():
            if len(row) != 9:
                continue
            top_nnz += 1
            coefficient_histogram[coefficient] += 1
            row_counts[row] = min(2, row_counts.get(row, 0) + 1)
        if index % 5000 == 0:
            print("top incidence", index, "/", len(added),
                  "rows", len(row_counts), "elapsed", f"{monotonic()-started:.1f}", flush=True)
    private_rows = {row for row, count in row_counts.items() if count == 1}
    shared_rows = {row for row, count in row_counts.items() if count == 2}
    private_columns = 0
    no_private_columns = 0
    lex_collision_row = min(shared_rows)
    collision_owners = []
    for index, column in enumerate(added, 1):
        entries = audit.invariant_entries(source, column)
        top_rows = {row for row in entries if len(row) == 9}
        if top_rows & private_rows:
            private_columns += 1
        else:
            no_private_columns += 1
        if lex_collision_row in entries:
            collision_owners.append((column, entries[lex_collision_row]))
        if index % 5000 == 0:
            print("privacy replay", index, "/", len(added),
                  "elapsed", f"{monotonic()-started:.1f}", flush=True)
    collision_owners.sort()
    require(len(collision_owners) >= 2, "lex collision row lost its owners")
    first_column, first_coefficient = collision_owners[0]
    second_column, second_coefficient = collision_owners[1]
    first_entries = {
        row: coefficient for row, coefficient in
        audit.invariant_entries(source, first_column).items() if len(row) == 9
    }
    second_entries = {
        row: coefficient for row, coefficient in
        audit.invariant_entries(source, second_column).items() if len(row) == 9
    }
    cell = defaultdict(int)
    for row, coefficient in first_entries.items():
        cell[row] += second_coefficient * coefficient
    for row, coefficient in second_entries.items():
        cell[row] -= first_coefficient * coefficient
    cell = {row: coefficient for row, coefficient in cell.items() if coefficient}
    require(lex_collision_row not in cell, "collision S-cell failed to cancel pivot")
    cell_record = [[row.hex(), coefficient] for row, coefficient in sorted(cell.items())]
    cell_digest = sha256(json.dumps(cell_record, separators=(",", ":")).encode()).hexdigest()

    result = {
        "format": "n8-chart26-degree9-round14-crossing-provenance-v1",
        "status": "TERMINAL_PROVENANCE_NO_GO_WITH_CUMULATIVE_CLASSIFICATION",
        "checkpoint_sha256": EXPECTED_CHECKPOINT_SHA256,
        "terminal_result_sha256": EXPECTED_RESULT_SHA256,
        "frozen_scope": {
            "initial_columns": len(initial),
            "cumulative_selected_columns": len(selected),
            "cumulative_post_initial_columns": len(added),
            "last_crossing_count": LAST_CROSSINGS,
            "last_crossing_labels_stored": False,
            "last_crossing_coefficients_stored_with_labels": False,
        },
        "cumulative_post_initial_profile": compact_census(added, coordinates),
        "cumulative_post_initial_detailed_profile": profile_census(added, coordinates),
        "top_incidence": {
            "columns": len(added),
            "rows": len(row_counts),
            "nonzeros": top_nnz,
            "private_rows": len(private_rows),
            "shared_rows": len(shared_rows),
            "columns_with_private_top_row": private_columns,
            "columns_without_private_top_row": no_private_columns,
            "coefficient_histogram": dict(sorted(coefficient_histogram.items())),
        },
        "non_identifiability_witness": {
            "explanation": (
                "The lex-first and lex-last 2452-label subsets of the post-initial "
                "pool can be assigned to round 14 while preserving every stored "
                "per-round cardinality and unlabeled residue histogram; their "
                "literal profile censuses differ. Reconstructing the actual subset "
                "therefore requires rerunning the forbidden round-14 functional scan."
            ),
            "hypothetical_first": first_profile,
            "hypothetical_last": last_profile,
        },
        "lex_first_collision_cell": {
            "ordering": "lexicographically first shared canonical degree-nine top row, then first two source columns",
            "pivot_row_hex": lex_collision_row.hex(),
            "owner_count": len(collision_owners),
            "first_source": source_record(first_column, coordinates),
            "first_pivot_coefficient": first_coefficient,
            "second_source": source_record(second_column, coordinates),
            "second_pivot_coefficient": second_coefficient,
            "cancellation": [second_coefficient, -first_coefficient],
            "residual_top_rows": len(cell),
            "residual_sha256": cell_digest,
            "residual": cell_record,
        },
        "module_compression_verdict": (
            "No theorem-grade 2452-column module or D8-style antichain can be "
            "extracted from this checkpoint: the required source-label subset is "
            "not stored. The 51687-column cumulative envelope is exact but is not "
            "a replacement for the missing last-round packet."
        ),
        "scope_guard": "read-only label/incidence audit; no D9 solve, rank, membership, or nonmembership claim",
        "elapsed_seconds": monotonic() - started,
    }
    logical = dict(result)
    logical.pop("elapsed_seconds")
    result["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("terminal provenance audit", len(added), private_columns,
          no_private_columns, result["logical_sha256"],
          "elapsed", f"{result['elapsed_seconds']:.1f}")


if __name__ == "__main__":
    main()
