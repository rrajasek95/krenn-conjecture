#!/usr/bin/env python3
"""Export exact and two-prime H-live gates for exceptional left-Q divisors."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE / "audit_left_slices_export_mate.py"
H_PATH = (HERE.parent /
          "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
          "export_branch0_cycle_generic_azero_bzero_full_source_hlive_exact.py")
OUT = HERE / "results_left_Q_exception_hlive_export.json"
PRIMES = (1073741827, 1073741789)
EXCEPTIONAL_LEFT_Q = (1, 2, 3, 11, 10, 6, 7)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load("generic_cycle_exception_audit", AUDIT_PATH)
HMOD = load("generic_cycle_exception_h", H_PATH)
BUILDER = AUDIT.BUILDER


def raw_to_sympy(poly, entries):
    result = sp.Integer(0)
    for monomial, coefficient in poly.items():
        term = sp.Rational(coefficient)
        for index in monomial:
            term *= entries[index]
        result += term
    return sp.cancel(result)


def main():
    variables, generators, _, live = BUILDER.derive()
    parameters, entries = AUDIT.raw_left_expressions()
    assert tuple(variables[:-1]) == tuple(parameters)
    lower, _, _, p_solution, a0_solution, a5_solution = \
        HMOD.SOURCE.derive_lower_cofactors()
    del lower
    hcore, _ = HMOD.derive_hcore(p_solution, a0_solution, a5_solution)
    q_polys = tuple(AUDIT.CORE.q_orientation(tuple(
        (index >> (3-site)) & 1 for site in range(4))) for index in range(16))
    q_numerators = {}
    records = []
    for index in EXCEPTIONAL_LEFT_Q:
        expression = raw_to_sympy(q_polys[index], entries)
        numerator, denominator = expression.as_numer_denom()
        numerator = sp.Poly(numerator, *parameters).primitive()[1].as_expr()
        q_numerators[index] = numerator
        rows = (*generators[:-1], numerator,
                sp.expand(variables[-1]*live*hcore-1))
        paths = []
        slice_paths = []
        generic_slice = parameters[2]+2*parameters[4]-3
        for characteristic in (0, *PRIMES):
            tag = "exact" if characteristic == 0 else f"p{characteristic}"
            path = HERE / f"left_Q{index}_Hlive_{tag}.msolve"
            path.write_text(
                ",".join(map(str, variables))+f"\n{characteristic}\n"
                + ",\n".join(BUILDER.SOURCE.SOURCE.encode(poly, variables)
                                for poly in rows)+"\n")
            body = path.read_text().split("\n", 2)[2]
            if "(" in body or "**" in body:
                raise RuntimeError("msolve syntax regression")
            paths.append({
                "characteristic": characteristic,
                "path": path.name,
                "sha256": sha256(path.read_bytes()).hexdigest(),
                "row_count": len(rows),
            })
            sliced_path = HERE / f"left_Q{index}_Hlive_slice_{tag}.msolve"
            sliced_rows = (*rows, generic_slice)
            sliced_path.write_text(
                ",".join(map(str, variables))+f"\n{characteristic}\n"
                + ",\n".join(BUILDER.SOURCE.SOURCE.encode(poly, variables)
                                for poly in sliced_rows)+"\n")
            slice_paths.append({
                "characteristic": characteristic,
                "path": sliced_path.name,
                "sha256": sha256(sliced_path.read_bytes()).hexdigest(),
                "row_count": len(sliced_rows),
                "slice": str(generic_slice),
            })
        profile = sp.Poly(numerator, *parameters)
        records.append({
            "left_Q_index": index,
            "mate_Q_forced": 15-index,
            "numerator_terms": len(profile.terms()),
            "numerator_total_degree": profile.total_degree(),
            "denominator": str(sp.factor(denominator)),
            "inputs": paths,
            "generic_slice_inputs": slice_paths,
        })
    # On the exact component Q5=Q6 and Q9=Q10.  Consequently the two
    # complementary pairs (5,10) and (6,9) lose all left coverage only on the
    # codimension-two intersection Q5=Q10=0, not on either divisor alone.
    intersection_indices = (5, 10)
    intersection_rows = []
    for index in intersection_indices:
        expression = raw_to_sympy(q_polys[index], entries)
        numerator = expression.as_numer_denom()[0]
        intersection_rows.append(
            sp.Poly(numerator, *parameters).primitive()[1].as_expr())
    intersection_inputs = []
    rows = (*generators[:-1], *intersection_rows,
            sp.expand(variables[-1]*live*hcore-1))
    for characteristic in (0, *PRIMES):
        tag = "exact" if characteristic == 0 else f"p{characteristic}"
        path = HERE / f"left_Q5_Q10_Hlive_{tag}.msolve"
        path.write_text(
            ",".join(map(str, variables))+f"\n{characteristic}\n"
            + ",\n".join(BUILDER.SOURCE.SOURCE.encode(poly, variables)
                            for poly in rows)+"\n")
        intersection_inputs.append({
            "characteristic": characteristic,
            "path": path.name,
            "sha256": sha256(path.read_bytes()).hexdigest(),
            "row_count": len(rows),
        })
    # Q15=D0 is already among the original nine chart factors and therefore
    # has no exceptional divisor on this chart.
    q15 = sp.factor(raw_to_sympy(q_polys[15], entries))
    b0, b1, b3, d1, d3, d4 = parameters
    assert sp.cancel(q15-(d1*d4+d3)) == 0
    result = {
        "status": "UNAUDITED exact/two-prime left-Q exceptional H-live exports PASS",
        "records": records,
        "paired_Q5_Q10_exception": {
            "equations": ["Q5=0", "Q10=0"],
            "reason": "Q5=Q6 and Q9=Q10 modulo the exact A=B source ideal",
            "inputs": intersection_inputs,
        },
        "chart_forced_Q15": "D0=d1*d4+d3",
        "localized_factors": (
            "the original nine chart factors and Hcore only; no other left-Q "
            "coordinate and no individual left cofactor is localized"),
        "scope": (
            "Each gate is the full sixteen-row A=B=0 reduced source chart plus "
            "one exceptional selected left-Q divisor, with literal left H "
            "localized. UNIT proves that exceptional divisor is left-H-dead."
        ),
        "source_hashes": {
            "audit": sha256(AUDIT_PATH.read_bytes()).hexdigest(),
            "H_export": sha256(H_PATH.read_bytes()).hexdigest(),
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("left-Q exception H-live export PASS")
    for record in records:
        print(record["left_Q_index"], record["numerator_terms"],
              record["numerator_total_degree"])
    print("result", result["result_sha256"])


if __name__ == "__main__":
    main()
