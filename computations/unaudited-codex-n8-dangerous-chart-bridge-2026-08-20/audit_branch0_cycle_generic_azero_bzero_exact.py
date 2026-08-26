#!/usr/bin/env python3
"""Independent referee for the exact A=B=0 positive-dimensional sentinel."""

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
EXPORTER = HERE / "export_branch0_cycle_generic_azero_bzero_exact.py"
INPUT = HERE / "branch0_cycle_generic_azero_bzero_exact.msolve"
OUTPUT = HERE / "results_branch0_cycle_generic_azero_bzero_exact_msolve.param.out"
MANIFEST = HERE / "results_branch0_cycle_generic_azero_bzero_exact_msolve.manifest.json"
RESULT = HERE / "results_branch0_cycle_generic_azero_bzero_exact_audit.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load(path: Path):
    spec = importlib.util.spec_from_file_location("generic_azero_bzero_referee", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load(EXPORTER)


def main() -> None:
    rows, labels, metadata = SOURCE.SOURCE.derive()
    source_rows = tuple(rows[:6])
    b0, b1, b3, d1, d3, d4 = SOURCE.SOURCE.SOURCE.PARAMETERS
    z = sp.Symbol("z")
    normalized_t013 = sp.cancel(source_rows[1]/d4)
    a_divisor = sp.cancel(sp.diff(normalized_t013, b3)/(2*b0))
    b_polynomial = sp.cancel(normalized_t013.subs(b3, 0)/2)
    delta = b1*d3+b3*d1*d4
    d0 = d1*d4+d3
    bplus = b1+d1
    live = sp.expand(b0*b1*b3*d1*d3*d4*delta*d0*bplus)
    expected = (*source_rows, a_divisor, b_polynomial, sp.expand(z*live-1))

    lines = INPUT.read_text().splitlines()
    require(lines[0] == "b0,b1,b3,d1,d3,d4,z" and lines[1] == "0",
            "canonical header changed")
    body = "\n".join(lines[2:])
    require("(" not in body and "**" not in body,
            "canonical strict syntax failed")
    encoded = body.rstrip().split(",\n")
    require(len(encoded) == 9, "canonical row count changed")
    local = {str(v): v for v in (b0, b1, b3, d1, d3, d4, z)}
    actual = tuple(sp.expand(sp.sympify(row.replace("^", "**"), locals=local))
                   for row in encoded)
    for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
        require(sp.expand(left-right) == 0, f"canonical row {index} changed")
    require(sp.expand(sp.diff(actual[-1], z)-live) == 0
            and sp.expand(actual[-1].subs(z, 0)+1) == 0,
            "Rabinowitsch sentinel replay failed")
    require(sp.cancel(live/(b0*b1*b3*d1*d3*d4*delta*d0*bplus)) == 1,
            "live product changed")
    require(sp.expand(a_divisor) == actual[6]
            and sp.expand(b_polynomial) == actual[7], "A/B rows changed")

    # Hostile source mutation fires before the engine sentinel is consulted.
    poly = sp.Poly(source_rows[5], b0, b1, b3, d1, d3, d4)
    monomial, coefficient = poly.terms()[0]
    mutation = source_rows[5] - 2*coefficient*sp.prod(
        variable**power for variable, power in
        zip((b0, b1, b3, d1, d3, d4), monomial, strict=True))
    require(sp.expand(mutation-actual[5]) != 0,
            "hostile source mutation did not fire")

    require(OUTPUT.read_text() == "[1, 7, -1, []]:\n",
            "exact positive-dimensional sentinel changed")
    manifest = json.loads(MANIFEST.read_text())
    require(manifest["status"] == "completed_characteristic_zero_parametrization"
            and manifest["characteristic_zero_explicit_opt_in"] is True,
            "exact runner status changed")
    require(manifest["solution"] == {"degree": None,
                                      "kind": "positive_dimensional",
                                      "variable_count": 7},
            "positive-dimensional envelope changed")
    require(manifest["input"]["sha256"] == sha256(INPUT.read_bytes()).hexdigest()
            and manifest["output"]["sha256"] == sha256(OUTPUT.read_bytes()).hexdigest(),
            "runner hashes changed")

    result = {
        "status": "UNAUDITED exact-Q positive-dimensional sentinel replay",
        "statement": (
            "The direct A=B=0 localized source core is positive-dimensional "
            "according to the exact characteristic-zero gate; no component "
            "parametrization or exact Krull dimension is extracted."),
        "source_labels": labels[:6],
        "source_omitted_sha256": metadata["omitted_sha256"],
        "input_sha256": sha256(INPUT.read_bytes()).hexdigest(),
        "output_sha256": sha256(OUTPUT.read_bytes()).hexdigest(),
        "literal_output": OUTPUT.read_text().strip(),
        "runner_logical_sha256": manifest["logical_sha256"],
        "elapsed_seconds": manifest["elapsed_seconds"],
        "signature": {"ambient_variables_including_inverse": 7,
                      "kind": "positive_dimensional", "degree": None},
        "scope_guard": "Q4098 is untouched; no full-source counterexample is claimed.",
        "source_mutation": "PASS",
        "sentinel_replay": "PASS",
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("generic A=B=0 exact sentinel referee: PASS")
    print("runner logical sha256:", manifest["logical_sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
