#!/usr/bin/env python3
"""Bounded target-rooted total-degree-11 restricted owner/seed peel.

Only primitive columns with t-free septimic multipliers are new modulo t*M10.
The seed-row restriction is completed under every literal top owner and then
private-row peeled.  No degree-12 work is performed.
"""

from collections import defaultdict
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D10_PATH = (
    ROOT / "computations/unaudited-codex-n8-y10-degree10-seeds-2026-08-23"
    / "audit_degree10_restricted.py"
)
TIME_CAP_SECONDS = 300.0
RSS_CAP_BYTES = 12 * 1024 ** 3
EXPECTED_LOGICAL_SHA256 = (
    "98a5254238a87e79d7861640ee8b9cb4c88f68cdee57ca8251f9fe714df5e171"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


D10_HELPERS = load(D10_PATH, "n8_d11_d10_helpers")


def audit():
    started = time.monotonic()
    d10_module = D10_HELPERS
    d10 = d10_module.audit()
    require(d10["status"] == "EXACT_TARGET_STANDARD_THROUGH_TOTAL_D10"
            and d10["logical_sha256"]
            == "d594eca45d977fae501602b8e2ee250d7ddabc9c4c4eb1e0f557d198b051a0fa",
            "the frozen exact degree-ten authority changed")
    d10_module.check_cap(started, "degree10_authority")

    base = d10_module.load(d10_module.D8_BASE_PATH, "n8_d11_base")
    source = base.load_source()
    originals, _leads = source.FIRST.original_basis()
    term_sources = base.make_term_sources(originals)
    coordinates = source.D5.COORDINATES

    slice_data = {
        y_degree: base.record_slice(
            term_sources, coordinates, 11, y_degree
        )
        for y_degree in (9, 10, 11)
    }
    slices = [slice_data[y_degree][0] for y_degree in sorted(slice_data)]
    require(slices[-1]["direct_source_columns"] == 0,
            "an impossible y11 divisor acquired a source incidence")
    seeds = {
        key
        for _y_degree, (_record, columns, _witnesses) in slice_data.items()
        for values in columns.values()
        for key in values
        if len(key[1]) == 7
    }
    d10_module.check_cap(started, "primitive_seed_census")

    top_sources = defaultdict(list)
    for code, polynomial in originals.items():
        for term, coefficient in polynomial.items():
            if len(term) == 4:
                top_sources[term].append((code, coefficient))

    rows = set()
    for seed_index, (code, multiplier) in enumerate(sorted(seeds), 1):
        for term, coefficient in originals[code].items():
            if len(term) == 4:
                require(coefficient != 0, "a seed top term has zero coefficient")
                rows.add(bytes(sorted(term + multiplier)))
        if seed_index % 16 == 0:
            d10_module.check_cap(started, f"seed_rows_{seed_index}")

    column_to_rows = defaultdict(set)
    row_to_columns = defaultdict(set)
    for row_index, row in enumerate(sorted(rows), 1):
        for term in base.divisors(row, 4):
            owners = top_sources.get(term)
            if not owners:
                continue
            multiplier = base.quotient(row, term)
            require(len(multiplier) == 7,
                    "a degree-eleven top owner lost septimic multiplier degree")
            for code, coefficient in owners:
                require(coefficient != 0, "a literal top owner has zero coefficient")
                column = (code, multiplier)
                column_to_rows[column].add(row)
                row_to_columns[row].add(column)
        if row_index % 256 == 0:
            d10_module.check_cap(started, f"owner_rows_{row_index}")
    require(seeds <= set(column_to_rows),
            "a primitive degree-eleven seed disappeared from its top rows")

    pivots, residual = d10_module.singleton_peel(
        column_to_rows, row_to_columns
    )
    residual_seeds = residual & seeds
    first_core = d10_module.first_seed_component(
        residual, seeds, column_to_rows, row_to_columns
    )
    elapsed = time.monotonic() - started
    status = (
        "D11_TARGET_RELEVANT_RESTRICTED_CORE"
        if residual_seeds
        else "EXACT_TARGET_STANDARD_THROUGH_TOTAL_D11"
    )
    require((len(seeds), len(rows), len(column_to_rows),
             sum(map(len, row_to_columns.values())))
            == (27, 1656, 613, 3328),
            "the degree-eleven restricted owner census changed")
    require((len(pivots), len(residual), len(residual_seeds))
            == (185, 428, 0),
            "the degree-eleven restricted peel ledger changed")

    payload = {
        "format": "n8-y10-degree11-restricted-owner-peel-v1",
        "status": status,
        "scope": (
            "exact degree-eleven target-rooted seed-row restriction in the "
            "frozen normalized chart/t-last order; no degree-twelve claim"
        ),
        "target": base.TARGET.hex(),
        "d10_authority_logical_sha256": d10["logical_sha256"],
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
            "If residual_seed_columns=0, the complete seed-row restriction "
            "forces every primitive target seed coefficient in a full y11-head "
            "relation to zero. All other d11 columns lie in t*M10, so exact "
            "d10 standardness proves d11 standardness. Otherwise the frozen "
            "seed-bearing residue is unresolved and no membership inference "
            "is made."
        ),
        "time_cap_seconds": TIME_CAP_SECONDS,
        "rss_cap_bytes": RSS_CAP_BYTES,
        "elapsed_seconds_nonlogical": elapsed,
        "peak_rss_bytes_nonlogical": d10_module.peak_rss_bytes(),
    }
    logical_payload = {
        key: value for key, value in payload.items()
        if not key.endswith("_nonlogical")
    }
    encoded = json.dumps(logical_payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = sha256(encoded.encode()).hexdigest()
    require(payload["logical_sha256"] == EXPECTED_LOGICAL_SHA256,
            "the degree-eleven logical ledger changed")
    return payload


if __name__ == "__main__":
    try:
        print(json.dumps(audit(), indent=2, sort_keys=True))
    except D10_HELPERS.BoundedStop as stopped:
        print(json.dumps({
            "status": "D11_BOUNDED_STOP_NO_INFERENCE",
            "detail": stopped.args[0],
            "scope": "no degree-eleven or degree-twelve inference",
        }, indent=2, sort_keys=True))
