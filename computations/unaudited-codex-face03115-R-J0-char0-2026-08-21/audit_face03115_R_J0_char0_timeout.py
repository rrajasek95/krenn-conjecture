#!/usr/bin/env python3
"""Independent source/hash replay for the R=J=U=0 timeout terminal."""

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
INPUT = HERE / "face03115_R_J0_full_source_char0.msolve"
LABELS = HERE / "face03115_R_J0_full_source_char0_labels.json"
OUTPUT = HERE / "results_face03115_R_J0_full_source_char0.param.out"
MANIFEST = HERE / "results_face03115_R_J0_full_source_char0.manifest.json"
TOOLKIT = REPO / "computations/toolkit/groebner/msolve_io.py"
PARAM = REPO / "computations/toolkit/groebner/run_msolve_parametrize.py"
RESULT_PREFIX = HERE / "results_face03115_R_J0_char0_timeout_replay"
ACTIVE = ("a0", "a1", "a3", "a4", "a5", "b3", "b4", "b5",
          "d1", "d2", "d3")
VARIABLES = ("z", *ACTIVE)
RAW = tuple(index for index in range(6, 22) if index != 16)
INPUT_SHA = "b50c04801f8d63f8251fbd9f05b4b082219ff26b93822ed5570f61657d0ae727"
MANIFEST_LOGICAL = "1eedd0fae291307b4755cf4e9d046432c54ddf5eeec1b8dde888876cd63118b9"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


E = load("face03115_R_J0_audit_source", SOURCE)
IO = load("face03115_R_J0_audit_io", TOOLKIT)
sys.path.insert(0, str(TOOLKIT.parent))
PARAMETRIZE = load("face03115_R_J0_audit_param", PARAM)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def expression(poly, symbols, reverse=False):
    items = list(poly.items())
    if reverse:
        items.reverse()
    return sp.expand(sp.Add(*(
        coefficient * sp.prod(symbol**power for symbol, power in
                              zip(symbols, exponent, strict=True))
        for exponent, coefficient in items)))


def primitive_numerator(poly, symbols):
    numerator, _ = sp.fraction(sp.cancel(poly))
    value = sp.Poly(sp.expand(numerator), *symbols, domain=sp.QQ)
    common = math.lcm(*(int(coefficient.q)
                        for _, coefficient in value.terms()))
    integer = sp.Poly(value.as_expr()*common, *symbols, domain=sp.ZZ)
    _, answer = integer.primitive()
    if answer.LC() < 0:
        answer = -answer
    return answer.as_expr()


