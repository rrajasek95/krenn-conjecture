#!/usr/bin/env python3
"""Source-faithful replay of the exact A=B=0 timeout result."""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
EXPORTER = HERE / "export_face03130_A0B0_char0.py"
EXPORT = HERE / "results_face03130_A0B0_char0_export.json"
INPUT = HERE / "face03130_A0B0_base_live_char0.msolve"
RUN = HERE / "results_face03130_A0B0_base_live_exact_run.json"
OUTPUT = HERE / "face03130_A0B0_base_live_char0.out"
TOOLKIT = REPO / "computations/toolkit/groebner/msolve_io.py"
OUT_PREFIX = HERE / "results_face03130_A0B0_timeout_audit"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutation", action="store_true")
    args = parser.parse_args()
    IO = load("face03130_A0B0_audit_io", TOOLKIT)
    export = json.loads(EXPORT.read_text())
    frozen_export_hash = export.pop("logical_sha256")
    require(logical_hash(export) == frozen_export_hash,
            "export logical digest mismatch")
    before = digest(INPUT)
    replay = subprocess.run([sys.executable, str(EXPORTER)], cwd=HERE,
                            capture_output=True, text=True, timeout=120)
    require(replay.returncode == 0 and "exact export PASS" in replay.stdout,
            "source exporter replay failed")
    export2 = json.loads(EXPORT.read_text())
    frozen2 = export2.pop("logical_sha256")
    require(export2 == export and frozen2 == frozen_export_hash and
            digest(INPUT) == before == export["input_sha256"],
            "export/input changed on replay")
    parsed = IO.read_msolve_input(INPUT, strict=True,
                                  allow_characteristic_zero=True)
    require(parsed.characteristic == 0 and len(parsed.polynomials) == 19,
            "strict input shape changed")
    require(export["literal_source_indices"] == list(range(6, 22)) and
            export["literal_source_rank_over_Q"] == 16,
            "full literal source ledger changed")
    require(export["row_labels"][:2] == ["branch_A", "branch_B"] and
            export["row_labels"][2:18] == [
                f"raw_{index}_{label}" for index, label in zip(
                    range(6, 22), export["literal_source_labels"], strict=True)] and
            export["row_labels"][-1] == "RAB_base_live_without_H",
            "branch/source/localizer ordering changed")
    require(export["localized_factors_stage1"] == [
                "selected_base", "both_live_a_d", "remaining_c_numerators"] and
            export["explicitly_not_localized_stage1"] == ["H", "A"],
            "stage-1 localization scope changed")
    require(export["factor_profiles"]["H"]["expanded"] not in
            parsed.polynomials[-1], "H entered stage-1 saturator")
    require("z" in parsed.polynomials[-1] and
            parsed.polynomials[-1].endswith("-1"),
            "Rabinowitsch row changed")

    run = json.loads(RUN.read_text())
    require(run["timeout_seconds"] == 600 and
            run["process_status"] == "timeout" and
            run["returncode"] is None and not run["unit_basis"] and
            not run["positive_dimensional_envelope"] and
            run["input_sha256"] == digest(INPUT) and
            run["output_bytes"] == 0 and OUTPUT.exists() and
            run["output_sha256"] == digest(OUTPUT) ==
            sha256(b"").hexdigest(), "terminal timeout record changed")
    if args.mutation:
        mutated = INPUT.read_text().replace(export["branch_polynomials"]["A"],
                                             export["branch_polynomials"]["A"]+"+1",
                                             1)
        require(sha256(mutated.encode()).hexdigest() != digest(INPUT),
                "input mutation failed to fire")

    result = {
        "status": "PASS exact-Q A=B=0 source/timeout replay",
        "mutation": args.mutation,
        "export_logical_sha256": frozen_export_hash,
        "input_sha256": digest(INPUT), "run_sha256": digest(RUN),
        "timeout_seconds": 600, "elapsed_seconds": run["elapsed_seconds"],
        "output_bytes": 0, "literal_source_rows": 16,
        "localized_stage1": export["localized_factors_stage1"],
        "not_localized": export["explicitly_not_localized_stage1"],
        "conclusion": (
            "The sole canonical characteristic-zero gate for the normalized "
            "0:31:30 A=B=0 branch reached its 600-second cap without output. "
            "This is neither a unit nor a positive-dimensional result. H is "
            "therefore not added, and the branch remains open."),
        "scope_guard": (
            "No claim is made about the A-open/R25 branch. A timeout is not "
            "an algebraic result; this package certifies only its exact input, "
            "source provenance, localization, and terminal process state."),
    }
    result["logical_sha256"] = logical_hash(result)
    suffix = "mutation" if args.mutation else "standard"
    path = OUT_PREFIX.with_name(OUT_PREFIX.name + "_" + suffix + ".json")
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("face03130 A=B=0 timeout audit PASS", result["logical_sha256"])


if __name__ == "__main__":
    main()
