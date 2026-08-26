#!/usr/bin/env python3
"""Hostile controls for the frozen R4-4 sample-only support repair."""
from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_k24_charge.py"
AUDIT = HERE / "audit_k16_r44_support_patch.py"
LITERAL = HERE / "referee_k24_charge_literals"
CANDIDATES = HERE / "k24_k16_r44_support_candidates.tsv"
OLD = HERE.parents[1] / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_k16_r44_prefix262144.json"
NEW = HERE / "control_k16_r44_distributed262144_support_v4.json"
OUTPUT = HERE / "results_k16_r44_support_patch_hostile_selftest.json"


def run(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def candidate_check(prefix: list[str], candidate: Path, output: Path) -> subprocess.CompletedProcess:
    return run(prefix + [str(VALIDATOR), "fast-k16-r44-candidates", "--candidates", str(candidate), "--output", str(output)])


def literal_check(candidate: Path, output: Path) -> subprocess.CompletedProcess:
    return run([str(LITERAL), "--family", "k16r44candidates", "--samples", str(candidate), "--output", str(output)])


def read_rows(path: Path) -> list[list[str]]:
    with path.open(newline="") as f:
        return list(csv.reader(f, delimiter="\t"))


def write_rows(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", newline="") as f:
        csv.writer(f, delimiter="\t", lineterminator="\n").writerows(rows)


def main() -> None:
    tests = []
    with tempfile.TemporaryDirectory(prefix="k24-k16-r44-support-") as td:
        tmp = Path(td)
        for label, prefix in [("std", [sys.executable]), ("opt", [sys.executable, "-O"]),
                              ("isolated", [sys.executable, "-I", "-S"])]:
            q = candidate_check(prefix, CANDIDATES, tmp / f"candidate-{label}.json")
            tests.append({"case": f"candidate_baseline_{label}", "expected": "PASS", "observed": q.returncode})
            if q.returncode != 0:
                raise RuntimeError(q.stderr)

        q = run([sys.executable, "-I", "-S", str(AUDIT), "--output", str(tmp / "audit.json")])
        tests.append({"case": "scalar_equivalence_baseline", "expected": "PASS", "observed": q.returncode})
        if q.returncode != 0:
            raise RuntimeError(q.stderr)

        changed = json.loads(NEW.read_text())
        for label, key in [("changed_charge", "full_charge_scaled_U"),
                           ("changed_count", "p2_uses")]:
            hostile = dict(changed)
            hostile[key] = str(int(hostile[key]) + 1)
            hp = tmp / f"{label}.json"
            hp.write_text(json.dumps(hostile) + "\n")
            q = run([sys.executable, "-I", "-S", str(AUDIT), "--old", str(OLD), "--new", str(hp), "--output", str(tmp / f"{label}-out.json")])
            tests.append({"case": label, "expected": "REJECT", "observed": q.returncode})
            if q.returncode == 0:
                raise RuntimeError(f"scalar hostile accepted: {label}")

        for label, mutate in [
            ("positive_support_outside", lambda value: value["nonzero_support_record_hist"].__setitem__("37", 1)),
            ("missing_realized_support_bin", lambda value: value["nonzero_support_record_hist"].pop("36")),
        ]:
            hostile = json.loads(NEW.read_text())
            mutate(hostile)
            hp = tmp / f"{label}.json"
            hp.write_text(json.dumps(hostile) + "\n")
            q = run([sys.executable, "-I", "-S", str(AUDIT), "--old", str(OLD), "--new", str(hp), "--output", str(tmp / f"{label}-out.json")])
            tests.append({"case": label, "expected": "REJECT", "observed": q.returncode})
            if q.returncode == 0:
                raise RuntimeError(f"support hostile accepted: {label}")

        base = read_rows(CANDIDATES)
        mutations = {
            "missing_candidate": lambda rows: rows.pop(),
            "duplicate_slot": lambda rows: rows[2].__setitem__(0, rows[1][0]),
            "wrong_record_index": lambda rows: rows[1].__setitem__(2, str(int(rows[1][2]) + 1)),
            "wrong_pivot": lambda rows: rows[1].__setitem__(6, "99"),
            "wrong_source_row": lambda rows: rows[1].__setitem__(4, ("01" if rows[1][4][:2] != "01" else "02") + rows[1][4][2:]),
            "wrong_unit": lambda rows: rows[1].__setitem__(12, str(-int(rows[1][12]))),
        }
        for label, mutate in mutations.items():
            rows = [r[:] for r in base]
            mutate(rows)
            candidate = tmp / f"{label}.tsv"
            write_rows(candidate, rows)
            q = candidate_check([sys.executable, "-I", "-S"], candidate, tmp / f"{label}-struct.json")
            tests.append({"case": f"struct_{label}", "expected": "REJECT", "observed": q.returncode})
            if q.returncode == 0:
                raise RuntimeError(f"candidate hostile accepted: {label}")
            if label in {"wrong_record_index", "wrong_pivot", "wrong_source_row", "wrong_unit"}:
                q = literal_check(candidate, tmp / f"{label}-literal.json")
                tests.append({"case": f"literal_{label}", "expected": "REJECT", "observed": q.returncode})
                if q.returncode == 0:
                    raise RuntimeError(f"literal hostile accepted: {label}")

    report = {
        "status": "PASS_K24_K16_R44_SUPPORT_PATCH_HOSTILE_SELFTEST",
        "cases": tests,
        "standard_optimized_isolated": True,
        "scalar_production_launched": False,
    }
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "cases": len(tests)}))


if __name__ == "__main__":
    main()
