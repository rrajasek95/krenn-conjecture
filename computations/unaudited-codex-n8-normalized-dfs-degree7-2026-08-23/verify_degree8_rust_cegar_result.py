#!/usr/bin/env python3
"""Independent exact replay of the terminal chart-26 degree-eight dual."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_degree8_dual_extension.py"
CORE_PATH = HERE / "results_degree8_initial_core.json"
REFERENCE_PATH = HERE / "results_degree8_lazy_dual_cegar.json"
RESULT_PATH = HERE / "results_degree8_rust_cegar.json"
CHECKPOINT_PATH = HERE / "results_degree8_rust_cegar_checkpoint.json"
REPLAY_PATH = HERE / "results_degree8_rust_cegar_replay.json"
EXPECTED_DUAL_SHA256 = (
    "561546730a738ad3e3432ae5f5b63456735514148f32b77268debbebdae09d9d"
)
COUNT_FIELDS = (
    "round", "selected_columns", "exposed_degree8_rows", "relative_nnz",
    "exact_top_rank", "extension_support", "incident_degree8_columns",
    "nonzero_pairing_columns", "new_violating_columns",
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    audit = load(AUDIT_PATH, "degree8_audit_replay")
    source = audit.load_d7()
    core = json.loads(CORE_PATH.read_text())
    reference = json.loads(REFERENCE_PATH.read_text())
    result = json.loads(RESULT_PATH.read_text())
    checkpoint = json.loads(CHECKPOINT_PATH.read_text())
    require(result["status"] == "EXTENDED_DUAL_EXACT_Q",
            "degree-eight result is not exact-terminal")
    require(result["terminal_selected_columns"] == result["exact_top_rank"] == 3097,
            "terminal selected/rank census changed")
    require(checkpoint["completed_round"] == 197
            and len(checkpoint["selected_columns"]) == 3097,
            "terminal checkpoint changed")
    for index in list(range(11)) + [47]:
        actual = {field: result["rounds"][index][field] for field in COUNT_FIELDS}
        expected = {field: reference["rounds"][index][field] for field in COUNT_FIELDS}
        require(actual == expected, f"frozen round {index} mismatch")

    record = result["exact_extended_dual"]
    digest = sha256(json.dumps(record, separators=(",", ":")).encode()).hexdigest()
    require(digest == result["exact_extended_dual_sha256"] == EXPECTED_DUAL_SHA256,
            "exact degree-eight dual digest changed")
    functional = {
        bytes.fromhex(encoded): Fraction(numerator, denominator)
        for encoded, numerator, denominator in record
    }
    require(len(functional) == 561 and functional.get(b"") == 1,
            "exact degree-eight dual support/target pairing changed")
    lambda7 = {
        bytes.fromhex(encoded): Fraction(numerator, denominator)
        for encoded, numerator, denominator in core["degree7_dual"]
    }
    require(all(functional.get(row) == value for row, value in lambda7.items()),
            "degree-eight dual no longer extends the pinned lambda7")

    candidates = source.bounded_incident_columns(
        functional, maximum_output_degree=8
    )
    pairings = {}
    for column in candidates:
        value = audit.pairing(audit.invariant_entries(source, column), functional)
        if value:
            pairings[column] = value
    require(not pairings, "exact degree-eight dual misses a literal column")
    degree_histogram = Counter(len(column[1]) for column in candidates)
    require(degree_histogram[4] == result["exact_incident_columns"] == 696,
            "new degree-eight incident-column census changed")

    # Hostile guard: changing the lexicographically first top weight by one
    # must be seen by a literal incident source column.
    mutation_row = min(row for row in functional if len(row) == 8)
    mutated = dict(functional)
    mutated[mutation_row] += 1
    crossing = None
    for column in sorted(candidates):
        value = audit.pairing(audit.invariant_entries(source, column), mutated)
        if value:
            crossing = (column, value)
            break
    require(crossing is not None, "hostile one-weight mutation was invisible")
    replay = {
        "format": "n8-chart26-degree8-rust-cegar-replay-v1",
        "status": "PASS_EXACT_Q_DUAL",
        "dual_sha256": digest,
        "dual_support": len(functional),
        "lower_degree7_support": len(lambda7),
        "degree8_extension_support": sum(len(row) == 8 for row in functional),
        "all_bounded_incident_columns": len(candidates),
        "incident_multiplier_degree_histogram": dict(sorted(degree_histogram.items())),
        "nonzero_exact_pairings": len(pairings),
        "target_pairing": [functional[b""].numerator, functional[b""].denominator],
        "hostile_mutation": {
            "row_hex": mutation_row.hex(),
            "delta": [1, 1],
            "lex_first_crossing": {
                "word_code": crossing[0][0],
                "multiplier_hex": crossing[0][1].hex(),
                "pairing": [crossing[1].numerator, crossing[1].denominator],
            },
        },
        "conclusion": "t^8 is not in the degree-eight homogeneous mixed ideal over Q",
        "scope_guard": "chart26 degree-eight homogeneous cap only; no t^9 or saturation inference",
    }
    REPLAY_PATH.write_text(json.dumps(replay, indent=2, sort_keys=True) + "\n")
    print("PASS exact degree8 dual", len(functional), len(candidates), digest)


if __name__ == "__main__":
    main()
