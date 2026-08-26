#!/usr/bin/env python3
"""Freeze the two smallest modular-greedy D0 source cores over Q."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
TOOL = HERE.parent / "toolkit/groebner/msolve_io.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


IO = load("d0_char0_msolve_io", TOOL)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    # Factor 0 uses compatibility 1; factor 1 uses compatibility 2.
    cores = ((0, "1"), (1, "2"))
    result = {"cores": []}
    for branch, compatibility in cores:
        source = HERE / (f"d0_factor{branch}_greedy_c{compatibility}_"
                         "p1073741827.ms")
        lines = source.read_text().splitlines()
        assert lines[1] == "1073741827"
        lines[1] = "0"
        target = HERE / f"d0_factor{branch}_exact_char0_core.msolve"
        target.write_text("\n".join(lines) + "\n")
        parsed = IO.read_msolve_input(target, strict=True,
                                      allow_characteristic_zero=True)
        assert parsed.characteristic == 0 and len(parsed.polynomials) == 6
        result["cores"].append({
            "branch": branch,
            "compatibility_index": int(compatibility),
            "path": target.name,
            "sha256": digest(target),
            "row_count": len(parsed.polynomials),
            "row_sha256": list(parsed.polynomial_sha256),
            "rab_row_index": 5,
            "rab_row_fully_expanded": True,
            "strict_parenthesis_guard": True,
        })
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    path = HERE / "results_d0_exact_char0_core_export.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("exact char0 cores PASS", result["logical_sha256"])


if __name__ == "__main__":
    main()
