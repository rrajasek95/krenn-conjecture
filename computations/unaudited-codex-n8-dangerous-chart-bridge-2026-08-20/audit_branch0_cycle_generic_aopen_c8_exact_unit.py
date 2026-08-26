#!/usr/bin/env python3
"""Independent source/sentinel referee for the exact A-open/C8 unit."""

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
EXPORTER = HERE / "export_branch0_cycle_generic_aopen_c8_exact.py"
INPUT = HERE / "branch0_cycle_generic_aopen_c8_exact.msolve"
OUTPUT = HERE / "results_branch0_cycle_generic_aopen_c8_exact_msolve.param.out"
MANIFEST = HERE / "results_branch0_cycle_generic_aopen_c8_exact_msolve.manifest.json"
RESULT = HERE / "results_branch0_cycle_generic_aopen_c8_exact_unit_audit.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load(path: Path):
    spec = importlib.util.spec_from_file_location("generic_aopen_c8_referee", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load(EXPORTER)


def parse_input():
    lines = INPUT.read_text().splitlines()
    require(len(lines) >= 4 and lines[1] == "0", "characteristic-zero header changed")
    variables = tuple(sp.Symbol(name) for name in lines[0].split(","))
    body = "\n".join(lines[2:])
    require("(" not in body and "**" not in body,
            "strict canonical syntax guard failed")
    encoded = body.rstrip().split(",\n")
    require(len(encoded) == 8, "canonical input row count changed")
    local = {str(variable): variable for variable in variables}
    polynomials = tuple(sp.expand(sp.sympify(row.replace("^", "**"), locals=local))
                        for row in encoded)
    return variables, encoded, polynomials


def main() -> None:
    rows, labels, metadata = SOURCE.SOURCE.derive()
    source_rows = tuple(rows[:6])
    b0, b1, b3, d1, d3, d4 = SOURCE.SOURCE.SOURCE.PARAMETERS
    z = sp.Symbol("z")
    normalized_t013 = sp.cancel(source_rows[1]/d4)
    a_divisor = sp.cancel(sp.diff(normalized_t013, b3)/(2*b0))
    c8 = (b0**2*d1*d3-b0**2*d3-b0*d1*d3*d4-b0*d1*d3
          -b0*d1*d4-b0*d3*d4-d1*d3*d4+d1*d4**2)
    delta = b1*d3+b3*d1*d4
    d0 = d1*d4+d3
    bplus = b1+d1
    live = sp.expand(b0*b1*b3*d1*d3*d4*delta*d0*bplus*a_divisor)
    expected = (*source_rows, c8, sp.expand(z*live-1))
    variables, encoded, actual = parse_input()
    require(variables == (b0, b1, b3, d1, d3, d4, z),
            "canonical variable order changed")
    for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
        require(sp.expand(left-right) == 0, f"canonical row {index} changed")

    sentinel = actual[-1]
    require(sp.expand(sp.diff(sentinel, z)-live) == 0,
            "Rabinowitsch derivative does not recover live product")
    require(sp.expand(sentinel.subs(z, 0)+1) == 0,
            "Rabinowitsch z=0 sentinel changed")
    require(sp.cancel(live/(b0*b1*b3*d1*d3*d4*delta*d0*bplus*a_divisor)) == 1,
            "localized factor product changed")

    # Hostile mutation of the source-derived Cof(3,3) row must be visible in
    # the canonical input before any engine output is consulted.
    mutated = sp.Poly(source_rows[5], b0, b1, b3, d1, d3, d4)
    terms = mutated.terms()
    monomial, coefficient = terms[0]
    mutation = source_rows[5] - 2*coefficient*sp.prod(
        variable**power for variable, power in
        zip((b0, b1, b3, d1, d3, d4), monomial, strict=True))
    require(sp.expand(mutation-actual[5]) != 0,
            "hostile source mutation did not fire")

    require(OUTPUT.read_text() == "[-1]:\n", "exact output is not literal [-1]")
    manifest = json.loads(MANIFEST.read_text())
    require(manifest["status"] == "completed_characteristic_zero_parametrization"
            and manifest["characteristic_zero_explicit_opt_in"] is True,
            "exact runner status changed")
    require(manifest["solution"] == {"degree": 0, "kind": "empty",
                                      "variable_count": 7},
            "exact empty solution envelope changed")
    require(manifest["input"]["sha256"] == sha256(INPUT.read_bytes()).hexdigest()
            and manifest["output"]["sha256"] == sha256(OUTPUT.read_bytes()).hexdigest(),
            "runner input/output hash changed")
    require("A-open C8 direct seven-row source core" in manifest["scope"],
            "runner scope changed")

    result = {
        "status": "UNAUDITED exact-Q source-replayed UNIT",
        "theorem": (
            "The direct generic cycle source core has no solution on "
            "Delta*D0*Bplus*b0*b1*b3*d1*d3*d4*A != 0 and C8=0."),
        "source_labels": labels[:6],
        "source_omitted_sha256": metadata["omitted_sha256"],
        "input_sha256": sha256(INPUT.read_bytes()).hexdigest(),
        "output_sha256": sha256(OUTPUT.read_bytes()).hexdigest(),
        "runner_logical_sha256": manifest["logical_sha256"],
        "elapsed_seconds": manifest["elapsed_seconds"],
        "literal_output": OUTPUT.read_text().strip(),
        "sentinel_replay": "PASS",
        "source_mutation": "PASS",
        "scope_guard": "Q4098 and A=0/B=0 remain open and untouched.",
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("generic A-open/C8 exact unit referee: PASS")
    print("runner logical sha256:", manifest["logical_sha256"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
