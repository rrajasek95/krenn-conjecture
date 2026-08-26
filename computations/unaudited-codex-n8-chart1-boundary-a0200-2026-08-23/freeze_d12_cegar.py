#!/usr/bin/env python3
"""Freeze/replay the accepted D12 CEGAR ledger and resumable column state."""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DRIVER = HERE / "run_d12_lazy_cegar.py"
RAW = HERE / "results_d12_lazy_cegar.json"
CHECKPOINT = HERE / "checkpoint_d12_lazy_cegar.json"
RESUME = HERE / "resume_d12_lazy_cegar.json"
RESULT = HERE / "results_d12_lazy_cegar_frozen.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError(path)
    spec.loader.exec_module(module)
    return module


def main():
    raw = json.loads(RAW.read_text())
    checkpoint = json.loads(CHECKPOINT.read_text())
    require(raw["status"] == "D12_CEGAR_CAP_UNRESOLVED"
            and raw["bounded_stop"]["label"] == "round_7_scan_512"
            and len(raw["ledger"]) == 7,
            "bounded terminal ledger changed")
    require([record["new_violating_column_orbits"] for record in raw["ledger"]]
            == [130, 229, 130, 585, 582, 897, 42],
            "accepted crossing census changed")
    require(len(checkpoint["selected_columns"]) == 2571
            and len(checkpoint["last_dual"]) == 1,
            "round-six checkpoint changed")

    driver = load(DRIVER, "chart1_boundary_cegar_freeze")
    provider = driver.Provider()
    selected = {(code, bytes.fromhex(multiplier))
                for code, multiplier in checkpoint["selected_columns"]}
    dual = {bytes.fromhex(row): Fraction(numerator, denominator)
            for row, numerator, denominator in checkpoint["last_dual"]}
    candidates = provider.incident_columns(dual)
    violations = set()
    for column in candidates:
        value = sum(Fraction(coefficient) * dual.get(row, Fraction(0))
                    for row, coefficient in provider.invariant_entries(column).items())
        if value and column not in selected:
            violations.add(column)
    require(len(candidates) == 42 and len(violations) == 42,
            "round-six repair cells changed")
    selected.update(violations)
    require(len(selected) == 2613, "resumable selected-column count changed")

    resume = {
        "format": "n8-chart1-boundary-d12-cegar-resume-v1",
        "accepted_rounds": 7,
        "accepted_ledger": raw["ledger"],
        "selected_column_orbits": len(selected),
        "selected_columns": [[code, multiplier.hex()]
                             for code, multiplier in sorted(selected)],
        "restart_instruction": (
            "Rebuild the full 32,965-row invariant Fh target, adjoin every output of these "
            "2,613 columns, and begin with the exact/modular round-seven span solve."
        ),
    }
    encoded = json.dumps(resume, sort_keys=True, separators=(",", ":"))
    resume["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESUME.write_text(json.dumps(resume, indent=2, sort_keys=True) + "\n")

    payload = {
        "format": "n8-chart1-boundary-d12-cegar-frozen-v1",
        "status": "D12_CEGAR_CAP_UNRESOLVED_RESUMABLE",
        "accepted_rounds": 7,
        "accepted_ledger": raw["ledger"],
        "last_accepted": raw["ledger"][-1],
        "crossing_counts": [record["new_violating_column_orbits"]
                            for record in raw["ledger"]],
        "selected_before_last_repair": 2571,
        "last_repair_cells": len(violations),
        "resumable_selected_column_orbits": len(selected),
        "resume_logical_sha256": resume["logical_sha256"],
        "bounded_stop": raw["bounded_stop"],
        "elapsed_seconds": raw["elapsed_seconds"],
        "peak_rss_bytes": raw["peak_rss_bytes"],
        "wall_cap_note": (
            "The 300-second cap was checked between 512-column scan blocks; terminalization "
            "occurred 8.918 seconds after the nominal cap. No round-seven result was accepted."
        ),
        "theorem_status": (
            "Unresolved. Every accepted finite dual was killed by literal incident columns; "
            "there is neither an exact D12 member nor an exact D12 separator."
        ),
        "scope": raw["scope"],
        "artifacts_sha256": {
            path.name: sha256(path.read_bytes()).hexdigest()
            for path in (DRIVER, RAW, CHECKPOINT, RESUME)
        },
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
