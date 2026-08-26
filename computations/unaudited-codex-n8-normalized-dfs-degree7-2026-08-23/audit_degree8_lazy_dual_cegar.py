#!/usr/bin/env python3
"""Lazy exact CEGAR for extending the frozen degree-seven dual to degree 8.

Start from the exact multiplier-degree-four columns on which lambda_7 has a
nonzero lower-boundary pairing.  Solve only their exposed degree-eight top
rows, choose the deterministic sparse exact solution supplied by the frozen
row order, scan every degree-eight column incident to the resulting
functional, and add only nonzero-pairing columns.  This avoids materializing
the full degree-eight top-incidence component.
"""

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
from time import monotonic


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_degree8_dual_extension.py"
CORE_PATH = HERE / "results_degree8_initial_core.json"
RESULTS = HERE / "results_degree8_lazy_dual_cegar.json"
QQ = Fraction
WALL_CAP_SECONDS = 300
ROUND_CAP = 100
COLUMN_CAP = 200_000
EXPECTED_CORE_LOGICAL_SHA256 = (
    "6ee3465a73beb17a871669ccb480e68a9f96867d95fd6eb51fba4fb75a68c9da"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_audit():
    spec = importlib.util.spec_from_file_location("degree8_audit", AUDIT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_core():
    core = json.loads(CORE_PATH.read_text())
    logical = dict(core)
    digest = logical.pop("logical_sha256")
    logical.pop("elapsed_seconds")
    replay = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    require(digest == replay == EXPECTED_CORE_LOGICAL_SHA256,
            "degree-eight initial core digest changed")
    return core


def fraction(pair):
    return QQ(pair[0], pair[1])


def serialize_functional(functional):
    return [
        [row.hex(), value.numerator, value.denominator]
        for row, value in sorted(functional.items())
    ]


def exposed_system(audit, source, lambda7, selected_columns, started):
    columns = tuple(sorted(selected_columns))
    column_index = {column: index for index, column in enumerate(columns)}
    entries = {
        column: audit.invariant_entries(source, column) for column in columns
    }
    rows = tuple(sorted({
        row
        for column_entries in entries.values()
        for row in column_entries
        if len(row) == 8
    }))
    row_index = {row: index for index, row in enumerate(rows)}
    row_vectors = [defaultdict(int) for _ in rows]
    target = {}
    nnz = 0
    for column in columns:
        cindex = column_index[column]
        boundary = audit.pairing(entries[column], lambda7)
        if boundary:
            target[cindex] = -boundary
        for row, coefficient in entries[column].items():
            if len(row) == 8:
                row_vectors[row_index[row]][cindex] += coefficient
                nnz += 1
    rank, extension, remainder, separator = audit.exact_relative_solve(
        rows, row_vectors, target, started
    )
    return {
        "columns": columns,
        "rows": rows,
        "row_vectors": row_vectors,
        "target": target,
        "rank": rank,
        "extension": extension,
        "remainder": remainder,
        "separator": separator,
        "nnz": nnz,
    }


def run():
    started = monotonic()
    audit = load_audit()
    source = audit.load_d7()
    core = load_core()
    lambda7 = {
        bytes.fromhex(encoded): QQ(numerator, denominator)
        for encoded, numerator, denominator in core["degree7_dual"]
    }
    require(len(lambda7) == 49 and lambda7.get(b"") == 1,
            "initial lambda7 support changed")
    selected = {
        (item["word_code"], bytes.fromhex(item["multiplier_hex"]))
        for item in core["violating_columns"]
    }
    require(len(selected) == core["degree8_boundary_violating_columns"] == 146,
            "initial selected-column core changed")

    rounds = []
    terminal = None
    final_functional = None
    relative_obstruction = None
    for round_index in range(ROUND_CAP):
        if monotonic() - started > WALL_CAP_SECONDS:
            terminal = "WALL_CAP"
            break
        require(len(selected) <= COLUMN_CAP,
                "lazy selected-column cap exceeded")
        system = exposed_system(audit, source, lambda7, selected, started)
        record = {
            "round": round_index,
            "selected_columns": len(selected),
            "exposed_degree8_rows": len(system["rows"]),
            "relative_nnz": system["nnz"],
            "exact_top_rank": system["rank"],
            "extension_support": len(system["extension"]),
            "exact_remainder_terms": len(system["remainder"]),
        }
        if system["remainder"]:
            terminal = "RELATIVE_INCONSISTENCY"
            target_pairing = sum(
                value * system["separator"].get(index, QQ(0))
                for index, value in system["target"].items()
            )
            require(target_pairing, "relative separator lost target pairing")
            for vector in system["row_vectors"]:
                require(not sum(QQ(value) * system["separator"].get(index, QQ(0))
                                for index, value in vector.items()),
                        "relative separator fails on an exposed top row")
            relative_obstruction = {
                "support": len(system["separator"]),
                "target_pairing": [
                    target_pairing.numerator, target_pairing.denominator
                ],
                "weights": [
                    [system["columns"][index][0],
                     system["columns"][index][1].hex(),
                     value.numerator, value.denominator]
                    for index, value in sorted(system["separator"].items())
                ],
            }
            rounds.append(record)
            break

        functional = dict(lambda7)
        functional.update(system["extension"])
        candidates = {
            column for column in source.bounded_incident_columns(
                functional, maximum_output_degree=8
            )
            if len(column[1]) == 4
        }
        violations = {}
        for column in candidates:
            value = audit.pairing(
                audit.invariant_entries(source, column), functional
            )
            if value:
                violations[column] = value
        # Selected equations must be satisfied exactly.
        require(not (set(violations) & selected),
                "exact extension fails on a selected column")
        new_columns = set(violations) - selected
        record.update({
            "incident_degree8_columns": len(candidates),
            "nonzero_pairing_columns": len(violations),
            "new_violating_columns": len(new_columns),
            "violation_pairing_histogram": [
                [[value.numerator, value.denominator], count]
                for value, count in sorted(Counter(violations.values()).items())
            ],
            "elapsed_seconds": monotonic() - started,
        })
        rounds.append(record)
        if not new_columns:
            terminal = "EXTENDED_DUAL"
            final_functional = functional
            break
        selected.update(new_columns)
    else:
        terminal = "ROUND_CAP"

    result = {
        "format": "n8-chart26-degree8-lazy-dual-cegar-v1",
        "status": terminal,
        "initial_core_logical_sha256": EXPECTED_CORE_LOGICAL_SHA256,
        "degree7_dual_sha256": core["degree7_dual_sha256"],
        "initial_selected_columns": 146,
        "round_cap": ROUND_CAP,
        "wall_cap_seconds": WALL_CAP_SECONDS,
        "column_cap": COLUMN_CAP,
        "rounds": rounds,
        "terminal_selected_columns": len(selected),
        "elapsed_seconds": monotonic() - started,
    }
    if terminal == "EXTENDED_DUAL":
        record = serialize_functional(final_functional)
        digest = sha256(json.dumps(
            record, separators=(",", ":")
        ).encode()).hexdigest()
        result.update({
            "degree8_extended_dual_support": len(final_functional),
            "degree8_extension_support": sum(len(row) == 8 for row in final_functional),
            "degree8_extended_dual_degree_histogram": dict(sorted(
                Counter(map(len, final_functional)).items()
            )),
            "degree8_extended_dual_coefficient_histogram": [
                [[value.numerator, value.denominator], count]
                for value, count in sorted(Counter(final_functional.values()).items())
            ],
            "degree8_extended_dual_sha256": digest,
            "degree8_extended_dual": record,
            "conclusion": "t^8 is not in the degree-eight homogeneous mixed ideal over Q",
            "scope_guard": "does not decide t^N for N>=9 or unrestricted t-saturation",
        })
    elif terminal == "RELATIVE_INCONSISTENCY":
        result.update({
            "relative_obstruction": relative_obstruction,
            "conclusion": "the selected lambda7 cannot be extended on the lazy exposed system",
            "scope_guard": "does not by itself prove t^8 membership; another degree-seven representative may extend",
        })
    else:
        result.update({
            "conclusion": "lazy degree-eight dual extension unresolved at a hard cap",
            "scope_guard": "no t^8 membership or nonmembership inference",
        })
    return result


def main():
    try:
        result = run()
    except TimeoutError as error:
        result = {
            "format": "n8-chart26-degree8-lazy-dual-cegar-v1",
            "status": "WALL_CAP_EXCEPTION",
            "error": str(error),
            "scope_guard": "no t^8 membership or nonmembership inference",
        }
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        "degree8 lazy dual CEGAR:", result["status"],
        "rounds=", len(result.get("rounds", ())),
        "selected=", result.get("terminal_selected_columns"),
    )
    print("elapsed_seconds=", result.get("elapsed_seconds"))


if __name__ == "__main__":
    main()
