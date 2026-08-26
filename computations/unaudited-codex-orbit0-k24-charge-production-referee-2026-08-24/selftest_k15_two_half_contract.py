#!/usr/bin/env python3
"""Bounded standard/-O/-I-S and hostile tests for the frozen K15 contract."""
from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_merge_k15_fast.py"
REFEREE = HERE / "referee_k24_k15_contract_v1"
RESULT = HERE / "control_k15_literals_v2_prefix8.json"
SAMPLES = Path(str(RESULT) + ".samples.tsv")
OUTPUT = HERE / "results_k15_two_half_contract_hostile_selftest.json"


def run(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def require_outcome(cases: list[dict], case: str, command: list[str], expected_pass: bool) -> None:
    completed = run(command)
    observed = completed.returncode == 0
    cases.append({"case": case, "expected": "PASS" if expected_pass else "REJECT", "observed_returncode": completed.returncode})
    if observed != expected_pass:
        raise RuntimeError(f"{case}: unexpected return {completed.returncode}: {completed.stderr}")


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def write_tsv(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", newline="") as stream:
        csv.writer(stream, delimiter="\t", lineterminator="\n").writerows(rows)


def main() -> None:
    cases: list[dict] = []
    base_result = json.loads(RESULT.read_text())
    with SAMPLES.open(newline="") as stream:
        base_rows = list(csv.reader(stream, delimiter="\t"))
    with tempfile.TemporaryDirectory(prefix="k24-k15-contract-") as directory:
        temp = Path(directory)
        modes = {
            "std": [sys.executable],
            "opt": [sys.executable, "-O"],
            "isolated": [sys.executable, "-I", "-S"],
        }
        for label, prefix in modes.items():
            require_outcome(cases, f"bounded_control_{label}", prefix + [
                str(VALIDATOR), "control", "--result", str(RESULT), "--samples", str(SAMPLES),
                "--start", "0", "--end", "8", "--output", str(temp / f"control-{label}.json"),
            ], True)
            require_outcome(cases, f"prefix_rejected_as_frozen_half_{label}", prefix + [
                str(VALIDATOR), "shard", "--result", str(RESULT), "--samples", str(SAMPLES),
                "--start", "0", "--end", "8", "--output", str(temp / f"half-{label}.json"),
            ], False)
        require_outcome(cases, "independent_eight_literal_baseline", [
            str(REFEREE), "--family", "k15", "--samples", str(SAMPLES),
            "--output", str(temp / "literal-baseline.json"),
        ], True)
        json_mutations = {
            "wrong_U": lambda data: data.__setitem__("scale_U", "1"),
            "extra_sink": lambda data: data["sinks"].__setitem__("D15:foreign|R:2-3-4", dict(next(iter(data["sinks"].values())))),
            "wrong_ID": lambda data: data["sinks"]["D15:{223,232,322}|R:2-3-4"]["ids"].__setitem__(0, "D15:999|R:2-3-4"),
            "fabricated_individual_charge": lambda data: data["sinks"]["D15:{223,232,322}|R:2-3-4"].__setitem__("individual_id_charges", {}),
            "terminal_count": lambda data: data["sinks"]["D15:{223,232,322}|R:2-3-4"].__setitem__("terminal_K24_occurrences", 1),
            "irreducible_charge": lambda data: data["sinks"]["D15:{223,232,322}|R:3-2-4"].__setitem__("irreducible_charge_scaled_U", "1"),
            "denominator_outside_U": lambda data: data["sinks"]["D15:{223,232,322}|R:3-2-4"]["denominator_product_hist"].__setitem__("13", 1),
            "literal_count": lambda data: data["sinks"]["D15:{223,232,322}|R:2-3-4"].__setitem__("literal_witnesses", 3),
            "scope": lambda data: data.__setitem__("scope", "broadened"),
        }
        for label, mutate in json_mutations.items():
            data = json.loads(json.dumps(base_result))
            mutate(data)
            path = temp / f"json-{label}.json"
            write_json(path, data)
            require_outcome(cases, f"structural_{label}", [
                sys.executable, str(VALIDATOR), "control", "--result", str(path),
                "--samples", str(SAMPLES), "--start", "0", "--end", "8",
                "--output", str(temp / f"json-{label}-report.json"),
            ], False)
        structural_sample_mutations = {
            "bin": lambda rows: rows[1].__setitem__(0, "200"),
            "foreign_group": lambda rows: rows[1].__setitem__(2, "source_foreign"),
            "ordinal_range": lambda rows: rows[1].__setitem__(4, "13824"),
            "row_hex": lambda rows: rows[1].__setitem__(5, "zz" + rows[1][5][2:]),
            "denominator": lambda rows: rows[1].__setitem__(7, "13"),
            "unit": lambda rows: rows[1].__setitem__(8, str(-int(rows[1][8]))),
            "contribution": lambda rows: rows[1].__setitem__(10, "0"),
            "step_degree": lambda rows: rows[1].__setitem__(11, rows[1][11].replace(":2:", ":9:", 1)),
        }
        for label, mutate in structural_sample_mutations.items():
            rows = [row[:] for row in base_rows]
            mutate(rows)
            samples_path = temp / f"structural-{label}.tsv"
            write_tsv(samples_path, rows)
            data = json.loads(json.dumps(base_result))
            data["sample_ledger"] = str(samples_path)
            result_path = temp / f"structural-{label}.json"
            write_json(result_path, data)
            require_outcome(cases, f"sample_structure_{label}", [
                sys.executable, str(VALIDATOR), "control", "--result", str(result_path),
                "--samples", str(samples_path), "--start", "0", "--end", "8",
                "--output", str(temp / f"structural-{label}-report.json"),
            ], False)
        literal_mutations = {
            "source_head_row": lambda rows: rows[1].__setitem__(5, ("01" if rows[1][5][:2] != "01" else "02") + rows[1][5][2:]),
            "source_head_ordinal": lambda rows: rows[1].__setitem__(4, str(int(rows[1][4]) + 1)),
            "source_coefficient": lambda rows: rows[1].__setitem__(6, str(-int(rows[1][6]))),
            "literal_pivot": lambda rows: rows[1].__setitem__(11, "99" + rows[1][11][rows[1][11].find(":"):]),
            "literal_child_row": lambda rows: rows[1].__setitem__(11, rows[1][11][:-2] + ("01" if rows[1][11][-2:] != "01" else "02")),
            "terminal_q": lambda rows: rows[1].__setitem__(9, str(int(rows[1][9]) + 1)),
        }
        for label, mutate in literal_mutations.items():
            rows = [row[:] for row in base_rows]
            mutate(rows)
            path = temp / f"literal-{label}.tsv"
            write_tsv(path, rows)
            require_outcome(cases, f"independent_literal_{label}", [
                str(REFEREE), "--family", "k15", "--samples", str(path),
                "--output", str(temp / f"literal-{label}-report.json"),
            ], False)
    report = {
        "status": "PASS_K24_K15_TWO_HALF_CONTRACT_HOSTILE_SELFTEST",
        "cases": cases, "case_count": len(cases),
        "modes": ["standard", "optimized", "isolated-no-site"],
        "bounded_scalar_slices": 8, "bounded_literal_witnesses": 8,
        "production_launched": False,
    }
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "cases": len(cases)}))


if __name__ == "__main__":
    main()
