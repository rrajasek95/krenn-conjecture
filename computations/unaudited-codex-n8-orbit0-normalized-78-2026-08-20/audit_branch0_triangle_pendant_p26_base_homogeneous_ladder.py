#!/usr/bin/env python3
"""Independently replay the bounded TP P26 homogeneous Macaulay ladder.

For degrees 9 through 14 and primes 1009,1013, this checker derives the
generator labels/degrees from the exact source interface, streams every
integer JSONL column, and verifies that the solver's displayed left dual
annihilates all columns while pairing nontrivially with t^D.  This certifies
the modular nonmembership statements only; it is not a characteristic-zero
obstruction.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
import json
from math import comb
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
EXPORTER = HERE / "export_branch0_triangle_pendant_p26_base_homogeneous_macaulay.py"
OUT = HERE / "results_branch0_triangle_pendant_p26_base_homogeneous_ladder_audit.json"
DEGREES = range(9, 15)
PRIMES = (1009, 1013)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def file_sha(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


E = load(EXPORTER, "n8_tp_p26_homogeneous_ladder_exporter")


def modular_fraction(numerator: int, denominator: int, prime: int) -> int:
    return numerator % prime * pow(denominator % prime, -1, prime) % prime


def check_one(degree: int, prime: int, mutate_target: bool) -> dict:
    interface = HERE / f"branch0_triangle_pendant_p26_base_homogeneous_d{degree}.jsonl"
    solution = HERE / f"results_toolkit_tp_p26_base_homogeneous_d{degree}.p{prime}.json"
    result = json.loads(solution.read_text())
    with interface.open() as stream:
        header = json.loads(next(stream))
        require(header["type"] == "header", "missing header")
        require(header["degree"] == degree, "degree mismatch")
        require(header["row_count"] == comb(degree + 8, 8),
                "row count mismatch")
        expected = E.generators()
        require(header["source_labels"] == [label for label, _, _ in expected],
                "source labels escaped exact derivation")
        require(header["generator_degrees"] == {
            label: generator_degree for label, _, generator_degree in expected
        }, "generator degrees escaped exact derivation")
        require(result["prime"] == prime, "solver prime mismatch")
        require(result["row_count"] == header["row_count"],
                "solver row count mismatch")
        require(result["column_count"] == header["column_count"],
                "solver column count mismatch")
        require(result["target_in_image"] is False,
                "ladder result is not a negative control")
        dual = {int(row): int(value) % prime
                for row, value in result["left_dual"]}
        column_count = 0
        for line in stream:
            column = json.loads(line)
            require(column["type"] == "column", "non-column record")
            require(column["index"] == column_count,
                    "nonsequential column provenance")
            pairing = sum(dual.get(int(row), 0) * (int(value) % prime)
                          for row, value in column["entries"]) % prime
            require(pairing == 0,
                    f"left dual fires on column {column_count} mod {prime}")
            column_count += 1
        require(column_count == header["column_count"],
                "streamed column count mismatch")
    target = list(header["target"])
    if mutate_target:
        target = [[row, 0, denominator] for row, _, denominator in target]
    target_pairing = sum(
        dual.get(int(row), 0) * modular_fraction(int(numerator),
                                                 int(denominator), prime)
        for row, numerator, denominator in target) % prime
    require(target_pairing != 0, "target mutation did not fire")
    require(target_pairing == result["left_dual_target_pairing"] % prime,
            "displayed target pairing mismatch")
    return {
        "degree": degree, "prime": prime,
        "row_count": header["row_count"],
        "column_count": header["column_count"],
        "rank": result["rank"],
        "dependent_columns": result["dependent_columns"],
        "target_pairing": target_pairing,
        "dual_support": len(dual),
        "interface_sha256": file_sha(interface),
        "solution_sha256": file_sha(solution),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate-target", action="store_true")
    args = parser.parse_args()
    records = [check_one(degree, prime, args.mutate_target)
               for degree in DEGREES for prime in PRIMES]
    result = {
        "status": "UNAUDITED exact replay of modular duals; not a Q theorem",
        "scope": (
            "TP P26=0 eight-row/base-Rabinowitsch homogeneous components "
            "through the declared degree-14 cap"
        ),
        "degrees": list(DEGREES), "primes": list(PRIMES),
        "records": records,
        "source_sha256": file_sha(Path(__file__)),
        "exporter_sha256": file_sha(EXPORTER),
        "must_fire": "--mutate-target sets the target to zero and must fail",
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("TP P26 base homogeneous ladder audit: PASS")
    print("records:", len(records))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
