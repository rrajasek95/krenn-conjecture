#!/usr/bin/env python3
"""Build deterministic modular generic slices of the full-source A=B=0 curve."""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
SOURCE_PATH = (HERE.parent /
               "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
               "export_branch0_cycle_generic_azero_bzero_full_source_exact.py")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load("generic_cycle_mate_slice_source", SOURCE_PATH)


def derive():
    rows, labels, metadata = SOURCE.SOURCE.SOURCE.derive()
    source_rows = tuple(rows[:6])
    b0, b1, b3, d1, d3, d4 = SOURCE.SOURCE.SOURCE.SOURCE.PARAMETERS
    normalized_t013 = sp.cancel(source_rows[1]/d4)
    A = sp.cancel(sp.diff(normalized_t013, b3)/(2*b0))
    B = sp.cancel(normalized_t013.subs(b3, 0)/2)
    lower, _, _, _, _, _ = SOURCE.derive_lower_cofactors()
    delta = b1*d3+b3*d1*d4
    d0 = d1*d4+d3
    bplus = b1+d1
    live = sp.expand(b0*b1*b3*d1*d3*d4*delta*d0*bplus)
    z = sp.Symbol("z")
    variables = (*SOURCE.SOURCE.SOURCE.SOURCE.PARAMETERS, z)
    generators = (*source_rows, A, B,
                  lower[1], lower[2], lower[4], lower[5],
                  sp.expand(z*live-1))
    return variables, generators, labels, live


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=1009)
    parser.add_argument("--slice-count", type=int, default=1)
    args = parser.parse_args()
    variables, generators, labels, live = derive()
    b0, b1, b3, d1, d3, d4, _ = variables
    slices = (
        b0+2*b1+3*b3+5*d1+7*d3+11*d4-13,
        17*b0+19*b1+23*b3+29*d1+31*d3+37*d4-41,
        43*b0+47*b1+53*b3+59*d1+61*d3+67*d4-71,
    )
    if not 0 <= args.slice_count <= len(slices):
        raise ValueError("slice count out of range")
    all_rows = (*generators, *slices[:args.slice_count])
    out = HERE / f"left_AB0_slice{args.slice_count}_p{args.prime}.msolve"
    out.write_text(
        ",".join(map(str, variables))+f"\n{args.prime}\n"
        + ",\n".join(SOURCE.SOURCE.encode(poly, variables)
                       for poly in all_rows)+"\n")
    body = out.read_text().split("\n", 2)[2]
    if "(" in body or "**" in body:
        raise RuntimeError("msolve syntax regression")
    result = {
        "status": "UNAUDITED deterministic modular left generic slice export",
        "prime": args.prime,
        "slice_count": args.slice_count,
        "variables": [str(value) for value in variables],
        "source_row_count": len(generators),
        "slice_rows": [str(value) for value in slices[:args.slice_count]],
        "input": out.name,
        "input_sha256": sha256(out.read_bytes()).hexdigest(),
        "source_export_sha256": sha256(SOURCE_PATH.read_bytes()).hexdigest(),
        "live_factor_terms": len(sp.Poly(live, *variables[:-1]).terms()),
        "scope": (
            "Full sixteen-literal-row A=B=0 reduced chart, original nine "
            "factors live, with deterministic affine slicing; left H is not "
            "localized or inferred."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    (HERE / f"results_left_AB0_slice{args.slice_count}_p{args.prime}.json").write_text(
        json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("left A=B=0 generic slice export PASS", out)
    print("rows", len(all_rows), "result", result["result_sha256"])


if __name__ == "__main__":
    main()
