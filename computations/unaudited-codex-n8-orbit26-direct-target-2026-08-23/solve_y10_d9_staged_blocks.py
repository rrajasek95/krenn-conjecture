#!/usr/bin/env python3
"""Bounded target-rooted y9 collision components at total degree nine."""

from collections import Counter, defaultdict, deque
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
STAGE6_PATH = HERE / "solve_y10_d6_staged_blocks.py"
D8_TERMINAL = HERE / "results_y10_d8_terminal.json"
D9_INCIDENT = HERE / "results_y10_dead_row_original_d9.json"
RESULTS = HERE / "results_y10_d9_staged_blocks.json"
CORE_PACKET = HERE / "d9_first_singleton_core.json"
TIME_CAP_SECONDS = 285.0
ROW_CAP = 8_000_000
COLUMN_CAP = 250_000


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


spec = importlib.util.spec_from_file_location("y10_d9_stage6", STAGE6_PATH)
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
        polynomial = STAGE6.top_polynomial(originals[column[0]], column[1])
        require(all(len(row) == 9 for row in polynomial),
                "d9 top output degree changed")
        column_rows = set(polynomial)
        column_to_rows[column] = column_rows
        for row in column_rows:
            row_to_columns[row].add(column)
            if row in rows:
                continue
            rows.add(row)
            seen_terms = set()
            for positions in combinations(range(9), 4):
                term = bytes(row[index] for index in positions)
                if term in seen_terms:
                    continue
                seen_terms.add(term)
                owners = top_term_to_codes.get(term)
                if not owners:
                    continue
                multiplier = STAGE6.quotient(row, term)
                require(len(multiplier) == 5,
                        "d9 inverse multiplier lost quintic degree")
                require(not any(5 in FIRST.D5.COORDINATES[value][:2]
                                for value in multiplier),
                        "d9 component multiplier acquired site 5")
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
    require(len(column_to_rows) == len(columns), "component closure incomplete")
    return columns, rows, column_to_rows, row_to_columns


def physical_matching(term):
    edges = frozenset(tuple(FIRST.D5.COORDINATES[value][:2]) for value in term)
    require(len(term) == len(edges) == 4, "top term lost four physical edges")
    degrees = Counter(site for edge in edges for site in edge)
    require(degrees == Counter({site: 1 for site in range(8)}),
            "top term is not a perfect matching")
    return edges


def cycle_type(first, second):
    symmetric = first ^ second
    if not symmetric:
        return "same_physical_matching"
    adjacency = defaultdict(set)
    for left, right in symmetric:
        adjacency[left].add(right)
        adjacency[right].add(left)
    require(all(len(values) == 2 for values in adjacency.values()),
            "matching difference is not a cycle union")
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


def freeze_core(component_index, columns, rows, row_to_columns,
                residual_columns, originals):
    active_rows = []
    cycle_types = Counter()
    edge_count = 0
    for row in sorted(rows):
        owners = sorted(row_to_columns[row] & residual_columns)
        if not owners:
            continue
        require(len(owners) >= 2, "residual core retained a singleton row")
        edge_count += len(owners)
        matchings = []
        for code, multiplier in owners:
            term = STAGE6.quotient(row, multiplier)
            require(len(term) == 4 and term in originals[code],
                    "core owner lost literal source term")
            matchings.append(physical_matching(term))
        for first in range(len(matchings)):
            for second in range(first + 1, len(matchings)):
                cycle_types[cycle_type(matchings[first], matchings[second])] += 1
        active_rows.append([
            row.hex(), [[code, multiplier.hex()] for code, multiplier in owners]
        ])
    packet = {
        "format": "n8-orbit26-d9-first-singleton-core-v1",
        "component_index": component_index,
        "closed_component_columns": len(columns),
        "closed_component_rows": len(rows),
        "residual_columns": [[code, multiplier.hex()]
                             for code, multiplier in sorted(residual_columns)],
        "residual_rows_with_edges": active_rows,
        "residual_edges": edge_count,
        "matching_pair_cycle_type_census": dict(sorted(cycle_types.items())),
    }
    encoded = json.dumps(packet, sort_keys=True, separators=(",", ":"))
    packet["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    CORE_PACKET.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n")
    return packet


