#!/usr/bin/env python3
"""Bounded target-rooted y8 collision components at total degree eight.

Only normalized originals times a t-free encoded-y quartic are new modulo
t times the full degree-seven module.  Components are closed by literal y8
inverse incidence and private-row peeled one at a time.  The first nonempty
peel core is frozen exactly and terminates the run; no broad rank solve is
attempted.
"""

from collections import Counter, defaultdict, deque
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
STAGE6_PATH = HERE / "solve_y10_d6_staged_blocks.py"
D7_RESULTS = HERE / "results_y10_d7_staged_blocks.json"
D8_INCIDENT = HERE / "results_y10_dead_row_original_d8.json"
RESULTS = HERE / "results_y10_d8_staged_blocks.json"
CORE_PACKET = HERE / "d8_first_singleton_core.json"
TIME_CAP_SECONDS = 285.0
ROW_CAP = 8_000_000
COLUMN_CAP = 250_000


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


spec = importlib.util.spec_from_file_location("y10_d8_stage6", STAGE6_PATH)
STAGE6 = importlib.util.module_from_spec(spec)
require(spec.loader is not None, "cannot load staged source helpers")
spec.loader.exec_module(STAGE6)
FIRST = STAGE6.FIRST


class BoundedStop(Exception):
    def __init__(self, detail):
        super().__init__(detail)
        self.detail = detail


def close_component(seed, originals, top_term_to_codes, started):
    columns = {seed}
    rows = set()
    pending = deque([seed])
    column_to_rows = {}
    row_to_columns = defaultdict(set)
    processed = 0
    while pending:
        column = pending.popleft()
        polynomial = STAGE6.top_polynomial(
            originals[column[0]], column[1]
        )
        require(all(len(row) == 8 for row in polynomial),
                "d8 top output degree changed")
        column_rows = set(polynomial)
        column_to_rows[column] = column_rows
        for row in column_rows:
            row_to_columns[row].add(column)
            if row in rows:
                continue
            rows.add(row)
            seen_terms = set()
            for positions in combinations(range(8), 4):
                term = bytes(row[index] for index in positions)
                if term in seen_terms:
                    continue
                seen_terms.add(term)
                owners = top_term_to_codes.get(term)
                if not owners:
                    continue
                multiplier = STAGE6.quotient(row, term)
                require(len(multiplier) == 4,
                        "d8 inverse multiplier lost quartic degree")
                require(not any(5 in FIRST.D5.COORDINATES[value][:2]
                                for value in multiplier),
                        "d8 component multiplier acquired site 5")
                for owner, _coefficient in owners:
                    candidate = (owner, multiplier)
                    row_to_columns[row].add(candidate)
                    if candidate not in columns:
                        columns.add(candidate)
                        pending.append(candidate)
        processed += 1
        if processed % 128 == 0:
            elapsed = time.monotonic() - started
            if elapsed > TIME_CAP_SECONDS:
                raise BoundedStop({
                    "reason": "time_cap",
                    "elapsed_seconds": elapsed,
                    "active_seed": [seed[0], seed[1].hex()],
                    "columns_discovered": len(columns),
                    "columns_processed": processed,
                    "rows_discovered": len(rows),
                })
            if len(rows) > ROW_CAP or len(columns) > COLUMN_CAP:
                raise BoundedStop({
                    "reason": "size_cap",
                    "elapsed_seconds": elapsed,
                    "active_seed": [seed[0], seed[1].hex()],
                    "columns_discovered": len(columns),
                    "columns_processed": processed,
                    "rows_discovered": len(rows),
                    "row_cap": ROW_CAP,
                    "column_cap": COLUMN_CAP,
                })
    # Every inverse provider was queued, so every adjacency is now complete.
    require(len(column_to_rows) == len(columns), "component closure incomplete")
    return columns, rows, column_to_rows, row_to_columns


def physical_matching(term):
    edges = frozenset(tuple(FIRST.D5.COORDINATES[value][:2]) for value in term)
    require(len(term) == len(edges) == 4, "top term lost four physical edges")
    degrees = Counter(site for edge in edges for site in edge)
    require(degrees == Counter({site: 1 for site in range(8)}),
            "top term is not a physical perfect matching")
    return edges


