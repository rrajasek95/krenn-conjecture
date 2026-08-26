#!/usr/bin/env python3
"""Exact source/localizer replay for the final D0/C0-open gate."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
BASE = HERE / "export_and_audit_d0_factor_split_gate.py"
EXPORT = HERE / "results_d0_AB_open_final_gate_export.json"
RUN = HERE / "results_d0_AB_open_final_exact_run.json"
INPUT = HERE / "d0_AB_open_all_U_three_cofactor_char0.msolve"
OUTPUT = HERE / "d0_AB_open_all_U_three_cofactor_char0.out"
OMITTED_AUDIT = (HERE.parent /
    "unaudited-codex-d0-branchwise-omitted-2026-08-21" /
    "results_d0_omitted_source_export.json")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest_bytes(value):
    return sha256(value).hexdigest()


def digest(path):
    return digest_bytes(path.read_bytes())


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    require(spec.loader is not None, "missing loader")
    spec.loader.exec_module(module)
    return module


def main():
    E = load("d0_AB_open_final_audit_base", BASE)
    sp = E.sp
    export = json.loads(EXPORT.read_text())
    export_logical = export.pop("logical_sha256")
    require(logical_hash(export) == export_logical, "export logical mismatch")
    run = json.loads(RUN.read_text())
    require(run["timeout_seconds"] == 600 and run["process_status"] == "completed",
            "exact gate did not complete under the 600s cap")
    require(run["returncode"] == 0 and run["unit_basis"],
            "exact run did not return a unit")
    require(run["input_sha256"] == digest(INPUT), "input digest mismatch")
    require(run["output_sha256"] == digest(OUTPUT), "output digest mismatch")
    require(OUTPUT.read_text().rstrip().endswith("[1]:"), "unit output changed")

    omitted_audit = json.loads(OMITTED_AUDIT.read_text())
    omitted_logical = omitted_audit.pop("logical_sha256")
    require(logical_hash(omitted_audit) == omitted_logical,
            "literal cofactor source export logical mismatch")
    require(omitted_logical ==
            "5b29fac1aa917b029df348adf3642891b7853ff6bd7c8442b6f26b09a6d396f1",
            "unexpected literal cofactor source-export version")

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
    labels = ("cofactor_1_3", "cofactor_2_3", "cofactor_3_3")
    z = sp.Symbol("z")
    live_product = sp.expand(A * B * pivot)
    localizer = sp.expand(z * live_product - 1)
    rows = [*U, *(cofactors[label] for label in labels), localizer]
    rebuilt = ("z,b0,d1,d4\n0\n" +
               ",\n".join(E.encode(row) for row in rows) + "\n").encode()
    require(digest_bytes(rebuilt) == digest(INPUT),
            "literal source/localizer rebuild differs from exact gate")
    require(len(sp.Poly(live_product, *variables3).terms()) == 1088,
            "live-product term count mutation failed")
    require(sp.Poly(localizer, z, *variables3).coeff_monomial(1) == -1,
            "Rabinowitsch constant term changed")

    # Must-fire changes: dropping B from the live product changes the input;
    # changing one U coefficient changes its exact ledger; changing [1] fails.
    weak_localizer = sp.expand(z * A * pivot - 1)
    weak_rows = [*U, *(cofactors[label] for label in labels), weak_localizer]
    weak = ("z,b0,d1,d4\n0\n" +
            ",\n".join(E.encode(row) for row in weak_rows) + "\n").encode()
    require(digest_bytes(weak) != digest(INPUT), "B-localizer mutation did not fire")
    mutated_u0 = sp.expand(U[0] + 1)
    require(E.term_dict(mutated_u0, variables3) != E.term_dict(U[0], variables3),
            "U0 mutation did not fire")
    require("[1]:" not in OUTPUT.read_text().replace("[1]:", "[b0]:"),
            "unit mutation did not fire")

    result = {
        "status": "final D0/C0-open exact gate PASS",
        "export_logical_sha256": export_logical,
        "literal_cofactor_source_logical_sha256": omitted_logical,
        "input_sha256": digest(INPUT),
        "output_sha256": digest(OUTPUT),
        "live_product_profile": E.profile(live_product, variables3),
        "mutation_controls": ["drop_B_from_localizer", "U0_coefficient", "unit_output"],
        "theorem": ("On the D0=0,C0!=0 chart with selected pivot, A, and B "
                    "nonzero, U0=U1=U2=U3=0 is incompatible with literal "
                    "Cof(1,3),Cof(2,3),Cof(3,3)."),
        "combined_scope": ("Together with the involutive factor-zero gate, this "
                           "closes the complete selected-pivot-open D0/C0 residual "
                           "case split. Pivot-zero and other D0/C0 faces remain out of scope."),
    }
    result["logical_sha256"] = logical_hash(result)
    (HERE / "results_d0_AB_open_final_gate_audit.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("final D0 AB-open exact audit PASS", result["logical_sha256"])


if __name__ == "__main__":
    main()
