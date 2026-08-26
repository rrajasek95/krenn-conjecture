#!/usr/bin/env python3
"""Independent exact-Q referee for the component-wide weak mate unit."""

from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
EXPORTER = HERE / "export_AB_component_weak_mate.py"
EXPORT = HERE / "results_AB_component_weak_mate_export.json"
LEDGER = HERE / "results_AB_component_localizer_faces.json"
INPUT = HERE / "AB_component_weak_mate_exact.msolve"
RAW = HERE / "AB_component_weak_mate_p1073741827.msolve"
MODULAR = (
    HERE / "AB_component_weak_mate_explicit_p1073741827.msolve",
    HERE / "AB_component_weak_mate_explicit_p1073741789.msolve",
)
FROZEN = HERE / "results_AB_component_weak_mate_exact.full.gb.out"
OUT = HERE / "results_AB_component_weak_mate_exact_audit.json"
COEFFICIENT_AFTER_SYMBOL = re.compile(
    r"(?:^|[^A-Za-z0-9_])[A-Za-z_][A-Za-z0-9_]*(?:\^\d+)?\*[+-]?\d")


def require(value, detail):
    if not value:
        raise RuntimeError(detail)


def parse_input(path):
    lines = path.read_text().splitlines()
    require(len(lines) >= 3, f"short msolve input: {path.name}")
    variables = tuple(lines[0].split(","))
    characteristic = int(lines[1])
    rows = tuple(row.strip() for row in "\n".join(lines[2:]).split(",")
                 if row.strip())
    require(len(variables) == len(set(variables)) and
            all(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", x)
                for x in variables),
            f"invalid variable header: {path.name}")
    for row in rows:
        require(not any(token in row for token in ("(", ")", "[", "]", ";")),
                f"forbidden syntax in {path.name}")
        require("**" not in row and not COEFFICIENT_AFTER_SYMBOL.search(row),
                f"noncanonical/coefficient-after-symbol row in {path.name}")
    return variables, characteristic, rows


def unit_basis(path):
    text = path.read_text()
    return ("#field characteristic: 0" in text and
            "#length of basis:      1 element" in text and
            text.rstrip().endswith("[1]:"))


def main():
    export = json.loads(EXPORT.read_text())
    ledger = json.loads(LEDGER.read_text())
    exact_variables, exact_characteristic, exact_rows = parse_input(INPUT)
    raw_variables, raw_characteristic, raw_rows = parse_input(RAW)
    require(exact_characteristic == 0 and raw_characteristic == 1073741827,
            "exact/raw characteristic changed")
    require(len(exact_variables) == 21 and exact_variables[-1] == "u" and
            exact_variables[:-1] == raw_variables,
            "exact variable header changed")
    require(len(exact_rows) == 33 and len(raw_rows) == 33,
            "component-wide row count changed")
    require(exact_rows[:-1] == raw_rows[:-1],
            "ordinary exact/raw rows ceased to agree")
    h_terms = raw_rows[-1].split("+")
    expected_rab = "-1+"+"+".join(
        "u" if term == "1" else "u*"+term for term in h_terms)
    require(exact_rows[-1] == expected_rab,
            "literal mate-H Rabinowitsch row changed")
    for modular_path in MODULAR:
        variables, characteristic, rows = parse_input(modular_path)
        require(characteristic in (1073741827, 1073741789) and
                variables == exact_variables and rows == exact_rows,
                f"exact/modular literal rows differ: {modular_path.name}")

    require(export["zero_cells"] == [1, 2, 21, 22] and
            len(export["entry_support"]) == 16 and
            export["left_Q_support"] == [0, 5, 6, 9, 10, 15] and
            export["ordinary_row_count"] == 32 and
            len(export["generator_aliases"]) == 32,
            "forced-support declaration changed")
    localizers = export["localizer_audit"]
    require(localizers["source_component_rows_replay"] and
            localizers["chart_factors_preserved"] and
            localizers["left_H_not_inferred"],
            "source/chart/H scope audit changed")
    chart_units = {factor
                   for factors in ledger["chart_factorization"].values()
                   for factor, _ in factors}
    groups = (
        localizers["cofactor_units_for_mate_entry_zeros"],
        localizers["entry_units_for_mate_cofactor_rows"],
        localizers["Q_units_for_complement_mate_Q_rows"],
    )
    require([len(group) for group in groups] == [4, 16, 6],
            "localizer audit cardinalities changed")
    for group in groups:
        for record in group.values():
            require(record["all_factors_are_chart_units"] and
                    set(record["numerator_factors"]) <= chart_units,
                    "a forced localizer is not supported by chart units")

    exact_meta = export["exact_output"]
    require(exact_meta["sha256"] == sha256(INPUT.read_bytes()).hexdigest() and
            exact_meta["strict_coefficient_first_parse"] and
            exact_meta["literal_modular_row_replay"] and
            exact_meta["mate_H_rabinowitsch_sha256"] ==
            sha256(re.sub(r"\s+", "", exact_rows[-1]).encode()).hexdigest(),
            "exact export metadata changed")
    require(unit_basis(FROZEN), "frozen exact basis is not [1]")
    with tempfile.TemporaryDirectory(prefix="AB-component-exact-referee-") as tmp:
        replay = Path(tmp) / "replay.gb.out"
        completed = subprocess.run(
            ["msolve", "-f", str(INPUT), "-o", str(replay), "-t", "4",
             "-g", "2", "-v", "0", "-l", "2"],
            capture_output=True, text=True, timeout=30, check=False)
        require(completed.returncode == 0 and unit_basis(replay),
                "independent exact msolve replay failed")
        replay_sha = sha256(replay.read_bytes()).hexdigest()

    result = {
        "status": "UNAUDITED exact-Q component-wide weak mate UNIT audit PASS",
        "exact_basis": "[1]",
        "literal_replay": True,
        "strict_coefficient_first_input": True,
        "ordinary_row_count": 32,
        "mate_variable_count": 20,
        "rabinowitsch_variable": "u",
        "all_source_rows_replay": True,
        "all_localizers_are_chart_units": True,
        "left_H_not_inferred": True,
        "mate_H_localized_literally": True,
        "two_modular_inputs_replayed_literally": True,
        "input_sha256": sha256(INPUT.read_bytes()).hexdigest(),
        "frozen_output_sha256": sha256(FROZEN.read_bytes()).hexdigest(),
        "replay_output_sha256": replay_sha,
        "conclusion": (
            "No H-live mate exists for any left presentation on the exact "
            "A=B generic-cycle component chart. The certificate uses only "
            "component-wide chart-forced incidence data, so it also covers "
            "every localizer divisor and every deeper C-face intersection."
        ),
        "scope_guard": (
            "Exact over Q for the frozen full-source A=B component and its "
            "original live chart only; no left H equation is assumed."
        ),
        "source_hashes": {
            "exporter": sha256(EXPORTER.read_bytes()).hexdigest(),
            "export": sha256(EXPORT.read_bytes()).hexdigest(),
            "localizer_ledger": sha256(LEDGER.read_bytes()).hexdigest(),
            "raw_modular_template": sha256(RAW.read_bytes()).hexdigest(),
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("AB component exact weak mate audit PASS")
    print("basis [1], rows", result["ordinary_row_count"], "+ mate H")
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
