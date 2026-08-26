#!/usr/bin/env python3
"""Referee the exact-Q compact Cof(3,3) unit and its source implication."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
EXPORTER_PATH = HERE / "export_branch0_cycle_delta_au_open_cofactor33_compact.py"
EXPORT_RESULT = HERE / "results_branch0_cycle_delta_au_open_cofactor33_export.json"
INPUT = HERE / "branch0_cycle_delta_au_open_cofactor33_char0.msolve"
OUTPUT = HERE / "results_branch0_cycle_delta_au_open_cofactor33_char0_exact.param.out"
MANIFEST = HERE / "results_branch0_cycle_delta_au_open_cofactor33_char0_exact.manifest.json"
RESULT = HERE / "results_branch0_cycle_delta_au_open_cofactor33_exact_unit.json"
TOOLKIT = HERE.parent / "toolkit" / "groebner"
if str(TOOLKIT) not in sys.path:
    sys.path.append(str(TOOLKIT))
from msolve_io import read_msolve_input  # noqa: E402


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    exporter = load("n8_cycle_cofactor33_exact_unit_exporter",
                    EXPORTER_PATH)
    core, metadata = exporter.derive_core()
    frozen_export = json.loads(EXPORT_RESULT.read_text())
    require(metadata["core_sha256"] == frozen_export["core_sha256"]
            and metadata["core_terms"] == 4031
            and metadata["core_degrees_b0_b1_d1_x"] == [1, 7, 24, 19],
            "the source-derived compact core changed")

    parsed = read_msolve_input(INPUT, strict=True,
                               allow_characteristic_zero=True)
    require(parsed.characteristic == 0
            and parsed.variables == ("b0", "b1", "d1", "x", "z")
            and len(parsed.polynomials) == 18,
            "the exact-Q input contract changed")
    require(parsed.polynomial_sha256[-2] == sha256(
        exporter.BASE.encode(core).replace(" ", "").encode("ascii")).hexdigest(),
        "the source core is not the penultimate exact-Q equation")

    manifest = json.loads(MANIFEST.read_text())
    require(manifest["status"] == "completed_characteristic_zero_parametrization"
            and manifest["returncode"] == 0
            and manifest["input"]["sha256"] == file_sha(INPUT)
            and manifest["solution"] == {
                "kind": "empty", "degree": 0, "variable_count": 5},
            "the exact-Q runner did not certify the empty scheme")
    require(OUTPUT.read_text().strip() == "[-1]:"
            and manifest["output"]["sha256"] == file_sha(OUTPUT),
            "the exact empty output changed")

    result = {
        "status": "UNAUDITED exact characteristic-zero unit theorem",
        "branch": "Delta=0,Bplus!=0,Au!=0,A!=0 branch0 k4-cycle",
        "source_row": "cofactor_3_3",
        "core_terms": 4031,
        "core_degrees_b0_b1_d1_x": [1, 7, 24, 19],
        "core_sha256": metadata["core_sha256"],
        "input_sha256": file_sha(INPUT),
        "input_logical_sha256": parsed.logical_sha256,
        "output_sha256": file_sha(OUTPUT),
        "runner_logical_sha256": manifest["logical_sha256"],
        "runner_elapsed_seconds": manifest["elapsed_seconds"],
        "conclusion": (
            "No full literal packet solution exists on the declared open "
            "branch. Every such solution kills Q, all fifteen augmented "
            "minors, and the fraction-free Cof(3,3) core; the exact-Q "
            "Rabinowitsch system containing these necessary equations is "
            "empty."),
        "scope": (
            "This is an exact characteristic-zero emptiness result for the "
            "displayed localized branch. It is not a sparse Nullstellensatz "
            "multiplier ledger. Combining it with adjacent frozen divisor "
            "closures is a separate bookkeeping step."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("compact Cof(3,3) exact-Q unit referee: PASS")
    print("runner logical sha256:", result["runner_logical_sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
