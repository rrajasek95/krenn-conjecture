#!/usr/bin/env python3
"""Lift the deletion-minimal F2 amplitude core verbatim to odd p and Q."""

from __future__ import annotations

import importlib.util
import itertools
import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent
CORE = HERE / "results_f2_core43.json"
SEALED_CORE = (
    HERE.parent / "unaudited-codex-n8-x5-seven-block-rank1-incidence-gate-2026-08-25"
    / "generate_rank1_gate.py"
)
REP2_ADDED = frozenset(((0, 6), (1, 4), (1, 7), (2, 3), (2, 6), (5, 6), (5, 7)))


def load_module():
    spec = importlib.util.spec_from_file_location("rank1_core", SEALED_CORE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ADDED = REP2_ADDED
    module.NONFIXED = tuple(sorted(module.ADDED | module.VARIABLE))
    module.RETAINED = tuple(edge for edge in module.NONFIXED if edge not in module.ELIMINATED)
    module.SUPPORT = module.FIXED | set(module.NONFIXED)
    module.SUPPORTED = tuple(matching for matching in module.PM8 if set(matching) <= module.SUPPORT)
    assert len(module.SUPPORTED) == 13
    module.SOURCE = {
        (edge, i, j): f"a{edge[0]}{edge[1]}_{i}{j}"
        for edge in module.RETAINED
        for i, j in itertools.product(module.COLORS, repeat=2)
    }
    return module


def main():
    module = load_module()
    core = json.loads(CORE.read_text())
    words = [tuple(map(int, word)) for word in core["amplitude_words"]]
    assert len(words) == 43 and words[0] == (0,) * 8
    equations = []
    for word in words:
        value = module.amplitude(word)
        equations.append(f"({value})-1" if word == (0,) * 8 else value)
    variables = list(module.SOURCE.values()) + list(module.U) + list(module.V)
    assert len(variables) == 87
    generated = {}
    for label, coefficient_ring in (("p32003", "32003"), ("Q", "0")):
        lines = [
            "option(noredefine);",
            f"ring r={coefficient_ring},({','.join(variables)}),dp;",
            "ideal I=" + ",\n".join(equations) + ";",
            'print("INPUT_GENERATORS="+string(size(I)));',
            "ideal G=slimgb(I);",
            'print("GROEBNER_SIZE="+string(size(G)));',
            "poly remainder=reduce(1,G);",
            'print("UNIT_REMAINDER="+string(remainder));',
            'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT"); }',
            "quit;",
        ]
        path = HERE / f"rep2_core43_{label}.sing"
        temporary = path.with_suffix(".sing.tmp")
        temporary.write_text("\n".join(lines) + "\n")
        os.replace(temporary, path)
        generated[label] = path.name
    result = {
        "schema": "KRENN_X5_REP2_CORE43_ODD_Q_LIFT_INPUT_V1",
        "source_core": CORE.name,
        "source_generator": str(SEALED_CORE),
        "equation_count": len(equations),
        "variable_count": len(variables),
        "inputs": generated,
        "logical_scope": "same 43 amplitude equations; no Boolean field equations, guard, incidence, adjoint, or rank assertions",
    }
    path = HERE / "core43_lift_metadata.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
