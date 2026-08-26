#!/usr/bin/env python3
"""Repackage the frozen full modular basis for finite-scheme solving."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
TOOLKIT = HERE.parent / "toolkit" / "groebner"
FULL = (HERE /
        "results_branch0_cycle_delta_au_open_all_minors_full_msolve.sat.full.gb.out")
STAGE = HERE / "branch0_cycle_delta_au_open_all_minors_full_stage.msolve"
RESULT = HERE / "results_branch0_cycle_delta_au_open_all_minors_full_stage.json"

if str(TOOLKIT) not in sys.path:
    sys.path.append(str(TOOLKIT))
from msolve_io import (file_sha256, read_msolve_basis, read_msolve_input,
                       write_input_from_full_basis)  # noqa: E402


def main():
    basis = read_msolve_basis(FULL, require_full=True)
    if basis.unit or basis.declared_length != 117:
        raise RuntimeError("the frozen finite all-minor basis changed")
    write_input_from_full_basis(basis, STAGE)
    stage = read_msolve_input(STAGE, strict=True)
    result = {
        "status": "UNAUDITED strict full-basis finite-solve stage",
        "source_full_basis": FULL.name,
        "source_full_basis_sha256": file_sha256(FULL),
        "stage_file": STAGE.name,
        "stage_file_sha256": stage.file_sha256,
        "stage_logical_sha256": stage.logical_sha256,
        "characteristic": basis.characteristic,
        "variables": list(basis.variables),
        "basis_length": basis.declared_length,
        "scope": (
            "Deterministic repackaging only. The source is a modular full "
            "basis of the live-saturated necessary determinantal locus; "
            "finite solving and every later point classification remain "
            "modular discovery."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("all-minor full-basis stage: PASS")
    print("stage sha256:", result["stage_file_sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
