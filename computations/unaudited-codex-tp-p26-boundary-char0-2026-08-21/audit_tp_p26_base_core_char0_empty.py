#!/usr/bin/env python3
"""Independent exact replay of the TP P26=0 characteristic-zero empty gate."""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
SOURCE_DIR = (HERE.parent /
              "unaudited-codex-n8-orbit0-normalized-78-2026-08-20")
DISCOVERY = SOURCE_DIR / "discover_branch0_triangle_pendant_reduction.py"
ROW_CORE = SOURCE_DIR / "results_branch0_triangle_pendant_p26_base_row_core.json"
INPUT = HERE / "tp_p26_base_core_char0.msolve"
OUTPUT = HERE / "results_tp_p26_base_core_char0.param.out"
MANIFEST = HERE / "results_tp_p26_base_core_char0.manifest.json"
LABELS = HERE / "tp_p26_base_core_char0_labels.json"
TOOLKIT = REPO / "computations/toolkit/groebner/msolve_io.py"
PARAM_RUNNER = REPO / "computations/toolkit/groebner/run_msolve_parametrize.py"
RESULT_PREFIX = HERE / "results_tp_p26_base_core_char0_replay"
CORE_LABELS = (7, 8, 9, 10, 12, 15, 19, 101)
ACTIVE_NAMES = ("a4", "a5", "b0", "b1", "b3", "d4", "d5")
VARIABLE_NAMES = ("z", *ACTIVE_NAMES)
INPUT_SHA = "62540e25e6dd53a668e48bef2af2f0fe4dcbcd0008138b1f210ae1af9d2523f6"
OUTPUT_SHA = "0333251e6ebb3890ef547f522ec55f27f0cef9a860998757e31f3e1b819e7490"
MANIFEST_LOGICAL = "62019cf3279c50d713b276bd28bcf0abbcb4b6658f342dfae1f8a8316602a2aa"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


D = load("tp_p26_empty_exact_source", DISCOVERY)
C = D.CHART
MSOLVE_IO = load("tp_p26_empty_msolve_io", TOOLKIT)
sys.path.insert(0, str(TOOLKIT.parent))
PARAM = load("tp_p26_empty_param_runner", PARAM_RUNNER)
ACTIVE_INDICES = tuple(C.names.index(name) for name in ACTIVE_NAMES)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path: Path):
    return sha256(path.read_bytes()).hexdigest()


