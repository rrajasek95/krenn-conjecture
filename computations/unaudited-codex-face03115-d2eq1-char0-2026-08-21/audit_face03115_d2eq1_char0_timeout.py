#!/usr/bin/env python3
"""Independent literal-source and timeout replay for 0:31:15, d2=1."""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
PARENT = HERE.parent / "unaudited-codex-face03115-modular-lead-2026-08-21"
SOURCE = PARENT / "export_face03115_base12_f4sat.py"
INPUT = HERE / "face03115_d2eq1_full_source_char0.msolve"
LABELS = HERE / "face03115_d2eq1_full_source_char0_labels.json"
OUTPUT = HERE / "results_face03115_d2eq1_full_source_char0.param.out"
MANIFEST = HERE / "results_face03115_d2eq1_full_source_char0.manifest.json"
TOOLKIT = REPO / "computations/toolkit/groebner/msolve_io.py"
PARAM = REPO / "computations/toolkit/groebner/run_msolve_parametrize.py"
RESULT_PREFIX = HERE / "results_face03115_d2eq1_char0_timeout_replay"
ACTIVE = ("a0", "a1", "a2", "a3", "a4", "a5", "b3", "b5", "d1", "d3")
VARIABLES = ("z", *ACTIVE)
RAW = tuple(index for index in range(6, 22) if index != 16)
INPUT_SHA = "641fc90f837dbfa02b8c6a105a35beadc436ec3c80138fba98450cfdb302c068"
MANIFEST_LOGICAL = "502a6c4d31fd902601d0ef48a44d0af7b018887232782f75ba7120f5b38817fa"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


E = load("face03115_d2eq1_audit_source", SOURCE)
IO = load("face03115_d2eq1_audit_io", TOOLKIT)
sys.path.insert(0, str(TOOLKIT.parent))
P = load("face03115_d2eq1_audit_param", PARAM)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def expression(poly, symbols, reverse=False):
    items = list(poly.items())
    if reverse:
        items.reverse()
    return sp.expand(sp.Add(*(
        coefficient * sp.prod(symbol**power for symbol, power in
                              zip(symbols, exponent, strict=True))
        for exponent, coefficient in items)))


