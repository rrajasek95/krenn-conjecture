#!/usr/bin/env python3
"""Bounded hostile tests for the prepared R2-2-4 half merger/literal referee."""
from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MERGER = HERE / "validate_merge_k16_r224.py"
LITERAL = HERE / "referee_k24_charge_literals"
RESULT = ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_k16_r224_prefix262144.json"
SAMPLES = Path(str(RESULT) + ".samples.tsv")
OUTPUT = HERE / "results_k16_r224_referee_hostile_selftest.json"


def run(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main() -> None:
    cases = []
    with tempfile.TemporaryDirectory(prefix="k24-k16-r224-referee-") as td:
        tmp = Path(td)
        q = run([str(LITERAL), "--family", "k16r224", "--samples", str(SAMPLES), "--output", str(tmp / "baseline.json")])
        cases.append({"case": "bounded_257_literal_baseline", "expected": "PASS", "observed": q.returncode})
        if q.returncode != 0:
            raise RuntimeError(q.stderr)
        for label, prefix in [("std", [sys.executable]), ("opt", [sys.executable, "-O"]), ("isolated", [sys.executable, "-I", "-S"])]:
            q = run(prefix + [str(MERGER), "shard", "--result", str(RESULT), "--samples", str(SAMPLES), "--start", "0", "--end", "12048547", "--output", str(tmp / f"mode-{label}.json")])
            cases.append({"case": f"distributed_as_half_{label}", "expected": "REJECT", "observed": q.returncode})
            if q.returncode == 0:
                raise RuntimeError("distributed prefix accepted as contiguous half")
        with SAMPLES.open(newline="") as f:
            base = list(csv.reader(f, delimiter="\t"))
        mutations = {
            "source_row": lambda rows: rows[1].__setitem__(3, ("01" if rows[1][3][:2] != "01" else "02") + rows[1][3][2:]),
            "p1": lambda rows: rows[1].__setitem__(6, "99"),
            "K18_row": lambda rows: rows[1].__setitem__(4, ("01" if rows[1][4][:2] != "01" else "02") + rows[1][4][2:]),
            "p2": lambda rows: rows[1].__setitem__(8, "99"),
            "K20_row": lambda rows: rows[1].__setitem__(5, ("01" if rows[1][5][:2] != "01" else "02") + rows[1][5][2:]),
            "p3": lambda rows: rows[1].__setitem__(10, "99"),
            "unit_sign": lambda rows: rows[1].__setitem__(15, str(-int(rows[1][15]))),
        }
        for label, mutate in mutations.items():
            rows = [row[:] for row in base]
            mutate(rows)
            path = tmp / f"{label}.tsv"
            with path.open("w", newline="") as f:
                csv.writer(f, delimiter="\t", lineterminator="\n").writerows(rows)
            q = run([str(LITERAL), "--family", "k16r224", "--samples", str(path), "--output", str(tmp / f"literal-{label}.json")])
            cases.append({"case": f"literal_{label}", "expected": "REJECT", "observed": q.returncode})
            if q.returncode == 0:
                raise RuntimeError(f"R2-2-4 hostile literal accepted: {label}")
    report = {"status": "PASS_K24_K16_R224_REFEREE_HOSTILE_SELFTEST", "cases": cases, "production_launched": False}
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "cases": len(cases)}))


if __name__ == "__main__":
    main()
