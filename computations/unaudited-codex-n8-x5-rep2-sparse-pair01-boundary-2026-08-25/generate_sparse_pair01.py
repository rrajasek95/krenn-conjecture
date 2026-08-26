#!/usr/bin/env python3
"""Generate exact-Q sparse rep2 full-pair01 charts from the sealed core point."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep2-tensor-flattening-2026-08-25"
CORE_SOURCE = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rank1-incidence-gate-2026-08-25/generate_rank1_gate.py"
PINS = {
    PARENT / "MANIFEST.sha256": "16d459603ae0107e0da21ded47b67de62dd289c128667b67bad83bdd36deae1b",
    PARENT / "results_tensor_core_audit.json": "b164264e31b6b3c9341409db79df81cabb3b843db7aae7cf6615715656a16a00",
    CORE_SOURCE: "1fc2a1a62e4092f75cbb330009bbb9649e83e559167f251217a26b7eb3bc7c14",
}
REP2_ADDED = frozenset(((0, 6), (1, 4), (1, 7), (2, 3), (2, 6), (5, 6), (5, 7)))
BASE_LIVE = frozenset((
    "a04_01", "a06_10", "a12_01", "a14_00", "a14_10", "a17_00",
    "a17_10", "a23_01", "a26_01", "a26_12", "a35_01", "a35_10",
    "a67_01", "a67_11", "u0", "v0", "v2",
))


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def load_core():
    spec = importlib.util.spec_from_file_location("rank1_core", CORE_SOURCE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ADDED = REP2_ADDED
    module.NONFIXED = tuple(sorted(module.ADDED | module.VARIABLE))
    module.RETAINED = tuple(edge for edge in module.NONFIXED if edge not in module.ELIMINATED)
    module.SUPPORT = module.FIXED | set(module.NONFIXED)
    module.SUPPORTED = tuple(m for m in module.PM8 if set(m) <= module.SUPPORT)
    assert len(module.SUPPORTED) == 13
    module.SOURCE = {
        (edge, i, j): f"a{edge[0]}{edge[1]}_{i}{j}"
        for edge in module.RETAINED
        for i, j in itertools.product(module.COLORS, repeat=2)
    }
    return module


def build(live, label):
    module = load_core()
    all_amplitude_vars = set(module.SOURCE.values()) | set(module.U) | set(module.V)
    assert set(live) <= all_amplitude_vars
    module.SOURCE = {
        key: value if value in live else "0" for key, value in module.SOURCE.items()
    }
    module.U = tuple(value if value in live else "0" for value in module.U)
    module.V = tuple(value if value in live else "0" for value in module.V)
    equations = []
    word_ledger = []
    for word in itertools.product((0, 1), repeat=8):
        value = module.amplitude(word)
        equation = f"({value})-1" if len(set(word)) == 1 else value
        if equation not in {"0", "(1)-1", "1-1"}:
            equations.append(equation)
            word_ledger.append("".join(map(str, word)))
    word = (2,) * 8
    value = module.amplitude(word)
    equation = f"({value})-1"
    if equation not in {"0", "(1)-1", "1-1"}:
        equations.append(equation)
        word_ledger.append("22222222")
    assert equations
    variables = tuple(sorted(live))
    lines = [
        "option(noredefine);",
        f"ring r=0,({','.join(variables)}),dp;",
        "ideal I=" + ",\n".join(equations) + ";",
        'print("INPUT_GENERATORS="+string(size(I)));',
        "ideal G=slimgb(I);",
        'print("GROEBNER_SIZE="+string(size(G)));',
        "poly remainder=reduce(1,G);",
        'print("UNIT_REMAINDER="+string(remainder));',
        'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT"); print(G); }',
        "quit;",
    ]
    output = HERE / f"rep2_pair01_{label}_Q.sing"
    temporary = output.with_suffix(".sing.tmp")
    temporary.write_text("\n".join(lines) + "\n")
    os.replace(temporary, output)
    return {
        "label": label,
        "path": output.name,
        "sha256": sha256(output),
        "live_variables": list(variables),
        "live_variable_count": len(variables),
        "emitted_equation_count": len(equations),
        "emitted_word_ledger": word_ledger,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--extra", default="")
    parser.add_argument("--label", default="base17")
    args = parser.parse_args()
    for path, digest in PINS.items():
        assert sha256(path) == digest, path
    live = set(BASE_LIVE)
    if args.extra:
        live.add(args.extra)
    result = build(frozenset(live), args.label)
    metadata_path = HERE / f"metadata_{args.label}.json"
    temporary = metadata_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps({
        "schema": "KRENN_X5_REP2_SPARSE_PAIR01_INPUT_V1",
        "parent_pins": {str(path): digest for path, digest in PINS.items()},
        "base_live": sorted(BASE_LIVE),
        "extra": args.extra or None,
        "input": result,
        "scope": "257 pair01 amplitudes only; guard, adjoint, incidence, and rank nonzero are not included",
    }, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, metadata_path)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