def matching_cycle_type(first, second):
    symmetric = first ^ second
    if not symmetric:
        return "same_physical_matching"
    adjacency = defaultdict(set)
    for left, right in symmetric:
        adjacency[left].add(right)
        adjacency[right].add(left)
    require(all(len(neighbours) == 2 for neighbours in adjacency.values()),
            "matching symmetric difference is not a cycle union")
    unseen = set(adjacency)
    sizes = []
    while unseen:
        start = min(unseen)
        component = {start}
        queue = deque([start])
        unseen.remove(start)
        while queue:
            site = queue.popleft()
            for neighbour in adjacency[site]:
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    component.add(neighbour)
                    queue.append(neighbour)
        sizes.append(len(component))
    return "+".join(f"C{size}" for size in sorted(sizes))


def freeze_core(component_index, columns, rows, column_to_rows,
                row_to_columns, residual_columns, originals):
    active_rows = []
    edge_count = 0
    cycle_types = Counter()
    multiplier_site5 = 0
    for _code, multiplier in residual_columns:
        multiplier_site5 += any(
            5 in FIRST.D5.COORDINATES[value][:2] for value in multiplier
        )
    require(multiplier_site5 == 0,
            "a residual multiplier unexpectedly touches site 5")
    for row in sorted(rows):
        owners = sorted(row_to_columns[row] & residual_columns)
        if not owners:
            continue
        require(len(owners) >= 2,
                "singleton residual core retained a private row")
        edge_count += len(owners)
        matchings = []
        for code, multiplier in owners:
            term = STAGE6.quotient(row, multiplier)
            require(len(term) == 4 and term in originals[code],
                    "core owner lost its literal top source term")
            matchings.append(physical_matching(term))
        for first_index in range(len(matchings)):
            for second_index in range(first_index + 1, len(matchings)):
                cycle_types[matching_cycle_type(
                    matchings[first_index], matchings[second_index]
                )] += 1
        active_rows.append([
            row.hex(),
            [[code, multiplier.hex()] for code, multiplier in owners],
        ])
    packet = {
        "format": "n8-orbit26-d8-first-singleton-core-v1",
        "component_index": component_index,
        "closed_component_columns": len(columns),
        "closed_component_rows": len(rows),
        "residual_columns": [
            [code, multiplier.hex()]
            for code, multiplier in sorted(residual_columns)
        ],
        "residual_rows_with_edges": active_rows,
        "residual_edges": edge_count,
        "residual_multiplier_site5_count": multiplier_site5,
        "matching_pair_cycle_type_census": dict(sorted(cycle_types.items())),
    }
    encoded = json.dumps(packet, sort_keys=True, separators=(",", ":"))
    packet["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    CORE_PACKET.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n")
    return packet


