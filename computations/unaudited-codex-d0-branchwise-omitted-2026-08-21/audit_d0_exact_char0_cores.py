#!/usr/bin/env python3
"""Audit exact-Q msolve units back to the frozen literal source packets."""

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


IO = load("d0_exact_char0_audit_io", TOOL)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    source_export = json.loads(
        (HERE / "results_d0_exact_branch_packet_export.json").read_text())
    core_export = json.loads(
        (HERE / "results_d0_exact_char0_core_export.json").read_text())
    selected = {0: 1, 1: 2}
    records = []
    for branch in (0, 1):
        source_path = HERE / f"d0_factor{branch}_source_packet_p1073741827.ms"
        source = IO.read_msolve_input(source_path, strict=True)
        require(len(source.polynomials) == 9, "source packet row count changed")
        core_path = HERE / f"d0_factor{branch}_exact_char0_core.msolve"
        core = IO.read_msolve_input(core_path, strict=True,
                                    allow_characteristic_zero=True)
        expected = ((source.polynomials[selected[branch]],) +
                    source.polynomials[4:])
        require(core.polynomials == expected,
                f"branch {branch}: exact core is not the selected source core")
        output_path = HERE / f"d0_factor{branch}_exact_char0_core.out"
        output = output_path.read_text().strip()
        require(output == "[-1]:", f"branch {branch}: not a literal unit output")
        # Must fire if the terminal output or selected compatibility is changed.
        require(output.replace("-1", "1") != "[-1]:",
                "output mutation failed to fire")
        mutated = list(core.polynomials)
        mutated[0] = mutated[0] + "+1"
        require(tuple(mutated) != expected, "row mutation failed to fire")
        records.append({
            "branch": branch,
            "selected_compatibility_index": selected[branch],
            "packet_labels": source_export["branches"][branch]["packet_labels"],
            "core_path": core_path.name,
            "core_sha256": digest(core_path),
            "core_row_sha256": list(core.polynomial_sha256),
            "source_packet_path": source_path.name,
            "source_packet_sha256": digest(source_path),
            "output_path": output_path.name,
            "output_sha256": digest(output_path),
            "literal_output": output,
        })
    result = {
        "status": "UNAUDITED exact-Q D0 branch packet units PASS",
        "records": records,
        "source_export_logical_sha256": source_export["logical_sha256"],
        "core_export_logical_sha256": core_export["logical_sha256"],
        "theorem": (
            "On the D0=0,C0!=0,selected-pivot-open chart, the exact degree-21 "
            "factor-0 branch is incompatible with compatibility 1 and literal "
            "Cof(1,3),Cof(2,3),Cof(3,3); factor-1 is incompatible with "
            "compatibility 2 and literal Cof(2,3),Cof(3,3),Cof(4,3)."
        ),
        "scope_guard": (
            "This closes the two reconstructed degree-21 resultant-factor "
            "branches only. The earlier exact resultant divisibility does not "
            "prove that these factors exhaust the entire source scheme or the "
            "large resultant quotient. Single omitted cofactors and every pair "
            "were nonunits at p1073741827; no one-row theorem is claimed."
        ),
        "mutation_control": (
            "Replacing [-1]: by [1]: and adding 1 to the selected compatibility "
            "both fire before theorem acceptance."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    target = HERE / "results_d0_exact_char0_core_audit.json"
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 exact char0 core audit PASS", result["logical_sha256"])


if __name__ == "__main__":
    main()
