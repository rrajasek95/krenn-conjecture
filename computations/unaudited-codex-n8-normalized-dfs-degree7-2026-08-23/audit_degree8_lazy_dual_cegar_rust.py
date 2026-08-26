#!/usr/bin/env python3
"""Rust-accelerated lazy CEGAR for the normalized chart-26 degree-eight dual.

The literal invariant row/column provider remains the digest-pinned Python
checker.  Sparse least-column-pivot elimination and solution transport are
performed over p=1073741827 by ``degree8_modsolve``.  Frozen Python rounds
0..10 and 47 are mandatory provider/solver controls.  A modular terminal is
never promoted: it is replayed once with the exact Fraction solver and every
incident literal column is checked over Q.
"""

from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import resource
import subprocess
import sys
from time import monotonic


HERE = Path(__file__).resolve().parent
LAZY_PATH = HERE / "audit_degree8_lazy_dual_cegar.py"
REFERENCE_PATH = HERE / "results_degree8_lazy_dual_cegar.json"
CHECKPOINT_PATH = HERE / "results_degree8_rust_cegar_checkpoint.json"
RESULTS_PATH = HERE / "results_degree8_rust_cegar.json"
SOLVER = HERE / "target" / "release" / "degree8_modsolve"
PRIME = 1_073_741_827
ROUND_CAP = 1000
# The validated prefix consumed 95 seconds before its checkpointed restart;
# leave the combined discovery budget below 600 seconds.
INTERNAL_WALL = 450
VALIDATE_ROUNDS = set(range(11)) | {47}
COUNT_FIELDS = (
    "round", "selected_columns", "exposed_degree8_rows", "relative_nnz",
    "exact_top_rank", "extension_support", "incident_degree8_columns",
    "nonzero_pairing_columns", "new_violating_columns",
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def residue(value):
    if isinstance(value, Fraction):
        return value.numerator * pow(value.denominator, PRIME - 2, PRIME) % PRIME
    return value % PRIME


def signed(value):
    return value if value <= PRIME // 2 else value - PRIME


def column_record(column):
    return [column[0], column[1].hex()]


def run_modsolve(columns, rows, row_vectors, target):
    lines = [f"KRENN_D8_MODSOLVE_V1 {PRIME} {len(columns)} {len(rows)}"]
    terms = sorted((index, value % PRIME) for index, value in target.items() if value % PRIME)
    lines.append("TARGET " + str(len(terms)) + "".join(f" {index} {value}" for index, value in terms))
    for row in rows:
        vector = sorted((index, value % PRIME) for index, value in row_vectors[row].items() if value % PRIME)
        lines.append("ROW " + row.hex() + " " + str(len(vector))
                     + "".join(f" {index} {value}" for index, value in vector))
    completed = subprocess.run(
        [str(SOLVER)], input=("\n".join(lines) + "\n").encode(),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
    )
    output = completed.stdout.decode().splitlines()
    header = output[0].split()
    require(len(header) == 5 and header[0] == "KRENN_D8_MODSOLUTION_V1"
            and int(header[1]) == PRIME, "bad Rust solution header")
    rank, remainder, support = map(int, header[2:])
    solution = {}
    for line in output[1:]:
        kind, encoded, coefficient = line.split()
        require(kind == "SOLUTION", "bad Rust solution record")
        solution[bytes.fromhex(encoded)] = int(coefficient)
    require(len(solution) == support, "Rust solution support mismatch")
    return rank, remainder, solution


def main():
    started = monotonic()
    try:
        resource.setrlimit(resource.RLIMIT_AS, (12 * 1024 ** 3, 12 * 1024 ** 3))
        memory_cap = "RLIMIT_AS_12GB"
    except (ValueError, OSError):
        memory_cap = "RLIMIT_AS_UNAVAILABLE"
    lazy = load_module(LAZY_PATH, "degree8_lazy_frozen")
    audit = lazy.load_audit()
    source = audit.load_d7()
    core = lazy.load_core()
    reference = json.loads(REFERENCE_PATH.read_text())
    require(reference["status"] == "WALL_CAP" and len(reference["rounds"]) == 48,
            "frozen 48-round reference changed")
    lambda7_exact = {
        bytes.fromhex(encoded): Fraction(numerator, denominator)
        for encoded, numerator, denominator in core["degree7_dual"]
    }
    lambda7 = {row: residue(value) for row, value in lambda7_exact.items()}
    selected = {
        (item["word_code"], bytes.fromhex(item["multiplier_hex"]))
        for item in core["violating_columns"]
    }
    require(len(selected) == 146, "initial selected core changed")
    prior_rounds = []
    start_round = 0
    resumed_from = None
    if "--resume" in sys.argv[1:]:
        checkpoint = json.loads(CHECKPOINT_PATH.read_text())
        require(checkpoint["format"] == "n8-chart26-degree8-rust-cegar-checkpoint-v1"
                and checkpoint["prime"] == PRIME, "bad resume checkpoint")
        selected = {
            (word, bytes.fromhex(multiplier))
            for word, multiplier in checkpoint["selected_columns"]
        }
        prior_rounds = checkpoint["rounds"]
        start_round = checkpoint["completed_round"] + 1
        resumed_from = checkpoint["completed_round"]
        require(len(prior_rounds) == start_round, "checkpoint round ledger mismatch")

    @lru_cache(maxsize=None)
    def entries(column):
        return tuple(sorted(audit.invariant_entries(source, column).items()))

    def pairing(column, functional):
        return sum(coefficient * functional.get(row, 0)
                   for row, coefficient in entries(column)) % PRIME

    rounds = list(prior_rounds)
    terminal = None
    terminal_functional = None
    for round_index in range(start_round, ROUND_CAP):
        require(monotonic() - started < INTERNAL_WALL, "internal 570-second wall cap")
        columns = tuple(sorted(selected))
        column_index = {column: index for index, column in enumerate(columns)}
        row_vectors = defaultdict(dict)
        target = {}
        nnz = 0
        for column in columns:
            cindex = column_index[column]
            boundary = pairing(column, lambda7)
            if boundary:
                target[cindex] = (-boundary) % PRIME
            for row, coefficient in entries(column):
                if len(row) == 8:
                    row_vectors[row][cindex] = (
                        row_vectors[row].get(cindex, 0) + coefficient
                    ) % PRIME
                    if row_vectors[row][cindex] == 0:
                        del row_vectors[row][cindex]
                    nnz += 1
        rows = tuple(sorted(row_vectors))
        rank, remainder, extension = run_modsolve(
            columns, rows, row_vectors, target
        )
        require(not remainder, "modular relative inconsistency")
        functional = dict(lambda7)
        functional.update(extension)
        candidates = {
            column for column in source.bounded_incident_columns(
                functional, maximum_output_degree=8
            ) if len(column[1]) == 4
        }
        violations = {
            column: pairing(column, functional)
            for column in candidates if pairing(column, functional)
        }
        require(not (set(violations) & selected),
                "modular extension fails a selected column")
        new_columns = set(violations) - selected
        record = {
            "round": round_index,
            "selected_columns": len(selected),
            "exposed_degree8_rows": len(rows),
            "relative_nnz": nnz,
            "exact_top_rank": rank,
            "extension_support": len(extension),
            "incident_degree8_columns": len(candidates),
            "nonzero_pairing_columns": len(violations),
            "new_violating_columns": len(new_columns),
            "violation_residue_histogram": [
                [signed(value), count]
                for value, count in sorted(Counter(violations.values()).items())
            ],
            "elapsed_seconds": monotonic() - started,
        }
        if round_index in VALIDATE_ROUNDS:
            expected = reference["rounds"][round_index]
            actual_counts = {field: record[field] for field in COUNT_FIELDS}
            expected_counts = {field: expected[field] for field in COUNT_FIELDS}
            require(actual_counts == expected_counts,
                    f"frozen round {round_index} count mismatch: "
                    f"{actual_counts} != {expected_counts}")
            record["frozen_count_replay"] = "PASS"
        rounds.append(record)
        selected.update(new_columns)
        checkpoint = {
            "format": "n8-chart26-degree8-rust-cegar-checkpoint-v1",
            "prime": PRIME,
            "completed_round": round_index,
            "selected_columns": [column_record(column) for column in sorted(selected)],
            "rounds": rounds,
        }
        CHECKPOINT_PATH.write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + "\n")
        print(
            "round", round_index, "selected", record["selected_columns"],
            "rows", len(rows), "rank", rank, "extension", len(extension),
            "candidates", len(candidates), "new", len(new_columns),
            "elapsed", f"{record['elapsed_seconds']:.3f}", flush=True,
        )
        if not new_columns:
            terminal = "MODULAR_EXTENDED_DUAL"
            terminal_functional = functional
            break
    if terminal is None:
        terminal = "ROUND_CAP"

    result = {
        "format": "n8-chart26-degree8-rust-cegar-v1",
        "status": terminal,
        "prime": PRIME,
        "memory_cap": memory_cap,
        "initial_core_logical_sha256": lazy.EXPECTED_CORE_LOGICAL_SHA256,
        "degree7_dual_sha256": core["degree7_dual_sha256"],
        "validated_reference_rounds": sorted(VALIDATE_ROUNDS),
        "rounds": rounds,
        "terminal_selected_columns": len(selected),
        "resumed_from_round": resumed_from,
        "elapsed_seconds": monotonic() - started,
        "scope_guard": "modular discovery alone proves no characteristic-zero statement",
    }

    if terminal == "MODULAR_EXTENDED_DUAL":
        # One exact replay at the terminal selected packet.  This recreates
        # the same source matrix over Q and verifies every incident column.
        columns = tuple(sorted(selected))
        column_index = {column: index for index, column in enumerate(columns)}
        exact_rows = defaultdict(lambda: defaultdict(int))
        exact_target = {}
        for column in columns:
            cindex = column_index[column]
            boundary = sum(Fraction(coefficient) * lambda7_exact.get(row, Fraction(0))
                           for row, coefficient in entries(column))
            if boundary:
                exact_target[cindex] = -boundary
            for row, coefficient in entries(column):
                if len(row) == 8:
                    exact_rows[row][cindex] += coefficient
        ordered_rows = tuple(sorted(exact_rows))
        exact_rank, exact_extension, exact_remainder, _separator = audit.exact_relative_solve(
            ordered_rows, [exact_rows[row] for row in ordered_rows],
            exact_target, monotonic(),
        )
        require(not exact_remainder and exact_rank == len(columns),
                "terminal modular extension failed exact replay")
        exact_functional = dict(lambda7_exact)
        exact_functional.update(exact_extension)
        exact_candidates = {
            column for column in source.bounded_incident_columns(
                exact_functional, maximum_output_degree=8
            ) if len(column[1]) == 4
        }
        exact_violations = {
            column: sum(Fraction(coefficient) * exact_functional.get(row, Fraction(0))
                        for row, coefficient in entries(column))
            for column in exact_candidates
        }
        exact_violations = {column: value for column, value in exact_violations.items() if value}
        require(not exact_violations, "exact terminal dual misses a literal incident column")
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
            "conclusion": "t^8 is not in the degree-eight homogeneous mixed ideal over Q",
            "scope_guard": "does not decide t^N for N>=9 or unrestricted t-saturation",
        })
    RESULTS_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("terminal", result["status"], "selected", len(selected),
          "elapsed", f"{monotonic() - started:.3f}")


if __name__ == "__main__":
    main()