def encode(poly, symbols):
    pieces = []
    for position, (exponent, coefficient) in enumerate(
            sp.Poly(sp.expand(poly), *symbols, domain=sp.ZZ).terms()):
        coefficient = int(coefficient)
        symbolic = [str(symbol) + (f"^{power}" if power != 1 else "")
                    for symbol, power in zip(symbols, exponent, strict=True)
                    if power]
        magnitude = abs(coefficient)
        factors = ([str(magnitude)] if magnitude != 1 or not symbolic else [])
        factors.extend(symbolic)
        body = "*".join(factors)
        pieces.append((("-" if coefficient < 0 else "+") if position else
                       ("-" if coefficient < 0 else "")) + body)
    return "".join(pieces)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("standard", "-O", "-I-S"),
                        default="standard")
    args = parser.parse_args()
    reverse = args.mode != "standard"
    require(sha256(INPUT.read_bytes()).hexdigest() == INPUT_SHA,
            "frozen input changed")
    parsed = IO.read_msolve_input(INPUT, strict=True,
                                  allow_characteristic_zero=True)
    require(parsed.variables == VARIABLES and parsed.characteristic == 0 and
            len(parsed.polynomials) == 18,
            "strict char0 interface changed")
    labels = json.loads(LABELS.read_text())
    require(tuple(labels["raw_source_indices"]) == RAW and
            labels["branch_rows"] == ["J", "U"],
            "label interface changed")

    context, rows, h, *_ = E.raw_source()
    parent_symbols = sp.symbols(" ".join(E.ACTIVE_NAMES))
    parent = dict(zip(E.ACTIVE_NAMES, parent_symbols, strict=True))
    active_symbols = sp.symbols(" ".join(ACTIVE))
    active = dict(zip(ACTIVE, active_symbols, strict=True))
    active_indices = tuple(context.variable_names.index(name)
                           for name in E.ACTIVE_NAMES)
    projected = {index: E.project(poly, context, active_indices)
                 for index, _, poly in rows if poly}
    source = {index: expression(poly, parent_symbols, reverse)
              for index, poly in projected.items()}
    pivot = parent["a2"]
    P = sp.Poly(source[16], pivot)
    Q = sp.Poly(source[11], pivot)
    A, B = map(sp.expand, P.all_coeffs())
    C, D = map(sp.expand, Q.all_coeffs())
    R = sp.expand(A*D-B*C)
    substitution = {parent[name]: active[name] for name in ACTIVE}
    A0, B0 = sp.expand(A.subs(substitution)), sp.expand(B.subs(substitution))
    substitution[pivot] = -B0/A0
    require(sp.cancel(source[16].subs(substitution)) == 0,
            "raw16 solve failed")

    expected_rows = []
    for index in RAW:
        expected_rows.append(primitive_numerator(
            source[index].subs(substitution), active_symbols))
    R0 = primitive_numerator(R.subs(substitution), active_symbols)
    require(sp.expand(expected_rows[RAW.index(11)]-R0) == 0 or
            sp.expand(expected_rows[RAW.index(11)]+R0) == 0,
            "raw11/R replay failed")
    a3, a4, a5 = active["a3"], active["a4"], active["a5"]
    b3, b4, b5 = active["b3"], active["b4"], active["b5"]
    d3 = active["d3"]
    J = sp.expand(a4*b4*d3-b3)
    U = sp.expand(2*a3*d3+a5**2*b4**2*d3**2-2*a5*b4*d3+1)
    F = expected_rows[RAW.index(9)]
    S = sp.expand(a3*a4*b4*d3+a3*b3+a4*b4+
                  a5**2*b3*b4**2*d3-2*a5*b3*b4)
    require(sp.expand(F-a5*b3*J*b5-S) == 0 and
            sp.expand(d3*S-b3*U-J*(a3*d3+1)) == 0,
            "raw9 J/U replay failed")

    expected = [encode(poly, active_symbols) for poly in expected_rows]
    expected.extend((encode(J, active_symbols), encode(U, active_symbols)))
    for position in (list(range(17)) if not reverse else
                     list(reversed(range(17)))):
        require(IO.polynomial_sha256(expected[position]) ==
                parsed.polynomial_sha256[position],
                f"literal row hash mismatch at {position}")

    h_dict = E.project(h, context, active_indices)
    h_num = primitive_numerator(
        expression(h_dict, parent_symbols, reverse).subs(substitution),
        active_symbols)
    C2 = sp.expand(A0-B0*active["d2"])
    live = [active["d2"]-1, h_num, active["a5"], active["b3"],
            active["b4"], active["a0"], active["a1"], B0, active["a3"],
            active["d1"], active["d2"], active["d3"], 1+active["a0"],
            1+active["a1"]*active["d1"], C2,
            1+active["a3"]*active["d3"]]
    localizer = primitive_numerator(sp.prod(live), active_symbols)
    z = sp.symbols("z")
    rab = encode(z*localizer-1, sp.symbols(" ".join(VARIABLES)))
    require(IO.polynomial_sha256(rab) == parsed.polynomial_sha256[-1] and
            len(sp.Poly(localizer, *active_symbols).terms()) == 18446,
            "literal localizer hash/profile mismatch")

    manifest = json.loads(MANIFEST.read_text())
    require(manifest["logical_sha256"] == MANIFEST_LOGICAL and
            manifest["status"] == "timeout" and
            manifest["elapsed_seconds"] >= 600 and
            manifest["returncode"] == -15 and
            manifest["solution"] is None and
            manifest["input"]["sha256"] == INPUT_SHA,
            "terminal timeout manifest changed")
    require(OUTPUT.is_file() and OUTPUT.stat().st_size == 0,
            "timeout unexpectedly produced output")
    rejected = False
    try:
        PARAMETRIZE.parse_parametrization(OUTPUT, 0, len(VARIABLES))
    except ValueError:
        rejected = True
    require(rejected, "zero-byte output accepted as sentinel")
    require(IO.polynomial_sha256("-"+expected[0]) !=
            parsed.polynomial_sha256[0] and
            IO.polynomial_sha256(rab.replace("-1", "+1")) !=
            parsed.polynomial_sha256[-1], "mutation guard failed")

    result = {
        "status": "UNAUDITED source replay PASS; exact gate TIMEOUT",
        "mode": args.mode, "branch": "d2-1!=0,R=J=U=0",
        "raw_source_indices": list(RAW), "branch_rows": ["J", "U"],
        "localizer_terms": 18446,
        "input_sha256": INPUT_SHA,
        "manifest_logical_sha256": MANIFEST_LOGICAL,
        "terminal": "600s timeout; zero-byte output; no sentinel",
        "must_fire": ["raw11=R", "raw9 J/U identities",
                      "source sign mutation", "Rabinowitsch mutation",
                      "zero-byte sentinel rejection"],
        "scope_guard": "No algebraic verdict; J!=0 untouched.",
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    suffix = {"standard": "standard", "-O": "O", "-I-S": "I-S"}[args.mode]
    Path(str(RESULT_PREFIX)+"_"+suffix+".json").write_text(
        json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(args.mode, "PASS", result["result_sha256"])


if __name__ == "__main__":
    main()
