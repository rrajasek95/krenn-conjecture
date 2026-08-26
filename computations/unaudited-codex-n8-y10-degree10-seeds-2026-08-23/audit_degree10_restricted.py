#!/usr/bin/env python3
"""Bounded target-rooted total-degree-10 restricted owner/seed peel.

Only primitive columns with t-free sextic multipliers are new modulo t*M9.
We restrict the y10 head to every top row of a target-touching primitive
column and include every literal owner of those rows.  A private-row peel
either removes every target seed or freezes the first seed-bearing residue.
No degree-11 work is performed.
"""

from collections import defaultdict, deque
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import resource
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D8_BASE_PATH = (
    ROOT / "computations/unaudited-codex-n8-y10-first-possible-degree-2026-08-23"
    / "audit_first_possible_degree.py"
)
D9_PATH = (
    ROOT / "computations/unaudited-codex-n8-y10-degree9-seeds-2026-08-23"
    / "audit_degree9_seeds.py"
)
TIME_CAP_SECONDS = 300.0
RSS_CAP_BYTES = 12 * 1024 ** 3
EXPECTED_LOGICAL_SHA256 = (
    "d594eca45d977fae501602b8e2ee250d7ddabc9c4c4eb1e0f557d198b051a0fa"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def peak_rss_bytes():
    # macOS reports ru_maxrss in bytes; Linux reports KiB.  This workspace is
    # macOS, but retain the platform guard for isolated replay portability.
    import sys
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value if sys.platform == "darwin" else value * 1024


class BoundedStop(Exception):
    pass


def check_cap(started, checkpoint):
    elapsed = time.monotonic() - started
    rss = peak_rss_bytes()
    if elapsed > TIME_CAP_SECONDS:
        raise BoundedStop({
            "reason": "time_cap", "checkpoint": checkpoint,
            "elapsed_seconds": elapsed, "peak_rss_bytes": rss,
        })
    if rss > RSS_CAP_BYTES:
        raise BoundedStop({
            "reason": "rss_cap", "checkpoint": checkpoint,
            "elapsed_seconds": elapsed, "peak_rss_bytes": rss,
        })


def singleton_peel(column_to_rows, row_to_columns):
    active = set(column_to_rows)
    active_by_row = {
        row: set(columns) for row, columns in row_to_columns.items()
    }
    queue = deque(sorted(
        row for row, columns in active_by_row.items() if len(columns) == 1
    ))
    pivots = []
    while queue:
        row = queue.popleft()
        owners = active_by_row[row] & active
        if len(owners) != 1:
            continue
        column = next(iter(owners))
        active.remove(column)
        pivots.append((column, row))
        for touched in column_to_rows[column]:
            active_by_row[touched].discard(column)
            if len(active_by_row[touched] & active) == 1:
                queue.append(touched)
    return pivots, active


def first_seed_component(residual, seeds, column_to_rows, row_to_columns):
    live_seeds = residual & seeds
    if not live_seeds:
        return None
    start = min(live_seeds)
    columns = {start}
    rows = set()
    pending = [start]
    while pending:
        column = pending.pop()
        for row in column_to_rows[column]:
            owners = row_to_columns[row] & residual
            if not owners:
                continue
            rows.add(row)
            for owner in owners:
                if owner not in columns:
                    columns.add(owner)
                    pending.append(owner)
    incidence = sum(
        len(row_to_columns[row] & columns) for row in rows
    )
    encoded_columns = b"".join(
        code.to_bytes(2, "big") + multiplier for code, multiplier in sorted(columns)
    )
    encoded_rows = b"".join(sorted(rows))
    return {
        "lex_seed": [start[0], start[1].hex()],
        "columns": len(columns),
        "rows": len(rows),
        "incidences": incidence,
        "target_seed_columns": len(columns & seeds),
        "column_sha256": sha256(encoded_columns).hexdigest(),
        "row_sha256": sha256(encoded_rows).hexdigest(),
        "sample_columns": [
            [code, multiplier.hex()] for code, multiplier in sorted(columns)[:16]
        ],
        "sample_rows": [row.hex() for row in sorted(rows)[:16]],
    }


def audit():
    started = time.monotonic()
    base = load(D8_BASE_PATH, "n8_d10_base")
    d9_module = load(D9_PATH, "n8_d10_d9_authority")
    d9 = d9_module.audit()
    require(d9["status"] == "EXACT_TARGET_STANDARD_THROUGH_TOTAL_D9"
            and d9["logical_sha256"]
            == "fee70f071e6123712a6d060c5dd2aadc4f9e7c79efc082b660343fb77d1238de",
            "the frozen exact degree-nine authority changed")
    check_cap(started, "degree9_authority")

    source = base.load_source()
    originals, _leads = source.FIRST.original_basis()
    term_sources = base.make_term_sources(originals)
    coordinates = source.D5.COORDINATES

    slice_data = {
        y_degree: base.record_slice(
            term_sources, coordinates, 10, y_degree
        )
        for y_degree in (8, 9, 10)
    }
    slices = [slice_data[y_degree][0] for y_degree in sorted(slice_data)]
    require(slices[-1]["direct_source_columns"] == 0,
            "a t-free y10 divisor acquired source incidence despite missing site5")
    seeds = {
        key
        for _y_degree, (_record, columns, _witnesses) in slice_data.items()
        for values in columns.values()
        for key in values
        if len(key[1]) == 6
    }
    check_cap(started, "primitive_seed_census")

    top_sources = defaultdict(list)
    for code, polynomial in originals.items():
        for term, coefficient in polynomial.items():
            if len(term) == 4:
                top_sources[term].append((code, coefficient))

    rows = set()
    column_to_rows = defaultdict(set)
    row_to_columns = defaultdict(set)
    for seed_index, (code, multiplier) in enumerate(sorted(seeds), 1):
        for term, coefficient in originals[code].items():
            if len(term) != 4:
                continue
            row = bytes(sorted(term + multiplier))
            rows.add(row)
        if seed_index % 32 == 0:
            check_cap(started, f"seed_rows_{seed_index}")

    for row_index, row in enumerate(sorted(rows), 1):
        for term in base.divisors(row, 4):
            owners = top_sources.get(term)
            if not owners:
                continue
            multiplier = base.quotient(row, term)
            require(len(multiplier) == 6,
                    "a degree-ten top owner lost sextic multiplier degree")
            for code, coefficient in owners:
                require(coefficient != 0, "a literal top owner has zero coefficient")
                column = (code, multiplier)
                column_to_rows[column].add(row)
                row_to_columns[row].add(column)
        if row_index % 512 == 0:
            check_cap(started, f"owner_rows_{row_index}")
    require(seeds <= set(column_to_rows),
            "a primitive target seed disappeared from its own top rows")

    pivots, residual = singleton_peel(column_to_rows, row_to_columns)
    residual_seeds = residual & seeds
    first_core = first_seed_component(
        residual, seeds, column_to_rows, row_to_columns
    )
    elapsed = time.monotonic() - started
    if residual_seeds:
        status = "D10_TARGET_RELEVANT_RESTRICTED_CORE"
    else:
        status = "EXACT_TARGET_STANDARD_THROUGH_TOTAL_D10"
    require((len(seeds), len(rows), len(column_to_rows),
             sum(map(len, row_to_columns.values())))
            == (84, 5186, 1303, 9156),
            "the degree-ten restricted owner census changed")
    require((len(pivots), len(residual), len(residual_seeds))
            == (558, 745, 0),
            "the degree-ten restricted peel ledger changed")

    payload = {
        "format": "n8-y10-degree10-restricted-owner-peel-v1",
        "status": status,
        "scope": (
            "exact degree-ten target-rooted seed-row restriction in the frozen "
            "normalized chart/t-last order; no degree-eleven claim"
        ),
        "target": base.TARGET.hex(),
        "d9_authority_logical_sha256": d9["logical_sha256"],
        "slices": slices,
        "primitive_seeds": len(seeds),
        "seed_top_rows": len(rows),
        "complete_owner_columns": len(column_to_rows),
        "complete_owner_incidences": sum(map(len, row_to_columns.values())),
        "singleton_pivots": len(pivots),
        "residual_columns": len(residual),
        "residual_seed_columns": len(residual_seeds),
        "residual_seed_list": [
            [code, multiplier.hex()] for code, multiplier in sorted(residual_seeds)
        ],
        "first_target_relevant_residual_core": first_core,
        "theorem_or_stop": (
            "If residual_seed_columns=0, restricting any full y10-head relation "
            "to these complete seed rows forces every primitive target seed "
            "coefficient to zero. All other d10 columns lie in t*M9, so frozen "
            "d9 standardness proves d10 standardness. If nonzero, the first "
            "seed-bearing restricted residue is unresolved and no membership "
            "inference is made."
        ),
        "time_cap_seconds": TIME_CAP_SECONDS,
        "rss_cap_bytes": RSS_CAP_BYTES,
        "elapsed_seconds_nonlogical": elapsed,
        "peak_rss_bytes_nonlogical": peak_rss_bytes(),
    }
    logical_payload = {
        key: value for key, value in payload.items()
        if not key.endswith("_nonlogical")
    }
    encoded = json.dumps(logical_payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = sha256(encoded.encode()).hexdigest()
    require(payload["logical_sha256"] == EXPECTED_LOGICAL_SHA256,
            "the degree-ten logical ledger changed")
    return payload


if __name__ == "__main__":
    try:
        print(json.dumps(audit(), indent=2, sort_keys=True))
    except BoundedStop as stopped:
        print(json.dumps({
            "status": "D10_BOUNDED_STOP_NO_INFERENCE",
            "detail": stopped.args[0],
            "scope": "no degree-ten or degree-eleven inference",
        }, indent=2, sort_keys=True))
