#!/usr/bin/env python3
"""Independent exact-Q replay of the terminal Rust-discovered degree-8 dual.

The discovery ledger is treated only as a certificate container.  This
checker reloads the digest-pinned literal normalized source provider,
reconstructs the rational functional, exhausts every incident column with
multiplier degree at most four, and performs a hostile one-weight mutation.
It does not rerun the modular CEGAR discovery.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_degree8_dual_extension.py"
CERTIFICATE_PATH = HERE / "results_degree8_rust_cegar.json"
RESULTS_PATH = HERE / "results_degree8_rust_cegar_exact_replay.json"
EXPECTED_CERTIFICATE_FILE_SHA256 = (
    "5d39aa3d8d6ae83a8b2b357e148232fb1046e069c79bed5ff8e5ff970b6d8485"
)
EXPECTED_DUAL_SHA256 = (
    "561546730a738ad3e3432ae5f5b63456735514148f32b77268debbebdae09d9d"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def column_record(column):
    return [column[0], column[1].hex()]


def main():
    certificate_bytes = CERTIFICATE_PATH.read_bytes()
    certificate_file_sha = sha256(certificate_bytes).hexdigest()
    require(certificate_file_sha == EXPECTED_CERTIFICATE_FILE_SHA256,
            "terminal Rust certificate file changed")
    certificate = json.loads(certificate_bytes)
    require(certificate["status"] == "EXTENDED_DUAL_EXACT_Q",
            "terminal certificate is not exact-Q")

    audit = load_module(AUDIT_PATH, "degree8_exact_replay_provider")
    source = audit.load_d7()
    record = certificate["exact_extended_dual"]
    digest = sha256(json.dumps(
        record, separators=(",", ":")
    ).encode()).hexdigest()
    require(digest == certificate["exact_extended_dual_sha256"]
            == EXPECTED_DUAL_SHA256, "exact dual digest changed")
    functional = {
        bytes.fromhex(encoded): Fraction(numerator, denominator)
        for encoded, numerator, denominator in record
    }
    require(len(functional) == len(record) == 561,
            "exact dual support changed")
    require(functional.get(b"") == 1,
            "the degree-eight target pairing is not one")
    degree_histogram = Counter(map(len, functional))
    require(degree_histogram == Counter({
        0: 1, 4: 1, 5: 3, 6: 5, 7: 39, 8: 512,
    }),
            "exact dual row-degree profile changed")

    columns = sorted(source.bounded_incident_columns(
        functional, maximum_output_degree=8
    ))
    multiplier_histogram = Counter(len(multiplier) for _word, multiplier in columns)
    require(multiplier_histogram == Counter({0: 1, 1: 3, 2: 6, 3: 46, 4: 696}),
            "bounded incident-column census changed")
    pairings = []
    for column in columns:
        value = audit.pairing(audit.invariant_entries(source, column), functional)
        if value:
            pairings.append((column, value))
    require(not pairings, "terminal exact dual misses a literal incident column")

    # Hostile control: increment the lex-first nonconstant weight.  The
    # exhaustive replay must catch the now-nonzero literal column.
    mutated_row = min(row for row in functional if row)
    mutated = dict(functional)
    mutated[mutated_row] += 1
    mutation_violations = []
    for column in columns:
        value = audit.pairing(audit.invariant_entries(source, column), mutated)
        if value:
            mutation_violations.append((column, value))
    require(len(mutation_violations) == 1,
            "hostile one-weight mutation was not uniquely detected")
    witness_column, witness_pairing = mutation_violations[0]
    require(mutated_row.hex() == "0103093349bfc6f6"
            and functional[mutated_row] == 2
            and column_record(witness_column) == [56, "02061ec0"]
            and witness_pairing == 1,
            "hostile mutation witness changed")

    result = {
        "format": "n8-chart26-degree8-rust-cegar-exact-replay-v1",
        "status": "PASS independent exact-Q replay",
        "certificate_file_sha256": certificate_file_sha,
        "literal_source_checker_sha256": audit.EXPECTED_D7_SHA256,
        "degree7_dual_sha256": audit.EXPECTED_D7_DUAL_SHA256,
        "exact_extended_dual_sha256": digest,
        "exact_extended_dual_support": len(functional),
        "dual_row_degree_histogram": dict(sorted(degree_histogram.items())),
        "target_t8_pairing": [1, 1],
        "bounded_incident_columns": len(columns),
        "incident_multiplier_degree_histogram": dict(sorted(
            multiplier_histogram.items()
        )),
        "nonzero_literal_pairings": 0,
        "hostile_mutation": {
            "row_hex": mutated_row.hex(),
            "old_weight": [2, 1],
            "new_weight": [3, 1],
            "detected_nonzero_columns": 1,
            "witness_column": column_record(witness_column),
            "witness_pairing": [1, 1],
        },
        "conclusion": (
            "the displayed exact functional separates t^8 from the "
            "degree-eight homogeneous mixed ideal over Q"
        ),
        "scope_guard": (
            "does not decide t^N for N>=9 or unrestricted t-saturation"
        ),
    }
    RESULTS_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])
    print(
        "dual/incident/nonzero="
        f"{len(functional)}/{len(columns)}/0; hostile=1"
    )


if __name__ == "__main__":
    main()
