#!/usr/bin/env python3
"""Structural census of primitive total-degree-nine target seeds.

No target-rooted closure or rank solve is performed.  We enumerate the new
columns with t-free quintic multipliers, their literal top-factorization
rows, and the smallest exchange packet that could seed a two-core.
"""

from collections import Counter, defaultdict, deque
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE_PATH = (
    ROOT / "computations/unaudited-codex-n8-y10-first-possible-degree-2026-08-23"
    / "audit_first_possible_degree.py"
)
D8_RESULT = (
    ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23"
    / "results_y10_d8_staged_blocks.json"
)
EXPECTED_LOGICAL_SHA256 = (
    "fee70f071e6123712a6d060c5dd2aadc4f9e7c79efc082b660343fb77d1238de"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_base():
    spec = importlib.util.spec_from_file_location("n8_d9_seed_base", BASE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def classify_seed_set(base, originals, term_sources, coordinates, primitive):
    top_sources = {
        term: tuple(codes) for term, codes in term_sources.items()
        if len(term) == 4
    }
    top_rows = set()
    seed_top_pairs = set()
    for code, multiplier in primitive:
        for term in originals[code]:
            if len(term) == 4:
                row = bytes(sorted(term + multiplier))
                top_rows.add(row)
                seed_top_pairs.add((row, term))

    row_factors = {}
    factorization_histogram = Counter()
    exchange_histogram = Counter()
    forced_site5_failures = 0
    smallest_exchange = None
    for row in sorted(top_rows):
        factors = []
        for term in base.divisors(row, 4):
            if term not in top_sources:
                continue
            multiplier = base.quotient(row, term)
            for code in top_sources[term]:
                factors.append((code, multiplier, term))
        factors = tuple(sorted(set(factors)))
        row_factors[row] = factors
        factorization_histogram[len(factors)] += 1
        site5_cells = [
            value for value in row if 5 in coordinates[value][:2]
        ]
        if len(site5_cells) != 1:
            forced_site5_failures += 1
        local_types = Counter()
        for first_index, first in enumerate(factors):
            for second in factors[first_index + 1:]:
                kind = base.exchange_type(first[2], second[2], coordinates)
                exchange_histogram[kind] += 1
                local_types[kind] += 1
        if len(factors) > 1 and smallest_exchange is None:
            smallest_exchange = {
                "top_row": row.hex(),
                "factorizations": [
                    {
                        "code": code,
                        "multiplier_y": multiplier.hex(),
                        "source_matching_y": term.hex(),
                    }
                    for code, multiplier, term in factors
                ],
                "exchange_types": dict(sorted(local_types.items())),
            }

    # One-shell leaf audit.  Rows are the literal top rows of direct seeds;
    # columns are every factorization of those rows.  Outside top rows of the
    # added columns are deliberately not closed, so any residual is only a
    # candidate core, never a kernel certificate.
    row_to_columns = {
        row: {(code, multiplier) for code, multiplier, _term in factors}
        for row, factors in row_factors.items()
    }
    column_to_rows = defaultdict(set)
    for row, columns in row_to_columns.items():
        for column in columns:
            column_to_rows[column].add(row)
    live_columns = set(column_to_rows)
    live_rows = set(row_to_columns)
    queue = deque(row for row in live_rows if len(row_to_columns[row]) == 1)
    peeled = 0
    while queue:
        row = queue.popleft()
        incident = row_to_columns[row] & live_columns
        if len(incident) != 1:
            continue
        column = next(iter(incident))
        live_columns.remove(column)
        peeled += 1
        for touched in column_to_rows[column]:
            if touched in live_rows:
                remaining = row_to_columns[touched] & live_columns
                if len(remaining) == 0:
                    live_rows.remove(touched)
                elif len(remaining) == 1:
                    queue.append(touched)

    residual_rows = {
        row for row in live_rows if len(row_to_columns[row] & live_columns) >= 2
    }
    residual_columns = {
        column for row in residual_rows
        for column in row_to_columns[row] if column in live_columns
    }

    def full_owners(row):
        owners = set()
        for term in base.divisors(row, 4):
            for code in top_sources.get(term, ()):
                owners.add((code, base.quotient(row, term)))
        return owners

    # Add only globally private outside rows of the shell-frontier columns.
    # Their owner census is complete by literal factorization, so these leaves
    # remain private even under the omitted full inverse-incidence closure.
    external_private = {}
    for column in sorted(residual_columns):
        code, multiplier = column
        known_rows = column_to_rows[column]
        for term in originals[code]:
            if len(term) != 4:
                continue
            row = bytes(sorted(term + multiplier))
            if row in known_rows:
                continue
            if full_owners(row) == {column}:
                external_private[column] = row
                break

    augmented_row_to_columns = {
        row: set(columns) & residual_columns
        for row, columns in row_to_columns.items()
        if set(columns) & residual_columns
    }
    augmented_column_to_rows = defaultdict(set)
    for row, columns in augmented_row_to_columns.items():
        for column in columns:
            augmented_column_to_rows[column].add(row)
    for column, row in external_private.items():
        augmented_row_to_columns[row] = {column}
        augmented_column_to_rows[column].add(row)
    augmented_live = set(residual_columns)
    augmented_queue = deque(sorted(
        row for row, columns in augmented_row_to_columns.items()
        if len(columns) == 1
    ))
    augmented_peeled = 0
    while augmented_queue:
        row = augmented_queue.popleft()
        incident = augmented_row_to_columns[row] & augmented_live
        if len(incident) != 1:
            continue
        column = next(iter(incident))
        augmented_live.remove(column)
        augmented_peeled += 1
        for touched in augmented_column_to_rows[column]:
            augmented_row_to_columns[touched].discard(column)
            if len(augmented_row_to_columns[touched] & augmented_live) == 1:
                augmented_queue.append(touched)

    # Connected components of the residual one-shell incidence graph.
    components = []
    unseen_columns = set(residual_columns)
    while unseen_columns:
        start = min(unseen_columns)
        columns = {start}
        rows = set()
        pending_columns = [start]
        while pending_columns:
            column = pending_columns.pop()
            unseen_columns.discard(column)
            for row in column_to_rows[column] & residual_rows:
                if row in rows:
                    continue
                rows.add(row)
                for neighbor in row_to_columns[row] & residual_columns:
                    if neighbor not in columns:
                        columns.add(neighbor)
                        pending_columns.append(neighbor)
        components.append((
            len(columns), len(rows), tuple(sorted(columns)), tuple(sorted(rows))
        ))
    components.sort(key=lambda item: (item[0], item[1], item[2], item[3]))
    smallest_component = None
    if components:
        column_count, row_count, component_columns, component_rows = components[0]
        row_incidence = []
        for row in component_rows:
            incident = tuple(sorted(row_to_columns[row] & set(component_columns)))
            pair_types = Counter()
            terms = []
            for code, multiplier in incident:
                term = base.quotient(row, multiplier)
                terms.append((code, multiplier, term))
            for first_index, first in enumerate(terms):
                for second in terms[first_index + 1:]:
                    pair_types[
                        base.exchange_type(first[2], second[2], coordinates)
                    ] += 1
            row_incidence.append({
                "row": row.hex(),
                "columns": [[code, multiplier.hex()]
                            for code, multiplier in incident],
                "exchange_types": dict(sorted(pair_types.items())),
            })
        smallest_component = {
            "column_count": column_count,
            "row_count": row_count,
            "columns": [[code, multiplier.hex()]
                        for code, multiplier in component_columns],
            "rows": [row.hex() for row in component_rows],
            "row_incidence": row_incidence,
        }

    return {
        "primitive_columns": len(primitive),
        "top_rows": len(top_rows),
        "seed_top_incidence_pairs": len(seed_top_pairs),
        "top_factorization_count_histogram": dict(sorted(
            factorization_histogram.items()
        )),
        "top_rows_with_multiple_factorizations": sum(
            count for degree, count in factorization_histogram.items()
            if degree > 1
        ),
        "pair_exchange_type_histogram": dict(sorted(exchange_histogram.items())),
        "rows_not_having_unique_site5_cell": forced_site5_failures,
        "smallest_row_local_exchange": smallest_exchange,
        "one_shell_scope": (
            "direct-seed top rows plus all their literal factorizations; "
            "outside top rows of newly added columns omitted"
        ),
        "one_shell_columns": len(column_to_rows),
        "one_shell_peeled_columns": peeled,
        "one_shell_residual_columns": len(residual_columns),
        "one_shell_residual_seed_columns": len(residual_columns & primitive),
        "one_shell_residual_rows": len(residual_rows),
        "one_shell_residual_components": len(components),
        "one_shell_smallest_candidate_component": smallest_component,
        "shell2_globally_private_frontier_columns": len(external_private),
        "shell2_augmented_peeled_columns": augmented_peeled,
        "shell2_residual_columns": len(augmented_live),
        "shell2_first_external_private_witness": (
            None if not external_private else {
                "column": [min(external_private)[0],
                           min(external_private)[1].hex()],
                "row": external_private[min(external_private)].hex(),
            }
        ),
    }


def audit():
    base = load_base()
    source = base.load_source()
    originals, _leads = source.FIRST.original_basis()
    term_sources = base.make_term_sources(originals)
    coordinates = source.D5.COORDINATES

    d8 = json.loads(D8_RESULT.read_text())
    require(d8["status"] == "EXACT_TARGET_STANDARD_THROUGH_TOTAL_D8",
            "the exact degree-eight terminal changed")
    require(d8["first_core"] is None and d8["seed_columns_unprocessed"] == 0,
            "the exact degree-eight private-row peel is no longer terminal")
    require(sum(item["closed_columns"] for item in d8["component_records"])
            == 70578, "the exact degree-eight closed-column count changed")
    require(sum(item["closed_rows"] for item in d8["component_records"])
            == 3650920, "the exact degree-eight closed-row count changed")

    slice_data = {
        y_degree: base.record_slice(
            term_sources, coordinates, 9, y_degree
        )
        for y_degree in (7, 8, 9)
    }
    slices = [slice_data[y_degree][0] for y_degree in sorted(slice_data)]
    require(slices[-1]["direct_source_columns"] == 0,
            "a t-free y9 target divisor acquired a source incidence")

    by_slice = {}
    primitive_all = set()
    for y_degree, (_record, columns, _witnesses) in slice_data.items():
        primitive = {
            key for values in columns.values() for key in values
            if len(key[1]) == 5
        }
        primitive_all.update(primitive)
        by_slice[f"y{y_degree}*t{9-y_degree}"] = classify_seed_set(
            base, originals, term_sources, coordinates, primitive
        )
    combined = classify_seed_set(
        base, originals, term_sources, coordinates, primitive_all
    )
    require(len(primitive_all) == 160,
            "the primitive degree-nine target seed census changed")
    require(combined["rows_not_having_unique_site5_cell"] == 0,
            "a primitive d9 target seed lost the forced site-5 cell")
    require(not ({"C8", "C4+C4"} & set(
        combined["pair_exchange_type_histogram"]
    )), "a no-shared-edge exchange entered the missing-site target packet")
    require(combined["one_shell_residual_seed_columns"] == 0,
            "a primitive target seed survived the exact one-shell peel")
    require(all(
        record["one_shell_residual_seed_columns"] == 0
        for record in by_slice.values()
    ), "a target slice retained a primitive seed after one-shell peel")

    payload = {
        "format": "n8-y10-degree9-structural-seeds-v1",
        "target": base.TARGET.hex(),
        "status": "EXACT_TARGET_STANDARD_THROUGH_TOTAL_D9",
        "scope": (
            "exact target standardness through total degree nine in the frozen "
            "normalized chart/t-last order; no degree-ten claim"
        ),
        "d8_result_sha256": sha256(D8_RESULT.read_bytes()).hexdigest(),
        "d8_terminal_logical_sha256": d8["logical_sha256"],
        "slices": slices,
        "by_slice": by_slice,
        "combined": combined,
        "theorem": (
            "The only new d9 columns modulo t*M8 have t-free quintic "
            "multipliers. Exactly 160 such columns touch target divisors. "
            "Taking every y9 top row of those seeds and every literal source "
            "factorization owner gives 1689 columns and 9976 rows. Exact "
            "private-row peeling removes 945 columns including all 160 seeds; "
            "the 744-column induced residue contains no seed. Therefore no y9 "
            "head relation can involve a new target-touching column. All other "
            "d9 columns lie in t*M8, and exact d8 standardness excludes their "
            "lower target pivots. Hence the target is standard through d9. "
            "The first apparent y8*t decoration-only square lies entirely in "
            "the nonseed frontier and is not a target obstruction."
        ),
    }
    logical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = sha256(logical.encode()).hexdigest()
    require(payload["logical_sha256"] == EXPECTED_LOGICAL_SHA256,
            "the degree-nine structural ledger changed")
    return payload


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