def primitive_project(poly, reverse=False):
    """Independently clear content and project a source dictionary."""
    require(poly, "zero source row")
    values = list(poly.values())
    denominator = math.lcm(*(value.denominator for value in values))
    integers = [value.numerator * (denominator // value.denominator)
                for value in values]
    content = math.gcd(*map(abs, integers))
    items = list(poly.items())
    if reverse:
        items.reverse()
    answer = {}
    sign = -1 if poly[min(poly)] < 0 else 1
    for exponent, value in items:
        require(all(exponent[index] == 0 for index in range(C.n)
                    if index not in ACTIVE_INDICES),
                ("source row escaped active variables", exponent))
        key = tuple(exponent[index] for index in ACTIVE_INDICES)
        coefficient = sign * value.numerator * (
            denominator // value.denominator) // content
        require(key not in answer and coefficient != 0,
                "projected source collision/zero")
        answer[key] = coefficient
    return answer


def sympy_dict(expression, symbols):
    return {tuple(monomial): int(coefficient)
            for monomial, coefficient in
            sp.Poly(sp.expand(expression), *symbols).terms()}


def expected_base():
    b0 = C.variable(C.names.index("b0"))
    b1 = C.variable(C.names.index("b1"))
    b3 = C.variable(C.names.index("b3"))
    d4 = C.variable(C.names.index("d4"))
    d5 = C.variable(C.names.index("d5"))
    return C.multiply(b0, b1, b3, d4, d5,
                      C.add(C.multiply(b1, d4), C.multiply(b0, d5)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("standard", "-O", "-I-S"),
                        default="standard")
    args = parser.parse_args()
    require(file_sha(INPUT) == INPUT_SHA and file_sha(OUTPUT) == OUTPUT_SHA,
            "frozen char0 input/output digest changed")
    parsed = MSOLVE_IO.read_msolve_input(
        INPUT, strict=True, allow_characteristic_zero=True)
    require(parsed.variables == VARIABLE_NAMES and parsed.characteristic == 0
            and len(parsed.polynomials) == 9,
            "strict input interface changed")
    labels = json.loads(LABELS.read_text())
    require(tuple(labels["source_labels"]) == CORE_LABELS and
            labels["labels"][-1] == "RAB_F0",
            "source labels changed")
    frozen_core = json.loads(ROW_CORE.read_text())
    require(tuple(frozen_core["final_labels"]) == CORE_LABELS,
            "two-prime core labels changed")

    data = D.cramer_branch_system(7, 12)
    all_rows = {label: poly for label, poly in data["closed_rows"]}
    active_symbols = sp.symbols(" ".join(ACTIVE_NAMES))
    input_symbols = sp.symbols(" ".join(VARIABLE_NAMES))
    input_locals = dict(zip(VARIABLE_NAMES, input_symbols, strict=True))
    input_polys = [sp.expand(sp.sympify(value.replace("^", "**"),
                                          locals=input_locals))
                   for value in parsed.polynomials]
    order = list(range(len(CORE_LABELS)))
    if args.mode == "-O":
        order.reverse()
    row_checks = []
    for position in order:
        label = CORE_LABELS[position]
        expected = primitive_project(
            all_rows[label], reverse=args.mode in ("-O", "-I-S"))
        actual_full = sympy_dict(input_polys[position], input_symbols)
        require(all(exponent[0] == 0 for exponent in actual_full),
                f"source {label} acquired z")
        actual = {exponent[1:]: coefficient
                  for exponent, coefficient in actual_full.items()}
        require(actual == expected,
                f"literal monomial/coefficient replay failed for {label}")
        row_checks.append({
            "label": label, "terms": len(expected),
            "degree": max(map(sum, expected)),
            "dictionary_sha256": sha256(json.dumps(
                sorted((list(key), value) for key, value in expected.items()),
                separators=(",", ":")).encode()).hexdigest(),
        })

    base_from_system = data["closed_live_factors"][0]
    explicit_base = expected_base()
    require(C.add(base_from_system, C.scale(explicit_base, -1)) == {},
            "system F0 differs from explicit factor product")
    base = primitive_project(explicit_base,
                             reverse=args.mode in ("-O", "-I-S"))
    z = input_symbols[0]
    expected_rab = z * sp.Add(*(
        coefficient * sp.prod(symbol**power for symbol, power in
                              zip(active_symbols, exponent, strict=True))
        for exponent, coefficient in base.items())) - 1
    require(sympy_dict(input_polys[-1], input_symbols) ==
            sympy_dict(expected_rab, input_symbols),
            "expanded Rabinowitsch row replay failed")
    require(set(base) == {(0, 0, 1, 2, 1, 2, 1),
                          (0, 0, 2, 1, 1, 1, 2)}
            and set(base.values()) == {1},
            "literal F0 expansion changed")

    manifest = json.loads(MANIFEST.read_text())
    require(OUTPUT.read_text() == "[-1]:\n",
            "literal msolve empty sentinel changed")
    require(PARAM.parse_parametrization(OUTPUT, 0, 8) ==
            {"kind": "empty", "degree": 0, "variable_count": 8},
            "toolkit did not parse literal char0 empty sentinel")
    require(manifest["status"] ==
            "completed_characteristic_zero_parametrization"
            and manifest["solution"] ==
            {"kind": "empty", "degree": 0, "variable_count": 8}
            and manifest["logical_sha256"] == MANIFEST_LOGICAL
            and manifest["input"]["sha256"] == INPUT_SHA,
            "toolkit result manifest changed")

    # Sentinel must-fire: positive-dimensional output is not emptiness and
    # the historical char0 `[1]` discovery is rejected as malformed.
    hostile_positive = HERE / ".hostile_positive_dimension.tmp"
    hostile_one = HERE / ".hostile_one.tmp"
    try:
        hostile_positive.write_text("[1,8,-1,[]]:\n")
        hostile_one.write_text("[1]:\n")
        require(PARAM.parse_parametrization(hostile_positive, 0, 8)["kind"] ==
                "positive_dimensional",
                "positive-dimensional sentinel was accepted as empty")
        rejected_one = False
        try:
            PARAM.parse_parametrization(hostile_one, 0, 8)
        except ValueError:
            rejected_one = True
        require(rejected_one, "historical char0 [1] was accepted")
    finally:
        hostile_positive.unlink(missing_ok=True)
        hostile_one.unlink(missing_ok=True)

    # Literal mutation guards fire independently on a source coefficient and
    # on one of the two F0 monomials.
    mutated_row = dict(primitive_project(all_rows[7]))
    row_key = max(mutated_row, key=lambda item: (sum(item), item))
    mutated_row[row_key] *= -1
    actual_row0 = {exponent[1:]: coefficient for exponent, coefficient in
                   sympy_dict(input_polys[0], input_symbols).items()}
    require(mutated_row != actual_row0 and
            primitive_project(all_rows[7]) == actual_row0,
            "source-row mutation did not fire against literal input")
    mutated_base = dict(base)
    base_key = max(mutated_base)
    mutated_base[base_key] *= -1
    mutated_rab = z * sp.Add(*(
        coefficient * sp.prod(symbol**power for symbol, power in
                              zip(active_symbols, exponent, strict=True))
        for exponent, coefficient in mutated_base.items())) - 1
    require(sympy_dict(mutated_rab, input_symbols) !=
            sympy_dict(input_polys[-1], input_symbols),
            "localizer mutation did not fire against literal input")

    result = {
        "status": "UNAUDITED exact char0 empty source replay PASS",
        "mode": args.mode,
        "branch": "triangle-plus-pendant P26=0",
        "source_labels": list(CORE_LABELS),
        "row_checks": row_checks,
        "base_factor": "b0*b1*b3*d4*d5*(b1*d4+b0*d5)",
        "base_factor_dictionary": sorted(
            (list(key), value) for key, value in base.items()),
        "rabinowitsch_terms": len(base) + 1,
        "empty_sentinel_exact": "[-1]:",
        "manifest_solution": manifest["solution"],
        "input_sha256": INPUT_SHA,
        "output_sha256": OUTPUT_SHA,
        "manifest_logical_sha256": MANIFEST_LOGICAL,
        "must_fire": [
            "source row7 leading-coefficient sign mutation",
            "F0 monomial-coefficient sign mutation",
            "positive-dimensional sentinel rejection",
            "historical characteristic-zero [1] rejection",
        ],
        "scope": manifest["scope"],
        "excludes": ["P26!=0", "N5^3", "triangle-pendant closure without F0"],
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    suffix = {"standard": "standard", "-O": "O", "-I-S": "I-S"}[args.mode]
    output = Path(str(RESULT_PREFIX) + "_" + suffix + ".json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(args.mode, "PASS", result["result_sha256"])


if __name__ == "__main__":
    main()