def main():
    started = time.monotonic()
    d8 = json.loads(D8_TERMINAL.read_text())
    require(d8["logical_sha256"]
            == "5573ea640136fc17748aa131ec2bb6d5ad1c793834ce62ad9f7cbd689c31ad18",
            "d8 terminal theorem changed")
    incident = json.loads(D9_INCIDENT.read_text())
    require(incident["logical_sha256"]
            == "bcd18e073f231a5b37aeb8bbc98ba86724b871bd09d171b9c34d7fcfba5373b6",
            "d9 incidence census changed")
    originals, _lead_to_code = FIRST.original_basis()
    top_term_to_codes = defaultdict(list)
    for code, polynomial in originals.items():
        for row, coefficient in polynomial.items():
            if len(row) == 4:
                top_term_to_codes[row].append((code, coefficient))

    seeds = {(record["source_code"], bytes.fromhex(record["multiplier_y"]))
             for record in incident["incident_records"]
             if record["multiplier_t_exponent"] == 0}
    require(len(seeds) == 160, "d9 quintic seed census changed")
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
        remaining.difference_update(component_seeds)
        pivots, residual = STAGE6.singleton_column_peel(
            column_to_rows, row_to_columns
        )
        record = {
            "component_index": len(component_records) + 1,
            "lex_seed": [seed[0], seed[1].hex()],
            "seed_columns": len(component_seeds),
            "closed_columns": len(columns),
            "closed_rows": len(rows),
            "singleton_pivots": len(pivots),
            "singleton_residual_columns": len(residual),
            "column_digest": sha256(b"".join(
                code.to_bytes(2, "big") + multiplier
                for code, multiplier in sorted(columns)
            )).hexdigest(),
            "row_digest": sha256(b"".join(sorted(rows))).hexdigest(),
        }
        component_records.append(record)
        if residual:
            first_core = freeze_core(
                record["component_index"], columns, rows, row_to_columns,
                residual, originals
            )

    elapsed = time.monotonic() - started
    if bounded_stop is not None:
        status = "D9_CAP_UNRESOLVED_DURING_COMPONENT_CLOSURE"
    elif first_core is not None:
        status = "D9_EXACT_FIRST_SINGLETON_CORE"
    else:
        require(not remaining, "d9 standardness claimed with seeds remaining")
        status = "EXACT_TARGET_STANDARD_THROUGH_TOTAL_D9"
    result = {
        "format": "n8-orbit26-y10-d9-staged-components-v1",
        "status": status,
        "elapsed_seconds": elapsed,
        "time_cap_seconds": TIME_CAP_SECONDS,
        "row_cap": ROW_CAP,
        "column_cap": COLUMN_CAP,
        "new_t_free_y5_seeds": len(seeds),
        "seed_components_completed": len(component_records),
        "seed_columns_accounted": len(seeds) - len(remaining),
        "seed_columns_unprocessed": len(remaining),
        "component_records": component_records,
        "aggregate_closed_columns": sum(item["closed_columns"]
                                        for item in component_records),
        "aggregate_closed_rows": sum(item["closed_rows"]
                                     for item in component_records),
        "bounded_stop": bounded_stop,
        "first_core": None if first_core is None else {
            "component_index": first_core["component_index"],
            "closed_component_columns": first_core["closed_component_columns"],
            "closed_component_rows": first_core["closed_component_rows"],
            "residual_columns": len(first_core["residual_columns"]),
            "residual_rows": len(first_core["residual_rows_with_edges"]),
            "residual_edges": first_core["residual_edges"],
            "cycle_types": first_core["matching_pair_cycle_type_census"],
            "packet_logical_sha256": first_core["logical_sha256"],
        },
        "lower_slice_theorem": (
            "Positive-t d9 multiplier slices lie in t*M8 and are excluded by "
            "the frozen d8 standardness theorem if the new y5 head is injective."
        ),
        "scope": (
            "exact target-rooted y9 inverse incidence and singleton peel only; "
            "a core is not a rank defect and a cap is unresolved; no d10"
        ),
    }
    logical = dict(result)
    logical.pop("elapsed_seconds")
    encoded = json.dumps(logical, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("y10 d9 staged components:", status)
    print("components/accounted/remaining:", len(component_records),
          len(seeds) - len(remaining), len(remaining))
    print("first core:", result["first_core"])
    print("elapsed:", elapsed)
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