def primitive_numerator(poly, symbols):
    numerator, denominator = sp.fraction(sp.cancel(poly))
    require(denominator != 0, "zero denominator")
    value = sp.Poly(sp.expand(numerator), *symbols, domain=sp.QQ)
    common = math.lcm(*(int(coefficient.q)
                        for _, coefficient in value.terms()))
    integer = sp.Poly(value.as_expr()*common, *symbols, domain=sp.ZZ)
    _, answer = integer.primitive()
    if answer.LC() < 0:
        answer = -answer
    return answer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("standard", "-O", "-I-S"),
                        default="standard")
    args = parser.parse_args()
    reverse = args.mode != "standard"
    require(file_sha(INPUT) == INPUT_SHA, "frozen char0 input changed")
    parsed = IO.read_msolve_input(INPUT, strict=True,
                                  allow_characteristic_zero=True)
    require(parsed.variables == VARIABLES and parsed.characteristic == 0 and
            len(parsed.polynomials) == 16,
            "strict input interface changed")
    labels = json.loads(LABELS.read_text())
    require(tuple(labels["raw_source_indices"]) == RAW and
            labels["eliminated_raw_index"] == 16,
            "literal source label interface changed")

    context, rows, h, *_ = E.raw_source()
    parent_symbols = sp.symbols(" ".join(E.ACTIVE_NAMES))
    parent = dict(zip(E.ACTIVE_NAMES, parent_symbols, strict=True))
    active_symbols = sp.symbols(" ".join(ACTIVE))
    active = dict(zip(ACTIVE, active_symbols, strict=True))
    all_symbols = sp.symbols(" ".join(VARIABLES))
    locals_map = dict(zip(VARIABLES, all_symbols, strict=True))
    active_indices = tuple(context.variable_names.index(name)
                           for name in E.ACTIVE_NAMES)
    source_dicts = {index: E.project(poly, context, active_indices)
                    for index, _, poly in rows if poly}
    source = {index: expression(source_dicts[index], parent_symbols, reverse)
              for index in source_dicts}
    t = active["a5"]*(active["d1"]+1)
    K, N = sp.expand(t+1), sp.expand(t-1)
    substitution = {parent[name]: active[name] for name in ACTIVE}
    substitution[parent["d2"]] = 1
    substitution[parent["b4"]] = N/K
    relation = sp.expand(source[16].subs(parent["d2"], 1))
    Kp = parent["a5"]*(parent["d1"]+1)+1
    require(sp.expand(relation-Kp*(parent["b4"]-1)-2) == 0 and
            sp.cancel(relation.subs(parent["b4"], N/K)) == 0,
            "independent raw16 solve failed")

    input_expressions = [sp.sympify(value.replace("^", "**"),
                                    locals=locals_map)
                         for value in parsed.polynomials]
    row_checks = []
    order = list(enumerate(RAW))
    if reverse:
        order.reverse()
    for position, index in order:
        expected = primitive_numerator(source[index].subs(substitution),
                                       active_symbols)
        actual_full = sp.Poly(input_expressions[position], *all_symbols,
                              domain=sp.ZZ)
        require(all(exponent[0] == 0 for exponent, _ in actual_full.terms()),
                f"raw{index} acquired z")
        actual = sp.Poly(actual_full.as_expr(), *active_symbols, domain=sp.ZZ)
        require(actual == expected, f"raw{index} literal replay failed")
        row_checks.append({"raw_index": index,
                           "terms": len(expected.terms()),
                           "degree": int(expected.total_degree())})

    h_dict = E.project(h, context, active_indices)
    h_num = primitive_numerator(
        expression(h_dict, parent_symbols, reverse).subs(substitution),
        active_symbols).as_expr()
    factors = [K, h_num, active["a5"], active["b3"], N,
               active["a0"], active["a1"], active["a2"], active["a3"],
               active["d1"], active["d3"], 1+active["a0"],
               1+active["a1"]*active["d1"], 1+active["a2"],
               1+active["a3"]*active["d3"]]
    localizer = primitive_numerator(sp.prod(factors), active_symbols).as_expr()
    z = all_symbols[0]
    expected_rab = sp.Poly(z*localizer-1, *all_symbols, domain=sp.ZZ)
    actual_rab = sp.Poly(input_expressions[-1], *all_symbols, domain=sp.ZZ)
    require(expected_rab == actual_rab,
            "full surviving-live Rabinowitsch row replay failed")

    manifest = json.loads(MANIFEST.read_text())
    require(manifest["logical_sha256"] == MANIFEST_LOGICAL and
            manifest["status"] == "timeout" and
            manifest["elapsed_seconds"] >= 600 and
            manifest["returncode"] == -15 and
            manifest["solution"] is None and
            manifest["input"]["sha256"] == INPUT_SHA and
            manifest["timeout_seconds"] == 600,
            "bounded timeout manifest changed")
    require(OUTPUT.is_file() and OUTPUT.stat().st_size == 0,
            "timeout unexpectedly produced a terminal output")
    rejected_zero = False
    try:
        P.parse_parametrization(OUTPUT, 0, len(VARIABLES))
    except ValueError:
        rejected_zero = True
    require(rejected_zero, "zero-byte output was accepted as a sentinel")
    hostile = HERE / ".hostile_positive_dimension.tmp"
    try:
        hostile.write_text(f"[1,{len(VARIABLES)},-1,[]]:\n")
        require(P.parse_parametrization(hostile, 0, len(VARIABLES))["kind"] ==
                "positive_dimensional",
                "positive-dimensional sentinel was accepted as empty")
    finally:
        hostile.unlink(missing_ok=True)

    # Literal source/localizer mutations must disagree with the frozen input.
    mutated_row = -primitive_numerator(source[RAW[0]].subs(substitution),
                                       active_symbols)
    require(mutated_row != sp.Poly(input_expressions[0], *active_symbols),
            "source sign mutation did not fire")
    require(sp.Poly(z*localizer+1, *all_symbols) != actual_rab,
            "Rabinowitsch constant mutation did not fire")
    result = {
        "status": "UNAUDITED exact source replay PASS; char0 gate TIMEOUT",
        "mode": args.mode, "state": "0:31:15", "branch": "d2=1",
        "row_checks": row_checks,
        "restored_omitted_rows": list(E.OMITTED),
        "localizer_terms": len(sp.Poly(localizer, *active_symbols).terms()),
        "localizer_degree": int(sp.total_degree(localizer)),
        "forced_denominator_identity": "raw16=K*(b4-1)+2",
        "input_sha256": INPUT_SHA,
        "manifest_logical_sha256": MANIFEST_LOGICAL,
        "terminal": "600s timeout; zero-byte output; no sentinel",
        "must_fire": ["source sign mutation", "Rabinowitsch constant mutation",
                      "zero-byte output rejection",
                      "positive-dimensional sentinel rejection"],
        "scope_guard": "No algebraic verdict; irreducible R=0 untouched.",
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    suffix = {"standard": "standard", "-O": "O", "-I-S": "I-S"}[args.mode]
    Path(str(RESULT_PREFIX)+"_"+suffix+".json").write_text(
        json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(args.mode, "PASS", result["result_sha256"])


if __name__ == "__main__":
    main()
