#!/usr/bin/env python3
"""Export pinned, line-oriented inputs for the incremental degree-nine solver."""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
D8 = HERE / "results_degree8_rust_cegar.json"
CHECKPOINT = HERE / "results_degree9_rust_cegar_checkpoint.json"
DUAL_OUT = HERE / "degree9_lambda8_mod.tsv"
COLUMNS_OUT = HERE / "degree9_selected_round14.tsv"
RESULT_OUT = HERE / "results_degree9_incremental_inputs.json"
PRIME = 1_073_741_827
EXPECTED_DUAL = "561546730a738ad3e3432ae5f5b63456735514148f32b77268debbebdae09d9d"
EXPECTED_CHECKPOINT = "9100c0624464d0a82c0e11bde9a2782d555d1f1d7b7f7368b603a343928034a5"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    require(digest(CHECKPOINT) == EXPECTED_CHECKPOINT,
            "round-14 checkpoint changed")
    d8 = json.loads(D8.read_text())
    checkpoint = json.loads(CHECKPOINT.read_text())
    require(d8["status"] == "EXTENDED_DUAL_EXACT_Q"
            and d8["exact_extended_dual_sha256"] == EXPECTED_DUAL,
            "lambda8 changed")
    require(checkpoint["completed_round"] == 14
            and len(checkpoint["selected_columns"]) == 53_995,
            "selected packet changed")

    dual_lines = [f"KRENN_N8_LAMBDA8_MOD_V1 {PRIME} {len(d8['exact_extended_dual'])}"]
    for row, numerator, denominator in d8["exact_extended_dual"]:
        value = Fraction(numerator, denominator)
        residue = value.numerator * pow(value.denominator, PRIME - 2, PRIME) % PRIME
        require(residue, "lambda8 exported a zero residue")
        dual_lines.append(f"ROW {row or '-'} {residue} {numerator} {denominator}")
    DUAL_OUT.write_text("\n".join(dual_lines) + "\n")

    selected = sorted((word, multiplier)
                      for word, multiplier in checkpoint["selected_columns"])
    column_lines = [f"KRENN_N8_D9_SELECTED_V1 {len(selected)}"]
    column_lines.extend(f"COLUMN {word} {multiplier or '-'}"
                        for word, multiplier in selected)
    COLUMNS_OUT.write_text("\n".join(column_lines) + "\n")

    result = {
        "status": "PASS_PINNED_DEGREE9_INCREMENTAL_INPUT_EXPORT",
        "prime": PRIME,
        "lambda8_rows": len(d8["exact_extended_dual"]),
        "selected_columns": len(selected),
        "lambda8_exact_sha256": EXPECTED_DUAL,
        "frozen_checkpoint_sha256": EXPECTED_CHECKPOINT,
        "dual_tsv_sha256": digest(DUAL_OUT),
        "columns_tsv_sha256": digest(COLUMNS_OUT),
        "scope": "input export only; no degree-nine solve or saturation claim",
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT_OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
