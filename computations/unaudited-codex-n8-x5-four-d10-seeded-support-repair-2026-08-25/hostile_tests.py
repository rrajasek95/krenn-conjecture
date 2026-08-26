#!/usr/bin/env python3
"""Hostile fail-closed tests for the independent D10 certificate validator."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent

def load_validator():
    spec = importlib.util.spec_from_file_location("d10_validator", HERE / "validate.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module

def rejected(label, function):
    try:
        function()
    except (AssertionError, KeyError, ValueError):
        return {"test": label, "rejected": True}
    raise AssertionError(f"hostile mutation accepted: {label}")

def atomic(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)

def main():
    validator = load_validator()
    certificate = HERE / "exact_lift_direct/integer_dual.tsv"
    original = certificate.read_text().splitlines()
    records = []
    with tempfile.TemporaryDirectory(prefix="krenn-d10-hostile-") as raw:
        directory = Path(raw)
        def mutation(name, lines):
            path = directory / name
            path.write_text("\n".join(lines) + "\n")
            return path

        bad = list(original)
        bad[0] = bad[0].replace("D10", "D11")
        path = mutation("bad_schema.tsv", bad)
        records.append(rejected("wrong_schema", lambda: validator.dual(path, 10)))

        bad = list(original)
        fields = bad[1].split("\t")
        fields[1] = ",".join(reversed(fields[1].split(",")))
        bad[1] = "\t".join(fields)
        path = mutation("unsorted_row.tsv", bad)
        records.append(rejected("unsorted_row", lambda: validator.dual(path, 10)))

        bad = list(original)
        bad[2] = bad[1]
        path = mutation("duplicate_row.tsv", bad)
        records.append(rejected("duplicate_row", lambda: validator.dual(path, 10)))

        bad = list(original)
        target = "361,361,361,361,361,361,361,361,361,361"
        index = next(i for i, line in enumerate(bad) if f"\t{target}\t" in line)
        fields = bad[index].split("\t")
        fields[2] = "0"
        bad[index] = "\t".join(fields)
        path = mutation("zero_target.tsv", bad)
        records.append(rejected("zero_target", lambda: validator.dual(path, 10)))

        integer = validator.dual(certificate, 10)
        excessive = dict(integer)
        excessive[next(row for row in excessive if row != (361,) * 10)] = 3
        records.append(rejected("coefficient_magnitude_three", lambda: validator.validate_integer(excessive)))

        modular = validator.dual(HERE / "p1073741827_direct/dual.tsv", 10)
        corrupt = dict(modular)
        row = next(row for row in corrupt if row != (361,) * 10)
        corrupt[row] = (corrupt[row] + 1) % 1073741827
        records.append(rejected("wrong_modular_reduction", lambda: validator.check_reduction(integer, corrupt, 1073741827)))

        records.append(rejected("wrong_provider_hash", lambda: validator.provider(
            validator.REPO / "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/provider_direct.ms",
            "0" * 64)))

    optimized = subprocess.run([sys.executable, "-O", str(HERE / "validate.py")], cwd=HERE, text=True, capture_output=True, check=False)
    assert optimized.returncode != 0 and "assertions required" in optimized.stderr
    records.append({"test": "optimized_assertions_disabled", "rejected": True, "returncode": optimized.returncode})
    result = {"schema": "KRENN_X5_FOUR_D10_VALIDATOR_HOSTILE_TESTS_V1", "status": "PASS_ALL_HOSTILES_REJECTED",
              "tests": records, "test_count": len(records), "degree_eleven_launched": False}
    atomic(HERE / "results_hostile_tests.json", result)
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
