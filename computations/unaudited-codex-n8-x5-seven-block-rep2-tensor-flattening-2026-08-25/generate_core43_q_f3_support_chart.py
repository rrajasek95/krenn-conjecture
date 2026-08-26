#!/usr/bin/env python3
"""Exact-Q chart on the nonzero support of the literal F3 core43 model."""

from __future__ import annotations

import importlib.util
import itertools
import json
import os
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_PATH = (
    HERE.parent / "unaudited-codex-n8-x5-seven-block-rank1-incidence-gate-2026-08-25"
    / "generate_rank1_gate.py"
)
REP2_ADDED = frozenset(((0, 6), (1, 4), (1, 7), (2, 3), (2, 6), (5, 6), (5, 7)))


def load():
    spec = importlib.util.spec_from_file_location("rank1_core", SOURCE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ADDED = REP2_ADDED
    module.NONFIXED = tuple(sorted(module.ADDED | module.VARIABLE))
    module.RETAINED = tuple(edge for edge in module.NONFIXED if edge not in module.ELIMINATED)
    module.SUPPORT = module.FIXED | set(module.NONFIXED)
    module.SUPPORTED = tuple(m for m in module.PM8 if set(m) <= module.SUPPORT)
    module.SOURCE = {
        (edge, i, j): f"a{edge[0]}{edge[1]}_{i}{j}"
        for edge in module.RETAINED
        for i, j in itertools.product(module.COLORS, repeat=2)
    }
    return module


def main():
    module = load()
    model_text = (HERE / "rep2_core43_f3.stdout").read_text()
    model = {
        match.group(1): int(match.group(2), 16)
        for match in re.finditer(
            r"\(define-fun (\w+) \(\) \(_ BitVec 8\)\s+#x([0-9a-f]+)\)", model_text
        )
    }
    amplitude_variables = set(module.SOURCE.values()) | set(module.U) | set(module.V)
    live = tuple(sorted(name for name in amplitude_variables if model.get(name, 0) != 0))
    assert len(live) == 19
    module.SOURCE = {
        key: value if value in live else "0" for key, value in module.SOURCE.items()
    }
    module.U = tuple(value if value in live else "0" for value in module.U)
    module.V = tuple(value if value in live else "0" for value in module.V)
    core = json.loads((HERE / "results_f2_core43.json").read_text())
    equations = []
    for raw_word in core["amplitude_words"]:
        word = tuple(map(int, raw_word))
        value = module.amplitude(word)
        equations.append(f"({value})-1" if word == (0,) * 8 else value)
    lines = [
        "option(noredefine);",
        f"ring r=0,({','.join(live)}),dp;",
        "ideal I=" + ",\n".join(equations) + ";",
        'print("INPUT_GENERATORS="+string(size(I)));',
        "ideal G=slimgb(I);",
        'print("GROEBNER_SIZE="+string(size(G)));',
        "poly remainder=reduce(1,G);",
        'print("UNIT_REMAINDER="+string(remainder));',
        'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT"); print(G); }',
        "quit;",
    ]
    output = HERE / "rep2_core43_f3_support_chart_Q.sing"
    temporary = output.with_suffix(".sing.tmp")
    temporary.write_text("\n".join(lines) + "\n")
    os.replace(temporary, output)
    metadata = {
        "schema": "KRENN_X5_REP2_CORE43_F3_SUPPORT_Q_CHART_V1",
        "live_variables": list(live),
        "live_variable_count": len(live),
        "equation_count": len(equations),
        "f3_model_values": {name: model[name] for name in live},
        "scope": "zero-pattern chart only; a nonunit Q result disproves a characteristic-zero core43 identity",
    }
    path = HERE / "core43_f3_support_chart_metadata.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)
    print(json.dumps({"variables": len(live), "equations": len(equations)}, sort_keys=True))


if __name__ == "__main__":
    main()
