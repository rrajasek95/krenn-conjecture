#!/usr/bin/env python3
"""Exact capped target/lower-row-rooted K24 closure with arbitrary words."""
import argparse
import hashlib
import importlib.util
import json
import os
import resource
from collections import Counter
from functools import lru_cache
from pathlib import Path
from time import perf_counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROVIDER = ROOT / "computations/unaudited-codex-orbit0-k24-factorized-relative-production-gate-2026-08-24/k24_factorized_B20_provider.py"
PROVIDER_SHA = "689499ecf501eb37879b41f05e3f3caecfad454eaf57f5586b28edd7c616a018"
WITNESSES = ROOT / "computations/unaudited-codex-orbit0-k24-factorized-direct-d17-d18-producer-2026-08-24/prefix1_fast/literal_witnesses.tsv"
WITNESS_SHA = "477b9ae9249b72d2e1c9ba4c71fd5b63605866ce533c6c79eb199b8103dd001c"
ROW_LAYER_CAP = 257
COLUMN_LAYER_CAP = 257
GLOBAL_COLUMN_CAP = 1_000_000
GLOBAL_ROW_CAP = 1_000_000


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_provider():
    need(sha(PROVIDER) == PROVIDER_SHA, "provider hash")
    spec = importlib.util.spec_from_file_location("k24_arbitrary_word_closure_provider", PROVIDER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


P = None
FACTOR = None


@lru_cache(None)
def natural_row(row):
    return min(P.F.move_row(row, action) for action in P.H)


@lru_cache(None)
def term_table(word):
    terms = tuple(P.D24.BASE.word_terms(word))
    need(len(terms) == 105, "physical matching term census")
    histogram = Counter(P.D24.row_k_degree(term) for term in terms)
    need(set(histogram) <= {0, 1, 2, 3, 4} and sum(histogram.values()) == 105, "term degree histogram")
    payload = b"".join(terms)
    return terms, hashlib.sha256(payload).hexdigest()


def is_frozen_source_word(word):
    return tuple(word) == (word[0], word[0], word[2], word[2], word[4], word[4], word[6], word[6])


def natural_column(column):
    representative, orbit_size, *_ = FACTOR.fast_natural_canonical_and_orbit_size(column)
    need(orbit_size > 0 and 384 % orbit_size == 0, "column orbit divisor")
    return representative, orbit_size


def row_key(row):
    return f"K{P.D24.row_k_degree(row)}:{row.hex()}"


def column_key(column):
    return P.column_key(column)


def expand_rows(rows):
    columns = {}
    edges = set()
    literal_incident = 0
    for row in sorted(rows):
        need(natural_row(row) == row, "row not natural canonical")
        incidents = P.D24.incident_degree24_columns(row)
        literal_incident += len(incidents)
        local = set()
        for incident in incidents:
            representative, orbit_size = natural_column(incident)
            old = columns.setdefault(representative, orbit_size)
            need(old == orbit_size, "column orbit-size mismatch")
            local.add(representative)
        for column in local:
            edges.add((row, column))
    return columns, edges, literal_incident


def expand_columns(columns, cap):
    ordered = sorted(columns)
    selected = ordered[:cap]
    rows = {}
    edges = set()
    literal_outputs = 0
    for column in selected:
        terms, _digest = term_table(column[0])
        local = Counter()
        for term in terms:
            row = bytes(sorted(column[1] + term))
            representative = natural_row(row)
            degree = P.D24.row_k_degree(representative)
            need(0 <= degree <= 24, "ambient filtered output block")
            local[representative] += 1
            literal_outputs += 1
        for row, multiplicity in local.items():
            actual_degree = P.D24.row_k_degree(row)
            old = rows.setdefault(row, actual_degree)
            need(old == actual_degree, "row-degree mismatch")
            edges.add((column, row, multiplicity))
    return rows, edges, literal_outputs, len(selected), len(ordered) > cap


def write_rows(path, rows):
    lines = ["K_degree\tnatural_row_hex"]
    lines.extend(f"{P.D24.row_k_degree(row)}\t{row.hex()}" for row in sorted(rows))
    atomic_text(path, "\n".join(lines) + "\n")


def write_columns(path, columns):
    lines = ["natural_column_key\torbit_size\tfrozen_78_source_word"]
    lines.extend(f"{column_key(column)}\t{columns[column]}\t{int(is_frozen_source_word(column[0]))}" for column in sorted(columns))
    atomic_text(path, "\n".join(lines) + "\n")


def atomic_text(path, text):
    temporary = Path(str(path) + ".tmp")
    temporary.write_text(text)
    os.replace(temporary, path)


def layer_metrics(rows, columns, edges, literal_count, elapsed, capped=False):
    return {
        "unique_rows": len(rows),
        "unique_columns": len(columns),
        "unique_incidence_edges_E": len(edges),
        "literal_occurrences_examined": literal_count,
        "elapsed_seconds": elapsed,
        "layer_cap_reached": capped,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    output = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    need(not output.exists(), "refuse output overwrite")
    output.mkdir(parents=True)
    global P, FACTOR
    FACTOR = load_provider()
    P = FACTOR.P
    need(sha(WITNESSES) == WITNESS_SHA, "witness hash")
    lines = WITNESSES.read_text().splitlines()
    header = lines[0].split("\t")
    need(len(lines) == 258 and header[14] == "canonical_column_key" and header[19] == "literal_K24_row", "witness shape")
    source_columns = []
    lower_rows = set()
    target_rows = set()
    first_lower_row = None
    for expected, line in enumerate(lines[1:]):
        fields = line.split("\t")
        need(int(fields[2]) == expected, "sample bin sequence")
        column = P.parse_column_key(fields[14])
        representative, orbit_size = natural_column(column)
        need(representative == column and orbit_size == int(fields[15]), "sample natural column")
        source_columns.append(column)
        lower_counter = P.literal_block_counters(column) if hasattr(P, "literal_block_counters") else None
        # The provider module exposed here is the pinned top provider; use its
        # degree-24 engine directly for the unique K20 matching term.
        rows = P.D24.degree24_column_rows(column)
        realized_lower = [row for row in rows if P.D24.row_k_degree(row) == 20]
        need(len(realized_lower) == 1, "one K20 output per column")
        lower = natural_row(realized_lower[0])
        lower_rows.add(lower)
        if expected == 0:
            first_lower_row = lower
        target = bytes.fromhex(fields[19])
        need(len(target) == 24 and P.D24.row_k_degree(target) == 24, "literal target row")
        target_rows.add(natural_row(target))
    need(len(set(source_columns)) == len(lower_rows) == len(target_rows) == 257, "distributed seed dedup")
    total_begun = perf_counter()

    # Gate A: complete two alternating layers from one lower row, followed by
    # a deterministic 257-row prefix of the next row-to-column layer.
    need(first_lower_row is not None, "first lower row")
    one_seed = {first_lower_row}
    begun = perf_counter();one_columns, one_edges_01, one_literals_01 = expand_rows(one_seed);seconds_01 = perf_counter() - begun
    need(len(one_columns) == 56, "one-row incidence control drift")
    begun = perf_counter();one_rows_2, one_edges_12, one_literals_12, one_processed_columns, one_columns_capped = expand_columns(one_columns, len(one_columns));seconds_12 = perf_counter() - begun
    need(not one_columns_capped and one_processed_columns == len(one_columns), "one-row second layer completeness")
    one_row_prefix = set(sorted(one_rows_2)[:ROW_LAYER_CAP])
    begun = perf_counter();one_columns_3, one_edges_23, one_literals_23 = expand_rows(one_row_prefix);seconds_23 = perf_counter() - begun
    one_third_capped = len(one_rows_2) > ROW_LAYER_CAP

    # Gate B: all 257 distributed lower rows and all 257 target rows through
    # the exact inverse incidence layer, then a 257-column prefix forward.
    begun = perf_counter();lower_columns, lower_edges, lower_literals = expand_rows(lower_rows);seconds_lower = perf_counter() - begun
    begun = perf_counter();target_columns, target_edges, target_literals = expand_rows(target_rows);seconds_target = perf_counter() - begun
    combined_columns = dict(lower_columns)
    for column, orbit in target_columns.items():
        old = combined_columns.setdefault(column, orbit);need(old == orbit, "combined orbit mismatch")
    begun = perf_counter();distributed_rows_2, distributed_edges_12, distributed_literals_12, distributed_processed_columns, distributed_capped = expand_columns(combined_columns, COLUMN_LAYER_CAP);seconds_distributed_12 = perf_counter() - begun

    need(len(combined_columns) < GLOBAL_COLUMN_CAP, "bounded first layer unexpectedly exceeded global cap")
    need(len(distributed_rows_2) < GLOBAL_ROW_CAP, "bounded second layer unexpectedly exceeded global cap")
    write_rows(output / "one_lower_seed_rows.tsv", one_seed)
    write_columns(output / "one_lower_layer1_columns.tsv", one_columns)
    write_rows(output / "one_lower_layer2_rows.tsv", one_rows_2)
    write_columns(output / "one_lower_layer3_columns_prefix.tsv", one_columns_3)
    write_rows(output / "distributed257_lower_seed_rows.tsv", lower_rows)
    write_rows(output / "distributed257_target_seed_rows.tsv", target_rows)
    write_columns(output / "distributed257_lower_layer1_columns.tsv", lower_columns)
    write_columns(output / "distributed257_target_layer1_columns.tsv", target_columns)
    write_rows(output / "distributed257_layer2_rows_prefix.tsv", distributed_rows_2)

    word_rows = ["natural_word\tfrozen_78_source_word\tterm_count\tterm_table_sha256"]
    for word in sorted(term_table.cache_info() and {column[0] for column in one_columns} | {column[0] for column in combined_columns}):
        terms, digest = term_table(word)
        word_rows.append(f"{''.join(map(str, word))}\t{int(is_frozen_source_word(word))}\t{len(terms)}\t{digest}")
    atomic_text(output / "on_demand_word_tables.tsv", "\n".join(word_rows) + "\n")
    files = sorted(path for path in output.iterdir() if path.is_file())
    artifacts = {path.name: {"sha256": sha(path), "bytes": path.stat().st_size} for path in files}
    one_all_columns = set(one_columns) | set(one_columns_3)
    one_all_rows = one_seed | set(one_rows_2)
    one_all_edges = len(one_edges_01) + len(one_edges_12) + len(one_edges_23)
    arbitrary_words = {column[0] for column in combined_columns if not is_frozen_source_word(column[0])}
    need(arbitrary_words, "arbitrary-word repair not exercised")
    payload = {
        "status": "PASS_BOUNDED_K24_ARBITRARY_WORD_LAYERED_CLOSURE_NO_LAUNCH",
        "canonical_order_id": "natural_word_tuple_then_multiplier_bytes_v1",
        "H_order": len(P.H),
        "caps": {"row_layer": ROW_LAYER_CAP, "column_layer": COLUMN_LAYER_CAP, "global_columns": GLOBAL_COLUMN_CAP, "global_rows": GLOBAL_ROW_CAP},
        "one_K20_row_gate": {
            "layer0_lower_rows": len(one_seed),
            "layer1_row_to_column": layer_metrics(one_seed, one_columns, one_edges_01, one_literals_01, seconds_01),
            "layer2_column_to_row": layer_metrics(one_rows_2, one_columns, one_edges_12, one_literals_12, seconds_12),
            "layer3_row_to_column_prefix": layer_metrics(one_row_prefix, one_columns_3, one_edges_23, one_literals_23, seconds_23, one_third_capped),
            "known_unique_rows": len(one_all_rows),
            "known_unique_columns": len(one_all_columns),
            "known_unique_bipartite_edges_E": one_all_edges,
            "closure_status": "ROW_LAYER_CAP_257_NOT_COMPLETE" if one_third_capped else "NOT_QUEUES_DRAINED",
        },
        "distributed257_gate": {
            "lower_seed_rows": len(lower_rows),
            "target_seed_rows": len(target_rows),
            "lower_row_to_column": layer_metrics(lower_rows, lower_columns, lower_edges, lower_literals, seconds_lower),
            "target_row_to_column": layer_metrics(target_rows, target_columns, target_edges, target_literals, seconds_target),
            "combined_unique_columns": len(combined_columns),
            "column_to_row_prefix": layer_metrics(distributed_rows_2, dict(list(sorted(combined_columns.items()))[:COLUMN_LAYER_CAP]), distributed_edges_12, distributed_literals_12, seconds_distributed_12, distributed_capped),
            "processed_columns": distributed_processed_columns,
            "queued_columns": len(combined_columns) - distributed_processed_columns,
            "closure_status": "COLUMN_LAYER_CAP_257_NOT_COMPLETE" if distributed_capped else "NOT_QUEUES_DRAINED",
        },
        "word_tables": {
            "on_demand_tables_materialized": len(word_rows) - 1,
            "arbitrary_non_frozen_word_tables_realized": len(arbitrary_words),
            "frozen_78_source_dictionary_is_closure_complete": False,
            "hostile_restricted_word_domain_rejected": True,
        },
        "natural_order_dedup_exact": True,
        "lower_transfer_below_K20_complete": False,
        "global_verdict": "INCONCLUSIVE_INCOMPLETE_LAYERED_CLOSURE",
        "resources": {
            "total_seconds": perf_counter() - total_begun,
            "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "retained_bytes": sum(item["bytes"] for item in artifacts.values()),
        },
        "artifacts_before_result": artifacts,
        "provider_sha256": PROVIDER_SHA,
        "witness_sha256": WITNESS_SHA,
        "decision": "NO_LAUNCH: arbitrary-word repair works, but both layered queues remain capped and lower transfer is incomplete",
        "scope": "one K20 row plus 257 distributed lower/target row bounded layers only; no complete closure or K24 membership claim",
    }
    result = output / "results_k24_arbitrary_word_layered_closure_gate.json"
    atomic_text(result, json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
