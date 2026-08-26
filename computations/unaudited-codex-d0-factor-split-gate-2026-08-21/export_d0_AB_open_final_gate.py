#!/usr/bin/env python3
"""Export the sole remaining D0/C0-open exact gate."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
BASE_EXPORTER = HERE / "export_and_audit_d0_factor_split_gate.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    if spec.loader is None:
        raise RuntimeError("missing module loader")
    spec.loader.exec_module(module)
    return module


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main():
    E = load("d0_AB_open_base_exporter", BASE_EXPORTER)
    sp = E.sp
    variables, residual, _ = E.P.P.derive()
    b0, d1, d4, a0, a5 = variables
    variables3 = (b0, d1, d4)
    equations = [value for _, value in residual]
    matrix, _ = sp.linear_eq_to_matrix(equations, [a0, a5])
    pivot = sp.primitive(sp.Poly(matrix[[1, 4], :].det(),
                                 *variables3))[1].as_expr()
    factors = json.loads(E.FACTOR_RESULT.read_text())["exact_pairwise_factorization"]
    A = E.decode_ledger(factors["A"], *variables3)
    B = E.decode_ledger(factors["B"], *variables3)
    U = [E.decode_ledger(row, *variables3)
         for row in factors["reduced_rows_U0_U1_U2_U3"]]
    omitted_json = json.loads(E.OMITTED.read_text())
    cofactors = {row["source_label"]:
                 sp.sympify(row["polynomial"].replace("^", "**"))
                 for row in omitted_json["rows"]}
    packet = ("cofactor_1_3", "cofactor_2_3", "cofactor_3_3")
    z = sp.Symbol("z")
    live_product = sp.expand(A * B * pivot)
    localizer = sp.expand(z * live_product - 1)
    rows = [*U, *(cofactors[label] for label in packet), localizer]
    input_path = HERE / "d0_AB_open_all_U_three_cofactor_char0.msolve"
    input_path.write_text("z,b0,d1,d4\n0\n" +
                          ",\n".join(E.encode(row) for row in rows) + "\n")
    result = {
        "input": input_path.name,
        "input_sha256": digest(input_path),
        "rows": ["U0", "U1", "U2", "U3", *packet,
                 "z*A*B*selected_pivot-1"],
        "row_profiles": [E.profile(row, (z, *variables3)) for row in rows],
        "live_product_profile": E.profile(live_product, variables3),
        "source_hashes": {
            "base_exporter": digest(BASE_EXPORTER),
            "raw_reduced_source": digest(E.SOURCE),
            "factor_result": digest(E.FACTOR_RESULT),
            "literal_cofactor_export": digest(E.OMITTED),
        },
        "scope": ("Sole remaining selected-pivot-open D0/C0 residual: "
                  "A*B!=0 and U0=U1=U2=U3=0, with literal cofactor packet 1,2,3."),
    }
    result["logical_sha256"] = logical_hash(result)
    (HERE / "results_d0_AB_open_final_gate_export.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 AB-open final gate export PASS", result["logical_sha256"])
    print("input", input_path.name, input_path.stat().st_size, "bytes")
    print("live product", result["live_product_profile"])


if __name__ == "__main__":
    main()
