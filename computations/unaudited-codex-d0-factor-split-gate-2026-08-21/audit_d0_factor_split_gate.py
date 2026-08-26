#!/usr/bin/env python3
"""Independent exact replay of the D0 factor-split involution and unit gate."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
EXPORTER = HERE / "export_and_audit_d0_factor_split_gate.py"
EXPORT = HERE / "results_d0_factor_split_gate_export.json"
RUN = HERE / "results_d0_factor_split_exact_run.json"
OUTPUT = HERE / "d0_A_U2_three_cofactor_pivot_open_char0.out"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def load_module():
    spec = importlib.util.spec_from_file_location("d0_factor_split_exporter_audit",
                                                  EXPORTER)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    require(spec.loader is not None, "missing exporter loader")
    spec.loader.exec_module(module)
    return module


def main():
    E = load_module()
    export = json.loads(EXPORT.read_text())
    frozen_logical = export.pop("logical_sha256")
    require(logical_hash(export) == frozen_logical,
            "export logical digest mismatch")
    run = json.loads(RUN.read_text())
    require(run["timeout_seconds"] == 600 and run["returncode"] == 0,
            "exact run did not use the required successful 600s gate")
    require(digest(OUTPUT) == run["output_sha256"], "output digest mismatch")
    require(OUTPUT.read_text().rstrip().endswith("[1]:"),
            "exact characteristic-zero basis is not [1]")
    require(export["gate"]["sha256"] == run["input_sha256"],
            "gate input digest mismatch")
    involution = export["involution"]
    require(involution["packet_covariant"], "minimal packet covariance failed")
    require(involution["packet0_to_packet1_set"] ==
            ["cofactor_1_3", "cofactor_3_3", "cofactor_4_3"],
            "wrong involutive mate packet")

    # Rebuild the raw exact objects, independently of the JSON relation claims.
    variables, residual, _ = E.P.P.derive()
    b0, d1, d4, a0, a5 = variables
    variables3 = (b0, d1, d4)
    equations = [value for _, value in residual]
    matrix, _ = E.sp.linear_eq_to_matrix(equations, [a0, a5])
    pivot = E.sp.primitive(E.sp.Poly(matrix[[1, 4], :].det(),
                                     *variables3))[1].as_expr()
    factors = json.loads(E.FACTOR_RESULT.read_text())["exact_pairwise_factorization"]
    A = E.decode_ledger(factors["A"], *variables3)
    B = E.decode_ledger(factors["B"], *variables3)
    U = [E.decode_ledger(row, *variables3)
         for row in factors["reduced_rows_U0_U1_U2_U3"]]
    exact_checks = {
        "A_to_B": E.relation(A, B, variables3),
        "B_to_A": E.relation(B, A, variables3),
        "U2_to_U1": E.relation(U[2], U[1], variables3),
        "U1_to_U2": E.relation(U[1], U[2], variables3),
        "pivot_to_pivot": E.relation(pivot, pivot, variables3),
    }
    for label, value in exact_checks.items():
        require(value == involution[label], f"exact involution replay failed: {label}")

    # Must-fire controls: one coefficient mutation must destroy Laurent
    # covariance; changing the unit output or the mate packet must be rejected.
    mutated = E.image_dict(A, variables3)
    first = min(mutated)
    mutated[first] += 1
    require(E.normalized_relation(mutated, E.term_dict(B, variables3)) is None,
            "coefficient mutation failed to fire")
    require(not "[1]:" in OUTPUT.read_text().replace("[1]:", "[b0]:"),
            "unit-output mutation failed to fire")
    wrong_packet = set(involution["packet0_to_packet1_set"])
    wrong_packet.remove("cofactor_1_3")
    require(wrong_packet != {"cofactor_1_3", "cofactor_3_3", "cofactor_4_3"},
            "packet mutation failed to fire")

    result = {
        "status": "exact D0 factor-split representative gate PASS",
        "export_logical_sha256": frozen_logical,
        "input_sha256": run["input_sha256"],
        "output_sha256": run["output_sha256"],
        "exact_relations": exact_checks,
        "mutation_controls": ["coefficient", "unit_output", "packet_label"],
        "theorem": ("On the D0=0,C0!=0,selected-pivot-open reduced chart, "
                    "A=U2=0 plus literal Cof(1,3),Cof(2,3),Cof(3,3) is empty. "
                    "The exact Laurent involution closes B=U1=0 with the "
                    "involutive minimal packet Cof(1,3),Cof(3,3),Cof(4,3)."),
        "scope_guard": ("The A,B-open component U0=U1=U2=U3=0 is untouched; "
                        "nothing here closes the pivot-zero or D0/C0 boundary."),
    }
    result["logical_sha256"] = logical_hash(result)
    (HERE / "results_d0_factor_split_gate_audit.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 factor split exact audit PASS", result["logical_sha256"])


if __name__ == "__main__":
    main()
