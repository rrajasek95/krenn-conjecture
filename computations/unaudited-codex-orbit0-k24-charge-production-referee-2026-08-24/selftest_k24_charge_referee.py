#!/usr/bin/env python3
"""Hostile fail-closed tests for the K24 charge shard and literal referees."""
from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_k24_charge.py"
LITERAL = HERE / "referee_k24_charge_literals"
BASE_RESULT = HERE / "control_direct17_prefix1_v2.json"
BASE_SAMPLES = HERE / "control_direct17_prefix1_v2.json.samples.tsv"


def run(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def structural(python_prefix: list[str], result: Path, samples: Path, output: Path) -> subprocess.CompletedProcess:
    return run(python_prefix + [str(VALIDATOR), "shard", "--family", "direct17",
        "--result", str(result), "--samples", str(samples), "--start", "0", "--end", "1",
        "--output", str(output)])


def literal(samples: Path, output: Path) -> subprocess.CompletedProcess:
    return run([str(LITERAL), "--family", "direct17", "--samples", str(samples), "--output", str(output)])


def mutate_json(source: Path, target: Path, mutator) -> None:
    obj = json.loads(source.read_text())
    mutator(obj)
    target.write_text(json.dumps(obj) + "\n")


def mutate_samples(source: Path, target: Path, mutator) -> None:
    with source.open(newline="") as f:
        rows = list(csv.reader(f, delimiter="\t"))
    mutator(rows)
    with target.open("w", newline="") as f:
        csv.writer(f, delimiter="\t", lineterminator="\n").writerows(rows)


def main() -> None:
    tests = []
    with tempfile.TemporaryDirectory(prefix="k24-charge-referee-") as td:
        tmp = Path(td)
        for label, mode in [("std", [sys.executable]), ("opt", [sys.executable, "-O"]),
                            ("isolated", [sys.executable, "-I", "-S"])]:
            q = structural(mode, BASE_RESULT, BASE_SAMPLES, tmp / f"base-{label}.json")
            tests.append({"case": f"baseline_{label}", "expected": "PASS", "observed": q.returncode})
            if q.returncode != 0:
                raise RuntimeError(q.stderr)

        cases = {
            "wrong_U": lambda x: x.__setitem__("scale_U", "1"),
            "legacy_physical_v1": lambda x: x.__setitem__("sample_schema", "legacy_v1"),
            "extra_ID": lambda x: x["groups"][0]["ids"].append("D99:hostile|R:4"),
            "wrong_interval": lambda x: x.__setitem__("source_interval", [0, 2]),
            "nonterminal_count": lambda x: x["groups"][0].__setitem__("irreducible_occurrences", 0),
            "charge_disagreement": lambda x: x["groups"][0].__setitem__("irreducible_charge_scaled_U", "0"),
            "cache_identity": lambda x: x["groups"][0]["terminal_cache"].__setitem__("hits", 0),
        }
        for label, mutator in cases.items():
            r = tmp / f"{label}.json"
            mutate_json(BASE_RESULT, r, mutator)
            q = structural([sys.executable, "-I", "-S"], r, BASE_SAMPLES, tmp / f"out-{label}.json")
            tests.append({"case": label, "expected": "REJECT", "observed": q.returncode})
            if q.returncode == 0:
                raise RuntimeError(f"hostile structural case accepted: {label}")

        sample_cases = {
            "source_head_row": lambda r: r[1].__setitem__(5, ("01" if r[1][5][:2] != "01" else "02") + r[1][5][2:]),
            "source_head_ordinal": lambda r: r[1].__setitem__(4, str(int(r[1][4]) + 1)),
            "unavailable_pivot": lambda r: r[1].__setitem__(11, "99" + r[1][11][r[1][11].find(":"):]),
            "wrong_sign_unit": lambda r: (r[1].__setitem__(8, str(-int(r[1][8]))), r[1].__setitem__(10, str(-int(r[1][10])))),
        }
        for label, mutator in sample_cases.items():
            s = tmp / f"{label}.tsv"
            mutate_samples(BASE_SAMPLES, s, mutator)
            q = literal(s, tmp / f"lit-{label}.json")
            tests.append({"case": label, "expected": "REJECT_LITERAL", "observed": q.returncode})
            if q.returncode == 0:
                raise RuntimeError(f"hostile literal case accepted: {label}")

        bad_header = tmp / "bad-header.tsv"
        shutil.copyfile(BASE_SAMPLES, bad_header)
        text = bad_header.read_text().replace("source_head_ordinal\tsource_head_row\t", "", 1)
        bad_header.write_text(text)
        q1 = structural([sys.executable], BASE_RESULT, bad_header, tmp / "bad-header-struct.json")
        q2 = literal(bad_header, tmp / "bad-header-lit.json")
        tests.append({"case": "incomplete_provenance_header", "expected": "REJECT_BOTH", "observed": [q1.returncode, q2.returncode]})
        if q1.returncode == 0 or q2.returncode == 0:
            raise RuntimeError("incomplete provenance header accepted")

    report = {"status": "PASS_K24_CHARGE_REFEREE_HOSTILE_SELFTEST", "cases": tests,
              "standard_optimized_isolated": True, "production_launched": False}
    output = HERE / "results_k24_charge_referee_hostile_selftest.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "cases": len(tests)}))


if __name__ == "__main__":
    main()
