#!/usr/bin/env python3
"""Generate a strict modular mixed-word ladder for rep2 cap03/star6."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
SUBSET_GENERATOR = HERE / "generate_incidence_subset_gates.py"
STAGES = ("pure", "distinguished", "pair01", "failed_pairs")


def load_helper():
    specification = importlib.util.spec_from_file_location("rep2_subset_helper", SUBSET_GENERATOR)
    assert specification is not None and specification.loader is not None
    helper = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(helper)
    return helper


def selected(stage):
    pure = {tuple([colour] * 8) for colour in range(3)}
    distinguished = {
        (a, b, b, a, a, a, b, b)
        for a, b in itertools.permutations(range(3), 2)
    }
    pair01 = {word for word in itertools.product((0, 1), repeat=8)}
    failed_pairs = pair01 | {word for word in itertools.product((0, 2), repeat=8)}
    choices = {
        "pure": pure,
        "distinguished": pure | distinguished,
        "pair01": pure | pair01,
        "failed_pairs": pure | failed_pairs,
    }
    return tuple(sorted(choices[stage]))


def build(helper, module, stage):
    words = selected(stage)
    full_equations = []
    records = []
    for word in words:
        value = module.amplitude(word)
        target = int(len(set(word)) == 1)
        full_equations.append(f"({value})-1" if target else value)
        records.append(("".join(map(str, word)), target))
    guard = module.guard_equations()
    adjoint = module.adjoint_equations()
    incidence, incidence_variables = helper.alternate_incidence(module)
    equations = full_equations + guard + adjoint + incidence
    variables = (
        list(module.SOURCE.values()) + list(module.U) + list(module.V)
        + [item for name in "xyz" for item in module.DUAL[name]] + incidence_variables
    )
    assert len(variables) == 105 and len(set(variables)) == 105
    lines = [
        "option(noredefine);",
        f"ring r=32003,({','.join(variables)}),dp;",
        "ideal I=" + ",\n".join(equations) + ";",
        'print("INPUT_GENERATORS="+string(size(I)));',
        "ideal G=slimgb(I);",
        'print("GROEBNER_SIZE="+string(size(G)));',
        "poly remainder=reduce(1,G);",
        'print("UNIT_REMAINDER="+string(remainder));',
        'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_SUBSET"); }',
        "quit;",
    ]
    ledger = hashlib.sha256(json.dumps(records, separators=(",", ":")).encode()).hexdigest()
    return "\n".join(lines) + "\n", {
        "variables": len(variables), "equations": len(equations),
        "selected_full_x5": len(full_equations), "guard": len(guard),
        "adjoint": len(adjoint), "incidence": len(incidence),
        "word_ledger_sha256": ledger,
    }


def atomic_write(path, text):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text)
    os.replace(temporary, path)


def main():
    helper = load_helper()
    module = helper.load_core()
    inputs = {}
    counts = {}
    for stage in STAGES:
        program, count = build(helper, module, stage)
        path = HERE / f"rep2_ladder_cap03_star6_{stage}_p32003.sing"
        atomic_write(path, program)
        inputs[stage] = {"path": path.name, "sha256": hashlib.sha256(program.encode()).hexdigest()}
        counts[stage] = count
    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_REP2_CAP03_INCIDENCE_LADDER_V1",
        "status": "READY_MODULAR_DIAGNOSTIC_ONLY",
        "carrier": {
            "cap": "03", "center": 6,
            "factorization": "A04^T*K*[A23^T|A35]",
            "incidence": ["A04*rho=e0", "A23^T*sigma+A35*tau=e0"],
        },
        "stages": counts,
        "inputs": inputs,
        "logic": {
            "unit": "logically sufficient for the full ideal because every stage is a literal subset of full-X5 plus identical guard/adjoint/incidence equations",
            "nonunit": "diagnostic only",
            "timeout": "zero coverage",
            "Q_policy": "none until a terminal modular unit identifies a sufficient reduced system",
        },
    }
    atomic_write(HERE / "rep2_incidence_ladder_metadata.json", json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "stages": counts}, sort_keys=True))


if __name__ == "__main__":
    main()
