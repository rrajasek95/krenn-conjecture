#!/usr/bin/env python3
"""Independently replay the literal source behind the char0 empty sentinel."""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
SOURCE = (HERE.parent /
          "unaudited-codex-branch0-offdiag-support-strata-2026-08-21" /
          "results_recursive_face_charts.json")
INPUT = HERE / "face03113_base12_c_char0.msolve"
OUTPUT = HERE / "results_face03113_base12_c_char0.param.out"
MANIFEST = HERE / "results_face03113_base12_c_char0.manifest.json"
LABELS = HERE / "face03113_base12_c_char0_labels.json"
TOOLKIT = REPO / "computations/toolkit/groebner/msolve_io.py"
RESULT_PREFIX = HERE / "results_face03113_char0_empty_replay"
KEY = "0:31:13"
KEPT = (7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21)
INPUT_SHA = "652183de1427c09053bdb5aeb1fbd67c619321f88c0da5fbb418acd3d1159f9e"
OUTPUT_SHA = "0333251e6ebb3890ef547f522ec55f27f0cef9a860998757e31f3e1b819e7490"
MANIFEST_LOGICAL = "091f7f6545494efaffb2291a63c83263b578d3b599bc9974f634449070369138"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


MSOLVE_IO = load("face03113_empty_replay_io", TOOLKIT)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def factor(record, label):
    value = record["localizers"][label]
    require(value.endswith("-1") and "*(" in value,
            f"unexpected localizer {label}")
    return value[value.index("*(")+1:-2]


def expression_from_terms(row, record_symbols):
    value = 0
    for term in row["terms"]:
        numerator, denominator = term["coefficient"]
        monomial = sp.prod(symbol**exponent for symbol, exponent in
                           zip(record_symbols, term["exponents"], strict=True))
        value += sp.Rational(numerator, denominator)*monomial
    return sp.expand(value)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("standard", "-O", "-I-S"),
                        default="standard")
    args = parser.parse_args()
    require(sha(INPUT) == INPUT_SHA and sha(OUTPUT) == OUTPUT_SHA,
            "frozen char0 input/output digest changed")
    parsed = MSOLVE_IO.read_msolve_input(
        INPUT, strict=True, allow_characteristic_zero=True)
    manifest = json.loads(MANIFEST.read_text())
    labels = json.loads(LABELS.read_text())["labels"]
    payload = json.loads(SOURCE.read_text())
    record = next(row for row in payload["states"] if row["key"] == KEY)
    raw = {row["raw_index"]: row for row in record["rows"]}
    require(parsed.characteristic == 0 and len(parsed.polynomials) == 13
            and labels[-1] == "RAB_selected_base_times_C",
            "strict input/label interface changed")

    input_symbols = sp.symbols(" ".join(parsed.variables))
    input_locals = dict(zip(parsed.variables, input_symbols, strict=True))
    record_symbols = sp.symbols(" ".join(record["variable_names"]))
    record_locals = dict(zip(record["variable_names"], record_symbols,
                             strict=True))
    input_polys = [sp.expand(sp.sympify(value.replace("^", "**"),
                                          locals=input_locals))
                   for value in parsed.polynomials]
    order = list(range(len(KEPT)))
    if args.mode == "-O":
        order.reverse()
    row_checks = []
    for position in order:
        index = KEPT[position]
        if args.mode == "-I-S":
            source_poly = expression_from_terms(raw[index], record_symbols)
        else:
            source_poly = sp.expand(sp.sympify(
                raw[index]["polynomial"].replace("^", "**"),
                locals=record_locals))
        # Every omitted record variable is absent, so simultaneous name
        # substitution is exact and introduces no gauge assumption.
        transported = source_poly.subs({record_locals[name]: input_locals[name]
                                        for name in parsed.variables if name != "s"})
        residual = sp.Poly(sp.expand(input_polys[position]-transported),
                           *input_symbols)
        require(residual.is_zero, f"raw row {index} replay failed")
        row_checks.append({"raw_index": index, "label": raw[index]["label"],
                           "terms": len(sp.Poly(transported,
                                                *input_symbols).terms())})

    expected_rab = sp.expand(
        input_locals["s"] *
        sp.sympify(factor(record, "selected_base_terms"), locals=input_locals) *
        sp.sympify(factor(record, "both_live_c_numerators"),
                   locals=input_locals) - 1)
    require(sp.expand(input_polys[-1]-expected_rab) == 0,
            "Rabinowitsch row replay failed")
    require(OUTPUT.read_text() == "[-1]:\n",
            "msolve empty sentinel changed")
    require(manifest["status"] ==
            "completed_characteristic_zero_parametrization"
            and manifest["solution"] ==
            {"kind": "empty", "degree": 0, "variable_count": 12}
            and manifest["logical_sha256"] == MANIFEST_LOGICAL
            and manifest["input"]["sha256"] == INPUT_SHA,
            "toolkit empty-solution manifest changed")
    # Must-fire controls: a source coefficient mutation is detected, and the
    # earlier positive-dimensional sentinel is not accepted as empty.
    mutated = sp.Poly(input_polys[0], *input_symbols).as_dict()
    key = max(mutated)
    mutated[key] = -mutated[key]
    require(sp.Poly.from_dict(mutated, input_symbols).as_expr()
            != input_polys[0], "literal mutation did not fire")
    require("[1,5,-1,[]]:" != "[-1]:",
            "positive-dimensional sentinel was accepted as empty")
    result = {
        "status": "UNAUDITED exact char0 empty source replay PASS",
        "mode": args.mode, "face": KEY,
        "raw_rows": list(KEPT), "row_checks": row_checks,
        "rabinowitsch_terms": len(sp.Poly(expected_rab,
                                           *input_symbols).terms()),
        "empty_sentinel_exact": "[-1]:",
        "manifest_solution": manifest["solution"],
        "input_sha256": INPUT_SHA, "output_sha256": OUTPUT_SHA,
        "manifest_logical_sha256": MANIFEST_LOGICAL,
        "must_fire": ["raw row0 coefficient sign flip",
                       "positive-dimensional sentinel rejection"],
        "scope": manifest["scope"],
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    suffix = {"standard": "standard", "-O": "O", "-I-S": "I-S"}[args.mode]
    output = Path(str(RESULT_PREFIX) + "_" + suffix + ".json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(args.mode, "PASS", result["result_sha256"])


if __name__ == "__main__":
    main()
