#!/usr/bin/env python3
"""Referee A=B=0 plus literal Cof(4,3) positive-dimensional sentinel."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))
import sympy as sp


HERE = Path(__file__).resolve().parent
EXPORTER = HERE / "export_branch0_cycle_generic_azero_bzero_cofactor43_exact.py"
INPUT = HERE / "branch0_cycle_generic_azero_bzero_cofactor43_exact.msolve"
OUTPUT = HERE / "results_branch0_cycle_generic_azero_bzero_cofactor43_exact_msolve.param.out"
MANIFEST = HERE / "results_branch0_cycle_generic_azero_bzero_cofactor43_exact_msolve.manifest.json"
RESULT = HERE / "results_branch0_cycle_generic_azero_bzero_cofactor43_exact_audit.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load(path: Path):
    spec = importlib.util.spec_from_file_location("generic_ab_cof43_referee", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load(EXPORTER)


def main() -> None:
    rows, labels, metadata = SOURCE.SOURCE.SOURCE.derive()
    source_rows = tuple(rows[:6])
    b0, b1, b3, d1, d3, d4 = SOURCE.SOURCE.SOURCE.SOURCE.PARAMETERS
    z = sp.Symbol("z")
    normalized_t013 = sp.cancel(source_rows[1]/d4)
    a_divisor = sp.cancel(sp.diff(normalized_t013, b3)/(2*b0))
    b_polynomial = sp.cancel(normalized_t013.subs(b3, 0)/2)
    cofactor43, cofactor43_source_sha = SOURCE.derive_cofactor43()
    delta = b1*d3+b3*d1*d4
    d0 = d1*d4+d3
    bplus = b1+d1
    live = sp.expand(b0*b1*b3*d1*d3*d4*delta*d0*bplus)
    expected = (*source_rows, a_divisor, b_polynomial, cofactor43,
                sp.expand(z*live-1))

    lines = INPUT.read_text().splitlines()
    require(lines[0] == "b0,b1,b3,d1,d3,d4,z" and lines[1] == "0",
            "canonical header changed")
    body = "\n".join(lines[2:])
    require("(" not in body and "**" not in body,
            "canonical strict syntax failed")
    encoded = body.rstrip().split(",\n")
    require(len(encoded) == 10, "canonical row count changed")
    local = {str(v): v for v in (b0, b1, b3, d1, d3, d4, z)}
    actual = tuple(sp.expand(sp.sympify(row.replace("^", "**"), locals=local))
                   for row in encoded)
    for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
        require(sp.expand(left-right) == 0, f"canonical row {index} changed")
    require(sp.expand(sp.diff(actual[-1], z)-live) == 0
            and sp.expand(actual[-1].subs(z, 0)+1) == 0,
            "Rabinowitsch sentinel replay failed")
    require(len(sp.Poly(actual[8], b0, b1, b3, d1, d3, d4).terms()) == 472,
            "literal Cof(4,3) row profile changed")

    # The exporter itself replays a literal Cof(4,3) source mutation; an
    # additional canonical-row mutation must also be visible here.
    poly = sp.Poly(actual[8], b0, b1, b3, d1, d3, d4)
    monomial, coefficient = poly.terms()[0]
    mutation = actual[8] - 2*coefficient*sp.prod(
        variable**power for variable, power in
        zip((b0, b1, b3, d1, d3, d4), monomial, strict=True))
    require(sp.expand(mutation-cofactor43) != 0,
            "hostile Cof(4,3) mutation did not fire")

    require(OUTPUT.read_text() == "[1, 7, -1, []]:\n",
            "exact positive-dimensional sentinel changed")
    manifest = json.loads(MANIFEST.read_text())
    require(manifest["status"] == "completed_characteristic_zero_parametrization"
            and manifest["solution"] == {"degree": None,
                                          "kind": "positive_dimensional",
                                          "variable_count": 7},
            "exact positive-dimensional envelope changed")
    require(manifest["input"]["sha256"] == sha256(INPUT.read_bytes()).hexdigest()
            and manifest["output"]["sha256"] == sha256(OUTPUT.read_bytes()).hexdigest(),
            "runner hashes changed")

    result = {
        "status": "UNAUDITED exact-Q positive-dimensional necessary core",
        "statement": (
            "Adding literal Cof(4,3) to the A=B=0 generic necessary core "
            "still yields a positive-dimensional exact gate. This is not a "
            "full packet point or counterexample."),
        "source_labels": labels[:6],
        "source_cofactor33_sha256": metadata["omitted_sha256"],
        "source_cofactor43_sha256": cofactor43_source_sha,
        "input_sha256": sha256(INPUT.read_bytes()).hexdigest(),
        "output_sha256": sha256(OUTPUT.read_bytes()).hexdigest(),
        "literal_output": OUTPUT.read_text().strip(),
        "runner_logical_sha256": manifest["logical_sha256"],
        "elapsed_seconds": manifest["elapsed_seconds"],
        "signature": {"ambient_variables_including_inverse": 7,
                      "kind": "positive_dimensional", "degree": None},
        "scope_guard": (
            "Other omitted lower cofactors and Q4098 remain untested; no full "
            "source solution is claimed."),
        "source_and_mutation_replay": "PASS",
        "sentinel_replay": "PASS",
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("generic A=B=0 + Cof(4,3) exact referee: PASS")
    print("runner logical sha256:", manifest["logical_sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
