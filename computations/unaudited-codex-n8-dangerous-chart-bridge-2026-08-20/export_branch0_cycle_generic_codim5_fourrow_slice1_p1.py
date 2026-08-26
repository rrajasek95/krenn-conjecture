#!/usr/bin/env python3
"""Remove only the second hyperplane from the frozen two-slice p1 probe."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "branch0_cycle_generic_codim5_fourrow_slice2_c8open_p1073741827.msolve"
SOURCE_RESULT = HERE / "results_branch0_cycle_generic_codim5_fourrow_slice2_c8open_export.json"
OUTPUT = HERE / "branch0_cycle_generic_codim5_fourrow_slice1_c8open_p1073741827.msolve"
LABELS = HERE / "branch0_cycle_generic_codim5_fourrow_slice1_c8open_labels.json"
RESULT = HERE / "results_branch0_cycle_generic_codim5_fourrow_slice1_c8open_export.json"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    lines = SOURCE.read_text().splitlines()
    rows = "\n".join(lines[2:]).strip().split(",\n")
    source_result = json.loads(SOURCE_RESULT.read_text())
    require(lines[:2] == ["b0,b1,d1,d3,d4", "1073741827"]
            and len(rows) == 7, "two-slice source changed")
    require(rows[4] == "b0+2*b1+3*d1+5*d3+7*d4-11"
            and rows[5] == "b0+9*b1+4*d1+22*d3+10*d4-46",
            "deterministic hyperplanes changed")
    output_rows = [*rows[:5], rows[6]]
    OUTPUT.write_text("\n".join(lines[:2])+"\n"+",\n".join(output_rows)+"\n")
    labels = ["P324", "P851", "P1342", "P1846",
              "slice_h1", "C8_open_live_saturator"]
    LABELS.write_text(json.dumps({"labels": labels}, indent=2)+"\n")
    result = {
        "status": "UNAUDITED p1 four-row one-slice C8-open export",
        "two_slice_source": SOURCE.name,
        "two_slice_source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "two_slice_export_result_sha256": source_result["result_sha256"],
        "output": OUTPUT.name,
        "output_sha256": sha256(OUTPUT.read_bytes()).hexdigest(),
        "labels": LABELS.name,
        "labels_sha256": sha256(LABELS.read_bytes()).hexdigest(),
        "retained_hyperplane": rows[4],
        "removed_hyperplane": rows[5],
        "row_count": len(output_rows),
        "live_identity": source_result["live_identity"],
        "scope": (
            "The exact same four rows and base*C8 live saturator as the "
            "two-slice overslice control, with only its second deterministic "
            "affine hyperplane removed. Modular discovery only."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("four-row one-slice C8-open export: PASS")
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
