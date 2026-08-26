#!/usr/bin/env python3
"""One bounded lazy extension step from the exact chart-26 lambda8 to degree 9."""

from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import resource
from time import monotonic


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_degree8_dual_extension.py"
RUST_DRIVER_PATH = HERE / "audit_degree8_lazy_dual_cegar_rust.py"
D8_PATH = HERE / "results_degree8_rust_cegar.json"
INITIAL_PATH = HERE / "results_degree9_initial_census.json"
CHECKPOINT_PATH = HERE / "results_degree9_rust_cegar_checkpoint.json"
RESULTS_PATH = HERE / "results_degree9_rust_cegar.json"
EXPECTED_D8_DUAL = "561546730a738ad3e3432ae5f5b63456735514148f32b77268debbebdae09d9d"
EXPECTED_INITIAL = "2c36f6054bacd4654236037849a2dc841b96b6ecb2161f3ee0322734c7ce94b1"
PRIME = 1_073_741_827
ROUND_CAP = 500
INTERNAL_WALL = 570


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    started = monotonic()
    try:
        resource.setrlimit(resource.RLIMIT_AS, (12 * 1024 ** 3, 12 * 1024 ** 3))
        memory_cap = "RLIMIT_AS_12GB"
    except (ValueError, OSError):
        memory_cap = "RLIMIT_AS_UNAVAILABLE"
    audit = load(AUDIT_PATH, "degree9_audit")
    rust = load(RUST_DRIVER_PATH, "degree9_rust_solver")
    source = audit.load_d7()
    d8 = json.loads(D8_PATH.read_text())
    initial = json.loads(INITIAL_PATH.read_text())
    require(d8["status"] == "EXTENDED_DUAL_EXACT_Q"
            and d8["exact_extended_dual_sha256"] == EXPECTED_D8_DUAL,
            "pinned lambda8 changed")
    require(initial["logical_sha256"] == EXPECTED_INITIAL,
            "degree9 initial census changed")
    lambda8_exact = {
        bytes.fromhex(encoded): Fraction(numerator, denominator)
        for encoded, numerator, denominator in d8["exact_extended_dual"]
    }
    require(len(lambda8_exact) == 561 and lambda8_exact.get(b"") == 1,
            "lambda8 support/target changed")
    lambda8 = {row: rust.residue(value) for row, value in lambda8_exact.items()}
    selected = {
        (item["word_code"], bytes.fromhex(item["multiplier_hex"]))
        for item in initial["violating_columns"]
    }
    require(len(selected) == initial["degree9_boundary_violations"] == 2308,
            "degree9 initial selected packet changed")

    @lru_cache(maxsize=None)
    def entries(column):
        return tuple(sorted(audit.invariant_entries(source, column).items()))

    def pairing(column, functional):
        return sum(coefficient * functional.get(row, 0)
                   for row, coefficient in entries(column)) % PRIME

    rounds = []
    terminal = None
    terminal_system = None
    terminal_functional = None
    for round_index in range(ROUND_CAP):
        if monotonic() - started >= INTERNAL_WALL:
            terminal = "WALL_CAP"
            break
        columns = tuple(sorted(selected))
        column_index = {column: index for index, column in enumerate(columns)}
        row_vectors = defaultdict(dict)
        target = {}
        nnz = 0
        for column in columns:
            cindex = column_index[column]
            boundary = pairing(column, lambda8)
            if boundary:
                target[cindex] = (-boundary) % PRIME
            for row, coefficient in entries(column):
                if len(row) == 9:
                    value = (row_vectors[row].get(cindex, 0) + coefficient) % PRIME
                    if value:
                        row_vectors[row][cindex] = value
                    else:
                        row_vectors[row].pop(cindex, None)
                    nnz += 1
        rows = tuple(sorted(row_vectors))
        rank, remainder, extension = rust.run_modsolve(
            columns, rows, row_vectors, target
        )
        record = {
            "round": round_index,
            "selected_columns": len(selected),
            "exposed_degree9_rows": len(rows),
            "relative_nnz": nnz,
            "modular_top_rank": rank,
            "modular_remainder_terms": remainder,
            "extension_support": len(extension),
            "elapsed_seconds": monotonic() - started,
        }
        if remainder:
            rounds.append(record)
            terminal = "MODULAR_RELATIVE_INCONSISTENCY"
            terminal_system = (columns, rows, row_vectors)
            break
        functional = dict(lambda8)
        functional.update(extension)
        candidates = {
            column for column in source.bounded_incident_columns(
                functional, maximum_output_degree=9
            ) if len(column[1]) == 5
        }
        violations = {
            column: pairing(column, functional)
            for column in candidates if pairing(column, functional)
        }
        require(not (set(violations) & selected),
                "degree9 modular extension fails a selected column")
        new_columns = set(violations) - selected
        record.update({
            "incident_degree9_columns": len(candidates),
            "nonzero_pairing_columns": len(violations),
            "new_violating_columns": len(new_columns),
            "violation_residue_histogram": [
                [rust.signed(value), count]
                for value, count in sorted(Counter(violations.values()).items())
            ],
        })
        rounds.append(record)
        selected.update(new_columns)
        checkpoint = {
            "format": "n8-chart26-degree9-rust-cegar-checkpoint-v1",
            "prime": PRIME,
            "completed_round": round_index,
            "selected_columns": [rust.column_record(column) for column in sorted(selected)],
            "rounds": rounds,
        }
        CHECKPOINT_PATH.write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + "\n")
        print(
            "degree9 round", round_index, "selected", record["selected_columns"],
            "rows", len(rows), "rank", rank, "extension", len(extension),
            "candidates", len(candidates), "new", len(new_columns),
            "elapsed", f"{record['elapsed_seconds']:.3f}", flush=True,
        )
        if not new_columns:
            terminal = "MODULAR_EXTENDED_DUAL"
            terminal_system = (columns, rows, row_vectors)
            terminal_functional = functional
            break
    if terminal is None:
        terminal = "ROUND_CAP"

    result = {
        "format": "n8-chart26-degree9-rust-cegar-v1",
        "status": terminal,
        "prime": PRIME,
        "memory_cap": memory_cap,
        "lambda8_sha256": EXPECTED_D8_DUAL,
        "initial_census_logical_sha256": EXPECTED_INITIAL,
        "initial_selected_columns": 2308,
        "round_cap": ROUND_CAP,
        "wall_cap_seconds": INTERNAL_WALL,
        "rounds": rounds,
        "terminal_selected_columns": len(selected),
        "elapsed_seconds": monotonic() - started,
        "scope_guard": "selected-lambda modular discovery only until exact terminal replay",
    }

    if terminal in {"MODULAR_EXTENDED_DUAL", "MODULAR_RELATIVE_INCONSISTENCY"}:
        columns, rows, row_vectors = terminal_system
        exact_target = {}
        exact_rows = defaultdict(lambda: defaultdict(int))
        column_index = {column: index for index, column in enumerate(columns)}
        for column in columns:
            cindex = column_index[column]
            boundary = sum(Fraction(coefficient) * lambda8_exact.get(row, Fraction(0))
                           for row, coefficient in entries(column))
            if boundary:
                exact_target[cindex] = -boundary
            for row, coefficient in entries(column):
                if len(row) == 9:
                    exact_rows[row][cindex] += coefficient
        ordered_rows = tuple(sorted(exact_rows))
        exact_rank, exact_extension, exact_remainder, separator = audit.exact_relative_solve(
            ordered_rows, [exact_rows[row] for row in ordered_rows],
            exact_target, monotonic(),
        )
        if exact_remainder:
            target_pairing = sum(
                value * separator.get(index, Fraction(0))
                for index, value in exact_target.items()
            )
            require(target_pairing, "degree9 exact separator lost boundary target")
            result.update({
                "status": "SELECTED_LAMBDA8_BOCKSTEIN_EXACT_Q",
                "exact_top_rank": exact_rank,
                "exact_remainder_terms": len(exact_remainder),
                "exact_relative_separator_support": len(separator),
                "exact_relative_separator_target_pairing": [
                    target_pairing.numerator, target_pairing.denominator
                ],
                "exact_relative_separator": [
                    [columns[index][0], columns[index][1].hex(),
                     value.numerator, value.denominator]
                    for index, value in sorted(separator.items())
                ],
                "conclusion": "the selected lambda8 does not extend to degree nine",
                "scope_guard": "Bockstein for this lambda8 only; not degree9 membership or nonmembership",
            })
        else:
            require(terminal == "MODULAR_EXTENDED_DUAL"
                    and exact_rank == len(columns),
                    "degree9 exact/modular terminal disagreement")
            exact_functional = dict(lambda8_exact)
            exact_functional.update(exact_extension)
            exact_candidates = {
                column for column in source.bounded_incident_columns(
                    exact_functional, maximum_output_degree=9
                ) if len(column[1]) == 5
            }
            exact_violations = {}
            for column in exact_candidates:
                value = sum(Fraction(coefficient) * exact_functional.get(row, Fraction(0))
                            for row, coefficient in entries(column))
                if value:
                    exact_violations[column] = value
            require(not exact_violations,
                    "degree9 exact terminal dual misses a literal incident column")
            dual_record = [
                [row.hex(), value.numerator, value.denominator]
                for row, value in sorted(exact_functional.items())
            ]
            digest = sha256(json.dumps(dual_record, separators=(",", ":")).encode()).hexdigest()
            result.update({
                "status": "EXTENDED_DUAL_EXACT_Q",
                "exact_top_rank": exact_rank,
                "exact_extended_dual_support": len(exact_functional),
                "exact_extension_support": len(exact_extension),
                "exact_incident_columns": len(exact_candidates),
                "exact_extended_dual_sha256": digest,
                "exact_extended_dual": dual_record,
                "conclusion": "t^9 is not in the degree-nine homogeneous mixed ideal over Q",
                "scope_guard": "chart26 degree-nine homogeneous cap only; no degree>=10 or saturation inference",
            })
    RESULTS_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("degree9 terminal", result["status"], "selected", len(selected),
          "elapsed", f"{monotonic() - started:.3f}")


if __name__ == "__main__":
    main()
