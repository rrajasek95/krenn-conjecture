#!/usr/bin/env python3
"""Assemble the exact D0 theorem ledger and expose the pivot-zero gap."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = (ROOT / "unaudited-codex-root-integration-2026-08-20" /
          "probe_branch0_cycle_d0_c0_pivot.py")
C0_RESULT = (ROOT / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
             "results_branch0_cycle_d0_cramer_exception.json")
EXHAUST = (ROOT / "unaudited-codex-d0-exhaustiveness-gcd-2026-08-21" /
           "results_d0_exhaustiveness_gcd_audit.json")
E_BRANCHES = (ROOT / "unaudited-codex-d0-branchwise-omitted-2026-08-21" /
              "results_d0_exact_char0_core_audit.json")
FACTOR_ZERO = HERE / "results_d0_factor_split_gate_audit.json"
AB_OPEN = HERE / "results_d0_AB_open_final_gate_audit.json"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def read_logical(path):
    value = json.loads(path.read_text())
    frozen = value.pop("logical_sha256")
    require(logical_hash(value) == frozen, f"logical digest mismatch: {path}")
    return value, frozen


def load_source():
    spec = importlib.util.spec_from_file_location("d0_theorem_ledger_source", SOURCE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    require(spec.loader is not None, "source loader missing")
    spec.loader.exec_module(module)
    return module


def main():
    c0_result = json.loads(C0_RESULT.read_text())
    require(c0_result["result_sha256"] ==
            "a8b5f3480b137580b6cd6751171afdc2cec5cc6505239e6cd62ba47fa776e6d0",
            "C0=0 exact closure version changed")
    require("closes only the C0=0 exception" in c0_result["scope"],
            "C0=0 scope guard changed")
    exhaust, exhaust_hash = read_logical(EXHAUST)
    e_branches, e_hash = read_logical(E_BRANCHES)
    factor_zero, factor_zero_hash = read_logical(FACTOR_ZERO)
    ab_open, ab_open_hash = read_logical(AB_OPEN)
    require(exhaust_hash ==
            "78d0f68127380ad28ea5f762b7828ed003d37c6b6457672dd35b8a958ed116a3",
            "exhaustive factor-pattern audit version changed")
    require(e_hash ==
            "4df338ae7dad51107c4fb2b1c52f9a0d6efd57938a97bb7cf6c5c5f33bb55e4c",
            "E-factor exact closure version changed")
    require(factor_zero_hash ==
            "ca262c59b932fc711889e1867d934450e12f13780e36257a15afe3bb4b953d37",
            "factor-zero gate version changed")
    require(ab_open_hash ==
            "38327726447992dc10cb13be72be798aa0c7b9d615aa2e017ed34a268a03148f",
            "AB-open gate version changed")
    require("A=0,U2=0" in exhaust["remaining_gap"] and
            "B=0,U1=0" in exhaust["remaining_gap"],
            "residual case split changed")
    require("selected-pivot-open" in factor_zero["theorem"],
            "factor-zero pivot scope was lost")
    require("selected pivot" in ab_open["theorem"],
            "AB-open pivot scope was lost")

    # Exact source check of what remains of the selected pivot on C0!=0.
    # The cleared determinant contains C0^2 and declared Laurent monomials,
    # but also a positive-degree residual factor.  Thus its zero boundary
    # cannot be silently identified with the already-closed C0=0 face.
    source = load_source()
    variables, residual, c0 = source.P.derive()
    b0, d1, d4, a0, a5 = variables
    equations = [value for _, value in residual]
    matrix, _ = source.sp.linear_eq_to_matrix(equations, [a0, a5])
    pivot = source.sp.primitive(source.sp.Poly(
        matrix[[1, 4], :].det(), b0, d1, d4))[1].as_expr()
    cleared = source.sp.expand(b0 * d1**5 * d4**3 * c0**2)
    quotient, remainder = source.sp.div(source.sp.Poly(pivot, b0, d1, d4),
                                         source.sp.Poly(cleared, b0, d1, d4))
    require(remainder.is_zero, "declared C0/live factors do not divide selected pivot")
    require(quotient.total_degree() > 0 and len(quotient.terms()) > 1,
            "selected pivot has no residual boundary after C0/live localization")
    residual_factorization = source.sp.factor_list(quotient.as_expr())[1]
    require(len(residual_factorization) == 4 and
            all(multiplicity == 1 for _, multiplicity in residual_factorization),
            "selected-pivot residual factorization changed")
    require("pivot-zero complement is always out of scope" in SOURCE.read_text(),
            "upstream pivot-zero scope guard disappeared")

    result = {
        "status": "D0 theorem ledger PASS with one explicit open face",
        "closed": [
            {"stratum": "D0=0,C0=0", "digest": c0_result["result_sha256"]},
            {"stratum": "D0=0,C0!=0,selected-pivot!=0,E-factor subcomponents",
             "digest": e_hash, "note": "exactly closed but redundant after full case split"},
            {"stratum": "D0=0,C0!=0,selected-pivot!=0,A=0,U2=0",
             "digest": factor_zero_hash},
            {"stratum": "D0=0,C0!=0,selected-pivot!=0,B=0,U1=0",
             "digest": factor_zero_hash, "via": "exact Laurent involution"},
            {"stratum": ("D0=0,C0!=0,selected-pivot!=0,A*B!=0,"
                          "U0=U1=U2=U3=0"), "digest": ab_open_hash},
        ],
        "exhaustive_only_after_localization": {
            "digest": exhaust_hash,
            "cases": ["A=0,U2=0", "B=0,U1=0",
                      "A*B!=0,U0=U1=U2=U3=0"],
        },
        "open": ["D0=0,C0!=0,selected-pivot=0"],
        "selected_pivot_factorization": {
            "cleared_live_C0_factor": "b0*d1^5*d4^3*C0^2",
            "residual_terms": len(quotient.terms()),
            "residual_total_degree": quotient.total_degree(),
            "irreducible_factor_count": len(residual_factorization),
        },
        "conclusion": ("The selected-pivot-open D0=0 cycle subtree is exact-closed. "
                       "The entire D0=0 subtree cannot yet be marked closed because "
                       "the C0!=0,selected-pivot=0 complement has no certificate."),
        "mutation_control": ("Identifying pivot=0 with C0=0 must fire because the "
                             "cleared determinant has a nonconstant four-factor "
                             "quotient after removing C0^2 and declared live monomials."),
    }
    result["logical_sha256"] = logical_hash(result)
    (HERE / "results_d0_theorem_ledger.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("D0 theorem ledger PASS", result["logical_sha256"])
    print("OPEN:", result["open"][0])


if __name__ == "__main__":
    main()
