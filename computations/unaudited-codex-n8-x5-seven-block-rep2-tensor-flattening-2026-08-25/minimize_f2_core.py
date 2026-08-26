#!/usr/bin/env python3
"""Extract, deletion-check, and proof-log the exact 43-amplitude F2 core."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
SEARCH = HERE / "search_pair01_f2.py"
CORE_STDOUT = HERE / "rep2_pair01_rank1_f2.stdout"


def load_search():
    spec = importlib.util.spec_from_file_location("pair01_f2", SEARCH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def declarations(module):
    variables = (
        list(module.SOURCE.values())
        + list(module.U)
        + list(module.V)
        + [item for name in "xyz" for item in module.DUAL[name]]
        + list(module.RHO)
        + list(module.SIGMA)
        + [module.TAU]
    )
    return variables, [f"(declare-const {variable} Bool)" for variable in variables]


def run_z3(text, timeout=10):
    process = subprocess.run(
        ["z3", f"-T:{timeout}", "-in"], input=text, capture_output=True,
        text=True, timeout=timeout + 3,
    )
    return process.returncode, process.stdout + process.stderr


def main():
    module = load_search()
    equations, labels = module.constraints()
    by_name = {
        f"c_{index}_{label}": (index, label, equation)
        for index, (label, equation) in enumerate(zip(labels, equations))
    }
    raw = CORE_STDOUT.read_text()
    names = re.findall(r"c_\d+_amp_[012]+", raw)
    assert len(names) == 43 == len(set(names))
    assert all(name in by_name for name in names)
    # Canonicalize by the amplitude-word index, independent of Z3 core order.
    names.sort(key=lambda name: by_name[name][0])
    variables, decls = declarations(module)

    def core_text(kept, proof=False):
        lines = []
        if proof:
            lines.extend((
                "(set-option :produce-proofs true)",
                "(set-option :proof true)",
            ))
        lines.extend(decls)
        for name in kept:
            _, _, equation = by_name[name]
            lines.append(f"(assert (not {equation}))")
        lines.append("(check-sat)")
        if proof:
            lines.append("(get-proof)")
        return "\n".join(lines) + "\n"

    rc, output = run_z3(core_text(names), timeout=10)
    assert rc == 0 and output.splitlines()[0] == "unsat", output
    deletion = []
    for position, dropped in enumerate(names):
        kept = names[:position] + names[position + 1 :]
        rc, output = run_z3(core_text(kept), timeout=10)
        status = next(
            (line for line in output.splitlines() if line in {"sat", "unsat", "unknown", "timeout"}),
            "NO_STATUS",
        )
        deletion.append({"dropped": dropped, "returncode": rc, "status": status})
        assert rc == 0 and status == "sat", (dropped, rc, output[:1000])

    proof_input = HERE / "rep2_pair01_f2_core43_proof.smt2"
    temporary = proof_input.with_suffix(".smt2.tmp")
    temporary.write_text(core_text(names, proof=True))
    os.replace(temporary, proof_input)
    process = subprocess.run(
        ["z3", str(proof_input)], capture_output=True, text=True, timeout=30
    )
    proof_output = process.stdout + process.stderr
    assert process.returncode == 0 and proof_output.splitlines()[0] == "unsat"
    proof_path = HERE / "rep2_pair01_f2_core43_proof.stdout"
    temporary = proof_path.with_suffix(".stdout.tmp")
    temporary.write_text(proof_output)
    os.replace(temporary, proof_path)

    result = {
        "schema": "KRENN_X5_REP2_PAIR01_F2_MINIMAL_CORE_V1",
        "status": "PASS_EXACT_F2_DELETION_MINIMAL_UNSAT_CORE",
        "field": 2,
        "core_size": len(names),
        "amplitude_words": [by_name[name][1].removeprefix("amp_") for name in names],
        "target_one_words": [
            by_name[name][1].removeprefix("amp_") for name in names
            if by_name[name][1] == "amp_00000000"
        ],
        "deletion_checks": deletion,
        "z3_proof_check_enabled": True,
        "proof_input": proof_input.name,
        "proof_output": proof_path.name,
        "variables_declared": len(variables),
        "scope": "characteristic two only; no guard, incidence, adjoint, or rank assertion occurs in the core",
    }
    output_path = HERE / "results_f2_core43.json"
    temporary = output_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output_path)
    print(json.dumps({
        "status": result["status"],
        "core_size": result["core_size"],
        "deletion_sat": sum(item["status"] == "sat" for item in deletion),
        "proof_bytes": len(proof_output.encode()),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
