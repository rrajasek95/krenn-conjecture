#!/usr/bin/env python3
"""Hostile tests for the full hidden-decorated structural/literal referee."""
from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
VALIDATOR = HERE / "validate_hidden_decorated_complete.py"
LITERAL = HERE / "referee_k24_charge_literals"
RESULT = ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_hidden_decorated_complete.json"
SAMPLES = Path(str(RESULT) + ".samples.tsv")
OUTPUT = HERE / "results_hidden_decorated_complete_referee_hostile_selftest.json"


def run(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def structural(prefix: list[str], result: Path, samples: Path, output: Path) -> subprocess.CompletedProcess:
    return run(prefix + [str(VALIDATOR), "--result", str(result), "--samples", str(samples), "--output", str(output)])


def main() -> None:
    cases = []
    with tempfile.TemporaryDirectory(prefix="k24-hidden-decorated-referee-") as td:
        tmp = Path(td)
        for label, prefix in [("std", [sys.executable]), ("opt", [sys.executable, "-O"]), ("isolated", [sys.executable, "-I", "-S"])]:
            q = structural(prefix, RESULT, SAMPLES, tmp / f"base-{label}.json")
            cases.append({"case": f"baseline_{label}", "expected": "PASS", "observed": q.returncode})
            if q.returncode != 0:
                raise RuntimeError(q.stderr)
        base = json.loads(RESULT.read_text())
        mutations = {
            "wrong_U": lambda value: value.__setitem__("scale_U", "1"),
            "wrong_id": lambda value: value["covered_lineage_ids"].__setitem__(0, "D99:bad|R:4"),
            "wrong_interval": lambda value: value.__setitem__("input_interval", [0, 1]),
            "wrong_charge": lambda value: value["sink"].__setitem__("full_charge_scaled_U", "0"),
            "wrong_terminal_count": lambda value: value["sink"].__setitem__("terminal_K24_occurrences", 0),
            "wrong_histogram": lambda value: value["sink"]["m2_m3_histogram"].__setitem__("3_1", 0),
            "wrong_cache": lambda value: value["sink"].__setitem__("cache_hits", 0),
            "wrong_stabilizers": lambda value: value["stabilizer_histogram"].__setitem__("1", 0),
        }
        for label, mutate in mutations.items():
            value = json.loads(json.dumps(base))
            mutate(value)
            hostile = tmp / f"{label}.json"
            hostile.write_text(json.dumps(value) + "\n")
            q = structural([sys.executable, "-I", "-S"], hostile, SAMPLES, tmp / f"{label}-out.json")
            cases.append({"case": label, "expected": "REJECT", "observed": q.returncode})
            if q.returncode == 0:
                raise RuntimeError(f"hidden-decorated structural hostile accepted: {label}")
        with SAMPLES.open(newline="") as f:
            sample_base = list(csv.reader(f, delimiter="\t"))
        sample_mutations = {
            "wrong_source_index": lambda rows: rows[1].__setitem__(0, "1"),
            "wrong_source_row": lambda rows: rows[1].__setitem__(1, ("01" if rows[1][1][:2] != "01" else "02") + rows[1][1][2:]),
            "wrong_p2": lambda rows: rows[1].__setitem__(2, "99"),
            "wrong_weight": lambda rows: rows[1].__setitem__(3, str(int(rows[1][3]) + 1)),
            "wrong_pair_uses": lambda rows: rows[1].__setitem__(4, str(int(rows[1][4]) + 1)),
            "wrong_literal_charge": lambda rows: rows[1].__setitem__(12, str(int(rows[1][12]) + 1)),
        }
        for label, mutate in sample_mutations.items():
            rows = [row[:] for row in sample_base]
            mutate(rows)
            hostile = tmp / f"{label}.tsv"
            with hostile.open("w", newline="") as f:
                csv.writer(f, delimiter="\t", lineterminator="\n").writerows(rows)
            q = run([str(LITERAL), "--family", "hidden_decorated_fast", "--samples", str(hostile), "--output", str(tmp / f"{label}-literal.json")])
            cases.append({"case": f"literal_{label}", "expected": "REJECT", "observed": q.returncode})
            if q.returncode == 0:
                raise RuntimeError(f"hidden-decorated literal hostile accepted: {label}")
    report = {"status": "PASS_K24_HIDDEN_DECORATED_COMPLETE_REFEREE_HOSTILES", "cases": cases, "standard_optimized_isolated": True, "scalar_rerun": False}
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "cases": len(cases)}))


if __name__ == "__main__":
    main()
