#!/usr/bin/env python3
"""Final bounded degree-12 restricted owner/seed peel for one monomial.

The target monomial is y10*t2.  Only primitive columns with t-free octic
multipliers are new modulo t*M11.  This checker decides standardness of that
single monomial in total degree 12; it does not reduce the 140,185,881-term
fixed C10 residual polynomial and does not test t-saturation or degree 13.
"""

from collections import defaultdict
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D11_PATH = (
    ROOT / "computations/unaudited-codex-n8-y10-degree11-seeds-2026-08-23"
    / "audit_degree11_restricted.py"
)
FULL_C10 = (
    ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23"
    / "results_full_y10_aggregate.json"
)
TIME_CAP_SECONDS = 300.0
RSS_CAP_BYTES = 12 * 1024 ** 3
EXPECTED_LOGICAL_SHA256 = (
    "8030714e1f1edaa844664c893bb28f6574e32cca7d3e88a3e1379cfc25d541bd"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


D11_HELPERS = load(D11_PATH, "n8_d12_d11_helpers")


def audit():
    started = time.monotonic()
    d11_module = D11_HELPERS
    d10_module = d11_module.D10_HELPERS
    d11 = d11_module.audit()
    require(d11["status"] == "EXACT_TARGET_STANDARD_THROUGH_TOTAL_D11"
            and d11["logical_sha256"]
            == "98a5254238a87e79d7861640ee8b9cb4c88f68cdee57ca8251f9fe714df5e171",
            "the frozen exact degree-eleven authority changed")
    d10_module.check_cap(started, "degree11_authority")

    full_c10 = json.loads(FULL_C10.read_text())
    require(full_c10["logical_sha256"]
            == "3dd16ca8793cb5b435700fb90773dd1c4dae5a4b9166034feaef944740ffa75d",
            "the fixed C10 residual provenance changed")
    require(full_c10["PM4_incidence"]["lex_dead_row"]
            == "0111202020494f4f50f8"
            and full_c10["PM4_incidence"]["lex_dead_coefficient"] == -4,
            "the selected lex-dead term changed")

    base = d10_module.load(d10_module.D8_BASE_PATH, "n8_d12_base")
    source = base.load_source()
    originals, _leads = source.FIRST.original_basis()
    term_sources = base.make_term_sources(originals)
    coordinates = source.D5.COORDINATES

    slice_data = {
        y_degree: base.record_slice(
            term_sources, coordinates, 12, y_degree
        )
        for y_degree in (10, 11, 12)
    }
    slices = [slice_data[y_degree][0] for y_degree in sorted(slice_data)]
    require(slices[0]["target_divisors"] == 1,
            "degree twelve lost its unique homogeneous target divisor")
    require(all(record["target_divisors"] == 0 for record in slices[1:]),
            "an impossible y11/y12 target divisor appeared")
    seeds = {
        key
        for _y_degree, (_record, columns, _witnesses) in slice_data.items()
        for values in columns.values()
        for key in values
        if len(key[1]) == 8
    }
    d10_module.check_cap(started, "primitive_seed_census")

    top_sources = defaultdict(list)
    for code, polynomial in originals.items():
        for term, coefficient in polynomial.items():
            if len(term) == 4:
                top_sources[term].append((code, coefficient))

    rows = set()
    for code, multiplier in sorted(seeds):
        for term, coefficient in originals[code].items():
            if len(term) == 4:
                require(coefficient != 0, "a seed top term has zero coefficient")
                rows.add(bytes(sorted(term + multiplier)))

    column_to_rows = defaultdict(set)
    row_to_columns = defaultdict(set)
    for row_index, row in enumerate(sorted(rows), 1):
        for term in base.divisors(row, 4):
            owners = top_sources.get(term)
            if not owners:
                continue
            multiplier = base.quotient(row, term)
            require(len(multiplier) == 8,
                    "a degree-twelve top owner lost octic multiplier degree")
            for code, coefficient in owners:
                require(coefficient != 0, "a literal top owner has zero coefficient")
                column = (code, multiplier)
                column_to_rows[column].add(row)
                row_to_columns[row].add(column)
        if row_index % 128 == 0:
            d10_module.check_cap(started, f"owner_rows_{row_index}")
    require(seeds <= set(column_to_rows),
            "a primitive degree-twelve seed disappeared from its top rows")

    pivots, residual = d10_module.singleton_peel(
        column_to_rows, row_to_columns
    )
    residual_seeds = residual & seeds
    first_core = d10_module.first_seed_component(
        residual, seeds, column_to_rows, row_to_columns
    )
    elapsed = time.monotonic() - started
    status = (
        "D12_TARGET_RELEVANT_RESTRICTED_CORE"
        if residual_seeds
        else "EXACT_MONOMIAL_NONMEMBERSHIP_AT_TOTAL_D12"
    )
    require((len(seeds), len(rows), len(column_to_rows),
             sum(map(len, row_to_columns.values())))
            == (4, 244, 138, 579),
            "the degree-twelve restricted owner census changed")
    require((len(pivots), len(residual), len(residual_seeds))
            == (30, 108, 0),
            "the degree-twelve restricted peel ledger changed")

    payload = {
        "format": "n8-y10-degree12-restricted-owner-peel-v1",
        "status": status,
        "scope": (
            "exact total-degree-twelve standardness/nonmembership of the one "
            "monomial y10*t2 in the frozen normalized chart/t-last order; no "
            "full-C10 reduction, t-saturation, or degree-thirteen claim"
        ),
        "target": base.TARGET.hex(),
        "target_homogenizing_t_exponent": 2,
        "d11_authority_logical_sha256": d11["logical_sha256"],
        "fixed_c10_aggregate_logical_sha256": full_c10["logical_sha256"],
        "fixed_c10_target_coefficient": -4,
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
        "membership_scope_verdict": (
            "If residual_seed_columns=0, the monomial y10*t2 itself is not in "
            "the homogeneous normalized mixed ideal: it is standard through "
            "all possible generator degrees up to its total degree 12. This "
            "does NOT decide membership of the fixed 140,185,881-term C10 "
            "residual polynomial. The aggregate certifies only that this "
            "monomial occurs there with coefficient -4 and is lex-first among "
            "the minimum-PM4-dead rows; it does not identify its quotient "
            "normal-form coefficient after reducing all other C10 rows."
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
            "the degree-twelve logical ledger changed")
    return payload


if __name__ == "__main__":
    try:
        print(json.dumps(audit(), indent=2, sort_keys=True))
    except D11_HELPERS.D10_HELPERS.BoundedStop as stopped:
        print(json.dumps({
            "status": "D12_BOUNDED_STOP_NO_INFERENCE",
            "detail": stopped.args[0],
            "scope": (
                "no degree-twelve monomial membership, full-C10 membership, "
                "t-saturation, or degree-thirteen inference"
            ),
        }, indent=2, sort_keys=True))
