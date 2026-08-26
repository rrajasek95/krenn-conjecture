#!/usr/bin/env python3
"""Export the exact A=B pairwise-factor intersection on the pivot-open chart."""

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
RESULT = HERE / "results_d0_alternative_resultant_gcd.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main():
    module = load("d0_pairwise_factor_source", SOURCE)
    sp = module.sp
    variables, residual, _ = module.P.derive()
    b0, d1, d4, a0, a5 = variables
    equations = [value for _, value in residual]
    matrix, _ = sp.linear_eq_to_matrix(equations, [a0, a5])
    pivot = sp.primitive(sp.Poly(matrix[[1,4],:].det(),b0,d1,d4))[1].as_expr()
    data = json.loads(RESULT.read_text())["exact_pairwise_factorization"]

    def decode(name):
        answer = sp.Integer(0)
        for term in data[name]["coefficient_ledger"]:
            e0,e1,e2 = term["monomial_b0_d1_d4"]
            answer += term["coefficient"]*b0**e0*d1**e1*d4**e2
        return sp.expand(answer)
    A, B = decode("A"), decode("B")
    z = sp.Symbol("z")
    rab = sp.expand(z*pivot-1)
    encode = lambda value: str(value).replace("**","^")
    target = HERE / "d0_pairwise_AB_pivot_open_char0.msolve"
    target.write_text("z,b0,d1,d4\n0\n" +
                      ",\n".join(map(encode,(A,B,rab))) + "\n")
    out = {
        "input": target.name,
        "input_sha256": sha256(target.read_bytes()).hexdigest(),
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "factor_result_logical_sha256": json.loads(RESULT.read_text())["logical_sha256"],
        "A": encode(A), "B": encode(B),
        "pivot_terms": len(sp.Poly(pivot,b0,d1,d4).terms()),
        "row_count": 3,
        "scope": "Exact A=B intersection localized only at the selected pivot.",
    }
    logical=json.dumps(out,sort_keys=True,separators=(",",":"))
    out["logical_sha256"]=sha256(logical.encode()).hexdigest()
    path=HERE/"results_d0_pairwise_factor_component_export.json"
    path.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("D0 pairwise component export PASS",out["logical_sha256"])


if __name__ == "__main__":
    main()
