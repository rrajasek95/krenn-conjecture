#!/usr/bin/env python3
"""Export exact-Q branch packet ideals from literal Cramer source data."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIVOT_PATH = (ROOT / "unaudited-codex-root-integration-2026-08-20" /
              "probe_branch0_cycle_d0_c0_pivot.py")
FACTORS_PATH = (ROOT / "unaudited-codex-d0-c0-eliminant-audit-2026-08-21" /
                "results_d0_eliminant_factor_reconstruction.json")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


P = load("d0_exact_branch_packet_pivot", PIVOT_PATH)
sp = P.sp


def singular(poly):
    return str(sp.expand(poly)).replace("**", "^")


def profile(poly, variables):
    p = sp.Poly(poly, *variables)
    return {"terms": len(p.terms()), "total_degree": p.total_degree(),
            "multidegree": [p.degree(v) for v in variables]}


def primitive_factor(record, d1, d4):
    poly = sp.Integer(0)
    for item in record["coefficients"]:
        numerator, denominator = item["coefficient"]
        poly += (sp.Rational(numerator, denominator) *
                 d1**item["d1_degree"] * d4**item["d4_degree"])
    return sp.primitive(sp.Poly(poly, d1, d4).clear_denoms()[1])[1].as_expr()


def main():
    variables, residual, _ = P.P.derive()
    b0, d1, d4, a0, a5 = variables
    equations = [value for _, value in residual]
    matrix, rhs = sp.linear_eq_to_matrix(equations, [a0, a5])
    augmented = matrix.row_join(rhs)
    pivot_rows = (1, 4)
    pivot = sp.primitive(sp.Poly(matrix[list(pivot_rows), :].det(),
                                 b0, d1, d4))[1].as_expr()
    compatibilities = []
    for row in (0, 2, 3, 5):
        value = augmented[[*pivot_rows, row], :].det()
        compatibilities.append(sp.primitive(sp.Poly(value,
            b0, d1, d4))[1].as_expr())

    factor_data = json.loads(FACTORS_PATH.read_text())
    factors = [primitive_factor(record, d1, d4)
               for record in factor_data["factors"]]
    omitted_data = json.loads((HERE / "d0_omitted_rows.json").read_text())
    omitted = {row["source_label"]:
               sp.sympify(row["polynomial"].replace("^", "**"))
               for row in omitted_data["rows"]}
    packets = {
        0: ("cofactor_1_3", "cofactor_2_3", "cofactor_3_3"),
        1: ("cofactor_2_3", "cofactor_3_3", "cofactor_4_3"),
    }
    result = {
        "branches": [],
        "sources": {
            "pivot_exporter": {"path": str(PIVOT_PATH),
                               "sha256": sha256(PIVOT_PATH.read_bytes()).hexdigest()},
            "factor_reconstruction": {"path": str(FACTORS_PATH),
                                      "sha256": sha256(FACTORS_PATH.read_bytes()).hexdigest()},
            "omitted_rows": {"path": "d0_omitted_rows.json",
                             "sha256": sha256((HERE / "d0_omitted_rows.json").read_bytes()).hexdigest()},
        },
    }
    for branch in (0, 1):
        z = sp.Symbol("z")
        rows = compatibilities + [factors[branch]] + [
            omitted[label] for label in packets[branch]]
        localizer = sp.expand(z*pivot - 1)
        script = (
            "ring R=0,(z,b0,d1,d4),dp;\n"
            "ideal I=" + ",\n".join(singular(row) for row in rows) +
            ",\n" + singular(localizer) + ";\n"
            "timer=1; ideal G=slimgb(I); timer=0;\n"
            'print("BEGIN"); print(size(G)); print(dim(G)); '
            'print(string(reduce(1,G))); print("END");\nquit;\n')
        path = HERE / f"d0_factor{branch}_exact_packet.sing"
        path.write_text(script)
        modular_inputs = []
        for prime in (1073741827, 536870909):
            modular = HERE / f"d0_factor{branch}_source_packet_p{prime}.ms"
            modular.write_text(
                "z,b0,d1,d4\n" + str(prime) + "\n" +
                ",\n".join(singular(row) for row in rows + [localizer]) +
                "\n")
            modular_inputs.append({"prime": prime, "path": modular.name,
                                   "sha256": sha256(modular.read_bytes()).hexdigest()})
        result["branches"].append({
            "branch": branch,
            "packet_labels": list(packets[branch]),
            "compatibility_profiles": [profile(row, (b0,d1,d4))
                                           for row in compatibilities],
            "factor_profile": profile(factors[branch], (d1,d4)),
            "omitted_profiles": [profile(omitted[label], (b0,d1,d4))
                                  for label in packets[branch]],
            "pivot_profile": profile(pivot, (b0,d1,d4)),
            "script": path.name,
            "script_sha256": sha256(path.read_bytes()).hexdigest(),
            "modular_inputs": modular_inputs,
        })
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    path = HERE / "results_d0_exact_branch_packet_export.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("exact branch packet export PASS", result["logical_sha256"])


if __name__ == "__main__":
    main()