def main():
    started = time.monotonic()
    d7 = json.loads(D7_RESULTS.read_text())
    require(d7["status"] == "EXACT_TARGET_STANDARD_THROUGH_TOTAL_D7"
            and d7["logical_sha256"]
            == "30e98f20fd4f5f7a08b43295cf6eb93b46cefc96a232dc44ed0a03c72538251a",
            "frozen d7 standardness theorem changed")
    incident = json.loads(D8_INCIDENT.read_text())
    require(incident["logical_sha256"]
            == "e5388aeb4ff6adfe87d30457a933c5dddadc3c7b5a6a96344b1179ac9570b0ce",
            "d8 incidence census changed")
    originals, _lead_to_code = FIRST.original_basis()
    top_term_to_codes = defaultdict(list)
    top_occurrences = 0
    for code, polynomial in originals.items():
        for row, coefficient in polynomial.items():
            if len(row) == 4:
                top_term_to_codes[row].append((code, coefficient))
                top_occurrences += 1
    require(top_occurrences == 567_338, "original top occurrence census changed")

    seeds = set()
    seed_slice_histogram = Counter()
    for record in incident["incident_records"]:
        multiplier = bytes.fromhex(record["multiplier_y"])
        if len(multiplier) == 4:
            seeds.add((record["source_code"], multiplier))
            row_lengths = {len(bytes.fromhex(item[0]))
                           for item in record["target_rows"]}
            require(len(row_lengths) == 1,
                    "one d8 seed crossed target t slices")
            seed_slice_histogram[8 - next(iter(row_lengths))] += 1
    require(len(seeds) == incident["new_t_free_y4_seed_columns"] == 205,
            "d8 seed census changed")
    require(seed_slice_histogram == Counter({1: 61, 2: 144}),
            "d8 seed target-slice census changed")

    remaining = set(seeds)
    component_records = []
    first_core = None
    bounded_stop = None
    while remaining and first_core is None:
        seed = min(remaining)
        try:
            columns, rows, column_to_rows, row_to_columns = close_component(
                seed, originals, top_term_to_codes, started
            )
        except BoundedStop as stopped:
            bounded_stop = stopped.detail
            break
        component_seeds = columns & seeds
        require(seed in component_seeds, "active seed left its component")
        remaining.difference_update(component_seeds)
        pivot_ledger, residual_columns = STAGE6.singleton_column_peel(
            column_to_rows, row_to_columns
        )
        record = {
            "component_index": len(component_records) + 1,
            "lex_seed": [seed[0], seed[1].hex()],
            "seed_columns": len(component_seeds),
            "closed_columns": len(columns),
            "closed_rows": len(rows),
            "singleton_pivots": len(pivot_ledger),
            "singleton_residual_columns": len(residual_columns),
            "column_digest": sha256(b"".join(
                code.to_bytes(2, "big") + multiplier
                for code, multiplier in sorted(columns)
            )).hexdigest(),
            "row_digest": sha256(b"".join(sorted(rows))).hexdigest(),
        }
        component_records.append(record)
        if residual_columns:
            first_core = freeze_core(
                record["component_index"], columns, rows, column_to_rows,
                row_to_columns, residual_columns, originals
            )

    elapsed = time.monotonic() - started
    if bounded_stop is not None:
        status = "D8_CAP_UNRESOLVED_DURING_COMPONENT_CLOSURE"
    elif first_core is not None:
        status = "D8_EXACT_FIRST_SINGLETON_CORE"
    else:
        status = "EXACT_TARGET_STANDARD_THROUGH_TOTAL_D8"
        require(not remaining, "standardness claimed before every seed component")

    result = {
        "format": "n8-orbit26-y10-d8-staged-components-v1",
        "status": status,
        "elapsed_seconds": elapsed,
        "time_cap_seconds": TIME_CAP_SECONDS,
        "row_cap": ROW_CAP,
        "column_cap": COLUMN_CAP,
        "new_t_free_y4_seeds": len(seeds),
        "new_seed_target_t_exponent_histogram": dict(sorted(
            seed_slice_histogram.items()
        )),
        "seed_components_completed": len(component_records),
        "seed_columns_accounted": len(seeds) - len(remaining),
        "seed_columns_unprocessed": len(remaining),
        "component_records": component_records,
        "aggregate_closed_columns": sum(
            item["closed_columns"] for item in component_records
        ),
        "aggregate_closed_rows": sum(
            item["closed_rows"] for item in component_records
        ),
        "largest_component_columns": max(
            (item["closed_columns"] for item in component_records), default=0
        ),
        "largest_component_rows": max(
            (item["closed_rows"] for item in component_records), default=0
        ),
        "bounded_stop": bounded_stop,
        "first_core": None if first_core is None else {
            "component_index": first_core["component_index"],
            "closed_component_columns": first_core["closed_component_columns"],
            "closed_component_rows": first_core["closed_component_rows"],
            "residual_columns": len(first_core["residual_columns"]),
            "residual_rows": len(first_core["residual_rows_with_edges"]),
            "residual_edges": first_core["residual_edges"],
            "packet_logical_sha256": first_core["logical_sha256"],
        },
        "lower_slice_theorem": (
            "All d8 columns with positive multiplier t exponent lie in t*M7. "
            "If the new y4 head is injective, frozen d7 standardness excludes "
            "every lower y7*t or y6*t^2 target pivot."
        ),
        "scope": (
            "exact target-rooted inverse-incidence components and singleton peel "
            "only; a residual core is not a rank defect, while a bounded stop is "
            "unresolved. No degree-nine computation."
        ),
        "source_sha256": {
            str(D8_INCIDENT.relative_to(HERE.parents[1])):
                sha256(D8_INCIDENT.read_bytes()).hexdigest(),
            str(STAGE6_PATH.relative_to(HERE.parents[1])):
                sha256(STAGE6_PATH.read_bytes()).hexdigest(),
        },
    }
    logical_result = dict(result)
    logical_result.pop("elapsed_seconds")
    encoded = json.dumps(logical_result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("y10 d8 staged components:", status)
    print("components/accounted/remaining:", len(component_records),
          len(seeds) - len(remaining), len(remaining))
    print("first core:", result["first_core"])
    print("elapsed:", elapsed)
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
